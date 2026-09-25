---
eyebrow: CRYPTO · SYNTHETIC DOLLARS
title: "Ethena's $150 Trillion Bet: What USDe's Push Into Tokenized Equities Actually Buys"
deck: A single tweet framed a Binance tie-up as a twentyfold expansion of Ethena's addressable market. The mechanics say the real constraint is a few billion dollars of equity-derivative liquidity — and the last time this trade broke, USDe printed $0.65 on the exchange now hosting it.
lede: |
  On September 25, 2026, Ethena Labs announced it is expanding the collateral behind its USDe synthetic dollar into "bStocks" — Binance's tokenized US equities — hedged with equity perpetual futures, framing the move as unlocking a jump in addressable collateral from $2.5 trillion of crypto to more than $150 trillion of real-world assets. The $150 trillion figure is a real fact about the size of global equity markets. It is not a fact about how much of that market Ethena's basis trade can actually touch, and Ethena's own risk disclosures — not outside critics — say so.
stats:
  - {label: USDe market cap, value: $4.9B, note: "2026-09-25, -67% off Oct-2025 peak"}
  - {label: Qualifying equity-perp OI, value: $2.9B, note: "Binance, all venues combined"}
  - {label: USDe rank among stablecoins, value: "#4", note: "behind USDT, USDC, USDS"}
  - {label: ENA market cap, value: ~$2.3B, note: "2026-09-25"}
---

:::callout(kind=info, label="In short")
- Ethena is not adding $150 trillion of collateral capacity today. Binance's own reported equity-perpetual open interest was **$2.9 billion** as of the announcement[^2]; running Ethena's own $25M-eligibility gate across every venue narrows that to roughly **$2.73 billion** of pairs that actually qualify for the trade (Binance $2.14B, OKX $585M, Kraken $9.3M, Bybit $0).[^3] Either way, that is the actual near-term ceiling its own risk framework sets.
- USDe's core mechanism (long collateral, short an equal-notional perpetual) has gone through a real stress event before: it printed **$0.65** on Binance's own orderbook on October 10-11, 2025, while staying near $1 on Curve.[^14]
- The protocol's Reserve Fund — the backstop meant to keep sUSDe yield from ever going negative — held about **1.06% to 1.7%** of USDe's supply through 2026, thin relative to the multi-week negative-funding streaks the mechanism has produced historically.[^9][^11]
- Ethena Pay's advertised 5-6% savings rate is explicitly labeled a discretionary, revocable promotion in Ethena's own terms — one that exists precisely because the underlying basis-trade yield (~4.6-4.8% in September 2026) currently falls short of it.[^21][^23]
- A German regulator, not a crypto critic, has already tested the "USDe escapes stablecoin rules" thesis: BaFin fined Ethena's EU entity, forced a wind-down, and found grounds to suspect sUSDe is an unregistered security.[^30][^31]
:::

## 01. What Ethena actually announced

Ethena's September 25 announcement, relayed through The Block and Ethena's own channels, describes a specific and narrow mechanism: hold Binance "bStocks" — tokenized exposure to US equities — as collateral, and hedge the position with equity perpetual futures on the same venue, generating a funding-rate-driven basis yield the same way USDe's original crypto trade does.[^1][^2] Ethena founder Guy Young called it "the most significant expansion of USDe's funding mechanism since we started," and Ethena's own data (relayed by The Block, not independently audited by the outlet) put Binance's equity-perpetual open interest above $2.9 billion, growing at roughly a 105% compound monthly rate through 2026, with average annualized equity basis of 3.56% over the prior six months.[^2]

The headline framing — moving from "$2.5 trillion of crypto" to "$150 trillion-plus of real-world assets" as the addressable market — did not originate on September 25. Guy Young previewed the logic nearly a year earlier, arguing in October 2025 that equities are "more than 30x the size" of the crypto asset class that had already produced Ethena's core business, and Delphi Digital's Jose Macedo separately floated a $120 trillion figure for the same idea.[^6] The fact that two independent tellings of the same thesis land on different numbers ($150T vs. $120T) is itself a signal that this is a rhetorical order-of-magnitude claim, not a rigorously bounded estimate.

:::timeline
- {date: "2024-02", headline: "USDe launches", body: "Founded by Guy Young; delta-neutral basis trade begins with ETH/BTC collateral."}
- {date: "2024-04/05", headline: "First stress test", body: "More than $100M redeemed; USDe price held within 20bps of $1."}
- {date: "2025-10-10/11", headline: "Binance oracle dislocation", body: "USDe prints $0.65 on Binance's own orderbook amid a market-wide liquidation cascade; peg holds elsewhere."}
- {date: "2025-04 to 2025-06", headline: "BaFin enforcement", body: "Germany's regulator fines Ethena GmbH EUR600,000, orders wind-up, flags sUSDe as a suspected unregistered security."}
- {date: "2026-09-01", headline: "Ethena Pay launches", body: "Self-custodial neobank on Avalanche; up to 6% savings, AVAX-denominated cashback."}
- {date: "2026-09-08", headline: "Fee switch approved", body: "Governance vote passes to route 5-20% of gross revenue to ENA buybacks once USDe supply hits tiered thresholds."}
- {date: "2026-09-25", headline: "bStocks / equity perps", body: "USDe backing expands into tokenized-equity collateral hedged with equity perpetuals."}
:::

Why this matters: every subsequent section of this piece is really a stress test of the same underlying claim — that a mechanism built for one liquidity pool (crypto perpetuals) transfers cleanly to another (equity perpetuals, consumer payments, tokenized RWA) without changing its risk profile. The record so far says it doesn't transfer for free.

## 02. The TAM math: why $150 trillion is not $150 trillion of capacity

