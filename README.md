# JC-skills

A curated collection of practical AI skills by Jay Chen.

JC-skills keeps each skill self-contained in its own directory, so you can browse, copy, install, and share one skill without downloading the entire collection.

## Skill directory

| Skill | Purpose | Platform | Entry point | License status |
|---|---|---|---|---|
| [严谨模式 2.0 / Rigor Mode 2.0](skills/rigor-mode/) | A structured workflow for reliable, verifiable, and revisable AI outputs. | Any AI assistant | [SKILL.md](skills/rigor-mode/SKILL.md) | Author-authorized; no formal license file in source |
| [技能测试台 / Skill Effectiveness Evaluator](skills/skill-effectiveness-evaluator/) | Auditable experiments for testing and comparing AI skills. | Any AI assistant | [SKILL.md](skills/skill-effectiveness-evaluator/SKILL.md) | Author-authored; no formal open-source license added automatically. |`r`n| [桌面救星 / Desktop Savior](skills/desktop-savior/) | A cautious, reversible organizer for mixed personal and work files. | Personal/work folders | [SKILL.md](skills/desktop-savior/SKILL.md) | MIT declared in source README |
| [Windows 轻净计划 / Windows PC Care](skills/windows-pc-care/) | A safety-first workflow for diagnosing and improving Windows 10/11 PCs. | Windows 10/11 | [SKILL.md](skills/windows-pc-care/SKILL.md) | MIT declared in source README |
| [本地 Agent 记忆管家 / Local Agent Memory Governor](skills/local-agent-memory-governor/) | A generic audit, backup, and rollback workflow for local agent memory stores. | Any local AI agent | [SKILL.md](skills/local-agent-memory-governor/SKILL.md) | Author-authored; no formal open-source license added automatically. |
| [探索隔离区 / Sandbox Isolation](skills/sandbox-isolation/) | Diagnose and safely govern memory stores in workspaces used for unrelated exploration. | Any AI assistant | [SKILL.md](skills/sandbox-isolation/SKILL.md) | Author-authored; no formal open-source license added automatically. |

See [SKILLS.md](SKILLS.md) for direct page and raw-file links.

## Share one skill

Share the directory when the recipient needs the complete skill package:

- [Rigor Mode](skills/rigor-mode/)
- [Desktop Savior](skills/desktop-savior/)
- [Windows PC Care](skills/windows-pc-care/)
- [Local Agent Memory Governor](skills/local-agent-memory-governor/)
- [Sandbox Isolation](skills/sandbox-isolation/)

Share the `SKILL.md` page when only the main instruction file is needed. Raw links are also listed in [SKILLS.md](SKILLS.md).

## Repository structure

```text
JC-skills/
├─ README.md
├─ SKILLS.md
├─ CONTRIBUTING.md
├─ LICENSES/
└─ skills/
   ├─ rigor-mode/
   ├─ desktop-savior/
   ├─ windows-pc-care/
   ├─ local-agent-memory-governor/
   └─ sandbox-isolation/
```

Each skill directory is independent. References and scripts stay inside the skill that uses them. New skills should be added as a new `skills/<skill-slug>` directory.

## Source repositories

This collection consolidates the following public repositories without deleting them:

- [rigor-mode](https://github.com/shijcheng666-dotcom/rigor-mode)
- [desktop-savior](https://github.com/shijcheng666-dotcom/desktop-savior)
- [windows-pc-care](https://github.com/shijcheng666-dotcom/windows-pc-care)

The original repositories remain available as historical and compatibility entry points.

## License and attribution

License status is recorded per skill in [LICENSES/](LICENSES/). Do not assume that the presence of this collection grants a broader license than the source skill declares. See [CONTRIBUTING.md](CONTRIBUTING.md) before adding or redistributing a skill.
