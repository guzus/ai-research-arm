---
eyebrow: Deep Research · Open Models · Compute Audit
title: "Reflection's Beam, audited: the GPU disclosure is real, the 3–4× is mostly about GLM-5.2's verbosity"
deck: A 501B / 23B-active Apache-2.0 MoE from America's best-funded open-weight lab. We rebuilt its compute arithmetic from the published numbers, decomposed the efficiency claim into parameters and tokens, and checked who it was actually compared against.
domain: general
lede: |
  On October 5, 2026, Reflection AI, the lab founded by former DeepMind researchers Misha Laskin and Ioannis Antonoglou, announced Beam: a 501-billion-parameter mixture-of-experts model with 23 billion parameters active per token, pretrained on 23.8 trillion tokens, with Apache-2.0 weights promised "later this month". The launch post is unusually specific about hardware: 6,144 NVIDIA GB300 GPUs for pretraining, 10.5K for reinforcement learning. Its headline claim is that Beam matches GLM-5.2 on advanced reasoning while using 3–4× less inference compute. This report rebuilds the compute arithmetic from Reflection's own figures. It splits the efficiency claim into its two factors, active parameters and generated tokens, and tests "comparable" against the published benchmark table. Our conclusions: the efficiency claim is plausible, narrowly scoped and unverified; the capability framing is generous; and the compute disclosure raises a utilization question Reflection has not answered.
stats:
  - {label: Total / active params, value: "501B / 23B", note: "4.6% active, 52 layers"}
  - {label: Pretraining tokens, value: "23.8T", note: "≈3.3e24 FLOPs by 6ND"}
  - {label: Pretraining cluster, value: "6,144", note: "GB300, under 4 weeks"}
  - {label: RL cluster, value: "10.5K", note: "GB300, 4 weeks, 100M+ rollouts"}
---

:::kv
- {term: "Is the GB300 compute disclosure plausible?", def: "Yes, but it is generous. 23B active × 23.8T tokens is about 3.3e24 FLOPs, roughly DeepSeek-V3's budget. On 6,144 GB300s for four weeks, that implies only about 9% of dense BF16 peak, a quarter of what DeepSeek-V3 and Llama 3 reported [^1,7,10,11]. Either the run was much shorter than four weeks of full-cluster time, or the cluster did other work, or utilization was low. Reflection does not say which."}
- {term: "Does the 3–4× efficiency claim hold?", def: "Arithmetically, it can. About 1.74× comes from active parameters (40B vs 23B). The other 1.7–2.3× must come from GLM-5.2 writing more tokens, and Artificial Analysis independently ranks GLM-5.2 among the least token-efficient leading models [^1,3,25]. No third party has measured Beam's tokens yet."}
- {term: "What does the claim leave out?", def: "Prefill, attention and serving cost, by Reflection's own footnote [^1]. At long agentic contexts those terms likely favor GLM-5.2's sparse attention. In memory-bound decode, where a batch touches most experts, bandwidth costs track total parameters (501B vs ~753B), not active ones [^4,16]."}
- {term: "Is Beam 'comparable' to GLM-5.2?", def: "On agentic coding, roughly. On the four 'advanced reasoning' benchmarks in Reflection's table, Beam trails GLM-5.2 on all four, by 4.3 points on HLE [^1,4]. In Reflection's own table, DeepSeek V4.1 Flash beats Beam on HLE, Terminal Bench 2.1 and DeepSWE with fewer decode-active parameters, though Beam leads it on CritPt [^1,21]."}
- {term: "Is it open yet?", def: "No. Weights, model card and technical report are due later in October 2026; today there is a waitlist [^1,2]."}
:::

## 01. What Reflection actually disclosed

Beam's launch post is more detailed than most open-model announcements about the training system, and less detailed about the model itself. Reflection describes a 52-layer sparse MoE with 501B total and 23B active parameters, "interleaved local and global attention", "fine-grained routed experts", auxiliary-loss-free load balancing borrowed from DeepSeek, and a midtraining stage that extends effective context to one million tokens [^1]. It does not publish the expert count, hidden size, attention-window size or local-to-global layer ratio. Those are exactly the numbers needed to check its inference-compute claim independently [^1].

:::kv
- {term: Architecture, def: "Sparse MoE, 501B total / 23B active, 52 layers, interleaved local + global attention, text-only [^1]"}
- {term: Pretraining data, def: "23.8T tokens; ~95% of raw web tokens filtered out; code and technical content repeated [^1]"}
- {term: Pretraining compute, def: "'Under four weeks' on 6,144 GB300 NVL72 GPUs; goodput 'reached 92.3% towards the end'; nine semi-automatic rewinds [^1]"}
- {term: RL compute, def: "Over 100M rollouts on 10.5K GB300 GPUs over 4 weeks; ~1.3B sandboxes; 256K max rollout context [^1]"}
- {term: Context, def: "1M tokens effective after midtraining [^1]"}
- {term: Licence, def: "Apache 2.0, promised; weights 'later this month' [^1]"}
- {term: Total FLOPs, def: "Not disclosed [^1]"}
:::

The infrastructure detail is unusual. Reflection reports an inference-to-training GPU ratio of 3.9:1 to 5.4:1 during RL, a median weight sync of about 12 seconds, and 71 inference incidents absorbed with a median recovery of 8 minutes [^1]. It also says the pretraining recipe "scales predictably across four orders of magnitude of compute" and that the final base model landed on its predicted performance [^1]. These are claims about engineering maturity, and they are plausible for a lab founded in 2024 that has raised roughly $4.7B [^2].

