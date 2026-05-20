---
eyebrow: REPORT · CRYPTO × AI
title: "Venice ($VVV): a real AI business wired to a reflexive token machine"
deck: Three million users and genuine inference revenue, governed by a single company through a two-token loop that is cleverer — and more circular — than the marketing admits.
domain: crypto
lede: |
  Venice ($VVV) is the rarest object in crypto-AI: a token bolted to a
  product that millions of people actually use. The app — a privacy-first,
  deliberately uncensored AI front-end built by ShapeShift founder Erik
  Voorhees — passed three million registered users in May 2026. But the
  ~$800M token wrapped around that product is governed by no one except the
  company, runs on a contract with no published audit, and is increasingly
  priced as a function of itself. This report separates the business that is
  real from the tokenomics that are reflexive — and finds both halves
  stranger than the pitch.
stats:
  - {label: VVV price, value: $17.29, note: "+18.5% on the day, 2026-05-20"}
  - {label: Market cap, value: $799M}
  - {label: FDV, value: $1.38B}
  - {label: Holders, value: "134,774"}
  - {label: Registered users, value: 3M, note: "May 2026"}
  - {label: VVV staked, value: "~69%", note: "of circulating"}
---

## 01. The thesis in one screen

Most token "utility" stories collapse on contact with a browser: the product is a slide, the users are airdrop farmers, the revenue is zero. Venice is the exception that makes the genre interesting. The underlying app is a working, privacy-first AI service — chat, image, video, and an OpenAI-compatible API — that crossed three million registered users in May 2026[^16][^21] and serves 230+ models[^21]. The $VVV token that funds it trades at $17.29 with a circulating market cap near $799M and a fully-diluted valuation around $1.38B.[^2][^4]

{accent}The tension is the whole story.{/} Venice the *business* is real, growing, and revenue-funded.[^7] Venice the *token system* is a centrally-controlled, inflationary, two-token reflexive loop with no governance[^1] and no contract audit on file.[^3] A buyer is purchasing exposure to both at once, and the pitch blurs them deliberately.

The price path captures the whiplash: a launch-day spike to $22.58, a year underwater, then a ~17× recovery off the December-2025 floor. {sparkline:3.10,2.83,1.97,1.52,1.02,1.64,2.33,5.43,8.57,17.15}

This report works through, in order: what holders actually experienced; the real cap table; the staking-and-DIEM engine; the true emissions-and-burn accounting; whether the product is as big as claimed; where VVV sits among peers; and the securities question that hangs over the whole design.

## 02. The launch, and what holders actually lived through

$VVV launched on Coinbase's Base L2 on 27 January 2025 as an explicit "fair launch" — no pre-sale, no venture round — with half the genesis supply earmarked for an airdrop.[^1] Within roughly two hours the token's fully-diluted valuation crossed $1B,[^34] and Coinbase listed it spot the same day.[^34] That is where the clean narrative ends.

The airdrop required claiming, and most of it was never claimed. When the 45-day window shut on 13 March 2025, only ~17.4M VVV had been claimed by ~40,000 wallets; the ~32.6M unclaimed tokens — worth roughly $100M at the time — were burned.[^6] A 35%-ish claim rate is itself a verdict: the "100,000+ users" the airdrop targeted[^1] mostly did not show up to collect.

Price action was brutal for anyone who held. The all-time high of $22.58 printed on 28 January 2025; within five days VVV had fallen ~86% to about $3.10.[^2] It then spent more than a year grinding through low single digits, bottoming at an all-time low of $0.9197 on 1 December 2025[^2] before a sector-wide AI-token rally, exchange listings, and the burn narrative drove a violent recovery into May 2026.[^33]

:::line-chart(title="VVV monthly close, USD", subtitle="GeckoTerminal (Base VVV/WETH); Feb–Apr 2025 approximate", y-unit=$)
x: 2025-02,2025-03,2025-04,2025-05,2025-06,2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05
VVV: 3.10,2.70,3.00,2.83,2.98,2.73,2.78,1.97,1.52,1.02,1.64,2.33,5.43,6.53,8.57,17.15
:::

