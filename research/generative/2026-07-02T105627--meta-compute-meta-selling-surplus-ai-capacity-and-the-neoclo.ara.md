---
eyebrow: REPORT · AI INFRASTRUCTURE
title: "Meta Compute: the surplus that reprices the neocloud"
domain: finance
deck: When the largest AI buyer floats the idea of becoming a seller, the market reprices everyone it might undercut — even before a product exists.
lede: |
  On July 1, 2026, a single Bloomberg report that Meta was building a cloud
  business to sell excess AI compute wiped roughly $18 billion off two
  companies' market value in a session — CoreWeave and Nebius each fell about
  15% while Meta rose nearly 9%. Nothing had launched. No price sheet, no
  timeline, no confirmation. What moved was not the supply of GPUs but the
  *story* underwriting neocloud valuations: that AI compute is scarce, and that
  hyperscalers are buyers. This report asks what a Meta "surplus" actually is,
  whether it can exist in a power-constrained world, and how much of the
  neocloud repricing is mechanism versus reflex.
stats:
  - {label: Meta 2026 capex guide, value: $125–145B, note: from $115–135B}
  - {label: CoreWeave RPO, value: $60.7B, note: as of 2025-12-31}
  - {label: Nebius ARR, value: $1.92B, note: as of 2026-03-31}
  - {label: NBIS on July 1, value: "−17%", note: one session}
---

## 01. The event: what "Meta Compute" is — and is not

The falsifiable core of this story is narrow. On July 1, 2026, Bloomberg reported that Meta is developing a cloud unit internally called "Meta Compute" to sell access to both AI compute capacity and models — with the plans explicitly "still in development."[^1] The market treated it as material: Meta jumped nearly 9% while CoreWeave and Nebius each fell about 15% in morning trading, Nebius closing down 17%.[^2] Nebius alone shed roughly $11.9 billion of market value and CoreWeave about $5.7 billion — a combined loss near $18 billion.[^24,20] {accent}The repricing preceded the product by an unknown margin — there is no launch date, no pricing, and no Meta confirmation.[^1]{/}

:::callout(kind=info, label="Direct answer")
- **Is Meta actually selling surplus compute?** Not yet. It is a reported, in-development plan plus an on-record Zuckerberg remark that it is "definitely on the table" *if* Meta overbuilds.[^1,3]
- **Why did neoclouds crater anyway?** Their valuations price GPU *scarcity* and hyperscaler *demand*. A hyperscaler that could dump depreciated capacity attacks both at once — and Meta is a top counterparty for CoreWeave and Nebius.[^2,20]
- **Is the "surplus" real?** Only transitionally. Meta is compute-*constrained* and a large net buyer of external GPUs; any sellable slack is the gap between capacity landing on the depreciation clock and internal demand ramping.[^6,7]
- **Is the sell-off justified?** Partly reflex. Near-term neocloud revenue is contract-locked; the real exposure is 2028+ renewal pricing and terminal value, not this year's cash flows.[^8,17]
:::

The reported structure has two tracks: hosting Meta's own models — including the closed-weight "Muse Spark," AWS-Bedrock style — and renting raw GPU capacity like a neocloud.[^1] It is co-led by infrastructure head Santosh Janardhan alongside Superintelligence Labs' Daniel Gross and president Dina Powell McCormick.[^1] The seniority signals intent; it is not a launch. Muse Spark, unveiled in April 2026, had not been released to developers as of the report.[^1]

The primary evidence sits one level up from Bloomberg's anonymous sourcing. At Meta's May 27, 2026 shareholder meeting, Zuckerberg said a cloud business is "definitely on the table" — but conditioned it: "if we get to a point where we feel that we have overbuilt, then that is an option that we have."[^3] He added that "almost every week" companies ask to buy Meta's compute "at some premium."[^4] {accent}That is inbound demand and optionality — not a decision to sell.{/} The premise worth stress-testing is therefore not "will Meta rent GPUs" but "can Meta have a durable surplus to rent at all."

## 02. The overbuild that manufactures a surplus

A surplus needs a build big enough to outrun even Meta's appetite. Meta's capital expenditure, including finance-lease principal, went from $28.1 billion in FY2023 to $39.2 billion in FY2024 to $72.2 billion in FY2025 — and 2026 guidance was raised in April to $125–145 billion, up from $115–135 billion, citing higher GPU/component pricing.[^5,6] The FY2026 midpoint is roughly 1.9× FY2025 and larger than most national infrastructure budgets.

