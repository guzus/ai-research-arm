---
slug: google-embeddinggemma-2-2026-10
title: "EmbeddingGemma 2 — Google DeepMind's 740M natively multimodal open on-device embedding model (Apache 2.0)"
company: "Google / DeepMind"
model: "EmbeddingGemma 2"
status: released
status_note: |
  **First-party launch, 2026-10-06 16:04 UTC (@GoogleDeepMind).** "Meet
  EmbeddingGemma 2, our first natively multimodal open model for on-device
  embeddings. It expands beyond text to unify code, images, audio, and video in a
  shared space." 740M parameters; claimed competitive with specialist models more
  than twice its size; positioned for multimodal search (e.g. finding moments in a
  video from a voice memo) and for private on-device RAG paired with Gemma 4.
  Weights on Hugging Face and Kaggle under Apache 2.0.

  **Secondary detail:** built on the Gemma 4 architecture; MTEB Code reportedly
  rises from 68.76 to 78.68 versus the prior EmbeddingGemma (@TheInfoMachine).
expected: "RELEASED 2026-10-06 with open weights (Hugging Face, Kaggle). Open: independent MMEB/MTEB placement and on-device latency numbers."
labels:
  - google
  - deepmind
  - open-weights
  - embeddings
  - multimodal
  - on-device
verification: confirmed
sources:
  - https://x.com/GoogleDeepMind/status/2107502286758895878
  - https://x.com/GoogleDeepMind/status/2107502289652982118
  - https://x.com/TheInfoMachine/status/2107828162352533704
  - "@GoogleDeepMind"
created_at: 2026-10-07
updated_at: 2026-10-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-07
    change: "Created — RELEASED / confirmed. @GoogleDeepMind announced EmbeddingGemma 2 on 2026-10-06 16:04 UTC: a 740M-parameter, natively multimodal open embedding model (text, code, images, audio, video in one space) for on-device use, Apache 2.0, weights on Hugging Face and Kaggle; pairs with Gemma 4 for private on-device RAG. Secondary: Gemma 4 architecture, MTEB Code 68.76 -> 78.68 (@TheInfoMachine)."
---

Google's open embedding line goes multimodal. The first EmbeddingGemma was
text-only; version 2 puts five modalities into one vector space at under a
billion parameters, which is the size class that actually runs on a phone.

The pairing with Gemma 4 ([[gemma-4]]) is the product story: retrieval and
generation both on-device, nothing leaving the handset. The API-side sibling is
[[gemini-embedding-2]].

All benchmark claims are Google's own so far. Transition trigger: ≥4 weeks after
2026-10-06 → close as released-and-aged.
