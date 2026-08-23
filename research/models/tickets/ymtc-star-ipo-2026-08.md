---
slug: ymtc-star-ipo-2026-08
title: YMTC's STAR Market IPO review formally accepted — RMB 33B target
company: YMTC (Yangtze Memory Technologies)
model: null
status: confirmed
status_note: |
  **@jukan05** (2026-08-21 12:32 UTC): "**YMTC STAR Market IPO review
  officially accepted.** According to the **Shanghai Stock Exchange**,
  the review status for YMTC's proposed IPO and listing on the STAR
  Market has been updated to **'Accepted (已受理)'**. Planned issuance:
  **1.98–2.43 billion shares**. Fundraising target: **RMB 33.0 billion** —
  RMB 20.8B for upgrading and expanding mass-production lines, RMB 12.2B
  for R&D."

  Status `confirmed`: an **exchange filing-status change** is a
  primary-record event, cited to the SSE with a share range and a
  proceeds breakdown. Verification `partial` — the SSE record is cited,
  not linked, and the relay is a single (well-sourced, semiconductor-focused)
  account; no SSE URL or prospectus was captured.

  **Why a NAND IPO belongs in this lane.** Memory is currently the
  binding constraint on AI-server cost — Nvidia is reportedly raising
  system prices ~17% on HBM4/LPDDR5X inflation
  ([[nvidia-server-price-increase-2026-08]]), Korean DRAM export unit
  prices are rising, and every major NAND maker is converting from
  tungsten to molybdenum word lines to scale past ~300 layers
  (@SemiAnalysis_). A Tianfeng/SanDisk IR readout in the same window
  expects **YMTC to capture ~80% of the Chinese market** while arguing its
  expansion is "unlikely to become a major risk to global supply and
  demand over the next several years" — the explicit bear case for this
  raise being a global price event.
expected: "SSE review status moved to 'Accepted' on 2026-08-21 with a RMB 33.0B target across 1.98-2.43B shares. Pending: SSE review progression, the prospectus, pricing and listing date, and whether the RMB 20.8B capacity spend measurably loosens NAND supply"
labels:
  - china
  - memory
  - ipo
  - supply-chain
  - semiconductors
verification: partial
sources:
  - "@jukan05"
  - "@SemiAnalysis_"
created_at: 2026-08-23
updated_at: 2026-08-23
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-23
    change: "Created — the Shanghai Stock Exchange moved YMTC's STAR Market IPO review status to 'Accepted (已受理)' (@jukan05, 2026-08-21 12:32 UTC), with a planned issuance of 1.98-2.43 billion shares and an RMB 33.0 billion target split RMB 20.8B for mass-production line upgrades/expansion and RMB 12.2B for R&D. Status confirmed — an exchange filing-status change is a primary-record event with disclosed figures. Verification partial — the SSE record is cited rather than linked and the relay is a single account; no prospectus captured. Relevant to the model lane through memory supply: Nvidia is reportedly raising AI-server prices ~17% on memory inflation, and a SanDisk IR readout in the same window expects YMTC to take ~80% of the Chinese market while arguing its expansion will not materially loosen global supply for several years."
---

This ticket tracks memory supply, which is currently the most binding
non-power constraint on AI compute cost.

**The number that matters is the split, not the total.** RMB 20.8B of
the RMB 33.0B target goes to upgrading and expanding mass-production
lines — that is capacity, and capacity is what would eventually relieve
the NAND tightness that is pushing AI-server prices up
([[nvidia-server-price-increase-2026-08]]). RMB 12.2B goes to R&D, which
is the layer-count race @SemiAnalysis_ describes: past roughly 300
layers, tungsten word lines fail on resistance, fluorine leakage and
gap-fill, and molybdenum becomes mandatory rather than optional.

**The counter-argument is already on the record, from a competitor's
investor-relations desk.** SanDisk's IR team expects YMTC to take ~80%
of the Chinese market but argues China's own demand is growing fast
enough to absorb it, so the expansion is "unlikely to become a major
risk to global supply and demand over the next several years." If that
holds, this raise reshapes the *Chinese* memory market without loosening
prices for anyone building AI datacenters elsewhere. That is the
distinction to watch.

"Accepted" is the first formal gate of a STAR Market review, not an
approval and not a listing. Treat the timeline as open.

Related: [[cxmt-ipo-debut-2026-07]], [[sk-hynix-nasdaq-ipo-2026-07]],
[[baidu-kunlunxin-ipo-2026-06]], [[anthropic-micron-supply-2026-06]],
[[china-nvidia-h200-import-2026-07]].
