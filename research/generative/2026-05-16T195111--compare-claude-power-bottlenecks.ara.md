---
eyebrow: REPORT · AI INFRASTRUCTURE
title: The megawatt is the model
deck: 2026's binding AI constraint is not the transformer block — it is the transformer.
lede: |
  In Q1 2026 the four AI hyperscalers committed roughly $700B of combined annual capex. In the same quarter GE Vernova's gas-turbine order book crossed 100 GW with five-year delivery slots, PJM's December capacity auction failed to procure target capacity for the first time in its history, and FERC directed the largest US grid operator to invent three new transmission service categories for AI data centers. The bottleneck has stopped being a forecast. It is a printed earnings release, a docketed tariff filing, and a county zoning decision — and the people responsible for the grid say so on the record.
stats:
  - {label: "Hyperscaler 2026 capex", value: "~$700B", note: "+50% YoY"}
  - {label: "PJM 2027/28 BRA cleared", value: "$333.44/MW-d", note: "First-ever shortfall"}
  - {label: "GE Vernova GT backlog", value: "100 GW", note: "→ 110 GW YE 2026"}
  - {label: "US interconnection queue", value: "2,290 GW", note: "55-mo median wait"}
---

## 01. The capex print is the floor

In Q1 2026 the four AI hyperscalers committed to roughly $700B of combined annual capex — a step-change that has already locked in 8+ years of grid stress before a single new transformer arrives.

:::stats
- {label: "Amazon TTM capex (Q1 2026)", value: "$151.0B", note: "Q1 alone $44.2B"}
- {label: "Microsoft 9M FY26 capex", value: "$80.1B", note: "+69% YoY; ~$190B FY26 run-rate"}
- {label: "Alphabet Q1 2026 capex", value: "$35.7B", note: "TTM $109.9B; >2x YoY"}
- {label: "Meta FY26 capex guide", value: "$125-145B", note: "raised from $115-135B"}
:::

The April 29 8-Ks read like coordinated capitulation to a single conclusion. Alphabet printed $35.674B of Q1 2026 capex — more than double the year-ago quarter — and dragged trailing-twelve-month spend to $109.924B.[^1] Microsoft spent $30.876B in its fiscal Q3 alone (up 84% YoY), bringing nine-month FY26 capex to $80.146B and putting the company on a ~$190B annual trajectory.[^2] Meta nudged its 2026 envelope to $125-145B — the high end now exceeds Alphabet's entire 2025 program.[^3] Amazon was the largest single check: $44.203B in Q1 and $151.003B TTM, with management volunteering that the spend "primarily reflects investments in artificial intelligence."[^4]

What separates this print from prior capex cycles is that the order book on the demand side now matches. Amazon disclosed an OpenAI agreement for approximately {accent}2 GW of Trainium capacity{/} ramping in 2027, with the Anthropic relationship sized "up to 5 GW."[^5] Microsoft's commercial remaining performance obligation hit $627B, up 99% YoY, against an AI business now running at a $37B annualized rate (+123%).[^6] These are not pipeline indications — they are contracted load that has to be served somewhere on the North American grid.

The forecasting community has finally caught up. LBNL's December 2024 report put US data-center electricity on track for 325-580 TWh by 2028 — 6.7% to 12.0% of total US consumption — versus 176 TWh as recently as 2023.[^7]

:::line-chart(title="US data-center electricity, TWh", subtitle="LBNL 2024 report low/high scenarios", y-unit=TWh)
x: 2023,2024,2025,2026,2027,2028
LBNL low: 176,206,236,266,296,325
LBNL high: 176,257,338,419,499,580
:::

The IEA's "Energy and AI" frames the same wave globally: a Base case of ~945 TWh of data-center electricity by 2030 — about 3% of world power — bounded by a 670 TWh Headwinds case and a 1,260 TWh Lift-Off case.[^8]

:::compare
- {role: LOWEST, name: "IEA Headwinds", value: "670", unit: TWh}
- {role: HIGHEST, name: "IEA Lift-Off", value: "1,260", unit: TWh}
- {role: SUBJECT, name: "IEA Base", value: "945", unit: TWh}
:::

EPRI, working only on the US grid, lands in the same envelope: data centers consuming 9-17% of US electricity by 2030 under annual-growth scenarios spanning 3.7% to 15%.[^9]

The counterpoint is real and worth naming. {accent}Capex is not kilowatt-hours, and orders are not deliveries.{/} A $44B quarter at AWS includes warehouses, last-mile vans, and fulfillment-network gear alongside GPUs; the LBNL low-to-high range is a factor of 1.8x for a reason, and the IEA's spread is wider still. Trainium "GW commitments" are contractual ceilings, not metered draw. If perf-per-watt improves faster than Hopper-to-Blackwell did, or if utilization disappoints, the high cases collapse toward the low ones.

But the asymmetry runs the other way for grid planners. Transformers, switchgear, and 500 kV transmission have 4-7 year lead times; the capex commitments in front of us are already 18 months ahead of the iron. Even at the LBNL low-case, the US grid has to find another ~150 TWh of dispatchable supply by 2028 — roughly the annual generation of fifteen Vogtle-3 reactors. The capex print is not the ceiling on grid stress; it is the floor, and every section that follows is about how the physical system fails to keep up.

## 02. The capacity market has already cracked

PJM's capacity construct — the auction that is supposed to price scarcity three years forward and call new generation onto the system — has failed three years running, and each failure has been worse than the last.

:::line-chart(title="PJM Base Residual Auction clearing price", subtitle="$/MW-day, RTO-wide cleared price by delivery year", y-unit=$)
x: 2024/25,2025/26,2026/27,2027/28
BRA: 28.92,269.92,329.17,333.44
:::

The 2025/26 auction, cleared in July 2024, jumped to $269.92/MW-day RTO-wide from $28.92 the year before — an 833% increase that lifted total capacity costs from $2.2B to $14.7B in a single procurement cycle.[^10] Constrained Mid-Atlantic zones cleared higher still: $466.35/MW-day at BGE and $444.26 at Dominion.[^10]

:::compare
- {role: LOWEST, name: "Rest of RTO", value: "$269.92"}
- {role: HIGHEST, name: "BGE zone", value: "$466.35"}
- {role: SUBJECT, name: "Dominion zone", value: "$444.26"}
:::

The 2026/27 auction never got a real clearing price. After the prior result triggered double-digit residential bill increases — New Jersey utilities filed for hikes of 17.23% to 20.20% effective June 1, 2025, adding roughly $23/month to a JCP&L bill[^16] — five Mid-Atlantic governors (PA, MD, NJ, DE, IL) settled with PJM in January 2025 on a temporary $325/MW-day price cap and $175/MW-day floor.[^17] The 2026/27 BRA duly cleared at the cap-equivalent $329.17/MW-day across every LDA; PJM's own simulation showed it would have cleared at $388.57 without the cap.[^11] The market didn't soften — politics simply moved the ceiling.

Then in December 2025 the auction broke in a new way. The 2027/28 BRA cleared at the renewed cap of $333.44/MW-day and, for the first time in the auction's history, failed to procure the target capacity — a 6,516.6 MW UCAP shortfall that pushed the reserve margin down to 14.4% against a 20% IRM target.[^12] An auction at the price cap that *still* under-procures is not a price signal; it is a flashing instrument with no actuator behind it.

:::donut(center-label="$16.4B")
- {label: "Data center load", value: 40}
- {label: "Other load growth", value: 60}
:::

PJM's Independent Market Monitor attributes roughly 40% — about $6.5B — of the 2027/28 BRA's $16.4B capacity cost to data center load, and ~45% of the $47.2B transacted across the last three auctions to the same demand.[^13] The IMM's allocation methodology is contested — load-serving entities argue the counterfactual is sensitive to assumptions about retirements, import limits, and demand-response participation — but the directional message is uncontroversial: this is a hyperscaler-driven price event being socialized across residential ratepayers.

The Virginia case makes the inversion concrete. Dominion Energy reported ~48.5 GW of data-center capacity under contract in December 2025, up from ~16.5 GW in July 2023, against a system all-time peak of 24.7 GW set in January 2025 — contracted data-center load alone is now nearly double the entire historical system peak, with another ~70 GW in the connection queue.[^14] The state's own Joint Legislative Audit and Review Commission concluded that unconstrained data-center growth could lift Virginia electricity use +183% by 2040, requiring +150% in-state generation, +150% imports, and +40% transmission build.[^15] A caveat worth carrying: "contracted" GW includes early-stage Electrical Service Agreements that historically convert at well under 100%, and queue figures are notoriously inflated by speculative duplicates. The order-of-magnitude gap survives any reasonable haircut.

Federal regulators have now effectively conceded the auction can't carry the load alone. On December 18, 2025 FERC directed PJM to file tariff revisions creating three new service options for co-located large loads — Network Integration Transmission Service, Firm Contract Demand, and Non-Firm Contract Demand — with compliance filings due January 20 and February 16, 2026.[^18] Read plainly, FERC is routing hyperscaler interconnections around the capacity construct rather than through it.

Residential electricity bills are now the political third rail of the AI build-out. The capacity market was designed to convert scarcity into investment signals; in PJM it is now converting scarcity into ratepayer revolt, governor-imposed price caps, and the first procurement shortfall in its history. Every other bottleneck in this report — queues, iron, gas turbines, nuclear — sits downstream of a market mechanism that the operator, the states, and FERC have all stopped trusting.

## 03. The queue is 2,290 GW, and almost nothing moves

The US interconnection queue now holds roughly seven times the entire installed US generating fleet, yet the median project that filed in 2020 will not energize until 2027 — and the country built fewer than 900 miles of new high-voltage transmission in 2024. The bottleneck strangling AI's power buildout is administrative, not physical.

:::stats
- {label: "Active US queue", value: "2,290 GW", note: "1,400 GW gen + 890 GW storage"}
- {label: "Median wait to COD", value: "55 mo.", note: "for projects built in 2024"}
- {label: "345 kV+ built in 2024", value: "322 mi.", note: "third-slowest year in 15"}
- {label: "PJM connected in 2025", value: "2.1 GW", note: "of a 220 GW queue"}
:::

Berkeley Lab's *Queued Up 2025* counts roughly 2,290 GW of active capacity sitting in US interconnection queues at end-2024 — about 1,400 GW of generation and 890 GW of storage, with gas requests jumping 72% year-over-year to 136 GW.[^19] The queue actually shrank 12% on the year, but the shrinkage is a red flag, not progress: developers are pulling out, not plugging in. Only {accent}19%{/} of projects that requested interconnection between 2000 and 2019 ever reached commercial operation.[^20]

The wait time has nearly tripled in 16 years. A project entering the queue in 2008 waited a median of 22 months to energize; by 2015 that had stretched to 36 months; for projects built in 2024 the median was 55 months.[^20]

:::compare
- {role: LOWEST, name: "2008 cohort", value: "22 mo."}
- {role: HIGHEST, name: "2024 cohort", value: "55 mo."}
- {role: SUBJECT, name: "2015 cohort", value: "36 mo."}
:::

Even if developers cleared the queue tomorrow, the wires would not be there to carry the electrons. The US completed just 322 miles of 345 kV-or-higher transmission in 2024 — the third-slowest year in a decade and a half — against an implied need of roughly {accent}5,000 miles per year{/} from DOE's 2024 National Transmission Planning Study.[^21] And the long-lead equipment needed to build any of it is in deep backlog.

