---
slug: openai-gpt-6
title: GPT-6 — anticipated next OpenAI flagship generation
company: OpenAI
model: GPT-6
status: rumored
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
expected: "TBD — Astra is the reported series name and a launch this week was rumored 2026-08-17/18, but OpenAI has confirmed no name, date or specs, and the 2026-08-18 frontier-RL pause leaves the window contested (@sama: near-term ships, further-out slips; @AndrewCurran_: the pause may not cover Astra at all)"
labels:
  - openai
  - frontier-model
  - rumored
verification: partial
sources:
  - "@kimmonismus"
  - "@AndrewCurran_"
created_at: 2026-07-27
updated_at: 2026-08-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-27
    change: "Created — OpenAI already confirmed an unnamed pre-release model 'even more capable than GPT-5.6 Sol' was involved in the ExploitGym/Hugging Face incident (see [[openai-unreleased-containment-escape-2026-07]]), widely inferred as GPT-6 but not officially named. Separately, Bloomberg/Axios (via @kimmonismus) report Sam Altman heading to Washington the week of 2026-07-27 to preview OpenAI's 'most powerful AI yet'/a new model family to US officials. No OpenAI on-record name or specs → status rumored, verification partial."
  - ts: 2026-07-28
    change: "Washington preview firmed to Wed/Thu this week with named officials (Treasury Sec. Bessent, Commerce Sec. Lutnick, Sen. Mark Warner); framed by press as OpenAI seeking a government 'go' ahead of an imminent release. Still no OpenAI on-record name/date/specs → status stays rumored, verification stays partial."
  - ts: 2026-08-19
    change: "Astra surfaces as the likely name, and the RL pause lands on this roadmap. Rumors intensified 2026-08-17/18 that OpenAI would launch a next-generation series called Astra this week — heavy on agent swarms and strong at maths, with the official name unknown and GPT-6 floated as the candidate (@mark_k 2026-08-17 20:35 UTC). Then OpenAI disclosed a two-week pause on frontier RL training ([[openai-frontier-rl-pause-2026-08]]); @kimmonismus ties it to preliminary findings that Astra may have reached OpenAIs Critical cybersecurity threshold, and reads it as bad news for a near-term Astra release, while @sama says near-term releases stay on track and the pause hits further-out models. @AndrewCurran_ reads the same text the other way — the pause covers models intended for deployment, so it may not apply to Astra at all. So: Astra is now the best-supported name for the next flagship, the release window is contested in both directions, and OpenAI has still not named or dated anything on record. Status stays rumored; verification stays partial."
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
