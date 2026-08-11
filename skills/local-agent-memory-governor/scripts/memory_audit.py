#!/usr/bin/env python3
"""
本地 Agent 长期记忆审计脚本
自动完成审计基线阶段的机械工作，输出结构化 JSON 供 AI 进行语义判断。

用法：
  python memory_audit.py [--memory-dir PATH] [--output PATH]

默认 memory-dir 为标准桌面端记忆目录。
默认输出到 stdout。
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# 默认记忆目录（自动探测：环境变量 → %APPDATA% → 报错）
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

# 项目级信息的路径模式（用于检测 references.md 中的违规路径）
# 收紧：只匹配"真正的项目级路径/文档"，不匹配跨项目通用的固定信息。
# 注意：vivo Docs 是跨项目长期通用的访问方式（个人空间 ID 等），不算项目级，故不含 vivo Docs 通用模式。
PROJECT_PATH_PATTERNS = [
    r"[A-Z]:\\[^|]*项目",          # 本地路径中含"项目"目录，如 D:\...\AI项目\...
    r"business_reports\.md",       # 工作区记忆文件名（个人化模式，其他用户可调整）
    r"project_rules\.md",          # 工作区记忆文件名（个人化模式，其他用户可调整）
]

def parse_markdown_entries(filepath: Path) -> list[dict]:
    """解析 Markdown 文件，提取列表条目（以 - 开头的行）。"""
    entries = []
    if not filepath.exists():
        return entries

    lines = filepath.read_text(encoding="utf-8").splitlines()
    current_section = ""
    in_frontmatter = False
    in_code_block = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # 跳过 frontmatter
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue

        # 跳过代码块
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # 检测标题
        if stripped.startswith("#"):
            current_section = stripped.lstrip("#").strip()
            continue

        # 检测列表项
        if stripped.startswith("- "):
            content = stripped[2:].strip()
            entries.append({
                "line": i,
                "section": current_section,
                "content": content,
                "content_normalized": normalize_text(content),
                "content_hash": hash_text(normalize_text(content)),
            })

    return entries


def normalize_text(text: str) -> str:
    """标准化文本用于去重比较：去首尾空格、合并连续空格、转小写。"""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text.lower()


def hash_text(text: str) -> str:
    """计算文本哈希用于精确去重。"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def extract_profile_summary_lines(filepath: Path) -> list[dict]:
    """提取 profile.md 中的画像条目。

    兼容两种结构：
    - 新版：身份块标记之后 + 可选"画像摘要"区
    - 实际结构：直接按 ## 分区（用户偏好/助手反馈/长期参考），全部条目都算画像内容
    身份块（local-agent-company-identity:start/end）区间内容跳过，视为系统维护。
    """
    if not filepath.exists():
        return []

    lines = filepath.read_text(encoding="utf-8").splitlines()

    summary_lines = []
    in_code_block = False
    in_identity_block = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # 身份块边界：整块跳过（系统维护，AI 不改）
        if "<!-- local-agent-company-identity:start" in stripped:
            in_identity_block = True
            continue
        if "<!-- local-agent-company-identity:end" in stripped:
            in_identity_block = False
            continue
        if in_identity_block:
            continue

        # 代码块跳过
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # 收集所有列表条目（profile.md 的条目即画像内容）
        if stripped.startswith("- "):
            summary_lines.append({
                "line": i,
                "content": stripped[2:].strip(),
                "content_normalized": normalize_text(stripped[2:]),
            })

    return summary_lines


def extract_raw_snapshots(filepath: Path) -> list[dict]:
    """提取 raw/memories.md 中的会话快照块（只统计元信息，不解析内部条目）。
    
    raw 不参与审计，只统计快照数量用于报告。不解析 entries 以避免 JSON 膨胀和 token 浪费。
    """
    if not filepath.exists():
        return []

    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()

    snapshots = []

    for i, line in enumerate(lines, 1):
        if "<!-- local-agent-auto-memory:start" in line:
            sid_match = re.search(r"sessionID=(\S+)", line)
            time_match = re.search(r"consolidatedAt=(\S+)", line)
            snapshots.append({
                "session_id": sid_match.group(1) if sid_match else "unknown",
                "consolidated_at": time_match.group(1) if time_match else "unknown",
                "start_line": i,
            })
        elif "<!-- trimmed:" in line:
            snapshots.append({
                "session_id": "trimmed",
                "start_line": i,
                "is_trimmed": True,
            })

    return snapshots


