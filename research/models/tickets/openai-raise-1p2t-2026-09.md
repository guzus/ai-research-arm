---
slug: openai-raise-1p2t-2026-09
title: OpenAI in early discussions for a new raise at a $1.2 trillion valuation
company: OpenAI
model: null
status: rumored
status_note: |
  **One reported line, from a credible relay, 2026-09-16 02:50 UTC.**
  @AndrewCurran_: "OpenAI is in early discussions for a new raise at a
  valuation of $1.2 trillion," with a linked source that was not resolvable
  in-window. No amount, no investors, no structure, no timing.

  **"Early discussions" is the operative phrase** and it is why this is
  `rumored` rather than `confirmed`. A valuation floated in early talks is a
  negotiating anchor, not a price; nothing is committed and no counterparty is
  named.

  **Adjacent corroboration on the financing environment, not on this round.**
  Broadcom CEO Hock Tan, on television the same window, described two of his
  six frontier-model customers — naming **OpenAI and Anthropic** — as "cash
  flow poor, but they are valuation rich," and said Broadcom is "creating a
  platform by bringing in strong financial partners… not your traditional
  finance partners," naming **Apollo and Blackstone**, "because the rates are
  better than going treasury." Asked whether those lenders would still fund
  OpenAI if it keeps pushing its IPO out, Tan: "Absolutely, they are."
  (@Schulz_Research relay.) That is a named CEO on the record describing
  private-credit appetite for OpenAI, which supports the *plausibility* of a
  large private raise. It says nothing about $1.2T.

  **The IPO interaction is the thing to watch.** A private round at $1.2T is
  an alternative to, and a delay of, the public listing tracked at
  [[openai-ipo-2026-06]] — and Tan's answer implies the private-credit route
  works precisely because the IPO keeps slipping.
expected: "TBD — early-stage talks only. Watch for: an amount, a named lead, a close, or a contradicting report; and whether this substitutes for the listing on [[openai-ipo-2026-06]]."
labels:
  - openai
  - funding
  - valuation
  - rumored
verification: partial
sources:
  - https://x.com/AndrewCurran_/status/2100054614888583229
  - "@Schulz_Research"
created_at: 2026-09-16
updated_at: 2026-09-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-16
    change: "Created — RUMORED. @AndrewCurran_ reported (2026-09-16 02:50 UTC) that 'OpenAI is in early discussions for a new raise at a valuation of $1.2 trillion', with a linked source not resolvable in-window; no amount, investors, structure or timing given. Status rumored because 'early discussions' describes an anchor, not a price, and nothing is committed; verification partial rather than unverified because a well-followed AI journalist relaying sourced reporting is a secondary corroboration, and because the financing environment was independently described on the record in the same window: Broadcom CEO Hock Tan named OpenAI and Anthropic as 'cash flow poor, but valuation rich' frontier-model customers, said Broadcom is bringing in Apollo and Blackstone as financial partners 'because the rates are better than going treasury', and answered 'Absolutely, they are' when asked whether those lenders would keep funding OpenAI if the IPO keeps slipping (@Schulz_Research relay). That corroborates private-credit appetite for OpenAI, NOT the $1.2T number. Opened as its own ticket because a private round is a distinct financing event from the listing tracked on [[openai-ipo-2026-06]] and may substitute for it; related compute-financing tickets are [[nvidia-openai-ohio-datacenter-financing-2026-07]] and [[openai-us-govt-stake-2026-06]]."
---

OpenAI is reported to be in **early discussions** for a new private raise at a
**$1.2 trillion** valuation. That is one line of reporting and it is the whole
confirmed content.

**Why it is `rumored` and stays there.** "Early discussions" plus a valuation
with no amount, no lead and no structure is the textbook shape of a leaked
anchor. Rounds at this scale routinely price differently from the first number
that reaches the press, and some never happen. This ticket exists to hold the
number so the eventual close can be compared against it, not to treat it as a
fact.

**The useful corroboration is about mechanism, not price.** Hock Tan — the CEO
of OpenAI's custom-silicon partner, speaking on television — said out loud
that his frontier-model customers are cash-flow poor and valuation rich, that
Broadcom is assembling non-traditional financial partners (Apollo, Blackstone)
at better-than-treasury rates, and that those lenders will keep funding OpenAI
even if the IPO slips. That is a named executive describing why a very large
private raise is fundable right now. It is evidence for the category and none
at all for the $1.2T figure, and the two should not be merged.

**Read it against the IPO ticket.** [[openai-ipo-2026-06]] tracks the public
listing. Every large private round is a reason to delay one, and Tan's
"absolutely, they are" is an insider saying the delay is financeable. If this
round closes, the listing timeline on that ticket should be re-read, not left
alone.

**Transition triggers:**
- An amount, a named lead investor, or a close → advance to `confirmed`,
  UPDATE both tickets.
- A second independent outlet on the $1.2T figure → advance `verification`.
- A contradicting report, or an IPO filing instead → UPDATE; if the listing
  supersedes it, close `superseded-by:openai-ipo-2026-06`.
- ≥15 cycles with no corroboration → `closed: stale-rumor-unverified`.

**Dedup note:** the public listing stays on [[openai-ipo-2026-06]]; the US
government stake stays on [[openai-us-govt-stake-2026-06]]; datacenter-level
financing stays on [[nvidia-openai-ohio-datacenter-financing-2026-07]].
