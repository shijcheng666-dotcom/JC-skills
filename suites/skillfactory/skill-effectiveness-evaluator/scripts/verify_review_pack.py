#!/usr/bin/env python3
"""Verify a frozen anonymous review pack without modifying it."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

AREAS = ("final-quality", "process-quality")
SAFE_NAME = re.compile(r"^task-T(?P<task>\d{2})-(?P<candidate>CAND-[AB])\.md$")
UNIT_RE = re.compile(r"\bu\d+\b", re.IGNORECASE)
FORBIDDEN = (
    re.compile(r"\bARM-\d+\b", re.IGNORECASE),
    re.compile(r"\b(?:CAND|CTRL|TREATMENT)[-_ ]?\d+\b", re.IGNORECASE),
    re.compile(r"\bload\s+evidence\b", re.IGNORECASE),
    re.compile(r"\b(?:skill|version|candidate)\s*(?:name|version|id)\s*[:=]", re.IGNORECASE),
    re.compile(r"执行代理|执行者角色|执行单元|运行目录|真实加载|加载状态|实验组别|候选版本|技能名称|版本名称"),
)


def materials(pack: Path) -> list[Path]:
    paths: list[Path] = []
    for area in AREAS:
        directory = pack / area
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError(f"missing or unsafe area: {area}")
        entries = list(directory.iterdir())
        if not entries:
            raise ValueError(f"empty area: {area}")
        for path in entries:
            if path.is_symlink() or not path.is_file():
                raise ValueError(f"non-regular material: {path}")
            if path.suffix.lower() != ".md":
                raise ValueError(f"unexpected file in material area: {path.name}")
            if not SAFE_NAME.fullmatch(path.name):
                raise ValueError(f"unsafe material filename: {path.name}")
            paths.append(path)
    return sorted(paths, key=lambda p: p.relative_to(pack).as_posix())


def manifest_entries(pack: Path, paths: list[Path]) -> list[dict[str, str]]:
    return [
        {"path": path.relative_to(pack).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in paths
    ]


def compute_hash(entries: list[dict[str, str]]) -> str:
    payload = "".join(f"{item['path']}\t{item['sha256']}\n" for item in entries).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def check(pack: Path, expected: str | None) -> int:
    try:
        if not pack.is_dir():
            raise ValueError(f"pack directory missing: {pack}")
        manifest_path = pack / "pack-manifest.json"
        if not manifest_path.is_file() or manifest_path.is_symlink():
            raise ValueError("pack-manifest.json missing")
        declared = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        if declared.get("schema_version") != 1 or declared.get("algorithm") != "sha256":
            raise ValueError("unsupported manifest schema or algorithm")
        allowed_root = {"pack-manifest.json", "SCORING.md", "anonymization-report.json"}
        unexpected_root = {path.name for path in pack.iterdir() if path.name not in allowed_root and path.name not in AREAS}
        if unexpected_root:
            raise ValueError(f"unexpected root files: {sorted(unexpected_root)}")
        paths = materials(pack)
        entries = manifest_entries(pack, paths)
        actual_set = {(item["path"], item["sha256"]) for item in entries}
        declared_files = declared.get("files")
        if not isinstance(declared_files, list):
            raise ValueError("manifest files must be a list")
        if len(declared_files) != len(entries):
            raise ValueError("manifest file count mismatch or duplicate entries")
        if any(not isinstance(item, dict) or set(item) != {"path", "sha256"} for item in declared_files):
            raise ValueError("manifest entries must contain only path and sha256")
        declared_paths = [item["path"] for item in declared_files]
        if declared_paths != sorted(declared_paths) or len(set(declared_paths)) != len(declared_paths):
            raise ValueError("manifest paths must be unique and sorted")
        if any(not isinstance(item["path"], str) or not isinstance(item["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) for item in declared_files):
            raise ValueError("manifest entry path or sha256 format is invalid")
        declared_set = {(item["path"], item["sha256"]) for item in declared_files}
        if actual_set != declared_set:
            raise ValueError("manifest file set or file hash mismatch")
        digest = compute_hash(entries)
        actual_hash = f"sha256:{digest}"
        if declared.get("blind_pack_hash") != actual_hash:
            raise ValueError(f"manifest blind_pack_hash mismatch: {declared.get('blind_pack_hash')} != {actual_hash}")
        scoring_path = pack / "SCORING.md"
        if scoring_path.is_symlink() or not scoring_path.is_file():
            raise ValueError("SCORING.md must be a regular file")
        declared_scoring = declared.get("scoring_sha256")
        actual_scoring = f"sha256:{hashlib.sha256(scoring_path.read_bytes()).hexdigest()}"
        if not isinstance(declared_scoring, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", declared_scoring):
            raise ValueError("scoring_sha256 format is invalid")
        if declared_scoring != actual_scoring:
            raise ValueError(f"scoring hash mismatch: {declared_scoring} != {actual_scoring}")
        report_path = pack / "anonymization-report.json"
        if report_path.is_symlink() or not report_path.is_file():
            raise ValueError("anonymization-report.json must be a regular file")
        report = json.loads(report_path.read_text(encoding="utf-8-sig"))
        if not isinstance(report, dict) or set(report) != {path.relative_to(pack).as_posix() for path in paths}:
            raise ValueError("anonymization report must cover exactly the review materials")
        if expected and expected != actual_hash:
            raise ValueError(f"expected hash mismatch: {expected} != {actual_hash}")
        by_task: dict[str, dict[str, set[str]]] = {}
        for path in paths:
            match = SAFE_NAME.fullmatch(path.name)
            assert match
            task = match.group("task")
            candidate = match.group("candidate")
            area = path.parent.name
            by_task.setdefault(task, {}).setdefault(area, set()).add(candidate)
            text = path.read_text(encoding="utf-8-sig")
            stripped = re.sub(r"\bCAND-[AB]\b", "", text)
            if UNIT_RE.search(stripped):
                raise ValueError(f"unit id leak: {path.relative_to(pack)}")
            for pattern in FORBIDDEN:
                if pattern.search(stripped):
                    raise ValueError(f"forbidden metadata ({pattern.pattern}): {path.relative_to(pack)}")
        expected_candidates = {"CAND-A", "CAND-B"}
        for task, areas in by_task.items():
            for area in AREAS:
                if areas.get(area) != expected_candidates:
                    raise ValueError(f"incomplete candidate pair: {area}/{task}")
        print(f"REVIEW PACK VALID: {len(paths)} materials, {len(by_task)} tasks")
        print(f"blind_pack_hash={actual_hash}")
        return 0
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"REVIEW PACK INVALID: {exc}", file=sys.stderr)
        return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack", type=Path)
    parser.add_argument("--expected-hash")
    args = parser.parse_args()
    return check(args.pack, args.expected_hash)


if __name__ == "__main__":
    raise SystemExit(main())
