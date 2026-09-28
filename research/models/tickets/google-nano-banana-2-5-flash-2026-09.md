---
slug: google-nano-banana-2-5-flash-2026-09
title: Nano Banana 2.5 Flash — traces spotted in Google Flow
company: Google / DeepMind
model: Nano Banana 2.5 Flash
status: in-testing
status_note: |
  **Single-source app artifact, 2026-09-24 13:25 UTC.** @testingcatalog:
  "GOOGLE: Nano Banana 2.5 Flash traces have been spotted on Google Flow.
  Soon?" with a screenshot. No Google statement, no model card, no date, no
  pricing.

  **Why `in-testing` rather than `rumored`.** A version string present in a
  shipped Google product is an artifact, not a tease — the same class of
  evidence as a GCP console listing. What is NOT established is anything about
  the model: capability, modality changes, whether "2.5" is a checkpoint bump
  or a new family member, or whether Flow is the launch surface rather than
  merely where the string leaked.

  **Lineage.** Nano Banana is Google's image-generation line, already tracked
  at [[google-nano-banana-2-2026-05]] and
  [[google-nano-banana-2-lite-2026-06]]. Google Flow is the video/creative
  surface that also received Lyria 3.5 ([[google-lyria-3-5-2026-07]]), so a
  Flow-first appearance is consistent with how this line has shipped before.

  **Cadence context, not evidence.** Google shipped Gemini 3.8 Flash, 3.8 Flash
  TTS, 3.8 Live and WeatherNext 3 inside a month, and Gemini 4 is reportedly in
  post-training ([[google-gemini-4-2026-09]]). A 2.5 Flash string appearing now
  fits that release tempo. That makes the leak plausible; it does not make it
  corroborated.
expected: "TBD — still not available. The Flow reference changed from Nano Banana 2.5 Flash to Nano Banana 2.1 on 2026-09-27, so the version number this ticket is named for may not be what ships. Watch for a Google/DeepMind post, availability in Flow, or the model appearing in the Gemini API or AI Studio."
labels:
  - google
  - deepmind
  - image-generation
  - nano-banana
  - leak
  - unreleased
verification: partial
sources:
  - https://x.com/testingcatalog/status/2103113565880090830
  - https://x.com/testingcatalog/status/2104218540567924747
  - https://x.com/testingcatalog/status/2104493424472674634
created_at: 2026-09-25
updated_at: 2026-09-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-25
    change: "Created — IN-TESTING / unverified. @testingcatalog reported on 2026-09-24 13:25 UTC (~525 likes) that 'Nano Banana 2.5 Flash traces have been spotted on Google Flow', with a screenshot and no further detail. Status in-testing rather than rumored because a version string inside a shipped Google product is a real artifact, the same evidence class as a console listing; verification unverified because it is one outlet, one surface, no Google statement, no model card, no date, no pricing, and nothing at all about capability. Recorded in the existing Nano Banana lineage alongside [[google-nano-banana-2-2026-05]] and [[google-nano-banana-2-lite-2026-06]]; Flow is a plausible launch surface for this line, having previously carried Lyria 3.5 ([[google-lyria-3-5-2026-07]]). Google's September release tempo is noted as context only, explicitly not as corroboration. If no second sighting or announcement appears within the stale-rumor window this should close rather than linger as an unresolved string."
  - ts: 2026-09-28
    change: "THE VERSION STRING MOVED DOWN, which is the most informative thing a leak of this class can do. @testingcatalog (2026-09-27 14:36 UTC), following its own 2026-09-24 sighting: 'Nano Banana 2.5 Flash reference has been changed to Nano Banana 2.1 on Google Flow. A minor bump? * Not available yet.' Restated in its 2026-09-28 brief: 'Flow build now points to Nano Banana 2.1, replacing the Nano Banana 2.5 Flash reference. Not available yet.' Two readings and this desk does not pick one: either the 2.5 Flash string was a placeholder/internal name and 2.1 is the real next release, or Google reshuffled the line's numbering. Both are consistent with the observation; neither is established. Verification unverified -> partial: the same outlet has now made two dated, mutually-consistent observations of the same build surface, which is materially better than a single screenshot, and still short of a Google statement. Status stays in-testing — a string in a shipped build remains an artifact, and 'Not available yet' remains true four days on. SLUG NOTE: this ticket keeps its name per the immutability rule even though the artifact it was named for may be superseded by a lower version number; if a '2.1' ships as a distinct model line, it gets its own ticket and links here."
---

This is a string in a product, and that is genuinely all it is.

The reason it is worth a ticket rather than a shrug is that Google's image line
has leaked this way before, and the leaks have converted. Nano Banana 2 and
Nano Banana 2 Lite both surfaced as artifacts ahead of announcement, so a
version string in Flow is a signal with a track record rather than a rumour
with a plausible shape.

What the string does not tell you is whether "2.5 Flash" is a meaningful
capability step or a routing-tier rename. Google has been aggressive about
splitting families into Flash, Flash-Lite and Live variants across the Gemini
3.8 wave, and a "2.5 Flash" in the image line could as easily be a cheaper
serving tier of the existing model as a new one.

The honest position for now: something called Nano Banana 2.5 Flash exists
inside Google Flow, one outlet saw it, and nothing else is known. A second
independent sighting or an appearance in AI Studio would move this; another
week of silence should close it.
