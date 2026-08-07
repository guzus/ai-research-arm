---
slug: evo-genome-models
title: Evo (genome language models)
type: entity
aliases: [Evo, "Evo 1", "Evo 2", "Evo genome language model", "Evo genome language models"]
tags: [genomics, biology, foundation-model, arc-institute, stanford, biosecurity, phage]
description: Arc Institute and Stanford's genome language models; in Science on 2026-08-07 they were reported to have written the first complete bacteriophage genomes from scratch, 16 of which produced working viruses.
created_at: 2026-08-07
timestamp: 2026-08-07T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-07", path: research/digest/2026-08-07-digest.md}
---

**Evo 1** and **Evo 2** are genome language models from the **Arc Institute** and
**Stanford**, developed by a group led by **Brian Hie**. On **2026-08-07** the
team published in **Science** what the digest records as the first complete
**bacteriophage genomes written from scratch by a model** — **16 of the designed
phages were working viruses**.

## Why it matters

- **The output is a functioning organism, not a document.** Most generative-AI
  results in the life sciences stop at a proposed structure or candidate
  molecule that still needs wet-lab validation — the gap [[lifescibench]] was
  built to measure and that [[chai-discovery]]'s molecules run through. Here the
  design was synthesized and the viruses replicated. That collapses the usual
  distance between model output and physical verification, and it is why this
  is the day's most consequential science item rather than another benchmark
  move (Science via NYT/BBC, Ars Technica; ARA daily digest 2026-08-07).
- **The modeling claim is joint reasoning across DNA, RNA and protein.**
  **Evo 1 was trained on 2.7 million prokaryotic genomes** and pushed to reason
  across all three layers at once rather than editing one component at a time —
  the design difference the team credits for producing coherent whole genomes
  instead of viable fragments.
- **There is a real therapeutic target.** Some of the 16 phages **kill hard
  *E. coli* strains**, which points at **phage therapy for antibiotic-resistant
  infection** — a use case where the ability to design many candidate phages
  quickly is the whole bottleneck.
- **It ships with a governance mechanism, and no governance response.**
  **Viruses capable of infecting complex organisms were excluded from the
  training data**, and the work ran in a secure lab. That training-data
  exclusion protocol is a concrete, copyable biosecurity control — arguably the
  most transferable part of the paper — but **no biosecurity body had responded
  to it at ingest**. Compare [[agentic-ai-security]], where the analogous
  capability-misuse debate only became a category after incidents forced it.
- **It is a different shape of AI-for-science than the frontier labs are
  selling.** [[anthropic]]'s [[claude-science]] and the automation thesis behind
  [[discovery-loop]] both aim a general agent at the research *process*. Evo is
  a domain-specific model whose training distribution *is* the science. The
  [[verification-bottleneck]] cuts differently here too: a phage either
  replicates or it does not, so verification is empirical rather than a matter
  of finding a qualified human reader.

## Open questions

- **How much of the 16 is selection?** The digest records 16 working phages but
  not how many designs were synthesized to get them. The hit rate is the
  capability number, and it is not in the curated input.
- **Does the exclusion protocol generalize?** Withholding complex-organism
  viruses works because the target class is nameable. It is unclear what the
  equivalent is for a model trained on broader biology.
- **Who regulates this?** [[federal-ai-policy]]'s frontier-review framework is
  built around closed *chat* products and compute thresholds; a genome model
  published in Science by a non-profit institute sits outside every instrument
  currently in force.
