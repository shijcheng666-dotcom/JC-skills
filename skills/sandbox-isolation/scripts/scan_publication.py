#!/usr/bin/env python3
"""Read-only publication hygiene scanner."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PATTERNS = {
    "absolute_windows_path": re.compile(r"[A-Za-z]:[\\/]"),
    "home_path": re.compile(r"(?:~[/\\]|/home/|/Users/|[A-Za-z]:[/\\][^\\r\\n]{0,80}[\\\\/]Users[/\\])"),
    "secret_like": re.compile(r"(?i)(api[_-]?key|access[_-]?token|password|secret|cookie)\s*[:=]"),
}
EXCLUDED = {".zip", ".pyc"}
PRIVATE_PARTS = {"node_modules", "__pycache__", ".aime", "selector-state.json"}


def scan(root: Path) -> dict:
    findings = []
    for path in sorted(root.rglob("*")):
        if path.name == "scan_publication.py":
            continue
        if any(part in PRIVATE_PARTS for part in path.parts):
            findings.append({"path": path.relative_to(root).as_posix(), "line": 0, "type": "private_runtime_path"})
            continue
        if not path.is_file() or path.suffix.lower() in EXCLUDED:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append({"path": path.relative_to(root).as_posix(), "line": line, "type": name})
    return {"root": ".", "read_only": True, "findings": findings, "status": "fail" if findings else "pass"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_root", type=Path)
    args = parser.parse_args()
    report = scan(args.package_root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
