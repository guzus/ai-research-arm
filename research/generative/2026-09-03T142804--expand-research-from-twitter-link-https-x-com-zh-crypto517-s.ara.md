---
eyebrow: MARKETS · NVIDIA
title: The Earnings Paradox — Why NVIDIA Kept Falling After Beating, Until August Broke the Pattern
deck: Four straight beat-and-raise quarters, NVIDIA's stock fell the next day. Then in August 2026 it beat again and rallied 8.7%. The difference reveals more about how AI-era mega-cap earnings actually get priced than the "sell the news" cliché does.
lede: |
  Between August 2025 and May 2026, NVIDIA topped Wall Street's revenue and profit estimates in four consecutive quarters — and its stock fell the trading day after each report. Then on August 27, 2026, after another beat-and-raise print, shares closed up 8.74%, the company's best single day since April 2025. Untangling why the pattern held for a year and then broke apart requires separating at least five distinct stories that get collapsed into one headline: behavioral anchoring near all-time highs, options-market calibration, sector-wide AI-trade sentiment, a live Wall Street argument over circular financing, and a genuinely quiet regulatory shock that moved the stock less than an ordinary earnings day did.
stats:
  - {label: "Q2 FY27 revenue", value: "$96.2B", note: "+106% YoY"}
  - {label: "Data Center revenue", value: "$89.0B", note: "+117% YoY"}
  - {label: "Aug 27 2026 stock move", value: "+8.74%", note: "biggest gain since Apr 2025"}
  - {label: "Market cap", value: "~$5.5T", note: "as of Sep 3, 2026"}
domain: finance
---

:::note
This piece traces a research question a Chinese-language markets commentator (@Zh_Crypto517 / Z大诗, whose public posting record covers prediction markets, HK/US equities, and AI-linked names) has repeatedly engaged with — the seed post itself could not be retrieved in this run due to an X/Twitter access failure, so this article instead independently investigates the underlying, well-documented pattern using primary sources: SEC filings, earnings-call transcripts, and market data.
:::

:::callout(kind=info, label="In short")
- NVIDIA beat consensus on revenue and EPS in five straight quarters (Aug 2025 – Aug 2026), but the stock fell the day after four of the first five reports.
- The pattern broke on August 27, 2026: NVDA rallied 8.74% after Q2 FY2027 results, its best day since April 2025 — before giving back some of the gain the next session on ordinary profit-taking.
- Two mechanisms explain most of the four declines better than "sell the news": anchoring near all-time highs (guidance, not the beat, moves the stock) and an options market that had already priced in large, uncertain moves.
- At least one of the four declines (February 2026) shows clear sector-wide, not NVIDIA-specific, fingerprints — the Nasdaq and semiconductor sector fell the same day, and analysts raised price targets anyway.
- The more durable risk isn't the quarterly reaction pattern — it's the circular-financing debate around NVIDIA's $500B financing platform and $105B OpenAI guarantee, and the customer concentration visible in NVIDIA's own SEC filings.
:::

## 01. The Pattern That Broke

For four consecutive quarters, NVIDIA delivered results that beat Wall Street's estimates — and for four consecutive quarters, its stock fell the next day[^43]. That streak ended on August 27, 2026, when the company beat and raised guidance again and shares rallied 8.74%, the largest one-day gain since April 2025. The reversal was partially unwound the following session on what press coverage attributed to ordinary profit-taking, not new negative information.

:::timeline
- {date: "2025-08-28", headline: "Q2 FY2026 beat, stock dips", body: "NVDA closed at $179.93 the day after results, essentially flat to down."}
- {date: "2025-11-20", headline: "Q3 FY2026 beat, stock falls", body: "NVDA closed at $180.41, down sharply intraday despite topping estimates."}
- {date: "2026-02-26", headline: "Q4 FY2026 beat-and-raise, stock drops 5.5%", body: "NVDA closed at $184.66, erasing roughly $260B in market value."}
- {date: "2026-05-21", headline: "Q1 FY2027 beat, stock slips again", body: "NVDA closed at $219.25, a 'sell the news' reaction to a fourth straight post-earnings decline."}
- {date: "2026-08-27", headline: "Q2 FY2027 beat-and-raise, stock rallies 8.7%", body: "NVDA closed at $227.98, its biggest one-day gain since April 2025, breaking the streak."}
:::

:::line-chart(title="NVDA close, day after each earnings report", subtitle="Stock price on the first full trading session following results", y-unit=$)
x: 2025-08,2025-11,2026-02,2026-05,2026-08
NVDA: 179.93,180.41,184.66,219.25,227.98
:::

Each leg of the four-quarter decline followed the same script: NVIDIA topped consensus, and the stock sold off anyway. The August 2025 report produced only a marginal dip to $179.93[^10]. By November, the reaction had sharpened — a beat met a fall to $180.41, with intraday declines reported as high as 3.2% to 7.8%[^11]. February 2026 was the sharpest of the four: a beat-and-raise quarter still knocked the stock down roughly 5.5% to $184.66, wiping out an estimated $260 billion in market value in a single session[^12]. By May 2026, the pattern was recognized widely enough that CNBC titled a piece "Here we go again with Nvidia falling on earnings," describing the ~1.2-1.8% slide to $219.25 as a "buy the rumor, sell the news" reaction consistent with the prior three quarters[^13][^44]. The day before the August 2026 report, 24/7 Wall St noted explicitly that NVIDIA "has beaten Wall Street's earnings estimates five quarters in a row, yet the stock has dropped after four of those announcements," with declines reaching roughly 6%, and floated the possibility that the pattern would repeat a fifth time[^43].

It did not. On August 26, 2026, NVIDIA reported Q2 FY2027 revenue of $96.221 billion, up 106% year over year and above the roughly $92.17 billion consensus estimate, alongside Q3 guidance of $108.0 billion that cleared expectations near $104.2 billion[^7]. The next session, August 27, NVDA closed at $227.98, up 8.74% on volume of approximately 293.3 million shares — roughly 106% above the three-month average — adding an estimated $441.5 billion in market value in a single day[^6][^8].

That same day, August 27, the Wall Street Journal reported that NVIDIA had paused parts of a roughly $36 billion AI-cloud revenue-sharing financing arrangement[^9]. The timing matters for what it rules out: the report broke on the same session as the rally, a full trading day before NVDA's next decline. On August 28, the stock fell 4.57% to $217.55, erasing about $180 billion — roughly 41% of the prior day's gain[^8]. Because the WSJ story was already public before that decline, and because the magnitude and framing of the pullback tracked ordinary digestion of an outsized one-day move rather than any incremental disclosure on August 28 itself, the sequence does not support a clean causal line from the financing story to the next day's drop. It may still be relevant to the broader financing question taken up later in this piece, but it does not explain the profit-taking.

