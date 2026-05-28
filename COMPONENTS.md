# Research Article Components

Composable primitives for `kind: fragment` research articles in the Research tab.

**Rule:** every class in an article must start with `ara-`. Every HTML tag must be in the allowlist. The writer (`scripts/write_generative_research.py`) parses the body at commit time and rejects violations. The machine-readable contract lives in [`ARA_CATALOG.json`](ARA_CATALOG.json); this document is the human reference. The dashboard ships the matching CSS at `dashboard/src/components/ara-research.css`.

**Single source of truth (visual):** the "ARA Research Component Reference" article in the Research tab. It exercises every primitive. If a primitive renders wrong there, it renders wrong everywhere.

## Allowed tags

```
article, section, div, header, footer
h2, h3, h4
p, span, em, strong, code, mark, sup, sub, abbr, time
ul, ol, li, dl, dt, dd
a, img, figure, figcaption
table, thead, tbody, tr, th, td
blockquote, pre
br, hr
```

Anything else is rejected. No `<style>`, `<script>`, `<iframe>`, `<h1>` (the dashboard card supplies that), inline `style=`, `on*=` attributes, or `javascript:` URLs.

## Document root

| Class | What | When |
|---|---|---|
| `ara-doc` | Root container on `<article>`. Sets typography baseline. | Required. The outer `<article>` must be `<article class="ara-doc">`. |
| `ara-section` | Optional grouping wrapper inside `ara-doc`. | When you want a logical group with margin separation. |

## Title block

| Class | What | When |
|---|---|---|
| `ara-eyebrow` | Small mono uppercase label above the title (e.g. "REPORT · COMPANY"). | Optional kicker. |
| `ara-display` | Article title (h2-level visually). One per article. | Always, as the article's top heading. |
| `ara-deck` | Italic serif subtitle below the title. | When a sentence-long framing helps. |
| `ara-lede` | Opening paragraph, slightly larger. | First paragraph after the title. |

## Headings

| Class | Tag | Visual |
|---|---|---|
| `ara-h2` | `<h3 class="ara-h2">` (or h2) | Section heading. Top border + padding when not first child. |
| `ara-h2-num` | `<span class="ara-h2-num">01</span>` inside the heading | Section number chip. |
| `ara-h3` | `<h4 class="ara-h3">` (or h3) | Subsection heading. |
| `ara-h4` | `<h4 class="ara-h4">` | Minor head, muted. |
| `ara-divider` | `<hr class="ara-divider">` | Heavy section break. |

## Content blocks

| Class | Tag | When |
|---|---|---|
| `ara-callout` | `<div class="ara-callout ara-callout--info">` | Boxed aside. Variants: `--info` (warm accent), `--success` (green), `--warn` (yellow), `--danger` (red). Use sparingly. |
| `ara-callout-label` | `<span class="ara-callout-label">` inside the callout | Small uppercase chip (e.g. "Note", "Risk"). |
| `ara-quote` | `<blockquote class="ara-quote">` | Pull quote. One sentence worth slowing down for. |
| `ara-quote-attr` | `<span class="ara-quote-attr">` inside the quote | Attribution; prefixed with em-dash automatically. |
| `ara-figure` | `<figure class="ara-figure">` containing `<img>` + `<figcaption>` | Image with caption. Use `ara-figure--inline`, `--wide`, or `--bleed` for sizing variants. |
| `ara-caption` | `<figcaption class="ara-caption">` | Caption wrapper. Italic, centered, muted. |
| `ara-caption-text` | `<span class="ara-caption-text">` inside `ara-caption` | Human-readable image caption. |
| `ara-credit` | `<span class="ara-credit">` inside `ara-caption` | Source/credit line, optionally linking to the source URL. |

## Data display

