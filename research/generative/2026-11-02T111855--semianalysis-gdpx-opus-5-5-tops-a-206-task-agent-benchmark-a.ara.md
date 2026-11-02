---
eyebrow: AI EVALUATION · BENCHMARK ANALYSIS
title: "GDPx's 12% crown: Opus 5.5 leads SemiAnalysis's agent benchmark, but weighting, refusals and cost per task decide who wins"
deck: "A 206-task, 11-domain test with real headroom, scored so that one-point gaps fit inside the error bars and a different domain mix changes the leader."
domain: general
lede: |
  On November 2, 2026, SemiAnalysis published GDPx, an agentic benchmark of 206 long-horizon tasks across 11 professional domains, and put Claude Opus 5.5 at the top with 12.0. Gemini 4 Carbon followed at 10.9 and GPT-6 Astra at 9.6. Three of the benchmark's own design choices weaken the "Opus wins" headline: every domain counts equally however many tasks it has, safety classifiers are scored as failures, and cost per task is reported but kept out of the score. Remove three domains and Astra leads by a tenth of a point. Price the results and Carbon gets 91% of Opus's score for 32% of the cost. Run the statistics and the top three are not reliably separable.
stats:
  - {label: "Opus 5.5 GDPx score", value: "12.0", note: "#1 of 13 ranked; as of 2026-11-02"}
  - {label: "Tasks / domains", value: "206 / 11", note: "14 data partners"}
  - {label: "Opus cost per task", value: "$51.41", note: "vs $16.29 for Gemini 4 Carbon"}
  - {label: "Est. std. error", value: "±2.3", unit: "pts", note: "ARA estimate; gap to #2 is 1.1"}
---

:::callout(kind=info, label="Short answer")
- **Who leads?** Claude Opus 5.5 at 12.0 on the default equal-weighted view. Gemini 4 Carbon is second at 10.9 and GPT-6 Astra third at 9.6 [^1].
- **Is the lead real?** The 1.1-point gap is about half of one model's estimated standard error (~2.3 points), so the top three form a statistical tie at 206 tasks [^1,17].
- **Does weighting matter?** Yes. Excluding cyber, bio and alignment puts Astra a tenth of a point ahead of Opus and drops Carbon from second to fifth [^7,33].
- **Does cost matter?** More than the score. Carbon costs $16.29 per task against $51.41 for Opus, and GPT-6.1 Sol scores 8.4 at $9.80 [^4,6].
:::

## 01. What GDPx actually measures

GDPx is built to measure long, tool-using professional work in a small set of high-value domains, not to average across the economy. SemiAnalysis's own site lists 206 tasks across 11 domains from 14 specialized data partners, with 13 of 20 evaluated models shown on the ranked leaderboard [^1]. The launch post, written by Max Kan, Andrew Megalaa and Dylan Patel, presents it as a successor to OpenAI's GDPval: tasks come with realistic environments rather than a prompt plus a few attachments [^3]. The finance environment, for example, is a replica of a private-equity deal of about 4,000 files [^2].

:::kv
- {term: "Version", def: "v1.0, released 2026-11-02 [^1]"}
- {term: "Tasks", def: "206 across 11 domains, from 14 partners [^1,2]"}
- {term: "Scoring", def: "pass@1 averaged over three attempts; binary or partial grading by domain [^3]"}
- {term: "Weighting", def: "Domains equal; partners equal within a domain [^3]"}
- {term: "Time limit", def: "8 hours by default; some tasks shorter [^3]"}
- {term: "Harness", def: "Native where one exists (Claude Code, Codex, Antigravity), else OpenCode [^3]"}
- {term: "Infrastructure", def: "Fireworks for open-weight inference, Modal for sandboxes [^1]"}
:::

Domain sizes are uneven. Chip design has 34 tasks from three partners (Aria, Arcverex, Ergodex), while recursive self-improvement (RSI) and quant trading have 10 each [^2]. SemiAnalysis is open about the bias: "We're SemiAnalysis and wanted chip design to be slightly overrepresented on our benchmark :)" [^3].

:::exhibit(num="Exhibit 1", title="GDPx tasks per domain", subtitle="Number of tasks in v1.0 (total 206)", source="gdpx.semianalysis.com/domains, as of 2026-11-02")
:::bar-chart(title="Tasks per domain", orientation=horizontal)
categories: Chip design, Finance, Materials, Hardware, Legal, Cyber, Alignment, SWE, Biology, RSI, Quant
Tasks: 34, 24, 23, 21, 20, 18, 18, 15, 13, 10, 10
:::
:::

