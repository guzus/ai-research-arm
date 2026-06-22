---
eyebrow: DEEP DIVE · OPEN VS CLOSED FRONTIER
title: "GLM-5.2 vs the closed frontier: the narrow band where Zhipu's open model actually matches Opus 4.8 and GPT-5.5 — and where it doesn't"
deck: An open-weight model can be the best in its class and still lose to the closed frontier on the axes that decide hard problems. GLM-5.2 is exactly that — measured against the independent data, not the launch slides.
lede: |
  In June 2026 Zhipu shipped GLM-5.2, a 753-billion-parameter open-weight model under the
  MIT license, and the launch coverage collapsed into a single claim: it matches — even
  beats — Opus 4.8 and GPT-5.5 at a sixth of the price. The independent data tells a
  sharper story. GLM-5.2 is genuinely the leading open-weights model, sits about four
  points below the closed frontier on the best composite benchmark, ties or wins on a
  narrow band of agentic and frontend-coding tasks, and falls clearly behind on hard
  reasoning, multimodality, factuality, and token efficiency. Its single uncontested
  advantage is the one no benchmark scores: you can own the weights. This piece maps the
  comparison axis by axis, separating the numbers an independent evaluator measured from
  the numbers the vendor reported.
stats:
  - {label: AA Intelligence Index, value: "51", note: "#1 open · ~#6 overall"}
  - {label: Gap to Opus 4.8 / GPT-5.5, value: "−4 / −4", note: composite points}
  - {label: Context, value: "1M", unit: tok}
  - {label: Parameters, value: "753B", note: ~40B active MoE}
  - {label: Output price, value: "$4.40", unit: /Mtok, note: vs $25 Opus 4.8}
  - {label: License, value: MIT, note: open weights · text-only}
---

## 01. The one-number scorecard

The honest summary fits in five lines, before any of the analysis below.

:::kv
- {term: "Does it match the frontier?", def: "On one composite index it lands ~4 points behind Opus 4.8 and GPT-5.5 — close, not equal. It is the #1 open-weights model by a clear margin.[^1]"}
- {term: "Where it genuinely ties or wins", def: "Real-world economic tasks (GDPval), agentic and especially frontend/web coding on human-preference boards, and cost-per-token.[^1,4,25]"}
- {term: "Where it clearly fails", def: "Hardest reasoning (HLE, FrontierMath), multimodality (it is text-only), closed-book factuality, token efficiency, and independent verifiability.[^1,18,3]"}
- {term: "The uncontested edge", def: "Open MIT weights: fine-tuning, distillation, air-gap, and immunity to silent model swaps — things a closed API cannot offer at any price.[^2,35,38]"}
- {term: "The catch on that edge", def: "Serving 753B is a lab-scale undertaking; for most users the open-weight advantage stays latent and they hit an API anyway.[^31,32]"}
:::

Artificial Analysis, the most-cited independent evaluator, scored GLM-5.2 at {accent}51{/} on its Intelligence Index v4.1 on 17 June 2026 — the top open-weights model, ahead of the next-best open models (DeepSeek V4 Pro and MiniMax-M3, both 44) by eleven points, but fourth-to-sixth overall behind the closed cluster.[^1] The composite gap to the frontier is real but small: about four to five points.

:::rank-list
- {label: "Fable 5 (closed)", value: "60", pct: 100}
- {label: "Claude Opus 4.8 (closed)", value: "56", pct: 93}
- {label: "GPT-5.5 xhigh (closed)", value: "55", pct: 92}
- {label: "Claude Opus 4.7 (closed)", value: "54", pct: 90}
- {label: "GLM-5.2 (open, MIT)", value: "51", pct: 85, highlight: true}
- {label: "DeepSeek V4 Pro (open)", value: "44", pct: 73}
- {label: "MiniMax-M3 (open)", value: "44", pct: 73}
- {label: "Kimi K2.6 (open)", value: "43", pct: 72}
:::

The thesis of this article is that a single composite number flatters GLM-5.2, because it averages over axes where the model is at parity and axes where it is far behind. A four-point composite gap is the *blended* result of near-ties on agentic coding and ten-point deficits on hard reasoning.[^1] The honest comparison is per-axis, and the first thing to flag is the cost of that 51: GLM-5.2 reached it by emitting {accent}~43,000 output tokens per task{/} (about 37k of them internal reasoning), the most verbose model in its weight class — a fact that quietly undermines the headline price advantage and recurs in Section 04.[^1] Why this matters: a buyer choosing a model on the strength of "fourth in the world, one-sixth the cost" is reading a true number that hides exactly the trade-offs that determine whether it works for their task.

