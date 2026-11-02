# -*- coding: utf-8 -*-
"""check_capability_baseline.py — 能力基线检查：依赖 Skill 存在性、可读性与调度接口。

用法：
    python check_capability_baseline.py <skills_dir>

skills_dir 为安装各参与 Skill 的固定工作区目录，其下应含以 Skill 名命名的子目录。

判定规则：
    - 核心硬门禁（skill-creator、skill-effectiveness-evaluator）：缺失或不可读即未通过；
    - 条件调度专项（writing-for-agents、skill-from-externals、skill-from-masters）：缺失记为不可用，不判整体失败；
    - 每个可读的 Skill 检查 SKILL.md 是否含"调度接口"一节；缺失记为契约缺口（提示，不判失败）。

退出码：0 硬门禁齐备；1 任一硬门禁缺失或不可读。
"""
import sys
from pathlib import Path

HARD_GATES = ["skill-creator", "skill-effectiveness-evaluator"]
CONDITIONAL = ["writing-for-agents", "skill-from-externals", "skill-from-masters"]


def check_one(skills_dir: Path, name: str, hard: bool) -> bool:
    layer = "硬门禁" if hard else "专  项"
    skill_md = skills_dir / name / "SKILL.md"
    if not skill_md.is_file():
        print(f"  [{'失败' if hard else '不可用'}] [{layer}] {name}: SKILL.md 不存在（{skills_dir / name}）")
        return not hard
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"  [{'失败' if hard else '不可用'}] [{layer}] {name}: 不可读（{e}）")
        return not hard

    if "调度接口" in text:
        print(f"  [通过] [{layer}] {name}: 可读，调度接口已定义")
    else:
        print(f"  [契约缺口] [{layer}] {name}: 可读，但未定义『调度接口』一节，按其最低专项产出调度")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python check_capability_baseline.py <skills_dir>")
        return 1
    skills_dir = Path(sys.argv[1])
    if not skills_dir.is_dir():
        print(f"[失败] 工作区目录不存在: {skills_dir}")
        return 1

    print(f"工作区: {skills_dir}")
    ok = True
    for name in HARD_GATES:
        ok = check_one(skills_dir, name, hard=True) and ok
    for name in CONDITIONAL:
        check_one(skills_dir, name, hard=False)

    if ok:
        print("[结论] 核心硬门禁齐备，可进入生产阶段。专项不可用项按降级规则处理。")
        return 0
    print("[结论] 核心硬门禁未齐备：状态为『等待核心能力基线』，不得进入生产阶段。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