The single most important framing for a new buyer: even after a ~17× rally off the floor,[^5] VVV at $17.29 is still ~24% below its day-two peak.[^2] The "down only" early holders and the "up only" December-2025 buyers are the same token, twelve months apart.

:::compare
- {role: LOWEST, name: "All-time low (Dec 2025)", value: $0.92}
- {role: HIGHEST, name: "All-time high (Jan 2025)", value: $22.58}
- {role: SUBJECT, name: "Now (May 2026)", value: $17.29}
:::

Counterpoint to the bear read: the recovery is not purely reflexive sentiment. It coincides with a step-change in exchange access — an Upbit listing across KRW, BTC, and USDT pairs on 12 May 2026[^33], part of a broader May listing wave. {flag:yellow} But Korean and broker listings are *access* events, not fundamentals; the timing of the May spike maps onto them almost exactly, which is the signature of a liquidity-driven move rather than a re-rating of cash flows. Why it matters: a buyer today is paying a price set largely by a fresh retail-access wave, not by Venice's (undisclosed) earnings.

## 02b. A note on the "team dump" allegation

One launch-week controversy deserves a flag rather than a verdict. Analysts alleged in January 2025 that the team issued itself ~$5.7M of VVV through a fresh multisig wallet and sold ~$450k after the Coinbase listing, contributing to a ~50% drop.[^34] ==Unverified: this allegation was never confirmed by Venice and rests on third-party wallet analysis.== It belongs in the record because the launch's optics — instant top-exchange listing, a centrally-held treasury — created exactly the conditions in which such claims thrive.

## 03. The cap table: a fair launch with an owner's switch

The genesis supply was 100,000,000 VVV, distributed at the token-generation event as 50% airdrop, 35% to the Venice.ai company, 10% to an incentive fund, and 5% to liquidity[^1] — with the team's 10% carved *inside* the 35% company grant (25% unlocked at TGE, the rest streaming over 24 months).[^1] Read as five buckets, it sums cleanly to 100M:

:::donut(center-label="100M VVV")
- {label: Airdrop (users + Base AI protocols), value: 50}
- {label: Venice.ai company treasury, value: 25}
- {label: Team (25% TGE, rest over 24mo), value: 10}
- {label: Incentive fund, value: 10}
- {label: Liquidity, value: 5}
:::

The "fair launch / no-VC" claim is technically true and rhetorically slippery. There was genuinely no pre-sale and no venture allocation,[^1] which distinguishes VVV from the typical insider-heavy launch. But "fair" does not mean "decentralized": half the supply was retained by the company, team, and treasury,[^1] and the Venice.ai company is the single largest holder.[^1] The company itself is bootstrapped — Voorhees has said Venice took no external venture funding[^19] — so the token, not equity, is the de-facto capital base. The airdrop itself split 25M to 100,000+ Venice users and 25M to a basket of Base AI protocols (VIRTUALS, AERO, DEGEN, AIXBT, GAME, LUNA, VADER, CLANKER, and Morpheus/MOR).[^1]

The fact the marketing buries: VVV is explicitly **not** a governance token. Venice's own launch post states "No governance," and the protocol's economic parameters — emissions, burns, the DIEM mint curve — are all set unilaterally by the company.[^1] On-chain, the token contract is verified but carries "No Contract Security Audit Submitted" on Basescan,[^3] and security scanners flag an owner-controlled `mint()` with no hard cap.[^3] The "fixed, deflationary 100M" framing is therefore a *policy commitment by the team*, not a property enforced by code.

:::kv
- {term: Token, def: "VVV — ERC-20 on Base (0xacfE…21bf)"}
- {term: TGE, def: "2025-01-27 — fair launch, no pre-sale, no VC"}
- {term: Genesis supply, def: "100,000,000 VVV"}
- {term: Governance, def: "None — company retains full control"}
- {term: Largest holder, def: "Venice.ai company (35% grant)"}
- {term: Contract audit, def: "None submitted on Basescan"}
:::

