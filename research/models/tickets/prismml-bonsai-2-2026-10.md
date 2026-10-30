---
slug: prismml-bonsai-2-2026-10
title: "PrismML Bonsai 2 — second-generation ternary compression, reported to shrink Qwen3.8-27B from 55.6GB to 5.9GB at 98.2% retention"
company: "PrismML"
model: "Bonsai 2"
status: confirmed
status_note: |
  Single secondary source (@Oluwaphilemon1, 2026-10-30 13:06 UTC). PrismML, the team behind Bonsai, has
  introduced a second-generation compression system using ternary quantization. Reported numbers: Qwen3.8-27B goes from
  55.6GB to 5.9GB (−89.4%) and keeps 98.2% of aggregate benchmark performance across 20 benchmarks. The first-generation
  Bonsai 27B retained about 95%. No PrismML post, weights link or licence was captured.
expected: "Reported 2026-10-30. Open: PrismML announcement, whether compressed weights are downloadable, independent evals."
labels:
  - open-weights
  - quantization
  - compression
verification: unverified
sources:
  - https://x.com/Oluwaphilemon1/status/2116154889596276921
created_at: 2026-10-30
updated_at: 2026-10-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-30
    change: "Created — CONFIRMED / unverified. @Oluwaphilemon1 reports PrismML introduced Bonsai 2, a second-generation ternary-quantization system: Qwen3.8-27B at 5.9GB (from 55.6GB, −89.4%) with 98.2% aggregate benchmark retention over 20 benchmarks, vs ~95% for the first-generation Bonsai 27B. Unverified: one relay, no PrismML post, weights link or licence in signal. Predecessor is the closed [[prismml-bonsai-27b]]."
---
This is the successor artifact to the closed [[prismml-bonsai-27b]], which stays closed. The base model is
Alibaba's Qwen3.8-27B ([[alibaba-qwen-3-8-27b-2026-08]], closed).

The claim worth testing is retention, not size. Ternary weights at ~2 bits/param are not new. Keeping 98% of
a 27B model's aggregate score across 20 benchmarks would be, and aggregate scores can hide large regressions
on individual tasks. Status is confirmed in the reported-introduction sense. Move to released when downloadable
weights are confirmed, and close as stale-rumor-unverified if no primary source appears within ~15 cycles.