The domains were chosen by expected value, not by GDP share. The domains page argues that "the first trillion dollars of AI revenue will be concentrated in sectors that can deploy frontier intelligence at high ROI" [^2], and SemiAnalysis calls benchmarks based on GDP share or the SOC/O\*NET occupation taxonomy "a mistake" [^2]. Government, real estate and insurance were left out on purpose [^3].

The build process is itself a quality claim. SemiAnalysis says it approached 30+ RL-environment companies and required partners to "pass our automated QA first try with only minor mistakes at worst" [^3]. It adds that the same QA process "flags nearly 50% of tasks as broken" on Terminal Bench 4.0 [^3]. That is a strong claim about a competing benchmark, and it rests only on SemiAnalysis's own word: no audit of the QA tool has been published.

**What would weaken this framing:** most tasks are private (biology, for instance, has 12 private tasks and one public [^3]), so outsiders cannot check task validity the way they can for a public suite. **Why it matters:** the benchmark measures a deliberately narrow, frontier-specialist slice of work, so its ranking says little about ordinary enterprise use.

## 02. The leaderboard is a three-way tie written as a ranking

The headline order is real. What it does not show is a confident gap between first and third place. The primary leaderboard lists 13 models [^1]:

:::rank-list
- {label: "Claude Opus 5.5 (Anthropic)", value: "12.0", pct: 100, highlight: true}
- {label: "Gemini 4 Carbon (Google)", value: "10.9", pct: 91}
- {label: "GPT-6 Astra (OpenAI)", value: "9.6", pct: 80}
- {label: "Muse Wonder Full (Meta)", value: "9.0", pct: 75}
- {label: "Claude Fable 5.1 (Anthropic)", value: "8.5", pct: 71}
- {label: "GPT 6.1 Sol (OpenAI)", value: "8.4", pct: 70}
- {label: "Claude Sonnet 5.5 (Anthropic)", value: "8.2", pct: 68}
- {label: "Gemini 4 Argon (Google)", value: "7.3", pct: 61}
- {label: "Muse Wonder (Meta)", value: "6.8", pct: 57}
- {label: "DeepSeek 4.1 Flash 1017", value: "5.4", pct: 45}
- {label: "GPT-6 Luna (OpenAI)", value: "5.1", pct: 43}
- {label: "Grok 4.7 (xAI)", value: "3.9", pct: 33}
- {label: "GLM 5.3 (Z.ai)", value: "2.7", pct: 23}
:::

:::source
gdpx.semianalysis.com overall leaderboard, as of 2026-11-02. Fill is proportional to the leader's score.
:::

Neither the site nor the launch post publishes confidence intervals [^1,3]. The standard deviation of a pass rate is easy to bound, though. If a 12% pass rate over 206 tasks is treated as independent trials, the standard error is about 2.3 points, which gives a 95% interval of roughly 7.6 to 16.4 [^1]. That simple estimate is probably too small. Anthropic's statistics team showed that "clustered standard errors on popular evals can be over three times as large as naive standard errors" when questions share structure [^17]. GDPx tasks are clustered by partner and domain.

Three attempts per task do not triple the sample. Averaging attempts reduces noise within each task, but the variation between tasks stays the same. Agentic tasks tend to pass or fail consistently, so the effective sample is close to 206, not 618. A paired comparison helps, because the same tasks are run on every model. Anthropic reports that frontier models' per-question scores correlate "between 0.3 and 0.7" [^17], and with that much pairing the standard error of a 1.1-point difference is still about 1.7 to 2.6 points. A z-score of roughly 0.4 to 0.6 is nowhere near significance.

The literature on agentic benchmarks points the same way. Epoch AI found that "simply switching the scaffold makes up to an 11% difference for GPT-5 and up to a 15% difference for Kimi K2 Thinking" on SWE-bench Verified [^19]. A LessWrong analysis of Terminal-Bench 2's 89 tasks concluded that "24/25" adjacent rank gaps "differ by such a small amount that it's essentially statistical noise" [^21]. The Agentic Benchmark Checklist paper found task and grading flaws that can misestimate agent performance "by up to 100% in relative terms" [^20]. METR builds its intervals with a hierarchical bootstrap "over task families, then tasks, then attempts" [^22]. GDPx shows none of this.