:::rank-list
- {label: "HV circuit breakers", value: "151 wks", pct: 100}
- {label: "Generator step-up transformers", value: "144 wks", pct: 95}
- {label: "Large power transformers", value: "128 wks", pct: 85}
- {label: "Gas turbines (frame, foreshadowed §05)", value: "~260 wks", pct: 100, highlight: true}
:::

Wood Mackenzie's Q2 2025 survey pegs large power transformer lead times at 128 weeks and generator step-up unit lead times at 144 weeks, with a projected 30% supply deficit in 2025.[^22] High-voltage circuit breakers crossed 151 weeks — roughly three years, double the pre-pandemic norm — by end-2023.[^23]

NERC's 2025 Long-Term Reliability Assessment makes the consequence explicit: MISO and SPP are now rated High Risk and PJM Elevated, with 13 of 23 reliability areas flagged elevated or high risk. The 10-year summer peak forecast jumped {accent}+224 GW{/} — 69% higher than the +132 GW in the 2024 LTRA — and the winter forecast added +245 GW on top.[^24] The demand curve moved by more than a third in a single revision cycle; the build rate did not.

PJM is the canonical case. The largest grid operator in North America {accent}connected just 2.1 GW of new resources in all of 2025{/} — 2,033 MW of solar, 55 MW of wind, and 29 MW of coal — while its queue holds 220 GW: 106 GW of gas, 67 GW of storage, 18 GW of nuclear, 15 GW of solar, 9 GW of solar+storage, and 5 GW of wind.[^25] That is a 100-to-1 ratio of paper to steel. Hyperscaler load growth requests in PJM measure in the tens of gigawatts; the actual delivered capacity is a rounding error.

:::callout(kind=success, label=Counterpoint)
Reform is not impossible. CAISO's Cluster 15 process used a scored prioritization filter — 30% commercial readiness, 35% project viability, 35% system need — to compress 347 GW across 541 applications down to {accent}68 GW across 145 projects{/} that actually got studied.[^26] FERC Order 2023A is pushing every ISO toward the same cluster-study posture. And the headline 2,290 GW number is itself partly inflated: storage now accounts for ≥1/3 of the queue, and many projects file in multiple ISOs simultaneously.[^19]
:::

Even granting all of that, the arithmetic does not close. CAISO filtered the queue but did not build the lines. PJM's reform timeline runs to 2027. Transformer factories take three years to commission. The 55-month median wait is what 2026 looks like — 2027 and 2028 cohorts will be worse before they are better.

This matters because the queue is the single biggest moat protecting incumbent generators. Every month a 1 GW gas plant sits in study is a month the existing fleet collects scarcity rents — which is exactly the dynamic the next section traces inside ERCOT, where the rules are bending faster than anywhere else in North America.

## 04. ERCOT bends the rules, and Texas builds

ERCOT inherited a different regulatory operating system — no capacity market, no FERC jurisdiction, no balanced-bill politics — and used that latitude in 2025-26 to invent a utility-grade legal class for AI loads while absorbing the country's most ambitious gas-only AI campus, running in production the experiment the rest of the country can only debate.

The forecast itself is the first tell that something has broken. ERCOT's preliminary long-term load study now spans a range no other ISO would publish under its own letterhead: a 2030 peak of ~138 GW on the "adjusted" path that haircuts speculative large-flexible-load requests, versus ~208 GW unadjusted, against a stated-interest pipeline CEO Pablo Vegas pegs at roughly 360 GW.[^27] The spread between adjusted and stated-interest — more than 2x — is the entire AI-power debate compressed into one document.

:::compare
- {role: LOWEST, name: "2030 adjusted", value: "138 GW"}
- {role: SUBJECT, name: "2030 unadjusted", value: "208 GW"}
- {role: HIGHEST, name: "Vegas stated interest", value: "360 GW"}
:::

The interconnection queue is where the abstraction becomes a process problem. ERCOT's large-load queue grew roughly 269-300% in one year, reaching 233 GW entering 2026, with about 77% of it data centers.[^28] ERCOT VP Bill Hobbs said the quiet part out loud: {accent}"We have outgrown the process that was established for reviewing these large loads."{/}[^28] That admission — from the operator itself, not a critic — is what made Senate Bill 6 politically inevitable.

SB 6, effective 2025-06-20, did three things no other US grid statute has done in combination: it created a new "large load" regulatory class at the ≥75 MW threshold, granted ERCOT direct curtailment authority over any large load interconnected after 2025-12-31, and imposed a $100k minimum screening-study fee to filter speculative queue entries.[^29] The curtailment hook is the load-side analog of a demand-response obligation, but compulsory and ISO-administered — a tool PJM and MISO would need years of stakeholder process even to draft.

:::stats
- {label: "SB 6 threshold", value: "75 MW", note: "ERCOT-curtailable"}
- {label: "ERCOT large-load queue", value: "233 GW", note: "+300% YoY"}
- {label: "Stargate Abilene", value: "1.2 GW", note: "Mid-2026 COD"}
- {label: "Crusoe gas turbines", value: "29 units", note: "~1 GW aeroderivative"}
:::

The generation side is moving with similar velocity but a different mix than the orthodoxy expects. The ERCOT generation queue now totals 458 GW, of which solar+storage is 75% (343 GW), gas 14% (64 GW, up from 12.5 GW in March 2023 — a roughly 400% jump in two years), and wind 11% (48 GW).[^30] Gas has surpassed wind in the Texas queue for the first time. The reason is delivery speed: Stargate Abilene, the most-advanced US Stargate site, is already 0.3 GW operational and scaling to 1.2 GW across eight buildings by mid-2026, anchoring a roughly 4.4 GW Texas Stargate footprint across Abilene, Shackelford, and Milam counties.[^31] Crusoe ordered 29 GE Vernova LM2500XPRESS aeroderivative gas turbines (~35 MW each, ~1 GW combined) across two tranches in December 2024 and June 2025.[^32] The LM2500XPRESS is explicitly an efficiency-for-speed trade — aeroderivatives heat-rate worse than F-class combined cycles, but they ship in months, not years.

:::donut(center-label="458 GW")
- {label: "Solar+storage", value: 75}
- {label: "Gas", value: 14}
- {label: "Wind", value: 11}
:::

The cautionary tale runs ninety miles east. xAI's Colossus campus is operating 46+ unpermitted gas turbines at Southaven, Mississippi — across the state line from Memphis — against only ~247 MW of permitted capacity at the Memphis site, with Solaris targeting 1.1+ GW of behind-the-meter gas for xAI by Q2 2027.[^33] The Memphis playbook is the limit case of "build first, permit later," and it is already drawing NAAQS scrutiny and lawsuits. SB 6's $100k fee and curtailment regime are, in part, Texas's attempt to absorb the Stargate/Crusoe model into a sanctioned channel before the xAI model spreads.

The counterpoint matters. The 233 GW large-load queue is heavily double-counted — the same hyperscaler shops the same megaproject across multiple substations — and ERCOT's own adjusted forecast effectively haircuts the queue by roughly half.[^27][^28] The 64 GW gas queue is interconnection requests, not steel in the ground; historical realization rates in ERCOT's gas queue have run well below 50%. And SB 6's cost-allocation provisions — who pays for network upgrades triggered by a 75 MW load — remain in active PUCT rulemaking, meaning the economic teeth of the statute are not yet set.

Texas is the only US jurisdiction in 2026 with a working legal template for forcibly curtailing a hyperscaler. If SB 6 holds up through PUCT implementation, expect Virginia, Ohio, and Arizona to copy the 75 MW threshold and curtailment hook within 18 months — and expect every capacity-market ISO to ask why it can't do the same.

## 05. Iron, copper, and lead times — the bottleneck is industrial, not political

The interconnection queue is the headline constraint, but the binding constraint is the factory floor: the gas turbines, transformers, HV cable, switchgear, and gensets that an AI campus actually needs are sold out for the rest of the decade, and the OEM CEOs are saying so on the record.

:::stats
- {label: "GEV GT backlog", value: "100 GW", note: "Q1 2026, +17 GW QoQ"}
- {label: "GEV Electrification backlog", value: "$42.4B", note: "+86% org. orders YoY"}
- {label: "Siemens Energy backlog", value: "€154B", note: "Record; book-to-bill 1.72"}
- {label: "Caterpillar backlog", value: "$63B", note: "+79% YoY"}
- {label: "Vertiv Q1 sales", value: "+30%", note: "Backlog >$15B"}
:::

Start at the prime mover. GE Vernova's gas-turbine backlog plus slot-reservation agreements went from 83 GW to 100 GW in a single quarter and management is openly guiding to 110+ GW by year-end 2026; in Q1 they booked 21 GW (19 GW of SRAs, 2 GW of firm orders) and shipped only 4 GW.[^34] New bids are pricing 10–20% above the Q4 2025 booked backlog,[^35] and IEEFA's October survey found new-build CCGT equipment costs up roughly 3x in two years — from $700–1,000/kW to about $2,400/kW — with some developers paying $25M *non-refundable* reservation fees for a 2030 delivery slot.[^36] OEMs are now advising 7–8 year planning horizons against ~5-year lead times for large frames, up from 2–3 years earlier in the decade.[^37]

:::slope(left-label="2023", right-label="2026", unit="$/kW")
| Item | 2023 | 2026 |
|------|------|------|
| New-build CCGT equipment cost | 850 | 2400 |
:::

The equity market has noticed. The four cleanest pure-play exposures — GE Vernova on turbines and electrification, Vertiv on data-center power and cooling, and Constellation and Talen on the nuclear-PPA side — have re-rated as the constraint has hardened, with GEV up roughly 2x and Vertiv nearly 3x off mid-2025 lows.

:::line-chart(title="The power-trade rally", subtitle="TTM monthly close, $/share", y-unit=$)
x: 2025-06,2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05
GEV: 529.15,660.29,612.97,614.9,585.14,599.77,653.57,726.37,873.6,872.9,1083.46,1049.23
VRT: 128.41,145.6,127.55,150.86,192.86,179.73,162.01,186.18,254.89,250.58,328.49,370.94
CEG: 322.76,347.84,307.98,329.07,377.0,364.36,353.27,280.68,329.88,279.25,313.0,267.2
TLN: 290.77,377.57,378.92,425.38,399.78,394.27,374.84,348.36,370.97,319.23,372.42,334.24
:::

The downstream picture is the same shape. GE Vernova's Electrification segment took $2.4B of data-center equipment orders in *one quarter* — more than all of 2025 — pushing segment backlog to $42.4B on +86% organic order growth, with management guiding to $60B by 2028.[^38] Siemens Energy printed a record €17.7B of Q2 FY26 orders for a €154B group backlog and a 1.72 book-to-bill, with Gas Services leading.[^39] Vertiv's Q1 2026 sales rose 30% YoY to $2.65B at a 20.8% adjusted operating margin (+430 bps), backlog crossed $15B, and FY26 guidance went to $13.5–14.0B.[^40]

Cable is no looser. Prysmian's HV backlog sits near €17B plus another €2B unbooked — roughly €19B of addressable work, visibility through 2028.[^41] Nexans' adjusted Power-Transmission backlog is €7.9B with transmission sales up 11.1% YoY.[^42] Hitachi Energy and Siemens Energy are quoting ~18-month GIS switchgear backlogs while utilities pre-order 24 months ahead, and the EU's SF6 phase-out (Reg. 2024/573) layers replacement demand onto roughly 1.2M legacy panels.[^43]

:::rank-list
- {label: "Gas turbines (frame)", value: "~260 wks", pct: 100, highlight: true}
- {label: "HV cable (Prysmian/Nexans)", value: "Through 2028", pct: 95}
- {label: "Diesel/gas gensets", value: "~104 wks", pct: 80}
- {label: "GIS switchgear", value: "~78 wks", pct: 65}
:::

