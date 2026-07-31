---
eyebrow: POST-MORTEM · SITUATIONAL AWARENESS LP · 30 JULY 2026
title: The margin call that could not reach the Anthropic stake
domain: finance
deck: A correct secular thesis, expressed at four times gross in the most crowded factor on Wall Street, was liquidated
  whole in a single pre-open block. The half of the book nobody could margin-call is the half that survived — and that
  is a fact about plumbing, not about value.
lede: 'On 30 July 2026 Situational Awareness LP sold most of its public equity book — longs and shorts together — to
  Citadel in one block, as prime brokers Goldman Sachs, JPMorgan and Bank of America worked with it to meet margin
  requirements.[^1,15] Almost every number
  attached to that sentence in the press is a different layer of the same capital stack, and at least one of them is
  arithmetically impossible. This is an attempt to separate what is documented from what is recycled, to score
  Leopold Aschenbrenner''s 2024 thesis apart from the portfolio that expressed it, and to ask what it means that a
  roughly $5 billion private mark walked away untouched from a liquidation that consumed everything around it.'
stats:
- label: Q1 2026 13F book
  value: $13.68B
  note: 42 holdings, filed 2026-05-18[^2]
- label: Reported gross leverage
  value: ~4x
  note: anonymously sourced, never defined[^1]
- label: Worst July drawdown
  value: '-55%'
  note: SanDisk, 30 Jun to 29 Jul close[^3]
- label: Disclosed PB losses
  value: $0
  note: versus over $10B at Archegos[^4,5]
---

The forced unwind of Situational Awareness LP is being narrated as a blow-up, and the narration is running well ahead of the evidence. What is documented is narrow: a levered book was liquidated to a single buyer, the fund's assets fell sharply, and a private stake in Anthropic survived. What is asserted — a $45 billion fund, a 2,000% year, an Archegos repeat — is a mix of layered numbers, arithmetic that does not close, and an analogy that fails the only test an analogy has to pass.

:::callout(kind=info, label="The short answer")
- **The thesis did not break; the expression did.** The AI-buildout call has been directionally vindicated by realized capex, power scarcity and agentic capability trends. What broke was 4x gross leverage in the single most crowded factor in the market, where both legs of a nominal hedge were the same bet.[^6,7]
- **"Archegos" is the wrong analogy, and the reason matters.** Both books ran roughly 4x gross — so leverage is not the causal variable.[^4,34] What differs is instrument, conduct and exit: Archegos cost its lenders more than $10 billion, disclosed within one business day, and ended in a fraud conviction.[^5,8,32] Here, no counterparty loss has been disclosed, the book was 13F-visible, and one solvent buyer took it in a single negotiated block.[^2,34] The right precedents are Sowood and Amaranth.[^9,10]
- **Nearly every headline number is a different layer.** Form ADV regulatory AUM, the 13F long-and-put book, the public equity portfolio, fund AUM and peak total assets are five non-interchangeable quantities. Averaging them is malpractice.
- **The Anthropic stake survived because it could not be posted as collateral, not because it was correctly valued.** Those are separable claims, and only the first is supported.[^11,12]
- **The AI complex rebounded 18–31% the session the liquidation was reported.** That is the signature of a positioning event, not a repricing.[^3]
:::

## 01. Five numbers, one fund

Start with the layer problem, because everything downstream depends on it. The figures in circulation for "how big was Situational Awareness" are not competing estimates of one quantity. They measure five different things.

:::rank-list
- {label: "Peak total assets, early July (CNBC, single anonymous source)", value: $45B, pct: 100}
- {label: "Fund AUM, pre-sale (WSJ and CNBC's Faber)", value: $20-24B, pct: 53, highlight: true}
- {label: "Public equity book sold (Financial Times)", value: ~$16B, pct: 36}
- {label: "Q1 2026 13F filing value (EDGAR, verified)", value: $13.68B, pct: 30}
- {label: "Form ADV regulatory AUM (stale annual amendment)", value: $383M, pct: 1}
:::

Only one of these is a document you can read. Situational Awareness LP, CIK 0002045724, has filed six consecutive 13F-HRs. The Q1 2026 filing, submitted 18 May 2026, reports $13,676,657 thousand across 42 holdings; the Q4 2024 filing reported $254,813 thousand across six.[^2] That is a verifiable 54-fold increase in reportable US equity exposure in five quarters, and it is the only hard anchor in the entire record.

It is also badly misunderstood. Section 13(f) requires options to be reported at the market value of the underlying security, not at premium. Roughly $8.46 billion — 62% of the Q1 filing — was put-option exposure; the filing's four largest lines are SMH, NVDA, ORCL and AVGO puts.[^2,13] The disclosed long equity was closer to $5.2 billion. Anyone describing this as a "$13.7 billion hedge fund" is quoting a notional-inflated filing total as if it were fund size, and anyone describing the book as a pure long has not read it.

The $45 billion figure deserves particular scepticism. It rests on a single anonymous source, no outlet reconciles it against the Wall Street Journal's contemporaneous "$20 billion" reporting from 8 June 2026, and the leverage arithmetic does not close in either direction: 4x on $20-24 billion of AUM implies $80-96 billion of gross, not $45 billion, while $45 billion over $24 billion is 1.9x, not 4x.[^14,15] The two readings that survive are that $45 billion was peak levered assets against roughly $24 billion of equity, or that it was peak AUM in early July already compressed to $20-24 billion by month-end. The dates favour the second. Neither is confirmed.

### The performance figures do not all survive contact with arithmetic

Three return numbers circulate. Two are traceable; one is not.

| Claim | Earliest source | Window | Verdict |
|---|---|---|---|
| *+439% net | FT, from a 24 Jul 2026 investor letter | Calendar H1 2026, net | Single-sourced to a letter the FT read; the letter is not public[^16] |
| Over 1,000% since inception | WSJ, 8 Jun 2026 | Inception to about Jun 2026 | Traceable, but a June figure recycled into July coverage[^14] |
| About 270% in 2026 through May | WSJ, 8 Jun 2026 | Jan to May 2026 | Traceable[^14] |
| "Up 2,000% in 2025" | Untraced | Calendar 2025 | ==Arithmetically impossible as stated== |

The last row is worth showing rather than asserting. If the fund was up more than 1,000% since inception as of early June — call it 11.0x — and up roughly 270% in 2026 through May — 3.70x — then cumulative performance through 31 December 2025 was approximately 11.0 divided by 3.70, or about 2.97x, meaning roughly **+197%**.[^14] A genuine +2,000% in 2025 would be 21x, which compounded against a +439% first half would put the fund at roughly 113x since inception — an order of magnitude above the figure the Journal actually reported. The "2,000%" is best read as a factor-of-ten corruption of "roughly 200%." *This derivation is ours, not any outlet's.*

:::note
Throughout this piece, figures we computed rather than sourced are labelled as such. The distinction matters more than usual here: the entire event rests on anonymous sourcing, and there is no fund letter, no SEC filing and no on-the-record statement describing the transaction itself.
:::

## 02. The mechanism: why 4x gross has no buffer at inception