:::exhibit(num="Exhibit 1", title="Meta capital expenditures, incl. finance leases", subtitle="$ billion; FY2026 = guidance midpoint", source="Meta Q4-2025 and Q1-2026 earnings releases (SEC 8-K exhibits).", note="FY2026E shows the $135B midpoint of the $125–145B guide.")
:::bar-chart(title="Capex step-up", orientation=vertical, value-unit=$, value-suffix=B)
categories: FY2023, FY2024, FY2025, FY2026E
Capex: 28.1, 39.2, 72.2, 135
:::
:::
The money buys physical capacity gated by *power*, not silicon. Zuckerberg described "several multi-GW clusters": Prometheus (~1 GW, New Albany, Ohio, online 2026) and Hyperion (Richland Parish, Louisiana), which he said could "scale up to 5 GW over several years," each covering "a significant part of the footprint of Manhattan."[^7] Louisiana alone is a ~$10 billion, 4-million-square-foot build backed by new Entergy gas turbines, with the gas plan later expanded toward ~7.5 GW.[^8] Meta also signed a 20-year deal for the entire 1,121 MW output of Constellation's Clinton nuclear plant.[^9]

Here is the mechanism that turns a build into a sellable surplus. Effective January 1, 2025 Meta extended the useful life of most servers and network assets to 5.5 years; the change cut FY2025 depreciation by $2.92 billion and lifted net income $2.59 billion, or $1.00 per diluted share.[^10] {accent}A GPU depreciates whether or not it is running a job.{/} Once capacity lands, the power, cooling and depreciation clocks start regardless of utilization — so renting idle hours at marginal cost converts dead time into revenue exactly as the depreciation from this capex wave begins flowing through the income statement.[^11] The overbuild does not need to be a mistake to create rentable slack; it only needs to be *ahead of demand*.

The counterpoint is that Meta's own economics resist a standing surplus. On the Q3 2025 call, Zuckerberg said Meta will "aggressively front-load building capacity," and that if superintelligence takes longer, "we'll use the extra compute to accelerate our core business — which continues to be able to profitably use much more compute than we've been able to throw at it."[^12] In that framing, surplus is *absorbed internally or paused* — never sold. Why this matters: if the core ads-and-ranking business is an elastic sink for compute, a durable rentable surplus is hard to sustain, and Meta Compute becomes a monetization of the *transition window*, not a new structural business line.

## 03. The paradox: Meta is the neoclouds' biggest new buyer

The strongest evidence against a Meta "surplus" is Meta's own chequebook. In the ninety days before the surplus report, Meta was aggressively *buying* external capacity: it expanded its CoreWeave agreement by ~$21 billion (to roughly $35 billion total, through December 2032)[^13] and signed a Nebius deal worth up to ~$27 billion on NVIDIA's Vera Rubin platform, deploying from early 2027.[^14] Combined, Meta's commitments to just these two neoclouds reach up to ~$62 billion — about 46% of the midpoint of its own 2026 capex guide.[^20]

:::exhibit(num="Exhibit 2", title="A buyer, then a would-be seller", subtitle="Meta's 2026 compute moves", source="Company/SEC filings; CoreWeave and Nebius newsrooms; Bloomberg via CNBC.")
:::timeline
- {date: 2026-03, headline: "Nebius deal up to ~$27B", body: "Five-year Vera Rubin capacity, deploying early 2027 — Meta buying, not selling."}
- {date: 2026-03, headline: "Google caps Meta's Gemini", body: "Google could not meet the Gemini capacity Meta sought; some Meta AI projects slipped."}
- {date: 2026-04, headline: "CoreWeave expanded +$21B", body: "To ~$35B total through Dec 2032 — Meta locking in more third-party GPUs."}
- {date: 2026-05, headline: "Zuckerberg: 'on the table'", body: "Cloud business an option 'if we have overbuilt'; asked weekly to sell compute."}
- {date: 2026-07, headline: "'Meta Compute' reported", body: "Bloomberg: plan to sell excess capacity + Muse Spark. Neoclouds sell off."}
:::
:::
Two facts sharpen the paradox. First, on Meta's Q1 2026 call, CFO Susan Li said "I would be the first person to say we've underestimated our compute demand in the past... I'm not sure there's a team at the company that wouldn't like to get a little more compute right now."[^15] Second, around March 2026 Google *capped* Meta's paid access to its Gemini models because Meta wanted more capacity than Google could supply, reportedly delaying some internal Meta projects.[^16] A company that is rationed by a supplier and calls itself compute-constrained is not obviously sitting on a glut.

