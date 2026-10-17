---
eyebrow: Model Economics · DeepSeek V4.1-Flash-1017
title: "DeepSeek's $0.15 Flash vs Opus 5: cost-per-task dominance on DeepSWE, no parity on Terminal-Bench"
deck: "DeepSeek's 1017 checkpoint isn't at parity with Opus 5 on cost. If its own numbers hold, it is 20–60× cheaper per task. What is unproven is capability parity. Its scores are self-reported, the DeepSWE \"lead\" sits inside the error bars, Terminal-Bench shows a 9.5-point deficit, and the comparator was superseded in September."
domain: general
lede: |
  On October 17, 2026, DeepSeek pushed a checkpoint it called "a minor update" to its Flash endpoint. Its own table puts the model at 77.0 on DeepSWE v1.1 and 42.3 on Terminal-Bench 4.0, against 74.0 and 51.8 for Claude Opus 5, at an advertised $0.15 per million input tokens. Reposts collapsed this into a story of Opus 5 parity at a thirtieth of the price. Taken apart from first principles, the claim splits in two. The cost half is understated: on the one benchmark where the scores tie, DeepSeek's own chart implies about a 60× cheaper task. The capability half is overstated: it rests on self-reported runs, a best-of harness, a confidence interval wider than the lead, and a comparator Anthropic marked legacy four weeks ago.
stats:
  - {label: DeepSWE v1.1 (self-reported), value: "77.0", note: "vs Opus 5 74.0 ±4 (Datacurve)"}
  - {label: Terminal-Bench 4.0, value: "42.3", note: "vs Opus 5 51.8 · Opus 5.5 66.4"}
  - {label: Cost per DeepSWE task, value: "$0.195", note: "DeepSeek chart · Opus 5 $11.84"}
  - {label: Input price, value: "$0.15", unit: "/M", note: "off-peak, cache miss · $0.30 peak"}
---

:::kv
- {term: "Short answer", def: "Half. Cost-per-task parity is the wrong frame: on DeepSWE, 1017 claims a tie at roughly 1/60th the per-task cost of Opus 5. Capability parity holds only on scaffold-matched, contained repo tasks, and even there it is a statistical tie, not a lead."}
- {term: "Where it holds", def: "DeepSWE v1.1: 77.0 vs Opus 5's 74% ±4 on the independent leaderboard. The gap is smaller than one task-sampling standard error (~4 points on 113 tasks)."}
- {term: "Where it fails", def: "Terminal-Bench 4.0: 42.3 vs 51.8 for Opus 5 and 66.4 for Opus 5.5. Long-horizon terminal work is exactly where a cheap model's retries cost the most."}
- {term: "What is unverified", def: "Everything. As of 2026-10-17 neither the Datacurve DeepSWE board nor Artificial Analysis listed a 1017 score[^6,15]. DeepSeek's past agentic self-reports ran 3–10 points above independent re-runs[^31,32,34]."}
- {term: "Wrong comparator", def: "Opus 5 has been 'legacy' since Opus 5.5 shipped on 2026-09-22 at $4/$20 with Terminal-Bench 66.4. Against the current flagship, the capability gap widens and the price gap narrows by ~20%[^10,12]."}
:::

## 1. What "cost-per-task parity" actually requires

The phrase hides three separate claims, and each one has to hold for parity to mean anything to a buyer. In plain terms, the cost of one finished task is three things multiplied together: how many tokens one attempt uses, the price of those tokens, and how many attempts it takes to succeed. Parity therefore needs equal capability on the tasks you actually run, a known price per token, and a known token count per task. DeepSeek's release supplies the first only as self-reported benchmark scores, the second as a price table with a 2× peak multiplier, and the third not at all: the release says the model "reduces task execution time and output length" without giving a single percentage[^1,2].

The price input is the most concrete. DeepSeek's pricing page lists `deepseek-flash`, now served by "DeepSeek-V4.1-Flash-1017", at $0.15 per million cache-miss input tokens and $0.60 per million output tokens off-peak, doubling to $0.30 and $1.20 at peak[^3]. Cache hits cost $0.003 off-peak[^3]. The 1017 changelog says "the API calling method and pricing remain unchanged," so the price cut happened with the September V4.1-Flash release, not today[^4]. Claude Opus 5 lists at $5 input and $25 output, with cache reads at $0.50; Opus 5.5 lists at $4 and $20, with cache reads at $0.20[^12,10].

:::stats
- {label: "Input price ratio (Opus 5 ÷ 1017, off-peak)", value: "33×", note: "$5 vs $0.15"}
- {label: "Output price ratio", value: "42×", note: "$25 vs $0.60"}
- {label: "Cache-read price ratio", value: "167×", note: "$0.50 vs $0.003"}
- {label: "Peak-hour input ratio", value: "17×", note: "$5 vs $0.30"}
:::

The three inputs fail in different ways. The capability input is the one the parity framing asserts and cannot yet support. The price input is real but varies 2× by the hour. The token input is missing from DeepSeek's text and appears only as a per-task dollar figure in a vendor chart. That is why this analysis treats "cost per task" as the output to be checked, not the starting premise.

