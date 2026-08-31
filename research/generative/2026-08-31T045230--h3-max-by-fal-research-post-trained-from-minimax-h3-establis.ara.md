---
eyebrow: REPORT · GENERATIVE VIDEO
domain: software
title: "H3 Max: fal's fastest video model, and the moat that isn't the model"
deck: fal post-trained MiniMax's open weights into the fastest video endpoint on the market. A free distillation of the same weights had already shipped three weeks earlier.
lede: |
  On 27 August 2026 fal announced H3 Max, a post-trained version of MiniMax's
  open-weight H3 video model that renders a five-second 768p clip with
  synchronised audio in roughly three seconds — faster than the clip plays.
  The engineering is real and the endpoint works. But the three claims wrapped
  around it deserve separate treatment: the speed number is mostly fal's serving
  stack rather than its post-training, the "#1" is board-specific and was inside
  the noise floor on launch day, and the one asset in this story that a community
  distiller genuinely cannot copy is not a CUDA kernel. It is a licence that
  excludes the United States.
stats:
  - {label: 5s clip at 768p, value: "~3", unit: "sec", note: vendor-reported}
  - {label: List price, value: "$0.08", note: per second of video}
  - {label: Attributable to post-training, value: "~2.3x", note: of a headline 35x}
  - {label: Open weights to free 4-step distill, value: "8", unit: days}
  - {label: Territories excluded by the base licence, value: "4", note: "EU, UK, Korea, US"}
---

If you only need the answer, it is this.

:::kv
- {term: "Who built it", def: "fal Research post-trained MiniMax's open-weight H3. Uncontested — even MiniMax's own docs say so. But MiniMax calls it \"jointly released\" and sells it directly as MiniMax-H3-Max, so it is not fal-exclusive."}
- {term: "Is it really 50x faster", def: "No single number is. fal publishes 35x (throughput), 15x (latency vs peers) and quotes a third-party 50x. The third-party figure now measures 39.6x, and is not resolution-normalised."}
- {term: "What the post-training bought", def: "Roughly 2.3x on fal's own numbers — fal says base H3 on its stack is already ~15x MiniMax's inference, against 35x for H3 Max. Most of the headline speedup looks like the serving stack, not the model, though the baseline identity is contested."}
- {term: "Is the #1 real", def: "On one board, at today's sample size, marginally (p≈0.019). At the sample fal cited on launch day it was p≈0.085 — not separated from second place. On text-to-video it is third."}
- {term: "Moat or copyable", def: "The optimisation layer is demonstrably copyable: a free 4-step distill preceded H3 Max by weeks, and an open-weights one landed the same day. The durable asset is hardware access and a legal position."}
:::

:::note
Every leaderboard standing, price and latency figure in this article is a
point-in-time reading as of 31 August 2026. Preference boards recompute
hourly and vendor rate cards change monthly; figures are dated in place
throughout.
:::

## 01. What shipped, and who actually built it

On 2026-08-27 fal announced H3 Max as "a post-trained version of MiniMax H3 developed by fal Research and optimized for maximum speed by fal's inference team."[^1] That sentence is the whole dispute in miniature, because it is not quite the sentence MiniMax uses — and the gap between the two determines who owns whatever advantage H3 Max represents.

Start with what was actually on the table to post-train. MiniMax open-weighted the base model on 2026-08-03 as the HuggingFace repo `MiniMaxAI/MiniMax-H3`.[^6,7] The core is a 33B-parameter dense single-stream transformer — the "H3-Omni-Transformer" — with roughly 13B of those parameters sitting in AdaLN-related branches; the text conditioner is a separate full Qwen3-VL-32B whose 50th-layer hidden states are consumed, so anyone deploying it carries about 65B parameters, not 33B.[^7] Natively it produces 4–15s clips at 24 FPS, 768px short side, with jointly denoised 32 kHz stereo audio in the same pass.[^7]

What was *not* released matters more. Two base checkpoints shipped (FL2VA and Ref2VA); the H3-Context-IR orchestration module, the H3-Regenerate-2K upscaler, and the sparse-attention implementation were all withheld — MiniMax's stated reason for the upscaler being "Due to the complexity of the system, this module is not yet open-sourced. We will release it once it is ready."[^6,7] Independent commentary called the release "only minimally open," which is fair.[^46] The operative consequence: {accent}768px is the hard ceiling for anything post-trained from the open weights{/}, because 2K is a separate regeneration stage MiniMax kept.[^7]

:::timeline
- {date: 2026-07-31, headline: "MiniMax H3 ships as a hosted API", body: "fal is a Day 0 ecosystem partner hosting the H3 API from launch — its involvement predates the open weights."}
- {date: 2026-08-02, headline: "MiniMax H3 Community License takes effect", body: "The terms governing every downstream post-train, including this one."}
- {date: 2026-08-03, headline: "Base H3 open-weighted on HuggingFace", body: "Two checkpoints, 768p base only; the 2K regeneration stage, Context-IR, and sparse attention are withheld."}
- {date: 2026-08-26, headline: "H3 Max appears on both storefronts", body: "fal lists H3 Max; MiniMax lists model ID MiniMax-H3-Max at matching prices."}
- {date: 2026-08-27, headline: "fal publishes the H3 Max launch blog", body: "Framed as post-trained by fal Research, optimized by fal's inference team."}
:::

fal's landing page is blunter still: "H3 Max is post-trained by fal on top of the open-weight base MiniMax H3 model."[^2] No co-development credit. Yet fal was a Day 0 ecosystem partner hosting MiniMax's H3 API from its 2026-07-31 launch, so the relationship predates the weights being public at all.[^5,45] And MiniMax, quoted inside fal's own post, says "We've worked closely with fal since day one."[^1] MiniMax's API documentation goes further and calls H3 Max "jointly released by MiniMax and fal.ai" — while still conceding it is "a video generation model post-trained by fal.ai on MiniMax H3."[^10]

A widely repeated claim — that MiniMax never announced a model by this name and that H3 Max is fal-exclusive — is simply false against MiniMax's own docs, where `MiniMax-H3-Max` is a first-class servable model ID.[^10,11] The honest reading: {mark}training is uncontested (fal did it, and MiniMax's own documentation says so); distribution is genuinely joint{/}. The MiniMax-branded name flatters MiniMax and lends fal the base model's credibility. Both parties get paid.

Nor is H3 Max a superset. MiniMax's docs put the trade in the open:

| Model | Resolution | Duration | Modes |
|---|---|---|---|
| MiniMax-H3 | 768P / 2K | 4–15s | Text-to-video, image-to-video, Reference Generation |
| *MiniMax-H3-Max | 480P / 768P | 5–15s | Text-to-video, image-to-video only; reference generation not yet available |

It buys speed by giving up 2K and reference-to-video.[^10] And there is no technical report, paper, or model card for H3 Max, and no released checkpoint — it exists as a hosted endpoint plus marketing pages, while base H3 has only a model card.[^1,7]

That absence is why attribution is load-bearing here: every speed, price, and ranking claim in the sections that follow is a claim about a black box neither party has documented, sold by two vendors who describe its parentage differently.

## 02. Three speed numbers, three different baselines

Start with the only absolute figure fal publishes. The blog says H3 Max "generates a 5-second video in approximately 3 seconds."[^1] The landing page words it as "under 3 seconds, which is faster than real time," and separately reports backend denoising (`timings.inference`) at "roughly 2.5 seconds for a 5-second 768p generation."[^2] Approximately-three versus under-three, wall clock versus denoise: the two surfaces already disagree by roughly a fifth of the quantity being measured.

Around that anchor sit three multipliers. Each is individually defensible. None of them measures the same thing as the others.

