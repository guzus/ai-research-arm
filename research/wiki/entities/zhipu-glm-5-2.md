---
slug: zhipu-glm-5-2
title: Zhipu GLM-5.2
type: entity
aliases: ["Zhipu GLM 5.2", "Zhipu GLM-5.2", "GLM 5.2", "GLM-5.2", "Z.ai GLM-5.2"]
tags: [open-weights, china, coding, long-context, frontier-model]
description: Zhipu AI / Z.ai flagship model shipped under an MIT license with 1M context and two reasoning-effort levels; the marquee long-context Chinese open-weight release in the Fable 5 shutdown window.
created_at: 2026-06-17
timestamp: 2026-06-17T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-06-17", path: research/digest/2026-06-17-digest.md}
  - {title: "ARA model ticket — Zhipu GLM-5.2", path: research/models/tickets/zhipu-glm-5-2.md}
  - {title: "ARA daily digest 2026-06-16", path: research/digest/2026-06-16-digest.md}
  - {title: "ARA daily digest 2026-06-15", path: research/digest/2026-06-15-digest.md}
  - {title: "ARA daily digest 2026-06-14", path: research/digest/2026-06-14-digest.md}
---

Zhipu GLM-5.2 is the cycle's marquee Chinese open-weight flagship. Per the
ARA model ticket, it is already deployed in the GLM Coding Plan, with API access
and **MIT-licensed open weights** promised within about a week of the
2026-06-15 launch announcement. Reported specs include **1M-token context** and
max/high "thinking" modes.

## Why it matters

- **Long-context flagship for the open-weights wave.** GLM-5.2 gives the
  [[open-weights]] page a concrete long-context anchor: usable now in a coding
  plan, MIT weights promised, 1M context, and reported early community coding
  tests ranking it above Qwen 3.6 27B. It belongs beside [[minimax-m3]],
  [[moonshot-kimi-k2-7-code]], [[gemma-4]], and [[deepseek]] in the open-model
  pressure stack.
- **It filled the Fable 5 vacuum.** As [[claude-fable-5|Fable 5 / Mythos 5]]
  stayed dark under the US export-control order, GLM-5.2 became one of the
  examples used to argue that closed-frontier shutdowns accelerate the very
  open-weight commoditization they are supposed to slow.
- **The verification status is intentionally conservative.** The ticket is
  `released` because the model is usable in the GLM Coding Plan, but
  `verification: partial` because ARA had not captured a primary Zhipu model
  card and the MIT weights were still described as forthcoming.

- **Shipped under MIT (2026-06-17).** GLM-5.2 went out **under an MIT
  license** — **1M context**, **two reasoning-effort levels (max/high)**,
  **priced the same as GLM-5.1**, framed as "frontier intelligence" — with
  **day-0 vLLM v0.23.0 support** plus live **Notion** and **Baseten**
  availability within hours. Z.ai claims it "leads GLM-5.1 by a wide margin"
  and **46.2% on DeepSWE**; a community "62 vs [[claude-opus-4-8|Opus 4.8]]'s
  69 on SWE-Bench Pro" comparison is circulating but unverified, and neutral
  third-party SWE-bench/LiveCodeBench placement has not yet landed. The MIT
  ship converts the earlier "weights promised" status into a concrete
  open-weights anchor in the [[claude-fable-5|Fable 5]] shutdown window — see
  [[open-weights]] (ARA digest 2026-06-17).

## Open questions

- **Weights actually landing.** The decisive transition is public MIT weights
  plus a primary model card. Until then, the open-weight claim is directionally
  important but not complete.
- **Neutral evals.** Does GLM-5.2 hold up on contamination-aware coding,
  long-context, and agentic tasks, or is the current signal mostly community
  excitement and vendor-adjacent benchmarking?
- **Router adoption.** If GLM-5.2 becomes a default open coding backend, does it
  show up in [[openrouter]] traffic mix and price discovery, or stay inside
  Z.ai's own product surface?
