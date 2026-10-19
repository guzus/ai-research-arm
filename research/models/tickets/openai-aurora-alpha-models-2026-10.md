---
slug: openai-aurora-alpha-models-2026-10
title: "OpenAI lists three undocumented models in its API — aurora-red-alpha, aurora-green-alpha, aurora-blue-alpha"
company: OpenAI
model: aurora-red-alpha / aurora-green-alpha / aurora-blue-alpha
status: in-testing
status_note: |
  **Model-list artifact, 2026-10-17/18.** @AndrewCurran_ (2026-10-18 03:13 UTC, ~1.8K
  likes): "Three mysterious new models just showed up in the OpenAI API:
  aurora-red-alpha, aurora-green-alpha, aurora-blue-alpha." Independent repeats within
  hours: @thecodebub ("Source: OpenAI's API", 09:52 UTC), @Josephyala (says they
  appeared on 2026-10-17), @moa_builds ("None of them are callable yet"),
  @0xJoseDinero. No docs, pricing, changelog or OpenAI statement.

  **What the IDs might be — all speculation.** Some replies read "aurora" as an image
  model (@Nitocnt; @Waguri_Kaoruko8 groups "this new model" with GPT Image 2.5).
  Others note that an earlier OpenRouter "aurora-alpha" was linked, without
  confirmation, to a fast Codex model (@Josephyala, @themuscleai). The colour suffixes
  look like parallel variants of one candidate, which suits an A/B or arena-style
  evaluation. None of these readings is adopted.
expected: "Unannounced. Open: what modality the models are, whether they become callable, a launch name, and whether they map to an image or Codex release."
labels:
  - openai
  - api-artifact
  - stealth-model
verification: partial
sources:
  - "https://x.com/AndrewCurran_/status/2111656899338973391"
  - "https://x.com/thecodebub/status/2111757423098863683"
  - "https://x.com/Josephyala/status/2111747395591578023"
  - "https://x.com/moa_builds/status/2111771777047359817"
  - "https://x.com/0xJoseDinero/status/2111777966870900923"
  - "https://x.com/Goura_vk/status/2112170676710944923"
created_at: 2026-10-18
updated_at: 2026-10-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-18
    change: "Created — IN-TESTING / partial. Three undocumented model IDs (aurora-red-alpha, aurora-green-alpha, aurora-blue-alpha) appeared in the OpenAI API model list around 2026-10-17, first widely noted by @AndrewCurran_ (2026-10-18 03:13 UTC) and repeated by several independent accounts. One says they are not callable yet. No docs, pricing or OpenAI statement. Opened at in-testing because a vendor-side model-list entry is a real artifact, not a tease. Verification is partial because only secondary accounts report it. Readings as an image model or a fast Codex model are speculation and are not adopted. Not linked to the closed [[openai-gpt-image-2-5-leak-2026-08]] until a modality is known."
  - ts: 2026-10-19
    change: "In-testing, unchanged; verification stays partial. First modality-specific claim. @Goura_vk (2026-10-19 13:15 UTC) says the three IDs, after briefly appearing in OpenAI's API, 'showed up in Arena's image-generation tests', and that early testers see differences between the variants. This is one secondary account with no screenshot or Arena listing in signal, so the image-model reading moves from reply speculation to a reported sighting, but it is not adopted as fact. The same post calls 'GPT-Image-3' speculation. Still no docs, pricing or OpenAI statement."
---

OpenAI model IDs often show up in the API list before launch. When they do, the
listing tells you something is staged but not what it is. Three colour-coded
"alpha" variants of one name suggest OpenAI is comparing checkpoints rather than
shipping one product.

There are two readings in the replies, an image model and a fast coding model, and
the signal supports neither. This ticket records the artifact and waits for a
modality, a callable endpoint, or an announcement.

**Transition triggers:** OpenAI names or documents the models → confirmed; the IDs
become publicly callable → released; the IDs vanish with no launch for ~15 cycles →
close as stale.
