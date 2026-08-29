---
eyebrow: MECHANISM DESIGN · UNISWAP
title: "Uniswap's Continuous Clearing Auction: the whitepaper is more honest than the marketing page"
domain: crypto
deck: A block-by-block uniform-price auction is a real improvement on the fixed-price ICO. It is not the end of timing games, and nine months of launches show why that distinction matters.
lede: |
  Uniswap's Continuous Clearing Auction is the most carefully engineered token-sale mechanism the
  industry has shipped. It is also the one whose own authors quietly document the limits its own
  documentation denies. Read the two artifacts side by side and the gap is not a rounding error —
  it is the whole risk surface. Then read the outcomes: $68.6M of realized proceeds in nine months,
  86% of it from a single sale, and a flagship token that has never once traded at the price its
  auction discovered.
stats:
  - {label: Realized proceeds, value: $68.6M, note: all-time, to 2026-08-26}
  - {label: From one sale, value: 86%, note: Aztec, Dec 2025}
  - {label: Trailing 24h, value: $0, note: as of 2026-08-26}
  - {label: AZTEC vs clearing, value: "-69%", note: never traded at clearing}
---

:::kv
- {term: What a CCA is, def: "A uniform-price auction run once per block over a fixed block range, with supply released on a preset schedule and every bidder in a block paying that block's clearing price."}
- {term: What it fixes, def: "The gas-war rationing of fixed-price ICOs and the wait-until-the-end equilibrium of Dutch auctions. Both are real fixes, and both are demonstrable."}
- {term: What it does not fix, def: "Bid shading, demand reduction, and timing games. Uniswap's whitepaper says so explicitly; Uniswap's docs page says the opposite."}
- {term: Where the risk sits, def: "The final block. The clearing price there seeds the Uniswap v4 pool, and Uniswap's own technical docs warn that price is easy to manipulate if the schedule underweights the end."}
- {term: What the evidence shows, def: "Better price discovery for the issuer, worse outcomes for the buyer. Four of six priced CCA tokens trade below clearing; the flagship never reached clearing at all."}
:::

## 01. The mechanism, read from the code rather than the announcement

A Continuous Clearing Auction is a uniform-price auction that settles once per block instead of once at the end. Uniswap's developer documentation defines it as "a novel auction mechanism that generalizes the uniform-price auction into continuous time," and states the settlement rule plainly: "The clearing price of the auction in a block is the price which all bidders in that block pay."[^1]

The moving part is the supply schedule. Total supply is released across a fixed block range according to `auctionStepsData`, a packed byte blob in which each step carries a per-block issuance rate in MPS — milli-bips of total supply, where 1e7 equals 100% — and a block count to run at that rate.[^3] Each block, the released tranche is allocated to the highest max-price bids first, then downward, until the tranche is exhausted; the price at which it is exhausted is that block's clearing price.[^1]

A bidder submits a budget and a max price, not a per-block order. That single distinction carries most of the mechanism's behaviour. The bid is spread automatically across the auction's remaining blocks, so the quantity a bid is exposed to is the supply still unissued at the moment it is submitted.[^2] Capital is escrowed at submission and cannot be recovered early: "A core invariant of the auction is that no bids can be exited before the auction has graduated."[^3]

At the end, the contract compares `currencyRaised` against `requiredCurrencyRaised`. Above the threshold the auction graduates, the issuer sweeps proceeds net of protocol fee, unsold supply returns to the token recipient, and an LBP initializer seeds a Uniswap v4 pool at the final clearing price. Below it, every bidder is refunded in full and the entire supply goes back.[^3][^46] Claiming is a pull, not a push: bidders exit their bid to compute fills, then call `claimTokens`, which anyone may call on any valid bid.[^3]

:::stats
- {label: Supply unit, value: MPS, unit: "1e7 = 100%"}
- {label: Fee unit, value: pips, unit: "1e6 = 100%"}
- {label: Min tick spacing, value: 2}
- {label: Bid exit, value: post-graduation only}
:::

The contracts themselves are unusually clean. The factory declares no owner, no pauser and no proxy; auction parameters — floor price, tick spacing, start and end blocks, graduation threshold, step data, recipients — are constructor-immutable with no setters.[^19][^64] The repository is MIT-licensed, created 2025-07-08, and carries nine audit reports from three firms (Spearbit/Cantina, OpenZeppelin, ABDK) dated August 2025 through June 2026.[^19][^21] The v2.1.0 factory sits at the same CREATE2 address, `0x000000001F26a0044BaA66024e7b6599c61963F8`, on Ethereum, Unichain, Base, Arbitrum, Robinhood Chain and Sepolia.[^22]

What weakens this section: none of the above establishes that the mechanism is *good*, only that it is well-specified and well-reviewed. Specification quality and outcome quality are different questions, and the rest of this piece separates them. That matters because the strongest argument for CCA — and it is a strong one — is precisely that it is legible enough to audit, which almost nothing else in this category is.

## 02. What the whitepaper concedes that the documentation denies

Uniswap publishes two descriptions of the same mechanism — a launch blog post and docs page on one side, a whitepaper on the other[^4] — and they disagree on the three claims that matter most.

The developer documentation says CCA provides fair price discovery "while eliminating timing games and encouraging early participation," that "Sniping and last-minute gaming become ineffective," that "Dutch auctions create timing games and favor professionals over genuine participants," and that "One-shot auctions enable demand reduction and last-minute sniping."[^1]

The whitepaper — eleven authors including Hayden Adams and Columbia Business School's Ciamac Moallemi, plus two from Aztec Labs — says something materially weaker in its Risks and Limitations section.[^2]

