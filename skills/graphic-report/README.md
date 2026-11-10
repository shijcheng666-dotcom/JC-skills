# 图解报告（graphic-report）

按内容关系设计图形，把访谈、讨论纪要、报告草稿或 Markdown 整理成单文件 HTML 图解报告；也可为已有 HTML 页面生成局部图形片段。

## 使用场景

适用于“把这份材料做成图解”“可视化讨论结论”“把这一段画成图并嵌入现有页面”等请求。重点是先识别内容中的比较、变化、因果、层级、路径和状态关系，再选择、组合或自行设计适合的视觉表达，而非套固定图表模板。

## 文件结构

```text
graphic-report/
├── SKILL.md
├── assets/       # 中文主题与图形语汇样式
├── engine/       # visual-explainer 渲染内核（保留上游许可）
├── examples/     # 通用展示页与第六场案例
├── references/  # 图形语汇与选型说明
└── scripts/      # 构建、适配、截图与曲线工具
```

## 基本使用

1. 阅读 `SKILL.md`，按材料和交付模式选择独立报告或嵌入模式。
2. 使用 `.src.html` 编写源页面；独立报告通过 `node scripts/build.mjs <name>.src.html` 构建。
3. 如需整页截图，运行 `node scripts/shoot.mjs <page.html> <output-dir> 1400`。
4. 构建成功后仍需检查整页视觉效果，并核对内容忠实度。

运行需要 Node.js 20+。渲染和截图会调用随包 `engine/`，截图还依赖 Playwright 与本机 Chrome 或 Edge。

## 示例说明

- `examples/vocab-showcase.src.html`：展示图形语汇的通用示例。
- `examples/case-interview-recap.src.html` 与 `examples/case-interview-recap.html`：基于一场具体用户访谈整理的第六场案例。该案例不是原始逐字稿；其中包含受访者行为、偏好和产品讨论摘要。维护者已明确确认将其随本 Skill 一同公开，使用或再分发时仍应尊重原有语境与用途。

## 来源与许可

本 Skill 的规则、主题、图形语汇与工具由作者原创；当前没有为 Skill 整体声明正式开源许可证。**公开收录不等于授予他人修改或再分发 Skill 本身的许可**。许可状态见 [`LICENSES/graphic-report.md`](../../LICENSES/graphic-report.md)。

渲染内核来自 visual-explainer，采用 MIT 许可，原许可文本保留在 `engine/LICENSE`。`engine/kit/vendor/pele.mjs` 及其依赖的图标许可说明保留在 `engine/kit/vendor/PELE-LICENSE`。不得将这些第三方组件的许可证误读为整个 Skill 的许可证。

该 Skill 依赖的项目文件均保留在目录中；更新或分发时请一并保留对应第三方许可与来源说明。
