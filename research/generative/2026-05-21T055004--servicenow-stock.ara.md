---
eyebrow: "EQUITY RESEARCH · ENTERPRISE SOFTWARE · NYSE: NOW"
title: "ServiceNow After the Split: A 22% Compounder Priced for Decline"
deck: "The market split the stock five ways, then halved it. The real question is whether agentic AI breaks the per-seat model — or whether ServiceNow becomes the layer that governs it."
domain: finance
lede: |
  ServiceNow is the rarest profile in software: a $13B-revenue franchise still compounding north of 20% with a 35% free-cash-flow margin and a 98% renewal rate. It is also, after a first-ever 5-for-1 split in December 2025, a stock that has lost more than half its value from peak — caught in the 2026 "SaaSpocalypse," the market's bet that AI agents will hollow out seat-based software. This report works the numbers from the filings up: what ServiceNow is, why the engine is still strong, whether the AI-disruption fear is real, and what has to be true for the stock to work from here.
stats:
  - {label: "Price (May 20 2026)", value: "$103.30"}
  - {label: "Market cap", value: "~$106B"}
  - {label: "FY2025 revenue", value: "$13.3B", note: "+21% YoY"}
  - {label: "cRPO growth", value: "+22.5%"}
  - {label: "FCF margin", value: "35%"}
  - {label: "From peak", value: "-57%"}
---

## 01. The setup: split five ways, then cut in half

In December 2025 ServiceNow did something it had never done in 13 years as a public company — split its stock — and within months the market did something it rarely does to a 20%-plus grower: cut it roughly in half.

The mechanics first. ServiceNow's board authorized a 5-for-1 split alongside Q3 results on October 29, 2025 [^6]; shareholders ratified it on December 5; and it took effect after the close on December 17, 2025 — the first split in company history [^5]. A pre-split share worth ~$515 became five shares worth ~$103. ==The split changed the share count, not the company== — but it lowered the optical price into a range retail could buy, just as the stock was about to need every buyer it could find.

Because what followed was brutal. On a split-adjusted basis, NOW had run from ~$110 in mid-2021 to a peak above $210 in late 2024, with an intraday all-time high near $240 in January 2025 (roughly $1,200 before the split). By April 2026 it had fallen to the low $80s — a peak-to-trough drawdown of roughly two-thirds — before recovering to ~$103 by May 20, 2026, still about 57% below its high [^32][^37].

:::line-chart(title="ServiceNow (NOW) split-adjusted close", subtitle="Monthly close, Yahoo Finance via yfinance", y-unit=$)
x: 2021-06,2021-09,2021-12,2022-03,2022-06,2022-09,2022-12,2023-03,2023-06,2023-09,2023-12,2024-03,2024-06,2024-09,2024-12,2025-03,2025-06,2025-09,2025-12,2026-03,2026-05
NOW: 109.91,124.45,129.82,111.38,95.1,75.52,77.65,92.94,112.39,111.79,141.3,152.48,157.33,178.88,212.02,159.23,205.62,184.06,153.19,104.55,103.3
:::

:::compare
- {role: HIGHEST, name: "Jan 2025 high", value: "~$240"}
- {role: LOWEST, name: "Apr 2026 low", value: "~$81"}
- {role: SUBJECT, name: "May 20 2026", value: "$103"}
:::

The fall was not company-specific panic so much as a sector verdict. ServiceNow was among the worst-performing large-cap software names in the 2026 "SaaSpocalypse," a violent de-rating that also caught Salesforce, Adobe, Workday, and Atlassian on the fear that AI agents would gut seat-based software [^30]. Yet over the same window the business kept growing more than 20% and throwing off a 35% cash margin — the entire tension this report exists to resolve [^3].

Management did not act like a team that believed the obituary. CEO Bill McDermott bought ~$3M of stock on the open market in February 2026 [^35], and the board added $5B to its buyback authorization in January 2026 [^8]. The setup, then, is a classic value-versus-value-trap standoff: a high-quality compounder trading at a multi-year-low multiple because the market is pricing a structural break the company insists is a tailwind. The rest of this report tests both sides.

## 02. The franchise: a small, sticky enterprise base

ServiceNow is a {accent}near-pure subscription business{/} that has spent two decades turning an IT help-desk tool into a four-pillar workflow platform — and it grows not by adding logos but by selling more to a deliberately small base of the world's largest enterprises. [^1]

:::kv
- {term: Founded, def: "2004, as Glidesoft (Fred Luddy)"}
- {term: HQ, def: "Santa Clara, CA"}
- {term: IPO, def: "June 2012 — NYSE: NOW @ $18.00"}
- {term: Index membership, def: "S&P 500 & S&P 100"}
- {term: CEO, def: "Bill McDermott (since 2019)"}
- {term: Employees, def: "~29,200 (FY2025)"}
- {term: Customers, def: "~8,700"}
- {term: Fiscal year end, def: "Dec 31"}
:::

The company was founded in 2004 as Glidesoft by Fred Luddy, the former CTO of Peregrine Systems, and went public on the NYSE in June 2012 at $18.00 a share under the ticker "NOW." [^28] It joined the S&P 500 on November 21, 2019 — replacing Celgene — and today sits in both the S&P 500 and the elite S&P 100; note that despite its profile as a software bellwether, it is NYSE-listed and {accent}not a member of the Nasdaq-100{/}. [^29] Leadership has changed hands cleanly: Frank Slootman ran the company through its 2011-2017 growth phase and led the IPO, John Donahoe took the chair from 2017-2019, and former SAP chief Bill McDermott has been CEO since late 2019. [^34]

:::timeline
- {date: 2004, headline: "Founded as Glidesoft", body: "Fred Luddy starts the company that becomes ServiceNow."}
- {date: 2012, headline: "NYSE IPO at $18", body: "Lists under ticker NOW; Slootman at the helm."}
- {date: 2017, headline: "Slootman to Donahoe", body: "John Donahoe takes over as CEO."}
- {date: 2019, headline: "McDermott in; joins S&P 500", body: "Ex-SAP CEO arrives; NOW enters the S&P 500 on Nov 21."}
- {date: 2024, headline: "Crosses $10B subscription revenue", body: "Scale milestone for the platform franchise."}
- {date: 2025, headline: "First-ever 5-for-1 split + AI repositioning", body: "Stock splits; company recasts itself as an AI platform."}
:::