Backup power is the same story. Caterpillar's Q1 2026 backlog hit a record $63B, +79% YoY, with Power & Energy up 22% and Power Generation up 41–48%; large reciprocating-engine backlog is up 3.5x since January 2024 and CAT is building toward ~3x its 2024 capacity.[^44] Cummins says industry-wide gas/diesel genset lead times sit near two years, has doubled data-center production capacity through 2025, and has delivered more than 39 GW to date.[^45]

Two strategic chokepoints sit underneath all of this. First, *steel*: Cleveland-Cliffs' Butler Works is the only US producer of grain-oriented electrical steel — the magnetic core of every large transformer — and POSCO is taking an ~10% equity stake (~$700M) while a $150M Weirton conversion stands up additional transformer capacity in H1 2026; the White House's April 2026 DPA Section 303 Presidential Determination explicitly designated transformers, substations, HV breakers, and electrical core steel as defense-critical.[^47] Second, *copper*: Goldman sees LME copper averaging $10,710/t in H1 2026 and J.P. Morgan models a ~330 kt refined deficit for the year, against a single large AI campus that needs 40,000–50,000 tonnes of the metal.[^48] Carrier's data-center orders rose 500% in Q1 2026 (after +400% in Q4 2025), with management guiding ~$1.5B of 2026 data-center revenue and expanding the ZutaCore direct-to-chip liquid-cooling investment[^49] — heat rejection is now a line item, not an afterthought.

Then there is the human bottleneck. BLS pegs electrician median pay at $62,350 (May 2024) with 9% projected growth and ~81,000 openings a year; IBEW estimates electrical work is 45–70% of data-center construction cost and that the industry needs more than 300,000 new workers, while NECA reports apprenticeship applications grew >70% nationwide from 2022 to 2024.[^46] You cannot hire a journeyman in a quarter.

The counterpoint deserves a hearing. Jefferies recently argued the gas-turbine bottleneck is "easing" as OEMs add shifts and capacity, and the performance-per-watt curve on Blackwell-class accelerators compresses the copper-and-iron tonnage per delivered MW of useful compute. Both are real. Neither moves a 2027 delivery slot.

Tying back to section 03's queue, the cabinet-equipment factories *are* the queue. Even a politically perfect interconnection regime cannot ship a 500 MW campus without a frame, a transformer, and a switchgear lineup that does not yet exist. The marginal data-center MW in 2027–2029 is gated by Schenectady, Charlotte, Greensboro, Butler, and Drammen — not by FERC.

## 06. Nuclear: restarts deliver, SMRs are paper

The hyperscaler-nuclear press releases imply ~10 GW of new advanced capacity by 2030, but the MW that will actually serve AI loads before then are LWR restarts and license extensions — not anything described in NRC ADAMS as Generation IV.

The deal flow looks decisive on paper. Microsoft signed a 20-year PPA in September 2024 to restart Three Mile Island Unit 1 as the Crane Clean Energy Center (~835 MW), with COD pulled forward from 2028 to 2027 and a $1B DOE LPO conditional commitment behind it.[^52][^53] Meta locked up Constellation's Clinton plant (~1,121 MW) on a 20-year PPA starting June 2027, replacing Illinois's expiring ZEC and adding a 30 MW uprate.[^57] Amazon and X-energy announced >5 GW of Xe-100 capacity in Washington by 2039, with a Cascade phase of 4×80 MW.[^56] Oracle pitched a "triple SMR" gigawatt cluster. Add Meta's January 2026 deal for up to 8 additional TerraPower Natrium units (2.8 GW) and the announced stack clears 10 GW.[^61]

What is actually permitted, poured, or operating is a different number. NRC has issued construction permits for the Kairos Hermes 2 demonstration at Oak Ridge (~50 MWe combined across two KP-FHR units, ground broken April 17 2026, target COD 2030)[^58] and for TerraPower's Natrium at Kemmerer (345 MWe SFR boosted to 500 MWe with molten-salt storage, construction officially started April 23 2026, completion target February 2031).[^61] Holtec's Pioneer SMR-300 at Palisades — two ~340 MWe PWRs, ~680 MWe total — filed a phased construction permit plus limited work authorization on December 31 2025 and was formally docketed by NRC on February 27 2026, with construction completion in the early 2030s.[^63] {accent}That is the entire advanced-reactor steel-in-the-ground pipeline.{/} Zero commercial SMRs are operating on the US grid today, and the first plausible US SMR COD remains Hermes 2 in 2030 at tens of MWe.[^60]

The regulatory hinge that reshaped this market was FERC docket ER24-2172. On November 1 2024 FERC rejected PJM's amended Susquehanna ISA in a 2-1 vote (Christie and See in the majority, Phillips dissenting), blocking Amazon's expansion of co-located load at Talen's Susquehanna from 300 MW to 480 MW.[^54] AEP and Exelon's affidavit had estimated a {accent}~$140M/yr cost shift to other PJM ratepayers{/} from the behind-the-meter configuration.[^55] FERC denied rehearing in April 2025, and Talen and AWS reorganized into a 1,920 MW front-of-meter PPA in June 2025 — a structure that does not require FERC approval and has become the template for every post-November-2024 hyperscaler-nuclear deal.[^65]

The unwritten warning under all of this is the UAMPS-NuScale Carbon Free Power Project, terminated November 8 2023 after the LCOE rose from $58/MWh in 2021 to $89/MWh in 2023 — the first major SMR project killed on cost, and the reason every announced SMR target now lives behind take-or-pay sleeves from hyperscaler balance sheets.[^59]

Restarts and extensions are where the actual kWh come from. Holtec's Palisades (800 MWe PWR, closed 2022) transitioned to "operations" status August 25 2025 with a $1.52B DOE LPO loan behind it, though restart has slipped from late 2025 to Q1 2026 and continues to slip on welding-code disputes.[^62] Diablo Canyon (2,256 MW) received NRC 20-year license renewals in April 2026 extending Unit 1 to November 2 2044 and Unit 2 to August 26 2045 — but California state law still caps operations at 2030, leaving a CA-vs-NRC tension that has to resolve politically before the federal permit means anything.[^64]

:::timeline
- {date: 2023-11, headline: "NuScale-UAMPS terminated", body: "First major SMR project killed after $58→$89/MWh cost escalation."}
- {date: 2024-09, headline: "Microsoft-TMI/Crane PPA", body: "Constellation announces 20-year PPA to restart 835 MW TMI-1."}
- {date: 2024-10, headline: "Amazon-X-energy ≥5 GW", body: "Largest commercial SMR target announced; 5 GW by 2039 in Washington."}
- {date: 2024-11, headline: "FERC rejects Amazon-Talen", body: "2-1 vote blocks expansion of co-located load at Susquehanna."}
- {date: 2025-06, headline: "Meta-Constellation Clinton", body: "20-yr PPA for ~1,121 MW of existing nuclear, plus 30 MW uprate."}
- {date: 2025-06, headline: "Talen-AWS 1,920 MW FOM PPA", body: "Front-of-meter workaround signed after FERC denial."}
- {date: 2025-09, headline: "Crane COD pulled to 2027", body: "Constellation accelerates 835 MW restart one year."}
- {date: 2026-02, headline: "Holtec SMR-300 CP docketed", body: "NRC accepts construction permit for 2×340 MW at Palisades."}
- {date: 2026-03, headline: "TerraPower Natrium permit", body: "First commercial non-LWR construction permit in 40 years."}
- {date: 2026-04, headline: "Kairos Hermes 2 groundbroken", body: "First electricity-producing Gen IV reactor under construction."}
- {date: 2026-04, headline: "Diablo Canyon +20 yrs", body: "NRC extends to 2044/45, but CA law still caps at 2030."}
:::

:::rank-list
- {label: "Announced (Amazon X-energy + Oracle + Meta Natrium + Microsoft Crane)", value: ">10 GW", pct: 100}
- {label: "NRC construction permits issued (Natrium + Hermes 2 + Pioneer LWA + Crane)", value: "~1.5 GW", pct: 15}
- {label: "Operating new advanced reactor MWe", value: "0 MW", pct: 1}
:::

:::stats
- {label: "TMI/Crane restart", value: "835 MW", note: "COD pulled to 2027"}
- {label: "Palisades restart", value: "800 MW", note: "Slipping past Q1 2026"}
- {label: "Clinton (Meta PPA)", value: "1,121 MW", note: "Operating; contracted June 2027"}
- {label: "Diablo Canyon", value: "2,256 MW", note: "NRC extended to 2044/45"}
:::

:::callout(kind=warn, label=Counterpoint)
The SMR slate is not all paper. Westinghouse AP300 and GE-Hitachi BWRX-300 are both moving through pre-application review in 2026, restarts are politically robust under both parties, and the existing US fleet already generates ~770 TWh/yr — a modest uprate program across that fleet could deliver meaningful MW into AI load faster than any SMR construction schedule. The thesis is not "nuclear can't help"; it is "the help arrives from the boring end of the stack."
:::

The hyperscaler-nuclear PPA stack delivers accounting comfort — clean attributes for ESG disclosure, hedged long-dated power prices, board-level optics — but very little incremental kWh into the AI load curve before 2030. The MW that move the needle this decade are restarts (Crane, Palisades), license extensions (Diablo), and uprates on the operating fleet. Everything labeled "advanced" is a 2030s story being financed in the 2020s.

## 07. Behind-the-meter, and the gas counter-thesis

When FERC blocked the Amazon-Talen co-location amendment in November 2024, hyperscalers stopped waiting for the grid and started buying their own power plants — and the oil majors arrived to sell them gas.

The hinge was a 2-1 FERC order on Section 205 grounds rejecting PJM's amended Susquehanna ISA, which would have grown Amazon's behind-the-meter draw from 300 MW to 480 MW.[^54] The decisive evidence in the docket was an AEP/Exelon affidavit pegging the ratepayer cost-shift at roughly $140M/yr — transmission and ancillary services the co-located load would consume without paying for.[^55] That number, more than any climate or reliability argument, is why the order went the way it did. The industry's response was not to litigate but to route around: if the FERC-jurisdictional interconnect is the problem, don't have one.

Crusoe is now the canonical playbook. In December 2024 and June 2025 the company placed orders for 29 GE Vernova LM2500XPRESS aeroderivative turbines — roughly 35 MW each, about 1 GW in aggregate, deliverable as factory-finished skids in months rather than years.[^68] Those units anchor the Abilene/Lancium campus that Crusoe expanded to eight buildings and 1.2 GW for the Oracle-OpenAI Stargate workload, with Phase 2 commercial operation targeted for mid-2026.[^69] Chevron, partnered with Engine No. 1 and GE Vernova, has gone bigger and more explicit: up to 4 GW using seven GE Vernova 7HA frame turbines, first units end-2027, with the press release stating the power is "not designed to flow initially through the existing transmission grid" and the plants engineered to be >90% CCS-capable.[^70] ExxonMobil — not a power company a year ago — has disclosed a >1,500 MW gas-fired, >90% carbon-capture, non-grid-connected plant on a roughly five-year COD.[^71] Energy Transfer supplies the molecules: >6 Bcf/d of new contracted pipeline capacity at an 18-year average term, with ~900 MMcf/d already dedicated to three Oracle data centers and 150 MMcf/d to Hyperscale's Nexus Hubbard AI campus.[^74]

