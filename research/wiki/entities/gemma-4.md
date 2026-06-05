---
slug: gemma-4
title: Gemma 4
type: entity
aliases: ["Gemma 4", "Gemma 4 12B", "Gemma-4", "Gemma 4 family", "Gemma"]
tags: [open-weights, model, multimodal, google-deepmind, apache-2-0, on-device]
summary: Google DeepMind's open-weights (Apache 2.0) multimodal model family; the 2026-06-04 cycle surfaced an encoder-free 12B variant that runs locally on 16 GB RAM as Gemma crossed 150M+ cumulative downloads.
created_at: 2026-06-04
updated_at: 2026-06-05
sources:
  - {title: "ARA daily digest 2026-06-05", path: research/digest/2026-06-05-digest.md}
  - {title: "ARA daily digest 2026-06-04", path: research/digest/2026-06-04-digest.md}
  - {title: "ARA model ticket — Gemma 4", path: research/models/tickets/gemma-4.md}
  - {title: "Gemma 4 — Google DeepMind model page", url: "https://deepmind.google/models/gemma/gemma-4/"}
  - {title: "Hugging Face — google/gemma-4-26B-A4B", url: "https://huggingface.co/google/gemma-4-26B-A4B"}
---

**Gemma 4** is Google DeepMind's open-weights (**Apache 2.0**) multimodal model
family — Google's named open-weight brand, distinct from the closed
[[gemini-3-5-flash|Gemini]] API line. It is one of the fastest-rising AI
releases of the cycle and a flagship of the 2026 open-weights wave.

## Why it matters

- **Encoder-free 12B variant (2026-06-04).** The day's headline novelty was a
  **Gemma 4 12B** built with an **encoder-free multimodal design** — raw image
  patches and audio waveforms are projected *directly* into the LLM, with **no
  bolted-on vision/audio encoders** (the "transformer-less vision tower" framing
  that topped Hacker News, 269→537 pts in hours). It carries a **128K–256K
  context window**, audio support on the 12B and smaller, and **runs locally on
  a 16 GB RAM laptop** — pushing capable multimodal inference onto consumer
  hardware. Variants reportedly span **E2B, E4B, 26B-A4B (MoE), 31B**, with a
  larger (~120B+) model teased; r/LocalLLaMA is clamoring for a ~124B.
- **Scale of adoption.** Google reported crossing **150M+ cumulative Gemma
  downloads** in the same window — the open-weights distribution that anchors
  Gemma's mind-share against [[minimax-m3]], [[deepseek]], and Alibaba's Qwen
  line.
- **Quality is contested.** A HuggingFace-card comparison claims
  **Qwen3.5-9B beats Gemma 4 on 5/8 shared benchmarks** despite a smaller
  footprint — the live debate over whether the architectural novelty translates
  to top-tier quality. (Note: the model-timeline ticket dates the broader Gemma
  4 family's first ship to 2026-04-02; the 12B encoder-free variant and the
  150M-download milestone are the 2026-06-04 in-cycle signal folded in here.)

- **The runaway developer story (2026-06-05).** Gemma 4 12B was confirmed by
  **Jeff Dean** with **QAT variants and a possible 120B "incoming,"** and topped
  Hacker News at **1,004 pts** on real-world RTX 3090/4090 + Apple Silicon
  testing near the 26B variant — the day's runaway open-weights story. It shared
  developer mindshare with **[[nvidia|NVIDIA's Nemotron-3-Ultra-550B]]** on HN
  and r/LocalLLaMA, sharpening the **"do local models break the AI business
  model?"** debate. The two anchor opposite ends of the 2026 open-weights wave —
  Gemma's 16 GB-laptop accessibility vs. Nemotron's datacenter-only 550B scale
  (ARA digest 2026-06-05).

## Open questions

- **Does the encoder-free design hold up on multimodal benchmarks?** Projecting
  raw patches/waveforms directly is the load-bearing architectural bet; vision
  and audio eval reproduction is the test.
- **Will the ~120B+ teased model ship open-weight under Apache 2.0?** A
  frontier-scale open Gemma would materially shift the [[ai-capex]]
  build-vs-buy line for self-hosted inference.
- **Open vs. closed inside Google.** How Gemma's open-weight push interacts
  with the closed [[gemini-3-5-flash|Gemini]] API line is Google's standing
  open-weights strategic tension.