:::callout(kind=warn, label="Premise check")
"Parity" implies the two models are roughly interchangeable at similar cost. The numbers say something different: if DeepSeek's figures hold, 1017 is one to two orders of magnitude cheaper per task on contained coding work, and measurably *weaker* on long-horizon terminal work. That is a routing decision, not a substitution.
:::

## 2. What DeepSeek actually published, and what it left out

The headline numbers are real in the narrow sense: they appear on DeepSeek's own Hugging Face model card, under an MIT license, with a 1M-token context window[^1]. The card's 11-row table compares 1017 against the September V4.1-Flash, Kimi K3, GLM-5.3, GPT-5.6 Sol and Opus 5[^1]. The release was preceded by a silent swap. In the early UTC hours of October 17, @teortaxesTex reported that the endpoint's `system_fingerprint` had changed, and identified the new value as the MD5 of a build string naming `dsv41f_1017` with an FP8 KV cache[^24]. The official note followed hours later, and the benchmark and pricing rows spread quickly through reposts such as @kimmonismus's[^2,42].

| Benchmark | 1017 | V4.1-Flash (Sep) | GPT-5.6 Sol | Opus 5 |
|---|---|---|---|---|
| *DeepSWE v1.1 | 77.0 | 74.2 | 73.0 | 74.0 |
| *Terminal-Bench 4.0 | 42.3 | 31.2 | 39.9 | 51.8 |
| Automation-Bench v1.0.6 | 60.5 | 54.8 | 45.8 | 50.3 |
| ProgramBench | 29.1 | 20.3 | 23.0 | 37.0 |
| NL2Repo-Bench | 68.2 | 65.4 | 56.8 | 75.3 |
| HLE (no tools) | 42.6 | 36.8 | 44.5 | 56.3 |

:::source
DeepSeek-V4.1-Flash-1017 model card, Hugging Face, 2026-10-17[^1]. All six columns are DeepSeek's table; competitor provenance is not stated.
:::

The table is more interesting for what it concedes than for what it claims. Opus 5 leads 1017 on four of the six rows shown: Terminal-Bench, ProgramBench by 7.9 points, NL2Repo-Bench by 7.1, and Humanity's Last Exam by 13.7[^1]. "Parity with Opus 5" is a reading of one or two rows, not the table.

The methodology is thinner than the September card's. The 1017 card carries a single substantive footnote: "We use the Claude Code harness for Terminal-Bench 4.0 and the Mini-SWE-V2 harness for DeepSWE v1.1"[^1]. It gives no effort level, no number of samples, and no pass@k definition. By contrast, the September V4.1-Flash card said all results "use the maximum effort setting (`reasoning_effort=100`)" with "N=8 samples per task on DeepSWE v1.1"[^5]. Metadata embedded in DeepSeek's cost chart on the release page appears to label the 1017 points "training curve, eval step 196." If that reading is right, they are a snapshot from a training run, not a frozen-release evaluation[^2].

One comparison cell does not reconcile with any published figure. DeepSeek lists Opus 5 at 50.3 on Automation-Bench v1.0.6[^1]. Anthropic's own September launch post reports Opus 5 at 26.9% on AutomationBench, sourced from "Zapier's public leaderboard"[^10]. Zapier's live board shows even Opus 5.5 at Max below 43%[^39]. The 50.3 may be a DeepSeek re-run under a different scaffold, or a different subset. Either way, it is not the public number, and it makes 1017's Automation-Bench "win" non-comparable.

Why this matters: when a vendor's table mixes leaderboard-sourced baselines (DeepSWE, Terminal-Bench) with apparently self-run ones (Automation-Bench), every head-to-head cell needs its provenance checked before it can carry a parity claim.

## 3. DeepSWE: a statistical tie, bought at roughly one-sixtieth the price

On DeepSWE, the capability half of the claim survives, but only as a tie. DeepSWE v1.1 is maintained by Datacurve: 113 from-scratch tasks across 91 repositories in five languages, scored pass@1, with "all models run on mini-swe-agent for consistency"[^6,7,9]. Datacurve chose a single standard harness after a pilot in which mini-swe-agent "matches or beats every native harness at comparable token cost"[^8]. Its leaderboard, last updated September 22, puts Claude Opus 5 at max effort at **74% ±4%**, tied with GPT-6 Astra and Gemini 3.8 Flash at the top[^6].

:::rank-list
- {label: "DeepSeek V4.1-Flash-1017 (max, self-reported, mini-swe-v2)", value: "77.0", pct: 100, highlight: true}
- {label: "GPT-6 Astra (xhigh)", value: "74% ±3", pct: 96}
- {label: "Gemini 3.8 Flash (high)", value: "74% ±1", pct: 96}
- {label: "Claude Opus 5 (max)", value: "74% ±4", pct: 96}
- {label: "GPT-5.6 Sol (max)", value: "73% ±3", pct: 95}
- {label: "Claude Fable 5 (xhigh)", value: "70% ±3", pct: 91}
- {label: "GLM-5.3 (max)", value: "69% ±3", pct: 90}
- {label: "GPT-5.6 Luna (max)", value: "67% ±4", pct: 87}
:::

