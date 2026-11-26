---
eyebrow: ANALYSIS · OPEN MODELS · PERSONAL AI
title: "Is a Guardian Angel really $100 a month? Inkling 2 Mini, continual learning and the gap between a price and a system"
deck: A Nov 26 tweet says Thinking Machines' new looped model puts gwern's "Guardian Angel" within reach for about $100 a month. The price arithmetic mostly works. The learning part is mostly unproven.
lede: |
  On 2026-11-26 an X user, @0xangelfish, wrote that with Inkling 2 Mini, gwern's idea of a model that continually learns from you every day is now possible for about $100 a month.[^1] Six days earlier Thinking Machines had released an open-weights, 26.4B-parameter looped mixture-of-experts model that fits in about 20GB.[^2,5] This article checks the claim in three parts: whether the money works, whether the model can hold what a person would teach it, and whether the evidence shows a model learning from daily use rather than being fine-tuned on a stack of logs.
domain: software
stats:
  - {label: "Tweet claim", value: "$100/mo", note: "Guardian Angel, daily learning"}
  - {label: "Gwern's own budget", value: ">$1,000/mo", note: "per user, mid-2026"}
  - {label: "Tinker training price", value: "$0.75/M tok", note: "64K context, as of 2026-11-27"}
  - {label: "Model footprint", value: "~20GB", note: "NVFP4 + MXFP8"}
---

## 01. The claim, and what would make it true

The tweet is one sentence from a verified account; per a public mirror of X's data retrieved 2026-11-27 it had about 8,457 followers on the account, 6 likes and 707 views, and it links to no evidence.[^1] That is a pitch to be tested, not a finding. The claim bundles three separate assertions, and each needs its own evidence: (a) a suitable model exists at a price near $100 a month; (b) that model can absorb one person's data; (c) the result "continually learns from you every single day" the way gwern describes.

:::kv
- {term: "Direct answer: price", def: "Plausible. Published Tinker rates put $100 at roughly 133M training tokens at 64K context, enough for daily increments but not for repeated full retrains of a large augmented corpus."}
- {term: "Direct answer: model", def: "Inkling 2 Mini is a credible open base: Apache 2.0 per press and Artificial Analysis, about 20GB, strong on agentic coding. It is weak on factual recall."}
- {term: "Direct answer: learning", def: "Unproven. No source I found shows Inkling 2 Mini, or any open model, doing the daily personal learning gwern describes."}
- {term: "Direct answer: budget framing", def: "Gwern's essay says to expect more than $1,000 a month and warns against optimizing for low cost, so $100 is a different product."}
:::

The rest of the piece takes each assertion in turn. Sources outside X are used wherever the tweet's implied facts can be checked.

## 02. What Inkling 2 Mini actually is

Thinking Machines Lab announced Inkling 2 Mini on 2026-11-20.[^2] It is a mixture-of-experts model with 26.4B total parameters and 3.4B active per token, rising to 5.4B weight activations once looping is counted.[^2] Its 24 stored layers sit in four blocks of six; the two middle blocks run three times, so 24 stored layers give 48 layer applications per token.[^2,9] Experts were pruned from 384 to 128, then the model was healed on 1T tokens distilled from a larger internal Inkling model.[^2,8] Most weights are NVFP4 with the last four layers in MXFP8, giving a footprint of about 20GB and a Mac path via Ollama with 32GB or more.[^2,5]

The looping buys compute, not stored knowledge. The lab reports the non-looped version cost 7.5% less to train but needed 140% more inference compute to match loss.[^8,9] Reviewers also stress that looping does not add factual knowledge, which tracks total parameter count.[^8,9]

:::stats
- {label: Total parameters, value: 26.4B}
- {label: Active per token, value: 3.4B, note: 5.4B counting loops}
- {label: Layer applications, value: 48, note: from 24 stored layers}
- {label: Release, value: 2026-11-20}
:::

### Discrepancies worth knowing

