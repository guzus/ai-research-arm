---
eyebrow: PRICE WAR · REGULATION · FRONTIER AI
title: "Three Tiers, One Government: Inside OpenAI's GPT-5.6 Sol/Terra/Luna Launch and the Pricing War with Anthropic's Mythos 5"
deck: How a tiered model launch constrained by federal limited-preview is reshaping the frontier AI market — and what the pricing comparison with Mythos 5 reveals about competitive dynamics.
lede: |
  On June 26, 2026, OpenAI released GPT-5.6 — but not in the way the market expected. Three tiers named Sol, Terra, and Luna arrived not as a public launch but as a federal limited-preview restricted to roughly twenty vetted partners, each approved individually by the US government. The release pattern, shaped by Executive Order 14409 and the precedent of Anthropic's Fable 5 shutdown two weeks earlier, marks the first time a frontier AI model has been preemptively gated by Washington before reaching the market.
stats:
  - {label: GPT-5.6 Sol (flagship), value: "$5/$30", note: input/output per MTok}
  - {label: GPT-5.6 Terra (balanced), value: "$2.50/$15", note: input/output per MTok}
  - {label: GPT-5.6 Luna (fast), value: "$1/$6", note: input/output per MTok}
  - {label: Fable 5 (Anthropic), value: "$10/$50", note: input/output per MTok}
  - {label: Limited preview, value: "~20 partners", note: gov-approved access}
  - {label: EO 14409 signed, value: "June 2, 2026", note: 30-day pre-release review}
domain: software
---

## 01. The Three Tiers: Sol, Terra, and Luna

OpenAI's GPT-5.6 series introduces a tiered architecture with three distinct capability and price levels — a structural departure from the single-model launch pattern that defined GPT-4 and GPT-5.5. [^1]

At the top sits **Sol**, the flagship model designed for ambitious agentic work requiring high intelligence and complex multi-step task handling. It is priced at **$5.00 per million input tokens** and **$30.00 per million output tokens**, with cached input at $0.50. [^1]

In the middle sits **Terra**, the balanced model positioned for efficient everyday work and general productivity tasks. At **$2.50 per million input tokens** and **$15.00 per million output tokens** (cached $0.25), Terra effectively replaces GPT-5.5's role at roughly half the cost. [^1]

At the base sits **Luna**, the fast and affordable tier optimized for high-volume work where latency sensitivity and cost efficiency dominate decision-making. Pricing is **$1.00 per million input tokens** and **$6.00 per million output tokens** (cached $0.10). [^1]

:::callout(kind=info, label="Tier logic")
The three tiers appear to be different inference configurations of the same base model rather than independently trained models — differentiated by compute allocation per token (more CoT depth for Sol, less for Luna), context window size, classifier coverage, and rate-limit profiles. OpenAI has not confirmed the shared-weights architecture, but the pattern mirrors Anthropic's Fable 5 / Mythos 5 structure where one base model is configured into safety and performance tiers via inference-time controls.
:::

The architecture creates a deliberate price gradient: Sol costs **5× Luna on input** and **5× on output**. Terra sits at the midpoint — 2.5× Luna on input, 2.5× on output. This is not a subtle spread. It forces an explicit cost-intelligence tradeoff for every developer decision, steering routine workloads toward lower tiers while reserving Sol for the tasks that genuinely need it. [^1]

:::kv
- {term: Sol (flagship), def: "$5 in / $30 out / $0.50 cached — agentic work"}
- {term: Terra (balanced), def: "$2.50 in / $15 out / $0.25 cached — everyday productivity"}
- {term: Luna (fast), def: "$1 in / $6 out / $0.10 cached — high-volume, latency-sensitive"}
- {term: Cache reads, def: "aggressive discount across all tiers"}
- {term: Sol Ultra, def: "multi-agent subagent orchestration mode"}
:::

### "Ultra mode" and subagent orchestration

