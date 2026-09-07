# VER-20260908-001: 独立附属技能与本机入口默认联用

## 记录控制

- version_id: VER-20260908-001
- version_slug: logic_version-20260908-001-recall-compact
- status: effective
- date: 2026-09-08
- change_id: CHG-20260908-001
- before_commit: none (新建仓库)
- after_commit: 47d61c2893d3b854feb15e596c3887ef273588b4
- recall_route: medium
- governance_mode: personal
- changed_by: Codex
- semantic_review_state: passed
- semantic_reviewed_by: self
- decision_basis: user:2026-09-08 创建、安装、公开发布及 Recall 默认搭配请求；安装方式沿用已核实的独立本机指针结构。

## 为什么做这个决策？

长任务需要在阶段转换时保留可信的执行状态，并在宿主允许时切换上下文。附属技能应独立维护，同时继续依赖 Recall 恢复消费项目的规则与授权。

需求来源仅保留稳定引用和必要提炼，不归档原始对话或真实交接。

- raw_request: user:2026-09-08 当前创建请求；独立项目、设计、GitHub、技能导入、Recall 默认联用。
- decomposition: 新建技能和设计文档；安装指针与可撤销联用；测试文件保留与重复操作；GitHub 发布。
- fit_analysis: 已核实 Recall 的上下文恢复与外部工作流接口；保留其维护源，联用仅为安装配置，无需业务规则迁移。
- intent_non_goals: 不改 Recall 上游维护源、模型或容量设置；不创建后台调度器或业务授权。
- intent_constraints: 消费项目当前规则仍由 Recall 文档决定；保留停止点和未知外部操作状态；真实交接不进入此仓库。
- intent_acceptance: 独立技能和设计可阅读；安装可检查和撤销；使用 Recall 的入口默认联用；公开仓库可获取。
- intent_status: source-derived；具体安装方法由当前本机入口的实际结构确定。
- uncertainty: 不同宿主是否提供切换工具及技能发现机制取决于实际环境；不推断实际 token 节省或 1M 容量生效。

## 决策过程

采用“独立维护源 + 本机短入口指针”。它支持按需加载、独立升级及撤销，并满足仅调用 Recall 时默认搭配的需求。

替代方案及取舍：

- 修改 Recall 上游维护源：分发更直接，但会改变上游默认行为并增加耦合，未采用。
- 只依赖附属技能的 description：没有入口改动，但无法落实单独调用 Recall 时的明确默认联用，保留为辅助发现。
- 固定阈值或每步切换：实现简单，但没有跨宿主可靠用量依据，且可能放大规则重读成本，未采用。

完整流程、触发条件、状态区分和迁移说明见 [设计](../../references/design.md)。当前制度在所属 readme，不以此记录替代。

## 影响范围

- SKILL.md 与 references/：阶段评估、交接、真实切换、恢复流程和能力边界。
- scripts/install.py：创建附属技能配置指针，为已有 Recall 指针追加短联用块；仅支持显式独立入口。
- tests/test_install.py 与 .github/workflows/validate.yml：隔离安装契约测试与 Windows/Linux、Python 3.11/3.13 CI。
- logic_readme.md、logic_domains/compact/：职责、约束、注册领域、代码地图与验证义务。
- docs_impact: 新建项目宪法、领域文档、设计、安装说明、验收提纲及本决策记录。

本机安装改动限于两个附属技能配置文件和 Recall 入口的有界联用块。未改 Recall 维护源或消费项目数据；不存在业务数据迁移。

## 验证方式

本记录在本地实现验收后创建；记录中的 after_commit 对应已验证代码。后续 GitHub Actions 结果以公开仓库的实际运行记录为准。

- `python -B -X utf8 -m unittest discover -s tests -v`：17/17 通过。覆盖只读预览、幂等安装、字节级原文保留、BOM/CRLF、撤销、未知文件/损坏标记拒绝、中断回滚和并发编辑保留。
- Codex skill-creator `quick_validate.py`：维护源与已安装附属技能入口均通过。
- 安装器 `status`：本机实际返回 `INSTALLED_AND_PAIRED`；上游 Recall 源文件 SHA-256 与安装前一致，上游 Git 工作区保持干净。
- 真实接续验收：在本次开发环境保存交接后调用实际提供的 `functions.new_context`；进入新上下文后恢复目标及授权，重读根规则和账本，通过 Recall 路由加载命中领域，再继续发布工作。prepared、requested、confirmed、resumed 四个阶段有本次运行证据。
- 语义自审：确认摘要不会晋升议案，未知外部操作不得重放，无宿主能力时不冒充成功，刚恢复不重复触发，联用入口不递归加载。
- 临时验证依赖及测试目录已按限定绝对路径清理；实际交接从未写入技能仓库或安装配置。

运行时验收仅证明当前工具环境的一次完整接续；未证明其他客户端均支持相同工具、全部行为场景已实测、节省固定比例或模型容量配置生效。

## 回滚方式

使用原安装时相同的路径参数运行 `scripts/install.py uninstall` 预览，再加 `--apply`。先移除所拥有的联用块，再删除精确匹配的附属技能配置；保留块外用户编辑及其他文件。

若配置已被用户改动，安装器拒绝覆盖，应先核对差异。移动源目录前先撤销；撤销不会删除源项目、消费项目记录或真实交接。

## 关联

- current_logic: [根规则](../../logic_readme.md#当前制度)、[领域规则](../../logic_domains/compact/logic_readme.md#当前制度)
- promoted_rule_ids: RULE-001, RULE-002, RULE-003, RULE-004, RULE-010, RULE-011, RULE-012, RULE-013
- intent_traceability: INT-20260908-001/002 -> RULE-001..004/010..013 -> tests/test_install.py 与 references/acceptance.md -> VER-20260908-001
- proposal_revision: 1
