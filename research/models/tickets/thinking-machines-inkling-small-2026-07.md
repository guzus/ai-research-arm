---
slug: thinking-machines-inkling-small-2026-07
title: Thinking Machines ships Inkling-Small, a quarter-size open-weight sibling to Inkling
company: Thinking Machines
model: Inkling-Small
status: released
status_note: |
  @thinkymachines (official, primary): "Today, we are releasing
  Inkling-Small. Inkling-Small achieves comparable performance to Inkling
  at a quarter of its size. It features 276B total parameters, 12B active.
  We are making the full weights available." Distinct shipping artifact
  from [[thinking-machines-inkling]] (975B-total/41B-active) — a
  separately-launched, differently-sized open-weight sibling model, not a
  version bump of the same weights. Corroborated by a Hugging Face RT plus
  @kimmonismus, @testingcatalog, @AndrewCurran_.
expected: null
labels:
  - open-weights
  - multimodal
  - thinking-machines
  - released
verification: confirmed
sources:
  - "@thinkymachines"
  - "@kimmonismus"
  - "@testingcatalog"
  - "@AndrewCurran_"
created_at: 2026-07-31
updated_at: 2026-07-31
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-31
    change: "Created — Thinking Machines released Inkling-Small (276B-total/12B-active MoE), claimed comparable performance to the full Inkling (975B-total/41B-active, [[thinking-machines-inkling]]) at a quarter of the size, full weights made available. Official @thinkymachines primary + Hugging Face RT, corroborated by @kimmonismus, @testingcatalog, @AndrewCurran_ → status released, verification confirmed. Treated as a distinct shipping artifact from the original Inkling ticket rather than an update, since it is a separately-launched, differently-sized sibling model with its own release event."
---

**Thinking Machines** released **Inkling-Small**, a smaller open-weight
sibling to its earlier **Inkling** release
([[thinking-machines-inkling]]). Per the company's own account:
"Inkling-Small achieves comparable performance to Inkling at a quarter of
its size" — **276B total parameters, 12B active** (vs Inkling's
975B-total/41B-active), with **full weights made available**.

**Why its own ticket, not an update to [[thinking-machines-inkling]].**
Inkling-Small is a materially different shipping artifact: a distinct
size class, a separate open-weight release event, and its own launch
announcement roughly two weeks after the original Inkling — not a
version-number drift or patch of the same weights. This mirrors how other
distinctly-sized sibling releases in this ticket set (e.g. separate
tickets per Alibaba Qwen size tier) are tracked independently rather than
folded into the flagship's history.

**Transition triggers:**
- Independent benchmark results (positive or negative) comparing
  Inkling-Small to Inkling or competing open models → UPDATE.
- ≥4 weeks past release, settled into normal coverage → `closed:
  released-and-aged`.

**Dedup note:** further Inkling-Small signal (benchmarks, ecosystem
adoption) UPDATES this ticket. The full-size Inkling stays on
[[thinking-machines-inkling]].
