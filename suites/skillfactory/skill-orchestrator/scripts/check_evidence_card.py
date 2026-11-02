# -*- coding: utf-8 -*-
"""check_evidence_card.py — 证据卡完整性与证据位置真实性校验。

用法：
    python check_evidence_card.py <证据卡文件 | 含证据卡的目录> [--base 证据位置相对路径的基准目录]

通过标准（逐张卡判定）：
    1. 六个必填字段齐全且非空：被测版本、输入或场景、成功标准、实际结果、证据位置、结论；
    2. 结论取值合法：观察到 / 待验证 / 失败；
    3. 证据位置若为文件路径（含扩展名或以 ./、../、/、盘符开头），必须真实存在；
       若为"运行 ID: xxx""对话消息"等声明型标记，记为声明型证据（通过但单独列出）。

退出码：0 全部通过；1 任一卡未通过或找不到证据卡。
"""
import re
import sys
from pathlib import Path

REQUIRED = ["被测版本", "输入或场景", "成功标准", "实际结果", "证据位置", "结论"]
VALID_CONCLUSION = {"观察到", "待验证", "失败"}
DECLARED_MARK = re.compile(r"^(运行\s*ID|对话消息|会话记录|见对话)", re.IGNORECASE)
PATH_LIKE = re.compile(r"^(\.|/|~|[A-Za-z]:)|\.[A-Za-z0-9]{1,8}$")


def split_cards(text: str) -> list[str]:
    """按 ```text 块切分；无代码块时整文视为一张卡。"""
    blocks = re.findall(r"```(?:text)?\s*\n(.*?)```", text, re.DOTALL)
    if blocks:
        return [b for b in blocks if "证据位置" in b]
    return [text] if "证据位置" in text else []


def parse_card(block: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^\s*([^：:]+)[：:]\s*(.*)$", line)
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    return fields


def check_card(idx: int, fields: dict[str, str], base: Path) -> bool:
    ok = True
    for key in REQUIRED:
        if key not in fields or not fields[key]:
            print(f"  [失败] 卡 {idx}: 缺少或非空字段: {key}")
            ok = False

    concl = fields.get("结论", "")
    if concl and concl not in VALID_CONCLUSION:
        print(f"  [失败] 卡 {idx}: 结论取值非法: {concl}（应为 观察到/待验证/失败）")
        ok = False

    loc = fields.get("证据位置", "")
    if loc:
        if DECLARED_MARK.search(loc):
            print(f"  [提示] 卡 {idx}: 声明型证据（{loc[:40]}…），建议附可定位路径" if len(loc) > 40 else f"  [提示] 卡 {idx}: 声明型证据（{loc}），建议附可定位路径")
        elif PATH_LIKE.search(loc):
            target = Path(loc)
            if not target.is_absolute():
                target = base / loc
            if target.exists():
                print(f"  [通过] 卡 {idx}: 证据位置存在: {loc}")
            else:
                print(f"  [失败] 卡 {idx}: 证据位置不存在: {loc}（基准 {base}）")
                ok = False
        else:
            print(f"  [提示] 卡 {idx}: 证据位置为自由文本，无法客观核验: {loc[:40]}")
    return ok


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("用法: python check_evidence_card.py <文件|目录> [--base 基准目录]")
        return 1
    target = Path(args[0])
    base = target.parent if target.is_file() else target
    if "--base" in args:
        base = Path(args[args.index("--base") + 1])

    files: list[Path] = []
    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = sorted(target.rglob("*.md")) + sorted(target.rglob("*.txt"))
    else:
        print(f"[失败] 路径不存在: {target}")
        return 1

    total, passed = 0, 0
    for f in files:
        cards = split_cards(f.read_text(encoding="utf-8", errors="replace"))
        for i, block in enumerate(cards, 1):
            total += 1
            if check_card(i, parse_card(block), base):
                passed += 1
                print(f"  [通过] {f.name} 卡 {i}")
            else:
                print(f"  [定位] {f}")

    if total == 0:
        print(f"[失败] 未找到任何证据卡（需包含『证据位置』字段）: {target}")
        return 1

    print(f"[结论] {passed}/{total} 张证据卡通过。" if passed == total else f"[结论] {passed}/{total} 通过：未通过的卡不得作为『已评估/已回归』的依据。")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
