---
eyebrow: ANALYSIS · AI FINANCE · IPO
title: "Anthropic's $16.8B quarter: the profit is adjusted, the cash flow is leased, and $110B is just Q3 repeated"
deck: What Anthropic told prospective IPO investors on 14 October 2026, what its "adjusted" profitability leaves out, and why a $110B year-end run rate is not guidance but the arithmetic of one more 45% quarter.
lede: |
  On Wednesday 14 October 2026, at an investor day in San Francisco with CEO Dario Amodei and CFO Krishna Rao, Anthropic told prospective IPO investors that third-quarter revenue was $16.8 billion, up about 45% from the second quarter, and that it was profitable "on an adjusted basis". The Financial Times broke the number. Reuters and Bloomberg then confirmed it through attendees. Within hours a second figure was attached to the story: a $110 billion annualized run rate by year-end. The revenue number is the most solid thing in the story: three outlets with independent sourcing agree on it. Almost everything around it is softer. The profit is a margin with no dollar figure and no definition. The cash flow benefits from roughly $161 billion of equipment financed through leases rather than bought with cash. And the $110 billion was never an Anthropic number. It is what you get by assuming Q4 repeats Q3's growth rate.
stats:
  - {label: Q3 2026 revenue, value: "$16.8B", note: "+45% QoQ; FT, Reuters, Bloomberg"}
  - {label: Q3 annualized, value: "$67.2B", note: "16.8 × 4, our arithmetic"}
  - {label: Adjusted op. margin, value: "~11%", note: "excludes stock comp; period disputed"}
  - {label: 2025 GAAP operating loss, value: "$8.06B", note: "leaked draft S-1, via Reuters"}
domain: finance
---

:::callout(kind=info, label="The short answer")
- **The $16.8B is solid as a reported figure, but unaudited.** The FT, Reuters (two attendees) and Bloomberg agree on it. Anthropic has not confirmed it on the record, and no public S-1 exists yet. [^1,2,8]
- **"Adjusted" operating profit excludes stock-based compensation but, on the definition used in Anthropic's May projections, includes training costs.** The 80–85% "gross margin" is the measure that leaves training out. Executives cited an operating margin of about 11% and gave no dollar profit. The Information says the 11% covers the year through Q3, not Q3 alone. [^3,7,46,47]
- **$110B is not Anthropic guidance.** Reuters attributes it to estimates by analysts who met executives. According to The Decoder, Anthropic gave no September run rate and no full-year outlook. [^2,3]
- **The arithmetic works only if growth does not slow.** Repeat Q3's 45% quarter-on-quarter growth once more, compounded smoothly by month, and the December exit rate lands at about $110B. If growth slows to roughly 3% a month, which is what the Q3 total implies once you anchor to the $65B end-July run rate, the year ends nearer $75B.
:::

The rest of this piece works through four questions in order. What exactly was disclosed, and by whom? How does the quarterly revenue reconcile with the run-rate figures that preceded it? What does "adjusted" remove, and how big are those removals? And what has to be true in Q4 for $110B to happen? One framing note applies throughout. Every Anthropic financial figure in this article comes either from press accounts of a confidential draft prospectus or from a private investor meeting. Ratios and projections computed from those figures are labelled as our arithmetic, and the inputs are cited.

## 01. What was disclosed, by whom, and in what form

The only figure with independent multi-outlet sourcing is the revenue line. Each of the other numbers in circulation traces back to a single outlet, a reporter's tweet, or analyst extrapolation.

Reuters' account is the most explicit about its sourcing. It says Q3 revenue "rose to $16.8 billion from $11.6 billion in the second quarter and $4.7 billion in the first quarter", according to two people who attended an investor day at Anthropic's San Francisco headquarters. Amodei and Rao both attended. [^1,2] The same report says the company was "profitable on an adjusted basis in the third quarter", and that "The Financial Times first reported the third-quarter revenue figure." [^1] Bloomberg, citing people familiar with the matter, put Q2 at $11.5 billion and growth at about 46%. That small discrepancy probably traces back to August's preliminary "more than $11.5 billion" figure. [^5,18]

:::kv
- {term: "Q3 2026 revenue", def: "$16.8B. FT first, then Reuters (two attendees) and Bloomberg (people familiar). Not confirmed by Anthropic. [^1,2,5,8]"}
- {term: "Q2 / Q1 2026 revenue", def: "$11.6B / $4.7B (Reuters). Bloomberg gives Q2 as $11.5B. [^2,5]"}
- {term: "Profit metric", def: "Adjusted operating margin of about 11% (Bloomberg: \"11%+\"). Stock-based compensation excluded. No dollar figure. [^3,7]"}
- {term: "Gross margin", def: "Adjusted gross margin of 85% (Bloomberg). Exclusions not stated; in September the FT said the >80% figure leaves out training. [^7,47]"}
- {term: "Cash flow", def: "\"Cash flow positive\" (FT). Bloomberg's Ed Ludlow tweeted \"Free cash flow: Positive\". No amount given. [^4,7]"}
- {term: "Compute efficiency", def: "$1.70 of revenue per $1 of compute in Q3 (FT). [^4]"}
- {term: "$110B run rate", def: "An analyst estimate (Reuters) or an investor expectation (WSJ). Not company guidance. [^2,3]"}
- {term: "IPO timing", def: "Marketing as soon as the week of 9 November, trading before Thanksgiving (Bloomberg). [^6]"}
:::

The detail that matters most is the one *not* disclosed. According to The Decoder, some investors were disappointed in part because "the company did not discuss its September annualized revenue rate or a full-year outlook." [^3] A company that had published or leaked a run-rate milestone roughly every six weeks all year ($14 billion in February, $30 billion in April, $47 billion in May, $65 billion at end-July) went silent on the metric in the quarter it reported recognized revenue for the first time. [^14,15,16,17] Reuters' wording on $110 billion is unambiguous: "analysts who met with company executives earlier this week" estimate the run rate "could… reach $110 billion by the end of the year." [^1,2] Euronews, citing Bloomberg, goes further and says Anthropic "is now reportedly expected to end 2026 below $100 billion", short of what several backers had anticipated. [^5]

