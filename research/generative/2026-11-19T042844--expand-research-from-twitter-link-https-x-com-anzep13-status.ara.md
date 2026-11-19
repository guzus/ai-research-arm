---
eyebrow: ANALYSIS · ONCHAIN LENDING · DEFI
title: "Morpho vs. Aave: Is the \"BD War\" Real, and Who Is Winning It?"
deck: Two protocols, two theories of distribution. One bundles the stack and ships its own products; the other sells neutral plumbing to Coinbase, Base, Robinhood and Circle. The scoreboard says the gap is closing, but not for the reason the BD framing suggests.
lede: |
  On 18 November 2026 @anzep13 wrote that "Morpho and Aave are in a full BD war right now, and they're taking different strategies to achieve their goals," adding that liquidity and asset support are the obvious factors.[^1] We tested that against filings from both protocols' own governance venues, DefiLlama and Token Terminal readbacks, and third-party reports. The partnership race is real, but it is smaller than the framing implies. The largest share shift in 2026 came from a risk event, not a deal. Every figure below is dated, and several data series conflict.
stats:
  - {label: "Morpho TVL as share of Aave's", value: "68%", note: "from 19% at 2025-09-01; as of 2026-11-16"}
  - {label: "Aave borrowed / Morpho borrowed", value: "$11.1B / $5.3B", note: "gap shrank from ~8x to ~2x"}
  - {label: "Aave protocol revenue, Q3 2026", value: "$17.3M", note: "-36.6% vs Q2"}
  - {label: "Morpho protocol revenue", value: "$0", note: "per DefiLlama, 2026-11-19"}
---

:::kv
- {term: "Is there a BD war?", def: "Yes, but it is asymmetric: Aave Labs sells an integrated stack (V4, Horizon, App, Pro, Kit); Morpho sells neutral rails to distributors (Coinbase, Base, Robinhood Chain, Arc)."}
- {term: "Who is gaining?", def: "Morpho, on every share metric: TVL ratio 19% to 68% and borrowed ratio ~12% to ~48% since 2025-09-01 (Aave V3 borrowed as the baseline)."}
- {term: "Why?", def: "Mostly not BD. Aave's April 2026 rsETH shock and outflows explain the biggest step; Morpho's growth is concentrated in a few distributors and curators."}
- {term: "Who still leads?", def: "Aave on borrowed dollars, utilization and protocol revenue; Morpho on growth, RWA-type collateral borrowed and exchange-grade distribution."}
- {term: "Biggest caveat", def: "The headline RWA comparison and most TVL series mix definitions; no clean monthly series from one source was obtainable here."}
:::

## 01. What the tweet claims, and what can be tested

**Thesis: "BD war" decomposes into three testable propositions: distribution wins, asset-support speed, and liquidity depth.**

The seed post is by @anzep13 and was published 2026-11-18. The version retrievable here ends mid-sentence ("liquidity and asset support are the obvious factors…"), because the full text sits in a linked note tweet that was not accessible, so the argument beyond that point is not assessed.[^1] The visible claim is simple: business development matters a great deal in onchain lending, it will matter more, and the two protocols are pursuing it differently.

A tweet from a commentator is evidence of what the author said, not of the underlying facts.[^1] So we convert it into three claims we can check against primary material. First, **distribution**: which protocol has won the front-ends where users and institutions actually originate loans. Second, **asset support**: how quickly each can list a new collateral token, especially tokenized real-world assets (RWAs). Third, **liquidity**: whether deposits and borrowed dollars are flowing toward one or the other.

An independent framing exists in the research literature. Tiger Research argued in June 2026 that shared-pool lending lets one asset's failure spread across the whole system, and that DeFi lending is converging on modular designs where the operational layer, meaning risk judgment and curation, becomes the competitive surface.[^39] That is a claim about architecture, not about partnerships, and it will matter later: if architecture decides outcomes, BD is a second-order variable.

:::callout(kind=warn, label="Method note")
No single clean monthly series for both protocols could be retrieved: DefiLlama's history endpoints exceed the fetch limit used here, and Token Terminal's TVL definition differs from DefiLlama's. We therefore use dated snapshots from named sources and flag every definitional conflict, rather than drawing a line chart that would hide the mismatch.
:::

**Why this matters:** if the war is mostly about distribution, the winner can be predicted from partner announcements. If it is mostly about risk architecture, the winner is decided by incidents. The evidence below favors the second reading for 2026.

## 02. The scoreboard: share has moved, but Aave still leads where money is borrowed