The reconciliation is timing and fungibility. A firm legally committed to take-or-pay capacity it cannot yet fully use during ramp can resell utilization slack without implying it over-built end demand — the same "front-load then backfill" logic Zuckerberg described. But note the fungibility limit: Meta's custom MTIA silicon is internal-only and not a merchant-GPU substitute, so any sellable surplus is the Nvidia/AMD fleet, not the custom stack.[^12] {accent}The honest read: the surplus is real but reversible and transitional — a byproduct of front-loading, not a structural excess.{/} What would falsify the benign reading is a Meta capex *cut* — which no analyst yet forecasts, and which Wells Fargo explicitly does not expect.[^17]

## 04. The neocloud machine: a levered spread on GPU depreciation

To see why the market flinched, price the thing being threatened. A "neocloud" rents GPU compute and the power/networking around it — CoreWeave, Nebius, Crusoe, Lambda, Nscale, Together — as opposed to a hyperscaler's broad services portfolio. The segment cleared more than $25 billion of revenue in 2025 and is forecast to approach $400 billion by 2031, a ~58% CAGR that is itself a bet on durable scarcity.[^18]

CoreWeave, the largest pure-play, is the archetype: revenue scaled ~22× in two years, from $229 million (2023) to $1.9 billion (2024) to $5.1 billion (2025), against a committed backlog of $66.8 billion — of which $60.7 billion is the stricter GAAP remaining-performance-obligation figure, up from $15.1 billion a year earlier.[^19]

:::exhibit(num="Exhibit 3", title="CoreWeave: scale without profit", subtitle="FY2025 unless noted", source="CoreWeave FY2025 10-K and Q4 earnings release (SEC).")
:::stats
- {label: Revenue (FY2025), value: $5.13B, note: +168% YoY}
- {label: Backlog / RPO, value: $60.7B, note: vs $15.1B prior year}
- {label: Net loss, value: "−$1.17B", note: after interest + D&A}
- {label: Total debt (net), value: $21.4B, note: GPU-collateralized}
- {label: Interest expense, value: $1.23B, note: rates ~10–15%}
- {label: GPU useful life, value: 6, unit: yrs}
:::
:::
The business is best understood as a levered spread trade on GPU depreciation: high-cost, GPU-collateralized debt (~$21.4 billion net at 10–15% effective rates) funds an Nvidia fleet depreciated over six years and rented on multi-year take-or-pay contracts.[^19] A 60%-plus adjusted-EBITDA margin looks like healthy infrastructure; the −1% operating margin and $1.17 billion net loss are what survive after $1.23 billion of interest and heavy depreciation.[^19] The whole edifice rests on three mutually-reinforcing numbers: the backlog being durable, the customer concentration diversifying, and the six-year GPU life holding economically.

That concentration is the soft spot. Microsoft alone was ~67% of CoreWeave's FY2025 revenue.[^19]

:::donut(center-label="67%")
- {label: Microsoft, value: 67}
- {label: All other customers, value: 33}
:::
The diversification story *is* the counterparty risk: OpenAI committed up to ~$11.9 billion plus a further ~$6.5 billion, and Meta ~$14.2 billion (later expanded), so the customers who de-risk Microsoft dependence are the same names — OpenAI, Meta — whose own compute strategies can whipsaw the stock.[^19] Nebius shows the mirror image: ARR compounding from ~$551 million (September 2025) to $1.92 billion (March 2026), guided to $7–9 billion by year-end 2026, on the back of a ~$17.4 billion Microsoft deal (up to $19.4 billion) and the Meta contract.[^21,22] The bull case is contracted, investment-grade-anchored ARR; the bear case is that the same anchors can turn suppliers.

## 05. The repricing mechanism: marginal-cost supply breaks scarcity pricing

Why does a mere *plan* reprice a sector? Because neocloud multiples are underwritten on GPU scarcity, and a hyperscaler dumping depreciated capacity at marginal cost attacks the scarcity premium on three axes at once — it adds supply, removes a major buyer, and competes for the same enterprise customers. D.A. Davidson's Gil Luria put the bear case bluntly: "Those companies like CoreWeave and Nebius rely on Meta for their growth and Meta may not need them anymore."[^23] Independent analysis framed the mechanism as Meta "compressing GPU rental pricing exactly when Nebius's new gigawatt sites come online."[^24]

