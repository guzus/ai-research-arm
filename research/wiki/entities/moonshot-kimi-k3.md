---
slug: moonshot-kimi-k3
title: Moonshot AI Kimi K3
type: entity
aliases: ["Kimi K3", "Kivine", "Moonshot Kimi K3", "Moonshot AI Kimi K3"]
tags: [model-release, open-weights, china, coding, moonshot, frontier-model]
description: Moonshot AI's 2.8T-parameter flagship, reportedly closing the gap with Anthropic's Opus 4.8; dominated Hacker News (420→774 points) on 2026-07-17, with open weights promised by 2026-07-27.
created_at: 2026-07-17
timestamp: 2026-07-17T00:00:00Z
sources:
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

## Open questions

- **Does the 2.8T scale hold up under independent benchmarking once weights
  ship?** Community pelican-SVG and early local-benchmark reactions are
  informal; no neutral, contamination-aware eval has landed yet.
- **Does Moonshot hit the July 27 open-weights date?** Prior Kimi-family
  releases (K2.7 Code) shipped without a primary model card in-window; watch
  whether K3 breaks that pattern.
- **Distinct from Kimi K2.7 Code.** This page tracks the K3 flagship
  specifically — do not conflate with [[moonshot-kimi-k2-7-code]], a
  separate, smaller coding-focused release.
