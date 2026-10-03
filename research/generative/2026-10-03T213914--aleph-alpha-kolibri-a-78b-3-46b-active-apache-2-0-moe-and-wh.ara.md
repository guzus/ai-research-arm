---
eyebrow: Deep Research · Open Models · European AI
title: "Kolibri's borrowed voice: a sovereign European MoE taught partly by Chinese models"
deck: Aleph Alpha's 78B / 3.46B-active Apache-2.0 model is genuinely built in Europe. Its synthetic training data is not. That is legal, documented and mostly manageable, but it changes what the word "sovereign" can honestly mean.
domain: general
lede: |
  On October 3, 2026, Germany's Unity Day, Heidelberg's Aleph Alpha released Kolibri-1, an English–German mixture-of-experts model with 78.1 billion total and 3.46 billion active parameters, under Apache 2.0, trained from scratch on 768 B200 GPUs in Germany and Finland. The launch post calls it "sovereign". The company's own EU AI Act filing, published the same day, lists seven models whose outputs became Kolibri training data. Five come from Chinese labs: two GLM checkpoints from Zhipu/Z.ai, Kimi-K2.6 from Moonshot, and two Qwen models from Alibaba. This report reconstructs which of those models did what, what the upstream licences and EU law actually say, whether political bias can travel through generated text, and what is left of the sovereignty claim once the provenance chain is drawn honestly.
stats:
  - {label: Total params, value: "78.1B", note: "384 experts, top-6 + 1 shared"}
  - {label: Active per token, value: "3.46B", note: "4.4% of total"}
  - {label: Synthetic SFT tokens, value: "174B", note: "of a 268B SFT mix"}
  - {label: Chinese generators named, value: "5 of 7", note: "EU training summary §2.5"}
---

:::kv
- {term: "Is Kolibri a real from-scratch European model?", def: "Yes. It was pre-trained from random initialization on 20T tokens, on 768 B200s in Germany and Finland, by a German company [^1,2]."}
- {term: "Did Chinese models generate its training data?", def: "Yes, by Aleph Alpha's own disclosure. The EU filing names GLM-5.3, GLM-5.2-fp8, Kimi-K2.6, Qwen3-32B and Qwen3.8-27B as generators, and the model card says the data 'contains material generated with Chinese language models' [^3,1]."}
- {term: "Which stage did they shape?", def: "Pre-training rephrasing used Gemma-4 (US) and Mistral-NeMo (EU/US). Qwen3-32B was a quality judge. The GLM, Kimi and Qwen3.8 checkpoints have no stated role, but the 174B-token synthetic SFT set is the only large generation step left. That points to post-training, though this is an inference, not a disclosure [^1,2,4]."}
- {term: "Is that illegal or a licence problem?", def: "No. EU law requires disclosure, not exclusion. All seven generator licences are Apache-2.0, MIT or MIT-style and say nothing about using outputs [^11,12,13,14]."}
- {term: "So is 'sovereign' accurate?", def: "For jurisdiction, compute, team and weight control, mostly yes. For epistemic provenance, meaning where the model learned how to answer, no. Some of its teachers come from labs legally required to uphold 'core socialist values' [^25]."}
:::

## 01. What Aleph Alpha actually shipped

Kolibri is a small-active, wide-sparse MoE built to be cheap to serve on-premises. The engineering is serious, even though its capability is mid-tier. The model card gives exact counts: 78,103,074,560 total and 3,457,573,120 active parameters across 50 layers, with 384 routed experts per layer, top-6 sigmoid routing and one shared expert [^1]. Attention is hybrid. Four of every five layers use a 512-token sliding window, and only one in five uses global grouped-query attention, which is what makes long contexts cheap to hold in KV cache [^1].

:::kv
- {term: Architecture, def: "50-layer MoE, 4:1 sliding-window : GQA, 384 routed experts, top-6 + 1 shared [^1]"}
- {term: Context, def: "262,144 native; 1,048,576 by extrapolation; card recommends ≤262,144 for serving [^1]"}
- {term: Pre-training data, def: "20T tokens, ~62.5% English, ~23.9% German, ~13.6% code; +3.44T mid-training, +201B long-context [^1]"}
- {term: Compute, def: "768 B200 for 21 days (392k GPU-h) pre-training; 6.4e23 FLOPs total; ~950 MWh [^1]"}
- {term: Precision, def: "FP8 e4m3fn weights (~78 GB); BF16 variant also published [^1,7]"}
- {term: Minimum hardware, def: "2× A100 80GB, 2× H100 SXM5, or 1× H200 / B200 / B300 [^1]"}
- {term: Licence, def: "Apache 2.0, for weights and config files only [^1]"}
:::

The size was a serving-cost decision. Aleph Alpha says scaling from 32B to 123B kept improving quality. But a 123B variant could handle only 3 concurrent 256k-token queries on two H100s, while the 78B handles 18 and decodes 28% faster [^2]. That 6× concurrency gap is the economic case for sparse experts in a market where customers want to run the model on their own hardware.

:::compare
- {role: "123B VARIANT", name: "3 concurrent 256k queries", value: "2× H100"}
- {role: "SHIPPED 78B", name: "18 concurrent 256k queries", value: "+28% decode"}
- {role: SUBJECT, name: "Kolibri-1 (78B / 3.46B active)", value: "6× concurrency"}
:::

The licence is narrower than "Apache 2.0" suggests. The card says the rights "only apply to the weights and configuration files published in this repository" and do "not extend to underlying code, model architecture, parameter settings or any training method" [^1]. You can run, fine-tune and redistribute the weights. You cannot reproduce the pipeline, because the training code and most of the data mix stay private.