Secondary sources disagree on several facts that matter for a personal-AI build. The official announcement as retrieved gives no context window or license, while The Next Web, VentureBeat, The Decoder and Artificial Analysis give 1M tokens and Apache 2.0.[^2,5,6,7,11] Tinker's own model table lists Inkling 2 Mini at 256K maximum context.[^4] Per-task time is 9 minutes in one report and 14.7 minutes on Artificial Analysis's model page, and output speed is 280 tokens/s in one review and 172 on the Artificial Analysis page.[^5,10,11] One reading that reconciles them is that 1M is the weights' native window and 256K is Tinker's limit, but that is my inference and I have not verified it against the model card.

:::callout(kind=warn, label="Source caveat")
Most benchmark figures are vendor-reported, and the lab itself notes that evaluation setups vary by model.[^9] The Decoder flags that the "leads open models under 100B" claim is limited to that class and that the Intelligence Index result is a tie with Qwen3.8-27B.[^7]
:::

## 03. What gwern's Guardian Angel actually requires

Gwern's essay proposes LLMs personalized to emulate one user's values and preferences, with the user acting like a board that decides what is worth doing while the angel and its sub-agents execute and screen.[^13] The essay was first published in December 2025 and revised into mid-2026.[^13]

The core learning mechanism is **dynamic evaluation**: next-token finetuning on the fly, trading off against model size and context length.[^13] The technique is old: Krause et al. (2017) used gradient descent on recent history to set new word-level perplexity records of 51.1 on Penn Treebank and 44.3 on WikiText-2.[^18] Gwern argues catastrophic forgetting is largely handled by a small amount of replay and by larger overparameterized models, and the continual-pretraining literature supports a narrow version of this: learning-rate re-warming, re-decaying and replay matched full retraining at 405M and 10B scale on weakly shifted data.[^13,19]

Three details in the essay cut against the tweet's framing:

- **It is not a once-a-day batch job.** The nearest thing to "daily" is that every correction is trained on, interaction falls toward a few hard questions per day, and idle time is used for reprocessing the log.[^13]
- **The corpus is augmented, not raw.** The prototype uses a roughly 1GB corpus enriched with LLM-generated annotations, summaries and a `PRINCIPAL.md` profile, because plain finetuning generalizes poorly.[^13]
- **The budget is ten times the tweet's.** Gwern targets over $1,000 a month per user, notes dynamic evaluation costs more than 3x normal usage, a three-model ensemble more than 6x a frozen model, and warns against optimizing for low cost.[^13]

The essay does say a sub-100B off-the-shelf model on commodity hardware could do the job, which is the one place Inkling 2 Mini fits his specification.[^13] The sub-$100 version drops the ensemble, which gwern uses for uncertainty estimates.[^13]

## 04. The price arithmetic

Tinker's published rates for Inkling 2 Mini are $0.75 per million training tokens at 64K context and $1.50 at 256K, with sampling at $0.15 per million input tokens, $0.015 cached and $0.50 output; storage is $0.10 per GB-month, and forward-only requests from a training client bill at the training rate.[^3,4] A free 64K tier lists $0.00 for everything, subject to unspecified rate limits and a positive balance, with no stated end date.[^3] The pricing page is stamped as of 2026-10-19, a month before the model's release, so check it before budgeting.[^3]

The following is my arithmetic from those rates, not a sourced figure. $100 buys 100 ÷ 0.75 ≈ 133M training tokens at 64K, or about 4.4M a day, or 67M at the 256K rate. A 1GB text corpus is on the order of 250M tokens at roughly four bytes per token (an assumption), so a single pass costs about $188 at the 64K rate.

:::bar-chart(title="Training tokens per month vs. one pass of a 1GB corpus", subtitle="Million tokens; Tinker list prices as of 2026-11-27; corpus size is an assumption (~4 bytes/token)", orientation=horizontal, value-suffix=M)
categories: "$100 at 64K ($0.75/M)", "$100 at 256K ($1.50/M)", "One pass over ~1GB corpus (est.)"
Tokens (millions): 133, 67, 250
:::