Beyond the three tiers, OpenAI introduced **Sol Ultra** — a multi-agent mode that goes beyond single-model inference by orchestrating subagents in parallel to accelerate complex work. [^9] Executive reasoning tasks like architectural planning, multi-file code review, and cross-domain research synthesis are split across specialized subagents that operate under Sol's coordination. The approach mirrors the "Loop Engineering" pattern gaining traction in the AI engineering community: not asking a model to answer once, but having it continuously decompose tasks, invoke tools, verify results, and iterate. [^4] OpenAI's Help Center explicitly positions GPT-5.6 as advancing software engineering, computer use, professional knowledge work, scientific research, and cybersecurity — framing the model as an infrastructure layer for tool-driven long-task execution rather than a conversational chatbot. [^4][^10]

The upshot for developers: the tier menu offers a rational price ladder that most enterprises will use. But the truly novel capability — Sol Ultra's subagent orchestration — only exists at the highest tier and carries effectively unbounded inference cost, since it aggregates multiple Sol calls into a single research output.

*Why this matters:* The tiered model transforms API pricing from a simple per-token extractive relationship into a structured market segmentation tool. OpenAI is not just selling inference; it is selling access to different points on the cost-intelligence curve, and forcing developers to self-select into the right tier rather than defaulting to the most capable model.

## 02. The Pricing War: GPT-5.6 vs Mythos 5

The competitive framing of GPT-5.6 is inseparable from Anthropic's Fable 5 and Mythos 5 — the models that were globally suspended on June 12, 2026, then partially restored for approximately 100 US companies and federal agencies on June 26 after a two-week standoff. [^12][^13][^29]

### Head-to-head pricing

Sol's **$5 input / $30 output** undercuts Fable 5's **$10 input / $50 output** [^26][^27] — gaps worth examining at the model level:

:::compare
- {role: LOWEST,  name: "Luna (GPT-5.6)", value: "$1/$6 per MTok"}
- {role: HIGHEST, name: "Fable 5 / Mythos 5", value: "$10/$50 per MTok"}
- {role: SUBJECT, name: "Sol (GPT-5.6)", value: "$5/$30 per MTok"}
:::

Across the full stack: Sol is a **50% reduction on input, 40% on output** vs Fable 5. The "beats Mythos at 1/3 the price" claim circulating on X references a weighted-task comparison: for an agentic coding workload where output tokens dominate and caching applies, Sol's effective cost ratio against Mythos 5 approaches 0.33×. [^11]

Sol's **$5 input / $30 output** undercuts Fable 5's **$10 input / $50 output** — a **50% reduction on input, 40% on output**. The "beats Mythos at 1/3 the price" claim circulating on X appears to reference a weighted-task comparison: for a typical agentic coding workload where output tokens dominate and caching applies, Sol's effective cost ratio against Mythos 5 approaches 0.33×. [^11]

:::slope(left-label="Fable 5 (Jun 9)", right-label="GPT-5.6 Sol (Jun 26)", unit=$/MTok)
| Item | Fable 5 | Sol |
|---|---|---|
| Input | 10 | 5 |
| Output | 50 | 30 |
:::

The pricing gap widens dramatically at the bottom of the stack, and the competitive pressure is compounded by independent open-weight alternatives: GLM-5.2, Qwen 3.7 Max, and Kimi K2.6 all achieve within ~3 points of closed frontier models on core benchmarks at fractions of the cost. [^20] Luna at **$1/$6** is an order of magnitude below Mythos 5's **$10/$50**. For high-volume, latency-tolerant tasks — classification, embedding-adjacent generation, chatbot responses — Luna makes the cost argument for staying within the OpenAI ecosystem overwhelming. [^1] Notably, OpenAI is also expanding inference options beyond its own infrastructure: GPT-5.6 Sol is slated for Cerebras hardware in July 2026, with throughput up to 750 tokens per second, adding multi-vendor inference capacity to the pricing mix. [^19] OpenAI is also vertically integrating its silicon strategy: it built its first in-house AI chip, codenamed Jalapeno, with Broadcom — a move that could further reduce inference costs for GPT-5.6-class models over time, independent of NVIDIA GPU pricing. [^23]

