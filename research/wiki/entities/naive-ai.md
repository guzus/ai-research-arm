---
slug: naive-ai
title: Naive AI
type: entity
aliases: ["Naive AI", "Naive-N0.5-Flash", "N0.5-Flash", "NaiveRT", "@naiveailab"]
tags: [open-weights, moe, model-release, inference]
description: Lab behind N0.5-Flash, a 309B MIT-licensed MoE (15.5B active, native 1M context) continued-pretrained on Xiaomi's MiMo-V2.5.
created_at: 2026-09-28
timestamp: 2026-09-28T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-28", path: research/digest/2026-09-28-digest.md}
---

**Naive AI** is the lab that shipped **N0.5-Flash** on
27 September 2026: a 309B-parameter MIT-licensed
mixture-of-experts model (15.5B active, native 1M
context) continued-pretrained on Xiaomi's
[[xiaomi-mimo-v2-5-pro|MiMo-V2.5]] after an
attention swap. This is the lab's first wiki page;
the significant artifact is the model, not a priced
startup round.

## Why it matters

- **First-party MIT weights, not a leak
  (2026-09-28).** 309B MoE / 15.5B active, 48
  layers (39 SWA + 9 DSA, no full-attention
  layers), native 1M context, ~315 GB FP8, MIT
  weights on [[hugging-face|Hugging Face]].
  Continued pretraining after the attention swap:
  **3.25T tokens**. A posted **$0.10 / $0.40 /
  $0.01** API card is not yet a confirmed live
  endpoint. Source is promised **12 October**.
  Downloads were still near zero hours after the
  drop (@naiveailab, naive.ai, Hugging Face; ARA
  daily digest 2026-09-28).
- **NaiveRT serving claims stay lab charts.**
  Standard mode is claimed at **50 tok/s per
  user**; a one-second peak of **2,122 tok/s** on
  8 GPUs with thinking off. A 400-hour AutoWM run
  is scored **77.43** on WorldArena-1 Track 1 vs
  a previous published high of **73.64**. Hold
  both as first-party exhibits, not an
  independent bakeoff (Naive AI; ARA daily digest
  2026-09-28).
- **Continued pretraining on an existing open
  stack.** Starting from [[xiaomi-mimo-v2-5-pro]]
  rather than a from-scratch pretrain puts this
  ship on the [[open-weights]] lane next to
  other MIT / Apache drops, not as a new frontier
  lab. [[fireworks-ai|Ember-1]] shipped the same
  Sunday as a closed K3 specialist — the pair is
  open-weights reuse vs closed distillation.

## Open questions

- **Does the $0.10 / $0.40 / $0.01 card become a
  live endpoint?** A posted card is not a
  confirmed serving path.
- **Do 12 October sources actually appear?** An
  announced date is the same gap
  [[step-5-preview]] and [[zhipu-glm-5-3]]
  carried as weight-release promises.
- **Does WorldArena-1 77.43 survive an
  independent run?** The 73.64 prior high is a
  lab comparison, not a third-party board.
