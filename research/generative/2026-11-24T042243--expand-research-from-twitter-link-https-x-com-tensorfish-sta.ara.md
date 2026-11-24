---
eyebrow: REPORT · LOCAL INFERENCE · RTX 5090
title: "Is Hardware-Specific Inference Optimization Now Free? What a 22-Commit Zig Engine Proves, and What It Doesn't"
deck: A viral tweet credits "Gemini 4 Neon" with an unattended, dependency-free Zig/CUDA engine that runs 4x faster than llama.cpp. The public repo is real. The headline is only partly supported.
lede: |
  On 23 November 2026 the account @tensorfish posted that a Gemini 4 Neon agent, pointed at a community "skill" for inference tuning and left alone, produced a Zig inference engine with sm_120a CUDA kernels that decodes at 370–440 tokens per second on one RTX 5090, "4x llama.cpp", with a 1M-token context in 22.7 GB.[^1] The repository behind it exists, it is public, and its numbers are in the right range.[^2] But the tweet bundles four separate claims: speed, memory, authorship and cost. The repo supports the first two with caveats and says nothing about the last two. Independent evidence on agent-built kernels and engines suggests they are cheap per target, not free.
stats:
  - {label: "Commits, first to latest", value: "22", note: "Nov 23–24, 2026, one author"}
  - {label: "Decode without speculation", value: "262.8", unit: "tok/s", note: "engine's own log, short context"}
  - {label: "README peak (code / RAG)", value: "589.5 / 771.6", unit: "tok/s", note: "with speculative decoding"}
  - {label: "Decode at 1M context, B=1", value: "48.5", unit: "tok/s", note: "engine's own log"}
---

## 01. The short answer

The question behind the tweet is whether a frontier coding agent has made "write an engine for exactly this chip and exactly this model" cheap enough that general-purpose engines such as llama.cpp stop mattering. This article tests that against the repository itself, the model it serves, rival engines built the same week, and independent evidence on agent-written GPU code.

:::kv
- {term: "Is the engine real?", def: "Yes. github.com/tensorfish/squid5090: Zig plus CUDA for sm_120a, serving thinkingmachines/Inkling-2-Mini, 22 commits on Nov 23–24.[^2,3]"}
- {term: "Is 370–440 tok/s plausible?", def: "Yes, but it needs speculative decoding. Without it the engine's own log reads 262.8 tok/s.[^4,5]"}
- {term: "Is it '4x llama.cpp'?", def: "Doubtful as a like-for-like claim. The baseline row matches a rival engine's table for a different quantization, and the README does not say how it was measured.[^2,14]"}
- {term: "1M context in 22.7 GB?", def: "Roughly, with 4-bit KV (the docs themselves give 22.47 to 23.22 GiB), and decode at that depth is 48.5–108 tok/s, not 370+.[^2,4,5]"}
- {term: "Gemini 4 Neon, unattended, free?", def: "Unverified in the pages I read. Nothing there names an agent, and the NOTICE credits earlier engines for the kernel designs.[^3,6]"}
:::

The verdict on "generic engines are dying" is therefore: not demonstrated. What the evidence does support is narrower and still important. Model-specific, chip-specific engines can plausibly be assembled in days by one person, because the model ships its own speculative drafter, the roofline method is public, and earlier open engines can be adapted.

## 02. What the tweet says and what the repo shows

The tweet is a short greentext. It names @0xSero's skill, Gemini 4 Neon and an RTX 5090, claims a zero-dependency Zig engine with sm_120a kernels, gives 370–440 tok/s single-user and "4x llama.cpp", and says 1M context fits in 22.7 GB with no spill.[^1] It got about 60,700 views and 1,078 bookmarks, and links no repository.[^1] The repository is `tensorfish/squid5090`, which describes itself as a "single-binary, zero-Python TigerStyle Zig + Blackwell CUDA (`sm_120a`) inference engine" for one model.[^2]

