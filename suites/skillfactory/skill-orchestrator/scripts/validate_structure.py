# -*- coding: utf-8 -*-
"""validate_structure.py — 候选结构校验：frontmatter、命名、目录与引用死链。

用法：
    python validate_structure.py <skill_dir>

检查项（全部为客观判定）：
    1. SKILL.md 存在且非空；
    2. YAML frontmatter 存在，且含 name 与 description 两个必填字段；
    3. name 符合命名规范（小写字母、数字、短横线）；
    4. SKILL.md 中以相对路径引用的 scripts/、references/、assets/ 资源真实存在（死链检查；
       围栏代码块与"示例/例如"类说明行中的举例路径不计为依赖）。

退出码：0 通过；1 未通过。
"""
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# 匹配 markdown 链接与行内代码中的相对资源路径
REF_RE = re.compile(r"(?:\]\(|`)(scripts/[^)`\s]+|references/[^)`\s]+|assets/[^)`\s]+)")


def fail(msg: str) -> None:
    print(f"  [失败] {msg}")


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python validate_structure.py <skill_dir>")
        return 1
    skill_dir = Path(sys.argv[1])
    ok = True

    skill_md = skill_dir / "SKILL.md"
    if not skill_dir.is_dir():
        print(f"[失败] 目录不存在: {skill_dir}")
        return 1
    if not skill_md.is_file() or skill_md.stat().st_size == 0:
        print(f"[失败] SKILL.md 缺失或为空: {skill_md}")
        return 1
    print(f"检查对象: {skill_md}")

    text = skill_md.read_text(encoding="utf-8")

    # frontmatter 块
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        fail("缺少 YAML frontmatter 块（文件须以 --- 起始）")
        print("[结论] 未通过")
        return 1
    fm = m.group(1)

    fields = {}
    for line in fm.splitlines():
        kv = re.match(r"^([A-Za-z_-]+)\s*:\s*(.*)$", line)
        if kv:
            fields[kv.group(1)] = kv.group(2).strip().strip('"').strip("'")

    for required in ("name", "description"):
        if required not in fields or not fields[required]:
            fail(f"frontmatter 缺少必填字段: {required}")
            ok = False

    name = fields.get("name", "")
    if name:
        if not NAME_RE.match(name):
            fail(f"name 不符合命名规范（小写字母/数字/短横线）: {name}")
            ok = False
        elif skill_dir.name != name:
            print(f"  [提示] 目录名 {skill_dir.name} 与 name {name} 不一致，安装时以 name 为准")

    desc = fields.get("description", "")
    if desc and len(desc) > 1024:
        fail(f"description 超长（{len(desc)} 字符 > 1024）")
        ok = False

    # 引用死链：排除示例语境（围栏代码块、"示例/例如/比如"类说明行）中的引用，
    # 避免把"可以放什么"的文档举例误判为依赖死链。
    example_markers = ("示例", "例如", "比如", "example", "e.g.")
    refs = set()
    in_code_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        lowered = stripped.lower()
        if any(m in stripped or m in lowered for m in example_markers):
            continue
        refs.update(REF_RE.findall(line))
    refs = sorted(refs)
    if not refs:
        print("  [提示] 未发现 scripts/、references/、assets/ 相对引用")
    for ref in refs:
        target = skill_dir / ref
        if target.exists():
            print(f"  [通过] 引用存在: {ref}")
        else:
            fail(f"引用死链: {ref}")
            ok = False

    print("[结论] 通过" if ok else "[结论] 未通过：修复上述失败项后重新运行。")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
