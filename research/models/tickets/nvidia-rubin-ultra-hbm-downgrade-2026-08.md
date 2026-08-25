---
slug: nvidia-rubin-ultra-hbm-downgrade-2026-08
title: SemiAnalysis reports Rubin Ultra HBM content cut to 192GB, below regular Rubin
company: NVIDIA
model: null
status: confirmed
status_note: |
  **@SemiAnalysis_ (2026-08-24 21:00 UTC, ~1K likes / 82 RT), tagged "HBM
  MASSIVE CONTENT DOWNGRADE ALERT":** "**Nvidia Rubin Ultra will ship with
  192GB of HBM4 8-hi.** Not only is this a huge downgrade from the
  original Rubin Ultra which was previewed with **1TB of HBM**, but it is
  even **lower than regular Rubin which has 288GB**."

  **The stated mechanism is a chain of three separate cuts**, which is why
  the total lands at roughly a fifth of the preview:

  1. **Cube count cut to 8** when the **4-die Rubin Ultra was scrapped**.
  2. **Stack height reduced to 8-hi** instead of 16-hi.
  3. **HBM4 with 24Gb dies** instead of HBM4E with 32Gb dies — SemiAnalysis
     notes an 8-hi HBM4E upgrade "could come later."

  SemiAnalysis says it first broke this to subscribers in **July** via its
  Accelerator Model and is publishing the headline now.

  Status `confirmed`: a specialist research desk with a paid accelerator
  model, publishing a specific spec with a decomposed causal chain and a
  disclosed prior-publication date. Verification `partial`: **no NVIDIA
  statement, no roadmap slide, and no second independent source** —
  everything traces to one desk, and the detailed part (implications,
  NVIDIA's offsets, where HBM specs head next) sits behind their paywall
  and was not read.

  **The market read, and the pushback.** @scaling01 (~490 likes):
  "bearish as fuck — we are going to be stuck on small ass models forever,"
  since HBM capacity per package bounds the parameter count that fits
  without cross-node traffic. He then argued the opposite himself hours
  later: "Cerebras and Groq are just chaining together dozens, hundreds or
  even thousands of chips — if we want to scale to 100T models we could
  just do it today." Both are on the record; this ticket records the
  disagreement rather than picking a side.
expected: "Reported 2026-08-24 by SemiAnalysis: Rubin Ultra to ship with 192GB HBM4 8-hi vs 1TB previewed and 288GB on regular Rubin, after the 4-die variant was scrapped, stacks cut to 8-hi, and HBM4E 32Gb dies swapped for HBM4 24Gb. Pending: NVIDIA confirmation or denial (the 2026-08-26 earnings call is the near-term venue), a second independent source, whether the flagged 8-hi HBM4E upgrade materialises, and what NVIDIA does to offset lower capacity per GPU"
labels:
  - nvidia
  - rubin-ultra
  - hbm
  - memory
  - roadmap
verification: partial
sources:
  - "@SemiAnalysis_"
  - "@scaling01"
created_at: 2026-08-25
updated_at: 2026-08-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-25
    change: "Created — @SemiAnalysis_ (2026-08-24 21:00 UTC) reports Rubin Ultra will ship with 192GB of HBM4 8-hi, down from the 1TB originally previewed and below regular Rubin's 288GB, via three compounding cuts: cube count to 8 after the 4-die Rubin Ultra was scrapped, stack height to 8-hi instead of 16-hi, and HBM4 24Gb dies instead of HBM4E 32Gb dies (an 8-hi HBM4E upgrade flagged as possible later). SemiAnalysis says it broke this to Accelerator Model subscribers in July. Status confirmed on a specialist desk publishing a specific spec with a decomposed causal chain; verification partial — no NVIDIA statement, no second independent source, and the analysis sits behind a paywall that was not read. @scaling01 read it as bearish for large models, then argued the counterpoint himself; both recorded. Directly relevant to [[nvidia-server-price-increase-2026-08]] — memory is the cost driver in both."
---

SemiAnalysis reports that **Rubin Ultra will carry 192GB of HBM4** — less
than regular Rubin's 288GB, and roughly **a fifth of the 1TB** the part was
previewed with.

**The three cuts are independent, and that is the point.** Scrapping the
4-die package took cubes from 16 to 8. Halving stack height took 16-hi to
8-hi. Reverting HBM4E's 32Gb dies to HBM4's 24Gb took another ~25% off per
die. Each is a separate decision; together they compound to ~5x. A single
cut would read as a schedule slip. Three stacked cuts read as a supply
decision — and the same week NVIDIA is reported to be raising server prices
15-17% on memory inflation ([[nvidia-server-price-increase-2026-08]]),
the simplest explanation is that HBM supply and cost, not packaging
capability, set the ceiling.

**Why it belongs in a model-release lane at all.** HBM per package is the
practical bound on how large a model can be served without paying
cross-node interconnect on every token. An *Ultra* SKU landing below the
base SKU inverts the assumption the whole industry plans capacity against:
that each generation's top part buys more memory per GPU. If it holds,
frontier serving economics tilt further toward sparse MoE and toward
smaller dense models — exactly where the open-weight releases in this
ticket set already are ([[alibaba-qwen-3-8-27b-2026-08]],
[[deepseek-v4-ga-surge-pricing-2026-06]]).

**The counterargument deserves equal weight.** Aggregate memory has never
been the binding constraint for anyone willing to chain accelerators —
Cerebras and Groq already do — so "stuck on small models forever" overstates
it. What a lower per-package capacity actually raises is the *cost* of
serving a large model, not its feasibility. @scaling01 made both arguments
within four hours of each other, which is a fair summary of how unsettled
the read is.

**The near-term test is dated.** NVIDIA reports on **2026-08-26**. A
roadmap question about Rubin Ultra memory configuration is the kind of
thing an analyst asks on that call, and the answer will either corroborate
this desk or contradict it.

Related: [[nvidia-groq-3-lpx-2026-08]],
[[spacex-nvidia-starmind-orbital-compute-2026-08]],
[[cxmt-ipo-debut-2026-07]], [[ymtc-star-ipo-2026-08]].