**Counterpoint:** two claims in the launch materials need qualifying. The "1M context" figure is an extrapolation, and the longest trained stage is 256k [^1,40]. And the German share is 21.3% of pre-training tokens in the blog but 23.9% on the card and in the EU summary, probably because they count different stages [^2,1,3].

**Why it matters:** the design is optimized for a regulated buyer running a GPU or two in their own building. That buyer cares about provenance more than leaderboard rank, so the rest of this report focuses on provenance.

## 02. The provenance chain: who generated what

Kolibri's synthetic data comes from three layers. The first is Aleph Alpha's own rephrasing with Western models. The second is post-training generation, where the named Chinese checkpoints are the only candidates without a stated role. The third is inherited NVIDIA datasets, which are themselves mostly Qwen- and DeepSeek-generated.

### Layer 1: what is documented by role

The pre-training documentation is precise. "Deduplicated English Common Crawl was rephrased with Gemma-4-26B-A4B," a Google model [^1]. German web documents were rewritten with Mistral-Nemo-Instruct-2407, which produced roughly 1.1T unique tokens, the single largest German source [^4]. Qwen3-32B was the judge. It scored a 1M-document English sample with more than 20 prompts, and those labels trained cheaper quality classifiers [^4]. Aleph Alpha says about 24% of pre-training data (4.8T tokens) is synthetic [^4].

| Generator | Developer (country) | Documented role | Certainty |
|---|---|---|---|
| Gemma-4-26B-A4B | Google (US) | English CC rephrasing (pre-training) | Stated [^1] |
| Mistral-Nemo-12B | Mistral/NVIDIA (FR/US) | German rewriting (pre-training) | Stated [^4] |
| Qwen3-32B | Alibaba (CN) | LLM judge for quality-classifier labels | Stated [^4] |
| *GLM-5.3 | Zhipu / Z.ai (CN) | Listed generator; role undisclosed | Listed only [^3] |
| *GLM-5.2-fp8 | Zhipu / Z.ai (CN) | Listed generator; role undisclosed | Listed only [^3] |
| *Kimi-K2.6 | Moonshot (CN) | Listed generator; role undisclosed | Listed only [^3] |
| *Qwen3.8-27B | Alibaba (CN) | Listed generator; role undisclosed | Listed only [^3] |

:::stack-bar(legend=true)
- {label: "Chinese labs (GLM ×2, Kimi, Qwen ×2)", pct: 71.4}
- {label: "US (Gemma-4)", pct: 14.3}
- {label: "EU (Mistral-NeMo)", pct: 14.3}
:::

:::source
Share of the seven synthetic-data generator models named in Kolibri's EU AI Act training-content summary, by developer origin. Count-weighted, not token-weighted [^3].
:::

### Layer 2: the post-training gap

The four highlighted rows are the story. The EU AI Act summary, section 2.5, lists GLM-5.3, GLM-5.2-fp8, Kimi-K2.6 and Qwen3.8-27B as generator models but attaches no purpose to any of them [^3]. The template defines the category as training "directly on the outputs of another AI model", "in particular through model distillation or model alignment", and that wording is reproduced in Kolibri's filing [^3]. Meanwhile, the launch post says Aleph Alpha "generated a total of 174B tokens worth of synthetic data" for SFT inside a 268B-token mix [^2]. The card adds that for agentic SFT datasets "we regenerated the reasoning traces," and that 10.6B tokens of German reasoning data were generated from translated prompts [^1].

The German-reasoning post from September 24 describes the method without naming models. It "utilize[s] several open-source teacher models that we have found to be proficient in German" [^6]. Prefilling the teacher's thinking with a German opener kept 97% of 12,627 traces in German, against 67% of 8,721 with a system prompt alone, and the final set was 795,731 samples [^6].

:::slope(left-label="System prompt", right-label="Reasoning prefill", unit=%)
| Method | System prompt | Reasoning prefill |
|---|---|---|
| Traces staying German | 67 | 97 |
:::

So the teacher distillation is documented. The specific teachers are not. By elimination, the three pre-training generators already have stated jobs, which leaves GLM-5.3, GLM-5.2, Kimi-K2.6 and Qwen3.8-27B as the likeliest SFT teachers. They are also the strongest models on the list, and this inference is what lies behind the "GLM/Qwen-generated fine-tuning data" framing. ==It is an inference: no Aleph Alpha document seen for this report assigns those models to SFT.== The model card does state the conclusion that matters, without naming names: "Our model's training data also contains material generated with Chinese language models which are known to carry bias toward certain political positions" [^1].

### Layer 3: inherited datasets

The third layer is less discussed and larger. The EU summary lists NVIDIA Nemotron-CC-v2, v2.1, Nemotron-Pretraining-SFT-v1 and Nemotron-Pretraining-Specialized-v1 among the public datasets Aleph Alpha filtered and used in part [^3]. Per the tech report, 64.3% of Kolibri's pre-training tokens (12.85T) came from external sources, against 35.7% (7.15T) from Aleph Alpha's own pipeline [^4]. The Nemotron cards are explicit about their own generators. In Nemotron-CC-v2.1, about 2,448.5B of 2,544.8B tokens are synthetic or translated output of Qwen3-30B-A3B [^8]. NVIDIA's separate post-training dataset is 95.9% DeepSeek-R1-0528 output (24,602,969 of 25,659,642 rows) [^9].

:::bars
- {label: "Nemotron-CC-v2.1 tokens from Qwen3-30B-A3B", value: "96.2%", pct: 96.2}
- {label: "Nemotron Post-Training v1 rows from DeepSeek-R1-0528", value: "95.9%", pct: 95.9}
- {label: "Kolibri pre-training tokens from external sources", value: "64.3%", pct: 64.3}
- {label: "Kolibri pre-training tokens that are synthetic", value: "~24%", pct: 24}
:::

