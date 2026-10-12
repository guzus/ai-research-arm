---
slug: google-deepmind-alphaproof-nexus-2026-10
title: "Google DeepMind AlphaProof Nexus — Science paper: resolves 9 open Erdős problems via LLM + Lean"
company: "Google / DeepMind"
model: "AlphaProof Nexus"
status: confirmed
status_note: |
  **Per @daogangtang's 2026-10-12 digest:** DeepMind's **AlphaProof Nexus**,
  peer-reviewed in *Science* (published 2026-10-08), autonomously resolved
  **9 of 353** formalised open Erdős problems, two of which had been open for 56
  years. It also proved **44 of 492** OEIS conjectures by iterating LLM proof
  generation against Lean verification, at a few hundred dollars per problem in
  the reported runs.

  **Status `confirmed`:** a peer-reviewed publication is an official artifact. No
  public system or API release is reported. **Verification `partial`:** captured
  only through one digest relay. No DeepMind post or paper URL in this fetch.
expected: "Published 2026-10-08 (Science). Watch for a DeepMind post, released proofs/Lean artifacts, and independent verification of the Erdős results."
labels:
  - google
  - deepmind
  - math
  - formal-verification
  - research
verification: partial
sources:
  - "https://x.com/daogangtang/status/2109668616409174301"
created_at: 2026-10-12
updated_at: 2026-10-12
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-12
    change: "Created — CONFIRMED / partial. Per @daogangtang's digest (2026-10-12), DeepMind's AlphaProof Nexus, published in Science on 2026-10-08, autonomously resolved 9 of 353 formalised open Erdős problems (two open 56 years) and proved 44 of 492 OEIS conjectures by looping LLM proof generation against Lean, at a few hundred dollars per problem. Peer-reviewed paper; no system release. Single relay."
---

Machine-checked results on open problems are a different evidence class from
olympiad scores. Lean verification removes the grading question, so the open
issue is novelty: whether the resolved problems were genuinely open and not
already resolved in obscure literature.

Same-quarter context: OpenAI's own math-results release
([[openai-math-results-release-2026-10]]).