Why this matters: every downstream "value-accrual" story — staking yield, buy-and-burn, the DIEM peg — depends on the continued discretionary cooperation of one private company. That is not a flaw the market has priced; it is the precondition of the whole machine. {flag:yellow}

## 04. The engine: staking for inference, and the DIEM loop

The original utility was elegant: stake VVV and receive a daily, non-consumable claim on Venice's inference capacity, proportional to your share of active stakers — stake 1% of the active pool, get ~1% of the network's daily capacity (~18,148 "Diem" of compute per day), refreshed at midnight UTC, with a 7-day unstake cooldown.[^8] You kept your tokens (the "diamond" model) and earned inference instead of burning credits.

The flaw was reflexive, and the founder said so plainly:

:::quote(attr="Erik Voorhees, Venice founder, Aug 2025")
The amount of free inference received was determined by the capacity supply divided pro rata among all stakers. This amount naturally fluctuates, which made it difficult for stakers to plan long-term.
:::

The fix — DIEM, launched 20 August 2025 — did not remove the reflexivity; it engineered it into a second token.[^9][^11] You lock staked VVV to *mint* DIEM, a tradeable ERC-20 where **1 DIEM = $1/day of API credit, forever**, while your locked VVV still earns 80% of normal staking yield; burn DIEM to unlock the VVV.[^9] The catch is the mint curve: `Mint Rate = 90 × e^(2 × (supply ÷ 38,000)³)`, so each additional DIEM costs exponentially more VVV to mint.[^10] As of May 2026, roughly 7–9M VVV — ~15% of circulating supply — sits locked to back ~38,250 DIEM, up from ~6.3M locked in January.[^12][^31][^13]

:::stats
- {label: DIEM price, value: $1,795, note: "ATH $1,884 on 2026-05-19"}
- {label: Per DIEM, value: $1, unit: "/day", note: "API credit, perpetual"}
- {label: Simple payback, value: 4.9, unit: "yrs"}
- {label: Implied yield, value: "20.3%", note: "if fully consumed"}
- {label: VVV locked, value: "~15%", note: "of circulating supply"}
:::

Here is the non-obvious finding. The scary "death-spiral" reading — DIEM up → more VVV locked → float down → VVV up → each VVV mints a more valuable claim — is real on the demand side but heavily *self-damping*, and the arbitrage currently runs backwards. At ~38,250 DIEM outstanding, the *marginal* mint rate is ~693 VVV per DIEM; at $16.92/VVV that is ~$11,726 to mint one DIEM that trades for ~$1,795.[^13][^31] Minting is ~6.5× more expensive than simply buying DIEM on the open market — so the "lock-and-mint-to-sell" flywheel is switched off at spot prices, and the cube exponent chokes off supply growth before any blow-off.[^10]

The genuine consumer math is sobering, though. Buying one DIEM at ~$1,795 to consume $1/day of inference is a ~4.9-year payback — an implied ~20.3% perpetual yield only if you fully use the credit every day, forever, and Venice stays solvent.[^13] At today's price the "savings vs. paying cash for the API" is negative; what you are really buying is price exposure plus the option to resell. (DIEM is thinly traded, so its quoted price varies by tracker.) Counterpoint: a new yield leg appeared on 15 May 2026, when AntSeed launched a peer-to-peer market letting DIEM holders pool their credit and earn streaming USDC as it powers Venice inference[^35] — which, if it scales, gives DIEM a cash return beyond self-consumption. Why it matters: the loop's stability rests on the curve math, not on a peg that can break LUNA-style — locking is reversible by burning DIEM.

## 05. Emissions and burns: the real deflation accounting