:::quote(attr="Continuous Clearing Auctions whitepaper, §4 Risks and Limitations")
"uniform-price formats are not strategy-proof in general and may still admit residual bid shading" · "chunked clearing can concentrate activity near interval boundaries; careful parameterization mitigates but does not eliminate" · "onchain execution inherits network frictions (e.g., MEV, L2/L1 sequencing latency)"
:::

Set the two artifacts side by side and the pattern is consistent: every property the docs page presents as eliminated, the whitepaper presents as mitigated.[^1][^2]

| Claim | Documentation | Whitepaper §4 |
|---|---|---|
| Timing games | "eliminating timing games" | "mitigates but does not eliminate" |
| Demand reduction | one-shot auctions "enable demand reduction" | uniform-price "not strategy-proof in general" |
| *Sniping / MEV* | *"Sniping and last-minute gaming become ineffective"* | *"inherits network frictions (e.g., MEV…)"* |
| End-of-auction risk | not discussed | "underweighting the final chunk—can create manipulation risks" |

This is not a gotcha about marketing copy. It is the single most useful fact about CCA, because it tells you which document to trust when the two conflict, and the answer is the one with the economist on it.

There is a second tell in the whitepaper: its bibliography. Ten references, of which the only classical auction-theory citation is Milgrom and Weber (1982).[^2] There is no Ausubel, no Cramton, no Back and Zender, no Vickrey — that is, no citation to the literature that governs the exact failure mode §4 concedes. The relevant result is Ausubel, Cramton, Pycia, Rostek and Weretka, who establish that differential bid shading in multi-unit auctions "results generically in ex post inefficient allocations," a theorem covering the entire equilibrium set rather than a selected equilibrium.[^10] Their further finding is more awkward still for a uniform-price design: "in settings with symmetric bidders, the pay-as-bid auction often outperforms."[^10]

The counterpoint is fair and worth stating: a protocol whitepaper is not a survey article, and §4 concedes the substance even where the bibliography does not cite it. But the docs page is what a token issuer reads before configuring a sale, and it is the artifact that omits the concession entirely.

## 03. The ratchet, and who a rising clearing price actually pays

The clearing price in a CCA does not fall. The invariant test suite asserts the clearing price is non-decreasing across checkpoints, and independent walkthroughs of the deployed contracts describe the same behaviour: once a block clears at a price, the next block clears at that price or higher.[^19][^29] Uniswap's technical documentation adds the mechanism that produces it — demand above the clearing price does not expire with its block, it rolls forward into the remaining issuance schedule and keeps lifting the price. The docs are explicit that this breaks the naive reading: "Integrators should not assume that a block's issuance is settled at the clearing price of that block alone."[^3]

Combine the ratchet with automatic bid spreading and the incentive is unambiguous. A bid submitted at t=0 is exposed to 100% of the release schedule; a bid submitted after a quarter of supply has been issued is exposed to 75%.[^2][^3] Exposure decreases monotonically in submission time, and price weakly increases in it. Both effects point the same way, so there is no offsetting reason to wait.

That is the honest description of "encouraging early participation." It is a timing game — it simply points at the start of the auction rather than the end. The Dutch auction's pathology was that waiting dominated; CCA's is that rushing dominates. This is genuinely the better failure mode, because a race to be early over a multi-day window is far less capital-efficient to win than a race to be last within one block. But it is not the absence of a race, and the ratchet is a deliberate transfer from late bidders to early ones — a subsidy for speed of access, not a neutral price.

:::callout(kind=warn, label=Farmable)
A guaranteed early-bidder discount plus a price that can only rise is, structurally, a carry trade: fill early at the floor, sell into the later, higher clearing price. Pre-sale analysis flagged exactly this, arguing sophisticated participants would "get in early in the auction and then be first to sell at a later clearing price."[^29] Uniswap's post-hoc statement that no manipulation was detected addresses conduct *during* the auction and does not test the post-graduation leg.[^5]
:::

What would weaken this reading: because bids are immutable and cannot be exited before graduation, the "sell into the ratchet" leg cannot execute inside the auction — it requires the secondary market after the v4 pool opens.[^3] And because all bids inside the first issuance step carry identical exposure, the t=0 race is discretized to "be inside the opening window" rather than "be in the first block," which materially blunts the latency advantage. This is a real design mitigation, not a rhetorical one.

## 04. Against the alternatives, on the record rather than in theory

CCA's comparative case is strongest against the mechanism it most obviously beats, and weakest against the one it is closest to.

**Against the fixed-price ICO, it wins outright.** A capped fixed-price sale with excess demand does not clear a price; it rations first-come-first-served, and that queue position is then re-auctioned in transaction fees. The canonical instance is Basic Attention Token: roughly $35 million in about 30 seconds, with 185 purchases succeeding and over 10,000 failing, the chain congested for three hours, and a single transaction fee peaking around $6,600.[^16] Vitalik Buterin's formulation of the underlying impossibility is that certainty of valuation and certainty of participation cannot both be satisfied.[^16] CCA picks certainty of participation and discovers the price, which is the correct trade for a multi-day sale.

**Against the Dutch auction, the record is mixed but favourable.** Google's 2004 IPO is the canonical reference case: its founders set out in writing the intent to use an auction so that the offering price would reflect broad demand rather than an underwriter's book.[^17] ==Widely-repeated figures for that auction's final pricing and first-day move could not be verified against the founders' letter itself and are omitted here.== The sharper evidence for crypto is revealed preference: Gnosis, which ran the best-known crypto Dutch auction in 2017 (about 5% of GNO supply for $12.5M at an implied valuation above $300M[^16]), later shipped batch-auction contracts whose own README states that "the proposed batch auction system has a number of advantages over dutch auction."[^18] Notably, Gnosis's stated complaint was *undershoot* and blocktime-dependent gas wars, not the FOMO overshoot the popular story assumes — a useful correction to the standard narrative.[^18]

