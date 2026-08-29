---
slug: thinking-machines
title: Thinking Machines Lab
type: entity
aliases: ["Thinking Machines", "Thinking Machines Lab", Inkling, "Inkling-Small", Tinker, "Mira Murati"]
tags: [frontier-lab, open-weights, multimodal, mira-murati]
description: Mira Murati's AI lab; shipped Inkling on 2026-07-15, its first public model release — a 975B-parameter (41B active) open-weights multimodal MoE positioned against both Chinese open labs and closed US frontier players.
created_at: 2026-07-17
timestamp: 2026-08-22T00:00:00Z
sources:
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

## Open questions

- **Does Inkling's quality catch up to its launch billing?** The strong
  ecosystem uptake (fast quantization/hosting support) sits in tension with
  early negative independent benchmark reports.
- **Follow-on cadence.** Is Inkling a one-off open-weights entrant or the
  start of a regular release cadence from Thinking Machines, mirroring the
  Chinese open-weight labs it is positioned against?
- **Official benchmarks.** No official Thinking Machines blog post or model
  card with published benchmarks has landed yet; watch for one that could
  firm up the quality claims either way.
