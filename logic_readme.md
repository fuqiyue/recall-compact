# Recall Compact 项目宪法

## 文档控制

- doc_id: LOGIC-RECALL-COMPACT-001
- module_id: MOD-ROOT
- scope: .
- scope_path: .
- status: active
- owner: self
- governance_mode: personal
- source_of_truth: logic_readme.md
- last_verified: 2026-09-08

## 目标与边界

为 Recall 增加按需上下文切换与可靠接续；项目规则仍由消费项目的 Recall 文档管理。维护源独立于 Recall，本机入口仅增加可撤销的联用指针。
初始需求来自 user:2026-09-08 本项目创建请求，提炼为独立目录、完整设计、GitHub 介绍、技能安装、使用 Recall 时默认搭配。

## 当前制度

| rule_id | 规则等级 | 当前有效规则/行为 | why | 决策记录 |
|---|---|---|---|---|
| RULE-001 | key | 本项目只管理上下文生命周期；消费项目规则、用户裁决、变更批准仍由该项目的 Recall 文档与当前用户授权决定 | 避免摘要成为平行制度 | [VER-20260908-001](logic_version/records/logic_version-20260908-001-recall-compact.md) |
| RULE-002 | key | 默认联用通过安装入口中的短配置指针实现；不修改上游 Recall 维护源、提供者或模型容量配置 | 保持可独立升级和撤销 | [VER-20260908-001](logic_version/records/logic_version-20260908-001-recall-compact.md) |
| RULE-003 | key | 保存摘要、请求切换、确认切换、恢复成功分别报告；没有真实环境证据不得声称完成压缩 | 保持执行报告可信 | [VER-20260908-001](logic_version/records/logic_version-20260908-001-recall-compact.md) |
| RULE-004 | ordinary | 默认联用表示阶段边界评估，不表示每步强制压缩，也不是后台调度器 | 控制重读成本并维持连贯工作 | [VER-20260908-001](logic_version/records/logic_version-20260908-001-recall-compact.md) |

## 范围登记与归属

- owned_paths: README.md, SKILL.md, AGENTS.md, logic_readme.md, logic_change.md, logic_domains/, logic_version/, references/, scripts/, tests/, .gitignore, .gitattributes
- unmapped_paths: agents/ (技能 UI 配置), .github/ (CI 配置)
- version_root: logic_version/
- temp_root: logic_version/working/

### 范围登记表

| module_id | scope_path | membership | scope_type/layer | doc_policy | logic_readme | logic_change | owner | status |
|---|---|---|---|---|---|---|---|---|
| MOD-ROOT | . | in-system | root/runtime-code | paired | [宪法](logic_readme.md) | [公报](logic_change.md) | self | active |
| MOD-COMPACT | logic_domains/compact | in-system | domain/runtime-code | paired | [领域](logic_domains/compact/logic_readme.md) | [议案](logic_domains/compact/logic_change.md) | self | active |

## 功能意图与用户流程

| intent_id | 功能入口 | intent | 关联规则 | 代码锚点 | 来源 |
|---|---|---|---|---|---|
| INT-20260908-001 | $recall / $recall-compact | 默认组合使用，阶段完成后按需减轻上下文负担并继续任务 | RULE-001..004 | SKILL.md; scripts/install.py | user:2026-09-08 |
| INT-20260908-002 | GitHub / 本地目录 | 独立维护、介绍设计、可安装与撤销 | RULE-002 | README.md; references/design.md | user:2026-09-08 |

FLOW-001：安装并联用 → Recall 恢复规则 → 执行任务 → 阶段评估 → 留下可恢复交接 → 环境切换 → 核实并继续。
UXI-001：不要求用户重复已有授权；安装联用后无需每次输入两个技能名。无法切换时如实继续任务或说明限制。

## 不可破坏约束

- INV-001：摘要不能覆盖现行规则、未决冲突或用户裁决门。
- INV-002：不能将配置容量、估算 token、已写摘要或已发起调用当作实际切换成功证据。
- INV-003：安装与撤销不得覆盖未知文件或删除用户后续编辑；上游 Recall 维护源不写入。
- INV-004：真实交接内容不进入技能仓库、安装目录或 GitHub；这里只保存公开模板和设计。

## 代码地图与验证

具体流程、安装契约、代码地图和测试归 MOD-COMPACT；根文件由本宪法登记。
验证：`python -m unittest discover -s tests -v`；技能格式用 Codex skill-creator 的 quick_validate.py；真实切换需在提供相应工具的会话验证，单元测试不证明运行时可用。
维护本项目先读根 readme/change，再用外部 Recall 的 `recall route <路径或关键词>` 路由并读取命中领域。

## 有效决策索引

[VER-20260908-001](logic_version/records/logic_version-20260908-001-recall-compact.md)：独立附属技能与本机入口联用。完整索引见 [index](logic_version/index.md)。