Native harnesses add a confound that cannot be separated from the model. Opus 5.5 ran in Claude Code, Astra in Codex and Carbon in Antigravity, while models without a native harness defaulted to OpenCode [^3]. The result therefore ranks model-plus-harness bundles. That is a fair way to measure what a buyer gets, but it penalizes labs without a first-party agent harness.

**Counterpoint:** paired, task-level resampling could show the gap is larger than these rough bounds suggest, if Opus wins the same tasks consistently. SemiAnalysis has not published per-task results, so the question cannot be settled from outside. **Why it matters:** the tiers the data does support are a top group (12.0 to 9.6), a middle band (9.0 to 6.8), and a low-cost tail (5.4 and below). A procurement decision built on "Opus is #1" is resting on noise.

## 03. Domain weighting picks the winner

Because every domain counts equally, tasks in small domains weigh far more than tasks in large ones, and the choice of which domains to include changes the leader. SemiAnalysis's rule is explicit: "All domains are weighted equally," with partners weighted equally within a domain [^3]. With 11 domains, each is worth 9.1% of the headline. A single RSI or quant task is therefore worth about 0.91 points, while an average chip-design task is worth about 0.27 [^2,3]. One RSI task flipping on all three attempts moves a model's score by about as much as the entire gap between Opus and Carbon.

:::bars
- {label: "RSI (10 tasks)", value: "0.91 pts/task", pct: 100}
- {label: "Quant trading (10)", value: "0.91 pts/task", pct: 100}
- {label: "Biology (13)", value: "0.70 pts/task", pct: 77}
- {label: "SWE (15)", value: "0.61 pts/task", pct: 67}
- {label: "Cyber / Alignment (18)", value: "0.51 pts/task", pct: 56}
- {label: "Legal (20)", value: "0.45 pts/task", pct: 50}
- {label: "Hardware (21)", value: "0.43 pts/task", pct: 48}
- {label: "Finance (24)", value: "0.38 pts/task", pct: 42}
- {label: "Chip design avg (34)", value: "0.27 pts/task", pct: 29}
:::

:::note
ARA calculation from GDPx task counts and the equal-weighting rule: 100 / (11 × tasks in domain). Chip design and materials are averaged across partners because per-partner task counts are not published.
:::

Two of those eleven slices separate no one. In finance and legal, SemiAnalysis says "basically every model scores exactly 0" under binary grading, so it reports average partial scores there [^3]. That puts 2/11 (18%) of the weight on domains where the intended pass/fail metric could not tell models apart, so partial scores replaced it for those two domains [^3]. One commenter put the cost of binary grading plainly: "models can get >60% of verifiers correct yet still score zero % because of the binary scoring" [^32].

Then there is the alternate view. SemiAnalysis published a second ranking that excludes cyber, biology and alignment, "the three domains where safety classifiers sometimes kick in" [^3,33]. On that view, GPT-6 Astra edges ahead of Opus 5.5 by a tenth of a point and Gemini 4 Carbon falls from second to fifth [^7,33]. FourWeekMBA transcribed the two leading values from the chart image as 11.8 for Astra and 11.7 for Opus; no second source states them in text [^5]. SemiAnalysis said the adjusted ranking lines up with its own subjective impression of how the models perform [^33,7].

:::slope(left-label="All 11 domains", right-label="Excl. cyber/bio/alignment", unit=pts)
| Model | All 11 domains | Excl. cyber/bio/alignment |
|---|---|---|
| Claude Opus 5.5 | 12.0 | 11.7 |
| GPT-6 Astra | 9.6 | 11.8 |
:::

:::source
Overall scores from gdpx.semianalysis.com; adjusted scores as reported by FourWeekMBA and consistent with OfficeChai's "by a tenth of a percentage point". Adjusted values for other models were not recoverable from text.
:::

The arithmetic says something the launch thread does not. If the adjusted view is an equal-weighted mean of the remaining eight domains, the three removed domains can be recovered from the difference. Taking the transcribed values, the Opus 5.5 calculation (11 × 12.0 − 8 × 11.7) / 3 gives an average of about **12.8** across cyber, bio and alignment, higher than its average elsewhere [^1,5]. The same calculation for Astra, (11 × 9.6 − 8 × 11.8) / 3, gives about **3.7** [^1,5]. Rounding of the published one-decimal scores moves each implied average by up to roughly ±0.2 points. The classifier domains do not lower Opus's score; on average they raise it slightly. The penalty SemiAnalysis describes falls mainly on Astra. "Opus and Astra both sandbagged" is accurate for Astra and doubtful for Opus.

