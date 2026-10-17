---
slug: openbmb-minicpm-v-4-7-2026-10
title: "MiniCPM-V 4.7 — OpenBMB weights appear on ModelScope with no announcement"
company: "OpenBMB"
model: "MiniCPM-V 4.7"
status: released
status_note: |
  **2026-10-17 — RELEASED / partial.** @DogukanUrker's week-in-open-weights roundup lists
  "MiniCPM-V 4.7 1B + 35B-A3B" as released this week. That is independent of the
  2026-10-07 ModelScope sighting below. There is still no OpenBMB post or populated card.

  **Single-source artifact sighting, 2026-10-07 12:31 UTC (@anxuanng).**
  "OpenBMB just uploaded MiniCPM-V 4.7 to ModelScope with no announcement and an
  empty model card. 35B total and 3B active by the name, 70 GB of bf16 weights.
  the config looks like a Qwen3.5 35B A3B backbone with hybrid linear attention
  and 262k context."

  `in-testing` because an uploaded weights repo is an artifact, not a tease;
  `unverified` because one account reports it, the model card is empty, and there
  is no OpenBMB statement, benchmark or licence.
expected: "Released the week of 2026-10-12 (1B and 35B-A3B per one roundup). Open: OpenBMB announcement, populated model card/licence, Hugging Face mirror, benchmarks."
labels:
  - openbmb
  - open-weights
  - multimodal
  - moe
  - released
  - china
verification: partial
sources:
  - "https://x.com/DogukanUrker/status/2111337663286706405"
  - "https://x.com/xeonai44/status/2111394393383141839"
  - https://x.com/anxuanng/status/2107811004726014141
created_at: 2026-10-07
updated_at: 2026-10-17
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-07
    change: "Created — IN-TESTING / unverified. @anxuanng (2026-10-07 12:31 UTC) reports OpenBMB uploaded MiniCPM-V 4.7 to ModelScope with no announcement and an empty model card: 35B total / 3B active per the name, ~70 GB bf16, config resembling a Qwen3.5-35B-A3B backbone with hybrid linear attention and 262K context. Single source; no OpenBMB statement, licence or benchmarks."
  - ts: 2026-10-17
    change: "IN-TESTING -> RELEASED; verification unverified -> partial. A second, independent account now treats MiniCPM-V 4.7 as a released open-weight model. @DogukanUrker's 2026-10-17 06:05 UTC roundup of this week's open-weight releases lists 'MiniCPM-V 4.7 1B + 35B-A3B' and says they ran configs and benchmarks for several models on the list. @xeonai44 relayed the list. That matches the 35B-A3B shape @anxuanng read from the ModelScope config on 2026-10-07 and adds a 1B variant. Still no OpenBMB announcement, model card, or licence captured, so verification stops at partial."
---

MiniCPM-V is OpenBMB's on-device vision-language line, historically small
dense models. A 35B-A3B MoE on a Qwen backbone would be a change of shape for
the series — which is exactly the kind of detail an empty-card upload cannot
confirm.

Silent repository uploads ahead of announcement are a common Chinese-lab release
pattern, so the sighting is plausible; it is still one account reading a config
file. If no corroboration arrives within ~15 cycles this closes as
stale-rumor-unverified.