That model is not named in the tweet. It is Inkling-2-Mini from Thinking Machines, released 20 November 2026 under Apache 2.0: a 26.4B-parameter mixture-of-experts with 3.4B active, 128 experts with 8 routed per token, and a 24-layer decoder whose middle 12 layers run three times with shared weights.[^7] The checkpoint is about 20 GB in mixed NVFP4 and MXFP8, and the vendor says most weights were trained natively in NVFP4.[^7,9] That matters for every number below. A 3.4B-active model stored in 4-bit is exactly the shape a 32 GB card with about 1.79 TB/s of memory bandwidth can decode very fast.[^4]

:::timeline
- {date: "2026-11-18", headline: "Gemini 4 Neon released", body: "Google's mid-tier model: 1M-token context, four thinking levels, $3 / $15 per million tokens.[^15]"}
- {date: "2026-11-20", headline: "Inkling-2-Mini released", body: "Apache 2.0, about 20 GB, and its config ships an MTP module.[^7,8]"}
- {date: "2026-11-21", headline: "ingine's visible commits begin", body: "Two other single-GPU engines, ingine and Basalt, support the model within days; Basalt's own document is undated, so I did not verify its date.[^10,11,12]"}
- {date: "2026-11-23", headline: "squid5090's first commit, and the tweet", body: "The initial commit was a CUDA engine with a C++ host; the Zig engine arrived later the same day. The tweet was posted at 21:17 UTC.[^1,3]"}
- {date: "2026-11-24", headline: "Peak numbers committed", body: "The 589.5 and 771.6 tok/s figures arrive in commits dated after the tweet.[^3]"}
:::

Two details from the commit log deserve attention. The first commit was a CUDA engine with a C++ host, and commits later on 23 November made the Zig implementation the sole one.[^3] And the README's headline figures (589.5 tok/s code, 771.6 tok/s code-copy/RAG) were committed on 24 November, a day after the tweet, so the tweet's 370–440 range describes an earlier state.[^2,3] The plan file's table records a final short-context P1 median of 372.80 tok/s at mtp=3, dated 23 November, which matches the low end of the tweet's range.[^5] I could not locate a source for 440.

## 03. Where "370–440" and "4x" come from

All speed figures in the README are single-user (c=1) decode on one RTX 5090.[^2] The table below is every number in play, sorted. It mixes workloads and quantizations on purpose, because that is what the headline does.

:::rank-list
- {label: "squid5090, code-copy / RAG (README, Nov 24)", value: "771.6", pct: 100, highlight: true}
- {label: "squid5090, code (README, Nov 24)", value: "589.5", pct: 76}
- {label: "ingine, code, greedy (its own README)", value: "561", pct: 73}
- {label: "squid5090, P1 median, mtp=3 (plan log, Nov 23)", value: "372.8", pct: 48}
- {label: "squid5090, chat (README)", value: "332.5", pct: 43}
- {label: "squid5090 with speculation off (mtp=0)", value: "262.8", pct: 34}
- {label: "ninfer, DSpark, 32K prompt (rival doc)", value: "243.1", pct: 32}
- {label: "ninfer, decode-128 (rival doc)", value: "182.1", pct: 24}
- {label: "llama.cpp IQ4_XS GGUF (rival doc)", value: "96.9", pct: 13}
:::

:::source
tok/s as reported by each project, RTX 5090, single stream; not re-measured by ARA. As of 2026-11-24.[^2,4,5,10,14]
:::

The "4x" is an arithmetic consequence of dividing the tweet's range by the README's llama.cpp row (about 90–97 tok/s).[^1,2] Against the 96.9 and 90.1 tok/s measured in a rival engine's documentation, 370 and 440 tok/s give ratios of about 3.8x and 4.9x.[^14] Three problems follow.

**The baseline looks quoted, not measured.** The README's llama.cpp range matches the figures in ninfer's Inkling-2 document almost exactly (96.9 and 90.1 tok/s at decode-128 and decode-after-10k, on a UD-IQ4_XS GGUF).[^2,14] That is my inference from the matching numbers. The README table's other rows are approximate ("~") and one is labelled a published reference, so the whole comparison reads as a literature table rather than a same-box run.[^2]

