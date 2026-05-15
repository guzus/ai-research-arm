# Research Article Components

Composable primitives for `kind: fragment` research articles in the Research tab.

**Rule:** every class in an article must start with `ara-`. Every HTML tag must be in the allowlist. The writer (`scripts/write_generative_research.py`) parses the body at commit time and rejects violations. The dashboard ships the matching CSS at `dashboard/src/components/ara-research.css`.

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
| `ara-figure` | `<figure class="ara-figure">` containing `<img>` + `<figcaption>` | Image with caption. |
| `ara-caption` | `<figcaption class="ara-caption">` | The caption itself. Italic, centered, muted. |

## Data display

| Class | Tag | When |
|---|---|---|
| `ara-kv` | `<dl class="ara-kv">` with paired `<dt>` / `<dd>` | At-a-glance key/value pairs (company facts, paper metadata). Two-column grid; stacks on mobile. |
| `ara-stats` | `<div class="ara-stats">` containing `ara-stat` blocks | Headline number grid. Auto-fits 140px+ columns. |
| `ara-stat` | `<div class="ara-stat">` inside `ara-stats` | One stat. |
| `ara-stat-label` | `<span class="ara-stat-label">` | Mono uppercase tracked label. |
| `ara-stat-value` | `<div class="ara-stat-value">` | The big mono number. Tabular figures. |
| `ara-stat-note` | `<div class="ara-stat-note">` | Optional small caption (e.g. "+4.7% YoY"). |
| `ara-table` | `<table class="ara-table">` | Comparison or ranked data. Use `<thead>` + `<tbody>`. |

## Visualization

Proportional fills are declared with `data-pct="N"` (integer 0–100). The dashboard reads the attribute at render time and stamps `--ara-bar-pct: N%` on the element so authors never write inline `style=`.

| Class | Tag | When |
|---|---|---|
| `ara-bars` | `<div class="ara-bars">` wrapping multiple `ara-bar` | Group of comparable bars. Just provides spacing. |
| `ara-bar` | `<div class="ara-bar" data-pct="62">` containing label + value | Single labeled bar with proportional fill. |
| `ara-bar-label` | `<span class="ara-bar-label">` inside `ara-bar` | The category name. |
| `ara-bar-value` | `<span class="ara-bar-value">` inside `ara-bar` | The raw number, mono tabular figures. |
| `ara-stack-bar` | `<div class="ara-stack-bar">` containing `ara-stack-seg` spans | One horizontal bar split into categorical segments. |
| `ara-stack-seg` | `<span class="ara-stack-seg ara-stack-seg--1" data-pct="40">` | One segment. Variants `--1` through `--4` give four neutral shades. |
| `ara-stack-legend` | `<ul class="ara-stack-legend">` | Legend list below the stack-bar. |
| `ara-stack-dot` | `<span class="ara-stack-dot ara-stack-dot--1">` inside legend `<li>` | Color swatch keyed to the matching segment. |
| `ara-timeline` | `<ol class="ara-timeline">` containing `ara-timeline-item` | Vertical chronological log. |
| `ara-timeline-item` | `<li class="ara-timeline-item">` | One event. |
| `ara-timeline-date` | `<time class="ara-timeline-date">2024-01</time>` | Date or period label. |
| `ara-timeline-event` | `<div class="ara-timeline-event">` containing `<strong>` headline + `<p>` body | Event content. |

**Why no inline charts?** Arbitrary x/y line charts and donut charts would require either SVG (more attack surface) or an external library (more deps). When you genuinely need a chart, file an issue with a sample and we add a primitive.

## Inline

| Class | Tag | When |
|---|---|---|
| `ara-tag` | `<span class="ara-tag">cdn</span>` | Topic chip. Use for inline labels, not navigation. |
| `ara-cite` | `<a class="ara-cite" href="#ref-1">1</a>` (typically wrapped in `<sup>`) | Footnote reference. Renders as `[1]`. |
| `ara-mark` | `<mark class="ara-mark">` | Highlight a phrase. Distinct from search highlight (raw `<mark>`). |
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
2. Document the new primitive in this file under the right section.
3. Add an example usage to the Component Reference article (slug: `components`) so it's part of the visual regression.
4. Push. Vercel rebuilds. The new primitive is available everywhere.

Each new primitive is a maintenance liability. Reach for an existing one before adding a new one.