The benchmark table compares Beam with seven models: Inkling, Nemotron 3 Ultra, GLM 5.2, GLM 5.3, Kimi K3, Qwen 3.8 Max and DeepSeek V4.1 Flash [^1]. Reflection says plainly that Kimi K3 is "ahead on raw capability" and that Beam's advantage "is efficiency at inference time" [^1]. That concession matters for the rest of this report. The launch is not claiming frontier capability. It is claiming capability per unit of compute, and that is a narrower and harder claim to check.

**What would weaken this section:** everything above is self-reported. TechCrunch notes that "Reflection's performance claims haven't been independently verified" [^2], and Hacker News commenters' first objection was "Early access, no weights no tech details" [^28].

**Why it matters:** with no weights, config file or technical report, every independent check of Beam must work backwards from about a dozen disclosed numbers. The rest of this report does that.

## 02. The pretraining compute disclosure, recomputed

**Thesis:** the disclosed tokens and parameters imply a budget almost identical to DeepSeek-V3's. Spread over 6,144 GB300s for four weeks, that budget implies strikingly low hardware utilization. That points to a much shorter effective run or a cluster shared with other work.

Start with the standard training approximation, about 6 FLOPs per active parameter per token. Beam's 23B active parameters × 23.8T tokens gives about **3.28e24 FLOPs** [^1]. DeepSeek-V3 had 37B active parameters and 14.8T tokens, which gives 3.29e24 by the same rule, so the two runs match to within 0.04% [^10]. Beam is a DeepSeek-V3-scale pretraining run on Blackwell Ultra hardware. It is far below Llama 3 405B's 3.8e25 FLOPs [^11], and about 0.33× the EU AI Act's 10^25-FLOP presumption threshold for systemic-risk models, counting pretraining alone [^13].

Now the hardware side. NVIDIA rates a 72-GPU GB300 NVL72 rack at 360 PFLOPS FP16/BF16 and 720 PFLOPS FP8, both "with sparsity" [^7]. That works out to 2.5 PFLOPS dense BF16 and 5 PFLOPS dense FP8 per GPU. NVIDIA's own Blackwell Ultra deep-dive confirms that FP8 peak is unchanged from Blackwell; Ultra's gains are in dense NVFP4 and attention throughput [^8]. If 6,144 GPUs ran for the full 28 days, that is 4.13M GPU-hours. Delivering 3.28e24 FLOPs in that time works out to **about 221 TFLOPS per GPU**, or about 8.8% of dense BF16 peak.

:::stats
- {label: 6ND pretraining FLOPs, value: "3.28e24", note: "23B × 23.8T × 6"}
- {label: GPU-hours (≤28 days), value: "4.13M", note: "6,144 × 28 × 24"}
- {label: Implied delivered rate, value: "221", unit: "TFLOPS/GPU", note: "if cluster fully used"}
- {label: Implied BF16 MFU, value: "8.8%", note: "vs 2.5 PF dense peak"}
:::

That is low by any published standard. Under the same 6ND convention, DeepSeek-V3 delivered about 343 TFLOPS per older H800 [^10]. Meta reported 38–43% BF16 model-FLOPs utilization for Llama 3 405B on H100s, roughly 380–430 TFLOPS per GPU [^11]. And in July 2026 NVIDIA reported Megatron Core sustaining **1,648 TFLOPS per GPU** training DeepSeek-V3 671B on GB300 NVL72, holding 98.5% of that per-GPU rate when scaled from 256 to 1,024 GPUs [^9].

:::exhibit(num="Exhibit 1", title="Delivered training throughput per GPU", subtitle="TFLOPS per GPU, 6ND or vendor-reported", source="Reflection [1]; DeepSeek-V3 report [10]; Llama 3 paper [11]; NVIDIA [9]; ARA arithmetic", note="Beam's bar assumes all 6,144 GPUs ran Beam pretraining for 28 days. Llama 3 shown at the midpoint of its 380–430 range. NVIDIA's record precision is unstated and likely FP8 or lower.")
:::bar-chart(title="Delivered TFLOPS per GPU", orientation=horizontal, value-suffix=" TF")
categories: Beam on GB300 (if 28 days), DeepSeek-V3 on H800, Llama 3 405B on H100, NVIDIA GB300 MoE record
TFLOPS per GPU: 221, 343, 405, 1648
:::
:::

At NVIDIA's benchmark rate, 6,144 GB300s would finish Beam's 3.28e24 FLOPs in about **3.75 days** [^9]. NVIDIA does not state that benchmark's precision. At 66% of dense BF16 peak it is almost certainly FP8 or lower, so it is an upper reference rather than a like-for-like BF16 comparison. Benchmarks also overstate production throughput. Even so, a 35% BF16 utilization, ordinary for a well-tuned MoE run, would finish in about a week. "Under four weeks" is therefore true as an upper bound, but it says little about how hard the cluster worked. The likely explanations are not mutually exclusive:

- the four weeks include ablations, data-mixture sweeps or midtraining on the same machines;
- the cluster was shared with inference or RL infrastructure work;
- a 23B-active model with fine-grained experts spends a large share of its time on all-to-all expert communication rather than matrix multiplies.

The last explanation has a precedent. Aleph Alpha's Kolibri-1, a 3.46B-active MoE, reported 6.4e23 total FLOPs across roughly 492k B200 GPU-hours of pretraining, midtraining and long-context training [^12], which also implies modest utilization for a small-active model.

There is also a small oddity in the headline number. 6,144 is not a whole number of 72-GPU NVL72 racks: it is 85.33 racks [^7]. It is exactly 96 × 64, and 6,144 = 2¹¹ × 3, which is the kind of number a parallelism layout produces. The most charitable reading is that Reflection counted GPUs assigned to the job, not racks, perhaps holding back spare trays per rack for failover. That is our inference; Reflection does not say.

