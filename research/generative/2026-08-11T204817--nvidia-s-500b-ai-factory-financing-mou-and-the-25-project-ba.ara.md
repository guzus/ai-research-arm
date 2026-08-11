---
eyebrow: ARA RESEARCH · AI INFRASTRUCTURE CREDIT
domain: finance
title: Who actually holds the GPU residual
deck: NVIDIA put a number on the vendor's risk in its $500bn financing announcement — 25%. The number is not in the press release, not in a filing, and not attached to a defined denominator.
lede: |
  On 10 August 2026 NVIDIA said it had signed memorandums of understanding with
  Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs and KKR to build
  financing platforms designed to mobilise more than $500 billion of third-party
  capital for AI infrastructure. The press release runs to about 760 words of
  substantive body copy and does not contain the phrase "residual value" once. The 25% backstop that the
  entire market spent the following 48 hours pricing came from somewhere else
  entirely: a first-person essay the chief executive published himself the same
  day. That gap — between the reviewed corporate document and the founder's essay —
  is not a technicality. It is the most informative fact in the whole transaction,
  and it is where the answer to "who holds the residual" actually begins.
stats:
  - {label: Third-party capital target, value: $500B, note: MOU, not committed}
  - {label: Stated residual support, value: 25%, note: denominator undefined}
  - {label: NVIDIA disclosed guarantee book, value: $3.5B, note: as of 2026-04-26}
  - {label: SEC filings on the deal, value: 0, note: no 8-K as of 2026-08-12}
---

:::callout(kind=info, label="The short answer")
- **In law, nobody holds it yet.** The arrangements are MOUs "subject to execution of the final agreements," NVIDIA filed no Form 8-K, and the 25% figure appears in no SEC filing.[^1,2,62]
- **In time, sponsor equity holds it first.** A residual-value instrument cannot pay until a terminal date, after the asset is remarketed. Every operating-period default is absorbed by equity long before a guarantor writes a cheque.[^33]
- **In the terminal distribution, NVIDIA holds it first** — up to its cap — and the senior lender keeps everything above. That is why such instruments raise advance rates.[^33]
- **The instrument is aimed at the wrong asset.** GPU-equipment loans already fully amortise; the paper with real residual exposure is data-centre property ABS, and NVIDIA cannot guarantee concrete.[^18,23]
- **Ultimately it lands on insurance floats, pension money and semi-liquid credit funds** — which is not an inference. It is what BlackRock's chief executive said on television the day it was announced.[^12]
:::

## 01. The sentence that is not in the document

Three separate retrievals of NVIDIA's 10 August announcement — from the newsroom, from the investor-relations site, and through a raw-text proxy — return zero occurrences of "residual," zero of "backstop," and zero percentages other than the headline capital figure.[^1,3] The three hits for "guarantee" are all disclaimer boilerplate — NVIDIA's forward-looking-statement clause, and general performance disclaimers from BlackRock and KKR.[^1] The partner firms' own versions of the release carry the same NVIDIA-authored core and likewise advertise no credit support from the vendor, which is conspicuous: a binding NVIDIA backstop is precisely the thing an asset manager raising capital would want to advertise.[^4,5]

What the release does say is narrow and heavily qualified. "Memorandums of understanding signed with six of the world's premier financial institutions," aiming to establish platforms that will "mobilize over $500 billion of third-party capital for the buildout of AI infrastructure over time."[^1] And then the sentence that governs everything else: "These partnerships remain subject to execution of the final agreements."[^1] No borrowers, no rates, no tenors, no per-firm allocations, no schedule.

The 25% comes from a separate document — an essay Jensen Huang published under his own name the same day, in which he wrote that NVIDIA "may provide a residual-value support mechanism for up to 25% of an opportunity," assessed project-by-project, and characterised it as "limited, residual-value based and designed to complement — not replace — independent underwriting."[^2] He added that the exposure is "substantially lower than other compute-financing arrangements," naming no comparator.[^2]

:::timeline
- {date: 2026-06-10, headline: "KKR launches Helix Digital Infrastructure", body: "More than $10bn of long-duration commitments, with NVIDIA named among the founding investors."}
- {date: 2026-07-06, headline: "SemiAnalysis details the existing neocloud backstop", body: "A take-or-pay minimum revenue guarantee with NVIDIA sharing revenue above the floor; roughly six-year term."}
- {date: 2026-07-26, headline: "WSJ reports a $250bn OpenAI backstop in talks", body: "Lease and construction debt for a ~10GW Ohio campus, plus separate chip-purchase financing discussions."}
- {date: 2026-08-10, headline: "Six MOUs announced; Huang's essay adds the 25%", body: "Press release omits residual value entirely. NVDA closes down 2.86%; Apollo, Blackstone and KKR close up."}
- {date: 2026-08-12, headline: "Still no Form 8-K", body: "EDGAR shows NVIDIA's most recent 8-K predating the announcement; full-text search returns no post-2017 hit for residual value."}
- {date: 2026-08-26, headline: "Q2 FY2027 results and Form 10-Q", body: "The first filing in which an ASC 460 guarantee disclosure could appear. NVIDIA has historically filed the 10-Q the same day."}
:::

NVIDIA has filed no Form 8-K since 2 July 2026, well before the announcement.[^62] The most natural reading — and it is an inference, not a reported fact — is that this is a legal position rather than an oversight: Item 1.01 is triggered by a material *definitive* agreement, and the release's own language ("Memorandums of understanding," "subject to execution of the final agreements") describes something that generally is not one.[^1] The comparison set is suggestive rather than conclusive. An EDGAR full-text search for "residual-value" across 8-Ks filed in the first half of August 2026 returns 24 documents from roughly 21 filers; most are REITs and industrials with no lease-residual relevance, but the set does include a GM Financial auto-lease trust, Hertz, the aircraft lessor Sumisho Air Lease and the financial guarantor Assured Guaranty.[^63] NVIDIA is not among them. Firms that actually carry residual-value obligations tend to file about them.

So the disclosure asymmetry is total: the corporate document, reviewed by securities counsel, quantifies nothing; the number that moved the market was published in the chief executive's personal voice, on a channel with no review, and was never subjected to a follow-up question.

:::statement(attr="ARA Research")
A backstop that exists only in the founder's essay is a stated intention, not an obligation — and the first place it can become an obligation is the 10-Q on 26 August.
:::

## 02. Twenty-five per cent of what

"Up to 25% of an opportunity" has no defined denominator, and reputable outlets resolved the ambiguity in at least three incompatible directions from the same sentence — 25% of the loan, 25% of the transaction, 25% of GPU residual value.[^13,14] The differences are not cosmetic; they change the exposure by roughly a factor of two and change where the instrument sits in the loss waterfall.

Start with what an AI factory actually costs. Epoch AI's stylised one-gigawatt model puts servers at 55.9% of a $37.9bn project, network at 13.0%, facility at 30.2%, land at 0.5% and utility works at 0.4%.[^15] Huang's own figure is materially higher and differently scoped: he has said a gigawatt runs "between $50 billion and $60 billion," of which "$35 billion of that is for Nvidia chips and systems" — roughly 58–70% of project cost flowing to NVIDIA.[^16]