Ethena's delta-neutral trade does not earn yield from the size of an asset class. It earns yield from funding payments generated by leveraged positioning in a *derivatives market* — a structurally different and vastly smaller number than the spot market it references. Ethena's own Risk Committee, in a framework document authored by Kairos Research and published to Ethena's governance forum in August 2026, makes the constraint explicit: an equity perpetual market must clear at least $25 million of one-sided open interest (14-day average) and post 30 days of funding history before it is even eligible for the trade.[^3]

The results of applying that gate to the real market, as of August 26, 2026, are the actual capacity number that matters — and it is nowhere near $150 trillion:

:::bars
- {label: "Binance (qualifying pairs)", value: "$2.14B OI", pct: 78}
- {label: "OKX (qualifying pairs)", value: "$585M OI", pct: 21}
- {label: "Bybit (qualifying pairs)", value: "$0", pct: 1}
- {label: "Kraken (qualifying pairs)", value: "$9.3M", pct: 0.3}
:::

Binance qualified 17 of its 67 matched equity-perp pairs; OKX qualified 3; Bybit qualified zero (its SpaceX contract sat at 97% of the threshold); Kraken's entire 14-contract equity-perp lineup totaled $9.3 million in open interest, qualifying none.[^3] Total qualifying capacity across every venue Ethena evaluated: roughly $2.73 billion[^3] — a figure that is a rounding error against $150 trillion, and even against the ~$15 billion USDe itself once captured in *crypto* perpetuals, a market that took years to reach that depth.[^9]

Ethena's own extrapolation is more mechanistic than a bare TAM headline: reporting on the announcement notes the company models a roughly 2.5% open-interest-to-market-cap "penetration ratio" — the rate crypto perpetuals reached relative to crypto's own market cap — and applies it to global equities (~$166.5 trillion) to arrive at a theoretical ~$4 trillion long-run equity-perpetual open-interest ceiling.[^5] That is a real, ratio-based argument, not pure rhetoric, and it implies roughly 1,400x today's actual qualifying capacity. It is also unproven: crypto took years of market-structure maturation to reach 2.5% penetration, equities carry structural frictions crypto perpetuals don't (nightly/weekend market closures, exchange fragmentation, securities-law overhang), and $4 trillion of *eventual* open interest is still nowhere near $150 trillion of *collateral capacity* — the two numbers describe different things even in Ethena's own best-case model.

:::callout(kind=warn, label="Risk")
Ethena's own risk team states plainly that bStock holders "have no proprietary interest in the backing shares" and that holding bStocks as trade collateral is "unsecured credit exposure to a Binance affiliate" (BTech Holdings), with no multisig or timelock protecting the token's shared upgrade key.[^3][^4] That is a materially different risk than owning the underlying equities — it is closer to an unsecured claim on a single counterparty's promise to maintain 1:1 backing.
:::

Crypto-market history is the natural benchmark here, and it argues for skepticism rather than extrapolation. Crypto's roughly $4 trillion asset class produced an actually-captured basis-trade opportunity in the tens of billions, not trillions — a two-to-three-order-of-magnitude discount from spot size to derivative capacity, achieved only after years of market-structure maturation.[^9] Independent commentary on the September 2026 announcement makes the same point directly: the $150 trillion figure "describes the wider market opportunity rather than an amount Ethena has allocated or secured as USDe backing."[^5] The 105% compound monthly growth rate in Binance's equity-perp open interest is the more meaningful number to track — but compounding from a $2.9 billion base takes years to approach even a small fraction of $150 trillion, assuming equity derivatives markets can scale to crypto-style 24/7 depth at all, which is not obvious given market-hours mismatches (US equities trade roughly 30% of the week) and existing securities-market fragmentation.

Why this matters: if the addressable-market claim is the thesis investors are pricing into ENA and USDe adoption expectations, the gap between the rhetorical number and the mechanical ceiling is exactly the kind of gap that produces disappointment once growth rates (however fast) are measured against the honest denominator.

## 03. Inside the engine: the delta-neutral trade and funding-rate risk

USDe's mechanism, unchanged in its essentials since its February 2024 launch, is: hold spot or staked crypto collateral (originally ETH and BTC, since diversified), short an equal notional amount of the same asset via perpetual or dated futures, and collect the difference between staking yield and (usually positive) funding paid by leveraged longs.[^7][^8] Collateral sits with off-exchange settlement custodians — Copper, Ceffu, and Fireblocks — which can delegate assets to an exchange for margining without ever transferring beneficial title, insulating collateral from an exchange's own insolvency.[^7]

Delta-neutrality hedges *price* risk. It does not hedge *funding-rate* risk, which is a separate, unhedged cash flow set by the balance of leveraged long and short demand — and Ethena's own three-year retrospective shows that cash flow is not reliably positive. Over the trailing three years, ETH perpetual funding was net negative on 17.5% of days and BTC on 15.9%, with *combined* net revenue (funding plus staking yield) negative on 8.84% of days; the longest negative streak observed was 13 days against a 176-day longest positive streak.[^9]

:::stats
- {label: "ETH negative-funding days", value: "17.5%", note: "trailing 3-year window"}
- {label: "BTC negative-funding days", value: "15.9%", note: "trailing 3-year window"}
- {label: "Combined negative-revenue days", value: "8.84%", note: "funding + staking yield"}
- {label: "Longest negative streak", value: "13 days", unit: "vs. 176d positive"}
:::

Ethena's answer to this is architectural, not statistical: sUSDe is designed so stakers "can only accrue positive or flat rewards," with any shortfall absorbed by a separate Reserve Fund rather than passed through as negative yield.[^10] That converts a variable, sometimes-negative cash flow into one that is either attractive or flat from a holder's perspective — a sound design *if* the Reserve Fund is large enough, a question the next section takes on directly.