What makes this worth dissecting is not the reversal alone but what it interrupts: a four-quarter run in which beating estimates was, empirically, a poor predictor of the next day's stock move. A pattern that consistent, breaking on a quarter that was not obviously stronger on every metric than the ones that preceded it, raises the question the rest of this article investigates — whether the mechanism was something specific to how this print was read, or a signal that the market's relationship to NVIDIA's results has changed.

## 02. Inside the Beat

NVIDIA (Nasdaq: NVDA), founded in 1993 and headquartered in Santa Clara, has spent the past decade migrating from a graphics-chip company toward a data-center company[^42]. Its fiscal Q2 didn't clear consensus at the margin — it cleared it by a distance that made "beat" feel like an understatement, and the guide for Q3 pushed the bar higher still. But buried inside the same guidance is the one figure moving the wrong way.

:::kv
- {term: "Founded", def: "April 5, 1993 (Huang, Malachowsky, Priem)"}
- {term: "HQ", def: "Santa Clara, California"}
- {term: "Ticker", def: "Nasdaq: NVDA"}
- {term: "Fiscal calendar", def: "FY ends last Sunday of January; runs ~1 year ahead of the ending month"}
:::

:::stats
- {label: "Revenue (Q2 FY27)", value: "$96.2B", note: "+106% YoY"}
- {label: "Data Center revenue", value: "$89.0B", note: "+117% YoY, 92% of total"}
- {label: "GAAP diluted EPS", value: "$2.46", note: "+128% YoY"}
- {label: "Q3 FY27 guidance", value: "$108.0B", note: "vs. ~$104.2B expected"}
:::

:::compare
- {role: "STREET CONSENSUS", name: "Pre-print estimate", value: "$92.2B"}
- {role: "ACTUAL", name: "Q2 FY2027 revenue", value: "$96.2B"}
- {role: "SUBJECT", name: "Q3 FY2027 guide", value: "$108.0B"}
:::

Start with the magnitude. For the quarter ended July 26, 2026, NVIDIA reported total revenue of $96.221 billion, up 106% year-over-year and 18% sequentially, against a Street consensus of roughly $92.17 billion — a beat of just over $4 billion, or about 4.4%, on a base that had already grown fourfold in two years[^1]. Profitability scaled ahead of revenue: GAAP diluted EPS came in at $2.46, up 128% YoY, and non-GAAP diluted EPS at $2.22, up 120% YoY, versus a roughly $2.10 non-GAAP consensus[^1]. When both the top line and the bottom line beat by a wider margin than the top line's own growth rate, that is not a company squeaking past a lowered bar — it is a company whose actual demand curve is still outrunning what a room full of sell-side analysts, watching the same order book commentary, priced in three months earlier.

The composition of that revenue is where the beat starts to carry risk alongside reward. Data Center segment revenue was $89.0 billion, up 117% YoY and 18% QoQ — essentially in lockstep with the total-company growth rate, which means Data Center is now approximately 92% of total revenue[^2]. A company that was diversified across gaming, professional visualization, automotive and data center five years ago has, in the span of two AI capex cycles, become a data-center company with some other business lines attached. That concentration is not inherently bearish — it is the direct mechanical consequence of hyperscaler and neocloud capex being the single largest source of incremental demand in the semiconductor industry — but it does mean the stock's entire investment case now rides on the capital-spending decisions of a small number of customers, a dependency this article returns to directly in Section 06.

Then there is the guide, and the guide is where the discipline of reading past the headline actually pays off. NVIDIA guided Q3 FY2027 revenue to $108.0 billion, plus or minus 2%, versus a roughly $104.2 billion Street expectation — another beat-the-estimate print before a single unit has shipped, and notably given without assuming any Data Center compute revenue from China in the outlook[^3]. That last clause matters on its own (Section 07 deals with it), but it is easy to let the headline number's audacity obscure the line sitting directly next to it in the same CFO commentary: gross margin, GAAP and non-GAAP, is guided to 74.0% ± 50 basis points for Q3 — a full 100 basis points below the 75.0% NVIDIA actually delivered in Q2[^1][^3].

A 100bp sequential step-down in gross margin, disclosed in the same document as a revenue guide that beat consensus by nearly $4 billion, is not a rounding error — margin moves of that size on a base this large translate into real absolute dollars, and they are the kind of detail a headline-driven read of "another blowout quarter" will skip past entirely. It does not, by itself, invalidate the beat. But it is the first hard data point in this filing that points down rather than up, and a serious read of the print has to hold both facts at once: demand strong enough to beat guidance twice in the same sentence, and a cost or mix structure strong enough to start eating into the margin that demand is supposed to be buying. Section 06 returns to the filing to ask what, specifically, is driving that compression.

## 03. Two Mechanisms: Anchoring and the Options Market's Own Yardstick

Two mechanisms, not one, explain "NVIDIA beat and the stock still fell" better than the reflexive "sell the news." The first is behavioral: near an all-time high, a beat has to clear an ever-rising bar before investors will mark the stock up further, which pushes guidance rather than the headline number into the driver's seat. The second is mechanical: the options market has, most quarters, priced a move wide enough to contain what actually happened — so the surprise was usually about direction, not magnitude.

Start with anchoring. Kalsbach and Windmüller's "expectations treadmill" framework argues that when a stock is trading near its 52-week high, investors are structurally reluctant to revise their valuation upward even on genuinely positive news[^45]. The intuition is not exotic: if the price already embeds an optimistic scenario, a result that merely confirms the optimistic scenario changes nothing — it has to *exceed* an expectation that has already priced in excellence. Commentary building on this mechanism treats it as a leading explanation for why mega-cap tech names, and NVIDIA in particular, sell off on beats that would have been treated as unambiguously bullish two or three quarters earlier[^45].

Apply this to NVIDIA's 2025-2026 run. Across nearly every print in that window, the company was trading within single-digit percentage points of its all-time high going into earnings[^23], having already absorbed a story — AI infrastructure buildout, data-center demand, Blackwell ramp — that the market had priced aggressively in advance. Under an anchoring lens, that positioning is precisely what should make the *headline beat* nearly irrelevant to the stock's reaction: a beat in line with elevated expectations is a rounding error against a bar set by the prior quarter's beat. What moves the stock in that regime is guidance, and specifically whether guidance re-underwrites the multi-quarter growth narrative or merely confirms it. A "meets, doesn't exceed" guide, delivered against a backdrop of record actual results, is the textbook setup for a "great quarter, stock down" headline — not because the quarter was bad, but because the bar was already at the level the quarter cleared.

The second mechanism is where options pricing does real diagnostic work, because it lets us separate "the market was wrong about how big the move would be" from "the market correctly sized the move, and it just went down instead of up." The following table lines up implied and realized moves across NVIDIA's two most recent prints and the trailing 12-quarter baseline:

