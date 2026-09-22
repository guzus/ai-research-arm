---
eyebrow: BENCHMARK FORENSICS · MODEL EVALUATION
title: A 46 is not evidence that two models are the same
deck: Xiaomi's MiMo-V2.6-Pro and xAI's Grok 4.7 landed on the same integer on the same day. Almost everything that matters about them is in the parts the integer averaged away.
domain: general
lede: |
  On 21 September 2026 Xiaomi released MiMo-V2.6-Pro, a 1.02-trillion-parameter
  open-weight mixture of experts, and Artificial Analysis scored it 46 on
  Intelligence Index v4.3.2 at a reported $0.13 per Index task. xAI released
  Grok 4.7 the same day, and it scored 46 too. The headline wrote itself: an
  MIT-licensed Chinese model had tied a US frontier release at a twenty-ninth
  of the price. The score is real, the price is real, and the tie is real in
  the narrow sense that both numbers round to the same integer. What follows
  is an audit of everything those three facts do not settle — starting with
  the fact that the two models disagree on nine of the index's ten
  constituents, that the instrument was rebuilt three times in the seventeen
  days before they were measured, and that the $0.13 is a list price from the
  only seller currently offering one.
stats:
  - {label: Intelligence Index v4.3.2, value: 46, note: "MiMo-V2.6-Pro and Grok 4.7 (xhigh), as of 23 Sep 2026"}
  - {label: Cost per Index task, value: $0.13, note: "vs $3.74 for Grok 4.7 (xhigh)"}
  - {label: AA-Omniscience, value: 8, note: "vs 32 for Grok 4.7 — same composite"}
  - {label: API providers serving MiMo, value: 1, note: "Xiaomi's own endpoint"}
---

## 01. Anatomy of a 46

The Artificial Analysis Intelligence Index is not a test. It is a weighted average of ten tests, chosen editorially, recomposed repeatedly over the past year [^33], and reported as an integer.

:::callout(kind=info, label="The short answer")
- **Does MiMo-V2.6-Pro match Grok 4.7?** On the composite, yes, to the precision published. On the constituents, no: Grok leads the agentic and factuality evaluations, MiMo leads reasoning, coding and long context, and they differ by 24 points on factuality alone [^1].
- **Is the 0.1-point gap behind the shared integer meaningful?** No. It is inside Artificial Analysis' own stated 95% confidence interval and far inside the item-sampling error of the index's smallest constituents [^4].
- **Is $0.13 a task what the model costs?** It is what Xiaomi charges on the one endpoint that serves it [^7][^8]. Xiaomi sells the identical checkpoint at ten times that rate as UltraSpeed [^9], and a self-hoster renting a minimum cluster pays roughly two orders of magnitude more per token at single-stream throughput.
- **Is this evidence of rapid capability deflation?** Not from this number. The index and its cost metric were both rebased on 4 and 7 September 2026; the same unchanged Grok 4.6 reads 61 in August and 44 now, at $0.84 and then $1.86 a task [^34][^35].
- **Is the $2.62M training cost real?** Yes, and it covers a six-day reinforcement-learning run on an undisclosed base model — not the model [^17].
:::

Index v4.3.2 distributes its weight across four categories: Agents 30%, Coding 20%, General 30%, Scientific Reasoning 20% [^4]. Inside those sit ten evaluations — AA-Briefcase v1.1 at 15%, AA-Omniscience at 15% (split 10% accuracy and 5% non-hallucination), GDPval-AA v2.1, Terminal-Bench 4.0, SciCode, GDP.pdf, HLE and CritPt at 10% each, and AutomationBench-AA and AA-LCR v1.1 at 5% [^4].

:::stack-bar(legend=true)
- {label: "Agents", pct: 30}
- {label: "General", pct: 30}
- {label: "Coding", pct: 20}
- {label: "Scientific Reasoning", pct: 20}
:::

Two features of that construction are load-bearing and neither is visible in the headline. First, repeat counts are wildly uneven: GDP.pdf and CritPt are run five times, Terminal-Bench 4.0, SciCode and AA-LCR three times, and the remaining five — AA-Briefcase, GDPval-AA, AutomationBench-AA, AA-Omniscience and HLE — exactly once each [^4]. Those five carry 55% of total index weight, so the majority of the number has no run-to-run variance estimate behind it at all, at a sampling temperature of 0.6 for reasoning models [^4]. Second, two of the ten constituents — AA-Briefcase and GDPval-AA — are reported as Elo ratings, and are rescaled into the same average as the eight pass-rate percentages [^4]. Averaging an interval-scaled Elo, whose origin is an arbitrary anchor, against a proportion bounded at zero and one is a choice, not a measurement; and v4.3.2 consisted precisely of moving one of those anchors [^33].

The cost figure has a similar gap between what it says and what it counts. Artificial Analysis reports that evaluating MiMo-V2.6-Pro cost $206.66 in total and $0.13 per Index task [^7]. Those two numbers are not related by division. Summing the published item counts across the ten evaluations gives exactly 9,750 single-pass tasks [^4]; $206.66 spread across them is about $0.021 each, which is a sixth of the published figure. The reconciliation is that $0.13 is not total spend over tasks executed but a weighted average across benchmarks — Artificial Analysis labels the metric a "weighted average cost (USD) per Artificial Analysis Intelligence Index task" [^7] — so the "task" in "$0.13 a task" is a synthetic unit that corresponds to no workload anyone actually ran. It is internally consistent and externally unportable: it cannot be compared to a buyer's own per-request cost, and its denominator moves with how a given model's spend distributes across the ten evaluations.

The counterpoint deserves stating before the critique goes further. Artificial Analysis runs every evaluation itself rather than accepting vendor numbers, publishes its weights, publishes the constituents, and presents intelligence and cost as two axes rather than one ranking [^6]. That is a higher standard than most of the industry meets, and this article's argument is not that the index is dishonest. It is that a scalar reported to two significant figures, on an instrument with these properties, cannot carry the weight of "these two models are equivalent."

## 02. The tie is below the instrument's resolution

The gap between MiMo-V2.6-Pro and Grok 4.7 is smaller than the number of digits Artificial Analysis publishes, and smaller still than the error bar Artificial Analysis publishes on those digits.

Artificial Analysis reports the Intelligence Index as an integer. Xiaomi reports MiMo-V2.6-Pro at 46.32 on the same index [^36], a figure Artificial Analysis does not display. No one publishes Grok 4.7's score to matching precision. So the strongest defensible reading of the September 21 result is not "MiMo ties Grok" — it is that nobody, including the evaluator, has published enough precision for the comparison to be made at all. Against that, Artificial Analysis states that it estimates a 95% confidence interval for the index "of less than ±1%", derived from more than ten repeats on certain models [^4]. On a score of 46, ±1% is roughly ±0.46 index points under the relative reading and ±1 point under the absolute one. Either interval swallows the difference between two models that both display 46.

The sharper evidence is internal to Grok itself. Artificial Analysis scored Grok 4.7 at two reasoning-effort settings. Both display 46 [^33]. The high setting consumed 200M output tokens across the index run and cost $2.73 a task; xhigh consumed 240M and cost $3.74 [^56][^16]. Twenty per cent more generated tokens and 37% more money bought a difference that the published resolution cannot represent. If integer display destroys the signal between two configurations of the same model, it certainly destroys it between two different models.

Item-sampling error compounds this, and it is the error Artificial Analysis' stated interval does not address. A ±1% figure derived from repeat runs on a fixed question set estimates run-to-run variance; it conditions away the question of whether a different sample of items would have ordered the models the same way. For a benchmark of *n* binary-scored items at accuracy *p*, the standard error is √(p(1−p)/n), and the index's smallest constituents are very small.