The pricing history shows both the fragility and its limit. H100 rental collapsed from roughly $8/hour at 2023 launch toward a trough as new entrants and AWS's mid-2025 cut flooded supply.[^25] But by SemiAnalysis's index, one-year reserved H100 pricing then *rose* about 40%, from $1.70/hour in October 2025 to $2.35/hour by March 2026, with on-demand capacity "sold out across all GPU types."[^11] That reversal is the crux: rental rates sit right on top of owned break-even — on one vendor's cost model, roughly $2.55/hour at full utilization — so a marginal-cost seller can push prices back below the level at which debt-funded neoclouds service their depreciation.[^26]

:::exhibit(num="Exhibit 4", title="The repricing, priced daily", subtitle="Month-end close, $/share — Yahoo Finance, as of 2026-07-02", source="Yahoo Finance close prices; ARA analysis.", note="The final point captures the July 1 sell-off: NBIS −17%, CRWV ~−14% intraday.")
:::line-chart(title="CoreWeave and Nebius, trailing 12 months", y-unit=$)
x: 2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06,2026-07
CRWV: 114.13,103.04,136.85,133.71,73.12,71.61,93.19,79.56,77.47,111.6,109.53,99.54,85.68
NBIS: 54.43,68.32,112.27,130.82,94.87,83.71,85.19,91.19,103.76,138.23,231.09,276.17,229.18
:::
:::
The reaction was not unanimous, which is itself informative. Rosenblatt reiterated Buy with a $250 target, arguing the weakness was a buying opportunity, that channel checks showed "no change in hyperscale posture toward GPU compute procurement," and — critically — that Meta likely cannot even resell the CoreWeave capacity it leased through 2032.[^17] Roth called the neocloud reaction "an overreaction on a still-unconfirmed, capacity-gated plan."[^27] {accent}The tell: the desks that stayed constructive were pricing contracts and physics; the desks that turned bearish were pricing narrative and terminal value.{/} Both can be right on different horizons.

## 06. The depreciation fault line

Underneath both the surplus and the repricing sits one accounting choice: how long a GPU is assumed to last. Depreciation is asset cost divided by useful life; cost is fixed at purchase, but useful life is a management estimate, so lengthening it mechanically shrinks expense and lifts reported profit with no change in cash or physics. Into 2023–24, hyperscalers *extended* server lives even as Nvidia's product cadence *compressed* to a roughly annual beat — the two moving in opposite directions.

:::exhibit(num="Exhibit 5", title="Same chips, different clocks", subtitle="Stated server/GPU useful life (years)", source="Company 10-Ks (Meta, Amazon, Alphabet, Microsoft); CoreWeave 10-K; analyst compilations for Oracle/Nebius.", note="Amazon cut a subset from 6 to 5 years, citing AI pace; Nebius's ~4 years is an effective figure within a 3–10 year disclosed range.")
:::rank-list
- {label: "Alphabet / Google — servers", value: "6 yr", pct: 100}
- {label: "Microsoft — computer equip.", value: "6 yr", pct: 100}
- {label: "CoreWeave — GPUs", value: "6 yr", pct: 100}
- {label: "Meta — servers (from 2025)", value: "5.5 yr", pct: 92}
- {label: "Amazon — subset (cut 2025)", value: "5 yr", pct: 83, highlight: true}
- {label: "Nebius — DC equip. (effective)", value: "~4 yr", pct: 67}
:::
:::
The split in early 2025 is the tell. In the same window Meta *extended* to 5.5 years (a ~$2.9 billion boost to pre-tax income), Amazon — the operator with the most GPU-cloud experience — *cut* a subset of servers and networking from six to five years, explicitly citing "an increased pace of technology development, particularly in the area of artificial intelligence," and booked ~$920 million of accelerated depreciation on early retirements.[^10,28] {accent}When the most experienced operator shortens lives while peers lengthen them, "useful life" is revealed as a policy lever, not a physical measurement.{/}

Michael Burry made the aggressive version of the argument in late 2025: ramping capex on chips with a 2–3-year product cycle "should not result in the extension of useful lives," and he estimated ~$176 billion of understated depreciation and overstated profit across the industry in 2026–2028.[^29] Treat that as a short-seller's model, not a fact — the counter is that older GPUs cascade to cheaper inference tiers, keeping economic life closer to the accounting life. But the link to this report's thesis is direct: if real economic life is shorter than the six-year book, then idle GPUs erode both neocloud *margins* and the GPU *collateral value* pledged against neocloud debt at the same time — which is precisely the exposure a marginal-cost Meta surplus would expose. The CoreWeave-versus-Nebius contrast (identical H100/H200 fleets, six-year versus ~four-year books) is that risk in miniature.[^29]