The conclusion follows from the chart. A daily increment is cheap: at about 4.4M training tokens a day, a user adding a million tokens of new text and annotations daily fits with room for replay. What does not fit is re-training the whole augmented corpus every month, or the 3x dynamic-evaluation multiplier and ensembles gwern prices in.[^13] Serving adds little at list rates: $100 would also buy 200M output tokens at $0.50 per million, but Inkling 2 Mini was not on Tinker's serverless list, so serving a custom adapter is a separate question.[^3,10]

:::compare
- {role: LOWEST, name: "Tweet budget", value: "$100/mo"}
- {role: HIGHEST, name: "Gwern's stated target", value: ">$1,000/mo"}
- {role: SUBJECT, name: "Tinker 64K training allowance at $100", value: "~133M tokens"}
:::

Tinker is described as a Python-native fine-tuning API aimed at researchers who want control over training loops and reinforcement learning.[^6] That is a developer platform. Nothing in the pages I retrieved describes a consumer product that trains nightly on a person's data, so the $100 figure prices the compute and omits the engineering, the data pipeline and the evaluation.[^6]

## 05. Can a 3.4B-active looped model hold a person?

The capacity question has two halves: how much a low-rank adapter can store, and how much the base model knows to begin with.

On the first, Thinking Machines' own research says LoRA matches full fine-tuning on small-to-medium datasets when applied to all layers (MLP/MoE emphasized) and not capacity-constrained; past that, training efficiency degrades with the ratio of dataset to capacity, and the authors cite a roughly 2 bits per parameter storage limit from prior work, while cautioning that real-dataset capacity needs are an open question.[^17] An independent study found LoRA "learns less and forgets less": it underperforms full finetuning on code and math, forgets the base less, and full finetuning learns perturbations of rank 10 to 100 times higher than typical LoRA settings.[^16] For a personal model the second property is the useful one and the first is the cost.

On the second, the benchmarks show a model strong at agentic tasks and weak at facts:

:::slope(left-label=Qwen3.8-27B, right-label=Inkling-2-Mini, unit=%)
| Benchmark (vendor-reported) | Qwen3.8-27B | Inkling-2-Mini |
|---|---|---|
| DeepSWE v1.1 | 42.2 | 48.2 |
| BrowseComp | 61.6 | 79.0 |
| AutomationBench-AA | 48.2 | 41.8 |
| Non-hallucination rate | 71.4 | 63.4 |
:::

The comparison comes from a review that counted 25 wins, 10 losses, 2 ties and 1 split across 38 shared rows, drawn from the vendor table.[^10] The model card states Inkling is more likely than larger models to state incorrect information with confidence, and it can get stuck in repetitive loops and overwrite files without confirmation.[^10] AA-Omniscience is -8.6 for Inkling against -6.4 for Qwen3.8-27B.[^6]

Why this matters: a personal model is mostly a model of facts about one person, their history, preferences and relationships. A base that hallucinates more under uncertainty is a worse starting point for that job than one that scores well at coding.

## 06. Does fine-tuning on your own data actually teach it?

This is the weakest link in the tweet's chain. Two lines of evidence say that gradient updates are a poor way to inject facts.

Gekhman et al. (EMNLP 2024) found examples introducing unfamiliar facts are learned significantly slower than familiar ones and, once learned, linearly increase the model's tendency to hallucinate.[^20] Ovadia et al. compared unsupervised fine-tuning with retrieval and found retrieval consistently outperforms fine-tuning, both for facts seen in pretraining and for wholly new ones; training on many rephrasings of a fact may help.[^21] That rephrasing finding matches gwern's use of paraphrase and Q&A augmentation, so the essay is not naive about this.[^13,21]

The only public Inkling-2-Mini derivative I found that touches memory is a community model, and its own card is sobering. LTM-Lab's V19 adds an external, disk-backed event store with a small learned working state, not weight updates, and reports, self-reported and uncorroborated elsewhere, in a small pilot: 4/4 on color identification with the source image shown, 1/4 on choosing the right original from four, 0/8 on writing a valid lesson from eight events, 0/82 work-order executions after autonomous intake and 3/82 with verbatim stored sources.[^12] The card concludes that its results leave improvement in general continual skill learning unestablished.[^12] This is a single small pilot by a third party, so it shows the problem is hard, not that it is unsolvable.

