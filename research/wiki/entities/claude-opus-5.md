---
slug: claude-opus-5
title: Claude Opus 5
type: entity
aliases: ["Claude Opus 5", "Opus 5", "claude-opus-5"]
tags: [model-release, anthropic, claude, frontier-model, security]
description: Anthropic's 2026-07-25 frontier flagship, pitched as near-Fable-5 performance at roughly half the token price, with a system card citing markedly improved prompt-injection resistance.
created_at: 2026-07-26
timestamp: 2026-07-27T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-07-27", path: research/digest/2026-07-27-digest.md}
  - {title: "ARA daily digest 2026-07-26", path: research/digest/2026-07-26-digest.md}
  - {title: "ARA daily digest 2026-07-25", path: research/digest/2026-07-25-digest.md}
  - {title: "ARA model ticket — Claude Opus 5 leak", path: research/models/tickets/anthropic-opus-5-leak-2026-07.md}
---

Claude Opus 5 is [[anthropic]]'s frontier-flagship release, launched
2026-07-25 (TechCrunch, The Verge, The Decoder; #1 on Hacker News at 680
points/386 comments) as the successor to [[claude-opus-4-8|Opus 4.8]] in the
Opus line. Coverage frames it as delivering performance "close to" or "near"
[[claude-fable-5|Fable 5]] at roughly **half the token price** — The Decoder's
framing is the more bullish "near-Fable-5 performance," while The Verge's
headline is more hedged ("'close' to Fable 5's capabilities"). Voice mode
also rolled out across Anthropic's most capable models on all platforms the
same day.

**Provenance note.** The internal model-ticket tracker
(`anthropic-opus-5-leak-2026-07.md`) still records this as an unconfirmed
single-source rumor from 2026-07-22; the 2026-07-25 press coverage is the
first independently corroborated signal, and the ticket had not yet been
updated to reflect the actual launch as of this page's creation — a
CRUD lag between the ticket lane and the digest, not a factual dispute.

## Why it matters

- **Pricing/benchmark positioning (2026-07-26).** Follow-on Decoder coverage
  reports Opus 5 **matching or beating Fable 5 on most benchmarks** at well
  below Fable 5's token price — sharpening the July 25 "near-Fable-5
  performance, half the price" framing into a more specific competitive claim
  (ARA digest 2026-07-26).
- **Prompt-injection defenses detailed (2026-07-26).** Anthropic engineer
  Boris Cherny said the model's system card (p.73) shows Opus 5 holding up
  well across prompt-injection evals and red-teaming, calling it
  **Anthropic's least prompt-injectable model yet** (via Simon Willison) — a
  direct data point for the [[agentic-ai-security]] theme, and notable timing
  given that theme's tracked history of agent-memory and browser-based
  injection incidents (ARA digest 2026-07-26).
- **HN reception.** 680 points / 386 comments made it the dominant AI story
  of the 2026-07-25 cycle, ahead of Black Forest Labs' Flux 3 and Flux 3 X
  Mimic releases (ARA digest 2026-07-25).
- **Tops a new intelligence benchmark (2026-07-27).** The Decoder reports
  Opus 5 topping a benchmark "designed to measure real intelligence,"
  surpassing both [[claude-fable-5|Fable 5]] and [[gpt-5-6|GPT-5.6 Sol]] —
  an independent-outlet-relayed leaderboard claim distinct from the
  vendor/press "matches or beats Fable 5" framing already tracked above
  (ARA digest 2026-07-27).

## Open questions
- **Does the model-ticket tracker reconcile?** The ticket lane still shows
  this as an unverified rumor; watch for it to be updated to `released` on
  its next run.
- **Independent benchmark verification.** The "matches or beats Fable 5"
  claim is vendor/press-relayed so far — does an independent evaluator
  (e.g. a third-party leaderboard) corroborate the pricing/performance
  claim against [[claude-fable-5|Fable 5]]?
