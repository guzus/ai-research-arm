---
slug: openbmb-minicpm-v-4-7-2026-10
title: "MiniCPM-V 4.7 — OpenBMB weights appear on ModelScope with no announcement"
company: "OpenBMB"
model: "MiniCPM-V 4.7"
status: in-testing
status_note: |
  **Single-source artifact sighting, 2026-10-07 12:31 UTC (@anxuanng).**
  "OpenBMB just uploaded MiniCPM-V 4.7 to ModelScope with no announcement and an
  empty model card. 35B total and 3B active by the name, 70 GB of bf16 weights.
  the config looks like a Qwen3.5 35B A3B backbone with hybrid linear attention
  and 262k context."

  `in-testing` because an uploaded weights repo is an artifact, not a tease;
  `unverified` because one account reports it, the model card is empty, and there
  is no OpenBMB statement, benchmark or licence.
expected: "Weights reportedly uploaded to ModelScope 2026-10-07 without a card. Watch for an OpenBMB announcement, a populated model card/licence, Hugging Face mirror, and benchmarks — any of which advances this to released/confirmed."
labels:
  - openbmb
  - open-weights
  - multimodal
  - moe
  - leak
  - china
verification: unverified
sources:
  - https://x.com/anxuanng/status/2107811004726014141
created_at: 2026-10-07
updated_at: 2026-10-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-07
    change: "Created — IN-TESTING / unverified. @anxuanng (2026-10-07 12:31 UTC) reports OpenBMB uploaded MiniCPM-V 4.7 to ModelScope with no announcement and an empty model card: 35B total / 3B active per the name, ~70 GB bf16, config resembling a Qwen3.5-35B-A3B backbone with hybrid linear attention and 262K context. Single source; no OpenBMB statement, licence or benchmarks."
---

MiniCPM-V is OpenBMB's on-device vision-language line, historically small
dense models. A 35B-A3B MoE on a Qwen backbone would be a change of shape for
the series — which is exactly the kind of detail an empty-card upload cannot
confirm.

Silent repository uploads ahead of announcement are a common Chinese-lab release
pattern, so the sighting is plausible; it is still one account reading a config
file. If no corroboration arrives within ~15 cycles this closes as
stale-rumor-unverified.
