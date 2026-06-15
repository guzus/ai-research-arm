---
eyebrow: ANALYSIS · OPEN-WEIGHT LEGAL AI
title: One day, one open model, the frontier band — what the Harvey × Nemotron experiment actually proves
deck: Harvey and Trajectory post-trained NVIDIA's open-weight Nemotron 3 Ultra onto the closed-frontier band on a legal-agent benchmark in under a day. The result is real, the framing is slippery, and the economics are smaller than the headline.
lede: |
  On 10 June 2026, Harvey — the $11B legal-AI company — and the post-training
  startup Trajectory announced that they had taken NVIDIA's freshly-released
  open-weight Nemotron 3 Ultra from a 0% all-pass rate on Harvey's Legal Agent
  Benchmark to 5.8%, landing it between Anthropic's Sonnet 4.6 and Opus 4.6, "at
  roughly 1/8th to 1/50th the per-token price." It took under 24 hours. The claim
  is mostly true and genuinely important — and it leans on a benchmark where the
  "frontier" itself fails more than 93% of tasks, on a second metric that flatters
  the open model, and on a cost ratio whose top end no provider currently charges.
  This is what the experiment shows, and what it doesn't.
domain: general
stats:
  - {label: All-pass (held-out), value: 5.8%, note: "0% → 5.8% post-training"}
  - {label: Closed flagship, value: 6.6%, note: "Opus 4.6, same subset"}
  - {label: Rubric criteria, value: 83%, note: "vs 85% frontier"}
  - {label: Post-train time, value: "<24h", unit: "", note: "reused Super recipe"}
  - {label: Per-token price, value: "~1/8", note: "verified vs 1/50 claimed"}
---

The viral version of this story is a one-liner: an open model anyone can download
matched closed frontier models on real legal work, in a day, for a fraction of the
cost. Every clause of that sentence is defensible, and every clause is doing more
work than it admits. The experiment is a clean, well-instrumented data point about
where open-weight models sit in mid-2026 — and a case study in how benchmark
framing turns a narrow technical result into a market-shaking headline.

:::callout(kind=info, label="The short answer")
- {accent}The result is real but narrow.{/} Post-trained Nemotron 3 Ultra hit 5.8% all-pass on a held-out slice of Harvey's benchmark, between Sonnet 4.6 (4.2%) and Opus 4.6 (6.6%) on that same slice.[^3]
- {accent}"Frontier" is a low bar here.{/} On Harvey's strict all-pass standard, the best closed model in the world clears about 7% of tasks; the frontier fails >90%.[^4]
- {accent}Two metrics, one headline.{/} The "matches the frontier" claim rides on a *second*, gentler metric — share of rubric criteria passed (83% vs 85%) — not the all-pass rate.[^3]
- {accent}The cost gap is real but oversold.{/} Verified per-token pricing is ~1/6 to ~1/23 cheaper than Sonnet/Opus; the headline's "1/50" is not charged by any provider today.[^20]
- {accent}The method is undisclosed.{/} Neither Harvey nor Trajectory says whether the 24-hour run was SFT, RL, LoRA, or a mix — the single biggest gap in the claim.[^3]
:::

## 01. The claim, stated precisely

Strip the marketing and the announcement makes four distinct factual claims, each
worth separating because they are true to different degrees. First, capability:
post-trained Nemotron 3 Ultra reached a 5.8% all-pass rate on a held-out set of
Harvey's Legal Agent Benchmark (LAB), up from 0% for the untrained base model,
"placing it between Sonnet 4.6 (4.2%) and Opus 4.6 (6.6%)."[^3] Second, reliability:
Harvey described "many held-out tasks" moving from "around ~70% pass rates" before
training "toward ~95% pass rates" after.[^1] Third, cost — and this is the figure to
hold at arm's length — Harvey's tweet claims the open model runs ==at roughly 1/8th to
1/50th the per-token price of Sonnet 4.6 and Opus 4.6==,[^1] an unverified vendor figure
this article checks and partly walks back in Section 05. Fourth,
speed: the whole thing happened "less than 24 hours after Nemotron 3 Ultra launched,
using the same harness, data, and recipe we used for Nemotron 3 Super."[^1]

