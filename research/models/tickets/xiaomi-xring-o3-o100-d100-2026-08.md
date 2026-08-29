---
slug: xiaomi-xring-o3-o100-d100-2026-08
title: Xiaomi unveils three Xring chips — O3 flagship SoC, O100 on-device-LLM accelerator, D100 for driving
company: Xiaomi
model: null
status: confirmed
status_note: |
  Xiaomi unveiled **three Xring chips at once** (@ZionsAnvin and
  @bytelee_trade, 2026-08-24; specs echoed by @search-model-release):

  - **Xring O3** — flagship mobile SoC on a **3nm** process: 10-core CPU
    (**+60%**), 16-core G2-Ultra NX GPU (**up to +85%**, **+64%** power
    efficiency), **first mobile chip with LPDDR6**, up to **113.8 GB/s**
    memory bandwidth, **200 TOPS** tensor / **3.13 TFLOPS** vector AI,
    **NPU +45%**, 82ns static latency, developed over 459 days, claimed
    first past **5M on AnTuTu**. Ships in the **Xiaomi 18 Fold** and
    **Pad 9 Pro Max** in **September**.
  - **Xring O100** — **6nm**, wafer-level vertical stacking, a
    **near-memory AI architecture** aimed explicitly at **on-device
    large models** and the memory wall.
  - **Xring D100** — **3nm**, for intelligent driving. Xiaomi says
    development is complete; **commercialization planned for next year**.

  Status `confirmed`: a product unveiling with dated availability, named
  devices and a detailed spec sheet, carried consistently by two
  independent accounts plus a third relay. Verification `partial`: **no
  Xiaomi primary post, launch page, or press release was captured**, and
  every number here — including the AnTuTu claim and the "+60%/+85%"
  deltas — is a vendor figure passed through relays, not an independent
  measurement.

  **The O100 is the one that belongs in a model lane.** A 6nm
  near-memory part built specifically for on-device LLM inference is a
  bet that a meaningful share of model serving moves to the handset —
  the same bet visible in Google shipping **gemma-4-e2b-it** to run
  fully offline through AI Edge Gallery ([[gemma-4]]) and in Xiaomi's own
  MiMo line ([[xiaomi-mimo-v2-5-pro]]). Xiaomi is now the rare company
  positioned to co-design the model and the silicon it runs on.

  **2026-08-25 — the memory supplier is named, and the O100 got a
  demonstrated system.**

  *Supply chain.* @jukan05 (2026-08-25 06:56 UTC): "According to Chinese
  media reports, **CXMT is expected to be a key supplier of LPDDR6 for
  Xiaomi's new Xring O3 chip.**" @tphuang gives the technical detail
  behind it — after the O3 became the first SoC to support LPDDR6 at
  **10,667 Mbps / 113.8 GB/s**, CXMT was revealed as supplier; CXMT's
  LPDDR6 has a **designed ceiling of 12,800 Mbps** but runs at the 10,667
  base with this SoC, **16 Gb single die, 16 GB chip**. @teortaxesTex
  flags the schedule tension honestly: "We were supposed to get CXMT's
  LPDDR6 by end of 2026. Is this the end of year already?" — i.e. either
  CXMT pulled in its schedule or the parts are early samples, and nothing
  captured distinguishes those.

  **Why this is the most consequential detail on the ticket.** It makes
  the O3 an **end-to-end domestic part on its critical path** — Chinese
  SoC plus Chinese leading-edge DRAM — at the exact moment memory is the
  global bottleneck ([[nvidia-server-price-increase-2026-08]],
  [[nvidia-rubin-ultra-hbm-downgrade-2026-08]]) and the US is reported to
  be asking South Korea to build memory fabs on US soil. It also gives
  [[cxmt-ipo-debut-2026-07]] a named flagship customer.

  *System.* @mark_k (2026-08-24 15:45 UTC) reports a Xiaomi **"AI Cube"
  engineering prototype** packing **all three chips — Xring O3, O100 and
  D100 — together**, delivering up to **1.22 TB/s of near-memory
  bandwidth** and **150 W sustained**, demonstrated running **120B + 3B
  models entirely locally with a fast/slow model-switching
  architecture**. Explicitly **no price and no release date**. The
  fast/slow pairing is the notable part: it is speculative-decoding-shaped
  local serving designed into the silicon, which is what the O100's
  near-memory architecture was described as being for.

  Status stays `confirmed`; verification stays `partial` — still no Xiaomi
  primary post, and the AI Cube figures are a single relay of a prototype
  demo with no third-party measurement.
expected: "Unveiled 2026-08-24: Xring O3 (3nm flagship SoC, ships in Xiaomi 18 Fold and Pad 9 Pro Max in September), O100 (6nm near-memory accelerator for on-device LLMs), D100 (3nm driving, commercialization next year). Pending: a Xiaomi primary announcement, independent benchmarks against the vendor deltas and the 5M AnTuTu claim, O100 availability and which MiMo models it targets, and whether O100 ships in a shipping device at all"
labels:
  - xiaomi
  - china
  - silicon
  - on-device
  - edge-inference