The model is the story. In FY2025, subscriptions were {accent}97% of revenue{/} ($12,883M) against just 3% from professional services and other ($395M). [^1][^2] That services line is not a profit center — it runs at roughly {mark}-5% gross margin{/}, a deliberate adoption and customer-success cost designed to drive subscription consumption rather than to make money. [^1][^2] The economics live in the subscription line, which carries an ~80% gross margin and pulls total gross margin to ~78%. [^1] Revenue is recognized ratably over 12-36 month non-cancellable contracts, invoiced annually in advance, which converts signed deals into a {accent}$28.2B remaining-performance-obligation backlog{/} — visibility most software firms would envy. [^1][^2] With ~29,187 full-time employees, that works out to roughly $455K of revenue per head. [^1]

The customer base is striking for how *small* it is: ~8,700 customers, sold almost entirely to large enterprises. [^1] ServiceNow does not chase volume; it lands inside an IT department and expands across the org, which is why net retention and the backlog matter more than logo count. Geographically the franchise is North America-heavy: $8,348M (62.9%) from North America, $3,402M (25.6%) from EMEA, and $1,528M (11.5%) from Asia-Pacific & other — with the US alone at ~59% of total. [^1]

:::donut(center-label="$13.3B")
- {label: North America, value: 62.9}
- {label: EMEA, value: 25.6}
- {label: Asia-Pacific & other, value: 11.5}
:::

What customers buy spans four product areas on one platform: Technology (ITSM/ITOM/Security Ops), CRM & Industry, Core Business (HR/Finance/Legal), and Creator. [^1] Crucially, ServiceNow reports as a {accent}single segment and discloses no product-line revenue{/} — so outsiders cannot see which pillar is actually carrying growth. [^1] The "Now Platform" ships about two named releases a year (recently Washington DC, Xanadu, Yokohama, and Zurich), the cadence by which new capability — increasingly AI — reaches the installed base. [^33]

A note of skepticism on the bull narrative: management says its total addressable market has expanded from $90B to ==$600B==, but that is a CEO-letter figure, not a third-party estimate — and at $13.3B of revenue it implies only ~2% penetration of a number ServiceNow defined itself. [^9] Treat it as ambition, not measurement.

Why this matters: ServiceNow's value rests on a {accent}98%-renewal, ratable, backlog-rich subscription engine{/} sold to a tiny set of sticky enterprises — so the entire investment case hinges on whether that land-and-expand motion keeps compounding, the question the rest of this article tests.

## 03. The financial engine

Strip away the share price and ServiceNow looks less like a falling knife than a textbook compounder: it grew the top line {accent}21%{/} in FY2025 while throwing off a 35% free-cash-flow margin, the kind of growth-plus-profitability pairing that defines best-in-class software.

The headline numbers do the talking. FY2025 total revenue reached $13,278M, up 21% year over year, with subscription revenue — the durable, ratable core — at $12,883M, also +21%. [^2] Demand visibility is even stronger than the P&L: remaining performance obligations (RPO) closed the year at $28.2B (+26.5%), and current RPO, the slice expected to convert within twelve months, hit $12.85B (+25%). [^2] That backlog is growing faster than recognized revenue, which means the bookings engine is still accelerating ahead of the income statement.

:::stats
- {label: Revenue, value: $13.3B, note: +21% YoY}
- {label: Subscription, value: $12.9B, note: +21%}
- {label: cRPO, value: $12.85B, note: +25%}
- {label: RPO, value: $28.2B, note: +26.5%}
- {label: FCF margin, value: 35%}
- {label: Non-GAAP op margin, value: 31%}
:::

The growth is also steady, not spiky. Reported subscription growth has parked in a tight 21-22% band for five straight quarters {sparkline:19,22.5,21.5,21,22} — Q1'25 19%, Q2'25 22.5%, Q3'25 21.5%, Q4'25 21%, and Q1'26 22% — a remarkable consistency at this revenue scale. [^3] cRPO tells the same story of an order book compounding upward.

:::line-chart(title="Current RPO, last six quarters", subtitle="ServiceNow filings", y-unit=$)
x: 2024-Q4,2025-Q1,2025-Q2,2025-Q3,2025-Q4,2026-Q1
cRPO: 10.27,10.31,10.92,11.35,12.85,12.64
:::

Cash conversion is the part that should reassure long-term holders. FY2025 free cash flow was $4,636M — a 35% FCF margin, up from 31.5% the prior year — on operating cash flow of $5,444M (+41%). [^2] Q1 2026 carried the momentum forward: revenue of $3,770M (+22%, +19% constant currency), cRPO of $12.64B (+22.5%), and seasonally peak free cash flow of $1,665M, a 44% margin. [^3][^7] Combine ~22% growth with a 35% FCF margin and the Rule-of-40 score lands around 57 — well clear of the 40 threshold that separates healthy SaaS from the rest. [^3]

The counterpoint lives in the gap between GAAP and non-GAAP. FY2025 GAAP operating income was just $1,824M, a 13.5% margin, against $4,149M (31%) on a non-GAAP basis. [^2] Almost the entire wedge is stock-based compensation, running near 15% of revenue ($1,955M) — real dilution that a cash-margin lens conveniently ignores. [^1] GAAP EPS optics can compress further on timing: Q1 2026 GAAP diluted EPS of $0.45 (net income $469M) was dragged by a $204M tax provision at a ~30% effective rate, versus $0.97 non-GAAP. [^3] Investors who weight dilution heavily will mark the business down accordingly.

Management's own FY2026 guide frames the durability: subscription revenue of $15,735-15,775M (+22-22.5%; +20.5-21% constant currency), a 31.5% non-GAAP operating margin, and a 35% FCF margin held flat at the elevated FY2025 level. [^3]