| Multiplier | What it measures | Against what baseline | Measured by |
|---|---|---|---|
| ~35x | Throughput | "the official MiniMax H3 endpoint" | fal[^1,2] |
| ~15x | Latency | "models of comparable quality" | fal, with quality set by fal's own internal study — only 6 of 12 tested models were named[^2,52] |
| *>50x | Speed at matched quality | MiniMax H3 | Design Arena, quoted inside fal's blog[^1] |

The decomposition is where the marketing thins out. fal's own FAQ, answering how H3 Max differs from standard H3, says of the base model that "on fal's stack it runs about 15x faster than MiniMax's own inference."[^2] If fal-hosted *base* H3 is already ~15x, and H3 Max is ~35x, then everything the post-training and the Max-specific work contributed is roughly 2.3x. The large number is mostly fal's serving stack, applied to weights anyone can download.

That 2.3x is an illustrative upper bound, not a derived fact, and it should be read as one. The 35x is a throughput ratio; the 15x figures are latency claims, and under batching the two are not interchangeable — a stack can multiply throughput without moving per-request latency at all. The baselines are also worded differently ("the official MiniMax H3 endpoint" versus "MiniMax's own inference"), and neither carries a resolution, duration, batch, or concurrency qualifier.[^1,2] The arithmetic holds only if you assume those two baselines are the same thing measured the same way.

There is a specific way this could be wrong, and it deserves naming rather than burying. At least one independent reading of the launch takes the 35x baseline to be fal's *own* hosted endpoint rather than MiniMax's: "the baseline is fal's own hosted endpoint; fal controls both sides of the measurement."[^52] If that reading is right, the 35x is already measured against the very fal-hosted base H3 that the FAQ calls 15x, the division is invalid, and the residual attributable to post-training would be the full 35x rather than 2.3x — the opposite conclusion. Against that reading, both of fal's own surfaces say "the official MiniMax H3 endpoint" verbatim, which is the more natural construction.[^1,2] But ==the decomposition is only as good as that baseline identity, and fal has never clarified it==.

There is also no published denominator. fal never states an absolute latency for the thing it is 35x faster than. The best available anchor is MiniMax's own self-host benchmark: a ~5-second 768p generation (1344x768, 124 frames, 50 steps) takes 75.10 seconds mean inference latency on 4xH200 — 84.14 seconds end to end — and 19.04 seconds on 8xB300.[^12] Measured against the 8xB300 number, a 3-second result is about 6x, not 35x.

Two normalizations are missing outright. fal serves on GB200 NVL72 while MiniMax's published reference configurations are H200/B300 class, so an unknown share of the 35x is simply newer silicon rather than software.[^1,12] And Design Arena times base MiniMax H3 at its 2K default against H3 Max at 768p[^16] — a resolution gap, not an efficiency gap, which fal's own page acknowledges when it says "For 2K output, use standard MiniMax H3 instead."[^2]

The third-party number has also drifted. On Design Arena's live image-to-video board, base MiniMax H3 is timed at 241.4 seconds and H3 Max at 6.1 seconds — a ratio of 39.6x, not "more than 50x" (as of 2026-08-31).[^16] One caveat on that reading: Design Arena renders its board client-side, so these are as-observed values on that date rather than figures reproducible from the page source. ==Treat the 39.6x as a dated observation, not a published statistic.==

:::compare
- {role: FASTEST, name: "fal H3 Max (vendor-reported)", value: "~3.0s"}
- {role: SLOWEST, name: "MiniMax H3, official endpoint (Design Arena timing)", value: "241.4s"}
- {role: SUBJECT, name: "FastH3, open weights, 4xB200", value: "6.1s"}
:::

Those three points span a 5-second 768p generation as of 2026-08-31. The instructive one is the third: FastH3, an open-weight 4-step distillation of the same base, lands a 5-second clip in 6.1 seconds on 4xB200.[^23] WaveSpeedAI, self-hosting the same open weights without a distillation, reports a median end-to-end generation around 82 seconds.[^50] The distance between 82 and 6.1 is engineering anyone can attempt.

The auditable gap is verification. Nobody outside fal and Design Arena has independently timed H3 Max,[^40] and Artificial Analysis does not latency-benchmark audio-enabled video models at all.[^15]

## 03. What actually changed: the model, and the serving stack

fal tells two stories with one voice: post-training for quality, inference co-design for speed. Both are plausible. Neither, as published, is falsifiable.

Take post-training first. The launch write-up's complete description of method is that fal "introduced substantial new data during post-training" with "a particular focus on prompt adherence and visual quality."[^1] That is the whole disclosure — and the word "reinforcement" appears in it exactly zero times.[^1] Move one URL sideways to the marketing landing page and the claim grows a limb: fal "spent a huge portion of our post-training compute on verifiable RL tasks."[^2] fal's official X account repeated that line on 2026-08-26.[^53] So the RL claim is genuinely first-party — it is just that it lives only in marketing copy and one post, never in the technical document, and is backed by no paper, technical report, or engineer thread.[^1,2,53] Which fal surface you cite changes what fal "said."

The evaluation protocol is disclosed at the same altitude. fal ran "head-to-head preference studies" across three separate dimensions — overall quality, prompt understanding, aesthetics — aggregated "using Bayesian Elo ratings with 95% confidence intervals," and reports that scoring the axes separately "gave us a much clearer signal than optimizing against a single aggregate score."[^1] That is a defensible methodology and a real design insight. It also ships with no rater count, no rater pool, no blinding protocol, no prompt set, and no per-model score.[^1] Confidence intervals over an unspecified population are decoration.

:::kv
- {term: "Post-training method", def: "Named only as \"substantial new data\" plus tuning for prompt adherence and visual quality."}
- {term: "Post-training data", def: "No provenance, scale, licensing, or composition published."}
- {term: "RL detail", def: "\"Verifiable RL tasks\" asserted on the landing page and X — no task list, reward model, or compute share."}
- {term: "Step count / distillation", def: "Not disclosed; the public API exposes no num_inference_steps knob."}
- {term: "Quantization / precision", def: "No scheme or format published; no guidance_scale knob either."}
- {term: "Serving hardware", def: "GB200 NVL72, stated explicitly. The clearest fact in the release."}
- {term: "GPUs per request", def: "Never stated by fal on any surface."}
- {term: "Evaluation protocol", def: "Three-axis preference study, Bayesian Elo, 95% CIs — no raters, prompts, or scores."}
:::

The speed story is thinner still. fal attributes it to "co-designing the inference engine with the post-training rather than dropping new weights into a generic serving path."[^2] Read that as an engineer: it names no kernel, no parallelism scheme, no scheduler. It is a process claim wearing a mechanism's clothes, and as stated nothing could contradict it. What *is* substantiated is the engine's existence — "fal's in-house inference engine, which our team has spent the past four years optimizing for diffusion models"[^2] — and independently, co-founders describing "a collection of kernels, parallelization utilities, diffusion caching methods, quantization, all that stuff combined into one package," with over a hundred custom kernels and a dedicated kernel team.[^19] The hardware claim is concrete too: H3 Max "was trained and served entirely on NVIDIA GB200 NVL72 systems," delivering "up to 2x the performance of the previous-generation accelerators"[^1] — though the baseline generation goes unnamed, and that is NVIDIA's marketing frame restated by a customer, not a fal measurement.

fal does name step distillation, precision reduction and approximation — but only to hold them at arm's length, as techniques that "produce impressive speedups while degrading the output."[^1] Do not over-read that. It is positioning, not a denial, and it is fully compatible with having distilled steps. The absence of any step count, distillation ratio or precision format[^1] and the absence of the corresponding API knobs[^3] are evidence of non-disclosure, not of non-use.

:::stats
- {label: "Custom CUDA kernels", value: "100+", note: "co-founder account"}
- {label: "Years optimizing the engine", value: "4"}
- {label: "Ulysses end-to-end gain", value: "3-5%", note: "single 8xB200 node"}
- {label: "'Reinforcement' in the launch blog", value: "0", note: "mentions"}
:::

