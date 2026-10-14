---
slug: microsoft-decision-1-2026-10
title: "Microsoft-Decision-1 — reported decision-scoring model (scores options, generates no text)"
company: Microsoft
model: Microsoft-Decision-1
status: rumored
status_note: |
  Single secondary source: @AntonMartyniuk (2026-10-14 11:40 UTC) says Microsoft
  released "Microsoft-Decision-1". It is a model that generates no text and
  instead returns a score for each option in a fixed list, for example a
  bug/feature/question classification for a ticket. The post claims it is 2x
  faster than Typesafe's Jev and 35x faster than (GPT-6.1) Sol. No Microsoft,
  Azure or MAI post, model card or catalog link was captured. The post also calls
  it Microsoft's "first AI model", which is false given the MAI line, so the
  source is unreliable.
expected: "Unknown. Advances on a Microsoft/MAI/Azure post, a Foundry catalog entry or a model card."
labels:
  - microsoft
  - decision-model
  - unverified
verification: unverified
sources:
  - "https://x.com/AntonMartyniuk/status/2110334967209165310"
created_at: 2026-10-14
updated_at: 2026-10-14
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-14
    change: "Created — RUMORED / unverified. A single secondary post (@AntonMartyniuk, 2026-10-14 11:40 UTC) claims Microsoft released 'Microsoft-Decision-1', a decision-scoring model that returns a score per option instead of generating text. It claims 2x Jev's speed and 35x Sol's. The post has no link, model card or Microsoft post, and its claim that this is Microsoft's 'first AI model' is wrong. Opened as rumored despite the 'released' wording because nothing in the signal corroborates it."
---

This follows the decision-model category set by OpenAI's Decisions API on GPT-6
Luna ([[openai-decisions-api-2026-09]]) and Typesafe's Jev
([[typesafe-funding-round-2026-09]]; the Jev product ticket is closed). A
Microsoft entry would fit that trend, which makes the claim plausible but is not
evidence for it.

The source is weak. It is one post with a factual error and benchmark
comparisons with no link. It closes as `stale-rumor-unverified` if no Microsoft
artifact appears within about 15 cycles.
