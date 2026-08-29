---
eyebrow: REPORT · SEMICONDUCTORS
title: "Marvell's 58.97M-share Google warrant: what 240 tranches of $500M reveal about the TPU bet"
deck: Google's volume-vested warrant has a $12.2B headline and a $120B vesting ceiling. Neither number is the commitment — the ladder is.
lede: |
  On August 18, 2026, Marvell Technology issued to Google LLC a warrant to buy
  up to 58,970,907 shares at an exercise price of $206.58 — an aggregate
  exercise price of about $12.2 billion — in connection with a commercial
  agreement for custom silicon attached to Google's TPU ecosystem [^1][^2].
  The market read the headline as a vote of confidence and pushed Marvell up
  ~10% the next day while Google's other TPU partner, Broadcom, slid ~5% [^6][^3][^14][^13][^22].
  But the headline is the least informative number in the filing. The
  structure that matters is the vesting ladder: 240 tranches, each unlocking
  240,042 shares for every $500 million of cumulative Google custom-silicon
  revenue Marvell records through fiscal 2033 [^1][^2]. Full vesting implies
  $120 billion of revenue — 14.6x Marvell's entire fiscal 2026 revenue [^8].
  That ceiling is not a commitment, a forecast, or an order book. It is an
  incentive design, and reading it correctly reframes what Google is actually
  promising, and why it is paying its supplier in equity.
stats:
  - {label: "Aggregate exercise price", value: "$12.18B"}
  - {label: "Exercise price per share", value: "$206.58"}
  - {label: "Performance-based shares", value: "57.61M"}
  - {label: "Full-vest revenue", value: "$120B"}
---

## 01. The headline number isn't the deal

The warrant itself is mechanically unremarkable: a seven-year, private-placement
instrument issued under Section 4(a)(2), exercisable in whole or part through
August 18, 2033, with customary anti-dilution adjustments, cashless exercise,
registration rights, and a transfer restriction to controlled affiliates [^2][^1][^24].
Two features are not boilerplate. First, 1,360,867 shares (2.3% of the warrant)
vest purely on passage of time — in equal quarterly installments of
340,216 shares across the first year — regardless of what Google buys
[^1][^2]. Second, the remaining 57,610,040 shares vest on revenue: one tranche
of 240,042 shares for every $500 million of cumulative "Qualifying Revenue"
Google and its affiliates generate for Marvell, running from the third quarter
of fiscal 2027 (August 1, 2026) through fiscal 2033 (January 29, 2033) [^1][^2].

The arithmetic deserves to be flattened out, because it anchors both the
bullish and the bearish reads. 240 tranches times $500 million equals $120
billion of cumulative revenue for full vesting — an implied average of
roughly $18.5 billion per year over the 6.5-year measuring window [^1][^2].
Marvell reported $8.2 billion of total revenue in all of fiscal 2026, across
every customer and product line [^8]. So full vesting is not a base case; it
would require Google alone to buy roughly two-and-a-quarter times Marvell's
entire current annual revenue from a single discretionary relationship. The
filing is explicit that purchases are discretionary: nothing obligates Google
to spend a dollar [^1]. Reuters itself framed the package as "up to" $12.2
billion [^3], and the XenoSpectrum tear-down makes the distinction directly:
$120 billion is neither a purchase commitment nor a revenue forecast —
it is the cumulative amount needed for maximum vesting [^9].

What the 240-tranche ceiling *does* communicate is a price for work, not a
promise to buy. At the strike, each $500 million tranche is worth about $49.6
million to Google — a ~9.9% equity kicker on every increment of
custom-silicon revenue at the exercise price [^2][^4]. Because the kick is
constant per dollar, it behaves less like a threshold reward and more like a
per-unit commission Google pays itself in its supplier's stock. And because
the kick is *equity*, its value is levered on Marvell's share price: at the
August 21 close of $237.04, the full warrant's intrinsic value was about $1.8
billion — roughly $30 of spread per share on top of the $12.2 billion
aggregate exercise price [^13][^4].

