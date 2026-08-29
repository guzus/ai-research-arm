---
eyebrow: REPORT · AI POLICY
title: "The Ban That Isn't One Yet"
deck: DeepSeek's Huawei pivot, a 200-firm lobby, and a fight over what "banning" Chinese AI even means
lede: |
  On July 22, 2026, nearly 200 startups asked Washington not to cut off Chinese open-weight AI models — arguing against a ban that, as of this writing, does not legally exist. Behind the fight sits a genuine DeepSeek hardware pivot toward Huawei silicon, contested chip-performance claims, and a policy debate where "export control," "possession ban," and "procurement rule" keep getting flattened into one word.
stats:
  - {label: "LTA signatories", value: "~200", note: "unverified press count"}
  - {label: "DeepSeek funding round", value: "$7.4B", note: "closed June 2026"}
  - {label: "Nvidia China DC revenue", value: "$0", note: "from $4.6B a year earlier"}
  - {label: "Enacted bans on Chinese AI use", value: "0", note: "as of Jul 20, 2026"}
domain: policy
---

:::kv
- {term: "Who actually spoke", def: "Disclosures on Huawei chips and TileLang came mostly from tech reports and Huawei's own statements — not Liang Wenfeng's own words"}
- {term: "What TileLang really is", def: "A real, independently-built open-source DSL DeepSeek adopted; adds Huawei Ascend support but still runs alongside CUDA — and a 2025 DeepSeek training run on Ascend reportedly failed"}
- {term: "What the \"ban\" actually is", def: "As of July 20, 2026: no executive order, no completed Entity List action, no enacted statute — a menu of threatened and pending tools"}
- {term: "Why ~200 firms are lobbying", def: "Documented cost savings at Coinbase, Snowflake, and Lindy from Chinese open-weight models"}
- {term: "Beijing's mirror move", def: "China's commerce ministry is drafting its own controls on foreign downloads of Chinese open-weight models"}
:::

## 01. What Wenfeng revealed — and what he didn't say himself

Most of the "Liang Wenfeng detailed Huawei chip access" headlines rest on a citation chain the coverage itself blurs: what DeepSeek's founder actually said on the record in 2024 is a different statement from what DeepSeek's technical reports and Huawei's own disclosures say about 2026 hardware, and the two have been merged into a single narrative that neither party has stated in those terms.

:::quote(attr="Liang Wenfeng, DeepSeek, 2024")
No short-term plans. Our challenge has never been money; it's the embargo on high-end chips.
:::

That line is real, on the record, and dated — a January 2025-published English translation of a 2024 Chinese-language interview [^1]. (This article renders the translated wording verbatim rather than the looser paraphrase — "money has never been the problem... bans on shipments are the problem" — that has circulated in secondary coverage; the meaning is the same, but only the translation above is directly attributable to the cited source.) It is also the last clearly attributable Wenfeng statement in this entire chain. No corroborated 2026 on-the-record remark from Wenfeng personally detailing Ascend chip access has surfaced; the disclosure that press coverage folds into his "voice" instead traces to DeepSeek's own technical reports and to Huawei's statements, relayed by outlets citing unnamed insiders rather than Wenfeng himself [^2]. That is not a small gap — it is the difference between a founder narrating a strategic pivot and a company quietly changing its supplier list while the founder stays silent.

What is actually documented: Huawei confirmed its Ascend processors were used to train part of DeepSeek's V4-Flash model, and DeepSeek's V4 technical report listed domestic chips alongside Nvidia GPUs for the first time [^3]. That is a first — a named-model, named-chip disclosure with two corroborating parties (DeepSeek's paper and Huawei's confirmation) — and it is the strongest fact in this section [^3]. But it is a document trail, not a quote. Nobody should read "V4 technical report cites Ascend" and hear it in Wenfeng's voice; the technical report is an engineering artifact, not a founder interview.

:::timeline
- {date: 2024, headline: "\"Money was never the problem\"", body: "Liang Wenfeng, on the record: bans on advanced-chip shipments — not capital — are DeepSeek's binding constraint."}
- {date: 2025-02, headline: "Ren Zhengfei's self-sufficiency pledge", body: "At a Xi Jinping symposium, Huawei's Ren Zhengfei says he is coordinating 2,000+ companies toward 70%+ Chinese semiconductor self-sufficiency by 2028."}
- {date: 2026, headline: "Huawei confirms Ascend training role", body: "Huawei confirms Ascend processors trained part of V4-Flash; DeepSeek's V4 report lists domestic chips alongside Nvidia for the first time."}
:::

The middle beat matters for the same reason: it, too, is not a Wenfeng statement. Ren Zhengfei made the self-sufficiency pledge; Wenfeng's attendance at that February 2025 symposium is reported only in secondary outlets (SCMP, Fortune), and he was not among the six named speakers in the official Xinhua/CGTN readout [^4,5]. So the widely circulated "Wenfeng was there and signed on" framing rests on presence, not speech — a subtle but consequential downgrade from "he committed to this" to "he may have been in the room."

Lay the three points end to end and a fifteen-month arc emerges without Wenfeng narrating any of it: a 2024 quote prioritizing money over chips, a 2025 industry-wide self-sufficiency pledge he is only reported to have witnessed, and a 2026 technical disclosure — authored by DeepSeek's engineers and confirmed by Huawei, not spoken by him — that domestic silicon now trains part of a flagship model. Zero direct Wenfeng quotes anchor the 2025–2026 legs of that arc; one anchors 2024, and it argues the opposite of urgency around domestic chips.

The tension is real even without a founder quote to dramatize it: a man who said advanced-chip bans (not money) were the binding constraint now runs a company that, per its own paper, trained on the domestic chips those bans were partly meant to route around — while funding also moved (Section 04). What would weaken this section's framing: a verified 2026 Wenfeng interview or company statement using his own words to characterize the Ascend shift, which would collapse the press/reality gap this section documents; absent that, treat every "Wenfeng said" construction in circulating coverage as unsourced until a primary quote surfaces. This distinction matters because the rest of the piece hinges on separating founder intent from institutional fact — conflating the two overstates how deliberate or narrated DeepSeek's hardware pivot actually was.

## 02. TileLang: the DSL that unlocks portability, without replacing CUDA

DeepSeek did not build the kernel language it's credited with — TileLang is an independently-authored open-source project that DeepSeek adopted and productionized, and even in DeepSeek's own account it runs alongside CUDA rather than in place of it.

TileLang's canonical repository, `tile-ai/tilelang`, traces to a Peking University research group, with part of the work done during a Microsoft Research internship; it was open-sourced under the MIT license on 2025-01-20 — DeepSeek is a downstream adopter of the tooling, not its creator [^6]. That provenance matters for the "China built its own stack" framing: the DSL predates DeepSeek's public use of it and was never proprietary to the lab in the first place.