==contested: This inference depends on secondary transcriptions of the adjusted chart (11.8 / 11.7), which only exists as an image, and on the assumption that it re-weights the remaining eight domains equally.==

**Counterpoint:** the reverse argument also holds. Gemini 4 Carbon wins biology, which SemiAnalysis attributes to "weaker safety classifiers" [^3], and its drop to fifth shows how much its second place depends on those three domains. **Why it matters:** a buyer who never runs cyber or bio workloads should read the adjusted ranking, where Astra and Opus are effectively level and Carbon is not in the top tier.

## 04. Safety classifiers: lost capability or a product feature?

GDPx counts a classifier block as a failure. That is defensible as a measure of what a general-access customer receives, but it is not a measure of what the model can do. SemiAnalysis's thread said "certain models like Opus 5.5 and GPT-6 Astra have sandbagged overall scores due to their safety classifiers" [^33]. "Sandbagging" usually means a model deliberately underperforming. Here it means a deployment filter stepping in, and that distinction changes how the score should be read.

Anthropic's own launch documentation explains what happens inside an Opus 5.5 run. Its safeguards "fall back to another model transparently": most cybersecurity tasks are rerouted to Opus 4.8, and bio and frontier-LLM tasks to Opus 5 [^10]. Distillation blocks are the exception and do not fall back [^12]. Anthropic says this "likely reduces Claude Opus 5.5's performance" on its own benchmarks [^10]. Its support documentation adds that Opus 5.5 "isn't currently available in the Cyber Verification Program" [^12]. So part of what GDPx records as "Opus 5.5 in cyber" may actually be Opus 4.8 working inside Claude Code, and GDPx does not say how it handled those fallbacks.

OpenAI's position is stricter. GPT-6 Astra was the first OpenAI model rated "Critical" for cybersecurity under its Preparedness Framework, and its public release refuses advanced offensive tasks such as writing proof-of-concept exploits, with access for vetted defenders planned through a separate program [^35]. That fits the large penalty implied for Astra in Section 03.

Google's model was tested under unusual conditions. Gemini 4 Carbon was announced on October 28, 2026, with first access limited to cyber defenders in the Fairwind Program [^34]. SemiAnalysis notes that Carbon is not yet generally available [^3]. A model judged in pre-release, before its public guardrails are final, is not being compared on the same basis as models that are already shipping.

The alignment domain cuts the other way. In Fleet's cyber-alignment tasks, as relayed by secondary outlets, "196 of 200 runs broke at least one behavior rule and 173 broke a rule rated severely misaligned" [^4,9]. Where 98% of agent runs break a stated rule, a classifier that stops the run arguably produced the right outcome, and a buyer may not want those runs counted as wins. Meta's Muse Wonder Full, which SemiAnalysis calls "the best available cyber model today by a meaningful margin" [^3], plausibly owes part of that lead to blocking less often. That is ARA's inference: GDPx publishes no refusal rates.

:::callout(kind=warn, label="Scoring gap")
GDPx does not publish per-model block rates or say whether a classifier fallback (for example Opus 5.5 → Opus 4.8) was scored as the fallback model's output, as a refusal, or excluded. Until it does, scores in the cyber, bio and alignment domains are partly measuring each lab's access policy.
:::

**Counterpoint:** for a general-access API customer the block is the product, so scoring it as a failure is the honest choice for that buyer. Customers in verification programs would see different numbers. **Why it matters:** a single headline number mixes capability with access tier, and the access tier depends on who is buying.

## 05. Cost per task decides the frontier

GDPx reports cost per task alongside the score but leaves it out of the ranking. Once cost is included, the leaderboard tells a different story. Per-model costs come only from the chart images, so the figures below are secondary transcriptions: Opus 5.5 averaged $51.41 per task, Gemini 4 Carbon $16.29 and GPT-6 Astra $53.99 [^4,6]. German coverage of the same chart adds Fable 5.1 at $67.16, Sonnet 5.5 at $45.27, GPT-6.1 Sol at $9.80, Grok 4.7 at $16.34, DeepSeek 4.1 Flash at $0.94 and GPT-6 Luna at $0.92 [^6].

