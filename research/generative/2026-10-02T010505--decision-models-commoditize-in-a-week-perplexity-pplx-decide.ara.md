---
eyebrow: DEEP RESEARCH · AI INFRASTRUCTURE
title: "Decision models commoditized in a week — but what got commoditized was the wrapper, not the judgment"
deck: "Between 15 September and 1 October 2026, a new model category went from one vendor to dozens. Perplexity's pplx-decider-27b, Cloudflare's Clef and AutoTrust's JEV-27B-VL all built on the same open Qwen backbone. The price converged on $0.04 per million input tokens. On sealed independent tests the incumbent is still ahead, and OpenAI has yet to name a price."
domain: software
lede: |
  On 15 September 2026, Typesafe released Jev. It was billed as a "system one" model: it does not chat, does not generate text, and returns a calibrated probability over a fixed set of answers for $0.042 per million input tokens, with output free. Sixteen days later the category had flooded. OpenAI announced a Jev-shaped Decisions API at DevDay on 29 September. Liquid, Nace and AWS shipped rivals on 29–30 September. On 1 October, Cloudflare, AutoTrust and Perplexity released open-weight decision models within about twelve hours of each other, all three built on Alibaba's Qwen3.8 family. This piece looks at what actually got cheaper, what did not, and why the $0.04 price point is better read as a cost floor than as a price war.
stats:
  - {label: "Jev list price (in / out)", value: "$0.042 / $0", note: "per M tokens, Typesafe docs, as of 2026-10-02"}
  - {label: "pplx-decider list price", value: "$0.04 / $0", note: "per M tokens, Perplexity docs, as of 2026-10-02"}
  - {label: "Clef on Workers AI", value: "$0.24", note: "per M input; Clef-flash $0.09"}
  - {label: "OpenAI Decisions API price", value: "none", note: "limited preview, unpublished"}
---

:::callout(kind=info, label="Direct answer")
- **Interface and price: yes, commoditized.** Within 16 days of Jev's launch, at least six organisations shipped a Jev-compatible API or open weights[^7,14,20,25,28,29]. Perplexity's list price of $0.04/M input with free output is effectively Jev's own $0.042/M[^2,21].
- **The $0.04 figure is a cost floor, not a price cut.** A one-pass decision model emits no generated tokens, so free output costs the vendor almost nothing. Our arithmetic puts dense-FP8 H100 prefill for a 27B model at about $0.04/M on today's spot prices (about $0.085/M in BF16)[^45,48].
- **Judgment: not commoditized.** On the sealed-item JevBench v1.5.4 leaderboard, Jev 1.13 still has the top capability score among Jev-class systems, though it is #3 on the board's official four-axis score. GPT-6 Luna scores far above everything, at 3.5× Jev's cost per decision[^31].
- **OpenAI is not competing on price yet.** The Decisions API is a limited preview on a GPT-6 Luna variant. Its 150 ms latency figure comes from a vendor slide, and no price has been published[^8,9,10].
:::

## 01. Sixteen days: from one vendor to a category

The commoditization claim holds on the dimension that is easiest to copy, the API contract. Typesafe launched Jev on 15 September with a blog post introducing "System One models": a non-chat model that returns probabilities over predefined options[^1]. Its docs list one model, `jev-1.13.0`, behind `POST /v1/systemone`, priced at "$42 / $0.042" per billion / million input tokens, with "Output tokens are free"[^2]. Founder Diogo Almeida (@CompleteSkeptic) framed the launch as a new class of "frontier composable intelligence optimized for decisions"[^44].

The interface was cheap to replicate, and the replicas arrived quickly. Most of them adopted Typesafe's own wire format. Ollaya, an Ollama-style local host, serves open decision models over `/v1/systemone`, so the official Typesafe SDK works against localhost unchanged[^34]. Cloudflare says Clef is "fully API-compatible" with Jev, and its changelog says migrating means "changing the endpoint and model"[^14,43]. Perplexity's Denis Yarats published AutoJev, also exposing `POST /v1/systemone`, before Perplexity's own release[^24].

:::timeline
- {date: 2026-09-15, headline: "Typesafe launches Jev", body: "Non-chat 'System One' model; $0.042/M input, free output; text only."}
- {date: 2026-09-21, headline: "MotherDuck integration", body: "AG News, 100k rows: Jev 89% in 40 s vs GPT-5.6-terra 88% in ~32 min."}
- {date: 2026-09-24, headline: "$1B+ at $10B+ reported", body: "The Information: Typesafe in talks, ~50× its seed valuation."}
- {date: 2026-09-25, headline: "Ollaya ships", body: "Local host for open decision models speaking Jev's /v1/systemone."}
- {date: 2026-09-28, headline: "Jeff; Nace Drex", body: "Home-trained 0.8B/2B Jev-format models; Nace claims 58.28 vs Jev 57.91 on the community Decision Index."}
- {date: 2026-09-29, headline: "OpenAI Decisions API", body: "DevDay: GPT-6 Luna variant, limited preview, no price. Liquid d1 claims to top Jev the same day."}
- {date: 2026-10-01, headline: "AWS, Cloudflare, AutoTrust, Perplexity", body: "Strands Decider 2B; Clef/Clef-flash (Apache 2.0); JEV-27B-VL; pplx-decider-v1-27b at $0.04/M."}
:::

