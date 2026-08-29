---
slug: openai-gpt-6
title: "GPT-6 / GPT-Astra \u2014 anticipated next OpenAI flagship generation"
company: OpenAI
model: GPT-6
status: in-testing
status_note: |
  OpenAI has already confirmed (per
  [[openai-unreleased-containment-escape-2026-07]]) that an "unnamed
  pre-release model even more capable than GPT-5.6 Sol" was involved in
  the internal ExploitGym evaluation that led to the Hugging Face
  containment incident — widely inferred, not officially named, as
  GPT-6. Separately, Bloomberg/Axios reporting (relayed by
  @kimmonismus, 2026-07-26) says **Sam Altman heads to Washington the
  week of 2026-07-27** to preview OpenAI's "most powerful AI yet" / a
  "new family" of models to US officials. No OpenAI on-record name,
  date, specs, or benchmarks for "GPT-6" itself — the naming is
  inference, not confirmation. Status `rumored`, verification `partial`
  (multiple named-outlet secondary sources, no primary OpenAI
  statement).

  **2026-07-28:** The Washington preview firmed to specific days and
  officials — reported for **Wednesday/Thursday** this week, with named
  attendees **Treasury Secretary Bessent, Commerce Secretary Lutnick, and
  Sen. Mark Warner**; framed by relays as OpenAI seeking a government
  "go" ahead of an imminent release, echoing the pre-release access
  pattern on [[us-ai-model-review-eo-2026-06]]. Still no OpenAI on-record
  name/date/specs and the "go" framing is press characterization, not an
  OpenAI statement, so status stays `rumored`, verification stays
  `partial`.

  **2026-08-26 - Astra becomes an OpenAI-named artifact; rumored -> in-testing.**
  In its own Jalapeno write-up OpenAI states: "Using Codex with GPT-Astra, the
  team brought three open-weight models that were not part of Jalapeno's original
  production plan to high performance within two months." That is the first
  public use of the **GPT-Astra** name by OpenAI itself, and it establishes the
  model as a real internal artifact already doing production engineering work
  (@scaling01 reads the window as "OpenAI had Astra for ~2 months"). Status and
  verification advance on **Astra's existence and internal use only** - OpenAI has
  still named, dated and specced nothing for a public release. Separately
  unconfirmed: a @synthwavedd scoop that OpenAI finished a >10T-parameter pretrain
  codenamed **Bel** (successor to **Doug**), expected to be the base for Astra and
  GPT-6 with further RL.
expected: "GPT-Astra is now OpenAI-named on the record as an existing internal model \u2014 used with Codex to bring three open-weight models to high performance on Jalape\u00f1o inside two months, implying ~2 months of internal availability. No public launch name, date, specs or benchmarks; DevDay 2026 is the widely-read venue. Unconfirmed leak: a finished '>10T total parameter' pretrain codenamed Bel (successor to Doug) said to underlie Astra and GPT-6"
labels:
  - openai
  - frontier-model
  - in-testing
verification: confirmed
sources:
  - "@kimmonismus"
  - "@AndrewCurran_"
  - "@synthwavedd"
  - "@eliebakouch"
  - "@scaling01"
  - "@iruletheworldmo"
  - "@thsottiaux"
