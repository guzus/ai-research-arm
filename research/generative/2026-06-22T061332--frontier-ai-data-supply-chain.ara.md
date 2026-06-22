---
eyebrow: ARA RESEARCH · AI DATA SUPPLY CHAIN
title: "The data behind the models: inside the industry that sells human cognition to frontier AI labs"
deck: A first-principles map of the ~$5B/year business selling expert data, RLHF, evals, environments and rights-cleared content to a customer base of barely a dozen labs — and why its headline numbers are mostly mirage.
domain: finance
lede: |
  In June 2025, Meta paid roughly $14.3 billion for 49% of Scale AI and hired away its founder. Within a week, Google, OpenAI and xAI began walking out the door. The deal exposed the open secret of frontier AI: the models are only as good as the human data poured into them, that data is bought from a handful of vendors, and the whole industry rests on a customer base you could fit in one conference room. This is a map of that industry — who sells, what they actually earn once you strip the labor pass-through, and whether the business survives its own customers learning to do without it.
stats:
  - {label: Frontier-lab external data spend, value: "~$4.5B", note: "2025, bottom-up est."}
  - {label: Customers that matter, value: "~6–12", note: frontier labs}
  - {label: Meta's stake in Scale AI, value: "$14.3B", note: 49% non-voting}
  - {label: Contractor pass-through, value: "40–70%", note: of vendor "revenue"}
---

## 01. The shape of the supply chain

The popular story of AI progress is about compute: GPUs, datacenters, power. The quieter story is about data — specifically, the human-generated and human-judged data that turns a raw pretrained model into something useful. Pretraining on scraped web text is nearly tapped out; the marginal capability dollar has moved to *post-training* — supervised fine-tuning, reinforcement learning from human feedback (RLHF), reasoning traces, agentic task trajectories, and evaluations.[^1,47] That work is largely bought, not scraped, and an industry has grown up to sell it.

The supply chain has six distinguishable layers: **expert human data and RLHF** (Scale, Surge, Mercor); **coding and STEM task data** (Turing, Invisible, Micro1); **evals and benchmarks** (Scale SEAL, Epoch, LMArena); **RL environments** (Mechanize, Prime Intellect, plus incumbents' new divisions); **rights-cleared content licensing** (Reddit, Shutterstock, news publishers); and **synthetic-data tooling** (Gretel, now part of NVIDIA). What unites them is a brutal structural fact: there are only about six to twelve buyers on Earth — OpenAI, Anthropic, Google DeepMind, Meta, xAI, Microsoft, Amazon, and a thin tail of well-capitalized labs — and they account for nearly all the revenue.[^4,7]

:::statement(attr="ARA Research")
The frontier-AI data industry is a market with a dozen customers, billion-dollar valuations, and revenue figures that are mostly someone else's wages passing through.
:::

How big is it? Smaller than the headlines suggest, and the headlines disagree wildly with each other. Vendor-funded TAM reports put the "data-labeling market" anywhere from ~$1.1B to $3.8B in the current year with 22–35% CAGRs — a 3.5x spread for ostensibly the same market, a tell that the category is being measured incoherently.[^2] A cleaner bottom-up estimate — summing what the top labs actually pay external vendors, using *net* economics where revenue is a labor pass-through — lands around **$4–5.5 billion per year in 2025**, with content licensing adding perhaps $0.3–0.8B more.[^3,4] The "tens of billions by 2030" projections are the least reliable figures in the entire chain.

This article's organizing claim is a first-principles correction the whole sector resists: ==most of what is reported as "revenue" or "ARR" in this industry is gross billings, 40–70% of which is contractor pay flowing straight through to the people who actually produce the data.== Get that wrong and you misprice every vendor in the stack.

## 02. The great reshuffle: Scale falls, Surge and Mercor rise

For years Scale AI *was* the data industry. By 2024 it booked roughly $870M in revenue, exited the year at a ~$1.5B run-rate, and projected $2B for 2025.[^5] Then Meta bought 49% of it for ~$14.3B in June 2025, valued it near $29B, and took CEO Alexandr Wang to run Meta Superintelligence Labs.[^6] The investment was supposed to be a coup. It was closer to a controlled demolition of Scale's frontier-lab franchise.

The problem is structural, not reputational: a data vendor co-owned by one frontier lab cannot credibly serve that lab's rivals, who must hand over their proprietary training priorities to produce the data. Google — Scale's largest customer at ~$150M in 2024, with ~$200M budgeted for 2025 — moved to split; OpenAI began phasing Scale out (calling it "a small fraction" of its needs); Microsoft and xAI pulled back.[^7,8] By July 2025 Scale laid off 200 staff (14%) plus ~500 contractors and collapsed its generative-AI org from 16 groups to 5, with interim CEO Jason Droege conceding it had "scaled too quickly."[^9] Scale pivoted hard toward government, expanding a Pentagon CDAO agreement ceiling from $100M to $500M[^10] — a real business, but a far smaller and slower-moving market than frontier post-training.

The spend did not vanish; it *rotated* to vendors that were still neutral. Two beneficiaries stand out.

:::rank-list
- {label: "Surge AI — FY2024 revenue (bootstrapped)", value: ">$1.0B", pct: 100, highlight: true}
- {label: "Scale AI — FY2024 revenue", value: "$0.87B", pct: 87}
- {label: "Mercor — run-rate (Oct 2025 → est. May 2026)", value: "$0.45–1.5B", pct: 70}
- {label: "Turing — ARR (Mar 2025)", value: "~$0.30B", pct: 30}
- {label: "Innodata — FY2025 revenue (public)", value: "~$0.25B", pct: 25}
- {label: "Invisible Technologies — FY2024 revenue", value: "$0.13B", pct: 13}
:::

**Surge AI** is the industry's quiet giant. Bootstrapped by founder Edwin Chen with no outside funding, it booked *more than $1 billion in full-year 2024 revenue* — out-earning Scale's $870M on a like-for-like basis — with only ~110–130 employees and a network of ~50,000 vetted contractors.[^11] Anthropic is a named customer; co-founder Jared Kaplan has called Surge "an excellent partner."[^12] In mid-2025 Surge sought its first outside round — ~$1B at a valuation negotiated from ~$15B up toward ~$25B.[^13] One caveat worth flagging: the widely-quoted "$1.2B" Surge figure is an *annualized* run-rate, not the FY booked number, and the two get conflated constantly.

**Mercor** is the fastest riser. Founded by three Thiel Fellows, it matches credentialed domain experts — physicians, lawyers, PhDs, quants — to labs for high-end RLHF and evals. Its run-rate went from ~$1M to ~$100M to a reported $450M+ in roughly 18 months, and it raised a $350M Series C at a **$10B valuation in October 2025**, quintupling its February mark.[^14] But Mercor is the cleanest illustration of this article's thesis, which its own CEO confirms.

:::quote(attr="Brendan Foody, CEO, Mercor — to TechCrunch, Sept 2025")
The company's revenue includes the total amount that customers pay Mercor for services before its contractors receive their portion.
:::

That is gross accounting. With ~60–70% of every dollar passing through to contractors, Mercor's ~$10B valuation sits on roughly $150M of *net* run-rate — pricing it at ~65x net revenue for a business with the margin profile of a staffing agency, not software.[^15] The growth is real; the multiple is a bet on the future, not on present-day economics. Notably, even Scale's lawsuit against Mercor in September 2025 — alleging an ex-employee took 100+ confidential customer documents — underscores how *contestable* these customer relationships are: the people, the experts, and the contracts all move freely between vendors.[^16]

## 03. Gross vs. net: the industry's most misleading number

Why does "ARR" mislead so badly here? Because data labeling is a *labor-pass-through* business, not a software-license business. When a lab pays Mercor or Scale, most of the money is marked-up contractor hours. The vendor's true economic value-add is the thin layer on top: sourcing, vetting, quality control, workflow tooling, and trust. That layer is real — but it is a fraction of the headline.

The only *audited* window into the margin structure is Innodata (NASDAQ: INOD), the lone public pure-play. Its FY2025 gross margin ran **~40%** (GAAP) on ~$251.7M revenue — roughly half a typical SaaS gross margin of 75–85%.[^17] Private estimates put Scale around 50%+ gross margin and expert marketplaces like Mercor at a ~30% take rate.[^15,18] In every case, the missing 40–70% is the contractor wage bill.

:::bar-chart(title="The pass-through gap: vendor share vs. contractor share of billings", subtitle="approximate; expert marketplaces pass through the most", orientation=horizontal, mode=stacked, value-suffix=%)
categories: Innodata (audited GM), Scale AI (est.), Mercor (est. take-rate)
Vendor retains: 40, 50, 32
Passes to labor / direct cost: 60, 50, 68
:::

This reframes the valuation conversation entirely. A vendor doing "$1B in ARR" at a 30% take rate has ~$300M of net revenue; at SaaS-like multiples that supports a very different valuation than the gross number implies. It also explains the profitability divergence: Surge, Invisible (~11% EBITDA margin on $134M FY24 revenue), and Turing report profitability, while Scale restructured.[^19,26] The model itself is sound — contractor cost is *variable*, so disciplined markup yields profit at any scale. Scale's losses came from fixed-cost overbuild plus the Meta demand shock, not from broken unit economics.

The counterpoint: a concentrated buyer base can be *sticky* if QC and trust are genuinely differentiated, and a few vendors (Surge's elite-contractor curation, Turing's embedded-engineer model) may command durable premiums. But "ARR" as a metric papers over the difference between a software annuity and re-competed services revenue that resets every model cycle. Why this matters: when frontier-lab capex eventually cools, gross run-rates priced at 25–65x will reprice fastest in exactly the names whose moat is volume, not trust.

## 04. The contractor economy: $0.90 to $200 an hour

If the vendors' revenue is mostly contractor pay, then the contractor economy *is* the industry's cost structure — and it is brutally bifurcated. At the bottom sits commodity annotation, sourced from the global South via labor arbitrage. At the top sit credentialed experts in the US and Europe, paid more than many of the engineers building the models.

:::compare
- {role: LOWEST, name: "Remotasks, Venezuela (avg)", value: "~$0.90/hr"}
- {role: HIGHEST, name: "Mercor — US physicians", value: "~$200/hr"}
- {role: SUBJECT, name: "Mercor — platform average", value: "~$85/hr"}
:::

The canonical floor case is Sama's work for OpenAI in Kenya, labeling toxic content to build ChatGPT's safety filters: workers took home **$1.32–$2 per hour** while OpenAI was billed ~$12.50/hour — roughly a 6x markup, and the single sharpest illustration of gross-vs-net at the commodity tier.[^20] Remotasks workers in Venezuela averaged ~$0.90/hour; in March 2024 the platform abruptly pulled out of Kenya, Nigeria and Pakistan, with some workers reporting less than a dollar for 20+ hours of completed tasks.[^21]

The top tier is a different market. As models saturate easy benchmarks, labs pay for data at the *edge of human knowledge* — and price it accordingly. Mercor's listings reportedly pay physicians ~$200/hr, finance experts ~$150/hr, and biology PhDs $60–80/hr, with the platform averaging ~$85/hr.[^8,22] Scale's Outlier platform spans roughly $15–60/hr depending on task and credentials.[^23] The trajectory is unmistakable: the marginal data dollar is migrating *up* the expertise curve, because the data labs still can't get cheaply is exactly the frontier-expert judgment that defines the next capability jump.

That migration carries legal risk that is now materializing. Scale/Outlier faces multiple California wage-misclassification suits and a US Department of Labor investigation, with one complaint alleging ~$15/hr effective pay below minimum wage after unpaid training and review time.[^24] In Kenya, courts settled jurisdiction in September 2024 to let content moderators try Western firms over labor conditions — making the buyers, not just the BPO vendors, justiciable.[^25] The EU's Platform Work Directive reclassifies many gig workers but sets no wage floor and won't bite until December 2026. The teeth are latent, not yet realized — but they target precisely the misclassification that enables the low effective payout.

:::callout(kind=warn, label=Risk)
The industry's margin depends on the gap between what labs pay and what workers receive. Three triggers would compress it: a Kenyan court enforcing back-pay with penalties, EU transposition naming data platforms, or a California ABC-test ruling reclassifying contractors as employees.
:::

## 05. The neutrality moat — the one thing Scale can't buy back

The Meta–Scale deal accidentally revealed the industry's single most durable moat: **neutrality**. A data vendor's value to a frontier lab includes a promise that its training priorities won't leak to a competitor. The moment Meta took 49% of Scale, that promise broke for everyone else — and it broke *irreversibly*, because Scale cannot un-sell the stake.

This is textbook counter-positioning. Surge, Mercor, Turing and Invisible can offer something the category leader structurally cannot: independence from any single lab. The proof is in Meta's own behavior. Its flagship TBD Lab — the ~50-person unit training Meta's frontier models — reportedly routes its data work to **Surge and Mercor**, not the Scale data Meta part-owns, with researchers viewing Scale's data as lower quality.[^27] Meta bought a data vendor and then declined to eat its own cooking.

:::timeline
- {date: 2025-06, headline: "Meta buys 49% of Scale ($14.3B)", body: "Alexandr Wang departs to lead Meta Superintelligence Labs."}
- {date: 2025-06, headline: "The exodus", body: "Google moves to split; OpenAI phases Scale out; Microsoft and xAI pull back."}
- {date: 2025-07, headline: "Scale restructures", body: "14% layoffs; GenAI org cut from 16 groups to 5; pivot toward government."}
- {date: 2025-08, headline: "Meta's own lab defects", body: "TBD Lab reported to use Surge and Mercor over Scale data."}
- {date: 2025-10, headline: "Mercor hits $10B", body: "$350M Series C, 5x its February valuation, on neutral-vendor demand."}
:::

But neutrality is the *only* clean moat, and the others are softer than the bull case admits. Contractor supply is poachable (the Scale–Mercor lawsuit litigates documents precisely because the people move freely).[^16] Switching costs are low: labs multi-home and re-compete contracts every model cycle, which caps everyone's pricing power. The durable value, where it exists, lives in QC, workflow integration, and reputation — not in the size of a contractor pool that any well-funded rival can rent away. Why this matters: it means the category can grow while individual franchises stay fragile, exactly as Scale demonstrated.

## 06. Data as IP: the content-licensing layer

A parallel market sells *existing* corpora rather than freshly-produced labels: publishers, image libraries, and forums licensing rights-cleared content. It is roughly an order of magnitude smaller than labeling, and the best public window into it — Reddit's filings — is flashing yellow.

Reddit (NYSE: RDDT) signed a ~$60M Google AI-training license in February 2024 and a later undisclosed OpenAI deal.[^28] Its content-licensing revenue, buried inside "Other revenue," stepped up sharply on those signings — then plateaued. Other revenue ran ~$33.2M in Q3 2024 and ~$33.7M in Q1 2025; the ~$253M of remaining performance obligations disclosed in its FY2024 10-K are dominated by these fixed-term licensing contracts, recognizing on a flat-to-declining schedule rather than compounding.[^29] That is not a flywheel; it is a step-change followed by a flat line.

:::line-chart(title="Reddit 'Other revenue' (content licensing-heavy), $M/quarter", subtitle="SEC filings — step-up then plateau", y-unit=$)
x: Q1-24, Q2-24, Q3-24, Q1-25, Q1-26
Other revenue: 20.3, 28.1, 33.2, 33.7, 39.0
:::

Shutterstock (NYSE: SSTK) tells a steadier story: pure AI-data revenue more than quintupled to $104M in FY2023, and its "Data, Distribution and Services" segment reached $203.3M (21% of total revenue) in FY2025, with management targeting ~$250M annually by 2027.[^30] Only OpenAI is company-named (a six-year deal from July 2023); other big-tech counterparties and the reported $25–50M-per-deal band are press-sourced.

The instructive contrast is Getty Images, the lone holdout that chose to *litigate* rather than license — and largely lost. The UK High Court rejected Getty's core copyright claims against Stability AI on November 4, 2025 (partly on jurisdiction), leaving only a narrow trademark issue; a US trial isn't expected until 2028.[^31] Getty is now merging with Shutterstock — folding the litigator into the licenser. The verdict the market is reaching: license, don't sue.

:::kv
- {term: Cleanest disclosed cash floor, def: "Dotdash Meredith ≥$16M/yr (from IAC filings)"}
- {term: Biggest headline deal, def: "News Corp–OpenAI >$250M/5yr — but partly OpenAI credits, so cash < headline"}
- {term: Recurring API model, def: "Stack Overflow OverflowAPI (Google, OpenAI) — terms undisclosed"}
- {term: The catch, def: "Many deals are bidirectional — the publisher also buys the lab's product"}
:::

## 07. What the public filings reveal

Three public companies offer the only audited glimpse into an otherwise private industry — and each tells a different chapter of the same story.

**Appen (ASX: APX)** is the cautionary tale of commodity dependence. The former crowd-data leader's revenue collapsed from a US$388.5M peak in FY2022 to US$234.3M in FY2024 after Google terminated its ~US$82.8M contract in January 2024.[^32] Appen's equity is down roughly 97% from its 2020 peak. It has clawed back to *adjusted* growth (+16% in FY24, driven by generative-AI work, with China up 70.7%), but only ex-Google; statutory revenue kept falling.[^33] CEO Ryan Kolln's framing is the industry's universal aspiration:

:::quote(attr="Ryan Kolln, CEO, Appen — H1 FY2025 results")
The companies best positioned to deliver trusted, scalable data will be those that shape the next generation of AI development.
:::

**TELUS Digital (NYSE: TIXT)** shows the same Google-concentration risk resolving differently. Google was its second-largest client at 14.3% of 2024 revenue; rather than re-rate in public markets, parent TELUS took the company private at US$4.50/share (~$539M, a 32% bump over its initial offer), closing October 31, 2025.[^34] Notably, the filings contain **no standalone "AI Data Solutions" revenue line** — it's a service line, not a reportable segment — so any precise figure circulating for it is an estimate, not a disclosure.

**Innodata (NASDAQ: INOD)** is the rare legacy BPO that genuinely converted into a frontier supplier. FY2025 revenue rose ~45%+ to ~$251.7M, and it counts five of the "Magnificent Seven" plus three other big-tech firms as customers.[^17,35] But its filings also expose the sector's defining risk in audited form: **one customer is ~56–58% of total revenue.**[^35] That concentration is simultaneously the proof of frontier relevance and the dominant investment risk — the same coin, two faces, for every vendor in this report.

:::donut(center-label="~58%")
- {label: "Top single Big-Tech customer", value: 58}
- {label: "All other customers", value: 42}
:::

## 08. Evals, benchmarks, and the new RL-environment frontier

As models saturate public benchmarks, an adjacent market sells *measurement*: private, uncontaminated evaluations, and — increasingly — the reinforcement-learning environments labs use to train agents. The economic engine is **benchmark perishability**. A public benchmark, once saturated or contaminated, yields no signal; labs must continually re-buy fresh, held-out, expert-authored tests. That makes eval revenue recurring rather than one-time.

It also makes the layer riddled with conflicts of interest. Scale markets its SEAL leaderboards as neutral and added a self-imposed 60-day data-segregation rule — but the safeguard is first-party, and Scale sells the training data *and* grades the models. The starkest case is Epoch AI's FrontierMath: OpenAI funded the benchmark and had access to many of its problems, disclosed only at o3's launch.[^36] Even nominally crowdsourced LMArena — which raised a ~$100M seed at ~$600M in May 2025 — drew a peer-reviewed critique ("The Leaderboard Illusion") arguing its policies structurally favored a few large providers.[^37] No major benchmarker is cleanly independent; the capture channels merely differ.

The hot new sub-category is **RL environments** — executable, verifiable task worlds (a simulated browser, a codebase, a software replica) in which agents are trained against machine-checkable rewards. Reporting (single-sourced, and worth treating as directional) says Anthropic leaders *discussed* spending more than $1 billion on RL environments over a single year, with rivals in a similar range.[^38] The supply side is still tiny relative to that demand: pure-plays like Prime Intellect (~$70M raised, an open Environments Hub) and Mechanize sit alongside new divisions inside Surge, Mercor and Scale.

:::stats
- {label: Environment contract size, value: "7-figures", unit: "/qtr"}
- {label: Per-task pricing, value: "$200–2,000"}
- {label: Software-replica environment, value: "~$300K"}
- {label: Exclusivity premium, value: "4–5×"}
:::

A caution on sizing: the "$1B RL-environment market" framing conflates one lab's internal budget *discussion* with incumbents' total labeling revenue. There is no audited RL-environment market figure, and much of the spend is a *subset* of the $4–5.5B external-data total, not additive to it.[^38]

## 09. The bear case: synthetic data and the melting commodity tier

The most serious threat to this industry is that its customers learn to need it less. Two forces drive the bear case: synthetic data and sample efficiency.

On synthetic data, the marketing ("synthetic is replacing human data") is about 70% wrong as literally stated, but right in spirit. The commercial synthetic-data *vendors* — Gretel (acquired by NVIDIA in March 2025 for a reported nine figures), Mostly AI, Tonic — are overwhelmingly an *enterprise privacy and simulation* category; they are not documented suppliers of frontier-LLM training data.[^39] The real synthetic story is internal and model-generated. NVIDIA's Nemotron-4 340B used **>98% synthetically generated alignment data** — but the reward model that filtered all of it was trained on only ~10,000 real human preferences.[^40] "98% synthetic" is a *volume* statistic hiding a 2% dependency that the entire loop pivots on.

The deeper finding is that model collapse — the degeneration from training on recursively generated data — is real but *conditional*. The canonical Nature result holds under indiscriminate, recursive *replacement* of real data with synthetic.[^41] But accumulating synthetic data *alongside* retained real data avoids collapse, and a verifier — even an imperfect one — that filters synthetic samples makes them net-positive.[^42] Modern post-training is exactly this filtered regime, which is why empirically observed collapse is mild. Synthetic data scales the body; human-derived signal (constitutions, reward models, verifiable ground truth) remains the spine.

:::callout(kind=info, label="The verifiable-reward wedge")
DeepSeek-R1-Zero showed that pure RL with verifiable rewards can elicit reasoning with *no* human-labeled reasoning traces — peer-reviewed in Nature.[^43] This genuinely removes humans from the loop, but only where ground truth is machine-checkable (math, code). It is the sharpest bear datapoint and the clearest boundary of it.
:::

On sample efficiency, papers like LIMA (1,000 examples for alignment) and s1 (1,000 curated samples for o1-style reasoning) show that *per-capability* human-label intensity is falling fast for commodity tasks.[^44] Ilya Sutskever's "we've achieved peak data" and Elon Musk's agreement that training data is exhausted point the same way.[^45] So is the industry a melting ice cube?

The honest answer is a Jevons-paradox reading, not a collapse. Per-unit human-label intensity is falling — *and total dollar demand grew roughly 10x year-over-year in 2025* (Mercor alone went from ~$75M to a ~$840M run-rate in eight months).[^14] The reconciliation is mix-shift: the cheap, high-volume, crowd-labeling tier genuinely *is* a melting ice cube (RLAIF-substitutable, RLVR-displaced), while growth concentrates in expensive frontier-expert data and hand-built environments — work that is harder to automate because authoring the verifier *is* the expert task. The ice cube is the bottom rung, not the industry. But the bear hedge is real: the 10x growth is downstream of frontier-lab capex, and if that cools, gross run-rates priced at 25–65x reverse fast.

## 10. What the labs need next

The demand side, stated on the correct axis, is growing and recurring — and migrating predictably. Four vectors define 2026+ data demand:

:::kv
- {term: Agentic trajectories, def: "Recorded multi-step tool/browser/coding-agent task data, productized as RL environments — the fastest-growing line."}
- {term: Frontier-expert knowledge, def: "PhD/MD/lawyer/quant-level data at the edge of human knowledge, as easy benchmarks saturate."}
- {term: Verifiable + rubric rewards, def: "Cheap to scale in code/math via RLVR; soft domains now need expert-authored rubrics — which grows expert demand."}
- {term: Multimodal & embodied, def: "Video, audio, 3D and robotics data — a real but mostly separate 2027–2030 scarcity, not a 2026 LLM driver."}
:::

The throughline is that each capability jump *opens* new data needs rather than closing them. When reasoning got solved in verifiable domains, demand moved to agentic and soft-domain tasks where verification itself requires judgment. Rubric-based RL — decomposing a soft task into expert-authored criteria an LLM-judge scores — is the current frontier, and authoring accurate rubrics in medicine, law and science is expert work that *expands* the human-data market upmarket.[^1] The labs are simultaneously insourcing the highest-value, most-sensitive work (Meta's large internal data-generation unit, reportedly thousands of transferred engineers[^48]; xAI's ~1,500 in-house "AI tutors"[^46]; OpenAI's and Anthropic's internal Human Data teams) while outsourcing expert labor and surge capacity to neutral vendors. Insourcing and outsourcing are not opposites here; they target different tiers. The exposed instrument is vendor *take-rate* on the most valuable work, not vendor existence.

## 11. What could break the thesis

Several load-bearing claims here deserve their strongest counter-arguments.

**The numbers are mostly private and self-reported.** Only Innodata is audited; every Scale/Surge/Mercor/Turing figure is leaked, estimated, or company-sourced, and "run-rate" overstates net economics throughout. The bottom-up ~$4.5B market estimate carries wide error bars and depends on take-rate assumptions that could be off by half.[^3]

**Customer concentration cuts both ways.** A dozen buyers is a fragility (Innodata's ~58%-of-revenue customer, Scale's overnight exodus) — but few, deep, high-trust relationships can also be sticky and hard to dislodge. The same concentration that looks like risk can read as moat.

**Synthetic and sample-efficiency could move faster than mix-shift.** RLAIF is already substituting for human preference data, and RLVR genuinely removes humans in verifiable domains. If verifiable-reward methods generalize to soft domains faster than expected, the expert-data growth that offsets the melting commodity tier could stall. The bear case is about timing and durability, not direction.

**Red-team pass.** Independent adversarial checks of this article's three load-bearing claims — Surge out-earning Scale on FY2024, the ~$14.3B/49% Meta–Scale deal, and the gross-vs-net pass-through thesis — surfaced no contradicting primary sources; the claims survived the falsification attempt. The figures most worth distrusting are the forward and private ones: the >$1B RL-environment budget (single-sourced), the $4–5.5B market total (estimate), and any vendor "ARR" quoted without its take-rate.

The synthesis: this is a real, fast-growing industry built on an unusually fragile foundation — a dozen customers, a poachable workforce, headline numbers inflated by labor pass-through, and a live debate over whether its customers are about to need it less. The neutral expert-data and environment vendors look structurally advantaged; the commodity labelers and any single compromised incumbent look exposed. The durable bet is not on the headline revenue. It is on whichever vendors own the trust and the verification layer — the parts a frontier lab can't cheaply rent, poach, or synthesize away.

:::references
- {id: 1, title: "An FAQ on Reinforcement Learning / post-training data", url: "https://epochai.substack.com/p/an-faq-on-reinforcement-learning", source: Epoch AI, date: "2026-01-12"}
- {id: 2, title: "Data Collection and Labeling Market", url: "https://www.grandviewresearch.com/industry-analysis/data-collection-labeling-market", source: Grand View Research, date: "2024"}
- {id: 3, title: "Surge AI company profile (revenue, customers)", url: "https://sacra.com/c/surge-ai/", source: Sacra, date: "2025"}
- {id: 4, title: "Scale AI company profile (revenue, margin)", url: "https://sacra.com/c/scale-ai/", source: Sacra, date: "2025"}
- {id: 5, title: "Scale AI expects to more than double sales to $2B in 2025", url: "https://www.bloomberg.com/news/articles/2025-04-02/scale-ai-expects-to-more-than-double-sales-to-2-billion-in-2025", source: Bloomberg, date: "2025-04-02"}
- {id: 6, title: "Scale AI founder Wang announces exit for Meta, part of $14B deal", url: "https://www.cnbc.com/2025/06/12/scale-ai-founder-wang-announces-exit-for-meta-part-of-14-billion-deal.html", source: CNBC, date: "2025-06-12"}
- {id: 7, title: "Google, Scale AI's largest customer, plans split after Meta deal", url: "https://www.cnbc.com/2025/06/14/google-scale-ais-largest-customer-plans-split-after-meta-deal.html", source: CNBC, date: "2025-06-14"}
- {id: 8, title: "OpenAI drops Scale AI as a data provider following Meta deal", url: "https://techcrunch.com/2025/06/18/openai-drops-scale-ai-as-a-data-provider-following-meta-deal/", source: TechCrunch, date: "2025-06-18"}
- {id: 9, title: "Scale AI lays off 14% of staff, largely in data-labeling business", url: "https://techcrunch.com/2025/07/16/scale-ai-lays-off-14-of-staff-largely-in-data-labeling-business/", source: TechCrunch, date: "2025-07-16"}
- {id: 10, title: "Scale AI–Pentagon CDAO $500 million agreement", url: "https://scale.com/blog/Scale-ai-pentagon-cdao-500-million-agreement", source: Scale AI, date: "2025-09-01"}
- {id: 11, title: "Bootstrapped to $1 billion: Surge AI CEO Edwin Chen", url: "https://www.inc.com/sam-blum/bootstrapped-to-1-billion-surge-ai-ceo-edwin-chen-on-how-he-did-it/91207937", source: Inc., date: "2025-07"}
- {id: 12, title: "Anthropic + Surge AI RLHF platform", url: "https://surgehq.ai/blog/anthropic-surge-ai-rlhf-platform-train-llm-assistant-human-feedback", source: Surge AI, date: "2023-03-09"}
- {id: 13, title: "Scale rival Surge AI in talks for funding at $25 billion value", url: "https://www.bloomberg.com/news/articles/2025-07-30/scale-rival-surge-ai-in-talks-for-funding-at-25-billion-value", source: Bloomberg, date: "2025-07-30"}
- {id: 14, title: "Mercor quintuples valuation to $10B with $350M Series C", url: "https://techcrunch.com/2025/10/27/mercor-quintuples-valuation-to-10b-with-350m-series-c/", source: TechCrunch, date: "2025-10-27"}
- {id: 15, title: "AI training startup Mercor eyes $10B valuation on $450M run-rate", url: "https://techcrunch.com/2025/09/09/sources-ai-training-startup-mercor-eyes-10b-valuation-on-450m-run-rate/", source: TechCrunch, date: "2025-09-09"}
- {id: 16, title: "Scale AI is suing a former employee and rival Mercor", url: "https://techcrunch.com/2025/09/03/scale-ai-is-suing-a-former-employee-and-rival-mercor-alleging-they-tried-to-steal-its-biggest-customers/", source: TechCrunch, date: "2025-09-03"}
- {id: 17, title: "Innodata reports third quarter 2025 results", url: "https://www.stocktitan.net/news/INOD/innodata-reports-third-quarter-2025-mv9ywlam30wi.html", source: "Innodata 8-K (via StockTitan)", date: "2025-11-06"}
- {id: 18, title: "Mercor company profile (take rate, payout)", url: "https://sacra.com/c/mercor/", source: Sacra, date: "2026"}
- {id: 19, title: "Invisible Technologies company profile (revenue, EBITDA)", url: "https://sacra.com/c/invisible/", source: Sacra, date: "2025"}
- {id: 20, title: "OpenAI used Kenyan workers on less than $2 per hour", url: "https://time.com/6247678/openai-chatgpt-kenya-workers/", source: TIME, date: "2023-01-18"}
- {id: 21, title: "Scale AI's Remotasks bans workers in Kenya, Nigeria, Pakistan", url: "https://restofworld.org/2024/scale-ai-remotasks-banned-workers/", source: Rest of World, date: "2024-03-28"}
- {id: 22, title: "AI's professional-task data annotation pay", url: "https://time.com/7322386/ai-mercor-professional-tasks-data-annotation/", source: TIME, date: "2025"}
- {id: 23, title: "Scale AI / Outlier pay (worker review aggregator)", url: "https://www.aigigjobs.com/platforms/scale-ai", source: AI Gig Jobs, date: "2026"}
- {id: 24, title: "Scale AI hit by second employee wage lawsuit; DOL probe", url: "https://techcrunch.com/2025/01/09/scale-ai-hit-by-its-second-employee-wage-lawsuit-in-less-than-a-month/", source: TechCrunch, date: "2025-01-09"}
- {id: 25, title: "Facebook content moderators, Kenya: Meta appeal rejected", url: "https://www.foxglove.org.uk/2024/09/23/facebook-content-moderators-kenya-meta-appeal/", source: Foxglove, date: "2024-09-20"}
- {id: 26, title: "Turing raises $111M at a $2.2B valuation", url: "https://techcrunch.com/2025/03/06/turing-a-key-coding-provider-for-openai-and-other-llm-producers-raises-111m-at-a-2-2b-valuation/", source: TechCrunch, date: "2025-03-06"}
- {id: 27, title: "Cracks are forming in Meta's partnership with Scale AI", url: "https://techcrunch.com/2025/08/29/cracks-are-forming-in-metas-partnership-with-scale-ai/", source: TechCrunch, date: "2025-08-29"}
- {id: 28, title: "Google–Reddit $60 million AI training deal", url: "https://www.cbsnews.com/news/google-reddit-60-million-deal-ai-training/", source: CBS News, date: "2024-02-22"}
- {id: 29, title: "Reddit Inc. FY2024 Form 10-K (Other revenue, RPO)", url: "https://www.sec.gov/Archives/edgar/data/0001713445/000171344525000018/rddt-20241231.htm", source: SEC EDGAR, date: "2025-02"}
- {id: 30, title: "Shutterstock full-year 2025 financial results", url: "https://investor.shutterstock.com/news-releases/news-release-details/shutterstock-reports-full-year-2025-and-fourth-quarter-financial", source: Shutterstock IR, date: "2026-02-18"}
- {id: 31, title: "Getty Images statement on UK ruling in Stability AI litigation", url: "https://newsroom.gettyimages.com/en/getty-images/getty-images-issues-statement-on-ruling-in-stability-ai-uk-litigation", source: Getty Images, date: "2025-11-04"}
- {id: 32, title: "Alphabet ends contract with Appen, which trained Bard, Google Search", url: "https://www.cnbc.com/2024/01/23/alphabet-ends-contract-with-appen-which-trained-bard-google-search.html", source: CNBC, date: "2024-01-23"}
- {id: 33, title: "Appen FY2024 results (ASX announcement)", url: "https://announcements.asx.com.au/asxpdf/20250226/pdf/06fyjdglv66466.pdf", source: ASX / Appen, date: "2025-02-26"}
- {id: 34, title: "TELUS to acquire TELUS Digital at US$4.50/share (definitive)", url: "https://www.sec.gov/Archives/edgar/data/1825155/000110465925086091/tm2524985d1_ex99-1.htm", source: SEC EDGAR (6-K), date: "2025-09-02"}
- {id: 35, title: "Innodata Inc. Q3 2025 Form 10-Q (customer concentration)", url: "https://www.sec.gov/Archives/edgar/data/0000903651/000110465925107873/inod-20250930x10q.htm", source: SEC EDGAR, date: "2025-09-30"}
- {id: 36, title: "AI benchmarking org criticized for waiting to disclose OpenAI funding", url: "https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai/", source: TechCrunch, date: "2025-01-19"}
- {id: 37, title: "The Leaderboard Illusion", url: "https://arxiv.org/abs/2504.20879", source: arXiv, date: "2025-04-29"}
- {id: 38, title: "Silicon Valley bets big on environments to train AI agents", url: "https://techcrunch.com/2025/09/21/silicon-valley-bets-big-on-environments-to-train-ai-agents/", source: TechCrunch, date: "2025-09-21"}
- {id: 39, title: "NVIDIA reportedly acquires synthetic data startup Gretel", url: "https://techcrunch.com/2025/03/19/nvidia-reportedly-acquires-synthetic-data-startup-gretel/", source: TechCrunch, date: "2025-03-19"}
- {id: 40, title: "Nemotron-4 340B Technical Report", url: "https://arxiv.org/abs/2406.11704", source: "arXiv (NVIDIA)", date: "2024-06-14"}
- {id: 41, title: "AI models collapse when trained on recursively generated data", url: "https://www.nature.com/articles/s41586-024-07566-y", source: Nature, date: "2024-07"}
- {id: 42, title: "Is model collapse inevitable? Accumulating data avoids it", url: "https://arxiv.org/abs/2404.01413", source: arXiv, date: "2024-04"}
- {id: 43, title: "DeepSeek-R1: incentivizing reasoning via reinforcement learning", url: "https://www.nature.com/articles/s41586-025-09422-z", source: Nature, date: "2025-09-17"}
- {id: 44, title: "s1: Simple test-time scaling", url: "https://arxiv.org/abs/2501.19393", source: arXiv, date: "2025-01-31"}
- {id: 45, title: "Elon Musk agrees that we've exhausted AI training data", url: "https://techcrunch.com/2025/01/08/elon-musk-agrees-that-weve-exhausted-ai-training-data/", source: TechCrunch, date: "2025-01-08"}
- {id: 46, title: "xAI reportedly lays off 500 workers from data annotation team", url: "https://techcrunch.com/2025/09/13/xai-reportedly-lays-off-500-workers-from-data-annotation-team/", source: TechCrunch, date: "2025-09-13"}
- {id: 47, title: "Will we run out of data? Limits of LLM scaling", url: "https://epoch.ai/publications/will-we-run-out-of-data-limits-of-llm-scaling-based-on-human-generated-data", source: Epoch AI, date: "2024-06"}
- {id: 48, title: "Inside Meta's months-old AI unit and its internal data work", url: "https://techcrunch.com/2026/06/12/metas-months-old-ai-unit-is-a-soul-crushing-gulag-say-the-engineers-stuck-inside-it/", source: TechCrunch, date: "2026-06-12"}
:::