:::line-chart(title="MRVL monthly close, 12 months", subtitle="Yahoo Finance, month-end; the vertical gap marks the Aug 18 warrant strike", y-unit=$)
x: 2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06,2026-07,2026-08
MRVL: 84.07,93.74,89.40,84.98,78.92,81.69,99.05,165.15,205.00,297.89,187.56,237.04
:::

:::source
Yahoo Finance daily/monthly closes via query API, retrieved 2026-08-22 [^13].
:::

:::statement(attr="ARA Research")
The warrant is not a $12.2B investment and not a $120B commitment. It is a
volume-linked equity rebate — Google pays itself about 10% of each
$500M it spends, in Marvell stock, if the stock keeps going up.
:::

## 02. Inside the ladder: revenue that discounts itself

The "Qualifying Revenue" that moves the tranches is narrower than Google's
total checkout at Marvell. Qualifying Products are custom semiconductors
developed under written Statements of Work in which Google holds a "Sale
Control Right" — the right to decide whether Marvell may sell the
product to anyone else — plus any products the parties add by written
agreement [^2]. The definition also says revenue is measured under Marvell's
normal GAAP recognition, "adjusted to exclude any contra revenue impact
resulting from any allocation of the value of this Warrant" [^2]. That
carve-out is itself the tell: Marvell recognizes customer warrants *as a
reduction to revenue* as the tied revenue vests, and the parties wrote the
tranche hurdle to ignore that haircut [^9][^2].

This is the trap in headline revenue math. The fiscal 2025 customer warrant
— issued December 2024 to a buyer identified in the press as Amazon Web
Services, 4.2 million shares at an $87.77 strike — was valued at $54.44
per share by Black-Scholes, a $227.6 million total, and is booked into the
income statement as contra-revenue over its vesting life [^8][^12]. The Google
warrant is roughly 14 times the share count of that AWS award at a 2.4 times
higher strike [^12][^2]. If the fair-value-to-spot ratio lands anywhere near
the fiscal 2025 precedent (about half of spot), the Google warrant's
Black-Scholes value would run to the multiple-billions — a
contra-revenue stream sitting directly on top of the very revenue numbers the
street will use to track the deal (ARA estimate) [^8][^2]. Neither party has
disclosed the valuation model yet; the next 10-Q will, as it must.

The contract also quietly names a product. The warrant defines "Kestrel
Product Launch" as the date Google completes qualification of the final
production version of a custom product codenamed Kestrel, and Google cannot
transfer non-affiliate warrant interests before the earlier of November 10,
2027 or that launch [^2][^9]. Marvell's 8-K lists the agreement's scope as AI
inference accelerators, storage controllers, network interface controllers,
memory interface controllers, and near-memory compute — the silicon
ring around the TPU rather than the TPU die itself [^1][^21]. XenoSpectrum's
reading holds: the contract "distributes responsibility across an entire
system," and says nothing about who designs the core TPU [^9].

:::callout(kind=info, label="How to read the tranche table")
Cumulative Qualifying Revenue is the only input; each $500M milestone vests
one block. The table converts plausible annual purchase tracks into shares
vested, dilution against 875.6M shares outstanding, and intrinsic value to
Google at the August 21, 2026 close — ARA analysis built directly from
the warrant's 240,042-share tranche size [^2][^13][^8][^16].
:::

:::exhibit(num="Exhibit 1", title="What each qualifying-revenue track buys Google", subtitle="Vested performance shares, dilution, and intrinsic value at $237.04 (strike $206.58)", source="Marvell warrant Exhibit 4.1; Marvell 10-Q; Yahoo Finance; ARA analysis", note="Full vest only at $120B cumulative. Time-based 1.36M shares vest regardless. Scenario math, not a forecast.")
| Avg. annual qualifying revenue | Cumulative (6.5 yrs) | Tranches | Shares vested | Dilution | Intrinsic at close |
|---|---|---|---|---|---|
| $1.0B | $6.5B | 13 | 3.1M | 0.36% | ~$0.10B |
| $2.5B | $16.3B | 32 | 7.7M | 0.88% | ~$0.23B |
| $5.0B | $32.5B | 65 | 15.6M | 1.78% | ~$0.48B |
| $10.0B | $65.0B | 130 | 31.2M | 3.56% | ~$0.95B |
| *$18.5B* | *$120.3B* | *240 (full)* | *57.6M* | *6.58%* | *~$1.75B* |
:::

