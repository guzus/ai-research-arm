---
slug: cognition-ai
title: Cognition AI
type: entity
aliases: ["Cognition", "Cognition AI", "Cognition Labs", "Devin"]
tags: [agentic, coding-agent, startup, ai-engineering]
summary: Maker of the Devin autonomous coding agent; raised $1B+ at a $26B post-money valuation in May 2026 against $492M ARR (~13× YoY), with 89% of Cognition's own code now written by Devin.
created_at: 2026-05-29
updated_at: 2026-05-29
sources:
  - {title: "ARA daily digest 2026-05-29", path: research/digest/2026-05-29-digest.md}
  - {title: "ARA daily digest 2026-05-27", path: research/digest/2026-05-27-digest.md}
---

Cognition AI is the maker of **Devin**, the autonomous software-engineering
agent that became the reference point for "agent until done" in 2024–2025. It
is the natural opposite-pole to [[anthropic]]'s [[dynamic-workflows]] (and
OpenAI Codex Goal Mode) in the agentic-iterate-until-objective category: a
purpose-built agent product rather than a parallel-subagent feature in a chat
client.

## Why it matters
- **Cap-table.** Raised **$1B+ at a $26B post-money** in the May 2026 cycle
  (ARA digest 2026-05-29, carried from 2026-05-27). Pre-money was a small
  fraction of the [[anthropic|Anthropic Series H]] but the funding/ARR ratio
  is striking: **$492M ARR / ~13× YoY**. Folds straight into the [[ai-capex]]
  supercycle narrative on the demand side: agent-product revenue scaling
  almost exactly with infrastructure backlog growth.
- **Self-eating dogfood.** **89% of Cognition's own code is now written by
  Devin.** This is the kind of internal-adoption number that frontier labs
  rarely volunteer; for a pure-play agent maker, it is the strongest possible
  signal that the product clears its own bar.
- **Competitive frame.** The agentic-coding space crystallized this cycle:
  Cognition Devin, [[anthropic]] [[dynamic-workflows]] on Claude Code (gated
  to Enterprise / Team / Max), and OpenAI Codex Goal Mode (carry, 2026-05-27)
  are now the three named systems for fan-out / iterate-until-done coding
  work. All three converged within ~10 days.
- **Security exposure compounds.** As Devin is given broader autonomy on
  customer repos, the [[agentic-ai-security]] failure modes — supply-chain
  CVEs, capability misuse — apply to the agent product directly, not just
  to the agent frameworks it competes with.

## Open questions
- **Moat against Dynamic Workflows.** If [[anthropic]] turns Claude Code into
  a native parallel-subagent platform with Opus-4.8-Fast economics, does
  Cognition's "agent product" framing stay differentiated, or compress into
  a UX layer?
- **Customer concentration.** What share of the $492M ARR is one or two
  anchor customers? The 13× YoY rate is a "growth at any cost" footprint;
  the bear case is that incumbents' free agent surfaces erode it.
- **GPU dependence.** A coding agent that runs Devin against full
  repositories sits hard against frontier-model API costs — does
  Cognition try to vertically integrate via its own inference stack?