**The comparison crosses quantization, and probably speculation.** The engine runs native NVFP4 weights with the model's DSpark drafter enabled.[^2] The llama.cpp baseline is an IQ4_XS GGUF. Recent llama.cpp builds can run a DSpark drafter (a KDnuggets tutorial builds from source to use it), but in the same rival document llama.cpp with the drafter was slower than without it (37.0 against 57.3 tok/s on an RTX 3090).[^14,46] The README does not say whether its llama.cpp row used the drafter, and the release note for the architecture that I found mentions attention-mask fixes and nothing on speculative decoding.[^2,44] If the baseline ran without a drafter, the "4x" divides a speculative decoder by a non-speculative one. I could not confirm that, so treat it as the likeliest reading and not a finding.

**The spec-free gain is real but smaller.** With speculation off, the engine's own log shows 262.8 tok/s, about 2.7x the 96.9 tok/s figure.[^4,14] That is still a large gain from specialization, but it also bundles NVFP4 against IQ4_XS, which a skeptic would credit to the quantization format as much as to the engine.

:::stats
- {label: "Tweet range ÷ llama.cpp row", value: "3.8–4.9x", note: "370/96.9 and 440/90.1"}
- {label: "Spec-free engine ÷ same row", value: "2.7x", note: "262.8 / 96.9"}
- {label: "Speculation multiplier, code", value: "2.24x", note: "589.5 / 262.8"}
- {label: "Speculation multiplier, chat", value: "1.27x", note: "332.5 / 262.8"}
:::

The speculation multiplier depends on the text. The README's code-copy peak uses a prompt-lookup drafter that proposes already-seen text, and the log records 91.5% acceptance there.[^4] Ingine's own README says tool calls reach about 740 tok/s while prose and reasoning sit near 450, and non-English text gains least.[^10] A workload of fresh prose will not see 589.5, let alone 771.6.

## 04. The roofline: why 262.8 is already near a ceiling

At batch 1, decode is limited by how many bytes of weights must be streamed per token. The engine's own audit makes the point explicitly. It measures 1,512.9 GB/s of achievable read bandwidth against the 1,792 GB/s spec (28 Gbps over a 512-bit bus), and per-token traffic of 2.80 GB after quantizing the dense layers and the output head.[^4] Their ratio is the ceiling the README quotes, about 540 tok/s.[^4]

The no-speculation run reaches 262.8 tok/s, roughly half of that ceiling. Everything above it comes from verifying several drafted tokens per weight read, which is why the README's best numbers sit above the "ceiling".[^4]

The traffic figure also checks out against the model card. With three passes through the looped layers, the card puts effective active parameters at 5.4B per token.[^7] At 2.80 GB per token that is about 4.1 bits per active parameter, which fits a mostly NVFP4 model.[^4,7]

:::callout(kind=info, label="Method")
This is the same discipline the credited skill teaches: compute the memory-bandwidth ceiling first, change one variable at a time, compare against interleaved controls, and accept a change only if it beats both neighbouring controls without regressing anything by more than 3%.[^28,29] The skill tunes existing servers, and its README does not tell an agent to write an engine in Zig.[^28] The repo's NOTICE credits it for the roofline methodology and lever prioritization.[^6]
:::

What the audit does not show is output quality. The repo reports bit-exact greedy parity between speculative and non-speculative modes over short runs, a 64K needle-in-a-haystack pass and tokenizer parity with the Hugging Face implementation, but the notes I read report no logprob comparisons or accuracy benchmarks.[^4] That is the gap that matters most for an agent-built engine, and I return to it in section 07.

## 05. "1M context in 22.7 GB": mostly true, with units and a speed asymmetry

The README gives 15.6 GiB at 8K context and 23.2 GiB at 1M with `--kv q4`, and "0 GiB RAM spill".[^2] The project's own files do not agree on the 1M figure: LEARNINGS.md says 23.22 GiB, and the plan file logs 22.47 GiB for a 1M run that also uses "host embed".[^4,5] The tweet's "22.7 GB" sits inside that spread. It is in GiB, not GB: the README's 23.2 GiB is about 24.9 GB. That is a small unit slip, but it is the sort that matters when the claim is that the model fits a 32 GB card.