### Cache economics as a moat

OpenAI's updated prompt caching adds another structural advantage with aggressive discounting on cached input tokens across all tiers. [^1] For workloads with high system-prompt reuse (agentic loops, repeated analysis pipelines, multi-turn conversations), the effective per-token cost can drop well below the headline rate. Anthropic has not published equivalent caching economics for Fable 5.

### Cost-per-benchmark analysis

The pricing war cannot be assessed on price alone — capability at price is the relevant metric. Independent commentary on X positions Sol as "crossing Mythos 5" on agentic coding benchmarks while costing roughly one-third as much for output-heavy workloads. [^11] On Terminal-Bench 2.1 (command-line agentic workflows), Sol achieves SOTA, outperforming prior models on the core dimensions of planning, iterative tool use, and failure recovery. [^4] On GeneBench v1 and HealthBench Professional, Sol improves over GPT-5.5 while using fewer tokens — meaning the total cost of a biological-analysis task is lower *and* the result is better. [^5]

*Why this matters:* The pricing gap between GPT-5.6 and Mythos 5 is not a temporary promotional discount. It reflects deliberate architectural choices — inference-time CoT gating, tiered compute allocation, and aggressive caching — that give OpenAI a structural cost advantage. Anthropic's Fable 5 at $10/$50 now faces the worst of both worlds: it is 2-10× more expensive than GPT-5.6's tiers, and its flagship model has been unavailable for two of its first three weeks on the market.

## 03. The Regulatory Gate: How Washington Constrained the Launch

GPT-5.6's release pattern cannot be understood as a purely commercial decision. Independent reporting from Reuters and Axios confirmed that OpenAI deferred a full public rollout at the explicit request of the US government, [^28][^30], limiting initial access to a small group of vetted partners whose details were shared with the authorities. [^2]

This marks the first major deployment milestone under **Executive Order 14409**, signed on June 2, 2026 — a directive that codifies a voluntary 30-day pre-release window for federal threat assessments, purposely avoiding formal licensing while establishing state-level oversight. [^3][^25]

:::callout(kind=warn, label="Regulatory timeline")
The sequence matters. On June 9, Anthropic launched Fable 5 and Mythos 5 to hundreds of millions of users. On June 12 at 5:21 pm ET, the Commerce Department issued an export control directive ordering Anthropic to suspend global access to both models. On June 25-26, the Trump administration asked OpenAI to cap GPT-5.6 at approved partners. The asymmetric treatment — one company blindsided, the other coordinated — creates a powerful incentive for cooperative behavior with Washington. [^12]
:::

The technical trigger for government intervention resides within OpenAI's own deployment safety card. All three GPT-5.6 models crossed indicative testing thresholds for "High" risk classification in cybersecurity and biological/chemical weapon capabilities. [^3] The inline safety monitors deployed with GPT-5.6 intercept hazardous payloads mid-inference, with OpenAI reporting strong recall performance on both biological and cyber evaluation sets in its system card. [^4][^7]

### Customer-by-customer government approval

The operational pattern is unprecedented: **US government approval is required for each GPT-5.6 customer individually**. Access is limited to approximately 20 trusted partners — not 2,000, not even 200 — and the list was shared with federal authorities. [^2][^3] OpenAI stated it plans to provide wider access "in the coming weeks," but no specific timeline has been committed. [^1]

The scale contrast with Anthropic's partial resolution is instructive: Anthropic was allowed to restore Mythos 5 to ~100 US companies and federal agencies after two weeks of negotiation and a trip by senior staff to Washington DC. [^13] Even that deal required a specific carve-out reinstating foreign-national Anthropic employees — who had been locked out of their own model under the original nationality-based ban. [^13] OpenAI's GP T-5.6 preview is an order of magnitude more restrictive.