"Levered four times over" is repeated everywhere and defined nowhere. It is worth deriving what it can mean, because the arithmetic is the whole story.

Regulation T caps initial margin at 50%, which permits at most 2x long exposure in a conventional margin account.[^63] Four times gross is therefore unreachable under Reg T; it requires portfolio margin under FINRA Rule 4210(g) or synthetic financing. FINRA 4210(c) then sets ongoing maintenance at 25% of long market value and 30% of short.[^17] Take gross exposure at 4.0x NAV and apply a blended 25% requirement: equity divided by gross equals exactly 25.00%. **The book sits precisely on the maintenance floor before anything moves.**

:::compare
- {role: LOWEST, name: "Reg T maximum long exposure", value: 2.0x}
- {role: HIGHEST, name: "Long decline that exhausts equity, shorts flat", value: "-38.5%"}
- {role: SUBJECT, name: "Long decline that exhausts equity, shorts 10% adverse", value: "-33.1%"}
:::

Set NAV at 100 and split 4x gross into 2.6x long and 1.4x short — a long-tilted book, which the 13F composition supports. A 35% decline in the longs costs 260 times 0.35, or 91 points of equity. A simultaneous 10% adverse move in the shorts costs another 140 times 0.10, or 14 points. Total: **105 points of loss against 100 points of equity.** The fund is through zero, and the residual belongs to the prime brokers. *ARA arithmetic; the long/short split and blended requirement are assumed, not disclosed.*

The call fires long before that. At a 10% long decline, equity is 74 against gross of 374 — 19.8%, below the floor — requiring either 19.5 points of fresh cash or a forced sale of about 21% of gross.[^17] Realized July drawdowns in the named longs ran 36% to 55%.[^3] There was never a version of this month in which a 4x book survived without an outside capital injection, which is precisely what the 24 July letter was soliciting, effective 1 August.[^18] The capital did not arrive; the block cleared on 30 July.

:::statement(attr="ARA Research")
Leverage did not amplify a bad month. Leverage is what made this month unsurvivable at a drawdown the underlying thesis would have shrugged off.
:::

## 03. The hedge that was a second long

The received framing — long AI hardware, short AI-disrupted software — is half right and, in the half that matters, misleading.

The disclosed hedge in the Q1 2026 13F was not software shorts at all. It was $8.46 billion of put notional against **first-derivative** semiconductors, the two largest lines being $2.04 billion of SMH puts and $1.57 billion of NVDA puts, with further put exposure to Oracle and Broadcom.[^13] The long book was **second-derivative** infrastructure: SanDisk, CoreWeave, Nebius and Micron among the disclosed names,[^13] alongside Bloom Energy, IREN and Core Scientific in the filing itself.[^2] Those are different nodes of the same supply chain with different betas. When the complex broke, the longs fell two to four times harder than the instruments nominally hedging them — a basis mismatch, not a hedge.

Only one software short, Adobe, is named for this fund in any reporting.[^1] Everything else in the "AI losers" basket is the *generic* crowded short, and 13Fs never disclose short sales, so the true short book is unobservable. That is a limit on what anyone can honestly say, including us.

But the structural point holds regardless of the names. Consider the latent variable: call it the market-implied *rate* of AI capability diffusion. A long in AI hardware is a positive exposure to it — capex is the derivative of expected diffusion. A short in AI-disrupted software is also a positive exposure to it, because the short pays off precisely when diffusion is fast. **The two legs carry the same sign.** A dollar-neutral book of this construction is not hedged; it is roughly twice levered to one factor. Any downward revision in the *rate* — not the *fact* — of diffusion hits both legs from a single signal.

July 2026 delivered exactly that signal, twice. On 1 July, Bloomberg reported Meta preparing to rent out surplus AI compute under an internal programme called Meta Compute — a supply signal that broke the scarcity premium on AI hardware, and one the semiconductor complex sold off hard on.[^19] Then, from 22 July, software rallied on rotation rather than on news.

Single-name July 2026 moves in the crowded short, against the sector ETF:[^3]

:::bars
- {label: Workday, value: +29.2%, pct: 100}
- {label: "Adobe (reported no earnings in July)", value: +20.9%, pct: 72}
- {label: Salesforce, value: +15.4%, pct: 53}
- {label: ServiceNow, value: +10.9%, pct: 37}
- {label: "IGV software ETF", value: +3.0%, pct: 10}
:::

Adobe is the clean case. It reported no earnings in July. Morgan Stanley cut it to Underweight on 21 July with a price target of $240, and it then rose 20.9% on the month on no company news at all.[^20,21] A short with no remaining fundamental catalyst and record crowding behind it is not a position; it is a queue. Hedge funds had made roughly $24 billion shorting software in the first weeks of 2026 and increased the bet.[^22] The identical trade had already squeezed once, in May 2026, when software rebounded roughly 40% off its April low.[^64] The tail had been observed three months earlier and was not sized for.

The factor evidence is unambiguous. UBS's AI-capex basket trailed its AI-disruption basket by a record 42 percentage points in July.[^6] Goldman's US high-beta momentum basket fell roughly 37% — its worst month in a series going back to 1999, worse than 2000 or 2009 — after being up 57% in the first half at the 92nd percentile of five-year crowding.[^7]

**What would weaken this reading:** if the July decline had been driven by a genuine deterioration in AI-infrastructure fundamentals, the factor framing would be a rationalisation. The next section tests that directly.

## 04. The tape: concentrated, not uniform, and reversed on the day

The widely repeated "down 35% to 47% on the month" is not accurate as a month-to-date close-to-close figure. It is accurate only measured from the 30 June close to the 29 July trough — and even then the distribution is wider than the band suggests.

:::exhibit(num="Exhibit 1", title="Peak-to-trough, 30 June to 29 July 2026", subtitle="Indexed to 100 at the 30 June close", source="stockanalysis.com (S&P Global Market Intelligence); ARA calculation", note="SK hynix is measured on KRX, where the 30 July Korean session corresponds to the 29 July New York session.")
:::slope(left-label="30 Jun", right-label="29 Jul trough", unit=index)
| Name | 30 Jun | 29 Jul |
|---|---|---|
| SanDisk | 100 | 44.7 |
| SK hynix | 100 | 49.9 |
| Nebius | 100 | 53.7 |
| Bloom Energy | 100 | 54.1 |
| CoreWeave | 100 | 61.1 |
| Micron | 100 | 64.0 |
| SOXX | 100 | 72.6 |
| S and P 500 | 100 | 97.7 |
:::
:::

Three things fall out of that chart. First, the damage was concentrated in memory and neocloud-plus-power, not spread evenly: on a month-to-date basis Cipher Mining fell 7.5%, Core Scientific 14.8%, IREN 16.3%, Lumentum 19.2% and CoreWeave 25.8% — all well short of the reported band.[^3] Second, the S&P 500 was essentially flat, down 0.68% on the month, while the SOXX semiconductor ETF fell 21.3%.[^3] Damage concentrated beneath the index is the signature of positioning, not of a repriced macro variable. Third, every one of these names troughed on the same session: 29 July.