Why this matters: a 20%-plus grower with a 35% cash margin and a high-50s Rule-of-40 is the rarest profile in software — so whatever is wrong with the stock, it isn't the engine underneath it.

## 04. Land-and-expand: growth from wallet share, not logos

ServiceNow's growth engine is wallet-share expansion inside a small installed base, not logo proliferation — and that expansion is accelerating at the very top end even as the overall pace cools.

The starting point is retention so high it borders on structural lock-in. The subscription renewal rate held at {accent}98%{/} in each of FY2023, FY2024, and FY2025, before dipping to 97% in Q1 2026 — a slip management attributed to folding in newly acquired Moveworks rather than any churn in the core book [^1][^4][^13]. One caveat matters: this rate is *ACV-based* and excludes price and seat upsell, so it understates true net retention — the renewed dollars don't capture the expansion layered on top at each renewal [^1].

That expansion is most visible at the apex of the customer base. The cohort of customers contributing more than $5M in annual contract value has compounded steadily, and the count is the cleanest tier ServiceNow still discloses — it no longer breaks out the legacy $1M/$10M/$20M tiers in its filings [^1].

:::bars
- {label: 2023, value: "420", pct: 67}
- {label: 2024, value: "502", pct: 80}
- {label: 2025, value: "603", pct: 96}
- {label: "Q1 2026", value: "630", pct: 100}
:::

By Q1 2026 there were {accent}630{/} customers above $5M in ACV — roughly +22% YoY — averaging ~$14.9M each [^1][^3][^13]. Critically, the gains skew toward the very top: customers above $20M in ACV grew more than 30% YoY in FY2025, *faster* than the broader $5M+ cohort [^14]. The biggest accounts are getting bigger faster than the merely-large ones.

Deal velocity tells the same story from the flow side rather than the stock side. ServiceNow closed 244 transactions over $1M in net-new ACV in Q4 2025 (up ~40% YoY, including just 9 new logos), then signed 16 deals over $5M in net-new ACV in Q1 2026 (up ~80% YoY, with 5 over $10M) [^2][^3][^13][^14].

:::stats
- {label: "Deals >$1M net-new ACV (Q4'25)", value: "244", note: "~+40% YoY"}
- {label: "Deals >$5M net-new ACV (Q1'26)", value: "16", note: "~+80% YoY"}
- {label: ">$20M ACV customers", value: "+30%", note: "YoY (FY2025)"}
- {label: "New-logo ACV (Q1'26)", value: "+50%", note: "YoY"}
:::

Even the new-logo motion is concentrated and premium: new-logo ACV growth accelerated to over 50% YoY in Q1 2026, the largest new-logo deal ever exceeded $15M, and 17 of the top-20 deals included seven or more products — landing already-expanded [^13]. And a fresh expansion vector has appeared: customers spending more than $1M in ACV on {accent}Now Assist{/} (the AI suite) grew more than 130% YoY in Q1 2026, suggesting AI is becoming an upsell lever in its own right rather than a substitute for the seat-based core [^3].

The counterpoint is concentration. The same dynamic that makes ServiceNow's revenue durable also makes it dependent on a handful of very large relationships — including channel partners.

:::callout(kind=warn, label="Concentration")
A single US federal channel partner / systems integrator represented {accent}12%{/} of total revenue and 19% of accounts receivable in Q1 2026 [^4]. Wallet-share growth at the top end is a strength, but it concentrates both revenue and collection risk in a shrinking set of counterparties.
:::

Why this matters: ServiceNow is not winning by adding customers — it is winning by mining the ones it has, and the mining is intensifying exactly where the dollars are largest. That makes the franchise both more defensible and more exposed to the fortunes of a few apex accounts.

## 05. The crux: agentic AI versus the seat

Strip away the franchise, the cash flows, and the land-and-expand mechanics, and the entire ServiceNow bull/bear argument collapses into a single question: **if AI agents do the work humans used to log in to do, does per-seat SaaS pricing survive?** Everything else in this report is a footnote to that one debate.

The bear case is not vague hand-waving — it is specific, sourced, and argued by serious people. The most quoted version comes from the top of the software industry itself.

:::quote(attr="Satya Nadella, CEO, Microsoft")
Business applications... will probably collapse in the agent era. These [SaaS apps] are essentially CRUD databases with a bunch of business logic — and that business logic is all going to go to the agents. [^17]
:::

If Nadella is right, the value migrates from the application tier (where ServiceNow lives and bills per user) to the agent tier (where Microsoft would prefer it live). The sell-side has begun pricing that risk directly. On April 10, 2026, UBS analyst Karl Keirstead downgraded ServiceNow from Buy to Neutral and cut his target from $170 to $100, citing AI-driven seat-compression — concentrated first in customer-service/CSM, roughly {accent}10% of revenue{/} — layered on top of broader non-AI software-budget pressure; he trimmed his cRPO estimate to exit 2026 at ~16% constant currency, down from 20%. [^16] Bain & Company frames the same mechanism on a ~three-year horizon for routine tasks: ==seat-based pricing may not fit when AI is doing the work, and customers will expect to pay based on outcomes, not log-ons.== [^19] None of this happened in a vacuum — the 2026 "SaaSpocalypse" de-rating hit the whole group (Salesforce, Adobe, Workday, Atlassian), and ServiceNow was among the worst large-cap performers in it. [^30]

:::callout(kind=warn, label="The bear case")
AI agents replace the human seats that SaaS bills against. Per-seat revenue compresses, growth decelerates, and the multiple de-rates. The risk bites first where AI most directly substitutes for a logged-in human — customer-service/CSM, ~10% of revenue — then spreads. UBS now models cRPO exiting 2026 at ~16% cc versus 20%; Bain puts the routine-task transition on a ~3-year clock. [^16][^19]
:::

The marquee real-world anecdote — "AI cuts SaaS seats" — was Klarna dropping Salesforce and Workday during an AI overhaul. But it is worth steelmanning *and then finishing the quote*: CEO Sebastian Siemiatkowski later walked it back, saying {accent}"we did not replace SaaS with an LLM"{/} and that he doubts most companies will follow. [^18] The cleanest piece of bear evidence turned out to be murkier than the headline.

