#!/usr/bin/env python3
"""
本地 Agent 长期记忆备份脚本
在修改前完整备份所有记忆文件。

用法：
  python memory_backup.py [--memory-dir PATH] [--backup-dir PATH]
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
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

FILES_TO_BACKUP = [
    "MEMORY.md",
    "profile.md",
    "raw/memories.md",
    "topics/user_preferences.md",
    "topics/assistant_feedback.md",
    "topics/references.md",
]


def run_backup(memory_dir: Path, backup_base: Path | None = None) -> dict:
    """执行备份，返回备份结果。"""
    if backup_base is None:
        backup_base = memory_dir / "backups"

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = backup_base / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    backed_up = []
    failed = []

    for rel_path in FILES_TO_BACKUP:
        src = memory_dir / rel_path
        if not src.exists():
            failed.append({"file": rel_path, "reason": "源文件不存在"})
            continue

        dst = backup_dir / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src, dst)
            if dst.exists() and dst.stat().st_size == src.stat().st_size:
                backed_up.append({
                    "file": rel_path,
                    "src_size": src.stat().st_size,
                    "dst_size": dst.stat().st_size,
                    "verified": True,
                })
            else:
                failed.append({"file": rel_path, "reason": "备份验证失败：大小不一致"})
        except Exception as e:
            failed.append({"file": rel_path, "reason": str(e)})

    result = {
        "backup_time": timestamp,
        "backup_dir": str(backup_dir),
        "backed_up": backed_up,
        "failed": failed,
        "success": len(failed) == 0,
    }

    meta_file = backup_dir / "_backup_meta.json"
    import json
    meta_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    return result


def main():
    parser = argparse.ArgumentParser(description="本地 Agent 长期记忆备份脚本")
    parser.add_argument("--memory-dir", type=str, default=str(DEFAULT_MEMORY_DIR))
    parser.add_argument("--backup-dir", type=str, default=None)
    args = parser.parse_args()

    memory_dir = Path(args.memory_dir)
    backup_dir = Path(args.backup_dir) if args.backup_dir else None

    result = run_backup(memory_dir, backup_dir)

    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