The section thesis is simple: each claim is anchored to a real primary source — the
Harvey X thread, Trajectory's own field note, and NVIDIA's model card — but the
*headline* fuses them into a stronger statement than any single one supports. The
load-bearing primary document is Trajectory's field note, authored by Jerry Chan and
dated 9 June 2026, one day before the X thread.[^3] That date matters: it tells you
the announcement is a coordinated launch between an application company (Harvey), a
training-platform vendor (Trajectory), and a chip vendor (NVIDIA), each of whom
benefits from the result reading as large.

:::kv
- {term: "Application company", def: "Harvey — owns the LAB benchmark, picks the models"}
- {term: "Training vendor", def: "Trajectory — sells the post-training that produced the gain"}
- {term: "Model / silicon vendor", def: "NVIDIA — ships Nemotron open, sells the GPUs it runs on"}
- {term: "Primary record", def: "Trajectory field note, Jerry Chan, 2026-06-09 [^3]"}
:::

Why does this matter? Because the experiment is being read as an independent
verdict on open-versus-closed economics, and it is nothing of the kind — it is a
three-party product announcement in which all three parties win if you believe it.
That does not make it false. It makes the caveats load-bearing rather than
decorative. The counterpoint to my own skepticism: the underlying artifacts (the
benchmark, the model, the prices) are public, so the claim is checkable in a way
most vendor announcements are not.[^4][^7][^20]

## 02. The benchmark underneath the number

A 5.8% score sounds like a failing grade because, in ordinary terms, it is. The
key to the whole story is what LAB measures and how it scores. Harvey built LAB from
"more than 1,200 agent tasks across 24 legal practice areas," decomposed from real
client matters and graded against "over 75,000 expert-written rubric criteria."[^5]
The headline metric is the {accent}all-pass rate{/}: a task counts as passing "only
if every required rubric criterion passes."[^4] A deal-team memo that catches eight
of ten risks scores zero, not 80%. With dozens of criteria per task, the all-pass
rate is a product of many per-criterion probabilities — it is engineered to sit near
the floor even when a model is individually competent on most criteria.

That design choice is the entire reason "frontier legal performance" can mean ~6%.
On Harvey's own published leaderboard, the best model on earth — Claude Opus 4.7 —
clears 7.1% of tasks end-to-end, and "the frontier models we evaluated complete less
than 10% of tasks end-to-end in aggregate."[^4] Topping that leaderboard "runs to
roughly $50 per task and over 20 minutes of latency."[^4] So when the post-trained
open model lands "between Sonnet 4.6 and Opus 4.6," it is joining a cohort that, by
Harvey's own framing, cannot yet deliver complete legal work product.

:::callout(kind=warn, label="Read this twice")
"Reaching the frontier band" on LAB's all-pass metric means reaching a band where
the frontier itself fails more than nine tasks in ten. The result says the open
model is now {accent}as unable as the closed models{/}, not that either is
production-ready. That is still a meaningful capability statement — it just isn't
the one most readers hear.[^4]
:::

This is where the framing turns. "Matching the frontier" does not actually refer to the
all-pass rate above — on that strict metric the open model trails Opus. It refers to a
*second*, gentler metric: the share of individual rubric criteria a model passes, where
post-trained Ultra reaches 83%, within two points of Sonnet 4.6 and Opus 4.6 at 85%, and
well past the 52% base.[^3]

:::bars
- {label: "Opus 4.6 (closed)", value: 85%, pct: 85}
- {label: "Sonnet 4.6 (closed)", value: 85%, pct: 85}
- {label: "Nemotron 3 Ultra (post-trained)", value: 83%, pct: 83}
- {label: "GPT 5.5 (closed)", value: 78%, pct: 78}
- {label: "Nemotron 3 Ultra (base)", value: 52%, pct: 52}
:::

On this metric the "matches the frontier" claim is fair. But the two metrics tell
different stories — near-parity on criteria-passed, a clear gap on tasks-fully-passed —
and the headline silently picks the friendlier one. A reader who hears "between Sonnet
and Opus" pictures the gentle 83/85 race, not the brutal 5.8/6.6 one.

