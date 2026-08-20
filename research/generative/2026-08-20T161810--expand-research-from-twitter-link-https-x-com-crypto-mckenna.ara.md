---
eyebrow: Crypto · DeFi credit · AI infrastructure
title: 'Arete Capital''s CHIP thesis, checked against the chain'
deck: A fund that holds half its book in liquid tokens published a bull case for USD.AI's GPU-lending protocol on August 19, 2026. Its two most load-bearing numbers do not survive contact with the protocol's own dashboard.
lede: 'On August 19, 2026, Arete Capital -- a crypto fund whose stated mandate is half venture, half liquid-token
  investing -- published an X Article titled "Arete Capital CHIP Thesis: Serving the $2T GPU Debt Middle
  Market," arguing that USD.AI''s CHIP token is underpriced against a loan book "approaching $500M," a
  net lender APY of 7.66%, and "$30M ARR to the DAO" in the second quarter. Three months earlier, an
  independent audit of the same protocol found it was still, in practice, mostly a Treasury-bill fund
  wearing a GPU-credit brand. This article checks Arete''s numbers against USD.AI''s own dashboard, DefiLlama''s
  API, an SEC filing, and a short-seller report on one of the protocol''s anchor borrowers -- and finds a
  thesis that gets the macro setup right and several of its own protocol''s numbers wrong, in a direction
  that happens to flatter the token both authors work for.'
stats:
- label: TVL, Arete's claim vs. DefiLlama
  value: $430M vs $177M
  note: −37% claimed, −74% actual since Jan 1
- label: Loan book, claimed vs. self-reported
  value: ~$500M vs $205M
  note: USD.AI's own H1 2026 report
- label: CHIP price since mid-May 2026
  value: −46%
  note: fresh all-time low Aug 9, 2026
- label: "'$2T middle market' vs. actual specialist GPU-debt market"
  value: $2T vs $20–30B
  note: ~100x overstatement
---

## 0. The five-second version

:::callout(kind=info, label="Direct answer")
Arete Capital's August 19 thesis is right about the macro setup (Morgan Stanley really did estimate a
$1.5T AI data-center financing gap) and wrong, or at minimum unreconciled, about the protocol it is
pitching: its TVL figure matches USD.AI's own dashboard but is 2.4x DefiLlama's independently tracked
number; its "approaching $500M" loan book is 2.4x what USD.AI's own H1 report discloses as actually
deployed; its "$2T" addressable market is roughly 100x the independently sized specialist GPU-debt
market; and its "$30M ARR" figure, while sourced to USD.AI's own report, is roughly 4x DefiLlama's
independently tracked trailing revenue. Both named authors are Arete Capital staff, not one Arete
partner plus an independent analyst, and neither the thesis nor any indexed source discloses a CHIP
position.
:::

## 1. Who is making this claim, and what do they claim

Arete Capital is a crypto fund that launched in April 2024 targeting a $20M first vehicle, structured
explicitly as half venture-stage token investing and half secondary-market liquid-token positions --
meaning a bullish public thesis on a live, tradeable governance token like CHIP sits squarely inside the
fund's stated investment universe, not adjacent to it.[^1] Its Managing Partner, who posts as
@Crypto_McKenna ("McKenna," ~105,700 followers), has a pattern worth flagging before reading
his numbers: an October 2025 bullish thesis on Hyperliquid's HYPE token is reported to have preceded a
disclosed purchase of HYPE at $33; the token later peaked near $76-77 in June 2026 before pulling back to
roughly $59 by early August, short of the $100 target attached to that thesis. ==unverified: the purchase
disclosure was located via secondary aggregation of McKenna's public statements rather than a direct read
of the original post; treat the trading-pattern characterization as directionally plausible, not
confirmed verbatim.==[^2] The CHIP piece's co-author,
who posts as @Daveeemor, is not an independent outside analyst -- the account's own bio reads "Investments
@Arete_xyz," identifying them as Arete Capital staff.[^3] Neither the thesis nor Arete's own research
page (which has not been updated to include the CHIP piece at all) discloses a CHIP, USDai, or sUSDai
position by either author.[^4] Absence of a public disclosure is not proof of an undisclosed position --
but a fund whose stated strategy is trading the exact asset class it is publicly promoting should be read
as investor-relations content until shown otherwise, not as neutral research.

