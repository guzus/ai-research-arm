---
slug: china-nvidia-h200-import-2026-07
title: China reportedly preparing to let Alibaba, ByteDance, DeepSeek import limited Nvidia H200 quantities
company: PRC / Nvidia
model: null
status: rumored
status_note: |
  The Information reports China is preparing to let **Alibaba,
  ByteDance, and DeepSeek** buy **limited quantities of Nvidia H200
  chips** — a domestic-import policy shift distinct from the existing
  outbound-deal review regime tracked on
  [[china-outbound-deal-rules-2026-06]] (that ticket covers outbound
  Chinese investment/deal review; this is an inbound hardware-import
  allowance). Single outlet, no second source in this ingest window.
expected: "Still no policy text and no approvals. As of 2026-09-28 the reported vehicle has shifted from H200 to the new RTX Pro 5500 workstation part, with Beijing reportedly polling Alibaba and ByteDance on volumes; The Information-derived estimates put a possible ~500K chips/quarter from late December at ~$6.5B/quarter. Watch for: an actual approval, a Chinese policy document, NVIDIA guidance including China data-center revenue (its $108B forecast currently assumes zero), and resolution of the Chinese antitrust finding."
labels:
  - china
  - nvidia
  - export-controls
  - hardware
  - rumor
verification: partial
sources:
  - "@theinformation"
  - https://x.com/mark_k/status/2104457886369808622
  - https://x.com/rohanpaul_ai/status/2104520212100051211
  - https://x.com/StockSavvyShay/status/2104242807775117544
  - https://x.com/shanaka86/status/2104566466712609035
created_at: 2026-07-12
updated_at: 2026-09-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-12
    change: "Created — The Information (2026-07-10) reports China is preparing to let Alibaba, ByteDance and DeepSeek buy limited quantities of Nvidia H200 chips, read as evidence Beijing's AI ambitions still depend on US hardware. Single but high-authority outlet, no second source, no policy text → status rumored, verification partial. Distinct from the outbound-deal review regime on [[china-outbound-deal-rules-2026-06]] — this is an inbound import allowance."
  - ts: 2026-09-28
    change: "THE CHIP CHANGED, and that is the substance of this update — the same reported policy opening, now running through a different part. @mark_k (2026-09-28 06:27 UTC), citing The Information: 'Beijing has asked Alibaba and ByteDance how many of Nvidia's new RTX Pro 5500 chips they want to buy, and what they would use them for… No purchases have been approved yet.' @StockSavvyShay adds that ByteDance is 'reportedly considering an order of ~1 million chips'. @rohanpaul_ai puts the arithmetic on it: '~500K RTX Pro 5500 chips a quarter for China, with shipments starting in late December is a possibility now… roughly $6.5B per quarter, or about $26B a year'. These are WORKSTATION parts, not data-center accelerators, which is the whole reason they are discussable — and they are the natural successor vehicle to the H200 allowance this ticket was opened on. Kept on this ticket rather than split out: same shipping artifact (a Chinese inbound-import allowance for named buyers), same reported mechanism, one generation later. Status stays rumored — nothing is approved. Verification stays partial. COUNTERWEIGHT, and it is heavy: @shanaka86 summarises Nvidia telling the SEC that under current rules it CANNOT sell China's data centers a competitive AI chip both Washington and Beijing will approve; the 2026-09-24 Huang/Xi White House summit left controls untouched and USTR called them a national-security matter off the negotiating table; the licensed H200 goes in small amounts to named buyers after US-soil inspection and a 25% tariff; Beijing's antitrust regulator preliminarily found that selling China the downgraded parts US law required breached the terms of its approval of an Nvidia acquisition; and Nvidia's $108B quarterly forecast assumes ZERO China data-center revenue, with Bernstein putting its China share at ~8% this year against Huawei near 50%. Read together: the workstation channel is the only live path, and even it is unapproved."
---

**The Information** reports that **China is preparing to let Alibaba,
ByteDance, and DeepSeek buy limited quantities of Nvidia H200 chips** —
an inbound hardware-import policy shift, read as evidence that Beijing's
AI ambitions still depend on US hardware despite the broader
decoupling push.

**Why a separate ticket from [[china-outbound-deal-rules-2026-06]]:**
that ticket tracks the PRC's **outbound** deal-review regime (Chinese
investors buying foreign tech/data assets). This is the opposite
direction — an **inbound** hardware-import allowance for named Chinese
AI labs.

**Transition triggers:**
- Official PRC policy text, or a named import transaction → UPDATE,
  advance status to `in-testing`/`confirmed`.
- A second independent outlet corroborates → advance verification to
  `confirmed`.
- ≥15 cycles with no fresh corroboration → `closed:
  stale-rumor-unverified`.

**Dedup note:** further signal on this specific H200-import allowance
UPDATES this ticket. The outbound-deal-review regime stays on
[[china-outbound-deal-rules-2026-06]].