There is a second subtlety that the announcement quietly relies on. The all-pass
numbers in the Nemotron thread — Sonnet 4.6 at 4.2%, Opus 4.6 at 6.6% — are *not*
the numbers on Harvey's published LAB leaderboard, where Sonnet 4.6 scores 5.4% and
Opus 4.6 scores 4.2%.[^3][^4] They differ because Trajectory evaluated on a *held-out
subset* used for the post-training experiment, not the full 1,200-task benchmark. The
same model scores differently on the two task sets — Opus 4.6 actually *rises* from
4.2% to 6.6%, while Sonnet 4.6 *falls* from 5.4% to 4.2%. The held-out subset is a
legitimate way to test generalization, but it means the viral comparison is not
drawn from the same ruler Harvey published.

On the held-out subset the announcement reports, the all-pass ranking looks like this —
the post-trained open model slots above Sonnet 4.6 and just below Opus 4.6:

:::rank-list
- {label: "Opus 4.6 (closed)", value: 6.6%, pct: 100}
- {label: "Nemotron 3 Ultra (post-trained)", value: 5.8%, pct: 88, highlight: true}
- {label: "Sonnet 4.6 (closed)", value: 4.2%, pct: 64}
- {label: "Nemotron 3 Ultra (base)", value: 0.0%, pct: 1}
:::

The catch is that these are not the numbers on Harvey's published leaderboard. The same
two closed models score differently on the full benchmark versus this held-out slice:

:::slope(left-label="Full LAB", right-label="Held-out subset", unit=%)
| Model      | Full LAB | Held-out subset |
|------------|----------|-----------------|
| Opus 4.6   | 4.2      | 6.6             |
| Sonnet 4.6 | 5.4      | 4.2             |
:::

The chart above is the single most important caveat in the piece: the two evaluations
disagree on which closed model is better, so a 1.6-point gap between the open model
and Opus on the subset should not be over-read. Small absolute numbers on small task
subsets are noisy. The counterpoint, in fairness to Harvey: holding out a test split
is exactly what you *should* do to avoid training on the eval, and Harvey open-sourced
LAB with a runnable harness, so third parties can in principle reproduce the methodology
even if not the exact subset.[^5] Why it matters: the
credibility of "between Sonnet and Opus" depends entirely on which slice you score,
and the announcement reports the most favorable slice without flagging that it differs
from the public leaderboard.

## 03. The model: a genuinely open frontier-class system

The open-weight leg of the story is the strongest. Nemotron 3 Ultra is not a
toy. NVIDIA released it on 4 June 2026 as a 550-billion-parameter Mixture-of-Experts
model with 55 billion active parameters — a hybrid that "interleaves MoE layers with
cheaper Mamba-2 layers" plus a few attention layers, supporting up to a 1-million-token
context window.[^6][^7] NVIDIA's self-reported scores put it at 86.8 on MMLU-Pro and
70.7 on SWE-Bench Verified — genuinely competitive numbers, with the standard caveat
that they are vendor-run on NVIDIA's own evaluation harness, not independently
replicated.[^7]

What makes Ultra unusually important for this story is its license. It ships under
the Linux Foundation's permissive OpenMDW-1.1, which grants rights to "train, modify,
contribute, redistribute and deploy" the model — a materially more permissive grant
than the restrictive NVIDIA house license attached to the smaller Super and Nano
variants.[^7][^9] In other words, within a single model family, the largest model is
the most openly licensed. A law firm or an application vendor can legally download the
weights, fine-tune them, and run them on its own hardware with no per-token rent and
no data leaving its environment. That combination — frontier-class capability plus
unrestricted weights — is the precondition that makes the whole Harvey experiment
possible.

:::kv
- {term: Parameters, def: "550B total · 55B active (MoE)"}
- {term: Architecture, def: "Hybrid Mamba-2 + MoE + attention, Multi-Token Prediction"}
- {term: Context window, def: "Up to 1,000,000 tokens"}
- {term: License, def: "OpenMDW-1.1 (permissive, redistribution + derivative training)"}
- {term: Released, def: "2026-06-04"}
- {term: "NVIDIA-reported", def: "MMLU-Pro 86.8 · SWE-Bench Verified 70.7"}
:::

