#!/usr/bin/env python3
"""Read-only memory workspace audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SYSTEM_FILES = {
    "profile.md": "system_memory",
    "MEMORY.md": "system_memory",
    "raw/memories.md": "system_memory",
}
RULE_CANDIDATES = ("topics/project_rules.md", "project-rules.md")
STATE_NAMES = {"selector-state.json"}


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def record(root: Path, path: Path, category: str, status: str, evidence: list[str], action: str, confirm: bool) -> dict:
    return {
        "path": rel(root, path),
        "category": category,
        "status": status,
        "evidence": evidence[:3],
        "proposed_action": action,
        "requires_confirmation": confirm,
    }


def inspect_file(root: Path, path: Path, category: str) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return record(root, path, category, "malformed", ["not valid UTF-8"], "review", True)
    except OSError as exc:
        return record(root, path, category, "unknown", [type(exc).__name__], "review", True)
    indicators = []
    if category == "system_memory" and len(text.strip()) > 0:
        indicators.append(f"{len(text.splitlines())} non-empty lines")
    if category == "daily_log":
        indicators.append(f"{len(text.splitlines())} lines")
    status = "clean" if not indicators else "unknown"
    return record(root, path, category, status, indicators or ["empty"], "none", False)


def audit(memory_root: Path) -> dict:
    root = memory_root.resolve()
    if not root.is_dir():
        return {
            "mode": "diagnose",
            "governance": "missing",
            "read_only": True,
            "writes_performed": False,
            "limitations": ["memory root does not exist"],
            "files": [],
        }
    files: list[dict] = []
    governance = root / "GOVERNANCE.md"
    governance_state = "present" if governance.is_file() else "missing"
    if governance.is_file():
        files.append(inspect_file(root, governance, "governance"))
    else:
        files.append(record(root, governance, "governance", "missing", ["GOVERNANCE.md not found"], "create_by_user", True))

    for name, category in SYSTEM_FILES.items():
        path = root / name
        if path.is_file():
            files.append(inspect_file(root, path, category))
        else:
            files.append(record(root, path, category, "missing", ["file not found"], "review", True))

    rule_paths = [root / candidate for candidate in RULE_CANDIDATES if (root / candidate).is_file()]
    if len(rule_paths) > 1:
        for path in rule_paths:
            files.append(record(root, path, "system_memory", "conflict", ["multiple rules-file candidates exist"], "review", True))
    elif len(rule_paths) == 1:
        files.append(inspect_file(root, rule_paths[0], "system_memory"))
    else:
        files.append(record(root, root / RULE_CANDIDATES[0], "system_memory", "missing", ["no rules-file candidate found"], "review", True))

    for path in sorted(root.glob("*.md")):
        if path.name == "GOVERNANCE.md" or path.name == "MEMORY.md" or path.name == "profile.md":
            continue
        if path.name.count("-") == 2 and len(path.stem) == 10:
            files.append(inspect_file(root, path, "daily_log"))
        else:
            files.append(record(root, path, "extra", "unknown", ["unclassified markdown file"], "review", True))
    for name in STATE_NAMES:
        path = root / name
        if path.is_file():
            files.append(inspect_file(root, path, "state"))
    return {
        "mode": "diagnose",
        "governance": governance_state,
        "read_only": True,
        "writes_performed": False,
        "limitations": ["This audit does not prevent host-level memory writes."],
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("memory_root", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.memory_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
