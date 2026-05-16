---
eyebrow: Compute Economics · Inference Silicon
title: 'Wafer or Rack: the real cost-per-token economics of Cerebras WSE-3 versus Nvidia GB200'
deck: Cerebras sells the fastest single-stream tokens money can buy. Nvidia sells the cheapest tokens
  per dollar of capex at scale. They are not the same product — and the prices reflect it.
lede: A wafer-scale chip with 44 GB of on-die SRAM[^1] and a 72-GPU liquid-cooled rack with 13.4 TB of
  HBM3e[^12] are now the two ends of the merchant-inference spectrum. Cerebras priced its May 2026 IPO
  at $185 a share and raised $5.55 billion[^45] on a story that wafer-scale memory bandwidth bends the
  cost-per-token curve. Nvidia's data-center segment did $62.3 billion in Q4 of FY26 alone at 75.0% GAAP
  gross margin[^47]. Both numbers can be true. They describe different workloads.
stats:
- label: WSE-3 SRAM
  value: '44 GB'
  note: '21 PB/s on-die BW[^2]'
- label: NVL72 HBM
  value: '13.4 TB'
  note: '576 TB/s aggregate[^12]'
- label: '405B speed (Cerebras)'
  value: '969 tok/s'
  note: at $6 in / $12 out per Mtok[^6]
- label: '405B per-GPU (MLPerf v5.1)'
  value: '170 tok/s'
  note: GB200 server scenario[^20]
- label: NVL72 rack power
  value: ~120 kW
  note: Nvidia spec, liquid cooling[^36]
- label: CS-3 power
  value: '23 kW'
  note: per 15-16U system[^4]
---

This essay does the comparison from first principles. It distinguishes the unit economics of a single CS-3 system from the unit economics of a GB200 NVL72 rack; it pulls the per-GPU MLPerf v5.1 numbers Nvidia itself publishes[^20]; it traces market prices on Cerebras, Groq, Together, Fireworks, DeepInfra and Replicate[^24,25,26,27,28]; and it asks what would have to break for either thesis to fail. The short version: **Cerebras owns latency-bounded, decode-dominated, small-batch workloads where the model fits on a wafer. Nvidia owns everything else, which today is almost everything.**

## 01. Two products, one taxonomy

Both companies sell "an AI accelerator," but the architectural choice points in opposite directions. The WSE-3 puts all of its memory on the silicon die — 44 GB of SRAM, 900,000 cores, 46,225 mm² of substrate, all on a single TSMC 5nm wafer[^1,2]. Aggregate on-die bandwidth is 21 PB/s[^3]. Off-package I/O is only ~150 GB/s[^55]. The B200 die in the GB200 superchip, by contrast, ships with 192 GB of HBM3e at ~8 TB/s per GPU[^12], and an NVL72 rack stitches 72 of them together with fifth-generation NVLink — 130 TB/s of switch-domain bandwidth and 13.4 TB of pooled HBM[^12].

The two memory hierarchies invert each other. Cerebras has roughly 2,600× the per-chip memory bandwidth of one B200 — but ~300× less capacity than one NVL72 rack. The choice cascades into every other design decision: cooling (closed-loop water for one CS-3[^3] vs. rack-level direct-to-chip liquid plus air for NVL72[^36]); software (Cerebras's compile-time mapping vs. Nvidia's CUDA/TensorRT-LLM/Dynamo runtime[^51]); and what a buyer actually pays per workload class.

| Metric | Cerebras CS-3 | Nvidia GB200 NVL72 | Ratio |
|---|---|---|---|
| Process node | TSMC 5nm[^1] | TSMC 4NP (Blackwell)[^11] | — |
| Transistors | 4 trillion (one die)[^1] | 208B × 72 dies ≈ ~15 T[^11] | ~4× |
| Compute cores | 900,000[^1] | 72 Blackwell GPUs[^12] | — |
| Fast memory | 44 GB SRAM[^1] | 13.4 TB HBM3e[^12] | 304× (Nvidia) |
| Memory bandwidth | 21 PB/s on-die[^3] | 576 TB/s aggregate[^12] | 36× (Cerebras) |
| Off-package I/O | ~150 GB/s[^55] | 1.8 TB/s NVLink per GPU[^13] | ~860× (Nvidia) |
| Power | ~23 kW[^4] | ~120 kW[^36] | ~5× |
| Form factor | 16RU per system[^3] | One 42–48U rack[^12] | — |

The honest framing isn't "which is better." It's: *where on the roofline does your workload sit?*

## 02. Roofline: why decode is bandwidth-bound and prefill is compute-bound

An LLM inference request has two phases. Prefill ingests the prompt as one big matrix-matrix multiply against the weights — it saturates compute[^51]. Decode is the autoregressive loop that emits one output token at a time. Each decode step is a matrix-vector multiply against the same weights, and at low batch size it spends most of its wall-clock moving model parameters from memory into the multiply-accumulate units[^30].

The published arithmetic-intensity figures make the regime concrete. A roofline analysis of Llama-2-7B decode layers measures ~1.0 FLOP/byte for the q/k/v/o projections and MLPs[^30]. The hardware ridge point — the FLOPs-per-byte at which compute and memory become equally constrained — sits near 300 FLOPs/byte for an H100[^31]. In other words, batch-1 decode runs two orders of magnitude inside the memory-bound corner of the roofline. Bandwidth dominates wall time; FLOPs sit idle.