:::slope(left-label="Options-implied move", right-label="Realized move", unit=%)
| Quarter | Options-implied move | Realized move |
|---|---|---|
| May 2026 (Q1 FY27) | 7 | 1.8 |
| Aug 2026 (Q2 FY27) | 5.6 | 8.74 |
| 12-quarter trailing average | 7.7 | 7.6 |
:::

Ahead of the May 2026 print, options priced an implied move of roughly 6.5-8%[^20]. The stock actually fell about 1.8% the next day[^20][^21] — well inside the priced range, on the low side of it. That is not a surprised market; that is a market that correctly flagged elevated uncertainty and then watched the outcome land in the calm middle of its own distribution. The press coverage of that move as "buy the rumor, sell the news" despite record revenue[^21] describes investor psychology accurately but says nothing about whether the options market mispriced risk — it did not.

Zoom out further and the calibration argument gets stronger, not weaker, on average. Per ORATS analytics, NVIDIA's trailing 12-quarter average implied move (7.7%) and average realized move (7.6%) are almost identical[^22]. That is a well-calibrated options market on average, not a systematically complacent or systematically panicked one. Against that baseline, going into the August 26, 2026 print specifically, implied volatility priced a move of only about 5.4-5.9% — the lowest in two years and noticeably below the 7.6-7.7% trailing realized average[^19]. As the table above shows, that gap did not hold: the realized move (+8.74%) blew through the top of the priced range, meaning August was the one quarter in this window where the options market was NOT well calibrated — it under-priced uncertainty, and the direction happened to be up rather than down. Section 09 returns to this asymmetry directly.

None of this reads as a stock priced for perfection about to break under its own valuation. NVIDIA's forward P/E sat near 18.6x as of September 3, 2026, with a PEG around 0.38 — among the cheapest growth-adjusted multiples in the Magnificent Seven[^33]. More tellingly, the forward multiple actually *compressed* through mid-2026, falling to roughly 23.2x by mid-July even as the share price rose, because consensus earnings estimates were rising faster than the stock[^34]. A classic "priced for perfection" unwind requires the multiple to be stretched and then reset; here the multiple was already resetting downward while the stock climbed. That pattern is far more consistent with anchoring-driven guidance sensitivity than with a valuation bubble popping — which is exactly why the question the rest of this piece has to answer is not "was NVIDIA overvalued," but "was the August 2026 reaction more of the same, or something the two mechanisms above can't fully explain."

## 04. The Confound: NVIDIA Problem or Market Problem?

The single worst post-earnings session in this sequence — February 26, 2026, when NVDA closed at $184.66, down 5.46% the day after a beat-and-raise Q4 FY2026 report — did not happen in isolation[^12]. The Nasdaq Composite fell that same day, the semiconductor sector fell by almost exactly as much as NVDA itself, and sell-side desks raised their price targets on the stock even as it dropped. That combination is hard to square with a story about NVIDIA-specific disappointment; it looks much more like a sector-wide repricing of the AI trade that used NVIDIA's print as the trigger rather than the cause.

:::bars
- {label: "NVDA", value: "-5.46%", pct: 55}
- {label: "Semiconductor sector (SOX-adjacent)", value: "-5%", pct: 50}
- {label: "Nasdaq Composite", value: "-1.18%", pct: 12}
- {label: "Dow Jones Industrial Average", value: "+0.03%", pct: 1}
:::

Start with the breadth of the move. The Nasdaq Composite fell roughly 1.18% on February 26, with an intraday drawdown as steep as 1.91%, while the Dow Jones Industrial Average was essentially flat, up 0.03%[^16]. That split matters: a genuinely macro-driven selloff — a rate shock, a growth scare, a risk-off day across asset classes — should hit the Dow and the Nasdaq together. Instead, the damage was concentrated almost entirely in technology and semiconductors, which is the signature of a sector-specific sentiment wobble, not a market-wide one. The bond market corroborates this reading rather than complicating it: the 10-Year Treasury yield fell to 4.01% that session, its lowest level since November 28[^16]. Falling yields are the opposite of what a "rates repriced against tech multiples" narrative would predict — if anything, lower yields should have been a tailwind for long-duration growth names like NVDA, not a headwind. Whatever pushed the stock down, it was not a bond-market shock.

The semiconductor sector's move on February 26 was, if anything, more severe than NVIDIA's own. The broader semiconductor and equipment complex fell by roughly 5% that session, dragging the Philadelphia Semiconductor Index down in lockstep with NVDA, and coverage of the day named Broadcom, Micron, and AMD among the peers falling alongside it[^17]. A stock-specific disappointment does not typically take an entire peer group — companies with different customers, different product cycles, and in some cases different end markets — down by nearly the same percentage on the same day. A sector-wide repricing of AI-capex exposure does exactly that. And the sector's nerves did not start on February 26: SOXX, the semiconductor ETF, had already fallen 2% the day before the print, on February 25, underperforming the Nasdaq-100's 1.1% decline that same day[^15]. That is jitters accumulating *ahead of* NVIDIA's own numbers, not a reaction produced by them — evidence that whatever was unsettling the group predated any information content in the Q4 FY2026 report.

The analyst reaction is the hardest piece of evidence to reconcile with a "the market didn't like NVIDIA's results" story. Citi, Bernstein, Baird, Bank of America, and Rosenblatt all raised their NVDA price targets immediately after the February 25 print — Rosenblatt moved its target from $245 to $300, the largest percentage increase among the group — on the same day the stock was falling[^18][^47]. Sell-side analysts do not typically raise price targets on results they consider a letdown; a target hike is a statement that the fundamental picture improved. A Goldman Sachs analysis cited in the same coverage offered the more coherent explanation: 2026 growth was already priced into the stock, and what the market wanted from this print was clearer visibility into 2027 — visibility the report didn't fully deliver[^18]. That is a valuation and positioning problem, not an execution problem: a stock priced for perfection can fall on a beat if the beat doesn't extend the visibility window far enough, especially when the whole sector is already jumpy.

Taken together, the Nasdaq-not-Dow breadth, the falling yields, the semiconductor sector's near-equal decline, the pre-print SOXX weakness, and same-day price-target hikes all point the same direction: at least one of the four down days in this sequence carries the fingerprints of sector rotation, not a company-specific NVIDIA problem. It is worth being honest, though, about the limits of this evidence[^12][^17]: the sector-confound case is strongest for February 2026, where a same-day cross-index and cross-peer dataset exists. This piece did not assemble equally granular peer and index data for the November 2025 or May 2026 declines, so generalizing "these drops are usually sector rotation" beyond the one date documented here would overstate the evidence — Section 09 returns to this gap explicitly.

