---
eyebrow: ANALYSIS · AI INFRASTRUCTURE · MARKET STRUCTURE
title: "Is there a liquid market for compute? Not yet, and the answer depends on which of three markets you mean"
deck: A Pantera research director polled 200 people on whether the compute market is "real", got 61.5% yes, and scheduled a debate on "there won't ever be a liquid market for compute". The evidence says the question bundles three different markets that are at three very different stages.
lede: |
  On 27 October 2026 @sui414 asked whether compute can be standardized, whether any market exists beyond "a handful of monopoly OTC deals", and whether any venue has enough liquidity for price discovery. Two days later the author narrowed the motion for a 2-vs-2 Oxford-style debate. This article tests that motion against filings, exchange notices, index-vendor data and a live Vast.ai price snapshot, and separates what is established from what is merely announced.
stats:
  - {label: "CoreWeave revenue under commitment", value: "98%", note: "Q2 2026, 10-Q"}
  - {label: "CoreWeave backlog (RPO)", value: "$103.7B", note: "30 Jun 2026"}
  - {label: "H100 on Vast.ai, max / min ask", value: "2.9x", note: "29 Oct 2026, 13 offers, outlier-sensitive"}
  - {label: "CME / ICE compute futures trading", value: "0", note: "none confirmed as of 30 Oct 2026"}
---

## 01. The direct answer

:::kv
- {term: "Physical capacity (large clusters)", def: "Not a liquid market. Bilateral, multi-year, take-or-pay; CoreWeave books 98% of revenue under commitments.[^23]"}
- {term: "Posted spot / on-demand rental", def: "A real but fragmented price layer. Same-day asks for one GPU differ by about 3x on one venue.[^34]"}
- {term: "Listed derivatives", def: "Announced, not yet liquid. CME's 5 Oct start slipped, and the only live product I found, Kalshi's, has reported notional volume of about $4.4M through 27 July.[^2,3,36]"}
- {term: "'Won't ever' (the debate motion)", def: "Too strong. The freight and power precedents show that an index plus clearing can work without a fungible deliverable, but compute has a shorter hardware cycle and concentrated buyers."}
:::

The question in the poll bundles three separate things. A *physical spot market* is where capacity changes hands for hours or days. A *term-contract market* is where almost all capacity is actually sold. A *derivatives market* is where price risk could be transferred without moving a single GPU. Each has different liquidity physics, so a yes or no on "the compute market" is under-specified.

The tweet itself frames the poll as 123 "Yes it's real" votes against 77 "No it doesn't exist", out of 200.[^1] That is a small, self-selected sample from one analyst's audience, so it measures sentiment among that audience, not the state of the market.

A first-principles definition helps. A market is liquid when you can transact a meaningful size quickly, near the last price, repeatedly, with many independent counterparties on both sides. Every claim below is judged against that, not against whether a price chart exists.

:::callout(kind=info, label="Scope and method")
Where a figure comes from a vendor with a commercial interest (index providers, GPU clouds), the text says so. Where a source was only partly retrievable, the claim is hedged. The Twitter/X thread was read through a public mirror; the poll counts are the author's own, unaudited.
:::

## 02. Layer one: the physical contract book is bilateral, long and concentrated

*Thesis: the bulk of compute value changes hands in contracts that are the opposite of a spot market.*

CoreWeave's June 2026 quarterly filing is the cleanest primary evidence. One unnamed customer was 36% of Q2 revenue, down from 71% a year earlier; two more were 26% and 10%.[^23] The filing does not name them, so identifying Microsoft or OpenAI is inference.

:::donut(center-label="Q2 2026")
- {label: "Customer A", value: 36}
- {label: "Customer B", value: 26}
- {label: "Customer C", value: 10}
- {label: "All other (residual)", value: 28}
:::

:::note
Residual is 100% minus the three disclosed customer shares; it is a computed remainder, not a filed figure.[^23]
:::