Note the chronology, because it corrects a piece of the announcement. The Harvey thread
says the work happened "less than 24 hours after Nemotron 3 Ultra launched."[^1] Ultra
launched on 4 June; the field note is dated 9 June.[^6][^3] The reconciliation is that
the *post-training run* reportedly took under 24 hours of wall-clock time on Trajectory's
platform — not that the announcement came within 24 hours of launch.[^3] It is a
defensible reading, but the looser "24 hours after launch" phrasing in the viral tweet
is not literally accurate. The "why this matters": the speed claim is really a claim
about *re-use* — Trajectory says it simply "point[ed] the same harness, data, and recipe
[it] used for Nemotron 3 Super at the new weights, with no new engineering in between."[^3]
The 24 hours is impressive precisely because almost none of it was new work.

:::timeline
- {date: 2025-12-15, headline: "Nemotron 3 family launches", body: "NVIDIA ships the open Nemotron 3 line (Nano first), built on a new hybrid Mamba-2/MoE architecture.[^8]"}
- {date: 2026-03-11, headline: "Nemotron 3 Super (120B-A12B)", body: "The mid-size variant ships under NVIDIA's house open-model license.[^7]"}
- {date: 2026-05-26, headline: "Harvey publishes LAB results", body: "Strict all-pass leaderboard: best frontier model clears 7.1% of tasks.[^4]"}
- {date: 2026-05-29, headline: "Trajectory post-trains Super", body: "First pass of the recipe: trained Super 'matches GPT 5.5,' lifts rubric-pass criteria.[^31]"}
- {date: 2026-06-04, headline: "Nemotron 3 Ultra (550B-A55B)", body: "The flagship ships under the permissive OpenMDW-1.1 license.[^6][^9]"}
- {date: 2026-06-09, headline: "Trajectory publishes Ultra field note", body: "Same recipe, new weights: 0% → 5.8% all-pass, 52% → 83% rubric criteria.[^3]"}
:::

## 04. How you reach the frontier band in a day

The most interesting — and least disclosed — part of the story is the *how*. Neither
Harvey nor Trajectory states the training method: the field note refers only to a
"harness, data, and recipe" and never names SFT, RL, RLVR, LoRA, or a distillation
step.[^3] That silence is the single largest gap in the claim, so the honest move is
to ground the plausibility in the public literature and Trajectory's other
disclosures rather than guess.

Trajectory — a continual-learning startup that raised $15M in May 2026, backed by
Conviction, Bessemer, and Radical with angels including Jeff Dean and Fei-Fei Li[^15] —
has separately described its stack: a reinforcement-learning method it calls
SDPO that "learns from a single trajectory, with no group required," and a training
infrastructure called Continual LoRA that runs "many lightweight adapters at once on one
shared base model," which it claims yields 2.81x experiment throughput.[^16][^17] If — and
it is an *if* — the Harvey run used adapter-based RL on a frozen base, the 24-hour,
large-model turnaround becomes mechanically believable: you are not retraining 550B
parameters, you are fitting small adapters against a verifiable reward.

The academic literature makes the *direction* of the result unsurprising. Reinforcement
learning with verifiable rewards (RLVR) lifted DeepSeek-R1-Zero from 15.6% to 71.0%
pass@1 on AIME 2024 using nothing but a correctness signal.[^21] "Rubrics as Rewards"
extended the same idea to soft domains, using checklist-style rubrics as the reward and
reporting up to ~31% relative gains on HealthBench[^22] — and LAB is, structurally, a
giant rubric. The Tulu 3 recipe scaled RLVR to 405B parameters and reached parity with
closed models like GPT-4o on targeted benchmarks,[^25] and "Tina" showed LoRA-based RL
can add 20-plus points of reasoning for about $9 of compute.[^26] Fast, cheap,
rubric-driven post-training that lifts a model sharply on a verifiable target is exactly
what the field has been demonstrating for eighteen months.

There is a structural reason to expect the gain. A benchmark scored by tens of thousands
of explicit pass/fail criteria is a near-ideal RLVR target: the rubric *is* the reward
function. The same property that makes LAB hard to game with prose makes it easy to
optimize against with reinforcement learning — which is both why the gain is believable
and why the overfitting worry below is serious.[^22]