The headline number does the most work and the least honest work: "over 33.7M VVV burned, ~42.9% of the original 100M supply."[^7] True — and almost entirely a one-time event. Of that cumulative burn, ~32.6M was the single March-2025 incineration of unclaimed airdrop tokens.[^6][^7] The *ongoing*, revenue-funded program is tiny by comparison: Venice's own buy-and-burn post discloses only ~180k VVV (~$1.35M) removed via discretionary buybacks since November 2025.[^7]

:::bars
- {label: "One-time unclaimed-airdrop burn (Mar 2025)", value: "32.6M", pct: 100}
- {label: "All ongoing buy-and-burn (Nov 2025 →)", value: "~1.1M", pct: 3}
:::

The programmatic per-subscription burn — every new Pro signup auto-triggering a VVV buy-and-burn — only launched on 15 April 2026, initially at ~$1 per Pro (~$1,000/day), later scaled to $2 / $5 / $10 across the Pro, Pro+, and Max tiers.[^7][^37] Against an ~$800M market cap, that is real but immaterial today; the "net deflationary by July 2026" goal is a forecast, not a fact.[^15]

On the supply side, emissions are uncapped by design but glide downward on a schedule Venice has actually executed, announced step-by-step on its official account:

:::timeline
- {date: 2025-01, headline: "14M VVV/yr at genesis", body: "Starting inflation ~14%, declining over time."}
- {date: 2025-08, headline: "Cut to 10M/yr", body: "Alongside the DIEM launch."}
- {date: 2025-11, headline: "Cut to 8M/yr", body: "Announced Oct 7 in the 'Venice is Burning' thread."}
- {date: 2026-02, headline: "Cut to 6M/yr", body: "Effective Feb 10, 2026."}
- {date: 2026-05, headline: "Cut to 5M/yr", body: "Effective May 1, 2026."}
- {date: 2026-06, headline: "Cut to 4M/yr", body: "Scheduled June 1, 2026."}
- {date: 2026-07, headline: "Cut to 3M/yr", body: "Scheduled July 1, 2026."}
:::

The schedule is genuine and well-documented across primary sources, from the 14M genesis rate[^1] through every cut.[^30][^14][^15] But two caveats restrain the deflation thesis. First, with ~69% of circulating VVV staked,[^31] holders must keep re-staking simply to avoid dilution — the "yield" is in large part defense against the very emissions that fund it. Second, the burns that would make VVV net-deflationary are still an order of magnitude below emissions in dollar terms.[^7][^15] Why it matters: the "deflationary AI token" narrative driving the 2026 rally is mostly *prospective*; the realized burn to date is a launch-cleanup line item.

## 06. Is the product actually real? Mostly yes — with two opaque spots

This is where Venice earns its valuation more than most. The app launched publicly in July 2024[^20] and reports an accelerating adoption curve: the first million users took 13 months, the second 7, the third just 3 — reaching 3M by 16 May 2026.[^16] Independent web-traffic estimates corroborate the direction: ~9.9M monthly visits in April 2026, up ~15.5% month-on-month.[^22]

:::stats
- {label: Registered users, value: 3M, note: "13 → 7 → 3 mo per million"}
- {label: Models served, value: "230+", note: "text, image, video, audio"}
- {label: Monthly web visits, value: 9.9M, note: "+15.5% MoM (Similarweb)"}
- {label: Venice Pro, value: $18, unit: "/mo", note: "no VVV required"}
- {label: Refusal rate, value: "2.2%", note: "vs 71% Claude (self-reported)"}
:::

The product is genuinely differentiated on privacy and permissiveness: prompts are not stored or logged server-side, chats live in the local browser, and Venice's uncensored model posts a self-reported 2.2% refusal rate against 71% for Claude and 64% for GPT-4o-mini.[^23] Crucially, the consumer business is a normal SaaS line — Pro is $18/month, fiat-purchasable, and requires no VVV at all[^21] — which means real revenue exists independent of the token. In May 2026 Venice also shipped agentic chat and an official MCP server exposing 31 tools, widening the product from chatbot toward agent platform.[^16]

