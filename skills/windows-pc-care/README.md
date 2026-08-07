# Windows 轻净计划

**安全优先的 Windows 10/11 电脑整理与提速方案**

[English README](./README.en.md)

---

## 这是什么

一套**安全优先**的 Windows PC 诊断、清理与性能优化工作流。不同于市面上那些"一键加速"的野路子工具，这个项目遵循：

- **先诊断，后计划，再执行，最后复检**
- **个人文件只读** — 绝不自动动你的桌面、下载、文档
- **逐项授权** — 每个变更都先问你再动手
- **不牺牲安全** — 不禁用 Defender、Windows Update、不卸载 Edge/OneDrive
- **可回滚** — 每个操作都记录变更前状态

## 适合谁用

- 家里/办公室的 Windows 电脑变慢了，想系统地清理一遍
- C 盘快满了，但不知道哪些能删哪些不能删
- 开机启动了一堆东西，想理一理哪些该留哪些该关
- 想评估一下要不要加内存、换 SSD，还是干脆换新电脑
- **不**适合：想一键自动清理、不想看每一步确认的人

## 使用方法

### 方式一：作为 AI Skill 导入

将本仓库导入 WorkBuddy / Claude 等 AI 工具作为 Skill 使用，AI 会自动按流程引导你完成诊断→计划→执行→复检。

### 方式二：手动运行脚本

```powershell
# 1. 采集基线（只读，不修改任何东西）
powershell -NoProfile -File scripts\\collect-diagnostics.ps1

# 2. 预览可清理的临时文件（只统计，不删除）
powershell -NoProfile -File scripts\\safe-cache-cleanup.ps1

# 3. 清理指定缓存（需要你确认后加上 -Apply）
powershell -NoProfile -File scripts\\safe-cache-cleanup.ps1 -Targets UserTemp,WindowsTemp -Apply
```

> ⚠️ 所有脚本均设计为**默认无害**：诊断脚本只读输出 JSON；清理脚本默认只预览，加 `-Apply` 才真正执行。

## 项目结构

```
windows-pc-care/
├── SKILL.md                         # AI Skill 核心指引
├── README.md                        # 本文件（中文）
├── README.en.md                     # 英文说明
├── scripts/
│   ├── collect-diagnostics.ps1      # 只读体检 → 输出 JSON 基线
│   └── safe-cache-cleanup.ps1      # 安全缓存清理（默认预览模式）
└── references/
    └── safety-and-decision-matrix.md # 风险分层、回退规则、报告模板
```

## 安全原则

| 准则 | 说明 |
|---|---|
| 只读诊断 | 不修改配置、不删除文件、不读取个人文件内容 |
| 缓存清理需显式确认 | 默认仅预览，`-Apply` 才执行 |
| 不碰系统关键文件 | Prefetch、WinSxS、System32、pagefile 等绝对不动 |
| 逐项授权 | 卸载软件、关闭启动项、改系统设置都先列出清单 |
| 保护个人数据 | 桌面/下载/文档等目录仅统计大小，不自动操作 |
| 可回退 | 每个变更都记录原始状态，支持还原点 |

## 许可证

MIT

## JC-skills

This skill is maintained in the unified [JC-skills](https://github.com/shijcheng666-dotcom/JC-skills) collection. Browse the complete package at [skills/windows-pc-care](../../skills/windows-pc-care/).
