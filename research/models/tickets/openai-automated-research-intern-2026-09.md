---
slug: openai-automated-research-intern-2026-09
title: OpenAI declares its "automated research intern" milestone reached, targets a fully autonomous AI researcher by March 2028
company: OpenAI
model: null
status: confirmed
status_note: |
  OpenAI published internal data on 2026-09-06 claiming it has reached its
  **"automated research intern"** milestone — a human-supervised system able to
  complete well-defined research tasks that would take a skilled researcher
  several days — and says it is on track for a **fully autonomous AI researcher
  in 18 months, i.e. March 2028**. @sama amplified the accompanying post from
  Chief Scientist **Jakub Pachocki**.

  The published numbers, as relayed by @AndrewCurran_, @mark_k, @rohanpaul_ai
  and @WesRoth: as of mid-August the research organization used **3.1
  agent-workdays of effort for every workday of human labor** (a runtime ratio,
  not a productivity-equivalence claim); the **median** OpenAI researcher spent
  **>$600/day** of coding-agent inference at API prices and the **90th
  percentile >$7,000/day**; experiments per active researcher hit an all-time
  high in August. @scaling01's read of the same charts puts Astra broadly
  available to employees between **2026-07-12 and 07-26** — median spend +87%,
  p90 +169%, researcher output-token usage +33%, agent runtime +33% — and
  computes an internal P50 time-horizon increase of **6.18x since January 2026**,
  implying a **2.18-2.28 month doubling time** (95% CI 1.46-5.23 months) with
  the trend visibly slowing in March and June an outlier. Reliability is the
  honest counterweight OpenAI published itself: success without human
  intervention falls from **86% on sub-15-minute tasks to ~16% on the 64-128
  hour bucket**.

  Pachocki's own framing is not a victory lap. Quoted by @AndrewCurran_:
  "Currently I believe that **no lab has solved alignment and monitoring to a
  sufficient degree to continue responsibly scaling at maximum speed for much
  longer**. I expect and hope for **voluntary slowdowns** to become commonplace
  until shared safety bars are established. And I believe that **international
  coordination** on future AI development needs to become a top priority for
  governments around the world." He also says AI is "grown more than designed,"
  that its study is largely an experimental science, and — per @kimmonismus —
  that evaluations show **declining reliability of chain-of-thought
  monitoring** even as he expects progress to continue into recursive
  self-improvement.

  Tracked separately from [[openai-frontier-rl-pause-2026-08]], which this
  disclosure corroborates: the same charts show Astra-related RL compute
  dropping after the 2026-07-20 safety-infrastructure pause and again after
  Astra-class restrictions on 2026-08-06/07.
expected: "Stated target: fully autonomous AI researcher by ~March 2028. Near-term watchables: whether the 3.1:1 agent-to-human runtime ratio keeps climbing, whether the P50 time-horizon doubling time holds near ~2.2 months, and whether Pachocki's call for voluntary slowdowns and international coordination produces anything concrete."
labels:
  - openai
  - recursive-self-improvement
  - safety
  - research-automation
verification: confirmed
sources:
  - https://x.com/sama/status/2096647371983880383
  - https://x.com/AndrewCurran_/status/2096629434732388687
  - https://x.com/AndrewCurran_/status/2096638237439901985
  - "@kimmonismus"
  - "@scaling01"
  - "@rohanpaul_ai"
  - "@WesRoth"
  - "@mark_k"
created_at: 2026-09-07
updated_at: 2026-09-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-07
    change: "Created — CONFIRMED. On 2026-09-06 OpenAI published internal data claiming it reached its 'automated research intern' milestone (a human-supervised system completing well-defined research tasks that would take a skilled researcher several days) and says it is on track for a fully autonomous AI researcher in 18 months, ~March 2028; @sama amplified the accompanying post by Chief Scientist Jakub Pachocki. Published figures: 3.1 agent-workdays of effort per human workday as of mid-August (runtime, not productivity equivalence); median researcher >$600/day of coding-agent inference at API prices, 90th percentile >$7,000/day; experiments per active researcher at an all-time high in August; and the counterweight OpenAI published itself — success without human intervention falls from 86% on sub-15-minute tasks to ~16% on the 64-128 hour bucket. @scaling01 reads the charts as showing Astra broadly available to employees 2026-07-12..07-26 (median spend +87%, p90 +169%, output tokens +33%, agent runtime +33%) and computes internal P50 time-horizon up 6.18x since January 2026, a 2.18-2.28 month doubling time with a 1.46-5.23 month 95% CI. Pachocki on the record: no lab has solved alignment and monitoring well enough to keep scaling at maximum speed much longer, he expects and hopes for voluntary slowdowns until shared safety bars exist, international coordination should be a top government priority, AI is 'grown more than designed', and per @kimmonismus evaluations show declining reliability of chain-of-thought monitoring. Verification confirmed (OpenAI's own publication). Corroborates [[openai-frontier-rl-pause-2026-08]]."
---

Two claims are being made here and they need separating, because the reporting
merged them.

The measurable one is a ratio: 3.1 agent-workdays of runtime per human workday,
median researcher spend above $600/day and p90 above $7,000/day. OpenAI is
explicit that this measures *runtime*, not productivity equivalence, and the
reliability curve it published alongside undercuts any stronger reading —
86% unassisted success on sub-15-minute tasks collapsing to ~16% on 64-128 hour
tasks. An agent that is extremely capable locally and unreliable over a long
trajectory is a real result, but it is not an autonomous researcher.

The unmeasurable one is the trajectory: a fully autonomous AI researcher by
March 2028, extrapolated from an internal time-horizon doubling of roughly 2.2
months. @scaling01's own fit — the number the extrapolation rests on — puts the
95% confidence interval at 1.46 to 5.23 months, notes the trend slowing in
March, and flags June as an outlier. That is a wide enough band that the 18-month
date is a choice, not a projection.

What makes the disclosure unusual is that OpenAI's Chief Scientist paired it
with an argument against his own employer's incentives: no lab has solved
alignment and monitoring well enough to keep scaling at maximum speed, voluntary
slowdowns should become commonplace, and international coordination should be a
government priority — while separately reporting that chain-of-thought
monitoring is getting *less* reliable. Read against Anthropic's Hacker-Opus
research ([[openai-unreleased-containment-escape-2026-07]]) published five days
earlier, two frontier labs spent the same week publishing evidence that their
own oversight mechanisms are degrading.

The compute data also settles an August argument on
[[openai-frontier-rl-pause-2026-08]]: the RL pause was about Astra, and it shows
up as a dent in the charts.
