---
eyebrow: REPORT · CRYPTO MARKET STRUCTURE
title: "Verifiable is not the same as fair: does Lighter answer Don Wilson's five questions about Hyperliquid onshore?"
deck: A trader-advisor's thread says a ZK-proven perp exchange dissolves the objections to bringing Hyperliquid-style markets under US rules. The primary sources say it answers one question well, two partly, and leaves two where Wilson put them.
domain: crypto
lede: |
  On 2026-10-30 Don Wilson, founder of DRW and Cumberland, thanked the CFTC chairman for "experimentation" and then asked five hard questions about a plan to put Hyperliquid-based perpetuals under US regulation.[^2] A day later Will Price, publicly described as a Lighter advisor, replied that Lighter, a zero-knowledge-proven perp exchange, already has the answers: everything is verifiable, an escape hatch protects users, there are "no priority fees", and the only inefficiency is a small, falling proof cost.[^1][^36] We checked each claim against Lighter's documentation, L2BEAT's independent analysis, Hyperliquid's own docs, the Commodity Exchange Act and CFTC releases, and market data. The result is more interesting than a rebuttal: Lighter's design is a serious answer to a question Wilson did not ask.
---

:::callout(kind=info, label="Direct answer")
- **Premise check:** the deal is ICE operating Trade[XYZ]'s regulated markets, "built on Hyperliquid", pending unnamed approvals, and the release does not say where matching will run.[^3]
- **"No priority fees":** true of an auction, false of speed. Lighter's Standard taker waits 300 ms; the opt-in Premium account waits 140 ms and pays fees.[^9]
- **"Escape hatch":** real and independently reproduced, but L2BEAT rates Lighter Stage 0, with a 14-day forced-transaction deadline and upgrades that a council can make instant.[^12][^13]
- **"Easy privacy":** no Lighter privacy roadmap was found, and the one deployed encrypted-data precedent, Paradex, has no generic escape hatch.[^17]
- **"Small, falling proof cost":** plausible for Ethereum settlement given what is posted, but unquantified; proving compute is undisclosed, and proof lag is minutes.[^12]
:::

## 01. The premise is looser than the thread

**Thesis: the question both men are debating is narrower, and less settled, than "NYSE brings Hyperliquid onshore."**

Wilson's post refers to "@NYSE working to bring @HyperliquidX onshore."[^2] The primary source is an Intercontinental Exchange release dated 2026-10-29: a definitive agreement with Trade[XYZ] under which ICE becomes "the exclusive operator" of Trade[XYZ]'s regulated markets, builds a retail market and clearing structure separate from its institutional futures business, and takes a minority stake, all "subject to regulatory approvals".[^3] The release names no regulator and no registration category, gives no launch date, and says customers would be KYC/AML-verified and reach the venue through futures commission merchants.[^3]

Trade[XYZ] is not Hyperliquid. It is a builder that deploys markets under Hyperliquid's HIP-3 framework, and today matching, positions and settlement run on HyperCore, Hyperliquid's on-chain engine.[^4] HIP-3 deployers must keep 500,000 HYPE staked.[^7] ICE says the new structure will be "built on Hyperliquid", but where order matching will physically occur is not stated.[^3] That matters because Wilson's questions about public positions, priority fees and on-chain matching all assume the answer is "on HyperCore." If the regulated venue matches in an ICE engine and borrows only product design, three of his five questions largely dissolve, and so does the relevance of Lighter's architecture to this particular deal.

:::timeline
- {date: 2026-05-15, headline: "CME and ICE press regulators", body: "Bloomberg-sourced reporting says both raised insider-trading and manipulation risks on Hyperliquid's commodity perps."}
- {date: 2026-05-26, headline: "Wilson's FT op-ed on front-running", body: "He argues the choice of blockchain is a market-structure decision and favors privacy and limited pre-trade visibility."}
- {date: 2026-05-29, headline: "CFTC approves Kalshi BTCPERP", body: "First true perpetual approved as a futures contract under Reg. 40.3."}
- {date: 2026-10-29, headline: "ICE and Trade[XYZ] agreement", body: "Definitive agreement, pending approvals, no regulator named."}
- {date: 2026-10-30, headline: "Wilson's five questions", body: "Posted 14:44 UTC; 88,920 views at fetch."}
- {date: 2026-10-31, headline: "Price's reply", body: "Posted 19:09 UTC; 27,878 views at fetch."}
:::

