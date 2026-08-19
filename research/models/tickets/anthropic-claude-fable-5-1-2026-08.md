---
slug: anthropic-claude-fable-5-1-2026-08
title: Claude Fable 5.1 — successor stealth-testing on a subset of accounts
company: Anthropic
model: Claude Fable 5.1 (reported)
status: in-testing
status_note: |
  A successor to Fable 5 — reported as **Fable 5.1** (5.5 also floated) —
  is being **served to a subset of accounts that have "Fable 5" selected**
  in Claude, per leaker **@synthwavedd** (2026-08-18, "🚨 A successor to
  Fable 5, likely Fable 5.1, is now being tested for a subset of accounts
  with 'Fable 5' selected on Claude…"). @kimmonismus amplified it with the
  credibility note that synthwavedd "is one of the most reliable AI leakers
  out there" and read it as "an official launch may therefore be very
  close." It trended as its own AI news item (~956 posts).

  **@AndrewCurran_ independently says the same thing from a different
  angle:** "I've said before that Fable 5.1 has been ready to ship for a
  long time, for weeks. It may be live for some of us right now, a small
  stealth test flight leading up to launch is the norm for both OpenAI and
  Anthropic."

  Status is `in-testing` rather than `rumored` because the claim is that a
  **real artifact is being served in production to real accounts**, which
  is the canonical in-testing shape. Verification is `partial`: two
  independent secondary accounts, no Anthropic statement, no model card, no
  API id, and no firsthand user posting a distinguishing output.

  Circumstantial support, none of it decisive: Anthropic is visibly capacity
  constrained this week (@ClaudeDevs extended the 50% weekly Claude Code
  limit increase through Aug 31 while warning "capacity may be tight over
  the coming weeks"; the status page reported degraded performance across
  Mythos 5, Fable 5, Opus 5, Sonnet 5 and Haiku 4.5 on 2026-08-18).
expected: "TBD — no Anthropic announcement, date, model card, API id or pricing. Leakers describe a stealth test flight, which historically precedes launch by days-to-weeks"
labels:
  - anthropic
  - frontier-model
  - stealth-test
  - leak
verification: partial
sources:
  - "@synthwavedd"
  - "@kimmonismus"
  - "@AndrewCurran_"
  - "@jukan05"
created_at: 2026-08-19
updated_at: 2026-08-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — @synthwavedd (2026-08-18) reports a Fable 5 successor, likely Fable 5.1, being served to a subset of accounts with Fable 5 selected; amplified by @kimmonismus (who vouches for the leaker and reads a launch as very close) and independently echoed by @AndrewCurran_, who says Fable 5.1 has been ready to ship for weeks and that a small stealth test flight before launch is normal for both OpenAI and Anthropic. Trending as its own AI news item (~956 posts). Status in-testing — the claim is a real artifact served in production, not a tease. Verification partial: two independent secondary accounts, no Anthropic statement, model card, API id or firsthand distinguishing output. Successor to the closed [[claude-fable-5]]."
---

Anthropic pulled **Claude Fable 5** in mid-June under an export-control
order ([[anthropic-fable-mythos-export-control-2026-06]]); its ticket
[[claude-fable-5]] closed `released-and-aged` on 2026-07-31. This ticket
tracks what appears to be its successor.

**The signal.** Leaker **@synthwavedd** reports that accounts with "Fable
5" selected in Claude are, for a subset of users, being served something
else — the canonical shape of an Anthropic stealth test flight.
@kimmonismus, who has a reasonable track record of sorting leakers,
vouched for the source explicitly and read it as an imminent launch.
@AndrewCurran_ arrived at the same conclusion independently and earlier:
Fable 5.1 "has been ready to ship for a long time, for weeks," and "it may
be live for some of us right now."

**Why `in-testing`, why `partial`.** The lifecycle distinction that matters
here is whether an artifact exists. A prediction that Anthropic will ship a
5.1 would be `rumored`; a claim that it is **already being served in
production** is `in-testing`. But nothing pins it down: no Anthropic post,
no model card, no API identifier, no pricing, and — notably — nobody
posting a firsthand output that distinguishes it from Fable 5. Two
independent secondary sources is `partial`, not `confirmed`.

**Version number is unsettled.** @kimmonismus's own relay hedges between
**5.1 and 5.5**. Per slug convention the slug is immutable regardless of
what it is eventually called; if it ships as 5.5 (or under a different
name entirely) the title updates and the slug stays.

**Ambient context, not evidence.** Anthropic is running hot: @ClaudeDevs
extended the 50% weekly Claude Code limit increase through Aug 31 while
warning that "strong demand for our models means that capacity may be
tight," and the status page showed degraded performance across the whole
model line on 2026-08-18. A capacity squeeze is consistent with serving a
new model to a slice of traffic, and equally consistent with just being
busy. It is not corroboration.

**Transition triggers:**
- Anthropic announcement, model card or API id → UPDATE, advance to
  `confirmed`/`released`, `verification: confirmed`.
- Firsthand user output that distinguishes it from Fable 5 → UPDATE,
  advance `verification` to `partial`→`confirmed` as evidence allows.
- The stealth flight is disproved, or ≥15 cycles pass with no
  corroboration → `closed: stale-rumor-unverified`.

**Dedup note:** Fable 5 itself stays closed on [[claude-fable-5]]; the
export-control action that pulled it stays on
[[anthropic-fable-mythos-export-control-2026-06]]. Mythos-line successors
stay on [[mythos-public-release]]. Further Fable 5.1 leak, launch or
pricing signal UPDATES this ticket.
