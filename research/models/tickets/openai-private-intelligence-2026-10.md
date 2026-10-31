---
slug: openai-private-intelligence-2026-10
title: "OpenAI announces Private Intelligence — enterprise data-privacy controls for its most capable models"
company: OpenAI
model: null
status: confirmed
status_note: |
  **First-party, 2026-10-30 15:12 UTC.** @OpenAI: "Privacy should advance as fast as intelligence.
  OpenAI Private Intelligence gives businesses stronger controls over their data while using our most
  capable models. We're building these protections in close collaboration with some of our largest
  customers to help businesses apply frontier AI to their most sensitive work."

  **Why `confirmed`, not `released`:** the post does not say what the controls are, which tiers get
  them, or whether they are generally available. "We're building" suggests at least part of it is
  still rolling out.
expected: "Announced 2026-10-30. Open: the specific controls (e.g. retention, key management, isolation), tier and price, and general availability."
labels:
  - enterprise
  - privacy
  - data-controls
verification: confirmed
sources:
  - https://x.com/OpenAI/status/2116186509384815084
created_at: 2026-10-31
updated_at: 2026-10-31
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-31
    change: "Created — CONFIRMED / confirmed. @OpenAI (2026-10-30 15:12 UTC) announced OpenAI Private Intelligence, which gives businesses 'stronger controls over their data while using our most capable models' and is being built 'in close collaboration with some of our largest customers' for their most sensitive work. The tweet gives no feature list, tier or pricing, and no general-availability statement."
---
This is OpenAI's answer to the objection that keeps coming up in regulated verticals: privileged or
regulated data cannot simply be sent to a shared cloud and billed per token. The same signal includes
a critique of OpenAI's legal configuration on exactly that point
([[openai-gpt-6-astra-law-2026-10]]).

Until the controls are named, this is a positioning announcement. What would make it material is
customer-managed keys, guaranteed zero retention, or dedicated or isolated inference for frontier
models. Any of those would directly address the law, health and finance buyers OpenAI is pursuing.
