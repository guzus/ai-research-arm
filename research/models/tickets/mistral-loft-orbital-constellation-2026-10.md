---
slug: mistral-loft-orbital-constellation-2026-10
title: Mistral models (Ministral 3) run on Orbitworks/Loft Orbital's AI satellite constellation with NVIDIA
company: Mistral AI / Loft Orbital / Orbitworks / NVIDIA
model: Ministral 3
status: confirmed
status_note: |
  @MistralAI (2026-10-13 13:25 UTC): "Mistral models are in orbit", joining
  @orbitworksspace and @LoftOrbital's AI satellite constellation with
  @NVIDIAAIInfra. @LoftOrbital (13:17 UTC): Orbitworks launched Altair "a few
  weeks ago". It is the first of a planned 50-satellite AI constellation that
  delivers AI-generated alerts within minutes, and it uses NVIDIA hardware running
  models such as Mistral's Ministral 3. One satellite is in orbit; the other 49
  are planned.
expected: "First satellite (Altair) in orbit; constellation build-out to 50 satellites, no schedule given."
labels:
  - mistral
  - partnership
  - edge-inference
  - space
verification: confirmed
sources:
  - "https://x.com/MistralAI/status/2109998925037859091"
  - "https://x.com/LoftOrbital/status/2109996918935867758"
created_at: 2026-10-14
updated_at: 2026-10-14
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-14
    change: "Created — CONFIRMED / confirmed. @MistralAI (2026-10-13 13:25 UTC) announced that its models are running on Orbitworks/Loft Orbital's AI satellite constellation with NVIDIA. @LoftOrbital (13:17 UTC) says the first satellite, Altair, launched a few weeks ago. It is the first of a planned 50, and it runs models such as Ministral 3 on NVIDIA hardware to deliver AI alerts within minutes. Both companies posted on their own handles."
---

This is a small deployment partnership, but it is primary on both sides and in
production on one satellite. It is the first open-weight frontier-lab model
reported running inference in orbit. For comparison, the orbital-compute tickets
[[google-suncatcher-tpu-satellite-2026-09]] and
[[spacex-nvidia-starmind-orbital-compute-2026-08]] are about hardware.

The model is Ministral 3, Mistral's small edge model, not Mistral Large 4
([[mistral-large-4-2026-10]]). Status is `confirmed` rather than `released`
because the constellation is one satellite of 50 and the service is not
generally available.