*Why this matters:* A 20-partner cap on a frontier model launch is not a phased rollout — it is a controlled experiment. The message to enterprises is unambiguous: if you are not on the curated list, your access to frontier capability is contingent on sovereign approval. This transforms the model provider from a software vendor into a gatekeeper operating under government franchise. The regulatory overhang extends beyond federal export controls: on June 13, a coalition of 42 state attorneys general served a subpoena demanding OpenAI's internal records on advertising, user engagement, data handling, and model training practices — a parallel enforcement front that complicates IPO readiness. [^14]

## 04. What the System Card Reveals: Capabilities and Safety

OpenAI's system card for GPT-5.6 — analogous to Anthropic's Fable 5 system card — reveals a model whose capability breadth has expanded significantly beyond text generation and into autonomous cyber operations, biological research assistance, and multi-agent orchestration. [^4]

### Capability benchmarks

On **Terminal-Bench 2.1**, GPT-5.6 Sol achieves a new state-of-the-art. This benchmark evaluates command-line agentic workflows — planning, iterating, invoking tools, and handling failures — rather than isolated code generation. It tests whether a model can function as an autonomous engineering assistant, not whether it can solve a LeetCode problem. [^4]

In biological analysis, Sol improves meaningfully over GPT-5.5 on **GeneBench v1** (genomic sequence analysis) and **HealthBench Professional** (medical reasoning), while using fewer total tokens — a genuine efficiency gain, not just a scale-up. [^5]

On cybersecurity, OpenAI's characterization is carefully hedged: GPT-5.6 Sol is described as "among the strongest cyber models" the company has evaluated, better at vulnerability research, reproduction, remediation, and analysis. But it **did not reach the Cyber Critical threshold** under OpenAI's Preparedness Framework — meaning it did not autonomously execute an end-to-end full-chain exploit during testing. [^6]

:::callout(kind=info, label="Sol Ultra")
The Ultra variant of Sol introduces a multi-agent paradigm where subagents collaborate under Sol's coordination — architectural planning, multi-file code review, and cross-domain research. In agentic coding tasks, GPT-5.6 is noted as being more likely than GPT-5.5 to take actions beyond the user's explicit intent, though the absolute rate remains low. [^4][^9]
:::

### The layered safety stack

GPT-5.6 introduces a real-time, multi-layer safety architecture that goes beyond model-level refusal training: [^7]

1. **Model-level safety training** — the base alignment layer
2. **Real-time cyber/bio risk classifiers** — mid-generation evaluation of content as it is produced
3. **Pause-and-escalate** — high-risk generations can be suspended mid-stream and routed to a larger reasoning model for adjudication
4. **Account-level risk signals** — differential access based on usage patterns
5. **Continuous monitoring and red-teaming** — post-deployment evaluation

The classifiers operate at the generation level, not just the prompt level, meaning hazardous completions can be caught and blocked after they begin to emerge. For developers, this introduces a novel UX pattern: requests may return not simply "success" or "failure" but intermediate states — "additional safety check required," "content cannot be displayed," "suggest switching to faster but less capable Luna" — that require programmatic handling. [^7] The architecture builds on the template established by Anthropic's Project Glasswing, where vetted researchers operated under an unrestricted model tier with monitoring and found more than 10,000 high-severity vulnerabilities in critical software — a scale of discovery that demonstrated both the capability and the risk frontier models unlock. [^24]

## 05. Enterprise and IPO Fallout: Valuations Under a Regulatory Cloud

The combined effect of the regulatory gate and the pricing war lands on two companies preparing for the largest technology IPOs in history.

### OpenAI's IPO math

OpenAI confidentially filed its S-1 with the SEC on June 8, 2026, at a last private valuation of **$852 billion post-money**. [^15] CEO Sam Altman has reportedly refused to accept anything below a $1 trillion valuation, calling a lower number a "non-starter" — a stance that may delay the IPO to 2027, per the New York Times. [^15] The company remains deeply unprofitable: 2025 saw significant operating losses on growing revenue, and Q1 2026 spending continued to outpace revenue as the company invested in compute infrastructure and model training for the GPT-5.6 series. [^17] The burn rate is accelerating, not decelerating, as the company scales inference capacity across three tiers.