:::callout(kind=warn, label="Disclosure gap")
Reflection publishes GPU counts and wall-clock time but not total FLOPs, training precision, or MFU [^1]. Without those three numbers, "6,144 GB300s in under four weeks" describes a cluster reservation, not the compute Beam actually consumed.
:::

**Counterpoint:** the 6ND rule ignores attention FLOPs, which add roughly 10–30% at long sequence lengths. A low-precision run could also count differently. Neither changes the order of magnitude: even with a 30% attention adjustment, implied BF16 utilization stays near 11%.

**Why it matters:** compute disclosures are increasingly used as proof of seriousness, for investors, governments and regulators. A GPU count without FLOPs lets a lab sound bigger than its run was. Here it most likely means Beam was cheaper to pretrain than the headline suggests, which flatters Reflection's efficiency story even though Reflection did not make that argument.

## 03. The bigger number: RL used more GPU-time than pretraining

**Thesis:** the most important figure in the disclosure is not the pretraining cluster but the RL cluster. By GPU-hours, Beam's post-training was about 1.7× its pretraining. That is a deliberate bet that capability now comes from reinforcement learning at scale.

Reflection's RL run used 10.5K GB300 GPUs for four weeks and produced over 100 million rollouts, with about 1.3 billion sandboxes used for training and grading and an average of 110K concurrent rollouts [^1]. At the same 28-day assumption, that is about **7.06M GPU-hours**, versus at most 4.13M for pretraining: a ratio of about 1.71×.

:::bars
- {label: "Pretraining (6,144 GB300 × ≤28 d)", value: "4.13M GPU-h", pct: 59}
- {label: "RL (10.5K GB300 × 28 d)", value: "7.06M GPU-h", pct: 100}
:::

Most of those RL GPUs were not training. With an inference-to-training ratio of 3.9:1 to 5.4:1, only about 1,600–2,100 GPUs were running gradient updates at any time; the rest generated rollouts [^1]. RL compute is therefore dominated by inference, so a model that writes fewer tokens per rollout is also cheaper to post-train. That connects Reflection's training economics to its inference-efficiency claim. A team that pays per rollout token for 100M rollouts has a strong incentive to train a terse model, and the post describes a "controllable length penalty" applied during RL [^1].

This scale of RL is new for an open-weight lab. For comparison, DeepSeek-V3's entire post-training stage was listed at 5K H800 GPU-hours against 2,664K for pretraining [^10]. Reflection also reports that its reasoning expert alone accounted for 80M rollouts, against what it says were 30M for Thinking Machines' Inkling [^1]. Those competitor figures are Reflection's characterisation, not ours.

**Counterpoint:** GPU-hours are not FLOPs. Rollout generation is memory-bandwidth-bound decode, so 7M RL GPU-hours probably delivered far fewer FLOPs than 7M pretraining GPU-hours would. The cumulative compute that the EU AI Act counts could still land below 10^25 [^13]. Whether it does depends on numbers Reflection has not published.

**Why it matters:** if open-weight capability is increasingly bought with RL rather than pretraining, the right compute disclosure is the full pipeline, not the pretraining cluster. Beam's post is better than most here because it gives both clusters. It still gives neither FLOP total.

## 04. Decomposing the 3–4× efficiency claim

**Thesis:** under Reflection's own formula, the claim multiplies two factors. One, active parameters, is a disclosed architectural fact worth 1.74×. The other, generated tokens, is a behavioural property worth 1.7–2.3×, and it is the part no one outside Reflection has measured.

Reflection's exact wording is that Beam "achieves scores comparable to GLM-5.2 while using 3–4× less inference compute" [^1]. Its method note defines the metric: "FLOPs ≈ 2 × active parameter count × mean generated tokens per attempt", over DeepSWE, HLE and Terminal Bench 2.1, using token data "from Artificial Analysis and DataCurve" [^1]. The post adds that this is "an approximate compute comparison rather than measured inference cost" [^1].

### Factor one: active parameters

Artificial Analysis lists GLM-5.2 at 744B total and 40B active parameters [^3], consistent with the GLM-5 technical report's "744B parameter model (40B active parameters)" [^14]. 40 ÷ 23 = **1.74×**. That factor is fixed by architecture and is not controversial. Reflection's "even more pronounced" comparison to the 2T+ class is also correct on this factor alone: Qwen 3.8-Max is reported at 2.4T total / 95B active [^24] and Kimi K3 at 2.8T / 104B active [^20], so per token they cost 4.1× and 4.5× Beam before any token-count difference. The comparison breaks the other way for DeepSeek V4.1 Flash, which activates 16B parameters during decode [^21]. Per token, Flash is cheaper than Beam.

:::rank-list
- {label: "Kimi K3 (2.8T total)", value: "104B active", pct: 100}
- {label: "Qwen 3.8-Max (2.4T total)", value: "95B active", pct: 91}
- {label: "Nemotron 3 Ultra (550B)", value: "55B active", pct: 53}
- {label: "Inkling (975B)", value: "41B active", pct: 39}
- {label: "GLM-5.2 (744B)", value: "40B active", pct: 38}
- {label: "Beam (501B)", value: "23B active", pct: 22, highlight: true}
- {label: "DeepSeek V4.1 Flash (decode)", value: "16B active", pct: 15}
:::

Sources for the ranking: Kimi K3 model card [^20]; Qwen 3.8-Max per The Decoder [^24]; NVIDIA's Nemotron 3 Ultra page [^22]; Thinking Machines' Inkling page [^23]; Artificial Analysis for GLM-5.2 [^3]; DeepSeek's V4.1 Flash card [^21].

### Factor two: generated tokens