:::note
Datacurve DeepSWE v1.1 leaderboard as of 2026-09-22[^6]; the 1017 row is DeepSeek's self-report[^1] inserted for comparison and is not on the independent board.
:::

The 3-point lead is noise. With 113 tasks and a pass rate near 75%, one task is worth about 0.9 points, and the task-sampling standard error of a single run is about 4.1 points. Datacurve's own ±4 band on Opus 5 is already wider than the gap[^6]. The harness also differs: 1017 ran on "Mini-SWE-V2"[^1], while Datacurve uses mini-swe-agent[^6]. In September DeepSeek showed how much the harness matters for its own model: the same V4.1-Flash checkpoint scored 74.2 on mini-SWE and 65.5 on OpenCode, an 8.7-point spread across eight scaffolds[^5]. DeepSeek's headline is its best scaffold.

The cost side is where the claim is understated. Datacurve measured Opus 5 at max effort at **$11.84 per task**[^6]. DeepSeek's release chart puts 1017 at max effort at about $0.20 per DeepSWE task (a chart reading of $0.195), down from about $0.50 for the September Flash. The Decoder read the same chart the same way[^2,20].

:::bars
- {label: "Claude Opus 5 (max) — Datacurve", value: "$11.84", pct: 100}
- {label: "Claude Fable 5 (xhigh) — Datacurve", value: "$13.41", pct: 100}
- {label: "GPT-6 Astra (xhigh) — Datacurve", value: "$4.43", pct: 37}
- {label: "Gemini 3.8 Flash (high) — Datacurve", value: "$2.36", pct: 20}
- {label: "GPT-5.6 Luna (max) — Datacurve", value: "$0.61", pct: 5}
- {label: "V4.1-Flash Sep (max) — DeepSeek chart", value: "$0.495", pct: 4}
- {label: "V4.1-Flash-1017 (max) — DeepSeek chart", value: "$0.195", pct: 2}
:::

:::source
Average cost per DeepSWE v1.1 task. Datacurve leaderboard 2026-09-22[^6]; DeepSeek figures from the vendor's 1017 perf-vs-cost chart[^2], corroborated by The Decoder[^20]. Bars capped at the Opus 5 value.
:::

Taking both sources at face value, Opus 5 costs about 61× more per DeepSWE attempt. Dividing each cost by its pass rate, the gap per *solved* task is about 63×. The comparison also says something about Opus 5 that the parity framing misses. Gemini 3.8 Flash already matched Opus 5's 74% at $2.36, a fifth of the cost, before DeepSeek shipped anything[^6]. On this benchmark, Opus 5 was not the efficient frontier for cheap models to reach. It was the most expensive way to reach the top score.

The weakness: the two cost figures come from different parties, harnesses and price assumptions. DeepSeek's chart does not say whether it priced at peak or off-peak rates, or what cache-hit rate it assumed. Treat the 61× as an order-of-magnitude result (tens of times, not single digits) rather than a precise ratio.

## 4. Terminal-Bench 4.0: the benchmark where parity clearly fails

On long-horizon terminal tasks, 1017 is not at parity with Opus 5, and it is further still from Opus 5.5. DeepSeek's own number is 42.3 against Opus 5's 51.8, a 9.5-point deficit[^1]. The 51.8 matches the public leaderboard; Anthropic says the board, which uses "5 trials/task, Claude Code harness," reports Opus 5 at 51.8%, and its own setup "reproduces it at 52.3%, within noise"[^10]. Unlike the DeepSWE row, this gap is about four times Anthropic's ±1.6–2 point standard error on its Claude scores[^10].

:::slope(left-label="V4.1-Flash (Sep)", right-label="1017 (Oct)", unit=pts)
| Model | V4.1-Flash (Sep) | 1017 (Oct) |
|---|---|---|
| DeepSeek Flash, Terminal-Bench 4.0 | 31.2 | 42.3 |
| Claude Opus 5 (reference) | 51.8 | 51.8 |
| Claude Opus 5.5 (reference) | 66.4 | 66.4 |
:::

:::source
DeepSeek model cards (Sep[^5], Oct[^1]); Anthropic Opus 5.5 launch post[^10]. Opus rows are flat references, not re-measurements.
:::

The 11.1-point jump from September is partly a change of harness. The September card ran Terminal-Bench on "the Minimal mode of DeepSeek Harness"[^5]. The 1017 card switched to the Claude Code harness[^1]. The direction of that effect is not obvious: on Terminal-Bench 2.1 in September, Claude Code scored *lower* than DeepSeek's own harness for the same checkpoint, 88.0 vs 90.6[^5]. But the September-to-October comparison is not like-for-like, so some of the gain cannot be credited to the weights.

The independent data available so far points the same way. Artificial Analysis runs all 66 Terminal-Bench 4.0 tasks on mini-swe-agent with three repeats[^15]. A secondary tracker lists Artificial Analysis's score for the September V4.1-Flash at 26.8, below DeepSeek's self-reported 31.2[^19]. The same tracker, citing Terminal-Bench's own Harbor runs, shows how strongly Opus 5's own score depends on effort: 34.9 at low, 44.9 at medium, 50.3 at high, 51.8 at max, and 53.9 at extra-high[^19]. Terminal-Bench 4.0 itself removed 8 tasks, fixed 19, and set a flat 8-hour agent timeout[^14]. These are long tasks, and on long tasks a cheap model that "rabbitholes" spends its savings.

