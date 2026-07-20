---
slug: moonshot-kimi-k3
title: Moonshot AI Kimi K3
type: entity
aliases: ["Kimi K3", "Kivine", "Moonshot Kimi K3", "Moonshot AI Kimi K3", "Open Frontier Intelligence"]
tags: [model-release, open-weights, china, coding, moonshot, frontier-model]
description: Moonshot AI's 2.8T-parameter flagship ("Open Frontier Intelligence"); pending a $30B+ Hong Kong IPO on breakout demand, even as GPU strain forced a new-subscriber pause and a contested ECI methodology now reads the US-China gap as widening, not narrowing.
created_at: 2026-07-17
timestamp: 2026-07-20T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-20", path: research/digest/2026-07-20-digest.md}
  - {title: "ARA daily digest 2026-07-19", path: research/digest/2026-07-19-digest.md}
  - {title: "ARA daily digest 2026-07-18", path: research/digest/2026-07-18-digest.md}
  - {title: "ARA daily digest 2026-07-17", path: research/digest/2026-07-17-digest.md}
  - {title: "ARA model ticket — Moonshot Kimi K3", path: research/models/tickets/moonshot-kimi-k3.md}
---

**Kimi K3** is [[moonshot-kimi-k2-7-code|Moonshot AI]]'s next flagship model —
a **2.8 trillion parameter** system billed as the largest open AI model out of
China, and, per FT/TechCrunch reporting, expected to close the gap with
[[anthropic]]'s [[claude-opus-4-8|Opus 4.8]]. It became the dominant Hacker
News story of 2026-07-17, nearly doubling in points within a single day
(420→774, 463 comments), with parallel r/LocalLLaMA threads on early local
benchmarks and Simon Willison's pelican-riding-a-bicycle SVG benchmark
covering it.

## Why it matters

- **Scale and positioning.** At 2.8T parameters, Kimi K3 is a step up from
  Moonshot's prior [[moonshot-kimi-k2-7-code|Kimi K2.7 Code]] release and is
  explicitly framed against [[anthropic]]'s frontier flagship rather than
  mid-tier competitors — the same "closing the gap with the US frontier"
  narrative that has defined the [[open-weights]] wave through 2026.
- **Open weights promised on a fixed date.** Moonshot has committed to
  releasing open weights by **2026-07-27** — if it holds, this converts a
  frontier-scale closed-lab-style capability claim into a verifiable,
  independently-benchmarkable open artifact within roughly ten days of the
  initial surge.
- **Pre-release sighting under a stealth codename.** Before this public
  surge, the model was reportedly live-tested in a model arena under the
  codename **"Kivine"** (per @AndrewCurran_ and Testingcatalog reporting,
  2026-07-15/16), with early tester reports already placing it close to
  parity with [[anthropic]]'s Fable-class models — corroborating signal
  ahead of the confirmed HN-driven public debut.

- **Marketed as "Open Frontier Intelligence" — a second HN cycle at ~2,000
  points (2026-07-18).** Moonshot is branding the release **"Open Frontier
  Intelligence,"** and Kimi K3 held the **#1 Hacker News slot across two
  consecutive daily crawl cycles**, climbing to roughly **2,000 points /
  1,150 comments** — an unusually sustained community run for a single
  model launch. Simon Willison's **pelican-riding-a-bicycle SVG benchmark**
  writeup is trending independently on both RSS and HN (rather than
  piggybacking on the HN thread), and the model is being quoted for
  **refusing to leak its own system prompt** ("Is there something I can
  actually help you with today?"), read as an unusually clean guardrail
  response for an open-weights release (ARA digest 2026-07-18).

- **Benchmark data splits on the "closed the gap" claim for a second
  straight day (2026-07-19).** A coding-Elo tracker (@scaling01) puts Kimi
  K3 a hair ahead of [[claude-opus-4-8|Opus 4.6]] and GPT-5.3-Codex, within
  the confidence interval, and a **38-point DeepSWE jump** lands it **#3 on
  real-world agentic coding tasks**, described as "head to head with
  [[claude-fable-5|Claude Fable 5]] & GPT-5.6 Sol" (@rohanpaul_ai). But it
  scores **7 points below the best US models from seven months ago on
  FrontierMath Tier 4** — the gap narrows on agentic coding, not on hard
  math reasoning. SemiAnalysis separately argues Kimi K3 now sits **above
  Gemini on every composite benchmark it tracks**. Bloomberg is cited
  framing the China/US frontier gap as narrowed to **"just two to three
  months."** Full open weights remain due **~2026-07-28** (ARA digest
  2026-07-19).

