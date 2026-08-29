---
eyebrow: REPORT · AI ECONOMICS
title: "The price of the frontier: what an Opus-level LLM actually costs — time, compute, and capital, measured"
deck: Quoted figures for the same models range from $5.6 million to $100 billion. All of them are defensible. None of them measure the same thing.
lede: |
  Ask what it costs to build a frontier large language model — Anthropic's Opus line being the reference standard the question usually attaches to — and you will collect answers spanning four orders of magnitude. DeepSeek says one run cost $5.6 million.[^7] Epoch AI puts GPT-4's final run at roughly $40 million amortized and Grok 4's near half a billion.[^1,6] Stanford's AI Index, pricing the same GPT-4 run at cloud rates, says $79 million and prices Llama 3.1 405B at $170 million.[^3,4] Anthropic's CEO says models in training two years ago already cost "more like a billion," with $10–100 billion runs coming.[^10] And the institutions building them have raised tens of billions of dollars and committed to hundreds of billions more in compute.[^22,23,28] Every number is real. The error is treating them as answers to the same question.
stats:
  - {label: Marginal frontier run (2025–26), value: "$0.5–1B", note: "Epoch/Anthropic estimate band"}
  - {label: Full development program, value: "$2–5B/yr", note: "run + experiments + staff"}
  - {label: Capital to stay at the frontier, value: "$10B+/yr", note: "Anthropic/OpenAI scale, 2025–26"}
  - {label: Final-run cost trend, value: "2.4x/yr", note: "since 2016, amortized"}
---

## 01. Four different things get called "the cost of a model"

The public argument about LLM costs is mostly a measurement error. Strip it to first principles and there are exactly four quantities that matter, each one strictly larger than the last, and each answering a different question.

The first is the **marginal final-run cost**: the compute consumed by the one successful pre-training run that produced the released weights, priced either at cloud-rental rates or at depreciated hardware plus energy. This is the number DeepSeek published and the number Epoch AI and the Stanford AI Index estimate.[^1,3,7] The second is the **amortized development cost**: the final run plus the failed runs, ablations and experiments that preceded it, plus the research staff — the full R&D program behind one model.[^1] The third is the **cluster acquisition cost**: what the hardware actually cost to buy, which is what matters if you are building rather than renting, and the framing Leopold Aschenbrenner's "trillion-dollar cluster" analysis insists is the only honest one.[^33] The fourth is the **institutional cost**: everything the company raised and burned — training, inference, salaries, data — to exist at the frontier continuously, which is what pitch decks, investor letters and leaked financials actually document.[^21,26]

:::kv
- {term: "1 · Marginal final run", def: "compute hours of one successful pre-training run, priced[^1,7]"}
- {term: "2 · Amortized development", def: "final run + experiments + failed runs + R&D staff[^1]"}
- {term: "3 · Cluster acquisition", def: "purchase price of the hardware fleet itself[^1,33]"}
- {term: "4 · Institutional burn", def: "total capital consumed to operate at the frontier[^21,26]"}
:::

Confusing layer 1 with layer 4 is how a $5.6 million training run and a $5 billion annual burn get quoted as evidence about the same model in the same week. They are both true; they are not about the same cost.

:::statement(attr="ARA Research")
The cost of a model is falling; the cost of the frontier is rising. Both are measured honestly — at different layers.
:::

## 02. The marginal run: tens of millions in 2023, half a billion by 2025

The best-documented layer is the final run itself, thanks to Epoch AI's cost model (Cottier et al.), which prices frontier runs two ways — depreciated hardware plus energy, and cloud rental — across 45 models.[^1,2] The headline series: the amortized hardware-plus-energy cost of the most expensive publicly announced final run has grown **2.4x per year since 2016** (90% CI 2.0–2.9x); the cloud-rental method shows a statistically indistinguishable 2.6x per year at roughly twice the absolute level.[^1] On those estimates GPT-4's final run cost about **$40 million** amortized, Gemini Ultra about **$30 million**; priced at historical cloud rates instead, Stanford's AI Index puts GPT-4 at **$78–79 million**, Gemini Ultra at **$191 million**, and Llama 3.1 405B — one of the few 2024 models with enough public data to price — at **$170 million**.[^1,3,4] Sam Altman, asked directly whether GPT-4 cost $100 million to train, answered: "It's more than that."[^19]