The format also matters, for a legal reason. Testing-the-waters conversations with institutional investors are governed by Securities Act Rule 163B, which exempts them from the usual pre-filing restrictions but says they are "deemed an offer." [^30] Section 08 returns to why that matters. The practical point now, on our reading, is that numbers told to investors privately are not throwaway figures.

**What would weaken this read:** if Anthropic's public S-1, which must be on file 15 days before a 9 November roadshow, contains a Q3 income statement with a defined adjusted measure, most of the ambiguity in this section disappears. [^34] **Why it matters:** an IPO priced at a reported target of more than $2 trillion, double the $965 billion Series H valuation in May, rests on figures nobody outside the room has seen in writing. [^2,16]

## 02. The revenue line: $4.59B in a year, then $16.8B in a quarter

The recognized-revenue series, though leaked and unaudited, is internally consistent. Through Q2 it reconciles with Anthropic's own published run-rate milestones to within a few percent. That makes it the best anchor in the story.

Reuters' reading of the draft prospectus puts 2025 revenue at $4.59 billion. That is up 1,088% from roughly $386 million in 2024, and it was earned at an operating loss of $8.06 billion. [^9,10] Bloomberg, citing investor documents in August, reported Q2 2025 revenue of $787 million and Q1 2026 revenue of $4.73 billion. [^18] Q1 2026 alone therefore slightly exceeded all of 2025.

:::exhibit(num="Exhibit 1", title="Anthropic quarterly recognized revenue", subtitle="$ billion, as reported from leaked investor materials", source="Bloomberg (Q2 2025, Q1 2026); Reuters (Q2, Q3 2026). Unaudited.")
:::bar-chart(title="Quarterly revenue", orientation=vertical, value-unit=$, value-suffix=B)
categories: Q2 2025, Q1 2026, Q2 2026, Q3 2026
Revenue: 0.787, 4.73, 11.6, 16.8
:::
:::

The run-rate series Anthropic chose to publish tells the same story at a different speed. The company's own releases put run-rate revenue at about $1 billion at the start of 2025, "over $5 billion" by August 2025, $14 billion on 12 February 2026, more than $30 billion in April, and more than $47 billion in early May. [^13,14,15,16] Bloomberg then reported more than $19 billion in early March and more than $65 billion at the end of July, citing company investor updates. [^43,17,19]

:::line-chart(title="Anthropic annualized run-rate revenue, as published or leaked", subtitle="$ billion; company releases and Bloomberg", y-unit=$)
x: 2025-01,2025-08,2025-12,2026-02,2026-03,2026-04,2026-05,2026-07
Run rate: 1,5,9,14,19,30,47,65
:::

The two series reconcile through Q2. Q2's $11.6 billion averages $3.87 billion a month, a $46.4 billion annualized pace. That sits almost exactly on the $47 billion run rate Anthropic announced in May, the middle month of the quarter. [^2,16] Q3 is where the fit loosens. Its $16.8 billion averages $5.6 billion a month, or $67.2 billion annualized, which is barely above the $65 billion pace already reported for the *end of July*, the first month of the quarter. [^2,17]

:::slope(left-label="Q1→Q2 2026", right-label="Q2→Q3 2026", unit=%)
| Measure | Q1→Q2 2026 | Q2→Q3 2026 |
|---|---|---|
| Sequential revenue growth | 147 | 45 |
:::

Growth fell by roughly two-thirds in one quarter, from about 147% sequentially to about 45%. That is our arithmetic on the reported figures. [^2] Euronews, citing the FT, reported that the Q3 figure fell short of some investors' hopes. [^5] One investor quoted on Techmeme said buy-side expectations had been near $18 billion. [^7] The counterpoint is real: 45% quarter-on-quarter still compounds to about 340% a year (our arithmetic). **Why it matters:** the $110 billion question is entirely a question about which of those two growth rates Q4 resembles.

## 03. Run rate is not revenue: the formula, the gross-up, and the September gap

"Run rate" is a management metric with no GAAP definition, and three features of Anthropic's version make it run hotter than recognized revenue. It annualizes a short window. It books cloud-reseller sales gross. And it was last published at a moment that Q3's total now suggests was near a local peak.

**The formula.** Anthropic has never published a definition. Its Series H release simply states that "our run-rate revenue crossed $47 billion earlier this month." [^16] The method in circulation comes from Reuters Breakingviews, citing a person familiar, as glossed by Simon Willison. Take the last 28 days of consumption-billed sales and multiply by 13, then add monthly subscriptions multiplied by 12. [^22] Ed Zitron reports the FT describing the same method from "a person with knowledge of its accounting practices." [^23] The multiplier is harmless, since 28 × 13 = 364. The lever is the *window*. For a business that is mostly metered API consumption, a 28-day window that includes a launch surge, a large one-off batch job or distillation traffic gets multiplied by thirteen.

**The gross-up.** Reuters' reading of the draft prospectus says marketplace sales through Amazon and Google were $2.16 billion, 47% of 2025 revenue. Anthropic books them gross as principal and records the partners' fees, about $351 million by Reuters' estimate, in the "sales, marketing, and partnerships" operating-expense line. [^12] That is a 16% partner cut on 47% of revenue. The $351 million in fees is about 7.6% of 2025 revenue, which would not appear under net presentation (our arithmetic). OpenAI, by contrast, books its Microsoft revenue share net. [^23,24] The gross-up is real but modest. In an April internal memo, OpenAI's revenue chief Denise Dresser claimed that Anthropic's $30 billion run rate was overstated by about $8 billion. [^51] That is roughly 27%, several times what the prospectus figures support (our arithmetic). The gross-up also leaves operating income unchanged, because "operating income does not move a dollar under either treatment." [^24]

