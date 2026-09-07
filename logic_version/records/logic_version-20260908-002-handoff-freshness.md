# VER-20260908-002: 使用证据与交接时效性

## 记录控制

- version_id: VER-20260908-002
- version_slug: logic_version-20260908-002-handoff-freshness
- status: effective
- date: 2026-09-08
- change_id: CHG-20260908-002
- before_commit: ae9c491e2716264c425d6cad57129f998dcc87de
- after_commit: 32d8d24d76738833b5d8c68f7108045d5ee8e35f
- recall_route: medium
- governance_mode: personal
- changed_by: Codex
- proposal_revision: 1
- semantic_review_state: passed
- semantic_reviewed_by: self

## 为什么做这个决策？

本机入口配对只能证明配置成立，不能证明单个任务实际应用。已有 [初始验收](logic_version-20260908-001-recall-compact.md) 证明过当前工具环境的一次切换和恢复；需要保持结论范围，并让后续接续明确采用当前状态。

- raw_request: user:2026-09-08 本次使用核查与优化请求。
- decomposition: 核实本机安装与已完成的运行验收；明确使用证据口径；精简并刷新交接状态；补充行为验收。
- fit_analysis: 沿用 INT-20260908-001 与 FLOW-001，细化交接和恢复步骤，不改变触发条件、安装契约或消费项目授权。
- intent_non_goals: 不修改 Recall 维护源、模型设置或消费项目；不增加后台监控和强制切换。
- intent_constraints: 保留当前用户输入与已有授权；交接不复制项目制度；不上传真实交接或对话。
- intent_acceptance: 使用结论有对应证据；恢复先核对最新请求；旧阶段动作不再作为当前下一步；安装仍可联用。
- intent_status: source-derived
- decision_basis: 当前用户已授权依据实际优化，采用既有最小交接与可信报告原则的局部细化，无未决长期选择。

## 决策过程

采用当前执行快照，并替换失效的下一步；已结束阶段按需保留结果和来源。恢复先判断最新输入与原目标的关系，再核对运行状态。保留必要授权、未明操作与不可变历史。

使用证据分别对应配置、任务应用和本次切换/恢复；不从安装状态、旧事件或宿主自行切换推断本技能主动调用。沿用现有载体，不增加遥测服务。固定长度截断会损失必要边界，因此仅按下一步需要精简，不引入硬字符上限。

## 影响范围

SKILL.md、交接提纲、设计、README 使用说明、行为验收与所属领域 RULE-011/012。安装器和其配置格式保持兼容，本机指针仍指向同一维护源，无需重装；已缓存旧正文的任务需重新读取。

- docs_impact: 上述技能及说明、领域规则、决策索引；保留初始不可变记录。
- promoted_rule_ids: RULE-011, RULE-012

## 验证方式

- `python -B -X utf8 -m unittest discover -s tests -v`：17/17 通过，验证安装契约。
- skill-creator `quick_validate.py`：维护源和本机附属技能入口均通过。
- 安装器 `status`：返回 `INSTALLED_AND_PAIRED`；Recall 维护源 SHA-256 与初始验收记录一致。
- 语义自审：核对新增的 6 个 [行为场景](../../references/acceptance.md)，覆盖安装与应用区分、不强制切换、过期下一步、新输入、旧事件和宿主自行切换。场景核对不是独立代理运行测试。
- 本轮复核了原有实际切换验收；本轮未再次主动切换，未测量 token 或费用收益，也未声称其他任务均自动应用。

验证后的本次临时依赖清理由 CHG 收尾跟踪，不属于技能运行依赖，且不纳入版本控制。

## 回滚方式

按 Git 恢复本次技能和说明改动，并将所属领域规则同步恢复；本机入口、安装数据和 Recall 上游无需迁移。原验收记录保持不变。

## 关联

- current_logic: [领域规则](../../logic_domains/compact/logic_readme.md#当前制度)
- intent_traceability: INT-20260908-001 -> RULE-011/012 -> references/acceptance.md -> VER-20260908-002

