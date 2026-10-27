---
eyebrow: RESEARCH · HYPERLIQUID MARKET DATA
title: "Sixty milliseconds for $49: what a faster Hyperliquid book feed fixes, and what it cannot"
deck: A Hong Kong quant says Quicknode's gRPC feed cut his stale-book problem and that structure matters more than speed. The mechanics support the second claim more than the first.
lede: |
  On 2026-10-27 a Hyperliquid-focused quant, @UST_mean, posted production latency numbers for his Tokyo-hosted cross-exchange arbitrage bot: moving from Hyperliquid's public WebSocket to Quicknode's gRPC stream cut median book latency from 236 ms to 176 ms, p90 from 346 ms to 211 ms, and frames older than one second from 2.05% to 0.02%.[^1] He paid $49 a month, and closed by saying traders should find the structure before talking about speed.[^1] This article tests the pieces: why the public feed is stale, what 60 ms is worth in basis points, what the cheaper and dearer alternatives cost, and whether execution latency, not data latency, is the clock that actually binds.
stats:
  - {label: Median latency, value: "236 → 176", unit: ms, note: "tweet, public WS → gRPC"}
  - {label: p90 latency, value: "346 → 211", unit: ms}
  - {label: Frames over 1 s, value: "2.05% → 0.02%"}
  - {label: Build plan, value: $49, unit: "/mo", note: 80M credits}
---

:::callout(kind=info, label="Direct answer")
- **Is the gain real?** Plausible, not proven. One author, one workload, no stated method; a vendor benchmark of a different Dwellir product shows a similar ~50 ms median gain.[^1,12]
- **Is it worth $49?** For a bot that reads books to price taker orders, almost certainly, because the cost is small against the tail-frame fix. For a bot whose losses come from elsewhere, no.
- **What 60 ms is worth:** about 0.17 bp of one-sigma Bitcoin drift at current implied volatility, against the 2–8 bp p90 slippage he reports.[^1,18] The median gain cannot explain the slippage; the elimination of 1-second frames is closer to relevant.
- **Bigger clock:** Hyperliquid order-to-fill took a median 884 ms in Glassnode's Tokyo test, so the data feed is not the binding latency.[^6]
- **His closing line holds up:** fee tier, funding mechanics and venue structure move costs by amounts the feed cannot.[^14,15]
:::

## 01. What the tweet claims, and what can be checked

**Thesis: the tweet is a clean, falsifiable field report, but everything quantitative in it is single-source.**

The post, dated 2026-10-27 07:43 UTC, is from an account describing itself as a Hyperliquid maximalist and quant trader, based in Hong Kong with roughly 1,500 followers.[^22] It makes five testable claims. The author sees p90 slippage of 2–8 bp in cross-exchange arbitrage and traced it to stale order-book data at order time.[^1] His server is in Tokyo and the public WebSocket was still slow, with a median of 236 ms, p90 346 ms, and about 2% of frames over a second.[^1] Switching to Quicknode's gRPC feed gave 176 ms, 211 ms and 0.02%.[^1] Subscribing only to best bid/offer for about 20 coins fit the $49 Build plan with 80M credits.[^1] And running his own node would be faster but cost about $1,000 a month.[^1]

:::note
Access caveat. The birdy CLI had no configured accounts in this run, so the tweet was read through the public fxtwitter mirror, which returns a summary rather than the verbatim Chinese text; figures above are as that mirror reported them.[^22] The same mirror lists no attached media.[^22]
:::

:::stats
- {label: Tweet likes, value: 92, note: "as of 2026-10-27"}
- {label: Bookmarks, value: 131, note: "as of 2026-10-27"}
- {label: Views, value: "6,323", note: "as of 2026-10-27"}
:::

What we cannot check from the post is the method. It does not say which public subscription was used (`l2Book`, `l2Book` with `fast`, or `bbo`), how "latency" was defined (receipt time minus the exchange `time` stamp, or something else), how the clocks were synchronised, or how many frames the percentiles cover.[^1] Those omissions matter for reasons the next section makes concrete.

