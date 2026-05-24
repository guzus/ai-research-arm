---
slug: neocloud
title: Neocloud
type: concept
aliases: [neocloud, "neo-cloud", "GPU-as-a-service", GPUaaS]
tags: [ai-infrastructure, gpu-cloud, business-model, take-or-pay]
summary: Business model where a specialized provider buys GPUs on debt and rents the capacity back under multi-year take-or-pay contracts, distinct from general-purpose hyperscalers.
created_at: 2026-05-24
updated_at: 2026-05-24
sources:
  - {title: "ARA generative research — CoreWeave GPU-as-a-service unit economics", path: research/generative/2026-05-16T103712--coreweave-gpu-as-a-service-unit-economics-and-customer-conce.html}
  - {title: "ARA daily digest 2026-05-20", path: research/digest/2026-05-20-digest.md}
---

A **neocloud** is a specialized cloud provider whose business is renting GPU
compute for AI training and inference, as opposed to the general-purpose
hyperscalers (AWS, Azure, GCP). The defining mechanics: acquire NVIDIA (or, in
the hyperscaler-JV variant, TPU) capacity financed largely by debt, sign
multi-year **take-or-pay** contracts with a small set of anchor tenants, and
underwrite the debt against that forward contract book. [[coreweave]] and
[[nebius]] are the canonical public examples.

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
