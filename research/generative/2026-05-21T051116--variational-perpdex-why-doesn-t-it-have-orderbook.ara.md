---
eyebrow: REPORT · DEFI MARKET STRUCTURE
title: Why Variational's Perp DEX Has No Order Book
deck: A request-for-quote protocol, one in-house liquidity provider, and a $50M bet that breadth beats depth.
domain: crypto
lede: |
  Almost every serious derivatives venue ever built — the CME, Binance,
  dYdX, and the on-chain juggernaut Hyperliquid — is organized around a
  central limit order book. Variational, which raised a $50M Series A
  led by Dragonfly on 2026-05-20, deliberately threw the order book out.
  Its retail app, Omni, runs 450+ perpetual markets, has cleared
  $200B+ in cumulative volume, and quotes every trade through a single
  in-house liquidity provider at zero fees. The question is not whether
  this is unusual. It is: why would two ex-Genesis derivatives traders
  conclude that the default market structure of modern finance is the
  wrong primitive — and what are they betting that it buys them?
stats:
  - {label: Series A, value: $50M, note: "Dragonfly-led, May 2026"}
  - {label: Cumulative volume, value: $200B+, note: self-reported}
  - {label: Live markets, value: 450+, note: "peak 1,000+"}
  - {label: Trading fees, value: 0%, note: spread-funded}
---

## 01. The question: a perps venue that skips the order book

The order book is so deeply identified with "an exchange" that its absence reads as a missing feature. Variational treats it as a design choice. The protocol's own documentation states the position bluntly: "Variational is a request-for-quote (RFQ) protocol, and does not utilize an orderbook."[^1] In an RFQ system, takers request quotes and makers respond with bids and offers — a quote-driven market, not the order-driven matching of a CLOB.[^1]

That choice is not naïveté about how exchanges work. Co-founders Lucas Schuermann and Edward Yu built and sold a quantitative hedge fund (Qu Capital), then ran engineering and quantitative research, respectively, at Genesis — one of crypto's largest OTC desks and market makers — before leaving in 2021 to start Variational.[^42,15] They have spent more than a decade inside the machinery of derivatives market-making. The decision to skip the order book comes from that experience, not despite it.

:::kv
- {term: Founded, def: 2021 (founders ex-Genesis OTC desk)}
- {term: Chain, def: "Arbitrum One (general-purpose L2)"}
- {term: Flagship app, def: "Omni — retail permissionless perps"}
- {term: Market structure, def: "RFQ (request-for-quote), no order book"}
- {term: Counterparty, def: "OLP — one in-house liquidity provider"}
- {term: Fees, def: "0% (revenue from bid-ask spread)"}
- {term: Total raised, def: "~$61.8M across seed, strategic, Series A"}
:::

The company's trajectory is short and steep. A $10.3M seed co-led by Bain Capital Crypto and Peak XV Partners (formerly Sequoia India) landed in October 2024, with Coinbase Ventures, Dragonfly, North Island, and HackVC participating.[^15,16] A $1.5M strategic round followed in June 2025.[^17] Then the $50M Series A, again led by Dragonfly, with Bain and Coinbase returning, announced on 2026-05-20 and explicitly earmarked to "go all in on RWAs."[^13,41] By that point Omni had grown from a private beta to hundreds of live markets and a self-reported $200B+ in lifetime volume.[^14,18]

:::timeline
- {date: 2017, headline: "Qu Capital founded", body: "Schuermann and Yu launch a quant trading firm; later acquired by Genesis."}
- {date: 2021, headline: "Variational founded", body: "Founders leave the Genesis OTC desk to build a peer-to-peer derivatives protocol."}
- {date: 2024-10, headline: "$10.3M seed", body: "Co-led by Bain Capital Crypto and Peak XV; Coinbase Ventures, Dragonfly, HackVC join."}
- {date: 2025-01, headline: "Omni private beta", body: "RFQ perps app goes live on Arbitrum with the OLP as sole counterparty."}
- {date: 2025-06, headline: "$1.5M strategic round", body: ">$100M cumulative volume; OLP vault reports 87% annualized yield."}
- {date: 2025-10, headline: "First $1B day", body: "Single-day volume tops $1B; market count peaks above 1,000 listings."}
- {date: 2025-12, headline: "Omni Points launch", body: "3,000,000 points distributed retroactively ahead of a future $VAR token."}
- {date: 2026-05, headline: "$50M Series A", body: "Dragonfly-led raise to push into real-world-asset perps; RWA Phase 1 goes live."}
:::

