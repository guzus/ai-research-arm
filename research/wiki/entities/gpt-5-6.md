---
slug: gpt-5-6
title: OpenAI GPT-5.6
type: entity
aliases: ["GPT-5.6", "GPT 5.6", "GPT-5.6 Pro", "GPT-5.6 Mini", "GPT-5.6 Sol", "GPT-5.6 Terra", "GPT-5.6 Luna", "Sol", "Terra", "Luna"]
tags: [model-release, openai, gpt, frontier-model, government-gated, preview]
description: OpenAI frontier family shipped 2026-06-26 as a US-government-gated limited preview — Sol (flagship) / Terra (balanced) / Luna (fast/cheap), with new "max" and "ultra" (subagent-spawning) reasoning modes and a Terminal-Bench 2.1 SOTA; GA "in the coming weeks."
created_at: 2026-06-20
timestamp: 2026-06-29T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-06-29", path: research/digest/2026-06-29-digest.md}
  - {title: "ARA daily digest 2026-06-23", path: research/digest/2026-06-23-digest.md}
  - {title: "ARA daily digest 2026-06-21", path: research/digest/2026-06-21-digest.md}
  - {title: "ARA daily digest 2026-06-20", path: research/digest/2026-06-20-digest.md}
  - {title: "ARA model ticket — OpenAI GPT-5.6", path: research/models/tickets/openai-gpt-5-6.md}
  - {title: "OpenAI — Previewing GPT-5.6 Sol", url: "https://openai.com/index/previewing-gpt-5-6-sol/", date: 2026-06-26}
---

**GPT-5.6** is [[openai]]'s frontier family, shipped **2026-06-26** as a
**US-government-gated limited preview** after weeks of rumor. It lands as a
three-tier family — **Sol** (flagship), **Terra** (balanced), **Luna**
(fast/cheap) — with new **"max" reasoning effort** and an **"ultra" mode** that
spawns subagents. Per the model ticket `openai-gpt-5-6`, the lifecycle advanced
from `rumored` to `in-testing` on 2026-06-26 (a real admin-panel artifact plus a
gated external preview); GA is "in the coming weeks."

## Why it matters

- **Shipped — but gated at the US government's request (2026-06-26).** OpenAI
  began a **limited preview of the GPT-5.6 family** with access restricted, **at
  the US government's request**, to a small group of trusted partners shared
  with the government before broader release — the same "de facto licensing
  regime" shape as the [[claude-fable-5|Fable 5 / Mythos 5]] export suspension
  (see [[federal-ai-policy]]). OpenAI stated "this kind of government access
  process shouldn't become the long-term default." *The Information*/Axios report
  the request came through the Office of the National Cyber Director and OSTP
  under the voluntary June 2 frontier-model review EO, and that GPT-5.6 has
  **"Mythos-like" capability** — OpenAI had reportedly pushed for release since
  before the Fable ban. **GA "in the coming weeks"; Polymarket prices ~90% chance
  of public release by July 31.**
- **Capability + pricing.** Sol sets a new SOTA on **Terminal-Bench 2.1** and
  improves agentic coding, biology, and cybersecurity. Pricing (per 1M tokens):
  **Sol $5 in / $30 out**; **Terra $2.50 / $15**; **Luna $1 / $6**, with new
  explicit cache breakpoints and a 30-minute minimum cache life.
- **From rumor to artifact — the prelude.** For most of June the signal was
  anticipation, not a shipping artifact: prediction markets priced a
  by-2026-06-30 release ~89%; a `gpt-5.6-preview` route leaked in OpenAI's admin
  panel (2026-06-25, @scaling01/@haider1); chief scientist **Jakub Pachocki**
  reportedly called it internally a "meaningful improvement" over GPT-5.5. The
  viral "stealth GPT-5.6-Pro" demos were debunked as model-tier confusion
  (testers were on GPT-5.5-Pro). The leaked ~1.5M-context / ~3×-cheaper-than-
  Fable-5 specs were rumor until the preview.
- **The competitive backdrop.** GPT-5.6 is the closed-frontier counterweight to a
  field where [[anthropic]]'s [[claude-fable-5|Fable 5 / Mythos 5]] sits embargoed
  and open weights like [[zhipu-glm-5-2|GLM-5.2]] are closing the gap. It shipped
  the same window as OpenAI's **Jalapeño** custom inference ASIC
  ([[broadcom|Broadcom]]-co-designed) — vertical integration on both the model
  and the silicon layer.

## Open questions

- **Does the government gate become the default?** OpenAI itself said the access
  process "shouldn't become the long-term default" — but with Sol gated and
  [[claude-fable-5|Mythos 5]] export-suspended, the de facto licensing regime now
  covers both US frontier flagships. Watch whether GA actually opens "in the coming
  weeks" or slips (Polymarket ~90% by July 31).
- **Neutral benchmarks.** Sol's Terminal-Bench 2.1 SOTA is OpenAI's own claim;
  no independent eval has landed. Does it hold up against [[claude-fable-5|Fable 5]]
  and [[zhipu-glm-5-2|GLM-5.2]] on contamination-aware harnesses?
- **Family-at-once cadence.** Shipping Sol/Terra/Luna together (plus "ultra"
  subagent-spawning mode) is a break from staggered GPT-5.x rollouts — a signal
  about OpenAI's product discipline ahead of its IPO.