| Class | Tag | When |
|---|---|---|
| `ara-kv` | `<dl class="ara-kv">` with paired `<dt>` / `<dd>` | At-a-glance key/value pairs (company facts, paper metadata). Two-column grid; stacks on mobile. |
| `ara-stats` | `<div class="ara-stats">` containing `ara-stat` blocks | Headline number grid. Auto-fits 140px+ columns. |
| `ara-stat` | `<div class="ara-stat">` inside `ara-stats` | One stat. |
| `ara-stat-label` | `<span class="ara-stat-label">` | Mono uppercase tracked label. |
| `ara-stat-value` | `<div class="ara-stat-value">` | The big mono number. Tabular figures. |
| `ara-stat-unit` | `<span class="ara-stat-unit">yrs.</span>` inside any big-figure value | Tiny unit suffix attached to a big number — `87 yrs.`, `$39.6T`, `5.2 GW`. Works inside `ara-stat-value` or `ara-compare-value`. |
| `ara-stat-note` | `<div class="ara-stat-note">` | Optional small caption (e.g. "+4.7% YoY"). |
| `ara-table` | `<table class="ara-table">` | Comparison or ranked data. Use `<thead>` + `<tbody>`. |
| `ara-row-highlight` | `<tr class="ara-row-highlight">` inside `ara-table`, or `<li class="ara-rank-item ara-row-highlight">` inside `ara-rank-list` | Single-row emphasis. Use for "the subject" row in a ranked list (e.g., your country in a global comparison). At most one per table. |
| `ara-compare` | `<div class="ara-compare">` containing three `ara-compare-card` blocks | Three-card horizontal block for "where the subject sits on the distribution" — e.g. `Lowest · Highest · Subject`. Mark the subject card with `ara-compare-card--subject`. |
| `ara-compare-card` | `<div class="ara-compare-card">` | One card. Contains `ara-compare-role` + `ara-compare-name` + `ara-compare-value`. |
| `ara-compare-role` | `<span class="ara-compare-role">` | Mono uppercase tag — `LOWEST`, `HIGHEST`, the subject's name. |
| `ara-compare-name` | `<span class="ara-compare-name">` | The entity name (country, company, period). |
| `ara-compare-value` | `<div class="ara-compare-value">` | The big mono figure. Can contain a nested `ara-stat-unit`. |
| `ara-rank-list` | `<ol class="ara-rank-list">` containing `ara-rank-item` | Dense ranked listing: rank, label, value, proportional bar. Bloomberg-style. |
| `ara-rank-item` | `<li class="ara-rank-item">` containing `ara-rank-num` + `ara-rank-label` + `ara-rank-value` + `ara-rank-fill` | One row. Add `ara-row-highlight` for the subject row. |
| `ara-rank-num` | `<span class="ara-rank-num">1</span>` | Mono rank index. |
| `ara-rank-label` | `<span class="ara-rank-label">Korea</span>` | Entity name. Truncates with ellipsis. |
| `ara-rank-value` | `<span class="ara-rank-value">36.2%</span>` | Mono tabular figure. |
| `ara-rank-fill` | `<span class="ara-rank-fill" data-pct="36"></span>` | Proportional bar fill with row tooltip. Reads `data-pct` like `ara-bar`. |

## Visualization

Proportional fills are declared with `data-pct="N"` (integer 0–100). The dashboard reads the attribute at render time and stamps `--ara-bar-pct: N%` on the element so authors never write inline `style=`.

