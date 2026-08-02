---
slug: deepseek-v4-ga-surge-pricing-2026-06
title: DeepSeek dates V4 GA for mid-July with first-of-its-kind API surge pricing
company: DeepSeek
model: DeepSeek V4 (Pro + Flash)
status: released
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

  **2026-07-31 — GA landed: official API now LIVE in public beta.**
  @deepseek_ai's own account: "DeepSeek-V4-Flash Official API is now LIVE in
  public beta! We've massively upgraded its Agent capabilities... The
  official V4-Flash now natively supports the Responses API format and is
  fully adapted for Codex." Independently corroborated by @kimmonismus and
  @AndrewCurran_. Reported specs: MoE, 284B total / ~13B active (6-of-256
  experts). **Pricing figures conflict across secondary relays** —
  ~$0.14/$0.28 per Mtok per one account vs ~$0.28/$0.87 per Mtok per
  another — so the exact rate card stays unresolved pending an official
  pricing page; open weights are reported "coming shortly" by secondary
  accounts, not yet DeepSeek-primary. A separate, thinly-sourced claim of a
  fresh 2x peak-hour surge-pricing change layered on top of this GA is
  unconfirmed (single low-signal account) and not carried forward as fact.
  Official primary launch clears `released` (real, live, publicly usable
  artifact) and `confirmed` verification for the GA itself; the peak-window
  and exact-pricing gaps from the original filing persist for the rate-card
  specifics. Status advances confirmed → released; verification advances
  partial → confirmed.
expected: "GA live 2026-07-31 in public beta (official API, agent-capability upgrade, native Responses API + Codex support). Pending: an official DeepSeek pricing page resolving the conflicting $0.14/$0.28 vs $0.28/$0.87 per-Mtok figures, and confirmation of open weights release"
labels:
  - frontier-model
  - pricing
  - china
  - deepseek
  - released
verification: partial
sources:
  - "@alephantai"
  - "@MikelEcheve"
  - "@AndrewCurran_"
  - "@teortaxesTex"
  - https://x.com/alephantai/status/2071621413711094240
  - https://x.com/AndrewCurran_/status/2071590515909480648
created_at: 2026-06-30
updated_at: 2026-07-31
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-30
    change: "Created — DeepSeek emailed API users (relayed 2026-06-29/30 by 10+ accounts) that V4-Pro and V4-Flash (~1M context) leave preview for mid-July GA, paired with first-of-its-kind LLM time-of-day surge pricing: peak hours ~2× off-peak (relayed as 9–12 and 14–18 Beijing time, off-peak flat). Mid-July date corroborated by @AndrewCurran_. V4-Flash already in wide use, so 'V4' = full GA. Status confirmed (consistent multi-account email relay + Curran corroboration); verification partial (peak windows diverge across reposters, no official pricing page yet). Distinct from the May permanent 75% V4-Pro price cut ([[deepseek-v4-pro-price-cut-2026-05]]) and the V4 Vision turn-on ([[deepseek-v4-vision-2026-06]])."
  - ts: 2026-07-31
    change: "GA landed — official V4-Flash API now LIVE in public beta (@deepseek_ai primary), massively upgraded agent capabilities, native Responses API support, full Codex adaptation. Corroborated by @kimmonismus and @AndrewCurran_. Reported MoE 284B total/~13B active. Pricing figures conflict across secondary relays (~$0.14/$0.28 vs ~$0.28/$0.87 per Mtok) — unresolved pending an official pricing page; open weights reported 'coming shortly' but not yet DeepSeek-primary. A separate single-account claim of renewed 2x peak surge pricing is unconfirmed, not carried forward. Status confirmed → released; verification partial → confirmed."
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
