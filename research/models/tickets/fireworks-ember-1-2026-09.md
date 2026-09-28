---
slug: fireworks-ember-1-2026-09
title: Ember-1 — Fireworks AI's Kimi K3 post-train, ~40% more concise reasoning
company: Fireworks AI / Moonshot AI (Kimi K3 base)
model: Ember-1
status: released
status_note: |
  **First-party, 2026-09-27 20:45 UTC.** @dzhulgakov (Fireworks AI co-founder /
  CTO), in the company's voice: "**Ember-1** is hot on HN, our research team
  cooked — it's **Kimi K3 post trained to be 40% more concise in reasoning**,
  same quality, **40% faster and cheaper**."

  **The disclosure is the notable part.** Fireworks named its base model in the
  launch post rather than letting it be discovered. @rasbt, who had previously
  reverse-engineered an undisclosed lineage from config files, called that out
  explicitly: "kudos to fireworks AI for admitting that they built on top of Kimi
  (I remember the awkward Mistral 3 release)" — his earlier finding being that
  Mistral 3 Large used the DeepSeek V3 architecture including MLA. Voluntary
  base-model attribution is not the norm in this category and is the cleanest
  fact on this ticket.

  **@rasbt's second point is the strategic one, and he states it as his own
  recommendation rather than as a result:** asked how to build a frontier LLM
  today on a modest budget, "start with an existing one and spend that budget on
  post-training. Great example here."

  **What the claim actually is, stated narrowly.** Not "a better model" —
  **the same quality at ~40% fewer reasoning tokens**, which converts directly
  into latency and cost. That is a serving-economics result, and for an inference
  provider it is the result that matters: Fireworks sells tokens, so shortening
  the chain of thought on a strong open base improves its own unit economics and
  its customers' bills simultaneously.

  **Verification `confirmed` on the release, with the benchmark gap named.**
  The company's own CTO announcing a shipped model clears the primary bar. The
  **40% figures are Fireworks' own, against an unstated evaluation suite**, with
  no model card, licence, parameter count, context window, weights location or
  independent reproduction captured in-window. "Same quality" is the specific
  claim needing outside measurement.

  **Corporate context.** Fireworks is simultaneously reported to be weighing a
  round at a ~$30B valuation ([[fireworks-funding-round-2026-09]]), and is the
  provider behind several profiles in this repo's own backend routing. A
  first-party model raises its multiple from "inference vendor" toward "lab" —
  @quxiaoyin described the playbook in-window without naming anyone: host the
  strong Chinese open weights, sell the inference, ship a model of your own, and
  raise on the blended story.
expected: "Released and on Hacker News. Open: licence and weights location, the evaluation suite behind the 40%-conciseness and same-quality claims, parameter count and context window, whether Moonshot's Kimi K3 licence permits this commercially, pricing on Fireworks, and any independent reproduction."
labels:
  - fireworks
  - post-training
  - kimi
  - open-weights-derivative
  - inference-economics
  - released
verification: confirmed
sources:
  - https://x.com/dzhulgakov/status/2104311573640855903
  - https://x.com/rasbt/status/2104326522354147793
  - https://x.com/rasbt/status/2104333634329247985
created_at: 2026-09-28
updated_at: 2026-09-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-28
    change: "Created — RELEASED. Fireworks AI co-founder @dzhulgakov announced Ember-1 on 2026-09-27 20:45 UTC: Moonshot's Kimi K3 post-trained to be ~40% more concise in reasoning at the same quality, hence ~40% faster and cheaper. Verification confirmed on the first-party announcement; the 40% figures are Fireworks' own against an unstated eval suite, with no model card, licence, parameter count, context window or independent reproduction in-window. The genuinely distinguishing fact is disclosure: Fireworks named its base model in the launch post rather than leaving it to config-file archaeology, which @rasbt contrasted favourably with the Mistral 3 Large / DeepSeek V3 architecture episode he had previously uncovered. Recorded as a serving-economics result, not a capability result — shortening the reasoning chain on a strong open base is what an inference vendor monetises. Corporate context on [[fireworks-funding-round-2026-09]]."
---

Ember-1 is not a claim to have built a better model. It is a claim to have made
a good one cheaper to run: Kimi K3, post-trained to reach the same answers with
roughly 40% fewer reasoning tokens.

For an inference provider that is the highest-leverage thing to work on. Fireworks
serves tokens for a living and says it moves more than 40 trillion a day; a 40%
cut in reasoning length on a popular open base improves gross margin and the
customer's invoice at the same time. It also sidesteps the capital problem — the
post-training budget for this is a rounding error against a pretraining run.

The part worth crediting is the attribution. Providers shipping derivatives of
Chinese open-weight models have not reliably said so, and the space has a recent
history of the lineage being found rather than disclosed. Fireworks led with it.

What is still missing is everything that would let anyone check the claim. "Same
quality" is doing the entire load, against no named benchmark, with no model card
and no third-party run. Until that appears, Ember-1 is a credible first-party
efficiency claim on a disclosed base — which is more than this category usually
offers, and less than a measurement.

The open licensing question is not cosmetic: whether Moonshot's Kimi K3 terms
permit a commercial post-trained derivative served at scale determines whether
this is a business or a liability.