sUSDe's realized yield has swung across a wide range consistent with this variability: a 35.2% all-time high near the Q1 2024 bull peak, an all-time low of 4.1% in August 2024 (a compression from 19% to 4% inside 11 days), a 90-day trailing average around 9.4-11.8% in an April 2026 snapshot, and a live Aave supply-side rate near 4.7-4.8% as of September 25, 2026.[^12][^13]

:::note
sUSDe yield figures compiled from a third-party aggregator (eco.com) and a live Aave market rate (Aavescan), not Ethena's own protocol-wide dashboard — treat exact percentages as directionally reliable, not audited.
:::

Why this matters: "delta-neutral" is routinely shorthand, in coverage of Ethena, for "safe." Ethena's own numbers say the trade is *price-hedged*, not *yield-guaranteed* — the entire viability of the "always positive" promise rests on a Reserve Fund whose size is a policy choice, not a mechanical property of the hedge.

## 04. Stress-tested once already: the October 2025 Binance dislocation

The clearest evidence available on how this mechanism behaves under stress is the market-wide liquidation event of October 10-11, 2025 — reportedly the largest in crypto history at the time — during which USDe's price diverged sharply across venues.

:::compare
- {role: LOWEST, name: "Binance orderbook", value: "$0.65"}
- {role: HIGHEST, name: "Bybit", value: "$0.92"}
- {role: SUBJECT, name: "Curve (deep liquidity)", value: "~$1.00 (<100bps)"}
:::

Guy Young publicly rejected the "depeg" framing, attributing the gap to Binance's own internal oracle sourcing prices from a thin, illiquid orderbook — compounded by deposit/withdrawal friction on Binance that prevented arbitrageurs from closing the gap — rather than to any impairment of USDe's actual collateral.[^15] Ethena's own disclosures in the days after the event reported the protocol remaining overcollateralized (on the order of tens of millions of dollars of excess collateral) and having processed roughly $2 billion in redemptions within 24 hours without interruption; Chainlink separately confirmed via its own proof-of-reserve feed that Ethena's collateral remained above $9 billion through the event.[^17] ==The exact excess-collateral figure and the specific list of attesting firms could not be independently confirmed against a single first-party report in this research pass; treat the precise dollar amount as directionally reported, not audited here.== No source found in this research — including independent data firm Coin Metrics — alleges that redemptions were halted or that Ethena's actual custodied collateral was impaired; collateral was reported above 100% throughout.[^20]

That is the strongest part of the "nothing was structurally wrong" reading, and the mechanics support it: a protocol that is actually insolvent cannot sustain $1 billion-plus-per-hour redemptions near 1:1 without freezing them, and USDe didn't freeze them. But two complications keep the episode from being a clean bill of health. First, the dislocation was not confined to a single venue's quirk: Bybit's price moved too, just less severely, weakening the strictest "isolated to one exchange" version of the explanation.[^14] Second, a competing causal theory — voiced publicly by OKX's CEO — holds that Binance's own USDe yield-promotion campaign had encouraged leveraged loops using USDe as collateral, which set up the cascade rather than a pure oracle bug; Dragonfly's Haseeb Qureshi countered that BTC bottomed roughly 30 minutes before USDe's price gap opened on Binance, arguing USDe could not have caused the broader liquidation wave.[^16] That causation debate remains unresolved between named analysts rather than settled.

The event also had real second-order consequences outside Ethena's own balance sheet. Aave manually hardcoded USDe/sUSDe oracle pricing to USDT to halt cascading liquidations on its lending markets — an intervention the Bank Policy Institute criticized as shifting risk to lenders rather than eliminating it, though no bad debt materialized in the specific Morpho markets checked.[^18] BPI, a US bank policy group with its own institutional interest in stricter stablecoin rules, went on to cite the event as evidence that leveraged synthetic-dollar stablecoins could transmit losses into fiat-backed stablecoins during stress — commentary, not a regulatory finding, but a marker of how the episode is being used in the broader stablecoin-policy debate.[^18]

:::callout(kind=danger, label="What actually moved")
USDe's total supply fell from a peak of roughly $14.8 billion in October 2025 to about $4.9 billion by September 2026 — an $8-10 billion contraction one research firm labeled a "sharp loss of confidence." Mechanically, that outflow is redemptions working as designed (the opposite of insolvency), but reputationally it is the most durable consequence of the October event.[^19]
:::

Why this matters: the October 2025 event is the single most relevant precedent for judging what happens when Ethena's *new* equity-perpetual leg hits its own stress event — on a venue (Binance) that already demonstrated its internal pricing infrastructure can diverge sharply from deep-liquidity references under load.

## 05. The reserve fund: how thin is the backstop

The Reserve Fund is the component actually doing the work of the "sUSDe yield never goes negative" promise, so its size relative to potential shortfalls is the load-bearing risk metric — more so than the headline funding-rate statistics in Section 3.

As of end-March 2026, Ethena's own governance-forum update reported the Reserve Fund at approximately $62 million ($41.98M in USDtb plus $20.02M in a USDtb-USDC liquidity position) against roughly $5.8 billion of USDe supply — a 1.061% ratio, which Ethena modeled as about 9x a conservative 24-hour unwind-stress requirement.[^11] Independent analysis from Hindenrank put the fund at a somewhat larger $73 million (1.7% of supply) by mid-2026, but modeled depletion in roughly 52 days under a moderately bearish funding scenario.[^11]

:::kv
- {term: "Reserve Fund (end-Mar 2026)", def: "$62M — 1.061% of USDe supply"}
- {term: "Independent estimate (mid-2026)", def: "$73M — 1.7% of supply"}
- {term: "Ethena's own stress model", def: "~9x a 24h unwind requirement"}
- {term: "Modeled depletion (Hindenrank, bearish case)", def: "~52 days"}
:::