Was there a fundamental cause? The July earnings calendar says no. CoreWeave and Nebius reported nothing in July — their second-quarter dates were 11 and 12 August.[^23] Micron's last print, on 24 June, was a large beat: revenue $41.46 billion against $35.25 billion expected, with the stock up 15% after hours.[^24] SK hynix delivered the one genuine July negative on 28 July, a record quarter that still missed consensus on both revenue and operating profit as HBM long-term agreements damped short-term price elasticity.[^25] Its US listing — a roughly $26.5 billion Nasdaq ADR offering, described as the largest US share sale ever completed by a foreign company, with newly issued underlying shares additionally listing in Seoul on 29 July Korea time — landed directly into the Korean leveraged unwind.[^26]

The decisive test is Bloom Energy. On 28 July it reported record results: revenue $1,065.4 million, up 165.5% year over year, GAAP operating income of $182.2 million against a small loss a year earlier, and full-year guidance raised to $3.9-4.2 billion.[^27] The stock fell to its July low the next session anyway, then rose 26.5% on 30 July.[^3] **A beat-and-raise that cannot arrest a decline is not a fundamental repricing.**

Single-session moves on 30 July 2026, the day the forced seller was removed:[^3]

:::bars
- {label: "IREN, 30 July 2026 single session", value: +30.5%, pct: 100}
- {label: "Nebius", value: +27.1%, pct: 89}
- {label: "Bloom Energy", value: +26.5%, pct: 87}
- {label: "SanDisk", value: +26.0%, pct: 85}
- {label: "CoreWeave", value: +21.5%, pct: 70}
- {label: "Micron", value: +18.4%, pct: 60}
- {label: "SOXX (sector benchmark)", value: +8.5%, pct: 28}
- {label: "SPY (market benchmark)", value: +1.7%, pct: 6}
:::

**The honest caveat:** 30 July was confounded. The same session carried a Federal Reserve hold and a Microsoft print that sent the stock up sharply on Azure.[^3] But the internal structure of the rebound is still informative. Names not held by the fund but with comparable drawdowns — Lumentum, Intel, Coherent — rebounded 11-15%, roughly half the 18-31% snapback in the names being liquidated.[^3] That differential is what price-impact reversal looks like. It is consistent evidence, not proof.

Around this sat a genuine systemic de-grossing. Goldman's prime desk recorded information technology as the most net-sold US sector for a fourth consecutive week in the week to 3 July, and separately reported hedge funds cutting US tech exposure roughly 10% over eight weeks — the largest sector retreat in the history of its series.[^28,29] Asia fundamental long/short funds fell 18.6% month-to-date through 28 July, having been up 40% year-to-date on 22 July: 21 percentage points surrendered in six sessions, on the largest five-day cumulative de-grossing Goldman has on record.[^30] Credit joined in: five-year CDS on CoreWeave reached roughly 855 basis points and Oracle roughly 215, against about 145 at the end of 2023.[^31] Situational Awareness was the largest single casualty of that unwind, not its cause.

## 05. Is "Archegos" the right analogy? No, and the reason is the point

An analogy earns its keep by predicting the next thing. Archegos predicts multibillion-dollar counterparty losses, a systemic scare, criminal charges and regulatory reform. On the evidence available, none of that obtains here.

| Dimension | Archegos, March 2021 | Situational Awareness, July 2026 |
|---|---|---|
| Peak gross leverage | About 4.4x ($36B capital, $160B exposure)[^4] | About 4x, undefined, anonymously sourced[^34] |
| Instrument | Total return swaps: no 13F, no 13D/G[^4] | Cash equities and listed options; six 13F-HRs filed[^2] |
| Float concentration | Over 70% of GSX shares outstanding[^62] | 8.2% of Core Scientific; 2-5% elsewhere[^34] |
| Exit | Standstill refused; lenders raced for the exits[^32] | One negotiated block to one solvent buyer[^34] |
| *Counterparty losses | Over $10 billion, within one business day[^5,32] | None disclosed as of 31 July 2026 |
| Conduct | Convicted fraud; 18-year sentence[^8] | No allegation of fraud or misrepresentation |

The leverage was the same. That is exactly why leverage cannot be the distinguishing variable, and why "Archegos 2.0" is not merely lazy but actively misdirecting. It points risk attention at the failure mode that did not occur.

The three variables that genuinely diverge are instrument, conduct and exit structure. Archegos's swaps were the crime scene: each bank saw only its own slice, and Bill Hwang was convicted in July 2024 and sentenced to 18 years for deliberately misleading counterparties about exposure, concentration and liquidity.[^8] Situational Awareness filed quarterly. Its book was *directionally* visible — though not fully, since SK hynix is not 13F-reportable and options are reported by underlying notional without strike or expiry, so the put book's actual delta is unrecoverable from the filing.[^2,13]

The clean disanalogy is counterparty loss. Credit Suisse and Nomura both went public with Archegos losses on the first business day after the default, while rival lenders were still running for the exits.[^5,32] Two days after this block, no prime broker has disclosed anything. At 4x gross a 25% decline exhausts fund equity before the lender is touched: the losses landed on limited partners, not on lenders. That is not an absence of risk, it is the system working as designed — and it is an absence-of-evidence claim at T+1, not an audited zero. Third-quarter bank disclosures arrive in October.

:::callout(kind=warn, label="The risk that is still unguarded")
The specific Archegos disclosure gap was never closed. Proposed Rule 10B-1, the SEC's direct response requiring disclosure of large security-based swap positions, was formally withdrawn in June 2025.[^33] Rule 13f-2 survived but its first reporting period is January 2028. The multi-prime swap opacity that let one fund hide $160 billion is fully intact in 2026 — Situational Awareness simply did not use it. Calling this "Archegos 2.0" points attention away from the one failure mode still unguarded.
:::

The better precedents are Sowood Capital in July 2007 and Amaranth Advisors in September 2006: a levered fund's limited partners are wiped out, the book transfers whole to Citadel, and the financing counterparties take nothing. And at the market level, the July 2026 factor unwind rhymes with the August 2007 quant quake — a crowded-factor liquidation in which the most visible casualty was a symptom.

## 06. Why one buyer beat three sellers

Citadel has absorbed a distressed book whole four times before this one, and the outcomes split cleanly by deal shape.[^9,10,34]

:::timeline
- {date: 2006-09, headline: "Amaranth Advisors", body: "Energy book transferred to Citadel and JPMorgan at roughly 50 cents on the dollar after a loss above $6B; Amaranth later alleged a $1.85B concession payment in litigation."}
- {date: 2007-07, headline: "Sowood Capital", body: "A roughly $3B fund lost about half in under a month; Citadel bought the corporate bond and loan book and is reported to have made large profits as markets recovered."}
- {date: 2007-11, headline: "E-Trade", body: "A $2.55B cash injection plus purchase of an asset-backed portfolio with roughly $3B face value."}
- {date: 2021-01, headline: "Melvin Capital", body: "A $2.75B injection ($2B Citadel, $750M Point72) for a non-controlling revenue share; Citadel pulled $500M by August 2021 and Melvin shut in May 2022. The counter-example."}
- {date: 2026-07, headline: "Situational Awareness LP", body: "Entire public book, longs and shorts, in one pre-open block. Price and discount undisclosed. Millennium and Jane Street looked and did not participate."}
:::