## 07. Power, not silicon, is the binding constraint

The surplus thesis quietly assumes idle GPUs can be switched on and sold. In a power-constrained world, they cannot — and the evidence that power is now the binding constraint is convergent. GE Vernova's gas-turbine backlog and slot reservations together are set to exceed 110 GW and stretch into 2029, with roughly 10 GW of open slots left across 2029–2030 and ~3-year lead times on heavy-duty units; management expects reservations sold out through 2030 by the end of 2026.[^30] Grid interconnection is no faster: ERCOT's large-load queue nearly quadrupled in a single year to 226 GW, about 77% of it data centers targeting connection by 2030.[^31] US data-center electricity is projected to roughly double to 325–580 TWh by 2028 — 6.7% to 12% of all US power.[^32]

:::callout(kind=warn, label="First principles")
A GPU with no power is not compute — it is inventory. If the binding constraint is megawatts, then "idle" GPUs are *stranded* (unpowerable), not *surplus* (sellable). Genuine rentable surplus requires spare **powered** capacity — which only exists if an operator provisioned power *ahead* of chips. So the headline "GPU glut" and a power-bound world can only be reconciled as a localized power-ahead-of-silicon overbuild, the opposite imbalance to the one the word "surplus" implies.[^30,32]
:::

This reframes Meta Compute. Meta's Louisiana and Ohio campuses are power-first builds — self-procured gas, a nuclear PPA, behind-the-meter generation — precisely because power is the scarce input.[^8,9] If Meta secured multi-gigawatt power envelopes on long lead times and its chip deliveries or model-training demand arrive on a different schedule, it could hold *powered* capacity ahead of internal need. That is the one configuration in which a genuine, dispatchable surplus exists — and it is also the configuration most worth renting, because stranded power is pure cost. Why it matters: it means the credible version of Meta Compute is less "dumping obsolete GPUs" and more "monetizing a power lead," which is a scarcer and more durable asset than the bear case assumes — cutting against a simple margin-compression story even as it validates that Meta has something real to sell.

## 08. The bull rebuttal: why the sell-off may be overdone

The strongest case that July 1 was reflex rests on four load-bearing facts. First, near-term neocloud revenue is contract-locked: CoreWeave's $60.7 billion RPO carries a ~5-year weighted average duration and pays regardless of spot price, and Nebius's Microsoft and Meta contracts are committed multi-year revenue unchanged by the news.[^19,14] A spot-price dip cannot claw back already-contracted cash. Second, demand still outstrips supply — SemiAnalysis reported on-demand capacity "sold out across all GPU types" and rising reserved prices into 2026, the opposite of what a dumping thesis predicts.[^11] Third, a hyperscaler renting raw idle GPUs is not a like-for-like substitute for a rated full stack — networking, orchestration, reliability SLAs, support — and enterprises may distrust buying compute from a competitor.[^17] Fourth, the plan is unconfirmed, product-less, and Meta has never run an external cloud.[^1]

There is even a precedent argument that "selling surplus" is not a stable strategy. The popular story that AWS was built from Amazon's spare holiday retail capacity is a myth — AWS was purpose-built from inception, per co-proposer Benjamin Black ("From day one, every part of AWS has been purpose built for AWS").[^33,34] The only durable mechanism for selling idle capacity, the cloud spot market, is a deep-discount clearing layer bolted onto purpose-built fleets, not a business in itself. Genuine idle silicon depreciates too fast to anchor a stable business, which is exactly why profitable operators purpose-build and contract forward.

:::statement(attr="ARA Research")
The near term belongs to the contracts; the terminal value belongs to the narrative. Take-or-pay backlog defends 2026–2029 cash flows — it does not defend 2028+ renewal pricing, customer concentration, or the multiple.
:::
The genuine bear counter, then, is a duration mismatch, not a cash-flow one. What repriced was not this year's revenue but the *terminal* assumptions: that hyperscalers remain net buyers, that GPU scarcity persists to contract-renewal, and that neoclouds keep their pricing power. And the macro backdrop makes those assumptions fragile: OpenAI alone has amassed roughly $1.4 trillion of multi-year compute commitments — including ~$300 billion with Oracle and an up-to-$100 billion Nvidia investment — against a small revenue base, a circular structure in which Nvidia funds customers who buy Nvidia chips that neoclouds finance with GPU-collateralized debt.[^35,36] Jim Chanos warned that a ~3-year real GPU life would break "the whole economics of a lot of these deals."[^37] In that world, any hyperscaler wobble de-rates the debt-funded neoclouds first — and Meta Compute is simply the wobble with a name.

