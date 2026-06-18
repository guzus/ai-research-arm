/** Runtime DOM enhancements for ARA articles and front-page fragments. */

/** Expand `<span class="ara-iso-glyphs" data-count="17" data-glyph="🚶">`
 * into N repeated child glyph spans. Done in JS (not in the article HTML)
 * so authors don't have to paste long strings of identical glyphs and so
 * the count is machine-readable. Hard cap at 200 to keep a typo from
 * rendering a million emoji into the DOM. */
function applyIsotypes(root: HTMLElement): void {
  const groups = root.querySelectorAll<HTMLElement>('.ara-iso-glyphs');
  for (const g of groups) {
    if (g.dataset.expanded === '1') continue;
    const count = Math.max(0, Math.min(200, Number(g.dataset.count) || 0));
    const glyph = g.dataset.glyph || '•';
    g.textContent = '';
    for (let i = 0; i < count; i++) {
      const s = document.createElement('span');
      s.className = 'ara-iso-glyph';
      s.textContent = glyph;
      g.appendChild(s);
    }
    g.dataset.expanded = '1';
  }
}

// ── SVG chart injection ──────────────────────────────────────────────
//
// Authored markup uses <div data-*> only — the writer's tag allowlist
// rejects <svg> in fragments, so we generate SVG at render time and
// inject it here. Same security model as applyBarFills / applyIsotypes:
// values come from data-* attrs (validator strips on*= and inline style),
// and we never `innerHTML` raw author strings — every numeric attr is
// parsed and clamped before being templated into the SVG.

const SVG_NS = 'http://www.w3.org/2000/svg';

function svgEl<T extends SVGElement>(tag: string, attrs: Record<string, string | number>): T {
  const el = document.createElementNS(SVG_NS, tag) as T;
  for (const [k, v] of Object.entries(attrs)) {
    el.setAttribute(k, String(v));
  }
  return el;
}

/** Parse a comma-separated number list from a data attribute. Drops
 * anything non-finite. Caps length so a typo can't blow up render. */
function parseSeries(raw: string | undefined, cap = 1000): number[] {
  if (!raw) return [];
  return raw
    .split(',')
    .map((s) => Number(s.trim()))
    .filter((n) => Number.isFinite(n))
    .slice(0, cap);
}

function parseLabels(raw: string | undefined, cap = 200): string[] {
  if (!raw) return [];
  return raw.split(',').map((s) => s.trim()).slice(0, cap);
}

function approxSvgTextWidth(text: string, fontPx: number, mono = false): number {
  return text.length * fontPx * (mono ? 0.62 : 0.56);
}

function formatNumber(value: number, digits?: number): string {
  if (digits !== undefined) return value.toFixed(digits);
  return Number.isInteger(value) ? String(value) : String(value);
}

function formatUnitValue(value: number, unit: string, digits?: number): string {
  const n = formatNumber(value, digits);
  const u = unit.trim();
  if (!u) return n;
  // Currency prefix with trailing context, e.g. "$/kW" → "$5/kW".
  const currency = u.match(/^([$€£¥₩])(.+)$/);
  if (currency) return `${currency[1]}${n}${currency[2]}`;
  // Bare currency symbol prefixes the number with no space, e.g. "$" → "$5".
  if (/^[$€£¥₩]$/.test(u)) return `${u}${n}`;
  // Percent and percent-prefixed phrases bind tight to the number ("17%", "17% bit share").
  if (u === '%') return `${n}%`;
  if (u.startsWith('%')) return `${n}${u}`;
  // Everything else (alphabetic units like "GB/s", non-ASCII like "μm",
  // multi-word phrases like "k wpm" / "RMB B", or units with punctuation
  // like "index (2019=100)") renders as "<value> <unit>" with a single space.
  return `${n} ${u}`;
}

function fitSvgText(text: string, maxPx: number, fontPx: number, mono = false): string {
  if (approxSvgTextWidth(text, fontPx, mono) <= maxPx) return text;
  const charPx = fontPx * (mono ? 0.62 : 0.56);
  const maxChars = Math.max(6, Math.floor(maxPx / charPx) - 1);
  return `${text.slice(0, maxChars)}…`;
}

function setSvgFullLabel(el: SVGElement, text: string): void {
  el.setAttribute('aria-label', text);
}

function appendSvgTitle(el: SVGElement, text: string): void {
  const title = svgEl<SVGTitleElement>('title', {});
  title.textContent = text;
  el.appendChild(title);
}

const ARA_TOOLTIP_TITLE_ATTR = 'data-ara-tooltip-title';
const ARA_TOOLTIP_BODY_ATTR = 'data-ara-tooltip-body';
const ARA_TOOLTIP_BOUND_ATTR = 'data-ara-tooltip-bound';
let araTooltipDelegatesBound = false;
let araFigureModalLastFocus: HTMLElement | null = null;

function compactText(el: Element | null): string {
  return (el?.textContent || '').replace(/\s+/g, ' ').trim();
}

function formatSignedNumber(value: number, digits?: number): string {
  if (value === 0) return formatNumber(0, digits);
  const sign = value > 0 ? '+' : '-';
  return sign + formatNumber(Math.abs(value), digits);
}

function deltaDigits(value: number): number {
  const abs = Math.abs(value);
  if (abs === 0) return 0;
  if (abs < 1) return 2;
  if (abs < 10) return 2;
  return 1;
}

function formatSignedUnitValue(value: number, unit: string): string {
  if (value === 0) return formatUnitValue(0, unit);
  const sign = value > 0 ? '+' : '-';
  return sign + formatUnitValue(Math.abs(value), unit, deltaDigits(value));
}

function pctLabel(raw: string | undefined): string | null {
  if (!raw) return null;
  const n = Number(raw);
  if (!Number.isFinite(n)) return null;
  return `${Math.max(0, Math.min(100, n))}%`;
}

function setAraTooltip(target: Element, title: string, body = ''): void {
  const cleanTitle = title.replace(/\s+/g, ' ').trim();
  const cleanBody = body.replace(/\s+/g, ' ').trim();
  if (!cleanTitle) return;
  target.setAttribute(ARA_TOOLTIP_TITLE_ATTR, cleanTitle);
  if (cleanBody) target.setAttribute(ARA_TOOLTIP_BODY_ATTR, cleanBody);
  else target.removeAttribute(ARA_TOOLTIP_BODY_ATTR);
  target.setAttribute('aria-label', cleanBody ? `${cleanTitle}: ${cleanBody}` : cleanTitle);
  if ((target instanceof HTMLElement || target instanceof SVGElement) && !target.hasAttribute('tabindex')) {
    target.setAttribute('tabindex', '0');
  }
}

function ensureAraTooltip(): HTMLDivElement {
  let tooltip = document.getElementById('araTooltip') as HTMLDivElement | null;
  if (tooltip) return tooltip;
  tooltip = document.createElement('div');
  tooltip.id = 'araTooltip';
  tooltip.className = 'ara-tooltip';
  tooltip.setAttribute('role', 'tooltip');
  tooltip.hidden = true;
  document.body.appendChild(tooltip);
  return tooltip;
}

function placeAraTooltip(tooltip: HTMLElement, clientX: number, clientY: number): void {
  const gap = 12;
  const edge = 8;
  const rect = tooltip.getBoundingClientRect();
  let x = clientX + gap;
  if (x + rect.width > window.innerWidth - edge) x = clientX - rect.width - gap;
  x = Math.max(edge, Math.min(window.innerWidth - rect.width - edge, x));
  let y = clientY - rect.height - gap;
  if (y < edge) y = clientY + gap;
  y = Math.max(edge, Math.min(window.innerHeight - rect.height - edge, y));
  tooltip.style.left = `${x}px`;
  tooltip.style.top = `${y}px`;
}

function showAraTooltip(target: Element, clientX: number, clientY: number): void {
  const title = target.getAttribute(ARA_TOOLTIP_TITLE_ATTR);
  if (!title) return;
  const body = target.getAttribute(ARA_TOOLTIP_BODY_ATTR) || '';
  const tooltip = ensureAraTooltip();
  tooltip.textContent = '';
  const titleEl = document.createElement('div');
  titleEl.className = 'ara-tooltip-title';
  titleEl.textContent = title;
  tooltip.appendChild(titleEl);
  if (body) {
    const bodyEl = document.createElement('div');
    bodyEl.className = 'ara-tooltip-body';
    bodyEl.textContent = body;
    tooltip.appendChild(bodyEl);
  }
  tooltip.hidden = false;
  tooltip.classList.add('is-visible');
  placeAraTooltip(tooltip, clientX, clientY);
}

function hideAraTooltip(): void {
  const tooltip = document.getElementById('araTooltip') as HTMLDivElement | null;
  if (!tooltip) return;
  tooltip.classList.remove('is-visible');
  tooltip.hidden = true;
}

function closestAraTooltipTarget(start: Element | null): Element | null {
  let el: Element | null = start;
  while (el && el !== document.documentElement) {
    if (el.hasAttribute(ARA_TOOLTIP_TITLE_ATTR)) return el;
    el = el.parentElement;
  }
  return null;
}

function ensureAraTooltipDelegates(): void {
  if (araTooltipDelegatesBound) return;
  araTooltipDelegatesBound = true;

  const handleMove = (event: MouseEvent): void => {
    const target = closestAraTooltipTarget(document.elementFromPoint(event.clientX, event.clientY));
    if (target) showAraTooltip(target, event.clientX, event.clientY);
    else hideAraTooltip();
  };

  document.addEventListener('mousemove', handleMove, true);
  document.addEventListener('pointermove', handleMove, true);
  document.addEventListener('mouseleave', hideAraTooltip, true);
  document.addEventListener('focusin', (event) => {
    const target = closestAraTooltipTarget(event.target instanceof Element ? event.target : null);
    if (!target) return;
    const rect = target.getBoundingClientRect();
    showAraTooltip(target, rect.left + rect.width / 2, rect.top + rect.height / 2);
  }, true);
  document.addEventListener('focusout', hideAraTooltip, true);
}