To reach 3×, GLM-5.2 must generate **1.725×** Beam's tokens per attempt. To reach 4×, it must generate **2.3×**. Put differently, Beam must use at most 58% of GLM-5.2's tokens for 3×, and at most 43.5% for 4×.

That is a moderate requirement, because GLM-5.2 is an unusually verbose comparator. Artificial Analysis reports that GLM-5.2 "uses 43k output tokens per Intelligence Index task, of which 37k is reasoning", up from 26k for GLM-5.1, and calls it "among the less token-efficient open weights models at its intelligence level" [^3]. In a June 30 post, Artificial Analysis called it "the most verbose among the leading models", at about 141M output tokens to run its index, roughly 1.8× the average model [^25].

:::exhibit(num="Exhibit 2", title="Output tokens per Intelligence Index task", subtitle="Thousands of tokens, Artificial Analysis, June 2026", source="Artificial Analysis [3]")
:::bar-chart(title="Output tokens per task", orientation=horizontal, value-suffix="k")
categories: GLM-5.2, DeepSeek V4 Pro (max), Kimi K2.6, GLM-5.1, MiniMax-M3
Tokens per task: 43, 37, 35, 26, 24
:::
:::

Artificial Analysis, which has early access, has said only that "early indicators suggest Beam will be one of the most token-efficient open models we've seen for its level of intelligence" [^41]. That points in Reflection's direction. It is not a token count, and it reached us second-hand rather than from AA's own post. Because GLM-5.2's comparison data is AA's, the token side of the claim will become checkable as soon as AA publishes a Beam page.

:::callout(kind=info, label="What the claim really says")
Roughly half of "3–4× less compute" (in log terms) is the active-parameter ratio, a fixed architectural choice. The other half is "Beam thinks in fewer tokens than GLM-5.2 at max effort." That is a claim about RL-trained behaviour, controllable through Beam's reasoning-effort setting [^1], and it depends on which effort level each model was run at. Reflection does not state the effort levels.
:::

Two choices in the comparison flatter Beam. First, the comparator: GLM-5.2's verbosity is concentrated on HLE, one of the three benchmarks in Reflection's chart [^25]. Against a terser model of similar capability, the token factor would shrink. Second, the vintage: GLM-5.2 shipped in June 2026 [^3] and was already superseded by GLM-5.3 by the time Beam launched. Reflection's table includes GLM-5.3, but the headline efficiency claim does not use it [^1].

**Counterpoint:** choosing the most verbose strong model is not cheating. Verbosity is a real cost that buyers pay, and GLM-5.2 is a widely deployed open model. If Beam really reaches GLM-5.2-class agentic coding scores with half the tokens and 58% of the active parameters, that is a meaningful engineering result.

**Why it matters:** "3–4× less compute" will be read as "3–4× cheaper to serve." The decomposition shows that about 1.74× is durable and architectural, while the rest depends on comparator, benchmark mix and effort setting.

## 05. What the formula leaves out, and which way that cuts

**Thesis:** "2 × active parameters × tokens" is a fair floor for MoE feed-forward compute at short context. Reflection's footnote excludes attention, prefill and serving overhead. For long agentic workloads, which are Beam's target, those exclusions probably flatter Beam, and real serving cost is set as much by memory as by FLOPs.

The approximation comes from Kaplan et al. (2020), whose per-token forward compute is 2N **plus** a context-dependent attention term of 2·n_layer·n_ctx·d_attn [^15]. Kaplan notes that the attention term is "a relatively small fraction of the total compute" only when d_model exceeds n_ctx/12 [^15]. For a model a few thousand dimensions wide, that condition fails above roughly 70–100K tokens of context. Agentic coding and terminal tasks run well past that: Beam's own RL rollouts went up to 256K tokens [^1].

At that length the two architectures differ. GLM-5.2 uses DeepSeek-style sparse attention, in which each query attends to a fixed top-k set of earlier tokens. Its "IndexShare" reuses one indexer across every four sparse-attention layers, which Z.ai says reduces "per-token FLOPs by 2.9× at a 1M context length" [^4]. The GLM-5 report says its sparse attention cuts attention compute by roughly 1.5–2× on long sequences [^14]. Beam uses "interleaved local and global attention" [^1]. The local layers are cheap, but the global layers are presumably dense and grow linearly per token with context. How much that costs depends on the local-to-global ratio and window size, which Reflection has not published.

| Cost term | Counted by Reflection? | Likely direction vs GLM-5.2 | Evidence |
|---|---|---|---|
| FFN / expert FLOPs (2 × active × tokens) | Yes | Favors Beam (1.74×/token) | [^1,3] |
| Generated-token count | Yes | Favors Beam, unmeasured externally | [^3,41] |
| Attention at 100K+ context | No | Likely favors GLM-5.2 (sparse, top-k) | [^4,14,15] |
| Prefill of long prompts | No | Mixed: GLM has more active params, Beam's global layers are dense | [^1,4] |
| Weight memory / bandwidth | No | Favors Beam by ~1.5× (501B vs ~753B total) | [^4,16] |
| Serving tier / precision | No | Unknown; can move price 2×+ on its own | [^18] |

Memory is the second gap. Decode is usually memory-bandwidth-bound. DeepSeek's V3 report says that at small per-expert batch sizes "the bottleneck is memory access rather than computation" [^10]. Its production inference write-up notes that high sparsity "necessitates an extremely large overall batch size" [^19]. On memory traffic, Epoch AI is explicit: at batch sizes small enough to be memory-bound, where the tokens in a batch still touch most experts, an MoE must stream nearly all of its weights each step, so its small active count stops paying off against a dense model [^16]. On that axis the relevant ratio is total parameters, about 753B for GLM-5.2's checkpoint against 501B for Beam [^4,1], which is roughly 1.5×, not 1.74×. Weight footprint also sets the minimum deployment size. At FP8, Beam's weights are about 501 GB. A GB300 NVL72 rack carries 20 TB of GPU memory across 72 GPUs, so roughly 278 GB per GPU [^7], meaning Beam needs at least two GPUs and realistically four once KV cache is included.

