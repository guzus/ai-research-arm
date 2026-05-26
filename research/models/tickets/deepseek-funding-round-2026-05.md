---
slug: deepseek-funding-round-2026-05
title: DeepSeek seeking ~$7.35B funding round at ~$45–55B valuation
company: DeepSeek
model: null
status: confirmed
status_note: |
  The Information's exclusive (2026-05-25, 21:00 UTC) reported DeepSeek
  is seeking ~$7.35B in fresh funding as rising compute costs push the
  once research-focused lab toward commercialization — landing the same
  day Caixin (14:59 UTC) reported a permanent 75% V4-Pro API price cut.
  The figure sits inside a ~$7–13B cluster of raise reports since
  mid-May (FirstSquawk "~50B yuan / ~$6.9B" May 22; Bloomberg-relayed
  "$10.29B"; some outlets ~"70B yuan / $13.2B") at a ~$45–55B valuation.
  CATL / Tencent / state funds are reported to be circling. No DeepSeek
  primary statement; round not confirmed closed. The long-circulating
  ">$50B" figure was always the valuation, not the round size.
expected: "Close at $7–13B at $45–55B valuation; no announced close date"
labels:
  - funding
  - china
  - commercialization
verification: partial
sources:
  - https://www.theinformation.com/articles/deepseek-seeks-7-35-billion-funding-round
  - "@theinformation"
  - "@FirstSquawk"
  - "@caixin"
created_at: 2026-05-26
updated_at: 2026-05-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-26
    change: "Created — The Information exclusive (2026-05-25 21:00 UTC) pegs DeepSeek's raise at ~$7.35B, resolving the prior ~$7–13B cluster (FirstSquawk \"50B yuan / ~$6.9B\" May 22; Bloomberg \"$10.29B\"; \"70B yuan / $13.2B\") at a ~$45–55B valuation. Same-day Caixin reported a permanent 75% V4-Pro API price cut; reframes the long-running \">$50B\" shorthand as valuation, not round size. CATL/Tencent/state funds circling; no DeepSeek primary, round not confirmed closed"
---

**The Information's exclusive on 2026-05-25 (21:00 UTC)** pegged DeepSeek's
raise at **~$7.35 billion**, framing it as the lab's pivot from research
to commercialization under compute-cost pressure. The figure sits inside
a ~$7–13B cluster of mid-May reporting (FirstSquawk "50B yuan / ~$6.9B"
May 22; Bloomberg-relayed "$10.29B"; some outlets "70B yuan / $13.2B"),
all at a ~$45–55B *valuation*.

This ticket exists to resolve a recurring conflation in earlier feed
coverage: the long-circulating **">$50B round"** shorthand was always
the **valuation**, not the raise size. The Information's specific
number plus the surrounding cluster make that clear.

The raise lands the same day **Caixin reported a permanent 75% V4-Pro
API price cut** (14:59 UTC May 25) — see
[deepseek-v4-pro-price-cut-2026-05](./deepseek-v4-pro-price-cut-2026-05.md).
Read together, the two reports describe a single move: DeepSeek is
funding aggressive commercialization (cheaper API, hardware co-design
with Huawei Ascend, broader deployment) at a ~$45–55B mark. CATL,
Tencent, and Chinese state funds are reported to be circling; no
DeepSeek primary statement, and the round is not confirmed closed.

**Why verification is `partial`:** The Information's reporting is
named-byline original journalism but is not a DeepSeek-primary source;
the cluster of corroborating raise figures gives multi-secondary
confirmation but the exact close size and valuation remain in flux.
Upgrade to `confirmed` once DeepSeek or a lead investor issues a primary
statement.

**Transition triggers:**
- DeepSeek primary statement on the raise → UPDATE, advance verification
  to `confirmed`.
- Round closed at a disclosed final size/valuation → UPDATE with the
  number; ≥4 weeks of normal coverage → `closed: released-and-aged`.
- Round withdrawn, materially down-sized, or contradicted → close
  per `closed_reason`.
- If 15+ daily cycles pass with no fresh corroboration → close with
  `closed_reason: stale-rumor-unverified`.

**Dedup note:** new signal about the round size, valuation, or
participating investors UPDATES this ticket. The V4-Pro price cut lives
on its own ticket. A follow-on round (Series-X / pre-IPO) gets a new
ticket and links here.
