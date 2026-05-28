# Newspaper ARA DSL

The daily newspaper uses the ARA compiler's dedicated `newspaper` target:

```bash
uv run python scripts/compile_ara.py --target newspaper \
  research/front-page/YYYY-MM-DD-front-page.ara.md \
  --out research/front-page/YYYY-MM-DD-front-page.html
```

This target emits `<article class="ara-paper">` for the dashboard front-page view.
It is separate from the default research article target, which still emits
`<article class="ara-doc">` and is validated as a generative research fragment.

## Frontmatter

Required:

```yaml
---
title: THE AGI AWARENESS POST
---
```

Optional:

```yaml
kicker: Your Daily Artificial Intelligence Briefing
date: May 28, 2026
edition: All Sources Edition
volume: 2026
number: 149
deck: Interactive daily AI briefing
```

## Components

### `paper-index`

Navigation links for the edition.

```markdown
:::paper-index
- {label: Lead, target: "#lead-top-story"}
- {label: Signals, target: "#meter-signal-mix"}
:::
```

Targets must be `#anchor` links.

### `lead`

Collapsible top story.

```markdown
:::lead(id="lead-top-story", label="Top Story", title="Main headline")
Lead body supports normal article markdown blocks.
:::
```

### `briefs`

Expandable brief cards.

```markdown
:::briefs(id="briefs-breaking", title="Breaking", columns=2)
- headline: New model ships
  tag: Models
  body: Early notes point to lower latency.
- headline: Regulator opens inquiry
  tag: Policy
:::
```

### `news-meter`

Interactive signal bars. `value / max` must resolve to 0-100 percent.

```markdown
:::news-meter(id="meter-signal-mix", title="Signal Mix")
- {label: Breaking, value: 75, display: "3 items", tone: hot}
- {label: Research, value: 40, max: 80, display: "2 papers", tone: research}
:::
```

Valid tones: `neutral`, `hot`, `watch`, `research`, `market`.

### `story-deck`

Expandable department cards.

```markdown
:::story-deck(id="deck-departments", title="Departments")
- headline: Models & Systems
  summary: Release notes and benchmarks.
  meta: 3 digest items
  tone: watch
:::
```

The newspaper target can also use the shared ARA directives such as `quote`,
`line-chart`, `donut`, `bar-chart`, and `timeline` when the dashboard needs
chart-rich editions.