## 09. What could break this thesis — and the verdict

The thesis of this report is deliberately narrow: Meta's "surplus" is a transitional byproduct of front-loading rather than a structural excess, and the July 1 repricing is part mechanism, part reflex — real on terminal value, overdone on near-term cash flows. Here is what would falsify it.

- **A Meta capex cut.** If Meta *reduces* 2026–2027 capex guidance, "overbuild" becomes real and durable, the surplus is structural, and the bear case strengthens sharply. No analyst currently forecasts this; Wells Fargo explicitly does not.[^17] This is the single cleanest tell to watch.
- **Meta Compute actually launches at scale with a price.** A published price sheet materially below neocloud reserved rates would convert narrative into mechanism. As of the report there is no product, no pricing, and Muse Spark is unreleased.[^1] Bloomberg Intelligence's estimate that an xAI-style resale business could reach $50–100 billion by 2028–2030 is an aspirational ceiling, not a booking.[^19]
- **The GPU shortage ends.** If SemiAnalysis's "sold out" reverses and reserved H100 pricing rolls back over, the demand-absorbs-supply rebuttal collapses and a Meta surplus lands on a soft market.[^11] Conversely, persistent scarcity absorbs any Meta capacity and vindicates the bulls.
- **Depreciation catches up.** If economic GPU life proves closer to Burry's 2–3 years than the six-year book, neocloud margins and collateral erode together — independent of anything Meta does.[^29]
- **Resale rights don't exist.** If Meta legally cannot resell leased capacity (Rosenblatt's read of the CoreWeave contract through 2032), the incremental supply is smaller than the headline implies and the sell-off was mostly reflex.[^17]

