---
slug: claude-opus-4-8
title: Claude Opus 4.8
type: entity
aliases: ["Claude Opus 4.8", "Opus 4.8", "claude-opus-4-8"]
tags: [model-release, anthropic, claude, frontier-model, alignment]
summary: Anthropic's 2026-05-28 frontier flagship, succeeding Opus 4.7 at flat pricing with a +4.9pp agentic-coding lift, +137 knowledge-work Elo, and a Fast Mode that runs ~2.5× faster and 3× cheaper.
created_at: 2026-05-29
updated_at: 2026-06-10
sources:
  - {title: "ARA daily digest 2026-06-10", path: research/digest/2026-06-10-digest.md}
  - {title: "ARA daily digest 2026-05-29", path: research/digest/2026-05-29-digest.md}
  - {title: "ARA daily digest 2026-05-30", path: research/digest/2026-05-30-digest.md}
  - {title: "Introducing Claude Opus 4.8 (Anthropic)", url: "https://www.anthropic.com/news/claude-opus-4-8", date: 2026-05-28}
  - {title: "Anthropic releases Opus 4.8 with new Dynamic Workflow tool (TechCrunch)", url: "https://techcrunch.com/2026/05/28/anthropic-releases-opus-4-8-with-new-dynamic-workflow-tool/", date: 2026-05-28}
  - {title: "Claude Opus 4.8 — Simon Willison", url: "https://simonwillison.net/2026/May/28/claude-opus-4-8/", date: 2026-05-28}
---

Claude Opus 4.8 is [[anthropic]]'s public frontier release of 2026-05-28
(carrying through May 29–30), the direct successor to **Opus 4.7** in the
Claude family. It shipped concurrently with the **$65B Series H close** (see
[[anthropic]]) and the **[[dynamic-workflows]]** feature in Claude Code, making
the May 28 window the most concentrated single-day shipping window from
Anthropic of the year. GA across **claude.ai, Anthropic API, Bedrock, Vertex AI**.

## Why it matters
- **Confirmed benchmark deltas vs Opus 4.7** (ARA digest 2026-05-30): agentic
  coding **64.3 → 69.2** (+4.9pp), multidisciplinary reasoning with tools
  **54.7 → 57.9** (+3.2pp), agentic computer use **82.8 → 83.4** (+0.6pp),
  knowledge-work Elo **1753 → 1890** (+137). The +137 Elo is the largest
  single-cycle knowledge-work jump Anthropic has reported.
- **Pricing held; Fast Mode ~2.5× faster and 3× cheaper.** Per-token price
  stays at Opus 4.7's level. The Fast Mode delta is the lever that keeps the
  [[dynamic-workflows]] fan-out economics tractable.
- **HN reception.** **1,693 pts / 1,319 comments** — the dominant story of the
  day across May 28–30 (ARA digest 2026-05-30). Discussion split between
  capability deltas vs Opus 4.7, pricing-held-flat, and positioning vs
  GPT-5.5.
- **Quote of the day.** **Simon Willison: "A modest but tangible improvement."**
  The cleanest one-line summary of the release — a *flow-state* update; the
  architecture story is being saved for the **Mythos-class** line, re-teased
  in the same post.

- **Now the Fable 5 safeguard floor (2026-06-10).** With the **2026-06-09 launch
  of [[claude-fable-5|Fable 5 / Mythos 5]]**, Opus 4.8 took on a second role: it is
  the **auto-route target** for high-risk cyber/bio/chem queries inside Fable 5
  (Anthropic says this fires in "<5% of sessions"), so a Fable 5 deployment
  performs **closer to Opus 4.8 than to Mythos 5** on those exact tasks. The
  reroute also became the launch's loudest friction strand — users hit it on
  **benign queries** at ~2× token burn. Pricing-wise Fable 5 lists at **~2× Opus
  4.8 ($10/$50 per M)**, making Opus 4.8 the cheaper, always-safeguarded workhorse
  beneath the new flagship (ARA digest 2026-06-10).

## Open questions
- **Successor sequencing — resolved.** Opus 4.8 was a **single-cycle bridge**:
  the Mythos-class line shipped as [[claude-fable-5|Fable 5 / Mythos 5]] on
  2026-06-09, ~12 days after Opus 4.8, with Opus 4.8 retained as the safeguard
  reroute floor rather than retired.
- **Does Fast-Mode 3× cheaper compound the agentic story?** Dynamic Workflows
  fan-out economics scale with the per-call price of the cheapest
  always-available Claude. A 3× cut shifts where the cost ceiling bites.
- **Deployed-agent regression.** [[agent-lifespan-engineering]] / AgingBench
  reports that swapping **Sonnet 4.6 → Opus 4.7** in Claude Code CLI *dropped*
  PyTest pass rate by ~15%. Does Opus 4.8 reverse that, or does the same
  memory-policy dynamic re-bite?