This is the regime where Cerebras's design choice pays off. With 21 PB/s of on-wafer bandwidth feeding a model whose weights live in SRAM, the per-stream decode rate is unconstrained by any HBM-stack-count physics. The fielded result is the 969 tokens/sec on Llama 3.1 405B that Cerebras advertises[^6] and the 2,100+ tok/s number on Llama 3.1 70B[^50]. Artificial Analysis independently measured Cerebras at ~2,360 tok/s on Llama 3.1 8B and over 2,600 tok/s on Llama 4 Scout — "the highest measured across all providers"[^22].

The counterpoint, as ML systems researcher Tim Dettmers framed it in a widely-quoted November 2024 post, is that those wins are batch-1 wins: ==paraphrasing== "Cerebras is fast at batch size 1 and slow at batch size n; GPUs are the inverse"[^63]. Decode arithmetic intensity rises roughly linearly with batch size[^31]; modern continuous batching frameworks like vLLM lift GPU decode throughput 2–4× over the prior state of the art at the same latency[^52], and Anyscale measured ~23× for vLLM (continuous batching combined with PagedAttention) over a naive static baseline[^53]. By a batch of 32 or more, a GPU has crossed out of the memory-bound regime; its per-stream tokens-per-second drops, but per-GPU throughput climbs sharply. Nvidia's own MLPerf v5.0 reporting showed the same shape one generation earlier — B200 hitting ~98,400 tok/s on Llama 2 70B server scenario across an 8-GPU node, roughly 3× H200[^16].

Why this matters: if your product is a chat interface where one user is waiting for one stream, the Cerebras curve looks decisive. If your product is millions of concurrent requests behind a load balancer, the same workload converts to a GPU continuous-batching problem where Nvidia's HBM capacity earns its keep.

## 03. MLPerf v5.1: the only apples-to-apples table in town

Cerebras has never submitted to MLPerf Inference. Neither has Groq, nor SambaNova. The v5.1 results announcement from September 2025 listed 27 submitters — Nvidia, AMD, Intel, Google, and others — without any of the SRAM-architecture vendors[^19]. The most charitable read is that MLPerf takes engineering effort and brings in no revenue when chips are sold out. The skeptical read is that MLPerf's server and interactive scenarios — Poisson arrivals with TTFT and per-token latency caps[^21] — would expose how the batch-1 marketing numbers degrade under realistic load.

Nvidia's submitted v5.1 per-GPU numbers, audited by MLCommons, are the closest thing to an apples-to-apples reference:

| Workload | Offline (tok/s/GPU) | Server (tok/s/GPU) | Interactive (tok/s/GPU) |
|---|---|---|---|
| Llama 2 70B (99.9%) | 12,934[^20] | 12,701[^20] | 7,856[^20] |
| Llama 3.1 405B | 224[^20] | 170[^20] | 138[^20] |
| Mixtral 8×7B | 16,099[^20] | 16,131[^20] | — |

Two things jump off the page. First, the 405B interactive number (138 tok/s/GPU) is ~38% below the offline figure — that's the price the GB200 NVL72 pays for honoring chat-style latency budgets at 12.5 tokens/sec/user and a 4.5-second TTFT cap[^20]. That gap is exactly where Cerebras's per-stream lead would manifest in an MLPerf-style comparison, if they submitted. Second, on Llama 2 70B the per-GPU throughput is so high — 12,701 tok/s/GPU server — that multiplying across a 72-GPU rack approximates Microsoft Azure's published "over 860,000 tok/s on Llama 70B" for the same rack[^15,14]. The two figures triangulate.

The counterclaim is that MLPerf's offline mode is a throughput contest with no user-perceived latency anchor, and that its server mode uses Poisson arrivals that don't model agent loops or RAG pipelines. That's fair — but it remains the only third-party-audited number anyone can cite, and Cerebras's absence is informative.

## 04. List prices: what customers actually pay per million tokens

Headline architecture stories collapse into pricing on the public API pages. Here is the merchant inference market at list, as of early 2026:

| Model | Cerebras | Groq | DeepInfra | Together | Fireworks |
|---|---|---|---|---|---|
| Llama 3.1 / 3.3 8B (in / out, $/Mtok) | 0.10 / 0.10[^5] | 0.05 / 0.08[^24] | 0.02 / 0.05[^27] | ~0.10 flat[^25] | tiered[^26] |
| Llama 3.3 70B | 0.85 / 1.20[^22,23] | 0.59 / 0.79[^24] | 0.10 / 0.32[^27] | ~0.88 flat[^25] | 0.90 (16B+ tier)[^26] |
| Llama 3.1 405B | 6.00 / 12.00[^6] | not offered[^24] | not offered[^27] | ==3.50 / 3.50 (historical; may have been delisted)==[^25] | 3.00 / 3.00[^26] |
| DeepSeek-R1 (reasoning) | — | — | 0.50 / 2.15[^27] | — | 0.55 / 2.19[^26] |

Three findings worth pulling out. First, Cerebras's structural premium widens with model size. At 8B they match Groq and sit 2–5× DeepInfra. At 70B they are several multiples of DeepInfra's $0.10/$0.32 floor[^27] and ~1.5× Groq. At 405B they are 3.4× Fireworks's price for the output token — and Groq doesn't compete at 405B at all because their LPU's 230 MB of SRAM[^56] won't host the model economically. Cerebras is selling speed, and the speed premium is real but explicit.

Second, output tokens cost much more than input for reasoning models — DeepSeek-R1 at DeepInfra is 4.3× more expensive to emit than to ingest[^27]; at Fireworks the multiplier is 4.0×[^26]. That's the cost of hidden chain-of-thought generation, and it's the workload class that most plays to bandwidth-rich architectures because the wall time really is decode-dominated.

