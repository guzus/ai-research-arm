---
slug: huawei-tau-scaling-law-2026-05
title: Huawei unveils Tau (τ) Scaling Law + LogicFolding chip architecture
company: Huawei
model: null
status: confirmed
status_note: |
  Huawei chip lead He Tingbo presented the Tau (τ) Scaling Law and the
  LogicFolding 3D architecture at IEEE ISCAS Shanghai (~2026-05-25),
  framing a path to transistor density equivalent to a 1.4 nm process by
  2031 without EUV — via time-based optimization across devices, circuits,
  chips and systems rather than geometric shrink. A Bernstein research
  note circulated 2026-05-26 (~06:39 UTC, via @jukan05) framing it as
  "another DeepSeek moment" for compute, with a "2x–10x speedup possible
  with software optimizations" callout. Huawei's own corporate account
  re-amplified the announcement at 07:26 / 07:27 UTC the same day.
  Reporting also links DeepSeek's V4 family to Huawei Ascend co-engineering
  (third-party-reported, not DeepSeek-confirmed); a "LogicFolding" Kirin
  chip is said to ship this fall.
expected: "Kirin chips with LogicFolding stated for fall 2026; 1.4 nm-equivalent density target 2031"
labels:
  - chip-architecture
  - china
  - huawei-ascend
  - compute-sovereignty
verification: confirmed
sources:
  - "@Huawei"
  - "@jukan05"
  - "@AndrewCurran_"
  - "@kimmonismus"
  - "@DavidLe76335983"
created_at: 2026-05-26
updated_at: 2026-05-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-26
    change: "Created — Huawei presented Tau (τ) Scaling Law / LogicFolding at IEEE ISCAS Shanghai (~May 25, He Tingbo); Bernstein research note circulated May 26 ~06:39 UTC framing it as \"another DeepSeek moment\" with a 2x–10x software-speedup callout; @Huawei official account re-amplified at 07:26 / 07:27 UTC. Roadmap target: transistor density equivalent to 1.4 nm process by 2031 without EUV, via time-based optimization; LogicFolding Kirin chips stated to ship this fall. Reporting links DeepSeek V4 family to Huawei Ascend co-engineering (third-party only, not DeepSeek-confirmed)"
---

Huawei used its IEEE ISCAS Shanghai slot (~2026-05-25) to unveil the
**Tau (τ) Scaling Law** and the **LogicFolding** 3D chip architecture,
its formal pitch for *time-based* rather than *geometric* scaling — a
direct response to being cut off from EUV lithography by US export
controls. The headline roadmap claim is **transistor density equivalent
to a 1.4 nm process by 2031** without EUV, paired with the LogicFolding
3D architecture as the first commercial implementation (a "LogicFolding"
Kirin chip — Mate 90 series per relays — is stated to ship this fall).

The story shifted from "China research talk" to "Wall Street thesis"
within ~24 hours: a Bernstein Research note (relayed via @jukan05 at
06:39 UTC May 26 as a screenshot, captioned "Another DeepSeek moment")
flagged a **"2x–10x speedup possible with software optimizations"**
bullet. Huawei's own corporate account re-amplified the announcement
twice in the same window (07:26 and 07:27 UTC May 26), confirming the
institutional framing.

The DeepSeek tie-in is what gives this a place on the model-timeline
roadmap rather than just the semis beat: DeepSeek's V4 family is
**reported to be co-engineered for Huawei Ascend (950 / 950PR)** —
meaning the [deepseek-v4-pro-price-cut-2026-05](./deepseek-v4-pro-price-cut-2026-05.md)
cost reduction may be partly a hardware-co-design dividend rather than
pure software pricing. That linkage rests on third-party reporting
(@skyguan122465, 2026-05-19) rather than a DeepSeek primary statement
and is flagged as such.

**What is unverified:** the 1.4 nm-equivalent figure is a 2031 roadmap
target, not delivered silicon; the 2x–10x speedup bullet has no model,
workload, or method in the visible Bernstein snippet; Huawei has missed
prior node-by-X-year targets; and no externally measured Huawei Ascend
vs Nvidia H20/H200 inference benchmark on a published model has surfaced
in this window. Anchor to "Bernstein and Huawei together elevate the
architecture-not-lithography frame," not to a verified speedup number.

**Transition triggers:**
- A named Western semis analyst (SemiAnalysis, Morgan Stanley, Goldman,
  Citi) engages on the Bernstein call → UPDATE.
- DeepSeek primary statement confirming Ascend V4 co-engineering → UPDATE
  (and reflect on the price-cut ticket).
- First Kirin chip with LogicFolding ships with a confirmed launch date →
  `status: released`; ≥4 weeks after → `closed: released-and-aged`.
- If the 1.4 nm-by-2031 target is publicly retracted or contradicted →
  refresh status_note; consider closure on contradiction.

**Dedup note:** further Tau / LogicFolding / Kirin-LogicFolding signal
UPDATES this ticket. A distinct Huawei Ascend GPU release (e.g.
Ascend 960) gets its own ticket. DeepSeek-Ascend confirmation goes to
both this ticket *and* [deepseek-v4-pro-price-cut-2026-05](./deepseek-v4-pro-price-cut-2026-05.md).
