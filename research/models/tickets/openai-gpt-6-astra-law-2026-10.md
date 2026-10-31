---
slug: openai-gpt-6-astra-law-2026-10
title: "OpenAI lists gpt-6-astra-law on its API pricing page as a 'Legal model configuration'"
company: OpenAI
model: gpt-6-astra-law
status: confirmed
status_note: |
  **Pricing-page listing, surfaced 2026-10-31 by relays.** @saiitoshii: "OpenAI just slipped
  gpt-6-astra-law onto its API pricing page with zero announcement", filed under "Legal model
  configuration" at $10 input / $50 output / $1 cached per 1M tokens, with promo pricing through
  Dec 31. @lucasjamali links the pricing-page listing and OpenAI's September 17 announcement.
  @BasMondragon says this is the same price as GPT-6 Astra, and that per the September announcement
  it is Astra with a legal search index and legal instructions on top, with 26 plugins and Harvey and
  Legora building on it.

  **Why `confirmed` / `partial`:** the listing is reported to be on an official OpenAI page, and three
  independent accounts describe it consistently. This desk has not read the page itself, and no OpenAI
  post announced the API listing.
expected: "Listed on the API pricing page by 2026-10-31; promo pricing through 2026-12-31. Open: first-party docs/model card, availability terms, and whether more vertical Astra configurations follow."
labels:
  - legal
  - vertical-model
  - api
  - pricing
verification: partial
sources:
  - https://x.com/saiitoshii/status/2116476301359931622
  - https://x.com/lucasjamali/status/2116476943650414612
  - https://x.com/BasMondragon/status/2116487222870327546
created_at: 2026-10-31
updated_at: 2026-10-31
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-31
    change: "Created — CONFIRMED / partial. Relays (@saiitoshii, @lucasjamali, @BasMondragon, 2026-10-31 10:24–11:07 UTC) report that gpt-6-astra-law appeared on OpenAI's API pricing page under 'Legal model configuration' without an announcement. Reported price: $10 input / $50 output / $1 cached per 1M tokens, promo pricing through Dec 31, the same as GPT-6 Astra. Per the relays, OpenAI's September 17 announcement describes it as Astra plus a legal search index and legal instructions, with 26 plugins and Harvey and Legora as builders. Verification partial: consistent multi-account reports of an official page, but this desk has not read the page and there is no first-party post."
---
The price is the tell. If a vertical model costs exactly what its base model costs, it is a
configuration (retrieval index, system instructions, plugins), not a separately trained model. One
relay says OpenAI's own September announcement describes it that way.

The commercial question is whether configurations like this can win regulated buyers when the data
still leaves the firm. A relay makes that critique directly. OpenAI's same-week enterprise privacy
announcement ([[openai-private-intelligence-2026-10]]) looks like the intended answer.

**Transition trigger:** first-party docs or a model card showing general API access → `released`.
