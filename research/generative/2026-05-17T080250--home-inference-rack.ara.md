---
eyebrow: REPORT · HARDWARE
title: The Home Inference Rack
deck: Can a Mac mini plus a consumer GPU fleet beat cloud APIs in 2026? Short answer — sometimes, for specific people, with surprising conditions.
lede: |
  In May 2026 a single Apple M3 Ultra Mac Studio decodes a 671-billion-parameter DeepSeek-V3 at roughly 21 tokens per second on 4-bit weights, drawing under 200 watts. Four M5 Max MacBooks lashed together over Thunderbolt 5 RDMA pool 512 GB of unified memory at 2,456 GB/s aggregate bandwidth for $20,000 — a stack Exo Labs founder Alex Cheema says a government is now running in production. Meanwhile, DeepInfra serves an open-weight Llama 3.3 70B at $0.10 per million input tokens, DeepSeek's first-party API runs a 671B MoE for $0.27/M, and Claude Sonnet 4.6 has held at $3/$15 across seven releases since March 2024. The home-rack thesis asks whether the silicon on your desk can beat that floor — and the honest answer turns on prefill latency, batched serving, and whether your workload looks more like Haiku-class chat or DeepSeek-class agentic inference.
stats:
  - {label: M3 Ultra 4-bit 671B decode, value: "21 tok/s", note: single Mac Studio}
  - {label: 4× M5 Max MacBook cluster, value: "$20K", note: 512 GB at 2,456 GB/s}
  - {label: Cheapest hosted Llama 70B, value: "$0.10/M", note: DeepInfra input price}
  - {label: Closed→open Elo gap, value: "~39", note: LMArena, May 2026}
  - {label: GPT-4 → GPT-5.4-nano, value: "150×", note: input price collapse in 3 yr}
  - {label: 4090 daily TCO (US avg), value: "$2.51", note: $2K used + 160 W avg}
---

## 01. The 2026 substrates

The personal-AI hardware ladder of 2026 has settled into four distinct rungs — Apple M-series unified memory, NVIDIA's DGX Spark, AMD's Strix Halo APUs, and the legacy consumer-GPU rig — and at every rung the binding constraint on token generation is memory bandwidth, not FLOPS.[^1]

The cheapest entry point is a base Mac mini M4: $599, 16 GB of unified memory (32 GB upgrade available), 120 GB/s, and a 65 W maximum board draw.[^2][^3] Step up to the M4 Pro mini at $1,399 and you get 64 GB at 273 GB/s in a 140 W envelope — the same bandwidth class as a $4,699 DGX Spark.[^2][^3][^4] At the top of Apple's stack, the M3 Ultra Mac Studio shipped in March 2025 with a 32-core CPU, 80-core GPU, and 819 GB/s of unified bandwidth starting at $3,999.[^5] The maxed-out 512 GB SKU added another $4,000 — $14,099 fully configured — before Apple quietly pulled both the 256 GB and 512 GB options in early 2026 and raised the 256 GB upgrade from $1,600 to $2,000, a tell that the AI DRAM squeeze is real even for vertically integrated buyers.[^5][^6] A MacBook Pro M4 Max tops out at 128 GB / 546 GB/s; the M5 chip lifted base bandwidth 30% to 153 GB/s, and the M5 Ultra Studio is expected in H2 2026.[^7][^8]

NVIDIA's response was Project DIGITS, announced at CES 2025 at a $3,000 sticker.[^9] The product that actually shipped on October 15, 2025 was the DGX Spark at $3,999 MSRP, which NVIDIA then hiked to $4,699 by February 2026 — a 57% price drift in thirteen months.[^4] Spark uses the GB10 Grace-Blackwell superchip: 20 Arm cores, 128 GB of LPDDR5x, 273 GB/s, 140 W TDP — the same bandwidth class as the M4 Pro Mac mini and roughly one-third of the M3 Ultra, a striking outcome given NVIDIA's CUDA moat.[^4] The pitch is twofold: ConnectX-7 networking lets two Sparks gang up to host a 405B-parameter model, and the box runs the standard CUDA stack on day one.[^4]

AMD slotted in below both. The Ryzen AI Max+ 395 ("Strix Halo") packs 16 Zen 5 cores, 40 RDNA 3.5 compute units, a 50 TOPS NPU, and supports up to 128 GB of LPDDR5x.[^10] Theoretical bandwidth is 256 GB/s; measured throughput on the Framework Desktop sits around 215 GB/s.[^11] Framework shipped that desktop on February 26, 2025, starting at $1,099 and topping out at $1,999 for the 128 GB variant — and sold out seven batches in two months.[^12] On dollars-per-GB of fast RAM, Strix Halo is the floor of the market.

Then there is the legacy rig: an ATX case, one or more discrete GPUs, and a PSU to match. The pricing has decoupled from MSRP. RTX 4090 production halted in fall 2024; used cards traded $1,500–$2,450 by May 2026 against a $1,599 launch price.[^13] The RTX 5090 carries a $1,999 MSRP but sold for an average $3,658 street as of May 2026, with a 575 W TDP.[^14] Used RTX 3090s — still 24 GB at 936 GB/s — clear at $800–$1,050.[^15] At the top of the consumer-adjacent stack, the RTX PRO 6000 Blackwell datasheet specs 96 GB of GDDR7 at 1,597 GB/s in a 600 W envelope, with channel pricing $8,000–$9,200.[^1][^16] Used datacenter parts — A100 80 GB at $6,300–$18,900, H100 at $15,000–$28,000 — round out the long tail.[^17][^18]

:::rank-list
- {label: "RTX 5090", value: "1,792 GB/s", pct: 100}
- {label: "RTX PRO 6000 Blackwell", value: "1,597 GB/s", pct: 89}
- {label: "RTX 4090", value: "1,008 GB/s", pct: 56}
- {label: "RTX 3090 (used)", value: "936 GB/s", pct: 52}
- {label: "Mac Studio M3 Ultra", value: "819 GB/s", pct: 46, highlight: true}
- {label: "MacBook Pro M4 Max", value: "546 GB/s", pct: 30}
- {label: "Mac mini M4 Pro", value: "273 GB/s", pct: 15}
- {label: "NVIDIA DGX Spark (GB10)", value: "273 GB/s", pct: 15}
- {label: "AMD Strix Halo (Framework)", value: "215 GB/s", pct: 12}
- {label: "Mac mini M4 (base)", value: "120 GB/s", pct: 7}
:::

The 14× price spread between the cheapest and most expensive substrate buys only ~15× the bandwidth, and capacity-versus-bandwidth is not a clean tradeoff.

:::compare
- {role: LOWEST, name: "Used RTX 3090 · 24 GB", value: "$1,000"}
- {role: HIGHEST, name: "RTX PRO 6000 · 96 GB", value: "$9,000"}
- {role: SUBJECT, name: "Mac Studio M3 Ultra · 512 GB", value: "$14,099"}
:::

But bandwidth is not the whole story. A 4090 with 1,008 GB/s is theoretically 23% faster per byte than an M3 Ultra at 819 GB/s — yet it can't decode a 70B-parameter model in Q4 at all, because the weights don't fit in 24 GB. Capacity gates which models you can run; bandwidth gates how fast they generate. The 4-bit ceilings shake out cleanly: ~50B parameters at 32 GB, ~100B at 64 GB, ~200B at 128 GB, ~670B at 512 GB.[^7] That is why a maxed Mac Studio — slower per byte than every NVIDIA card on the chart — was the only consumer box that could host DeepSeek-V3-class models locally before Apple yanked the SKU.

Idle and load power are the other axis cloud comparisons ignore. The base Mac mini M4 idles at 4 W and peaks at 65 W; the M4 Pro at 5 W / 140 W; the M3 Ultra Mac Studio at 9 W / 270 W.[^3][^19] An RTX 5090 alone draws 575 W TDP, averages 559 W under gaming load, and peaks above 700 W; an H100 SXM is rated 700 W.[^14][^20] A four-3090 rig pulls more wall power continuously than a refrigerator. For an always-on personal inference endpoint, the Apple boxes are not in the same power class as anything from NVIDIA — that is a real, recurring TCO line item before you even price the silicon.

The equity market has priced both bets to keep winning:

:::line-chart(title="AAPL & NVDA monthly close, June 2024 – May 2026", subtitle="Yahoo Finance · the market priced both bets", y-unit=$)
x: 2024-06,2024-07,2024-08,2024-09,2024-10,2024-11,2024-12,2025-01,2025-02,2025-03,2025-04,2025-05,2025-06,2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05
AAPL: 210.62,222.08,229.0,233.0,225.91,237.33,250.42,236.0,241.84,222.13,212.5,200.85,205.17,207.57,232.14,254.63,270.37,278.85,271.86,259.48,264.18,253.79,271.35,300.23
NVDA: 123.54,117.02,119.37,121.44,132.76,138.25,134.29,120.07,124.92,108.38,108.92,135.13,157.99,177.87,174.18,186.58,202.49,177.0,186.5,191.13,177.19,174.4,199.57,225.32
:::

AAPL is up ~43% and NVDA up ~82% over the window, but they're winning different jobs: NVIDIA owns prefill and training, Apple owns idle-cheap, fits-in-a-drawer decode.[^21]

Why this matters: the ladder is the substrate every later argument in this piece rests on. Picking a rung dictates which models you can serve, what your watts-per-token look like, and whether scaling means another box on the desk or another card in the case.