| Class | Tag | When |
|---|---|---|
| `ara-bars` | `<div class="ara-bars">` wrapping multiple `ara-bar` | Group of comparable bars. Just provides spacing. |
| `ara-bar` | `<div class="ara-bar" data-pct="62">` containing label + value | Single labeled bar with proportional fill and hover/focus tooltip. |
| `ara-bar-label` | `<span class="ara-bar-label">` inside `ara-bar` | The category name. |
| `ara-bar-value` | `<span class="ara-bar-value">` inside `ara-bar` | The raw number, mono tabular figures. |
| `ara-stack-bar` | `<div class="ara-stack-bar">` containing `ara-stack-seg` spans | One horizontal bar split into categorical segments. |
| `ara-stack-seg` | `<span class="ara-stack-seg ara-stack-seg--1" data-pct="40">` | One segment with hover/focus tooltip. Variants `--1` through `--6` (six neutral shades). |
| `ara-stack-legend` | `<ul class="ara-stack-legend">` | Legend list below a single stack-bar. |
| `ara-stack-dot` | `<span class="ara-stack-dot ara-stack-dot--1">` inside legend `<li>` | Color swatch keyed to the matching segment. |
| `ara-stack-rows` | `<div class="ara-stack-rows">` wrapping `ara-stack-rows-legend` + `ara-stack-rows-grid` | Many labeled rows of `ara-stack-bar` sharing one legend. Bloomberg's "Luxury Companies' Sales Exposure" pattern. |
| `ara-stack-rows-legend` | `<div class="ara-stack-rows-legend">` containing `ara-stack-rows-cat` spans | Shared color legend rendered above the grid. |
| `ara-stack-rows-cat` | `<span class="ara-stack-rows-cat ara-stack-rows-cat--1">China</span>` | One legend entry. Variants `--1` through `--6` align with `ara-stack-seg--N`. |
| `ara-stack-rows-grid` | `<div class="ara-stack-rows-grid">` containing `ara-stack-rows-row` | The data area: row label + stack-bar per row. |
| `ara-stack-rows-row` | `<div class="ara-stack-rows-row">` containing `ara-stack-rows-label` + `ara-stack-bar` | One labeled row. Uses `display: contents` so its children align in the parent grid. |
| `ara-stack-rows-label` | `<span class="ara-stack-rows-label">Moncler</span>` | Right-aligned row label. |
| `ara-sparkline` | `<span class="ara-sparkline" data-points="5.2,5.4,5.5,6.1,6.8,7.0"></span>` (self-closing — dashboard fills) | Inline mini-trend SVG with first/latest/change tooltip. Dashboard injects path at render time. ~80×22 px, sits in prose. |
| `ara-line-chart` | `<div class="ara-line-chart" data-series-1="..." data-series-1-label="..." data-x-labels="..." data-y-unit="$" data-title="..." data-subtitle="..."></div>` | Full SVG line chart with axes, gridlines, and hover/focus value tooltip. Up to 4 series via `data-series-1`..`data-series-4`. Dashboard injects SVG at render time. |
| `ara-bar-chart` | `<div class="ara-bar-chart" data-categories=… data-series-1=… data-orientation=… data-mode=…></div>` | Bar/column chart with a real numeric value axis. `orientation=vertical\|horizontal`, `mode=grouped\|stacked`; signed values render a diverging zero-baseline. Up to 6 series; dashboard injects SVG at render time. |
| `ara-donut` | `<div class="ara-donut" data-labels="China,US,Europe,Other" data-values="40.6,25,20,14.4" data-center-label="100%"></div>` | Proportional ring with side legend and segment tooltip. Dashboard injects SVG + legend at render time. 3–7 segments work best. |
| `ara-slope` | `<div class="ara-slope" data-items="Apple,Microsoft,Google" data-left-values="3.2,1.6,1.2" data-right-values="4.1,3.0,2.0" data-left-label="2020" data-right-label="2026" data-unit="$"></div>` | Two-period slopegraph with change tooltip. Each line is auto-colored green (up) or red (down). Best when ≤8 items. |
| `ara-tradingview` | `<div class="ara-tradingview" data-symbol="NASDAQ:NOW" data-interval="D" data-theme="dark" data-range="12M"></div>` | Live TradingView Advanced Chart embed. The fragment ships only this script-free placeholder plus an `ara-tradingview-fallback` link; the dashboard injects the real third-party widget at view time (lazy-loaded on scroll). `data-symbol` (EXCHANGE:TICKER) is required; `data-interval`/`data-theme`/`data-range` optional. **Renders only inside the dashboard runtime** — in the static `.html` artifact or a PDF, only the fallback link shows. |
| `ara-tradingview-fallback` | `<a class="ara-tradingview-fallback" href="https://www.tradingview.com/symbols/NASDAQ-NOW/">View NASDAQ:NOW on TradingView ↗</a>` inside `ara-tradingview` | No-JS / SEO fallback link the compiler emits. The dashboard hides it via `.ara-tradingview.is-loaded` once the widget mounts; if the widget errors, the link stays visible. |
| `ara-timeline` | `<ol class="ara-timeline">` containing `ara-timeline-item` | Vertical chronological log. |
| `ara-timeline-item` | `<li class="ara-timeline-item">` | One event. |
| `ara-timeline-date` | `<time class="ara-timeline-date">2024-01</time>` | Date or period label. |
| `ara-timeline-event` | `<div class="ara-timeline-event">` containing `<strong>` headline + `<p>` body | Event content. |
| `ara-iso` | `<div class="ara-iso">` containing `ara-iso-label` + `ara-iso-glyphs` + `ara-iso-total` | Pictogram count — repeated glyph for ratio at a glance. "1950: 🚶×17 workers per beneficiary." |
| `ara-iso-label` | `<span class="ara-iso-label">1950</span>` | Mono uppercase row label (period, group). |
| `ara-iso-glyphs` | `<span class="ara-iso-glyphs" data-glyph="🚶" data-count="17"></span>` (self-closing — dashboard fills) | The dashboard expands `data-count` copies of `data-glyph` into child spans at render time. Hard cap 200 to prevent runaway DOM. Pick any single glyph: emoji, unicode symbol, or short text. |
| `ara-iso-total` | `<span class="ara-iso-total">17</span>` | The raw count, mono tabular, after the glyphs for fast scanning. |