This piece reasons from first principles through five layers: the mechanics of an order-book-free trade, the structural reasons on-chain order books are hard, the counter-example of Hyperliquid (which makes the order book work), the single-liquidity-provider design that is both the source of the model's elegance and its biggest risk, and the deeper claim — that Variational is building a clearinghouse, not an exchange, with real-world assets as the end-game. The thesis only holds if breadth beats depth. The closing section stress-tests exactly that.

## 02. How a trade actually works without a book

On a CLOB, a taker hits resting limit orders posted by makers at discrete price levels. On Omni there are no resting orders to hit. The flow is a request and a reply.[^1] A user fills out an order form — say, buy 1 ETH at 50x leverage. The Omni Liquidity Provider (OLP), as the only eligible maker on Omni, returns a quote consisting of a single executable price. The user accepts, OLP performs a final "last look" risk check, collateral moves from the OLP vault and the user into a shared settlement pool, and the position is booked and cleared.[^1] From the trader's seat it feels like any perps UI: enter size, see a price, click. The entire round trip completes in seconds.[^1]

The settlement pool is the load-bearing primitive. It is an isolated on-chain escrow holding the open positions, both sides' USDC collateral, and the rules governing margin and liquidation; every pool is "completely isolated from each other," so one pool's bankruptcy cannot contaminate another.[^3] This bilateral, per-counterparty escrow is the on-chain analogue of how OTC derivatives are cleared between two parties — and it is fundamentally incompatible with a single shared order book, where many anonymous participants net into one fungible queue.

The rest of the mechanics are conventional, which is the point — none of them require an order book:

| Mechanic | How Omni does it | Why it needs no book |
|---|---|---|
| Margin | Portfolio or simple mode; engine is Deribit-compatible; maintenance margin is half the initial requirement | Risk is computed per settlement pool, bilaterally |
| Liquidation | Triggered when maintenance-margin usage hits 100%; position force-closed against OLP at quote price plus a 0.5% penalty | The counterparty (OLP) is always known and present |
| Mark/index price | Variational oracle streams a weighted multi-venue price, used for margin, liquidation, and unrealized PnL | Reference price is imported, not discovered locally |
| Execution price | OLP shows an indicative quote, then a "firm quote" on click | Price is quoted on demand, not rested at levels |

Two facts in that table do real work. First, the executable price is whatever OLP quotes — there is no public price formation happening inside Omni.[^6] Second, the mark and index prices come from an oracle that weights external venues.[^6] Omni borrows its price from the wider market and competes on execution, spread, and breadth instead. That is a deliberate inversion of what an order book is for, and it sets up every argument that follows.

## 03. Why on-chain order books are hard

Start from the physics. A competitive order book is a machine for absorbing and cancelling quotes at microsecond cadence; professional makers update orders thousands of times per second as conditions move. General-purpose blockchains run orders of magnitude slower. Ethereum produces a block roughly every 12 seconds; even an optimized L2 like Arbitrum, the chain Variational runs on, is far faster but still far slower than the microsecond cadence competitive makers run at.[^30] Posting and cancelling a limit order every block — and paying gas each time — makes high-frequency market-making structurally uneconomic on a public chain.

Then add adversarial transparency. A public on-chain order book and mempool expose order flow to anyone watching. The canonical result here is Daian et al.'s "Flash Boys 2.0," which documented bots running priority gas auctions to front-run and sandwich ordinary DEX trades — extracting what the paper named miner-extractable value.[^27] A maker who must broadcast quotes into that environment is quoting into a minefield; the people best positioned to pick off stale quotes are exactly the people watching the chain.

Finally, the cold-start problem. An order book needs dedicated maker depth at every price level of every market. Bootstrapping that depth per market is expensive, and it gets ruinous for long-tail or newly listed assets — which is why so much of DeFi's perp history is a sequence of attempts to route around the on-chain book entirely.