## 02. What you can actually run

In May 2026 the open-weight frontier sits roughly 40 LMArena Elo points behind the closed frontier — meaningfully close enough that the honest answer to "what can you run at home?" is *nearly everything*, with a 3–5 percentage-point deficit on reasoning-heavy academic evals and a measurable surplus on agentic coding tasks.

The shape of the open ladder has changed twice in eighteen months. In December 2024 Meta's Llama 3.3 70B Instruct was the reference dense model — MMLU 86.0, MMLU-Pro 68.9, GPQA-Diamond 50.5, HumanEval 88.4, MATH 77.0, IFEval 92.1 — the best thing that fit on a single 80 GB card.[^22] Two weeks later DeepSeek V3 detonated the cost narrative: a 671B-parameter MoE with 37B active, trained on 14.8T tokens in ~2.788M H800-hours for roughly $5.6M, scoring MMLU 88.5 / MMLU-Pro 75.9 / GPQA-D 59.1 / MATH-500 90.2.[^23] Three weeks after *that*, DeepSeek R1 (MIT-licensed) posted reasoning numbers — MMLU 90.8, GPQA-D 71.5, AIME-2024 79.8, MATH-500 97.3 — that DeepSeek themselves described as "on par with OpenAI-o1."[^24]

:::compare
- {role: LOWEST, name: "DeepSeek V3", value: "$5.6M"}
- {role: HIGHEST, name: "GPT-4 (est.)", value: "~$100M+"}
- {role: SUBJECT, name: "DeepSeek V3", value: "$5.6M"}
:::

The GPT-4 figure is a contested 2023 estimate; treat it as a Fermi anchor, not a ledger entry. Qwen 2.5 72B Instruct meanwhile beat Llama 3.1 405B on math and code despite having 5.6× fewer parameters — MMLU-Pro 71.1, HumanEval 86.6, MATH 83.1, Arena-Hard 81.2 — collapsing the "you need a hyperscaler to be competitive" assumption from a different direction.[^25] In April 2025 Alibaba released the Qwen3 family in **eight sizes from 0.6B to 235B-A22B MoE under Apache 2.0**, finally giving local operators a coherent menu from edge to workstation.[^26]

Llama 4, released the same week, took the opposite tack: an MoE hierarchy of Scout (109B / A17B, 10M context), Maverick (400B / A17B, 128 experts), and the unreleased Behemoth (~2T / A288B), with Maverick benchmarking MMLU-Pro 80.5 and LiveCodeBench 43.4.[^27] It is also the section's first counterpoint. Within 72 hours analysts noticed that the LMArena leaderboard variant — a "conversationality-optimized" Maverick that scored ~1417 Elo (rank #2) — was not the model whose weights Meta had shipped; the publicly downloadable Maverick scored ==unverified: ~1273 Elo (rank #32)== on the same arena.[^28] Treat every headline benchmark, including everything in the table below, with the discount this episode earned.

On the public Chatbot Arena leaderboard as of May 12, 2026:[^29]

:::rank-list
- {label: "GPT-5.5-high (closed, OpenAI)", value: "1506", pct: 100}
- {label: "Claude Opus 4.7 Thinking (closed, Anthropic)", value: "1505", pct: 99}
- {label: "Gemini-3.1-Pro (closed, Google)", value: "1505", pct: 99}
- {label: "GLM-5.1 (open, MIT, China)", value: "1467", pct: 70, highlight: true}
- {label: "DeepSeek-V4-Pro (open, MIT, China)", value: "1467", pct: 70}
- {label: "Qwen3.5-Max (open, Apache 2.0, China)", value: "1466", pct: 68}
:::

The other counterpoint is structural. In July 2025 Mark Zuckerberg signalled that Meta's superintelligence-tier models "may stay closed for safety reasons," ending the assumption that the frontier-lab-with-open-weights would remain a Western phenomenon.[^30] By April 2026 the open frontier was entirely Chinese: DeepSeek V4-Pro (1.6T / 49B active, 1M context, trained on 32T tokens) and its sibling V4-Flash (284B / 13B active) shipped under MIT, with V4-Pro leading Opus 4.6 on Terminal-Bench 2.0 (67.9 vs 65.4) and LiveCodeBench (93.5 vs 88.8) while trailing Gemini 3.1 Pro on MMLU-Pro (87.5 vs 91.0) and GPQA-D (90.1 vs 94.3).[^31][^32] The pattern is consistent across the open frontier: coding-task surplus, reasoning-eval deficit, conversational parity.

:::kv
- {term: "Llama 3.3 70B", def: "Dense, Llama Community License (Dec 2024)"}
- {term: "DeepSeek V3", def: "671B MoE / 37B active, MIT (Dec 2024)"}
- {term: "DeepSeek R1", def: "Reasoning, MIT (Jan 2025)"}
- {term: "DeepSeek V4-Pro", def: "1.6T MoE / 49B active, MIT (Apr 2026)"}
- {term: "Qwen3 family", def: "0.6B–235B-A22B MoE, Apache 2.0 (Apr 2025)"}
- {term: "Llama 4 Maverick", def: "400B-A17B MoE, Llama Community License (Apr 2025)"}
- {term: "Mistral Large 2", def: "123B dense, Mistral Research (non-commercial)"}
:::

License matters as much as benchmarks. Mistral Large 2 (123B dense, MMLU 84.0, July 2024) is technically competitive but ships under a non-commercial research license that disqualifies it from most production use — a reminder that the dense-model era's last European entry was eclipsed both architecturally (by MoE) and legally (by MIT/Apache permissiveness).[^33] DeepSeek's recent 75% V4-Pro API promo through 31 May 2026, and its quiet integration into Anthropic's Claude Code as a routing target, make the price comparison even uglier for the closed labs.[^34]

What does this mean for the rack? At 4-bit Q4_K_M quantization the perplexity penalty is ~0.18 on Wikitext-2 for Llama-3-8B (Q8_0 adds only +0.003) — small enough to be invisible in product testing.[^35] Apple's unified-memory ceilings then dictate the menu: 32 GB fits ~50B params at 4-bit, 64 GB ~100B, 128 GB ~200B, and the 512 GB M3 Ultra Mac Studio fits all 670B of DeepSeek V3 in one box.[^7] The Maverick scandal and the reasoning-eval gap argue against treating open weights as drop-in substitutes for Opus or GPT-5.5 on math-olympiad and PhD-qualifier workloads. Why this matters: for the 80% of production traffic that is summarization, retrieval-augmented Q&A, code completion, and structured extraction, the home rack is no longer making a quality compromise — it is making a latency, privacy, and unit-economics choice.

## 03. Bandwidth wins decode, compute loses prefill

LLM inference is two workloads in a trench coat: a memory-bandwidth-bound decode loop where Apple's unified memory genuinely competes with an H100, and a compute-bound prefill that exposes a roughly 30× FLOPS gap and decides whether a home Mac is a usable inference box or a beautiful brick.

The split is mechanical. Decode generates one token at a time; each step streams the entire model's weights through the matmul units once, so wall-clock is governed by memory bandwidth, not arithmetic. Prefill ingests the prompt in parallel, batching across the sequence dimension, which turns the same matmuls into compute-bound GEMMs that want raw FLOPS. The hardware ladder that wins one regime is not the hardware ladder that wins the other. An M3 Ultra rates roughly 65.5 TFLOPS FP16 against an H100 SXM's 1,979 TFLOPS — a ~30× gap [^36] — while its 819 GB/s of unified memory bandwidth sits within a small constant factor of the H100's HBM3. M5 Max nudges the FLOPS figure to ~70 TFLOPS; an RTX 5090 lands near 380, and the RTX PRO 6000 near 500 [^37]. The asymmetry between those two ratios — bandwidth close, FLOPS catastrophically far — is the entire story of this section.

The published numbers are unambiguous. On Llama-3 70B Q4_K_M with a 1,024-token prompt, an H100 PCIe 80GB processes 984 tok/s of prefill against an M2 Ultra's 117.76 tok/s — about 8.4× — while decode for the same model on the M2 Ultra clocks 12.13 tok/s, perfectly respectable for a desktop [^38]. Move to Llama-3 8B at FP16 and the prefill gap widens further: H100 at 10,342 tok/s, RTX 4090 at 9,056, M2 Ultra at 1,202, M3 Max at 751 [^38]. The same llama.cpp Metal traces show the within-Mac asymmetry directly — on M3 Ultra Q4_0, prompt processing runs 1,471 tok/s while token generation runs 92 tok/s, a 16× spread between the two regimes on identical silicon [^39].

:::compare
- {role: LOWEST, name: "M2 Ultra (Mac Studio)", value: "118 tok/s"}
- {role: HIGHEST, name: "H100 PCIe 80GB", value: "984 tok/s"}
- {role: SUBJECT, name: "M3 Ultra (Mac Studio)", value: "~150 tok/s"}
:::

The prefill problem compounds with context length, because KV cache size grows linearly with tokens and quadratically pressures the attention matmul. Ivan Fioravanti's M3 Ultra DeepSeek V4 Flash run watched prefill collapse from 419 tok/s at 0.5k context to 99 tok/s at 16k while decode held roughly steady near 31 tok/s [^40]. A separate M3 Ultra 512 GB run of DeepSeek-V3 0324 4-bit showed decode itself sliding from 21.05 tok/s at 69 tokens of context to 17.81 at 1,145 and 5.79 at 15,777 — the bandwidth-bound regime degrades too once the KV cache is the dominant streamed object [^41]. For Llama-3.1-70B with GQA-8, that cache is ~10 GB at 32k tokens and ~40 GB at 128k per request in FP16, which is why a practitioner stress-test of GLM 4.6 5-bit on the same M3 Ultra 512 GB settled on roughly 32k tokens as the practical prefill ceiling — beyond that, time-to-first-token becomes hostile [^42][^43].

