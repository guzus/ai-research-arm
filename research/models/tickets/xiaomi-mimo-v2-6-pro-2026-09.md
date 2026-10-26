---
slug: xiaomi-mimo-v2-6-pro-2026-09
title: Xiaomi MiMo-V2.6-Pro — open-weight leader on the Artificial Analysis Intelligence Index
company: Xiaomi
model: MiMo-V2.6-Pro
status: closed
status_note: |
  **Reported shipped and leading the open-weight field, 2026-09-24.**
  @kimmonismus: "Xiaomi's MiMo-V2.6-Pro... now leads open-weight models on the
  Artificial Analysis Intelligence Index. 46 points, just behind GPT-5.6 Sol
  (max) at 47... The cost gap is much larger: $0.13 versus $1.99 per
  Intelligence Index task, on a weighted-average basis. Pro handles text,
  images, video and audio, with a 1M-token context window. Xiaomi has kept API
  pricing unchanged from V2.5. The model weights are available under MIT.
  Xiaomi is also releasing the training environments and RL code alongside the
  technical report."

  **Independent evidence that the weights are actually out.** @Hikari_07_jp
  built and published an abliterated variant of a 9B model distilled from MiMo
  (2026-09-24 11:46 UTC), then shipped Q4_K_M and NVFP4 quantizations of
  `MiMo-V2.6-Distill-Qwen-9B` with measured throughput (108 tok/s NVFP4 W4A8 on
  an RTX 5070 Ti, 2026-09-24 21:57 UTC). Someone quantizing a derivative is
  harder evidence that a V2.6 family shipped openly than any benchmark relay.

  **The claim to hold loosely is the 15× cost gap, not the score.** 46 vs 47
  on a published third-party index is checkable and unremarkable in itself.
  "$0.13 versus $1.99 per Intelligence Index task" is a weighted-average
  derived figure that folds in token pricing AND verbosity — a model that
  reasons less to reach the same score looks arbitrarily cheaper on it. It is
  the right metric for a buyer and the wrong one for a capability claim.

  **Relationship to [[xiaomi-mimo-v2-5-pro]].** That ticket tracks the
  V2.5-Pro-UltraSpeed release (~1,000 tok/s on a 1T MoE) and stays open; this
  is the next version, not a restatement, and Xiaomi holding API pricing flat
  across the version bump is the notable continuity.

  **Why this lane cares.** It is the second time in two months that a Chinese
  open-weight release has landed within a point of a Western closed flagship
  ([[zhipu-glm-5-3-2026-08]] was the first), and Treasury Secretary Bessent
  argued in the same 24 hours that stronger US open models are a strategic
  necessity precisely because Chinese models distill American capabilities.
expected: "Reported released with MIT weights, unchanged API pricing from V2.5, 1M context and text/image/video/audio input. Open: the Artificial Analysis listing verified directly rather than through a relay, the technical report and RL code actually published, the parameter count and architecture, and whether the ~15x cost advantage survives a normalization for output-token verbosity."
labels:
  - xiaomi
  - open-weights
  - china
  - multimodal
  - mit-license
  - released
verification: partial
sources:
  - https://x.com/kimmonismus/status/2103137466467361275
  - https://x.com/Hikari_07_jp/status/2103242476962349314
  - https://x.com/Hikari_07_jp/status/2103088731645505988
  - "https://x.com/urdav3/status/2110010973373538766"
  - "https://x.com/Rich79_Capital/status/2109997103804232004"
created_at: 2026-09-25
updated_at: 2026-10-26
closed_at: 2026-10-26
closed_reason: released-and-aged
history:
  - ts: 2026-09-25
    change: "Created — RELEASED / partial. @kimmonismus reported on 2026-09-24 15:00 UTC (~470 likes) that Xiaomi's MiMo-V2.6-Pro now leads open-weight models on the Artificial Analysis Intelligence Index at 46 points, one behind GPT-5.6 Sol (max) at 47, at $0.13 vs $1.99 per Intelligence Index task weighted-average; handles text, images, video and audio at 1M context; API pricing unchanged from V2.5; weights under MIT, with training environments, RL code and a technical report said to accompany the release. Verification partial rather than unverified on the strength of INDEPENDENT corroboration of the artifact: @Hikari_07_jp published an abliterated 9B distilled from MiMo (2026-09-24 11:46 UTC) and then Q4_K_M and NVFP4 quantizations of MiMo-V2.6-Distill-Qwen-9B with measured throughput (2026-09-24 21:57 UTC) — a third party building derivatives is stronger evidence that open weights exist than a benchmark relay. Status released on that basis. The 15x cost-per-task gap is recorded but flagged: it is a derived weighted-average that mixes token price with reasoning verbosity, so it measures buyer economics, not capability. Distinct ticket from [[xiaomi-mimo-v2-5-pro]] (V2.5-Pro-UltraSpeed), which stays open; noted alongside [[zhipu-glm-5-3-2026-08]] as the second Chinese open-weight release in two months to land within a point of a Western closed flagship."
  - ts: 2026-10-13
    change: "Released, unchanged — V2.5 traffic is being moved onto V2.6. A migration notice from @BAI_AGI was relayed in-window by @urdav3, @Rich79_Capital and @Temitope_Fire. From 2026-10-14 18:00 SGT, requests using the legacy MiMo-V2.5-Pro and MiMo-V2.5 IDs will be routed to MiMo-V2.6-Pro and MiMo-V2.6-Flash and billed at the new models' rates. From 2026-10-21 10:00 SGT, the legacy IDs will return errors. The notice also names a MiMo-V2.6-Flash tier that this ticket had not recorded. Verification stays partial: the notice comes from a provider/community account, not a Xiaomi handle, and the relays come from a promotional cluster (#TRONEcoStar). One point is unresolved: 'billed at the new models' rates' does not fit easily with the 2026-09-24 report that V2.6 kept V2.5 API pricing."
  - ts: 2026-10-26
    change: "Closed — released-and-aged. Released state since creation (reported live 2026-09-24, per the creation history entry); at least four weeks have now passed, and the artifact has rolled into normal coverage. History preserved; any successor version gets its own ticket."
---

The score is not the interesting number. The license is.

A model one point off a closed Western flagship on a third-party index is a
story that has now happened several times this year, and each time the gap has
been narrow enough to be inside the noise of whatever the index weights that
month. What is not noise is Xiaomi shipping it MIT, together with the training
environments and the RL code. That is a strictly stronger release than weights
alone: it hands the reproduction path to anyone, which is the thing that
compounds.

The pricing decision underneath it is deliberate too. Holding API prices flat
across a version bump, while the open weights are free, means Xiaomi is not
monetizing the model — it is monetizing something adjacent, or nothing yet. A
company with Xiaomi's device footprint releasing a 1M-context multimodal model
into the commons is a distribution play, not a model-API play.

The cost-per-task figure should be treated as marketing arithmetic until
someone normalizes it. Fifteen-to-one is the kind of ratio you get when a
cheaper model also happens to emit fewer reasoning tokens, and that is a
different claim from "fifteen times cheaper at equal work".

For the pipeline, the tell to watch is derivative velocity. Within hours of the
release, third parties were publishing quantized abliterated distillations with
measured throughput. That ecosystem response, not the index row, is what makes
an open release matter.
