# -*- coding: utf-8 -*-
"""verify_backup.py — 演进闸门第 1 步：验证备份存在、可读并输出指纹。

用法：
    python verify_backup.py <skill_dir> [--backup-dir backups]

通过标准：
    1. 备份目录存在；
    2. 至少一个备份文件存在、非空且可完整读取；
    3. 输出最新备份的 sha256 指纹与全部备份清单。

退出码：0 通过；1 未通过。
"""
import hashlib
import sys
from pathlib import Path


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python verify_backup.py <skill_dir> [--backup-dir backups]")
        return 1
    skill_dir = Path(sys.argv[1])
    backup_name = "backups"
    if "--backup-dir" in sys.argv:
        i = sys.argv.index("--backup-dir")
        backup_name = sys.argv[i + 1]

    if not skill_dir.is_dir():
        print(f"[失败] Skill 目录不存在: {skill_dir}")
        return 1

    backup_dir = skill_dir / backup_name
    if not backup_dir.is_dir():
        print(f"[失败] 备份目录不存在: {backup_dir}")
        print("行为改动前必须先创建备份目录并放入当前正式版本的副本。")
        return 1

    backups = sorted(
        [p for p in backup_dir.iterdir() if p.is_file()],
        key=lambda p: p.stat().st_mtime,
    )
    if not backups:
        print(f"[失败] 备份目录为空: {backup_dir}")
        return 1

    print(f"备份目录: {backup_dir}")
    print(f"备份数量: {len(backups)}")
    latest = backups[-1]
    ok = True
    for p in backups:
        try:
            size = p.stat().st_size
            if size == 0:
                print(f"  [失败] 空备份文件: {p.name}")
                ok = False
                continue
            digest = sha256_of(p)
            tag = "最新" if p == latest else "    "
            print(f"  {tag} {p.name}  {size}B  sha256:{digest}")
        except OSError as e:
            print(f"  [失败] 备份不可读: {p.name} ({e})")
            ok = False

    if not ok:
        print("[结论] 备份验证未通过：请先修复上述失败项，再进行任何行为改动。")
        return 1

    print(f"[结论] 通过。最新备份 {latest.name}，指纹 sha256:{sha256_of(latest)}")
    print("将该指纹写入演进清单的『备份指纹』字段。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