The thesis itself, reconstructed from the X Article via an independent extraction (the platform's rendered
article page returned a login wall on direct fetch), makes six load-bearing claims: a $2.9T/$1.5T Morgan
Stanley financing-gap citation; an $8T McKinsey figure; a "$2T GPU debt middle market" framing; a loan book
"approaching $500M"; TVL "fallen by 37% since the start of the year to $430M"; "$30M ARR to the DAO" in
Q2 2026; a net lender APY of 7.66%; and a base-case projection of $68.8M in protocol revenue by the end of
2027 off $2.5B of annual loan originations.[^5] What would weaken this critique: if the underlying X Article
turns out to include qualifying language, ranges, or as-of dates the extraction tool dropped, several of
the gaps below would narrow. That caveat cuts only so far, though, because every comparison below is against
the protocol's *own* published numbers, not against a hypothetical fuller version of Arete's text.

## 2. Three trackers, three truths: the TVL number

USD.AI's total value locked is not one number. It is at least three, and Arete's $430M sits at the
favorable end of the range rather than at a consensus midpoint.

DefiLlama's public API -- the same aggregator most DeFi analysts default to -- shows USD.AI's TVL at
$177.1M as of August 16, 2026, down from a January 1, 2026 peak of $686.9M: a 74.2% decline, roughly
double the "37% since the start of the year" Arete cites.[^6] USD.AI's own app dashboard, by contrast,
shows TVL of $432.4M as of August 21 -- a near-exact match for Arete's $430M.[^7] A third tracker,
Stablewatch, puts sUSDai's vault TVL at $299.8M.[^8] The likely explanation is not that any single
tracker is lying: DefiLlama's headline TVL figure is documented to exclude active/deployed loans by
default unless a viewer manually toggles them in, while USD.AI's own dashboard appears to sum idle
backing assets *plus* deployed loan principal *plus* collateral value -- a broader definition that
mechanically produces a bigger number.[^9] That is a real, defensible methodological difference. But
it means "TVL fell 37% to $430M" is true only under the one definition that happens to look best, stated
without the caveat that an equally standard definition puts the decline at double that rate and the
absolute figure at less than half.

:::compare
- {role: LOWEST, name: DefiLlama API, value: $177M}
- {role: HIGHEST, name: USD.AI's own dashboard, value: $432M}
- {role: SUBJECT, name: "Arete's cited figure", value: $430M}
:::

What would weaken this: DefiLlama toggles are a known source of cross-protocol inconsistency industry-wide,
not a USD.AI-specific red flag, and a protocol citing its own dashboard is not inherently dishonest.
Why this matters: a reader who checks Arete's $430M against the first tracker they open (DefiLlama, the
most commonly cited DeFi data source) will conclude the thesis understated the damage by roughly half --
exactly the kind of discrepancy a rigorous published thesis should flag and reconcile, not silently avoid.

## 3. The loan book: pipeline, term sheets, and what's actually drawn

USD.AI's own mid-2026 "Lighthouse" report -- the same document that appears to be Arete's source for its
revenue figure (Section 5) -- discloses a funnel, not a single number: 394 leads reviewed representing
$13.0B of potential volume, 26 signed term sheets worth $817M, and **$202-205M of loans actually deployed**
across 13 active positions, with $283M in total collateral value.[^10] "Approaching $500M" is roughly 2.4x
that disclosed deployed figure. The most plausible source of the gap is that $500M is the size of a single
*approved facility ceiling* -- Sharon AI's "up to $500M" commitment is the best-known example -- being read
as if it were the aggregate drawn loan book, when in practice both of USD.AI's original anchor borrowers have
drawn far less than their headline ceilings (Section 4).[^11]

What has genuinely changed since a prior independent audit of this protocol found $104M deployed against
Sharon AI and QumulusAI as roughly 83% of the book: the growth since then traces almost entirely to *new*
borrowers, not the two original anchors scaling up. Duos Edge AI, a subsidiary of Nasdaq-listed Duostech
managed by Hydra Host, grew from a $620,000 loan in July 2025 to a $98.1M facility by June 2026 --
now the single largest position in the book.[^12] NexGen Cloud drew $34M in June 2026 backing 768 Nvidia
B200 GPUs at a 12% APY.[^13] Crucible Capital drew $26.8M.[^14] That is real diversification and real
growth -- from $104M to roughly $205-283M is genuine expansion, just not the "approaching $500M" Arete
states, and the growth driver (new small borrowers) is a different story than the implied one (the
original anchor facilities scaling toward their ceilings).

