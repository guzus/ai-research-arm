# ARA DSL — the source format for research articles

This is the language section-writer sub-agents emit. The compiler at
`scripts/compile_ara.py` turns it into a validated `<article>` fragment
using only the `ara-*` component vocabulary documented in
[COMPONENTS.md](COMPONENTS.md). The DSL is the source of truth; the
HTML is a build artifact stored beside it.

Rule of thumb: if you can express it as a block directive, use one. If
you can express it in plain markdown, do that. Never write raw HTML —
the validator will reject every unknown class or tag.

## File shape

```
---
eyebrow: REPORT · COMPANY
title: The article title (required)
deck: Optional italic dek.
lede: |
  Opening paragraph. Can span lines.
stats:                       # optional inline stats grid in the header
  - {label: Revenue (TTM), value: $1.8B, note: +47% YoY}
  - {label: Backlog,       value: $14B}
---

## 01. First section title

Body paragraph with **bold**, *italic*, `code`, ==highlight==,
{accent}an accent phrase{/}, a citation [^1], and an inline
{sparkline:1,2,3,5,8,13}.

:::callout(kind=info, label=Note)
A callout body. Markdown works in here. Inline cites work too [^2].
:::

:::stats
- {label: Founded, value: 2001}
- {label: HQ,      value: "San Jose, CA"}
:::

## 02. Second section

> A blockquote that captures one striking idea.
> — Attribution line

:::references
- {id: 1, title: "Q1 2026 10-Q", url: "https://sec.gov/...", source: SEC EDGAR}
- {id: 2, title: "Earnings call", url: "https://ir.example.com/..."}
:::
```

The frontmatter compiles to a `<header>` block. Every `## N. Heading`
opens a fresh `<section class="ara-section">`. The compiler wraps the
whole thing in `<article class="ara-doc">`.

## Frontmatter fields

| Field | Required | Compiles to |
|---|---|---|
| `eyebrow` | optional | `<div class="ara-eyebrow">` (small mono kicker above the title) |
| `title` | **required** | `<h2 class="ara-display">` |
| `deck` | optional | `<p class="ara-deck">` (italic serif subtitle) |
| `lede` | optional | `<p class="ara-lede">` (slightly larger opening paragraph) |
| `stats` | optional | A `<div class="ara-stats">` with one `<div class="ara-stat">` per item. Each item: `{label, value, unit?, note?}`. |

## Markdown subset

Plain CommonMark for these, with one ara-specific affordance per row.

| Source | Output | Notes |
|---|---|---|
| `## 01. Title` | `<h3 class="ara-h2"><span class="ara-h2-num">01</span>Title</h3>` | Leading `N.` / `N -` / `N —` becomes the section-number chip. |
| `## Title` (no number prefix) | `<h3 class="ara-h2">Title</h3>` | No chip. |
| `### Title` | `<h4 class="ara-h3">` | Subsection. |
| `#### Title` | `<h4 class="ara-h4">` | Minor head. |
| paragraph | `<p>` | Inline markup runs. |
| `> quoted line` | `<blockquote class="ara-quote">` | If the last `>` line starts with `— ` it becomes the `ara-quote-attr` attribution. |
| `---` | `<hr class="ara-divider">` | Heavy section break. |
| `- item` / `1. item` | `<ul>` / `<ol>` | Flat lists (no nesting in v1). |
| markdown table | `<table class="ara-table">` | Prefix `*` on the first cell of a row to mark it `ara-row-highlight`. |
| ```` ```code``` ```` fence | `<pre><code>` | Block code (no syntax highlight). |

### Inline

| Source | Output |
|---|---|
| `**text**` | `<strong>text</strong>` |
| `*text*` | `<em>text</em>` |
| `` `text` `` | `<code>text</code>` |
| `==text==` | `<mark class="ara-mark">text</mark>` |
| `[label](https://url)` | `<a href="url">label</a>` |
| `[^1]` | `<sup><a class="ara-cite" href="#ref-1">1</a></sup>` |
| `[^1,2,3]` | Three consecutive `<sup>` cites pointing at `#ref-1`/`-2`/`-3`. |
| `{accent}text{/}` | `<strong class="ara-accent">text</strong>` (eye-anchor color) |
| `{tag}cdn{/}` | `<span class="ara-tag">cdn</span>` (inline chip) |
| `{mark}text{/}` | Same as `==text==`. Use for readability if you prefer. |
| `{flag:green}` (or `yellow` / `red`) | `<span class="ara-flag ara-flag--green"></span>` |
| `{sparkline:1.2,1.4,1.5,1.8}` | `<span class="ara-sparkline" data-points="...">` |
| `{h2num:X}` | `<span class="ara-h2-num">X</span>` — only if you need a custom chip outside a heading. |