:::exhibit(num="Exhibit 1", title="Where a gigawatt of AI factory capex goes", subtitle="Share of $37.9bn stylised total project cost", source="Epoch AI, AI datacenter cost breakdown, 14 May 2026", note="Denominator is IT/critical load, not gross capacity. The authors describe it as a stylised model, not an estimate for any specific facility.")
:::donut(center-label="100%")
- {label: Servers, value: 55.9}
- {label: Facility, value: 30.2}
- {label: Network, value: 13.0}
- {label: "Land and utility works", value: 0.9}
:::
:::

That arithmetic eliminates the broadest reading. If "25% of an opportunity" meant 25% of total project cost, then — at NVIDIA content of 58–70% — the guarantee would equal 36–43% of the original cost of NVIDIA's own hardware.[^15,16] Against realistic terminal values that is not residual *support*; it is close to a full asset guarantee, and it is irreconcilable with Huang's own words "limited" and "substantially lower."[^2] There is also a control objection: roughly 30% of project cost is shell, land and electrical plant.[^15] NVIDIA does not own, remarket or clear the price of a substation. Its entire residual claim rests on CUDA-ecosystem redeployability of the compute.[^2]

:::compare
- {role: "25% OF PROJECT COST", name: "Per gigawatt", value: "$9.5B"}
- {role: "25% OF THE DEBT", name: "At 75% LTV", value: "$7.1B"}
- {role: "25% OF NVIDIA CONTENT", name: "Epoch base case", value: "$6.5B"}
:::

The narrower readings converge, because NVIDIA content and the debt quantum at 70–80% loan-to-value are arithmetically close: both land near $6–9bn per gigawatt, versus roughly $9.5bn under the broadest reading.[^15,17] On the balance of language — "residual-value based," a phrase equipment finance conventionally quotes against original equipment cost — the equipment-value reading is best supported.[^2] The loan reading rests entirely on one reporter's paraphrase, not a quote.[^13]

There is a second ambiguity nobody has resolved, and it matters more. "Up to 25%" is quantity language, not strike language. It admits a floor set at 25% of original cost (a deep out-of-the-money put, nearly free), a cap of 25% on NVIDIA's payment against a higher attachment point (genuinely first-loss and expensive), or a 25% quota share of the residual exposure. Those have opposite economics. ==No public source specifies which.==

## 03. What the residual is actually worth

Huang's underwriting case is that NVIDIA compute is fungible, universally adopted, software-upgradable and redeployable, which "helps protect residual value."[^2] The case deserves a fair hearing, because the observed data is genuinely mixed and the bear consensus is lazier than the evidence supports.

Start with the market's own prices. Our standing collection from the Vast.ai public offers API — normalised to dollars per GPU-hour by dividing total hourly price by GPU count — shows what a live marketplace paid across five NVIDIA generations on 11 August 2026.

:::exhibit(num="Exhibit 2", title="Median spot rental by GPU generation", subtitle="USD per GPU-hour, Vast.ai, 11 August 2026", source="ARA collection from console.vast.ai/api/v0/bundles, research/market/gpu-spot.json", note="Vast.ai is the low end of the market — decentralised, frequently consumer-hosted, no SLA. Absolute levels sit well below neocloud and hyperscaler pricing; the ratios are the transferable finding, not the levels.")
:::rank-list
- {label: "B300 (2025/26)", value: "$8.13", pct: 100}
- {label: "B200 (2025)", value: "$6.13", pct: 75}
- {label: "H200 (2024)", value: "$4.21", pct: 52}
- {label: "H100 SXM (2022/23)", value: "$2.27", pct: 28}
- {label: "A100 SXM4 (2020)", value: "$0.84", pct: 10, highlight: true}
:::
:::

The A100 is the test case, because it is the only NVIDIA data-centre part with six years of history. It still clears — six years after announcement it is transacting, not stranded — but at roughly 37% of an H100's hourly rate and about 10% of a B300's.[^41] At $0.84 an hour a part that carried a five-figure list price is not amortising anything close to its original cost inside a six-year life. Both halves of that sentence are true, and most commentary picks one.

The falsifying evidence for the bear case is real and recent: H100 one-year contract rentals bottomed around $1.70 in October 2025 and ran to roughly $2.35 by March 2026 — a 38% move off the bottom — and were reported near $2.65 in mid-2026.[^42,43] Two-year-old silicon repricing *upward* is exactly what Huang's fungibility argument predicts. The caveat is that it happened during an acute supply crunch, with Blackwell lead times stretched; it measures scarcity, not durable terminal value, and it unwinds when Rubin volume lands.[^42]

The falsifying evidence for the bull case is a filing. Amazon — the operator with the largest owned fleet and the best proprietary utilisation data — moved *against* the industry, shortening the useful life of a subset of servers and networking equipment from six years to five effective 1 January 2025, and said why: "The shorter useful lives are due to the increased pace of technology development, particularly in the area of artificial intelligence and machine learning."[^19] The disclosed cost was roughly $0.7bn of 2025 operating income.[^19] Microsoft, Alphabet and Meta had all gone the other way in 2022–25, and Meta's extension to 5.5 years alone deferred about $2.9bn of 2025 depreciation.[^20] There is no industry consensus on how long a GPU lives, which means there is no consensus input into any residual model.

:::callout(kind=warn, label="Wrong-way risk")
NVIDIA's obligation is largest exactly when NVIDIA is weakest. A residual shortfall arises when a generation is obsoleted or when aggregate AI investment slows — the same conditions under which NVIDIA's own revenue, margin and $43.4bn of ecosystem equity stakes all impair together.[^6] The guarantor is insuring against its own product cadence.
:::

That last point is not rhetorical. NVIDIA has compressed to an annual architecture cadence, and its own marketing claims large per-generation gains — Vera Rubin at roughly 5x performance per dollar over GB200 on vendor-selected configurations.[^44] Independent work is sharply more conservative and notes that Rubin's absolute cost per GPU-hour is *higher* than GB300's; it wins on tokens, not on rental price, which cuts against a simple "Rubin crushes Hopper residuals" thesis.[^44] But the structural point survives: the party writing the residual guarantee is also the party that decides, every twelve months, how obsolete the guaranteed asset becomes.

## 04. The instrument: where a residual guarantee sits in the waterfall

A residual-value instrument has a precise mechanical shape, and A.M. Best's criteria for rating residual-value insurers state it plainly: payment occurs only at a predefined terminal date — "usually on maturity or break of a lease of the physical asset, or when a balloon payment is due" — and equals "the excess, if any, of the RVI attachment point over market values."[^33] The indemnified party is the lender.

That fixes the position, and it dissolves the first-loss/last-loss argument as a false binary:

| Dimension | Where NVIDIA sits |
|---|---|
| *Timing* | **Last.** No payment until a terminal date, after remarketing. Sponsor equity absorbs every operating-period default, DSCR breach and interest shortfall first. |
| *Terminal-value distribution* | **First.** The writer absorbs the first dollars of decline below the attachment point, up to the cap; the lender keeps everything above. This is precisely why such instruments raise advance rates. |
| *Net* | **Mezzanine-equivalent** — junior to nothing, senior to sponsor equity, ahead of the senior lender's residual exposure. |

