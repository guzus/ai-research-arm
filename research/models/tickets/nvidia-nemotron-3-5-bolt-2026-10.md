---
slug: nvidia-nemotron-3-5-bolt-2026-10
title: "NVIDIA Nemotron 3.5 Bolt 74B-A9B — reported open-weight multimodal MoE with ~2-bit QAT weights"
company: "NVIDIA"
model: "Nemotron 3.5 Bolt 74B-A9B"
status: released
status_note: |
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
expected: "Reported released ~2026-10-16 with open weights. Open: an NVIDIA post or Hugging Face model card; independent head-to-head against Qwen3.6-35B-A3B."
labels:
  - nvidia
  - nemotron
  - open-weights
  - moe
  - quantization
  - unverified
verification: unverified
sources:
  - "https://x.com/Oluwaphilemon1/status/2111051657916064053"
  - "https://x.com/iamlukethedev/status/2111056522470174956"
created_at: 2026-10-16
updated_at: 2026-10-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-16
    change: "Created — RELEASED / unverified. A single secondary post (@Oluwaphilemon1, 2026-10-16 11:08 UTC) reports NVIDIA released Nemotron 3.5 Bolt 74B-A9B as open weights on Hugging Face. It is a 74B-total / 9B-active MoE shipped at ~2-bit via quantization-aware training (~22GB), with text/image/video input, 256K context and LiLiCorr speculative decoding. The post quotes NVIDIA's BF16-vs-IQ2 retention numbers (e.g. GPQA Diamond 88.83 -> 86.43). Model-card-level detail, but no NVIDIA primary captured, so unverified. Family context only: a Hermes changelog relay (@iamlukethedev) mentions 'Nemotron Super 3.5 defaults'. Prior Nemotron tickets are closed and untouched ([[nvidia-nemotron-3-ultra-imo-2026-09]])."
---

The notable part is the packaging. NVIDIA ships the 2-bit weights as the main
artifact, trained for that precision, instead of leaving quantization to the
community. That targets 24-48GB local GPUs directly.

It needs a primary source. If no NVIDIA post or model card appears within about 15
cycles, it closes as `stale-rumor-unverified`.