:::note
Kolibri used unspecified filtered subsets of the Nemotron sets, so these bars show exposure, not the Chinese-generated share of Kolibri's corpus. Nemotron-Post-Training-v1 is shown as an industry reference and is not on Kolibri's dataset list [^3,8,9].
:::

**Counterpoint:** "Chinese-generated" does not mean Chinese content. The Nemotron-CC synthetic subsets are rephrasings seeded from Common Crawl pages, so the source facts come from the web and the wording comes from Qwen [^8]. In this analysis, the political risk sits mostly in open-ended chat and reasoning answers, not in rephrased encyclopedic or math text.

**Why it matters:** the honest description is not "a European model contaminated by China". It is a European model built from the same open supply chain everyone uses, and that supply chain runs largely through Chinese open weights.

## 03. Can political bias travel through generated text?

Yes, measurably, but narrowly. The mechanism is the text itself, not hidden signals, and for a from-scratch model like Kolibri the risk can be filtered rather than being structural.

The upstream motive is regulatory. China's 2023 Interim Measures for generative AI, Article 4, require services to "坚持社会主义核心价值观" (uphold core socialist values) and not generate content that "damages the national image" [^25]. That shows up in weights, not just API filters. NIST's CAISI evaluated DeepSeek models and found they "echoed four times as many inaccurate and misleading CCP narratives as U.S. reference models did" [^26]. For Kimi K2 Thinking, CAISI found heavy censorship in Chinese but much less in English, a language gap that matters for an English–German student [^27].

Aleph Alpha published its own measurement five days before launch. Its 967-prompt, 56-topic benchmark, judged by GPT-OSS-120B, found "six Chinese models answered only 17 to 41 percent of prompts in a balanced way" [^5].

:::rank-list
- {label: "Kimi K3", value: "41% balanced", pct: 41}
- {label: "Kimi K2.5", value: "37% balanced", pct: 37}
- {label: "DeepSeek R1-0528", value: "22% balanced", pct: 22}
- {label: "Qwen 3.8 (2.4T-A95B)", value: "19% balanced", pct: 19}
- {label: "DeepSeek V4 Pro", value: "18% balanced", pct: 18}
- {label: "Qwen 3.6 35B-A3B", value: "17% balanced", pct: 17}
:::

:::source
Aleph Alpha, "Training on the party line", 2026-09-28. Share of China-sensitive prompts answered in a balanced way, LLM-judged. GLM was not tested [^5].
:::

The same post gives the key transfer evidence. NVIDIA's Nemotron Cascade 2 is a US-pretrained base whose SFT data was "generated largely with DeepSeek and Qwen". Only about 3.5k of its 9.3M chat rows carried CCP talking points, yet the model "was flagged on 17 percent of prompts" [^5]. That is a non-Chinese base model picking up the slant through a 0.04% slice of SFT data.

:::callout(kind=warn, label="Transfer is real")
A tiny share of tainted SFT rows was enough to show up clearly in a model with a different base. Small contamination rates can still matter in post-training, because SFT shapes how the model answers [^5].
:::

What does *not* obviously transfer is the hidden kind of bias. Anthropic-affiliated researchers showed in 2025 that traits can pass through semantically unrelated data ("subliminal learning"). But they report "we do not observe the effect when the teacher and student have different base models" [^28]. Kolibri was initialized from scratch, so the residual channel is the visible content of answers, which a filter can inspect. Filtering has a known weak spot, though. A 2026 preprint found newer Qwen generations dropped refusals to zero while increasing narrative steering, so filters that look for refusals or keywords miss framing bias [^29].

Aleph Alpha's mitigation, as stated: "we screen SFT data for Chinese political biases… filter out all flagged rows and add dedicated political alignment data to the mix" [^5]. The card adds that all data was filtered for "political bias potentially inherited from generator models" and that alignment data was centred on "human dignity, universal human rights, liberal democracy" [^1].

**Counterpoint:** no before/after score for Kolibri on the 967-prompt benchmark has been published, and the card concedes the model "may reproduce political biases present in its training data in some contexts" [^1]. Until a third party runs a CAISI-style evaluation, the mitigation is a plausible claim, not a measured one.

**Why it matters:** for a German ministry, the worry is not that Kolibri will praise the CCP. It is subtle framing on China, Taiwan or Xinjiang that a 0.04% data slice proved capable of producing in another model. That can be tested, and it should be tested before procurement.

## 04. Licences: clean on paper, with three soft spots

None of the seven generator licences restricts what you do with outputs, so Kolibri's Apache-2.0 grant is not legally encumbered by its teachers. The exposure lies in API terms, ambiguous "derivative" language and reputation.

| Generator | Licence | Output / training clause | Extra condition |
|---|---|---|---|
| Gemma-4-26B-A4B | Apache 2.0 | None [^14] | — |
| Qwen3-32B, Qwen3.8-27B | Apache 2.0 | None | — |
| Mistral-Nemo-Instruct-2407 | Apache 2.0 | None | — |
| GLM-5.2-FP8 | MIT | None [^13] | — |
| GLM-5.3 | MIT-style custom | None on outputs [^12] | Security review for MaaS firms with >$10B revenue [^12] |
| *Kimi-K2.6 | Modified MIT | None on outputs [^11] | Display "Kimi K2.6" above 100M MAU or $20M/month revenue [^11] |