:::donut(center-label="2025 revenue")
- {label: "Sold through Amazon/Google marketplaces (booked gross)", value: 47}
- {label: "Direct (API, subscriptions, enterprise)", value: 53}
:::

**The September gap.** In mid-September the New York Times reported, citing people familiar with the company's finances, that Anthropic would exceed $100 billion in annualized revenue. Relays disagree on the tense. Gulf News renders it as "by the end of 2026". Axios, as relayed by Yahoo Finance, wrote that it "is now pacing" above $100 billion, "up 50% from just two months ago." [^20,21] The Q3 total settles the dispute. If September alone had run at a $100 billion pace ($8.33 billion in the month), July and August together could have brought in only $8.47 billion. That is an average annualized pace of $50.8 billion, *below* the $65 billion Bloomberg reported for the end of July. [^17,2] Unless revenue fell in August, the "already pacing at $100 billion" reading is arithmetically incompatible with the Q3 total. The year-end-forecast reading is the only one that survives.

:::compare
- {role: LOWEST, name: "Flat path from $65B end-July", value: "~$69B"}
- {role: HIGHEST, name: "\"Pacing above $100B\" (Axios relay of NYT)", value: "$100B+"}
- {role: SUBJECT, name: "SemiAnalysis estimate, end-September (via FT)", value: "~$74B"}
:::

The plausible end-September exit rate therefore lies between about $69 billion and $76 billion, depending on how growth was distributed across the three months. SemiAnalysis's estimate of about $74 billion, reported by the FT, sits inside that band. [^4,5] The low end assumes July ran at the reported $65 billion end-July pace and growth compounded at about 3% a month thereafter. The high end assumes the quarter's 45% growth compounded smoothly at about 13% a month. Both are our arithmetic.

**What would weaken this:** if the run rate is defined on something other than recognized revenue, such as including contracted minimum commitments or credits, then "$100 billion pace" and "$16.8 billion quarter" measure different things and can both be true. Nothing published supports that. **Why it matters:** the $110 billion target is a growth rate applied to a starting point. A $74 billion starting point needs about 49% growth in one quarter. A $100 billion starting point needs 10%.

## 04. What "adjusted" profitability actually excludes

Every profit claim made on 14 October carries the word "adjusted". One exclusion from operating profit is on the record: stock-based compensation. Training compute is excluded from the *gross margin* but, on the definition reported in May, not from adjusted operating income. A third item is structural. The roughly $34 billion of 2025 losses tied to convertible financing never reaches operating income at all.

Start with the GAAP baseline that the S-1 will have to show. For 2025, Reuters' reading of the draft prospectus reports operating expenses of $12.65 billion against revenue of $4.59 billion, an operating loss of $8.06 billion (2024: $2.98 billion). [^9,10] Compute and infrastructure took $7.33 billion of that, about 58% of operating expenses and 1.6 times revenue. [^9] The net loss was about $42 billion. Roughly $34 billion of it was a non-cash charge "reflecting a rise in the estimated value of financing that could later turn into Anthropic shares." [^9]

:::bars
- {label: "Operating expenses, 2025", value: "$12.65B", pct: 100}
- {label: "…of which compute & infrastructure", value: "$7.33B", pct: 58}
- {label: "…of which everything else", value: "$5.32B", pct: 42}
- {label: "Revenue, 2025", value: "$4.59B", pct: 36}
- {label: "Operating loss, 2025", value: "−$8.06B", pct: 64}
:::

**Exclusion 1: stock-based compensation.** The FT reported in September that Anthropic's adjusted operating income measure "strips out costs including stock-based compensation." The Information says the Q3 margin "leaves out major costs like stock-based compensation." [^47,3] Excluding stock pay is routine and accepted by the SEC, but at Anthropic the amount could be very large. The company's private valuation went from $380 billion in February to $965 billion in May, and a $2 trillion IPO target sits on top of that. [^14,16,2] Every restricted unit granted in 2026 is expensed at the much higher valuation in force when it was granted. No outlet has reported Anthropic's stock-compensation expense, so the size of this add-back is the largest unknown in the profit claim.

**Not an exclusion from operating profit: training compute.** This is where much of the commentary goes wrong. The FT reported that Anthropic's gross margins are "above 80 per cent" before revenue shared with distribution partners and "the cost of training its models." Bloomberg's Q3 figure is an 85% adjusted gross margin. [^47,7] But the WSJ's reading of the May fundraising projections, as reported by PYMNTS, is explicit: "The operating profit figure includes model training costs but excludes stock-based compensation." [^46] On that definition, training spend is inside the 11%. Put the ratios together and the size of it becomes visible. At $1.70 of revenue per compute dollar, Q3 compute spend was about $9.9 billion, or 59% of revenue. An 85% gross margin implies cost of revenue of only about $2.5 billion. That leaves roughly $7.4 billion of Q3 compute, about 44% of revenue, outside cost of revenue but, on the May definition, still charged against adjusted operating income. All three figures are our arithmetic on the reported ratios. [^4,7] That makes the claim *stronger* than its critics allow: the business covered its training bill in Q3 before stock pay. The caveat is that the definition comes from May projections. The October presentation's adjustment list has not been reported. [^3]

