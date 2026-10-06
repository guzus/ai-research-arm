---
slug: nebius
title: Nebius Group
type: entity
aliases: [Nebius, NBIS, "Nebius Group N.V.", Inferize]
tags: [neocloud, gpu-cloud, ai-infrastructure, nvidia-partner]
description: Amsterdam-based AI cloud ("neocloud") spun out of Yandex; Token Factory acquired Inferize to cut GPU cold-start times, after a $1B Reflection AI compute book and a $17B Microsoft-linked Vineland site.
created_at: 2026-05-24
timestamp: 2026-10-06T00:00:00Z
market:
  ticker: NBIS
  exchange: NASDAQ
  symbol: NASDAQ:NBIS
  provider: yahoo
sources:
  - {title: "ARA daily digest 2026-10-06", path: research/digest/2026-10-06-digest.md}
  - {title: "ARA daily digest 2026-10-05", path: research/digest/2026-10-05-digest.md}
  - {title: "ARA model ticket — Nebius acquires Inferize", path: research/models/tickets/nebius-inferize-acquisition-2026-10.md}
  - {title: "ARA daily digest 2026-09-27", path: research/digest/2026-09-27-digest.md}
  - {title: "ARA daily digest 2026-09-18", path: research/digest/2026-09-18-digest.md}
  - {title: "ARA daily digest 2026-08-13", path: research/digest/2026-08-13-digest.md}
  - {title: "ARA daily digest 2026-07-15", path: research/digest/2026-07-15-digest.md}
  - {title: "ARA daily digest 2026-05-20", path: research/digest/2026-05-20-digest.md}
  - {title: "ARA daily digest 2026-05-21 (Google × Blackstone neocloud JV targets CoreWeave/Nebius)", path: research/digest/2026-05-21-digest.md}
  - {title: "Nebius Group investor relations", url: "https://group.nebius.com/investors", date: 2026-05-20}
---

Nebius Group (NASDAQ: NBIS) is an Amsterdam-based AI cloud provider — a
"[[neocloud]]" — that rents out GPU capacity for AI training and inference.
It emerged from the restructuring of Yandex's international business and now
trades publicly as a pure-play [[ai-capex]] infrastructure name, competing for
the same NVIDIA allocations and anchor-tenant contracts as [[coreweave]] and
the new hyperscaler joint ventures.

## Why it matters
Nebius is one of the named comparables when the market sizes up the neocloud
land-grab. In the May 2026 cycle, Google and Blackstone unveiled a **$5B
TPU-as-a-service neocloud JV** (the "BXN1" unit, targeting 500 MW by 2027) that
press coverage framed as "directly targeting CoreWeave/Nebius" — i.e. Nebius is
treated as a category-defining incumbent in GPU-cloud capacity, not a fringe
player (ARA digest 2026-05-20). The neocloud thesis it embodies — buy GPUs on
debt, sign multi-year take-or-pay contracts, rent the capacity back — is the
same structure scrutinized in ARA's CoreWeave unit-economics audit, and the
same structure that ties Nebius's fortunes to the broader [[ai-capex]] supercycle
that NVIDIA's "demand has gone parabolic" Q1 FY27 print is meant to confirm
(ARA digest 2026-05-21).

## Open questions
- **Customer concentration.** The neocloud model lives or dies on a handful of
  anchor tenants. Like [[coreweave]], does Nebius's forward book rest on two or
  three counterparties, or is it genuinely broadening?
- **Capacity vs. demand timing.** With hyperscaler-backed JVs (Google ×
  Blackstone) entering the same market, does independent neocloud capacity get
  commoditized, or does the [[ai-capex]] demand curve stay ahead of supply?
- **Financing durability.** CoreWeave bootstrapped GPU-backed debt to an
  investment-grade SPV rating; can independent neoclouds like Nebius access
  comparably cheap capital, or does the cost of capital separate the winners?

## Recent developments