The complication is that at least four distinct NVIDIA instruments are being conflated in the coverage, and they have four different waterfall positions. Keeping them apart is the analytical work.

:::kv
- {term: "Facility lease guarantee", def: "Disclosed. $3.5bn maximum gross exposure, $712m partner escrow, 5-7 year terms, taken in exchange for warrants. On balance sheet as credit derivatives, fair value through Other income."}
- {term: "Neocloud revenue backstop", def: "A take-or-pay minimum revenue guarantee with NVIDIA sharing revenue above the floor. Roughly six-year term. Not an asset-value instrument."}
- {term: "Capacity offtake", def: "NVIDIA obligated to purchase CoreWeave's residual unsold capacity through 13 April 2032, initial value $6.3bn. Disclosed by CoreWeave, not by NVIDIA."}
- {term: "Residual-value support", def: "The new 25%. Asset-value floor. Undefined denominator, undisclosed attachment point, undisclosed trigger, no signed contract."}
:::

The first of these is the template worth watching, and it is more interesting than its size suggests. NVIDIA guarantees partners' facility lease obligations on default "in exchange for warrants," discloses maximum gross exposure of $3.5bn less $712m of partner escrow, and classifies the guarantees "as credit derivatives with changes in fair value recognized in Other income (expense), net," describing them as not material.[^7] That book is a *different instrument* — a credit guarantee of lease payments, not an asset-value floor — and it predates the August announcement by three and a half months, so it contains none of the new platform.[^6] But three things follow anyway. NVIDIA already has a stated policy of carrying guarantees at fair value through earnings, not off balance sheet. It has established that such guarantees have measurable non-zero value at inception — it charged warrants for them. And the $125bn the press has inferred from 25% of $500bn would be roughly 36 times that book; "not material" does not port.

The accounting is not the escape hatch the "off-balance-sheet" framing implies. A market-value guarantee over a nonfinancial asset owned by the guaranteed party is expressly within the scope of ASC 460, and ASC 460-10-50-4 requires disclosure of the maximum potential undiscounted future payment which "should not be reduced by any potential recoveries under collateralization or recourse provisions," even where payment is remote.[^24] Where a manufacturer instead agrees to reacquire the equipment at a guaranteed price, ASC 842-30-55 routes the transaction into ASC 606's repurchase rules — a *harsher* regime that can recharacterise the original sale as a lease or financing.[^25] The structure NVIDIA chooses therefore determines whether it books a liability, or defers revenue, or consolidates the vehicle entirely.

## 05. The market has already priced this risk — twice

The most useful evidence in this file is not an opinion. It is a set of prices, from the same borrower, on the same collateral class, five months apart.

CoreWeave's GPU-backed term loans have repriced three times in 2026. In March, an $8.5bn facility to a bankruptcy-remote subsidiary, backed by a contract Fitch identifies as being with Meta, cleared at SOFR+225 with a floating tranche and roughly 5.9% fixed — rated A3 by Moody's and A (low) by DBRS, and marketed as the first investment-grade-rated financing secured by this class of hardware.[^21,22] In May, a $3.1bn facility whose customers were not investment grade cleared at SOFR+450.[^22] On 10 August — the same day as the NVIDIA announcement — a $2.6bn facility priced at SOFR+550, wider than talk, on a structure whose roughly five-year maturity runs past the roughly three-year average customer contract.[^26]

:::exhibit(num="Exhibit 3", title="What lenders charge CoreWeave for GPU-backed debt", subtitle="Spread over SOFR, by facility, 2026", source="CoreWeave investor relations; Fitch Ratings; trade press", note="Not strictly like-for-like: collateral pools and customers differ across facilities. The direction and magnitude are the point.")
:::bars
- {label: "Mar 2026 · IG take-or-pay offtaker (A3/A-low)", value: "+225bp", pct: 41}
- {label: "May 2026 · two non-IG customers", value: "+450bp", pct: 82}
- {label: "Aug 2026 · 5yr tenor vs ~3yr contracts (Ba2/BB+)", value: "+550bp", pct: 100}
:::
:::

That 325 basis-point spread — from the March deal to the August deal — is the market's own price for exactly the risk NVIDIA proposes to absorb. It did not move because the chips changed. It moved because the offtaker's credit deteriorated and, in the last step, because the loan's maturity was pushed *beyond* the contracted revenue, handing lenders renewal and terminal-value risk for the first time.[^26]

Which brings us to the structural inversion at the centre of this transaction. As currently written, GPU equipment loans **amortise on a sculpted schedule**: Fitch's A-sf rating of the $8.5bn CoreWeave facility describes loans that "amortize over five years after the commitment period ends, 15 months from closing," sculpted to a 1.20x DSCR, with the borrower able to draw "for 90% of the incurred equipment cost."[^21] Fitch does not use the word "balloon" — reading the sculpted schedule as leaving none is an inference, not the agency's language. But where the debt substantially amortises inside the contract, residual value is a recovery buffer, not a repayment source — and a residual guarantee is close to redundant. Fitch says as much directly in a different deal: debt sized to fully amortise within the lease term "eliminates lease renewal risk."[^18]

Where residual value genuinely bites is data-centre *property* ABS, which carries **zero scheduled amortisation** to a five-to-ten-year anticipated repayment date against a thirty-year legal final.[^23] That is 100% of principal outstanding at the ARD, entirely dependent on refinancing or terminal value. And it is the one asset NVIDIA cannot guarantee.

:::position(confidence=medium, horizon="2026-Q4 to 2027-Q2")
stance: The 25% support is a financeability device that lets lenders extend tenor beyond contracted offtake, manufacturing a balloon it then fills — not credit protection on paper that needed it.
consensus: The market reads it as NVIDIA absorbing depreciation risk on GPUs, capping downside for lenders on an existing exposure.
resolves: Whether new NVIDIA-supported facilities print with maturities materially longer than their underlying customer contracts, and inside SOFR+250 rather than near SOFR+550.
:::

The rating agencies have not converged either. S&P has assigned no data-centre ABS tranche above single-A, citing refinancing, obsolescence and tenant concentration, while Moody's, Fitch and Morningstar DBRS have put AAA on comparable paper — a four-notch methodological disagreement on an asset class that grew from roughly $4bn of annual issuance in 2018–22 to $27bn in 2025.[^27,28] {sparkline:4,4,10,10,27,18}

## 06. The binding constraint is the tenant, not the terminal value

Here is the reframe that most of the commentary misses. In a contracted infrastructure financing, residual value is the *second* thing that fails. The first is the offtaker's ability to pay. Terminal value only becomes the binding question after a tenant defaults or declines to renew.

Fitch states this without ambiguity. Rating Applied Digital's ComputeCo senior secured notes — a 250MW, fifteen-year lease to CoreWeave — it assigned BB-/RR3 and wrote that "the project rating is capped by CoreWeave's credit quality."[^18] The asset did not set the rating. The tenant did.