The tension is structural: the fund is capitalized *by* prior positive-funding periods, meaning it is largest exactly when it is needed least and thinnest exactly when a sustained funding drought — the kind of multi-week negative streak the 2022 bear market produced, at a scale Ethena's own three-year retrospective (Section 3) confirms is a recurring, not exceptional, feature of perpetual markets — would draw it down fastest. Ethena's single largest historical stress test, the April-May 2024 redemption wave (over $100 million redeemed, peg held within 20 basis points), validated the mechanism's response to *redemption-driven* stress.[^9] It has not yet faced a *funding-driven* solvency stress at anything like the multi-billion-dollar scale USDe operates at today, and a 1-1.7% reserve ratio leaves limited room for error if one materializes at the same time the equity-perpetual leg (Section 2) is also under load.

Why this matters: every promotional claim about USDe's stability rests on the Reserve Fund holding up under conditions materially worse than anything it has faced since 2022 — at current supply levels, a scenario the protocol has not experienced.

## 06. Ethena Pay: a neobank funded by a shrinking basis trade

Ethena Pay, a self-custodial neobank app launched on Avalanche on September 1, 2026, offers IBAN-linked accounts and a Visa card across 48 countries (excluding the US and EU at launch), advertising up to 6% dollar savings[^21] and cashback that Ethena's launch reporting put at 4% (Standard) up to 5% (VIP base rate), rising to as much as 10% at select partner brands, paid in AVAX.[^26]

The product's own terms undercut the "sustainable yield" reading before any external critique is needed. Ethena Pay's FAQ explicitly classifies the "Daily Boost" — the top-up that gets a user from base USDe yield to the advertised 5-6% tier rate — as "a discretionary promotional incentive: it is not interest, not yield, not a deposit," and states the Boost automatically zeroes out the moment base yield already covers the tier rate.[^21] That structure only makes sense if base yield is currently *below* the advertised floor, and it is: live Aave sUSDe supply APY sat at roughly 4.67-4.84% on September 25, 2026, and Ethena's own August 27, 2026 governance proposal used a 4.6% backing-yield assumption — below both the 5% Standard and 6% Pro/VIP tiers.[^13][^23]

:::kv
- {term: "Standard tier savings rate", def: "5% (balance cap ~$5K)"}
- {term: "Pro/VIP tier savings rate", def: "6% (higher caps, ENA lock required)"}
- {term: "Underlying base yield (Sept 2026)", def: "~4.6-4.8%"}
- {term: "Card cashback", def: "4-10%, paid in AVAX (not USDe/ENA)"}
:::

The gap is not small in context: Ethena's own basis-trade carry compressed roughly 61% in about five weeks, from approximately 18% in late July 2026 to approximately 7% by August 26, 2026 — the opposite direction from what a newly-launched, additive cashback liability would need.[^23] Layering that on top: cashback is denominated in AVAX, a third party's token, not USDe or ENA, consistent with Avalanche Foundation ecosystem-incentive funding rather than Ethena's own basis-trade economics — Ava Labs has itself described the arrangement as "a template other neobanks and fintechs could copy," language that describes a co-marketed customer-acquisition deal more than a bank product's standalone unit economics.

:::callout(kind=warn, label="Design signals, not just math")
Every incentive in Ethena Pay's terms points toward customer acquisition rather than passive banking: the Boost requires at least one card transaction per month, Pro/VIP tiers require locking $2,000-$10,000 of ENA (tying "higher yield" to ENA demand, not banking fundamentals), and account balance caps bound Ethena's total dollar exposure to a fixed promotional budget.[^21]
:::

Around the September 1 launch, ENA rose roughly 5.3% same-day (to $0.1574) and about 14% over the following days, though the move overlapped with a separate September 2 fee-switch governance vote and left ENA about 89% below its all-time high — making the launch a contributing catalyst, not a cleanly isolated one.[^24][^25]

Why this matters: a consumer financial product marketed on a headline yield that is explicitly discretionary and currently unfunded by underlying economics is a subsidized distribution channel for USDe and ENA adoption, not evidence that the basis trade generates enough durable yield to support a banking-style product — a distinction retail users are unlikely to parse from the marketing.

## 07. Regulation: the GENIUS Act gap and BaFin's precedent

The regulatory case for USDe's yield rests on a definitional argument: the US GENIUS Act (signed July 18, 2025) defines a "payment stablecoin" functionally, by (a) design for use in payment or settlement and (b) an issuer obligation to redeem for a fixed amount of monetary value — and separately bars payment-stablecoin issuers from paying holders interest or yield solely for holding the coin.[^27] USDe is overwhelmingly used as DeFi/CeFi collateral and a yield-bearing store of value rather than as a payment rail comparable to USDC or USDT, so an argument that it fails prong (a) and sits outside the "payment stablecoin" box is plausible — and, as far as this research found, untested in US courts or by US regulators rather than settled either way.

Ethena's own conduct is revealing here: rather than attempting to bring USDe itself into GENIUS-style compliance, the company partnered with Anchorage Digital Bank to launch an entirely separate token, USDtb, explicitly described as offering "a clear pathway to becoming compliant" — leaving USDe outside that compliance claim altogether.[^29] That is a tell that Ethena itself does not believe USDe's structure could clear a licensed-issuer bar, whatever the definitional argument's merits.

The one jurisdiction that has actually adjudicated an analogous question, rather than merely debating it, ruled against the "escapes regulation" framing. Germany's BaFin brought MiCAR's first-ever enforcement action against Ethena GmbH in 2025: freezing reserves, banning public USDe sales, and ultimately imposing a EUR600,000 coercive fine and ordering wind-up after Ethena withdrew its EU authorization application, citing "serious deficiencies in the business organisation of Ethena GmbH."[^30] Separately, and more pointedly for the yield question specifically, BaFin found "sufficient grounds to suspect" that sUSDe — the very wrapper structured to carry yield outside stablecoin rules — constitutes an unregistered security offered without a required prospectus.[^31] MiCA's Article 50 independently bars e-money-token issuers from granting interest at all, using a broad definition meant to catch economically-equivalent workarounds.[^32]

