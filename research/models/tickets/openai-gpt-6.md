---
slug: openai-gpt-6
title: "GPT-6 Astra — OpenAI flagship, publicly released 2026-09-03"
company: OpenAI
model: GPT-6
status: released
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

  **2026-09-03/04 — SHIPPED. in-testing -> released, and the ticket's release half
  is now confirmed.** OpenAI announced GPT-6 Astra on 2026-09-03 19:32 UTC
  ("This is GPT-6 Astra. Anything you can do on a computer, Astra can do for
  you. Fast." — ~334K likes, the largest single item in this cycle's signal),
  rolling out that day to a limited set of organizations and over the following
  days to all ChatGPT Plus/Pro/Business/Enterprise users plus the OpenAI API and
  AWS. On 2026-09-04 20:13 UTC OpenAI confirmed availability to all
  Pro/Enterprise/Business Premium users in ChatGPT Work and Codex and in the API;
  @sama confirmed Plus and Business at 22:52 UTC and apologised for a "messy
  rollout". OpenAI's own claims: state of the art for computer use, browsing,
  software engineering, cybersecurity, science and professional work, with SOTA
  on Agents' Last Exam, AutomationBench and ScreenSpot Pro, and "our most aligned
  model". Pre-launch (2026-09-01) OpenAI disclosed that Astra reaches the
  **Critical** cybersecurity threshold under its Preparedness Framework — the
  same capability that drove the RL pause in
  [[openai-frontier-rl-pause-2026-08]].

  **Not confirmed.** Per @mark_k (2026-09-06), GPT-6 is a **family**, Astra is its
  flagship and currently the only member shipped, with Sol, Terra and Luna to
  follow — a well-followed relay, not an OpenAI statement. Jensen Huang stated
  Astra was trained on ~100K NVIDIA Grace Blackwell NVL72 with 400K GPUs coming
  online next at Stargate Texas, and called it AGI (@AndrewCurran_ 2026-09-06).
  Parameter count is actively contested — @scaling01 argues 6-8T total against
  10T+ rumors, @teortaxesTex argues <350B active — and The Information's
  "recurrent depth / looped transformer" architecture claim was publicly pushed
  back on by @rasbt. Only the release is confirmed.

  **2026-09-16 — the second family member surfaces. GPT-6 Sol, sighted, not
  announced.** @AndrewCurran_ (2026-09-15 15:21 UTC), flatly: "GPT-6 Sol is
  incoming." @yota0x_ (2026-09-16 10:57 UTC) supplies the artifact detail:
  "GPT-6 Sol just appeared in **OpenAI's API and Arena system tests**… no
  official announcement yet," claiming it produced **28K tokens in ~3 minutes
  against Astra's 19 minutes on the same task (~6x faster)**, positioned
  "below Astra but above GPT-5.6 Sol." This is the first concrete artifact
  for any GPT-6 family member beyond Astra, and it matches the naming
  @mark_k relayed on 2026-09-06 (Sol/Terra/Luna to follow) — the first
  independent support that relay has received.

  **The speed claim is publicly contested in the same window.**
  @paul010318 separates signal from assumption: @sama's teaser ("big 🚢 this
  week and then for devday", 2026-09-15 14:46 UTC) named no model and no
  date, a knowledge-cutoff probe returned inconsistent answers across
  instances, and "the recent buzz… hinges on unverified signals — not
  shipped capabilities." So the *sighting* is the evidence; the 6x figure is
  one account's single-task measurement and is **not adopted here**.

  **Positioning, recorded as inference and not fact:** a fast/cheap tier
  below the flagship rather than a successor to it — the same shape as the
  Flash/Live split Google shipped this week
  ([[google-gemini-3-8-live-2026-09]]) — with DevDay the venue in frame.
expected: "RELEASED (Astra). GA across ChatGPT Plus/Pro/Business/Enterprise, the OpenAI API and AWS as of 2026-09-04. Open: GPT-6 Sol, now SIGHTED in API/Arena system tests but not announced — watch for an OpenAI post, model card or pricing; Terra and Luna still unsupported by anything but one relay; parameter count and the 'looped transformer' architecture claim remain unverified rumor."
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
  - https://x.com/OpenAI/status/2095595741528125780
  - https://x.com/OpenAI/status/2095595757072191802
  - https://x.com/OpenAI/status/2095968413646737608
  - https://x.com/sama/status/2096008528834244741
  - https://x.com/OpenAI/status/2094885578173260259
  - https://x.com/mark_k/status/2096533124096172402
  - https://x.com/AndrewCurran_/status/2096703533144052116
  - "@rasbt"
  - "@WesRoth"
  - https://x.com/kimmonismus/status/2099045668241457529
  - "@simonw"
  - https://x.com/AndrewCurran_/status/2099881354494361835
  - https://x.com/yota0x_/status/2100177184262398146
  - "@paul010318"
created_at: 2026-07-27
updated_at: 2026-09-16
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
  - ts: 2026-09-07
    change: "RELEASED. OpenAI announced GPT-6 Astra 2026-09-03 19:32 UTC and completed the public rollout 2026-09-04: GA to all Pro/Enterprise/Business Premium in ChatGPT Work and Codex plus the OpenAI API and AWS (OpenAI 20:13 UTC), then to all Plus and Business users (@sama 22:52 UTC); @sama apologised for the 'messy rollout'. OpenAI claims SOTA for computer use, browsing, software engineering, cybersecurity, science and professional work, with state-of-the-art results on Agents' Last Exam, AutomationBench and ScreenSpot Pro, and calls it 'our most aligned model'. Pre-launch on 2026-09-01 OpenAI disclosed that Astra reaches the Critical cybersecurity threshold under its Preparedness Framework. Third-party placement: #1 on Code Arena WebDev at 1,797, +35 over Claude Fable 5.1 and +180 over GPT-5.6 Sol (@WesRoth 2026-09-07). Status in-testing -> released; verification stays confirmed and now covers the release itself, not just Astra's existence. Recorded as rumor, NOT confirmed: @mark_k says GPT-6 is a model family with Sol/Terra/Luna still to come; Jensen Huang says Astra trained on ~100K Grace Blackwell NVL72 with 400K GPUs next at Stargate Texas and that 'AGI has arrived'; parameter count is disputed (@scaling01 6-8T total vs @teortaxesTex <350B active) and The Information's looped-transformer architecture claim was publicly disputed by @rasbt. The separate @synthwavedd 'Bel' pretrain scoop remains uncorroborated."
  - ts: 2026-09-14
    change: "Cadence, a size correction, and the first post-launch quality complaints. CADENCE (@kimmonismus, 2026-09-13 08:01 UTC, ~2.5K likes): 'GPT-5.6 Sol launched on July 9. GPT-6 Astra began rolling out on September 3. Exactly eight weeks apart' — which dates the predecessor's launch and is the basis on which [[openai-gpt-5-6]] was closed released-and-aged this cycle. He adds a forward worry rather than a fact: that the slowdown push may make Astra 'the last release to follow its predecessor so quickly.' SIZE (@scaling01, 2026-09-14 02:16 UTC, ~2.3K likes): 'Astra is much smaller than I thought / looped transformers are going to eat the world' — relevant because this ticket carries the looped-transformer architecture claim as unverified; a well-followed account revising DOWNWARD is weak evidence for the architecture and none at all for a parameter count. @teortaxesTex, same window, is blunt that the surrounding numbers are invented: 'neither Astra nor Fable are \"10T\". stop soyfacing over speculative model sizes, they're very tenuously related to capability now.' No parameter count is adopted here. QUALITY COMPLAINTS (@deoriginalme, 2026-09-14 12:35 UTC): 'Users are already reporting a noticeable drop in GPT-6 Astra's performance just a week after its launch' — single unsourced roundup account, recorded as a claim to watch, NOT as a measured regression. CAPABILITY, firsthand and better-sourced (@simonw, 2026-09-13 00:19 UTC): ChatGPT Work and GPT-6 Astra on a 'Max' tier produced a 5K/10K circular running route from an address using OSM data, returned through a 'visualize' skill as an HTML fragment using D3 — which independently attests a 'Max' reasoning tier in the product UI. Standing assessment from @emollick (2026-09-13): 'GPT-6 Astra and Fable 5.1 are already enough for transformative impact in large sections of the economy. They can reliably do weeks worth of human work when properly guided & harnessed.' Status stays released."
  - ts: 2026-09-16
    change: "GPT-6 SOL SURFACES AS AN ARTIFACT — the first family member beyond Astra with anything concrete behind it. @AndrewCurran_ (2026-09-15 15:21 UTC): 'GPT-6 Sol is incoming.' @yota0x_ (2026-09-16 10:57 UTC) supplies the artifact: 'GPT-6 Sol just appeared in OpenAI's API and Arena system tests… no official announcement yet', claiming 28K tokens in roughly 3 minutes against Astra's 19 minutes on the same task (~6x faster) and positioning it 'below Astra but above GPT-5.6 Sol'. This is the first independent support for @mark_k's 2026-09-06 relay that GPT-6 is a family with Sol/Terra/Luna to follow, and it is why this stays on THIS ticket: the expected: field has carried the rest of the family as the named open item since 2026-09-07, so Sol is in declared scope rather than a new artifact — it gets its own ticket only if it launches as a separately-priced product. THE SPEED CLAIM IS NOT ADOPTED. @paul010318 published the contra the same morning, separating what changed from what is assumed: @sama's 2026-09-15 14:46 UTC teaser ('big ship this week and then for devday') named no model and no date; a knowledge-cutoff probe returned 'Claude Opus 4.7' on one instance and '4.1' on another, so instance-level probing is not evidence; and 'the recent buzz around a potential GPT-6 Sol release hinges on unverified signals — not shipped capabilities.' The SIGHTING is the evidence; the 6x figure is one account's single-task measurement with no methodology and is recorded as a claim only. Ticket status stays RELEASED (Astra shipped 2026-09-03/04) — Sol does not move it, because a system-test sighting of a sibling is not a release. Recorded as inference and not fact: Sol positioned below the flagship reads as a fast/cheap tier rather than a successor, the same shape as the Flash/Live split Google shipped this week ([[google-gemini-3-8-live-2026-09]]), with DevDay the venue in frame."
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