Sources for the timeline: [^29][^26][^19][^20][^3][^2][^1].

A disclosure belongs next to the reply. Bankless identified Price on 2026-06-02 as "a DeFi investor and Lighter advisor" who argued LIT was underpriced.[^36] The article does not say whether he holds the token. That does not make his technical claims wrong, but it makes them an advocate's claims, and we test them as such.

**Counterpoint.** ICE's own history cuts the other way: five months before the deal, ICE and CME were reported pressing regulators about Hyperliquid, citing "insider trading and price manipulation risks."[^29] The agreement may reflect a changed assessment, or a retail business ICE intends to wall off; the release says only that the perp markets are "additive to our futures markets."[^3]

**Why it matters:** an analysis of whether Lighter "answers" Wilson has to hold the venue design fixed, and today the design is unspecified.

## 02. The five questions, scored

**Thesis: Price's reply is strongest where it describes Lighter and weakest where it claims to answer a regulator's question.**

Wilson's five questions, in his words, ask: what the benefit is of trading perps on-chain on a regulated exchange, given that atomic receipt "obviously isn't helpful" for something that "is not an asset"; whether the sponsor knows that on Hyperliquid "the world will be able to track your positions and trades in real time"; whether paid priority fits CFTC core principles; whether offshore and onshore liquidity could be combined; and, if not, whether a traditional centralized order book would avoid "the inefficiencies that on-chain matching introduces."[^2] Price's five-point reply covers verifiability and the escape hatch, optional privacy, the absence of priority fees, the technical feasibility of merging books, and centralized-but-fast matching.[^1]

| Wilson's question | Price's reply | What the primary sources show | Our score |
|---|---|---|---|
| 1. Benefit of on-chain on a regulated venue | Verifiable; escape hatch | Escape hatch is independently reproduced but Stage 0, 14-day trigger[^12][^13] | Partly answered |
| 2. Public positions | Privacy could be added | No Lighter privacy roadmap found; encrypted-DA precedent breaks exit[^17] | Not answered |
| 3. Priority fees vs core principles | "No priority fees" | No auction, but latency is sold in tiers[^9] | Partly answered |
| 4. Merge onshore and offshore books | Feasible; regulators decide | Statute and rules make it a legal, not technical, question[^25] | Agreed, trivially |
| 5. Why not a plain CLOB? | Matching is centralized and fast | Price-time priority matching with soft finality, plus later proofs[^16][^10] | Conceded, in effect |

The last row is the most revealing. Price writes that Lighter's matching engine is centralized and that speed is not traded against security.[^1] Lighter's own documentation confirms a price-time priority system,[^16] and its architecture page describes the sequencer as providing "soft finality" before proofs land.[^10] That is close to the "traditional centralized order book" Wilson proposed in question 5, with a validity proof layered behind it. The honest reading is that Lighter does not refute the on-chain-matching critique; it routes around it by not matching on-chain.

**Why it matters:** the debate is usually framed as on-chain versus off-chain. Lighter's architecture suggests a third category, centralized matching with decentralized verification, whose trust assumptions are different from both.

## 03. "No priority fees": Hyperliquid sells speed explicitly, Lighter sells it by account tier

**Thesis: both venues let participants pay for speed; they differ in whether the price is an auction or a menu.**

Wilson is right that Hyperliquid has priority fees. Two mechanisms are documented. Order priority is a per-order rate, charged from undelegated staked HYPE as a fraction of filled notional for immediate-or-cancel orders; latency improves linearly from 0 to 8 basis points, at roughly 45 ms per basis point, and higher rates only break ties inside a 70 ms bucket.[^5] Passive orders pay a rate on resting notional, sorted within a 400 ms window, and the fee is charged whether or not the order fills.[^5] Cancels always go ahead of executable orders, and the fees are burned rather than paid to validators.[^5] Gossip priority is a separate Dutch auction, re-run every three minutes, that buys about 25 ms of earlier read access per slot, resetting to ten times the prior winning price with a floor of 0.1 HYPE.[^5] Secondary coverage dates the launch to 2026-04-13.[^43]

The docs page restricts order priority only to orders on a "non-outcome asset"; secondary reports describe it as limited to HIP-3 markets, and we could not reconcile the two.[^5][^43] That ambiguity matters for the ICE deal, because Trade[XYZ] is a HIP-3 deployer.[^4]

