---
slug: reflection-open-weight-model-2026-10
title: Reflection AI releases Beam — 501B sparse MoE open-weight model under Apache 2.0 (reported)
company: Reflection AI
model: Beam
status: released
status_note: |
  **2026-10-06 — reported RELEASED as "Beam" on 2026-10-05.** AI-news digest
  @TheInfoMachine (2026-10-06 12:35 UTC): "Reflection AI released Beam on October 5,
  a 501B sparse MoE model under Apache 2.0. Its Terminal Bench v2.1 chart excludes
  DeepSeek V4.1 Flash at 90.6 and Kimi K3 at 88.3, against Beam's 80.1." Still no
  Reflection first-party post, model card or weights URL captured in-window, so
  verification stays partial. The digest's chart-selection critique is its own
  framing; the 80.1 vs 90.6 / 88.3 comparison is consistent with Axios's earlier
  "competitive with Chinese open models" positioning rather than ahead of them.

  **Axios scoop, 2026-10-04**, relayed by @HerbScribner (12:51 UTC, ~469 likes):
  NVIDIA-backed Reflection "is preparing to shake up the AI race with a powerful
  open-weight system that could threaten Chinese upstarts and U.S. AI giants
  alike." Per a secondary summary of the report (@shipfrontierai), capabilities
  are initially below the most advanced US systems but competitive with leading
  Chinese open-weight models; no release date given.

  **CEO on record.** Journalist @Cat_Zakrzewski (2026-10-05) says Reflection CEO
  Misha Laskin told her in a recorded interview the prior week that he plans to
  launch an open-weight model soon, framing it as necessary for national
  security. No Reflection first-party announcement, model name, size or
  licence captured in-window.
expected: "Reported released 2026-10-05 (Beam, 501B sparse MoE, Apache 2.0). Open: first-party confirmation, weights location, active-parameter count, independent benchmarks, and whether it was trained on the SpaceX Colossus 2 capacity Reflection leases."
labels:
  - open-weights
  - us-lab
  - nvidia-backed
verification: partial
sources:
  - https://x.com/HerbScribner/status/2106728828206756337
  - https://x.com/Cat_Zakrzewski/status/2107120604805517445
  - https://x.com/shipfrontierai/status/2107098970145337761
  - https://x.com/TheInfoMachine/status/2107449727696433179
  - "@HerbScribner"
  - "@Cat_Zakrzewski"
created_at: 2026-10-05
updated_at: 2026-10-06
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-05
    change: "Created — CONFIRMED / partial. Axios reported on 2026-10-04 (relayed by @HerbScribner) that NVIDIA-backed Reflection AI is preparing a powerful open-weight model; a secondary summary (@shipfrontierai) adds it is initially below top US systems but competitive with leading Chinese open-weight models, with no release date. Journalist @Cat_Zakrzewski says CEO Misha Laskin told her on camera the prior week he plans to launch an open-weight model soon, on national-security grounds. Confirmed because the plan is on record from the CEO plus primary-source reporting; partial because no Reflection first-party post, model name or specs were captured in-window."
  - ts: 2026-10-06
    change: "RELEASED (from confirmed); verification stays partial; title and model updated to the reported name. AI-news digest @TheInfoMachine (2026-10-06 12:35 UTC) reports Reflection AI released Beam on 2026-10-05 — a 501B sparse mixture-of-experts model under Apache 2.0 — and notes its Terminal Bench v2.1 chart omits DeepSeek V4.1 Flash (90.6) and Kimi K3 (88.3) against Beam's 80.1. Single secondary source; no Reflection first-party announcement, model card or weights link captured in-window, so the release, size and licence are reported rather than verified. If accurate, Beam lands below the leading Chinese open-weight models on that benchmark, matching the Axios framing recorded at creation."
---

Reflection AI has been the US open-weights lab defined mostly by its
fundraising and compute commitments — most visibly the $6.3B SpaceX lease in
[[spacex-reflection-compute-2026-06]] — rather than by a shipped model. The
Axios report and Laskin's on-camera remarks are the first concrete signal that
a release is near.

The positioning matters more than the specs, which are unknown. Laskin frames
an American open-weight model as a national-security necessity, i.e. a direct
answer to Chinese open-weight dominance (DeepSeek, Qwen, Kimi). Axios's own
framing — competitive with Chinese open models, below US frontier closed ones
— sets the bar the release will be judged against.

Transition triggers: a Reflection first-party announcement or model card →
UPDATE (verification confirmed); downloadable weights → `released`. Further
Reflection compute-deal news stays on the SpaceX ticket; a reported Nebius
compute deal (>$1B, per the same secondary summary) is unverified here.
