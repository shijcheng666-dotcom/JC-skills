#!/usr/bin/env node
// 曲线路径生成器：为 SVG <path d="..."> 生成平滑曲线，避免手写坐标出错。
// 用法：
//   node curve.mjs wave  --x 70,720 --y 130 --amp 80 --cycles 4.5 --decay 0.9 [--n 120]
//       衰减波：振幅随时间逐渐变小，最终趋于平稳（decay 越大收敛越快；0 表示不衰减）
//   node curve.mjs bump  --x 0,100 --y 84 --h 50 --centers 0.5 --w 0.12 [--n 120]
//       一个或多个“冲高后回落”的钟形（centers 为 0~1 的位置，逗号分隔）
//   node curve.mjs pulse --x 0,100 --y 88 --h 56 --at 0.15,0.47,0.74 --w 0.02 [--n 200]
//       平时贴着基线、在若干位置出现尖脉冲
//   node curve.mjs rise  --x 0,100 --y 84 --h 60 --from 0.3 --to 0.7 [--n 120]
//       平稳—爬升—平稳（S 形）
// 说明：y 是基线纵坐标；SVG 纵轴向下，所以“向上”的幅度为 y - h。
// 输出：一行 d 字符串，直接粘贴到 <path d="..."> 即可。
const a = process.argv.slice(2);
const type = a[0];
const arg = (k, d) => { const i = a.indexOf(`--${k}`); return i >= 0 ? a[i + 1] : d; };
const [x0, x1] = (arg("x", "0,100")).split(",").map(Number);
const y0 = Number(arg("y", 100));
const n = Number(arg("n", 120));
const pts = [];
const push = (x, y) => pts.push(`${pts.length ? "L" : "M"}${x.toFixed(1)},${y.toFixed(1)}`);

if (type === "wave") {
  const amp = Number(arg("amp", 60)), cycles = Number(arg("cycles", 4)), decay = Number(arg("decay", 0.8));
  for (let i = 0; i <= n; i++) { const t = i / n; push(x0 + (x1 - x0) * t, y0 - amp * Math.exp(-decay * 4 * t) * Math.sin(2 * Math.PI * cycles * t)); }
} else if (type === "bump") {
  const h = Number(arg("h", 50)), w = Number(arg("w", 0.12)), cs = arg("centers", "0.5").split(",").map(Number);
  for (let i = 0; i <= n; i++) { const t = i / n; push(x0 + (x1 - x0) * t, y0 - h * Math.min(1, cs.reduce((s, c) => s + Math.exp(-(((t - c) / w) ** 2)), 0))); }
} else if (type === "pulse") {
  const h = Number(arg("h", 56)), w = Number(arg("w", 0.02)), at = arg("at", "0.5").split(",").map(Number);
  for (let i = 0; i <= n; i++) { const t = i / n; push(x0 + (x1 - x0) * t, y0 - h * Math.min(1, at.reduce((s, c) => s + Math.exp(-(((t - c) / w) ** 2)), 0))); }
} else if (type === "rise") {
  const h = Number(arg("h", 60)), from = Number(arg("from", 0.3)), to = Number(arg("to", 0.7));
  for (let i = 0; i <= n; i++) { const t = i / n; const s = Math.min(1, Math.max(0, (t - from) / (to - from))); push(x0 + (x1 - x0) * t, y0 - h * (s * s * (3 - 2 * s))); }
} else {
  console.error("用法：node curve.mjs <wave|bump|pulse|rise> --x a,b --y base --h|--amp N [...]"); process.exit(2);
}
console.log(pts.join(" "));