ServiceNow's rebuttal does not deny the mechanism — it reprices around it. CEO Bill McDermott's framing is that agents *expand* the surface area the platform covers, so seat counts can rise even as each seat matters less:

:::quote(attr="Bill McDermott, CEO, ServiceNow, Q1 2026 earnings call")
When you have many more seats because the surface area you cover is 80% greater than what you used to cover, you're going to do fine on seats — but nobody cares about seats. [^13]
:::

The hard number behind the rhetoric: ServiceNow says roughly **50% of net-new business** now comes from a non-seat-based pricing model — tokens, consumption, infrastructure, connectors. [^3][^13] That is the single most important data point in the bull case, and it carries an honest caveat: this is net-*new* business, not the installed base, which remains largely seat-priced and will take years to convert. The transition is real but front-loaded into the marginal deal. Strategically, ServiceNow's answer to "agents eat the application" is to *become the layer that governs the agents* — its "AI Control Tower" — with McDermott arguing a governed platform to run enterprise agents is {accent}"not optional... essential."{/} [^13] The moat underwriting that claim: ~95B workflows run on the platform annually, the system-of-record switching costs are deep, and ServiceNow remains the sole Leader in Gartner's ITSM Magic Quadrant. [^13] If agents need a place to act, get permissioned, and be audited, the system of record is a defensible place for that to happen.

So what would settle it? **The bear thesis is falsified** if seat counts and cRPO keep compounding even as Now Assist deployments scale — i.e., the 50%-non-seat mix climbs *and* total seats hold, proving McDermott's "more seats / nobody cares" math. **The bull thesis is falsified** if CSM and customer-service seats start shrinking in absolute terms, net revenue retention rolls over, or the non-seat 50% stalls instead of bleeding into the installed base — the first hard sign that agents are subtracting from, not adding to, billable surface area.

Why this matters: every section that follows — AI monetization, M&A, valuation, risks, the verdict — is a conditional bet on which way this one question resolves, which is why no honest model of ServiceNow can be built without first taking a side here.

## 06. AI monetization: real dollars, small slice

ServiceNow's agentic-AI story has crossed from narrative into revenue — Now Assist is booking real money — but it remains a thin sliver of the whole, and the metrics management quotes shift framing quarter to quarter, so the discipline is to size it honestly rather than annualize the hype.

The trajectory is genuine. Now Assist — the generative-AI add-on bolted onto existing workflows — was "on pace to exceed" {accent}$500M in ACV{/} through 2025, a subscription-based figure with consumption revenue layering in afterward. [^15] By Q4 2025 net-new ACV had surpassed {accent}$600M and more than doubled year-over-year{/}, with 35 deals over $1M. [^14][^2] In Q1 2026 the cohort of customers spending over $1M in Now Assist ACV grew over {accent}130% YoY{/}. [^3] Adjacent products are scaling alongside it: RaptorDB Pro, ServiceNow's database / data-fabric layer, saw deal volume rise {accent}80% YoY{/} in Q1 2026, including 5 deals over $1M. [^13]

:::timeline
- {date: 2025, headline: "Now Assist on pace past $500M ACV", body: "Subscription-based; consumption revenue layers in afterward."}
- {date: "Q4 2025", headline: ">$600M ACV, more than doubled YoY", body: "35 Now Assist deals over $1M."}
- {date: "Q1 2026", headline: "$1M+ Now Assist customers +130% YoY", body: "RaptorDB Pro deal volume +80% YoY, 5 deals over $1M."}
- {date: 2026, headline: "AI-commitments target raised $1B to $1.5B", body: "A broader basket than Now Assist alone."}
:::

The headline number that travels fastest is the raised target: management lifted its 2026 AI-commitments goal from $1B to {accent}$1.5B{/}, a 50% increase. [^13][^3] But that is not a like-for-like raise of the original Now Assist figure. "AI commitments" is a broader basket — it folds in AI Control Tower, RaptorDB Pro, tokens, and connectors — so the bigger number is partly a redefinition, not pure acceleration of the core add-on. [^13][^3] This is the metric-inconsistency caveat in miniature: ACV vs. commitments vs. net-new vs. consumption get swapped between calls, and an analyst has to keep relabeling the goalposts.

:::quote(attr="Bill McDermott / Gina Mastantuono, ServiceNow, Q4 2025 earnings call")
Now Assist net-new annual contract value surpassed $600 million and more than doubled year over year — with 35 deals above a million dollars in the quarter.
:::

The monetization model is also mutating. Now Assist is sold as "Pro Plus" and "Enterprise Plus" add-ons layered onto existing licenses, priced per seat with a metered allotment of "assists." [^36] But pricing has gone hybrid — subscription plus consumption — and roughly {accent}50% of net-new business{/} now comes from a non-seat-based model built on tokens, infrastructure, and connectors. [^3][^13] That matters because it is the financial expression of the seats-vs-agents debate from the prior section: if agents do the work, the unit of value migrates from human seats to consumed tokens, and ServiceNow is repricing to capture it.

The agentic stack underneath has shipped on schedule. AI Agent Orchestrator and AI Agent Studio reached GA in the Yokohama release (early 2025); the Zurich release added the AI Control Tower; and at Knowledge 2026 ServiceNow launched a conversational front-end, "Otto." [^33] The product is real and progressing — the question is purely one of magnitude.

:::callout(kind=info, label="Size it honestly")
At roughly $600M, Now Assist ACV is still under ~5% of ServiceNow's ~$13.3B revenue. [^15] And ACV is *annualized contract value*, not recognized GAAP revenue — it overstates what hits the income statement today. The eye-catching growth multiples (doubling, +130%, +80%) ride tiny bases, and the "50% non-seat" figure bundles tokens with hardware and connectors and counts net-new bookings only. [^13] Real, monetizing, accelerating — but not yet material to the P&L.
:::

