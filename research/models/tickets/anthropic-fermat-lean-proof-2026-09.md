---
slug: anthropic-fermat-lean-proof-2026-09
title: Claude completes the first formalized proof of Fermat's Last Theorem in Lean
company: Anthropic
model: Claude
status: confirmed
status_note: |
  @AnthropicAI, 2026-09-04: "**Last month, Claude completed the first formalized
  proof of Fermat's Last Theorem**, one of the most famous theorems of all time.
  This was a project experts thought would take many years. It is the largest
  Lean pro[ject]..." Anthropic's framing is about verification cost:
  checking that a major mathematical proof is correct can take years, and
  formalization into a proof assistant like **Lean** collapses that.

  Two things to keep separate. Claude did **not** prove Fermat's Last Theorem —
  Wiles did, in 1994. What Claude did is **formalize** an existing proof into
  machine-checkable Lean, which is a different and mechanically verifiable
  achievement: a Lean proof either compiles against the kernel or it does not,
  so the result is checkable in a way almost nothing else in AI capability
  reporting is.

  The scale claim propagating alongside it — that dozens of AI agents
  coordinated on a problem too large for one agent, compressing a multi-year
  project into ~11 days via an orchestration layer maintaining a shared
  dependency graph of mathematical tasks — comes from third-party relays
  (@ChainPulseAI1 and others), **not** from Anthropic's own post, and is
  recorded here as unconfirmed detail.

  Verification `confirmed` on Anthropic's own statement plus the inherent
  checkability of a Lean artifact. Status `confirmed` rather than `released`:
  this is a research result, not a product anyone can use.
expected: "Result announced 2026-09-04 for work completed 'last month'. Open: publication of the Lean project for independent compilation, and whether the multi-agent orchestration described by relays is documented by Anthropic."
labels:
  - anthropic
  - formal-methods
  - mathematics
  - multi-agent
verification: confirmed
sources:
  - https://x.com/AnthropicAI/status/2095947707605266436
  - "@ChainPulseAI1"
created_at: 2026-09-07
updated_at: 2026-09-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-07
    change: "Created — CONFIRMED. @AnthropicAI announced on 2026-09-04 18:50 UTC that Claude completed, during August, the first formalized proof of Fermat's Last Theorem — described as the largest Lean project of its kind and as work experts expected to take many years. Anthropic frames it around verification cost: checking a major proof can take years, and formalization into a proof assistant collapses that. Recorded precisely: Claude did NOT prove FLT (Wiles, 1994); it formalized an existing proof into machine-checkable Lean, which is a mechanically verifiable claim — a Lean proof compiles against the kernel or it does not. Verification confirmed on Anthropic's own statement plus the checkability of the artifact class. Status confirmed rather than released: a research result, not a usable product. NOT confirmed and recorded as third-party detail only: relays (@ChainPulseAI1 and others) claim dozens of agents coordinated through an orchestration layer maintaining a shared dependency graph of mathematical tasks, compressing the project into ~11 days; Anthropic's own post does not say this."
---

The reason this belongs on a model-timeline ticket rather than in a science
roundup is that it is one of the very few frontier-capability claims that is
falsifiable by machine. Benchmark scores are contested, agentic demos are
cherry-picked, and "AGI has arrived" is an opinion. A Lean development either
compiles against the kernel or it does not.

The precision matters and most coverage lost it. Claude did not prove Fermat's
Last Theorem. Wiles proved it in 1994. Claude translated that proof into a form
a computer can check — which is arguably the harder engineering problem, since
the informal proof runs to hundreds of pages of machinery that has to be built
up from foundations, and which is why formalizing it was expected to take years
of human effort.

The claim doing the most work in secondary coverage — dozens of agents
coordinating through a shared dependency graph, years compressed to eleven days
— is not in Anthropic's post. It may well be true; it is not sourced to
Anthropic here, so it stays labelled. If it is documented, it becomes the more
interesting result than the theorem, and it rhymes directly with Meta's
no-central-controller AIRA₃ architecture ([[meta-aira-3-2026-09]]) published the
following day.
