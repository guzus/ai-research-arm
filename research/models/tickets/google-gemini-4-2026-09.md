---
slug: google-gemini-4-2026-09
title: Gemini 4 — pre-training reportedly finishing, release targeted well before year-end
company: Google / DeepMind
model: Gemini 4
status: in-testing
status_note: |
  **2026-09-24 — the lifecycle stage moved, on the record, at a public
  event.** At The Information's AI Agenda Live in San Francisco, DeepMind chief
  **Koray Kavukcuoglu** said Gemini 4 is in **post-training / refinement**, could
  arrive **"well before year-end"**, and — the new detail — that the team is
  excited enough by the results to **release an early version and keep improving
  it quickly** (@theinformation 2026-09-24 14:30 UTC; @mark_k relay 14:14 UTC:
  "in its refinement stage, with a release planned 'much earlier' than the end of
  the year").

  That is a named executive at a named participant speaking at a public
  conference, which is a stronger source than the previous entry's relay, and it
  advances the reported stage from "pre-training finishing / early post-training"
  to "refinement, with a staged early release planned".

  **Status stays `in-testing` deliberately.** There is still no date, no model
  card, no benchmark, no spec and no access path. "Excited enough to ship early"
  is a disposition, not an artifact.

  **Second Kavukcuoglu datapoint from the same session, tracked as context.**
  He also said DeepMind now trusts AI agents to autonomously run parts of the
  model-training process — running experiments, analysing results, proposing
  hypotheses, under human supervision — and that this was not the case six months
  ago (@theinformation, 2026-09-24 20:31 UTC). Relevant to how Gemini 4 is being
  built, not evidence about Gemini 4 itself.

  **Competitive framing.** Google has gone roughly a year without a new flagship
  while shipping the 3.8 line continuously, and Gemini 4 now lands into a market
  where GPT-6 Astra and Opus 5.5 are both out and benchmarked against each other.

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
expected: "Reported target: release well before end of 2026, with DeepMind's Koray Kavukcuoglu saying on 2026-09-24 that the model is in post-training/refinement and that Google intends to ship an early version and improve it quickly. Still no date, spec, model card or benchmark."
labels:
  - google
  - deepmind
  - frontier-model
  - unreleased
verification: partial
sources:
  - https://x.com/kimmonismus/status/2102949590542741983
  - https://x.com/testingcatalog/status/2103015463089238076
  - https://x.com/theinformation/status/2103129866375659543
  - https://x.com/mark_k/status/2103125879903629571
  - https://x.com/theinformation/status/2103220914347188282
created_at: 2026-09-24
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — IN-TESTING. Successor to [[gemini-4-2026-07]], closed 2026-08-19 as stale-rumor-unverified with the standing condition that a named artifact or a DeepMind statement would open a successor. Condition met: @kimmonismus (2026-09-24, citing The Information) reports Gemini 4 has almost finished training with release 'hopefully much earlier than end of year', and @testingcatalog's same-day brief attributes the statement to Koray (Kavukcuoglu, DeepMind CTO) with the more specific claim that Gemini 4 is in early post-training. Opened at in-testing rather than rumored because the claim is a falsifiable training-stage assertion from a named principal, not an anonymous roadmap tease; verification partial because it still arrives via an outlet and two relay accounts with no Google or DeepMind post, no date, no specs and no model card in this cycle's signal. The predecessor's central failure — a timing claim that never resolved — is the specific risk being carried forward, so the 'well before year-end' target is recorded as an aspiration to hold accountable, not a schedule."
  - ts: 2026-09-25
    change: "Stage advanced within in-testing; status unchanged. DeepMind chief Koray Kavukcuoglu, speaking at The Information's AI Agenda Live on 2026-09-24, said Gemini 4 is in post-training / refinement and could arrive 'well before year-end', adding the new detail that the team is excited enough by the results to release an EARLY VERSION and keep improving it quickly (@theinformation 14:30 UTC; @mark_k relay 14:14 UTC, ~509 likes, quoting 'much earlier' than end of year). This is a stronger source class than the previous entry's relay — a named executive of the building lab, on the record, at a public conference — and it moves the reported stage from 'pre-training finishing / early post-training' to 'refinement with a staged early release planned'. Status deliberately HELD at in-testing rather than advanced to confirmed: there is still no date, model card, benchmark, spec or access path, and a stated intention to ship early is a disposition rather than an artifact. Separately recorded as build-process context, not as evidence about Gemini 4: Kavukcuoglu said in the same session that DeepMind now trusts AI agents to autonomously run parts of the training process — conducting experiments, analysing results, proposing hypotheses under human supervision — and that this was not true six months ago (@theinformation 20:31 UTC). Competitive frame: Gemini 4 will land after roughly a year without a new Google flagship, into a market where GPT-6 Astra ([[openai-gpt-6]]) and Claude Opus 5.5 ([[anthropic-opus-5-5-2026-09]]) are already shipped and benchmarked head-to-head."
  - ts: 2026-09-25
    change: "Bookkeeping — citations added for the 2026-09-25 entry: @theinformation (Kavukcuoglu, Gemini 4 in post-training, could arrive well before year-end), @mark_k (relay: refinement stage, release 'much earlier' than year-end, team willing to ship an early version), @theinformation (same session: DeepMind now lets agents autonomously run parts of the training process under human supervision). No status, verification or content change."
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