## 02. Where it matches: agentic and frontend coding

The strongest version of the bull case is not "GLM-5.2 is as smart as Opus" — it is "on the tasks people actually pay models to do, it is at parity, for a fraction of the cost." On the evidence, that holds for a specific, narrow band.

The single best independent data point in GLM-5.2's favor is GDPval-AA v2, Artificial Analysis's measure of performance on real-world economic tasks: GLM-5.2 scored {accent}1524{/}, edging GPT-5.5 (xhigh) at 1514.[^1,21] On human-preference coding boards the result is even sharper. On Code Arena's blind Frontend leaderboard, GLM-5.2 ranks #2 at ~1595 Elo — behind only the closed Fable 5 (1654) and ahead of every sampled Claude Opus, including Opus 4.8 (1561) — and it is #1 on DesignArena.[^25,39] latent.space, summarizing the launch, called it the top frontend-coding model available.[^24] For generating working UI, GLM-5.2 is the most credible open challenge to the closed frontier on record.

But "matches on coding" needs two hard caveats, and both cut against the launch framing.

First, the benchmarks where GLM-5.2 reportedly *beats* GPT-5.5 are vendor-measured. The headline "beats GPT-5.5 on long-horizon coding" traces to a single number — FrontierSWE 74.4 vs 72.6, a ~1.8-point margin — published by Zhipu with no third-party replication, and even on Zhipu's own table Opus 4.8 (75.1) still leads GLM-5.2.[^16,17] When you switch to a neutral harness, GLM-5.2 mostly isn't there at all:

| Benchmark (harness) | GLM-5.2 | Opus 4.8 | GPT-5.5 | Provenance |
|---|---|---|---|---|
| SWE-bench Verified (Vals AI, neutral) | not listed | 88.6 | 82.6 | independent |
| Terminal-Bench 2.1 (Terminus-2, neutral) | not listed | 74.6 | 78.2 | independent |
| SWE-bench Pro | 62.1 | 69.2 | 58.6 | vendor |
| FrontierSWE | 74.4 | 75.1 | 72.6 | vendor |
| Terminal-Bench 2.1 (own harness) | 81.0 | 78.9 | 83.4 | vendor / own scaffold |

The only coding numbers that survive a standardized independent run are the closed ones: Opus 4.8 at 88.6% and GPT-5.5 at 82.6% on Vals AI's SWE-bench Verified, where GLM-5.2 has no entry.[^13]

:::callout(kind=warn, label="Read the provenance")
Harness choice swings the same model by ~5 points — Anthropic itself reports Terminal-Bench on the public Terminus-2 harness and notes GPT-5.5's higher 83.4% uses OpenAI's own Codex CLI.[^15,14] So a cross-vendor coding table is meaningless unless the scaffold is fixed. GLM-5.2's strongest coding claims are vendor-and-scaffold-dependent; its strongest *independent* signals are general-index and human-preference, not standardized pass-rates.[^13,14]
:::

Second, even on its home turf of long-horizon agentic work, GLM-5.2 trails — and the evidence is its own model card. On the hardest agentic benchmarks Zhipu published, GLM-5.2 sits below Opus 4.8: SWE-Marathon 13.0 vs 26.0 (a 2× gap), Toolathlon 48.2 vs 59.9, MCP-Atlas 76.8 vs 77.8.[^3] The pattern is consistent: GLM-5.2 ties on single-shot tool use and visually-judged frontend output, and falls behind as task horizon and multi-tool orchestration grow. Why this matters: "matches the frontier on coding" is true for a UI-generation demo and false for a week-long autonomous refactor — and most production agent value lives closer to the second.

## 03. Where it fails: the hard-reasoning ceiling

If frontend coding is where GLM-5.2 looks frontier-class, the hardest reasoning benchmarks are where the closed models pull clearly ahead — and where the comparison is least contaminated by saturation.

The discriminating benchmark is Humanity's Last Exam. Without tools, Opus 4.8 scores 49.8% and GPT-5.5 41.4%, while GLM-5.2 reaches about 40% on Artificial Analysis's independent run — roughly a ten-point gap to Opus on the test specifically designed to resist saturation.[^18,1,20] On FrontierMath, the gap is starker still because GLM-5.2 simply isn't measured: GPT-5.5 (xhigh) posts 85.3% and Opus 4.8 80.0% on Tiers 1–3, while no independent FrontierMath score for GLM-5.2 exists.[^19,42] The absence is itself a finding — Zhipu's strongest math claim is AIME, a benchmark the field has effectively beaten.

