---
slug: etched-stealth-2026-06
title: Etched exits stealth — $800M raised, $1B+ contracts, Sohu ASIC racks
company: Etched
model: null
status: confirmed
status_note: |
  **2026-06-30**: AI-chip startup **Etched** came out of stealth announcing
  **$800M raised**, **$1B+ in signed customer contracts**, and first racks of
  its **transformer-only Sohu inference ASIC shipping this summer**, with
  claims of SOTA throughput, latency, and power (@kimmonismus 15:17 UTC ~84
  likes; independently @asteris_ai, @qamcintyre, @MillionInt). Builds on
  Etched's ~$500M January-2026 round (Stripes / Peter Thiel, ~$5B valuation) —
  a fresh disclosure on top, not a re-report. The financing figures are
  corroborated; the **performance superlatives are vendor-sourced and
  unaudited** (no third-party Sohu teardown; prior "20× H100" / 500K-tok/s
  claims have circulated unaudited since 2024–25). Part of the week's
  Nvidia-alternative-silicon / compute-sovereignty arc (LongCat-2.0, GLM 5.2).
expected: "First Sohu transformer-ASIC racks shipping summer 2026; named customers behind the '$1B in contracts' and independent Sohu-vs-Nvidia inference benchmarks still pending"
labels:
  - hardware
  - inference
  - funding
  - asic
  - nvidia-alternative
verification: partial
sources:
  - "@kimmonismus"
  - "@asteris_ai"
  - https://x.com/asteris_ai/status/2071986725253976434
created_at: 2026-07-01
updated_at: 2026-07-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-01
    change: "Created — AI-chip startup Etched exited stealth on 2026-06-30 with $800M raised, $1B+ in signed customer contracts, and a ~$5B valuation; first racks of its transformer-only Sohu inference ASIC ship this summer, with vendor claims of SOTA throughput/latency/power (@kimmonismus 15:17 UTC ~84 likes; independently @asteris_ai, @qamcintyre, @MillionInt). Fresh disclosure atop the ~$500M Jan-2026 Stripes/Thiel round (Harvard dropouts Gavin Uberti + Chris Zhu, founded 2022). Status confirmed for the event; verification partial — financing is multi-source social relay with no primary press release surfaced, and the performance superlatives are Etched's own with no independent Sohu teardown. Sits alongside the compute-sovereignty / Nvidia-alternative arc ([[meituan-longcat-2-2026-06]], [[zhipu-glm-5-2]])."
---

**Etched** exited stealth on **2026-06-30**, disclosing **$800M raised**,
**$1B+ in signed customer contracts**, and that the first racks of its
**Sohu** transformer-only inference ASIC will **ship this summer**, with
claims of SOTA throughput, latency, and power. The raise and contract
figures were relayed by @kimmonismus and independently corroborated by
@asteris_ai, @qamcintyre, and @MillionInt.

**Why a separate ticket.** This is a discrete **funding / hardware** event —
one of the event classes this timeline tracks (funding round, shipping
artifact). It is a fresh disclosure on top of Etched's ~$500M January-2026
round (led by Stripes with Peter Thiel, ~$5B valuation; founders Gavin
Uberti and Chris Zhu, Harvard dropouts, founded 2022), not a re-report.

**Confirmed vs. unproven.** The dollar figures are multi-source corroborated
→ `confirmed` event, but **`verification: partial`**: the corroboration is
social relay with no primary Etched press release surfaced, and Sohu is a
**transformer-only ASIC** whose entire bet is that the transformer
architecture stays dominant long enough to amortize fixed-function silicon.
The "SOTA throughput/latency/power" superlatives are Etched's own, with no
third-party teardown and a history of unaudited "20× H100" claims since
2024–25. Treat the financing as real and the performance as unproven.

**Why it matters.** It lands the same week as the LongCat-2.0 /
GLM-5.2 compute-sovereignty story ([[meituan-longcat-2-2026-06]],
[[zhipu-glm-5-2]]) — the whole stack, from Chinese non-Nvidia training
clusters to US transformer-ASIC challengers, is reorganizing around
inference economics and Nvidia-alternative silicon.

**Transition triggers:**
- Named customers, an official Etched release, or independent Sohu
  benchmarks → UPDATE, advance verification toward confirmed.
- Racks actually shipping on the summer timeline → append history.
- ≥15 cycles with no fresh corroboration → revisit for closure.

**Dedup note:** further Etched / Sohu funding, contracts, shipping, or
benchmark signal UPDATES this ticket. The broader Nvidia-alternative and
compute-sovereignty storylines stay on their own tickets.
</content>