## 03. Full vest is priced like a decade of Google custom silicon

The bull case treats $120 billion as a proxy for Google's multi-year
TPU-ecosystem spend, and as a scale sanity check that is not absurd at
Alphabet's size. Alphabet spent $44.9 billion on capex in calendar Q2 2026
alone and $132 billion over the trailing twelve months — so $120 billion
of qualifying purchases is roughly nine to ten months of the current capex
base, fully allocable to custom silicon [^4][^20]. Bloomberg reported the deal the
same way Reuters did: it could "generate up to $120 billion in revenue for
Marvell through fiscal 2033" [^11].

:::bar-chart(title="The $120B ceiling vs. the denominators that give it scale", subtitle="$ billion", value-unit=$, value-suffix=B)
categories: Marvell FY26 revenue, Full-vest ceiling, Alphabet TTM capex
value: 8.2, 120, 132
:::

:::source
Marvell 10-K FY2026; warrant terms; Alphabet Q2 2026 via The Motley Fool; ARA analysis [^8][^2][^20].
:::

The bear case is that the incentive is misaligned with the denominator.
Marvell's ten largest customers already deliver 82% of revenue, its largest
direct customer (Customer A) 14%, and a single distributor 37%; an expanding
Google program deepens that concentration rather than diversifying it [^8].
Full-vest dilution of ~6.6% lands on existing shareholders, and the strike
sits only about 4% below where the stock closed the day the warrant was
issued — if MRVL trades below $206.58, the entire performance warrant
is out of the money and Google's economic incentive to drive the ladder
collapses, at exactly the revenue levels that are supposed to vest it
[^2][^4][^13]. The equity is a call option on Marvell, not a floor under it.

:::quote(attr="William Kerwin, Morningstar")
Google's chip budget is expanding to accommodate new suppliers rather than
displacing Broadcom as an incumbent.
:::

## 04. Equity-for-orders is becoming the hyperscaler template

The Google warrant is Marvell's third customer warrant and by far the largest.
December 2024: 4.2 million shares at $87.77 tied to AWS custom AI procurement,
per press accounts. December 2025: a 1.0 million-share warrant at $87.00
issued in the Celestial AI acquisition context, linked to photonic-fabric
revenue. August 2026: 58.97 million shares at $206.58 for Google [^8][^9][^12].
Press analysts describe Marvell as the only custom-silicon vendor with
warrants tied to two hyperscaler ecosystems, and the only firm designing
across all three big public clouds [^12].

The template extends beyond Marvell. In October 2025 AMD handed OpenAI a
warrant for up to 160 million shares (about 10% of AMD) at an exercise price
of one cent, vesting as GPU deployments scale and as AMD's stock hits price
targets, alongside a 6-gigawatt supply pact [^4][^10][^17]. Days before the Google
deal, Reuters reported Nvidia agreed to backstop up to $105 billion tied to
an Ohio data-center project OpenAI plans to lease [^10][^18]. The biggest buyers
of AI silicon have, in effect, started charging their suppliers — in
equity — for the privilege of supplying them [^4]. Google also gains
something subtler at the P&L level: Alphabet already books a large
equity-securities portfolio and recorded a $98 billion net gain in Q2 2026,
mostly unrealized gains on equity securities — Marvell warrant gains
would land in exactly that bucket [^4].

