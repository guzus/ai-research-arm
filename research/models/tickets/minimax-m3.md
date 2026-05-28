---
slug: minimax-m3
title: MiniMax M3 — teased successor with sparse attention
company: MiniMax
model: MiniMax M3
status: rumored
status_note: |
  MiniMax is teasing an upcoming **M3** model with a new sparse-attention
  mechanism and a **15.6× long-context response speed** boost over the
  current M2 family — per secondary roundup coverage on 2026-05-27/28.
  No MiniMax primary tweet, blog, or whitepaper is visible in the signal
  yet; the figure traces back to roundup tweets summarising the day's AI
  news, not a MiniMax-controlled channel. Treated as a single-source
  tease until corroborated by a primary or a second independent
  reporter.
expected: "TBD — no announced release date"
labels:
  - frontier-model
  - china
  - long-context
  - sparse-attention
verification: unverified
sources:
  - "@J90236317"
created_at: 2026-05-28
updated_at: 2026-05-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-28
    change: "Created — MiniMax M3 teased with a new sparse-attention mechanism and 15.6× long-context response speed boost over M2, per secondary roundup coverage 2026-05-27/28. No MiniMax-primary source in the visible signal; status set to `rumored` with `verification: unverified` accordingly"
---

**MiniMax M3** surfaced in late-May 2026 AI-news roundups as the next
generation of MiniMax's flagship M-series, with two specific claims:

- A new **sparse-attention mechanism** as the architectural change.
- A **15.6× speedup** on long-context responses versus the current M2
  generation.

**Why this ticket is `rumored` / `unverified`:** the 15.6× figure
appears in a Korean-language daily roundup tweet that aggregates news
from multiple feeds. No MiniMax-controlled channel (the company's
official X account, a model card, a blog post, or a benchmark
submission) is visible in the signal as of writing — and the bird
search-roadmap pull from MiniMax's own handle returned no results. The
ticket exists so future signal lands somewhere; do not treat the 15.6×
number as load-bearing until a MiniMax primary or a named-byline
independent outlet corroborates.

**Where this fits in the lane.** MiniMax's M2 family has been a
benchmark-competitive Chinese frontier model alongside DeepSeek's V4
series (see
[deepseek-v4-pro-price-cut-2026-05](./deepseek-v4-pro-price-cut-2026-05.md))
and the broader Chinese sparse-/efficient-architecture push that
Huawei's Tau Scaling Law (see
[huawei-tau-scaling-law-2026-05](./huawei-tau-scaling-law-2026-05.md))
just elevated to Bernstein-research-note territory. A sparse-attention
M3 would slot into that narrative cleanly — which is also why the
single-source roundup framing needs corroboration before it carries
weight.

**Transition triggers:**
- MiniMax primary statement (blog, official X, model card) →
  `status: in-testing` (preview) or `confirmed` (announced),
  `verification: confirmed`.
- Independent named-byline secondary corroboration (The Information,
  Bloomberg, Caixin, named X analyst with a primary source) →
  advance `verification: partial`.
- 15+ daily cycles with no fresh corroboration → `closed:
  stale-rumor-unverified`.
- A confirmed M3 release → advance through the lifecycle normally and
  bump `updated_at`.

**Dedup note:** further M3 / sparse-attention / 15.6× signal UPDATES
this ticket. A distinct M3-mini / M3-Pro variant gets its own ticket
and links back here. M2-family signal stays out of this ticket.
