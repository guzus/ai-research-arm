---
slug: qwen-image-2-1
title: Qwen-Image-2.1
type: entity
aliases: ["Qwen-Image-2.1", "Qwen Image 2.1", "Qwen-Image-2.1-PE-T2I", "Qwen-Image-2.1-PE-I2I"]
tags: [open-weights, image-generation, china, dit, alibaba]
description: Alibaba's inspectable 7B single-stream visual DiT with a Qwen3-VL 8B encoder; native RGBA and 2K, day-0 Diffusers/ComfyUI hooks, under a non-commercial Qwen Research License.
created_at: 2026-09-21
timestamp: 2026-09-21T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-21", path: research/digest/2026-09-21-digest.md}
---

**Qwen-Image-2.1** is [[alibaba]]'s 20 September 2026
open-weight image model — a unified **7B / 32-layer**
single-stream visual DiT with a **Qwen3-VL 8B**
encoder and a **64-channel RGBA VAE**. Treat the
weights and day-0 runtimes as the news, not a
closed-frontier knockout. See [[open-weights]].

## Why it matters

- **Inspectable stack, not an API tease
  (2026-09-20).** GitHub and Hugging Face cards
  name the 7B DiT, 8B VL encoder, and **~1.4 GB
  VAE** (~**33 GB bf16** stack), **native RGBA**,
  up to **ten reference images**, **2048²**
  default at 40 steps, and prefix KV reuse.
  Day-0 hooks landed in Diffusers, ComfyUI,
  vLLM-Omni, and SGLang. Prompt-rewrite siblings
  **Qwen-Image-2.1-PE-T2I** and **PE-I2I**
  (Qwen3.5-VL 9B) shipped beside it (Alibaba
  Qwen, The Decoder; ARA daily digest
  2026-09-21).
- **The license stepped back.** The drop is
  under the **Qwen Research License
  (non-commercial)** — a retreat from earlier
  Apache Qwen-Image weights. That is the
  component-withholding pattern [[open-weights]]
  already tracks, now on the image line rather
  than a text MoE.
- **Vendor chart, not a bake-off.** Qwen's own
  sheet puts Image-2.1 at **60.28** versus
  [[nano-banana-2-lite|Nano Banana 2.0]] at
  **59.82**, still under GPT Image 2.5 at
  **67.01**. The "beats Nano Banana" line is
  Alibaba's chart. Distinct from the July
  **Qwen-Image-3.0** knowledge-grounded drop
  already logged on [[alibaba]] — this is the
  inspectable 2.1 DiT, not a 3.0 successor
  claim (Alibaba Qwen, The Decoder, HN 426/145;
  ARA daily digest 2026-09-21).

## Open questions

- **Does the Research License hold, or does an
  Apache/MIT card follow?** Earlier Qwen-Image
  weights were more permissive; watch the card,
  not the marketing line.
- **Independent image evals.** The 60.28-versus-
  59.82 sheet omits a public harness and a
  third-party rerun.
