---
slug: thinking-machines
title: Thinking Machines Lab
type: entity
aliases: ["Thinking Machines", "Thinking Machines Lab", Inkling, Tinker, "Mira Murati"]
tags: [frontier-lab, open-weights, multimodal, mira-murati]
description: Mira Murati's AI lab; shipped Inkling on 2026-07-15, its first public model release — a 975B-parameter (41B active) open-weights multimodal MoE positioned against both Chinese open labs and closed US frontier players.
created_at: 2026-07-17
timestamp: 2026-07-17T00:00:00Z
sources:
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
