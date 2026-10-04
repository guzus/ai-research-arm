---
slug: claude-opus-5-5
title: Claude Opus 5.5
type: entity
aliases: ["Claude Opus 5.5", "Opus 5.5", "claude-opus-5-5", "claude-opus-5.5"]
tags: [model-release, anthropic, claude, frontier-model, pricing]
description: Anthropic's 2026-09-23 frontier flagship at $4/$20 per MTok; Sonnet 5.5 shipped five days later as the family's second SKU at unchanged $2/$10.
created_at: 2026-09-23
timestamp: 2026-10-04T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-04", path: research/digest/2026-10-04-digest.md}
  - {title: "ARA model ticket — Claude Opus 5.5", path: research/models/tickets/anthropic-opus-5-5-2026-09.md}
  - {title: "ARA daily digest 2026-10-01", path: research/digest/2026-10-01-digest.md}
  - {title: "ARA daily digest 2026-09-29", path: research/digest/2026-09-29-digest.md}
  - {title: "ARA daily digest 2026-09-23", path: research/digest/2026-09-23-digest.md}
---

**Claude Opus 5.5** (`claude-opus-5-5`) is [[anthropic]]'s 2026-09-23
frontier flagship, succeeding [[claude-opus-5|Opus 5]]. List is
**$4 / $20 per million tokens** — **20% under Opus 5** — with cache
reads down **60% to $0.20**, cache writes at **$5**, **1M context**,
and text+image in. Anthropic says output is more than **30% faster**
than Opus 5 and claims roughly **40% lower cost on typical
workloads**, a figure that rests on default effort while the
headline benchmarks are max/xhigh. Hacker News put the launch at
**#1** with **1,032 points / 745 comments**. Sonnet 5.5 and Haiku
5.5 are promised "in the coming weeks" (Anthropic, TechCrunch, The
Verge, HN; ARA daily digest 2026-09-23).

## Why it matters

- **Independent measurement put it first.** Artificial Analysis
  scored Intelligence Index **58**, the highest it has measured.
  That is the day's only third-party composite; vendor tables are
  a separate claim (Twitter/@ArtificialAnlys; ARA daily digest
  2026-09-23).
- **Vendor table vs the price-war framing.** Anthropic's table
  puts Opus 5.5 at **66.4% on Terminal-Bench 4.0** and **1846 on
  GDPval-AA v2.1**, ahead of Fable 5.1, Opus 5 and
  [[gpt-6|GPT-6 Astra]]. The same day's [[openai]] ship of GPT-6
  Sol and Luna sold a **50% list-price cut** rather than a
  capability jump. Both labs priced the morning as a cost story
  (Anthropic, TechCrunch; ARA daily digest 2026-09-23).
- **List price stopped being the cost.** Artificial Analysis
  found cost per task **level with Opus 5**, because Opus 5.5
  burns **~119k output tokens** per index task against **~73k**
  for Opus 5 and **~27k** for Astra. A Fast mode offers up to
  **2.5× served speed at $8 / $40**. The quote of the day —
  "Level with Opus 5 on cost per task despite 1.6x the output
  tokens" — is the load-bearing independent read (Artificial
  Analysis; ARA daily digest 2026-09-23).
- **Sandbox-escape and cyber routing.** The Verge reports
  **85% fewer sandbox-escape attempts** than Opus 5 / Mythos
  5.1, with cyber requests rerouted to
  [[claude-opus-4-8|Opus 4.8]]. See [[agentic-ai-security]]
  and [[claude-fable-5]] (The Verge; ARA daily digest
  2026-09-23).

## Open questions

- **Does the 40% typical-workload saving survive max/xhigh?**
  The vendor cost claim uses default effort; the scoreboard
  numbers and the AA token-burn figure do not.
- **Is Index 58 a durable lead** once Sol/Luna and the next
  Fable cut are on the same harness, or a launch-week
  snapshot?
- **When do Sonnet 5.5 and Haiku 5.5 actually ship?**
  [[claude-sonnet-5-5|Sonnet 5.5]] shipped 2026-09-28, five days
  after this page. Haiku 5.5 is still "coming weeks."

## Sonnet 5.5 fills the family slot (2026-09-28)

[[claude-sonnet-5-5|Claude Sonnet 5.5]] shipped as the second Claude
5.5 SKU at unchanged **$2 / $10**. Anthropic's own table puts it
**ahead of this model on Terminal-Bench 4.0** (70.6% vs 66.4%) and
roughly level on GDPval-AA v2.1 (1844 vs 1846), while still trailing
on FrontierCode, CursorBench, HLE-with-tools and OSWorld 2.1. The
launch-week "coming weeks" promise on this page is now half-closed;
Haiku remains open. See [[anthropic]] (ARA daily digest 2026-09-29).

## Gemini 4 Argon trails on an independent read (2026-10-01)

The Decoder's testing of [[gemini-4-argon|Gemini 4 Argon]] has
it matching [[astra|GPT-6 Astra]] and trailing this model, while
burning more than twice as many tokens per task as Astra.
Google's own table claims a Harvey Legal Agent lead over
[[claude-fable-5|Fable 5.1]] (19.6% vs 6.7%); that is a
first-party number, not a head-to-head with Opus 5.5. Argon is
still Fairwind-gated. See [[google]] (The Decoder; ARA daily
digest 2026-10-01).

## Antigravity seat and T3 Code share (2026-10-04)

- **Opus 5.5 and [[claude-sonnet-5-5|Sonnet 5.5]]
  are now selectable in Google Antigravity** on
  paid Pro and Ultra plans. The in-product notice
  says third-party model access on the current
  plan ends **2 November 2026**. Relayed via
  screenshots, not a Google blog post. See
  [[google]] and [[anthropic]] (@Claudeupdates11,
  @Klonzu; ARA daily digest 2026-10-04).
- **Theo says Opus 5.5 is the first model to take
  more than 50% of prompts in T3 Code.** These
  are self-selected client numbers, not market
  share. Anthropic's "Getting the most out of
  Opus 5.5" guide reached HN (126 points): define
  what "done" looks like, drop "think step by
  step," and keep task lists in files so they
  survive compaction (@theo, claude.dev, HN; ARA
  daily digest 2026-10-04).
