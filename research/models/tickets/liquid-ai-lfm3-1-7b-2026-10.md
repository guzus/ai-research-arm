---
slug: liquid-ai-lfm3-1-7b-2026-10
title: "Liquid AI LFM3-1.7B — small tri-hybrid model for local agents (reported)"
company: "Liquid AI"
model: "LFM3-1.7B"
status: released
status_note: |
  **Single secondary relay, 2026-10-28 13:10 UTC (@Oluwaphilemon1).** It describes Liquid AI's
  LFM3-1.7B as a tri-hybrid model for local inference and agents: ~1.1GB as Q4_K_M GGUF, 256K context,
  native tool calling. Liquid's reported scores against Qwen3.5-9B are WebArena Verified 38.4 vs 28.9,
  AutomationBench 41.3 vs 15.1, LiveClaw 45.6 vs 35.8, ToolSandbox 80.4 vs 76.4 and Claw-Eval 68.6 vs
  66.5. Decoding is ≥1.8× and prefill 2.5× faster at 32K.

  **Status `released`** because the relay describes downloadable GGUF weights. **Verification
  `unverified`:** one relay, no Liquid post, and **no release date in the signal**. It may predate this
  window.
expected: "Weights reportedly available (GGUF). Open: Liquid AI announcement and date, licence, independent agent-benchmark results."
labels:
  - liquid-ai
  - small-model
  - on-device
  - agents
  - open-weights
verification: unverified
sources:
  - "https://x.com/Oluwaphilemon1/status/2115430969842819125"
created_at: 2026-10-28
updated_at: 2026-10-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-28
    change: "Created — RELEASED / unverified. A single relay describes Liquid AI's LFM3-1.7B (tri-hybrid, ~1.1GB Q4 GGUF, 256K context, tool calling) beating Qwen3.5-9B on five Liquid-reported agent benchmarks. No release date or Liquid post captured."
---
First LFM3-generation model in this set. Earlier Liquid tickets: [[liquid-ai-lfm2-5-230m-2026-06]] (closed)
and [[liquid-ai-d1-ultra-2026-10]]. All benchmark numbers are Liquid's own, as the relay itself notes.