| Project | Operator | Capacity | Status | COD |
|---|---|---|---|---|
| *Stargate Abilene | Crusoe / Oracle-OpenAI | 1.2 GW | Under construction | Mid-2026 |
| Chevron Power Foundry | Chevron / Engine No.1 / GEV | 4 GW | FID stage | End-2027 |
| ExxonMobil gas+CCS | ExxonMobil | >1.5 GW | Engineering | ~2029-30 |
| AWS-Vistra Comanche Peak | Vistra (nuclear, on-site) | 1.2 GW | Contracted | 4Q-2027 |
| AWS-Talen Susquehanna FOM | Talen | 1.92 GW | Signed (post-FERC) | Ramping |

:::stats
- {label: "Total announced", value: "~10 GW", note: "BTM + FOM, AI-dedicated"}
- {label: "BTM gas", value: "~7 GW", note: "Crusoe + Chevron + Exxon"}
- {label: "FOM gas (NRG/LS Power)", value: "~2 GW"}
- {label: "Nuclear FOM", value: "~3 GW", note: "Talen + Vistra + Crane"}
:::

:::quote(attr="Larry Coben, NRG Energy CEO")
We have zero interest in being in the speculative new capacity build business. New large loads must bring their own power.
:::

Coben's line captures what the merchant generators learned from the 2000s capacity glut and are not going to forget: a 5.4 GW GEV/Kiewit pipeline and a $12B LS Power 13 GW gas acquisition are being built only against contracted demand.[^73] Even the front-of-meter response to FERC fits the same pattern — the Talen-AWS 1,920 MW PPA signed June 2025 is a bilateral that does not need FERC approval,[^75] and AWS's 20-year 1,200 MW Comanche Peak deal with Vistra sites the data center on Vistra's nuclear-adjacent land with 1-for-1 backup, with initial energization 4Q-2027 and full ramp through 2032.[^72]

The counter-thesis is real and worth stating plainly. BTM gas runs at up to roughly 3x the carbon intensity of the average grid kWh it displaces, and the CCS economics that Chevron and Exxon are leaning on remain unproven at this scale and tariff regime; Exxon's 1.5 GW is still engineering rather than steel-in-the-ground, with COD no earlier than 2029. FERC's December 2025 PJM ruling, which signaled that some co-located arrangements will be re-categorized as firm-contract transmission demand, threatens to pull a slice of this capacity back into the regulated tariff and the cost-allocation fight that started it all.[^18]

Roughly 10 GW of generation for AI is being procured outside the integrated-resource-plan process that has governed US power since the 1970s. The hyperscalers are not waiting for the queue, the capacity auction, or the ratepayer; they are paying gas-turbine OEMs and oil majors directly to put steel on a pad next to a fence.

## 08. The flexibility case the orthodoxy ignores

The bottleneck thesis assumes every new AI gigawatt must be served firm at four-nines reliability — but if hyperscalers accept even 0.5% annual curtailment, the existing US grid has roughly 98 GW of headroom sitting idle, dwarfing anything a new transformer foundry can deliver before 2028.

The Norris et al. work out of Duke's Nicholas Institute is the document the orthodoxy keeps not citing. Their central finding: the installed US generation and transmission base can absorb very large flexible loads at trivial curtailment levels, because system-wide capacity is sized for a peak that almost never occurs.

:::stats
- {label: "Headroom @ 0.25% curtailment", value: "76 GW", note: "~22 hrs/year"}
- {label: "Headroom @ 0.5% curtailment", value: "98 GW"}
- {label: "Headroom @ 1.0% curtailment", value: "126 GW"}
- {label: "Headroom @ 5.0% curtailment", value: "215 GW"}
:::

The 98 GW figure at 0.5% curtailment[^151] is larger than the entire combined nameplate of US nuclear. And it is not evenly distributed — the headroom concentrates in the RTOs that are already the focus of data-center siting fights:

:::rank-list
- {label: "PJM Interconnection", value: "18 GW", pct: 100, highlight: true}
- {label: "MISO", value: "15 GW", pct: 83}
- {label: "ERCOT", value: "10 GW", pct: 56}
- {label: "SPP", value: "10 GW", pct: 56}
- {label: "Southern Company", value: "8 GW", pct: 44}
:::

The reason is structural slack. US power systems run at only a 53% average annual load factor; 98% of the hours in a year, more than 10% of installed capacity sits unused; only ~35 hours per year qualify as true extreme peak.[^77] Even the marginal thermal asset is underutilized — the US natural gas combined-cycle fleet ran at a 57% capacity factor in 2022, and the most efficient new units only manage 64%.[^83] The grid is not full. The grid is mostly empty, most of the time.

The operators closest to the data-center build-out are starting to say so out loud.

:::quote(attr="Lynn Good, Duke Energy CEO")
99.99% of the time, we have plenty of power. In our contracts, we have 50 hours per year that we can curtail them — and this allows them to come online now versus having to wait.
:::

Duke's posture matters because it inverts the queue problem from section 03: the interconnection delay is not generation scarcity, it is rigid firmness assumed at the meter. Drop the assumption, and the queue partially clears itself.[^79] The hyperscaler with the most to lose from rigid firmness has reached the same conclusion.

:::quote(attr="Amin Vahdat, Google AI Infrastructure")
Would you rather have four nines of availability and half the capacity, or two nines of availability and twice the capacity? Very often they say: oh my gosh, give me the two-times capacity.
:::

This is not theory.[^81] Google has now contracted approximately 1 GW of data-center demand response across Indiana Michigan Power, TVA, Entergy Arkansas, Minnesota Power, and DTE,[^78] the first hyperscaler-scale commitment of its kind. EPRI's DCFlex initiative — explicitly a venue for codifying these load-following protocols — has grown from 14 to 45 collaborators in months, with a Phoenix demonstration achieving 10–40% workload flex during a simulated peak event.[^80] And the technical objection that AI training is non-interruptible is being engineered away: Microsoft Research models 17–54% cost savings from training-cluster participation in reserve-service DR programs, exploiting checkpoint-and-resume; Microsoft and NVIDIA have already co-developed GB200 power-smoothing firmware to keep the training loop from destabilizing the grid in the first place.[^82] Google's Carbon-Intelligent Computing System has been time-shifting non-urgent compute — YouTube transcoding, Translate model updates, Photos enhancement — across more than twenty data centers on four continents for half a decade using what it calls Virtual Capacity Curves.[^84] The flex toolkit exists, in production, at hyperscale.

The honest counterpoints are real but narrower than the orthodoxy claims. Inference workloads — the latency-sensitive serving side, not training — genuinely cannot be curtailed without violating end-user SLAs; enterprise contracts on Azure and AWS do not contemplate utility-driven brownouts; some of the Norris headroom is transmission-bound and cannot reach the substations where AI campuses want to land; and 1 GW of contracted Google DR is a rounding error against the 8+ GW Google already operates. But "the cheapest gigawatt before 2028 is firm new generation" survives none of this. It is, almost certainly, the gigawatt you already have, served to a customer willing to take 0.5% curtailment — a customer who, increasingly, is asking for exactly that deal.

## 09. The global race — UAE buys 5 GW, China starts 94 GW of coal

While US grid politics calcify around capacity auctions and county zoning hearings, sovereign states have unlocked balance sheet, fuel, and permitting at a scale the US cannot match this decade — making the AI power constraint, in the end, a {accent}jurisdictional{/} one.

:::rank-list
- {label: "UAE Abu Dhabi (G42 + Stargate UAE)", value: "5.0 GW", pct: 100, highlight: true}
- {label: "France Paris (MGX/Mistral/EDF)", value: "1.4 GW", pct: 28}
- {label: "UK Blyth (Stargate UK + Blackstone)", value: "1.1 GW", pct: 22}
- {label: "Saudi HUMAIN (Phase 1 with Nvidia)", value: "0.5 GW", pct: 10}
- {label: "UK Culham", value: "0.5 GW", pct: 10}
:::

The headline number is Abu Dhabi. G42 and a US consortium unveiled Phase 1 of a {accent}5 GW AI campus{/} during Trump's state visit on May 15 2025 — the largest AI campus outside the United States.[^85] A week later, Stargate UAE — a 1 GW compute cluster inside the same campus, anchored by OpenAI, Oracle, Nvidia, SoftBank, and Cisco — was formally launched, with the first 200 MW slated to come online in 2026.[^86] Saudi Arabia moved in parallel: HUMAIN's May 2025 Nvidia partnership committed to an initial 18,000 GB300 GPUs and "several hundred thousand" over five years across up to 500 MW of AI factories.[^87] By November, that envelope had expanded to {accent}600,000 GPUs over three years{/}, with xAI taking 18k GB300, AWS standing up 150k GPUs in Riyadh, and Global AI as a third anchor.[^88]

The UK has run a smaller, more state-led version of the same play. January 2025's AI Opportunities Action Plan designated Culham — the UKAEA fusion site — as the first AI Growth Zone, scaling from 100 MW to 500 MW.[^89] In September, North East England (Cobalt Park + Blyth) was named the second zone, anchored by a £10B Blackstone commitment and a Stargate UK expansion from 8,000 to 31,000 GPUs; Blyth is targeted at {accent}1.1 GW within six years{/}.[^90] France completed the European picture in May 2025, when MGX (UAE), Bpifrance, Mistral, and Nvidia announced a 1.4 GW Paris-region campus — Europe's largest — powered by EDF nuclear, with construction in H2 2026 and operations in 2028.[^93] Korea's October 2025 sovereign deal with Nvidia covers 260,000+ GPUs across Samsung, SK, Hyundai, the MSIT National AI Computing Center, and NAVER Cloud.[^94] India's IndiaAI Mission ($1.25B over five years) put 44% of its envelope into sovereign GPU compute;[^91] its common pool crossed {accent}38,000 GPUs{/} by late 2025 at roughly 42% below market rates.[^92]

:::stats
- {label: "China coal starts 2024", value: "94.5 GW", note: "Highest since 2015"}
- {label: "China wind+solar 2024", value: "356 GW", note: "4.5× EU additions"}
- {label: "Intelligent compute (FP16)", value: "725.3 EF", note: "+74.1% YoY"}
- {label: "State Grid 2024 capex", value: "$84B", note: "RMB 600B, record"}
:::

China is in a different league, and it is the only jurisdiction that has openly fused fossil and renewable build-out behind compute. CREA/GEM document that China started construction on {accent}94.5 GW of new coal in 2024{/} — the highest since 2015 — even as it added 356 GW of wind and solar, a figure roughly equal to the total US installed wind+solar fleet at year-end.[^95][^96] The NDRC's "Eastern Data, Western Compute" framework routes ten national data center clusters across eight hubs, with the western nodes (Inner Mongolia, Ningxia, Gansu, Guizhou) sitting on top of that cheap stranded power.[^97] The result: intelligent computing capacity hit 725.3 EFLOPS (FP16) in 2024, up 74% YoY, with a 46.2% CAGR target through 2028.[^98] To move the electrons, State Grid spent {accent}RMB 600B ($84B){/} on grid capex in 2024 — a record — primarily on UHV corridors.[^99] The Hami–Chongqing ±800 kV UHVDC, commissioned June 2025, is the third Xinjiang-to-east line; alone it will deliver >36 TWh/year over 2,260 km.[^100]

:::compare
- {role: LOWEST, name: "Rest of world", value: "~10 GW"}
- {role: HIGHEST, name: "China (grid + coal starts)", value: "~144 GW"}
- {role: SUBJECT, name: "United States", value: "~30 GW"}
:::