Revenue under commitment was 98% for the three months to 30 June 2026. The filing's definition includes capacity delivered before commitment start dates, so the remaining roughly 2% is non-committed revenue, a ceiling on true on-demand, not a measurement of it.[^23] Remaining performance obligations were $103.7B, with 41% converting inside 24 months and 39% in months 25 to 48.[^23] The company's own release says more than $25B of net new commitments were added in early Q3.[^24]

This is financed with debt secured on the contracts. CoreWeave reports recourse debt of $31.4B and non-recourse debt of $3.7B, and Q2 net interest expense of $640M against $2,575M of revenue.[^23] A $3.1B facility closed in May 2026 priced at SOFR plus 4.50%, secured on contracts with two customers the company describes as non-investment-grade.[^25]

The pattern repeats elsewhere, with weaker sourcing. One trade-press account puts Oracle's backlog at $664B, with roughly half tied to OpenAI.[^27] One third-party analysis estimates that about 70% of Lambda's reported $50B backlog is a single Anthropic arrangement, though that is the analyst's inference.[^28] Both figures are secondary and should be treated as indicative.

:::timeline
- {date: "2025-12-09", headline: "Neocloud H100 index low", body: "Silicon Data series at about $2.00 per GPU-hour.[^12]"}
- {date: "2026-05-19", headline: "ICE and Ornn announce futures", body: "Cash-settled contracts on the Ornn index, subject to regulatory approval.[^4]"}
- {date: "2026-08-11", headline: "CME and Silicon Data set 5 Oct start", body: "H100 and B200 rental-index futures on NYMEX.[^2]"}
- {date: "2026-10-21", headline: "Not yet cleared", body: "A secondary report says regulators had not cleared the market; 9 Nov is the reported target or review-window end.[^3]"}
:::

*Counterpoint.* Concentrated demand is not the same as a monopoly market. The buyers are a few very strong credits, and prepayments and guarantees carry the risk.[^25] That structure makes a bilateral contract cheap to finance. It also removes the incentive to route capacity through an exchange, which is Enron's problem again (section 06).

*Why it matters:* if 98% of a leading supplier's revenue never touches a spot venue, a spot price can only describe the residual 2%, however well it is measured.

## 03. Layer two: posted spot prices exist, but they price different goods

*Thesis: there is a real price layer, but its dispersion is mostly product difference, not noise, so a single "the" price is a modelling choice.*

The repo's own hourly-refreshed Vast.ai snapshot makes the point directly. On 29 October 2026, 13 rentable H100 SXM offers were asked at $1.93 to $5.56 per GPU-hour, with a median of $2.40 and a mean of $2.82.[^34] The ratio of the highest to lowest ask is about 2.9, computed from those two numbers. The sample basis is on-demand asks only, with interruptible bids excluded.[^34] This is a small snapshot and the top ask may be an outlier host: another tracker lists Vast.ai verified hosts at roughly $1.49 to $2.27 in August 2026, a much narrower band.[^37] Both can be true, because dispersion depends on which hosts and configurations are sampled, which is itself the point.

:::bars
- {label: "Min ask", value: "$1.93", pct: 35}
- {label: "25th percentile", value: "$2.14", pct: 38}
- {label: "Median", value: "$2.40", pct: 43}
- {label: "Mean", value: "$2.82", pct: 51}
- {label: "Max ask", value: "$5.56", pct: 100}
:::

:::source
Vast.ai public offers API, H100 SXM, 29 Oct 2026, USD per GPU-hour; bars scaled to the maximum.[^34]
:::

Vast.ai's own documentation explains why. On-demand prices are set by hosts; only the interruptible tier uses bids.[^21] That is a posted-ask board, not a two-sided order book.

Hyperscalers also cut list prices administratively: AWS lowered P5 (H100) On-Demand prices by 44% from 1 June 2025.[^10] Across venues the gap widens. In March 2026 Silicon Data measured hyperscaler H100 at about $7.43 to $7.52 per hour against $2.43 to $2.63 on neoclouds, roughly 3x.[^11] A June 2026 aggregator reported published H100 on-demand rates spread about 8.2x between venues, though that figure mixes venues, SKUs and regions and is weakly sourced.[^14] In mid-May 2026, one report quoted on-demand H100 prices between $1.38 and $11.01 per hour.[^15]