By 2025 the frontier run had outgrown the hundred-million band entirely. Epoch's resource estimate for xAI's Grok 4 — the largest run it has priced — comes to roughly **$490 million** of compute, about 246 million H100-hours, excluding labor, experiments and inference.[^6] Contemporary reporting had already guessed "hundreds of millions" for Llama 3.1 from chip costs alone, and Meta's CEO told investors the next generation, Llama 4, would need roughly **10 times more compute** than Llama 3.[^13,14] That is the empirical floor for what "Opus-level" means as a single training run in the current generation: {accent}high hundreds of millions of dollars, brushing $1 billion{/}. Epoch projected in 2024 that the largest publicly announced run would cross **$1 billion by early 2027**; Anthropic's CEO, speaking on the Norges Bank podcast in mid-2024, said models costing "more like a billion" were already in training.[^1,10]

:::exhibit(num="Exhibit 1", title="One frontier training run: marginal cost estimates", subtitle="$ million, final pre-training run only — no staff, no experiments, no inference", source="Epoch AI; Stanford HAI AI Index; DeepSeek[^1,3,4,6,7]", note="GPT-4 and Gemini Ultra shown under both pricing conventions. Grok 4 is a model-based Epoch estimate, not a disclosure.")
:::bar-chart(title="Marginal final-run cost", orientation=horizontal, value-unit=$, value-suffix=M)
categories: DeepSeek-V3 (rental claim), Gemini Ultra (amortized), GPT-4 (amortized), GPT-4 (cloud-rental), Llama 3.1 405B (cloud-rental), Grok 4 (Epoch estimate)
Cost ($M): 5.6, 30, 40, 79, 170, 490
:::
:::

Two properties of this layer deserve emphasis because they falsify the two laziest takes. First, even the biggest single runs remain **cheap relative to the companies**: a $490 million run is real money, but it is a rounding error against the capex programs in section 05 — which is why "frontier AI costs X per run" arguments, in either direction, prove almost nothing about the economics of the labs.[^6,15] Second, the trend is steeper than any single data point: at 2.4x per year, the marginal run that cost $40 million in early 2023 costs roughly ten times that three years later, which is exactly what the Grok 4 estimate shows.[^1,6] Epoch's separate scaling analysis finds training compute itself growing about **4x per year**, with a 2×10^29 FLOP run — about 5,000 times Llama 3.1 405B — physically feasible by 2030 if someone is willing to spend "hundreds of billions of dollars" on it.[^5]

## 03. The research tax: the run you ship is the tip of the spend

The final run is the only part of the program that shows up in a paper's cost table. The rest — failed runs, ablations, architecture experiments, and the people — is larger. Epoch's decomposition of four models' full development costs (final run plus experiments plus R&D staff compensation) puts **hardware at 47–67% of the total, R&D staff at 29–49% including equity, and energy at just 2–6%**.[^1] GPT-4's amortized hardware bill rises from ~$40 million for the final run to about **$90 million** once experiment compute is included — and its credited contributor count rose from 25 on GPT-3 to 284, while Gemini Ultra listed 941 and carried the highest staff share of all.[^1]

:::exhibit(num="Exhibit 2", title="What a frontier development program pays for", subtitle="share of total development cost, midpoints of Epoch AI's estimated ranges", source="Cottier et al., Epoch AI[^1]", note="Ranges: hardware 47–67%, staff 29–49%, energy 2–6%. Midpoints shown; staff includes equity compensation.")
:::stack-bar(legend=true)
- {label: Hardware (chips, servers, interconnect), pct: 57}
- {label: "R&D staff, incl. equity", pct: 39}
- {label: Energy, pct: 4}
:::
:::