Which brings us to the most technical-sounding sentence in circulation — and it is not fal's. The line that H3 Max "runs on fal's multi-node inference engine, several machines working on one request together" appears on no fal surface: not the launch blog, not the landing page, not fal Serverless.[^1,2] It circulates instead through third-party aggregator and reseller pages, laundered into authority by search summarizers — and fal Serverless, fal's own description of its GPU platform, does not attach it to H3 Max either.[^47] fal's own published work on splitting one diffusion request across GPUs, "Ulysses Unbound," benchmarks a single 8xB200 node and reports chunk-latency gains of 23-25% collapsing to roughly 3-5% end-to-end.[^18] That is the opposite of a multi-node triumph.

Reason it through and the two facts reconcile without the invented claim. A GB200 NVL72 rack is a single 72-GPU NVLink domain.[^1] "Several machines" can be *physically* true — multiple compute trays — while being *architecturally* one interconnect fabric rather than a network cluster. That distinction is exactly what rescues all-to-all-heavy context parallelism from the cross-node collapse it suffers over Ethernet,[^18] and it is a more interesting story than the one the reseller made up. fal just never told it.

## 04. The rankings, audited

fal's launch page leads with a flat superlative: H3 Max is number one on independent benchmarks.[^2] The ordering is real, and it is corroborated on two boards that do not share a voter pool. It is also board-specific, resolution-mismatched, and — at the sample size fal cited on launch day — not statistically separated from second place. Here is the board the claim rests on, Artificial Analysis's image-to-video *with audio* arena as of 2026-08-31.[^13]

:::rank-list
- {label: "Minimax H3 Max (post-trained by fal)", value: "1,203", pct: 100, highlight: true}
- {label: "Dreamina Seedance 2.0 720p", value: "1,190", pct: 88}
- {label: "MiniMax H3 (Open Weights)", value: "1,185", pct: 84}
- {label: "Gemini Omni Flash", value: "1,179", pct: 79}
- {label: "grok-imagine-video-1.5", value: "1,108", pct: 16}
- {label: "HappyHorse-1.1", value: "1,104", pct: 12}
- {label: "MAGI-2 Preview", value: "1,099", pct: 8}
:::

Two structural facts before the arithmetic. The top four are one cluster and everything below is another: 1,203 / 1,190 / 1,185 / 1,179, then a 71-point cliff to 1,108.[^13] Whatever separates H3 Max from Seedance 2.0 is a hair; what separates either from seventh is a regime change. And H3 Max is rated on the thinnest evidence in that cluster — n=5,368 against Seedance's 17,383 and Gemini Omni Flash's 12,057.[^13]

Now the number fal actually shipped. On launch day it cited Elo 1,201 ±11 over 2,177 samples.[^2] That interval is [1,190, 1,212]; second place's is [1,184, 1,196] — they overlap by six points, and the claimed leader's *lower bound lands exactly on the runner-up's point estimate*.[^13] Treated as a two-sample test rather than two eyeballed error bars: Δ = 11, SE₁ = 11/1.96 = 5.61, SE₂ = 6/1.96 = 3.06, SE_diff = √(5.61² + 3.06²) = 6.39, z = 1.72, p ≈ 0.085. Not significant at α = 0.05. On launch day, "#1" was a photo finish.

Fairness demands the update: the lead has firmed. At today's larger sample, Δ = 13 with SE_diff = 5.52 gives z = 2.35, p ≈ 0.019 — that clears the conventional bar, and Artificial Analysis's own rank-range column now assigns H3 Max an unambiguous "1" where second place carries "2-3".[^13] But the marginal intervals still overlap by two points, this is a single unpreregistered pairwise comparison drawn from a 33-model board after seeing the ranking, with no multiplicity correction — and AA publishes no definition of how that rank range is computed, so it cannot be independently audited.[^15]

The blanket "#1" also rounds up across boards. On Artificial Analysis's *text*-to-video with-audio arena, H3 Max is third, inside a three-way statistical tie:

| Model | Elo | 95% CI |
|---|---|---|
| Wan 3.0 | 1,242 | ±9 |
| Gemini Omni Flash | 1,237 | ±6 |
| *Minimax H3 Max | 1,235 | ±10 |

Wan 3.0 versus H3 Max is Δ = 7, z ≈ 1.02, p ≈ 0.31 — no separation at all.[^14] On the text-to-video board *without* audio, H3 Max does not appear in the top five — though that may reflect too few silent-mode votes rather than a worse model.[^14]

Then the resolution mismatch. Artificial Analysis generates at "1080p (or closest supported value)" with otherwise identical settings.[^15] fal's H3 Max API accepts only 480P or 768P.[^3] H3 Max is therefore rated at 768p against rivals rendering at 1080p. This is a consistently applied rule, not a fal-specific exemption — but blind human raters can reward or penalise visible resolution, and AA does not disclose per-row generation resolution.[^15] AA's method is Bradley-Terry MLE on blind pairwise votes rescaled to an Elo-like range and recomputed hourly; it documents no confidence-interval method, does not state who may vote, and describes no de-duplication or brigading defence.[^15] One smaller discrepancy: fal says AA lists the model as "MiniMax H3 Turbo (768p)"; the live board carries no such row.[^2] Most likely a post-publication rename — a stale claim, not a fabrication.[^13]

Design Arena corroborates the ordering: H3 Max 1,349 over 3,574 image-to-video battles against base H3's 1,326.[^16] But fal cited the launch-day figures, 1,341 versus 1,333 — eight points.[^2] On a 400·log₁₀ scale, eight points implies a 51.15% head-to-head win rate, which needs roughly 7,250 *direct* pairings to exclude 50% at 95% confidence — about double the battles H3 Max had against the entire field.[^16] Design Arena lists a model after fifteen comparisons, weights every vote equally "with no filtering or editorial adjustment," is a 2025-founded, $7.9M-seed startup selling private evaluations to the labs it ranks, and promoted H3 Max on launch day.[^17] Its methodology page was not directly retrievable on re-check, so ==those terms are reported from a cached reading rather than confirmed live==. On its general Video board the ordering inverts outright: base H3 1,298 beats H3 Max 1,293, both behind Gemini Omni 1.1 Flash at 1,377.[^16]

Preference Elo is weak evidence at these margins by construction. Two *identical* Aya-Vision-8B checkpoints scored 17 Elo apart in Chatbot Arena — a gap the authors attribute to sampling variance and private best-of-N submission dynamics, and larger than H3 Max's text-to-video lead.[^33] In 3D Arena, identical models gained 78 Elo purely from rendering changes "that enhance immediate visual appeal" across 123,243 votes.[^34] That is precisely the failure mode for a model post-trained for aesthetics and then scored on aesthetics by fast pairwise voters. The defensible reading: H3 Max is at least as good as base H3 on preference. Its speed result is far more distinctive than its quality result.

## 05. The price inversion

Read fal's rate card as of 2026-08-31 and the arithmetic looks broken. H3 Max — the variant that turns a minute of 768p video around roughly 35x faster than base MiniMax H3 — lists at **$0.08 per second of generated video**, or $4.80 per minute. fal's own hosting of the *slower* base H3 lists at **$0.06 per second at the same 768p**, alongside $0.05 at 480p, $0.13 at 2K and $0.16 at 4K.[^2,4] The fast model carries a 33% premium over the slow one at identical resolution. At 480p the two are priced to the cent — $0.05 either way — so the inversion is resolution-specific, not a blanket markup.[^2,4]

The mechanism matters more than the anomaly. These endpoints bill **per second of generated video, not per second of compute**.[^2,4] A 35x throughput gain therefore lands entirely on the vendor's cost line and not at all on the customer's invoice. Speed and price are decoupled by the billing unit, which is exactly why an inversion is possible without anyone being irrational.

