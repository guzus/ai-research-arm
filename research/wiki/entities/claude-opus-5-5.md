---
slug: claude-opus-5-5
title: Claude Opus 5.5
type: entity
aliases: ["Claude Opus 5.5", "Opus 5.5", "claude-opus-5-5", "claude-opus-5.5"]
tags: [model-release, anthropic, claude, frontier-model, pricing]
description: Anthropic's 2026-09-23 frontier flagship at $4/$20 per MTok — 20% under Opus 5 — first on Artificial Analysis' Intelligence Index at 58, the highest score it has measured.
created_at: 2026-09-23
timestamp: 2026-09-23T00:00:00Z
sources:
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
- **When do Sonnet 5.5 and Haiku 5.5 actually ship?** The
  "coming weeks" line is a promise, not a date.