The staff line is compounding fastest. Since mid-2025 the marginal cost of elite researchers has been publicly repriced: Meta's superintelligence recruiting blitz offered packages reported at **$100 million**, and Apple foundation-models lead Ruoming Pang defected to Meta for a package Bloomberg put **over $200 million**; Sam Altman said Meta tried — and mostly failed — to buy OpenAI staff with $100 million signing bonuses.[^30,31,38] Even DeepSeek, the efficiency outlier, reportedly pays top candidates more than $1.3 million.[^8] When 29–49% of program cost is people and the price of the pivotal people is set in nine-figure auctions, the amortized cost of a frontier model inflates even where compute efficiency improves.[^1,30]

The engineering ledger adds its own tax that never appears in GPU-hour arithmetic. Meta's Llama 3 herd paper records **466 job interruptions over a 54-day snapshot** of the 405B pre-training run — 419 of them unexpected, roughly 78% hardware-related — on a cluster of up to 16,000 H100s, with >90% effective training time achieved only through heavy tooling investment.[^12] Multiply the final run's ~30–50 million GPU-hours by the several full attempts and hundreds of ablations a serious lab runs, and Amodei's casual disclosure that the mid-sized Claude 3.5 Sonnet "cost a few $10M's to train" reads as the arithmetic floor of a single production model, not the ceiling.[^9,12]

:::callout(kind=info, label="Reading the estimates")
Marginal-run figures are model-based reconstructions, not audited disclosures: Epoch and Stanford infer chip counts and durations from papers and reporting, and the two pricing conventions differ by ~2x on the same model.[^1,3] Treat any single point estimate as a band.
:::

## 04. The DeepSeek test: what $5.6 million actually proved

No figure has been more misused than DeepSeek-V3's **$5.576 million**. The technical report is precise about what it is: 2.788 million H800 GPU-hours — 2.664M for pre-training on a 2,048-GPU H800 cluster in under two months, plus context extension and post-training — priced at an assumed **$2 per H800-hour**.[^7] It is also precise about what it excludes, in its own words: "the costs associated with prior research and ablation experiments on architectures, algorithms, or data."[^7] It is a layer-1 number, honestly labeled.

:::quote(attr="DeepSeek-V3 technical report, December 2024[^7]")
Our training costs include only the official training of DeepSeek-V3, excluding the costs associated with prior research and ablation experiments on architectures, algorithms, or data.
:::

Two independent checks bound the true cost. SemiAnalysis estimated DeepSeek's cumulative GPU investments at **over $500 million** — roughly 50,000 Hopper-generation chips, seeded by High-Flyer's 10,000-A100 purchase before export controls — with about **$1.6 billion of server capex** and $944 million of operating cost across the relevant period.[^8] And Amodei, writing weeks after the release, located V3 on the cost curve rather than off it: frontier capability gets roughly **4x cheaper per year** (his own Claude 3.5 Sonnet data point: "a few $10M's" for a mid-2024-class model), so a late-2024 model matching 7–10-month-old US models at a lower-but-not-order-of-magnitude-lower cost is "on-trend at best."[^9]

:::callout(kind=warn, label="What DeepSeek proves — and does not")
DeepSeek demonstrates that a *follower*, standing on published research and distillation-permissive ecosystems, can reproduce near-frontier capability for a single-digit-million marginal run plus a few hundred million dollars of hardware.[^7,8,9] It does not demonstrate that *pushing* the frontier is cheap: every efficiency gain DeepSeek exploited also lowers the incumbent's cost of the *next* run, which is the mechanism Amodei's export-control essay turns on.[^9]
:::

The honest synthesis is the two-curves picture. Efficiency compresses the cost of *any fixed capability* by ~4x a year; labs respond by buying **more** capability, pushing the frontier run up 2.4x a year in dollars and ~4x a year in FLOP.[^1,5,9] The residual — capability per dollar at the frontier — improves, but the absolute admission price of the frontier has risen every single year on record. There is no year in the data where the frontier got cheaper in dollars.[^1]