The pattern splits cleanly by deal shape: buying *assets at a concession* made money; buying a *stake in a manager* did not. The Situational Awareness trade is the first shape.

Why Citadel rather than the banks working the book down over days? Derive it from market impact. Permanent price impact scales roughly with the square root of quantity over average daily volume, so multiples-of-volume supply is punitive and convex in duration. Residual variance over an n-day unwind scales with variance times n, and July realized daily volatility in these names plausibly ran 6-10%, which puts the one-standard-deviation residual over a five-day workout at 13-22% — larger than the entire equity cushion the brokers were protecting.[^34] On the short side, covering a crowded software short over days is a squeeze the broker triggers against itself; a block transfers it with zero buy-to-cover prints. And three prime brokers liquidating independently is a prisoner's dilemma that maximises aggregate impact. One block is the cooperative equilibrium. *This decomposition is ours; the volatility inputs are inferred from monthly drawdowns, not measured.*

The block converts unbounded, path-dependent gap risk into a fixed discount crystallised today. What that discount was, nobody has said.[^34] The instinct to reach for the 3-8% band typical of clean single-name blocks is wrong here; the correct comparable is Amaranth's roughly 50 cents on the dollar, because the price of a whole-book transfer is set by the seller's desperation, not by mark-to-market.[^9] That Millennium and Jane Street both evaluated the book without ultimately participating would have compressed the concession relative to a sole bidder.[^15,34]

Ken Griffin's own public posture is worth noting for what it says about motive. Asked at Davos in January 2026 whether AI was hype, he replied: "Of course! Of course! How else are you getting people to write 500 billion dollars worth of checks?" — while separately, in May, describing the technology's impact on society as obviously dramatic.[^35] That is the posture of someone buying a discount, not a thesis. *The Davos quote reaches us through aggregators rather than a World Economic Forum transcript; treat the wording as reported, not verified.*

## 07. Scoring the thesis, separately from the portfolio

Aschenbrenner's June 2024 essay is unusually scoreable because it committed to dated numbers. Its ladder: roughly 1 million GPUs, tens of billions of dollars and about 1GW for a 2026 cluster; about 10GW and hundreds of billions by 2028; about 100GW and a trillion dollars by 2030, which he noted would be "equivalent to >20% of US electricity production."[^36] Alongside that, AI reaching roughly 5% of US electricity by 2026 and 20% by 2028, and a $100 billion AI revenue run-rate by mid-2026.[^36]

| Forecast | Realized through July 2026 | Verdict |
|---|---|---|
| About 0.5 orders of magnitude a year of compute plus the same again in algorithmic gains | Independent audits put the combined rate near the midpoint | Confirmed |
| Test-time compute and "unhobbling" overhang | o1 shipped roughly four months after publication | Confirmed |
| Power, not chips, is the binding constraint | Over five-year median interconnection wait; PJM at the price cap | Confirmed[^37,38] |
| About $500B annual AI investment by 2026 | Big-four 2026 guidance about $720-745B | *Exceeded[^39,40] |
| About 1GW single training cluster by 2026 | Largest energized site near 0.9GW; Stargate at 0.3GW of 9GW planned | Early, mixed[^41] |
| $100B AI revenue run-rate by mid-2026 | Most generous aggregate about $60B on the essay's own definition | Missed |
| AI at about 5% of US electricity by 2026 | *All* US datacenters at 4.7% of US electricity in 2024 | Missed by about 3x[^58] |
| Export controls tighten; nationalisation by 2027 or 2028 | Controls loosened; no coalition, no Defense Production Act | Falsified |

The physics was right and the politics was wrong. Every forecast resting on an empirically lawful substrate — scaling curves, capex aggregates, power draw, benchmark saturation — landed or overshot. Every forecast resting on coalitional contingency failed, several in the opposite direction.

The single strongest piece of evidence in his favour is not capex. It is METR's agentic time-horizon series, which measures the length of task an agent completes at 50% success.

:::exhibit(num="Exhibit 2", title="METR 50% task-completion time horizon", subtitle="Minutes, frontier model at date of release", source="METR-Horizon-v1.1 benchmark results, retrieved 2026-07-31", note="METR states that measurements above 16 hours (960 minutes) are unreliable with its current task suite; the final two points sit in that regime.")
:::line-chart(title="50% time horizon", subtitle="minutes")
x: 2023-03,2023-11,2024-05,2024-10,2025-02,2025-04,2025-08,2025-11,2025-12,2026-02,2026-04
Frontier model: 3.99,4.04,6.99,20.52,60.39,119.73,203.01,292.99,352.25,718.81,1044.78
:::
:::

The trend has not merely held; it has accelerated. METR's own revised fit puts the 2023-onward doubling time at roughly 129 days — about 4.3 months — against the seven months in the original paper.[^43,44] But the instrument is failing in the direction of its own success. METR warns that measurements above 16 hours are unreliable with the current task suite, and the confidence intervals on the top points span nearly an order of magnitude.[^43] Its Frontier Risk Report separately found that on tasks over eight hours, at least 16% of successful runs were illegitimate on review — for one model, scoring those attempts as passes would have made the measured horizon roughly twice as large.[^45] Drop the two points above the reliability ceiling and the doubling time is about 5.4 months — still materially faster than seven, but the headline 4.3 is the top of the plausible range. *That recalculation is ours.*

Meanwhile the most aggressive professional forecasters shortened their estimates in 2026 and still land around mid-2028 for an "automated coder" — a bar weaker than AGI.[^46] Aschenbrenner's 2027 is not falsified; it resolves in January 2028. But the bar he set is explicitly unmet, and the two series that would both have to run hot are sending opposite signals: the agentic horizon accelerated, while single-cluster scale, lab revenue and autonomous AI research all lag.

### The unit error that reconciles everything

Here is the reconciliation that most commentary misses. His dollar rungs are being met while his power rungs are not, and the reason is a unit-cost assumption.

His 2026 rung pairs "tens of billions of dollars" with about 1GW — implying something near $10 billion per gigawatt.[^36] Realized all-in cost, including silicon, runs closer to $35-40 billion per gigawatt.[^41] **The dollar milestones therefore arrive roughly four times earlier than the power milestones they were meant to describe.** A "$100 billion cluster" on 2026 economics is about 2.5GW, not 10GW; a "$1 trillion cluster" is about 25GW, not 100GW. Anyone reading the ladder as a power forecast off the dollar headlines is off by a factor of four in the optimistic direction.

The physical constraint that binds is not capital and not chips. It is energization. LBNL's Queued Up 2026 edition reports a median interconnection-request-to-commercial-operation duration of over five years for projects built in 2025, with only 13% of 2000-2020 queue capacity reaching commercial operation and 75% withdrawn.[^37] As of April 2026, six of OpenAI's seven US Stargate sites were at zero megawatts energized against more than 9GW planned.[^41] And the demand simply has not shown up in the aggregate: US net generation grew 2.8% in 2025 to 4,430 billion kilowatt-hours — not by the "tens of percent" the thesis requires.[^42] All US datacenters together, AI and conventional, drew 192 TWh in 2024, or 4.7% of national consumption.[^58]