Price is a third, independent measure. Z.ai lists GLM-5.2 at $1.40 per million input tokens and $4.40 per million output tokens (as of 2026-10-06) [^17]. On OpenRouter, the same model's output price ranges from $1.80 at an fp4 endpoint to $12 at the most expensive of 32 endpoints (as of 2026-10-06) [^18]. Quantization and service tier alone move the price by more than 2×. That is about the same size as the architectural factor in Reflection's claim, and it shows how loosely FLOP counts map to what a buyer pays. Reflection has not published Beam pricing.

**Counterpoint:** the exclusions are not all against Beam. Beam's smaller total size helps memory and deployment footprint. Its local-attention layers could make prefill cheap if global layers are rare. If Beam really generates half as many tokens, the attention term it skips also shrinks. The claim could survive a fuller accounting, perhaps at 2–3× rather than 3–4×. That cannot be determined until the config file ships.

**Why it matters:** buyers of an open-weight model pay for GPUs, memory and latency, not FLOPs. An independent cost-to-run measurement, such as Artificial Analysis's, which uses provider-reported token counts including cached input, is the comparison buyers should wait for [^6].

## 06. "Comparable to GLM-5.2": what the table actually shows

**Thesis:** Beam is roughly at GLM-5.2's level on agentic coding, behind it on every advanced-reasoning benchmark Reflection lists, and clearly behind the current Chinese frontier, including a smaller-active DeepSeek model.

Reflection's table has 13 rows with scores for both Beam and GLM-5.2; Beam leads on eight and trails on five [^1]. Its leads are on agentic coding, tool use, long-context and instruction-following rows. Every one of its five deficits is on reasoning or terminal tasks, and four are the reasoning benchmarks: HLE without tools (36.2 vs 40.5), CritPt (16.3 vs 20.9), AIME 2026 (97.8 vs 99.2) and GPQA Diamond (90.5 vs 91.2) [^1,4]. The HLE gap of 4.3 points on a 2,158-question set [^6] is roughly three standard errors, so unlikely to be noise if both were run on the same harness. The CritPt gap is 22% in relative terms.

:::slope(left-label="GLM-5.2", right-label="Beam")
| Benchmark | GLM-5.2 | Beam |
|---|---|---|
| HLE (no tools) | 40.5 | 36.2 |
| CritPt | 20.9 | 16.3 |
| Terminal Bench 2.1 | 81.0 | 80.1 |
| SWE-Bench Pro v1 | 62.1 | 65.5 |
| DeepSWE | 44.0 | 44.4 |
:::

The claim does fit the agentic benchmarks. On Terminal Bench 2.1 the gap is 0.9 points; on DeepSWE Beam leads by 0.4; on SWE-Bench Pro v1 Beam leads by 3.4 [^1]. So "comparable" is fair for coding agents and overstated for "advanced reasoning", which is the phrase Reflection used [^1].

Harness consistency is a second problem. Reflection's GLM-5.2 numbers for HLE (40.5), Terminal Bench 2.1 (81.0) and CritPt (20.9) match Z.ai's self-reported model card [^4]. Artificial Analysis independently measured GLM-5.2's Terminal Bench 2.1 at 78% [^3]. Z.ai's card lists DeepSWE at 46.2, while Reflection's table shows 44.0 [^4,1]. The table therefore mixes vendor self-reports and third-party numbers, and Beam's own scores come from Reflection's harness. Differences of a few points can come from the harness alone. NVIDIA's Nemotron card and Thinking Machines' Inkling card report the same model, Kimi K2.6, at 75.7 and 80.2 on SWE-bench Verified [^43,42].

The more uncomfortable row is DeepSeek V4.1 Flash. In Reflection's own table, it beats Beam on HLE (39.1 vs 36.2), Terminal Bench 2.1 (90.6 vs 80.1) and DeepSWE (74.2 vs 44.4) [^1], with 16B decode-active parameters against Beam's 23B [^21]. Per token, Beam costs about 1.44× as much as Flash. One Hacker News commenter put it bluntly: "larger than DeepSeek v4.1 Flash, more expensive to run, and worse on every measured metric" [^28]. That is too strong, because Flash's token counts are unknown and Beam could win on tokens. But it explains why the headline compares against GLM-5.2 rather than Flash. Another commenter noticed that GLM 5.3 and DeepSeek V4.1 Flash appear in the table "but not in the charts" [^28].

| Benchmark | Beam | GLM-5.2 | GLM-5.3 | Kimi K3 | DS V4.1 Flash |
|---|---|---|---|---|---|
| *HLE (no tools) | 36.2 | 40.5 | 42.3 | 46.9 | 39.1 |
| Terminal Bench 2.1 | 80.1 | 81.0 | 88.2 | 88.3 | 90.6 |
| DeepSWE v1.1 | 44.4 | 44.0 | 61.0 | 68.0 | 74.2 |
| GPQA Diamond | 90.5 | 91.2 | 91.7 | 93.5 | 90.9 |
| MCP Atlas | 78.7 | 77.8 | 84.2 | 82.3 | NR |

Source: Reflection's launch table [^1]. NR = not reported.

