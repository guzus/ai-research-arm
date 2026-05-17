---
eyebrow: COMPUTE ECONOMICS · LOCAL INFERENCE
title: 'The home inference math just changed: MTP and speculative decoding break the batch-1 ceiling'
deck: Multi-token prediction heads ship with DeepSeek-V3, Qwen3-Next, and Gemma 4. Speculative decoding
  lands in llama.cpp, MLX, vLLM, and LM Studio. The bottleneck moves from memory bandwidth to draft
  quality — and the consumer hardware tier shifts with it.
lede: A 671B-parameter mixture-of-experts model now decodes at over twenty tokens a second on a single
  desk machine in someone's apartment[^23]. The Mac Studio M3 Ultra that runs it costs nine and a half
  thousand dollars and draws under two hundred watts at the wall[^53,54]. Neither number was possible
  in 2023 — and neither is the headline. The real change is what is happening inside the decode loop.
  DeepSeek-V3's built-in multi-token prediction head accepts roughly eighty-five percent of its proposals
  and delivers a 1.8× tokens-per-second speedup at inference[^2]. Qwen3-Next ships a native MTP module
  exposed through vLLM and SGLang[^17,18]. The llama.cpp project just landed its first MTP draft head
  for Qwen3.6, with a measured two-times speedup at roughly seventy-five percent acceptance[^15]. The home inference
  math has moved from "weights divided by bandwidth" to "weights divided by bandwidth, divided by one
  minus alpha." Every term in that fraction is shifting at once.
stats:
- label: DeepSeek-V3 MTP gain
  value: '1.8×'
  note: 85-90% accept on next token[^2]
- label: M3 Ultra bandwidth
  value: '819 GB/s'
  note: 512 GB unified[^22]
- label: DeepSeek-V3 on M3 Ultra
  value: '>20 tok/s'
  note: 4-bit MLX, Awni Hannun[^23]
- label: EAGLE-3 peak
  value: '6.5×'
  note: SGLang batch 1[^7]
- label: llama.cpp MTP lag
  value: '~15 mo'
  note: vs vLLM DeepSeek MTP[^13,14]
- label: Mac Studio capex
  value: '$9,499'
  note: 512 GB SKU, launch[^67]
---

This essay does the comparison from first principles. It distinguishes the math of batch-1 home decode from the math of large-batch cloud serving; it walks the Leviathan formula and Multi-Token Prediction mechanics; it maps the consumer hardware bandwidth ladder against the active-weight requirements of frontier mixture-of-experts models; and it asks what would have to break for the thesis to fail. The short version: ==speculative decoding and MTP do not raise the bandwidth ceiling — they multiply the tokens you extract from each bandwidth-bound step==. Because home users run at batch one, almost by definition, they capture the largest possible share of that multiplier. The cloud cannot. That is the home inference math.

## 01. The batch-1 ceiling — why home inference is a different sport

The fundamental constraint on local LLM decoding is memory bandwidth, not floating-point throughput. At batch size one, every output token requires moving the model's active weights from DRAM into the matrix-multiply units once[^49]. The ceiling is arithmetic: bandwidth divided by bytes-per-token. Horace He's classic roofline analysis pegged the A100's ridge point — where a kernel transitions from memory-bound to compute-bound — at roughly fifty FLOPs per byte; a single decode forward pass operates two orders of magnitude inside the memory-bound corner[^48]. Databricks measured the constraint concretely: a 7B model at FP16 with 14 ms time-per-output-token implies 1 TB/s of bandwidth utilization[^49], meaning the GPU is doing nothing else.

This is why batch one is the home regime. Cloud serving stacks like vLLM and TensorRT-LLM amortize the same weight read across dozens of concurrent requests through continuous batching, pushing the workload off the bandwidth wall and onto the compute wall where {accent}per-stream throughput drops but per-GPU throughput climbs{/}[^65]. A home user has no concurrent requests. Their per-stream throughput equals their per-machine throughput, and both are governed by one number.

:::stats
- {label: A100 ridge point, value: '~50', unit: ' FLOP/B'}
- {label: Batch-1 intensity, value: '~1', unit: ' FLOP/B'}
- {label: Bandwidth headroom (compute), value: '~98%'}
- {label: Weight reload per token, value: '1×', note: every decode step}
:::

Because the verifier sits idle ~98% of the time at batch one, there is enormous slack to do extra arithmetic for free. Speculative decoding and MTP are the methods that spend that slack on parallelism. NVIDIA's own introduction to the technique frames it cleanly: "only the new, speculated tokens incur a computational cost during this verification pass" because the bandwidth read is already paid[^66]. The compute headroom that goes wasted at batch one on a cloud serving cluster — where it would otherwise be filled by concurrent users — is available for free at home. That is the structural arbitrage.

The counterargument is that the cloud will batch the same trick. It does, partially. But SqueezeBits' measurement on Llama-3.1-70B with a Qwama-0.5B draft on an A100 cluster found that speculative decoding stops being net-positive once concurrency exceeds 32 at 1K context, and 16 at 2K[^32]. {accent}Above that threshold, verification overhead exceeds the savings and standard decoding wins on throughput{/}. The home user is permanently below that threshold by construction.

## 02. The math of speculative decoding — Leviathan's formula

Speculative decoding has a closed-form expected speedup. Leviathan et al. (Google, 2022) gave it: a small draft model proposes γ tokens, the target model verifies them all in a single parallel forward pass, and the expected wall-time improvement factor is **(1 - α^(γ+1)) / ((1 - α)(γc + 1))**, where α is the per-token acceptance rate and c is the draft's per-step cost relative to the target's[^3]. Improvement is guaranteed whenever α > c[^3]. The paper demonstrated 2× to 3× speedup on T5-XXL with identical outputs[^3]; Chen et al. at DeepMind replicated the result a month later on Chinchilla 70B with a 4B draft, hitting 2.0× to 2.5× speedup on XSum and HumanEval with no quality loss[^4].

