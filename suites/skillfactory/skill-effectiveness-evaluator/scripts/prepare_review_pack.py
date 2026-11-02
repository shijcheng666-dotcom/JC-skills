#!/usr/bin/env python3
"""Create a frozen, anonymous review pack for content-effect evaluations."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

AREAS = ("final-quality", "process-quality")
SOURCE_NAME = re.compile(r"^(?P<task>.+)-(?P<candidate>CAND-[AB])\.md$")
UNIT_RE = re.compile(r"\bu\d+\b", re.IGNORECASE)
FORBIDDEN = (
    re.compile(r"\bARM-\d+\b", re.IGNORECASE),
    re.compile(r"\b(?:CAND|CTRL|TREATMENT)[-_ ]?\d+\b", re.IGNORECASE),
    re.compile(r"\bload\s+evidence\b", re.IGNORECASE),
    re.compile(r"\b(?:skill|version|candidate)\s*(?:name|version|id)\s*[:=]", re.IGNORECASE),
    re.compile(r"执行代理|执行者角色|执行单元|运行目录|真实加载|加载状态|实验组别|候选版本|技能名称|版本名称"),
)
METADATA_LINE = re.compile(
    r"^\s*>?\s*(?:load evidence|task unit|run directory|executor|candidate|group|skill name|version name|任务单元：|运行目录：|执行者：|执行单元：|组别：|候选版本：|技能名称：|版本名称：).*$",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    raise ValueError(message)


def read_source(source: Path) -> dict[str, dict[str, Path]]:
    if not source.is_dir():
        fail(f"source directory missing: {source}")
    result: dict[str, dict[str, Path]] = {}
    source = source.absolute()
    for area in AREAS:
        directory = source / area
        if directory.is_symlink() or not directory.is_dir():
            fail(f"source area missing or unsafe: {area}")
        files = sorted(directory.glob("*.md"), key=lambda p: p.name)
        if not files:
            fail(f"source area is empty: {area}")
        for path in files:
            if not path.is_file() or path.is_symlink():
                fail(f"source must contain regular files only: {path}")
            match = SOURCE_NAME.fullmatch(path.name)
            if not match:
                fail(f"source filename must be task-<id>-CAND-A/B.md: {path.name}")
            task = match.group("task")
            candidate = match.group("candidate")
            result.setdefault(task, {})[f"{area}:{candidate}"] = path
    tasks = sorted(result)
    if not tasks:
        fail("no candidate materials found")
    for task in tasks:
        for area in AREAS:
            expected = {f"{area}:CAND-A", f"{area}:CAND-B"}
            actual = {key for key in result.get(task, {}) if key.startswith(f"{area}:")}
            if actual != expected:
                fail(f"incomplete candidate pair for {area}/{task}: {sorted(actual)}")
    return result


def anonymize(text: str) -> tuple[str, list[dict[str, str | int]]]:
    kept: list[str] = []
    changes: list[dict[str, str | int]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        original = line
        if METADATA_LINE.search(line):
            changes.append({"line": line_number, "action": "removed", "before": original, "after": ""})
            continue
        line = re.sub(r"\b(?:CTRL|TREATMENT)[-_ ]?\d+\b", "", line, flags=re.IGNORECASE)
        line = re.sub(r"执行代理|执行者角色|执行单元|运行目录|真实加载|加载状态|实验组别|候选版本|技能名称|版本名称", "", line)
        line = line.rstrip()
        if line != original:
            changes.append({"line": line_number, "action": "replaced", "before": original, "after": line})
        kept.append(line)
    return "\n".join(kept).strip() + "\n", changes


def check_text(text: str, path: Path) -> None:
    stripped = re.sub(r"\bCAND-[AB]\b", "", text)
    if UNIT_RE.search(stripped):
        fail(f"unit id leak after anonymization: {path.name}")
    for pattern in FORBIDDEN:
        if pattern.search(stripped):
            fail(f"forbidden metadata after anonymization ({pattern.pattern}): {path.name}")


def material_manifest(pack: Path) -> list[dict[str, str]]:
    files = sorted(
        [p for area in AREAS for p in (pack / area).glob("*.md")],
        key=lambda p: p.relative_to(pack).as_posix(),
    )
    entries = []
    for path in files:
        entries.append({"path": path.relative_to(pack).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return entries


def pack_hash(entries: list[dict[str, str]]) -> str:
    payload = "".join(f"{item['path']}\t{item['sha256']}\n" for item in entries).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build(source: Path, output: Path, scoring: Path | None) -> None:
    source_files = read_source(source)
    output = output.absolute()
    if output == source.absolute() or output.is_relative_to(source.absolute()):
        fail("output must not be the source directory or inside it")
    if output.exists():
        fail(f"refusing to overwrite existing output: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        if scoring is None:
            fail("formal review packs require --scoring-card")
        if not scoring.is_file() or scoring.is_symlink():
            fail(f"scoring card must be a regular file: {scoring}")
        task_labels = {task: f"T{index:02d}" for index, task in enumerate(sorted(source_files), start=1)}
        anonymization_report: dict[str, list[dict[str, str | int]]] = {}
        for area in AREAS:
            (temp / area).mkdir()
            for task in sorted(source_files):
                for candidate in ("CAND-A", "CAND-B"):
                    source_path = source_files[task][f"{area}:{candidate}"]
                    text, changes = anonymize(source_path.read_text(encoding="utf-8-sig"))
                    check_text(text, source_path)
                    safe_name = f"task-{task_labels[task]}-{candidate}.md"
                    target = temp / area / safe_name
                    target.write_text(text, encoding="utf-8", newline="\n")
                    anonymization_report[target.relative_to(temp).as_posix()] = changes
        entries = material_manifest(temp)
        digest = pack_hash(entries)
        scoring_hash = hashlib.sha256(scoring.read_bytes()).hexdigest()
        shutil.copyfile(scoring, temp / "SCORING.md")
        (temp / "anonymization-report.json").write_text(
            json.dumps(anonymization_report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        manifest = {
            "schema_version": 1,
            "algorithm": "sha256",
            "scope": "final-quality + process-quality markdown materials",
            "files": entries,
            "blind_pack_hash": f"sha256:{digest}",
            "scoring_sha256": f"sha256:{scoring_hash}",
        }
        (temp / "pack-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        if output.exists():
            fail(f"output appeared during build: {output}")
        temp.replace(output)
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise
    print(f"Created {len(entries)} blinded materials")
    print(f"blind_pack_hash=sha256:{digest}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--scoring-card", type=Path)
    args = parser.parse_args()
    try:
        build(args.source, args.output, args.scoring_card)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"REVIEW PACK NOT CREATED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