function bindAraTooltip(target: Element): void {
  ensureAraTooltipDelegates();
  if (target.getAttribute(ARA_TOOLTIP_BOUND_ATTR) === '1') return;
  target.setAttribute(ARA_TOOLTIP_BOUND_ATTR, '1');
  // Typed as EventListener (not MouseEvent) because addEventListener on the
  // base Element interface uses ElementEventMap, which does not include
  // pointer/mouse events — TS6 routes through the string-based overload that
  // requires Event. PointerEvent extends MouseEvent at runtime, so the
  // instanceof narrowing covers both pointer* and mouse* listeners below.
  const showFromMouse: EventListener = (event) => {
    if (!(event instanceof MouseEvent)) return;
    showAraTooltip(target, event.clientX, event.clientY);
  };
  const moveFromMouse: EventListener = (event) => {
    if (!(event instanceof MouseEvent)) return;
    const tooltip = document.getElementById('araTooltip') as HTMLDivElement | null;
    if (!tooltip || tooltip.hidden) return;
    placeAraTooltip(tooltip, event.clientX, event.clientY);
  };
  target.addEventListener('pointerenter', showFromMouse);
  target.addEventListener('pointermove', moveFromMouse);
  target.addEventListener('pointerleave', hideAraTooltip);
  target.addEventListener('mouseenter', showFromMouse);
  target.addEventListener('mousemove', moveFromMouse);
  target.addEventListener('mouseleave', hideAraTooltip);
  const showFromFocus = () => {
    const rect = target.getBoundingClientRect();
    showAraTooltip(target, rect.left + rect.width / 2, rect.top + rect.height / 2);
  };
  target.addEventListener('focus', showFromFocus);
  target.addEventListener('focusin', showFromFocus);
  target.addEventListener('blur', hideAraTooltip);
  target.addEventListener('focusout', hideAraTooltip);
}

function figureModalCaptionForImage(img: HTMLImageElement): string {
  const figure = img.closest('.ara-figure');
  const caption = figure?.querySelector('.ara-caption, figcaption');
  return (caption?.textContent || '').replace(/\s+/g, ' ').trim();
}

function prepareAraFigures(root: HTMLElement): void {
  const imgs = root.querySelectorAll<HTMLImageElement>('.ara-figure img');
  for (const img of imgs) {
    img.dataset.araFigureLightbox = '1';
    if (!img.hasAttribute('tabindex')) img.tabIndex = 0;
    img.setAttribute('role', 'button');
    const label = figureModalCaptionForImage(img) || img.alt || 'figure';
    img.setAttribute('aria-label', `Open figure: ${label}`);
  }
}

function ensureAraFigureModal(): HTMLDivElement {
  let modal = document.getElementById('araFigureModal') as HTMLDivElement | null;
  if (modal) return modal;

  modal = document.createElement('div');
  modal.id = 'araFigureModal';
  modal.className = 'ara-figure-modal';
  modal.hidden = true;
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.setAttribute('aria-label', 'Expanded figure');

  const backdrop = document.createElement('button');
  backdrop.className = 'ara-figure-modal-backdrop';
  backdrop.type = 'button';
  backdrop.dataset.araFigureClose = '1';
  backdrop.setAttribute('aria-label', 'Close expanded figure');

  const panel = document.createElement('div');
  panel.className = 'ara-figure-modal-panel';
  panel.setAttribute('role', 'document');

  const close = document.createElement('button');
  close.className = 'ara-figure-modal-close';
  close.type = 'button';
  close.dataset.araFigureClose = '1';
  close.setAttribute('aria-label', 'Close expanded figure');
  close.textContent = '×';

  const image = document.createElement('img');
  image.className = 'ara-figure-modal-img';
  image.alt = '';

  const caption = document.createElement('div');
  caption.className = 'ara-figure-modal-caption';

  panel.appendChild(close);
  panel.appendChild(image);
  panel.appendChild(caption);
  modal.appendChild(backdrop);
  modal.appendChild(panel);
  modal.addEventListener('click', (event) => {
    if (event.target instanceof Element && event.target.closest('[data-ara-figure-close]')) {
      closeAraFigureModal();
    }
  });
  document.body.appendChild(modal);
  return modal;
}

export function openAraFigureModal(img: HTMLImageElement): void {
  const src = img.currentSrc || img.src;
  if (!src) return;
  const modal = ensureAraFigureModal();
  const modalImg = modal.querySelector<HTMLImageElement>('.ara-figure-modal-img');
  const caption = modal.querySelector<HTMLElement>('.ara-figure-modal-caption');
  const close = modal.querySelector<HTMLButtonElement>('.ara-figure-modal-close');
  if (!modalImg || !caption || !close) return;

  araFigureModalLastFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
  modalImg.src = src;
  modalImg.alt = img.alt || '';
  const captionText = figureModalCaptionForImage(img);
  caption.textContent = captionText;
  caption.hidden = !captionText;
  modal.hidden = false;
  document.body.classList.add('ara-figure-modal-open');
  close.focus();
}

export function closeAraFigureModal(): void {
  const modal = document.getElementById('araFigureModal') as HTMLDivElement | null;
  if (!modal || modal.hidden) return;
  const modalImg = modal.querySelector<HTMLImageElement>('.ara-figure-modal-img');
  modal.hidden = true;
  if (modalImg) modalImg.removeAttribute('src');
  document.body.classList.remove('ara-figure-modal-open');
  araFigureModalLastFocus?.focus();
  araFigureModalLastFocus = null;
}

function numberedVariant(el: Element, prefix: string): string | null {
  for (const className of Array.from(el.classList)) {
    const match = new RegExp(`^${prefix}--(\\d+)$`).exec(className);
    if (match) return match[1];
  }
  return null;
}

function stackSegmentCategory(seg: HTMLElement): string {
  const ownText = compactText(seg);
  if (ownText) return ownText;
  const idx = numberedVariant(seg, 'ara-stack-seg');
  if (!idx) return 'Segment';
  const rows = seg.closest('.ara-stack-rows');
  const rowCat = rows?.querySelector(`.ara-stack-rows-cat--${idx}`);
  if (rowCat) return compactText(rowCat);
  const stack = seg.closest('.ara-stack-bar');
  const legend = stack?.nextElementSibling?.classList.contains('ara-stack-legend')
    ? stack.nextElementSibling
    : stack?.parentElement?.querySelector('.ara-stack-legend');
  const legendItem = legend?.querySelector(`.ara-stack-dot--${idx}`)?.closest('li');
  return compactText(legendItem ?? null) || `Segment ${idx}`;
}

function decorateDataTooltips(root: HTMLElement): void {
  for (const bar of root.querySelectorAll<HTMLElement>('.ara-bar[data-pct]')) {
    const pct = pctLabel(bar.dataset.pct);
    if (!pct) continue;
    const label = compactText(bar.querySelector('.ara-bar-label')) || 'Bar';
    const value = compactText(bar.querySelector('.ara-bar-value'));
    setAraTooltip(bar, label, value ? `${value} · ${pct} of scale` : `${pct} of scale`);
  }

  for (const item of root.querySelectorAll<HTMLElement>('.ara-rank-item')) {
    const fill = item.querySelector<HTMLElement>('.ara-rank-fill[data-pct]');
    const pct = pctLabel(fill?.dataset.pct);
    if (!fill || !pct) continue;
    const rank = compactText(item.querySelector('.ara-rank-num'));
    const label = compactText(item.querySelector('.ara-rank-label')) || 'Ranked item';
    const value = compactText(item.querySelector('.ara-rank-value'));
    const prefix = rank ? `#${rank} · ` : '';
    setAraTooltip(item, `${prefix}${label}`, value ? `${value} · ${pct} of max` : `${pct} of max`);
  }

  for (const seg of root.querySelectorAll<HTMLElement>('.ara-stack-seg[data-pct]')) {
    const pct = pctLabel(seg.dataset.pct);
    if (!pct) continue;
    const row = seg.closest('.ara-stack-rows-row');
    const rowLabel = compactText(row?.querySelector('.ara-stack-rows-label') || null);
    const category = stackSegmentCategory(seg);
    setAraTooltip(seg, rowLabel ? `${rowLabel} · ${category}` : category, pct);
  }
}

function applyAraTooltips(root: HTMLElement): void {
  decorateDataTooltips(root);
  for (const target of root.querySelectorAll<Element>(`[${ARA_TOOLTIP_TITLE_ATTR}]`)) {
    bindAraTooltip(target);
  }
}

/** Distribute words across `lineCount` lines, minimizing the longest line
 * (in characters, including the inter-word space). Greedy enumeration of
 * split points; O(W^(lineCount-1)) so we cap lineCount at 3 and words at ≤8
 * for the donut center-label case. Returns null if lineCount > words.length. */
function splitWordsIntoLines(words: string[], lineCount: number): string[] | null {
  if (lineCount < 1 || lineCount > words.length) return null;
  if (lineCount === 1) return [words.join(' ')];

  const widthOf = (line: string) => line.length; // monospace: width ≈ chars
  let best: { lines: string[]; widest: number } | null = null;

  // Enumerate all ways to choose (lineCount-1) split positions from
  // (words.length-1) gaps. Recursive walk for arbitrary lineCount.
  const walk = (startWord: number, linesLeft: number, acc: string[]) => {
    if (linesLeft === 1) {
      const tail = words.slice(startWord).join(' ');
      const candidate = [...acc, tail];
      const widest = Math.max(...candidate.map(widthOf));
      if (!best || widest < best.widest) best = { lines: candidate, widest };
      return;
    }
    // Leave at least (linesLeft - 1) words for the remaining lines.
    const maxEnd = words.length - (linesLeft - 1);
    for (let end = startWord + 1; end <= maxEnd; end++) {
      const line = words.slice(startWord, end).join(' ');
      walk(end, linesLeft - 1, [...acc, line]);
    }
  };
  walk(0, lineCount, []);
  return best ? (best as { lines: string[]; widest: number }).lines : null;
}