## 05. The capital: what the institutions actually burn and raise

Layer 4 is where the pitch-deck and IR evidence lives, and the numbers are unambiguous about scale. OpenAI's leaked audited financials — reported in June 2026 after FT review — show **R&D expense of $19.2 billion in 2025**, up from $7.8 billion in 2024, against revenue of $13.1 billion; the operating loss widened to **$20.9 billion** in one year.[^21] Internal projections that surfaced earlier tell the same story from the other side: OpenAI told investors in September 2024 to expect ~$5 billion of losses on $3.7 billion of revenue that year, and by mid-2024 reporting it was spending about **$7 billion a year on training and inference compute** alone.[^20,34] Anthropic's trajectory matches: reporting based on investor materials put its 2024 spend above **$2.7 billion, roughly $2.5 billion of it compute**, and its annualized revenue run rate has since climbed from ~$1 billion at the start of 2025 to a claimed **$47 billion by May 2026** — figures the company attaches to signed fundraise announcements, which is the strongest form of self-report a private company can give.[^28,34]

:::exhibit(num="Exhibit 3", title="Anthropic annualized revenue run rate vs. the escalation it funds", subtitle="$ billion, company-disclosed run rate at announcement dates", source="Anthropic announcements; compilation by Simon Willison[^27,28]", note="Run-rate revenue is self-reported and unaudited; it is disclosed inside securities-governed fundraise announcements.")
:::line-chart(title="Annualized revenue run rate", y-unit=$)
x: 2025-01,2025-08,2025-12,2026-02,2026-04,2026-05
Anthropic run rate ($B): 1,5,9,14,30,47
:::
:::

The fundraising ladder that finances this has no precedent in private-company history. Anthropic raised $3.5 billion at a $61.5 billion post-money valuation in March 2025, then **$13 billion at $183 billion** six months later, followed by a reported ~$30 billion round in February 2026 and ~$65 billion more in May 2026.[^27,28,39] OpenAI is raising a round exceeding **$100 billion** at a $730 billion pre-money valuation and has reset its compute-spending target to roughly **$600 billion by 2030** — the *reduced* figure, walked back from $1.4 trillion of announced infrastructure commitments, anchored by the $500 billion Stargate program, a **$300 billion** Oracle cloud contract and a $38 billion AWS deal.[^22,23,24,25] Anthropic's own compute commitments are proportional: up to **one million Google TPUs** in a deal "worth tens of billions of dollars," bringing well over a gigawatt of capacity online in 2026, on top of Amazon's Project Rainier.[^29]

The hyperscalers' audited capex — the money that actually clears — confirms the commitment level is real, not deck-ware. Meta spent **$72.2 billion** on capex in 2025 and guided to **$115–135 billion in 2026**, explicitly for "Meta Superintelligence Labs" and core AI; Alphabet spent **$91.5 billion** and guided to **$175–185 billion**; Amazon spent **$131.8 billion** and told investors to expect **about $200 billion** in 2026; Microsoft added $80.1 billion of property and equipment in just the first nine months of its fiscal 2026.[^15,16,17,18]

:::exhibit(num="Exhibit 4", title="Hyperscaler capex: 2025 actual vs. 2026 guidance midpoint", subtitle="$ billion, purchases of property and equipment", source="SEC filings[^15,16,17]", note="2026 figures are guidance midpoints: Meta $115–135B, Alphabet $175–185B, Amazon ~$200B (Jassy statement).")
:::bar-chart(title="Capex, $B", orientation=vertical, mode=grouped, value-unit=$, value-suffix=B)
categories: Meta, Alphabet, Amazon
2025 actual: 72.2, 91.5, 131.8
2026 guidance (midpoint): 125, 180, 200
:::
:::

