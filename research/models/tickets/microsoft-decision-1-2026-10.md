---
slug: microsoft-decision-1-2026-10
title: "Microsoft-Decision-1 — decision-scoring model (scores options, generates no text), measured by Artificial Analysis"
company: Microsoft
model: Microsoft-Decision-1
status: released
status_note: |
  **2026-10-16 — independently measured → `released` / `partial`.**
  @ArtificialAnlys scores Microsoft-Decision-1 at 54 on its Decision Index v1.0 and
  prices it at $31 per 1M tasks. That makes the model live and purchasable. No
  Microsoft primary has been captured yet. The original claim of 2x Jev's speed does not
  match AA's Time per Task ranking, which lists Jev 1.14 and Celeris-1 Decision as
  faster.

  Single secondary source: @AntonMartyniuk (2026-10-14 11:40 UTC) says Microsoft
  released "Microsoft-Decision-1". It is a model that generates no text and
  instead returns a score for each option in a fixed list, for example a
  bug/feature/question classification for a ticket. The post claims it is 2x
  faster than Typesafe's Jev and 35x faster than (GPT-6.1) Sol. No Microsoft,
  Azure or MAI post, model card or catalog link was captured. The post also calls
  it Microsoft's "first AI model", which is false given the MAI line, so the
  source is unreliable.
expected: "Live: measured by Artificial Analysis on 2026-10-16 (Decision Index 54, $31 per 1M tasks). Open: a Microsoft/MAI/Azure post, Foundry catalog entry or model card."
labels:
  - microsoft
  - decision-model
  - unverified
verification: partial
sources:
  - "https://x.com/AntonMartyniuk/status/2110334967209165310"
  - "https://x.com/ArtificialAnlys/status/2111052531166249039"
created_at: 2026-10-14
updated_at: 2026-10-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-14
    change: "Created — RUMORED / unverified. A single secondary post (@AntonMartyniuk, 2026-10-14 11:40 UTC) claims Microsoft released 'Microsoft-Decision-1', a decision-scoring model that returns a score per option instead of generating text. It claims 2x Jev's speed and 35x Sol's. The post has no link, model card or Microsoft post, and its claim that this is Microsoft's 'first AI model' is wrong. Opened as rumored despite the 'released' wording because nothing in the signal corroborates it."
  - ts: 2026-10-16
    change: "RUMORED -> RELEASED; verification unverified -> partial. The model is now independently measured. @ArtificialAnlys (2026-10-16 11:11 UTC), in its d1-ultra write-up, lists Microsoft-Decision-1 on its Decision Index v1.0 at 54 (tied with GLiDE, behind d1-ultra 65 and Jev 1.14 57) and prices it at $31 per 1M tasks. A third-party benchmarker publishing a score and a per-task price means the model is live and purchasable, which matches the 2026-10-14 'released' claim this ticket held as rumor. Verification is partial, not confirmed, because no Microsoft, Azure or MAI post or Foundry entry has been captured. The source's 2x-Jev speed claim is not supported by the AA numbers, which do not put Decision-1 among the three fastest decision models."
---

This follows the decision-model category set by OpenAI's Decisions API on GPT-6
Luna ([[openai-decisions-api-2026-09]]) and Typesafe's Jev
([[typesafe-funding-round-2026-09]]; the Jev product ticket is closed). A
Microsoft entry would fit that trend, which makes the claim plausible but is not
evidence for it.

The source is weak. It is one post with a factual error and benchmark
comparisons with no link. It closes as `stale-rumor-unverified` if no Microsoft
artifact appears within about 15 cycles.

**2026-10-16 — measured, so live.** Artificial Analysis now scores and prices
Microsoft-Decision-1 alongside Jev 1.14, d1-ultra and GPT-6 Luna (Decisions).
The model exists and can be bought. The original post's speed claims do not hold
up against AA's numbers.