**Thesis: Morpho has closed most of the gap on deposits and about two thirds of the gap on borrowed dollars since September 2025, while Aave still lends out more per deposited dollar.**

As of 2026-11-16, DefiLlama figures relayed by CoinPaprika put Aave (V3 plus V4) at $15.11B TVL and $11.10B borrowed, against Morpho at $10.22B TVL and $5.34B borrowed.[^2] Since 2025-09-01, Aave's TVL is down 61.4% and Morpho's is up 37.8%; Aave V3 borrowed fell from $28.13B to $10.59B while Morpho borrowed rose from $3.49B to $5.34B.[^2] Morpho's TVL is about 12% below its record of 5 November 2026.[^2]

:::slope(left-label="2025-09-01", right-label="2026-11-16", unit="$B borrowed")
| Item | 2025-09-01 | 2026-11-16 |
|------|------------|------------|
| Aave V3 | 28.13 | 10.59 |
| Morpho | 3.49 | 5.34 |
:::

:::source
Borrowed balances per DefiLlama as relayed by CoinPaprika (2026-11-16). Aave shown as V3 only because the baseline is V3; the V3-to-total difference is about $0.5B of V4 borrowed.
:::

Computed from the same inputs, Morpho's borrowed balance is about 48% of Aave's (all versions) on 2026-11-16, versus about 12% on the 2025-09-01 V3 baseline.[^2] Direct DefiLlama calls made on 2026-11-19 returned $13.67B for Aave V3 and $9.91B for Morpho's `morpho-v1` slug, consistent with a continued slide at Aave and a small pullback at Morpho from the November peak, though the scopes differ from the 11-16 figures.[^34][^35]

Aave is not just bigger; it is more fully used. On 2026-11-16 Aave V3 lent out 43% of deposits against 35% for Morpho Blue.[^2] Morpho's own recaps put total deposits above $17B, and The Block reported Blue at about $5.2B of loans against $16B of deposits in September, an implied utilization near 32.5%.[^16][^36] A deposit-weighted comparison therefore flatters Morpho: part of its TVL is capital looking for borrowers.

:::rank-list
- {label: "Aave V3", value: "$16.8B", pct: 100, highlight: true}
- {label: "Morpho Blue", value: "$9.8B", pct: 58, highlight: true}
- {label: "SparkLend", value: "$4.9B", pct: 29}
- {label: "JustLend", value: "$3.6B", pct: 21}
- {label: "Compound V3", value: "$1.4B", pct: 8}
- {label: "Kamino", value: "$1.3B", pct: 8}
- {label: "Fluid", value: "$0.75B", pct: 4}
- {label: "Euler V2", value: "$0.33B", pct: 2}
:::

:::source
Lending TVL by protocol on 2026-09-15 (DefiLlama lending category, via eco.com; low confidence, internally inconsistent page). The same two names remain far ahead of the field.
:::

The ranking matters because it shows the contest is a duopoly with a long tail: the next largest EVM lender, SparkLend, held roughly half of Morpho's TVL in mid-September.[^33] That raises the stakes of the Aave-vs-Morpho framing and also lowers its explanatory power for the whole category: Token Terminal's September report found Aave held 47% of tracked active loans, down 17.4 percentage points year on year, so some of the share that left Aave went to neither of the two.[^28]

**Counterpoint:** these series mix tools. Token Terminal's Aave TVL (about $31.4B average for September) is roughly twice DefiLlama's figure for the same month because the definitions differ, and no source reconciled them.[^28][^33] A clean line chart cannot be drawn honestly from what is public here.

**Why this matters:** "Morpho is catching up" is true on every metric tried, but "Morpho is winning" is not: Aave remains larger on borrowed dollars and far larger on revenue.

## 03. Aave's strategy: sell the whole stack, then govern the listings

**Thesis: Aave Labs is trying to turn a protocol into a product company with its own BD function, and the numbers show that bet is early.**

Aave V4 went live on Ethereum on 2026-03-30 with three hubs (Prime, Core and Plus) that give credit lines to spokes, with launch spokes including Lido, EtherFi, Kelp, Ethena and Lombard.[^25] Liquidity is pooled at the hub while collateral and liquidation rules are isolated per spoke.[^39] V4 is also where Aave's distribution plans live: V4 supplied grew from $212.6M on 2026-07-01 to $1.34B on 2026-10-01, a 6.3-fold rise in a quarter, with $402.9M borrowed.[^3] But V4 was still only about 5.2% of Aave TVL on 2026-11-16.[^2]