**Counterpoint.** A practitioner reporting his own production telemetry is better evidence than a vendor chart, and the numbers are internally coherent: p90 improves by more than the median, and the tail collapses, which is the signature of removing a throttled or queued path rather than shaving transit time.

**Why it matters.** The rest of the article takes the numbers as given and asks what they imply, rather than whether the author is honest.

## 02. Why the public feed is stale: the mechanics

**Thesis: Hyperliquid's public book feeds are throttled by design, and the 2026 changes move them further from what an automated trader needs.**

Hyperliquid's own documentation says `l2Book` is "pushed on each block that is at least 0.5 since last push," and that `bbo` is sent only if the best bid or offer changes on a block.[^3] The `fast` option trades depth for cadence: 5 levels versus 20, at a 0.5 s cadence.[^2,3] In June 2026 Hyperliquid's core team announced that several public feeds would push less often after the next upgrade, then softened it on June 11: default `l2Book` becomes 20 levels every 2 seconds with a later move to 5 seconds, `l2Book` with `fast: true` stays 5 levels every 0.5 seconds, `allMids` every 5 seconds.[^2] The team's guidance, as Quicknode quotes it, was explicit about who the public feed is for.[^2]

:::quote(attr="Hyperliquid core team, as quoted by Quicknode, 2026-06-12")
Automated traders should run a non-validating node for more levels or real time update streams.
:::

Two facts from this explain a 236 ms median. First, if the author consumed `l2Book` with `fast: true`, a 0.5 s push floor means an update's age at a random instant is uniform between 0 and 0.5 s, so the median age from the throttle alone is 250 ms before any network delay (ARA calculation from the documented cadence).[^2,3] That is the same order as his 236 ms, which suggests cadence rather than the network path may dominate his "before" number, though the tweet does not say which feed he used.[^1] Second, the HyperCore chain produces blocks at about 12 per second, roughly one per 83 ms, so a per-block stream's own sampling age averages tens of milliseconds, not hundreds.[^13]

gRPC changes the delivery model rather than the pipe. Quicknode's `StreamL2Book` sends a full aggregated snapshot every block, `StreamBboBook` emits only when the best bid/offer changes, and `StreamL2BookDiff` adds sequence numbers, none of which exist on the public WebSocket.[^2,7] Its documentation example shows each update carrying a block number and an apparently millisecond-resolution timestamp, which is what a latency measurement would be computed from.[^8]

:::timeline
- {date: 2026-01-20, headline: "Quicknode HyperCore public beta", body: "gRPC and streams on paid plans."}
- {date: 2026-03, headline: "Glassnode Tokyo fill test", body: "Median order-to-fill 884 ms across 120 orders."}
- {date: 2026-06-09, headline: "Hyperliquid announces slower public feeds", body: "Reported by Quicknode."}
- {date: 2026-06-11, headline: "Rollout softened", body: "Default l2Book to 20 levels / 2 s; fast stays 0.5 s."}
- {date: 2026-10-27, headline: "Tweet", body: "236 → 176 ms median reported."}
:::

**Counterpoint.** I found no primary confirmation that the slower cadence is live in production as of this article; the Quicknode post describes it as coming "after the next network upgrade," and the official docs page I read still shows the `fast` flag and 0.5 s language without dates.[^2,3] The tweet's "before" baseline may therefore be either regime.

**Why it matters.** If the baseline is a throttled snapshot feed, the gain from gRPC is largely a change of data model (event-driven versus sampled), and it will widen if Hyperliquid slows the public feeds further.

## 03. The measured gain, and a second data point

**Thesis: the reported improvement is about 60 ms at the median and 135 ms at p90, and the tail collapse is the bigger story.**

The arithmetic on the tweet's own figures is straightforward. The median fell by 60 ms, or 25.4%. The p90 fell by 135 ms, more than twice as much, and the share of frames older than one second fell from 2.05% to 0.02%, a factor of roughly 100 (ARA calculation from the reported figures; the 0.02% is rounded, so the ratio is imprecise).[^1]