:::rank-list
- {label: "Color ID with source image shown", value: "4/4", pct: 100}
- {label: "Pick correct original of four", value: "1/4", pct: 25}
- {label: "Valid lesson from eight events", value: "0/8", pct: 0}
- {label: "Work orders after autonomous intake", value: "0/82", pct: 0}
:::

## 07. Data, hosting and risk are not in the $100

Even if the compute works, two inputs are missing from the price. First, data: one proposal builds a single-user evaluation set from continuous screen recordings at 4fps, about 1GB per hour of capture, estimating a year at under 10TB and under $150 of Cloudflare storage.[^14] That is the kind of capture a personal model needs and the kind it makes sensitive. Second, trust: gwern argues hosting should use tamper-proof cloud servers with hardware attestation and end-to-end encryption, and calls the claim that prompt-injection resistance improves a speculation.[^13]

Forethought's design sketch names the risks of getting this wrong: unreliable angels would be annoying, "fallen angel" variants could manipulate users, and over-outsourcing risks gradual disempowerment; it also argues for keeping the deep personal data these tools need on-device and encrypted where possible.[^15] Thinking Machines also notes that looping lets a model reason without writing its reasoning down, which complicates chain-of-thought monitoring, though early tests found no meaningful loss of monitorability at this scale and called the results preliminary.[^5,8]

## 08. Timeline of what is and is not verified

:::timeline
- {date: 2025-10, headline: "Tinker debuts", body: "Python-native fine-tuning API from Thinking Machines."}
- {date: 2025-12, headline: "Gwern publishes Guardian Angels", body: "Revised through mid-2026; sets the >$1,000/month target."}
- {date: 2026-01-29, headline: "Forethought angels-on-the-shoulder sketches", body: "Lists reliability, adoption and privacy hurdles."}
- {date: 2026-06-26, headline: "Screencast data-eval proposal", body: "LessWrong response to gwern's essay."}
- {date: 2026-11-20, headline: "Inkling 2 Mini released", body: "Open weights, looped MoE, Tinker support."}
- {date: 2026-11-26, headline: "The tweet", body: "Claims $100/month Guardian Angel is within reach."}
:::

Sources for the timeline: Tinker's debut[^6], gwern's essay[^13], Forethought[^15], the LessWrong post[^14], the release[^2] and the tweet[^1].

## 09. What could break this analysis

Four things could make the tweet more right than I have allowed. Tinker's free 64K tier, if it persists, makes the training cost near zero, though its end date is unstated and it is rate limited.[^3] A retrieval-plus-small-adapter design may achieve most of the benefit without the fine-tuning's hallucination penalty, which is consistent with the Ovadia result.[^21] The LTM-Lab pilot is tiny and may say little about a better-built system.[^12] And much of my capacity reasoning draws on pre-2026 papers about other model families, so a looped MoE could behave differently; no source I found tests that.[^16,17]

Four things push the other way. Gwern himself says to budget at least ten times the tweet's figure and not to optimize for cost.[^13] The only public continual-learning artifact on this base reports essentially no measured gain.[^12] The base model is weaker on factual recall, where a personal model lives.[^10] And hosting, data capture and security are unpriced.[^13,14]

:::callout(kind=info, label="Verdict")
The $100 figure is defensible as a compute budget for incremental adapter training on Inkling 2 Mini at Tinker list prices. It is not evidence that a Guardian Angel in gwern's sense exists at that price. As of 2026-11-27 I found no demonstration of daily personal learning on this model.
:::

## References