That failure mode was observed on day one. @teortaxesTex, normally a DeepSeek bull, reported that 1017 is "massively faster than V4.1 Flash, but only up until it does 90% of the job," after which it needed close handholding[^22]. Thom Wolf of Hugging Face wrote that he was "curious to see how these numbers will hold up outside their own eval setup"[^23]. Neither is a measurement, but both point at the same risk: per-task cost on a long-horizon task depends on whether the agent stops.

Why this matters: Terminal-Bench is the closer proxy for autonomous agent work, where nobody checks each step. That is where buyers most want Opus-class reliability, and it is where the self-reported gap is largest.

## 5. The price is real, but $0.15 is the floor, not the average

The advertised price is genuine for one buyer profile: US-hours traffic hitting DeepSeek's own API. DeepSeek defines peak as "01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays," and says "off-peak rates are half of the peak rates"[^3]. That is 35 of 168 weekly hours, about 21%. All of US business hours fall off-peak, while European mornings fall inside the peak window. The release day, a Saturday, was entirely off-peak[^3].

:::stack-bar(legend=true)
- {label: "Off-peak hours ($0.15 in / $0.60 out)", pct: 79}
- {label: "Peak hours, Mon–Fri UTC 01–04 & 06–10 ($0.30 / $1.20)", pct: 21}
:::

:::source
Share of the 168-hour week at each DeepSeek price tier. DeepSeek API pricing page, fetched 2026-10-17[^3].
:::

Buyers who will not send traffic to a PRC endpoint pay more. OpenRouter lists 36 endpoints for `deepseek/deepseek-v4.1-flash`, with input prices from about $0.015 to $0.60[^26]. The Western cluster (Together, Fireworks, Nebius, BaseTen, Parasail) mostly charges $0.30 / $1.20, double the headline, and some US-region or "fast" endpoints charge $0.45–$0.60 input[^26]. Opus 5.5 has no such spread: every host, including Bedrock, Vertex and Azure, charges the $4 / $20 list price, with regional variants at $4.40 / $22 and a 2× "fast" priority tier at $8 / $40[^27].

:::kv
- {term: "DeepSeek first-party, off-peak", def: "$0.003 cache hit · $0.15 cache miss · $0.60 output per M tokens[^3]"}
- {term: "DeepSeek first-party, peak", def: "$0.006 · $0.30 · $1.20[^3]"}
- {term: "Typical US third-party host", def: "≈ $0.30 in / $1.20 out (OpenRouter endpoint list, 2026-10-17)[^26]"}
- {term: "Concurrency", def: "2,500 requests per account, enforced at the account level regardless of API key[^3,44]"}
- {term: "Service availability", def: "99.47% for the V4.1 Flash API, Jul–Oct 2026 (status page)[^30]"}
- {term: "Claude Opus 5 (legacy)", def: "$5 in · $25 out · $0.50 cache read · $6.25 cache write[^12]"}
- {term: "Claude Opus 5.5", def: "$4 in · $20 out · $0.20 cache read · $5 cache write[^12,10]"}
:::

Mix matters more than headline price for agents. OpenRouter's October telemetry found cached tokens are "nearly nine in ten agentic tokens, but only about a third of the bill," with output around 1% of volume[^25]. It also found DeepSeek had the highest provider cache rate, about 96%[^25]. Heavy single-agent use can be more extreme still: one Claude Code user logged 5.09 billion cache-read tokens in 30 days against 3.89 million input-plus-output tokens[^43]. Applying OpenRouter's worked mix (87% cached, 12% fresh input, 1% output) to list prices gives a blended $0.027 per million tokens for DeepSeek off-peak, against $1.285 for Opus 5 and $0.854 for Opus 5.5. That makes Opus 5 about 48× more expensive and Opus 5.5 about 32×. At DeepSeek's peak rate, or a typical US host, the ratios fall to about 24× and 16×. These figures exclude Anthropic's cache-write premium, which would widen the gap, since DeepSeek does not charge separately for writes[^3,12].

The counterpoint is availability: 99.47% uptime is about 3.9 hours of downtime a month, below "three nines"[^30]. For an agent fleet, that downtime has to be priced in as a fallback provider.

## 6. Tokens per task: the missing variable

If per-token prices were the whole story, the per-task gap would track the price gap. It does not, because token consumption differs by model, and DeepSeek has published no number for its claimed reduction. The changelog says only "we also reduced the model's task runtime and output length"[^4]. The release note says the same in qualitative terms[^2].

Independent measurements before 1017 show DeepSeek's Flash line is not frugal. Artificial Analysis records that the September V4.1-Flash at max effort "generated 250M tokens" running its Intelligence Index, "very verbose in comparison to the median of 130M," at $0.27 per task[^16]. Opus 5 at max used 140M tokens at $5.86 per task, and Opus 5.5 at max used 260M at $5.98[^17,18]. So the per-task gap measured independently was about 22×, not the 42× output-price ratio. Flash spent about 1.8× as many tokens as Opus 5 to finish the same suite.