:::slope(left-label="Arete's claim", right-label="USD.AI's own H1 2026 report", unit=$M)
| Item | Arete's claim | USD.AI's own report |
|------|------|------|
| Loan book deployed | 500 | 205 |
| Protocol TVL | 430 | 177 |
:::

Why this matters: a reader underwriting CHIP on "the loan book is approaching $500M" is pricing in roughly
2.4x the collateral base the protocol's own most detailed disclosure supports, at exactly the moment that
disclosure would matter most for judging whether the revenue growth in Section 5 is durable or a one-time
spike from origination-fee lumpiness.

## 4. Sharon AI and QumulusAI: real growth, real allegations

The two original anchor borrowers tell genuinely different stories, and Arete's thesis conflates them
into one "the middle market is working" narrative that undersells both the good news and the bad news.

Sharon AI (Nasdaq: SHAZ) has scaled its customer-facing business substantially since May: 212MW of secured
AI Factory capacity as of its August 13, 2026 earnings call (up from 132MW guidance), a new $373M five-year
cloud agreement announced August 4, and customer acceptance of an initial deployment under a roughly $950M
contract announced August 20 -- the day before Arete's thesis.[^15] None of that, however, is a disclosed
incremental drawdown against the USD.AI facility itself beyond its original roughly $65M initial tranche;
the growth is customer-contract value, which is a different balance-sheet line than USD.AI loan
utilization.[^16] Layered on top is an active short thesis: Bleecker Street Research's April 30, 2026 report
alleges Sharon AI's $1.25B anchor contract with Indian operator ESDS requires roughly $250M/year in payments
against ESDS's disclosed FY2025 revenue of $39.9M (a 6.3x ratio) and a $140M letter-of-credit requirement
against ESDS's total assets of $69.5M -- and separately argues India's RBI data-localization rules may bar
ESDS's banking customers from using Australian-hosted compute at all.[^17] These are short-seller allegations,
not adjudicated fact, and Sharon AI has continued signing new contracts since the report -- but Arete's
thesis does not mention the report, the ESDS solvency question, or the CEO litigation the same report
raises.[^17]

QumulusAI is the cleaner data point, because it traces to an SEC filing rather than a press release.
QumulusAI's own S-1/A is reported to disclose just **$4.3M drawn against its $500M USD.AI facility** as
of February 2026 -- more than six months before Arete's thesis and consistent with the earlier
short-seller figure. ==unverified: this article could not directly render the S-1/A's text and relies on
a secondary characterization of the filing rather than a first-hand read of the primary document; treat
the $4.3M figure as well-corroborated but not independently re-confirmed here.==[^18] The company had
separately announced delivery of 1,144 Nvidia Blackwell GPUs under the same facility, a mismatch between
hardware delivered and dollars drawn that the S-1/A does not fully reconcile in public disclosure.[^19]

| Borrower | Facility ceiling | Actually drawn (disclosed) | Source |
|---|---|---|---|
| Sharon AI | $500M | ~$65M (initial tranche, no confirmed increase) | CoinDesk, Aug 2026 filings[^16] |
| QumulusAI | $500M | $4.3M (Feb 2026, per own S-1/A) | SEC EDGAR[^18] |
| *Duos Edge AI (new)* | *n/a* | *$98.1M* | *USD.AI[^12]* |

What would weaken this: undrawn commitment is not the same as a bad loan, and forward-flow facilities that
ramp slowly as GPU racks are delivered and energized are a standard feature of equipment finance, not
inherently a red flag. Why this matters: two of the protocol's three largest named facilities are drawn at
13% (Sharon AI, roughly) and 0.9% (QumulusAI) of their headline ceiling respectively, which is the opposite
of the "the market is validating $500M-scale middle-market lending" reading Arete's framing implies.

## 5. The revenue question: $30M ARR vs. $7M in independently tracked fees

Arete's "$30M ARR to the DAO in Q2" is traceable, almost verbatim, to USD.AI's own Lighthouse report,
which states annualized DAO ARR grew from $1.1M in 2025 to $4.0M in Q1 2026 to $30M (annualized) in Q2
2026.[^10] That is a real, self-reported trajectory, not a fabricated number -- but it is worth being
precise about what "annualized Q2" means: it is a single quarter's revenue multiplied by four, and DefiLlama
logs a $3M one-time origination fee tied to the Duos Edge AI facility landing on June 4, 2026 -- squarely
inside that same quarter.[^20] A single large origination-fee event concentrated in one quarter, annualized,
can produce a headline run-rate well above the protocol's trailing actual revenue.

