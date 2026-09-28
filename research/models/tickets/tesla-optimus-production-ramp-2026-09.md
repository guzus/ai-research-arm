---
slug: tesla-optimus-production-ramp-2026-09
title: Tesla Optimus production up ~10x to several hundred robots a week, hands still the bottleneck
company: Tesla
model: Optimus
status: confirmed
status_note: |
  **The Information's own handle, posted twice on 2026-09-27 15:30 UTC and
  2026-09-28 13:30 UTC:** "Tesla has increased Optimus production **roughly
  tenfold, reaching several hundred robots a week**. But problems with the robot's
  **intricate hands, automated equipment and suppliers** are complicating its push
  to manufacture Optimus at scale."

  **Both halves are the story, and the second half is the more informative one.**
  A 10x ramp to hundreds per week is a real manufacturing step. Naming the hands
  as the constraint is a specific, falsifiable engineering claim — and it is the
  same constraint Tesla has hit publicly before, because a humanoid hand packs the
  highest actuator and tendon density on the machine into the smallest volume and
  is the part least amenable to automated assembly.

  **Status `confirmed`, verification `partial`.** The outlet published it under its
  own byline and repeated it, which establishes the reporting; there is **no Tesla
  statement, no production figure from the company, and no independent count** in
  this cycle's signal. "Several hundred a week" is a range, and 10x is relative to
  an unstated base.

  **Scale check, because the absolute number is what matters.** Several hundred per
  week annualises to roughly 15,000-25,000 units a year — a pilot line by
  automotive standards and a large number by humanoid-robot standards. This is the
  first tracked instance of any humanoid program reporting weekly output in the
  hundreds.

  **Where it sits against the rest of the humanoid board.** This set tracks
  capability and funding across the category — [[figure-helix-02-2026-05]] (200-hour
  autonomous fleet run), [[agility-digit-5-2026-09]], [[skild-s1-2026-08]] (robot
  foundation model), [[nvidia-sonic-humanoid-model-2026-09]] (whole-body motion
  foundation model), [[unitree-ipo-debut-2026-08]] and
  [[xpeng-dogotix-funding-2026-08]] on the China side, plus
  [[china-humanoid-ipo-curbs-2026-09]] on the policy side. Almost all of that is
  models, demos and capital. This is the first ticket about *units*, which is the
  axis that eventually decides the category.
expected: "Reported ramp in place. Open: a Tesla-stated production figure, whether the hand supply chain is resolved or redesigned, cost per unit, and how many units are deployed externally versus inside Tesla's own factories. Independent counts (VIN-style registrations, teardown supply-chain estimates) would settle the number."
labels:
  - tesla
  - optimus
  - humanoid
  - manufacturing
  - supply-chain
verification: partial
sources:
  - https://x.com/theinformation/status/2104232104473014585
  - https://x.com/theinformation/status/2104564303256834396
created_at: 2026-09-28
updated_at: 2026-09-28
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-28
    change: "Created — The Information, under its own handle on both 2026-09-27 and 2026-09-28, reports Tesla has raised Optimus production roughly tenfold to several hundred robots a week, while problems with the robot's intricate hands, automated equipment and suppliers complicate scaling. Status confirmed on the reporting (own byline, repeated), verification partial — no Tesla statement, no company production figure, no independent count, '10x' relative to an unstated base and 'several hundred' a range. Logged because it is the first ticket in this set about humanoid UNITS rather than models, demos or capital: the rest of the category board ([[figure-helix-02-2026-05]], [[skild-s1-2026-08]], [[nvidia-sonic-humanoid-model-2026-09]], [[unitree-ipo-debut-2026-08]]) is capability and funding. Several hundred a week annualises to roughly 15-25K units/year — a pilot line by automotive standards, the largest humanoid output reported here to date."
---

Two numbers, one specific failure mode. Production up roughly tenfold to several
hundred robots a week; the hands, the automated equipment around them, and the
suppliers behind them are what is in the way.

The hand constraint is the part worth taking seriously, because it is the part that
is mechanically obvious. A humanoid hand concentrates more actuators, tendons and
sensors per cubic centimetre than anything else on the machine, and it is the
component that most resists automated assembly — which is a problem when your
scaling thesis is that you are an automaker who already knows how to build lines.
It is also the component that determines whether the robot can do useful work, so
it cannot be simplified away.

Against the rest of this board, the interesting thing is the axis. Nearly every
other humanoid ticket here is about a model, a demo, or a funding round: Figure's
fleet run, Skild's foundation model, NVIDIA's whole-body motion model, Unitree's
IPO, Dogotix's raise. This one is about units shipped per week, which is
eventually the only number that settles the category.

What is missing is Tesla's own voice. The figure is an outlet's, twice, with no
company confirmation, no base to compare the 10x against, and no split between
robots deployed externally and robots working inside Tesla's own plants — which
is the difference between a product and an internal tool.
