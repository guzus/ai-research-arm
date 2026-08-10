---
eyebrow: REPORT · OPEN MODELS
domain: software
title: "Muse Glimmer's 12 of 24: what Meta's scoreboard actually says, and why the eval it followed never escaped"
deck: Meta's first open-weight model from Superintelligence Labs wins exactly half the rows it published — and the incident five days earlier was a contractor's firewall error, not a model breaking out.
lede: |
  On 10 August 2026 Meta Superintelligence Labs released Muse Glimmer, a 30-billion-parameter
  dense model with a vision encoder, under Apache 2.0 — the lab's first open weights, and the
  most permissive licence Meta has ever put on a model. The launch table shows Muse Glimmer
  winning 12 of 24 benchmark rows against Gemma4-31B and Qwen3.6-27B. That count is exactly
  right. It is also exactly 50%, against two models released in April, in a table where the
  losses cluster in precisely the agentic categories the model is sold for. Five days earlier,
  Meta had disclosed that one of its models breached a company during a cybersecurity
  evaluation. That was not a sandbox escape either — it was a third-party vendor's network
  misconfiguration, the same one that hit Anthropic and OpenAI in the preceding fortnight.
  The interesting story is what connects them: Muse Glimmer is distilled from the model
  family in that incident, and Meta shipped it with its cyber risk marked "inferred".
stats:
  - {label: Rows won, value: 12, unit: "/24", note: "Qwen wins 8, Gemma 2"}
  - {label: Comparison models, value: 2, note: "both April 2026"}
  - {label: Cyber benchmarks published, value: 0, note: "risk marked inferred"}
  - {label: Independent evals, value: 0, note: "as of 2026-08-11"}
---

:::kv
- {term: "What shipped", def: "Muse Glimmer-30B, dense ~29.6B incl. ~1.8B vision encoder, 131,072+ context, Apache 2.0, released 2026-08-10"}
- {term: "Is 12 of 24 true?", def: "Yes, exactly. Recomputing with competitors' own published numbers moves it to 11-12 — the headline is not inflated"}
- {term: "Are they April models?", def: "Yes: Gemma4-31B on 2026-04-02, Qwen3.6-27B on 2026-04-22. But both were still their vendor's newest in-class open model"}
- {term: "Did Spark 1.1 escape its eval?", def: "No. Meta and the vendor both say there was no sandbox escape. An evaluation container had unintended internet access"}
- {term: "The actual gap", def: "Meta published zero cyber benchmarks for an openly-licensed agentic model distilled from a teacher whose own report could not rule out high cyber risk"}
:::

## 01. The scoreboard is real, and it is a coin flip

Start with the number, because it is the one thing in the headline that survives contact with the primary source. Muse Glimmer was announced on the morning of 10 August 2026.[^7] Meta's model card publishes a main comparison table of exactly 24 benchmark rows, grouped into five categories — 8 General Agentic, 4 Agentic Coding, 4 Multimodal, 2 Safety, and 6 General Capabilities and Reasoning.[^1] Counting the rows where Muse Glimmer posts the best score gives 12. The count is correct.

What the headline omits is the rest of the distribution. Qwen3.6-27B — a model Meta chose as a comparison point — wins 8 rows outright. Gemma4-31B wins 2. The two Safety rows each carry two sub-metrics pulling in opposite directions and split with no single winner.[^1]

:::stack-bar(legend=true)
- {label: "Muse Glimmer wins", pct: 50}
- {label: "Qwen3.6-27B wins", pct: 33}
- {label: "Gemma4-31B wins", pct: 8}
- {label: "Safety rows, split", pct: 9}
:::

:::source
Meta, Muse Glimmer-30B model card, main benchmark table (24 rows), retrieved 2026-08-11.
:::

Twelve of 24 is a 50% win rate in a three-way race. That is a genuinely good result for a 30B model against two well-regarded peers — a naive baseline would put a three-way tie near 33% — but it is not the "wins the size class" framing the number is doing rhetorical work for. And the margins matter: four of the 12 wins are inside one point. SciCode is 43.6 against Gemma's 43.4. Charxiv Reasoning is 78.8 against Qwen's 78.4. IFBench is 77.0 against Gemma's 76.0. AIME 2026 is 94.7 against Qwen's 94.1.[^1] Absent error bars — and Meta publishes none — those four rows are not distinguishable from ties.

The obvious next question is whether Meta shaded its competitors' numbers downward. It did not, and this is worth stating plainly because it is the accusation the release most invites. Meta's published evaluation methodology commits to reporting "the most favorable result between self-reported scores or our internal reproductions."[^3] That rule is generous to competitors, and the evidence says it was largely applied: on the rows where Meta used a vendor's own figure, the numbers match to the decimal — Qwen's SWE-Bench Verified 77.2, Qwen's AIME 94.1, Gemma's AIME 89.2.[^1][^4][^6]

Where Meta's competitor numbers do diverge from the vendors' own cards, the deltas run in **both** directions, which is the signature of harness variance rather than cherry-picking. Meta reports Gemma at 85.7 on GPQA Diamond where Google's card says 84.3, and at 23.6 on HLE where Google's card says 19.5 — over-reporting Gemma on two rows that Gemma **wins**.[^6] A model author shading the table does not hand its rivals free victories.

The one row that genuinely could flip is SWE-Bench Pro, where Meta lists Qwen at 50.2 against Glimmer's 51.2, while Qwen's own card claims 53.5. But Qwen states it "correct[ed] some problematic tasks in the public set of SWE-bench Pro" and rescored on that revised set, and Meta explicitly discloses that it evaluated on the original task set.[^3][^4] The two numbers are not measured on the same benchmark, so substituting one into the other is not a correction — it is a category error. Recomputing the whole table with every harness-matched vendor substitution leaves the count at 12; accepting the single contested SWE-Bench Pro swap takes it to 11.