## 05. The Circular-Financing Debate

NVIDIA spent August 2026 at the center of two separate financing stories that Wall Street kept collapsing into one[^23][^28]. The first is a $500 billion third-party capital platform NVIDIA does not fund. The second is a $105 billion guarantee NVIDIA does. Conflating them is where most of the panic — and most of the pushback — actually comes from.

:::stats
- {label: "$500B platform target", value: "$500B+", note: "6-institution MOU, third-party capital"}
- {label: "NVIDIA's optional backstop", value: "$125B", note: "25% cap, contingent guarantee"}
- {label: "OpenAI-specific guarantee", value: "$105B", note: "separate, direct NVIDIA obligation"}
- {label: "Balance-sheet obligations (Q2 FY27)", value: "$279.0B supply / $108.5B guarantee", note: "per company disclosure"}
:::

Start with what NVIDIA actually announced. In August 2026 the company signed non-binding memoranda of understanding with six financial institutions — Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs, and KKR — to stand up "compute financing platforms" targeting more than $500 billion in capital for AI infrastructure buildouts[^23]. Nothing here commits NVIDIA to write a check. The MOUs are non-binding, no individual firm's commitment was disclosed, and no deployment schedule was published. The capital, if it materializes, is raised and held by the consortium — asset managers and banks whose business is precisely this kind of structured lending, not NVIDIA's balance sheet.

NVIDIA's own exposure to that platform is capped and contingent. Jensen Huang said the company has the *option* to backstop up to $125 billion, or 25% of the potential deals — a guarantor of last resort on a fraction of the structure, not the platform's primary funder[^24]. Markets initially treated the mere existence of financing talks as bad news anyway: NVDA fell roughly 2.4–3% (about $130 billion in market cap) on August 10, 2026, when the Financial Times first reported the discussions, though that session also carried a broader semiconductor selloff — the Philadelphia Semiconductor Index down about 2.94% and Intel down roughly 4% on an unrelated equity raise — so isolating the financing-specific portion of that move from the sector-wide one is not clean[^24].

This $500 billion platform is structurally distinct from the $105 billion guarantee NVIDIA separately extended to help OpenAI lease computing infrastructure. The OpenAI guarantee is a direct obligation to one named customer; the six-institution platform is a capital-raising vehicle for third parties across the industry, with NVIDIA's own liability capped well below the headline number[^28]. Financial press that reports "NVIDIA's $500 billion deal" in the same breath as its OpenAI exposure risks implying the company is on the hook for a sum it is not — the two numbers describe different instruments with different counterparties and different loss distributions.

:::quote(attr="Jensen Huang, CEO, NVIDIA")
The demand is real, and the capital is not Nvidia revenue.
:::

:::quote(attr="Colette Kress, CFO, NVIDIA, Q2 FY2027 earnings call")
We recognize the scale of this support, and we know some will call this circular financing. We see it differently.
:::

The skeptical case does not rest on structural confusion, though — it has its own evidence. Short-seller Michael Burry called the arrangement a "Wall Street stunt" with "shades of Enron," pointing specifically to the $105 billion OpenAI guarantee as his clearest circular-financing red flag, alongside a separate Wall Street Journal analysis he cited that counted roughly $3 trillion in off-balance-sheet AI financing commitments across the industry[^48]. Burry holds a disclosed short position in NVDA, which does not make his argument wrong but does mean his incentive and his analysis point the same direction — a caveat worth weighing rather than ignoring.

Sell-side reaction to the platform split cleanly, and neither side is obviously mistaken. BofA's Vivek Arya read the six-institution structure as a pivot *away* from vendor financing precisely because the capital burden now sits with Apollo, BlackRock, Blackstone, Brookfield, Goldman, and KKR rather than NVIDIA's own balance sheet — a genuine de-risking relative to NVIDIA financing its customers directly[^26]. Wells Fargo traders pushed back on the same facts: "In the end NVDA is still a part of the financing," noting that a 25% contingent backstop on a $500 billion platform is still tens of billions of dollars of NVIDIA exposure that did not exist before, structured or not[^26]. Both readings are defensible from the same disclosure — which is the point. This is not a case where one side has the facts and the other doesn't; it is a genuine disagreement about how to price contingent, capped, non-binding exposure that has never been tested by a downturn.

Kress's August 26 remarks are notable less for what they revealed than for what they stopped doing: NVIDIA no longer denies the "circular financing" label, it argues with it[^27]. The same disclosures put $279.0 billion in supply obligations and $108.5 billion in guarantee obligations on NVIDIA's balance sheet as of that quarter — real, quantified figures sitting alongside management's insistence that the arrangement is healthy[^27].

This is the durable question. Beat-or-miss on any single quarter is noise against it; whether these obligations represent demand NVIDIA is financing into existence or demand that would exist anyway is the risk factor that persists into 2027, and it is exactly what the filing language in Section 06 and the broader capex debate in Section 08 have to be read against.

## 06. Reading the Filing

The gap between NVIDIA's press-release framing[^1] and its own SEC disclosures is where this quarter's caution actually lives. Read past the headline beat, and the 10-Q's commitments footnote and concentration tables tell a story about counterparty power the earnings call does not.

:::kv
- {term: "Supply/purchase commitments", def: "$119B (prior qtr) -> $279B (Q2 FY27) -- company states these 'may be cancelable, rescheduled, or adjustable'"}
- {term: "Revenue concentration (Q1 FY27)", def: "3 customers = 54% of total revenue"}
- {term: "Receivables concentration (Q2 FY27)", def: "5 customers = 70% of accounts receivable"}
- {term: "Gross margin trend", def: "75.0% actual (Q2) -> 74.0% guided (Q3), -100bps sequential"}
- {term: "China Data Center revenue", def: "<1% of segment revenue; $0 assumed going forward"}
:::

Start with who is actually buying. NVIDIA's 10-Q for the quarter ended April 26, 2026 discloses that three direct customers accounted for 21%, 17%, and 16% of total revenue — roughly 54% combined — "primarily attributable to the Compute & Networking segment"[^4]. That is not a diversified demand curve. It is three capital-allocation committees, almost certainly hyperscalers building out AI infrastructure, whose internal capex decisions now function as NVIDIA's real top-line driver. The growth story the market is pricing is, in practical terms, a bet that three boardrooms keep saying yes.

