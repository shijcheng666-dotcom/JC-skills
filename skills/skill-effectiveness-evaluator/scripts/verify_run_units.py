#!/usr/bin/env python3
"""Verify execution-unit evidence before strict status aggregation."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED_FILES = ("input.json", "execution.json", "transcript.md", "artifact.md", "status.json")
ALLOWED_STATUSES = {"VALID", "LIMITED", "INVALID", "CONTAMINATED", "SUPERSEDED"}
TASK_ID_RE = re.compile(r"^[A-Za-z0-9._:-]+$")


def fail(message: str) -> None:
    raise ValueError(message)


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON: {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON object required: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_unit(unit: Path) -> None:
    if not unit.is_dir() or unit.is_symlink():
        fail(f"unit directory missing or unsafe: {unit}")
    missing = [name for name in REQUIRED_FILES if not (unit / name).is_file()]
    if missing:
        fail(f"required files missing in {unit.name}: {', '.join(missing)}")

    read_json(unit / "input.json")
    execution = read_json(unit / "execution.json")
    status = read_json(unit / "status.json")

    unit_id = execution.get("unit_id")
    if not isinstance(unit_id, str) or not unit_id:
        fail("execution.unit_id is required")
    if status.get("unit_id") != unit_id:
        fail("status.unit_id does not match execution.unit_id")

    task_id = execution.get("subagent_task_id")
    if not isinstance(task_id, str) or not TASK_ID_RE.fullmatch(task_id):
        fail("execution.subagent_task_id must identify a task invocation")
    if execution.get("subagent_context") != "fresh":
        fail("execution.subagent_context must be fresh")

    input_hash = execution.get("execution_input_fingerprint")
    actual_input_hash = f"sha256:{sha256(unit / 'input.json')}"
    if input_hash != actual_input_hash:
        fail(f"input fingerprint mismatch: {input_hash} != {actual_input_hash}")

    transcript = (unit / "transcript.md").read_text(encoding="utf-8-sig").strip()
    artifact = (unit / "artifact.md").read_text(encoding="utf-8-sig").strip()
    if not transcript:
        fail("transcript.md is empty")
    if not artifact:
        fail("artifact.md is empty")

    structured = execution.get("structured_result")
    if not isinstance(structured, dict):
        fail("execution.structured_result is required")
    for field in ("status", "verification", "concerns", "next_steps", "artifact_paths", "constraint_checks"):
        if field not in structured:
            fail(f"structured_result.{field} is required")

    checks = status.get("constraint_checks")
    if not isinstance(checks, dict):
        fail("status.constraint_checks is required")
    if checks.get("subagent_task_verified") != "verified":
        fail("subagent_task_verified must be verified")
    if checks.get("fresh_context_verified") != "verified":
        fail("fresh_context_verified must be verified")
    if checks.get("execution_input_match") is not True:
        fail("execution_input_match must be true")
    if checks.get("artifact_complete") is not True:
        fail("artifact_complete must be true")

    state = status.get("status")
    if state not in ALLOWED_STATUSES:
        fail(f"unsupported status: {state}")
    if state == "VALID":
        if execution.get("executor_model_id") in (None, "", "unknown"):
            fail("VALID requires an exact executor_model_id")
        if checks.get("load_or_injection_verified") is not True:
            fail("VALID requires verified load or injection evidence")
        if checks.get("isolation_verified") != "verified":
            fail("VALID requires verified isolation evidence")
        if not execution.get("evidence_refs", {}).get("load"):
            fail("VALID requires load or injection evidence references")

    print(f"RUN UNIT VALID: {unit.name} status={state} task={task_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", type=Path, help="runs directory or one unit directory")
    args = parser.parse_args()
    try:
        root = args.runs
        units = [root] if (root / "execution.json").is_file() else sorted(
            path for path in root.iterdir() if path.is_dir() and not path.is_symlink()
        )
        if not units:
            fail(f"no run units found: {root}")
        for unit in units:
            verify_unit(unit)
        print(f"RUN UNITS VALID: {len(units)}")
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"RUN UNITS INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