| Model · host (as of 2026-08-31) | 480p | 768p | 2K |
|---|---|---|---|
| MiniMax H3 base — on fal | $0.05 | $0.06 | $0.13 |
| MiniMax H3 base — MiniMax direct | — | $0.08 | $0.13 |
| *MiniMax H3 Max — on fal | $0.05 | $0.08 | — |
| MiniMax H3 Max — MiniMax direct | $0.05 | $0.08 | — |

MiniMax's own rate card prices `MiniMax-H3-Max` at $0.05/sec (480P) and $0.08/sec (768P) — an exact match to fal's post-promotion list — while pricing base `MiniMax-H3` at $0.08/sec (768P) and $0.13/sec (2K).[^11,2] So fal undercuts its partner by 25% on the base model it merely resells, and matches it to the cent on the model they launched together. fal priced *with* MiniMax where they co-sell and competed only where it was free to. One tell that the two lists are not the same product surface: fal advertises a 4K tier for base H3 that MiniMax does not list, and the open weights are 768p-native — that 4K is almost certainly an added upscale, not a model capability.[^4,11]

A 50%-off launch discount was live on 2026-08-31, putting H3 Max at $0.04/sec, but fal contradicts itself across three of its own pages on when it ends — "the first week," "the first 14 days," and a September 1 date on the API page — so no single expiry should be assumed.[^1,2,3] The consequence is downstream: Artificial Analysis's leaderboard carries H3 Max at $2.40/min, the promotional rate rather than the $4.80/min list, which temporarily flatters the #1 model's price-per-quality position.[^13,2]

Against the field, per second of generated video, as of 2026-08-31:

:::bars
- {label: "Veo 3.1 Lite (720p)", value: "$0.05", pct: 7}
- {label: "MiniMax H3 Max (768p, list)", value: "$0.08", pct: 11}
- {label: "Veo 3.1 Fast (720p)", value: "$0.10", pct: 14}
- {label: "Gemini Omni Flash (720p)", value: "$0.10", pct: 14}
- {label: "MiniMax H3 base (2K)", value: "$0.13", pct: 19}
- {label: "Kling 3.0 Pro (1080p)", value: "$0.336", pct: 48}
- {label: "Veo 3.1 Standard (720p)", value: "$0.40", pct: 57}
- {label: "Seedance 2.5 on fal (720p)", value: "$0.47", pct: 67}
- {label: "Sora 2 Pro (1080p)", value: "$0.70", pct: 100}
:::

Google's cheapest tier undercuts H3 Max outright at $0.05/sec with audio included by default; Veo 3.1 Fast and Sora 2 sit at $0.10/sec at 720p.[^31,32] Gemini Omni Flash is token-billed at $17.50 per 1M output video tokens against 5,792 tokens per second of 720p video, landing near $0.10/sec and independently corroborating the $6.00/min on the leaderboard.[^31,13] Kling 3.0 Pro at 1080p works out to roughly $0.336/sec from the $20.16/min rate carried on that same board.[^13] Seedance 2.5's ~$0.47/sec on fal is mostly resale spread — BytePlus direct is about half that.[^51]

The conclusion is that {accent}H3 Max is not a discount product{/}. It is mid-pack, undercut by Google's floor, and priced above its own slower sibling: it sells latency at a premium, not cost savings. The counterpoint is real, though — at $0.08/sec it is still the cheapest of the top four on the with-audio board, and OpenAI has scheduled the Sora 2 and Sora 2 Pro Videos API for removal on 2026-09-24 with no listed replacement, pulling the highest-profile Western competitor three weeks after launch.[^13,35] All of these are list prices on a card that changes monthly.

## 06. What a three-second clip costs to make

fal says H3 Max was "trained and served entirely on NVIDIA GB200 NVL72 systems," and that backend denoising for a 5-second 768p generation runs roughly 2.5 seconds against a wall clock near 3 seconds.[^1,2] What fal never states — on the model card, the pricing page, the launch post, or any engineering surface — is **how many GPUs are working during those 2.5 seconds**.[^2,1] That single integer, call it N, is the whole unit economics. Everything below is a sensitivity analysis around it, not a claim about fal's realized margins.

:::stats
- {label: "Revenue per 5s clip (list)", value: "$0.40"}
- {label: "GB200 cost", value: "$10.50", note: "per GPU-hour, CoreWeave list"}
- {label: "Break-even", value: "55", note: "GPUs per request at list price"}
- {label: "Margin at 16 GPUs", value: "70.8%"}
:::

Start with a public rate card. CoreWeave lists on-demand GB200 NVL72 at $42.00/hour for a 4-GPU instance — $10.50 per GPU-hour — with no spot tier available for GB200.[^20] Divide by 3,600: **$0.00291667 per GPU-second**. H3 Max lists at $0.08 per second of generated video, so a 5-second clip bills $0.40, or $0.20 under the 50%-off launch promo.[^2]

Compute cost is then N × 2.5 × $0.00291667 = **N × $0.00729**. Break-even is $0.40 ÷ $0.00729 ≈ **55 GPUs**. Every number in the table below is that one multiplication.

| GPUs per request | Compute cost per clip | Gross margin at list |
|---|---|---|
| 8 | $0.058 | 85.4% |
| 16 | $0.117 | 70.8% |
| 32 | $0.233 | 41.7% |
| *55 (break-even) | $0.401 | ~0% |
| 72 (full NVL72 rack) | $0.525 | −31.3% |

The conclusion is narrow but firm: fal {accent}cannot be dedicating a full 72-GPU rack to a single clip at list price{/} without losing about 31 cents on every dollar of revenue. The plausible operating band is 8–16 GPUs, or roughly 71–85% gross margin on compute. Under the launch promo, break-even falls to ~27 GPUs and 16 GPUs yields only ~42% — the promo is a real cash cost, not a rounding error. Using the 3-second wall clock instead of the 2.5-second denoise window pulls break-even down to ~46 GPUs.[^2]

MiniMax's own self-host benchmark is a useful sanity check on the lower bound: the same workload takes 75.10 seconds mean inference latency on 4×H200 and 19.04 seconds on 8×B300.[^12] Nothing about that curve is consistent with a single-card job. fal's ~2.5 seconds implies many GPUs, materially fewer denoising steps, or both.

Now the caveats, which are load-bearing. First, $10.50/GPU-hour is a **ceiling** — a published on-demand list price. CoreWeave advertises committed-use discounts up to 60%, so a buyer at fal's scale plausibly lands near $4–6/GPU-hour, roughly doubling every margin above.[^20] If fal owns rather than rents, the arithmetic moves further: a $3.9M all-in NVL72 rack is about $54,000 per GPU; amortized over three years of continuous operation (26,280 hours) that is **$2.06 per GPU-hour** in raw capex, about 5× cheaper than CoreWeave list — and the full-rack loss case disappears entirely.[^21] Those rack estimates are themselves analyst supply-chain reconstructions; NVIDIA publishes no list price and the estimates disagree by up to 1.7×.[^21]

Second, the model assumes 100% utilization with zero idle, cold-start, or failed-generation overhead. Realistic serverless utilization of 50% halves every margin. It also excludes storage, egress, the ~120 kW rack draw, and whatever fal pays MiniMax — an unknown.[^21]

Third, fal has disclosed no GB200 purchase, ownership, or neocloud partnership, so its capacity source is unverified. NVIDIA participated via NVentures in the $140M Series D at a $4.5B valuation, which is the most plausible allocation channel but is not a disclosed supply agreement.[^54] Against roughly $400M annualized revenue serving Adobe, Canva, Shopify, Perplexity and Amazon MGM Studios, the absolute compute bill is affordable at any N in this range.[^54,30] And CoreWeave has told investors it is largely sold out of 2026 capacity while raising list prices — so the marginal cost of incremental GB200 may be rising, not falling.[^20]