def check_duplicates(entries: list[dict]) -> list[dict]:
    """检测同一文件内的逐字重复条目。"""
    seen = {}
    duplicates = []
    for entry in entries:
        h = entry["content_hash"]
        if h in seen:
            duplicates.append({
                "type": "exact_duplicate",
                "first_line": seen[h]["line"],
                "first_content": seen[h]["content"],
                "dup_line": entry["line"],
                "dup_content": entry["content"],
            })
        else:
            seen[h] = entry
    return duplicates


def check_cross_file_mirrors(profile_summaries: list[dict], topics_entries: dict[str, list[dict]]) -> list[dict]:
    """检测 profile.md 与 topics 文件之间的镜像。"""
    mirrors = []
    all_topics = []
    for fname, entries in topics_entries.items():
        for e in entries:
            all_topics.append({"file": fname, **e})

    for ps in profile_summaries:
        ps_norm = ps["content_normalized"]
        for te in all_topics:
            if ps_norm == te["content_normalized"]:
                mirrors.append({
                    "type": "profile_topic_exact_mirror",
                    "profile_line": ps["line"],
                    "profile_content": ps["content"],
                    "topic_file": te["file"],
                    "topic_line": te["line"],
                    "topic_content": te["content"],
                })
            elif is_near_duplicate(ps_norm, te["content_normalized"]):
                mirrors.append({
                    "type": "profile_topic_near_duplicate",
                    "profile_line": ps["line"],
                    "profile_content": ps["content"],
                    "topic_file": te["file"],
                    "topic_line": te["line"],
                    "topic_content": te["content"],
                })
    return mirrors


def is_near_duplicate(text1: str, text2: str) -> bool:
    """简单近似重复判定：一方包含另一方且长度差异不太大。"""
    if not text1 or not text2:
        return False
    shorter = min(len(text1), len(text2))
    longer = max(len(text1), len(text2))
    if shorter < 10:
        return False
    if text1 in text2 or text2 in text1:
        return shorter / longer > 0.5
    return False


def check_project_level_info(entries: list[dict], filename: str) -> list[dict]:
    """检测项目级信息违规。"""
    violations = []
    for entry in entries:
        for pattern in PROJECT_PATH_PATTERNS:
            if re.search(pattern, entry["content"], re.IGNORECASE):
                violations.append({
                    "file": filename,
                    "line": entry["line"],
                    "content": entry["content"],
                    "matched_pattern": pattern,
                    "reason": "疑似项目级路径或文件名",
                })
                break
    return violations


def check_profile_constraints(profile_summaries: list[dict]) -> list[dict]:
    """检查 profile.md 画像摘要的量化约束。

    用户原则：不限定固定条数上限，但确实重要的内容才保留、尽量精炼篇幅、
    不变成流水账。因此：
    - 不再用固定条数硬上限，改为"条数偏多"的软提示（默认阈值 40 条，供 AI 判断精炼空间）
    - 单条过长仍提示（精炼篇幅的具体体现）
    """
    issues = []
    count = len(profile_summaries)
    # 软阈值：条数明显偏多时提示可精炼，而非硬性违规
    SOFT_MANY = 40
    if count > SOFT_MANY:
        issues.append({
            "type": "profile_summary_many",
            "severity": "soft",
            "current_count": count,
            "threshold": SOFT_MANY,
            "reason": f"画像共 {count} 条，偏多；请人工判断哪些是真正重要、可合并精炼的（不强制删除）",
        })
    for ps in profile_summaries:
        if len(ps["content"]) > 80:
            issues.append({
                "type": "profile_summary_line_too_long",
                "severity": "soft",
                "line": ps["line"],
                "content": ps["content"],
                "length": len(ps["content"]),
                "max": 80,
                "reason": f"第 {ps['line']} 行 {len(ps['content'])} 字符，偏长，可精炼",
            })
    return issues


def get_file_info(filepath: Path) -> dict:
    """获取文件基本信息。"""
    if not filepath.exists():
        return {"exists": False, "path": str(filepath)}
    stat = filepath.stat()
    return {
        "exists": True,
        "path": str(filepath),
        "size_bytes": stat.st_size,
        "line_count": len(filepath.read_text(encoding="utf-8").splitlines()),
        "last_modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
    }