Lighter has no gas-style auction. But its fee page shows that speed is sold:

:::bar-chart(title="Lighter taker latency by account type", subtitle="Milliseconds of added delay before a taker order is processed; docs fetched 2026-11-01", orientation=horizontal, value-suffix=" ms")
categories: Standard (0% fee), Plus (0.5 bp fee), Premium (fee + LIT discount)
Taker latency: 300, 300, 140
:::

Standard accounts pay 0% maker and 0% taker but carry a 300 ms delay on takers and on cancel or modify requests; makers carry none. The opt-in Premium account cuts taker latency to 140 ms for 0.0280% (2.8 bp) taker and 0.0040% maker fees, discounted up to 30% by staking 500,000 LIT.[^9] One critic estimated the Standard tier's total cost at 6 to 12 bp, but that is opinion with no data behind it.[^37]

:::kv
- {term: "Hyperliquid order priority", def: "Per-order rate paid in HYPE, up to 8 bp buys ~45 ms per bp; fee burned; cancels always first"}
- {term: "Hyperliquid gossip priority", def: "3-minute Dutch auction for ~25 ms earlier data; floor 0.1 HYPE; burned"}
- {term: "Lighter Standard", def: "0 / 0 fees; takers and cancels delayed 300 ms; makers 0 ms"}
- {term: "Lighter Premium", def: "0.0040% maker / 0.0280% taker; takers delayed 140 ms"}
:::

So "no priority fees" is accurate about the mechanism and misleading about the economics. Both venues publish the price of speed, which is the property a regulator would most care about; neither hides it. The substantive differences are that Hyperliquid's version is continuous, per order and burned, while Lighter's is a standing account election whose fees are revenue.[^5][^9]

**Counterpoint.** Wilson's real objection may be to any paid advantage on an order book, whatever its form, and a latency tier is arguably the more discriminatory design because it is attached to the account and not to the order.

**Why it matters:** "no priority fees" is a slogan; the compliance question is whether paid speed is published, uniformly available and surveilled.

## 04. What the CFTC text actually says about paid priority, merged books and public positions

**Thesis: nothing in the core principles prohibits priority fees by name; three hooks could constrain them, and merging books is a legal rather than a technical problem.**

The statutory core principles for designated contract markets do not mention paid priority or latency access.[^21] Three provisions carry the weight. Regulation 38.151 requires access criteria that are "impartial, transparent, and applied in a non-discriminatory manner" and "comparable fee structures" for equal access.[^22] Core Principle 9 requires "a competitive, open, and efficient market and mechanism for executing transactions."[^23] Core Principle 12 requires rules "to promote fair and equitable trading."[^21] Core Principle 7 requires the execution mechanism itself to be published.[^21] A flat, published, universally available priority tier is arguably consistent with all four; a discretionary or bilateral tier is the real exposure. This is our legal reading from the primary text, not a CFTC position, and we found no CFTC guidance on priority fees.

On public positions, the law cuts against Wilson's framing less than he implies. The CFTC itself may not publish data that would "separately disclose the business transactions or market positions of any person," and large-trader reports flow to it daily,[^24][^45] but those provisions bind the Commission, not a venue's order-book design. No rule we retrieved requires a public order book, and the rulebook standard is publication of the rules and mechanisms, not of positions.[^46] The constraint on wallet-level transparency is therefore commercial and ethical, not statutory.

On merging liquidity, a foreign board of trade cannot permit direct access to its matching system from the US without registration under Part 48.[^25] The CFTC's existing bridge is intermediated: per Dechert's summary, staff Letter 26-17 allows Coinbase's futures commission merchant to offer offshore perps as foreign futures and accept digital commodities or stablecoins as margin at a foreign affiliate.[^20] The agency also approved Kalshi's BTCPERP on 2026-05-29 under Regulation 40.3, found it consistent with the core principles, noted the design "may not be suitable for all asset classes," and invited other perpetual submissions.[^19] Price is right that regulators would decide a merger of books; the more precise statement is that a shared book would need every participant identified and routed through registered intermediaries, so "merge" would mean the offshore side adopts KYC, not that onshore adopts offshore.[^1][^25]

:::stats
- {label: "Core-principle hooks for priority fees", value: "3", note: "38.151 access, CP9 open/efficient, CP12 fair/equitable"}
- {label: "CFTC perp approval", value: "2026-05-29", note: "Kalshi BTCPERP, Reg. 40.3"}
- {label: "Hooks found that name paid priority", value: "0", note: "ARA reading of retrieved text"}
:::

