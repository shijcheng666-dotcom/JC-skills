# Contributing to JC-skills

## Add a new skill

1. Create `skills/<lowercase-kebab-case-slug>/`.
2. Put the required `SKILL.md` at the directory root.
3. Keep references, scripts, templates, and examples inside that directory.
4. Add a focused `README.md`: purpose, trigger, structure, safety boundaries, version, license status.
5. Update `README.md`, `SKILLS.md`, `LICENSES/`, and `CHANGELOG.md`.
6. Include clear author and license information. Do not copy content whose redistribution rights are unclear.

## Add a suite

A suite is a set of skills that depend on each other.

1. Create `suites/<slug>/` with a `README.md` covering contents, install steps, usage, and environment notes.
2. Put each member in its own subdirectory with its own `SKILL.md`.
3. Declare member roles and the entry skill in the suite README.
4. Record the pinned version of each member. If a member also exists under `skills/`, note any version difference in `SKILLS.md`. Do not silently overwrite either copy.
5. Preserve any license file shipped inside a member (for example `LICENSE.txt`) and record it in `LICENSES/`.

## Directory rules

- Lowercase kebab-case for directory names.
- A skill under `skills/` stays self-contained; no undeclared cross-skill dependencies.
- Cross-skill dependencies are allowed only inside a suite, and must be declared in its README.
- Use relative links inside a directory.

## Versioning

- The version of record for a skill comes from its release source (for example SkillsHub) or the version field in its `SKILL.md`. Record it in `SKILLS.md`.
- Before overwriting a skill, confirm the incoming package is the latest release. Check the release page and file timestamps, and compare hashes against the installed copy. Do not trust a file name such as "v3" alone.
- Every content change gets an entry in `CHANGELOG.md`: what changed, why, and how it was verified.
- Do not delete or silently roll back behavior or safety rules. Explain any replacement.

## Safety and quality checks

Before publishing:

- Every skill has a root `SKILL.md`.
- Markdown links and relative paths work.
- Scan for tokens, passwords, private URLs, personal data, local absolute paths, and temporary files.
- This repository is public. Do not publish interview transcripts, company-internal material, or credentials.
- Do not silently change the behavior of safety-sensitive scripts.
- After upload, compare remote files with the local source, file by file.

## Commits

- Write commit messages in Chinese, one purpose per commit, for example "新增 xx 套件" or "修正 xx 为最新发布版".
- Keep unrelated changes in separate commits.