And the tenant set is thin. Of the entities that would plausibly lease NVIDIA-backed AI factories, essentially none carries an investment-grade corporate rating: CoreWeave sits at Ba3/B+/BB-, Applied Digital at B+, and OpenAI, Anthropic, xAI, Lambda and Nebius are unrated.[^22] Every investment-grade rating in this ecosystem is *borrowed* — manufactured at an SPV through structural subordination, a take-or-pay contract with a rated counterparty, or a third-party wrap. CoreWeave's own A3-rated facility sits six notches above its parent.[^21,22]

The commitment-to-revenue arithmetic is the reason. OpenAI's leaked 2025 accounts show $13.07bn of revenue against a $20.92bn loss from operations — an operating loss at 160% of revenue — and CNBC reported — from people familiar, not from any announcement — that the company had told investors it was targeting roughly $600bn of total compute spend by 2030, against the $1.4 trillion of infrastructure commitments Altman had previously touted.[^30] Those two figures measure different things over different horizons, so the widely repeated "57% cut" is not a valid subtraction. Two things are nonetheless clear: the roughly $600bn target is about 46 times OpenAI's 2025 revenue, and the loss ratio is improving rather than deteriorating — 160% of revenue in 2025 against 237% in 2024.[^29,30] Anthropic is the fastest-improving credit in the set — a run-rate that went from about $9bn at end-2025 to $47bn by May 2026 — but every published Anthropic figure is a company-guided run-rate, and it has never disclosed an audited revenue, cash or loss figure of any kind.[^31]

The counter-evidence is genuine and should not be waved away. Contracted backlog is large and growing: CoreWeave reported $98.8bn of remaining performance obligations at 31 March 2026, up from $15.1bn at end-2024.[^32,52] Oracle carried $638bn at 31 May 2026 and Microsoft $678bn at 30 June 2026 — three different as-of dates in the steepest part of the backlog ramp, so they are a trend, not a snapshot.[^64,65] Take-or-pay structures with investment-grade counterparties are real. But roughly half of the committed cloud revenue at the major clouds is owed by two unrated, loss-making private companies — and Microsoft's commercial RPO grew 25% excluding OpenAI against 84% including it.[^65] Backlog is a claim on a counterparty, not cash.

## 07. The chain: from Santa Clara to a retirement account

The most direct answer to "who ultimately holds this" was given on television on the day of the announcement, by one of the six.

:::quote(attr="Larry Fink, Chairman and CEO, BlackRock, CNBC, 10 August 2026")
This is the very beginning, like what it was when I started in the mortgage-backed securities market in the 1970s.
:::

Asked what the platform means for people's retirement funds, Fink said BlackRock would be "working with pension funds across the world" and expected investors to "move away from a short-term money market return to a long-dated return."[^12] That is the risk-transfer channel stated by a principal, not inferred by a critic.

The rest of the chain is visible in filings. Apollo's balance-sheet arm, Athene, held $472.9bn of total assets at 30 June 2026, funded by retail annuity liabilities.[^34] US life insurers' private and illiquid bond holdings grew from $685bn, or 18% of the portfolio, at end-2024 to $807bn, or 20%, at end-2025 — with the top ten insurers holding 44% of that book while holding only 24% of industry fixed income.[^35] The Federal Reserve's May 2026 Financial Stability Report notes that leverage at the largest life insurers sat "well into the upper quartile" of its historical distribution, and that life insurers' move into risky and illiquid assets "has contributed to the expansion of private credit."[^36]

:::exhibit(num="Exhibit 4", title="Two-year moves in the channels that would hold this paper", subtitle="$ billion", source="Moody's via Insurance Business; KBRA; Morgan Stanley", note="Data-centre securitisation is 2025 full year against 2026 to early August, so the 2026 figure is a partial year and understates the run-rate.")
:::slope(left-label="Prior year", right-label="Latest", unit=$bn)
| Item | Prior | Latest |
|---|---|---|
| Life insurer private/illiquid bonds | 685 | 807 |
| Data-centre securitisation issuance | 27 | 18 |
| Non-listed BDC quarterly gross sales | 12 | 4.9 |
:::
:::

The Bank of England has put the AI-specific figures on the record: private credit's share of AI investment financing rose from 9% in 2024 to 34% in 2025, and AI issuers accounted for 41% of non-refinancing US high-yield issuance in 2026 year to date against 1% of the index at end-2025.[^37] The FPC's warning is about visibility rather than volume — the structures "can result in higher asset-level leverage and increase the complexity of identifying where risk ultimately sits," and "it may be difficult for financial firms to be aware of the full extent of their direct and indirect exposures."[^37]

The retail leg is already showing stress that predates this announcement. Non-listed BDC redemptions exceeded fundraising for the first time on record in the first quarter of 2026, with gross sales of $4.9bn against roughly $6.9bn of redemptions; the four largest perpetual non-traded BDCs all shrank in the first half of 2026 after peaking at year-end 2025.[^38] Roughly $6.5bn of public NAV BDC redemption requests went unmet in the quarter — soft gating by proration, while sponsors correctly note nobody formally gated.[^38]

One more link deserves naming, because it undercuts the word "independent." NVIDIA is a founding investor in KKR's Helix Digital Infrastructure — KKR's own co-chief executives say so in the 10 August release — and an investor and founding partner in Brookfield's AI Infrastructure Fund, which had $5bn of commitments toward a $10bn equity target.[^5,39] Two of the six firms described as bringing independent third-party capital are deploying vehicles the vendor co-owns.

## 08. What the precedents actually say

The reflex comparison is Lucent, and it is the wrong one — in a way that matters, because getting it wrong makes the risk look larger than it is on one axis and smaller on another.

Lucent's customer financing peaked at $8.1bn of commitments at 30 September 2000, and the structure was overwhelmingly *lending*: at September 2001, $4.6bn of the $5.3bn outstanding commitments were loans and only $0.7bn were third-party guarantees.[^40] It reserved $2.1bn against $3.0bn of drawn commitments — a 70% severity on principal it had actually advanced — and the SEC subsequently found $1.148bn of fiscal 2000 revenue improperly recognised.[^40] A residual backstop has no principal at risk. Its severity is bounded by the cap and offset by whatever the asset actually fetches. The instruments are not comparable, and analysts who reach for Lucent are importing a loss distribution that does not apply.

The closer analogue is the manufacturer residual-value guarantee, and its record is less dramatic than the AI-bubble framing implies. Embraer disclosed that "on average, our residual value guarantee exposure is limited to 17% of the original sale price," and reported maximum exposure net of provisions of $1.34bn at end-2010 — a figure that covers financial *and* residual-value guarantees together, and assumes every guaranteed customer defaults with no aircraft remarketed.[^45] Boeing ran the same structure through the worst downturn in aviation history and recognised $11m of trade-in and $15m of asset-related-guarantee expense in fiscal 2003, against carried liabilities of $70m on $1,747m of maximum potential payments.[^46] Caterpillar Financial disclosed in April 2009, at the bottom of that cycle, that ten years of gain or loss on lease terminations "has averaged about 1 percent of Cat Financial's profit before tax."[^47] Capped manufacturer residual programmes can be run for a decade without material loss. That is the honest base rate, and it favours NVIDIA.

