# Changelog

Newest first. Each entry records what changed, why, and how it was verified.

## 2026-11-12

### 更新：skillfactory 套件
- **来源**：用户提供 `skillfactory.zip`，SHA-256 `B5A9AAE23EC50851533ED8B07F695D02925E51AAC47CF0C18E524051B4308F2F`；ZIP 30 个文件，路径与原 suite 完全一致，无新增或删除路径。
- **版本变化**：`skill-orchestrator` 1.8.2→1.9.0；`skill-creator` 1.1.1→1.2.0；套件内 `skill-effectiveness-evaluator` 0903V3→0903V4；其余成员版本字段不变，但文件与 ZIP 同步。ZIP 未声明 Suite 整体版本。
- **管理变更**：替换 `suites/skillfactory/` 的 30 个文件；更新根 README、SKILLS 索引中的成员版本及 evaluator 版本注记；更新 skillfactory 许可证说明；保留 `skill-creator/LICENSE.txt` 原文。
- **边界**：仅更新 Suite 内副本；独立目录 `skills/skill-effectiveness-evaluator/` 的 0903V2 未改动。
- **安全检查**：检查文件清单、机器绝对路径、邮箱、token/私钥模式；未发现敏感命中。Apache-2.0 许可文件 SHA-256 与原快照一致。
- **验证**：Suite 基线脚本确认两个核心门禁和三个专项 Skill 可读且含调度接口；6 个成员结构校验通过（两项仅提示无资源引用）；ZIP 30 个文件与暂存快照 SHA-256 一致；链接检查无断链。推送后的远端树待核验。

## 2026-11-11

### 更新：graphic-report 视觉流程与构图指南
- **来源**：作者本地 `graphic-report` Git 仓库当前 `master` 最新提交 `02a7188`（截至本次同步）。Skill 本身无版本字段，索引仍记 `-`。
- **变更**：同步 52 个 Git 已跟踪源文件到 `skills/graphic-report/`（上次快照 49 个文件）。新增基础中文主题、构图/好图指南、桌面专用视觉检查脚本和基础 HTML 模板；更新 Skill 工作流、截图脚本、主题、语汇与两个示例。
- **行为影响**：独立报告改为基础主题 + 按需 recap 层；默认视觉检查只验收桌面 1280px，不再检查 390px 手机视口；首轮查看多页联系表，后续按改动范围复查，增加 `--figure`/`--selector` 局部截图；将每图 `<figure>`、场景/几何推导和换词测试写入流程。
- **依赖变化**：Playwright Core 不随 Git 快照分发，需本地另行安装；Node.js 20+、Chrome/Edge 为检查环境依赖。
- **许可证**：`scripts/desktop-look.mjs` 基于 MIT 许可的 visual-explainer `engine/kit/look.mjs` 改编；第三方上游 `engine/` 未修改。已在 `NOTICE.md` 与 `LICENSES/graphic-report.md` 登记，保留 `engine/LICENSE`。
- **隐私/历史**：仅复制本地子仓库已跟踪文件，不导入本地提交历史、邮箱、上层工作区转录稿、试验文件或记忆；用户此前已明确接受第六场案例随 Skill 公开。
- **验证**：52 个本地 Git 跟踪源文件与快照逐文件 Git blob 比对一致（另有 README/NOTICE/许可证维护说明）；20 个 JS/MJS 文件通过 `node --check`；新桌面检查器在 1280px 上检查 `vocab-showcase.html` 无错误；两个示例均重新构建并报告桌面视觉检查无问题；敏感模式扫描未发现凭据、邮箱或绝对用户路径。联系表文件已生成，未逐张作人工外观验收；推送后的远端树待核验。

## 2026-11-11

### 升级：graphic-report 1.0.0 → 1.0.1
- **来源**：本地开发仓库正式 Git 标签 `v1.0.1`，发布提交 `6a5509d34f226d4b0fbcddfe57ab2025c9f14a74`；其后仅有记录该提交哈希的文档提交 `9cd6797`。同步依据为 tagged 1.0.1 的 53 个已跟踪文件。
- **变更**：阅读列改为 40rem 居中，标题、正文与判断条共用阅读列；图、表及卡片保持通栏；修复 recap 模块内部布局被全局居中规则影响的问题。更新 `SKILL.md` version 到 1.0.1；同步 Skill README、仓库 README 和 SKILLS 索引版本。
- **版本行为**：1.0.1 属 PATCH 修复。保留本地 CHANGELOG 中既有验证声明，不额外扩展声称此次重复了 1280/1440 所有路径测试。
- **许可证与范围**：仅同步 `graphic-report` 子仓库已跟踪文件，不导入本地 Git 历史、备份目录或父级工作区材料；保持 Skill 本身未声明开源许可证和第三方许可证记录。
- **验证**：待完成 tagged 文件逐 blob 校验、敏感信息/链接检查和远端树核验。