:::bars
- {label: "Terminal-Bench 4.0 (n=66)", value: "±12.1 pp", pct: 100}
- {label: "CritPt (n≈70)", value: "±11.7 pp", pct: 97}
- {label: "AA-Briefcase v1.1 (n≈91)", value: "±10.3 pp", pct: 85}
- {label: "AA-LCR v1.1 (n=100)", value: "±9.8 pp", pct: 81}
- {label: "SciCode (n≈288)", value: "±5.8 pp", pct: 48}
- {label: "AutomationBench-AA (n≈657)", value: "±3.8 pp", pct: 32}
- {label: "Humanity's Last Exam (n≈2,158)", value: "±2.1 pp", pct: 17}
- {label: "AA-Omniscience (n≈6,000)", value: "±1.3 pp", pct: 11}
:::

:::source
95% half-widths computed by this article from the binomial standard error at p = 0.5 (p = 0.49 for HLE), using the per-evaluation item counts published in Artificial Analysis' Index v4.3.2 methodology as read on 23 September 2026 [^4]. The counts sum to exactly 9,750. Item-level scoring is not strictly binary for the Elo-based constituents, AA-Briefcase and GDPval-AA, for which no clean binomial analogue exists; they are omitted here.
:::

Terminal-Bench 4.0 and CritPt together carry 20% of the index weight on roughly 136 items. Propagating those errors through the published weights puts the composite's item-sampling half-width in the region of two index points — double Artificial Analysis' stated interval, and an order of magnitude above the gap being reported as a tie. The measurement literature points the same way from a different angle: Miller's work on evaluation error bars concludes that a new evaluation needs roughly 969 questions to detect a three-point difference at 80% power, and that clustered standard errors can be more than three times larger than naive ones [^37]. Separately, semantically neutral prompt-format changes have been shown to move accuracy by as much as 76 points on the same model and the same items [^53] — a reminder that the quantity being averaged is not capability but capability-given-a-harness.

What would weaken this reading: aggregation genuinely does suppress per-benchmark noise, and a ten-evaluation mean is far more stable than any one of its parts. The argument here is not that the composite is noise. It is that the *specific claim being made* — that two models are at the same level — is a claim about a difference, and differences are where the noise lives. "Tie" survives. "MiMo edges out Grok," or the reverse, does not.

This matters because a rounded integer reads as a fact and a confidence interval reads as a caveat, and only the integer travels.

## 03. Same score, opposite shapes

The two models agree on the composite and differ on every one of its ten parts — and the disagreement is not scattered noise, it is sorted by evaluation family, which is precisely the condition under which a single scalar stops carrying information about the thing it is being used to decide.

| Constituent | Weight | MiMo-V2.6-Pro | Grok 4.7 (xhigh) | Edge |
|---|---|---|---|---|
| AA-Briefcase v1.1 (Elo) | 15% | 1522 | 1657 | Grok |
| *AA-Omniscience (index) | 15% | 8 | 32 | Grok |
| GDPval-AA v2.1 (Elo) | 10% | 1673 | 1695 | Grok |
| GDP.pdf | 10% | 19% | 20% | Grok |
| AutomationBench-AA | 5% | 59% | 66% | Grok |
| Terminal-Bench 4.0 | 10% | 35% | 26% | MiMo |
| SciCode | 10% | 61% | 57% | MiMo |
| Humanity's Last Exam | 10% | 49% | 43% | MiMo |
| CritPt | 10% | 27% | 18% | MiMo |
| AA-LCR v1.1 | 5% | 86% | 77% | MiMo |

All figures above are from Artificial Analysis' own comparison page as of 23 September 2026, which states verbatim that "Both models score 46 on the Artificial Analysis Intelligence Index."[^1] The weights are AA's published v4.3.2 allocation.[^4]

The partition is clean enough to be structural. Grok 4.7 takes every agentic and tool-use constituent — Briefcase, GDPval-AA, AutomationBench — plus the PDF-comprehension eval, a bloc carrying 55% of index weight. MiMo-V2.6-Pro takes every reasoning, coding and long-context constituent — Terminal-Bench, SciCode, HLE, CritPt, AA-LCR — carrying the other 45%.[^1][^4] Neither model wins a constituent that belongs to the other's cluster.

:::slope(left-label=MiMo-V2.6-Pro, right-label="Grok 4.7 (xhigh)", unit=%)
| Item | MiMo | Grok |
|---|---|---|
| Terminal-Bench 4.0 | 35 | 26 |
| SciCode | 61 | 57 |
| AA-LCR v1.1 | 86 | 77 |
| Humanity's Last Exam | 49 | 43 |
| CritPt | 27 | 18 |
| AutomationBench-AA | 59 | 66 |
:::

Five of the six directly comparable percentage constituents slope the same way, and the sixth — the one agentic eval scored as a percentage rather than an Elo — reverses. A composite is defensible as a single number when its constituents load on one latent factor and the residuals are random. Here the residuals are cluster-aligned, which means the index is averaging across at least two distinct capabilities and reporting their midpoint. At 46, the midpoint is reached by opposite routes.

The factuality constituent is where the divergence stops being a methodological observation and becomes a deployment risk. AA-Omniscience separates these two tied models by 24 index points, 8 against 32.[^1] For calibration: the leaderboard leader as of 23 September 2026 is Claude Opus 5.5 at 46, with GPT-6 Astra at 44 and Claude Fable 5.1 at 43.[^2] The gap between Grok 4.7 and the frontier is 14 points. The gap between Grok 4.7 and the model it ties on the composite is larger than that — nearly twice the distance that separates Grok from the best-measured system in the world.

:::callout(kind=warn, label=Unresolved)
Artificial Analysis publishes Grok 4.7's Omniscience components — 47% accuracy against a 29% hallucination rate, down from Grok 4.6's 34%.[^3] It does not publish the corresponding split for MiMo-V2.6-Pro.[^2] Because Artificial Analysis defines hallucination rate as the proportion of incorrect answers out of all non-correct responses,[^2] an index of 8 is reachable either by a model that knows little or by a model that answers confidently when it does not know. Those two failure modes call for opposite mitigations, and the published data does not distinguish them.
:::

What would weaken this reading: several of MiMo's winning margins are thin at the constituent level. AA-LCR v1.1 is 100 questions over documents of 10k to 100k tokens and carries 5% of the index;[^4] the leaderboard puts MiMo at 86.3% and Grok at 77%, behind Kimi K3 at 88.7%.[^5] On a 100-item instrument, a nine-point difference sits under two standard errors of the difference in proportions — suggestive, not established. The same eval also fails to probe what it appears to reward: MiMo advertises a 1,000k context window against Grok's 500k,[^1] while the constituent that names long context tops out an order of magnitude below either.

The fair objection is not that Artificial Analysis aggregated. An equally weighted composite is *designed* to average across divergent strengths, and a reader who wanted one scalar received one; Artificial Analysis also publishes the constituents, and elsewhere presents a two-dimensional intelligence-versus-cost frontier rather than a single ranking.[^6] The problem is the decision surface. The public leaderboard row a buyer actually scans carries index, cost per task, output tokens per second and latency — no factuality column. A 24-point Omniscience gap is therefore invisible at the moment of selection, recoverable only by clicking through to the comparison page.

The same inversion shows up in the speed row. MiMo posts 76 output tokens per second to Grok's 39, but time to first answer token is 28.79 seconds against 0.85.[^1] Artificial Analysis' own prose calls MiMo "faster than average, however somewhat verbose" and Grok "notably slow and very verbose."[^7] On the published throughput metric MiMo is twice as fast; on the metric a user perceives it is thirty-four times slower.

At this score level the composite is not merely incomplete — it is non-discriminating. A 46 tells a buyer nothing about which of two structurally opposite systems to deploy, and the selection has to be made on constituents that point the other way.

## 04. The instrument moved three times in seventeen days

Artificial Analysis rebuilt the Intelligence Index on 4, 7 and 19 September 2026 — the last of those two days before both models being compared were released [^33].