**Against batch auctions, CCA inherits only half the property.** Budish, Cramton and Shim's result is that discrete batching converts speed competition into price competition, and the empirical scale of the problem it addresses is large: Aquilina, Budish and O'Neill measure latency arbitrage at roughly $5 billion a year, a 0.5 basis point tax, and estimate that eliminating it would cut the cost of liquidity by about 17%.[^14][^15] A blockchain block gives you discrete time for free. It does not give you a neutral batch closer, because the entity that closes the batch is the entity that profits from closing it — see §08.

**Against bonding curves, the comparison is barely a contest, but it is also barely relevant.** A large-sample study of 832,941 pump.fun launches found 1,651 graduated — under 0.2%.[^43] That is a different product serving a different buyer, and the honest reading is that CCA does not compete with it.

The strongest counter-argument to CCA's whole comparative case comes from the empirical auction literature, and it is not small. Hortaçsu and McAdams find that switching from a discriminatory to a uniform-price or Vickrey auction "would not significantly increase revenue," bounding bidder surplus gains near 0.02%.[^11] Kang and Puller — studying the only treasury market that actually ran both formats — find the discriminatory auction yielded statistically higher revenue *and* better allocative efficiency.[^12] Hortaçsu, Kastl and Zhang put US Treasury bidder surplus at roughly 3 basis points and efficiency loss at about 2.[^13] The uniform-price family is not the established winner; it is one defensible choice among two, adopted here without the literature being engaged.

## 05. Aztec: the only launch large enough to learn from

The Aztec sale is the reference implementation of CCA in the wild, and nearly everything known about CCA's real behaviour comes from it.

:::timeline
- {date: 2025-11, headline: "CCA announced; Aztec named launch partner", body: "Built with Aztec Labs; whitepaper published with eleven authors including Columbia's Ciamac Moallemi."}
- {date: 2025-12-06, headline: "Aztec auction completes on Ethereum", body: "DefiLlama flags a single $59,240,697 realized-proceeds datapoint labelled 'AZTEC Sale Completed'."}
- {date: 2026-01-28, headline: "Auctions announced for the Uniswap web app", body: "Live on Ethereum, Unichain, Arbitrum and Base."}
- {date: 2026-02-11, headline: "AZTEC TGE; token becomes transferable", body: "Listing price reported at $0.0188 against an auction clearing price near $0.047."}
- {date: 2026-06-16, headline: "v2.0.0 audits published", body: "Spearbit/Cantina and OpenZeppelin; two Medium findings on final-block bid exclusion, both fixed."}
- {date: 2026-06-24, headline: "No-code auction creation ships", body: "Any team can configure and launch a CCA from the Uniswap web app."}
:::

The auction offered 1,547,000,000 AZTEC — about 14.95% of a 10,350,000,000 genesis supply — for ETH, with a per-account cap of 250 ETH under the binding terms, a figure most press reported as 240.[^8] Uniswap reports roughly 17,000 participants who "verified their identities and submitted bids" across 191 countries, with "96% of bidders contributed under $10,000" and a mean contribution "approximately $4,000."[^5] It states the sale "cleared at a price 60% above Aztec's floor price" and that "No clear instances of sniping or automated price manipulation were detected based on onchain data."[^5] Identity verification ran through ZKPassport alongside Predicate.[^5] Aztec reports 19,476 ETH raised from over 16,700 participants; the precise figure of 16,741 comes from contemporaneous reporting rather than the issuer.[^9][^30]

By the standards of a token sale, that is a good distribution outcome, and it should be credited as one. Seventeen thousand verified retail bidders at a $4,000 mean is not what a private round looks like.

Three caveats do real work against the headline, though.

First, the participation statistics are issuer-selected and do not answer the concentration question. No source discloses the largest bidder's share, a top-ten ratio, or how many accounts hit the cap.[^5] The one disclosed concentration figure — "28% of the total token supply went to wallets holding under $100,000" — is measured against *total* supply including insider allocations, not against the 14.95% actually sold.[^5] A 250 ETH cap against a 19,476 ETH raise means one capped account could take roughly 1.3% of the sale, and the cap is per-account, not per-person.[^8]

Second, "60% above floor" is a statement about a floor Uniswap and Aztec chose, not an independent valuation benchmark — and it is denominated in ETH, which fell materially over the auction window, so the USD price discovery was smaller than the headline.[^30]

Third, and most awkward: the graduation threshold appears to have been set to 0 ETH, meaning the auction was guaranteed to graduate regardless of demand.[^57] ==If that parameter reading is correct, "the token graduated" carries no information about demand at all — the sale could not have failed.== The figure comes from a third-party contract read-out rather than an issuer disclosure and should be treated as indicative rather than settled.

## 06. Nine months, $68.6M, and one deal

The adoption picture is where the reporting and the on-chain data diverge most sharply, and the on-chain data is the one to trust.

DefiLlama's adapter for Uniswap Auctions measures what its methodology calls "finalized, withdrawable auction proceeds, not bid budgets."[^6] As of 2026-08-26 it reports $68,584,270 in cumulative realized proceeds, $543,076 in the trailing 30 days, $536,987 in the trailing 7 days, and $0 in the trailing 24 hours.[^6] The single flagged spike, $59,240,697 on 2025-12-06, is labelled "AZTEC Sale Completed."[^6] Every other CCA ever run therefore accounts for roughly $9.3 million of realized proceeds across about nine months.

