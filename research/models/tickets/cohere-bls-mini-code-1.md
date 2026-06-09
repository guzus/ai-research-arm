---
slug: cohere-bls-mini-code-1
title: Cohere BLS-Mini-Code-1.0 — 30B MoE coding model (pre-release weights)
company: Cohere
model: BLS-Mini-Code-1.0
status: in-testing
status_note: |
  **Nick Frosst** (Cohere co-founder) posted **pre-release weights** of
  **BLS-Mini-Code-1.0**, a **30B-parameter MoE coding model with ~3B active**,
  to **HuggingFace for community testing ahead of launch** (surfaced via
  r/LocalLLaMA). A real artifact from a primary (the co-founder) → in-testing /
  confirmed; full launch terms, benchmarks, and license still pending.
expected: "Public launch following the community-test period; date/benchmarks/license TBD"
labels:
  - cohere
  - coding-model
  - moe
  - open-weights
  - pre-release
verification: confirmed
sources:
  - "@nickfrosst"
  - "@huggingface"
created_at: 2026-06-09
updated_at: 2026-06-09
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-09
    change: "Created — Cohere co-founder Nick Frosst posted pre-release weights of BLS-Mini-Code-1.0 (30B MoE, ~3B active) to HuggingFace for community testing ahead of launch (relayed via r/LocalLLaMA). Real artifact from a primary → status in-testing, verification confirmed. Full launch, benchmarks, and license pending"
---

**Cohere** is testing the waters on a coding model: co-founder **Nick
Frosst** posted **pre-release weights** of **BLS-Mini-Code-1.0** — a **30B-
parameter mixture-of-experts model with roughly 3B active parameters** — to
**HuggingFace for community testing ahead of an official launch**, surfaced
this cycle through r/LocalLLaMA.

**Why `in-testing` / `confirmed`.** Unlike a leak or a rumor, this is a
**real downloadable artifact posted by a company principal** — the canonical
"private/community preview" shape that maps to `in-testing`, with
`verification: confirmed` because the source is primary (the co-founder
himself). What remains open: the **official launch date, full benchmarks,
pricing, and license terms**.

The pattern — releasing pre-launch weights for community shakeout — fits the
broader open-weights momentum dominating developer chatter this week (Gemma 4,
Qwen 3.6/3.7, MiMo-v2.5-Pro). It also keeps Cohere in the **smaller-but-fast
coding model** lane rather than the frontier-scale race.

**Transition triggers:**
- Official Cohere launch (GA weights / API) → `released`, refresh title if the
  marketing name changes.
- Published benchmarks / license → UPDATE.
- The pre-release is pulled or the launch is abandoned → `closed`.
- ≥15 cycles with no launch follow-through → `closed: stale-rumor-unverified`.

**Dedup note:** further BLS-Mini-Code signal UPDATES this ticket. Other Cohere
model releases get their own tickets.
