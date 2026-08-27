---
slug: gemini-3-5-transcribe-2026-08
title: Gemini 3.5 Transcribe — Google speech-to-text model with streaming and post-processing
company: Google / DeepMind
model: Gemini 3.5 Transcribe
status: released
status_note: |
  **Shipped 2026-08-26 and available the same day.** Announced in parallel
  by **@GoogleAI**, **@GoogleDeepMind**, **@OfficialLoganK** (Gemini API
  product lead), **@_philschmid** and **@sundarpichai** (RT'd by
  @demishassabis) — a full first-party launch, not a leak or a preview.

  **What it is.** @OfficialLoganK: "Introducing **Gemini 3.5 Transcribe**,
  our new speech to text model with smart transcription, **function
  calling**, more precise transcription (**lower WER**), **custom
  vocabulary** support, **multi-speaker identification**, and support for
  **over 85 languages**! Also with **realtime streaming** support."

  **The numbers are first-party and specific**, which is unusual enough to
  record verbatim. @_philschmid: "**2.6% WER on non-streaming and 4.0% on
  streaming**… **70% reduction time for the final transcription compared
  to Chirp 3**," across "85+ languages," with the model cleaning up
  conversational disfluencies ("um", "ah", mid-sentence self-corrections)
  and handling alphanumeric tokens such as postal codes and IDs. Two model
  ids ship:

  - **`gemini-3.5-transcribe-live`** — sub-second bidirectional streaming
    via the **Gemini Live API**
  - **`gemini-3.5-transcribe`** — recorded processing via the
    **Interactions API**

  **Distribution is broad on day one.** Per @GoogleAI and @testingcatalog:
  the **Gemini app on macOS**, **Gboard on Android**, **Google AI Studio**,
  the **Gemini API**, **Antigravity**, and the **Gemini Enterprise Agent
  Platform** (public preview), with **Chrome** and **Gemini Enterprise for
  Customer Experience** listed as coming. @OfficialLoganK adds that it is
  "already powering many product experiences across Google."

  **Why a speech model earns a ticket in a frontier-model lane.** The
  feature list is an *agent* feature list, not a dictation one:
  **function calling** in a transcription model means the transcript can
  drive tool calls directly, and @_philschmid frames the streaming variant
  explicitly as "for **agent interfaces**." That places it against
  [[gemini-omni-api-2026-06]] and the realtime-voice race rather than
  against legacy ASR.

  Verification `confirmed`: multiple first-party Google accounts including
  the DeepMind and Google AI institutional handles and the responsible
  product lead. What is **not** established is any of the quality numbers
  — 2.6%/4.0% WER and the 70% latency reduction versus Chirp 3 are all
  Google-published, on unstated test sets, with no neutral evaluation and
  no third-party firsthand report captured in-window.
expected: "Live as of 2026-08-26 in the Gemini app for macOS, Gboard on Android, Google AI Studio, the Gemini API, Antigravity and the Gemini Enterprise Agent Platform (public preview); Chrome and Gemini Enterprise for Customer Experience announced as coming. Two ids: gemini-3.5-transcribe-live (sub-second streaming, Live API) and gemini-3.5-transcribe (recorded, Interactions API). Pending: pricing, a model card, any neutral-org WER benchmark against the claimed 2.6%/4.0%, independent confirmation of the 70% latency reduction versus Chirp 3, and firsthand practitioner reports — none existed in-window"
labels:
  - google
  - gemini
  - speech-to-text
  - realtime
  - agents
  - released
verification: confirmed
sources:
  - "@OfficialLoganK"
  - https://x.com/OfficialLoganK/status/2092660925509890397
  - "@GoogleAI"
  - https://x.com/GoogleAI/status/2092660089509314735
  - "@GoogleDeepMind"
  - "@_philschmid"
  - "@sundarpichai"
  - "@demishassabis"
  - "@testingcatalog"
created_at: 2026-08-27
updated_at: 2026-08-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-27
    change: "Created — Google shipped Gemini 3.5 Transcribe on 2026-08-26, announced in parallel by @GoogleAI, @GoogleDeepMind, @OfficialLoganK, @_philschmid and @sundarpichai (RT'd by @demishassabis), and available the same day. Capabilities per @OfficialLoganK: smart transcription, function calling, lower WER, custom vocabulary, multi-speaker identification, 85+ languages, realtime streaming. First-party numbers per @_philschmid: 2.6% WER non-streaming, 4.0% streaming, 70% reduction in final-transcription time versus Chirp 3, automatic removal of disfluencies and correct handling of alphanumeric tokens like postal codes and IDs. Two model ids ship — gemini-3.5-transcribe-live for sub-second bidirectional streaming via the Gemini Live API, and gemini-3.5-transcribe for recorded processing via the Interactions API. Day-one distribution per @GoogleAI and @testingcatalog: Gemini app on macOS, Gboard on Android, Google AI Studio, the Gemini API, Antigravity and the Gemini Enterprise Agent Platform in public preview, with Chrome and Gemini Enterprise for Customer Experience announced as coming; @OfficialLoganK says it already powers many Google product experiences. Status released, verification confirmed on multiple first-party institutional accounts. Explicitly NOT established: every quality claim is Google-published on unstated test sets, with no neutral evaluation and no third-party firsthand report in-window. Earns a ticket in this lane because function calling plus sub-second streaming makes it an agent-interface component rather than dictation — the same surface as [[gemini-omni-api-2026-06]]."
---

**Gemini 3.5 Transcribe** is Google's new speech-to-text model, announced
and shipped on 2026-08-26 across the Gemini app, Gboard, AI Studio, the
Gemini API, Antigravity and Gemini Enterprise.

**Read the feature list carefully and it is not a dictation model.**
Traditional ASR ships WER and language count. This ships WER *and*
**function calling**, *and* sub-second bidirectional streaming through the
Live API. @_philschmid says the quiet part directly: the streaming variant
is "for **agent interfaces**." A transcription model that can call tools
is a voice front-end for an agent, which is why it sits next to
[[gemini-omni-api-2026-06]] in this ticket set rather than alongside
legacy speech products.

**The claimed numbers, and the caveat that must travel with them.**
2.6% WER non-streaming, 4.0% streaming, 85+ languages, and a **70%
reduction in final-transcription latency versus Chirp 3** — Google's own
predecessor, which is the comparison a vendor picks when it wants a clean
win. All of it is first-party, on undisclosed test sets. Nothing neutral
has scored it, and in this window nobody outside Google posted a firsthand
run. Treat the shipping as confirmed and the quality as unverified.

**What it displaces internally.** @OfficialLoganK notes the model is
"already powering many product experiences across Google" and calls it
"another key element of our Gemini Audio portfolio" — so this is
consolidation of Google's audio stack onto the Gemini line, continuing the
pattern [[gemini-embedding-2]] and [[gemini-omni]] follow: specialist
models folded into one family, shipped through one API.

**Transition triggers:**
- Pricing and a model card → UPDATE.
- Any neutral-org WER result, or a firsthand practitioner comparison
  against Whisper/Chirp/competitors → UPDATE, and correct the numbers if
  they do not hold.
- Chrome / Gemini Enterprise CX availability landing → UPDATE.
- ≥4 weeks past release, settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** Gemini flagship and Flash releases stay on their own
tickets ([[gemini-3-7-flash-2026-08]], [[gemini-3-5-pro]]); realtime
multimodal API surface stays on [[gemini-omni-api-2026-06]]. Further
Gemini 3.5 Transcribe pricing, benchmark or availability signal UPDATES
this ticket.