| Era | Architecture | Representative venue | What it traded away |
|---|---|---|---|
| 2020 | Virtual AMM (vAMM) | Perpetual Protocol v1 | Real liquidity; synthetic pricing only |
| 2021 | Oracle-priced peer-to-pool | GMX | Price discovery; LPs are the house[^29] |
| 2021–23 | Off-chain book, on-chain settle | dYdX v3, Aevo | On-chain matching; trust in an off-chain engine |
| 2023 | App-chain CLOB | dYdX v4 | Validators hold an in-memory book off-chain[^28] |
| 2024 | On-chain CLOB on a bespoke L1 | Hyperliquid | The general-purpose chain itself |
| 2024–26 | On-chain RFQ | Variational | The order book — for imported quotes |

Academic work has formalized this same taxonomy of perpetual-DEX designs — vAMM, oracle-pricing, and order-book models — confirming that the field's architectural diversity is a series of deliberate responses to the order book's on-chain limits, not an accident.[^31] Variational's RFQ sits at the end of that arc as the most explicit rejection: don't rebuild the book on-chain, and don't simulate it with a pool either — quote against liquidity that already exists somewhere else.

## 04. The order book that won: Hyperliquid

The convenient story — "order books don't work on-chain" — is false, and the cleanest disproof is the most successful perp DEX in the world. Hyperliquid runs a fully on-chain central limit order book in which "every order, cancel, trade, and liquidation happens transparently with one-block finality."[^25] Its documentation is pointed about it: "HyperCore does not rely on the crutch of off-chain order books."[^24] And it is fast: mainnet "currently supports approximately 200k orders/sec," with end-to-end latency of "median 0.2 seconds and 99th percentile 0.9 seconds" for a co-located client.[^24] The result is dominance — on the order of $4.5T in cumulative volume and roughly $9.4B in open interest, capturing the large majority of on-chain perpetuals flow.[^26]

:::rank-list
- {label: Hyperliquid, value: "~70% on-chain perps", pct: 100, highlight: false}
- {label: "Aster / Lighter (CLOB)", value: "next tier", pct: 34}
- {label: "GMX / Jupiter (pool)", value: "mid tier", pct: 14}
- {label: "Variational (RFQ)", value: "long-tail leader", pct: 9, highlight: true}
:::

But look at what Hyperliquid had to do. It did not run its order book on a general-purpose chain — it left Arbitrum and built an entire purpose-built L1, with its own HyperBFT consensus and validator set, optimized from first principles for matching.[^25] And the cost reappears in a familiar form: research found traders co-located near Hyperliquid's validators in Tokyo enjoy a ~200-millisecond latency edge — a CEX-style speed arms race, reconstituted on-chain.[^43] So the rigorous lesson is narrower than the slogan: you can run a CLOB on-chain, but only by abandoning the general-purpose chain and rebuilding the stack beneath it.

:::stats
- {label: Throughput, value: 200k, unit: "ord/s"}
- {label: Median latency, value: "0.2", unit: s}
- {label: On-chain perps share, value: "~70%"}
- {label: Built on, value: "bespoke L1"}
:::

Variational chose to stay on a general-purpose L2 and reach for RFQ instead — and its founders frame the relationship to Hyperliquid not as competition but as dependency. Schuermann told Fortune: "We don't view Hyperliquid as a direct competitor, or exchanges in general, for that matter. We actually rely on them."[^13] He compares Variational to a brokerage — Robinhood, not Nasdaq — that sources liquidity from venues rather than hosting its own book, and points to "a 100x gap or more between liquidity that's on Hyperliquid and traditional finance sources like say trading on the CME" as the real prize.[^13] If you believe that framing, the order book was never the thing to compete on.

## 05. One market maker to rule them all: the OLP

Here is the crux, and the catch. Because Omni has no order book, it needs a counterparty for every trade — and that counterparty is a single entity, the Omni Liquidity Provider. The docs describe it as "a vertically integrated market maker that acts as the counterparty to all trades on Omni," composed of a vault, a market-making engine, and a risk-management system, running "the same market making engine that the Variational founders have been using and improving for over 7 years."[^2] OLP quotes every market, hedges its accumulated exposure on external venues with its own capital, and never moves user funds off-platform.[^2]