:::line-chart(title="DeepSeek-V3 4-bit decode on M3 Ultra 512 GB", subtitle="Tokens/sec as context grows", y-unit="tok/s")
x: 69,1145,15777
tok/s: 21.05,17.81,5.79
:::

This is exactly the workload coding agents generate. A Claude Code or Cursor session shovels 20k–50k tokens of system prompt, repo context, and tool definitions on every turn; first-token latency dominates perceived speed because the model has to chew the whole context before a single character appears. The result is brutal on Apple silicon. One practitioner using K2.5 on a "cheap Mac setup" puts it plainly:

:::quote(attr="@sdmat123, coding-agent user, March 2026")
K2.5 at long context will drop into the low teens on the cheap mac setup. With terribly slow prefill — a Mac setup is going to be compute bound doing so, you really want GPUs.[^44]
:::

And the prefill problem is not Apple-exclusive — it is a memory-bandwidth-class problem that hits any system whose FLOPS/byte ratio undershoots a discrete GPU. NVIDIA's DGX Spark, a unified-memory ARM box explicitly aimed at this market, posts 803 tok/s prefill and 2.7 tok/s decode on Llama 3.1 70B FP8 — competitive prefill but the same bandwidth-pinned decode story in reverse [^45]. The architecture choice is a regime choice.

The counterpoint is that Apple noticed. The M5's per-core Neural Accelerators close roughly 4× of the prefill gap versus M4 on a 10K-token Qwen3-8B-4bit prompt: M4 took 81 seconds to first token, M5 took 18 [^46]. On Gemma 34B prompt-processing, M5 Max hits 4,468 tok/s against M4 Max's 1,855 and M3 Ultra's 2,959 — the first time a binned Max chip beats a top-bin Ultra at prefill [^47]. Expressed as effective prefill throughput, the M4→M5 jump on the Qwen3 long-prompt test is 124 → 556 tok/s, a 4.5× generational delta that no x86 vendor matched in 2025.

:::slope(left-label="M4 Max", right-label="M5 Max", unit="tok/s")
| Workload | M4 Max | M5 Max |
|---|---|---|
| Qwen3-8B-4bit @10k (effective prefill) | 124 | 556 |
| Gemma 34B prefill | 1855 | 4468 |
:::

The second escape hatch is software. Without prefix caching, an MLX 40k-token prefill takes ~200 seconds; with cache reuse on a warmed-up agentic flow, the same prompt completes in ~5 seconds — a 40× speedup that turns cold-start pain into amortized warm-loop comfort [^48]. Coding agents, which replay 90%+ of their context across turns, are the workload that benefits most from prefix caching and the workload most punished by cold prefill. The same prompt structure is the bug and the fix.

Why this matters: the home-rack pitch lives or dies on whether your workload tolerates 30 seconds of TTFT for a single agentic turn, because that is the gap a 30× FLOPS deficit imposes at the context lengths coding tools actually use — and no amount of bandwidth fixes it until the M5 Neural Accelerators (or their successors) close another order of magnitude.

## 04. The cluster gambit

When one box runs out of memory — for a 671B DeepSeek MoE, a trillion-parameter Kimi K2.5, or simply to multiply aggregate bandwidth — the open-source distributed-inference stack has, in the last six months, crossed the line from party trick to production deployment.

The story is best told by Exo Labs founder Alex Cheema, whose January 2025 cost-per-GB ledger reframed the entire local-inference debate. At the time, an NVIDIA H100 80 GB cost roughly $25,000, or {accent}$312.50 per GB{/} of HBM; AMD's MI300X 192 GB landed at $104.17/GB; an Apple M2 Ultra Mac Studio with 192 GB of unified memory came in at $26.04/GB.[^49] Per gigabyte of model-weight capacity, an Apple desktop was ~12× cheaper than an H100, which is the number that started everyone gluing Mac minis together.

:::compare
- {role: LOWEST, name: "Apple M2 Ultra (192 GB, $5K)", value: "$26.04/GB"}
- {role: HIGHEST, name: "NVIDIA H100 (80 GB, $25K)", value: "$312.50/GB"}
- {role: SUBJECT, name: "Apple M2 Ultra (192 GB, $5K)", value: "$26.04/GB"}
:::

The chronology of viral demos is the proof of work. In July 2024, a hobbyist wired 23 base-model Mac minis (16 GB each, 368 GB total) into a single fabric and ran Llama-3 405B at Q4_K_S quantization.[^50] By November, Cheema had compressed that into four M4 Pro Mac minis sharing a Thunderbolt 5 mesh, hitting 8 tok/s on Nemotron 70B with headroom for 405B.[^51] In December 2024, Exo sharded DeepSeek-V3 671B across eight M4 Pro minis — 512 GB of pooled unified memory — the first credible local serving of a frontier MoE.[^52]

:::timeline
- {date: "2024-07", headline: "First viral cluster", body: "@ac_crypto runs Llama-3-405B Q4_K_S across 23 Mac minis (368 GB total) — the proof-of-concept that lit the fuse."}
- {date: "2024-11", headline: "Mac mini M4 cluster", body: "Cheema's 4× M4 Pro mini build runs Nemotron 70B at 8 tok/s over Thunderbolt 5; promises 405B 'soon.'"}
- {date: "2024-12", headline: "DeepSeek V3 on 8× Mac mini", body: "Exo shards 671B MoE across 8× M4 Pro 64 GB minis — 512 GB total unified pool."}
- {date: "2025-11", headline: "RDMA-over-TB5 lands", body: "macOS Tahoe 26.2 ships RDMA over Thunderbolt 5; tensor-parallel scaling finally unlocks."}
- {date: "2025-12", headline: "Geerling's 1.5 TB cluster", body: "Jeff Geerling's 4-node M3 Ultra cluster scales DeepSeek V3.1 671B from 21.1 → 32.5 tok/s."}
- {date: "2026-04", headline: "1T params on AMD", body: "AMD publishes a 4× Framework Desktop reference build running Kimi K2.5 (1T params, 32B active) via llama.cpp RPC."}
- {date: "2026-05", headline: "MacBook cluster in prod", body: "Cheema's 4× M5 Max MacBook RDMA build delivers 512 GB at 2,456 GB/s for $20K — and ships to a government customer."}
:::

The unlock that turned 2024's curiosities into 2026's deployable systems was {accent}RDMA over Thunderbolt 5{/}, which Apple shipped in macOS Tahoe 26.2 in November 2025. Pre-RDMA, a 4-node Mac Studio cluster gave only a 54% performance gain from 4× the compute — the interconnect was eating the win. Post-RDMA, latency dropped from ~300 μs to single-digit microseconds, and tensor parallelism roughly tripled throughput.[^53] Jeff Geerling's December 2025 benchmark on a 4-node M3 Ultra cluster (1.5 TB of unified VRAM across the box) is the cleanest scaling receipt: DeepSeek V3.1 671B at ==unverified: 21.1 tok/s on one node, 27.8 on two, 32.5 on four== — the exact figures circulate via secondary summaries while Geerling's blog shows them only in embedded benchmark images.[^54]

:::line-chart(title="DeepSeek V3.1 671B on Mac Studio cluster, RDMA-over-Thunderbolt-5", subtitle="Jeff Geerling, Dec 2025", y-unit="tok/s")
x: 1 node,2 nodes,4 nodes
tok/s: 21.1,27.8,32.5
:::

That is the context for Cheema's May 2026 headline build, which has anchored every cluster argument since: four M5 Max MacBooks lashed together with Thunderbolt 5 RDMA, delivering 512 GB of unified memory at 2,456 GB/s aggregate bandwidth, 240 TFLOPS FP16, $20,000, 560 W, and silent operation, tested running LLMs continuously for eight hours with no performance loss.[^55][^56] Compared head-to-head against an M3 Ultra Mac Studio (512 GB, 819 GB/s, 26 TFLOPS), the laptop cluster offers 3× the bandwidth and ~9× the compute for similar weight capacity.[^56]

:::stats
- {label: Unified memory, value: "512 GB"}
- {label: Aggregate bandwidth, value: "2,456 GB/s"}
- {label: Total cost, value: "$20K"}
- {label: Sustained power, value: "560 W"}
- {label: FP16 compute, value: "240 TFLOPS"}
:::

:::quote(attr="Alex Cheema, Exo Labs founder, May 2026")
The shitstorm of supply chain issues has created a new best-in-class local AI deployment: M5 Max MacBook clusters. You can't get Mac Studios right now, so customers are buying MacBook clusters instead. A government is running this in prod.[^55]
:::

