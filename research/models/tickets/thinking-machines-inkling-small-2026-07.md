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
expected: "Released, and as of 2026-08-21 served directly by Thinking Machines on OpenRouter free inside agentic harnesses, explicitly to collect real-world agentic behavior. Pending: whether free access is time-boxed, published agentic results from the collected data, and pricing when it ends"
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
  - "@OpenRouter"
  - "@soumithchintala"
created_at: 2026-07-31
updated_at: 2026-08-23
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-31
    change: "Created — Thinking Machines released Inkling-Small (276B-total/12B-active MoE), claimed comparable performance to the full Inkling (975B-total/41B-active, [[thinking-machines-inkling]]) at a quarter of the size, full weights made available. Official @thinkymachines primary + Hugging Face RT, corroborated by @kimmonismus, @testingcatalog, @AndrewCurran_ → status released, verification confirmed. Treated as a distinct shipping artifact from the original Inkling ticket rather than an update, since it is a separately-launched, differently-sized sibling model with its own release event."
  - ts: 2026-08-23
    change: "Distribution widens and the motive is stated outright. @OpenRouter (2026-08-21, relayed by @soumithchintala): 'Inkling and Inkling Small are now served directly by @thinkymachines on OpenRouter, free to use inside agentic harnesses.' @thinkymachines' own account gives the reason in the same window: 'We want to improve Inkling's agentic performance. To help us understand its real-world behavior, we are making it available...' — i.e. free serving as behavioral data collection, which is the same trade Meta made explicit with its Muse Spark contributor tier ([[meta-hatch-muse-spark-2026-06]]) the same day. Served directly by the lab rather than a third-party host, so latency and quality are the lab's own. Status stays released; verification stays confirmed (lab-primary post). Pending: whether free access is time-boxed, and any published agentic benchmarks from the collected data."
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
