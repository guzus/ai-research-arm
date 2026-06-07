---
slug: xai-claude-training-cutoff-2026-06
title: xAI reportedly trained coding models on Claude outputs, kept going after Anthropic cut access
company: xAI
model: null
status: confirmed
status_note: |
  The Decoder (2026-06-06) reports **xAI used Anthropic's Claude to train its
  own coding models for months** and **continued even after Anthropic cut off
  access**, routing around the block via **private accounts and the Blackbox AI
  service**. The same reporting says xAI's **pretraining team has shrunk
  significantly, with several leads departing**. This is an IP/competitive-ethics
  controversy plus a roadmap-relevant talent signal. Reported by a secondary
  outlet relaying prior reporting; no xAI/Anthropic primary statement or legal
  filing → confirmed event (multi-detail report) but verification partial.
expected: "No formal legal action reported as of 2026-06-07"
labels:
  - xai
  - anthropic
  - ip-controversy
  - distillation
  - personnel
verification: partial
sources:
  - https://the-decoder.com/elon-musks-xai-reportedly-trained-its-coding-models-on-claude-outputs-for-months-before-getting-cut-off/
created_at: 2026-06-07
updated_at: 2026-06-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-07
    change: "Created — The Decoder (2026-06-06) reports xAI trained its coding models on Anthropic's Claude outputs for months and kept going after Anthropic cut off access, using private accounts and the Blackbox AI service; xAI's pretraining team reportedly shrank with several leads departing. IP/ethics controversy + roadmap-relevant talent signal; secondary outlet, no primary/legal filing → confirmed event / partial"
---

The Decoder reported (2026-06-06) that **Elon Musk's xAI trained its own coding
models on Anthropic's Claude outputs for months**, and **kept doing so even
after Anthropic cut off access** — reportedly routing around the block via
**private accounts and the Blackbox AI service**. The same reporting notes
xAI's **pretraining team has shrunk significantly, with several leads
departing**.

**Why this is a ticket.** It combines two event classes this timeline tracks:
an **IP / competitive-ethics controversy** (distilling a rival's frontier model
in violation of access terms) and an **exec/roadmap signal** (a thinning
pretraining org). It is directly relevant to xAI's coding-model surface — see
the [xai-grok-build-2026-05](./xai-grok-build-2026-05.md) `grok-build-0.1`
ticket, which is the public-facing coding model the underlying training
practices feed.

**Why `confirmed` event / `partial` verification.** The report is detailed and
specific (mechanism, the Blackbox workaround, named team attrition), which is
more than a single-tweet tease — but it is **secondary reporting** with **no
xAI or Anthropic on-record statement and no legal filing**. It mirrors the
broader cycle's training-provenance scrutiny (cf. The Decoder's 2026-06-05
report that **Microsoft trained its MAI models on unlicensed web data**).

**Transition triggers:**
- An on-record xAI or Anthropic statement, or a **formal legal action** (cease
  & desist, suit) → UPDATE, advance verification (a suit may warrant a
  successor legal-action ticket back-linking here).
- Additional named departures or confirmation of the pretraining-team
  contraction → UPDATE the talent vector in history.
- Story denied or retracted → `closed` with the appropriate reason.

**Dedup note:** further xAI-trained-on-Claude / Blackbox-workaround /
pretraining-attrition signal UPDATES this ticket. xAI's shipping coding model
stays on [[xai-grok-build-2026-05]]; the 1.5T frontier model stays on
[[grok-v9-medium]].
