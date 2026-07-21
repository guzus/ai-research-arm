---
slug: motif-3-beta-2026-07
title: Motif-3-Beta open-weight release
company: Motif Technologies
model: Motif-3-Beta
status: released
status_note: |
  Sparse MoE, ~314B total / ~13B active parameters, 256K native context.
  Weights live on Hugging Face; no official company blog post surfaced yet,
  but the artifact itself is downloadable.
expected: null
labels:
  - open-weight
  - moe
verification: confirmed
sources:
  - https://x.com/_akhaliq/status/2079377502565179556
  - https://x.com/TheCrawlHub/status/2079484564406222999
  - "@huggingface"
created_at: 2026-07-21
updated_at: 2026-07-21
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-21
    change: Created — Motif-3-Beta (~314B total / ~13B active MoE, 256K context) appeared on Hugging Face, corroborated by multiple independent accounts.
---

Motif-3-Beta is a sparse mixture-of-experts model from Motif Technologies
(a Korean AI lab) that surfaced on Hugging Face with roughly 314B total
parameters and ~13B active per token, plus a 256K native context window.
Several independent accounts (including HuggingFace's own amplification)
flagged it the same day, describing it as performing on par with larger
models despite the much smaller active-parameter count.

No press release or company blog post has surfaced yet — the primary
evidence is the live Hugging Face listing itself. Worth watching for
benchmark corroboration and an official announcement in the next cycle.
