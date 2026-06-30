---
slug: meituan-longcat-2-2026-06
title: Meituan open-sources LongCat-2.0 — 1.6T agentic-coding model ("Owl Alpha")
company: Meituan
model: LongCat-2.0
status: released
status_note: |
  Released and open-weighted **2026-06-30** (GitHub + Hugging Face; VentureBeat
  + multiple relays): **LongCat-2.0**, a **1.6T-parameter MoE (~48B active),
  ~1M-token context**, pretrained on **35T tokens** across a **~50,000-chip
  all-domestic cluster** that Meituan says used **no NVIDIA silicon**. Meituan
  also revealed it was the anonymous **"Owl Alpha"** model that had topped
  OpenRouter's coding usage for ~two months before the reveal. One relay
  (@eddiboi) cites **SWE-bench Pro 59.5** "beats GPT-5.5"; Meituan's card claims
  parity with the Gemini 3.1 Pro / GPT / Opus tier. The **release and OpenRouter
  standing are independently visible** → status `released`; the **capability-
  parity and "no-NVIDIA" claims are vendor-supplied** and not third-party
  confirmed → verification `partial`.
expected: "Pending: first independent SWE-bench Pro / LMArena run on the open weights; scrutiny of the 'trained entirely on Chinese chips' claim and the cluster's actual silicon composition"
labels:
  - frontier-model
  - open-weights
  - coding
  - china
  - released
verification: partial
sources:
  - "@VentureBeat"
  - "@vince_chow1"
  - "@__vandos__"
  - "@eddiboi"
  - https://x.com/VentureBeat/status/2071831014872092715
  - https://x.com/__vandos__/status/2071842186627317844
created_at: 2026-06-30
updated_at: 2026-06-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-30
    change: "Created — Meituan open-sourced LongCat-2.0 (2026-06-30, GitHub + Hugging Face; VentureBeat + multi-relay): 1.6T-param MoE (~48B active), ~1M context, 35T-token pretraining on a ~50,000-chip all-domestic (claimed no-NVIDIA) cluster, and revealed it as the anonymous 'Owl Alpha' that topped OpenRouter coding usage for ~2 months. Relays cite SWE-bench Pro 59.5 / 'beats GPT-5.5' and card-claimed Gemini 3.1 Pro / GPT / Opus-tier parity. Status released (open weights live + observable OpenRouter standing); verification partial (capability-parity and all-domestic-silicon claims are vendor-supplied, not third-party confirmed). Frontier-scale evidence for the moat-leak thesis alongside [[zhipu-glm-5-2]] and DeepSeek V4 ([[deepseek-v4-ga-surge-pricing-2026-06]])."
---

On **2026-06-30**, Chinese food-delivery giant **Meituan** released and
**open-weighted LongCat-2.0** — a **1.6-trillion-parameter MoE** (~48B
active), **~1M-token context**, pretrained on **35T tokens** across a
**~50,000-chip cluster** Meituan says is **entirely domestic, with no NVIDIA
silicon**. Posted to GitHub and Hugging Face and corroborated across relays
(VentureBeat as the strongest secondary).

The reveal's key twist: LongCat-2.0 is the model that had been running
anonymously on OpenRouter as **"Owl Alpha"** for roughly two months,
**topping developer coding usage** before Meituan claimed it. One relay
cites **SWE-bench Pro 59.5** ("beats GPT-5.5"); Meituan's own card claims
parity with the Gemini 3.1 Pro / GPT / Opus tier.

**Confirmed vs. vendor-supplied.** The **release and the OpenRouter
standing are independently observable** → `released`. The contested parts
are vendor claims: "beats GPT/Opus" is Meituan's own evaluation (no
third-party benchmark), and "trained entirely on Chinese chips" is Meituan's
framing — plausible given the observable performance, but the cluster's
silicon is unverified → `verification: partial`.

**Context.** This is the **moat-leak thesis made concrete**. Prior cycles
tracked it via GLM-5.2's Claude-matching cyber numbers ([[zhipu-glm-5-2]])
and DeepSeek V4's mid-July GA ([[deepseek-v4-ga-surge-pricing-2026-06]]);
LongCat-2.0 pushes it to **frontier scale** — a 1.6T open-weight model,
claimed domestic-silicon-trained, that was already winning real developer
usage incognito. The US export-control gate
([[anthropic-fable-mythos-export-control-2026-06]]) is being routed around in
the open.

**Transition triggers:**
- First independent SWE-bench Pro / LMArena numbers on the open weights →
  UPDATE, advance `verification`.
- Scrutiny confirming/refuting the all-domestic-silicon claim → UPDATE.
- A successor (LongCat-2.x / 3) → new ticket; do not reopen this one.
- ≥4 weeks settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further LongCat-2.0 signal (benchmarks, the chip claim,
API/pricing) UPDATES this ticket.
