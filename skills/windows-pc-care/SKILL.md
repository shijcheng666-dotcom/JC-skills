---
name: windows-pc-care
description: "This skill should be used when a user wants to assess, organize, free space on, or improve the responsiveness of a Windows 10/11 PC. It provides a safety-first workflow for slow computers, full system drives, excess startup items, software audits, storage organization, performance bottlenecks, and upgrade decisions. It diagnoses before changing anything, never automatically touches personal files, and requires explicit approval for every change."
agent_created: true
---

# Windows 电脑整理与提速（安全通用版）

## 目标与适用范围

处理 Windows 10/11 电脑变慢、C 盘空间紧张、启动项过多、软件冗余、后台占用异常，以及是否需要加内存或换 SSD 等问题。优先恢复系统可用性、保留用户数据和同步能力；不以“提速”为理由关闭安全更新、移除浏览器、卸载同步工具或删除个人文件。

使用简体中文沟通。将所有建议说明成“发现、影响、建议、风险、是否需要确认”五项。遇到 BitLocker、企业设备、来宾账户、未知磁盘健康状态或疑似中毒时，停止自动变更并转为人工处理建议。

## 不可突破的安全边界

1. **先诊断，后计划，再执行，最后复检。** 不跳过诊断或确认步骤。
2. **个人文件只读。** 桌面、下载、文档、图片、视频、音乐、用户目录、网盘/微信/浏览器资料与外接盘仅可统计、列清单、提出迁移或归档建议；绝不自动移动、重命名、删除或清空回收站。
3. **逐项授权。** 每个卸载、开机启动项变更、服务/计划任务变更、注册表变更、系统设置变更都必须列出名称、路径/键值、预期收益和回退方式，取得明确确认后才执行。
4. **不默认移除系统功能。** 不默认卸载 Edge、OneDrive、Defender、Windows Update、Microsoft Store、驱动程序、UWP 应用或厂商恢复工具；只有用户明确说明不用，且确认影响后，才给出官方卸载或设置路径。
5. **不执行危险捷径。** 不使用 `ExecutionPolicy Bypass`、不关闭 Defender/更新、不删除 Prefetch、WinSxS、System32、pagefile、hiberfil 或 Program Files 中的文件；不以 `rm -rf`、通配符或静默卸载批量处理未知对象。
6. **可恢复优先。** 修改前优先建议创建 Windows 还原点，并记录变更前状态。对可卸载软件优先走“设置 > 应用 > 已安装的应用”或厂商卸载器；不直接删除安装目录来代替卸载。
7. **小批量验证。** 涉及清理或配置的工作每批最多 10 个明确对象，完成后立即复检；任一失败或异常立即停止并报告。

详见 `references/safety-and-decision-matrix.md`。

## 工作流

### 0. 建立边界与目标

先确认：设备是否为个人设备、Windows 版本、主要症状、可接受的停机时间、是否正在使用 OneDrive/其他同步盘、是否有 BitLocker/企业管理、是否愿意重启。

把目标分成以下一个或多个类别：
- 空间：释放系统盘空间，识别大文件和可安全清理的缓存。
- 速度：定位启动慢、卡顿、内存紧张、磁盘忙或后台占用。
- 软件：识别重复、过期、不再使用或可能捆绑的软件。
- 整理：为个人文件建立迁移/归档建议，等待用户点名具体文件后才行动。
- 升级：评估 RAM、SSD、电池或整机更换的性价比。

### 1. 只读体检

运行 `scripts/collect-diagnostics.ps1`，该脚本不会写入配置、不会删除文件、不会读取文件内容。将输出保存为 JSON，基线命名为 `pc-care-baseline-YYYYMMDD.json`。

覆盖：系统/硬件、内存、磁盘空间与文件系统、启动应用、已安装软件、前台内存进程、系统盘可清理目录的体积、Windows 安全状态、Windows 更新最近安装时间、休眠/还原/BitLocker 状态（可用时）。

若用户只关心某一个问题，可缩小诊断范围；但在建议卸载或清理前，至少取得磁盘空间、启动项、已安装软件和安全状态。

### 2. 形成分级计划

将发现按以下层级输出，禁止把“可能不用”表述成“应该删除”：

| 级别 | 含义 | 处理方式 |
|---|---|---|
| A：只读结论 | 例如内存持续紧张、C 盘低于 15% 可用空间、启动项数量偏多 | 可直接说明与建议 |
| B：低风险维护 | 用户临时目录、系统临时目录中的可删除缓存 | 先预演，再逐项确认 |
| C：用户选择 | 不常用软件、浏览器扩展、启动项、云盘功能、可选应用 | 提供用途与影响，逐项确认 |
| D：高影响变更 | 驱动/固件、服务、计划任务、注册表、分区、BitLocker、重装系统 | 只提供审慎方案，建议备份或专业人员介入 |

