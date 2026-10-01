---
slug: google-gemini-4-2026-09
title: "Gemini 4 Argon — announced 2026-09-30, gated rollout to trusted cyber defenders via the Fairwind Program"
company: Google / DeepMind
model: Gemini 4
status: confirmed
status_note: |
  **2026-09-30 — ANNOUNCED, primary, by every Google voice at once.** @GoogleDeepMind
  (20:03 UTC): "Introducing Gemini 4 Argon – our new frontier model … rolling out
  today to a set of trusted testers through our Fairwind Program." Same hour from
  @GoogleAI, @Google, @OfficialLoganK, @sundarpichai ("an early look as soon as
  possible") and @demishassabis ("starting with government and trusted cyber
  defenders … before wider availability soon"). This is exactly the "early
  version" Kavukcuoglu described on 2026-09-24.

  **What Google states.** Built for long-horizon work — software engineering,
  legal/finance knowledge work, cybersecurity defense. **Output limit raised to
  1M tokens** (from 64K per relays). Introductory pricing **$2 in / $10 out per
  MTok** (@OfficialLoganK), reported as rising to $4/$20 at standard rate
  (@FundaAI). Google says Argon agents already run inside its own infrastructure
  (300+ TiB memory freed, 800K+ lines of C/C++→Rust kernel migration, per
  @kimmonismus relaying Google's post, retweeted by @demishassabis).

  **Third-party placements within hours** (all on gated access): #1 Text Arena at
  1525 (@arena), #1 Vals Index at 68.9% (@ValsAI), Artificial Analysis index 53 —
  level with GPT-6 Astra, below Opus 5.5 (58) and Sonnet 5.5 (56) per @FundaAI,
  with a notably low AA hallucination rate (15%, @aipulseda1ly relay).

  **Why `confirmed`, not `released`.** Access is a partner list. WSJ frames it as
  a gradual rollout "amid safety concerns" (@miraclemasui headline relay); there
  is no GA date. Released means anyone can use it.

  **Successor bookkeeping.** Coverage of the launch states Gemini 3.5 Pro was
  shelved and is not happening; [[gemini-3-5-pro]] is closed today as
  superseded by this ticket.
expected: "Announced 2026-09-30; rolling out first to government and trusted cyber defenders in the Fairwind Program, with paid API customers and Google AI Ultra subscribers reported next. Broader developer/enterprise/consumer availability 'as soon as possible' — no public date. Moves to released when anyone can use it."
labels:
  - google
  - deepmind
  - frontier-model
  - unreleased
verification: confirmed
sources:
  - https://x.com/kimmonismus/status/2102949590542741983
  - https://x.com/testingcatalog/status/2103015463089238076
  - https://x.com/theinformation/status/2103129866375659543
  - https://x.com/mark_k/status/2103125879903629571
  - https://x.com/theinformation/status/2103220914347188282
  - https://x.com/theinformation/status/2104217001925251455
  - https://x.com/mark_k/status/2104479951952986469
  - https://x.com/JustLingonberry/status/2104431004337479933
  - https://x.com/GoogleDeepMind/status/2105388084154056939
  - https://x.com/GoogleDeepMind/status/2105388087367127256
  - https://x.com/GoogleAI/status/2105388478683119904
  - https://x.com/OfficialLoganK/status/2105388054274080946
  - https://x.com/demishassabis/status/2105417239432200636
  - "@sundarpichai"
  - "@arena"
  - "@ValsAI"
  - https://x.com/FundaAI/status/2105651450462249245
  - https://x.com/miraclemasui/status/2105649564057530623
created_at: 2026-09-24
updated_at: 2026-10-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — IN-TESTING. Successor to [[gemini-4-2026-07]], closed 2026-08-19 as stale-rumor-unverified with the standing condition that a named artifact or a DeepMind statement would open a successor. Condition met: @kimmonismus (2026-09-24, citing The Information) reports Gemini 4 has almost finished training with release 'hopefully much earlier than end of year', and @testingcatalog's same-day brief attributes the statement to Koray (Kavukcuoglu, DeepMind CTO) with the more specific claim that Gemini 4 is in early post-training. Opened at in-testing rather than rumored because the claim is a falsifiable training-stage assertion from a named principal, not an anonymous roadmap tease; verification partial because it still arrives via an outlet and two relay accounts with no Google or DeepMind post, no date, no specs and no model card in this cycle's signal. The predecessor's central failure — a timing claim that never resolved — is the specific risk being carried forward, so the 'well before year-end' target is recorded as an aspiration to hold accountable, not a schedule."
  - ts: 2026-09-25
    change: "Stage advanced within in-testing; status unchanged. DeepMind chief Koray Kavukcuoglu, speaking at The Information's AI Agenda Live on 2026-09-24, said Gemini 4 is in post-training / refinement and could arrive 'well before year-end', adding the new detail that the team is excited enough by the results to release an EARLY VERSION and keep improving it quickly (@theinformation 14:30 UTC; @mark_k relay 14:14 UTC, ~509 likes, quoting 'much earlier' than end of year). This is a stronger source class than the previous entry's relay — a named executive of the building lab, on the record, at a public conference — and it moves the reported stage from 'pre-training finishing / early post-training' to 'refinement with a staged early release planned'. Status deliberately HELD at in-testing rather than advanced to confirmed: there is still no date, model card, benchmark, spec or access path, and a stated intention to ship early is a disposition rather than an artifact. Separately recorded as build-process context, not as evidence about Gemini 4: Kavukcuoglu said in the same session that DeepMind now trusts AI agents to autonomously run parts of the training process — conducting experiments, analysing results, proposing hypotheses under human supervision — and that this was not true six months ago (@theinformation 20:31 UTC). Competitive frame: Gemini 4 will land after roughly a year without a new Google flagship, into a market where GPT-6 Astra ([[openai-gpt-6]]) and Claude Opus 5.5 ([[anthropic-opus-5-5-2026-09]]) are already shipped and benchmarked head-to-head."
  - ts: 2026-09-25
    change: "Bookkeeping — citations added for the 2026-09-25 entry: @theinformation (Kavukcuoglu, Gemini 4 in post-training, could arrive well before year-end), @mark_k (relay: refinement stage, release 'much earlier' than year-end, team willing to ship an early version), @theinformation (same session: DeepMind now lets agents autonomously run parts of the training process under human supervision). No status, verification or content change."
  - ts: 2026-09-28
    change: "Two developments, one of which this ticket explicitly REFUSES to treat as evidence. (1) @theinformation, on its own handle (2026-09-27 14:30 UTC), restates the stage claim directly rather than through a relay: 'Google is preparing to release Gemini 4 as it works to close the gap with Anthropic and OpenAI. DeepMind chief Koray Kavukcuoglu said the model is in post-training and could arrive well before year-end.' Same substance as the 2026-09-24 entry, now in the outlet's own voice — a sourcing upgrade, not a new fact, so status stays in-testing and verification stays partial. (2) UNADOPTED: 'leaked Gemini 4 Pro benchmarks' circulated widely on 2026-09-28 claiming Gemini 4 Pro 'absolutely destroys' Astra and Opus 5.5 (@JustLingonberry, amplified by @mark_k as 'Huge if true', and by others as timed to spoil OpenAI DevDay). NO benchmark table, harness, provenance or verifiable artifact reached this desk — only screenshots and reaction. Unsourced leaked scores are the single most gamed artifact class in this space and are recorded here solely so a later real benchmark is not confused with them. @iruletheworldmo takes the opposite position the same day ('gemini 4 will be far off sota'), which is equally unsourced and is logged for symmetry. Nothing changes: no date, no model card, no spec, no access path."
  - ts: 2026-10-01
    change: "ANNOUNCED -> status confirmed (from in-testing), verification confirmed (from partial); title updated to the official name. Google announced Gemini 4 Argon on 2026-09-30 ~20:03 UTC across @GoogleDeepMind, @GoogleAI, @Google, @OfficialLoganK, @sundarpichai and @demishassabis: a frontier model for long-horizon coding, enterprise knowledge work and cyber defense, with a 1M-token output limit, rolling out first to government and trusted cyber defenders in the Fairwind Program, broader availability 'as soon as possible'. Introductory API price $2/$10 per MTok (@OfficialLoganK; reported $4/$20 standard per @FundaAI). Third-party placements the same evening: #1 Text Arena 1525 (@arena), #1 Vals Index 68.9% (@ValsAI), AA index 53 (level with GPT-6 Astra, below Opus 5.5 58) per @FundaAI. WSJ headline: Google rolls the model out gradually amid safety concerns. Held at confirmed rather than released because access is a partner list with no GA date. The 2026-09-28 'leaked Gemini 4 Pro benchmarks' entry remains unadopted; the official tables replace it. Companion change: [[gemini-3-5-pro]] closed as superseded-by this ticket."
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

**2026-10-01 update — it shipped as an announcement, not a release.** The model
is Gemini 4 **Argon**, announced 2026-09-30 by Google's own accounts, and the
"early version" framing from the 2026-09-24 entry turned out to be literal: a
gated rollout to cyber defenders first. The timing claim this ticket was opened
to hold accountable resolved early, and the open question is now the GA date.