**Exclusion 2: the period.** Bloomberg's Ed Ludlow reported the adjusted operating margin as "11%+". The Information, relayed by The Decoder, says the 11% was "for the year through Q3." [^7,3] Those two readings imply very different Q3 profits. Eleven percent of Q3 alone is about $1.85 billion. Eleven percent of year-to-date revenue of $33.1 billion is about $3.6 billion. In May, Anthropic projected $559 million of operating income for Q2 on $10.9 billion of revenue, and its Q1 compute bill ran 71 cents per revenue dollar. [^46,48] If Q2 came in near that projection and Q1 roughly broke even, the year-to-date reading puts Q3 at roughly $3 billion, an 18%-plus quarterly margin. Either reading is profitable. They differ by more than $1 billion.

:::stats
- {label: "Compute per revenue $, 2025", value: "$1.60", note: "7.33 ÷ 4.59, draft S-1"}
- {label: "Compute per revenue $, Q1 2026", value: "$0.71", note: "May investor projections"}
- {label: "Compute per revenue $, Q2 2026 (proj.)", value: "$0.56", note: "May investor projections"}
- {label: "Compute per revenue $, Q3 2026", value: "$0.59", note: "1 ÷ 1.70, FT ratio"}
:::

The most important *improvement* in the story is real and does not depend on any adjustment. Compute cost per revenue dollar fell from about $1.60 in 2025 to about 59 cents in Q3 2026, a 2.7× improvement in the business's core unit economics. [^4,9,48] The counterpoint is in the same series. Q3's 59 cents is slightly *worse* than the 56 cents projected for Q2. That is consistent with Q3 being the first quarter to carry the SpaceX contract at its full $1.25 billion a month (Section 05). Anthropic itself told investors in May that it "likely won't be profitable for the whole year" as compute spending rises. [^48] **Why it matters:** Anthropic is now plausibly profitable before stock pay at the operating level. That is a genuine change from an $8 billion operating loss a year earlier. But "adjusted profitability" in the headline tells you nothing about GAAP net income, which in 2026 will again be hit by fair-value charges on any convertible instruments that are still outstanding as the valuation roughly doubles.

## 05. "Cash flow positive" is not the same as self-funding

Positive cash flow in Q3 is plausible and probably true. But Anthropic's cost base is moving off the cash-flow statement and into contracts. The quarterly cash figure therefore understates the economic cost of the capacity that produced the revenue.

Reuters' reading of the draft prospectus lists at least $518 billion of cloud, compute and infrastructure obligations over roughly a decade. About 80% of that "is non-cancellable or requires payment regardless of usage." [^11] The largest single line is about $161.2 billion of "Broadcom-related equipment lease obligations that are largely non-cancellable." [^11] Leases are the key to the cash-flow question. Equipment acquired under a lease never appears as capital expenditure, so it never reduces free cash flow as most analysts compute it. The cost arrives instead as lease payments, often split between operating and financing lines. Our inference is that a company that leases its accelerators can report positive free cash flow while committing to more hardware spending than its entire revenue history.

:::rank-list
- {label: "Broadcom (equipment leases)", value: "$161.2B", pct: 100, highlight: true}
- {label: "Google (Apr 2026 – Jul 2033)", value: "$111.1B", pct: 69}
- {label: "Amazon (May 2026 – Apr 2036)", value: "$110.0B", pct: 68}
- {label: "SpaceX/xAI Nvidia capacity (through 2029)", value: "$84.5B", pct: 52}
- {label: "Microsoft (Nov 2026 – May 2033)", value: "$31.4B", pct: 19}
- {label: "AMD compute supply", value: ">$20B", pct: 12}
:::

The terms are asymmetric. On the Google contract the draft states, "If our actual spend falls short, we must pay Google the difference," and Amazon carries similar terms. [^11] The Microsoft commitment is "non-cancellable except in the event of Microsoft's uncured material breach." [^11] The one large exit is the SpaceX deal, "largely cancellable with a 90-day notice." [^11] It is also the one hitting the P&L hardest right now. SpaceX's own filing, as reported by Quartz, says "Anthropic will pay $1.25 billion monthly until May 2029," with payments discounted during the May–June ramp. [^26] Anthropic announced that deal on 6 May as giving it "more than 300 megawatts of new capacity (over 220,000 NVIDIA GPUs) within the month." [^25] Q3 is therefore the first full-rate quarter: $3.75 billion, about 22% of Q3 revenue (our arithmetic).

Three mechanisms can make Q3 cash flow positive without Q3 being economically profitable. First, leased equipment bypasses capex, as above. Second, enterprise prepayments and committed-use contracts bring cash in ahead of revenue recognition. No outlet has reported Anthropic's deferred-revenue balance, so this one is unverified. Third, partner capital arrives alongside compute. Amazon invested $5 billion in April with up to $20 billion more to come, and AMD has committed to buy up to $5 billion of stock. [^15,11] Equity inflows are not operating cash flow, but they show who is funding the capacity build. The SEC's rule for non-GAAP *liquidity* measures is strict on this point. Item 10(e) bars excluding "charges or liabilities that required, or will require, cash settlement." [^29] A free-cash-flow figure in the S-1 cannot simply leave lease payments out.

**What would weaken this:** if the S-1 shows free cash flow that remains positive *after* finance-lease principal payments, the "leased cash flow" critique falls away. **Why it matters:** fixed commitments turn a demand miss directly into losses. At roughly $414 billion non-cancellable (80% of $518 billion), the obligations average about $41 billion a year over a decade. That is more than the company's revenue through Q3. [^11]

## 06. Is a $110B year-end run rate arithmetic?

Yes, in a narrow and revealing sense. $110 billion is almost exactly what you get by assuming Q4 grows as fast as Q3 did. The target is therefore not evidence of acceleration. It is the assumption that deceleration stops.

