# Recall Compact 活跃变更

## 文档控制

- module_id: MOD-ROOT
- scope: .
- scope_path: .
- current_policy: logic_readme.md
- owner: self
- governance_mode: personal
- active_changes: 1
- effective: false

## 议案规则

议案不直接生效；当前制度由 logic_readme.md 定义。完成后保留 VER 决策依据，再移除本账本正文及公报行。

## 活跃议案索引

| change_id | status | scope | owner | target/summary | blocked_by | proposal_path | last_updated |
|---|---|---|---|---|---|---|---|
| CHG-20260908-001 | verifying | . | self | 独立技能与默认联用 | none | [CHG-20260908-001](logic_change.md#chg-20260908-001) | 2026-09-08 |

<a id="chg-20260908-001"></a>
## CHG-20260908-001: 独立技能与默认联用

- status: verifying
- effective: false
- recall_route: medium
- proposal_revision: 1
- owner: self
- changed_by: Codex
- scope: .
- affected_scopes: ., logic_domains/compact
- decision_confirmed_by: user
- decision_confirmed_at: 2026-09-08
- last_updated: 2026-09-08
- raw_request: user:2026-09-08 当前创建请求；独立项目、设计、GitHub、技能导入、Recall 默认联用。
- decomposition: 新建技能和设计文档；安装指针与可撤销联用；测试文件保留与重复操作；GitHub 发布。
- fit_analysis: 已核实 Recall 的上下文恢复与外部工作流接口；保留其维护源，联用仅为安装配置，无需业务规则迁移。
- decision_basis: 当前用户明确授权创建、安装、上传及默认搭配，另明确选择公开仓库；安装方式为不改变 Recall 维护源的可撤销配置。
- logic_temp: logic_version/working/recall-compact-initial/logic_temp.md
- next_action: 17 项安装测试、技能格式验证、本机安装状态及一次真实切换恢复已通过；完成决策记录和公开发布后关案。