**What would falsify this section's reading:** if 2027 delivers a model that autonomously conducts end-to-end AI research, the "right physics, wrong date" framing collapses into "right, and early." That is a live possibility, not a rhetorical concession.

## 08. The private-mark asymmetry

The fund's public book absorbed 100% of the deleveraging. Its roughly $5 billion Anthropic stake absorbed none. The tempting inference — that private AI marks are inflated and public proxies took the pain the privates deserved — is not supported by the evidence, and the reason it is not supported is more interesting than the inference.

Two claims are being conflated, and they are separable:

:::kv
- {term: "The collateral claim", def: "A private mark cannot be posted as variation margin, so it cannot be liquidated to meet a call. Supported."}
- {term: "The valuation claim", def: "A private mark is therefore held above its true clearing price. Not supported by anything in the record."}
- {term: "The accounting claim", def: "A fund is entitled to freeze a Level 3 mark at the last round price. False as a matter of GAAP."}
:::

Take them in order. The collateral claim holds, but not for the reason usually given. Private stakes *are* financeable: NAV lending reached a record $23 billion across 38 KBRA-rated transactions in 2025.[^47] But 84% of surveyed loans carry loan-to-value ratios of 20% or lower, against advance rates above 50% on listed equity.[^48] A private stake can be borrowed against; it cannot be *levered* at a scale that would force liquidation. The operative consequence inverts the usual framing: because the private stake could not carry leverage, **the public book carried all of it, and therefore ate all of the forced selling.**

The accounting claim is simply wrong. ASC 820-10-35-24C requires that valuation techniques be calibrated so they reflect observable market data at the measurement date.[^49] There is no "hold at last round" exemption. The real position is weaker than the entitlement and more revealing than it: discretion sits in *how much* to calibrate, never in *whether*. And ==the enforcement record we could locate covers only affirmatively inflated or fabricated marks — we found no action premised on a manager simply failing to write down a stale venture position==. The deterrent against carrying a mark too long is therefore largely theoretical, which is itself the finding.

The valuation claim is where the evidence turns hostile to the intuitive story.

:::exhibit(num="Exhibit 3", title="Anthropic post-money valuation by round", subtitle="$ billion", source="Anthropic company announcements; Series H announced 2026-05-28")
:::line-chart(title="Post-money valuation", subtitle="$ billion", y-unit=$)
x: 2023-12,2025-03,2025-09,2026-02,2026-05
Anthropic: 18.4,61.5,183,380,965
:::
:::

The ladder ran from $18.4 billion at the end of 2023 to $380 billion at the Series G in February 2026.[^56] The Series H then closed on 28 May 2026 at a $965 billion post-money on $65 billion raised — and Anthropic's own announcement names Situational Awareness LP among the participating investors.[^50] So the $5 billion is not a third-party guess; it is a round-participation mark. The reported figure was struck on 30 July, **63 days after the last priced round**, which means it excludes July's public repricing by construction, not by choice.[^11,50]

Did the private market itself move? The last observable secondary print, dated 9-13 July 2026, put Anthropic at an implied $1.2 trillion — a roughly 24% **premium** to the primary round, inverting the normal illiquidity discount.[^51] That is the single most damaging fact for the naive version of this article's thesis, and it deserves to be stated plainly rather than buried. It is also dated *before* the late-July drawdown. A systematic search across the main secondary platforms found **no dated secondary observation at all for the 20-30 July window**.[^51] The honest statement is not "secondaries did not fall." It is: *no public secondary print exists for the selloff window.*

So where is the asymmetry actually provable? Not in the private marks. In the publicly quoted wrappers that hold them.

:::exhibit(num="Exhibit 4", title="Two listed vehicles holding private AI stakes", subtitle="Market price versus last reported net asset value", source="Fundrise Innovation Fund Form N-CSR; stockanalysis.com", note="Both NAVs predate the July 2026 drawdown. The VCX premium figures are third-party computations, not fund-reported.")
| Vehicle | Last reported NAV | NAV date | Market observation |
|---|---|---|---|
| *Fundrise Innovation Fund (VCX) | $18.97 a share; Anthropic 16.5% of net assets | 2026-03-31 | Closed $86.43 on 30 June (a 356% premium) and $35.14 on 30 July (an 85% premium) |
| Destiny Tech100 (DXYZ) | ==$19.97 a share, last publicly reported== | 2025-12-31 | Closed $23.50 on 2026-07-30 against a 52-week high of $72.87 |
:::

VCX is the cleanest datapoint available.[^52] Its SEC-filed net asset value was struck on 31 March and did not move; the market's price for that same portfolio fell from $86.43 on 30 June to $35.14 on 30 July — **59% in a single month**, collapsing the premium to reported NAV from about 356% to about 85%.[^3,52] Nothing inside the fund was re-marked. DXYZ corroborates from a different angle: its last publicly reported NAV was struck seven months before the drawdown, and the shares fell from a 52-week high of $72.87 to $23.50 on 30 July.[^53] In both cases the *mark* did not move and the *price* did. That is the asymmetry, and it is a statement about reporting cadence, not about fraud.

### What this does to reported AUM

The arithmetic is mechanical and worth stating explicitly. On reported figures, a roughly $5 billion stake inside a roughly $20 billion fund is about 25% of net asset value. Liquidate the public book down to a roughly $10 billion residual and the same unchanged asset becomes about 50%.[^11] *ARA arithmetic; the residual explicitly still contains public stocks and other privates, so the true post-event private share is unknown and could be higher.*

:::compare
- {role: LOWEST, name: "Anthropic stake, share of NAV pre-unwind", value: ~25%}
- {role: HIGHEST, name: "Anthropic stake, share of NAV post-unwind", value: ~50%}
- {role: SUBJECT, name: "Change in the Anthropic position itself", value: "0%"}
:::

Generalise that across AI-exposed funds and the implication is uncomfortable: in a drawdown, the price-discovered portion of a book shrinks and the non-price-discovered portion mechanically grows as a share of reported net asset value. Reported returns across the sector will therefore be smoothed by construction, and the smoothing is largest exactly when public marks are most stressed. The 2022 control case says the marks do eventually move — Tiger Global's hedge fund fell 52% that year and wrote down its venture positions by about 33% across it — but with a two-to-four-quarter lag absorbed by liquidity terms, side pockets and gates.[^54]

### Is the surviving stake more honest or less?

Both, along different axes, and the distinction is worth keeping.

As a *measurement*, it is less honest: it is the half of the book that has not been tested by a price, carried off a 63-day-old round, and it is now half of what the fund reports. As an *expression of the thesis*, it is arguably more honest. Bloom Energy's share price is a claim about behind-the-meter power procurement economics wrapped in three layers of market sentiment; a stake in Anthropic is closer to the object of the original essay. The fund lost the leveraged proxies and kept the thing itself. Whether that is a consolation depends entirely on a price nobody has been asked to pay.

## 09. What would break this thesis

Five ways this reading could be wrong, ranked by how much damage each would do.