:::kv
- {term: Origin, def: Peking University + Microsoft Research internship}
- {term: License, def: MIT (open-sourced 2025-01-20)}
- {term: Backends, def: NVIDIA, AMD, Ascend (AscendC / AscendNPU-IR), Metal, WebGPU}
:::

What TileLang actually does is narrower than "hardware independence" implies. DeepSeek's V4 technical report describes it as replacing hundreds of fine-grained Torch ATen operators with fused kernels — a productivity and performance layer for kernel authoring — and is explicit that TileLang kernels coexist with CUDA kernels rather than fully displacing them [^7]. In other words, this is a portability *option* layered on top of the existing CUDA-centric stack, not a rip-and-replace migration off it.

The part of the story that does support a genuine multi-vendor claim is codegen breadth: TileLang ships dedicated AscendC and AscendNPU-IR backends targeting Huawei's Ascend silicon, in addition to its existing NVIDIA, AMD, Metal, and WebGPU backends [^6]. That confirms what TileLang structurally is — a kernel-authoring DSL with pluggable, vendor-specific codegen — rather than a runtime abstraction that quietly routes around vendor toolchains. Write once, compile to whichever backend is present; the toolchain-specific compiler still does the heavy lifting underneath.

On raw performance, TileLang's own paper reports up to {accent}5x speedup over Triton on Nvidia H100{/} and up to 6x on AMD GPUs, plus up to 90% code-size reduction for fused attention kernels [^8]. ==unverified: these are best-case, workload-specific figures for fused attention kernels, self-reported in the TileLang paper and not independently reproduced at that magnitude — the same paper's own GEMM benchmarks show TileLang closer to parity with Triton (roughly 1.0-1.25x), and at least one independently reported community benchmark (a Native Sparse Attention kernel on H20) found TileLang running several times SLOWER than Triton, not faster== so treat the 5x/6x headline as a best-case ceiling, not a general benchmark result — and note they describe TileLang the *DSL*, not the separate DeepSeek-V4 Expert-Parallel scheduler that press coverage often conflates with it. That EP/MoE scheme was verified running on both Nvidia GPUs and Huawei Ascend NPUs, with DeepSeek reporting 1.50–1.73x speedup for general inference and up to 1.96x for small-batch RL workloads [^7] — real, disclosed multipliers, but relative ones; DeepSeek did not publish absolute Ascend-vs-Nvidia throughput, so the numbers say the scheduler helps on both platforms, not that Ascend matches Nvidia.

:::callout(kind=warn, label=Counterpoint)
Portability at inference time is not the same claim as hardware independence at training time. An earlier 2025 DeepSeek attempt to train on Huawei Ascend chips reportedly failed outright — unstable chips, slow interconnects, immature CANN software, and no FP8 support forced a reset back to Nvidia H20s for training, with Ascend relegated to inference duty [^9].
:::

That failed training run is the load-bearing fact against any "DeepSeek has achieved hardware independence" narrative. TileLang plus the Ascend backend plus the EP scheduler together demonstrate that DeepSeek can *serve* trained models on non-Nvidia silicon with credible efficiency gains — a real and useful capability. But the frontier-scale training workload that actually produces a model like V4 reportedly still could not run on Ascend as of the most recent reported attempt, and stayed on Nvidia H20s. Portability, in DeepSeek's own 2025–2026 experience, is currently a one-way door: open on the inference side, still closed on the training side.

Why it matters: every downstream claim in this piece — that DeepSeek "de-risked" Nvidia dependence, that ~200 firms are betting on a Huawei-capable open-weight stack, that Beijing's procurement posture reflects confidence in domestic silicon — rests on conflating what TileLang has proven (inference portability, vendor-published and independently-corroborated EP numbers) with what it hasn't (training-time hardware independence at frontier scale). Get that distinction wrong and the rest of the "Nvidia moat is cracking" thesis inherits an unsupported premise.

## 03. The Ascend 950PR: a real chip, contested numbers

Huawei's Ascend 950PR, unveiled March 20, 2026, is not vaporware — it is a shipping accelerator with in-house-fabricated memory [^10], but the performance and volume figures attached to its launch are almost entirely vendor-sourced and thirdhand, while independent analysis points to a domestic memory bottleneck, not chip fabrication, as the real cap on how many can actually reach customers [^14].

Huawei's own disclosure puts the 950PR at 1.56 PFLOPS of FP4 compute, 112GB of in-house HBM under the "HiBL 1.0" brand, 1.4 TB/s of bandwidth, and a 600W power envelope — and Huawei frames that package as roughly 2.8x an Nvidia H20 [^10]. None of those four headline specs has been independently verified by a teardown; they trace to Huawei's launch materials as relayed by TrendForce [^10]. The comparison undergirding the "2.8x" claim is also methodologically shakier than the round number suggests: Nvidia's H20 does not natively support the FP4 precision format Huawei used to generate that ratio, meaning the benchmark compares Huawei's chip in its best format against Nvidia's chip in a format it wasn't built to run [^11]. That is not proof the underlying chip is weak — but it means the 2.8x figure describes a favorable-precision comparison, not an apples-to-apples throughput measurement.

Demand signals are more credible than the specs, but still thinly sourced. Reuters reported, citing two anonymous sources, that ByteDance and Alibaba were preparing to place Ascend 950PR orders after internal chip testing "went well" — a real signal of hyperscaler interest, though the report at that stage quantified no order volume [^12]. The number that later circulated widely — combined Alibaba/ByteDance/Tencent orders in the "hundreds of thousands of units" — is a thirdhand attribution chain: TrendForce citing Reuters citing The Information, with no company confirming an exact figure in an earnings call or IR filing [^13]. That distinction matters: a specific-sounding number that has passed through three outlets without a primary source attached is analytically weaker than its precision implies, even when it isn't wrong.

The real ceiling on any of this may not be Huawei's fab capacity at all. SemiAnalysis assessed — for the prior 910C generation, before the 950PR existed — that Chinese domestic HBM supply from CXMT (roughly 2 million stacks per year), not SMIC's logic-die capacity, is the binding constraint on Ascend production volume, sufficient for only an estimated 250,000-300,000 units of that generation [^14]. A separate independent estimate from The Substrate gives a materially higher range, so this is a live disagreement among analysts rather than a settled number [^14] — but even the more optimistic camp is debating a memory-supply ceiling, not a compute-fab one. Laid side by side, a reported order figure in the "hundreds of thousands" and an HBM-constrained capacity estimate in roughly the same band aren't necessarily contradictory, but they leave little headroom: if Chinese hyperscalers are ordering anywhere near the volume reported, they may be ordering close to, or beyond, what the domestic memory supply chain can currently fill.