Two opacities keep this from being a clean bull case. **First, revenue is undisclosed.** No public source — including Voorhees — gives a hard revenue or paying-subscriber figure; "3M users" is cumulative registrations, not MAU or payers.[^16] **Second, the "decentralized GPU compute" claim is unverified:** Venice has never named its providers, their count, or how they are paid, and confidential-compute (TEE) is described as research, not production. The "uncensored" capability is itself largely upstream IP — its flagship Venice Uncensored model derives from Eric Hartford's Dolphin lineage and is trained on Targon, Bittensor's Subnet 4[^32] — so the headline feature is reproducible by anyone serving the same open weights. Counterpoint: none of that negates the usage, which is the hardest thing to fake; it just means the moat is brand, UX, and distribution, not proprietary models. Why it matters: you can verify the users far better than you can verify the margins.

## 07. Where it sits: composing, not just competing

Ranked by token market cap, VVV sits mid-pack in the crypto-AI complex — well below Bittensor, ahead of the GPU-marketplace and agent tokens:

:::rank-list
- {label: "Bittensor (TAO)", value: "$2.51B", pct: 100}
- {label: "Render (RENDER)", value: "$938M", pct: 37}
- {label: "Venice (VVV)", value: "$799M", pct: 32, highlight: true}
- {label: "Akash (AKT)", value: "$219M", pct: 9}
- {label: "io.net (IO)", value: "$48M", pct: 2}
- {label: "Morpheus (MOR)", value: "$19.6M", pct: 1}
:::

But "competitor" is the wrong frame for half this list.[^32] Venice *composes* with the strongest crypto-native players rather than fighting them: it trains its uncensored model on Bittensor's Targon subnet,[^32] sources that model from the Dolphin/Cognitive Computations lineage,[^32] and routes distribution through OpenRouter's developer network.[^23] Venice owns the consumer-facing demand-and-burn layer; TAO, its subnets, and the model providers own the compute-and-weights layer.

The real competition is on two narrower fronts. On the crypto side, Bittensor's inference subnets (Chutes, Targon) could in principle disintermediate Venice's API.[^32] On the mainstream side, neutral routers like OpenRouter, Together, and Groq can serve the *same* open weights with their own "we don't log" policy — which is why the privacy/uncensored pitch is a feature, not a moat.[^23] The defensible core is the combination a clone cannot copy: Voorhees's distribution, a polished product doing real volume, and an installed staking base that makes the token flywheel actually spin. Why it matters: VVV's token value is downstream of demand the *brand* generates, and that demand is the one input no fork can replicate.

## 08. The securities question: a bad blueprint in a good climate

Strip away the branding and VVV staking looks uncomfortably like an investment contract. Run the Howey prongs against it:

| Howey prong | Applies to VVV staking? | Why |
|---|---|---|
| Investment of money | Yes | Acquire and commit VVV (purchased or airdropped-then-staked). |
| Common enterprise | Yes | Shared emissions pool; buy-and-burn funded by Venice's revenue lifts all holders. |
| Expectation of profit | Strong (yield) / weak (pure compute use) | 14–18% staking APY and a deflation narrative vs. genuine inference consumers. |
| Efforts of others | Strongest | Venice runs the API and sets emissions, burns, and the DIEM curve; "No governance." |

The "efforts of others" prong is where VVV is most exposed: profit depends wholly on an identified, centralized promoter, and the explicit "No governance" design removes any decentralization defense.[^1] Worse, the SEC's 29 May 2025 staff statement that protocol staking generally is not a securities transaction[^25] explicitly *excludes* assets that "generate a passive yield or convey rights to future income, profits, or assets of a business enterprise."[^24] VVV staking pays a passive yield and conveys a claim on a company-operated revenue service — landing squarely in the carve-out. The September-2025 DoubleZero no-action letter, the safe path for "utility" tokens, rewards participant effort and de-minimis issuer discretion[^26] — the two things VVV most lacks.