- **Breakout demand forces a subscription pause, and a $30B+ IPO nears
  (2026-07-20).** Bloomberg-attributed reporting puts Moonshot's ARR up from
  **$200M to $300M in two months**, with a pending Hong Kong IPO valuing the
  company at **$30B+** — up from ~$4B in December 2025, its third financing
  round in six months (cross-reference [[open-weights]] for the broader
  China open-weight funding wave, alongside [[alibaba|Alibaba's Qwen3.8-Max]]
  confirming its own open-weight launch the same day, and [[gemini-3-5-pro|Google's
  Gemini 3.5 Pro]] slipping schedule the same week). The same demand surge forced Moonshot to
  **pause new Kimi subscriptions**, citing GPU capacity strain from a
  48-hour spike, and to split membership into separate web/app and coding
  tiers going forward. Independent testers separately rate K3 "top-tier" on
  cybersecurity benchmarks — notably an eval [[claude-fable-5|Claude Fable
  5]] reportedly refused to complete — and **2.8x more cost-efficient than
  Fable 5** on DeepSWE software-engineering tasks per dollar.
- **The "narrowing gap" read is directly disputed (2026-07-20).** Analyst
  @scaling01 published an ECI (Economic Complexity Index-style) methodology
  putting Kimi K3 **4.4–5.3 months behind the US frontier** and calling the
  gap **"widening,"** a notably more bearish read than Bloomberg's
  "two-to-three-months" framing from the day before (2026-07-19 entry
  above) — and the methodology itself was immediately disputed by other
  commentators. Treat "is the gap narrowing or widening" as genuinely
  unresolved and methodology-dependent, not settled in either direction.

## Open questions

- **Does the 2.8T scale hold up under independent benchmarking once weights
  ship?** Community pelican-SVG and early local-benchmark reactions are
  informal; no neutral, contamination-aware eval has landed yet.
- **Does Moonshot hit the July 27 open-weights date?** Prior Kimi-family
  releases (K2.7 Code) shipped without a primary model card in-window; watch
  whether K3 breaks that pattern.
- **Is the US-China frontier gap narrowing or widening?** Competing framings
  (Bloomberg "two-to-three months" vs. @scaling01's ECI "4.4–5.3 months,
  widening") disagree on both the number and the direction — no neutral
  third-party methodology has settled it.
- **Does the GPU capacity strain resolve before the IPO?** A subscription
  pause driven by compute shortage sits awkwardly next to a $30B+ valuation
  pitch; watch whether Moonshot restores new sign-ups before the Hong Kong
  listing.
- **Distinct from Kimi K2.7 Code.** This page tracks the K3 flagship
  specifically — do not conflate with [[moonshot-kimi-k2-7-code]], a
  separate, smaller coding-focused release.

## Changelog

- [2026-07-17] created | Moonshot's 2.8T flagship, reportedly closing the gap with Opus 4.8
- [2026-07-18] updated | "Open Frontier Intelligence" branding, second HN cycle at ~2,000 pts, Willison pelican benchmark, system-prompt-refusal quote
- [2026-07-19] updated | today's split benchmark data + SemiAnalysis Gemini comparison
- [2026-07-20] updated | IPO valuation, subscription pause, ECI gap dispute