## 07. The copyability test

A moat claim is really a claim about time: how long can you hold the ground before somebody else stands on it for free? On that test, H3 Max does not survive its own calendar. MiniMax open-weighted the H3 base on 2026-08-03, and the ecosystem began optimizing it the same day — ComfyUI native support plus INT8, pruned-INT8 and NVFP4-AWQ quantizations all landed within hours of the release.[^6,7] fal's fast endpoint arrived twenty-four days later.[^1]

:::timeline
- {date: 2026-08-03, headline: "MiniMax open-weights the H3 base", body: "ComfyUI native support and INT8, pruned-INT8 and NVFP4-AWQ quantizations ship the same day."}
- {date: 2026-08-11, headline: "Community 4-step Turbo LoRA v1.0", body: "lightx2v/ModelTC publish 8-step and 4-step 768p variants — about eight days after the weights dropped, and free."}
- {date: 2026-08-27, headline: "fal launches H3 Max", body: "A proprietary post-trained fast endpoint, 24 days after the base weights."}
- {date: 2026-08-27, headline: "FastH3 ships with full open weights", body: "UCSD Hao AI Lab with Nuva Lab and NVIDIA: 4-step DMD2 distillation plus 90%-sparse attention, released the same day."}
:::

The middle of that timeline is where the moat argument breaks. A community four-step Turbo LoRA appeared within days of the weights, reaching a v1.0 with 8-step and 4-step 768p variants on 2026-08-11.[^22] By the time H3 Max launched, a free step-distillation of the same base model had been downloadable for over two weeks. And on launch day itself, FastH3 shipped with full open weights: 15 seconds of 768p video in under 13 seconds on 8×B200, the base model's 49 DiT calls collapsed to 4, trained on prompts alone with no video data for a reported "1k+ B200 training hours" — a 5-second clip in 6.1 seconds on 4×B200.[^23] On the speed axis, fal was not ahead of the open ecosystem. It was contemporaneous with it, and later than the free LoRA.

Be fair about what that does and doesn't prove. The community LoRA distills one checkpoint; fal post-trained the whole model, and those are not identical work products.[^22,23] FastH3 publishes no quality metrics at all — gallery samples, no VBench, no FVD, no preference score — covers only text-to-video-with-audio, leaves the image-to-video and reference checkpoints undistilled, and reports latencies that exclude model loading and compilation while depending on a specific CUDA kernel.[^23] A production endpoint that holds quality across every modality is harder than any of that.

| Variant | Weights available | Method disclosed | Quality metrics | 5s clip latency |
|---|---|---|---|---|
| *H3 Max | No | No | No | ~2× faster than FastH3 at matched length[^1,23] |
| FastH3 | Yes, full | Yes (DMD2 + sparse attention) | No — gallery only | 6.1s on 4×B200[^23] |
| Community Turbo LoRA | Yes, free | Yes (4-step LoRA) | No | Not published[^22] |

Every lever in the stack is a published paper with open code. DMD2 reaches four steps and reports a large reduction in inference cost — NeurIPS 2024 Oral, with code, model and dataset released.[^37] TeaCache, training-free, reports up to 4.41× acceleration for a VBench cost of −0.07%, at CVPR 2025.[^38] Step distillation, caching, sparse attention, low-precision quantization: all public, mostly academic, peer-reviewed.[^37,38]

We have watched this exact race before. In late July 2025, fal and Replicate shipped competing branded fast variants of Wan 2.2 within roughly 72 hours of each other at the identical $0.05 per video — and neither did the post-training, both building on the same third-party lightx2v/ModelTC distillation that later produced the H3 Turbo LoRA. Replicate's unoptimized pricing had been $0.40–$1.00, so an 8–20× cost cut was matched immediately.[^24] Six weeks before H3 Max, Baseten published fal's recipe fully itemized: 53.6× total = 20× timestep distillation × 1.5× custom kernels × 1.5× NVFP4, taking Wan 2.2 from over 120 seconds to 2.75.[^25] fal Research's own history rhymes — AuraFlow, the largest fully open flow-based text-to-image model at release, was overtaken by FLUX.1 in about two weeks, and no version has shipped since v0.3 in August 2024. The retiring commit reads *"Not largest now, damn it BFL."*[^49]

The honest counter-argument is that these techniques interfere rather than multiply. FastH3's own numbers scale negatively: a 5-second clip takes 6.1 seconds on 4×B200 but 6.84 on 8×B200 — worse with twice the hardware — and the 15-second case gets 1.20× from doubling GPUs, roughly 60% efficiency.[^23] A tuned serving stack really is harder to reproduce than the sum of its public parts, and fal's ~2× wall-clock edge at matched clip length is genuine engineering. But notice what that concedes: the durable asset is the serving stack and the hardware access, not the post-training. Anyone can post-train these weights. The free versions already did.

## 08. The license nobody is discussing

Everything else in this story is copyable. The distillation recipe is public, the serving tricks leak, and a well-funded community can rent the GPUs. The one input no distiller can reproduce is a legal position — and the H3 weights arrive attached to one.

The weights ship under the **MiniMax H3 Community License Agreement**, dated 2026-08-02 and granted by Nanonoble Pte. Ltd. It is a bespoke instrument, not an OSI-approved open-source licence, and its terms do work that no permissive licence does.[^8]

:::kv
- {term: Licence, def: "MiniMax H3 Community License Agreement, dated 2026-08-02 — bespoke, not OSI-approved"}
- {term: Licensor, def: "Nanonoble Pte. Ltd."}
- {term: Excluded Territories, def: "European Union; United Kingdom; Republic of Korea; United States of America"}
- {term: Derivatives, def: "Permitted — modification, distillation and synthetic-data training, solely within the Applicable Territory"}
- {term: Commercial use, def: "Permitted within the Applicable Territory"}
- {term: Revenue threshold, def: "Separate prior written authorization above $20M yearly revenue (Section IV.1)"}
- {term: Attribution, def: "Section IV.2 — display 'MiniMax H3' prominently on the product interface"}
- {term: Output ownership, def: "'MiniMax claims no rights over the Outputs you generate'"}
- {term: Governing law, def: "Hong Kong SAR"}
:::

Section I.5 defines "Excluded Territories" as "the European Union, the United Kingdom, the Republic of Korea and the United States of America," and "Applicable Territory" as "worldwide, excluding the Excluded Territories."[^8] Section V.4 then states that you "may not use, reproduce, modify, distribute, or display the MiniMax H3 Works or any of their Outputs or results outside the Applicable Territory."[^8] Read the object of that sentence carefully: it reaches **Outputs**, not merely where you stand up a GPU.

What the licence gives is genuinely generous. "Model Derivatives" expressly covers modification, distillation and synthetic-data training, and the grant covers creating them — qualified by "Solely within the Applicable Territory," and separately by Section V.3, which bars using the Works or their Outputs to improve any other AI model except H3 itself and its own derivatives.[^8] There is no Llama-style naming mandate, and MiniMax disclaims ownership of what you generate: "MiniMax claims no rights over the Outputs you generate."[^8] The constraint is not on what you build. It is on where.

Why the carve-out? A MiniMax organization member wrote on the licence discussion thread that "this regional carve-out stems from our ongoing generative video copyright litigation with major Hollywood studios."[^9] MiniMax's own pinned explanation is broader — "the current territory scope is not about excluding specific countries or regions" — pointing instead at a fast-moving regulatory landscape, promising that excluded-territory applicants "auto get access" through an application path, and characterising the Section III.3 attribution as "encouraged best practice, not a legal obligation." Those are informal forum replies, not amendments to an agreement carrying an entire-agreement clause.[^9] From first principles, neither story alone fits: the four-territory set does not track copyright-enforcement risk, because MiniMax is sued only in the US, while the EU, UK and Korea are precisely the jurisdictions with binding AI-specific obligations landing in this window. The coherent read is two mechanisms in one clause — the US leg avoids handing plaintiffs a fresh act of distribution inside a forum where discovery is already open; the other three avoid becoming a regulated model provider. A litigation-only theory does not predict Korea.[^9]