Direction also differs by tenor. SemiAnalysis's survey-based one-year H100 contract rate rose from $1.70 in October 2025 to $2.35 in March 2026, and the newsletter treats posted on-demand prices as only a directional signal.[^13] Nebius raised H100 on-demand from $3.85 to $4.50 per GPU-hour in October 2026 and made its preemptible tier a floating price capped one cent below on-demand.[^26]

:::slope(left-label=Start, right-label=End, unit="$/GPU-hr")
| Series | Start | End |
|---|---|---|
| SemiAnalysis 1-yr H100 contract (Oct 2025 to Mar 2026) | 1.70 | 2.35 |
| Silicon Data neocloud H100 (9 Dec 2025 to 29 Oct 2026) | 2.00 | 2.90 |
| Silicon Data B200 (1 Jan to 25 Mar 2026) | 4.40 | 6.11 |
| Nebius H100 on-demand (pre- to post-1 Oct 2026) | 3.85 | 4.50 |
:::

:::source
SemiAnalysis,[^13] Silicon Data,[^6,12,11] Nebius price notice.[^26] Different series, definitions and dates; compare slopes, not levels.
:::

The B200 shows how fast a thin price can gap. Silicon Data's B200 index rose about 24% in March 2026, including a one-day move of 0.96 index points on 23 March, as introductory and spot offers were withdrawn; the same note reports some providers cutting 34% while others raised 16%.[^11] That is a vendor's own index over a short window, so read it as an illustration of fragility, not a settled statistic.

*Counterpoint.* Dispersion alone is not disqualifying; physical commodities show regional and grade differentials all the time. The real test is whether the differentials are stable and explainable enough to be hedged by a basis. Section 05 covers why that is harder for GPUs.

*Why it matters:* any benchmark must choose a cell (SKU, tenor, venue type), and the choice moves the headline number by multiples.

## 04. Layer three: derivatives are announced, indices disagree, volume is undisclosed

*Thesis: the financial wrapper is arriving faster than the liquidity it needs.*

CME Group and Silicon Data announced on 11 August 2026 that H100 and B200 rental-index futures would start on 5 October on NYMEX.[^2] The release was conditional on regulatory review, and the date was a reaffirmation of a launch first announced in May. A trade-association explainer describes the contract as 730 GPU-hours, cash-settled.[^8] By 21 October a report citing the Wall Street Journal said regulators had not cleared the market, with a 9 November target in its headline; that page was only partly retrievable.[^3] Secondary aggregators attribute 9 November to the end of a CFTC review extension, not to a confirmed first trade date, and I found no CME or CFTC primary page confirming either reading.

ICE announced on 19 May that it would list GPU compute futures on the Ornn Compute Price Index for H100, H200, B200 and RTX 5090, cash-settled and subject to regulatory approval.[^4] Ornn says its index is built only from printed transactions.[^4] A later account says no listing date has been published; I could not read the underlying notice.

The one product reported as live is Kalshi's compute forward curves, covering B200, H200 and A100, launched in July 2026. The launch coverage said volume and open interest were not disclosed and warned that thin liquidity could let small trades move a reference price.[^5] A later report, citing Allium data relayed through Bloomberg Opinion, put Kalshi's GPU rental markets at $4.4 million of notional volume through 27 July, with the most popular August market at just over $100,000.[^36] Kalshi is a regulated prediction-market exchange rather than a CME-style futures venue, and these are third-party figures, but they are the only volume numbers I found, and they are small.

:::stats
- {label: "CME / ICE compute futures trading", value: "0", note: "none confirmed as of 30 Oct 2026"}
- {label: "Competing index families", value: "4+", note: "Silicon Data, Ornn, Compute Desk, SemiAnalysis"}
- {label: "Contract size (CME, per FIA)", value: "730", unit: "GPU-hr"}
:::

