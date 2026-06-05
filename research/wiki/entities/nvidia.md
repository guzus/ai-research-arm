---
slug: nvidia
title: NVIDIA
type: entity
aliases: [NVIDIA, Nvidia, NVDA, "@nvidia", "@nvidianewsroom", "Jensen Huang", "Nemotron", "Nemotron-3-Ultra", "Nemotron-3-Ultra-550B", "Nemotron 3 Ultra"]
tags: [gpu, ai-chips, accelerators, open-weights, datacenter, semiconductors]
summary: The dominant AI accelerator supplier; its GPUs underwrite the AI-capex buildout, and on 2026-06-05 it released the open-weights Nemotron-3-Ultra-550B that dominated developer mindshare alongside Gemma 4.
created_at: 2026-06-05
updated_at: 2026-06-05
sources:
  - {title: "ARA daily digest 2026-06-05", path: research/digest/2026-06-05-digest.md}
  - {title: "ARA daily digest 2026-05-21", path: research/digest/2026-05-21-digest.md}
  - {title: "ARA model ticket — NVIDIA GTC Taipei 2026", path: research/models/tickets/nvidia-gtc-taipei-2026-06.md}
---

**NVIDIA** is the dominant supplier of AI training and inference accelerators —
the company whose GPUs (and the demand for them) sit at the structural center of
the [[ai-capex]] supercycle. Its earnings are the canonical "demand is real"
data point, its hardware is what [[neocloud]] providers like [[coreweave]] and
[[nebius]] buy on debt and rent back, and in 2026 it has increasingly shipped
its own **open-weights models** (the Nemotron line) on top of the silicon.

## Why it matters

- **The supply/demand pin.** NVIDIA's **Q1 FY27 print — $81.62B revenue (+85%
  Y/Y)**, Data Center $75.25B, a **$91B Q2 guide** above the buy-side bar, a
  fresh **$80B buyback** — is the canonical demand-is-real signal for the
  [[ai-capex]] buildout. Jensen Huang: "the largest infrastructure expansion in
  human history… agentic AI has arrived." Yet the stock slid ~3% after-hours,
  extending the **"beats but closes lower"** pattern — the market prices the
  *narrative*, not the quarter (ARA digest 2026-05-21). That same tell hit
  Broadcom far harder on 2026-06-05 (AVGO −12.6%, ~$320B erased on an *un-raised*
  guide) — see [[ai-capex]].
- **GTC Taipei keynote (2026-06-01).** Jensen Huang's Computex keynote rolled out
  eleven announcements, led by **DGX Station for Windows** (first deskside AI
  supercomputer running up to **1-trillion-parameter** models locally on Windows
  via GB300), the **Cosmos 3** robotics/AV world-model family, **Alpamayo 2
  Super** (32B open-weights VLA for L4 robotaxis), **Isaac GR00T** reference
  humanoid, **RTX Spark** (1 PFLOP on-device inference for consumer Windows
  laptops, fall 2026), and the **Vera CPU** ("fastest product launch in company
  history"). The DGX Station + RTX Spark + OpenShell trio is unambiguously a
  **Windows-on-NVIDIA** pitch, landing 24h before [[microsoft]] Build 2026.
- **Nemotron-3-Ultra-550B — the open-weights play (2026-06-05).** NVIDIA released
  **Nemotron-3-Ultra-550B-A55B**, a **LatentMoE hybrid** (Mamba-2 + MoE +
  Attention + MTP), **550B total / 55B active**, **1M context**, **NVFP4
  pre-training**, with toggleable reasoning. It is **datacenter-only**
  (8×GB200 / 16×H100) under **OpenMDW 1.1** (commercial use OK), and — per the
  GTC framing — "**truly open**": weights + datasets + code, not weights-only.
  It dominated Hacker News and r/LocalLLaMA alongside Google's [[gemma-4]],
  bracketing the 2026 open-weights wave: Nemotron's datacenter-scale 550B at one
  end, Gemma's 16 GB-laptop accessibility at the other. NVIDIA also shipped
  **Nemotron 3.5 Content Safety**, a customizable multimodal enterprise safety
  model (Hugging Face) (ARA digest 2026-06-05).

## Open questions

- **Does shipping open-weights models cannibalize or deepen the silicon moat?**
  Nemotron is datacenter-only and NVFP4-native — a model that runs best on
  NVIDIA hardware is a demand pull, not a giveaway.
- **The TSMC ceiling.** TSMC warned (2026-06-05) it **cannot meet AI-chip demand
  even with US expansion** — a hard supply constraint sitting directly upstream
  of NVIDIA's guides (see [[ai-capex]]).
- **The "beats but closes lower" tell.** Why does the market keep selling the
  single best supply-side data point? Priced-in growth, or early doubt about the
  supercycle's durability?