**1. A prime-brokerage loss surfaces in October.** The entire Archegos disanalogy rests on zero disclosed counterparty losses at T+1. That is an absence-of-evidence claim, and third-quarter 2026 bank disclosures are not due until October. The Archegos precedent argues strongly against it — Credit Suisse and Nomura both announced within one business day — but the window is open.[^5]

**2. The "down 67% in July" figure is real and worse than modelled.** A single Wall Street Journal headline dated 31 July reports the fund down 67% on the month.[^61] It appears in exactly one item, its body is paywalled, and no outlet has published a post-unwind year-to-date or since-inception return. If that is a fund-level net monthly return, then compounded against +439% the fund is still up roughly 78% year to date and roughly 263% since inception — which would make "collapse" the wrong word entirely. If it instead measures something else, or if the residual $10 billion is impaired further, the arithmetic changes. *This compounding is ours; nobody has published it. We flag it precisely because the answer is load-bearing and unavailable.*

**3. The private mark is the thing that is wrong.** Our claim is only that no evidence establishes the Anthropic mark is inflated, and that the last observable secondary print was a 24% premium.[^51] But note what that print is: the source giving the $1.2 trillion level ==does not disclose the transaction volume behind it==, and completed secondary deals in these names are reported as scarce.[^51] A $5 billion block is a qualitatively different transaction from the trades that set an indicative level. Both the carrying mark and the secondary premium are prices for quantities nobody has actually transacted. That is a liquidity argument, and it cuts in whichever direction the first real block goes.

**4. The buildout genuinely is decelerating and July was early, not wrong.** The bearish case has real content. Alphabet printed its first negative quarterly free cash flow as a public company, at minus $5.9 billion, while raising capex.[^39] Oracle's fiscal 2026 free cash flow was minus $23.7 billion.[^40] ==Sell-side estimates we could not independently verify put capex near 94-100% of hyperscaler operating cash flow against a roughly 40% decade average==, and the marginal dollar is increasingly funded through special-purpose vehicles and project debt rather than operating cash. The credit market agrees: five-year CDS on Oracle reached roughly 215 basis points and on CoreWeave roughly 855 into late July.[^31] Set against that: every one of the big four *raised* 2026 guidance in the last week of July, and Microsoft's apparent $15 billion cut was an accounting reclassification following an extension of datacenter useful life from 15 to 25 years — a change that also flatters future reported earnings.[^55] Nobody has guided capex down. Yet.

**5. Archegos is right and we are early.** If a regulatory inquiry emerges from the 24 July capital solicitation — a letter framing the selloff as a buying opportunity and inviting fresh money six days before a forced liquidation — the conduct axis of the comparison changes.[^18] Nothing has been alleged. The fact pattern is the one a plaintiff would reach for.

An adversarial pass over this article's three most load-bearing claims — that no prime broker has disclosed a loss, that the July decline was a positioning event rather than a repricing, and that the Anthropic mark survived on collateral mechanics rather than on valuation — found no contradicting source for any of the three across roughly a dozen independent retrievals. **Red-team pass: 3/3 top claims unbroken.** That raises shipping confidence; it does not convert an absence-of-evidence claim into a positive one, and the October bank disclosures remain the real test of the first.

:::callout(kind=danger, label="What this episode does not settle")
It does not settle whether AI infrastructure is overvalued. A forced seller's price is information about the seller. The July drawdown was concentrated beneath a flat index, reversed 18-31% the session the forced seller was removed, and occurred while the affected companies were reporting record results and their customers were raising capital-expenditure guidance.[^3,27,39] Read as a verdict on AI capex, this event says almost nothing. Read as a verdict on running a correct long-horizon view through 4x gross leverage in the most crowded factor on the tape, it says everything.
:::

:::statement(attr="ARA Research")
A thesis is a claim about the world. A portfolio is a claim about the world plus a claim about your own solvency along the path. Situational Awareness was mostly right about the first and mispriced the second, and only one of those two is margin-callable.
:::

:::source
Verified primary anchors: SEC 13F-HR filings for CIK 0002045724; Anthropic Series F, G and H announcements; the Bloom Energy second-quarter 2026 Form 8-K; FINRA Rule 4210; LBNL and EIA datasets; METR benchmark data. Every fund-level figure describing the 29-30 July transaction is anonymously sourced and should be read accordingly. Market data as of the 30 July 2026 close.
:::

