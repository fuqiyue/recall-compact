from pathlib import Path
import importlib.util
import tempfile
import unittest
from unittest.mock import patch
import sys

SPEC = importlib.util.spec_from_file_location("compact_install", Path(__file__).parents[1] / "scripts" / "install.py")
install = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = install
SPEC.loader.exec_module(install)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        test_root = Path(__file__).resolve().parents[1] / ".test-tmp"
        test_root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="recall-compact-", dir=test_root)
        assert Path(self.temp.name).resolve().parent == test_root.resolve()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.source = root / "source"
        self.skills = root / "skills"
        self.upstream = root / "upstream" / "SKILL.md"
        self.entry = root / "installed" / "recall" / "SKILL.md"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("---\nname: recall-compact\n---\n", encoding="utf-8")
        self.upstream.parent.mkdir()
        self.upstream.write_text("---\nname: recall\n---\n# Upstream\n", encoding="utf-8")
        self.entry.parent.mkdir(parents=True)
        self.original = ("---\r\nname: recall\r\n---\r\n# Recall 本机入口\r\n"
                         f"[维护源 SKILL.md]({self.upstream.as_posix()})\r\n").encode("utf-8")
        self.entry.write_bytes(self.original)
        self.upstream_bytes = self.upstream.read_bytes()

    def plan(self, action="install"):
        return install.build_plan(action, self.source, self.skills, self.entry, self.upstream)

    def enable(self):
        install.apply_plan(self.plan())

    def test_preview_has_no_side_effects(self):
        self.assertEqual(3, len(self.plan()))
        self.assertFalse(self.skills.exists())
        self.assertEqual(self.original, self.entry.read_bytes())

    def test_install_and_repeat_are_idempotent(self):
        self.enable()
        self.assertEqual([], self.plan())
        self.assertEqual(1, self.entry.read_bytes().count(install.BEGIN.encode()))
        self.assertEqual(self.upstream_bytes, self.upstream.read_bytes())
        pointer = (self.skills / "recall-compact" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn((self.source / "SKILL.md").as_uri(), pointer)

    def test_uninstall_restores_exact_original_and_is_repeatable(self):
        self.enable()
        install.apply_plan(self.plan("uninstall"))
        self.assertEqual(self.original, self.entry.read_bytes())
        self.assertEqual([], self.plan("uninstall"))
        self.assertFalse((self.skills / "recall-compact" / "SKILL.md").exists())
        self.assertEqual(self.upstream_bytes, self.upstream.read_bytes())

    def test_uninstall_keeps_user_additions(self):
        self.enable()
        extra = "\n用户后来添加的配置\n".encode("utf-8")
        self.entry.write_bytes(self.entry.read_bytes() + extra)
        install.apply_plan(self.plan("uninstall"))
        self.assertEqual(self.original + extra, self.entry.read_bytes())

    def test_bom_and_crlf_are_preserved(self):
        self.original = b"\xef\xbb\xbf" + self.original
        self.entry.write_bytes(self.original)
        self.enable()
        install.apply_plan(self.plan("uninstall"))
        self.assertEqual(self.original, self.entry.read_bytes())

    def test_source_cannot_be_install_entry(self):
        with self.assertRaises(install.InstallError):
            install.build_plan("install", self.source, self.skills, self.upstream, self.upstream)

    def test_unrelated_recall_file_is_rejected(self):
        self.entry.write_text("---\nname: recall\n---\n# Full unrelated skill", encoding="utf-8")
        with self.assertRaises(install.InstallError):
            self.plan()
        self.assertFalse(self.skills.exists())

    def test_unknown_compact_file_is_not_overwritten(self):
        target = self.skills / "recall-compact" / "SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text("User skill", encoding="utf-8")
        with self.assertRaises(install.InstallError):
            self.plan()
        self.assertEqual("User skill", target.read_text(encoding="utf-8"))
        self.assertEqual(self.original, self.entry.read_bytes())

    def test_modified_pairing_is_not_removed(self):
        self.enable()
        self.entry.write_bytes(self.entry.read_bytes().replace("默认联用".encode(), b"edited"))
        with self.assertRaises(install.InstallError):
            self.plan("uninstall")

    def test_missing_end_marker_is_not_ignored(self):
        self.enable()
        self.entry.write_bytes(self.entry.read_bytes().replace(install.END.encode(), b""))
        with self.assertRaises(install.InstallError):
            self.plan()

    def test_stale_plan_does_not_change_any_file(self):
        changes = self.plan()
        self.entry.write_bytes(self.original + b"new user edit")
        with self.assertRaises(install.InstallError):
            install.apply_plan(changes)
        self.assertFalse(self.skills.exists())

    def test_missing_upstream_never_installs_half_configuration(self):
        self.upstream.unlink()
        with self.assertRaises(install.InstallError):
            self.plan()
        self.assertFalse(self.skills.exists())

    def test_mid_install_failure_rolls_back_own_writes(self):
        real_write = install.atomic_write
        calls = 0

        def failing_write(path, value):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated interrupted write")
            return real_write(path, value)

        with patch.object(install, "atomic_write", side_effect=failing_write):
            with self.assertRaises(OSError):
                install.apply_plan(self.plan())
        self.assertEqual(self.original, self.entry.read_bytes())
        self.assertFalse((self.skills / "recall-compact" / "SKILL.md").exists())

    def test_uninstall_is_planned_to_unpair_before_removal(self):
        self.enable()
        self.assertEqual(self.entry, self.plan("uninstall")[0].path)

    def test_concurrent_edit_is_kept_when_remaining_install_rolls_back(self):
        real_write = install.atomic_write
        target = self.skills / "recall-compact" / "SKILL.md"
        user_edit = b"concurrent user edit"
        calls = 0

        def editing_write(path, value):
            nonlocal calls
            calls += 1
            if calls == 2:
                target.write_bytes(user_edit)
                raise OSError("simulated interruption after user edit")
            return real_write(path, value)

        with patch.object(install, "atomic_write", side_effect=editing_write):
            with self.assertRaises(OSError):
                install.apply_plan(self.plan())
        self.assertEqual(user_edit, target.read_bytes())
        self.assertEqual(self.original, self.entry.read_bytes())

    def test_uninstall_preserves_unrelated_files_in_target_directory(self):
        self.enable()
        extra = self.skills / "recall-compact" / "user-notes.txt"
        extra.write_bytes(b"keep this file")
        install.apply_plan(self.plan("uninstall"))
        self.assertEqual(b"keep this file", extra.read_bytes())
        self.assertEqual(self.original, self.entry.read_bytes())

    def test_changed_ui_metadata_is_preserved(self):
        self.enable()
        ui = self.skills / "recall-compact" / "agents" / "openai.yaml"
        ui.write_text("user change", encoding="utf-8")
        with self.assertRaises(install.InstallError):
            self.plan("uninstall")
        self.assertEqual("user change", ui.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
