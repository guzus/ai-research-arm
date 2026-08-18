---
eyebrow: DEFI · MARKET STRUCTURE
title: "Hayden Adams Says AMMs Will Eat Global Finance. The Data Says: Not Like This."
deck: A tweet-essay case for automated market makers replacing Wall Street, checked line by line against the numbers its author didn't cite.
lede: |
  On August 18, 2026, Uniswap founder Hayden Adams published a long essay arguing automated market makers (AMMs) are retracing the arc index funds walked from "Bogle's Folly" to owning the majority of American savings — and that tokenized stocks trading against correlated assets, not dollars, will eventually unbundle the capital-strategy-execution stack that lets firms like Citadel Securities post record profits. Every piece of that argument is independently checkable. The data on DEX market share, AMM liquidity-provider economics, Uniswap's own new hook, Robinhood Chain's actual trade composition, and 2026 securities regulation tell a messier story than the essay does.
stats:
  - {label: "Uniswap cumulative volume", value: "$4.0T+", note: "confirmed, Dec 2025"}
  - {label: "DEX share of spot volume", value: "13.6%-24.5%", note: "swings, not a plateau"}
  - {label: "Citadel Securities 2025 revenue", value: "$12.2B", note: "verified"}
  - {label: "RWA tokenized market", value: "$34.7B", note: "55% shows zero weekly activity"}
---

:::callout(kind=info, label="The short answer")
Adams is right that DEX volume and tokenized real-world assets have grown fast, and right that Uniswap's v4 architecture is a genuine engineering advance. He is on much shakier ground claiming a durable ">20%" DEX share (the honest number swings between 13.6% and 24.5% depending on the month and the memecoin cycle), that the Bogle analogy predicts anything about AMM economics (index funds won on a fee/performance mechanism AMMs don't share), that "DualPool" concentrates liquidity across correlated pairs (it doesn't — it parks idle capital in yield vaults), and that tokenization is bypassing regulators (DTCC, Nasdaq, and NYSE's parent are building their own tokenization rails, under direct SEC permission, precisely to avoid being bypassed).
:::

## 01. What the essay actually claims

Adams's essay bundles four separate arguments that need to be pulled apart before any of them can be judged: a historical analogy (index funds were mocked, then won), a market-share statistic (DEXs grew "from under 1% of centralized spot volume to over 20%"), a market-structure indictment (Citadel Securities' "record $12.2 billion in net trading revenue" on "$21 billion of trading capital" is evidence of entrenchment, not efficiency), and a product roadmap (Uniswap v4 "hooks" and a "DualPool" hook will let liquidity providers earn better returns by concentrating around correlated pairs, the way ETH pairs with stETH or SOL pairs with Solana-ecosystem tokens) [^1]. Each of those four claims rests on a different kind of evidence — history, market data, corporate financials, and smart-contract mechanics — and each fails or holds up on its own terms.

That matters here specifically because the person making the argument is not a disinterested analyst. Adams founded Uniswap in 2018 and remains its most visible public voice; UNI, the protocol's governance token, traded near $3.25 (market cap roughly $2.03 billion) on the day the essay was published, down meaningfully from where it traded at the start of 2026 [^39]. A newly activated fee-burn mechanism (more on this in Section 09) ties UNI's value directly to Uniswap's usage and reputation [^35]. None of that makes the essay's factual claims false. It does mean every one of them needs the same scrutiny a sell-side note gets when the analyst's firm holds the stock.

The essay's real number, $4.6 trillion in cumulative Uniswap volume, sits close to independently reported figures: Uniswap Labs announced the protocol crossed $4 trillion in cumulative volume on December 2, 2025, reaching each successive trillion faster than the last — four years to $1 trillion, two years to $2 trillion, one year to $3 trillion, six months to $4 trillion [^2]. Extrapolating that acceleration to $4.6 trillion by mid-August 2026 is plausible, though it comes from a Dune Analytics community dashboard Adams himself has publicized, not an independent audit [^2][^3]. The volume claim is the least contestable part of the essay. The market-share claim is where things get complicated.

:::kv
- {term: "Historical analogy", def: "Index funds, mocked in 1976, now hold the majority of US fund assets"}
- {term: "Market-share claim", def: "DEX share of centralized spot volume: <1% to >20%"}
- {term: "Structure indictment", def: "Citadel Securities' $12.2B revenue reflects TradFi entrenchment"}
- {term: "Product roadmap", def: "Uniswap v4 hooks let LPs concentrate liquidity around correlated pairs"}
:::

## 02. Reality-checking the DEX-share numbers

**Thesis: "over 20%" describes a peak the market has already round-tripped through twice, not a floor.**