**Counterpoint.** Our reading rests on fragments of statute and rule that the retrieval returned; Part 39 clearing conditions, CEA 2(i) and FinCEN rules were not retrieved and could bind more tightly.

**Why it matters:** a priority-fee design is defensible if it is published, uniform and surveilled; "no priority fees" is not a legal safe harbor, and "merge the books" is a KYC question.

## 05. Verifiability and the escape hatch: what the proofs guarantee, and what they cannot

**Thesis: Lighter's exit guarantee is real, independently tested and bounded, and "no need to trust the operator" overstates it.**

Lighter's documentation says each batch carries "a new post-execution state along with a succinct cryptographic proof," and that the data posted as blobs is enough to rebuild user states.[^10] L2BEAT's independent analysis, dated 2026-05-22, found the mechanism sound: if the operator stops processing a forced priority transaction for 14 days, anyone can freeze the L1 contract into desert mode, users prove their account's balance against the last committed state root, and the contract releases funds.[^13] L2BEAT rebuilt the verifier bytecode "byte-for-byte" and reproduced the state root from blobs alone across about 5,000 batches.[^13] That is a stronger check than most exchanges ever face.

The boundaries are specific. Open positions "cash-settle at the last published mark price," and live orders and matching-engine state are lost.[^13] The primary oracle feed's signatures are "not currently verified onchain."[^13] The operator "can ignore a new order, front-run it, or reorder it in the queue."[^13] L2BEAT rates Lighter Stage 0, lists three permissioned operator addresses, and shows that regular upgrades have a 21-day delay but that a 4-of-7 Security Council can reduce it to zero, which L2BEAT flags as critical; 91 upgrades had occurred at fetch time.[^12] L2BEAT called upgrades "the biggest unresolved exposure."[^13] The forced L1 queue includes reduce-only IOC orders, order cancellation, withdrawals and share burns, and the L1 messaging contract was scheduled to change on 2026-11-08.[^11]

:::stats
- {label: "Forced-transaction deadline", value: "14", unit: "days", note: "before desert mode can be triggered"}
- {label: "Regular upgrade delay", value: "21", unit: "days", note: "Security Council 4/7 can cut to zero"}
- {label: "L2BEAT rating", value: "Stage 0", note: "exit window: None"}
- {label: "Avg proof interval", value: "3m41s", note: "state updates ~6m53s"}
:::

An independent audit of the block circuits by zkSecurity found two high-severity bugs, one of which would let a malicious prover create an account with arbitrary collateral; all but one finding were fixed.[^14] The same report shows the client relied on the sequencer to enforce a cancel-all time bound off-circuit.[^14] These facts are consistent with a well-audited system and with the claim that proofs bind the operator to valid state transitions. They are inconsistent with a claim that trust in the operator is unnecessary, because ordering, inclusion timing, oracle prices and upgrade authority all remain operator-controlled.

**Counterpoint.** A proof system that ensures the operator cannot steal funds through invalid transitions is a material improvement over a conventional exchange, and the escape hatch has no analogue on Hyperliquid.

**Why it matters:** "verifiable" is a statement about state transitions, not about fairness of ordering; Wilson's own concern about the order in which transactions are processed is untouched by the proofs.[^26]

## 06. Public positions and the privacy claim

**Thesis: transparency has documented costs, but "easily add privacy without affecting the escape hatch" is an unsupported design claim, not a feature.**

Hyperliquid positions are queryable by address with no authentication.[^48] The documented costs are real. An autopsy of the 2025-10-10 crash put total market-wide liquidations above $19B.[^40] In March 2025 the JELLY episode left Hyperliquid's vault with roughly $12M of unrealized losses at the outset, and validators force-settled the market at $0.0095 and delisted it.[^44] A market-maker infrastructure founder relayed that a top Hyperliquid maker rotates strategies every three weeks because they get copied; that is hearsay from a vendor selling a private venue.[^39] Wilson's own proposed remedy in his May op-ed was privacy and limited pre-trade visibility, not abandoning chains.[^26]