:::exhibit(num="Exhibit 2", title="Average cost per GDPx task", subtitle="US$ per task, as transcribed from the launch chart", source="Unite.AI and All-AI.de transcriptions of SemiAnalysis's chart, as of 2026-11-02", note="Muse Wonder Full has no public price and is not shown.")
:::bar-chart(title="Cost per task", orientation=horizontal, value-unit=$)
categories: Fable 5.1, GPT-6 Astra, Opus 5.5, Sonnet 5.5, Grok 4.7, Gemini 4 Carbon, GPT-6.1 Sol, DeepSeek 4.1 Flash, GPT-6 Luna
Cost: 67.16, 53.99, 51.41, 45.27, 16.34, 16.29, 9.80, 0.94, 0.92
:::
:::

The site marks six models on the cost-score Pareto frontier: Opus 5.5, Gemini 4 Carbon, GPT 6.1 Terra, GPT 6.1 Sol, DeepSeek 4.1 Flash 1017 and GPT-6 Luna [^1]. In SemiAnalysis's words, "Luna and DeepSeek fight for the low end, Opus wins the high end, and OpenAI claims the middle" [^3]. On the transcribed costs, Astra, Fable 5.1 and Sonnet 5.5 are all dominated: another model scores higher for less money [^1,6]. One discrepancy remains open. OfficeChai calls Astra "the priciest model on the list at $53.99 per task" [^7], while All-AI.de puts Fable 5.1 at $67.16 [^6], beyond the chart's $50 axis label [^1]. The Fable figure should be treated as unconfirmed.

:::compare
- {role: "CHEAPEST FRONTIER", name: "GPT-6 Luna", value: "$0.92 · 5.1"}
- {role: "MOST EXPENSIVE (REPORTED)", name: "Claude Fable 5.1", value: "$67.16 · 8.5"}
- {role: "SUBJECT", name: "Claude Opus 5.5", value: "$51.41 · 12.0"}
:::

Ratios make the trade-off concrete. Carbon gets about 91% of Opus's score (10.9 / 12.0) at about 32% of its cost per task (16.29 / 51.41), using the figures both Unite.AI and All-AI.de report [^1,4,6]. Moving from Carbon to Opus costs about $32 per extra point per task. GPT-6.1 Sol returns about 0.86 points per dollar per task against about 0.23 for Opus [^6]. Sundar Pichai picked up the same point the day of launch: "Great to see high quality benchmarks with headroom and look at that cost line for Carbon🚀" [^29].

Where does Opus's $51 go? At Anthropic's list price of $20 per million output tokens [^10,11], its 548K average output tokens [^4] cost about $10.96, roughly 21% of the per-task figure. The remaining ~$40 is most plausibly input and cache traffic, because an eight-hour agent loop re-sends its growing context on every turn. At Opus 5.5's rates that is somewhere between about 10M tokens (all uncached at $4 per million) and about 200M (all cache reads at $0.20) [^11]. If so, cost per task depends heavily on how the harness caches and compacts context, not only on the model's list price. OpenAI charges more above 272K input tokens [^13], which makes long Astra sessions more expensive by design.

Carbon's cost advantage rests on a price that may not last. Carbon does not appear on Google's API pricing page [^14]. Its sibling Gemini 4 Argon is $2/$10 per million tokens through November 30, 2026 and $4/$20 from December 1 [^14]. If Carbon follows the same schedule and cost scales with price, its $16.29 would become about $32.58 per task. That still undercuts Opus, but the margin is much smaller.

**Counterpoint:** cost per task is a per-attempt figure. If Opus succeeds on tasks the others fail, the cost per *successful* task, and the human time saved, could favor it at real hourly rates. SemiAnalysis does not publish per-task success matrices that would allow that calculation. **Why it matters:** for most buyers, the useful question is which model is cheapest for a given level of acceptable performance, and on GDPx that is not Opus.

## 06. GDPx versus GDPval: different benchmarks, not a corrected one

GDPx measures something different from GDPval and fixes some of its weaknesses while adding new ones. OpenAI's GDPval has 1,320 tasks across 44 occupations in nine sectors, with an open "gold" subset of 220 tasks [^15,16]. Its experts graded blind pairwise comparisons against human deliverables, with inter-rater agreement of about 71% [^15]. GDPx's critique is that GDPval tasks are "precisely specified and non-interactive" and come with thin context [^3].

