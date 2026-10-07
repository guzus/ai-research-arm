---
slug: openai-decisions-api-2026-09
title: OpenAI Decisions API — GPT-6 Luna-backed choice endpoint in limited preview
company: OpenAI
model: GPT-6 Luna
status: released
status_note: |
  **~2026-10-07 — public beta (secondary relay of OpenAI's Tibo).** Decisions
  API opened to developers in public beta: GPT-6 Luna, up to ~10x faster than the
  Responses API for selection tasks, text+image in, outputs as true/false
  probability, a choice, or a numeric score; $0.10 per 1M input tokens, no output
  charge. Original DevDay record below is retained.

  **Announced at DevDay, 2026-09-29, and it is a preview rather than a GA
  product.** The most precise account is @masahirochaen's, ranking it #5 of 25
  announcements: the Decisions API runs on **GPT-6 Luna**, is purpose-built for
  *choosing*, returns **one option from a predefined set in a few hundred
  milliseconds**, accepts **text and image** input, and is aimed at ticket
  routing, classification and an agent's next-action selection. He states it is in
  **limited preview for a subset of customers, with expansion expected within
  days**. @insanekrishnaa describes the same product as "built for situations
  where an AI needs to choose between predefined actions."

  **Why a separate endpoint is the interesting part.** Every one of these tasks is
  already doable with a chat completion. What a dedicated endpoint buys is a
  *shape guarantee* — the response is one of N known options rather than text that
  has to be parsed and validated — plus a latency budget small enough to sit in a
  request path. That makes it infrastructure for agent control flow, not a model
  release, which is why several recaps called it the underrated announcement
  despite ranking it low on attention.

  **Named as a competitive response.** @MagicPower21M calls it a "Jev competitor,
  with vision support, millisecond-scale routing/multiple-choice"; @davidarngar's
  skeptical recap lists it as a "Jev clone". Jev is tracked at
  [[typesafe-jev-2026-09]]. @mickcodez, a DevDay attendee, is firsthand and
  positive: "Really excited about the coming decision model too."

  **First dedicated product surface for the cheap tier.** GPT-6 Luna shipped on
  2026-09-22 as the cheapest member of the GPT-6 family
  ([[openai-gpt-6]]); this is the first product built specifically around it
  rather than around Astra. Note the inconsistency in signal: one recap attributes
  the endpoint to Luna, others do not name a model — the Luna attribution comes
  from the single most detailed recap and is recorded as such, not as confirmed.
expected: "PUBLIC BETA for developers since ~2026-10-07 (Day 2 of OpenAI's 28-day improvements series). Pricing reported at $0.10 per 1M input tokens, no output charge. Open: GA, a first-party docs/pricing page, measured latency, maximum options per call."
labels:
  - openai
  - api
  - devday-2026
  - agents
  - routing
verification: partial
sources:
  - https://x.com/masahirochaen/status/2105148217650475496
  - https://x.com/masahirochaen/status/2105147966889886057
  - https://x.com/insanekrishnaa/status/2105147666850304017
  - https://x.com/MagicPower21M/status/2105148814105710821
  - https://x.com/mickcodez/status/2105147895351771644
  - https://x.com/davidarngar/status/2105149492357976295
  - https://x.com/AI_Levela/status/2107828005687181382
created_at: 2026-09-30
updated_at: 2026-10-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-30
    change: "Created — CONFIRMED / partial. OpenAI announced the Decisions API at DevDay on 2026-09-29. Per @masahirochaen's item #5 of 25, the most detailed account in signal: it runs on GPT-6 Luna, is specialised for selecting one option from a predefined set, returns in a few hundred milliseconds, takes text and image input, targets inquiry routing, classification and agent next-action selection, and is in limited preview for a subset of customers with expansion expected within days. @insanekrishnaa and @MagicPower21M describe the same product independently; @mickcodez attended DevDay and refers to 'the coming decision model', which supports the preview-not-GA reading. Status CONFIRMED (announced, multi-source) rather than released, because every account describes a gated preview rather than general availability. Verification partial: no OpenAI post in this cycle's fetch, no pricing, and the GPT-6 Luna attribution rests on one recap while others name no model — recorded as reported, not established. Treated as its own ticket rather than folded into the DevDay agent products because it is an API primitive for control flow, not an agent or a model: the value is a guaranteed response shape plus a latency budget small enough for a request path, both of which are infrastructure properties. Positioned by two independent recaps as a competitor to Jev ([[typesafe-jev-2026-09]]), one of them dismissively ('Jev clone'). It is also the first dedicated product surface for GPT-6 Luna, the cheap tier that shipped 2026-09-22 ([[openai-gpt-6]]), which is consistent with that ticket's recorded fast/cheap-tier inference. Several recaps flagged it as the most underrated item of the event despite ranking it low on measured attention — recorded as a judgement, not a measurement."
  - ts: 2026-10-07
    change: "CONFIRMED -> RELEASED (public beta for developers). Per a Japanese recap of OpenAI's Tibo (@thsottiaux) 'Day 2 of 28 days of improvements' post (@AI_Levela, 2026-10-07 13:38 UTC): the Decisions API is now in public beta for developers; it runs on GPT-6 Luna (the attribution this ticket held as single-source is now repeated), is up to ~10x faster than the standard Responses API for choosing models, tools or next actions, takes text and image input, returns three output kinds (true/false probability, a choice, a numeric score), and costs $0.10 per 1M input tokens with no output-token charge. OpenAI says it uses it internally to improve app experiences. Verification stays partial — secondary relay, no first-party post in this fetch."
---

This is the smallest announcement of DevDay and the one most likely to end up
inside other people's production systems.

Everything the Decisions API does is already possible with a chat completion and a
parser. What it removes is the parser — and the class of bug where a model returns
prose instead of one of your four enum values, or returns a fifth value it
invented. If the endpoint genuinely constrains output to the supplied option set,
then a whole category of defensive scaffolding in agent harnesses becomes
unnecessary, and the latency claim puts it inside request paths where a
chat-completion round trip was too slow to consider.

The vision input is the detail that suggests real thought rather than
repackaging. Routing on text is a solved-enough problem; routing on a screenshot
— which button, which region, which of these four states is this UI in — is the
primitive a computer-use agent needs on every step. An endpoint that answers that
in a few hundred milliseconds is what makes a long agent trajectory affordable,
because most steps in such a trajectory are selections, not generations.

Which is also the honest limit of the current record: the latency and
constrained-output claims are the entire value proposition, and both are vendor
descriptions relayed through a recap. Neither has been measured by anyone outside
the preview. Nor is there any pricing, which matters more here than usual — an
endpoint designed to be called on every agent step has a cost profile that is
multiplied by trajectory length, and a per-call price that looks trivial in
isolation is the dominant line item at ten thousand steps.

Worth watching for a second reason. If this endpoint is where agent control flow
ends up living, the model behind it becomes the arbiter of what every agent does
next — a lot of consequential routing on the cheapest model in the family.
