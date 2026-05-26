---
slug: anthropic-spacex-colossus-2026-05
title: Anthropic–SpaceX ~$40B Colossus 1 compute lease disclosed in S-1
company: Anthropic
model: null
status: confirmed
status_note: |
  The Information reporting (2026-05-25, 14:00 / 16:00 UTC) on SpaceX's
  IPO filing disclosed that Anthropic has agreed to pay SpaceX about
  $1.25B/month to lease the Colossus 1 AI data center through May 2029
  — roughly $15B/year and ~$40B cumulative. Either side can terminate
  on 90 days' notice, so the $40B is a run-rate, not a locked
  take-or-pay backlog. SpaceX itself reported $4.7B Q1 revenue against a
  $4.3B loss, with AI capex reshaping the financial story pre-IPO.
  Anthropic's compute now spans SpaceX/Colossus + Google TPU
  (multi-gigawatt deal starting 2027, $40B Google investment) + AWS
  Trainium / NVIDIA + the May 21 Microsoft Maia 200 talks.
expected: "Lease runs through May 2029; $SPCX Nasdaq target ~June 12"
labels:
  - infrastructure
  - compute
  - partnership
  - ipo-adjacent
verification: confirmed
sources:
  - https://www.theinformation.com/articles/spacex-ipo-filing-anthropic-colossus
  - "@theinformation"
  - "@crepesupreme"
  - "@ainews_24_7"
  - "@iisanidhya"
created_at: 2026-05-26
updated_at: 2026-05-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-26
    change: "Created — The Information reporting on SpaceX's IPO filing (2026-05-25 14:00 / 16:00 UTC) disclosed Anthropic's $1.25B/month Colossus 1 lease through May 2029 (~$15B/year, ~$40B cumulative) with a 90-day mutual-termination right; SpaceX Q1 $4.7B revenue / $4.3B loss; AI capex reshaping the pre-IPO story. Anthropic compute web now spans SpaceX/Colossus + Google TPU + AWS Trainium / NVIDIA + Microsoft Maia 200 talks"
---

**The Information's reporting on 2026-05-25** put concrete numbers on
the Anthropic–SpaceX compute relationship that prior cycles had only
gestured at (xAI / SpaceX as "Anthropic's compute landlord," May 6):
the SpaceX IPO filing discloses **Anthropic has agreed to pay SpaceX
about $1.25 billion a month to lease the Colossus 1 AI data center
through May 2029** — roughly **$15 billion per year and ~$40 billion
cumulative**.

The terms include a **90-day mutual-termination right**, which is the
material caveat: the ~$40B is a *run-rate*, not a take-or-pay backlog.
Public-market investors inherit duration risk that a single headline
figure papers over.

SpaceX itself reported **$4.7B Q1 revenue against a $4.3B loss** in the
same filing — i.e. its pre-IPO revenue line is materially propped up by
leasing AI compute to a rival lab. The week's compute-web parse
(@iisanidhya, 2026-05-25 16:00 UTC) sets the deal alongside Anthropic's
other infrastructure surfaces: a multi-gigawatt Google/Broadcom TPU
agreement starting 2027 (with Google's reported $40B investment),
existing AWS Trainium / NVIDIA capacity, and the still-talks-only
[Microsoft Maia 200 reporting](https://x.com/MachineBrief/status/2059115614783103174)
from May 21 CNBC.

**What is unverified:** the sharper "Colossus 1 running at ~11% MFU /
Anthropic pays for what xAI couldn't use" framing (@crepesupreme) cites
an unverified internal xAI memo and is not in The Information's posts;
the "18,712 BTC in the S-1" / "$20B related-party transaction" lines
trace only to crypto-account chatter (@GWIZARD9K, @WhaleMasterPro). The
$SPCX Nasdaq target of ~June 12 is reported but not confirmed by SpaceX.
Neither SpaceX nor Anthropic has issued a primary statement on the
Colossus lease terms.

**Transition triggers:**
- SpaceX's S-1 becomes formally public on SEC EDGAR → UPDATE.
- Anthropic or SpaceX primary statement on the lease terms or
  termination clause → UPDATE.
- 90-day termination right exercised by either side → UPDATE; close
  with `closed_reason` per the outcome.
- ~$40B run-rate holds through the IPO and into normal coverage; ≥4
  weeks past the $SPCX listing → `closed: released-and-aged`.

**Dedup note:** new signal about the Colossus 1 lease (utilization,
expansion, price renegotiation, termination) UPDATES this ticket.
Anthropic's Google TPU multi-gigawatt deal or the Microsoft Maia 200
talks each get their own ticket if/when they harden into disclosed
terms.