The pitch-deck stratum of the evidence shows this was planned, not improvised. Anthropic's leaked 2023 fundraising deck told investors its next model — "Claude-Next," "10 times more capable than today's most powerful AI" — would require **"a billion dollars in spending over the next 18 months"** on clusters of "tens of thousands of GPUs," and warned that the companies training the best 2025–26 models "will be too far ahead for anyone to catch up."[^26] Three years later the deck's logic is simply the industry's budget line: Anthropic's own policy submission to the White House now projects that by 2027 a **single frontier training run will require clusters drawing ~5 gigawatts**, and it recommends the United States plan for 50 additional gigawatts of AI-dedicated power accordingly.[^11] Aschenbrenner's cluster math — ~$500 million for a GPT-4-class 2022 cluster, tens of billions by 2026, **$1 trillion-plus and ~100 GW by 2030** — is the same curve drawn from the hardware side.[^33]

## 06. Time: the frontier is reachable in under two years — if the money is already there

The temporal evidence cuts against pure capital determinism in one instructive way. Anthropic went from founding in early 2021 to **Claude 3 Opus in March 2024** — its first flagship to claim parity or better with GPT-4 — in about three years; Opus 4 followed in May 2025 and Opus 4.5 in November 2025.[^35,36,37] The fast followers were faster still: Mistral shipped Mistral Large **ten months** after its April 2023 founding; DeepSeek shipped V3 roughly **19 months** after spinning out of High-Flyer; xAI shipped Grok-3 about **23 months** after its March 2023 incorporation.[^7,8,40,41,42,43]

:::timeline
- {date: 2021-01, headline: "Anthropic founded", body: "Ex-OpenAI safety researchers; frontier flagship (Claude 3 Opus) ~38 months later.[^35]"}
- {date: 2023-03, headline: "xAI incorporated", body: "Grok-3 ~23 months later, trained on Colossus.[^40,42]"}
- {date: 2023-04, headline: "Mistral founded; Anthropic deck leaks", body: "Deck budgets $1B / 18 months for 'Claude-Next.'[^26,43]"}
- {date: 2023-05, headline: "DeepSeek spins out of High-Flyer", body: "Inherited a 10,000-A100 pre-controls stockpile.[^8]"}
- {date: 2024-10, headline: "Colossus online in 122 days", body: "100,000 H100s; 19 days from first rack to first training run — later doubled to 200K.[^32]"}
- {date: 2024-12, headline: "DeepSeek-V3", body: "2.788M H800-hours; $5.576M marginal-run claim.[^7]"}
- {date: 2025-09, headline: "Grok 4's ~$490M run", body: "Epoch's largest priced final run to date.[^6]"}
- {date: 2025-11, headline: "Claude Opus 4.5", body: "Third Opus generation in 20 months.[^37]"}
:::

What xAI's buildout clarifies is *which* time constant collapsed. The 122-day Colossus story — 100,000 H100s racked, networked and training in Memphis, against a conventional three-year datacenter planning horizon — shows that capital plus urgency can compress the **infrastructure** timeline to months.[^32] What it did not compress is the **capability** timeline: Grok-3 still arrived ~23 months after founding, because the irreducible serial time is not pouring concrete but iterating research — recipe discovery, eval-driven debugging, post-training — on hardware you already own.[^6,42] Time-to-frontier is therefore best read as *minimum* ~10–24 months with unlimited capital and a hired-away frontier team, and ~3 years from a standing start; the binding constraint in both cases is that the frontier you are chasing keeps moving at 2.4x a year while you close the gap.[^1,35]

## 07. The empirical answer

Putting the layers together, the mid-2026 evidence supports a three-part answer to what an Opus-level model costs.

**One run:** a frontier final training run now costs {accent}roughly $0.5–1 billion{/} of compute — Grok 4's ~$490 million is the largest priced estimate on record, Amodei's $1-billion-in-training remark is two years old, and the 2.4x annual trend crosses $1 billion cleanly by early 2027.[^1,6,10] Followers exploiting published methods and distillation can match *last year's* capability for a low-single-digit-million marginal run — that is real, and it is not the frontier.[^7,9]