The Kimi clause binds commercial products using "the Software (or any derivative works thereof)" above the thresholds, which must "prominently display 'Kimi K2.6'" [^11]. "Derivative works" is undefined. Under ordinary copyright reading, a model trained from scratch on generated text is not a derivative of the generator's weights, and Aleph Alpha's roughly 200-person company is nowhere near $20M a month [^35]. The risk is low, but not zero, and the card's blanket line that it "generated synthetic data using permissively-licensed LLMs" glosses over a licence that is not plain MIT [^1].

The sharper edge is contractual. If generation went through hosted APIs rather than self-hosted weights, Z.ai's terms bar using "model-generated content for the development, training, labeling, fine-tuning" of external models without authorization [^15]. Moonshot's platform terms prohibit building "models that have potential competitive possibilities" [^16]. Aleph Alpha's filing links Hugging Face weight repositories, not APIs, which points to self-hosting, but it does not say so [^3].

:::callout(kind=info, label="Reputational irony")
Moonshot, the developer of Kimi-K2.6, is one of three Chinese labs (with DeepSeek and MiniMax) that Anthropic accused in February 2026 of distilling Claude. The campaign used roughly 24,000 fraudulent accounts and "over 16 million exchanges" [^17]. Nothing ties the Kimi checkpoint Kolibri used to that activity. But if the accusation is right, part of a "sovereign" model's teaching data is two distillation hops from a US frontier lab's outputs.
:::

**Counterpoint:** the NVIDIA dataset cards flag that models trained on them "may be subject to redistribution and use requirements" of the Qwen, DeepSeek and Phi-4 licence agreements [^8]. Kolibri used those datasets [^3]. Since Qwen and DeepSeek weights are permissively licensed, this is a notice obligation rather than a restriction. Still, it is a licence trail the model card does not mention.

**Why it matters:** sovereign buyers often require a clean IP chain. Kolibri's chain is clean enough to pass a lawyer's review, but the card describes it as tidier than it is.

## 05. What EU law asks, and what it doesn't

EU law treats outputs from Chinese models as a disclosure item, not a prohibited input. On disclosure, Kolibri's filing is unusually complete.

Article 53(1)(d) of the AI Act requires every general-purpose model provider to publish "a sufficiently detailed summary about the content used for training" [^18]. The open-source exemption in Article 53(2) removes only the technical-documentation duties in points (a) and (b). Open-weight providers must still keep a copyright policy and publish the training-content summary [^18,20]. The Commission's template, published July 24, 2025, has a section 2.5 on synthetic data that asks which models generated it. It asks nothing about the generator's jurisdiction [^20].

Compute keeps Kolibri out of the heavy regime. Systemic risk is presumed above 10^25 training FLOPs [^19]. At 6.4e23, Kolibri sits at 6.4% of the line [^1,19], roughly a tenth of the ~6.7e24 reported for Switzerland's Apertus-70B [^54].

:::bar-chart(title="Training compute vs. the AI Act systemic-risk line", orientation=horizontal, value-suffix="e23 FLOPs")
categories: Kolibri-1, Apertus-70B, AI Act threshold, Llama 3.1 405B
Training compute: 6.4, 67.4, 100, 380
:::

:::source
Kolibri model card; Apertus technical report (reported figure); Regulation (EU) 2024/1689 Art. 51; Meta Llama 3 paper. Values in units of 10^23 FLOPs [^1,54,19,47].
:::

:::timeline
- {date: 2023-08-15, headline: "China's generative-AI measures take effect", body: "Article 4 requires services to uphold core socialist values."}
- {date: 2024-06-13, headline: "EU AI Act adopted", body: "Art. 53 GPAI duties; Art. 51 sets the 10^25 FLOP systemic-risk presumption."}
- {date: 2025-07-24, headline: "Commission training-summary template", body: "Section 2.5 asks providers to name models used to generate synthetic data."}
- {date: 2025-08-02, headline: "GPAI obligations apply", body: "New models must publish the summary when placed on the market."}
- {date: 2026-08-02, headline: "AI Office enforcement powers start", body: "Fines up to 3% of turnover or €15M for GPAI non-compliance."}
- {date: 2026-10-03, headline: "Kolibri-1 placed on the EU market", body: "Summary v1.0 lists five Chinese-developed generators."}
:::

The timeline entries draw on the CAC measures, the AI Act articles and the Commission FAQ [^25,18,19,20,3].

Kolibri's disclosure goes beyond the minimum. The filing names all seven generators with links [^3], and Aleph Alpha is on the Commission's Code of Practice signatory list, while Zhipu, Moonshot and Alibaba are not [^21]. One inconsistency stands out: the same document declares "Model dependencies: None" while listing seven generator models [^3]. That field is about weight lineage, so the answer is technically right but easy to misread.

Nothing in national practice changes the picture. Germany's Deutschland-Stack sets a procurement preference for "Open Source Lösungen oder Lösungen europäisch souveräne Anbieter" and states "für generative KI gibt es aktuell keine spezifischen Standards" [^23]. The 2025 actions against DeepSeek targeted unlawful transfers of personal data to China through a hosted app [^24]. Generating text offline from self-hosted weights sends no personal data anywhere.

**Counterpoint:** disclosure without roles is only half useful. Section 2.5 shows a German buyer that GLM and Kimi were used, not whether they wrote 10 million tokens of chat answers or 10 billion. A stricter reading of "sufficiently detailed" could ask for role and volume per generator.

**Why it matters:** Kolibri is legally compliant and more transparent than most peers. The sovereignty debate is therefore a procurement and branding question, not an enforcement one.

## 06. Capability: where Kolibri sits

