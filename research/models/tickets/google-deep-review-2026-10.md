---
slug: google-deep-review-2026-10
title: "Google Research opens Deep Review to the public, expanding from peer review to general documents, with an API"
company: "Google / Google Research"
model: "Deep Review"
status: released
status_note: |
  **Primary.** @GoogleResearch (2026-10-14 18:54 UTC, Research@ event): after
  deployments across 16K+ submissions at STOC, ICML, NeurIPS and ICLR, Deep Review is
  expanding from scientific peer review to "rigorous, grounded verification for
  knowledge documents, including Google Docs & presos. Try it today."

  **Detail from a secondary summary (@CalatheaAI):** documents are split into
  sections, with more compute spent on harder passages. Parallel agents check the
  sections and a final agent merges the findings and checks them against outside
  sources. Users get two free reviews per week, with extras billed at Gemini API rates
  using their own key. A Deep Review API was announced. Input is PDF and plain text,
  with Docs/Slides listed in the FAQ and multi-file support still coming. Uploads are
  kept for up to a year, and training on them is opt-in.
expected: "Released 2026-10-14 (public, metered). Open: API GA/pricing page, the underlying model (presumably Gemini 4 Argon or 3.8), and multi-file support."
labels:
  - google
  - agents
  - verification
  - research-tools
  - released
verification: confirmed
sources:
  - "https://x.com/GoogleResearch/status/2110444265608458512"
  - "https://x.com/CalatheaAI/status/2110698709885599844"
created_at: 2026-10-15
updated_at: 2026-10-15
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-15
    change: "Created — RELEASED / confirmed. @GoogleResearch announced at its Research@ event (2026-10-14 18:54 UTC) that Deep Review, previously deployed on 16K+ submissions at STOC, ICML, NeurIPS and ICLR, now extends to general knowledge documents including Google Docs and presentations, with 'Try it today'. A secondary summary (@CalatheaAI, 2026-10-15) adds: sectioned review with adaptive compute, parallel checking agents plus a final agent that consolidates and checks against outside sources, two free reviews per week, extra reviews billed at Gemini API rates with the user's own key, a Deep Review API, PDF and plain-text input (Docs/Slides in the FAQ, multi-file pending), and up-to-a-year retention with opt-in training. This is the first Deep Review ticket; Google's model-line tickets such as [[google-gemini-4-2026-09]] are separate."
---
This is an agentic product built on Google's models, not a model release. It
goes in the ticket set because it is a public launch with an API and metered
pricing, and because the design (adaptive compute per section, parallel verifier
agents, an external-source cross-check) is the same pattern labs now ship as
"deep research" features, here applied to checking instead of writing.

The 16K-paper deployment history at top ML and theory venues is unusually strong
evidence that the tool was used before the public launch.
