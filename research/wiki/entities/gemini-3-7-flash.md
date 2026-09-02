---
slug: gemini-3-7-flash
title: Gemini 3.7 Flash
type: entity
aliases: ["Gemini 3.7 Flash", "Gemini 3.7 Flash model"]
tags: [model-release, google-deepmind, flash-tier]
description: Google's Flash-tier follow-on after Gemini 3.6 Flash, shipped 2026-08-13 at 50% below 3.6 pricing through year end; gained agent-based video analysis on 2026-09-02 (choose-what-to-inspect, claimed up to 88% fewer tokens) after an ARC-AGI-2 84.6% / $0.25-per-task launch card.
created_at: 2026-08-23
timestamp: 2026-09-02T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-02", path: research/digest/2026-09-02-digest.md}
  - {title: "ARA daily digest 2026-08-23", path: research/digest/2026-08-23-digest.md}
---

**Gemini 3.7 Flash** is the Flash-tier follow-on to [[gemini-3-6-flash]],
shipped from [[google]] on **2026-08-13** — the same week the Flash line's
price-performance cadence resumed after [[gemini-3-5-pro]].

## Why it matters

- **"Fastest-growing launch ever" — a claim with no unit (2026-08-23).** Three
  top Google figures — Sundar Pichai, Demis Hassabis and Logan Kilpatrick —
  each asserted within hours of each other that Gemini 3.7 Flash is Google's
  **fastest-growing launch ever**. No unit accompanies the claim, so it reads
  as positioning rather than a measured adoption number.
- **Priced 50% below 3.6 Flash through year end.** The model is set at **half
  of 3.6 Flash pricing through end-2026** — an aggressive re-cut of the Flash
  tier's already-cheap economics, consistent with Google competing on the
  fast/cheap axis while the Pro tier stays delayed (see [[gemini-3-5-pro]]).
- **ARC-AGI-2 at 84.6% for $0.25/task.** The headline capability number posted
  at **84.6% on ARC-AGI-2 at $0.25 per task** — frontier-adjacent
  reasoning-efficiency at a commodity price point.
- **Agent-based video analysis (2026-09-02).** [[google]] added a video path
  on 3.7 Flash, [[gemini-3-6-flash|3.6 Flash]], and **3.5 Flash-Lite** in
  which the model **chooses what to inspect instead of scanning every
  frame**, cutting token use by **up to 88 percent** per The Decoder. That
  is a serving-cost claim on the cheap Flash tier, not a new benchmark
  score, and it is the first post-launch product increment on this page
  (The Decoder; ARA daily digest 2026-09-02).

## Open questions

- **What does "fastest-growing" measure?** No unit accompanies the claim; a
  bare trend statement or a measured user/token baseline would change the read.
- **Where does it sit against Gemini 3.6 Flash and 3.5 Flash-Lite?** The Flash
  tier has shipped three generations in about a month; whether 3.7 Flash is a
  point release on the 3.6 base or a new training run is not yet stated.
- **Does the 88% video-token cut reproduce?** The Decoder figure is
  first-party/relayed; no independent token-use measurement landed in
  today's files.