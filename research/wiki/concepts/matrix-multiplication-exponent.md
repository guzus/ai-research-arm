---
slug: matrix-multiplication-exponent
title: Matrix multiplication exponent (ω)
type: concept
aliases: ["matrix multiplication exponent", "omega", "AlphaEvolve matrix multiplication", "ω"]
tags: [theoretical-cs, algorithms, ml-for-math, alphaevolve, complexity]
description: The exponent ω bounding the complexity of matrix multiplication; on 2026-08-19 a DeepMind-and-academia team combined a reformulated optimization with AlphaEvolve to push ω below 2.371177, improving the 2.371339 record and marking a genuine ML-assisted result in theoretical CS.
created_at: 2026-08-19
timestamp: 2026-08-19T00:00:00Z
sources:
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

## Open questions

- **Does the bound hold under independent review?** As with any automated/
  learned result, reproduction and formal checking matter before the number is
  fully accepted.
- **How far can the optimization+AlphaEvolve loop push ω?** The paper extends
  the setting in which the combination-loss optimization is solved; whether the
  technique has further headroom is open.
