---
slug: nvidia-gtc-taipei-2026-06
title: NVIDIA GTC Taipei 2026 — DGX Station for Windows, Cosmos 3, Alpamayo 2 Super, Nemotron 3 Ultra, RTX Spark, Isaac GR00T humanoid
company: NVIDIA
model: null
status: confirmed
status_note: |
  Jensen Huang's NVIDIA GTC Taipei keynote at Computex 2026 rolled out
  eleven distinct announcements in the 04:43 → 05:04 UTC band on
  2026-06-01, all primary @nvidianewsroom. The headline cluster:
  **DGX Station for Windows** (first deskside AI supercomputer to run
  frontier models up to 1 trillion parameters locally on Windows via
  NVIDIA GB300, with NVIDIA OpenShell for on-device agents, ASUS / Dell
  / GIGABYTE chassis partners); **Cosmos 3 family** (Super for highest-
  accuracy robotics + AV post-training, Nano for high-speed video /
  action reasoning, Edge for real-time edge inference); **Cosmos
  Coalition** (Agilex, Black Forest Labs, GeneralistAI, LTX Studio,
  Runway, Skild); **Alpamayo 2 Super** (32B open-weights reasoning VLA
  for level-4 robotaxis); **DRIVE Hyperion expansion** (Lucid + HUMAIN,
  VinFast + Autobrains, Uber + Autobrains); **Isaac GR00T Reference
  Humanoid Robot** (Unitree H2 body + Sharpa five-fingered hands +
  Jetson Thor compute); **Nemotron 3 Ultra** ("truly open" — weights +
  datasets + code, not weights-only); **RTX Spark** (1 PFLOP on-device
  AI inference for consumer Windows laptops, shipping fall 2026 with
  ASUS, Dell, HP, Lenovo, Microsoft Surface, MSI, Acer); **Vera CPU**
  (Jensen: "fastest product launch in our company's history"); and
  the **NVIDIA DSX platform** for end-to-end AI-factory infrastructure.
  Lands 24 hours before Microsoft Build 2026 keynote (2026-06-02
  09:30 PT) — the DGX Station for Windows + RTX Spark + OpenShell trio
  is unambiguously a Windows-on-NVIDIA pitch.
expected: "RTX Spark ships fall 2026 with every major OEM; DGX Station for Windows + Vera CPU availability windows TBD"
labels:
  - nvidia
  - keynote-bundle
  - cosmos
  - robotics
  - nemotron
  - rtx-spark
  - dgx-station
  - windows-on-nvidia
verification: confirmed
sources:
  - "@nvidianewsroom"
  - "@firstadopter"
  - "@SwanDesk"
  - "@Quipra_"
  - "@PANewsCN"
  - "@IdleProtocol"
  - "@andrei199868"
  - "@NVIDIAAI"
  - "@WesRoth"
  - "@Marktechpost"