Then there is the coding headline most outlets repeated: 80.9 on SWE-bench Verified [^1]. Reflection reports it only against two US models, Inkling at 77.6 and Nemotron 3 Ultra at 70.7; every Chinese comparator is marked NR [^1]. Inkling's own card lists Kimi K2.6 at 80.2 [^42], so Beam's Verified score roughly matches an earlier-generation Chinese model. The benchmark itself is contested. In February 2026 OpenAI said it was "no longer reporting SWE-bench Verified" and recommended SWE-bench Pro instead [^26], after an audit found flawed tests in 59.4% of a hard failed subset and evidence that frontier models had memorized gold patches [^27].

**Counterpoint:** Reflection's table is more candid than most launch tables. It includes models that beat Beam, and it states that Kimi K3 is ahead [^1]. The chart, not the table, is where the framing is selective.

**Why it matters:** on capability, Beam enters the market roughly level with Chinese models from mid-2026 and behind those from late summer. Its case therefore rests on efficiency and on being American, not on being best.

## 07. The company, the money, and the open-weight promise

**Thesis:** Beam is late against Reflection's own 2025 timeline. It is backed by more money and committed compute than any other US open-weight-only lab, and its "open" status is still a promise. The financing figures most often quoted are weaker than they look.

:::timeline
- {date: 2024-09, headline: "A different 'Reflection' stumbles", body: "HyperWrite's unrelated Reflection 70B is accused of misrepresenting benchmarks; a common source of confusion [^37]."}
- {date: 2025-10, headline: "$2B at $8B valuation", body: "Reflection pitches itself as America's open frontier lab and targets a first model 'early next year' [^29,31]."}
- {date: 2026-04, headline: "$25B pre-money round", body: "CEO confirms the valuation on CNBC; round size not disclosed by the company [^32]."}
- {date: 2026-06, headline: "SpaceX compute deal", body: "Up to $6.3B for GB300 capacity at Colossus 2, $150M/month through 2029 [^33]."}
- {date: 2026-07, headline: "Nebius deal", body: "More than $1B of GB300 capacity through 2029 [^34]."}
- {date: 2026-10-05, headline: "Beam announced", body: "501B/23B MoE; weights promised later in October [^1]."}
:::

**The money.** Reflection's own October 2025 post says it "raised $2 billion" from a list including NVIDIA, Sequoia, Lightspeed, DST and Eric Schmidt [^29]; Reuters put the valuation at $8B [^30]. The often-repeated figure that Nvidia put in $800M is weaker than it looks: Reuters issued a correction "to remove reference to Nvidia being a lead investor" [^30], and neither Nvidia nor Reflection has stated an amount. Startup Fortune repeats the $800M figure [^40]. By October 2026 TechCrunch, citing PitchBook, put total funding at roughly $4.7B and the last round at $25B pre-money [^2]. The company's newsroom links the CEO's on-air confirmation of the valuation [^32].

**The compute deals.** The ">$7B of compute deals" headline adds two contracts of different quality [^2]. The SpaceX deal is "up to $6.3 billion" at $150M per month for GB300s at Colossus 2, a facility xAI built before merging into SpaceX. TechCrunch reports that "either company has the option to end the contract with 90 days' notice after the first three months" [^33]. The firm commitment is therefore about six months of payments, roughly $0.9B. The rest is an option. The Nebius deal is "more than $1 billion" through 2029, which Bloomberg says Nebius confirmed [^34]. Together they buy GB300 access through 2029. They are also circular: Nvidia-linked equity is spent renting Nvidia chips.

**The schedule.** In October 2025 Laskin told TechCrunch the company was "aiming to release" its first model "early next year", trained on "tens of trillions of tokens" [^31]. Beam arrived in October 2026, and its weights are not yet out [^1]. Startup Fortune put it this way: "A waitlisted early version and a promise of full weights 'later in October' is progress, not delivery" [^40]. Delays of announced open weights have precedent, and most have eventually shipped. Until the Hugging Face repository and LICENSE file exist, "Apache 2.0" cannot be checked. Even then, Beam will be open-weight, not open-source: Reflection has said nothing about releasing its 23.8T-token data mix or training code [^1].

**The strategic frame.** Laskin's 2025 pitch was that "DeepSeek and Qwen and all these models are our wake-up call" [^31]. At launch he told Semafor that sovereign-AI customers "don't really have very good options today" [^35] and told Sources that closed models are like "renting an apartment" [^36]. The market data supports the urgency. By March 2026, Chinese open models had 1.15B cumulative Hugging Face downloads against 723M for US models, according to the ATOM report [^38]. The White House's July 2025 AI Action Plan said "we need to ensure America has leading open models founded on American values" [^39].

:::bars
- {label: "Chinese open models (cum. HF downloads, Mar 2026)", value: "1.15B", pct: 100}
- {label: "US open models (cum. HF downloads, Mar 2026)", value: "723M", pct: 63}
:::

**Counterpoint:** a year's slip on a first frontier model is ordinary. Reflection's launch post also gives a specific release window, which is a commitment readers can check within weeks.

**Why it matters:** Beam's value to the US open-weight ecosystem depends on the release actually happening, under the promised licence, with a config that lets others check its efficiency claims.

## 08. What could break this analysis

The analysis above depends on several of our own assumptions, each of which could be wrong.

