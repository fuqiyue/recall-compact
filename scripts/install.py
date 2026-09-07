#!/usr/bin/env python3
"""Install local skill pointers; never perform or simulate context compaction."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
import stat
import tempfile
from dataclasses import dataclass

BEGIN = "<!-- recall-compact:begin -->"
END = "<!-- recall-compact:end -->"
SOURCE_ROOT = Path(__file__).resolve().parents[1]


class InstallError(ValueError):
    pass


@dataclass(frozen=True)
class Change:
    path: Path
    before: bytes | None
    after: bytes | None


def safe_path(path: Path) -> Path:
    path = Path(os.path.abspath(path.expanduser()))
    # Refuse symlinks/junctions in the entire existing path, including dangling links.
    for part in (path, *path.parents):
        reparse = part.exists() and bool(getattr(part.lstat(), "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))
        if part.is_symlink() or reparse:
            raise InstallError(f"Linked path is not supported: {part}")
    return path


def read_optional(path: Path) -> bytes | None:
    if path.exists() and not path.is_file():
        raise InstallError(f"Expected a file: {path}")
    return path.read_bytes() if path.exists() else None


def utf8(data: bytes, path: Path) -> str:
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise InstallError(f"Expected UTF-8: {path}") from exc


def skill_name(data: bytes, path: Path) -> str:
    text = utf8(data, path)
    front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    name = re.search(r"(?m)^name:\s*[\'\" ]?([a-z0-9-]+)[\'\" ]?\s*$",
                     front.group(1) if front else "")
    return name.group(1) if name else ""


def managed_block(source: Path) -> bytes:
    uri = source.as_uri()
    return (
        "\n\n" + BEGIN + "\n"
        f"默认联用：使用 Recall 时同时读取并应用 [$recall-compact]({uri})；"
        "本轮已加载则沿用。详细流程仅见该维护源，当前项目规则仍由 Recall 恢复。\n"
        + END + "\n"
    ).encode("utf-8")


def remove_block(data: bytes, expected: bytes) -> bytes:
    start, end = BEGIN.encode(), END.encode()
    if start not in data and end not in data:
        return data
    if data.count(start) != 1 or data.count(end) != 1 or expected not in data:
        raise InstallError("Managed pairing block is edited or malformed; refusing to overwrite.")
    return data.replace(expected, b"", 1)


def compact_pointer(source: Path) -> bytes:
    return (
        "---\nname: recall-compact\n"
        "description: 与 Recall 默认配合，在阶段边界按需整理交接并使用宿主上下文切换能力，随后恢复任务。\n"
        "---\n\n# Recall Compact 本机入口\n\n"
        f"读取并遵循 [维护源 SKILL.md]({source.as_uri()})；"
        "相对引用基于维护源目录解析。此文件仅为本机配置指针。\n"
    ).encode("utf-8")


def yaml_pointer() -> bytes:
    return (
        'interface:\n'
        '  display_name: "Recall Compact"\n'
        '  short_description: "配合 Recall 在阶段完成后按需整理交接、切换上下文并恢复任务"\n'
        '  default_prompt: "使用 $recall-compact 配合当前 Recall 按需切换上下文并继续任务。"\n'
        'policy:\n  allow_implicit_invocation: true\n'
    ).encode("utf-8")


def build_plan(action: str, source_root: Path, skills_root: Path,
               recall_entry: Path, recall_source: Path) -> list[Change]:
    source = safe_path(source_root / "SKILL.md")
    upstream = safe_path(recall_source)
    entry = safe_path(recall_entry)
    target = safe_path(skills_root / "recall-compact")
    if not source.is_file() or skill_name(source.read_bytes(), source) != "recall-compact":
        raise InstallError(f"Missing or invalid recall-compact source: {source}")
    if not upstream.is_file() or skill_name(upstream.read_bytes(), upstream) != "recall":
        raise InstallError(f"Missing or invalid Recall source: {upstream}")
    if entry == upstream or target in source.parents or target in entry.parents:
        raise InstallError("Source, installed entry, and compact target must be separate.")
    if entry.name != "SKILL.md" or entry.parent.name != "recall":
        raise InstallError("Recall entry must be a recall/SKILL.md installation pointer.")
    original = read_optional(entry)
    if original is None:
        raise InstallError(f"Recall installation entry does not exist: {entry}")
    block = managed_block(source)
    base = remove_block(original, block)
    text = utf8(base, entry)
    # Accept both existing Markdown local-path pointers and our URI pointers.
    local = upstream.as_posix()
    if (len(base) > 8192 or skill_name(base, entry) != "recall"
            or not any(value.casefold() in text.replace("\\", "/").casefold()
                       for value in (local, upstream.as_uri()))):
        raise InstallError("Recall entry must be a short pointer to the supplied Recall source.")
    entries = [
        (safe_path(target / "SKILL.md"), compact_pointer(source)),
        (safe_path(target / "agents" / "openai.yaml"), yaml_pointer()),
    ]
    changes = []
    for path, expected in entries:
        before = read_optional(path)
        if before is not None and before != expected:
            raise InstallError(f"Existing file is not the owned pointer; refusing to overwrite: {path}")
        after = expected if action == "install" else None
        if before != after:
            changes.append(Change(path, before, after))
    updated = base + block if action == "install" else base
    if updated != original:
        # Uninstall unpairs first, so a partial operation cannot leave a dangling pairing.
        change = Change(entry, original, updated)
        if action == "uninstall":
            changes.insert(0, change)
        else:
            changes.append(change)
    return changes


def atomic_write(path: Path, value: bytes | None) -> None:
    safe_path(path)
    if value is None:
        path.unlink()
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".recall-compact-", dir=path.parent)
    temp_path = Path(temp)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(value)
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def apply_plan(changes: list[Change]) -> None:
    for change in changes:
        safe_path(change.path)
        if read_optional(change.path) != change.before:
            raise InstallError(f"File changed after preview: {change.path}")
    done = []
    try:
        for change in changes:
            if read_optional(change.path) != change.before:
                raise InstallError(f"File changed during install: {change.path}")
            atomic_write(change.path, change.after)
            done.append(change)
    except Exception:
        for change in reversed(done):
            # Preserve concurrent edits; roll back only bytes this operation wrote.
            if read_optional(change.path) == change.after:
                atomic_write(change.path, change.before)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "status", "uninstall"))
    parser.add_argument("--skills-root", type=Path,
                        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills")
    parser.add_argument("--recall-entry", required=True, type=Path)
    parser.add_argument("--recall-source", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="Write the previewed configuration")
    args = parser.parse_args(argv)
    try:
        action = "install" if args.action == "status" else args.action
        changes = build_plan(action, SOURCE_ROOT, args.skills_root, args.recall_entry, args.recall_source)
        if args.action == "status":
            print("INSTALLED_AND_PAIRED" if not changes else "NOT_FULLY_INSTALLED_OR_PAIRED")
            return 0 if not changes else 1
        for change in changes:
            verb = "DELETE" if change.after is None else ("CREATE" if change.before is None else "UPDATE")
            print(f"{verb}: {change.path}")
        if args.apply:
            apply_plan(changes)
            print(f"APPLIED: {len(changes)} file(s). Upstream Recall source was not modified.")
        else:
            print(f"PREVIEW ONLY: {len(changes)} file(s); use --apply to write.")
        return 0
    except (InstallError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