created_at: 2026-06-01
updated_at: 2026-06-03
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-01
    change: "Created — NVIDIA GTC Taipei keynote (Computex 2026, Jensen Huang) shipped eleven announcements 2026-06-01 04:43–05:04 UTC via primary @nvidianewsroom: DGX Station for Windows (1T-param local on GB300 + OpenShell, ASUS/Dell/GIGABYTE), Cosmos 3 Super/Nano/Edge for robotics + AV + edge, Cosmos Coalition (Agilex, BFL, GeneralistAI, LTX, Runway, Skild), Alpamayo 2 Super (32B open driving VLA), DRIVE Hyperion expansion (Lucid+HUMAIN, VinFast+Autobrains, Uber+Autobrains), Isaac GR00T Reference Humanoid (Unitree H2 + Sharpa + Jetson Thor), Nemotron 3 Ultra truly-open (weights+datasets+code), RTX Spark (1 PFLOP consumer Windows AI inference, every major OEM, fall 2026), Vera CPU ('fastest product launch in our company's history' — Jensen), NVIDIA DSX AI-factory platform. Lands 24h before [[microsoft-build-2026-models]] keynote (2026-06-02 09:30 PT). Open driving VLA and Nemotron 3 Ultra published with weights"
  - ts: 2026-06-02
    change: "Param-size + benchmark clarifications surfaced 2026-06-01 04:46 UTC via primary @NVIDIAAI launch tweet (~2,514 likes / 376 RT) + 2026-06-02 07:00 UTC @WesRoth amplification: **Cosmos 3 Super = 32B, Cosmos 3 Nano = 8B** explicit parameter sizes (the bundle ticket previously had Super/Nano/Edge tiers without sizes). Cosmos 3 frames as 'the world's first fully open omnimodel with native vision reasoning, world and action generation' and 'ranks first among open models' across Artificial Analysis, Physics-IQ, PAI-Bench, R-Bench, RoboLab, RoboArena, VANTAGE-Bench, and TAR. Separately, **Nemotron 3 Ultra = 550B parameters** confirmed via @NVIDIAAI 'Nemotron 3 Ultra is coming this week' tweet (2026-06-01 04:35 UTC, ~3,030 likes / 332 RT) + @WesRoth secondary framing ('NVIDIA's most intelligent open-weight model so far'). Param-size disclosure was the only material delta in-window — strategic framing of the bundle (Windows-on-NVIDIA, agentic, robotaxi) unchanged"
  - ts: 2026-06-03
    change: "Cosmos 3 open release lands (transition trigger hit). @Marktechpost analysis 2026-06-03 08:41 UTC reports **model weights + GitHub repo + six SDG datasets + training recipes (SFT + action post-training) now publicly live under the OpenMDW-1.1 license** — the 'fully open' claim is now backed by actual artifacts, not just keynote framing. Architecture detail: two towers, one transformer (autoregressive VLM Reasoner → diffusion Generator). Refined param breakdown given as **total** sizes — Cosmos3-Nano 16B total (dense 8B + Qwen3-VL 8B), Cosmos3-Super 64B total (dense 32B + Qwen3-VL 32B); reconciles with the 2026-06-02 entry's 8B/32B figures, which were the dense-backbone sizes. A **4B Edge** model is stated for a later release. Deployment: Reasoner NIM now / Generator NIM later, BF16/FP8/NVFP4 quant (up to 2x with NVFP4), vLLM + Efficient Video Sampling. New HUE eval introduced. Secondary source (Marktechpost) corroborating primary @NVIDIAAI launch; bundle status stays confirmed"
---

NVIDIA's **GTC Taipei keynote at Computex 2026** ran 2026-06-01
04:43 → 05:04 UTC and consolidated eleven distinct announcements on
the @nvidianewsroom feed within a 20-minute window. This is the broadest
single-keynote surface NVIDIA has covered in 2026 and intentionally
lands 24 hours before Microsoft Build 2026's keynote (Fort Mason,
2026-06-02 09:30 PT) — the Windows-on-NVIDIA half of the cluster is
a deliberate counter-position before Nadella takes the stage.

**The keynote spine (all primary @nvidianewsroom):**

- **DGX Station for Windows** — the first deskside AI supercomputer
  to run frontier models with **up to 1 trillion parameters locally
  on Windows** via NVIDIA GB300, paired with **NVIDIA OpenShell** for
  building and running secure on-device agents. Chassis partners:
  ASUS, Dell, GIGABYTE (full list TBD). The Linux-native DGX line had
  existed; the Windows-first variant is the new product.
- **Cosmos 3 family** — **Cosmos Super (32B)** for highest-accuracy
  robotics + AV post-training, **Cosmos Nano (8B)** for high-speed
  video + action reasoning, **Cosmos Edge** for real-time edge
  inference. Per @NVIDIAAI's launch framing: "the world's first fully
  open omnimodel with native vision reasoning, world and action
  generation"; "ranks first among open models" on Artificial Analysis,
  Physics-IQ, PAI-Bench, R-Bench, RoboLab, RoboArena, VANTAGE-Bench,
  and TAR. Replaces the prior Cosmos generation as the world-model +
  simulation stack.
