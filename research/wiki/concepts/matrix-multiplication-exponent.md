---
slug: matrix-multiplication-exponent
title: Matrix multiplication exponent (ω)
type: concept
aliases: ["matrix multiplication exponent", "omega", "AlphaEvolve matrix multiplication", "ω", "9/4 matrix multiplication"]
tags: [theoretical-cs, algorithms, ml-for-math, alphaevolve, complexity]
description: An OpenAI model-written manuscript claims ω = 9/4 with a matching lower bound over every field; partial Lean formalization, no referee.
created_at: 2026-08-19
timestamp: 2026-11-25T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-11-25", path: research/digest/2026-11-25-digest.md}
  - {title: "ARA daily digest 2026-08-19", path: research/digest/2026-08-19-digest.md}
  - {title: "Improving the matrix multiplication exponent with modern optimization and AlphaEvolve", url: "https://arxiv.org/abs/2608.16884", date: 2026-08-18}
---

The **matrix multiplication exponent** ω is the infimum exponent bounding the
asymptotic cost of multiplying two `n×n` matrices. The naive algorithm is
`O(n³)`; decades of work (Strassen and successors) have driven ω steadily
downward. On **2026-08-18** a **DeepMind-and-academia** team published
**"Improving the matrix multiplication exponent with modern optimization and
AlphaEvolve"** (arXiv 2608.16884; Dupont, Eisenberger, Mehrabian, Alman,
Vassilevska Williams, Balog et al.) that **reformulates the combination-loss
optimization** behind the current best bounds, solves it in a strictly larger
setting, and **refines the result with AlphaEvolve** to push **ω below
2.371177**, improving on the prior **2.371339** record.

## Why it matters

- **A genuine ML-assisted result in theoretical CS.** The improvement is small
  numerically — the interesting part is *mechanism*: modern optimization plus
  AlphaEvolve applied to the combination-loss optimization, the same
  ML-for-math trajectory [[google|Google DeepMind]] has pursued since AlphaTensor.
  It is a case where a compute/learning loop tightens a classical complexity
  bound rather than a purely hand-fashioned proof (ARA daily digest 2026-08-19).
- **Symbolic, not practical, speed.** ω improvements of this size do not change
  the constant factors that dominate real `n`; the result matters for the
  theory of algorithmic complexity, not for immediate runtime wins — worth
  holding against the hardware-efficiency thread (see [[model-specific-silicon]]).
- **Part of the verify-vs-produce tension.** Like the OpenAI ten-proofs
  manuscript, an ML-assisted bound invites scrutiny about verification — see
  [[verification-bottleneck]].

## OpenAI's 9/4 claim (2026-11-25)

- **A model-written manuscript in [[openai]]'s math repo claims ω = 9/4**,
  with a matching lower bound over every field and a **partial Lean
  formalization**. No referee has checked it. If the claim held it would
  smash the 2026-08-19 AlphaEvolve record (ω < 2.371177) all the way to
  **2.25** — a jump of a different kind from the 0.000162 improvement
  that paper recorded. Treat it as an **unchecked lab dump**, not a
  published bound. See [[verification-bottleneck]] and [[gpt-6]]
  (Hacker News; ARA daily digest 2026-11-25).
- **The same repo edition is a 730-manuscript dump** (375 families)
  from an unnamed internal model, labelled "raw research data, rather
  than polished academic papers," and also lists results on the
  Valiant hierarchy and Smale's ninth problem. That is the
  produce-faster-than-check pattern this concept already shares with
  [[astra]]'s ten-proofs manuscript.

## Open questions

- **Does the bound hold under independent review?** As with any automated/
  learned result, reproduction and formal checking matter before the number is
  fully accepted. The 9/4 manuscript is the sharper version of this question:
  a claimed closed-form exponent with only a partial Lean artifact.
- **How far can the optimization+AlphaEvolve loop push ω?** The paper extends
  the setting in which the combination-loss optimization is solved; whether the
  technique has further headroom is open. The OpenAI dump does not use that
  loop; it is a different production path.