:::rank-list
- {label: "Aztec (Dec 2025)", value: $59.2M, pct: 100, highlight: true}
- {label: "All other CCAs combined", value: ~$9.3M, pct: 16}
- {label: "Trailing 30 days, all CCAs", value: $543K, pct: 1}
- {label: "Trailing 24 hours", value: $0, pct: 0}
:::

The chain distribution is equally lopsided. Realized proceeds run Ethereum $67,722,311, Arbitrum $465,451, Base $336,010 and Unichain $60,498 — Ethereum is roughly 98.7% of the total, despite the factory being deployed identically across six chains.[^6][^22]

:::donut(center-label="98.7%")
- {label: Ethereum, value: 98.75}
- {label: Arbitrum, value: 0.68}
- {label: Base, value: 0.49}
- {label: Unichain, value: 0.09}
:::

Third-party trackers do not reconcile with this and do not reconcile with each other. CryptoRank's Uniswap CCA launchpad page reports 9 launches and $45.30M raised — a total smaller than Aztec's single sale, which means the aggregate excludes the flagship or measures something else entirely.[^44] The naming picture is similarly muddy: CryptoRank names only five of its nine launches, leaving four unidentified.[^44] ==Treat any published CCA aggregate other than the on-chain adapter as unreliable.==

For scale: Uniswap v4 held roughly $952.5M of TVL against $23.96B of 30-day volume as of 2026-08-26.[^45][^61] CCA's entire all-time realized proceeds are on the order of a single day of Uniswap swap volume. The launchpad is strategically interesting to Uniswap and financially immaterial to it — which is worth saying plainly, because the "Uniswap takes on pump.fun" framing in trade coverage does not survive contact with either number.

The obvious counter: nine months is early, auctions only reached the Uniswap web app in January 2026 and the no-code creation flow only shipped that June,[^38][^39] and the surrounding primary market has been unforgiving: 2026 public token sales have concentrated into a handful of ecosystems, with Ethereum leading at roughly $334M year-to-date as of 2026-08-11.[^49] A mechanism launching into a weak primary market should not be judged on volume alone. That is a genuine defence of the adoption numbers. It is not a defence of the outcome numbers.

## 07. The mechanism worked. The buyers lost.

This is the finding that matters most, and it is not ambiguous.

As of 2026-08-26, AZTEC trades at $0.01468, with a market cap of $43.99M and a fully diluted valuation of $151.94M against 2.996B circulating of 10.35B total.[^7] Its auction cleared near $0.047.[^30][^31] Its listing price on 2026-02-11 was $0.0188 — already 60% below clearing before the first day of open trading ended.[^31]

:::compare
- {role: CLEARING, name: "CCA final price, Dec 2025", value: ~$0.0470}
- {role: HIGHEST, name: "All-time high, 2026-02-20", value: $0.0399}
- {role: SUBJECT, name: "Spot, 2026-08-26", value: $0.01468}
:::

Read the middle card again. AZTEC's all-time high of $0.03990 on 2026-02-20 is *below* its auction clearing price.[^7][^31] The token has never traded at the price the auction discovered — not for a single tick, not on listing day, not at the top. The price path since clearing runs roughly {sparkline:4.70,1.88,3.99,2.18,1.46} in cents: clearing, listing, February peak, March, today.[^7][^31] Its all-time low of $0.01131 was set eight days before this writing, on 2026-08-18.[^7]

The broader CCA cohort is dispersed rather than uniformly bad, and honesty requires saying so.

| Token | Sale | Clearing | Spot (2026-08-26) | vs clearing |
|---|---|---|---|---|
| CAP | Feb / Jun 2026 | $0.01065 (Feb round); Jun auction undisclosed | ~$0.0712 | strongly positive |
| *AZTEC* | *Dec 2025* | *~$0.047* | *$0.01468* | *−69%* |
| OCT (Octra) | Apr 2026 | $0.02881 | ~$0.0211 | −27% |
| IDOS (idOS) | Mar 2026 | ~$0.04 | ~$0.0054 | −87% |
| RNBW (Rainbow) | Feb 2026 | $0.111 | ~$0.0135 | −88% |
| STRATO | Jun 2026 | not disclosed | no public mark located | n/a |

Four of six priced tokens sit below clearing, three of them by 69–88%.[^7][^31][^34][^35][^36,37,62] Rainbow is the sharpest case after Aztec: reporting puts its all-time high, set on TGE day, *below* its clearing price too.[^35] STRATO's auction concluded in June and no public price mark for the token could be located as of 2026-08-26, so its buyers hold a position nobody can value.[^52] Against that, CAP is a clear winner, trading near $0.0712 at a fully diluted valuation around $712M as of 2026-08-26.[^33][^32] ==Aggregators disagree materially on CAP's sale price and raise: ICO Drops prices a February 2026 Uniswap round at $0.01065 and reports no price at all for the June auction, while CryptoRank baselines a different round entirely. Treat the magnitude as contested even though the direction is not.==[^32][^33]

Here is the uncomfortable synthesis. A price-discovery mechanism that works *transfers surplus from the buyer to the issuer*. That is what discovery is for. Aztec cleared 60% above its floor and its buyers are down 69%; those two facts are not in tension, they are the same fact seen from opposite sides of the trade. The 2025 cohort-wide base rate makes the same point without any reference to CCA: of 533 public token sales in 2025, 63 — 11.82% — were trading above their offering price at year end.[^48]