:::references
- {id: 1, title: "@0xangelfish tweet on Inkling 2 Mini and Guardian Angel", url: "https://x.com/0xangelfish/status/2125969819321372724", source: "X/Twitter", date: "2026-11-26"}
- {id: 2, title: "Introducing Inkling 2 Mini", url: "https://thinkingmachines.ai/news/inkling-2-mini/", source: "Thinking Machines Lab", date: "2026-11-20"}
- {id: 3, title: "Tinker pricing", url: "https://thinkingmachines.ai/tinker/pricing/", source: "Thinking Machines Lab", date: "2026-11-27"}
- {id: 4, title: "Tinker", url: "https://thinkingmachines.ai/tinker/", source: "Thinking Machines Lab", date: "2026-11-27"}
- {id: 5, title: "Thinking Machines releases Inkling 2 Mini, a looped AI model for laptops", url: "https://thenextweb.com/news/inkling-2-mini-thinking-machines-looped-open-weights-laptop", source: "The Next Web", date: "2026-11-21"}
- {id: 6, title: "Thinking Machines wows with Inkling 2 Mini looped transformer model", url: "https://venturebeat.com/technology/thinking-machines-wows-with-inkling-2-mini-looped-transformer-model-that-runs-locally-on-laptops", source: "VentureBeat", date: "2026-11"}
- {id: 7, title: "New open model Inkling 2 Mini thinks in loops", url: "https://the-decoder.com/new-open-model-inkling-2-mini-thinks-in-loops-to-solve-problems-with-fewer-words-and-still-runs-on-a-laptop/", source: "The Decoder", date: "2026-11-21"}
- {id: 8, title: "Thinking Machines Lab Releases Inkling 2 Mini for Local Devices", url: "https://www.unite.ai/thinking-machines-lab-releases-inkling-2-mini-for-local-devices/", source: "Unite.AI", date: "2026-11-20"}
- {id: 9, title: "Inkling 2 Mini Explained: How a Looped Transformer Gets More Reasoning Out of a 20GB Model", url: "https://dev.to/jamilxt/inkling-2-mini-explained-how-a-looped-transformer-gets-more-reasoning-out-of-a-20gb-model-14a6", source: "DEV Community", date: "2026-11"}
- {id: 10, title: "Inkling 2 Mini Review: Does It Beat Qwen3.8-27B?", url: "https://aitoolsreview.co.uk/insights/thinking-machines-inkling-2-mini", source: "AIToolsReview", date: "2026-11-22"}
- {id: 11, title: "Inkling 2 Mini model page", url: "https://artificialanalysis.ai/models/inkling-2-mini", source: "Artificial Analysis", date: "2026-11-27"}
- {id: 12, title: "LTM-Lab/Inkling-2-Mini-Uncensored-V19", url: "https://huggingface.co/LTM-Lab/Inkling-2-Mini-Uncensored-V19", source: "Hugging Face", date: "2026-11"}
- {id: 13, title: "Guardian Angels: LLM Personalization for Productivity and Security", url: "https://gwern.net/guardian-angel", source: "gwern.net", date: "2026"}
- {id: 14, title: "Screencasts could be scalable data evals for single user", url: "https://www.lesswrong.com/posts/NwrbrHmkDuKPXgLFb/screencasts-could-be-scalable-data-evals-for-single-user", source: "LessWrong", date: "2026-06-26"}
- {id: 15, title: "Design Sketches: Angels-on-the-Shoulder", url: "https://www.forethought.org/research/design-sketches-angels-on-the-shoulder", source: "Forethought", date: "2026-01-29"}
- {id: 16, title: "LoRA Learns Less and Forgets Less", url: "https://arxiv.org/abs/2405.09673", source: "arXiv / TMLR", date: "2024-09-20"}
- {id: 17, title: "LoRA Without Regret", url: "https://thinkingmachines.ai/blog/lora/", source: "Thinking Machines Lab", date: "2025-09"}
- {id: 18, title: "Dynamic Evaluation of Neural Sequence Models", url: "https://arxiv.org/abs/1709.07432", source: "arXiv", date: "2017-10-25"}
- {id: 19, title: "Simple and Scalable Strategies to Continually Pre-train Large Language Models", url: "https://arxiv.org/abs/2403.08763", source: "arXiv", date: "2024-09-04"}
- {id: 20, title: "Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?", url: "https://arxiv.org/abs/2405.05904", source: "arXiv / EMNLP 2024", date: "2024-10-01"}
- {id: 21, title: "Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs", url: "https://arxiv.org/abs/2312.05934", source: "arXiv", date: "2024-01-30"}
:::