The indices do not agree. A commentary piece by the founder of a competing index (a conflicted source) reported that March 2026 H100 readings were about $3.50 on Compute Desk against about $2.64 on Silicon Data, and B200 ranged from $5.70 to above $8.00 against $4.40 to $6.11.[^7] The two may measure different tenors, so the gap is not a pure error, but it is exactly the basis risk a hedger inherits.

Silicon Data's own H100 page claims coverage of more than 80% of the GPU rental market, standardizes for machine spec, rental terms, performance and geolocation, and showed $2.90 per GPU-hour on 29 October.[^6] Those are vendor claims and the page's FAQ carried an inconsistent $2.53.[^6]

Pantera's September 2026 report describes cash-settled exchanges as early stage, "without large amounts of trading volumes", and says participants are probably OTC desks and brokers hedging inventory, not end users.[^22] It also relays an "extremely large spread" between compute indices and individual GPU marketplaces, without quantifying it.[^22]

:::compare
- {role: LOWEST, name: "Silicon Data H100, Mar 2026", value: "$2.64"}
- {role: HIGHEST, name: "Compute Desk H100, Mar 2026", value: "$3.50"}
- {role: SUBJECT, name: "Spread between two 'H100 indices'", value: "$0.86 (about 33%)"}
:::

:::source
Compute Desk and Silicon Data March 2026 readings as reported in a competitor-authored commentary;[^7] spread computed from the two figures.
:::

*Counterpoint.* Launches are the normal order of operations: an index must exist before it can be settled against. A bad first year of volume would not by itself prove the thesis. Most new futures contracts fail, which is the survey consensus, but the literature also says success depends on spot-market size, homogeneity and hedging effectiveness, not on the listing itself.[^35]

*Why it matters:* the most informative number for this debate does not exist yet. Open interest and daily volume in the first quarter after CME's start are the first honest measurement of whether anyone wants to hedge compute.

## 05. The standardization problem is physical, not legal

*Thesis: unlike barrels or kilowatt-hours, a GPU-hour is not one good, and the differences are performance differences.*

Variant Fund puts the critique bluntly: "There is no standardized, tradeable unit for compute."[^33] The FIA explainer lists basis risk, fungibility, a chicken-and-egg liquidity problem and generation obsolescence among the risks, and notes that "A Nvidia H100 is not a Nvidia B200".[^8]

A vendor-authored (so interested) engineering post gives the mechanics. It describes 72 GPUs in a single NVLink domain versus eight-GPU islands, an H800 whose NVLink bandwidth is cut from 900 to 400 GB/s, and one operating point at which an NVL72 system delivers about 4.4x the per-GPU throughput of a B200.[^32] That 4.4x is for one workload and one operating point, so it shows the direction of the effect, not a general constant.

Hardware turns over fast. Dave Friedman, in a pre-launch critique, notes chips turn over in 18 to 24 months and warns that "Hedgers discover they've hedged a benchmark, not their P&L."[^9] Accounting lives tell the same story from the other side: Amazon shortened a subset of servers from six to five years, Meta lengthened most to 5.5, and CoreWeave uses six, according to a secondary summary of the filings.[^16] If the people who own the assets disagree by years on how long they last, a forward curve has no consensus anchor.

:::quote(attr="Dave Friedman, 'Will GPU futures ever work?' (Sept 2025)")
Hedgers discover they've hedged a benchmark, not their P&L.
:::

*Counterpoint.* Cash settlement does not require a perfectly fungible deliverable. Freight is the standing proof: Baltic-index swaps settle on a published index even though ships differ. A hedger accepts basis risk and uses a close proxy. The relevant question becomes whether the proxy tracks a buyer's actual cost closely enough, which is empirical and currently untested at scale.

*Why it matters:* standardization determines which cell of the market can be liquid first. The narrow, mature SKU (H100 on neoclouds) is the plausible candidate; frontier systems in rack-scale configurations are not.

## 06. Precedents: what worked, what failed, and why

