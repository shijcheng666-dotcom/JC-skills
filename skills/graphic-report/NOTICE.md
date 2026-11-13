# 第三方组件与来源

## engine/（渲染内核）
- 项目：visual-explainer，作者 nicobailon，MIT 许可
- 仓库：https://github.com/nicobailon/visual-explainer
- 版本：v0.15.0（提交 9d5f880b，2026-11-04）
- 用途：把页面源文件（`.src.html`）渲染为自包含 HTML，并提供浏览器视觉检查（`kit/render.mjs`、`kit/look.mjs`）。
- 本包仅保留 `kit/`、`plan/`、`references/` 目录，**未修改任何源文件**。完整许可见 `engine/LICENSE`；上游 SKILL.md 存为 `engine/UPSTREAM-SKILL.md.txt` 以备参考。
- `playwright-core`（Apache-2.0）用于控制本机浏览器做视觉检查与截图；主分发包和工作区内置于 `engine/node_modules`，精简上传包不携带，按需执行 `npm install --no-save --prefix engine playwright-core` 补齐。
- 安全审查（2026-11-09）：渲染脚本无 `fetch`/HTTP 请求；仅 `render.mjs` 会向页面写入 Google Fonts 外链（本包通过 `zh-adapt.mjs` 移除）；`child_process` 仅用于打开文件与运行 `<ve-flow model>`（本包不使用该功能）。

## 图形语汇（assets/vocab.css、references/vocabulary.md）
- 设计参考：微信输入法"AI 录音笔"公开分享页中的 54 个图（用户提供的 9 份），**仅学习其图的结构与表达方式并自行重新实现，未复制其文字内容或代码**。
- 语汇库为本技能原创的整理与实现。
- 扩展方法参考：Mermaid、Vega-Lite、Apache ECharts、FT Visual Vocabulary，以及 NN/g 关于用户旅程和服务蓝图的公开资料。仅借鉴图形关系与组合思想，未引入其运行时依赖或复制其页面代码。

## 领域复合组件（assets/set-cover.js）
- 双分母集合覆盖图为本技能根据用户手绘结构独立实现的原生 JS/SVG 组件，无外部图表库依赖。
- 组件仅提供数据驱动渲染；调用方负责提供真实集合、交集和盲区数据。演示数据仅用于版式验证。

## 升级引擎
1. 在工作区另建目录克隆新版 visual-explainer；
2. 对比 `kit/render.mjs` 是否仍含 Google Fonts 外链及 `child_process` 的使用范围；
3. 覆盖 `engine/kit`、`engine/plan`、`engine/references`；
4. 重跑 `examples/vocab-showcase.src.html` 的构建与目检，确认无回退。
