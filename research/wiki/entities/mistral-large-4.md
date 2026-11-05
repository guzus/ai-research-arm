---
slug: mistral-large-4
title: Mistral Large 4
type: entity
aliases: ["Mistral Large 4", "Le Chonk"]
tags: [model-release, mistral, open-weights, moe, multimodal, europe, cybersecurity]
description: Mistral's 1T-parameter / 49B-active multimodal MoE; open weights shipped 2026-10-29 and a technical report landed 2026-11-03, pitched at cybersecurity work closed US models refuse.
created_at: 2026-10-07
timestamp: 2026-11-05T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-11-04", path: research/digest/2026-11-04-digest.md}
  - {title: "ARA model ticket — Mistral Large 4", path: research/models/tickets/mistral-large-4-2026-10.md}
  - {title: "ARA daily digest 2026-10-07", path: research/digest/2026-10-07-digest.md}
---

**Mistral Large 4** ("Le Chonk") is
[[mistral]]'s first trillion-parameter
model: a natively multimodal
mixture-of-experts with **1T total /
49B active** parameters on the first-
party blog, or **1.05T / 52B** plus a
**1.6B vision encoder** and a
**1M-token** context in the docs and
MarkTechPost. It is on Mistral's API
now. Co-founder Guillaume Lample says
the RL run is still in flight and a
final checkpoint plus open weights
will ship before month-end (secondary
reports name **27 October**). There
is no tech report or license yet
(Mistral, TechCrunch, The Decoder,
MarkTechPost, Simon Willison, Hacker
News; ARA daily digest 2026-10-07 and
ticket `mistral-large-4-2026-10`).

## Why it matters

- **It is the European answer to the
  Chinese open-weight trillion-scale
  MoE.** Mistral calls it the best
  open-weights model from the US or
  Europe — a claim that leaves out
  Chinese labs. Artificial Analysis
  places it **6th** among open-weight
  models. The Decoder says it still
  trails Claude, [[gpt-6|GPT-6]] and
  the top Chinese systems. Launch
  prices are **$1.36 / $4.18** per
  million tokens. Training used about
  **3,800–4,000** Grace Blackwell
  GPUs in Mistral's own European
  datacenters. See [[open-weights]]
  and [[nvidia]] (Mistral, Artificial
  Analysis, The Decoder, TechCrunch;
  ARA daily digest 2026-10-07).
- **The lead pitch is cybersecurity
  work that closed US models refuse.**
  Mistral reports **61.7** on DeepSWE
  v1.1 and **82%** on CyberGym-E2E, a
  test where [[claude-opus-5-5|Opus
  5.5]] and [[gpt-6|GPT-6 Astra]]
  score near zero because they refuse
  the task. The ticket's secondary
  card adds 93% Cybench, FinWorkBench
  67%, and Harvey legal-agent 15%
  versus [[moonshot-kimi-k3|Kimi K3]]
  13% / Astra 5%. All of those
  numbers are company-reported.
  [[anthropic]]'s same-day Cyber
  Verification Program is the closed-
  model counterpart: gated access
  rather than "we will do the
  security work." See
  [[agentic-ai-security]] and
  [[claude-fable-5]] (Mistral,
  @GuillaumeLample; ARA daily digest
  2026-10-07).
- **It dominated Hacker News
  (1,543 / 944).** Commenters were
  impressed by the benchmarks
  "probably without distillation."
  Plotly reported its data-analytics
  benchmark rising from **58% to
  74%** at a tenth of Medium 3.5's
  cost, while noting it is "not on
  the Pareto curve yet." Others found
  it fast but verbose, and said it
  forgets instructions over long
  sessions (Hacker News, Plotly;
  ARA daily digest 2026-10-07).

## Weights, then the technical report (2026-11-04)

- **Open weights of a "new and
  improved Le Chonk" shipped
  2026-10-29** on Hugging Face,
  inside the end-of-October
  promise. Mistral self-reports
  #1 among open models on
  Cognition's FrontierCode and
  SOTA cyber defence tested
  with CrowdStrike, Cloudflare,
  Rubrik and Zscaler. Secondary
  only: 1M context, commercial
  use permitted, API price
  halved to **$0.70 / $2.10**
  per million tokens. See
  [[open-weights]] and
  [[hugging-face]] (ticket
  `mistral-large-4-2026-10`).
- **The technical report
  ("the story of how Le Chonk
  was built") landed on
  alphaXiv on 2026-11-03.**
  Pierre Stock called the final
  model "way more efficient and
  compact than its Preview
  version three weeks ago."
  Mistral also demoed **Orbital
  Trace**, a real-time 3D
  tracker of about 19,000
  satellites and debris. A
  secondary roundup cites a
  modified MIT-style licence
  with hosting-as-a-service
  restrictions; that licence
  detail is not first-party in
  the digest (@MistralAI, ARA
  daily digest 2026-11-04).

## Open questions

- **What is the exact licence
  name?** The inspectable
  artifact is out; the
  hosting-restriction claim is
  still secondary.
- **Do independent evals hold the
  CyberGym / DeepSWE / Cybench
  numbers** on the final
  checkpoint?
- **Does "best open-weights from
  the US or Europe" remain the
  useful comparison**, or does
  leaving Chinese labs out of the
  frame become the story?