CoinGecko's own DEX-versus-CEX spot-volume tracker — a primary dataset, not a critic's cherry-pick — shows DEX share rising from 6.9% in January 2024 to a peak of 24.5% in June 2025, then falling back to 13.6% by January 2026 [^3]. The Block's separately-constructed ratio (top-30 DEXs by DeFiLlama volume, divided by a curated basket of major centralized exchanges) tells a similar volatility story from a different angle: a record 24.14% in July 2026, up from 17% twelve months earlier [^4]. Both readings support "DEX share has touched or exceeded 20%." Neither supports "DEX share is durably above 20%," because both series show it falling well below that line in between.

:::compare
- {role: LOWEST, name: "Jan 2024", value: "6.9%"}
- {role: HIGHEST, name: "Jun 2025 peak", value: "24.5%"}
- {role: SUBJECT, name: "Jan 2026 (latest)", value: "13.6%"}
:::

Part of the volatility has an identifiable, non-structural cause. PancakeSwap's June 2025 spike to 58% of all DEX activity — and a corresponding plunge in Uniswap's own share to 19.4%, briefly ceding the "largest DEX" title it has held for most of its history — traced to Binance's "Alpha 2.0" program mechanically routing its own retail order flow into PancakeSwap pools [^5]. That is a single centralized exchange redirecting its users into one AMM as a rewards gimmick, not the market migrating. The share reversed within seven months [^3][^5].

:::rank-list
- {label: "PancakeSwap - Jun 2025 peak", value: "64.5%", pct: 100}
- {label: "Uniswap - Jun 2025", value: "19.4%", pct: 30}
- {label: "Uniswap - Aug 2025", value: "35.9%", pct: 56, highlight: true}
- {label: "PancakeSwap - Aug 2025", value: "29.5%", pct: 46}
:::

A second confound: DEX volume composition splits sharply by chain and by asset class. Solana's DEX activity has been reported anywhere from 30% to 48% of total DEX market share in 2025, with memecoin trading estimated at 60-80% of that chain's DEX revenue at peak, and weekly Solana DEX volume once fell 62% in three weeks (from $118.2 billion to $44.5 billion) as one memecoin cycle ended [^41]. Ethereum and its L2s, by contrast, carry the larger institutional-size trades [^41]. A DEX/CEX ratio measured near a memecoin-volume peak — which several of the "record" readings coincide with — mechanically overstates the durable, structural share of trading that has actually migrated off centralized venues. What would falsify Adams's framing entirely: if DEX share settles at a materially lower steady state than 20% once the current tokenized-equity and memecoin cycles cool, the "under 1% to over 20%" line becomes a description of one good year, not a trend.

## 03. The Bogle analogy: a good story, missing a mechanism

**Thesis: index funds won because of a quantified, structural fee-and-performance gap; AMMs face a quantified, structural cost that pushes the opposite direction.**

The historical facts check out. Jack Bogle's 1976 Vanguard First Index Investment Trust was mocked as "Bogle's Folly" and raised just over $11 million against a target of $50-150 million — by Bogle's own account, an "abject failure" at launch [^6]. Fifty years later, index-based funds hold roughly 52-54% of US long-term fund assets, up from roughly 19% in 2010, per ICI Fact Book data [^7]. Adams is not wrong that the crowd mocked something that went on to dominate.

:::stats
- {label: "1976 index-fund raise", value: "$11M+", note: "vs. $50-150M target"}
- {label: "Passive share, 2010", value: "~19%"}
- {label: "Passive share, 2025", value: "~53%"}
- {label: "Active-vs-index fee gap", value: "~5x", note: "reported estimate"}
:::

But the mechanism that actually drove the shift is specific and well documented, not narrative: ==unverified: index funds reportedly average roughly 0.11% versus 0.59% for active funds (asset-weighted), and a widely-cited estimate puts active-fund underperformance near 88% over ten years== — precise figures this article could not pin to one primary SPIVA/Morningstar report, but directionally consistent with the well-established persistent fee gap and the empirical signature the Efficient Market Hypothesis predicts. Passive investors were not vindicated because the market changed its mind about a novel financial structure; they were vindicated by a slow, quantifiable compounding of costs that active managers, collectively, could not out-earn.

:::callout(kind=warn, label="The missing mechanism")
AMM liquidity provision carries a distinct, quantified structural cost with no index-fund analog: "loss-versus-rebalancing" (LVR). Because on-chain pool prices update only through trades, better-informed arbitrageurs systematically extract value from LPs whenever the true market price moves between blocks — a cost that scales with the *square* of volatility, so a pool needs roughly 10% of its value to turn over in daily volume just to break even on a typical fee tier [^9]. A passive index-fund holder faces no equivalent minimum-turnover requirement to avoid loss; they just hold. "The fund that makes no decisions wins" was literally true for Bogle's investors. It is not obviously true for a passive Uniswap LP, who is exposed to a real, model-able adverse-selection tax every single block.
:::

