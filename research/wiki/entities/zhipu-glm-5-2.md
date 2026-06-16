---
slug: zhipu-glm-5-2
title: Zhipu GLM-5.2
type: entity
aliases: ["Zhipu GLM 5.2", "Zhipu GLM-5.2", "GLM 5.2", "GLM-5.2", "Z.ai GLM-5.2"]
tags: [open-weights, china, coding, long-context, frontier-model]
description: Zhipu AI / Z.ai flagship model deployed in the GLM Coding Plan with 1M context and MIT-licensed open weights promised; the marquee long-context Chinese open-weight release in the Fable 5 shutdown window.
created_at: 2026-06-17
timestamp: 2026-06-17T00:00:00Z
sources:
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
  plan, MIT weights promised, 1M context, and early community coding tests
  ranking it above Qwen 3.6 27B. It belongs beside [[minimax-m3]],
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