| Benchmark | GLM-5.2 | Opus 4.8 | GPT-5.5 | Reading |
|---|---|---|---|---|
| HLE (no tools) | ~40 | 49.8 | 41.4 | discriminating; GLM ~10 pts behind Opus |
| FrontierMath T1–3 | no indep. score | 80.0 | 85.3 | GLM unmeasured = the gap |
| GPQA Diamond | 89 | 93.6 | ~94 | saturated; parity uninformative |
| AIME 2026 | 99.2 (vendor) | 98.3 | 100 | saturated; parity uninformative |

The trap in most "parity" tables is that they lead with AIME and GPQA Diamond, where all three models score 89–100% and differences are inside attempt-variance.[^1,18] At that ceiling, "GLM ties the frontier on GPQA" tells you nothing — everyone has solved it. A second, quieter trap is vendor optimism: Zhipu self-reports GPQA Diamond at 91.2%, but Artificial Analysis measures the same model at 89% — a ~2-point haircut that recurs across GLM's headline numbers.[^20,1] The counterpoint a fair reader should hold: GLM-5.2's reasoning is genuinely strong for an open model and good enough for the large majority of real prompts, which never reach HLE difficulty. But on the frontier-defining tasks — novel proofs, expert-level science, multi-step reasoning under uncertainty — the closed models are measurably, repeatably better, and GLM-5.2's verbosity (Section 04) is partly the sound of it working harder to get close.

## 04. The token-efficiency tax: cheap per token, not per task

The "one-sixth the cost" headline is true and misleading in the same breath. It is true per token: GLM-5.2 lists at $1.40 input / $4.40 output per million tokens, against Opus 4.8 at $5 / $25 and GPT-5.5 at $5 / $30 — roughly 5.7× to 6.8× cheaper on output.[^10,11,12] It is misleading per *task*, because list price is not cost-to-complete, and GLM-5.2 is the most verbose model in its class.

The cleanest apples-to-apples figure is what Artificial Analysis actually paid to run its full Intelligence Index on each model — same workload, real bill:

:::bars
- {label: "GLM-5.2 (max) — 140M tokens", value: "$983", pct: 24}
- {label: "GPT-5.5 (xhigh) — 72M tokens", value: "$2,853", pct: 71}
- {label: "Opus 4.8 (max) — 120M tokens", value: "$4,012", pct: 100}
:::

