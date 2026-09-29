---
slug: claude-sonnet-5-5
title: Claude Sonnet 5.5
type: entity
aliases: ["Claude Sonnet 5.5", "Sonnet 5.5", "claude-sonnet-5-5", "claude-sonnet-5.5"]
tags: [model-release, anthropic, claude, agentic-coding, frontier-model, pricing]
description: Anthropic's 2026-09-28 mid-tier Claude 5.5 model at unchanged $2/$10; vendor Terminal-Bench 4.0 70.6% vs Sonnet 5's 10.3%, with the 30% cheaper claim a per-task assertion, not a price cut.
created_at: 2026-09-29
timestamp: 2026-09-29T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-29", path: research/digest/2026-09-29-digest.md}
  - {title: "ARA model ticket — Claude Sonnet 5.5", path: research/models/tickets/anthropic-sonnet-5-5-2026-09.md}
---

**Claude Sonnet 5.5** (`claude-sonnet-5-5`) is [[anthropic]]'s 2026-09-28
mid-tier model, the second SKU in the Claude 5.5 family after
[[claude-opus-5-5|Opus 5.5]]. Released **18:04 UTC**. List price is unchanged
from [[claude-sonnet-5|Sonnet 5]] — **$2 / $10 / $0.20 per Mtok** input /
output / cache-read. Anthropic claims **30%+ faster output** and **up to 30%
lower cost per task** from fewer tokens and tool calls; the token card itself
did not move. It is now the **claude.ai free-tier** default. Haiku 5.5 is
still "coming weeks" (Anthropic, TechCrunch, The Decoder, Simon Willison, HN
539 pts; ARA daily digest 2026-09-29).

## Why it matters

- **Vendor table vs Sonnet 5 and Opus 5.5.** Anthropic's published deltas:
  Terminal-Bench 4.0 **70.6%** vs Sonnet 5 **10.3%** / Opus 5.5 **66.4%**;
  FrontierCode 1.1 Main **52.1%** Xhigh vs **42.4%** / **54.4%**; CursorBench
  4.0 **55.5%** vs **34.1%** / **57.8%**; GDPval-AA v2.1 **1844** vs **1449** /
  **1846**; HLE with tools **64.5%** vs **54.9%** / **67.7%**; OSWorld 2.1
  partial **80.1%** vs **57.0%** / **81.8%**. It is the first Sonnet Anthropic
  says launches with Opus-class cyber fallbacks, and the first it says beats
  Pokémon Red from screenshots only (Anthropic; ARA daily digest 2026-09-29).
- **The 70.6% step is partly harness fit.** A near-floor prior score of 10.3%
  on a new harness version usually means the older agentic scaffold did not
  fit, not a 7× raw-capability jump. No independent reproduction of the
  Terminal-Bench number at default effort appeared in the day's local sources.
  HN argued the same split: **jtrn** called it "90% of Opus 5.5 at half the
  cost"; **bayesianbot** flagged that cache reads price the same as Opus 5.5
  (Twitter, HN; ARA daily digest 2026-09-29).
- **"30% cheaper" is not a price cut.** The claim is per-task token and tool
  use, not a moved card. Simon Willison reported the same max-thinking
  **128k-token bug** already seen on Opus 5.5. See [[agentic-ai-security]] for
  the cyber-fallback posture (Simon Willison, Twitter; ARA daily digest
  2026-09-29).

## Open questions

- **Does 70.6% on Terminal-Bench 4.0 reproduce at default effort** on an
  independent harness, or only on Anthropic's launch scaffold?
- **Does the per-task saving survive max/xhigh?** The cost claim and the
  scoreboard numbers may not be the same effort setting — the same trap
  [[claude-opus-5-5]] already hit.
- **When does Haiku 5.5 actually ship?** Still a "coming weeks" line, not a
  date.
