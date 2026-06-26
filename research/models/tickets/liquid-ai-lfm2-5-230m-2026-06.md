---
slug: liquid-ai-lfm2-5-230m-2026-06
title: Liquid AI LFM2.5-230M — smallest-yet on-device model
company: Liquid AI
model: LFM2.5-230M
status: released
status_note: |
  Liquid AI launched **LFM2.5-230M** on SGLang via LMSYS on 2026-06-26
  (@lmsysorg, ~27 likes) — its **smallest model yet at 230M parameters**,
  aimed at **on-device deployment**. Low-engagement, single-relay coverage,
  but a genuine model release in the "efficient frontier" / on-device thread.
  Joins the set of small/efficient open models tracked in this lane
  ([[xiaomi-mimo-code-2026-06]], [[cohere-bls-mini-code-1]],
  [[sakana-fugu-2026-06]]). No benchmarks, pricing, or architecture detail in
  this window beyond the parameter count and the on-device framing.
expected: null
labels:
  - liquid-ai
  - small-model
  - on-device
  - open-weights
  - released
verification: partial
sources:
  - https://x.com/lmsysorg/status/2070168574849945721
  - "@lmsysorg"
created_at: 2026-06-26
updated_at: 2026-06-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-26
    change: "Created — Liquid AI launched LFM2.5-230M on SGLang via LMSYS on 2026-06-26 (@lmsysorg ~27 likes): its smallest model yet at 230M params, for on-device deployment. Launched and usable → status released; verification partial (single low-engagement relay via @lmsysorg; no benchmarks/pricing/architecture detail in window). Joins the small/efficient-model set ([[xiaomi-mimo-code-2026-06]], [[cohere-bls-mini-code-1]], [[sakana-fugu-2026-06]])."
---

**Liquid AI** launched **LFM2.5-230M** — its **smallest model yet at 230M
parameters** — on SGLang via LMSYS on 2026-06-26, aimed at **on-device
deployment**. It is a genuine model release in the "efficient frontier" /
on-device thread, though the in-window coverage was low-engagement and
single-source.

**Why `released` / `partial`.** The model is launched and usable on SGLang →
`released`. `verification: partial` because the signal is a single
low-engagement relay (@lmsysorg, ~27 likes) with no benchmarks, pricing, or
architecture detail in this window beyond the parameter count and the
on-device framing. LMSYS is a credible org account, but corroboration is thin.

**Context.** Joins the set of small/efficient open models this lane tracks
alongside [[xiaomi-mimo-code-2026-06]], [[cohere-bls-mini-code-1]], and
[[sakana-fugu-2026-06]] — the on-device / efficient-model tier that runs in
parallel to the frontier-weight story.

**Transition triggers:**
- Benchmarks, architecture detail, or broader deployment data → UPDATE, append
  history.
- A successor LFM point release → new ticket.
- ≥4 weeks past release, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further LFM2.5-230M signal (benchmarks, adoption, architecture)
UPDATES this ticket. Other small/efficient models stay on their own tickets.