:::slope(left-label="Public WS", right-label="Quicknode gRPC", unit=" ms")
| Statistic | Public WS | Quicknode gRPC |
|-----------|-----------|----------------|
| Median (p50) | 236 | 176 |
| p90 | 346 | 211 |
:::

:::bar-chart(title="Share of frames older than 1 second", subtitle="Tweet, production, Tokyo server", orientation=horizontal, value-suffix=%)
categories: Public WebSocket, Quicknode gRPC
Frames over 1 s: 2.05, 0.02
:::

An independent-looking cross-check exists, but it is a vendor's. Quicknode's early-2026 comparison reports Dwellir's order-book server cutting median latency by 24.1% versus the public feed across 2,662 trades.[^12] Dwellir's own docs put that at a 263 ms public-API median against 212 ms on its WebSocket, a 51 ms gain; the "24%" is the ratio of the two (263/212), while the same gain is 19% of the public figure.[^23] The convergence of two unrelated products on a gain of roughly 50–60 ms and 24–25% is suggestive that something systematic, such as the public feed's cadence, is being removed. It is not independent confirmation: both are self-reported by vendors, and the comparison does not say who ran the Dwellir test.[^12]

**Counterpoint.** Quicknode's blog describes its docs as claiming "sub-millisecond latency" for gRPC market data, a figure that is plainly not what the author measured (176 ms median).[^2] The gap is explained by what is being measured: vendor figures describe delivery after their node has the block, while a trader's number includes consensus-to-node propagation, the node's processing, and transit to Tokyo. Treat any vendor "sub-millisecond" figure as irrelevant to end-to-end freshness.

**Why it matters.** A trader should size the purchase on the p90 and tail rows, not the median, because adverse selection concentrates in the stale frames.

## 04. What 60 ms is worth in basis points

**Thesis: at BTC-like volatility, the median gain is worth a fraction of a basis point; the tail frames and the execution leg are larger.**

Price drift over a stale interval scales with the square root of time. Using Deribit's DVOL, which stood at 38.28 on 2026-10-20 (realized 14-day volatility 20.2%), a driftless random walk has a one-standard-deviation move of about 0.17 bp over 60 ms and 0.68 bp over one second (ARA calculation).[^18] Those are BTC numbers; drift is linear in volatility, so a more volatile coin sees proportionally more, and the tweet does not say which coins the bot trades.[^1]

:::bar-chart(title="One-sigma BTC price drift by stale interval", subtitle="DVOL 38.3% annualized, driftless random walk (ARA calculation)", orientation=horizontal, value-suffix=" bp")
categories: 60 ms (median gain), 884 ms (median fill), 1000 ms (stale frame)
One-sigma drift: 0.17, 0.64, 0.68
:::

Set that beside the fee schedule. Hyperliquid's base perps tier charges 0.045% taker (4.5 bp) and 0.015% maker, falling to 0.024% taker at the top volume tier above $7B of 14-day volume.[^14] The tweet's reported p90 slippage of 2–8 bp is the same order as a taker fee, and the gap between the base and top taker tiers (4.5 versus 2.4 bp) is larger than the whole drift cost of a median stale frame.[^1,14]

:::bars
- {label: "Tier 0 taker (< $5M)", value: "4.5 bp", pct: 100}
- {label: "Tier 1 taker (> $5M)", value: "4.0 bp", pct: 89}
- {label: "Tier 2 taker (> $25M)", value: "3.5 bp", pct: 78}
- {label: "Tier 3 taker (> $100M)", value: "3.0 bp", pct: 67}
- {label: "Tier 4 taker (> $500M)", value: "2.8 bp", pct: 62}
- {label: "Tier 5 taker (> $2B)", value: "2.6 bp", pct: 58}
- {label: "Tier 6 taker (> $7B)", value: "2.4 bp", pct: 53}
:::

The inference: on a diffusive-drift model, a p90 of 2–8 bp cannot be mostly stale-quote drift on a BTC-like asset, because a median stale frame is worth a fifth of a basis point and even a one-second frame under one. The p90 is probably dominated by thin books on less liquid coins, the size of the order relative to displayed depth, and adverse selection (quotes that are stale precisely when the market has moved against them). The feed fix addresses only the last, and only in the tail. That is a hypothesis from the arithmetic, not a measurement; the author's trade-level data would settle it.