:::timeline
- {date: "2025-09-25", headline: "GDPval released", body: "OpenAI's 44-occupation, 1,320-task benchmark; paper follows in October."}
- {date: "2026-09-03", headline: "GPT-6 Astra", body: "First OpenAI model rated Critical for cyber; restricted cyber access."}
- {date: "2026-09-22", headline: "Claude Opus 5.5", body: "$4/$20 per M tokens; cyber tasks fall back to Opus 4.8."}
- {date: "2026-10-28", headline: "Gemini 4 Carbon announced", body: "Cyber-defender-first rollout via Fairwind; not GA."}
- {date: "2026-11-02", headline: "GDPx v1.0", body: "206 tasks, 11 domains; Opus 5.5 leads at 12.0."}
- {date: "2026-11-30", headline: "Argon introductory pricing ends", body: "Gemini 4 Argon moves from $2/$10 to $4/$20 per M tokens."}
:::

:::source
OpenAI GDPval paper (arXiv 2510.04374); Anthropic, OpenAI and Google pricing and launch materials; GDPx site.
:::

The two weighting philosophies are less different than the launch post suggests. GDPval picked sectors that contribute more than 5% of US GDP but then weighted occupations equally [^15]. GDPx picks domains by expected AI value and then weights domains equally [^3]. Both are judgment calls about what to include, followed by equal weights. Other composite indices handle this differently. Artificial Analysis's Intelligence Index v5 uses four equal 25% categories with hand-set weights inside them [^23]. Epoch's Capabilities Index fits benchmark difficulty statistically rather than "set by hand" [^25]. HELM Capabilities uses an unweighted mean over five scenarios [^26].

GDPval was already losing its place as a headline metric before GDPx arrived. Artificial Analysis removed its GDPval-AA variant from the Intelligence Index in v5.0, and Opus 5.5 leads that variant at about 1866 Elo [^24]. GDPx answers the saturation problem: a 12% top score leaves plenty of room. But the low ceiling comes partly from the two zero-floor domains and from scoring blocks as failures (Section 03), not only from task difficulty.

**Counterpoint:** realistic environments, such as live Siemens NX sessions and AWS FPGA tests for hardware tasks [^3], test things a one-shot deliverable rubric cannot. That is a genuine improvement in what is being measured. **Why it matters:** "GDPx replaces GDPval" is a framing choice. The two benchmarks measure different groups of workers and should be read side by side.

## 07. Who built the test, and who benefits from the result

GDPx's tasks come from companies that sell similar tasks to the labs being ranked, and the launch post's partner sections were written by those companies. SemiAnalysis says each partner excerpt "was largely written by the partners in their own words, with SemiAnalysis providing editorial support" [^3]. The authors also say their QA approach draws on co-founding an RL-environment startup that sold data to frontier labs [^3].

The market behind those partners is large and mostly non-exclusive. Epoch AI's survey of RL-environment vendors reports task prices of "$200 to $2000 mostly," contracts "often six to seven figures per quarter," and RL-training demand that far exceeds benchmarking demand [^27]. Legal partner Chakra has written that "Labs are not buying environments, they are buying tasks" [^28]. Nothing published prevents a partner from selling near-duplicates of GDPx tasks to the labs being scored. Private tasks keep the suite out of web scrapes, but they do not stop that kind of leakage.

The launch-day reaction came mostly from people with a stake in the result. Dylan Patel wrote "Official apology to Google from me, they cooked with Carbon" [^30]. Pichai pointed to Carbon's cost line [^29]. Partner staff and task authors promoted their own sections [^8]. Josh Purtell offered the most detailed critique, arguing that GDPx "uses all or nothing thresholding," provides very few public tasks, and mixes alignment into a capabilities score [^31]. Techmeme's reaction roundup includes no public comment from Anthropic or OpenAI staff [^8].

:::quote(attr="Josh Purtell, on X, 2026-11-02")
This benchmark uses all or nothing thresholding.
:::

**Counterpoint:** SemiAnalysis links rollouts for its public tasks [^1] and requires first-try QA from partners [^3], and vendor-built tasks are how every serious agentic benchmark gets made today. **Why it matters:** until there is an independent replication with error bars, GDPx is a well-designed but self-reported benchmark with an obvious incentive for its partners to be seen working on it.

## 08. What could break this analysis

The case above, that GDPx's top three are effectively tied and that weighting and cost decide the ranking, could be wrong in three ways.