- **The utilization finding assumes full-cluster use for 28 days.** If Reflection's pretraining ran for, say, eight days at normal MFU and the rest of "under four weeks" was midtraining and ablations, the low-utilization reading disappears. The post's 92.3% goodput figure "towards the end" [^1] suggests the run was instrumented carefully, which argues against simple inefficiency. A technical report with total FLOPs would settle this.
- **6ND may undercount Beam.** Midtraining to 1M context and repeated code epochs add compute beyond 23.8T × 6 × 23B. If Beam's real pretraining FLOPs were 1.5–2× our estimate, implied utilization rises to the mid-teens, which is still low.
- **The token factor could be larger than needed.** If Artificial Analysis publishes Beam's tokens per task well below half of GLM-5.2's 43k [^3], the 3–4× claim survives even after attention and prefill are added back. AA's early comment points that way [^41].
- **Attention cost might favor Beam.** If Beam's global layers are rare (say 1 in 8) and the local window is short, its long-context attention could be close to GLM-5.2's sparse attention, and our directional call in Section 05 would be wrong. We do not know Beam's ratio.
- **Benchmark harnesses.** Our "comparable" analysis uses Reflection's table, which mixes self-reports and third-party numbers [^1,3,4]. Independent re-runs could move every gap by a few points in either direction.
- **The SpaceX deal's exit clause** comes from one secondary report [^33]; if the full contract differs, the "firm vs option" split changes.

:::callout(kind=success, label="Red-team pass")
Red-team pass: 3/3 top claims unbroken. Our adversarial reviewer tried to falsify the 3.28e24-FLOP / ~9% utilization arithmetic, the 1.74× active-parameter share of the efficiency claim, and Beam trailing GLM-5.2 on all four advanced-reasoning benchmarks. It found no contradiction for the first and third. For the second, the only low-severity discrepancy was vLLM's recipe listing GLM-5.2 at 39B active rather than 40B. That would make the architectural factor 1.70× instead of 1.74×, which does not change the conclusion.
:::

**Bottom line:** Beam is a credible, efficiently sized American open-weight MoE built on an unusually large RL investment. Its compute disclosure is more informative than most, though less so than it appears. Its 3–4× efficiency claim is plausible and depends heavily on comparator choice: about 1.74× is architecture, and the rest is GLM-5.2's verbosity. "Comparable on advanced reasoning" overstates the table. The weights, config and an independent token count, all expected within weeks, will settle most of this.

