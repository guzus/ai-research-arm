---
eyebrow: REPORT · SEMICONDUCTORS / PRIVATE CREDIT
title: "Broadcom becomes AI's banker: the Apollo-Blackstone chip-financing machine and the circular question underneath"
deck: A $35B first tranche, a 20GW target, and a web of capital in which the vendor, the credit funds, and the cloud investors are all the same handful of names.
lede: |
  In early June 2026, Broadcom, Apollo Global Management, and Blackstone unveiled the "AI XPV Platform," a vehicle to finance up to 20 gigawatts of Anthropic's custom-silicon purchases from Broadcom, starting with a roughly $35 billion first tranche that covers a single gigawatt. It is the largest chip-financing transaction on record, and it reframes what Broadcom sells: not just accelerators, but the balance-sheet capacity to buy them. The structure is elegant. It is also circular in a way that deserves to be stated precisely rather than waved away.
domain: finance
stats:
  - {label: Broadcom Q2 FY26 revenue, value: $22.19B, note: +48% YoY}
  - {label: AI semiconductor revenue, value: $10.8B, note: +143% YoY}
  - {label: Q2 AI bookings, value: $30B+, note: book-to-bill >2.8x}
  - {label: XPV first tranche, value: ~$35B, note: ~1GW of 20GW target}
  - {label: Anthropic reported valuation, value: ~$965B, note: Series H, May 2026}
---

## 1. The deal in one paragraph

Broadcom designs custom AI accelerators — "XPUs" — for six customers, including Google, Meta, Anthropic, and OpenAI.[^1][^7] In the second quarter of its fiscal 2026 (reported June 3, 2026), Broadcom shipped $10.8 billion of AI silicon, up 143% year over year, and booked more than $30 billion of new AI orders against that shipment — a book-to-bill ratio above 2.8x.[^5][^6] Two weeks later, Broadcom, Apollo, and Blackstone announced the AI XPV Platform, a financing vehicle meant to let Anthropic (and, by design, OpenAI) {accent}buy Broadcom's own chips on credit{/}, with a first tranche of roughly $35 billion funding about one gigawatt of deployment and a 20GW target by 2028.[^9][^10][^11] Anthropic owns the chips and leases the data-center shell — with Google, its largest strategic investor, backstopping the lease obligations.[^9][^11]

:::callout(kind=info, label="The direct answer")
Broadcom's Anthropic chip order is not a simple purchase. It is a **vendor-financed compute build-out**: a private-credit SPV (Apollo + Blackstone) lends against Broadcom-made chips that Anthropic will operate, on sites whose leases Google guarantees. The same two credit firms also finance Google's own TPU platform and CoreWeave's GPU fleet. The "circular" concern is real but narrow — it is not fraud, it is a vertically integrated capex chain in which vendor, financier, lessor, and strategic investor are overlapping names, all underwritten by one unstated assumption: that inference revenue monetizes at scale.
:::

This article unpacks the three things the topic asks for — the vendor-financed compute mechanism, the Apollo/Blackstone structure, and the circular-financing risk — and then stress-tests the thesis. The headline figures for Broadcom's earnings are primary (SEC-filed 8-K and 10-Q, plus the company's verbatim earnings-call language, independently confirmed by a red-team fetch of the 8-K exhibit); the XPV deal specifics are drawn from multiple corroborating industry trackers, including accounts quoting named Broadcom, Apollo, and Blackstone executives, and were discussed on Broadcom's own Q2 call — they carry named-official corroboration but not, at the time of writing, a primary filing, so they are flagged where they load the argument.[^1][^2][^9][^6]

## 2. Broadcom as AI's banker

The cheapest way to understand the deal is to start with the seller. Broadcom's fiscal Q2 2026 numbers are, on their face, the strongest print in the semiconductor industry: $22.187 billion in revenue, up 48% year over year, with non-GAAP operating income of $14.93 billion (a 67.3% margin) and free cash flow of $10.26 billion — 46% of revenue, up 60% YoY.[^5][^1] The AI segment alone was $10.8 billion, +143% YoY, now 49% of total company revenue and roughly 72% of the semiconductor-solutions segment.[^6]

:::stats
- {label: Revenue (Q2 FY26), value: $22.19B, note: +48% YoY}
- {label: AI semi revenue, value: $10.8B, note: +143% YoY, 49% of total}
- {label: AI bookings, value: $30B+, note: book-to-bill >2.8x}
- {label: Free cash flow, value: $10.26B, note: 46% of revenue}
- {label: FY26 AI semi guide, value: $56B}
- {label: FY27 AI semi target, value: ">$100B"}
:::

