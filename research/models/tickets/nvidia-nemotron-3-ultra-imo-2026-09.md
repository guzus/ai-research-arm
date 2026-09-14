---
slug: nvidia-nemotron-3-ultra-imo-2026-09
title: Nemotron 3 Ultra — IMO gold-medal score with the full recipe open-released
company: NVIDIA
model: Nemotron 3 Ultra
status: released
status_note: |
  NVIDIA's **Nemotron 3 Ultra** system scored **30/42 at the 2026 International
  Mathematical Olympiad** — gold-medal territory — using **natural-language
  proofs only**: no formal theorem prover, no external tools, no internet
  access. Architecture per @mark_k (2026-09-13 12:18 UTC): three checkpoints
  generate, verify and refine candidate proofs, then a high-compute stage
  selects the final answer.

  **The release, not the score, is what makes this a ticket.** NVIDIA published
  the two specialist checkpoints, the training data, training and inference
  code, the submitted solutions, and a **new benchmark of 200 olympiad-level
  problems**. That is an enumerated artifact list, not a benchmark screenshot —
  which is why this is `released` rather than a capability claim.

  **Verification `partial`, and the gap is named:** no NVIDIA first-party post,
  model card, repository link, licence or weights URL was captured in this
  cycle's fetch. Everything above comes from one relay describing an NVIDIA
  release. The claims are unusually checkable — a published benchmark and
  released checkpoints either exist at a URL or they do not — so this should
  resolve to `confirmed` or collapse quickly on the next cycle.

  Context worth keeping straight: NVIDIA's open-model line was previously
  tracked at [[nvidia-nemotron-openrouter-2026-06]] (closed). This is a
  different artifact — a math-reasoning system with specialist checkpoints, not
  a general Nemotron distribution event. Adjacent Anthropic math-proof work is
  at [[anthropic-fermat-lean-proof-2026-09]], and the contrast is the point:
  that one used Lean, this one deliberately did not.
expected: "Released with checkpoints, data, code, solutions and a 200-problem benchmark per the relay. Pending: the NVIDIA first-party post / model card / repo URL, the licence, and whether the 200-problem benchmark is adopted by anyone outside NVIDIA."
labels:
  - nvidia
  - open-weights
  - reasoning
  - math
  - benchmark
verification: partial
sources:
  - https://x.com/mark_k/status/2099110580455924060
  - "@NVIDIAAI"
created_at: 2026-09-14
updated_at: 2026-09-14
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-14
    change: "Created — RELEASED. NVIDIA's Nemotron 3 Ultra scored 30/42 at the 2026 International Mathematical Olympiad — gold-medal level — using natural-language proofs only, with no formal theorem prover, external tools or internet access; three checkpoints generate, verify and refine candidate proofs before a high-compute stage selects the final answer (@mark_k, 2026-09-13 12:18 UTC). NVIDIA released the two specialist checkpoints, the training data, training and inference code, the submitted solutions, and a new 200-problem olympiad-level benchmark. Recorded as released rather than as a capability claim precisely because the evidence is an enumerated artifact list rather than a score image. Verification partial with the gap named: no NVIDIA first-party post, model card, repo link, licence or weights URL was captured in-window, so the entire record rests on one relay with modest engagement (~84 likes) — a case where reach is anti-correlated with artifact quality. Distinct from the closed [[nvidia-nemotron-openrouter-2026-06]]: that tracked a Nemotron distribution event, this is a math-reasoning system with its own checkpoints and benchmark. Deliberate contrast with [[anthropic-fermat-lean-proof-2026-09]], which used a formal prover where this one did not."
---

The headline is the medal; the substance is the recipe.

An IMO gold-equivalent score on natural-language proofs — with no Lean, no
tools, no retrieval — is a strong result on its own, because it removes the
usual escape hatch of "the prover did the reasoning." But frontier labs have
posted olympiad results before and published nothing runnable. What is unusual
here is the enumerated release: two specialist checkpoints, the training data,
training *and* inference code, the actual submitted solutions, and a new
200-problem benchmark. Each of those is independently checkable, and together
they let a third party attempt to reproduce the score rather than take it.

That also sets the evidentiary bar for this ticket. The claim is not "NVIDIA
says it is good"; it is "NVIDIA says these files exist." One relay reported it
and no NVIDIA primary was captured, so verification stays `partial` — but this
is the easy kind of `partial` to resolve, and if the artifacts do not surface at
a URL, that absence is itself the finding.

Worth watching for a reason that outlives the medal: the 200-problem benchmark.
A lab publishing its own eval alongside its own record score is proposing a
standard it currently tops. Whether anyone outside NVIDIA adopts it is the real
test of whether this was a release or a press release.