:::callout(kind=warn, label=Counterpoint)
Sovereign announcements have a historically low realization rate, and the UAE/Saudi numbers are heavily contingent on US BIS export licenses for advanced GPUs — a license regime that could tighten under any future administration. Most "Stargate global" sites are still paper: Stargate UAE has 200 MW live in 2026, not 1 GW; Stargate UK is at 8k GPUs, not 31k.[^86][^90] China's 725 EFLOPS figure is FP16, not the FP32/BF16 baseline Western hyperscalers report against, so the headline gap to US capacity is overstated.[^98] And 94 GW of coal *starts* is not 94 GW of generation — completion timelines stretch three to five years.
:::

The binding constraint on US AI buildout is no longer chips or capital — it is permitting, interconnection, and local politics. The sovereigns the US Commerce Department is licensing chips to can {accent}underwrite balance sheet, fuel, transmission, and zoning in a single signature{/}. If a frontier lab in 2027 needs 2 GW in 24 months, Abu Dhabi, Riyadh, and the NDRC can answer yes. PJM and ERCOT, on current rules, cannot.

## 10. The disconfirming view — efficiency, overbuild, and the case the bottleneck softens

The strongest argument against everything in sections 01-09 is that the demand curve bends before the supply curve breaks — that algorithmic efficiency, generational perf/W jumps, and the first audible hyperscaler murmurs of "overbuild" together push the binding power constraint out past 2028, by which time iron, copper, and queue reform have time to catch up.

The cost evidence is hard to dismiss. Inference for GPT-3.5-quality output fell {accent}280x in 18 months{/}, from $20.00 to $0.07 per million tokens between November 2022 and October 2024.[^103] Anthropic cut Opus list pricing 67% in a single release this February — Opus 4.1 at $15/$75 became Opus 4.6 at $5/$25, with the long-context surcharge eliminated.[^104] Epoch AI's longitudinal study finds the compute needed to reach a fixed LLM performance level halves every {accent}~8 months{/} (95% CI 5-14 months), roughly 3x faster than Moore's Law.[^102] And the training side has its own shock: DeepSeek shipped a 671B-parameter MoE model for $5.576M in direct compute — 2.788M H800 GPU-hours at $2/hr.[^101]

:::slope(left-label="Nov 2022", right-label="Oct 2024", unit=$)
| Item | Nov 2022 | Oct 2024 |
|------|----------|----------|
| Cost per 1M tokens (GPT-3.5-quality) | 20.00 | 0.07 |
:::

The hardware story rhymes. Blackwell B200 delivered up to {accent}30x inference perf/W{/} over Hopper H100 in best-case FP4 LLM workloads with NVLink,[^106] and NVIDIA's March announcement claims Vera Rubin will add another ~10x perf/W over Blackwell at the rack level, with 35x tokens/MW once the LPU-plus-Rubin disaggregated inference stack is in production.[^105] If even half of that lands in the field, the megawatt-per-token denominator in 2027 looks nothing like the one driving today's load-growth forecasts.

:::compare
- {role: LOWEST,  name: "Hopper H100", value: "1x baseline"}
- {role: HIGHEST, name: "Vera Rubin (2027)", value: "~10x vs Blackwell"}
- {role: SUBJECT, name: "Blackwell B200", value: "~30x vs Hopper"}
:::

:::stats
- {label: "Efficiency halving", value: "~8 mo", note: "Epoch AI, 95% CI 5-14"}
- {label: "DeepSeek V3 training", value: "$5.576M", note: "2.788M H800-hrs @ $2"}
- {label: "Anthropic Opus price cut", value: "-67%", note: "Feb 2026 release"}
- {label: "DeepSeek V4 inference FLOPs", value: "27%", note: "vs V3.2 at 1M-tk context"}
:::

DeepSeek's V4-Pro release in February brought {accent}27% of single-token inference FLOPs{/} and {accent}10% of KV-cache{/} versus V3.2 at 1M-token context, with 1.6T total / 49B active parameters[^107] — exactly the kind of architectural compounding that, multiplied by hardware perf/W, makes the orthodox 2030 power forecasts look like straight-line extrapolation through a curve.

The hyperscaler side is starting to admit it out loud:

:::quote(attr="Satya Nadella, Microsoft CEO")
There will be an overbuild of AI infrastructure. Our problem is not a lack of chips, but a lack of places to plug them in.
:::

That was November 2025.[^108] Nine months earlier, TD Cowen's channel checks reported Microsoft canceling ~200 MW of US data center leases and letting more than 1 GW of statements-of-qualifications expire — the first public crack in the hyperscaler AI capex wall, though Microsoft partially walked the framing back as reallocation rather than retreat.[^109] Jensen Huang's preferred frame, that chips run roughly {accent}10x the cost of the electricity{/} that powers them and that grid bottlenecks add months not years to a buildout,[^110] is the steelman in one sentence: the economics still favor pouring concrete now, because the chip amortization dwarfs the kilowatt-hour bill.

Where the steelman fails is timing. Microsoft's Q3 FY26 print RAISED capex guidance[^2] — the same Microsoft whose CEO said "overbuild." The Stargate signings keep coming. And critically, perf/W only helps for *new* builds: the iron already on order for 2026-2027 delivery was specified in 2024, against power contracts written in 2024, into substations queued in 2023. Vera Rubin's 35x tokens/MW arrives {accent}after{/} the 2026-2027 power bottleneck binds, not before. The APAC inference buildout (section 09) is locking in inflexible 24/7 load profiles that defeat the very flexibility case (section 08) the orthodoxy ignores. Efficiency is real, the overbuild is plausible past 2028 — but the next 18 months of capex prints will land on iron whose denominator is fixed. The disconfirming view loses, narrowly, on calendar.

## 11. The political fork — ratepayers below, the executive above, counties in the middle

The AI build is no longer being decided in one room: the federal executive is accelerating, state utility commissions are repricing, and county boards are saying no — and the three vectors are pulling hard enough in opposite directions that the load that gets built in 2026-2028 will be the load that survives a three-front political fight, not the load with the best LCOE.

:::timeline
- {date: 2025-01-20, headline: "Trump EO 14156", body: "National energy emergency invoked; DPA, CWA §404 emergency permits, and 10 USC §2808 DoD construction authority unlocked."}
- {date: 2025-02-19, headline: "Indiana I&M tariff", body: "IURC settlement creates Tariff I.P. for ≥70 MW per site / ≥150 MW aggregate; I&M peak forecast climbs from 2,800 MW to >7,000 MW by 2030."}
- {date: 2025-03-18, headline: "Loudoun eliminates by-right", body: "World's largest data-center cluster ends by-right siting; every application now needs Planning Commission review."}
- {date: 2025-07-23, headline: "AEP Ohio Data Center Tariff", body: "≥25 MW threshold, 85% contracted-capacity monthly minimum, 12-yr term, exit fee = 3 years of minimum charges."}
- {date: 2025-08-06, headline: "Tucson rejects Project Blue", body: "City Council unanimously kills 290-acre AWS-linked campus — first major US city to reject an Amazon hyperscale project."}
- {date: 2025-08-07, headline: "Prince William Digital Gateway void", body: "Circuit Court rules 2,100-acre / 37-data-center rezoning 'void ab initio' on Virginia public-notice grounds."}
- {date: 2025-11-25, headline: "Virginia SCC creates GS-5", body: "Dominion biennial review approves new ≥25 MW data-center rate class; residential bills rise $11.24/mo in 2026."}
- {date: 2025-12-05, headline: "AZ ACC ratepayer protections", body: "TEP agreement approved with cost-shift firewall; APS proposes +45% rate hike for XL users."}
- {date: 2025-12-18, headline: "FERC PJM colocation order", body: "Unanimous FERC order directs PJM to set clear rules for data-center colocation at existing power plants."}
- {date: 2025-12-19, headline: "Georgia PSC approves 9,885 MW", body: "5-0 vote authorizes Georgia Power 2025 IRP Update; ~$16B capex against ~7,900 MW of signed data-center contracts."}
:::

The tariff convergence is striking. In ten months four of the largest data-center jurisdictions wrote essentially the same contract — high minimum take, decade-plus term, exit penalty — and the AEP Ohio order has become the template the others copy.

| Jurisdiction | Threshold | Minimum take | Term |
|---|---|---|---|
| VA Dominion GS-5[^111] | ≥25 MW | 85% T&D / 60% gen | 14 yrs |
| *AEP Ohio[^113] | ≥25 MW | 85% capacity / monthly | 12 yrs (4 ramp + 8 min) |
| Indiana I&M Tariff I.P.[^114] | ≥70 / 150 MW | Not-disclosed | Long-term |
| Arizona APS XHLF (proposed)[^121] | Extra-large | TBD | TBD |

The Memphis xAI case shows what happens when tariff design lags load arrival. TVA wholesales power to MLGW at roughly $88/MWh for residential and $60/MWh for industrial; MLGW then resells residential at $122/MWh (a 38.6% markup) versus industrial at $64/MWh (6.7%) — meaning a majority-Black residential base is effectively subsidizing the distribution cost of the largest single new industrial load in the city, even after xAI funded a $24M substation.[^119]

:::compare
- {role: LOWEST, name: "TVA→MLGW industrial", value: "$60/MWh"}
- {role: HIGHEST, name: "MLGW residential resale", value: "$122/MWh"}
- {role: SUBJECT, name: "TVA→MLGW residential", value: "$88/MWh"}
:::

:::callout(kind=warn, label="Ratepayer impact")
New Jersey residential rates climbed 21.6% from July 2024 to July 2025 (24.5% for one DC utility), with data centers accounting for ~97% of PJM's 5,250 MW load-growth forecast.[^122] Virginia's new GS-5 class is forecast to add $11.24/mo to residential bills in 2026.[^111] Ratepayer rage — not transmission queues — is the central political risk to the 2026 build.
:::

Federal policy is the only vector pushing unambiguously forward. Trump EO 14156, signed January 20 2025 and continued January 14 2026, invokes the National Emergencies Act, Defense Production Act, Clean Water Act §404 emergency permits, and 10 USC §2808 DoD construction authority — a stack designed to override exactly the state and local processes now hardening against new load.[^115] FERC's December 18 unanimous order on PJM colocation provides the regulatory plumbing for behind-the-meter deals at existing plants.[^120]

State and county pushback is no longer rhetorical. Loudoun County — the literal physical center of the global internet — eliminated by-right data-center development on March 18 2025 and approved Phase 2 siting standards in September; every new campus now needs a public hearing.[^116] Two weeks earlier a Prince William Circuit Court voided the 2,100-acre Digital Gateway rezoning on public-notice grounds, freezing 37 planned data centers.[^118] Tucson's unanimous August 6 rejection of Project Blue is the first time a major US city has killed an Amazon hyperscale project outright, and the trigger was a combination of water sustainability concerns and the NDAs the developer demanded.[^117]

The counterpoint matters. Tariff terms are negotiable in practice — hyperscaler cash flow easily absorbs 85% minimum take, and several of the new structures (Indiana, Arizona) include carve-outs that let utilities discount headline rates against bundled commitments. The OBBBA permitting overhaul could re-energize federal siting authority in 2026, and the executive's emergency powers under EO 14156 are real — DoD construction authority alone can move generation onto federal land outside state PUC jurisdiction.[^115] The Georgia PSC's 5-0 approval of 9,885 MW of new build[^112] is the reminder that the political fight is not uniformly hostile; in pro-growth states the regulatory machine is still saying yes.

The question is no longer whether 2026's planned AI MW get electrons, but who pays for them. Every jurisdiction that copies the AEP Ohio template forces hyperscalers to either absorb the take-or-pay, slow the build, or move to a federal-emergency-authority site — and the location of the next 50 GW of AI load will be determined by which of those three options breaks first.