*Thesis: the closest historical analogue that failed is bandwidth; the closest that worked is freight; power worked only after a regulator built the market.*

**Enron Broadband (failure).** In Q2 2001 Enron Broadband Services recorded 759 bandwidth transactions, up from 580 in Q1, yet lost $102M on $16M of revenue, and Jeff Skilling said there were no creditworthy counterparties in the business.[^29] The lesson is that deal counts overstated depth, and credit risk blocked a market that had a product. Clearing, which was absent then, is what the 2026 exchange proposals add. The sources disagree on earlier transaction counts, so I use only the figures in the cited piece.

**Freight (partial success, with caveats).** Exchange-listed freight futures did not survive on their own, and even the electronic venue Baltex was closed after the clearing house ended freight clearing amid slower volumes.[^30] The widely repeated account that over-the-counter agreements settled on independent Baltic indices then carried the market is consistent with that, but I did not verify the dates from primary Baltic Exchange pages. The takeaway is that an independent, transaction-based index mattered more than the exchange wrapper.

**Power (success through regulation).** Pantera argues that the benchmarks that won in power were the ones with the most liquid physical delivery infrastructure, and that compute has no equivalent of a FERC transparency mandate.[^22] The implication is that compute may need a physical-settlement venue before an index is trusted.

**AWS Spot (supplier-set).** In late 2017 AWS dropped bidding; Spot prices now adjust slowly over days and weeks, with typical savings of 70 to 90% against On-Demand.[^31] The largest supplier sets the "spot" price, so it is an administered discount, not competitive price discovery.

*Counterpoint.* None of these is an exact analogue. Bandwidth deflated continuously and was route-specific; compute hardware also deflates per generation yet 2026 renewals suggest the opposite, with H100s reportedly being renewed at original contract rates.[^13] If scarcity persists, hedging demand rises; if it ends, the hedging need shifts from buyers to asset owners (section 08).

*Why it matters:* the failure modes (credit, standardization, route-specific products) are the same ones the new proposals must beat, and clearing plus a shared index addresses two of the three.

## 07. Decentralized and marketplace venues: real, small, and subsidized

*Thesis: the venues that look most like open markets show the least liquidity.*

Akash's Q1 2026 utilization was reported at about 33.7%, with 84 GPUs used of 334 available and lease revenue of $253,250, down 45% quarter on quarter; the article's own percentage does not match 84 over 334 (about 25%), so the figure is shaky.[^17] A different blog claims utilization above 80% and sector on-chain revenue of $72M for FY2025 against roughly $10B in token market value, with no primary source for those numbers.[^18] The sources conflict, which is itself a data-quality finding.

io.net's daily earnings averaged about $35 to $36 thousand, about $13M annualized, alongside roughly $4.5M of block rewards, according to a CoinDesk Research piece that reads as aligned with the project.[^19] Earnings are network-reported and unaudited.

SF Compute is the closest to a true order book. Its founder says about 5% of total capacity sits on the book, that cumulative volume is "several hundred million" dollars, and that thin indices can be manipulated and diverge from true cost.[^20] These are self-reported.

:::rank-list
- {label: "CoreWeave: committed revenue share", value: "98%", pct: 98, highlight: true}
- {label: "Akash: reported GPU utilization (Q1 2026, disputed)", value: "33.7%", pct: 34}
- {label: "SF Compute: capacity on order book (founder estimate)", value: "~5%", pct: 5}
:::

:::note
Three different metrics (revenue share, utilization, order-book share) placed on one scale for orientation only; they are not like-for-like.[^23,17,20]
:::

*Counterpoint.* Small does not mean wrong. Every exchange starts thin, and SF Compute's design (time-windowed, physically settled capacity) targets the settlement problem Pantera says matters most.[^22] But "5% of capacity" is a long way from a benchmark that a lender would write into a covenant.

*Why it matters:* a physical-delivery venue is the missing piece in the power analogy, and nobody has yet shown one at scale.

## 08. Who actually needs to hedge? Lenders, not users