- **Cosmos Coalition** — Agilex Robotics, Black Forest Labs,
  GeneralistAI, LTX Studio, Runway, Skild AI as the named coalition
  of world-model builders + AI developers.
- **Alpamayo 2 Super** — NVIDIA's most powerful open driving
  foundation model to date, a **32-billion-parameter reasoning VLA**
  for level-4 robotaxis, shipping with AlpaGym + OmniDreams + a
  "physical AI agent skills" stack. Open-weights.
- **DRIVE Hyperion expansion** — the robotaxi-ready platform adds
  Lucid Motors + HUMAIN, VinFast + Autobrains, and Uber + Autobrains.
- **Isaac GR00T Reference Humanoid Robot** — the first **open
  humanoid robot reference design** for robotics research, combining
  the Unitree H2 body, Sharpa five-fingered hands, Jetson Thor
  compute, and the Isaac GR00T open software/models stack.
- **Nemotron 3 Ultra** — a **550-billion-parameter open-weight model**
  framed by @NVIDIAAI as "NVIDIA's most intelligent open-weight model
  so far," released **"truly open"**: weights + datasets + code, not
  weights-only. Drop window: "this week" per the 2026-06-01 @NVIDIAAI
  tweet.
- **RTX Spark** — **1 PFLOP of on-device AI inference** for consumer
  Windows laptops, shipping **fall 2026** with ASUS, Dell, HP, Lenovo,
  Microsoft Surface, MSI, Acer — every major PC OEM.
- **Vera CPU** — Jensen on-stage: "**Fastest product launch in our
  company's history**." Pairs with the "last six months everything
  changed" agentic-AI framing.
- **NVIDIA DSX platform** — end-to-end AI-factory infrastructure with
  modular open-source software libraries, APIs, reference designs, and
  partner tech across design, deployment, and operations.

**Why this is a single bundle ticket** (rather than 11 separate
tickets): the keynote ships a coherent strategic statement — NVIDIA
extending its frontier-AI footprint horizontally across consumer
Windows (RTX Spark), deskside (DGX Station for Windows), robotaxi
(Alpamayo 2 Super + DRIVE Hyperion), humanoid (Isaac GR00T), open
foundation models (Nemotron 3 Ultra), and AI-factory infrastructure
(DSX). Individual lines that develop their own cadence (e.g. a Nemotron
3 family successor, a separate Alpamayo 2 Heavy / Ultra release, an
Isaac GR00T 2.0) get their own tickets and back-link here.

**Distinct overlapping tickets (do NOT duplicate):**
- The **Microsoft Build 2026 keynote** the next day —
  [[microsoft-build-2026-models]] — is its own ticket; Build-day
  NVIDIA-Microsoft framing UPDATES that one, not this.
- **Anthropic–SpaceX Colossus compute lease**, **Huawei Tau Scaling
  Law**, and other compute-side / chip-architecture stories live on
  their own tickets ([[anthropic-spacex-colossus-2026-05]],
  [[huawei-tau-scaling-law-2026-05]]).

**Transition triggers:**
- RTX Spark ships in fall 2026 with a confirmed launch date and
  multi-OEM availability → UPDATE with the GA date; ≥4 weeks past →
  `closed: released-and-aged`.
- DGX Station for Windows pricing / availability window discloses →
  UPDATE.
- Nemotron 3 Ultra weights + datasets + code appear on Hugging Face /
  GitHub with independent reproduction → UPDATE.
- Independent reproductions of Alpamayo 2 Super on level-4 driving
  benchmarks → UPDATE.
- A successor Cosmos 4 family or Alpamayo 3 release → new ticket, link
  back here.

**Dedup note:** further GTC Taipei / Cosmos 3 / Alpamayo 2 Super /
Nemotron 3 Ultra / RTX Spark / DGX Station for Windows / Vera CPU /
Isaac GR00T / DSX signal UPDATES this ticket. Individual product
lines that grow load-bearing enough to warrant their own ticket
(e.g. Alpamayo 2 family becoming the dominant open driving VLA) can
be spun out later; until then this bundle is the canonical anchor.