The following quarter's 10-Q, for the period ended July 26, 2026, adds a second and distinct lens: accounts receivable[^2]. As of that date, five direct customers accounted for 22%, 14%, 13%, 11%, and 10% of NVIDIA's accounts receivable balance — about 70% combined. This is worth being precise about, because revenue concentration and receivables concentration measure different exposures. Revenue concentration tells you who is buying — the demand side, recognized as goods ship and title transfers. Receivables concentration tells you who currently owes NVIDIA money — the credit side, a snapshot of uncollected balances at a single balance-sheet date. A company can have modest revenue concentration but a receivables balance dominated by one slow-paying customer, or vice versa. Here, both metrics point the same direction: a handful of counterparties sit on both sides of NVIDIA's income statement and balance sheet simultaneously. If any one of those five names delayed payment, renegotiated terms, or paused a purchasing cycle, the effect would show up in working capital before it ever showed up in a guidance cut.

Taken together, [^2] and [^4] describe a company whose growth and whose collections both run through a small, overlapping set of hyperscaler relationships. That is not a solvency concern — these are investment-grade counterparties — but it is a concentration risk in the textbook sense: the variance in NVIDIA's results is increasingly the variance in a handful of external capex budgets, not a diversified base of demand that smooths out any single customer's hesitation.

The commitments footnote in the same July 26, 2026 filing is where the "backlog" narrative gets more complicated[^2]. Total supply and purchase commitments rose from $119 billion the prior quarter to $279 billion — more than doubling in a single quarter. Read as a headline number, that looks like locked-in future revenue. Read as a disclosure, it is something narrower: a set of obligations NVIDIA has entered into with its supply chain and, per the same footnote, with counterparties on the demand side — and the filing's own language qualifies exactly how firm those numbers are.

NVIDIA states plainly that these commitments "may be cancelable, rescheduled, or adjustable." That is the company's own hedge, not an analyst's discount applied after the fact. The same footnote goes further, disclosing that NVIDIA's largest AI-cloud counterparties "can unilaterally stop providing to us and sell to third-party customers at more advantageous rates" — language that describes real customer-side optionality, not a contractually locked pipeline. A $279 billion figure that the filer itself flags as cancelable and subject to counterparties walking toward better terms elsewhere is a materially different object than "backlog" as the word is normally used in a beat-and-raise headline. The number measures intent and capacity planning across the supply chain; it does not measure a receivable NVIDIA is entitled to collect.

That hedge language connects directly to the margin mechanics already flagged in Section 02: gross margin stepped down sequentially from 75.0% actual in the July quarter to a 74.0% guide for the following quarter, a 100-basis-point compression the CFO Commentary confirms alongside a China disclosure worth noting on its own — Hopper/H200 shipments were less than 1% of Data Center revenue in the quarter, and the Q3 guide assumes zero China Data Center compute revenue going forward[^3]. A company guiding margin down while explicitly zeroing out a formerly meaningful geography is not signaling confidence that every commitment on its books converts to revenue on the timeline implied by the topline commitments figure. For scale, none of this is happening at a company standing still: the FY2026 10-K reports roughly 42,000 employees, up 16.67% year over year[^5] — an organization still hiring aggressively even as its own filings narrow the number of counterparties whose decisions move the results.

None of this contradicts the quarter's headline beat. It qualifies it. The filing's own language is more cautious than the press release, and that caution resolves in only one place: whether the handful of hyperscaler customers behind both the revenue and the commitments figures keep their capex plans intact — which is precisely the question Section 08 has to confront at the level of the whole AI-capex cycle, not just one supplier's quarter.

## 07. The China Sideshow

If China export controls were driving NVIDIA's stock the way headlines implied[^31][^32], the one unambiguous, clearly-dated shock in this window should show it. It doesn't. A reported $54 billion order freeze — about as concrete and quantifiable as regulatory bad news gets — moved the stock less in a day than NVIDIA's ordinary trading noise, and the move was gone within 72 hours.

:::timeline
- {date: "2026-01-13", headline: "BIS eases H200 China export review", body: "Case-by-case review replaces presumption of denial. NVDA rises only 0.47% on below-average volume."}
- {date: "2026-01-14", headline: "China customs reportedly blocks H200 imports", body: "An estimated $54B in pending orders frozen. NVDA falls about 1.4%."}
- {date: "2026-01-16", headline: "Suppliers pause production; stock nets flat", body: "NVDA closes at $186.23, down only 0.44% that day and roughly +0.2% net since January 13."}
:::

The sequence itself reads like a real regulatory whiplash. On January 13, BIS eased its review posture on H200 and MI325X exports to China, replacing presumption-of-denial with case-by-case review — on its face, a green light for a market NVIDIA had written down to nothing[^29]. The stock's response to that easing was itself telling: a 0.47% gain on volume roughly 16.5% below its three-month average, not the kind of participation a genuine unlock in a multi-billion-dollar addressable market should generate[^30]. Then, within a day, Chinese customs authorities reportedly moved the other direction entirely, instructing agents to block H200 imports and freezing an estimated $54 billion in orders from Alibaba, ByteDance, and others — a headline number large enough to anchor a week of coverage[^31]. NVDA fell about 1.4% that day.

That 1.4% is the number worth sitting with. A $54 billion freeze, reported and specific rather than speculative, moved the stock by less than one and a half points — comfortably inside NVIDIA's typical single-day range across this entire window, and smaller than several of the post-earnings drops examined in Section 01, where the company had just beaten consensus and guided up. By January 16, after further reporting that component suppliers had paused production lines in response to the customs block — an operational consequence, not just a policy headline — NVDA closed at $186.23, down just 0.44% on the day[^32]. Across the full four trading days from the BIS announcement through the supplier-pause report, the stock was net *up* roughly 0.2%. A sequence that included a genuine regulatory easing, a $54 billion freeze, and a supplier production pause left no net mark at all.

The comparison that matters is the one this article keeps returning to: an ordinary "beat but the stock falls anyway" earnings reaction, of the kind cataloged in Section 01, routinely produced larger single-day moves than this entire China episode combined. If a market that reliably punishes NVIDIA five or six points for merely-good earnings shrugs off a $54 billion order freeze, the freeze was not new information to that market — it was already in the price.

That is consistent with what shows up on the other side of the ledger. NVIDIA has carried effectively zero China revenue in its guidance through every 2026 quarter (Section 02, Section 06), and the muted January reaction suggests investors had already marked China down to near-zero in their own models well before the company said so explicitly, on the record, in a filing.

## 08. Zooming Out: Is the Whole AI-Capex Cycle the Story?

NVIDIA's earnings-day swings are a symptom, not the disease. Underneath every one of those moves sits an unresolved, much larger argument about whether the roughly three-quarters-of-a-trillion-dollar hyperscaler buildout[^37] is durable demand-driven scaling or a structurally fragile boom running ahead of its own returns[^35][^36].

:::donut(center-label="~$739B")
- {label: "Amazon", value: 29.8}
- {label: "Alphabet", value: 27.1}
- {label: "Microsoft", value: 24.6}
- {label: "Meta", value: 18.5}
:::