:::timeline
- {date: 2026-06-15, headline: "Index v4.1", body: "Nine evaluations. GPQA-Diamond and τ³-Banking still in the basket; roughly 20% of weight on private held-out sets."}
- {date: 2026-08-06, headline: "v4.1.1 — graders swapped", body: "LLM graders upgraded; category weights unchanged."}
- {date: 2026-08-12, headline: "Grok 4.6 published at 61", body: "Artificial Analysis reports Grok 4.6 scoring 61, joining the frontier, at $0.84 per Index task."}
- {date: 2026-09-04, headline: "v4.2 — GPQA-Diamond dropped as saturated", body: "AA-Briefcase and GDP.pdf added. Private held-out weighting doubles from 20% to 40%."}
- {date: 2026-09-07, headline: "v4.3 — Terminal-Bench 2.1 replaced by 4.0", body: "τ³-Banking replaced by AutomationBench-AA. Private weighting rises to 45%."}
- {date: 2026-09-19, headline: "v4.3.2 — GDPval-AA Elo re-anchored", body: "Scale pinned to DeepSeek V4.1 Flash (max) at 1600, mechanically shifting every model's contribution from that constituent."}
- {date: 2026-09-21, headline: "MiMo-V2.6-Pro and Grok 4.7 both score 46", body: "Both measured under v4.3.2. The unchanged Grok 4.6 now reads 44 — seventeen points below its August figure."}
:::

The Grok 4.6 case is the cleanest available proof that these are instrument moves, not model moves. Artificial Analysis published Grok 4.6 at 61 on 12 August 2026 [^34]; its model page reports 44 today [^35]. The weights did not change; the index did. The cost metric moved with it: the same model on the same unchanged $2 input and $6 output rate card is reported at $0.84 per Index task in August and $1.86 in September [^34][^35], because the task set got harder and longer, not because anyone repriced anything. Artificial Analysis publishes no index-level statement that scores are non-comparable across versions. It publishes such statements per evaluation — AA-LCR v1.1 carries the note that scores "are not directly comparable with v1.0" [^4] — but the composite does not.

Two consequences follow, and they point in opposite directions, which is why this section exists.

The first is that the MiMo-versus-Grok comparison is *unaffected*. Both were scored under v4.3.2, two days after it shipped [^7][^16]. So is the generational comparison: MiMo-V2.5-Pro's 26 and MiMo-V2.6-Pro's 46 are both current v4.3.2 readings [^31], which means the 20-point gain is a real same-instrument result and not the artefact it is sometimes assumed to be. Anyone reaching for the rebase to discount the headline result has the argument backwards.

The second is that every *cross-time* claim built on these numbers is invalid, and those claims are everywhere. "The top open-weight score rose from 26 to 46" is fine; "capability at a given price has collapsed since August" is not, because no cost-per-task figure published before 4 September 2026 can be differenced against one published after. The longest valid cost-per-task series ending at MiMo's $0.13 begins on 7 September 2026 — fifteen days — and within it Artificial Analysis has published per-task figures for different models, not a time series for any one of them. This repository's own independent price instrument is the only method-stable series spanning the window, and it is denominated per token rather than per task. Across 171 records from 6 August to 22 September 2026 under a frozen method, the cheapest dollar-per-million-output-tokens buying a GPQA-Diamond score of at least 0.8 drifted from $0.18 to $0.13, dipping as low as $0.08 in between; over the same window the price of the highest tier it measures, at least 0.9, went the other way, from $0.18 to $0.50 [^52]. Two caveats blunt both readings: the basket of scored models grew from 76 to 104 over those seven weeks, so the series is not a constant-quality index, and the 0.95 tier's move from $50.00 to $3.75 in five days was caused by a benchmark score being published, not by a price changing [^52]. Forty-seven days of a churning basket cannot be annualised, and nothing in it resembles the order-of-magnitude deflation the $0.13 headline is being used to illustrate.

The steelman for Artificial Analysis is strong and should be stated. The index was rebuilt because it was being outrun: GPQA-Diamond was dropped because models had solved it [^27], Terminal-Bench 2.1 was saturated with current models clustering between 84 and 92 [^24], and the private held-out share more than doubled specifically to reduce the ability of labs to game evaluations [^27][^6]. Those are the actions of an evaluator responding to saturation, not manufacturing outcomes. But responsiveness and comparability are in direct tension, and Artificial Analysis has chosen responsiveness without labelling what it costs. A third consideration cuts at the constituents themselves: Epoch AI audited a random sample of 48 Humanity's Last Exam questions and found 22 of them — 46% — carried substantial accuracy-altering errors, designating the benchmark Flawed [^38]. HLE carries 10% of the index.

This matters because the rebase is the single most common unstated confound in AI benchmark coverage, and it is invisible from the leaderboard: the page renders today's number against today's instrument, with no version stamp on last month's memory of it.

## 05. The $0.13 is a price, and one seller sets it

$0.13 per Index task is a real measurement of one seller's list price on one endpoint on one day — not a property of the model, and not a cost any third party can presently obtain.

Artificial Analysis spent $206.66 evaluating MiMo-V2.6-Pro on the Intelligence Index, consuming 140M output tokens, and reports the result as $0.13 per task [^7]. Every input to that figure is Xiaomi's own price card: $0.43 per 1M input tokens and $0.87 per 1M output, blending to $0.18 per 1M tokens under Artificial Analysis' 7:2:1 cache-hit/input/output assumption, as of 23 September 2026 [^7]. The card also carries a 99% cache discount, which Xiaomi and OpenRouter both price at $0.0036 per million tokens on a cache read [^36][^8] — so on a harness with long shared prefixes, the blended rate is dominated by a term that encodes Xiaomi's storage policy rather than the model's competence [^7].

:::rank-list
- {label: "Claude Fable 5.1 (max)", value: $7.63, pct: 100}
- {label: "Grok 4.7 (xhigh)", value: $3.74, pct: 49}
- {label: "GPT-6 Astra (max)", value: $3.26, pct: 43}
- {label: "Grok 4.7 (high) — also scores 46", value: $2.73, pct: 36}
- {label: "GLM-5.3 (max)", value: $2.01, pct: 26}
- {label: "Kimi K3", value: $2.00, pct: 26}
- {label: "Gemini 3.8 Flash", value: $1.24, pct: 16}
- {label: "DeepSeek V4.1 Flash", value: $0.27, pct: 4}
- {label: "MiMo-V2.6-Pro", value: $0.13, pct: 2, highlight: true}
:::

The spread above is a price table, not a compute table. Grok 4.7 at xhigh costs $3.74 per task against MiMo's $0.13, a 29× ratio; the high setting that also ties MiMo at 46 costs $2.73, a 21× ratio [^56]. None of those multiples were measured in joules or GPU-seconds. They were read off vendor cards.

What makes MiMo's card unusually weak as evidence is that it has no second quote. Artificial Analysis lists **1 API provider** [^7]; OpenRouter's endpoint list for the model returns exactly one, "Xiaomi," serving FP8 at 1,048,576 context with 99.994% single-day uptime as of 23 September 2026 [^8]. A directory that counts routing gateways rather than inference hosts shows thirteen rows for the model, but every one of them resolves to Xiaomi or a reseller quoting *above* the card — $0.47/$0.94 and $2.17/$4.35 at the two independents [^15]. There is no quote below Xiaomi's, because there is no one else running the weights. A single-seller price has no arbitrage floor. It is whatever the seller posted on the morning of measurement.