## 12. What would break the thesis

The case built across sections 01–11 is that AI's binding 2026-2028 constraint is power, the supply chain, and the politics around them — and that no near-term mitigation closes the gap. The honest exercise is to ask what would falsify that. Four scenarios would meaningfully soften it.

**(a) Algorithmic efficiency compounds faster than perf/W.** Epoch AI's ~8-month halving time for compute-per-quality is the conservative reading of the curve;[^102] if the next two model generations cut effective MW-per-useful-token by another 5-10x on top of Vera Rubin's claimed gains,[^105] the LBNL low-case (325 TWh by 2028) becomes the high-case, and the iron already on order overbuilds the market. Two things to watch: the *gap* between DeepSeek-V4-class efficiency releases and the next Western frontier model,[^107] and any explicit hyperscaler guidance to *reduce* FY27 capex from the FY26 print.

**(b) Large-load curtailment regimes proliferate at SB 6 speed.** Texas wrote a 75 MW threshold plus ERCOT-administered curtailment into statute in eight months.[^29] If PJM, MISO, ERCOT, and CAISO converge on similar regimes by mid-2027 — and FERC's December 2025 colocation order is the federal half of exactly that movement[^120] — Norris's 98 GW of latent headroom[^151] becomes deliverable supply rather than research-paper rhetoric. Watch the PJM tariff filings due Q2 2026 and whether Indiana, Virginia, and Arizona copy the curtailment language alongside the take-or-pay terms.

**(c) Hyperscaler capex turns over.** Microsoft's CEO has already said "overbuild" out loud;[^108] TD Cowen has already flagged canceled leases;[^109] but Q1 2026 prints across all four hyperscalers raised guidance.[^1][^2][^3][^4] If even one of the four guides FY27 capex *down* in the next two earnings cycles, the demand wave loses its self-reinforcing quality and the queue-vs-iron problem becomes a 2028 absorption problem rather than a 2026 shortage.

**(d) Federal emergency authority actually builds.** Trump EO 14156 is a stack of unused statutory hammers — DPA Section 303, ESA emergency consultation, DoD construction authority on federal land.[^115] If the administration uses 10 USC §2808 to site 5 GW of gas or restart 3 GW of nuclear on military reservations *outside* state PUC and county jurisdiction, the political fork of section 11 inverts: federal speed beats local veto. The April 2026 DPA Section 303 determination on transformers[^47] is the signal that this lever is being warmed up.

**What would not break the thesis.** Counter-claims that do *not* survive the evidence: that perf/W gains will arrive in time to bend the 2026-2027 iron-on-order curve (calendar mismatch); that BTM gas can scale to 50 GW without environmental backlash (xAI Memphis already shows the limit);[^33][^119] that SMRs deliver before 2030 (zero operating new advanced reactor MW in the US, ~400 MW permitted);[^60][^61][^58] that the capacity market mean-reverts (it has under-procured at the price cap with FERC pushing rule changes).[^12][^120]

The default scenario remains the one the report describes: $700B of locked-in 2026 capex, a queue that doesn't move, factories sold out into 2029, 0 MW of new advanced nuclear, 10 GW of unregulated BTM gas, sovereign rivals with permitting velocity the US cannot match, and a residential ratepayer revolt that gets louder every quarter. The next eighteen months of capex prints, FERC orders, and Loudoun zoning hearings will decide which scenario actually obtains.