Why this matters: the AI line is the cleanest evidence that ServiceNow can attach new pricing models to its installed base, but at under 5% of revenue it is an option on the future, not the engine of the present — bullish on direction, premature as a thesis pillar until it scales into recognized revenue.

## 07. The M&A spree and the debt pivot

Across 2025 and 2026 ServiceNow committed roughly $12B to acquisitions — capped by the ~$7.75B all-cash purchase of Armis, the largest deal in its history — and in the process flipped from a self-funding cash-and-stock buyer into a debt-financed acquirer whose goodwill is about to clear $10B. [^1][^11]

The cadence tells the story. What began as small data and tooling tuck-ins escalated into platform-scale, security-led purchases in the space of fifteen months.

:::timeline
- {date: 2025-01, headline: "Cuein (undisclosed)", body: "Conversational-AI data to feed agentic workflows."}
- {date: 2025-03, headline: "Moveworks — $2.85B announced", body: "An agentic front door and enterprise search; closed Dec 15 2025."}
- {date: 2025-05, headline: "Logik.io — $506M (closed)", body: "CPQ to round out the sales/order workflow."}
- {date: 2025-07, headline: "data.world", body: "Data catalog; immaterial purchase price."}
- {date: 2026-03, headline: "Veza — ~$1.25B (closed Mar 2)", body: "Identity security; first leg of the security build."}
- {date: 2026-04, headline: "Armis — ~$7.75B all cash (closed Apr 20)", body: "Cyber-exposure management; largest acquisition ever."}
:::

Stack the disclosed prices and the concentration is stark: Armis alone is more than double the next-largest deal, and Veza plus Armis are jointly expected to {accent}more than triple{/} ServiceNow's addressable market for security and risk. [^11]

:::rank-list
- {label: Armis, value: "$7.75B", pct: 100, highlight: true}
- {label: Moveworks, value: "$2.85B", pct: 37}
- {label: Veza, value: "$1.25B", pct: 16}
- {label: Logik.io, value: "$0.5B", pct: 6}
:::

One nuance cuts against the headlines: Moveworks' *booked* consideration came in at ~$2.4B, roughly ==$443M below== the $2.85B announced figure, because the stock portion was struck at $153.04 after ServiceNow's shares de-rated between announcement and close. [^1] The headline number a press release prints and the number that lands on the balance sheet are not the same thing.

The under-covered shift is how ServiceNow paid. Historically its only borrowing was $1.5B of 1.40% notes due 2030, with M&A funded out of cash and stock. [^1] To close Armis it assembled an entirely new debt stack: a $4B term loan, a fresh $3B revolver, $4B of senior notes across five tranches (ranging from 4.25% due 2028 to 6.30% due 2056), plus roughly $2.1B of commercial paper. [^1][^12] That is on the order of $11B of new facilities behind a company that, until recently, prided itself on not needing any.

The mechanical consequence is goodwill. It rose from {accent}$1,273M{/} at year-end 2024 to $3,578M at year-end 2025, and will balloon past $10B once the ~$7.75B Armis price is allocated — mostly to goodwill — in Q2 2026. [^1] More than $10B of intangible carrying value now sits exposed to a future impairment test, and Armis is already modeled as a ~200bps headwind to FY2026 free-cash-flow margin. [^3]

So the debate writes itself. Management's line is that ServiceNow {accent}"doesn't need M&A to buy market traction or growth,"{/} and the CFO has said it "won't need to do any more M&A in security." [^11] Skeptics read it differently: Guggenheim has framed the spree as "less like a disciplined product strategy and more like an attempt to revive slowing top-line growth." [^11]

:::callout(kind=warn, label="Bear read")
A debt-funded $12B buying spree that quadruples goodwill is only accretive if the security+AI platform thesis holds. If organic growth is what's actually decelerating, the same deals become a >$10B impairment risk carried at a higher cost of capital. [^1][^11]
:::

Why this matters: the funding pivot converts ServiceNow's M&A from a balance-sheet luxury into a leveraged bet — investors now have to underwrite both the security strategy *and* the debt that paid for it, and judge whether the spree is platform-building or growth-papering.

## 08. Valuation: cheap, but only if growth holds

After the crash, ServiceNow trades at the lowest multiple of its public life — cheap against its own history, reasonable against its growth, and dangerous only if the growth that justifies it stalls.

At $103.30 (May 20, 2026) the franchise carries a ~$106.5B market cap and ~$101B enterprise value — a valuation that no longer looks like the perennial premium it once commanded. [^20] Trailing GAAP P/E reads a frightening ~61.5x, but that figure is hollowed out by stock-based comp; the cash-economics view is far gentler — forward P/E ~23.8x, PEG ~0.96, and EV/FCF ~22x trailing. [^20] On the sales line the de-rating is starkest: EV/Sales has walked down from 11.6x in 2023 to 9.4x, then 7.8x, then ~7.2x on an LTM basis {sparkline:11.6,9.4,7.8,7.2} — a multi-year low and a roughly 38% compression in three years. [^21] A Rule-of-40 score of ~57 says the underlying engine has not deteriorated nearly as fast as the multiple. [^3]

:::stats
- {label: "EV/Sales (LTM)", value: "7.2x", note: "vs 11.6x in 2023"}
- {label: "Forward P/E", value: "23.8x"}
- {label: "PEG", value: "0.96"}
- {label: "EV/FCF (TTM)", value: "22x"}
- {label: "Rule of 40", value: "57"}
:::

The cleanest read of the de-rating is that it is *sector-wide multiple compression, not a fundamentals break*. [^21][^20] Set ServiceNow against its peer group and it lands in the unglamorous middle of the EV/Sales table — well below the hyper-growth names, comfortably above the mature large-caps it is outgrowing. [^20]

:::rank-list
- {label: "Datadog (DDOG)", value: "19.6x", pct: 100}
- {label: "Snowflake (SNOW)", value: "11.9x", pct: 61}
- {label: "Microsoft (MSFT)", value: "10.0x", pct: 51}
- {label: "ServiceNow (NOW)", value: "7.2x", pct: 37, highlight: true}
- {label: "Adobe (ADBE)", value: "4.2x", pct: 21}
- {label: "Salesforce (CRM)", value: "3.7x", pct: 19}
- {label: "Atlassian (TEAM)", value: "3.6x", pct: 18}
- {label: "Workday (WDAY)", value: "3.1x", pct: 16}
:::