Xiaomi demonstrates the discretion directly by selling the same checkpoint at two prices. MiMo-V2.6-Pro lists $0.435/$0.87 per million tokens; MiMo-V2.6-Pro-UltraSpeed, which Xiaomi's own release notes describe as a *mode* of MiMo-V2.6-Pro rather than a different model, lists $4.35/$8.70 — exactly 10× — and publishes no rate limits at all, where Pro publishes RPM 100 and TPM 10M [^9][^17][^36]. Applying Artificial Analysis' own arithmetic to the UltraSpeed card yields roughly $1.33 per Index task instead of $0.13 [^9]. In fairness the two tiers are not an arbitrary relabel: UltraSpeed advertises up to 20× the output speed [^9], so the buyer gets a materially different service level. But the capability being scored is the same, and the number the index reports is the cheaper tier's.

### The weights transfer; the price does not

The following is this article's derivation over cited inputs, not a vendor figure.

:::kv
- {term: "Weights at FP8 (1.02T params × 1 byte)", def: "1.02 TB resident"}
- {term: "Floor at 80 GB/H100, before any KV cache", def: "13 GPUs"}
- {term: "Xiaomi reference topology (SGLang, 2 nodes, tp 16)", def: "16 GPUs"}
- {term: "Median Vast.ai H100 SXM, 22 Sep 2026", def: "$2.40 per GPU-hour, so $38.40 per hour for 16"}
- {term: "Artificial Analysis measured single-stream output", def: "76.2 tokens/s, so 0.274M tokens per hour"}
- {term: "Derived single-stream cost", def: "about $140 per 1M output tokens"}
- {term: "Versus Xiaomi list of $0.87 per 1M", def: "about 161 times"}
:::

The parameter count is 1.02T total with 42B active across 384 routed experts [^10]; mixture-of-experts sparsity cuts arithmetic, not residency, so all 1.02 TB must sit in high-bandwidth memory. Xiaomi's published launch command specifies sixteen GPUs across two nodes, and Xiaomi publishes no GPU model and no VRAM requirement [^10]. Spot rates come from Vast.ai as of 22 September 2026: H100 SXM median $2.4002 per GPU-hour, H200 $4.3428, B200 $8.7526 [^11]. Repricing Artificial Analysis' run at the derived $140 per million tokens produces on the order of $19,600 instead of $206.66, or about $12 per task instead of $0.13 [^7]. Break-even against the $0.87 card requires roughly 12,300 sustained output tokens per second on that same cluster.

:::note
This is the single-stream worst case and should be read as a bound, not a forecast. Batching closes most of the gap: at the concurrency Xiaomi's own reference configuration is built for, the multiple would fall to low single digits. That order-of-magnitude estimate is this article's, not a measured figure, and no independent throughput benchmark for MiMo-V2.6-Pro exists to check it against. The direction is the point — the gap is a function of utilisation, which is a function of demand volume, which open weights do not confer.
:::

### The subsidy hypothesis mostly fails

The obvious reading — that Xiaomi is dumping — does not survive the disclosed numbers. DeepSeek published one 24-hour window at 226.75 average nodes of eight H800s costing $87,072 against $562,027 of theoretical revenue, a 545% cost-profit margin, which is a 6.45× revenue-to-cost ratio and an 84.5% gross margin — a markup routinely miscompared to a margin [^12]. DeepSeek itself caveats that actual revenue was substantially lower because V3 is priced below R1, web and app access remain free, and nighttime discounts apply [^12]. Separately, DeepSeek V4-Pro is listed with 71 providers, among them NVIDIA, Hugging Face, ZenMux and TokenGo, at the same $0.43/$0.87 [^15] — unaffiliated commercial hosts with no incentive to subsidise a Chinese lab, quoting a large mixture-of-experts model in the same price band. And Z.AI's interim results show gross margin moving from −0.4% to +24.6% while average API selling price rose approximately 101% — margin recovered by raising prices, not by deepening a discount, against R&D of RMB 2,131.2m and a net loss of RMB 2,072.0m [^13]. Xiaomi's own account is consistent and should be read as a vendor claim: Luo Fuli said the MiMo team can "basically still maintain break-even," that pricing "naturally leaves 2 to 3× profit headroom," and that Xiaomi "decided to pass these structural cost advantages straight to developers" [^14].

So the honest reading is that $0.13 is plausibly above marginal cost at scale. What the open weights fail to transfer is not the price but the *scale* required to reach it — continuous datacenter-grade concurrency on sixteen-GPU units, which is capital structure, not a checkpoint.

One falsifiable test is already running. MiMo-V2.6-Pro had zero third-party hosts two days after release, while the prior generation has seven [^8]. Re-check at thirty days: if independents are still absent, absence stops being latency and becomes evidence about whether the price is replicable.

This matters because the composite reports $0.13 in the same row as 46, inviting readers to treat both as measurements of the artefact — when one is a benchmark result and the other is a pricing decision by the only entity currently permitted to make it.

## 06. What $2.62 million bought

The $2.62 million is the price of six days of reinforcement learning applied to a base model Xiaomi has not described, on hardware Xiaomi has not named — a marginal cost of the last mile that is being read, downstream, as the cost of the model.

:::stats
- {label: "RL cost, MiMo-V2.6-Pro", value: $2.62M, note: "Flash: $854K; disclosed by Xiaomi"}
- {label: "Training steps", value: 30, note: "Pro run restarted at step 17 after a GPU OOM"}
- {label: "Trajectories", value: "~750K", note: "Both models, cumulative"}
- {label: "Wall clock", value: "<6 days", note: "Started 2026-09-15 10:32 UTC; stopped 2026-09-20"}
- {label: "Pretraining cost", value: "undisclosed", note: "V2-Flash's predecessor run used 27T tokens"}
- {label: "Base checkpoints released", value: 0, note: "V2.5, V2.5-Pro and V2-Flash all shipped -Base repos"}
:::

Xiaomi's own words scope the number precisely: "in less than 6 days, MiMo-V2.6-Flash and MiMo-V2.6-Pro completed 30 steps each with a cumulative total of approximately 750,000 trajectories, at training costs of around 850,000 and 2.62 million US dollars respectively" [^17]. The live dashboard puts the Pro run at $2,620,670 and splits it 43.5% training, 43.8% rollout generation, 12.7% grading [^18]. That split is itself a tell: fewer than half of the dollars are gradient updates, because a reinforcement-learning bill is dominated by generating and scoring trajectories against the 7,000-plus task environments Xiaomi built [^17]. A pretraining bill has no such shape, and none was published.

What the figure excludes is larger than what it includes. The model card reports 1.02 trillion total parameters, 42 billion active and 384 routed experts [^10]; the predecessor V2-Flash was pretrained on 27 trillion tokens [^19], and nothing in Xiaomi's V2.6 materials puts a cost on whatever pretraining run this generation sits on. Xiaomi has disclosed no cost basis whatsoever for any of it — no GPU model, no chip count, no GPU-hours, no assumed hourly rate [^17]. And for the first time in the series, no base checkpoint was released: V2.5, V2.5-Pro and V2-Flash all shipped base repositories, and the V2.6 generation published only reinforcement-learned checkpoints and a 9B distill [^57]. The thing the $2.62 million was spent *on top of* is the one artefact nobody outside Xiaomi can inspect or re-run.

The industry has made this exact error before, and with better excuse. DeepSeek-V3's technical report gave 2,664K H800 GPU-hours of pre-training, 119K for context extension, 5K for post-training, 2,788K total, priced at an assumed $2 per GPU-hour for $5.576 million — with the explicit caveat that the costs "include only the official training of DeepSeek-V3, excluding the costs associated with prior research and ablation experiments on architectures, algorithms, or data" [^20]. The structural difference is worth stating plainly: DeepSeek disclosed the full training stack in GPU-hours on named silicon and excluded only research overhead, then converted at a price it assumed; Xiaomi disclosed a dollar figure for one post-training stage, excluded the entire pretraining run, and named no hardware at all [^17][^20]. Xiaomi flags the gap in the same announcement — "behind these 6 days lie half a year of foundational research accumulation and engineering trial and error" [^17] — and Luo Fuli, who leads MiMo, describes "a team of several dozen people" working through an era "when compute is brutally scarce" [^22]. Neither the half-year nor the several dozen people are in the $2.62 million.