This is what makes zero fees possible. "Since all market making on Omni is done by OLP instead of external market makers, Omni doesn't need fees to generate revenue"; OLP earns the bid-ask spread, and the protocol skims 20% of that spread into its treasury.[^2] It is, structurally, payment-for-order-flow turned inside out: instead of paying external makers subsidies to rest depth, the venue internalizes the market-making and keeps the spread. Schuermann's framing is that this lets the platform "share the PnL with retail" rather than leak it to outside firms.[^21] And it is the engine of breadth — a new listing needs only "a reliable price feed, a quoting strategy, and a hedging mechanism," all built in-house, which is how Omni reaches ~500 markets without bootstrapping a book for each.[^2]

The OLP vault has reportedly thrown off eye-watering yields on a small base — 87% annualized at the time of the June 2025 round, and triple-digit figures during 2025 — but those numbers ride a tiny early treasury and are unaudited.[^17,37] The vault's yield trajectory has cooled as assets grew {sparkline:300,150,87,80}, and the vault remains team-funded; the docs say only that "once the system's stability is proven over time," the team intends "to open it up to user deposits via a community vault."[^2] As of the Series A it had not.

:::callout(kind=danger, label="Concentration risk")
The docs are unusually candid about the downside: "there is a risk that OLP loses money," and if OLP were insolvent, "any unrealized or realized PnL accrued going forward would be considered 'bad debt,' and would not be able to be paid out to the user."[^2] There is no mutualized insurance fund across pools. A CLOB spreads counterparty and inventory risk across many independent makers; Omni concentrates it in one balance sheet. Trade size is therefore capped by OLP's TVL (~$100M), a ceiling no order book has.[^18,38]
:::

Variational positions OLP as a novel hybrid — "the first vault that simultaneously runs a sophisticated market making strategy and is the only counterparty," in contrast to Hyperliquid's HLP (sophisticated but not the sole counterparty) and Jupiter's JLP (sole counterparty but a passive AMM).[^2] That is a fair description of the innovation. It is also a precise description of the centralization: one closed, proprietary, currently-private engine sitting on the other side of every trade.

## 06. RFQ vs CLOB: the real trade-offs

Strip away the crypto framing and this is an old debate. Equities trade on lit, continuous order books. But swaps, corporate bonds, FX blocks, and options blocks have always traded primarily RFQ, dealer-to-client — not for lack of technology, but because of the shape of the instruments. US regulation even codifies it: under the CFTC's swap-execution-facility rules, a request for a quote must be sent to "no less than three market participants."[^32] And the BIS has found that even in the most electronified mandated-clearing swap markets, "the majority of swap trading still occurs in response to an RFQ, rather than via a CLOB."[^33] Derivatives gravitate to quote-driven structure. Variational is porting that default on-chain.

The honest scorecard cuts both ways:

| Dimension | CLOB | RFQ (Omni's single-maker form) |
|---|---|---|
| Price discovery | Forms price; transparent and continuous | Imports a reference price; is a price-taker[^6] |
| Capital efficiency | Resting orders lock capital at every level | Liquidity quoted on demand[^2] |
| Long-tail markets | Needs maker depth per market | One engine quotes ~500 markets[^2] |
| Information leakage | Resting orders are public; front-runnable on-chain[^27] | Quote is private to the request |
| Adverse selection | Flow is anonymous | Maker can profile and quote you specifically[^34] |
| Best execution | Verifiable best price in the book | Trust the single maker's spread[^40] |

The cons are not hypothetical, and the sharpest critics are not cranks. In the run-up to a public "order books vs RFQ for RWAs" debate between Lighter and Variational on The Chopping Block,[^35] analyst David Jeong argued the structural weakness directly: with RFQ "it is easier to segment each quote and based on your 'trader profile,' RFQ makers can provide much more granular quotes to adversely select /just you/" — adding that "the reason why tradfi funds use CLOBs over RFQ has to do with information leakage."[^34] A single-maker RFQ has no competitive quote tension and no on-chain-verifiable best execution; as one widely-shared critique put it, "a bad RFQ system is just opacity with a nice UI. Zero fees can simply mean the fee is hidden in the spread."[^40] Another flagged that on Omni "different traders will get different prices," because one market maker sets and adapts every spread.[^44]

Variational's defense is twofold. RFQ lets OLP refuse toxic flow it can identify — a protection the team claims is "impossible on an orderbook platform"[^20] — and the protocol's institutional tier, Variational Pro, is a genuine multi-dealer RFQ where a taker sees competing quotes from several market makers and picks the best.[^11] That mitigant is real, but it lands on Pro, which is not yet live; on the retail Omni product, the single OLP is the whole market.[^11,2]

## 07. It's a clearinghouse, not an exchange

The deepest reason there is no order book is that Variational does not think of itself as an exchange. Its docs say so directly: "Variational is not an exchange; it is a peer-to-peer trading protocol."[^9] The protocol is "a collection of on and off-chain infrastructure designed to automate the process of booking, clearing, and settling derivatives trades."[^10] Omni — retail perps, single OLP — is just the first app on top of it; Pro is the second.[^10,11] The order-book question is really a question about what layer you are looking at.

A clearinghouse for arbitrary bilateral derivatives cannot use a single price-time-priority book, because the contracts are not fungible. On Variational, "almost every aspect of the trading, clearing, and settlement process is customizable. Terms are decided before any trade is done and agreed upon by both parties as part of the quote," and "positions are not fungible between pools."[^11,3] You cannot rest a bespoke, custom-margined, custom-expiry contract on the same book as someone else's differently-termed contract — there is nothing to match against. RFQ plus per-pool settlement is the natural primitive for generalized derivatives: options, futures, perps, and structured products, each negotiated and cleared bilaterally.

This is the founders' actual background showing through. Variational's own documentation narrates the legacy institutional workflow it is automating — negotiate an ISDA agreement, complete KYC, request a quote from a dealer over Telegram, transfer collateral manually, field manual margin calls.[^11] That is how OTC derivatives clear: bilaterally, by request, with credit and collateral managed between two named parties — the model TradFi reserves central order books and clearinghouses for only the most standardized contracts. Two people who ran an OTC desk built the on-chain version of an OTC desk.

| Layer | What it is | Counterparty | Status |
|---|---|---|---|
| *Variational protocol* | Booking, clearing, settling derivatives bilaterally | Any whitelisted maker | Live |
| Omni | Retail perps app, simplified single-maker RFQ | OLP only | Live |
| Pro | Institutional multi-dealer RFQ for custom structures | Competing market makers | Not yet live |

The single-maker critique, then, is correctly scoped: it is a property of the Omni app, not of the architecture. Whether Pro's multi-dealer competition actually materializes — and pulls institutional flow — is one of the open questions on which the whole thesis rests.

## 08. The RWA end-game

The Series A reframed everything. Variational is, in its own words, going "all in on RWAs" — real-world assets — and it argues the order book is uniquely unfit for them.[^41] The company's manifesto, titled "CLOBs Are a Mistake for RWAs," makes the case at full volume: traditional finance dwarfs on-chain derivatives by orders of magnitude, and "every CLOB platform is sucking RWA liquidity through a straw."[^20] Schuermann's compression of the argument: "Order books have a cold start problem. They're not porting liquidity, they're rebuilding liquidity."[^13]

The empirical anchor is a benchmark of Hyperliquid's on-chain oil market against CME's WTI. At ±2bp depth, CME showed roughly $19M of resting depth versus the on-chain market's ~$152k — about 1%. Slippage on a $1M trade ran roughly 20x worse on-chain.[^36] And because the on-chain market trades through the weekend while CME is closed, it must absorb any gap in the underlying alone — exactly when imported liquidity is thinnest. An order book that must rebuild commodity liquidity from scratch, one contract at a time, cannot match a dealer network plugged into the venue where that liquidity already lives — which is exactly the gap RFQ aggregation is built to span.

:::compare
- {role: LOWEST, name: "CME WTI ($1M trade)", value: "0.79 bp"}
- {role: HIGHEST, name: "On-chain oil ($1M trade)", value: "15.4 bp"}
- {role: SUBJECT, name: "On-chain oil ($1M trade)", value: "15.4 bp"}
:::

The no-order-book design is what lets Omni out-list everyone. Because OLP imports and quotes rather than bootstraps, Omni already carries more perpetual markets than the order-book leaders — the clearest signal of the breadth-over-depth bet.[^18,7]

:::bars
- {label: "Omni (Variational, RFQ)", value: "450+", pct: 100}
- {label: "Hyperliquid (CLOB)", value: "~343", pct: 73}
- {label: "Lighter (CLOB)", value: "~175", pct: 37}
- {label: "dYdX v4 (CLOB)", value: "~119", pct: 25}
:::

Phase 1 of the RWA rollout is already live — gold, silver, copper, oil, and equity indices, traded from a single USDC cross-margined account at up to 50x leverage with zero fees, 24/7 — with 100+ TradFi markets promised for summer 2026.[^41,20] The regulatory posture fits the design: trades are peer-to-peer and non-custodial, funds sit in segregated on-chain settlement pools, and Omni is opening "to the public in select jurisdictions" rather than everywhere at once.[^9,13]

:::callout(kind=warn, label="The other edge of the sword")
The same weekend-gap event that indicts on-chain order books also indicts on-chain RWAs generally: a perp that trades 24/7 on an underlying that closes on weekends carries gap risk no quoting model fully removes, and an RFQ that imports a reference price is only as good as that feed when the source market is shut. Offering commodity and equity perps to retail also sits squarely inside CFTC jurisdiction — peer-to-peer self-custody changes the custody surface, not the fact that perpetuals are regulated derivatives. The breadth bet and the regulatory bet are the same bet.
:::

## 09. What could break the thesis

The strongest case against Variational is not that the order book is sacred — it is that the model's bets are unproven and its risks are concentrated. Five ways it could be wrong:

First, the order book may simply be good enough, even for RWAs. Hyperliquid disproves the slogan that CLOBs fail on-chain, and nothing stops it — or Lighter, or a CME-backed entrant — from listing the same real-world assets and out-executing a single-maker RFQ on the names that matter. A CLOB can serve RWAs too; the Castle Labs benchmark shows today's gap, not a permanent law.[^36]

Second, the single OLP is a genuine point of failure. Depth is capped by one vault's TVL, there is no shared insurance fund, and the docs themselves concede OLP can lose money and leave traders with uncollectable "bad debt."[^2,38] One analyst called the structure "a massive centralization bet... tail risk spikes if that LP or infra ever cracks."[^39] The elegance and the fragility are the same fact.

Third, the price-discovery critique is structural, not cosmetic. An RFQ that imports its reference price contributes nothing to price formation and free-rides on the venues it quotes against; a single maker that can profile each taker can adversely select them in ways an anonymous book cannot.[^34,40] "Trust the spread" is a weaker promise than "verify the book."

Fourth, the breadth bet has not yet translated into volume leadership. Most-listed is not most-traded: on-chain perp volumes cooled sharply from their late-2025 peak, and by daily volume Variational sits well behind Hyperliquid, Aster, and Lighter.[^45] Leading on market count and open interest while trailing on volume is a coherent niche — but it is a niche, not yet the disruption the manifesto promises.

Fifth, the regulatory perimeter is load-bearing and untested. The whole RWA push depends on offering leveraged commodity and equity exposure to retail through an offshore, geofenced, self-custodial structure — a posture that works until a regulator decides it does not.

A red-team pass against the three load-bearing claims — that Variational has no order book by design, that one OLP is the sole Omni counterparty, and that it raised $50M to pursue RWAs — found no contradicting evidence; all three are confirmed by first-party docs, the protocol's own statements, and on-record reporting.[^1,2,13] The claims are solid. What remains contestable is not the facts but the wager built on them: that in on-chain derivatives, the venue connected to the deepest existing liquidity beats the venue with the best order book. Variational has $61.8M and a decade of OTC instinct riding on the answer being yes.

:::references
- {id: 1, title: "Trading via RFQ", url: "https://docs.variational.io/variational-protocol/key-concepts/trading-via-rfq", source: Variational Docs}
- {id: 2, title: "The Omni Liquidity Provider (OLP)", url: "https://docs.variational.io/omni/the-omni-liquidity-provider-olp", source: Variational Docs}
- {id: 3, title: "Settlement Pools", url: "https://docs.variational.io/variational-protocol/key-concepts/settlement-pools", source: Variational Docs}
- {id: 4, title: "Margin (Omni)", url: "https://docs.variational.io/omni/trading/margin", source: Variational Docs}
- {id: 5, title: "Liquidation (Omni)", url: "https://docs.variational.io/omni/trading/liquidation", source: Variational Docs}
- {id: 6, title: "Quoted, Index & Mark Prices", url: "https://docs.variational.io/omni/trading/quoted-index-and-mark-prices", source: Variational Docs}
- {id: 7, title: "About Omni", url: "https://docs.variational.io/omni/about-omni", source: Variational Docs}
- {id: 8, title: "Why Build Variational", url: "https://docs.variational.io/getting-started/why-build-variational", source: Variational Docs}
- {id: 9, title: "Peer-to-Peer Trading Protocol vs DEX", url: "https://docs.variational.io/variational-protocol/key-concepts/p2p-trading-protocol-vs-dex", source: Variational Docs}
- {id: 10, title: "Variational Protocol Overview", url: "https://docs.variational.io/variational-protocol/overview", source: Variational Docs}
- {id: 11, title: "About Pro", url: "https://docs.variational.io/pro/about-pro", source: Variational Docs}
- {id: 12, title: "Omni Points / Rewards", url: "https://docs.variational.io/omni/rewards/points", source: Variational Docs}
- {id: 13, title: "Variational raises $50 million Series A", url: "https://fortune.com/2026/05/20/variational-raises-50-million-series-a/", source: Fortune, date: "2026-05-20"}
- {id: 14, title: "Variational raises $50M from Dragonfly", url: "https://cryptobriefing.com/variational-50m-series-a-dragonfly-capital/", source: CryptoBriefing, date: "2026-05-20"}
- {id: 15, title: "Variational secures $10.3M seed (Bain, Peak XV)", url: "https://cryptoslate.com/press-releases/variational-secures-10-3-million-in-seed-funding-to-expand-peer-to-peer-trading-protocol-led-by-bain-capital-crypto-and-peak-xv-partners-fka-sequoia-india/", source: CryptoSlate, date: "2024-10-23"}
- {id: 16, title: "Arbitrum-based Variational raises $10.3M seed", url: "https://www.theblock.co/post/322653/arbitrum-crypto-protocol-variational-funding", source: The Block, date: "2024-10-23"}
- {id: 17, title: "Variational announces $1.5M strategic round", url: "https://chainwire.org/2025/06/04/variational-announces-1-5-million-strategic-round-and-launches-referral-program/", source: Chainwire, date: "2025-06-04"}
- {id: 18, title: "How Variational Omni Powers a Perpetual Futures DEX", url: "https://www.coingecko.com/learn/variational-case-study", source: CoinGecko, date: "2026-04-21"}
- {id: 19, title: "How Variational is Reinventing Derivatives Onchain", url: "https://blog.arbitrum.io/how-variational-is-reinventing-derivatives-onchain-with-arbitrum/", source: Arbitrum, date: "2025-08-28"}
- {id: 20, title: "CLOBs Are a Mistake for RWAs", url: "https://x.com/variational_io/status/2049857522358464823", source: "Variational (X)", date: "2026-04-30"}
- {id: 21, title: "RFQ, not order books — share PnL with retail", url: "https://x.com/variational_lvs/status/2009613816125137345", source: "Lucas Schuermann (X)", date: "2026-01-09"}
- {id: 22, title: "RWA order books bootstrap from scratch", url: "https://x.com/variational_lvs/status/2049867143337132204", source: "Lucas Schuermann (X)", date: "2026-04-30"}
- {id: 23, title: "RFQ is global liquidity aggregation", url: "https://x.com/mr_plumpkin/status/2009094737710784591", source: "Edward Yu (X)", date: "2026-01-08"}
- {id: 24, title: "HyperCore Overview (200k ord/s, 0.2s latency)", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/overview", source: Hyperliquid Docs}
- {id: 25, title: "About Hyperliquid (on-chain order books)", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/about-hyperliquid", source: Hyperliquid Docs}
- {id: 26, title: "Hyperliquid — volume & open interest", url: "https://defillama.com/protocol/hyperliquid", source: DefiLlama}
- {id: 27, title: "Flash Boys 2.0: Frontrunning, MEV & PGAs", url: "https://arxiv.org/abs/1904.05234", source: "Daian et al. (arXiv)", date: "2019-04-10"}
- {id: 28, title: "dYdX v4 Technical Architecture Overview", url: "https://www.dydx.xyz/blog/v4-technical-architecture-overview", source: dYdX}
- {id: 29, title: "GMX Documentation (peer-to-pool)", url: "https://docs.gmx.io/docs/intro", source: GMX Docs}
- {id: 30, title: "Arbitrum block numbers and time (250ms)", url: "https://docs.arbitrum.io/build-decentralized-apps/arbitrum-vs-ethereum/block-numbers-and-time", source: Arbitrum Docs}
- {id: 31, title: "Architecture of perpetual futures DEXes (taxonomy)", url: "https://arxiv.org/abs/2402.03953", source: "Chen, Ma & Nie (arXiv)", date: "2024-02-06"}
- {id: 32, title: "17 CFR 37.9 — RFQ to at least three participants", url: "https://www.law.cornell.edu/cfr/text/17/37.9", source: "CFTC / Cornell LII"}
- {id: 33, title: "Electronic trading in fixed income markets", url: "https://www.bis.org/publ/mktc07.pdf", source: "BIS Markets Committee", date: "2016-01"}
- {id: 34, title: "RFQ adverse selection / trader profiling", url: "https://x.com/davidyjeong/status/2057298088356893147", source: "David Y. Jeong (X)", date: "2026-05-21"}
- {id: 35, title: "Lighter vs Variational: order books vs RFQ debate", url: "https://x.com/hosseeb/status/2057181792747114540", source: "Haseeb Qureshi (X)", date: "2026-05-20"}
- {id: 36, title: "432 Hours of the Hyperliquid Oil Market", url: "https://research.castlelabs.io/p/432-hours-of-hyperliquid-oil-market", source: Castle Labs, date: "2026-03"}
- {id: 37, title: "Variational first $1B day; OLP yield", url: "https://www.gate.com/news/detail/15062265", source: Gate News, date: "2025-10-20"}
- {id: 38, title: "Depth limited by OLP's TVL", url: "https://x.com/yh_0x/status/2050133745274061117", source: "yh_0x (X)", date: "2026-05-01"}
- {id: 39, title: "Single-OLP centralization bet / tail risk", url: "https://x.com/position_xbt/status/2057171539674722375", source: "position_xbt (X)", date: "2026-05-20"}
- {id: 40, title: "A bad RFQ system is opacity with a nice UI", url: "https://x.com/Rencrypta/status/2051791919450349608", source: "Rencrypta (X)", date: "2026-05-05"}
- {id: 41, title: "Variational Series A — going all in on RWAs", url: "https://x.com/variational_io/status/2057097346086047982", source: "Variational (X)", date: "2026-05-20"}
- {id: 42, title: "Core Contributors (founders, Genesis OTC)", url: "https://docs.variational.io/getting-started/core-contributors", source: Variational Docs}
- {id: 43, title: "Hyperliquid traders in Tokyo get 200ms edge", url: "https://www.coindesk.com/markets/2026/03/30/hyperliquid-traders-in-tokyo-get-200-millisecond-edge-glassnode-research-shows", source: CoinDesk, date: "2026-03-30"}
- {id: 44, title: "On Omni different traders get different prices", url: "https://x.com/denko0x/status/2049508446542639566", source: "denko0x (X)", date: "2026-04-29"}
- {id: 45, title: "Onchain perp DEX volumes decline", url: "https://cointelegraph.com/news/onchain-perp-dex-volumes-decline-hyperliquid-share", source: Cointelegraph, date: "2026-04"}
:::