On Aleph Alpha's own harness, Kolibri beats the spring-2026 sparse models it chose to compare against on math and reasoning. It trails on agentic coding, and it loses nearly every row to a dense Qwen model of similar memory footprint, which also appears on Kolibri's own list of synthetic-data generators.

:::bar-chart(title="Vendor-harness scores, post-trained models (EN)", orientation=vertical, mode=grouped)
categories: AIME 2025, GPQA Diamond, LiveCodeBench v6, SWE-Bench Verified, IFBench
Kolibri (3.46B act.): 96.9, 84.3, 85.9, 66.4, 78.1
Nemotron 3 Super (12B act.): 91.7, 78.0, 82.0, 60.2, 73.7
Qwen3.6 35B-A3B: 84.6, 83.4, 82.5, 73.8, 66.1
Qwen3.8 27B (dense): 97.9, 89.2, 93.8, 72.6, 81.9
:::

:::source
Aleph Alpha Kolibri-1 model card and launch blog, 2026-10-03; all models run on Aleph Alpha's own harness at highest reasoning effort [^1,2].
:::

The headline averages make the point. Kolibri scores 75.5 English and 70.8 German overall. Nemotron 3 Super scores 73.0 / 67.9, Qwen3.6-35B-A3B 71.4 / 67.3, and dense Qwen3.8 27B 80.2 / 79.9 [^1,2].

:::slope(left-label="Overall EN", right-label="Overall DE")
| Model | Overall EN | Overall DE |
|---|---|---|
| Qwen3.8 27B (dense) | 80.2 | 79.9 |
| Kolibri-1 | 75.5 | 70.8 |
| Nemotron 3 Super | 73.0 | 67.9 |
| Qwen3.6 35B-A3B | 71.4 | 67.3 |
:::

Independent readers have been sceptical. Trending Topics noted "all three comparison models date from the spring" and that newer GLM-5.3, Kimi K3, Qwen3.8-family and MiMo-V2.6-Pro releases are absent [^38]. Tejas Kumar summarized Kolibri's abstention strength with "It knows when it doesn't know, which is great, but it also knows less" [^39]. Qwen's own card for Qwen3.8-Flash-Next reports GPQA 91.7 and LiveCodeBench 91.9 at 6B active, against Kolibri's 84.3 and 85.9 [^44]. On the claim that Kolibri "matches" Nemotron 3 Super, the vendor's own card shows it ahead on math and code but behind on TerminalBench 2.1 (27.7 vs 39.7) [^1].

Deployment is early. On day two, Hugging Face Transformers support was still an open issue, and the model needs Aleph Alpha's own vLLM plugin [^42,41]. One DGX Spark user measured about 47 tokens per second for a single request [^41].

**Counterpoint:** there is no independent reproduction yet [^40]. Harness drift of 2–3 points on comparators is the same size as several of Kolibri's leads, so the ranking among the 3–12B-active MoEs is within noise in places [^44,1].

**Why it matters:** the capability argument sharpens the sovereignty dilemma. If a dense Qwen model that helped teach Kolibri still beats it, then the case for Kolibri has to rest on provenance, control and German fluency, not on raw scores.

## 07. The company behind the bird

Kolibri arrives as Aleph Alpha is being absorbed into a Canadian company. "Sovereign" here describes the model's training conditions, not the long-term ownership of its maker.

:::timeline
- {date: 2023-11-06, headline: "'More than $500M' Series B", body: "Led by Ipai, Bosch Ventures and Schwarz Group companies."}
- {date: 2024-08-26, headline: "PhariaAI launch", body: "Pivot to a model-agnostic stack orchestrating third-party LLMs."}
- {date: 2024-09-05, headline: "Founder: an LLM alone is not a business", body: "Andrulis tells Bloomberg a European LLM alone doesn't justify the investment."}
- {date: 2026-01-08, headline: "About 50 roles cut", body: "After a strategy review by the new leadership team."}
- {date: 2026-04-24, headline: "Planned combination with Cohere", body: "Schwarz Group to lead a €500M structured financing for Cohere."}
- {date: 2026-09-16, headline: "Definitive agreement", body: "Combined firm to operate as Cohere; closing subject to regulators."}
- {date: 2026-10-03, headline: "Kolibri-1 released", body: "Apache-2.0, 78B / 3.46B active."}
:::

The timeline draws on the company's announcements and contemporaneous reporting [^30,33,32,36,37,34,2].

The 2023 round was announced as "more than 500 million US Dollars" [^30]. The company later broke a €470M package into €110M of equity, €300M of research funding and €60M of order commitments [^31]. In 2024 founder Jonas Andrulis said "Just having an European LLM is not sufficient as a business model" [^32]. PhariaAI then repositioned the company around "evaluating, adapting and orchestrating different proprietary and open-source LLMs" [^33].

:::donut(center-label="€470M")
- {label: "Research funding (€300M)", value: 63.8}
- {label: "Equity (€110M)", value: 23.4}
- {label: "Order commitments (€60M)", value: 12.8}
:::

The definitive agreement with Cohere, signed September 16, 2026, says the unified company will operate "globally as Cohere" with dual headquarters in Berlin and Toronto and a Heidelberg research centre. Co-CEO Ilhan Scheer would become Cohere COO and co-founder Samuel Weinbach Cohere's Chief Research Officer [^34]. Co-CEO Reto Spörri left on September 28, leaving Scheer as sole CEO [^35]. The deal announcement does not mention Kolibri [^34].

**Counterpoint:** a Canada–Germany combination with Schwarz Group's STACKIT as the cloud backbone can still be sovereign in the procurement sense, because the hosting, contracts and legal jurisdiction stay European [^34]. And Apache-2.0 weights cannot be withdrawn once downloaded. That is the strongest version of sovereignty Kolibri offers.