The {accent}growth-adjusted{/} case is where ServiceNow looks genuinely mispriced. It still compounds revenue at ~22% while the mature application-software large-caps — Salesforce, Adobe, Workday — have settled into a ~9-13% band, yet trades at a comparable or even cheaper sales multiple than several of them. [^20][^3] On that basis it is arguably the best growth-adjusted value among large-cap application software: you are paying a Salesforce-like multiple for roughly double the growth.

The Street agrees, mostly. Consensus runs roughly 37 Buy / ~6 Hold / 1 Sell, with a mean target of ~$142 — about 38% above the current ~$103 — bracketed by a $236 high (Bernstein) and an $85 low. [^22][^31] The disagreement is real, not cosmetic: UBS cut to Neutral at a $100 target while Bank of America reinstated Buy at $130. [^16][^25]

:::compare
- {role: LOWEST, name: "UBS (bear)", value: "$85"}
- {role: HIGHEST, name: "Bernstein (bull)", value: "$236"}
- {role: SUBJECT, name: "Consensus", value: "$142"}
:::

Here is the honest caveat. The multiple is only cheap *if growth holds north of ~20%*. [^20] Strip that assumption and the math turns brittle fast: a name decelerating into the low teens does not deserve 7x sales — Workday and Salesforce, at ~3x, are the warning shot. And deceleration is not a tail risk; it is baked into even the bull framework. ServiceNow's own 2030 target of $30B+ subscription revenue implies only a ~17% CAGR from here — management is explicitly underwriting a glide from the low-20s toward the mid-teens. [^24] The valuation prices the company as if it threads that needle without faltering.

Why this matters: at ~7x sales and a sub-1 PEG, the downside is largely sentiment and the upside is re-rating plus compounding — but the entire thesis rests on a single load-bearing assumption, that growth stays above ~20% long enough for the multiple to look cheap in hindsight rather than merely cheap-for-a-reason.

## 09. The risk register beyond AI

Strip away the AI-vs-seats debate, and ServiceNow still presents a stack of concrete, separable risks — and the common thread is that almost all of them sharpen if growth keeps decelerating. The company is not in trouble; it is, however, priced for a future that its own disclosures describe as slower than its past.

| Risk | What it is | Evidence |
|---|---|---|
| Growth deceleration | Q2 2026 cRPO guided to ~19% YoY (down from +22.5% in Q1); the 2030 $30B+ subscription target implies only a ~17% CAGR | [^3][^24] |
| Federal concentration | A single US federal channel partner / systems integrator routes a large slice of government demand to NOW | [^4] |
| SBC dilution | Stock-based comp ~15% of revenue with a ~$3.2B unrecognized RSU overhang | [^1] |
| Goodwill / integration | Goodwill exceeds $10B post-Armis; the deal forced ServiceNow's first major debt raise | [^1][^12] |
| FX | A 10% USD strengthening would have cut FY2025 operating income by $177M | [^1] |
| Valuation | The multiple needs growth to stay near 20% to hold; UBS models cRPO exiting 2026 at ~16% cc | [^16] |

**Deceleration is the master risk.** Q2 2026 cRPO is guided to roughly 19% year-over-year, down from +22.5% in Q1 — and that ~19% even *includes* about 125 basis points of contribution from the Armis acquisition, so the organic deceleration is steeper than the headline. [^3] This is not a one-quarter wobble: the 10-K itself states that the company expects its "revenue growth rate to decline over the long term." [^1] Management's own 2030 ambition of $30B+ in subscription revenue pencils out to only a ~17% CAGR from here, and UBS models cRPO exiting 2026 at roughly 16% cc. [^24][^16] Every other risk in the register is a function of how this curve bends.

:::callout(kind=warn, label="The deceleration tell")
The Q2 2026 cRPO guide of ~19% YoY is down from +22.5% in Q1 — and it leans on ~125bps from Armis, meaning organic growth is decelerating faster than the print suggests. ServiceNow's own 10-K codifies the trend: it expects its "revenue growth rate to decline over the long term." [^3][^1]
:::

**Federal concentration is the most acute single-name exposure.** A "growing portion" of revenue comes from government, and a "substantial majority" of US government sales flow indirectly through partners; the 10-K explicitly names extended federal shutdowns, partisan gridlock, and "changes to government policy" as demand risks. [^1] The sharp end: one US federal channel partner / systems integrator represented {accent}12% of total revenue and 19% of accounts receivable{/} in Q1 2026. [^4] That is genuine concentration risk — a budget impasse or the loss of one reseller relationship could dent both the income statement and collections at once.

**SBC dilution is real but partly self-funded.** Stock-based compensation ran $1,955M, roughly 15% of revenue, and is the single biggest reason GAAP operating margin (13.5%) sits so far below the non-GAAP figure (31%). [^1] There is a ~$3.2B unrecognized RSU overhang still to expense. [^1] The mitigant: buybacks of ~$1.84B in FY2025 hold net diluted-share-count growth to roughly 1%, so shareholders are bleeding cash flow to neutralize dilution rather than watching their stake erode outright. [^1] It is a tax on owners, not a rupture — but it is a recurring one.

The remaining lines compound the picture. Goodwill jumped from $1,273M to $3,578M in 2025 and clears $10B after Armis, layering integration and impairment risk on top of the company's first major debt raise (~$11B of new facilities). [^1][^12] A hypothetical 10% strengthening of the dollar would have trimmed FY2025 operating income by $177M. [^1] And the 10-K flags both key-person dependence on the CEO and the warning that the stock can move "disproportionate to" financial performance — precisely the multiple compression that played out across 2025-2026. [^1]

Why this matters: at ServiceNow's multiple, the valuation only clears if growth holds near 20%, which makes the deceleration line the hinge on which every other risk swings — federal shocks, dilution drag, and goodwill all hurt far more in a 16% world than a 21% one. [^16]