Crucially this is not an Apple-only story. In April 2026, AMD published a reference build of four Framework Desktops running Kimi K2.5 — a 1-trillion-parameter MoE with 32B active — via llama.cpp's RPC backend, the same plumbing approach as Exo with a different silicon vendor on the other end.[^57] On the MLX side, Awni Hannun (Apple's MLX lead) clocked Kimi K2.5 running in native precision across two M3 Ultras via mlx-lm sharding at 21.9 tok/s, ~350 GB per node.[^58] The orchestration layer has consolidated: Exo's open-source project sits at 44.7K GitHub stars, with v1.0.71 shipping the RDMA-over-TB5 stack and a claimed 99% latency reduction.[^59] The earlier swing at this problem, BigScience's Petals, has been effectively defunct since its v2.2.0 release in September 2023.[^60] Independent reproductions exist outside the Exo Labs blog — one user runs a 6-node M1 Studio Max cluster over plain Thunderbolt 4 (no RDMA) serving Qwen3.5-122B-A10B 8-bit at 17.8 tok/s.[^61]

:::callout(kind=warn, label=Counterpoint)
Three caveats before declaring victory. First, the celebrated 4× scaling number is recent and fragile — pre-RDMA, the same 4-node topology netted only 54% performance gain, and RDMA-over-TB5 only landed in shipping macOS in November 2025.[^53] Second, the absolute throughput on giant MoE models is still modest by API standards: 32.5 tok/s on DeepSeek 671B across four M3 Ultras is roughly an order of magnitude below what a Groq or SambaNova endpoint returns on a smaller 70B model. Third, Cheema's framing of "$20K cluster vs $780K NVIDIA build" is the founder of a cluster-orchestration startup pricing his own win — treat it as a directional claim, not an audited TCO.[^55][^62]
:::

Why this matters: for the first time, an open-source software stack, a consumer interconnect, and a fleet of laptops can pool enough unified memory to serve frontier MoE weights locally — slowly, but at single-digit-thousands-of-dollars per gigabyte instead of hundreds. The cluster gambit is no longer about whether it works; it's about whether the tokens-per-second gap to a cloud endpoint matters for your workload.

## 05. The cloud price collapse

The price floor for serving an open-weight 70B is now $0.10 per million input tokens at DeepInfra,[^63] DeepSeek's own first-party API charges $0.27/M for a 671B MoE,[^64] and the frontier closed labs have either held the line (Anthropic Sonnet $3/$15 unchanged for seven releases since March 2024)[^65] or moved in the opposite direction (OpenAI GPT-5.5 input price 8×'d from GPT-5 in nine months)[^66] — a divergence that, combined with stacked 50% batch and 90% cache discounts,[^65][^66] makes the cloud math against any home rig keep getting harder, not easier, almost month over month.

### The open-weight floor has fallen through

Hosting commodity 70B-class open weights is now a knife fight where the cheapest tier sits at ten cents per million input tokens. DeepInfra serves Llama 3.3 70B Instruct at $0.10/M input and $0.32/M output[^63] — the lowest hosted price observed for that weight class. Together AI charges $0.88/M flat across input and output for the same model;[^67] Groq runs it at $0.59 in / $0.79 out at 394 TPS;[^68] SambaNova at $0.60/$1.20 on RDU;[^69] and Cerebras matches at $0.60/M flat while pushing 1,800 TPS, the fastest accelerator inference on record.[^70] Ranked on input price, the picture is brutally compressed:

:::rank-list
- {label: "DeepInfra · Llama 3.3 70B", value: "$0.10 in · $0.32 out", pct: 100, highlight: true}
- {label: "Groq · 394 TPS", value: "$0.59 in · $0.79 out", pct: 17}
- {label: "Cerebras · 1,800 TPS", value: "$0.60 flat", pct: 17}
- {label: "SambaNova · RDU", value: "$0.60 in · $1.20 out", pct: 17}
- {label: "Together AI", value: "$0.88 flat", pct: 11}
:::

Step up one weight class and the same compression holds: Cerebras runs Llama 3.1 405B at $6/$12 with 969 TPS — what the company itself calls "12× faster than the best GPU result."[^71] That is dense-model territory; on the MoE side, the floor falls again. DeepSeek's own first-party API charges $0.27/M (cache miss) and $0.07/M (cache hit) for `deepseek-chat` (V3-class, 671B MoE), with $1.10/M output.[^64] The reasoning tier `deepseek-reasoner` (R1-class) is $0.55/M input miss, $0.14 cache hit, $2.19/M output[^64] — roughly 10× cheaper than Together's $3/$7 R1 hosting of the same open weights.[^72] Same model, ten times the price, depending on whose silicon serves it.

### The 2024→2026 collapse, quantified

Two years ago, Together's Llama 70B tier sat at about $0.90/M; today the same vendor is at $0.88/M, but the cheapest tier (DeepInfra) is at $0.10/M — a ~9× collapse at the floor over 24 months.[^73] Stretched out further, the curve gets uglier still: GPT-4 launched at $30/M input in March 2023; GPT-5.4-nano is now $0.20/M[^66] — a 150× collapse at the cheap end, and a 12× collapse from GPT-4 to standard GPT-5.4 at $2.50.[^66] OpenRouter routing shows the resulting fan-out as a 400× spread between Claude Opus 4.7 Fast at $30/M and Ring-2.6-1T at $0.075/M for the same prompt.[^74]

:::stats
- {label: "Anthropic cache hit", value: "0.10×", note: "vs base input price"}
- {label: "OpenAI cache hit", value: "0.10×", note: "vs base input price"}
- {label: "Batch API discount", value: "50%", note: "Together, Groq, Anthropic, OpenAI"}
- {label: "GPT-4 → GPT-5.4-nano", value: "150×", note: "input price collapse, 3 yr"}
:::

### Stacked discounts: the 20× compound

The headline rate is only the start. Anthropic gives a 90% discount on cached input and a 50% discount on both legs through the Batch API;[^65] OpenAI matches the cache discount and offers the same 50% batch;[^66] Together[^67] and Groq[^75] both run 50% batch tiers. Stacked, the marginal cost of a cached, batched Opus input call is $0.25/M instead of $5/M — a 20× compound discount on the frontier list price. To make this concrete:

:::compare
- {role: LOWEST, name: "DeepInfra · Llama 3.3 70B (open weights)", value: "$0.10/M in"}
- {role: SUBJECT, name: "DeepSeek V3 · 671B MoE (first-party)", value: "$0.27/M in"}
- {role: HIGHEST, name: "Claude Opus 4.7 (frontier)", value: "$5.00/M in"}
:::

A home rig has to beat $0.10/M on a routine 70B call and $0.27/M on a frontier-quality MoE just to break even on tokens served — before electricity, before the depreciation schedule on whatever silicon does the serving, and before the operator's time.

### The frontier output ladder

Output pricing is where the spread really shows. Anthropic has held Sonnet at $3/$15 across seven Sonnet releases since March 2024[^65] — and held Opus 4.7 at $5/$25, unchanged from 4.6.[^65] Haiku 4.5 sits at $1/$5.[^65] Google undercuts the lot with Gemini 3.1 Pro Preview at $2/$12 (≤200K context) and Gemini 2.5 Flash-Lite at $0.10/$0.40, with a free AI Studio tier on top.[^76] OpenAI is the only major lab moving the other way: GPT-5.5 launched April 23, 2026 at $5/$30 — an 8× jump on input from GPT-5.4's $2.50, and the reasoning-tier GPT-5.5 Pro is $30/$180, a 6× premium over the standard tier.[^66]

:::donut(center-label="$/M out")
- {label: "GPT-5.5 Pro (reasoning)", value: 180}
- {label: "GPT-5.5 (standard)", value: 30}
- {label: "Claude Opus 4.7", value: 25}
- {label: "Gemini 3.1 Pro (>200K)", value: 18}
:::

### Counterpoint: not everything gets cheaper

Two facts complicate the "cloud always falls" narrative. First, GPT-5.5 is a real price hike — an 8× input increase in nine months on the most-watched frontier API,[^66] and a signal that reasoning-tier pricing (GPT-5.5 Pro at $30/$180) is moving toward 6× premiums over the standard tier rather than approaching it. Second, the 400× OpenRouter spread suggests the floor is now architecture-driven — MoE plus sparse experts at DeepSeek and Ring-1T routing — more than it is "compute getting cheaper." If frontier dense models stop benefiting from the same MoE tricks, the gap between $0.10/M open hosting and $30/M frontier-reasoning could widen, not close.

Why this matters: to beat $0.10/M of Llama 70B input or $0.27/M of DeepSeek V3 at home, a Mac mini plus consumer GPU stack has to amortize hardware, power, and operator time against a cloud floor that has fallen ~9× in 24 months and 150× in three years — and is still falling for everything except OpenAI's flagship. The next section runs that break-even math.

## 06. The break-even math

The honest break-even for a $2,000 used RTX 4090, amortized over three years and run at a realistic 20%-load duty cycle on US-average power, lands at ~502K output tokens per day against Claude Haiku 4.5 and ~5.98M tokens per day against DeepSeek V3 — meaning local serving wins on Haiku-class workloads and loses on the open-API floor for any single user.

:::stats
- {label: "Tokens/day to beat Haiku 4.5", value: "502K", note: "single 4090, 3-yr amort"}
- {label: "Tokens/day to beat DeepSeek V3", value: "5.98M", note: "same box; needs batched serving"}
- {label: "Daily cost (US avg)", value: "$2.51", note: "$2K capex + electricity"}
- {label: "Daily cost (Hawaii)", value: "$3.49", note: "same rig, $0.43/kWh"}
:::

Start with the hardware. A used RTX 4090 in May 2026 trades for $1,500–$2,450; the 5090 launch barely dented prices because the 4090's 24 GB of VRAM is still the cheapest way to put a 70B-class model in a single PCIe slot.[^13] Take the middle: $2,000. Straight-line amortize over a three-year service life and that is $1.83/day in pure capex — already the dominant line item before a single watt is drawn.

