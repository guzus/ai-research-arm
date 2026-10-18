---
slug: deepseek-v4-1-flash
title: DeepSeek V4.1 Flash
type: entity
aliases: ["DeepSeek V4.1 Flash", "V4.1 Flash", "DeepSeek-V4.1-Flash", "deepseek-flash", "DeepSeek-V4.1-Flash-1017", "V4.1-Flash-1017", "dsv41f_1017"]
tags: [frontier-model, open-weights, chinese-llm, moe, multimodal, mit-license]
description: DeepSeek's MIT-licensed multimodal MoE; the 2026-10-17 Flash-1017 checkpoint posts first-party DeepSWE 77.0 and Terminal-Bench 4.0 42.3, with no independent evals yet.
created_at: 2026-09-11
timestamp: 2026-10-18T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-18", path: research/digest/2026-10-18-digest.md}
  - {title: "ARA model ticket — DeepSeek-V4.1-Flash-1017", path: research/models/tickets/deepseek-v4-1-flash-1017-2026-10.md}
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

## Flash-1017 post-training refresh (2026-10-18)

- **DeepSeek shipped
  V4.1-Flash-1017** as a
  post-training refresh of this
  card, not a new base. The
  `deepseek-flash` system
  fingerprint changed at about
  **03:24 UTC**; its MD5
  decodes to a `dsv41f_1017`
  build string, and the
  first-party release note
  followed about five hours
  later. [[deepseek]] called it
  a Pareto improvement —
  stronger benches, faster
  completion, shorter outputs —
  via self-feedback RL. MIT
  weights remain. The Hugging
  Face card now reports **~763B
  params** and about **510 GB**
  of weights, against the
  original **552B** figure on
  this page; treat the size
  restatement as unresolved
  until a card or tech-report
  reconciliation lands
  (@deepseek_ai, @teortaxesTex,
  Hugging Face; ARA daily
  digest 2026-10-18 and ticket
  `deepseek-v4-1-flash-1017-2026-10`).
- **All headline scores are
  DeepSeek's own**, compared
  with the prior Flash,
  [[gpt-5-6|GPT-5.6 Sol]] and
  [[claude-opus-5|Opus 5]] —
  not the current
  [[claude-opus-5-5|Opus 5.5]]
  / [[gpt-6|GPT-6.1 Sol]].
  DeepSWE **77.0** vs
  74.2 / 73.0 / 74.0;
  Terminal-Bench 4.0 **42.3**
  vs 31.2 / 39.9 / **51.8**
  (Opus 5 still leads by about
  **9.5 points**); Automation-
  Bench **60.5**; HLE no-tools
  **42.6** vs Opus 5's
  **56.3**. The ticket also
  relays Agents' Last Exam
  **35.4** vs Opus 5 **28.6**.
  No independent composite has
  landed. @scaling01's
  distillation and
  contamination claims rest on
  informal probes and prove
  nothing yet (DeepSeek,
  MarkTechPost, The Decoder;
  ARA daily digest 2026-10-18).
- **List is $0.15 / $0.60
  off-peak and $0.30 / $1.20
  peak**, against **$5 / $25**
  for Opus 5. DeepSeek also
  opened Search and Fetch APIs
  at **$0.75 per 1,000
  successful calls**, and is
  offering unbilled access via
  Claude Code and Codex until
  about **1 November**. Hands-on
  reports call it "massively
  faster" until it
  "rabbitholes" on the last
  10% of a task. It was HN's
  top story of the day at
  **620 points / 539 comments**.
  See [[open-weights]]
  (@teortaxesTex, HN; ARA daily
  digest 2026-10-18).

## Open questions

- **Does the 2026-09-14 Pro-to-Flash route hold?** If
  `deepseek-v4-pro` bills at Flash rates, the 4.5× Pro
  premium this wiki recorded on 2026-08-13 is a two-week
  leftover, not a durable tier.
- **Does AA 40 survive a non-estimate evaluation?** The
  composite is already independent; the provider row is
  still labelled forthcoming. Flash-1017 has no independent
  composite at all yet.
- **Why did the HF card jump from 552B to ~763B?** A
  post-training refresh should not change total parameters
  this much unless the original figure or the new card is
  counting something different.
- **Does the MIT license hold for the next tier?** The same
  open question this wiki asked of V4-Flash-0731, now asked
  of a multimodal successor.
