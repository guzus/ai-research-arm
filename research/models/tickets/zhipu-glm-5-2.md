---
slug: zhipu-glm-5-2
title: Zhipu GLM 5.2 — open-weight frontier model
company: Zhipu AI
model: GLM 5.2
status: released
status_note: |
  **GLM 5.2** (Zhipu AI / Z.ai) is **out** — deployed in the **GLM Coding
  Plan** now, with **API access and MIT-licensed open weights "in a week."**
  Reported specs: **1M-token context**, **max/high "thinking" modes**. Early
  community benchmarks place it strongly among open models — a one-shot Pac-Man
  coding test ranked it **first above Qwen 3.6 27B**. Dominant open-weights
  story this cycle (HN front page ~468 pts; top of r/LocalLLaMA). Tracked
  alongside other open-weight contenders [[minimax-m3]], [[alibaba-qwen-3-7-plus]],
  [[gemma-4]].
expected: "API access + MIT open weights ~week of 2026-06-15 (per Zhipu)"
labels:
  - frontier-model
  - open-weights
  - china
  - coding
  - released
verification: partial
sources:
  - "@Zai_org"
  - https://news.ycombinator.com/item?id=48518684
created_at: 2026-06-14
updated_at: 2026-06-14
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-14
    change: "Created — Zhipu AI shipped GLM 5.2: deployed in the GLM Coding Plan now, with API + MIT open weights promised within a week. Reported 1M context, max/high thinking modes; early one-shot coding benchmarks rank it above Qwen 3.6 27B. Dominant open-weights story this cycle (HN ~468 pts, top of r/LocalLLaMA). Usable in the coding plan now → status released; widely corroborated across HN/r/LocalLLaMA but no captured primary Zhipu blog/model card and weights not yet public → verification partial. Sits with open-weight peers [[minimax-m3]], [[alibaba-qwen-3-7-plus]], [[gemma-4]]"
---

**GLM 5.2**, from **Zhipu AI (Z.ai)**, is the cycle's dominant open-weights
release. It is **already deployed in the GLM Coding Plan**, with **API
access and MIT-licensed open weights** promised **within a week**. Reported
specs include a **1M-token context window** and **max/high "thinking"
modes**.

**Capability signal.** Early community benchmarks are strong rather than
authoritative: a widely-shared one-shot Pac-Man coding test ranked GLM 5.2
**first, above Qwen 3.6 27B**. The release topped r/LocalLLaMA and reached
the Hacker News front page (~468 points), with the open-weights / local-
hosting community treating it as a timely counterpoint to the same week's
Anthropic export-control shutdown
([[anthropic-fable-mythos-export-control-2026-06]]).

**Why `released` / `partial`.** Because GLM 5.2 is usable now inside the
GLM Coding Plan, the lifecycle is `released`. `verification` stays
`partial`: the release is corroborated across HN and r/LocalLLaMA, but no
**primary Zhipu blog post or model card** was captured in-window, and the
MIT open weights are not yet public — both would advance it to `confirmed`.

**Transition triggers:**
- MIT weights + API go live, or a primary Zhipu model card → UPDATE,
  advance `verification` to `confirmed`.
- A successor (GLM 5.x) → new ticket; do not reopen this one.
- ≥4 weeks past release, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further GLM 5.2 release/benchmark/weights signal UPDATES
this ticket. Other open-weight models stay on their own tickets
([[minimax-m3]], [[alibaba-qwen-3-7-plus]], [[gemma-4]]).
