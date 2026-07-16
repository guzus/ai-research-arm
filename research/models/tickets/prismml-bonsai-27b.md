---
slug: prismml-bonsai-27b
title: PrismML releases Bonsai 27B, a 1-bit-quantized model claimed to run on a phone
company: PrismML
model: Bonsai 27B
status: released
status_note: |
  Technical-report release, trending on **Papers with Code** and
  **Hugging Face**. Claimed to be the first 27B-class model able to run
  on a phone via **1-bit quantization**, shrinking footprint from **54GB
  to 3.8GB** at **~90% retained quality** per the reported technical
  evaluation. Corroborated by **@HuggingFace** and ML researcher
  **@NielsRogge**; no primary PrismML statement/blog located in this
  pass, hence verification `partial` not `confirmed`.
expected: null
labels:
  - open-weights
  - efficiency
  - mobile
verification: partial
sources:
  - "@HuggingFace"
  - https://x.com/HuggingFace/status/2077164993989017668
  - "@NielsRogge"
created_at: 2026-07-16
updated_at: 2026-07-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-16
    change: "Created — PrismML released Bonsai 27B, a 1-bit-quantized 27B-class model claimed to run on a phone, shrinking footprint from 54GB to 3.8GB at ~90% retained quality per the reported technical evaluation. Technical-report release, trending on Papers with Code and Hugging Face; corroborated by @HuggingFace and ML researcher @NielsRogge → status released. No primary PrismML statement/blog located in this pass → verification partial."
---

**PrismML** released **Bonsai 27B**, claimed to be the first **27B-class
model** able to run on a phone via **1-bit quantization**. The reported
technical evaluation shows the footprint shrinking from **54GB to
3.8GB** while retaining **~90% of quality** versus the unquantized
model. The release is a technical report, currently trending on
**Papers with Code** and **Hugging Face**.

**Why tracked.** Aggressive quantization enabling a 27B-class model to
run on-device is directly relevant to the ongoing efficiency/mobile-AI
storyline (alongside other open-weights efficiency releases this desk
tracks) and worth watching for independent quality validation.

**Corroboration read.** The release and its headline claims are
corroborated by **@HuggingFace** (the platform's own account, reflecting
real trending activity) and independent ML researcher **@NielsRogge** —
enough secondary corroboration for `status: released` given it's a
live, downloadable artifact. No primary PrismML blog post, model card,
or company statement was located in this pass, so `verification` stays
`partial` rather than `confirmed`.

**Transition triggers:**
- A primary PrismML statement, blog post, or model card → UPDATE,
  advance `verification` to `confirmed`.
- Independent third-party benchmarks validating (or contradicting) the
  ~90%-retained-quality claim → UPDATE.
- ≥4 weeks past release, settled into normal coverage → `closed:
  released-and-aged`.

**Dedup note:** further Bonsai 27B signal (benchmarks, follow-on
versions, primary confirmation) UPDATES this ticket.