## 2026-11-12

### 更新：skillfactory 套件
- **来源**：用户提供的 `skillfactory.zip`（SHA-256 `7D8E...`），包含 6 个成员、30 个文件；ZIP 内文件路径与现有 Suite 完全一致，无新增/删除路径。
- **版本变化**：`skill-orchestrator` 1.8.2→1.9.0；`skill-creator` 1.1.1→1.2.0；套件内 `skill-effectiveness-evaluator` 0903V3→0903V4；其余成员保持自身版本声明。
- **变更**：以 ZIP 内容更新 `suites/skillfactory/`；更新根 `README.md`、`SKILLS.md` 的套件版本及 evaluator 版本备注；保留 `skill-creator/LICENSE.txt` 原文件。
- **边界**：仅更新 suite 副本；`skills/skill-effectiveness-evaluator/` 独立版 0903V2 不变，不与 Suite 副本合并。
- **隐私与范围**：上传前检查包内文件路径、凭据/邮箱/绝对路径模式；未见敏感命中。无提交本地开发目录、工作区材料或 ZIP 外文件。
- **验证**：待完成 ZIP 解包副本与 GitHub 快照逐文件 SHA-256 比对、结构/链接检查及远端树核验。

## 2026-11-12

### 更新：skillfactory 套件
- **来源**：用户提供 `skillfactory.zip`，SHA-256 `B5A9AAE23EC50851533ED8B07F695D02925E51AAC47CF0C18E524051B4308F2F`；ZIP 30 个文件，路径与原 suite 完全一致，无新增或删除文件。
- **版本变化**：`skill-orchestrator` 1.8.2→1.9.0；`skill-creator` 1.1.1→1.2.0；套件内 `skill-effectiveness-evaluator` 0903V3→0903V4；`writing-for-agents` 1.1.0、`skill-from-externals` 1.0.0、`skill-from-masters` 1.1.1 版本号不变，但包内文件与 ZIP 内容同步。ZIP 未声明 Suite 整体版本。
- **管理变更**：替换 `suites/skillfactory/` 的 30 个文件；README/SKILLS 索引记录成员版本与无 suite-level version；更新 skillfactory 许可证说明；保留 `skill-creator/LICENSE.txt` 原文及 SHA-256。
- **边界**：独立目录 `skills/skill-effectiveness-evaluator/` 的 0903V2 不改动；仅 Suite 内副本升至 0903V4。
- **安全检查**：检查文件清单、权限相关字符串、绝对用户路径、个人邮箱、token/私钥模式；未发现敏感命中。许可证文件与原快照 SHA 一致。
- **验证**：待完成 ZIP/临时快照对比、结构脚本验证、管理文档链接检查、远端逐文件核验。

## 2026-11-10

### 新增：graphic-report 原创 Skill
- **来源**：作者原创项目，快照复制自本地开发仓库 `graphic-report/`；纳入其 Git 已跟踪的 48 个源文件，并新增项目说明，不导入原仓库提交历史。
- **内容**：图解报告 Skill、中文主题与图形语汇、visual-explainer 渲染内核、构建/截图脚本、通用展示页，以及用户明确确认公开的第六场访谈案例。
- **排除**：上层工作区的访谈转录稿、试验目录、`.aime` 记忆和其他工作区材料；`engine/node_modules` 依忽略规则未纳入。
- **许可**：Skill 本身没有正式开源许可证；不把第三方引擎的 MIT 许可误作整套 Skill 的授权。单独登记 visual-explainer（MIT）、PELE（MIT）及 Lucide 图标（ISC），保留上游许可文本。
- **研究案例**：案例是访谈内容整理页而非原始逐字稿；按作者明确要求随公开仓库收录。收录不等于授权对研究内容进行其他用途的再利用。
- **提交历史**：以快照加入，不导入原开发仓库的提交历史及其提交者元数据。
- **验证**：源仓库 48 个已跟踪文件与快照逐一 Git blob SHA-1 一致；扫描未发现凭据、本机绝对路径或转录稿副本；文档相对链接检查无断链。推送后核验 152 个远端 Git blob 与本地一致（0 差异），Skill 入口和索引 raw 链接返回 HTTP 200。

