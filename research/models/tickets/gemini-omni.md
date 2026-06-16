---
slug: gemini-omni
title: Gemini Omni — multimodal generation model
company: Google / DeepMind
model: Gemini Omni (Omni Flash)
status: closed
status_note: |
  **Closed 2026-06-16 (released-and-aged).** Launched GA at Google I/O 2026
  (2026-05-19); ≥4 weeks of settled coverage, no successor variant or API news
  in-window, rolled into normal coverage. History preserved below.
  Launched at Google I/O 2026 (2026-05-19), starting with "Omni Flash". A
  generation + editing model that turns any mix of text / photo / audio /
  video into video, with consistent characters, physics, and scenes (and
  conversational video editing). Available now to paid subscribers in the
  Gemini app, Google Flow, and YouTube; Gemini API support "coming soon".
expected: null
labels:
  - google-io
  - multimodal
  - video-generation
  - released
verification: confirmed
sources:
  - "@OfficialLoganK"
  - "@demishassabis"
  - "@GoogleDeepMind"
created_at: 2026-05-20
updated_at: 2026-06-16
closed_at: 2026-06-16
closed_reason: released-and-aged
history:
  - ts: 2026-05-20
    change: "Created — Gemini Omni unveiled at Google I/O 2026 (official @OfficialLoganK, @demishassabis, @GoogleDeepMind); video-first \"any input → any output\" model, live now in the Gemini app, Flow, and YouTube as Omni Flash, with API support coming soon"
  - ts: 2026-06-16
    change: "Closed — released-and-aged. ≥4 weeks past the 2026-05-19 I/O GA with no successor variant, pricing, or public API news in-window; rolled into normal coverage. Per the ticket's transition trigger (close ≥4 weeks past public release). History preserved; reopen via a new ticket if a distinct Omni successor or the Gemini API GA lands."
---

Gemini Omni is Google DeepMind's new multimodal generation model,
announced at Google I/O 2026 alongside the
[Gemini 3.5 Flash](./gemini-3-2-flash.md) release. Logan Kilpatrick
framed it as "Nano Banana but for video": it can create from any input —
starting with video — and supports batch editing, improved character
consistency, and conversational editing. Demis Hassabis called it "a
major leap in world understanding & multimodal editing," able to take
photos, video, and audio and build entirely new scenes.

The first variant is **Omni Flash**, available now to paid subscribers in
the Gemini app, Google Flow, and YouTube. There is no public Gemini API
for Omni yet ("coming soon"), and early hands-on reports flagged some
buggy behavior in Flow at launch.

**Transition triggers:**
- Gemini API / general availability for Omni → keep `released`, update the
  status_note + history.
- ≥4 weeks past public release → `status: closed` with
  `closed_reason: released-and-aged`.

**Dedup note:** new Omni variants, the API launch, or pricing UPDATE this
ticket. A distinct successor model family gets its own ticket and links
back here.
