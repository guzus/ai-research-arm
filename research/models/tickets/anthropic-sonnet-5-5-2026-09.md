---
slug: anthropic-sonnet-5-5-2026-09
title: Claude Sonnet 5.5 — reported stealth testing at 1M context, $2/$10 per MTok
company: Anthropic
model: Claude Sonnet 5.5 (reported)
status: rumored
status_note: |
  Single relay source. @kimmonismus, 2026-09-24 04:05 UTC: "Here we go: Sonnet
  5.5 already being stealth tested. The model has a 1M-token context window and
  a 128K-token maximum output. Pricing per 1M tokens: $2 input, $10 output."
  He reads it as a direct answer to GPT-6 Sol on price.

  **No Anthropic statement, no model card, no API id, no benchmark, and no
  independent corroboration in this cycle's signal.** That is the same shape
  that has been wrong before on this ticket set, so status is `rumored` and
  verification `unverified` despite the specificity of the numbers.

  What makes it more than a bare tease, and the reason it gets a ticket rather
  than a footnote: Anthropic itself opened a *family*. The Opus 5.5 launch post
  called it "the first model in our new Claude 5.5 family"
  ([[anthropic-opus-5-5-2026-09]]), which means a Sonnet 5.5 is the expected
  second entry rather than an invented name. The quoted specs also match the
  shape Anthropic has been shipping — Fable 5.1 reportedly runs 1M context /
  128K max output ([[anthropic-claude-fable-5-1-2026-08]]).

  Treat the $2/$10 figure as the least reliable part. It is exactly GPT-6 Sol's
  competitive slot, which makes it both plausible and the sort of number a
  relay account would infer rather than observe.
expected: "TBD — no Anthropic statement. Family precedent (Opus 5.5 shipped 2026-09-22 as the family opener) suggests weeks, not months, but nothing in signal dates it."
labels:
  - anthropic
  - frontier-model
  - rumored
  - claude-5-5-family
verification: unverified
sources:
  - https://x.com/kimmonismus/status/2102972781495566455
  - https://x.com/arankomatsuzaki/status/2102445494735982603
created_at: 2026-09-24
updated_at: 2026-09-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — RUMORED. @kimmonismus reported on 2026-09-24 04:05 UTC that Claude Sonnet 5.5 is already being stealth tested, with a 1M-token context window, 128K max output, and pricing of $2 input / $10 output per MTok, reading it as a direct response to GPT-6 Sol. Against it: single relay source, no Anthropic post, no model card, no API id, no benchmark, no independent corroboration in this cycle's signal — status rumored, verification unverified. For it: Anthropic's own Opus 5.5 launch (2026-09-22) described it as \"the first model in our new Claude 5.5 family\" ([[anthropic-opus-5-5-2026-09]]), so a Sonnet 5.5 is a named slot in a family Anthropic has publicly opened rather than an invented model, and the quoted 1M/128K shape matches Fable 5.1's reported specs. The $2/$10 figure is flagged as the weakest element: it lands exactly on GPT-6 Sol's price point, which is equally consistent with observation and with inference. Close trigger set: if no corroboration appears within ~15 cycles, close as stale-rumor-unverified."
---

This ticket exists to hold a specific prediction accountable, not to assert that
Sonnet 5.5 is real. One relay account, no company signal, precise numbers — the
combination that has produced both good early calls and confident nonsense on
this set before.

The asymmetry worth recording: the *existence* of a Sonnet 5.5 is now much
better supported than it would have been a week ago, because Anthropic itself
named a "Claude 5.5 family" when it shipped Opus 5.5 on 2026-09-22
([[anthropic-opus-5-5-2026-09]]). Families get filled in. What is not supported
is the spec sheet. A 1M context and 128K max output would match Fable 5.1, which
is a reasonable inference from public information rather than evidence of
insider access; $2/$10 is precisely GPT-6 Sol's slot, which is what a
competitive-response narrative would predict whether or not anyone saw a price
card.

So the falsifiable content is: if Sonnet 5.5 ships and the context/output/price
triple is materially different, this was pattern-matching. If it ships at those
exact numbers, the source had something.

Distinct from [[claude-sonnet-5]] (Sonnet 5, closed — the prior generation) and
from [[anthropic-claude-fable-5-1-2026-08]]. Also note @iruletheworldmo's
separate unverified claim the same day that "fable 5.5 is trained and coming
soon" — different artifact, same weak sourcing, not tracked here.
