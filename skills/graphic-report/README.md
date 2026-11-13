# 图解报告（graphic-report）

**版本：1.1.0**（源版本与 Git 标签以本地开发仓库 `CHANGELOG.md`、`v1.1.0` 为准）

按内容关系设计图形，把访谈、讨论纪要、报告草稿或 Markdown 整理成单文件 HTML 图解报告；也可为已有 HTML 页面生成局部图形片段。

1.1.0 起，Skill 不预设背景、配色、形状、材质、插画或动效等视觉形式偏好：用户给出风格、参考模板或品牌规范时遵循，嵌入模式服从宿主；未指定时按内容主题、读者与使用场景自主设计。基础主题只作渲染兜底，引擎的风格建议不替代本次设计选择。

## 使用场景

适用于“把这份材料做成图解”“可视化讨论结论”“把这一段画成图并嵌入现有页面”等请求。重点是先识别内容中的比较、变化、因果、层级、路径和状态关系，再选择、组合或自行设计适合的视觉表达，而非套固定图表模板。

## 文件结构

```text
graphic-report/
├── SKILL.md
├── assets/       # 基础主题、复盘主题与图形语汇样式
├── engine/       # visual-explainer 渲染内核（保留上游许可）
├── examples/     # 通用展示页与第六场案例
├── references/   # 视觉推导与图形语汇说明
├── scripts/      # 构建、桌面检查、截图与曲线工具
└── templates/    # HTML 起始模板
```

## 基本使用

1. 阅读 `SKILL.md`，按材料和交付模式选择独立报告或嵌入模式。
2. 使用 `.src.html` 编写源页面；独立报告通过 `node scripts/build.mjs <name>.src.html` 构建。
3. 默认验收桌面 1280px 视口。首次查看 `.sheet.png` / `.sheet-2.png` 联系表；局部重查可用 `node scripts/shoot.mjs <page.html> <output-dir> 1400 --figure=N`，或 `--selector="CSS选择器"`（须唯一命中）。
4. 构建成功后仍需检查图形主次、内容关系和事实忠实度；视觉检查的 `⚠` 是复查线索，`✗` 才是阻塞项。

运行需要 Node.js 20+ 和本机 Chrome 或 Edge。渲染使用随包 `engine/`；浏览器视觉检查依赖 Playwright Core，但 `node_modules` 不纳入仓库，需在本地安装：`npm install --no-save --prefix engine playwright-core`。未安装时仍可构建，但浏览器检查会跳过并提示。独立报告可从 `templates/base.src.html` 起步；视觉构思方法见 `references/design.md`。

## 示例说明

- `examples/vocab-showcase.src.html`：展示图形语汇的通用示例。
- `examples/case-interview-recap.src.html` 与 `examples/case-interview-recap.html`：基于一场具体用户访谈整理的第六场案例。该案例不是原始逐字稿；其中包含受访者行为、偏好和产品讨论摘要。维护者已明确确认将其随本 Skill 一同公开，使用或再分发时仍应尊重原有语境与用途。

## 来源与许可

本 Skill 的规则、主题、图形语汇与原创工具由作者完成；当前没有为 Skill 整体声明正式开源许可证。**公开收录不等于授予他人修改或再分发 Skill 本身的许可**。许可状态见 [`LICENSES/graphic-report.md`](../../LICENSES/graphic-report.md)。

`engine/` 渲染内核和 `scripts/desktop-look.mjs` 桌面检查器包含 visual-explainer 上游代码；检查器为本地改编版本，MIT 许可原文保留在 `engine/LICENSE`。`engine/kit/vendor/pele.mjs` 及其依赖图标许可说明保留在 `engine/kit/vendor/PELE-LICENSE`。不得将第三方组件许可证误读为整个 Skill 的许可证。

Playwright Core 不随仓库快照分发，运行视觉检查前需本地安装，Apache-2.0 许可随该依赖包提供。更新或再分发时请保留目录内的上游来源和许可说明。
