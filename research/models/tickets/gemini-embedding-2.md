---
slug: gemini-embedding-2
title: Gemini Embedding 2 — native multimodal embedding model
company: Google / DeepMind
model: Gemini Embedding 2
status: confirmed
status_note: |
  Google DeepMind shared the Gemini Embedding 2 whitepaper on 2026-05-27
  (09:04 UTC RT by @GoogleDeepMind amplifying @mseyed), positioning it as
  the first **native multimodal** embedding model in the Gemini family —
  text, image, audio, and video encoded into a shared embedding space.
  Released alongside the Gemini 3.5 family I/O push. Whitepaper out; no
  public pricing, API endpoint, or benchmark table in the visible signal
  yet — those land via Gemini API + Vertex AI in the same lane Gemini 3.5
  Flash rolled out on.
expected: "API + AI Studio rollout via the Gemini 3.5 lane; no announced date"
labels:
  - embedding
  - multimodal
  - frontier-model
  - gemini-3-5-family
verification: confirmed
sources:
  - "@GoogleDeepMind"
  - "@mseyed"
created_at: 2026-05-28
updated_at: 2026-05-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-28
    change: "Created — Google DeepMind whitepaper for Gemini Embedding 2 (2026-05-27 09:04 UTC RT by @GoogleDeepMind from @mseyed): \"A Native Multimodal Embedding Model from Gemini\". Frames text+image+audio+video into a single embedding space; ships alongside the broader Gemini 3.5 family launched at I/O 2026-05-19"
---

Google DeepMind published the **Gemini Embedding 2** whitepaper on
2026-05-27, the embedding sibling to the Gemini 3.5 family that landed
at I/O 2026 ([gemini-3-2-flash](./gemini-3-2-flash.md),
[gemini-3-5-pro](./gemini-3-5-pro.md), [gemini-omni](./gemini-omni.md)).

The pitch in the announcement framing: **a native multimodal embedding
model**, encoding text, image, audio, and video into a unified
embedding space — rather than text-only embeddings stitched to
modality-specific encoders. This sits naturally alongside Gemini Omni
(any-input, any-output generation) as the retrieval/representation half
of the same stack.

**Why this ticket sits at `confirmed`:** the whitepaper is a Google
DeepMind primary publication, but no pricing, API endpoint, or detailed
benchmark numbers are visible in the launch tweet alone. Upgrade
to `released` once a public API endpoint (`text-embedding-gemini-2-…`
or equivalent) and pricing land — Google's Gemini lane historically goes
whitepaper → AI Studio → Gemini API → Vertex AI within weeks.

**Transition triggers:**
- API endpoint / model card published on AI Studio or Vertex AI →
  `status: released`.
- Benchmark numbers (MTEB-multimodal, retrieval scores) disclosed →
  UPDATE with the comparator.
- ≥4 weeks past public availability with the release settled into
  normal coverage → `closed: released-and-aged`.

**Dedup note:** further Gemini Embedding 2 signal (pricing, benchmark
positioning, modality extensions, model-size variants like
`gemini-embedding-2-large`) UPDATES this ticket. A distinct Gemini
Embedding 3 or text-only-embedding refresh gets its own ticket.