A direct empirical test of that gap: a 2021 study spanning 17 Uniswap v3 pools (43% of v3's total value locked at the time) found LPs collectively earned $199.3 million in fees but suffered $260.1 million in impermanent/divergence loss over the same window — a net loss of $60.8 million versus simply holding the underlying assets, with 49.5% of individual LPs net-negative [^10]. That data predates v4 and DualPool, but it is the closest thing to a direct measurement of whether "passive liquidity provision" has actually behaved like a passive index fund. So far, it has not.

## 04. Citadel Securities: entrenchment, or the price of risk?

**Thesis: the headline figures are real; the "entrenchment" interpretation is one reading among several equally supported by the same data.**

Independent reporting confirms Adams's numbers: Citadel Securities posted $12.2 billion in net trading revenue in 2025, a 25% increase over 2024's $9.7 billion record, ending the year with $21 billion in trading capital and $6.5 billion in EBITDA [^11]. That much is not in dispute.

:::stats
- {label: "2025 net trading revenue", value: "$12.2B", note: "+25% YoY"}
- {label: "Year-end trading capital", value: "$21B"}
- {label: "US retail equity share", value: ">35%", note: "self-reported"}
- {label: "US listed options share", value: "~30%"}
:::

What the essay leaves out: Citadel Securities' revenue-to-capital ratio, calculated from the same disclosed figures, has held roughly flat — about 0.61x in 2024, 0.58x in 2025 — rather than expanding, and its revenue fell 35% in the first half of 2023 versus the first half of 2022, during a lower-volatility stretch [^12]. That is the signature of a volatility-dependent risk-taking business, not a fixed toll extracted regardless of market conditions. Citadel Securities' self-reported >35% of retail order flow and ~30% of listed options volume is also a narrower claim than "dominates market-making" broadly, and competitors Jane Street and Hudson River Trading have both been reported gaining share since 2024 — a contested, not locked-in, position, not the picture of an unchallenged monopoly [^13].

:::quote(attr="Bradford Lynch and Robert Battalio, Wharton Research Spotlight, 2023")
More than 75% of orders routed to TD Ameritrade executed at the mid-price or better; only 25% of orders routed to Robinhood did — using the same wholesalers.
:::

That Wharton finding is the strongest evidence against treating "vertical integration" itself as the villain [^14]. If the same market-making firms deliver dramatically different execution quality depending on which broker routes the order, the problem Adams is pointing at is a specific contract-design and incentive failure between brokers and wholesalers — not an inherent property of bundling capital, strategy, and execution. It's a real problem. It's a different problem than the one the essay diagnoses, and it argues for better broker-wholesaler contract terms or disclosure rules, not necessarily for routing all order flow through an AMM instead.

## 05. Correlated pairs: a real mechanic, and a real fragility

**Thesis: liquidity genuinely does organize around correlated pairs — but the risk reduction holds only within the assumed correlation band, and Adams's own example asset pair sits outside a tight one.**

The underlying mechanic is not new or speculative — it is already the dominant pattern in DeFi. Curve Finance, the largest venue for correlated-pair trading, built its "StableSwap" bonding curve specifically to create a flat, low-slippage region near price parity for stablecoins and liquid-staking tokens like stETH/ETH and wBTC/BTC [^15][^16]. Within the amplification parameter's target range, impermanent loss on those pools is genuinely minimal [^15].

Outside that range, the same design amplifies losses precisely when the correlation assumption fails. Curve's stETH/ETH pool depegged in June 2022 after Three Arrows Capital and Celsius liquidations drained liquidity; pool TVL fell from $4.6 billion to about $621 million within weeks, and stETH separately traded as low as 0.9671 ETH against ETH during a later stress episode the same year [^15]. UST/LUNA — designed around its own correlated-pair peg mechanism — failed even more completely two weeks earlier, wiping out roughly $18 billion of UST and $40 billion of LUNA market value within days [^17].

:::timeline
- {date: "2022-05-13", headline: "UST/LUNA collapse", body: "Algorithmic peg mechanism fails; ~$18B UST and $40B LUNA wiped out within days."}
- {date: "2022-06", headline: "Curve stETH/ETH depeg", body: "3AC and Celsius liquidations drain the pool; TVL falls from $4.6B to ~$621M within weeks."}
:::

That history matters directly for Adams's forward-looking example: "NVDA/USD can become NVDA/SPY." NVDA's rolling 30-day correlation with the S&P 500 has ranged between 0.35 and 0.87 over the past year (averaging roughly 0.66) — a real but loose and time-varying relationship, not the tight peg that makes stablecoin or liquid-staking pools work [^18]. NVDA's beta versus the broader market is reported between 1.88 and 2.24 depending on vendor and lookback window — comfortably above 1.0, meaning a large share of NVDA's price movement is idiosyncratic and would not be hedged away by pairing against SPY [^19].

:::kv
- {term: "NVDA-SPY rolling 30-day correlation", def: "0.35 - 0.87 (avg. ~0.66)"}
- {term: "NVDA beta vs. market", def: "1.88 - 2.24 (vendor range)"}
:::

An LP in an NVDA/SPY pool would carry meaningfully more basis risk than an LP in a stETH/ETH pool — and Curve's own crisis response to the stETH/ETH depeg was to deploy a *second* pool with a much higher amplification parameter (1000 versus the original 50), because the standard correlated-pair curve failed to hold under stress [^15]. "Correlated pairs reduce LP risk" is conditional on curve design and correlation tightness holding up under stress, not a free, automatic property of pairing two assets that usually move together.

## 06. Uniswap v4 hooks and the DualPool reality check

**Thesis: the actual DualPool mechanism captures idle-capital yield, not cross-correlated-pair liquidity concentration — a real capital-efficiency improvement, but a different one than the essay implies.**

Uniswap v4's "hooks" are a genuine architectural advance: plugin smart contracts that customize pool behavior at defined points in the swap and liquidity lifecycle, replacing v3's fixed, one-size-fits-all pool logic [^20]. That customization layer sits alongside a separate v4 change — a singleton contract plus "flash accounting" — that Uniswap Labs estimates cuts gas costs for pool creation and multi-hop swaps by roughly 99%; the gas savings trace to that architectural redesign, not to hooks themselves [^20]. Both pieces of the roadmap claim hold up, correctly attributed.

DualPool specifically, however, does something different from what the essay implies. Live since July 22, 2026 and built with Spark, DualPool parks idle pool capital in ERC-4626 yield vaults between swaps; when a trade arrives, the hook atomically withdraws only the shortfall needed, deploys it as a concentrated liquidity position for the duration of that single swap, then redeposits the leftover funds back into the vault [^21]. Between swaps, a DualPool holds effectively zero liquidity in Uniswap's PoolManager. That is a genuinely clever idle-capital-yield mechanism — Spark's separate $150 million migration of stablecoin liquidity to Uniswap v4 is explicitly earmarked to eventually route through DualPool as its largest deployment, and OpenZeppelin's audit of the hook found no critical or high-severity issues [^21]. It is not the cross-correlated-pair liquidity concentration the essay describes; the trust assumption it introduces is vault-governance and vault-liquidity risk, not correlation risk [^21].

:::bars
- {label: "LP fees earned (2021 study)", value: "$199.3M", pct: 77}
- {label: "LP impermanent loss suffered", value: "$260.1M", pct: 100}
:::

That distinction matters because it means DualPool does not resolve the structural LP-economics problem documented in Section 03 — it optimizes idle-capital yield, which is a separate line item from the adverse-selection cost LVR describes. Uniswap Labs' own research found that JIT (just-in-time) liquidity — bots that add concentrated liquidity in the same block as a large swap purely to capture fees, then withdraw — was relatively rare (roughly 8,000 transactions between May 2021 and July 2022) [^43], but an independently documented single case still cut a regular LP's fee accrual from 0.17853 ETH to 0.02223 ETH in one block [^22]. Better hooks can route around specific extraction vectors. They have not yet been shown to flip the sign on the LVR-driven, volatility-scaled cost that is the deeper problem for "passive" AMM liquidity.

## 07. Robinhood Chain: the $33 million headline vs. what's underneath

**Thesis: the SPY-pair figure is real but small, sits atop a debt-wrapper with no shareholder rights, and most of Robinhood Chain's tokenized-stock DEX volume traces to a memecoin-collateral loop, not equity-investing demand.**

Robinhood Chain — an Arbitrum-tech-stack Ethereum L2 — went live July 1, 2026 [^23]. Its tokenized "Stock Tokens" are structured as 1:1-backed tokenized *debt securities*, issued by a Jersey special-purpose vehicle (Robinhood Assets (Jersey) Limited), and explicitly carry no voting or shareholder rights; the product is excluded from the US and US persons entirely [^23][^24]. Adams's headline figure — $33 million in volume from more than 11,000 traders in the first twelve days, on a single tokenized SPY pair [^1][^39] — traces to Uniswap's own dashboard of its own protocol's activity, not third-party verification; a separate, earlier Uniswap Labs post reports the much larger protocol-wide real-world-asset figures below, but does not itself contain the SPY-pair number [^25].

:::stats
- {label: "SPY-pair volume, 12 days", value: "$33M", note: "single pool, self-reported"}
- {label: "Protocol-wide RWA volume", value: "$9.1B+", note: "2.6M txns, 140k+ wallets"}
- {label: "Peak weekly active traders, whole chain", value: "20,000+", note: "week of Jul 20, 2026"}
- {label: "Uniswap share of RH Chain DEX liquidity", value: "~99%", note: "V4 ~73% + V3 ~26%"}
:::

Zoom out and the picture gets murkier, not clearer. Uniswap V3 and V4 combined control roughly 99% of tokenized-stock DEX liquidity on Robinhood Chain, meaning there is effectively no independent venue whose data could corroborate or contradict Adams's account of "the market" [^27] — a near-monopolist publishing an essay about the health of a market it almost entirely constitutes. More concretely: a large share of Robinhood Chain's tokenized-stock DEX volume has been traced to memecoins launched using stock tokens as their liquidity-pool collateral — a loop where speculative memecoin trading mechanically generates stock-token volume as a byproduct, not because traders are seeking equity exposure via a SPY pair [^26]. Robinhood Chain's daily active tokenized-stock traders peaked above 20,000 in the week of July 20, 2026 — a larger number than Adams's 11,000, but measuring a different thing (whole-chain daily-active peak, not one pair's 12-day cumulative trader count) and plausibly inflated by the same memecoin-collateral loop [^26].

:::callout(kind=warn, label="Counterparty risk the essay doesn't address")
Robinhood's tokenized stocks route through a three-layer custody chain — US broker-dealer to Jersey issuer to on-chain token — and holders have no direct legal claim on the underlying share, only a debt claim on the Jersey entity. That is a real, disclosed structural risk that a genuine equity holding does not carry, and it is separate from and additional to the smart-contract and liquidity risks discussed above.
:::

## 08. The incumbents are not standing still

**Thesis: DTCC, Nasdaq, and NYSE's parent are building their own tokenization rails under direct SEC permission — the opposite of the disintermediation the essay implies.**

If tokenization were quietly routing around the SEC, DTCC, and the exchanges, none of those institutions would need to build their own tokenized-settlement products. They are doing exactly that. DTCC — custodian of $114 trillion in securities and processor of $4.7 quadrillion in transactions in 2025 — is running production pilot trades of its own tokenization platform since July 2026 under an SEC No-Action Letter, with more than 50 participating firms including BlackRock, Goldman Sachs, and JPMorgan, targeting a full commercial launch in October 2026 [^28]. Nasdaq's tokenized-securities rule change, approved by the SEC on March 18, 2026, requires tokenized shares to remain fungible with, share the same CUSIP and ticker as, and carry identical shareholder rights to the underlying share — settled through DTC, not any AMM [^29]. NYSE's parent, ICE, formed a 50-50 joint venture with OKX in June 2026 to put NYSE-listed stocks on-chain for roughly 120 million crypto traders, pending SEC and CFTC approval [^30].

:::timeline
- {date: "2025-12-11", headline: "DTCC SEC No-Action Letter", body: "Regulator clears DTCC's own tokenized-settlement pilot program."}
- {date: "2026-01-28", headline: "SEC staff statement", body: "Existing securities law applies fully to tokenized securities; no new exemption is created."}
- {date: "2026-03-18", headline: "Nasdaq tokenization approved", body: "SEC approves a rule change requiring full share-rights parity and DTC-mediated settlement."}
- {date: "2026-06-23", headline: "ICE-OKX joint venture", body: "NYSE's parent forms a 50-50 JV with OKX targeting ~120M crypto traders, pending approval."}
- {date: "2026-07", headline: "DTCC production pilot", body: "50+ firms including BlackRock, Goldman Sachs, JPMorgan begin live pilot trades."}
:::

The regulatory backdrop reinforces the same point. The SEC's January 28, 2026 joint staff statement holds that federal securities laws apply to tokenized securities in substantially the same way as traditional securities regardless of format, and explicitly creates no new exemption or safe harbor [^31]. SEC Chair Paul Atkins has repeatedly signaled a forthcoming "innovation exemption" that would allow limited AMM-style trading of tokenized securities; as of the most recent public remarks reviewed, it remained unissued. Reporting on its likely scope is contested: some coverage describes it as cabined and time-limited with voting and dividend rights excluded, while other reporting and SEC commissioners' own public remarks suggest the draft could preserve full rights parity — the shape of the exemption is not yet settled [^32]. Separate legal analysis concludes that intermediaries facilitating secondary tokenized-securities trades remain subject to the same broker-dealer, exchange, and transfer-agent registration requirements as in traditional markets, with best-execution obligations flagged as "a particular challenge given the current fragmentation" [^33]. None of that is disintermediation. It's incumbents building tokenization on their own terms, under a regulator that has been explicit that the format of a security does not change which laws apply to it.

## 09. Who actually benefits if Adams is right

**Thesis: Uniswap's own financial position — a collapsing TVL, a UNI token well off its highs, and a freshly activated fee-burn mechanism — complicates the "pure unbundling, no rent-seeking" framing the essay offers.**

Uniswap's total value locked fell to about $3.31 billion by March 2026 and roughly $3.42 billion by May 2026 — well below trackers' reports of a prior-year peak above $6 billion — tracking a broader DeFi-wide contraction, even as combined V2/V3/V4 trading volume reportedly held up comparatively well into mid-2026 [^37][^38]. That volume-resilience-amid-TVL-collapse pattern is exactly the metric an interested party would emphasize as proof that usage is decoupling from locked capital. It is also consistent with a less flattering read: LPs becoming more capital-efficient out of necessity as the underlying token prices in TVL depreciated.

:::line-chart(title="Uniswap total value locked, Aug 2025-May 2026", subtitle="DeFiLlama, $ billions", y-unit=$)
x: 2025-08,2026-03,2026-05
TVL: 6.3,3.31,3.42
:::

In December 2025, Uniswap's DAO activated a long-dormant protocol fee switch through a "UNIfication" vote — redirecting one-quarter to one-sixth of LP fees, plus Unichain sequencer and MEV-auction proceeds, into a UNI burn mechanism, including a one-time retroactive burn of 100 million UNI (worth roughly $600 million at vote-time prices) and a 20-million-UNI-per-year treasury budget for Uniswap Labs starting January 2026 [^35][^36]. That is value accrual through token scarcity rather than a cash dividend, but it is still Uniswap extracting a cut of trading activity for the benefit of UNI holders — a structure not obviously less "bundled" than the capital-strategy-execution stack the essay criticizes, just bundled differently and with Adams himself as a major beneficiary.

:::stats
- {label: "UNI price, essay date", value: "$3.25", note: "mkt cap ~$2.03B"}
- {label: "UNI price, Jan 2026", value: "~$5.30-5.85", note: "range across trackers"}
- {label: "SEC investigation", value: "Closed, no action", note: "Feb 2025"}
- {label: "CFTC settlement", value: "$175,000", note: "Sep 2024"}
:::

On the regulatory side, Uniswap Labs' own record is genuinely mixed in Adams's favor: the SEC closed its multi-year investigation into Uniswap Labs with no enforcement action in February 2025, after previously issuing a Wells Notice alleging unregistered exchange and broker/clearing activity [^40]; separately, Uniswap Labs settled with the CFTC for a reduced $175,000 penalty in September 2024 over unregistered leveraged retail transactions, with two of five CFTC commissioners publicly dissenting as regulatory overreach [^42]. A federal court also fully dismissed a private class action (*Risley v. Universal Navigation Inc.*) alleging Uniswap's interface facilitated fraudulent-token trading, holding that Uniswap's developers are not "statutory sellers" under securities law [^44]. Those are real, favorable data points for the "AMMs carry less legal tail-risk than a centralized bundler" argument — and they are also direct financial benefits to Adams personally, as founder and large UNI holder, not neutral legal footnotes.

## 10. What would have to be true - and the counter-argument

**Thesis: Adams's forecast is falsifiable on specific, trackable margins, and the current evidence sits closer to "plausible eventually" than "already happening."**

For the essay's central prediction to be vindicated, several things would need to hold that the evidence in this piece does not yet show: DEX share of spot volume would need to settle at a durable level above 20% once the current tokenized-equity and memecoin cycles cool, rather than continuing to round-trip between roughly 14% and 25% [^3][^4]; the SEC's still-unissued "innovation exemption" would need to grant AMMs genuine access to full-rights tokenized equities, not the narrower, rights-stripped version some reporting anticipates [^32]; and Uniswap-style pools would need to show LP economics turning durably net-positive at scale, resolving the LVR-driven drag that a direct 2021 measurement found erased LP fee income entirely [^9][^10].

The counter-case is that incumbents retain effective control of the rails that matter — DTCC still runs settlement, Nasdaq's approved tokenization path preserves full shareholder rights and exchange oversight, and the SEC has been explicit that a security's format does not change which laws bind it [^28][^29][^31] — while the AMM-native alternative currently thriving on Robinhood Chain does so by stripping shareholder rights, routing through a Jersey debt wrapper, and drawing a meaningful share of its reported volume from a memecoin-collateral loop rather than organic equity demand [^24][^26]. Both paths could plausibly coexist for years without either "winning" in the way the essay's Bogle analogy implies a single structure eventually will.

Why this matters beyond one founder's essay: billions of dollars in capital allocation and at least three live SEC rulemakings are being shaped right now by exactly this narrative — that tokenization plus AMMs represents an inevitable, index-fund-style disintermediation of legacy market structure. The mechanism-level evidence assembled here doesn't say that's wrong. It says the mechanism is not yet proven, the headline statistics describe a peak more often than a plateau, and the person making the case has a direct financial stake in which version of the story the market believes.

:::references
- {id: 1, title: "Essay on AMMs, index funds, and tokenized markets", url: "https://x.com/haydenzadams/status/2089531754004554215", source: "Hayden Adams via X", date: "2026-08-18"}
- {id: 2, title: "Uniswap protocol surpasses $4 trillion in total trading volume", url: "https://phemex.com/news/article/uniswap-protocol-surpasses-4-trillion-in-total-trading-volume-41375", source: "Phemex", date: "2025-12-02"}
- {id: 3, title: "CEX vs. DEX Trading Activity Report 2026", url: "https://www.coingecko.com/research/publications/cex-dex-trading-activity-report-2026", source: "CoinGecko Research", date: "2026-03-03"}
- {id: 4, title: "DEXs capture record spot crypto trading as CEX volumes sink", url: "https://www.theblock.co/news/defi/2026-08-03-dexs-capture-record-spot-crypto-trading-as-cex-volumes-sink-410476", source: "The Block", date: "2026-08-03"}
- {id: 5, title: "Decentralized crypto exchanges market share", url: "https://www.coingecko.com/research/publications/decentralized-crypto-exchanges-market-share", source: "CoinGecko Research", date: "2025-08-01"}
- {id: 6, title: "50 years, 50 facts: indexing since 1976", url: "https://corporate.vanguard.com/content/corporatesite/us/en/corp/articles/50-years-50-facts-indexing-since-1976.html", source: "Vanguard", date: "2026"}
- {id: 7, title: "Index fund share of US long-term fund assets", url: "https://finance.biggo.com/news/7c39a4f7-f301-483c-aa82-8b5d5e7d1827", source: "ICI Fact Book data, via BiGGo", date: "2025"}
- {id: 8, title: "Active vs. index fund fee gap and SPIVA underperformance", url: "https://www.morningstar.com", source: "Morningstar / S&P SPIVA", date: "2025"}
- {id: 9, title: "Automated Market Making and Loss-Versus-Rebalancing", url: "https://arxiv.org/abs/2208.06046", source: "arXiv (Milionis, Moallemi, Roughgarden, Zhang)", date: "2022-08"}
- {id: 10, title: "Impermanent Loss in Uniswap v3", url: "https://arxiv.org/abs/2111.09192", source: "arXiv", date: "2021-11-17"}
- {id: 11, title: "Citadel Securities nets record $12 billion trading haul in 2025", url: "https://www.bloomberg.com/news/articles/2026-03-24/citadel-securities-nets-record-12-billion-trading-haul-in-2025", source: "Bloomberg", date: "2026-03-24"}
- {id: 12, title: "Griffin's Citadel Securities reports record $9.7bn trading revenue", url: "https://www.hedgeweek.com/griffins-citadel-securities-reports-record-9-7bn-trading-revenue/", source: "Hedgeweek", date: "2025-03"}
- {id: 13, title: "What We Do: Options", url: "https://www.citadelsecurities.com/what-we-do/options/", source: "Citadel Securities", date: "2026"}
- {id: 14, title: "Research Spotlight: Payment for Order Flow and Price Improvement", url: "https://wffi.wharton.upenn.edu/uncategorized/research-spotlight-payment-for-order-flow-and-price-improvement/", source: "Wharton Financial Institutions Center", date: "2023"}
- {id: 15, title: "stETH depegs as whale pulls $101M ETH from Curve Finance", url: "https://beincrypto.com/steth-depegs-whale-pulls-101m-eth-curve-finance/", source: "BeInCrypto", date: "2022-06"}
- {id: 16, title: "The TerraUSD (UST) and Luna crash", url: "https://www.richmondfed.org/publications/research/economic_brief/2022/eb_22-24", source: "Federal Reserve Bank of Richmond", date: "2022-05"}
- {id: 17, title: "NVDA vs. SPY comparison", url: "https://www.gale.finance/compare/nvda-vs-spy/", source: "Gale Finance", date: "2026"}
- {id: 18, title: "NVIDIA (NVDA) Beta", url: "https://www.gurufocus.com/term/beta/NVDA", source: "GuruFocus", date: "2026-08-14"}
- {id: 19, title: "Our Vision for Uniswap v4", url: "https://blog.uniswap.org/uniswap-v4", source: "Uniswap Labs", date: "2023"}
- {id: 20, title: "Our Vision for Uniswap v4", url: "https://blog.uniswap.org/uniswap-v4", source: "Uniswap Labs", date: "2023"}
- {id: 21, title: "DualPool hook is now live", url: "https://blog.uniswap.org/dualpool-hook-is-now-live", source: "Uniswap Labs", date: "2026-07-22"}
- {id: 22, title: "Quantifying just-in-time liquidity in Uniswap v3", url: "https://medium.com/coinmonks/quantifyng-just-in-time-liquidity-in-uniswap-v3-23ac1db729c5", source: "Medium / CoinMonks", date: "2022"}
- {id: 23, title: "Robinhood Chain goes live on mainnet", url: "https://www.theblock.co/news/business/2026-07-01-robinhood-chain-goes-live-mainnet-alongside-24-7-tokenized-stocks-lighter-perps-planned-crypto-agentic-trading-406918", source: "The Block", date: "2026-07-01"}
- {id: 24, title: "Robinhood tokenized stocks: the on-chain custody catch", url: "https://ryder.id/blogs/post/robinhood-tokenized-stocks-the-on-chain-custody-catch", source: "ryder.id", date: "2026-07"}
- {id: 25, title: "Tokenized securities are live", url: "https://blog.uniswap.org/tokenized-securities-are-live", source: "Uniswap Labs", date: "2026-06-12"}
- {id: 26, title: "Robinhood Chain tops Solana in tokenized stock volume via memecoin pairs", url: "https://thedefiant.io/news/blockchains/robinhood-chain-tops-solana-in-tokenized-stock-volume-via-memecoin-pairs", source: "The Defiant", date: "2026-07-28"}
- {id: 27, title: "Uniswap v4 dominates Robinhood Chain tokenized stocks", url: "https://cryptobriefing.com/uniswap-v4-dominates-robinhood-chain-tokenized-stocks/", source: "Crypto Briefing", date: "2026-07"}
- {id: 28, title: "DTCC advances development of new tokenization service", url: "https://www.dtcc.com/news/2026/may/04/dtcc-advances-development-of-new-tokenization-service", source: "DTCC", date: "2026-05-04"}
- {id: 29, title: "SEC approves Nasdaq's move to allow tokenized securities trading", url: "https://www.coindesk.com/policy/2026/03/18/sec-approves-nasdaq-s-move-to-allow-tokenized-securities-trading", source: "CoinDesk", date: "2026-03-18"}
- {id: 30, title: "NYSE parent ICE and OKX form joint venture to put tokenized stocks on blockchain", url: "https://www.techtimes.com/articles/318915/20260623/nyse-parent-ice-okx-form-joint-venture-put-tokenized-stocks-blockchain.htm", source: "Tech Times", date: "2026-06-23"}
- {id: 31, title: "SEC clarifies federal securities law treatment of tokenized securities", url: "https://www.morganlewis.com/pubs/2026/02/sec-clarifies-federal-securities-law-treatment-of-tokenized-securities", source: "Morgan Lewis", date: "2026-02"}
- {id: 32, title: "SEC's Peirce, Atkins detail incremental path for tokenized securities", url: "https://www.theblock.co/post/390544/secs-peirce-atkins-incremental-path-tokenized-securities-agency-readies-innovation-exemption", source: "The Block", date: "2026"}
- {id: 33, title: "Tokenized Securities", url: "https://www.skadden.com/insights/publications/2026/04/tokenized-securities", source: "Skadden, Arps, Slate, Meagher & Flom", date: "2026-04"}
- {id: 34, title: "Accelerated Settlement", url: "https://www.dtcc.com/accelerated-settlement", source: "DTCC", date: "2026-05"}
- {id: 35, title: "UNIfication", url: "https://blog.uniswap.org/unification", source: "Uniswap Labs", date: "2025-11-10"}
- {id: 36, title: "Uniswap DAO to activate fee switch and burn 100M UNI tokens", url: "https://www.dlnews.com/articles/defi/uniswap-dao-to-activate-fee-switch-and-burn-100m-uni-tokens/", source: "DL News", date: "2025-12-26"}
- {id: 37, title: "Uniswap protocol page", url: "https://defillama.com/protocol/uniswap", source: "DeFiLlama", date: "2026-05"}
- {id: 38, title: "Uniswap Statistics", url: "https://coinlaw.io/uniswap-statistics/", source: "CoinLaw", date: "2026-06"}
- {id: 39, title: "Uniswap founder Hayden Adams on AMMs and tokenized markets", url: "https://www.cryptopolitan.com/uniswap-hayden-adams-amm-tokenized-markets/", source: "Cryptopolitan", date: "2026-08-18"}
- {id: 40, title: "A win for DeFi", url: "https://blog.uniswap.org/a-win-for-defi", source: "Uniswap Labs", date: "2025-02-25"}
- {id: 41, title: "CEX vs. DEX Trading Activity Report 2026 (perps and Solana data)", url: "https://www.coingecko.com/research/publications/cex-dex-trading-activity-report-2026", source: "CoinGecko Research", date: "2026-03-03"}
- {id: 42, title: "CFTC orders Uniswap Labs to pay $175,000 penalty", url: "https://www.cftc.gov/PressRoom/PressReleases/8961-24", source: "CFTC", date: "2024-09-04"}
- {id: 43, title: "JIT liquidity on Uniswap v3", url: "https://blog.uniswap.org/jit-liquidity", source: "Uniswap Labs", date: "2022"}
- {id: 44, title: "Scam token case against Uniswap dismissed with prejudice", url: "https://www.coindesk.com/policy/2026/03/03/scam-token-case-against-uniswap-dismissed-with-prejudice-by-u-s-district-judge-in-nyc", source: "CoinDesk", date: "2026-03-03"}
:::
