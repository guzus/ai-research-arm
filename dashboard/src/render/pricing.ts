/**
 * Price vs. capability — the Pareto view over research/market/model-pricing.json.
 *
 * WHY A LOG X AXIS IS NOT A STYLE CHOICE
 * --------------------------------------
 * Output price spans roughly $0.03 to $180 per Mtok — nearly four orders of
 * magnitude. On a linear axis every model except the handful of premium tiers
 * collapses onto the left edge, which hides exactly the comparison the chart
 * exists to make. Log10 gives each 10x of price equal width, so "twice the
 * score for 1000x the price" is legible as distance.
 *
 * WHAT THE FRONTIER LINE MEANS
 * ----------------------------
 * It connects the non-dominated models: those where nothing else is both
 * cheaper and at least as good. Everything above/left of the line is
 * unreachable today; everything below/right is a model you would only pick for
 * a reason this chart does not show (latency, context, licence, availability).
 * The line is drawn as a STEP, not a smooth curve, because the intermediate
 * points are not purchasable — interpolating would imply products that do not
 * exist.
 */

import { uiText, type UiLanguage } from '../i18n';

export type PricedModel = {
  key: string;
  name: string;
  vendor: string;
  openrouter_id?: string | null;
  price_variant?: string | null;
  input_usd_per_mtok: number;
  output_usd_per_mtok: number;
  blended_usd_per_mtok?: number;
  context_length?: number | null;
  score: number;
  stderr?: number | null;
  score_variant?: string | null;
  score_as_of?: string | null;
  runs?: number;
  pareto?: boolean;
};

export type AlternatePoint = {
  key: string;
  name: string;
  vendor: string;
  output_usd_per_mtok: number;
  score: number;
  stderr?: number | null;
  pareto?: boolean;
};

export type ModelPricing = {
  generated_at: string;
  benchmark: string;
  stale?: boolean;
  capability_stale?: boolean;
  price_basis?: string;
  score_basis?: string;
  price_source?: string;
  price_source_url?: string;
  capability_source?: string;
  capability_source_url?: string;
  capability_license?: string;
  capability_attribution?: string;
  capability_tiers?: number[];
  benchmarks_available?: Record<string, number>;
  snapshot: {
    as_of: string;
    models: PricedModel[];
    alternates?: Record<string, AlternatePoint[]>;
    unscored?: Array<{ name: string; vendor: string; output_usd_per_mtok: number }>;
    counts?: Record<string, number>;
  };
  history?: Array<{
    ts: string;
    frontier_price_at?: Record<string, number | null>;
    plotted?: number;
    pareto?: number;
    best_score?: number | null;
  }>;
};

// Vendor colours. Deliberately a small fixed set with a neutral fallback:
// generating a hue per vendor produces near-duplicate colours once you pass a
// dozen vendors, which is worse than an honest "other".
// Hues are spread deliberately rather than taken from brand palettes: four
// vendors ship a nearly identical brand blue, and a legend with four blues is
// a legend that does not work.
const VENDOR_COLORS: Record<string, string> = {
  anthropic: '#d97757',   // terracotta
  openai: '#10a37f',      // emerald
  google: '#4285f4',      // blue
  deepseek: '#e11d48',    // rose
  'x-ai': '#a855f7',      // purple
  mistralai: '#f59e0b',   // amber
  qwen: '#ec4899',        // pink
  'z-ai': '#06b6d4',      // cyan
  moonshotai: '#78716c',  // stone
  'meta-llama': '#1d4ed8', // deep blue
  microsoft: '#84cc16',   // lime
};
const VENDOR_FALLBACK = '#94a3b8';

const VIEW_W = 1000;
const VIEW_H = 560;
const M = { top: 28, right: 28, bottom: 62, left: 62 };

/**
 * Escape for BOTH text and attribute contexts.
 *
 * Deliberately not shared.ts's `escapeHtml` (textContent -> innerHTML): that
 * round-trip escapes &, < and > but leaves quotes intact, so interpolating its
 * output into `attr="..."` lets a quote break out of the attribute. Every
 * string here is third-party — OpenRouter model names, Epoch benchmark task
 * names — and several land in `data-benchmark="..."` and `aria-label="..."`,
 * so quotes are escaped too.
 */
