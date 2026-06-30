---
slug: deepseek-v4-ga-surge-pricing-2026-06
title: DeepSeek dates V4 GA for mid-July with first-of-its-kind API surge pricing
company: DeepSeek
model: DeepSeek V4 (Pro + Flash)
status: confirmed
status_note: |
  Reported **2026-06-29/30** across 10+ independent accounts relaying a
  **DeepSeek email to API users**: **V4-Pro and V4-Flash** (~1M context) leave
  preview **mid-July GA**, paired with the first major LLM **time-of-day demand
  pricing** — **peak hours cost ~2× off-peak** (relayed as 9:00–12:00 and
  14:00–18:00 Beijing time, ~seven peak hours/day, off-peak unchanged). The
  mid-July date is corroborated by @AndrewCurran_ ("the Whale arrives in about
  two weeks"). V4-Flash is already in wide use, so "V4" here means **full GA**,
  not a first appearance. Email relayed consistently by many accounts → status
  `confirmed`; **peak-window details diverge across reposters** (Beijing vs UTC)
  and **no official DeepSeek pricing page** was surfaced → verification
  `partial`.
expected: "Mid-July 2026 GA. Pending: official DeepSeek pricing page / API changelog with exact peak windows and per-token rates; whether competitors copy time-of-day pricing"
labels:
  - frontier-model
  - pricing
  - china
  - deepseek
  - upcoming
verification: partial
sources:
  - "@alephantai"
  - "@MikelEcheve"
  - "@AndrewCurran_"
  - "@teortaxesTex"
  - https://x.com/alephantai/status/2071621413711094240
  - https://x.com/AndrewCurran_/status/2071590515909480648
created_at: 2026-06-30
updated_at: 2026-06-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-30
    change: "Created — DeepSeek emailed API users (relayed 2026-06-29/30 by 10+ accounts) that V4-Pro and V4-Flash (~1M context) leave preview for mid-July GA, paired with first-of-its-kind LLM time-of-day surge pricing: peak hours ~2× off-peak (relayed as 9–12 and 14–18 Beijing time, off-peak flat). Mid-July date corroborated by @AndrewCurran_. V4-Flash already in wide use, so 'V4' = full GA. Status confirmed (consistent multi-account email relay + Curran corroboration); verification partial (peak windows diverge across reposters, no official pricing page yet). Distinct from the May permanent 75% V4-Pro price cut ([[deepseek-v4-pro-price-cut-2026-05]]) and the V4 Vision turn-on ([[deepseek-v4-vision-2026-06]])."
---

Reported **2026-06-29/30** across 10+ independent accounts relaying a
**DeepSeek email to API users**: **V4-Pro and V4-Flash** (~1M context)
leave preview for **mid-July GA**, paired with the first major LLM
**time-of-day demand pricing** — **peak hours cost roughly 2× off-peak**
(relayed as 9:00–12:00 and 14:00–18:00 Beijing time, ~seven peak hours/day,
with off-peak rates unchanged). The mid-July date is corroborated by Andrew
Curran ("the Whale arrives in about two weeks").

**Why a separate ticket.** This is a distinct **V4 GA + novel pricing
mechanism** event, separate from the May **permanent 75% V4-Pro price cut**
([[deepseek-v4-pro-price-cut-2026-05]]) and the June **V4 Vision** turn-on
([[deepseek-v4-vision-2026-06]]). Surge pricing is a new pricing *structure*,
not another discount, and the mid-July GA is a dated release milestone.

**Confirmed vs. reported.** The core facts — mid-July GA, Pro+Flash,
peak/off-peak doubling — are **consistent across the whole cluster** and
backed by an emailed announcement plus Curran's corroboration → `confirmed`.
But **peak-window details diverge** (Beijing time vs UTC across reposters)
and **no official DeepSeek pricing page** was surfaced → `verification:
partial`. V4-Flash is already in wide use, so "V4" here means the full GA,
not a first appearance.

**Context.** Surge pricing reframes open-weight economics: the cheap default
many lean on for routine coding gets a load-shedding incentive, nudging
batch/off-peak workloads and self-hosting. It lands amid the open-weight
surge — LongCat-2.0 ([[meituan-longcat-2-2026-06]]), GLM-5.2
([[zhipu-glm-5-2]]) — collapsing the cost floor while Western frontier weights
sit export-gated ([[anthropic-fable-mythos-export-control-2026-06]]).

**Transition triggers:**
- Official DeepSeek pricing page / API changelog with exact windows + per-token
  rates → UPDATE, advance `verification` to `confirmed`.
- Actual mid-July GA going live → `status: released`.
- Competitors adopting time-of-day pricing → UPDATE (context).
- ≥4 weeks past GA settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further DeepSeek V4 GA / surge-pricing signal UPDATES this
ticket. The May 75% price cut and the Vision turn-on stay on their own tickets.