The 1 October cluster is what turned a trend into a commoditization story. TechCrunch's headline that day described decision models "flood[ing] the web". It reported AWS's Strands Decider 2B as "an open source decision model inspired by TypeSafe's Jev", built on the "torso" of Qwen3.5-2B[^7]. Cloudflare's post put Clef, a frozen Qwen3.8-27B, and Clef-flash, a frozen Qwen3.5-9B, under Apache 2.0[^14]. AutoTrust's card describes JEV-27B-VL as "JEV-27B with vision", also on an unchanged Qwen3.8-27B base[^25]. Perplexity's card says pplx-decider-v1-27b "is a decision model fine-tuned from Qwen3.8-27B" and is Apache-2.0 licensed[^20].

The community trackers measure the breadth. The JevBench v1.5.4 board evaluates 1,624 decisions per system and lists dozens of Jev-class entrants[^31]. The community "Decision Index" kit counts 67 entrants[^26,27].

**What weakens this.** A count of entrants measures how cheap a decision model is to build, not whether anyone buys one. Marc Brooker's AWS side project reportedly cost "in the hundreds or thousands of dollars" (TechCrunch's paraphrase, not a direct quote)[^7]. Firelex trained its 0.8B Jeff adapters in "half an hour to four hours" on one GPU[^35].

**Why it matters.** When the reproduction cost of a category is four figures, whatever the incumbent can defend lives outside the weights.

## 02. What a "decision model" actually is — and why output is free by construction

Mechanically, a decision model is a classifier head on top of a language-model backbone, sold through a typed API. Cloudflare's description is the most explicit. It froze the Qwen backbone, "jointly optimized the routing head alongside rank-256 low-rank adapters", and trained with label-smoothed cross-entropy plus a Brier term. On top of that sits a secondary objective called Reinforcement Learning for Calibrated Decisions (RLCD)[^14]. Its Hugging Face cards describe "a small transformer head that reads the backbone's final hidden states". The released code covers inference only: "record encoding, batching, the model… and `systemone`"[^15,16].

The economics follow from that shape. The model reads the input once (prefill), then reads off one logit per allowed option. Nothing is decoded token by token. Perplexity's developer account describes pplx-decider as trained to produce a probability distribution over a fixed set of answers rather than generating text[^23]. Since output costs the server almost nothing, every vendor bills input only.

:::kv
- {term: "Typesafe Jev 1.13", def: "POST /v1/systemone · text only · 64k per request, 32k for state + longest question · 40 req/s"}
- {term: "Perplexity Decisions API", def: "POST /v1/decisions · question types noul / choice (1–255 options) / score · 1–128 questions · <262,144 input tokens · base64 images only · 10 req/s per org"}
- {term: "Cloudflare Clef (Workers AI)", def: "65,536-token context · 1–64 questions · up to 4 images (Clef extension to the System One API)"}
- {term: "OpenAI Decisions API", def: "Question + allowed answers + text/image context → one answer; no public schema, option cap or probability field yet"}
:::

Sources: Typesafe[^2], Perplexity[^22,46], Cloudflare[^18], AlphaSignal on OpenAI[^10].

None of this is new technique. Zero-shot classification by entailment was open-weight by 2023: Moritz Laurer's 0.4B DeBERTa-v3 model scores labels as "true / not true" hypotheses[^37]. Knowledgator's GLiClass, released in 2025, scores all labels "at a single forward path". That is Jev's interface roughly a year before Jev[^38]. Rerankers had already moved to per-query pricing. Cohere Rerank on AWS Marketplace is priced per "search unit" of one query and up to 100 documents[^39]. Closer to home, OpenAI's Structured Outputs already "ensures the model will always generate responses that adhere to your supplied JSON Schema", which rules out invented enum values[^11]. Its logprobs cookbook already shows per-class probabilities for threshold-setting[^12].

What *is* new is the bundle. A large instruction-tuned backbone supplies world knowledge that a 0.4B NLI model lacks. A head trained for calibration supplies probabilities you can gate on. A typed schema means callers parse nothing. On the Clef thread, one Hacker News commenter called "decision model" "the same kind of marketing as 'LRM'"[^19]. On the Jeff thread, another wrote that "there really isn't any architectural magic to Jev"[^42]. Both readings are defensible, and neither changes the price arithmetic.

**What weakens the "nothing new" reading.** Calibration is the hard part and the measurable one. A 37-dataset third-party arXiv study found Jev's choice probabilities "well calibrated and support selective prediction". In the same study Jev beat a raw Qwen3.8-27B on 27 of 37 datasets[^41]. The backbone alone does not get you there.

**Why it matters.** If the product is backbone + head + schema, the head and the schema are the only things a vendor owns. On 1 October three vendors gave away a head and a schema.

## 03. The price: everyone converged on Jev's number — because that is roughly what it costs