The commercial side is the "Aave Will Win" framework, whose February 2026 temp check proposed routing 100% of Aave-branded product revenue (App, Pro, Kit, Horizon and others) to the DAO treasury, with Aave Labs funded $25M in stablecoins and 75,000 AAVE vesting over two years.[^24] AIP 469, the binding step, is listed as executed in Aave Labs' own report.[^3] In the same report, Labs lists 97 staff and $19.48M of spend excluding token compensation, of which BD & Growth was $3.57M, about 18.3%.[^3]

Revenue from that machine is still small. Aave Labs' net product revenue was $1.17M in Q2 and $1.31M in Q3 2026, mainly Aave Pro/aave.com CoW fees, with Horizon contributing roughly $100K per quarter.[^3] Over the same 180 days protocol revenue was $44.58M, so product revenue was about 5.6% of it.[^3] Labs' reported partners include EtherFi Cash (over 100,000 cardholders) and Coinbase tokenized stocks on Base, where Coinbase's announcement describes Aave as the sole credit infrastructure,[^27] plus Circle Mint customers borrowing USDC against cirBTC on Arc.[^26]

:::bars
- {label: "Engineering + product", value: "63%", pct: 63}
- {label: "BD & Growth", value: "18%", pct: 18}
- {label: "Legal, finance, other", value: "19%", pct: 19}
:::

:::note
Aave Labs spend (excl. token compensation), Q2+Q3 2026, from the report's own table: engineering 43.0% plus product 20.2%, BD & Growth 18.3%, legal, finance and other operations the remainder. Unaudited.
:::

**Who decides what gets listed?** Aave's governance is a three-key system: Labs publishes technical assessments, a risk provider (LlamaRisk for most V4 and Horizon listings) recommends parameters, and the DAO votes via ARFC and Snapshot, with some V4 and Horizon markets using the Snapshot as the binding step and Risk Stewards handling routine cap changes.[^26] For Horizon, since 2026-08-14 each new fund needs an ARFC with a business case, a LlamaRisk assessment, an Aave Labs technical assessment and a binding Snapshot, according to Protofire.[^4]

**Counterpoints.** (1) Governance friction is itself a BD cost. The Defiant described a DAO publicly fracturing in February, with BGD Labs departing and contributors disputing Aave Labs' compensation.[^40] (2) After the April incident Aave's buyback was halted effective 2026-04-19, and a restart thread auto-closed on 2026-07-26 without a vote, so token-holder value accrual is unresolved.[^31][^32] (3) Aave's partner claims are self-reported in Labs' development updates; partner-side confirmation is thin, and no revenue figure is attached to any of the named integrations.[^26][^27]

**Why this matters:** Aave is spending on BD, but the revenue it reports from products is a rounding error against its lending revenue. The BD bet is a bet on future V4 volume, not a current earner.

## 04. Morpho's strategy: be the plumbing, let others own the customer

**Thesis: Morpho wins by being embedded in other companies' products, and its main strategic risk is the concentration that this creates.**

Morpho Association announced a $175M raise on 2026-06-09, co-led by Paradigm, a16z crypto and Ribbit, with Apollo Funds, Circle Ventures, VanEck and Ledger Cathay among the strategic participants, and states $11B+ in deposits.[^12] Fortune and The Block report it was a purchase of MORPHO tokens at the monthly average price, not equity, at a reported valuation of up to $2B.[^13][^14] A token purchase at market price carries no negotiated premium, so "$2B valuation" describes the token's fully diluted value, not a private mark.[^13]

The distribution record is concrete. Coinbase runs bitcoin-backed USDC loans through Morpho and in September added fixed-rate loans on Morpho Midnight alongside variable-rate loans on Blue; Coinbase's variable-rate book exceeded $1.4B outstanding against Blue's roughly $5.2B across all integrations.[^16] That is about 27% of Blue's loans from one distributor.[^16] A Steakhouse report from 2026-07-14 found over half of Morpho's $2.8B+ USDC supply sat in Steakhouse vaults, with about 65% of Base USDC via Steakhouse and about $368M from the Coinbase App lending product alone.[^22] Morpho's own recaps add Arc ($220M+ of day-one deposits) and Robinhood Chain ($1B within three months) as sponsor-driven launches.[^36][^37]

Institutional ties run deeper than product integrations. Under a cooperation agreement announced 2026-02-13, Apollo affiliates may acquire up to 90M MORPHO over 48 months, with transfer and trading restrictions; it is a ceiling, not a purchase commitment, and no dollar amount is disclosed.[^17] Base's Earn & Borrow stack, announced 2026-10-13, lets apps embed lending through Morpho and Aave, and a secondary summary dated 2026-10-15 puts Morpho on Base at about $4.38B TVL versus roughly $533M for Aave V3 there; these figures move daily and were not independently re-pulled.[^30]

