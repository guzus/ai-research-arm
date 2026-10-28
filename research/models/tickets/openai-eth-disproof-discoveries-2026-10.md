---
slug: openai-eth-disproof-discoveries-2026-10
title: "OpenAI announces three model-produced discoveries: local smoothing in all dimensions, an Exponential Time Hypothesis disproof, and a QFT result"
company: "OpenAI"
model: null
status: confirmed
status_note: |
  **First-party claim, 2026-10-26 (~21:37 UTC).** @OpenAI and @sama retweeted OpenAI
  researcher @danintheory: "We are announcing three new discoveries in mathematics, computer
  science, and physics about harmonic analysis, complexity theory, and quantum field theory."

  **Content, per relays (not first-party in this fetch).** (1) An internal model proved the
  local smoothing conjecture in all dimensions; it was previously known only in low
  dimensions. Relays tie this to the Kakeya and Stein restriction conjectures. (2) The model
  disproved the Exponential Time Hypothesis (ETH), with a Lean formalization published on
  GitHub. One relay says the model found it on 2026-10-16 and formalized it on 2026-10-17.
  (3) The physics result is on hold while outside experts write their own analysis
  (@piman7555, @Macfeecn, @Aleeexanderrrrr).

  **Confirmed: that OpenAI makes the claim. Not confirmed: the mathematics.** Expert
  review of the ETH disproof is still running. A disproof of ETH would overturn a
  hypothesis that a large body of complexity-theory results assumes.

  **2026-10-28 — outside review starts.** @OpenAI retweeted a @KITP_UCSB statement from a
  'Yang-Mills Working Group' formed to interpret the physics result (existence of QCD,
  including a quantum Yang-Mills existence subproblem). A relay names Impagliazzo, Paturi and
  Williams as the group verifying the 67-page ETH preprint. No verdicts yet.
expected: "Announced 2026-10-26. Watch: the Impagliazzo/Paturi/Williams verdict on the ETH disproof, expert response to the local-smoothing proof, and what the KITP Yang-Mills Working Group statement concludes about the QCD / Yang-Mills existence result."
labels:
  - research
  - mathematics
  - complexity-theory
  - ai-for-science
  - internal-model
verification: partial
sources:
  - "https://x.com/OpenAI/status/2114833781815456118"
  - "https://x.com/sama/status/2114864981934329996"
  - "https://x.com/piman7555/status/2115052172765548630"
  - "https://x.com/Macfeecn/status/2115034555904372848"
  - "https://x.com/Aleeexanderrrrr/status/2115015347401355314"
  - "https://x.com/OpenAI/status/2115237121300770818"
  - "https://x.com/KITP_UCSB/status/2115236165330846045"
  - "https://x.com/ayushsainime/status/2115413826745307481"
created_at: 2026-10-27
updated_at: 2026-10-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-27
    change: "Created — CONFIRMED / partial. @OpenAI and @sama (2026-10-26) retweeted @danintheory announcing three discoveries, in harmonic analysis, complexity theory and quantum field theory. Relays say an internal model proved the local smoothing conjecture in all dimensions and disproved the Exponential Time Hypothesis, with a Lean proof on GitHub (reportedly found 10-16 and formalized 10-17). The physics result waits on outside experts' analysis. The claim is first-party; the mathematics has not been independently verified."
  - ts: 2026-10-28
    change: "Confirmed / partial, unchanged — the physics result gets an outside working group, and the ETH reviewers are named. @OpenAI (2026-10-28 00:20 UTC) retweeted @KITP_UCSB (00:16 UTC): a 'Statement of Yang-Mills Working Group, a scientific collaboration to interpret AI result related to the existence of quantum chromodynamics & completions of the Standard Model, including a subproblem proving the existence of the Quantum Yang-Mills theory.' This is the outside analysis the 10-27 entry said the physics result was waiting on; the statement text is in images not read here, so its verdict is not recorded. A relay (@ayushsainime, 2026-10-28 12:02 UTC) adds that the ETH preprint is 67 pages, that a group led by Russell Impagliazzo, Ramamohan Paturi (UC San Diego) and Ryan Williams (MIT) will verify it, and that OpenAI calls practical speedups far off. A second relay says Anthropic separately reported an internal Claude model reached its own subexponential 3-SAT algorithm the same day (single relay; not adopted). Verification stays partial: no expert verdict yet on any of the three results."
---
This is a follow-on to the bulk release tracked at [[openai-math-results-release-2026-10]]. It is
smaller and more pointed: three named results instead of hundreds, and one of them is the
falsification of a standard complexity-theory assumption. Neither result here is a Millennium
Prize problem, so [[openai-millennium-problems-2026-09]] stays open and unresolved.

The verification bar is outside review, not the announcement. A Lean formalization is strong
evidence when the formal statement matches the informal claim. Whether it does is what reviewers
will check. Verification stays `partial` until named experts respond.