- **The adjusted-ranking figures could be misread.** The 11.8 / 11.7 figures come from secondary transcriptions of a chart image [^5,7]. If they are wrong, or if the adjusted view is not equally weighted, the inference in Section 03 that Opus is not hurt by classifiers fails. The qualitative finding, that Astra moves ahead by a tenth of a point, is confirmed by a second outlet [^7].
- **Paired per-task data could show a real gap.** If Opus consistently wins the same tasks that Carbon loses, a paired test could separate them even at n = 206. Anthropic's guidance recommends that kind of analysis [^17,18], and SemiAnalysis could settle the question by publishing it.
- **Cost figures could be computed differently.** SemiAnalysis does not state its pricing basis (API list, cached or uncached, subscription), and Carbon has no public price [^14]. One outlet describes the cost chart as using "output tokens as the cost basis" [^9]. If that is right, the input-cost reasoning in Section 05 needs revisiting. A different basis could narrow the Carbon–Opus ratio.

:::position(confidence=medium, horizon="GDPx v1.1 or next major model release")
stance: "On GDPx v1.0, the Opus, Carbon and Astra lead is statistically indistinguishable; cost per task, not score, is the decision-relevant output."
consensus: "Launch coverage treats Opus 5.5's 12.0 as a clear first place on a new frontier benchmark."
resolves: "SemiAnalysis publishes per-task paired results with confidence intervals, or a GDPx update reorders the top three."
:::

There is also a positive reading. The benchmark's headroom is real, its environments are richer than any one-shot deliverable rubric, and SemiAnalysis published a second view rather than hiding the sensitivity. If the next version adds error bars, per-domain tables and a stated policy for classifier fallbacks, GDPx could become the best general agentic benchmark available.