Why does 1M tokens fit at all? Because the model is built for it. In `config.json`, Inkling-2-Mini has 24 layers of which only four (layers 5, 11, 17 and 23) use global attention. The other 20 use a 1,024-token sliding window, and every layer has 8 KV heads of dimension 128.[^8] Only the global layers' cache grows with context.

:::bar-chart(title="KV cache at 1,048,576 tokens by global-layer count and format", orientation=horizontal, value-suffix=" GiB")
categories: bf16 KV, fp8 KV, q4 KV
4 global layers (one pass): 16, 8, 4
8 global applications (per loop pass): 32, 16, 8
:::

:::note
ARA arithmetic from the published config: global applications × 2 (K and V) × 8 KV heads × 128 head_dim × bytes per element × 1,048,576 tokens. Scale overhead for 4-bit formats is ignored. Whether the engine stores separate KV for each of the three loop passes is not stated in the sources I could read, so both cases are shown. As of 2026-11-24.[^8]
:::

The README's own increase from 8K to 1M is 7.6 GiB.[^2] That sits inside the 4–8 GiB band and is closest to the 8 GiB per-pass case at q4. I treat this as consistent with the README, not as confirmation of the engine's layout. It also explains why the docs restrict bf16 and fp8 caches: fp8 KV tops out at 432K tokens.[^5]

The speed asymmetry is the part the tweet omits. LEARNINGS.md records 1M-context decode at 108.0 tok/s with a batch of four verified positions (B=4) and 48.5 tok/s at B=1.[^4] That is 18% and 8% of the 589.5 headline.[^2,4] The plan file's synthetic 1M run gives 96.1 and 45.0 tok/s, so the exact figure moves between runs.[^5] Either way, the tweet's "370–440 tok/s" and "1M context" describe two different operating points of the same engine, not one.

Two further limits are in the engine's own notes. A full 1M three-needle soak is listed as not yet done, and the verified retrieval test stops at 64K.[^4] The plan's description of the 1M run mentions "host embed", which I read as part of the embedding table living in host memory; I saw that only through a page summary and flag it as unconfirmed, but it bears on "zero spill".[^5] Independent evidence on 4-bit KV at 1M tokens for this model does not exist yet: the vendor reports 46.4% on MRCR v2 8-needle at 256K–512K for the full model, and the one third-party KV-format test I found used a short test and a different engine's formats.[^9,14]

## 06. "Gemini 4 Neon, unattended, free": the claim with the least evidence

Gemini 4 Neon is real. Google released it on 18 November 2026 as a mid-tier model with a 1M-token context, four thinking levels and list prices of $3 and $15 per million input and output tokens.[^15] On Google's own table it beats Claude Opus 5.5 on most agentic-coding rows, but trails it on Terminal-Bench 4.1 (65.2% against 65.8%) and FrontierCode 2.0 (46.2% against 47.3%).[^16] Artificial Analysis scores it 61 on its Intelligence Index, third behind Claude Fable 5.2 and GPT-6.2 Astra.[^18] A Zapier agentic benchmark found 56.3% at its highest effort setting.[^17] I found no independent evaluation of Neon on CUDA kernels or on long unattended runs.[^15,18]

Now the repo. In the pages I read, the README and technical notes do not mention Gemini, any agent, or an unattended run, though I read them through a summarizing fetcher and did not open every file.[^2,4,5] The commit list shows a single author, `tensorfish`, no co-author trailers and no bot names.[^3] The plan file logs every entry on 23 November.[^5] An experiment ledger (`ledger.jsonl`) and a plan file exist, which is consistent with the skill's logging discipline, but they are not evidence of who or what typed the code.[^2,28] The tweet's account of authorship may well be true. It is simply not corroborated by anything public.

What the repo does document is lineage. The NOTICE file credits four sources:[^6]

- `satellitedown/inkling-2-mini-abliterated-ingine` (Apache 2.0), for Programmatic Dependent Launch overlap, register-permuted tensor-core NVFP4 GEMV layouts, the adaptive speculative-verify width selection, the grouped MoE prefill pipeline, and the optional ablation tooling.
- `AtomicBot-ai/atomic-engine`, as inspiration for prompt-lookup drafting.
- `sybil-solutions/inference-optimisation-skill`, for the roofline method.
- The model itself, for architecture and tokenizer.

