---
slug: nvidia
title: NVIDIA
type: entity
aliases: [NVIDIA, Nvidia, NVDA, "@nvidia", "@nvidianewsroom", "Jensen Huang", "Nemotron", "Nemotron-3-Ultra", "Nemotron-3-Ultra-550B", "Nemotron 3 Ultra"]
tags: [gpu, ai-chips, accelerators, open-weights, datacenter, semiconductors]
description: The dominant AI accelerator supplier and the anchor of a reported ~$500B Wall Street AI-infrastructure financing package (2026-08-10); agreed to backstop $105B of OpenAI's Ohio PORTS-Pike lease (2026-08-18), backs Ilya Sutskever's Safe Superintelligence (~$5B), the open-weights Nemotron line now targeting a 1T-parameter Nemotron 4, and the residual-value guarantees inside its own ~$500B package.
created_at: 2026-06-05
timestamp: 2026-08-18T00:00:00Z
market:
  ticker: NVDA
  exchange: NASDAQ
  symbol: NASDAQ:NVDA
  provider: yahoo
sources:
  - {title: "ARA daily digest 2026-08-18", path: research/digest/2026-08-18-digest.md}
  - {title: "ARA daily digest 2026-08-13", path: research/digest/2026-08-13-digest.md}
  - {title: "ARA daily digest 2026-08-12", path: research/digest/2026-08-12-digest.md}
  - {title: "ARA daily digest 2026-08-11", path: research/digest/2026-08-11-digest.md}
  - {title: "ARA daily digest 2026-08-05", path: research/digest/2026-08-05-digest.md}
  - {title: "ARA daily digest 2026-07-29", path: research/digest/2026-07-29-digest.md}
  - {title: "ARA model ticket — NVIDIA Taiwan smuggling probe", path: research/models/tickets/nvidia-taiwan-smuggling-probe-2026-07.md}
  - {title: "ARA daily digest 2026-07-28", path: research/digest/2026-07-28-digest.md}
  - {title: "ARA daily digest 2026-06-30", path: research/digest/2026-06-30-digest.md}
  - {title: "ARA daily digest 2026-06-05", path: research/digest/2026-06-05-digest.md}
  - {title: "ARA daily digest 2026-05-21", path: research/digest/2026-05-21-digest.md}
  - {title: "ARA model ticket — NVIDIA GTC Taipei 2026", path: research/models/tickets/nvidia-gtc-taipei-2026-06.md}
images:
  - url: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/NVIDIA_H100_%28%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan%29_007.png/1280px-NVIDIA_H100_%28%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan%29_007.png"
    alt: "Close-up of an NVIDIA H100 accelerator used to depict NVIDIA's role in AI training and inference."
    caption: "NVIDIA H100 hardware, the accelerator class at the center of the AI-capex buildout."
    credit: "Geekerwan / Wikimedia Commons (CC BY 3.0)"
    source_url: "https://commons.wikimedia.org/wiki/File:NVIDIA_H100_(%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan)_007.png"
  - url: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Nvidia_DGX_Station%2C_world%27s_most_powerful_desktop%2C_a_Supercomputer_at_the_office.webm/1280px--Nvidia_DGX_Station%2C_world%27s_most_powerful_desktop%2C_a_Supercomputer_at_the_office.webm.jpg"
    alt: "NVIDIA DGX Station deskside AI supercomputer shown as an example of NVIDIA's local and datacenter AI systems."
    caption: "DGX Station-class hardware, useful context for the page's deskside AI-supercomputer discussion."
    credit: "Charbax / Wikimedia Commons (CC BY 3.0)"
    source_url: "https://commons.wikimedia.org/wiki/File:Nvidia_DGX_Station,_world%27s_most_powerful_desktop,_a_Supercomputer_at_the_office.webm"
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
  [[broadcom]] far harder on 2026-06-05 (AVGO −12.6%, ~$320B erased on an
  *un-raised* guide) — see [[ai-capex]].
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

