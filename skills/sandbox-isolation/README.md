# Sandbox Isolation

A safety-first skill for diagnosing and governing memory stores in workspaces used for unrelated exploration.

## What it does

- Uses `GOVERNANCE.md` as the workspace-specific source of truth.
- Separates read-only diagnosis from confirmed cleanup.
- Detects missing governance, contaminated system memory, daily-log violations, extra project files, and layout conflicts.
- Requires an explicit scope confirmation and a verified backup before modifying core memory files.
- Keeps daily logs and system state files out of default cleanup.
- Cannot prevent a host platform from appending or overwriting memory later; it detects and repairs that drift after approval.

## Trigger examples

- "检查这个探索隔离区"
- "诊断 workspace memory"
- "清理沙盒记忆"
- "隔离不同会话"
- "sandbox isolation"

## Package layout

```text
sandbox-isolation/
├── SKILL.md
├── README.md
├── references/
│   ├── governance-contract.md
│   ├── log-policy.md
│   ├── path-layout.md
│   ├── privacy-and-publication.md
│   ├── report-schema.md
│   └── reset-templates.md
├── scripts/
│   ├── audit_memory.py
│   ├── lint_daily_logs.py
│   └── scan_publication.py
└── tests/
    ├── fixtures/
    └── test_scripts.py
```

## Safety boundary

Diagnosis is read-only. Cleanup is not implied by a check request. Cleanup may touch only the explicitly confirmed core files after a verified backup. The governance document, daily logs, system state files, extra project files, credentials, and private workspace data are excluded by default.

## Local validation

Run from this skill directory:

```text
python scripts/audit_memory.py tests/fixtures/dirty/memory
python scripts/lint_daily_logs.py tests/fixtures/dirty/memory --governance-date 2026-07-28
python scripts/scan_publication.py .
python -m unittest discover -s tests -p "test_*.py"
```

The scripts are read-only. They emit JSON by default and do not create backups or modify input files.

## License status

Author-authored; no formal open-source license added automatically. This status does not grant a broader license than the repository maintainer has explicitly documented.
