---
slug: nvidia-rfd4-proteina-2026-10
title: "NVIDIA and UW Institute for Protein Design release RFD4-Proteina, an open protein design model (GTC Berlin)"
company: "NVIDIA / UW Institute for Protein Design"
model: "RFD4-Proteina"
status: released
status_note: |
  **What was released.** Per a headline relay of NVIDIA investor news (@MKRlimitless,
  2026-10-21 10:17 UTC), NVIDIA and the UW Medicine Institute for Protein Design
  (David Baker's lab) debuted RFD4-Proteina, an open model for programmable protein
  design aimed at drug discovery. Launch partner Apheris (@RoehmRobin, 2026-10-21
  12:01 UTC) says it was released at GTC Berlin and designs a protein's sequence and
  structure together against a target. Apheris is a launch distribution partner and
  offers fine-tuning on customers' own GPUs for VHHs, antibodies, binders and enzymes.

  **GTC Berlin context.** A Korean keynote summary (@DrNHJ) says Jensen Huang reported
  about $10B invested in European startups and partnerships over the last year, Vera
  Rubin in full volume production, and sovereign-AI work with Schneider Electric,
  Siemens Energy, Mistral and Nebius.

  **Why partial.** Both release accounts are secondary (a headline relay and a launch
  partner). No NVIDIA or IPD post, model card or licence was captured.
expected: "Released 2026-10-21 at GTC Berlin per partner and investor-news relays. Open: NVIDIA/IPD primary post, licence, weights location, and wet-lab validation numbers."
labels:
  - nvidia
  - biology
  - protein-design
  - open-weights
  - gtc
verification: partial
sources:
  - "https://x.com/MKRlimitless/status/2112850678918131774"
  - "https://x.com/RoehmRobin/status/2112876877891121314"
  - "https://x.com/DrNHJ/status/2112878636009439296"
created_at: 2026-10-21
updated_at: 2026-10-21
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-21
    change: "Created — RELEASED / partial. NVIDIA and the UW Institute for Protein Design released RFD4-Proteina, an open model that co-designs protein sequence and structure against a target, at GTC Berlin on 2026-10-21 (headline relay of NVIDIA investor news via @MKRlimitless; launch partner Apheris via @RoehmRobin). GTC Berlin keynote context (Vera Rubin in volume production, ~$10B European investment) from a @DrNHJ summary. No NVIDIA/IPD primary post or model card captured."
---

RFdiffusion is the Baker lab's standard protein-design tool, and Proteina is
NVIDIA's own protein generative model. A joint "RFD4-Proteina" open model puts the
two lines together and gives it day-one enterprise distribution through partners
like Apheris.

The same week, Anthropic published Claude-orchestrated binder designs against
scorpion neurotoxins ([[anthropic-protein-binder-design-2026-08]]). That work runs
open design models like this one through an LLM agent, so the two approaches feed
each other rather than compete.