Price's proposal is to encrypt posted data with each trader's public key while keeping trades, volume and open interest public and positions hidden.[^1] The mechanics are harder than the sentence suggests. In Lighter's exit design, users rebuild state from public blobs and prove their own account against it.[^10][^13] Settlement uses shared marks and the global state root.[^13] The nearest deployed precedent for encrypted posted data, Paradex, posts encrypted blobs under a symmetric key itself encrypted to a three-member council; L2BEAT records that any one member can decrypt and that "there is no generic escape hatch mechanism."[^17] StarkEx's perpetual exit shows the other side of the coupling: the withdrawable amount is computed from the vault's position and the prices of all assets in the last batch, and in validium mode users need data held by a committee.[^18] We found no Lighter roadmap for privacy: its docs mention only "modularity for data privacy" in general terms.[^10]

**Counterpoint.** A per-user key scheme is not impossible: each user could retain their own encrypted state and prove it at exit, but then liquidation, insurance-fund and deleveraging logic that depend on other users' positions must run inside zero-knowledge circuits whose scope has not been described for Lighter. No published design we found does this with a permissionless exit.

**Why it matters:** privacy is the answer an institution like DRW would most want, which is exactly why the claim needs a design, not an adjective.

## 07. Is the proof cost "small and falling"?

**Thesis: the Ethereum-side design is frugal, but the cost a venue actually bears, proving compute, is not disclosed.**

Lighter posts per-account state differences as blobs, not per-trade records; placing and cancelling orders are proven but not posted.[^15][^49] Ethereum raised blob capacity through the Fusaka upgrade and later blob-parameter-only forks, while also adding an execution-linked floor under the blob base fee,[^41] so the posting cost is bounded below as well as cheap. L2BEAT lists Lighter's recurring Ethereum transactions as batch commits, proof verifications and batch executions, but its cost chart is interactive and we could not retrieve a verified dollar total for them.[^12] We also found no Lighter disclosure of its off-chain proving compute; its proofs rest on custom Plonky2 circuits wrapped in a Plonk-based proof that needs a trusted setup, per L2BEAT.[^12] The design makes a low settlement cost plausible, and the audit trail confirms what is posted, but "small and falling" remains unquantified.[^15]

The cost that does show up in the public record is latency, not dollars. L2BEAT records average intervals of about 3m40s for batch submission, 3m41s for proofs and 6m53s for state updates, with a stall of more than four hours on 2026-10-29.[^12] Lighter's architecture page describes sequencer-provided "soft finality" until a proof lands.[^10] The verifiable measurement of Price's "inefficiency" is therefore minutes of proof lag, not a dollar cost.

:::callout(kind=warn, label="Data caveat")
Dollar figures for Lighter's settlement and proving cost circulate in search summaries, but we could not trace them to a fetched primary page and have left them out.
:::

**Counterpoint.** Proof lag is a latency to finality, not a cost to the trader, who is matched immediately by the sequencer; a venue could reasonably call minutes of settlement lag cheap.

**Why it matters:** Wilson's question 5 asks about inefficiency; the verifiable figure is minutes of proof lag and an unexplained four-hour stall, not a dollar cost.

## 08. Scale and incentives: how big is the thing being compared

**Thesis: Hyperliquid is roughly three to four times Lighter on the common measures, and Lighter's late-2025 volume surge was followed by a sharp decline.**

Secondary reports citing DefiLlama put thirty-day perp volume on 2026-10-15 at roughly $209.5B for Hyperliquid and $62.7B for Lighter, with open interest of $7.70B against $711M.[^30]

:::rank-list
- {label: "Hyperliquid (30d volume, $B)", value: "209.5", pct: 100, highlight: true}
- {label: "Lighter", value: "62.7", pct: 30}
- {label: "Aster", value: "54.9", pct: 26}
- {label: "edgeX", value: "30.2", pct: 14}
- {label: "ApeX Omni", value: "12.9", pct: 6}
:::

Source: coincentral, citing DefiLlama as of 2026-10-15; the article is promotional for ApeX.[^30] Another snapshot as of about 2026-09-28 gives a wider set that includes Variational and GRVT:[^31]

:::donut(center-label="$598B 30d")
- {label: "Hyperliquid", value: 34.1}
- {label: "Aster", value: 10.9}
- {label: "Lighter", value: 8.8}
- {label: "Variational", value: 8.5}
- {label: "edgeX", value: 6.2}
- {label: "ApeX", value: 4.4}
- {label: "GMX", value: 3.8}
- {label: "GRVT", value: 2.4}
- {label: "Not itemised", value: 20.9}
:::

