---
slug: sina-vibethinker-3b-2026-06
title: VibeThinker-3B — 3B open model matching frontier math/coding via post-training
company: Sina Weibo
model: VibeThinker-3B
status: released
status_note: |
  **VibeThinker-3B** (Sina Weibo) is a **3B-parameter** open model reported to
  match **DeepSeek V3.2 / Kimi K2.5** on math and coding while being **up to
  333× smaller**, achieved via a **multi-stage post-training** recipe. The
  framing claim — surfaced via the 2026-06-29 digest's Model Releases / Research
  section (The Decoder) — is that **logical reasoning compresses well into a
  small model while factual knowledge does not**, making it a data point in the
  "small-model reasoning" thesis rather than a general-purpose frontier
  contender. Usable now (open model) → status `released`; in-window sourcing is
  a single secondary outlet (The Decoder) without a captured primary model card
  or neutral third-party benchmark reproduction → verification `partial`.
expected: "Open model released; primary model card + neutral third-party reproduction of the DeepSeek V3.2 / Kimi K2.5-parity math/coding claims pending"
labels:
  - released
  - open-weights
  - small-model
  - reasoning
  - math
  - coding
  - china
verification: partial
sources:
  - https://the-decoder.com/sinas-open-model-vibethinker-3b-aims-to-show-reasoning-compresses-well-but-factual-knowledge-doesnt
created_at: 2026-06-29
updated_at: 2026-06-29
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-29
    change: "Created — VibeThinker-3B (Sina Weibo), a 3B open model reported to match DeepSeek V3.2 / Kimi K2.5 on math and coding while up to 333× smaller, via a multi-stage post-training recipe. Hypothesis it illustrates: logical reasoning compresses well into a small model, factual knowledge doesn't. Surfaced via the 2026-06-29 digest (The Decoder). Open model usable now → status released; single secondary outlet without a captured primary model card or neutral benchmark reproduction → verification partial."
---

**VibeThinker-3B**, from **Sina Weibo**, is a **3-billion-parameter** open
model reported to match **DeepSeek V3.2** and **Kimi K2.5** on math and
coding benchmarks while being **up to 333× smaller**, achieved through a
**multi-stage post-training** pipeline rather than scale.

**Why its own ticket.** It is a discrete open-model release — the event
class this timeline tracks. It sits alongside the cycle's other
open-weight contenders ([[zhipu-glm-5-2]], [[minimax-m3]],
[[nvidia-nemotron-openrouter-2026-06]]) but carries a distinct thesis:
the team frames it as evidence that **logical reasoning compresses well
into a small model while factual knowledge does not** — a small-model
reasoning data point, not a general-purpose frontier model.

**Why `released` / `partial`.** As an open model it is usable now →
`released`. In-window sourcing is a **single secondary outlet** (The
Decoder) with no captured primary model card and no neutral third-party
reproduction of the parity claims → `verification: partial`. A primary
release page or an independent benchmark re-run would advance it to
`confirmed`.

**Transition triggers:**
- Primary model card / repo, or neutral third-party reproduction of the
  DeepSeek V3.2 / Kimi K2.5-parity math/coding numbers → UPDATE, advance
  `verification`.
- A successor / larger VibeThinker variant → new ticket, link back here.
- ≥4 weeks past release settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further VibeThinker-3B release/benchmark signal UPDATES
this ticket. Other small/open models stay on their own tickets.