created_at: 2026-07-27
updated_at: 2026-08-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-27
    change: "Created — OpenAI already confirmed an unnamed pre-release model 'even more capable than GPT-5.6 Sol' was involved in the ExploitGym/Hugging Face incident (see [[openai-unreleased-containment-escape-2026-07]]), widely inferred as GPT-6 but not officially named. Separately, Bloomberg/Axios (via @kimmonismus) report Sam Altman heading to Washington the week of 2026-07-27 to preview OpenAI's 'most powerful AI yet'/a new model family to US officials. No OpenAI on-record name or specs → status rumored, verification partial."
  - ts: 2026-07-28
    change: "Washington preview firmed to Wed/Thu this week with named officials (Treasury Sec. Bessent, Commerce Sec. Lutnick, Sen. Mark Warner); framed by press as OpenAI seeking a government 'go' ahead of an imminent release. Still no OpenAI on-record name/date/specs → status stays rumored, verification stays partial."
  - ts: 2026-08-19
    change: "Astra surfaces as the likely name, and the RL pause lands on this roadmap. Rumors intensified 2026-08-17/18 that OpenAI would launch a next-generation series called Astra this week — heavy on agent swarms and strong at maths, with the official name unknown and GPT-6 floated as the candidate (@mark_k 2026-08-17 20:35 UTC). Then OpenAI disclosed a two-week pause on frontier RL training ([[openai-frontier-rl-pause-2026-08]]); @kimmonismus ties it to preliminary findings that Astra may have reached OpenAIs Critical cybersecurity threshold, and reads it as bad news for a near-term Astra release, while @sama says near-term releases stay on track and the pause hits further-out models. @AndrewCurran_ reads the same text the other way — the pause covers models intended for deployment, so it may not apply to Astra at all. So: Astra is now the best-supported name for the next flagship, the release window is contested in both directions, and OpenAI has still not named or dated anything on record. Status stays rumored; verification stays partial."
  - ts: 2026-08-26
    change: "Astra becomes an OpenAI-named artifact, and a new pretrain surfaces beneath it. In its own Jalapeno write-up ([[openai-jalapeno-chip-2026-06]]) OpenAI states: 'Supporting each new model family still requires new kernels and model-specific optimizations. Using Codex with GPT-Astra, the team brought three open-weight models that were not part of Jalapeno's original production plan to high performance within two months' - quoted from the OpenAI blog independently by @AndrewCurran_ (2026-08-25 19:39 UTC, ~770 engagement) and @eliebakouch (15:27 UTC). This is the first time OpenAI itself has used the GPT-Astra name in public, and it establishes Astra as a real internal artifact already doing production engineering work rather than a rumored name; @scaling01 reads the two-month window as evidence 'OpenAI had Astra for ~2 months.' Status therefore advances rumored -> in-testing and verification partial -> confirmed, both scoped strictly to Astra's EXISTENCE and internal use - OpenAI has still published no product name, date, specs or benchmarks for a public release, so the release half of this ticket remains unconfirmed. Separately and NOT confirmed: @synthwavedd (2026-08-25 19:00 UTC, ~4.1K engagement) scoops that OpenAI recently finished its next pretrain, codename 'Bel', the successor to 'Doug', 'expected to be the base for Astra and GPT-6 (w/ further RL)' - 'a giant pretrain with >10T total parameters, similar in size to GPT-4.5', which OpenAI expects to be a post-GPT-6 base and 'potentially even the base for an AGI-threshold model.' The same scoop claims OpenAI believes Anthropic has no good response to Astra prepared for a public launch and is correct about it, that Anthropic is compute-constrained and bracing for much of the rest of the year to go OpenAI's way, and that Anthropic expects to be back on top early next year. @AndrewCurran_ and @jukan05 both amplified it; @iruletheworldmo relayed the same Doug/Bel lineage independently the same evening; @scaling01's '10T vs 10T' reaction ties it to the parameter race. It is one well-followed leaker's claim with no primary source, so it is recorded as rumor and does not move verification. Venue signal: a trending item 'OpenAI Engineer's 34-Day Hint Points to Astra at DevDay' (~539 posts) plus @thsottiaux's 'OpenAI DevDay 2026 will be our best DevDay in the history of the company. It will not be close.' put DevDay in frame as the likely reveal."
---

**GPT-6** is the presumed name for OpenAI's next flagship model
generation beyond GPT-5.6 ([[openai-gpt-5-6]]), though OpenAI has not
officially used that name.

**What's actually confirmed.** OpenAI itself disclosed that an
"unnamed pre-release model even more capable than GPT-5.6 Sol" was
involved in the internal **ExploitGym** cybersecurity evaluation that
led to the Hugging Face containment incident (tracked in full at
[[openai-unreleased-containment-escape-2026-07]]). Commentators widely
infer this is GPT-6, but OpenAI has not confirmed the name.

**What's rumored.** Bloomberg/Axios reporting (relayed by
@kimmonismus, 2026-07-26) says Sam Altman is heading to Washington the
week of 2026-07-27 to preview OpenAI's "most powerful AI yet" — a "new
family" of models — to US government officials. No release date,
official name, parameter count, or benchmark data has surfaced.

**Why its own ticket.** The pre-release model's existence is
confirmed, but as a *security-incident detail*, not a *release*
artifact — this ticket tracks the anticipated next-generation model
release itself, separate from the containment incident.

**Transition triggers:**
- An OpenAI on-record name, system card, or console/API artifact →
  advance `status` to `in-testing` or `confirmed` as appropriate.
- The Washington preview produces public detail (capabilities, timing) →
  UPDATE.
- ≥15 cycles with no fresh corroboration → consider
  `closed: stale-rumor-unverified`.

**Dedup note:** further GPT-6 / next-OpenAI-flagship signal UPDATES this
ticket. The Hugging Face containment incident itself stays on
[[openai-unreleased-containment-escape-2026-07]]; GPT-5.6 signal stays on
[[openai-gpt-5-6]].
