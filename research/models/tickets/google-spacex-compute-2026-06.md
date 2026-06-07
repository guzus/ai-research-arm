---
slug: google-spacex-compute-2026-06
title: Google–SpaceX $920M/month compute pact (~110K NVIDIA GPUs through 2029)
company: Google / DeepMind / SpaceX
model: null
status: confirmed
status_note: |
  Multi-outlet reporting (TechCrunch, CNBC, The Decoder, 2026-06-05/06) says
  **Google will pay SpaceX ~$920M/month** — roughly **$30B through June 2029** —
  for access to about **110,000 NVIDIA GPUs**, with a Google representative
  describing the deal as a response to unexpected demand for its recently
  launched AI products (Gemini Enterprise). The dollar figure and GPU count are
  consistent across outlets and Google-rep-confirmed, so the *existence* of the
  pact is confirmed. The **mechanism/direction is contested**: CNBC frames the
  capacity as sitting at **xAI/SpaceX data centers**, and analysts on X flagged
  the intuitive "SpaceX resells GPUs to GPU-rich Google" arrow as backwards —
  the credible read is Starlink/space-linked or SpaceX-operated data-center
  capacity, not SpaceX reselling NVIDIA silicon. Awaiting SpaceX S-1 language
  to nail the structure.
expected: "Term runs through June 2029; SpaceX S-1 / preliminary prospectus expected to clarify structure"
labels:
  - compute
  - partnership
  - infrastructure
  - nvidia-gpu
  - spacex
verification: partial
sources:
  - https://techcrunch.com/2026/06/05/google-will-pay-spacex-920m-per-month-for-compute/
  - https://the-decoder.com/spacex-signs-920-million-per-month-deal-with-google-for-110000-nvidia-ai-chips-ahead-of-ipo/
  - https://www.cnbc.com/2026/06/05/google-to-pay-spacex-920-million-a-month-for-xai-compute-capacity.html
  - "@SawyerMerritt"
  - "@WorldBriefDaily"
created_at: 2026-06-07
updated_at: 2026-06-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-07
    change: "Created — Google to pay SpaceX ~$920M/month (~$30B through June 2029) for ~110K NVIDIA GPUs, confirmed by a Google rep as a response to unexpected demand for its AI products (TechCrunch 2026-06-05; CNBC; The Decoder 2026-06-06). 784-comment HN thread (2026-06-07) treats it as the largest publicly disclosed compute-procurement contract. Existence confirmed; mechanism/direction contested (CNBC ties capacity to xAI/SpaceX data centers; X analysts call the 'SpaceX resells GPUs to Google' framing backwards) → confirmed / partial pending SpaceX S-1"
---

A reported **$920M/month compute pact between Google and SpaceX** — roughly
**$30B through June 2029** for access to about **110,000 NVIDIA GPUs** —
surfaced across primary tech press on 2026-06-05/06. TechCrunch carried a
Google representative describing the deal as a result of **unexpected demand
for Google's recently launched AI products** (Gemini Enterprise); CNBC and The
Decoder corroborated the same dollar figure and GPU count.

**Why this is its own ticket.** It is a discrete, very large infrastructure
partnership distinct from the existing
[anthropic-spacex-colossus-2026-05](./anthropic-spacex-colossus-2026-05.md)
compute arrangement — different counterparties (Google rather than Anthropic),
and on the SpaceX side the capacity is reportedly co-located with **xAI's
Colossus-class data centers** (per CNBC's framing).

**Why `partial`, not fully `confirmed`.** The *existence* of the deal is
multi-source and Google-rep-acknowledged, but the **mechanism is contested**.
The intuitive arrow — a GPU-rich, TPU-building Google paying SpaceX for compute
— is backwards, and at least one X analyst called the "SpaceX sells NVIDIA GPUs
to Google" framing likely wrong. The credible read is space/Starlink-linked
infrastructure capacity or SpaceX-operated data-center buildout. Until SpaceX's
S-1 / preliminary prospectus specifies who supplies what to whom, the dollar
figure is more solid than the narrative.

**Transition triggers:**
- SpaceX S-1 or an official Google/SpaceX statement clarifying the structure →
  UPDATE, advance verification.
- Confirmed term changes (size, duration, GPU count) → UPDATE.
- Deal scrapped or materially restructured → `closed` with the appropriate
  reason.

**Dedup note:** further Google–SpaceX compute-pact signal UPDATES this ticket.
Anthropic–SpaceX compute stays on [[anthropic-spacex-colossus-2026-05]].
