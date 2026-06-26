---
slug: nvidia-dflash-2026-06
title: NVIDIA DFlash — open-sourced block-diffusion speculative decoding (up to 15x Blackwell throughput)
company: NVIDIA
model: DFlash
status: released
status_note: |
  NVIDIA **open-sourced DFlash** — a **block-diffusion speculative-decoding**
  technique (from UC San Diego + NVIDIA) that generates full token blocks in
  parallel, delivering **up to 15x throughput on Blackwell** for ~120B models.
  Works with **vLLM / SGLang / TensorRT-LLM with no application rewrites**, and
  is **shipping now**. Important framing: it is **not** a blanket "15x Blackwell
  uplift" — it is a **decode-efficiency layer for specific workloads** (the 15x
  is workload-specific, not general). A competing/complementary answer to
  custom inference silicon: NVIDIA isn't ceding the inference-efficiency
  narrative to OpenAI's Jalapeño ASIC ([[openai-jalapeno-chip-2026-06]]) —
  DFlash is the software-optimization path to the same question (can inference
  cost keep dropping fast enough to sustain demand growth). Single-relay
  coverage in this window (@arsh_goyal); the open-source release itself is
  verifiable but the headline 15x figure should be read as workload-specific
  until independent benchmarks land.
expected: "Independent benchmark results vs the 15x claim across broader workloads; whether inference-optimized silicon (Jalapeño) and software optimization (DFlash) emerge as complements or competing paths"
labels:
  - nvidia
  - inference
  - open-source
  - software
  - released
verification: partial
sources:
  - https://x.com/arsh_goyal/status/2070029887407284303
  - "@arsh_goyal"
created_at: 2026-06-26
updated_at: 2026-06-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-26
    change: "Created — NVIDIA open-sourced DFlash (block-diffusion speculative decoding, UC San Diego + NVIDIA): generates full token blocks in parallel, up to 15x Blackwell throughput on ~120B models, works with vLLM/SGLang/TensorRT-LLM with no app rewrites, shipping now. Framing caveat logged: 15x is workload-specific (decode-efficiency layer for specific workloads), not a blanket Blackwell uplift. Open-sourced and shipping → status released; verification partial (single-relay window coverage via @arsh_goyal; the 15x headline awaits independent benchmarks). Competing/complementary to OpenAI Jalapeño ASIC ([[openai-jalapeno-chip-2026-06]]) — NVIDIA's software-optimization answer to the inference-cost question."
---

**DFlash** is a **block-diffusion speculative-decoding** technique from
UC San Diego + NVIDIA that NVIDIA **open-sourced**. It generates full token
blocks in parallel rather than token-by-token, delivering **up to 15x
throughput on Blackwell** for ~120B-parameter models, and works with
**vLLM, SGLang, and TensorRT-LLM with no application rewrites**. It is
**shipping now**.

**Why `released` / `partial`.** It is open-sourced and usable today →
`released`. `verification: partial` because the in-window coverage was a
single relay (@arsh_goyal); the open-source release itself is verifiable, but
the headline **15x figure is workload-specific** — it is a decode-efficiency
layer for particular workloads, not a blanket Blackwell uplift — and should be
read as such until independent benchmarks land across a broader model/workload
set.

**Why it matters.** DFlash is NVIDIA's answer to the same inference-cost
question that OpenAI's **Jalapeño** ASIC ([[openai-jalapeno-chip-2026-06]])
answers with custom silicon: can inference cost keep dropping fast enough to
sustain the demand growth curve? DFlash is the **software-optimization path**,
Jalapeño the **custom-silicon path** — whether they emerge as complements or
competitors is the open industry question. NVIDIA isn't ceding the
inference-efficiency narrative.

**Transition triggers:**
- Independent benchmark results vs the 15x claim → UPDATE, append history.
- Broader framework integrations or production deployment data → UPDATE.
- A successor technique → new ticket.
- ≥4 weeks past release, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further DFlash signal (benchmarks, integrations, adoption)
UPDATES this ticket. Other NVIDIA stories stay on their own tickets
([[nvidia-gtc-taipei-2026-06]], [[nvidia-korea-ai-factories-2026-06]],
[[nvidia-nemotron-openrouter-2026-06]]).