The pricing story reads as a race to the bottom, but nobody undercut Jev by more than rounding. The newcomers priced at, or marginally below, Jev's rate, or well above it. Perplexity's docs list `pplx-decider-v1-27b` at "$ per 1,000,000 input tokens (output tokens are free; no per-request fee)" with an input value of 0.04[^21]. That is $0.002/M under Jev's $0.042[^2]. Cloudflare's Workers AI table lists `@cf/cloudflare/clef` at "$0.240 per M input tokens" and `clef-flash` at "$0.090 per M input tokens"[^17]. Those are 5.7× and 2.1× Jev's rate. Liquid's d1 launched on Liquid's own API as a free `d1:free` tier with paid rates unpublished. OpenRouter now lists it at $0.04/M input with free output[^49,50].

:::bars
- {label: "Cloudflare Clef (27B)", value: "$0.240/M", pct: 100}
- {label: "Cloudflare Clef-flash (9B)", value: "$0.090/M", pct: 38}
- {label: "Typesafe Jev 1.13", value: "$0.042/M", pct: 18}
- {label: "Perplexity pplx-decider-v1-27b", value: "$0.040/M", pct: 17}
- {label: "OpenAI GPT-6 Luna (chat API, for reference)", value: "$0.10/M in + $0.50/M out", pct: 42}
:::

List input prices, as of 2026-10-02. Output is free for all four decision models. Sources: Workers AI pricing[^17], Typesafe docs[^2], Perplexity pricing[^21], OpenAI pricing[^9]. OpenAI has published no Decisions API price[^8].

Aravind Srinivas framed Perplexity's release as a price move. He said it would offer the model "in a new Decisions API at 4 cents per million input tokens and free output tokens", and that prices would fall further[^23]. First principles suggest little room below that. A dense ~26B model needs about 2 × 26B ≈ 52 GFLOP per input token. NVIDIA lists the H100 SXM at 3,958 TFLOPS FP8 "with sparsity", so about 1,979 TFLOPS dense[^48]. At 40% utilisation that is roughly 15k tokens/s, or about 55M tokens per GPU-hour. The repo's Vast.ai snapshot of 2026-10-01 puts the H100 SXM median at about $2.33/GPU-hour[^45]. That gives about $0.042/M at full occupancy in dense FP8. In BF16, at half the throughput, the floor doubles to about $0.085/M.

Either way, $0.04/M sits within a factor of two of the marginal compute cost of a 27B prefill on rented GPUs. That means FP8 or FP4, high batch occupancy, and owned or contracted capacity. The arithmetic says Perplexity is pricing at cost, perhaps with a subsidy, not cutting a fat margin. The same reasoning likely explains Cloudflare's 6× premium. Workers AI bills in "neurons", 21,818 per million Clef input tokens, on a shared serverless fleet where latency-sensitive traffic cannot be batched as aggressively[^17].

:::callout(kind=warn, label="List price ≠ price per decision")
An independent survey-simulation run (Mimic E8, 44,620 predictions, $2.00 of spend) found pplx-decider "costs 8.7× Jev per prediction on batches despite a lower list rate". Tokens consumed per question differ by vendor[^32]. Hacker News users estimated one million Clef decisions at about $72 and measured Clef as "5.2x more expensive" than Jev on their own workload[^19]. Compare cost per decision on your own traffic, not $/M.
:::

The cost-per-decision view also changes the OpenAI comparison. JevBench v1.5.4 lists Jev at $0.032 per 1,000 decisions. Its small-model rivals sit at $0.017. GPT-6 Luna at default effort costs $0.11 per 1,000, which is "cost 3.5× Jev"[^31]. A separate independent run had Luna on chat completions with structured output costing 1.4–2.5× Jev per decision, about 3.5× slower, and returning "no probabilities to gate on"[^13].

**What weakens this.** Jev's parameter count is undisclosed[^3]. If Jev is much smaller than 27B, Typesafe's $0.042 carries a healthy margin, and the 27B open models are the ones pricing at cost. Typesafe's own launch post concedes: "We can't prove it isn't subsidized"[^1].

**Why it matters.** When the list price equals the cost floor, the price war is over before it starts. The remaining levers are hardware (FP4 on Blackwell), model size (distil to 2–9B), and bundling with other services.

## 04. Same backbone, different heads: the open-weight releases compared

All three 1 October open-weight releases share a base model, so their differences come down to the head, the training data and the vendor's claims. The table lays them out side by side, from primary model cards.

| Model | Org | Base | Params | License | Vision | Price (hosted) |
|---|---|---|---|---|---|---|
| *pplx-decider-v1-27b | Perplexity | Qwen3.8-27B (fine-tune) | 26B | Apache-2.0 | Yes | $0.04/M in |
| Clef | Cloudflare | Qwen3.8-27B (frozen) + LoRA r=256 + head | 27B | Apache-2.0 | Yes | $0.24/M in |
| Clef-flash | Cloudflare | Qwen3.5-9B (frozen) + head | 9B | Apache-2.0 | Yes | $0.09/M in |
| JEV-27B-VL | AutoTrust | Qwen3.8-27B (unchanged) + adapter + head | 28B | Apache-2.0 | Yes | — |
| Strands Decider 2B | AWS | Qwen3.5-2B "torso" | 2B | open (licence not named) | — | — |
| Jev 1.13 | Typesafe | undisclosed | undisclosed | closed | No (text only) | $0.042/M in |

