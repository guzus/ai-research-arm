---
slug: remote-labor-index
title: Remote Labor Index (RLI)
type: concept
aliases: ["Remote Labor Index", "RLI", "Scale RLI"]
tags: [benchmark, agentic-ai, evaluation, economic-impact]
description: Scale AI × Center for AI Safety benchmark measuring how much real, paid remote freelance work AI agents can automate end-to-end; the leading model tops out near 16% while still failing the large majority of tasks.
created_at: 2026-07-02
timestamp: 2026-07-02T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-02", path: research/digest/2026-07-02-digest.md}
  - {title: "@ScaleAILabs — Remote Labor Index", date: 2026-07-02}
---

The **Remote Labor Index (RLI)** is a benchmark from **Scale AI** and the
**Center for AI Safety (CAIS)** that measures how much genuine, paid remote
freelance work an AI agent can complete **end-to-end** — evaluated against a set
of **~240 real paid freelance projects** rather than synthetic tasks. Unlike
capability benchmarks that score isolated skills, RLI is an **economic-automation**
metric: what fraction of actual billable work could an agent finish and get paid
for. It is the cleanest cold-water counterweight to launch-week model hype.

## Why it matters

- **The headline number is low even for the leader.** On the 2026-07-02 update
  (which added frontier models to the index), the **best automation rate is
  ~16%** — meaning even the top agent **fails ~84% of real freelance tasks**. The
  metric reframes "frontier" claims: capability leaderboards can show a model
  "pulling away" while RLI shows most paid work still out of reach.
- **The direction is the story.** Best automation rose from **<3% to ~16% in under
  a year** — a steep trajectory. Treat the exact figure as provisional (the
  published **Oct-2025 RLI paper put the floor at 2.5%**; the ~16.10% number this
  window came via the Twitter pulse), but the **direction is solid**.
- **[[claude-fable-5|Fable 5]] tops it at ~16.10% (2026-07-02).** Freshly back from
  its two-week export ban, Fable 5 leads (🥈 [[claude-opus-4-8|Opus 4.8]], 🥉 Codex
  GPT-5.5), roughly **double the next model** — the neutral capability print of the
  window. **Caveat:** the field **excludes GPT-5.6 (Sol/Terra) and any Gemini
  Flash**, so "#1" is a snapshot of who was entered, not the whole frontier.
- **It sharpens the demand-side / [[ai-capex]] ROI debate.** An 84% failure rate on
  paid work is the empirical anchor for the "labs oversold models / *tokenmaxxing*"
  critique (Palantir's Karp) and for measured-productivity skepticism — the gap
  between benchmark capability and realized economic value.

## Open questions

- **Does the ~16% ceiling move once GPT-5.6 and Gemini Flash are entered?** The
  current leaderboard is incomplete; a fuller field could reshuffle the top.
- **Is RLI's task set representative of remote knowledge work,** or biased toward
  the freelance-marketplace projects it samples?
- **How fast does the failure rate fall?** The <3% → 16% jump in a year is the
  variable that most directly bears on AI's near-term labor-market impact.

## Changelog

- [2026-07-02] created | Scale×CAIS end-to-end paid-freelance automation benchmark, leader ~16% / fails ~84%
