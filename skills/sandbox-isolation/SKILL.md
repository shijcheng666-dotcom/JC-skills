---
name: sandbox-isolation
description: This skill should be used when a workspace is intended for unrelated exploration and its agent-memory files need to be diagnosed, isolated, or safely cleaned. Trigger on requests such as "check the isolation area", "diagnose workspace memory", "clean sandbox memory", "isolate sessions", or "sandbox isolation". It separates read-only diagnosis from confirmed cleanup, follows a workspace governance file, detects path/layout conflicts, validates compact daily logs, and requires backup plus explicit confirmation before writes.
agent_created: true
disable: false
---

# Sandbox Isolation

Govern memory in a workspace that intentionally contains unrelated explorations. Treat each conversation as independent unless the user explicitly requests historical linkage. Use the workspace's governance document as the source of truth; do not invent rules when it is missing.

## Modes

Select exactly one mode from the user's request:

- **Diagnose**: inspect only. Do not write, move, delete, rename, or create files.
- **Cleanup**: diagnose first, show the exact scope and proposed changes, obtain explicit confirmation, create and verify a backup, then modify only the approved allowlist.
- **Archive review**: report expired logs and project-specific extra files. Do not archive or delete them unless the user separately confirms each operation.

Never silently interpret a request to "check" as permission to clean.

## 1. Discover the governance source

1. Locate the workspace memory root. Prefer an explicitly supplied path or the workspace's configured memory directory.
2. Look for `GOVERNANCE.md` at the memory-root level.
3. Read it before interpreting any other memory file.
4. If it is missing:
   - Diagnose mode: report `governance_missing` and inspect no further than needed to establish the missing source.
   - Cleanup mode: stop. Do not create a governance file and do not apply bundled defaults.
5. Treat the governance document as authoritative for summary limits, file names, retention, and approval rules. If it conflicts with this skill, report the conflict and follow the more conservative behavior: read-only, no deletion, and explicit confirmation.

## 2. Resolve file-layout differences

Do not assume one platform layout. Detect the actual files under the memory root. Common candidates include:

- `profile.md`
- `MEMORY.md`
- `topics/project_rules.md`
- `project-rules.md`
- `raw/memories.md`
- date-named daily logs such as `YYYY-MM-DD.md`
- system state files such as `selector-state.json`

If both `topics/project_rules.md` and `project-rules.md` exist, report a `layout_conflict` with both paths. Do not overwrite either file until the user chooses the canonical path. Keep the governance file itself outside the cleanup allowlist.

## 3. Diagnose without side effects

For each discovered file, report:

- path relative to the workspace or memory root;
- category: governance, system memory, daily log, state file, or extra file;
- state: missing, clean, contaminated, malformed, expired, conflict, or unknown;
- evidence: concise line numbers or content indicators;
- proposed action: none, reset, review, archive, or confirm separately.

Check the following:

- Governance source exists and is readable.
- System files contain only governance metadata rather than unrelated project memory.
- Daily logs use a topic tag and one compact summary line.
- The summary limit comes from governance; use 20 characters/字 as the conservative default only when governance does not define one.
- Logs created before the governance effective date are historical and should be reported but not treated as current violations.
- Extra project-specific files under `memory/` or `topics/` are reported, never moved automatically.
- `selector-state.json` and similar state files are never modified by this skill.

Do not claim that the host platform will definitely rewrite files. State only that host-level memory behavior may append or overwrite them later and that this skill cannot prevent that behavior.

## 4. Cleanup safety gate

Cleanup is allowed only after all conditions pass:

1. The user explicitly requested cleanup.
2. A readable governance source exists.
3. The exact target paths are shown to the user.
4. The proposed replacement content and meaningful differences are shown or summarized.
5. The user explicitly confirms the listed scope.
6. A backup is created outside the replacement operation and verified readable.
7. Every target is within this core allowlist, unless the user separately authorizes a documented extra-file operation:
   - `profile.md`
   - the user-confirmed canonical rules file
   - `MEMORY.md`
   - `raw/memories.md`

Never modify `GOVERNANCE.md`, `selector-state.json`, or daily logs as part of core cleanup. Never delete logs by default. Never move or delete extra project files as a side effect of core cleanup.

When a target is already equivalent to the governance-derived template, report `clean` and skip the write. When a target differs, rewrite only after backup verification. After each write, re-read and validate the result; stop on the first failure.

## 5. Daily-log policy

Apply the governance-defined policy. Unless governance explicitly says otherwise:

- Require a topic tag such as `[topic]`.
- Require one compact summary line.
- Use a conservative default maximum of 20 characters/字 for the summary.
- Allow a separate output-path line only when governance permits it.
- Do not automatically distill logs into `MEMORY.md`.
- Do not automatically delete or archive logs after a retention period. Report candidates and request a separate confirmation.

## 6. Reporting

Use the report shape in `references/report-schema.md`. Always separate facts from inferences. Include a limitations section:

- Diagnosis is read-only.
- Cleanup is limited to the confirmed scope.
- Backups are required before writes.
- Host memory automation may reintroduce content later.
- This skill does not automatically trigger itself in a new session.

## 7. Publication hygiene

When packaging or publishing this skill:

- Keep all paths abstract or relative; never include a real user directory, username, account, token, cookie, research note, or private project name.
- Do not include daily logs, runtime state, cache directories, audit outputs, or unrelated workspace files.
- Keep references and scripts inside this skill directory.
- Do not claim a formal open-source license unless a formal license file exists and is verified.
- Run the publication scanner before upload.
