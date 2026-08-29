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

  **2026-08-26/27 — the rollout widened and, for the first time, there is
  a REPRODUCIBLE TEST.** The gap this ticket named on 2026-08-19 was
  "nobody posting a firsthand output that distinguishes it from Fable 5."
  That gap is now partly closed. **@legit_api** published an actual probe:
  "Claude Fable 5 **is now routing to Fable 5.1** on claude web for some
  users. To check if you have access, you can test this prompt: *opus 4.6
  date of release and gpt image 1.5 without searching the web*" — i.e. a
  **knowledge-cutoff discriminator** anyone can run. @testingcatalog
  relayed it with the observation that "**more users are now routed** to
  Claude Fable 5.1 from Claude Fable 5 in the background… Some users have
  spotted that **knowledge cutoff of the Fable 5 model got updated**,
  pointing to a stealth rollout."

  A model answering post-Fable-5 questions under the "Fable 5" label is
  a *distinguishing behavioural output*, not a leaker assertion — which
  is what separates this cycle from the last. It is still not an
  Anthropic statement, a model card, an API id, or pricing.

  **Timing claims firmed to "today," and then did not land in-window.**
  @synthwavedd: "Preparations are ramping up for a launch **as soon as
  tomorrow** — and if they don't want to risk being embarrassed, they'll
  need it out latest early next week." @kimmonismus, 2026-08-27 09:25 UTC:
  "Per @synthwavedd, **today is release day**." As of this run's
  17:43 UTC cutoff **no Anthropic announcement exists**, so the prediction
  is recorded as unfulfilled rather than as evidence.

  **Scope may be wider than this ticket's title — recorded, NOT adopted.**
  @kimmonismus expects "Fable 5.1 **and Opus 5.1 / Sonnet 5.1**," and it
  trended as "Anthropic's Claude 5.1 **Models** Spark Release Buzz" (~142
  posts) alongside "Anthropic Quietly Rolls Out Claude Fable 5.1 Update"
  (~1.8K posts). @vepsi__ frames the Opus 5.1 leg honestly as "**NOT
  CONFIRMED YET**." No Opus/Sonnet 5.1 ticket is created on that basis:
  the entire Opus/Sonnet leg traces to one leaker chain with no probe, no
  artifact and no routing observation, which is below the bar that got
  Fable 5.1 its own ticket. If a 5.1 wave ships, siblings get their own
  tickets then.

  Verification stays `partial`. The routing probe is a real advance, but
  it is one leak account's test relayed by one aggregator, and neither
  posted the *output* they got. `confirmed` needs Anthropic.
expected: "As of 2026-08-27 17:43 UTC: still unannounced. Rollout reportedly widened — @legit_api reports Fable 5 routing to Fable 5.1 on claude web for a subset of users and published a knowledge-cutoff probe prompt to test for it; @testingcatalog reports more users routed and an updated Fable 5 knowledge cutoff. Leakers called 2026-08-27 release day and it did not land in-window. Pending: an Anthropic announcement, model card, API id and pricing; someone posting the actual probe output; and whether the rumoured Opus 5.1 / Sonnet 5.1 siblings are real (currently single-chain, unconfirmed)"
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
  - "@legit_api"
  - "@testingcatalog"
  - https://x.com/testingcatalog/status/2092645689951981758
  - "@mark_k"
created_at: 2026-08-19
updated_at: 2026-08-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — @synthwavedd (2026-08-18) reports a Fable 5 successor, likely Fable 5.1, being served to a subset of accounts with Fable 5 selected; amplified by @kimmonismus (who vouches for the leaker and reads a launch as very close) and independently echoed by @AndrewCurran_, who says Fable 5.1 has been ready to ship for weeks and that a small stealth test flight before launch is normal for both OpenAI and Anthropic. Trending as its own AI news item (~956 posts). Status in-testing — the claim is a real artifact served in production, not a tease. Verification partial: two independent secondary accounts, no Anthropic statement, model card, API id or firsthand distinguishing output. Successor to the closed [[claude-fable-5]]."
  - ts: 2026-08-27
    change: "The rollout widened and the ticket's own named evidence gap partly closed — but it still has not shipped. This ticket noted on 2026-08-19 that nobody had posted a firsthand output distinguishing 5.1 from Fable 5; @legit_api (2026-08-26) published a reproducible probe instead: 'Claude Fable 5 is now routing to Fable 5.1 on claude web for some users. To check if you have access, you can test this prompt: opus 4.6 date of release and gpt image 1.5 without searching the web' — a knowledge-cutoff discriminator anyone can run. @testingcatalog relayed it and reported that more users are now routed in the background and that the Fable 5 knowledge cutoff itself got updated, which is a behavioural fingerprint rather than a leaker assertion. @mark_k: 'Fable 5.1 coming soon from @AnthropicAI'. It trended twice — 'Anthropic Quietly Rolls Out Claude Fable 5.1 Update' (~1.8K posts) and 'Anthropic's Claude 5.1 Models Spark Release Buzz' (~142 posts). Timing claims firmed and then failed in-window: @synthwavedd said launch 'as soon as tomorrow', @kimmonismus said on 2026-08-27 09:25 UTC that 'today is release day', and as of this run's 17:43 UTC cutoff there is no Anthropic announcement — recorded as an unfulfilled prediction, not as evidence. Scope creep recorded but deliberately not adopted: @kimmonismus expects Opus 5.1 / Sonnet 5.1 alongside Fable 5.1 and @vepsi__ labels the Opus leg 'NOT CONFIRMED YET'; that entire leg traces to one leaker chain with no probe, no artifact and no routing observation, so no sibling ticket is created — if a 5.1 wave ships, siblings get their own tickets then. Status stays in-testing; verification stays partial, because the probe is one leak account's test relayed by one aggregator and neither posted the output they actually got. confirmed needs Anthropic."
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
