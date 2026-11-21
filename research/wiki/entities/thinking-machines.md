---
slug: thinking-machines
title: Thinking Machines Lab
type: entity
aliases: ["Thinking Machines", "Thinking Machines Lab", Inkling, "Inkling-Small", Tinker, "Mira Murati", "Inkling 2 Mini", "Inkling-2 Mini", "Inkling 2"]
tags: [frontier-lab, open-weights, multimodal, mira-murati]
description: Mira Murati's AI lab; shipped Inkling 2 Mini, a 26.4B/3.4B-active looped transformer with a 1M-token window aimed at laptops, after the 2026-07 Inkling drop.
created_at: 2026-07-17
timestamp: 2026-11-21T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-11-21", path: research/digest/2026-11-21-digest.md}
  - {title: "ARA daily digest 2026-09-07", path: research/digest/2026-09-07-digest.md}
  - {title: "ARA daily digest 2026-08-22", path: research/digest/2026-08-22-digest.md}
  - {title: "ARA daily digest 2026-08-01", path: research/digest/2026-08-01-digest.md}
  - {title: "ARA model ticket — Thinking Machines Inkling-Small", path: research/models/tickets/thinking-machines-inkling-small-2026-07.md}
  - {title: "ARA daily digest 2026-07-17", path: research/digest/2026-07-17-digest.md}
  - {title: "ARA model ticket — Thinking Machines Inkling", path: research/models/tickets/thinking-machines-inkling.md}
---

**Thinking Machines Lab** is Mira Murati's AI startup, founded in 2025. On
**2026-07-15** it shipped **Inkling**, its first public model release since
founding — announced by team member @soumithchintala and Tinker's official
account, corroborated within 15 minutes by @ns123abc and @kimmonismus.

## Why it matters

- **Inkling's specs.** A **975B-total-parameter / 41B-active MoE**, natively
  **multimodal** (text/image/audio), supporting up to **1M context**, trained
  from scratch on GB300s (~45T tokens), open-weighted on **Tinker** and
  Hugging Face under an Apache-style license per community reports.
- **Explicit two-front positioning.** Inkling is framed as a customizable
  alternative to one-size-fits-all closed frontier models (competing with
  [[anthropic]], [[openai]]) **and** a direct answer to Chinese open-weight
  labs ([[deepseek]], [[zhipu-glm-5-2]], [[moonshot-kimi-k3]]) — the same
  two-front framing running through the broader [[open-weights]] theme.
- **Contested quality claims within 24 hours.** Independent researchers Ethan
  Mollick (@emollick) and Jonas Jitsev (@JJitsev) reported the model
  underperforming its launch-day billing — struggling on basic reasoning
  tests and lagging [[zhipu-glm-5-2|GLM 5.2]] on the TB 2.1 benchmark — even
  as HuggingFace/Unsloth/Modal shipped fast ecosystem support (quantized
  versions, accelerated hosting) within a day. Treat the launch specs as
  confirmed and the quality claims as contested pending further independent
  evals.

- **Inkling-Small answers the cadence question (2026-07-31, digested
  2026-08-01).** Thinking Machines shipped **Inkling-Small**, an open-weights
  reasoning model **cut from 41B to 12B active parameters**, benchmarked
  around **#88 overall and #21 among open models on Text Arena (1431
  points)**. That resolves the "one-off or a cadence" question below in favour
  of a cadence — a second open-weights release inside three weeks — and moves
  the lab down-market rather than up, competing on efficiency against the
  Chinese open labs ([[deepseek-v4-flash]], [[moonshot-kimi-k3]]) shipping in
  the same window rather than on raw scale. Its **verified 36.5% ARC-AGI-2**
  score is also now the reference line against which an unverified 60.4% Kimi
  K3 claim is being measured. See [[open-weights]] and the
  [Inkling-Small ticket](../../models/tickets/thinking-machines-inkling-small-2026-07.md)
  (ARA daily digest 2026-08-01).