:::callout(kind=info, label="Strongest counter-argument")
Two hedges apply to the "already tested and rejected" framing above, and both matter. First, BaFin's securities-suspicion finding against sUSDe is explicitly framed as "sufficient grounds to suspect" — a preliminary characterization, never converted into a binding fine the way the MiCAR action against Ethena GmbH was. Second, and more substantively, BaFin classified USDe as an Asset-Referenced Token under MiCAR — a compositional test based on what backs the token — not as an E-Money Token, which is the MiCAR category legal commentators consider closest to the US GENIUS Act's "payment stablecoin" (a redemption/reserve-quality test). Those are genuinely different legal questions, so a EU enforcement outcome on USDe's ART status does not mechanically settle whether USDe would be found a GENIUS Act payment stablecoin in the US. No US regulator (SEC, CFTC, Treasury) has taken any public action or issued guidance on USDe's status specifically. The accurate framing is that the US question remains genuinely untested, not "resolved in Ethena's favor" — but it is also not resolved against Ethena on identical legal grounds, only on a related one.[^30][^31]
:::

A useful piece of doctrinal backdrop, though it does not address USDe directly: US SEC staff issued a joint statement in January 2026 affirming that the federal securities laws apply to tokenized securities regardless of their technological format — a substance-over-form posture consistent with how BaFin treated sUSDe, and relevant by analogy to how regulators might eventually view Binance's tokenized-equity bStocks, which have not yet been the subject of any specific regulatory ruling in any jurisdiction found in this research.[^34] A dedicated BIS survey of stablecoin-yield regulatory approaches (October 2025) does not yet recognize "delta-neutral" or "synthetic dollar" yield as a distinct regulatory category at all — an absence, not an endorsement.[^33]

Why this matters: the regulatory thesis embedded in Ethena's marketing — "we are not a stablecoin, so stablecoin rules don't bind us" — has already been tested once, by a real regulator, and the result was not "unregulated." It was enforcement under a different rule (MiCAR) plus a live suspicion of an even more burdensome one (securities law).

## 08. ENA and the fee switch: does the math support a re-rating?

ENA, Ethena's governance token, has roughly 10.1 billion tokens in circulation against a 15 billion maximum supply, with a market capitalization of approximately $2.1-2.5 billion as of September 25, 2026.[^35] The price path has been volatile: from roughly $0.56-0.70 in August-September 2025, down to a 2026 low near $0.07 in the March-June window, recovering to roughly $0.21-0.25 by late September 2026 — a trend visible across the run-up to and aftermath of the fee-switch vote and Ethena Pay launch.[^35][^36]

{sparkline:55.9,20.0,13.9,9.1,7.2,22.5}
*ENA price, cents, monthly close approximation, Sep-2025 through Sep-2026.[^35][^36]*

A governance vote on September 3-8, 2026 — passing near-unanimously but on low turnout (17.8 million ENA voting, roughly 0.18% of circulating supply) — approved a "fee switch" that would direct 5-20% of *gross* protocol revenue (95% of that slice to open-market ENA buybacks) once USDe's 14-day average supply crosses tiered thresholds from $7.5 billion up to $20 billion.[^38][^39] As of September 20, 2026, USDe's supply of roughly $4.75 billion sat about 37% below the $7.5 billion floor needed to trigger even the lowest, 5%, tier — meaning the switch is approved but not yet active.[^40]

The revenue math matters more than the vote outcome. Ethena's cumulative gross protocol revenue since launch is approximately $1.04 billion ($284 million trailing-twelve-months), but that figure is overwhelmingly funding-rate income that is *contractually* the property of USDe/sUSDe holders as yield — it is not money available to ENA under the current design. The protocol's actual retained profit, independent of the fee switch, was only about $614,000 in Q1 2026 (down from roughly $10.18 million in Q3 2025)[^40][^41], a figure broadly consistent with DeFiLlama's own live tracker, which separately shows Ethena's trailing-year annualized revenue at roughly $2.89 million against approximately $275 million in annualized fees.[^50]

:::stats
- {label: "Trailing-12mo gross revenue", value: "$284M", note: "belongs to USDe/sUSDe holders"}
- {label: "Q1 2026 retained profit", value: "$614K", note: "down from $10.18M in Q3 2025"}
- {label: "Tier-1 buyback flow (if activated)", value: "~$13.5M/yr", note: "5% of $284M x 95%"}
- {label: "Top disclosed tier (20%, never reached)", value: "~$54M/yr", note: "at flat $284M revenue"}
:::

Even generously holding trailing revenue flat at $284 million, the lowest activatable tier (5%, requiring USDe to grow 58% from current levels) implies roughly $13.5 million a year in buybacks — an approximately 0.5-0.6% "buyback yield" against a $2.1-2.5 billion market cap. The highest disclosed tier (20%, at $20 billion USDe supply — a level never yet reached; the October 2025 peak was $14.8 billion) implies roughly $54 million a year, a 2.2-2.6% yield, and only if revenue holds steady while supply more than quadruples from today. For context, one analyst estimate puts more than $300 million of scheduled 2026 ENA token emissions at current prices — six to twenty times any realistic near-term buyback figure — and ENA's daily trading volume (reported around $74 million) means even the top-tier buyback flow is roughly 0.2% of a single day's volume, not a mechanically significant demand shock.