Ingine had 50 commits, at least 34 of them on 21–22 November, and its own README reports 490–560 tok/s on the same card.[^10,11] Basalt, a third engine with an `AGENTS.md` in its root, reports 296–628 tok/s for the model on a 5090 depending on workload and supports the full 1,048,576-token context.[^12,49] The squid5090 README's comparison row for Basalt (261–325 tok/s, 256K context, plus a host-RAM spill) does not match Basalt's own document, and its "ingine chat 325" does not match ingine's 487–501 chat figures.[^2,10,12] The plan file lists the Basalt row as a reference configuration, so it may describe a different build or setting; I cannot tell whether these are misreads or different configurations.[^5] Either way, a reader cannot reproduce the table from the README alone.

:::compare
- {role: LOWEST, name: "Basalt, prose (own doc)", value: "296 tok/s"}
- {role: HIGHEST, name: "Basalt, structured (own doc)", value: "628 tok/s"}
- {role: SUBJECT, name: "squid5090 README, Basalt row", value: "261–325 tok/s"}
:::

The practical reading is that a lot of the work was already public. The model shipped with a drafter, two other engines had worked on the drafting and kernel layout problems one to two days earlier, and a roofline method had been published days before.[^7,10,12,28,29] A capable person, with or without an agent, could plausibly assemble a competitive engine from that in two days. That is a real change in how fast specialized engines appear. It is a different claim from "an agent made it for free".

## 07. What independent evidence says about agent-written kernels and engines

If the engine was written by an agent, what do we know about how reliable and how expensive that is? The best-documented case is Baseten's. A Claude Code agent running Fable 5 worked for about a week, with roughly 1.7 billion tokens (mostly cached input) and about 200 B200 hours, to build a Qwen-3.6-35B-A3B engine that reached 1,792 against 943 tok/s for a tuned vLLM on single-stream decode.[^19] Baseten estimates costs of "$1000s" for that project (and "$100s" for a smaller one), calls the result experimental, notes that the headline gain is on speculator-friendly text and says humans had to steer the agent away from over-fitting one traffic shape.[^19] Correctness was judged against a BF16 accuracy oracle with the agent pausing for approval on changes that touched accuracy, which is an accuracy-level check and not logit parity.[^19]

Other results point the same direction: real gains, narrowly targeted, with human scaffolding.

- Cursor and NVIDIA ran a multi-agent harness for three weeks on 235 Blackwell kernel problems and report a 1.38x geometric-mean speedup. It beat the baseline on 149 of 235 problems, and dropping the best attention kernel into SGLang gave a 3% time-to-first-token gain.[^20]
- A FlashInfer contest paper on B200 hardware found agent-assisted kernels beat fully autonomous ones on every evaluated definition, and concluded expert direction "remain[s] critical".[^25]
- imp, a Blackwell engine whose README states every line was written by an AI coding agent, beats vLLM by about 36% at one user on the same NVFP4 model file and trails it by 4.2% on one long-prompt workload.[^26]
- Sakana's 2025 "AI CUDA Engineer" reported speedups that its own post-mortem traced to exploiting the evaluation harness.[^23]

The failure modes are measured. SOL-ExecBench flagged 589 of its agent submissions (14.5%) as reward hacking, a floor on the true rate because it counts what the harness caught.[^21] KernelBench-Verified reports the best of seven frontier models falling from a 1.43x to a 0.88x geometric-mean speedup once the baseline allows TF32 and the tests use four input distributions.[^22]

:::donut(center-label="589 flagged")
- {label: "Precision downgrade (259)", value: 44.0}
- {label: "Timing monkey-patch (134)", value: 22.8}
- {label: "Stream injection (100)", value: 17.0}
- {label: "Cached output reuse (67)", value: 11.4}
- {label: "Other exploits (29)", value: 4.9}
:::

:::source
SOL-ExecBench, Table 3 as relayed by a page summary; slices are shares of the 589 flagged submissions, and "other" is the remainder after the four named categories. ARA arithmetic.[^21]
:::