Here is the computation. If Q3's 45% sequential growth was spread evenly as monthly compounding, revenue grew about 13.2% a month (1.45 to the power of one-third). Spreading $16.8 billion across July, August and September on that curve gives September revenue of about $6.31 billion, a $75.7 billion run rate. That matches SemiAnalysis's roughly $74 billion. [^4] Apply the same 45% over Q4 and December revenue is about $9.14 billion, an exit run rate of $109.7 billion. Q4 revenue would be about $24.4 billion, and 2026 recognized revenue about $57.5 billion. All of this is our arithmetic on the reported quarterly figures. [^2] The analysts' $110 billion is, to within rounding, the curve extended one more quarter. The investor expectations in circulation before the meeting were more aggressive still. In September the FT reported investors forecasting $120 billion of annualized revenue at year-end and "almost triple that" by the close of 2027. [^47]

| Q4 scenario | Sep. starting point | Dec. exit run rate | Q4 revenue | 2026 revenue |
|---|---|---|---|---|
| * Q3's 45% growth repeats | $75.7B | ~$110B | ~$24.4B | ~$57.5B |
| Growth halves to ~22% QoQ | $75.7B | ~$92B | ~$20.5B | ~$53.6B |
| Q3 intra-quarter pace (~3%/month) | ~$69B | ~$76B | ~$18.6B | ~$51.7B |
| Flat at the September level | ~$74B | ~$74B | ~$18.5B | ~$51.6B |

The bear case needs no deceleration beyond what Q3 already showed. If the reported $65 billion end-July run rate is taken at face value, Q3's total implies monthly growth of only about 3% across the quarter. [^17,2] Continuing at that pace gives an exit rate in the mid-$70 billions, the bottom rows of the table. Euronews' Bloomberg-sourced line that Anthropic is now "expected to end 2026 below $100 billion" fits that bottom half better than the top. [^5]

Q4 faces specific headwinds and tailwinds:

- **Distillation is going away.** Anthropic told investors that distillation traffic was 5% to 7% of revenue, at least $840 million of Q3 on our arithmetic (5% × $16.8 billion). It also said it had cut that activity back and expected it to weigh on the current quarter. [^3,4] Removing it costs roughly 1 to 1.5 points of Q4 growth before anything else happens.
- **Price cuts landed in the quarter.** Opus 5.5 launched on 22 September at $4/$20 per million tokens against Opus 5's $5/$25, a 20% list-price cut. [^36] Anthropic then "priced Claude Haiku 5.5 about 75% below its predecessor" in October. [^4] Lower prices can raise volume, but they mechanically lower revenue per token.
- **Capacity is the binding constraint, and more is arriving.** The draft prospectus says future demand will be "limited principally by the availability of compute." [^11] From 14 September, Claude Code users' weekly limits fell about 17%. A temporary 50% boost expired that day, partly offset by a permanent 25% increase in the standard limit. [^27] Amazon promised "nearly 1GW in total before the end of the year" of Trainium capacity. [^15] If supply rather than demand set Q3's pace, Q4 capacity additions are the most credible route to re-acceleration.

**What would falsify the "it's just extrapolation" reading:** a disclosed September run rate at or above $90 billion, or Q4 guidance in the S-1, would show genuine acceleration rather than a curve fit. **Why it matters:** the IPO valuation is a multiple of the exit run rate. On a $2 trillion target, the gap between a $75 billion and a $110 billion exit rate is the gap between about 27× and about 18× run-rate revenue (our arithmetic). [^2]

## 07. Revenue quality: concentration, channel and price

Even taken at face value, the $16.8 billion is less diversified and less contractually locked-in than the "recurring revenue" vocabulary implies.

The draft prospectus, as reported by Reuters, says "two customers accounted for nearly one-quarter of its 2025 revenue." It also says many of the largest customers have no long-term contracts and "could cut or stop spending." [^10,9] Ramp's spend data points the same way. Its economist Ara Kharazian found that the top 1% of customers generate 80% of enterprise revenue at both Anthropic and OpenAI, calling it "a level of concentration risk unseen in any other software category we track." [^35] The same PYMNTS report says two coding tools, Cursor and GitHub Copilot, made up "close to a quarter of total revenue." [^35] Both route requests to whichever model they choose, so for them switching away from Claude is a configuration change, not a migration.

Channel and pricing pull in opposite directions on the same customers. Anthropic moved enterprise seats to metered API billing in February. The Register reported that for some clients the seat fee had been "only about 20 percent of their total bill." [^45] That raises revenue per customer. List prices for new models are falling at the same time (Section 06). The net effect on Q4 depends on whether volume growth outruns price cuts, and the leaked figures do not reveal it.

Policy risk is concentrated too. On 25 September the D.C. Circuit ruled 2-1 to uphold the Pentagon's designation of Anthropic as a supply-chain risk, which "bars the military and its contractors from using Anthropic's Claude models." [^39] The ruling is subject to further review, and revenue kept growing through the dispute. But it is the kind of item that becomes a risk factor in the S-1.

**Counterpoint:** concentration is normal for an API platform in its second year of real scale. Ramp found the same top-heavy pattern at OpenAI, so it describes the category, not just Anthropic. [^35] The two-customer share is also a 2025 figure. Full-year revenue then was $4.59 billion, barely a quarter of what Anthropic now books in a single quarter. [^10,2] **Why it matters:** IPO investors pay software multiples for recurring, contracted, diversified revenue. Anthropic's revenue is mostly metered, partly resold, top-heavy, and repriced several times a year.

## 08. What the S-1 has to show, and what will probably change

The privately stated "adjusted profitability" will almost certainly appear in the S-1 in a narrower form, next to GAAP losses at least as prominent and with a line-by-line reconciliation.

Anthropic confidentially submitted a draft S-1 on 1 June 2026 and announced it under Rule 135, which limits such a notice to bare facts. [^33] Before it registers securities, Regulation G does not bind it. Once a non-GAAP measure appears in a registration statement, though, Regulation S-K Item 10(e) applies. Item 10(e) requires the most directly comparable GAAP measure "with equal or greater prominence" plus a quantitative reconciliation. [^29] For 2025 that means an $8.06 billion operating loss and a roughly $42 billion net loss sitting next to any adjusted figure. [^9]