:::references
- {id: 1, title: "Alphabet Q1 2026 8-K Exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1652044/000165204426000043/googexhibit991q12026.htm", source: "SEC EDGAR", date: "2026-04-29"}
- {id: 2, title: "Microsoft Q3 FY26 Press Release Exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/789019/000119312526191457/msft-ex99_1.htm", source: "SEC EDGAR", date: "2026-04-29"}
- {id: 3, title: "Meta Q1 2026 Press Release Exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1326801/000162828026028364/meta-03312026xexhibit991.htm", source: "SEC EDGAR", date: "2026-04-29"}
- {id: 4, title: "Amazon Q1 2026 Press Release Exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1018724/000101872426000012/amzn-20260331xex991.htm", source: "SEC EDGAR", date: "2026-04-29"}
- {id: 5, title: "Amazon Q1 2026 8-K - OpenAI Trainium and Anthropic 5 GW commitments", url: "https://www.sec.gov/Archives/edgar/data/1018724/000101872426000012/amzn-20260331xex991.htm", source: "SEC EDGAR", date: "2026-04-29"}
- {id: 6, title: "Microsoft Q3 FY26 - RPO $627B and AI run-rate $37B", url: "https://www.sec.gov/Archives/edgar/data/789019/000119312526191457/msft-ex99_1.htm", source: "SEC EDGAR", date: "2026-04-29"}
- {id: 7, title: "2024 United States Data Center Energy Usage Report", url: "https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report_1.pdf", source: "LBNL", date: "2024-12-20"}
- {id: 8, title: "Energy and AI", url: "https://iea.blob.core.windows.net/assets/de9dea13-b07d-42c5-a398-d1b3ae17d866/EnergyandAI.pdf", source: "IEA", date: "2025-04-10"}
- {id: 9, title: "EPRI: Data Centers Could Consume Up to 17% of US Electricity by 2030", url: "https://www.globenewswire.com/news-release/2026/02/26/3245491/0/en/EPRI-Data-Centers-Could-Consume-Up-to-17-of-U-S-Electricity-by-2030.html", source: "EPRI / GlobeNewswire", date: "2026-02-26"}
- {id: 10, title: "PJM 2025/26 Base Residual Auction Report", url: "https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2025-2026/2025-2026-base-residual-auction-report.ashx", source: "PJM Interconnection", date: "2024-07-30"}
- {id: 11, title: "PJM 2026/27 Base Residual Auction Report", url: "https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2026-2027/2026-2027-bra-report.pdf", source: "PJM Interconnection", date: "2025-07-22"}
- {id: 12, title: "PJM 2027/28 Base Residual Auction Report", url: "https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2027-2028/2027-2028-bra-report.pdf", source: "PJM Interconnection", date: "2025-12-17"}
- {id: 13, title: "Data centers drove 40% of latest PJM capacity auction costs", url: "https://www.utilitydive.com/news/data-centers-pjm-capacity-auction/808951/", source: "Utility Dive / Monitoring Analytics IMM", date: "2026-01-26"}
- {id: 14, title: "Dominion Energy contracted data center capacity ~48.5 GW", url: "https://www.datacenterdynamics.com/en/news/dominion-energy-nearly-doubles-data-center-capacity-under-contract-to-40gw/", source: "Data Center Dynamics", date: "2025-12"}
- {id: 15, title: "JLARC: Data Centers in Virginia", url: "https://jlarc.virginia.gov/pdfs/reports/Rpt598-2.pdf", source: "Virginia JLARC", date: "2024-12-09"}
- {id: 16, title: "NJ utility bills to rise 17-20% from PJM auction", url: "https://www.utilitydive.com/news/new-jersey-electric-bills-pjm-bpu-pseg-auction/740053/", source: "Utility Dive", date: "2025-02-12"}
- {id: 17, title: "Mid-Atlantic states reach PJM electricity price cap settlement", url: "https://insideclimatenews.org/news/30012025/mid-atlantic-states-pjm-electricity-price-cap/", source: "Inside Climate News", date: "2025-01-30"}
- {id: 18, title: "FERC directs PJM to create new rules for co-located large loads", url: "https://www.ferc.gov/news-events/news/ferc-directs-nations-largest-grid-operator-create-new-rules-embrace-innovation-and", source: "FERC", date: "2025-12-18"}
- {id: 19, title: "Queued Up 2025 Edition", url: "https://eta-publications.lbl.gov/sites/default/files/2025-12/queued_up_2025_edition_12.15.2025.pdf", source: "LBNL", date: "2025-12-15"}
- {id: 20, title: "Queued Up 2025 - median wait time", url: "https://eta-publications.lbl.gov/sites/default/files/2025-12/queued_up_2025_edition_12.15.2025.pdf", source: "LBNL", date: "2025-12-15"}
- {id: 21, title: "Fewer New Miles - US transmission grid build-out", url: "https://gridstrategiesllc.com/wp-content/uploads/ACEG_Grid-Strategies_Fewer-New-Miles-2025_vF.pdf", source: "Grid Strategies / ACEG", date: "2025-07"}
- {id: 22, title: "Transformer troubles - manufacturing and policy constraints", url: "https://www.woodmac.com/news/opinion/transformer-troubles-manufacturing-and-policy-constraints-hit-us-transformer-supply/", source: "Wood Mackenzie", date: "2025-08"}
- {id: 23, title: "Reshore electrical equipment as backlogs persist", url: "https://www.utilitydive.com/news/reshore-electrical-equipment-backlogs-transformer-breaker-nema/749265/", source: "Utility Dive / NEMA", date: "2025-04"}
- {id: 24, title: "2025 Long-Term Reliability Assessment", url: "https://www.nerc.com/globalassets/our-work/assessments/nerc_ltra_2025.pdf", source: "NERC", date: "2026-01-29"}
- {id: 25, title: "PJM queue and 2025 connections", url: "https://www.utilitydive.com/news/pjm-interconnection-queue-gas-solar-nuclear/818824/", source: "Utility Dive / PJM data", date: "2026-02"}
- {id: 26, title: "Briefing on Interconnection Process Enhancements", url: "https://www.caiso.com/documents/briefing-on-the-status-of-interconnection-process-enhancements-and-the-interconnection-queue-jul-2025.pdf", source: "CAISO", date: "2025-07"}
- {id: 27, title: "Long-Term Load Forecast Update 2025-2031 and Methodology Changes", url: "https://www.ercot.com/files/docs/2025/04/07/8.1-Long-Term-Load-Forecast-Update-2025-2031-and-Methodology-Changes.pdf", source: "ERCOT", date: "2025-04-07"}
- {id: 28, title: "ERCOT's large-load queue jumped almost 300% last year", url: "https://www.utilitydive.com/news/ercots-large-load-queue-jumped-almost-300-last-year-official/808820/", source: "Utility Dive / ERCOT", date: "2026-01-06"}
- {id: 29, title: "Texas Senate Bill 6 - large-load interconnection overhaul", url: "https://www.bracewell.com/resources/texas-senate-bill-6-ushers-in-major-overhaul-of-large-load-interconnection-and-grid-access-rules/", source: "Bracewell LLP analysis", date: "2025-07"}
- {id: 30, title: "Texas grid - gas surpasses wind in ERCOT queue", url: "https://www.texastribune.org/2026/05/07/texas-power-grid-ercot-interconnection-queue-gas-wind/", source: "Texas Tribune / ERCOT data", date: "2026-05-07"}
- {id: 31, title: "OpenAI Stargate - where the US sites stand", url: "https://epoch.ai/blog/openai-stargate-where-the-us-sites-stand", source: "Epoch AI", date: "2026-04-17"}
- {id: 32, title: "GE Vernova and Crusoe announce major 29-unit aeroderivative deal", url: "https://www.gevernova.com/news/press-releases/ge-vernova-crusoe-announce-major-29-unit-aeroderivative-gas-turbine-deliver-ai-data-centers", source: "GE Vernova", date: "2025-07-22"}
- {id: 33, title: "Musk xAI running nearly 50 gas turbines unchecked", url: "https://techcrunch.com/2026/05/13/musks-xai-is-running-nearly-50-gas-turbines-unchecked-at-its-mississippi-data-center/", source: "TechCrunch", date: "2026-05-13"}
- {id: 34, title: "GE Vernova Q1 2026 Earnings Press Release", url: "https://www.gevernova.com/sites/default/files/gev_webcast_pressrelease_04222026.pdf", source: "GE Vernova", date: "2026-04-22"}
- {id: 35, title: "GE Vernova gas turbine backlog hits 100 GW as prices rise", url: "https://www.utilitydive.com/news/ge-vernova-gas-turbine-backlog-hits-100-gw-as-prices-rise/818332/", source: "Utility Dive", date: "2026-04-22"}
- {id: 36, title: "Global gas turbine shortages - CCGT capex tripled", url: "https://ieefa.org/sites/default/files/2025-10/IEEFA%20Report_Global%20gas%20turbine%20shortages%20add%20to%20LNG%20challenges%20in%20Vietnam%20and%20the%20Philippines_October2025.pdf", source: "IEEFA", date: "2025-10-01"}
- {id: 37, title: "Global gas turbine shortages - 7-8 year planning horizons", url: "https://ieefa.org/sites/default/files/2025-10/IEEFA%20Report_Global%20gas%20turbine%20shortages%20add%20to%20LNG%20challenges%20in%20Vietnam%20and%20the%20Philippines_October2025.pdf", source: "IEEFA", date: "2025-10-01"}
- {id: 38, title: "GE Vernova Q1 2026 - Electrification $42.4B backlog and $2.4B DC orders", url: "https://www.gevernova.com/sites/default/files/gev_webcast_pressrelease_04222026.pdf", source: "GE Vernova", date: "2026-04-22"}
- {id: 39, title: "Siemens Energy Q2 FY26 Earnings Release", url: "https://www.siemens-energy.com/global/en/home/press-releases/earnings-release-q2-fy-2026.html", source: "Siemens Energy", date: "2026-05-12"}
- {id: 40, title: "Vertiv Reports Strong First Quarter 2026", url: "https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx", source: "Vertiv IR", date: "2026-04-30"}
- {id: 41, title: "Prysmian Q1 2026 results / earnings call presentation", url: "https://seekingalpha.com/article/4896440-prysmian-s-p-a-2026-q1-results-earnings-call-presentation", source: "Seeking Alpha (Prysmian call)", date: "2026-04-30"}
- {id: 42, title: "Nexans Q1 2026 solid start to 2026", url: "https://www.nexans.com/app/uploads/2026/04/2026-04-28-pr-nexans-q1-2026.pdf", source: "Nexans", date: "2026-04-28"}
- {id: 43, title: "Transformer supply chain woes persist as energy demand grows", url: "https://eepower.com/tech-insights/transformer-supply-chain-woes-persist-as-energy-demand-grows/", source: "ePower Tech Insights", date: "2026"}
- {id: 44, title: "Caterpillar to triple power generation capacity (Q1 2026)", url: "https://www.manufacturingdive.com/news/caterpillar-triple-power-generation-capacity-raises-2030-targets-q1-2026-earnings/819078/", source: "Manufacturing Dive", date: "2026-04-30"}
- {id: 45, title: "Powering growth - Cummins data center backup power", url: "https://www.cummins.com/en-na/news/2025/11/12/powering-growth-cummins-solutions-data-center-backup-power", source: "Cummins", date: "2025-11-12"}
- {id: 46, title: "BLS Electricians OOH and IBEW data-center surge", url: "https://www.bls.gov/ooh/construction-and-extraction/electricians.htm", source: "US BLS / IBEW", date: "2024-2026"}
- {id: 47, title: "Cleveland-Cliffs Weirton transformer plant + GOES + DPA 303", url: "https://www.clevelandcliffs.com/news/news-releases/detail/644/cleveland-cliffs-announces-its-new-state-of-the-art", source: "Cleveland-Cliffs", date: "2026"}
- {id: 48, title: "Goldman Sachs - Copper prices forecast 2026", url: "https://www.goldmansachs.com/insights/articles/copper-prices-forecast-to-decline-from-record-highs-in-2026", source: "Goldman Sachs", date: "2026"}
- {id: 49, title: "Carrier Reports First Quarter 2026 Results", url: "https://ir.carrier.com/news/news-details/2026/Carrier-Reports-First-Quarter-2026-Results/default.aspx", source: "Carrier IR", date: "2026"}
- {id: 52, title: "Constellation to launch Crane Clean Energy Center (Microsoft PPA)", url: "https://www.constellationenergy.com/news/2024/Constellation-to-Launch-Crane-Clean-Energy-Center-Restoring-Jobs-and-Carbon-Free-Power-to-The-Grid.html", source: "Constellation Energy", date: "2024-09-20"}
- {id: 53, title: "US government backs Constellation Crane plan ($1B DOE loan)", url: "https://www.constellationenergy.com/newsroom/2025/11/us-government-backs-constellations-plan-to-launch-crane-clean-energy-center-adding-835-mws-of-new-baseload-power-to-the-grid.html", source: "Constellation Energy", date: "2025-11-03"}
- {id: 54, title: "FERC Order on ER24-2172 (Susquehanna ISA rejection)", url: "https://www.ferc.gov/sites/default/files/2024-11/20241101-3061_ER24-2172-000.pdf", source: "FERC", date: "2024-11-01"}
- {id: 55, title: "FERC ER24-2172 - AEP/Exelon $140M/yr cost shift testimony", url: "https://www.ferc.gov/sites/default/files/2024-11/20241101-3061_ER24-2172-000.pdf", source: "FERC", date: "2024-11-01"}
- {id: 56, title: "Amazon and Energy Northwest announce X-energy Cascade", url: "https://www.energy-northwest.com/news-releases/amazon-energy-northwest-announce-plans-to-develop-advanced-nuclear-technology-in-washington/", source: "Energy Northwest", date: "2024-10-16"}
- {id: 57, title: "Constellation-Meta 20-year deal for Clinton nuclear", url: "https://investors.constellationenergy.com/news-releases/news-release-details/constellation-meta-sign-20-year-deal-clean-reliable-nuclear", source: "Constellation Energy", date: "2025-06-03"}
- {id: 58, title: "Kairos Power breaks ground on Hermes 2 demonstration plant", url: "https://www.kairospower.com/updates/kairos-power-breaks-ground-on-hermes-2-demonstration-plant", source: "Kairos Power", date: "2026-04-17"}
- {id: 59, title: "UAMPS and NuScale terminate the Carbon Free Power Project", url: "https://www.nuscalepower.com/press-releases/2023/utah-associated-municipal-power-systems-and-nuscale-power-agree-to-terminate-the-carbon-free-power-project", source: "NuScale Power", date: "2023-11-08"}
- {id: 60, title: "Small Modular Reactor (SMR) Global Tracker", url: "https://world-nuclear.org/information-library/nuclear-power-reactors/small-modular-reactors/small-modular-reactor-smr-global-tracker", source: "World Nuclear Association", date: "2026-05-16"}
- {id: 61, title: "TerraPower Commences Construction at Kemmerer", url: "https://www.terrapower.com/TerraPower-Commences-Construction-on-Americas-First-Utility-Scale-Advanced-Nuclear-Power-Plant", source: "TerraPower", date: "2026-04-23"}
- {id: 62, title: "Palisades nuclear plant in operations status", url: "https://www.utilitydive.com/news/palisades-nuclear-plant-holtec-nrc-operations/758845/", source: "Utility Dive / Holtec", date: "2025-08"}
- {id: 63, title: "SMR LLC Pioneer Units 1 and 2 - Phased Construction Permit", url: "https://www.federalregister.gov/documents/2026/02/27/2026-03943/smr-llc-pioneer-units-1-and-2-phased-construction-permit-application-limited-work-authorization", source: "US Federal Register / NRC", date: "2026-02-27"}
- {id: 64, title: "Newsom welcomes approval of Diablo Canyon license renewals", url: "https://www.gov.ca.gov/2026/04/02/governor-newsom-welcomes-approval-of-diablo-canyon-license-renewals-delivering-on-californias-commitment-to-a-clean-and-reliable-grid/", source: "Office of the Governor of California", date: "2026-04-02"}
- {id: 65, title: "FERC denies Talen-Amazon agreement (again); 1,920 MW FOM PPA", url: "https://www.ans.org/news/2025-04-16/article-6937/ferc-denies-talen-amazon-agreementagain/", source: "ANS Nuclear Newswire", date: "2025-04-16"}
- {id: 68, title: "Crusoe and GE Vernova 29-unit LM2500XPRESS deal", url: "https://www.crusoe.ai/resources/newsroom/ge-vernova-and-crusoe-announce-major-29-unit-gas-turbine-deal", source: "Crusoe Energy", date: "2025-07-22"}
- {id: 69, title: "Crusoe expands Abilene AI data center campus to 1.2 GW", url: "https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts", source: "Crusoe Energy", date: "2025-03-18"}
- {id: 70, title: "Chevron + Engine No. 1 + GE Vernova - up to 4 GW", url: "https://engine1.com/wp-content/uploads/2025/01/2025-0127_FINAL-PRESS-RELEASE_EN1_CVX_GE_.pdf", source: "Engine No. 1 / Chevron / GE Vernova", date: "2025-01-28"}
- {id: 71, title: "ExxonMobil planning large gas-fired plant for data centers", url: "https://www.powermag.com/exxonmobil-planning-large-gas-fired-plant-to-serve-data-centers/", source: "Power Magazine", date: "2024-12-11"}
- {id: 72, title: "Vistra Reports Fourth Quarter and Full Year 2025 Results", url: "https://investor.vistracorp.com/2026-02-26-Vistra-Reports-Fourth-Quarter-and-Full-Year-2025-Results", source: "Vistra Corp IR", date: "2026-02-26"}
- {id: 73, title: "NRG bring-your-own-power and 5.4 GW pipeline", url: "https://www.utilitydive.com/news/nrg-energy-data-center-texas-earnings/813076/", source: "Utility Dive / NRG", date: "2025"}
- {id: 74, title: "Energy Transfer Q1 2026 earnings call", url: "https://www.fool.com/earnings/call-transcripts/2026/05/05/energy-transfer-et-q1-2026-earnings-transcript/", source: "Energy Transfer call (transcript)", date: "2026-05-05"}
- {id: 75, title: "Talen-AWS 1,920 MW front-of-meter PPA (post-FERC pivot)", url: "https://www.ans.org/news/2025-04-16/article-6937/ferc-denies-talen-amazon-agreementagain/", source: "ANS Nuclear Newswire", date: "2025-06"}
- {id: 77, title: "Norris Aug 2025 deck - 53% US load factor", url: "https://bloximages.newyork1.vip.townnews.com/newsdata.com/content/tncms/assets/v3/editorial/f/08/f08ea856-f7e5-457f-ad0d-852a813308e9/68b0ce304291e.pdf.pdf", source: "Norris (Duke Nicholas Institute)", date: "2025-08-21"}
- {id: 78, title: "Google demand-response milestone across five US utilities", url: "https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/demand-response-data-center-milestone/", source: "Google", date: "2026-03-19"}
- {id: 79, title: "Tyler Norris quoting Duke Energy CEO Lynn Good (Fortune)", url: "https://twitter.com/TylerHNorris", source: "Tyler Norris / Duke Energy", date: "2026-04-25"}
- {id: 80, title: "EPRI DCFlex - data center flexibility initiative", url: "https://spectrum.ieee.org/dcflex-data-center-flexibility", source: "IEEE Spectrum / EPRI", date: "2025-09"}
- {id: 81, title: "Tyler Norris quoting Vahdat at Latitude Media Transition AI", url: "https://twitter.com/TylerHNorris", source: "Tyler Norris / Vahdat (Google)", date: "2026-05"}
- {id: 82, title: "Power Stabilization for AI Training Datacenters (arXiv 2508.14318)", url: "https://arxiv.org/html/2508.14318v1", source: "Microsoft Research", date: "2025-08"}
- {id: 83, title: "Norris deck citing EIA-860M on NGCC capacity factor", url: "https://bloximages.newyork1.vip.townnews.com/newsdata.com/content/tncms/assets/v3/editorial/f/08/f08ea856-f7e5-457f-ad0d-852a813308e9/68b0ce304291e.pdf.pdf", source: "Norris (Duke) / EIA", date: "2025-08"}
- {id: 84, title: "Data centers work harder when the sun shines (CICS)", url: "https://blog.google/inside-google/infrastructure/data-centers-work-harder-sun-shines-wind-blows/", source: "Google", date: "2020-04"}
- {id: 85, title: "UAE and US presidents unveil 5 GW AI campus", url: "https://www.uae-embassy.org/news/uae-us-presidents-attend-unveiling-phase-1-new-5gw-ai-campus-abu-dhabi", source: "UAE Embassy / Commerce Department", date: "2025-05-15"}
- {id: 86, title: "G42 - Global Tech Alliance launches Stargate UAE", url: "https://www.g42.ai/resources/news/global-tech-alliance-launches-stargate-uae", source: "G42", date: "2025-05-22"}
- {id: 87, title: "HUMAIN and NVIDIA strategic partnership in Saudi Arabia", url: "https://nvidianews.nvidia.com/news/humain-and-nvidia-announce-strategic-partnership-to-build-ai-factories-of-the-future-in-saudi-arabia", source: "NVIDIA", date: "2025-05-13"}
- {id: 88, title: "HUMAIN expands partnership with NVIDIA, xAI, Global AI, AWS", url: "https://www.prnewswire.com/news-releases/humain-expands-strategic-partnership-with-nvidia-advancing-global-ai-infrastructure-with-xai-global-ai-and-aws-at-the-us-saudi-investment-forum-302620854.html", source: "PR Newswire / HUMAIN", date: "2025-11-19"}
- {id: 89, title: "UK AI Growth Zones strategy explainer", url: "https://www.computerweekly.com/news/366628066/The-UK-governments-AI-Growth-Zones-strategy-Everything-you-need-to-know", source: "Computer Weekly / UK gov.uk", date: "2025-01-13"}
- {id: 90, title: "GOV.UK - North East England AI Growth Zone", url: "https://www.gov.uk/government/news/north-east-england-set-for-billions-in-investment-and-thousands-of-jobs-as-uk-and-us-ink-tech-partnership", source: "GOV.UK", date: "2025-09-17"}
- {id: 91, title: "Cabinet approves IndiaAI Mission", url: "https://www.pmindia.gov.in/en/news_updates/cabinet-approves-ambitious-indiaai-mission-to-strengthen-the-ai-innovation-ecosystem/", source: "PMO India", date: "2024-03-07"}
- {id: 92, title: "India common compute capacity crosses 34,000 GPUs (PIB)", url: "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2132817", source: "Press Information Bureau India", date: "2025-05"}
- {id: 93, title: "MGX, Bpifrance, Mistral, NVIDIA - 1.4 GW Paris campus", url: "https://www.mgx.ae/en/news/mgx-bpifrance-mistral-ai-and-nvidia-launch-joint-venture-build-europes-largest-ai-campus", source: "MGX", date: "2025-05-19"}
- {id: 94, title: "South Korea AI infrastructure (NVIDIA + chaebols)", url: "https://nvidianews.nvidia.com/news/south-korea-ai-infrastructure", source: "NVIDIA", date: "2025-10-30"}
- {id: 95, title: "CREA/GEM - China 2024 coal construction starts 94.5 GW", url: "https://energyandcleanair.org/wp/wp-content/uploads/2025/02/CREA_GEM_China_Coal-power_H2-2024_FINAL.pdf", source: "CREA / Global Energy Monitor", date: "2025-02-13"}
- {id: 96, title: "China added 356 GW wind+solar in 2024 (CREA/GEM)", url: "https://energyandcleanair.org/wp/wp-content/uploads/2025/02/CREA_GEM_China_Coal-power_H2-2024_FINAL.pdf", source: "CREA / Global Energy Monitor", date: "2025-02-13"}
- {id: 97, title: "NDRC - ten national data center clusters across eight EDWC hubs", url: "https://en.ndrc.gov.cn/news/mediarusources/202202/t20220218_1315947.html", source: "NDRC", date: "2022-02-17"}
- {id: 98, title: "Xinhua - China intelligent computing 725.3 EFLOPS in 2024", url: "https://english.news.cn/20250217/3aa217e260d24515b7a3f66a5bb3a0da/c.html", source: "Xinhua", date: "2025-02-17"}
- {id: 99, title: "SASAC - SGCC 2024 grid investment surpassed RMB 600B", url: "http://en.sasac.gov.cn/2024/07/29/c_17563.htm", source: "SASAC / State Grid Corporation of China", date: "2024-07-29"}
- {id: 100, title: "Hami-Chongqing ±800 kV UHVDC commissioned", url: "https://english.news.cn/20250610/8643cf83a9ce4a75a52b4ef60865c001/c.html", source: "Xinhua", date: "2025-06-10"}
- {id: 101, title: "DeepSeek-V3 Technical Report (arXiv 2412.19437)", url: "https://arxiv.org/pdf/2412.19437", source: "DeepSeek", date: "2024-12-27"}
- {id: 102, title: "Algorithmic progress in language models", url: "https://epoch.ai/blog/algorithmic-progress-in-language-models", source: "Epoch AI", date: "2024-03-12"}
- {id: 103, title: "Stanford AI Index Report 2025 - inference cost collapse", url: "https://hai.stanford.edu/assets/files/ai_index_report_2026.pdf", source: "Stanford HAI", date: "2025-04-07"}
- {id: 104, title: "Anthropic API pricing - Opus 67% cut Feb 2026", url: "https://www.finout.io/blog/anthropic-api-pricing", source: "Finout / Anthropic", date: "2026-02"}
- {id: 105, title: "NVIDIA Vera Rubin platform", url: "https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform", source: "NVIDIA", date: "2026-03-17"}
- {id: 106, title: "Comparing NVIDIA Tensor Core GPUs (Hopper vs Blackwell)", url: "https://www.exxactcorp.com/blog/hpc/comparing-nvidia-tensor-core-gpus", source: "Exxact / NVIDIA spec sheets", date: "2024-03-18"}
- {id: 107, title: "DeepSeek V4 mHC efficiency breakthrough (Introl analysis)", url: "https://introl.com/blog/deepseek-v4-mhc-efficiency-breakthrough-february-2026", source: "Introl / DeepSeek V4 technical report", date: "2026-02"}
- {id: 108, title: "Microsoft CEO says there is an overbuild of AI systems", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-ceo-says-there-is-an-overbuild-of-ai-systems-dismisses-agi-milestones-as-show-of-progress", source: "Tom's Hardware / Satya Nadella", date: "2025-11-03"}
- {id: 109, title: "Microsoft cancels up to 2 GW of data center projects (TD Cowen)", url: "https://www.datacenterdynamics.com/en/news/microsoft-cancels-up-to-2gw-of-data-center-projects-says-td-cowen/", source: "DCD / TD Cowen", date: "2025-02-24"}
- {id: 110, title: "Nvidia CEO pours cold water on the AI power debate", url: "https://www.thestreet.com/technology/nvidia-ceo-pours-cold-water-on-the-ai-power-debate", source: "TheStreet / Jensen Huang", date: "2025"}
- {id: 111, title: "Virginia SCC rules in DEV biennial review case", url: "https://www.scc.virginia.gov/about-the-scc/newsreleases/release/scc-issues-order-on-dev-biennial-review-2025/scc-rules-in-dev-biennial-review-case.html", source: "Virginia State Corporation Commission", date: "2025-11-25"}
- {id: 112, title: "Georgia PSC data center fact sheet - 9,885 MW Georgia Power IRP", url: "https://psc.ga.gov/site/downloads/datacenterfactsheet.pdf", source: "Georgia PSC", date: "2025-12-19"}
- {id: 113, title: "AEP Ohio Data Center Tariff (PUCO 24-508-EL-ATA)", url: "https://www.aepohio.com/company/about/rates/data-center-tariff/", source: "AEP Ohio / PUCO", date: "2025-07-23"}
- {id: 114, title: "IURC Cause 46097 - Indiana Michigan Power large-load tariff", url: "https://iurc.portal.in.gov/_entity/sharepointdocumentlocation/865e7a14-3a7d-f011-b4cc-001dd803db57/bb9c6bba-fd52-45ad-8e64-a444aef13c39?file=46097_IndMich_+Submission+of+Semi-Annual+Report+-+August+2025_081925.pdf", source: "IURC / Indiana Michigan Power", date: "2025-02-19"}
- {id: 115, title: "Executive Order 14156 - Declaring a National Energy Emergency", url: "https://www.whitehouse.gov/presidential-actions/2025/01/declaring-a-national-energy-emergency/", source: "The White House", date: "2025-01-20"}
- {id: 116, title: "Loudoun County Phase 2 Data Center Standards & Locations", url: "https://www.loudoun.gov/6222/Phase-2-Data-Center-Standards-Locations", source: "Loudoun County, VA", date: "2025-03-18"}
- {id: 117, title: "Tucson City Council rejects Project Blue", url: "https://azluminaria.org/2025/08/06/tucson-city-council-rejects-project-blue-amid-intense-community-pressure/", source: "AZ Luminaria", date: "2025-08-06"}
- {id: 118, title: "Prince William Digital Gateway court ruling", url: "https://www.beankinney.com/data-center-infrastructure-under-siege-lessons-from-virginias-digital-gateway-decision/", source: "Bean Kinney LLP", date: "2025-08"}
- {id: 119, title: "NAACP and others appeal xAI turbine permits for Memphis DC", url: "https://tennesseelookout.com/briefs/naacp-others-appeal-xai-turbine-permits-for-memphis-data-center/", source: "Tennessee Lookout", date: "2025"}
- {id: 120, title: "FERC directs PJM to embrace innovation (colocation rules)", url: "https://www.ferc.gov/news-events/news/ferc-directs-nations-largest-grid-operator-create-new-rules-embrace-innovation-and", source: "FERC", date: "2025-12-18"}
- {id: 121, title: "ACC approves TEP Energy Supply Agreement - ratepayer protections", url: "https://www.azcc.gov/news/home/2025/12/05/acc-approves-tep-energy-supply-agreement--ensures-customer-protections-from-costs-related-to-data-center-project", source: "Arizona Corporation Commission", date: "2025-12-05"}
- {id: 122, title: "PJM capacity market and NJ rate-shock (FERC complaint)", url: "https://www.utilitydive.com/news/ferc-pjm-capacity-market-pennsylvania-shapiro/738095/", source: "Utility Dive / NJ BPU", date: "2025"}
- {id: 151, title: "Rethinking Load Growth - Norris/Duke Nicholas Institute (Aug 2025 deck)", url: "https://bloximages.newyork1.vip.townnews.com/newsdata.com/content/tncms/assets/v3/editorial/f/08/f08ea856-f7e5-457f-ad0d-852a813308e9/68b0ce304291e.pdf.pdf", source: "Norris et al. (Duke Nicholas Institute)", date: "2025-08-21"}
:::