The litigation is real. Disney, Universal/NBCUniversal and Warner Bros. Discovery entities sued in the Central District of California on 2025-09-16 — *Disney Enterprises, Inc. v. MiniMax*, No. 2:25-cv-08768 — and the case number, court, filing date and plaintiff families are independently confirmed.[^26,27] Variety's report on the complaint records a plaintiff group including Marvel, Lucasfilm, Twentieth Century Fox, DreamWorks and DC Comics, an allegation that MiniMax "pirates and plunders Plaintiffs' copyrighted works on a massive scale," and statutory damages sought up to $150,000 per infringed work; that page is now paywalled and the complaint PDF was not re-retrievable, so ==the quotation and the per-work figure are reported but not re-verified at source==.[^26] The detail that matters most: Nanonoble Pte. Ltd. is both the licensor on the H3 Community Licence and a named defendant in that case — the entity granting the weights is the entity being sued.[^26,8] MiniMax's Rule 12(b)(2) personal-jurisdiction motion was denied in May 2026; the case is in discovery, with no settlement, dismissal or injunction.[^27]

Now place fal. Features & Labels, Inc. is a San Francisco company. Post-training is modification; hosting is reproduction; serving is distribution and display — the four verbs Section V.4 restricts outside the Applicable Territory, and the US is an Excluded Territory.[^8,2] Two things cut the other way. The clause is territorial, not nationality-based, so it plausibly turns on where compute and distribution sit rather than where a company is incorporated. And fal is a publicly announced, long-standing MiniMax distribution partner and the day-0 partner for H3 — the obvious vehicle for a bilateral licence outside the community terms, which the agreement itself contemplates through Section IV.1. On revenue alone, fal's reported ~$400M annualized would sit far above the $20M threshold requiring separate written authorization.[^30,8]

:::callout(kind=warn, label=Unresolved)
No public statement, press response, or announced agreement from either fal or
MiniMax addresses whether H3 Max is authorized despite the US exclusion, and
fal's launch materials mention licensing nowhere.[^2,30] A private agreement
would not be expected to surface publicly, so this is an **unanswered question
on the public record — not evidence of non-compliance**. DeepLearning.AI's The
Batch judged MiniMax's release "only minimally open," summarising the position as
weights that "are free, but carry unusual restrictions."[^46]
:::

Why does MiniMax tolerate an arrangement where a US partner serves its base model faster and cheaper? Because the revenue line rewards it. MiniMax listed in Hong Kong in January 2026, raising about $619M at roughly a $6.5B valuation.[^29] Its revenue trajectory in millions of USD — 2023, 2024, FY2025 and H1 2026 — runs {sparkline:3.5,30.5,79.0,116.6}, with first-half 2026 revenue of $116.6M, up 283.1%, and the Open Platform and enterprise line growing 703.1% to $73.9M, or 63.4% of revenue against 30.3% a year earlier; gross margin was 17.9% and the adjusted net loss $293M on R&D of $296.9M, roughly 2.5x revenue.[^28] The trade is legible: give away the 768p base, keep the 2K stage, the Context-IR orchestration and the hosted API. Section IV.2 requires the "MiniMax H3" mark on the interface, so fal's speed win markets MiniMax's model and funnels 2K work back to MiniMax's own endpoint.[^55,8] Founder Yan Junjie has said that "if we had to start over, we would have gone open source on day one."[^55] The tension worth naming is that MiniMax's fastest-growing line is exactly the API business a cheaper, faster H3 Max competes against.[^28]

## 09. Does speed actually matter to buyers?

fal's headline claim is that a 5-second 768p clip renders in under three seconds — faster, they note, than the clip itself plays.[^2,1] The question this section asks is whether that is a product feature or a marketing number, and the honest answer is that it is a real threshold crossing aimed at a want the buyers surveyed to date have not expressed.

Start with the cognition, because it is the one part of this that has not changed. Nielsen's three response-time limits — 0.1 second for a system to feel instantaneous and support direct manipulation, 1 second to keep the user's flow of thought uninterrupted, 10 seconds as the outer limit of attention — are properties of human perception, not of hardware, and they have not moved since 1968.[^39] Be precise about where H3 Max lands. A batch model that returns a finished clip in under three seconds sits in the 1-to-10-second band: the user waits, notices the wait, and stays in the loop. It is nowhere near the 0.1-second direct-manipulation band. {accent}H3 Max buys flow, not interactivity.{/}[^39,2]

Is flow worth paying for? The best causal evidence is not from video. A peer-reviewed controlled experiment on exploratory data analysis found that adding 500 milliseconds of latency significantly decreased user activity and dataset coverage, reduced the rate at which participants made observations, generalizations and hypotheses, and shifted their exploration strategy outright — with a hysteresis effect in which early exposure to the slow condition depressed performance even after the latency was removed.[^41] The domain is charts, not shots, so this transfers by analogy and should be labelled as such. But the mechanism is exactly the one that governs iterate-and-reject creative work: latency narrows the search space a human is willing to traverse.

Now the arithmetic. At $0.08 per second, a 5-second clip costs $0.40. Creative work is iterative; the figure below uses the practitioner rule of thumb of roughly three generations per usable shot — an illustrative ratio, not a measured statistic.

:::iso
- {label: Attempts, glyph: "🎬", count: 3}
- {label: Keepers, glyph: "🎬", count: 1}
:::

Three attempts is $1.20 of compute per keeper. Under the old regime, at MiniMax's own hosted latencies, those same three attempts also consumed twelve to twenty-four minutes of a person waiting. At a $100/hour loaded creative rate, that idle time costs roughly $40 — about 33x the compute bill. At sub-three-second generation the compute stays at $1.20 while the wait collapses to under nine seconds, pulling the entire loop inside Nielsen's 10-second attention limit.[^2,39] Two weaknesses, stated plainly: the three-to-one ratio is practitioner anecdote — there is no published generation-to-keeper study — and $100/hour is an assumption. And the obvious workaround undercuts the whole labour term: a creator who fires several batch jobs in parallel and works on something else recovers most of that idle time. That is what people actually do today.

It is also worth naming where genuine real time already lives, because it is not here. Google DeepMind's Genie 3 generates navigable worlds in real time at 24 frames per second for a few minutes at 720p.[^42] Microsoft Research's WHAMM went from roughly one image per second to 10+ FPS and described the result as a change in kind — users "see the effects of your actions immediately, essentially allowing you to play inside the model."[^48] That is the best-documented case of a latency threshold changing the artifact itself. But these are frame-by-frame streaming systems that accept input mid-generation. H3 Max streams nothing and accepts nothing mid-generation; at identical total latency it is still a different product.[^42,48]

Then the turn. A CVPR 2025 workshop survey gathered artist feedback on generative film-making and named the wanted improvements as consistency, controllability, fine-grained editing, and motion refinement. Speed does not appear.[^43] Advertising is the demand centre, and its top use case is volume — 42% of buyers cite different versions of one video for different audiences, ahead of style changes at 38% and contextual relevance at 36% — yet the benefit they name is cost efficiency, cited by 64% and up from fifth place in 2024. Not turnaround time.[^44]

The steelman for fal is that respondents rank against the frontier they know; nobody asked for streaming video before it existed.[^43] The sharper critique is that the real cost driver is iteration count, not per-generation time — a model needing fewer attempts beats one that fails faster. On that framing the prompt-adherence claim matters more than the speed claim, and prompt adherence is precisely what rests on fal's own unpublished preference study. Meanwhile 768p sits below the 1080p delivery floor for paid social, making the output a master requiring an upscale rather than a deliverable — and with the 2K stage never open-weighted, that ceiling is structural.[^1]