But plausibility cuts both ways, and the counterpoint is sharp. A widely-cited 2025
study found that RL with verifiable rewards often does *not* expand a model's reasoning
beyond its base: base models match or exceed RL-trained variants at large pass@k, implying
RL mostly reweights paths the model could already find rather than teaching new
capability.[^23] More damning, a separate result showed that *random* rewards —
uncorrelated with correctness — lifted Qwen2.5-Math-7B by 21.4 points on MATH-500, nearly
matching the 29.1-point gain from real rewards, because of an optimization bias in the
GRPO algorithm.[^24] The implication for the Harvey result is uncomfortable: a large
benchmark jump is *consistent with* genuine skill acquisition and with the model learning
the shape of the rubric, and the benchmark number alone cannot distinguish them. Why this
matters: without the method, the data size, or an out-of-distribution test, "0% → 5.8%"
is a strong marketing number and a weak scientific one.

## 05. The economics: per-token is not per-task

The cost claim is where the headline most outruns the evidence, and it is worth doing
the arithmetic. Anthropic lists Sonnet 4.6 at $3 per million input tokens and $15 output;
Opus 4.6 at $5 input and $25 output.[^11][^10] Nemotron 3 Ultra, served on third-party
infrastructure, runs roughly $0.37–$0.50 per million input tokens and $1.08–$2.50
output across providers.[^20] Work the ratios and the open model is about 6x cheaper than
Sonnet and 10x cheaper than Opus at a mid-tier provider, widening to roughly 1/8 to 1/23
at the cheapest provider against Opus's output price.

:::compare
- {role: LOWEST, name: "Nemotron 3 Ultra (3rd-party)", value: $2.50}
- {role: HIGHEST, name: "Opus 4.6", value: $25.00}
- {role: SUBJECT, name: "Nemotron 3 Ultra", value: $2.50}
:::

So the bottom of the claimed range (1/8) holds comfortably; the top (1/50) does not —
no current provider charges a per-token rate that deep, and the deepest verified ratio
is about 1/23.[^20] Trajectory's own field note is, to its credit, more conservative
than the Harvey tweet: it says "at least 10x cheaper to run," which the pricing data
supports.[^3] The "1/50" appears to be the Harvey thread reaching for the widest
defensible spread.

The deeper problem is the unit. {accent}Per-token price is not per-task cost.{/} A
thread reply asked exactly this — "did per token savings translate to task savings?" —
and it went unanswered.[^1] Agentic legal tasks are multi-turn and output-heavy; if the
open model emits more reasoning tokens to reach the same answer, the realized per-task
saving shrinks below the per-token ratio. Harvey's own data is the cautionary tale:
even the closed frontier costs about $50 and 20-plus minutes *per task* on LAB.[^4] None
of the published material reports the post-trained model's per-task token consumption,
so the per-task economics remain genuinely unknown.

:::callout(kind=danger, label="The hidden cost line")
A 550B model is not free to run just because the weights are. Self-hosting needs
multi-GPU clusters and engineering; the per-token win only materializes at sustained
high utilization. The escape hatch — and it is real — is that third-party serverless
prices already bundle that GPU cost into the per-token rate, so a buyer on DeepInfra or
Fireworks captures the savings without owning a single GPU. The total-cost-of-ownership
caveat bites hardest for those who self-host specifically to fine-tune and control the
model.[^20]
:::

This is the part of the story that genuinely matters for a company like Harvey, and
it explains why an application vendor — not a model lab — drove the experiment. Harvey
raised $200M in March 2026 at an $11B valuation, serves 1,300-plus organizations and
100,000-plus lawyers, and runs on roughly $300M of ARR — and it pays its model
inference as a cost of goods it does not control.[^12][^14] It already scrapped its own
proprietary legal model and now routes across Anthropic, OpenAI, Google, and Mistral
per task.[^13] Open weights also buy the one thing a closed API structurally cannot:
the ability to run the model inside a law firm's own environment, with privileged
documents never leaving it — the on-premise, data-residency wedge that BigLaw
procurement cares about most.[^32] An open-weight model that reaches the same band at a
fraction of the inference cost is, for Harvey, a margin lever, a privacy story, and a
negotiating chip against its closed suppliers — regardless of whether open "wins" the
broader race.

