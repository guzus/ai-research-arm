---
slug: nvidia-nemotron-3-5-super-vl-2026-10
title: "NVIDIA Nemotron 3.5 Super VL — 120B-total / 12B-active open multimodal model for long-running agents"
company: NVIDIA
model: Nemotron 3.5 Super VL
status: released
status_note: |
  **Released 2026-10-16 (multiple independent secondary sources).**
  @testingcatalog's 2026-10-16 brief: "NVIDIA released Nemotron 3.5 Super VL, an open
  120B-total, 12B-active multimodal model for long-running AI agents." It is also
  available in Perplexity for Pro and Max subscribers and in Perplexity's Agent API.
  @ArtificialAnlys (2026-10-16 00:41 UTC, quoted by @Mekarly) calls it the
  next-highest-scoring US open-weights model after Muse Spark Open. It scores 26 on
  the AA Intelligence Index and "launched today". @DogukanUrker's week-in-open-weights
  roundup lists "Super VL 120B".

  `partial` because no NVIDIA post or Hugging Face model card was captured in this
  window.
expected: "Released 2026-10-16 (open weights; Perplexity Pro/Max and Agent API). Open: NVIDIA primary post / model card and licence."
labels:
  - nvidia
  - nemotron
  - open-weights
  - multimodal
  - agents
  - released
verification: partial
sources:
  - "https://x.com/testingcatalog/status/2111409303701577925"
  - "https://x.com/ArtificialAnlys/status/2110893784422908225"
  - "https://x.com/Mekarly/status/2111407881585136042"
  - "https://x.com/DogukanUrker/status/2111337663286706405"
created_at: 2026-10-17
updated_at: 2026-10-17
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-17
    change: "Created — RELEASED / partial. Nemotron 3.5 Super VL, a 120B-total / 12B-active open multimodal model for long-running agents, launched 2026-10-16 per @testingcatalog's 2026-10-16 brief. @ArtificialAnlys scores it 26 on its Intelligence Index, second among US open-weights models behind [[meta-muse-spark-open-2026-10]]. Perplexity added it for Pro/Max and the Agent API. Sibling small model: [[nvidia-nemotron-3-5-bolt-2026-10]]. No NVIDIA primary captured."
---

This is the larger member of the Nemotron 3.5 family that showed up this week,
next to the 24GB-class Bolt ([[nvidia-nemotron-3-5-bolt-2026-10]]). A Hermes
changelog had already mentioned "Nemotron Super 3.5 defaults" on 2026-10-16.

On Artificial Analysis it sits well behind Meta's much larger Muse Spark Open (26
vs 39). At 12B active it is a different cost class, and Perplexity shipping it on
day one makes it a practical agent backend.

**Transition triggers:** NVIDIA post or model card → verification `confirmed`;
about four weeks after release → close as released-and-aged.
