# 模板

## 能力卡

```markdown
# 能力卡

- 用户决策：要选择、诊断或验证什么
- 典型使用者与任务：谁在什么场景中使用
- 可观察收益：2-4 项应改善的结果、可靠性、效率或用户成本
- 风险与副作用：可能增加的轮次、篇幅、工具成本、等待、模板化或错误
- 应测情境：核心、边界/压力和版本差异情境
- 最终质量维度：任务达成、材料支持度、完整性、可用性/返工、效率
- 过程行为维度：触发、澄清、确认、核验、轮次和留档
- 非评分项：流程名称、框架名称、格式复杂度、篇幅和方法声明本身
```

## 差异表

```markdown
| 候选 | 可定位差异 | 可能影响 | 需验证任务 | 已知限制 |
|---|---|---|---|---|
| 版本 A | ... | ... | T3 | ... |
```

## 执行输入 `input.json`

```json
{
  "task_id": "T1",
  "role": "...",
  "user_input": "...",
  "allowed_background": {},
  "formal_confirmation": "..."
}
```

只包含执行者实际可见的内容。不得包含预期判断、成功标准、事实账本、评分卡、其他候选或私有任务卡。

## 执行记录 `execution.json`

```json
{
  "unit_id": "u01",
  "subagent_task_id": "task-id-or-runtime-reference",
  "subagent_context": "fresh",
  "load_mode": "real-load | method-injection | content-observation | control",
  "skill_name": "... | null",
  "skill_tool_success": true,
  "skill_fingerprint": "sha256:... | null",
  "reference_fingerprints": {},
  "injection_fingerprint": "sha256:... | null",
  "execution_input_fingerprint": "sha256:...",
  "executor_model_id": "exact runtime model id or unknown",
  "evidence_refs": {
    "load": ["transcript.md#..."],
    "input": ["input.json"],
    "isolation": []
  },
  "self_reported_fields": [],
  "structured_result": {
    "status": "DONE | DONE_WITH_CONCERNS | BLOCKED",
    "verification": [],
    "concerns": [],
    "next_steps": [],
    "artifact_paths": [],
    "constraint_checks": {}
  }
}
```

`method-injection` 和 `content-observation` 不能用于真实 Skill 加载归因。`evidence_refs` 只能引用可定位日志或文件；无法独立验证的内容列入 `self_reported_fields`。

## 严格状态 `status.json`

```json
{
  "unit_id": "u01",
  "status": "VALID | LIMITED | INVALID | CONTAMINATED | SUPERSEDED",
  "reasons": [],
  "superseded_by": null,
  "supersedes": null,
  "audited_by": "coordinator | verifier",
  "evidence": ["execution.json", "input.json", "transcript.md", "artifact.md"],
  "constraint_checks": {
    "subagent_task_verified": "verified | self-reported | unknown",
    "fresh_context_verified": "verified | self-reported | unknown",
    "execution_input_match": true,
    "private_task_card_hidden": "verified | self-reported | unknown",
    "artifact_complete": true,
    "load_or_injection_verified": true,
    "isolation_verified": "verified | self-reported | unknown"
  }
}
```

`VALID` 需要所有必要条件具有可定位证据；`self-reported` 或 `unknown` 不能替代 `verified`。快速探索不强制生成此文件。

## 评分矩阵

```markdown
| 任务 | 候选 | 任务达成 | 材料支持度 | 完整性 | 可用性 | 效率 | 过程观察 | 证据 |
|---|---|---:|---:|---:|---:|---:|---|---|
| T1 | 版本 A | 5 | 4 | 4 | 5 | 4 | 一次澄清 | 原文引用 |
```

最终质量和过程观察分开呈现。没有一致实验类型、核验模式、评分维度和有效状态时，不计算综合排序分。

## 人工复核页

```markdown
| 版本 | 首次回应摘要 | 澄清/确认动作 | 最终交付摘要 | 轮次 | 状态或限制 | 原始记录 |
|---|---|---|---|---:|---|---|
| 版本 A | ... | ... | ... | 2 | VALID | [对话](../runs/u01/transcript.md) / [产物](../runs/u01/artifact.md) |
```

人工查看总入口建议同时列出：

```text
reviewers/
├── human-review.md
├── execution-index.md
├── blind-review-index.md
└── task-<task-id>-comparison.md
```

`execution-index.md` 链接所有执行子代理的 transcript、artifact、execution 和 status；`blind-review-index.md` 链接所有盲审子代理的完整评分记录、盲审包哈希和模型 ID。它们不得进入匿名盲审包。

## 跨模型复评交接卡

```text
请使用 skill-effectiveness-evaluator 对本次实验进行跨模型复评。

首轮模型 ID：<first-model-id>
仅读取冻结盲审包：<review-pack absolute path>
盲审包哈希：<blind-pack-hash>
评分卡哈希：<scoring-sha256>

不要读取首轮报告、分数、issues.md、mapping.json、reviewers/、runs/、inputs/ 或工作区记忆。
必须使用并记录一个与首轮不同的准确模型 ID。只读取盲审包及评分卡，复用候选标签，分别评审最终质量和过程质量，每项附原文证据，并保存到 `scores/<reviewer-id>/blind-review.md`。

如果无法选择或核验不同模型，停止复评，不创建同模型复评分数，并说明该前提未满足。
```