- **Inkling and Inkling Small served free on OpenRouter — as a data-collection
  exercise, not a price move (2026-08-22).** Both models are being served **free
  on [[openrouter|OpenRouter]] inside agentic harnesses**, with the lab stating the
  arrangement is **data collection on real-world agentic behaviour**, not a
  promotional price cut. It is a notable play on the [[open-weights]] axis: rather
  than charging for the strongest open multimodal model it has shipped, Thinking
  Machines is transparently paying in free inference for telemetry on how open
  models behave inside harnesses — and it doubles as a live-lab dataset play ahead
  of follow-on releases (ARA daily digest 2026-08-22).

- **A $40B-plus raise, with NVIDIA reported in talks on $2.5B
  (2026-09-07).** The Information, via Twitter, says
  [[thinking-machines|Thinking Machines]] is seeking
  **$5–6 billion at a $40 billion-plus pre-money**, with Accel
  in talks to lead and [[nvidia]] discussing a **$2.5 billion**
  position. The Information's own post confirms only the ~$40B
  raise and "at least a few hundred million dollars in
  annualized revenue"; the NVIDIA and Accel specifics reach the
  record through one aggregator's paraphrase. Neither NVIDIA
  nor Accel is named in the primary outlet's own summary. This
  is the financing item the 2026-09-04 ingest skipped; treat
  the $2.5B stake as contested until a principal comments.
  See [[nvidia]] and [[ai-capex]] (The Information, Twitter;
  ARA daily digest 2026-09-07).

## Inkling 2 Mini (2026-11-21)

- **Thinking Machines shipped Inkling 2 Mini**, an open-weights looped
  transformer aimed at laptops: **26.4B total, 3.4B active**, about **20GB**
  of memory, and a **1M-token** window. Architecture is **24 stored layers
  in four blocks of six**, with the two middle blocks run three times, so
  **48 layer applications per token from 24 stored layers**. Most weights
  train and serve in **NVFP4**, last four layers **MXFP8**; [[hugging-face]]
  lists hidden size **2,304**, **8-of-128** experts, and GGUF IQ4_NL / Q8_0
  (HN, Thinking Machines; ARA daily digest 2026-11-21).
- **Vendor benches under 100B total** include SWE-bench Verified **79.2%**,
  a tie with [[qwen-3-8-max|Qwen3.8-27B]] on AA Index, DeepSWE v1.1
  **48.2%**, SWE-bench Pro v2 Hard **77.9%**, BrowseComp **79.0%**, and MCP
  Atlas **82.7%**. MultiChallenge **50.0%** and ComplexConstraints **33.4%**
  still trail Qwen3.8-27B. Treat those as first-party until independent
  evals land. Stanford Hazy’s “intelligence per joule” on [[nvidia|DGX
  Spark]] is **0.703 versus 0.430** for a Qwen 3.6 MoE (HN, Thinking
  Machines; ARA daily digest 2026-11-21).
- **Tinker list prices** in a minutesofai recap are **$0.15 / $0.50 /
  $0.015** per 1M input / output / cache-hit — secondary, not a lab price
  card. HN’s Inkling 2 Mini thread was the largest new-model thread of the
  day at **651 points / 104 comments**. See [[open-weights]].

## Open questions

- **Do independent evals hold the vendor SWE-bench / AA Index / MCP Atlas
  numbers?** Inkling’s 2026-07 launch quality was contested within a day;
  Mini’s 79.2% SWE-bench Verified is the same class of claim until a third
  party reruns it.
- **Is the looped-transformer recipe the product, or a one-off efficiency
  cut?** 48 layer applications from 24 stored layers is a distinct serving
  story from the 975B/41B Inkling MoE.
- **Does the $40B-plus raise close, and does [[nvidia]] take the reported
  $2.5B seat?** Unchanged from 2026-09-07; no principal comment in this
  digest.
