---
slug: claude-science
title: Claude Science
type: entity
aliases: ["Claude Science", "Anthropic biology lab", "ART enzyme family"]
tags: [anthropic, claude, ai-for-science, agentic-research, product]
description: Anthropic's agentic research workbench; its biology lab's first wet-lab result recovered the ART enzyme family from 1.94B protein clusters via ~950 Claude agents.
created_at: 2026-07-01
timestamp: 2026-09-24T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-24", path: research/digest/2026-09-24-digest.md}
  - {title: "ARA daily digest 2026-07-05", path: research/digest/2026-07-05-digest.md}
  - {title: "ARA daily digest 2026-07-04", path: research/digest/2026-07-04-digest.md}
  - {title: "ARA daily digest 2026-07-01", path: research/digest/2026-07-01-digest.md}
  - {title: "@claudeai launch post", date: 2026-06-30}
---

Claude Science is [[anthropic]]'s agentic research environment, launched
**17:02 UTC June 30, 2026** — an hour before [[claude-sonnet-5|Claude Sonnet 5]].
It is an agentic workbench with **artifacts traced back to their generating
code**, **on-demand managed compute**, and **60+ optional scientific tools**
(genomics, computational chemistry), plus a **citation/calculation verification
agent** and **local/HPC execution** so sensitive data can stay in-lab. Debut
partners: **Novartis, Bristol Myers Squibb, and Genentech**. MIT Technology
Review calls it Anthropic's "newest flagship product" (ARA digest 2026-07-01).

## Why it matters
- **The AI-for-science race becomes an open contest.** Claude Science shipped
  the **same day OpenAI released its GeneBench-Pro research-judgment benchmark**,
  turning AI-for-science from a hiring story into a product/benchmark contest.
  It operationalizes Anthropic's science bet — the same bet signalled by the
  [[john-jumper]] (AlphaFold) hire from DeepMind and measured against
  [[lifescibench|LifeSciBench]], where the best model still clears only 36.1%.
- **In-lab execution as the enterprise wedge.** Local/HPC execution and
  verification agents target the exact objection regulated pharma has to cloud
  agents — that sensitive data must not leave the lab — making the debut
  partners (Novartis, BMS, Genentech) a credibility signal for the product's
  data-residency design.
- **A distribution move amid the export freeze.** It lands while
  [[anthropic]]'s frontier [[claude-fable-5|Fable / Mythos]] line sits under
  export controls (see [[federal-ai-policy]]) — Anthropic shipping product
  surface and science partnerships rather than a frontier model.

- **Secondary press coverage continues; life-sciences hire named
  (2026-07-04).** Business-press outlet fourweekmba.com framed the launch as
  "rewriting the model company playbook," continuing the pattern of
  secondary coverage without new primary detail on target diseases or
  partners. The digest also names a new life-sciences hire, **Jonah Cool**,
  alongside AlphaFold co-creator **[[john-jumper]]** as the personnel signal
  behind Anthropic's science push (ARA digest 2026-07-04).
- **Trade-press coverage keeps broadening, still no primary specifics
  (2026-07-05).** FT, Pharmaceutical Technology, MIT Technology Review, STAT
  News, and GEN all covered the launch this week, and The Decoder separately
  reports Anthropic is funding development for diseases "Big Pharma
  considers unprofitable." Anthropic still has not published an official
  blog post naming specific diseases, partners beyond the debut three, or a
  timeline — the coverage volume is growing faster than the primary-source
  detail behind it (ARA digest 2026-07-05).

## First wet-lab result — the ART enzyme family (2026-09-24)

- **The workbench produced a confirmed wet-lab
  finding.** [[anthropic]]'s biology lab ran
  roughly **950 Claude agents** across
  **1.94B protein clusters** for about
  **21.5 hours** (~215.6M tokens). The swarm
  recovered **198,290 reverse-transcriptase
  clusters** and surfaced one sitting next
  to a tandem repeat array. Bench work
  confirmed the system produces short RNAs.
  Anthropic named the family **ART** and
  released a preprint; **function is still
  unknown**. The lab likens the array
  structurally — not functionally — to
  CRISPR. Feng Zhang (MIT/Broad) called the
  finding "genuinely intriguing and merits
  further investigation." Critics noted
  Anthropic's own text says scientists
  review every hypothesis and run all lab
  work — so this is agent-assisted
  discovery, not autonomous wet-lab
  science. HN **389 / 406**. Read against
  the August protein-binder designs and
  [[evo-genome-models|Evo]]'s working
  phages: ART is the first named enzyme
  family from this workbench that left
  the computer and entered a bench
  protocol (Anthropic, The Verge,
  TechCrunch, HN; ARA daily digest
  2026-09-24).

## Open questions
- **Does the workbench beat a benchmark?** GeneBench-Pro and
  [[lifescibench|LifeSciBench]] measure research judgment;
  ART is a wet-lab confirmation of a search hit, not a
  scored suite result, and function remains unknown.
- **How much runs on which model?** The launch paired with
  [[claude-sonnet-5|Sonnet 5]]; the ART search's model tier
  is not named in-window. [[claude-opus-5-5|Opus 5.5]]
  shipped the day before the digest cycle.
- **What does ART do?** The preprint flags a CRISPR-like
  repeat beside an unusual phage reverse transcriptase;
  no function is claimed. Until one is shown, the
  scientific payload is "agents can surface a
  structurally unusual cluster that survives bench
  confirmation," not a new enzyme mechanism.