ENA's roughly 200%+ rally from its June 2026 trough to late September overlaps closely with the fee-switch proposal (August 27) and vote (September 2-8), consistent with the market having already re-rated the token on the *news* of the switch, ahead of any dollar actually flowing through it.[^35][^36] Bulls point out ENA trades cheaply relative to gross fees collected — but that comparison conflates gross USDe revenue, which belongs to stablecoin holders, with the much smaller slice ENA can actually capture even at full activation.

Why this matters: priced against the revenue ENA can actually capture even under generous full-activation assumptions (~$13.5-54 million/year), a $2.1-2.5 billion market cap implies a forward multiple in the tens to hundreds — a bet on USDe supply growing well past its historical peak, not a valuation grounded in currently disclosed, activatable cash flow.

## 09. Competitive landscape: moat or commodity trade?

USDe's approximately $4.9 billion market cap ranks it fourth among all stablecoins as of September 25, 2026 — behind USDT (~$183.7B), USDC (~$76.2B), and Sky's USDS (~$6.6B), and only narrowly ahead of DAI (~$4.79B) and USD1/World Liberty Financial (~$4.4B), a margin thin enough to flip on any given week.[^42][^43] USDT and USDC alone accounted for roughly 85% of total stablecoin market capitalization (approximately $305 billion) — the delta-neutral, yield-bearing category that USDe pioneered remains a small fraction of the overall market.[^43][^44]

:::rank-list
- {label: USDT, value: "$183.7B", pct: 100}
- {label: USDC, value: "$76.2B", pct: 41}
- {label: USDS, value: "$6.6B", pct: 4}
- {label: USDe, value: "$4.9B", pct: 3, highlight: true}
- {label: DAI, value: "$4.8B", pct: 3}
- {label: "USD1 (WLFI)", value: "$4.4B", pct: 2}
:::

The delta-neutral basis trade at USDe's core is not proprietary technology — a Bitwise executive observed as early as April 2024, before any credible rival existed, that Ethena had "just put this trade into a protocol, tokenized it, and then issued units of it," describing a decades-old cash-and-carry strategy rather than a novel mechanism.[^49] The competitive field since has split along exactly that line. Resolv's USR runs a near-identical mechanism and suffered its own operational-security failure — an approximately $80 million unauthorized mint via a compromised key on March 22, 2026 — showing that clones inherit the full basis-trade risk surface plus their own added attack surface, with no differentiation to show for it.[^46] Falcon Finance's USDf (~$1.2 billion market cap) differs on the minting side (overcollateralized, multi-asset) but explicitly mirrors Ethena's delta-neutral yield engine.[^47] Genuinely different mechanisms exist in the category — Usual's USD0 and Ondo's USDY are backed by tokenized short-term US Treasuries, trading funding-rate/exchange-counterparty risk for duration and custodian risk instead — but they are a different risk bet entirely, not a like-for-like comparison.[^48]

Ethena's own portfolio shifts corroborate the "commoditizing" reading more than the "defensible moat" one: the crypto basis trade, once effectively the entirety of USDe's backing, has been diversified down to a small share of total backing over 2026 as the protocol has rotated into RWA exposure, DeFi lending, and now equity perpetuals — consistent with the original trade no longer scaling profitably once competitors and Ethena's own size began chasing the same finite pool of perpetual open interest.[^49]

:::note
What would flip this: if Ethena's exchange relationships, custody integrations, and risk-committee infrastructure (Section 2) prove durably hard to replicate — rather than the trade itself — the moat argument shifts from "mechanism" to "distribution," a real but different claim that would require evidence Ethena maintains a first-mover advantage in *venue access*, not yield.
:::

Why this matters: if the mechanism is commoditized, USDe's medium-term competitive position depends on scale, exchange relationships, and execution — assets that erode, rather than compound, once well-capitalized copies exist and the finite pool of qualifying derivative liquidity gets split among more claimants.

## 10. What would change this analysis

The critical reading in this piece rests on evidence that is itself imperfect, and several developments would meaningfully revise it. If Binance's equity-perpetual open interest keeps compounding at anything close to its recent 105% monthly rate for a sustained period — rather than the growth rate decaying as it approaches genuinely limited market depth — the TAM gap in Section 2 would narrow faster than the historical crypto-perpetual analogy suggests. If Ethena's Reserve Fund is meaningfully rebuilt from its 1-1.7% ratio toward a level closer to the 9x-of-24h-stress buffer Ethena itself models as adequate, the funding-drought risk in Sections 3 and 5 would be substantially better hedged. If USDe supply recovers toward its October 2025 peak and the fee switch activates at higher tiers with revenue holding steady rather than compressing further, the ENA valuation case in Section 8 gets meaningfully stronger. And if a US regulator explicitly declines to treat USDe as a payment stablecoin — rather than the question remaining untested — the regulatory argument in Section 7 moves from "plausible but unlitigated" to "confirmed."

:::position(confidence=medium, horizon=2027-Q2)
stance: The equity-perpetual expansion will scale in line with Binance's actual qualifying open interest (low-single-digit billions, growing but bounded by market-hours and liquidity constraints) rather than anywhere near the $150 trillion framing, and Ethena Pay's advertised savings rate will be reduced or restructured before basis-trade carry recovers to cover it organically.
consensus: Crypto-market coverage has largely repeated Ethena's own $150 trillion TAM framing without benchmarking it against the open-interest eligibility data in Ethena's own risk-committee document.
resolves: Watch Binance/OKX equity-perpetual open interest reported in Ethena's or Binance's own disclosures over the next two-to-three quarters, and any change to Ethena Pay's advertised savings-rate tiers or Boost terms.
:::

None of this makes USDe's mechanism fraudulent or Ethena's disclosures dishonest — if anything, Ethena's own risk-committee documents are the single best source for the caveats in this piece, more candid than most of the press coverage repeating the company's headline framing. The gap this analysis identifies is between a real, working delta-neutral trade with a demonstrated (if imperfect) stress-test record, and a growth narrative measured in the size of asset classes rather than the size of the markets that actually generate the protocol's yield.

