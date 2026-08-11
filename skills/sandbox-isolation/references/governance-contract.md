# Governance contract

`GOVERNANCE.md` is the source of truth for a workspace's memory policy. It is not a license to modify files.

## Required fields to look for

- workspace purpose and isolation intent;
- effective date, if present;
- memory root and canonical file layout;
- daily-summary format and maximum length;
- retention and archive policy;
- files that must never be changed;
- confirmation and backup requirements.

## Missing or ambiguous governance

- Missing governance: diagnosis reports the gap; cleanup stops.
- Multiple governance files: report all candidates and ask which one is authoritative.
- Conflicting rules: follow the more conservative behavior and report the conflict.
- A proposed migration is not proof that the migration has already happened. Separate current rules from historical plans.

## Capability boundary

A governance document cannot necessarily disable a host platform's automatic memory extraction or distillation. Describe that rule as a desired workspace policy and use this skill to detect and repair drift after approval.
