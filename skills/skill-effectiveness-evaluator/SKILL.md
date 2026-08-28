---
name: skill-effectiveness-evaluator
description: "当用户需要测试、比较、评估或优化 AI Skill，建立空白对照、进行匿名盲审或跨模型复评时使用。通过独立能力卡设计第三方视角实验，以统一的决策摘要、综合评分、任务矩阵和人工复核阅读包输出可用于决策的结论和改进建议。"
agent_created: true
---


# 技能测试台

## 目标

通过小而可审计的对照实验，判断 Skill 是否改善结果、可靠性、效率或用户成本，并识别适用边界与改进重点。默认只读评估被测 Skill。

## 实验类型

开始前选定一种类型，不同类型分别报告。

| 类型 | 用途 | 加载要求 |
|---|---|---|
| `content-effect` | 比较 Skill 内容对交付的影响 | 真实加载目标 Skill |
| `natural-trigger` | 观察触发、跳过、确认与交互成本 | 只提供原始用户输入 |
| `method-injection` | 比较注入方法文本的效果 | 明确标为方法注入，不归因于 Skill |

## 硬门禁

### 加载与输入

每个单元必须保存 `input.json`、`execution.json`、`transcript.md`、`artifact.md` 与 `status.json`。字段模板见 `references/templates.md`。

- `content-effect` 中缺少真实加载证据的候选组标记 `LIMITED`，不得用于版本胜负结论。
- 无法真实加载时，统一使用 `method-injection`，不伪装为真实 Skill 实验。
- 每题只有一个 `inputs/<task-id>.json`；所有候选仅使用其中允许的材料。
- `prompt-only` 与 `context-aware` 分别评分。出现未声明背景、历史结果、其他候选或工作区记忆时，标记 `CONTAMINATED`。

### 状态与汇总

- `VALID` 是进入主汇总的唯一状态；`LIMITED` 仅可附录呈现；`INVALID`、`CONTAMINATED` 和 `SUPERSEDED` 排除。
- 重试使用新单元 ID，并在旧单元记录替代关系。
- 汇总前生成 `unit-manifest.json`。状态冲突、重复单元、必要文件缺失或未验证加载时，停止主汇总并输出问题清单。

## 工作流

### 1. 预注册与能力卡

在 `design/experiment-design.md` 记录实验问题、版本差异、自变量、实验类型、共同输入、样本量、评分锚点、事实核验模式、无效规则与结论规则。

多版本实验建立私有 `mapping.json`，并在首轮固定 `CAND-*` 与 `blind_pack_hash`。模板见 `references/templates.md`。

在任务设计前创建 `design/capability-card.md`。能力卡从使用者视角描述可观察行为、预期收益、成本、副作用、应测情境、评价维度和非评分项。被测 Skill 的自述仅用于理解边界和形成假设，不直接作为成功标准。

### 2. 任务设计

快速实验至少覆盖一个核心任务、一个边界或压力任务，以及一个能区分版本差异的情境。每题明确用户目标、输入缺口、成功标准、不可接受结果、事实账本与预计区分能力。

输入模糊时，至少保留一题模糊需求以检验需求澄清。流程名称、框架名称、格式复杂度、篇幅和方法声明本身不得成为主要评分依据。

### 3. 隔离执行

每个单元使用新上下文、独立目录和相同输入包。

- 测过程时，在确认门槛停止并记录。
- 测最终交付时，在输入包提供相同的正式确认消息。
- transcript 保留完整对话、关键工具调用和加载证据。
- 执行结束后依据门禁更新 `status.json` 与 `unit-manifest.json`。

### 4. 盲审包与评分

首轮只创建一次 `review-pack/` 并写入包哈希：

- `final-quality/`：匿名最终交付，评任务达成、材料支持度、完整性、可用性和效率。
- `process-quality/`：中性化过程材料，评需求澄清、确认门槛、核验动作、交互轮次和留档质量。

移除版本、组别、Skill 名称、agent 身份、实验假设、运行状态和映射信息。匿名化后检查候选文件不含版本名、`ARM-*` 或单元 ID。

事实核验模式只能选一种：

- `pack-only`：只评材料支持度，外部正确性为 `N/A`。
- `source-pack`：所有盲审者使用同一来源包。
- `open-web`：记录来源、日期和 URL。

评分必须附原文证据或指出证据缺失；不因篇幅、格式或方法声明本身加分。

### 5. 跨模型复评

跨模型复评复用同一 `review-pack/`、`CAND-*` 和 `blind_pack_hash`，并使用 `task(context: "fresh")` 派遣独立盲审者。复评者只读取盲审包与评分卡，报告保存到 `scores/<model-id>/blind-review.md`。

校验候选标签、盲审包哈希和评分文件完整性后，生成共识报告。首轮盲审交付结尾提供已填入路径的复评交接卡；模板见 `references/templates.md`。缺少冻结盲审包或哈希时，明确列出复评前提。

### 6. 汇总与人工复核

`REPORT.md` 依次呈现：

1. 决策摘要：推荐版本、适用场景、证据强度和关键限制。
2. 综合评分一览：最终质量、过程质量、效率/成本、样本数和状态。
3. 任务级评分矩阵：各维度分数、总分和证据索引。
4. 关键观察、分歧、风险边界和建议动作。

最终质量与过程质量分开汇总。综合分只在实验类型、核验模式、评分维度一致且单元均为 `VALID` 时用于辅助排序；不可比样本显示 `N/A`、样本数和原因。模板见 `references/templates.md`。

为使用者创建 `reviewers/`：

```text
reviewers/
├── human-review.md
└── task-<id>-comparison.md
```

- 总入口列出任务对照页、版本状态和原始记录索引。
- 每个任务对照页横向呈现真实组别的首次回应摘要、澄清动作、最终交付摘要、轮次、状态及原始记录链接。
- 从 `reviewers/` 链接原始材料使用 `../runs/<unit-id>/...`。
- 原始对话和产物供阅读；输入、执行和状态文件供审计。

## 标准目录

```text
artifacts/skill-lab/<evaluation-id>/
├── design/
│   ├── experiment-design.md
│   └── capability-card.md
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

## 交付前检查

1. 有效单元、状态和汇总一致。
2. 实验类型、加载方式和证据边界一致。
3. 盲审包、候选标签、包哈希和复评记录一致。
4. `REPORT.md`、人工复核阅读包和复评交接卡完整。
5. 失败、污染、限制和未验证项已明确呈现。

详细模板见 `references/templates.md`。