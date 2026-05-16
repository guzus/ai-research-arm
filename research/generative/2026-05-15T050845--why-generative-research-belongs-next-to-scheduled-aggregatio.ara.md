---
eyebrow: Architecture · Meta
title: Why a generative-research lane belongs next to scheduled aggregation
lede: 'This dashboard already aggregates AI news on a clock — Twitter every three hours, RSS every hour,
  arXiv and digests daily. That cadence is great at *not missing* things, but it''s incurious by construction:
  it can''t ask *why* a story matters or what the second-order implications are.'
---

The generative lane fixes that. You point it at a question, a model writes the answer as a self-contained article, and the result lives next to the scheduled feeds. Same dashboard, same calendar conventions, different shape.

## 01. Three properties worth defending

- **Slug-keyed, not date-keyed.** Multiple pieces per day, organised by topic. The calendar metaphor breaks for ad-hoc research; an index list works better.
- **Composable components, not freeform pages.** Articles use a small `ara-*` vocabulary. The dashboard CSS owns the look. Edit one file, restyle every article in place.
- **One writer, three triggers.** Local slash command, GitHub issue label, and `workflow_dispatch` all flow through the same Python script. The output format can't drift because there's only one place that writes it.

## 02. What this fixture proves

If you're reading this on the dashboard, the chain is working end-to-end: the writer accepted the body, validated it against the `ara-doc` contract (every class begins with `ara-`, every tag is in the allowlist), appended a row to `index.json`, and the deploy pipeline copied the file into `dashboard/public/research/generative/` so the SPA could fetch it.

## 03. Next obvious moves

1. Extend the vocabulary as articles need new shapes — but slowly, since every new component is a maintenance liability.
2. Decide whether to expose the prompt itself on each rendered doc, or keep it in the index only.
3. Consider whether the existing standalone reports (XMAQUINA, Akamai) should migrate into the vocabulary, or remain as legacy iframes that don't restyle when the dashboard does.

Until then, this article is its own integration test.
