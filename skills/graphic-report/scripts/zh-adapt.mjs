#!/usr/bin/env node
// 后处理：注入中文基础主题与按需复盘层（不修改第三方引擎源码），并移除 Google Fonts 外链。幂等。
// 用法：node zh-adapt.mjs <page.html>
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const file = process.argv[2];
if (!file) { console.error("usage: node zh-adapt.mjs <page.html>"); process.exit(2); }
const here = dirname(fileURLToPath(import.meta.url));
let html = readFileSync(file, "utf8");
const assets = ["base-theme.css", "vocab.css"];
if (/<html\b[^>]*\bdata-theme="recap"/i.test(html)) assets.push("recap-theme.css");
const theme = assets.map((f) => readFileSync(join(here, "..", "assets", f), "utf8")).join("\n");
const themeName = assets.includes("recap-theme.css") ? "中文基础 + recap" : "中文基础";
html = html
  .replace(/<link[^>]+rel="preconnect"[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>\s*/g, "")
  .replace(/<link[^>]+href="https:\/\/fonts\.googleapis\.com\/css2[^"]*"[^>]*>\s*/g, "")
  .replace(/<style data-zh-adapt>[\s\S]*?<\/style>\s*/g, "");
html = html.replace(/<\/head>/i, `<style data-zh-adapt>\n${theme}\n</style>\n</head>`);
writeFileSync(file, html);
const left = [...new Set((html.match(/https?:\/\/[^\s"'<>)]+/g) || []).filter((u) => !u.includes("w3.org")))];
console.log(`✓ ${themeName} 主题已应用 ${file}  外链剩余: ${left.length}${left.length ? " → " + left.join(", ") : ""}`);