Third, DeepInfra is the price floor — and they don't host 405B. The lowest-cost serious provider has voted with their menu that 405B isn't economic at scale; only the speed-tier specialists (Cerebras at $12 out) and the throughput shops with idle Blackwell capacity (Together, Fireworks at $3.00–3.50) keep it lit. The market is signaling that 405B is a niche.

:::callout(kind=info, label=Methodology)
All prices above are list rates fetched from each provider's pricing page in early 2026. Enterprise rates and committed-spend discounts are not disclosed publicly. Fireworks publishes 50% batch and cached-input discounts; DeepInfra offers ~30% on cached input[^26,27]. Replicate, the most expensive provider on a token basis, prices most non-LLM models per GPU-second rather than per token[^28].
:::

## 05. The capex denominator: hardware unit costs

Neither vendor publishes a list price. The best public proxy for the GB200 NVL72 rack is an HSBC analyst estimate of ~$3M per fully equipped rack, with per-GPU Blackwell pricing reported by trade press in the $30–70K range[^18]. SemiAnalysis, drawing on supply-chain primaries (paywalled), reports ~$3.9M per NVL72 rack with 1,200 W per chip versus 700 W for an H100, and calculates TCO/GPU at roughly 1.6× the H100 — with throughput uplifts that net to a lower cost per token at modern utilization[^39]. ==SemiAnalysis figures cited from publicly visible newsletter previews; the underlying spreadsheet sits behind a subscriber paywall.==

For Cerebras, secondary estimates of the CS-3 system price cluster around $2–3M, but Cerebras does not publish it and the S-1 does not break out per-system economics. What it does disclose is that 64 CS-3 systems make up Condor Galaxy 3[^10]; ==unverified: third-party reporting of $300–400M for that build implies $2–4M per system but is not a Cerebras-published number==. A serving cluster of 20 CS-3 systems — what a third-party arithmetic from The Next Platform argues you need to hold Llama 405B in SRAM[^35] — therefore sits in the tens of millions of dollars before networking and the data-center shell. Twenty B200s — enough to serve the same model with HBM headroom to spare — list at well under $1M of silicon by Huang's own number[^18].

This is the core of the skeptical TCO critique on Hacker News: that the 2.5× single-stream speed Cerebras buys on Llama 4 Maverick comes — by one Hacker News commenter's arithmetic — at as much as ~80× in capex per equivalent serving slot[^65]. The counterclaim is that the right denominator isn't capex per serving slot but capex amortized over the speed premium a buyer can charge — i.e. Cerebras's $12-per-Mtok output token at 969 tok/s is selling something Together's $3.50-per-Mtok 50-tok/s endpoint can't sell at any price. Both can be true at once.

## 06. Power, cooling, and tokens-per-kWh

An NVL72 rack draws ~120 kW according to Nvidia's own DGX user guide[^36], with the compute trays cooled by direct-to-chip liquid and networking/storage cooled by air. Meta's ORv3 rack design supports up to 140 kW liquid-cooled, the highest publicly disclosed AI-rack envelope[^37]. A CS-3 system is rated at 23 kW for 16U[^4], with a proprietary closed water loop[^3]. By rack density, a fully populated 48U cabinet of CS-3 systems (three units) approaches ~70 kW; an NVL72 rack delivers more compute and more memory in a single chassis but at nearly 2× the power.

Industrial electricity in the major US AI corridors as of February 2026 ran 7.07¢ (Arizona) to 9.98¢ (Virginia) per kWh[^38]; hyperscalers negotiate sub-average PPA rates closer to 4–6¢. ==No primary-source tokens-per-kWh benchmark across CS-3, GB200 and H100 at matched batch sizes and model sizes has been published as of mid-2026.== An H100-only measurement in the TokenPowerBench paper found ~0.39 J per total token at vLLM batch 128 with FP8 — roughly 108 Wh per million tokens[^40]. Cerebras's own marketing positions CS-3 at "1/3 lower cost" and "21× faster" than a DGX B200 on selected gpt-oss workloads[^41], but the numbers are single-user comparisons that the company chose; no independent reproduction yet exists.

:::callout(kind=warn, label="What would falsify this")
If MLCommons publishes a v6.0 round in which Cerebras submits an audited Llama 3.1 405B server result that exceeds 200 tok/s/system at MLPerf's latency cap, the "batch-1 only" critique collapses for that model. Conversely, if a third party publishes a tokens-per-kWh comparison showing CS-3 within 50% of GB200 NVL72 at production batch sizes, the speed-premium pricing becomes much harder for Cerebras to defend.
:::

## 07. The memory ceiling: what fits, and what doesn't

SRAM has roughly three orders of magnitude more bandwidth per byte than HBM, and roughly three orders of magnitude less capacity per dollar. That tradeoff has hard consequences for which models can run economically on a wafer.

The arithmetic, per third-party reporting, is that one CS-3 holds 44 GB; Llama 3.1 70B in FP16 needs ~140 GB just for weights — roughly four CS-3 systems just to fit the parameters[^35]. Llama 3.1 405B needs ~18–20 systems; DeepSeek-V3 671B would need 30+, before any KV cache[^35]. The KV cache for a single Llama-3-70B request at 128k tokens — with GQA — runs ~40 GB in BF16[^32], almost exactly the WSE-3 SRAM budget for one concurrent user.

