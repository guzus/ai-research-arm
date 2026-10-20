---
slug: neocloud
title: Neocloud
type: concept
aliases: [neocloud, "neo-cloud", "GPU-as-a-service", GPUaaS]
tags: [ai-infrastructure, gpu-cloud, business-model, take-or-pay]
description: Buy GPUs on debt, rent capacity back under take-or-pay contracts; Microsoft's Nscale Essex exit and CoreWeave's +1,000 bps spreads mark a mid-cycle shakeout.
created_at: 2026-05-24
timestamp: 2026-10-20T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-20", path: research/digest/2026-10-20-digest.md}
  - {title: "ARA daily digest 2026-09-18", path: research/digest/2026-09-18-digest.md}
  - {title: "ARA generative research — CoreWeave GPU-as-a-service unit economics", path: research/generative/2026-05-16T103712--coreweave-gpu-as-a-service-unit-economics-and-customer-conce.html}
  - {title: "ARA daily digest 2026-05-20", path: research/digest/2026-05-20-digest.md}
---

A **neocloud** is a specialized cloud provider whose business is renting GPU
compute for AI training and inference, as opposed to the general-purpose
hyperscalers (AWS, Azure, GCP). The defining mechanics: acquire NVIDIA (or, in
the hyperscaler-JV variant, TPU) capacity financed largely by debt, sign
multi-year **take-or-pay** contracts with a small set of anchor tenants, and
underwrite the debt against that forward contract book. [[coreweave]] and
[[nebius]] are the canonical public examples;
[[crusoe]] is now a private peer after a $3.9B
Series F at $30.9B (2026-09-18).

## Why it matters
The neocloud model is the load-bearing structure of the current [[ai-capex]]
supercycle — it is how GPU demand gets converted into financeable, multi-year
revenue. ARA's CoreWeave audit makes the mechanics concrete: ~98% of FY2025
revenue under take-or-pay contracts let CoreWeave bootstrap a ~$99B backlog into
the first **investment-grade-rated GPU-backed loan** (the $8.5B DDTL 4.0, A3 at
the SPV level) — capital structure unavailable to a business without committed
forward contracts (ARA generative research, 2026-05-16).

The model is now attractive enough that hyperscalers are entering it directly:
the **Google × Blackstone $5B TPU-as-a-service JV** (BXN1, 500 MW by 2027) is a
neocloud play explicitly aimed at [[coreweave]] and [[nebius]] (ARA digest
2026-05-20). OpenAI's "Guaranteed Capacity" multi-year compute futures are the
demand-side mirror of the same take-or-pay logic.

## Open questions
- **Concentration is structural.** Because the debt is underwritten against a few
  anchor tenants, neoclouds inherit their customers' counterparty risk. Is this a
  feature (financeability) or a fragility (correlated default)?
- **Commoditization.** As hyperscaler-backed JVs flood in, does independent
  neocloud capacity get commoditized, compressing the spread between GPU cost and
  rental price?
- **Power, not just chips.** Increasingly the binding constraint is megawatts, not
  GPUs. Who controls owned power versus leases it?

## Crusoe prices in; Nebius hikes the card (2026-09-18)

[[crusoe]] closed a **$3.9B Series F at $30.9B**,
citing **$140B+ in contracted value** — the
largest private neocloud mark of the window,
still without a public RPO split. The same day
[[nebius]] told customers on-demand GPU rent
rises **17–21% on October 1**. See [[ai-capex]]
(Reuters, TechCrunch, Twitter; ARA daily digest
2026-09-18).

## Essex grid delay; a 7–10 survivor set (2026-10-20)

[[microsoft]] ended its deal for Nscale's
Essex/Loughton site — The Decoder puts it at
**23,000 [[nvidia|Nvidia]] chips**, with grid
power possibly delayed into the **2030s** —
about a month after Nscale's US IPO filing.
[[coreweave]] bonds trade around **+1,000 bps**
over Treasuries, and executives expect only
**7–10 of hundreds** of AI cloud providers to
survive. Gartner warns more than **$3.5T** of
AI infrastructure could need write-downs by
**2030**. Nscale is still reportedly talking a
second **$45B** book with [[anthropic]]. Power
and offtake, not GPU scarcity, are the
shakeout variables. See [[ai-capex]] (Reuters,
The Decoder, The Verge, TechCrunch; ARA daily
digest 2026-10-20).
