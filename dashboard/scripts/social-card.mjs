// Deterministic 1200x630 social-card renderer (SVG -> PNG via @resvg/resvg-js).
//
// Replaces the old Playwright/Chromium screenshot pipeline: no browser, no
// network, no S3 — the same "resvg, not Chromium" decision as
// scripts/render_front_page.mjs. Output depends only on the inputs, so every
// build (Railway Docker, CI, local) produces a valid card for every article.
//
// Typography: bundled Source Serif 4 statics in scripts/fonts/ (the site's
// own typeface; Subhead optical cut for titles) render identically on every
// host. System fonts remain loaded as a glyph fallback (host serif when the
// bundle is missing, e.g. stripped-down forks; non-Latin glyphs). Titles are
// wrapped with a per-character width estimate — resvg has no text wrapping —
// calibrated against real font metrics so estimation never paints past the
// right margin.

import { existsSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';

export const CARD_WIDTH = 1200;
export const CARD_HEIGHT = 630;

// Bundled brand fonts (dashboard/scripts/fonts/, OFL-licensed Source Serif 4
// statics — the site's own typeface, incl. the Subhead optical size for
// display text). With the bundle present, rendering is host-independent;
// system fonts stay loaded only as a glyph fallback for characters the
// bundle lacks (e.g. CJK).
const FONT_DIR = join(dirname(fileURLToPath(import.meta.url)), 'fonts');
const BUNDLED_FONTS = existsSync(FONT_DIR)
  ? readdirSync(FONT_DIR).filter(f => /\.(otf|ttf)$/i.test(f)).map(f => join(FONT_DIR, f))
  : [];
const RESVG_FONT_OPTIONS = {
  fontFiles: BUNDLED_FONTS,
  loadSystemFonts: true,
  defaultFontFamily: BUNDLED_FONTS.length ? 'Source Serif 4' : 'Georgia',
};

export function pngFromSvg(svg) {
  return new Resvg(svg, { font: RESVG_FONT_OPTIONS }).render().asPng();
}

const PAD_X = 72;
const CONTENT_WIDTH = CARD_WIDTH - PAD_X * 2;

// Brand tokens mirrored from dashboard/src/components/ara-research.css.
// "Folio" treatment (picked from a three-candidate design round): a newspaper
// folio line — date left, domain right, over an ink rule — stamps the top
// edge; the title owns the middle; model attribution sits alone at the foot.
// White ground, no dark outer frame; royal appears exactly once (the domain).
const COLOR = {
  bg: '#ffffff',
  folio: '#191713', // date + rule ink
  title: '#191713', // article display ink
  desc: '#4a4f57',
  attribution: '#6b7078',
  domain: '#2251ff', // --ara-royal
};

// One family everywhere — the site itself sets Source Serif 4 for every role,
// so the card does too. Optical sizes carry the hierarchy: the Subhead cut
// for display titles, the text cut for everything else.
export const FAMILY = {
  title: `'Source Serif 4 Subhead', 'Source Serif 4', Georgia, 'Liberation Serif', serif`,
  text: `'Source Serif 4', Georgia, 'Liberation Serif', serif`,
};

export function escapeXml(s) {
  return String(s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

// Approximate advance width of one character in em units, tuned for a serif
// text face and corrected by per-role calibration below; exactness doesn't
// matter, never-overflowing does.
function charEm(ch) {
  if (/[iljI.,:;'’!|[\]()]/.test(ch)) return 0.32;
  if (/[ftr]/.test(ch)) return 0.38;
  if (ch === ' ') return 0.27;
  if (/[mwMW]/.test(ch)) return 0.92;
  if (/[—]/.test(ch)) return 1.0;
  if (/[–\-]/.test(ch)) return 0.45;
  if (/[A-Z]/.test(ch)) return 0.74;
  if (/[0-9]/.test(ch)) return 0.52;
  if (/[^\x00-\x7f]/.test(ch)) return 1.0; // CJK/emoji/etc: assume full-width
  return 0.52;
}

function rawEstimate(text, sizePx) {
  let em = 0;
  for (const ch of String(text || '')) em += charEm(ch);
  return em * sizePx;
}

// The char table only gets RELATIVE widths roughly right; absolute scale
// depends on the resolved font (bundled Source Serif 4, or the host's serif
// when the bundle is absent). Calibrate once per role by measuring a
// representative sample with resvg's real font metrics and scaling every
// estimate by measured/estimated. Falls back to a conservative 1.12 if
// measurement is unavailable (e.g. no fonts — the render would be blank
// anyway and the postbuild guard catches that).
const CALIBRATION_SAMPLES = {
  title: { text: 'Moonshot AI: the lab that traded its consumer app for the open-weights frontier, 2.8T #1', weight: 700, family: FAMILY.title },
  text: { text: 'From a Pink Floyd-named startup to a $31.5 billion ask in forty months — the funding', weight: 400, family: FAMILY.text },
};
const calibrationCache = new Map();

function measuredWidth(sample, sizePx) {
  const svg =
    `<svg xmlns="http://www.w3.org/2000/svg" width="8000" height="300">` +
    `<text x="0" y="200" font-family="${sample.family}" font-size="${sizePx}" font-weight="${sample.weight}">${escapeXml(sample.text)}</text>` +
    `</svg>`;
  const bbox = new Resvg(svg, { font: RESVG_FONT_OPTIONS }).getBBox();
  return bbox && bbox.width > 0 ? bbox.width : null;
}

function calibration(role) {
  const key = CALIBRATION_SAMPLES[role] ? role : 'title';
  if (calibrationCache.has(key)) return calibrationCache.get(key);
  let ratio = 1.12;
  try {
    const sample = CALIBRATION_SAMPLES[key];
    const size = 64;
    const measured = measuredWidth(sample, size);
    if (measured) {
      ratio = measured / rawEstimate(sample.text, size);
      ratio = Math.min(1.4, Math.max(0.8, ratio));
    }
  } catch {
    // keep the conservative fallback ratio
  }
  calibrationCache.set(key, ratio);
  return ratio;
}

export function estimateWidth(text, sizePx, { role = 'title' } = {}) {
  // 1.06 safety margin over the calibrated estimate absorbs residual
  // per-character error so estimation never paints past the right margin.
  return rawEstimate(text, sizePx) * calibration(role) * 1.06;
}

// Greedy word wrap against the pixel budget. Returns at most maxLines lines;
// overflow is ellipsized on the last line. Words longer than a full line are
// hard-clipped rather than painted past the margin.
export function wrapText(text, sizePx, maxWidthPx, maxLines, opts = {}) {
  const words = String(text || '').trim().split(/\s+/).filter(Boolean);
  const lines = [];
  let line = '';
  for (let i = 0; i < words.length; i++) {
    const candidate = line ? `${line} ${words[i]}` : words[i];
    if (estimateWidth(candidate, sizePx, opts) <= maxWidthPx || !line) {
      line = candidate;
      continue;
    }
    lines.push(line);
    line = words[i];
    if (lines.length === maxLines) break;
  }
  if (lines.length < maxLines && line) lines.push(line);

  const consumed = lines.join(' ').split(/\s+/).length;
  const truncated = consumed < words.length;
  if (truncated || (lines.length && estimateWidth(lines.at(-1), sizePx, opts) > maxWidthPx)) {
    let last = lines.at(-1) || '';
    while (last && estimateWidth(`${last}…`, sizePx, opts) > maxWidthPx) {
      last = last.replace(/\s*\S+$/, '') || last.slice(0, -1);
    }
    lines[lines.length - 1] = `${last.replace(/[\s,;:—–-]+$/, '')}…`;
  }
  return lines;
}

// Pick the largest title size whose wrap fits the line budget without
// truncation; otherwise take the smallest size and let wrapText ellipsize.
// Sizes are ~1.5x the old page-screenshot rendering (~34px display).
export function fitTitle(title, maxWidthPx = CONTENT_WIDTH) {
  const steps = [
    { size: 52, maxLines: 3 },
    { size: 46, maxLines: 4 },
    { size: 40, maxLines: 4 },
  ];
  for (const step of steps) {
    const lines = wrapText(title, step.size, maxWidthPx, step.maxLines);
    if (!lines.length) return { ...step, lines: [] };
    if (!lines.at(-1).endsWith('…')) return { ...step, lines };
  }
  const last = steps.at(-1);
  return { ...last, lines: wrapText(title, last.size, maxWidthPx, last.maxLines) };
}

export function renderSocialCardSvg({ eyebrow, title, description, attribution, domain }) {
  const fitted = fitTitle(String(title || '').trim() || 'ara — AI research arm');
  const titleLineHeight = Math.round(fitted.size * 1.18);
  const titleTop = 150;
  const parts = [];

  parts.push(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${CARD_WIDTH}" height="${CARD_HEIGHT}" viewBox="0 0 ${CARD_WIDTH} ${CARD_HEIGHT}">`,
    `<rect width="${CARD_WIDTH}" height="${CARD_HEIGHT}" fill="${COLOR.bg}"/>`,
  );

  // Folio line: date left, domain right, ink rule underneath.
  if (eyebrow) {
    const eyebrowLine = wrapText(String(eyebrow).toUpperCase(), 24, CONTENT_WIDTH - 300, 1, { role: 'text' })[0] || '';
    parts.push(
      `<text x="${PAD_X}" y="88" font-family="${FAMILY.text}" font-size="24" font-weight="600" letter-spacing="2.5" fill="${COLOR.folio}">${escapeXml(eyebrowLine)}</text>`,
    );
  }
  parts.push(
    `<text x="${CARD_WIDTH - PAD_X}" y="88" text-anchor="end" font-family="${FAMILY.text}" font-size="24" font-weight="600" fill="${COLOR.domain}">${escapeXml(domain || 'ara.guzus.xyz')}</text>`,
    `<line x1="${PAD_X}" y1="112" x2="${CARD_WIDTH - PAD_X}" y2="112" stroke="${COLOR.folio}" stroke-width="2"/>`,
  );

  let cursorY = titleTop;
  for (const line of fitted.lines) {
    cursorY += titleLineHeight;
    parts.push(
      `<text x="${PAD_X}" y="${cursorY}" font-family="${FAMILY.title}" font-size="${fitted.size}" font-weight="700" fill="${COLOR.title}">${escapeXml(line)}</text>`,
    );
  }

  // Description sits under the title but must never crowd the attribution foot.
  const descLimitY = 560;
  if (description) {
    const descSize = 28;
    const descLineHeight = 40;
    let descY = cursorY + 52;
    const room = Math.max(0, Math.floor((descLimitY - 28 - descY) / descLineHeight) + 1);
    const descLines = wrapText(description, descSize, CONTENT_WIDTH, Math.min(3, room), { role: 'text' });
    for (const line of descLines) {
      parts.push(
        `<text x="${PAD_X}" y="${descY}" font-family="${FAMILY.text}" font-size="${descSize}" fill="${COLOR.desc}">${escapeXml(line)}</text>`,
      );
      descY += descLineHeight;
    }
  }

  // Foot: model attribution alone (the folio already carries the domain).
  if (attribution) {
    const attributionLine = wrapText(attribution, 24, CONTENT_WIDTH, 1, { role: 'text' })[0] || '';
    parts.push(
      `<text x="${PAD_X}" y="586" font-family="${FAMILY.text}" font-size="24" font-weight="500" fill="${COLOR.attribution}">${escapeXml(attributionLine)}</text>`,
    );
  }
  parts.push('</svg>');
  return parts.join('\n');
}

export async function renderSocialCardPng(card) {
  return pngFromSvg(renderSocialCardSvg(card));
}

function pngDimensions(buf) {
  // PNG signature (8 bytes) + IHDR length/type (8) → width/height at 16/20.
  if (buf.length < 24 || buf.readUInt32BE(12) !== 0x49484452) return null;
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

// Site-wide default share image: the committed brand illustration with the
// project wordmark centered in white. A manual offset shadow (no SVG filters —
// keeps the resvg feature surface minimal) lifts the text off the busy art.
export async function renderSiteDefaultCardPng(baseImagePng, label = 'ai-research-arm') {
  const dims = pngDimensions(baseImagePng);
  if (!dims) throw new Error('base image is not a PNG');
  const { width, height } = dims;
  const size = Math.round(width / 11.5); // ~111px on the 1280-wide brand art
  const cx = Math.round(width / 2);
  const cy = Math.round(height / 2 + size * 0.35); // baseline for optical vertical center
  const href = `data:image/png;base64,${baseImagePng.toString('base64')}`;
  const text = escapeXml(label);
  const svg = [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">`,
    `<image x="0" y="0" width="${width}" height="${height}" href="${href}"/>`,
    `<text x="${cx}" y="${cy + 4}" text-anchor="middle" font-family="${FAMILY.title}" font-size="${size}" font-weight="700" fill="rgba(5,28,44,0.5)">${text}</text>`,
    `<text x="${cx}" y="${cy}" text-anchor="middle" font-family="${FAMILY.title}" font-size="${size}" font-weight="700" fill="#ffffff">${text}</text>`,
    '</svg>',
  ].join('\n');
  return pngFromSvg(svg);
}