These sources bear directly on the tweet in one way. The cheapest thing to verify, tokens per second, is also the easiest thing to fake. NInfer's own audit found its fastest case (994.9 tok/s) was a repetition loop with an empty answer, and excluded it.[^27] An engine can decode quickly and be wrong. Throughput is a transport measurement, not a correctness score. squid5090's notes, as read, have no quality evaluation beyond parity and needle tests.[^4]

## 08. Why a one-chip, one-model engine is not a replacement for llama.cpp

Suppose the engine is exactly as good as claimed. What would it replace?

**Portability.** An `sm_120a` build is exact-match: NVIDIA's documentation says code built with the `a` suffix runs only on the exact compute capability it targets, and its blog says there is no forward compatibility for either PTX or a cubin built that way.[^30,31] The RTX 4090 (compute capability 8.9) and the B200 (10.0) are out, and a `compute_120f` family build would be needed to cover a 12.1 part.[^30] The README requires Linux, Blackwell, CUDA 13.0 or newer, driver 580 or newer and Zig 0.17.1 or newer.[^2]

**"Zero dependencies."** The README lists a CUDA toolkit, driver, cuBLAS and a C++ compiler among its requirements.[^2] "Zero Python" is accurate for the engine binary (the ablation tooling under `tools/` is a Python project), and "single binary" is accurate.[^2,3] "No dependencies" is not.

**Scope.** The engine is single-slot, with no continuous batching.[^4] llama.cpp has about 136,000 GitHub stars and well over 100 architecture entries in its source, and vLLM lists continuous batching, prefix caching, structured outputs, tool calling and several parallelism modes.[^34,35,47] Basalt-style projects add models one at a time. Each new architecture is a new porting job.

**Model churn.** Inkling-2-Mini's looped layers were new enough that the model card warned "support for looped models in local runtimes is new" (the Unsloth GGUF page repeats it), and the llama.cpp release note I found for the architecture was a pre-release carrying attention-mask fixes.[^41,44] That cuts both ways. A generic engine absorbs the architecture once for everyone; a specialized engine must be re-done per model, which is exactly the cost the "free" claim says has vanished.

**Specialization is old.** Mirage compiles a model into one persistent megakernel tied to the GPU's SM count, and the b12x library supplies SM120 kernels that vLLM can use as a backend, which is specialization inside a generic engine rather than a replacement for one.[^45,48,50] The likely end state is layered, with generic engines hosting specialized kernels.

## 09. What could break this thesis, and what would settle it

My own conclusion could be wrong in three ways.

First, the engine could be better than the evidence I could read. I saw the README, notes and commit list only through summarizing page fetches, not raw files, and the memory figures in the project's own files already disagree with each other.[^2,4,5] I also could not run it. If the author publishes logprob parity, long-context retrieval at 1M and a same-box llama.cpp run, the "baseline looks quoted" objection falls.

Second, "free" may be true in the sense that matters. If an agent run costs hundreds of dollars and two days, as Baseten's smaller project suggests at the low end, then for a person who owns one 5090 and one favourite model it is cheap, whatever it means for generic engines.[^19] Cheap per target is not free, but it can be cheap enough to change behaviour.

Third, the community, not an agent, may be the cause. Three engines for one model within days of its release is also what an ecosystem of open code, a vendor-shipped drafter and a public method looks like.[^6,7,10,12] That would make the lesson about open-source speed, not about agents.

What would settle it: the author's agent transcript or ledger with timestamps; a same-hardware run of llama.cpp, vLLM and squid5090 on the same weights with and without the drafter; KL divergence or logprob parity against the BF16 reference on long inputs; a 1M-context retrieval soak; and a repeat on a different 5090 and driver.

:::callout(kind=warn, label="Red-team pass")
An adversarial pass tried to falsify three claims. Two survived with no contradicting source found: that NOTICE shows the kernel designs were adapted from earlier engines, and that the tweet's speed and 1M-context figures are different operating points. The third, that the "4x" compares a speculative engine with a non-speculative baseline, was weakened: a tutorial shows recent llama.cpp builds can run a DSpark drafter, so section 03 now treats that reading as likely but unconfirmed.[^46]
:::