Two observations follow. First, the inflection between "Cerebras wins" and "Cerebras struggles" sits at the boundary where the model+KV exceeds on-wafer SRAM and the workload spills to off-package storage at 150 GB/s[^55]. SemiAnalysis has argued that KV-cache transfer takes "several milliseconds" in that regime — enough to materially hurt TTFT and crush batching[^55]. Second, SRAM scaling has essentially flatlined past 5nm: WSE-3 added only ~10% SRAM over WSE-2 while logic scaled ~50% on the same TSMC node change[^55]. The capacity gap with HBM is not a transient — it's structural for the next several process generations.

HBM pricing is the other lever. TrendForce reports HBM3e at ~$300 per 36 GB stack pre-2026, with Samsung and SK hynix raising prices ~20% for 2026[^33]. A B200's 192 GB (eight 24-GB stacks) carries on the order of $1,600–2,000 in HBM at that rate. A TSMC N5 wafer carries ~$17–18.5k per 300 mm wafer[^34], of which Cerebras enables ~93% via per-core redundancy[^29]. The wafer-scale design is BoM-efficient at silicon; the HBM-attached design is capacity-efficient at memory.

What it means for the buyer: if your serving target is a frontier-class model (≥400B dense, ≥600B MoE), the per-token economics on Cerebras involve a multi-system pipeline that, per SemiAnalysis, "goes against the entire ethos of the wafer"[^55]. Notably, Cerebras's own production cloud catalog tops out at gpt-oss 120B, and the original Llama 3.1 70B and 405B endpoints were deprecated[^55] — the menu is the tell.

## 08. Workload shape determines the winner

From the roofline plus the capacity ceiling, the workload taxonomy is straightforward.

- **Long-prompt RAG, short-output classification.** Prefill-dominated. The matrix-matrix multiply against a long sequence is FLOPs-bound. Nvidia's compute density per dollar wins.
- **High-concurrency batch inference behind a load balancer.** Continuous batching lifts GPU decode throughput 2–4× vs. prior baselines[^52]; per-GPU tokens-per-second on Llama 2 70B sit at ~12,700 in MLPerf server mode[^20]. Nvidia wins on cost-per-token at scale.
- **Single-stream interactive chat at low latency.** Decode-dominated, batch-1. Cerebras's 21 PB/s on-wafer bandwidth is structurally hard to beat. The 1,200 tok/s Perplexity Sonar build[^8] and 1,100+ tok/s Mistral Le Chat Flash Answers[^7] are the proof points.
- **Reasoning models with long hidden chains of thought.** Decode explodes 5–20× per visible answer. The output-token premium across providers — 4× on R1[^27,26] — captures this. In principle, this is the regime where Cerebras's per-stream speed is most economically valuable; in practice, Cerebras has not yet productized DeepSeek-V3 or Kimi K2 on its public cloud[^55].
- **Agentic loops with many sequential turns.** Each turn's wall time is dominated by decode tokens. Cerebras claims a 10-step agent chain drops from 30+s on GPU at 50 tok/s to under 3s at 1,200 tok/s[^54] — the architectural point is right, the magnitude is vendor-flavored.
- **Long-context (128k+).** KV-cache memory dominates. The 40 GB-per-user KV figure for Llama 3 70B[^32] is benign on a 13.4 TB NVL72 rack and adversarial on a 44 GB WSE-3. Nvidia wins.

The honest statement of Cerebras's wedge is that it's narrow but real: *latency-bounded, decode-dominated, low-concurrency workloads on models small enough to fit on the wafer.* Chat UIs for premium products fit that description. Backend RAG at scale does not.

## 09. Customer base: where the revenue actually comes from

The marketing momentum and the financial reality diverge. Cerebras's S-1 amendment for the April 2026 refile shows 2025 revenue of ~$510M, of which roughly 24% came from G42 and 62% from Mohamed bin Zayed University of Artificial Intelligence (MBZUAI), a G42-related party — combined ~86% UAE concentration[^46]. The headline 2025 GAAP net income of $237.8M is dominated by a $363.3M one-time non-cash gain from extinguishing a G42 forward-contract liability; on a non-GAAP basis, Cerebras lost $75.7M in 2025, a 247% deterioration from 2024[^46]. GAAP operating loss was $145.9M[^46]. The original September 2024 S-1 had disclosed 2023 revenue of $78.7M and net loss of $127.2M, with G42 at 83% of revenue and rising to 87% in H1 2024[^43,42].

The named Western customer wins are real but small. Mistral runs Le Chat Flash Answers on CS-3 for 1,100+ tok/s on Mistral Large 2[^7]; Perplexity Sonar runs on CS-3 for 1,200 tok/s on a Llama 3.3 70B fine-tune[^8]; Meta's Llama API offers Cerebras as one of several inference back-ends for Llama 4 Scout[^9]. None of these arrangements has had its dollar value disclosed. The disclosed $20B+ multi-year OpenAI master agreement is forward-commit only, with deployment through 2028[^46].

Cerebras announced six new datacenters across North America and Europe in March 2025, including ~300 CS-3 systems in Oklahoma City and a Cerebras-owned Montreal site[^61]; G42 and India's C-DAC formalized a framework in May 2026 for a 64-system Condor Galaxy India build[^62]. The IPO on May 14, 2026 priced at $185 — well above the $150–160 marketed range — for ~30M shares and $5.55B raised, with first-day close of $311.07 (+68%) and intraday peak of $385 (+108%)[^45].

On the Nvidia side, the contrast is roughly two orders of magnitude. Q4 FY26 data-center revenue was $62.3B (+75% YoY), with full-year FY26 DC at $193.7B; Q4 GAAP gross margin was 75.0%; Q1 FY27 revenue guidance was $78B[^47]. By the Q3 FY26 call (November 2025), GB300 shipments had crossed GB200 and accounted for roughly two-thirds of Blackwell revenue, with Hopper down to ~$2B per quarter[^48]. Nvidia's 10-K for FY26 disclosed that two direct customers accounted for 36% of revenue and the top four for 61%; the top five end-customer hyperscalers were ~50%+ of revenue[^49]. CoWoS packaging capacity at TSMC is the binding supply constraint into 2026, with Nvidia booking the majority of available slots — a consensus view across supply-chain reporting and Nvidia partner-cloud announcements[^17].