DefiLlama's independently tracked fee data supports that read: trailing-twelve-month fees total
approximately $7.0M annualized as of the same window, roughly a quarter of Arete's cited $30M.[^21] The
two numbers are not strictly contradictory -- "annualized run-rate off the strongest recent quarter" and
"trailing twelve-month actual" are different, both legitimate methodologies that will diverge whenever
growth is lumpy -- but Arete presents the more favorable of the two without noting the other, and without
flagging that the underlying quarter likely contains a one-time fee spike rather than a repeatable run-rate.

:::stats
- {label: "2025 full-year ARR (self-reported)", value: $1.1M}
- {label: "Q1 2026 ARR, annualized (self-reported)", value: $4.0M}
- {label: "Q2 2026 ARR, annualized (self-reported, Arete's figure)", value: $30M}
- {label: "Trailing 12-month fees (DefiLlama, independent)", value: ~$7.0M}
:::

What would weaken this: if Duos Edge AI's $98.1M facility keeps originating new tranches at a similar pace
each quarter, the "one-time spike" read is wrong and $30M genuinely becomes the new baseline -- that is
falsifiable within a quarter or two of future reporting. Why this matters: revenue is the number that
ultimately has to support both sUSDai's yield and any future CHIP value-accrual mechanism Arete's thesis
gestures toward (Section 7); a 4x gap between self-reported and independently tracked revenue is exactly
the kind of number a reader needs flagged before underwriting a 2027 revenue forecast built on top of it.

## 6. CHIP: what actually happened to the price since May

An independent audit in mid-May 2026 found CHIP trading around $0.054, with a market cap near $108.6M and
an FDV near $542.8M.[^22] Since then, CHIP has not moved sideways or up in a straight line -- it made a
fresh all-time low of $0.02163 on August 9, 2026, 78% below its April 23 all-time high of $0.1402, before
a sharp short-term bounce to roughly $0.028-0.031 by August 19-21, the exact window Arete's thesis was
published in.[^23] Market cap sits near $56-62M and FDV near $293-310M as of the thesis date -- both
roughly 45% below the May baseline.[^22,23]

:::line-chart(title="CHIP price, Apr-Aug 2026", subtitle="CoinGecko", y-unit=$)
x: 2026-04-23,2026-05-16,2026-08-09,2026-08-21
CHIP: 0.1402,0.0540,0.02163,0.0300
:::

The seven-day change into the thesis's publication date was +34.8% -- a real bounce -- but the thirty-day
change was only +1.8%, meaning the net position over the full prior month was close to flat: the bounce is
a recovery off a two-week-old floor, not a sustained trend a reader should mistake for the token "having
been stable since May" or grinding higher on the back of the loan-book growth described in Section 3.[^23]
No governance proposal addressing the April 21, 2027 unlock cliff -- when roughly 1.68B tokens (33% of the
combined 53.1% team-and-investor allocation) unlock in a single day against a circulating supply of
roughly 2B -- was found as of this writing.[^24] Independent analyst Pine Analytics, writing near CHIP's
launch, argued the token's $300M FDV priced in at 1.2x Ethena's FDV/TVL multiple and 2.9x Maple Finance's
despite far lower loan utilization at the time (roughly 10% of TVL deployed), and modeled compression
scenarios of roughly $250M FDV (an Ethena-comparable re-rating) or $105M FDV (a Maple-comparable one).[^25]
CHIP's current FDV of roughly $293-310M sits almost exactly at the milder of those two bear-case scenarios
-- meaning a meaningful chunk of the valuation correction that bear case anticipated has already happened,
which cuts in a genuinely more constructive direction for anyone buying today versus at the April launch.
==unverified: no governance proposal addressing the April 21, 2027 unlock cliff was found in the sources
checked for this article, but that is an absence-of-evidence result from a limited documentation search,
not confirmation that none exists or that USD.AI governance has been silent on the topic.==

What would weaken this: a token that has already round-tripped through an 80% drawdown and a fresh
all-time low, and is still trading at a bear-case-implied valuation rather than the original launch
multiple, is arguably a *more* interesting entry point than the same protocol at its April 21 launch price
-- if the underlying loan book and revenue genuinely are compounding as Section 5's self-reported trajectory
suggests. Why this matters: Arete's thesis frames CHIP's setup without mentioning the fresh all-time low
eleven days before publication, which a reader would reasonably want to know before treating "expected to
exceed 10%" APY guidance or a 2027 revenue forecast as the operative variable over near-term price action.

