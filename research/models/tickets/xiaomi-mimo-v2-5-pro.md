---
slug: xiaomi-mimo-v2-5-pro
title: Xiaomi MiMo-v2.5-Pro-UltraSpeed — ~1,000 tok/s on a 1T MoE
company: Xiaomi
model: MiMo-v2.5-Pro-UltraSpeed
status: confirmed
status_note: |
  Xiaomi's **MiMo-v2.5-Pro-UltraSpeed** claims **1,000+ tokens/sec on a
  1T-parameter MoE** using a **standard 8-GPU server** (no Cerebras/Groq custom
  silicon) — the day's **top community AI story** (419 pts on Hacker News).
  "Crazy if true": the **throughput headline is pending independent
  verification**, so verification is partial. The model itself sits in Xiaomi's
  established open-leaning MiMo line.
expected: "Independent throughput reproduction pending; weights/availability per Xiaomi's MiMo line"
labels:
  - open-weights
  - moe
  - efficiency
  - inference-throughput
  - china
verification: partial
sources:
  - "@Xiaomi"
  - "@ycombinator"
created_at: 2026-06-09
updated_at: 2026-06-09
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-09
    change: "Created — Xiaomi MiMo-v2.5-Pro-UltraSpeed claims 1,000+ tok/s on a 1T-parameter MoE using a standard 8-GPU server (no Cerebras/Groq), the day's top community AI story (419 pts on HN). Real model in the MiMo line + heavy community attention → status confirmed; the throughput headline is unverified independently → verification partial"
---

**Xiaomi's MiMo-v2.5-Pro-UltraSpeed** was the cycle's **top community AI
story** (419 points on Hacker News), on a striking efficiency claim:
**1,000+ tokens/second on a 1-trillion-parameter MoE**, reportedly using a
**standard 8-GPU server** rather than Cerebras/Groq-class custom inference
silicon. If it holds, it is a notable data point in the "frontier-class
throughput on commodity hardware" thread that dominated developer chatter
this week (alongside Luce Spark, NanoQuant, and Gemma 4 speedups).

**Why `confirmed` / `partial`.** The model sits in Xiaomi's established,
open-leaning **MiMo** family and drew sustained, high-signal community
attention — enough to clear `confirmed` for the release/announcement. But the
**1,000 tok/s headline is a vendor/community claim not yet independently
reproduced** ("crazy if true"), so `verification` stays `partial` until a
third-party benchmark lands.

**Transition triggers:**
- Independent third-party throughput reproduction → UPDATE, advance verification to confirmed.
- Public weights / API confirmed downloadable and usable → `released`.
- The throughput claim is debunked → `closed` (note the contradiction; spawn a successor only if a corrected artifact exists).
- ≥15 cycles with no corroboration and no usable artifact → `closed: stale-rumor-unverified`.

**Dedup note:** further MiMo-v2.5-Pro / UltraSpeed throughput signal UPDATES
this ticket. Other open-weights efficiency releases get their own tickets.
