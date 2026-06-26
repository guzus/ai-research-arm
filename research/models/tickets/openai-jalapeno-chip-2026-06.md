---
slug: openai-jalapeno-chip-2026-06
title: OpenAI Jalapeño — first custom inference ASIC (with Broadcom)
company: OpenAI
model: Jalapeño
status: in-testing
status_note: |
  OpenAI unveiled its **first custom AI chip**, **Jalapeño**, on 2026-06-24
  (@OpenAI 13:10 UTC, ~20.7K–21.5K likes): "We've designed and built our first
  AI chip: Jalapeño. Designed from the ground up by OpenAI and brought to
  production with Broadcom." **Inference-only** (no claimed training capability).
  Broadcom CEO **Hock Tan** told Bloomberg early testing shows **~50% cost
  savings per inference token vs standard GPUs**, and told Reuters performance
  is "on par with NVIDIA Blackwell and Google TPUs" — the 50% figure is
  Broadcom's claim, not OpenAI's (OpenAI's own language hedges to "substantially
  better than state-of-the-art"). Claimed a **9-month design-to-tape-out**
  (accelerated by OpenAI's own models designing the chip); **3nm TSMC
  engineering samples** hand-delivered to Sam Altman and Greg Brockman by
  Broadcom's CEO. Microsoft reportedly guaranteed **~40% of initial output**
  (The Decoder, unconfirmed by either company). Prototype deployment **late
  2026**, ramps **2027–2028**, targeting gigawatt-scale data centers.
  Lands the same week as NVIDIA's open-sourced DFlash speculative-decoding
  ([[nvidia-dflash-2026-06]]) — competing answers to dropping inference cost.
expected: "Prototype deployment late 2026, ramp 2027–2028, gigawatt-scale DCs; 3nm TSMC engineering samples now. Microsoft ~40% of initial output reported but unconfirmed"
labels:
  - hardware
  - inference-asic
  - openai
  - broadcom
  - in-testing
verification: confirmed
sources:
  - https://x.com/OpenAI/status/2069770172802773292
  - "@OpenAI"
  - "@TheValueist"
  - "@OwenGregorian"
created_at: 2026-06-26
updated_at: 2026-06-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-26
    change: "Created — OpenAI unveiled Jalapeño, its first custom AI inference ASIC, on 2026-06-24 (@OpenAI 13:10 UTC, ~20.7K–21.5K likes), designed in-house and brought to production with Broadcom. Inference-only. Broadcom CEO Hock Tan told Bloomberg ~50% cost savings per inference token in early testing vs GPUs, and told Reuters performance 'on par with NVIDIA Blackwell and Google TPUs' (the 50% is Broadcom's claim, not OpenAI's — OpenAI hedges to 'substantially better'). 9-month design-to-tape-out (AI-assisted chip design); 3nm TSMC engineering samples hand-delivered to Altman/Brockman; Microsoft reportedly guaranteed ~40% of initial output (The Decoder, unconfirmed). Prototype deployment late 2026, ramps 2027–2028. Real artifact (engineering samples) but not yet deployed at scale → status in-testing; verification confirmed (official @OpenAI post + Broadcom CEO on-record to Bloomberg/Reuters). Pairs with NVIDIA DFlash ([[nvidia-dflash-2026-06]] as competing inference-cost answers; analyst framing is pricing-power erosion for NVIDIA, not displacement."
---

**Jalapeño** is **OpenAI's first custom AI chip**, unveiled 2026-06-24 and
designed from the ground up by OpenAI with **Broadcom** bringing it to
production. It is **inference-only** — OpenAI makes no training-capability
claim — and is positioned as a vertical-integration move to reduce OpenAI's
dependency on NVIDIA GPUs at the inference layer.

**What's confirmed vs. claimed.** The announcement itself is first-party
(@OpenAI's official post, ~20.7K–21.5K likes) and Broadcom CEO **Hock Tan**
went on-record to Bloomberg and Reuters. That makes the *existence* of the
chip and the partnership `confirmed`. The headline economics — **~50% cost
savings per inference token** — is **Tan's claim, not OpenAI's**: OpenAI's
own statement notably hedges to "substantially better than state-of-the-art,"
unusual language for a flagship product launch. Treat the 50% as
Broadcom-sourced and unvalidated at production scale.

**Timeline.** Engineering samples (3nm TSMC) exist now and were hand-delivered
to Altman and Brockman, which is why this is `in-testing` rather than
`rumored`/`confirmed`-only. Meaningful deployment is **18+ months out**
(prototype late 2026, ramp 2027–2028). A reported **Microsoft guarantee of
~40% of initial output** (The Decoder) is unconfirmed by either company.

**Why it matters.** The honest analyst framing (@TheValueist) is that
Jalapeño is a **pricing-power erosion signal** for NVIDIA, not a displacement
event — inference-only, far from scale, with a Broadcom-CEO cost number and
no disclosed baseline. But the **9-month AI-assisted design cycle** is an
underappreciated proof point: it suggests OpenAI can iterate hardware fast
enough to make multi-generational improvements credible. It lands alongside
NVIDIA's open-sourced **DFlash** speculative decoding
([[nvidia-dflash-2026-06]]) — two competing answers to whether inference cost
can keep dropping fast enough to sustain demand growth.

**Transition triggers:**
- A technical report with benchmark numbers, or Microsoft's 40% guarantee
  confirmed → UPDATE, append history.
- Production deployment / first customer traffic → advance toward `released`.
- Abandoned or spun into a different silicon program → close per reason.

**Dedup note:** Jalapeño hardware signal (specs, deployment, benchmarks)
UPDATES this ticket. OpenAI's broader compute/datacenter buildout stays on
its own relevant tickets.