**How the SVG primitives stay safe.** Authors only write `<div data-*>` / `<span data-*>` — `<svg>` is NOT on the allowed-tags list. `main.ts` reads `data-*` attributes at render time, parses every numeric value (dropping anything non-finite), clamps array lengths to a hard cap, and synthesises the SVG inside the dashboard. No author HTML ever touches the SVG element directly.

## Inline

| Class | Tag | When |
|---|---|---|
| `ara-tag` | `<span class="ara-tag">cdn</span>` | Topic chip. Use for inline labels, not navigation. |
| `ara-cite` | `<a class="ara-cite" href="#ref-1">1</a>` (typically wrapped in `<sup>`) | Footnote reference. Renders as `[1]`. |
| `ara-mark` | `<mark class="ara-mark">` | Highlight a phrase. Distinct from search highlight (raw `<mark>`). |
| `ara-accent` | `<strong class="ara-accent">United States</strong>` (or `<span>`) | Inline accent color + semi-bold. Use to anchor the eye on "the subject" across a global comparison. Distinct from `<em>` (italic) and `ara-mark` (background highlight). |
| `ara-flag` | `<span class="ara-flag ara-flag--green"></span>` | Status dot. Variants: `--green`, `--yellow`, `--red`. |

## Code

```html
Inline: <code>backticks-still-work</code>
Block:  <pre><code>multi-line</code></pre>
```

Inline `<code>` and `<pre><code>` need no class — they're styled automatically inside `.ara-doc`.

## What's not here, by design

- **No layout primitives.** No `ara-grid`, `ara-row`, `ara-col`. Articles flow top to bottom; if you need a grid, it's probably `ara-stats` or a table.
- **No color utilities.** No `ara-text-red`. Use callouts or flags for semantic color.
- **No spacing utilities.** Margins live inside each component. If two components feel cramped, fix the component's margins.
- **No theming knobs.** Light/dark come from dashboard CSS variables. Articles never pick colors.

## Minimal article skeleton

```html
<article class="ara-doc">
  <span class="ara-eyebrow">Category · Topic</span>
  <h2 class="ara-display">Article title</h2>
  <p class="ara-deck">Optional one-line dek.</p>

  <p class="ara-lede">Opening paragraph.</p>

  <p>Body paragraph.</p>

  <h3 class="ara-h2"><span class="ara-h2-num">01</span>First section</h3>
  <p>…</p>
</article>
```

## Extending the vocabulary

If a real article needs a shape no primitive covers, add a new `ara-*` class:

1. Edit `dashboard/src/components/ara-research.css`.
2. Add the primitive to `ARA_CATALOG.json`.
3. Document the new primitive in this file under the right section.
4. Add an example usage to the Component Reference article (slug: `components`) so it's part of the visual regression.
5. Run `uv run python scripts/ara_catalog.py`.
6. Push. Vercel rebuilds. The new primitive is available everywhere.

Each new primitive is a maintenance liability. Reach for an existing one before adding a new one.
