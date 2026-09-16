---
slug: openai-millennium-problems-2026-09
title: OpenAI claims significant progress on a second Millennium Prize problem
company: OpenAI
model: null
status: confirmed
status_note: |
  **On the record from OpenAI's president.** Greg Brockman (@gdb): "…We have
  significant progress on another one of these Millennium problems" — quoted
  and clipped by @Hangsiin (2026-09-15 21:01 UTC) and independently relayed by
  @AndrewCurran_ (2026-09-15 23:10 UTC) as "More confirmation that OpenAI has
  made 'significant progress' on a second Millennium problem, this time from
  Greg Brockman." A named executive saying it in a recorded setting is a
  primary source for the *claim*.

  **Confirmed: that OpenAI says this. Not confirmed: the mathematics.** No
  problem is named, no paper, no formalization, no referee. "Significant
  progress" is undefined and is not a solution.

  **Two independent accounts of a deliberate hold.** @AndrewCurran_
  (2026-09-15 23:36 UTC): Scott Aaronson wrote that he has heard rumors AI
  companies have reached solutions to longstanding open problems in
  theoretical computer science and "are now sitting on multiple major
  announcements because of the Navier-Stokes firestorm." Separately
  @scottnarmstrong, from closer in: "Since at least the ICM they (openAI) have
  been sitting on 'hundreds' of proofs of results, I was told… If they tell
  the NY Times 'we have major advance on another millennium problem' then they
  should be out with the news when they have the result. They can write a 450k
  lean formalization and a 160-page paper of a millennium problem in a few
  days." Both are secondhand, and both describe the same thing: results
  announced rhetorically and withheld substantively.

  **The governance complaint is the durable part.** Armstrong's stated worry —
  "your distance to the labs in the social graph determines how much you know"
  — is a claim about verification infrastructure, not about any one proof, and
  it is the reason this is a tracked artifact rather than a news item.
expected: "OpenAI has claimed progress; nothing has been published. Watch for: a named problem, a Lean formalization or preprint, referee response, or a Clay Mathematics Institute reaction. DevDay is the venue in frame per in-window speculation."
labels:
  - openai
  - mathematics
  - research-claim
  - disclosure
verification: partial
sources:
  - https://x.com/Hangsiin/status/2099966745595555904
  - https://x.com/AndrewCurran_/status/2099999310490603856
  - https://x.com/AndrewCurran_/status/2100005852564611151
  - https://x.com/scottnarmstrong/status/2099960311801696580
created_at: 2026-09-16
updated_at: 2026-09-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-16
    change: "Created — CONFIRMED (the claim), verification partial (the mathematics). OpenAI president Greg Brockman said on the record, '…We have significant progress on another one of these Millennium problems' (clipped by @Hangsiin 2026-09-15 21:01 UTC; independently relayed by @AndrewCurran_ 2026-09-15 23:10 UTC, who framed it as 'more confirmation… this time from Greg Brockman', implying a prior NYT-sourced statement). Status confirmed that OpenAI is making the claim; the claim itself is unverifiable — no problem named, no paper, no formalization, no referee, and 'significant progress' is undefined. TWO INDEPENDENT ACCOUNTS OF A DELIBERATE HOLD, both secondhand: @AndrewCurran_ relays Scott Aaronson writing that he has heard AI companies reached solutions to longstanding open problems in theoretical computer science and 'are now sitting on multiple major announcements because of the Navier-Stokes firestorm'; @scottnarmstrong says OpenAI has 'been sitting on \"hundreds\" of proofs of results, I was told' since at least the ICM, and argues that if they tell the NY Times they have a major advance they should publish, noting they 'can write a 450k lean formalization and a 160-page paper of a millennium problem in a few days'. Armstrong's stated concern — that 'your distance to the labs in the social graph determines how much you know' — is logged as the durable issue: this is a disclosure-practice artifact, not a mathematics result. Related same-cycle AI-mathematics signal, tracked elsewhere: [[anthropic-fermat-lean-proof-2026-09]] and [[google-gemini-deepthink-mathematica-2026-09]]. Same-window @captain_sude claim that Astra proved an unconditional conjecture for multiples of 4 is recorded as context, not evaluated. @tszzl (OpenAI) argued in-window that 'labs sitting on solutions to important problems must reveal them quickly' — an employee taking the opposite side of the hold."
---

OpenAI's president said the company has **significant progress on another
Millennium Prize problem**. Nothing has been published.

**Separate the two facts.** That OpenAI is making the claim is confirmed — a
named executive said it in a recorded setting, and a second relay places an
earlier version of it in the New York Times. Whether the mathematics exists is
entirely unverified: no problem named, no preprint, no Lean artifact, no
referee. `verification: partial` reflects exactly that split.

**The hold is the story.** Two sources, from different distances, describe the
same pattern — results reached and withheld. Aaronson (secondhand, via
Curran) attributes the hold to the Navier-Stokes reaction; Armstrong
(secondhand, but closer to the room) says OpenAI has been sitting on
"hundreds" of proofs since the ICM. An OpenAI employee, @tszzl, publicly
argued the opposite position in the same window: "labs sitting on solutions to
important problems must reveal them quickly… everyone will have those
capabilities in a month or two." The company does not appear to have one
policy.

**Why this is a ticket and not a headline.** A Millennium problem is settled
by publication and refereeing; a claim of progress announced to a newspaper
and then held is not a mathematical event, it is a disclosure decision.
Armstrong names the cost precisely — proximity to the labs becomes the
determinant of what is knowable — and that is a structural property of the
field that outlasts whichever problem this turns out to be.

**The falsifier is unusually clean.** Either a formalization and a paper
appear and get refereed, or they do not. Armstrong's own point that the
artifacts could be produced "in a few days" makes continued silence
informative rather than neutral.

**Transition triggers:**
- A named problem, preprint, or Lean formalization published → UPDATE,
  advance `verification`.
- Referee or Clay Mathematics Institute response → UPDATE; this is what
  would settle it.
- DevDay (the venue in frame per in-window speculation) passing with no
  disclosure → UPDATE; treat continued silence as evidence about the hold.
- A retraction or walk-back → UPDATE.

**Dedup note:** Anthropic's formal-proof work stays on
[[anthropic-fermat-lean-proof-2026-09]]; Google's math variant stays on
[[google-gemini-deepthink-mathematica-2026-09]]; GPT-6 model signal stays on
[[openai-gpt-6]].