**Counterpoint.** Adverse selection is not random drift, and diffusion understates it: a market-maker write-up on crypto price discovery describes arbitrageurs spamming immediate-or-cancel orders at stale liquidity right after a move on a faster venue, so the cost arrives as discrete jumps in a few moments, not as smooth drift.[^24] A stale quote is more likely to be a bad quote when the market has just moved, because that is when fast participants pick it off. The academic evidence on equities puts latency arbitrage at about one-third of effective spread and price impact, a roughly 0.5 bp tax on trading, with the typical race lasting 5–10 microseconds, which shows the cost is concentrated in the few instants when information is asymmetric, not spread evenly over time.[^16]

**Why it matters.** Optimise the feed to remove rare, expensive stale frames; do not expect it to shrink average slippage by the headline 25%.

## 05. The cost ladder: $49, a node, or a vendor

**Thesis: the $49 plan is cheap relative to alternatives, but its credit metering means the 20-coin claim depends on update rates the docs do not publish.**

Quicknode's Build plan is $49 a month ($42 annual) with 80M API credits, 50 requests per second, and $0.62 per additional million credits.[^9] HyperCore gRPC requires Build or higher.[^7] Metering depends on stream: core streams cost 10 credits per 0.1 MB, order book streams 10 credits per 0.0165 MB, and `StreamBboBook` 10 credits per 0.00165 MB, a tenfold-cheaper unit than L2 because top-of-book messages are small.[^7]

On the arithmetic: 80M credits at 10 credits per 0.00165 MB is 13,200 MB of BBO data a month, or a sustained 5.1 KB/s over a 30-day month (ARA calculation).[^7,9] The docs do not publish a BBO message size; at an assumed 100 bytes per update, that is about 51 updates per second across all subscribed coins, against a theoretical ceiling of 240 per second if all 20 coins changed at every one of about 12 blocks per second (ARA calculation; the 100-byte figure is an assumption).[^7,13] Real top-of-book changes are sparser than every block, so 20 coins at $49 is plausible, as the author reports, but a more active set of coins or a bigger stream such as L2 would exhaust 80M credits and bill overage at $0.62 per million.[^1,9]

The alternatives, mostly from a vendor-written comparison dated March 2026:

:::rank-list
- {label: "Hydromancer Starter (L4)", value: "$300/mo", pct: 26}
- {label: "Self-run non-validator, AWS Tokyo compute only (ARA calculation)", value: "$888/mo", pct: 77}
- {label: "Tweet's estimate for own node", value: "~$1,000/mo", pct: 87}
- {label: "Dwellir dedicated node", value: "$1,150/mo", pct: 100}
- {label: "Quicknode Build", value: "$49/mo", pct: 4, highlight: true}
:::

Self-hosting is not just a rent line. Hyperliquid's node README specifies 16 vCPU, 128 GB RAM and a 500 GB SSD for a non-validator on Ubuntu 24.04, notes about 100 GB of logs per day by default, and recommends Tokyo for lowest latency.[^10] The closest AWS shape in Tokyo, an r6i.4xlarge, is $1.216 per hour on-demand, about $888 per month for compute alone before storage and egress (ARA calculation from a third-party price aggregator).[^11] The validator spec is larger, 32 vCPU, 128 GB and 1 TB, and Hyperliquid's docs treat running either kind of node as permissionless, with setup deferred to that repository.[^10,19,20] A node also produces order-status and book-diff files only when started with the relevant flags, and the README warns that raw book diffs and order statuses are large.[^10]

**Counterpoint.** Dwellir's dedicated node at $1,150 includes JSON-RPC, gRPC and order-book unmetered, and Hydromancer lists tiers from $300 to $2,500 a month, so a high-volume trader may be cheaper on a flat-rate plan than on metered credits.[^12] The comparison is also a Quicknode marketing document and contains internal inconsistencies, such as differing provider counts.[^12]

