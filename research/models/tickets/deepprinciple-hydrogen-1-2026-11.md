---
slug: deepprinciple-hydrogen-1-2026-11
title: "Deep Principle releases Hydrogen-1.0, an open-weight science model post-trained from GLM-5.3"
company: Deep Principle
model: Hydrogen-1.0
status: released
status_note: |
  **Announced by the team, 2026-11-02 13:35 UTC.** @chenru_duan (Deep Principle, tagging @DeepPrinciple):
  "We're introducing Hydrogen-1.0, our first open-weight model for scientific research. We post-trained GLM-5.3
  (@Zai_org) on our internal scientific data, lab records, and discovery trajectories." Self-reported scores:
  38.3% on FrontierScience-Research (GPT-6 Astra: 33.3%) and 93.0% on GPQA-Diamond. Mind Lab says it helped
  with training and infrastructure (@XiaotengMa1996).

  No independent benchmark or parameter count was captured. The weights link and license were not in the
  fetched text.
expected: "Released 2026-11-02 as open weights. Open: license, parameter count, and independent evaluation."
labels:
  - open-weights
  - science
  - glm-derivative
  - released
verification: confirmed
sources:
  - "https://x.com/chenru_duan/status/2117249292469665838"
  - "https://x.com/XiaotengMa1996/status/2117289555695149065"
  - "https://x.com/shipfrontierai/status/2117605865507447070"
  - "https://x.com/forangeai/status/2117616485158076443"
created_at: 2026-11-02
updated_at: 2026-11-03
closed_at: null
closed_reason: null
history:
  - ts: 2026-11-02
    change: "Created — RELEASED / confirmed. @chenru_duan (2026-11-02 13:35 UTC, ~1K likes) introduced Hydrogen-1.0, Deep Principle's first open-weight model for scientific research, post-trained from Zhipu's GLM-5.3 on internal scientific data, lab records and discovery trajectories. Self-reported: 38.3% on FrontierScience-Research vs 33.3% for GPT-6 Astra, and 93.0% on GPQA-Diamond. Mind Lab (@XiaotengMa1996) says it contributed training and infrastructure. No independent scores yet."
  - ts: 2026-11-03
    change: "Released, unchanged — model-card details from secondary accounts. @shipfrontierai (2026-11-03 13:12 UTC) describes a science model's model card: MIT-licensed weights on a GLM-5.3 base, 1M-token context and 128K output, with NVFP4 quants for NVIDIA Blackwell (tested on 8x B300) and MXFP4 quants for AMD Instinct MI350X. The post does not name Hydrogen in its text, but the GLM-5.3 base and science focus match this ticket. @forangeai (13:54 UTC) says the announcement passed 1M views. Licence and context length are still not first-party in this run's signal; parameter count and independent evaluation remain open."
---

Hydrogen-1.0 is a domain model, not a new base model. Deep Principle took Zhipu's open-weight GLM-5.3
([[zhipu-glm-5-3-2026-08]]) and post-trained it on its own scientific data. The claim that matters is the
FrontierScience-Research score, where the team reports it beats GPT-6 Astra. That number is self-reported.

It is one more sign that GLM-5.3 has become a common base for derivative open models, alongside the
cyber evaluations tracked on [[zhipu-glm-5-3-cyber-evaluations-2026-10]].

**Transition triggers:** independent benchmark results or license details → history update; a Hydrogen-2
or successor → new ticket.