verification: partial
sources:
  - "@jukan05"
  - "@tphuang"
  - "@teortaxesTex"
  - "@mark_k"
  - "@ZionsAnvin"
  - https://x.com/ZionsAnvin/status/2091783440601653386
  - "@bytelee_trade"
  - https://x.com/bytelee_trade/status/2091787209104052312
created_at: 2026-08-24
updated_at: 2026-08-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-24
    change: "Created — Xiaomi unveiled three Xring chips simultaneously (@ZionsAnvin, @bytelee_trade, 2026-08-24): Xring O3, a 3nm flagship SoC (10-core CPU +60%, 16-core G2-Ultra NX GPU up to +85%, first mobile part with LPDDR6, 113.8 GB/s, 200 TOPS tensor, NPU +45%, claimed first past 5M AnTuTu) shipping in the Xiaomi 18 Fold and Pad 9 Pro Max in September; Xring O100, a 6nm wafer-level-stacked near-memory accelerator aimed at on-device large models and the memory wall; and Xring D100, a 3nm intelligent-driving part with development complete and commercialization planned for next year. Status confirmed on a dated unveiling with named devices and a detailed spec sheet from two independent accounts; verification partial — no Xiaomi primary post captured and all figures are vendor-supplied. The O100 is the model-lane-relevant part: purpose-built on-device LLM silicon from a company that also ships the MiMo model line ([[xiaomi-mimo-v2-5-pro]])."
  - ts: 2026-08-25
    change: "Memory supplier named and the O100 got a demonstrated system. @jukan05 (2026-08-25 06:56 UTC) relays Chinese media reporting CXMT as a key LPDDR6 supplier for the Xring O3; @tphuang adds that after the O3 became the first SoC supporting LPDDR6 at 10,667 Mbps / 113.8 GB/s, CXMT was revealed as supplier, with a 12,800 Mbps design ceiling, 16 Gb single die and 16 GB chip. @teortaxesTex flags the schedule tension — CXMT LPDDR6 was expected end-2026 — which nothing captured resolves between a pulled-in schedule and early samples. Consequential because it makes the O3 an end-to-end domestic part on its critical path while memory is the global bottleneck ([[nvidia-server-price-increase-2026-08]], [[nvidia-rubin-ultra-hbm-downgrade-2026-08]]), and gives [[cxmt-ipo-debut-2026-07]] a named flagship customer. Separately @mark_k (2026-08-24 15:45 UTC) reports a Xiaomi AI Cube engineering prototype packing all three chips together at up to 1.22 TB/s near-memory bandwidth and 150W sustained, demonstrated running 120B + 3B models fully locally with a fast/slow model-switching architecture, with no price or release date — speculative-decoding-shaped local serving designed into the silicon, which is what the O100 was described as being for. Status stays confirmed; verification stays partial — still no Xiaomi primary post, and the AI Cube figures are a single relay of a prototype demo."
---

Xiaomi announced **three Xring parts in one event**, extending in-house
silicon from phones into on-device model inference and vehicles.

**The O3 is the headline and the least interesting entry here.** It is a
strong 3nm flagship SoC with a September ship date in named devices, and
its numbers — +60% CPU, +85% GPU, 200 TOPS, a claimed first-ever 5M
AnTuTu score — are all vendor deltas relayed secondhand. Treat them as
marketing until someone benchmarks the shipping Xiaomi 18 Fold.

**The O100 is why this ticket exists.** A 6nm part using wafer-level
vertical stacking and a near-memory architecture, aimed explicitly at
running large models on-device and at the memory wall, is a different
kind of claim than a faster NPU block. Memory bandwidth, not arithmetic,
is what bounds local LLM decode; a near-memory design is an attempt to
attack that bound directly. Whether it works is unknown — Xiaomi gave no
availability date and named no device for it.

**The strategic read is vertical integration of the whole stack.**
Xiaomi ships models ([[xiaomi-mimo-v2-5-pro]],
[[xiaomi-robotics-1-2026-07]]), phones, tablets and cars, and now
designs the silicon under all four. @bytelee_trade's framing is the
useful one: the change is not a benchmark score but chip development
moving from a cost centre to a platform capability shared across
handsets, on-device models and vehicles.

**Context that cuts against the timing.** This lands in the middle of a
memory-cost squeeze severe enough to push Nvidia's server prices up
~17% ([[nvidia-server-price-increase-2026-08]]) and, per the same
window's reporting, to raise iPhone 18 Pro pricing. A first-to-LPDDR6
flagship and a wafer-stacked near-memory part are both bets placed
directly into the tightest memory market in years.

Related: [[huawei-tau-scaling-law-2026-05]], [[gemma-4]],
[[cxmt-ipo-debut-2026-07]].