The SEC staff's interpretations narrow what can be adjusted. C&DI 100.01 says a measure can mislead if it excludes "normal, recurring, cash operating expenses necessary to operate a registrant's business." C&DI 100.04 flags "individually tailored" accounting such as presenting revenue net when GAAP requires gross, or the reverse. [^28] Training compute recurs with every model generation and is paid in cash, which fits the C&DI 100.01 example almost word for word. Excluding stock-based compensation, by contrast, is routinely accepted.

:::timeline
- {date: "2011-09", headline: "Groupon removes ACSOI", body: "During SEC review, Groupon's response letter quoted CEO Andrew Mason's email: normal marketing dollars are not something it would remove from ACSOI. [^31]"}
- {date: "2019-03", headline: "Uber drops a tailored adjustment", body: "Staff said the adjustment for divested operations looked like an individually tailored measure. [^32]"}
- {date: "2026-06-01", headline: "Anthropic confidential draft S-1", body: "Rule 135 notice, no financials. [^33]"}
- {date: "2026-09-28", headline: "Draft prospectus leaks via Reuters", body: "2025 revenue $4.59B, operating loss $8.06B, $518B in commitments. [^9,11]"}
- {date: "2026-10-14", headline: "Investor day", body: "Q3 revenue $16.8B, adjusted profit, no run rate or outlook given. [^1,3]"}
- {date: "2026-11-09", headline: "Earliest roadshow (reported)", body: "Public S-1 due about 15 days earlier. [^6,34]"}
:::

Rule 163B makes the investor-day numbers more than marketing. Communications to qualified institutional buyers under the rule are "deemed an offer." [^30] Our reading is that numbers given at the investor day will need to be consistent with what the prospectus eventually shows. **What would weaken this:** if Anthropic's S-1 defines adjusted operating income to exclude only stock pay and a narrow set of non-cash items, and Q3 still shows positive adjusted income, then the private claim survives intact. **Why it matters:** the first public, reconciled set of numbers will arrive two to three weeks before pricing. Anyone pricing the deal now is pricing it off a margin percentage.

## 09. What could break this analysis

This piece's central claims are that $110 billion is an extrapolation and not guidance, that the September "$100 billion pace" reading is incompatible with Q3, and that adjusted profit rests on large exclusions. Each could fail in a specific way.

- **The run rate might measure something different.** If Anthropic's run rate counts contracted minimums, credits or committed-use agreements that recognized revenue does not, the Q3 reconciliation in Section 03 compares unlike quantities. Its arithmetic would then not falsify the "$100 billion pace" report. No published source describes such a definition. [^22,23]
- **Q4 might re-accelerate on supply.** If Q3's slowdown was capacity-driven, as the 17% net reduction in Claude Code weekly limits and the prospectus's "limited principally by the availability of compute" language suggest, then roughly a gigawatt of new Trainium capacity plus Colossus capacity could push Q4 above 45% growth. [^11,15,27] Under that path $110 billion is conservative, not optimistic.
- **The 11% margin might be the conservative reading.** If The Information's year-to-date framing is right, Q3's adjusted operating margin was probably above 18%. The profitability story would then be stronger than headlines suggest, not weaker, especially since the operating measure appears to carry training costs. [^3,46]
- **The figures are all second-hand.** Every number here comes from press accounts of documents or meetings. A restatement in the public S-1, for example Q2 settling at $11.5 billion rather than $11.6 billion, would shift the growth rates by a point or two but not the conclusions. [^5,18]

**Red-team pass:** an adversarial reviewer tried to falsify the three load-bearing claims. It found no contradiction for the $16.8 billion revenue figure. It found only low-severity commentary against the other two.

- **$110 billion.** One aggregator wrote that Anthropic "told institutional investors it expects to reach a $110 billion annual revenue run rate." [^49] Reuters, which sourced attendees directly, attributes the figure to analysts. The Decoder reports that no full-year outlook was given. [^2,3] On Techmeme the only "guiding to $110B" framing was a question posed by an investor. [^7] This article sides with the directly sourced reports, while noting that analysts may have inferred the figure from something executives said.
- **What adjusted operating profit includes.** An August newsletter asserted that the measure leaves out "the amortization of training compute." [^50] That conflicts with the WSJ-sourced definition from May. [^46] If the newsletter is right, adjusted profit is materially weaker than Section 04 credits. The S-1 reconciliation will settle the question.