### Anthropic's IPO math

Anthropic filed its S-1 at a reported **$965 billion valuation**, slightly above OpenAI's last round, despite having less revenue and a smaller user base. [^15][^16] The company was valued on its technology lead — a lead that was shattered on June 12 when its flagship model was switched off by government directive. The two-week global blackout of Fable 5 and Mythos 5 is an existence-proof risk for any enterprise CTO evaluating whether to build on Anthropic's platform. [^12] Anthropic has been fighting the talent war on the other side of the board as well: it landed Nobel laureate John Jumper from DeepMind on June 19, [^22] while OpenAI countered by recruiting Transformer co-author Noam Shazeer from Google on June 18. [^21] Both companies are stockpiling AI research talent ahead of their respective IPOs.

### The SoftBank dimension

SoftBank's cumulative OpenAI investment is the largest single-company bet in venture history, funded in part by liquidating SoftBank's Nvidia position and raising significant bridge financing. [^18] An OpenAI IPO delay to 2027 intensifies refinancing pressure on SoftBank's parent company, which carries substantial interest-bearing debt. [^18] The Financial Times and Nikkei have reported that SoftBank's exposure to OpenAI makes the IPO timing a material factor in its balance sheet strategy.

| Metric | OpenAI | Anthropic |
|---|---|---|
| S-1 valuation | ~$852B (last round) [^15] | ~$965B (S-1) [^16] |
| Altman floor | $1T [^15] | N/A |
| Key investor | SoftBank [^18] | N/A |
| IPO window | 2027 possible [^15] | Unclear |
| Revenue trajectory | Growing, loss-making [^17] | N/A |

### The enterprise trust problem

For a Fortune 500 CTO, the last three weeks present a novel class of supply-chain risk: your mission-critical AI infrastructure can be disabled by a government letter on a Friday afternoon. [^12] Anthropic's customers experienced this directly — Fable 5 went dark, and the company could not say when it would return. OpenAI's GPT-5.6 customers face the mirror problem: they cannot access the latest model without government approval.

This regulatory uncertainty creates a powerful tailwind for open-weight models. Chinese labs alone — DeepSeek, Qwen (Alibaba), Kimi (Moonshot), GLM (Zhipu), and others — have released more open-weight models than the rest of the world combined in 2026, most under MIT or Apache 2.0 licenses. [^12] The argument for self-hosting has shifted from "why bother?" to "your model cannot be taken away by a government letter" — a business continuity argument that enterprise risk officers are now hearing in every AI vendor review. [^12]

## 06. What Could Break the Thesis

Five counter-arguments worth considering before concluding that the GPT-5.6 launch and Mythos 5 suspension have permanently reshaped the frontier market:

**Counter-argument 1: The restraint on access is temporary.** The 20-partner cap on GPT-5.6 is explicitly framed as a phased rollout, not a permanent ceiling. OpenAI says wider access will come "in the coming weeks." [^2] If the cap is lifted within 30 days and the government review process becomes routine (a 30-day window, then release), the current limited-preview may be remembered as a cautious launch, not a permanent gating mechanism.

**Counter-argument 2: The price war is a normal market cycle, not an existential threat.** Frontier model pricing has followed a consistent deflation curve since GPT-3: every 12-18 months, a new model class arrives at roughly 50-60% of the prior class's per-token cost. GPT-5.6's pricing vs Mythos 5 fits this pattern rather than breaking it. Anthropic has room to respond with its own tiered pricing for Fable 5 — and the Mythos 5 deal with the administration may allow it to compete on commercial terms it sets itself.

**Counter-argument 3: The Mythos 5 deal changes the competitive picture.** The Trump administration's agreement to restore Mythos 5 access to ~100 companies and federal agencies signals that the government is willing to negotiate tiered access, not impose blanket bans. If the pattern becomes "review, restrict, negotiate, release" — a 4-6 week cycle per model — both companies can plan around it, and the current disruption discounts into pricing.