- **$1B+ Reflection AI compute deal; stock falls despite the win
  (2026-07-15).** Nebius signed a **$1B+ compute agreement** with
  **Reflection AI** for **Nvidia GB300** access through **2029** — a
  large multi-year anchor-tenant contract of the kind that defines the
  neocloud business model. Nebius stock still **fell ~5%** on the news,
  with separate commentary noting Reflection AI has **~60 employees, no
  revenue**, and already owes [[spacex]] ~$150M/month under existing
  commitments — a customer-concentration and counterparty-risk read that
  sharpens the "Customer concentration" open question above (ARA digest
  2026-07-15).

- **FY26Q2: the model's economics finally print (2026-08-13).** Nebius
  posted **$582.3M quarterly revenue (+454% YoY, +46% sequential)** with a
  **~50% AI Cloud adjusted EBITDA margin**, **$8.04B of cash**, and
  **contracted power raised from ~4GW to 5GW** — saying it **could sell all
  of its 2027 capacity today** while leaving **2026 guidance unchanged**.
  It disclosed an **asset-light model where partners finance and operate
  facilities**, and that **~70% of the quarter's deals carried customer
  prepayments** — prepayments being the counterparty-quality evidence the
  neocloud thesis needs against the reflection-deal skepticism above. The
  print was the day's cleanest neocloud economics data point (ARA digest
  2026-08-13).

- **On-demand GPU rent rises 17–21% on October 1
  (2026-09-18).** Customer notices — not an IR
  release — put H100 at **$3.85 → $4.50** and
  B300 at **$7.85 → $9.50**, the **second hike
  since May**. Reserved SKUs are unchecked. This
  is a price-card move on the same take-or-pay
  capacity the FY26Q2 print said it could sell
  out through 2027, and it lands the same day
  [[crusoe]] closed a $3.9B Series F at $30.9B.
  See [[neocloud]], [[coreweave]] and
  [[ai-capex]] (Twitter; ARA daily digest
  2026-09-18).

- **New Jersey fined DataOne $1.07 million
  (2026-09-27).** A record air-permit
  penalty on a [[microsoft|Microsoft]]-linked
  Vineland datacenter after a Floodlight
  drone found 45 of 62 unpermitted gas
  generators running at once. The site is
  slated to serve Microsoft under a **$17
  billion Nebius deal**. DataOne disputes
  the "temporary generator" finding and
  says it will apply for permits while
  moving to Bloom Energy fuel cells. This
  is a regulator action on a named
  neocloud-to-hyperscaler site, not a
  Nebius earnings print. See [[microsoft]],
  [[neocloud]] and [[ai-capex]] (The
  Guardian via @rohanpaul_ai; ARA daily
  digest 2026-09-27).

- **Token Factory acquired Inferize
  (2026-10-01 / ingested 2026-10-05).**
  @demian_ai announced the deal for
  Nebius Token Factory: Inferize is a
  17-person Israeli startup whose
  technology loads models in seconds
  and cuts cold-start / warm-up time
  on shared GPUs (model loads, demand
  spikes, RL weight reloads). The team
  folds into Token Factory after Eigen
  and Clarifai's core team. Nebius has
  not posted terms. The digest relays
  "up to $150M" with earnout wording
  from @Israel; the ticket records
  terms as undisclosed. Treat the
  dollar figure as unverified. The
  direction is clear: neoclouds
  competing on utilisation of
  open-weight inference, not raw GPU
  count. Same window, Axios says
  [[reflection-ai]] has paid **$150M a
  month since July** for compute on
  [[xai|xAI]]'s Colossus, **on top of**
  the $1B Nebius deal already on this
  page. The next day Reflection named
  the model **Beam** (501B / 23B
  active) and promised Apache 2.0
  weights later this month — still a
  preview. See [[xai]],
  [[neocloud]] and [[open-weights]]
  (@demian_ai, @Israel, Axios via
  @AndrewCurran_; ARA daily digest
  2026-10-05 and ticket
  `nebius-inferize-acquisition-2026-10`).