*Thesis (analysis, not sourced fact): the natural hedger for compute price risk is whoever holds residual value, not whoever rents.*

Buyers with long-dated needs already hedge by signing multi-year take-or-pay deals, which is the 98% above.[^23] The remaining unhedged exposure is on the supply side: GPU owners carry about $35B of debt at CoreWeave alone, serviced by contracts that expire before the assets are worthless.[^23] The price of a renewal in 2029 and the resale value of a 2026 chip are risks no bilateral contract covers.

That risk is already priced informally. The 2026 move of H100 renewals back to original rates is what lets a lender underwrite six-year lives,[^13,16] and the Pantera report mentions that Nvidia reportedly offers up to 25% residual value support.[^22] A compute forward curve could, in principle, let lenders and neoclouds hedge exactly that. If so, the early volume would come from neoclouds, brokers and lenders, which matches Pantera's expectation that OTC desks and brokers dominate first.[^22]

*Counterpoint.* A sell-side hedger needs a benchmark that tracks the asset they own, and a buy-side hedger needs one that tracks what they rent. Section 05 argues one index may not serve both.

*Why it matters:* it changes what "liquidity" has to mean. Depth may be built by financiers managing collateral, not by AI labs managing budgets.

## 09. What could break the thesis

*Thesis: the base case is "not yet, and narrow if it comes", but three things would change it.*

:::callout(kind=warn, label="Falsifiers")
1. Disclosed CME open interest that grows through the first quarter after launch, from non-bank end users, would contradict "no one wants to hedge".
2. Convergence of the competing indices (H100 spread inside a few percent) would weaken the basis-risk argument.
3. A physical-delivery venue exceeding low-single-digit percent of capacity would address the settlement gap Pantera identifies.[^22]
:::

Arguments against the "won't ever" motion. First, clearing solves counterparty credit, which sank bandwidth.[^29] Second, a narrow SKU such as the H100 is old enough to behave like a mature product, and an index exists for it.[^6] Third, Pantera's report says compute may become a commodity asset over a multi-year horizon.[^22] An investor's view is not independent evidence, but it states the bull case the debate will hear.

Arguments for the motion. First, 98% of a leading supplier's revenue is committed, so spot prices describe a thin residual.[^23] Second, there is no shared unit or index, and the available indices differ materially.[^7,33] Third, hardware turns over in 18 to 24 months, so any benchmark must be rebuilt continuously.[^9]

The honest probability judgement is that "ever" is a long time and a motion of "won't ever" is the harder side to defend. A better-posed question is "which cell will be liquid first and who will be its hedgers", with the answer, on current evidence, being older GPU generations on neoclouds, hedged by brokers and lenders.

:::source
Red-team pass: the 98% committed-revenue claim survived (with the caveat added above). The "no listed futures trading" claim survived for CME and ICE, but the red-team found third-party Kalshi volume figures, now included. The Vast.ai dispersion claim was weakened by a narrower competing tracker, now disclosed.
:::

## 10. Watch list

:::kv
- {term: "CME GPU1 / GPU2", def: "First trading date (9 Nov is reported but unconfirmed), then daily volume and open interest.[^3]"}
- {term: "ICE / Ornn", def: "Whether a listing date is published and which contracts launch first.[^4]"}
- {term: "Index spread", def: "Whether Silicon Data, Ornn and Compute Desk H100 readings converge.[^7]"}
- {term: "Neocloud on-demand share", def: "CoreWeave's non-commitment revenue share, now about 2%.[^23]"}
- {term: "Physical venues", def: "SF Compute's share of capacity and whether lenders reference any index in covenants.[^20]"}
:::