## 7. The "$2T GPU debt middle market" that isn't

The thesis's title framing -- "Serving the $2T GPU Debt Middle Market" -- is the single largest gap between
citation and independent verification in the piece, even though its underlying macro citation checks out.

Morgan Stanley's $2.9T/$1.5T figures are real and traceable to a specific, named report, "Bridging a $1.5tr
Data Center Financing Gap": $2.9T of cumulative global data-center capex from 2025-2028 ($1.3T physical
infrastructure, $1.6T IT hardware), against roughly $1.4T of hyperscaler self-funded capacity, leaving a
$1.5T gap Morgan Stanley expects credit markets -- roughly $800B private credit, $200B corporate bonds,
$150B securitized products, and the remainder other channels -- to fill.[^26] "Unfunded by hyperscaler cash
flow" is a fair paraphrase of that framing, if slightly sharper than Morgan Stanley's own "external
financing" language, which implies the gap *will* be filled rather than sitting unfunded.[^27] The
separately cited McKinsey "$8T by 2030" figure is less clean: McKinsey's most commonly cited headline
number is $6.7T (or $7T in some framings) of total global data-center capex by 2030; $8T appears only as
the *upper bound* of a $3-8T range for AI-specific capacity demand under McKinsey's more aggressive
scenario, not a standalone estimate.[^28] Citing the top of a range as "McKinsey estimates" is a real, if
minor, upward bias in the thesis's favor.

The bigger problem is the leap from "$1.5-2.9T of total AI infrastructure spending needs financing" to
"$2T GPU debt middle market" as if that middle-market segment specifically is worth trillions. Independent
sizing of the actual specialist GPU-collateralized private-credit niche -- the layer between venture debt
and investment-grade asset-backed securitization where USD.AI, Compute Labs, and similar lenders compete --
comes in around $20-30B, with institutional entrants (Blackstone, Ares) already pricing deals at SOFR+450-700
basis points. ==unverified: this range is drawn from a single specialist industry reference rather than a
bank or ratings-agency market-sizing report, and should be treated as an order-of-magnitude estimate, not
a precise figure.==[^29] USD.AI's own cumulative disclosed lending across every facility to date is roughly $1.2B
in approvals, of which Section 3 showed roughly $205-283M is actually deployed.[^30] Traditional (non-crypto)
private credit already serves comparably sized or larger deals in exactly this tier: Upper90 ($225M to
Crusoe), Victory Park Capital ($175M, also Crusoe), and Macquarie (up to $10B for FluidStack, backstopped
by a $6.7B Google contract).[^31]

:::bars
- {label: "'$2T middle market' (Arete's framing)", value: $2,000B, pct: 100}
- {label: "Specialist GPU-debt market (independent estimate)", value: $20-30B, pct: 1}
- {label: "USD.AI cumulative approved (all facilities)", value: $1.2B, pct: 0.06}
- {label: "USD.AI actually deployed", value: ~$205M, pct: 0.01}
:::

What would weaken this: a real, underserved financing gap for sub-institutional AI infrastructure operators
plainly does exist -- banks are slow, private credit funds mostly serve known names, and venture debt comes
with equity warrants, which is a genuine structural complaint independent of any specific dollar figure --
and $20-30B today growing toward a meaningfully larger number over several years as the AI buildout matures
is not an unreasonable growth thesis on its own. Why this matters: "$2T" is doing rhetorical work the
underlying data does not support; the real opportunity, on the best independent sizing available, is roughly
two orders of magnitude smaller than the number in the thesis's own title.

## 8. The insurance backstop: what "100% coverage" actually covers

One structural claim in the thesis checks out cleanly, with one important nuance. Barker (branded "Barkr"
in its own product) is a single AI-hardware valuation company -- not two different entities, despite the
spelling variance across sources -- founded by CEO Thomas Galbraith and backed by a roughly $2B cumulative
track record of asset valuations for banks and specialty lenders before entering the USD.AI relationship.[^32]
The USD.AI-Barker coverage, reinsured through Munich Re's Great Lakes Insurance SE, launched February 6,
2026 -- a few weeks earlier than a prior audit had dated it -- and is structured so that an 80%-of-valuation
warranty exactly matches USD.AI's 80% maximum loan-to-value cap, meaning coverage is designed to equal full
outstanding principal at origination under standard underwriting.[^33] No publicly reported claim, dispute,
or payout under the wrap has surfaced as of this writing.[^34]

