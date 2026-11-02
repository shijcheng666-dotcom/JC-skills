# JC-skills

A curated collection of practical AI skills and skill suites by Jay Chen.

Each skill lives in its own directory, so you can browse, copy, install, and share one skill without downloading the whole collection. Multi-skill workflows are kept together as **suites**.

## Skills

| Skill | Version | Purpose | Entry point | License status |
|---|---|---|---|---|
| [严谨模式 2.0 / Rigor Mode 2.0](skills/rigor-mode/) | 2.2.0 | A structured workflow for reliable, verifiable, and revisable AI outputs. | [SKILL.md](skills/rigor-mode/SKILL.md) | Author-authorized; no formal license file |
| [技能测试台 / Skill Effectiveness Evaluator](skills/skill-effectiveness-evaluator/) | 0903V2 | Auditable experiments for testing and comparing AI skills. | [SKILL.md](skills/skill-effectiveness-evaluator/SKILL.md) | Author-authored; no formal license |
| [用户笔录校准 / User Interview Transcript Calibrator](skills/user-interview-transcript-calibrator/) | 2.5.2 | Turn interview transcripts into archive-ready user records. | [SKILL.md](skills/user-interview-transcript-calibrator/SKILL.md) | Author-authored; no formal license |
| [桌面救星 / Desktop Savior](skills/desktop-savior/) | - | A cautious, reversible organizer for mixed personal and work files. | [SKILL.md](skills/desktop-savior/SKILL.md) | MIT declared in source README |
| [Windows 轻净计划 / Windows PC Care](skills/windows-pc-care/) | - | A safety-first workflow for diagnosing and improving Windows 10/11 PCs. | [SKILL.md](skills/windows-pc-care/SKILL.md) | MIT declared in source README |
| [本地 Agent 记忆管家 / Local Agent Memory Governor](skills/local-agent-memory-governor/) | - | Audit, backup, and rollback workflow for local agent memory stores. | [SKILL.md](skills/local-agent-memory-governor/SKILL.md) | Author-authored; no formal license |
| [探索隔离区 / Sandbox Isolation](skills/sandbox-isolation/) | - | Diagnose and govern memory stores in workspaces used for unrelated exploration. | [SKILL.md](skills/sandbox-isolation/SKILL.md) | Author-authored; no formal license |

## Suites

A suite is a set of skills designed to work together. Install the whole suite, not individual members.

| Suite | Contents | Purpose | Entry point |
|---|---|---|---|
| [skillfactory](suites/skillfactory/) | 6 skills | Create, evaluate, and evolve team-level skills through one orchestrated flow. | [README.md](suites/skillfactory/README.md) |

See [SKILLS.md](SKILLS.md) for the full index with direct and raw links, and [CHANGELOG.md](CHANGELOG.md) for version history.

## Skills versus suites

- `skills/<slug>/`: one self-contained skill. Safe to copy on its own.
- `suites/<slug>/`: several skills with declared dependencies on each other. Copy the whole suite directory and follow its README.
- The same skill name may appear in both places. Copies inside a suite are the suite's pinned members and may be a different version from the standalone copy. Versions are recorded in [SKILLS.md](SKILLS.md).

## Repository structure

```text
JC-skills/
├─ README.md
├─ SKILLS.md
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ LICENSES/
├─ skills/
│  ├─ rigor-mode/
│  ├─ skill-effectiveness-evaluator/
│  ├─ user-interview-transcript-calibrator/
│  ├─ desktop-savior/
│  ├─ windows-pc-care/
│  ├─ local-agent-memory-governor/
│  └─ sandbox-isolation/
└─ suites/
   └─ skillfactory/
```

## Source repositories

Some skills were consolidated from earlier public repositories, which remain available as historical entry points:

- [rigor-mode](https://github.com/shijcheng666-dotcom/rigor-mode)
- [desktop-savior](https://github.com/shijcheng666-dotcom/desktop-savior)
- [windows-pc-care](https://github.com/shijcheng666-dotcom/windows-pc-care)

For `rigor-mode`, the published release is on SkillsHub (`sug-ur-skills/rigor-mode-v2`); this repository follows it.

## License and attribution

License status is recorded per skill and suite in [LICENSES/](LICENSES/). A public repository is not a grant of broader rights than the source declares. Read [CONTRIBUTING.md](CONTRIBUTING.md) before adding or redistributing anything.
