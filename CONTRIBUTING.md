# Contributing to JC-skills

## Add a new skill

1. Create `skills/<lowercase-kebab-case-slug>/`.
2. Put the required `SKILL.md` at the skill directory root.
3. Keep references, scripts, templates, and examples inside that skill directory.
4. Add a focused `README.md` describing purpose, trigger/use cases, structure, safety boundaries, and license status.
5. Update `README.md` and `SKILLS.md` with the new skill and direct links.
6. Include clear author and license information. Do not copy content whose redistribution rights are unclear.

## Directory rules

- Use lowercase kebab-case for skill directory names.
- Keep each skill self-contained.
- Use relative links inside a skill directory.
- Do not create undeclared cross-skill dependencies.
- Keep scripts and references next to the `SKILL.md` that uses them.

## Safety and quality checks

Before publishing a change:

- Check that every skill has a root `SKILL.md`.
- Check Markdown links and examples after moving a skill.
- Scan for tokens, passwords, private URLs, personal data, and temporary files.
- Do not silently change the behavior of safety-sensitive scripts.
- Record meaningful behavior or compatibility changes in the relevant README.

## Pull requests

Explain which skill changed, why it changed, whether behavior changed, and how you checked the result. Keep unrelated skill changes in separate commits where practical.