Two details qualify it. First, in Embraer's book the one realised loss — a $103.0m charge recorded at 31 December 2009 on Mesa Air's insolvency — was a credit impairment on a *financial* guarantee, not a residual-value settlement.[^45] Even through the deepest aviation downturn on record, the pure residual leg did not visibly pay: the base rate is reassuring partly because these instruments are rarely tested at all. Second, Boeing's own table shows why the reserve ratio flatters. The $70m carried liability is 4.0% of maximum potential payments, but the same table discloses $1,578m of estimated proceeds from collateral and recourse — against net exposure of $169m, the reserve is roughly 41%.[^46] And Boeing made $746m of net cash payments on trade-in commitments in 2003 while booking $11m of expense, because it received aircraft worth roughly what it paid.[^46] ==A residual programme is cheap in the P&L and expensive in liquidity — and the liquidity leg arrives during the downturn.==

Two precedents cut the other way. The first is scale: benchmarked against manufacturers, 25% is *high*, not low. The second is AIG, which is the precise structural warning. AIG's guarantee book was called not through realised credit losses but through rating-triggered collateral mechanics — $40.1bn of collateral posted across 2007–08 — on assets the Maiden Lane vehicles ultimately liquidated for a combined $9.5bn gain.[^48] The guarantor died of the correlation, not of the ultimate loss.

Measured against its actual peer group, meanwhile, Huang's "substantially lower" claim survives — barely, and only because he chose the comparator class carefully.

:::exhibit(num="Exhibit 5", title="Vendor and sponsor retained share, by disclosed structure", subtitle="Support as a share of the relevant deal denominator, %", source="SEC filings: Meta FY2025 10-K, Broadcom Q2 FY2026 10-Q, Google/Fluidstack 8-K exhibits, Embraer FY2010 20-F; NVIDIA figures per Huang essay", note="Denominators are NOT commensurable: Meta's is RVG threshold over project cost, Broadcom's is max exposure over initial tranche, Google's is backstop over contracted revenue, NVIDIA's 25% is of an undefined opportunity. Read as rank order only.")
:::rank-list
- {label: "Meta / Blue Owl Hyperion RVG", value: "~104%", pct: 100}
- {label: "Google / Hut 8 lease backstop", value: "100%", pct: 96}
- {label: "Broadcom / XPV lease backstop", value: "~83%", pct: 80}
- {label: "Google / TeraWulf-Fluidstack", value: "~48%", pct: 46}
- {label: "Google / Cipher-Fluidstack", value: "~46%", pct: 44}
- {label: "NVIDIA compute platform (stated)", value: "≤25%", pct: 24, highlight: true}
- {label: "Embraer aircraft RVG (average cap)", value: "17%", pct: 16}
:::
:::

Meta guaranteed its Louisiana data-centre joint venture's residual value with "an aggregate threshold of approximately $28 billion that decreases over time" against roughly $27bn of estimated development costs, on four-year initial lease terms with renewal options to a total lease period of up to 20 years, from a 20% membership interest.[^49] Its aggregate unconsolidated-VIE maximum exposure to loss was $45.95bn — a figure that already *contains* the $28bn threshold, the $1.83bn equity carrying value, the lease commitments and the committed future fundings, so it is not a leverage ratio on the guarantee.[^49] Broadcom disclosed a backstop of an unnamed customer's lease obligations over five-year terms "with a maximum exposure of $29 billion"; the $35bn financing it sits inside, and the platform's name, come from Apollo's second-quarter earnings call rather than from Broadcom's filing.[^50,61] Against that cohort, 25% is genuinely modest. Against the industrial norm it is high. And against NVIDIA's own book it is inconsistent: NVIDIA's disclosed facility guarantee covers 100% of the lease obligation on default, and its CoreWeave arrangement obligates it to purchase 100% of residual unsold capacity through 2032.[^7,51]

## 09. The premium is booked. The put is not.

There is a second half to this trade that the coverage has almost entirely detached from the first. Morgan Stanley reportedly modelled the platform as a recurring revenue stream worth up to roughly $51bn a year at gross margins "approaching 100%," on the reasoning that NVIDIA owns no hardware and bears no depreciation — "resembling the annuity-type income of software subscriptions or cloud services."[^60] The arithmetic behind it is three undisclosed assumptions stacked: a 35% capture of GPU usage surplus, $13 per GPU-hour rental, and 5GW of new capacity added annually.[^60] None of the three is a disclosed fee on a disclosed base.

Set aside whether the number is right. The category is wrong. A fee for bearing residual risk is not a software subscription; it is an insurance premium, and it is the consideration for a written put. NVIDIA's own disclosed analogue makes the structure explicit: in the pre-existing neocloud programme, NVIDIA writes a take-or-pay minimum revenue guarantee and "shares in a portion of the Neocloud's revenue earned above the backstop level."[^17] The revenue share *is* the premium. They are one instrument, not two.

That matters because the two legs hit the financial statements at different times, in different places, with different recognition thresholds. The premium is revenue, recognised as earned. The guarantee is a contingent liability whose contingent component is recognised only when payment becomes probable — so the earnings benefit lands years before the obligation is measured. NVIDIA has already demonstrated it charges for guarantees: the disclosed facility-lease book was taken "in exchange for warrants," which is a priced instrument, not a courtesy.[^7]

:::callout(kind=warn, label="The asymmetry")
Booking a residual-risk premium at ~100% gross margin while leaving the written put unrecognised is not an accounting abuse — it is what the standards permit. It is also why an income statement that looks like a software company's can sit on top of an obligation that behaves like a monoline's.
:::

Morgan Stanley's own behaviour is the tell. It left its price target unchanged.[^60] A genuine $51bn annuity at near-100% margin would be roughly 24% of fiscal 2026 revenue in incremental gross profit; an analyst who believed it would not leave the target where it was.[^9,60] The number is a scenario, not a forecast.

The same time-asymmetry runs through the rest of NVIDIA's ecosystem exposure, and it is bigger than the guarantee book. In the quarter ended 26 April 2026, NVIDIA put $18.6bn of cash into private companies and infrastructure funds — 23% of that quarter's revenue — and disclosed that "some of these investments include AI model makers that may indirectly purchase or use our products in the cloud."[^6,8] Non-marketable securities went from $22.3bn to $43.4bn in a single quarter.[^6] The earnings effect is real, but it has to be split correctly, and most coverage does not: $2.6bn of unrealised gains came from those private holdings and a further $13.4bn from NVIDIA's publicly-listed stakes — $15.9bn pre-tax in total, against $69.9bn of pre-tax income.[^6] Roughly a quarter of pre-tax profit is therefore a mark on ecosystem equity rather than a chip sold, and it is precisely the mark that reverses in the scenario that calls a residual guarantee.

That is the wrong-way problem stated in the cleanest available form. It is not that NVIDIA cannot afford $125bn. It is that the collateral behind the guarantee, the equity stakes that flatter the earnings, the receivables concentrated 64% in three customers, and the guarantee itself all move together — and in the same direction.[^6]

## 10. What would break this thesis

