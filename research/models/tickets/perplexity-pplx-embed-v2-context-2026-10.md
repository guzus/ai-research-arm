---
slug: perplexity-pplx-embed-v2-context-2026-10
title: "Perplexity pplx-embed-v2-context-9b-preview — open-weight contextual chunk-embedding model"
company: "Perplexity"
model: "pplx-embed-v2-context-9b-preview"
status: released
status_note: |
  **Single secondary source, 2026-10-12 15:38 UTC (@RodrigoESPorto):** Perplexity's
  **pplx-embed-v2-context-9b-preview** embeds each chunk while seeing the whole
  document in one pass. Preview weights are on Hugging Face. Per the company:
  Matryoshka vectors at 1024/2048 dims, int8-aware training, documents up to
  32,768 tokens. It claims SOTA on ConTEB and on turbopuffer's private
  context-bench, and +14.4 points of answer recall over voyage-context-4.

  **Caveats the relay itself flags:** the rankings are Perplexity's own,
  context-bench is not publicly reproducible, the name says 9B while the HF card
  reportedly says 8B, and there is no API yet.

  **Status `released`** (weights reportedly downloadable). **Verification
  `unverified`:** one relay; no Perplexity post or HF URL captured in this fetch.
expected: "Preview weights on Hugging Face per relay; no API. Watch for a Perplexity post, the HF card URL and licence, and independent ConTEB results."
labels:
  - perplexity
  - embeddings
  - open-weights
  - retrieval
verification: unverified
sources:
  - "https://x.com/RodrigoESPorto/status/2109669934020104571"
created_at: 2026-10-12
updated_at: 2026-10-12
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-12
    change: "Created — RELEASED / unverified. @RodrigoESPorto (2026-10-12) reports Perplexity released preview weights for pplx-embed-v2-context-9b-preview on Hugging Face: whole-document contextual chunk embeddings, Matryoshka 1024/2048 dims, int8-aware, up to 32K-token documents, self-claimed SOTA on ConTEB and +14.4 pts answer recall vs voyage-context-4. Name/card size mismatch (9B vs 8B) and no API. Single relay; advances verification on a Perplexity post or HF URL."
---

Related Perplexity retrieval-stack release: [[perplexity-photon-fast-search-2026-09]].
