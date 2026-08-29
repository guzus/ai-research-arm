---
slug: muse-glimmer
title: Muse Glimmer
type: entity
aliases: ["Muse Glimmer", "Meta Muse Glimmer", "Glimmer"]
tags: [model-release, meta, open-weights, multimodal, agentic]
description: Meta's 30B dense multimodal agent model, released 2026-08-10 under Apache 2.0 with day-0 transformers/llama.cpp/vLLM/SGLang/Ollama support; best of 12 of 24 benchmark rows, distilled from Muse Spark.
created_at: 2026-08-11
timestamp: 2026-08-11T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-11", path: research/digest/2026-08-11-digest.md}
---

**Muse Glimmer** is [[meta]]'s 30B dense multimodal agent model, released
2026-08-10 under **Apache 2.0** with weights live on Hugging Face and day-0
support in transformers, llama.cpp, vLLM, SGLang and Ollama — Meta's return to
[[open-weights]] after its recent priced-product posture. It is distilled from
the proprietary **Muse Spark** lineage (see [[muse-code]]), runs on one
consumer GPU (~17GB in 4-bit), and won 12 of 24 benchmark rows.

## Why it matters

- **The open-weights return.** The release breaks a streak of Meta shipping
  closed, priced models ([[muse-code|Muse Code / Muse Spark 1.2]]) and lands
  days after CEO Mark Zuckerberg's superintelligence manifesto pushed
  open-weighting as US policy. Meta separately committed to open-weighting a
  version of **Muse Spark 1.2** — the proprietary model it began charging for
  four days earlier — with timing firmed from "soon" to "in the coming weeks"
  (still a commitment, not a release). See [[open-weights]].
- **Capability read.** Best on **12 of 24 benchmark rows**, ahead of Gemma 4
  31B on 19 and Qwen 3.6 27B on 14 — with wins clustered in **agentic tool
  use** (MCP Atlas 75.5, DeepSearch QA 74.6, AA-LCR 80.0) and losses clustered
  where an agent touches a computer (Qwen leads OSWorld, TerminalBench and most
  multimodal tests; [[gemma-4|Gemma 4]] leads both primary safety metrics).
  SWE-Bench Pro is 51.2 vs 50.2 — a tie inside run-to-run variance. Both
  comparison models are **April-generation**, and Ethan Mollick's calibrated
  read is that Glimmer is *not* at the frontier of Chinese open models, is well
  behind the closed frontier, but is the **best non-Chinese open-weights
  release in a year**.
- **Local-inference economics.** Meta puts the 4-bit build at **~17GB with
  ~1% average degradation across 15 benchmarks**, down from 55GB+ at full
  precision. The DFlash speculative-decoding drafter gives 2–4× throughput on
  an RTX 5090 (74.9 → 233.4 tok/s) but only roughly half that on Mac unified
  memory — the machines the "runs on your laptop" pitch targets collect the
  smallest speed-up. A 2-bit GGUF completed 100+ tool calls in 14GB of RAM on
  an unattended repo bug hunt.
- **100+ languages and a controllable reasoning-effort dial**, plus a
  dedicated perception encoder for multimodal input.

## Open questions

- **When does the Muse Spark 1.2 open-weight release actually land?** The
  promise is the load-bearing part of the "Meta is back on open weights"
  framing and has moved from "soon" to "in the coming weeks."
- **Does the 30B dense architecture scale up?** Distilled from Spark, Glimmer
  is a mid-tier agentic model; whether Meta's open lane extends to frontier
  scale (as [[moonshot-kimi-k3|Kimi K3]] and [[qwen-3-8-max|Qwen3.8]] do)
  is unanswered.