Scale sharpens the point. Xiaomi reported FY2025 R&D expenses of RMB 33,132.2 million against revenue of RMB 457,286.7 million, with 25,457 R&D personnel [^21]. Spread evenly across the 8,760 hours in a year, that is roughly RMB 3.78 million per hour. At an assumed exchange rate of about 7.1 yuan to the dollar — an estimate here, not a Xiaomi figure — the $2.62 million run is roughly RMB 18.6 million, or about five hours of the company's average FY2025 research burn; both V2.6 runs together come to about six and a half hours [^21][^18].

:::iso
- {label: "MiMo-V2.6-Pro RL run", glyph: "🕐", count: 5}
- {label: "One day of Xiaomi FY2025 R&D", glyph: "🕐", count: 24}
:::

That comparison does not mean the model was cheap. It means the published number is not the expensive part. The expensive parts — a multi-trillion-token pretraining run, the fleet it ran on, and the half-year Xiaomi itself references — are precisely the parts left undisclosed [^19][^17].

:::source
The step count, trajectory count, dollar totals and cost split are Xiaomi's own, from the release notes [^17] and the live training dashboard as rendered on 23 September 2026 [^18]. The dashboard is a live client-rendered application and its figures could not be independently re-retrieved at the time of writing; treat the run-level detail as first-party and unaudited.
:::

Xiaomi's filings offer no help: there is no AI-specific R&D line, no AI capital-expenditure line, no GPU fleet count, and no standalone MiMo revenue anywhere, only a forward commitment that cumulative 2026–2030 R&D "will exceed RMB200 billion" [^21].

The counterpoint deserves its full weight: Xiaomi's disclosure is materially better than the industry norm, not worse. It ran a public cost dashboard *during* the run, named step and trajectory counts, published the data mix and the fact that the Pro run restarted at step 17 after a GPU out-of-memory event, acknowledged the uncosted half-year in the announcement itself, and — unlike almost every lab quoting a training cost — released the weights under an MIT tag [^10][^17][^18]. The category error is downstream, in coverage that compresses "$2.62 million of reinforcement learning" into "a frontier model for $3 million."

:::callout(kind=warn, label=Attribution)
The widely repeated line that MiMo was trained "entirely on Chinese chips rather than Nvidia GPUs" traces to a named outside commenter, Daanish Khazi, not to Xiaomi [^22]. Xiaomi has disclosed no training hardware of any kind [^17]. The export-control reading is also a non-sequitur on its own terms: a six-day post-training run says almost nothing about the pretraining compute that controls actually target, even against a backdrop where NVIDIA told the SEC it was "effectively foreclosed from competing in China's data center computing/compute market" as of fiscal 2026 [^23].
:::

This matters because a cost figure is only as useful as its scope, and a scope this narrow cannot support the inference — about efficiency frontiers, about export controls, or about what a 46 on the index costs to produce — that the number is currently being asked to carry.

## 07. The audit nobody can run

The contamination question about MiMo-V2.6-Pro is not answerable in either direction today, because the artefact that would settle it — the reinforcement-learning task corpus — was announced and not shipped, and the strongest interpretable signal in the release turns out to be Xiaomi's own benchmark table rather than any accusation made against it.

Xiaomi's V2.6 announcement describes "7k+ high-quality RL task environments" spanning software engineering, vulnerability reproduction, knowledge-intensive work and web design [^17]. Those environments are the object an overlap computation would need: the check that matters is not whether Artificial Analysis' questions appeared in pretraining text, but whether the rollouts were built from the same repositories, issues and artefacts the evaluations are drawn from. As of 22 September 2026 the corpus was not public — "the complete 7k+ task datasets have not yet been released" [^25] — and inspection of the XiaomiMiMo GitHub organisation on 23 September 2026 found 18 repositories — among them a `verl` fork carrying four recipe directories, `uni-agent`, `mimoagent`, `MiMo-Code`, `MiMo-Skills` and a `vllm` fork — with no reinforcement-learning environment dataset repository among them [^26]. What is open is the harness and the recipes; the task corpus is the part that is closed [^25]. The overlap computation nobody has run is therefore also the one nobody outside Xiaomi can run.

The predecessor pipeline suggests what the corpus is made of. The MiMo-V2-Flash technical report describes over 100,000 code tasks derived from real-world GitHub issues, roughly 120K containerised environments in rollout, and more than 10,000 concurrent Kubernetes pods [^19]. The only filtering it documents removes tasks with unreliable correctness judgments or insufficient complexity for effective RL training — a difficulty filter, not an overlap check [^19]. Searching four Xiaomi surfaces (that report, the V2.6 announcement, the V2.6 model card, and the V2.6 technical report listing) returned zero hits for decontamination, contamination, n-gram, overlap, held-out, leakage, or excluded repositories. That is absence of found evidence across named surfaces, not proven absence: the 44-page V2.6 technical report body could not be retrieved, and a decontamination protocol may well be described inside it.

Why the RL-environment shape matters specifically: Cursor's sealed-container re-run of SWE-bench Pro removed runtime git-history leakage and found Opus 4.6 moved less than a point while Opus 4.8 Max fell 14.1 and Composer 2.5 fell 20.7, with 63% of Opus 4.8 Max's successes retrieved rather than derived [^30]. That is a vendor blog whose own flagship shows the largest drop, and it measures runtime environment leakage rather than training contamination — a third mechanism, distinct from both. It is cited here only because it is the mechanism structurally closest to reinforcement-learning environments built from live repositories.

### The table Xiaomi published itself

| Benchmark | MiMo-V2.6-Pro | Claude Opus 5 | Delta |
|---|---|---|---|
| Terminal-Bench 2.1 | 89.9 | 89.1 | +0.8 |
| *Terminal-Bench 4.0 | 34.9 | 49.0 | −14.1 |

A 14.9-point relative swing between two versions of the same benchmark family, both legs run on Xiaomi's own harness [^10]. Terminal-Bench 4.0 is a 66-task set [^6] built by removing tasks that were saturated, refusal-prone, publicly solved, or affected by unresolved quality issues [^24]. Terminal-Bench's own release notes carry the objection that matters most here: the update "included resource changes in the agent environment" as well as a new task set [^24]. A cross-version delta therefore mixes genuine capability change with protocol change, and is not a clean contamination readout. Terminal-Bench 2.1 is also close to saturated — every model in Xiaomi's own table sits between 65 and 90 on it [^10] — which compresses any real gap on that leg toward zero.

What makes the card credible rather than promotional cuts the other way: MiMo-V2.6-Pro loses to Claude Opus 5 on 10 of the 14 rows where both are scored, including DeepSWE v1.1 (71.9 against 74.0), Toolathlon-Verified (76.9 against 80.6) and OSWorld-Verified (82.0 against 83.4) [^10]. The card's real weaknesses are structural, not directional: CyberGym is reported at 94.0 with no competitor column, three in-house benchmarks carry no external baseline, and no row is annotated to distinguish Xiaomi-run scores from cited ones [^10].

:::bars
- {label: AutomationBench-AA, value: "14% → 59%", pct: 59}
- {label: Terminal-Bench 4.0, value: "0% → 35%", pct: 35}
- {label: CritPt, value: "4% → 27%", pct: 27}
- {label: GDP.pdf, value: "4% → 19%", pct: 19}
- {label: SciCode, value: "51% → 61%", pct: 61}
- {label: AA-LCR, value: "80% → 86%", pct: 86}
:::