The nuance is the same one a prior independent audit flagged in May: the payout is benchmarked to *Barker's
own* predicted valuation, not to an independently observed market-clearing price, so the insurance only
protects against a shortfall relative to Barker's own estimate of what the GPU was worth -- it does not
protect against Barker's estimate itself being too optimistic. That underlying dispute is, if anything,
murkier now than in May: Silicon Data, the firm whose data underpinned the original "Barker's curve is too
generous" critique, has since published commentary describing used H100 and B200 pricing as having
*appreciated* through 2026 on rising rental income, while other aggregators (CloudZero) still show steep
multi-year depreciation on used H100s.[^35] Treat any single source's resolution of the residual-value
question skeptically; the underlying secondary market data is itself provider-dependent and still moving.

:::position(confidence=medium, horizon=2027-Q1)
stance: The next real re-rating catalyst for CHIP is not the April 2027 unlock cliff Arete's thesis omits discussing -- it is whether Q3 2026 revenue holds anywhere near the $30M annualized run-rate without another single-borrower origination-fee spike the size of Duos Edge AI's.
consensus: Public commentary on CHIP centers almost entirely on the unlock cliff as the dominant forward risk.
resolves: USD.AI's Q3 2026 Lighthouse-style report, or DefiLlama's independently tracked fee data over the same window, whichever is published first.
:::

## 9. What would make Arete right anyway

Steelmanning the thesis matters as much as stress-testing it. The protocol's self-reported trajectory --
$1.1M to $4.0M to $30M annualized ARR across three consecutive periods -- is directionally the kind of
curve that, if it holds even at a fraction of the Q2 print, represents real compounding growth from a
genuinely tiny base.[^10] The loan book has diversified into new borrowers rather than concentrating further
in two names a short-seller had already targeted, which is a structural improvement over the May 2026
picture regardless of the exact dollar total.[^12,13,14] CHIP's FDV has already compressed close to an independent
bear case's milder scenario, meaning much of the "priced for perfection" risk that existed at April's
launch has already been worked off through an 80% drawdown few token launches survive without a de-listing
or a rug.[^23,25] And the macro backdrop Arete cites first -- a genuine, Morgan-Stanley-sized financing gap for AI
infrastructure -- is real, even if the specific "$2T middle market" framing overstates USD.AI's addressable
slice of it by roughly two orders of magnitude.[^26,29]

:::timeline
- {date: "2026-01-01", headline: "TVL peaks at $686.9M", body: "DefiLlama; before the sharpest phase of the year's decline."}
- {date: "2026-01-22", headline: "Sharon AI facility approved", body: "Up to $500M, non-recourse, GPU-backed."}
- {date: "2026-02-06", headline: "Barker/Munich Re coverage launches", body: "80% of Barker's valuation, matching the 80% max LTV cap."}
- {date: "2026-02-19", headline: "QumulusAI draws $4.3M", body: "Against its $500M facility, per its own later S-1/A."}
- {date: "2026-04-21", headline: "CHIP TGE", body: "$300M FDV, 20% circulating at launch."}
- {date: "2026-04-23", headline: "CHIP all-time high", body: "$0.1402."}
- {date: "2026-04-30", headline: "Bleecker Street short report", body: "Targets Sharon AI; cites the same QumulusAI draw figure."}
- {date: "2026-06-04", headline: "$3M one-time origination fee", body: "Tied to the Duos Edge AI facility, landing inside Q2."}
- {date: "2026-06-08", headline: "USD.AI Lighthouse H1 report", body: "$202-205M deployed; $30M annualized Q2 ARR."}
- {date: "2026-08-09", headline: "CHIP all-time low", body: "$0.02163, 78% below April's high."}
- {date: "2026-08-19", headline: "Arete Capital publishes CHIP thesis", body: "The subject of this article."}
- {date: "2027-04-21", headline: "Unlock cliff (ahead)", body: "~1.68B CHIP unlocks in a single day."}
:::

## 10. What would break this call

