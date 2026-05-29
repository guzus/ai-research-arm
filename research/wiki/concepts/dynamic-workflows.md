---
slug: dynamic-workflows
title: Dynamic Workflows
type: concept
aliases: ["Dynamic Workflows", "Claude Code Dynamic Workflows", "parallel subagents"]
tags: [agentic, claude-code, anthropic, subagents, codebase-migration]
summary: Anthropic's 2026-05-29 Claude Code feature that fans a single session into hundreds of parallel subagents, gated to Enterprise / Team / Max tiers and aimed at codebase-scale migrations.
created_at: 2026-05-29
updated_at: 2026-05-29
sources:
  - {title: "ARA daily digest 2026-05-29", path: research/digest/2026-05-29-digest.md}
  - {title: "Introducing Dynamic Workflows in Claude Code", url: "https://claude.com/blog/introducing-dynamic-workflows-in-claude-code", date: 2026-05-29}
---

**Dynamic Workflows** is a Claude Code feature shipped by [[anthropic]] on
2026-05-29 alongside [[claude-opus-4-8]]. It lets a single Claude Code session
spawn **hundreds of parallel subagents** to attack a codebase-scale task — the
canonical example is a large-codebase migration — coordinated and reported back
to the parent session. Gated to **Enterprise / Team / Max** tiers.

## Why it matters
- **Concrete answer to "agent until done."** Dynamic Workflows reads as
  Anthropic's most concrete entry in the **agentic-iterate-until-objective**
  category, opposite [[cognition-ai|Cognition Devin]] (whose maker now writes
  89% of its own code via Devin) and OpenAI Codex Goal Mode (ARA digest
  2026-05-29).
- **Cost surface shifts to fan-out.** A session that fans out into hundreds of
  subagents puts the cost story on **per-subagent token spend** and parent
  orchestration overhead, not on a single conversation. The same release made
  **Opus 4.8 Fast mode 3× cheaper**, which is the lever that keeps fan-out
  economically tractable.
- **Companion features land in the same window.** Effort control on
  claude.ai (user-side compute-budget knob) and **mid-task system-prompt
  injection via the Messages API** ship with Dynamic Workflows — together
  these turn multi-turn sessions into editable agentic loops without
  restarting context (ARA digest 2026-05-29).
- **Community reception.** A standalone HN thread (118 pts / 92 comments)
  ran in parallel with the launch — excitement balanced with questions about
  cost controls and **blast radius on destructive operations**, the natural
  failure mode of large-fan-out agentic systems.

## Open questions
- **Blast radius.** Hundreds of parallel subagents on a real codebase create
  a much larger destructive surface than a single chat session — the same
  failure surface that [[agentic-ai-security]] tracks. What guardrails ship
  by default, and what falls to the user?
- **Memory policy, not model strength, may dominate.** [[agent-lifespan-engineering]]
  predicts that subagent half-life is set by the parent's memory policy, not
  by which Claude model the children call.
- **Coordination tax.** How much of the savings from parallelism gets eaten
  by the parent session's orchestration / conflict-resolution overhead?
- **Tier gating economics.** Enterprise / Team / Max only — does this stay a
  high-tier feature, or pressure downward as competitors (Devin / Goal Mode)
  expose comparable fan-out at lower tiers?