Cites are the most important inline primitive. Every substantive factual
claim must end with one or more `[^N]` markers, and every `N` must
appear in the `:::references` block at the bottom.

## Block directives

Every block opens with `:::name(attr=value, attr2="quoted value")` on
its own line and closes with bare `:::` on its own line. Attributes
without a value are booleans (`legend=true` is the same as `legend`).
Attribute values that contain spaces, parens, commas, or quotes must
be double-quoted.

The body of a directive is either **YAML** (a list of mappings, usually
in flow style `{key: value, key2: value2}`), **markdown** (free-form
prose with inline syntax), or **lines** (a directive-specific
shorthand). The body type is fixed per directive.

### Component blocks

Use these by default. They map 1:1 to the `ara-*` primitives in
COMPONENTS.md.

#### `:::stats` (body: YAML list)

```
:::stats
- {label: Revenue (TTM), value: $1.8B, note: +47% YoY}
- {label: Backlog,       value: $14B}
- {label: Lifespan,      value: 87,    unit: "yrs."}
:::
```

Fields per item: `label` (required), `value` (required), `unit` (optional, attaches as `ara-stat-unit`), `note` (optional, becomes `ara-stat-note`).

#### `:::kv` (body: YAML list)

```
:::kv
- {term: Founded, def: 2001}
- {term: HQ,      def: "San Jose, CA"}
:::
```

Fields: `term`, `def`. Compiles to `<dl class="ara-kv">`.

#### `:::callout(kind=info|success|warn|danger, label="Note")` (body: markdown)

```
:::callout(kind=warn, label=Risk)
A 25% China tariff on EML wafers would cost BE ~$120M annually.
:::
```

`kind` defaults to `info`. `label` is optional; when set it renders as the small uppercase chip.

#### `:::quote(attr="Sam Altman, OpenAI")` (body: markdown)

```
:::quote(attr="Sam Altman, OpenAI")
The compute will keep getting cheaper, but the demand will outpace
the price.
:::
```

Use for pull quotes (one striking sentence). For inline quotation
in prose, use a regular markdown `> ...` blockquote.

#### `:::figure(src=..., alt=..., caption=...)` (body: empty)

```
:::figure(src="/img/diagram.png", alt="Component flow", caption="The compiler pipeline.")
:::
```

#### `:::line-chart(title=..., subtitle=..., y-unit=$)` (body: lines)

```
:::line-chart(title="BE close, TTM", subtitle="Yahoo Finance", y-unit=$)
x: 2025-06,2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05
BE: 23.92,37.39,52.94,84.57,132.16,109.24,86.89,151.37,155.67,135.49,283.36,275.95
:::
```

The `x:` row is the shared x-axis labels. Every other `LABEL: nums`
row defines one of up to 4 data series. The first non-`x:` row becomes
`data-series-1` with label = the row's `LABEL`.

For real stock data, use `scripts/stock_prices.py` (the runner has
`yfinance` installed; output is copy-pasteable into this format):

```
python3 scripts/stock_prices.py BE NVDA --range 1y --interval 1mo
```

#### `:::donut(center-label="100%")` (body: YAML list)

```
:::donut(center-label="100%")
- {label: China,  value: 40.6}
- {label: US,     value: 25}
- {label: Europe, value: 20}
- {label: Other,  value: 14.4}
:::
```

#### `:::slope(left-label=2020, right-label=2026, unit=$T)` (body: markdown table)

```
:::slope(left-label=2020, right-label=2026, unit=$T)
| Item       | 2020 | 2026 |
|------------|------|------|
| Apple      | 3.2  | 4.1  |
| Microsoft  | 1.6  | 3.0  |
| Google     | 1.2  | 2.0  |
:::
```

#### `:::timeline` (body: YAML list)

```
:::timeline
- {date: 2024-01, headline: "H200 launch",        body: "First HBM3e at scale."}
- {date: 2024-06, headline: "B100/B200 sampling", body: "Blackwell ships to hyperscalers."}
:::
```

Fields: `date`, `headline`, `body` (optional).

#### `:::iso` (body: YAML list)

```
:::iso
- {label: 1950, glyph: "🚶", count: 17}
- {label: 2025, glyph: "🚶", count: 3}
:::
```

Pictogram count. One row per item. `count` is capped at 200 by the
dashboard renderer.

#### `:::bars` (body: YAML list)

```
:::bars
- {label: NVIDIA, value: 92%, pct: 92}
- {label: AMD,    value: 5%,  pct: 5}
- {label: Intel,  value: 3%,  pct: 3}
:::
```