## 06. The competitive read: who should actually be nervous

The triumphalist reading — open weights are eating the closed frontier in vertical
markets — is half right. By H1 2026, open-weight models had reached parity with closed
frontier systems on code and competitive-math benchmarks.[^30] NVIDIA is actively pushing
this: it ships Nemotron open precisely because, as Jensen Huang frames it, "this ecosystem
needs open models" — open weights commoditize the model layer and sell the GPUs that
layer runs on.[^29][^8] When the chip vendor's strategy is to make models cheap and
abundant, the application layer is the winner and the closed model labs face structural
margin pressure in any domain where "good enough plus cheap plus controllable" beats "best
plus expensive plus rented."

:::statement(attr="ARA Research")
The party with the most to gain from open-weight legal agents is not the open-model lab
or the law firm — it is the application company that no longer has to rent its
intelligence.
:::

But the counter-case is stronger than the headline allows, and it splits into three
parts. First, the gap that remains is exactly the wrong gap for legal work: by one open-weight
retrospective's tally, open models still trail closed frontier on factual retrieval (a
~17.7-point SimpleQA gap) and on 1-million-token long-context recall (a ~9.4-point MRCR
gap) — the two capabilities that matter most when an agent has to read a data room and
cite it correctly.[^30] (That figure rests on a single secondary source and should be
read as indicative, not precise.) Second,
absolute performance is unsolved: matching a frontier that completes under 10% of tasks
is not a product, and the firm that ships the first model to clear, say, 40% all-pass
will reset the board regardless of whether it is open or closed.[^4] Third, the result
is self-administered — Harvey owns the benchmark, Trajectory sells the training, and no
independent party has reproduced the specific run.[^19]

There is also a quieter structural point: LAB is being post-trained by *multiple*
vendors with *different* recipes. Harvey's own writeup with Baseten Research used
Iterative SFT plus GRPO on Qwen3.5, not Trajectory's stack on Nemotron.[^18] That is bad
news for any single "open model X beat closed model Y" narrative and good news for
Harvey: the benchmark is becoming a neutral procurement ground where many suppliers
compete to specialize whatever base model Harvey points them at. The application company
benefits from the competition no matter which base or vendor wins.

## 07. What would break the thesis

The strongest version of the bullish thesis is: "domain-specific post-training of open
weights now reaches closed-frontier quality on real professional work, cheaply and
fast." Here is what would falsify it, in descending order of how much it would hurt.

:::callout(kind=warn, label="Falsification checklist")
- {accent}Generalization failure.{/} If the held-out gains do not transfer to fresh,
  out-of-distribution legal tasks, the result is benchmark overfitting, not capability.
  The RLVR literature shows this failure mode is real and common.[^23][^24]
- {accent}The metric switch.{/} If you hold to the strict all-pass rate, the open model
  (5.8%) sits *below* Opus 4.6 (6.6%) on the very subset cited; "matches the frontier"
  only survives by switching to the gentler rubric-criteria metric (83% vs 85%).[^3]
- {accent}Per-task cost.{/} If the open model burns more tokens per task, the per-token
  price advantage compresses; no per-task figure has been published.[^1][^4]
- {accent}Independent reproduction.{/} The run is self-administered by three commercially
  interested parties; no neutral third party has reproduced it.[^19]
:::

Each of these is a live risk, not a rhetorical hedge. The generalization worry is the
deepest, and software engineering is the cautionary precedent: open agents went from near
zero to the frontier band on SWE-bench in barely two years,[^27] only for the field to
discover that frozen issue-resolving benchmarks "introduce risks of overfitting and data
contamination," forcing a continuously-updated successor.[^28] A benchmark scored by an
explicit rubric is the easiest possible thing for RL to overfit, and the published academic
work specifically warns that large verifiable-reward gains can reflect path-reweighting or
optimization artifacts rather than new skill.[^23][^24]
The honest synthesis is that the experiment proves *feasibility* — you can move an open
model sharply on a hard legal rubric in a day — without yet proving *durability* or
*real-world transfer*.

