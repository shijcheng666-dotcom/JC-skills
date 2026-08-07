# Windows Light & Clean Plan

**A safety-first PC cleanup & optimization skill for Windows 10/11**

[中文说明](./README.md)

---

## What This Is

A **safety-first** workflow for diagnosing, cleaning, and optimizing sluggish Windows PCs. Unlike typical "one-click booster" tools, this project follows strict safety boundaries:

- **Diagnose first, plan second, execute third, verify last.**
- **Personal files are read-only** — never touch your Desktop, Downloads, or Documents automatically.
- **Explicit approval for every change** — no silent modifications.
- **Don't sacrifice security** — never disable Defender, Windows Update, or uninstall Edge/OneDrive by default.
- **Rollback-friendly** — every change is logged with its original state.

## Project Structure

```
windows-pc-care/
├── SKILL.md                         # AI Skill entry point
├── README.md                        # This file (Chinese)
├── README.en.md                     # English version
├── scripts/
│   ├── collect-diagnostics.ps1      # Read-only system baseline → JSON
│   └── safe-cache-cleanup.ps1       # Safe cache cleanup (preview by default)
└── references/
    └── safety-and-decision-matrix.md # Risk tiers, rollback rules, report template
```

## Quick Start

```powershell
# 1. Collect baseline (read-only, no modifications)
powershell -NoProfile -File scripts\\collect-diagnostics.ps1

# 2. Preview cleanable temp files (read-only)
powershell -NoProfile -File scripts\\safe-cache-cleanup.ps1

# 3. Clean confirmed caches (requires -Apply)
powershell -NoProfile -File scripts\\safe-cache-cleanup.ps1 -Targets UserTemp,WindowsTemp -Apply
```

> ⚠️ All scripts are **harmless by default**: diagnostics are read-only; cleanup scripts only preview unless `-Apply` is explicitly added.

## Safety Principles

| Principle | Description |
|---|---|
| Read-only diagnostics | No config changes, no file deletion, no personal file reads |
| Opt-in cleanup | Preview only by default; `-Apply` required for execution |
| System files untouched | Prefetch, WinSxS, System32, pagefile are never touched |
| Item-by-item approval | Uninstalls, startup changes, settings all require your explicit OK |
| Personal data protected | Desktop/Downloads/Documents are size-audited only |
| Rollback-friendly | Original state recorded; system restore points recommended before changes |

## License

MIT

## JC-skills

This skill is maintained in the unified [JC-skills](https://github.com/shijcheng666-dotcom/JC-skills) collection. Browse the complete package at [skills/windows-pc-care](../../skills/windows-pc-care/).
