---
slug: step-5-preview
title: Step 5 Preview
type: entity
aliases: ["Step 5 Preview", "Step-5-Preview", "Step 5", "StepFun Step 5"]
tags: [china, moe, frontier-model, vision, open-weights]
description: StepFun's 600B / 27B-active MoE with 1M context; open weights landed in FP8 and BF16, with first-party AA-LCR 88.3% and Terminal-Bench 4.0 33.3%.
created_at: 2026-09-21
timestamp: 2026-10-18T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-18", path: research/digest/2026-10-18-digest.md}
  - {title: "ARA model ticket — StepFun Step-5-Preview", path: research/models/tickets/stepfun-step-5-preview-2026-10.md}
  - {title: "ARA daily digest 2026-09-21", path: research/digest/2026-09-21-digest.md}
---

**Step 5 Preview** is StepFun's first-party 600B /
27B-active mixture-of-experts model with **1M
context** and vision, launched on the company page
as "Today, we're introducing Step 5 Preview." The
2026-09-20 wiki pass skipped an earlier scrape;
this page waits for the first-party launch. StepFun
was already named in CISA advisory AA26-251A on
[[federal-ai-policy]] — this is the model, not a
new lab page.

## Why it matters

- **First-party launch, not a leaderboard leak
  (2026-09-21).** The company page, a Studio picker
  shot, and a docs row beside Step 3.7 Flash now
  agree on the **600B / 27B** split, **1M
  context**, and vision. Live in Studio and the
  API at **$1.00 / $2.70 per Mtok**. Artificial
  Analysis still lists **Intelligence Index 44**.
  That is a priced preview, not a closed
  frontier claim (StepFun, Artificial Analysis;
  ARA daily digest 2026-09-21).
- **Vendor charts stay vendor charts.** StepFun
  posts DeepSWE v1.1 High **67.7** against
  [[moonshot-kimi-k3|Kimi K3 Max]] **67.5**,
  [[zhipu-glm-5-3|GLM-5.3 Max]] **66.9**, and
  [[gpt-6|GPT-6 Astra Max]] **74.1**. A Pokémon
  Red demo is stamped at **>3,000 turns / 6M
  tokens** and Lt. Surge by turn **3,082**. Hold
  both as first-party exhibits (StepFun; ARA
  daily digest 2026-09-21).
- **Open weights are dated, not landed.** Official
  weights are promised **15 October**. r/LocalLLaMA
  circulated an empty official
  `stepfun-ai/Step-5-Preview-BF16` repo and a
  `rene98c` fork claimed as an accidental dump;
  treat the dump as unverified. See
  [[open-weights]] (StepFun, Reddit; ARA daily
  digest 2026-09-21).

## Open weights land; Arena Alignment Index (2026-10-18)

- **The 15 October weights
  landed** as a 600B MoE with
  **27B active** and **1M
  context**, in FP8 and BF16.
  First-party scores now
  include **88.3% on AA-LCR**
  and **33.3% on Terminal-Bench
  4.0**. The Arena Alignment
  Index added the preview at
  **75.1%**, behind
  [[muse-wonder|Muse Wonder]]
  **77.5%** and Reflection Beam
  **75.3%**. MarkTechPost is
  the digest's named outlet;
  the model-ticket
  verification is still
  **partial** (no StepFun
  primary captured in that
  window). See
  [[open-weights]]
  (MarkTechPost, @arena; ARA
  daily digest 2026-10-18 and
  ticket
  `stepfun-step-5-preview-2026-10`).

## Open questions

- **Do independent agentic
  evals move Index 44?** The
  AA-LCR, Terminal-Bench 4.0
  and Arena Alignment rows are
  still vendor or arena
  figures, not a reproduced
  Artificial Analysis
  composite.
- **Does the licence match the
  open-weight claim?** The
  ticket still lacks a
  first-party licence line.
