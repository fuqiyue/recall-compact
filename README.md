# Recall Compact

[![Validation](https://github.com/fuqiyue/recall-compact/actions/workflows/validate.yml/badge.svg)](https://github.com/fuqiyue/recall-compact/actions/workflows/validate.yml)

为 [Recall](https://github.com/fuqiyue/recall) 提供按需上下文切换与任务接续的独立附属技能。

长任务完成一个阶段后，保留目标、授权边界、验证证据和下一步，再调用当前运行环境提供的上下文能力。恢复时继续遵循 Recall，不要求用户重复背景。

> **保存摘要不等于已经压缩。** 本技能明确区分准备、请求、确认切换和恢复成功；没有宿主工具时如实报告未切换。

## 能做什么

- 在可恢复阶段边界结合上下文负担决定是否切换。
- 与现有 Recall 的规则、CHG、VER 和下一步记录配合。
- 通过本机入口配置，让使用 $recall 时默认搭配 recall-compact。
- 独立维护、安装与撤销；保留 Recall 上游维护源。
- 不安装后台调度器，不修改模型、容量或提供者配置。

## 安装与默认联用

需要 Python 3.11+、已安装 Recall，以及一个指向 Recall 维护源的本机 SKILL.md 入口。以下示例请按实际路径调整。

```powershell
git clone https://github.com/fuqiyue/recall-compact.git D:\vscode3\recall-compact
cd D:\vscode3\recall-compact

# 默认只预览
python scripts/install.py install --skills-root "$env:USERPROFILE\.codex\skills" --recall-entry "$env:USERPROFILE\.agents\skills\recall\SKILL.md" --recall-source "D:\vscode3\recall\SKILL.md"

# 核对后安装，并默认联用
python scripts/install.py install --skills-root "$env:USERPROFILE\.codex\skills" --recall-entry "$env:USERPROFILE\.agents\skills\recall\SKILL.md" --recall-source "D:\vscode3\recall\SKILL.md" --apply
```

安装器只增加附属技能入口与 Recall 本机入口中的短联用配置，不修改 Recall 维护源。若 Recall 安装目录中就是完整维护源，请先按你现有环境的安装方式建立单独的本机指针入口；本工具不会把完整技能改写成指针。

安装后的新任务：

```text
使用 $recall 完成这项任务。
```

入口会要求搭配附属技能。已打开的任务若仍缓存旧入口，明确要求重新读取，必要时重新加载技能或重启客户端。默认联用是入口指令，不是每个客户端都提供的强制事件 hook。

单独调用也可以：

```text
使用 $recall-compact 配合当前 Recall，在阶段完成且值得切换时整理交接、切换上下文，然后继续。
```

## 检查和撤销

使用与安装相同的三个路径参数，将 install 替换为 status 或 uninstall。status 只读；uninstall 默认预览，加 --apply 才写。
撤销保留 Recall 原有内容、用户在联用块外的后续编辑与本项目源文件；遇到未知改动会拒绝覆盖。移动本仓库前先在原路径撤销，移动后重新安装。安装路径不支持符号链接或 Windows junction。

## 环境支持

- Skill 是可复用工作流指令，不能凭空提供上下文压缩工具。
- 当前工具列表有文档化切换能力时才调用；functions.new_context 是一种特定环境接口，不保证其他客户端具备。
- 无能力时可准备交接，但不得声称实际压缩。
- 不承诺固定节省比例、1M 容量生效或账单下降。
- 安装器仅标准库；Windows/Linux/macOS 路径按宿主调整。

## 文档与开发

- [SKILL.md](SKILL.md)：代理使用入口。
- [完整设计](references/design.md)：职责、状态流程、默认联用、取舍和回滚。
- [交接提纲](references/handoff.md)：空白参考，真实数据不提交。
- [验收场景](references/acceptance.md)：可验证的行为边界。
- [项目宪法](logic_readme.md) / [领域规则](logic_domains/compact/logic_readme.md)：本项目当前规则。
- [初始设计决策](logic_version/records/logic_version-20260908-001-recall-compact.md)：理由与交付证据。

```powershell
python -m unittest discover -s tests -v
```

技能格式可用当前 Codex skill-creator 提供的 quick_validate.py 检查。测试不需要模型 API 或 GitHub 凭据。

## 相关资源

- [Recall 上游](https://github.com/fuqiyue/recall)
- [OpenAI 技能文档](https://learn.chatgpt.com/docs/build-skills)