| Quantity | Cerebras (2025, S-1) | Nvidia DC (Q4 FY26) |
|---|---|---|
| Revenue | $510M (full year)[^46] | $62.3B (one quarter)[^47] |
| GAAP gross margin | thin / improving (~40% hardware)[^43] | 75.0%[^47] |
| Customer concentration | 86% UAE-related[^46] | ~50% to top 5 hyperscalers[^49] |
| GAAP net income | $237.8M (incl. $363.3M one-time gain)[^46] | Full FY26 total revenue $130.5B prior year reference point[^47] |

## 10. The other non-Nvidia options

Cerebras isn't the only or even the largest non-Nvidia inference fleet. Two captive fleets dwarf every merchant alternative: Google's TPU (Trillium v6e for Gemini 2.0 serving, "nearly 2×" per-chip inference throughput on Llama 2 70B vs. v5e per Google's own numbers[^59]) and AWS Trainium2 under Project Rainier (~500K chips deployed by November 2025, targeting >1M for Anthropic by year-end)[^60]. These together likely serve more daily inference tokens than every merchant non-Nvidia accelerator combined.

Among speed specialists, Groq is Cerebras's most direct competitor — SRAM-only LPU, ~230 MB on-chip ==(vendor architecture summary; not on the cited blog directly)==, 276 tok/s baseline on Llama 3.3 70B[^56], priced at $0.59 in / $0.79 out per Mtok[^24]. Cerebras's own competitive piece argues 2,500 tok/s vs. Groq's ~403 tok/s on Llama 3.3 70B at "similar or up to ~50% higher" pricing[^22]. SambaNova's SN40L combines a tiered memory hierarchy (HBM3 + DDR5 + on-package SRAM) aimed at serving the largest models, with vendor-reported 457 tok/s on Llama 3.1 70B and 129 tok/s on 405B[^57].

The most consequential merchant competitor remains AMD. The MI355X, per AMD's own MLPerf Inference 6.0 submission, claims parity with B200 in offline, 97% in server, and 119% in interactive on Llama 2 70B[^58]. That is the first time merchant silicon has reached parity with Nvidia on the standard MLPerf benchmark. AMD's pricing has historically been ~30% below Nvidia at like-for-like; if the parity holds at GA volume, AMD becomes the natural pressure point on Nvidia's gross margin, not Cerebras.

A short interpretive note: Cerebras is competing with Groq for the speed-bracket niche, not with Nvidia for the throughput market. The right competitive comparison is "Cerebras vs. Groq vs. SambaNova," and on the financial scoreboard Cerebras's $66B post-IPO market cap[^45] is ==unverified-precision: roughly an order of magnitude above widely-reported private valuations for Groq (~$6.9B) and SambaNova (~$2.2B, down from a $5.1B peak); specific multiples depend on the round cited.== The divergence reflects revenue traction the others don't have publicly — but also a market betting that Cerebras has uniquely cracked something Groq and SambaNova haven't, which is a thesis the underlying customer-concentration disclosures don't yet support.

## 11. Three serious counter-arguments to the Cerebras thesis

I've sprinkled counterpoints through the sections. Here are the three that, if they prove out, are most likely to compress the bull case.

**(a) Nvidia's software stack closes the gap.** Speculative decoding, multi-token prediction, and disaggregated prefill-vs-decode serving via Dynamo and TensorRT-LLM are systematically eating into the per-stream latency where Cerebras leads. Nvidia's published Blackwell Ultra (B300) writeup advertises generational gains of "up to 50× higher AI factory output" on reasoning-model workloads at low-latency targets versus Hopper[^64]. The Cerebras lead at batch 1 is more defensible architecturally than the lead at batch 8 or 16.

**(b) The wedge workload doesn't generalize.** Cerebras has not productized DeepSeek-V3, Kimi K2, or any frontier-class MoE model on its public cloud[^55]. The deprecation of Llama 3.1 70B and 405B from the active catalog[^55] suggests that, at production utilization, those endpoints did not earn their wafer count. If the frontier keeps moving toward sparse MoE models with high-capacity expert pools and long context, the on-wafer-only architecture becomes a worse fit, not a better one.

**(c) Revenue concentration is structural, not transitional.** The CFIUS-driven restructuring of G42's stake to non-voting[^44] removed the regulatory blocker on the IPO, but the underlying customer concentration just reshuffled inside the same group of UAE-related entities — 24% G42 + 62% MBZUAI in 2025[^46]. Western customers like Mistral and Perplexity are marketing wins; the dollar volume isn't visible in revenue mix. If the OpenAI master-agreement deployment slips, or if a future US administration revisits UAE export-control posture, the demand side becomes thin.

:::callout(kind=danger, label=Risk)
The thinnest part of the bull case isn't the chip — it's that 86% of revenue ties to two UAE-related entities with overlapping ownership[^46], and that the headline 2025 GAAP profit is a one-time accounting gain[^46]. The wafer is interesting; the customer book is fragile.
:::

## 12. What this means for buyers and operators

The practical framing for an inference buyer in mid-2026 is a decision tree, not a vendor preference.

- **If you're serving frontier-class models (≥400B dense, ≥600B MoE) at any meaningful concurrency:** GB200 NVL72 or its successor (GB300/Rubin) is the default. The HBM capacity per rack is the dominant constraint.
- **If you're serving chat/agent products where end-to-end latency is the differentiator and the model is in the 8–120B range:** Cerebras or Groq is plausible, with Groq cheaper at the low end and Cerebras faster at the top end. Validate the production batch-size assumption — many "single-stream" products actually have meaningful concurrent demand and convert to a GPU-batching problem on closer inspection.
- **If your workload is RAG-heavy, long-context, or prefill-dominated:** Nvidia. The arithmetic intensity of prefill rewards FLOPs density.
- **If you care most about cost per output token at large batch:** DeepInfra-class providers on cheaper Nvidia capacity (H100/H200) often beat the bleeding-edge B200/GB200 deployments because the buyer is paying for amortized older capex.
- **If you're a hyperscaler with sovereign-AI customers and an Arabic-Gulf relationship:** Cerebras is a credible vendor today partly *because* G42 and MBZUAI underwrote it through three years of revenue.

The cost-per-token contest as a generic horse race obscures more than it reveals. The numbers that decide it are workload-specific: what's the model size, what's the prompt-to-completion ratio, what's the concurrency, what's the latency budget, what's the context length. Cerebras has built the best chip in the world for one quadrant of that space. Nvidia has built the most economically dominant rack in the history of computing for the other quadrants.

## 13. Bottom line

Two true sentences, neither of which contradicts the other.

One: at batch 1, on a 70B-class model that fits on a wafer, Cerebras delivers throughput per stream that Nvidia cannot match at any price, and the Mistral, Perplexity, and Meta Llama API integrations are real evidence that there is a paying market for that capability[^7,8,9].

Two: at the throughput / concurrency / capacity scale where the inference market actually sells most of its tokens, GB200 NVL72 — and increasingly GB300 — delivers per-GPU MLPerf results that no merchant competitor has yet matched on an audited basis[^20], sustains ~75% gross margins on $62.3B of quarterly data-center revenue[^47], and faces real but bounded competition from AMD's MI355X[^58], AWS Trainium2[^60], and Google's TPU[^59] — none of which is Cerebras.

The right framing for the next 18 months isn't "Cerebras vs. Nvidia." It's: *which workloads, at which latencies, on which model classes, defect from the Nvidia stack to one of the speed specialists* — and how fast does Nvidia's own software stack (Dynamo, MTP, disaggregated serving[^64]) close that defection window. The answer determines whether Cerebras's $66B post-IPO valuation is a generational pricing of a wafer-scale inflection, or a richly-funded niche player whose moat is the diameter of one TSMC reticle.

---

## 14. References

:::references
- id: 1
  title: Cerebras Systems, "Cerebras Announces Third Generation Wafer-Scale Engine," press release, March
    13, 2024
  url: https://www.cerebras.ai/press-release/cerebras-announces-third-generation-wafer-scale-engine
- id: 2
  title: Samuel K. Moore, "Cerebras Introduces Its 2.6-Trillion Transistor AI Chip," IEEE Spectrum, March
    13, 2024
  url: https://spectrum.ieee.org/cerebras-chip-cs3
- id: 3
  title: Cerebras Systems, "Cerebras CS-3 System," product page
  url: https://www.cerebras.ai/system
- id: 4
  title: Cerebras Systems, "Introducing the Cerebras CS-3," blog post, March 12, 2024
  url: https://www.cerebras.ai/blog/cerebras-cs3
- id: 5
  title: Cerebras Systems, "Cerebras Launches the World's Fastest AI Inference," press release, August
    27, 2024
  url: https://www.cerebras.ai/press-release/cerebras-launches-the-worlds-fastest-ai-inference
- id: 6
  title: Cerebras Systems, "Cerebras Inference Now Generates 969 Tokens/s on Llama 3.1-405B," press release,
    November 18, 2024
  url: https://www.cerebras.ai/press-release/cerebras-inference-llama-405b
- id: 7
  title: 'Cerebras Systems, "Mistral Le Chat: Now with Cerebras Inference," blog, February 6, 2025'
  url: https://www.cerebras.ai/blog/mistral-le-chat
- id: 8
  title: Cerebras Systems, "Cerebras Powers Perplexity Sonar with Industry's Fastest AI Inference," press
    release, February 11, 2025
  url: https://www.cerebras.ai/press-release/cerebras-powers-perplexity-sonar-with-industrys-fastest-ai-inference
- id: 9
  title: Cerebras Systems, "Meta Unleashes Llama API," news post, April 29, 2025
  url: https://www.cerebras.ai/news/meta-unleashes-llama-api-running-18x-faster-than-openai-cerebras-partnership-delivers-2-600
- id: 10
  title: Cerebras Systems & G42, "Cerebras & G42 Announce Condor Galaxy 3," press release, March 13, 2024
  url: https://www.cerebras.ai/press-release/cerebras-g42-announce-condor-galaxy-3
- id: 11
  title: NVIDIA, "NVIDIA Blackwell Platform Arrives to Power a New Era of Computing," press release, March
    18, 2024
  url: https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives-to-power-a-new-era-of-computing
- id: 12
  title: NVIDIA, "GB200 NVL72," product page (specs table)
  url: https://www.nvidia.com/en-us/data-center/gb200-nvl72/
- id: 13
  title: NVIDIA Developer Blog, "NVIDIA GB200 NVL72 Delivers Trillion-Parameter LLM Training and Real-Time
    Inference," 2024
  url: https://developer.nvidia.com/blog/nvidia-gb200-nvl72-delivers-trillion-parameter-llm-training-and-real-time-inference/
- id: 14
  title: Microsoft Azure Docs, "ND GB200 v6-series virtual machines," updated April 2, 2026
  url: https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nd-gb200-v6-series
- id: 15
  title: Microsoft Azure HPC Blog, "Accelerating the Intelligence Age with Azure AI Infrastructure and
    the GA of ND GB200 v6," 2025
  url: https://techcommunity.microsoft.com/blog/azurehighperformancecomputingblog/accelerating-the-intelligence-age-with-azure-ai-infrastructure-and-the-ga-of-nd-/4394575
- id: 16
  title: NVIDIA Developer Blog, "Blackwell Delivers Massive Performance Leaps in MLPerf Inference v5.0,"
    April 2, 2025
  url: https://developer.nvidia.com/blog/nvidia-blackwell-delivers-massive-performance-leaps-in-mlperf-inference-v5-0/
- id: 17
  title: NVIDIA Blog, "CoreWeave Brings Grace Blackwell GB200 NVL72 to GA," April 15, 2025
  url: https://blogs.nvidia.com/blog/coreweave-grace-blackwell-gb200-nvl72/
- id: 18
  title: 'Anton Shilov, "Nvidia''s Blackwell AI GPUs to Cost Up to $70,000; Fully Equipped Servers Range
    Up to $3,000,000: Report," Tom''s Hardware, March 2024'
  url: https://www.tomshardware.com/pc-components/gpus/nvidias-next-gen-blackwell-ai-gpus-to-cost-up-to-dollar70000-fully-equipped-servers-range-up-to-dollar3000000-report
- id: 19
  title: MLCommons, "MLPerf Inference v5.1 Results," September 9, 2025
  url: https://mlcommons.org/2025/09/mlperf-inference-v5-1-results/
- id: 20
  title: NVIDIA Developer Blog, "Blackwell Ultra Sets New Inference Records in MLPerf Debut," September
    9, 2025
  url: https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/
- id: 21
  title: MLCommons, "MLPerf Inference Rules," ongoing GitHub policy doc
  url: https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc
- id: 22
  title: 'Artificial Analysis, "Cerebras: Provider Performance," live benchmark page'
  url: https://artificialanalysis.ai/providers/cerebras
- id: 23
  title: 'Artificial Analysis, "Llama 3.3 Instruct 70B: Providers," live benchmark page'
  url: https://artificialanalysis.ai/models/llama-3-3-instruct-70b/providers
- id: 24
  title: Groq, "Pricing," vendor page (May 2026)
  url: https://groq.com/pricing/
- id: 25
  title: Together AI, "Pricing," vendor page
  url: https://www.together.ai/pricing
- id: 26
  title: Fireworks AI, "Pricing," vendor page
  url: https://fireworks.ai/pricing
- id: 27
  title: DeepInfra, "Pricing," vendor page
  url: https://deepinfra.com/pricing
- id: 28
  title: Replicate, "Pricing," vendor page
  url: https://replicate.com/pricing
- id: 29
  title: 'Cerebras Systems, "100x Defect Tolerance: How Cerebras Solved the Yield Problem," blog'
  url: https://www.cerebras.ai/blog/100x-defect-tolerance-how-cerebras-solved-the-yield-problem
- id: 30
  title: 'Zhihang Yuan et al., "LLM Inference Unveiled: Survey and Roofline Model Insights," arXiv 2402.16363v4,
    2024'
  url: https://arxiv.org/html/2402.16363v4
- id: 31
  title: 'Pierre Lienhart, "LLM Inference Series 5: Dissecting Model Performance," Medium, 2024'
  url: https://medium.com/@plienhar/llm-inference-series-5-dissecting-model-performance-6144aa93168f
- id: 32
  title: LMCache, "KV Cache Calculator," tool
  url: https://lmcache.ai/kv_cache_calculator.html
- id: 33
  title: TrendForce, "Samsung & SK hynix Reportedly Plan 20% HBM3e Price Hike for 2026," December 24,
    2025
  url: https://www.trendforce.com/news/2025/12/24/news-samsung-sk-hynix-reportedly-plan-20-hbm3e-price-hike-for-2026-as-nvidia-h200-asic-demand-rises/
- id: 34
  title: 'Anton Shilov, "TSMC''s Wafer Prices Revealed: 300mm Wafer at 5nm Is Nearly $17,000," Tom''s
    Hardware'
  url: https://www.tomshardware.com/news/tsmcs-wafer-prices-revealed-300mm-wafer-at-5nm-is-nearly-dollar17000
- id: 35
  title: Timothy Prickett Morgan, "Cerebras Trains Llama Models To Leap Over GPUs," The Next Platform,
    October 25, 2024
  url: https://www.nextplatform.com/2024/10/25/cerebras-trains-llama-models-to-leap-over-gpus/
- id: 36
  title: 'NVIDIA, "DGX GB200 User Guide: Hardware Overview," current docs'
  url: https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html
- id: 37
  title: 'Matt Vincent, "OCP 2024: Meta Shows Off 140-kW Liquid-Cooled AI Rack," Data Center Frontier,
    October 2024'
  url: https://www.datacenterfrontier.com/hyperscale/article/55238148/ocp-2024-spotlight-meta-shows-off-140-kw-liquid-cooled-ai-rack
- id: 38
  title: 'U.S. Energy Information Administration, "Electric Power Monthly Table 5.6.A: Average Retail
    Price of Electricity," February 2026'
  url: https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a
- id: 39
  title: SemiAnalysis, "H100 vs GB200 NVL72 Training Benchmarks," 2024–2025
  url: https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks
- id: 40
  title: '"TokenPowerBench: Energy Consumption Benchmarks for LLM Inference," arXiv 2512.03024v1, December
    2025'
  url: https://arxiv.org/html/2512.03024v1
- id: 41
  title: Cerebras Systems, "Cerebras CS-3 vs NVIDIA DGX B200 (Blackwell)," vendor blog
  url: https://www.cerebras.ai/blog/cerebras-cs-3-vs-nvidia-dgx-b200-blackwell
- id: 42
  title: Cerebras Systems, Form S-1, filed September 30, 2024 (original)
  url: https://www.sec.gov/Archives/edgar/data/2021728/000162828024041596/cerebras-sx1.htm
- id: 43
  title: Tanay Jaipuria, "Cerebras S-1 Breakdown," analysis, October 2024
  url: https://www.tanayj.com/p/cerebras-s-1-breakdown
- id: 44
  title: Reuters / US News, "Cerebras Likely to Postpone IPO Due to CFIUS Review Delay on G42 Deal," October
    8, 2024
  url: https://www.usnews.com/news/technology/articles/2024-10-08/exclusive-cerebras-likely-to-postpone-ipo-due-to-cfius-review-delay-on-g42-deal-sources-say
- id: 45
  title: TechCrunch, "Cerebras Raises $5.5B, Kicking Off 2026's IPO Season with a Bang," May 14, 2026
  url: https://techcrunch.com/2026/05/14/cerebras-raises-5-5b-kicking-off-2026s-ipo-season-with-a-bang/
- id: 46
  title: TechTimes, "Cerebras Raises $5.55B AI Chip IPO; 86% Revenue Dependence on UAE Entities Unresolved,"
    May 15, 2026 (citing S-1/A)
  url: https://www.techtimes.com/articles/316698/20260515/cerebras-raises-555-billion-ai-chip-ipo-86-revenue-dependence-uae-entities-unresolved.htm
- id: 47
  title: NVIDIA, "NVIDIA Announces Financial Results for Fourth Quarter and Fiscal 2026," press release,
    February 25, 2026
  url: https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026
- id: 48
  title: NVIDIA, "Q3 FY26 Earnings Call Transcript," November 19, 2025
  url: https://s201.q4cdn.com/141608511/files/doc_financials/2026/q3/NVDA-Q3-2026-Earnings-Call-19-November-2025-5_00-PM-ET.pdf
- id: 49
  title: NVIDIA, Form 10-K for fiscal year ended January 25, 2026
  url: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm
- id: 50
  title: 'Cerebras Systems, "Cerebras Inference: 3x Faster," blog, October 24, 2024'
  url: https://www.cerebras.ai/blog/cerebras-inference-3x-faster
- id: 51
  title: 'NVIDIA Developer Blog, "Mastering LLM Techniques: Inference Optimization," ongoing'
  url: https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/
- id: 52
  title: Woosuk Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention,"
    SOSP 2023, arXiv 2309.06180
  url: https://arxiv.org/abs/2309.06180
- id: 53
  title: Anyscale, "How Continuous Batching Enables 23x Throughput in LLM Inference," engineering blog,
    2023
  url: https://www.anyscale.com/blog/continuous-batching-llm-inference
- id: 54
  title: Cerebras Systems, "Disaggregated Inference," blog
  url: https://www.cerebras.ai/blog/disaggregated-inference
- id: 55
  title: 'SemiAnalysis, "Cerebras: Faster Tokens, Please," subscriber newsletter, 2025'
  url: https://newsletter.semianalysis.com/p/cerebras-faster-tokens-please
- id: 56
  title: Groq, "New AI Inference Speed Benchmark for Llama 3.3 70B Powered by Groq," blog
  url: https://groq.com/blog/new-ai-inference-speed-benchmark-for-llama-3-3-70b-powered-by-groq
- id: 57
  title: 'SambaNova, "SN40L: The Best Inference Solution," blog'
  url: https://sambanova.ai/blog/sn40l-chip-best-inference-solution
- id: 58
  title: AMD, "AMD Delivers Breakthrough MLPerf Inference 6.0 Results," blog, 2026
  url: https://www.amd.com/en/blogs/2026/amd-delivers-breakthrough-mlperf-inference-6-0-results.html
- id: 59
  title: Google Cloud Blog, "Trillium TPU is GA," 2024
  url: https://cloud.google.com/blog/products/compute/trillium-tpu-is-ga
- id: 60
  title: 'Amazon, "AWS Project Rainier: AI Trainium Chips Compute Cluster," November 2025'
  url: https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster
- id: 61
  title: Cerebras Systems, "Cerebras Announces Six New AI Datacenters Across North America and Europe,"
    press release, March 2025
  url: https://www.cerebras.ai/press-release/cerebras-announces-six-new-ai-datacenters-across-north-america-and-europe-to-deliver-industry-s
- id: 62
  title: G42, "G42 and Government of India Formalize Commercial Framework for Condor Galaxy India," press
    release, May 15, 2026
  url: https://www.g42.ai/resources/news/g42-and-government-india-formalize-commercial-framework-condor-galaxy-india-ai-supercomputer
- id: 63
  title: Tim Dettmers, post on X, November 19, 2024
  url: https://x.com/Tim_Dettmers/status/1858977311569440955
- id: 64
  title: NVIDIA Developer Blog, "Inside NVIDIA Blackwell Ultra," April 2026
  url: https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era/
- id: 65
  title: 'Hacker News discussion #44141728, May 28, 2025'
  url: https://news.ycombinator.com/item?id=44141728
:::
