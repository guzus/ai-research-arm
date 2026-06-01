---
slug: figure-helix-02-2026-05
title: Figure Helix-02 — 200-hour autonomous fleet run, 249,560 packages, zero failures, zero teleoperation
company: Figure AI
model: Helix-02
status: confirmed
status_note: |
  Figure 03 fleet anchored by the unit nicknamed "Rose" cleared
  **200 continuous hours** of autonomous package sorting at Figure's
  Sunnyvale HQ on 2026-05-30, processing **249,560 packages** with
  the dashboard still climbing. CEO **Brett Adcock** confirmed
  **zero hardware failures** and **zero teleoperation** across the
  full window; the fleet ran entirely on **Helix-02**, Figure's
  in-house VLA neural network, with **autonomous task selection,
  autonomous fault recovery, and autonomous rotation to charging**.
  The run started as a 2026-05-20 8-hour livestream and Figure declined
  to stop after each milestone, escalating past 60h, 100h, and finally
  200h. Prior publicly-verified continuous-autonomy shifts (Optimus,
  Apollo, 1X Neo, Sanctuary, Unitree) topped out near 10–20h at
  meaningful throughput — Helix-02's run is **~10× the previous
  envelope** on MTBI (mean-time-between-intervention), the metric
  governing warehouse / 3PL / manufacturing procurement. Strategic
  frame from the company: Helix-02 is internally developed end-to-end,
  making Figure the only humanoid OEM with **zero frontier-lab
  inference dependency** — a deliberate distinction within the same
  72-hour band as [[openai-robotics-2026-05]] and
  [[nvidia-gtc-taipei-2026-06]] (Isaac GR00T humanoid reference).
expected: "BotQ-scale Figure 4 procurement / supply-chain independence runway"
labels:
  - released
  - figure
  - helix
  - humanoid
  - vla
  - capability-disclosure
  - robotics
verification: confirmed
sources:
  - "@adcock_brett"
  - https://humanoidsdaily.com
created_at: 2026-06-01
updated_at: 2026-06-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-01
    change: "Created — Figure 03 fleet (Rose anchor unit) cleared 200 continuous hours of autonomous package sorting at Sunnyvale HQ ending 2026-05-30, processing 249,560 packages, dashboard still climbing. Brett Adcock confirmed zero hardware failures, zero teleoperation. Fleet ran entirely on Helix-02 VLA — autonomous task selection / fault recovery / charging rotation. Started 2026-05-20 8h livestream, escalated past 60h/100h/200h. ~10× prior public MTBI envelope (Optimus/Apollo/1X Neo/Sanctuary/Unitree topped out ~10–20h). Helix-02 internally developed end-to-end → Figure has zero frontier-lab inference dependency. Lands same 72h as [[openai-robotics-2026-05]] formalization and [[nvidia-gtc-taipei-2026-06]] Isaac GR00T humanoid reference"
---

**Figure AI's 200-hour Helix-02 marathon** is the longest
publicly-verified autonomous humanoid shift on record. The Figure 03
fleet — anchored by the unit nicknamed **"Rose"** — cleared
**200 continuous hours** of autonomous package sorting at Figure's
Sunnyvale HQ, processing **249,560 packages**, with CEO **Brett
Adcock** confirming **zero hardware failures** and **zero
teleoperation** across the full window.

**What ran the run.** The fleet ran entirely on **Helix-02**, Figure's
in-house Vision-Language-Action neural network. The shift exercised:

- **Autonomous task selection** — Helix-02 chose what to do next.
- **Autonomous fault recovery** — Helix-02 handled hardware /
  perception edge cases without human intervention.
- **Autonomous rotation to charging** — when batteries depleted, the
  units routed themselves to chargers, and the fleet kept running.

**The escalation pattern.** The run started as a **2026-05-20
8-hour livestream**. Figure declined to stop after the original
challenge cleared, escalating past 60h, 100h, and finally 200h on
**2026-05-30**.

**Why this is load-bearing on the model-timeline lane.** Prior
publicly-verified continuous-autonomy shifts — Tesla Optimus, Apptronik
Apollo, 1X Neo, Sanctuary Phoenix, Unitree H1/H2 — have topped out
**near 10–20 hours** at meaningful throughput. Helix-02's run is
**roughly 10× the previous envelope** on **MTBI**
(mean-time-between-intervention), the metric that actually governs
warehouse / 3PL / manufacturing procurement decisions. A capability
proof at this scale resets the procurement floor for the whole
humanoid lane.

**Strategic frame from Figure.** Helix-02 is **internally developed
end-to-end** — Figure runs no frontier-lab inference inside the VLA
loop. That posture is a deliberate distinction in a week with
**[[openai-robotics-2026-05]]** (OpenAI's world-sim research formally
becoming a hardware-manufacturing org), **[[nvidia-gtc-taipei-2026-06]]**
(NVIDIA's Cosmos 3 + Isaac GR00T humanoid reference + Alpamayo 2
Super 32B open driving VLA), and the rising **Anthropic Series H at
$965B** ([[anthropic-series-h-2026-05]]) — Brett Adcock framed the
"no frontier-lab dependency" line directly as a supply-chain
independence thesis underwriting BotQ-scale Figure 4 procurement.

**Why this is its own ticket** (rather than rolling into NVIDIA Isaac
GR00T or the OpenAI Robotics announcement): Helix-02 is a *Figure-
specific named VLA*, and the capability disclosure (the 200h run) is
the **first time** a humanoid OEM has publicly cleared multi-day
continuous-autonomy at production throughput. Distinct from the
hyperscaler-aligned humanoid stacks (NVIDIA's GR00T reference design,
OpenAI's eventual robotics product), and distinct from the existing
Helix-01 baseline that Figure had been operating against.

**Transition triggers:**

- A successor model (Helix-03, Helix-Pro) or a named variant
  capability bump → UPDATE history.
- A real customer-facing deployment (warehouse / 3PL / manufacturing
  contract publicly confirmed) → UPDATE.
- A regression / publicly-reported autonomous-shift failure that
  contradicts the "zero hardware failures, zero teleoperation"
  framing → UPDATE, document.
- ≥4 weeks past the 2026-05-30 disclosure with the capability
  settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further Helix-02 / Figure 03 / Figure 4 / Brett
Adcock primary signal UPDATES this ticket. A successor humanoid OEM
capability disclosure (Tesla Optimus G2, Apptronik Apollo 2, 1X Neo
Generation, Sanctuary Phoenix 9) gets its own ticket and back-links
here as the comparator on MTBI envelopes. The NVIDIA Isaac GR00T
humanoid reference design ([[nvidia-gtc-taipei-2026-06]]) lives on
the GTC Taipei bundle ticket, not here.
