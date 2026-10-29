---
slug: nvidia-nemotron-3-5-transcribe-2026-10
title: "NVIDIA releases Nemotron 3.5 Transcribe — open-weight 30B-A4B MoE speech model (40 languages, speaker attribution)"
company: NVIDIA
model: "Nemotron 3.5 Transcribe"
status: released
status_note: |
  **First-party announcement, 2026-10-28 15:14 UTC.** @NVIDIAAI: "an open-weight, promptable 30B MoE model with
  ~4B active parameters that brings transcription in 40 languages, speaker attribution, translation, contextual
  prompting and audio understanding into one checkpoint."

  **Reported by secondary accounts:** 5.33% word error rate on the Hugging Face Open ASR (English) leaderboard,
  first among open-weight models (@AIEngineRoom). Handles hour-long audio. A user says a 4-bit build runs in about
  20 GB of unified memory (@argofowl). These are not first-party figures.
expected: "Released 2026-10-28 (open weights)."
labels:
  - open-weights
  - speech
  - asr
  - moe
  - nvidia
verification: confirmed
sources:
  - "@NVIDIAAI"
  - "https://x.com/AIEngineRoom/status/2115795597131178207"
  - "https://x.com/argofowl/status/2115793218868765039"
  - "https://x.com/kurahashi52173/status/2115792410701926718"
created_at: 2026-10-29
updated_at: 2026-10-29
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-29
    change: "Created — RELEASED / confirmed. @NVIDIAAI (2026-10-28 15:14 UTC) introduced Nemotron 3.5 Transcribe, an open-weight, promptable 30B-total / ~4B-active MoE speech model. It covers transcription in 40 languages, speaker attribution, translation, contextual prompting and audio understanding in one checkpoint. Secondary accounts report a 5.33% WER, first among open weights on the Hugging Face English ASR board, and early local use. Part of the Nemotron 3.5 wave with [[nvidia-nemotron-3-5-super-vl-2026-10]] and [[nvidia-nemotron-3-5-bolt-2026-10]]."
---
Nemotron 3.5 Transcribe brings NVIDIA's Nemotron 3.5 open-weight family to speech. It is a sparse MoE: 30B total
parameters with about 4B active. That gives it the compute cost of a small model while claiming one checkpoint
for transcription, diarization and translation.

The open-ASR-leaderboard placement is the claim most worth checking. It comes from a secondary account, not NVIDIA's
post. Early users are already running quantized builds locally, for example as the fallback transcriber in a
video-summarization CLI.

Related: [[nvidia-nemotron-3-5-super-vl-2026-10]], [[nvidia-nemotron-3-5-bolt-2026-10]].
