# 技能测试台（Skill Effectiveness Evaluator）

**版本：0903V2**（独立版）

通过可审计的对照实验，评估一个 AI Skill 到底有没有用、不同版本哪个更好、存在哪些问题，并给出有证据支撑的结论与改进建议。

## 使用

- 触发：想知道某个 Skill 的效果、要比较多个版本，或准备把 Skill 分享给团队时。
- 三个层级：快速探索（只能得出 `exploratory` 结论）、标准比较（可形成 `directional` 推荐）、严格审计（满足全部条件才可为 `decision-ready`）。
- 建议在开始任务前给予完全访问权限，便于隔离运行与留存证据。

## 文件结构

```text
skill-effectiveness-evaluator/
├── SKILL.md
├── references/     # 执行协议、三个层级说明、任务设计原则、模板
└── scripts/        # 评审包生成与校验脚本（Python）
```

## 与 skillfactory 中副本的关系

`suites/skillfactory/skill-effectiveness-evaluator/` 是版本 0903V3，增加了供 `skill-orchestrator` 调度的接口，并限定标准比较与严格审计只在编排流程中执行。两份刻意并存、未合并：单独使用选本目录，使用 skillfactory 套件时用套件内副本。差异见根目录 [SKILLS.md](../../SKILLS.md)。

许可状态见 [LICENSES/](../../LICENSES/)。
