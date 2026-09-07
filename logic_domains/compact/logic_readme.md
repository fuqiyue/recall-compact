# 上下文与安装领域

## 文档控制

- module_id: MOD-COMPACT
- scope: logic_domains/compact
- scope_path: logic_domains/compact
- parent_module_id: MOD-ROOT
- membership: in-system
- scope_type: domain
- layer: runtime-code
- module_doc_policy: paired
- owner: self
- governance_mode: personal
- governance_ref: git:https://github.com/fuqiyue/recall-compact@main
- governance_evidence: git:https://github.com/fuqiyue/recall-compact@main
- governance_verification: recorded
- governance_verified_at: 2026-09-08
- last_verified: 2026-09-08
- review_trigger: interval:90d; event:major-refactor
- parent: ../../logic_readme.md
- owned_paths: SKILL.md, scripts/install.py, tests/test_install.py, references/design.md, references/handoff.md, references/acceptance.md
- status: active

## 范围登记与归属

- canonical_readme: logic_domains/compact/logic_readme.md
- canonical_change: logic_domains/compact/logic_change.md
- registry_status: registered

## 当前制度

| rule_id | 规则等级 | 当前有效规则/行为 | why（仅一句可审计摘要） | 决策记录 | 决策依据 | 验证证据 | validity | last_reviewed | review_owner |
|---|---|---|---|---|---|---|---|---|---|
| RULE-010 | key | 明确请求可触发切换；自动模式须同时具备可恢复阶段边界和实际上下文压力或下一阶段明显转向，刚恢复且无新进度时不再次切换 | 避免压缩循环和无效重读 | [VER](../../logic_version/records/logic_version-20260908-001-recall-compact.md) | 初始设计见 VER | 见 VER 验证方式 | valid | 2026-09-08 | self |
| RULE-011 | key | 交接保留任务、授权、已核证据、剩余动作和运行句柄；可变执行快照以当前状态替换过期下一步，已结束阶段按需留指针；恢复先核对新输入与现状，仍亲自读取 Recall 要求的根 readme/change 与命中领域 | 减少旧指令误执行，同时保留必要来源 | [VER-20260908-002](../../logic_version/records/logic_version-20260908-002-handoff-freshness.md)、[初始 VER](../../logic_version/records/logic_version-20260908-001-recall-compact.md) | user:2026-09-08 使用核查与优化；沿用初始授权边界 | 见 VER-002 语义核对与验收边界 | valid | 2026-09-08 | self |
| RULE-012 | key | 仅调用当前实际暴露且有文档的切换能力；失败不循环重试；无工具时标 prepared-only，无法可靠恢复则暂缓；安装、任务应用、切换与恢复按各自证据说明，不继承旧事件成功或把宿主自行切换归为技能主动触发 | 保持使用报告与本次实际执行相符 | [VER-20260908-002](../../logic_version/records/logic_version-20260908-002-handoff-freshness.md)、[初始 VER](../../logic_version/records/logic_version-20260908-001-recall-compact.md) | user:2026-09-08 使用核查与优化；沿用初始能力边界 | 见 VER-002 语义核对与验收边界 | valid | 2026-09-08 | self |
| RULE-013 | key | 安装默认仅预览，--apply 才写；仅支持单独的 Recall 本机指针入口；技能指针采用精确所有权核对，联用块可独立移除，保留其外文本 | 防止安装修改上游或用户文件 | [VER](../../logic_version/records/logic_version-20260908-001-recall-compact.md) | 初始设计见 VER | 见 VER 验证方式 | valid | 2026-09-08 | self |

## 代码地图

| 路径/稳定锚点 | artifact_class/layer | contract_class | 职责 | 输入 | 输出 | 权威来源 | 可直接编辑 | 关联测试 |
|---|---|---|---|---|---|---|---|---|
| SKILL.md | source/runtime-code | public | 按需上下文流程入口 | 任务阶段与宿主能力 | 接续流程 | 根与本领域规则 | yes | references/acceptance.md |
| scripts/install.py | source/runtime-code | persisted | 安装、联用、预览、状态、撤销 | 显式路径参数 | 本机配置指针 | 本领域 RULE-013 | yes | tests/test_install.py |
| references/design.md | source/runtime-code | internal | 设计解释与取舍 | 当前规则 | 可阅读设计 | 根与本领域规则 | yes | 语义自审 |
| references/handoff.md | source/runtime-code | internal | 空白交接提纲 | 使用场景 | 最小交接提示 | 本领域 RULE-011 | yes | references/acceptance.md |
| tests/test_install.py | source/runtime-code | internal | 隔离安装契约验证 | 临时测试夹具 | 17 项测试结果 | 本领域 RULE-013 | yes | unittest |

## 验证

`python -m unittest discover -s tests -v`：重复安装、保留原文、撤销、拒绝源码入口、未知文件/损坏标记、只读预览、文件冲突。
行为验收见 references/acceptance.md，包含使用状态区分、旧下一步清理、新输入接续与事件证据隔离；这些场景需语义核对或实际代理运行，安装单元测试不能证明它们。没有运行时切换工具的环境只能验收 prepared-only。