/** Wrap a donut center-label into up to `maxLines` lines and pick a font
 * size that fits the widest line within `usableWidth` SVG units. Prefers
 * fewer lines at larger fonts. Falls back to clamped `minFontSize` for a
 * single ultra-long unhyphenated word (it will visually overflow, which
 * is better than dropping the label). */
function wrapDonutCenterLabel(
  label: string,
  maxFontSize: number,
  minFontSize: number,
  usableWidth: number,
  maxLines = 3,
): { lines: string[]; fontSize: number } {
  const clean = label.trim();
  if (!clean) return { lines: [], fontSize: maxFontSize };

  // 1-line fast path: if the whole string fits at max font, use it.
  // Preserves the exact pre-change rendering for short labels.
  // Uses approxSvgTextWidth with mono=true (0.62 ratio) for consistency
  // with the rest of the SVG-text helpers in this file.
  if (approxSvgTextWidth(clean, maxFontSize, true) <= usableWidth) {
    return { lines: [clean], fontSize: maxFontSize };
  }

  const words = clean.split(/\s+/);

  // Guard against pathological input. splitWordsIntoLines is recursive and
  // enumerates O(W^(maxLines-1)) split positions; with maxLines=3 that's
  // O(W^2). Realistic donut center-labels are 1-4 words (the longest in
  // the corpus is "The three-leg bottleneck" at 3 words). If a malformed
  // ara source ever stuffs a paragraph into center-label, bypass the wrap
  // enumeration entirely and render the whole label on a single shrunk
  // line — better than hanging the page or silently dropping words.
  const WORD_ENUM_CAP = 12;
  if (words.length > WORD_ENUM_CAP) {
    const ideal = usableWidth / Math.max(1, clean.length * 0.62);
    const fontSize = Math.max(minFontSize, Math.min(maxFontSize, ideal));
    return { lines: [clean], fontSize };
  }

  // Try N = 1..maxLines. For each N, find the split that minimizes the
  // widest line, then compute the largest font that fits that line.
  // Prefer the largest font (which tends to be the highest N that still
  // fits comfortably). Short-circuit once we hit the max font.
  const lineCap = Math.min(maxLines, words.length);
  let best: { lines: string[]; fontSize: number } | null = null;
  for (let n = 1; n <= lineCap; n++) {
    const lines = splitWordsIntoLines(words, n);
    if (!lines) continue;
    const widestChars = Math.max(...lines.map((l) => l.length));
    // font ≤ usableWidth / (widestChars * 0.62)
    const ideal = usableWidth / Math.max(1, widestChars * 0.62);
    const fontSize = Math.max(minFontSize, Math.min(maxFontSize, ideal));
    if (!best || fontSize > best.fontSize) {
      best = { lines, fontSize };
    }
    // If this N hits the cap, no point trying more lines (more lines
    // can't beat a max-font fit at fewer lines).
    if (fontSize >= maxFontSize) break;
  }
  return best ?? { lines: [clean], fontSize: minFontSize };
}

/** Build a polyline d-attribute from (x,y) pairs. */
function pathFromPoints(points: Array<[number, number]>): string {
  if (!points.length) return '';
  return points
    .map(([x, y], i) => (i === 0 ? `M${x.toFixed(2)},${y.toFixed(2)}` : `L${x.toFixed(2)},${y.toFixed(2)}`))
    .join(' ');
}

type LineChartPoint = {
  x: number;
  y: number;
  xLabel: string;
  valueLabel: string;
  seriesLabel: string;
  seriesIndex: number;
  pointIndex: number;
};

// ── TradingView live embed ────────────────────────────
// The article fragment carries only a script-free placeholder
// `<div class="ara-tradingview" data-symbol="NASDAQ:NOW">` plus a fallback
// link — the writer's validator rejects <script>/<iframe> in fragments. Here,
// in trusted dashboard code, we inject the real TradingView Advanced Chart
// widget, lazily via IntersectionObserver so s3.tradingview.com is only hit
// when a chart scrolls into view. The symbol is re-validated (defense in
// depth) before it reaches the third-party widget config.
const TV_SYMBOL_RE = /^[A-Za-z0-9:._-]{1,32}$/;
const TV_TOKEN_RE = /^[A-Za-z0-9]{1,5}$/;
const TV_EMBED_SRC = 'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js';

function mountTradingView(el: HTMLElement): void {
  if (el.dataset.tvMounted === '1') return;
  const symbol = el.getAttribute('data-symbol') || '';
  if (!TV_SYMBOL_RE.test(symbol)) return; // bad symbol → leave the fallback link in place
  el.dataset.tvMounted = '1';

  const interval = el.getAttribute('data-interval') || 'D';
  const range = el.getAttribute('data-range') || '';
  const theme = el.getAttribute('data-theme') === 'light' ? 'light' : 'dark';

  const config: Record<string, unknown> = {
    autosize: true,
    symbol,
    theme,
    style: '1',
    locale: 'en',
    allow_symbol_change: false,
    hide_side_toolbar: true,
    support_host: 'https://www.tradingview.com',
  };
  if (TV_TOKEN_RE.test(interval)) config.interval = interval;
  if (range && TV_TOKEN_RE.test(range)) config.range = range;

  const container = document.createElement('div');
  container.className = 'tradingview-widget-container';
  const widget = document.createElement('div');
  widget.className = 'tradingview-widget-container__widget';
  container.appendChild(widget);

  // The embed script reads its JSON config from its own text content. We set
  // it via textContent (never innerHTML) before appending, so there is no HTML
  // parsing surface; the symbol is regex-validated above.
  const script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = TV_EMBED_SRC;
  script.async = true;
  script.textContent = JSON.stringify(config);
  container.appendChild(script);

  el.appendChild(container);
  el.classList.add('is-loaded'); // CSS hides .ara-tradingview-fallback
}

/** Inject live TradingView widgets into `<div class="ara-tradingview" data-symbol>`
 * placeholders, lazily as they scroll into view. */
function renderTradingView(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-tradingview[data-symbol]');
  if (!els.length) return;
  if (typeof IntersectionObserver === 'undefined') {
    els.forEach(mountTradingView);
    return;
  }
  const io = new IntersectionObserver(
    (entries, obs) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          mountTradingView(entry.target as HTMLElement);
          obs.unobserve(entry.target);
        }
      }
    },
    { rootMargin: '200px' },
  );
  els.forEach((el) => io.observe(el));
}

/** Sparkline — small inline trend, no axes. */
function renderSparklines(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-sparkline');
  for (const el of els) {
    if (el.dataset.rendered === '1') continue;
    const values = parseSeries(el.dataset.points, 500);
    if (values.length < 2) continue;
    const w = 80;
    const h = 22;
    const pad = 2;
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;
    const points: Array<[number, number]> = values.map((v, i) => [
      pad + (i / (values.length - 1)) * (w - pad * 2),
      h - pad - ((v - min) / range) * (h - pad * 2),
    ]);
    const svg = svgEl<SVGSVGElement>('svg', { viewBox: `0 0 ${w} ${h}`, preserveAspectRatio: 'none' });
    const path = svgEl<SVGPathElement>('path', { class: 'ara-sparkline-path', d: pathFromPoints(points) });
    svg.appendChild(path);
    const last = points[points.length - 1];
    const dot = svgEl<SVGCircleElement>('circle', { class: 'ara-sparkline-end', cx: last[0], cy: last[1], r: 1.6 });
    svg.appendChild(dot);
    const firstValue = values[0];
    const lastValue = values[values.length - 1];
    const delta = lastValue - firstValue;
    const pct = firstValue !== 0 ? ` (${formatSignedNumber((delta / Math.abs(firstValue)) * 100, 1)}%)` : '';
    const label =
      `${formatNumber(firstValue)} to ${formatNumber(lastValue)}; ` +
      `change ${formatSignedNumber(delta, deltaDigits(delta))}${pct}`;
    el.setAttribute(
      'aria-label',
      `Sparkline ${label}`,
    );
    el.setAttribute('role', 'img');
    setAraTooltip(el, 'Sparkline', label);
    el.textContent = '';
    el.appendChild(svg);
    el.dataset.rendered = '1';
  }
}

/** Full line chart with axes. Supports up to 4 series via data-series-{1..4}.
 * Optional data-series-{N}-label, data-x-labels, data-y-unit, data-title,
 * data-subtitle. */