:::callout(kind=info, label="For aggregators the two are substitutes")
Galaxy's GOFR blends rates from Aave, Morpho, Spark, Kamino and others into one continuously rebalanced rate, with Galaxy committing up to $100M of first-loss capital.[^23] A distributor that routes across both protocols is not choosing a side in the BD war.
:::

The new product line is fixed-rate credit. Morpho Midnight launched on Base on 2026-07-21 with a cbBTC/USDC pair and limited maturities, and Morpho itself warns the model only works when enough participants quote both sides.[^15] Morpho's October recap put Midnight deposits at about $200M,[^37] while its September recap put total deposits above $17B,[^36] so the roughly 1.2% share mixes two months; The Block had reported only about $30M of Midnight deposits at the Coinbase fixed-rate launch in September.[^16] It is a strategic option, not yet a driver.

**Counterpoints.** (1) Concentration: one distributor is about a quarter of Blue's loans, and one curator holds over half of USDC supply, so a single partner decision can move the totals.[^16][^22] (2) Curator risk is real: after Stream Finance's $93M loss in November 2025, Yields and More mapped about $285M of potential exposure across DeFi and put MEV Capital's at about $25.4M.[^29] (3) Many figures here are Morpho's or its curators' own, and the Steakhouse report comes from a participant with a commercial interest.[^22]

**Why this matters:** Morpho's strategy converts other firms' customers into its balance sheet, which scales fast but leaves it dependent on a handful of counterparties for its growth narrative.

## 05. Asset support and RWAs: a headline that needs its denominator

**Thesis: Morpho lists faster, but the widely shared "RWAs are picking Morpho" comparison rests on a single commercially interested snapshot and mismatched definitions.**

Mechanically the difference is real. On Morpho Blue anyone can create a market with five parameters (loan token, collateral token, oracle, LLTV and interest-rate model), though the LLTV must be one governance has enabled.[^20] Supply still depends on a curator choosing to allocate, so a market can exist and stay empty.[^4] Vaults V2 splits roles into owner, curator, allocator and sentinel, with timelocks and an adapter architecture.[^21] On Aave Horizon, each fund goes through an ARFC and binding vote, and new listings can arrive weeks after a vote.[^4]

The numbers behind the viral comparison come from Protofire's 2026-10-18 guide: 59 Morpho markets with about $657.2M borrowed (against $887.0M collateral) versus Horizon at $121.4M borrowed against $151.0M collateral.[^4] That is about 5.4 times on a borrowed basis.[^4] But three problems qualify it. First, Protofire discloses that it earns a share of borrower interest on its own white-label market stack, so it is not a neutral party.[^4] Second, the page itself warns that rows "should not be added together" because Morpho rows show loans while some others show collateral.[^4] Third, the Morpho total is concentrated: one PRIME/PYUSD market had $186.1M borrowed against $259.4M, and six Treasury-token markets (BUIDL, USTB, USDY, JTRSY, VBILL, USYC) held $0.[^4]

:::stats
- {label: "Morpho RWA-type borrowed", value: "$657.2M", note: "59 markets; Protofire, 2026-10-18"}
- {label: "Horizon borrowed", value: "$121.4M", note: "same snapshot"}
- {label: "Horizon TVL (ex-loans)", value: "$254.3M", note: "from $420.9M on 2026-01-12"}
- {label: "Largest Morpho RWA market", value: "$186.1M", note: "PRIME/PYUSD; ~28% of the total"}
:::

Horizon's own trend is negative. Its TVL excluding loans was $254.3M on 2026-10-18, down about 39.6% from $420.9M on 2026-01-12, and Aave's recap had reported over $570M of deposits at the end of 2025, though the two figures are different metrics and not comparable.[^4][^38] Aave Labs' report lists RWA-backed active loans passing $500M on 2026-06-30 across Horizon and other markets, which again is a different scope.[^3] The honest summary is that Morpho has more borrowed against credit-style RWA tokens, Horizon is smaller than it was in January, and neither number says which protocol RWA issuers will prefer after the fund-share and Treasury categories mature.

**Counterpoint.** Aave's counter-strategy does not need to win this table. It lists tokenized equities on V4 (Coinbase equities on Base),[^26] and its Horizon partner roster (VanEck, Circle, Securitize, Ripple, WisdomTree, Superstate and others) is built around regulated issuers rather than permissionless markets.[^38] Whether regulated issuers value a binding DAO vote as a feature or a delay is an open empirical question.

