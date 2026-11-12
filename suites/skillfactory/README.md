# skillfactory

一套联动的 Skill 生产工具：以 `skill-orchestrator` 为唯一入口，调度 5 个参与 Skill，完成团队级 Skill 的创建、评估与演进。适用于需要把 Skill 沉淀为团队资产（可复用、可推广、迭代可证伪）的场景。

## 包内容

| 目录 | 角色 | 何时起作用 |
| --- | --- | --- |
| `skill-orchestrator` | 唯一入口（重决策总控） | 团队复用/推广级 Skill 的创建、改造、版本比较、推广判断 |
| `skill-creator` | 硬门禁：创建、结构校验、安装与打包 | 编排流程的创建环节；个人轻量 Skill 也可直接单独使用 |
| `skill-effectiveness-evaluator` | 硬门禁：有效性评估与证据归档 | 候选验证、版本比较、推广判断 |
| `writing-for-agents` | 条件调度专项：候选结构审查 | 候选涉及触发描述、分支结构、引用关系或完成条件风险时 |
| `skill-from-externals` | 条件调度专项：外部学习 | 分支 A 现成 Skill 复用；分支 B 项目机制学习 |
| `skill-from-masters` | 条件调度专项：实践标杆深挖 | 质量依赖人类判断/沟通/创作，真实成败模式会改变规则时 |

## 安装

**建议为 skillfactory 新建一个独立工作区，并将全部六个技能仅安装在该工作区，不要全局安装。** 原因：

- 本套件是自洽的 Skill 生产环境：六个技能会参与该环境内所有"创建/改造 Skill"类请求的路由，装入全局或已有工作区会改变那些环境的触发行为，个人轻量任务也可能被误引导进编排流程。
- 独立工作区让生产过程的中间产物（任务卡、候选、评估证据）与日常业务文件自然隔离，触发行为可预期，也便于按项目做版本管理。

步骤：

1. 新建一个空文件夹作为工作区（例如 `skillfactory-workspace`），在其中创建技能目录（如 `skills/`）。
2. 将本包六个技能目录解压到该技能目录下，最终结构为 `skillfactory-workspace/skills/skill-orchestrator/` 等。
3. 在该工作区中让 AI 运行以下命令验证安装（路径替换为实际技能目录）：

```bash
python skills/skill-orchestrator/scripts/check_capability_baseline.py skills
```

全部显示"调度接口已定义"且结论为"核心硬门禁齐备"即安装成功。如果 AI 所在平台有自己的技能目录约定（如 `.trae/skills/`、`.aime/skills/`），按平台约定放置并相应调整验证命令路径；平台目录不可写时，工作区根下的 `skills/` 目录同样可用。

## 使用

- **团队级 Skill**（要复用、要推广）：直接描述需求，例如"做一个部门通用的 XX Skill，几个团队都要用"，由 orchestrator 接管完整流程。
- **个人轻量 Skill**：直接说"做个 XX Skill 我自己用"，由 `skill-creator` 完成创建与轻量验证，不经过 orchestrator。
- 参与 Skill 不会主动响应业务任务，只接受 orchestrator 按环节调度；缺少某个参与 Skill 时，orchestrator 会按降级规则说明影响并继续。
- 迭代按可独立验收与回滚的变更集推进。Git 仅作为可选的版本协同能力，不可用时降级为源目录外快照与指纹记录；是否提交、发布与推广始终由作者决定。

## 环境说明

`skill-creator` 支持两种模式：Aime 环境使用 `create_skill` 工具完成正式安装；无该工具的环境自动降级为直接创建文件并如实声明加载状态未验证。评估环节的独立子代理执行依赖平台能力，不可用时按 `skill-effectiveness-evaluator` 的状态缺口规则降级。
