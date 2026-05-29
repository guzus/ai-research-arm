---
slug: liquid-ai
title: Liquid AI
type: entity
aliases: ["Liquid AI", "LiquidAI", "Liquid Foundation Models", "LFM"]
tags: [open-weights, on-device, hybrid-models, mit-spinout]
summary: MIT-spinout foundation model lab focused on on-device hybrid (non-pure-transformer) architectures; shipped LFM2.5-8B-A1B with day-one llama.cpp / MLX / vLLM / SGLang support on 2026-05-29.
created_at: 2026-05-29
updated_at: 2026-05-29
sources:
  - {title: "ARA daily digest 2026-05-29", path: research/digest/2026-05-29-digest.md}
---

Liquid AI is a foundation-model lab (MIT-spinout lineage) that ships the
**Liquid Foundation Models (LFM)** series, focused on **on-device hybrid
architectures** — explicitly not pure transformers. On 2026-05-29 it released
**LFM2.5-8B-A1B** (8B total parameters, 1B active), the latest in the series.

## Why it matters
- **Day-one runtime support.** LFM2.5-8B-A1B shipped with **simultaneous
  support across llama.cpp, MLX, vLLM, and SGLang** — rare for a non-pure-
  transformer architecture, which usually requires runtime-specific kernels.
  Positioned as fastest in class on CPU+GPU at its size; r/LocalLLaMA reception
  was the "you can run it on any potato" line of the day (ARA digest
  2026-05-29).
- **Western open-weight signal.** The launch lands in the same week as **X
  Square Robot's Wall-OSS-0.5** and **IBM Granite 4.1** — collectively the
  Western open-weights tier pushing back against a stretch of news dominated
  by Qwen3.6 / GLM-5.1 / DeepSeek V4. Liquid AI is the most architecturally
  distinct of the three (Wall-OSS is a 4B VLA; Granite 4.1 dropped its Mamba
  hybrid for a pure transformer — see ARA digest 2026-05-29).
- **Hybrid-vs-pure-transformer evidence.** Granite 4.1's decision to *drop*
  its Mamba hybrid for a pure transformer "for fine-tuning ease" lands the
  same day as Liquid AI's hybrid push — making 2026-05-29 a small natural
  experiment in whether hybrid architectures earn their complexity at the
  on-device size class.

Day-one **vLLM** support also puts LFM2.5 squarely on the surface that
[[agentic-ai-security]] is currently tracking — the 2026-05-29 vLLM/MCP
framework CVE touches the same runtime path Liquid is shipping against.

## Open questions
- **Fine-tuning story.** Granite explicitly cited fine-tuning friction as the
  reason to abandon hybrid. Does LFM2.5 have a credible fine-tuning toolchain
  for downstream users, or does the runtime story stop at base-model
  inference?
- **Benchmark independence.** "Fastest in class on CPU+GPU at its size" is
  vendor framing — does it survive third-party local-LLaMA benchmarks at
  matched quantization?
- **Compounding releases.** The 2.5 → 8B-A1B numbering implies a Liquid
  release ladder. How quickly does the lab iterate compared to dense
  open-weight peers?