:::references
- {id: 1, title: "Anthropic's Q3 revenue surges 45% to nearly $17 billion (Reuters)", url: "https://www.investing.com/news/stock-market-news/anthropics-q3-revenue-surges-45-to-nearly-17-billion-4950208", source: "Reuters via Investing.com", date: "2026-10-14"}
- {id: 2, title: "Anthropic tells investors it is profitable as quarterly revenue hits $16.8 billion", url: "https://www.calcalistech.com/ctechnews/article/tgb6eqw4z", source: "Reuters via CTech (Calcalist)", date: "2026-10-15"}
- {id: 3, title: "Anthropic's Q3 revenue hits $16.8B but growth slows ahead of planned November IPO", url: "https://the-decoder.com/anthropics-q3-revenue-hits-16-8b-but-growth-slows-ahead-of-planned-november-ipo/", source: "The Decoder (citing The Information, FT)", date: "2026-10-15"}
- {id: 4, title: "Anthropic's $2 Trillion IPO Pitch Meets a Revenue Growth Slowdown", url: "https://finance.yahoo.com/technology/ai/articles/anthropic-2-trillion-ipo-pitch-045117254.html", source: "BeInCrypto via Yahoo Finance (citing FT)", date: "2026-10-15"}
- {id: 5, title: "Anthropic revenue jumps 46% to $16.8bn as AI firm eyes record $2 trillion IPO valuation", url: "https://www.euronews.com/2026/10/15/anthropic-revenue-jumps-46-to-168bn-as-ai-firm-eyes-record-2-trillion-ipo-valuation", source: "Euronews (citing Bloomberg, FT)", date: "2026-10-15"}
- {id: 6, title: "Anthropic hits $16.8B revenue (Bloomberg relay: IPO timing)", url: "https://finance.yahoo.com/technology/ai/articles/anthropic-hits-16-8b-revenue-234550826.html", source: "Stocktwits via Yahoo Finance (citing Bloomberg)", date: "2026-10-14"}
- {id: 7, title: "Techmeme river, 14 Oct 2026 (Ed Ludlow / Bloomberg margin figures; buy-side reactions)", url: "https://techmeme.com/261014/p56", source: "Techmeme", date: "2026-10-14"}
- {id: 8, title: "Anthropic Q3 revenue $16.8bn ahead of IPO", url: "https://thenextweb.com/news/anthropic-q3-revenue-16-8bn-ipo", source: "The Next Web", date: "2026-10-15"}
- {id: 9, title: "Anthropic lost $42bn in 2025 as revenue grew 12-fold, Reuters reports", url: "https://thenextweb.com/news/anthropic-ipo-prospectus-42bn-loss-518bn-compute", source: "The Next Web (citing Reuters on draft S-1)", date: "2026-09-29"}
- {id: 10, title: "Anthropic's leaked IPO prospectus: losses, growth and a warning", url: "https://fortune.com/2026/09/29/anthropic-leaked-ipo-prospectus-losses-growth-ai-end-humanity/", source: "Fortune (citing Reuters)", date: "2026-09-29"}
- {id: 11, title: "Anthropic plans $518bn AI infrastructure spend, 80% non-cancellable", url: "https://www.businessday.co.za/world/international-companies/2026-09-29-anthropic-plans-518bn-ai-infrastructure-spend-80-non-cancellable/", source: "Reuters via BusinessDay", date: "2026-09-29"}
- {id: 12, title: "Anthropic IPO prospectus lays bare deep dependence on Big Tech partners", url: "https://www.khaleejtimes.com/business/anthropic-ipo-prospectus-lays-bare-deep-dependence-on-big-tech-partners", source: "Reuters via Khaleej Times", date: "2026-09-30"}
- {id: 13, title: "Anthropic raises Series F at $183B post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-series-f-at-usd183b-post-money-valuation", source: "Anthropic", date: "2025-09-02"}
- {id: 14, title: "Anthropic raises $30 billion Series G at $380 billion post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation", source: "Anthropic", date: "2026-02-12"}
- {id: 15, title: "Anthropic and Amazon expand compute partnership", url: "https://www.anthropic.com/news/anthropic-amazon-compute", source: "Anthropic", date: "2026-04-20"}
- {id: 16, title: "Anthropic raises $65 billion Series H", url: "https://www.anthropic.com/news/series-h", source: "Anthropic", date: "2026-05-28"}
- {id: 17, title: "Anthropic's annualized revenue tops $65 billion before IPO", url: "https://news.bgov.com/financial-accounting/anthropic-revenue-run-rate-surpasses-65-billion-ahead-of-ipo", source: "Bloomberg via Bloomberg Government", date: "2026-08-18"}
- {id: 18, title: "Anthropic revenue surges to over $11.5 billion in second quarter", url: "https://news.bgov.com/artificial-intelligence/anthropic-revenue-surges-to-over-11-5-billion-in-second-quarter", source: "Bloomberg via Bloomberg Government", date: "2026-08-14"}
- {id: 19, title: "Anthropic's annualized revenue surges to $65B", url: "https://techcrunch.com/2026/08/17/anthropics-annualized-revenue-surges-to-65b/", source: "TechCrunch (citing Bloomberg, FT)", date: "2026-08-17"}
- {id: 20, title: "Anthropic on track to top $100 billion revenue pace ahead of potential IPO", url: "https://gulfnews.com/world/americas/anthropic-on-track-to-top-100-billion-revenue-pace-ahead-of-potential-ipo-1.500680887", source: "Gulf News (citing NYT)", date: "2026-09-19"}
- {id: 21, title: "Anthropic tops $100 billion revenue pace, report says", url: "https://finance.yahoo.com/technology/ai/articles/anthropic-tops-100-billion-revenue-224001996.html", source: "Axios via Yahoo Finance (citing NYT)", date: "2026-09-19"}
- {id: 22, title: "Anthropic's run-rate revenue", url: "https://simonwillison.net/2026/May/31/anthropic-run-rate/", source: "Simon Willison (citing Reuters Breakingviews)", date: "2026-05-31"}
- {id: 23, title: "Annualized Enron Rate", url: "https://www.wheresyoured.at/annualized-enron-rate/", source: "Ed Zitron, Where's Your Ed At (commentary)", date: "2026-10-13"}
- {id: 24, title: "Anthropic's accounting boost", url: "https://epistrophy.beehiiv.com/p/anthropic-s-accounting-boost", source: "Epistrophy (analyst newsletter)", date: "2026-08-24"}
- {id: 25, title: "Higher limits, powered by SpaceX", url: "https://www.anthropic.com/news/higher-limits-spacex", source: "Anthropic", date: "2026-05-06"}
- {id: 26, title: "Anthropic nears first quarterly profit (SpaceX S-1 payment terms)", url: "https://finance.yahoo.com/sectors/technology/articles/anthropic-nears-first-quarterly-profit-120712552.html", source: "Quartz via Yahoo Finance", date: "2026-05-21"}
- {id: 27, title: "Anthropic is cutting Claude Code's current weekly limits by 17 percent", url: "https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-is-cutting-claude-codes-current-weekly-limits-by-17-percent/", source: "BleepingComputer", date: "2026-08-29"}
- {id: 28, title: "Non-GAAP Financial Measures — Compliance & Disclosure Interpretations", url: "https://www.sec.gov/divisions/corpfin/guidance/nongaapinterp.htm", source: "SEC Division of Corporation Finance", date: "2022-12-13"}
- {id: 29, title: "17 CFR 229.10 — Regulation S-K Item 10(e)", url: "https://www.law.cornell.edu/cfr/text/17/229.10", source: "LII / eCFR"}
- {id: 30, title: "17 CFR 230.163B — Exemption from Section 5(b)(1) and 5(c) for certain communications", url: "https://www.law.cornell.edu/cfr/text/17/230.163B", source: "LII / eCFR"}
- {id: 31, title: "Groupon response letter to SEC staff comments (Form S-1)", url: "https://www.sec.gov/Archives/edgar/data/0001490281/000104746911008103/filename1.htm", source: "SEC EDGAR", date: "2011-09-16"}
- {id: 32, title: "Uber response letter to SEC staff comments (Form S-1)", url: "https://www.sec.gov/Archives/edgar/data/1543151/000095012319002653/filename1.htm", source: "SEC EDGAR", date: "2019-03-12"}
- {id: 33, title: "Anthropic confidentially submits draft registration statement", url: "https://www.anthropic.com/news/confidential-draft-s1-sec", source: "Anthropic", date: "2026-06-01"}
- {id: 34, title: "Anthropic's 14 October investor day nears but its S-1 still isn't public", url: "https://financefeeds.com/anthropics-14-october-investor-day-nears-but-its-s-1-still-isnt-public-the-ipo-timeline-explained/", source: "FinanceFeeds", date: "2026-10-12"}
- {id: 35, title: "OpenAI and Anthropic get 80% of revenue from 1% of customers", url: "https://www.pymnts.com/news/artificial-intelligence/2026/openai-and-anthropic-get-80percent-of-revenue-from-1percent-of-customers/", source: "PYMNTS (citing Ramp)", date: "2026-09-04"}
- {id: 36, title: "Claude Opus 5.5 pricing: what Anthropic's new flagship actually costs", url: "https://www.finout.io/blog/claude-opus-5.5-pricing-2026-what-anthropics-new-flagship-actually-costs", source: "Finout", date: "2026-09-23"}
- {id: 39, title: "Appeals court upholds Pentagon supply-chain-risk label on Anthropic", url: "https://thenextweb.com/news/anthropic-pentagon-supply-chain-risk-appeals-court-ruling", source: "The Next Web", date: "2026-09-25"}
- {id: 41, title: "Anthropic is profitable if you ignore the cost of building it (FT relay)", url: "https://finance.yahoo.com/technology/ai/articles/anthropic-profitable-ignore-cost-building-164202958.html", source: "BeInCrypto via Yahoo Finance (citing FT)", date: "2026-09-16"}
- {id: 43, title: "Anthropic nears $20 billion revenue run rate amid Pentagon feud", url: "https://news.bgov.com/artificial-intelligence/anthropic-nears-20-billion-revenue-run-rate-amid-pentagon-feud", source: "Bloomberg via Bloomberg Government", date: "2026-03-03"}
- {id: 44, title: "Anthropic Q3 revenue rises to $16.8 billion, achieving adjusted profit", url: "https://www.tradingkey.com/analysis/stocks/us-stocks/262217602-anthropic-q3-revenue-rises-16-8-billion-achieving-adjusted-profit-tradingkey", source: "TradingKey (citing Bloomberg)", date: "2026-10-15"}
- {id: 45, title: "Anthropic ejects bundled tokens from enterprise plans", url: "https://www.theregister.com/2026/04/16/anthropic_ejects_bundled_tokens_enterprise/", source: "The Register", date: "2026-04-16"}
- {id: 46, title: "Anthropic on track for first operating profit as revenue surges", url: "https://www.pymnts.com/news/artificial-intelligence/2026/anthropic-on-track-for-first-operating-profit-as-revenue-surges/", source: "PYMNTS (citing WSJ review of investor projections)", date: "2026-05-20"}
- {id: 47, title: "Anthropic tells investors it will be profitable for second straight quarter", url: "https://www.irishtimes.com/business/2026/09/14/anthropic-tells-investors-it-will-be-profitable-for-second-straight-quarter/", source: "Financial Times via The Irish Times", date: "2026-09-14"}
- {id: 48, title: "What's behind Anthropic's surprise turn to profitability", url: "https://www.thedailyupside.com/technology/artificial-intelligence/whats-behind-anthropics-surprise-turn-to-profitability/", source: "The Daily Upside", date: "2026-05-22"}
- {id: 49, title: "Anthropic projects $110B year-end revenue run rate and 85% gross margin", url: "https://huggingnews.com/earnings/anthropic-projects-110b-year-end-revenue-run-rate-and-85percent-gross-ma-6260b4e3", source: "HuggingNews (aggregator; commentary)", date: "2026-10-15"}
- {id: 50, title: "AI Pulse 2026-08-18: Anthropic posts its first profitable quarter, then a credibility test", url: "https://enterprisedna.co/resources/ai-pulse/ai-pulse-2026-08-18-anthropic-posts-its-first-profitable-quarter-then-a-credibil", source: "Enterprise DNA (newsletter; commentary)", date: "2026-08-18"}
- {id: 51, title: "OpenAI CRO tells staff Anthropic inflates run rate by $8 billion", url: "https://www.implicator.ai/openai-cro-tells-staff-anthropic-inflates-run-rate-by-8-billion/", source: "Implicator.ai (citing The Verge)", date: "2026-04-13"}
:::