**Why it matters:** a buyer choosing Kolibri for "sovereignty" is buying weights they control, not a commitment that a German lab will keep training successors.

## 08. Redefining "sovereign" so it means something

No official definition requires training-data independence. Taken literally, that standard would disqualify every competitive European open model, so the useful move is to split the word into layers and grade each one.

The EU AI Office's expert findings frame sovereignty as the ability to "access, select, control, and benefit from frontier AI models" [^22]. The Commission's Apply AI strategy promotes "a 'buy European' approach, particularly for the public sector, with a focus on open source AI solutions" [^53]. NVIDIA's framing stresses models "trained and fine-tuned with local data, hosted and run on local infrastructure, subject only to local laws" [^52]. None of these mention distillation. Other European projects show the same dependency. Apertus generated alignment completions with Llama and Qwen models [^54], and EuroLLM-22B regenerated responses "using several open models" [^46].

| Sovereignty layer | Kolibri grade | Evidence |
|---|---|---|
| Jurisdiction of training | {flag:green} Strong | Germany and Finland, "under European and German law" [^2] |
| Control of weights | {flag:green} Strong | Apache 2.0, self-hostable on one H200/B200 [^1] |
| Regulatory transparency | {flag:green} Strong | Seven generators named in the EU summary; Code signatory [^3,21] |
| Pipeline reproducibility | {flag:yellow} Partial | Licence excludes code and training methods [^1] |
| Data provenance | {flag:yellow} Partial | 64.3% external tokens; Qwen/DeepSeek-heavy Nemotron inputs [^4,8] |
| Epistemic provenance (who taught it to answer) | {flag:red} Weak | Five of seven generators are Chinese; SFT teachers unnamed [^3,6] |
| Corporate continuity | {flag:yellow} Partial | Merging into Cohere, pending approval [^34] |

German enterprise demand points the same way. A Bitkom survey of German firms using AI found DeepSeek at 2% and Qwen at 1% usage, against 76% for ChatGPT [^51]. Buyers are not choosing Chinese models directly. Kolibri means some Chinese-model output reaches them indirectly, through a German product.

:::statement(attr="ARA Research")
Sovereignty over the weights is not the same as sovereignty over the knowledge. Kolibri delivers the first in full and the second only as far as its filters do.
:::

**Counterpoint:** epistemic provenance may be the wrong frame entirely. Synthetic data is a tool, like a dictionary. The student learns from text the teacher wrote, not from the teacher's values, and Aleph Alpha filtered and counter-aligned that text [^5]. On this view, demanding EU-only teachers would only lock Europe into weaker models, which is a worse sovereignty outcome.

**Why it matters:** procurement offices can make this concrete. They can ask for per-generator roles and token counts, and an independent CCP-narrative evaluation before deployment. Those requests are cheap, and Aleph Alpha already has the benchmark to answer them [^5].

## 09. What could break this analysis

The thesis is that Kolibri is genuinely European-built and legally clean, but its post-training was likely taught partly by Chinese models and its bias mitigation is unmeasured publicly. Five things could overturn it.

1. **The SFT teachers are not who we infer.** If the tech report's post-training section assigns GLM-5.3, Kimi-K2.6 and Qwen3.8-27B only to minor tasks, such as translation or prompt generation, the "Chinese-taught" framing weakens a lot. The card's admission of Chinese-generated material would still stand [^1,3]. The report's later sections were not machine-readable for this analysis [^4].
2. **Published bias numbers.** A Kolibri score near Western baselines on Aleph Alpha's 967-prompt benchmark, or on a NIST-style evaluation, would show the filtering worked [^5,26].
3. **API rather than weights.** If generation used Z.ai or Moonshot APIs, the licence picture moves from "clean" to "breach of contract", because both sets of terms prohibit competitive training [^15,16].
4. **Independent benchmarks.** Third-party runs could move Kolibri up or down the 3–12B-active pack. Every number here comes from Aleph Alpha's own harness [^40].
5. **The Cohere integration.** If Kolibri is retired in favour of Cohere's own models after the deal closes, the question becomes moot for future buyers [^34].

:::callout(kind=success, label="Red-team pass")
Red-team pass: 3/3 top claims unbroken. An adversarial review searched for evidence against the Chinese generators listed in the EU filing, the 174B-token synthetic SFT set, and the 17–41% balanced-answer range, and found none. The one open caveat is that the tech report's SFT section could not be machine-read, so a named-teacher disclosure there cannot be ruled out.
:::