The asymptote matters more than the headline. As γ grows, expected accepted tokens per step converges to **1/(1-α)**[^3]. At α = 0.8, that ceiling is five tokens per verifier call; at α = 0.9, ten. The closer the draft tracks the target, the more headroom the formula has — but draft cost c grows with γ as well, so doubling the draft length past a model-specific knee delivers diminishing returns. This is why most production deployments settle at γ between three and five.

:::compare
- {role: 'α=0.5', name: 'Weak draft', value: '2×'}
- {role: 'α=0.8', name: 'Typical draft', value: '5×'}
- {role: 'α=0.9', name: 'Strong draft', value: '10×'}
:::

The home-relevant corollary is brutal: ==α is everything==. A draft that matches the target on chat at α=0.7 may collapse to α=0.4 on code or to α=0.2 on RAG-grounded answers where the target's distribution diverges. Leviathan's original paper showed even a trivial bigram draft against T5-XXL on English-to-German translation yielded α≈0.2 and a 1.25× speedup at γ=3 — a {accent}floor, not a ceiling{/}[^3]. Acceptance compounds with draft quality, and draft quality is now the constrained resource.

The mechanism also explains why prefill barely benefits. Prefill is one large matrix-matrix multiply that already saturates the GPU's compute units; there is no slack to verify candidate tokens for free. Decode is the only phase where the speculation budget is real, which is precisely the phase home users spend almost all their wall-clock time in.

## 03. Multi-Token Prediction — when the draft is built into the model

Gloeckle et al. (Meta FAIR, 2024) proposed training language models with multi-token prediction heads instead of next-token only. Their architecture shares a single transformer trunk feeding n independent output heads, each predicting one further future token; the inference-time payoff comes from using those heads as a self-drafting mechanism[^1]. The Meta team reported a 3.0× greedy-decoding speedup on code and 2.7× on text for a 7B model with four heads, plus a 12% lift on HumanEval and 17% on MBPP versus a baseline trained with next-token only[^1].

DeepSeek-V3 (December 2024) adapted the idea into production. Instead of Gloeckle's parallel heads, DeepSeek's MTP module is a sequential block that predicts one additional next-next token at depth D=1, preserving the full causal chain through embedding and head sharing[^2]. The reported acceptance rate for the second-token prediction is **85% to 90%** across topics, yielding a **1.8× TPS speedup** when MTP runs as the speculative drafter[^2]. The MTP module ships as part of the 685B HF checkpoint — 671B for the main model, ~14B for the MTP head — and is optional at inference[^2].

:::timeline
- {date: 2024-04, headline: 'Gloeckle et al. MTP paper (Meta FAIR)', body: 'Parallel heads, 3.0× code / 2.7× text speedup at greedy decoding[^1].'}
- {date: 2024-12, headline: 'DeepSeek-V3 ships MTP', body: 'Sequential D=1 module, 85-90% accept, 1.8× TPS[^2].'}
- {date: 2025-02, headline: 'vLLM merges DeepSeek MTP', body: 'PR #13626 lands; 83/72/61% accept at k=1/2/3[^13].'}
- {date: 2025-04, headline: 'Llama 4 ships without MTP', body: 'Meta blog confirms MoE + iRoPE; no MTP heads[^19].'}
- {date: 2025-07, headline: 'SGLang production MTP blog (LMSYS)', body: '+60% throughput small-scale; +14.2% at 128-GPU disaggregated[^12].'}
- {date: 2025-09, headline: 'Qwen3-Next-80B-A3B ships with native MTP', body: 'SGLang NEXTN and vLLM qwen3_next_mtp drivers[^17,18].'}
- {date: 2026-03, headline: 'TensorRT-LLM MTP Vanilla + Eagle', body: '2.16× → 2.33× on 8×B200, relaxed acceptance[^11].'}
- {date: 2026-05, headline: 'llama.cpp PR #22673 adds MTP for Qwen3.6', body: '~75% accept, >2× speedup; ~15-month lag vs vLLM[^15].'}
- {date: 2026-05, headline: 'Google ships Gemma 4 MTP drafters', body: 'External drafter artifact, up to 3× claimed[^20].'}
:::

DeepSeek-V3.1, V3.2-Exp, and R1 all retain the MTP head — `num_nextn_predict_layers: 1` in every shipped config.json[^2]. Qwen3-Next-80B-A3B (September 2025) is the second frontier family to ship a co-trained MTP module, exposed through `--speculative-config '{"method":"qwen3_next_mtp","num_speculative_tokens":2}'` in vLLM and `--speculative-algo NEXTN` in SGLang[^18]. Neither HF Transformers nor stock llama.cpp load the MTP weights, locking the speedup to dedicated serving engines until very recently[^18]. Llama 4 took a different path — Meta's announcement and Transformers documentation describe MoE, iRoPE, chunked attention, and QK-norm but contain zero references to multi-token prediction[^19]. Google's Gemma 4 (May 2026) released MTP drafters as a separate, optional artifact rather than co-training them into the base model, claiming up to 3× and measuring roughly 2.2× on Apple Silicon at batch 4-8[^20].

The skeptical reading is that MTP is a forecast-bias correction wrapped in a speculation budget — the model trains to predict beyond the next token, which improves both quality and self-drafting. The bullish reading is that {accent}every frontier MoE family except Llama 4 now ships native MTP{/}, and inference engines are racing to expose it. Both are true.

## 04. The hardware ladder — bandwidth × capacity is the constraint

A home inference rig is a bandwidth account with a capacity ceiling. Bandwidth sets the per-step roofline; capacity decides whether the model can be held in RAM at all. The 2026 consumer landscape spreads an order of magnitude on the first axis and another on the second.

:::rank-list
- {label: 'NVIDIA RTX 5090 (32 GB GDDR7)', value: '1792 GB/s', pct: 100}
- {label: 'NVIDIA RTX 4090 (24 GB GDDR6X)', value: '1008 GB/s', pct: 56}
- {label: 'Apple M3 Ultra (up to 512 GB unified)', value: '819 GB/s', pct: 46, highlight: true}
- {label: 'Apple M4 Max (up to 128 GB unified)', value: '546 GB/s', pct: 30}
- {label: 'NVIDIA DGX Spark (128 GB LPDDR5x)', value: '273 GB/s', pct: 15}
- {label: 'AMD Strix Halo / Framework Desktop (128 GB)', value: '~256 GB/s', pct: 14}
:::

