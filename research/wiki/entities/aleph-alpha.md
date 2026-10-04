---
slug: aleph-alpha
title: Aleph Alpha
type: entity
aliases: ["Aleph Alpha", "Kolibri", "Kolibri-1", "Kolibri 1", "@Aleph__Alpha"]
tags: [open-weights, moe, europe, sovereign-ai, model-release]
description: Heidelberg European lab that returned to training with Kolibri-1, a 78B/3.46B-active Apache-2.0 MoE validated to 1M context.
created_at: 2026-10-04
timestamp: 2026-10-04T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-04", path: research/digest/2026-10-04-digest.md}
  - {title: "ARA model ticket — Aleph Alpha Kolibri-1", path: research/models/tickets/aleph-alpha-kolibri-1-2026-10.md}
---

**Aleph Alpha** is a Heidelberg European lab that
spent two years cited as the cautionary tale of
continental frontier ambitions — a well-funded
company that pivoted from training its own models
toward enterprise tooling. On **2026-10-03** it
reversed that pivot in public: **Kolibri-1**, a
**78.1B-total / 3.46B-active** mixture-of-experts
released under **Apache 2.0**, was the top AI
story on Hacker News (**470 points / 282
comments**). A staffer framed the drop as going
"back to the roots: train and release models,"
built in under a year alongside pipelines for
"upcoming releases" (@Aleph__Alpha, @SohirMaskey;
ARA daily digest 2026-10-04).

## Why it matters

- **A cheap-inference European open MoE, not a
  leaderboard bid.** 384 experts (1 shared, 6
  routed), context **trained to 262K and
  validated to 1M tokens**, four
  reasoning-effort levels, pretrained on **20T
  tokens** on **768 B200s over 21 days**. FP8
  weights are about **78 GB**. The data mix is
  about **62.5% English, 21.3% German and 14%
  code**. That is a sovereign-deployment shape
  — modest active parameters, a German document
  tilt, a permissive licence — next to
  [[mistral]] and [[soofi-s-30b-a3b]], not a
  claim to close on [[zhipu-glm-5-3|GLM-5.3]]
  or [[deepseek-v4-flash|DeepSeek V4 Flash]]
  (aleph-alpha.com, HN; ARA daily digest
  2026-10-04).
- **Community read is split and the training
  data is not a from-scratch story.** HN
  commenters praise German document reading and
  a low hallucination rate, and question
  general competitiveness. Ethan Mollick says
  the model was fine-tuned on [[zhipu|GLM]]-
  and [[alibaba|Qwen]]-generated data — a
  distillation/synthetic-data path, not a
  clean-room pretrain (Aleph Alpha, HN,
  @emollick; ARA daily digest 2026-10-04).
- **It is a European increment on the
  [[open-weights]] wave.** The 2026
  open-weight frontier has been mostly
  Chinese. Kolibri does not change that
  ranking, but it is a first-party Apache
  drop from a named European lab that had
  publicly left the training business. See
  [[eu-ai-regulation]] (ARA daily digest
  2026-10-04).

## Open questions

- **Does the 1M-context claim hold at 3.46B
  active?** Validated is not the same as a
  published long-context eval.
- **How much of Kolibri is original pretrain
  versus GLM/Qwen synthetic data?** Mollick's
  note is a single-source caveat; Aleph Alpha
  has not published a data card that would
  settle it.
- **Do the "upcoming releases" arrive as a
  family**, or is Kolibri-1 a one-off return
  to training?