These are MiMo-V2.5-Pro to MiMo-V2.6-Pro, both measured under Intelligence Index v4.3.2, so they are directly comparable [^31]. The anomalous movements are the ones left out of the chart: HLE 36 to 49 and AA-Omniscience 3 to 8 are knowledge evaluations, and the disclosed RL data mix was 65.8% code, 19.5% visual, 11.3% general, 3.4% chat, 0.0% cyber — with no knowledge category at all [^18]. Knowledge gains from a code-dominated reinforcement-learning stage require an explanation the release does not supply.

Artificial Analysis offers a partial control: evaluations with private questions or answers account for 45% of Intelligence Index v4.3's weighting, up from 40% in v4.2 [^6][^27]. That number needs unpacking, because "private" conflates two different defences — private *questions* (AA-Briefcase, AA-Omniscience, AutomationBench-AA), which resist ingestion, with public questions plus a private *answer key* (CritPt), which do not [^6]. Separately, none of AIME, GPQA-Diamond, MMLU-Pro, LiveCodeBench or SWE-bench — the benchmarks contamination arguments usually target — are in v4.3.2 at all [^4].

Two constraints keep this from becoming an accusation. First, the contamination discount is not transferable. GSM1k found gaps of −8.0 for Yi-6B-Chat, −7.2 for math-shepherd-mistral-7b and −6.3 for phi-2, but −0.2 for gpt-4o, +2.2 for claude-3-opus and +3.8 for gemini-1.5-flash, concluding that "all frontier or close-to-frontier models... appear to perform similarly on both GSM8k and GSM1k" [^28]. A 2026 benchmark-renewal study that rewrote AIME under executable specifications found 16 models falling a mean 14.2 points on the 2024 contest set under the rewrite [^29] — and the part of that drop attributable to memorisation rather than to the rewrite's added difficulty is a fraction of it, not the whole. Applying a double-digit haircut to MiMo by analogy would be unjustified.

Second, a rival hypothesis fits the evidence better. Xiaomi's own card discloses a post-RL stage named "Multi-Prefix Multi-Teacher On-Policy Distillation (MOPD2)" and does not name the teacher models [^10]. Distillation from a stronger teacher predicts rank-consistent performance on private evaluations, which is roughly what the thin private-suite evidence shows; contamination predicts a private-eval collapse, which has not been observed [^31]. Neither is established, and the release as shipped cannot distinguish them.

:::callout(kind=warn, label=Unverified)
The distillation claim that circulated is not the one on the model card. A single Hacker News comment on 17 September 2026 quoted a `"Claude Distill Requests":'hidden'` line as an item from Xiaomi's training dashboard, with no screenshot, no field path, and quoting that is not valid JSON; the thread responded with jokes, and a full live render of the dashboard on 23 September 2026 contained no occurrence of "Distill", "Claude" or "hidden" [^32]. No transcript of MiMo self-identifying as another lab's model was found, and Xiaomi has issued no denial because no one appears to have asked [^32]. The thin, joke-shaped claim travelled; the first-party, unnamed-teacher disclosure sitting on Xiaomi's own model card did not [^10].
:::

This matters because an unpublished task corpus converts a testable empirical question into an unfalsifiable one, and an index score computed on top of it inherits that status silently.

## 08. What has not been measured

Two days after release, the Artificial Analysis 46 had zero corroboration from any independent evaluator, and the axes Xiaomi most differentiates on had none at all.

The only other third-party number in existence is an Arena AutoEval score of 1628 on Code Arena — explicitly unranked, with zero human votes [^39]. Arena is candid about what that means: AutoEval substitutes a reward model's proxy votes for human ones, achieves above 90% pairwise accuracy only when the true gap exceeds ten points, and treats models within five points as statistically indistinguishable [^40]. It is a second automated composite, not an independent check on the first. On the board that does carry human volume, MiMo-V2.6-Pro is absent and the prior generation sits at rank 44 with 60,919 votes [^50].

| Evaluator | MiMo-V2.6-Pro | Note (as of 23 Sep 2026) |
|---|---|---|
| Artificial Analysis Intelligence Index | 46 | The only independent score in existence |
| Arena Code Arena | 1628, unranked | AutoEval proxy, zero human votes [^39] |
| Arena Text Arena | absent | V2.5-Pro at rank 44, 60,919 votes [^50] |
| *Vals.ai | absent (HTTP 404) | Evaluated Grok 4.7 on its release day [^41] |
| SWE-rebench | absent | Latest decontaminated evaluation window closes 1 July 2026 [^43] |
| MMMU-Pro | absent | No MiMo generation listed [^2] |
| Aider polyglot | absent | Board not updated since late 2025, so absence carries no signal |

Several of those absences are schedule, not verdict: the model is two days old, and a monthly-refresh decontaminated benchmark cannot have spoken yet. But the absence is the honest description of the present state, and it has a direction. The one private-suite result that exists points the other way from the index. A named practitioner running a personal held-out suite reported MiMo-V2.6-Pro at 38.8 against Claude Opus 5's 66.9 and GPT-6 Astra's 57.9 [^42] — a spread far wider than the single-digit gap the Intelligence Index puts between MiMo and the same models [^7]. A separate structured hands-on found MiMo matching Claude Opus 5 at 23 of 23 hidden checks across three small scoped coding tasks at roughly a thirtieth of the cost [^54].

:::compare
- {role: LOWEST, name: "MiMo-V2.6-Pro", value: 38.8}
- {role: HIGHEST, name: "Claude Opus 5", value: 66.9}
- {role: SUBJECT, name: "MiMo-V2.6-Pro", value: 38.8}
:::

:::source
One practitioner's private held-out suite, reported on Hacker News, 22 September 2026 [^42]. Neither methodology, task count, nor error bars are published, and the model was served through default OpenRouter routing rather than the UltraSpeed endpoint. Treat as a single low-confidence datapoint pointing away from the index, not as a refutation of it.
:::

Two capability axes are not merely unmeasured by third parties but structurally outside the index. MiMo-V2.6-Pro accepts text, image, audio and video [^10]; Intelligence Index v4.3.2 is text-only, and Artificial Analysis scores image, speech and multilingual performance in separate tracks that MiMo does not yet appear in [^4][^2]. The capability Xiaomi differentiates hardest on is invisible to the number being quoted about it. The same holds for context. MiMo advertises a one-million-token window, and 60 of its 70 layers use sliding-window attention with a 128-token window [^10]; the index's only long-context constituent is 100 questions over documents capped at 100,000 tokens, carrying 5% of the weight [^4]. The independent literature on this gap is unambiguous in direction if not in magnitude: NoLiMa tested 13 models all claiming at least 128k context and found 11 of them dropping below half their short-length baseline by 32k [^51]. No NoLiMa, RULER or equivalent result exists for MiMo-V2.6-Pro.

What would weaken this section: two days is a genuinely short window, and treating a leaderboard's silence as a signal is exactly the error this article accuses others of making in the other direction. The correct reading is not "MiMo is worse than 46 suggests." It is that on 23 September 2026 the claim rests on one evaluator, and the standard for a result this widely repeated should be higher than that.

This matters because corroboration is what converts a score into evidence, and the interval between a launch and its corroboration is exactly when the score does most of its travelling.

## 09. What would falsify this

The strongest case against this article's framing is that composites work, and there is real evidence for it.

A confirmatory factor analysis across 591 language models and 12 tests found evidence of interrelated, cognitive-like capabilities loading on a single dominant factor — reported at an average loading of 0.81, explaining 65.6% of benchmark variance, with a mean inter-test correlation of 0.73 [^55]. If constituents are that collinear, an equal-weighted mean is a legitimate estimator of a real latent trait, weighting choices matter less than they appear to, and aggregation genuinely averages down per-benchmark noise and gaming. Artificial Analysis also has a validity credential few evaluators can match: in September 2024 it independently evaluated Reflection-70B, could not reproduce its claimed results even with private API access, and was the instrument through which an inflated open-weights claim collapsed [^45]. The critique in this article is aimed at the aggregation and versioning layers, not at Artificial Analysis' execution discipline, which is good.

