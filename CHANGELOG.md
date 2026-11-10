# Changelog

Newest first. Each entry records what changed, why, and how it was verified.

## 2026-11-10

### 新增：graphic-report 原创 Skill
- **来源**：作者原创项目，快照复制自本地开发仓库 `graphic-report/`；纳入其 Git 已跟踪的 48 个源文件，并新增项目说明，不导入原仓库提交历史。
- **内容**：图解报告 Skill、中文主题与图形语汇、visual-explainer 渲染内核、构建/截图脚本、通用展示页，以及用户明确确认公开的第六场访谈案例。
- **排除**：上层工作区的访谈转录稿、试验目录、`.aime` 记忆和其他工作区材料；`engine/node_modules` 依忽略规则未纳入。
- **许可**：Skill 本身没有正式开源许可证；不把第三方引擎的 MIT 许可误作整套 Skill 的授权。单独登记 visual-explainer（MIT）、PELE（MIT）及 Lucide 图标（ISC），保留上游许可文本。
- **研究案例**：案例是访谈内容整理页而非原始逐字稿；按作者明确要求随公开仓库收录。收录不等于授权对研究内容进行其他用途的再利用。
- **提交历史**：以快照加入，不导入原开发仓库的提交历史及其提交者元数据。
- **验证**：源仓库 48 个已跟踪文件与快照逐一 Git blob SHA-1 一致；扫描未发现凭据、本机绝对路径或转录稿副本；文档相对链接检查无断链。推送后再核验远端文件。

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
