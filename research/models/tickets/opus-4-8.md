---
slug: opus-4-8
title: Claude Opus 4.8 — public release
company: Anthropic
model: Claude Opus 4.8
status: released
status_note: |
  Public release 2026-05-28 at the same per-token price as Opus 4.7.
  Headline gains over 4.7: ~4× lower rate of missing flaws in its own
  generated code, sharper judgment, more honest self-progress reporting,
  ability to work independently longer. **Fast mode** is now ~2.5× faster
  than normal and **3× cheaper than the Opus 4.7 Fast preview**, available
  in Claude Code via `/fast` (API access via waitlist). A research
  preview of **Dynamic Workflows** in Claude Code spawns hundreds of
  parallel sub-agents per session, aimed at large code migrations.
  Available immediately on AWS (Microsoft Foundry confirmed by @Azure
  2026-05-28 18:40 UTC), with Anthropic API support including
  in-message system instructions that don't break the prompt cache.
expected: null
labels:
  - frontier-model
  - released
  - coding
  - agentic
  - fast-mode
verification: confirmed
sources:
  - "@claudeai"
  - "@AnthropicAI"
  - "@alexalbert__"
  - "@Azure"
  - "@testingcatalog"
  - "@kimmonismus"
created_at: 2026-05-28
updated_at: 2026-06-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-28
    change: "Created — Claude Opus 4.8 announced and released same day (@claudeai 16:57 UTC, retweeted by @AnthropicAI). Same price as Opus 4.7. Successor to the closed [[opus-4-7]] ticket. Headline: 4× better at catching flaws in its own generated code, sharper judgment, longer independent work, Dynamic Workflows research preview in Claude Code (parallel sub-agent swarms), Fast mode 2.5× faster and 3× cheaper than 4.7 Fast preview. Microsoft Foundry availability confirmed same day"
  - ts: 2026-05-29
    change: "Day-1 adoption signal: Eden AI, Microsoft Foundry, third-party benches surfacing. Reported pace: 42 days from Opus 4.7 (Apr 16) to Opus 4.8 (May 28), the shortest Opus-to-Opus gap to date"
  - ts: 2026-06-01
    change: "Post-launch use signals (week 1): trending-news framing 'Anthropic's Claude Opus 4.8 Tops AI Index Over OpenAI's GPT-5.5' at ~19K post-count; @testingcatalog 2026-05-31 14:49 UTC endorses Opus 4.8 Max as 'best for writing at this moment'; Salesforce reportedly moved its entire dev org to Claude Code with no token limits (231-day migration cut to 13 days, 79% more PRs/dev per the-decoder). Adversarial framing: Cobi Gantz (Chapter CEO, @theinformation 2026-05-30 18:00 UTC) accuses Anthropic of 'Apple-playbook' pre-launch model degradation (single-source, no benchmark, no response); @kimmonismus 2026-05-31 02:11 UTC 'Opus 4.8 is a solid jump over Opus 4.7, GPT-5.5 xhigh still beats it by a pretty clear margin while being cheaper' (directional, not third-party eval). No primary @AnthropicAI / @darioamodei rebuttal in-window. No regression / rollback. Status remains released"
---

Claude Opus 4.8 is Anthropic's successor to
[Opus 4.7](./opus-4-7.md), announced and released the same day
(2026-05-28, 16:57 UTC) at the same per-token pricing. The framing on
@claudeai's launch post — "sharper judgment, more honesty about its own
progress, and the ability to work independently for longer than its
predecessors" — emphasises agentic reliability over raw benchmark gains.

**Headline improvements vs Opus 4.7.** Per Anthropic's own messaging
and @alexalbert__'s launch thread:

- **~4× lower rate of missing flaws** in its own generated code.
- Sharper judgment, more natural conversation, stronger collaboration
  on both coding and knowledge work.
- Calibrated thinking effort — the team specifically tuned to reduce
  the over-/under-thinking complaints that hit Opus 4.7.

**Fast mode.** Available immediately for Opus 4.8 in Claude Code via
`/fast`, at ~2.5× the speed of normal mode and **3× cheaper than the
Opus 4.7 Fast preview**. API access is via account-manager request /
waitlist rather than open self-serve. @alexalbert__ characterises Fast
mode as the right default for interactive Claude Code work, with normal
mode reserved for longer async tasks.

**Dynamic Workflows (research preview).** A new orchestration surface
in Claude Code that lets Opus 4.8 spawn hundreds of parallel sub-agents
within a single session — pitched at large code migrations (a third
party reported migrating a 750k-LOC enterprise codebase in 11 days
using this framework). The research-preview label means rollout is
gated and the API shape may change.

**Distribution on day one.** Anthropic API (same model ID family as
Opus 4.7, with a 4.8 variant), Claude Code, AWS Bedrock, and Microsoft
Foundry (announced by @Azure on launch day). The Messages API also
gains the ability to place system instructions inside the messages
array without breaking the prompt cache.

**Why this is a separate ticket from [opus-4-7](./opus-4-7.md).**
Per the schema, the Opus 4.7 ticket was closed 2026-05-19 with reason
`released-and-aged`, and successor releases get their own ticket
rather than reopening the prior one. The history on this ticket is the
only place that captures the 4.7 → 4.8 transition.

**Transition triggers:**
- ≥4 weeks past 2026-05-28 release with no successor → close with
  `released-and-aged`.
- A successor `opus-4-9` (or rename) appears → create a new ticket;
  do not reopen this one.
- Reported regressions or rollback (e.g. official Anthropic pause on
  4.8 rollout) → keep `released` but document via history entry; close
  only on explicit Anthropic action.
