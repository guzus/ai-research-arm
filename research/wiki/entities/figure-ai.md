---
slug: figure-ai
title: Figure AI
type: entity
aliases: [Figure, "Figure AI", "Figure Robotics", "Figure 03", "Figure 4", "Helix", "Helix-02", "Helix 2.5", "@adcock_brett", "Brett Adcock"]
tags: [humanoid-robotics, vla, robotics, brett-adcock]
description: US humanoid-robotics company; Helix 2.5 Index pretraining lifted zero-shot household tidy/fold/make-bed success from 9% to 56% across 30 unseen homes, after the 200-hour Sunnyvale package-sort run.
created_at: 2026-06-01
timestamp: 2026-09-18T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-18", path: research/digest/2026-09-18-digest.md}
  - {title: "ARA daily digest 2026-07-19", path: research/digest/2026-07-19-digest.md}
  - {title: "ARA daily digest 2026-06-01", path: research/digest/2026-06-01-digest.md}
  - {title: "Humanoids Daily — Figure 200-hour Helix-02 marathon", date: 2026-05-30}
---

**Figure AI** is a US humanoid-robotics company led by founder/CEO
**Brett Adcock**. Its **Figure 03** humanoid runs **Helix-02**, Figure's
in-house **vision-language-action (VLA)** neural network. Figure is the
only major humanoid OEM with **zero frontier-lab inference dependency** —
its perception + control stack is end-to-end internally developed.

## Why it matters

The **2026-05-30 Sunnyvale 200-hour run** is the company's defining
2026 capability disclosure:

- **200 continuous hours** of fully autonomous package sorting at Figure HQ,
  the longest publicly-verified autonomous humanoid shift on record.
- **249,560 packages** processed; **zero hardware failures**, **zero
  teleoperation**. The fleet (anchored by the unit nicknamed "Rose")
  ran entirely on Helix-02 with autonomous task selection, autonomous
  fault recovery, and autonomous rotation to charging.
- **~10× the prior public envelope** on MTBI (mean-time-between-intervention).
  Optimus, Apollo, 1X Neo, Sanctuary, and [[unitree|Unitree]] had previously topped
  out near 10–20h at meaningful throughput. MTBI is the metric that
  actually governs warehouse / 3PL / manufacturing procurement.
- **Origin shape.** Started May 20 as an 8-hour livestream challenge;
  Figure declined to stop after the original challenge cleared,
  escalating past 60h, 100h, and finally 200h on May 30.

**Strategic frame.** Adcock framed the run as the MTBI proof-point
underwriting **BotQ-scale Figure 4 procurement** and the
"no frontier-lab dependency" supply-chain thesis — explicitly positioned
against a backdrop where the frontier labs are increasingly
competitor-ish to robotics primes (Anthropic Series H at $965B, OpenAI
S-1 filed). Figure controlling its own VLA stack matters more when
[[anthropic]] and [[openai]] are themselves shipping agent products
into adjacent markets.

The Helix-02 capability disclosure is the most consequential
"model-side" artifact of the 2026-05-30/31 window — capability proof
rather than weights release — and slots into the [[ai-capex]]
supercycle as a demand signal: humanoid autonomy at warehouse-grade
MTBI lifts the addressable case for production-scale on-prem inference
hardware.

Figure competes on the humanoid axis with Chinese entrant [[agibot]],
which showcased its A3 Ultra humanoid and three other embodied-AI
products at WAIC 2026 (2026-07-19) as part of a global export push.

## Helix 2.5 — Index pretraining and a household ablation (2026-09-18)

- **Figure claimed the first zero-shot whole-body
  humanoid eval at this scope:** tidying,
  towel-folding and bed-making in **30 unseen Bay
  Area homes** with no data collected there.
  Holding task data and architecture fixed,
  **Index pretraining alone** moved full-task
  success from **9% to 56%** — a 6× lift. Figure
  also published an **8× pretraining-data scaling
  sweep** on action-prediction loss and restated
  a **$3.5B Helix compute commitment**. **56% is
  still a vendor-graded research result**, not a
  product that can be left alone, and there is
  **no third-party rerun**. This is a Helix 2.5
  policy update, not a new robot SKU (Figure;
  ARA daily digest 2026-09-18).
- **Why it matters next to the Sunnyvale run.**
  The 200-hour package-sort marathon proved MTBI
  on one warehouse workflow. The household
  ablation is the first published test of
  whether the same VLA stack generalizes to
  unstructured homes with no on-site data —
  exactly the open question this page has
  carried since June. 56% is a research
  checkpoint, not a procurement envelope.
  See [[agibot]] and [[ai-capex]].

## Open questions

- **Generalization.** The 249,560-package run was a single workflow
  (package sort) in a single facility. The 2026-09-18 household
  ablation moves the question from warehouse MTBI to homes, but
  56% full-task success is still vendor-graded and not a product
  that can be left alone.
- **Figure 4 timing.** "BotQ-scale procurement" implies a 2026–27 ramp.
  When does Figure 4 ship at production volume, and to which customer?
- **No frontier-lab dependency — at what cost?** Helix-02 is Figure-internal,
  but the company is far smaller than [[anthropic]] / [[openai]] on training
  compute. Is supply-chain independence sustainable as VLA training-FLOPS
  requirements grow? The restated **$3.5B Helix compute commitment**
  is the first dollar figure attached to that question.