**Why this matters:** the RWA contest is real but is currently measured by one commercially interested snapshot. Treat 5.4x as an upper-bound illustration, not a market share.

## 06. Liquidity and risk: the April shock explains more than any partnership

**Thesis: the biggest single change in relative position was the Kelp rsETH exploit, which exposed the cost of pooled liquidity and moved deposits away from Aave.**

On 2026-04-18, 116,500 rsETH (about $292M) was taken from Kelp's bridge; Aave-specific bad-debt exposure was roughly $196M, Aave's TVL fell from $26.4B to nearly $20B, and AAVE dropped 16% to $92.[^5] Aave's own incident report says 89,567 rsETH was posted as collateral and used to borrow WETH, and modelled bad debt of $123.7M to $230.1M depending on how losses were socialized.[^10] Galaxy recorded Aave's TVL falling to $17.9B within 48 hours and WETH markets reaching 100% utilization, which trapped ordinary depositors who had not touched rsETH.[^9]

The response was funded by the DAO and partners rather than depositors: a 2026-04-24 ARFC proposed 25,000 ETH from the DAO, with 14,570 ETH in public pledges and a Mantle credit facility of up to 30,000 ETH against a residual gap of about 75,081 ETH.[^11] Aave Labs' report records AIP 478 (executed 2026-05-06) liquidating the eight attacker positions and AIP 482 (2026-05-16) restoring WETH borrowing limits across six V3 markets.[^3] No final realized bad-debt figure appears in the Aave sources retrieved; a single secondary investigation reports that Aave wrote off about $124.5M of bad debt on 2026-05-06, close to the low scenario in Aave's own report, which would put the $196M exposure figure above the realized loss.[^41]

Morpho's CEO reported only about $1M of exposure across two isolated markets, which Galaxy attributes to market-level isolation, though that is a self-reported number and curator selection may also have kept rsETH out.[^9]

:::timeline
- {date: "2025-11-04", headline: "Stream Finance fallout", body: "Analysts map ~$285M of cross-DeFi exposure; MEV Capital's Morpho vaults hit (~$25.4M exposure)."}
- {date: "2026-02-12", headline: "Aave Will Win temp check", body: "100% of Aave-branded product revenue to DAO; $25M funding to Aave Labs."}
- {date: "2026-03-30", headline: "Aave V4 live on Ethereum", body: "Prime, Core and Plus hubs; Lido, EtherFi, Kelp, Ethena, Lombard spokes."}
- {date: "2026-04-18", headline: "Kelp rsETH exploit", body: "Aave TVL falls from $26.4B to nearly $20B; buybacks paused from 04-19."}
- {date: "2026-06-09", headline: "Morpho raises $175M", body: "Token purchase; Apollo, Circle Ventures, VanEck participate."}
- {date: "2026-07-21", headline: "Morpho Midnight launches", body: "Fixed-rate, fixed-term credit on Base."}
- {date: "2026-10-13", headline: "Base Earn & Borrow", body: "Embeddable lending through Morpho and Aave."}
:::

The risk story cuts both ways. Morpho's curator layer had its own failure in November 2025.[^29] Its Vaults V2 design answers part of that with timelocks and a sentinel role, but the curator still picks the risk.[^21] Tiger Research's view is that all three major designs (Morpho, Euler, Aave V4) are converging on modular risk isolation, so the operational layer becomes the competitive surface.[^39]

**Counterpoint.** TVL is price- and definition-sensitive, so the size of the April move varies by source: CoinDesk's fetched figure is about $6.6B, while Galaxy's reads about $8.45B within 48 hours.[^5][^9] The share loss to Morpho is also not the whole story: Token Terminal's data show Aave's loan share down 17.4 points year on year, but Aave's September active loans rose 8.1% month on month to $12.6B after the shock.[^28]

**Why this matters:** an incident changes a depositor's willingness to hold capital in a venue far faster than a partnership does. If another asset fails in a shared-pool market, the "BD war" scoreboard moves again, in the other direction if that failure is on Morpho's curators.

## 07. Who gets paid: the war is over customers, but the revenue goes elsewhere

**Thesis: Aave captures protocol revenue at the DAO level; Morpho's fees mostly flow to curators and depositors, so winning share does not yet translate into protocol revenue.**

Aave protocol revenue was $27,288,040 in Q2 2026 and $17,292,461 in Q3, a 36.6% quarter-on-quarter fall, $44,580,501 over the 180 days.[^3] Token Terminal's September report counts DAO revenue at $5.2M for the month and Aave fees at $36.5M, down 65.7% year on year.[^28] DefiLlama's 30-day fees on 2026-11-19 were $42.0M for Aave and $34.1M for Morpho, with trailing-year fees of $601.8M and $214.9M, so Aave's 30-day fees were about 1.23 times Morpho's, but about 2.8 times over the year.[^7][^8]

