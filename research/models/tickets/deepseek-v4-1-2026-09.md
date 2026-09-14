---
slug: deepseek-v4-1-2026-09
title: DeepSeek V4.1 / V4.1 Flash — shipped, base weights withheld
company: DeepSeek
model: DeepSeek V4.1 / V4.1 Flash
status: released
status_note: |
  **DeepSeek V4.1 and V4.1 Flash are in third-party hands and being used**, but
  no DeepSeek announcement, model card or pricing page was captured in this
  cycle. The evidence is entirely incidental usage — which, for this lab, is the
  normal shape.

  What the usage establishes:
  - **V4.1 Flash is served and fast.** @Hikari_07_jp (2026-09-13 08:01 UTC)
    reports running it through the Commandcode GOAT reseller at ~$60/month of
    usage on a $10/month plan, measuring "TTFT of 4.2s, 204 tok/s" over a
    3,201-step run. That evidences availability through a broker, not a DeepSeek
    release event.
  - **V4.1 is being evaluated against Terminal-Bench.** @teortaxesTex
    (2026-09-14 10:20 UTC): "The discourse on benchmaxxing due to higher
    relative rank on TB 2.1 vs TB 4.0 is funny. V4.1 is almost anti-benchmaxxed.
    They clearly do not care about benchmarks, or even about user experience."
  - **The base model was NOT released** — the one clearly-negative fact, and the
    most decision-relevant. @teortaxesTex (12:17 UTC): "A bit annoyed that
    DeepSeek didn't release the V4.1 base model." His own stated counterpoint is
    logged too: "do you think you could even finetune it? … DeepSeeks might be
    the least finetuned bases historically."

  **Status `released`** (people are running it in production through paid
  routes), **verification `partial`** — no @deepseek_ai post, no model card, no
  first-party pricing, no parameter count, no context window, and no licence.
  The named gap is whether V4.1 is a point upgrade to the V4 line or a distinct
  generation.

  Relationship to existing tickets: this is the V4 line moving forward from
  [[deepseek-v4-flash-vision-exp-2026-08]] (released) and
  [[deepseek-v4-pro-price-cut-2026-05]]; the closed
  [[deepseek-v4-ga-surge-pricing-2026-06]] covers the V4 GA event. Opened as a
  new ticket rather than an update because V4.1 is a distinct model name with
  its own weights-release posture.
expected: "In use via API and resellers as of 2026-09-13/14. Pending: any DeepSeek first-party post, model card, pricing, parameter count and context window; and whether the V4.1 base weights are released later or withheld permanently."
labels:
  - deepseek
  - china
  - flash-tier
  - open-weights
  - released
verification: partial
sources:
  - https://x.com/teortaxesTex/status/2099472484869247006
  - https://x.com/teortaxesTex/status/2099443152222363731
  - https://x.com/teortaxesTex/status/2099470167667249534
  - https://x.com/Hikari_07_jp/status/2099045700965392860
created_at: 2026-09-14
updated_at: 2026-09-14
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-14
    change: "Created — RELEASED. DeepSeek V4.1 and V4.1 Flash are in third-party hands with no DeepSeek announcement, model card or pricing captured in-window; the entire record is incidental operator usage, which is this lab's normal release shape. @Hikari_07_jp (2026-09-13 08:01 UTC) measured V4.1 Flash through the Commandcode GOAT reseller at 'TTFT of 4.2s, 204 tok/s' over a 3,201-step run — evidence of availability via a broker, not of a DeepSeek release event. @teortaxesTex ran V4.1 Flash autonomously on a Rust task (12:07 UTC) and assessed V4.1 against Terminal-Bench (10:20 UTC): 'The discourse on benchmaxxing due to higher relative rank on TB 2.1 vs TB 4.0 is funny. V4.1 is almost anti-benchmaxxed. They clearly do not care about benchmarks, or even about user experience.' The load-bearing negative fact, same source (12:17 UTC): 'A bit annoyed that DeepSeek didn't release the V4.1 base model' — no open base weights this generation, with his own counterpoint logged ('do you think you could even finetune it? … DeepSeeks might be the least finetuned bases historically'). Verification partial: no @deepseek_ai post, model card, first-party pricing, parameter count, context window or licence. Opened as a new ticket rather than an update to [[deepseek-v4-flash-vision-exp-2026-08]] because V4.1 is a distinct model name with its own weights-release posture."
---

The interesting fact here is a non-release.

DeepSeek built its reputation on open base weights, and V4.1 shipped without
them. That is a posture change worth recording even from thin sourcing, because
it is the kind of thing that gets rationalised after the fact rather than
announced. The counter-argument came from the same person who raised it, and it
is a good one: DeepSeek bases have historically been among the least fine-tuned
open releases, because deployment alone is hard at that scale. If nearly nobody
used the open weights, withholding them costs the lab little and hands
competitors less.

The second observation is about what DeepSeek appears to be optimising. A model
that ranks higher on an older Terminal-Bench revision than a newer one is the
opposite of the usual failure mode — it suggests the lab is not tuning to the
current eval. Read generously, that is a lab building for internal research
goals rather than leaderboard position. Read less generously, "they clearly do
not care about … user experience" is the same observation with the compliment
removed. Both readings come from one operator and neither is established.

What would settle this ticket is mundane and still missing: a model card. Until
DeepSeek publishes one, everything above is inference from people who happen to
be paying for tokens — good evidence that the model exists and is served, and no
evidence at all about what it is.