Combined 2026 AI capex guidance across Microsoft, Alphabet, Amazon and Meta has climbed to roughly $725-739 billion, up about 77% from roughly $410 billion in 2025 — and the raise wasn't a one-off: every major cloud provider lifted guidance at least once during the year, and most did it twice[^37]. That $725B-versus-$739B spread is itself worth flagging rather than rounding away: the two figures come from aggregating slightly different same-year disclosures across sources that don't share identical accounting definitions for what counts as "AI capex" versus general data-center spend, so the donut above should be read as directionally right, not to the decimal.

The skeptical case starts from a simple pattern-matching exercise, made rigorous. Apollo Global's chief economist Torsten Slok has pointed out that AI data-center capex is rising as a share of GDP at nearly twice the pace of the 2000s housing boom — roughly 0.85 percentage points of GDP per year, versus about 0.5pp/year for housing in the run-up to 2007 and just 0.15pp/year for the 1990s telecom buildout that preceded the dot-com bust[^35]. The pace comparison matters more than the absolute level, because it is a claim about velocity of capital commitment relative to the size of the economy — the same metric that, in both prior cycles, proved to be the leading indicator of how violently the unwind happened when it came.

:::quote(attr="Torsten Slok, Chief Economist, Apollo Global Management")
A cycle that builds at 0.85 percentage points of GDP a year can unwind at a similar pace.
:::

The Bank for International Settlements has now made a version of this argument formally, not just anecdotally. Its 2026 Annual Economic Report named AI capex a financial-stability "pressure point," warning that the opaque circular financing arrangements running through the sector (see Section 05) could turn an ordinary disappointment in AI returns into something worse — a "protracted investment bust" — if hyperscaler capex, which it projects will exceed $1 trillion across the top five companies in 2025-2026 combined, keeps outpacing free cash flow[^36]. That is a specific transmission mechanism, not a vague warning: it names the trigger (a returns disappointment), the amplifier (circular financing obscuring who actually bears the loss), and the outcome (a multi-year, not a one-quarter, downturn).

The defense of the cycle is not "trust us" — it is a specific, checkable counter-claim about what is actually constraining growth, made independently by executives at three different companies. Microsoft CFO Amy Hood held CY2026 capex guidance at roughly $175-190 billion and attributed it explicitly to demand outstripping available capacity, not speculative overbuild[^38]. Amazon CEO Andy Jassy pointed to AWS's roughly $364 billion backlog — a figure that excludes a separate Anthropic commitment exceeding $100 billion — as evidence that Amazon's capex raise to $220 billion for 2026 is demand-driven rather than speculative[^39]. Neither of those is a vague reassurance; both are backlog and duration claims that will either be validated or falsified by 2027 utilization data.

The most falsifiable version of the defense, though, comes from NVIDIA itself. On the company's August 26, 2026 earnings call, CFO Colette Kress said its FY2028 guidance of roughly 70% revenue growth is explicitly "a supply-constrained outlook," pointed to a cloud-industry backlog she put at greater than $2 trillion, and said memory (DRAM/HBM) price increases "have exceeded our prior expectations and are headed even higher into next year"[^40] — language that describes a bottleneck on the supply side, not softness on the demand side. Three months earlier, on the May 20, 2026 call, CEO Jensen Huang went further, saying "my sense is that we will be supply constrained throughout the entire life of Vera Rubin," NVIDIA's next-generation platform after Blackwell, while Kress disclosed total supply and prepaid commitments of $145 billion as of that quarter[^41].

:::quote(attr="Colette Kress, CFO, NVIDIA, Q2 FY2027 earnings call")
This is a supply-constrained outlook.
:::

That said, at least one plank of the defense hands the skeptics ammunition rather than rebutting them. Hood's capex framing rests partly on an accounting shift — extending datacenter useful life from 15 to 25 years — that is the same category of assumption Section 06 criticizes when it shows up in NVIDIA's own margin disclosures: it lowers the depreciation hit *today* by betting on utilization and resale value holding up over a much longer horizon, which is precisely the kind of bet a demand-side disappointment would break.

So the two sides are not really arguing past each other, and they're not arguing the same thing either. Slok and the BIS are making a top-down, GDP-share and financial-stability claim that plays out over years and is checkable against aggregate capital-formation data; Hood, Jassy, Huang and Kress are making a bottom-up, backlog-and-supply-constraint claim that is checkable quarter by quarter against utilization and order books. Both claims are falsifiable, on different clocks, against different evidence — which is exactly why neither side has won the argument yet.

## 09. What Would Break This Thesis

The two mechanisms in Section 03 — anchoring[^45] and options-market calibration[^22] — explain four data points, not forty. A sample of five earnings reactions, four falls and one rally, is thin enough that a skeptical reader should ask what would falsify the reading offered here rather than confirm it after the fact.

Start with the cleanest test: the next print. If NVIDIA beats and guides up again in its next quarterly report and the stock falls the following day by a magnitude the options market did not price in — not a sentiment-driven dip inside the implied range, but a move that exceeds it — that would undercut the calibration argument in Section 03 more directly than anything in this piece. It is worth being explicit that the August 2026 print already gave one data point cutting the other way: implied volatility priced a move of roughly 5.4-5.9%[^19], and the realized move (+8.74%) blew through the top of that range[^6]. The options market was not well-calibrated for August — it under-priced uncertainty, and direction happened to break upward rather than downward. A repeat of that miscalibration, in either direction, would mean the "the options market usually gets the magnitude right" claim in Section 03 is weaker going forward than the 12-quarter trailing average suggests.

Second, the sector-confound argument in Section 04 rests on unusually good same-day data for exactly one of the four declines — February 2026. This piece did not assemble comparably granular cross-index, cross-peer evidence for the November 2025 or May 2026 drops. If a future examination of those two dates found NVDA moved alone while the Nasdaq and semiconductor peers were flat or up, that would weaken the generalized "these reactions are often sector rotation" framing to "this happened once, in February."

Third, and most consequentially: the circular-financing structures described in Sections 05 and 06 are the risk this piece considers most durable, precisely because they do not resolve on an earnings-day timescale. NVIDIA's $279 billion in supply commitments carry the company's own hedge language ("may be cancelable, rescheduled, or adjustable")[^2], and revenue is concentrated in three to five counterparties[^4][^2]. If hyperscaler capex growth decelerates in 2027 — the falsifiable window Amazon and Microsoft's own guidance points to[^38][^39] — while NVIDIA's guarantee and supply obligations remain on the books, Huang's "the capital is not Nvidia revenue" defense[^26] would look considerably thinner than it does with capex still accelerating. Michael Burry's "shades of Enron" framing[^48] is easy to dismiss as a short-seller talking his book; it becomes harder to dismiss if a specific counterparty in the $105 billion OpenAI guarantee or the $500 billion platform actually renegotiates or defaults. That single event — not another quarter of beat-and-raise — is the one this thesis would not survive intact.

