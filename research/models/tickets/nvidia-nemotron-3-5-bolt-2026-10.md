---
slug: nvidia-nemotron-3-5-bolt-2026-10
title: "NVIDIA Nemotron 3.5 Bolt 74B-A9B — reported open-weight multimodal MoE with ~2-bit QAT weights"
company: "NVIDIA"
model: "Nemotron 3.5 Bolt 74B-A9B"
status: released
status_note: |
  **2026-10-17 — verification partial.** Now corroborated by @testingcatalog (2026-10-16
  brief, "Nemotron 3.5 Bolt 24GB"), @Narra_Creator (links an official NVIDIA model
  page) and @DogukanUrker's open-weights roundup, which also says a Bolt E4B variant
  lands next week (single source).

  **Single secondary source.** @Oluwaphilemon1 (2026-10-16 11:08 UTC) says NVIDIA
  released Nemotron 3.5 Bolt: 74B total / 9B active MoE, about 2-bit quantization via
  quantization-aware training (~22GB weights), text/image/video input, up to 256K
  context, LiLiCorr speculative decoding, and open weights plus training resources on
  Hugging Face. Quoted NVIDIA BF16→IQ2 numbers: PinchBench 90.35→87.82, BrowseComp
  70.00→66.75, GPQA Diamond 88.83→86.43, Terminal-Bench 2.1 53.93→50.98. Official
  llama.cpp recipes reportedly target 32GB+ GPUs at 65K context and 48GB+ at 256K.

  The detail reads like a model card, but no NVIDIA post or HF page was captured (a
  direct HF check was blocked on this runner), so verification is `unverified`. The
  Nemotron 3.5 family is otherwise visible: a Hermes changelog in the same signal adds
  "Nemotron Super 3.5 defaults".
expected: "Released ~2026-10-16 with open weights (multiple secondary reports). Open: an NVIDIA post or Hugging Face model card; the reported Bolt E4B variant 'next week'; independent head-to-head against Qwen3.6-35B-A3B."
labels:
  - nvidia
  - nemotron
  - open-weights
  - moe
  - quantization
  - partial
verification: partial
sources:
  - "https://x.com/testingcatalog/status/2111409303701577925"
  - "https://x.com/Narra_Creator/status/2111410227543228851"
  - "https://x.com/DogukanUrker/status/2111337663286706405"
  - "https://x.com/Oluwaphilemon1/status/2111051657916064053"
  - "https://x.com/iamlukethedev/status/2111056522470174956"
created_at: 2026-10-16
updated_at: 2026-10-17
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-16
    change: "Created — RELEASED / unverified. A single secondary post (@Oluwaphilemon1, 2026-10-16 11:08 UTC) reports NVIDIA released Nemotron 3.5 Bolt 74B-A9B as open weights on Hugging Face. It is a 74B-total / 9B-active MoE shipped at ~2-bit via quantization-aware training (~22GB), with text/image/video input, 256K context and LiLiCorr speculative decoding. The post quotes NVIDIA's BF16-vs-IQ2 retention numbers (e.g. GPQA Diamond 88.83 -> 86.43). Model-card-level detail, but no NVIDIA primary captured, so unverified. Family context only: a Hermes changelog relay (@iamlukethedev) mentions 'Nemotron Super 3.5 defaults'. Prior Nemotron tickets are closed and untouched ([[nvidia-nemotron-3-ultra-imo-2026-09]])."
  - ts: 2026-10-17
    change: "Released, unchanged; verification unverified -> partial. Independent corroboration, still no NVIDIA post captured. (1) @testingcatalog's 2026-10-16 brief: 'NVIDIA also introduced Nemotron 3.5 Bolt 24GB, a model that fits into 24GB of memory', next to the Nemotron 3.5 Super VL launch ([[nvidia-nemotron-3-5-super-vl-2026-10]]). (2) @Narra_Creator (2026-10-17 10:53 UTC) restates 74B total / 9B active compressed to 24GB, built for local agents, and links an 'official NVIDIA model' page. (3) @DogukanUrker's week-in-open-weights list (2026-10-17 06:05 UTC) includes 'Nemotron 3.5 Bolt 74B' and says 'next week Nemotron 3.5 Bolt E4B lands'. The E4B variant comes from that one source and is not adopted as a date."
---

The notable part is the packaging. NVIDIA ships the 2-bit weights as the main
artifact, trained for that precision, instead of leaving quantization to the
community. That targets 24-48GB local GPUs directly.

It needs a primary source. If no NVIDIA post or model card appears within about 15
cycles, it closes as `stale-rumor-unverified`.
