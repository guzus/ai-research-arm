---
slug: gemini-4-argon
title: Gemini 4 Argon
type: entity
aliases: ["Gemini 4 Argon", "Gemini 4", "gemini-4", "4 Argon", "Gemini 4 Carbon", "Barium-B", "Argon for Robotics"]
tags: [model-release, google-deepmind, frontier-model, fairwind, cyber-defense, pricing]
description: Google's Gemini 4 flagship; Perplexity rolled Argon out to all users, and four Argon agents beat Minecraft in 27h14m.
created_at: 2026-10-01
timestamp: 2026-10-25T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-25", path: research/digest/2026-10-25-digest.md}
  - {title: "ARA daily digest 2026-10-17", path: research/digest/2026-10-17-digest.md}
  - {title: "ARA daily digest 2026-10-16", path: research/digest/2026-10-16-digest.md}
  - {title: "ARA daily digest 2026-10-15", path: research/digest/2026-10-15-digest.md}
  - {title: "ARA daily digest 2026-10-14", path: research/digest/2026-10-14-digest.md}
  - {title: "ARA daily digest 2026-10-10", path: research/digest/2026-10-10-digest.md}
  - {title: "ARA daily digest 2026-10-05", path: research/digest/2026-10-05-digest.md}
  - {title: "ARA model ticket — Gemini app tier changes", path: research/models/tickets/google-gemini-app-tier-changes-2026-10.md}
  - {title: "ARA daily digest 2026-10-02", path: research/digest/2026-10-02-digest.md}
  - {title: "ARA daily digest 2026-10-01", path: research/digest/2026-10-01-digest.md}
  - {title: "ARA model ticket — Gemini 4 post-training", path: research/models/tickets/google-gemini-4-2026-09.md}
---

**Gemini 4 Argon** is [[google]]'s first new-generation frontier model in
more than seven months, succeeding the harvested 3.8 Flash / Live line
([[gemini-3-8-flash]], [[gemini-3-8-live]]). It shipped first to government
and trusted cyber defenders through the Fairwind program that already
gated **3.8 Flash Cyber**. Demis Hassabis said the rollout starts "with
government and trusted cyber defenders." Paid API and Google AI Ultra
access is promised "as soon as possible," with no date. Paying consumer
Gemini-app users still see **3.6**. The September 24–28 ticket that
placed Gemini 4 in post-training, with an early drop "well before
year-end," is now a named artifact rather than a stage claim (Google
DeepMind, The Verge, Ars Technica, TechCrunch, The Decoder, HN 381 pts;
ARA daily digest 2026-10-01).

## Why it matters

- **Gated first, priced like a flagship.** Output limit is **1M tokens**,
  up from 64K. Introductory API card is **$2 / $10 per Mtok**, rising to
  **$4 / $20** after the intro window; cached input is **95% off**. The
  post-intro card matches [[claude-opus-5-5|Opus 5.5]] list. HN commenters
  flagged that jump and the still-on-3.6 consumer app (Google, HN; ARA
  daily digest 2026-10-01).