:::references
- {id: 1, title: "Introducing Beam: Reflection's 501B open-weight model", url: "https://reflection.ai/blog/introducing-beam", source: Reflection AI, date: "2026-10-05"}
- {id: 2, title: "Reflection debuts Beam, an open-weight AI model to rival Chinese models at lower compute cost", url: "https://techcrunch.com/2026/10/05/reflection-debuts-beam-a-open-weight-ai-model-to-rival-chinese-models-at-lower-compute-cost/", source: TechCrunch, date: "2026-10-05"}
- {id: 3, title: "GLM-5.2 is the new leading open weights model on the Artificial Analysis Intelligence Index", url: "https://artificialanalysis.ai/articles/glm-5-2-is-the-new-leading-open-weights-model-on-the-artificial-analysis-intelligence-index", source: Artificial Analysis, date: "2026-06-16"}
- {id: 4, title: "zai-org/GLM-5.2 model card", url: "https://huggingface.co/zai-org/GLM-5.2", source: Hugging Face / Z.ai, date: "2026-06-16"}
- {id: 5, title: "GLM-5.2 model page", url: "https://artificialanalysis.ai/models/glm-5-2", source: Artificial Analysis, date: "2026-10-06"}
- {id: 6, title: "Intelligence benchmarking methodology", url: "https://artificialanalysis.ai/methodology/intelligence-benchmarking", source: Artificial Analysis, date: "2026-10-06"}
- {id: 7, title: "GB300 NVL72 specifications", url: "https://www.nvidia.com/en-us/data-center/gb300-nvl72/", source: NVIDIA, date: "2026-10-06"}
- {id: 8, title: "Inside NVIDIA Blackwell Ultra: the chip powering the AI factory era", url: "https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era/", source: NVIDIA Technical Blog, date: "2025-08-22"}
- {id: 9, title: "Setting a world record for MoE pre-training on NVIDIA GB300 NVL72", url: "https://developer.nvidia.com/blog/setting-a-world-record-for-moe-pre-training-on-nvidia-gb300-nvl72/", source: NVIDIA Technical Blog, date: "2026-07-21"}
- {id: 10, title: "DeepSeek-V3 Technical Report", url: "https://arxiv.org/html/2412.19437v2", source: arXiv, date: "2024-12-27"}
- {id: 11, title: "The Llama 3 Herd of Models", url: "https://ar5iv.labs.arxiv.org/html/2407.21783", source: arXiv / Meta, date: "2024-07-23"}
- {id: 12, title: "Aleph-Alpha/Kolibri-1-BF16 model card", url: "https://huggingface.co/Aleph-Alpha/Kolibri-1-BF16", source: Hugging Face / Aleph Alpha, date: "2026-10-03"}
- {id: 13, title: "General-purpose AI models in the AI Act: questions and answers", url: "https://digital-strategy.ec.europa.eu/en/faqs/general-purpose-ai-models-ai-act-questions-answers", source: European Commission}
- {id: 14, title: "GLM-5 technical report", url: "https://arxiv.org/html/2602.15763v1", source: arXiv / Z.ai, date: "2026-02-17"}
- {id: 15, title: "Scaling Laws for Neural Language Models (Kaplan et al.)", url: "https://ar5iv.labs.arxiv.org/html/2001.08361", source: arXiv, date: "2020-01-23"}
- {id: 16, title: "MoE vs dense models: inference", url: "https://epoch.ai/gradient-updates/moe-vs-dense-models-inference", source: Epoch AI, date: "2024-12-20"}
- {id: 17, title: "Z.ai pricing overview", url: "https://docs.z.ai/guides/overview/pricing", source: Z.ai, date: "2026-10-06"}
- {id: 18, title: "GLM-5.2 endpoints", url: "https://openrouter.ai/api/v1/models/z-ai/glm-5.2/endpoints", source: OpenRouter, date: "2026-10-06"}
- {id: 19, title: "DeepSeek-V3/R1 inference system overview", url: "https://github.com/deepseek-ai/open-infra-index/blob/main/202502OpenSourceWeek/day_6_one_more_thing_deepseekV3R1_inference_system_overview.md", source: DeepSeek / GitHub, date: "2025-03-01"}
- {id: 20, title: "moonshotai/Kimi-K3 model card", url: "https://huggingface.co/moonshotai/Kimi-K3", source: Hugging Face / Moonshot AI}
- {id: 21, title: "deepseek-ai/DeepSeek-V4.1-Flash model card", url: "https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash", source: Hugging Face / DeepSeek}
- {id: 22, title: "Nemotron 3 Ultra", url: "https://research.nvidia.com/labs/nemotron/Nemotron-3-Ultra/", source: NVIDIA Research, date: "2026-06-04"}
- {id: 23, title: "Inkling", url: "https://thinkingmachines.ai/inkling/", source: Thinking Machines Lab}
- {id: 24, title: "Alibaba's open-weight Qwen3.8-Max takes on long-horizon AI tasks with 2.4 trillion parameters", url: "https://the-decoder.com/alibabas-open-weight-qwen3-8-max-takes-on-long-horizon-ai-tasks-with-2-4-trillion-parameters/", source: The Decoder, date: "2026-08-03"}
- {id: 25, title: "Artificial Analysis on GLM-5.2 verbosity (X post, mirrored)", url: "https://api.fxtwitter.com/ArtificialAnlys/status/2072022576394821859", source: Artificial Analysis on X, date: "2026-06-30"}
- {id: 26, title: "OpenAI Developers: no longer reporting SWE-bench Verified", url: "https://x.com/OpenAIDevs/status/2026002219909427270", source: OpenAI on X, date: "2026-02-23"}
- {id: 27, title: "OpenAI explains SWE-bench Verified is no longer meaningful", url: "https://gigazine.net/gsc_news/en/20260429-swe-bench-verified/", source: GIGAZINE, date: "2026-04-29"}
- {id: 28, title: "Hacker News discussion: Introducing Beam", url: "https://news.ycombinator.com/item?id=49969183", source: Hacker News, date: "2026-10-05"}
- {id: 29, title: "Building frontier open intelligence", url: "https://reflection.ai/blog/building-frontier-open-intelligencence", source: Reflection AI, date: "2025-10-09"}
- {id: 30, title: "Nvidia-backed Reflection AI raises $2 billion, boosts valuation to $8 billion (Reuters, corrected)", url: "https://www.investing.com/news/stock-market-news/nvidiabacked-reflection-ai-raises-2-billion-in-funding-boosts-valuation-to-8-billion-4279981", source: Reuters via Investing.com, date: "2025-10-09"}
- {id: 31, title: "Reflection raises $2B to be America's open frontier AI lab, challenging DeepSeek", url: "https://techcrunch.com/2025/10/09/reflection-raises-2b-to-be-americas-open-frontier-ai-lab-challenging-deepseek", source: TechCrunch, date: "2025-10-09"}
- {id: 32, title: "Reflection newsroom", url: "https://reflection.ai/newsroom", source: Reflection AI, date: "2026-04-23"}
- {id: 33, title: "SpaceX inks compute deal with Reflection", url: "https://finance.yahoo.com/technology/ai/articles/spacex-inks-compute-deal-reflection-165129019.html", source: TechCrunch via Yahoo Finance, date: "2026-06-23"}
- {id: 34, title: "Nebius to sell $1 billion in AI capacity to startup Reflection", url: "https://news.bloomberglaw.com/ip-law/nebius-to-sell-1-billion-in-ai-capacity-to-startup-reflection", source: Bloomberg Law, date: "2026-07-14"}
- {id: 35, title: "Reflection AI unveils an open-source answer to Chinese labs", url: "https://semafor.com/article/10/05/2026/reflection-ai-unveils-an-open-source-answer-to-chinese-labs", source: Semafor, date: "2026-10-05"}
- {id: 36, title: "Reflection's founders on the open-weight Beam release", url: "https://sources.news/p/reflection-founders-open-weight-beam-release", source: Sources (Alex Heath), date: "2026-10-05"}
- {id: 37, title: "New open source AI leader Reflection 70B's performance questioned, accused of fraud", url: "https://venturebeat.com/ai/new-open-source-ai-leader-reflection-70bs-performance-questioned-accused-of-fraud", source: VentureBeat, date: "2024-09-09"}
- {id: 38, title: "The ATOM Report: American vs Chinese open models", url: "https://arxiv.org/html/2604.07190", source: arXiv, date: "2026-04-08"}
- {id: 39, title: "Open-source AI in Trump's AI Action Plan", url: "https://fedscoop.com/open-source-ai-trump-ai-action-plan/", source: FedScoop, date: "2025-07-23"}
- {id: 40, title: "Reflection AI unveils Beam, a 501-billion-parameter open model to rival China", url: "https://startupfortune.com/reflection-ai-unveils-beam-a-501-billion-parameter-open-model-to-rival-china/", source: Startup Fortune, date: "2026-10-05"}
- {id: 41, title: "Market bell card quoting Artificial Analysis on Beam", url: "https://247wallst.com/cards/tech-did-the-heavy-lifting-again-the-nasdaq-s-1-06-gain-ne-gspc-market-bell-01m46tkf2f7w10vn47cy4b9tyt", source: 24/7 Wall St., date: "2026-10-05"}
- {id: 42, title: "thinkingmachines/Inkling model card", url: "https://huggingface.co/thinkingmachines/Inkling", source: Hugging Face / Thinking Machines Lab}
- {id: 43, title: "nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16 model card", url: "https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16", source: Hugging Face / NVIDIA, date: "2026-06-04"}
:::