Electricity is the second line. A 4090 draws up to 450 W under load running Llama-2 70B Q2/Q4 at 15–18 tok/s,[^77] but a realistic always-on home rig spends most hours idle near 100 W and occasionally spikes to ~400 W during inference. Use a 20%/80% mix: `0.2 × 400 W + 0.8 × 100 W = 160 W avg`. At the US Feb 2026 residential average of 17.65¢/kWh,[^78] that's `0.160 kW × 24 h × $0.1765 = $0.68/day`. Total: $2.51/day, all-in, of which 73% is capex and 27% is power.

:::bars
- {label: "Capex amortization", value: "$1.83/day · 73%", pct: 73}
- {label: "Electricity at avg load", value: "$0.68/day · 27%", pct: 27}
:::

Now divide by the API floor. Claude Haiku 4.5 outputs cost $5/M tokens; Sonnet 4.6 is $15/M; DeepSeek V3.2 is $0.42/M.[^65] So to amortize the rig against Haiku, the break-even is `$2.51 ÷ $5/M = 502K output tokens/day`. At a sustained 50 tok/s of generation, that is about 40 minutes of pure output per day — well inside the envelope of a heavy Cursor user, a single agent loop, or one always-on Discord bot. Against DeepSeek V3 the math flips: `$2.51 ÷ $0.42/M = 5.98M tokens/day`, which at 50 tok/s requires ~33% of the day, every day, sustained — feasible only as a batched multi-user endpoint, not as a single-user chat companion.

The cleanest per-token comparison is electricity-only, ignoring capex. A 4090 at 400 W produces 0.4 kWh in one hour and ~180K tokens at 50 tok/s, so the marginal cost is `$0.1765 × 0.4 ÷ 0.180 ≈ $0.39/M tokens` of pure power.[^78] That's where the local rig sits on the price ladder:

:::compare
- {role: LOWEST, name: "DeepInfra Llama 70B", value: "$0.32/M"}
- {role: SUBJECT, name: "Self-hosted 4090 (Llama 70B, elec only)", value: "$0.39/M"}
- {role: HIGHEST, name: "Claude Opus 4.7", value: "$25/M"}
:::

Once you include the $1.83/day capex line, the true blended cost of a single-user 4090 climbs well above DeepInfra's metered rate at any realistic personal-utilization level. The "you're paying for the GPU whether or not you use it" problem is the entire bear case.

Geography moves the answer. In California (~33¢/kWh) the daily total climbs to about $3.10; in Hawaii at 43¢/kWh it's $3.49,[^78] which widens the Haiku break-even to 698K tokens/day and the DeepSeek break-even past 8M. Hot climates also pay an air-conditioning penalty of roughly +50% on the GPU's heat output, which is not included here.

The counterpoint is batched serving. Running four parallel users through llama.cpp on one 4090 drops per-user throughput from 28 to 18 tok/s but pushes aggregate throughput to 72 tok/s — a 2.6× multiplier on the same wattage.[^79] vLLM is even more aggressive: a single 4090 serves Llama 3.1 8B at 339.6 tok/s in FP16 and 579–599 tok/s under AWQ/GPTQ quantization.[^80] If you actually run an endpoint with four chat users plus a coding agent, the DeepSeek break-even collapses from "impossible" to "tight but plausible." Second counterpoint: reasoning models like DeepSeek R1 emit 3–10× more tokens per response than chat models, so the *effective* hosted cost of a reasoning workload is several multiples of the headline $/M figure — local serving claws back ground on any thinking-heavy use case.

Scaling up the rack scales up both sides. Sabareesh Sabu's 4×4090 prosumer build totals $12,000 plus a 30 A circuit upgrade ($500–$1,500) and two 1,500 W PSUs.[^81] That is ~$11/day in capex amortization alone — you now need ~2.2M Haiku-equivalent tokens/day just to break even, before you've paid the electrician. At the absurd top, tinybox green v2 with 4× RTX Pro 6000 Blackwells lists at $65,000 with 384 GB VRAM and dual 1,600 W PSUs;[^82] amortization is $59/day, so the break-even against Haiku is 12M tokens/day and against DeepSeek V3 is 141M tokens/day — startup territory, not personal compute.

Two non-financial constraints bind the math. Noise: an RTX 4090 Founders Edition runs at ~39 dBA under stress (bedroom-tolerable), while a DGX H100 emits 98.7 dB acoustic power at 80% fan — a difference of ~60 dB, or roughly a million-fold in acoustic power, the difference between "office corner" and "requires a closet with sound treatment." For a Mac mini M4 Pro four-node cluster at ~$5,000, daily cost works out to $5.11 ($4.57 capex + $0.54 electricity at 5 W idle / 140 W max), pushing the Haiku break-even past 1M tokens/day — Apple's silent, low-watt advantage is real but the capex premium swamps the power savings on any sub-year horizon.

The rule of thumb: ==local serving wins against Haiku- and Sonnet-class pricing, loses against DeepSeek-class pricing for any single-user workload, and only re-wins on DeepSeek-class pricing if you batch-serve multiple users==. Why this matters: the question "should I buy a 4090?" is no longer about whether self-hosting is *technically* viable — it's about whether your daily token throughput puts you above the 500K-token floor that justifies the capex.

## 07. The non-economic case

Even when the per-token spreadsheet says cloud wins, the structural reasons to run inference at home or inside a tenant boundary are hardening from preference into compliance — and the regulators, courts, and vendors themselves are doing most of the work.

The clearest signal is legal. In February 2026, Judge Jed Rakoff (SDNY) ruled that 31 documents created with a public generative-AI tool and forwarded to counsel were neither covered by attorney-client privilege nor work-product doctrine, on the grounds that public AI platforms' privacy policies leave users with no reasonable expectation of confidentiality.[^83] That single ruling moves the cost calculus for any law firm, in-house counsel, or accounting partner whose drafts touch an LLM: the question is no longer "is local cheaper?" but "what is the malpractice exposure of *not* keeping the prompt inside our perimeter?" It is, importantly, one district court — federal courts are still diverging on AI-and-privilege questions, and the ruling will be tested on appeal — but Rakoff is a senior judge and the reasoning is portable.[^83]

The regulatory drumbeat reinforces it. Italy's Garante fined OpenAI €15M in December 2024 for missing lawful basis, opaque training-data sourcing, weak age-gating, and an undisclosed March 2023 breach,[^84] then blocked DeepSeek from Italian Apple and Google stores in January 2025 citing GDPR Articles 6, 12, 13, 14, 27, 31, and 44.[^85] The EU AI Act's GPAI obligations took effect 2 August 2025 for models trained above 10²³ FLOPs — training-data summaries, copyright compliance attestations — with the systemic-risk tier above 10²⁵ FLOPs and the enforcement-and-fines window unlocking 2 August 2026.[^86] None of this directly bans hosted inference, but it raises the cost of *receiving* a frontier model into a regulated workflow without contractual carve-outs you can actually verify.

:::timeline
- {date: "2024-12", headline: "OpenAI fined €15M (Italy)", body: "Italian Garante cites missing lawful basis, opaque training data, weak age-gating, undisclosed March 2023 breach."}
- {date: "2025-01", headline: "Italy blocks DeepSeek", body: "Removed from Italian Apple and Google stores; GDPR Art 6, 13, 27, 44 cited."}
- {date: "2025-08", headline: "EU AI Act GPAI obligations in force", body: "Models >10²³ FLOPs sold into EU must publish training-data summaries; enforcement unlocks Aug 2026."}
- {date: "2025-08", headline: "Anthropic flips training default", body: "Consumer tiers opt-in to chat training by default; retention 30 days → 5 years unless users opt out by Sept 28."}
- {date: "2025-08", headline: "Claude Code weekly rate limits", body: "Power users hit caps; HN thread #11810 documents migration to local Qwen3-Coder via Ollama and vLLM."}
- {date: "2026-02", headline: "SDNY: public AI tools waive privilege", body: "Judge Rakoff rules 31 documents created with public AI tool and sent to counsel NOT protected."}
:::

The second axis is vendor trust decay. In August 2025 Anthropic flipped its consumer-tier default — Free, Pro, and Max — to train on user chats unless the customer explicitly opted out by 28 September 2025, and extended retention from 30 days to five years.[^87] The policy was lawful, well disclosed, and is — crucially — not how the commercial API or Enterprise tier work; those tenants are explicitly carved out. But it is the textbook case for the proposition that *defaults change*, and that an operating assumption baked into a 2024 procurement memo can quietly invert eighteen months later. If your threat model includes "the vendor flips the switch," local inference is the only deployment that is structurally immune.

:::callout(kind=warn, label=Privilege)
In February 2026 Judge Jed Rakoff (SDNY) ruled that 31 documents created with a public generative-AI tool and sent to counsel were *not* protected by attorney-client privilege or work-product doctrine — because "public AI platforms' privacy policies demonstrate users have no reasonable expectation of confidentiality." For any firm whose work product touches LLMs, this is the case that moved the cost of a private/local deployment from "IT preference" to "malpractice avoidance."[^83]
:::