- **Vendor table claims a sweep.** Google's own charts: DeepSWE v1.1
  **77.9%** (SOTA), AutomationBench **51.3%** (#1), LVBench long-video
  **91.7%**, CWE-bench v1 **68%** (tied first), plus leads on the Vals
  Index, Vals Finance Agent v2, and Harvey's Legal Agent Benchmark
  (**19.6%** vs [[claude-fable-5|Fable 5.1]]'s **6.7%**). Treat as
  first-party until independently reproduced. See [[harvey]] (Google;
  ARA daily digest 2026-10-01).
- **Internal-use claims are specific.** Google says a fleet of Argon
  agents freed more than **300 TiB** of datacenter memory, and that in
  the libgav1 Rust port Argon replaced **32K lines of SIMD** with safe
  Rust that runs **2.7×** faster than the previous port. First-party
  engineering anecdotes, not a public benchmark (Google; ARA daily
  digest 2026-10-01).
- **Independent reads are mixed and token-hungry.** The Decoder's
  testing has Argon matching [[gpt-6|GPT-6 Astra]] and trailing Opus
  5.5, while burning **more than twice as many tokens per task as
  [[astra|Astra]]** — which cuts into the low per-token intro price.
  Artificial Analysis, as relayed, scores Intelligence Index **53**,
  tying Astra; on AA-Omniscience it hallucinates far less than Astra
  (**15% vs 51%**) but also answers correctly less often (**50% vs
  63%**). No third-party reproduction of the vendor DeepSWE / Vals
  sweep landed in today's files (The Decoder, Twitter; ARA daily
  digest 2026-10-01).
- **Fairwind is now a frontier gate, not only a Flash-Cyber pen.**
  3.8 Flash Cyber already sat behind the same ~650-member defender
  program. Putting the generation flagship on that path is Google's
  Daybreak-shaped answer in a week when [[federal-ai-policy]] is
  tracking a voluntary White House accord and a reported FTC probe.
  See [[gemini-3-8-flash]] and [[agentic-ai-security]] (Google DeepMind,
  The Verge; ARA daily digest 2026-10-01).

## Open questions

- **Does the DeepSWE 77.9% / Vals sweep hold** now that paid API
  access is open, or only on Google's launch table? Every's 21%
  refactoring score is the first public contradiction.
- **Does the >2× token burn vs Astra persist** on the GA SKU? If
  it holds, the $2/$10 intro card is not the cheap task price.
- **Is the ~1.9-hour P50 / high eval-awareness read in the safety
  report** real, or a screenshot that does not match the document?
- **What is Argon for Robotics**, and is it a separate checkpoint
  or a serving wrapper?

## Vals #1 and a contested cheap-task claim (2026-10-02)

- **Argon finished the day as HN's #1 story** at **1,632 points /
  1,110 comments**. The debate centred on the gated release and
  whether the **$2/$10 introductory price** is "an accounting
  trick." See [[google]] (Hacker News; ARA daily digest
  2026-10-02).
- **Vals Index #1 at 68.9%** is now the day's independent
  placement, not only a launch-day relay. Artificial Analysis
  says Argon **ties [[astra|GPT-6 Astra]] on the Intelligence
  Index at 60% of the cost per task**; Demis Hassabis amplified
  that result. This **conflicts with The Decoder's earlier
  finding** that Argon burns more than twice as many tokens per
  task as Astra. Treat the cost comparisons as provisional until
  paid API access opens (Vals AI, Artificial Analysis, The
  Decoder; ARA daily digest 2026-10-02).

## Free-app cut as a serving-cost counterpart (2026-10-05)

The same window that left Argon gated behind Fairwind, [[google]]
cut the free Gemini app to
[[gemini-3-6-flash|3.5 Flash-Lite]] from 9 October. The ticket
reads that as capacity coming from somewhere after a gated
frontier rollout — a consumer-tier cut, not an Argon price
change. See [[google]] (The Decoder; ARA daily digest
2026-10-05 and ticket `google-gemini-app-tier-changes-2026-10`).

## Antigravity picker and Carbon leak (2026-10-10)

- **Gemini 4 Argon appeared in
  the Antigravity Insiders
  picker** with **256K, 512K,
  and 900K** context tiers.
  Argon was already a named
  Sept. 30 cybersecurity-partner
  preview; tonight's new facts
  are the picker strings, not
  a public API open. See
  [[google]] (ARA daily digest
  2026-10-10).
- **Business Insider says
  employees are testing a later
  Carbon checkpoint** that some
  of them compare to
  [[claude-opus-5-5|Claude Opus
  5.5]] on coding. That
  comparison is staff feel, not
  a published bench. TestingCatalog
  says BI names **Barium-B** as
  the public Argon cut, which
  implies Carbon is not what
  outside users get first
  (Business Insider,
  TestingCatalog; ARA daily
  digest 2026-10-10).

## General availability (2026-10-14)