**One program:** the amortized development cost — the run, the failed runs, the staff — is several times the final run, in the **low single-digit billions per year** for a serious frontier lab: GPT-4's hardware bill roughly doubled once experiments were included, staff is 29–49% of development cost and inflating at nine-figure-per-researcher rates, and OpenAI's audited R&D line hit $19.2 billion in 2025 across its full program.[^1,21,30]

**One institution:** staying at the frontier — which is what "building an Opus-level LLM" means as a going concern rather than a stunt — currently requires **$10 billion-plus per year** of committed capital: Anthropic's $2.5 billion compute bill in 2024 scaled into "tens of billions" of TPU commitments and roughly **$110 billion raised across four rounds in fifteen months**, while OpenAI plans $600 billion of compute through 2030.[^22,27,28,29,34,39] The capital markets are presently funding this at escalating marks; the entire structure rests on revenue curves like Exhibit 3 continuing to compound — which is a financing fact, not a technical one, and it is the single point of fragility in the whole edifice.[^21,22,28]

:::callout(kind=danger, label="The fragility")
Every layer-4 figure in this article is underwritten by private-market belief in frontier revenue growth. OpenAI's 2025 operating loss was 160% of its revenue; its $600 billion compute plan assumes revenue topping $280 billion by 2030.[^21,22] If that belief reprices, the marginal-run cost of the frontier — the layer that actually drives the science — reprises with it.
:::

:::note
All dollar figures are nominal US dollars at disclosure date. "Marginal run" estimates are model-based (Epoch AI / Stanford HAI conventions differ ~2x); company financials for private labs are self-reported or leaked documents reviewed by major outlets. Hyperscaler capex is audited and filed with the SEC.
:::

:::source
Epoch AI and Stanford HAI cost studies; arXiv technical reports; SEC filings (Meta, Alphabet, Amazon, Microsoft); company announcements (Anthropic, OpenAI, NVIDIA); leaked materials reported by TechCrunch, NYT, WSJ, Bloomberg, Ars Technica; darioamodei.com; situational-awareness.ai.
:::

