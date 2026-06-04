---
slug: deepseek-funding-round-2026-05
title: DeepSeek raising ~$7B first external round at up to ~$59B valuation (Tencent / CATL leading)
company: DeepSeek
model: null
status: confirmed
status_note: |
  Reuters/CNBC (2026-06-03) and then Bloomberg ("DeepSeek Close to Sealing
  $7 Billion Funding") + SCMP ("nears US$7b haul") (2026-06-04) now carry
  DeepSeek's maiden external round as near-closed: ~50B yuan (~$7B–$7.4B)
  at a valuation of up to $59B, with Tencent and CATL as the largest
  outside investors and NetEase also planning to join. Founder Liang
  Wenfeng's reported ~20B-yuan (~$2.8B) personal check is part of the
  structure. Still entirely anonymously sourced ("people who declined to
  be identified"); no DeepSeek/Tencent/CATL primary or filing, and the
  $59B is a ceiling ("up to"), not a struck price. The earlier mid-May
  ~$7–13B / $45–55B cluster now converges on $7B / up to $59B.
expected: "Close to sealing at ~$7B (50B yuan); valuation up to $59B (ceiling); Tencent + CATL lead, NetEase joining; no announced close date"
labels:
  - funding
  - china
  - commercialization
verification: partial
sources:
  - https://www.theinformation.com/articles/deepseek-seeks-7-35-billion-funding-round
  - "@theinformation"
  - "@business"
  - https://x.com/Scutty/status/2062026768782131279
  - https://x.com/DeJesusMorrobel/status/2062326054375571587
  - https://x.com/AndroOxinu/status/2062336652408688918
  - "@FirstSquawk"
  - "@caixin"
created_at: 2026-05-26
updated_at: 2026-06-04
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-26
    change: "Created — The Information exclusive (2026-05-25 21:00 UTC) pegs DeepSeek's raise at ~$7.35B, resolving the prior ~$7–13B cluster (FirstSquawk \"50B yuan / ~$6.9B\" May 22; Bloomberg \"$10.29B\"; \"70B yuan / $13.2B\") at a ~$45–55B valuation. Same-day Caixin reported a permanent 75% V4-Pro API price cut; reframes the long-running \">$50B\" shorthand as valuation, not round size. CATL/Tencent/state funds circling; no DeepSeek primary, round not confirmed closed"
  - ts: 2026-06-03
    change: "Reuters (via @Scutty 04:21 UTC) + CNBC + Jiemian News fix the round at ~$7B (50B yuan) at up to a $59B valuation, with Tencent and CATL as the largest external investors and NetEase also planning to invest — superseding the earlier garbled $10B/$50B relays. Round 'finalizing', not closed; $59B is a ceiling. Lands the same morning as Alphabet's ~$80B AI-infra raise, feeding the cross-company issuance-wave narrative"
  - ts: 2026-06-04
    change: "Bloomberg ('DeepSeek Close to Sealing $7 Billion Funding in Historic AI Deal') and SCMP ('nears US$7b haul, backing from Tencent, CATL') now carry the round as near-closed; structure adds founder Liang Wenfeng's ~20B-yuan (~$2.8B) personal check. Still anonymously sourced with no DeepSeek/Tencent/CATL primary or filing (@Signal8Ai: 'no S-1, no filing of any kind') — status stays confirmed-report, verification stays partial"
---

**The Information's exclusive on 2026-05-25 (21:00 UTC)** pegged DeepSeek's
raise at **~$7.35 billion**, framing it as the lab's pivot from research
to commercialization under compute-cost pressure. The figure sits inside
a ~$7–13B cluster of mid-May reporting (FirstSquawk "50B yuan / ~$6.9B"
May 22; Bloomberg-relayed "$10.29B"; some outlets "70B yuan / $13.2B"),
all at a ~$45–55B *valuation*.

**Update (2026-06-03 → 06-04):** the round has firmed considerably.
Reuters (relayed by markets journalist David Scutt) and CNBC on 2026-06-03
fixed it at **~$7B (50B yuan) at up to a $59B valuation**, with **Tencent
and CATL** as the largest external investors and **NetEase** also planning
to invest. By 2026-06-04, **Bloomberg** ("DeepSeek Close to Sealing $7
Billion Funding") and the **SCMP** ("nears US$7b haul") carried it as a
near-closed deal, adding founder **Liang Wenfeng's ~20B-yuan (~$2.8B)
personal check**. It remains anonymously sourced — no DeepSeek/Tencent/CATL
primary or filing — so the `$59B` is a ceiling and verification stays
`partial`.

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