Three further points cut in MiMo's favour and should not be lost in the audit. The 26-to-46 generational gain is measured on a single instrument version and is real [^31]. Xiaomi published the weights, the harness, the recipes, a live cost dashboard and a failed step, which is more than most labs disclose about a model they will never let anyone run [^10][^18]. And the Llama 4 Maverick precedent — a model advertised at rank 2 on LMArena via an experimental chat variant, then ranking 32nd when the released weights were scored [^44] — is a precedent about *not disclosing which artefact was evaluated*. MiMo's evaluated artefact is public. That specific failure mode is closed here.

:::statement(attr="ARA Research")
The index settles that an MIT-licensed model built by a handset company reached the same composite as a US frontier release. It does not settle that they are substitutes, that the gap is measurable, that the price is portable, or that any of it can be compared to last month.
:::

An adversarial pass over this article's three most load-bearing claims — the cluster-aligned constituent split, the Grok 4.6 rebase from 61 to 44, and the single-seller reading of $0.13 — found no contradicting source for any of the three. The rebase was the closest call: Artificial Analysis' changelog renders Grok 4.6 at 44 *under its 12 August entry*, which reads at first as a contradiction of the 61 published that day, until the dated article is checked and still says 61. That the changelog re-renders current scores against historical dates is not a counterexample to this section's argument; it is the argument. Three of three surviving is a real signal, and a bounded one: no adversarial pass can search what search engines will not return, and archive.org was unreachable from this environment.

Four tests would move this analysis, each with a date attached:

1. **LMArena human votes.** Human preference is close to impossible to encode in a reinforcement-learning environment. If MiMo-V2.6-Pro accumulates real votes and lands near its index rank, the contamination hypothesis weakens sharply. If it lands where MiMo-V2.5-Pro did — rank 44 [^50] — the index is measuring something narrow.
2. **The next decontaminated software-engineering benchmark window.** SWE-rebench builds its task sets from repository activity inside a dated window, and its latest closed on 1 July 2026 [^43]. The first window that opens after 21 September is the instrument most likely to catch exactly the overlap this release made unauditable.
3. **Third-party hosts at thirty days.** Zero independents serve MiMo-V2.6-Pro today; seven serve the prior generation [^8]. Persistent absence at T+30 would say something real about whether $0.13 is replicable.
4. **The V2.6 technical report body and the RL task corpus.** Publishing the 7,000 environments would convert the contamination question from unfalsifiable back to testable in a single commit [^17][^25].

There is also a structural caveat this article cannot resolve and should name. Adoption and benchmark rank are close to disjoint. OpenRouter's request share for the week beginning 14 September 2026 put DeepSeek at 25.4%, Google at 18.6% and Anthropic at 2.7% [^46], against an index top ten dominated by Anthropic and OpenAI; OpenRouter itself states that its rankings "measure adoption, not quality." Menlo Ventures separately puts DeepSeek — the most-used Chinese open-weight family — at just 1% of enterprise LLM API usage, against 13% for open source as a whole [^47]. Whatever a 46 means, it is not currently what determines where tokens go.

Finally, the deflation frame deserves a caution the coverage has not given it. Epoch AI's canonical measurement of inference-price decline — 9× to 900× per year depending on the capability milestone — is denominated per token at a fixed benchmark score, and says nothing about tokens consumed per task [^49]. A 2026 hedonic price index built from 21,024 posted prices across 3,208 models finds that a conventional matched-model measure records a decline of about 0.10 log points per year while a quality-adjusted index records 0.73 — so roughly 87% of the decline is invisible to standard methods, and the paper's separate finding is that counted per completed task the buyer's price stopped falling, because reasoning models raised token consumption faster than token prices fell [^48]. It is a single-author preprint and its task-denominated estimate carries a confidence interval that spans zero, so it establishes a divergence between the two units rather than a flat task price. That is the honest state of the art: per-token intelligence is getting cheaper fast, per-task intelligence may not be, and a single $0.13 measured fifteen days after the instrument changed cannot adjudicate between them.