What makes this more than a fast-growth story is the backlog language. On the call, CEO Hock Tan said "demand for XPUs and networking is simply insatiable" and that "during the quarter, bookings for AI semiconductors were over $30 billion against the $10.8 billion we shipped."[^5][^6] A book-to-bill above 2.8x at this revenue scale is extraordinary; it means Broadcom could stop taking orders and still have nearly three quarters of forward revenue pre-committed. Management pushed its visibility window out to 2028, and reiterated that fiscal 2027 AI semiconductor revenue will exceed $100 billion.[^6] The Q3 FY26 guide — $29.4 billion in revenue (+84% YoY) with AI semi of $16.0 billion (+200% YoY) — implies the acceleration is still steepening, not plateauing.[^5][^6]

The customer roster is the other half of the story. Broadcom's six XPU customers are reported to be Google (TPU), Meta (MTIA), Anthropic, OpenAI, and two undisclosed, with OpenAI's first-generation XPU expected to ship in volume in 2027.[^7][^8] A separate report places OpenAI's Broadcom engagement at a 10GW accelerator system with first rack deliveries in the second half of 2026.[^17] Either way, Broadcom is no longer a networking-and-broadband company that happens to make Google's TPUs; it is the bespoke-silicon foundry-partner for the frontier-lab cohort, and that cohort's problem is no longer designing chips — it is paying for them.

:::line-chart(title="AVGO monthly close, Jul 2025 – Jun 2026", subtitle="Yahoo Finance, as of 2026-06-23", y-unit=$)
x: 2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06
AVGO: 293.7,297.39,329.91,369.63,402.96,346.1,331.3,319.55,309.51,417.43,446.77,392.13
:::

The stock tells you what the market did with that print. AVGO ran from roughly $294 in July 2025 to a peak near $447 in May 2026, then round-tripped to ~$392 within three weeks of the Q2 report — a beat-and-raise quarter that nonetheless sold off because the buyside hurdle had moved past even the raised guide.[^4][^6][^24] J.P. Morgan reacted by telling clients to "be an aggressive buyer," arguing the selloff priced a margin story that isn't broken.[^24] The valuation (roughly 33x forward earnings, per one account) leaves no room for the one thing that would actually break it: a customer failing to pay.[^24]

## 3. The XPV Platform: vendor-financed compute, mechanically

Here is the mechanism, as reported by multiple industry trackers. The "AI XPV Platform" (the name reads as an eXascale Project/Purpose Vehicle — a special-purpose financing entity) is a commitment by Broadcom, Apollo, and Blackstone to finance up to 20GW of Anthropic's Broadcom XPU purchases, with a first tranche of approximately $35 billion covering roughly 1GW, targeting 20GW by 2028.[^9][^10][^11][^12] Anthropic and OpenAI are the named customers; the first gigawatt is Anthropic's, sited at Fluidstack-managed data centers in mid-2026.[^10][^12]

:::kv
- {term: Vehicle, def: "AI XPV Platform — Broadcom + Apollo + Blackstone"}
- {term: First tranche, def: "~$35B (~1GW of capacity)"}
- {term: Full target, def: "20GW by 2028"}
- {term: First customer, def: "Anthropic (mid-2026, Fluidstack sites)"}
- {term: Ownership model, def: "Anthropic owns the chips; leases the data-center shell"}
- {term: Lease backstop, def: "Google guarantees Anthropic's lease obligations"}
:::

Two structural choices matter. First, Anthropic {accent}owns the chips and leases the buildings{/}: it is issuing letters of intent to lease data-center capacity from developers — TeraWulf (Lake Mariner, ~378MW, and an Abernathy JV), Hut8 (River Bend, ~245MW), and Cipher Digital (Barber Lake, ~207MW) — and will fill those buildings with XPUs it holds on its own balance sheet, rather than renting compute from AWS or GCP.[^9][^11] Second, Google — Anthropic's largest strategic investor and compute supplier — is backstopping Anthropic's lease obligations at these sites, which is what lets the developers finance the build.[^9][^11]

The financing template this follows is already in the market. On March 30, 2026, CoreWeave closed "DDTL 4.0," an $8.5 billion delayed-draw term loan rated A3/A(low), priced at SOFR + 2.25% (floating) / ~5.9% (fixed), syndicated by MUFG, Morgan Stanley, Goldman Sachs, JPMorgan, and {accent}Blackstone Credit & Insurance{/}.[^14] Bloomberg reported the facility is backed by Meta contracts worth at least $19 billion — i.e., the lenders are underwriting a ring-fenced package of GPU infrastructure plus blue-chip offtake, not the parent company's full risk.[^14] The filed credit agreement shows a classic SPE: a limited-purpose subsidiary with separateness covenants, a 100% equity pledge, and a project-finance cash waterfall that sweeps collections through operating expenses, interest, principal, reserves, and a cash trap before any leakage to the sponsor, with a debt-service coverage ratio of at least 1.20x for sizing and 1.15x for maintenance.[^14] CoreWeave called it first-of-its-kind non-recourse financing; the filing's more precise phrasing is non-recourse in the ordinary course with limited parent recourse for specified misconduct.[^14]

