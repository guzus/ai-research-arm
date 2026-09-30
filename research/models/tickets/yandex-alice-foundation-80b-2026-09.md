---
slug: yandex-alice-foundation-80b-2026-09
title: Yandex AliceAI-Foundation-80B-A3B-Base — reported 80B MoE beating its 235B predecessor
company: Yandex
model: AliceAI-Foundation-80B-A3B-Base
status: rumored
status_note: |
  **One source, but an unusually specific one.** @GarinArtyom, 2026-09-30 03:45
  UTC: AliceAI-Foundation-80B-A3B-Base "outperform[s] the previous Alice AI LLM on
  factual knowledge, math, coding, and long-context tasks while using roughly one-
  third as many total parameters." Architecture as described: MoE with **512 routed
  experts**, the router picking **10 plus one shared expert** per token, so **~80B
  total / ~3B active**. The predecessor is described as **continued from
  Qwen3-235B-A22B** — 235B total, ~22B active.

  **Why the specificity is the evidence, and why it still is not enough.** The
  naming convention (`-80B-A3B-Base`) is the standard open-weights format encoding
  total and active parameters, and the 512/10+1 routing detail plus the named
  Qwen3-235B-A22B lineage are the kind of facts that come from a model card rather
  than from imagination. But: no link, no HuggingFace reference, no benchmark table,
  no license, no Yandex official post, and no second mention anywhere in this
  cycle's 131 retained signal groups. Status `rumored`, verification `unverified`.

  **The claim's substance is an architecture argument, not a leaderboard claim.**
  The interesting assertion is that a much larger pool of much smaller experts
  (512 experts, 10 active) gives the router more specialization options at ~3B
  active compute, and that this beats 22B active drawn from a smaller expert pool.
  That is a testable statement about MoE sparsity ratios rather than a marketing
  line — which is why it is worth recording even at single-source strength.

  **First Yandex ticket in this set.** No prior Alice/Yandex model ticket exists,
  so there is nothing to dedup against; the closest comparators are the Qwen
  continued-pretrain lineage ([[alibaba-qwen-4-architecture-2026-08]], closed) and
  other sparse-MoE releases.
expected: "REPORTED 2026-09-30, single source. Open: a Yandex primary announcement or model card; whether weights are actually published and under what license; the benchmark table behind the 'outperforms on factual knowledge, math, coding and long-context' claim; context length; and whether the predecessor really was a Qwen3-235B-A22B continued pretrain. If nothing corroborates within ~15 cycles, close as stale-rumor-unverified."
labels:
  - yandex
  - open-weights
  - moe
  - unverified
  - architecture
verification: unverified
sources:
  - https://x.com/GarinArtyom/status/2105142078107726315
created_at: 2026-09-30
updated_at: 2026-09-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-30
    change: "Created — RUMORED / unverified. @GarinArtyom (2026-09-30 03:45 UTC, with an attached chart) reports Yandex's AliceAI-Foundation-80B-A3B-Base outperforming the previous Alice AI LLM on factual knowledge, math, coding and long-context tasks at roughly one third the total parameters, and supplies the architecture: MoE with 512 routed experts, 10 routed plus 1 shared expert active per token, ~80B total and ~3B active, against a predecessor described as continued from Qwen3-235B-A22B at 235B total and ~22B active. Single source with NO link, model card, HuggingFace reference, benchmark table, license or Yandex post, and no second mention across the 131 retained signal groups — hence rumored/unverified. WHAT MAKES IT WORTH A TICKET AT THAT STRENGTH: the details are model-card-shaped rather than hype-shaped. The '-80B-A3B-Base' suffix is the standard open-weights encoding of total/active parameters, the 512-expert / 10+1-active routing configuration is a concrete design choice, and naming Qwen3-235B-A22B as the predecessor's base is a specific and falsifiable lineage claim. The substantive assertion is an ARCHITECTURE argument — that a large pool of small experts gives the router more specialization headroom at a fraction of the active compute, and beats a smaller pool with 22B active — which is testable rather than promotional. FIRST YANDEX/ALICE TICKET in this set, so there is nothing to dedup against; nearest comparators are the Qwen continued-pretrain lineage at [[alibaba-qwen-4-architecture-2026-08]] (closed) and other sparse-MoE releases. Close trigger: no corroboration within ~15 cycles closes as stale-rumor-unverified."
---

The claim here is not "our model is better." It is "sparsity ratio is the lever,"
and that is a more interesting thing to be right or wrong about.

If the numbers as described hold — ~3B active parameters outperforming ~22B active
on knowledge, math, code and long context — then the gain is not coming from
compute. It is coming from having 512 experts to route among instead of a smaller
set, so each expert can specialise harder while the per-token cost stays tiny. That
is the design direction several labs have been drifting toward, and it is the
argument behind the recurring "looped transformers / much smaller than you think"
discourse around frontier models this quarter. A concrete open-weights datapoint at
80B/3B would be a useful public test of it.

The reason this sits at `rumored` is simply that none of it can be checked from what
was posted. There is no model card, no repository, no benchmark table, no license,
and no Yandex statement — and Yandex releasing an open-weights foundation model
would ordinarily come with all of those plus a blog post. What was posted is one
practitioner's summary, and while its details read like they came from documentation,
"reads like documentation" is not a source.

One specific claim is worth checking first if corroboration appears, because it is
load-bearing for the whole comparison: that the *predecessor* was a continued
pretrain of Qwen3-235B-A22B. If true, the headline result is a from-scratch (or
differently-based) 80B beating a continued-pretrain of a much larger Chinese
open-weights model — which says something about continued pretraining as a strategy
as much as about sparsity. If the lineage is wrong, the parameter comparison loses
most of its meaning.
