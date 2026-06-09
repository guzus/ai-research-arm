---
slug: spacex-ipo-2026-06
title: SpaceX IPO — Nasdaq SPCX, prices June 11 / first trade June 12
company: SpaceX
model: null
status: confirmed
status_note: |
  **SpaceX's IPO** — reported as the largest in history — **prices after the
  close 2026-06-11** and **first trades 2026-06-12 on Nasdaq under ticker
  SPCX** at **$135/share**, a **~$75B raise** at a **~$1.75T valuation**
  (~30% reserved for retail; reported demand far exceeding the raise). The AI
  relevance: SpaceX funds the **xAI / Colossus compute-landlord business**
  that rents capacity to Anthropic and Google
  ([[anthropic-spacex-colossus-2026-05]], [[google-spacex-compute-2026-06]]).
  Some Wall Street coverage argues the stock is worth roughly half the ask.
expected: "Prices 2026-06-11 after close; first trade 2026-06-12 (Nasdaq: SPCX), $135/share, ~$75B raise, ~$1.75T valuation"
labels:
  - spacex
  - ipo
  - funding
  - compute
  - corporate-action
verification: partial
sources:
  - "@SpaceX"
  - "@business"
created_at: 2026-06-09
updated_at: 2026-06-09
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-09
    change: "Created — SpaceX IPO (reported largest in history) prices 2026-06-11 after close, first trade 2026-06-12 on Nasdaq SPCX at $135/share, ~$75B raise, ~$1.75T valuation, ~30% reserved for retail. AI relevance: funds the xAI/Colossus compute-landlord business renting to Anthropic and Google ([[anthropic-spacex-colossus-2026-05]], [[google-spacex-compute-2026-06]]). Widely reported with a set ticker/date → status confirmed; no primary filing captured in-window → verification partial. Part of the 2026 AI IPO supercycle alongside [[openai-ipo-2026-06]] and [[anthropic-ipo-2026-06]]"
---

**SpaceX's IPO** — reported as the largest in history — is the third leg of
the 2026 **AI IPO supercycle**, alongside OpenAI's confidential S-1
([[openai-ipo-2026-06]]) and Anthropic's ([[anthropic-ipo-2026-06]]). It
**prices after the close on 2026-06-11** and **first trades 2026-06-12 on
Nasdaq under ticker SPCX**, at **$135/share** for a **~$75B raise** at a
**~$1.75T valuation**, with ~30% of shares reserved for retail and reported
demand well above the raise.

**Why it's tracked here.** SpaceX is not an AI lab, but the listing is the
funding engine for the **xAI / Colossus compute-landlord business** — the
capacity that Anthropic ([[anthropic-spacex-colossus-2026-05]]) and Google
([[google-spacex-compute-2026-06]]) rent at $1B+/month combined. The IPO
proceeds underwrite that buildout, making it a load-bearing node in the AI
infrastructure-economics story.

**Why `confirmed` / `partial`.** The pricing date, ticker, share price, raise,
and valuation are widely and consistently reported, clearing `confirmed` for
the event. No **primary SEC filing or SpaceX investor-relations URL** was
captured in this cycle's signal, so `verification` stays `partial`. Note the
skeptic line: some Wall Street coverage argues the stock is worth roughly half
the ask.

**Transition triggers:**
- Pricing confirmed 2026-06-11 → UPDATE with the final price.
- First trade 2026-06-12 → UPDATE, note opening print (status stays confirmed).
- Postponed or repriced → UPDATE; do NOT close.
- ≥4 weeks past first trade, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further SpaceX IPO signal (pricing, first-day trading,
allocation) UPDATES this ticket. The compute-lease relationships stay on
[[anthropic-spacex-colossus-2026-05]] and [[google-spacex-compute-2026-06]].