:::statement(attr="ARA Research")
CCA is doing exactly what it was built to do. The question buyers should be asking is not whether the auction was fair, but whether they want to be on the other side of a mechanism designed to leave nothing on the table.
:::

## 08. MEV, the final block, and the one thing CCA cannot fix

CCA has no MEV mitigation of its own. There is no commit-reveal, no encrypted bidding, no private-orderflow integration anywhere in the whitepaper, docs or repository.[^2][^3][^19] Its defences are structural: bids are persistent state spread across all remaining blocks, unfilled demand rolls over, and settlement is uniform within a block.[^3] Those are real and they are load-bearing. Censoring a bid for one block delays it rather than excludes it, so full exclusion would require sustained censorship across a multi-day auction — a much higher bar than the single-slot attack that general proposer-manipulation results describe.[^42]

The residual is the final block, and Uniswap documents it themselves:

:::callout(kind=danger, label="The final block")
"the last block of the auction MUST sell a significant amount of tokens" — because "if only a small number of tokens are sold at the end, the final price will be easy to manipulate."[^3] That final price is what seeds the Uniswap v4 pool. The whitepaper echoes it: "poor shaping—such as underweighting the final chunk—can create manipulation risks near the auction's end."[^2]
:::

This is framed as a configuration requirement, not a protocol invariant. The factory is permissionless and enforces no sane step schedule, so a badly shaped auction can hand its pool-initialization price to whoever controls the last block.[^3][^19] The same is true of tick spacing: the docs warn that too-fine a setting is "extremely gas inefficient, and in specific cases, can result in a DoS attack where the auction cannot finish," and nothing in the factory prevents it.[^3]

The audit record is the best evidence that these are real rather than hypothetical. The Spearbit/Cantina v2.0.0 review reported 10 issues — 0 Critical, 0 High, 2 Medium, 1 Low, 7 Informational — and both Mediums concern a bidder weaponizing the same permissionless force-iteration entrypoint against other bidders — one of them specifically at the marginal clearing tick — with harm maximized in the final biddable block because a rejected bidder cannot retry.[^20][^21] Both were fixed. Note what that finding requires: only a *bidder*, not a builder. A builder with ordering power makes it strictly easier.

Context on who that builder would be: Coin Metrics put Titan Builder at 47.6% and BuilderNet at 26.0% of Ethereum blocks.[^40] Running on Unichain changes this partially — its external block builder operates in a TEE with revert protection — but that covers $60,498 of the $68.6M in realized CCA proceeds.[^41][^6] Essentially every dollar that has moved through a CCA settled on Ethereum L1 with no special sequencing protection.[^6]

Two further exposures deserve naming because nothing in the design addresses them. The protocol places no restriction on the issuing team bidding in its own auction, and the theory says a staged-release auction is exactly the format where self-bidding pays: Komo, Kominers and Roughgarden show a deterministic auction can satisfy only two of {static, strategy-proof, weakly shill-proof}.[^55] And ZKPassport is an eligibility gate, not a sybil gate — it establishes that a document issuer vouched for a holder, which does not cap addresses per person.[^5] Neither is an observed attack on any CCA; both are unmitigated.

## 09. A primary offering, priced in public, with nobody claiming to be the offeror

The legal shape of a CCA is uncomfortable in a way the technical shape is not. An auction that discovers a price for a newly issued token and delivers the proceeds to the issuer is, structurally, a primary offering.

Uniswap Labs' Terms of Service address this by disclaiming every intermediary role: "Uniswap Labs is not the seller, underwriter, or issuer of any tokens distributed through a CCA," it is "not your broker, intermediary, agent, or advisor in connection with any CCA," and it is "not registered with the U.S. Securities and Exchange Commission as a national securities exchange or in any other capacity."[^24] The ToS enumerates no blocked countries; restrictions are sanctions-referential, the United States is not excluded, and governing law is New York.[^24]

Self-characterization has a poor track record here. In both the Telegram and Kik matters, courts assessed the *distribution scheme as a whole* rather than the token in isolation, and integrated a private pre-sale with the subsequent public distribution into a single offering; neither issuer's own labelling survived that analysis.[^59][^60] There is a real tension worth flagging: since 2026-06-24 Uniswap's own web app has offered no-code auction creation, which is issuer-facing origination rather than neutral display.[^39]

The policy environment has moved in issuers' favour, but less than the headlines suggest, and the dates matter.