**Why it matters.** The marginal decision is not $49 versus $1,000. It is whether the metering fits your subscription set; the price jump to the next tier is $249.[^9,12]

## 06. The execution leg is the bigger clock

**Thesis: no private data provider can speed up order placement, and order-to-fill latency dwarfs the feed gain.**

Quicknode's comparison states plainly that order placement and cancellation cannot go through any private provider and use the public Hyperliquid API.[^12] Glassnode measured that path in March 2026 by placing 120 real market orders from AWS Tokyo: a median order-to-fill of 884 ms, range 695–1,634 ms, of which about 5 ms was network and about 879 ms processing (an estimate).[^6] Hyperliquid's documentation claims a co-located median of 0.2 s and a p99 of 0.9 s for end-to-end latency.[^5] Glassnode's figure is about four times the documented median; it suggests that growth to over 200,000 orders per second and 24 active validators may be a cause (Hyperliquid's docs put the active set at the top 27 by stake), but the explanation is Glassnode's, not demonstrated.[^6,20]

Set against that, the 60 ms median gain is about 6.8% of the median fill time (ARA calculation from two sources taken seven months apart).[^1,6] Put differently, between the moment the bot reads the book and the moment its order fills, roughly 884 ms elapses in which the displayed book can move, on the same one-sigma BTC calculation worth about 0.64 bp.[^6,18] A faster feed shrinks only the first leg of a round trip dominated by the second.

:::kv
- {term: "Feed gain (median)", def: "60 ms — from tweet"}
- {term: "Documented e2e median", def: "200 ms, p99 900 ms — Hyperliquid docs"}
- {term: "Measured order-to-fill", def: "884 ms median, 695–1,634 ms range, n=120 — Glassnode, March 2026"}
- {term: "Network share of fill", def: "~5 ms — Glassnode"}
- {term: "Implication", def: "Server-side processing and queueing, not distance, set the fill clock"}
:::

**Counterpoint.** The Glassnode test is one session sample of 120 orders, measures a market-order round trip rather than limit-order placement, and predates the tweet by seven months.[^6] Whether his cancel/replace cadence is dominated by data staleness or by acknowledgement latency is not stated in the tweet.[^1]

**Why it matters.** If the strategy resubmits on every refreshed quote, a faster feed raises message rate against an unchanged acknowledgement clock. The public API allows 2,000 messages per minute across all connections and, for address-based limits, one request per USDC traded after a 10,000-request buffer, so a faster feed can run into rate limits before it runs into profit.[^4]

## 07. Structure first: fees, funding and the speed race

**Thesis: the author's closing advice matches the economics. Costs set by fee tiers, funding design and venue rules shift outcomes by more than a 60 ms feed, while speed advantages decay as competitors buy the same service.**

Three structural levers are visible in the primary documents. Fee tier: the spread between base and top taker rates is 2.1 bp on every taker fill, available to anyone with enough volume, not to the fastest.[^14] Funding: Hyperliquid settles funding every hour at one eighth of the computed 8-hour rate, samples the premium every 5 seconds, fixes the interest component at 0.01% per 8 hours, caps funding at 4% per hour, and charges on oracle rather than mark price.[^15] These are design facts about the venue, and any difference from another venue's funding interval or formula is a recurring, forecastable spread rather than a race. The author names exactly this class of difference, across exchanges, DEXs, funding rates and pricing rules, as the source of opportunity.[^1] I did not verify the other venues' funding mechanics for this article, so the size of the cross-venue edge is outside what is evidenced here.

The speed side of the argument has academic support. Budish, Cramton and Shim documented that correlations between near-identical instruments (ES futures and the SPY ETF) break down at millisecond horizons, creating mechanical arbitrage; competition raised the speed required to capture it without shrinking the opportunity, the signature of an arms race.[^17] Their remedy, frequent batch auctions run roughly every tenth of a second, is a structural change to market design rather than a speed upgrade.[^17] Aquilina, Budish and O'Neill later measured the prize: races were about 20% of volume in their UK equity sample, six firms took over 80% of wins and losses, and the races were won in microseconds.[^16] A $49 feed does not compete in that league; it removes self-inflicted staleness. Everyone can buy it, so by the arms-race logic it is table stakes rather than an edge.[^16,17]

