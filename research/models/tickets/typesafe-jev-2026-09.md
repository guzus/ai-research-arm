---
slug: typesafe-jev-2026-09
title: Typesafe releases Jev — a non-chat "system one" decision model with free output tokens
company: Typesafe
model: Jev
status: released
status_note: |
  **Founder announcement, 2026-09-15 18:17 UTC.** @CompleteSkeptic: "After
  co-inventing ChatGPT, I kept asking myself: why have superhuman chat models
  not led to AGI? I've spent the last 2 years in stealth building a new way to
  train models (RLCD), and a new type of frontier AI model that we are
  releasing today: Jev • 20-200x faster • 40-400x cheaper (w/ output tokens
  free) • Frontier composable intelligence optimized for decisions." The
  company is @typesafeai, described by @SourceCodeplz as "built by former
  OpenAI staff."

  **What the product actually is, per a third-party reader of the launch
  post** (@VisheshBaghell, 2026-09-16): no chat, no free text — "just typed
  structured decisions with calibrated probabilities," with a fixed output
  schema fixed in advance, priced at **$0.042 per million input tokens with
  output free**, and ~70ms per call. The pitch is a "system one" model: a fast
  classifier-shaped decision layer, not a conversational model.

  **Treat the multipliers as marketing.** "20-200x faster / 40-400x cheaper"
  are ranges against an unnamed baseline, and comparing per-decision cost
  against a chat subscription — as the widely-shared third-party analysis does
  — compares different units of work. The architectural claim (constrained
  output schema removes free-form hallucination) is structurally true of any
  constrained-decoding system and is not novel by itself; the claim that
  matters is RLCD, the training method, and nothing about it was captured
  in-window.
expected: "Released with published pricing ($0.042/Mtok in, output free). Open: the RLCD training method's actual description, any independent benchmark, and whether 'decisions with calibrated probabilities' calibrate under third-party testing."
labels:
  - new-entrant
  - decision-model
  - pricing
  - structured-output
verification: partial
sources:
  - https://x.com/CompleteSkeptic/status/2099925682726002904
  - https://x.com/SourceCodeplz/status/2100174636377883004
  - https://x.com/VisheshBaghell/status/2100190919186419992
created_at: 2026-09-16
updated_at: 2026-09-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-16
    change: "Created — RELEASED. Typesafe (@typesafeai) released Jev on 2026-09-15, announced by its founder (@CompleteSkeptic, 2026-09-15 18:17 UTC), who describes himself as a co-inventor of ChatGPT and says the company spent two years in stealth building a new training method, RLCD, plus 'a new type of frontier AI model… optimized for decisions', claiming 20-200x faster and 40-400x cheaper with output tokens free. @SourceCodeplz (2026-09-16) confirms the company as Typesafe, 'built by former OpenAI staff', linking the announcement. A third-party reader of the launch post (@VisheshBaghell, 2026-09-16) describes the product concretely: no chat and no free text, only typed structured decisions with calibrated probabilities against an output schema fixed in advance, $0.042 per million input tokens with output free, ~70ms per call. Verification partial: the release and pricing are corroborated by three independent accounts but there is no model card, no benchmark and no independent evaluation, and the speed/cost multipliers are ranges against an unnamed baseline. The viral third-party cost comparison against a $100/mo Claude Max subscription compares different units of work and is NOT adopted here. The substantive open question is RLCD, which was named but not described."
---

**Jev** is a deliberately non-conversational model: fixed output schema, typed
structured decisions, calibrated probabilities, no free text. Typesafe
released it on 2026-09-15 with published pricing of **$0.042 per million input
tokens and free output**.

**Why it is worth tracking despite the marketing.** Almost every model in this
repo is a chat or agent model competing on capability per token. Jev is priced
and shaped as an *infrastructure component* — a decision call in a workflow,
at ~70ms, where output is free because the output is a schema field rather
than prose. If that category is real, it competes with classifiers and rules
engines, not with frontier models, and the correct comparison is to the
workflow logic it replaces.

**The comparison everyone is making is wrong.** The widely-shared analysis
divides $100 of Jev tokens into ~1.19M "decisions" and $100 of a Claude Max
subscription into ~11,250 messages, and reports 100x. Those are different
units of work: a decision with a fixed schema and a multi-turn agentic session
are not substitutable, and the founder's own framing ("system one") concedes
it. The price is interesting on its own terms; the ratio is not evidence.

**What would make the claim real.** RLCD. The entire differentiation rests on
a training method that was named and not described. Constrained decoding
against a schema is ordinary; producing *calibrated* probabilities under that
constraint is not, and calibration is measurable. Nobody has measured it.

**Credential caution.** "Co-inventor of ChatGPT" is a self-description and is
carried here as such. It is relevant to plausibility and it is not evidence
about the model.

**Transition triggers:**
- An RLCD paper, model card, or technical description → UPDATE, advance
  `verification`.
- Any independent calibration or accuracy evaluation → UPDATE; this is the
  load-bearing test.
- A named production customer → UPDATE.
- ≥4 weeks past release with the debate settled → `closed: released-and-aged`.