:::stats
- {label: "FP4 compute (Huawei-disclosed)", value: "1.56", unit: "PFLOPS"}
- {label: "In-house HBM, HiBL 1.0 (Huawei-disclosed)", value: "112", unit: "GB"}
- {label: "Memory bandwidth (Huawei-disclosed)", value: "1.4", unit: "TB/s"}
- {label: "Power draw (Huawei-disclosed)", value: "600", unit: "W"}
:::

:::bars
- {label: "HBM-constrained capacity ceiling (910C-gen est., SemiAnalysis)", value: "~275,000-300,000 units/yr", pct: 75}
- {label: "Reported combined 950-series orders (thirdhand, unconfirmed)", value: "\"hundreds of thousands\" of units", pct: 100}
:::

This matters because the 950PR is the clearest test case for whether China's chip-independence narrative is production reality or press-cycle momentum: a genuinely mass-producing, in-house-memory accelerator with real hyperscaler order interest is a meaningfully different fact pattern than a launch-day spec sheet — but until an order volume is confirmed in a filing rather than a fourthhand citation, and until domestic HBM output is shown to clear the volumes being discussed, the honest read is "real chip, unverified scale."

## 04. Money was never the problem, until it was

In 2024, Liang Wenfeng dismissed the idea that DeepSeek needed outside capital at all — a claim that reads very differently after the company opened its books to a state fund fourteen months later.

:::quote(attr="Liang Wenfeng, DeepSeek, 2024")
No short-term plans. Our challenge has never been money; it's the embargo on high-end chips.
:::

That line was a statement of independence: DeepSeek would stay self-funded, insulated from investor pressure, free to chase research bets without a cap table to answer to. It held for two years. Then, in June 2026, DeepSeek closed its first-ever external funding round — roughly 50 billion yuan (~$7.4B) at a post-money valuation near 350.88 billion yuan (~$52B), traced through a chain of minor indirect LPs in a Chinese regulatory filing [^16]. Six weeks after that round closed, reports surfaced of early, unconfirmed talks for a second round at a pre-transaction valuation near $71B, with proceeds reportedly earmarked not for talent or model research but for DeepSeek's own gigawatt-scale datacenters and AI chip purchases [^18]. The destination of the money is the tell: this is not a company buying researchers, it is a company buying infrastructure [^18].

The structure of the June round is where the story sharpens. Commercial backers — Tencent, CATL, JD.com, NetEase, and a slate of VC funds — invested through a Liang-controlled limited partnership carrying a five-year lock-up and zero voting rights. China's National AI Industry Investment Fund invested directly instead, on its own terms, retaining voting rights with no lock-up at all [^15,17]. Every other check in the round bought silence; the state fund's check bought a seat.

:::callout(kind=info, label="Governance")
The asymmetry isn't cosmetic. Every commercial investor in the June round accepted a five-year lock-up and no vote; the National AI Industry Investment Fund alone got voting rights and no lock-up. That is a golden share in substance, awarded to exactly one LP — the state's [^15,17].
:::

:::stats
- {label: Round size, value: "$7.4B", note: "closed June 2026"}
- {label: Post-money valuation, value: "~$52B", note: "regulatory filing chain"}
- {label: Commercial-LP lock-up, value: "5 yrs", unit: "no vote"}
- {label: State-fund lock-up, value: "0", unit: "full vote"}
:::

Zoom out to six weeks of headlines and the trajectory looks less like a funding event and more like a repricing in real time.

:::slope(left-label="June 2026", right-label="Reported, July 2026", unit=$B)
| Item | June 2026 | Reported, July 2026 |
|------|-----------|----------------------|
| DeepSeek valuation | 52 | 71 |
| Liang Wenfeng net worth | 16.7 | 36 |
:::

Neither right-column figure is settled. The $71B talk has no signed term sheet and comes from early-stage reporting [^18]. The net-worth jump is even softer: Bloomberg's Billionaires Index moved Liang from ~$16.7B to ~$36B on July 13, 2026, built on an assumed ~78% DeepSeek stake against a ~$50B valuation that has never been market-tested by an actual share trade — and the naive arithmetic (78% of $50B ≈ $39B) doesn't cleanly reproduce Bloomberg's $36B figure, which implies undisclosed adjustments to the model. Forbes' own tracker implies a materially different number for the same stake [^19,20]. Two trackers, one filing, no public trade to arbitrate between them — the number is a modeled estimate dressed as a fact, and it should be read that way.

Strip out the contested figures and the closed round still tells a clean story. A founder who spent two years insisting money was never the constraint chose, the moment a real one showed up — gigawatt-scale datacenter buildout and chip procurement at a cost no self-funded lab can absorb — to trade board-level control to a single state investor rather than dilute broadly. That is not a company that ran out of ambition or talent; it is a company that ran into a capital-intensity wall that only compute infrastructure, not researchers, could explain. The distinction matters for everything downstream: the domestic-chip story in Sections 2–3, and the export-control debate in Sections 5–7, are ultimately arguments about whether DeepSeek can build that infrastructure without Nvidia — and this section is the first hard evidence that DeepSeek itself now believes the answer requires money it didn't think it needed before.

## 05. The ~200-firm revolt: Little Tech Association vs. a ban

A trade association that did not exist until nine days earlier organized nearly 200 companies to lobby the Trump administration against a blanket ban on Chinese open-weight AI models — a mobilization notable for its speed and its unverified headline number in equal measure.

The Little Tech Association launched July 13, 2026 as a self-described trade group, with branding that traces directly to a16z's July 2024 "Little Tech Agenda" manifesto — though no source establishes that a16z funds or governs the new entity [^23,24]. Nine days after launch, on July 22, 2026, the association sent letters to President Trump, Commerce Secretary Howard Lutnick, and OSTP Director Michael Kratsios urging against a blanket ban on Chinese open-weight models [^21]. The letter's core argument was quoted consistently across outlets: "American leadership requires two things: world-leading American open-weight models and continued access for U.S. builders to open models already available worldwide" [^22].

:::kv
- {term: Launched, def: "July 13, 2026"}
- {term: "Letter sent", def: "July 22, 2026, 9 days later"}
- {term: "Addressed to", def: "Trump, Commerce Sec. Lutnick, OSTP Dir. Kratsios"}
- {term: "Branding lineage", def: "a16z's 2024 \"Little Tech Agenda\" (funding/governance link unconfirmed)"}
:::

The press framed the effort as "nearly 200" firms signing on — but that figure is a press characterization repeated identically across outlets, not a number stated inside the letter itself or backed by a published signatory roster [^21]. That gap matters for how much weight the count should carry: a headline that travels unchanged across multiple publications can just as easily reflect a shared press release as an independently verified tally, and readers have no way to check who actually signed without a roster to inspect.