Sources: Perplexity card[^20], Cloudflare blog and cards[^14,15,16], AutoTrust card[^25], TechCrunch[^7], Typesafe docs[^2].

Vision is the one axis on which every newcomer differentiates against Jev. Typesafe's docs say "No image, audio, or video input"[^2]. Clef accepts up to four images per request as a "Clef extension to the System One API"[^18]. Perplexity's Decisions API takes base64 PNG, JPEG or WebP, and "The API never fetches a URL"[^22]. The extensions break the compatibility story in one direction: a Jev request runs on Clef, but an image request will not run on Jev. AutoTrust's own card is candid that image-decision calibration "has not been measured systematically"[^25].

"Open" here means open weights, not open systems. Cloudflare released weights, the head, and an inference script. The RLCD training pipeline, the data and the "Trainer" stay closed, and an HN commenter summed it up as "Open weights, not open source"[^15,19]. Perplexity's card publishes no training data or code[^20]. AutoJev, the Yarats repo that appears to be pplx-decider's precursor, is the exception: it documents a full recipe of "One H200 · full-weight SFT · 73,000 unique training examples · 286 updates"[^24].

:::quote(attr="Diogo Almeida, founder, Typesafe, to TechCrunch, 2026-10-01")
I get that people think it's a gold rush, but they might be underestimating the difficulty of making the models actually smart.
:::

The quote is from TechCrunch[^7]. Almeida had already told Latent Space that the training algorithm is not the moat: "It's not about the PPO. That part doesn't matter." Elsewhere in the interview he said: "To me, model capabilities means data"[^4]. Asked whether an RLCD paper exists, he answered: "No, not yet"[^4].

**What weakens the "same backbone, so same product" reading.** The backbone is shared, but the training data, label smoothing, calibration objective and head design differ. Calibration, the one property that justifies paying for a decision model instead of a classifier, is precisely what the releases leave unmeasured. Perplexity's card has no ECE or Brier numbers[^20]. Cloudflare publishes no ECE[^14].

**Why it matters.** When three competitors start from identical weights, the market should expect quality to cluster tightly and price to be set by serving efficiency. That is what the first week shows.

## 05. Benchmarks: who is "ahead" depends on who ran the test

Every 1 October release claims parity or leadership over Jev, and every such claim is self-run. Perplexity's card reports 85.71% overall accuracy for pplx-decider vs 84.51% for Jev and 74.76% for the Qwen base, across 11 benchmarks. It adds that "the pplx-decider-v1-27b results were measured through the Perplexity API", without saying how Jev was measured[^20]. Cloudflare says "Clef is currently the leader when evaluated against the Jev Decision Index"[^14]. Its card shows Clef winning BFCL (98.47 vs 95.75) and BANKING77 (94.20 vs 79.74). The same card shows Jev far ahead on GPQA Diamond (78.3 vs 48.0) and BBH (92.9 vs 73.7)[^15]. AutoTrust reports a self-run six-benchmark mean of 84.07 vs Jev's 83.85[^25].

:::bar-chart(title="Vendor-reported head-to-heads vs Jev (self-run)", orientation=horizontal, mode=grouped, value-suffix=%)
categories: pplx-decider overall (11 tasks), AutoTrust 6-bench mean, Clef BANKING77 F1, Clef BBH, Clef GPQA Diamond
Challenger: 85.71, 84.07, 94.20, 73.7, 48.0
Jev: 84.51, 83.85, 79.74, 92.9, 78.3
:::

Sources: Perplexity card[^20], AutoTrust card[^25], Cloudflare Clef card[^15]. All numbers are vendor-run.

The "Decision Index" that vendors cite is not an official Hugging Face leaderboard. Its README says it is "Unofficial and community-maintained; not affiliated with TypeSafe AI"[^26]. The kit rebuilds its frozen suite from pinned public benchmarks such as MMLU-Pro, BBH and GPQA, so it is not contamination-resistant. Scores within 0.25 points count as ties[^27]. The kit lists three editions (0.1, 0.2 and 0.2.1, the last dated 27 September), so scores are not comparable across versions[^27].

Margins claimed against that index are thin. Nace's Drex claims 58.28 vs Jev's 57.91, +0.37, but it was "trained on the official training splits of the index benchmarks"[^29]. Liquid calls d1 "the first model to outperform Jev on @huggingface's Decision Index". d1 is served through Liquid's API without self-hosted weights[^28,50].

The sealed board tells a different story. JevBench v1.5.4 holds back 720 of 1,624 items, and "sealed decisions are half of Intelligence". On it, Jev 1.13 has the highest capability score among Jev-class systems. It is #3 on the board's official score, which also weighs speed and cost, behind Cygnet[^31]. Perplexity's own card concedes the same pattern on hard items: pplx-decider scores 70.30% on JevBench public hard against Jev's 73.27%[^20].

:::rank-list
- {label: "Jev 1.13.0 (Typesafe)", value: "80.0", pct: 100, highlight: true}
- {label: "Winnow-12B Q8", value: "79.3", pct: 99}
- {label: "Cygnet", value: "79.0", pct: 99}
- {label: "Surogate Rune 26B-A4B v3", value: "79.0", pct: 99}
- {label: "Jev-Omni", value: "76.5", pct: 96}
- {label: "djev", value: "76.4", pct: 96}
- {label: "JevK5 v0.3", value: "72.3", pct: 90}
- {label: "Plumb-4B", value: "71.6", pct: 90}
:::

