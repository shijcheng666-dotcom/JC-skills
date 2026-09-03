# 严格审计

## 适用范围

仅用于版本归档、重要决策、高风险场景或用户明确要求严格审计。严格性来自可验证证据，不来自更多文档。

## 任务设计

正式任务按 `references/task-design-principles.md` 设计：先阅读 Skill 的完整内容、架构、引用资源、工具依赖和失败路径，识别真实目标，再设计围绕目标的核心任务，并根据薄弱点、易错点和版本差异设计压力或边界任务。任务设计只需达到与审计风险相称的程度，不要求每次建立复杂任务工程。

## 冻结与证据

正式执行前冻结并记录 SHA-256：

- `design/experiment-design.md`
- `design/capability-card.md`
- `design/difference-table.md`
- `design/tasks/`
- `inputs/`
- `SCORING.md`

执行开始后若改变候选定义、关键自变量、输入、任务卡或评分卡，必须新建 `evaluation-id`，或记录替代关系并将旧单元标为 `SUPERSEDED`。不得静默覆盖旧材料。

每个运行单元必须包含：

```text
runs/<unit-id>/
├── input.json
├── execution.json
├── transcript.md
├── artifact.md
└── status.json
```

`execution.json` 的自报字段不是验证证据。`status.json` 只能由协调者或验证脚本根据日志、文件或哈希判定。运行单元完成后使用 `scripts/verify_run_units.py <runs-or-unit>`；它会校验 task 调用标识、`fresh` 上下文、输入指纹、完整 transcript/artifact、结构化返回、隔离证据和 `VALID` 前置条件。验证失败时不得进入主汇总。

执行子代理和盲审子代理必须返回结构化结果，至少包含 `status`、`verification`、`concerns`、`next_steps`、产物路径和约束检查。缺少 fresh 子代理证据、结构化结果、完整 transcript 或关键加载证据时，不得标记 `VALID`。

## 输入、隔离与状态判定

按 `references/execution-protocol.md` 执行任务和盲审的角色隔离、输入边界、重试与证据留存。读取私有标准、其他候选或未声明背景时标记 `CONTAMINATED`；材料缺失、哈希不一致或执行失败时标记 `INVALID`；加载、隔离或输入一致性无法独立验证时至少标记 `LIMITED`。

## 盲审

按 `references/execution-protocol.md` 派发首轮盲审和跨模型复评。严格双候选盲审包结构：

```text
review-pack/
├── final-quality/
├── process-quality/
├── SCORING.md
├── anonymization-report.json
└── pack-manifest.json
```

使用 `scripts/prepare_review_pack.py` 创建，并使用 `scripts/verify_review_pack.py` 校验。盲审者只读取冻结的盲审包和评分卡，不得读取报告、分数、映射、运行材料、输入或工作区记忆。

盲审者先阅读同一任务的所有候选，再评分；每项评分必须给原文证据或指出证据缺失。最终质量与过程质量分开汇总。

## 跨模型复评

跨模型复评前必须记录首轮准确模型 ID，且能选择和核验不同的模型 ID。条件不满足时停止，只生成交接卡。复评者复用同一冻结盲审包、候选标签和哈希，单独保存评分结果；不得提前读取首轮结论。

## 完整目录与交付

```text
artifacts/skill-lab/<evaluation-id>/
├── design/
├── inputs/
├── runs/
├── unit-manifest.json
├── mapping.json
├── review-pack/
├── scores/
├── reviewers/
├── issues.md
└── REPORT.md
```

只有预注册要求、有效单元、证据门禁和核验要求均满足时，才可使用 `decision-ready`。否则降级为 `directional` 或 `exploratory`，并在结论附近说明原因。
