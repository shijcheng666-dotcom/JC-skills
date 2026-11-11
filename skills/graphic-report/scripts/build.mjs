#!/usr/bin/env node
// graphic-report 渲染入口：一条命令完成 渲染 → 中文适配 → 浏览器视觉检查
// 用法：node build.mjs <name.src.html> [--open] [--no-check]
//   输出：<name>.html（同目录）；若检查可用，另有 <name>.sheet.png 截图联系表
// 依赖：Node 20+；视觉检查需要 playwright-core（安装在 engine 旁）和本机 Chrome/Edge，缺失时自动跳过检查并提示。
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const engine = join(here, "..", "engine");
const render = join(engine, "kit", "render.mjs");
const args = process.argv.slice(2);
const input = args.find((a) => !a.startsWith("-"));
if (!input) { console.error("usage: node build.mjs <name.src.html> [--open] [--no-check]"); process.exit(2); }
if (!/\.src\.html?$/i.test(input)) { console.error("源文件必须命名为 <name>.src.html"); process.exit(2); }
const src = resolve(input);
const out = src.replace(/\.src(\.html?)$/i, "$1");

// 1) 渲染但不做检查（检查要在中文适配之后进行，才能反映真实字体与排版）
let r = spawnSync(process.execPath, [render, src, "--no-check"], { stdio: "inherit", cwd: dirname(src) });
if (r.status !== 0) process.exit(r.status ?? 1);

// 2) 中文适配
r = spawnSync(process.execPath, [join(here, "zh-adapt.mjs"), out], { stdio: "inherit" });
if (r.status !== 0) process.exit(r.status ?? 1);

// 3) 视觉检查（对适配后的最终页面）
if (!args.includes("--no-check")) {
  const pw = join(engine, "..", "node_modules", "playwright-core");
  const pwEngine = join(engine, "node_modules", "playwright-core");
  if (!existsSync(pw) && !existsSync(pwEngine)) {
    console.log("  ⚠ 未安装 playwright-core，已跳过视觉检查。安装：npm install --no-save --prefix \"" + join(engine) + "\" playwright-core");
  } else {
    const check = `
      import { lookAt, lookLines } from ${JSON.stringify("file:///" + join(here, "desktop-look.mjs").replaceAll("\\", "/"))};
      const looked = await lookAt(${JSON.stringify(out)});
      for (const line of lookLines(looked)) console.log("  " + line);
      process.exitCode = looked.problems.length ? 1 : 0;
    `;
    // 默认只做 1280px 桌面检查；移动端不属于本技能的交付验收范围。
    r = spawnSync(process.execPath, ["--input-type=module", "-e", check], { encoding: "utf8", cwd: engine });
    const lines = (r.stdout || "").split(/\r?\n/);
    const blocking = lines.some((l) => /^\s*✗/.test(l));
    for (const l of lines) if (l.trim()) console.log(l);
    if (r.stderr) console.error(r.stderr);
    if (blocking) {
      console.log("✗ 视觉检查发现问题；页面已写出，请按提示修正后重新运行。");
      process.exitCode = 1;
    }
    else if (!lines.some((l) => /Visual check/.test(l))) console.log("  ✓ 桌面端视觉检查通过");
  }
}
console.log("✓ 输出：" + out);

if (args.includes("--open")) {
  const [cmd, a] = process.platform === "win32" ? ["cmd", ["/c", "start", "", out]] : process.platform === "darwin" ? ["open", [out]] : ["xdg-open", [out]];
  spawnSync(cmd, a, { stdio: "ignore" });
}
