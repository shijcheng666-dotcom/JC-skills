# graphic-report license status

## Skill 本身

- 作者：Jay Chen（施景程）
- 来源：作者原创工作，开发源位于本地 `graphic-report` 项目仓库。
- 状态：公开收录，但**未声明正式开源许可证**。公开可见不等于已授权第三方修改、复制、改编或再分发 Skill 本身；需联系作者取得许可。
- 本目录不附加或推断 MIT、Apache-2.0 等许可证。

## 随包第三方组件

| 路径 | 组件 / 版权方 | 许可证 | 说明 |
|---|---|---|---|
| `engine/` 与改编的 `scripts/desktop-look.mjs` | visual-explainer / Copyright (c) 2025 Nico Bailon | MIT | 渲染内核在 `engine/`；桌面视觉检查器基于上游 `engine/kit/look.mjs` 改编，保留上游引擎原文件不变。许可文本见 [`engine/LICENSE`](../skills/graphic-report/engine/LICENSE)。 |
| `engine/kit/vendor/pele.mjs` | PELE / Copyright (c) 2026 kepano | MIT | 许可文本位于 [`PELE-LICENSE`](../skills/graphic-report/engine/kit/vendor/PELE-LICENSE)。 |
| `engine/kit/vendor/pele.mjs` 中 reset 图标 | Lucide Icons and Contributors | ISC | 许可文本同样列在 `PELE-LICENSE`。 |
| Playwright Core（运行时依赖，不在仓库快照） | Microsoft Playwright contributors | Apache-2.0 | `node_modules` 已被 `.gitignore` 排除，不纳入公开快照；在运行环境单独安装，依赖包自带许可证文本。 |

本说明只涵盖列出的第三方组件，不改变其各自许可。使用者需遵循对应许可文件中的版权声明、许可和再分发条件。

## 研究案例

`skills/graphic-report/examples/case-interview-recap.*` 是基于一场具体访谈整理的案例页面，不含原始逐字稿。它不单独赋予使用者对受访者研究内容的再利用权；超出该 Skill 展示用途的引用、转载或进一步公开，应另行确认研究资料的授权和隐私要求。
