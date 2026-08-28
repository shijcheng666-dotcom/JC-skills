# 模板

## execution.json

```json
{
  "unit_id": "u01",
  "load_mode": "real-load | method-injection | control",
  "skill_name": "...",
  "skill_tool_success": true,
  "skill_fingerprint": "sha256:...",
  "reference_fingerprints": {"references/file.md": "sha256:..."},
  "input_fingerprint": "sha256:...",
  "model": "..."
}
```

## status.json

```json
{
  "unit_id": "u01",
  "status": "VALID | LIMITED | INVALID | CONTAMINATED | SUPERSEDED",
  "reasons": [],
  "superseded_by": null,
  "constraint_checks": {
    "input_match": true,
    "artifact_complete": true,
    "load_verified": true,
    "isolation_verified": true
  }
}
```

## 能力卡

```markdown
# 能力卡

- 使用者问题：为什么需要这个 Skill
- 可观察行为：Skill 应改变的输入处理、判断或交付行为
- 预期收益：对质量、可靠性、效率或返工的可观察改善
- 成本与副作用：轮次、篇幅、工具成本、等待、模板化或错误风险
- 应测情境：核心、边界、压力和版本差异情境
- 评价维度：4-6 个直接反映使用者收益的指标
- 非评分项：流程名称、框架名称、格式复杂度、篇幅或方法声明本身
```

## 映射文件

```json
{
  "arms": [{"arm_id": "ARM-01", "version": "...", "candidate": "CAND-A"}],
  "blind_pack_hash": "sha256:..."
}
```

## 综合评分一览

```markdown
## 综合评分一览

| 版本 | 最终质量 | 过程质量 | 效率/成本 | 有效单元 | 状态 |
|---|---:|---:|---:|---:|---|
| 版本 A | 4.2/5 | 4.5/5 | 4.0/5 | 3/3 | VALID |

## 任务级评分矩阵

| 任务 | 版本 | 任务达成 | 材料支持度 | 完整性 | 可用性 | 效率 | 总分 | 证据 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 任务 1 | 版本 A | 5 | 4 | 4 | 5 | 4 | 22/25 | §3.1 |
```

## 人工复核对照页

```markdown
| 版本 | 首次回应摘要 | 澄清动作 | 最终交付摘要 | 轮次 | 状态 | 原始记录 |
|---|---|---|---|---:|---|---|
| 版本 A | … | … | … | 2 | VALID | [对话](../runs/u01/transcript.md) / [产物](../runs/u01/artifact.md) |
```

## 跨模型复评交接卡

```text
请使用 skill-effectiveness-evaluator 对本次实验进行独立盲审复评。

仅读取盲审包：<review-pack 绝对路径>
不要读取首轮报告、分数、issues.md、mapping.json、reviewers/ 或工作区记忆。

请作为协调者，使用 task(context: "fresh") 派遣独立盲审者：
1. 只读取上述盲审包及其中评分卡；
2. 复用现有 CAND 标签和盲审包，不重新匿名化；
3. 分别评审 final-quality 与 process-quality；
4. 将完整报告保存至 <scores/<模型ID>/blind-review.md>；
5. 校验候选标签、blind_pack_hash 和评分文件完整性后，生成共识报告。

返回独立盲审结果、与首轮的一致观察、分歧和证据强度。
```