GLM-5.2 still wins — it is genuinely the cheapest to run the suite, at $982.90.[^5,6,7] But notice the inversion: it emitted the *most* tokens (140M, nearly double GPT-5.5's 72M) and still cost the least, because its per-token price is so low.[^5,6] The consequence is that its real cost advantage is far smaller than the sticker implies. On the actual workload the multiple collapses:

:::slope(left-label="Per-token list price", right-label="Full-index run", unit="×")
| GLM-5.2 cheaper by | Per-token list price | Full-index run |
|---|---|---|
| vs GPT-5.5 | 6.8 | 2.9 |
| vs Opus 4.8 | 5.7 | 4.1 |
:::

Against the concise GPT-5.5, GLM-5.2's headline 6.8× edge erodes to ~2.9× once you pay for the tokens it actually spends.[^5,6] And the erosion is structurally resistant to the usual fix: prompt caching discounts *input*, but GLM-5.2's problem is *output* verbosity — caching cannot reduce it.[^11] On long-horizon agentic loops, where reasoning tokens (37k of GLM-5.2's 43k/task) compound across many turns, practitioners report the bill climbing faster than expected; one developer noted GLM-5.2 spending "about 45k tokens" and over fifteen minutes of reasoning "before it finally wrote the first file."[^1,24] Why this matters: the open-weight pitch is "frontier-near intelligence at a fraction of the cost," and the cost half of that sentence is true on the price card and only partly true on the invoice.

## 05. Long-context: 1M on the box, unproven in the field

All three models now advertise roughly a million tokens of context — GLM-5.2 at 1,048,576, Opus 4.8 at 1M, GPT-5.5 at 1,050,000 — so the nominal window is no longer a differentiator.[^2,8,9] The differentiator is *effective* context: how well retrieval holds up at depth. Here the asymmetry is about evidence, not just capability.

GLM-5.2 launched with no long-context benchmarks at all, and as of late June 2026 it had no independent needle-in-haystack, RULER, or multi-hop retrieval curve published.[^23,24] Its only "1M" numbers are long-horizon *coding* scores — agentic throughput, not retrieval fidelity.[^3] That matters because its predecessor GLM-4.6 showed the classic open-model failure mode: sharp degradation as context filled toward its limit. Until the depth curves land, GLM-5.2's million-token window should be read as an advertised ceiling, not a demonstrated capability.

The closed models, by contrast, have at least one depth-resolved third-party curve — and it shows that even the leaders bleed accuracy at depth:

:::line-chart(title="GraphWalks BFS: multi-hop retrieval at depth", subtitle="F1 %, graph-traversal accuracy (Opus 4.8 system card)", y-unit="%")
x: 256K,1M
Opus 4.8: 85.9,68.1
GPT-5.5: 73.7,45.4
:::

Opus 4.8 falls from 85.9% at 256K to 68.1% at 1M; GPT-5.5 from 73.7% to 45.4%.[^22] So "1M context" is lossy for everyone — but the closed models have *shown their work*, and GLM-5.2 has not.

:::callout(kind=info, label="The serving caveat compounds it")
At 1M tokens the KV cache alone runs to hundreds of gigabytes — on an 8×H200 node serving GLM-5.2, roughly 387 GB of memory goes to the 1M-token cache, co-equal with the quantized weights, collapsing concurrency.[^40] The million-token window is expensive to serve even before you ask whether the quality holds — which is exactly why a self-hoster (Section 08) cannot treat 1M as free.
:::

## 06. Text-only, less factual, and censored

Three axes where GLM-5.2 does not merely trail but structurally differs from the closed frontier — and where the gap is unlikely to close with a point release.

The clearest is modality. GLM-5.2 is {accent}text-only{/}. Its Hugging Face plumbing references an `AutoModelForMultimodalLM` class, which has misled some coverage, but the official blog and independent reviewers confirm it processes only text; vision lives in Zhipu's separate, weaker GLM-V line.[^2,3,27] Both closed rivals are natively multimodal — Opus 4.8 accepts image and PDF input, and GPT-5.5 is natively omnimodal across image, audio and video.[^8,9,26] On vision benchmarks like MMMU-Pro the frontier clears 81–83% while GLM-5.2 fields no score at all.[^26] For any workflow that touches a screenshot, a chart, or a PDF, this is not a gap to be argued — it is a capability GLM-5.2 does not have.

The second is closed-book factuality. On Artificial Analysis's AA-Omniscience, GLM-5.2 scores an index of 4 with 25.1% accuracy, against Opus 4.8's index of 27 and 46.6% accuracy.[^1,7] A subtle point: GLM-5.2's raw *hallucination rate* (28.1%) actually looks lower than Opus 4.8's (35.9%), but only because it knows and answers far less — the index (4 vs 27) is the honest summary of factual reliability, and it is not close.[^1,7]

:::callout(kind=danger, label="Deployment caveat")
GLM models carry documented political censorship: GLM-5 scored ~3% compliance on ChinaBench's politically sensitive prompts, and peer-reviewed work in *PNAS Nexus* finds China-origin models refuse more and answer less accurately on political questions.[^29,30] Much of this is a serving-layer and post-training artifact a self-hoster can partly strip by fine-tuning — a freedom closed-API users lack — but the residue is baked into the weights. For global, political, or public-sector use, treat it as disqualifying until tested.[^29]
:::

Be fair about what is *not* a strong failure axis: on basic factual recall (SimpleQA-style) and instruction-following (IFEval), GLM-5.2 is roughly competitive, and those benchmarks are saturated across the field — overclaiming a deficit there would be as dishonest as the launch slides overclaiming parity on AIME.[^1] The real, durable gaps are modality, deep factual breadth, and content controls.

## 07. The one axis closed models can't touch: open weights

Every axis so far has been a benchmark, and on benchmarks GLM-5.2 is "very good, narrowly behind." But for a large class of buyers the decisive question is not "is it as smart?" — it is "can I own it?" Here the comparison inverts, because open MIT weights deliver capabilities a closed API cannot offer at any price.[^2]

:::statement(attr="The structural case")
A closed API sells you inference governed by the provider's clock. Open weights hand you the artifact — and the artifact is yours to fine-tune, distill, air-gap, and run unchanged for as long as you choose.
:::

Four concrete advantages, each falsifiable. {accent}Fine-tuning and distillation:{/} open weights can be post-trained or used as a teacher — the Harvey × Trajectory experiment took an open Nemotron model into the frontier band on a proprietary legal benchmark in under a day, a workflow closed-API terms forbid; and OpenAI is *winding down* its hosted fine-tuning platform entirely, widening the gap.[^35,37] {accent}Deprecation immunity:{/} closed models are retired on a schedule — Anthropic gives a 60-day floor, and both Claude 3.5 Sonnet snapshots were retired in October 2025, after which "requests to retired models will fail."[^36] Weights you possess cannot be remotely retired. {accent}Immunity to silent swaps:{/} closed providers change the model behind a stable name — the GPT-5 router once routed prompts to weaker models on launch day ("GPT-5 seemed way dumber," per Altman), and OpenAI silently updated GPT-4o into sycophancy in April 2025 before rolling it back.[^38] {accent}Air-gap and control:{/} only local weights run in a classified or fully offline enclave, expose raw logits, and let you remove a refusal layer.

:::timeline
- {date: "2025-04", headline: "GPT-4o sycophancy", body: "OpenAI silently updates the model behind ChatGPT, then rolls it back after users notice — no changelog. An open weight cannot change under you."}
- {date: "2025-08", headline: "GPT-5 router 'seemed way dumber'", body: "A broken autoswitcher routed prompts to weaker models on launch day; users could not tell which model answered."}
- {date: "2025-10", headline: "Claude 3.5 Sonnet retired", body: "Both dated snapshots reach end-of-life; requests to retired model IDs now fail."}
- {date: "2027-01", headline: "OpenAI fine-tuning API shutdown", body: "Hosted fine-tuning is wound down; even existing customers are blocked from new jobs."}
:::

The counterpoint is essential, and it is where most open-weight evangelism overreaches. For the great majority of buyers these advantages are theoretical: cloud tiers like AWS Bedrock and Azure already deliver no-training data residency, closing the *privacy* gap without any self-hosting; z.ai's own API undercuts self-hosting on raw price; and using that API forfeits every sovereignty advantage while sending your data to Chinese infrastructure.[^10] The advantage is real, structural, and narrow — it is *control and possession*, not *cheaper or better*. Sell it that way or not at all.

## 08. But can you actually run it? Self-hosting 753B

The open-weight advantage only exists if you can serve the weights — and a 753B-total / ~40B-active MoE is not a laptop model. The categorical fact stands: Opus 4.8 and GPT-5.5 cannot be self-hosted at any price, full stop. The practical fact is that GLM-5.2 mostly can't either, unless you are an enterprise.

:::stats
- {label: "FP8 weights", value: "~750", unit: GB, note: "8× H200-class node"}
- {label: "INT4 weights", value: "~372", unit: GB, note: "4× H200"}
- {label: "Decode, H200 @ conc 1", value: "~34", unit: tok/s, note: per GPU}
- {label: "API break-even", value: "~2.4B", unit: tok/mo, note: "~3,000+ prompts/day"}
:::

To load the weights you need roughly 1.5 TB at BF16 (≈16 GPUs), ~750 GB at FP8 (an 8×H200 node), or ~372 GB at INT4 (4×H200) — and at long context the KV cache rivals the weights for memory.[^2,31,40] Day-zero inference support is genuinely good: SGLang, vLLM, Transformers, and Ascend NPU backends all shipped on release.[^2,41] But the economics are unforgiving. A 24/7 cloud node runs ~$10–22/hr, and the break-even against z.ai's $4.40/Mtok API sits around {accent}2.4 billion output tokens a month{/} — roughly 3,000+ prompts a day at sustained utilization.[^32] Below that, the API (or OpenRouter at ~$1/$4) is strictly cheaper and far less operational pain.[^31]

So who actually self-hosts? Enterprises with data-residency, air-gap, or fine-tuning mandates and sustained volume — not individuals. A community 2-bit quantization shrinks the model to ~238 GB while retaining ~82% of quality, and a pruned 469B variant fits four prosumer Blackwell cards, but a true single-consumer-GPU deployment of full GLM-5.2 is not feasible at usable quality.[^31] Why this matters: the open-weight edge that makes GLM-5.2 strategically distinct from the closed frontier is, for most of the people excited about it, latent — they will reach for z.ai's API and inherit a cheaper, faster, but *not* sovereign and *not* fine-tunable experience, partially neutralizing the very thing that made open weights interesting.

## 09. The verification problem and the cheaper open rival

Two facts complicate even the careful version of the bull case, and both deserve to be stated plainly.

:::callout(kind=warn, label="The vendor-benchmark problem")
GLM-5.2's flashiest parity claims — "#1 on SWE-bench Pro," "beats GPT-5.5 on long-horizon coding" — originate as Zhipu's own self-reported numbers; the only genuinely independent result is the aggregate AA Intelligence Index of 51, not the per-claim parity figures.[^20,1] The-decoder put it cleanly: the headline coding wins "started as Z.ai internal, self-reported numbers."[^20] A reader should treat every GLM-5.2 benchmark that beats a closed model as vendor-reported until a neutral harness confirms it.
:::

The second complication is that GLM-5.2 may not even be the cheap open frontier. DeepSeek V4 Pro is also MIT-licensed, *has* vision, and is roughly 5× cheaper than GLM-5.2 on output ($0.87 vs $4.40 per million) — though it scores lower on the AA Index (44 vs 51) and the capability split is uneven, with DeepSeek leading competitive coding and GLM leading agentic tool use.[^33] So "cheap, open, frontier-adjacent" is a contested niche, not GLM-5.2's alone. And in terms of actual adoption, GLM-5.2 is too new (launched 13 June) to appear in OpenRouter's weekly top-ten by tokens — a board led by DeepSeek V4 Flash at ~10.9 trillion tokens — even as the structural picture holds that Chinese open-weight models win token volume while Anthropic captures ~42% of platform revenue on ~11% of tokens.[^34] GLM-5.2's clearest adoption lever is mundane and real: it is a zero-switching-cost drop-in for Claude Code via an Anthropic-protocol-compatible endpoint, and developers are already cancelling paid subscriptions over the token-per-dollar math.[^24]

## 10. What could break the thesis

The argument here is two-sided by construction: GLM-5.2 matches the closed frontier on a narrow band (cost-adjusted agentic and frontend coding, real-world economic tasks, and — categorically — open-weight control) and fails on a wider one (hard reasoning, multimodality, factuality, token efficiency, verifiability). Here is what would falsify each side.

What would falsify the {accent}skeptical{/} read (that GLM-5.2 is meaningfully behind):

- {flag:green} Independent replication of GLM-5.2's coding wins on a fixed neutral harness — if a third party reproduces "beats GPT-5.5 on FrontierSWE," the vendor-benchmark caveat collapses and the parity claim strengthens.[^16,13]
- {flag:green} A published long-context depth curve showing GLM-5.2 holding retrieval near 1M — which would convert its advertised window into a demonstrated one.[^23]
- {flag:green} It is already, unambiguously, the #1 open-weights model on the best independent index, and #2 in the world on blind frontend-coding preference — neither is hype.[^1,25]

What would falsify the {accent}bull{/} read (that GLM-5.2 matches the frontier):

- {flag:red} The ~10-point HLE gap and the absent FrontierMath score: on the benchmarks built to resist saturation, the closed models are clearly ahead, and GLM's strongest math claim sits on a saturated test.[^18,19]
- {flag:red} Token economics: the 6.8× headline price edge shrinks to ~2.9× on real workloads, and caching can't fix output verbosity.[^5,6]
- {flag:red} Text-only modality and a 4-vs-27 factuality index are structural deficits a point release won't erase.[^1,7]

:::statement(attr="ARA Research")
GLM-5.2 is the best open-weights model in the world and a notch below the closed frontier — and which of those two sentences matters depends entirely on whether you need to own the model or just to use the smartest one.
:::

:::callout(kind=success, label="Red-team note")
The three load-bearing claims of this piece — the AA Intelligence Index of 51 (≈4 points behind the closed frontier), the ~43k-tokens-per-task verbosity that erodes the cost advantage, and the text-only modality gap — were each re-checked against the primary source (Artificial Analysis and Zhipu's own model card) and an adversarial search before publication; the strongest counter-evidence found (GDPval and frontend-Arena parity) is incorporated in Sections 02 and 04 rather than buried.[^1,3,25]
:::

Why this matters, finally: GLM-5.2 is the cleanest test yet of a question the whole industry is asking. If the best open model can land within four points of the closed frontier, win the frontend-coding boards, and undercut it on price — and still lose decisively on hard reasoning, multimodality, and the simple ability to be independently verified — then "open and frontier-adjacent" is worth a great deal to the buyer who needs to own the weights, and a good deal less to the one who just needs the right answer.

## R. References

:::references
- {id: 1, title: "GLM-5.2 is the new leading open-weights model on the Artificial Analysis Intelligence Index", url: "https://artificialanalysis.ai/articles/glm-5-2-is-the-new-leading-open-weights-model-on-the-artificial-analysis-intelligence-index", source: Artificial Analysis, date: "2026-06-17"}
- {id: 2, title: "GLM-5.2 model card", url: "https://huggingface.co/zai-org/GLM-5.2", source: "Hugging Face (zai-org)", date: "2026-06-13"}
- {id: 3, title: "GLM-5.2 technical blog", url: "https://huggingface.co/blog/zai-org/glm-52-blog", source: "Hugging Face / Zhipu", date: "2026-06-17"}
- {id: 4, title: "Artificial Analysis models leaderboard", url: "https://artificialanalysis.ai/leaderboards/models", source: Artificial Analysis, date: "2026-06-22"}
- {id: 5, title: "GLM-5.2 model page (cost-to-run, tokens)", url: "https://artificialanalysis.ai/models/glm-5-2", source: Artificial Analysis, date: "2026-06-22"}
- {id: 6, title: "GPT-5.5 model page (cost-to-run, tokens)", url: "https://artificialanalysis.ai/models/gpt-5-5", source: Artificial Analysis, date: "2026-06-22"}
- {id: 7, title: "Claude Opus 4.8 model page (cost-to-run)", url: "https://artificialanalysis.ai/models/claude-opus-4-8", source: Artificial Analysis, date: "2026-06-22"}
- {id: 8, title: "Claude Opus 4.8 — model overview (context, pricing, modalities)", url: "https://platform.claude.com/docs/en/about-claude/models/overview", source: Anthropic, date: "2026-06-22"}
- {id: 9, title: "GPT-5.5 — model reference (context, cutoff, modalities)", url: "https://developers.openai.com/api/docs/models/gpt-5.5", source: OpenAI, date: "2026-06-22"}
- {id: 10, title: "z.ai API pricing", url: "https://docs.z.ai/guides/overview/pricing", source: "Z.ai docs", date: "2026-06-16"}
- {id: 11, title: "Claude API pricing", url: "https://platform.claude.com/docs/en/about-claude/pricing", source: Anthropic, date: "2026-06-22"}
- {id: 12, title: "OpenAI API pricing", url: "https://developers.openai.com/api/docs/pricing", source: OpenAI, date: "2026-06-22"}
- {id: 13, title: "SWE-bench Verified — independent leaderboard", url: "https://www.vals.ai/benchmarks/swebench", source: "Vals AI", date: "2026-06-17"}
- {id: 14, title: "Terminal-Bench 2.1 leaderboard (Terminus-2 harness)", url: "https://www.tbench.ai/leaderboard/terminal-bench/2.1", source: "tbench.ai", date: "2026-06-22"}
- {id: 15, title: "Introducing Claude Opus 4.8 (benchmarks + harness disclosure)", url: "https://www.anthropic.com/news/claude-opus-4-8", source: Anthropic, date: "2026-05-28"}
- {id: 16, title: "Z.ai's GLM-5.2 beats GPT-5.5 on long-horizon coding for 1/6th the cost", url: "https://venturebeat.com/technology/z-ais-open-weights-glm-5-2-beats-gpt-5-5-on-multiple-long-horizon-coding-benchmarks-for-1-6th-the-cost", source: VentureBeat, date: "2026-06-13"}
- {id: 17, title: "GLM-5.2 model guide (vendor benchmark table)", url: "https://docs.z.ai/guides/llm/glm-5.2", source: "Z.ai docs", date: "2026-06-13"}
- {id: 18, title: "Claude Opus 4.8 benchmarks explained (HLE, GPQA)", url: "https://www.vellum.ai/blog/claude-opus-4-8-benchmarks-explained", source: Vellum, date: "2026-05-29"}
- {id: 19, title: "LM Council benchmarks (FrontierMath, aggregating Epoch/AA)", url: "https://lmcouncil.ai/benchmarks", source: "LM Council", date: "2026-06"}
- {id: 20, title: "Zhipu's GLM-5.2 closes in on closed-source leaders in coding marathons", url: "https://the-decoder.com/zhipu-ais-glm-5-2-closes-in-on-closed-source-leaders-in-coding-marathons/", source: The Decoder, date: "2026-06-16"}
- {id: 21, title: "GLM-5.2 becomes the top open-weight model on Artificial Analysis", url: "https://www.implicator.ai/glm-5-2-becomes-the-top-open-weight-model-on-artificial-analysis/", source: Implicator AI, date: "2026-06-18"}
- {id: 22, title: "Claude Opus 4.8 vs GPT-5.5 (GraphWalks long-context)", url: "https://www.datacamp.com/blog/claude-opus-4-8-vs-gpt-5-5", source: DataCamp, date: "2026-06"}
- {id: 23, title: "Z.ai launches GLM-5.2 with a usable 1M-token context and no benchmarks at launch", url: "https://www.marktechpost.com/2026/06/14/z-ai-launches-glm-5-2-with-a-usable-1m-token-context-two-thinking-effort-levels-and-no-benchmarks-at-launch/", source: MarkTechPost, date: "2026-06-14"}
- {id: 24, title: "AINews: GLM-5.2, the top frontend coding model", url: "https://www.latent.space/p/ainews-glm-52-the-top-frontend-coding", source: "Latent.Space / AINews", date: "2026-06-17"}
- {id: 25, title: "GLM-5.2 benchmarks: open weights vs Claude Opus (Code Arena)", url: "https://www.digitalapplied.com/blog/glm-5-2-benchmarks-open-weights-vs-claude-opus", source: Digital Applied, date: "2026-06-18"}
- {id: 26, title: "Multimodal AI benchmarks 2026 (vision, audio, code)", url: "https://www.digitalapplied.com/blog/multimodal-ai-benchmarks-2026-vision-audio-code", source: Digital Applied, date: "2026-04"}
- {id: 27, title: "GLM-5.2 — first impressions (text-only)", url: "https://simonwillison.net/2026/Jun/17/glm-52/", source: "Simon Willison", date: "2026-06-17"}
- {id: 29, title: "ChinaBench: open-source LLM censorship benchmark results", url: "https://adam.holter.com/chinabench-open-source-llm-censorship-benchmark-results-across-qwen-glm-kimi-minimax-deepseek-and-gpt-oss/", source: "Adam Holter", date: "2026-02"}
- {id: 30, title: "Censorship in China-originating large language models", url: "https://academic.oup.com/pnasnexus/article/5/2/pgag013/8487339", source: "PNAS Nexus", date: "2026"}
- {id: 31, title: "GLM-5.2 self-host: vLLM hardware & cost", url: "https://ofox.ai/blog/glm-5-2-self-host-vllm-hardware-cost-2026/", source: "ofox.ai", date: "2026-06"}
- {id: 32, title: "Deploy GLM-5.2 on GPU cloud (cost & break-even)", url: "https://www.spheron.network/blog/deploy-glm-5-2-gpu-cloud/", source: "Spheron", date: "2026-06"}
- {id: 33, title: "GLM-5.2 vs DeepSeek V4 Pro (price, capability)", url: "https://codingfleet.com/blog/glm-5-2-vs-deepseek-v4-pro/", source: CodingFleet, date: "2026-06"}
- {id: 34, title: "Most popular AI models on OpenRouter, June 2026", url: "https://officechai.com/miscellaneous/these-are-the-most-popular-ai-models-on-openrouter-june-2026/", source: OfficeChai, date: "2026-06-17"}
- {id: 35, title: "Harvey × Trajectory: post-training Nemotron into the frontier band", url: "https://trajectory.ai/field-notes/harvey-nemotron-3-ultra", source: "Trajectory", date: "2026-06-09"}
- {id: 36, title: "Anthropic model deprecations", url: "https://platform.claude.com/docs/en/about-claude/model-deprecations", source: Anthropic, date: "2026-06-22"}
- {id: 37, title: "OpenAI winding down the fine-tuning API and platform", url: "https://community.openai.com/t/openai-is-winding-down-the-fine-tuning-api-and-platform-discussion-thread/1380522", source: "OpenAI Developer Community", date: "2026-05-07"}
- {id: 38, title: "Sam Altman addresses bumpy GPT-5 rollout (autoswitcher)", url: "https://techcrunch.com/2025/08/08/sam-altman-addresses-bumpy-gpt-5-rollout-bringing-4o-back-and-the-chart-crime/", source: TechCrunch, date: "2025-08-08"}
- {id: 39, title: "Code Arena: Frontend — GLM-5.2 ranking", url: "https://x.com/arena/status/2066957802741043641", source: "Arena.ai (X)", date: "2026-06-16"}
- {id: 40, title: "GLM-5.2 at 1M context on 8×H200 (KV cache reality)", url: "https://phala.com/posts/glm-5-2-1m-context-8xh200", source: Phala, date: "2026-06"}
- {id: 41, title: "SGLang cookbook: GLM-5.2 deployment & throughput", url: "https://lmsysorg.mintlify.app/cookbook/autoregressive/GLM/GLM-5.2", source: "SGLang / LMSYS", date: "2026-06"}
- {id: 42, title: "FrontierMath", url: "https://epoch.ai/frontiermath", source: "Epoch AI", date: "2026-06"}
:::