function renderLineCharts(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-line-chart');
  for (const el of els) {
    if (el.dataset.rendered === '1') continue;
    // data-series-N attrs use digit suffixes — DOMStringMap leaves the
    // hyphen in (data-series-1 does NOT map to dataset.series1), so read
    // them with getAttribute to sidestep the gotcha.
    const seriesList: Array<{ values: number[]; label: string }> = [];
    for (let i = 1; i <= 4; i++) {
      const v = parseSeries(el.getAttribute(`data-series-${i}`) || undefined, 1000);
      if (!v.length) continue;
      const label = el.getAttribute(`data-series-${i}-label`) || `Series ${i}`;
      seriesList.push({ values: v, label });
    }
    if (!seriesList.length) continue;
    const xLabels = parseLabels(el.dataset.xLabels, 1000);
    const yUnit = el.dataset.yUnit || '';
    const title = el.dataset.title || '';
    const subtitle = el.dataset.subtitle || '';

    const W = 640;
    const H = 220;
    const MT = 10;
    const MB = 26;

    const allValues = seriesList.flatMap((s) => s.values);
    const min = Math.min(...allValues);
    const max = Math.max(...allValues);
    const pad = (max - min) * 0.08 || 1;
    const yMin = min - pad;
    const yMax = max + pad;
    const yRange = yMax - yMin || 1;
    const longest = Math.max(...seriesList.map((s) => s.values.length));
    const Y_TICKS = 5;
    const yTickLabels = Array.from({ length: Y_TICKS + 1 }, (_, i) => {
      const v = yMax - (i / Y_TICKS) * yRange;
      return formatUnitValue(v, yUnit, yRange < 5 ? 2 : 1);
    });
    const maxYLabelW = Math.max(...yTickLabels.map((label) => approxSvgTextWidth(label, 10, true)));
    const ML = Math.min(118, Math.max(44, Math.ceil(maxYLabelW) + 10));
    const MR = 16;
    const innerW = W - ML - MR;
    const innerH = H - MT - MB;

    const xFor = (i: number, total: number) => ML + (i / Math.max(1, total - 1)) * innerW;
    const yFor = (v: number) => MT + innerH - ((v - yMin) / yRange) * innerH;

    el.textContent = '';
    if (title) {
      const t = document.createElement('p');
      t.className = 'ara-line-chart-title';
      t.textContent = title;
      el.appendChild(t);
    }
    if (subtitle) {
      const s = document.createElement('p');
      s.className = 'ara-line-chart-subtitle';
      s.textContent = subtitle;
      el.appendChild(s);
    }
    const svg = svgEl<SVGSVGElement>('svg', { viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: 'xMidYMid meet' });

    // 5 horizontal gridlines + y-axis tick labels
    for (let i = 0; i <= Y_TICKS; i++) {
      const y = MT + (i / Y_TICKS) * innerH;
      svg.appendChild(svgEl('line', { class: 'ara-chart-grid', x1: ML, y1: y, x2: W - MR, y2: y }));
      const lab = svgEl<SVGTextElement>('text', { class: 'ara-chart-tick-label', x: ML - 6, y: y + 3, 'text-anchor': 'end' });
      lab.textContent = yTickLabels[i];
      svg.appendChild(lab);
    }

    // X-axis labels — sparse to avoid clutter
    if (xLabels.length) {
      const stepRender = Math.max(1, Math.ceil(xLabels.length / 8));
      for (let i = 0; i < xLabels.length; i += stepRender) {
        const x = xFor(i, xLabels.length);
        const anchor = i === 0 ? 'start' : i + stepRender >= xLabels.length ? 'end' : 'middle';
        const lab = svgEl<SVGTextElement>('text', { class: 'ara-chart-tick-label', x, y: H - 8, 'text-anchor': anchor });
        lab.textContent = xLabels[i];
        svg.appendChild(lab);
      }
    }

    const chartPoints: LineChartPoint[] = [];

    // Series paths
    seriesList.forEach((s, idx) => {
      const points: Array<[number, number]> = s.values.map((v, i) => [
        xFor(i, s.values.length === 1 ? 2 : s.values.length),
        yFor(v),
      ]);
      const latestLabel = xLabels[s.values.length - 1] || `point ${s.values.length}`;
      const latestValue = formatUnitValue(s.values[s.values.length - 1], yUnit);
      const path = svgEl<SVGPathElement>('path', {
        class: `ara-chart-series ara-chart-series-${idx + 1}`,
        d: pathFromPoints(points),
        tabindex: '0',
      });
      appendSvgTitle(path, `${s.label}: latest ${latestValue} (${latestLabel})`);
      svg.appendChild(path);

      if (points.length <= 24) {
        points.forEach(([x, y], pointIdx) => {
          const label = xLabels[pointIdx] || `point ${pointIdx + 1}`;
          const value = formatUnitValue(s.values[pointIdx], yUnit);
          const visible = svgEl<SVGCircleElement>('circle', {
            class: `ara-chart-point ara-chart-point--${idx + 1}`,
            cx: x,
            cy: y,
            r: 2.2,
          });
          svg.appendChild(visible);
          const hit = svgEl<SVGCircleElement>('circle', {
            class: 'ara-chart-hit',
            cx: x,
            cy: y,
            r: 7,
          });
          appendSvgTitle(hit, `${s.label} · ${label}: ${value}`);
          svg.appendChild(hit);
        });
      }

      points.forEach(([x, y], pointIdx) => {
        chartPoints.push({
          x,
          y,
          xLabel: xLabels[pointIdx] || `point ${pointIdx + 1}`,
          valueLabel: formatUnitValue(s.values[pointIdx], yUnit),
          seriesLabel: s.label,
          seriesIndex: idx,
          pointIndex: pointIdx,
        });
      });
    });

    if (chartPoints.length) {
      const hoverZone = svgEl<SVGRectElement>('rect', {
        class: 'ara-chart-hover-zone',
        x: ML,
        y: MT,
        width: innerW,
        height: innerH,
        tabindex: '0',
        role: 'img',
        'aria-label': `${title || 'Line chart'}: hover or focus to inspect point values`,
      });
      const tooltip = svgEl<SVGGElement>('g', { class: 'ara-chart-tooltip', 'aria-hidden': 'true' });
      const guide = svgEl<SVGLineElement>('line', {
        class: 'ara-chart-tooltip-guide',
        x1: ML,
        y1: MT,
        x2: ML,
        y2: H - MB,
      });
      const marker = svgEl<SVGCircleElement>('circle', {
        class: 'ara-chart-tooltip-marker ara-chart-point--1',
        cx: ML,
        cy: MT,
        r: 4,
      });
      const box = svgEl<SVGRectElement>('rect', {
        class: 'ara-chart-tooltip-box',
        x: 0,
        y: 0,
        width: 80,
        height: 36,
        rx: 0,
      });
      const labelText = svgEl<SVGTextElement>('text', {
        class: 'ara-chart-tooltip-label',
        x: 8,
        y: 14,
      });
      const valueText = svgEl<SVGTextElement>('text', {
        class: 'ara-chart-tooltip-value',
        x: 8,
        y: 29,
      });

      tooltip.appendChild(guide);
      tooltip.appendChild(marker);
      tooltip.appendChild(box);
      tooltip.appendChild(labelText);
      tooltip.appendChild(valueText);
      svg.appendChild(hoverZone);
      svg.appendChild(tooltip);

      const keyboardPoints = [...chartPoints].sort((a, b) => a.pointIndex - b.pointIndex || a.seriesIndex - b.seriesIndex);
      let keyboardIndex = keyboardPoints.length - 1;

      const nearestPoint = (svgX: number, svgY: number): LineChartPoint => {
        let best = chartPoints[0];
        let bestScore = Number.POSITIVE_INFINITY;
        for (const point of chartPoints) {
          const dx = point.x - svgX;
          const dy = point.y - svgY;
          const score = dx * dx + dy * dy;
          if (score < bestScore) {
            best = point;
            bestScore = score;
          }
        }
        return best;
      };

      const showTooltip = (point: LineChartPoint): void => {
        const labelLine = seriesList.length > 1 ? `${point.xLabel} · ${point.seriesLabel}` : point.xLabel;
        const valueLine = point.valueLabel;
        const maxTextW = 150;
        const fittedLabel = fitSvgText(labelLine, maxTextW, 10);
        const fittedValue = fitSvgText(valueLine, maxTextW, 11, true);
        const boxW = Math.ceil(Math.max(76, Math.max(approxSvgTextWidth(fittedLabel, 10), approxSvgTextWidth(fittedValue, 11, true)) + 16));
        const boxH = 36;
        let boxX = point.x + 10;
        if (boxX + boxW > W - 4) boxX = point.x - boxW - 10;
        boxX = Math.max(4, Math.min(W - boxW - 4, boxX));
        let boxY = point.y - boxH - 10;
        if (boxY < 4) boxY = point.y + 10;
        boxY = Math.max(4, Math.min(H - boxH - 4, boxY));

        guide.setAttribute('x1', point.x.toFixed(2));
        guide.setAttribute('x2', point.x.toFixed(2));
        marker.setAttribute('cx', point.x.toFixed(2));
        marker.setAttribute('cy', point.y.toFixed(2));
        marker.setAttribute('class', `ara-chart-tooltip-marker ara-chart-point--${point.seriesIndex + 1}`);
        box.setAttribute('x', boxX.toFixed(2));
        box.setAttribute('y', boxY.toFixed(2));
        box.setAttribute('width', String(boxW));
        box.setAttribute('height', String(boxH));
        labelText.setAttribute('x', (boxX + 8).toFixed(2));
        labelText.setAttribute('y', (boxY + 14).toFixed(2));
        labelText.textContent = fittedLabel;
        valueText.setAttribute('x', (boxX + 8).toFixed(2));
        valueText.setAttribute('y', (boxY + 29).toFixed(2));
        valueText.textContent = fittedValue;
        tooltip.classList.add('is-visible');
        tooltip.setAttribute('aria-hidden', 'false');
        hoverZone.setAttribute('aria-label', `${point.seriesLabel} · ${point.xLabel}: ${point.valueLabel}`);
      };

      const hideTooltip = (): void => {
        tooltip.classList.remove('is-visible');
        tooltip.setAttribute('aria-hidden', 'true');
      };

      const pointerToSvg = (event: PointerEvent): [number, number] => {
        const rect = svg.getBoundingClientRect();
        const svgX = ((event.clientX - rect.left) / Math.max(1, rect.width)) * W;
        const svgY = ((event.clientY - rect.top) / Math.max(1, rect.height)) * H;
        return [svgX, svgY];
      };

      hoverZone.addEventListener('pointermove', (event) => {
        const [svgX, svgY] = pointerToSvg(event);
        showTooltip(nearestPoint(svgX, svgY));
      });
      hoverZone.addEventListener('pointerleave', hideTooltip);
      hoverZone.addEventListener('focus', () => {
        keyboardIndex = keyboardPoints.length - 1;
        showTooltip(keyboardPoints[keyboardIndex]);
      });
      hoverZone.addEventListener('blur', hideTooltip);
      hoverZone.addEventListener('keydown', (event) => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        const step = event.key === 'ArrowRight' ? 1 : -1;
        keyboardIndex = Math.max(0, Math.min(keyboardPoints.length - 1, keyboardIndex + step));
        showTooltip(keyboardPoints[keyboardIndex]);
      });
    }

    el.appendChild(svg);
    longest; // (silence unused — could be used for x-tick stride)

    // Legend
    if (seriesList.length > 1) {
      const legend = document.createElement('div');
      legend.className = 'ara-line-chart-legend';
      seriesList.forEach((s, idx) => {
        const item = document.createElement('span');
        item.className = `ara-chart-legend-item ara-chart-legend-item--${idx + 1}`;
        item.textContent = s.label;
        const latestLabel = xLabels[s.values.length - 1] || `point ${s.values.length}`;
        setAraTooltip(item, s.label, `latest ${formatUnitValue(s.values[s.values.length - 1], yUnit)} (${latestLabel})`);
        legend.appendChild(item);
      });
      el.appendChild(legend);
    }
    el.dataset.rendered = '1';
  }
}

