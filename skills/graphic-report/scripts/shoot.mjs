#!/usr/bin/env node
// 桌面截图（1280 宽）：默认整页分段，也可只截取一个图块或局部容器。
// 用法：node shoot.mjs <page.html> [outDir] [segmentHeight=1500] [--figure=N | --selector=CSS]
// 输出：整页为 seg-01.png...；局部为 figure-N.png 或 target.png；依赖 engine 内的 playwright-core 与本机 Chrome/Edge。
import { mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(join(here, "..", "engine", "package.json"));
const { chromium } = require("playwright-core");

const file = resolve(process.argv[2] ?? "");
const outDir = resolve(process.argv[3] ?? join(dirname(file), "shots"));
const segH = Number(process.argv[4] ?? 1500);
mkdirSync(outDir, { recursive: true });

let browser;
try { browser = await chromium.launch({ channel: "chrome" }); }
catch { browser = await chromium.launch({ channel: "msedge" }); }
const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(file).href);
await page.evaluate(() => document.fonts.ready);
// 触发入场动画，避免截到半透明状态
await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } scrollTo(0, 0); });
await page.waitForTimeout(700);
const total = await page.evaluate(() => document.documentElement.scrollHeight);
const figureOption = process.argv.slice(2).find((a) => a.startsWith("--figure="));
const selectorOption = process.argv.slice(2).find((a) => a.startsWith("--selector="));
if (figureOption && selectorOption) throw new Error("--figure 与 --selector 只能使用一个");

if (figureOption || selectorOption) {
  let target;
  let outputName;
  let label;
  if (figureOption) {
    const index = Number(figureOption.slice("--figure=".length));
    const figures = page.locator("main figure");
    const count = await figures.count();
    if (!Number.isInteger(index) || index < 1 || index > count) throw new Error(`图块编号无效：${figureOption}（页面共 ${count} 个 main figure）`);
    target = figures.nth(index - 1);
    outputName = `figure-${String(index).padStart(2, "0")}.png`;
    label = `图块 ${index}/${count}`;
  } else {
    const selector = selectorOption.slice("--selector=".length);
    target = page.locator(selector);
    const count = await target.count();
    if (count !== 1) throw new Error(`局部选择器必须恰好匹配一个元素：${selector}（实际 ${count} 个）`);
    outputName = "target.png";
    label = selector;
  }
  const clip = await target.evaluate((e) => {
    const frames = [...(e.matches(".frame") ? [e] : []), ...e.querySelectorAll(".frame")].filter((f) => f.scrollWidth > f.clientWidth + 1);
    e.__grOld = frames.map((f) => [f, f.getAttribute("style")]);
    for (const f of frames) f.style.cssText += `;overflow:visible;width:${f.scrollWidth}px;max-width:none`;
    const rs = [e, ...frames].map((x) => x.getBoundingClientRect());
    const x = Math.min(...rs.map((r) => r.left)), y = Math.min(...rs.map((r) => r.top));
    return { x: x + scrollX, y: y + scrollY, width: Math.max(...rs.map((r) => r.right)) - x, height: Math.max(...rs.map((r) => r.bottom)) - y };
  });
  const name = join(outDir, outputName);
  try {
    await page.screenshot({ path: name, fullPage: true, clip });
  } finally {
    await target.evaluate((e) => { for (const [f, s] of e.__grOld) s === null ? f.removeAttribute("style") : f.setAttribute("style", s); delete e.__grOld; });
  }
  console.log(`✓ ${label} → ${name}`);
} else {
  let n = 0;
  for (let y = 0; y < total; y += segH) {
    n++;
    const name = join(outDir, `seg-${String(n).padStart(2, "0")}.png`);
    await page.screenshot({ path: name, clip: { x: 0, y, width: 1280, height: Math.min(segH, total - y) }, fullPage: true });
  }
  console.log(`✓ ${n} 张截图 → ${outDir}（页面总高 ${total}px）`);
}
await browser.close();