:::timeline
- {date: 2024-12, headline: "AWS/Marvell fiscal-2025 warrant", body: "4.2M shares at $87.77; $227.6M fair value; revenue-linked vesting through Jan 2030."}
- {date: 2025-10, headline: "AMD/OpenAI warrant", body: "Up to 160M AMD shares (~10%) at $0.01; deployment- and price-linked tranches."}
- {date: 2025-12, headline: "Marvell fiscal-2026 warrant", body: "1.0M shares at $87.00 issued alongside the Celestial AI acquisition; photonic-fabric revenue-linked vesting."}
- {date: 2026-04, headline: "Google launches 8th-generation TPUs", body: "TPU 8t (training) and TPU 8i (inference) announced; general availability later in 2026."}
- {date: 2026-07-29, headline: "Marvell/Google commercial agreement", body: "Custom TPU-ecosystem silicon scope signed."}
- {date: 2026-08-18, headline: "Google warrant issued", body: "58.97M shares at $206.58, 240-tranche ladder, expiry August 18, 2033."}
:::

## 05. What the warrant says about the TPU supplier web

Google's roadmap, per its April 2026 launch, is TPU 8t for training (a single
superpod scales to 9,600 chips and 121 ExaFlops) and TPU 8i for inference
(288GB HBM, 384MB on-chip SRAM, Axion host CPUs, doubled interchip bandwidth,
about 2x performance-per-watt over the prior-generation Ironwood) [^7].
Custom silicon around those parts is now explicitly multisourced. Broadcom's
April 6 8-K disclosed a long-term agreement to develop and supply Google's
*future* TPU generations plus a supply-assurance deal on next-generation
AI-rack networking through 2031, with Anthropic set to access roughly 3.5GW
of next-generation TPU compute capacity through Broadcom starting 2027 [^5].
MediaTek is producing its first U.S.-cloud AI ASIC in Q4 2026 and raised its
2027 AI-ASIC market-share target to 15-20% [^10][^15]. Tom's Hardware, citing
analysts, floats AMD on a 10th-generation TPU program [^10].

Marvell's slice — inference accelerators, storage controllers, network
interface controllers, memory interface controllers, near-memory compute
— fits the "system ring" reading: Marvell deepens its already-substantial
role around TPUs while the core die and the newest frontier-training parts
stay with Broadcom [^1][^9][^5]. The warrant is Google's tool for aligning
that ring. Because vesting is discretionary-purchase-based with no minimums,
the filing is simultaneously the strongest signal Google has given that the
TPU-ecosystem silicon spend will be large, and no commitment at all.
Morningstar's Kerwin frames the layout as Google growing the supplier pie
rather than rotating Broadcom out [^12][^19][^10].

:::note
The Reuters figure that a fully-exercised warrant makes Google Marvell's
"fifth-largest investor" reflects the aggregate exercise price — an
instrument value, not cash paid today [^3][^2].
:::

## 06. Analyst position: watch the tranche scorecard, not the headline

The most useful property of this structure is that it converts a confidential,
discretionary buying plan into a public, quarterly-measured scorecard.
Marvell's 10-Q policy already discloses vested shares under its customer
warrants, and the Google warrant's 240-milestone ladder guarantees that every
subsequent filing reveals exactly how many $500M tranches Google's
TPU-ecosystem spend has unlocked [^9][^8][^2][^23]. The first milestone ($500M
cumulative — about 0.4% of the full-vest pace) is plausibly reachable
within fiscal 2027-28. The five-to-ten-tranche band by fiscal 2029, the
midpoint of the ARA scenarios, corresponds to $2.5-5 billion of cumulative
Google custom-silicon revenue — at the low end of credible ramp tracks,
yet already a real, if modest, equity transfer to Google [^2][^13].

:::position(confidence=medium, horizon=2027-Q4)
stance: >-
  Read the warrant as a roughly 10% equity commission, at the strike, on
  TPU-ecosystem silicon Google would largely buy anyway; the quarterly
  tranche scorecard, not the $120B ceiling, is the tradeable signal.
