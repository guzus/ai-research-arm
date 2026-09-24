---
slug: google-gemini-4-2026-09
title: Gemini 4 — pre-training reportedly finishing, release targeted well before year-end
company: Google / DeepMind
model: Gemini 4
status: in-testing
status_note: |
  Successor to [[gemini-4-2026-07]], which was closed 2026-08-19 as
  `stale-rumor-unverified` with the explicit note that "a named artifact or a
  DeepMind statement opens a successor ticket." That condition is now met on the
  second half: the claim is attributed to a named DeepMind principal rather than
  to an anonymous relay.

  @kimmonismus, 2026-09-24 02:33 UTC, citing The Information: "Gemini 4 almost
  finished training, release 'hopefully much earlier than end of year'."
  @testingcatalog's 2026-09-24 brief attributes it: "Koray says Gemini 4 is in
  early post-training and hopes for an early drop well before year-end."

  Two details separate this from the July rumour. First, a **named executive**
  (Koray Kavukcuoglu, DeepMind CTO) rather than an unattributed quote. Second,
  a **stage claim** — pre-training finished, early post-training underway — which
  is falsifiable and is the shape of a real artifact rather than a roadmap tease.

  Still absent: no Google or DeepMind post in this cycle's signal, no date, no
  specs, no model card, no benchmark. The quote reaches us via an outlet and two
  relay accounts. Status `in-testing` on the post-training claim; verification
  `partial` — attributed and specific, but not primary.

  Read "hopefully much earlier than end of year" as an aspiration from someone
  who would know, not a schedule. The predecessor ticket exists precisely because
  Gemini-4 timing claims have not survived contact before.
expected: "Reported target: release well before end of 2026. No date, spec or model card. In early post-training as of 2026-09-24."
labels:
  - google
  - deepmind
  - frontier-model
  - unreleased
verification: partial
sources:
  - https://x.com/kimmonismus/status/2102949590542741983
  - https://x.com/testingcatalog/status/2103015463089238076
created_at: 2026-09-24
updated_at: 2026-09-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — IN-TESTING. Successor to [[gemini-4-2026-07]], closed 2026-08-19 as stale-rumor-unverified with the standing condition that a named artifact or a DeepMind statement would open a successor. Condition met: @kimmonismus (2026-09-24, citing The Information) reports Gemini 4 has almost finished training with release 'hopefully much earlier than end of year', and @testingcatalog's same-day brief attributes the statement to Koray (Kavukcuoglu, DeepMind CTO) with the more specific claim that Gemini 4 is in early post-training. Opened at in-testing rather than rumored because the claim is a falsifiable training-stage assertion from a named principal, not an anonymous roadmap tease; verification partial because it still arrives via an outlet and two relay accounts with no Google or DeepMind post, no date, no specs and no model card in this cycle's signal. The predecessor's central failure — a timing claim that never resolved — is the specific risk being carried forward, so the 'well before year-end' target is recorded as an aspiration to hold accountable, not a schedule."
---

The July ticket died of exactly one thing: nobody in a position to know would
put their name to it. That has changed. The claim now has an attributed speaker
(DeepMind's CTO), a training stage (pre-training complete, early post-training),
and a rough window (well before end of 2026). Any of those three can be checked
against reality later, which is the difference between a ticket worth keeping
open and the one that was closed.

What has *not* changed is the sourcing path. This is an outlet report relayed by
two aggregator accounts; Google has posted nothing. The ticket set has been
burned before by treating a plausible relay as a company statement, and the
predecessor is the local proof. So: `in-testing` on the artifact,
`partial` on the verification, and the timing quote logged as an aspiration.

Context that makes the timing claim credible rather than merely convenient.
Google has shipped an unusually dense 3.8 line in September alone — Flash and
Flash Cyber ([[gemini-3-8-flash-2026-09]]), Live and Live Extended Thinking
([[google-gemini-3-8-live-2026-09]]), and now Flash TTS and Flash-Lite TTS
([[google-gemini-3-8-flash-tts-2026-09]]). A cadence that fast on the point
releases is consistent with a generation boundary approaching, because the 3.x
line is being harvested rather than extended.

The competitive frame is the one the July ticket named and it still holds: GPT-6
Astra shipped and Sol/Luna followed ([[openai-gpt-6]]), Anthropic opened a 5.5
family ([[anthropic-opus-5-5-2026-09]]). Google is the remaining lab of the
three without a new-generation flagship out. Also still open from the
predecessor: whether [[gemini-3-5-pro]] ever gets a full public release or is
simply overtaken.
