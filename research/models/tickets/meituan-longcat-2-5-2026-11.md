---
slug: meituan-longcat-2-5-2026-11
title: "Meituan LongCat-2.5 — 1.6T-parameter natively multimodal agentic model"
company: Meituan
model: LongCat-2.5
status: confirmed
status_note: |
  **Secondary report, 2026-11-03 13:17 UTC.** @AINativeF: "Meituan LongCat unveils LongCat-2.5,
  a 1.6T-parameter multimodal agentic model", with about 48B active parameters, built for
  long-horizon agentic tasks, with stronger visual understanding and agentic coding (complex coding
  projects, creative design, 3D work). The post says the announcement came from Meituan LongCat's
  official account. That official post is not in this run's signal.

  The 1.6T / ~48B-active shape matches LongCat-2.0, so this looks like a natively multimodal
  successor on the same MoE backbone. One user (@fableforge) mentions using "LongCat 2.0 and 2.5",
  which suggests some access exists, but no weights, API or licence details were captured.
expected: "Announced 2026-11-03 (per relay). Open: Meituan's own post, open weights or API availability, licence, and independent benchmarks."
labels:
  - frontier-model
  - multimodal
  - agentic
  - moe
  - china
verification: partial
sources:
  - "https://x.com/AINativeF/status/2117607019175920023"
  - "https://x.com/fableforge/status/2117624333656830210"
  - "@Meituan_LongCat"
created_at: 2026-11-03
updated_at: 2026-11-03
closed_at: null
closed_reason: null
history:
  - ts: 2026-11-03
    change: "Created — CONFIRMED / partial. @AINativeF (2026-11-03 13:17 UTC) reports that Meituan's LongCat team unveiled LongCat-2.5: a natively multimodal agentic model with 1.6T total and about 48B active parameters, aimed at long-horizon agentic tasks, visual understanding and agentic coding, announced via Meituan LongCat's official account. The official post itself was not in this run's signal, so verification is partial. Availability (weights, API) and licence are not yet captured. Successor to the closed [[meituan-longcat-2-2026-06]]."
---

LongCat-2.5 is the successor to LongCat-2.0, tracked at [[meituan-longcat-2-2026-06]] and closed
as released-and-aged. LongCat-2.0 was a 1.6T open-weight MoE trained on an all-domestic cluster. It
was also revealed as the anonymous "Owl Alpha" that led OpenRouter coding usage.

The same parameter shape suggests 2.5 is a multimodal and agentic upgrade on the same backbone, not a
new pretraining scale. The open questions are whether Meituan again releases open weights and whether
the agentic-coding claims hold up on independent benchmarks.

**Transition triggers:** Meituan's own post, or weights or an API that anyone can use → `released`;
independent benchmark results → history update.