:::stack-bar(legend=true)
- {label: "Race wins+losses: top 6 firms", pct: 80}
- {label: "All other firms", pct: 20}
:::

:::note
Aquilina–Budish–O'Neill figures are from UK equity data (message-level exchange data), not crypto perpetuals; they illustrate how concentrated speed rents are when speed is the whole game, not the size of any rent on Hyperliquid.[^16]
:::

**Counterpoint.** "Structure before speed" can itself be an excuse. Structural spreads such as funding differentials are visible to everyone with an API, and capacity is limited; if they are crowded, execution quality (the thing speed buys) becomes the residual source of edge. The tweet's own closing admits he is still searching for the structure.[^1]

**Why it matters.** Spend the first dollar on the lever with the biggest, least competed effect: fee tier and venue design. Spend on the feed only after measuring that stale frames, not impact, are the loss.

## 08. What could break the thesis

**Thesis: three things would overturn the reading here: a different baseline feed, a different loss mechanism, or a throttled-credit surprise.**

1. **The baseline.** If the author used `bbo` rather than `l2Book`, the 0.5 s cadence argument disappears and the 60 ms gain must come from node proximity and push semantics, a different mechanism with a different ceiling.[^3,1] If the slower public cadence announced in June has since shipped, a rerun of the same test would show a larger gain.[^2]
2. **The loss mechanism.** If trade-level data show that the 2–8 bp p90 is mostly market impact on thin coins, then feed speed is nearly irrelevant and sizing or venue selection is the fix. The arithmetic in section 04 points that way for BTC-like volatility but is silent on small caps.[^18]
3. **The metering.** If a larger coin set or L2 depth is needed, the cost rises from $49 toward the $249 tier, or to a flat-rate node, which erases the cost advantage.[^9,12]
4. **Measurement drift.** Vendor and practitioner numbers use different clocks. Dwellir's 51 ms and the tweet's 60 ms might agree because both subtract a common cadence term, not because gRPC is fast.[^12,1]
5. **Counterexample on structure.** The Aquilina–Budish–O'Neill result that races persist despite competition cuts both ways: it supports "speed is an arms race" and equally "structural edges attract capital that also arbs them away."[^16,17]