The RTX 5090 wins on raw bandwidth: 32 GB of GDDR7 on a 512-bit bus delivering 1792 GB/s — a 78% jump over the 4090[^25,26]. But 32 GB cannot hold a 4-bit-quantized Llama 70B (which needs ~35 GB) or a 4-bit DeepSeek-V3 (which needs ~350 GB at full 671B). The capacity ceiling rules the consumer GPU out for frontier MoE entirely. The Mac Studio M3 Ultra is the inverse: 819 GB/s — 46% of the 5090's — but up to 512 GB of unified memory, the largest single-system pool any consumer can buy[^21,22]. Apple's specs page rates the workstation at a 270 W maximum continuous draw[^53], and reviewers measure 160-180 W under live DeepSeek R1 load[^54]. NVIDIA's DGX Spark (October 2025, $3,999 to $4,699[^27]) and AMD's Strix Halo (CES 2025, $1,999 in the Framework Desktop[^30]) bring 128 GB of unified LPDDR5x at ~273 and ~256 GB/s respectively — the right amount of memory for a 70B-class model at the wrong amount of bandwidth.

The arithmetic ceiling at batch one is bandwidth ÷ active bytes. For a dense 70B model in INT4 (~35 GB):

| Hardware | Bandwidth | Dense 70B ceiling | DeepSeek-V3 MoE ceiling |
|---|---|---|---|
| RTX 5090 | 1792 GB/s[^25] | ~51 tok/s | ~97 tok/s (cannot fit) |
| RTX 4090 | 1008 GB/s[^26] | ~29 tok/s | ~55 tok/s (cannot fit) |
| *M3 Ultra (512 GB) | 819 GB/s[^22] | ~23 tok/s | ~44 tok/s |
| M4 Max | 546 GB/s[^22] | ~16 tok/s | ~30 tok/s (cannot fit 671B) |
| DGX Spark | 273 GB/s[^27] | ~8 tok/s | ~15 tok/s (cannot fit) |
| Strix Halo | ~256 GB/s[^29] | ~7 tok/s | ~14 tok/s (cannot fit) |

The MoE column uses DeepSeek-V3's 37B active parameters per token (~18.5 GB at INT4)[^2]. The M3 Ultra is the only consumer device that holds the full 671B checkpoint in RAM and is fast enough to make MoE active-weight math feasible. LMSYS measured the DGX Spark sustaining only **2.7 tok/s** on Llama 3.1 70B FP8 decode — concretely confirming that 273 GB/s of LPDDR5x is the binding constraint, not the Blackwell GPU rated at 1 PFLOP FP4[^28]. The same Spark hits 803 tok/s on prefill, an order of magnitude faster, because prefill is compute-bound[^28].

The roofline math is what makes MTP and speculative decoding worth caring about. A 235B-A22B Qwen3 model in INT4 needs ~120 GB of total weights and ~11 GB of active weights per token. On M3 Ultra's 819 GB/s, the active-weight ceiling is ~74 tok/s. MacStories measured the model at **24 tok/s in MLX** and 16 tok/s in GGUF — roughly a third of the theoretical limit, before any speculative trick[^59]. The room to grow is real, and it is exactly what MTP fills.

## 05. The software ladder — engines, the 15-month lag, and what runs at home

The frontier MTP and speculative-decoding implementations land first on cloud serving engines, then trickle into the consumer stack with a lag that has become predictable. vLLM merged DeepSeek MTP in PR #13626 on February 27, 2025 — sixty days after the DeepSeek-V3 paper dropped[^13]. SGLang shipped production MTP in mid-July 2025 with a +60% throughput claim at small concurrency on H200 and +14.2% at large-scale 128-GPU disaggregated deployments[^12]. NVIDIA's TensorRT-LLM added MTP Vanilla and MTP Eagle variants, hitting 2.16× speedup at MTP=3 on 8×B200 and 2.33× with relaxed acceptance for reasoning workloads[^11]. AMD's ROCm tutorial reproduces the 1.2× to 2.1× operational band on MI300X[^58].

