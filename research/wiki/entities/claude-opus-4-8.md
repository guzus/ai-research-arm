---
slug: claude-opus-4-8
title: Claude Opus 4.8
type: entity
aliases: ["Claude Opus 4.8", "Opus 4.8", "claude-opus-4-8"]
tags: [model-release, anthropic, claude, frontier-model, alignment]
summary: Anthropic's 2026-05-29 frontier flagship, succeeding Opus 4.7 at the same price with materially better alignment numbers and the cleanest deception-rate result of any 2026 frontier release.
created_at: 2026-05-29
updated_at: 2026-05-29
sources:
  - {title: "ARA daily digest 2026-05-29", path: research/digest/2026-05-29-digest.md}
  - {title: "Claude Opus 4.8 release", url: "https://www.anthropic.com/news/claude-opus-4-8", date: 2026-05-29}
---

Claude Opus 4.8 is [[anthropic]]'s public frontier release of 2026-05-29, the
direct successor to **Opus 4.7** in the Claude family. It shipped concurrently
with the **Series H close** (see [[anthropic]]) and the **[[dynamic-workflows]]**
feature in Claude Code, making 2026-05-29 the most concentrated single-day
shipping window from Anthropic of the year.

## Why it matters
- **Capability print.** 84% on **Online-Mind2Web** — ahead of Opus 4.7 and
  GPT-5.5; **4× less likely to let code flaws go unremarked** than its
  predecessor (ARA digest 2026-05-29).
- **Alignment, in real numbers.** Deception-rate behavior reported "on par with
  **Mythos Preview**" — the gated frontier — which is the cleanest
  alignment-improvement number any frontier lab has put on a flagship release
  this year. The pairing of a new SOTA print *and* an alignment improvement
  reads as a deliberate counter to the "scaling forces tradeoffs" framing.
- **Pricing held; Fast 3× cheaper.** Per-token price stays at Opus 4.7's level,
  and **Fast mode is now 3× cheaper** — meaningful for high-volume agentic
  workflows that [[dynamic-workflows]] is built to multiply. Available across
  claude.ai, the API, and Claude Code.
- **HN reception.** 943 pts / 751 comments on the launch thread — concurrent
  with the Series H thread (166 pts / 146 comments), driving cross-thread
  discussion about commercialization vs. safety mission (ARA digest 2026-05-29).
- **Successor signal.** Anthropic flagged **Mythos-class models** moving toward
  GA "in the coming weeks" in the same release — the strongest public signal
  yet that the gated-frontier strategy is not permanent.

## Open questions
- **Where does the alignment gain come from?** "On par with Mythos Preview" on
  deception rate is a striking claim for a non-gated model — does it generalize
  outside the eval set, or reflect the test distribution?
- **Does Fast-mode 3× cheaper compound the agentic story?** Dynamic Workflows
  fan-out economics scale with the per-call price of the cheapest
  always-available Claude. A 3× cut shifts where the cost ceiling bites.
- **Successor sequencing.** With Mythos GA "in the coming weeks," is Opus 4.8
  a multi-month flagship or a single-cycle bridge?