JevBench v1.5.4 capability score (mean of intelligence and calibration), Jev-class systems, as of 2026-10-02. pplx-decider, Clef, JEV-27B-VL, d1 and Strands Decider are not yet listed[^31].

Two things stand out. The open top-4 are within one point of Jev, so the gap on composite capability is small. And none of the 1 October releases is on the board yet. An earlier JevBench release (v1.4.2) had open decider-4b v2 at 64.13 vs Jev 1.13 at 63.29. The maintainer noted that Jev "out-reasons decider-4b v2 (Intelligence 53.1 vs 49.4) and is better calibrated", and that the 4B model won on speed and cost[^30]. Field tests are mixed. Mimic E8 found pplx-decider, Clef and Clef-flash all statistically "level" with Jev on log loss, and concluded "keep Jev"[^32]. AIMultiple's 1,655-item test had AutoJev-27B and Jev 1.13 within a few points of each other on every axis, with no calibration test[^33].

**What weakens the "incumbent still leads" reading.** Jev is the board's reference system ("Reference system for the Jev-class limits"), and its cost and latency define the class[^31]. A board built around Jev's envelope may structurally favour Jev. On a pure-capability ranking GPT-6 Luna scores 95.9, far above any Jev-class model[^31].

**Why it matters.** "Commoditized" requires interchangeability on quality, not only on price. On sealed items, a one-point composite gap with the 12B–26B open models looks interchangeable for most routing work. The 16-point intelligence gap with the 4B models does not.

## 06. Calibration — the claimed moat that nobody has fully measured

The category's distinguishing promise is calibrated probabilities. On that dimension the evidence is thinnest, for incumbent and challengers alike. A September aggregation of independent studies noted that Typesafe "publishes no calibration error, reliability plot, Brier score or log loss for Jev on any dataset". It found Jev's median ECE of 0.157 beat 16 of 19 LLMs as shipped, but after each LLM got one fitted temperature, 15 of them beat Jev[^40]. AutoJev's README is the only release-day source with calibration numbers. It reports ECE 0.0428 and Brier 0.220 for AutoJev-27B vs 0.0527 and 0.254 for Jev, and Qwen3.8-27B at 0.0648 ECE. All of these are self-run, with calibration from one fitted temperature[^24].

:::stats
- {label: "AutoJev-27B ECE (self-run)", value: "0.043"}
- {label: "Jev ECE (AutoJev run)", value: "0.053"}
- {label: "Laya ECE, before → after refit", value: "0.466 → 0.081"}
- {label: "pplx-decider / Clef ECE", value: "not published"}
:::

Sources: AutoJev README[^24], Laya card[^36], Perplexity card[^20], Cloudflare blog[^14].

Small models show the pattern sharply. Convai's Laya card reports ECE 0.466 before refitting and 0.081 after, but zero-shot accuracy of 0.362, below the 0.461 majority-class baseline. It describes itself as "a fast base to specialise, not a zero-shot decision engine"[^36]. Ollaya's page, citing Winnow's run for Jev, puts hosted Jev at 0.738 accuracy against 0.591 for the open decider:2b and 0.361 for laya:en. Selected local models answered roughly 3–25× faster on an RTX 4090, while others were slower[^34]. Firelex's current Jeff README has its 2B model at 81.7 overall vs Jev's 83.0, winning Financial PhraseBank by about 19 points but losing BBH 66.4 vs 94.3[^35].

**What weakens this section's scepticism.** The one third-party arXiv preprint supports Jev's calibration as "well calibrated" for selective prediction[^41]. And temperature fitting is cheap. If buyers will fit temperatures on their own data, calibration stops being a moat for anyone, Jev included.

**Why it matters.** If calibration can be bolted on with one scalar per task, the category's premium collapses to latency and convenience. That is the classic commodity profile.

## 07. OpenAI's Decisions API: competing on distribution, not price

OpenAI's entry is the most important for market structure and the least specified. The Decoder reports that OpenAI "uses a version of GPT-6 Luna, its low-cost model", that developers supply questions with fixed answers plus text or image context, and that "the API launches as a limited preview, with broad availability expected in the coming days"[^8]. Its latency claim is one slide: about 150 ms vs 1.6 s for a standard Luna call, "ten times faster"[^8]. Sam Altman's stage description, as transcribed by Firecrawl, was "giving our Luna model a predefined set of options to choose from"[^47].

:::compare
- {role: "FASTER", name: "Decisions API (OpenAI slide, unmeasured)", value: "~150 ms"}
- {role: "SLOWER", name: "GPT-6 Luna via standard API (OpenAI slide)", value: "~1.6 s"}
- {role: SUBJECT, name: "Jev hosted p50 / p95 (independent run)", value: "341 / 458 ms"}
:::

Sources: The Decoder[^8], independent Luna-vs-Jev benchmark[^13].