The third is reliability under rate-limit. Anthropic imposed weekly caps on Claude Code on 28 August 2025; the 6 May 2026 doubling of the 5-hour limit left the weekly ceiling untouched, and GitHub issue #11810 has become a running ledger of power users routing boilerplate, refactors, and test-scaffolding to local Qwen3-Coder, Llama, and Kimi K2 via Ollama or vLLM — keeping Claude in reserve for the hard turns.[^88]

:::quote(attr="GitHub issue #11810 commenter, August 2025")
With open models like Qwen3, DeepSeek, LLaMA, and Kimi K2 you can avoid rate limit limitations by deploying these models using vLLM, Ollama … with no rate limits and no API surprises.[^88]
:::

The use cases bear out across regulated industries. A NEJM AI study in March 2025 demonstrated that a local Llama-3 70B instance running inside the "LLM-Anonymizer" pipeline removed ==unverified: 99.24% of PII from 250 German clinical letters== (paywalled DOI; figures reported in the journal abstract) — a number that is only meaningful if the model never leaves the hospital network.[^89] NHS England's January 2026 guidance on ambient-scribing products explicitly ties deployment to MHRA and CQC sign-off, raising the bar for any vendor whose data path crosses a public API.[^90] On the defense side, Rancher Government Solutions reports that 80–90% of its DoD customers run air-gapped; IBM launched a Granite-based defense LLM in October 2025 marketed as "deployable in air-gapped, classified, edge" environments; Los Alamos moved its LLM stack on-prem in early 2025 to handle ITAR and UCNI data; and xAI has been onboarded at DoD IL5.[^91]

:::stats
- {label: "Local Llama-3 PII removal", value: "99.24%", note: "NEJM AI study, 250 clinical letters"}
- {label: "JPM LLM Suite onboarding", value: "200K users", note: "in 8 months, tenant-isolated"}
- {label: "OpenAI Italian fine", value: "€15M", note: "December 2024"}
- {label: "Italy DeepSeek block", value: "Jan 30 2025", note: "removed from app stores"}
:::

Here is the honest counterpoint, and it matters: the most-cited enterprise deployments are *not* full local. JPMorgan's LLM Suite wraps OpenAI and Anthropic inside a tightly controlled internal tenant and reached 200,000 employees in eight months — that is tenant isolation, not on-prem inference.[^92] Thomson Reuters' May 2026 expansion of CoCounsel with Claude via MCP is explicitly architected so "customer data is not used to train third-party models and is not shared beyond a customer's own environment," covering one million CoCounsel users across 107 countries — again, a contractual carve-out on a frontier provider, not a homelab.[^93] For most regulated buyers the answer in 2026 is "frontier model on a contractually isolated tenant," and the home rack is the long tail.

The vibes layer is real but politically loaded — the QuitGPT campaign in February 2026 collected 700,000-plus cancellation pledges (later cited at 2.5M), uninstalls spiked 295% above the daily average, and app downloads dropped 13%.[^94] That is a signal about consumer sentiment, not enterprise procurement, and it sits inside a broader cultural backlash that mixes privacy with unrelated grievances.

Why this matters: the cost-per-token chart is no longer the only chart. A regulated buyer in 2026 is solving a four-variable problem — price, privilege, sovereignty, and rate-limit resilience — and three of those four variables now point away from the public API regardless of what the price column says.

## 08. What could break this thesis

The home-rack thesis has five concrete failure modes, four of them already partially visible in mid-2026 — and the honest read is that the win condition narrows to a specific persona, not the median user.

:::callout(kind=warn, label="The 512 GB moment passed")
In early 2026 Apple quietly pulled the 256 GB and 512 GB SKUs from the Mac Studio M3 Ultra configurator and raised the 256 GB upgrade from $1,600 to $2,000.[^6] The only consumer box that could host a 4-bit DeepSeek-V3 671B on a desk is no longer for sale at the top end. Apple cited DRAM market conditions; the AI inference community read it as a structural signal — capacity-per-dollar may not improve linearly even as the silicon does, because hyperscaler HBM demand is eating the same wafer pool that feeds unified-memory Macs.
:::

The first counter to the home-rack pitch is the price floor on hosted open-weight inference. DeepInfra is already serving Llama 70B at $0.10/M input,[^63] DeepSeek's own API runs V3-class for $0.27/M input,[^64] and OpenRouter now lists Ring-2.6-1T at $0.075/M input — a sparse MoE whose architecture, not its hardware, sets the floor.[^74] The 400× spread between Ring-2.6 and Opus 4.7 Fast at $30/M isn't a hardware gap; it's a sparsity gap, which means cloud margins on open MoE could compress toward electricity-only economics ($0.05/M is the limit case).

:::compare
- {role: LOWEST, name: "Ring-2.6-1T (OpenRouter)", value: "$0.075/M in"}
- {role: HIGHEST, name: "Opus 4.7 Fast", value: "$30/M in"}
- {role: SUBJECT, name: "DeepInfra Llama 70B", value: "$0.10/M in"}
:::

The counter-counter is that hosted prices don't move monotonically: GPT-5.5 input is 8× GPT-5's price after nine months,[^66] and the direction of travel at the frontier is up, not down. But the home rack is competing with the open floor, not the frontier — and that floor is where the squeeze lives.

The second failure mode is memory ceilings on prosumer silicon. The M5 announced in October 2025 ships 153 GB/s of bandwidth per package, with an M5 Ultra Mac Studio expected H2 2026[^8] — but Apple has not committed to a >128 GB consumer SKU on M5, and the pulled 512 GB option on M3 Ultra is the precedent that matters. If the M5 Ultra ships at 256 GB max, the 671B-class open models become a server purchase, not a desk purchase.

The third failure mode is the prefill-compute deficit for the most-cited home workload: coding agents. As one practitioner put it bluntly: "K2.5 at long context will drop into the low teens on the cheap mac setup. With terribly slow prefill ... A mac setup is going to be compute bound."[^44] Bandwidth wins decode; compute loses prefill; a Cursor session reading a 200K-token repo every turn is mostly prefill. Worse, NVFP4 — Blackwell-only — cuts memory 3.5× vs FP16 with under 1% accuracy delta,[^95] which is great if you own a B200 and a forced-obsolescence vector if you own a 4090 or an H100.

The fourth failure mode is the open-vs-closed Elo gap, which is real and may not narrow. As of May 12, 2026, LMArena shows the closed frontier at 1505–1506 Elo and the open frontier at 1466–1467 — a ~39-point gap, roughly a 55% win rate for closed.[^29] DeepSeek V4-Pro trails on MMLU-Pro (87.5 vs 91.0), GPQA-Diamond (90.1 vs 94.3), and Opus 4.6 on HLE (37.7 vs 40.0).[^32] Zuckerberg signaled in July 2025 that Meta's superintelligence-tier models may stay closed,[^30] and Meta's Llama 4 Maverick benchmark scandal — submitting a 1417 Elo variant while shipping a 1273 Elo variant[^28] — undermines confidence that open Elo numbers translate to shipping quality. If Western labs go fully closed and Chinese open weights face export-control friction, the gap could widen, not narrow.

The fifth failure mode is operational labor — the cost TCO sheets never capture. A DIY 4×4090 build runs $12K and requires a dedicated 30 A circuit;[^81] a DGX Spark shipped five months late at $3,999 and was hiked to $4,699 four months after launch;[^96] a DGX H100 produces 98.7 dB of acoustic power, which is unlivable in any room you'd sleep or take meetings in.[^97] And cloud providers batch your traffic across thousands of unseen users, multiplying throughput-per-GPU in ways a single-tenant home box structurally can't match.[^79]

:::rank-list
- {label: "Cloud price floor compression to ~$0.05/M for open MoE", value: "severe", pct: 100, highlight: true}
- {label: "Apple memory ceilings (512 GB pulled, no >128 GB M5 yet)", value: "severe", pct: 85}
- {label: "Prefill deficit for coding agents (30× FLOPS gap, KV cache pressure)", value: "high", pct: 75}
- {label: "Open-vs-closed Elo gap as Western labs pull back open weights", value: "moderate", pct: 60}
- {label: "Operational labor (drivers, ROCm regressions, model swaps, electrical work)", value: "moderate", pct: 50}
:::

Four of these five are already happening in mid-2026 — Apple has pulled the SKU, prices have collapsed, the prefill gap is measured, and the Elo gap is stable. The fifth is a permanent tax. So the honest read: the home rack works, it can host the open frontier on a desk, and for a specific persona it wins on every axis that matters. That persona is the user with privacy-driven workloads, batched throughput across 5+ concurrent users or agents, the technical taste to debug Vulkan and Metal and ROCm in the same week, regulatory exposure that makes some prompts literally illegal to send to a US API, or all-of-the-above. For the casual chat user, the single-stream Cursor user, or the company without an IT department, the cloud will keep winning.

Why this matters: the answer flips if any of four watches fires in late 2026 or 2027 — an M5 Ultra Mac Studio shipping with 256+ GB and Neural Accelerators; an AMD Strix Halo successor with HBM-class bandwidth on a consumer board; the open-vs-closed gap widening past 70 Elo; or a regulatory event (EU AI Act enforcement, a US export-rule inversion, a sectoral data-residency mandate) that makes specific workloads non-routable to public APIs. Until then, the home rack is a real choice with real downside — buy with eyes open.

