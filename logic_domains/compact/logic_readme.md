# 上下文与安装领域

- module_id: MOD-COMPACT
- scope_path: logic_domains/compact
- parent: ../../logic_readme.md
- owned_paths: SKILL.md, scripts/install.py, tests/test_install.py, references/design.md, references/handoff.md, references/acceptance.md
- status: active

## 当前制度

| rule_id | 规则等级 | 当前有效规则/行为 | why | 决策记录 |
|---|---|---|---|---|
| RULE-010 | key | 明确请求可触发切换；自动模式须同时具备可恢复阶段边界和实际上下文压力或下一阶段明显转向，刚恢复且无新进度时不再次切换 | 避免压缩循环和无效重读 | [VER](../../logic_version/records/logic_version-20260908-001-recall-compact.md) |
| RULE-011 | key | 交接保留任务、授权来源与范围、已核证据、剩余动作和运行中句柄；恢复时仍亲自读取 Recall 要求的根 readme/change 与命中领域 | 兼顾接续效率和设计正确性 | [VER](../../logic_version/records/logic_version-20260908-001-recall-compact.md) |
| RULE-012 | key | 仅调用当前实际暴露且有文档的运行时切换能力；失败不循环重试；缺工具时标 prepared-only，恢复信息不可靠时暂缓切换 | 技能无法创造宿主能力 | [VER](../../logic_version/records/logic_version-20260908-001-recall-compact.md) |
| RULE-013 | key | 安装默认仅预览，--apply 才写；仅支持单独的 Recall 本机指针入口；技能指针采用精确所有权核对，联用块可独立移除，保留其外文本 | 防止安装修改上游或用户文件 | [VER](../../logic_version/records/logic_version-20260908-001-recall-compact.md) |

## 代码地图

| 路径/稳定锚点 | contract_class | 职责 | 关联测试 |
|---|---|---|---|
| ../../SKILL.md | public | 按需上下文流程入口；细节引用本规则与操作参考 | references/acceptance.md |
| ../../scripts/install.py | persisted | 本机指针安装、联用、预览、状态、撤销；仅标准库 | tests/test_install.py |
| ../../references/design.md | internal | 完整设计解释与取舍，规则权威仍在逻辑文档 | 语义自审 |
| ../../references/handoff.md | internal | 按需交接提纲，实际运行数据不写入仓库 | references/acceptance.md |
| ../../tests/test_install.py | internal | 隔离临时目录中的安装契约验证 | unittest |

## 验证

`python -m unittest discover -s tests -v`：重复安装、保留原文、撤销、拒绝源码入口、未知文件/损坏标记、只读预览、文件冲突。
行为验收见 references/acceptance.md；没有运行时切换工具的环境只能验收 prepared-only。
