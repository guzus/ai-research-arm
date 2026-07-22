---
slug: anthropic-opus-5-leak-2026-07
title: Claude Opus 5 — single-source leak claims imminent launch
company: Anthropic
model: Claude Opus 5
status: rumored
status_note: |
  A single low-follower account (@Mr_Salio) claims **"Claude Opus 5"**
  launch is imminent — "this week or next" with Thursday floated as the
  current target — citing an alleged brief appearance in Cursor before
  disappearing, a rumored **3M-token context window**, and claims of major
  coding/reasoning/agentic improvements. The same post also claims
  Anthropic is separately prepping a next-generation Fable successor for
  August to compete with GPT-6 — a claim that would need its own
  corroboration if it resurfaces. No other account, Anthropic channel, or
  independent leak corroborates any of this in the current window; treat
  as an unconfirmed single-source tease.
expected: "Claimed 'this week or next' (Thursday floated) per a single unverified source; no corroboration"
labels:
  - anthropic
  - unreleased
  - rumored
verification: unverified
sources:
  - "@Mr_Salio"
created_at: 2026-07-22
updated_at: 2026-07-22
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-22
    change: "Created — single low-follower account (@Mr_Salio) claims Claude Opus 5 launch is imminent (Thursday floated), briefly appeared in Cursor before disappearing, rumored 3M-token context. No corroboration from other accounts or Anthropic → status rumored, verification unverified."
---

A single account, **@Mr_Salio**, posted a "leak" claiming Anthropic's next
Opus-line model — **Claude Opus 5** — is due to launch imminently ("this
week or next," Thursday floated as the target), citing:

- A brief, since-vanished appearance in Cursor's model picker.
- A rumored **3M-token context window**.
- Claimed major improvements in coding, reasoning, and agentic workflows.
- A separate claim that Anthropic is preparing a next-generation Fable
  successor for August, positioned to compete with GPT-6.

**Why filed as rumored/unverified.** This is a single, low-credibility
account with no independent corroboration in the current signal window —
no other leaker, no Anthropic-adjacent account, and no official Anthropic
channel references "Opus 5" or a matching timeline. It is filed now
precisely so the claim isn't lost if it resurfaces or gets corroborated
later, per the ticket system's standard practice for early single-source
leaks.

**Transition triggers:**
- A second independent account, an official Anthropic tease, or a
  console/API artifact → UPDATE, advance `status` toward `in-testing`.
- If no fresh corroboration appears within ~15 daily cycles → close with
  `closed_reason: stale-rumor-unverified`.

**Dedup note:** further Claude Opus 5 signal UPDATES this ticket. The
separately-claimed "next-gen Fable successor for August" should get its
own ticket if and when it gets independent corroboration — it is not the
same artifact as Opus 5.