For Morpho, DefiLlama states no revenue accrues to the protocol.[^8] Morpho's own post says the DAO is considering protocol fees and that the restructuring made MORPHO the only asset, folding Morpho Labs into a subsidiary.[^18] 4Pillars noted in March that no fee-switch proposal had appeared in 128 Snapshot votes.[^19] 1kx's report credits Morpho with $62M of user-paid fees in Q3 2026, second among lending markets, much of it going to curators such as Steakhouse and Gauntlet; the same report puts onchain lending user-paid fees down about 50% year on year.[^6]

:::bars
- {label: "Aave, 30-day fees", value: "$42.0M", pct: 100}
- {label: "Morpho, 30-day fees", value: "$34.1M", pct: 81}
- {label: "Aave Q3 protocol revenue", value: "$17.3M", pct: 41}
- {label: "Aave Labs product revenue, Q3", value: "$1.3M", pct: 3}
- {label: "Morpho protocol revenue", value: "$0", pct: 0}
:::

:::source
DefiLlama fees API (2026-11-19); Aave Labs 180-day report (Q3 2026). Fee definitions differ by source and the two DefiLlama slugs may not cover every product.
:::

**Counterpoints.** (1) The 30-day Morpho fee figure ($34.1M) sits oddly beside the 1kx quarterly $62M; the definitions differ and we did not reconcile them.[^6][^8] (2) A zero-revenue protocol can still win: 4Pillars argued in March that Morpho "can be the dominant lending protocol and MORPHO can be a bad token at the same time," because no fee switch had been proposed.[^19] (3) A protocol fee would change the economics of every distribution deal, because partners currently capture the spread.

**Why this matters:** the BD war looks symmetric on the scoreboard but is asymmetric in what winning pays. Aave wins revenue first; Morpho wins customers first.

## 08. What would falsify this reading

**Thesis: the claim that distribution is not the primary driver is weakest where Morpho's growth is entirely partner-sourced.**

- **The partner-source objection.** Morpho's scale on Base and its Arc and Robinhood launches are all sponsor-driven.[^36][^37] If the April shock was the cause of share shift, Morpho's gains should appear across non-partner venues too; the evidence available here (Steakhouse, Coinbase) does not separate the two.
- **Definition drift.** The path of both TVLs depends on which slug and metric are used: Token Terminal's September average for Aave ($31.4B) is about twice DefiLlama's mid-September figure ($16.8B), and the two Morpho DefiLlama slugs differ on scope.[^28][^33][^35] We therefore rely on same-date, same-source pairs, and the ratios above should be read as indicative.
- **Aave's recovery path.** Token Terminal's September average TVL for Aave was up 13.9% month on month, and V4 grew 6.3-fold in a quarter; if V4 spokes bring in distribution partners such as EtherFi Cash and Circle at scale, the share trend could reverse.[^3][^26][^28]
- **The red-team pass.** An adversarial search of the three load-bearing claims found one medium-severity contradiction: the $196M Aave exposure figure was an early estimate, and a later single-source account reports about $124.5M written off, so we treat $196M as exposure, not realized loss.[^41] The 68% TVL ratio and the 30-day and trailing-year fee figures were not broken: DefiLlama pages around 17-18 November showed Aave near $14.9B-$15.1B and Morpho near $10.2B-$10.3B, and the fees API returned the quoted values.[^34][^7]
- **Unobserved events.** We found no sourced public Morpho-vs-Aave spat or distribution race event in October-November 2026 beyond the Base Earn & Borrow launch; the "war" label may describe a trend rather than a discrete contest.[^30]

**Why this matters:** a thesis that survives only if the data is read generously is a hypothesis, not a finding. The sections above give the specific readings that would overturn it.

## 09. What to watch

**Thesis: five observable events will resolve the BD framing within a few quarters.**

1. Whether Morpho's DAO adopts protocol fees, and whether distributors renegotiate.[^18][^19]
2. Whether Aave V4's share of Aave TVL, 5.2% on 2026-11-16, keeps rising, and whether external curators scale.[^2]
3. Horizon's TVL trend versus Morpho's credit-token markets in the next RWA snapshot.[^4]
4. Coinbase's share of Blue loans; a change in that single ratio moves Morpho's growth story.[^16]
5. Any new bad-debt event at either architecture, since the April shock showed that one event outweighs many partnerships.[^5][^29]