:::references
- {id: 1, title: "NVIDIA RTX PRO 6000 Blackwell Server Edition", url: "https://www.nvidia.com/en-us/data-center/rtx-pro-6000-blackwell-server-edition/", source: "NVIDIA"}
- {id: 2, title: "Mac mini (2024) tech specs", url: "https://support.apple.com/en-us/121555", source: "Apple"}
- {id: 3, title: "Mac mini — power and thermal output", url: "https://support.apple.com/en-us/103253", source: "Apple"}
- {id: 4, title: "NVIDIA DGX Spark product page", url: "https://www.nvidia.com/en-us/products/workstations/dgx-spark/", source: "NVIDIA"}
- {id: 5, title: "Mac Studio (2025) tech specs", url: "https://support.apple.com/en-us/122211", source: "Apple"}
- {id: 6, title: "Apple pulls $4,000 512GB Mac Studio upgrade", url: "https://www.tomshardware.com/tech-industry/apple-pulls-512-mac-studio-upgrade-option", source: "Tom's Hardware", date: "2026-05-05"}
- {id: 7, title: "Apple introduces M4 Pro and M4 Max", url: "https://www.apple.com/newsroom/2024/10/apple-introduces-m4-pro-and-m4-max/", source: "Apple Newsroom", date: "2024-10-30"}
- {id: 8, title: "Apple unleashes M5, the next big leap in AI performance", url: "https://www.apple.com/newsroom/2025/10/apple-unleashes-m5-the-next-big-leap-in-ai-performance-for-apple-silicon/", source: "Apple Newsroom", date: "2025-10-15"}
- {id: 9, title: "NVIDIA puts Grace Blackwell on every desk", url: "https://nvidianews.nvidia.com/news/nvidia-puts-grace-blackwell-on-every-desk-and-at-every-ai-developers-fingertips", source: "NVIDIA Newsroom", date: "2025-01-06"}
- {id: 10, title: "AMD Ryzen AI Max+ 395 — breakthrough AI", url: "https://www.amd.com/en/blogs/2025/amd-ryzen-ai-max-395-processor-breakthrough-ai-.html", source: "AMD", date: "2025-01-06"}
- {id: 11, title: "Strix Halo LLM optimization", url: "https://www.hardware-corner.net/strix-halo-llm-optimization/", source: "Hardware Corner", date: "2026-01-15"}
- {id: 12, title: "Framework's first desktop PC", url: "https://techcrunch.com/2025/02/26/frameworks-first-desktop-pc-is-ready-for-gaming-and-local-ai-inference/", source: "TechCrunch", date: "2025-02-26"}
- {id: 13, title: "RTX 4090 price history and specs", url: "https://bestvaluegpu.com/history/new-and-used-rtx-4090-price-history-and-specs/", source: "BestValueGPU"}
- {id: 14, title: "RTX 5090 price tracker (May 2026)", url: "https://gpupoet.com/gpu/learn/price/may-2026/nvidia-geforce-rtx-5090", source: "GPU Poet", date: "2026-05-01"}
- {id: 15, title: "RTX 3090 price history and specs", url: "https://bestvaluegpu.com/history/new-and-used-rtx-3090-price-history-and-specs/", source: "BestValueGPU", date: "2026-05-01"}
- {id: 16, title: "RTX PRO 6000 Blackwell pricing", url: "https://www.thundercompute.com/blog/nvidia-rtx-pro-6000-pricing", source: "Thundercompute", date: "2026-05-01"}
- {id: 17, title: "NVIDIA A100 PCIe 80GB listings", url: "https://gpupoet.com/gpu/shop/nvidia-a100-pcie", source: "GPU Poet", date: "2026-04-01"}
- {id: 18, title: "H100 GPU price in 2026", url: "https://compute.exchange/blogs/h100-gpu-price-2026", source: "Compute Exchange", date: "2026-03-01"}
- {id: 19, title: "Mac Studio (2025) power and thermal output", url: "https://support.apple.com/en-us/102027", source: "Apple"}
- {id: 20, title: "NVIDIA H100 product page", url: "https://www.nvidia.com/en-us/data-center/h100/", source: "NVIDIA"}
- {id: 21, title: "AAPL & NVDA monthly close data", url: "https://finance.yahoo.com/quote/AAPL/history", source: "Yahoo Finance (via scripts/stock_prices.py)"}
- {id: 22, title: "Llama 3.3 70B Instruct model card", url: "https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct", source: "Hugging Face", date: "2024-12-06"}
- {id: 23, title: "DeepSeek-V3 model card", url: "https://huggingface.co/deepseek-ai/DeepSeek-V3", source: "Hugging Face", date: "2024-12-27"}
- {id: 24, title: "DeepSeek-R1 release news", url: "https://api-docs.deepseek.com/news/news250120", source: "DeepSeek", date: "2025-01-20"}
- {id: 25, title: "Qwen2.5 LLM release", url: "https://qwenlm.github.io/blog/qwen2.5-llm/", source: "Alibaba", date: "2024-09-19"}
- {id: 26, title: "Qwen3 release", url: "https://qwenlm.github.io/blog/qwen3/", source: "Alibaba", date: "2025-04-29"}
- {id: 27, title: "Llama 4 models page", url: "https://www.llama.com/models/llama-4/", source: "Meta", date: "2025-04-05"}
- {id: 28, title: "Meta Llama 4 LMArena cheating", url: "https://www.theregister.com/2025/04/08/meta_llama4_cheating/", source: "The Register", date: "2025-04-08"}
- {id: 29, title: "Chatbot Arena leaderboard", url: "https://openlm.ai/chatbot-arena/", source: "OpenLM (LMArena mirror)", date: "2026-05-12"}
- {id: 30, title: "Zuckerberg says Meta likely won't open source all superintelligence models", url: "https://techcrunch.com/2025/07/30/zuckerberg-says-meta-likely-wont-open-source-all-of-its-superintelligence-ai-models/", source: "TechCrunch", date: "2025-07-30"}
- {id: 31, title: "DeepSeek V4 LLM preview", url: "https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html", source: "CNBC", date: "2026-04-24"}
- {id: 32, title: "DeepSeek V4 release specs and benchmarks 2026", url: "https://www.nxcode.io/resources/news/deepseek-v4-release-specs-benchmarks-2026", source: "NXcode", date: "2026-04-24"}
- {id: 33, title: "Mistral Large 2", url: "https://mistral.ai/news/mistral-large-2407", source: "Mistral", date: "2024-07-24"}
- {id: 34, title: "DeepSeek-V4-Pro discount extension", url: "https://x.com/deepseek_ai", source: "@deepseek_ai (X)", date: "2026-04-29"}
- {id: 35, title: "Quantization explained: Q4_K_M vs AWQ vs FP16", url: "https://www.sitepoint.com/quantization-explained-q4km-vs-awq-vs-fp16-for-local-llms/", source: "SitePoint", date: "2025-09-15"}
- {id: 36, title: "Apple M3 Ultra GPU 80 cores", url: "https://www.waredb.com/processor/apple-m3-ultra-gpu-80-cores", source: "WareDB", date: "2025-03-07"}
- {id: 37, title: "Apple M5 Max vs NVIDIA AI deep dive", url: "https://skorppio.com/blog/apple-m5-max-vs-nvidia-ai-deep-dive", source: "Skorppio", date: "2025-11-15"}
- {id: 38, title: "GPU Benchmarks on LLM Inference", url: "https://github.com/XiongjieDai/GPU-Benchmarks-on-LLM-Inference", source: "GitHub (XiongjieDai)"}
- {id: 39, title: "llama.cpp Apple Silicon benchmarks", url: "https://github.com/ggml-org/llama.cpp/discussions/4167", source: "GitHub (llama.cpp)"}
- {id: 40, title: "Ivan Fioravanti — DeepSeek V4 Flash on M3 Ultra", url: "https://x.com/ivanfioravanti/status/2048709786141647283", source: "@ivanfioravanti (X)", date: "2026-04-27"}
- {id: 41, title: "M3 Ultra running DeepSeek V3", url: "https://www.hardware-corner.net/studio-m3-ultra-running-deepseek-v3/", source: "Hardware Corner", date: "2025-04-08"}
- {id: 42, title: "KV cache memory calculation for LLMs", url: "https://lyceum.technology/magazine/kv-cache-memory-calculation-llm/", source: "Lyceum", date: "2025-11-04"}
- {id: 43, title: "Ivan Fioravanti — GLM 4.6 5-bit on M3 Ultra", url: "https://x.com/ivanfioravanti/status/1973105854305149091", source: "@ivanfioravanti (X)", date: "2025-09-30"}
- {id: 44, title: "@sdmat123 on Mac coding agents", url: "https://x.com/sdmat123/status/2037307220539679120", source: "@sdmat123 (X)", date: "2026-03-26"}
- {id: 45, title: "NVIDIA DGX Spark in-depth review", url: "https://www.lmsys.org/blog/2025-10-13-nvidia-dgx-spark/", source: "LMSYS", date: "2025-10-13"}
- {id: 46, title: "iPad Pro M5 neural benchmarks (MLX)", url: "https://www.macstories.net/stories/ipad-pro-m5-neural-benchmarks-mlx/", source: "MacStories", date: "2025-10-28"}
- {id: 47, title: "@Topaz750 — M5 Max prompt processing", url: "https://x.com/Topaz750/status/2031881149182550398", source: "@Topaz750 (X)", date: "2026-03-11"}
- {id: 48, title: "MLX prefix cache discussion", url: "https://github.com/ml-explore/mlx/discussions/3203", source: "GitHub (MLX)", date: "2026-02-10"}
- {id: 49, title: "Alex Cheema — cost-per-GB", url: "https://x.com/alexocheema/status/1883764144625664392", source: "@alexocheema (X)", date: "2025-01-27"}
- {id: 50, title: "23× Mac mini cluster runs Llama-3-405B", url: "https://x.com/ac_crypto/status/1815628236522770937", source: "@ac_crypto (X)", date: "2024-07-23"}
- {id: 51, title: "Cheema — 4× M4 Pro Mac mini cluster", url: "https://x.com/alexocheema/status/1855238474917441972", source: "@alexocheema (X)", date: "2024-11-09"}
- {id: 52, title: "Exo — DeepSeek V3 on 8× M4 Pro minis", url: "https://x.com/exolabs/status/1872446290917347799", source: "@exolabs (X)", date: "2024-12-27"}
- {id: 53, title: "Apple Thunderbolt 5 AI supercomputer", url: "https://medium.com/@cdcore/apple-just-turned-your-thunderbolt-5-mac-into-an-ai-supercomputer-and-heres-how-they-did-it-346619b411ae", source: "Medium / cdcore"}
- {id: 54, title: "1.5 TB VRAM on Mac Studio: RDMA over TB5", url: "https://www.jeffgeerling.com/blog/2025/15-tb-vram-on-mac-studio-rdma-over-thunderbolt-5/", source: "Jeff Geerling", date: "2025-12-18"}
- {id: 55, title: "Cheema — M5 Max MacBook cluster $20K", url: "https://x.com/alexocheema/status/2054598636588122184", source: "@alexocheema (X)", date: "2026-05-13"}
- {id: 56, title: "Cheema — M5 Max vs M3 Ultra benchmark", url: "https://x.com/alexocheema/status/2055018796759277922", source: "@alexocheema (X)", date: "2026-05-14"}
- {id: 57, title: "Run a trillion-parameter LLM locally (AMD)", url: "https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-run-a-one-trillion-parameter-llm-locally-an-amd.html", source: "AMD Developer", date: "2026-04"}
- {id: 58, title: "Awni Hannun — Kimi K2.5 on 2× M3 Ultras", url: "https://x.com/awnihannun/status/2016221496084205965", source: "@awnihannun (X)", date: "2026-01-27"}
- {id: 59, title: "exo-explore/exo repository", url: "https://github.com/exo-explore/exo", source: "GitHub"}
- {id: 60, title: "bigscience-workshop/petals repository", url: "https://github.com/bigscience-workshop/petals", source: "GitHub"}
- {id: 61, title: "@ruider92545 — 6-node M1 Studio Max cluster", url: "https://x.com/ruider92545/status/1910519854262943918", source: "@ruider92545 (X)", date: "2026-04-10"}
- {id: 62, title: "Nemotron 70B on four Mac minis M4 Pro", url: "https://www.heise.de/en/news/Local-AI-Nemotron-70B-on-four-Mac-minis-M4-Pro-with-Thunderbolt-5-interconnect-10015283.html", source: "Heise", date: "2024-11-11"}
- {id: 63, title: "DeepInfra pricing", url: "https://deepinfra.com/pricing", source: "DeepInfra"}
- {id: 64, title: "DeepSeek API pricing (USD)", url: "https://api-docs.deepseek.com/quick_start/pricing-details-usd", source: "DeepSeek"}
- {id: 65, title: "Anthropic Claude pricing", url: "https://platform.claude.com/docs/en/docs/about-claude/pricing", source: "Anthropic"}
- {id: 66, title: "OpenAI API pricing", url: "https://developers.openai.com/api/docs/pricing", source: "OpenAI"}
- {id: 67, title: "Together AI pricing", url: "https://www.together.ai/pricing", source: "Together AI"}
- {id: 68, title: "Groq pricing", url: "https://groq.com/pricing", source: "Groq"}
- {id: 69, title: "SambaNova Cloud pricing", url: "https://cloud.sambanova.ai/pricing", source: "SambaNova"}
- {id: 70, title: "Cerebras API access speed tests 2026", url: "https://tokenmix.ai/blog/cerebras-api-key-access-speed-tests-2026", source: "TokenMix"}
- {id: 71, title: "Cerebras Llama 405B inference", url: "https://www.cerebras.ai/blog/llama-405b-inference", source: "Cerebras"}
- {id: 72, title: "Together AI pricing (DeepSeek R1)", url: "https://www.aipricing.guru/together-pricing/", source: "AI Pricing Guru"}
- {id: 73, title: "Meta / Llama hosted pricing history", url: "https://www.aipricing.guru/meta-pricing/", source: "AI Pricing Guru"}
- {id: 74, title: "OpenRouter models pricing", url: "https://openrouter.ai/models", source: "OpenRouter"}
- {id: 75, title: "Groq API pricing & batch tier", url: "https://tokenmix.ai/blog/groq-api-pricing", source: "TokenMix"}
- {id: 76, title: "Google AI / Gemini pricing", url: "https://ai.google.dev/pricing", source: "Google"}
- {id: 77, title: "RTX 4090 LLM inference benchmarks", url: "https://blog.easecloud.io/ai-cloud/gpu-for-your-llm-deployment/", source: "EaseCloud"}
- {id: 78, title: "EIA Electric Power Monthly Table 5.6.A", url: "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a", source: "U.S. EIA"}
- {id: 79, title: "Boosting llama-server performance with batch settings", url: "https://promptsicle.com/tips/boosting-llama-server-performance-with-batch-settings/", source: "Promptsicle"}
- {id: 80, title: "vLLM GPU benchmark on RTX 4090", url: "https://www.databasemart.com/blog/vllm-gpu-benchmark-rtx4090", source: "Databasemart"}
- {id: 81, title: "Building a 4× RTX 4090 LLM rig", url: "https://sabareesh.com/posts/llm-rig/", source: "Sabareesh Sabu"}
- {id: 82, title: "tinybox green v2 with 4× RTX Pro 6000 Blackwell", url: "https://tinycorp.myshopify.com/products/tinybox-green-v2-with-4x-rtx-pro-6000-blackwell", source: "tiny corp"}
- {id: 83, title: "SDNY: AI-generated documents not protected by privilege", url: "https://www.debevoisedatablog.com/2026/02/11/district-court-rules-ai-generated-documents-are-not-protected-by-privilege/", source: "Debevoise", date: "2026-02-11"}
- {id: 84, title: "Italy's privacy watchdog fines OpenAI €15M", url: "https://www.euronews.com/next/2024/12/20/italys-privacy-watchdog-fines-openai-15-million-after-probe-into-chatgpt-data-collection", source: "Euronews", date: "2024-12-20"}
- {id: 85, title: "Italy blocks Chinese AI tool DeepSeek", url: "https://therecord.media/italy-blocks-chinese-ai-tool-deepseek-over-privacy-concerns", source: "The Record", date: "2025-01-31"}
- {id: 86, title: "EU Commission — GPAI guidelines", url: "https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers", source: "European Commission", date: "2025-08-02"}
- {id: 87, title: "Anthropic users face a new choice: opt-out or share data", url: "https://techcrunch.com/2025/08/28/anthropic-users-face-a-new-choice-opt-out-or-share-your-data-for-ai-training/", source: "TechCrunch", date: "2025-08-28"}
- {id: 88, title: "Claude Code weekly rate-limit issue #11810", url: "https://github.com/anthropics/claude-code/issues/11810", source: "GitHub"}
- {id: 89, title: "LLM-Anonymizer with local Llama-3 70B", url: "https://ai.nejm.org/doi/full/10.1056/AIdbp2400537", source: "NEJM AI", date: "2025-03-25"}
- {id: 90, title: "NHS England — AI ambient-scribing guidance", url: "https://www.england.nhs.uk/long-read/guidance-on-the-use-of-ai-enabled-ambient-scribing-products-in-health-and-care-settings/", source: "NHS England", date: "2026-01-01"}
- {id: 91, title: "IBM Granite defense LLM", url: "https://defensescoop.com/2025/10/29/ibm-new-large-language-model-defense-applications-janes/", source: "DefenseScoop", date: "2025-10-29"}
- {id: 92, title: "JPMorgan Chase's LLM Suite", url: "https://thedigitalbanker.com/jpmorgan-chases-llm-suite-drives-ai-transformation-across-the-enterprise/", source: "The Digital Banker", date: "2025-09-01"}
- {id: 93, title: "Thomson Reuters + Anthropic CoCounsel", url: "https://www.prnewswire.com/news-releases/thomson-reuters-and-anthropic-expand-partnership-to-connect-claude-with-cocounsel-legal-302769890.html", source: "PRNewswire", date: "2026-05-12"}
- {id: 94, title: "QuitGPT campaign urges ChatGPT cancellations", url: "https://www.technologyreview.com/2026/02/10/1132577/a-quitgpt-campaign-is-urging-people-to-cancel-chatgpt-subscriptions/", source: "MIT Technology Review", date: "2026-02-10"}
- {id: 95, title: "Introducing NVFP4 for efficient low-precision inference", url: "https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/", source: "NVIDIA Developer", date: "2025-06-24"}
- {id: 96, title: "NVIDIA starts selling its $3,999 DGX Spark", url: "https://www.engadget.com/ai/nvidia-starts-selling-its-3999-dgx-spark-ai-developer-pc-120034479.html", source: "Engadget", date: "2025-10-15"}
- {id: 97, title: "DGX SuperPOD H100 sound mitigation", url: "https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/sound.html", source: "NVIDIA Docs"}
:::