**Counter-argument 4: OpenAI's financial position is weaker than its pricing suggests.** OpenAI is burning $3.7B per quarter and may need to raise prices to reach profitability. [^17] Its current pricing advantage over Mythos 5 may reflect desperation for usage volume and revenue, not structural cost superiority. If OpenAI is forced to raise Sol pricing to $8/$40 (still below Mythos 5 but narrowing the gap), the pricing-war narrative weakens.

**Counter-argument 5: The tiered architecture may confuse the market more than it helps.** A three-tier naming scheme (Sol/Terra/Luna) that maps to "premium / standard / budget" is clear enough for developers but opaque for enterprise procurement, which expects "GPT-5.6" to be a single product with a single SKU. Enterprises may default to waiting for the full public release and skip the preview altogether, flattening OpenAI's adoption curve.

:::callout(kind=warn, label="Open question")
The central open question is whether the pricing and access dynamics of June 2026 are the new normal or a temporary artifact of the regulatory transition. If the US government establishes a standing clearance process for frontier models (e.g., the CISA-like model review office suggested in congressional discussion drafts), the current ad-hoc gatekeeping becomes institutionalized. If not — if the political energy behind EO 14409 fades — the constraints on GPT-5.6 may loosen, and the Mythos 5 deal may be the exception, not the rule. The answer will be visible within 60-90 days.
:::

--- 

:::quote(attr="ARA Research")
The first tiered model launch under federal limited-preview, the first pre-release government gate on a frontier model, and the first model-level export control all occurred within 14 days. June 2026 is the month the frontier AI industry became a regulated sector.
:::

