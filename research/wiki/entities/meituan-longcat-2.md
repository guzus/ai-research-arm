---
slug: meituan-longcat-2
title: Meituan LongCat-2.0
type: entity
aliases: ["LongCat-2.0", "LongCat", "Owl Alpha", "Meituan LongCat"]
tags: [open-weights, china, coding, frontier-model, moe]
description: Meituan's 2026-06-30 open-weighted 1.6T-param MoE coding model, ~1M context, that Meituan says was pretrained on a ~50,000-chip all-domestic (no-Nvidia) cluster — and revealed as the anonymous "Owl Alpha" that had topped OpenRouter coding usage for ~two months.
created_at: 2026-07-01
timestamp: 2026-07-01T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-01", path: research/digest/2026-07-01-digest.md}
  - {title: "ARA model ticket — meituan-longcat-2-2026-06", path: research/models/tickets/meituan-longcat-2-2026-06.md}
  - {title: "VentureBeat — Meituan open-sources LongCat-2.0", url: "https://x.com/VentureBeat/status/2071831014872092715", date: 2026-06-30}
---

LongCat-2.0 is a **1.6-trillion-parameter MoE** (~48B active), **~1M-token
context** coding model that Chinese food-delivery giant **Meituan** released and
**open-weighted on 2026-06-30** (GitHub + Hugging Face). Meituan says it was
pretrained on **35T tokens** across a **~50,000-chip cluster that is entirely
domestic, with no NVIDIA silicon**. The reveal's twist: LongCat-2.0 is the model
that had run anonymously on OpenRouter as **"Owl Alpha"** for ~two months,
**topping developer coding usage** before Meituan claimed it (ARA digest
2026-07-01; model ticket `meituan-longcat-2-2026-06`).

## Why it matters
- **The moat-leak thesis at frontier scale.** Where prior cycles tracked
  open-weight closing via [[zhipu-glm-5-2|GLM-5.2]] and [[deepseek|DeepSeek V4]],
  LongCat-2.0 pushes it to a **1.6T open-weight model that was already winning
  real developer usage incognito** — concrete evidence for the [[open-weights]]
  "no moat" argument.
- **The no-Nvidia training claim is the strategic edge.** If verified, training
  a 1.6T frontier-class model on an all-domestic cluster is a direct answer to
  US export controls — the compute-sovereignty story made concrete, alongside
  DeepSeek's DSpark and GLM 5.2's price/speed pressure. See
  [[federal-ai-policy]]. On the inference side, [[etched]]'s transformer-only
  Sohu ASIC is the hardware counterpart to the same route-around-Nvidia
  pressure.
- **Confirmed vs. vendor-supplied.** The **release and OpenRouter standing are
  independently observable** → treat as shipped. The contested parts are vendor
  claims: one relay cites **SWE-bench Pro 59.5** ("beats GPT-5.5") and Meituan's
  card claims Gemini 3.1 Pro / GPT / Opus-tier parity, but there is **no
  third-party benchmark**, and the "trained entirely on Chinese chips" framing
  is Meituan's own — plausible but unverified.

## Open questions
- **Independent benchmarks.** First neutral SWE-bench Pro / LMArena runs on the
  open weights will settle the parity claims.
- **The silicon question.** Scrutiny confirming or refuting the all-domestic,
  no-Nvidia cluster composition is the load-bearing verification for the
  export-control-workaround narrative.