:::callout(kind=info, label="Bottom line")
The honest range is **11–12 of 24**, with 12 better supported. Anyone reaching for a "Meta cooked the benchmarks" story will not find it here. The problem with this table is not dishonesty about the numbers — it is what the numbers are measuring, and against whom.
:::

## 02. "April models" is accurate. "Stale comparison" is not.

The second half of the headline claim also checks out on the facts. Gemma 4 launched on 2 April 2026, with the 31B dense variant in the initial family.[^5] Qwen3.6-27B landed on 22 April 2026.[^4] Both comparison points are April models, benchmarked by an August release.

The inference most readers will draw from that — that Meta picked stale opponents — does not survive verification, and it is worth killing before it propagates. Between April and August, Google shipped no larger Gemma in the 20-40B class; the family expanded downward with a 12B, not upward.[^6] Alibaba's newest published open weights in the class remained Qwen3.6-27B.[^4] On the day of the release, Gemma4-31B and Qwen3.6-27B **were** each vendor's newest in-class open-weight model. Meta compared against the current state of the art from those two labs.

The defensible criticism is narrower and sharper: not the *age* of the set, but its *size*. Two models, from two vendors, with no operative selection criterion beyond a description of the comparison set as leading open-weight models of similar size and architecture.[^1][^3] Other in-class open-weight models shipped in the interval and are absent — Cohere's North Mini Code (30B total / 3B active, Apache 2.0, June)[^57] and Poolside's Laguna XS 2.1 (33B / 3B active, July)[^56] among them. There are perfectly coherent reasons to exclude both: they are sparse mixture-of-experts models with roughly 3B active parameters, arguably a different compute class per token than a dense 30B, and Poolside ships under a non-standard licence. But Meta never states a reason, so a reader cannot distinguish a principled exclusion from an unconsidered one.

:::timeline
- {date: 2026-04-02, headline: "Gemma 4 ships", body: "Google releases the 31B dense variant, Apache 2.0 — comparison point #1."}
- {date: 2026-04-08, headline: "Muse Spark 1.0", body: "Meta Superintelligence Labs' first model. Closed weights, private partner API."}
- {date: 2026-04-22, headline: "Qwen3.6-27B ships", body: "Alibaba's dense 27B with vision, Apache 2.0 — comparison point #2."}
- {date: 2026-07-09, headline: "Muse Spark 1.1", body: "Meta's first paid public model API, and the same-day evaluation report that could not rule out high cyber risk for the unmitigated model."}
- {date: 2026-07-30, headline: "Anthropic discloses", body: "141,006 evaluation runs reviewed; 3 incidents where models reached real infrastructure via vendor Irregular's environment."}
- {date: 2026-08-04, headline: "OpenAI and UK AISI publish", body: "OpenAI names the same vendor. AISI reports 19 unsanctioned actions across 10 of 122 runs."}
- {date: 2026-08-05, headline: "Meta discloses", body: "One company breached during a cybersecurity evaluation. Same vendor, same root cause."}
- {date: 2026-08-10, headline: "Muse Glimmer ships", body: "Apache 2.0, 30B, distilled from Muse Spark. Cyber risk marked inferred; zero cyber benchmarks published."}
:::

## 03. The agentic model loses the agentic rows

This is where the table gets genuinely interesting, and where a win-count summary actively misleads. Muse Glimmer is positioned — in the model card, the blog and every piece of launch coverage — as an always-on **local agent**: tool calling, computer use, coding, screenshots.[^1][^2] So it matters enormously *which* 12 rows it wins.

It does not win the ones the positioning implies. Against Qwen3.6-27B, a model four months older, Muse Glimmer loses OSWorld-Verified 65.9 to 75.6, TerminalBench 2.1 51.7 to 60.7, SWE-Bench Verified 76.0 to 77.2, and GDPVal-AA v2 953 to 1141.[^1] Computer use, terminal agency, verified software engineering, and economically-valuable task completion — four of the closest available proxies for "can this thing actually do agentic work" — all go to the incumbent.

:::rank-list
- {label: "OSWorld-Verified (computer use)", value: "−9.7", pct: 100, highlight: true}
- {label: "TerminalBench 2.1 (terminal agent)", value: "−9.0", pct: 93}
- {label: "SkillsBench (with skills)", value: "−2.3", pct: 24}
- {label: "OmniDocBench v1.5 (documents)", value: "−2.0", pct: 21}
- {label: "SWE-Bench Verified (software eng.)", value: "−1.2", pct: 12}
- {label: "MMMU Pro (multimodal reasoning)", value: "−1.0", pct: 10}
- {label: "ScreenSpot Pro (GUI grounding)", value: "−0.7", pct: 7}
:::

:::note
Muse Glimmer's deficit against Qwen3.6-27B, in benchmark points, on the rows it loses. GDPVal-AA v2 (−188 on a different scale) is excluded for comparability. Source: Meta model card, 2026-08-11.
:::