:::references
- {id: 1, title: "Aleph-Alpha/Kolibri-1 model card", url: "https://huggingface.co/Aleph-Alpha/Kolibri-1", source: Hugging Face (Aleph Alpha), date: "2026-10-03"}
- {id: 2, title: "Kolibri Has Landed: A Sovereign Open-Weight Model", url: "https://aleph-alpha.com/en/blog/kolibri-has-landed-a-sovereign-open-weight-model/", source: Aleph Alpha blog, date: "2026-10-03"}
- {id: 3, title: "Kolibri 1 - Sufficiently Detailed Summary (EU AI Act public summary of training content)", url: "https://aleph-alpha.com/downloads/Kolibri_1_-_Sufficiently_Detailed_Summary.pdf", source: Aleph Alpha, date: "2026-10-03"}
- {id: 4, title: "Kolibri: A Sovereign European Model on the Pareto Frontier (technical report)", url: "https://aleph-alpha.com/downloads/tech-report.pdf", source: Aleph Alpha, date: "2026-10-03"}
- {id: 5, title: "Training on the party line", url: "https://aleph-alpha.com/en/blog/training-on-the-party-line/", source: "Aleph Alpha blog (Bastian Boll)", date: "2026-09-28"}
- {id: 6, title: "Through the valley of tears: cold-starting German reasoning in LLMs", url: "https://aleph-alpha.com/en/blog/through-the-valley-of-tears-cold-starting-german-reasoning-in-llms/", source: "Aleph Alpha blog (Finken, Thel)", date: "2026-09-24"}
- {id: 7, title: "Aleph-Alpha/Kolibri-1-BF16 model card", url: "https://huggingface.co/Aleph-Alpha/Kolibri-1-BF16", source: Hugging Face, date: "2026-10-03"}
- {id: 8, title: "nvidia/Nemotron-CC-v2.1 dataset card", url: "https://huggingface.co/datasets/nvidia/Nemotron-CC-v2.1", source: Hugging Face (NVIDIA), date: "2025-12-15"}
- {id: 9, title: "nvidia/Nemotron-Post-Training-Dataset-v1 dataset card", url: "https://huggingface.co/datasets/nvidia/Nemotron-Post-Training-Dataset-v1", source: Hugging Face (NVIDIA), date: "2025"}
- {id: 10, title: "nvidia/Nemotron-Pretraining-SFT-v1 dataset card", url: "https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-SFT-v1", source: Hugging Face (NVIDIA), date: "2025-08-18"}
- {id: 11, title: "Kimi-K2.6 LICENSE (Modified MIT)", url: "https://huggingface.co/moonshotai/Kimi-K2.6/blob/main/LICENSE", source: Moonshot AI, date: "2026"}
- {id: 12, title: "GLM-5.3 LICENSE", url: "https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE", source: Z.ai, date: "2026"}
- {id: 13, title: "GLM-5.2-FP8 model card", url: "https://huggingface.co/zai-org/GLM-5.2-FP8", source: Z.ai, date: "2026"}
- {id: 14, title: "Gemma 4 license", url: "https://ai.google.dev/gemma/docs/gemma_4_license", source: Google, date: "2026-04-01"}
- {id: 15, title: "Z.ai Terms of Service", url: "https://chat.z.ai/legal-agreement/terms-of-service", source: Z.ai, date: "2026-04-14"}
- {id: 16, title: "Kimi platform model use agreement", url: "https://platform.kimi.ai/docs/agreement/modeluse", source: Moonshot AI, date: "2026-07-30"}
- {id: 17, title: "Detecting and preventing distillation attacks", url: "https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks", source: Anthropic, date: "2026-02-23"}
- {id: 18, title: "AI Act Article 53: Obligations for providers of general-purpose AI models", url: "https://artificialintelligenceact.eu/article/53/", source: "Regulation (EU) 2024/1689", date: "2024-06-13"}
- {id: 19, title: "AI Act Article 51: Classification of GPAI models with systemic risk", url: "https://artificialintelligenceact.eu/article/51/", source: "Regulation (EU) 2024/1689", date: "2024-06-13"}
- {id: 20, title: "Guidelines and template for the public summary of training content for GPAI models (FAQ)", url: "https://digital-strategy.ec.europa.eu/en/faqs/guidelines-and-template-public-summary-training-content-general-purpose-ai-models", source: European Commission, date: "2025-07-24"}
- {id: 21, title: "The General-Purpose AI Code of Practice: signatories", url: "https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai", source: European Commission, date: "2026-07-31"}
- {id: 22, title: "AI Office frontier AI expert findings on competitiveness, sovereignty and security; Apply AI Strategy", url: "https://digital-strategy.ec.europa.eu/en/library/ai-office-publishes-frontier-ai-expert-findings-eu-competitiveness-sovereignty-and-security", source: European Commission, date: "2026-07-15"}
- {id: 23, title: "Deutschland-Stack: Gesamtbild", url: "https://deutschland-stack.gov.de/gesamtbild/", source: German Federal Government, date: "2026-01"}
- {id: 24, title: "Berliner Datenschutzbeauftragte meldet KI-App DeepSeek bei Apple und Google als rechtswidrigen Inhalt", url: "https://www.datenschutz-berlin.de/pressemitteilung/berliner-datenschutzbeauftragte-meldet-ki-app-deepseek-in-deutschland-bei-apple-und-google-als-rechtswidrigen-inhalt/", source: Berlin Commissioner for Data Protection, date: "2025-06-27"}
- {id: 25, title: "Interim Measures for the Management of Generative AI Services", url: "https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm", source: Cyberspace Administration of China, date: "2023-07-13"}
- {id: 26, title: "CAISI evaluation of DeepSeek AI models finds shortcomings and risks", url: "https://www.nist.gov/news-events/news/2025/09/caisi-evaluation-deepseek-ai-models-finds-shortcomings-and-risks", source: NIST, date: "2025-09-30"}
- {id: 27, title: "CAISI evaluation of Kimi K2 Thinking", url: "https://www.nist.gov/news-events/news/2025/12/caisi-evaluation-kimi-k2-thinking", source: NIST, date: "2025-12-12"}
- {id: 28, title: "Subliminal Learning: language models transmit behavioral traits via hidden signals in data", url: "https://arxiv.org/abs/2507.14805", source: arXiv, date: "2025-07-20"}
- {id: 29, title: "Refusal to narrative steering in Chinese LLMs (arXiv 2603.18280v3)", url: "https://arxiv.org/html/2603.18280v3", source: arXiv, date: "2026-05-01"}
- {id: 30, title: "Aleph Alpha raises a total investment of more than half a billion US Dollars", url: "https://aleph-alpha.com/en/news/half-billion-dollar-investment-round/", source: Aleph Alpha, date: "2023-11-06"}
- {id: 31, title: "Deutsches KI-Start-up Aleph Alpha differenziert 500-Millionen-Investitionspaket aus", url: "https://the-decoder.de/deutsches-ki-start-up-aleph-alpha-differenziert-500-millionen-investitionspaket-aus/", source: The Decoder, date: "2024-06-27"}
- {id: 32, title: "Aleph Alpha quits AI model race", url: "https://the-decoder.com/aleph-alpha-quits-ai-model-race/", source: The Decoder (citing Bloomberg), date: "2024-09-06"}
- {id: 33, title: "PhariaAI launch", url: "https://aleph-alpha.com/en/news/phariaai-launch/", source: Aleph Alpha, date: "2024-08-26"}
- {id: 34, title: "Cohere and Aleph Alpha sign agreement to become the first transatlantic sovereign AI solution", url: "https://aleph-alpha.com/en/news/cohere-agreement-transatlantic-sovereign-ai/", source: Aleph Alpha, date: "2026-09-16"}
- {id: 35, title: "Reto Spörri leaves Aleph Alpha, Ilhan Scheer continues as CEO", url: "https://aleph-alpha.com/en/news/reto-spoerri-leaves-ilhan-scheer-ceo/", source: Aleph Alpha, date: "2026-09-28"}
- {id: 36, title: "Organization aligned with strategic priorities", url: "https://aleph-alpha.com/en/news/organization-aligned-with-strategic-priorities/", source: Aleph Alpha, date: "2026-01-08"}
- {id: 37, title: "Cohere and Aleph Alpha to build a global AI powerhouse", url: "https://aleph-alpha.com/en/news/cohere-aleph-alpha-global-ai-powerhouse/", source: Aleph Alpha, date: "2026-04-24"}
- {id: 38, title: "Aleph Alpha's Kolibri Is No Match for the Open-Weight Leaders", url: "https://www.trendingtopics.eu/aleph-alpha-kolibri-open-weight/", source: Trending Topics, date: "2026-10-03"}
- {id: 39, title: "Aleph Alpha Kolibri: How the Sovereign German LLM Works", url: "https://tej.as/blog/aleph-alpha-kolibri", source: Tejas Kumar, date: "2026-10-03"}
- {id: 40, title: "Aleph Alpha's Kolibri: 1M Context, Trained to 256K", url: "https://fourweekmba.com/ai-aleph-alpha-kolibri-open-weights-1m-context-trained-256k/", source: FourWeekMBA, date: "2026-10-03"}
- {id: 41, title: "Aleph Alpha Kolibri-1: interesting new model for German and English texts", url: "https://forums.developer.nvidia.com/t/aleph-alpha-kolibri-1-interesting-new-model-for-german-and-english-texts/384940", source: NVIDIA Developer Forums, date: "2026-10-03"}
- {id: 42, title: "New model Aleph-Alpha/Kolibri-1 (issue #49281)", url: "https://github.com/huggingface/transformers/issues/49281", source: GitHub (huggingface/transformers), date: "2026-10-03"}
- {id: 43, title: "Aleph Alpha on X: Kolibri launch post", url: "https://x.com/Aleph__Alpha/status/2106306840657297814", source: X (Aleph Alpha), date: "2026-10-03"}
- {id: 44, title: "Qwen/Qwen3.8-Flash-Next model card", url: "https://huggingface.co/Qwen/Qwen3.8-Flash-Next", source: Hugging Face (Qwen), date: "2026-08-26"}
- {id: 45, title: "swiss-ai/Apertus-70B-2509 model card", url: "https://huggingface.co/swiss-ai/Apertus-70B-2509", source: Hugging Face (Swiss AI), date: "2025-09"}
- {id: 46, title: "utter-project/EuroLLM-22B-Instruct-2512 model card", url: "https://huggingface.co/utter-project/EuroLLM-22B-Instruct-2512", source: Hugging Face, date: "2025-12"}
- {id: 47, title: "The Llama 3 Herd of Models", url: "https://arxiv.org/abs/2407.21783", source: arXiv (Meta), date: "2024-07-31"}
- {id: 48, title: "Cohere and Aleph Alpha sign agreement", url: "https://cohere.com/blog/cohere-and-aleph-alpha-sign-agreement", source: Cohere, date: "2026-09-16"}
- {id: 49, title: "Leadership team expanded", url: "https://aleph-alpha.com/en/news/leadership-team-expanded/", source: Aleph Alpha, date: "2025-07-24"}
- {id: 50, title: "Ilhan Scheer appointed co-CEO", url: "https://aleph-alpha.com/en/news/ilhan-scheer-appointed-co-ceo/", source: Aleph Alpha, date: "2026-02-02"}
- {id: 51, title: "KI aus China für deutsche Wirtschaft kein Thema", url: "https://www.bitkom.org/Presse/Presseinformation/KI-aus-China-fuer-deutsche-Wirtschaft-kein-Thema", source: Bitkom, date: "2026-09-09"}
- {id: 52, title: "What Is Sovereign AI?", url: "https://blogs.nvidia.com/blog/what-is-sovereign-ai/", source: NVIDIA, date: "2024-02-28"}
- {id: 53, title: "Apply AI Strategy", url: "https://digital-strategy.ec.europa.eu/en/policies/apply-ai", source: European Commission, date: "2025-10"}
- {id: 54, title: "Apertus: Democratizing open and compliant LLMs for global language environments (technical report)", url: "https://arxiv.org/abs/2509.14233", source: arXiv (Swiss AI), date: "2025-09"}
:::
