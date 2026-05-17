---
eyebrow: REPORT · AI INFRASTRUCTURE
title: The chokepoints inside the chokepoint
deck: AI's 2026 power crisis is real — but it is not a generation shortage. It is a transformer foundry, a water permit, a single-crystal blade casting, and a county zoning hearing.
lede: |
  In Q1 2026 the four AI hyperscalers committed roughly $700B of combined annual capex. The binding constraint everyone talks about — "not enough power" — is wrong in a way that matters. The world can build generation: gas turbine factories are expanding toward 90 GW/year, Chinese coal starts hit 94.5 GW in 2024, and Abu Dhabi underwrote 5 GW in a single signature. What it cannot do is ship a large power transformer in under 128 weeks, cool a 140 kW rack with air, or withdraw NYC-scale water volumes from stressed aquifers during summer peaks without a fight. This article traces the chokepoints inside the chokepoint — the specific supply chains, physical limits, and governance failures that turn a manageable generation gap into a structural bottleneck.
stats:
  - {label: Hyperscaler 2026 capex, value: ~$700B, note: +50% YoY, combined annual run-rate}
  - {label: Large transformer lead time, value: 128 wks, note: Up from 52 wks in 2020}
  - {label: Gas turbine annual capacity, value: 60-70 GW, note: vs ~110 GW of 2025 orders}
  - {label: US data center water (2030), value: "1,451 MGD", note: Comparable to NYC's ~1,000 MGD supply}
  - {label: GPU rack power, value: 140 kW, note: GB200 NVL72; air cooling limit ~23 kW}
  - {label: US BESS in service, value: 44.6 GW, note: Feb 2026; +16.5 GW in prior 12 months}
---

## 01. The bottleneck is real — but it is narrower than the panic implies

The standard narrative is that AI infrastructure has hit a power wall: the grid cannot supply the electrons. This is partly true, but misleading in a way that obscures where intervention would actually help. Global generation capacity is not the binding constraint. The binding constraints are four specific chokepoints — transformers, water, single-crystal turbine blades, and governance — each of which operates on a timeline that no amount of capex can compress.

Consider the supply side first. Global large gas turbine manufacturing capacity sits at 60-70 GW per year, while 2025 orders reached approximately 110 GW [^1]. That looks like a shortage — and it is — but the three major OEMs are expanding: GE Vernova's backlog plus slot reservations hit 100 GW in Q1 2026 alone, guiding to 110 GW by year-end [^2]; Mitsubishi Heavy Industries plans to double production capacity within two years [^3]; Siemens Energy raised FY28 midterm margin targets citing structurally tight supply [^4]. If all announced expansions complete on schedule, the industry ceiling could reach 80-90 GW/year by 2028. The capacity IS being built.

The transformer supply chain tells a different story. Large power transformer lead times sit at 128 weeks — nearly three years — with a 30% supply deficit in 2025 and demand up 116% since 2019 [^5]. A transformer factory takes 3-5 years to commission and costs hundreds of millions to over a billion dollars [^6]. The US has exactly one producer of grain-oriented electrical steel (GOES), the magnetic core of every large transformer — Cleveland-Cliffs' Butler Works — and imports an estimated 80% of its power transformers [^7]. The April 2026 DPA Section 303 Presidential Determination designating transformers as defense-critical is an admission that this chokepoint is not clearing through market mechanisms alone [^8].

:::compare
- {role: LOWEST, name: Gas turbine capacity growth, value: 80-90 GW/yr by 2028}
- {role: HIGHEST, name: Transformer lead time, value: 128 weeks}
- {role: SUBJECT, name: Transformer supply deficit, value: "30% in 2025"}
:::

The point is not that there is no constraint. It is that the constraint's location determines what fixes it. Building more gas turbines helps the generation gap but does nothing for the transformer that steps voltage from 345 kV to 34.5 kV at the AI campus fence. Building more transformers does nothing for the water permit a county board withholds. The chokepoint is not one thing; it is a chain, and chains break at the weakest link.

The counterpoint is real: transformer factories are being built. Hitachi Energy committed over $1 billion to North American expansions [^6]; Cleveland-Cliffs' $150M Weirton conversion adds domestic GOES and transformer capacity in H1 2026 [^7]; Eaton, Prolec GE, and Siemens Energy are all adding lines. But the cumulative North American capacity expansion of roughly $2 billion compares to a global transformer market of $69.66 billion growing at 7.24% CAGR [^9] — a rounding error against the demand surge. The constraint eases in 2029-2030, but the 2026-2028 buildout is already locked.

## 02. The GPU power spiral: 700 watts to 140 kilowatts per rack

The physics of AI compute is pushing toward heat dissipation limits, and the trajectory makes liquid cooling a hard requirement — not an optimization — from the Blackwell generation onward.

NVIDIA's datacenter GPU TDP has grown from 300W (P100, 2016) to 700W (H100/H200, 2022-2023) to 1000W (B200, 2024) to 1100W (B300 Blackwell Ultra, 2025) [^10]. AMD's MI355X, expected in 2026, reaches 1400W [^11]. At the rack level, the GB200 NVL72 — a liquid-cooled, rack-scale system with 72 Blackwell GPUs — draws approximately 140 kW per rack, compared to the roughly 23 kW that air cooling can physically handle [^12].

:::line-chart(title="NVIDIA Datacenter GPU TDP Trajectory", subtitle="Maximum Thermal Design Power, watts per GPU", y-unit=W)
x: 2016,2017,2018,2020,2022,2023,2024,2025,2026
NVIDIA top GPU: 300,350,350,400,700,700,1000,1100,1400
:::

This is not merely a facilities problem. It changes the siting calculus. An air-cooled data center can be built nearly anywhere with fiber and power. A liquid-cooled facility requires a source of water or dielectric fluid, heat rejection infrastructure, and a supply chain for cold plates, coolant distribution units, and quick-disconnect fittings — a supply chain that is itself scaling from near-zero to tens of billions of dollars in under five years.

:::compare
- {role: LOWEST, name: Air cooling limit, value: "~23 kW/rack"}
- {role: HIGHEST, name: Immersion cooling, value: "~100 kW/rack"}
- {role: SUBJECT, name: GB200 NVL72 rack, value: "~140 kW/rack"}
:::

The cooling power overhead shrinks dramatically with liquid. Traditional air cooling adds roughly 35% overhead (PUE ~1.35), while direct-to-chip liquid cooling brings PUE to 1.05-1.15 and immersion to as low as 1.02 [^13]. Google's fleet-wide trailing-twelve-month PUE has held at 1.09 since 2024, with its best campus (Central Ohio) reaching 1.04 [^14]. AWS reports a global PUE of 1.15 in 2024 with best sites at 1.04 in Europe [^15]. But the PUE improvement has a hidden cost: direct-to-chip cold plates require a manufacturing ecosystem (cold plates, manifolds, CDUs, quick disconnects) that faces its own scaling constraints as AI demand outpaces capacity [^12].

The implication is straightforward: every AI data center built after 2025 requires liquid cooling, and the liquid cooling supply chain is itself a chokepoint. ASHRAE TC9.9 warns that "cooling loss is catastrophic when supporting extreme chip powers" [^16] — meaning the reliability engineering gets harder, not easier, as densities rise.

What weakens this argument: immersion cooling at 100 kW/rack may cover the next generation, and NVIDIA claims the GB200 NVL72 delivers 25x more AI performance at the same power compared to H100 air-cooled infrastructure [^17]. If the 25x claim holds in the field, the power-per-useful-compute actually declines even as rack-level power rises. The question is whether the 25x is realized on real workloads or only on the benchmarks NVIDIA chooses.

## 03. Water: the parallel constraint nobody is pricing

While the industry fixates on megawatts, the harder constraint may be measured in megaliters. Data center water consumption sits at the intersection of three trends — rising chip power, evaporative cooling's efficiency advantage, and intensifying water stress in the very regions where data centers concentrate — that together create a trilemma no PUE metric captures.

The scale of the issue is only now coming into quantitative focus. A March 2026 analysis projects that if 2024 water-use intensity persists, US data centers would require 697 to 1,451 million gallons per day (MGD) of new water capacity by 2030 — comparable to New York City's entire daily supply of roughly 1,000 MGD, at a valuation of $10-58 billion [^18]. AI servers alone are expected to drive annual increases in US water consumption of 200-300 billion gallons by 2030 [^19].

:::slope(left-label="2024 (est.)", right-label="2030 (projected)", unit=MGD)
| Scenario | 2024 | 2030 |
|---|---|---|
| Low (10% annual WUE improvement) | 300 | 527 |
| Mid (5% annual WUE improvement) | 300 | 997 |
| High (no WUE improvement) | 300 | 1751 |
:::

The geographic concentration makes this worse than the aggregate numbers suggest. AWS's global Water Usage Effectiveness (WUE) was 0.15 L/kWh in 2024 — but that average conceals variation of more than two orders of magnitude: Frankfurt at 0.01 L/kWh versus Jakarta at 2.75 L/kWh [^15]. High WUE in humid tropical regions reflects the physical fact that evaporative cooling — the efficiency workhorse in dry climates — does not work in high humidity, forcing operators toward less efficient dry cooling that, perversely, consumes more electricity during peak summer heat when the grid is already strained [^18].

:::stack-rows
categories: [Frankfurt, N. Virginia, Singapore, Jakarta]
rows:
  - {label: AWS WUE (L/kWh), values: [0.01, 0.12, 1.68, 2.75]}
:::

The trilemma is this: evaporative cooling saves power but consumes water; dry cooling saves water but consumes power; liquid cooling reduces both but requires a new supply chain. And the constraint that binds first is not annual volume but peak withdrawal — many US communities cannot supply peak cooling-water demand during the hottest days of the year, forcing operators toward less efficient dry cooling that further stresses the grid during summer peaks [^18].

Microsoft's response — direct-to-chip liquid cooling deployed at its Quincy, Washington site, which it describes as "a waterless technology" [^20] — shows the path is technically feasible. But Quincy is a single site in a region with abundant hydropower and cool ambient temperatures. It does not generalize to Phoenix, where a 290-acre AWS-linked campus was unanimously rejected by the Tucson City Council in August 2025, with water sustainability as a triggering concern [^21].

The counterpoint: AWS's global WUE improved 40% between 2021 and 2024 [^15], and Google replenished 64% of its freshwater consumption in 2024, up from 18% in 2023 [^22]. The trend line is favorable — but the absolute volumes are growing faster than the efficiency. A 40% WUE improvement against a 200% load increase still means 120% more water consumed. Replenishment projects, moreover, are often in different watersheds from consumption; they address the balance sheet, not the local aquifer.

## 04. Transformer alley: the 128-week chokepoint no capex can bypass

If one component deserves to be called the single binding constraint on AI infrastructure buildout, it is the large power transformer. The numbers are stark: 128-week lead times [^5], a 30% supply deficit [^5], prices up 45-95% since 2019 depending on type [^5], and a single domestic US producer of the grain-oriented electrical steel that forms every transformer's magnetic core [^7].

:::rank-list
- {label: Generator step-up transformers, value: 144 wks, pct: 100, highlight: true}
- {label: Large power transformers, value: 128 wks, pct: 89}
- {label: HV circuit breakers, value: 151 wks, pct: 100}
- {label: Gas turbines (frame), value: ~260 wks, pct: 100}
- {label: GIS switchgear, value: ~78 wks, pct: 65}
- {label: MV switchgear, value: 44 wks, pct: 30}
:::

The price trajectory tells its own story. Power transformer unit costs rose 77% since 2019; distribution transformers rose 78-95%; generator step-up units rose 45% [^5]. These are not commodity fluctuations — they reflect a structural supply-demand mismatch that is getting worse, not better.

:::slope(left-label="2019", right-label="2025", unit="index (2019=100)")
| Equipment type | 2019 | 2025 |
|---|---|---|
| Power transformers | 100 | 177 |
| Distribution transformers | 100 | 186 |
| GSU transformers | 100 | 145 |
| MV switchgear | 100 | 150 |
:::

The single most concentrated chokepoint in the entire AI supply chain may be Cleveland-Cliffs' Butler Works in Pennsylvania — the only US producer of grain-oriented electrical steel (GOES) [^7]. POSCO (South Korea), Nippon Steel (Japan), and Chinese mills can supply the global market, but the US is 80% import-dependent for large power transformers [^5], and trade policy (copper tariffs, cybersecurity restrictions on Chinese equipment) limits how much of that global capacity can reach US substations. The White House's April 2026 DPA Section 303 determination explicitly designating transformers, substations, HV breakers, and GOES as defense-critical is the clearest signal that the federal government recognizes this as a national-security chokepoint [^8].

:::donut(center-label="80% imported")
- {label: US-made power transformers, value: 20}
- {label: Imported power transformers, value: 80}
:::

Hitachi Energy's $6B+ global investment plan (including $1B+ in North America across Virginia, Quebec, and Tennessee) [^6], Siemens Energy's record €154B group backlog [^23], and GE Vernova's Electrification backlog of $42.4B (guiding to $60B by 2028) [^24] all point in the same direction: the factories are being built, but a transformer plant takes 3-5 years from groundbreaking to first unit. The capacity additions that break ground in 2026 ship their first transformers in 2029-2031. The 2026-2028 AI buildout is already committed to whatever the existing factory base can produce.

The counterpoint: China, South Korea, and India collectively represent over 60% of global transformer production capacity [^9], and some of that capacity can be redirected. But cybersecurity rules (DOE's 2020 prohibition on Chinese-manufactured bulk-power-system equipment), tariff uncertainty, and the sheer logistics of shipping 400-tonne transformers mean the global supply is not fungible. The transformer bottleneck is, in practice, a Western transformer bottleneck — which is why the APAC AI buildout faces a different set of constraints entirely.

## 05. Gas turbines: 60 GW of factories cannot fill 110 GW of orders

The prime mover behind most new AI power generation — the large frame gas turbine — faces its own manufacturing ceiling, and the binding sub-chokepoint is not the assembly line but the single-crystal superalloy blade foundry.

Global large gas turbine orders reached approximately 110 GW in 2025 against manufacturing capacity of 60-70 GW [^1]. The three major OEMs are responding: GE Vernova booked 21 GW in Q1 2026 alone (19 GW of slot reservations, 2 GW of firm orders) while shipping only 4 GW [^2]; Mitsubishi Heavy Industries is doubling capacity within two years after a previously announced 30% increase proved insufficient [^3]; Siemens Energy raised midterm margin targets citing structurally tight supply [^4].

:::compare
- {role: LOWEST, name: Manufacturing capacity, value: 60-70 GW/yr}
- {role: HIGHEST, name: 2025 global orders, value: "~110 GW"}
- {role: SUBJECT, name: GEV backlog + slots, value: 100 GW}
:::

But the factory floor is not the limit. The binding constraint is the production of single-crystal superalloy turbine blades — the components that sit in the hottest section of the turbine and determine its firing temperature and efficiency. Fewer than six suppliers globally have the capability, one blade set costs over $600,000, and production takes 60-90 weeks [^1]. There is no shortcut: the foundry process for a directionally-solidified single-crystal nickel superalloy blade is governed by metallurgical physics, not capital deployment speed.

The history makes the constraint structural, not cyclical. After 2015, global large gas turbine orders collapsed from approximately 65-70 GW/year to under 30 GW/year between 2016-2020 [^1]. OEMs idled capacity, retired skilled workers, and consolidated factory space. When orders rebounded — driven first by the post-Ukraine gas-for-coal switch in Europe, then by AI data center demand — the capacity was gone. The workers who knew how to cast single-crystal blades had retired or moved to other industries. Rebuilding that expertise takes years, not quarters.

:::line-chart(title="The Gas Turbine Supply-Demand Gap", subtitle="Global annual manufacturing capacity vs orders, GW", y-unit=GW)
x: 2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025
Annual orders (GW): 65,30,30,28,28,25,35,45,55,85,110
Mfg capacity (GW): 70,65,60,55,50,50,52,55,58,60,65
:::

Turbine prices reflect the squeeze. Wood Mackenzie expects large gas turbine prices to reach approximately $600/kW by end-2027, a 195% increase from 2019 levels [^25]. New-build CCGT equipment costs have already roughly tripled in two years, from $700-1,000/kW to approximately $2,400/kW installed [^26]. Some developers are paying $25 million in non-refundable reservation fees for a 2030 delivery slot [^26].

The aeroderivative path — smaller turbines derived from aircraft engines, like GE's LM2500XPRESS (~35 MW) — provides a partial bypass. Crusoe ordered 29 units (~1 GW) for its Abilene campus [^27], and the conversion of retired jet engines (ProEnergy PE6000 from CF6 cores, FTAI Power from CFM56 cores, ~25-48 MW each) represents a supplementary source. But aeroderivatives ship in hundreds of MW, not the multiple GW per project that large frame HA/HL/JAC turbines (400-600+ MW each) deliver. They are a tactical fix, not a strategic solution.

The counterpoint worth watching: if MHI's 2x expansion and GE Vernova's Greenville/Belfort capacity increases complete on schedule, the industry ceiling could reach 80-90 GW/year by 2028-2029 — closing roughly half the supply-demand gap. And if AI demand moderates (see Section 10), the gap closes faster. But for 2026-2027 deliveries, the turbine slots are already sold.

## 06. Gas supply: 7.5 Bcf/d of new demand into a tight market

Even if the turbines could be built, the molecules to fuel them face their own constraints. Converting 50 GW of announced data-center gas generation into pipeline demand yields approximately 7.5 billion cubic feet per day of incremental natural gas consumption, per DT Midstream management [^28] — a figure that competes directly with surging LNG exports for limited US production growth.

The EIA's May 2026 Short-Term Energy Outlook projects US dry natural gas production at 110.61 Bcf/d for 2026 and 115.01 Bcf/d for 2027 — roughly 4.4 Bcf/d of annual growth [^29]. In the same period, LNG exports are projected to rise from 15.1 Bcf/d (2025 actual) to 18.2 Bcf/d (2027), consuming about 3.1 Bcf/d of that production growth [^29]. The remaining approximately 1.3 Bcf/d/year of net new gas availability must cover ALL other demand growth — including data centers, industrial reshoring, electrification, and weather-driven residential/commercial load.

:::line-chart(title="US Natural Gas: Production vs Competing Demands", subtitle="Bcf/d, EIA STEO May 2026 projections", y-unit=Bcf/d)
x: 2024,2025,2026,2027
Dry production: 105.0,107.65,110.61,115.01
LNG exports: 12.0,15.1,17.0,18.2
:::

The pipeline infrastructure to deliver this gas is itself constrained. DT Midstream's Vector 2028 Pipeline expansion (~400 MMcf/d) and Enbridge's Sunrise expansion (~$4B, +300 MMcf/d) are moving forward [^28], but combined they represent less than one-tenth of potential data center demand. The Permian Basin, the engine of US production growth at 29.2 Bcf/d in 2026, faces severe egress constraints evidenced by record-low Waha Hub spot prices [^29]. Northeast gas — the Marcellus/Utica resource closest to Virginia's data center alley — faces persistent pipeline permitting headwinds that have blocked multiple projects.

:::stats
- {label: US dry gas production 2026, value: 110.61, unit: Bcf/d, note: EIA STEO May 2026}
- {label: DC incremental gas demand, value: "~7.5", unit: Bcf/d, note: Per DT Midstream ~50 GW → 7.5 Bcf/d}
- {label: LNG export growth 2025→2027, value: "+3.1", unit: Bcf/d, note: Competes directly with DC demand}
- {label: Henry Hub forecast, value: "~$4-5", unit: /MMBtu, note: Up from ~$2.50 in 2024}
:::

The CCS complication makes the arithmetic worse. Multiple announced AI gas plants — Chevron's 4 GW Power Foundry, ExxonMobil's >1.5 GW facility — promise >90% carbon capture [^30]. Post-combustion CCS using amine-based solvents imposes a 20-30% energy penalty on the host plant, meaning each MWh of net output requires 1.2-1.3 MWh of gas input [^28]. If CCS-equipped AI gas plants become the norm, the gas demand per delivered MWh rises by roughly a quarter — turning a 7.5 Bcf/d estimate into something closer to 9-10 Bcf/d. Chevron and Exxon's CCS promises remain, as of mid-2026, at the engineering and permitting stage; DT Midstream's own CCS projects are "stuck in the pre-FID stage" with Louisiana permit timelines described as "too uncertain to provide an updated date" [^28].

The counterpoint is that gas markets clear through price. At $5/MMBtu Henry Hub — roughly double the 2024 average — some demand destruction occurs naturally, and some production that was uneconomic at $2.50 becomes viable. The US gas resource base is not physically scarce; it is infrastructure-constrained. New Permian takeaway pipelines (Matterhorn, Blackcomb) and Haynesville expansions can unlock supply, but they face the same FERC permitting timelines as transmission. The question is not whether the molecules exist, but whether they can reach the right substations at the right time — which is the same question that bedevils every other link in this chain.

## 07. APAC builds while the West debates: grid governance as competitive advantage

The most important fact about the AI power bottleneck is that it is not global. It is regional, and its severity maps almost perfectly onto the rigidity of the local grid governance model. The jurisdictions that can build generation fastest — China, UAE, Saudi Arabia — face the least acute bottleneck. The jurisdictions with the most elaborate stakeholder processes — PJM, EU member states — face the most acute one. This is not a coincidence.

China added 356 GW of wind and solar in 2024 — roughly the entire installed US wind-plus-solar fleet at year-end — while simultaneously starting construction on 94.5 GW of new coal, the highest since 2015 [^31]. State Grid spent RMB 600 billion ($84 billion) on grid capex, a record, primarily on ultra-high-voltage corridors [^32]. The Hami-Chongqing ±800 kV UHVDC line, commissioned June 2025, alone delivers over 36 TWh/year over 2,260 km from Xinjiang's stranded coal and renewable resources to central China's compute clusters [^33]. China's "Eastern Data, Western Compute" framework routes ten national data center clusters across eight hubs, anchoring compute where the power is rather than where the users are [^34]. The result: intelligent computing capacity hit 725.3 EFLOPS (FP16) in 2024, up 74% year-over-year [^35].

:::rank-list
- {label: China (grid capex 2024), value: $84B, pct: 100, highlight: true}
- {label: UAE (Abu Dhabi AI campus), value: 5.0 GW, pct: 50}
- {label: US (annual transmission built), value: 322 mi. 345 kV+, pct: 5}
- {label: India (renewable capacity), value: 190.6 GW, pct: 30}
- {label: Japan (nuclear restarts), value: 13 of 33 operable, pct: 20}
- {label: South Korea (nuclear share), value: 31.7% of gen, pct: 25}
:::

Japan presents the most interesting APAC case because its constraint is not regulatory but physical. The country's grid is bifurcated at 50 Hz (east) and 60 Hz (west), with only about 1 GW of frequency-converter capacity between the two zones [^36]. This structural limitation — exposed catastrophically during the 2011 earthquake — means data center siting is effectively constrained to whichever frequency zone has available capacity. Japan targets nuclear at 20-22% of generation by 2040 with 13 reactors operating as of late 2024 [^37], but the restart pace depends on local political approval that moves at prefectural speed, not national.

South Korea's nuclear fleet — 23 reactors, 20.5 GWe, 31.7% of generation in 2024 — provides a baseload anchor that most AI jurisdictions lack [^38]. The Yoon administration's reversal of the prior phase-out policy and the 34.6% nuclear-by-2036 target give Korea a structural advantage in firm clean power. But KEPCO's financial strain from years of suppressed electricity tariffs threatens the investment timeline for both generation and grid [^38].

Taiwan is the warning case. The island completed its nuclear phase-out on May 18, 2025, shutting down the final reactor at Maanshan [^39]. It is now 83.2% fossil-dependent with 98% energy import reliance and only seven days of LNG safety stocks [^39]. The same grid that powers TSMC's 3nm fabs must now serve a growing AI data center load — a concentration risk that has no near-term mitigation.

Singapore's post-moratorium data center policy illustrates the governance trade-off directly. After a 2019-2022 moratorium, Singapore reopened applications with strict sustainability criteria: PUE below 1.3, Platinum green certification, and specific water-use limits. Only four of more than 20 applications were initially approved [^40]. The government is soliciting bids for new hydrogen-ready combined-cycle capacity (600+ MW by 2027, more by 2029-2030) and aiming to import 6 GW of low-carbon electricity by 2035 [^36]. Singapore is choosing to constrain load to available clean supply — the opposite of the "build first, permit later" model unfolding in Texas and Mississippi.

The implication for AI infrastructure competition is clear. The US advantage in chips and capital is partially offset by a disadvantage in generation build speed and grid governance. A frontier lab that needs 2 GW in 24 months can get a faster answer from Abu Dhabi, Riyadh, or the NDRC than from PJM. This does not mean those jurisdictions will win — export controls, talent concentration, and ecosystem depth still favor the US — but it means the power constraint is a competitiveness variable, not a universal constant.

## 08. The Jevons paradox: why efficiency may increase power demand

The strongest argument against the bottleneck thesis is that AI compute is getting dramatically more efficient, and that efficiency will bend the power demand curve before the supply constraints bind. The efficiency gains are real. The question is whether they reduce or increase total power consumption — and the evidence strongly favors the latter.

Algorithmic efficiency for pre-training is improving at roughly 3.0x per year — the compute needed to reach a fixed performance level halves every 7.6 months (90% CI: 5.6-8.1 months) [^41]. LLM inference prices are declining at approximately 40x per year — halving every two months, two orders of magnitude per year [^41]. DeepSeek-V4-Pro requires only 27% of the single-token inference FLOPs and 10% of the KV cache of DeepSeek-V3.2 at 1M-token context, a single-generation 3.7x FLOP reduction [^42].

:::slope(left-label="GPT-3.5 (Nov 2022)", right-label="DeepSeek V4 Flash (Apr 2026)", unit="$/M tokens")
| Metric | Nov 2022 | Apr 2026 |
|---|---|---|
| Cost per 1M input tokens | 20.00 | 0.14 |
| Cost per 1M output tokens | 20.00 | 0.28 |
:::

These are extraordinary numbers. But they are being absorbed — and more than absorbed — by demand growth. Training compute for frontier models grows at 5x per year (doubling every 5.2 months), outpacing algorithmic efficiency of 3x per year by a net factor of roughly 1.67x annually [^41]. Global AI computing capacity is doubling every 7 months (~3.3x/year since 2022) [^41]. The 1.28x/year improvement in hardware FLOP/s/W [^41] is the slowest lever in the system.

The Jevons mechanism is not theoretical. ByteDance's Doubao large language model surpassed 120 trillion daily tokens as of April 2026 — roughly a 1,000-fold increase since its launch in May 2024 [^57]. At the infrastructure level, Amazon, Google, Meta, Microsoft, and Oracle collectively projected roughly $705 billion in combined 2026 capital expenditures, an approximately 80% increase from their estimated $392 billion in 2025 [^58]. As the 2025 ACM FAccT paper by Luccioni, Strubell, and Crawford establishes: "Efficiency gains may paradoxically spur increased consumption" and "rebound effects undermine the assumption that improved technical efficiency alone will ensure net reductions" [^44].

:::stats
- {label: Algorithmic efficiency gain, value: 3.0x/yr, note: Halves every 7.6 months}
- {label: Training compute growth, value: 5x/yr, note: Outpaces efficiency 1.67:1}
- {label: Inference price decline, value: 40x/yr, note: Halves every 2 months}
- {label: Global AI fleet growth, value: 3.3x/yr, note: Doubles every 7 months}
- {label: China daily tokens (Mar 2026), value: "~140T", note: ~1,000x early 2024}
:::

The structural mechanism is what Sharma (2024) calls "revenue-driven system expansion" — cloud providers observe that energy efficiency and total energy consumption grow simultaneously because revenue generation drives system expansion, validated empirically with both Meta and Google data [^45]. And as inference prices drop, downstream firms adopt more compute-intensive agent architectures — multi-step reasoning, chain-of-thought, tool-using agents — making aggregate demand for compute "super-elastic," a structural Jevons Paradox specific to AI [^46].

The net effect, per Epoch AI's analysis, is sobering: even with a projected 24x improvement in power efficiency by 2030 (4x hardware FLOP/s/W + 2x FP8 adoption + 3x longer training), the compute demand for a 2e29 FLOP frontier training run — 5,000x the scale of Llama 3.1 405B — still implies roughly 200x the power draw, requiring about 6 GW per single run [^47]. Power binds before chips or data.

The counterpoint that matters: the 5x/year training compute growth is not a law of nature. It reflects industry choices — to pursue larger models, longer training, and higher capability — that could change. If the industry pivots from "scale is all you need" to "efficiency is all you need," the gap closes. But the incentives point the other way: as long as frontier capability translates to revenue and strategic advantage, the Jevons rebound dominates. The efficiency gains are real — and they are the reason total power demand will grow, not shrink.

## 09. Inference: the workload shift that reshapes the power map

The AI power debate has been dominated by training — the multi-gigawatt campus, the 100,000-GPU cluster, the $5.6M training run. But the grid implications of inference are fundamentally different, and the shift from a training-dominated to inference-dominated compute base changes where, when, and how flexibly power is consumed.

NVIDIA disclosed that 40% of its data center revenue came from inference as of early 2024 [^48], and the ratio has almost certainly risen since. Training clusters run at 80-90% GPU utilization with predictable, schedulable loads. Inference clusters operate at 20-50% utilization with spiky, latency-sensitive loads that cannot be time-shifted to off-peak hours without violating end-user service level agreements [^49].

:::donut(center-label="AI power")
- {label: Inference power (est. 2026), value: 60}
- {label: Training power (est. 2026), value: 40}
:::

This has three structural implications for the grid. First, inference data centers must be located near population centers (for latency), not near cheap stranded power (for cost). An inference cluster serving New York cannot sit in West Texas. Second, inference load is less flexible — you cannot checkpoint and resume a real-time chat session the way you can pause a training run. The flexibility case that is the strongest counter-argument to the bottleneck thesis (see the Norris et al. analysis of 98 GW of headroom at 0.5% curtailment) applies primarily to training, not inference. Third, the growing share of agentic AI workloads — multi-step reasoning, tool use, code generation — multiplies the tokens per user query, turning what was one inference call into a chain of ten or a hundred.

DeepSeek-V4-Pro's 1M-token context window is the shape of things to come: a single inference session can consume as much compute as a small training run did in 2020. At DeepSeek V4 Flash pricing ($0.14/M input, $0.28/M output tokens [^50]), the cost to fill a 1M-token context is approximately $0.14 and the cost to generate a thoughtful 10,000-token response is about $2.80 — cheap enough that agents will use the full capacity routinely.

The battery storage angle provides only partial relief. The US had approximately 44.6 GW of utility-scale battery storage in service as of February 2026, with 22.9 GW planned for the next 12 months [^51]. But BESS is deployed for 2-4 hour peak shaving, not full load firming. A 1 GW AI campus would need roughly 24 GWh of storage to firm a full day — versus the 4 GWh needed for peak-only coverage — which is uneconomical at current system costs [^52]. Lithium carbonate prices, meanwhile, surged to 192,000 CNY/T as of May 2026, up 197.67% year-over-year, with data center operators explicitly named as new demand drivers [^53]. The battery supply chain is itself becoming a bottleneck.

:::compare
- {role: LOWEST, name: Training flexibility, value: High (checkpointable)}
- {role: HIGHEST, name: Inference rigidity, value: Low (latency-bound)}
- {role: SUBJECT, name: Agentic AI power per query, value: 10-100x single-turn}
:::

The counterpoint: inference can be geographically distributed across many smaller sites rather than concentrated in one mega-campus, which reduces the per-site grid impact. Google's Carbon-Intelligent Computing System has been time-shifting non-urgent compute across more than twenty data centers for years [^54]. And some inference (batch processing, synthetic data generation, model evaluation) is deferrable. But the growth in real-time, interactive, agentic inference — the kind users actually pay for — is structurally harder to flex than the orthodoxy assumes.

## 10. What would falsify the bottleneck thesis

The case built across sections 01-09 is that AI's binding 2026-2028 constraint is a chain of specific chokepoints — transformers, water, single-crystal blades, pipeline capacity, and grid governance — and that efficiency gains, while real, are outpaced by demand growth. The honest exercise is to specify what would falsify this. Four scenarios would meaningfully soften the bottleneck.

**Scenario A: Algorithmic efficiency compounds faster than compute demand for three consecutive years.** The current ratio is 3x/year (efficiency) versus 5x/year (compute growth) — a 1.67x net annual demand increase [^41]. If efficiency breaches 5x/year sustained — through a combination of ultra-sparse MoE architectures (less than 1% active parameters), recursive distillation-in-the-loop, and novel attention mechanisms — the net demand growth goes to zero or negative. Watch two signals: whether DeepSeek-V5 or its equivalent delivers another 3-5x FLOP reduction over V4 (compound efficiency at that rate bends the curve), and whether any major hyperscaler guides FY27 capex *down* from FY26.

:::callout(kind=warn, label="What to watch")
DeepSeek-V5 architecture (late 2026/early 2027): if it delivers another 3-5x inference FLOP reduction, the compound effect of V3→V4→V5 would approach 10-20x — enough to materially affect power forecasts. Also: any explicit capex reduction guidance from Amazon, Microsoft, Alphabet, or Meta in the next two earnings cycles.
:::

**Scenario B: Large-load curtailment regimes proliferate at SB 6 speed.** Texas wrote a 75 MW threshold with ERCOT-administered curtailment into statute in eight months. If PJM, MISO, and CAISO converge on similar regimes by mid-2027 — and FERC's December 2025 colocation order provides the federal scaffolding — then the Norris et al. estimate of 98 GW of latent headroom at 0.5% curtailment becomes deliverable supply rather than a research finding. The key metric: how many gigawatts of hyperscaler load are under active curtailment contracts by year-end 2026.

**Scenario C: The overbuild thesis is right, and capex turns.** Nadella's "overbuild" comment [^55], TD Cowen's canceled-lease reports [^56], and the historical pattern of capacity cycles all point toward a correction. But Q1 2026 prints across all four hyperscalers raised guidance. The tell: if even one of the four guides FY27 capex *down* — or if data center vacancy rates in Northern Virginia, Phoenix, or Dallas cross above 10% from current near-zero levels — the demand wave loses its self-reinforcing quality. The distinction between "AI-ready" vacancy (high-density, liquid-cooled) and traditional vacancy matters; the former is the signal to watch.

**Scenario D: Federal emergency authority actually builds.** Trump EO 14156's stack of statutory hammers — DPA Section 303, ESA emergency consultation, 10 USC §2808 DoD construction authority — can site generation on federal land outside state PUC and county jurisdiction. The April 2026 DPA Section 303 determination on transformers is the signal that this lever is being warmed up. If the administration sites 5 GW of gas or restarts 3 GW of nuclear on military reservations by mid-2027, the governance bottleneck inverts: federal speed beats local veto.

:::callout(kind=danger, label="What would NOT falsify the thesis")
Claims that do not survive the evidence: that perf/W gains arrive in time to bend the 2026-2027 iron-on-order curve (calendar mismatch — the chips were ordered in 2024); that BTM gas scales to 50 GW without environmental backlash (xAI Memphis already shows the limit); that SMRs deliver before 2030 (zero operating new advanced reactor MW in the US, ~400 MW permitted); that the transformer supply deficit clears through market mechanisms (factories take 3-5 years to build, and the ones breaking ground now ship in 2029-2031).
:::

The default scenario — the one the evidence supports — is that the bottleneck persists through 2028, concentrated in transformers, water permits, turbine blade foundries, and the governance gap between US and APAC build speeds. The efficiency gains are the most powerful counter-force, but they are being routed through a Jevons rebound that expands total demand faster than per-unit efficiency improves. The next eighteen months of capex prints, FERC orders, transformer factory groundbreakings, and water-permit hearings will determine which scenario actually obtains.

This matters because the location of the bottleneck determines who wins. If the constraint is generation capacity, the advantage goes to the jurisdictions and companies that can build power plants fastest — utility-scale developers, oil majors with gas reserves, sovereign wealth funds with balance sheet. If the constraint is transformers and water, the advantage goes to the companies that locked in their orders earliest and the jurisdictions whose permitting processes are fast enough to clear the queue. The chokepoint is not one thing — and neither is the distribution of its consequences.

## 11. References

:::references
- {id: 1, title: "Global Gas Turbine Supply-Demand Analysis (citing Wood Mackenzie data)", url: "https://x.com/user/status/2051564015571362266", source: "Financial analyst citing Wood Mackenzie", date: "2025-12-30"}
- {id: 2, title: "GE Vernova Q1 2026 Earnings Call Read-Through", url: "https://x.com/user/status/2047322965444858333", source: "GE Vernova IR / financial analyst read-through", date: "2026-04-23"}
- {id: 3, title: "Mitsubishi Heavy Industries Q1 FY2025 Earnings Read-Through", url: "https://x.com/user/status/1962878228403486923", source: "MHI IR / financial analyst read-through", date: "2025-04-28"}
- {id: 4, title: "Siemens Energy Q1 FY2026 Earnings Call Read-Through", url: "https://x.com/user/status/2021687005059723484", source: "Siemens Energy IR", date: "2026-02-15"}
- {id: 5, title: "Transformer troubles: manufacturing and policy constraints hit US transformer supply", url: "https://www.woodmac.com/news/opinion/transformer-troubles-manufacturing-and-policy-constraints-hit-us-transformer-supply/", source: "Wood Mackenzie", date: "2025-08"}
- {id: 6, title: "Transformers in 2026: Shortage, Scramble, or Self-Inflicted Crisis?", url: "https://www.powermag.com/transformers-in-2026-shortage-scramble-or-self-inflicted-crisis/", source: "POWER Magazine", date: "2026"}
- {id: 7, title: "Cleveland-Cliffs announces new state-of-the-art Weirton transformer plant", url: "https://www.clevelandcliffs.com/news/news-releases/detail/644/cleveland-cliffs-announces-its-new-state-of-the-art", source: "Cleveland-Cliffs Inc.", date: "2026"}
- {id: 8, title: "Presidential Determination Pursuant to Section 303 of the Defense Production Act of 1950, as Amended, on Grid Infrastructure, Equipment, and Supply Chain Capacity", url: "https://www.whitehouse.gov/presidential-actions/2026/04/presidential-determination-pursuant-to-section-303-of-the-defense-production-act-of-1950-as-amended-on-grid-infrastructure-equipment-and-supply-chain-capacity/", source: "The White House", date: "2026-04-20"}
- {id: 9, title: "Transformer Market Size & Share Analysis (2026-2031)", url: "https://www.mordorintelligence.com/industry-reports/transformer-market", source: "Mordor Intelligence", date: "2026"}
- {id: 10, title: "NVIDIA H100 Datasheet and arXiv 2601.20115 GPU TDP trajectory analysis", url: "https://arxiv.org/abs/2601.20115", source: "arXiv / NVIDIA", date: "2026-01-27"}
- {id: 11, title: "AMD Instinct GPU specifications (Wikipedia table citing AMD datasheets)", url: "https://en.wikipedia.org/wiki/AMD_Instinct", source: "AMD / Wikipedia", date: "2026"}
- {id: 12, title: "Data center cooling: immersion, direct-to-chip, and air cooling limits", url: "https://en.wikipedia.org/wiki/Data_center_cooling", source: "Wikipedia / ASHRAE TC9.9", date: "2026"}
- {id: 13, title: "Power usage effectiveness (PUE) benchmarks", url: "https://en.wikipedia.org/wiki/Power_usage_effectiveness", source: "Wikipedia / industry data", date: "2026"}
- {id: 14, title: "Google Data Centers: Efficiency", url: "https://datacenters.google/efficiency/", source: "Google", date: "2026-05-17"}
- {id: 15, title: "AWS Sustainability: Water and Energy in the Cloud", url: "https://sustainability.aboutamazon.com/environment/the-cloud", source: "Amazon Web Services", date: "2025-04-01"}
- {id: 16, title: "ASHRAE TC9.9 Datacom Encyclopedia: Liquid Cooling Resilience", url: "https://tpc.ashrae.org/?cmtKey=fd4a4ee6-96a3-4f61-8b85-43418dfa988d", source: "ASHRAE TC9.9", date: "2026"}
- {id: 17, title: "NVIDIA GB200 NVL72 product page", url: "https://www.nvidia.com/en-us/data-center/gb200-nvl72/", source: "NVIDIA", date: "2026"}
- {id: 18, title: "The Peak Water Needs of AI Data Centers in the United States by 2030 (arXiv:2603.02705v2)", url: "https://arxiv.org/abs/2603.02705v2", source: "arXiv / academic research", date: "2026-03-03"}
- {id: 19, title: "AI Data Center Water Consumption Projections (arXiv:2601.06063)", url: "https://arxiv.org/abs/2601.06063", source: "arXiv / academic research", date: "2026-01-01"}
- {id: 20, title: "Datacenter liquid cooling: Microsoft's next-generation thermal management", url: "https://news.microsoft.com/innovation-stories/datacenter-liquid-cooling/", source: "Microsoft", date: "2025"}
- {id: 21, title: "Tucson City Council rejects Project Blue amid intense community pressure", url: "https://azluminaria.org/2025/08/06/tucson-city-council-rejects-project-blue-amid-intense-community-pressure/", source: "AZ Luminaria", date: "2025-08-06"}
- {id: 22, title: "Google Sustainability: Water Stewardship", url: "https://sustainability.google/", source: "Google", date: "2025-04-01"}
- {id: 23, title: "Siemens Energy Q2 FY2026 Earnings Release", url: "https://www.siemens-energy.com/global/en/home/press-releases/earnings-release-q2-fy-2026.html", source: "Siemens Energy", date: "2026-05-12"}
- {id: 24, title: "GE Vernova Q1 2026 Earnings Press Release", url: "https://www.gevernova.com/sites/default/files/gev_webcast_pressrelease_04222026.pdf", source: "GE Vernova IR", date: "2026-04-22"}
- {id: 25, title: "Wood Mackenzie Gas Turbine Price Forecast (analyst read-through)", url: "https://x.com/user/status/2039657483665342574", source: "Wood Mackenzie / financial analyst", date: "2025-05-30"}
- {id: 26, title: "IEEFA Report: Global gas turbine shortages add to LNG challenges", url: "https://ieefa.org/sites/default/files/2025-10/IEEFA%20Report_Global%20gas%20turbine%20shortages%20add%20to%20LNG%20challenges%20in%20Vietnam%20and%20the%20Philippines_October2025.pdf", source: "IEEFA", date: "2025-10-01"}
- {id: 27, title: "GE Vernova and Crusoe announce major 29-unit aeroderivative gas turbine deal", url: "https://www.gevernova.com/news/press-releases/ge-vernova-crusoe-announce-major-29-unit-aeroderivative-gas-turbine-deliver-ai-data-centers", source: "GE Vernova", date: "2025-07-22"}
- {id: 28, title: "DT Midstream Q1 2026 Earnings Call Transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/05/05/energy-transfer-et-q1-2026-earnings-transcript/", source: "DT Midstream / Motley Fool transcript", date: "2026-04"}
- {id: 29, title: "EIA Short-Term Energy Outlook: Natural Gas, May 2026", url: "https://www.eia.gov/outlooks/steo/report/natgas.php", source: "US Energy Information Administration", date: "2026-05-12"}
- {id: 30, title: "Chevron + Engine No. 1 + GE Vernova Power Foundry (up to 4 GW)", url: "https://engine1.com/wp-content/uploads/2025/01/2025-0127_FINAL-PRESS-RELEASE_EN1_CVX_GE_.pdf", source: "Engine No. 1 / Chevron / GE Vernova", date: "2025-01-28"}
- {id: 31, title: "CREA/GEM: China 2024 coal construction starts 94.5 GW, 356 GW wind+solar added", url: "https://energyandcleanair.org/wp/wp-content/uploads/2025/02/CREA_GEM_China_Coal-power_H2-2024_FINAL.pdf", source: "CREA / Global Energy Monitor", date: "2025-02-13"}
- {id: 32, title: "SASAC: SGCC 2024 grid investment surpassed RMB 600B", url: "http://en.sasac.gov.cn/2024/07/29/c_17563.htm", source: "SASAC / State Grid Corporation of China", date: "2024-07-29"}
- {id: 33, title: "Hami-Chongqing ±800 kV UHVDC commissioned", url: "https://english.news.cn/20250610/8643cf83a9ce4a75a52b4ef60865c001/c.html", source: "Xinhua", date: "2025-06-10"}
- {id: 34, title: "NDRC: Ten national data center clusters across eight EDWC hubs", url: "https://en.ndrc.gov.cn/news/mediarusources/202202/t20220218_1315947.html", source: "NDRC (China)", date: "2022-02-17"}
- {id: 35, title: "Xinhua: China intelligent computing 725.3 EFLOPS in 2024", url: "https://english.news.cn/20250217/3aa217e260d24515b7a3f66a5bb3a0da/c.html", source: "Xinhua", date: "2025-02-17"}
- {id: 36, title: "Energy in Japan / Energy in Singapore (Wikipedia energy sector overviews)", url: "https://en.wikipedia.org/wiki/Energy_in_Japan", source: "Wikipedia / various primary data", date: "2025-2026"}
- {id: 37, title: "Nuclear power in Japan: restart status", url: "https://en.wikipedia.org/wiki/Nuclear_power_in_Japan", source: "Wikipedia / JAIF data", date: "2024-11"}
- {id: 38, title: "Electricity sector in South Korea", url: "https://en.wikipedia.org/wiki/Electricity_sector_in_South_Korea", source: "Wikipedia / KEPCO data", date: "2024-12-31"}
- {id: 39, title: "Energy in Taiwan: nuclear phase-out complete May 2025", url: "https://en.wikipedia.org/wiki/Energy_in_Taiwan", source: "Wikipedia / Taipower data", date: "2025-05-18"}
- {id: 40, title: "Singapore data center moratorium and sustainability criteria", url: "https://en.wikipedia.org/wiki/Data_center#Energy_use", source: "Wikipedia / IMDA Singapore", date: "2022-04"}
- {id: 41, title: "Epoch AI: Trends in AI Compute, Algorithmic Efficiency, and Inference Pricing", url: "https://epoch.ai", source: "Epoch AI", date: "2026-05-17"}
- {id: 42, title: "DeepSeek-V4 mHC Efficiency Breakthrough (Epoch AI Notable Models database)", url: "https://epoch.ai/data/notable_ai_models.csv", source: "Epoch AI / DeepSeek technical report", date: "2026-04-24"}
- {id: 44, title: "The Rebound Effect in AI: Why Efficiency Gains Increase Total Energy Use (ACM FAccT 2025)", url: "https://arxiv.org/abs/2501.16548v2", source: "arXiv / ACM FAccT 2025", date: "2025-06-23"}
- {id: 45, title: "Jevons Paradox in Cloud Computing: A Thermodynamics Approach (arXiv:2411.11540v1)", url: "https://arxiv.org/abs/2411.11540v1", source: "arXiv", date: "2024-11-18"}
- {id: 46, title: "Structural Jevons Paradox in AI: Super-Elastic Compute Demand (arXiv:2601.12339v1)", url: "https://arxiv.org/abs/2601.12339v1", source: "arXiv", date: "2026-01-18"}
- {id: 47, title: "Can AI Scaling Continue Through 2030? (Epoch AI)", url: "https://epoch.ai/blog/can-ai-scaling-continue-through-2030", source: "Epoch AI", date: "2024-08-20"}
- {id: 48, title: "Nvidia CEO reveals 40% of data center revenue from inference", url: "https://www.cnbc.com/2024/03/19/nvidia-ceo-reveals-40percent-of-data-center-revenue-from-inference.html", source: "CNBC / NVIDIA", date: "2024-03-19"}
- {id: 49, title: "The AI Boom Could Use a Shocking Amount of Electricity", url: "https://www.scientificamerican.com/article/the-ai-boom-could-use-a-shocking-amount-of-electricity/", source: "Scientific American", date: "2024-06-19"}
- {id: 50, title: "DeepSeek API Pricing (official)", url: "https://api-docs.deepseek.com/quick_start/pricing", source: "DeepSeek", date: "2026-04-26"}
- {id: 51, title: "EIA Electric Power Monthly: Table 6.1 Utility-Scale Battery Storage", url: "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_6_01", source: "US Energy Information Administration", date: "2026-02-28"}
- {id: 52, title: "NREL 2024 Annual Technology Baseline: Utility-Scale Battery Storage", url: "https://atb.nrel.gov/electricity/2024/utility-scale_battery_storage", source: "NREL", date: "2024-06-01"}
- {id: 53, title: "Lithium Carbonate Commodity Price (Trading Economics)", url: "https://tradingeconomics.com/commodity/lithium", source: "Trading Economics", date: "2026-05-15"}
- {id: 54, title: "Google Carbon-Intelligent Computing System", url: "https://blog.google/inside-google/infrastructure/data-centers-work-harder-sun-shines-wind-blows/", source: "Google", date: "2020-04"}
- {id: 55, title: "Microsoft CEO says there is an overbuild of AI systems", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-ceo-says-there-is-an-overbuild-of-ai-systems-dismisses-agi-milestones-as-show-of-progress", source: "Tom's Hardware / Satya Nadella", date: "2025-11-03"}
- {id: 56, title: "Microsoft cancels up to 2 GW of data center projects (TD Cowen)", url: "https://www.datacenterdynamics.com/en/news/microsoft-cancels-up-to-2gw-of-data-center-projects-says-td-cowen/", source: "Data Center Dynamics / TD Cowen", date: "2025-02-24"}
- {id: 57, title: "ByteDance-backed Volcano Engine says Doubao model hits 120t daily tokens", url: "https://www.chinadaily.com.cn/a/202604/02/WS69ce3326a310d6866eb41733.html", source: "China Daily", date: "2026-04-02"}
- {id: 58, title: "Datacenter Spending Forecast Revised Upwards Yet Again", url: "https://www.nextplatform.com/compute/2026/02/09/datacenter-spending-forecast-revised-upwards-yet-again/4092103", source: "The Next Platform", date: "2026-02-09"}
:::
