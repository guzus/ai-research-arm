---
slug: typesafe-jev-1-14-2026-10
title: "TypeSafe AI ships Jev 1.14.0 with opt-in 'danger zone' features (images, box type, longer context)"
company: "TypeSafe AI"
model: "Jev 1.14.0"
status: released
status_note: |
  **2026-10-16 — corroborated by Artificial Analysis; distributed by OpenRouter.**
  @ArtificialAnlys measures "the recently released Jev 1.14" at 57 on its Decision
  Index v1.0, with a 78 ms Time per Task. @OpenRouter's Armor beta (a tool-call safety
  classifier) runs on Jev, per OpenRouter's own launch post quoted by @stretchcloud.
  Verification moves to `partial`. A TypeSafe changelog would make it `confirmed`.

  **Single secondary source.** @bykimdohoon (2026-10-15): TypeSafe AI shipped Jev
  1.14.0 on 2026-10-14. Experimental features sit behind opt-in API headers called
  "danger zone": image input, a new `box` type returning one bounding box, and longer
  context. `jev-latest` moves to 1.14.0 in a week, and 1.13.0 deprecation comes with
  60 days' notice.

  **New ticket, not a reopen.** The original Jev ticket
  ([[typesafe-jev-2026-09]]) is closed and stays untouched. This is a new versioned
  artifact.
expected: "Released 2026-10-14; jev-latest alias moves to 1.14.0 ~2026-10-21; 1.13.0 deprecation after 60 days' notice. Open: a TypeSafe primary changelog."
labels:
  - typesafe
  - versioned-release
  - multimodal
  - unverified
verification: partial
sources:
  - "https://x.com/bykimdohoon/status/2110696542541861273"
  - "https://x.com/ArtificialAnlys/status/2111052531166249039"
  - "https://x.com/stretchcloud/status/2111048256272888005"
  - "@OpenRouter"
created_at: 2026-10-15
updated_at: 2026-10-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-15
    change: "Created — RELEASED / unverified. @bykimdohoon (2026-10-15 11:37 UTC) reports TypeSafe AI shipped Jev 1.14.0 on 2026-10-14. It adds opt-in 'danger zone' API headers gating image input, a new single-bounding-box 'box' type and longer context. The jev-latest alias moves to 1.14.0 in one week, and 1.13.0 will get 60 days' deprecation notice. Single secondary source with no TypeSafe changelog captured, hence unverified. The predecessor [[typesafe-jev-2026-09]] is closed and untouched. Company context: [[typesafe-funding-round-2026-09]]."
  - ts: 2026-10-16
    change: "Released, unchanged; verification unverified -> partial. Two independent corroborations, neither a TypeSafe changelog. (1) @ArtificialAnlys (2026-10-16 11:11 UTC) measures 'the recently released Jev 1.14' on its Decision Index v1.0: score 57 (second, behind Liquid AI's new d1-ultra at 65) and the lowest-but-one Time per Task at 78 ms. A third-party benchmarker measuring the exact version confirms it is live. (2) @OpenRouter launched OpenRouter Armor in beta this week (quoted by @stretchcloud, 2026-10-16 10:55 UTC). It is a tool-call safety classifier that 'uses @typesafeai's Jev model' and claims better performance than Claude Code's auto classifier at a fraction of the cost, with 279 ms median added latency on the Claude Code-compatible ruleset, free during beta. That is a primary third-party distribution of the Jev line, but it does not name a version. Competitor context: [[liquid-ai-d1-ultra-2026-10]], [[microsoft-decision-1-2026-10]]."
---
This is a point release, tracked because it adds a modality (images) and a
structured-output type to a model line already in the set
([[typesafe-jev-2026-09]], closed).

The useful operational detail is the alias policy. `jev-latest` moves in a week,
so anyone pinned to the alias gets new behaviour without deploying anything.