Red-team pass: two of the three top claims (the documented per-block `l2Book`/`bbo` cadence and Glassnode's 884 ms fill median) survived adversarial search unbroken; the third, the diffusive-drift inference, drew one low-severity counterpoint, the stale-liquidity-sniping description already folded into section 04.[^24]

## 09. What to measure before spending

**Thesis: a three-number test decides whether a faster feed pays.**

The perpetuals info endpoint already exposes `fundingHistory` and `predictedFundings` across venues, which covers the structural half of the check.[^21] First, replay the bot's last 30 days of fills against a synchronised high-resolution book capture and compute the mid-price move between decision time and fill time; that is the realised cost of staleness, directly comparable to the 2–8 bp slippage.[^1] Second, split that into a median and a tail: a feed that removes the top 2% of frames matters only if those frames carry a disproportionate share of the loss. Third, check the credit burn: Quicknode's `StreamBboBook` is metered at 10 credits per 0.00165 MB, so measure bytes per hour for the coin set and extrapolate to a month before assuming $49 is the bill.[^7,9]

Cheap controls exist before buying anything. The public WebSocket allows up to 10 connections and 1,000 subscriptions, and `bbo` is event-driven per block, so testing `bbo` for the coins that matter is free and isolates how much of the gap is cadence versus network.[^3,4] If the gap persists with `bbo`, the premium feed has earned its place; if it closes, the problem was subscription choice.

**Why it matters.** The tweet's best idea is its closing one: establish where the loss is, then buy speed against it.

:::references
- {id: 1, title: "@UST_mean — Hyperliquid order book data latency, Quicknode gRPC (tweet)", url: "https://x.com/UST_mean/status/2114986287216369744", source: "X / Twitter", date: "2026-10-27"}
- {id: 2, title: "Hyperliquid Foundation WebSocket changes (Quicknode blog)", url: "https://www.quicknode.com/blog/hyperliquid-foundation-websocket-changes", source: Quicknode, date: "2026-06-12"}
- {id: 3, title: "Hyperliquid docs: WebSocket subscriptions", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions", source: "Hyperliquid docs"}
- {id: 4, title: "Hyperliquid docs: Rate limits and user limits", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits", source: "Hyperliquid docs"}
- {id: 5, title: "Hyperliquid docs: HyperCore overview", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/overview", source: "Hyperliquid docs"}
- {id: 6, title: "Glassnode Latency Monitor: Hyperliquid fill latency", url: "https://latency.glassnode.com/hyperliquid/fill-latency", source: Glassnode, date: "2026-03"}
- {id: 7, title: "Quicknode docs: Hyperliquid gRPC API", url: "https://quicknode.com/docs/hyperliquid/grpc-api", source: Quicknode}
- {id: 8, title: "Quicknode docs: Node.js OrderBook (L2/L4) setup", url: "https://www.quicknode.com/docs/hyperliquid/grpc-api/setup/nodejs-orderbook", source: Quicknode}
- {id: 9, title: "Quicknode pricing", url: "https://www.quicknode.com/pricing.md", source: Quicknode}
- {id: 10, title: "hyperliquid-dex/node README", url: "https://github.com/hyperliquid-dex/node", source: GitHub}
- {id: 11, title: "Amazon EC2 r6i.4xlarge pricing", url: "https://aws-pricing.com/r6i.4xlarge.html", source: "aws-pricing.com"}
- {id: 12, title: "Best Hyperliquid RPC providers 2026: full comparison (Quicknode blog)", url: "https://www.quicknode.com/blog/best-hyperliquid-rpc-providers-2026-full-comparison", source: Quicknode, date: "2026-02-08"}
- {id: 13, title: "HyperCore for Hyperliquid enters public beta (Quicknode blog)", url: "https://www.quicknode.com/blog/hypercore-for-hyperliquid-enters-public-beta", source: Quicknode, date: "2026-01-20"}
- {id: 14, title: "Hyperliquid docs: Fees", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees", source: "Hyperliquid docs"}
- {id: 15, title: "Hyperliquid docs: Funding", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding", source: "Hyperliquid docs"}
- {id: 16, title: "Quantifying the High-Frequency Trading Arms Race (NBER WP 29011)", url: "https://nber.org/papers/w29011", source: NBER, date: "2021"}
- {id: 17, title: "Research Spotlight: The High-Frequency Trading Arms Race (Budish, Cramton, Shim)", url: "https://www.richmondfed.org/publications/research/econ_focus/2015/q3/research_spotlight", source: "Richmond Fed Econ Focus", date: "2015"}
- {id: 18, title: "Bitcoin options price in 38.3 percent volatility, the price delivers 20.2", url: "https://cryptoticker.io/en/bitcoin-price-prediction-volatility-premium-20-october-2026/", source: CryptoTicker, date: "2026-10-20"}
- {id: 19, title: "Hyperliquid docs: Nodes", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/nodes", source: "Hyperliquid docs"}
- {id: 20, title: "Hyperliquid docs: Running a validator", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/validators/running-a-validator", source: "Hyperliquid docs"}
- {id: 21, title: "Hyperliquid docs: Info endpoint (perpetuals)", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals", source: "Hyperliquid docs"}
- {id: 22, title: "fxtwitter API representation of the seed tweet", url: "https://api.fxtwitter.com/UST_mean/status/2114986287216369744", source: fxtwitter, date: "2026-10-27"}
- {id: 23, title: "Dwellir docs: Hyperliquid Order Book WebSocket API (benchmark)", url: "https://www.dwellir.com/docs/hyperliquid/order-book-server", source: Dwellir}
- {id: 24, title: "Crypto price discovery and stale liquidity (Arrakis Finance)", url: "https://arrakis.finance/blog/crypto-price-discovery", source: "Arrakis Finance"}
:::
