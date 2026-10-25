---
slug: dessa
title: Dessa
type: entity
aliases: ["Dessa", "Block Dessa", "Block's Dessa"]
tags: [speech-to-speech, voice-model, local-inference, open-weights-promised, block]
description: Block's speech-only voice model; trained from scratch on conversation, runs locally on a MacBook Pro M4 Max, with weights promised but not shipped.
created_at: 2026-10-25
timestamp: 2026-10-25T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-25", path: research/digest/2026-10-25-digest.md}
---

**Dessa** is Block's audio-native voice
model. It is trained only on human
speech — no text, no ASR step, no
pretrained checkpoint — and is not
public yet. Jack Dorsey has said the
weights will be released. The model
became the #1 AI story on Hacker News
overnight on 2026-10-25 after a
late-Saturday surge (498 points / 188
comments).

## Why it matters

- **Speech-to-speech without a text
  intermediate.** Dessa backchannels
  in real time and picks its own
  voice. That is a different bet
  from the live-dialogue APIs on
  [[gemini-3-8-live]] and
  [[mistral|Voxtral 3]]: those
  systems sit on a text stack.
  Commenters asked whether a
  speech-only model without world
  knowledge is a dead end (Hacker
  News, TechCrunch, The Decoder;
  ARA daily digest 2026-10-25).
- **Local inference is the demo,
  not the training budget.**
  Inference is faster than real
  time on a MacBook Pro M4 Max
  ([[apple]]). Training used one
  [[nvidia|NVIDIA]] GB200 NVL72
  rack, which HN commenters priced
  at about **$4–6 million** and
  flagged as not exactly "indie"
  (Hacker News; ARA daily digest
  2026-10-25).
- **Weights are promised, not
  shipped.** Safety researchers
  are invited for early access.
  Until the checkpoint lands, this
  is the same
  [[open-weights|weights-promised]]
  gap the wiki already tracks on
  [[moonshot-kimi-k3|Kimi K3.1
  Pro]] and
  [[minimax-m3-1-flash]]
  (The Decoder; ARA daily digest
  2026-10-25).

## Open questions

- **Do the weights actually ship,
  and under what license?**
- **Does a conversation-only
  training set stay useful once
  callers need world knowledge,
  or is the no-text constraint a
  ceiling?**
- **Is one GB200 NVL72 rack a
  reproducible recipe**, or a
  one-off that does not travel
  to labs without that hardware?
