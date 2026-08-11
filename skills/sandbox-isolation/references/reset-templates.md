# Governance-derived reset templates

These are comparison templates, not permission to overwrite files. Render them only after reading `GOVERNANCE.md` and resolving the actual layout.

## Profile

```markdown
# Workspace governance

This workspace is an exploration sandbox.
- Conversations are independent by default.
- Cross-session project memory is not inferred automatically.
- Historical linkage requires an explicit user request.
- Projects that need durable state belong in a dedicated workspace.

Authority: <memory-root>/GOVERNANCE.md
```

## Rules

```markdown
# Workspace rules

- Daily logs follow the governance-defined compact format.
- Do not distill unrelated project memory into the workspace index.
- Keep project-specific knowledge in its dedicated workspace.
- Do not infer links between sessions unless the user asks.
```

## Memory index

```markdown
# Memory index

- Governance: GOVERNANCE.md
- Profile: profile.md
- Rules: <canonical rules path>
- Daily logs: <memory-root>/YYYY-MM-DD.md
```

## Raw memories marker

```markdown
<!-- Automatic memory content archived during an approved cleanup. -->
<!-- The host platform may append content again; diagnose it in a later session. -->
```

## Comparison rules

- Replace `<canonical rules path>` with the path selected from the actual layout.
- Preserve governance-specific wording when it is compatible with the safety boundary.
- Do not compare generated timestamps as substantive content.
- If governance and a template disagree, report the difference instead of silently applying the template.
