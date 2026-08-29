---
slug: anthropic-opus-5-leak-2026-07
title: Claude Opus 5 — public release
company: Anthropic
model: Claude Opus 5
status: closed
status_note: |
  Confirmed released and in wide public use as of 2026-07-25/26. Dozens of
  independent accounts report first-hand usage of Opus 5 directly (coding
  benchmarks, ARC-AGI-3 puzzles, pricing comparisons vs Fable 5 and GPT-5.6
  Sol, agentic/subagent workflows, threejs one-shots), and aggregator/
  weekly-digest accounts (@btibor91, @AlphaSignalAI) list it as a shipped
  release alongside other Week-30-2026 model news. @IRudyak notes it is
  "Anthropic's fourth Claude 5 model release in less than two months."
  Anthropic itself published methodology detail tied to its "newest
  models" (an 80% system-prompt reduction in Claude Code, per
  @VaibhavSisinty relaying Anthropic's own writeup), consistent with a
  real Opus 5 ship. No single official Anthropic announcement post was
  captured in this signal window, but the volume and diversity of
  independent first-hand usage reports clears the bar for
  `released`/`confirmed`. Originally filed as a single-source rumor
  (@Mr_Salio, 2026-07-22, claiming imminent launch with a rumored
  3M-token context window) — that claim is now superseded by direct
  evidence of shipment; the 3M-context claim remains uncorroborated and
  is not carried forward as fact.
expected: null
labels:
  - anthropic
  - frontier-model
  - released
verification: confirmed
sources:
  - "@Mr_Salio"
  - https://x.com/IRudyak/status/2080923338222796814
  - https://x.com/AlphaSignalAI/status/2081292892187029971
  - https://x.com/btibor91/status/2081288037980319903
  - https://x.com/NielsRogge/status/2080947253687001345
created_at: 2026-07-22
updated_at: 2026-08-23
closed_at: 2026-08-23
closed_reason: released-and-aged
history:
  - ts: 2026-07-22
    change: "Created — single low-follower account (@Mr_Salio) claims Claude Opus 5 launch is imminent (Thursday floated), briefly appeared in Cursor before disappearing, rumored 3M-token context. No corroboration from other accounts or Anthropic → status rumored, verification unverified."
  - ts: 2026-07-26
    change: "Confirmed released — widespread independent first-hand usage across dozens of accounts (coding, ARC-AGI-3, agentic workflows, pricing comparisons vs Fable 5 / GPT-5.6 Sol), weekly-digest accounts list it as shipped (@btibor91, @AlphaSignalAI), and Anthropic's own methodology writeup (80% system-prompt cut for 'newest models,' relayed by @VaibhavSisinty) is consistent with a real ship → status released, verification confirmed."
  - ts: 2026-08-23
    change: "Closed — released-and-aged. Claude Opus 5 shipped publicly on/around 2026-07-24 and was confirmed released on this ticket 2026-07-26; that is beyond the >=4-week trigger, and the release itself has settled into normal coverage. The model is very much still being argued about — @scaling01 (2026-08-22, ~650 likes) calls it 'the closest thing we have to whatever Anthropic has internally… give it a target and it will hillclimb,' NVIDIA's AVO agent uses it as its base model ([[nvidia-avo-arc-agi-3-2026-08]]), and a large cohort including @kimmonismus and @TheAhmadOsman report it feeling inconsistent and verbose — but that is model-quality discourse, not release-lifecycle signal. The two live threads have their own tickets: the Claude Code reasoning-effort mapping that drove much of the 'Opus feels dumber' wave is at [[anthropic-claude-code-effort-mapping-2026-08]], where Anthropic engineer @trq212 conceded on the record that 'Opus 5 is a really spiky model and we want our models to be consistent.' Community expectation of an Opus 5.1 is inference, not an Anthropic statement — if a 5.1 is announced it gets a new ticket. History preserved."
---

**Claude Opus 5** is confirmed released and in wide public use. What began
as a single-source rumor on 2026-07-22 (@Mr_Salio, claiming an imminent
launch with a rumored 3M-token context window) is now corroborated by
dozens of independent accounts using the model directly — coding
benchmarks, ARC-AGI-3 puzzle performance, pricing comparisons against
Fable 5 and GPT-5.6 Sol, agentic subagent workflows, and one-shot demo
builds. Weekly AI-news digest accounts (@btibor91, @AlphaSignalAI) list
Opus 5 as a shipped Week-30-2026 release alongside other model news.

**Why `released`/`confirmed` without a single official announcement
capture.** No individual Anthropic press post was captured in this
window, but the bar for `released` is public availability, not a
specific citation format — and the volume, independence, and
first-hand nature of the usage reports (people running real workloads
against it, not relaying a rumor) is stronger evidence than a single
announcement link would be. Anthropic's own published methodology note
about its "newest models" (an 80% Claude Code system-prompt reduction,
relayed by @VaibhavSisinty) is consistent with — though not sole proof
of — a real Opus 5 ship.

**What's not carried forward.** The original leak's claimed 3M-token
context window has no independent corroboration in this window and is
not treated as fact; if a concrete context-window figure surfaces, note
it via an UPDATE rather than assuming the original leak was accurate.

**Transition triggers:**
- An official Anthropic announcement post/blog → UPDATE sources, no
  status change needed (already `released`).
- Concrete pricing, context-window, or benchmark specifics from a
  primary source → UPDATE `status_note`.
- ≥4 weeks past release, settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** further Claude Opus 5 signal (pricing, benchmarks,
adoption) UPDATES this ticket. Slug retained from the original leak
filing per slug-immutability convention.