:::compare
- {role: LOWEST, name: "DeepSeek V4.1-Flash (Sep, max)", value: "$0.27 / task · 250M tokens"}
- {role: HIGHEST, name: "Claude Opus 5.5 (max)", value: "$5.98 / task · 260M tokens"}
- {role: SUBJECT, name: "Claude Opus 5 (max)", value: "$5.86 / task · 140M tokens"}
:::

:::source
Artificial Analysis Intelligence Index model pages, fetched 2026-10-17; all pre-1017[^16,17,18]. AA prices DeepSeek at its $0.30/$1.20 peak rate[^16].
:::

The only third-party measurement of 1017's token use so far is small. An ai.rs hands-on run of seven code-repair tasks, all solved by both checkpoints, found that "at equal effort, 1017 against its own September run thinks 18% less, answers 5% shorter and finishes 9% sooner"[^21]. That is a real reduction, but far short of the roughly 2.5× fewer tokens implied by DeepSeek's chart, which shows per-task cost falling about 61% at an unchanged price[^2,21]. One possible reconciliation: the chart's savings come mostly from long agentic trajectories, which a seven-task repair set does not exercise. Until an independent DeepSWE run reports tokens per task, the 1017 cost figure is DeepSeek's alone.

Anthropic's side has a similar confound. Its claim that Opus 5.5 is "~40% cheaper than Opus 5 per task" is stated "at default settings"[^41,10]. The effort docs show the default dropped from `high` on Opus 5 to `medium` on Opus 5.5[^13]. At max effort, Artificial Analysis measured the two at roughly equal per-task cost[^17,18].

Why this matters: a 2× swing in tokens per task moves the per-task ratio more than the peak/off-peak price schedule does. The single most valuable independent number for this question is 1017's tokens per DeepSWE task.

## 7. The track record: how far DeepSeek self-reports drift

DeepSeek's past agentic self-reports have held up directionally but run several points high, and the gap is larger on terminal benchmarks than on SWE-style repair. That history sets a reasonable prior for 1017.

:::slope(left-label="DeepSeek self-report", right-label="Independent", unit=pts)
| Release · benchmark | DeepSeek self-report | Independent |
|---|---|---|
| V3.2 · SWE-bench Verified (Vals) | 73.1 | 67.6 |
| V3.2 · Terminal-Bench 2.0 (Vals) | 46.4 | 36.0 |
| V4-Pro · SWE-bench Verified (Vals) | 80.6 | 77.4 |
| V4.1-Flash · Terminal-Bench 4.0 (AA) | 31.2 | 26.8 |
:::

:::source
DeepSeek V3.2 report[^31]; Vals.ai[^32,34]; DeepSeek V4-Pro card[^33]; V4.1-Flash card[^5]; Artificial Analysis via tracker[^19].
:::

The V3.2 case shows the mechanism. DeepSeek's report says "the reported score of 46.4 was achieved using the Claude Code framework," and its non-thinking Terminus run gave 39.3[^31]. Vals measured 35.95 ±5.12[^32]. On SWE-bench Verified, DeepSeek's 73.1 came from "our internal framework," and Vals measured 67.6 ±2.1[^31,32]. V4-Pro's 80.6 became 77.4 ±1.9 at Vals[^33,34]. The pattern: a 3–5 point discount on repair benchmarks and 5–10 points on terminal benchmarks.

The harness literature makes the same point more broadly. A May 2026 survey found that holding the model fixed and changing only the harness "raises Terminal-Bench 2 pass@1 from 69.7% to 77.0%," and documents up to 15 points of scaffold-only variation on SWE-bench Verified[^35]. A September paper found "within-model scaffold ranges reach 29.8 percentage points, compared with the 8.8-point spread of the top thirty" on the SWE-bench board[^36]. Leaderboard rank among frontier models is inside the scaffold noise.

Applying a 3–5 point discount to 77.0 gives roughly 72–74 on an independent DeepSWE run. That is still a tie with Opus 5's 74 ±4, and at the low end, a small deficit. The Decoder reads DeepSeek's chart as showing 1017 clearing only about 72 at its lowest effort setting[^20]. Applying 5–10 points to 42.3 on Terminal-Bench gives 32–37, a 15–20 point deficit to Opus 5.

The counterpoint: independent evaluators disagree with each other too. Vals' scale for later DeepSeek models has shifted in ways no other source reproduces[^34]. "Independent" is not one number, and a single third-party run will not settle this.

## 8. The comparator problem: Opus 5 is no longer Anthropic's model

DeepSeek benchmarked against a model Anthropic had already superseded, and that choice inflates the parity framing on both axes.

