---
slug: microsoft-mai-base-2-2026-10
title: "Microsoft AI MAI-Base-2 — in-house ~3T-parameter pre-trained base model; post-training underway"
company: "Microsoft AI"
model: "MAI-Base-2"
status: confirmed
status_note: |
  **Announced by Microsoft AI's CEO, 2026-10-15 16:16 UTC.** @mustafasuleyman: "We
  now have state-of-the-art pre-trained base models in the 3T-parameter weight class,
  built entirely in-house at MAI. Post-training results coming soon." The thread
  names the model MAI-Base-2, claims a clean training run thanks to "careful scaling
  ladders", and says it matched DeepSeek-V4-Pro-Base's pre-trained held-out code score
  with 12x less training compute. It links a technical blog post. @satyanadella
  retweeted it.

  **Report details (secondary, @NextHub_API).** 2.8T total / 80B active parameters.
  Trained on 16,000 GB200 GPUs over 38 days in August-September. Microsoft plans to
  license the weights to trusted partners through Foundry. The 4.2-12.3x efficiency
  range is a scaling-law estimate against DeepSeek-V4-Pro-Base bits-per-byte, and the
  actual run used more FLOPs than that reference. No release date, serving price or
  access terms.

  This is a base model, not a usable product, which is why the status is `confirmed`
  and not `released`.
expected: "No date. Post-training 'coming soon'. Licensed weights for trusted partners via Foundry planned. Advances to released when a post-trained model or Foundry access ships."
labels:
  - microsoft
  - mai
  - base-model
  - pretraining
  - frontier-model
verification: confirmed
sources:
  - "https://x.com/mustafasuleyman/status/2110766651344146564"
  - "https://x.com/mustafasuleyman/status/2110766652875030948"
  - "https://x.com/mustafasuleyman/status/2110766656750575855"
  - "https://x.com/satyanadella/status/2110778673850941834"
  - "https://x.com/NextHub_API/status/2111035936331190695"
created_at: 2026-10-16
updated_at: 2026-10-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-16
    change: "Created — CONFIRMED / confirmed. Microsoft AI CEO @mustafasuleyman (2026-10-15 16:16 UTC, RT'd by @satyanadella) announced MAI-Base-2, a state-of-the-art pre-trained base model in the 3T-parameter class built entirely in-house, with post-training results 'coming soon'. He claims it matched DeepSeek-V4-Pro-Base's held-out code score using 12x less training compute, and links a technical blog post. Secondary detail from @NextHub_API's read of the technical report: 2.8T total / 80B active, 16,000 GB200s for 38 days in Aug-Sep, plans to license weights to trusted partners through Foundry, and no release date or price. The efficiency figure is a company scaling-law estimate. Company-primary, so verification confirmed; nothing usable has shipped, so status confirmed rather than released. Related Microsoft model tickets: [[microsoft-mai-transcribe-2-streaming-2026-10]], [[microsoft-decision-1-2026-10]]."
---

MAI-Base-2 is Microsoft's clearest statement yet that it is training frontier-scale
models itself rather than relying only on OpenAI. A 3T-class base model, trained
in-house, with a plan to license weights, puts MAI in a different category from its
earlier image, voice and transcription models.

The efficiency claim needs care. "12x less compute" is measured against
DeepSeek-V4-Pro-Base on held-out code bits-per-byte, using fitted scaling laws. It is
not a statement about the compute MAI-Base-2 actually used, which per the report was
more than the reference.

**Transition triggers:** post-training results or a named chat/agent model built on
MAI-Base-2 → UPDATE. Foundry weight licensing or API availability → `released`.