It is worth saying what survived scrutiny. An adversarial pass that tried to falsify the
three load-bearing claims — the 5.8% held-out result, the verified cost gap, and the
open-weight 550B/55B OpenMDW-1.1 model — found no contradicting primary source for any of
them across roughly nine distinct searches: 3 of 3 top claims unbroken. The facts are
solid; it is the *framing* layered on top of them that this piece contests.

To Harvey and Trajectory's credit, the artifacts that would let a skeptic check all of
this are unusually public: the benchmark is open-source,[^5] the model weights are
downloadable,[^7] and the prices are listed.[^20] That is more falsifiable than the
typical AI launch, and the right posture is neither the viral celebration nor reflexive
dismissal. It is this: a genuine, checkable demonstration that the open-weight layer has
become a credible substrate for specialized professional agents — wrapped in a headline
that borrows certainty the underlying numbers have not yet earned.

:::callout(kind=success, label="Net assessment")
Believe the structural claim: open weights plus cheap rubric-based post-training are now
a real competitive substrate for vertical AI, and the application layer is the
beneficiary. Discount the specific superlatives: "matches the frontier," "1/50th the
cost," and "24 hours after launch" are each true only under the most generous available
reading.
:::

:::references
- {id: 1, title: "We partnered with Trajectory to post-train Nemotron 3 Ultra for legal (X thread)", url: "https://x.com/harvey/status/2064757424540749879", source: "Harvey / X", date: "2026-06-10"}
- {id: 2, title: "We post-trained Nemotron 3 Ultra on Harvey Legal Agent Bench in under 24 hours (X)", url: "https://x.com/trajectorylabs/status/2064756005507072339", source: "Trajectory / X", date: "2026-06-10"}
- {id: 3, title: "Post-Training NVIDIA Nemotron 3 Ultra on Harvey LAB in Under 24 Hours (field note)", url: "https://trajectory.ai/field-notes/harvey-nemotron-3-ultra", source: "Trajectory (Jerry Chan)", date: "2026-06-09"}
- {id: 4, title: "Legal Agent Benchmark: Initial Results", url: "https://www.harvey.ai/blog/legal-agent-benchmark-initial-results", source: "Harvey", date: "2026-05-26"}
- {id: 5, title: "Introducing Harvey's Legal Agent Benchmark", url: "https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark", source: "Harvey", date: "2026-05-06"}
- {id: 6, title: "NVIDIA Nemotron 3 Ultra powers faster, more efficient reasoning for long-running agents", url: "https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-powers-faster-more-efficient-reasoning-for-long-running-agents/", source: "NVIDIA Developer", date: "2026-06-04"}
- {id: 7, title: "NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16 model card", url: "https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16", source: "Hugging Face / NVIDIA", date: "2026-06-04"}
- {id: 8, title: "NVIDIA debuts Nemotron 3 family of open models", url: "https://nvidianews.nvidia.com/news/nvidia-debuts-nemotron-3-family-of-open-models", source: "NVIDIA Newsroom", date: "2025-12-15"}
- {id: 9, title: "Linux Foundation releases OpenMDW 1.1; NVIDIA adopts OpenMDW for Nemotron", url: "https://www.linuxfoundation.org/press/linux-foundation-releases-openmdw-1.1-nvidia-adopts-openmdw-for-cosmos-isaac-gr00t-ising-and-nemotron-ai-model-families", source: "Linux Foundation", date: "2026-05-28"}
- {id: 10, title: "Claude Opus 4.6", url: "https://www.anthropic.com/news/claude-opus-4-6", source: "Anthropic", date: "2026-02-05"}
- {id: 11, title: "Claude Sonnet 4.6", url: "https://www.anthropic.com/news/claude-sonnet-4-6", source: "Anthropic", date: "2026-02-17"}
- {id: 12, title: "Harvey raises at $11B valuation to scale agents across law firms and enterprises", url: "https://www.harvey.ai/blog/harvey-raises-at-dollar11-billion-valuation-to-scale-agents-across-law-firms-and-enterprises", source: "Harvey", date: "2026-03-25"}
- {id: 13, title: "Expanding Harvey's Model Offerings", url: "https://www.harvey.ai/blog/expanding-harveys-model-offerings", source: "Harvey", date: "2025-05-13"}
- {id: 14, title: "Harvey company research (ARR, valuation history)", url: "https://sacra.com/c/harvey/", source: "Sacra", date: "2026-05-01"}
- {id: 15, title: "Trajectory raises $15M to build a platform for continual learning", url: "https://pulse2.com/trajectory-raises-15-million-to-build-a-platform-for-continual-learning/", source: "Pulse 2.0", date: "2026-05-31"}
- {id: 16, title: "SDPO: learning from a single trajectory on agentic tasks (X)", url: "https://x.com/trajectorylabs/status/2061888175916941548", source: "Trajectory / X", date: "2026-06-02"}
- {id: 17, title: "Continual LoRA (C-LoRA): many adapters on one shared base (X)", url: "https://x.com/trajectorylabs/status/2060769967164056037", source: "Trajectory / X", date: "2026-05-30"}
- {id: 18, title: "Post-training open legal agents with Baseten Research", url: "https://www.harvey.ai/blog/post-training-open-legal-agents-with-baseten-research", source: "Harvey", date: "2026-05-19"}
- {id: 19, title: "Rapid post-training of open-weight models for legal AI applications", url: "https://www.zenml.io/llmops-database/rapid-post-training-of-open-weight-models-for-legal-ai-applications", source: "ZenML LLMOps Database", date: "2026-06-11"}
- {id: 20, title: "Nemotron 3 Ultra 550B-A55B — provider pricing", url: "https://artificialanalysis.ai/models/nvidia-nemotron-3-ultra-550b-a55b/providers", source: "Artificial Analysis", date: "2026-06-15"}
- {id: 21, title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL", url: "https://arxiv.org/abs/2501.12948", source: "arXiv", date: "2025-01-22"}
- {id: 22, title: "Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains", url: "https://arxiv.org/abs/2507.17746", source: "arXiv", date: "2025-07-23"}
- {id: 23, title: "Does Reinforcement Learning Really Incentivize Reasoning Beyond the Base Model?", url: "https://arxiv.org/abs/2504.13837", source: "arXiv (NeurIPS 2025)", date: "2025-04-18"}
- {id: 24, title: "Spurious Rewards: Rethinking Training Signals in RLVR", url: "https://arxiv.org/abs/2506.10947", source: "arXiv", date: "2025-06-12"}
- {id: 25, title: "Tulu 3: Pushing Frontiers in Open Language Model Post-Training", url: "https://arxiv.org/abs/2411.15124", source: "arXiv (AI2)", date: "2024-11-22"}
- {id: 26, title: "Tina: Tiny Reasoning Models via LoRA", url: "https://arxiv.org/abs/2504.15777", source: "arXiv", date: "2025-04-22"}
- {id: 27, title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", url: "https://arxiv.org/abs/2310.06770", source: "arXiv", date: "2023-10-10"}
- {id: 28, title: "SWE-bench-Live: continuously-updated software-agent benchmark", url: "https://arxiv.org/abs/2505.23419", source: "arXiv", date: "2025-05-29"}
- {id: 29, title: "Jensen Huang interview", url: "https://www.dwarkesh.com/p/jensen-huang", source: "Dwarkesh Patel", date: "2026-06-01"}
- {id: 30, title: "Open-weight models H1 2026 retrospective", url: "https://www.digitalapplied.com/blog/open-weight-models-h1-2026-retrospective-deepseek-qwen-llama", source: "Digital Applied", date: "2026-06-01"}
- {id: 31, title: "Post-trained Nemotron 3 Super approaches the closed frontier (X)", url: "https://x.com/trajectorylabs/status/2060407704699772984", source: "Trajectory / X", date: "2026-05-29"}
- {id: 32, title: "Harvey's multi-model bet and Mistral open-weight on-prem", url: "https://www.shashi.co/2026/05/harveys-multi-model-bet-gives-mistral.html", source: "Shashi", date: "2026-05-01"}
:::