/** Donut chart with side legend. Author writes data-labels + data-values. */
function renderDonuts(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-donut');
  for (const el of els) {
    if (el.dataset.rendered === '1') continue;
    const labels = parseLabels(el.dataset.labels, 8);
    const values = parseSeries(el.dataset.values, 8);
    if (!values.length || labels.length !== values.length) continue;
    const total = values.reduce((a, b) => a + b, 0);
    if (total <= 0) continue;

    // Donut share formatting: keep one-decimal precision but drop a trailing
    // ".0" so whole-number shares read "66%" not "66.0%". round-then-reparse
    // also absorbs IEEE754 noise (0.66*100 -> 66.00000000000001).
    const fmtShare = (share: number): string => `${parseFloat(share.toFixed(1))}%`;

    const size = 200;
    const cx = size / 2;
    const cy = size / 2;
    const ro = 88;
    const ri = 56;
    const centerLabel = el.dataset.centerLabel || '';

    el.textContent = '';
    const svgWrap = document.createElement('div');
    const svg = svgEl<SVGSVGElement>('svg', { viewBox: `0 0 ${size} ${size}` });

    let acc = 0;
    values.forEach((v, idx) => {
      const start = (acc / total) * Math.PI * 2 - Math.PI / 2;
      acc += v;
      const end = (acc / total) * Math.PI * 2 - Math.PI / 2;
      const largeArc = end - start > Math.PI ? 1 : 0;
      const sx = cx + ro * Math.cos(start);
      const sy = cy + ro * Math.sin(start);
      const ex = cx + ro * Math.cos(end);
      const ey = cy + ro * Math.sin(end);
      const sxi = cx + ri * Math.cos(end);
      const syi = cy + ri * Math.sin(end);
      const exi = cx + ri * Math.cos(start);
      const eyi = cy + ri * Math.sin(start);
      const d =
        `M${sx.toFixed(2)},${sy.toFixed(2)}` +
        ` A${ro},${ro} 0 ${largeArc},1 ${ex.toFixed(2)},${ey.toFixed(2)}` +
        ` L${sxi.toFixed(2)},${syi.toFixed(2)}` +
        ` A${ri},${ri} 0 ${largeArc},0 ${exi.toFixed(2)},${eyi.toFixed(2)}` +
        ' Z';
      const slice = svgEl<SVGPathElement>('path', {
        class: `ara-donut-slice ara-donut-slice--${(idx % 6) + 1}`,
        d,
        tabindex: '0',
      });
      const pct = fmtShare((values[idx] / total) * 100);
      appendSvgTitle(slice, `${labels[idx]}: ${values[idx]} (${pct})`);
      setAraTooltip(slice, labels[idx], `${values[idx]} (${pct})`);
      svg.appendChild(slice);
    });

    if (centerLabel.trim()) {
      // Conservative usable width: 85% of the donut hole diameter to leave
      // breathing room from the slices. ri = 56 → hole = 112 → usable = ~95.
      const usableWidth = ri * 2 * 0.85;
      const wrapped = wrapDonutCenterLabel(centerLabel, 18, 9, usableWidth, 3);
      if (wrapped.lines.length === 1) {
        // 1-line. Two sub-cases:
        //   - At max font (18): use the original y = cy + 1 nudge to keep
        //     short labels like "2024" bit-identical to the pre-fix output.
        //   - Below max font (single oversize token, e.g. "Verylongunhyphenatedword"):
        //     respect the shrunk font and center at cy. Without this branch
        //     the shrink fallback would be silently discarded and the label
        //     would still overflow the donut hole.
        const fs = wrapped.fontSize;
        const atMax = fs >= 18;
        const text = svgEl<SVGTextElement>('text', {
          class: 'ara-donut-center-label',
          x: cx,
          y: atMax ? cy + 1 : cy,
          'font-size': atMax ? '18' : fs.toFixed(2),
        });
        text.textContent = wrapped.lines[0];
        svg.appendChild(text);
      } else if (wrapped.lines.length > 1) {
        // Multi-line: center the block vertically around cy. With
        // dominant-baseline: middle (from CSS), each tspan's y is its
        // vertical center. Stack lines with lineHeight = fontSize * 1.1.
        const fs = wrapped.fontSize;
        const lineHeight = fs * 1.1;
        const firstY = cy - ((wrapped.lines.length - 1) * lineHeight) / 2;
        const text = svgEl<SVGTextElement>('text', {
          class: 'ara-donut-center-label',
          x: cx,
          y: firstY,
          'font-size': String(fs.toFixed(2)),
        });
        wrapped.lines.forEach((line, i) => {
          const tspan = svgEl<SVGTSpanElement>('tspan', {
            x: cx,
            y: (firstY + i * lineHeight).toFixed(2),
          });
          tspan.textContent = line;
          text.appendChild(tspan);
        });
        svg.appendChild(text);
      }
    }
    svgWrap.appendChild(svg);
    el.appendChild(svgWrap);

    const legend = document.createElement('ul');
    legend.className = 'ara-donut-legend';
    labels.forEach((label, idx) => {
      const li = document.createElement('li');
      const swatch = document.createElement('span');
      swatch.className = `ara-donut-legend-swatch ara-donut-legend-swatch--${(idx % 6) + 1}`;
      const name = document.createElement('span');
      name.textContent = label;
      const value = document.createElement('span');
      value.className = 'ara-donut-legend-value';
      const pctText = fmtShare((values[idx] / total) * 100);
      value.textContent = pctText;
      li.title = `${label}: ${values[idx]} (${pctText})`;
      setAraTooltip(li, label, `${values[idx]} (${pctText})`);
      li.appendChild(swatch);
      li.appendChild(name);
      li.appendChild(value);
      legend.appendChild(li);
    });
    el.appendChild(legend);
    el.dataset.rendered = '1';
  }
}

/** In-place bounded anti-overlap. Sort items by current Y, walk top-down to
 * push colliders down by `lineHeight`, then if the bottommost item exceeds
 * `maxY` clamp it and walk back up pushing earlier items higher to make room.
 * Mutates the input array.
 *
 * Properties:
 * - Stable: items that don't overlap keep their original positions, so
 *   comfortable slope charts render pixel-identically to before this pass.
 * - Bounded: no item ends up below `maxY`, so labels can't get clipped by
 *   the SVG viewBox even when many values cluster at the bottom of the chart.
 *   (Bottom-bound only; the symmetric top-clip case would need yTop and
 *   doesn't trigger for any real data we render today.) */
function antiOverlap(positions: number[], lineHeight: number, maxY: number): void {
  if (positions.length < 2) return;
  const order = positions.map((_, i) => i).sort((a, b) => positions[a] - positions[b]);
  // Forward sweep: push each colliding label down by lineHeight.
  for (let j = 1; j < order.length; j++) {
    const prev = positions[order[j - 1]];
    const cur = positions[order[j]];
    if (cur - prev < lineHeight) {
      positions[order[j]] = prev + lineHeight;
    }
  }
  // Backward sweep: if the bottommost label overflows the viewport, clamp it
  // and push preceding labels up only as far as needed to keep `lineHeight`
  // between them. The clamp shrinks the gap from `lineHeight` toward zero
  // (labels can still overlap if too many cluster at the very bottom) but
  // keeps every label inside the SVG so nothing disappears.
  const last = order.length - 1;
  if (positions[order[last]] > maxY) {
    positions[order[last]] = maxY;
    for (let j = last - 1; j >= 0; j--) {
      const below = positions[order[j + 1]];
      if (positions[order[j]] > below - lineHeight) {
        positions[order[j]] = below - lineHeight;
      } else {
        // No more pressure to push; everything above is already clear.
        break;
      }
    }
  }
}

/** Two-period slopegraph. data-items, data-left-values, data-right-values,
 * data-left-label, data-right-label. Lines colored green/red by direction. */