`pct` is the proportional fill (0–100); `value` is the displayed
number (often the same with a `%` suffix, but they can diverge).

#### `:::stack-bar(legend=true)` (body: YAML list)

```
:::stack-bar(legend=true)
- {label: China,  pct: 40}
- {label: US,     pct: 25}
- {label: Europe, pct: 20}
- {label: Other,  pct: 15}
:::
```

Max 6 segments. Segments are colored `--1` through `--6`. With
`legend=true` a swatch legend is rendered below.

#### `:::stack-rows` (body: YAML mapping)

```
:::stack-rows
categories: [China, US, Europe, Other]
rows:
  - {label: Moncler, values: [50, 20, 25, 5]}
  - {label: LVMH,    values: [30, 30, 35, 5]}
:::
```

Many labeled rows sharing one legend. Each row's `values` list length
must match `categories` length. Max 6 categories.

#### `:::rank-list` (body: YAML list)

```
:::rank-list
- {label: Korea, value: 36.2%, pct: 100, highlight: true}
- {label: Japan, value: 28.9%, pct: 80}
- {label: US,    value: 22.1%, pct: 61}
:::
```

Fields: `label`, `value`, `pct`, `highlight` (optional, marks the
subject row), `rank` (optional, overrides the auto 1-based index).

#### `:::compare` (body: YAML list)

```
:::compare
- {role: LOWEST,  name: Plug Power,    value: $2.10}
- {role: HIGHEST, name: Bloom Energy,  value: $275.95}
- {role: SUBJECT, name: Bloom Energy,  value: $275.95}
:::
```

Three-card distribution display. Cards with `role: SUBJECT` (or
explicit `subject: true`) get the highlight treatment.

#### `:::references` (body: YAML list, required when citations are used)

```
:::references
- {id: 1, title: "Q1 2026 10-Q", url: "https://sec.gov/...", source: SEC EDGAR, date: "2026-04-30"}
- {id: 2, title: "Earnings call", url: "https://ir.example.com/..."}
:::
```

Fields per item: `id` (required, the number used in `[^N]` cites),
`title` (required), `url`, `source`, `date` (all optional).

Place this block last. The compiler renders it as a `References`
section and enforces that every cited `[^N]` has a matching `id`.
Articles without citations may omit the block.

## The `:::raw` escape hatch

If the DSL truly can't express what you need (it should be rare —
file a bug instead of reaching for this), drop into raw markdown
inside `:::raw`:

```
:::raw
<div class="ara-callout ara-callout--info">
  <p>Hand-crafted HTML the DSL doesn't cover yet.</p>
</div>
:::
```

Content is passed through verbatim and then re-validated by the
writer's strict tag/class allowlist — invented classes still fail at
commit time. The escape hatch is a wider knife, not a bypass.

## Validator backstop

After the compiler runs, the output is fed through `validate_body`
(in `scripts/write_generative_research.py`). The validator rejects:

- Any HTML tag outside the allowlist (`article, section, div, header, footer, h2, h3, h4, p, span, em, strong, code, mark, sup, sub, abbr, time, ul, ol, li, dl, dt, dd, a, img, figure, figcaption, table, thead, tbody, tr, th, td, blockquote, pre, br, hr`).
- Any `class=` token that doesn't start with `ara-`.
- Any `ara-*` class not documented in COMPONENTS.md (or a valid `--variant` suffix of one).
- Inline `style=`, `on*=` handlers, `javascript:` URLs.

If you write valid DSL, the validator never fires. If you reach for
`:::raw` and invent a class, you'll see a `did you mean: ara-callout`
hint at commit time.

## Authoring tips

- One thesis sentence per `##` section, then evidence with cites, then
  a counterpoint, then a "why this matters" closer. The compiler
  doesn't enforce structure but readers expect it.
- Cite density target: 10+ cited claims per 1000 words. Every
  surprising number gets a `[^N]`.
- Use `:::table` (via plain markdown tables) for comparisons,
  `:::stats` for headline numbers, `:::line-chart` for time series.
  Don't reach for `:::callout` for cosmetic emphasis — it's for thesis
  breaks and risk flags.
- For an embedded stock chart, run `scripts/stock_prices.py TICKER`
  and paste the `x:` and `TICKER:` lines into a `:::line-chart` block.
- Treat the DSL like Python: clear is better than clever. A flat list
  of blocks reads better than a labyrinth of `:::callout` nesting.

## Compiling locally

```
python3 scripts/compile_ara.py path/to/draft.ara.md --out /tmp/draft.html
python3 scripts/check_generative_research.py path/to/draft.ara.md
```

The check accepts `.ara.md` (compiles then validates) or `.html`
(validates directly). Both report `OK` when safe to commit.