## 10. What would break the thesis — and the verdict

ServiceNow is, on the numbers, a quality compounder priced for decline; whether that is an opportunity or a trap turns on a single, binary question that no model can dodge.

Either agentic AI is a solvent that dissolves seat-based software — in which case a 7x-sales multiple is still too high for a franchise about to decelerate — or it is a tailwind that makes a governed system-of-record more valuable, in which case a 22% grower at a multi-year-low multiple is mispriced. There is little middle ground, which is why the stock now trades with the volatility of a thesis stock rather than the placidity of a $100B compounder [^1].

The bear case is not foolish. ServiceNow's own Q2 2026 cRPO guide of ~19% year-over-year — propped up by ~125bps of Armis — signals the organic line is bending toward the mid-teens [^3]. Its 2030 target of $30B+ subscription revenue concedes a ~17% CAGR [^24]. UBS models cRPO exiting 2026 at ~16% [^16]. If seat compression in customer service is the leading edge of a broader erosion, the multiple has further to fall.

But the bull case has hard evidence too: 50% of net-new business is already non-seat-based, Now Assist ACV more than doubled to over $600M, the >$5M customer cohort keeps compounding, and renewal sits at 98% [^13][^14][^1]. If ServiceNow is the control tower for enterprise agents, AI adds billable surface area rather than subtracting it. McDermott has staked his credibility — and ~$3M of his own cash — on that reading [^35][^26]. An independent adversarial review of this report's three most load-bearing claims — the split and ~57% drawdown, the FY2025 growth-and-margin profile, and the 50%-non-seat figure — turned up no contradicting evidence on any of them.

The debate will be settled by data, not narrative. Four tells to track:

:::kv
- {term: "cRPO growth (cc)", def: "The master gauge. Stabilizing near 20% validates the bull; sliding toward UBS's 16% confirms the bear."}
- {term: "Non-seat mix", def: "The ~50% of net-new on consumption pricing must bleed into the installed base, not stall."}
- {term: "Now Assist scale", def: "AI ACV must climb from under 5% of revenue toward the raised $1.5B commitment to matter to the P&L."}
- {term: "Federal & integration", def: "The 12%-of-revenue federal partner and the >$10B Armis goodwill are the two balance-sheet fault lines."}
:::

The verdict is conditional by construction. At ~$103 — about 7x forward sales, a sub-1 PEG, ~38% below the average analyst target [^22] — ServiceNow offers a quality franchise at the cheapest multiple of its public life, with the explicit risk that "cheapest ever" and "cheap for a reason" can be the same price until growth proves which one it is. For investors who believe enterprises will run their AI agents on top of a system of record rather than around it, the de-rating looks like the opportunity. For those who believe the agents eat the application, it looks like the first leg down. The filings can tell you the business is excellent; only the next four quarters of cRPO can tell you whether the market or the management is right.

