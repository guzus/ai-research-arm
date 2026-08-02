---
slug: ai-hyperscaler-nuclear-smr-deals-2026-07
title: Amazon-X Energy and Meta-TerraPower nuclear SMR power deals for AI datacenters
company: Amazon / Meta
model: null
status: confirmed
status_note: |
  Reported by The Information (2026-07-26, two posts) as part of the same
  coverage window: **Amazon** has an agreement with startup **X Energy**
  to build a **small modular reactor (SMR)** power plant in Washington
  state. Separately, **TerraPower** — the Bill Gates-funded SMR
  startup — has a deal with **Meta**. Both read as part of the broader
  hyperscaler push to secure dedicated, long-lead-time power for AI
  datacenter buildout (adjacent to [[meta-compute-2026-07]] and
  [[google-spacex-compute-2026-06]]). No dollar figures, capacity
  numbers, site details beyond Washington state (Amazon), or timelines
  captured in this window. Single named-outlet sourcing for both deals →
  status `confirmed` (substantive reported events), verification
  `partial` (no primary Amazon/Meta/X Energy/TerraPower statement).
expected: "TBD — capacity, cost, site, and timeline details for both deals; primary company confirmation from Amazon, Meta, X Energy, or TerraPower"
labels:
  - amazon
  - meta
  - nuclear
  - energy
  - infrastructure
  - compute
verification: partial
sources:
  - "@theinformation"
created_at: 2026-07-27
updated_at: 2026-07-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-27
    change: "Created — The Information (Jul 26) reports two separate nuclear SMR power deals for AI datacenter buildout in the same coverage window: Amazon has an agreement with X Energy for an SMR plant in Washington state; TerraPower (Bill Gates-funded) has a deal with Meta. Single named-outlet sourcing, no primary company confirmation, no dollar/capacity/timeline figures → status confirmed, verification partial."
---

The Information reported (2026-07-26) two separate **small modular
reactor (SMR)** nuclear power deals tied to AI-datacenter buildout,
covered in the same reporting window:

- **Amazon** has an agreement with startup **X Energy** to build an SMR
  power plant in **Washington state**.
- **TerraPower** — the Bill Gates-funded SMR startup — has a deal with
  **Meta**.

**Why tracked together.** Both deals surfaced via the same outlet in the
same news cycle and represent the same underlying trend: hyperscalers
locking in dedicated, long-lead-time nuclear power specifically to feed
AI-datacenter compute demand, alongside other compute/power moves like
[[meta-compute-2026-07]] (Meta's excess-capacity rental business) and
[[google-spacex-compute-2026-06]].

**What's missing.** No dollar figures, reactor capacity, cost, precise
site (beyond "Washington state" for Amazon), or timeline for either
deal. No primary statement from Amazon, Meta, X Energy, or TerraPower.

**Transition triggers:**
- Either company confirms details on record (capacity, cost, timeline) →
  UPDATE, consider splitting into separate tickets if the two deals
  diverge materially in scope or timeline.
- Construction begins or a site is finalized → UPDATE.
- 15+ cycles with no further corroboration and no company confirmation →
  consider `closed: stale-rumor-unverified`.

**Dedup note:** further Amazon-X Energy or Meta-TerraPower SMR signal
UPDATES this ticket. Meta's separate "Meta Compute" capacity-rental
business stays on [[meta-compute-2026-07]].