The strongest counter-argument is that the exposure is contingent, capped, and currently theoretical — and that NVIDIA's balance sheet is large enough that the question is academic. That case is better than the bears allow.

NVIDIA generated roughly $125.6bn of operating cash flow in the trailing twelve months to 26 April 2026 and reported $259.5bn of total assets and $195.5bn of stockholders' equity.[^8,9] More importantly, the observable behaviour does not look like distressed vendor financing. Days sales outstanding *fell* to 45 days from 51 sequentially, so receivables are growing more slowly than revenue.[^8] And the single cleanest test of whether the existing backstops are being drawn: NVIDIA was a greater-than-10% CoreWeave customer in fiscal 2024 and fell *below* the threshold in fiscal 2025 — CoreWeave sold its capacity to third parties and the $6.3bn residual-capacity obligation was largely not called.[^51,52] A backstop that is never drawn costs nothing.

The circularity numbers in circulation are also weaker than their citation frequency suggests. The most-quoted figure — roughly 67% of revenue — is a *committed-capital-to-revenue ratio*, not a revenue attribution, and its numerator was dominated by the $100bn OpenAI letter of intent that was subsequently cut to a $30bn investment inside a $110bn round.[^53,54] Goldman Sachs, the only named estimator to publish the metric actually at issue, put circular deals at under 15% of projected 2027 revenue — and even that was built on the pre-cut $100bn.[^55] NVIDIA has also fully exited Applied Digital, WeRide and Arm, which is not how a company treats revenue conduits.[^52]

:::callout(kind=danger, label="What would actually falsify the sanguine case")
Three observable events, in order of decisiveness. **One:** a guarantee or commitment balance in the 26 August 10-Q materially above the current $3.5bn book, or an ASC 460 maximum-potential-payment disclosure with no stated cap.[^11] **Two:** execution of the reported $250bn OpenAI lease-and-construction backstop, which would be roughly 71 times the current guarantee book and would convert NVIDIA from equity investor to credit guarantor.[^56] **Three:** NVIDIA-supported paper printing near SOFR+550 rather than inside SOFR+250 — the market declining to credit the guarantee at all.[^17,26]
:::

Two further things would break the thesis in this piece specifically. If NVIDIA discloses on 26 August that the 25% is a deep out-of-the-money floor set at 25% of original equipment cost, the instrument is nearly free and this article has overweighted it. Conversely, if the support proves to attach at a high strike with NVIDIA absorbing the first 25 points of shortfall, the exposure is real, first-loss in the terminal distribution, and considerably larger than the disclosed guarantee book can absorb without an earnings line.

The credit market's read is harder to pin down than the coverage suggests. NVIDIA's five-year credit default swap was quoted near 77.5 basis points on 10 August, per a Bloomberg Markets Live note relayed second-hand by a market column — single-name CDS is licensed data with no free print, so ==neither the size of that day's move nor any subsequent level could be independently sourced, and both are excluded here==.[^57] Anyone quoting an intraday CDS move on this deal to half a basis point is repeating a number that has no public source.

The equity market was legible. NVDA closed down 2.86% at $217.55 on 10 August while Apollo, Blackstone and KKR all closed higher; the next session NVDA was unchanged at $217.50.[^58,59] When the equity of the party giving the guarantee falls and the equity of the parties receiving it rises, the market is telling you which direction value moved — and it is not the direction Huang's essay describes.

An adversarial pass against this article's three most load-bearing claims found no contradicting evidence for two of them — the absence of residual-value language from the press release and the absence of an 8-K, and the CoreWeave spread ladder including the August tenor mismatch. The third, that a fully amortising loan makes a residual guarantee close to redundant, drew only low-severity commentary disagreement, from writers addressing securitisations rather than the term loans described here. Two of three unbroken raises the shipping confidence of the argument; it does not raise the confidence of the 25% figure itself, which remains unfiled.

:::note
The 25% figure originates in a self-published essay, not a filing. Every exposure figure derived from it — including the widely quoted $125bn — is the press's arithmetic on an undefined denominator, not a disclosed cap. Treat all of it as provisional until 26 August 2026.
:::

