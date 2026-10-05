---
slug: aleph-alpha-kolibri-1-2026-10
title: Aleph Alpha releases Kolibri-1 — 78B-total / 3.46B-active open-weight MoE under Apache 2.0
company: Aleph Alpha
model: Kolibri-1
status: released
status_note: |
  **Official, first-party.** @Aleph__Alpha (2026-10-03 08:54 UTC): "Small bird,
  fast wings, Kolibri is here. 78B parameters. 3.46B active. Up to 1M tokens of
  context. Built in Europe. Now the weights are yours. Run it on your own
  hardware, under Apache 2.0." An Aleph Alpha team member (@SohirMaskey) frames
  it as the company going "back to the roots: train and release models", built
  in under a year alongside the pipelines for "upcoming releases".

  **What is and is not known.** Size, active parameters, context window and
  licence come from the company. No benchmark table, model card details or
  hosted-API pricing reached this desk in-window.

  **2026-10-05 — reception, contested.** Aleph Alpha followed up on its own
  handle (06:06 UTC, ~532 likes): "Built in Germany from scratch and on
  infrastructure in Europe… This weekend, we released Kolibri." Relays call it a
  "SOTA open-weight model" that beats Qwen, Mistral and Nemotron at similar
  active-parameter count (@charles_maddock); replies dispute that framing as a
  comparison against older ~3B-active models (@TheDevilCloud). Still no
  benchmark table captured, so the SOTA claim is unverified.
expected: "Released 2026-10-03 as open weights (Apache 2.0). Open: published benchmarks and a model card; independent evals of the 1M-context claim at 3.46B active; whether Aleph Alpha follows with larger releases as its staff post implies."
labels:
  - open-weights
  - moe
  - europe
  - sovereign-ai
verification: confirmed
sources:
  - https://x.com/Aleph__Alpha/status/2106306840657297814
  - https://x.com/SohirMaskey/status/2106313014186303685
  - https://x.com/Aleph__Alpha/status/2106989436839858676
  - "@charles_maddock"
  - "@TheDevilCloud"
created_at: 2026-10-03
updated_at: 2026-10-05
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-03
    change: "Created — RELEASED / confirmed. @Aleph__Alpha announced Kolibri-1 on its own handle (2026-10-03 08:54 UTC): 78B total parameters, 3.46B active, up to 1M tokens of context, weights released under Apache 2.0. Aleph Alpha staffer @SohirMaskey adds that the model and its training pipelines were built in under a year and that more releases are planned. Released because the weights are downloadable by anyone; confirmed because the source is the company's own account. No benchmarks or model-card details captured in-window."
  - ts: 2026-10-05
    change: "Released, unchanged. Aleph Alpha's own follow-up thread (2026-10-05 06:06 UTC, ~532 likes) restates that Kolibri was built in Germany from scratch on European infrastructure and introduces the team. Third-party reception is split: @charles_maddock calls it a SOTA open-weight model beating Qwen, Mistral and Nemotron at similar active-parameter count; @TheDevilCloud replies that the comparison is against older ~3B-active models and 'is not SOTA'. No benchmark table captured in-window, so the SOTA claim stays unverified."
---

Aleph Alpha spent the last two years being cited as the cautionary tale of
European frontier ambitions: a well-funded lab that pivoted away from training
its own models toward enterprise tooling. Kolibri-1 is the company publicly
reversing that pivot, and its own staff say so in as many words.

The shape is the interesting part. A 78B mixture-of-experts with only ~3.5B
parameters active per token is built for cheap inference on modest hardware,
not for leaderboard rank, and the 1M-token context claim is the headline
capability. Paired with an Apache 2.0 licence, it is pitched squarely at the
European sovereign-deployment buyer — the same market Mistral is chasing in
[[france-sovereign-ai-procurement-2026-08]] and [[mistral-humain-saudi-2026-08]].

What is missing is everything that would let anyone rank it: no benchmark
table, no long-context eval, no comparison to Qwen3.8 or DeepSeek V4 Flash in
the same active-parameter class. Until those exist, this ticket tracks a
release, not a result.
