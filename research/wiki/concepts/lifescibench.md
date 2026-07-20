---
slug: lifescibench
title: LifeSciBench
type: concept
aliases: ["LifeSciBench", "Life Sci Bench", "Life-Sci-Bench", "LifeSci Bench"]
tags: [benchmark, life-sciences, evaluation, agentic, openai, frontier-ai]
description: OpenAI's 750-task, expert-authored life-science research benchmark (released 2026-06-17) on which the best model clears only 36.1% — a concrete measure of the gap between frontier models and autonomous scientific research.
created_at: 2026-06-19
timestamp: 2026-06-19T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-06-19", path: research/digest/2026-06-19-digest.md}
  - {title: "OpenAI — Introducing LifeSciBench", url: "https://openai.com/index/introducing-life-sci-bench", date: 2026-06-17}
  - {title: "MarkTechPost — OpenAI releases LifeSciBench", url: "https://www.marktechpost.com/2026/06/17/openai-releases-lifescibench-a-750-task-benchmark-grading-ai-models-on-real-life-science-research-with-expert-written-rubric/", date: 2026-06-17}
---

**LifeSciBench** is a life-science research benchmark released by [[openai]] on
**2026-06-17**: **750 expert-authored tasks** written by **173 PhD scientists**,
in free-response form and **rubric-graded** across **7 workflows / 7 domains**.
The headline result is the point of the benchmark: the best model — OpenAI's own
life-sciences model **GPT-Rosalind** — clears only **36.1%**, meaning roughly two
in three research-level tasks still defeat frontier systems.

## Why it matters

- **A concrete capability-gap measurement.** Amid a cycle of vendor capability
  claims (the GPT-Rosalind biodefense/drug-discovery arc, "AI rivals doctors"
  Nature studies, an autonomous AI chemist), LifeSciBench is a rigor counterweight:
  a single, expert-rubric number that says autonomous scientific research is still
  far out of reach. It is the empirical sibling of the [[agent-lifespan-engineering]]
  /AgingBench style of "measure what models actually can't do yet" work.
- **It anchors [[openai]]'s life-sciences narrative in an eval.** OpenAI has been
  productizing GPT-Rosalind for drug discovery, design, and experimental
  workflows; publishing a benchmark its own model scores 36.1% on is an unusually
  candid framing of the remaining distance, and a likely yardstick competitors and
  policymakers will reach for when assessing "AI for science" claims.
- **Free-response + rubric grading raises the bar.** Unlike multiple-choice
  knowledge tests, free-response research tasks graded against expert-written
  rubrics test workflow-level competence (design, analysis, interpretation), which
  is closer to what autonomous research would require — and harder to game.

## Open questions

- **Does 36.1% move fast?** With GPT-5.6 imminent and a compressed model cadence,
  is LifeSciBench a durable hard benchmark or one that saturates within a few
  release cycles?
- **Neutral adoption.** Will third parties run LifeSciBench on non-OpenAI frontier
  models, or does an OpenAI-authored life-science benchmark scored highest by
  OpenAI's own model stay vendor-anchored?
- **Policy use.** Could a "fraction of research tasks autonomously solvable"
  number feed into the biosecurity / pre-release-review framing in
  [[federal-ai-policy]]?

## Changelog

- [2026-06-19] created | OpenAI 750-task life-science benchmark, best model 36.1%), updated 7 (openai — Shazeer + Dean Ball hires, GPT-5.6 ≈June 25 stealth test, LifeSciBench, GPT-5.5 Instant health upgrade + AI chemist
