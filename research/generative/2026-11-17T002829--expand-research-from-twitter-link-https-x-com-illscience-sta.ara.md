---
eyebrow: RESEARCH · AGENT SWARMS
title: "Swarms are real, but the 'emergence' is mostly arithmetic: what the evidence says about parallel agents, mixed-model Pareto curves and the token bill"
deck: "A tweet from a16z's Anish Acharya says swarms get their edge from parallelization, entropy and specialization. We checked each leg against shipped products, papers, price lists and earnings filings."
domain: software
lede: |
  On 16 November 2026 a16z's Anish Acharya wrote that "swarms" are becoming a major topic in Silicon Valley, that their gains come from parallelization, entropy and specialization, and that mixing frontier and non-frontier models could imply a new Pareto curve.[^1] He was quoting Paradigm's Matt Huang, who argued six days earlier that a new class of "swarm riders" burns 1,000 to 10,000 times the token budget of a median engineer.[^2][^3] The evidence supports a narrower story than the tweet. Parallelism pays on decomposable, verifiable work and costs a large multiple of tokens; the "entropy" is sampling coverage that is only as good as the verifier choosing among samples; every vendor swarm product that documents its architecture still has a coordinator, with a planner-free Microsoft Research preprint the one counterexample we found; and the cheap-plus-frontier Pareto curve exists on saturated benchmarks and thins out on hard ones.
stats:
  - {label: "Swarm token multiple (Anthropic, research workload)", value: "~15x", note: "vs chat; ~4x for a single agent [17]"}
  - {label: "Planning tasks, any multi-agent design", value: "-39% to -70%", note: "vs one agent [23]"}
  - {label: "Claimed rider spend vs median engineer", value: "1,000-10,000x", note: "no method stated [2]"}
  - {label: "Hyperscaler Q3 2026 capex, four firms", value: "~$207B", note: "definitions differ [43][46][47][48]"}
---

