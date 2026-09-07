# 上下文与安装领域活跃变更

## 文档控制

- module_id: MOD-COMPACT
- scope: logic_domains/compact
- scope_path: logic_domains/compact
- current_policy: logic_readme.md
- owner: self
- governance_mode: personal
- governance_ref: git:https://github.com/fuqiyue/recall-compact@main
- governance_evidence: git:https://github.com/fuqiyue/recall-compact@main
- governance_verification: recorded
- governance_verified_at: 2026-09-08
- last_updated: 2026-09-08
- active_changes: 1
- effective: false

## 议案规则

议案不直接生效；当前规则见 logic_readme.md，历史决策见项目决策索引。

## 讨论主题索引

| topic_id | 同类议题/共享问题 | coordinator | discussion_refs | related_changes | status |
|---|---|---|---|---|---|

## 活跃议案索引

<a id="chg-20260908-002"></a>
## CHG-20260908-002: 实际使用核验与交接时效性优化

- status: promoting
- proposal_revision: 1
- recall_route: medium
- changed_by: Codex
- scope: logic_domains/compact
- owner: self
- governance_mode: personal
- affected_scopes: SKILL.md, references/, README.md, logic_domains/compact
- based_on: commit:ae9c491e2716264c425d6cad57129f998dcc87de; RULE-003/011; VER-20260908-001
- raw_request: user:2026-09-08 本次使用核查与优化请求。
- decomposition: 核实本机安装与已完成的运行验收；明确使用证据口径；精简并刷新交接状态；补充行为验收。
- fit_analysis: 沿用 INT-20260908-001 与 FLOW-001，细化交接和恢复步骤，不改变触发条件、安装契约或消费项目授权。
- intent_non_goals: 不修改 Recall 维护源、模型设置或消费项目；不增加后台监控和强制切换。
- intent_constraints: 保留当前用户输入与已有授权；交接不复制项目制度；不上传真实交接或对话。
- intent_acceptance: 使用结论有对应证据；恢复先核对最新请求；旧阶段动作不再作为当前下一步；安装仍可联用。
- intent_status: source-derived
- decision_gate: not-required
- decision_basis: 当前请求授权依据实际优化；仅细化既有最小交接与可信报告要求，无未决长期选择。
- current_behavior: 本机 status 为 INSTALLED_AND_PAIRED；VER-20260908-001 记录当前工具环境一次实际切换与恢复。安装状态本身不证明单个任务应用。
- proposed_rule: 用当前执行快照和证据区分安装、应用与切换；恢复先核对新输入，再查询现状并继续。
- docs_impact: 技能入口、交接提纲、使用说明、设计、验收场景、所属领域规则和精简 VER。
- next_action: 格式与 17 项安装测试通过，语义自审通过；创建精简 VER、更新规则索引、清理临时依赖并关案同步。
- semantic_review_state: passed
- semantic_reviewed_by: self
- verification: 17/17 unittest；源与安装入口 quick_validate 通过；6 个新增场景已语义核对，未声称全部实际运行；本轮未再次主动切换。
- blocked_by: none
- last_updated: 2026-09-08