The gaps are on record. OpenAI's API pricing page lists gpt-6-luna at $0.10 per M input and $0.50 per M output, with no Decisions row[^9]. AlphaSignal notes OpenAI "has not published… latency measurements"[^10]. Coverage also disagrees on whether the endpoint returns probabilities at all[^47]. As of 2 October we found no OpenAI price change in response to the 1 October releases[^9].

OpenAI's advantage is capability and placement, not cost. On JevBench, GPT-6 Luna at default effort scores 95.9 capability, 96.2 intelligence and 95.6 calibration, against Jev's 80.0 / 72.0 / 88.0. It costs $0.11 per 1,000 decisions and 1.56 s per call, outside the Jev-class envelope[^31]. If the Decisions endpoint keeps most of Luna's accuracy at a tenth of the latency, it would be a different product from the open 27B models, not a clone. It would also sit next to every OpenAI customer's existing key and billing.

**What weakens this.** All of that is conditional on numbers OpenAI has not published. An endpoint that is "a version of" Luna could be a distilled, much weaker model. Structured Outputs already guarantees valid enums, minus refusals and token-limit cutoffs, so the shape guarantee alone adds little[^11].

**Why it matters.** If OpenAI prices Decisions near Luna's input rate, it brackets the open models from above with higher accuracy. If it prices at $0.04, the independent hosted APIs lose their only differentiator except self-hosting.

## 08. What is left for Typesafe — and for a $10B valuation

The commoditization week landed squarely on a fundraise. AI Weekly, relaying The Information, reported Typesafe in talks to raise $1B+ at a $10B+ valuation. That is "a 50x jump from the $200M valuation PitchBook logged on the company's $40M seed announced September 15"[^6]. No revenue was disclosed. The deal is talks, not a close[^6].

:::slope(left-label="Seed (2026-09-15)", right-label="Reported talks (2026-09-24)", unit=$M)
| Item | Seed | Talks |
|---|---|---|
| Valuation | 200 | 10000 |
| Round size | 40 | 1000 |
:::

Source: AI Weekly / The Information, as relayed[^6]. Unconfirmed by Typesafe.

The defensible assets are data, serving and customers, not weights or method. Almeida's position is that "if model quality matters, then we are gonna be in a very good position for a long time"[^4]. The independent evidence partly supports him. MotherDuck's AG News run, 100k rows, had Jev at 89% in 40 seconds for $0.50 retail vs GPT-5.6-terra at 88% in 31m 59s for $37.58[^5]. Jev still has the top capability score on the sealed JevBench Jev-class board, though it is #3 on the official four-axis score[^31]. As of 2 October Typesafe had not cut its price or shipped a new version: `jev-latest` and `jev-preview` both resolve to `jev-1.13.0`[^2].

**What weakens the bull case.** The open models are within one composite point on the sealed board[^31], and Perplexity matched the price[^21]. Typesafe's own speed multipliers lack a fixed baseline. The launch post's "193.6x faster, 444.6x cheaper" is measured against LLMs run through Typesafe's own wrapper, which Typesafe says "tends to be slower and more expensive", and the post expects these "are on the higher end of real world gains"[^1].

**Why it matters.** A $10B price for a two-week-old product only works if quality keeps a lead that open Qwen fine-tunes cannot close. The first week says the lead is small and measurable, which is a fragile basis for a megaround.

## 09. What could break the thesis

The thesis is that the interface and the price commoditized, while judgment quality and calibration did not. Several pieces of evidence would falsify it.

- **Independent sealed scores for the 1 October models.** If pplx-decider, Clef or JEV-27B-VL lands at or above Jev's 80.0 on JevBench's sealed board, the judgment layer is commoditized too[^31]. The open Winnow-12B and Rune 26B are already within a point[^31].
- **An OpenAI price at or below $0.04/M with Luna-class accuracy.** That would commoditize the incumbent from above, not from below[^9,31].
- **Evidence that Jev is small.** If Typesafe serves a ~2–4B model, its $0.042 carries a large margin, and the "cost floor" reading applies only to the 27B challengers[^3].
- **Calibration measured, not asserted.** Published ECE/Brier on the same items for all vendors would resolve the category's central claim. Today only AutoJev publishes such numbers, and only self-run[^24,40].
- **Field latency vs vendor latency.** Cloudflare's card claims 38.8 ms median for Clef-flash in its internal run. An HN user measured Clef-flash at 661 ms median through the hosted API[^16,19]. If hosted latency stays 10× off the cards, the "system one" pitch weakens for everyone except local deployments.

:::callout(kind=danger, label="Counter-argument: maybe nothing commoditized because nothing existed")
The sharpest deflationary view is that "decision models" are rebranded classifiers and rerankers. GLiClass had one-pass multi-label scoring in 2025[^38], Cohere priced rerank per query[^39], and OpenAI's Structured Outputs and logprobs already gave enums and probabilities[^11,12]. On this view the week did not commoditize a product. It revealed that the product was a fine-tune recipe plus a schema. An HN commenter measured 93.0% on Banking77 with all-MiniLM-L6-v2 plus a simple classifier[^42].
:::

