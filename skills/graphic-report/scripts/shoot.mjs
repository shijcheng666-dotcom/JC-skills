#!/usr/bin/env node
// 整页分段截图（桌面 1280 宽），用于人工目检全部版块。
// 用法：node shoot.mjs <page.html> [outDir] [segmentHeight=1500]
// 输出：<outDir>/seg-01.png, seg-02.png ...；依赖 engine 内的 playwright-core 与本机 Chrome/Edge。
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
let n = 0;
for (let y = 0; y < total; y += segH) {
  n++;
  const name = join(outDir, `seg-${String(n).padStart(2, "0")}.png`);
  await page.screenshot({ path: name, clip: { x: 0, y, width: 1280, height: Math.min(segH, total - y) }, fullPage: true });
}
await browser.close();
console.log(`✓ ${n} 张截图 → ${outDir}（页面总高 ${total}px）`);