The letter's stated principle — access to open models keeps U.S. builders competitive — coexists with a more self-interested read of why signatories mobilized so fast. Particle founder Suhail Doshi, one of the signatories, was blunt about who benefits from a ban:

:::quote(attr="Suhail Doshi, Particle")
It's great for Anthropic. We're all going to have to spend money on Anthropic.
:::

Doshi's framing names the counterpoint explicitly: firms that build on cheap, capable Chinese open-weight models have a direct financial stake in keeping that option open, independent of any broader argument about American open-weight leadership [^25]. Whether the "nearly 200" figure holds up to scrutiny or the coalition's professed principle is doing more work than the economics, the letter's timing is what stands out — a brand-new association turning around a 200-firm-scale lobbying push in nine days is fast by trade-association standards, and it lands the argument squarely in front of the officials weighing the ban before any policy is finalized.

:::callout(kind=warn, label="Same-week counter")
==contested: within the same 24-48 hour window as the letter, OSTP Director Kratsios alleged Moonshot AI used a "sophisticated internal platform" to distill Anthropic's models at scale and acquired export-controlled Nvidia GB300 servers — allegations Moonshot has not publicly addressed. The exact sequencing (whether Kratsios's statement landed the same day as the letter or the day after) is unresolved in available reporting, and the specific claim traces to Kratsios's own public statement rather than the general coverage cited elsewhere in this section [^26].== The administration's stated rationale for scrutinizing Chinese open-weight providers arrived in the same narrow window as the lobby letter urging against a blanket ban, underscoring that this is a live, unresolved dispute rather than a settled question either way.
:::

This matters because the outcome shapes who gets to build on which models at what cost: if the administration treats the letter's "nearly 200" framing as evidence of broad industry consensus, it changes the political cost of a ban — even though the underlying count, the association's funding lineage, and the Moonshot allegations are all, as of this writing, contested or unverified.

## 06. Why 200 firms actually care: the economics of Chinese open-weight adoption

The Little Tech Association's lobbying push in Section 5 is not abstract free-market principle — it is defending a cost migration that is already showing up in named companies' own numbers and in platform-level token-share data. Coinbase CEO Brian Armstrong said the exchange defaulted more than 1,200 internal AI agents to Zhipu's GLM-5.2 and Moonshot's Kimi K2.7 Code, self-hosting the downloaded open weights, and cut Coinbase's AI bill nearly in half in the process [^27]. Lindy CEO Flo Crivello went further, moving 100% of the company's model traffic off Anthropic Claude and onto DeepSeek after inference costs began exceeding payroll, a switch he projects will save millions of dollars a year [^31]. Snowflake CEO Sridhar Ramaswamy benchmarked GLM-5.2 within 1% of Claude Opus 4.7 on an internal 103-task coding suite at roughly one-fifth the per-token cost — a notable admission given Snowflake simultaneously holds a commercial Anthropic partnership, which cuts both ways: either its Anthropic ties should bias it toward downplaying a rival model, or the number is credible precisely because it works against Snowflake's own commercial interest [^30]. ==unverified: the "within 1%" framing describes best-of-N (Pass@3) scoring; on first-attempt (Pass@1) scoring the same benchmark reportedly showed a wider gap favoring Opus, so the headline parity claim depends on which scoring method is used and shouldn't be read as unqualified across-the-board parity==.

{accent}These are not isolated anecdotes{/} — they track a platform-wide shift. OpenRouter's own 2025 State of AI report shows Chinese open-source models climbing from under 1.2% of weekly token share in late 2024 to nearly 30% in some peak 2025 weeks, averaging roughly 13% across the full year [^28]. That is a real, order-of-magnitude swing in where enterprise inference spend is flowing on OpenRouter's own platform [^28]. ==unverified: OpenRouter is one routing marketplace among many (alongside direct API access, cloud-hosted deployments, and self-hosted inference), and no verified figure for its share of total global AI spend was found for this article — treat the percentages above as a real trend on OpenRouter specifically, not a market-wide census==.

:::line-chart(title="Chinese open-source models' share of OpenRouter weekly tokens", subtitle="OpenRouter State of AI 2025", y-unit=%)
x: Late 2024,2025 average,2025 peak weeks
Chinese OSS share: 1.2,13,30
:::

:::note
These three points are the only snapshots OpenRouter's report discloses — late-2024 baseline, full-year average, and peak weeks — not a smooth continuous series. Treat the line between them as illustrative, not measured.
:::

A more dramatic — and far shakier — figure surfaced in Chinese state-affiliated media: People's Daily Online reported Chinese-origin models processing 12.96 trillion tokens on OpenRouter versus 3.03 trillion for U.S. models, a roughly 4.3x ratio, in the week of March 30–April 5, 2026 [^29]. That number is relayed via a state outlet citing OpenRouter data rather than pulled directly from OpenRouter's own dashboard, and it should be flagged as unverified and directionally motivated reporting, not weighted the same as OpenRouter's own disclosed report cited above.

:::rank-list
- {label: Snowflake (internal coding suite), value: "~80% cheaper/token", pct: 80, highlight: true}
- {label: Coinbase (1,200+ agents on GLM-5.2/Kimi K2.7), value: "~50% AI bill cut", pct: 50}
- {label: Lindy (100% traffic moved to DeepSeek), value: "100% of traffic moved", pct: 100}
:::

The counterpoint is unavoidable: every cost-savings figure in this section is self-reported by an executive with a direct incentive to publicize the number, whether to justify the switch to a board, to market open-weight adoption as a competitive edge, or — in Snowflake's case — to signal impartiality despite a competing Anthropic relationship. None of these disclosures come with an independently audited cost breakdown. Still, the pattern matters: when a payments exchange, an AI-agent startup, and a data-cloud vendor all report double-digit-to-order-of-magnitude savings from the same class of models within weeks of each other, the Little Tech Association's opposition to a ban reads less like ideology and more like firms defending line items they can already point to on an invoice.

## 07. The ban that isn't one yet: procurement bans, Entity Lists, enforcement reality

As of July 20, 2026, no executive order, completed Entity List action, or enacted procurement-ban statute specifically bars U.S. use of Chinese AI models — what exists is a menu of five tools still being weighed, a legal distinction most coverage collapses, and a five-year-old precedent for what "restriction" actually delivers.

Reporting places the administration in deliberation, not enforcement: Axios describes officials weighing Entity List threats, procurement rules, security advisories, liability rules, and public pressure as five *distinct* and still-unselected levers [^32]. The clearest legislative vehicle, the bipartisan No Adversarial AI Act (H.R. 4142, Reps. Moolenaar and Krishnamoorthi), would direct the Federal Acquisition Security Council to maintain a list — refreshed every 180 days — of adversarial-nation AI models federal agencies cannot buy or use without exemption. It remains referred to committee, not enacted [^33]. Pressure is building through oversight rather than statute: House Homeland Security Chairman Andrew Garbarino and Select Committee on the CCP Chairman John Moolenaar sent formal inquiry letters to Airbnb and Anysphere (Cursor) on April 29, 2026, demanding details on their use of Chinese-built AI systems [^34] — a fact-finding move, not a prohibition.

