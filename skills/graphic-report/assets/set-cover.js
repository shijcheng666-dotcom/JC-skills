(function (global) {
  'use strict';

  const STYLE_ID = 'set-cover-component-styles';
  let instanceCount = 0;
  let badgeMeasurer;

  const styles = `
    .set-cover {
      --sc-bg: #ffffff;
      --sc-surface: #ffffff;
      --sc-ink: #172033;
      --sc-muted: #5d6678;
      --sc-rule: #d8dde7;
      --sc-accent: #1768e5;
      --sc-accent2: #7457c8;
      --sc-model-fill: #e7e9ff;
      --sc-self-fill: #fff2cf;
      --sc-neutral-fill: #f4f5f7;
      --sc-intersection: #1268e8;
      --sc-ellipse-stroke: #252a34;
      --sc-split-stroke: #525b6c;
      --sc-on-accent: #ffffff;
      --sc-soft: #f7f9fc;
      max-width: 1380px;
      margin: 0 auto;
      padding: 32px 28px 40px;
      background: var(--sc-bg);
      color: var(--sc-ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.5;
    }

    .set-cover *, .set-cover *::before, .set-cover *::after { box-sizing: border-box; }
    .set-cover .sc-page-header { margin-bottom: 22px; }
    .set-cover .sc-page-title { margin: 0 0 8px; font-size: 27px; line-height: 1.3; }
    .set-cover .sc-page-header p { margin: 0; color: var(--sc-muted); font-size: 14px; }

    .set-cover .sc-legend {
      display: flex;
      flex-wrap: wrap;
      gap: 10px 20px;
      margin-top: 16px;
      color: var(--sc-muted);
      font-size: 13px;
    }

    .set-cover .sc-legend-item { display: inline-flex; align-items: center; gap: 7px; }
    .set-cover .sc-legend-dot { width: 12px; height: 12px; border-radius: 3px; border: 1px solid var(--sc-rule); }
    .set-cover .sc-legend-dot.sc-model { background: var(--sc-model-fill); }
    .set-cover .sc-legend-dot.sc-self { background: var(--sc-self-fill); }
    .set-cover .sc-legend-dot.sc-neutral { background: var(--sc-neutral-fill); }
    .set-cover .sc-legend-dot.sc-intersection { background: var(--sc-intersection); border-color: var(--sc-intersection); }

    .set-cover .sc-panel {
      margin: 0 0 24px;
      overflow: hidden;
      border: 1px solid var(--sc-rule);
      border-radius: 12px;
      background: var(--sc-surface);
    }

    .set-cover .sc-panel figcaption { padding: 16px 20px 0; font-size: 17px; font-weight: 700; }
    .set-cover .sc-figure-index { margin-right: 9px; color: var(--sc-accent); }
    .set-cover .sc-diagram { overflow-x: auto; padding: 2px 12px 0; }
    .set-cover .sc-diagram svg { display: block; width: 100%; height: auto; min-width: 900px; }
    .set-cover .sc-diagram svg.sc-triple { min-width: 1060px; }

    .set-cover .sc-panel-note {
      margin: 0;
      padding: 0 20px 15px;
      color: var(--sc-muted);
      font-size: 12px;
    }

    .set-cover svg text { font-family: inherit; }
    .set-cover .sc-set-title { fill: var(--sc-ink); font-size: 16px; font-weight: 700; text-anchor: middle; }
    .set-cover .sc-set-subtitle { fill: var(--sc-muted); font-size: 13px; text-anchor: middle; }
    .set-cover .sc-set-n { fill: var(--sc-ink); font-size: 14px; font-weight: 600; text-anchor: middle; }
    .set-cover .sc-set-outline { fill: none; stroke: var(--sc-ellipse-stroke); stroke-width: 1.35; }
    .set-cover .sc-split-line { stroke: var(--sc-split-stroke); stroke-width: 1.25; }
    .set-cover .sc-split-label { fill: var(--sc-ink); font-size: 14px; font-weight: 600; text-anchor: middle; }
    .set-cover .sc-badge-title { fill: var(--sc-on-accent); font-size: 13px; font-weight: 700; text-anchor: middle; }
    .set-cover .sc-badge-count { fill: var(--sc-on-accent); font-size: 12px; text-anchor: middle; opacity: 0.9; }
    .set-cover .sc-badge-value { fill: var(--sc-on-accent); font-size: 28px; font-weight: 750; text-anchor: middle; }
    .set-cover .sc-badge-denominator { fill: var(--sc-on-accent); font-size: 11px; text-anchor: middle; }
    .set-cover .sc-badge-separator { stroke: var(--sc-on-accent); stroke-width: 2; opacity: 0.85; }
    .set-cover .sc-blind-title { fill: var(--sc-ink); font-size: 20px; font-weight: 750; text-anchor: middle; }
    .set-cover .sc-blind-meta { fill: var(--sc-muted); font-size: 12px; text-anchor: middle; }
    .set-cover .sc-blind-detail { fill: var(--sc-ink); font-size: 13px; text-anchor: middle; }

    .set-cover .sc-method-note {
      margin: 4px 0 0;
      padding: 14px 16px;
      border-left: 3px solid var(--sc-accent2);
      background: var(--sc-soft);
      color: var(--sc-muted);
      font-size: 13px;
    }

    @media (max-width: 700px) {
      .set-cover { padding: 22px 14px 30px; }
      .set-cover .sc-page-title { font-size: 23px; }
      .set-cover .sc-panel figcaption { padding: 14px 15px 0; font-size: 16px; }
      .set-cover .sc-panel-note { padding: 0 15px 13px; }
    }

    @media print {
      .set-cover { max-width: none; padding: 0; }
      .set-cover .sc-panel { break-inside: avoid; box-shadow: none; }
      .set-cover .sc-diagram { overflow: visible; }
      .set-cover .sc-diagram svg, .set-cover .sc-diagram svg.sc-triple { min-width: 0; }
    }
  `;

  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = styles;
    (document.head || document.documentElement).appendChild(style);
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, character => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    })[character]);
  }

  function percentFromCount(count, denominator) {
    return Math.round((count / denominator) * 100);
  }

  function percentFromRatio(ratio) {
    return Math.round(ratio * 100);
  }

  function bounds(place) {
    return {
      left: place.cx - place.rx,
      right: place.cx + place.rx,
      top: place.cy - place.ry,
      bottom: place.cy + place.ry
    };
  }

  function ellipseTag(place, className, fill) {
    const fillAttribute = fill ? ` fill="${fill}"` : '';
    const classAttribute = className ? ` class="${className}"` : '';
    return `<ellipse${classAttribute} cx="${place.cx}" cy="${place.cy}" rx="${place.rx}" ry="${place.ry}"${fillAttribute}></ellipse>`;
  }

  function overlap(panel, relation) {
    const leftPlace = panel.sets.find(item => item.ref === relation.left);
    const rightPlace = panel.sets.find(item => item.ref === relation.right);
    const leftBounds = bounds(leftPlace);
    const rightBounds = bounds(rightPlace);
    const left = Math.max(leftBounds.left, rightBounds.left);
    const right = Math.min(leftBounds.right, rightBounds.right);
    return {
      left,
      right,
      width: right - left,
      x: (left + right) / 2,
      y: (leftPlace.cy + rightPlace.cy) / 2,
      top: Math.min(leftBounds.top, rightBounds.top),
      bottom: Math.max(leftBounds.bottom, rightBounds.bottom)
    };
  }

  function overlapSlice(panel, relation, y) {
    const slices = [relation.left, relation.right].map(key => {
      const place = panel.sets.find(item => item.ref === key);
      const normalizedY = (y - place.cy) / place.ry;
      const halfWidth = place.rx * Math.sqrt(Math.max(0, 1 - normalizedY * normalizedY));
      return { left: place.cx - halfWidth, right: place.cx + halfWidth };
    });
    const left = Math.max(slices[0].left, slices[1].left);
    const right = Math.min(slices[0].right, slices[1].right);
    return { left, right, width: right - left, x: (left + right) / 2 };
  }

  function badgeText(text, x, y, className, maxWidth, font, fontFamily) {
    if (!badgeMeasurer) {
      badgeMeasurer = document.createElement('canvas').getContext('2d');
    }
    badgeMeasurer.font = `${font} ${fontFamily}`;
    const naturalWidth = badgeMeasurer.measureText(text).width;
    const fit = naturalWidth > maxWidth
      ? ` textLength="${maxWidth.toFixed(2)}" lengthAdjust="spacingAndGlyphs"`
      : '';
    return `<text class="${className}" x="${x}" y="${y}"${fit}>${escapeHtml(text)}</text>`;
  }

  function renderSplitLabel(panel, place, sets) {
    const set = sets[place.ref];
    if (set.awareRatio === undefined) return '';

    const box = bounds(place);
    const inactiveRatio = 1 - set.awareRatio;
    const splitX = set.awareSide === 'left'
      ? box.left + (box.right - box.left) * set.awareRatio
      : box.left + (box.right - box.left) * inactiveRatio;

    const before = panel.sets
      .filter(item => item.cx < place.cx)
      .map(item => bounds(item).right)
      .filter(value => value > box.left && value < box.right);
    const after = panel.sets
      .filter(item => item.cx > place.cx)
      .map(item => bounds(item).left)
      .filter(value => value > box.left && value < box.right);

    const visibleLeft = before.length ? Math.max(...before) : box.left;
    const visibleRight = after.length ? Math.min(...after) : box.right;
    const awareX = set.awareSide === 'left'
      ? (visibleLeft + splitX) / 2
      : (splitX + visibleRight) / 2;
    const unawareX = set.awareSide === 'left'
      ? (splitX + box.right) / 2
      : (box.left + splitX) / 2;
    const awareY = place.awareLabelY || place.cy;

    return `
      <text class="sc-split-label" x="${unawareX}" y="${place.cy}">用户无印象 ${percentFromRatio(inactiveRatio)}%</text>
      <text class="sc-split-label" x="${awareX}" y="${awareY}">用户有印象 ${percentFromRatio(set.awareRatio)}%</text>`;
  }

  function renderBlind(panel, sets) {
    if (!panel.blind) return '';
    const blind = panel.blind;
    const host = panel.sets.find(item => item.ref === blind.set);
    const leftRelation = panel.intersections.find(item => item.right === blind.set);
    const rightRelation = panel.intersections.find(item => item.left === blind.set);
    const hostBounds = bounds(host);
    const leftEdge = leftRelation ? overlap(panel, leftRelation).right : hostBounds.left;
    const rightEdge = rightRelation ? overlap(panel, rightRelation).left : hostBounds.right;
    const x = (leftEdge + rightEdge) / 2;
    const value = percentFromCount(blind.count, sets[blind.set].n);
    const details = blind.detailLines.map((line, index) =>
      `<text class="sc-blind-detail" x="${x}" y="${host.cy + 20 + index * 20}">${escapeHtml(line)}</text>`
    ).join('');

    return `
      <text class="sc-blind-title" x="${x}" y="${host.cy - 31}">${escapeHtml(blind.label)} ${value}%</text>
      <text class="sc-blind-meta" x="${x}" y="${host.cy - 7}">${blind.count} 人 · 分母为集合${escapeHtml(blind.set)}</text>
      ${details}`;
  }

  function renderPanel(panel, panelIndex, sets, instanceId, fontFamily) {
    const panelId = `${instanceId}-panel-${panelIndex}`;
    const clipIds = new Map(panel.sets.map((place, index) => [place.ref, `${panelId}-clip-${index}`]));
    const clipId = key => clipIds.get(key);

    const defs = panel.sets.map(place =>
      `<clipPath id="${clipId(place.ref)}">${ellipseTag(place, '', '')}</clipPath>`
    ).join('');

    const bases = panel.sets.map(place => {
      const set = sets[place.ref];
      const box = bounds(place);
      const baseFill = set.awareRatio === undefined ? 'var(--sc-self-fill)' : 'var(--sc-neutral-fill)';
      let markup = ellipseTag(place, '', baseFill);

      if (set.awareRatio !== undefined) {
        const splitX = set.awareSide === 'left'
          ? box.left + (box.right - box.left) * set.awareRatio
          : box.left + (box.right - box.left) * (1 - set.awareRatio);
        const awareX = set.awareSide === 'left' ? box.left : splitX;
        const awareRight = set.awareSide === 'left' ? splitX : box.right;
        markup += `
          <g clip-path="url(#${clipId(place.ref)})">
            <rect x="${awareX}" y="${box.top}" width="${awareRight - awareX}" height="${place.ry * 2}" fill="var(--sc-model-fill)"></rect>
          </g>`;
      }
      return markup;
    }).join('');

    const badges = panel.intersections.map(relation => {
      const area = overlap(panel, relation);
      return `
        <g clip-path="url(#${clipId(relation.left)})">
          <g clip-path="url(#${clipId(relation.right)})">
            <rect x="${area.left}" y="${area.top}" width="${area.width}" height="${area.bottom - area.top}" fill="var(--sc-intersection)"></rect>
          </g>
        </g>`;
    }).join('');

    const splitLines = panel.sets.map(place => {
      const set = sets[place.ref];
      if (set.awareRatio === undefined) return '';
      const box = bounds(place);
      const splitX = set.awareSide === 'left'
        ? box.left + (box.right - box.left) * set.awareRatio
        : box.left + (box.right - box.left) * (1 - set.awareRatio);
      return `
        <g clip-path="url(#${clipId(place.ref)})">
          <line class="sc-split-line" x1="${splitX}" y1="${box.top}" x2="${splitX}" y2="${box.bottom}"></line>
        </g>`;
    }).join('');

    const outlines = panel.sets.map(place => ellipseTag(place, 'sc-set-outline', '')).join('');

    const headers = panel.sets.map(place => {
      const set = sets[place.ref];
      return `
        <text class="sc-set-title" x="${place.cx}" y="22">集合${escapeHtml(set.key)}｜${escapeHtml(set.name)}</text>
        <text class="sc-set-subtitle" x="${place.cx}" y="45">${escapeHtml(set.subtitle)}</text>
        <text class="sc-set-n" x="${place.cx}" y="66">N=${set.n}</text>`;
    }).join('');

    const badgeLabels = panel.intersections.map(relation => {
      const area = overlap(panel, relation);
      const leftSet = sets[relation.left];
      const rightSet = sets[relation.right];
      const leftValue = `${percentFromCount(relation.count, leftSet.n)}%`;
      const rightValue = `${percentFromCount(relation.count, rightSet.n)}%`;
      const titleY = area.y - 34;
      const countY = area.y - 16;
      const valueY = area.y + 14;
      const denominatorY = area.y + 34;
      const titleSlice = overlapSlice(panel, relation, titleY - 13);
      const countSlice = overlapSlice(panel, relation, countY - 12);
      const denominatorSlice = overlapSlice(panel, relation, denominatorY + 2);
      const padding = 6;
      const columnGap = 6;
      const columnWidth = (denominatorSlice.width - padding * 2 - columnGap) / 2;
      const leftX = denominatorSlice.left + padding + columnWidth / 2;
      const rightX = denominatorSlice.right - padding - columnWidth / 2;
      const centerX = (leftX + rightX) / 2;

      return [
        badgeText(relation.label, titleSlice.x, titleY, 'sc-badge-title', titleSlice.width - 12, '700 13px', fontFamily),
        badgeText(`${relation.count} 人`, countSlice.x, countY, 'sc-badge-count', countSlice.width - 12, '400 12px', fontFamily),
        badgeText(leftValue, leftX, valueY, 'sc-badge-value', columnWidth, '750 28px', fontFamily),
        badgeText(rightValue, rightX, valueY, 'sc-badge-value', columnWidth, '750 28px', fontFamily),
        badgeText(`分母为集合${leftSet.key}`, leftX, denominatorY, 'sc-badge-denominator', columnWidth, '400 11px', fontFamily),
        badgeText(`分母为集合${rightSet.key}`, rightX, denominatorY, 'sc-badge-denominator', columnWidth, '400 11px', fontFamily),
        `<line class="sc-badge-separator" x1="${centerX}" y1="${area.y - 7}" x2="${centerX}" y2="${area.y + 40}"></line>`
      ].join('\n');
    }).join('');

    const splitLabels = panel.sets.map(place => renderSplitLabel(panel, place, sets)).join('');
    const description = panel.intersections.map(relation =>
      `集合${relation.left}与集合${relation.right}交集${relation.count}人，分别占${percentFromCount(relation.count, sets[relation.left].n)}%和${percentFromCount(relation.count, sets[relation.right].n)}%`
    ).join('；');

    return `
      <figure class="sc-panel" aria-labelledby="${panelId}-caption">
        <figcaption id="${panelId}-caption"><span class="sc-figure-index">${escapeHtml(panel.index)}</span>${escapeHtml(panel.title)}</figcaption>
        <div class="sc-diagram">
          <svg class="${panel.sets.length === 3 ? 'sc-triple' : ''}" viewBox="0 0 ${panel.width} ${panel.height}" role="img" aria-labelledby="${panelId}-svg-title ${panelId}-svg-desc">
            <title id="${panelId}-svg-title">${escapeHtml(panel.index)} ${escapeHtml(panel.title)}</title>
            <desc id="${panelId}-svg-desc">${escapeHtml(description)}</desc>
            <defs>${defs}</defs>
            ${bases}
            ${badges}
            ${splitLines}
            ${outlines}
            ${headers}
            ${splitLabels}
            ${badgeLabels}
            ${renderBlind(panel, sets)}
          </svg>
        </div>
        <p class="sc-panel-note">交集徽章：${escapeHtml(description)}。百分比按各自集合 N 为分母计算。</p>
      </figure>`;
  }

  function render(target, data) {
    const host = typeof target === 'string' ? document.getElementById(target) : target;
    if (!host || host.nodeType !== 1) {
      throw new Error('SetCover.render 需要有效的 DOM 元素或元素 id。');
    }

    injectStyles();
    const sets = data.sets;
    const instanceId = `set-cover-${++instanceCount}`;
    const fontFamily = getComputedStyle(document.body).fontFamily;
    const figures = data.panels.map((panel, index) =>
      renderPanel(panel, index, sets, instanceId, fontFamily)
    ).join('');

    host.innerHTML = `
      <main class="set-cover">
        <header class="sc-page-header">
          <h1 class="sc-page-title">复合集合图</h1>
          <p>模型判定、用户自述与普通关注集合的关系</p>
          <div class="sc-legend" aria-label="图例">
            <span class="sc-legend-item"><span class="sc-legend-dot sc-model"></span>有印象</span>
            <span class="sc-legend-item"><span class="sc-legend-dot sc-neutral"></span>无印象</span>
            <span class="sc-legend-item"><span class="sc-legend-dot sc-self"></span>用户自述集合</span>
            <span class="sc-legend-item"><span class="sc-legend-dot sc-intersection"></span>交集标注徽章</span>
          </div>
        </header>
        <div class="sc-figures">${figures}</div>
        <p class="sc-method-note">所有百分比均由交集人数或盲区人数除以对应集合 N 后四舍五入至整数；印象切分线按有印象比例定位。椭圆及蓝色交集面积为结构示意，不与 N 或交集人数构成精确面积比例。</p>
      </main>`;
  }

  global.SetCover = global.SetCover || {};
  global.SetCover.render = render;
}(window));
