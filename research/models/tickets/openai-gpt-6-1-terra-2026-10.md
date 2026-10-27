---
slug: openai-gpt-6-1-terra-2026-10
title: "GPT-6.1 Terra — OpenAI's low-cost computer-use model, live in ChatGPT, Codex and the API"
company: "OpenAI"
model: "GPT-6.1 Terra"
status: released
status_note: |
  **First-party, 2026-10-26 18:06 UTC (@OpenAI, three-post thread).** "GPT-6.1 Terra:
  delivering fast and capable computer use at a lower price." OpenAI says it substantially
  outperforms GPT-5.6 Terra on Agents' Last Exam, matches GPT-6 Astra "at one-tenth the
  price per token", and finishes tasks over 3x faster on average than Astra and GPT-6.1 Sol.
  It is rolling out to Plus, Pro, Enterprise and Edu users in ChatGPT Work and Codex, and to
  developers as `gpt-6.1-terra`. @sama: "especially excited for this new era of computer use."

  **Pricing and third-party read.** @ArtificialAnlys (quoted by @KM15528116): $1 / $5 per
  million input/output tokens, against $2 / $12 for GPT-5.6 Terra; cached input $0.05. It gains
  6 Intelligence Index points over GPT-5.6 Terra at max effort, at under a third of the cost per
  task ($0.40 vs $1.40), and scores 4 points below GPT-6.1 Sol. Its Coding Agent Index v2.0 score
  is 48 (Sol 54, GPT-6 Luna 31). Its AA-Omniscience hallucination rate fell from 88% to 38%.
  Relays of OpenAI's launch post add Terminal-Bench 4.0 at 50.3% vs 21.5% for the predecessor.
expected: "Released 2026-10-26. Watch: free-tier availability, independent computer-use evals, and the rumored GPT-6.1 Astra."
labels:
  - frontier-model
  - computer-use
  - api
  - pricing
  - openai-gpt-6-family
verification: confirmed
sources:
  - "https://x.com/OpenAI/status/2114780711664398349"
  - "https://x.com/OpenAI/status/2114780717188272382"
  - "https://x.com/OpenAI/status/2114780720170164735"
  - "https://x.com/sama/status/2114818620782248024"
  - "https://x.com/KM15528116/status/2115058292968063333"
  - "https://x.com/HypePakistan/status/2115058434005446937"
created_at: 2026-10-27
updated_at: 2026-10-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-27
    change: "Created — RELEASED / confirmed. @OpenAI (2026-10-26 18:06 UTC) launched GPT-6.1 Terra for computer use: it matches GPT-6 Astra on Agents' Last Exam at one-tenth the price per token and runs over 3x faster than Astra and GPT-6.1 Sol. It is rolling out to Plus/Pro/Enterprise/Edu in ChatGPT Work and Codex, and in the API as gpt-6.1-terra. @ArtificialAnlys puts it at $1/$5 per Mtok (GPT-5.6 Terra: $2/$12), +6 Intelligence Index points over GPT-5.6 Terra at under a third of the cost per task, and a hallucination rate down from 88% to 38%."
---
OpenAI's GPT-6.1 Terra is the first Terra-class model since GPT-5.6. It fills the cheap, fast slot
below [[openai-gpt-6-1-sol-2026-09]] and GPT-6 Astra ([[openai-gpt-6]]). The pitch is cost per
task more than raw intelligence: per OpenAI it ties Astra on Agents' Last Exam at a tenth of the
token price.

Artificial Analysis independently confirms the price-performance claim at low and medium effort,
where Terra is on the cost-efficiency frontier. At max effort it trails Sol by 4 Intelligence Index
points. The hallucination drop (88% to 38% on AA-Omniscience) matters more for unattended
computer-use agents than any benchmark gain.

`released` / `confirmed`: OpenAI's own account announced it, the model is live in ChatGPT and the
API, and a third party measured it on day one.