:::timeline
- {date: 2025-01-16, headline: "Zhipu AI Entity List addition", body: "BIS adds Zhipu AI and 9 subsidiaries, citing PRC military-modernization concerns — the only completed action in this section, and it binds U.S. exporters, not U.S. users of already-downloaded weights."}
- {date: 2026-04-29, headline: "House probes Airbnb, Anysphere", body: "Garbarino and Moolenaar send formal letters demanding detail on the firms' use of Chinese-built AI systems."}
- {date: 2026-07-16, headline: "Kimi K3 partial launch", body: "Moonshot AI ships a 2.8-trillion-parameter model; full open weights promised July 27."}
- {date: 2026-07-20, headline: "Axios reports the five-tool menu", body: "Entity List threats, procurement rules, security advisories, liability rules, and public pressure — still unselected."}
- {date: 2026-07-21, headline: "Bessent threatens sanctions", body: "Treasury Secretary Scott Bessent cites \"watermarks of our U.S. large language models\" in Chinese models and threatens sanctions tied to Kimi K3."}
:::

The proximate trigger for all of this is one model. Moonshot AI's Kimi K3 partially launched July 16-17, 2026 — 2.8 trillion parameters, full open weights promised for July 27 — and is the specific catalyst named across the reporting for the administration's renewed push [^36]. Treasury Secretary Scott Bessent escalated the rhetoric on July 21: "We are finding watermarks of our U.S. large language models on many of the Chinese models, and that's unacceptable," he said, threatening sanctions tied directly to the K3 release [^35]. That threat, notably, is prospective — a review, not a signed order.

:::compare
- {role: ENACTED, name: "Zhipu Entity List (export-only)", value: "Jan 2025"}
- {role: PENDING, name: "No Adversarial AI Act (H.R. 4142)", value: "Referred to committee"}
- {role: THREATENED, name: "Bessent sanctions review", value: "Jul 2026, prospective"}
:::

:::callout(kind=info, label="Legal distinction")
Export controls, physical possession, and government procurement are three separate legal regimes, and most coverage of a China-AI "ban" blurs them into one. The Zhipu AI Entity List addition legally binds U.S. **exporters** — it restricts who may sell or transfer controlled items *to* Zhipu — it does not reach a U.S. firm that has already downloaded Zhipu's open weights and is simply running them [^38]. A procurement rule like H.R. 4142 works differently again: it would restrict what federal *agencies* may buy or deploy, leaving private-sector use untouched. Legal scholarship backs the narrowest reading of what's constitutionally reachable here: Rozenshtein (Lawfare, April 2024) argues there is no general First Amendment right to distribute model weights, distinguishing them from source code in the Bernstein v. DOJ / Junger v. Daley "code as speech" lineage — a March 2026 SSRN paper (Trevino & Nikolich) reaches the same conclusion [^41,42]. Brookings' Kyle Chan goes further, arguing it is "ultimately impossible" to ban Chinese open-source models once weights are freely downloadable — which is precisely why Washington's actual center of gravity has shifted to procurement-only restrictions rather than a possession ban [^43].
:::

The strongest counterpoint to "restrictions will neutralize the threat" is not hypothetical — it already happened, to a different Chinese tech giant, and it didn't work as advertised. Huawei's May 2019 Entity List addition triggered a real and measurable hit: global smartphone shipments fell 41% year-over-year in Q4 2020, and Huawei dropped from the #1 global vendor to #6 [^39,40]. But the same day it was listed, HiSilicon activated a "spare tire" self-sufficiency plan, and by 2023 Huawei had replaced more than 13,000 components and redesigned over 4,000 circuit boards [^39,40]. ITIF estimates the controls cost U.S. firms at least $33B in lost Huawei-related sales between 2021 and 2024 [^40] — worth flagging that ITIF holds an explicit anti-unilateral-controls policy position, so treat that figure as an interested estimate, not a neutral one. The bottom line: Huawei's global telecom-equipment share still stood near 31-34% in 2024, up from roughly 29% in 2018 [^40]. Controls redirected Huawei's business and cost U.S. firms real revenue; they did not eliminate the targeted firm.

Meanwhile, the White House's own AI advisor has publicly named the interest group pushing hardest for restriction. David Sacks accused closed-source labs — which he called "already a duopoly in terms of model revenue" — of lobbying the government to eliminate their open-source competitors [^37], a reminder that "national security" and "incumbent protection" arguments are travelling together in this debate, not always separably.

This matters because the 200-firm coalition described in the prior section is not defending against a ban that exists — it is lobbying pre-emptively against a menu of tools, several of which (procurement rules, security advisories) would not touch private-sector open-weight use at all, while the one tool proven to work at scale (Entity List controls) has a five-year track record of redirecting rather than eliminating the targeted firm's global footprint.

## 08. The moat, the mirror, and Beijing's own about-face

Nvidia's own CEO now publicly concedes China's AI-chip market to Huawei — but that concession is a byproduct of export controls erasing Nvidia's China revenue, not proof Huawei has out-built Nvidia on the merits, and it lands the same month Beijing quietly moves to wall off the very open-weight models it spent years promoting abroad.

Speaking on CNBC on May 21, 2026, Jensen Huang said Nvidia has "largely conceded" China's AI-chip market to Huawei — a striking admission from a CEO who has spent two years insisting Nvidia would keep competing there [^47]. The number behind the quote is stark: Nvidia's China data-center revenue fell to $0 that quarter, down from $4.6B a year earlier [^47]. That is not a market-share loss measured in points; it is a line item going to zero [^47]. But the cause matters as much as the effect — the collapse tracks the tightening of U.S. export controls, not a documented case of Chinese buyers choosing Huawei silicon over Nvidia's on performance or price. Concession, in Huang's own framing, describes a regulatory wall Nvidia can no longer climb, not a battle it lost on a level field.

:::compare
- {role: "A YEAR AGO", name: "Nvidia China data-center revenue", value: "$4.6B"}
- {role: "TODAY", name: "Nvidia China data-center revenue", value: "$0"}
- {role: "SUBJECT", name: "Cause", value: "Export controls, not Huawei out-competing on merits"}
:::