:::references
- {id: 1, title: "@anzep13 on Morpho vs Aave BD war (tweet; syndication copy, text truncated)", url: "https://x.com/anzep13/status/2123121413733109813", source: "X", date: "2026-11-18"}
- {id: 2, title: "DeFi Lending: Aave vs Morpho vs Spark vs Compound (DefiLlama data as of 2026-11-16)", url: "https://coinpaprika.com/education/defi-lending/", source: "CoinPaprika", date: "2026-11-16"}
- {id: 3, title: "Aave Labs 180-Day Report", url: "https://governance.aave.com/t/aave-labs-180-day-report/26342", source: "Aave governance forum", date: "2026-11-13"}
- {id: 4, title: "Lending Against Tokenized Assets: Aave vs Morpho", url: "https://protofire.io/guides/lending-against-tokenized-assets/", source: "Protofire", date: "2026-10-18"}
- {id: 5, title: "Aave records $6B TVL drop as Kelp hack exposes structural risk", url: "https://www.coindesk.com/tech/2026/04/19/aave-records-usd6-billion-tvl-drop-as-kelp-hack-exposes-structural-risk-at-defi-lender", source: "CoinDesk", date: "2026-04-19"}
- {id: 6, title: "Onchain Lending Fees Plunge 50% as Morpho Bucks the Trend (1kx report)", url: "https://news.bitcoin.com/finance/onchain-lending-fees-plunge-50-as-morpho-bucks-the-trend/", source: "Bitcoin.com News", date: "2026-10-29"}
- {id: 7, title: "DefiLlama fees summary: Aave", url: "https://api.llama.fi/summary/fees/aave?dataType=dailyFees", source: "DefiLlama API", date: "2026-11-19"}
- {id: 8, title: "DefiLlama fees summary: Morpho", url: "https://api.llama.fi/summary/fees/morpho", source: "DefiLlama API", date: "2026-11-19"}
- {id: 9, title: "KelpDAO LayerZero exploit and DeFi", url: "https://www.galaxy.com/insights/research/kelpdao-layerzero-exploit-defi", source: "Galaxy Research", date: "2026-04-22"}
- {id: 10, title: "rsETH Incident Report (April 20, 2026)", url: "https://governance.aave.com/t/rseth-incident-report-april-20-2026/24580", source: "Aave governance forum", date: "2026-04-20"}
- {id: 11, title: "ARFC: rsETH incident funding update", url: "https://governance.aave.com/t/arfc-rseth-incident-funding-update/24740", source: "Aave governance forum", date: "2026-04-24"}
- {id: 12, title: "Morpho Association raises $175M to build the open credit network for the world", url: "https://morpho.org/blog/morpho-association-raises-175m-to-build-the-open-credit-network-for-the-world", source: "Morpho", date: "2026-06-09"}
- {id: 13, title: "Morpho fundraise: a16z crypto, Paradigm, Ribbit Capital, $175 million", url: "https://fortune.com/2026/06/09/morpho-fundraise-a16z-crypto-paradigm-ribbit-capital-175-million/", source: "Fortune", date: "2026-06-09"}
- {id: 14, title: "Morpho raises $175M from Paradigm, a16z crypto, Ribbit Capital", url: "https://www.theblock.co/post/404111/morpho-raises-175m-paradigm-a16z-crypto-ribbit-capital", source: "The Block", date: "2026-06-09"}
- {id: 15, title: "Now live: Morpho Midnight", url: "https://morpho.org/blog/now-live-morpho-midnight", source: "Morpho", date: "2026-07-21"}
- {id: 16, title: "Coinbase launches fixed-rate bitcoin loans on Morpho Midnight", url: "https://theblock.co/news/defi/2026-09-22-coinbase-fixed-rate-bitcoin-loans-morpho-midnight-416050", source: "The Block", date: "2026-09-22"}
- {id: 17, title: "Morpho Association announces cooperation agreement with Apollo", url: "https://morpho.org/blog/morpho-association-announces-cooperation-agreement-with-apollo/", source: "Morpho", date: "2026-02-13"}
- {id: 18, title: "Aligning around MORPHO as the only asset", url: "https://morpho.org/blog/aligning-around-morpho-the-only-asset-for-morpho", source: "Morpho"}
- {id: 19, title: "Morpho: The Apollo pump is your exit", url: "https://research.4pillars.io/en/research/morpho-the-apollo-pump-is-your-exit", source: "4Pillars", date: "2026-03-16"}
- {id: 20, title: "Creating a market (Morpho Blue v1 docs)", url: "https://docs.morpho.org/curate/tutorials-market-v1/creating-market/", source: "Morpho docs"}
- {id: 21, title: "Morpho Vaults V2: a new standard for asset curation", url: "https://morpho.org/blog/morpho-vaults-v2-a-new-standard-for-asset-curation", source: "Morpho"}
- {id: 22, title: "DeFi Markets Update, 14 July 2026", url: "https://kitchen.steakhouse.financial/p/defi-markets-update-2026-07-14", source: "Steakhouse Financial", date: "2026-07-14"}
- {id: 23, title: "Galaxy blends Aave, Morpho and other DeFi rates in new GOFR crypto borrowing product", url: "https://www.theblock.co/news/defi/2026-07-14-galaxy-blends-aave-morpho-other-defi-rates-new-gofr-crypto-borrowing-product-408267", source: "The Block", date: "2026-07-14"}
- {id: 24, title: "Temp Check: Aave Will Win framework", url: "https://governance.aave.com/t/temp-check-aave-will-win-framework/24055", source: "Aave governance forum", date: "2026-02-12"}
- {id: 25, title: "Aave V4 launches on Ethereum mainnet", url: "https://www.theblock.co/news/defi/2026-03-30-aave-v4-launches-ethereum-mainnet-395617", source: "The Block", date: "2026-03-30"}
- {id: 26, title: "AL Development Update: October 2026", url: "https://governance.aave.com/t/al-development-update-october-2026/25979", source: "Aave governance forum", date: "2026-11-02"}
- {id: 27, title: "AL Development Update: August 2026", url: "https://governance.aave.com/t/al-development-update-august-2026/25579", source: "Aave governance forum", date: "2026-09-01"}
- {id: 28, title: "Aave September 2026 core metrics (Token Terminal report, press rewrite)", url: "https://cryptonews.net/news/defi/33567416/", source: "Cryptonews", date: "2026-10-09"}
- {id: 29, title: "Analysts map $285M in potential exposure across DeFi after Stream Finance's $93M loss", url: "https://www.theblock.co/news/defi/2025-11-04-analysts-map-285m-in-potential-exposure-across-defi-after-stream-finances-93m-loss-377491", source: "The Block", date: "2025-11-04"}
- {id: 30, title: "Base Earn & Borrow", url: "https://stablecoininsider.org/base-earn-and-borrow/", source: "Stablecoin Insider", date: "2026-10-15"}
- {id: 31, title: "ARFC: Pause Aave buybacks", url: "https://governance.aave.com/t/arfc-pause-aave-buybacks/24686", source: "Aave governance forum", date: "2026-04-19"}
- {id: 32, title: "Restart AAVE buy backs (thread)", url: "https://governance.aave.com/t/restart-aave-buy-backs/24936", source: "Aave governance forum", date: "2026-07-26"}
- {id: 33, title: "Best DeFi lending protocols 2026: TVL, rates, risk", url: "https://eco.com/support/en/articles/14800882-best-defi-lending-protocols-2026-tvl-rates-risk", source: "Eco", date: "2026-09-15"}
- {id: 34, title: "DefiLlama TVL: Aave V3", url: "https://api.llama.fi/tvl/aave-v3", source: "DefiLlama API", date: "2026-11-19"}
- {id: 35, title: "DefiLlama TVL: Morpho (morpho-v1)", url: "https://api.llama.fi/tvl/morpho-v1", source: "DefiLlama API", date: "2026-11-19"}
- {id: 36, title: "The Morpho Effect: September 2026", url: "https://morpho.org/blog/the-morpho-effect-september-2026", source: "Morpho", date: "2026-09"}
- {id: 37, title: "The Morpho Effect: October 2026", url: "https://morpho.org/blog/the-morpho-effect-october-2026", source: "Morpho", date: "2026-10"}
- {id: 38, title: "Aave 2025 recap", url: "https://aave.com/blog/aave-2025-recap", source: "Aave", date: "2025-12"}
- {id: 39, title: "DeFi Lending Is Modularizing: The Risk Management War Among Morpho, Euler, and Aave", url: "https://reports.tiger-research.com/p/defi-lending-is-modularizing-the-eng", source: "Tiger Research", date: "2026-06-16"}
- {id: 41, title: "Aave rsETH exploit investigation", url: "https://bitquery.io/investigations/aave-rseth-exploit-run", source: "Bitquery", date: "2026-05"}
- {id: 40, title: "Aave is eating itself", url: "https://thedefiant.io/newsletter/defi-daily/aave-is-eating-itself", source: "The Defiant", date: "2026-02-26"}
:::