function renderSlopes(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-slope');
  for (const el of els) {
    if (el.dataset.rendered === '1') continue;
    const items = parseLabels(el.dataset.items, 12);
    const leftValues = parseSeries(el.dataset.leftValues, 12);
    const rightValues = parseSeries(el.dataset.rightValues, 12);
    if (!items.length || items.length !== leftValues.length || items.length !== rightValues.length) continue;
    const leftLabel = el.dataset.leftLabel || 'Left';
    const rightLabel = el.dataset.rightLabel || 'Right';
    const unit = el.dataset.unit || '';

    const W = 960;
    const rowH = 26;
    const headerH = 30;
    const H = headerH + items.length * rowH + 20;
    const leftTexts = items.map((name, i) => `${name} ${formatUnitValue(leftValues[i], unit)}`);
    const rightTexts = items.map((name, i) => `${formatUnitValue(rightValues[i], unit)} ${name}`);
    const maxLeftW = Math.max(...leftTexts.map((text) => approxSvgTextWidth(text, 12)));
    const maxRightW = Math.max(...rightTexts.map((text) => approxSvgTextWidth(text, 12)));
    const minPlotW = 180;
    const maxSideW = Math.floor((W - minPlotW) / 2) - 18;
    const leftW = Math.min(maxSideW, Math.max(130, Math.ceil(maxLeftW)));
    const rightW = Math.min(maxSideW, Math.max(130, Math.ceil(maxRightW)));
    const colL = leftW + 14;
    const colR = W - rightW - 14;

    const all = [...leftValues, ...rightValues];
    const min = Math.min(...all);
    const max = Math.max(...all);
    const range = max - min || 1;
    const yTop = headerH + 10;
    const yBot = H - 14;
    const yFor = (v: number) => yBot - ((v - min) / range) * (yBot - yTop);

    el.textContent = '';
    const svg = svgEl<SVGSVGElement>('svg', { viewBox: `0 0 ${W} ${H}` });

    // Headers
    const lh = svgEl<SVGTextElement>('text', { class: 'ara-slope-header', x: colL, y: 18, 'text-anchor': 'end' });
    lh.textContent = leftLabel;
    svg.appendChild(lh);
    const rh = svgEl<SVGTextElement>('text', { class: 'ara-slope-header', x: colR, y: 18, 'text-anchor': 'start' });
    rh.textContent = rightLabel;
    svg.appendChild(rh);

    // Pass 1: compute dot Y for each item and the desired label Y (baseline + 4
    // so the text visually centers on the dot for 12px font).
    const lys = items.map((_, i) => yFor(leftValues[i]));
    const rys = items.map((_, i) => yFor(rightValues[i]));
    const labelLY = lys.map((y) => y + 4);
    const labelRY = rys.map((y) => y + 4);

    // Pass 2: anti-overlap each side independently. Dots stay at lys/rys; only
    // label Y positions get nudged when two values would collide. `maxLabelY`
    // keeps the descender of a 12px label inside the SVG viewBox so the pass
    // never clips a label off the bottom.
    const lineHeight = 14; // 12px font + ~2px breathing room.
    const maxLabelY = H - 4; // ~3px below the baseline is where the descender ends.
    antiOverlap(labelLY, lineHeight, maxLabelY);
    antiOverlap(labelRY, lineHeight, maxLabelY);

    items.forEach((_, i) => {
      const lv = leftValues[i];
      const rv = rightValues[i];
      const ly = lys[i];
      const ry = rys[i];
      const direction = rv > lv ? 'up' : rv < lv ? 'down' : 'flat';
      const delta = rv - lv;
      const pctChange = lv !== 0 ? ` · ${formatSignedNumber((delta / Math.abs(lv)) * 100, 1)}%` : '';
      const tooltipBody =
        `${leftLabel}: ${formatUnitValue(lv, unit)} -> ${rightLabel}: ${formatUnitValue(rv, unit)}` +
        ` · change ${formatSignedUnitValue(delta, unit)}${pctChange}`;
      const line = svgEl<SVGLineElement>('line', {
        class: `ara-slope-line ${direction !== 'flat' ? `ara-slope-line--${direction}` : ''}`.trim(),
        x1: colL + 6,
        y1: ly,
        x2: colR - 6,
        y2: ry,
      });
      svg.appendChild(line);
      const hit = svgEl<SVGLineElement>('line', {
        class: 'ara-slope-hit',
        x1: colL + 6,
        y1: ly,
        x2: colR - 6,
        y2: ry,
      });
      setAraTooltip(hit, items[i], tooltipBody);
      svg.appendChild(hit);
      const leftDot = svgEl('circle', { class: 'ara-slope-dot', cx: colL + 6, cy: ly, r: 3 });
      setAraTooltip(leftDot, items[i], `${leftLabel}: ${formatUnitValue(lv, unit)}`);
      svg.appendChild(leftDot);
      const rightDot = svgEl('circle', { class: 'ara-slope-dot', cx: colR - 6, cy: ry, r: 3 });
      setAraTooltip(rightDot, items[i], `${rightLabel}: ${formatUnitValue(rv, unit)}`);
      svg.appendChild(rightDot);
      const lRaw = leftTexts[i];
      const lLabel = svgEl<SVGTextElement>('text', { class: 'ara-slope-label', x: colL - 8, y: labelLY[i], 'text-anchor': 'end' });
      lLabel.textContent = fitSvgText(lRaw, colL - 8, 12);
      if (lLabel.textContent !== lRaw) setSvgFullLabel(lLabel, lRaw);
      setAraTooltip(lLabel, items[i], `${leftLabel}: ${formatUnitValue(lv, unit)}`);
      svg.appendChild(lLabel);
      const rRaw = rightTexts[i];
      const rLabel = svgEl<SVGTextElement>('text', { class: 'ara-slope-label', x: colR + 8, y: labelRY[i], 'text-anchor': 'start' });
      rLabel.textContent = fitSvgText(rRaw, W - colR - 8, 12);
      if (rLabel.textContent !== rRaw) setSvgFullLabel(rLabel, rRaw);
      setAraTooltip(rLabel, items[i], `${rightLabel}: ${formatUnitValue(rv, unit)}`);
      svg.appendChild(rLabel);
    });

    el.appendChild(svg);
    el.dataset.rendered = '1';
  }
}

/** Nice-number rounded tick marks across [min, max].
 *
 * Returns an evenly-spaced ascending list of "round" values (steps of
 * 1/2/5 × 10^k) that bracket the domain — niceTicks[0] <= min and the
 * last entry >= max. Because the chart always passes a domain that
 * includes 0 (bars originate from a zero baseline), and 0 is a multiple
 * of every step, the returned ticks always include 0 when the domain
 * spans it. Used for both the value axis labels and gridline positions. */
function niceTicks(min: number, max: number, maxTicks = 6): number[] {
  if (!Number.isFinite(min) || !Number.isFinite(max)) return [0, 1];
  if (min === max) {
    // Degenerate domain (e.g. all-zero series). Give a tiny symmetric range.
    if (min === 0) return [0, 1];
    min = Math.min(0, min);
    max = Math.max(0, max);
    if (min === max) return [min, min + 1];
  }
  const range = max - min;
  const rawStep = range / Math.max(1, maxTicks - 1);
  const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
  const norm = rawStep / mag;
  let niceNorm: number;
  if (norm < 1.5) niceNorm = 1;
  else if (norm < 3) niceNorm = 2;
  else if (norm < 7) niceNorm = 5;
  else niceNorm = 10;
  const step = niceNorm * mag;
  const niceMin = Math.floor(min / step) * step;
  const niceMax = Math.ceil(max / step) * step;
  const ticks: number[] = [];
  // Build with integer arithmetic on step counts to dodge float drift
  // (e.g. 0.1 + 0.2 != 0.3); the last push guards against the loop
  // missing niceMax by an epsilon.
  const count = Math.round((niceMax - niceMin) / step);
  for (let i = 0; i <= count; i++) {
    ticks.push(niceMin + i * step);
  }
  return ticks;
}

/** Bar / column chart with a real numeric value axis. Authored markup is
 * one empty <div class="ara-bar-chart" data-*> (the writer's tag allowlist
 * rejects <svg> in fragments) — we inject the SVG here. Supports:
 *   - vertical stacked / grouped columns
 *   - horizontal diverging bars (signed values around a zero baseline)
 *   - plain horizontal/vertical single-series bars
 * data-series-N use digit suffixes, so they are read with getAttribute
 * (data-series-1 does NOT map to dataset.series1). */
