---
slug: deepseek-v4-1-flash
title: DeepSeek V4.1 Flash
type: entity
aliases: ["DeepSeek V4.1 Flash", "V4.1 Flash", "DeepSeek-V4.1-Flash", "deepseek-flash"]
tags: [frontier-model, open-weights, chinese-llm, moe, multimodal, mit-license]
description: DeepSeek's 552B MIT-licensed multimodal MoE with a causal encoder–decoder stack; weights, tech report and the $0.003/$0.15/$0.60 off-peak card shipped together on 2026-09-11, scoring 40 on Artificial Analysis.
created_at: 2026-09-11
timestamp: 2026-09-11T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-11", path: research/digest/2026-09-11-digest.md}
---

**DeepSeek V4.1 Flash** is [[deepseek|DeepSeek's]] 2026-09-11 weight
drop: a **552B MIT-licensed multimodal MoE** with a new **causal
encoder–decoder (CED)** stack. Weights, a tech report, and the live
Flash card posted together at **06:10 UTC**, after the public USD
table still showed August rates at 04:00. The API id is
`deepseek-flash`. It succeeds [[deepseek-v4-flash|V4-Flash-0731]]
as the cheap Fast tier; `deepseek-v4-pro` is scheduled to **route
here and bill at Flash rates on 2026-09-14**.

## Why it matters

- **A new architecture, not a re-post-train.** The stack is a
  **40-layer CED (20+20)** activating **8B on input and 16B on
  output**, with **CSA2 sparse attention**, **FP4 main KV at 890
  bytes/token**, **Engram conditional memory**, a from-scratch
  **DeepSeek-ViT**, **45T multimodal pretrain tokens**, and **1M
  context**. That is a different artifact from the 284B/13B-active
  [[deepseek-v4-flash|V4-Flash-0731]] this wiki already tracks
  (DeepSeek, Hugging Face; ARA daily digest 2026-09-11).
- **The promised off-peak card is live.** List is **$0.003 /
  $0.15 / $0.60** off-peak. Yesterday's digest recorded those
  figures as a V4 Flash cache-hit cut plus an interim
  `deepseek-v4.1-flash-expires-on-0910` tier; today's drop is
  the weights-plus-card event that closes that interim
  (DeepSeek; ARA daily digest 2026-09-11).
- **Two independent composites, neither a Terminal-Bench 4
  reproduction.** Artificial Analysis's first independent
  composite is **40 — four points above V4 Pro 0813 (36)** —
  with **194 tok/s** and **$0.27 per index task**. The provider
  list still says *"Estimate (independent evaluation
  forthcoming)"*; the model is **sixth of 113** in its
  comparison class, not among closed frontier systems. Vals
  ranked it the **top open-weight model**, beating
  [[moonshot-kimi-k3|Kimi K3]] at **$0.30 a test** (Artificial
  Analysis, Vals AI, Twitter; ARA daily digest 2026-09-11).
- **Vendor coding sits next to Opus; HLE does not travel.**
  First-party **DeepSWE 74.2** sits next to
  [[claude-opus-5|Opus 5.0]] **74.0**; **HLE 36.8 vs Opus
  56.3** is the gap the digest says will not travel (DeepSeek,
  Hugging Face; ARA daily digest 2026-09-11).
- **It owned Hacker News, then left.** The launch peaked at
  **836 points / 462 comments** as the day's official
  weights + paper + live card, then left the front page by
  the 22:36 UTC snapshot. See [[open-weights]] (Hacker News;
  ARA daily digest 2026-09-11).

## Context

The ship lands the morning after US agencies named
[[deepseek]] in advisory **AA26-251A**, and the same day
[[anthropic]] accused the lab of silently relaying its own
customers' prompts to Opus. The MIT drop and the distillation
charge are not the same fact; do not merge them. See
[[federal-ai-policy]].

## Open questions

- **Does the 2026-09-14 Pro-to-Flash route hold?** If
  `deepseek-v4-pro` bills at Flash rates, the 4.5× Pro
  premium this wiki recorded on 2026-08-13 is a two-week
  leftover, not a durable tier.
- **Does AA 40 survive a non-estimate evaluation?** The
  composite is already independent; the provider row is
  still labelled forthcoming.
- **Does the MIT license hold for the next tier?** The same
  open question this wiki asked of V4-Flash-0731, now asked
  of a multimodal successor.