:::timeline
- {date: "2026-07-24", headline: "Claude Opus 5 ships", body: "Priced at $5 / $25 per M tokens, same as Opus 4.8."}
- {date: "2026-09-10", headline: "DeepSeek V4.1-Flash", body: "Price cut; DeepSWE 74.2 (best of 8 scaffolds), Terminal-Bench 4.0 31.2."}
- {date: "2026-09-22", headline: "Claude Opus 5.5 ships; Opus 5 becomes legacy", body: "$4 / $20; Terminal-Bench 4.0 66.4 at xhigh. Datacurve DeepSWE board updated the same day."}
- {date: "2026-09-28", headline: "ByteDance Seed phase-sensitivity paper", body: "Finds positional retrieval gaps from compressed attention in DeepSeek V4/V4.1."}
- {date: "2026-10-17 03:24 UTC", headline: "Silent fingerprint change", body: "deepseek-flash fingerprint decodes to a dsv41f_1017 build."}
- {date: "2026-10-17", headline: "V4.1-Flash-1017 announced", body: "\"Minor update\"; MIT weights; price unchanged; table compares against Opus 5."}
:::

:::source
Anthropic[^11,10]; DeepSeek[^5,1,4]; Datacurve[^6]; arXiv 2609.36322[^37]; @teortaxesTex[^24].
:::

Anthropic's own pricing page lists Opus 5 as legacy and Opus 5.5 at $4 input, $20 output and $0.20 cache read, 20% below Opus 5 on input and output and 60% below on cache reads[^12,10]. Against Opus 5.5, the price ratios shrink by about a fifth, and the Terminal-Bench gap grows from 9.5 points to 24.1 (42.3 vs 66.4)[^1,10]. Artificial Analysis independently measured Opus 5.5 at 59.6 on its mini-swe-agent Terminal-Bench 4.0 run[^15], still about 17 points above 1017's self-reported score. Datacurve's DeepSWE board has no Opus 5.5 row yet[^6], so the one benchmark where 1017 ties cannot be checked against the current flagship.

Market data suggests buyers already treat these as separate tiers. Vercel's AI Gateway reported that in July, Anthropic "collected 65.1% of all spend on 30% of total volume," with more than 80% of coding-agent spend, while DeepSeek held about a quarter of tokens and its spend share "barely moved"[^29]. OpenRouter said V4.1-Flash did "1T tokens in 24 hours" after launch, about 90% of them cache reads[^28]. Volume is going to DeepSeek. Coding-agent money, so far, has not.

:::callout(kind=info, label="Why the comparator choice matters")
Comparing against a superseded flagship is standard practice for open-weight labs: the newest closed model's numbers often are not on public leaderboards yet. It is not evidence of bad faith. But it means "parity with Opus 5" describes a model buyers can no longer choose as their default, not the current price-performance frontier.
:::

## 9. What could break the thesis

The thesis is that 1017 is likely tens of times cheaper per task than Opus 5 on contained repo work, ties it there within noise, and trails clearly on long-horizon terminal work. Five things could break it, in both directions.

**1. Independent DeepSWE runs come in low.** If Datacurve or Artificial Analysis scores 1017 at the bottom of the 3–5 point discount band (about 72) on mini-swe-agent, the "tie" becomes a 2-point deficit. That is still inside ±4, but it removes the headline "beats Opus 5." The Decoder's reading of DeepSeek's chart, about 72 at the lowest effort setting, shows how thin the margin is[^20].

**2. Token savings fail to reproduce.** The only independent token measurement shows 5–18% reductions on seven tasks[^21], not the roughly 2.5× implied by the vendor chart[^2]. If an independent DeepSWE run measures per-task cost nearer the September figure, the per-task gap falls back toward the 22× Artificial Analysis measured on its index[^16,17]. That would still be a large gap, but far from 60×.

**3. Long-context quality under compressed attention.** A ByteDance Seed-led paper found "high average accuracy can coexist with systematic positional failures" in DeepSeek V4-family models. It measured a 40.2-point best-to-worst phase gap on V4-Flash-Base, narrowing to at most about 6.1 points after post-training on the September V4.1-Flash[^37,38]. The test was run at 128K, not 1M[^37]. Agent loops that fill the context window are exactly where such failures would show up as retries.

**4. Legal exclusion for some buyers.** Section 1532 of the FY2026 NDAA (Public Law 119-60) bars Department of Defense contractors from using AI "developed by" DeepSeek or High-Flyer in contract performance. That ban has applied since January 17, 2026, and a compliance analysis reads it as covering self-hosted weights too[^40,46,47]. DeepSeek is not on the Commerce Entity List, although an interagency committee approved listing it[^45]. For a defense contractor, the parity question is moot.

**5. The steelman for parity.** For most buyers the relevant question is not "is it as good as Opus" but "is it good enough at 1/20th the cost." On DeepSWE-shaped work, where a test suite verifies each attempt, a cheap model can buy reliability by retrying: three 1017 attempts at about $0.20 each still cost about 5% of one Opus 5 attempt[^2,6]. If that holds, "parity" understates what DeepSeek shipped. The limit is that retries only help when a verifier can tell which attempt worked, and long open-ended terminal tasks often lack one.

