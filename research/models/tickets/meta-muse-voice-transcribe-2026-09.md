---
slug: meta-muse-voice-transcribe-2026-09
title: Muse Voice Transcribe — Meta Superintelligence Labs' first real-time audio perception model
company: Meta (Meta Superintelligence Labs)
model: Muse Voice Transcribe
status: released
status_note: |
  Announced and shipped 2026-09-01 by @AIatMeta and @alexandr_wang as "the
  first real-time audio perception model from Meta Superintelligence Labs."
  Claimed capabilities: real-time streaming ASR, diarization with **20+
  speakers**, endpointing, multilingual with seamless code-switching, and
  accuracy improvements from language, keyword and context biasing. Meta says
  it ranks **first on Artificial Analysis' streaming speech-to-text** leaderboard
  and, with adaptive delay, sits on the pareto frontier of the speed-accuracy
  trade-off measured by time-to-final-transcription.

  Tracked separately from [[meta-hatch-muse-spark-2026-06]] because it is a
  different shipping artifact on a different modality — a perception model, not
  a Muse Spark reasoning/coding release — even though it opened the same
  seven-day Meta launch run that continued with Muse Spark 1.3 (09-02), Muse
  Spark 1.3 max (09-04) and AIRA₃ (09-05,
  [[meta-aira-3-2026-09]]).

  Verification `confirmed` on Meta's own announcement; the benchmark placement
  is Meta's claim against a third-party leaderboard and has not been
  independently reproduced in this cycle's signal.
expected: "RELEASED 2026-09-01. Open: pricing/API surface, whether it lands in the Meta Model API alongside Muse Spark, and independent reproduction of the Artificial Analysis streaming STT placement."
labels:
  - meta
  - speech
  - audio-perception
  - released
verification: confirmed
sources:
  - https://x.com/AIatMeta/status/2094839236016976028
  - "@alexandr_wang"
created_at: 2026-09-07
updated_at: 2026-09-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-07
    change: "Created — RELEASED. @AIatMeta introduced Muse Voice Transcribe on 2026-09-01 17:26 UTC as the first real-time audio perception model from Meta Superintelligence Labs, rolled out the same day by @alexandr_wang. Claimed: real-time streaming ASR, diarization with 20+ speakers, endpointing, multilingual with seamless code-switching, and accuracy gains from language/keyword/context biasing. Meta claims first place on Artificial Analysis' streaming speech-to-text leaderboard and, with adaptive delay, the pareto frontier on the speed-accuracy trade-off measured by time to final transcription. Status released and verification confirmed on Meta's own announcement; the benchmark placement is Meta's claim and is not independently reproduced in this cycle's signal. Tracked separately from [[meta-hatch-muse-spark-2026-06]] because it is a distinct artifact on a distinct modality."
---

Meta opened a seven-day release run with this: a perception model rather than a
reasoning model. Muse Voice Transcribe on 09-01, Muse Spark 1.3 on 09-02, Muse
Spark 1.3 max on 09-04, AIRA₃ on 09-05 — four artifacts in five days from a lab
that spent most of 2026 being written off.

The interesting claim is not the leaderboard placement but the shape of the
trade-off Meta chose to optimize. Streaming ASR has a hard tension between how
long you wait and how right you are; Meta's stated result is a pareto frontier
on *time to final transcription* with adaptive delay, which is the metric that
matters for an assistant that has to decide when a person has stopped talking.
Read against the Muse agent in closed alpha
([[meta-hatch-muse-spark-2026-06]]), that reads less like a standalone model
launch and more like a component being staged.

Both claims — the Artificial Analysis first place and the pareto result — are
Meta's own, made against a third-party leaderboard, and nothing in this cycle's
signal independently reproduces either. The model itself is confirmed released;
the numbers are not yet corroborated.