:::references
- {id: 1, title: "Ethena announcement", url: "https://x.com/ethena/status/2103439484113346986", source: "X / Ethena", date: "2026-09-25"}
- {id: 2, title: "Ethena expands USDe backing strategy into bStocks and equity perpetuals on Binance", url: "https://www.theblock.co/news/deals/2026-09-25-ethena-expands-usde-backing-strategy-into-bstocks-and-equity-perpetuals-on-binance-416367", source: "The Block", date: "2026-09-25"}
- {id: 3, title: "A framework for the tokenized equity basis trade", url: "https://gov.ethenafoundation.com/t/a-framework-for-the-tokenized-equity-basis-trade/832", source: "Ethena Governance Forum (Kairos Research)", date: "2026-08-28"}
- {id: 4, title: "What are bStocks? A guide to tokenized stocks on Binance", url: "https://www.binance.com/en/academy/articles/what-are-bstocks-a-guide-to-tokenized-stocks-on-binance", source: "Binance Academy", date: "2026-06-12"}
- {id: 5, title: "Ethena opens a new yield market for USDe with Binance bStocks", url: "https://www.crypto-news-flash.com/ethena-opens-a-new-yield-market-for-usde-with-binance-bstocks/", source: "Crypto News Flash", date: "2026-09-25"}
- {id: 6, title: "Bigger Than Robinhood: Ethena's Guy Young Bets On 30x Equity-Perpetual Boom", url: "https://ambcrypto.com/bigger-than-robinhood-ethenas-guy-young-bets-on-30x-equity-perpetual-boom/", source: "AMBCrypto", date: "2025-10-01"}
- {id: 7, title: "Backing, Custody and Security — Overview", url: "https://docs.ethena.fi/backing-custody-and-security/overview", source: "Ethena Docs", date: "2026"}
- {id: 8, title: "Ethena Labs company profile", url: "https://cryptoslate.com/companies/ethena-labs/", source: "CryptoSlate", date: "2026"}
- {id: 9, title: "Funding Risk", url: "https://docs.ethena.fi/protocol-overview/risks/funding-risk", source: "Ethena Docs", date: "2026"}
- {id: 10, title: "Rewards Mechanism", url: "https://docs.ethena.fi/protocol-overview/rewards-mechanism", source: "Ethena Docs", date: "2026"}
- {id: 11, title: "Reserve Fund — March 2026 Update", url: "https://gov.ethenafoundation.com/t/reserve-fund-march-2026-update/775", source: "Ethena Governance Forum", date: "2026-03"}
- {id: 12, title: "sUSDe Explained: Ethena's Yield-Bearing Stablecoin", url: "https://eco.com/support/en/articles/14798653-susde-explained-ethena-s-yield-bearing-stablecoin", source: "Eco", date: "2026-04-25"}
- {id: 13, title: "Ethena sUSDe rates", url: "https://aavescan.com/rates/ethena-susde", source: "Aavescan", date: "2026-09-25"}
- {id: 14, title: "No, Ethena's USDe Didn't De-Peg", url: "https://www.coindesk.com/markets/2025/10/13/no-ethena-s-usde-didn-t-de-peg", source: "CoinDesk", date: "2025-10-13"}
- {id: 15, title: "USDe price slip not a true depeg, says Ethena founder", url: "https://thecurrencyanalytics.com/altcoins/usde-price-slip-not-a-true-depeg-says-ethena-founder-urges-external-oracles-204599", source: "The Currency Analytics", date: "2025-10-11"}
- {id: 16, title: "OKX CEO: Binance's USDe Yield Campaign Caused the October 10 Crash", url: "https://finance.yahoo.com/news/okx-ceo-binance-usde-yield-151104149.html", source: "Yahoo Finance", date: "2025-10"}
- {id: 17, title: "Ethena USDe oracle design, October 2025", url: "https://coinfomania.com/ethena-usde-oracle-design-october-2025/", source: "Coinfomania", date: "2025-10-12"}
- {id: 18, title: "Stablecoin Risks: Some Warning Bells", url: "https://bpi.com/stablecoin-risks-some-warning-bells/", source: "Bank Policy Institute", date: "2025-11"}
- {id: 19, title: "Ethena's USDe loses $8.3B since October crash amid loss of confidence", url: "https://www.tradingview.com/news/cointelegraph:4bc2a9faa094b:0-ethena-s-usde-loses-8-3b-since-october-crash-amid-loss-of-confidence/", source: "Cointelegraph via TradingView", date: "2025-12"}
- {id: 20, title: "State of the Network, Issue 335", url: "https://coinmetrics.substack.com/p/state-of-the-network-issue-335", source: "Coin Metrics", date: "2025-10"}
- {id: 21, title: "Ethena Pay FAQ", url: "https://pay.ethena.fi/faq", source: "Ethena Pay", date: "2026-09-01"}
- {id: 22, title: "Ethena launches Ethena Pay, a self-custodial neobank built exclusively on Avalanche", url: "https://www.blockhead.co/2026/09/02/ethena-launches-ethena-pay-a-self-custodial-neobank-built-exclusively-on-avalanche/", source: "Blockhead", date: "2026-09-02"}
- {id: 23, title: "Ethena's stablecoin economics give and take", url: "https://alearesearch.substack.com/p/ethenas-stablecoin-economics-give", source: "Alea Research", date: "2026-08-27"}
- {id: 24, title: "ENA price reaction coverage", url: "https://coinmarketcap.com/top-stories/6a9cca3698f4795d490fd4c1/", source: "CoinMarketCap", date: "2026-09-01"}
- {id: 25, title: "Ethena jumps 7% following launch of Avalanche-powered neobank", url: "https://bitcoinethereumnews.com/finance/ethena-jumps-7-following-launch-of-avalanche-powered-neobank/", source: "Bitcoin Ethereum News", date: "2026-09-02"}
- {id: 26, title: "Ethena Pay app: Avalanche, yield, cashback", url: "https://www.theblock.co/news/web3/2026-09-01-ethena-pay-app-avalanche-yield-cashback-413225", source: "The Block", date: "2026-09-01"}
- {id: 27, title: "GENIUS Act, Public Law 119-27", url: "https://www.congress.gov/119/plaws/publ27/PLAW-119publ27.htm", source: "US Congress", date: "2025-07-18"}
- {id: 28, title: "Circle, Coinbase, and the Prohibition on Interest Under the GENIUS Act", url: "https://clsbluesky.law.columbia.edu/2025/12/11/circle-coinbase-and-the-prohibition-on-interest-under-the-genius-act/", source: "Columbia CLS Blue Sky Blog", date: "2025-12-11"}
- {id: 29, title: "Anchorage Digital partners with Ethena Labs to launch first GENIUS-compliant, federally regulated stablecoin", url: "https://www.anchorage.com/insights/anchorage-digital-partners-with-ethena-labs-to-launch-first-genius-compliant-federally-regulated-stablecoin", source: "Anchorage Digital", date: "2025-07-24"}
- {id: 30, title: "Ethena GmbH enforcement notice", url: "https://www.bafin.de/SharedDocs/Veroeffentlichungen/EN/Verbrauchermitteilung/weitere/2025/meldung_2025_04_15_Ethena_GmbH_en.html", source: "BaFin", date: "2025-06-25"}
- {id: 31, title: "sUSDe securities-suspicion notice", url: "https://www.bafin.de/SharedDocs/Veroeffentlichungen/EN/Verbrauchermitteilung/weitere/2025/meldung_2025_06_03_sUSDe_en.html", source: "BaFin", date: "2025-06-03"}
- {id: 32, title: "MiCA Article 50 — Prohibition of granting interest", url: "https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mica/article-50-prohibition-granting-interest", source: "ESMA", date: "2024"}
- {id: 33, title: "FSI Brief No. 27 — stablecoin yield regulatory approaches", url: "https://www.bis.org/fsi/fsibriefs27.pdf", source: "Bank for International Settlements", date: "2025-10-23"}
- {id: 34, title: "Statement on tokenized securities", url: "https://www.sec.gov/newsroom/speeches-statements/corp-fin-statement-tokenized-securities-012826-statement-tokenized-securities", source: "US SEC", date: "2026-01-28"}
- {id: 35, title: "Ethena (ENA)", url: "https://www.coingecko.com/en/coins/ethena", source: "CoinGecko", date: "2026-09-25"}
- {id: 36, title: "Ethena historical data", url: "https://www.coinlore.com/coin/ethena/historical-data", source: "Coinlore", date: "2026-09-24"}
- {id: 37, title: "ENA overview", url: "https://docs.ethena.fi/overview/ena", source: "Ethena Docs", date: "2026"}
- {id: 38, title: "ENA fee switch activation", url: "https://gov.ethenafoundation.com/t/ena-fee-switch-activation/830", source: "Ethena Governance Forum", date: "2026-08-27"}
- {id: 39, title: "Ethena approves protocol fee switch", url: "https://ethdaily.io/ethena-approves-protocol-fee-switch", source: "ETH Daily", date: "2026-09-03"}
- {id: 40, title: "Ethena fee-switch and revenue analysis", url: "https://www.techflowpost.com/en-US/article/34112", source: "TechFlowPost", date: "2026-09-20"}
- {id: 41, title: "Ethena revenue falls 32% in Q1 2026 amid declining TVL and user activity", url: "https://www.kucoin.com/news/flash/ethena-revenue-falls-32-in-q1-2026-amid-declining-tvl-and-user-activity", source: "KuCoin News", date: "2026-04"}
- {id: 42, title: "USDe", url: "https://www.coingecko.com/en/coins/ethena-usde", source: "CoinGecko", date: "2026-09-25"}
- {id: 43, title: "Stablecoin statistics 2026", url: "https://reap.global/blog/stablecoin-statistics-2026", source: "Reap Global (DefiLlama-aggregated)", date: "2026-09-21"}
- {id: 44, title: "Stablecoins API", url: "https://stablecoins.llama.fi/stablecoins", source: "DefiLlama", date: "2026-09-25"}
- {id: 45, title: "Ethena's USDe vaults to No. 3 stablecoin, $9.3 billion supply", url: "https://thedefiant.io/news/defi/ethenas-usde-vaults-to-no-3-stablecoin-9-3-billion-supply-888f0206", source: "The Defiant", date: "2025-08"}
- {id: 46, title: "Resolv stablecoin drops 70% after $80 million exploit", url: "https://www.coindesk.com/markets/2026/03/23/resolv-stablecoin-drops-70-after-usd80-million-exploit-after-attacker-mints-usr", source: "CoinDesk", date: "2026-03-23"}
- {id: 47, title: "Falcon Finance", url: "https://coinmarketcap.com/currencies/falcon-finance/", source: "CoinMarketCap", date: "2026-09-25"}
- {id: 48, title: "USD0", url: "https://app.rwa.xyz/assets/USD0", source: "RWA.xyz", date: "2026-09-25"}
- {id: 49, title: "Ethena Labs: the stablecoin trying to out-Tether Tether", url: "https://fortune.com/crypto/2024/04/19/ethena-labs-stablecoin-synthetic-dollar-tether-circle", source: "Fortune", date: "2024-04-19"}
- {id: 50, title: "Ethena protocol overview (fees and revenue)", url: "https://defillama.com/protocol/ethena", source: "DefiLlama", date: "2026-09-25"}
:::
