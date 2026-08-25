---
slug: spacex-nvidia-starmind-orbital-compute-2026-08
title: SpaceX and NVIDIA co-design a space-optimized Vera Rubin NVL72 for Starmind orbital AI satellites
company: SpaceX / NVIDIA
model: null
status: confirmed
status_note: |
  **@elonmusk, on the record (2026-08-24 ~20:00 UTC, ~3.3K RT across the
  original and relays):** "SpaceX, in partnership with Nvidia, has designed
  a **space-optimized Vera Rubin NVL72 system** for launch to orbit in
  **Q4 next year** [Q4 2027], with **significant scale in 2028**."

  **What the relays add**, consistently across independent accounts
  (@ns123abc's itemised readout, ~114 likes; @BharatFactsIN; @JenH7820):

  - The satellites are branded **Starmind**; each carries **72 Rubin GPUs
    + 36 Vera CPUs per rack** in a **SpaceX-designed rack** Elon calls
    "simpler, lower cost, denser and lighter than a traditional rack."
  - **The same design deploys on the ground** — described as "a radical
    simplification of the normal NVL72." That is the part that matters
    most near-term: this is a rack redesign that ships terrestrially long
    before anything reaches orbit.
  - In orbit: **solar powered**, results returned over **Starlink laser
    links**; each satellite runs datacenter-class compute; **up to 1
    million satellites planned** (an aspiration, not a manifest).
  - **"We are exclusive to NVIDIA."** Grok's ground compute is described
    as scaling **2 GW → ~10 GW**.

  Status `confirmed`: a named principal announced it on the record with a
  named partner, a named product, a dated first launch, and a specific
  rack configuration. Verification `partial`: **no NVIDIA statement, no
  SpaceX press page, and no third-party document was captured** — every
  number above traces to one Musk post and its relays. The 1M-satellite
  figure and the 10 GW ground target are aspirational statements of intent,
  not committed builds, and this ticket records them as such.

  **Read the exclusivity claim narrowly.** "We are exclusive to NVIDIA"
  is a buyer-side statement from SpaceX about its own procurement, not a
  supply commitment from NVIDIA, and it lands the same week NVIDIA is
  reported to be raising server prices ([[nvidia-server-price-increase-2026-08]])
  and cutting HBM content on Rubin Ultra
  ([[nvidia-rubin-ultra-hbm-downgrade-2026-08]]).
expected: "Announced 2026-08-24 by @elonmusk: first Starmind launch Q4 2027, significant scale 2028, ground version of the simplified NVL72 rack available sooner. Pending: an NVIDIA or SpaceX first-party post, thermal/radiation engineering detail (an orbital NVL72 has no air and no water loop), power and downlink budgets, and whether the terrestrial rack simplification ships to anyone other than SpaceX"
labels:
  - spacex
  - nvidia
  - vera-rubin
  - compute
  - orbital
  - infrastructure
verification: partial
sources:
  - "@elonmusk"
  - "@ns123abc"
  - "@BharatFactsIN"
  - "@JenH7820"
  - "@efecollinsevb"
created_at: 2026-08-25
updated_at: 2026-08-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-25
    change: "Created — @elonmusk announced (2026-08-24) that SpaceX, in partnership with NVIDIA, has designed a space-optimized Vera Rubin NVL72 for launch to orbit in Q4 2027 with significant scale in 2028. Relays (@ns123abc, @BharatFactsIN, @JenH7820) add the Starmind branding, 72 Rubin GPUs + 36 Vera CPUs per SpaceX-designed rack, solar power with Starlink laser downlink, up to 1M satellites planned, 'we are exclusive to NVIDIA,' and Grok ground compute scaling 2GW to ~10GW; the same simplified rack is said to deploy terrestrially too. Status confirmed — on-record from a named principal with a named partner, product, date and configuration. Verification partial — no NVIDIA or SpaceX first-party page captured, and the 1M-satellite and 10GW figures are stated intent, not committed builds."
---

SpaceX and NVIDIA say they have co-designed a **space-optimized Vera Rubin
NVL72** and will fly it as the **Starmind** satellite line starting **Q4
2027**, with scale in 2028.

**The orbital headline is the least load-bearing part.** Launching
datacenter-class compute is a 2027-2028 claim with no captured engineering
detail on the two problems that actually decide it — rejecting ~100 kW of
rack heat with no atmosphere and no water loop, and surviving total
ionizing dose on commodity HPC silicon. Neither Musk's post nor any relay
addresses them, and this ticket does not treat the launch date as settled.

**The terrestrial claim is the one to watch.** Elon describes the same
design as "a radical simplification of the normal NVL72" that also deploys
on the ground, "simpler, lower cost, denser and lighter than a traditional
rack." If a customer-designed rack variant genuinely ships, that is a
near-term change to how NVL72-class systems are built and priced — and it
is testable long before anything reaches orbit.

**Exclusivity cuts one way only.** "We are exclusive to NVIDIA" binds
SpaceX's purchasing, not NVIDIA's allocation. Its value to NVIDIA is a
named anchor customer disclosed two days before the 2026-08-26 earnings
call, during a seven-session share decline and amid reports of
memory-driven server price increases
([[nvidia-server-price-increase-2026-08]]) and a cut to Rubin Ultra HBM
content ([[nvidia-rubin-ultra-hbm-downgrade-2026-08]]).

**Why it sits in this lane.** The stated purpose is Grok's compute supply:
ground capacity scaling from 2 GW toward ~10 GW, with orbit as the
extension. That makes it a model-roadmap input for xAI/SpaceX the same way
[[google-spacex-compute-2026-06]] and [[anthropic-spacex-colossus-2026-05]]
are, and it belongs beside [[cursor-spacexai-model-2026-06]] and
[[xai-grok-2t-spacex-data-2026-07]] rather than in a pure infrastructure
bucket.