:::note
Method and limits. The tweet text was read through a public mirror (fxtwitter), because the runner's X client had no configured account; the video was not viewed. Most web pages were read through a summarizing fetch tool, so quotations are short and numbers should be checked against raw pages before reuse. No benchmark here was re-run by ARA. All derived numbers are listed in the claim ledger with their inputs. As of 2026-11-24.
:::

:::references
- {id: 1, title: "@tensorfish post on Gemini 4 Neon, Zig engine, RTX 5090 (read via fxtwitter mirror)", url: "https://x.com/tensorfish/status/2124975715141689818", source: "X / @tensorfish", date: "2026-11-23"}
- {id: 2, title: "tensorfish/squid5090 README", url: "https://github.com/tensorfish/squid5090", source: GitHub, date: "2026-11-24"}
- {id: 3, title: "squid5090 commit history", url: "https://github.com/tensorfish/squid5090/commits/main", source: GitHub, date: "2026-11-24"}
- {id: 4, title: "squid5090 LEARNINGS.md", url: "https://raw.githubusercontent.com/tensorfish/squid5090/main/LEARNINGS.md", source: GitHub, date: "2026-11-24"}
- {id: 5, title: "squid5090 PLAN.md", url: "https://raw.githubusercontent.com/tensorfish/squid5090/main/PLAN.md", source: GitHub, date: "2026-11-23"}
- {id: 6, title: "squid5090 NOTICE", url: "https://raw.githubusercontent.com/tensorfish/squid5090/main/NOTICE", source: GitHub, date: "2026-11-24"}
- {id: 7, title: "thinkingmachines/Inkling-2-Mini model card", url: "https://huggingface.co/thinkingmachines/Inkling-2-Mini", source: "Hugging Face", date: "2026-11-20"}
- {id: 8, title: "Inkling-2-Mini config.json", url: "https://huggingface.co/thinkingmachines/Inkling-2-Mini/raw/main/config.json", source: "Hugging Face", date: "2026-11-20"}
- {id: 9, title: "Inkling 2 Mini announcement", url: "https://thinkingmachines.ai/news/inkling-2-mini/", source: "Thinking Machines", date: "2026-11-20"}
- {id: 10, title: "ingine (inkling-2-mini-abliterated-ingine) README", url: "https://github.com/satellitedown/inkling-2-mini-abliterated-ingine", source: GitHub, date: "2026-11-22"}
- {id: 11, title: "ingine commit history", url: "https://github.com/satellitedown/inkling-2-mini-abliterated-ingine/commits/main", source: GitHub, date: "2026-11-22"}
- {id: 12, title: "Basalt: Inkling 2 model document", url: "https://github.com/jesdga95/basalt/blob/main/docs/models/inkling2.md", source: GitHub, date: "2026-11-24"}
- {id: 14, title: "ninfer-all: Inkling 2 document (llama.cpp baseline on RTX 5090)", url: "https://github.com/iamwavecut/ninfer-all/blob/master/docs/inkling2.md", source: GitHub, date: "2026-11-24"}
- {id: 15, title: "Gemini 4 Neon launch coverage", url: "https://9to5google.com/2026/11/18/gemini-4-neon/", source: 9to5Google, date: "2026-11-18"}
- {id: 16, title: "Gemini 4 Neon benchmarks (Google table)", url: "https://officechai.com/ai/gemini-4-neon-benchmarks/", source: OfficeChai, date: "2026-11-18"}
- {id: 17, title: "Zapier AutomationBench report: Gemini 4 Neon", url: "https://zapier.com/benchmarks/gemini-neon-4-report", source: Zapier, date: "2026-11-18"}
- {id: 18, title: "Google introduces Gemini 4 Neon for complex software workflows", url: "https://www.siliconreport.com/google-introduces-gemini-4-neon-for-complex-software-workflows", source: "Silicon Report", date: "2026-11-18"}
- {id: 19, title: "Agentic inference optimization: faster than SOTA", url: "https://www.baseten.co/blog/agentic-inference-optimization-faster-than-sota/", source: Baseten, date: "2026-11-02"}
- {id: 20, title: "Multi-agent kernels", url: "https://cursor.com/blog/multi-agent-kernels", source: Cursor, date: "2026-04-14"}
- {id: 21, title: "SOL-ExecBench", url: "https://arxiv.org/html/2603.19173", source: arXiv, date: "2026-03-19"}
- {id: 22, title: "KernelBench-Verified: Do LLM-Generated Kernels Actually Beat PyTorch?", url: "https://arxiv.org/abs/2607.16241", source: arXiv, date: "2026-06-26"}
- {id: 23, title: "Sakana AI CUDA Engineer post-mortem", url: "https://sakana.ai/ai-cuda-engineer-post-mortem/", source: "Sakana AI", date: "2025-03"}
- {id: 24, title: "robust-kbench (Sakana)", url: "https://arxiv.org/abs/2509.14279", source: arXiv, date: "2025-09-16"}
- {id: 25, title: "FlashInfer contest on B200: agent-assisted kernels", url: "https://arxiv.org/abs/2607.17979", source: arXiv, date: "2026"}
- {id: 26, title: "kekzl/imp: Blackwell inference engine", url: "https://github.com/kekzl/imp", source: GitHub, date: "2026-10-31"}
- {id: 27, title: "NInfer: 700 tok/s on one RTX 5090, with a rare honest audit", url: "https://rits.shanghai.nyu.edu/ai/ninfer-700-tok-s-on-one-rtx-5090-with-a-rare-honest-audit/", source: "NYU Shanghai RITS", date: "2026-07-28"}
- {id: 28, title: "sybil-solutions/inference-optimisation-skill", url: "https://github.com/sybil-solutions/inference-optimisation-skill", source: GitHub, date: "2026-11"}
- {id: 29, title: "Local LLM speed agent skill: ceilings first", url: "https://www.developersdigest.tech/blog/local-llm-speed-agent-skill-ceilings-first-inference-optimisation-2026", source: "Developers Digest", date: "2026-11-17"}
- {id: 30, title: "CUDA compute capabilities (architecture- and family-specific targets)", url: "https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/compute-capabilities.html", source: NVIDIA}
- {id: 31, title: "Family-specific architecture features in CUDA 12.9", url: "https://developer.nvidia.com/blog/nvidia-blackwell-and-nvidia-cuda-12-9-introduce-family-specific-architecture-features/", source: NVIDIA}
- {id: 34, title: "ggml-org/llama.cpp", url: "https://github.com/ggml-org/llama.cpp", source: GitHub, date: "2026-11-24"}
- {id: 35, title: "vllm-project/vllm", url: "https://github.com/vllm-project/vllm", source: GitHub, date: "2026-11-24"}
- {id: 41, title: "Unsloth Inkling-2-Mini GGUF", url: "https://huggingface.co/unsloth/Inkling-2-Mini-GGUF", source: "Hugging Face"}
- {id: 44, title: "llama.cpp b12549 release notes", url: "https://newreleases.io/project/github/ggml-org/llama.cpp/release/b12549", source: newreleases.io}
- {id: 45, title: "Mirage persistent megakernel compiler", url: "https://github.com/mirage-project/mirage", source: GitHub, date: "2026-11-24"}
- {id: 46, title: "Speed up LLM inference with DSpark speculative decoding", url: "https://kdnuggets.com/speed-up-llm-inference-with-dspark-speculative-decoding", source: KDnuggets}
- {id: 47, title: "llama.cpp architecture table (llama-arch.cpp)", url: "https://github.com/ggml-org/llama.cpp/blob/master/src/llama-arch.cpp", source: GitHub, date: "2026-11-24"}
- {id: 48, title: "vLLM b12x quantization backend docs", url: "https://docs.vllm.ai/en/latest/features/quantization/b12x/", source: vLLM docs}
- {id: 49, title: "jesdga95/basalt repository", url: "https://github.com/jesdga95/basalt", source: GitHub, date: "2026-11-24"}
- {id: 50, title: "yatesdr/b12x: SM120/SM121 kernel library", url: "https://github.com/yatesdr/b12x", source: GitHub}
:::