:::references
- {id: 1, title: "ServiceNow FY2025 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm", source: "SEC EDGAR", date: "2026-01-29"}
- {id: 2, title: "ServiceNow Q4 & Full-Year 2025 Results (8-K Ex. 99.1)", url: "https://www.sec.gov/Archives/edgar/data/1373715/000137371526000005/erq4fy25.htm", source: "SEC EDGAR", date: "2026-01-28"}
- {id: 3, title: "ServiceNow Q1 2026 Results (8-K Ex. 99.1)", url: "https://www.sec.gov/Archives/edgar/data/1373715/000137371526000054/erq1fy26.htm", source: "SEC EDGAR", date: "2026-04-22"}
- {id: 4, title: "ServiceNow Q1 2026 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/1373715/000137371526000056/now-20260331.htm", source: "SEC EDGAR", date: "2026-04-23"}
- {id: 5, title: "Form 8-K — 5-for-1 split effected; special-meeting vote", url: "https://www.sec.gov/Archives/edgar/data/1373715/000137371525000321/now-20251205.htm", source: "SEC EDGAR", date: "2025-12-05"}
- {id: 6, title: "Form 8-K — board authorizes 5-for-1 stock split", url: "https://www.sec.gov/Archives/edgar/data/1373715/000137371525000305/now-20251029.htm", source: "SEC EDGAR", date: "2025-10-29"}
- {id: 7, title: "ServiceNow Reports First Quarter 2026 Financial Results", url: "https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-Reports-First-Quarter-2026-Financial-Results/default.aspx", source: "ServiceNow IR", date: "2026-04-22"}
- {id: 8, title: "ServiceNow Q4/FY2025 Results; +$5B Buyback Authorization", url: "https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results-Board-of-Directors-Authorizes-Additional-5B-for-Share-Repurchase-Program/default.aspx", source: "ServiceNow IR", date: "2026-01-28"}
- {id: 9, title: "ServiceNow FY2025 Annual Report (TAM / CEO letter)", url: "https://www.sec.gov/Archives/edgar/data/1373715/000137371526000041/now2025ars.pdf", source: "SEC EDGAR", date: "2026-01-29"}
- {id: 10, title: "Form 8-K — ServiceNow to acquire Moveworks for $2.85B", url: "https://www.sec.gov/Archives/edgar/data/1373715/000137371525000096/prmavericks3-10.htm", source: "SEC EDGAR", date: "2025-03-10"}
- {id: 11, title: "ServiceNow completes Armis acquisition", url: "https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-completes-Armis-acquisition-closing-the-gap-between-asset-visibility-and-cyber-risk/default.aspx", source: "ServiceNow IR", date: "2026-04-20"}
- {id: 12, title: "Form 8-K — $4.0B senior notes offering (5 tranches)", url: "https://www.sec.gov/Archives/edgar/data/1373715/000119312526226644/d60522d8k.htm", source: "SEC EDGAR", date: "2026-05-15"}
- {id: 13, title: "ServiceNow Q1 2026 earnings call transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/04/22/servicenow-now-q1-2026-earnings-transcript/", source: "The Motley Fool", date: "2026-04-22"}
- {id: 14, title: "ServiceNow Q4 2025 earnings call transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/01/28/servicenow-now-q4-2025-earnings-call-transcript/", source: "The Motley Fool", date: "2026-01-28"}
- {id: 15, title: "ServiceNow Q3 2025 earnings call transcript", url: "https://www.fool.com/earnings/call-transcripts/2025/10/30/servicenow-now-q3-2025-earnings-call-transcript/", source: "The Motley Fool", date: "2025-10-30"}
- {id: 16, title: "UBS downgrades ServiceNow to Neutral, PT to $100", url: "https://www.cnbc.com/2026/04/10/ubs-downgrades-servicenow-saying-ai-is-a-bigger-threat-than-first-believed.html", source: "CNBC", date: "2026-04-10"}
- {id: 17, title: "SaaS applications will collapse in the AI agent era — Satya Nadella (BG2)", url: "https://officechai.com/stories/saas-applications-will-collapse-in-the-ai-agent-era-microsoft-ceo-satya-nadella/", source: "OfficeChai / BG2 podcast", date: "2024-12-12"}
- {id: 18, title: "Klarna CEO doubts other companies will replace Salesforce with AI", url: "https://techcrunch.com/2025/03/04/klarna-ceo-doubts-that-other-companies-will-replace-salesforce-with-ai/", source: "TechCrunch", date: "2025-03-04"}
- {id: 19, title: "Will agentic AI disrupt SaaS?", url: "https://www.bain.com/insights/will-agentic-ai-disrupt-saas/", source: "Bain & Company", date: "2025-09-23"}
- {id: 20, title: "ServiceNow (NOW) statistics — valuation multiples", url: "https://stockanalysis.com/stocks/now/statistics/", source: "StockAnalysis", date: "2026-05-20"}
- {id: 21, title: "ServiceNow valuation multiples (historical EV/Revenue)", url: "https://multiples.vc/public-comps/servicenow-valuation-multiples", source: "Multiples.vc", date: "2026-05-21"}
- {id: 22, title: "ServiceNow (NOW) analyst forecast & consensus target", url: "https://www.marketbeat.com/stocks/NYSE/NOW/forecast/", source: "MarketBeat", date: "2026-05-19"}
- {id: 23, title: "ServiceNow (NOW) market cap & enterprise value", url: "https://stockanalysis.com/stocks/now/market-cap/", source: "StockAnalysis", date: "2026-05-20"}
- {id: 24, title: "ServiceNow sets $30B subscription target by 2030", url: "https://fortune.com/2026/05/06/servicenow-30-billion-revenue-not-crazy-why/", source: "Fortune", date: "2026-05-06"}
- {id: 25, title: "Bank of America reinstates ServiceNow at Buy, $130 PT", url: "https://sherwood.news/markets/servicenow-rises-after-bank-of-america-analysts-reinstate-buy-with-130-price-target/", source: "Sherwood News", date: "2026-05-19"}
- {id: 26, title: "ServiceNow CEO Bill McDermott on the SaaSpocalypse", url: "https://fortune.com/2026/05/08/servicenow-ceo-bill-mcdermott/", source: "Fortune", date: "2026-05-08"}
- {id: 27, title: "ServiceNow got hammered by Wall Street", url: "https://finance.yahoo.com/markets/stocks/articles/servicenow-got-hammered-wall-street-164128511.html", source: "Yahoo Finance", date: "2026-04-25"}
- {id: 28, title: "ServiceNow IPO final prospectus (Form 424B4)", url: "https://www.sec.gov/Archives/edgar/data/0001373715/000119312512289628/d301887d424b4.htm", source: "SEC EDGAR", date: "2012-06-29"}
- {id: 29, title: "ServiceNow to join the S&P 500", url: "https://press.spglobal.com/2019-11-19-Thermo-Fisher-Scientific-Set-to-Join-S-P-100-ServiceNow-to-Join-S-P-500", source: "S&P Dow Jones Indices", date: "2019-11-19"}
- {id: 30, title: "Worst-performing software stock of 2026: ADBE, CRM, or NOW", url: "https://247wallst.com/investing/2026/04/27/which-software-stock-has-been-the-worst-performer-in-2026-adobe-salesforce-or-servicenow/", source: "24/7 Wall St.", date: "2026-04-27"}
- {id: 31, title: "Bernstein hikes ServiceNow price target to $236", url: "https://247wallst.com/investing/2026/05/06/bernstein-hikes-servicenow-price-target-to-236-was-the-analyst-day-a-win-or-a-trap/", source: "24/7 Wall St.", date: "2026-05-06"}
- {id: 32, title: "ServiceNow (NOW) split-adjusted price history", url: "https://finance.yahoo.com/quote/NOW/history", source: "Yahoo Finance (via yfinance)", date: "2026-05-21"}
- {id: 33, title: "ServiceNow Zurich release introduces agentic AI / AI Control Tower", url: "https://www.cio.com/article/4054799/servicenow-zurich-release-introduces-agentic-ai-to-the-platform.html", source: "CIO", date: "2025-09-10"}
- {id: 34, title: "ServiceNow 2026 proxy statement (DEF 14A)", url: "https://www.sec.gov/Archives/edgar/data/1373715/000137371526000039/now-20260406.htm", source: "SEC EDGAR", date: "2026-04-06"}
- {id: 35, title: "Form 4 — W. McDermott open-market purchase (~$3M)", url: "https://www.sec.gov/Archives/edgar/data/1334944/000133494426000020/0001334944-26-000020.txt", source: "SEC EDGAR", date: "2026-02-27"}
- {id: 36, title: "ServiceNow launches Now Assist across the Now Platform (pricing bundles)", url: "https://www.constellationr.com/blog-news/insights/servicenow-launches-now-assist-across-now-platform-pricing-bundles", source: "Constellation Research", date: "2025-04-01"}
- {id: 37, title: "ServiceNow (NOW) price & returns summary", url: "https://www.financecharts.com/stocks/NOW/summary/price", source: "FinanceCharts", date: "2026-05-20"}
:::