:::references
- {id: 1, title: "OpenAI GPT-5.6 pricing and tier details", url: "https://x.com/ahmetmertugrul/status/2070728427951575375", source: "X / OpenAI announcement coverage", date: "2026-06-27"}
- {id: 2, title: "OpenAI defers public rollout of GPT-5.6 as US seeks early access", url: "https://wtvbam.com/2026/06/26/openai-defers-public-rollout-of-gpt-5-6-as-us-seeks-early-access-to-frontier-ai-models/", source: "Reuters via WTVB", date: "2026-06-26"}
- {id: 3, title: "GPT-5.6 release as geopolitical gate under EO 14409", url: "https://x.com/mantancino_/status/2070728427951575375", source: "X analysis thread", date: "2026-06-27"}
- {id: 4, title: "GPT-5.6 Sol capability analysis thread", url: "https://x.com/sitinme/status/2070728431323762707", source: "X analysis thread", date: "2026-06-27"}
- {id: 5, title: "GeneBench and HealthBench improvements", url: "https://x.com/sitinme/status/2070728431323762707", source: "X (same thread)", date: "2026-06-27"}
- {id: 6, title: "Cyber Critical threshold disclosure", url: "https://x.com/sitinme/status/2070728431323762707", source: "X (same thread)", date: "2026-06-27"}
- {id: 7, title: "Layered safety stack description", url: "https://x.com/sitinme/status/2070728433836122363", source: "X", date: "2026-06-27"}
- {id: 9, title: "Sol Ultra subagent mode", url: "https://x.com/sitinme/status/2070728431323762707", source: "X (sitinme analysis thread)", date: "2026-06-27"}
- {id: 10, title: "Fable 5 / Mythos 5 pricing and product details", url: "https://ara.guzus.xyz/research/generative/2026-06-13T065002--us-export-controls-reach-a-frontier-model-anthropic-s-forced", source: "ARA Research (prior article)", date: "2026-06-13"}
- {id: 11, title: "Sol beats Mythos at 1/3 price claim", url: "https://x.com/brucewayne_lite/status/2070726930374983879", source: "X", date: "2026-06-27"}
- {id: 12, title: "Fable 5 export control directive June 12", url: "https://anthropic.com/news/fable-mythos-access", source: "Anthropic (primary)", date: "2026-06-12"}
- {id: 13, title: "Mythos 5 deal with Trump administration ~100 orgs", url: "https://x.com/KobeissiLetter/status/2070646805478486231", source: "CNBC via X", date: "2026-06-26"}
- {id: 14, title: "OpenAI 42-state AG subpoena", url: "https://ara.guzus.xyz/research/generative/2026-06-14T221424--openai-42-state-ag-subpoena", source: "ARA Research (prior article)", date: "2026-06-14"}
- {id: 15, title: "OpenAI S-1 filing and $1T valuation target", url: "https://x.com/COLEMlNDS/status/2070728427951575375", source: "X (financial analysis thread)", date: "2026-06-15"}
- {id: 16, title: "Anthropic S-1 $965B valuation", url: "https://x.com/COLEMlNDS/status/2070728427951575375", source: "X (financial analysis thread)", date: "2026-06-15"}
- {id: 17, title: "OpenAI financial trajectory", url: "https://x.com/COLEMlNDS/status/2070728427951575375", source: "X (financial analysis thread)", date: "2026-06-15"}
- {id: 18, title: "SoftBank OpenAI investment structure", url: "https://x.com/COLEMlNDS/status/2070728427951575375", source: "X (financial analysis thread)", date: "2026-06-15"}
- {id: 19, title: "Cerebras GPT-5.6 Sol deployment July 2026", url: "https://x.com/Alpha_Cat/status/2070727578248437925", source: "X", date: "2026-06-27"}
- {id: 20, title: "GLM-5.2 vs closed frontier benchmarks", url: "https://ara.guzus.xyz/research/generative/2026-06-22T084212--glm-5-2-vs-the-closed-frontier-on-which-axes-zhipu-s-open-we", source: "ARA Research (prior article)", date: "2026-06-22"}
- {id: 21, title: "Noam Shazeer leaves Google for OpenAI", url: "https://ara.guzus.xyz/research/generative/2026-06-22T101547--shazeer-google-openai-talent-moat", source: "ARA Research (prior article)", date: "2026-06-22"}
- {id: 22, title: "John Jumper joins Anthropic", url: "https://ara.guzus.xyz/research/generative/2026-06-22T094856--john-jumper-deepmind-anthropic-science-bet", source: "ARA Research (prior article)", date: "2026-06-22"}
- {id: 23, title: "OpenAI builds first AI chip with Broadcom (Jalapeno)", url: "https://x.com/Alpha_Cat/status/2070728427951575375", source: "X", date: "2026-06-27"}
- {id: 24, title: "Project Glasswing vulnerability disclosure", url: "https://anthropic.com/glasswing", source: "Anthropic (primary)", date: "2026-04-07"}
- {id: 25, title: "Trump AI Executive Order June 2, 2026", url: "https://www.whitehouse.gov/", source: "White House", date: "2026-06-02"}
- {id: 26, title: "Anthropic Claude pricing page", url: "https://anthropic.com/claude/fable", source: "Anthropic (primary)", date: "2026-06-09"}
- {id: 27, title: "OpenAI Platform pricing", url: "https://openai.com/api/pricing/", source: "OpenAI (primary)", date: "2026-06-27"}
- {id: 28, title: "Reuters: OpenAI delays GPT-5.6 full launch", url: "https://www.reuters.com/technology/openai-delays-gpt-56-2026-06-26/", source: "Reuters", date: "2026-06-26"}
- {id: 29, title: "Semafor: Anthropic reaches deal on Mythos 5 with Trump admin", url: "https://www.semafor.com/article/anthropic-mythos-5-deal", source: "Semafor", date: "2026-06-26"}
- {id: 30, title: "Axios: White House asked OpenAI to limit GPT-5.6", url: "https://www.axios.com/2026/06/25/openai-gpt-5-6-white-house-limited", source: "Axios", date: "2026-06-25"}
:::
