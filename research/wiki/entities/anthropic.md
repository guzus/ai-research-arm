---
slug: anthropic
title: Anthropic
type: entity
aliases: [Anthropic, "Anthropic PBC", "@AnthropicAI"]
tags: [frontier-lab, claude, ai-safety, foundation-models]
summary: AI safety company and frontier lab behind the Claude model family, operating gated frontier model Mythos and valued at $965B post-money after closing a $65B Series H in May 2026.
created_at: 2026-05-24
updated_at: 2026-05-29
sources:
  - {title: "ARA daily digest 2026-05-20", path: research/digest/2026-05-20-digest.md}
  - {title: "ARA daily digest 2026-05-21", path: research/digest/2026-05-21-digest.md}
  - {title: "ARA daily digest 2026-05-29", path: research/digest/2026-05-29-digest.md}
  - {title: "Claude Opus 4.7 release", url: "https://www.anthropic.com/news/claude-opus-4-7", date: 2026-04-16}
  - {title: "Claude Opus 4.8 release", url: "https://www.anthropic.com/news/claude-opus-4-8", date: 2026-05-29}
  - {title: "Anthropic Series H", url: "https://www.anthropic.com/news/series-h", date: 2026-05-29}
---

Anthropic is an AI-safety-focused frontier lab and the maker of the **Claude**
model family. As of the 2026-05-29 cycle it ships **[[claude-opus-4-8]]** as its
standard public frontier model — succeeding Opus 4.7 — and operates a more
capable, deliberately gated model — **Mythos** — behind the multi-org "Project
Glasswing" partnership (ARA digest 2026-05-29). It is the
dominant counterweight to OpenAI and Google in the [[ai-capex]]-fueled race for
frontier capability.

## Why it matters
Four developments through May 2026 put Anthropic at the center of the field:

- **Capital closed.** The Bloomberg-flagged round closed on 2026-05-29 as a
  **$65B Series H at a $965B post-money valuation** — Sequoia / Dragoneer /
  Altimeter / Greenoaks lead the cap table, and the print confirms the >$30B /
  >$900B carry from earlier in the month. Anthropic-internal guidance points
  past **~$50B ARR run-rate by end of June** (ARA digest 2026-05-29). A scale
  that only makes sense against the broader [[ai-capex]] supercycle.
- **Frontier ship: Opus 4.8.** [[claude-opus-4-8]] reports 84% on
  Online-Mind2Web (ahead of Opus 4.7 and GPT-5.5), claims 4× less likely to
  let code flaws go unremarked, and shows deception-rate behavior "on par with
  Mythos Preview" — the cleanest alignment-improvement number any frontier lab
  has shipped alongside a new flagship in 2026. Pricing held at Opus 4.7's
  level; Fast mode 3× cheaper. Anthropic signals Mythos-class models moving
  toward GA "in the coming weeks" (ARA digest 2026-05-29).
- **Agentic stack ships.** Same release window: **[[dynamic-workflows]]** in
  Claude Code (hundreds of parallel subagents per session, Enterprise / Team /
  Max gated), effort control on claude.ai, and mid-task system-prompt
  injection via the Messages API — Anthropic's most concrete answer to
  [[cognition-ai|Cognition Devin]] and OpenAI Codex Goal Mode on the
  agentic-iterate-until-objective axis.
- **Karpathy → Anthropic.** Andrej Karpathy, an OpenAI co-founder and ex-Tesla
  AI lead, joined Anthropic's pre-training team under Nick Joseph "to get back
  to R&D" — the year's most significant talent move, confirmed by WSJ /
  CNBC / Axios (ARA digest 2026-05-20).
- **Consolidation around MCP.** Anthropic acquired SDK/MCP-server platform
  Stainless (its 4th acqui-hire in six months), tightening control over the
  developer surface and the agent protocol it stewards.

Anthropic also competes head-to-head with Google's flagship releases like
[[gemini-3-5-flash]] — analysts frame the Gemini 3.5 family as "in the class of
GPT-5.5, well short of Mythos," using Anthropic's gated model as the frontier
reference point (ARA model tickets, 2026-05-14).

Anthropic's MCP stewardship is now load-bearing for the broader
[[agentic-ai-security]] story: the 2026-05-29 vLLM/MCP framework CVE and the
OpenClaw post-mortem put the supply chain Anthropic anchors directly in the
public discussion. And [[agent-lifespan-engineering]] (AgingBench, 2026-05-29)
is the empirical counter-signal: swapping in a stronger Claude *reduced*
deployed-agent pass rate, sharpening the question of where Opus 4.8's gains
actually translate to production.

## Open questions
- **Gated frontier strategy.** Anthropic has signaled no public release of
  Mythos. Does a permanently-gated frontier model become the norm, and what does
  that do to the public benchmark race against [[gemini-3-5-flash]] and GPT-5.x?
- **Compute dependence.** A $900B-valuation lab needs guaranteed capacity. How
  much of Anthropic's roadmap rides on [[neocloud]] / hyperscaler GPU supply
  versus owned infrastructure?
- **Pre-training acceleration.** Karpathy's group reportedly uses Claude to
  accelerate frontier pre-training. Does recursive self-acceleration materially
  change Anthropic's release cadence?