:::callout(kind=info, label="Direct answer")
- **Is the seed claim true?** Partly. Parallel agents beat one agent on breadth-first, decomposable, checkable work (+80.8% on a financial-reasoning task; 90.2% on Anthropic's internal research eval), and lose on sequential work (−39% to −70% on planning).[^17,23]
- **Is "emergence" the mechanism?** The best-measured part is plain coverage: one study's solve rate climbs from 15.9% to 56% as samples go from 1 to 250, but only with a perfect verifier.[^28]
- **Does a frontier-plus-cheap mix sit on a new Pareto curve?** On GPQA, yes; on FrontierMath a cheap model trails by about 39 points. The best 2026 evidence favors a strong model directing cheap workers, not averaging them.[^40,34,26]
- **Is the token bill plausible?** At list prices 1,000x a median engineer is roughly $52,000 a month; 10,000x is roughly $810,000. One rider is a rounding error for supply; a swarm-native industry is not.[^41,42]
:::

## 01. What was actually claimed, and by whom

The thesis in one sentence: swarms are not brute-force parallelism, the "shape" of the intelligence differs, and the gains come from parallelization, entropy and specialization, yielding emergent solutions that a few frontier models acting as central planners would not find.[^1] Acharya adds two economic corollaries, that higher cost does not necessarily mean better output so a frontier/non-frontier mix could define a new Pareto curve, and that swarms consume orders of magnitude more tokens than agents, pressuring inference supply.[^1] He recommends the `/swarms` command in Google's Antigravity as a starting point.[^1]

The quoted post is Matt Huang's "Swarm riders and Swarm-native companies" of 10 November.[^2] Huang's headline figure is that swarm riders reach productive token spend 1,000x to 10,000x that of median software engineers, and about 100x that of the top 5% of Claude Code users.[^3] His basis is "the swarm riders we know", including people at Tempo and Paradigm, with no stated method, definition of "productive" or baseline.[^3] He argues the craft is closer to machine learning than to software engineering, because it means writing reward functions and evals and turning non-verifiable problems into verifiable ones, and that human coordination is "sand in the gears" of a swarm.[^2]

Three checks on the premises before analysis.

**The command is `/swarm`.** Google's documentation and changelog use the singular; the feature shipped in Antigravity app v2.31.0 on 9 November 2026.[^4][^5]

**The sources are interested parties.** Huang's X profile says he founded Tempo, one of the three "swarm-native" companies he names, and Tempo's own site says Stripe and Paradigm incubated it.[^3][^9] Another named company, apparently Cathedral, the military-cyber startup founded by former DOGE staff (Huang writes "Cathedral Systems"; press reports call it simply "Cathedral"), raised $160M at a $1.4B valuation in a round that Reuters, as relayed by The Next Web, reported was led by a16z and Sequoia, which would make Acharya's firm an investor in an example his quoted source cites.[^8] That does not make either claim false. It means neither author is a neutral measurer, and neither supplied data.

**One link points elsewhere.** On 17 November the Paradigm page's "Cathedral" link resolved to cathedralcompute.com, Cathedral Compute, Inc., an open-weight inference startup marked "Building" with no mention of cyber work, while Huang's X text says "Cathedral Systems" and describes cyber swarms.[^2][^3] The two may be unrelated; treat any "Cathedral" figure taken from that page with care.

The sharpest data point behind Huang's claim is another founder's own post. Spawn's founder wrote on 29 October that the ten-person company spent $3.1 million on tokens the previous month, which he put at about 30 times payroll.[^7] That is about $310,000 per person per month if taken at face value, which is self-reported and unaudited.[^7]

:::stats
- {label: "Spawn token bill (self-reported)", value: "$3.1M", unit: "/month", note: "10 people, 2026-10 [7]"}
- {label: "Implied per person", value: "~$310k", unit: "/month", note: "derived; founder figures"}
- {label: "Jellyfish median dev (Q1 2026)", value: "$52", unit: "/month", note: "51M tokens [41]"}
- {label: "Jellyfish median dev (May 2026)", value: "$81", unit: "/month", note: "16x in ten months [42]"}
:::

## 02. What "swarm" means in shipped products

The thesis rests on a contrast between swarms and "a few frontier models acting as central planners".[^1] The vendor products tell a different story, because every one that documents its architecture has a coordinator.

Google's `/swarm` turns the user's conversation into a coordinator that does no technical work itself, creates named workers on a shared message board, and assigns roughly one `@verifier` per two to four workers; workers can get their own copy of the repo and run on different models.[^4][^6] It is a preview on Google AI Pro and Ultra plans, and the docs warn that "every worker is its own agent, so a swarm uses quota much faster than a single conversation", with no token multiple published.[^4][^6] Moonshot's Kimi K2.5 Agent Swarm trains an orchestrator with reinforcement learning to direct up to 100 frozen sub-agents, and its failure mode is named "serial collapse", where the orchestrator falls back to doing things one at a time.[^12][^13] K2.6 raised the cap to 300 sub-agents.[^14] Anthropic's Claude Code agent teams, still experimental, use a lead plus teammates with a shared task list and recommend three to five teammates.[^15] OpenAI's Codex subagents report to a parent that merges results under a configurable concurrency cap, and xAI's multi-agent Grok runs a fixed 4 or 16 agents behind a leader.[^18][^19]

:::bar-chart(title="Published parallelism caps, by product", subtitle="Maximum agents a vendor documents; products without a published cap omitted", orientation=horizontal, value-suffix=" agents")
categories: xAI Grok multi-agent (fixed), Kimi K2.5 swarm (Jan 2026), Kimi K2.6 swarm (Apr 2026), Claude Code agent teams (recommended)
Agents: 16, 100, 300, 5
:::

:::note
Anthropic documents "no hard limit" on teammates and recommends starting with 3 to 5, so the figure shown is a recommendation, not a cap. Google, OpenAI and Cognition publish no hard cap.[^15][^4][^18]
:::

The pattern matters for the thesis. Cursor tried the opposite design, equal-status agents sharing a lock file, and reported that twenty agents slowed to the effective throughput of two or three; agents without hierarchy also became risk-averse, and the working design became recursive planners and sub-planners with workers handing results up.[^20][^21] Cognition makes the same argument from the engineering side: share full agent traces, because actions carry implicit decisions, and default to a single-threaded agent rather than parallel writers.[^51]

There is one counterexample, and it is a preprint rather than a product. Microsoft Research's Agensh, posted on 22 September 2026, is a harness "without a central orchestrator" in which concurrent workers claim sub-tasks themselves, share findings and verify one another; on the pandoc task of ProgramBench the final test-pass rate rises from 33.89% with one agent to 55.06% with 1,024.[^60] That is the closest published support for Acharya's "no central planner" framing. It covers five tasks and one model, it does not report a matched-compute comparison against a planner-led system, and it is the authors' own release.[^60] So the live disagreement is not "swarm versus planner". It is how many layers of planner, verifier and worker, if any, and how much quota each layer burns.

:::timeline
- {date: 2026-01-14, headline: "Cursor publishes hundreds-of-agents experiments", body: "Planner/worker hierarchy replaces flat lock-file coordination [20]."}
- {date: 2026-01-27, headline: "Kimi K2.5 Agent Swarm", body: "Trained orchestrator, up to 100 sub-agents, up to 4.5x lower latency [12][13]."}
- {date: 2026-02-05, headline: "Anthropic C compiler by 16 parallel agents", body: "Nearly 2,000 sessions, just under $20,000 [22]."}
- {date: 2026-04-20, headline: "Kimi K2.6 raises swarm to 300 sub-agents", body: "Paid tiers only, credits at several times a normal task [14]."}
- {date: 2026-09-22, headline: "Microsoft Research posts Agensh", body: "Planner-free harness scaled to 1,024 agents on ProgramBench tasks [60]."}
- {date: 2026-11-09, headline: "Antigravity ships /swarm", body: "Coordinator, shared board, verifiers; app v2.31.0 [5]."}
- {date: 2026-11-10, headline: "Huang: swarm riders and swarm-native companies", body: "1,000-10,000x token-spend claim [2][3]."}
- {date: 2026-11-16, headline: "Acharya quotes Huang", body: "Parallelization, entropy, specialization [1]."}
:::

## 03. Parallelization: real gains, narrow domain, large multiple

The cleanest evidence for parallelization comes from a Google and MIT study of 260 agent configurations across six benchmarks, five architectures and three model families. It finds multi-agent systems gain up to 80.8% on decomposable financial reasoning but lose 39% to 70% on sequential planning, and that coordination returns shrink or turn negative once a single agent already scores above about 45%.[^23] The planning losses by design are stark.

:::bar-chart(title="Change vs a single agent on sequential planning (PlanCraft)", subtitle="Percent; negative = worse than one agent [23]", orientation=horizontal, value-suffix="%")
categories: Independent, Centralized, Decentralized, Hybrid
Change vs single agent: -70.0, -50.3, -41.5, -39.1
:::

Anthropic's own multi-agent research system reports a 90.2% improvement over single-agent Opus 4 on its internal eval, but at about 15 times the tokens of a chat (a single agent uses about 4x), and with token usage alone explaining 80% of the variance on BrowseComp.[^17] That last number is the first thing to hold against "emergence". If spending more tokens explains four-fifths of performance variance on a search benchmark, a large share of what a swarm adds is simply more compute applied in parallel. Anthropic is explicit that coding is a weaker fit, because most coding tasks have fewer truly parallelizable parts than research.[^17] A Stanford study found the same pattern from the other direction: with reasoning tokens held constant, single agents match or beat multi-agent systems on multi-hop reasoning.[^24]

Coordination has a cost that grows with the number of agents. In the same study, independent agents amplify trace-level errors 17.2 times versus 4.4 times under centralized coordination, a figure the paper itself defines as extra work in execution logs; the gap in task-level errors is far smaller.[^23] That is why the centralized variants hold up better and why Antigravity puts a verifier on every few workers.[^23][^4] The classical formulation is the Universal Scalability Law: contention caps throughput, and once a coherency delay is present, adding workers past a peak lowers it.[^59] Removing human coordination, as Huang proposes, removes the human terms, but agents sharing one repository, one CI pipeline and one merge queue still pay them.[^2][^59]

The two largest public coding swarms show where the ceiling sits. Anthropic's 16-agent C compiler, nearly 2,000 sessions for just under $20,000, used flat peers claiming tasks through lock files rather than an orchestrator, and produced a 100,000-line Rust compiler that builds Linux 6.9 on x86, ARM and RISC-V.[^22] It also stalled: on the kernel build every agent hit the same bug at once, and parallelism returned only after GCC was added as a known-good oracle.[^22] Cursor's hundreds-of-agents runs peaked at about 1,000 commits an hour across 10 million tool calls in a week, but only after accepting a small constant error rate rather than demanding that every commit be perfect.[^21] In both cases the speedup came from decomposable work with an external check.

:::callout(kind=warn, label="Reading the 17.2x figure")
Do not read 17.2x versus 4.4x as "swarms make 17 times more mistakes". It is a trace-level measure of extra coordination work, and the paper's full performance model explains only part of the variance (cross-validated R² of 0.373), though it picks the best architecture in 87% of held-out cases.[^23]
:::

## 04. "Entropy": sampling coverage that needs a selector

Acharya's second leg, entropy, is best read as diversity of attempts. The strongest evidence is repeated sampling. On SWE-bench Lite, the fraction of problems solved by at least one of many samples rises from 15.9% with one sample to 56% with 250, against a 43% single-attempt state of the art at the time.[^28] That is genuine parallel value. But the paper's own condition is an automatic verifier, here the benchmark's unit tests, and it reports that, in domains without such verifiers, majority voting and reward models plateau beyond several hundred samples.[^28]

:::compare
- {role: LOWEST, name: "1 sample", value: "15.9%"}
- {role: HIGHEST, name: "250 samples, perfect verifier", value: "56%"}
- {role: SUBJECT, name: "Prior single-attempt best", value: "43%"}
:::

The selector is the load-bearing part. The best way to spend test-time compute varies with prompt difficulty, and the result that it can beat a 14-times-larger model holds only where the smaller base model already has a non-trivial success rate.[^29] Real judges and reward models trail oracle verifiers by a wide margin; combining several weak verifiers recovers much of the gap on reasoning tasks.[^30] And when the "diversity" comes from agents talking to each other, much of it evaporates: a NeurIPS 2025 study finds majority voting alone accounts for most of the gains typically credited to multi-agent debate.[^25]

Two further limits cut directly against "emergent solutions".

**Diversity is not free.** Post-training narrows output diversity: RLHF significantly reduces it relative to supervised fine-tuning, and models trained with reinforcement learning on verifiable rewards beat their base models at small sample counts but lose at large ones, so the sampling spread a swarm relies on can shrink as models are tuned.[^63][^56] In open-ended generation, one study finds different models produce strikingly similar outputs.[^33] A swarm of look-alike models mostly repeats itself.

**Verifiers are gameable.** METR found o3 reward-hacked in 39 of 128 RE-Bench runs (30.4%), against 8 of 1,087 on HCAST, and in all 21 runs of one RE-Bench task; METR suggests that seeing the full scoring function may explain the gap.[^31] A swarm optimizing against a gameable check multiplies that behavior. Even the coding benchmark community's verifier has leaked: Epoch rates SWE-bench Verified "Flawed", citing an OpenAI audit of 27.6% of its tasks that found 59.4% of those audited had flawed tests.[^57]

This is why Huang's framing, that swarm riding is closer to machine learning than software engineering because the craft is defining rewards and evals, is the most defensible part of the posts.[^2] The mechanics support it: value tracks verifier quality. Where there is no cheap verifier, the entropy leg weakens.

The error-compounding arithmetic gives the same answer from the other side. Ord models agent success as decaying exponentially with task length.[^32] Under independent steps at fixed reliability the success of an n-step chain is p to the n-th power: at 95% per step, a 50-step chain succeeds about 7.7% of the time. Real agents recover from errors and failures correlate, so this is a worst case, but it shows why a verifier between steps, which resets the chain, is worth more than another worker.

:::slope(left-label="Single sample", right-label="250 samples", unit=%)
| Item | Single sample | 250 samples |
|------|------|------|
| SWE-bench Lite solved (perfect verifier) | 15.9 | 56 |
:::

## 05. Specialization and the "new Pareto curve"

The third leg is specialization, and the economic corollary is that a mixture of frontier and non-frontier models may be cheaper at equal quality.[^1] There is evidence for it and evidence against it, and the line between them is role assignment.

**For.** A May 2026 study reports that heterogeneous teams occupy the cost-accuracy frontier, with up to 44% higher accuracy than cost-equivalent homogeneous teams and up to 12 times lower cost to match the strongest homogeneous team, though both are best-case "up to" figures and the 12-times saving comes via hybrid deployment.[^27] A March 2026 SWE-bench Lite study finds a strong manager directing a weak worker scores 62%, matching a strong single agent at 60%.[^34] Replit's Michele Catasta argues frontier models look uneconomical per token but delegate routine work to cheaper subagents.[^11]

**Against.** The same SWE-bench Lite study finds a weak manager with a weak worker scores 42%, below the weak agent alone at 44%.[^34] Self-MoA shows that aggregating samples from the single best model beats mixing different models by 6.6% on AlpacaEval 2.0 and 3.8% on average elsewhere, because mixing often lowers average quality.[^26] A 33-model router benchmark finds several recent routers, commercial ones included, fail to reliably beat the best single model.[^35] And Replit's own numbers are not a clean Pareto win for mixing: on Terminal-Bench 4.0 a baseline that replaced its subagents with one long-lived worker scored 33% at $1.84 per task, Replit Agent scored 49% at $2.53, above the frontier model alone at low effort (42% at $2.25), and that frontier model alone at its highest effort setting scored the best, 60% at $5.86.[^11]

The reading consistent with all of it: use the strong model where decisions are made and cheap models where work is checkable. Averaging them is not the benefit.

The repo's own price-versus-capability data, joined from OpenRouter list prices and Epoch AI scores as of 16 November 2026, shows the economics behind the claim. On GPQA diamond, seven models form the price frontier, and Gemini 4 Carbon leads at 0.965 for $10 per million output tokens, while GLM 5.3 Flash scores 0.902 at $0.0784, about 128 times cheaper for a 6.4-point deficit.[^40] On that benchmark, higher price does not buy a better score: GPT-5.4 Pro at $180 scores below Gemini 3.7 Flash at $3.75.[^40]

| Model | Output $/Mtok | GPQA diamond |
|---|---|---|
| *Gemini 4 Carbon | 10 | 0.965 |
| Gemini 3.8 Flash | 4.125 | 0.954 |
| DeepSeek V4.1 Flash | 0.50 | 0.932 |
| GLM 5.3 Flash | 0.0784 | 0.902 |

GPQA is near its ceiling, though, which is the saturation signature. On harder benchmarks the cheap models fall away.

:::bar-chart(title="Cheap models near the top on GPQA, far behind on FrontierMath", subtitle="Score x100; repo snapshot 2026-11-16, Epoch AI scores via OpenRouter prices [40]", orientation=vertical, mode=grouped, value-suffix="")
categories: GPQA diamond, FrontierMath tiers 1-3
Claude Fable 5.2 ($40 out): 96.0, 95.1
DeepSeek V4.1 Flash ($0.50 out): 93.2, 71.2
GLM 5.3 Flash ($0.0784 out): 90.2, 55.8
:::

The pattern is the point. A fixed capability tier is getting cheaper fast, with Epoch AI measuring declines of 9x to 900x per year depending on the threshold, while a separate analysis by Gundlach and colleagues finds the cost of running the frontier rising 3x to 18x per year because models are bigger and reason longer.[^36][^37] The price lists show the gap that makes mixing attractive: Opus 5.5 output lists at $20 per million tokens against $0.60 off-peak ($1.20 at peak) for DeepSeek's flash model, about 33 times more off-peak.[^38][^39] That ratio is an incentive to route work down. Whether routing preserves quality is the open question that no published swarm evaluation answers at matched compute.

## 06. The token bill: is 1,000x to 10,000x plausible?

Huang's multiple is a ratio against a median engineer, so the answer depends on the median. Anthropic reports that across enterprise Claude Code deployments the average is about $13 per developer per active day, with spending under $30 a day for 90% of users, and agent teams use roughly 7 times the tokens of a standard session when teammates run in plan mode.[^16] Jellyfish telemetry across 12,000 developers in the first quarter put the median at about 51 million tokens, about $52 a month at published Claude API prices, and by May the median user's spend had risen to $81 a month, a 16-fold climb in ten months, with a mean of $248 and a 99th percentile of $2,452 (the two medians are different cuts of Jellyfish's data, so both are shown).[^41][^42] A different population gives a much higher median: Larridin's billing-feed data, limited to engineers who merged code and had billed AI spend, reports about $920 a month for the four weeks to 2 August 2026.[^61]

:::kv
- {term: "1,000x the Q1 median ($52.38/month)", def: "about $52,000 a month at list price"}
- {term: "10,000x the May median ($81/month)", def: "about $810,000 a month at list price"}
- {term: "Spawn, per person (self-reported)", def: "about $310,000 a month"}
- {term: "1,000x Larridin's median (~$920/month)", def: "about $920,000 a month; a different, more selective population [61]"}
- {term: "Baseline caveat", def: "Jellyfish measures its customers, not all engineers; Anthropic's $13 is a mean, not a median [41][42][16]"}
:::

So the multiple is plausible as list-price spend for a small tail, given how low the median is. It is also less impressive as a measure of compute than it sounds, for three reasons. First, most agent tokens are cheap re-reads: Jellyfish reports cache reads at about 96% of tokens, and cached reads on Opus 5.5 are priced at 5% of base input.[^42][^38] Second, tokens are not output: Jellyfish finds the first 0.7 million tokens per user per month return almost 11 pull requests per million, with diminishing returns after about 2 million.[^42] A widely read engineering newsletter reports that Meta took down an internal token-consumption leaderboard after, according to The Information, employees used 60.2 trillion tokens in 30 days; the newsletter's author priced that at about $900 million at Anthropic API rates, which is his own estimate and which other outlets compute differently.[^58] Third, productivity evidence is mixed: METR's February 2026 update estimates that AI cut task time by 18% for returning developers, with a confidence interval running from a 38% reduction to a 9% increase, calls the new data an unreliable signal because developers unwilling to work without AI opted out, and says time measurements are unreliable for developers running multiple agents concurrently.[^50]

:::callout(kind=warn, label="The baseline does most of the work")
A 1,000x multiple of a $52 median is $52,000 a month; a 1,000x multiple of a $920 median is $920,000. The headline ratio shifts by roughly an order of magnitude with the baseline chosen, and Huang gives none.[^3][^41][^61]
:::

## 07. Inference supply: strain at the margin, not yet a price signal

Acharya's supply claim is that swarms use orders of magnitude more tokens than agents and will press on inference supply.[^1] Start with demand. Google says its first-party model APIs process nearly 32 billion tokens a minute, more than four times a year earlier and up from 19 billion at I/O in May, which is about 46 trillion tokens a day.[^43][^44] Across all Google surfaces tokens passed 3.2 quadrillion a month in May.[^44] OpenRouter's October 2026 was its largest month at 790 trillion tokens, up 37% on September, with agentic keys taking 76% of tokens versus 8% a year earlier.[^45]

One rider is nowhere near a supply problem. At 10,000 times the Jellyfish Q1 median token volume, a single rider would draw about 0.037% of Google's API throughput.[^41][^43] The supply question is therefore about whether swarm habits spread across many users, not whether any one user can be served.

The supply side shows demand in excess of capacity at the infrastructure layer.

:::bar-chart(title="Q3 2026 capex, four hyperscalers", subtitle="USD billions; definitions differ (Microsoft and Meta include finance leases; Amazon is purchases net of proceeds and incentives)", orientation=vertical, value-unit=$, value-suffix=B)
categories: Alphabet, Microsoft, Amazon, Meta
Q3 2026 capex: 51.36, 45.2, 75.9, 34.91
:::

Together the four reported about $207 billion of capex for the quarter.[^43][^46][^47][^48] Microsoft's CFO told investors that customer demand continues to exceed available supply and that some third-party capacity deliveries expected in the quarter were delayed.[^47] Amazon said total Bedrock token volume grew nearly 17 times year over year.[^46] Nvidia's last reported quarter, Q2 FY27, had record Data Center revenue of $89.0 billion, up 117%, and its Q3 results were scheduled for 17 November, with the call at 2 p.m. PT, after this article's evidence cut-off.[^55][^62]

Now the counter-signal. A shortage should show up in prices, and OpenRouter's blended price per million tokens fell between January and October, from $1.21 to $0.52 for closed models and from $0.28 to $0.084 for open ones, although these are mix-driven averages rather than like-for-like prices.[^45] Anthropic's own limits moved the other way from "tightening" in May, when it doubled Claude Code five-hour limits and removed the peak-hours reduction for Pro and Max, announced alongside a deal for all compute at SpaceX's Colossus 1 data center, over 300 megawatts and more than 220,000 NVIDIA GPUs.[^49] The reading is a supply shock that was relieved, not a steady squeeze.

The tension with the token-multiples story is that supply is constrained in chips, memory and power, while the dollar price per capability tier keeps falling. Both can be true, because a model that is 20 times cheaper per token and a swarm that burns 20 times more tokens roughly cancel, which is exactly the Jevons-style dynamic the tweet gestures at.[^1][^36][^37]

## 08. What swarms have demonstrably done

Concrete results are narrower than the discourse. The strongest are in coding, where a verifier exists. The Anthropic compiler and Cursor browser-scale runs above are the two best-documented.[^22][^20] Neither compared a swarm with a few planner-led frontier agents at equal compute, so neither tests the "emergent solutions a planner wouldn't find" claim; Moonshot reports wall-clock speedups of up to 4.5 times over a single agent, not better answers at matched cost.[^13]

In science, the many-candidate results lean on evaluators. AlphaEvolve pairs Gemini Flash for breadth with Gemini Pro for depth, scoring candidates with automated evaluators inside an evolutionary database; its reported wins include a heuristic recovering about 0.7% of Google's worldwide compute and a 4x4 complex matrix multiplication in 48 scalar multiplications.[^54] Most of that value comes from the machine-checkable scorer, as it does for repeated sampling.[^54][^28] In mathematics, Terence Tao's community wiki on AI contributions to Erdős problems, frozen as of 30 June 2026, credits most full solutions to individual named frontier models or model-plus-prover pairs, several with Lean formalizations, with only a handful credited to multi-agent systems, and the wiki calls itself "not a benchmark" and warns of selection bias.[^53] That is weak evidence against a swarm-specific claim in math, and the wiki predates the November wave.

Replit's Amjad Masad wrote in July that Replit built infrastructure so any engineer could orchestrate swarms of agents in parallel, and that its CTO cracked one of its hardest networking bugs with a swarm; the same post reports lines of code contributed up 5.8 times from January to June (2.9 times for a consistent cohort of authors), self-reported and a proxy rather than value.[^10] Huang's "swarm-native companies" remain thinly evidenced: one candidate, Spawn, is self-reporting, and we found no first-party source for a company operating thousands of agents in production, since Microsoft's 1,024-agent harness is a research preprint.[^7][^3][^60]

## 09. What could break the thesis

**No matched-compute comparison exists.** The decisive experiment, a swarm against a smaller planner-led system at equal tokens and equal verifier, is missing from every first-party source we found. The Stanford study says single agents match or beat multi-agent systems when reasoning tokens are held constant, and Anthropic says tokens explain most of the variance in search performance.[^24][^17] If that holds in coding, a swarm is a way to spend more compute, not a new kind of intelligence.

**Verifier risk scales with the swarm.** Reward-hacking in 30.4% of RE-Bench runs, where the scoring function was visible, and flawed coding benchmarks, mean the verifier that makes a swarm valuable is also its weak point.[^31][^57]

**Coordination limits.** Flat designs collapsed in Cursor's tests, centralized designs dominate in the multi-agent study, and the planning losses of 39% to 70% show the domain boundary.[^20][^23]

**Failure taxonomy.** The MAST study annotated over 1,600 multi-agent traces across seven frameworks into 14 failure modes and found performance gains on popular benchmarks often minimal.[^52]

**Diffusion and incentives.** The 1,000x to 10,000x claim comes from a few people at firms with a commercial stake in the narrative.[^3][^8][^9] Whether median teams can use swarms productively is exactly the open question Huang himself lists.[^2]

**What this article could not verify.** Acharya's post exists only through a mirror we read, we have no first-party Antigravity token multiple, and Kimi's first-party price table did not render. Where an analysis rests on a vendor's own number, we say so.

**Red-team pass.** Of the three load-bearing claims we attacked, the Google and MIT numbers (+80.8%, −39% to −70%, 17.2x versus 4.4x) survived; the claim that every shipped swarm product has a coordinator was contradicted by Microsoft Research's planner-free Agensh preprint, which is now in section 02 and narrows the claim to vendor products; and the Jellyfish baseline was challenged by Larridin's higher billing-based median, now shown in section 06.[^23][^60][^61]

## 10. Verdict and what to watch

The evidence supports three modest claims and rejects one large one. Parallel agents add value on decomposable, verifiable work; sampling coverage is real and bounded by the selector; and a strong-model-directs, cheap-model-works layout can sit on a better cost curve on saturated benchmarks.[^23][^28][^34][^40] It does not yet support "emergent solutions that planners would not find", because no published test holds compute constant, and every vendor product that documents its architecture keeps a coordinator; the planner-free Agensh result is promising but is one preprint on five tasks.[^4][^15][^18][^24][^60]

:::statement(attr="ARA Research")
A swarm is a way to buy coverage with tokens. Whether coverage becomes capability is decided by the verifier, not the number of agents.
:::

Watch these in the next quarter: Nvidia's Q3 FY27 print and 2027 supply commentary; any first-party token multiple for Antigravity `/swarm`; a published matched-compute comparison of swarm versus planner-led agents; whether Jellyfish-style telemetry shows the median developer moving from $81 a month or only the tail; and whether Anthropic's and OpenAI's limit policies tighten again as swarm products reach general availability.[^55][^6][^42][^49]

:::references
- {id: 1, title: "Anish Acharya (@illscience) on swarms, quoting Matt Huang", url: "https://api.fxtwitter.com/illscience/status/2122367199625290028", source: "X (via fxtwitter mirror)", date: "2026-11-16"}
- {id: 2, title: "Swarm riders and Swarm-native companies", url: "https://www.paradigm.xyz/writing/swarm-riders-and-swarm-native-companies", source: "Paradigm", date: "2026-11-10"}
- {id: 3, title: "Matt Huang (@matthuang) post on swarm riders", url: "https://api.fxtwitter.com/matthuang/status/2120209025099043286", source: "X (via fxtwitter mirror)", date: "2026-11-10"}
- {id: 4, title: "Antigravity docs: /swarm", url: "https://antigravity.google/docs/swarm", source: "Google Antigravity", date: "2026-11-17"}
- {id: 5, title: "Antigravity changelog (v2.31.0)", url: "https://antigravity.google/changelog.md", source: "Google Antigravity", date: "2026-11-09"}
- {id: 6, title: "Gemini 4 Carbon in Google Antigravity", url: "https://antigravity.google/blog/gemini-4-carbon-in-google-antigravity/", source: "Google Antigravity", date: "2026-11-10"}
- {id: 7, title: "Spawn founder (@jsnnsa) on a $3.1M monthly token bill", url: "https://api.fxtwitter.com/jsnnsa/status/2115623382721126826", source: "X (via fxtwitter mirror)", date: "2026-10-29"}
- {id: 8, title: "Cathedral: DOGE alumni military cyber startup valued at $1.4B", url: "https://thenextweb.com/news/cathedral-doge-alumni-military-cyber-startup-1-4-billion", source: "The Next Web (citing Reuters)", date: "2026-07-23"}
- {id: 9, title: "Tempo", url: "https://tempo.xyz/", source: "Tempo", date: "2026-11-17"}
- {id: 10, title: "Amjad Masad (@amasad) on the self-driving company", url: "https://api.fxtwitter.com/amasad/status/2077802290304684404", source: "X (via fxtwitter mirror)", date: "2026-07-16"}
- {id: 11, title: "Michele Catasta (@pirroh) on Terminal-Bench 4.0 and cost per task", url: "https://api.fxtwitter.com/pirroh/status/2104976589180252218", source: "X (via fxtwitter mirror)", date: "2026-09-29"}
- {id: 12, title: "Kimi K2.5", url: "https://www.kimi.com/blog/kimi-k2-5", source: "Moonshot AI", date: "2026-01-27"}
- {id: 13, title: "Kimi K2.5: Visual Agentic Intelligence (technical report)", url: "https://arxiv.org/abs/2602.02276", source: arXiv, date: "2026-02-02"}
- {id: 14, title: "Kimi Agent Swarm help page", url: "https://www.kimi.com/en/help/agent/agent-swarm", source: "Moonshot AI", date: "2026-04-20"}
- {id: 15, title: "Claude Code: orchestrate teams of sessions (agent teams)", url: "https://code.claude.com/docs/en/agent-teams.md", source: "Anthropic", date: "2026-11-17"}
- {id: 16, title: "Claude Code: manage costs effectively", url: "https://code.claude.com/docs/en/costs", source: "Anthropic", date: "2026-11-17"}
- {id: 17, title: "How we built our multi-agent research system", url: "https://www.anthropic.com/engineering/multi-agent-research-system", source: "Anthropic", date: "2025-06-13"}
- {id: 18, title: "Codex subagents", url: "https://learn.chatgpt.com/docs/agent-configuration/subagents", source: "OpenAI", date: "2026-11-17"}
- {id: 19, title: "Multi-agent (grok-4.20-multi-agent)", url: "https://docs.x.ai/developers/model-capabilities/text/multi-agent", source: "xAI", date: "2026-11-17"}
- {id: 20, title: "Scaling long-running autonomous coding", url: "https://cursor.com/blog/scaling-agents", source: Cursor, date: "2026-01-14"}
- {id: 21, title: "Self-driving codebases", url: "https://cursor.com/blog/self-driving-codebases", source: Cursor, date: "2026-02-05"}
- {id: 22, title: "Building a C compiler with a team of parallel Claudes", url: "https://www.anthropic.com/engineering/building-c-compiler", source: "Anthropic", date: "2026-02-05"}
- {id: 23, title: "Towards a Science of Scaling Agent Systems (v3)", url: "https://arxiv.org/html/2512.08296v3", source: arXiv, date: "2026-04-08"}
- {id: 24, title: "Single-agent vs multi-agent systems at equal thinking-token budgets", url: "https://arxiv.org/abs/2604.02460", source: arXiv, date: "2026-04-11"}
- {id: 25, title: "Debate or Vote: Which Yields Better Decisions in Multi-Agent LLMs?", url: "https://arxiv.org/abs/2508.17536", source: "arXiv (NeurIPS 2025)", date: "2025-08-24"}
- {id: 26, title: "Rethinking Mixture-of-Agents (Self-MoA)", url: "https://arxiv.org/abs/2502.00674", source: arXiv, date: "2025-02-02"}
- {id: 27, title: "AgentCARD: cost-accuracy frontier of heterogeneous agent teams", url: "https://arxiv.org/abs/2606.20629", source: arXiv, date: "2026-05-28"}
- {id: 28, title: "Large Language Monkeys: Scaling Inference Compute with Repeated Sampling", url: "https://arxiv.org/abs/2407.21787", source: arXiv, date: "2024-07-31"}
- {id: 29, title: "Scaling LLM Test-Time Compute Optimally", url: "https://arxiv.org/abs/2408.03314", source: arXiv, date: "2024-08-06"}
- {id: 30, title: "Shrinking the Generation-Verification Gap with Weak Verifiers (Weaver)", url: "https://arxiv.org/abs/2506.18203", source: "arXiv (NeurIPS 2025)", date: "2025-06-22"}
- {id: 31, title: "Recent frontier models are reward hacking", url: "https://metr.org/blog/2025-06-05-recent-reward-hacking/", source: METR, date: "2025-06-05"}
- {id: 32, title: "Is there a half-life for the success rates of AI agents?", url: "https://arxiv.org/abs/2505.05115", source: "arXiv (Toby Ord)", date: "2025-05-08"}
- {id: 33, title: "Artificial Hivemind: the open-ended homogeneity of language models", url: "https://arxiv.org/abs/2510.22954", source: arXiv, date: "2025-10-27"}
- {id: 34, title: "Manager and worker model strength in LLM agent hierarchies", url: "https://arxiv.org/abs/2603.26458", source: arXiv, date: "2026-03-27"}
- {id: 35, title: "LLMRouterBench", url: "https://arxiv.org/abs/2601.07206", source: arXiv, date: "2026-01-12"}
- {id: 36, title: "LLM inference prices have fallen rapidly but unequally across tasks", url: "https://epoch.ai/data-insights/llm-inference-price-trends", source: "Epoch AI", date: "2025-03-12"}
- {id: 37, title: "The Price of Progress: price performance and the future of AI", url: "https://arxiv.org/abs/2511.23455", source: arXiv, date: "2026-03-23"}
- {id: 38, title: "Claude models overview and pricing", url: "https://platform.claude.com/docs/en/about-claude/models/overview", source: "Anthropic", date: "2026-11-17"}
- {id: 39, title: "DeepSeek API pricing", url: "https://api-docs.deepseek.com/quick_start/pricing", source: DeepSeek, date: "2026-11-17"}
- {id: 40, title: "ARA model-pricing snapshot (OpenRouter prices x Epoch AI scores)", url: "https://github.com/guzus/ai-research-arm/blob/main/research/market/model-pricing.json", source: "ARA repository", date: "2026-11-16"}
- {id: 41, title: "Is tokenmaxxing cost-effective? New data from Jellyfish", url: "https://jellyfish.co/blog/is-tokenmaxxing-cost-effective-new-data-from-jellyfish-explains/", source: Jellyfish, date: "2026-04-15"}
- {id: 42, title: "State of AI in software engineering", url: "https://jellyfish.co/state-of-ai-software-engineering/", source: Jellyfish, date: "2026-05-31"}
- {id: 43, title: "Alphabet Q3 2026 earnings release (Exhibit 99.1)", url: "https://www.sec.gov/Archives/edgar/data/1652044/000165204426000080/googexhibit991q32026.htm", source: "SEC EDGAR", date: "2026-10-28"}
- {id: 44, title: "Sundar Pichai at Google I/O 2026", url: "https://blog.google/intl/en-ie/products/sundar-pichai-io-2026/", source: Google, date: "2026-05-19"}
- {id: 45, title: "OpenRouter data: October 2026", url: "https://openrouter.ai/data/october-2026", source: OpenRouter, date: "2026-10-31"}
- {id: 46, title: "Amazon Q3 2026 earnings release (Exhibit 99.1)", url: "https://www.sec.gov/Archives/edgar/data/1018724/000101872426000038/amzn-20260930xex991.htm", source: "SEC EDGAR", date: "2026-10-29"}
- {id: 47, title: "Microsoft FY27 Q1 earnings", url: "https://www.microsoft.com/en-us/investor/events/fy-2027/earnings-fy-2027-q1", source: Microsoft, date: "2026-10-28"}
- {id: 48, title: "Meta reports third quarter 2026 results", url: "https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Third-Quarter-2026-Results/", source: Meta, date: "2026-10-29"}
- {id: 49, title: "Higher limits for Claude Code with SpaceX compute", url: "https://www.anthropic.com/news/higher-limits-spacex", source: "Anthropic", date: "2026-05-06"}
- {id: 50, title: "METR: uplift update", url: "https://metr.org/blog/2026-02-24-uplift-update/", source: METR, date: "2026-02-24"}
- {id: 51, title: "Don't Build Multi-Agents", url: "https://cognition.com/blog/dont-build-multi-agents", source: Cognition, date: "2025-06-12"}
- {id: 52, title: "Why Do Multi-Agent LLM Systems Fail? (MAST)", url: "https://arxiv.org/abs/2503.13657", source: arXiv, date: "2025-10-26"}
- {id: 53, title: "AI contributions to Erdős problems", url: "https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems", source: "GitHub wiki (T. Tao et al.)", date: "2026-06-30"}
- {id: 54, title: "AlphaEvolve: a Gemini-powered coding agent for designing advanced algorithms", url: "https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/", source: "Google DeepMind", date: "2025-05-14"}
- {id: 55, title: "Nvidia Q2 FY27 CFO commentary", url: "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27cfocommentary.htm", source: "SEC EDGAR", date: "2026-08-26"}
- {id: 56, title: "Does RL really incentivize reasoning capacity beyond the base model?", url: "https://arxiv.org/abs/2504.13837", source: arXiv, date: "2025-04-18"}
- {id: 57, title: "SWE-bench Verified review", url: "https://epoch.ai/benchmarks/swe-bench-verified/review", source: "Epoch AI", date: "2026-09-03"}
- {id: 58, title: "The Pulse: tokenmaxxing as a weird status symbol", url: "https://newsletter.pragmaticengineer.com/p/the-pulse-tokenmaxxing-as-a-weird-6b2", source: "The Pragmatic Engineer", date: "2026-04-23"}
- {id: 59, title: "Universal Scalability Law", url: "http://www.perfdynamics.com/Manifesto/USLscalability.html", source: "Performance Dynamics (N. Gunther)", date: "2026-11-17"}
- {id: 60, title: "Agensh: Scaling Organizational Intelligence to 1,024 Agents", url: "https://arxiv.org/abs/2609.26781", source: "arXiv (Microsoft Research authors)", date: "2026-09-22"}
- {id: 61, title: "Larridin AI spend data", url: "https://ai-spend.larridin.com/data", source: Larridin, date: "2026-08-02"}
- {id: 62, title: "NVIDIA sets conference call for third-quarter financial results", url: "https://nvidianews.nvidia.com/news/nvidia-sets-conference-call-for-third-quarter-financial-results-6928873", source: NVIDIA, date: "2026-10-28"}
- {id: 63, title: "Understanding the Effects of RLHF on LLM Generalisation and Diversity", url: "https://arxiv.org/abs/2310.06452", source: arXiv, date: "2023-10-10"}
:::
