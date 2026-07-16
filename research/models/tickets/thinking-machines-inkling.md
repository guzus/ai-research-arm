---
slug: thinking-machines-inkling
title: Thinking Machines ships Inkling, a 975B-parameter open-weights multimodal model
company: Thinking Machines
model: Inkling
status: released
status_note: |
  Released **2026-07-15** via a Thinking Machines team member's own
  account (**@soumithchintala**) plus **Tinker's** official account,
  independently corroborated within 15 minutes by **@ns123abc** and
  **@kimmonismus**. **975B-total / 41B-active MoE**, natively
  multimodal (text/image/audio), up to **1M context**, trained from
  scratch on GB300s (~45T tokens), open weights on **Tinker** + Hugging
  Face (Apache-licensed per community reports).

  **Caveat (within 24h):** independent researchers **Ethan Mollick
  (@emollick)** and **Jonas Jitsev (@JJitsev)** reported it underperforming
  launch-day billing — struggling on basic reasoning tests, lagging
  GLM 5.2 on the TB 2.1 benchmark — even as HuggingFace/Unsloth/Modal
  shipped fast ecosystem support (trending, quantized versions,
  accelerated hosting). Treat the launch specs as confirmed and the
  quality claims as contested pending more independent evals.
expected: null
labels:
  - open-weights
  - multimodal
  - frontier-model
verification: confirmed
sources:
  - "@soumithchintala"
  - https://x.com/soumithchintala/status/2077457110728884327
  - "@ns123abc"
  - https://x.com/ns123abc/status/2077472600196788351
  - "@kimmonismus"
  - https://x.com/kimmonismus/status/2077472478499053846
  - "@emollick"
  - https://x.com/emollick/status/2077593908540850491
  - "@JJitsev"
  - https://x.com/JJitsev/status/2077670736462750106
created_at: 2026-07-16
updated_at: 2026-07-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-16
    change: "Created — Thinking Machines released Inkling, a 975B-total/41B-active MoE, natively multimodal (text/image/audio) model with up to 1M context, trained from scratch on GB300s (~45T tokens), open-weighted on Tinker + Hugging Face. Announced 2026-07-15 by @soumithchintala and Tinker's official account, corroborated within 15 minutes by @ns123abc and @kimmonismus → status released, verification confirmed. Within 24h, @emollick and @JJitsev independently reported it underperforming on basic reasoning tests and lagging GLM 5.2 on TB 2.1, even as HuggingFace/Unsloth/Modal shipped fast ecosystem support."
---

On **2026-07-15**, **Thinking Machines** shipped **Inkling**, a
**975B-total-parameter / 41B-active MoE** model, announced by team
member **@soumithchintala** and Tinker's official account. It is
**natively multimodal** (text, image, audio), supports **up to 1M
context**, was **trained from scratch on GB300s** (~45T tokens), and
ships as **open weights** on **Tinker** and Hugging Face
(Apache-licensed per community reports). Independent accounts
**@ns123abc** and **@kimmonismus** corroborated the release within 15
minutes of the initial post.

**Why tracked.** This is Thinking Machines' first frontier-scale
open-weights release — a large natively-multimodal MoE from a lab whose
prior public output had been comparatively narrow. The scale (975B
total) and open-weights posture make it immediately relevant to the
open-model competitive landscape alongside DeepSeek, GLM, and Kimi.

**Corroboration read.** The launch specs (parameter count, context
window, training compute, license) come from the team's own account and
Tinker's official account, corroborated by two independent
well-followed AI-news accounts within minutes → `status: released`,
`verification: confirmed` for the release itself.

**Caveat — quality claims contested.** Within 24 hours, independent
researchers **Ethan Mollick (@emollick)** and **Jonas Jitsev
(@JJitsev)** separately reported the model underperforming its
launch-day billing: struggling on basic reasoning tests and lagging
GLM 5.2 on the TB 2.1 benchmark. This tension — strong ecosystem uptake
(HuggingFace/Unsloth/Modal shipping quantized versions and accelerated
hosting within a day) against weak independent quality signal — is
worth tracking as its own thread rather than either dismissing the
release or taking the launch framing at face value.

**Transition triggers:**
- Further independent benchmark results (positive or negative) → UPDATE
  `status_note`.
- An official Thinking Machines blog post / model card with published
  benchmarks → UPDATE, may firm quality claims either way.
- ≥4 weeks past release, settled into normal coverage → `closed:
  released-and-aged`.

**Dedup note:** further Inkling signal (benchmarks, ecosystem support,
follow-on versions) UPDATES this ticket. Distinct from any prior
Thinking Machines Tinker-platform tickets, if any exist — this ticket
tracks the model artifact specifically.