:::references
- {id: 1, title: "@sui414 poll and debate announcement (Oct 27-29, 2026), read via public fxtwitter mirror", url: "https://x.com/sui414/status/2115856908900798954", source: "X / Twitter", date: "2026-10-29"}
- {id: 2, title: "CME Group and Silicon Data to launch compute futures on October 5", url: "https://www.prnewswire.com/news-releases/cme-group-and-silicon-data-to-launch-compute-futures-on-october-5-to-unlock-new-way-to-hedge-ai-risks-302848593.html", source: "PR Newswire", date: "2026-08-11"}
- {id: 3, title: "Silicon Data / CME compute futures November 2026", url: "https://runtimewire.com/article/silicon-data-cme-compute-futures-november-2026", source: "RuntimeWire", date: "2026-10-21"}
- {id: 4, title: "ICE and Ornn to launch GPU compute futures contracts", url: "https://ir.theice.com/press/news-details/2026/ICE-and-Ornn-to-Launch-GPU-Compute-Futures-Contracts/default.aspx", source: "ICE investor relations", date: "2026-05-19"}
- {id: 5, title: "Kalshi launches GPU compute forward curves for AI hedging", url: "https://aiweekly.co/alerts/kalshi-launches-gpu-compute-forward-curves-for-ai-hedging", source: "AI Weekly", date: "2026-07-14"}
- {id: 6, title: "Silicon Data H100 rental index page", url: "https://www.silicondata.com/products/silicon-index/h100", source: "Silicon Data", date: "2026-10-29"}
- {id: 7, title: "GPU pricing disarray: four indices diverge", url: "https://www.kucoin.com/news/flash/gpu-pricing-disarray-four-indices-diverge-market-lacks-consensus", source: "KuCoin News (commentary)", date: "2026-04-08"}
- {id: 8, title: "Explainer: what are compute futures and how do they work", url: "https://www.fia.org/marketvoice/articles/explainer-what-are-compute-futures-and-how-do-they-work", source: "FIA", date: "2026-09-23"}
- {id: 9, title: "Will GPU futures ever work?", url: "https://davefriedman.substack.com/p/will-gpu-futures-ever-work", source: "Dave Friedman, Substack", date: "2025-09-06"}
- {id: 10, title: "Announcing up to 45% price reduction for EC2 NVIDIA GPU-accelerated instances", url: "https://aws.amazon.com/blogs/aws/announcing-up-to-45-price-reduction-for-amazon-ec2-nvidia-gpu-accelerated-instances/", source: "AWS", date: "2025-06-05"}
- {id: 11, title: "B200 rental price, March 2026 update", url: "https://www.silicondata.com/blog/b200-rental-price-march-2026-update", source: "Silicon Data", date: "2026-03-31"}
- {id: 12, title: "NVIDIA H100 GPU rental price up 45% since December: claimed vs verified", url: "https://explainx.ai/blog/nvidia-h100-gpu-rental-price-45-percent-since-december-silicon-data-chamath-claimed-vs-verified-2026", source: "ExplainX", date: "2026-10-24"}
- {id: 13, title: "The Great GPU Shortage: Rental Capacity", url: "https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity", source: "SemiAnalysis", date: "2026-03-31"}
- {id: 14, title: "H100 rental price history and trends", url: "https://gpusmith.com/articles/en/h100-rental-price-history-trends", source: "GPUSmith", date: "2026-06-30"}
- {id: 15, title: "H100 rental prices slide as Ornn index normalizes", url: "https://cryptobriefing.com/h100-rental-prices-slide-ornn-ai/", source: "Crypto Briefing", date: "2026-05-27"}
- {id: 16, title: "Amazon and Meta server depreciation useful lives", url: "https://altss.com/blog/amazon-meta-server-depreciation-useful-lives-earnings", source: "Altss", date: "2026-07-07"}
- {id: 17, title: "AKT after AI rally: decentralized compute utilization", url: "https://cryptodaily.co.uk/2026/06/akt-after-ai-rally-decentralized-compute-utilization", source: "Crypto Daily", date: "2026-06-03"}
- {id: 18, title: "DePIN compute revenue pivot: Akash, io.net, Aethir", url: "https://blockeden.xyz/blog/2026/03/12/depin-compute-revenue-pivot-akash-ionet-aethir/", source: "BlockEden", date: "2026-03-12"}
- {id: 19, title: "The Incentive Dynamic Engine: a new era for io.net tokenomics", url: "https://coindesk.com/research/the-incentive-dynamic-engine-a-new-era-for-io-net-tokenomics", source: "CoinDesk Research", date: "2026-06-12"}
- {id: 20, title: "SF Compute interview", url: "https://www.latent.space/p/sfcompute2", source: "Latent Space", date: "2026-10-20"}
- {id: 21, title: "Vast.ai instance pricing documentation", url: "https://docs.vast.ai/documentation/instances/pricing", source: "Vast.ai docs", date: "2026-10-30"}
- {id: 22, title: "Compute capital markets", url: "https://panteracapital.com/compute-capital-markets/", source: "Pantera Capital", date: "2026-09-09"}
- {id: 23, title: "CoreWeave Form 10-Q, quarter ended June 30, 2026", url: "https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000366/crwv-20260630.htm", source: "SEC EDGAR", date: "2026-08-11"}
- {id: 24, title: "CoreWeave reports strong second quarter 2026 results", url: "https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/", source: "CoreWeave IR", date: "2026-08-11"}
- {id: 25, title: "CoreWeave closes $3.1 billion loan facility for GPU-backed financing", url: "https://investors.coreweave.com/news/news-details/2026/CoreWeave-Closes-3-1-Billion-Loan-Facility-Expanding-Access-to-Public-Markets-for-GPU-Backed-Financing/", source: "CoreWeave IR", date: "2026-05-18"}
- {id: 26, title: "Nebius AI GPU price increase", url: "https://usagepricing.com/blueprint/activity/nebius-ai-2026-09-24-gpu-price-increase", source: "UsagePricing", date: "2026-10-01"}
- {id: 27, title: "Oracle Q1 FY27 results: $664B backlog", url: "https://erp.today/oracle-q1-fy27-results-664b-backlog-ai-contracts/", source: "ERP Today", date: "2026-09"}
- {id: 28, title: "Lambda backlog and Anthropic concentration", url: "https://blog.pebblous.ai/blog/lambda-backlog-anthropic-concentration/en/", source: "Pebblous", date: "2026-10-06"}
- {id: 29, title: "Enron Broadband bandwidth trading volumes and counterparties", url: "https://www.energyintel.com/0000017b-a79a-de4c-a17b-e7dac4620000", source: "Energy Intelligence", date: "2001-09-09"}
- {id: 30, title: "London's Baltic Exchange to close ship futures platform Baltex", url: "https://gcaptain.com/londons-baltic-exchange-to-close-ship-futures-platform-baltex", source: "gCaptain"}
- {id: 31, title: "New Amazon EC2 Spot pricing", url: "https://aws.amazon.com/blogs/compute/new-amazon-ec2-spot-pricing/", source: "AWS Compute Blog", date: "2018-03-13"}
- {id: 32, title: "Why identical GPU clusters diverge in production", url: "https://cudocompute.com/blog/why-identical-gpu-clusters-diverge-in-production", source: "CUDO Compute"}
- {id: 33, title: "Variant Fund analysis of compute futures", url: "https://variant.fund/?p=3574", source: "Variant", date: "2026-05-14"}
- {id: 34, title: "Vast.ai public offers API (repo snapshot research/market/gpu-spot.json)", url: "https://console.vast.ai/api/v0/bundles/", source: "Vast.ai / ARA gpu-spot lane", date: "2026-10-29"}
- {id: 36, title: "Kalshi compute forward curve for GPU hedging", url: "https://thenextweb.com/news/kalshi-compute-forward-curve-gpu-ai", source: "The Next Web"}
- {id: 37, title: "H100 GPU cost guide", url: "https://www.cloudzero.com/blog/h100-gpu-cost/", source: "CloudZero"}
- {id: 35, title: "Why some futures contracts succeed and others fail: a survey of relevant research", url: "https://climateinstitute.edhec.edu/publications/why-some-futures-contracts-succeed-and-others-fail-survey-relevant-research", source: "EDHEC", date: "2014-06"}
:::