- **Anthropic's first deployment lands on NVIDIA silicon (2026-06-30).**
  [[anthropic|Anthropic's]] [[claude-opus-4-8|Claude Opus 4.8]] and **Haiku 4.5** went
  GA in **[[microsoft|Microsoft Foundry]] on Azure** running on **NVIDIA GB300 NVL72
  (Blackwell Ultra)** systems with **Quantum-X800 InfiniBand** — reportedly the
  **first time Anthropic models run on NVIDIA GPUs** (its stack historically leaned on
  AWS Trainium and Google TPUs). It is a notable demand-pull data point: the last
  major frontier lab not natively on NVIDIA now ships its flagship on Blackwell Ultra,
  reinforcing the silicon's position at the center of the [[ai-capex]] buildout. *(The
  "first-ever on NVIDIA" superlative was initially single-sourced.)* (ARA digest
  2026-06-30).

- **A trio of capital/alliance moves stack in one day (2026-07-28).** NVIDIA
  is reportedly discussing a **~$250B financing backstop** for [[openai|OpenAI]]'s
  **10-gigawatt southern-Ohio datacenter campus** (SoftBank-developed, ~$500B
  total cost), alongside a **separate ~$350B talk for OpenAI to buy Nvidia
  chips** — an arrangement one monitored account flagged as circular
  financing (see [[openai]] and [[ai-capex]]). Separately, NVIDIA committed a
  reported **~$5B to [[safe-superintelligence|Ilya Sutskever's Safe Superintelligence]]**
  against SSI's **$32B post-money valuation**, hours
  after the two companies confirmed a compute partnership — its first
  substantial disclosed SSI backing since the 2024 founding, framed as
  milestone-contingent rather than a straight cash payment. And NVIDIA's new
  **Open Secure AI Alliance** — Hugging Face, [[microsoft|Microsoft]], Palo
  Alto Networks, [[salesforce|Salesforce]], SAP, Red Hat, Cloudflare — shipped
  AI-security tooling with **OpenAI conspicuously absent** from the published
  member list; one unverified relay claims an internal decision drew employee
  "backlash" (ARA daily digest 2026-07-28).

- **Taiwan chip-smuggling probe turns criminal (2026-07-29).** A Taiwanese
  court approved continued detention of the NVIDIA employee held since
  2026-07-28, citing suspected **document forgery and breach of trust**, and
  linked the case to a **broader network** that already includes a detained
  Super Micro-connected distributor and a data-center operator — widening
  what began as a single-employee detention (see the model ticket
  `nvidia-taiwan-smuggling-probe-2026-07`) into a multi-party criminal
  investigation into chips reaching China around export controls. First
  time Taiwan's government has taken direct action against an NVIDIA
  employee (ARA daily digest 2026-07-29).

- **The second source gets a quarter to point at; HBM becomes the shared
  constraint (2026-08-05).** [[amd|AMD]] posted **Data Center revenue of $6.7B,
  up 107% YoY** at 58% of the company with **Helios beginning to ramp** into
  [[anthropic]]'s 2 GW MI450 commitment — the first quarterly print that makes
  "credible second source" a number rather than a narrative. In the same cycle
  **TrendForce reported NVIDIA has been re-evaluating Rubin Ultra's HBM
  configuration since early Q3 2026 with no final spec chosen**, against 2027
  HBM bit shipments projected up 50–60% and still short of demand. Memory
  allocation, not accelerator design, is what both vendors are now scheduling
  around — see [[ai-capex]] and [[micron]] (ARA daily digest 2026-08-05).

## Open questions

- **Does shipping open-weights models cannibalize or deepen the silicon moat?**
  Nemotron is datacenter-only and NVFP4-native — a model that runs best on
  NVIDIA hardware is a demand pull, not a giveaway.

## Wall Street assembles ~$500B around NVIDIA — on debt (2026-08-10)

A **~$500B AI-infrastructure financing package** is reported assembling around
NVIDIA with **Apollo, Blackstone, BlackRock's Global Infrastructure Partners,
Brookfield, Goldman Sachs and KKR** named — CNBC's relay sourced to one
anonymous person, with a later FT-attributed relay specifying **debt rather than
equity**, the material distinction (leverage against depreciating GPU assets).
**Unconfirmed by any named participant.** The first named vehicle attached to the
syndicate is the **Nvidia–IREN "DSX AI factories" partnership**, announced with
quoted executives (Jensen Huang, Brookfield's Bruce Flatt, BlackRock's Larry
Fink, Blackstone's Jon Gray); IREN nonetheless closed **down ~6.1%** on the
session before the announcement landed. See [[ai-capex]] for how this extends the
off-balance-sheet financing pattern this page has tracked since the OpenAI Ohio
backstop (CNBC/FT via relays; ARA daily digest 2026-08-11).

## The 25% backstop is named — and the Nemotron line pivots to agents (2026-08-11/12)

- **The 25% per-project backstop, reported (2026-08-11/12).** *The Information*
  reported NVIDIA can absorb **up to 25% of losses on individual projects** inside
  the ~$500B package — including projects **its own GPUs are sold into** — the
  precise circularity the "new asset class" framing was built to answer. **No
  term sheet is public**; the "single anonymous CNBC source" and "debt, not
  equity" caveats from the 2026-08-10 entry still govern. On 2026-08-13 the WSJ
  reported **Jensen Huang characterising that support as residual-value
  guarantees** — NVIDIA **underwrites the resale floor of hardware whose
  obsolescence it schedules**, the vendor-controlled-depreciation reading of the
  backstop (ARA daily digest 2026-08-12/13).
- **Nemotron 3.5 Lightning + NeMo Switchyard — the agent-volume pitch
  (2026-08-11/12).** NVIDIA released **Nemotron 3.5 Lightning**, an
  **open-weight 30B mixture-of-experts** model with **~3B active parameters**
  aimed at **always-on agents**, plus **NeMo Switchyard**, a routing library that
  sends each step to the cheapest capable model. It shipped **27 hours after
  [[meta|Meta]] open-weighted its own 30B agent model** ([[muse-glimmer]]), and
  the accompanying pitch is **agent *volume*, not benchmark supremacy** —
  [[openai|OpenAI]] and [[anthropic]] traffic is the target, not a leaderboard.
  The most concrete public number yet on routing economics: **LangChain
  benchmarked Switchyard on 145 agent tasks and found only 7% of turns needed a
  frontier model**, with routing cutting cost **74% at a six-point accuracy
  loss** — a public estimate of how much agent traffic is over-served.
  On 2026-08-13 **Nemotron 3.5 Lightning went live on the Perplexity Agent API**
  at **$0.0115/$0.17 per million tokens** — the cheapest widely-distributed
  agent-model rate card of the cycle (The Information, The Decoder, LangChain;
  ARA daily digest 2026-08-12/13).
- **Nemotron 4 reported in development — now aimed at the leading edge
  (2026-08-11/13).** Per *The Information* and The Decoder, NVIDIA is building
  an **open-weight family targeting one trillion parameters** — a scale
  **Chinese labs have already passed** — with the goal of **spurring Western
  open-source competition**. The Information separately reports NVIDIA is aiming
  to make **Nemotron 4 leading-edge**, which would put it **in competition with
  the model labs that are its largest customers** — the Nemotron line's
  cannibalization question (below) posed at its sharpest. Treat as reported; no
  artifact exists yet (ARA daily digest 2026-08-12/13).
- **NVIDIA guarantees $105B of OpenAI's Ohio lease — the backstop gets a number
  and a campus (2026-08-18).** The OpenAI Ohio lease backstop tracked since
  the 2026-07-28 ~$250B talk hardened into a specific, capped commitment:
  NVIDIA agreed to **backstop up to $105 billion of OpenAI's 20-year lease**
  at the **PORTS-Pike campus**, triggering on **OpenAI default or insolvency**
  and covering **rent, power, and the buildings' residual value**. The
  Information's reporter states the reason plainly: **lenders will underwrite
  NVIDIA's balance sheet, not OpenAI's** — NVIDIA cannot fund that volume of
  borrowing itself, so it guarantees the paper. That guarantee, **not** the
  separately-reported **$1.5B equity stake in developer SB Energy**, is the real
  exposure. Separately, the SB Energy stake gives NVIDIA **exclusive AI compute
  supply to PORTS-Pike** (4.25 GW initial IT load plus a 3.75 GW option block,
  phased from 2028); Jensen Huang puts OpenAI's **total commitment at ~12 GW by
  2030, expandable to ~16 GW**, framed as **roughly $600B of NVIDIA revenue** —
  NVIDIA's own projection off its own capacity assumption, not a booking. See
  [[ai-capex]] and [[openai]] for how this sits inside the $500B debt package
  (The Decoder, TechCrunch, The Information; ARA daily digest 2026-08-18).

## Open questions
- **The TSMC ceiling.** TSMC warned (2026-06-05) it **cannot meet AI-chip demand
  even with US expansion** — a hard supply constraint sitting directly upstream
  of NVIDIA's guides (see [[ai-capex]]).
- **The "beats but closes lower" tell.** Why does the market keep selling the
  single best supply-side data point? Priced-in growth, or early doubt about the
  supercycle's durability?