:::callout(kind=warn, label="Bottom line")
On the doctrine, VVV staking-for-yield has the **worst securities profile in its cohort** — passive yield, rights to a centralized firm's future income, profit from the promoter's efforts, and no governance. The DIEM-as-consumed-compute path has a real but narrow utility defense that does not rescue the staking product.
:::

Yet the *practical* risk is low, because the enforcement climate inverted. The 2025–26 SEC under Chair Atkins dismissed its marquee crypto cases (Coinbase, with prejudice), closed most investigations, dropped crypto from its 2026 exam priorities, and shifted to rulemaking over enforcement.[^27] A March-2026 joint SEC/CFTC interpretation further raised the bar for finding a security.[^36] Peers signal the same drift: Grayscale filed an S-1 for a Bittensor (TAO) ETP in December 2025, the regulator engaging via registration, not enforcement.[^29] Prediction markets put the CLARITY market-structure bill at ~55% to be signed into law in 2026 — a coin-flip statutory off-ramp.[^28] The residual exposure is fraud/disclosure, where Voorhees's 2014 SEC settlement over SatoshiDICE (a $15,843.98 disgorgement plus a $35,000 penalty and a multi-year bar) makes him a salient repeat actor if anything goes wrong.[^18][^17] Why it matters: VVV carries the highest intrinsic securities risk in its peer set while operating in the most forgiving window the sector has seen — a latent, timing-dependent risk, not a present one.

## 09. What would break the thesis

A report this favorable to the *product* owes the reader the disconfirming cases. The strongest:

**The token is a centralized company's IOU, not a protocol.** Utility evaporates the moment Venice stops operating the API; there is no governance, no on-chain enforcement, and no recourse.[^1] Even bullish holders concede the asset is worth "$1/day of inference for as long as Venice exists." A keyman event around Voorhees, a treasury compromise (no published multisig disclosure, no audit), or a simple business failure zeroes the utility floor.[^3]

**The deflation story is mostly backward-looking.** ~97% of the celebrated burn was a one-time 2025 airdrop cleanup;[^6][^7] ongoing burns remain an order of magnitude below emissions in dollar terms.[^7] If the AI-token rally fades, the supply story alone will not hold the price.

**The DIEM premium is not utility — it is speculation.** A ~4.9-year payback for self-consumed inference[^13] means the marginal DIEM buyer is paying for VVV-lockup reflexivity, not compute savings. If DIEM demand reverses, the unlock dynamics are stickier than the lock dynamics, and ~15% of VVV float is structurally illiquid.[^31]

**The "uncensored" stance is a copyable feature with uncapped legal tail risk.** The capability is upstream open weights;[^32] meanwhile an explicitly permissive AI invites CSAM, defamation, and app-store/payment-rail exposure that is structural even though no major incident is yet documented.

**Red-team pass:** an adversarial review of the three load-bearing claims — the ~$799M market cap and price, the 50/35/10/5 genesis distribution, and the "No governance" design — found no contradicting primary sources; all three survived the falsification attempt. That raises shipping confidence on the factual spine, even as the *interpretive* bear cases above remain live.

The honest synthesis: Venice is a genuinely-used AI business that chose, for product and regulatory convenience, a maximally centralized and reflexive token wrapper. The features that make the company nimble — full control, no governance, revenue-funded burns, a self-referential mint curve — are precisely the features that make the *token* fragile. Both things are true at once, and any position in $VVV is a bet on which one the market keeps pricing.

