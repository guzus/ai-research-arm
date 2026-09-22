---
slug: jev
title: Jev (TypeSafe)
type: entity
aliases: [Jev, "TypeSafe Jev", TypeSafe, OpenJev, JevBench, RLCD]
tags: [decision-model, classifier, open-weights, system-one, structured-output]
description: TypeSafe's non-autoregressive decision model; Jared Palmer's Apache-2.0 Kev-0.8B/4B/9B family shipped the same noul/choice/score API and took four of the week's top HN slots.
created_at: 2026-09-20
timestamp: 2026-09-22T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-22", path: research/digest/2026-09-22-digest.md}
  - {title: "ARA daily digest 2026-09-20", path: research/digest/2026-09-20-digest.md}
  - {title: "ARA model ticket — Typesafe Jev", path: research/models/tickets/typesafe-jev-2026-09.md}
---

**Jev** is TypeSafe's non-chat "system one" decision
model — typed structured choices with calibrated
probabilities, not free-form generation. Former
OpenAI staff announced it on **2026-09-15**; this
page waited until the 2026-09-20 digest, when
open-weight clones and a Vercel adoption print
made the product a compounding subject rather
than a launch blurb. See [[open-weights]].

## Why it matters

- **Closed Jev is the reference product.** The
  2026-09-15 founder post pitched RLCD training,
  **20–200× faster / 40–400× cheaper** ranges
  against an unnamed baseline, and **$0.042 per
  million input tokens with output free**. Treat
  the multipliers as marketing; the architectural
  claim (a fixed output schema) is structurally
  true of any constrained decoder. Independent
  first-party-vs-clone numbers below are the
  first scoreboard (model ticket
  `typesafe-jev-2026-09`; ARA daily digest
  2026-09-20).
- **Vercel AI Gateway adoption (2026-09-20).**
  Guillermo Rauch said Jev reached about **13%
  of paid Gateway teams in 24 hours** — **2×
  the [[gpt-5-6|GPT-5.6]] family, 6×
  [[claude-fable-5|Fable 5.1]]** — and that
  open models took **78.4%** of token volume
  while Moonshot, [[deepseek]] and [[zhipu|Z.ai]]
  combined spend passed [[openai]]. Spend is
  inference across mostly-US providers, not lab
  revenue. TypeSafe's classifier is free through
  **25 September** (ARA daily digest
  2026-09-20).
- **Laya (ConvAI) is the open-weight argument.**
  An Apache-2.0 ModernBERT family (`laya` 421M,
  `laya-multilingual` 322M, `laya-typed-decisions`
  421M) does choice / score / noul in one
  forward pass. Author-dated idea:
  arXiv 2503.23303 (March 2025) and 2510.01237
  (September 2025). First-party vs TypeSafe Jev
  1.13.0: typed-decisions **0.766 vs 0.727**,
  AG News **0.950 vs 0.910**, ECE **0.081 vs
  0.246**, P50 **32.8 ms vs 236–276 ms**. Named
  miss: Banking77 **0.425 vs Jev 0.870** past
  ~20 options. The HN thread retitled to "I
  built non-autoregressive decision models with
  RL a year ago" and closed at **991/229**
  (HN, Latent Space; ARA daily digest
  2026-09-20).
- **Same-day specialists, not general Jev
  killers.** **Von-1.0** (`wfzyx/von-1.0`) is a
  395M ModernBERT-large, 8,192 ctx, RLCD on
  250k NLI pairs, Apache 2.0. Card NLI
  **91.23%** vs published Jev **88.3%**;
  independent `jabr/classifier-benchmark` is
  Von **81.6%** macro vs Jev **97.2%**.
  **CUA-S1-FORMS** is a 706k-parameter / 2.8 MB
  form specialist under MIT `trycua/cua`:
  whole-set **99.7%** vs hosted Jev **83.6%**
  on their task; **7–9 ms** local vs
  **260–280 ms** hosted. Latent Space counted
  **six Jev clones in two days**; OpenJev
  itself peaked at **683/285** then left the
  evening front page (ARA daily digest
  2026-09-20).
- **JevBench v1.2** scored 21 typed-decision
  systems on 534 decisions. classifier.dev
  leads at **84.8**; TypeSafe Jev 1.13.0 is
  **75.3**; [[gpt-5-6|GPT-5.6 Luna]] has the
  highest Intelligence (**96.8**) but ranks
  12th at **$0.247 / 1,000 decisions**. A
  bench, not a frontier-lab eval (Benchmark
  Heaven; ARA daily digest 2026-09-20).

## Open questions

- **Does RLCD survive an independent write-up?**
  The training method is the load-bearing
  novelty; nothing in today's files describes
  it beyond the name.
- **Are the clones the product or the method?**
  If a year-old ModernBERT family matches Jev
  on most typed-decision rows, the moat is
  distribution (Vercel, free-through-the-25th)
  rather than architecture.
- **Does a decision model stay a category?**
  LangChain shipped a Jev-in-the-agent-loop
  guide the same morning. Watch whether
  agent runtimes treat Jev as a tool or as
  a competing default.

## Kev family and Jev-as-a-judge (2026-09-22)

- **Decision models became the week's
  dominant open-source thread.** Jev-style
  "System One" checkpoints that return typed
  choices with zero generated tokens took
  **four of the top Hacker News slots** and
  shipped a trainable Apache-2.0 family (HN,
  Simon Willison, LangChain; ARA daily digest
  2026-09-22).
- **Jared Palmer released Kev-0.8B / 4B /
  9B** — rank-16 LoRA adapters plus a
  pointer head on frozen Qwen3.5 bases,
  exposing the same `noul` / `choice` /
  `score` API as TypeSafe's hosted Jev.
  New-source test accuracy **0.684 / 0.837 /
  0.852**; a stored temperature drops
  Kev-9B ECE from **0.106 to 0.042** without
  changing any answer. Honest gaps
  published: MMLU **0.74 vs Jev's 0.90**,
  and a **0.45–0.57** automation share vs
  Jev's **0.70**. This is the trainable
  open-weight counterpart to last cycle's
  Laya / Von / CUA-S1 clones, not a new
  hosted product. See [[open-weights]] and
  [[alibaba]] (HN, Simon Willison; ARA daily
  digest 2026-09-22).
- **LangChain shipped Jev-as-a-judge** for
  agent traces in LangSmith Evals,
  benchmarking it against LLM judges on
  accuracy, repeatability, latency, and
  cost. That answers yesterday's "tool or
  competing default" question in one
  direction: a judge inside the agent loop,
  not a replacement runtime (LangChain; ARA
  daily digest 2026-09-22).
