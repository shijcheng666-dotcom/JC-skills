#!/usr/bin/env python3
"""Read-only compact daily-log linter."""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

TAG_RE = re.compile(r"^\[[^\]\r\n]{1,40}\]\s+\S")
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")


def lint(root: Path, max_chars: int, governance_date: date | None) -> dict:
    files = []
    for path in sorted(root.glob("*.md")):
        match = DATE_RE.match(path.name)
        if not match:
            continue
        log_date = date.fromisoformat(match.group(1))
        historical = governance_date is not None and log_date < governance_date
        lines = path.read_text(encoding="utf-8").splitlines()
        nonempty = [line.strip() for line in lines if line.strip()]
        first = nonempty[0] if nonempty else ""
        summary = first.removeprefix("# ").strip()
        violations = []
        if not historical:
            if not TAG_RE.match(summary):
                violations.append({"line": 1, "reason": "missing topic tag or summary"})
            if len(summary) > max_chars:
                violations.append({"line": 1, "reason": f"summary exceeds {max_chars} characters"})
            if len(nonempty) > 2:
                violations.append({"line": 1, "reason": "daily log contains more than a compact entry"})
        files.append({
            "path": path.name,
            "historical": historical,
            "summary_chars": len(summary),
            "status": "historical" if historical else ("violation" if violations else "clean"),
            "violations": violations,
        })
    return {"summary_max_chars": max_chars, "governance_date": governance_date.isoformat() if governance_date else None, "files": files}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("memory_root", type=Path)
    parser.add_argument("--max-chars", type=int, default=20)
    parser.add_argument("--governance-date", type=date.fromisoformat)
    args = parser.parse_args()
    print(json.dumps(lint(args.memory_root, args.max_chars, args.governance_date), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