## 10. What would break this thesis

The argument of this article is narrow enough to be wrong in specific ways, so here is where it is most exposed.

:::position(confidence=medium, horizon=2027-Q1)
stance: H3 Max's durable advantage is hardware access and a licence position, not post-training — and fal's speed lead over the open ecosystem will be measured in months, not years.
consensus: That fal's in-house post-training and inference co-design produced a defensible quality-and-speed moat over open-weight alternatives.
resolves: A published independent wall-clock benchmark of H3 Max against fal-hosted base H3 at matched 768p, plus whether a rival provider ships a comparable H3 endpoint at or below $0.08/sec before 2027-Q1.
:::

**The decomposition could be wrong, and an adversarial pass found the specific way.** The 2.3x residual rests on dividing a throughput ratio by a latency ratio across two differently-worded baselines with no stated workload.[^1,2] If the 35x is measured against fal's own hosted base H3 rather than MiniMax's endpoint — as at least one independent reading holds — the division is void and the residual is the full 35x.[^52] That single ambiguity is the largest single point of failure in this article. fal can settle it in one sentence and has not.

**The quality result could firm up.** At today's sample the Artificial Analysis image-to-video lead clears significance at p≈0.019, and the Design Arena gap has widened from 8 to 23 Elo since launch.[^13,16] If that holds across both boards at much larger n, and especially if H3 Max starts appearing on the without-audio board where it is currently absent,[^14] "at least as good as base H3" becomes "better than base H3," and the post-training claim gains real support. What would *not* rescue it is more votes on one board: the identical-checkpoint experiments in Chatbot Arena and 3D Arena show preference Elo generating double-digit gaps from noise and rendering alone.[^33,34]

**The economics could invert.** Section 06's margin band assumes CoreWeave list pricing. If fal owns its GB200 capacity, effective cost falls toward ~$2/GPU-hour and even a full-rack allocation becomes profitable — which would mean fal is buying latency with capital rather than cleverness, strengthening the hardware-moat reading rather than the engineering one.[^20,21] If instead fal rents at list into a market CoreWeave calls largely sold out, the 8–16 GPU band is close to a hard constraint on how fast H3 Max can ever get.[^20]

**The legal reading could dissolve entirely.** If fal discloses a bilateral MiniMax authorization — which the licence explicitly contemplates and which fal's day-0 partner status makes plausible — the unresolved question in section 08 closes.[^8,30] Note what that does to the thesis: it does not weaken the argument that the licence is the least copyable asset. It strengthens it. A negotiated agreement with a licensor that no community distiller can obtain is precisely the moat. The reading that *would* break is the opposite one — if MiniMax's stated auto-approval for excluded-territory applicants is real and routine, then the legal position is available to anyone who asks, and it is not a moat at all.[^9]

**The copyability evidence could be overstated.** FastH3 publishes no quality metrics whatsoever and covers one modality.[^23] A free 4-step LoRA is not a production endpoint with an SLA. If nobody converts those artifacts into a competitive hosted product within a quarter, the practical moat is real even though the technical one is not — and the Wan 2.2 precedent, where fal and Replicate converged in 72 hours, cuts the other way.[^24]

:::statement(attr="ARA Research")
The most interesting thing about H3 Max is not that fal made an open model fast. It is that the fastest video endpoint on the market is built on weights whose licence excludes the country it is served from.
:::

Two things this article does not claim. It does not claim fal is infringing: the territorial clause turns on where compute sits, a bilateral licence is plausible, and no party has been asked on the record.[^8] And it does not claim H3 Max is a bad product — it is genuinely fast, genuinely cheap relative to Veo 3.1 Standard and Kling 3.0 Pro, and its speed result is far better evidenced than its quality result.[^13,31]

What it does claim is that the marketing and the evidence point at different assets. fal sold a post-training story. The record shows a serving story, a hardware story, and a licensing story — and only the last of those is hard to copy.

An adversarial pass over the article's three load-bearing claims broke one and left two standing. The statistical audit of the launch-day "#1" survived: no source was found asserting significance at the sample fal cited.[^13,14] The Nanonoble finding survived end-to-end against both the licence text and the federal docket.[^8,26] The 2.3x decomposition did not survive clean — its contested baseline is marked in section 02 and restated above.[^52]

:::note
The claim that post-training contributes roughly 2.3x is an illustrative upper
bound derived by dividing fal's 35x throughput figure by its own 15x figure for
base H3 on fal's stack. The two are stated against differently-worded baselines
with no published workload, and at least one independent reading disputes which
endpoint the 35x is measured against — so the ratio should be read as bounded
speculation, not a measured result. Leaderboard readings from Design Arena were
taken from a client-rendered page and are not reproducible from page source.
:::

:::source
fal, MiniMax and NVIDIA primary documentation; Artificial Analysis and Design
Arena leaderboards as of 2026-08-31; US District Court filings; ARA analysis.
:::

