---
slug: zhipu-glm-5-3
title: Zhipu GLM-5.3
type: entity
aliases: ["Zhipu GLM 5.3", "GLM 5.3", "GLM-5.3", "Z.ai GLM-5.3"]
tags: [open-weights, china, agentic, frontier-model]
description: Zhipu AI / Z.ai's successor to GLM-5.2, at 60 on the Artificial Analysis Intelligence Index (tied with Kimi K3) with the top agentic Elo gain of the cycle — 1524 → 1770 on GDPval-AA v2, second only to Claude Opus 5; the first independent scoring landed 2026-08-19, with MIT-licensed weights promised within a week.
created_at: 2026-08-19
timestamp: 2026-08-19T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-19", path: research/digest/2026-08-19-digest.md}
---

Zhipu AI / Z.ai's **GLM-5.3** is the follow-on to [[zhipu-glm-5-2]] — the same
**753B-total / 40B-active** MoE architecture with **1M-token context** as its
predecessor, but carrying the cycle's headline **agentic** gain. Its scoring is
distinct from the model itself: **Artificial Analysis published the first
independent evaluation on 2026-08-19**, and it is the day's marquee Chinese
open-weight agentic development.

## Why it matters

- **Second worldwide on agentic work (2026-08-19).** Artificial Analysis scores
  GLM-5.3 at **60 on its Intelligence Index v4.1** — **tied with
  [[moonshot-kimi-k3|Kimi K3]]** — with the load-bearing gain in agentic Elo:
  **GDPval-AA v2 jumped 1524 → 1770**, **second overall behind
  [[claude-opus-5|Claude Opus 5]] (1855)** and **more than 100 points above
  Kimi K3 (1668)**. Real-world knowledge on **AA-Omniscience moved 4 → 14**.
  Pricing is **$1.40/$4.40 per Mtok** (see [[open-weights]] for the
  open-weight price-pressure context).
- **Caveats to hold.** Z.ai claimed **~22% *fewer*** output tokens than
  GLM-5.2, but the independent harness measured **~18,700 tokens per task —
  about 20% *more***. The **hallucination rate also regressed 26% → 30%**.
  And the **MIT-licensed weights remain a promise, not a download** — "within
  a week" is still unfulfilled, the same verification gap that marked the
  GLM-5.2 arc (ARA daily digest 2026-08-19).

## Open questions

- **Do the MIT weights actually land, and when?** As with GLM-5.2, the decisive
  open-weights transition is a primary model card plus a download; until then
  the class-leading agentic claim is backed only by a vendor-framed eval.
- **Does the agentic Elo transfer outside the harness?** The +246 Elo swing is
  on one benchmark; whether it holds on contamination-aware agentic and coding
  tasks is unverified.
- **Where does it sit in Z.ai's product ladder?** A distinct model from
  [[zhipu-glm-5-2]] — does it replace it as the flagship, or coexist as the
  agentic tier?