The home stack moved more slowly. llama.cpp opened a DeepSeek-V3 MTP discussion (#11455) on January 27, 2025[^14] and did not land any MTP support until PR #22673 in May 2026 — and that PR covers Qwen, not DeepSeek-V3 specifically[^15]. The ~15-month lag is the load-bearing fact about the home ecosystem: the math has been provably available since late 2024, and consumer engines are still racing to expose it. MLX-LM supports standard speculative decoding via `--draft-model` and `--num-draft-tokens` (PR #1155, December 2024), with the original benchmark showing 19.7 → 35.7 tok/s (1.82×) on M3 Max[^36]. An EAGLE-3 prototype for MLX, however, delivered only a 1.05× speedup on M3 Ultra because the cache uses a single offset integer for RoPE positions, blocking the tree-attention path that drives EAGLE's CUDA-side 3.3× to 6.5× wins[^37].

:::callout(kind=info, label="The home stack today")
- **llama.cpp** ships `--model-draft`, `--draft-max`, and `--draft-p-min` with documented defaults (16 / 0.75)[^16]; MTP arrived in PR #22673 for Qwen with ~75% acceptance and >2× speedup[^15]; DeepSeek-V3 MTP still in flight[^14].
- **LM Studio 0.3.10** wraps llama.cpp and MLX with a click-to-enable draft picker; documented same-vocab pairs include Llama 3.1 8B + 3.2 1B, Qwen 2.5 14B + 0.5B, and DeepSeek-R1-Distill 32B + 1.5B[^34,35].
- **MLX-LM** supports standard speculative decoding (1.82× on M3 Max) but EAGLE-3 is bottlenecked on cache-position-ID support[^36,37].
- **Ollama** added Gemma 4 MTP via PR #15980 (May 2026); int4 results mixed (one user measured 60 → 45 tok/s at int4 vs BF16 winning at 41% match rate)[^20].
- **vLLM, SGLang, TensorRT-LLM** are years ahead but require server-class GPUs.
:::

LM Studio's own benchmark in the 0.3.10 release is the cleanest demonstration the home stack will produce all year. On an RTX 3090 Ti, Qwen2.5 32B with a 0.5B draft jumped from 21.84 to 45.15 tok/s (2.07×) on a quicksort coding prompt; on an M3 Pro 36 GB, the same pair went from **7.30 to 17.74 tok/s — a 2.43× speedup that crossed the interactive threshold** from unusable to usable[^34]. The mechanism is the home thesis in one number: a model that was too slow for chat became fast enough for chat, on the same hardware, by spending the bandwidth-bound step's idle FLOPs on parallel verification.

The counterpoint is fragmentation. Different drafts work with different targets, vocabularies must match, quantization must be set carefully, and Ollama users have already reported configurations where int4 MTP runs slower than int4 standard[^20]. The home stack's coordination cost is high enough that most users still pick a single static model and ignore the speculative-decoding switch entirely.

## 06. Real numbers — what crosses the interactive threshold

Awni Hannun's tweet on March 24, 2025 is the anchor: ==**"The new Deep Seek V3 0324 in 4-bit runs at > 20 toks/sec on a 512GB M3 Ultra with mlx-lm!"**==[^23]. As MLX's lead at Apple, his benchmarks have the weight of a vendor disclosure even when they read like enthusiasm. The single number — twenty tokens per second for a 671B-parameter model on a workstation a single human can buy — is the moment the home inference math became visible to anyone watching. Alex Cheema followed in twelve days with 11 tok/s for full DeepSeek R1 671B 8-bit across two M3 Ultras linked over Thunderbolt 5 using the exo distributed-inference stack — versus a theoretical ~20 tok/s ceiling on the cluster[^24].

The published primary measurements cluster tightly across vendors when normalized for hardware tier:

:::slope(left-label=Baseline, right-label="With MTP/spec", unit=' tok/s')
| Setup | Baseline | With MTP/spec |
|---|---|---|
| DeepSeek-V3 (H800, official, MTP)[^2] | 45 | 81 |
| DeepSeek-V3 (16×H200, SGLang MTP)[^12] | 51 | 82 |
| Llama 3.3 70B (H200, TRT-LLM, 1B draft)[^33] | 51 | 182 |
| Qwen2.5 32B (M3 Pro, LM Studio)[^34] | 7 | 18 |
| Qwen 32B (RTX 3090, llama.cpp)[^16] | 10 | 57 |
:::

The TensorRT-LLM measurement on Llama 3.3 70B with a Llama 3.2 1B draft is the most aggressive: 51.14 → 181.74 tok/s on a single H200 — a **3.55× speedup** at batch one[^33]. Georgi Gerganov's December 2025 collaboration tweet with NVIDIA put llama.cpp Ministral-3B at **385+ tok/s** on RTX 5090, demonstrating what the consumer stack can do when the model is small enough to live entirely in VRAM and the draft trick is properly wired[^64]. The LMSYS team measured DeepSeek-V3 with a 3-token MTP window on 16×H200 going from 51 to 82 tok/s per rank — a 60% throughput gain at 2.44 average accepted tokens, scaling down to +14.2% at 128 GPUs[^12].

These numbers tell a consistent story. At batch one on bandwidth-bound hardware, speculative decoding and MTP deliver roughly 1.5× to 3.5× speedups across hardware tiers. ==The headline 6.5× from EAGLE-3 papers is a peak under controlled conditions==[^7]; the operational band is narrower but reliably above 1.5×. For a home user running DeepSeek-V3 at 12 tok/s on a Mac, MTP at 1.8× pushes them to 22 tok/s — the difference between "slower than I read" and "faster than I read." That is the threshold that matters, and the threshold MTP crosses.

## 07. The counter-narrative — when these tricks hurt

The corpus of negative results is now large enough to be its own subgenre. The headline disappointment is on consumer MoE: a community benchmark using a vocab-matched Qwen3.5-0.8B draft against Qwen3.6-35B-A3B on RTX 3090 found that **none of llama.cpp's 19 tested speculative-decoding configurations beat baseline**[^38]. Baseline reached 135.7 tok/s; the best speculative variant dropped to 121.3 tok/s — an 11% regression despite 100% draft acceptance on some configurations[^38]. The MoE architecture is the culprit: the verifier already activates only ~3B parameters per token, so the "free verification" math that drives speculative decoding on dense models collapses.

A similar paired-delta in llama.cpp issue #10594 (November 2024) tested the same 160M draft against the same Llama target at two quantizations. Against FP16 weights of a Llama-2-7B target, speculative decoding lifted 17.3 → 26.8 tok/s (+54.9%); against the same target's Q4_K_M build, the identical draft dropped throughput from 40.7 → 22.3 tok/s (−45.2%)[^39]. The Q4 target is already running ~4× lighter on bandwidth than the FP16 baseline, so the draft's overhead — dequantization for verification, multi-position attention, tree-prefix bookkeeping — eats the savings. An arxiv paper from May 2025 ("Speculative Decoding Meets Quantization") confirmed this is a structural interaction: vanilla tree-draft methods like EAGLE-2 deliver "limited benefit" on W4A16 targets, recovering 2.78× only with a hierarchical drafter retrofit[^60].

:::callout(kind=warn, label="When the trick backfires")
- **MoE on consumer GPUs:** spec-decoding net-negative across all tested configs on Qwen3.6-35B-A3B / RTX 3090[^38].
- **Quantized targets:** −45% regression on Llama Q4_K_M with the same draft that gives +55% on FP16[^39].
- **Batch >16 (or 32 at short context):** verifier becomes compute-bound, savings invert[^32].
- **Metal (MLX) tree attention:** EAGLE-3 prototype hits only 1.05× on M3 Ultra (cache position-ID limit)[^37].
- **Medusa typical-acceptance:** explicitly not distribution-preserving at temperature > 0[^8].
:::

The quality story is the other quiet caveat. Speculative decoding as Leviathan formalized it preserves the *target's* output distribution exactly — verify-and-reject sampling is mathematically lossless against the target[^3]. But Medusa relaxed that guarantee with "typical acceptance," explicitly abandoning distribution-matching above greedy decoding to capture more speedup[^8]. Medusa's authors argue this is a feature for creative sampling; the EAGLE-2 paper notes Medusa is roughly 2× slower than EAGLE-2 on MT-bench and excludes it from their temperature-equal-one comparisons specifically because the acceptance rules diverge[^6]. ReDrafter on Apple Silicon hits 2.3× via MLX on M2 Ultra at batch 1, but its 2.7× headline number is from a single greedy run on an unnamed production model in NVIDIA TensorRT-LLM — Apple has never disclosed the model, batch size, or sequence length, and there is no public confirmation that ReDrafter ships inside on-device Apple Intelligence[^9,10,61].

The home implication is that ==the speedup is conditional on architecture, quantization, batch, kernel maturity, and draft-target compatibility==. The defaults that ship with llama.cpp's `-md` flag are conservative for a reason. A user who turns on speculative decoding on the wrong combination — MoE on a 3090, Q4 target with mismatched-quant draft, or any of several documented failure modes — will see throughput go *down*. The math is real; the engineering is brittle.

## 08. The cost math — privacy, not price

The home inference math does not make local inference cheaper per token than the cloud. It is not even close. DeepInfra serves Qwen3-235B-A22B-Instruct-2507 at **$0.071 per million input tokens and $0.10 per million output tokens**[^50]. DeepSeek's official API charges $0.27/$1.10 for V3-class chat[^51]. A Mac Studio M3 Ultra 512 GB cost **$9,499** at launch[^67]; the EIA projects US residential electricity at 18.02 cents per kWh in 2026[^52]; the workstation at a continuous 200 W draws ~1,750 kWh per year — about **$315 in electricity**.

The amortization is unkind. At 24 tok/s sustained, the Mac generates **~757 million output tokens per year** at peak utilization. Priced at DeepInfra's Qwen3-235B output rate of $0.10/Mtok, that is ~$76 of equivalent API spend. **Payback at peak utilization: 124 years.** Even priced at the Fireworks tier of ~$0.90/Mtok output, payback is ~14 years — and electricity alone costs four times the DeepInfra rate per generated token.

:::compare
- {role: HOME (24 tok/s, 100% util), name: 'Mac Studio + electricity', value: '~$0.42/Mtok'}
- {role: API (cheapest), name: 'DeepInfra Qwen3-235B output', value: '$0.10/Mtok'}
- {role: API (mid-tier), name: 'Fireworks Llama 70B output', value: '$0.90/Mtok'}
:::

The market has voted. Anthropic went from $1B ARR in December 2024 to a reported $30B annualized run rate by April 2026, while OpenAI sits at roughly $24-25B ARR[^55]. ==Hosted inference is not being displaced by home inference at any measurable rate==. Home wins on three things, none of which is price: privacy (PHI never crosses a network; medical, legal, and proprietary code stay local), latency floor (no network round trip), and sovereignty (no rate limits, no model deprecation, no terms-of-service revisions). The MTP/speculative-decoding stack is what makes those wins *usable* — without them, a home Mac runs DeepSeek-V3 at six tokens per second and the privacy is moot because no one waits that long.

The energy math is closer to a tie than the cost math. TokenPowerBench measured Llama-3-70B FP8 on H100 at roughly 0.39 J per output token at batch 128[^57]; a Mac Studio at 180 W and 20 tok/s sustains ~9 J per token, an order of magnitude worse per token but identical to the cloud once you account for one user's actual duty cycle (most home machines idle >95% of the day). Speculative decoding cuts inference energy by 4-29% in the relevant regime, with the headline 29% reduction at small batch shrinking to near-zero at high batch[^56]. {accent}MTP at 1.8× speedup at constant power translates roughly 1:1 to J-per-token improvement{/}, which is the home user's actual energy win.

## 09. What's next — the frontier beyond MTP

The post-MTP research bench is full. REST (Retrieval-Based Speculative Decoding) replaces the draft model with a trie of prior generations, hitting 1.62× to 2.36× speedup on 7B and 13B models in single-batch settings — exactly the home regime[^41]. SpecInfer's token-tree verification with multiple small drafters reaches 2.6× to 3.5× on offloading-based inference, the only frontier method explicitly characterized for the regime where weights exceed VRAM[^42]. Online Speculative Decoding adapts the draft model from live serving traffic for an extra 1.42×-2.17× — but only if you have a multi-tenant serving cluster, which a home user does not[^43]. DistillSpec adds 10-45% on top of standard speculative decoding by aligning the draft via knowledge distillation[^44]. SpecDec++ adaptively chooses draft length k, lifting Llama-2-70B speedup to 2.04×-2.26×[^45]. Cascade Speculative Drafting stacks drafters in two cascades for an additional +81% over baseline at NeurIPS 2024[^46]. Mamba-based drafters match EAGLE's throughput while being target-agnostic — they work with any target model without per-target retraining[^47].

:::bars
- {label: 'EAGLE-3 (peak)', value: '6.5×', pct: 100}
- {label: 'Cascade Spec Drafting', value: '+81% (~3.5×)', pct: 54}
- {label: 'SpecInfer (offload)', value: '3.5×', pct: 54}
- {label: 'NVIDIA Llama 3.3+1B draft', value: '3.55×', pct: 55}
- {label: 'DistillSpec (combined)', value: '6-10×', pct: 95}
- {label: 'DeepSeek MTP (V3 stock)', value: '1.8×', pct: 28}
- {label: 'REST (retrieval)', value: '2.36×', pct: 36}
- {label: 'Lookahead (no draft)', value: '1.5-1.8×', pct: 26}
:::

The home stack will probably absorb REST and Mamba drafters next, in that order. REST is attractive because it requires no extra model and no training — it just retrieves from the user's own prior generations, which a personal machine accumulates naturally. Mamba drafters solve the home pain point of swap-the-target-model-and-retrain-the-draft, since they generalize across targets without retraining[^47]. Apple's ReDrafter (Apple ML Research, December 2024) demonstrated 2.7× on TensorRT-LLM and 2.3× on MLX — but Apple has never publicly confirmed that on-device Apple Intelligence runs ReDrafter in production[^9,10,61]. If it does, the entire iOS install base is already inside the home inference math; if it doesn't, the next WWDC cycle is the time to expect that announcement.

## 10. What could break the thesis

==If batch one stops being the home workload==, the math collapses. A small office with three or four concurrent users hitting a shared Mac Studio crosses into the regime where verification cost dominates and speculative decoding regresses to neutral or worse — the SqueezeBits batch-32 threshold[^32]. The home market is structurally batch-one today, but multi-user household deployments are exactly the workload Apple Intelligence and personal AI servers are pushing toward.

==If quantization keeps improving faster than the speculation budget==, the trick loses its punch. The Q4_K_M target with INT4 weights already runs ~4× lighter on bandwidth than FP16, eating most of the slack that speculative decoding was supposed to exploit. {accent}1.58-bit (BitNet) and ternary models flip the regime entirely{/} — they are compute-bound at the ALU level, not bandwidth-bound, and there is no spare FLOP budget to spend on verification. No production benchmarks of BitNet-as-target with any speculative-decoding stack exist as of mid-2026 — the BitNet b1.58 2B4T report explicitly calls speculative decoding a "complementary" technique without pairing it[^68].

==If the cloud cuts prices another 10× and adds stronger private-inference guarantees==, the privacy argument that justifies the Mac weakens. Frontier providers already offer enterprise deployments with zero-retention clauses and per-tenant isolation; the gap to "data never leaves your tenant" is increasingly procedural rather than technical. The home stack's defense is sovereignty, not price — but if cloud sovereignty hardens, the marginal home user has less reason to spend $9,499.

==If MTP turns out to be a one-architecture quirk==, the chronology stops compounding. Llama 4 declined to ship MTP[^19], and there is no published explanation for why. If Meta's bet is that better quantization, faster KV caches, and continuous batching dominate the next 24 months, MTP could become a DeepSeek/Qwen idiosyncrasy that doesn't generalize. Gemma 4's choice to ship MTP as a *separate* drafter artifact[^20] hints that Google sees the same uncertainty — co-training is a commitment, post-hoc distillation is a fallback.

The most honest read is that the math is real and the engineering is messy. Five distinct primary measurements (DeepSeek V3 paper 1.8×; AMD ROCm 1.2-2.1×; vLLM ~2×; TensorRT-LLM 2.16-2.33×; SGLang +60% small-scale) bracket the operational MTP gain at roughly 1.8×, and the standard speculative-decoding gain on home GPUs at 2-3× when conditions are met. ==The conditions are met more often on Apple Silicon than on the consumer NVIDIA tier today, because Apple's bandwidth × capacity product is the only consumer combination that holds a frontier MoE in RAM== — and that is the configuration where the largest models, the highest acceptance rates, and the most untapped slack converge. The home inference math just changed. It is not done changing.

:::references
- {id: 1, title: "Better & Faster Large Language Models via Multi-token Prediction (Gloeckle et al.)", url: "https://arxiv.org/abs/2404.19737", source: "arXiv 2404.19737 / Meta FAIR", date: "2024-04-30"}
- {id: 2, title: "DeepSeek-V3 Technical Report", url: "https://arxiv.org/abs/2412.19437", source: "arXiv 2412.19437", date: "2024-12-27"}
- {id: 3, title: "Fast Inference from Transformers via Speculative Decoding (Leviathan, Kalman, Matias)", url: "https://arxiv.org/abs/2211.17192", source: "arXiv 2211.17192 / Google", date: "2022-11-30"}
- {id: 4, title: "Accelerating Large Language Model Decoding with Speculative Sampling (Chen et al.)", url: "https://arxiv.org/abs/2302.01318", source: "arXiv 2302.01318 / DeepMind", date: "2023-02-02"}
- {id: 5, title: "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty", url: "https://arxiv.org/abs/2401.15077", source: "arXiv 2401.15077 / SafeAI Lab", date: "2024-01-26"}
- {id: 6, title: "EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees", url: "https://arxiv.org/abs/2406.16858", source: "arXiv 2406.16858", date: "2024-06-24"}
- {id: 7, title: "EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test", url: "https://arxiv.org/abs/2503.01840", source: "arXiv 2503.01840", date: "2025-03-03"}
- {id: 8, title: "Medusa: Simple LLM Inference Acceleration via Multiple Decoding Heads", url: "https://arxiv.org/abs/2401.10774", source: "arXiv 2401.10774 / Together AI", date: "2024-01-19"}
- {id: 9, title: "Recurrent Drafter for Fast Speculative Decoding", url: "https://arxiv.org/abs/2403.09919", source: "arXiv 2403.09919 / Apple", date: "2024-03-14"}
- {id: 10, title: "Apple ReDrafter on NVIDIA TensorRT-LLM", url: "https://machinelearning.apple.com/research/redrafter-nvidia-tensorrt-llm", source: "Apple ML Research", date: "2024-12-18"}
- {id: 11, title: "DeepSeek-R1 MTP Implementation and Optimization (TensorRT-LLM)", url: "https://nvidia.github.io/TensorRT-LLM/blogs/tech_blog/blog2_DeepSeek_R1_MTP_Implementation_and_Optimization.html", source: "NVIDIA TensorRT-LLM", date: "2026-03-16"}
- {id: 12, title: "MTP unlocks 60% higher throughput for DeepSeek V3", url: "https://www.lmsys.org/blog/2025-07-17-mtp/", source: "LMSYS / SGLang", date: "2025-07-17"}
- {id: 13, title: "vLLM PR #13626 — DeepSeek MTP support (merged)", url: "https://github.com/vllm-project/vllm/pull/13626", source: "vLLM project", date: "2025-02-27"}
- {id: 14, title: "llama.cpp discussion #11455 — DeepSeek V3 MTP request", url: "https://github.com/ggml-org/llama.cpp/discussions/11455", source: "llama.cpp project", date: "2025-01-27"}
- {id: 15, title: "llama.cpp PR #22673 — speculative decoding / MTP support for Qwen", url: "https://github.com/ggml-org/llama.cpp/pull/22673", source: "llama.cpp project", date: "2026-05-16"}
- {id: 16, title: "llama.cpp PR #10455 — server speculative decoding", url: "https://github.com/ggml-org/llama.cpp/pull/10455", source: "llama.cpp project", date: "2024-11-25"}
- {id: 17, title: "Qwen3-Next architecture deep-dive (Alibaba Cloud Community)", url: "https://www.alibabacloud.com/blog/602580", source: "Alibaba Cloud", date: "2025-09-12"}
- {id: 18, title: "Qwen3-Next-80B-A3B-Instruct model card", url: "https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct", source: "Hugging Face", date: "2025-09-11"}
- {id: 19, title: "Llama 4 announcement (Meta AI blog)", url: "https://ai.meta.com/blog/llama-4-multimodal-intelligence/", source: "Meta AI", date: "2025-04-05"}
- {id: 20, title: "Multi-Token Prediction drafters for Gemma 4 (Google)", url: "https://blog.google/innovation-and-ai/technology/developers-tools/multi-token-prediction-gemma-4/", source: "Google", date: "2026-05-05"}
- {id: 21, title: "Apple unveils new Mac Studio (Apple Newsroom)", url: "https://www.apple.com/newsroom/2025/03/apple-unveils-new-mac-studio-the-most-powerful-mac-ever/", source: "Apple Newsroom", date: "2025-03-05"}
- {id: 22, title: "Mac Studio Tech Specs", url: "https://www.apple.com/mac-studio/specs/", source: "Apple", date: "2025-03-12"}
- {id: 23, title: "Awni Hannun on DeepSeek-V3 0324 at >20 tok/s on M3 Ultra", url: "https://x.com/awnihannun/status/1904177084609827054", source: "X / Awni Hannun (MLX lead)", date: "2025-03-24"}
- {id: 24, title: "Alex Cheema on DeepSeek R1 671B over 2 M3 Ultras at 11 tok/s", url: "https://x.com/alexocheema/status/1899735281781411907", source: "X / exo labs", date: "2025-03-12"}
- {id: 25, title: "GeForce RTX 5090 product page", url: "https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/", source: "NVIDIA", date: "2025-01-30"}
- {id: 26, title: "GeForce RTX 4090 product page", url: "https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/", source: "NVIDIA", date: "2022-10-12"}
- {id: 27, title: "DGX Spark product page", url: "https://www.nvidia.com/en-us/products/workstations/dgx-spark/", source: "NVIDIA", date: "2025-10-15"}
- {id: 28, title: "NVIDIA DGX Spark in-depth review", url: "https://www.lmsys.org/blog/2025-10-13-nvidia-dgx-spark/", source: "LMSYS", date: "2025-10-13"}
- {id: 29, title: "AMD Ryzen AI Max+ 395 announcement", url: "https://www.amd.com/en/blogs/2025/amd-ryzen-ai-max-395-processor-breakthrough-ai-.html", source: "AMD", date: "2025-01-06"}
- {id: 30, title: "Framework Desktop preorder coverage", url: "https://www.tweaktown.com/news/103516/frameworks-tiny-new-modular-desktop-pc-16c-32t-amd-strix-halo-apu-128gb-ram-for-just-1999/index.html", source: "TweakTown", date: "2025-02-26"}
- {id: 31, title: "Strix Halo LLM benchmark results (Level1Techs)", url: "https://forum.level1techs.com/t/strix-halo-ryzen-ai-max-395-llm-benchmark-results/233796", source: "Level1Techs forum", date: "2025"}
- {id: 32, title: "vLLM vs TensorRT-LLM #11: Speculative Decoding (SqueezeBits)", url: "https://blog.squeezebits.com/vllm-vs-tensorrtllm-11-speculative-decoding-37301", source: "SqueezeBits", date: "2024-12-09"}
- {id: 33, title: "Boost Llama 3.3 70B Inference Throughput 3x with TensorRT-LLM", url: "https://developer.nvidia.com/blog/boost-llama-3-3-70b-inference-throughput-3x-with-nvidia-tensorrt-llm-speculative-decoding/", source: "NVIDIA Developer Blog", date: "2024-12-17"}
- {id: 34, title: "LM Studio 0.3.10 release notes (speculative decoding)", url: "https://lmstudio.ai/blog/lmstudio-v0.3.10", source: "LM Studio", date: "2025-02-18"}
- {id: 35, title: "LM Studio Speculative Decoding documentation", url: "https://lmstudio.ai/docs/app/advanced/speculative-decoding", source: "LM Studio", date: "2026-05-17"}
- {id: 36, title: "mlx-examples PR #1155 — speculative decoding", url: "https://github.com/ml-explore/mlx-examples/pull/1155", source: "Apple MLX", date: "2024-12-15"}
- {id: 37, title: "MLX-LM discussion #890 — EAGLE-3 prototype on M3 Ultra", url: "https://github.com/ml-explore/mlx-lm/discussions/890", source: "Apple MLX-LM", date: "2026-02-14"}
- {id: 38, title: "Qwen3.6-35B-A3B speculative decoding RTX 3090 benchmark (thc1006)", url: "https://github.com/thc1006/qwen3.6-speculative-decoding-rtx3090", source: "GitHub community benchmark", date: "2026-04-19"}
- {id: 39, title: "llama.cpp issue #10594 — Q4_K_M target speculative regression", url: "https://github.com/ggml-org/llama.cpp/issues/10594", source: "llama.cpp project", date: "2024-11-28"}
- {id: 40, title: "Lookahead Decoding (LMSYS blog)", url: "https://lmsys.org/blog/2023-11-21-lookahead-decoding/", source: "LMSYS", date: "2023-11-21"}
- {id: 41, title: "REST: Retrieval-Based Speculative Decoding", url: "https://arxiv.org/abs/2311.08252", source: "arXiv 2311.08252", date: "2024-06-16"}
- {id: 42, title: "SpecInfer: Accelerating LLM Serving with Tree-based Speculative Inference", url: "https://arxiv.org/abs/2305.09781", source: "arXiv 2305.09781", date: "2024-04-01"}
- {id: 43, title: "Online Speculative Decoding", url: "https://arxiv.org/abs/2310.07177", source: "arXiv 2310.07177", date: "2024-05-30"}
- {id: 44, title: "DistillSpec: Improving Speculative Decoding via Knowledge Distillation", url: "https://arxiv.org/abs/2310.08461", source: "arXiv 2310.08461", date: "2024-03-15"}
- {id: 45, title: "SpecDec++: Boosting Speculative Decoding via Adaptive Draft Length", url: "https://arxiv.org/abs/2405.19715", source: "arXiv 2405.19715", date: "2024-05-30"}
- {id: 46, title: "Cascade Speculative Drafting", url: "https://arxiv.org/abs/2312.11462", source: "arXiv 2312.11462", date: "2024-12-10"}
- {id: 47, title: "Mamba Drafters for Speculative Decoding", url: "https://arxiv.org/abs/2506.01206", source: "arXiv 2506.01206", date: "2025-06-01"}
- {id: 48, title: "Making Deep Learning Go Brrrr From First Principles (Horace He)", url: "https://horace.io/brrr_intro.html", source: "horace.io", date: "2022-03-10"}
- {id: 49, title: "LLM Inference Performance Engineering: Best Practices (Databricks)", url: "https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices", source: "Databricks", date: "2023-10-12"}
- {id: 50, title: "DeepInfra pricing", url: "https://deepinfra.com/pricing", source: "DeepInfra", date: "2026-05-17"}
- {id: 51, title: "DeepSeek API pricing", url: "https://api-docs.deepseek.com/quick_start/pricing", source: "DeepSeek", date: "2026-05-17"}
- {id: 52, title: "EIA Short-Term Energy Outlook (US residential electricity 2026)", url: "https://www.eia.gov/outlooks/steo/pdf/steo_full.pdf", source: "U.S. Energy Information Administration", date: "2026-05-01"}
- {id: 53, title: "Mac Studio power consumption (Apple Support 102027)", url: "https://support.apple.com/en-us/102027", source: "Apple Support", date: "2025-03-12"}
- {id: 54, title: "M3 Ultra runs DeepSeek R1 efficiently (MacRumors)", url: "https://www.macrumors.com/2025/03/17/apples-m3-ultra-runs-deepseek-r1-efficiently/", source: "MacRumors", date: "2025-03-17"}
- {id: 55, title: "Anthropic ARR trajectory (SaaStr coverage)", url: "https://www.saastr.com/anthropic-just-passed-openai-in-revenue-while-spending-4x-less-to-train-their-models/", source: "SaaStr", date: "2026-04-15"}
- {id: 56, title: "Energy-Conscious LLM Decoding (spec dec energy)", url: "https://arxiv.org/abs/2502.11723", source: "arXiv 2502.11723", date: "2025-02-17"}
- {id: 57, title: "TokenPowerBench: Energy benchmarks for LLM inference", url: "https://arxiv.org/abs/2512.03024", source: "arXiv 2512.03024", date: "2025-12-03"}
- {id: 58, title: "AMD ROCm DeepSeek-V3 MTP tutorial", url: "https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/inference/mtp.html", source: "AMD ROCm", date: "2025-09-01"}
- {id: 59, title: "Mac Studio Qwen3-235B-A22B MLX vs GGUF (MacStories)", url: "https://www.macstories.net/notes/notes-on-early-mac-studio-ai-benchmarks-with-qwen3-235b-a22b-and-qwen2-5-vl-72b/", source: "MacStories", date: "2025-05-12"}
- {id: 60, title: "Speculative Decoding Meets Quantization", url: "https://arxiv.org/abs/2505.22179", source: "arXiv 2505.22179", date: "2025-05-28"}
- {id: 61, title: "Apple Recurrent Drafter (Apple ML Research)", url: "https://machinelearning.apple.com/research/recurrent-drafter", source: "Apple ML Research", date: "2024-11"}
- {id: 64, title: "llama.cpp + NVIDIA collaboration: Ministral-3B at 385+ tok/s on RTX 5090 (ggerganov)", url: "https://x.com/ggerganov/status/1995931445425271232", source: "X / Georgi Gerganov", date: "2025-12-02"}
- {id: 65, title: "How Speculative Decoding Boosts vLLM Performance by up to 2.8x", url: "https://blog.vllm.ai/2024/10/17/spec-decode.html", source: "vLLM", date: "2024-10-17"}
- {id: 66, title: "An Introduction to Speculative Decoding for Reducing Latency in AI Inference (NVIDIA)", url: "https://developer.nvidia.com/blog/an-introduction-to-speculative-decoding-for-reducing-latency-in-ai-inference/", source: "NVIDIA Developer Blog", date: "2025-09-17"}
- {id: 67, title: "Mac Studio M3 Ultra 512GB at $9,499 (ServeTheHome)", url: "https://www.servethehome.com/new-512gb-unified-memory-apple-mac-studio-is-the-local-ai-play/apple-mac-studio-m3-ultra-512gb-9499-base-price/", source: "ServeTheHome", date: "2025-03-12"}
- {id: 68, title: "BitNet b1.58 2B4T Technical Report", url: "https://arxiv.org/abs/2504.12285", source: "arXiv 2504.12285 / Microsoft", date: "2025-04-15"}
:::