function renderBarCharts(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-bar-chart');
  for (const el of els) {
    if (el.dataset.rendered === '1') continue;

    const seriesList: Array<{ values: number[]; label: string }> = [];
    for (let i = 1; i <= 6; i++) {
      const v = parseSeries(el.getAttribute(`data-series-${i}`) || undefined, 200);
      if (!v.length) continue;
      const label = el.getAttribute(`data-series-${i}-label`) || `Series ${i}`;
      seriesList.push({ values: v, label });
    }
    if (!seriesList.length) continue;

    const categories = parseLabels(el.dataset.categories, 200);
    if (!categories.length) continue;
    const N = categories.length;
    // Clamp every series to the category count so a mismatched author
    // attr can't read past the slot array (compiler already enforces
    // equality, but the renderer must not trust that).
    for (const s of seriesList) {
      if (s.values.length < N) {
        while (s.values.length < N) s.values.push(0);
      } else if (s.values.length > N) {
        s.values = s.values.slice(0, N);
      }
    }

    const orientation = el.dataset.orientation === 'horizontal' ? 'horizontal' : 'vertical';
    const mode = el.dataset.mode || (seriesList.length > 1 ? 'grouped' : 'simple');
    const prefix = el.dataset.unit || '';
    const suffix = el.dataset.valueSuffix || '';
    const title = el.dataset.title || '';
    const subtitle = el.dataset.subtitle || '';
    const isStacked = mode === 'stacked' && seriesList.length > 1;
    const isGrouped = mode === 'grouped' && seriesList.length > 1;

    // Value formatter: signed prefix + abs value (grouped thousands) + suffix.
    // e.g. -8000 with prefix "$" suffix "M" → "-$8,000M".
    const fmt = (v: number): string => {
      const sign = v < 0 ? '-' : '';
      return sign + prefix + Math.abs(v).toLocaleString('en-US', { maximumFractionDigits: 2 }) + suffix;
    };

    // ── Value-axis domain ────────────────────────────────────────────
    // stacked: per-category total (all >=0 by validation) → [0, maxTotal].
    // grouped/simple: every individual value, ALWAYS including zero so bars
    // originate from a zero baseline.
    let domainMin: number;
    let domainMax: number;
    if (isStacked) {
      const totals = categories.map((_, ci) =>
        seriesList.reduce((acc, s) => acc + s.values[ci], 0),
      );
      domainMin = 0;
      domainMax = Math.max(0, ...totals);
    } else {
      const allValues = seriesList.flatMap((s) => s.values);
      domainMin = Math.min(0, ...allValues);
      domainMax = Math.max(0, ...allValues);
    }
    const ticks = niceTicks(domainMin, domainMax, 6);
    const niceMin = ticks[0];
    const niceMax = ticks[ticks.length - 1];
    const valRange = niceMax - niceMin || 1;

    el.textContent = '';
    if (title) {
      const t = document.createElement('p');
      t.className = 'ara-bar-chart-title';
      t.textContent = title;
      el.appendChild(t);
    }
    if (subtitle) {
      const s = document.createElement('p');
      s.className = 'ara-bar-chart-subtitle';
      s.textContent = subtitle;
      el.appendChild(s);
    }

    const colorClass = (catIdx: number, seriesIdx: number): string => {
      // multi-series → color by series; single → color by category.
      const n = seriesList.length > 1 ? seriesIdx + 1 : (catIdx % 6) + 1;
      return `ara-bar-chart-bar ara-bar-chart-bar--${n}`;
    };

    let svg: SVGSVGElement;

    if (orientation === 'vertical') {
      // Columns: value axis on Y (left), categories along X (bottom).
      const W = 640;
      const H = 300;
      const MT = 12;
      const MB = 34;
      const MR = 16;
      const tickLabels = ticks.map((t) => fmt(t));
      const maxTickW = Math.max(...tickLabels.map((t) => approxSvgTextWidth(t, 10, true)));
      const ML = Math.min(140, Math.max(44, Math.ceil(maxTickW) + 10));
      const innerW = W - ML - MR;
      const innerH = H - MT - MB;
      const yFor = (v: number) => MT + innerH - ((v - niceMin) / valRange) * innerH;
      const slotW = innerW / N;

      svg = svgEl<SVGSVGElement>('svg', {
        viewBox: `0 0 ${W} ${H}`,
        preserveAspectRatio: 'xMidYMid meet',
        role: 'img',
        'aria-label': `${title || 'Bar chart'}: hover bars for values`,
      });

      // Gridlines + value tick labels.
      for (let i = 0; i < ticks.length; i++) {
        const y = yFor(ticks[i]);
        svg.appendChild(svgEl('line', { class: 'ara-chart-grid', x1: ML, y1: y, x2: W - MR, y2: y }));
        const lab = svgEl<SVGTextElement>('text', { class: 'ara-chart-tick-label', x: ML - 6, y: y + 3, 'text-anchor': 'end' });
        lab.textContent = tickLabels[i];
        svg.appendChild(lab);
      }
      // Emphasized zero baseline (coincides with axis edge when all-positive).
      const yZero = yFor(0);
      svg.appendChild(svgEl('line', { class: 'ara-bar-chart-baseline', x1: ML, y1: yZero, x2: W - MR, y2: yZero }));

      // Sparse category labels if crowded.
      const labelStep = N > 8 ? Math.ceil(N / 8) : 1;

      categories.forEach((cat, ci) => {
        const slotX = ML + ci * slotW;
        if (isStacked) {
          // Accumulate segments upward from baseline (all values >= 0).
          let posTop = 0; // running total above baseline
          const barW = slotW * 0.6;
          const barX = slotX + (slotW - barW) / 2;
          seriesList.forEach((s, si) => {
            const v = s.values[ci];
            const segTopVal = posTop + v;
            const yTop = yFor(segTopVal);
            const yBot = yFor(posTop);
            const h = Math.abs(yBot - yTop);
            const rect = svgEl<SVGRectElement>('rect', {
              class: colorClass(ci, si),
              x: barX,
              y: Math.min(yTop, yBot),
              width: barW,
              height: h,
            });
            appendSvgTitle(rect, `${s.label} · ${cat}: ${fmt(v)}`);
            setAraTooltip(rect, `${s.label} · ${cat}`, fmt(v));
            svg.appendChild(rect);
            posTop = segTopVal;
          });
        } else if (isGrouped) {
          // N series bars side-by-side within the slot.
          const groupPad = slotW * 0.12;
          const bandW = slotW - groupPad * 2;
          const barW = bandW / seriesList.length;
          seriesList.forEach((s, si) => {
            const v = s.values[ci];
            const barX = slotX + groupPad + si * barW;
            const yVal = yFor(v);
            const yTop = Math.min(yVal, yZero);
            const h = Math.abs(yZero - yVal);
            const rect = svgEl<SVGRectElement>('rect', {
              class: colorClass(ci, si),
              x: barX + 0.5,
              y: yTop,
              width: Math.max(0, barW - 1),
              height: h,
            });
            appendSvgTitle(rect, `${s.label} · ${cat}: ${fmt(v)}`);
            setAraTooltip(rect, `${s.label} · ${cat}`, fmt(v));
            svg.appendChild(rect);
          });
        } else {
          // simple: one bar per slot, centered.
          const v = seriesList[0].values[ci];
          const barW = slotW * 0.6;
          const barX = slotX + (slotW - barW) / 2;
          const yVal = yFor(v);
          const yTop = Math.min(yVal, yZero);
          const h = Math.abs(yZero - yVal);
          const rect = svgEl<SVGRectElement>('rect', {
            class: colorClass(ci, 0),
            x: barX,
            y: yTop,
            width: barW,
            height: h,
          });
          appendSvgTitle(rect, `${cat}: ${fmt(v)}`);
          setAraTooltip(rect, cat, fmt(v));
          svg.appendChild(rect);
        }

        // Category label under the slot (centered), sparse if crowded.
        if (ci % labelStep === 0) {
          const raw = cat;
          const fitted = fitSvgText(raw, slotW * (labelStep > 1 ? labelStep : 1) - 4, 10);
          const lab = svgEl<SVGTextElement>('text', {
            class: 'ara-chart-tick-label',
            x: slotX + slotW / 2,
            y: H - 12,
            'text-anchor': 'middle',
          });
          lab.textContent = fitted;
          if (fitted !== raw) setSvgFullLabel(lab, raw);
          svg.appendChild(lab);
        }
      });

      el.appendChild(svg);
    } else {
      // Horizontal bars: value axis along X (bottom), categories as Y rows.
      const W = 640;
      const rowH = 40;
      const MT = 12;
      const MB = 30;
      const MR = 18;
      const tickLabels = ticks.map((t) => fmt(t));
      const maxCatW = Math.max(...categories.map((c) => approxSvgTextWidth(c, 12)));
      const ML = Math.min(220, Math.max(60, Math.ceil(maxCatW) + 14));
      const H = MT + N * rowH + MB;
      const innerW = W - ML - MR;
      const innerH = N * rowH;
      const xFor = (v: number) => ML + ((v - niceMin) / valRange) * innerW;

      svg = svgEl<SVGSVGElement>('svg', {
        viewBox: `0 0 ${W} ${H}`,
        preserveAspectRatio: 'xMidYMid meet',
        role: 'img',
        'aria-label': `${title || 'Bar chart'}: hover bars for values`,
      });

      // Vertical gridlines + value tick labels along the bottom.
      for (let i = 0; i < ticks.length; i++) {
        const x = xFor(ticks[i]);
        svg.appendChild(svgEl('line', { class: 'ara-chart-grid', x1: x, y1: MT, x2: x, y2: MT + innerH }));
        const lab = svgEl<SVGTextElement>('text', { class: 'ara-chart-tick-label', x, y: H - 12, 'text-anchor': 'middle' });
        lab.textContent = tickLabels[i];
        svg.appendChild(lab);
      }
      // Emphasized zero baseline (vertical).
      const xZero = xFor(0);
      svg.appendChild(svgEl('line', { class: 'ara-bar-chart-baseline', x1: xZero, y1: MT, x2: xZero, y2: MT + innerH }));

      categories.forEach((cat, ci) => {
        const rowY = MT + ci * rowH;
        if (isStacked) {
          let posRight = 0; // running total (all >= 0)
          const barH = rowH * 0.6;
          const barY = rowY + (rowH - barH) / 2;
          seriesList.forEach((s, si) => {
            const v = s.values[ci];
            const xStart = xFor(posRight);
            const xEnd = xFor(posRight + v);
            const w = Math.abs(xEnd - xStart);
            const rect = svgEl<SVGRectElement>('rect', {
              class: colorClass(ci, si),
              x: Math.min(xStart, xEnd),
              y: barY,
              width: w,
              height: barH,
            });
            appendSvgTitle(rect, `${s.label} · ${cat}: ${fmt(v)}`);
            setAraTooltip(rect, `${s.label} · ${cat}`, fmt(v));
            svg.appendChild(rect);
            posRight += v;
          });
        } else if (isGrouped) {
          const groupPad = rowH * 0.12;
          const bandH = rowH - groupPad * 2;
          const barH = bandH / seriesList.length;
          seriesList.forEach((s, si) => {
            const v = s.values[ci];
            const barY = rowY + groupPad + si * barH;
            const xVal = xFor(v);
            const xStart = Math.min(xVal, xZero);
            const w = Math.abs(xVal - xZero);
            const rect = svgEl<SVGRectElement>('rect', {
              class: colorClass(ci, si),
              x: xStart,
              y: barY + 0.5,
              width: w,
              height: Math.max(0, barH - 1),
            });
            appendSvgTitle(rect, `${s.label} · ${cat}: ${fmt(v)}`);
            setAraTooltip(rect, `${s.label} · ${cat}`, fmt(v));
            svg.appendChild(rect);
          });
        } else {
          const v = seriesList[0].values[ci];
          const barH = rowH * 0.6;
          const barY = rowY + (rowH - barH) / 2;
          const xVal = xFor(v);
          const xStart = Math.min(xVal, xZero);
          const w = Math.abs(xVal - xZero);
          const rect = svgEl<SVGRectElement>('rect', {
            class: colorClass(ci, 0),
            x: xStart,
            y: barY,
            width: w,
            height: barH,
          });
          appendSvgTitle(rect, `${cat}: ${fmt(v)}`);
          setAraTooltip(rect, cat, fmt(v));
          svg.appendChild(rect);
        }

        // Right-aligned category label in the left margin, vertically centered.
        const raw = cat;
        const fitted = fitSvgText(raw, ML - 10, 12);
        const lab = svgEl<SVGTextElement>('text', {
          class: 'ara-chart-tick-label',
          x: ML - 8,
          y: rowY + rowH / 2 + 4,
          'text-anchor': 'end',
        });
        lab.textContent = fitted;
        if (fitted !== raw) setSvgFullLabel(lab, raw);
        svg.appendChild(lab);
      });

      el.appendChild(svg);
    }

    // Legend (only for multi-series). Reuses the line-chart legend item
    // swatch pattern; scoped CSS gives the bar-chart its own block fill.
    if (seriesList.length > 1) {
      const legend = document.createElement('div');
      legend.className = 'ara-bar-chart-legend';
      seriesList.forEach((s, idx) => {
        const item = document.createElement('span');
        item.className = `ara-chart-legend-item ara-chart-legend-item--${idx + 1}`;
        item.textContent = s.label;
        const total = s.values.reduce((acc, value) => acc + value, 0);
        setAraTooltip(item, s.label, `${N} categories · total ${fmt(total)}`);
        legend.appendChild(item);
      });
      el.appendChild(legend);
    }

    el.dataset.rendered = '1';
  }
}

