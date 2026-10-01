---
slug: gemini-4-argon
title: Gemini 4 Argon
type: entity
aliases: ["Gemini 4 Argon", "Gemini 4", "gemini-4", "4 Argon"]
tags: [model-release, google-deepmind, frontier-model, fairwind, cyber-defense, pricing]
description: Google's first frontier model in over seven months; gated to government and trusted cyber defenders via Fairwind, with a 1M-token output limit and $2/$10 intro pricing that later doubles.
created_at: 2026-10-01
timestamp: 2026-10-01T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-01", path: research/digest/2026-10-01-digest.md}
  - {title: "ARA model ticket — Gemini 4 post-training", path: research/models/tickets/google-gemini-4-2026-09.md}
---

**Gemini 4 Argon** is [[google]]'s first new-generation frontier model in
more than seven months, succeeding the harvested 3.8 Flash / Live line
([[gemini-3-8-flash]], [[gemini-3-8-live]]). It shipped first to government
and trusted cyber defenders through the Fairwind program that already
gated **3.8 Flash Cyber**. Demis Hassabis said the rollout starts "with
government and trusted cyber defenders." Paid API and Google AI Ultra
access is promised "as soon as possible," with no date. Paying consumer
Gemini-app users still see **3.6**. The September 24–28 ticket that
placed Gemini 4 in post-training, with an early drop "well before
year-end," is now a named artifact rather than a stage claim (Google
DeepMind, The Verge, Ars Technica, TechCrunch, The Decoder, HN 381 pts;
ARA daily digest 2026-10-01).

## Why it matters

- **Gated first, priced like a flagship.** Output limit is **1M tokens**,
  up from 64K. Introductory API card is **$2 / $10 per Mtok**, rising to
  **$4 / $20** after the intro window; cached input is **95% off**. The
  post-intro card matches [[claude-opus-5-5|Opus 5.5]] list. HN commenters
  flagged that jump and the still-on-3.6 consumer app (Google, HN; ARA
  daily digest 2026-10-01).
- **Vendor table claims a sweep.** Google's own charts: DeepSWE v1.1
  **77.9%** (SOTA), AutomationBench **51.3%** (#1), LVBench long-video
  **91.7%**, CWE-bench v1 **68%** (tied first), plus leads on the Vals
  Index, Vals Finance Agent v2, and Harvey's Legal Agent Benchmark
  (**19.6%** vs [[claude-fable-5|Fable 5.1]]'s **6.7%**). Treat as
  first-party until independently reproduced. See [[harvey]] (Google;
  ARA daily digest 2026-10-01).
- **Internal-use claims are specific.** Google says a fleet of Argon
  agents freed more than **300 TiB** of datacenter memory, and that in
  the libgav1 Rust port Argon replaced **32K lines of SIMD** with safe
  Rust that runs **2.7×** faster than the previous port. First-party
  engineering anecdotes, not a public benchmark (Google; ARA daily
  digest 2026-10-01).
- **Independent reads are mixed and token-hungry.** The Decoder's
  testing has Argon matching [[gpt-6|GPT-6 Astra]] and trailing Opus
  5.5, while burning **more than twice as many tokens per task as
  [[astra|Astra]]** — which cuts into the low per-token intro price.
  Artificial Analysis, as relayed, scores Intelligence Index **53**,
  tying Astra; on AA-Omniscience it hallucinates far less than Astra
  (**15% vs 51%**) but also answers correctly less often (**50% vs
  63%**). No third-party reproduction of the vendor DeepSWE / Vals
  sweep landed in today's files (The Decoder, Twitter; ARA daily
  digest 2026-10-01).
- **Fairwind is now a frontier gate, not only a Flash-Cyber pen.**
  3.8 Flash Cyber already sat behind the same ~650-member defender
  program. Putting the generation flagship on that path is Google's
  Daybreak-shaped answer in a week when [[federal-ai-policy]] is
  tracking a voluntary White House accord and a reported FTC probe.
  See [[gemini-3-8-flash]] and [[agentic-ai-security]] (Google DeepMind,
  The Verge; ARA daily digest 2026-10-01).

## Open questions

- **When does paid API / AI Ultra actually open?** "As soon as
  possible" is a disposition, not a date — the same gap the September
  post-training ticket refused to treat as a schedule.
- **Does the DeepSWE 77.9% / Vals sweep hold** on an independent
  harness once the model is public, or only on Google's launch table?
- **Does the >2× token burn vs Astra persist**, or is it a gated-SKU
  serving artifact that a later cut walks back? If it holds, the $2/$10
  intro card is not the cheap task price.
- **Is Fairwind a durable access model** for a more-permissive cyber
  flagship, or a temporary holding pen until a public SKU ships?
