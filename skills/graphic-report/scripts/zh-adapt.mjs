#!/usr/bin/env node
// 后处理：把 recap 主题层注入渲染产物（不修改第三方引擎源码），并移除 Google Fonts 外链。幂等。
// 用法：node zh-adapt.mjs <page.html>
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const file = process.argv[2];
if (!file) { console.error("usage: node zh-adapt.mjs <page.html>"); process.exit(2); }
const here = dirname(fileURLToPath(import.meta.url));
const theme = ["recap-theme.css", "vocab.css"].map((f) => readFileSync(join(here, "..", "assets", f), "utf8")).join("\n");

let html = readFileSync(file, "utf8");
html = html
  .replace(/<link[^>]+rel="preconnect"[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>\s*/g, "")
  .replace(/<link[^>]+href="https:\/\/fonts\.googleapis\.com\/css2[^"]*"[^>]*>\s*/g, "")
  .replace(/<style data-zh-adapt>[\s\S]*?<\/style>\s*/g, "");
html = html.replace(/<\/head>/i, `<style data-zh-adapt>\n${theme}\n</style>\n</head>`);
writeFileSync(file, html);
const left = [...new Set((html.match(/https?:\/\/[^\s"'<>)]+/g) || []).filter((u) => !u.includes("w3.org")))];
console.log(`✓ recap 主题已应用 ${file}  外链剩余: ${left.length}${left.length ? " → " + left.join(", ") : ""}`);
