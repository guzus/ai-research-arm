---
slug: openai-math-results-release-2026-10
title: "OpenAI publishes hundreds of mathematical results produced by an unreleased internal frontier model"
company: "OpenAI"
model: null
status: confirmed
status_note: |
  **First-party, 2026-10-06 22:19 UTC (@OpenAI).** "We're releasing a broad
  range of new mathematical results produced by an internal frontier model. We've
  been consulting with the independent Advisory Group on Mathematics and
  Artificial Intelligence at the Institute for Advanced Study, and we have drawn
  on their advice and public recommendations to inform how we release these
  results." @sama: "We are entering a new era of discovery now."

  **Scale, per relays (not first-party in this fetch):** 722 manuscripts covering
  372 results, published on GitHub (@TheInfoMachine, @BuiltByEstrada); about three
  hours of ChatGPT Pro compute per result per The Verge (@MyselfAryanSing); one
  result is a matrix-multiplication exponent bound of roughly n^2.25, which would
  be well below the ~2.3712 AlphaEvolve-era figure (@TheInfoMachine — unrefereed).

  **What is not released:** the model. A relay thread (@KyleRonen5amw) says OpenAI
  is working to release it, with no date. None of the results is refereed yet.
expected: "Results published 2026-10-06. Open: the producing model's name and release date, referee/community verification of headline results (matrix-multiplication bound), and whether any result is the Millennium-problem progress claimed in September."
labels:
  - openai
  - mathematics
  - research-claim
  - unreleased-model
  - disclosure
verification: confirmed
sources:
  - https://x.com/OpenAI/status/2107596713791767021
  - https://x.com/sama/status/2107623610483720463
  - https://x.com/TheInfoMachine/status/2107828162352533704
  - https://x.com/BuiltByEstrada/status/2107826479329329455
  - https://x.com/MyselfAryanSing/status/2107826560619409654
  - https://x.com/KyleRonen5amw/status/2107825797507756506
  - "@OpenAI"
created_at: 2026-10-07
updated_at: 2026-10-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-07
    change: "Created — CONFIRMED / confirmed. @OpenAI announced on 2026-10-06 22:19 UTC that it is releasing a broad range of new mathematical results produced by an internal frontier model, with release practice informed by IAS's Advisory Group on Mathematics and AI. Relays: 722 manuscripts on 372 results on GitHub, ~3h of ChatGPT Pro compute per result (The Verge), including a matrix-multiplication bound near n^2.25. The model itself is unreleased and undated. Linked to the prior claim at [[openai-millennium-problems-2026-09]]."
---

This is the disclosure that [[openai-millennium-problems-2026-09]] said was
being withheld: an internal model's output, published in bulk, with an outside
advisory body consulted on how. Staff framing is maximal (@sama "a new era of
discovery"; @tszzl speculating on quantum gravity within a year).

The status is `confirmed` rather than `released` because the tracked artifact is
the model behind the results, and that is not available to anyone outside
OpenAI. The results themselves are public and unrefereed; the useful falsifiers
are independent checks of the headline claims, starting with the
matrix-multiplication bound.

Related: [[openai-unreleased-containment-escape-2026-07]] (also concerns an
unreleased internal model), [[google-gemini-deepthink-mathematica-2026-09]] and
[[anthropic-fermat-lean-proof-2026-09]] for competing math efforts.
