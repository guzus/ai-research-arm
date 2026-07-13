---
slug: soofi-s-30b-a3b
title: Soofi S 30B-A3B
type: entity
aliases: ["Soofi S", "Soofi S 30B-A3B", "Soofi"]
tags: [model-release, open-weights, sovereign-ai, germany, mixture-of-experts]
description: Deutsche Telekom-backed sovereign open German/English MoE foundation model trained on ~27T tokens, claimed strongest fully-open model on combined English+German benchmarks.
created_at: 2026-07-13
timestamp: 2026-07-13T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-13", path: research/digest/2026-07-13-digest.md}
---

**Soofi S 30B-A3B** is a sovereign open German/English **mixture-of-experts**
foundation model shipped **2026-07-13** by a Deutsche Telekom-backed lab,
trained on **~27 trillion tokens**. It is claimed to be the **strongest fully-
open model on combined English+German benchmarks**, ahead of **Olmo 3 32B**
and **Apertus 70B**, with **weights, data, and training code released under
permissive licenses** — an "open weights *and* open process" release rather
than a weights-only drop.

## Why it matters

- **A sovereign-AI entrant inside the [[open-weights]] wave.** Most of 2026's
  open-weight momentum has come from Chinese labs (Zhipu's
  [[zhipu-glm-5-2|GLM-5.2]], [[moonshot-kimi-k2-7-code|Kimi K2.7-Code]],
  [[deepseek|DeepSeek]]); Soofi S is a concrete **European sovereign-model**
  counterexample, backed by a national telecom incumbent rather than a
  frontier AI lab.
- **Lands the same day as a policy threat to the category.** Soofi S shipped
  on the same digest cycle that Nathan Lambert (Interconnects) flagged
  **White House discussions of a possible executive order on open-weight
  models** as "the most serious test to date of open source AI's
  viability" — see [[open-weights]] and [[federal-ai-policy]]. A US EO
  targeting open weights would not directly bind a Germany-based release, but
  it sharpens the contrast between sovereign-open strategies and a US policy
  environment that may move against the category.
- **Full-stack openness, not just weights.** Releasing training **data and
  code** alongside weights answers the "open weights are not enough"
  critique that has recurred through 2026 (see [[open-weights]]) — training-loop
  transparency, not just inference-time access.

## Open questions

- **Does the "strongest fully-open combined EN+DE" claim hold up to neutral
  eval?** The benchmark comparison against Olmo 3 32B and Apertus 70B is
  reported via the digest's single-source coverage; no independent
  leaderboard placement is confirmed yet.
- **Does a US executive order on open weights affect non-US sovereign
  releases like this one** — through export-control-adjacent mechanisms, or
  only US-based labs and distribution channels?
- **Follow-on releases.** Is Soofi S a one-off sovereign-AI demonstration or
  the first in a planned model family from the same lab?
