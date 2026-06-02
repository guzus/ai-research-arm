---
slug: gemma-4
title: Gemma 4 — Google's open-weight multimodal family (E2B / E4B / 26B-A4B MoE / 31B dense)
company: Google / DeepMind
model: Gemma 4
status: closed
status_note: |
  Released **2026-04-02** under Apache 2.0 as Google DeepMind's open-weight
  multimodal family with four variants:
  **E2B** (~2.3B effective params, edge), **E4B** (~4.5B effective, edge),
  **26B-A4B** (Mixture-of-Experts with 128 small experts + 1 shared, only
  ~4B active per token — "near-31B quality at dramatically lower compute"),
  and a **31B dense** flagship. Native multimodal (text + image inputs;
  audio on smaller models, video via frame extraction), **256K context
  window**, 140+ languages, built-in agentic features (multi-step
  reasoning, function calling, thinking modes). Reported MoE-variant
  scores: **88.3% AIME 2026** with only 3.8B active parameters,
  **77.1% LiveCodeBench**. Distribution: Hugging Face
  (`google/gemma-4-26B-A4B`, `gemma-4-26B-A4B-it`) and DeepMind model
  page. In-cycle adoption signal: Hugging Models 2026-06-02 07:46 UTC
  cites **~11M downloads** for the 26B-A4B variant; secondary cap-markets
  framing (@EastonCapital, 2026-06-02 08:00 UTC) cites "$GOOGL rolled out
  Gemma 4" as part of an AI infrastructure / enterprise-agents push.
expected: null
labels:
  - released
  - open-weights
  - apache-2-0
  - multimodal
  - moe
  - dense
  - gemma-family
  - long-context
verification: confirmed
sources:
  - https://deepmind.google/models/gemma/gemma-4/
  - https://huggingface.co/google/gemma-4-26B-A4B
  - https://huggingface.co/google/gemma-4-26B-A4B-it
  - "@HuggingModels"
  - "@EastonCapital"
created_at: 2026-06-02
updated_at: 2026-06-02
closed_at: 2026-06-02
closed_reason: released-and-aged
history:
  - ts: 2026-06-02
    change: "Created — Gemma 4 family released 2026-04-02 under Apache 2.0 (Google DeepMind, primary deepmind.google/models/gemma/gemma-4/ + Hugging Face `google/gemma-4-26B-A4B[-it]`). Four variants: E2B (~2.3B effective, edge), E4B (~4.5B effective, edge), 26B-A4B MoE (~4B active per token, 128 small experts + 1 shared), 31B dense flagship. Native multimodal, 256K context, 140+ languages, agentic features (multi-step reasoning, function calling, thinking modes). Reported MoE scores: 88.3% AIME 2026, 77.1% LiveCodeBench. In-cycle adoption signal: HuggingModels 2026-06-02 07:46 UTC cites ~11M downloads for Gemma 4 26B-A4B; secondary $GOOGL framing positions Gemma 4 as part of the broader enterprise-agents push alongside the Gemini 3.5 lane. Ticket created late vs the 2026-04-02 release — this is the schema-compliant backfill of a release that wasn't tracked when it shipped"
  - ts: 2026-06-02
    change: "Closed — Same-cycle closure per the schema's `released-and-aged` rule: the underlying release shipped 2026-04-02, which is 61 days ago, well past the 4-week threshold. The ticket exists as a backfill record (so future consumers don't have a Gemma-shaped hole in the persistent set) but is moved straight to closed so it doesn't pollute the active-ticket dashboard. Re-opens via a new ticket if a Gemma 4 point release or successor ships"
---

**Gemma 4** is Google DeepMind's open-weight multimodal model family,
released on **2026-04-02** under **Apache 2.0**. This ticket backfills
the release into the persistent ticket set — Gemma 4 shipped before
the model-timeline pipeline started indexing Google's open-weight
lane, and the in-cycle adoption signal (~11M Hugging Face downloads
for the 26B-A4B variant cited 2026-06-02) made the lack of a tracking
ticket structurally visible.

**Family layout (four variants):**

- **E2B** — ~2.3B effective parameters, edge-optimised.
- **E4B** — ~4.5B effective parameters, edge-optimised.
- **26B-A4B** — Mixture-of-Experts (128 small experts + 1 shared,
  8 experts activated per token = ~4B active params). Designed to
  hit near-31B quality at dramatically lower compute.
- **31B dense** — flagship dense model for full-precision deployment.

**Capabilities:**

- **Native multimodal** — text + image inputs, audio on the smaller
  variants, video via frame extraction.
- **256K context window** — long-context support across the family.
- **140+ languages** — broad multilingual coverage on the dense and
  MoE tiers.
- **Agentic features** — multi-step reasoning, function calling,
  thinking modes built into the base release.

**Reported benchmarks (MoE variant):**

- **88.3% AIME 2026** mathematics with only 3.8B active parameters.
- **77.1% LiveCodeBench** competitive coding.

**Distribution.** Hugging Face (`google/gemma-4-26B-A4B`,
`google/gemma-4-26B-A4B-it`) + the DeepMind model page. The MoE
variant in particular is positioned as the cost-efficient option for
on-prem and self-hosted deployments.

**Why this is its own ticket** rather than rolling into a Gemini-family
ticket: Gemma is Google's named open-weight brand. The closed-source
Gemini line ([[gemini-3-2-flash]], [[gemini-3-5-pro]], [[gemini-omni]],
[[gemini-embedding-2]]) ships through Google's own API + Vertex AI; Gemma
ships through Hugging Face under Apache 2.0 and competes for the open-
weights mind-share against MiniMax M3 ([[minimax-m3]]), Nemotron 3 Ultra
(see [[nvidia-gtc-taipei-2026-06]]), Cosmos 3 (also on the NVIDIA bundle),
and the DeepSeek family.

**Transition triggers:**

- A Gemma 4 point release (Gemma 4.1, Gemma 4 Ultra, etc.) → new ticket
  and link back here.
- Independent reproduction of the 26B-A4B AIME/LiveCodeBench scores via
  Artificial Analysis / EleutherAI / Open LLM Leaderboard → UPDATE.
- Successor family (Gemma 5) → new ticket, close this one with
  `closed_reason: superseded-by:<slug>`.
- Routine aging (this ticket is being backfilled past the 4-week window
  for `released-and-aged`); the next CRUD cycle's closure sweep will
  age-close it under `released-and-aged` per the schema.

**Dedup note:** further Gemma 4 signal (point releases, benchmark
verification, adoption milestones, license / weight-format updates)
UPDATES this ticket. Gemma 5 or a rebrand gets its own ticket.