An adversarial red-team pass tested three load-bearing claims, with this result. The absence of a published OpenAI Decisions price survived unbroken[^8,9]. Two claims were tightened in this draft. First, Jev's lead on JevBench holds on capability score but not on the board's official four-axis score, where it ranks #3[^31]. Second, the newcomers did not merely match Jev's price: Perplexity's $0.040 and d1's OpenRouter listing sit marginally below Jev's $0.042[^21,49].

The evidence fits a middle reading. Packaging a frontier-scale backbone as a typed, calibrated classifier is useful. MotherDuck's 40 seconds vs 32 minutes on the same task is not marketing[^5]. But the packaging is reproducible in days on open weights, and the price is pinned to the compute floor. What remains scarce is measured calibration and sealed-set accuracy, and those are exactly the numbers most vendors did not publish this week.

:::references
- {id: 1, title: "Introducing System One models and Jev", url: "https://typesafe.ai/blog/introducing-system-one-models-and-jev", source: "Typesafe blog", date: "2026-09-15"}
- {id: 2, title: "Jev models, pricing and limits", url: "https://docs.typesafe.ai/models.md", source: "Typesafe docs", date: "2026-10-02"}
- {id: 3, title: "Typesafe homepage — $42 per billion input tokens", url: "https://typesafe.ai/", source: "Typesafe", date: "2026-09-28"}
- {id: 4, title: "Jev: Diogo Almeida interview", url: "https://www.latent.space/p/jev", source: "Latent Space", date: "2026-09-21"}
- {id: 5, title: "MotherDuck supports Jev", url: "https://motherduck.com/blog/motherduck-supports-jev/", source: "MotherDuck blog", date: "2026-09-21"}
- {id: 6, title: "The Information: TypeSafe in talks to raise $1B at $10B valuation", url: "https://aiweekly.co/alerts/the-information-typesafe-in-talks-to-raise-1b-at-10b-valuation-days-after-40m", source: "AI Weekly", date: "2026-09-24"}
- {id: 7, title: "Amazon releases its own Jev clone as decision models flood the web", url: "https://techcrunch.com/2026/10/01/amazon-releases-its-own-jev-clone-as-decision-models-flood-the-web/", source: "TechCrunch", date: "2026-10-01"}
- {id: 8, title: "OpenAI expands Codex and its API at DevDay with security scans, a Decisions API and Ultrafast", url: "https://the-decoder.com/openai-expands-codex-and-its-api-at-devday-with-security-scans-a-decisions-api-and-ultrafast/", source: "The Decoder", date: "2026-09-29"}
- {id: 9, title: "OpenAI API pricing", url: "https://developers.openai.com/api/docs/pricing", source: "OpenAI", date: "2026-10-02"}
- {id: 10, title: "OpenAI's Decisions API gives developers a constrained GPT-6 Luna router", url: "https://alphasignal.ai/news/openai-s-decisions-api-gives-developers-a-constrained-gpt-6-luna-router", source: "AlphaSignal", date: "2026-09-29"}
- {id: 11, title: "Structured Outputs guide", url: "https://developers.openai.com/api/docs/guides/structured-outputs", source: "OpenAI docs"}
- {id: 12, title: "Using logprobs", url: "https://developers.openai.com/cookbook/examples/using_logprobs", source: "OpenAI Cookbook"}
- {id: 13, title: "GPT-6 Luna vs Jev vs Liquid D1 benchmark (issue #2)", url: "https://github.com/maciejczub/skill-siujev/issues/2", source: "GitHub", date: "2026-10-01"}
- {id: 14, title: "Clef: open-source decision models, and a new RL fine-tuning platform", url: "https://blog.cloudflare.com/clef-decision-models/", source: "Cloudflare blog", date: "2026-10-01"}
- {id: 15, title: "Cloudflare/clef model card", url: "https://huggingface.co/Cloudflare/clef", source: "Hugging Face", date: "2026-10-01"}
- {id: 16, title: "Cloudflare/clef-flash model card", url: "https://huggingface.co/Cloudflare/clef-flash", source: "Hugging Face", date: "2026-10-01"}
- {id: 17, title: "Workers AI pricing", url: "https://developers.cloudflare.com/workers-ai/platform/pricing/", source: "Cloudflare docs", date: "2026-10-02"}
- {id: 18, title: "Workers AI model: clef", url: "https://developers.cloudflare.com/workers-ai/models/clef/", source: "Cloudflare docs", date: "2026-10-02"}
- {id: 19, title: "Clef: Open-source decision models (discussion)", url: "https://news.ycombinator.com/item?id=49923692", source: "Hacker News", date: "2026-10-01"}
- {id: 20, title: "perplexity-ai/pplx-decider-v1-27b model card", url: "https://huggingface.co/perplexity-ai/pplx-decider-v1-27b", source: "Hugging Face", date: "2026-10-01"}
- {id: 21, title: "Perplexity API pricing", url: "https://docs.perplexity.ai/docs/getting-started/pricing", source: "Perplexity docs", date: "2026-10-02"}
- {id: 22, title: "Decisions API quickstart", url: "https://docs.perplexity.ai/docs/decisions/quickstart", source: "Perplexity docs", date: "2026-10-01"}
- {id: 23, title: "Aravind Srinivas: open-sourcing pplx-decider-27b", url: "https://x.com/AravSrinivas/status/2105774153903268288", source: "X", date: "2026-10-01"}
- {id: 24, title: "AutoJev", url: "https://github.com/denis-pplx/autojev", source: "GitHub (Denis Yarats)"}
- {id: 25, title: "autotrust/JEV-27B-VL model card", url: "https://huggingface.co/autotrust/JEV-27B-VL", source: "Hugging Face", date: "2026-10-01"}
- {id: 26, title: "Jev Decision Index (community Space) README", url: "https://huggingface.co/spaces/multimodalart/jev-decision-index/blob/main/README.md", source: "Hugging Face Spaces", date: "2026-09-28"}
- {id: 27, title: "decision-index kit", url: "https://github.com/sinanuozdemir/decision-index", source: "GitHub", date: "2026-09-27"}
- {id: 28, title: "Liquid AI d1 announcement thread", url: "https://threadreaderapp.com/thread/2105003472332693869.html", source: "Liquid AI via Thread Reader", date: "2026-09-29"}
- {id: 29, title: "Drex", url: "https://www.nace.ai/drex", source: "Nace", date: "2026-09-28"}
- {id: 30, title: "JevBench v1.4.2 release", url: "https://github.com/fstandhartinger/jevbench/releases/tag/v1.4.2", source: "GitHub", date: "2026-09-24"}
- {id: 31, title: "JevBench v1.5.4 — Jev-class models", url: "https://benchmarkheaven.com/jev-models", source: "Benchmark Heaven", date: "2026-10-02"}
- {id: 32, title: "Mimic E8 live run: decision-model challengers vs Jev", url: "https://github.com/punitarani/mimic/pull/48", source: "GitHub", date: "2026-10-01"}
- {id: 33, title: "Decision models benchmark (AIM-Decision)", url: "https://aimultiple.com/decision-models", source: "AIMultiple", date: "2026-10-01"}
- {id: 34, title: "Ollaya", url: "https://ollaya.dev/", source: "Ollaya", date: "2026-09-25"}
- {id: 35, title: "Jeff: Jev-compatible decision models", url: "https://github.com/firelex/jeff", source: "GitHub", date: "2026-10-01"}
- {id: 36, title: "convaiinnovations/laya model card", url: "https://huggingface.co/convaiinnovations/laya", source: "Hugging Face"}
- {id: 37, title: "MoritzLaurer/deberta-v3-large-zeroshot-v2.0", url: "https://huggingface.co/MoritzLaurer/deberta-v3-large-zeroshot-v2.0", source: "Hugging Face", date: "2024"}
- {id: 38, title: "knowledgator/gliclass-modern-large-v3.0", url: "https://huggingface.co/knowledgator/gliclass-modern-large-v3.0", source: "Hugging Face", date: "2025"}
- {id: 39, title: "Cohere Rerank on AWS Marketplace", url: "https://aws.amazon.com/marketplace/pp/prodview-6q7el2wk6xcmo", source: "AWS Marketplace"}
- {id: 40, title: "Jev after eight days of independent tests", url: "https://dev.to/aws-builders/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1c60", source: "DEV Community", date: "2026-09-24"}
- {id: 41, title: "Deußer, Sparrenberg, Sifa — zero-shot evaluation of Jev across 37 datasets", url: "https://arxiv.org/abs/2609.37647", source: "arXiv", date: "2026-09-29"}
- {id: 42, title: "Jeff – Jev-compatible 0.8B decision models (discussion)", url: "https://news.ycombinator.com/item?id=49883844", source: "Hacker News", date: "2026-09-28"}
- {id: 43, title: "Clef on Workers AI changelog", url: "https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/", source: "Cloudflare changelog", date: "2026-10-01"}
- {id: 44, title: "Diogo Almeida (@CompleteSkeptic) launch post", url: "https://x.com/CompleteSkeptic/status/2099925682726002904", source: "X", date: "2026-09-15"}
- {id: 45, title: "Vast.ai GPU spot prices (USD per GPU-hour)", url: "https://github.com/guzus/ai-research-arm/blob/main/research/market/gpu-spot.json", source: "ARA market lane", date: "2026-10-01"}
- {id: 46, title: "Perplexity Decisions API reference", url: "https://docs.perplexity.ai/api-reference/decisions-post", source: "Perplexity docs", date: "2026-10-01"}
- {id: 47, title: "OpenAI Decisions API vs Jev", url: "https://www.firecrawl.dev/blog/openai-decisions-api-vs-jev", source: "Firecrawl", date: "2026-09-30"}
- {id: 48, title: "NVIDIA H100 Tensor Core GPU specifications", url: "https://www.nvidia.com/en-us/data-center/h100/", source: "NVIDIA"}
- {id: 49, title: "Liquid d1 on OpenRouter", url: "https://openrouter.ai/liquid/d1", source: "OpenRouter", date: "2026-10-02"}
- {id: 50, title: "Liquid AI releases d1, a decision model that returns calibrated probabilities with zero output tokens", url: "https://www.marktechpost.com/2026/09/29/liquid-ai-releases-d1-a-decision-model-that-returns-calibrated-probabilities-with-zero-output-tokens/", source: "MarkTechPost", date: "2026-09-29"}
:::