Independent chip analysts reach a more measured verdict than the headline suggests. SemiAnalysis tracked DeepSeek V4 from Day 0 to Day 43 across Huawei Ascend, Nvidia GB300, AMD MI355X, and Nvidia B200, and concluded that Huawei "has proven it can sling a stone on Day 0; whether it can fell a moving giant is yet to be seen" [^48]. That is a real, credible capability claim — same-day inference support for a frontier open-weight model is not trivial — but it is explicitly not a claim that Huawei has closed the ecosystem gap with Nvidia globally: software maturity, developer tooling, and multi-year deployment track record all still favor the incumbent. The counterpoint here cuts against the loudest reading of both data points: Nvidia's China exit is a policy outcome, and Huawei's Day-0 win is a capability proof point, but neither adds up to a durable, worldwide displacement of Nvidia's ecosystem lead.

The irony sharpens once the frame widens past chips to weights. Just days before reports surfaced that China's Commerce Ministry (MOFCOM) is drafting export controls on Chinese AI model weights, Xi Jinping stood at the July 2026 World AI Conference in Shanghai and publicly championed open-source AI cooperation, warning against nations that prioritize their own security interests over others' [^46]. The MOFCOM draft — reportedly done in consultation with Alibaba, ByteDance, and Zhipu — would restrict foreign users from downloading the weight files of Chinese models while preserving cloud and API access, and separately floats barring TSMC and Qualcomm from fabricating chips based on Chinese company designs from Huawei, Alibaba, and ByteDance [^44,45]. Nothing is finalized; this is consultation-stage policy, not statute, and it could still be narrowed or shelved.

:::kv
- {term: "What's restricted", def: "Foreign download of model weight files"}
- {term: "What's preserved", def: "Cloud/API access for overseas customers"}
- {term: "Also considered", def: "Barring TSMC/Qualcomm from fabricating Chinese-designed chips"}
- {term: "Status", def: "Draft/consultation stage, nothing finalized"}
:::

:::statement(attr="ARA Research")
The same week China's president was publicly championing open AI as a global good, China's own commerce ministry was drafting rules to keep China's best open models from leaving the country.
:::

Why it matters: both halves of this mirror — Nvidia's rhetorical concession and Beijing's rhetorical about-face — say more about export-control gravity than about anyone winning a technical race. Nvidia's headline exit reflects policy, not proven inferiority; China's headline openness now runs into the same instinct every technology leader eventually has once its assets become strategic: keep the best of it close. If the MOFCOM draft lands, the "open-weight China" narrative that underpinned much of this article's revolt-of-200-firms story gets a lot more conditional, and DeepSeek's own open releases could become the next thing Beijing decides is too valuable to freely export [^44,45].

## 09. What could break this thesis

Every section above leans skeptical — toward "the headline number is thirdhand," "the ban isn't real yet," "the moat isn't cracked." That skepticism has a blind spot: it can shade into treating the case for restriction as pure economic self-interest (closed labs protecting revenue) or press exaggeration, when the strongest evidence against Chinese open-weight models comes from parties with no commercial stake in the outcome at all.

Two independent government-adjacent findings carry more weight than any lobbying letter. NIST's Center for AI Standards and Innovation found that DeepSeek models echo Chinese state/CCP narratives roughly four times as often as U.S. reference models on the same evaluation [^49]. Separately, Estonia's Foreign Intelligence Service — a state intelligence agency with no AI product to sell — found that DeepSeek "conceals key information and inserts Chinese propaganda" when answering questions about Estonia's own security [^50]. Neither finding is about distillation, IP theft, or pricing; both describe the model's behavior itself. That is a materially different, and harder to wave away, argument than "OpenAI and Anthropic want to protect a duopoly" — and this article's skepticism toward the ban debate has, until this section, mostly left it unaddressed.

OpenAI's Dean Ball makes a version of this case from outside the security-agency frame: an open-weight-model-dominant world, he argues, risks drifting toward "full AI communism" — his term for AI treated as state-provided infrastructure rather than a competitive market — which he calls a "dystopian hellscape," and he has floated using "soft law" advisories to manufacture regulatory uncertainty around Chinese models rather than seeking an outright ban [^51]. Read charitably, this is a coherent structural worry, not obviously a competitive maneuver; read skeptically, Ball works for a firm that would benefit commercially from exactly the outcome he's warning about. Both readings can be true at once, and this article has spent more space on the second than the first.

:::callout(kind=warn, label="What would falsify Section 2's core claim")
Section 2 argued DeepSeek's "hardware independence" is proven for inference but not for training, based on a reported 2025 failed Ascend training run. If DeepSeek's next flagship model trains successfully on Ascend silicon at frontier scale, that caveat collapses — and with it, much of the reason to doubt the more triumphalist "China has cracked the CUDA moat" reading of Sections 2 and 8.
:::

The chip-performance story in Section 3 also has an unresolved gap this article hasn't fully closed: DeepSeek's own internal benchmarking, per CSIS, put Huawei's Ascend 910C at roughly 60% of an Nvidia H100's inference performance [^2]. That is DeepSeek's own assessment of the gap, not a hostile external one — and a real, non-trivial performance deficit sits awkwardly next to the "2.8x H20" marketing figure for the newer 950PR discussed in the same section. Both numbers can be true (different chip generations, different comparison baselines), but read together they argue for real but partial progress, not parity.

Finally, the enforcement-feasibility argument this article leans on — that a possession ban is "ultimately impossible" once weights are public — rests more on analyst consensus than on a tested legal or technical record. No GAO or CRS report, and no named Congressional testimony transcript, was found addressing the actual mechanics of enforcing a ban on already-downloaded open-weight models [^43]. That is a genuine evidence gap, not a settled fact in Washington's favor: the "impossible to enforce" framing could turn out to be true, but it hasn't yet been tested against a real enforcement attempt, a subpoena, or a court challenge — and Washington's National AI Industry Investment Fund-style precedents (Section 4) suggest that when Beijing decided to embed itself inside DeepSeek's cap table, "impossible" turned out to mean "not yet attempted."

An adversarial pass on this article's three most load-bearing quantitative claims — DeepSeek's ~$52B June 2026 valuation, Nvidia's China data-center revenue falling from $4.6B to $0, and TileLang's claimed 5x/6x speedup over Triton — found no contradicting evidence for the first two after multiple independent searches; the third held up only as a best-case, workload-specific figure, which Section 2 now states explicitly rather than presenting as a general benchmark result.

None of this reverses the article's central finding — that most of what's circulating as an imminent "China AI ban" is still a menu of threatened and pending tools, not a completed action, and that the ~200-firm lobbying campaign is defending real, documented cost savings. But the strongest version of the case for restriction doesn't come from OpenAI or Anthropic's balance sheets; it comes from intelligence services and a federal standards body with nothing to sell. That case deserves to be weighed on its own evidence, not dismissed by association with the labs that happen to also benefit from it.

