---
slug: sakana-fugu-2026-06
title: Sakana AI ships "Fugu" — orchestration-as-a-model
company: Sakana AI
model: Sakana Fugu
status: released
status_note: |
  On **2026-06-22** Japan's **Sakana AI** released **Sakana Fugu**, a multi-agent
  orchestration system exposed as a **single, OpenAI-API-compatible model**. Its
  top **"Fugu Ultra"** tier is pitched as **matching Fable- and Mythos-class
  performance** on engineering, science, and reasoning benchmarks — not by being
  a bigger base model, but by training an LLM to **dynamically route tasks across
  a pool of frontier models** (including recursive calls to itself). Tiered
  Ultra/Pro/Standard with credit/subscription pricing; drop-in for Codex-style
  clients (repoint `base_url`).

  **Confirmed vs. claimed:** the *release* is multi-source confirmed — official
  @SakanaAILabs announcement + blog, GIGAZINE coverage, heavy JP/EN developer
  chatter. The **"matches Fable/Mythos" parity is vendor-self-reported**; no
  neutral leaderboard has reproduced it. Key correction: Fugu is an
  **orchestrator, not a new frontier base model** — "matches Fable/Mythos" is an
  ensemble-routing claim over existing models. As one critic put it, "Fugu turns
  the frontier-model race into an orchestration race," a different (and weaker)
  claim than out-modeling OpenAI/Anthropic. Irony given the export saga: an
  orchestrator that routes to Anthropic/OpenAI/Google models inherits exactly the
  access risk that took Fable 5 offline for non-US users
  ([[anthropic-fable-mythos-export-control-2026-06]]).
expected: "Shipped — live via an OpenAI-compatible API, tiered Ultra/Pro/Standard. Vendor-reported Fable/Mythos parity awaiting independent benchmarks; orchestration (not a new base model)"
labels:
  - released
  - orchestration
  - japan
  - agents
verification: confirmed
sources:
  - "@SakanaAILabs"
  - https://x.com/SakanaAILabs/status/2068861630327443966
  - https://x.com/SakanaAILabs/status/2068862070062485867
created_at: 2026-06-22
updated_at: 2026-06-22
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-22
    change: "Created — Sakana AI released Sakana Fugu (2026-06-22): a multi-agent orchestration system exposed as a single OpenAI-API-compatible model, whose 'Fugu Ultra' tier is pitched as matching Fable/Mythos-class performance by dynamically routing across a pool of frontier models (incl. recursive self-calls). Release multi-source confirmed (official @SakanaAILabs announcement + blog, GIGAZINE, heavy JP/EN dev chatter) → status released, verification confirmed. Caveat: parity benchmarks are vendor-self-reported and Fugu is an orchestrator, not a new base model; lands 9 days into the Anthropic Fable 5/Mythos export freeze. Sources: @SakanaAILabs launch + how-it-works + benchmark posts."
---

**Sakana Fugu**, from Japan's **Sakana AI**, is a multi-agent **orchestration
system delivered as a single model API**. Released 2026-06-22, it's
OpenAI-API-compatible (a drop-in for Codex/LangChain-style clients) with a paid
**Ultra/Pro/Standard** tiering. The headline claim: **"Fugu Ultra" matches the
performance of Fable and Mythos**, delivering frontier capability without a new
frontier base model.

**How it works.** Per Sakana, Fugu "is itself an LLM, trained to call various
LLMs in an agent pool, including instances of itself recursively," dynamically
orchestrating "the world's best models." The capability comes from **routing**,
not from a larger pretrained model.

**Why `released` / `confirmed`.** It's live and usable via the API, and the
release is corroborated across the official @SakanaAILabs thread + blog,
GIGAZINE, and a wave of Japanese builders — so `released` / `confirmed`. The
**parity claim is the unverified part**: the "matches Fable/Mythos" benchmarks
are self-reported, with no neutral leaderboard yet. The honest framing is that
Fugu is an **orchestrator** — "matches Fable/Mythos" is an ensemble claim over
existing models, not proof of out-modeling the frontier labs.

**Why it matters.** Fugu lands directly in the vacuum opened by the **Fable 5
foreign-access cutoff** ([[anthropic-fable-mythos-export-control-2026-06]]),
released "nine days after" the US order per JP coverage, and extends the
"route-across-models" trend. The irony: an orchestrator that depends on
third-party frontier models — some now export-gated — inherits the very
access risk that just took Fable 5 offline for non-US users, which could become
a supply constraint rather than a moat.

**Transition triggers:**
- Independent reproducible benchmarks of Fugu Ultra vs Fable/Mythos → UPDATE,
  refine verification on the *parity* claim.
- A successor or major capability revision → new ticket; do not reopen.
- ≥4 weeks past release, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further Sakana Fugu release/benchmark signal UPDATES this
ticket. Open-weight contenders stay on their own tickets ([[zhipu-glm-5-2]],
[[minimax-m3]]); the export order stays on
[[anthropic-fable-mythos-export-control-2026-06]].
