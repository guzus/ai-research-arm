---
slug: anthropic-flashprove-2026-11
title: "Anthropic FlashProve — open-source prototype for cryptographically proving which model produced a response"
company: Anthropic
model: FlashProve
status: released
status_note: |
  **Secondary reports, 2026-11-03.** @TheBlockCo (14:16 UTC), quoting @TheLatentCo: "Anthropic
  unveiled FlashProve, an open-source prototype that uses cryptographic proofs to verify whether AI
  responses came from the claimed model without revealing its weights." It was developed with help
  from Claude and with contributions from StarkWare co-founder Alessandro Chiesa, among others.
  The stated uses are detecting model substitution, identifying tampering and supporting AI oversight.

  @matteoikari ties it to Anthropic's research post "Progress on provable inference for large
  language models". @kudodefi describes it as zkSNARK-based, aimed at resellers who sell "Opus 5.5"
  but serve another model.

  No @AnthropicAI post about it is in this run's signal. Status is `released` because the
  prototype is reported as open source. It is a research prototype, not a product.
expected: "Released 2026-11-03 or shortly before (open-source prototype, per secondary reports). Open: Anthropic's own post, repo location, licence, proof cost and latency, and supported model sizes."
labels:
  - research
  - open-source
  - verification
  - cryptography
  - anthropic
verification: partial
sources:
  - "https://x.com/TheBlockCo/status/2117621899454976344"
  - "https://x.com/matteoikari/status/2117622297225756798"
  - "https://x.com/kudodefi/status/2117621215124942936"
  - "@TheLatentCo"
created_at: 2026-11-03
updated_at: 2026-11-03
closed_at: null
closed_reason: null
history:
  - ts: 2026-11-03
    change: "Created — RELEASED / partial. Several secondary accounts on 2026-11-03 (@TheBlockCo quoting @TheLatentCo, @matteoikari, @kudodefi) report that Anthropic unveiled FlashProve. It is an open-source prototype that uses zero-knowledge proofs to show a response came from the claimed model without revealing the weights. It was built with help from Claude and with contributions from StarkWare co-founder Alessandro Chiesa, and is linked to Anthropic's research 'Progress on provable inference for large language models'. No first-party Anthropic post is in this run's signal, so verification is partial."
---

FlashProve addresses a known problem: users cannot verify which model actually answered. Resellers
and intermediaries can quietly swap a cheaper model for the one a customer pays for. The Claude Haiku
5.5 reseller sightings tracked at [[anthropic-haiku-5-5-2026-10]] show why this matters.

A cryptographic proof of model identity that keeps the weights secret would also help oversight and
third-party audits, such as the external evaluation access tracked at
[[anthropic-metr-third-party-evaluation-2026-10]].

The practical question is cost. Zero-knowledge proofs over frontier-scale inference have been far too
expensive to use. A "prototype" label suggests this works on small models or proof sketches, not
production Claude serving.

**Transition triggers:** Anthropic's own post or repository → verification `confirmed`; deployment in
the Claude API or a cloud partner → new history entry; ≥4 weeks after release → close as
released-and-aged.
