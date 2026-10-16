---
slug: liquid-ai-d1-ultra-2026-10
title: "Liquid AI releases d1-ultra — decision model, #1 on Artificial Analysis Decision Index v1.0"
company: "Liquid AI"
model: "d1-ultra"
status: released
status_note: |
  **Released per Artificial Analysis, 2026-10-16 11:11 UTC.** @ArtificialAnlys: "Liquid
  AI has released d1-ultra, taking the #1 position on the Artificial Analysis Decision
  Index v1.0". Score 65, ahead of Jev 1.14 (57), GLiDE and Microsoft-Decision-1 (54).
  It follows Liquid's d1 from earlier this month. Pricing is $0.042 per 1M input tokens
  (d1: $0.02), billed on input only, or $32 per 1M tasks.

  The lead comes from abstention. The non-hallucination rate on AA-Omniscience-Decision
  is 85% (d1: 2%), but accuracy fell to 32% (d1: 41%). Time per Task is 92 ms, the third
  lowest.

  AA is an independent benchmarker, not Liquid AI, so verification is `partial`. No
  @liquidai post was captured.
expected: "Released 2026-10-16. Open: a Liquid AI primary post or model card."
labels:
  - liquid-ai
  - decision-model
  - released
  - benchmark
verification: partial
sources:
  - "https://x.com/ArtificialAnlys/status/2111052531166249039"
created_at: 2026-10-16
updated_at: 2026-10-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-16
    change: "Created — RELEASED / partial. @ArtificialAnlys (2026-10-16 11:11 UTC) reports Liquid AI released d1-ultra, a decision model that takes #1 on AA's Decision Index v1.0 at 65 (Jev 1.14 57; GLiDE and Microsoft-Decision-1 54). It is priced at $0.042 per 1M input tokens, input-only billing, or $32 per 1M tasks. The gain comes from abstaining more: non-hallucination 85% vs d1's 2%, but accuracy 32% vs 41%. Time per Task is 92 ms. The predecessor d1 (earlier in October) had no ticket. Independent benchmarker, no Liquid primary captured → partial. Category peers: [[typesafe-jev-1-14-2026-10]], [[microsoft-decision-1-2026-10]], [[openai-decisions-api-2026-09]]."
---

Decision models (score a fixed list of options, generate no text) became a
category in a few weeks: OpenAI's Decisions API on GPT-6 Luna
([[openai-decisions-api-2026-09]]), TypeSafe's Jev ([[typesafe-jev-1-14-2026-10]]),
Microsoft-Decision-1 ([[microsoft-decision-1-2026-10]]), and now Liquid's d1 line.

d1-ultra tops the index by declining to answer more often, not by being more accurate.
Its accuracy dropped 9 points. Whether that trade suits a buyer depends on how much a
wrong answer costs compared with no answer.
