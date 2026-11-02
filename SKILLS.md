# Skill index

Find and share an individual skill or suite from [JC-skills](https://github.com/shijcheng666-dotcom/JC-skills).

## Skills

| Slug | Name | Version | Directory | Main file | Raw `SKILL.md` |
|---|---|---|---|---|---|
| `rigor-mode` | 严谨模式 2.0 / Rigor Mode 2.0 | 2.2.0 | [Browse](skills/rigor-mode/) | [Open](skills/rigor-mode/SKILL.md) | [Raw](https://raw.githubusercontent.com/shijcheng666-dotcom/JC-skills/main/skills/rigor-mode/SKILL.md) |
| `skill-effectiveness-evaluator` | 技能测试台 / Skill Effectiveness Evaluator | 0903V2 | [Browse](skills/skill-effectiveness-evaluator/) | [Open](skills/skill-effectiveness-evaluator/SKILL.md) | [Raw](https://raw.githubusercontent.com/shijcheng666-dotcom/JC-skills/main/skills/skill-effectiveness-evaluator/SKILL.md) |
| `user-interview-transcript-calibrator` | 用户笔录校准 / User Interview Transcript Calibrator | 2.5.2 | [Browse](skills/user-interview-transcript-calibrator/) | [Open](skills/user-interview-transcript-calibrator/SKILL.md) | [Raw](https://raw.githubusercontent.com/shijcheng666-dotcom/JC-skills/main/skills/user-interview-transcript-calibrator/SKILL.md) |
| `desktop-savior` | 桌面救星 / Desktop Savior | - | [Browse](skills/desktop-savior/) | [Open](skills/desktop-savior/SKILL.md) | [Raw](https://raw.githubusercontent.com/shijcheng666-dotcom/JC-skills/main/skills/desktop-savior/SKILL.md) |
| `windows-pc-care` | Windows 轻净计划 / Windows PC Care | - | [Browse](skills/windows-pc-care/) | [Open](skills/windows-pc-care/SKILL.md) | [Raw](https://raw.githubusercontent.com/shijcheng666-dotcom/JC-skills/main/skills/windows-pc-care/SKILL.md) |
| `local-agent-memory-governor` | 本地 Agent 记忆管家 / Local Agent Memory Governor | - | [Browse](skills/local-agent-memory-governor/) | [Open](skills/local-agent-memory-governor/SKILL.md) | [Raw](https://raw.githubusercontent.com/shijcheng666-dotcom/JC-skills/main/skills/local-agent-memory-governor/SKILL.md) |
| `sandbox-isolation` | 探索隔离区 / Sandbox Isolation | - | [Browse](skills/sandbox-isolation/) | [Open](skills/sandbox-isolation/SKILL.md) | [Raw](https://raw.githubusercontent.com/shijcheng666-dotcom/JC-skills/main/skills/sandbox-isolation/SKILL.md) |

Rigor Mode's `SKILL.md` frontmatter name is `rigor-mode-v2`. The directory keeps the older name `rigor-mode` so existing links keep working.

## Suites

| Slug | Members | Directory | Guide |
|---|---|---|---|
| `skillfactory` | `skill-orchestrator` (entry), `skill-creator`, `skill-effectiveness-evaluator`, `writing-for-agents`, `skill-from-externals`, `skill-from-masters` | [Browse](suites/skillfactory/) | [README](suites/skillfactory/README.md) |

### Version note: two copies of the evaluator

| Location | Version | Role |
|---|---|---|
| `skills/skill-effectiveness-evaluator/` | 0903V2 | Standalone use |
| `suites/skillfactory/skill-effectiveness-evaluator/` | 0903V3 | Pinned member of skillfactory, adds the orchestrator dispatch interface |

They are intentionally not merged. Use the suite copy inside skillfactory and the standalone copy elsewhere. Whether to promote V3 to the standalone directory is a maintainer decision.

## Direct sharing links

- [Rigor Mode](https://github.com/shijcheng666-dotcom/JC-skills/tree/main/skills/rigor-mode)
- [Skill Effectiveness Evaluator](https://github.com/shijcheng666-dotcom/JC-skills/tree/main/skills/skill-effectiveness-evaluator)
- [User Interview Transcript Calibrator](https://github.com/shijcheng666-dotcom/JC-skills/tree/main/skills/user-interview-transcript-calibrator)
- [Desktop Savior](https://github.com/shijcheng666-dotcom/JC-skills/tree/main/skills/desktop-savior)
- [Windows PC Care](https://github.com/shijcheng666-dotcom/JC-skills/tree/main/skills/windows-pc-care)
- [Local Agent Memory Governor](https://github.com/shijcheng666-dotcom/JC-skills/tree/main/skills/local-agent-memory-governor)
- [Sandbox Isolation](https://github.com/shijcheng666-dotcom/JC-skills/tree/main/skills/sandbox-isolation)
- [skillfactory suite](https://github.com/shijcheng666-dotcom/JC-skills/tree/main/suites/skillfactory)

## Adding a skill or suite

Add a single skill under `skills/<lowercase-kebab-case-slug>/`, or a multi-skill workflow under `suites/<slug>/`. Then update this index, the root [README.md](README.md), [LICENSES/](LICENSES/), and [CHANGELOG.md](CHANGELOG.md). See [CONTRIBUTING.md](CONTRIBUTING.md).
