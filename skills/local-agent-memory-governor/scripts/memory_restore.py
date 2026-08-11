#!/usr/bin/env python3
"""
本地 Agent 长期记忆回滚脚本
从指定备份目录恢复记忆文件。

用法：
  python memory_restore.py --backup-dir PATH [--memory-dir PATH] [--dry-run]
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


def _detect_memory_dir() -> Path:
    if os.environ.get("LOCAL_AGENT_MEMORY_DIR"):
        return Path(os.environ["LOCAL_AGENT_MEMORY_DIR"])
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        candidate = Path(local_appdata) / "local-agent" / "memory"
        if candidate.exists():
            return candidate
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidate = Path(appdata) / "local-agent" / "memory"
        if candidate.exists():
            return candidate
    base = local_appdata or appdata or ""
    return Path(base) / "local-agent" / "memory"

DEFAULT_MEMORY_DIR = _detect_memory_dir()


def list_backups(memory_dir: Path) -> list[dict]:
    """列出所有可用备份。"""
    backups_dir = memory_dir / "backups"
    if not backups_dir.exists():
        return []

    backups = []
    for d in sorted(backups_dir.iterdir(), reverse=True):
        if not d.is_dir():
            continue
        meta_file = d / "_backup_meta.json"
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                backups.append({
                    "dir": str(d),
                    "name": d.name,
                    "backup_time": meta.get("backup_time", d.name),
                    "files_backed_up": len(meta.get("backed_up", [])),
                    "success": meta.get("success", False),
                })
            except Exception:
                backups.append({"dir": str(d), "name": d.name, "backup_time": d.name, "files_backed_up": 0, "success": False})
        else:
            files = list(d.rglob("*.md"))
            backups.append({"dir": str(d), "name": d.name, "backup_time": d.name, "files_backed_up": len(files), "success": True})
    return backups


def run_restore(backup_dir: Path, memory_dir: Path, dry_run: bool = False) -> dict:
    """从备份恢复记忆文件。"""
    if not backup_dir.exists():
        return {"success": False, "error": f"备份目录不存在: {backup_dir}"}

    restored = []
    failed = []
    skipped = []

    for md_file in backup_dir.rglob("*.md"):
        rel_path = md_file.relative_to(backup_dir)
        if rel_path.name.startswith("_"):
            continue

        dst = memory_dir / rel_path

        if dry_run:
            skipped.append({"file": str(rel_path), "src": str(md_file), "dst": str(dst)})
            continue

        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(md_file, dst)
            if dst.exists() and dst.stat().st_size == md_file.stat().st_size:
                restored.append({
                    "file": str(rel_path),
                    "size": dst.stat().st_size,
                    "verified": True,
                })
            else:
                failed.append({"file": str(rel_path), "reason": "恢复验证失败"})
        except Exception as e:
            failed.append({"file": str(rel_path), "reason": str(e)})

    return {
        "backup_dir": str(backup_dir),
        "memory_dir": str(memory_dir),
        "dry_run": dry_run,
        "restored": restored,
        "failed": failed,
        "skipped": skipped,
        "success": len(failed) == 0,
    }


def main():
    parser = argparse.ArgumentParser(description="本地 Agent 长期记忆回滚脚本")
    parser.add_argument("--backup-dir", type=str, required=False, help="备份目录路径（不指定则列出可用备份）")
    parser.add_argument("--memory-dir", type=str, default=str(DEFAULT_MEMORY_DIR))
    parser.add_argument("--dry-run", action="store_true", help="只预览不执行")
    parser.add_argument("--list", action="store_true", help="列出可用备份")
    args = parser.parse_args()

    memory_dir = Path(args.memory_dir)

    if args.list or not args.backup_dir:
        backups = list_backups(memory_dir)
        print(json.dumps({"backups": backups}, ensure_ascii=False, indent=2))
        if not backups:
            print("没有找到可用备份", file=sys.stderr)
        return

    backup_dir = Path(args.backup_dir)
    result = run_restore(backup_dir, memory_dir, args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