:::references
- {id: 1, title: "Introducing H3 Max by fal", url: "https://blog.fal.ai/introducing-h3-max-by-fal/", source: "fal", date: "2026-08-27"}
- {id: 2, title: "MiniMax H3 Max: Free AI Video Generator, Ranked #1, Post-Trained by fal", url: "https://fal.ai/minimax-h3-max", source: "fal", date: "2026-08-26"}
- {id: 3, title: "MiniMax H3 Max text-to-video API reference", url: "https://fal.ai/models/minimax/h3-max/text-to-video", source: "fal"}
- {id: 4, title: "MiniMax H3 text-to-video API reference and pricing", url: "https://fal.ai/models/minimax/h3/text-to-video", source: "fal"}
- {id: 5, title: "MiniMax H3, open-weights general-purpose multimodal video model", url: "https://fal.ai/minimax-h3", source: "fal"}
- {id: 6, title: "MiniMax H3 is now open source", url: "https://www.minimax.io/news/minimax-h3-open-source", source: "MiniMax", date: "2026-08-03"}
- {id: 7, title: "MiniMaxAI/MiniMax-H3 model card", url: "https://huggingface.co/MiniMaxAI/MiniMax-H3", source: "Hugging Face", date: "2026-08-03"}
- {id: 8, title: "MiniMax H3 Community License Agreement", url: "https://huggingface.co/MiniMaxAI/MiniMax-H3/raw/main/LICENSE", source: "Nanonoble Pte. Ltd.", date: "2026-08-02"}
- {id: 9, title: "MiniMax-H3 discussion #12: license questions", url: "https://huggingface.co/MiniMaxAI/MiniMax-H3/discussions/12", source: "Hugging Face", date: "2026-08"}
- {id: 10, title: "Video generation models and IDs", url: "https://platform.minimax.io/docs/guides/video-generation", source: "MiniMax platform docs"}
- {id: 11, title: "Pay-as-you-go pricing", url: "https://platform.minimax.io/docs/guides/pricing-paygo", source: "MiniMax platform docs"}
- {id: 12, title: "Local deployment benchmarks for MiniMax H3", url: "https://platform.minimax.io/docs/guides/local-deploy-h3", source: "MiniMax platform docs"}
- {id: 13, title: "Video arena leaderboard: image to video", url: "https://artificialanalysis.ai/video/leaderboard/image-to-video", source: "Artificial Analysis", date: "2026-08-31"}
- {id: 14, title: "Video arena leaderboard: text to video", url: "https://artificialanalysis.ai/video/leaderboard/text-to-video", source: "Artificial Analysis", date: "2026-08-31"}
- {id: 15, title: "Video arena methodology", url: "https://artificialanalysis.ai/video/methodology", source: "Artificial Analysis", date: "2026-08-31"}
- {id: 16, title: "Image-to-video leaderboard", url: "https://www.designarena.ai/leaderboard/image-to-video", source: "Design Arena", date: "2026-08-31"}
- {id: 17, title: "Design Arena methodology", url: "https://notes.designarena.ai/methodology/", source: "Design Arena"}
- {id: 18, title: "Ulysses Unbound: experiments in communication-computation overlap", url: "https://blog.fal.ai/ulysses-unbound-experiments-in-communication-computation-overlap/", source: "fal", date: "2026-02-23"}
- {id: 19, title: "The fal interview: building the generative media cloud", url: "https://www.latent.space/p/fal", source: "Latent Space"}
- {id: 20, title: "CoreWeave GPU pricing", url: "https://www.coreweave.com/pricing", source: "CoreWeave", date: "2026-08-31"}
- {id: 21, title: "GB300 NVL72 vs GB200 NVL72: pricing and availability 2026", url: "https://www.spheron.network/blog/gb300-nvl72-vs-gb200-nvl72-pricing-availability-2026/", source: "Spheron", date: "2026-08-16"}
- {id: 22, title: "MiniMax H3 Turbo LightX2V v1.0 release", url: "https://comfyui-wiki.com/en/news/2026-08-11-minimax-h3-turbo-lightx2v-v1", source: "ComfyUI Wiki", date: "2026-08-11"}
- {id: 23, title: "FastH3 preview: 4-step distillation of MiniMax H3", url: "https://haoailab.com/blogs/fasth3-preview/", source: "Hao AI Lab, UCSD", date: "2026-08-27"}
- {id: 24, title: "Wan 2.2 on Replicate", url: "https://replicate.com/blog/wan-22", source: "Replicate", date: "2025-07-30"}
- {id: 25, title: "Real-time video generation inference on Baseten", url: "https://www.baseten.co/blog/real-time-video-generation-inference-on-baseten/", source: "Baseten", date: "2026-07-16"}
- {id: 26, title: "Disney, Warner Bros. Discovery and NBCU sue Chinese AI company MiniMax", url: "https://variety.com/2025/digital/news/disney-warner-bros-discovery-nbcu-lawsuit-minimax-chinese-ai-company-1236520395/", source: "Variety", date: "2025-09-16"}
- {id: 27, title: "Disney Enterprises, Inc. v. MiniMax, No. 2:25-cv-08768 (C.D. Cal.) docket", url: "https://www.courtlistener.com/docket/71357247/disney-enterprises-inc-v-minimax/", source: "CourtListener"}
- {id: 28, title: "MiniMax announces first half 2026 financial results", url: "https://www.minimax.io/news/minimax-announces-first-half-2026-financial-results-1787744160", source: "MiniMax", date: "2026-08-26"}
- {id: 29, title: "MiniMax shares surge in Hong Kong debut", url: "https://www.cnbc.com/2026/01/09/minimax-hong-kong-ipo-ai-tigers-zhipu.html", source: "CNBC", date: "2026-01-09"}
- {id: 30, title: "Partnering with fal: the generative media company", url: "https://sequoiacap.com/article/partnering-with-fal-the-generative-media-company", source: "Sequoia Capital", date: "2025-12"}
- {id: 31, title: "Gemini API pricing, including Veo 3.1 tiers", url: "https://ai.google.dev/gemini-api/docs/pricing", source: "Google", date: "2026-08-31"}
- {id: 32, title: "OpenAI API pricing, including Sora 2", url: "https://developers.openai.com/api/docs/pricing", source: "OpenAI", date: "2026-08-31"}
- {id: 33, title: "The Leaderboard Illusion", url: "https://arxiv.org/abs/2504.20879", source: "arXiv 2504.20879", date: "2025-04-29"}
- {id: 34, title: "3D Arena: an open platform for generative 3D evaluation", url: "https://arxiv.org/html/2506.18787v1", source: "arXiv 2506.18787", date: "2025-06-23"}
- {id: 35, title: "OpenAI API deprecations: Videos API and Sora 2 sunset", url: "https://developers.openai.com/api/docs/deprecations", source: "OpenAI", date: "2026-08-31"}
- {id: 37, title: "Improved distribution matching distillation for fast image synthesis (DMD2)", url: "https://arxiv.org/abs/2405.14867", source: "arXiv 2405.14867", date: "2024-05-23"}
- {id: 38, title: "Timestep embedding tells: it's time to cache for video diffusion model (TeaCache)", url: "https://arxiv.org/abs/2411.19108", source: "arXiv 2411.19108", date: "2024-11-28"}
- {id: 39, title: "Response times: the three important limits", url: "https://www.nngroup.com/articles/response-times-3-important-limits/", source: "Nielsen Norman Group"}
- {id: 40, title: "H3 Max vs MiniMax H3: what the boards actually show", url: "https://www.orcarouter.ai/blog/h3-max-vs-minimax-h3", source: "OrcaRouter", date: "2026-08-27"}
- {id: 41, title: "The effects of interactive latency on exploratory visual analysis", url: "https://idl.uw.edu/papers/latency", source: "IEEE TVCG 20(12)", date: "2014-10-01"}
- {id: 42, title: "Genie 3: a new frontier for world models", url: "https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/", source: "Google DeepMind", date: "2025-08"}
- {id: 43, title: "Generative AI for film creation: a survey of recent advances", url: "https://arxiv.org/abs/2504.08296", source: "arXiv 2504.08296", date: "2025-04-11"}
- {id: 44, title: "Over half of ad buyers are using generative AI for video creation", url: "https://www.marketingdive.com/news/over-half-of-ad-buyers-are-using-generative-ai-for-video-creation-iab/753048/", source: "Marketing Dive / IAB", date: "2025"}
- {id: 45, title: "MiniMax partners with fal", url: "https://www.minimax.io/news/minimax-partners-with-falai", source: "MiniMax"}
- {id: 46, title: "MiniMax's state-of-the-art video model is only minimally open", url: "https://www.deeplearning.ai/the-batch/minimaxs-state-of-the-art-video-model-is-only-minimally-open", source: "The Batch, DeepLearning.AI", date: "2026-08-14"}
- {id: 47, title: "fal Serverless", url: "https://fal.ai/serverless", source: "fal"}
- {id: 48, title: "WHAMM: real-time world modelling of interactive environments", url: "https://www.microsoft.com/en-us/research/articles/whamm-real-time-world-modelling-of-interactive-environments/", source: "Microsoft Research", date: "2025"}
- {id: 49, title: "fal/AuraFlow-v0.3 model repository", url: "https://huggingface.co/fal/AuraFlow-v0.3", source: "Hugging Face", date: "2024-08-14"}
- {id: 50, title: "MiniMax H3 image-to-video on WaveSpeedAI", url: "https://wavespeed.ai/models/wavespeed-ai/minimax-h3/image-to-video", source: "WaveSpeedAI", date: "2026-08-28"}
- {id: 51, title: "Seedance 2.5 text-to-video pricing", url: "https://fal.ai/models/bytedance/seedance-2.5/text-to-video", source: "fal", date: "2026-08-31"}
- {id: 52, title: "fal H3 Max: faster than real-time video generation", url: "https://www.digitalapplied.com/blog/fal-h3-max-faster-than-real-time-video-generation", source: "Digital Applied", date: "2026-08-27"}
- {id: 53, title: "fal on X: introducing H3 Max", url: "https://x.com/fal/status/2092710681577504975", source: "X / fal", date: "2026-08-26"}
- {id: 54, title: "fal company profile: funding, revenue and growth", url: "https://sacra.com/c/fal-ai/", source: "Sacra", date: "2026-03"}
- {id: 55, title: "Forget the price wars: MiniMax goes open source to rewrite the AI playbook", url: "https://kr-asia.com/forget-the-price-wars-minimax-goes-open-source-to-rewrite-the-ai-playbook", source: "KrASIA", date: "2026"}
:::