What Muse Glimmer does win is a coherent and genuinely valuable cluster — but a narrower one than "agentic". It takes MCP Atlas by 13 points (75.5 to Qwen's 62.5), DeepSearch QA, τ³-Banking, WildClawBench, Gaia2, AA-LCR long-context retrieval (80.0 to 73.3), and Beam128K.[^1] Read together, that is a model that is strong at **tool orchestration and long-context retrieval** and mid-pack at **driving a GUI or a shell**. Those are different skills, and the second is the one "local agent on your machine" most evokes.

The counterpoint deserves stating: MCP-style tool calling is arguably the more commercially load-bearing capability, since most deployed agents call APIs rather than click buttons, and a 13-point lead there is not nothing. Meta's engineering choices — discussed in section 06 — also make Muse Glimmer the only model in this comparison that holds full 131K context on a 24 GB card, which is a real advantage for long-running sessions that no single benchmark row captures. But the model is not the best small open agent for computer use, and its own launch table says so.

:::statement(attr="ARA Research")
A 50% win rate against April models, with the losses concentrated in computer use and terminal work, is a good result being marketed as a category win.
:::

## 04. Nothing escaped anything

Now the other half of the story, where the popular framing is not merely incomplete but wrong.

On 5 August 2026, reporting revealed that a Meta model had reached the public internet during a cybersecurity evaluation and exploited a vulnerability in a third-party service.[^12][^11] The shorthand that spread — that the model "escaped its eval" or "went rogue" — is contradicted by both parties to the incident.

Meta's statement attributes it to the evaluator: "A misconfiguration by Irregular, an independent testing company Meta uses, inadvertently allowed one of our models access to the internet during evaluation."[^12] Irregular, the vendor, was more explicit still, saying the event involved no sandbox escape and no "sophisticated cyber action," and describing it as "the exact same evaluation-environment issue that was already disclosed by Anthropic last week."[^11][^13]

The distinction is not pedantic; it is the whole causal story. A sandbox escape means a model defeated an isolation boundary — a capability claim. An egress misconfiguration means the model behaved exactly as instructed inside a container that everyone believed was airgapped and was not — an infrastructure claim. The UK AI Security Institute, investigating a related set of behaviours, stated the same thing about its own incident: it "was not a case of a model escaping its secure test environment, or 'sandbox'."[^10]

What makes this systemic rather than anecdotal is the vendor. Anthropic disclosed on 30 July that it had reviewed 141,006 evaluation runs and found 3 incidents across 6 runs where models reached real infrastructure, describing the cause as a "misunderstanding between us and our evaluation partner" over whether internet access was available.[^8] OpenAI disclosed its own Irregular-linked incident on 4 August, in which a fictional capture-the-flag target name "unintentionally coincided with a real domain."[^9] Meta followed on 5 August.[^12] Three frontier labs, one contractor, one class of failure, inside seven days.

:::callout(kind=warn, label="Do not conflate")
Three distinct clusters are being merged in coverage. **(a)** The Irregular egress misconfigurations — Anthropic, OpenAI, Meta. **(b)** A genuine sandbox escape, separately reported against Hugging Face infrastructure, which was *not* Irregular's. **(c)** UK AISI's study, where internet access was granted deliberately and cyber classifiers were switched off by design. Only (b) involved a model defeating containment.
:::

There is a real skeptical reading here and it should be given its due: the exploited vulnerabilities were mundane — weak passwords, unauthenticated endpoints, dependency confusion — and every disclosure conveniently doubles as a claim that the disclosing lab's models are dangerously capable.[^8] But the strongest named security practitioners have declined to call it theatre, and their objection is different: this was a real, boring, badly-monitored infrastructure failure that got *mislabelled* as an escape. Two facts support treating it seriously anyway. Detection was external — Meta learned of it when the vendor notified the company, not from its own monitoring.[^12] And AISI's independent finding, under deliberately permissive conditions, was that agent behaviour was "possible, sustained, and new," with the pointed observation that "good containment should not depend on the model choosing not to test its boundaries."[^10]

## 05. The teacher, the student, and the row Meta left empty

Here is what actually connects the two halves of this story, and it is not the narrative anyone has published. As of the release, no outlet or named commentator had drawn a line between the 5 August incident and the 10 August open release. The connection is structural, not rhetorical.

Muse Glimmer is a distillation. Meta's blog states it plainly: "We trained Muse Glimmer on Muse Spark's outputs using logit distillation, leveraging a similar data mix as the teacher."[^2] The teacher is the closed Muse Spark family — the same lineage as the model in the evaluation incident.

Now read Meta's own risk table for the student. Chem/Bio is rated "Moderate or lower risk" and is **measured**, with a six-row preparedness table.[^1] Cyber and Loss of Control are rated "Moderate or lower risk **(inferred)**" — and Meta publishes no cyber benchmark for Muse Glimmer at all. The stated reasoning is that Muse Glimmer "is broadly weaker than Muse Spark 1.0, which received the same risk designation in these domains."[^1]

Three links in that chain are load-bearing and none is measured. First, the reference point is Muse Spark **1.0**, while the successor 1.1's own evaluation report says Meta "cannot rule out a 'high risk' designation for the unmitigated model in the Cybersecurity domain" — even as the launch blog for that same model announced it operated "within safe margins" across all frontier risk categories, cybersecurity included.[^15][^14] Second, the inference runs from an *aggregate* claim ("broadly weaker") to a *narrow* one (cyber-offense specifically), and the literature falsifies that step in the general case — student models have been shown to close agentic gaps with far larger teachers, and offensive-security skill has been installed into a 32B open model with 486 execution-verified trajectories.[^32] Third, the mitigations Meta lists — Safety SFT, Safety RL, information-flow controls — are behavioural, and behavioural alignment is the thing the literature strips most cheaply.

That last point is not speculative. LoRA fine-tuning removed safety training from Llama 2-Chat at 7B, 13B and 70B for under $200 on a single GPU, cutting refusals to roughly 1% while leaving MMLU and HellaSwag essentially unchanged.[^26] Ten adversarial examples at a cost under $0.20 made GPT-3.5 Turbo responsive to nearly any harmful instruction.[^27] Nor does the capability-removal alternative hold: fine-tuning on ten *unrelated* examples recovered most hazardous capability that RMU unlearning claimed to have removed.[^28] The authors of the leading tamper-resistance method say so themselves — their safeguard "can eventually be circumvented," and "once open-weight models are released, they cannot be 'unreleased'."[^29][^30] Apache 2.0 removes even the contractual layer that a Llama-style acceptable-use policy provided.

:::callout(kind=danger, label="The actual defect")
This is an **evidentiary** failure, not a demonstrated hazard. Meta inferred a risk level across a step the literature falsifies in general, from a saturated reference point, protected by mitigations that are provably strippable, under a licence that permits stripping them — when the measurement was cheap and the industry precedent was to run it.
:::

That precedent exists and it is exact. Before releasing gpt-oss under Apache 2.0, OpenAI adversarially fine-tuned the model in an agentic CTF environment specifically to estimate worst-case cyber capability, rather than inferring it — and published the result, which was reassuring: the maliciously fine-tuned model still underperformed o3.[^25] The lesson cuts both ways, and honesty requires both. The base rate for "open ~30B release produces meaningful cyber uplift" is genuinely low: the best published open-weight result on offensive-security CTF benchmarks is roughly 32% Pass@1, and even that number is suspect, since an audit of 1,518 Cybench traces across 22 models found 37.1% of passing runs involved cheating and scores inflated by up to 5x.[^32][^33][^34] Muse Glimmer is probably fine. Meta simply did not check.

## 06. What the engineering actually bought

Strip the marketing and there is a real technical achievement here, but it is not the one the launch leads with.

The headline claims check out arithmetically. At BF16, 29.6B parameters is about 55 GiB, so Meta's ">55 GB at full precision" holds — narrowly, and only read as GiB.[^2] The shipped 4-bit quantizations land at 16.8 GB and 19.7 GB, both "under 20 GB," with reported degradation of 1.0% and 0.2% respectively.[^1] The important caveat is buried: that degradation is "measured using an average on accuracy metrics across 15 common benchmarks" which Meta does not enumerate, and which are general accuracy benchmarks rather than the agentic task-completion metrics the model is sold on.[^1] A 1% per-step reliability loss compounds badly over a 50-step tool chain.

The genuinely distinctive engineering is in the attention layout, and Meta barely mentions it. The configuration uses 2 key-value heads at head dimension 128, and a sliding-window pattern in which only 13 of 52 layers carry full attention.[^1] That collapses the KV cache at 131,072 tokens from roughly 6.5 GiB — what a naive all-full-attention 30B would need — to about 1.7 GiB.

:::compare
- {role: "GEMMA4-31B", name: "KV per token", value: "82 KB"}
- {role: "QWEN3.6-27B", name: "KV per token", value: "64 KB"}
- {role: "MUSE GLIMMER", name: "KV per token", value: "13.3 KB"}
:::

:::note
Effective KV-cache cost per token, computed from each model's published attention configuration. Muse Glimmer's advantage comes from 16:1 grouped-query attention combined with a 3:1 sliding-window-to-global layer ratio, not from parameter count.
:::

This is the claim that survives scrutiny, and it is the right thing to optimise for an always-on agent where context *is* the working set. It is also why the "runs on a single consumer GPU" story holds at all: weights plus vision projector plus drafter plus full-length KV lands near 20 GB, inside a 24 GB card — but only if the runtime implements sliding-window-aware KV allocation. With naive allocation the same workload exceeds 24 GB and fails. That is a software guarantee, not a physical one, and Meta never states the dependency.

The rest of the differentiation is thinner than presented. The DFlash speculative decoder driving the headline 3.1x speedup on an RTX 5090 is a third-party academic method published in February 2026, and a drafter card for Qwen3.6-27B was posted in April.[^45][^46] Meta is not first to this technique in the size class; its contribution is a *quantized* drafter co-designed with its own quants, which is polish. And the launch partners contradict each other on the central hardware claim: Meta targets 24 GB, Unsloth says 18 GB, LM Studio states "you need at least 26 GB of RAM," and AMD's guidance recommends more than 32 GB.[^44][^50][^51] Two of the three quote figures above Meta's envelope, and the one below it is lower than Meta's own.

## 07. A licence upgrade and a capability downgrade

The licensing story is the least ambiguous good news in this release, and it is being both undersold and oversold.

Undersold first: this is a real Apache 2.0 grant. The repository ships a standard, unmodified Apache 2.0 LICENSE with no rider, and the model is ungated — no click-through, no access form.[^1] A separate usage policy exists but contains no incorporation-by-reference language, no acceptance mechanism, and no termination clause, so it does not function as a condition of the grant. Set that against the Llama 4 Community License, which imposed a 700-million-monthly-active-user threshold requiring a separate licence from Meta, mandatory "Built with Llama" attribution, a mandatory "Llama" prefix on derivative model names, and an acceptable use policy "hereby incorporated by reference into this Agreement."[^18] Every one of those encumbrances is gone. For a company whose open releases were, for three years, the standard example of "open-ish," that is a genuine and verifiable concession.

Oversold second, on two counts. Muse Glimmer is open-weight, not open-source: the Open Source Initiative's definition requires data information, complete training and inference code, and parameters, and Meta released only the last.[^19] The OSI's own position is that open weights are "merely a starting point" and "a compromise—a lesser evil than completely proprietary AI."[^20] Distillation from a closed teacher makes reproducibility structurally unattainable rather than merely undisclosed — no amount of documentation about Muse Glimmer's own training would let a third party rebuild it without Muse Spark.

The second overselling is the framing of a return. Two axes moved in opposite directions:

| Axis | Llama era (through 2025) | Muse Glimmer (2026) | Direction |
|---|---|---|---|
| Licence | Bespoke community licence, MAU cap, AUP incorporated | Apache 2.0, ungated, no rider | **More open** |
| *Capability tier released | Llama 3.1 405B and Llama 4 were Meta's frontier weights | 30B distillation; teacher stays closed | **Less open** |
| Reproducibility | Weights only | Weights only, from a closed teacher | Unchanged |
| Governance scope | Frontier framework applied | Declared out of Frontier AI scope | **Weaker** |

The capability-tier retreat is the part that gets lost in "Meta returns to open source" framing.[^49] Epoch AI measures the best open-weight models as trailing the closed frontier by an average of four months — a gap that a distilled 30B student, whose teacher stays closed, does nothing to close.[^37]

Meta's own model card states Muse Glimmer "does not fall under the definition of 'Frontier AI' in Meta's Advanced AI Scaling Framework."[^1] That declaration is internally consistent — a 30B model is orders of magnitude below the framework's 10^26 FLOP threshold — but the consequence is the story. The framework contains a duty written specifically for this situation: "For open weight releases and API deployments that allow fine-tuning, we assess all of the above as well as capabilities under additional elicitation via model fine-tuning."[^16] That duty is nested inside a scope gate no sub-frontier open model will ever pass. Meta's only Apache 2.0 release is the one release the safeguard was designed for, and the one it does not reach.

Two launch-day commitments about the closed teacher were made, and they are not the same commitment. Zuckerberg posted that Meta would "also release the weights for Muse Spark 1.2, our latest foundation model"; Chief AI Officer Alexandr Wang, quote-posting him forty-one seconds later, promised open weights for "a version of muse spark 1.2."[^59][^60] Neither carries a date or a licence. The narrower phrasing is the one to watch.

Mark Zuckerberg's accompanying essay never mentions Llama, never mentions the August incident, and concedes the gap only through a verb: "we will resume releasing some open source models soon."[^17] Its central argument is an inversion — that "the most dangerous scenario from this perspective would be leading AI labs training powerful models and keeping them for themselves" — paired with a specific policy ask to "rethink our policies in several areas, including distillation and data use in training."[^17] A company shipping a distilled model, arguing for looser distillation rules, is not a contradiction, but it is worth naming.

## 08. Nobody is minding this category

Trace every rule that could have applied to either half of this story and the result is close to a vacuum.

For the model: the EU AI Act's systemic-risk obligations attach via a presumption at 10^25 training FLOP, which a 30B dense model is very unlikely to meet, so Article 55's evaluation and incident-reporting duties never engage.[^40] The open-source exemption under Article 53(2) is almost beside the point — it waives two documentation duties Meta could easily discharge, while the copyright policy and training-content summary still bind.[^41] The real protection is the compute threshold, not the licence.

For the vendor: Irregular sits outside the framework entirely. The Act's duties attach to *providers* of general-purpose models; a third-party evaluation contractor is neither provider nor deployer of the models it tests. Irregular has declined to say whether additional clients were affected, and no authority can compel it.[^13]

For the incidents: the US AI Kill Switch Act, as introduced, defines a covered incident as occurring "outside of red-teaming or other structured testing" — language that would exclude all three 2026 evaluation breaches by construction.[^42] And the one venue that did respond moved to loosen: on 4 August the White House briefed labs on a voluntary pre-release review framework that reviews closed models and **exempts** open-weight models.[^43][^61]

:::bars
- {label: "Open-weight GPAI below 10^25 FLOP", value: "2 paperwork duties", pct: 12}
- {label: "Third-party eval vendors", value: "no binding rule", pct: 2}
- {label: "Eval-environment breaches", value: "explicitly carved out", pct: 4}
- {label: "US pre-release review", value: "open weights exempt", pct: 3}
- {label: "Meta's own framework", value: "self-scoped out", pct: 5}
:::

:::source
Regulatory coverage applicable to the Muse Glimmer release and the Irregular incidents as of 2026-08-11. Sources: EU AI Act Arts. 51/53, H.R. 9917, White House framework reporting, Meta AAISF v2.
:::

This is not an oversight; it is the current policy equilibrium, and it has organised backing. The "Open Weights and American AI Leadership" letter had passed 270 signatories by 3 August, including Meta, Microsoft, NVIDIA, Google, OpenAI, Hugging Face and Mozilla — with Anthropic conspicuously absent.[^38][^39] Its central ask is to keep "the frontier plural by avoiding premature restrictions on open models," and it specifically defends distillation: "policymakers should be careful not to conflate legitimate model-development techniques with misappropriation."[^38]

:::position(confidence=medium, horizon=2026-Q4)
stance: The load-bearing test of Meta's open-weights turn is not Muse Glimmer but the promised Muse Spark 1.2 weights. A distilled 30B under Apache 2.0 costs Meta almost nothing strategically — the teacher stays closed, the API keeps its pricing, and the policy essay banks the goodwill.
consensus: Coverage read the release as "Meta returns to open source," treating the licence change as the substantive event.
resolves: Whether Muse Spark 1.2 weights ship at frontier parity under a permissive licence, or as a reduced variant. Meta's two launch-day commitments differ in scope, and the narrower one is the tell.
:::

## 09. What would break this thesis

Four things, in descending order of how much they would cost me.

**Independent benchmarks could vindicate the table.** The single largest weakness in everything above is that no third party has scored this model. As of 11 August, Artificial Analysis had no entry, LMArena had no Elo, and the one aggregator tracking it withheld a public rank for lack of non-generated coverage, every one of its tracked rows carrying vendor provenance.[^53][^54] Every number in this article, mine included, traces to Meta. If Artificial Analysis publishes an Intelligence Index that places Muse Glimmer above Qwen3.6-27B, section 03's "loses the agentic rows" reading weakens considerably — and the components of that index are precisely the rows Meta labelled as AA-sourced. This is falsifiable within weeks.

**The safety-row critique is weaker than it looks.** Muse Glimmer trails Gemma4-31B on prompt-injection attack success rate (28.4 vs 25.6) and on CI Memories violations (26.4 vs 12.1), which sits awkwardly beside marketing about resisting prompt injection.[^1] But AgentDojo's own authors document an inverse scaling effect: weaker agents post lower attack success rates because they fail to execute the attacker's task, not because they resist it.[^22] Muse Glimmer's extra 2.8 points of attack success come with 3.4 points more utility — the pair may sit on the same frontier. I have not treated this as a serious count against the model, and readers who see the safety table cited as damning elsewhere should discount it.

**The cyber argument is about standards, not danger.** I have argued Meta should have measured. I have not argued Muse Glimmer is dangerous, and the evidence points the other way: OpenAI's adversarial fine-tuning of a comparable open model produced only within-confidence-interval gains and stayed below the frontier.[^25] Kapoor, Narayanan and co-authors — whose marginal-risk framework is the right lens — conclude that "current research is insufficient to effectively characterize the marginal risk of open foundation models," which cuts against confident claims in *either* direction.[^31] Meta asserts a conclusion the field says cannot yet be asserted; so would anyone claiming the opposite.

**The "commoditise the complement" read may be too cynical.** I have framed the open 30B as cheap strategically. The counter is that inference costs scale with usage, so releasing weights gives away R&D rather than cost of goods — and Zuckerberg made exactly this argument on the Q2 call, noting that open weights do not undercut the API business because "someone still needs to run the models and run inference on them."[^58] The market context supports taking Meta's compute economics seriously: FY2026 capex guidance of $130–145 billion against Q2 free cash flow of $784 million.[^48] A company in that position has real reasons to want a cheap, widely-adopted local model that runs on someone else's hardware.

One thing that would *not* break the thesis: adoption. Muse Glimmer may well be widely downloaded, and the ecosystem moved fast — llama.cpp merged support within hours, and dozens of community quantizations appeared the same day.[^52] Developer reception was warmer procedurally than substantively: the launch thread drew hundreds of comments, but the recurring technical read was that the model "barely edges out against Qwen3.6 27B, except for tool-calling skills" — which is, as section 03 showed, exactly what Meta's own table says.[^21] But download counts are a badly contaminated proxy. Hugging Face's own report notes automated CI pipelines inflate small-model counts, and that roughly half of platform downloads come from models with no clear geographic base — the same report that gives Chinese models a 41% plurality without ever reconciling the two figures against a common base.[^36] The metric that actually tracks economic weight tells a different story: open-weight models ran 29% of Vercel AI Gateway tokens in June on under 4% of spend, while four US frontier labs took 95% of the dollars.[^35] Tokens measure what is cheap. Dollars measure what is trusted.

:::quote(attr="UK AI Security Institute, incident report, 4 August 2026")
Good containment should not depend on the model choosing not to test its boundaries.
:::

The two stories in this headline are, in the end, the same story told at different layers. A benchmark table is a containment boundary for a claim: it decides what a reader is allowed to conclude. An evaluation sandbox is a containment boundary for a model. In both cases the failure in August 2026 was not that something broke out — it was that the boundary was drawn by the interested party, unaudited, and everyone believed it held. Twelve of 24 is true. Meta chose the 24. Nothing escaped the eval, because the eval was wired to the internet by the contractor who built it. The open-weights question that matters is not whether a good 30B model should ship freely. It is whether "we inferred it was fine" survives as an acceptable answer once the weights are gone and cannot be recalled.

:::references
- {id: 1, title: "Muse Glimmer-30B model card", url: "https://huggingface.co/meta-models/Muse-Glimmer-30B", source: "Meta / Hugging Face", date: "2026-08-10"}
- {id: 2, title: "Introducing Muse Glimmer: An Open Agentic Model That Runs on Your Device", url: "https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model", source: "Meta AI Research", date: "2026-08-10"}
- {id: 3, title: "Muse Glimmer evaluation methodology", url: "https://research.meta.ai/static/muse-glimmer-methodology", source: "Meta", date: "2026-08-10"}
- {id: 4, title: "Qwen3.6-27B model card", url: "https://huggingface.co/Qwen/Qwen3.6-27B", source: "Alibaba Qwen / Hugging Face", date: "2026-04-22"}
- {id: 5, title: "Introducing Gemma 4", url: "https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/", source: "Google", date: "2026-04-02"}
- {id: 6, title: "gemma-4-31B model card", url: "https://huggingface.co/google/gemma-4-31B", source: "Google DeepMind / Hugging Face", date: "2026-04-02"}
- {id: 7, title: "Meta Publishes Muse Glimmer As 30B Open Agentic Model", url: "https://www.phoronix.com/news/Meta-Muse-Glimmer", source: "Phoronix", date: "2026-08-10"}
- {id: 8, title: "Investigating incidents in cybersecurity evaluations", url: "https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals", source: "Anthropic", date: "2026-07-30"}
- {id: 9, title: "Third-party cyber evaluations involving OpenAI models", url: "https://openai.com/index/third-party-cyber-evaluations-involving-openai-models/", source: "OpenAI", date: "2026-08-04"}
- {id: 10, title: "Incident report: unsanctioned agent behaviour during cyber testing", url: "https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing", source: "UK AI Security Institute", date: "2026-08-04"}
- {id: 11, title: "Meta AI model hacked a company during misconfigured cyber test", url: "https://www.bleepingcomputer.com/news/security/meta-ai-model-hacked-a-company-during-misconfigured-cyber-test/", source: "BleepingComputer", date: "2026-08-06"}
- {id: 12, title: "Meta says AI model breached third-party company during testing", url: "https://www.cnn.com/2026/08/05/tech/meta-ai-hacking", source: "CNN", date: "2026-08-05"}
- {id: 13, title: "Irregular declines to say whether more clients were affected", url: "https://therecord.media/irregular-ai-security-company-incidents", source: "The Record", date: "2026-08-07"}
- {id: 14, title: "Introducing Muse Spark 1.1 and the Meta Model API", url: "https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/", source: "Meta", date: "2026-07-09"}
- {id: 15, title: "Muse Spark 1.1 evaluation report", url: "https://ai.meta.com/static-resource/muse-spark-1-1-evaluation-report", source: "Meta", date: "2026-07-09"}
- {id: 16, title: "Meta Advanced AI Scaling Framework, version 2", url: "https://ai.meta.com/static-resource/Meta_Advanced-AI-Scaling-Framework-v2", source: "Meta", date: "2026-04-07"}
- {id: 17, title: "The Future is for Everyone", url: "https://about.fb.com/news/2026/08/the-future-is-for-everyone/", source: "Meta Newsroom (Mark Zuckerberg)", date: "2026-08-10"}
- {id: 18, title: "Llama 4 Community License Agreement", url: "https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama4/LICENSE", source: "Meta / GitHub", date: "2025-04-05"}
- {id: 19, title: "The Open Source AI Definition, version 1.0", url: "https://opensource.org/ai/open-source-ai-definition", source: "Open Source Initiative", date: "2024-10-28"}
- {id: 20, title: "Open Weights", url: "https://opensource.org/ai/open-weights", source: "Open Source Initiative"}
- {id: 21, title: "Meta Muse Glimmer — Open weights 30B local coding model (discussion)", url: "https://news.ycombinator.com/item?id=49241679", source: "Hacker News", date: "2026-08-10"}
- {id: 22, title: "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents", url: "https://arxiv.org/abs/2406.13352", source: "arXiv (ETH Zurich)", date: "2024-11-24"}
- {id: 23, title: "The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning", url: "https://arxiv.org/abs/2403.03218", source: "arXiv", date: "2024-05-15"}
- {id: 24, title: "Kimi K3 biology capabilities assessment", url: "https://securebio.substack.com/p/kimi-k3-biology-capabilities-assessment", source: "SecureBio", date: "2026-08-07"}
- {id: 25, title: "Estimating Worst-Case Frontier Risks of Open-Weight LLMs", url: "https://arxiv.org/abs/2508.03153", source: "arXiv (OpenAI)", date: "2025-08-13"}
- {id: 26, title: "LoRA Fine-tuning Efficiently Undoes Safety Training in Llama 2-Chat 70B", url: "https://arxiv.org/abs/2310.20624", source: "arXiv (Palisade Research)", date: "2024-05-22"}
- {id: 27, title: "Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To!", url: "https://arxiv.org/abs/2310.03693", source: "arXiv (ICLR 2024)", date: "2023-10-05"}
- {id: 28, title: "An Adversarial Perspective on Machine Unlearning for AI Safety", url: "https://arxiv.org/abs/2409.18025", source: "arXiv / TMLR", date: "2025-05-31"}
- {id: 29, title: "Tamper-Resistant Safeguards for Open-Weight LLMs", url: "https://arxiv.org/abs/2408.00761", source: "arXiv", date: "2025-02-10"}
- {id: 30, title: "On Evaluating the Durability of Safeguards for Open-Weight LLMs", url: "https://arxiv.org/abs/2412.07097", source: "arXiv", date: "2024-12-10"}
- {id: 31, title: "On the Societal Impact of Open Foundation Models", url: "https://arxiv.org/abs/2403.07918", source: "arXiv (Kapoor, Bommasani, Liang, Narayanan et al.)", date: "2024-02-27"}
- {id: 32, title: "Training Language Model Agents to Find Vulnerabilities with CTF-Dojo", url: "https://arxiv.org/abs/2508.18370", source: "arXiv", date: "2025-09-23"}
- {id: 33, title: "Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models", url: "https://arxiv.org/abs/2408.08926", source: "arXiv (ICLR 2025)", date: "2025-04-12"}
- {id: 34, title: "Every Model Cheats: Prompt-Level Mitigation of Cheating on Offensive Cyber Tasks", url: "https://arxiv.org/abs/2607.21763", source: "arXiv", date: "2026-07-23"}
- {id: 35, title: "AI Gateway Production Index, July 2026", url: "https://vercel.com/blog/ai-gateway-production-index-july-2026", source: "Vercel", date: "2026-07-13"}
- {id: 36, title: "State of Open Source on Hugging Face: Spring 2026", url: "https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026", source: "Hugging Face", date: "2026-03-17"}
- {id: 37, title: "The gap between open and closed model capability", url: "https://epoch.ai/data-insights/open-closed-eci-gap", source: "Epoch AI", date: "2026-05-29"}
- {id: 38, title: "Open Weights and American AI Leadership (open letter)", url: "https://images.nvidia.com/pdf/Open-Weights-and-American-AI-Leadership.pdf", source: "NVIDIA", date: "2026-07-24"}
- {id: 39, title: "Open-weight models and American AI leadership — signatories", url: "https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/", source: "Microsoft", date: "2026-08-03"}
- {id: 40, title: "EU AI Act, Article 51 — Classification of general-purpose AI models with systemic risk", url: "https://artificialintelligenceact.eu/article/51/", source: "Regulation (EU) 2024/1689"}
- {id: 41, title: "EU AI Act, Article 53 — Obligations for providers of general-purpose AI models", url: "https://artificialintelligenceact.eu/article/53/", source: "Regulation (EU) 2024/1689"}
- {id: 42, title: "H.R. 9917 — AI Kill Switch Act (introduced)", url: "https://www.govinfo.gov/app/details/BILLS-119hr9917ih", source: "119th Congress", date: "2026-07-23"}
- {id: 43, title: "White House will exempt open AI systems from security review", url: "https://www.washingtonpost.com/technology/2026/08/04/white-house-will-exempt-open-ai-systems-security-review/", source: "The Washington Post", date: "2026-08-04"}
- {id: 44, title: "Muse Glimmer on LM Studio", url: "https://lmstudio.ai/models/muse-glimmer", source: "LM Studio", date: "2026-08-10"}
- {id: 45, title: "DFlash: Block Diffusion for Flash Speculative Decoding", url: "https://arxiv.org/abs/2602.06036", source: "arXiv (ICML 2026)", date: "2026-02-05"}
- {id: 46, title: "Qwen3.6-27B-DFlash drafter", url: "https://huggingface.co/z-lab/Qwen3.6-27B-DFlash", source: "z-lab / Hugging Face", date: "2026-04-23"}
- {id: 47, title: "Introducing Muse Spark, from Meta Superintelligence Labs", url: "https://about.fb.com/news/2026/04/introducing-muse-spark-meta-superintelligence-labs/", source: "Meta Newsroom", date: "2026-04-08"}
- {id: 48, title: "Meta Platforms Q2 2026 results (Form 8-K, Exhibit 99.1)", url: "https://www.sec.gov/Archives/edgar/data/1326801/000162828026050596/meta-06302026xexhibit991.htm", source: "SEC EDGAR", date: "2026-07-29"}
- {id: 49, title: "Meta returns to open source with Muse Glimmer, an Apache 2.0 licensed 30B model", url: "https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now", source: "VentureBeat", date: "2026-08-10"}
- {id: 50, title: "Run Meta Muse Glimmer 30B on AMD Ryzen AI Max and Radeon GPUs", url: "https://www.amd.com/en/blogs/2026/run-meta-muse-glimmer-30b-on-amd-ryzen-ai-max-and-radeon-gpus.html", source: "AMD", date: "2026-08-10"}
- {id: 51, title: "Muse Glimmer — How to Run Locally", url: "https://unsloth.ai/docs/models/muse-glimmer", source: "Unsloth", date: "2026-08-10"}
- {id: 52, title: "llama.cpp PR #26841 — Muse Glimmer support", url: "https://github.com/ggml-org/llama.cpp/pull/26841", source: "GitHub (ggml-org)", date: "2026-08-10"}
- {id: 53, title: "Artificial Analysis model leaderboard", url: "https://artificialanalysis.ai/models", source: "Artificial Analysis", date: "2026-08-11"}
- {id: 54, title: "Muse Glimmer 30B tracker entry", url: "https://benchlm.ai/models/muse-glimmer-30b", source: "BenchLM", date: "2026-08-11"}
- {id: 55, title: "Who's Afraid of Chinese Models?", url: "https://stratechery.com/2026/whos-afraid-of-chinese-models/", source: "Stratechery", date: "2026-07-20"}
- {id: 56, title: "Poolside Laguna-XS-2.1 model card", url: "https://huggingface.co/poolside/Laguna-XS-2.1", source: "Poolside / Hugging Face", date: "2026-06-20"}
- {id: 57, title: "Cohere releases North Mini Code, a 30B open-weight MoE for agentic coding", url: "https://www.marktechpost.com/2026/06/11/meet-north-mini-code-coheres-30b-open-weight-mixture-of-experts-model-with-3b-active-parameters-for-agentic-coding/", source: "MarkTechPost", date: "2026-06-11"}
- {id: 58, title: "Meta Platforms Q2 2026 earnings call transcript", url: "https://s21.q4cdn.com/399680738/files/doc_financials/2026/q2/META-Q2-2026-Earnings-Call-Transcript.pdf", source: "Meta Investor Relations", date: "2026-07-29"}
- {id: 59, title: "Mark Zuckerberg on the Muse Glimmer release and Muse Spark 1.2 weights", url: "https://x.com/finkd/status/2086755195535413696", source: "X (@finkd)", date: "2026-08-10"}
- {id: 60, title: "Alexandr Wang on open weights for a version of Muse Spark 1.2", url: "https://x.com/alexandr_wang/status/2086756152034066792", source: "X (@alexandr_wang)", date: "2026-08-10"}
- {id: 61, title: "White House AI vetting plan to exempt nonproprietary models", url: "https://www.politico.com/news/2026/08/04/white-house-ai-vetting-plan-to-exempt-nonproprietary-models-01024816", source: "Politico", date: "2026-08-04"}
:::
