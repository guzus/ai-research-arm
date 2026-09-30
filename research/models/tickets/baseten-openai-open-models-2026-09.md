---
slug: baseten-openai-open-models-2026-09
title: Baseten serves GLM-5.3 Flash and Kimi K3 inside Codex, billed against OpenAI commits
company: OpenAI / Baseten
model: null
status: confirmed
status_note: |
  **Company-primary, from the vendor doing the serving.** @philipkiely (Baseten),
  2026-09-29 18:22 UTC, ~1,341 likes: "Enterprise teams can now use open models
  like GLM-5.3 Flash and Kimi K3 natively in Codex and count spend against their
  OpenAI commit."

  **The mechanism is the story, not the model list.** Per @stretchcloud's read,
  Baseten is serving open models natively inside **Codex and the Responses API**
  as one of the first inference providers in **OpenAI's new B2B Marketplace**, and
  the spend lands against an OpenAI commitment the customer has already signed —
  "No new PO, no separate vendor, no waiting on procurement to approve a second AI
  budget line." Procurement friction, not capability, is what this removes.

  **The models are not filler.** Kimi K3 is quoted at **$3 / $15 per Mtok in/out
  with a $0.30 cache-hit rate, a 1M-token context window and open weights**
  ([[moonshot-kimi-k3]], closed released-and-aged); GLM-5.3 Flash sits alongside
  it as the budget option and is the same profile currently routed in this repo's
  own editorial lanes.

  **The strategic argument, recorded as argument.** @stretchcloud contrasts Codex
  — bring-your-own-model, open-source harness — with Claude Code, which stays
  closed and pinned to Anthropic's own models, citing Gergely Orosz making the
  same point the same week. His conclusion is a prediction, not reporting: that
  Anthropic eventually copies this once enough enterprises ask why their AI budget
  is locked to one lab's roadmap.

  **Direct consequence for an open ticket.** If routing becomes a free feature
  inside frontier labs' own coding agents, the thing Stripe is reportedly paying
  ~$7B for at [[stripe-openrouter-acquisition-2026-08]] — a 5% commission on
  cross-model API flow, ~$160M annualized — is a toll booth on a road one of the
  destinations is now paving itself. That is the sharpest reason this event gets a
  ticket rather than a footnote.
expected: "ANNOUNCED/LIVE 2026-09-29 for enterprise teams. Open: a primary OpenAI statement about the B2B Marketplace itself (nothing in signal from OpenAI's own handle); which other inference providers are in it; the full list of eligible open models and who decides it; the commercial terms between OpenAI and the providers; and whether 'count spend against their OpenAI commit' means OpenAI is reselling third-party inference or merely crediting it."
labels:
  - openai
  - baseten
  - open-weights
  - codex
  - marketplace
verification: partial
sources:
  - https://x.com/philipkiely/status/2105000178709360963
  - https://x.com/stretchcloud/status/2105148884917891192
created_at: 2026-09-30
updated_at: 2026-09-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-30
    change: "Created — CONFIRMED / partial. @philipkiely of Baseten announced on 2026-09-29 18:22 UTC that enterprise teams can now use open models including GLM-5.3 Flash and Kimi K3 natively in Codex, with the spend counting against their existing OpenAI commit (~1,341 likes, ~72 RTs). Company-primary from one side of the deal; verification is partial because OpenAI has said nothing about it in this cycle's fetch and the B2B Marketplace framing comes from @stretchcloud's analysis rather than from either company. What that analysis adds: Baseten is described as one of the first inference providers inside OpenAI's new B2B Marketplace, serving open models natively in Codex and the Responses API, with the pitch being day-zero availability whenever a serious open model ships. THE LOAD-BEARING MECHANISM IS PROCUREMENT, NOT CAPABILITY — 'no new PO, no separate vendor, no waiting on procurement to approve a second AI budget line' — which is why this is a distribution event rather than a model event. Model economics as quoted: Kimi K3 at $3/$15 per Mtok with a $0.30 cache-hit rate, 1M context and open weights ([[moonshot-kimi-k3]]); GLM-5.3 Flash as the budget tier. DIRECT CONSEQUENCE FOR AN OPEN TICKET, and the main reason this is tracked: if a frontier lab offers cross-model routing free inside its own coding agent, billed against commitments enterprises already signed, that undercuts the asset in [[stripe-openrouter-acquisition-2026-08]] — a 5% commission on routed flow at ~$160M annualized, reportedly being bought for ~$7B. Recorded as an argument about durability, not as evidence about the deal. Also recorded as argument and not fact: @stretchcloud's contrast of Codex (bring-your-own-model, open-source harness) against Claude Code (closed, Anthropic models only), and his prediction that Anthropic follows. Distinct from [[nvidia-nemotron-openrouter-2026-06]] (a model landing on a router) because here the ROUTER FUNCTION is moving inside a frontier lab's own product."
---

The interesting number in this announcement is zero: the number of new vendor
relationships an enterprise needs in order to start running Chinese open-weight
models in production.

That is the whole move. Kimi K3 and GLM-5.3 Flash were already available, already
cheap, already open. What was missing was a way to pay for them that did not
require a second procurement cycle, a second security review and a second budget
line — which, inside a large company, is often the difference between a model being
technically available and actually usable. Routing the spend through an OpenAI
commitment the customer has already negotiated removes all three at once.

It also means OpenAI is now, in a limited way, in the business of selling other
people's models. That is a strange position for a lab whose pitch has been its own
frontier, and the logic only works if you believe commitment capture matters more
than model share: better that an enterprise burns its committed dollars on a
competitor's open weights inside Codex than that it opens an account somewhere
else and starts comparing.

The casualty, if this pattern holds, is the independent router. OpenRouter built a
nine-figure business on being the neutral place to compare and switch models, and
took 5% of the flow for it. A frontier lab bundling the same function into the
coding agent its customers already live in does not need to be better at routing —
it needs only to be free and already paid for. Whether that is fatal or merely
compressive is exactly the question Stripe is reportedly answering with $7 billion
([[stripe-openrouter-acquisition-2026-08]]).

What is missing from the record is OpenAI's own voice. Every detail here comes from
the partner or from an analyst reading the partner. A B2B Marketplace with
third-party inference providers is a significant platform commitment, and until
OpenAI describes it, the terms — who qualifies, who sets the model list, what
margin changes hands — are unknown.
