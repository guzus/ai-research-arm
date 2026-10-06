---
slug: reflection-ai
title: Reflection AI
type: entity
aliases: ["Reflection AI", "Reflection", "Beam", "Reflection Beam", "Misha Laskin"]
tags: [open-weights, moe, us-lab, nvidia-backed, model-release]
description: US open-weights lab that unveiled Beam, a 501B/23B-active sparse MoE pretrained on 23.8T tokens, with Apache 2.0 weights promised later this month.
created_at: 2026-10-06
timestamp: 2026-10-06T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-06", path: research/digest/2026-10-06-digest.md}
  - {title: "ARA model ticket — Reflection open-weight model", path: research/models/tickets/reflection-open-weight-model-2026-10.md}
  - {title: "ARA daily digest 2026-10-05", path: research/digest/2026-10-05-digest.md}
---

**Reflection AI** is a US open-weights
lab that, until this cycle, was
defined by compute commitments rather
than a shipped model — a **$1B
[[nebius]] book** through 2029 and a
reported **$150M-a-month** bill on
[[xai|xAI]]'s Colossus since July.
On **2026-10-05** it named the
artifact: **Beam**, a **501B**
sparse mixture-of-experts with
**23B active** parameters,
pretrained on **23.8T tokens** on
[[nvidia|NVIDIA]] GB300s. Apache 2.0
weights are promised "later this
month." That is a preview, not a
weight drop (Reflection, TechCrunch,
MarkTechPost, Latent Space, Hacker
News; ARA daily digest 2026-10-06
and ticket
`reflection-open-weight-model-2026-10`).

## Why it matters

- **The first named Western open
  model aimed at Chinese peers.**
  CEO Misha Laskin had already told
  a journalist the prior week that
  an open-weight launch was coming
  on national-security grounds, and
  Axios framed the system as below
  the most advanced US closed models
  but competitive with leading
  Chinese open weights. Beam is that
  claim with a name and a size.
  Company-reported scores are
  **80.9** on SWE-Bench Verified,
  **80.1** on Terminal Bench v2.1,
  **97.8** on AIME 2026 and
  **90.5** on GPQA Diamond, with
  [[zhipu-glm-5-2|GLM-5.2]]-class
  reasoning at an estimated 3–4×
  less inference compute. Beam
  trails
  [[deepseek-v4-1-flash|DeepSeek
  V4.1 Flash]] (**90.6**) and
  [[moonshot-kimi-k3|Kimi K3]]
  (**88.3**) on Terminal Bench, so
  "strongest Western open model" is
  the defensible framing, not a
  frontier close. HN's top comment
  was "Publish your weights and HF
  repo or shut up" (Reflection,
  @rohanpaul_ai, Hacker News,
  @Cat_Zakrzewski; ARA daily digest
  2026-10-06).
- **The compute book is already
  large relative to a lab that
  still has no public weights.**
  Axios's $150M-a-month Colossus
  print sits on top of the $1B
  Nebius deal this wiki already
  tracks on those pages. The ticket
  also notes an unverified reported
  Nebius increment. See [[ai-capex]]
  and [[open-weights]] (Axios via
  @AndrewCurran_; ARA daily digest
  2026-10-05).
- **It is a preview with a dated
  promise.** Until Apache 2.0
  weights land, Beam is a vendor
  card plus a first-party blog, the
  same shape this theme has already
  seen from labs that later
  withheld serving-side pieces.

## Open questions

- **Do the Apache 2.0 weights
  actually ship this month**, and
  on Hugging Face, or does the
  preview linger?
- **Do independent evals hold the
  company-reported SWE-Bench /
  Terminal Bench / GPQA numbers?**
  The efficiency claim uses
  *estimated* forward-pass FLOPs.
- **How much of the Colossus and
  Nebius book is reserved for
  Beam training versus later
  serving?**
