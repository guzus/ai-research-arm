---
slug: xai-grok-voice-2-2026-08
title: Grok Voice Think Fast 2.0 tops the Artificial Analysis speech-to-speech index, deployed at Starlink scale
company: SpaceX / xAI
model: Grok Voice Think Fast 2.0
status: released
status_note: |
  **Two first-party claims from @SpaceXAI on 2026-08-24, both amplified by
  @elonmusk:**

  *Benchmark:* "**Grok Voice Think Fast 2.0 is now #1 on the Artificial
  Analysis Speech-to-Speech Index.** This index measures whether voice
  agents can **reason over the speech it hears, resolve real customer
  issues, and correctly complete tasks using agent tools**." (Elon:
  "Grok Voice 2 is great," ~4.3K likes.)

  *Production deployment:* "At **Starlink**, we're using Grok Voice to
  resolve over **15,000 inbound customer support and sales calls a day**.
  Grok **diagnoses hardware issues, ships replacements, and fulfills over
  3,000 orders a week** across voice calls and chat." (Elon: "Grok Voice
  is used by Starlink at scale for support & sales," ~7.4K likes.)

  Status `released` — a named, versioned model running a production
  workload at disclosed volume. Verification `partial`: **every figure is
  vendor-supplied.** The Artificial Analysis index page was not captured,
  no pricing or API availability was stated, and the deployment numbers
  come from the operator describing its own sister company's product. The
  15,000 calls/day and 3,000 orders/week figures have no independent
  check.

  **The deployment claim is the more interesting one, and the softer.**
  "Resolve" is doing heavy lifting: a call the agent handles end-to-end
  and a call it triages before escalating are both plausibly counted, and
  nothing in the post distinguishes them. Order fulfilment is the harder
  claim — 3,000/week is an action taken in a billing system, not a
  conversation — and is the number that would matter if independently
  confirmed.

  **The benchmark claim is narrow by construction.** The index measures
  *task completion with tools*, not audio naturalness or latency. A #1 on
  it says the model is a good agent that happens to speak, which is
  consistent with the Starlink use case and says little about consumer
  voice quality.
expected: "Announced 2026-08-24 as #1 on the Artificial Analysis Speech-to-Speech Index and in production at Starlink handling 15,000+ calls/day and 3,000+ orders/week. Pending: the Artificial Analysis index page and where competitors land, API availability and pricing for Grok Voice 2 outside SpaceX properties, latency figures, and any independent measurement of the resolution rate behind 'resolve'"
labels:
  - xai
  - spacex
  - grok
  - voice
  - agents
  - released
verification: partial
sources:
  - "@elonmusk"
  - "@mark_k"
created_at: 2026-08-25
updated_at: 2026-08-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-25
    change: "Created — @SpaceXAI announced (2026-08-24, both amplified by @elonmusk) that Grok Voice Think Fast 2.0 is #1 on the Artificial Analysis Speech-to-Speech Index, an index measuring reasoning over heard speech, resolving real customer issues and completing tasks with agent tools; and separately that Starlink uses Grok Voice to resolve 15,000+ inbound support and sales calls a day, diagnosing hardware issues, shipping replacements and fulfilling 3,000+ orders a week across voice and chat. Status released — a named versioned model on a production workload at disclosed volume. Verification partial — all figures are vendor-supplied, the index page was not captured, 'resolve' is undefined between full handling and triage, and no pricing or external API availability was stated. Same-day @mark_k reports new Grok Imagine image-editing tools (colour-palette presets, in-app crop) from @SpaceXAI, recorded here as adjacent product motion rather than a separate ticket."
---

xAI/SpaceX say **Grok Voice Think Fast 2.0** leads the Artificial Analysis
speech-to-speech index and is already running Starlink's support line at
**15,000+ calls a day**.

**The production number is the story, not the leaderboard.** Voice-agent
benchmarks turn over constantly; a single company routing its own
high-volume, high-consequence support queue through its own model is a
durable claim about reliability. Starlink support is unusually good
evidence precisely because it is not a demo: hardware diagnosis has a
ground truth, and shipping a replacement costs real money when the model
is wrong.

**It is also entirely self-reported.** SpaceX is describing SpaceX's
deployment of xAI's model, with Elon Musk amplifying both. There is no
independent measurement, no definition of "resolve," and no error or
escalation rate. The 3,000 orders/week figure is the one to press on: it
is the only claim describing an irreversible action in a transactional
system, so it is the hardest to inflate and the most meaningful if true.

**Where this fits xAI's shape.** The lane pattern is consistent — Grok
sold as a *harness that does things* rather than a chat model. Grok Bot
([[xai-grok-bot-2026-08]]) was the same argument in consumer form this
month, drawing a stream of firsthand user reports of task completion
(transcribing podcast archives, building shopping carts, cancelling
services). Grok Voice 2 is the enterprise-facing version of the same bet,
now with an internal customer big enough to prove it at volume.

**Adjacent motion recorded here rather than split off:** @mark_k
(2026-08-24 16:47 UTC) reports Grok Imagine gained image-editing tools —
colour-palette presets including palettes extracted from the source image,
plus in-app cropping — which he reads as Imagine turning into a full image
editor. That is a feature update to a shipped product
([[xai-grok-imagine-video-1-5-2026-06]]), not a new artifact.

Related: [[xai-grok-bot-2026-08]],
[[spacex-nvidia-starmind-orbital-compute-2026-08]],
[[xai-grok-2t-spacex-data-2026-07]].