def run_audit(memory_dir: Path) -> dict:
    """执行完整审计，返回结构化报告。"""

    # 文件路径
    memory_md = memory_dir / "MEMORY.md"
    profile_md = memory_dir / "profile.md"
    raw_dir = memory_dir / "raw"
    raw_memories = raw_dir / "memories.md"
    topics_dir = memory_dir / "topics"
    user_prefs = topics_dir / "user_preferences.md"
    assistant_fb = topics_dir / "assistant_feedback.md"
    references = topics_dir / "references.md"

    # 文件信息
    file_infos = {
        "MEMORY.md": get_file_info(memory_md),
        "profile.md": get_file_info(profile_md),
        "raw/memories.md": get_file_info(raw_memories),
        "topics/user_preferences.md": get_file_info(user_prefs),
        "topics/assistant_feedback.md": get_file_info(assistant_fb),
        "topics/references.md": get_file_info(references),
    }

    # 解析条目
    topics_entries = {}
    topics_entries["user_preferences.md"] = parse_markdown_entries(user_prefs)
    topics_entries["assistant_feedback.md"] = parse_markdown_entries(assistant_fb)
    topics_entries["references.md"] = parse_markdown_entries(references)

    profile_summaries = extract_profile_summary_lines(profile_md)
    raw_snapshots = extract_raw_snapshots(raw_memories)

    # 执行检查
    all_entries_combined = {}
    for fname, entries in topics_entries.items():
        all_entries_combined[fname] = entries

    # 1. 同文件内逐字重复
    file_duplicates = {}
    for fname, entries in topics_entries.items():
        dups = check_duplicates(entries)
        if dups:
            file_duplicates[fname] = dups

    # 2. profile 与 topics 的镜像
    cross_mirrors = check_cross_file_mirrors(profile_summaries, topics_entries)

    # 3. 项目级信息违规
    project_violations = []
    for fname, entries in topics_entries.items():
        project_violations.extend(check_project_level_info(entries, fname))

    # 4. profile 约束检查
    profile_issues = check_profile_constraints(profile_summaries)

    # 汇总统计
    summary = {
        "audit_time": datetime.now(timezone.utc).isoformat(),
        "memory_dir": str(memory_dir),
        "total_topic_entries": sum(len(e) for e in topics_entries.values()),
        "entries_per_file": {fname: len(entries) for fname, entries in topics_entries.items()},
        "profile_summary_count": len(profile_summaries),
        "raw_snapshot_count": len(raw_snapshots),
        "exact_duplicates_count": sum(len(d) for d in file_duplicates.values()),
        "cross_mirrors_count": len(cross_mirrors),
        "project_violations_count": len(project_violations),
        "profile_issues_count": len(profile_issues),
    }

    return {
        "summary": summary,
        "file_infos": file_infos,
        "topics_entries": {
            fname: [{"line": e["line"], "section": e["section"], "content": e["content"]} for e in entries]
            for fname, entries in topics_entries.items()
        },
        "profile_summaries": [{"line": ps["line"], "content": ps["content"]} for ps in profile_summaries],
        "raw_snapshots": [
            {
                "session_id": s.get("session_id", "unknown"),
                "consolidated_at": s.get("consolidated_at", "unknown"),
                "is_trimmed": s.get("is_trimmed", False),
            }
            for s in raw_snapshots
        ],
        "check_results": {
            "exact_duplicates": file_duplicates,
            "cross_file_mirrors": cross_mirrors,
            "project_level_violations": project_violations,
            "profile_constraint_issues": profile_issues,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="本地 Agent 长期记忆审计脚本")
    parser.add_argument("--memory-dir", type=str, default=str(DEFAULT_MEMORY_DIR),
                        help="记忆仓库目录路径")
    parser.add_argument("--output", type=str, default=None,
                        help="输出文件路径（省略时自动输出到记忆仓库下 audit-baseline.json，- 表示 stdout）")
    args = parser.parse_args()

    memory_dir = Path(args.memory_dir)
    if not memory_dir.exists():
        print(f"错误：记忆目录不存在: {memory_dir}", file=sys.stderr)
        sys.exit(1)

    report = run_audit(memory_dir)
    output_json = json.dumps(report, ensure_ascii=False, indent=2)

    if args.output is None:
        output_path = memory_dir / "audit-baseline.json"
        output_path.write_text(output_json, encoding="utf-8")
        print(f"审计报告已写入: {output_path}", file=sys.stderr)
    elif args.output == "-":
        print(output_json)
    else:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"审计报告已写入: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
