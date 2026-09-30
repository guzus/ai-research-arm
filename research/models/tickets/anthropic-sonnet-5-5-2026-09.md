---
slug: anthropic-sonnet-5-5-2026-09
title: "Claude Sonnet 5.5 — shipped; list price $2/$10 per MTok matches the leak exactly"
company: Anthropic
model: Claude Sonnet 5.5 (reported)
status: released
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
expected: "RELEASED and being resold with published list pricing of $2 input / $10 output per MTok — the exact figure the 2026-09-24 leak gave, which is this ticket's falsifier resolving in the source's favour. Still open: an Anthropic announcement post, model card, official API id and benchmark set (none appeared in this cycle's fetch), plus whether the 1M context / 128K max output half of the leak also holds."
labels:
  - anthropic
  - frontier-model
  - rumored
  - claude-5-5-family
verification: partial
sources:
  - https://x.com/kimmonismus/status/2102972781495566455
  - https://x.com/arankomatsuzaki/status/2102445494735982603
  - https://x.com/testingcatalog/status/2104493424472674634
  - https://x.com/kimmonismus/status/2104547347287900337
  - https://x.com/RouteMux/status/2105149087846924753
  - https://x.com/azattelevision/status/2105149010654752976
created_at: 2026-09-24
updated_at: 2026-09-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — RUMORED. @kimmonismus reported on 2026-09-24 04:05 UTC that Claude Sonnet 5.5 is already being stealth tested, with a 1M-token context window, 128K max output, and pricing of $2 input / $10 output per MTok, reading it as a direct response to GPT-6 Sol. Against it: single relay source, no Anthropic post, no model card, no API id, no benchmark, no independent corroboration in this cycle's signal — status rumored, verification unverified. For it: Anthropic's own Opus 5.5 launch (2026-09-22) described it as \"the first model in our new Claude 5.5 family\" ([[anthropic-opus-5-5-2026-09]]), so a Sonnet 5.5 is a named slot in a family Anthropic has publicly opened rather than an invented model, and the quoted 1M/128K shape matches Fable 5.1's reported specs. The $2/$10 figure is flagged as the weakest element: it lands exactly on GPT-6 Sol's price point, which is equally consistent with observation and with inference. Close trigger set: if no corroboration appears within ~15 cycles, close as stale-rumor-unverified."
  - ts: 2026-09-28
    change: "Lifecycle advanced on a MODEL-ID ARTIFACT, not on a better rumour. @testingcatalog's 2026-09-28 daily brief reports under Anthropic: 'claude-sonnet-5-5 tag reportedly spotted. Nothing official, pricing unknown.' A model tag is the same evidence class this set treats as in-testing elsewhere (a registry/console string is an artifact, a tease is not), so status rumored -> in-testing. Verification unverified -> partial: two independent secondary accounts now carry it rather than one relay. Second, separable datapoint: @kimmonismus (12:22 UTC) 'Looks like Sonnet-5.5 could be released today!', citing @lyraxana's dated call of '<= 2026-09-28 11:00 PT' and vouching for that leaker's reliability. Recorded as a dated prediction so it can be scored, NOT as evidence — this ticket's own 2026-09-24 entry warns that specific numbers from relay accounts have been wrong on this set before, and the $2/$10 pricing claim is still uncorroborated. What is still absent: any Anthropic post, model card, API id, benchmark, or firsthand output. Note also a low-quality aggregator (@apimasteratai) listing Sonnet 5.5 alongside 'Claude Haiku 5.5' for October; the Haiku leg has no artifact and gets no ticket, though @theo's observation that the last Haiku release is nearly a year old is the reason it keeps being guessed."
  - ts: 2026-09-30
    change: "SHIPPED, AND THE LEAK'S RISKIEST NUMBER WAS RIGHT. Two independent secondary sources now treat Sonnet 5.5 as a live, purchasable model. (1) @RouteMux (2026-09-30 04:13 UTC), a reseller publishing its own discount sheet, lists 'Claude Sonnet 5.5 and Opus 5.5 at 72% off' alongside GPT-6.1 Sol and prints the LIST prices it is discounting from: Sonnet 5.5 $2 / $10 per 1M tokens in/out, Opus 5.5 $4 / $20. A reseller quoting list price is a commercial artifact rather than a rumour — it cannot discount a model it cannot serve. (2) @azattelevision reports Sonnet 5.5 as released and 'nearing the performance levels of the flagship Opus while cutting costs in half'. Status in-testing -> released. THE FALSIFIER THIS TICKET SET ON 2026-09-24 HAS RESOLVED IN THE SOURCE'S FAVOUR: the body stated that if the model shipped at materially different numbers the $2/$10 claim was pattern-matching off GPT-6 Sol's slot, and if it shipped at those exact numbers 'the source had something'. It shipped at exactly $2/$10. That is a real update on @kimmonismus's access for this class of claim and is recorded rather than quietly dropped. Verification stays PARTIAL deliberately: no Anthropic announcement post, model card, official API id or benchmark appears anywhere in this cycle's fetch, so availability is attested by third parties selling it rather than by the vendor shipping it on the record. The context/output half of the leak (1M / 128K) is still uncorroborated, and the 2026-09-28 leaker date of on-or-before 11:00 PT that day cannot be scored from this signal — only that it is live by 2026-09-30. Competitive frame: it lands the same week OpenAI shipped GPT-6.1 Sol at the identical $2/$10 ([[openai-gpt-6-1-sol-2026-09]]) and raised its top consumer tier to $500 ([[openai-chatgpt-pro-max-2026-09]]) — the two labs are now priced identically at the mid tier and diverging sharply at the top."
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