:::kv
- {term: "CLARITY Act (H.R. 3633)", def: "Reported in Senate 2026-06-01 with a Banking Committee substitute. Not enacted. Its exemptions are conditional and require an offering statement — they are not deregulation."}
- {term: "SEC Regulation Crypto Assets", def: "Rel. 33-11434 / 34-106150, File S7-2026-27. Published in the Federal Register 2026-08-21 as a PROPOSED rule; comments due 2026-10-20. No issuer can rely on it today."}
- {term: Proposed thresholds, def: "Up to $5 million over a four-year period (startup exemption); up to $75 million per 12-month period (fundraising exemption, modeled on Reg A)."}
- {term: Uniswap Labs' own record, def: "SEC Wells notice 2024-04-10, investigation closed with no action per the company on 2025-02-25. The CFTC action was not dropped: $175,000 penalty and cease-and-desist, 2024-09-04."}
:::

Sources: govinfo/GPO for the bill status and the Federal Register release; CFTC Release 8961-24; Uniswap's own blog for the Wells notice and the closure.[^25,26,27,28,63]

Two structural points follow. First, the SEC's proposed regime is organized around *issuers*, not distribution venues — it contains no rule text addressing auctions or launchpads, so the venue question is unaddressed rather than resolved.[^26] Second, the protocol fee is a live problem: CCA reads its fee from an external `ProtocolFeeController`, a single-owner `Ownable` contract with fee rates in pips against a 1,000,000 denominator, and the fee is read at application time rather than at auction creation.[^23] That means the controller's owner can change the rate on auctions already in flight. As of 2026-08-26 no rate is disclosed in the CCA blog posts, developer docs, help-center article or Terms of Service.[^24][^46] A size-bracketed fee skimmed off gross primary proceeds is economically a placement commission regardless of who receives it — and it is undisclosed.

The counter-argument, which is not weak: the contracts governing the auction itself are genuinely unowned and immutable, so this is a narrower centralization than most of DeFi carries, and the fee-controller pattern is standard. But "narrower than most" and "disclosed" are different claims, and only the first is true here.

## 10. What would falsify this

This piece makes three arguments. Each has a specific, checkable thing that would break it.

**"The docs oversell relative to the whitepaper."** This falls if the docs page is updated to match §4's hedging, or if the whitepaper text quoted here is an artifact of the text-extraction proxy used to read the PDF rather than the typeset document.[^2] The quotes are internally consistent and the docs quotes were fetched independently, but the whitepaper was read through a rendering proxy and that is a real limitation.

**"CCA's outcomes are bad for buyers."** This falls on sample size, and the sample is genuinely small: six priced tokens, one of which (CAP) is strongly positive and carries contested sale data across aggregators.[^32][^33] Four of the nine launches in CryptoRank's count remain unidentified, and The Interfold — which CryptoRank scores as the cohort's strongest peak performer — is absent from the table above because no clearing price for it is disclosed anywhere.[^44] A dozen more launches with CAP-like outcomes would invert the finding. The AZTEC-specific claim is more robust — its all-time high sitting below clearing is not a sample-size question — but the cohort claim is provisional and should be re-checked in six months.

**"The final block is CCA's sharpest risk."** This falls if a deployed auction's step schedule back-loads supply heavily enough that the final block is economically un-manipulable, which is exactly what Uniswap's guidance tells issuers to do.[^3] The flagship appears to have done precisely that: a community read-out of Aztec's on-chain parameters shows the final step concentrating roughly 40% of released supply into the closing block, which is the shape the guidance prescribes.[^57] It also weakens considerably on Unichain or any chain with TEE-based sequencing.[^41] No exploit of this surface has been observed on any CCA — the only concrete adversarial findings are the two audit Mediums, both fixed pre-deployment of v2.0.0.[^20]

Two further honest limits. The counterfactual is untestable: nobody knows what Aztec's token would have done under a fixed-price sale or a Dutch auction, and the 2026 market has been hostile to essentially every token launch regardless of mechanism.[^49] And Uniswap's "no manipulation detected" statement is self-reported by an interested party with no disclosed methodology — but no independent skeptical analysis (wallet clustering, sybil audit, concentration study) appears to exist either, so the claim is unrebutted rather than confirmed.[^5]

One thing that survived: an adversarial pass over this piece's three load-bearing claims — the whitepaper-versus-docs contradiction, AZTEC's all-time high sitting below clearing, and the DefiLlama concentration figures — searched specifically for disconfirming sources and found none. All three were independently reproduced against the primary artifacts, including a second, different extraction of the whitepaper PDF that resolves the proxy-rendering caveat above.[^1][^2][^6][^7] Red-team pass: 3 of 3 unbroken.

:::callout(kind=info, label="Net assessment")
CCA is the best-specified token-sale mechanism currently shipping, and the improvement over the fixed-price ICO is real and demonstrable. It does not eliminate timing games, it relocates them from the end of the auction to the beginning, and its authors say so in the whitepaper. Nine months in, it has moved $68.6M — 86% of it once — and its flagship token has never traded at the price it discovered. Both of those things can be true, and both are.
:::

:::references
- {id: 1, title: "Continuous Clearing Auction — concepts", url: "https://developers.uniswap.org/docs/liquidity/liquidity-launchpad/concepts/cca", source: Uniswap developer documentation, date: "2026-08-26"}
- {id: 2, title: "Continuous Clearing Auctions (whitepaper)", url: "https://developers.uniswap.org/whitepaper_cca.pdf", source: "Adams, Karys, Liu, Zhong, Kocsis, Gretzke, Wan, Toda, Andrews, Moallemi", date: "2025-11-30"}
- {id: 3, title: "CCA Technical Documentation", url: "https://raw.githubusercontent.com/Uniswap/continuous-clearing-auction/main/docs/TechnicalDocumentation.md", source: Uniswap GitHub, date: "2026-08-26"}
- {id: 4, title: "Continuous Clearing Auctions: Bootstrapping Liquidity on Uniswap v4", url: "https://blog.uniswap.org/continuous-clearing-auctions", source: Uniswap Labs blog, date: "2025-11-13"}
- {id: 5, title: "Aztec's Continuous Clearing Auction", url: "https://blog.uniswap.org/aztec-cca", source: Uniswap Labs blog, date: "2026-02-10"}
- {id: 6, title: "Uniswap Auctions — realized auction proceeds", url: "https://api.llama.fi/summary/dexs/uniswap-auctions?dataType=dailyVolume", source: DefiLlama, date: "2026-08-26"}
- {id: 7, title: "Aztec (AZTEC) price and market data", url: "https://www.coingecko.com/en/coins/aztec", source: CoinGecko, date: "2026-08-26"}
- {id: 8, title: "Aztec auction terms and conditions", url: "https://aztec.network/auction-terms-conditions", source: Aztec Network, date: "2025-11-12"}
- {id: 9, title: "Aztec TGE and next steps", url: "https://aztec.network/blog/aztec-tge-next-steps", source: Aztec Network, date: "2025-12-08"}
- {id: 10, title: "Demand Reduction and Inefficiency in Multi-Unit Auctions", url: "https://ideas.repec.org/a/oup/restud/v81y2014i4p1366-1400.html", source: "Ausubel, Cramton, Pycia, Rostek & Weretka, Review of Economic Studies 81(4)", date: "2014-10-01"}
- {id: 11, title: "Mechanism Choice and Strategic Bidding in Divisible Good Auctions", url: "https://ideas.repec.org/a/ucp/jpolec/doi10.1086-657948.html", source: "Hortacsu & McAdams, Journal of Political Economy 118(5)", date: "2010-10-01"}
- {id: 12, title: "Comparing Auction Designs Where Suppliers Have Uncertain Costs and Uncertain Pivotal Status", url: "https://s-puller.github.io/MyWebsite/Kang_Puller_JIE.pdf", source: "Kang & Puller, Journal of Industrial Economics 56(2)", date: "2008-06-01"}
- {id: 13, title: "Bid Shading and Bidder Surplus in the US Treasury Auction System", url: "https://www.aeaweb.org/articles?id=10.1257/aer.20160675", source: "Hortacsu, Kastl & Zhang, American Economic Review 108(1)", date: "2018-01-01"}
- {id: 14, title: "The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response", url: "https://ideas.repec.org/a/oup/qjecon/v130y2015i4p1547-1621.html", source: "Budish, Cramton & Shim, Quarterly Journal of Economics 130(4)", date: "2015-11-01"}
- {id: 15, title: "Quantifying the High-Frequency Trading Arms Race", url: "https://ericbudish.org/files/Quantifying-the-High-Frequency-Trading-Arms-Race.pdf", source: "Aquilina, Budish & O'Neill, Quarterly Journal of Economics 137(1)", date: "2022-02-01"}
- {id: 16, title: "Analyzing Token Sale Models", url: "https://vitalik.eth.limo/general/2017/06/09/sales.html", source: Vitalik Buterin, date: "2017-06-09"}
- {id: 17, title: "2004 Founders' IPO Letter", url: "https://abc.xyz/investor/founders-letters/2004-ipo-letter/", source: "Alphabet (Google) investor relations", date: "2004-08-18"}
- {id: 18, title: "Gnosis IDO contracts (batch auction) README", url: "https://github.com/gnosis/ido-contracts", source: Gnosis, date: "2021-01-01"}
- {id: 19, title: "Uniswap continuous-clearing-auction repository", url: "https://github.com/Uniswap/continuous-clearing-auction", source: Uniswap GitHub, date: "2026-08-24"}
- {id: 20, title: "Spearbit/Cantina security review of Uniswap Liquidity Launcher v2.0.0", url: "https://github.com/Uniswap/continuous-clearing-auction/blob/main/docs/audits/Spearbit_v2.0.0.pdf", source: Spearbit/Cantina, date: "2026-06-16"}
- {id: 21, title: "CCA audit index", url: "https://github.com/Uniswap/continuous-clearing-auction/blob/main/docs/audits/README.md", source: Uniswap GitHub, date: "2026-06-16"}
- {id: 22, title: "Liquidity Launchpad deployment addresses", url: "https://developers.uniswap.org/docs/liquidity/liquidity-launchpad/deployments", source: Uniswap developer documentation, date: "2026-08-26"}
- {id: 23, title: "ProtocolFeeController.sol", url: "https://github.com/Uniswap/liquidity-launcher/blob/main/src/periphery/ProtocolFeeController.sol", source: "Uniswap liquidity-launcher repository", date: "2026-08-26"}
- {id: 24, title: "Uniswap Labs Terms of Service", url: "https://support.uniswap.org/hc/en-us/articles/30935100859661", source: Uniswap Labs, date: "2026-07-28"}
- {id: 25, title: "H.R. 3633 — Digital Asset Market Clarity Act, Reported in Senate", url: "https://www.govinfo.gov/app/details/BILLS-119hr3633rs", source: "U.S. Government Publishing Office", date: "2026-06-01"}
- {id: 26, title: "Regulation Crypto Assets (proposed rule), Rel. Nos. 33-11434; 34-106150", url: "https://www.govinfo.gov/content/pkg/FR-2026-08-21/html/2026-17183.htm", source: "Federal Register / U.S. Securities and Exchange Commission", date: "2026-08-21"}
- {id: 27, title: "CFTC Orders Uniswap Labs to Pay $175,000 Penalty", url: "https://www.cftc.gov/PressRoom/PressReleases/8961-24", source: "U.S. Commodity Futures Trading Commission, Release 8961-24", date: "2024-09-04"}
- {id: 28, title: "A win for DeFi", url: "https://blog.uniswap.org/a-win-for-defi", source: Uniswap Labs blog, date: "2025-02-25"}
- {id: 29, title: "Want to win the Aztec sale? Study the mechanism", url: "https://research.auditless.com/p/want-to-win-the-aztec-sale-study", source: Auditless Research, date: "2025-12-02"}
- {id: 30, title: "Aztec raises $59 million in token sale with Uniswap's CCA", url: "https://unchainedcrypto.com/aztec-raises-59-million-in-token-sale-with-uniswaps-cca/", source: Unchained, date: "2025-12-08"}
- {id: 31, title: "Aztec ICO details and ROI", url: "https://icodrops.com/aztec/", source: ICO Drops, date: "2026-08-26"}
- {id: 32, title: "CAP ICO details and ROI", url: "https://icodrops.com/cap-3/", source: ICO Drops, date: "2026-08-24"}
- {id: 33, title: "CAP price and market data", url: "https://cryptorank.io/price/cap", source: CryptoRank, date: "2026-08-26"}
- {id: 34, title: "Octra (OCT) price and market data", url: "https://www.coingecko.com/en/coins/octra", source: CoinGecko, date: "2026-08-26"}
- {id: 35, title: "Rainbow (RNBW) price and IDO data", url: "https://cryptorank.io/price/rainbow", source: CryptoRank, date: "2026-08-26"}
- {id: 36, title: "idOS (IDOS) price and IDO data", url: "https://cryptorank.io/price/idos", source: CryptoRank, date: "2026-08-26"}
- {id: 37, title: "idOS public sale results", url: "https://www.idos.network/blog/public-sale-results", source: idOS, date: "2026-03-05"}
- {id: 38, title: "Token auctions are coming to the Uniswap web app", url: "https://blog.uniswap.org/token-auctions-are-coming-to-the-uniswap-web-app", source: Uniswap Labs blog, date: "2026-01-28"}
- {id: 39, title: "Launch auctions from the Uniswap web app", url: "https://blog.uniswap.org/launch-auctions-from-uniswap-web-app", source: Uniswap Labs blog, date: "2026-06-24"}
- {id: 40, title: "State of the Network, Issue 356", url: "https://coinmetrics.substack.com/p/state-of-the-network-issue-356", source: Coin Metrics, date: "2026-03-24"}
- {id: 41, title: "Unichain mainnet: TEE block building", url: "https://writings.flashbots.net/unichain-mainnet", source: Flashbots, date: "2025-05-02"}
- {id: 42, title: "Censorship-Resistant Sealed-Bid Auctions on Blockchains", url: "https://arxiv.org/html/2606.14939", source: "Alpos, Heimbach, Nayak & Wadhwa, arXiv:2606.14939", date: "2026-06-12"}
- {id: 43, title: "An empirical study of the pump.fun bonding-curve launchpad", url: "https://arxiv.org/html/2607.02823", source: arXiv, date: "2026-07-01"}
- {id: 44, title: "Uniswap CCA fundraising platform page", url: "https://cryptorank.io/fundraising-platforms/uniswap-cca", source: CryptoRank, date: "2026-08-26"}
- {id: 45, title: "Uniswap v4 total value locked", url: "https://api.llama.fi/tvl/uniswap-v4", source: DefiLlama, date: "2026-08-26"}
- {id: 46, title: "What are Continuous Clearing Auctions?", url: "https://support.uniswap.org/hc/en-us/articles/43107626487437-What-are-Continuous-Clearing-Auctions", source: Uniswap Labs help center, date: "2026-08-23"}
- {id: 48, title: "2025 public token sale performance review", url: "https://www.panewslab.com/en/articles/e21d9785-6cff-4ae6-9991-ad564c45c1f9", source: "PANews, citing CryptoRank", date: "2025-12-31"}
- {id: 49, title: "Ethereum leads 2026 public token sales race", url: "https://www.cryptotimes.io/2026/08/11/ethereum-leads-2026-public-token-sales-race-with-334m/", source: "The Crypto Times, citing CryptoRank", date: "2026-08-11"}
- {id: 52, title: "STRATO auction page", url: "https://strato.nexus/auction", source: STRATO, date: "2026-06-11"}
- {id: 55, title: "Shill-Proof Auctions", url: "https://arxiv.org/abs/2404.00475", source: "Komo, Kominers & Roughgarden, arXiv:2404.00475", date: "2025-12-31"}
- {id: 57, title: "Aztec CCA on-chain parameter read-out", url: "https://hackmd.io/SCfjYNHQTmuRl2adnFi2oA", source: "Community contract read-out (NocturnusCoder)", date: "2025-12-02"}
- {id: 59, title: "Court Sides with SEC in Blocking Distribution of Telegram's Grams", url: "https://www.wilmerhale.com/en/insights/client-alerts/20200406-court-sides-with-sec-in-blocking-distribution-of-telegrams-grams", source: WilmerHale, date: "2020-04-06"}
- {id: 60, title: "Court Holds That Kik ICO Was an Unregistered Securities Offering and That Reg D Private Placement Should Be Integrated with Public Offering", url: "https://www.sewkis.com/publications/court-holds-that-kik-ico-like-telegram-was-an-unregistered-securities-offering-and-that-reg-d-private-placement-should-be-integrated-with-public-offering/", source: "Seward & Kissel", date: "2020-09-30"}
- {id: 61, title: "Uniswap v4 volume summary", url: "https://api.llama.fi/summary/dexs/uniswap-v4", source: DefiLlama, date: "2026-08-26"}
- {id: 62, title: "Octra (OCT) IDO price and market data", url: "https://cryptorank.io/price/octra", source: CryptoRank, date: "2026-08-26"}
- {id: 63, title: "Fighting for DeFi", url: "https://blog.uniswap.org/fighting-for-defi", source: Uniswap Labs blog, date: "2024-04-10"}
- {id: 64, title: "ContinuousClearingAuctionFactory.sol", url: "https://github.com/Uniswap/continuous-clearing-auction/blob/main/src/ContinuousClearingAuctionFactory.sol", source: Uniswap GitHub, date: "2026-08-26"}
:::