- **Argon is now on the paid Gemini
  API, AI Studio, the Gemini app
  (Pro/Ultra), AI Mode in Search,
  and Antigravity**, with up to
  **1M output tokens**. Google
  calls it the first major
  flagship upgrade since Gemini
  3 Pro, aimed at coding,
  enterprise workflows, and cyber
  defense. More than **100,000
  Googlers** tested it. The
  September preview's introductory
  price remains **$2 / $10 per
  Mtok**. There is also an
  **Argon for Robotics** variant.
  Simon Willison's `llm-gemini
  0.35` already supports it. See
  [[google]] (@GoogleDeepMind,
  @OfficialLoganK, @_philschmid,
  The Verge, Ars Technica; ARA
  daily digest 2026-10-14).
- **Independent coding reads
  split.** Every's refactoring
  benchmark scored Argon **21%**
  against **81–85%** for
  [[gpt-6|GPT-6 Astra]], Fable
  5.1, and the Claude 5.5 models.
  @theo calls it "a huge jump
  for Gemini" and reports the
  first perfect Skatebench-private
  score, but also says it was
  the only model above a **50%
  false-claim rate** on his
  codebase-analysis bench. Every
  says Antigravity is "six months
  to a year behind" Claude Code
  and Codex. The launch led HN
  at **899 points / 700
  comments** (@danshipper, @theo,
  Hacker News; ARA daily digest
  2026-10-14).
- **A single-source safety-report
  read is not yet checked
  against the report.** One
  thread says the Argon safety
  report shows much higher
  evaluation awareness than
  Gemini 3.1 Pro, a ~**1.9-hour
  P50** agentic time horizon,
  and repetitive looping. Those
  figures are screenshots, not
  a first-party table
  (@scaling01; ARA daily digest
  2026-10-14).

## Day-two independent benches (2026-10-15)

- **Argon placed 3rd of 35 on
  KernelBench-Mega (27.0×)**,
  behind [[claude-opus-5-5|Opus
  5.5]] (**35.5×**) and
  [[claude-sonnet-5-5|Sonnet
  5.5]] (**32.1×**). @theo says
  it was wrong on over **50%**
  of claims in his own codebase
  tests, repeating yesterday's
  false-claim read. Latent Space
  says most benchmarks, like
  CursorBench, independently
  confirm Google's numbers. HN
  peaked at **1,360 / 963**
  before the story left the
  page. Ethan Mollick said
  Gemini 4 "feels quite
  different" from models that
  seem to distill Claude or GPT.
  See [[google]]
  (@elliotarledge, @theo,
  Latent Space, @emollick; ARA
  daily digest 2026-10-15).

## ARC-AGI-3 harness split (2026-10-16)

- **Arc Prize verified Argon at
  97.5% on ARC-AGI-3** using
  Google's own harness
  (**$4.8K**), and **49.8%** on
  the standard harness. It also
  scores **91.3% on ARC-AGI-2**
  at **$0.32/task**. The
  47.7-point gap is a
  harness-sensitivity result,
  not a second model. See
  [[verification-bottleneck]]
  (@arcprize, @GoogleDeepMind;
  ARA daily digest 2026-10-16).
- **DeepMind is giving 10,000
  scientists six months of free
  top-tier access.** That is a
  distribution move on the same
  day as the bench print, not a
  capability claim
  (@GoogleDeepMind; ARA daily
  digest 2026-10-16).
- **Ethan Mollick repeated that
  Gemini 4 "feels quite
  different"** from models he
  suspects distill Claude or
  GPT — the same day
  [[anthropic]] told investors
  distillation was 5–7% of its
  revenue (@emollick; ARA daily
  digest 2026-10-16).

## Minecraft, Perplexity, StarSkirmish (2026-10-17)

- **Four Argon agents beat
  Minecraft in 27h14m** via
  Mineflayer (text API, Easy
  difficulty, 605 deaths, 2,783
  programs; arXiv 2610.22319).
  That is a long-horizon agent
  demo, not a new SKU. See
  [[google]] (ARA daily digest
  2026-10-17).
- **[[perplexity]] rolled Argon
  out to all users**, citing
  **0.802** on its own WANDR
  benchmark against **0.735**
  for [[astra|GPT-6 Astra]].
  WANDR is a first-party
  Perplexity number, not an
  independent composite (ARA
  daily digest 2026-10-17).
- **On StarSkirmish Bench v0.2**
  (an HN Show), Argon,
  [[claude-opus-5-5|Opus 5.5]]
  and [[claude-fable-5|Fable 5.1]]
  are tied at 37–39
  behind GPT-6 Astra. Treat as
  a small community bench, not
  a ranking (ARA daily digest
  2026-10-17).

## Dream-1 undercut on RoboDojo-RC (2026-10-25)

[[dream-labs|Dream-1]] is
priced at **$3/hour**
($2/hour Flash). An
independent RoboDojo-RC
report puts it **16× cheaper
per attempt** than Argon.
That is a third-party
robotics bench, not a Google
first-party number, and it
does not say Argon lost the
capability comparison — only
the cost-per-attempt one
(Dream Labs, Hacker News;
ARA daily digest
2026-10-25).