consensus: >-
  The tape reads the $12.2B aggregate and the $120B ceiling as forward
  orders, and treats the deal as Broadcom-replacement news.
resolves: >-
  Cumulative qualifying revenue disclosures in Marvell 10-Qs; whether the
  Kestrel product qualifies before the November 10, 2027 gating date;
  whether Google waives the 4.999% beneficial-ownership cap; and whether
  GAAP revenue starts absorbing contra-revenue warrant charges.
:::

The two analytical bookends, then, are these. If Marvell's stock compounds
upward and Google's TPU-ecosystem purchases scale toward the multi-billion
per year range, the warrant quietly becomes one of the largest equity
transfers a supplier has ever made to its biggest customer — while
remaining pure optionality on Marvell's side, since Google never has to
exercise what it vests [^4][^2]. If the custom-silicon boom stalls, the
240-tranche ladder decays into a mostly-unvested curiosity [^9]. The deal's
honesty — discretionary purchases, sale-control rights, contra-revenue
carve-outs, a concrete named product — is the rare part of the
AI-infrastructure build-out that says precisely what it will and will not do.
The commitment is not $120 billion of orders; it is a standing offer from
Google to keep buying, priced to vest only as it does.

:::references
- {id: 1, title: "Marvell Technology Form 8-K — Google customary warrant and commercial agreement", url: "https://www.sec.gov/Archives/edgar/data/1835632/000119312526356217/d412696d8k.htm", source: "SEC EDGAR", date: "2026-08-18"}
- {id: 2, title: "Marvell–Google Warrant to Purchase Common Stock (Exhibit 4.1)", url: "https://www.sec.gov/Archives/edgar/data/1835632/000119312526356217/d412696dex41.htm", source: "SEC EDGAR", date: "2026-08-18"}
- {id: 3, title: "Marvell grants Google $12.2 billion stock warrant in AI chip deal", url: "https://finance.yahoo.com/technology/ai/articles/marvell-grants-google-12-2-133101313.html", source: "Reuters (via Quartz/Yahoo Finance)", date: "2026-08-19"}
- {id: 4, title: "Google Is Getting Paid in Marvell Stock Warrants for Buying Marvell's Chips", url: "https://www.fool.com/investing/2026/08/21/google-is-getting-paid-in-marvell-stock-warrants-for-buying-marvell-s-chips/", source: "The Motley Fool", date: "2026-08-21"}
- {id: 5, title: "Broadcom Inc. Form 8-K — Google TPU long-term agreement and Anthropic capacity", url: "https://www.sec.gov/Archives/edgar/data/1730168/000119312526144028/d87999d8k.htm", source: "SEC EDGAR", date: "2026-04-06"}
- {id: 6, title: "Marvell Shares Surge After Google Warrant Deal Tied to Custom Chips", url: "https://finance.yahoo.com/technology/articles/marvell-shares-surge-google-warrant-132458296.html", source: "Yahoo Finance", date: "2026-08-19"}
- {id: 7, title: "Our eighth generation TPUs: two chips for the agentic era", url: "https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/eighth-generation-tpu-agentic-era/", source: "Google (blog)", date: "2026-04-22"}
- {id: 8, title: "Marvell Technology Form 10-K, year ended January 31, 2026", url: "https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm", source: "SEC EDGAR", date: "2026-03-11"}
- {id: 9, title: "Why Google's Marvell Chip Deal Doesn't Replace Broadcom", url: "https://xenospectrum.com/en/google-marvell-custom-chip-warrant/", source: "XenoSpectrum", date: "2026-08-21"}
- {id: 10, title: "Marvell, AMD Reportedly Shake Up Google TPU Race, Putting Broadcom, MediaTek Under Pressure", url: "https://www.trendforce.com/news/2026/08/20/news-marvell-amd-reportedly-shake-up-google-tpu-race-putting-broadcom-mediatek-under-pressure/", source: "TrendForce", date: "2026-08-20"}
- {id: 11, title: "Marvell gives Google option to buy $12.2 billion stake in custom AI chip deal", url: "https://www.predictionmarkets.org/marvell-gives-google-option-to-buy-12-2-billion-stake-in-custom-ai-chip-deal/", source: "Reuters/Bloomberg (aggregator)", date: "2026-08-20"}
- {id: 12, title: "Marvell grants Google 7% warrant in $12.2 billion custom chip deal", url: "https://edgen.dev.edgen.tech/news/post/marvell-grants-google-7-warrant-in-122-billion-custom-chip-deal", source: "Edgen News", date: "2026-08-22"}
- {id: 13, title: "Market data: MRVL daily and monthly closes (Yahoo Finance query API)", url: "https://query1.finance.yahoo.com/v8/finance/chart/MRVL", source: "Yahoo Finance (market data)", date: "2026-08-22"}
- {id: 14, title: "Market data: AVGO daily closes (Yahoo Finance query API)", url: "https://query1.finance.yahoo.com/v8/finance/chart/AVGO", source: "Yahoo Finance (market data)", date: "2026-08-22"}
- {id: 15, title: "MediaTek 2026 Q2 quarterly earnings release — AI ASIC production timing and SAM", url: "https://www.mediatek.com", source: "MediaTek (via TrendForce/XenoSpectrum)", date: "2026-07-31"}
- {id: 16, title: "Marvell Technology Form 10-Q, first quarter fiscal 2027", url: "https://www.sec.gov/Archives/edgar/data/1835632/000183563226000019/mrvl-20260502.htm", source: "SEC EDGAR", date: "2026-05-28"}
- {id: 17, title: "AMD–OpenAI warrant structure (October 2025) coverage", url: "https://www.trendforce.com/news/2026/08/20/news-marvell-amd-reportedly-shake-up-google-tpu-race-putting-broadcom-mediatek-under-pressure/", source: "TrendForce; The Motley Fool", date: "2026-08-20"}
- {id: 18, title: "Nvidia to backstop up to $105 billion tied to Ohio data-center project (Reuters)", url: "https://www.trendforce.com/news/2026/08/20/news-marvell-amd-reportedly-shake-up-google-tpu-race-putting-broadcom-mediatek-under-pressure/", source: "Reuters (via TrendForce)", date: "2026-08-20"}
- {id: 19, title: "Morningstar analyst William Kerwin on Google supplier multisourcing", url: "https://edgen.dev.edgen.tech/news/post/marvell-grants-google-7-warrant-in-122-billion-custom-chip-deal", source: "Morningstar (via Edgen/TrendForce)", date: "2026-08-22"}
- {id: 20, title: "Alphabet second-quarter 2026 results — capex $44.9B, $132B TTM, $98B other income", url: "https://www.fool.com/investing/2026/08/21/google-is-getting-paid-in-marvell-stock-warrants-for-buying-marvell-s-chips/", source: "Alphabet (via The Motley Fool)", date: "2026-08-21"}
- {id: 21, title: "Marvell grants Google 59M-share AI chip warrant — 8-K filing summary", url: "https://www.stocktitan.net/sec-filings/MRVL/8-k-marvell-technology-inc-reports-material-event-40642dab2018.html", source: "StockTitan (SEC 8-K mirror)", date: "2026-08-19"}
- {id: 22, title: "Marvell hands Google $12.2B warrant in custom-chip deal", url: "https://aiweekly.co/alerts/marvell-hands-google-122b-warrant-in-custom-chip-deal", source: "AI Weekly", date: "2026-08-19"}
- {id: 23, title: "Marvell issues warrant to Google for 58.97 million shares at $206.58", url: "https://cryptobriefing.com/marvell-google-warrant-custom-chips/", source: "CryptoBriefing", date: "2026-08-19"}
- {id: 24, title: "Marvell 8-K filing index (August 2026)", url: "https://www.sec.gov/Archives/edgar/data/1835632/000119312526356217/", source: "SEC EDGAR", date: "2026-08-19"}
:::
