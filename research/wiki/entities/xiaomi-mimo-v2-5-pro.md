---
slug: xiaomi-mimo-v2-5-pro
title: Xiaomi MiMo-v2.5-Pro-UltraSpeed
type: entity
aliases: ["Xiaomi MiMo-v2.5-Pro-UltraSpeed", "MiMo-v2.5-Pro-UltraSpeed", "MiMo v2.5 Pro UltraSpeed", "Xiaomi MiMo"]
tags: [open-weights, china, moe, inference-throughput, efficiency]
description: Xiaomi's MiMo-v2.5-Pro-UltraSpeed claim of 1,000+ tokens/sec on a 1T-parameter MoE using a standard 8-GPU server; a high-signal but still partially verified inference-efficiency story.
created_at: 2026-06-17
timestamp: 2026-06-17T00:00:00Z
sources:
  - {title: "ARA model ticket — Xiaomi MiMo-v2.5-Pro-UltraSpeed", path: research/models/tickets/xiaomi-mimo-v2-5-pro.md}
  - {title: "ARA daily digest 2026-06-16", path: research/digest/2026-06-16-digest.md}
  - {title: "ARA daily digest 2026-06-10", path: research/digest/2026-06-10-digest.md}
  - {title: "ARA daily digest 2026-06-09", path: research/digest/2026-06-09-digest.md}
---

Xiaomi MiMo-v2.5-Pro-UltraSpeed is the MiMo-line release attached to the
cycle's most striking open-weight inference claim: **1,000+ tokens/sec on a
1T-parameter MoE** using a standard **8-GPU** server, with no Cerebras/Groq-like
custom inference silicon. ARA tracks it as `confirmed` for the announcement and
`partial` for verification because the throughput headline still needs
independent reproduction.

## Why it matters

- **Commodity-hardware throughput as the wedge.** Much of the [[open-weights]]
  story is about capability, licensing, or sovereignty. MiMo UltraSpeed is about
  raw serving economics: if a 1T MoE can run at four-digit tok/s on commodity
  hardware, the marginal cost curve for open models changes. That is a direct
  counter-pressure to [[nvidia]] scarcity and to closed API margins.
- **Different from "small local model" optimism.** The model is not a laptop
  toy. The important claim is that very large sparse MoEs can be made
  operationally fast with quantization, speculative decoding, and careful
  serving, without requiring exotic custom inference hardware.
- **A benchmark for skepticism.** The digest's framing was "crazy if true."
  That is the right status: the release is high-signal enough to track, but the
  wiki should preserve the uncertainty until neutral runs reproduce the claim.

## Open questions

- **Independent reproduction.** Does a third party reproduce the 1,000+ tok/s
  number with comparable hardware, prompt shape, batch behavior, and output
  quality?
- **What is the real workload?** Throughput claims can hide batch size, context
  length, speculative-acceptance rate, quality loss, and memory pressure. Which
  of those makes the number less useful for agentic coding or deep research?
- **Does Xiaomi stay in the open lane?** MiMo Code and MiMo-v2.5-Pro suggest
  sustained open-leaning releases. The strategic question is whether Xiaomi
  becomes a durable Chinese open-model supplier or a periodic community spike.

## Changelog

- [2026-06-17] created | 1T MoE / 1,000+ tok/s efficiency claim