:::position(confidence=medium, horizon=2027-Q4)
stance: "The quarterly earnings-reaction pattern examined in this piece is a second-order story. NVIDIA's real tail risk is the circular-financing structure disclosed in its own filings — concentrated customer commitments and contingent guarantees that have not yet been tested by a hyperscaler capex slowdown."
consensus: "Most coverage treats each earnings-day stock move (up or down) as the primary signal worth watching quarter to quarter."
resolves: "Whether NVIDIA's disclosed supply and guarantee obligations to a small number of hyperscaler and AI-lab counterparties are renegotiated, written down, or materially expanded by roughly Q4 2027."
:::

None of this is an argument that NVIDIA's results are weak — by every metric in Sections 01 and 02, they are not. It is an argument that the more interesting question was never "why did the stock fall after a beat," which behavioral anchoring and options calibration answer reasonably well. It is whether the financing structure underneath the beat can survive the first quarter that isn't one.

:::references
- {id: 1, title: "NVIDIA Announces Financial Results for Second Quarter Fiscal 2027", url: "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/default.aspx", source: "NVIDIA Investor Relations", date: "2026-08-26"}
- {id: 2, title: "NVIDIA Form 10-Q, quarter ended July 26, 2026", url: "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm", source: "SEC EDGAR", date: "2026-08-26"}
- {id: 3, title: "NVIDIA Q2 FY2027 CFO Commentary", url: "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27cfocommentary.htm", source: "SEC EDGAR", date: "2026-08-26"}
- {id: 4, title: "NVIDIA Form 10-Q, quarter ended April 26, 2026", url: "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000052/nvda-20260426.htm", source: "SEC EDGAR", date: "2026-04-26"}
- {id: 5, title: "NVIDIA Form 10-K, fiscal year ended January 25, 2026", url: "https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm", source: "SEC EDGAR", date: "2026-01-25"}
- {id: 6, title: "Nvidia (NASDAQ:NVDA) Stock Price Up 8.7% Following Better-Than-Expected Earnings", url: "https://www.marketbeat.com/instant-alerts/price-nvidia-nasdaq-nvda-stock-price-up-87-following-better-than-expected-earnings-2026-08-27/", source: "MarketBeat", date: "2026-08-27"}
- {id: 7, title: "NVIDIA Announces Financial Results for Second Quarter Fiscal 2027", url: "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/default.aspx", source: "NVIDIA Investor Relations", date: "2026-08-26"}
- {id: 8, title: "Nvidia Drops 3.3% as $315 Target Meets a $108 Billion Test", url: "https://finance.yahoo.com/markets/stocks/articles/nvidia-drops-3-3-315-222706659.html", source: "Yahoo Finance", date: "2026-08-29"}
- {id: 9, title: "Nvidia Pauses Revenue-Sharing Deals With AI Cloud Companies, WSJ Reports", url: "https://money.usnews.com/investing/news/articles/2026-08-27/nvidia-pauses-revenue-sharing-deals-with-ai-cloud-companies-wsj-reports", source: "US News (WSJ)", date: "2026-08-27"}
- {id: 10, title: "NVDA stock price on August 28, 2025", url: "https://www.statmuse.com/money/ask/nvda+stock+price+on+august+28+2025", source: "StatMuse", date: "2025-08-28"}
- {id: 11, title: "NVDA stock price on November 20, 2025", url: "https://www.statmuse.com/money/ask/nvda+stock+price+on+november+20+2025", source: "StatMuse", date: "2025-11-20"}
- {id: 12, title: "NVDA stock price on February 26, 2026", url: "https://www.statmuse.com/money/ask/nvda+stock+price+on+february+26+2026", source: "StatMuse", date: "2026-02-26"}
- {id: 13, title: "NVDA stock price on May 21, 2026", url: "https://www.statmuse.com/money/ask/nvda+stock+price+on+may+21+2026", source: "StatMuse", date: "2026-05-21"}
- {id: 15, title: "Nasdaq Drops Nearly 2% As The Tech Selloff Deepens Post-Nvidia's Earnings", url: "https://seekingalpha.com/news/4557921-nasdaq-drops-nearly-2-percent-as-the-tech-selloff-deepens-post-nvidias-earnings", source: "Seeking Alpha", date: "2026-02-25"}
- {id: 16, title: "Stock market today: Nasdaq falls as chip stocks retreat", url: "https://finance.yahoo.com/news/stock-market-today-feb-26-183634080.html", source: "Yahoo Finance", date: "2026-02-26"}
- {id: 17, title: "Semiconductor Stocks Fall Despite Nvidia's Strong Earnings", url: "https://www.indexbox.io/blog/semiconductor-stocks-fall-despite-nvidias-strong-earnings/", source: "IndexBox", date: "2026-02-26"}
- {id: 18, title: "Nvidia (NVDA) Earnings, Q4 Stock Price, Investors & Value", url: "https://www.tradingkey.com/analysis/stocks/us-stocks/261628049-nvidia-nvda-earnings-q4-stock-price-investors-value-tradingkey", source: "TradingKey", date: "2026-02-25"}
- {id: 19, title: "NVIDIA implied move lowest in two years", url: "https://cryptobriefing.com/nvidia-implied-move-lowest-volatility-two-years/", source: "CryptoBriefing", date: "2026-08"}
- {id: 20, title: "Nvidia Earnings: Trading the 8% Move the Options Market Is Pricing", url: "https://www.home.saxo/content/articles/options/nvidia-earnings-trading-the-8-move-the-options-market-is-pricing-18052026", source: "Saxo Bank", date: "2026-05-18"}
- {id: 21, title: "Nvidia Shares Dropped After Stellar Earnings. Is This a Buying Opportunity?", url: "https://www.fool.com/investing/2026/05/31/nvidia-shares-dropped-after-stellar-earnings-is-th/", source: "The Motley Fool", date: "2026-05-31"}
- {id: 22, title: "NVIDIA Earnings: Options Market Expectations vs. Reality", url: "https://orats.com/blog/nvidia-earnings-options-market-expectations-vs-reality", source: "ORATS", date: "2026-08"}
- {id: 23, title: "Wall Street giants partner with Nvidia to raise $500 billion for AI infrastructure", url: "https://finance.yahoo.com/technology/ai/articles/wall-street-giants-partner-nvidia-163441421.html", source: "Yahoo Finance (Reuters/AP)", date: "2026-08-11"}
- {id: 24, title: "Nvidia Stock Loses $130 Billion In Market Value As Firm Reportedly Enters $500 Billion AI Financing Deal", url: "https://www.forbes.com/sites/antoniopequenoiv/2026/08/10/nvidia-stock-loses-130-billion-in-market-value-as-firm-reportedly-enters-500-billion-ai-financing-deal/", source: "Forbes", date: "2026-08-10"}
- {id: 25, title: "Michael Burry Flags Nvidia's $500 Billion AI Financing Deal", url: "https://finance.yahoo.com/technology/ai/articles/michael-burry-flags-nvidias-500-220000898.html", source: "Yahoo Finance", date: "2026-08-14"}
- {id: 26, title: "Nvidia Tries To Quiet 'Circular Financing' Accusations. Wall Street Isn't Sure It Will.", url: "https://www.cnbc.com/2026/08/11/nvidia-tries-to-quiet-circular-financing-accusations-wall-street-unsure-it-will-.html", source: "CNBC", date: "2026-08-11"}
- {id: 27, title: "Why Nvidia Says Its AI Partnerships Aren't 'Circular Financing'", url: "https://finance.yahoo.com/video/why-nvidia-says-its-ai-partnerships-arent-circular-financing-222400222.html", source: "Yahoo Finance (earnings call coverage)", date: "2026-08-26"}
- {id: 28, title: "Michael Burry Points To Nvidia's $105B OpenAI Guarantee As 'Circular Financing' Red Flag", url: "https://www.benzinga.com/markets/earnings/26/08/61486426/michael-burry-points-to-nvidias-105b-openai-guarantee-as-circular-financing-red-flag-whistling-past-the-graveyard", source: "Benzinga", date: "2026-08"}
- {id: 29, title: "Department of Commerce Revises License Review Policy for Semiconductors Exported to China", url: "https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china", source: "U.S. Department of Commerce / BIS", date: "2026-01-13"}
- {id: 30, title: "Stock Market Today, Jan 13: Nvidia Rises on H200 Export Developments", url: "https://www.nasdaq.com/articles/stock-market-today-jan-13-nvidia-rises-h200-export-developments", source: "Nasdaq.com", date: "2026-01-13"}
- {id: 31, title: "Nvidia Slips 1.4% as China Reportedly Blocks H200 AI Chip Imports", url: "https://www.fxstreet.com/news/nvidia-slips-14-as-china-reportedly-blocks-h200-ai-chip-imports-202601151321", source: "FXStreet", date: "2026-01-15"}
- {id: 32, title: "Chinese Customs Block Nvidia H200 Shipments Hours After US Approval, Freezing $54B in Orders", url: "https://winbuzzer.com/2026/01/14/chinese-customs-block-nvidia-h200-shipments-hours-after-us-approval-freezing-54b-in-orders-xcxwbn/", source: "Winbuzzer (citing Reuters)", date: "2026-01-14"}
- {id: 33, title: "NVIDIA (NVDA) Statistics — Valuation Ratios", url: "https://stockanalysis.com/stocks/nvda/statistics/", source: "StockAnalysis.com", date: "2026-09-03"}
- {id: 34, title: "Nvidia's Forward P/E Has Actually Fallen As Its Stock Rose", url: "https://www.fool.com/investing/2026/07/11/nvidias-forward-pe-has-actually-fallen-as-its-stoc/", source: "The Motley Fool", date: "2026-07-11"}
- {id: 35, title: "The AI Capex Boom Is Building Twice as Fast as the Housing Boom", url: "https://www.apollo.com/wealth/insights-news/insights/daily-spark/the-ai-capex-boom-is-building-twice-as-fast-as-the-housing-boom", source: "Apollo Global Management", date: "2026-08"}
- {id: 36, title: "BIS Warns Hyperscaler Data-Center Spending Is a $1 Trillion Gamble", url: "https://fortune.com/2026/06/29/bis-central-bank-warning-hyperscaler-data-center-1-trillion-gamble-recession/", source: "Fortune", date: "2026-06-29"}
- {id: 37, title: "AI Spending 2026", url: "https://valueaddvc.com/ai-spending", source: "ValueAddVC", date: "2026-08"}
- {id: 38, title: "2026 Hyperscaler Capex Tops $700 Billion: Analysis", url: "https://www.tmtfinance.com/intel/2026-hyperscaler-capex-tops-us700bn-analysis", source: "TMT Finance", date: "2026-07-29"}
- {id: 39, title: "Google, SpaceX, Microsoft and Amazon Are About to Spend Twice the Entire U.S. Defense Budget on AI", url: "https://247wallst.com/investing/2026/06/19/google-spacex-microsoft-and-amazon-are-about-to-spend-twice-the-entire-u-s-defense-budget-on-ai/", source: "24/7 Wall St", date: "2026-07-30"}
- {id: 40, title: "NVIDIA (NVDA) Q2 2027 Earnings Call Transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/08/31/nvidia-nvda-q2-2027-earnings-call-transcript/", source: "The Motley Fool", date: "2026-08-26"}
- {id: 41, title: "NVIDIA (NVDA) Q1 2027 Earnings Call Transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/05/20/nvidia-nvda-q1-2027-earnings-transcript/", source: "The Motley Fool", date: "2026-05-20"}
- {id: 42, title: "NVIDIA Corporation (Q182477)", url: "https://www.wikidata.org/wiki/Q182477", source: "Wikidata", date: "2026-09-03"}
- {id: 43, title: "Nvidia Has Fallen After Four Straight Earnings Beats. Here's Why It Could Happen Again.", url: "https://247wallst.com/investing/2026/08/26/nvidia-has-fallen-after-four-straight-earnings-beats-heres-why-it-could-happen-again/", source: "24/7 Wall St", date: "2026-08-26"}
- {id: 44, title: "Here we go again with Nvidia falling on earnings. What the sellers are missing", url: "https://www.cnbc.com/2026/05/21/here-we-go-again-with-nvidia-falling-on-earnings-what-the-sellers-are-missing.html", source: "CNBC", date: "2026-05-21"}
- {id: 45, title: "Why the post-earnings announcement drift persists near 52-week highs", url: "https://klementoninvesting.substack.com/p/why-the-post-earnings-announcement", source: "Klement on Investing", date: "2026"}
- {id: 47, title: "Rosenblatt Raises NVIDIA (NVDA) Price Target to $300 Following Buy Rating", url: "https://www.gurufocus.com/news/8656989/rosenblatt-raises-nvidia-nvda-price-target-to-300-following-buy-rating-nvda-stock-news", source: "GuruFocus", date: "2026-02-26"}
- {id: 48, title: "Michael Burry Doubles Down on Nvidia Short After $500B Chip Deal He Calls a 'Wall Street Stunt' With 'Shades of Enron'", url: "https://finance.yahoo.com/markets/stocks/articles/michael-burry-doubles-down-nvidia-160000531.html", source: "Yahoo Finance", date: "2026-08-14"}
:::
