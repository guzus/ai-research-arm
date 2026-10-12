---
slug: microsoft-maia-300-2026-10
title: "Microsoft Maia 300 — next-gen inference accelerator; Maia to become Microsoft's primary inference system at multi-GW scale from 2027"
company: "Microsoft"
model: "Maia 300"
status: confirmed
status_note: |
  **First-party, 2026-10-12 13:03 UTC (@satyanadella):** "Today we are announcing
  our biggest bet yet on our own silicon. Starting next calendar year, we will
  scale our Maia family to multi-gigawatt deployments, making it the primary
  inference system for our own product and services. And we're introducing Maia
  300, which delivers 40% more tokens per watt compared to leading GPU-based
  systems." @Microsoft (13:16 UTC) adds "up to 7x the rack-scale token throughput
  of Maia 200"; @Azure and @mustafasuleyman amplified.

  **Maia 200 is already deployed** across the US, Europe and Australia, which
  Nadella says delivers up to 1.7x more tokens per watt in Teams and Copilot.

  **Why `confirmed`, not `released`.** Maia is internal silicon serving Microsoft's
  own products; no Azure customer SKU, availability date or independent
  measurement was captured. All performance numbers are vendor-stated against an
  unnamed "leading GPU-based system".
expected: "Multi-gigawatt Maia deployments start calendar 2027. Watch for a Maia 300 Azure customer offering, process/memory specs, and any third-party efficiency measurement."
labels:
  - microsoft
  - custom-silicon
  - inference
  - compute
verification: confirmed
sources:
  - "https://x.com/satyanadella/status/2109631106404487523"
  - "https://x.com/Microsoft/status/2109634232163471782"
  - "https://x.com/Azure/status/2109643052625403998"
  - "https://x.com/mustafasuleyman/status/2109655335250366752"
created_at: 2026-10-12
updated_at: 2026-10-12
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-12
    change: "Created — CONFIRMED / confirmed. @satyanadella (2026-10-12 13:03 UTC) announces Maia 300 — 40% more tokens per watt than leading GPU-based systems, up to 7x Maia 200 rack-scale throughput per @Microsoft — and says Maia will scale to multi-gigawatt deployments from next calendar year as the primary inference system for Microsoft's own products. Maia 200 is already deployed in the US, Europe and Australia. Held at confirmed: internal silicon with no customer availability; every number is vendor-stated."
---

Microsoft is the third hyperscaler to put its own accelerator at the center of
its inference fleet. The Maia announcement makes custom silicon the *primary*
inference path for Microsoft's own products, not a side experiment. That
reduces how much of Microsoft's future serving demand goes to NVIDIA.

The numbers to hold Microsoft to are the 40% tokens-per-watt claim and the
multi-gigawatt 2027 timeline. Neither can be checked from outside yet.