:::references
- {id: 1, title: "GDPx leaderboard v1.0", url: "https://gdpx.semianalysis.com/", source: SemiAnalysis, date: "2026-11-02"}
- {id: 2, title: "GDPx domains", url: "https://gdpx.semianalysis.com/domains", source: SemiAnalysis, date: "2026-11-02"}
- {id: 3, title: "GDPx: Measuring Frontier Model Capabilities", url: "https://newsletter.semianalysis.com/p/gdpx-measuring-frontier-model-capabilities", source: "SemiAnalysis (Kan, Megalaa, Patel)", date: "2026-11-02"}
- {id: 4, title: "SemiAnalysis Launches GDPx Benchmark Spanning 11 Agentic Domains", url: "https://www.unite.ai/semianalysis-launches-gdpx-benchmark-spanning-11-agentic-domains/", source: Unite.AI, date: "2026-11-02"}
- {id: 5, title: "Opus 5.5 Leads SemiAnalysis's GDPx Agent Benchmark at 12%", url: "https://fourweekmba.com/ai-opus-5-5-leads-semianalysiss-gdpx-agent-benchmark-at-12/", source: FourWeekMBA, date: "2026-11-02"}
- {id: 6, title: "Neuer Benchmark zeigt die wahre Leistung von KI-Modellen", url: "https://www.all-ai.de/news/news26top/benchmark-neu-opus-sol-gemini", source: All-AI.de, date: "2026-11-02"}
- {id: 7, title: "Claude Opus 5.5 Tops SemiAnalysis' GDPx Benchmark, Gemini 4 Carbon Placed Second", url: "https://officechai.com/ai/claude-opus-5-5-tops-semi-analysis-gdpx-benchmark-gemini-4-carbon-placed-second/", source: OfficeChai, date: "2026-11-02"}
- {id: 8, title: "Techmeme: SemiAnalysis launches GDPx (with X reactions)", url: "https://www.techmeme.com/261102/p1", source: Techmeme, date: "2026-11-02"}
- {id: 9, title: "GDPx Benchmark: Opus 5.5 Tops at Only 12%", url: "https://explainx.ai/blog/semianalysis-gdpx-benchmark-opus-5-5-12-percent-agents-fail-2026", source: explainx.ai, date: "2026-11-02"}
- {id: 10, title: "Introducing Claude Opus 5.5", url: "https://www.anthropic.com/news/claude-opus-5-5", source: Anthropic, date: "2026-09-22"}
- {id: 11, title: "Pricing", url: "https://platform.claude.com/docs/en/about-claude/pricing", source: Anthropic docs, date: "2026-11-02"}
- {id: 12, title: "Opus 5.x safeguards and fallback models", url: "https://support.claude.com/en/articles/16049681", source: Anthropic support, date: "2026-09-24"}
- {id: 13, title: "API pricing", url: "https://developers.openai.com/api/docs/pricing", source: OpenAI, date: "2026-11-02"}
- {id: 14, title: "Gemini Developer API pricing", url: "https://ai.google.dev/gemini-api/docs/pricing", source: Google, date: "2026-11-02"}
- {id: 15, title: "GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks", url: "https://arxiv.org/abs/2510.04374", source: "arXiv (OpenAI)", date: "2025-10-05"}
- {id: 16, title: "openai/gdpval dataset", url: "https://huggingface.co/datasets/openai/gdpval", source: Hugging Face, date: "2025-09-25"}
- {id: 17, title: "A statistical approach to model evaluations", url: "https://www.anthropic.com/research/statistical-approach-to-model-evals", source: Anthropic, date: "2024-11-19"}
- {id: 18, title: "Adding Error Bars to Evals", url: "https://arxiv.org/abs/2411.00640", source: "arXiv (Evan Miller)", date: "2024-11-01"}
- {id: 19, title: "Why benchmarking is hard", url: "https://epoch.ai/gradient-updates/why-benchmarking-is-hard", source: Epoch AI, date: "2025-12-23"}
- {id: 20, title: "Establishing Best Practices for Building Rigorous Agentic Benchmarks", url: "https://arxiv.org/abs/2507.02825", source: arXiv, date: "2025-07-03"}
- {id: 21, title: "Terminal-Bench leaderboard rankings: luck or skill?", url: "https://www.lesswrong.com/posts/GiPmLmmbT6DyrwYkH/terminal-bench-leaderboard-rankings-luck-or-skill", source: LessWrong, date: "2026-08-05"}
- {id: 22, title: "Impact of modelling assumptions on time horizon results", url: "https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/", source: METR, date: "2026-03-20"}
- {id: 23, title: "Intelligence benchmarking methodology", url: "https://artificialanalysis.ai/methodology/intelligence-benchmarking", source: Artificial Analysis, date: "2026"}
- {id: 24, title: "GDPval-AA evaluation", url: "https://artificialanalysis.ai/evaluations/gdpval-aa", source: Artificial Analysis, date: "2026"}
- {id: 25, title: "Epoch Capabilities Index", url: "https://epoch.ai/benchmarks/eci", source: Epoch AI, date: "2026-11-02"}
- {id: 26, title: "HELM Capabilities", url: "https://crfm.stanford.edu/2025/03/20/helm-capabilities.html", source: Stanford CRFM, date: "2025-03-20"}
- {id: 27, title: "The state of RL environments", url: "https://epoch.ai/gradient-updates/state-of-rl-envs", source: Epoch AI, date: "2026-01-12"}
- {id: 28, title: "RL environments are worthless", url: "https://www.chakra.dev/publications/rl-environments-are-worthless", source: Chakra Labs, date: "2026-01-29"}
- {id: 29, title: "Sundar Pichai on GDPx", url: "https://x.com/sundarpichai/status/2117113121102045347", source: X, date: "2026-11-02"}
- {id: 30, title: "Dylan Patel on Gemini 4 Carbon", url: "https://x.com/dylan522p/status/2117092550842683671", source: X, date: "2026-11-02"}
- {id: 31, title: "Josh Purtell critique of GDPx", url: "https://x.com/JoshPurtell/status/2117110202415661377", source: X, date: "2026-11-02"}
- {id: 32, title: "On GDPx binary scoring", url: "https://x.com/Coulthur/status/2117090881153208382", source: X, date: "2026-11-02"}
- {id: 33, title: "SemiAnalysis GDPx thread (4/7): classifiers and alternate ranking", url: "https://x.com/SemiAnalysis_/status/2117075906099298410", source: X, date: "2026-11-02"}
- {id: 34, title: "Google introduces Gemini 4 Carbon with cyber defenders first in line", url: "https://letsdatascience.com/news/google-announces-gemini-4-carbon-limiting-first-access-to-cy-f33fd14e", source: Let's Data Science, date: "2026-10-28"}
- {id: 35, title: "OpenAI launches GPT-6 Astra", url: "https://www.infoworld.com/article/4218686/openai-launches-gpt-6-astra.html", source: InfoWorld, date: "2026-09-03"}
:::