**Red-team pass: 3/3 top claims unbroken.** An adversarial reviewer ran multiple searches against each of three claims: the ~61× DeepSWE per-task cost gap, the 9.5-point Terminal-Bench deficit, and the peak/off-peak price schedule. It found no contradicting source. Independent runs do put Opus 5.5 lower on Terminal-Bench 4.0 than Anthropic's 66.4 (Artificial Analysis 59.6)[^15]. That narrows, but does not close, the gap to 1017. The 1017 per-task cost figures still exist only in DeepSeek's chart.

:::references
- {id: 1, title: "DeepSeek-V4.1-Flash-1017 model card", url: "https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017", source: "Hugging Face / DeepSeek", date: "2026-10-17"}
- {id: 2, title: "DeepSeek-V4.1-Flash-1017 release note", url: "https://api-docs.deepseek.com/news/news261017", source: "DeepSeek API Docs", date: "2026-10-17"}
- {id: 3, title: "Models & Pricing (deepseek-flash)", url: "https://api-docs.deepseek.com/quick_start/pricing", source: "DeepSeek API Docs", date: "2026-10-17"}
- {id: 4, title: "Change log", url: "https://api-docs.deepseek.com/updates", source: "DeepSeek API Docs", date: "2026-10-17"}
- {id: 5, title: "DeepSeek-V4.1-Flash model card", url: "https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash", source: "Hugging Face / DeepSeek", date: "2026-09-10"}
- {id: 6, title: "DeepSWE v1.1 leaderboard", url: "https://deepswe.datacurve.ai/", source: "Datacurve", date: "2026-09-22"}
- {id: 7, title: "DeepSWE v1.1 announcement", url: "https://deepswe.datacurve.ai/blog/deepswe-v1-1", source: "Datacurve", date: "2026-06-14"}
- {id: 8, title: "DeepSWE: harness pilot", url: "https://deepswe.datacurve.ai/blog/deepswe", source: "Datacurve", date: "2026-05-26"}
- {id: 9, title: "datacurve-ai/deep-swe repository", url: "https://github.com/datacurve-ai/deep-swe", source: "GitHub"}
- {id: 10, title: "Introducing Claude Opus 5.5", url: "https://www.anthropic.com/news/claude-opus-5-5", source: "Anthropic", date: "2026-09-22"}
- {id: 11, title: "Introducing Claude Opus 5", url: "https://www.anthropic.com/news/claude-opus-5", source: "Anthropic", date: "2026-07-24"}
- {id: 12, title: "Claude pricing", url: "https://claude.com/pricing", source: "Anthropic", date: "2026-10-17"}
- {id: 13, title: "Effort parameter documentation", url: "https://platform.claude.com/docs/en/build-with-claude/effort", source: "Anthropic Docs", date: "2026-10-17"}
- {id: 14, title: "Terminal-Bench 4.0 release notes", url: "https://www.tbench.ai/news/terminal-bench-4-0", source: "Terminal-Bench"}
- {id: 15, title: "Terminal-Bench 4.0 evaluation", url: "https://artificialanalysis.ai/evaluations/terminalbench-4-0", source: "Artificial Analysis", date: "2026-10-17"}
- {id: 16, title: "DeepSeek V4.1 Flash — model page", url: "https://artificialanalysis.ai/models/deepseek-v4-1-flash", source: "Artificial Analysis", date: "2026-10-17"}
- {id: 17, title: "Claude Opus 5 — model page", url: "https://artificialanalysis.ai/models/claude-opus-5", source: "Artificial Analysis", date: "2026-10-17"}
- {id: 18, title: "Claude Opus 5.5 — model page", url: "https://artificialanalysis.ai/models/claude-opus-5-5", source: "Artificial Analysis", date: "2026-10-17"}
- {id: 19, title: "Terminal-Bench 4.0 rankings (aggregator)", url: "https://llmlearner.com/rankings/terminal-bench-4-0", source: "LLM Learner", date: "2026-10-13"}
- {id: 20, title: "DeepSeek V4.1 Flash 1017 beats larger rivals in agentic tasks while once again massively cutting per-task costs", url: "https://the-decoder.com/deepseek-v4-1-flash-1017-beats-larger-rivals-in-agentic-tasks-while-once-again-massively-cutting-per-task-costs/", source: "The Decoder", date: "2026-10-17"}
- {id: 21, title: "DeepSeek V4.1 Flash 1017 vs V4 Flash vs Muse Spark Open on DGX Spark", url: "https://ai.rs/ai-developer/deepseek-v4-1-flash-1017-vs-v4-flash-vs-muse-spark-open-dgx-spark", source: "ai.rs", date: "2026-10-17"}
- {id: 22, title: "@teortaxesTex hands-on with 1017", url: "https://x.com/teortaxesTex/status/2111394568725774765", source: "X", date: "2026-10-17"}
- {id: 23, title: "@Thom_Wolf on 1017's numbers", url: "https://x.com/Thom_Wolf/status/2111401132840890440", source: "X", date: "2026-10-17"}
- {id: 24, title: "@teortaxesTex: deepseek-flash fingerprint change", url: "https://x.com/teortaxesTex/status/2111306155448205700", source: "X", date: "2026-10-17"}
- {id: 25, title: "Inferred #03: Cache is crucial", url: "https://openrouter.ai/data/newsletter/cache-is-crucial", source: "OpenRouter", date: "2026-10-08"}
- {id: 26, title: "deepseek/deepseek-v4.1-flash endpoints", url: "https://openrouter.ai/api/v1/models/deepseek/deepseek-v4.1-flash/endpoints", source: "OpenRouter API", date: "2026-10-17"}
- {id: 27, title: "anthropic/claude-opus-5.5 endpoints", url: "https://openrouter.ai/api/v1/models/anthropic/claude-opus-5.5/endpoints", source: "OpenRouter API", date: "2026-10-17"}
- {id: 28, title: "OpenRouter: DeepSeek V4.1 Flash 1T tokens in 24 hours", url: "https://x.com/OpenRouter/status/2098503808682967356", source: "X", date: "2026-09-11"}
- {id: 29, title: "DeepSeek overtakes Google on volume as cost per token falls", url: "https://vercel.com/blog/deepseek-overtakes-google-on-volume-cost-per-token-falls", source: "Vercel", date: "2026-08"}
- {id: 30, title: "DeepSeek service status", url: "https://status.deepseek.com/", source: "DeepSeek", date: "2026-10-17"}
- {id: 31, title: "DeepSeek-V3.2 technical report", url: "https://arxiv.org/html/2512.02556v1", source: "arXiv", date: "2025-12"}
- {id: 32, title: "DeepSeek V3.2 (Thinking) on Vals", url: "https://www.vals.ai/models/fireworks_deepseek-v3p2-thinking", source: "Vals.ai"}
- {id: 33, title: "DeepSeek-V4-Pro model card", url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro", source: "Hugging Face / DeepSeek", date: "2026-04"}
- {id: 34, title: "DeepSeek V4 Pro on Vals", url: "https://www.vals.ai/models/deepseek_deepseek-v4-pro", source: "Vals.ai"}
- {id: 35, title: "Harness effects in agent evaluation (Zhang et al.)", url: "https://arxiv.org/html/2605.23950v1", source: "arXiv", date: "2026-05-07"}
- {id: 36, title: "Scaffold variance vs ranking resolution on SWE-bench (Liu et al.)", url: "https://arxiv.org/abs/2609.17394", source: "arXiv", date: "2026-09-15"}
- {id: 37, title: "Phase sensitivity in compressed-attention long-context retrieval (Zhu et al.)", url: "https://arxiv.org/abs/2609.36322", source: "arXiv", date: "2026-09-28"}
- {id: 38, title: "ByteDance researchers identify cause of inconsistent long-context retrieval in DeepSeek models", url: "https://technode.com/2026/10/09/bytedance-researchers-identify-cause-of-inconsistent-long-context-retrieval-in-deepseek-models/", source: "TechNode", date: "2026-10-09"}
- {id: 39, title: "AutomationBench leaderboard", url: "https://zapier.com/benchmarks", source: "Zapier", date: "2026-10-17"}
- {id: 40, title: "Prohibition on use of DeepSeek AI in FY2026 NDAA (P.L. 119-60) entered into force for DoD contractors", url: "https://digitalpolicyalert.org/event/42290-prohibition-on-use-of-deepseek-and-related-artificial-intelligence-in-national-defense-authorization-act-for-fiscal-year-2026-public-law-119-60-entered-into-force-for-department-of-defense-and-its-contractors", source: "Digital Policy Alert", date: "2026-01-17"}
- {id: 41, title: "@ClaudeDevs: Opus 5.5 ~40% cheaper per task", url: "https://x.com/ClaudeDevs/status/2102438800836489554", source: "X", date: "2026-09-22"}
- {id: 42, title: "@kimmonismus: 1017 benchmarks and pricing", url: "https://x.com/kimmonismus/status/2111385805449048181", source: "X", date: "2026-10-17"}
- {id: 43, title: "Claude Code cache-read token usage report (issue #24147)", url: "https://github.com/anthropics/claude-code/issues/24147", source: "GitHub", date: "2026-02-08"}
- {id: 44, title: "Rate limit", url: "https://api-docs.deepseek.com/quick_start/rate_limit", source: "DeepSeek API Docs"}
- {id: 45, title: "US holds off blacklisting DeepSeek, CXMT and over 100 Chinese firms", url: "https://www.republicworld.com/world-news/us-holds-off-blacklisting-deepseek-cxmt-and-over-100-chinese-firms-despite-interagency-approval-to-avoid-beijing-tensions-2026-06-16-128557", source: "Reuters via Republic World", date: "2026-06-17"}
- {id: 47, title: "DeepSeek and the FY2026 NDAA: what DoD contractors need to know", url: "https://petronellatech.com/blog/deepseek-and-the-fy2026-ndaa-what-dod-contractors-need-to-know/", source: "Petronella Technology Group"}
- {id: 46, title: "NDAA 2026 guidance and prohibition on use of certain artificial intelligence", url: "https://bpb-us-e1.wpmucdn.com/websites.harvard.edu/dist/f/106/files/2026/01/NDAA-2026-Guidance-and-Prohibition-on-use-of-certain-Artificial-Intelligence.pdf", source: "Harvard University", date: "2026-01-14"}
:::