:::references
- {id: 1, title: "Interview with DeepSeek Founder: We're Done Following. It's Time to Lead.", url: "https://thechinaacademy.org/interview-with-deepseek-founder-were-done-following-its-time-to-lead/", source: "The China Academy", date: "2025-01-27"}
- {id: 2, title: "DeepSeek, Huawei, Export Controls, and the Future of the U.S.-China AI Race", url: "https://www.csis.org/analysis/deepseek-huawei-export-controls-and-future-us-china-ai-race", source: "CSIS", date: "2026-07-07"}
- {id: 3, title: "Exclusive: China's DeepSeek developing its own AI chip, sources say", url: "https://www.usnews.com/news/top-news/articles/2026-07-07/exclusive-chinas-deepseek-developing-its-own-ai-chip-sources-say", source: "Reuters / US News", date: "2026-07-07"}
- {id: 4, title: "President Xi attends symposium on private enterprises, delivers speech", url: "https://news.cgtn.com/news/2025-02-17/President-Xi-attends-symposium-on-private-enterprises-delivers-speech-1B3QqCUlZXG/p.html", source: "CGTN / Xinhua", date: "2025-02-17"}
- {id: 5, title: "Huawei founder told Xi China's 'core and soul' concerns have eased", url: "https://www.aol.com/news/huawei-founder-told-xi-chinas-015107530.html", source: "AOL / wire", date: "2025-02-21"}
- {id: 6, title: "tile-ai/tilelang", url: "https://github.com/tile-ai/tilelang", source: "GitHub", date: "2025-01-20"}
- {id: 7, title: "DeepSeek-V4 Technical Report", url: "https://arxiv.org/html/2606.19348v1", source: "arXiv", date: "2026-06"}
- {id: 8, title: "TileLang: A Composable Tiled Programming Model for AI Systems", url: "https://openreview.net/forum?id=Jb1WkNSfUB", source: "OpenReview", date: "2025-04"}
- {id: 9, title: "The chips are down: DeepSeek and Huawei's rocky AI romance", url: "https://www.theregister.com/2025/08/14/dodgy_huawei_deepseek/", source: "The Register, citing Financial Times", date: "2025-08-14"}
- {id: 10, title: "Huawei debuts Atlas 350 on Ascend 950PR with in-house HBM, touting 2.8x H20 performance", url: "https://www.trendforce.com/news/2026/03/23/news-huawei-debuts-atlas-350-on-ascend-950pr-with-in-house-hbm-touting-2-8x-h20-performance/", source: "TrendForce", date: "2026-03-23"}
- {id: 11, title: "Huawei Atlas 350 / Ascend 950PR AI accelerator vs Nvidia H20", url: "https://abit.ee/en/processors/huawei-atlas-350-ascend-950pr-ai-accelerator-nvidia-h20-fp4-hbm-china-ai-chips-en", source: "ABIT.ee", date: "2026-03-24"}
- {id: 12, title: "ByteDance, Alibaba planning to order Huawei's new AI chip: Reuters", url: "https://www.cnbc.com/2026/03/27/bytedance-alibaba-planning-to-order-huaweis-new-ai-chip-reuters.html", source: "CNBC / Reuters", date: "2026-03-27"}
- {id: 13, title: "Decoding DeepSeek V4: How Huawei's Ascend 950 PR is powering China's push to break CUDA dependence", url: "https://www.trendforce.com/news/2026/04/07/news-decoding-deepseek-v4-how-huaweis-ascend-950-pr-is-powering-chinas-push-to-break-cuda-dependence/", source: "TrendForce", date: "2026-04-07"}
- {id: 14, title: "Huawei Ascend production ramp", url: "https://newsletter.semianalysis.com/p/huawei-ascend-production-ramp", source: "SemiAnalysis", date: "2025-09-08"}
- {id: 15, title: "DeepSeek just raised $7.4 billion — here's the catch", url: "https://www.forbes.com/sites/anishasircar/2026/06/17/deepseek-just-raised-74-billion-heres-the-catch/", source: "Forbes", date: "2026-06-17"}
- {id: 16, title: "DeepSeek reaches $52 billion valuation in round backed by Tencent, CATL", url: "https://www.caixinglobal.com/2026-07-17/deepseek-reaches-52-billion-valuation-in-round-backed-by-tencent-catl-102465358.html", source: "Caixin Global", date: "2026-07-17"}
- {id: 17, title: "DeepSeek's golden-share structure", url: "https://finance.biggo.com/news/bb90b835-cbbe-4a7e-983f-fa0cdaa61d38", source: "BigGo Finance", date: "2026-07-15"}
- {id: 18, title: "DeepSeek weighs second fundraise at $71 billion valuation and eyes IPO as early as 2026", url: "https://techstory.in/deepseek-weighs-second-fundraise-at-71-billion-valuation-and-eyes-ipo-as-early-as-2026/", source: "TechStory, citing FT/Bloomberg", date: "2026-07-14"}
- {id: 19, title: "DeepSeek founder Liang Wenfeng's fortune rises to $36 billion", url: "https://technode.com/2026/07/15/deepseek-founder-liang-wenfengs-fortune-rises-to-36-billion/", source: "TechNode", date: "2026-07-15"}
- {id: 20, title: "Is Liang Wenfeng really worth $36 billion?", url: "https://thenextweb.com/news/liang-wenfeng-richest-ai-founder-deepseek-valuation", source: "The Next Web", date: "2026-07-14"}
- {id: 21, title: "Nearly 200 Silicon Valley startups urge Trump not to ban Chinese AI models", url: "https://www.chinatechnews.com/2026/07/23/126092-nearly-200-silicon-valley-startups-urge-trump-not-to-ban-chinese-ai-models-warn-it-could-kill-innovation", source: "China Tech News", date: "2026-07-23"}
- {id: 22, title: "Startup founders urge Trump not to shut off Chinese open-weight AI", url: "https://www.politico.com/news/2026/07/22/startup-founders-urge-trump-not-to-shut-off-chinese-open-weight-ai-01008992", source: "Politico", date: "2026-07-22"}
- {id: 23, title: "Little Tech Association", url: "https://littletech.org/", source: "Little Tech Association", date: "2026-07-13"}
- {id: 24, title: "The Little Tech Agenda", url: "https://a16z.com/the-little-tech-agenda/", source: "Andreessen Horowitz", date: "2024-07-01"}
- {id: 25, title: "Startup founders urge Trump not to shut off Chinese open-weight AI (syndicated)", url: "https://jingletree.com/startup-founders-urge-trump-not-to-shut-off-chinese-open-weight-ai-237211.html", source: "Jingletree", date: "2026-07-22"}
- {id: 26, title: "Trump administration reportedly reviving push to ban Chinese AI models following Kimi K3 launch", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/trump-administration-reportedly-reviving-push-to-ban-chinese-ai-models-following-kimi-k3-launch-citing-cybersecurity-concerns-downloadable-open-weights-could-make-an-outright-u-s-ban-nearly-impossible-to-enforce-amid-growing-adoption", source: "Tom's Hardware", date: "2026-07-22"}
- {id: 27, title: "Brian Armstrong on cutting Coinbase's AI bill", url: "https://x.com/brian_armstrong/status/2070670644577280109", source: "X / Brian Armstrong", date: "2026-06-27"}
- {id: 28, title: "OpenRouter State of AI 2025", url: "https://openrouter.ai/state-of-ai", source: "OpenRouter", date: "2026-01-15"}
- {id: 29, title: "China's AI model calls topped 12.96 trillion tokens", url: "https://en.people.cn/n3/2026/0408/c90000-20444562.html", source: "People's Daily Online", date: "2026-04-08"}
- {id: 30, title: "Snowflake CEO benchmarks China's GLM-5.2 within 1% of Claude Opus 4.7 at one-fifth the cost", url: "https://mlq.ai/news/snowflake-ceo-benchmarks-chinas-glm-52-within-1-of-claude-opus-47-at-one-fifth-the-cost/", source: "MLQ.ai", date: "2026-06-20"}
- {id: 31, title: "How Chinese AI models are undercutting OpenAI and Anthropic on cost", url: "https://www.cnbc.com/2026/07/07/chinese-ai-models-costs-us-openai-anthropic.html", source: "CNBC", date: "2026-07-07"}
- {id: 32, title: "The AI, US and China: Kimi, open-source weights and Trump", url: "https://www.axios.com/2026/07/20/ai-us-china-open-source-kimi", source: "Axios", date: "2026-07-20"}
- {id: 33, title: "No Adversarial AI Act, H.R. 4142", url: "https://www.congress.gov/bill/119th-congress/house-bill/4142/text", source: "Congress.gov", date: "2025-06-25"}
- {id: 34, title: "House panels probe Airbnb, Anysphere over use of Chinese AI models", url: "https://www.nextgov.com/artificial-intelligence/2026/04/house-panels-probe-airbnb-anysphere-over-use-chinese-ai-models/413207/", source: "Nextgov/FCW", date: "2026-04-29"}
- {id: 35, title: "Bessent: US to review Chinese AI models for IP theft, weighs sanctions", url: "https://www.cnbc.com/2026/07/21/bessent-china-ai-sanctions.html", source: "CNBC", date: "2026-07-21"}
- {id: 36, title: "China's Moonshot AI releases Kimi K3, the largest open-source model ever", url: "https://venturebeat.com/technology/chinas-moonshot-ai-releases-kimi-k3-the-largest-open-source-model-ever-rivaling-top-u-s-systems", source: "VentureBeat", date: "2026-07-17"}
- {id: 37, title: "David Sacks on open-source AI and the Trump administration", url: "https://www.axios.com/2026/07/17/sacks-kimi-open-source-weights-trump", source: "Axios", date: "2026-07-19"}
- {id: 38, title: "Addition of Entities to the Entity List (Zhipu AI)", url: "https://www.federalregister.gov/documents/2025/01/16/2025-00704/addition-of-entities-to-and-revision-of-entry-on-the-entity-list", source: "Federal Register / BIS", date: "2025-01-16"}
- {id: 39, title: "Huawei Q4 smartphone shipments plunge 41% as U.S. sanctions bite", url: "https://www.cnbc.com/2021/01/28/huawei-q4-smartphone-shipments-plunge-41percent-as-us-sanctions-bite.html", source: "CNBC", date: "2021-01-28"}
- {id: 40, title: "Backfire: How export controls helped Huawei and hurt US firms", url: "https://itif.org/publications/2025/10/27/backfire-export-controls-helped-huawei-and-hurt-us-firms/", source: "ITIF", date: "2025-10-27"}
- {id: 41, title: "There Is No General First Amendment Right To Distribute Machine Learning Model Weights", url: "https://www.lawfaremedia.org/article/there-is-no-general-first-amendment-right-to-distribute-machine-learning-model-weights", source: "Lawfare", date: "2024-04-04"}
- {id: 42, title: "Are AI Model Weights Protected Speech Under the First Amendment?", url: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6538918", source: "SSRN", date: "2026-03-26"}
- {id: 43, title: "Open-weight AI leaves Washington facing a ban it cannot enforce", url: "https://www.opensourceforu.com/2026/07/open-weight-ai-leaves-washington-facing-a-ban-it-cannot-enforce/", source: "Open Source For You", date: "2026-07-14"}
- {id: 44, title: "China considers tighter export controls on AI models", url: "https://finance.yahoo.com/technology/ai/articles/china-considers-tighter-export-controls-041139427.html", source: "Yahoo Finance, citing Reuters/FT", date: "2026-07-21"}
- {id: 45, title: "China is considering export controls on AI technologies, including banning local companies from using TSMC", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/china-is-considering-export-controls-on-ai-technologies-including-banning-local-companies-from-using-tsmc-report-claims-restrictions-would-also-advanced-ai-models-training-data-and-overseas-acquisitions", source: "Tom's Hardware", date: "2026-07-21"}
- {id: 46, title: "Xi Jinping, WAIC, and China's open-source AI governance", url: "https://qz.com/xi-jinping-waic-china-open-source-ai-governance-071726", source: "Quartz", date: "2026-07-17"}
- {id: 47, title: "Nvidia CEO Jensen Huang: we've largely conceded the China AI-chip market to Huawei", url: "https://www.cnbc.com/2026/05/21/nvidia-jensen-huang-china-ai-chip-market-huawei.html", source: "CNBC", date: "2026-05-21"}
- {id: 48, title: "DeepSeek V4: 16T, Day 0 to Day 43 performance", url: "https://newsletter.semianalysis.com/p/deepseekv4-16t-day-0-to-day-43-performance", source: "SemiAnalysis", date: "2026-06-09"}
- {id: 49, title: "CAISI evaluation of DeepSeek AI models finds shortcomings and risks", url: "https://www.nist.gov/news-events/news/2025/09/caisi-evaluation-deepseek-ai-models-finds-shortcomings-and-risks", source: "NIST", date: "2025-09-30"}
- {id: 50, title: "Chinese artificial intelligence distorts perceptions", url: "https://raport.valisluureamet.ee/2026/en/6-asia/6-3-chinese-artificial-intelligence-distorts-perceptions/", source: "Estonian Foreign Intelligence Service", date: "2026-02-10"}
- {id: 51, title: "Dean Ball on open-weight AI and \"full AI communism\"", url: "https://x.com/deanwball/status/2078133895766114412", source: "X / Dean Ball", date: "2026-07-17"}
:::
