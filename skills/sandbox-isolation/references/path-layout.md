# Path and layout contract

Use paths relative to the selected workspace memory root. Do not hard-code a vendor, operating system, user directory, or drive letter.

## Canonical conceptual layout

```text
<memory-root>/
├── GOVERNANCE.md
├── profile.md
├── MEMORY.md
├── topics/project_rules.md
├── raw/memories.md
├── YYYY-MM-DD.md
└── selector-state.json
```

## Accepted variations

Some hosts use `project-rules.md` instead of `topics/project_rules.md`, or omit one of the system files. Detect the actual layout. If both rules-file variants exist, report a layout conflict and do not choose one silently.

## Path rules

- Display relative paths in reports.
- Resolve symlinks before any proposed write.
- Reject targets outside the selected memory root.
- Keep `GOVERNANCE.md`, daily logs, and system state files outside the core cleanup allowlist.
- Treat extra files as report-only unless separately authorized.
