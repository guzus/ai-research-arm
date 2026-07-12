---
slug: tencent-hunyuan-hy3-2026-07
title: Tencent Hunyuan releases Hy3 — 295B open-weight MoE under Apache 2.0
company: Tencent
model: Hunyuan Hy3
status: released
status_note: |
  Tencent Hunyuan released **Hy3**, a **295B-parameter MoE** open-weight
  model under **Apache 2.0** with a commercial-use API. Reported as new
  open SOTA on the MCP-Atlas benchmark (beating GLM-5.2), and separately
  reported beating GPT-5.5 on a science benchmark with a much smaller
  compute setup. No official @TencentHunyuan tweet captured in this
  ingest window, but three independent accounts over a week agree on the
  specific parameter count, license, and benchmark claims.
expected: null
labels:
  - open-weight
  - china
  - tencent
  - released
verification: partial
sources:
  - "@NielsRogge"
  - "@rohanpaul_ai"
created_at: 2026-07-12
updated_at: 2026-07-12
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-12
    change: "Created — Tencent Hunyuan released Hy3, a 295B open-weight MoE under Apache 2.0 with a commercial API. @NielsRogge (2026-07-06): 'Impressive open release by @TencentHunyuan — new open SOTA on MCP-Atlas, even beating GLM-5.2'; a second account (2026-07-12) reports it beats GPT-5.5 on a science benchmark with a smaller compute setup; a Japanese aggregator (2026-07-12) restates the 295B/Apache-2.0/commercial-API specifics independently. Three independent secondary sources agree on specifics; no official Tencent primary captured → status released (weights are out), verification partial."
---

**Tencent Hunyuan** released **Hy3**, a **295-billion-parameter
Mixture-of-Experts** open-weight model licensed under **Apache 2.0**,
with a commercially-usable API. Independent reporting over the past week
places it as the new open-weights SOTA on the MCP-Atlas benchmark
(surpassing [[zhipu-glm-5-2]]) and separately claims it beats GPT-5.5 on
a science benchmark while using a much smaller compute setup.

**Why `partial`.** Three independent accounts (an ML researcher, a news
aggregator, and a Japanese-language outlet) agree on the specific
parameter count, license, and benchmark claims — consistent evidence
across independent sources — but no official Tencent Hunyuan primary
(blog, model card, or account) was captured in this ingest window.

**Transition triggers:**
- An official Tencent Hunyuan primary source → advance `verification` to
  `confirmed`.
- A successor Hunyuan model → new ticket; do not reopen this one.
- ≥4 weeks past release settled into normal coverage → `closed:
  released-and-aged`.

**Dedup note:** further Hy3 signal (benchmarks, API pricing, primary
confirmation) UPDATES this ticket. Other open-weight China-lab models
stay on their own tickets ([[zhipu-glm-5-2]], [[minimax-m3]],
[[alibaba-qwen-3-7-plus]]).