## 2026-11-05

### 升级：user-interview-transcript-calibrator 2.5.2 → 2.6.0
- **来源**：用户提供的 `user-interview-transcript-calibrator_v2.6.0.zip`（文件时间 2026-11-05，包内仅 `SKILL.md` 一个文件，`Skill 版本：v2.6.0`）。
- **变更**：`SKILL.md` 整体替换为 2.6.0；`README.md` 按 2.6.0 重写，补充 2.6.0 主要变化、三份默认产物与交付门禁说明。
- **2.6.0 要点**：新增定位锚点（时间戳或 `[段N]`）；新增身份置信度与显示形式降级顺序；参与者观察改为五维度逐项结项（已提炼／有依据缺省）；新增交付校验与门禁表 V01–V13 及 V07 计数断言；明确正式笔录与内部复盘的内容边界。
- **验证**：上传后从仓库取回 `SKILL.md` 与本地包逐字节比对一致（SHA-256 `4B70C8DA52093A5F0A5346B4E5376063BB8F516C38B4FA541456C1C8EC2482EA`）。
- **索引**：根 `README.md`、`SKILLS.md` 版本号同步为 2.6.0。
- **依赖旧版行为的使用者需注意**：观察维度由原表格口径改为五维度逐项结项，且未通过门禁断言时不得标记为正式笔录。
## 2026-11-02

### 维护决策确认
- `skill-effectiveness-evaluator` 的套件内 0903V3 是为 orchestrator 调用做的小幅适配；独立目录 0903V2 保持原样，两者独立维护，不自动合并或升级。
- 用户笔录校准可公开收录；真实访谈材料不得上传公开仓库。
- 暂不增加 MIT 等新许可证；维持现有逐技能许可证说明。

### 修正：rigor-mode 同步为最新发布版 2.2.0
- **原因**：2026-09-14 的同步误用了探索区的旧包（`严谨模式-v3-skill.zip`，文件时间 2026-07-31，内部名 `rigor-mode`），不是最新发布版。
- **依据**：SkillsHub `sug-ur-skills/rigor-mode-v2` 当前版本 2.2.0（2026-09-14 11:16 发布）；本机已安装版本与其逐文件哈希一致。
- **变更**：`SKILL.md`、`references/principles.md` 更新为 2.2.0；`references/frameworks.md`、`references/review-prompt.md` 原已一致；`README.md` 按 2.2.0 的七阶段结构重写。
- **验证**：上传后 5 个文件逐一与 2.2.0 发布包比对一致。
- **影响**：流程由旧版四阶段改为七阶段（含基础核验与可选加强核验）。依赖旧版行为的使用者需注意。

### 新增：suites/skillfactory
- 六技能联动的 Skill 生产工具，以 `skill-orchestrator` 为唯一入口，共 30 个文件。
- 成员：skill-orchestrator、skill-creator（Apache-2.0）、skill-effectiveness-evaluator（0903V3）、writing-for-agents、skill-from-externals、skill-from-masters。
- 与 `skills/skill-effectiveness-evaluator`（0903V2）独立维护；0903V3 是为套件编排调用做的小幅适配，0903V2 保留作单独使用版本。此为用户确认的设计决策，差异见 `SKILLS.md`。
- 上传前做了敏感信息扫描：仅 `skill-creator/SKILL.md` 一处出现应用数据目录的通用路径说明，不含个人信息或凭据。

### 整理：仓库管理
- 修复 `README.md`、`SKILLS.md` 中混入的字面量换行符，导致表格错乱。
- 修正 `windows-pc-care` raw 链接中的域名拼写错误。
- 将 `user-interview-transcript-calibrator` 补入索引。
- 新增 `suites/` 层级、版本字段、`CHANGELOG.md`；`CONTRIBUTING.md` 增加套件、版本核对与提交规范。
- 补充 `LICENSES/` 中新增条目；为缺少说明的 Skill 补 `README.md`。

## 此前（依据提交历史整理）

- 2026-09-18：新增 `user-interview-transcript-calibrator` v2.5.2。
- 2026-09-14：同步 `rigor-mode`（版本有误，已于 2026-11-02 修正）。
- 2026-09-03：`skill-effectiveness-evaluator` 更新为 0903V2。
- 2026-08-11：新增 `local-agent-memory-governor`、`sandbox-isolation`。
- 2026-08-07：迁入 `rigor-mode`、`desktop-savior`、`windows-pc-care`，建立仓库结构。