每项行动必须包含：对象、证据、预期收益、风险、执行方式、回退方式和确认状态。

### 3. 保护与确认

在任何 B/C/D 类变更前执行：

1. 请用户确认重要文件已同步或备份；如涉及系统设置或卸载，建议通过“控制面板 > 系统 > 系统保护”创建还原点。
2. 导出并展示“本轮变更清单”，不得混入未确认项目。
3. 对清理操作先运行 `scripts/safe-cache-cleanup.ps1` 的预演模式；清晰展示候选目录、文件数量、大小、跳过项和风险说明。
4. 取得一句包含对象范围的明确授权，例如“只清理用户临时目录和 Windows 临时目录，不卸载任何软件”。

### 4. 执行模块

#### 4A. 缓存与系统空间维护

仅使用 `scripts/safe-cache-cleanup.ps1`，默认只预演。仅在用户授权后使用 `-Apply`，并只启用经确认的目标：
- `UserTemp`：当前用户临时目录；跳过正被锁定的文件。
- `WindowsTemp`：系统临时目录；通常需要管理员权限，失败即跳过。

不清理 Prefetch、回收站、浏览器配置文件、下载目录、Windows Update 缓存、OneDrive 目录或任何个人数据。对浏览器缓存、Windows Storage Sense、组件存储清理等，优先引导用户在 Windows 设置中手动确认。

#### 4B. 启动与后台治理

只建议禁用明确可识别、非安全、非驱动、非同步关键功能且用户确认不需要的启动项。优先通过“任务管理器 > 启动应用”关闭，保留截图/名称记录；不删除 Run 键，不禁用未知服务。

对于高内存进程，先查明所属应用、是否正在同步/下载/更新、是否可关闭；只结束用户明确确认的普通应用进程。出现 Defender、系统进程、驱动服务、未知签名进程或疑似恶意进程时，建议执行 Defender 全盘扫描或寻求专业支持。

#### 4C. 软件与扩展治理

列出安装时间、发布者、版本、用途和启动项关联。将“重复功能、试用软件、过期组件、用户确认不用的软件”列为候选，逐项经用户确认后通过 Windows 设置或厂商卸载器卸载。不要静默卸载、不要直接删除程序目录、不要把国产软件或预装软件按名称一概视为垃圾。

浏览器扩展仅列出数量和名称；由用户在扩展管理页自行删除。不要读取账号、Cookie、历史记录、密码或同步数据。

#### 4D. 个人数据整理

只输出按路径、大小、修改日期和文件类型的候选报告。先询问用户保留/归档/删除规则；对于任何移动、改名或删除，遵循“备份成功 → 列出完整路径 → 明确确认 → 每批不超过 10 个 → 使用回收站 → 验证”的顺序。

#### 4E. 硬件升级建议

只有证据支持时才建议升级：
- 空闲内存长期低、频繁分页且 CPU/磁盘不是首要瓶颈：建议核对 RAM 规格、插槽与最大容量。
- 系统运行机械硬盘、磁盘响应高且 SMART/健康状态可疑：建议评估 SSD 迁移或更换。
- CPU 平台过旧、内存和存储升级成本接近二手/新机价值：明确说明整机替换可能更划算。

不凭单次瞬时使用率下结论；要求在用户典型工作负载下复测。

### 5. 复检与交付

变更后再次运行 `scripts/collect-diagnostics.ps1`，同基线对比：系统盘可用空间、启动项数量、可见进程、内存可用量、安全状态和已安装软件数量。输出：
- 已完成与实际收益；
- 跳过/失败项及原因；
- 需用户手动完成的步骤；
- 可回退操作与还原路径；
- 后续维护建议（每月检查存储、每季度审计启动项/软件）。

## 脚本用法

```powershell
# 只读基线采集
powershell -NoProfile -File .\\scripts\\collect-diagnostics.ps1 -OutputPath .\\pc-care-baseline.json

# 只查看可清理缓存，不做改动
powershell -NoProfile -File .\\scripts\\safe-cache-cleanup.ps1

# 仅在已展示预演、用户明确确认后执行指定目标
powershell -NoProfile -File .\\scripts\\safe-cache-cleanup.ps1 -Targets UserTemp,WindowsTemp -Apply
```

不要以管理员权限运行诊断脚本；只在 `WindowsTemp` 已获授权且确有需要时以管理员权限运行清理脚本。脚本使用 ASCII 内容以降低中文 Windows PowerShell 编码兼容问题，但面向用户的解释使用中文。

## 资源

- `scripts/collect-diagnostics.ps1`：只读体检，输出结构化 JSON。
- `scripts/safe-cache-cleanup.ps1`：默认预演、显式 `-Apply` 才可执行的临时缓存清理工具。
- `references/safety-and-decision-matrix.md`：风险边界、判断规则、报告模板、常见症状决策表。