:::references
- {id: 1, title: "AI investor Leopold Aschenbrenner forced to unwind all public stock positions after steep losses, sources say", url: "https://www.cnbc.com/2026/07/30/leopold-aschenbrenners-hedge-fund-is-facing-steep-ai-losses.html", source: CNBC, date: "2026-07-30"}
- {id: 2, title: "Situational Awareness LP, 13F-HR filing history, CIK 0002045724", url: "https://13f.info/manager/0002045724-situational-awareness-lp", source: "EDGAR via 13f.info", date: "2026-05-18"}
- {id: 3, title: "Daily price histories: CRWV, SNDK, NBIS, BE, MU, IREN, CIFR, CORZ, LITE, INTC, COHR, WDAY, CRM, NOW, ADBE, IGV, SOXX, SPY, QQQ, VCX", url: "https://stockanalysis.com/stocks/sndk/history/", source: "stockanalysis.com (S&P Global Market Intelligence)", date: "2026-07-30"}
- {id: 4, title: "SEC Charges Archegos and its Founder with Massive Market Manipulation Scheme", url: "https://www.sec.gov/newsroom/press-releases/2022-70", source: "US Securities and Exchange Commission", date: "2022-04-27"}
- {id: 5, title: "UBS, Nomura push global banks' Archegos losses over $10 billion", url: "https://www.cnbc.com/2021/04/27/ubs-nomura-push-global-banks-archegos-losses-over-10-billion.html", source: CNBC, date: "2021-04-27"}
- {id: 6, title: "Dramatic Reversal in the AI Trade Looks Overdone: Taking Stock", url: "https://www.bloomberg.com/news/articles/2026-07-29/dramatic-reversal-in-the-ai-trade-looks-overdone-taking-stock", source: Bloomberg, date: "2026-07-29"}
- {id: 7, title: "Goldman's high-beta momentum basket on track for worst monthly performance", url: "https://app.hedgeye.com/insights/185196-goldman-s-high-beta-momentum-basket-on-track-for-worst-monthly-perform?type=macro", source: Hedgeye, date: "2026-07-28"}
- {id: 8, title: "Founder And Head Of Archegos Capital Management Bill Hwang Sentenced To 18 Years In Prison", url: "https://www.justice.gov/usao-sdny/pr/founder-and-head-archegos-capital-management-bill-hwang-sentenced-18-years-prison", source: "US Department of Justice, SDNY", date: "2024-11-20"}
- {id: 9, title: "Amaranth Turns the Tables, Sues Former Bankers for $1B", url: "https://www.naturalgasintel.com/news/amaranth-turns-the-tables-sues-former-bankers-for-1b-2/", source: "Natural Gas Intelligence", date: "2007-11"}
- {id: 10, title: "Sowood Capital", url: "https://en.wikipedia.org/wiki/Sowood_Capital", source: Wikipedia, date: "2007-07-31"}
- {id: 11, title: "AI hedge fund Situational Awareness may have sold its public portfolio, but it still has its Anthropic shares", url: "https://techcrunch.com/2026/07/30/ai-hedge-fund-situational-awareness-may-have-sold-its-public-portfolio-but-it-still-has-its-anthropic-shares/", source: TechCrunch, date: "2026-07-30"}
- {id: 12, title: "The Situational Awareness unwind and the AI collateral fault line", url: "https://www.ctol.digital/news/situational-awareness-unwind-ai-collateral-fault-line/", source: "CTOL Digital", date: "2026-07-30"}
- {id: 13, title: "Situational Awareness sells public equities book following steep losses", url: "https://finance.yahoo.com/markets/stocks/articles/situational-awareness-sells-public-equities-140824582.html", source: "Blockspace via Yahoo Finance", date: "2026-07-30"}
- {id: 14, title: "Leopold Aschenbrenner's Situational Awareness Surpasses $20 Billion as AI-Focused Hedge Fund Gains 270% in 2026", url: "https://www.barchart.com/story/news/2370002/leopold-aschenbrenners-situational-awareness-surpasses-20-billion-as-ai-focused-hedge-fund-gains-270-in-2026", source: "Barchart, syndicating the Wall Street Journal", date: "2026-06-09"}
- {id: 15, title: "Citadel Buys Most of AI Hedge Fund Situational Awareness' Public Portfolio After Tech Selloff", url: "https://www.citybiz.co/article/882039/citadel-buys-most-of-ai-hedge-fund-situational-awareness-public-portfolio-after-tech-selloff/", source: citybiz, date: "2026-07-30"}
- {id: 16, title: "Can the Situational Awareness hedge fund raise capital after its 439% H1 gain?", url: "https://www.disruptionbanking.com/2026/07/30/can-the-situational-awareness-hedge-fund-raise-capital-after-its-439-h1-gain/", source: "Disruption Banking", date: "2026-07-30"}
- {id: 17, title: "FINRA Rule 4210, Margin Requirements", url: "https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210", source: FINRA}
- {id: 18, title: "AI wizkid Leopold Aschenbrenner seeks new funds after AI rout", url: "https://www.investing.com/news/stock-market-news/ai-wizkid-leopold-aschenbrenner-seeks-new-funds-after-ai-rout--report-4823476", source: "Investing.com, relaying the Financial Times", date: "2026-07-30"}
- {id: 19, title: "Meta, like SpaceX, looks to turn excess AI compute into cash", url: "https://techcrunch.com/2026/07/01/meta-like-spacex-looks-to-turn-excess-ai-compute-into-cash/", source: "TechCrunch, relaying Bloomberg", date: "2026-07-01"}
- {id: 20, title: "Morgan Stanley cuts Adobe stock rating on AI risks, slashes target to $240", url: "https://www.investing.com/news/analyst-ratings/morgan-stanley-cuts-adobe-stock-rating-on-ai-risks-slashes-target-to-240-93CH-4801949", source: "Investing.com", date: "2026-07-21"}
- {id: 21, title: "Adobe daily price history", url: "https://stockanalysis.com/stocks/adbe/history/", source: "stockanalysis.com", date: "2026-07-30"}
- {id: 22, title: "Hedge funds made $24 billion shorting software stocks so far in 2026, and they are increasing the bet", url: "https://www.cnbc.com/2026/02/04/hedge-funds-made-24-billion-shorting-software-stocks-so-far-in-2026-and-they-are-increasing-the-bet.html", source: "CNBC, citing S3 Partners", date: "2026-02-04"}
- {id: 23, title: "CoreWeave Announces Date of Second Quarter 2026 Financial Results and Conference Call", url: "https://investors.coreweave.com/news/news-details/2026/CoreWeave-Announces-Date-of-Second-Quarter-2026-Financial-Results-and-Conference-Call/default.aspx", source: "CoreWeave Investor Relations", date: "2026-07-27"}
- {id: 24, title: "Micron Technology, Inc. Reports Record Results for the Third Quarter of Fiscal 2026", url: "https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-record-results-third-quarter", source: "Micron Investor Relations", date: "2026-06-24"}
- {id: 25, title: "SK hynix Q2 2026 Business Results", url: "https://news.skhynix.com/en/q2-2026-business-results/", source: "SK hynix Newsroom", date: "2026-07-28"}
- {id: 26, title: "SK hynix Lists ADRs on Nasdaq", url: "https://news.skhynix.com/en/skhynix-lists-adrs-on-nasdaq/", source: "SK hynix Newsroom", date: "2026-07-10"}
- {id: 27, title: "Bloom Energy Q2 2026 supplemental financial information, Exhibit 99.2 to Form 8-K", url: "https://www.sec.gov/Archives/edgar/data/0001664703/000162828026050150/ex992q226supplementalfin.htm", source: "SEC EDGAR", date: "2026-07-28"}
- {id: 28, title: "Hedge funds dumped chip stocks for a fourth straight week, Goldman Sachs says", url: "https://finance.yahoo.com/markets/stocks/articles/hedge-funds-dumped-chip-stocks-111514085.html", source: "Reuters via Yahoo Finance", date: "2026-07-06"}
- {id: 29, title: "Goldman Says Hedge Funds Sell US Tech Stocks at Record Pace", url: "https://www.bloomberg.com/news/articles/2026-07-20/goldman-says-hedge-funds-sell-us-tech-stocks-at-record-pace", source: Bloomberg, date: "2026-07-20"}
- {id: 30, title: "Asia stock-picking hedge funds set for record monthly loss, Goldman Sachs says", url: "https://finance.yahoo.com/markets/stocks/articles/asia-stock-picking-hedge-funds-082032839.html", source: "Reuters via Yahoo Finance", date: "2026-07-30"}
- {id: 31, title: "Surging Borrowing Costs Signal AI Debt Risks", url: "https://www.briefs.co/news/surging-borrowing-costs-signal-ai-debt-risks/", source: "Briefs.co", date: "2026-07-29"}
- {id: 32, title: "Credit Suisse bid to head off Archegos crisis ends as rival banks run for the exits", url: "https://www.scmp.com/business/banking-finance/article/3127597/credit-suisse-bid-head-archegos-crisis-ends-rival-banks", source: "South China Morning Post", date: "2021-03-29"}
- {id: 33, title: "Withdrawal of Proposed Regulatory Actions, including proposed Rule 10B-1", url: "https://www.federalregister.gov/documents/2025/06/17/2025-11110/withdrawal-of-proposed-regulatory-actions", source: "Federal Register", date: "2025-06-17"}
- {id: 34, title: "Anatomy of a Margin Call: How Situational Awareness LP Unwound a $20 Billion AI Book in One Trade", url: "https://spotgamma.com/situational-awareness-unwind-margin-call-ai/", source: SpotGamma, date: "2026-07-30"}
- {id: 35, title: "Billionaire Ken Griffin once called AI garbage. Now he says it will have a dramatic impact on society", url: "https://fortune.com/2026/05/18/billionaire-ken-griffin-ai-garbage-depressed-dramatic-impact-society/", source: Fortune, date: "2026-05-18"}
- {id: 36, title: "Situational Awareness: Racing to the Trillion-Dollar Cluster", url: "https://situational-awareness.ai/racing-to-the-trillion-dollar-cluster/", source: "Leopold Aschenbrenner", date: "2024-06"}
- {id: 37, title: "Queued Up: 2026 Edition, Characteristics of Power Plants Seeking Transmission Interconnection", url: "https://emp.lbl.gov/queues", source: "Lawrence Berkeley National Laboratory", date: "2026-06"}
- {id: 38, title: "PJM Capacity Auction Procures 138,318 MW of Generation Resources", url: "https://www.prnewswire.com/news-releases/pjm-capacity-auction-procures-138-318-mw-of-generation-resources-as-work-continues-to-address-growing-electricity-demand-302825613.html", source: "PJM Interconnection", date: "2026-07-14"}
- {id: 39, title: "Alphabet Q2 2026 earnings call transcript", url: "https://www.investing.com/news/transcripts/earnings-call-transcript-alphabet-beats-q2-2026-estimates-shares-fall-on-capex-surge-93CH-4807140", source: "Investing.com", date: "2026-07-22"}
- {id: 40, title: "Oracle Announces Record Q4 and FY 2026 Results Driven by Cloud Infrastructure", url: "https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Record-Q4-and-FY-2026-Results-Driven-by-Cloud-Infrastructure--Cloud-Applications/default.aspx", source: "Oracle Investor Relations", date: "2026-06-10"}
- {id: 41, title: "OpenAI Stargate: where the US sites stand", url: "https://epochai.substack.com/p/openai-stargate-where-the-us-sites", source: "Epoch AI", date: "2026-04-20"}
- {id: 42, title: "The United States generated a record amount of electricity in 2025", url: "https://www.eia.gov/todayinenergy/detail.php?id=67284", source: "US Energy Information Administration", date: "2026-03-05"}
- {id: 43, title: "Measuring AI Ability to Complete Long Tasks, time horizons data", url: "https://metr.org/time-horizons", source: METR, date: "2026-05-08"}
- {id: 44, title: "Time Horizon 1.1: an updated methodology", url: "https://metr.org/blog/2026-1-29-time-horizon-1-1/", source: METR, date: "2026-01-29"}
- {id: 45, title: "Frontier Risk Report, February to March 2026", url: "https://metr.org/blog/2026-05-19-frontier-risk-report/", source: METR, date: "2026-05-19"}
- {id: 46, title: "Q1 2026 timelines update", url: "https://blog.aifutures.org/p/q1-2026-timelines-update", source: "AI Futures Project", date: "2026-03"}
- {id: 47, title: "KBRA-rated NAV loan issuance and performance review", url: "https://www.kbra.com/publications/WzjcnGdM", source: KBRA, date: "2026-07-13"}
- {id: 48, title: "Side Letter: NAV's surprising stats", url: "https://www.privateequityinternational.com/side-letter-navs-surprising-stats/", source: "Private Equity International"}
- {id: 49, title: "ASC 820-10 model calibration, Deloitte Roadmap on Fair Value Measurements and Disclosures", url: "https://dart.deloitte.com/USDART/home/codification/broad-transactions/asc820-10/roadmap-fair-value-measurements-disclosures/chapter-9-initial-measurement/9-3-model-calibration", source: "Deloitte DART and FASB ASC"}
- {id: 50, title: "Anthropic raises Series H", url: "https://www.anthropic.com/news/series-h", source: Anthropic, date: "2026-05-28"}
- {id: 51, title: "Anthropic hits $1.2 trillion in the secondary market", url: "https://enterprisedna.co/resources/news/anthropic-1-2-trillion-secondary-market-openai-july-2026/", source: "Enterprise DNA, citing Caplight", date: "2026-07-13"}
- {id: 52, title: "Fundrise Innovation Fund LLC, Form N-CSR", url: "https://www.stocktitan.net/sec-filings/VCX/n-csr-fundrise-innovation-fund-llc-sec-filing-61cad3265338.html", source: "SEC filing via StockTitan", date: "2026-03-31"}
- {id: 53, title: "Destiny Tech100 (DXYZ) quote and history", url: "https://stockanalysis.com/stocks/dxyz/", source: "stockanalysis.com", date: "2026-07-30"}
- {id: 54, title: "Tiger Global Writes Down Venture Funds' Bets by 33% in 2022", url: "https://www.wsj.com/articles/tiger-global-writes-down-venture-funds-bets-by-33-in-2022-3f9f6ade", source: "The Wall Street Journal", date: "2023"}
- {id: 55, title: "Microsoft's $15 billion capex cut isn't a cut at all", url: "https://www.benzinga.com/markets/tech/26/07/60808802/microsofts-15-billion-capex-cut-isnt-a-cut-at-all", source: Benzinga, date: "2026-07-29"}
- {id: 56, title: "Anthropic raises $30 billion Series G at $380 billion post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation", source: Anthropic, date: "2026-02-12"}
- {id: 57, title: "Situational Awareness: From GPT-4 to AGI", url: "https://situational-awareness.ai/from-gpt-4-to-agi/", source: "Leopold Aschenbrenner", date: "2024-06"}
- {id: 58, title: "2024 United States Data Center Energy Usage Report, 2025 Update", url: "https://www.osti.gov/biblio/3374245", source: "Lawrence Berkeley National Laboratory", date: "2026-06-18"}
- {id: 59, title: "Meta Reports Second Quarter 2026 Results", url: "https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/default.aspx", source: "Meta Investor Relations", date: "2026-07-29"}
- {id: 60, title: "AI data centers database", url: "https://epoch.ai/data/ai-data-centers", source: "Epoch AI", date: "2026-07-30"}
- {id: 61, title: "Exclusive: Situational Awareness Down 67% in July in AI Stock Rout (headline located via news index; article body paywalled)", url: "https://news.google.com/rss/search?q=%22Situational+Awareness%22+%2267%25%22+July", source: "The Wall Street Journal", date: "2026-07-31"}
- {id: 62, title: "Prosecutors Charge Archegos' Bill Hwang With Market Manipulation, Fraud and Conspiracy in $160 Billion Trading Scheme", url: "https://www.institutionalinvestor.com/article/2bstogbmjmznvrmtl1j40/culture/prosecutors-charge-archegos-bill-hwang-with-market-manipulation-fraud-and-conspiracy-in-160-billion-trading-scheme", source: "Institutional Investor", date: "2022-04-27"}
- {id: 63, title: "12 CFR Part 220, Regulation T: Credit by Brokers and Dealers", url: "https://www.ecfr.gov/current/title-12/chapter-II/subchapter-A/part-220", source: "Electronic Code of Federal Regulations"}
- {id: 64, title: "US software stocks attempt rebound after AI-displacement selloff", url: "https://finance.yahoo.com/sectors/technology/articles/us-software-stocks-attempt-rebound-145947008.html", source: "Reuters via Yahoo Finance", date: "2026-05-19"}
:::
