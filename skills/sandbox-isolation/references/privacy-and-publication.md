# Privacy and publication checks

Before publishing a skill, inspect the package only. Never scan or copy a user's whole workspace into a public repository.

Reject or remove:

- absolute Windows or POSIX paths;
- home, Desktop, Documents, Downloads, or user-profile paths;
- usernames, email addresses, phone numbers, account IDs, repository owners, and private URLs;
- tokens, passwords, cookies, API keys, SSH material, or environment dumps;
- real research notes, interview transcripts, daily logs, project data, or private filenames;
- runtime state, caches, `node_modules`, `__pycache__`, temporary reports, and generated archives;
- unreviewed third-party code or documentation.

Use abstract placeholders such as `<memory-root>`, `example-user`, and `example-workspace` in examples. A publication scan is a gate, not proof of legal authorization. Record license status honestly and do not infer MIT or another license from the absence of a license file.
