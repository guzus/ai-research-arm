---
slug: claude-sonnet-5
title: Claude Sonnet 5
type: entity
aliases: ["Claude Sonnet 5", "Sonnet 5", "claude-sonnet-5"]
tags: [model-release, anthropic, claude, agentic-coding, frontier-model]
description: Anthropic's 2026-06-30 mid-tier model — the default on Free and Pro, with the $2/$10 intro pricing made permanent on 2026-08-10 (September increase cancelled) and a 1M-token context — positioned as a cheap agentic default.
created_at: 2026-07-01
timestamp: 2026-08-11T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-11", path: research/digest/2026-08-11-digest.md}
  - {title: "ARA daily digest 2026-07-02", path: research/digest/2026-07-02-digest.md}
  - {title: "ARA daily digest 2026-07-01", path: research/digest/2026-07-01-digest.md}
  - {title: "@claudeai launch post", date: 2026-06-30}
---

Claude Sonnet 5 (`claude-sonnet-5`) is [[anthropic]]'s mid-tier model, launched
**18:00 UTC June 30, 2026** with a published system card. It became the
**default model on Free and Pro** across all Claude apps and the Platform the
same day. It is positioned as a **cheaper way to run agents** than
[[claude-opus-4-8|Opus 4.8]], GPT-5.5, and Gemini Pro — the workhorse tier
beneath Anthropic's frontier line (ARA digest 2026-07-01).

## Why it matters
- **Pricing and shape.** Intro pricing **$2/M input and $10/M output** (rising
  to **$3/$15 in September**); **1M-token context, 128K output**. Simon Willison
  notes it **drops the temperature / top_p / top_k knobs** and ships a **new
  tokenizer** that yields **~30% more tokens per input** — an effective ~30%
  price increase that partly offsets the headline cut.
- **Day-2 verdict is split.** Independent benchmarks are uneven: The Decoder
  reports a **GDPval-AA v2 score of 1,618**, edging [[claude-opus-4-8|Opus 4.8]]
  on some tasks, while it trails on others. Developer reception ranges from
  "best cheap agentic default" to "descoped [[claude-fable-5|Fable]] /
  maintenance release," with [[zhipu-glm-5-2|GLM 5.2]] speed comparisons
  (~60 tok/s vs. GLM 5.2's claimed 150–300) attached directly — tying the
  release into the [[open-weights]] price/speed pressure.
- **Deliberately lower cyber capability.** Sonnet 5 scores **lower than the
  older Sonnet 4.6** on CyberGym vulnerability-discovery — a deliberate
  "lower cyber risk" reduction consistent with Anthropic's Mythos
  export-control posture (see [[federal-ai-policy]] and
  [[agentic-ai-security]]). Capability was traded down on the one axis that got
  [[claude-fable-5|Fable 5 / Mythos 5]] export-controlled.
- **Enterprise distribution day-one.** **GitLab** put Sonnet 5 live on its Duo
  Agent Platform across all tiers, calling it the first model to handle its full
  benchmark range, "up 93.8% from its predecessor."
- **Reception cools on price-to-performance (2026-07-02).** A week after launch,
  sentiment turned negative: The Decoder reports Sonnet 5 **chews ~40% more tokens per
  task** than its predecessor, **nearly doubling real cost despite identical list
  prices** — compounding the launch-day tokenizer tax below. The complaint fed the
  wider **"tokenmaxxing" pushback** ([[meta|Meta]] capping internal token spend,
  Palantir's Karp arguing enterprises need an application/ontology layer over raw token
  access) that ran through the day's [[ai-capex]] ROI debate — reframing "cheap agentic
  default" as expensive-in-practice (ARA digest 2026-07-02).

## Open questions
- **Does "cheap agentic default" hold under the tokenizer tax?** The ~30%
  token inflation and the September price step-up narrow the cost gap the launch
  headline advertised.
- **A maintenance release, or a descoped Fable?** The split reception turns on
  whether Sonnet 5 is a genuine capability step or a safety-descoped repackaging
  shipped while [[claude-fable-5|Fable 5]]'s general re-release stayed
  conspicuously absent.

## Pricing made permanent (2026-08-10/11)

Anthropic made the **$2/$10 per million input/output tokens** pricing
**permanent**, **cancelling the increase scheduled after 31 August** (the
launch-day plan was a step to $3/$15 in September). Read across the feed as
**squeezing Haiku out of its own price tier** — at $2/$10 the mid-tier model now
prices below where a dedicated Haiku tier used to sit, a pressure signal on
Anthropic's own tiering ahead of its planned IPO. The tokenizer-tax and
cost-per-task questions above are now the standing cost argument, since the
price step that was supposed to claw some margin back has been cancelled (ARA
daily digest 2026-08-11).