The shares are ARA arithmetic on the snapshot's venue volumes over its stated $597.8B total.[^31] Reports put Lighter's 30-day volume ahead of Hyperliquid's around the end of 2025, with sources disagreeing on the size of the gap, and well behind it by September 2026.[^50] Lighter's retail trading was zero-fee, and a 21Shares note in October 2025 warned that incentive-driven perp volume across the sector raised the possibility of wash trading, applying its 70:1 volume-to-TVL flag to Aster rather than Lighter.[^33] After Lighter's token launched on 2025-12-30, reports describe daily volume falling from above $10B to about $2-4B.[^34] Sector volume roughly halved from the October 2025 peak, by ForkLog's count.[^32] The 2025-10-10 crash also knocked Lighter offline for about 4.5 hours after a database failure, with over 2,000 affected users and a liquidity-pool loss.[^35]

**Counterpoint.** Lighter's drop after the token launch is also what removing farmers should look like, and its later volume would then be more organic; no independent wash-trading study of either venue was found.

**Why it matters:** the comparison is between a venue that dominates volume and has the live regulated-deal optionality, and one with a better exit guarantee and a smaller, incentive-shaped book.

## 09. What could break this thesis

**Thesis: our own conclusion is exposed to four failures.**

First, the venue design. If the ICE market matches off Hyperliquid, Wilson's questions about public positions and on-chain inefficiency become moot and the comparison changes.[^3] Second, the law. We read the core principles from fragments, and a CFTC staff position on priority fees could tighten or relax everything in section 04; none was found.[^22][^23] Third, the data. Several figures are secondary, including the volume snapshots, and the X posts themselves were read through a mirror API; the Hyperliquid docs restrict priority to "non-outcome" assets while press says HIP-3 only.[^5][^43] Fourth, timing. Lighter's L1 messaging contract is due to change on 2026-11-08, and its upgrade delay is already conditional.[^11][^12]

What would falsify the headline: a Lighter privacy design that keeps a permissionless exit; an ICE venue that matches on HyperCore and publishes a priority-fee rulebook the CFTC accepts; or a Lighter incident in which desert mode is triggered and works.

:::callout(kind=success, label="Red-team status")
Red-team pass: 3/3 top claims unbroken. An adversarial reviewer tried to contradict the three load-bearing claims (the ICE release names no regulator and no matching venue; Lighter's Standard taker waits 300 ms against Premium's 140 ms; Lighter is L2BEAT Stage 0 with a 14-day forced-transaction deadline and council-shortenable upgrade delay) and found no contradicting primary or secondary source. Its one open lead was an unconfirmed report that ICE deleted its own social post about the deal on 2026-10-31 while the investor-relations release stayed live.
:::

