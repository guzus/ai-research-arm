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
  [[gemma-4]]. **2026-06-16:** corroborated by a dated **2026-06-15 launch
  announcement** (Zhipu/"Huazhang Technology") billing GLM-5.2 as its newest
  flagship — **1M long context**, "leading on long-range tasks," **to be
  open-sourced under MIT** — restated across China-tech aggregators. Still no
  captured primary Zhipu blog/model card and the MIT weights are described as
  forthcoming, so verification stays `partial`.

  **2026-06-18:** MIT weights are now **live** and the release is fully
  corroborated. Z.ai's **official announcement thread** (@Zai_org, 2026-06-16
  17:40 UTC) bills GLM-5.2 as "Frontier Intelligence, Open Weights" — a
  **744B-A40B MoE**, **1M context**, two reasoning-effort levels (max/high),
  priced the same as GLM-5.1, **46.2% DeepSWE**. Same-day **ecosystem uptake**:
  **vLLM day-0 support in v0.23.0**, plus Notion and Baseten live, and MIT
  weights on HuggingFace. Community placement is strong — @kimmonismus calls it
  "the third best model available across open and proprietary," it reportedly
  took the top of the design arena after Fable 5 was pulled, and @ns123abc rates
  it "Opus 4.6 / GPT-5.4 tier." Z.ai also shipped a **ZCode** desktop coding
  agent built around the model. With an official thread + live MIT weights +
  independent ecosystem adoption, verification advances to `confirmed`; neutral
  SWE-bench/LiveCodeBench placement beyond the lab's own DeepSWE number is the
  remaining gap.
expected: "Shipped — MIT weights live (HuggingFace), API + GLM Coding Plan, day-0 vLLM/Notion/Baseten support; neutral third-party benchmark placement still settling"
labels:
  - frontier-model
  - open-weights
  - china
  - coding
  - released
verification: confirmed
sources:
  - "@Zai_org"
  - https://news.ycombinator.com/item?id=48518684
  - "@testingcatalog"
  - "@kimmonismus"
  - "@ns123abc"
created_at: 2026-06-14
updated_at: 2026-06-18
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-14
    change: "Created — Zhipu AI shipped GLM 5.2: deployed in the GLM Coding Plan now, with API + MIT open weights promised within a week. Reported 1M context, max/high thinking modes; early one-shot coding benchmarks rank it above Qwen 3.6 27B. Dominant open-weights story this cycle (HN ~468 pts, top of r/LocalLLaMA). Usable in the coding plan now → status released; widely corroborated across HN/r/LocalLLaMA but no captured primary Zhipu blog/model card and weights not yet public → verification partial. Sits with open-weight peers [[minimax-m3]], [[alibaba-qwen-3-7-plus]], [[gemma-4]]"
  - ts: 2026-06-16
    change: "Corroboration — a dated 2026-06-15 launch announcement (attributed to Zhipu / 'Huazhang Technology') restates GLM-5.2 as the newest flagship with 1M long context, a claimed lead on long-range tasks, and MIT open-sourcing, echoed across China-tech aggregators. Strengthens the release record but still no captured primary Zhipu blog/model card and the MIT weights are described as forthcoming → status stays released, verification stays partial."
  - ts: 2026-06-18
    change: "MIT weights live + verification → confirmed. Z.ai's official thread (@Zai_org 2026-06-16) bills GLM-5.2 as 744B-A40B MoE, 1M context, max/high reasoning, 46.2% DeepSWE, same price as GLM-5.1. Day-0 ecosystem uptake (vLLM v0.23.0, Notion, Baseten) plus HuggingFace MIT weights. Strong community placement — @kimmonismus 'third best model across open + proprietary,' top of design arena after Fable 5's pull, @ns123abc 'Opus 4.6 / GPT-5.4 tier'; Z.ai also shipped a ZCode desktop agent. Official thread + live weights + independent adoption → verification confirmed; neutral SWE-bench/LiveCodeBench placement still the open gap."
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
