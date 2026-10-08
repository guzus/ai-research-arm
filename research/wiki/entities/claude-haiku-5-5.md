---
slug: claude-haiku-5-5
title: Claude Haiku 5.5
type: entity
aliases: ["Claude Haiku 5.5", "Haiku 5.5", "claude-haiku-5-5", "claude-haiku-5.5"]
tags: [model-release, anthropic, claude, small-model, pricing]
description: Anthropic's 2026-10-07 small Claude 5.5 model; $0.10/$0.50 to 100K tokens then $0.50/$2.50, first Haiku with effort controls.
created_at: 2026-10-08
timestamp: 2026-10-08T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-08", path: research/digest/2026-10-08-digest.md}
  - {title: "ARA model ticket — Claude Haiku 5.5", path: research/models/tickets/anthropic-haiku-5-5-2026-10.md}
---

**Claude Haiku 5.5** (`claude-haiku-5-5`) is
[[anthropic]]'s 2026-10-07 small model, the
third SKU in the Claude 5.5 family after
[[claude-opus-5-5|Opus 5.5]] and
[[claude-sonnet-5-5|Sonnet 5.5]]. It is live
on Claude.ai, Claude Code, AWS, Google Cloud,
and Microsoft Foundry. It is the first Haiku
with effort controls (Anthropic, The Decoder,
Simon Willison, Hacker News; ARA daily digest
2026-10-08).

## Why it matters

- **The headline card matches [[gpt-6|GPT-6
  Luna]] only up to 100K tokens.** List is
  **$0.10 / $0.50** per million tokens on
  prompts up to 100K, then **$0.50 / $2.50**.
  Long agent prompts therefore pay **5×** the
  advertised rate. HN called the 100K band
  "absurdly low" for classifiers and a trap
  for agents (Anthropic, HN; ARA daily digest
  2026-10-08).
- **Vendor benches beat Luna on computer use
  and terminals, with a tokenizer catch.**
  Anthropic reports OSWorld 2.1 offline
  **72.4%** (Haiku 4.5 15.7%, Luna 48.9%),
  Terminal-Bench 4.0 **39.2%** (4.5 0%, Luna
  16.4%), Chartography **46.4%**, and
  GDPval-AA **1620** vs Luna's 1437. Simon
  Willison notes the new tokenizer uses about
  **1.25×** as many tokens as Haiku 4.5, so
  some of the list-price saving is eaten.
  [[claude-sonnet-5-5|Sonnet 5.5]] still leads
  Terminal-Bench at **70.6%**. Willison's
  pelican test passed at medium effort and
  above (Anthropic, Simon Willison, HN 468 /
  220; ARA daily digest 2026-10-08).
- **The same day Anthropic cheapened the
  mid-tier cache path.** Sonnet 5.5 cache-read
  prices were halved to **$0.10/MTok**, and
  monthly Platform credits of **$100 / $200 /
  $500** (no rollover) were added. Computer-use
  and browser-use loops also landed in the
  Python and TypeScript SDKs. Those are
  company-level moves; see [[anthropic]]
  (Anthropic; ARA daily digest 2026-10-08).

## Open questions

- **Does the 100K cutoff hold for real agent
  traces?** If typical computer-use prompts
  sit above it, the Luna-matching card is not
  the price most buyers pay.
- **Do independent harnesses reproduce the
  OSWorld / Terminal-Bench deltas**, or is
  the jump partly a new scaffold plus effort
  controls?
