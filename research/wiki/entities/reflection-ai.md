---
slug: reflection-ai
title: Reflection AI
type: entity
aliases: ["Reflection AI", "Reflection", "Beam", "Reflection Beam", "Misha Laskin"]
tags: [open-weights, moe, us-lab, nvidia-backed, model-release]
description: US open-weights lab behind Beam; Apache-2.0 weights for the 501B/23B-active coding-agent MoE shipped, more permissive than Meta's Muse license.
created_at: 2026-10-06
timestamp: 2026-10-17T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-17", path: research/digest/2026-10-17-digest.md}
  - {title: "ARA daily digest 2026-10-11", path: research/digest/2026-10-11-digest.md}
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
weights, promised "later this
month," landed in the 2026-10-17
window on [[hugging-face]] — the
second large US
open-weight drop in two days,
after [[muse-spark-open]]
(Reflection, Hugging Face, HF
blog, TechCrunch; ARA daily
digest 2026-10-17).

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
- **The dated Apache 2.0 promise
  has now been met.** The
  remaining gap is independent
  agentic-coding evals, not
  whether the weights exist. See
  [[open-weights]].

## Open questions

- **Do independent evals hold the
  company-reported SWE-Bench /
  Terminal Bench / GPQA numbers?**
  The efficiency claim uses
  *estimated* forward-pass FLOPs,
  and no independent agentic-
  coding eval has appeared yet.
- **Does the 1M-context claim
  hold?** It comes only from a
  secondary account in the
  2026-10-17 digest.
- **How much of the Colossus and
  Nebius book is reserved for
  Beam training versus later
  serving?**

## Nvidia opened talks — early, unverified (2026-10-11)

- **The Saturday FT exclusive
  says [[nvidia]] is discussing
  a full takeover, a larger
  equity check, more chips, or
  a [[groq|Groq]]-style
  acqui-hire.** Talks are
  early and can still collapse;
  the acqui-hire is the
  structure most likely to skip
  a long antitrust review.
  NVIDIA already put **$800
  million** into the 2024
  Laskin/Antonoglou lab.
  Reuters could not
  independently verify; both
  companies were silent after
  hours. **$25B is April's
  pre-money, not a bid.** See
  [[open-weights]] (Financial
  Times, CNA/Reuters, Hacker
  News; ARA daily digest
  2026-10-11).
- **Beam remains a 501B-total /
  23B-active MoE** with Apache
  2.0 weights promised later
  this month. Those weights
  would still matter if the
  talks stall. HN entered at
  42/21 and closed at
  **100/66**, split between
  "didn't they just invest"
  and   "they want open models
  so they are not stuck with
  two customers." This page's
  dated weight-drop question
  is unchanged (Financial
  Times, HN; ARA daily digest
  2026-10-11).

## Apache 2.0 weights land (2026-10-17)

- **Beam shipped as Apache-2.0
  open weights**: **501B total /
  23B active**, a coding-agent
  MoE with NVFP4/FP8 checkpoints,
  day-0 transformers support, and
  its own harness. The license is
  more permissive than [[meta]]'s
  Muse Model License or Black
  Forest Labs'. Nathan Lambert
  said US open-weight models
  "cut the gap by at least half"
  against Chinese models. See
  [[open-weights]] and
  [[hugging-face]] (@reflection_ai
  via Hugging Face, HF blog,
  @mervenoyann; ARA daily digest
  2026-10-17).
- **Caveats stay in place.** The
  1M-context claim is secondary
  only. No independent
  agentic-coding evals have
  appeared yet, so the
  company-reported SWE-Bench /
  Terminal Bench card from the
  2026-10-05 preview is still
  unverified. The Nvidia talks
  this page logged on 2026-10-11
  are unchanged.
