---
slug: stanford-marin-535b-2026-08
title: Marin 535B-A23B — fully open pretraining run begins
company: Stanford CRFM (Marin)
model: Marin 535B-A23B
status: in-testing
status_note: |
  **@percyliang** (2026-08-21 21:44 UTC, ~2,570 likes / 342 RT): "🚢
  **Marin 535B-A23B started training this week!** As usual, the whole
  process is open. Voyage plan: **pretraining (80%) + midtraining (20%)
  on 18.75T tokens on 11 × GB200 NVL72 for ~3 months (2.7e24 FLOPs)**.
  Post-training will follow. Before kicking off the run, we trained a
  4-rung scaling ladder from 1.6B-A61M (48B tokens) to 27.7B-A1.2B (926B
  tokens) to debug issues, and to make a forecast of our hero run. This
  is by far our biggest run, so definitely expecting the unexpected."

  Status `in-testing` and verification `confirmed`: the training run is
  a **real artifact in progress**, disclosed by the project's principal
  with a complete and unusually specific plan — parameter count and
  active-parameter split (535B total / 23B active MoE), token budget,
  hardware, wall-clock, and total compute. Follow-up posts published the
  **data composition**, a **live wandb dashboard for the run**, and the
  **GitHub repository**; a team member (@classiclarryd) added that
  scaling laws let them simulate the entire training trajectory, and
  @percyliang showed forecasts of intermediate-checkpoint loss, not just
  final loss.

  It is `in-testing` rather than `confirmed`-as-a-release because **no
  model exists yet** — this is a three-month run that started this week,
  and post-training follows it.
expected: "Training started week of 2026-08-17; ~3 months of pretraining + midtraining on 18.75T tokens (2.7e24 FLOPs) on 11 x GB200 NVL72, post-training after. Pending: intermediate checkpoints against the published forecast, whether the run holds its trajectory, weights release, and post-training results"
labels:
  - open-weights
  - academic
  - pretraining
  - moe
  - in-testing
verification: confirmed
sources:
  - "@percyliang"
  - "@classiclarryd"
created_at: 2026-08-23
updated_at: 2026-08-23
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-23
    change: "Created — Stanford's Marin project began training Marin 535B-A23B (@percyliang, 2026-08-21 21:44 UTC, ~2,570 likes): 18.75T tokens, 80% pretraining / 20% midtraining, 11 x GB200 NVL72, ~3 months, 2.7e24 FLOPs, with post-training to follow. Preceded by a 4-rung scaling ladder from 1.6B-A61M (48B tokens) to 27.7B-A1.2B (926B tokens) used to debug and to forecast the hero run; the team also forecasts intermediate-checkpoint loss, not only final loss. Data composition, a live wandb dashboard for the run, and the GitHub repo were all published alongside. Status in-testing (run in progress, no model yet); verification confirmed (project principal, full disclosed plan, live public instrumentation)."
---

Nearly every training run in this ticket set is disclosed after the fact,
by a lab, in a launch post. **Marin discloses it in advance and streams
it.** The token budget, the MoE split (535B total / 23B active), the
hardware (11 × GB200 NVL72), the wall-clock, the FLOP count, the data
composition, the code, and a live wandb dashboard are all public before
the model exists.

**The methodological claim is the interesting one.** The team trained a
four-rung scaling ladder — 1.6B-A61M on 48B tokens up to 27.7B-A1.2B on
926B tokens — not just to debug infrastructure but to **forecast the
hero run's loss curve**, including intermediate checkpoints. That
converts scaling laws from a retrospective description into an
operational prediction with a public scoreboard: anyone can watch
whether the 535B run tracks the forecast the ladder produced. If it
diverges, that is a published result about the limits of scaling-law
extrapolation at the frontier; if it tracks, it is evidence that a
large run's trajectory is knowable from small ones.

**What this is not.** No weights, no benchmarks, no model. A three-month
run started this week, with post-training after it. @percyliang's own
framing — "by far our biggest run, so definitely expecting the
unexpected" — is the right expectation to hold.

The context that makes an academic open run matter right now is the same
one running through this week's other tickets: open-weight models took a
record 62% of tokens on Vercel's AI Gateway (@rauchg, 2026-08-22), up
from 28.4% in June, and the Flash-tier conversation
([[stealth-ox-alpha-model-2026-08]], [[zhipu-glm-5-3-2026-08]]) is being
led by labs that publish weights.

Related: [[industry-open-weights-letter-2026-07]], [[gemma-4]],
[[alibaba-qwen-3-8-27b-2026-08]].
