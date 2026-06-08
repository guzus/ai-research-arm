---
slug: nvidia-korea-ai-factories-2026-06
title: NVIDIA × LG Group + SK Group — Korea "AI Factories" (DSX, Isaac GR00T, HBM co-development)
company: NVIDIA
model: null
status: confirmed
status_note: |
  During Jensen Huang's **Seoul visit on 2026-06-08**, NVIDIA unveiled a
  cluster of South Korea partnerships to build "**AI Factories**":
  - **LG Group** — AI factories on the **NVIDIA DSX** platform; LG's
    **CLOiD** home assistants to be trained with the **Isaac GR00T**
    model; LG subsidiaries pushing data centers, autonomous-driving
    systems, and factory robots. LG Energy Solution working with NVIDIA
    on 800V DC power for data centers.
  - **SK Group** — extending the partnership beyond memory chips into
    full-stack AI factories (semiconductors + data centers + AI infra);
    a multi-year **SK hynix / SK Telecom (SKM)** deal to co-develop the
    next generation of **HBM** memory aligned to NVIDIA's roadmap (Vera
    Rubin → Jetson Thor), with SK bringing CUDA-X + Omniverse into its
    fabs. Same-day tie-ups also cited with **Doosan** and **NAVER**.
  Relayed across multiple secondary accounts as an official NVIDIA / LG /
  SK announcement; no primary @nvidianewsroom handle captured in-window,
  hence verification: partial. Distinct from the 2026-06-01 GTC Taipei
  keynote bundle ([[nvidia-gtc-taipei-2026-06]]), which introduced the
  DSX platform and Isaac GR00T this deal now deploys in Korea.
expected: "Build-out multi-year; HBM co-development aligned to NVIDIA Vera Rubin / Jetson Thor cycles; specific capacity + dates TBD"
labels:
  - nvidia
  - partnership
  - ai-factory
  - korea
  - robotics
  - isaac-groot
  - hbm
  - sovereign-ai
verification: partial
sources:
  - "@_PradeepGoel"
  - "@PSInvestor"
  - "@celestrix"
created_at: 2026-06-08
updated_at: 2026-06-08
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-08
    change: "Created — NVIDIA unveiled a Korea 'AI Factories' partnership cluster during Jensen Huang's Seoul visit (2026-06-08). LG Group: AI factories on NVIDIA DSX, CLOiD home assistants trained with Isaac GR00T, LG subsidiaries on data centers / autonomous driving / factory robots, LG Energy Solution on 800V DC data-center power. SK Group: partnership extended beyond memory into full-stack AI factories; multi-year SK hynix/SKM HBM co-development aligned to NVIDIA's roadmap (Vera Rubin → Jetson Thor), SK adopting CUDA-X + Omniverse in its fabs; same-day Doosan + NAVER tie-ups. Multiple secondary relays (@_PradeepGoel, @PSInvestor, @celestrix) of an official NVIDIA/LG/SK announcement; no primary handle captured in-window → status confirmed, verification partial. Deploys the DSX + Isaac GR00T stack introduced at [[nvidia-gtc-taipei-2026-06]]"
---

On **2026-06-08**, during Jensen Huang's visit to **Seoul**, NVIDIA
announced a cluster of South Korea partnerships to build "**AI
Factories**" — vertically integrated stacks spanning semiconductors,
data centers, robotics, and AI infrastructure. This is a deployment /
partnership event, not a model release: the model and platform pieces
(NVIDIA **DSX**, **Isaac GR00T**) were introduced at the GTC Taipei
keynote a week earlier ([[nvidia-gtc-taipei-2026-06]]); this ticket
tracks their landing in Korea's industrial base.

**LG Group.** AI factories powered by the **DSX** platform. LG's
**CLOiD** home-assistant robots are to be trained using the **Isaac
GR00T** model, while LG subsidiaries push forward on data centers,
autonomous-driving systems, and factory robots. **LG Energy Solution**
is working with NVIDIA on **800-volt DC** power delivery for data
centers — a tell that the build-out is already running into the same
power/physics ceiling that dominates the rest of the 2026 infra story.

**SK Group.** The existing SK–NVIDIA relationship is being extended
**beyond memory chips** into full-stack AI factories. A multi-year **SK
hynix / SK Telecom (SKM)** agreement co-develops the next generation of
**HBM** aligned to NVIDIA's accelerator roadmap (from Vera Rubin systems
down to Jetson Thor robotics), locking in supply across several product
cycles. It runs both ways: SK is bringing NVIDIA's **CUDA-X** and
**Omniverse** software into its own fabs to speed chip design and push
toward autonomous manufacturing. Same-day tie-ups with **Doosan** and
**NAVER** were also cited.

**Why `confirmed` / `partial`.** The announcement is dated, specific,
and relayed independently across multiple accounts as an official
NVIDIA / LG / SK statement (the LG factory deal, the SK HBM deal, and
the Doosan/NAVER tie-ups surface from different posters). That clears
`confirmed`. But no **primary** @nvidianewsroom / LG / SK handle was
captured in this cycle's signal, so `verification` stays `partial`
until a primary citation lands.

**Why this is its own ticket** rather than rolling into
[[nvidia-gtc-taipei-2026-06]]: GTC Taipei was a product-launch keynote
(DSX, Isaac GR00T, Cosmos 3, Nemotron 3 Ultra, RTX Spark). This is a
**named multi-conglomerate partnership** with its own counterparties
(LG Group, SK Group, Doosan, NAVER), its own commercial structure (HBM
co-development, AI-factory build-out), and its own geography (Korea). It
*consumes* the GTC stack rather than introducing it.

**Transition triggers:**

- Primary NVIDIA / LG / SK announcement URL or handle → UPDATE,
  advance `verification` to `confirmed`.
- Concrete capacity, GW, or capex figures for the Korea AI factories →
  UPDATE.
- HBM co-development milestones (tape-out, first samples aligned to Vera
  Rubin) → UPDATE.
- CLOiD / Isaac GR00T robot shipping milestone → UPDATE (or spin out a
  robot ticket if it grows load-bearing).
- Build-out settles into normal coverage ≥4 weeks past a defined GA →
  `closed: released-and-aged`.

**Dedup note:** further NVIDIA-in-Korea / LG AI factory / SK hynix HBM
co-development / Doosan / NAVER signal UPDATES this ticket. NVIDIA's
GTC Taipei product bundle stays on [[nvidia-gtc-taipei-2026-06]]; the
Google–SpaceX orbital-compute thread stays on
[[google-spacex-compute-2026-06]].