:::references
- {id: 1, title: "NVIDIA Partners With Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs and KKR to Establish AI Compute Infrastructure Financing Platforms", url: "https://nvidianews.nvidia.com/news/nvidia-partners-with-apollo-blackrock-blackstone-brookfield-goldman-sachs-and-kkr-to-establish-ai-compute-infrastructure-financing-platforms-to-mobilize-over-500-billion-of-third-party-capital", source: "NVIDIA Newsroom", date: "2026-08-10"}
- {id: 2, title: "The NVIDIA AI Factory: Compute Is Becoming an Investable Asset Class", url: "https://www.linkedin.com/pulse/nvidia-ai-factory-compute-becoming-investable-asset-class-huang-4ju6c/", source: "Jensen Huang", date: "2026-08-10"}
- {id: 3, title: "NVIDIA Partners With Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs and KKR (investor relations copy)", url: "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Partners-With-Apollo-BlackRock-Blackstone-Brookfield-Goldman-Sachs-and-KKR-to-Establish-AI-Compute-Infrastructure-Financing-Platforms-to-Mobilize-Over-500-Billion-of-Third-Party-Capital/default.aspx", source: "NVIDIA Investor Relations", date: "2026-08-10"}
- {id: 4, title: "NVIDIA Partners with Apollo and others to Establish AI Compute Infrastructure Financing Platforms", url: "https://www.apollo.com/insights-news/pressreleases/2026/08/nvidia-partners-with-apollo", source: "Apollo Global Management", date: "2026-08-10"}
- {id: 5, title: "NVIDIA partners with Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs and KKR (partner copy)", url: "https://bam.brookfield.com/press-releases/nvidia-partners-apollo-blackrock-blackstone-brookfield-goldman-sachs-and-kkr", source: "Brookfield Asset Management", date: "2026-08-10"}
- {id: 6, title: "NVIDIA Form 10-Q, quarter ended 26 April 2026", url: "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000052/nvda-20260426.htm", source: "SEC EDGAR", date: "2026-05-20"}
- {id: 7, title: "NVIDIA Form 10-Q Note 8, Derivative Financial Instruments (Facility Lease Guarantee)", url: "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000052/R15.htm", source: "SEC EDGAR", date: "2026-05-20"}
- {id: 8, title: "NVIDIA CFO Commentary, Q1 fiscal 2027", url: "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000051/q1fy27cfocommentary.htm", source: "SEC EDGAR", date: "2026-05-20"}
- {id: 9, title: "NVIDIA Announces Financial Results for First Quarter Fiscal 2027", url: "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-first-quarter-fiscal-2027", source: "NVIDIA", date: "2026-05-20"}
- {id: 11, title: "NVIDIA Sets Conference Call for Second Quarter Financial Results", url: "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Sets-Conference-Call-for-Second-Quarter-Financial-Results/default.aspx", source: "NVIDIA Investor Relations", date: "2026-07-29"}
- {id: 12, title: "CNBC Exclusive: Becky Quick speaks with NVIDIA's Jensen Huang and Wall Street leaders on the $500B AI infrastructure push", url: "https://www.cnbc.com/2026/08/10/cnbc-exclusive-transcript-cnbcs-becky-quick-speaks-with-nvidias-jensen-huang-wall-street-leaders-on-500b-ai-infrastructure-push-on-closing-bell-overtime-today.html", source: "CNBC", date: "2026-08-10"}
- {id: 13, title: "Wall Street endorsed Jensen Huang's big concept for AI. What now?", url: "https://www.cnbc.com/2026/08/11/wall-street-endorsed-jensen-huangs-big-concept-for-ai-what-now.html", source: "CNBC", date: "2026-08-11"}
- {id: 14, title: "Nvidia's $500 Billion Bet To Make AI Compute Wall Street's Next Asset Class", url: "https://www.forbes.com/sites/robertszczerba/2026/08/10/nvidias-500b-bet-to-make-ai-compute-wall-streets-next-asset-class/", source: "Forbes", date: "2026-08-10"}
- {id: 15, title: "AI data center cost breakdown", url: "https://epoch.ai/data-insights/ai-datacenter-cost-breakdown", source: "Epoch AI", date: "2026-05-14"}
- {id: 16, title: "Nvidia's $100 billion OpenAI deal and the cost of a gigawatt", url: "https://www.cnbc.com/2025/09/22/nvidia-openai-data-center.html", source: "CNBC", date: "2025-09-22"}
- {id: 17, title: "Nvidia GPU Debt Backstop Unleashes Neocloud Financing", url: "https://newsletter.semianalysis.com/p/nvidia-gpu-debt-backstop-unleashes", source: "SemiAnalysis", date: "2026-07-06"}
- {id: 18, title: "Fitch Rates APLD ComputeCo LLC Senior Secured Notes 'BB-'/'RR3'", url: "https://www.fitchratings.com/research/infrastructure-project-finance/fitch-rates-apld-computeco-llc-subsidiary-of-applied-digital-senior-secured-notes-bb-rr3-05-12-2025", source: "Fitch Ratings", date: "2025-12-05"}
- {id: 19, title: "Amazon.com Form 10-K, fiscal year 2024", url: "https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm", source: "SEC EDGAR", date: "2025-02-06"}
- {id: 20, title: "Meta accounting move on AI servers cuts 2025 depreciation by about $2.9 billion", url: "https://finance.yahoo.com/news/meta-accounting-move-ai-servers-124059775.html", source: "Yahoo Finance", date: "2025-01-29"}
- {id: 21, title: "Fitch Rates CoreWeave Compute Acquisition Co. VIII Loans 'A-sf'; Outlook Stable", url: "https://www.fitchratings.com/research/structured-finance/fitch-rates-coreweave-compute-acquisition-co-viii-loans-a-sf-outlook-stable-01-04-2026", source: "Fitch Ratings", date: "2026-04-01"}
- {id: 22, title: "CoreWeave Closes Landmark $8.5 Billion Financing Facility, Achieving First Investment Grade Rated GPU-backed Financing", url: "https://investors.coreweave.com/news/news-details/2026/CoreWeave-Closes-Landmark-8-5-Billion-Financing-Facility-Achieving-First-Investment-Grade-Rated-GPU-backed-Financing/default.aspx", source: "CoreWeave Investor Relations", date: "2026-03-31"}
- {id: 23, title: "QTS Issuer ABS II presale report", url: "https://www.spglobal.com/ratings/en/regulatory/article/-/view/sourceId/101671383", source: "S&P Global Ratings", date: "2026-01-01"}
- {id: 24, title: "Financial statement presentation guide 23.6, Guarantees (ASC 460-10-50-4)", url: "https://viewpoint.pwc.com/dt/us/en/pwc/accounting_guides/financial_statement_/financial_statement___18_US/chapter_23_commitmen_US/236_guarantees_US.html", source: "PwC Viewpoint", date: "2026-08-12"}
- {id: 25, title: "Leases guide 8.5, Sales of equipment with guaranteed minimum resale value (ASC 842-30-55)", url: "https://viewpoint.pwc.com/content/pwc-madison/ditaroot/us/en/pwc/accounting_guides/leases/leases__4_US/chapter_8_other_topi_US/85_sales_of_equipmen_US.html", source: "PwC Viewpoint", date: "2026-08-12"}
- {id: 26, title: "CoreWeave prices $2.6 billion facility at a wider spread", url: "https://theenergymag.com/news/2026-08-11/coreweave-ai-2-6-billion-wider-spread", source: "The Energy Mag", date: "2026-08-11"}
- {id: 27, title: "S&P is right to keep triple-A away from data center ABS", url: "https://www.globalcapital.com/article/2gatl6p6gtk1i71gbe2o0/people-and-markets/gc-view/s-p-is-right-to-keep-triple-a-away-from-data-center-abs", source: "GlobalCapital", date: "2026-04-30"}
- {id: 28, title: "MBA NewsLink Roundtable: Data centers, demand and deal structures with KBRA", url: "https://newslink.mba.org/mba-newslinks/2026/march/mba-newslink-thursday-march-5-2026/mba-newslink-roundtable-discussing-data-centers-demand-and-deal-structures-with-kbra/", source: "KBRA via MBA NewsLink", date: "2026-03-04"}
- {id: 29, title: "Leaked financial docs show OpenAI is losing billions of dollars a year", url: "https://arstechnica.com/ai/2026/06/leaked-financial-docs-show-openai-is-losing-billions-of-dollars-a-year/", source: "Ars Technica", date: "2026-06-16"}
- {id: 30, title: "OpenAI resets spend expectations, targets around $600 billion by 2030", url: "https://www.cnbc.com/2026/02/20/openai-resets-spend-expectations-targets-around-600-billion-by-2030.html", source: "CNBC", date: "2026-02-20"}
- {id: 31, title: "Anthropic Series H", url: "https://www.anthropic.com/news/series-h", source: "Anthropic", date: "2026-05-28"}
- {id: 32, title: "CoreWeave Form 10-Q, quarter ended 31 March 2026", url: "https://www.sec.gov/Archives/edgar/data/1769628/000176962826000222/crwv-20260331.htm", source: "SEC EDGAR", date: "2026-05-08"}
- {id: 33, title: "Rating Residual Value Insurance criteria", url: "https://www3.ambest.com/ambv/ratingmethodology/OpenPDF.aspx?rc=234387", source: "A.M. Best", date: "2015-03-09"}
- {id: 34, title: "Apollo Global Management second quarter 2026 earnings release", url: "https://www.sec.gov/Archives/edgar/data/0001858681/000185868126000036/agmearningsrelease2q2026.htm", source: "SEC EDGAR", date: "2026-08-04"}
- {id: 35, title: "US life insurers' private credit push is creating liquidity and concentration risks, Moody's warns", url: "https://www.insurancebusinessmag.com/us/news/life-insurance/us-life-insurers-private-credit-push-is-creating-liquidity-and-concentration-risks-moodys-warns-578168.aspx", source: "Insurance Business", date: "2026-06-09"}
- {id: 36, title: "Financial Stability Report, May 2026: Leverage in the Financial Sector", url: "https://www.federalreserve.gov/publications/2026-may-financial-stability-report-leverage.htm", source: "Federal Reserve Board", date: "2026-05-08"}
- {id: 37, title: "Financial Stability Report, July 2026", url: "https://www.bankofengland.co.uk/-/media/boe/files/financial-stability-report/2026/financial-stability-report-july-2026.pdf", source: "Bank of England", date: "2026-07-07"}
- {id: 38, title: "Quarterly redemptions exceed fundraising for the first time in the non-listed BDC market", url: "https://www.rastanger.com/news/quarterly-redemptions-exceed-fundraising-for-the-first-time-in-non-listed-bdc-market", source: "Robert A. Stanger & Co.", date: "2026-05-14"}
- {id: 39, title: "Brookfield Launches $100 Billion AI Infrastructure Program", url: "https://www.globenewswire.com/news-release/2025/11/19/3190798/0/en/Brookfield-Launches-100-Billion-AI-Infrastructure-Program.html", source: "Brookfield", date: "2025-11-19"}
- {id: 40, title: "Lucent Technologies Form 10-K, fiscal year 2002, Exhibit 13", url: "https://www.sec.gov/Archives/edgar/data/0001006240/000095011702003045/ex13.htm", source: "SEC EDGAR", date: "2002-12-11"}
- {id: 41, title: "GPU spot rental price series", url: "https://console.vast.ai/api/v0/bundles/", source: "Vast.ai, collected by ARA (research/market/gpu-spot.json)", date: "2026-08-11"}
- {id: 42, title: "SemiAnalysis GPU Cloud Rental Price Index", url: "https://gpu-index.semianalysis.com/", source: "SemiAnalysis", date: "2026-06-12"}
- {id: 43, title: "H100 rental price over time", url: "https://www.silicondata.com/blog/h100-rental-price-over-time", source: "Silicon Data", date: "2025-12-10"}
- {id: 44, title: "Vera Rubin NVL72 vs GB200 NVL72 inference TCO", url: "https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference", source: "SemiAnalysis", date: "2026-07-23"}
- {id: 45, title: "Embraer Form 20-F, fiscal year 2010", url: "https://www.sec.gov/Archives/edgar/data/1355444/000119312511101384/d20f.htm", source: "SEC EDGAR", date: "2011-04-19"}
- {id: 46, title: "The Boeing Company Form 10-K, fiscal year 2003", url: "https://www.sec.gov/Archives/edgar/data/12927/000119312504034751/d10k.htm", source: "SEC EDGAR", date: "2004-03-05"}
- {id: 47, title: "Caterpillar Form 8-K, first quarter 2009 results", url: "https://www.sec.gov/Archives/edgar/data/0000018230/000001823009000153/form8k_1q09results.pdf", source: "SEC EDGAR", date: "2009-04-21"}
- {id: 48, title: "AIG in Hindsight (NBER Working Paper 21108)", url: "https://www.nber.org/system/files/working_papers/w21108/w21108.pdf", source: "McDonald & Paulson, NBER", date: "2015-04-01"}
- {id: 49, title: "Meta Platforms Form 10-K, fiscal year 2025, Note 5 (non-marketable equity investments)", url: "https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/R14.htm", source: "SEC EDGAR", date: "2026-01-29"}
- {id: 50, title: "Broadcom Form 10-Q, quarter ended 3 May 2026, Note 11 (subsequent events)", url: "https://www.sec.gov/Archives/edgar/data/1730168/000173016826000054/avgo-20260503.htm", source: "SEC EDGAR", date: "2026-06-09"}
- {id: 51, title: "CoreWeave Form 8-K, NVIDIA order form and residual unsold capacity", url: "https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm", source: "SEC EDGAR", date: "2025-09-15"}
- {id: 52, title: "CoreWeave Form 10-K, fiscal year 2025", url: "https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm", source: "SEC EDGAR", date: "2026-03-02"}
- {id: 53, title: "OpenAI and NVIDIA announce strategic partnership (letter of intent)", url: "https://openai.com/index/openai-nvidia-systems-partnership/", source: "OpenAI", date: "2025-09-22"}
- {id: 54, title: "OpenAI's $110 billion funding round draws investment from Amazon, Nvidia and SoftBank", url: "https://www.reuters.com/business/retail-consumer/openais-110-billion-funding-round-draws-investment-amazon-nvidia-softbank-2026-02-27/", source: "Reuters", date: "2026-02-27"}
- {id: 55, title: "Nvidia now an AI hedge fund? Goldman warns on circular revenue risk", url: "https://www.benzinga.com/analyst-stock-ratings/analyst-color/25/10/48048036/nvidia-now-an-ai-hedge-fund-goldman-warns-circular-revenue-risk", source: "Benzinga (Goldman Sachs research)", date: "2025-10-06"}
- {id: 56, title: "Nvidia and OpenAI in talks for up to $250 billion AI backstop", url: "https://www.cnbc.com/2026/07/27/nvidia-and-openai-in-talks-for-up-to-250-billion-dollar-ai-backstop.html", source: "CNBC", date: "2026-07-27"}
- {id: 57, title: "Nvidia's $500 billion AI push is starting to show up in credit", url: "https://www.investing.com/analysis/nvidias-500-billion-ai-push-is-starting-to-show-up-in-credit-200685569", source: "Investing.com", date: "2026-08-11"}
- {id: 58, title: "NVIDIA Corporation stock price history", url: "https://stockanalysis.com/stocks/nvda/history/", source: "StockAnalysis", date: "2026-08-11"}
- {id: 59, title: "Apollo Global Management stock price history", url: "https://stockanalysis.com/stocks/apo/history/", source: "StockAnalysis", date: "2026-08-11"}
- {id: 60, title: "Nvidia Launches $500 Billion AI Financing Platform; Morgan Stanley Sees New Revenue Stream With Near-100% Gross Margin", url: "https://finance.biggo.com/news/e4d766cd-2797-4eb4-8203-4bbded281df3", source: "BigGo Finance (Morgan Stanley research)", date: "2026-08-11"}
- {id: 61, title: "Apollo Global Management second quarter 2026 earnings call transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/08/11/apollo-apo-q2-2026-earnings-call-transcript/", source: "The Motley Fool", date: "2026-08-04"}
- {id: 62, title: "NVIDIA Corporation Form 8-K filing index", url: "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001045810&type=8-K", source: "SEC EDGAR", date: "2026-08-12"}
- {id: 63, title: "EDGAR full-text search: \"residual-value\" in Form 8-K, 1-15 August 2026", url: "https://efts.sec.gov/LATEST/search-index?q=%22residual-value%22&forms=8-K&startdt=2026-08-01&enddt=2026-08-15", source: "SEC EDGAR full-text search", date: "2026-08-12"}
- {id: 64, title: "Oracle remaining performance obligations (XBRL company concept)", url: "https://data.sec.gov/api/xbrl/companyconcept/CIK0001341439/us-gaap/RevenueRemainingPerformanceObligation.json", source: "SEC EDGAR XBRL", date: "2026-05-31"}
- {id: 65, title: "Microsoft FY26 Q4 earnings press release and prepared remarks", url: "https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast", source: "Microsoft Investor Relations", date: "2026-07-29"}
:::