:::references
- {id: 1, title: "Introducing the Venice Token: VVV", url: "https://venice.ai/blog/introducing-the-venice-token-vvv", source: Venice.ai, date: "2025-01-27"}
- {id: 2, title: "Venice Token (VVV) — price, supply, ATH/ATL", url: "https://www.coingecko.com/en/coins/venice-token", source: CoinGecko, date: "2026-05-20"}
- {id: 3, title: "VVV token contract (Base) — holders, audit status, mint", url: "https://basescan.org/token/0xacfE6019Ed1A7Dc6f7B508C02d1b04ec88cC21bf", source: Basescan, date: "2026-05-20"}
- {id: 4, title: "Venice Token (VVV) market data", url: "https://coinmarketcap.com/currencies/venice-token/", source: CoinMarketCap, date: "2026-05-20"}
- {id: 5, title: "VVV/WETH pool — Base (price history)", url: "https://www.geckoterminal.com/base/pools/0x01784ef301d79e4b2df3a21ad9a536d4cf09a5ce", source: GeckoTerminal, date: "2026-05-20"}
- {id: 6, title: "Venice airdrop ends, $100M unclaimed VVV burned", url: "https://www.theblock.co/post/345912/venice-airdrop-ends-100-million-usd-unclaimed-vvv-tokens-burned", source: The Block, date: "2025-03-12"}
- {id: 7, title: "Programmatic VVV Buy & Burn", url: "https://venice.ai/blog/programmatic-vvv-buy-and-burn", source: Venice.ai, date: "2026-04-15"}
- {id: 8, title: "Understanding Venice Compute Units (Diem)", url: "https://venice.ai/blog/understanding-venice-compute-units-vcu", source: Venice.ai, date: "2025-07-01"}
- {id: 9, title: "Introducing DIEM as tokenized intelligence", url: "https://venice.ai/blog/introducing-diem-as-tokenized-intelligence-the-next-evolution-of-vvv", source: Venice.ai, date: "2025-08-20"}
- {id: 10, title: "7 Days to DIEM (mint-curve formula)", url: "https://venice.ai/blog/7-days-to-diem", source: Venice.ai, date: "2025-08-13"}
- {id: 11, title: "Voorhees on staking reflexivity / mint curve", url: "https://x.com/ErikVoorhees/status/1954293990146428966", source: "X (@ErikVoorhees)", date: "2025-08-09"}
- {id: 12, title: "Voorhees: 6.3M VVV locked, equilibrium logic", url: "https://x.com/ErikVoorhees/status/2008406334425715000", source: "X (@ErikVoorhees)", date: "2026-01-06"}
- {id: 13, title: "DIEM (Venice AI) — price, supply, ATH", url: "https://coinmarketcap.com/currencies/venice-ai/", source: CoinMarketCap, date: "2026-05-20"}
- {id: 14, title: "Emissions roadmap 6M → 3M/yr", url: "https://x.com/AskVenice/status/2037231269449523276", source: "X (@AskVenice)", date: "2026-03-26"}
- {id: 15, title: "Emissions cut to 5M/yr, net-deflation goal", url: "https://x.com/AskVenice/status/2050251602036941087", source: "X (@AskVenice)", date: "2026-05-01"}
- {id: 16, title: "Venice passes 3,000,000 users; agentic chat + MCP", url: "https://x.com/AskVenice/status/2055727865849671917", source: "X (@AskVenice)", date: "2026-05-16"}
- {id: 17, title: "Erik Voorhees — biography, SatoshiDICE/ShapeShift", url: "https://en.wikipedia.org/wiki/Erik_Voorhees", source: Wikipedia, date: "2026-05-01"}
- {id: 18, title: "Erik Voorhees faces $50K SEC settlement", url: "https://www.coindesk.com/markets/2014/06/03/erik-voorhees-faces-50k-fine-over-unauthorized-securities-sale", source: CoinDesk, date: "2014-06-03"}
- {id: 19, title: "Former Circle policy VP and Voorhees launch AI app", url: "https://www.dlnews.com/articles/people-culture/former-circle-policy-vp-and-erik-voorhees-launch-ai-app/", source: DL News, date: "2024-05-10"}
- {id: 20, title: "Welcome to Venice (launch thesis)", url: "https://venice.ai/blog/welcome-to-venice", source: Venice.ai, date: "2024-07-18"}
- {id: 21, title: "Voorhees: 3M users, 230+ models, privacy claims", url: "https://x.com/ErikVoorhees/status/2055724060152336768", source: "X (@ErikVoorhees)", date: "2026-05-16"}
- {id: 22, title: "venice.ai traffic estimates", url: "https://www.similarweb.com/website/venice.ai/", source: Similarweb, date: "2026-04-30"}
- {id: 23, title: "Venice + OpenRouter; refusal-rate comparison", url: "https://venice.ai/blog/venice-openrouter-partner-to-expand-reach-of-private-uncensored-ai-to-developers", source: Venice.ai, date: "2026-05-05"}
- {id: 24, title: "SEC staff statement on protocol staking (analysis)", url: "https://www.fenwick.com/insights/publications/sec-staff-statement-concludes-protocol-staking-is-not-a-securities-transaction", source: Fenwick, date: "2025-06-05"}
- {id: 25, title: "Statement on Certain Protocol Staking Activities", url: "https://www.sec.gov/newsroom/speeches-statements/statement-certain-protocol-staking-activities-052925", source: "SEC (DivCorpFin)", date: "2025-05-29"}
- {id: 26, title: "DoubleZero DePIN no-action letter (Peirce)", url: "https://www.sec.gov/newsroom/speeches-statements/peirce-092925-deep-statement-doublezero-no-action-letter", source: SEC, date: "2025-09-29"}
- {id: 27, title: "SEC Enforcement 2025: Year in Review", url: "https://corpgov.law.harvard.edu/2026/01/21/sec-enforcement-2025-year-in-review/", source: "Harvard Law (CorpGov)", date: "2026-01-21"}
- {id: 28, title: "Clarity Act signed into law in 2026? (market)", url: "https://polymarket.com/event/clarity-act-signed-into-law-in-2026", source: Polymarket, date: "2026-05-20"}
- {id: 29, title: "Grayscale files for first US Bittensor ETP", url: "https://www.coindesk.com/business/2025/12/30/grayscale-files-for-first-u-s-bittensor-etp-as-decentralized-ai-gains-momentum", source: CoinDesk, date: "2025-12-30"}
- {id: 30, title: "Emissions cut 10M → 8M ('Venice is Burning')", url: "https://x.com/AskVenice/status/1975598404085371013", source: "X (@AskVenice)", date: "2025-10-07"}
- {id: 31, title: "Voorhees: locked VVV ~5M → ~9M; lock dynamics", url: "https://x.com/ErikVoorhees/status/2051701847308837232", source: "X (@ErikVoorhees)", date: "2026-05-05"}
- {id: 32, title: "Top Bittensor subnets (dTAO); Targon/inference", url: "https://www.coingecko.com/learn/top-bittensor-subnets-dtao", source: CoinGecko, date: "2026-05-10"}
- {id: 33, title: "Upbit to list VVV (KRW/BTC/USDT)", url: "https://www.wublockchain.xyz/news/upbit-listing-venice-vvv-krw-btc-usdt-pairs-19093", source: Wu Blockchain, date: "2026-05-12"}
- {id: 34, title: "Did the Venice team dump $5.7M after Coinbase listing?", url: "https://coingape.com/trending/did-venice-team-dump-5-7m-tokens-after-coinbase-listing/", source: CoinGape, date: "2025-01-29"}
- {id: 35, title: "AntSeed opens first P2P rival to OpenRouter (DIEM)", url: "https://chainwire.org/2026/05/15/antseed-opens-first-peer-to-peer-rival-to-openrouter/", source: Chainwire, date: "2026-05-15"}
- {id: 36, title: "SEC/CFTC clarify securities laws for crypto assets", url: "https://www.fintechanddigitalassets.com/2026/04/sec-clarifies-the-application-of-the-securities-laws-to-cryptoassets/", source: "Fintech & Digital Assets", date: "2026-04-15"}
- {id: 37, title: "Programmatic $1-per-Pro VVV buy-and-burn launch", url: "https://x.com/AskVenice/status/2044511248864223561", source: "X (@AskVenice)", date: "2026-04-15"}
:::