/** Wrap each bare `.ara-table` in a `.ara-table-wrap` div so wide tables
 * scroll horizontally on narrow viewports instead of pushing the page
 * wider than the viewport. Done in JS (not in the article's HTML) so
 * existing fragments don't need to be rewritten. Counterpart to wrapTables()
 * above, which handles markdown-rendered tables for non-research tabs. */
function wrapAraTables(root: HTMLElement): void {
  const tables = root.querySelectorAll<HTMLTableElement>('.ara-table');
  for (const t of tables) {
    const parent = t.parentElement;
    if (!parent || parent.classList.contains('ara-table-wrap')) continue;
    const wrap = document.createElement('div');
    wrap.className = 'ara-table-wrap';
    parent.insertBefore(wrap, t);
    wrap.appendChild(t);
  }
}

/** Read every `data-pct` and stamp `--ara-bar-pct: <n>%` on the element so
 * the bar / stacked-segment CSS picks up the value. Avoids inline style=
 * in authored articles. */
function applyBarFills(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('[data-pct]');
  for (const el of els) {
    const raw = el.dataset.pct;
    if (!raw) continue;
    const n = Number(raw);
    if (!Number.isFinite(n)) continue;
    const clamped = Math.max(0, Math.min(100, n));
    el.style.setProperty('--ara-bar-pct', clamped + '%');
  }
}

let tocScrollHandler: ((e: Event) => void) | null = null;

export function hideResearchTOC(): void {
  const toc = document.getElementById('researchToc');
  if (toc) toc.hidden = true;
  document.body.classList.remove('has-toc');
  if (tocScrollHandler) {
    window.removeEventListener('scroll', tocScrollHandler);
    tocScrollHandler = null;
  }
}

function tocSlug(text: string): string {
  return text.toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48) || 'section';
}

/** Walk the article for `<h3 class="ara-h2">` (section heads) and
 * `<h4 class="ara-h3">` (subsections), assign IDs if missing, and build
 * a floating TOC in #researchToc. Sets up a passive scroll listener for
 * active-section highlighting. Hides if fewer than three sections. */
function renderResearchTOC(article: HTMLElement): void {
  const toc = document.getElementById('researchToc');
  const list = document.getElementById('researchTocList');
  if (!toc || !list) return;

  while (list.firstChild) list.removeChild(list.firstChild);

  const heads = Array.from(
    article.querySelectorAll<HTMLElement>(
      'h2.ara-h2, h3.ara-h2, h4.ara-h2, h2.ara-h3, h3.ara-h3, h4.ara-h3',
    ),
  );
  // Skip the article's display title — only section heads.
  if (heads.length < 3) {
    hideResearchTOC();
    return;
  }

  const links: HTMLAnchorElement[] = [];
  for (const h of heads) {
    if (!h.id) {
      const num = h.querySelector('.ara-h2-num');
      const rawText = (h.textContent || '').replace(num?.textContent || '', '').trim();
      h.id = tocSlug(rawText);
    }
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.className = 'ara-toc-link';
    a.href = '#' + h.id;
    if (h.classList.contains('ara-h3')) li.style.paddingLeft = '14px';
    const num = h.querySelector('.ara-h2-num');
    const restText = (h.textContent || '').replace(num?.textContent || '', '').trim();
    a.textContent = restText;
    // CSS clips overflow with ellipsis; surface the full title on hover.
    a.title = restText;
    a.dataset.target = h.id;
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const t = document.getElementById(a.dataset.target!);
      if (t) {
        // Push the fragment into the URL so users can copy/share the
        // section-level deep link directly from the address bar.
        history.pushState(null, '', '#' + a.dataset.target);
        t.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
    li.appendChild(a);
    list.appendChild(li);
    links.push(a);
  }
  toc.hidden = false;
  document.body.classList.add('has-toc');

  // Scroll-spy: the last heading whose top is above an offset is "current".
  if (tocScrollHandler) window.removeEventListener('scroll', tocScrollHandler);
  const OFFSET = 120;
  const onScroll = () => {
    let activeIndex = 0;
    for (let i = 0; i < heads.length; i++) {
      if (heads[i].getBoundingClientRect().top - OFFSET < 0) activeIndex = i;
      else break;
    }
    for (let i = 0; i < links.length; i++) {
      links[i].classList.toggle('active', i === activeIndex);
    }
  };
  tocScrollHandler = onScroll;
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/** Attach a small `#` anchor button to every section / subsection heading
 * that already has an id (renderResearchTOC assigns them). Clicking it
 * copies the deep link to the clipboard and updates the address bar so the
 * user can paste the URL anywhere. Cmd/Ctrl-click opens in a new tab via
 * the browser's default anchor behavior. */
function addSectionAnchors(article: HTMLElement): void {
  const heads = article.querySelectorAll<HTMLElement>(
    'h2.ara-h2, h3.ara-h2, h4.ara-h2, h2.ara-h3, h3.ara-h3, h4.ara-h3',
  );
  for (const h of heads) {
    if (!h.id || h.querySelector('.ara-anchor')) continue;
    const a = document.createElement('a');
    a.className = 'ara-anchor';
    a.href = '#' + h.id;
    a.title = 'Copy link to this section';
    a.setAttribute('aria-label', 'Copy link to this section');
    a.textContent = '#';
    h.appendChild(a);
    a.addEventListener('click', (e) => {
      // Honor open-in-new-tab modifiers — let the browser handle them.
      if (e.metaKey || e.ctrlKey || e.shiftKey || (e as MouseEvent).button === 1) return;
      e.preventDefault();
      history.pushState(null, '', '#' + h.id);
      h.scrollIntoView({ behavior: 'smooth', block: 'start' });
      const url = location.origin + location.pathname + '#' + h.id;
      copyTextToClipboard(url).then(() => {
        a.classList.add('ara-anchor--copied');
        window.setTimeout(() => a.classList.remove('ara-anchor--copied'), 1400);
      }).catch(() => {
        // Silent — the URL is still in the address bar, user can copy from there.
      });
    });
  }
}

/** Clipboard write with a non-secure-context fallback so this works on
 * localhost over plain HTTP and other edge environments. */
function copyTextToClipboard(text: string): Promise<void> {
  if (navigator.clipboard?.writeText) {
    return navigator.clipboard.writeText(text);
  }
  return new Promise((resolve, reject) => {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      resolve();
    } catch (err) {
      reject(err);
    } finally {
      ta.remove();
    }
  });
}

/** After the article renders, if the URL has a fragment, scroll to the
 * matching element. Runs in rAF so layout (chart sizing, isotype expansion,
 * table wrapping) has settled before we measure scroll positions. */
export function scrollToHashIfPresent(): void {
  if (!location.hash) return;
  const id = decodeURIComponent(location.hash.slice(1));
  if (!id) return;
  const t = document.getElementById(id);
  if (!t) return;
  requestAnimationFrame(() => {
    t.scrollIntoView({ behavior: 'auto', block: 'start' });
  });
}

export function enhanceAraVisuals(root: HTMLElement): void {
  applyBarFills(root);
  wrapAraTables(root);
  renderSparklines(root);
  renderLineCharts(root);
  renderDonuts(root);
  renderSlopes(root);
  renderTradingView(root);
  renderBarCharts(root);
}

export function enhanceAraArticle(article: HTMLElement): void {
  applyBarFills(article);
  wrapAraTables(article);
  prepareAraFigures(article);
  applyIsotypes(article);
  renderSparklines(article);
  renderLineCharts(article);
  renderDonuts(article);
  renderSlopes(article);
  renderTradingView(article);
  renderBarCharts(article);
  applyAraTooltips(article);
  renderResearchTOC(article);
  addSectionAnchors(article);
  scrollToHashIfPresent();
}