The adversarial pass on this report's three load-bearing claims — the $18B one-session repricing, Meta's simultaneous net-buyer status, and the power-as-binding-constraint frame — turned up no contradicting primary source; each survived (one secondary source put Meta's July 1 gain nearer 8% than 10%, corrected above). ==Red-team pass: 3/3 top claims unbroken.==

The verdict from first principles: the word "surplus" is doing too much work. Meta is not a company drowning in idle GPUs; it is a compute-constrained buyer whose front-loaded, power-first build creates a *transient* rentable slack that it may monetize to earn a return on ~$183 billion of commitments and offset a depreciation clock it started by lengthening useful lives.[^10] {accent}That is enough to reprice terminal assumptions for companies valued at 8–76× sales — but not enough, on the current evidence, to end the neocloud boom.{/} The real signal will not be a Bloomberg report. It will be a capex line.

:::references
- {id: 1, title: "Meta pops as company makes cloud push to sell excess AI compute", url: "https://www.cnbc.com/2026/07/01/meta-stock-cloud-ai-compute.html", source: CNBC, date: "2026-07-01"}
- {id: 2, title: "Nebius, CoreWeave, IREN tumble on Meta cloud plan", url: "https://finance.yahoo.com/technology/ai/articles/nebius-coreweave-iren-tumble-meta-162444225.html", source: Yahoo Finance, date: "2026-07-01"}
- {id: 3, title: "Mark Zuckerberg says Meta starting a cloud business is 'on the table'", url: "https://www.cnbc.com/2026/05/27/mark-zuckerberg-says-meta-starting-cloud-business-on-the-table.html", source: CNBC, date: "2026-05-27"}
- {id: 4, title: "Zuckerberg says Meta cloud business is 'definitely on the table' as AI capex hits $145B", url: "https://mlq.ai/news/zuckerberg-says-meta-cloud-business-is-definitely-on-the-table-as-ai-capex-hits-145-billion/", source: MLQ.ai, date: "2026-05-27"}
- {id: 5, title: "Meta Q4 & FY2025 earnings release (Exhibit 99.1)", url: "https://s21.q4cdn.com/399680738/files/doc_financials/2025/q4/Meta-12-31-2025-Exhibit-99-1-FINAL.pdf", source: Meta Platforms (SEC 8-K), date: "2026-01-28"}
- {id: 6, title: "Meta Q1 2026 earnings release (Exhibit 99.1) — capex guidance raise", url: "https://www.sec.gov/Archives/edgar/data/0001326801/000162828026028364/meta-03312026xexhibit991.htm", source: SEC EDGAR, date: "2026-04-29"}
- {id: 7, title: "Meta to invest hundreds of billions into compute; Prometheus & Hyperion", url: "https://www.datacenterdynamics.com/en/news/meta-to-invest-hundreds-of-billions-of-dollars-into-compute-to-build-superintelligence-with-several-multi-gw-data-center-clusters/", source: DatacenterDynamics, date: "2025-07-14"}
- {id: 8, title: "Entergy to power Meta's data center in Richland Parish, Louisiana", url: "https://www.entergy.com/news/entergy-louisiana-power-meta-s-data-center-in-richland-parish", source: Entergy, date: "2024-12-04"}
- {id: 9, title: "Constellation & Meta sign 20-year nuclear deal (Clinton, 1,121 MW)", url: "https://www.constellationenergy.com/news/2025/constellation-meta-sign-20-year-deal-for-clean-reliable-nuclear-energy-in-illinois.html", source: Constellation Energy, date: "2025-06-03"}
- {id: 10, title: "Meta FY2025 Form 10-K — useful-life change (5.5 yr; $2.92B)", url: "https://www.sec.gov/Archives/edgar/data/0001326801/000162828026003942/meta-20251231.htm", source: SEC EDGAR, date: "2026-01-29"}
- {id: 11, title: "The Great GPU Shortage: rental capacity ($1.70→$2.35, sold out)", url: "https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity", source: SemiAnalysis, date: "2026-04-02"}
- {id: 12, title: "Meta Q3 2025 earnings call transcript — 'front-load' compute", url: "https://s21.q4cdn.com/399680738/files/doc_financials/2025/q3/META-Q3-2025-Earnings-Call-Transcript.pdf", source: Meta Platforms, date: "2025-10-29"}
- {id: 13, title: "CoreWeave & Meta announce $21 billion expanded AI infrastructure agreement", url: "https://www.coreweave.com/news/coreweave-and-meta-announce-21-billion-expanded-ai-infrastructure-agreement", source: CoreWeave, date: "2026-04-09"}
- {id: 14, title: "Nebius signs new AI infrastructure agreement with Meta (up to ~$27B, Vera Rubin)", url: "https://nebius.com/newsroom/nebius-signs-new-ai-infrastructure-agreement-with-meta", source: Nebius Group, date: "2026-03-16"}
- {id: 15, title: "Meta Q1 2026 follow-up call transcript — 'compute-constrained'", url: "https://s21.q4cdn.com/399680738/files/doc_financials/2026/q1/META-Q1-2026-Follow-Up-Call-Transcript.pdf", source: Meta Platforms, date: "2026-04-29"}
- {id: 16, title: "Google limits Meta's use of its Gemini AI models (FT)", url: "https://www.cnbc.com/2026/06/28/google-limits-metas-use-of-its-gemini-ai-models-ft-reports.html", source: CNBC / Financial Times, date: "2026-06-28"}
- {id: 17, title: "Rosenblatt reiterates CoreWeave (Buy, $250) amid Meta cloud reports", url: "https://www.investing.com/news/analyst-ratings/rosenblatt-reiterates-coreweave-stock-rating-amid-meta-cloud-reports-93CH-4771129", source: Investing.com, date: "2026-07-01"}
- {id: 18, title: "Neocloud market forecast to approach $400B by 2031", url: "https://www.srgresearch.com/articles/neocloud-market-forecast-to-approach-400b-by-2031-driven-by-surging-ai-infrastructure-demand", source: Synergy Research Group, date: "2026-02-01"}
- {id: 19, title: "CoreWeave FY2025 Form 10-K (revenue, RPO, concentration, debt, useful life)", url: "https://s205.q4cdn.com/133937190/files/doc_financials/2025/q4/CoreWeave-Inc-FY25-10-K-7.pdf", source: CoreWeave (SEC 10-K), date: "2026-02-24"}
- {id: 20, title: "Meta cloud report weighs on CoreWeave & Nebius (combined ~$62.2B exposure)", url: "https://ts2.tech/en/meta-platforms-nasdaqmeta-cloud-report-sends-shares-higher-weighs-on-coreweave-nasdaqcrwv-nebius-nasdaqnbis/", source: TS2 Tech, date: "2026-07-01"}
- {id: 21, title: "Nebius Q1 2026 shareholder letter (ARR $1.92B; $7–9B target)", url: "https://www.sec.gov/Archives/edgar/data/0001513845/000110465926059872/tm2614392d1_ex99-2.htm", source: SEC EDGAR (6-K), date: "2026-05-13"}
- {id: 22, title: "Nebius–Microsoft agreement 6-K ($17.4B, up to $19.4B)", url: "https://www.sec.gov/Archives/edgar/data/0001513845/000110465925088312/tm2525580d1_6k.htm", source: SEC EDGAR (6-K), date: "2025-09-08"}
- {id: 23, title: "Meta Compute and the neocloud reaction — D.A. Davidson view", url: "https://easternherald.com/2026/07/02/meta-compute-cloud-business-excess-ai-capacity-coreweave-nebius-2026/", source: Eastern Herald, date: "2026-07-01"}
- {id: 24, title: "Nebius stock and the Meta cloud plan — repricing mechanism", url: "https://www.techi.com/nebius-stock-meta-cloud-plan/", source: TECHi, date: "2026-07-01"}
- {id: 25, title: "H100 rental price over time", url: "https://www.silicondata.com/blog/h100-rental-price-over-time", source: Silicon Data, date: "2025-12-01"}
- {id: 26, title: "NVIDIA H100 pricing 2026: rent-vs-buy break-even analysis", url: "https://www.gmicloud.ai/en/blog/nvidia-h100-gpu-pricing-2026-rent-vs-buy-cost-analysis", source: GMI Cloud, date: "2026-01-01"}
- {id: 27, title: "Roth says neocloud selloff overdone; buyer of CoreWeave", url: "https://www.tipranks.com/news/the-fly/roth-says-neocloud-selloff-overdone-buyer-of-coreweave-on-metas-cloud-news-thefly-news", source: TipRanks / TheFly, date: "2026-07-01"}
- {id: 28, title: "Amazon FY2024 Form 10-K — server useful life cut to 5 years", url: "https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm", source: SEC EDGAR, date: "2025-02-07"}
- {id: 29, title: "Michael Burry accuses AI hyperscalers of boosting earnings via depreciation", url: "https://www.cnbc.com/2025/11/11/big-short-investor-michael-burry-accuses-ai-hyperscalers-of-artificially-boosting-earnings.html", source: CNBC, date: "2025-11-11"}
- {id: 30, title: "Data centers drive record GE Vernova orders; turbine slots tighten through 2030", url: "https://www.power-eng.com/gas/turbines/data-centers-drive-record-surge-in-ge-vernova-power-equipment-orders-as-turbine-slots-tighten-through-2030/", source: Power Engineering, date: "2026-04-23"}
- {id: 31, title: "ERCOT's large-load queue has nearly quadrupled in a single year", url: "https://www.latitudemedia.com/news/ercots-large-load-queue-has-nearly-quadrupled-in-a-single-year/", source: Latitude Media, date: "2025-12-03"}
- {id: 32, title: "DOE report on increased electricity demand from data centers (6.7–12% by 2028)", url: "https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers", source: US Dept. of Energy / LBNL, date: "2024-12-01"}
- {id: 33, title: "The myth about how Amazon's web service started just won't die", url: "https://www.networkworld.com/article/936248/the-myth-about-how-amazon-s-web-service-started-just-won-t-die.html", source: Network World, date: "2015-03-02"}
- {id: 34, title: "EC2 origins", url: "https://blog.b3k.us/2009/01/25/ec2-origins.html", source: Benjamin Black, date: "2009-01-25"}
- {id: 35, title: "Oracle's $300B bet on OpenAI; ~$1.4T commitments", url: "https://finance.yahoo.com/news/oracle-made-a-300-billion-bet-on-openai-its-paying-the-price-205441863.html", source: Yahoo Finance, date: "2025-12-13"}
- {id: 36, title: "Nvidia's up-to-$100B OpenAI investment and circular-financing concerns", url: "https://fortune.com/2025/09/28/nvidia-openai-circular-financing-ai-bubble/", source: Fortune, date: "2025-09-28"}
- {id: 37, title: "Jim Chanos sees debt defaults in Nvidia-chip-backed lending", url: "https://finance.yahoo.com/news/famed-short-seller-jim-chanos-sees-risks-in-growing-debt-market-backed-by-nvidias-ai-chips-theres-going-to-be-debt-defaults-110013557.html", source: Yahoo Finance, date: "2025-12-01"}
:::