:::references
- {id: 1, title: "MiMo-V2.6-Pro vs Grok 4.7 — model comparison", url: "https://artificialanalysis.ai/models/comparisons/mimo-v2-6-pro-vs-grok-4-7", source: Artificial Analysis, date: "2026-09-23"}
- {id: 2, title: "AA-Omniscience evaluation leaderboard", url: "https://artificialanalysis.ai/evaluations/omniscience", source: Artificial Analysis, date: "2026-09-23"}
- {id: 3, title: "Benchmarking Grok 4.7", url: "https://artificialanalysis.ai/articles/benchmarking-grok-4-7", source: Artificial Analysis, date: "2026-09-21"}
- {id: 4, title: "Intelligence benchmarking methodology (Index v4.3.2)", url: "https://artificialanalysis.ai/methodology/intelligence-benchmarking", source: Artificial Analysis, date: "2026-09-19"}
- {id: 5, title: "Artificial Analysis Long Context Reasoning (AA-LCR) leaderboard", url: "https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning", source: Artificial Analysis, date: "2026-09-23"}
- {id: 6, title: "Artificial Analysis Intelligence Index v4.3", url: "https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-3", source: Artificial Analysis, date: "2026-09-07"}
- {id: 7, title: "MiMo-V2.6-Pro — intelligence, performance and price analysis", url: "https://artificialanalysis.ai/models/mimo-v2-6-pro", source: Artificial Analysis, date: "2026-09-23"}
- {id: 8, title: "OpenRouter endpoints API — xiaomi/mimo-v2.6-pro", url: "https://openrouter.ai/api/v1/models/xiaomi/mimo-v2.6-pro/endpoints", source: OpenRouter, date: "2026-09-23"}
- {id: 9, title: "MiMo-V2.6-Pro-UltraSpeed model and pricing page", url: "https://mimo.mi.com/models/en-US/mimo-v2.6-pro-ultraspeed", source: Xiaomi, date: "2026-09-23"}
- {id: 10, title: "XiaomiMiMo/MiMo-V2.6-Pro-RL model card", url: "https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL", source: Hugging Face, date: "2026-09-21"}
- {id: 11, title: "research/market/gpu-spot.json — Vast.ai USD per GPU-hour", url: "https://github.com/guzus/ai-research-arm/blob/main/research/market/gpu-spot.json", source: ARA repository, date: "2026-09-22"}
- {id: 52, title: "research/market/model-pricing.json — frontier price at capability tier", url: "https://github.com/guzus/ai-research-arm/blob/main/research/market/model-pricing.json", source: ARA repository, date: "2026-09-22"}
- {id: 12, title: "DeepSeek-V3/R1 inference system overview", url: "https://github.com/deepseek-ai/open-infra-index/blob/main/202502OpenSourceWeek/day_6_one_more_thing_deepseekV3R1_inference_system_overview.md", source: DeepSeek, date: "2025-03-01"}
- {id: 13, title: "Z.AI Co., Ltd. interim results (HKEX 2513)", url: "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0831/2026083101539.pdf", source: HKEXnews, date: "2026-08-31"}
- {id: 14, title: "Luo Fuli on the MiMo-V2.5 price cut", url: "https://www.ithome.com/0/956/280.htm", source: IT之家, date: "2026-05-28"}
- {id: 15, title: "DeepSeek V4-Pro provider and price listing", url: "https://models.dev/models/deepseek/deepseek-v4-pro/", source: models.dev, date: "2026-09-23"}
- {id: 16, title: "Grok 4.7 — intelligence, performance and price analysis", url: "https://artificialanalysis.ai/models/grok-4-7", source: Artificial Analysis, date: "2026-09-23"}
- {id: 17, title: "MiMo-V2.6 series release notes", url: "https://mimo.mi.com/docs/en-US/news/latest/v2-6", source: Xiaomi, date: "2026-09-22"}
- {id: 18, title: "MiMo live reinforcement-learning dashboard", url: "https://mimo.xiaomi.com/rl/", source: Xiaomi, date: "2026-09-23"}
- {id: 19, title: "MiMo-V2-Flash technical report", url: "https://arxiv.org/abs/2601.02780", source: arXiv, date: "2026-01-06"}
- {id: 20, title: "DeepSeek-V3 technical report", url: "https://arxiv.org/html/2412.19437v2", source: arXiv, date: "2024-12-26"}
- {id: 21, title: "Xiaomi Corporation FY2025 annual results announcement", url: "https://ir.mi.com/system/files-encrypted/nasdaq_kms/assets/2026/03/24/5-35-03/25Q4%20EN%20AC%20Xiaomi.pdf", source: Xiaomi Investor Relations, date: "2026-03-24"}
- {id: 22, title: "Xiaomi's MiMo-V2.6-Pro debuts as the top open weights model", url: "https://venturebeat.com/technology/better-than-deepseek-xiaomis-mimo-v2-6-pro-debuts-as-the-top-open-weights-model-in-the-world-alongside-cheaper-v2-6-flash", source: VentureBeat, date: "2026-09-21"}
- {id: 23, title: "NVIDIA Corporation Form 10-K, fiscal year 2026", url: "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm", source: SEC EDGAR, date: "2026-02-25"}
- {id: 24, title: "Terminal-Bench 4.0 release notes", url: "https://www.tbench.ai/news/terminal-bench-4-0", source: Terminal-Bench, date: "2026-08-26"}
- {id: 25, title: "AINews — Xiaomi MiMo-V2.6-Pro 1T-A42B", url: "https://www.latent.space/p/ainews-xiaomi-mimo-v26-pro-1t-a42b", source: Latent Space, date: "2026-09-22"}
- {id: 26, title: "XiaomiMiMo GitHub organisation repositories", url: "https://github.com/XiaomiMiMo", source: GitHub, date: "2026-09-23"}
- {id: 27, title: "Artificial Analysis Intelligence Index v4.2", url: "https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-2", source: Artificial Analysis, date: "2026-09-04"}
- {id: 28, title: "A Careful Examination of Large Language Model Performance on Grade School Arithmetic (GSM1k)", url: "https://ar5iv.labs.arxiv.org/html/2405.00332", source: arXiv, date: "2024-05-01"}
- {id: 29, title: "VeRA: Renewing Reasoning Benchmarks with Executable Specifications", url: "https://arxiv.org/abs/2602.13217", source: arXiv, date: "2026-01-23"}
- {id: 30, title: "Reward hacking in coding benchmarks", url: "https://cursor.com/blog/reward-hacking-coding-benchmarks", source: Cursor, date: "2026-06-25"}
- {id: 31, title: "MiMo-V2.5-Pro vs MiMo-V2.6-Pro — model comparison", url: "https://artificialanalysis.ai/models/comparisons/mimo-v2-5-pro-vs-mimo-v2-6-pro", source: Artificial Analysis, date: "2026-09-23"}
- {id: 32, title: "Hacker News discussion of the MiMo training dashboard", url: "https://news.ycombinator.com/item?id=49738573", source: Hacker News, date: "2026-09-17"}
- {id: 33, title: "Artificial Analysis changelog", url: "https://artificialanalysis.ai/changelog", source: Artificial Analysis, date: "2026-09-19"}
- {id: 34, title: "Grok 4.6 benchmarks and analysis", url: "https://artificialanalysis.ai/articles/grok-4-6-benchmarks-and-analysis", source: Artificial Analysis, date: "2026-08-12"}
- {id: 35, title: "Grok 4.6 — intelligence, performance and price analysis", url: "https://artificialanalysis.ai/models/grok-4-6", source: Artificial Analysis, date: "2026-09-23"}
- {id: 36, title: "MiMo-V2.6-Pro model page", url: "https://mimo.mi.com/models/en-US/mimo-v2.6-pro", source: Xiaomi, date: "2026-09-21"}
- {id: 37, title: "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations", url: "https://arxiv.org/abs/2411.00640", source: arXiv, date: "2024-11-01"}
- {id: 55, title: "Evidence of interrelated cognitive-like capabilities in large language models", url: "https://arxiv.org/abs/2310.11616", source: "arXiv / Intelligence 106:101858", date: "2023-10-17"}
- {id: 56, title: "Grok 4.7 (high) — intelligence, performance and price analysis", url: "https://artificialanalysis.ai/models/grok-4-7-high", source: Artificial Analysis, date: "2026-09-23"}
- {id: 57, title: "XiaomiMiMo model repositories", url: "https://huggingface.co/XiaomiMiMo", source: Hugging Face, date: "2026-09-23"}
- {id: 38, title: "Humanity's Last Exam benchmark review", url: "https://epoch.ai/benchmarks/hle/review", source: Epoch AI, date: "2026-08-11"}
- {id: 39, title: "Arena Code Arena leaderboard", url: "https://arena.ai/leaderboard/code", source: Arena, date: "2026-09-23"}
- {id: 40, title: "AutoEval scores — methodology", url: "https://arena.ai/blog/autoeval-scores", source: Arena, date: "2026-09-23"}
- {id: 41, title: "Vals Index and model evaluations", url: "https://www.vals.ai/home", source: Vals AI, date: "2026-09-23"}
- {id: 42, title: "Hacker News discussion of MiMo-V2.6-Pro's Artificial Analysis result", url: "https://news.ycombinator.com/item?id=49796660", source: Hacker News, date: "2026-09-22"}
- {id: 43, title: "SWE-rebench decontaminated SWE leaderboard", url: "https://swe-rebench.com/", source: SWE-rebench, date: "2026-09-23"}
- {id: 44, title: "Meta's vanilla Maverick AI model ranks below rivals on a popular chat benchmark", url: "https://techcrunch.com/2025/04/11/metas-vanilla-maverick-ai-model-ranks-below-rivals-on-a-popular-chat-benchmark", source: TechCrunch, date: "2025-04-11"}
- {id: 45, title: "New open source AI leader Reflection 70B's performance questioned", url: "https://venturebeat.com/ai/new-open-source-ai-leader-reflection-70bs-performance-questioned-accused-of-fraud", source: VentureBeat, date: "2024-09-09"}
- {id: 46, title: "OpenRouter model rankings", url: "https://openrouter.ai/rankings", source: OpenRouter, date: "2026-09-21"}
- {id: 47, title: "2025 mid-year LLM market update", url: "https://menlovc.com/perspective/2025-mid-year-llm-market-update/", source: Menlo Ventures, date: "2025-07-31"}
- {id: 48, title: "The Price of Intelligence: A Quality-Adjusted Price Index for AI Services", url: "https://arxiv.org/abs/2608.29843", source: arXiv, date: "2026-08-30"}
- {id: 49, title: "LLM inference price trends", url: "https://epoch.ai/data-insights/llm-inference-price-trends", source: Epoch AI, date: "2025-03-12"}
- {id: 50, title: "Arena Text Arena leaderboard", url: "https://arena.ai/leaderboard/text/", source: Arena, date: "2026-09-23"}
- {id: 51, title: "NoLiMa: Long-Context Evaluation Beyond Literal Matching", url: "https://arxiv.org/abs/2502.05167", source: arXiv, date: "2025-07-09"}
- {id: 53, title: "Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design", url: "https://arxiv.org/abs/2310.11324", source: arXiv, date: "2023-10-17"}
- {id: 54, title: "MiMo-V2.6-Pro benchmarks and hands-on test vs Claude Opus 5", url: "https://kingy.ai/blog/mimo-v2-6-pro-benchmarks-specs-comparison/", source: Kingy AI, date: "2026-09-22"}
:::