function esc(value: string): string {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** Only http(s) survives; anything else (javascript:, data:) becomes inert. */
function safeHref(url: string | undefined | null): string {
  if (!url) return '#';
  try {
    const parsed = new URL(url, window.location.origin);
    return parsed.protocol === 'https:' || parsed.protocol === 'http:' ? esc(parsed.href) : '#';
  } catch {
    return '#';
  }
}

function vendorColor(vendor: string): string {
  return VENDOR_COLORS[vendor] ?? VENDOR_FALLBACK;
}

function fmtPrice(value: number): string {
  if (value >= 100) return '$' + value.toFixed(0);
  if (value >= 1) return '$' + value.toFixed(2);
  return '$' + value.toFixed(3).replace(/0+$/, '').replace(/\.$/, '');
}

function fmtAge(iso: string, language: UiLanguage): string {
  const then = Date.parse(iso);
  if (!Number.isFinite(then)) return language === 'ko' ? '알 수 없음' : 'unknown';
  const mins = Math.max(0, Math.round((Date.now() - then) / 60000));
  if (mins < 60) return language === 'ko' ? mins + '분 전' : mins + 'm ago';
  const hours = Math.round(mins / 60);
  if (hours < 48) return language === 'ko' ? hours + '시간 전' : hours + 'h ago';
  return language === 'ko' ? Math.round(hours / 24) + '일 전' : Math.round(hours / 24) + 'd ago';
}

type Point = { x: number; y: number; model: AlternatePoint & Partial<PricedModel> };

/** Build the scale closures for one dataset. Log10 on price, linear on score. */
function makeScales(models: AlternatePoint[]) {
  const prices = models.map((m) => m.output_usd_per_mtok).filter((p) => p > 0);
  const scores = models.map((m) => m.score);
  const loMin = Math.log10(Math.min(...prices));
  const loMax = Math.log10(Math.max(...prices));
  // Pad by a tenth of a decade so edge points are not clipped by the axis.
  const x0 = Math.floor(loMin * 10) / 10 - 0.1;
  const x1 = Math.ceil(loMax * 10) / 10 + 0.1;
  const yMinRaw = Math.min(...scores);
  const y0 = Math.max(0, Math.floor(yMinRaw * 10) / 10 - 0.05);
  const y1 = Math.min(1, Math.ceil(Math.max(...scores) * 10) / 10 + 0.02);

  const plotW = VIEW_W - M.left - M.right;
  const plotH = VIEW_H - M.top - M.bottom;
  return {
    x0, x1, y0, y1, plotW, plotH,
    sx: (price: number) => M.left + ((Math.log10(price) - x0) / (x1 - x0)) * plotW,
    sy: (score: number) => M.top + plotH - ((score - y0) / (y1 - y0)) * plotH,
  };
}

function decadeTicks(x0: number, x1: number): number[] {
  const ticks: number[] = [];
  for (let e = Math.ceil(x0); e <= Math.floor(x1); e += 1) ticks.push(Math.pow(10, e));
  return ticks;
}

function scoreTicks(y0: number, y1: number): number[] {
  const ticks: number[] = [];
  const step = (y1 - y0) > 0.5 ? 0.2 : 0.1;
  for (let v = Math.ceil(y0 / step) * step; v <= y1 + 1e-9; v += step) {
    ticks.push(Math.round(v * 100) / 100);
  }
  return ticks;
}

function buildSvg(models: AlternatePoint[], benchmark: string, language: UiLanguage): string {
  if (models.length === 0) {
    return '<p class="pricing-empty">' + uiText(language, 'pricing.noData') + '</p>';
  }
  const s = makeScales(models);
  const points: Point[] = models.map((m) => ({
    x: s.sx(m.output_usd_per_mtok),
    y: s.sy(m.score),
    model: m,
  }));

  const gridX = decadeTicks(s.x0, s.x1).map((price) => {
    const x = s.sx(price);
    return (
      `<line class="pricing-grid" x1="${x.toFixed(1)}" y1="${M.top}" x2="${x.toFixed(1)}" y2="${VIEW_H - M.bottom}"/>` +
      `<text class="pricing-axis-label" x="${x.toFixed(1)}" y="${VIEW_H - M.bottom + 20}" text-anchor="middle">${fmtPrice(price)}</text>`
    );
  }).join('');

  const gridY = scoreTicks(s.y0, s.y1).map((score) => {
    const y = s.sy(score);
    return (
      `<line class="pricing-grid" x1="${M.left}" y1="${y.toFixed(1)}" x2="${VIEW_W - M.right}" y2="${y.toFixed(1)}"/>` +
      `<text class="pricing-axis-label" x="${M.left - 10}" y="${(y + 4).toFixed(1)}" text-anchor="end">${score.toFixed(1)}</text>`
    );
  }).join('');

  // Frontier: sort non-dominated points by price, then emit a step path.
  // Horizontal-then-vertical, because a cheaper model's score holds until the
  // next purchasable step up — a diagonal would imply blended products.
  const frontier = points
    .filter((p) => p.model.pareto)
    .sort((a, b) => a.model.output_usd_per_mtok - b.model.output_usd_per_mtok);
  let frontierPath = '';
  if (frontier.length > 1) {
    const segments = [`M ${frontier[0].x.toFixed(1)} ${frontier[0].y.toFixed(1)}`];
    for (let i = 1; i < frontier.length; i += 1) {
      segments.push(`H ${frontier[i].x.toFixed(1)}`);
      segments.push(`V ${frontier[i].y.toFixed(1)}`);
    }
    frontierPath = `<path class="pricing-frontier" d="${segments.join(' ')}"/>`;
  }

  const dots = points.map((p, i) => {
    const m = p.model;
    const on = !!m.pareto;
    return (
      `<circle class="pricing-dot${on ? ' is-pareto' : ''}" data-i="${i}" ` +
      `cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="${on ? 7 : 5}" ` +
      `fill="${vendorColor(m.vendor)}" tabindex="0" role="img" ` +
      `aria-label="${esc(m.name)}, ${esc(uiText(language, 'pricing.perMtokOutput', { price: fmtPrice(m.output_usd_per_mtok) }))}, ${esc(uiText(language, 'pricing.score'))} ${m.score.toFixed(3)}"/>`
    );
  }).join('');

  // Label only the frontier — labelling every point is unreadable at 76 models.
  //
  // Frontier points bunch up on the right (many models, similar high scores),
  // so naive placement collides: "Grok 4.5" landed on top of "Gemini 3.6
  // Flash". Walk left-to-right keeping the boxes already placed, and lift each
  // new label until it clears them. Character-width estimation is approximate
  // on purpose — it only has to be good enough to separate, and measuring real
  // text would mean rendering twice.
  const CHAR_W = 6.6;
  const LABEL_H = 15;
  const placed: Array<{ x0: number; x1: number; y: number }> = [];
  const labels = frontier.map((p) => {
    const text = p.model.name;
    const width = text.length * CHAR_W;
    const flip = p.x > VIEW_W - M.right - width - 14;
    const x = p.x + (flip ? -11 : 11);
    const x0 = flip ? x - width : x;
    const x1 = x0 + width;

    let y = p.y - 9;
    for (let guard = 0; guard < 12; guard += 1) {
      const clash = placed.some(
        (box) => x0 < box.x1 && x1 > box.x0 && Math.abs(y - box.y) < LABEL_H,
      );
      if (!clash) break;
      y -= LABEL_H;
    }
    // Never push a label out through the top of the plot.
    if (y < M.top + 10) y = p.y + 18;
    placed.push({ x0, x1, y });

    return (
      `<text class="pricing-point-label" x="${x.toFixed(1)}" ` +
      `y="${y.toFixed(1)}" text-anchor="${flip ? 'end' : 'start'}">${esc(text)}</text>`
    );
  }).join('');

  return [
    `<svg class="pricing-svg" viewBox="0 0 ${VIEW_W} ${VIEW_H}" role="group"`,
    ` aria-label="${esc(uiText(language, 'pricing.title'))}: ${esc(benchmark)}, ${models.length}">`,
    gridX, gridY, frontierPath, dots, labels,
    `<text class="pricing-axis-title" x="${(M.left + (VIEW_W - M.right)) / 2}" y="${VIEW_H - 14}" text-anchor="middle">`,
    esc(uiText(language, 'pricing.axisPrice')) + '</text>',
    `<text class="pricing-axis-title" transform="translate(16 ${(M.top + VIEW_H - M.bottom) / 2}) rotate(-90)" text-anchor="middle">`,
    esc(uiText(language, 'pricing.axisScore', { benchmark })) + '</text>',
    '</svg>',
  ].join('');
}

function buildLegend(models: AlternatePoint[], language: UiLanguage): string {
  const vendors = Array.from(new Set(models.map((m) => m.vendor))).sort();
  return (
    '<ul class="pricing-legend">' +
    vendors.map((v) =>
      `<li><span class="pricing-swatch" style="background:${vendorColor(v)}"></span>${esc(v)}</li>`
    ).join('') +
    '<li><span class="pricing-swatch pricing-swatch--frontier"></span>' + uiText(language, 'pricing.frontier') + '</li>' +
    '</ul>'
  );
}

function buildFrontierTable(models: AlternatePoint[], language: UiLanguage): string {
  const rows = models
    .filter((m) => m.pareto)
    .sort((a, b) => a.output_usd_per_mtok - b.output_usd_per_mtok)
    .map((m) => {
      const err = typeof m.stderr === 'number' ? ` <span class="pricing-err">±${m.stderr.toFixed(3)}</span>` : '';
      return (
        '<tr>' +
        `<td><span class="pricing-swatch" style="background:${vendorColor(m.vendor)}"></span>${esc(m.name)}</td>` +
        `<td class="pricing-num">${fmtPrice(m.output_usd_per_mtok)}</td>` +
        `<td class="pricing-num">${m.score.toFixed(3)}${err}</td>` +
        '</tr>'
      );
    })
    .join('');
  if (!rows) return '';
  return (
    '<div class="pricing-table-wrap"><table class="pricing-table">' +
    '<caption>' + uiText(language, 'pricing.frontierCaption') + '</caption>' +
    '<thead><tr><th>' + uiText(language, 'pricing.model') + '</th><th class="pricing-num">' + uiText(language, 'pricing.outputPrice') + '</th><th class="pricing-num">' + uiText(language, 'pricing.score') + '</th></tr></thead>' +
    `<tbody>${rows}</tbody></table></div>`
  );
}

/** Headline: the cheapest price that buys the highest tier anyone has reached. */
function buildHeadline(data: ModelPricing, models: AlternatePoint[], isPrimary: boolean, language: UiLanguage): string {
  if (!isPrimary || models.length === 0) return '';
  const latest = data.history?.[data.history.length - 1]?.frontier_price_at;
  if (!latest) return '';
  const reached = Object.entries(latest)
    .filter(([, price]) => typeof price === 'number')
    .sort((a, b) => Number(b[0]) - Number(a[0]))[0];
  if (!reached) return '';
  const [tier, price] = reached;
  return '<p class="pricing-headline">' + esc(uiText(language, 'pricing.cheapest', {
    tier,
    benchmark: data.benchmark,
    price: fmtPrice(price as number),
  })) + '</p>';
}

export function renderPricing(data: ModelPricing, benchmark?: string, language: UiLanguage = 'en'): string {
  const primary = data.benchmark;
  const active = benchmark || primary;
  const isPrimary = active === primary;
  const models: AlternatePoint[] = isPrimary
    ? data.snapshot.models
    : (data.snapshot.alternates?.[active] ?? []);

  const available = [primary, ...Object.keys(data.snapshot.alternates ?? {})];
  const chips = available.map((name) =>
    `<button type="button" class="pricing-chip${name === active ? ' is-active' : ''}" data-benchmark="${esc(name)}">` +
    `${esc(name)}</button>`
  ).join('');

  const counts = data.snapshot.counts ?? {};
  const paretoCount = models.filter((m) => m.pareto).length;

  // Freshness is disclosed per view, not buried in a footer — a chart of
  // prices that quietly went stale is worse than no chart.
  const staleFlags: string[] = [];
  if (data.stale) staleFlags.push(uiText(language, 'pricing.pricesStale'));
  if (data.capability_stale) staleFlags.push(uiText(language, 'pricing.scoresStale'));
  const staleNote = staleFlags.length
    ? `<span class="pricing-stale">${esc(staleFlags.join(' · '))}</span>`
    : '';

  return [
    '<div class="pricing-view">',
    '  <header class="pricing-head">',
    '    <div>',
    '      <h2 class="pricing-title">' + uiText(language, 'pricing.title') + '</h2>',
    '      <p class="pricing-sub">',
    '        ' + uiText(language, 'pricing.modelsSummary', { models: models.length, frontier: paretoCount }),
    counts.priced ? ' · ' + uiText(language, 'pricing.pricedTotal', { count: counts.priced }) : '',
    '      </p>',
    '    </div>',
    '    <div class="pricing-meta">' + uiText(language, 'pricing.lastSynced', { age: esc(fmtAge(data.generated_at, language)) }) + ' ' + staleNote + '</div>',
    '  </header>',
    buildHeadline(data, models, isPrimary, language),
    available.length > 1 ? `<div class="pricing-chips" role="tablist">${chips}</div>` : '',
    '  <div class="pricing-chart" id="pricingChart">',
    buildSvg(models, active, language),
    '    <div class="pricing-tooltip" id="pricingTooltip" hidden></div>',
    '  </div>',
    buildLegend(models, language),
    buildFrontierTable(models, language),
    '  <footer class="pricing-foot">',
    data.price_basis ? `<p><strong>${uiText(language, 'pricing.price')}</strong> — ${esc(data.price_basis)}. ${uiText(language, 'pricing.source')}: ` +
      `<a href="${safeHref(data.price_source_url)}" target="_blank" rel="noopener noreferrer">${esc(data.price_source ?? '')}</a>.</p>` : '',
    data.score_basis ? `<p><strong>${uiText(language, 'pricing.score')}</strong> — ${esc(data.score_basis)}.</p>` : '',
    data.capability_attribution ? `<p class="pricing-attribution">${esc(data.capability_attribution)}</p>` : '',
    '  </footer>',
    '</div>',
  ].filter(Boolean).join('\n');
}

/**
 * Wire hover/focus tooltips and the benchmark selector.
 * Re-entrant: called again after every re-render, so it must not accumulate
 * listeners on nodes that survive (it only binds to freshly-rendered ones).
 */
export function hydratePricing(
  root: ParentNode,
  data: ModelPricing,
  onBenchmarkChange: (benchmark: string) => void,
  benchmark?: string,
  language: UiLanguage = 'en',
): void {
  const chart = root.querySelector<HTMLElement>('#pricingChart');
  const tip = root.querySelector<HTMLElement>('#pricingTooltip');
  // The active benchmark is passed in, NOT re-read from the DOM. An earlier
  // version queried '.pricing-chip.is-active' inside #pricingChart — but the
  // chips render as a SIBLING of that container, so the lookup always returned
  // null and silently fell back to the primary benchmark. The SVG would then
  // show an alternate while this array held the primary, and every `data-i`
  // index resolved to the wrong model: correct-looking dots, wrong tooltips.
  // Deriving it from the same value that drove the render removes the class of
  // bug entirely.
  const active = benchmark || data.benchmark;
  const models: AlternatePoint[] = active === data.benchmark
    ? data.snapshot.models
    : (data.snapshot.alternates?.[active] ?? []);

  if (chart && tip) {
    const show = (target: Element) => {
      const index = Number((target as HTMLElement).dataset.i);
      const m = models[index] as AlternatePoint & Partial<PricedModel>;
      if (!m) return;
      const bits: string[] = [`<strong>${esc(m.name)}</strong>`, `<span class="pricing-tip-vendor">${esc(m.vendor)}</span>`];
      bits.push(uiText(language, 'pricing.perMtokOutput', { price: fmtPrice(m.output_usd_per_mtok) }));
      if (typeof m.input_usd_per_mtok === 'number') {
        bits.push(uiText(language, 'pricing.perMtokInput', { price: fmtPrice(m.input_usd_per_mtok) }));
      }
      const err = typeof m.stderr === 'number' ? ` ± ${m.stderr.toFixed(3)}` : '';
      bits.push(`${uiText(language, 'pricing.score')} ${m.score.toFixed(3)}${err}`);
      if (m.score_variant) bits.push(uiText(language, 'pricing.run', { value: esc(m.score_variant) }));
      if (m.price_variant) bits.push(uiText(language, 'pricing.priceTier', { value: esc(m.price_variant) }));
      if (m.pareto) bits.push('<em>' + uiText(language, 'pricing.onFrontier') + '</em>');

      tip.innerHTML = bits.join('<br>');
      tip.hidden = false;
      const box = chart.getBoundingClientRect();
      const dot = target.getBoundingClientRect();
      const left = dot.left - box.left + dot.width / 2;
      tip.style.left = Math.min(Math.max(left, 8), box.width - 8) + 'px';
      tip.style.top = dot.top - box.top - 12 + 'px';
    };
    const hide = () => { tip.hidden = true; };

    chart.querySelectorAll('.pricing-dot').forEach((dot) => {
      dot.addEventListener('mouseenter', () => show(dot));
      dot.addEventListener('focus', () => show(dot));
      dot.addEventListener('mouseleave', hide);
      dot.addEventListener('blur', hide);
    });
    chart.addEventListener('mouseleave', hide);
  }

  root.querySelectorAll<HTMLButtonElement>('.pricing-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      const name = chip.dataset.benchmark;
      if (name) onBenchmarkChange(name);
    });
  });
}