:::references
- {id: 1, title: "The rising costs of training frontier AI models (Cottier et al.)", url: "https://arxiv.org/abs/2405.21015", source: arXiv, date: "2024-05-31"}
- {id: 2, title: "How much does it cost to train frontier AI models?", url: "https://epoch.ai/blog/how-much-does-it-cost-to-train-frontier-ai-models", source: Epoch AI, date: "2024-06-03"}
- {id: 3, title: "AI Index Report 2024", url: "https://hai.stanford.edu/assets/files/hai_ai-index-report-2024-smaller2.pdf", source: Stanford HAI, date: "2024-04"}
- {id: 4, title: "AI Index Report 2025, Chapter 1", url: "https://hai.stanford.edu/assets/files/hai_ai-index-report-2025_chapter1_final.pdf", source: Stanford HAI, date: "2025-04"}
- {id: 5, title: "Can AI Scaling Continue Through 2030?", url: "https://epoch.ai/blog/can-ai-scaling-continue-through-2030", source: Epoch AI, date: "2024-08-20"}
- {id: 6, title: "Grok 4 training resources: compute, cost, and environmental impact", url: "https://epoch.ai/data-insights/grok-4-training-resources", source: Epoch AI, date: "2025-09-12"}
- {id: 7, title: "DeepSeek-V3 Technical Report", url: "https://arxiv.org/abs/2412.19437", source: arXiv, date: "2024-12-27"}
- {id: 8, title: "DeepSeek Debates: Chinese Leadership On Cost, True Training Cost, Closed Model Marginal Impacts", url: "https://semianalysis.com/2025/01/31/deepseek-debates/", source: SemiAnalysis, date: "2025-01-31"}
- {id: 9, title: "On DeepSeek and Export Controls", url: "https://darioamodei.com/on-deepseek-and-export-controls", source: Dario Amodei, date: "2025-01"}
- {id: 10, title: "AI models that cost $1B to train are underway, $100B models coming — Anthropic CEO", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/ai-models-that-cost-dollar1-billion-to-train-are-in-development-dollar100-billion-models-coming-soon-largest-current-models-take-only-dollar100-million-to-train-anthropic-ceo", source: Tom's Hardware (In Good Company podcast), date: "2024-07-07"}
- {id: 11, title: "Anthropic Response to OSTP RFI on the AI Action Plan", url: "https://assets.anthropic.com/m/4e20a4ab6512e217/original/Anthropic-Response-to-OSTP-RFI-March-2025-Final-Submission-v3.pdf", source: Anthropic, date: "2025-03"}
- {id: 12, title: "The Llama 3 Herd of Models", url: "https://arxiv.org/abs/2407.21783", source: arXiv, date: "2024-07-31"}
- {id: 13, title: "Meta's Llama 3.1 is the open-source assistant", url: "https://www.theverge.com/2024/7/23/24204055/meta-ai-llama-3-1-open-source-assistant-openai-chatgpt", source: The Verge, date: "2024-07-23"}
- {id: 14, title: "Zuckerberg says Meta will need 10x more computing power to train Llama 4", url: "https://techcrunch.com/2024/08/01/zuckerberg-says-meta-will-need-10x-more-computing-power-to-train-llama-4-than-llama-3/", source: TechCrunch, date: "2024-08-01"}
- {id: 15, title: "Meta Q4 2025 earnings exhibit (8-K)", url: "https://www.sec.gov/Archives/edgar/data/1326801/000162828026003832/meta-12312025xexhibit991.htm", source: SEC EDGAR, date: "2026-01-28"}
- {id: 16, title: "Alphabet Q4 2025 earnings exhibit (8-K)", url: "https://www.sec.gov/Archives/edgar/data/1652044/000165204426000012/googexhibit991q42025.htm", source: SEC EDGAR, date: "2026-02-04"}
- {id: 17, title: "Amazon Q4 2025 earnings exhibit (8-K)", url: "https://www.sec.gov/Archives/edgar/data/1018724/000101872426000002/amzn-20251231xex991.htm", source: SEC EDGAR, date: "2026-02-05"}
- {id: 18, title: "Microsoft FY2026 Q3 earnings exhibit (8-K)", url: "https://www.sec.gov/Archives/edgar/data/789019/000119312526191457/msft-ex99_1.htm", source: SEC EDGAR, date: "2026-04"}
- {id: 19, title: "OpenAI CEO Sam Altman: The Age of Giant AI Models Is Already Over", url: "https://www.wired.com/story/openai-ceo-sam-altman-the-age-of-giant-ai-models-is-already-over/", source: Wired, date: "2024-05"}
- {id: 20, title: "OpenAI seeks new funding at valuation over $100 billion", url: "https://www.nytimes.com/2024/09/27/technology/openai-chatgpt-investors-funding.html", source: The New York Times, date: "2024-09-27"}
- {id: 21, title: "Leaked financial docs show OpenAI is losing billions of dollars a year", url: "https://arstechnica.com/ai/2026/06/leaked-financial-docs-show-openai-is-losing-billions-of-dollars-a-year/", source: Ars Technica, date: "2026-06-16"}
- {id: 22, title: "OpenAI resets spend expectations, targets around $600 billion by 2030", url: "https://www.cnbc.com/amp/2026/02/20/openai-resets-spend-expectations-targets-around-600-billion-by-2030.html", source: CNBC, date: "2026-02-20"}
- {id: 23, title: "Announcing The Stargate Project", url: "https://openai.com/index/announcing-the-stargate-project/", source: OpenAI, date: "2025-01-21"}
- {id: 24, title: "OpenAI, Oracle sign $300 billion computing deal", url: "https://www.wsj.com/business/openai-oracle-sign-300-billion-computing-deal-among-biggest-in-history-ff27c8fe", source: The Wall Street Journal, date: "2025-09-10"}
- {id: 25, title: "AWS and OpenAI announce multi-year strategic partnership", url: "https://openai.com/index/aws-and-openai-partnership/", source: OpenAI, date: "2025-11-03"}
- {id: 26, title: "Anthropic's $5B, 4-year plan to take on OpenAI", url: "https://techcrunch.com/2023/04/06/anthropics-5b-4-year-plan-to-take-on-openai/", source: TechCrunch, date: "2023-04-06"}
- {id: 27, title: "Anthropic raises Series F at $183B post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-series-f-at-usd183b-post-money-valuation", source: Anthropic, date: "2025-09-02"}
- {id: 28, title: "Anthropic's revenue run-rate, as disclosed in its fundraise announcements", url: "https://simonwillison.net/2026/May/29/anthropic/", source: Simon Willison, date: "2026-05-29"}
- {id: 29, title: "Expanding our use of Google Cloud TPUs and services", url: "https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services", source: Anthropic, date: "2025-10-23"}
- {id: 30, title: "Zuckerberg leads AI recruitment blitz armed with $100 million pay packages", url: "https://www.wsj.com/tech/ai/meta-ai-recruiting-mark-zuckerberg-5c231f75", source: The Wall Street Journal, date: "2025-06"}
- {id: 31, title: "Meta poached Apple's Pang with pay package over $200 million", url: "https://www.bloomberg.com/news/articles/2025-07-09/meta-poached-apple-s-pang-with-pay-package-over-200-million", source: Bloomberg, date: "2025-07-09"}
- {id: 32, title: "NVIDIA Ethernet networking accelerates world's largest AI supercomputer, built by xAI", url: "https://www.globenewswire.com/news-release/2024/10/28/2970195/0/en/NVIDIA-Ethernet-Networking-Accelerates-World-s-Largest-AI-Supercomputer-Built-by-xAI.html", source: NVIDIA (GlobeNewswire), date: "2024-10-28"}
- {id: 33, title: "Racing to the Trillion-Dollar Cluster (Situational Awareness, IIIa)", url: "https://situational-awareness.ai/racing-to-the-trillion-dollar-cluster/", source: Leopold Aschenbrenner, date: "2024-06"}
- {id: 34, title: "OpenAI and Anthropic lose billions on AI development and operations", url: "https://the-decoder.com/openai-and-anthropic-lose-billions-on-ai-development-and-operations/", source: The Decoder, date: "2024-07-27"}
- {id: 35, title: "Introducing the next generation of Claude", url: "https://www.anthropic.com/news/claude-3-family", source: Anthropic, date: "2024-03-04"}
- {id: 36, title: "Anthropic's new Claude 4 AI models can reason over many steps", url: "https://techcrunch.com/2025/05/22/anthropics-new-claude-4-ai-models-can-reason-over-many-steps/", source: TechCrunch, date: "2025-05-22"}
- {id: 37, title: "Introducing Claude Opus 4.5", url: "https://www.anthropic.com/news/claude-opus-4-5", source: Anthropic, date: "2025-11-24"}
- {id: 38, title: "Sam Altman says Meta tried and failed to poach OpenAI's talent with $100M offers", url: "https://techcrunch.com/2025/06/17/sam-altman-says-meta-tried-and-failed-to-poach-openais-talent-with-100m-offers/", source: TechCrunch, date: "2025-06-17"}
- {id: 39, title: "Anthropic raises Series E at $61.5B post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-series-e-at-usd61-5b-post-money-valuation", source: Anthropic, date: "2025-03-03"}
- {id: 40, title: "xAI (Q120599684)", url: "https://www.wikidata.org/wiki/Q120599684", source: Wikidata, date: "2026-07"}
- {id: 41, title: "Au Large — Mistral Large flagship release", url: "https://mistral.ai/news/mistral-large/", source: Mistral AI, date: "2024-02-26"}
- {id: 42, title: "Elon Musk's AI company xAI releases its latest flagship AI Grok-3", url: "https://techcrunch.com/2025/02/17/elon-musks-ai-company-xai-releases-its-latest-flagship-ai-grok-3/", source: TechCrunch, date: "2025-02-17"}
- {id: 43, title: "Mistral AI (Q119718658)", url: "https://www.wikidata.org/wiki/Q119718658", source: Wikidata, date: "2026-07"}
:::