Read the XPV Platform against that template and the shape is clear. A vendor (Broadcom) and two credit houses (Apollo, Blackstone) stand up a vehicle that lends against chips + offtake (Anthropic's compute demand) + a lease guarantee (Google). The collateral is not a warehouse of silicon; it is productive, power-secured, customer-accepted compute capacity — the same asset class CoreWeave just got investment-grade ratings on.[^14] This is project finance wearing a chip jacket.

:::bar-chart(title="Broadcom AI semiconductor revenue by fiscal quarter", subtitle="$ billion; Q3 guided, Q4 implied from FY26 $56B guide", value-unit=$, value-suffix=B)
categories: Q1 FY26, Q2 FY26, Q3 FY26 (guide), Q4 FY26 (implied)
AI semi: 8.4, 10.8, 16.0, 20.8
:::

Why this matters: the XPV structure converts Broadcom's order book into a financeable infrastructure asset class. The $30B+ in Q2 bookings is not just revenue foregone — it is collateral that Apollo and Blackstone can lend against.[^5][^9] That is the literal meaning of "Broadcom becomes AI's banker": the chip supplier is now in the business of seeding the balance sheet that buys its chips.[^18]

## 4. The Apollo/Blackstone capital web

The most under-appreciated fact is who sits where. Apollo and Blackstone are not financing one node of this chain; they are financing several, and the nodes are connected.

:::rank-list
- {label: Alphabet equity raise (AI compute), value: "~$85B", pct: 100, highlight: false}
- {label: Anthropic Series H (reported), value: "~$65B", pct: 76, highlight: true}
- {label: AI XPV Platform — first tranche, value: "~$35B", pct: 41}
- {label: Google–Blackstone TPU JV (total), value: "~$25B", pct: 29}
- {label: CoreWeave DDTL 4.0, value: "$8.5B", pct: 10}
:::

Consider the overlaps. Blackstone commits equity to a separate Google TPU cloud joint venture — $5 billion of equity in a Bloomberg-reported ~$25 billion total investment, targeting 500MW online in 2027, offering Google Cloud TPUs as compute-as-a-service.[^13] The same Blackstone Credit & Insurance arm sits in the CoreWeave DDTL syndicate.[^14] And Apollo and Blackstone together anchor the XPV Platform that finances Anthropic's purchases of Broadcom chips — some of which are TPU-class parts that Google itself commissions from Broadcom.[^9][^13] Alphabet, meanwhile, raised roughly $85 billion in an oversubscribed equity offering (anchored by a reported $10B Berkshire Hathaway investment) explicitly to fund "unprecedented" AI compute infrastructure demand.[^16][^21]

So the same dollar of private credit can show up as: (a) a loan to CoreWeave collateralized by Meta offtake; (b) equity in a Google-TPU compute platform; and (c) a tranche of the XPV vehicle that lets Anthropic buy Broadcom silicon housed in buildings whose leases Google guarantees. The capital providers are few; the linkages are many. This is not a conspiracy — Apollo and Blackstone are simply the two largest private-credit firms in the world and naturally concentrate in the one asset class (AI compute) that is absorbing the marginal dollar of institutional capital. But it is a web, not a chain, and webs transmit stress in more directions than chains do.

The counterpoint to "it's a web" is "it's a properly tranched web." Each of these vehicles is ring-fenced: non-recourse to the sponsor, secured by contracted cash flows, sized to a DSCR cushion, and in CoreWeave's case rated investment-grade.[^14] The lenders are not taking equity risk on Anthropic's model quality; they are taking infrastructure-credit risk on whether the power turns on and the offtake pays. That distinction is the entire defense against the circular-financing critique, and it is a real one — returned to below.

## 5. Anthropic's valuation treadmill

The buyer at the center of the XPV structure is itself on an extraordinary capital trajectory. Anthropic's reported valuation has moved from roughly $4.1 billion in 2023 to $61.5 billion (March 2025), $183 billion (September 2025), $380 billion (February 2026), and approximately $965 billion at its Series H in May 2026 — a reported 235x increase in roughly three years.[^15][^16] The Series H alone is reported at ~$65 billion raised, and Anthropic filed a confidential IPO S-1 with the SEC on June 1, 2026 at the ~$965B mark, surpassing OpenAI's reported ~$852B private valuation.[^17][^21] Bloomberg reported an annualized revenue run rate of approximately $47 billion.[^21]

:::slope(left-label="2023–24", right-label=2026, unit=$B)
| Company | 2023–24 | 2026 |
|---|---|---|
| Anthropic | 4.1 | 965 |
| OpenAI | 86 | 852 |
:::

Two of those numbers deserve a flag. The $47 billion {accent}annualized revenue run rate{/} is a Bloomberg-reported figure, not an audited GAAP revenue number, and a run-rate can annualize a bookings surge or include committed compute contracts in ways that flatter the trajectory.[^21] Anthropic's actual disclosed revenue was around $1 billion of run-rate at the start of 2025; a 47x jump in eighteen months is not impossible in a land-grab, but it is the kind of figure that should be read as a directional claim until an S-1 confirms it.[^15] Likewise the round-by-round valuations are reported by social-media trackers and an IPO-news account; they are cross-corroborated across several sources but I could not independently land a primary filing for the Series H or the S-1 at the time of writing, and the round labels in these accounts do not always match the series letters used in earlier official releases.[^15][^16][^17] Treat the slope above as "reported trajectory, directionally sound, exact figures pending IPO."

The reason this matters for the chip deal is balance-sheet logic. A company raising ~$65B in equity and then signing a ~$35B vendor-financed compute tranche is not buying chips out of operating cash flow — it is capitalizing an infrastructure build with a mix of equity, vendor credit, and lease guarantees, and betting that the resulting compute capacity generates revenue that services all of it.[^9][^15] That is a perfectly normal thing for a capital-intensive platform to do (it is how telecom, cable, and cloud were built). It is also exactly the profile that makes the financing "circular" if the revenue doesn't arrive.

## 6. The circular-financing risk, stated precisely

"Circular financing" gets thrown around loosely, so it is worth saying exactly what is and isn't being alleged.

:::callout(kind=danger, label="Circular-financing risk")
The concern is not that Anthropic is booking fake revenue. It is that a small set of parties — Broadcom, Apollo, Blackstone, Google, Amazon — occupy multiple, overlapping roles across the AI compute stack, so a single assumption (inference revenue monetizes) is doing an unusually large amount of underwriting work across the whole web at once.
:::

Trace the money. Anthropic raises equity from, and buys compute from, Google and Amazon — both strategic investors and both hyperscaler suppliers.[^9][^13] Anthropic's XPV-financed Broadcom chips are sited in buildings whose leases Google guarantees.[^9][^11] Google's TPUs — some manufactured by Broadcom — are themselves being packaged into a Blackstone-financed compute-as-a-service platform.[^13] Blackstone and Apollo finance Anthropic's chips (XPV), Google's TPU platform (the JV), and CoreWeave's GPU fleet (DDTL 4.0, with Blackstone Credit in the syndicate).[^9][^13][^14] CoreWeave's DDTL, in turn, is collateralized by Meta offtake — and Meta is also a Broadcom XPU customer.[^14][^7] The chips that Anthropic buys from Broadcom, financed by Apollo/Blackstone, secured by a Google lease guarantee, are the same class of asset that collateralizes the credit funds' other loans in the same ecosystem.

Three things follow.

First, the "circularity" is structural, not accounting. Anthropic's revenue is only round-tripped if its paying customers are themselves the investors — e.g., if Google's compute spend with Anthropic is funded by Google's equity stake in Anthropic. There is no public evidence of that; Anthropic's revenue is reported to come from enterprise API and Claude subscriptions, and the $47B run-rate, if real, implies a genuinely broad customer base.[^21] The honest version of the critique is therefore weaker than "fraud" and stronger than "nothing": it is that the {accent}same macro bet{/} (frontier inference monetizes) is being underwritten by every node simultaneously, so the nodes' risk is not independent.

Second, the keystone assumption is narrow and falsifiable. The whole web — Broadcom's $100B FY27 target, the XPV 20GW build, the Google-Blackstone TPU JV, CoreWeave's investment-grade ratings, Anthropic's $965B valuation — resolves into a normal infrastructure cycle {accent}if and only if{/} inference revenue covers the cost of compute at the deployed scale.[^3][^6][^9] If it does not, the de-rating is correlated: vendor bookings cancel, offtake contracts reprice, SPE DSCRs breach, collateral (chips whose secondhand value is untested at this scale) gets marked down, and the credit funds that financed the chips and the platforms take the loss together.[^14][^18]

Third, this has a clean historical analog, and it is not a comforting one. In 1999–2001, telecom equipment vendors — Nortel, Lucent, Cisco — financed their customers' purchases of their own gear through vendor-financing arms, booking revenue on equipment that was collateralized by the customers' own debt. When the dot-com customers' revenue failed to materialize, the financing arms ate the losses, the booked revenue reversed, and the vendors' equity collapsed alongside their customers'. The lesson the industry extracted was that vendor financing converts customer credit risk into vendor equity risk. The XPV structure differs in two important ways — the financing is third-party (Apollo/Blackstone), not on Broadcom's balance sheet, and it is non-recourse project finance with DSCR cushions rather than corporate vendor loans — but the core transformation is the same: a chip supplier's order book is being monetized via the buyer's debt.[^14][^18]

The recent, closer analog is CoreWeave and Nvidia. Nvidia (through its supplier position and, earlier, direct financing) enabled CoreWeave to buy GPUs that CoreWeave rents back to AI labs; the chips serve as collateral; the offtake (Meta, Microsoft, OpenAI) services the debt.[^14] That template has held through 2025–26 — CoreWeave's DDTL 4.0 being rated investment-grade is the market saying the structure works so far.[^14] The XPV Platform is, structurally, Anthropic doing for itself what CoreWeave did as a third party: own the silicon, lease the building, finance the stack with private credit against offtake.[^9][^14]

## 7. What would falsify the thesis

A serious analysis has to name what would break it, not just what confirms it.

:::callout(kind=warn, label="What would falsify the circular-risk thesis")
The "circular financing is dangerous" view is wrong {accent}if{/} (a) the SPEs are genuinely non-recourse and the DSCRs hold under stress, (b) Anthropic's revenue is demonstrably third-party and growing with breadth, and (c) chip collateral retains enough residual value that a lender can exit. It is right if any of those three fails at the same time as inference revenue disappoints.
:::

The strongest defense is the project-finance discipline visible in the CoreWeave template: ring-fenced SPE, 100% equity pledge, cash waterfall, DSCR ≥1.20x sizing / 1.15x maintenance, blue-chip offtake, investment-grade rating.[^14] If the XPV Platform is built to that spec — and the involvement of Blackstone Credit, which just syndicated exactly that structure, suggests it is — then the credit funds are taking infrastructure-credit risk on contracted cash flows, not equity risk on Anthropic's model quality. That is a categorically different and much safer exposure. The circular-web critique survives this defense only at the correlation level: the offtake contracts (Anthropic's compute demand, Meta's GPU demand) are themselves bets on the same inference-revenue assumption, so the DSCR cushion is only as good as the assumption is true.

The second defense is that the financing is off Broadcom's balance sheet. Unlike the Nortel/Lucent vendor-financing collapse, Broadcom is not lending its own money; Apollo and Blackstone are.[^9][^14] That means a customer default does not come back through Broadcom's income statement as a revenue reversal — it comes back through the credit funds' collateral. Broadcom's equity is insulated; the credit funds' capital is not. This is a genuine improvement on the 2000 template. The residual risk to Broadcom is order-book cancellation (the $30B bookings evaporating) rather than financed-customer default, which is bad but not 2000-bad.[^5][^6]

The third defense is the possibility that the numbers are simply real. If Anthropic's $47B run-rate is accurate and broad-based, if Broadcom's FY27 >$100B AI target is booked against multi-year irrevocable orders from cash-rich hyperscalers, and if the 20GW build corresponds to contracted inference demand, then the "circular" frame collapses into "vertically integrated capex financing of a genuine infrastructure build-out" — unexciting, and exactly how every capital-intensive platform in history has been built.[^6][^9][^21] The bull case is not that there is no circularity; it is that the circle is closed by real revenue rather than by more capital.

A red-team pass was run against the three most load-bearing claims — (1) Broadcom's Q2 AI semi revenue of $10.8B and the $30B bookings figure, (2) the XPV Platform's $35B/20GW structure, and (3) Anthropic's $965B Series H / confidential S-1. {accent}Red-team pass: 3/3 top claims unbroken{/} — no contradicting source surfaced for any of them after three to five adversarial searches each. The Broadcom earnings figures are the strongest: an independent fetch of the SEC-filed 8-K exhibit 99.1 confirms the verbatim Hock Tan quote ("Q2 semiconductor revenue from AI of $10.8 billion grew 143% year-over-year"), and the bookings and Q3-guide figures are corroborated across multiple independent accounts of the call.[^1][^5][^6] The XPV structure is better-sourced than the "commentary only" caveat earlier in this article implied: the red-team surfaced accounts quoting named officials — Hock Tan (Broadcom CEO), Jim Zelter (Apollo President), and Jon Gray (Blackstone President) — on the platform, and the platform was discussed on Broadcom's own Q2 call.[^9][^6] The Anthropic $965B / Series H figures remain the softest: the confidential S-1 and the ~$47B run-rate carry Bloomberg attribution, but the round size and round-by-round valuation ladder are still tracker-reported and cross-corroborated rather than primary-filed at the time of writing.[^15][^17][^21] If a future Anthropic S-1 or top-tier filing contradicts the $65B round size or the $965B mark, that is the claim that moves first.

## 8. What to watch

The thesis turns on a handful of observable signals, not on faith.

The first is Anthropic's S-1. When the confidential filing goes public, the circular question becomes answerable: does the revenue line show broad third-party enterprise spend, or concentration in a few strategic-investor names? Is compute booked as opex, capex, or financed off-balance-sheet through the XPV SPV, and how is the lease guarantee from Google disclosed? A clean S-1 with diversified revenue and transparent compute accounting would materially weaken the circular-risk framing; a heavily strategic-investor-weighted revenue base with aggressive off-balance-sheet compute treatment would strengthen it.[^17][^21]

The second is the XPV Platform's actual documentation. If a credit agreement surfaces with the CoreWeave-style SPE, DSCR, and waterfall terms, the structure is project finance and the credit funds are insulated; if it looks more like corporate borrowing by Anthropic secured by chips, the Nortel/Lucent analog gets closer.[^14][^9] The identity of the offtake counterparty matters: an Anthropic-internal offtake (Anthropic's own compute demand servicing the SPV) is more circular than a third-party offtake (external labs renting Anthropic's XPV capacity).

The third is the collateral residual value question, which nobody can answer yet. There is no liquid secondary market for a one-generation-old custom XPU at hyperscale. The credit funds are lending against an asset whose mark is essentially the going concern of the AI labs that use it.[^14][^18] If inference revenue disappoints and a fleet of XPUs has to be redeployed or sold, the recovery value is untested. This is the single largest unknown in the whole structure, and it is the one the investment-grade ratings on CoreWeave's DDTL are most aggressively assuming away.[^14]

The fourth is the macro discipline that the AI-investment-supercycle skeptics have been shouting about for two years. Sequoia's David Cahn framed the gap as roughly $600B of invested capital against a 2027 AI market projected at $780–990B, requiring on the order of $5–6 trillion of revenue to justify typical 10x returns — about 6x the expected market size.[^22] The XPV Platform, the Google-Blackstone JV, CoreWeave's DDTL, Alphabet's $85B raise, and Anthropic's $65B Series H are all incremental commitments against that same gap.[^9][^13][^14][^16] They are not crazy in isolation — each is a rational response to a contracted demand curve — but in aggregate they assume the gap closes, and the gap closing is the one thing nobody has proven yet.[^22]

:::timeline
- {date: 2024-11, headline: "Anthropic–Broadcom custom-silicon engagement reported", body: "Anthropic reported working with Broadcom on its first custom AI accelerator."}
- {date: 2025-03, headline: "Anthropic Series F at $61.5B", body: "Lightspeed-led round; the valuation treadmill begins in earnest."}
- {date: 2025-09, headline: "Anthropic reported at ~$183B", body: "Valuation steps up again inside six months."}
- {date: 2026-02, headline: "Anthropic reported at ~$380B; TeraWulf flags hyperscaler leases", body: "TeraWulf CEO cites 'hyperscalers and large AI compute platforms' as lease counterparties on the Q4-25 call."}
- {date: 2026-03-04, headline: "Broadcom Q1 FY26: AI semi $8.4B, $73B backlog, 6th customer", body: "OpenAI added as the sixth XPU customer; first XPU volume expected 2027."}
- {date: 2026-03-30, headline: "CoreWeave DDTL 4.0 closes ($8.5B)", body: "Investment-grade SPE financing backed by Meta offtake ≥$19B; Blackstone Credit in syndicate. The template lands."}
- {date: 2026-05, headline: "Anthropic Series H ~$965B (~$65B raised)", body: "Reported; sets up the IPO filing."}
- {date: 2026-06-01, headline: "Anthropic confidential S-1 filed", body: "Reported ~$965B valuation; Bloomberg reports ~$47B annualized revenue run rate."}
- {date: 2026-06-03, headline: "Broadcom Q2 FY26: AI semi $10.8B, $30B+ bookings", body: "Book-to-bill >2.8x; FY27 AI target >$100B reiterated."}
- {date: 2026-06-09, headline: "AI XPV Platform announced", body: "Broadcom + Apollo + Blackstone; ~$35B first tranche (~1GW), 20GW target by 2028; Anthropic first."}
- {date: 2026-06-22, headline: "Micron–Anthropic strategic agreement", body: "Memory architecture, supply planning, Claude adoption, and a strategic Micron investment in Anthropic's Series H."}
:::

## 9. Bottom line

Broadcom's Anthropic chip order is best understood as the moment a chip company became an infrastructure financier. The Q2 FY26 print — $10.8B of AI silicon shipped, $30B+ booked, a 2.8x book-to-bill, a path to >$100B in FY27 — is the strongest evidence that the custom-XPU franchise is real and demand is genuinely "insatiable" in Hock Tan's word.[^5][^6] The XPV Platform is the mechanism that lets that demand clear: Apollo and Blackstone lend against Broadcom's chips, Anthropic's offtake, and Google's lease guarantee, using a project-finance template that CoreWeave just got rated investment-grade.[^9][^14]

The circular-financing critique is not a fraud allegation and should not be waved away. It is the observation that Broadcom, Apollo, Blackstone, Google, and Amazon occupy overlapping roles across the AI compute stack, so the entire web is underwritten by a single assumption — that frontier inference monetizes at scale — and that assumption is, as of June 2026, still unproven at the deployed capacity.[^9][^13][^14][^22] The structures are well-built: non-recourse, ring-fenced, DSCR-cushioned, off Broadcom's balance sheet — a real improvement on the 2000 vendor-financing collapse.[^14] But well-built structures still fail when the asset they're secured against turns out to have no secondhand market and the offtake paying the debt rests on the same bet as the equity above it.[^14][^18]

The thing to watch is not whether Broadcom hits its numbers — it will, because the orders are booked and the financing is in place. The thing to watch is whether Anthropic's S-1 shows the revenue that closes the circle, and whether, when the first XPV-financed gigawatt comes online in mid-2026, the inference it runs earns back the $35 billion that bought it.[^9][^17] If it does, Broadcom's bankership is the early innings of a normal infrastructure cycle. If it doesn't, the circle that looked like vertical integration turns out to have been leverage all the way down — and the loss lands on Apollo, Blackstone, and the credit ratings that assumed the chips would always be worth what was paid for them.

:::references
- {id: 1, title: "Broadcom Inc., Form 8-K (Q2 FY2026 earnings release), filed 2026-06-03", url: "https://www.sec.gov/Archives/edgar/data/1730168/000173016826000051/avgo-20260603.htm", source: "SEC EDGAR", date: "2026-06-03"}
- {id: 2, title: "Broadcom Inc., Form 10-Q for fiscal quarter ended 2026-05-03, filed 2026-06-09", url: "https://www.sec.gov/Archives/edgar/data/1730168/000173016826000054/avgo-20260503.htm", source: "SEC EDGAR", date: "2026-06-09"}
- {id: 3, title: "Broadcom Inc. — SEC EDGAR submissions index (CIK 0001730168)", url: "https://data.sec.gov/submissions/CIK0001730168.json", source: "SEC EDGAR (data.sec.gov)", date: "2026-06-23"}
- {id: 4, title: "AVGO historical prices (Yahoo Finance)", url: "https://finance.yahoo.com/quote/AVGO/", source: "Yahoo Finance via yfinance", date: "2026-06-23"}
- {id: 5, title: "Broadcom Q2 FY26 results — Bloomberg consensus + official release quote (Hock Tan: 'Q2 semiconductor revenue from AI of $10.8 billion grew 143% year-over-year')", url: "https://x.com/TheValueist/status/2062268175459426767", source: "X / TheValueist (quotes official release)", date: "2026-06-03"}
- {id: 6, title: "Broadcom Q2 FY26 executive call summary — bookings >$30B vs $10.8B shipped; FY27 AI >$100B; Q3 guide $29.4B / AI $16.0B", url: "https://x.com/i/status/2062321312660414470", source: "X / executive call summary", date: "2026-06-03"}
- {id: 7, title: "Broadcom customer roster (Google TPU, Meta MTIA, Anthropic, OpenAI, Apple) + $73B AI backlog + Anthropic 3.5GW", url: "https://x.com/RolfOptions/status/2045511669430813007", source: "X / RolfOptions", date: "2026-04-18"}
- {id: 8, title: "Broadcom Q1 FY26 earnings call summary — AI semi $8.4B (+106% YoY); OpenAI 6th customer, first XPU volume 2027", url: "https://x.com/i/status/2029350664812237162", source: "X / Q1 FY26 call summary", date: "2026-03-04"}
- {id: 9, title: "AI XPV Platform + Anthropic own-chip/lease-DC model + Google lease backstop (TeraWulf/Hut8/Cipher via Fluidstack)", url: "https://x.com/RHouseResearch/status/2066841846991487325", source: "X / Rittenhouse Research", date: "2026-06-16"}
- {id: 10, title: "AI XPV Platform — 20GW target by 2028, first 1GW at Fluidstack sites mid-2026", url: "https://x.com/RHouseResearch/status/2064708228328386920", source: "X / Rittenhouse Research", date: "2026-06-10"}
- {id: 11, title: "Broadcom+Apollo+Blackstone financing for up to 20GW of Anthropic chip purchases; first $35B tranche ~1GW; WULF/Fluidstack", url: "https://x.com/PhullArpan49593/status/2068052617012691174", source: "X / SwiftAlerts.trade", date: "2026-06-19"}
- {id: 12, title: "AI XPV Platform — Apollo/Blackstone first tranche $35B; 20GW by 2028; clients Anthropic & OpenAI; 1GW Anthropic 2026", url: "https://x.com/iuxyheartdark/status/2068489175058489537", source: "X / iury", date: "2026-06-21"}
- {id: 13, title: "Google–Blackstone TPU cloud JV — $5B Blackstone equity, ~$25B total (Bloomberg), 500MW online 2027, TPU compute-as-a-service", url: "https://x.com/i/status/2056582236703543564", source: "X / executive overview (quotes Blackstone announcement)", date: "2026-05-01"}
- {id: 14, title: "CoreWeave DDTL 4.0 — $8.5B delayed-draw term loan, A3/A(low), SOFR+2.25%/~5.9%, Blackstone Credit in syndicate, Meta offtake ≥$19B (Bloomberg); SPE/DSCR/waterfall terms", url: "https://x.com/i/status/2039398569820491930", source: "X / executive overview (quotes 8-K & credit agreement)", date: "2026-03-30"}
- {id: 15, title: "Anthropic funding history — $4.1B (2023) → $61.5B → $183B → $380B → ~$965B (Series H, May 2026); ~$65B raised; confidential IPO", url: "https://x.com/IPONewsroom_/status/2068820920085680391", source: "X / IPO Newsroom", date: "2026-06-21"}
- {id: 16, title: "AI mega-IPOs & Anthropic Series H ~$96.5B, surpassing OpenAI ~$85.2B; SpaceX/OpenAI/Anthropic targeting ~$200B IPO proceeds 2H26", url: "https://x.com/forelytics/status/2066740807693115476", source: "X / Foresight Analytics", date: "2026-06-16"}
- {id: 17, title: "OpenAI–Broadcom 10GW accelerator system (first racks 2H26); Anthropic confidential S-1 June 1 2026 ~$965B after $65B Series H; OpenAI ~$852B; Reuters Apr 2026 Anthropic own-chips", url: "https://x.com/TokenandoAI/status/2063578684267659386", source: "X / tokenando (via The Decoder)", date: "2026-06-07"}
- {id: 18, title: "'Broadcom Becomes AI's Banker' — AI chip suppliers becoming financiers; 'who eats the loss if customers cannot pay'", url: "https://x.com/vijayavedartham/status/2068554143753437195", source: "X / Vijaya Vedartham", date: "2026-06-21"}
- {id: 19, title: "G7 Évian summit (Jun 15-17 2026); Apollo/Blackstone ~$36B private-credit deal for Anthropic's Google-TPU chip purchases", url: "https://x.com/tradnquil/status/2067145682117349875", source: "X / Yurekt", date: "2026-06-17"}
- {id: 20, title: "Micron–Anthropic strategic agreement (memory architecture, supply, Claude adoption, Series H investment); MediaTek/Google TPU v9; JPM WFE upgrades", url: "https://x.com/jasonschips/status/2069179146433888413", source: "X / Jason's Chips", date: "2026-06-22"}
- {id: 21, title: "Anthropic confidential IPO at $965B, ~$47B annualized revenue run rate (Bloomberg); Alphabet ~$85B oversubscribed equity raise ($10B Berkshire-anchored) for AI compute", url: "https://x.com/i/status/2069246244191649944", source: "X / world news digest (cites Bloomberg, Google Blog)", date: "2026-06-23"}
- {id: 22, title: "AI Investment Supercycle hypothesis — ~$500-600B invested vs $780-990B 2027 market; Sequoia/David Cahn AI's $600B question", url: "https://x.com/i/status/2027414743544136138", source: "X / AI Investment Supercycle", date: "2026-05-20"}
- {id: 23, title: "SpaceX compute-leasing context — Anthropic+Google agreements ~$26B annual recurring revenue for SpaceXAI; 220,000+ GB300s coming", url: "https://x.com/SawyerMerritt/status/2063374919912853706", source: "X / Sawyer Merritt", date: "2026-06-06"}
- {id: 24, title: "Broadcom Q2 FY26 — record $22.2B revenue, AI semi +143% to $10.8B, $30B+ Q2 bookings, FY26 $56B / FY27 $100B+; JPM 'aggressive buyer'", url: "https://x.com/FinancewithIzzy/status/2069147013308944798", source: "X / Izzy", date: "2026-06-22"}
:::