If Q3 2026 revenue holds within shouting distance of the $30M annualized figure without another
single-borrower fee spike,[^20,21] if the loan book crosses $300-350M of genuinely deployed capital rather than
approved ceilings,[^10,11] and if a governance proposal addresses the April 2027 cliff before it arrives,[^24] the
skeptical reading in this article gets meaningfully weaker and Arete's growth thesis gets meaningfully
stronger. Conversely, if Q3 revenue reverts toward the $7-10M range DefiLlama's trailing data implies,[^20,21] if
Sharon AI's ESDS contract runs into the solvency or data-sovereignty problems Bleecker Street alleges,[^17] or
if CHIP's August bounce proves to be exactly the kind of "narrative rally" Pine Analytics warned would be a
short opportunity rather than a hold,[^25] the thesis's framing -- not just its specific numbers -- will have
been the story. Either way, a bull case published by a fund's own staff, on a token that fund is structurally
positioned to trade, whose two most citable numbers both round in the fund's favor relative to the
protocol's own more detailed disclosures, is a data point worth weighing on its own terms -- not a
substitute for checking the protocol's dashboard directly.

:::references
- {id: 1, title: "Crypto anon McKenna launches Arete Capital, with first fund targeting $20 million", url: "https://www.theblock.co/post/286286/crypto-anon-mckenna-launches-arete-capital-with-first-fund-targeting-20-million", source: The Block, date: "2024-04-08"}
- {id: 2, title: "McKenna's October 2025 HYPE thesis and disclosed purchase", url: "https://x.com/Crypto_McKenna/status/1978095055366676731", source: "X / @Crypto_McKenna", date: "2025-10-14"}
- {id: 3, title: "Daveeemor (@Daveeemor) profile", url: "https://x.com/Daveeemor", source: "X / @Daveeemor"}
- {id: 4, title: "Arete Capital research archive", url: "https://www.aretecapital.xyz/research", source: "Arete Capital"}
- {id: 5, title: "Arete Capital CHIP Thesis: Serving the $2T GPU Debt Middle Market", url: "https://x.com/Crypto_McKenna/status/2090078188752060628", source: "X Article / Arete Capital", date: "2026-08-19"}
- {id: 6, title: "USD AI protocol TVL", url: "https://api.llama.fi/protocol/usd-ai", source: DefiLlama, date: "2026-08-16"}
- {id: 7, title: "USD.AI CHIP dashboard", url: "https://app.usd.ai/chip", source: "USD.AI", date: "2026-08-21"}
- {id: 8, title: "sUSDai (USD.AI) analytics", url: "https://www.stablewatch.io/analytics/assets/sUSDai-USD.AI", source: Stablewatch}
- {id: 9, title: "DeFi Lending Protocols - TVL, Fees, & Revenue", url: "https://defillama.com/protocols/lending", source: DefiLlama}
- {id: 10, title: "USD.AI 2026 YTD Report (Lighthouse)", url: "https://usd.ai/insights/usdai-2026-ytd-report-lighthouse", source: "USD.AI", date: "2026-06-08"}
- {id: 11, title: "Sharon AI secures up to US$500M debt facility from USD.AI", url: "https://www.coindesk.com/business/2026/01/22/ai-infrastructure-firm-secures-up-to-usd500-million-onchain-loan-after-bypassing-banks", source: CoinDesk, date: "2026-01-22"}
- {id: 12, title: "USD.AI provides $98.1M debt financing to Duos Edge AI", url: "https://www.prnewswire.com/news-releases/usdai-provides-98-1m-debt-financing-to-support-duos-edge-ai-gpu-deployment-managed-by-hydra-host-302792700.html", source: "PR Newswire", date: "2026-06-05"}
- {id: 13, title: "USD.AI June recap: new highs across markets", url: "https://usd.ai/insights/usdai-june-recap-new-highs-across-markets", source: "USD.AI", date: "2026-06"}
- {id: 14, title: "Crucible Capital $26.8M GPU-backed loan", url: "https://usd.ai/insights/crucible-capital-26m-gpu-backed-loan", source: "USD.AI"}
- {id: 15, title: "SharonAI (SHAZ) Q2 2026 earnings call transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/08/13/sharonai-shaz-q2-2026-earnings-call-transcript/", source: "The Motley Fool", date: "2026-08-13"}
- {id: 16, title: "Sharon AI successfully delivers AI cloud deployment for global technology company", url: "https://www.stocktitan.net/news/SHAZ/sharon-ai-successfully-delivers-ai-cloud-deployment-for-global-1phs2xslrwpj.html", source: StockTitan, date: "2026-08-20"}
- {id: 17, title: "SharonAI (SHAZ): a neocloud built on phantom contracts and questionable financing", url: "https://www.bleeckerstreetresearch.com/research/shaz", source: "Bleecker Street Research", date: "2026-04-30"}
- {id: 18, title: "QumulusAI Form S-1/A", url: "https://www.sec.gov/Archives/edgar/data/2084026/000143774926017093/quma20260513_s1a.htm", source: "SEC EDGAR", date: "2026-05-13"}
- {id: 19, title: "QumulusAI deploys 1,144 Nvidia Blackwell GPUs through drawdown under $500M USD.AI facility", url: "https://www.qumulusai.com/articles/qumulusai-deploys-1144-nvidia-blackwell-gpus-through-drawdown-under-500m-usdai-facility", source: "QumulusAI", date: "2026-02-19"}
- {id: 20, title: "USD AI fees and revenue", url: "https://api.llama.fi/summary/fees/usd-ai?dataType=dailyRevenue", source: DefiLlama}
- {id: 21, title: "USD AI TVL, Fees & Revenue", url: "https://defillama.com/protocol/usd-ai", source: DefiLlama}
- {id: 22, title: "USD.AI (sUSDai) explained: GPU-backed synthetic dollar, yield and risk analysis", url: "https://www.stablewatch.io/research/usd-ai-deep-dive", source: Stablewatch}
- {id: 23, title: "USD.AI (CHIP) price", url: "https://www.coingecko.com/en/coins/usd-ai", source: CoinGecko, date: "2026-08-21"}
- {id: 24, title: "CHIP governance", url: "https://docs.usd.ai/governance/chip", source: "USD.AI docs"}
- {id: 25, title: "The Bear Case for $CHIP", url: "https://pineanalytics.substack.com/p/the-bear-case-for-chip", source: "Pine Analytics"}
- {id: 26, title: "Bridging a $1.5tr Data Center Financing Gap", url: "https://www.morganstanley.com/content/dam/msdotcom/en/assets/pdfs/Research_Bridging-Data-Center-Gap.pdf", source: "Morgan Stanley Research"}
- {id: 27, title: "Credit Markets' Role in AI Financing Gap", url: "https://www.morganstanley.com/insights/podcasts/thoughts-on-the-market/credit-markets-ai-financing-gap-vishy-tirupattur-vishwas-patkar", source: "Morgan Stanley"}
- {id: 28, title: "The cost of compute: A $7 trillion race to scale data centers", url: "https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-cost-of-compute-a-7-trillion-dollar-race-to-scale-data-centers", source: "McKinsey & Company"}
- {id: 29, title: "GPU collateralization reference", url: "https://altstreet.investments/reference/structures/gpu-collateralization", source: AltStreet}
- {id: 30, title: "Sharon AI secures up to US$500M debt facility from USD.AI to support GPU-backed AI infrastructure expansion", url: "https://sharonai.com/press-releases/sharon-ai-secures-up-to-us500m-debt-facility-from-usd-ai-to-support-gpu-backed-ai-infrastructure-expansion-in-australia-and-asia-pacific/", source: "Sharon AI"}
- {id: 31, title: "Upper90 closes $225M credit facility to Crusoe to expand AI cloud", url: "https://www.crusoe.ai/resources/newsroom/upper90-closes-usd225m-credit-facility-to-crusoe-to-expand-ai-cloud", source: Crusoe}
- {id: 32, title: "Barker secures $3.5 million to scale warrantied AI valuations for asset-backed lending", url: "https://www.businesswire.com/news/home/20251118349552/en/Barker-Secures-$3.5-Million-to-Scale-Warrantied-AI-Valuations-for-Asset-Backed-Lending", source: BusinessWire, date: "2025-11-18"}
- {id: 33, title: "USD.AI & Barker launch insured GPU loan coverage", url: "https://usd.ai/insights/usdai-barker-insured-gpu-loan-coverage", source: "USD.AI", date: "2026-02-06"}
- {id: 34, title: "USD.AI underwriting and risk management", url: "https://usd.ai/insights/usdai-underwriting-and-risk-management", source: "USD.AI"}
- {id: 35, title: "H100 GPU cost and depreciation", url: "https://www.cloudzero.com/blog/h100-gpu-cost/", source: CloudZero}
:::