:::references
- {id: 1, title: "Will Price (@will__price) reply, x.com/will__price/status/2116608448930697658 (read via FxTwitter mirror)", url: "https://api.fxtwitter.com/will__price/status/2116608448930697658", source: "X via FxTwitter", date: "2026-10-31"}
- {id: 2, title: "Don Wilson (@drwconvexity) five questions, x.com/drwconvexity/status/2116179494163615996 (read via FxTwitter mirror)", url: "https://api.fxtwitter.com/drwconvexity/status/2116179494163615996", source: "X via FxTwitter", date: "2026-10-30"}
- {id: 3, title: "ICE and Trade[XYZ] to bring Hyperliquid-based perpetual markets onshore", url: "https://ir.theice.com/press/news-details/2026/Intercontinental-Exchange-and-TradeXYZ-to-Bring-Hyperliquid-Based-Perpetual-Markets-Onshore/default.aspx", source: "ICE investor relations", date: "2026-10-29"}
- {id: 4, title: "Trade[XYZ]: relationship to Hyperliquid", url: "https://docs.trade.xyz/overview/relationship-to-hyperliquid.md", source: "Trade[XYZ] docs"}
- {id: 5, title: "Hyperliquid docs: priority fees", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/priority-fees", source: "Hyperliquid docs", date: "2026-11-01"}
- {id: 6, title: "Hyperliquid docs: fees", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees", source: "Hyperliquid docs", date: "2026-11-01"}
- {id: 7, title: "HIP-3: builder-deployed perpetuals", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals", source: "Hyperliquid docs", date: "2026-11-01"}
- {id: 8, title: "Hyperliquid docs: HyperCore overview", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/overview", source: "Hyperliquid docs", date: "2026-11-01"}
- {id: 9, title: "Lighter docs: trading fees and latency", url: "https://docs.lighter.xyz/trading/trading-fees.md", source: "Lighter docs", date: "2026-11-01"}
- {id: 10, title: "Lighter docs: technical architecture", url: "https://docs.lighter.xyz/about-lighter/technical-architecture-lighter-core.md", source: "Lighter docs", date: "2026-11-01"}
- {id: 11, title: "Lighter docs: priority transactions", url: "https://docs.lighter.xyz/developers/reference/priority-transactions.md", source: "Lighter docs", date: "2026-11-01"}
- {id: 12, title: "L2BEAT: Lighter", url: "https://l2beat.com/scaling/projects/lighter", source: "L2BEAT", date: "2026-11-01"}
- {id: 13, title: "L2BEAT Research: Exchange risk and how Lighter escapes it", url: "https://l2beat.com/publications/exchange-risk-and-how-lighter-escapes-it", source: "L2BEAT", date: "2026-05-22"}
- {id: 14, title: "zkSecurity: zkLighter block circuits audit", url: "https://reports.zksecurity.xyz/reports/zklighter-block/", source: "zkSecurity"}
- {id: 15, title: "zkSecurity: zkLighter wrapper audit", url: "https://reports.zksecurity.xyz/reports/zklighter-wrapper.md", source: "zkSecurity"}
- {id: 16, title: "Lighter docs: order types and matching", url: "https://docs.lighter.xyz/trading/order-types-and-matching.md", source: "Lighter docs", date: "2026-11-01"}
- {id: 17, title: "L2BEAT: Paradex", url: "https://l2beat.com/scaling/projects/paradex", source: "L2BEAT", date: "2026-11-01"}
- {id: 18, title: "StarkEx data availability", url: "https://docs.starkware.co/starkex/con_data_availability.html", source: "StarkWare docs"}
- {id: 19, title: "CFTC release 9240-26: Kalshi BTCPERP order", url: "https://www.cftc.gov/PressRoom/PressReleases/9240-26", source: "CFTC", date: "2026-05-29"}
- {id: 20, title: "CFTC takes historic steps to bring digital asset perpetual contracts onshore", url: "https://www.dechert.com/knowledge/onpoint/2026/6/cftc-takes-historic-steps-to-bring-digital-asset-perpetual-contr.html", source: "Dechert", date: "2026-06-09"}
- {id: 21, title: "7 U.S.C. 7: designated contract market core principles", url: "https://www.law.cornell.edu/uscode/text/7/7", source: "Cornell LII"}
- {id: 22, title: "17 CFR 38.151: access requirements", url: "https://www.law.cornell.edu/cfr/text/17/38.151", source: "Cornell LII"}
- {id: 23, title: "17 CFR 38.500: execution of transactions", url: "https://www.law.cornell.edu/cfr/text/17/38.500", source: "Cornell LII"}
- {id: 24, title: "7 U.S.C. 12: CFTC confidentiality of positions", url: "https://www.law.cornell.edu/uscode/text/7/12", source: "Cornell LII"}
- {id: 25, title: "17 CFR 48.3: foreign boards of trade", url: "https://www.law.cornell.edu/cfr/text/17/48.3", source: "Cornell LII"}
- {id: 26, title: "How some blockchains enable front-running (FT op-ed)", url: "https://drw.com/updates/insights/financial-times-how-some-blockchains-enable-front-running", source: "DRW", date: "2026-05-26"}
- {id: 27, title: "Wilson says regulators are getting crypto's biggest trading innovation wrong", url: "https://www.coindesk.com/markets/2026/07/28/wall-street-veteran-don-wilson-says-regulators-are-getting-crypto-s-biggest-trading-innovation-all-wrong", source: "CoinDesk", date: "2026-07-28"}
- {id: 28, title: "CFTC tokenized collateral initiative", url: "https://www.cftc.gov/PressRoom/PressReleases/9130-25", source: "CFTC", date: "2025-09-23"}
- {id: 29, title: "ICE, CME press US regulators to rein in Hyperliquid", url: "https://cointelegraph.com/news/ice-cme-press-us-regulators-rein-hyperliquid-dex", source: "Cointelegraph", date: "2026-05-15"}
- {id: 30, title: "Best perp DEXes in 2026 compared", url: "https://coincentral.com/best-perp-dexes-in-2026-hyperliquid-aster-lighter-edgex-and-apex-omni-compared/", source: "CoinCentral", date: "2026-10-22"}
- {id: 31, title: "Perp DEX landscape 2026: volume, architecture, ranking", url: "https://www.gate.com/learn/articles/perp-dex-landscape-2026-volume-architecture-ranking", source: "Gate Learn"}
- {id: 32, title: "Perp DEX trading volumes plummet over 50% since October", url: "https://forklog.com/en/perp-dex-trading-volumes-plummet-over-50-since-october/", source: "ForkLog", date: "2026-04-06"}
- {id: 33, title: "The perpetual DEX wars", url: "https://www.21shares.com/research/the-perpetual-dex-wars-hyperliquid-aster-and-lighter-in-focus", source: "21Shares", date: "2025-10-06"}
- {id: 34, title: "Lighter perp DEX faces sharp decline amid TGE fallout", url: "https://www.kucoin.com/news/flash/lighter-perp-dex-faces-sharp-decline-amid-tge-fallout", source: "KuCoin News", date: "2026-01-14"}
- {id: 35, title: "Lighter DEX to repay users in stablecoins after major outage", url: "https://ambcrypto.com/lighter-dex-to-repay-users-in-stablecoins-after-major-outage-details/amp/", source: "AMBCrypto", date: "2025-10-15"}
- {id: 36, title: "Is LIT the most underpriced perps bet in crypto?", url: "https://www.bankless.com/read/is-lit-the-most-underpriced-perps-bet-in-crypto", source: "Bankless", date: "2026-06-02"}
- {id: 37, title: "Zero fees is just a marketing number (Lighter latency)", url: "https://www.chaincatcher.com/en/article/2229046", source: "ChainCatcher", date: "2025-12-12"}
- {id: 38, title: "Wilson's questions on ICE and Hyperliquid", url: "https://www.chaincatcher.com/en/article/2300505", source: "ChainCatcher", date: "2026-10-30"}
- {id: 39, title: "Market makers shift to private exchanges to conceal strategies", url: "https://www.kucoin.com/news/flash/market-makers-shift-to-private-exchanges-to-conceal-trading-strategies", source: "KuCoin News", date: "2026-04-12"}
- {id: 40, title: "The ultimate 10/10 crash autopsy", url: "https://thedefiant.io/newsletter/defi-daily/the-ultimate-10-10-crash-autopsy", source: "The Defiant"}
- {id: 41, title: "Fusaka: blob parameters", url: "https://www.growthepie.com/quick-bites/fusaka", source: "growthepie"}
- {id: 42, title: "Hyperliquid 24h and 30d volume, 2026-10-07", url: "https://cryptonews.net/news/market/33553295/", source: "cryptonews.net", date: "2026-10-07"}
- {id: 43, title: "The third option: Hyperliquid priority fee", url: "https://www.coinlive.com/news/the-third-option-hyperliquid-priority-fee", source: "Coinlive", date: "2026-06-05"}
- {id: 44, title: "Hyperliquid delists JELLYJELLY amid whale manipulation", url: "https://www.theblock.co/post/348314/hyperliquid-delists-jellyjelly-memecoin-amid-whale-manipulation-fiasco", source: "The Block", date: "2025-03-26"}
- {id: 45, title: "17 CFR 17.00: large trader reports", url: "https://www.law.cornell.edu/cfr/text/17/17.00", source: "Cornell LII"}
- {id: 46, title: "17 CFR 38.401: disclosure of rules", url: "https://www.law.cornell.edu/cfr/text/17/38.401", source: "Cornell LII"}
- {id: 47, title: "Coinbase Markets has landmark year", url: "https://www.marketsmedia.com/coinbase-markets-has-landmark-year/", source: "Markets Media", date: "2026-01-12"}
- {id: 48, title: "Hyperliquid info endpoint: perpetuals", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals", source: "Hyperliquid docs"}
- {id: 49, title: "The Lighter system architecture", url: "https://dyb.mataroa.blog/blog/the-lighter-system-architecture/", source: "dyb blog"}
- {id: 50, title: "Perp DEX wars: Hyperliquid, Lighter, Aster", url: "https://arx.trade/blog/perp-dex-wars-hyperliquid-lighter-aster/", source: "ARX", date: "2026-03-30"}
:::
