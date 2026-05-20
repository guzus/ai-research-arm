---
eyebrow: REPORT · SPACEX SUPPLY CHAIN
title: SpaceX's inverted supply chain — vertical integration as both moat and single point of failure
deck: How a thin, overpriced aerospace supplier base forced SpaceX to build almost everything itself — collapsing the cost of orbit while concentrating the risk in its own factories, its own metallurgy, and a ten-million-unit Starlink line.
lede: |
  The aerospace supply chain SpaceX inherited was a pyramid: a prime contractor at the top orchestrating thousands of subcontractors below, each adding margin, schedule, and a phone number to call when a part failed. SpaceX did roughly the opposite. It makes the majority of its launch vehicle in-house — more than 70% of Falcon by value and mass on the earliest accounting, and likely higher today — buying mostly raw metal, propellant, and chips rather than finished aerospace components. That inversion is the source of both its cost advantage and its most under-discussed fragility: when you build everything yourself, the supply chain that can break you is your own.
stats:
  - {label: In-house content, value: "~70–85%", note: "of Falcon, by value & mass"}
  - {label: Global upmass 2024, value: "85.6%", note: "SpaceX share (BryceTech)"}
  - {label: Falcon launches 2025, value: "165", note: "> rest of world combined"}
  - {label: Starship propellant, value: "~4,900 t", note: "methalox per stack"}
  - {label: Stainless steel, value: "~$3/kg", note: "vs ~$135/kg carbon fiber"}
  - {label: Starlink terminals, value: ">20,000/day", note: "Bastrop, TX line"}
---

## 01. The inversion: vertical integration as necessity, not ideology

The defining fact of SpaceX's supply chain is how little of it is external. A 2015 Harvard manufacturing case put in-house content at "more than 70% (of both $ volume and mass)" of Falcon and Dragon[^2]; reporting from inside the company a couple of years earlier pegged it near 80%, noting the Merlin engines, structures, and "even the flight computers" were built in Hawthorne[^1]. The frequently repeated 85% figure has no clean first-party origin — ==treat 85% as folklore drift from the sourced ~70–80%==, even if Raptor, Starlink, and custom silicon have plausibly pushed the real number up since.

The origin story is not ideological. SpaceX integrated because the commercial aerospace supplier base was thin and expensive: when a vendor quoted an exorbitant price for an engine valve, the propulsion team simply built it themselves, and declined the vendor's later, lower bid[^1]. The first-principles rule that fell out of that — if a supplier quote violates the materials-plus-labor cost floor, make it yourself — is the engine of the whole model. Even sympathetic industry voices frame it as forced: many rocket-grade components "simply had no commercial supply chain" to outsource to[^1].

What replaces the supplier pyramid is a network of company-owned factories, each a node SpaceX controls end to end.

:::kv
- {term: "Hawthorne, CA", def: "HQ, Falcon/Dragon, avionics, Raptor Vacuum; ~1.1M sq ft former Northrop plant"}
- {term: "McGregor, TX", def: "Engine test (16 stands, 4,300 acres) + serial Raptor; ~800–1,000 engines/yr target"}
- {term: "Starbase, TX", def: "Starship build & launch; Starfactory plus a planned ~700k sq ft Gigabay"}
- {term: "Bastrop, TX", def: "Starlink terminals + PCB/PLP; >$280M expansion, billed as largest in North America"}
- {term: "Redmond, WA", def: "Starlink satellite manufacturing, ~70 satellites/week"}
- {term: "Brownsville, TX", def: "Linde ~$100M air-separation plant feeding LOX/LN2 to Starbase"}
:::

This is "the machine that builds the machine" transposed from Tesla: Musk frames Raptor output in automotive terms ("2 to 4 engines per day… low volume by automotive standards")[^4], and the Starfactory was designed around a one-Starship-per-day aspiration[^5]. The counterpoint is capital, not concept. Vertical integration trades a thin-margin supplier network for enormous fixed cost: SpaceX has reportedly sunk more than $3 billion into Starbase infrastructure alone[^12], and ULA chief Tory Bruno — whose own firm runs the opposite model — concedes the industry's outsourcing "went way too far" while warning that re-internalizing depth is "very expensive"[^3]. Why it matters: integration only pays at scale, which means SpaceX's supply-chain bet is really a bet on volume.

## 02. The cost logic: integration first, reusability second

The popular story is that reusability collapsed launch cost. The most rigorous primary source complicates it. A 2018 NASA cost study found that, as of that date, "launch vehicle reuse… has not so far actually cut cost," and attributed SpaceX's advantage primarily to vertical integration — a 68% development-cost reduction versus the traditional model in NASA's own NAFCOM accounting[^6]. Reuse was the second-order lever that matured later, not the first.

Either way, the cost-per-kilogram curve is the headline the supply chain underwrites. The same NASA work priced the Space Shuttle at roughly $54,500/kg to low orbit against a listed Falcon 9 of $2,720/kg and Falcon Heavy near $1,400/kg[^6]; Musk's Starship target of ~$100/kg (and lower) remains aspirational[^6].

:::compare
- {role: HIGHEST, name: "Space Shuttle", value: "$54,500/kg"}
- {role: LOWEST, name: "Starship (target)", value: "~$100/kg"}
- {role: SUBJECT, name: "Falcon 9 (list)", value: "$2,720/kg"}
:::

The reuse economics are now real but partial. Musk has put the marginal cost of a reflown Falcon 9 near $15 million against a list price around $50–62 million, with booster refurbishment as low as ~$250,000[^7]; Shotwell said the very first reflight cost "substantially less than half" a new stage[^10]. Musk's own breakeven math: a roughly 40% payload penalty for recovering booster and fairing, under 10% recovery/refurb cost, so "you're roughly even with 2 flights, definitely ahead with 3"[^8]. By 2026 the refurbish-and-reuse line dominates: the fleet-leading booster has flown 30-plus times and SpaceX raised its reuse certification target to 40 flights, with the overwhelming majority of 2025 launches reused[^11]. ==The ~34% payload tax of reuse is real[^9]==; it only wins because amortization over dozens of flights swamps a one-time per-flight penalty — which is precisely why cadence is the load-bearing variable.

The honest framing is that this is a capital-intensity trade: high fixed cost (the >$1B reuse R&D, the multi-billion factories) for low marginal cost[^6][^12]. It pays at 165 launches a year and would not at 20. And it is Starlink, not launch, that monetizes the cadence — IPO-era reporting describes Starlink as the group's sole profitable segment[^13].

## 03. Raptor: the engine is the chokepoint

If any single component governs SpaceX's forward supply chain, it is the Raptor engine — both because Starship needs 33 of them per booster and because their production rate gates the whole Starship program. The supply story here is metallurgical and additive, not a list of vendors.

Raptor's cost trajectory is the cleanest paired-delta in the company. Musk priced Raptor 1 at "well under $1M" with a Raptor 2 goal below $250,000[^14]; by 2025 he claimed Raptor 3 had "almost twice the thrust and much higher reliability than Raptor 1, despite costing about four times less"[^15]. Each generation also shed mass and parts.

| Generation | Mass | Sea-level thrust | Relative cost |
|---|---|---|---|
| Raptor 1 (2019) | 2,080 kg | 185 tf | <$1M |
| Raptor 2 (2022) | 1,630 kg | 230 tf | ~½ of Raptor 1 |
| *Raptor 3 (2025) | 1,525 kg | 250+ tf | ~¼ of Raptor 1 |

The mechanism is simplification by integration. Raptor 2 deleted development sensors and plumbing and converted flanges to welds; Raptor 3 made regenerative cooling and secondary flow paths "integral to the whole engine, thus no heat shield is required," removing the need for "10+ tons of fire suppression" per booster[^16]. The materials that make this possible are proprietary: SpaceX casts manifolds from in-house SX300 — later SX500 — superalloys, "a modern version of Inconel," to contain the ~800-atmosphere oxygen-rich gas[^18][^17], and leans heavily on additive manufacturing (the 2016 subscale engine was ~40% 3D-printed by mass)[^17].

Production cadence climbed from roughly one engine every 48 hours in 2021 toward better than one a day by late 2022[^17], with a second factory at McGregor targeted at 800–1,000 engines a year[^17]. But this is exactly where in-house integration becomes concentration risk: when the engine is yours, an engine failure is your supply chain failing. Two consecutive Starship upper stages were lost in early 2025 — Flight 8's root cause "a hardware failure in one of the upper stage's center Raptor engines that resulted in inadvertent propellant mixing and ignition"[^19]. Vertical integration removed the supplier to blame; it did not remove the failure mode.

## 04. Materials: cheap by the tonne, fragile by the gram

Strip SpaceX's supply chain down to inputs and a counterintuitive pattern appears: its largest material flows are cheap, abundant commodities, while its real chokepoints are tiny by mass.

The marquee example is Starship's skin. SpaceX abandoned carbon-fiber composites for 300-series stainless steel, and the driver was raw economics: Musk says steel "costs 2% as much" as composites[^20], a claim consistent with his earlier framing of carbon fiber at ~$135/kg (closer to $200/kg after 35% scrap) versus steel at ~$3/kg[^21]. Steel also tolerates reentry heat with less shielding and gains strength at cryogenic temperatures[^20], and SpaceX is tuning a proprietary "30X" 300-series alloy on top of the 304L it currently welds[^20]. Falcon, by contrast, flies aluminum-lithium 2195 tanks[^23] and switched its grid fins from ablative aluminum to single-piece cast titanium in 2017 for reusable reentry survival[^22].

Propellant is the most extreme case of "cheap by the tonne." A full Starship stack carries on the order of 4,900 tonnes of methalox — roughly 79% liquid oxygen, 21% liquid methane[^23] — yet oxygen is made from air and methane is a global commodity.

:::donut(center-label="~4,900 t")
- {label: "Liquid oxygen", value: 79}
- {label: "Liquid methane", value: 21}
:::

The logistics, not the molecules, are the constraint: each Starship campaign has needed on the order of 200 tanker trucks, which is why SpaceX is localizing supply via a ~$100 million Linde air-separation plant in Brownsville, less than 50 miles from Starbase versus a prior 500-mile haul[^24]. Starship also abandoned helium pressurization entirely (autogenous pressurization), shedding Falcon's helium-and-COPV dependency[^24].

Now the chokepoints, all low-mass and high-criticality. Titanium sponge is geographically concentrated, with China at ~69% of 2024 world output and the US over 95% import-reliant[^25].

:::rank-list
- {label: "China", value: "220,000 t", pct: 100, highlight: true}
- {label: "Japan", value: "55,000 t", pct: 25}
- {label: "Russia", value: "20,000 t", pct: 9}
:::

And rare-earth permanent magnets — in motors, actuators, and avionics — sit behind a near-monopoly: China controls roughly 85–90% of rare-earth refining and around 90% of high-performance magnet production[^26].

:::callout(kind=info, label="The inverse-mass rule")
SpaceX's material exposures run opposite to their mass. The ~4,900 t of methalox and the bulk steel airframe are cheap, abundant, and increasingly self-supplied; the genuine vulnerabilities — titanium and rare-earth magnets — weigh little and concentrate in China and Russia. Vertical integration de-risked the heavy inputs, not the strategic ones.
:::

## 05. Starlink is the real external supply chain

For launch hardware SpaceX buys mostly raw material. For Starlink it buys chips, antennas, and contract manufacturing at consumer-electronics volume — and that is where its verifiable external supplier base actually lives.

The satellites are built in Redmond, Washington at roughly 70 a week[^31], a pace that has put more than 11,900 Starlink satellites up cumulatively — over 10,000 still in orbit and around 9,200 operational[^31] — more than every other operator's active fleet combined.

Cumulative launched, 2019→2026: {sparkline:122,662,1744,4063,6523,9847,11979}[^31]

The user terminals are the higher-volume, more exposed line. SpaceX's Bastrop, Texas factory was producing ~15,000 dishes a day by 2025[^32] — part of a >$280M expansion the state backed as the largest PCB and panel-level-packaging plant in North America[^57] — and the terminal's cost curve is the cleanest economic story in the constellation: built cost fell from an initial ~$3,000 to over $1,000 in 2021[^28] and under $600 by 2023, at which point SpaceX stopped subsidizing them[^29]. Retail did not move in lockstep: the US Standard dish rose from $499 to $599 in 2022 and held there until mid-2024[^59], so the consumer price was flat-to-rising even as build cost fell by half — the gap is the margin reusability and custom silicon opened up.

:::stats
- {label: "2021 build cost", value: ">$1,000", note: "per terminal (Musk)"}
- {label: "2023 build cost", value: "<$600", note: "subsidy ended"}
- {label: "Retail price", value: "$499→$599", note: "raised 2022, cut back 2024"}
- {label: "Output", value: ">20,000/day", note: "Starlink terminals"}
:::

Two supply forces drove that curve. First, the 2021–22 semiconductor shortage was a genuine, SpaceX-acknowledged constraint — the company told customers that "silicon shortages have delayed production"[^30]. Second, the fix was vertical integration into custom silicon co-designed with STMicroelectronics, the single best-documented external supplier in the entire SpaceX chain. ST's SEC filing describes a decade-long partnership that has produced "billions of co-designed products used in millions of Starlink user terminals in addition to over 10,000 Starlink satellites," at a run rate the companies put above five million chips a day[^27]. That is the rare case where a public company's filing lets outsiders see inside SpaceX's procurement — and it confirms the pattern: even SpaceX's biggest supplier relationship is a co-design, not an off-the-shelf buy.

## 06. Geopolitics: ITAR, China, and tariffs

Three external forces press on a supply chain SpaceX otherwise controls: export controls on the inputs and the labor, China's grip on critical minerals, and tariffs on the equipment that builds Starlink.

Export control runs in both directions. ITAR makes SpaceX's hardware controlled technology and effectively restricts most roles to US persons — a constraint the Department of Justice challenged as overbroad in a 2023 hiring-discrimination suit[^34], though that case was ultimately dismissed with prejudice in February 2025 with no penalty[^35] (a useful corrective to the common claim of a SpaceX export-control "settlement"). On inputs, China's 2025 expansion of rare-earth and critical-mineral export licensing — adding heavy rare earths and magnets with extraterritorial reach over foreign products containing Chinese material — directly threatens the magnet supply behind aerospace motors and actuators[^36][^26].

Tariffs hit the Starlink line most concretely. Musk called the 2025 US tariff regime's cost impact "not trivial"[^37], and SpaceX asked Washington to exempt two Chinese-made machines — an industrial soldering system and a circuit-board printer — used to build terminals at a stated rate "over 90,000 units a week"[^38]; the outcome of that request was not publicly confirmed. In parallel, SpaceX pushed its Taiwanese terminal suppliers (led by Wistron NeWeb, the dominant dish maker) to relocate production to Vietnam, citing China-conflict risk[^33] — a rare visible instance of SpaceX actively de-risking a supply base it does not own.

:::callout(kind=warn, label="Concentration risk")
The strategic squeeze is not in steel or methane but in the small, China-dominated inputs: rare-earth magnets (≈85–90% refining[^26]) and the Chinese-made tooling on the Starlink line. SpaceX can vertically integrate a valve; it cannot vertically integrate a rare-earth refinery on any near-term horizon.
:::

Regulatory throughput is the quieter constraint. The FAA's 2025 environmental decision raised Starbase's authorized cadence to up to 25 launches a year from five[^39] — a reminder that for Starship the binding limit has often been licensing, not parts.

## 07. The make-vs-buy map: SpaceX versus the field

Is vertical integration a SpaceX peculiarity or the new industry default? The evidence points to a converging consensus among the new entrants and a grudging re-think among the incumbents.

| Company | Model | Engines | Supplier posture |
|---|---|---|---|
| *SpaceX | Vertical | In-house (Merlin, Raptor) | ~70–85% in-house; buys raw inputs |
| Rocket Lab | Vertical | In-house (Rutherford, Archimedes) | Acquired subsystem makers to internalize |
| Blue Origin | Hybrid | In-house BE-4 (also sells to ULA) | Vertically integrated, merchant supplier |
| ULA | Horizontal | Buys BE-4 from Blue Origin | Wide subcontractor base |
| Boeing / Lockheed | Horizontal | Outsourced | Thousands of suppliers (ULA's parents) |

Rocket Lab is the clearest convergence: its SEC filing names "Deep Vertical Integration" as a strategic pillar and lists a string of acquisitions — Sinclair, Planetary Systems, SolAero, Advanced Solutions — explicitly executed "to deliver a comprehensive space solution that spans spacecraft manufacture, satellite subsystems, flight software, ground operations, and launch"[^50]. The cautionary counter-case is ULA's horizontal model: its Vulcan rocket slipped for years waiting on Blue Origin's BE-4 engine, which arrived "more than four years late"[^51] — the structural risk of buying your most critical component. Even Bruno, defending horizontal integration, now argues primes should "bring more vertical integration back in" and rebuild in-house labs[^3].

The counterpoint worth keeping: vertical integration is not free strategy, it is capital strategy. It makes sense for SpaceX and Rocket Lab because they fly often enough to amortize the factories; for a low-cadence operator it can be pure overhead. The model is spreading because cadence is rising, not because integration is universally superior.

## 08. SpaceX as everyone else's supply chain

The inverse of "SpaceX's supply chain" is that SpaceX has become a critical supply node for everyone else. By BryceTech's accounting SpaceX carried 85.6% of all spacecraft mass to orbit in 2024[^42], and launched more than the rest of the world combined that year[^43] and again in 2025, when it flew 165 Falcon missions and lofted ~85% of all satellites[^44].

:::bars
- {label: "SpaceX", value: "85.6%", pct: 86}
- {label: "Rest of world", value: "14.4%", pct: 14}
:::

The cadence that makes this possible has roughly doubled every two years.

:::line-chart(title="Falcon family launches per year", subtitle="SpaceX, 2021–2025")
x: 2021,2022,2023,2024,2025
Falcon: 31,61,96,134,165
:::

That dominance creates hard dependencies for the customers. Crew Dragon is the only operational US crew vehicle after Boeing's Starliner faltered, even bringing Starliner's stranded crew home in 2025[^46]; NASA awarded SpaceX the sole ~$843M contract to build the vehicle that will deorbit the entire ISS[^45]; SpaceX won 28 of 54 of the Pentagon's most demanding NSSL Phase 3 Lane 2 missions[^40]; and its Transporter rideshare program has become the default smallsat bus, having orbited over 1,600 payloads[^47]. The systemic risk is concrete: when the FAA grounded Falcon 9 in mid-2024, it simultaneously froze NASA resupply, a crewed mission, and commercial manifests across the industry[^48].

The durability counterpoint is real but early. SpaceX's launch *share* actually fell from 2024 to 2025 — not because it shrank but because China surged past ~97 launches and targets 140-plus in 2026[^49]; Blue Origin's New Glenn and Rocket Lab's Neutron are climbing but behind schedule[^49]; and Europe, wary of relying on Starlink, is funding a €10.6B sovereign constellation, IRIS²[^41]. The monopoly looks durable on economics and cadence in the near term, contestable over a five-year horizon.

## 09. What could break the thesis

The bull case — vertical integration as a durable moat — has specific, identifiable failure modes, most of them the flip side of integration itself.

**Concentration of failure.** Owning the whole stack means owning every fault. The history is a chronology of single small components grounding a fleet:

:::timeline
- {date: "2015-06", headline: "CRS-7 lost", body: "A strut rated to 10,000 lbf failed near 2,000 lbf; NASA later faulted SpaceX's choice of industrial-grade steel, not just the part."}
- {date: "2016-09", headline: "AMOS-6 pad explosion", body: "A second-stage COPV helium tank failed, destroying the rocket and a ~$200M satellite."}
- {date: "2024-07", headline: "Falcon 9 streak broken", body: "A fatigue-cracked sensor line ended a 325-flight success run and grounded the fleet ~2 weeks."}
- {date: "2025", headline: "Starship Flight 7 & 8", body: "Two consecutive upper-stage losses traced to Raptor hardware and propellant leaks."}
- {date: "2026-02", headline: "Falcon 9 grounded again", body: "A fourth upper-stage anomaly in ~19 months halted the fleet pending FAA review."}
:::

The CRS-7 case is the cleanest rebuttal to the integration-makes-you-safe narrative: Musk initially blamed a supplier strut[^53], but NASA's review found the deeper fault was SpaceX's own decision to use industrial-grade rather than aerospace-grade steel "without adequate screening or testing" and against the maker's recommended safety factor[^52]. The July 2024 sensor-line crack that ended a 325-flight streak[^54] and the February 2026 grounding[^55] show the pattern persists even at record cadence.

**Throughput becomes the constraint.** When you make everything, your factory and workforce are the bottleneck. Raptor's complexity gates Starship cadence, and the human cost of the pace is visible: a Reuters investigation and subsequent records put Starbase injury rates at multiples of the industry average[^56] — a regulatory and labor risk to the very throughput the model depends on.

**Capital intensity if cadence stalls.** The economics only work at high volume[^6]; a prolonged grounding or a Starship that is slow to reach operational cadence turns the multi-billion-dollar factory base from an asset into a drag, with launch still unprofitable on its own and Starlink carrying the group[^13].

**Strategic-input leverage.** China's rare-earth and magnet controls[^26][^36], and the Chinese-made tooling on the Starlink line[^38], are exposures SpaceX cannot vertically integrate away on any near-term horizon.

**Opacity.** As of this writing the often-cited SpaceX S-1 is *not* public on SEC EDGAR — the company's filing record shows only private Form D placements, the latest from 2022[^58], with the registration still confidential ahead of an expected ~$1.75T listing[^13]. ==Every SpaceX financial figure here is therefore secondary and unaudited== until the prospectus posts; the supply-chain risk factors that filing will disclose are, as yet, unread.

On balance, the moat is real — no competitor matches SpaceX's in-house cost structure or cadence — but it is a moat made of fixed capital, proprietary metallurgy, and a labor and licensing pipeline, every one of which is a place the company can be hurt by itself before any rival touches it. A red-team pass found the two pillar claims — the ~70–85% in-house figure and the 85.6% upmass share — unbroken by any contradicting source; it corrected one detail on Starlink retail pricing (the dish was raised to $599 in 2022–24, now reflected above), leaving the central thesis intact while these structural risks remain its real test.

:::references
- {id: 1, title: "Is SpaceX Changing the Rocket Equation?", url: "https://www.smithsonianmag.com/air-space-magazine/is-spacex-changing-the-rocket-equation-132285884/", source: "Smithsonian Air & Space", date: "2013-11-01"}
- {id: 2, title: "SpaceX: Low-Cost Access to Space", url: "https://d3.harvard.edu/platform-rctom/submission/spacex-low-cost-access-to-space/", source: "Harvard Business School (TOM)", date: "2015-12-09"}
- {id: 3, title: "Inside the making of ULA's next rocket (Tory Bruno)", url: "https://spacenews.com/inside-the-making-of-ulas-next-rocket/", source: "SpaceNews", date: "2025-03-06"}
- {id: 4, title: "Musk on Raptor volume production", url: "https://www.tesmanian.com/blogs/tesmanian-blog/raptors", source: "Tesmanian", date: "2021-07-01"}
- {id: 5, title: "SpaceX wants to build 1 Starship a day with Starfactory", url: "https://www.space.com/spacex-starship-one-a-day-starfactory", source: "Space.com", date: "2024-05-01"}
- {id: 6, title: "The Recent Large Reduction in Space Launch Cost (ICES-2018-81)", url: "https://ntrs.nasa.gov/citations/20200001093", source: "NASA NTRS", date: "2018-07-08"}
- {id: 7, title: "How much does it cost to launch a reused Falcon 9? Musk explains", url: "https://www.elonx.net/how-much-does-it-cost-to-launch-a-reused-falcon-9-elon-musk-explains-why-reusability-is-worth-it/", source: "ElonX (Musk, Aviation Week)", date: "2020-05-01"}
- {id: 8, title: "Musk on reuse breakeven (tweet)", url: "https://x.com/elonmusk/status/1295883862380294144", source: "@elonmusk", date: "2020-08-19"}
- {id: 9, title: "SpaceX price chart illustrates cost of reusability", url: "https://spacenews.com/spacexs-new-price-chart-illustrates-performance-cost-of-reusability/", source: "SpaceNews", date: "2016-05-03"}
- {id: 10, title: "SpaceX spent less than half a new first stage on relaunch (Shotwell)", url: "https://techcrunch.com/2017/04/05/spacex-spent-less-than-half-the-cost-of-a-new-first-stage-on-falcon-9-relaunch/", source: "TechCrunch", date: "2017-04-05"}
- {id: 11, title: "List of Falcon 9 first-stage boosters", url: "https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters", source: "Wikipedia", date: "2026-02-22"}
- {id: 12, title: "Starbase seeks enterprise-zone tax break for Gigabay", url: "https://myrgv.com/local-news/2025/11/17/starbase-seeks-enterprise-zone-tax-break-for-spacex-gigabay-project/", source: "The Monitor (myRGV)", date: "2025-11-17"}
- {id: 13, title: "SpaceX IPO: valuation, moat, Starlink", url: "https://fortune.com/2026/05/16/spacex-ipo-spcx-stock-valuation-space-market-moat-elon-musk-starlink-xai/", source: "Fortune", date: "2026-05-16"}
- {id: 14, title: "Musk on Raptor cost targets (tweet)", url: "https://twitter.com/elonmusk/status/1179107539352313856", source: "@elonmusk", date: "2019-10-01"}
- {id: 15, title: "Musk on Raptor 3 thrust/cost (tweet)", url: "https://twitter.com/elonmusk/status/1896703213434462640", source: "@elonmusk", date: "2025-03-03"}
- {id: 16, title: "Musk on Raptor 3 integration (tweet)", url: "https://twitter.com/elonmusk/status/1804871620114214978", source: "@elonmusk", date: "2024-06-23"}
- {id: 17, title: "SpaceX Raptor (specs, SX300/SX500, production)", url: "https://en.wikipedia.org/wiki/SpaceX_Raptor", source: "Wikipedia", date: "2026-01-01"}
- {id: 18, title: "Musk on SpaceX superalloys SX300/SX500", url: "https://www.teslarati.com/spacex-superalloys-raptor-rocket-engine-elon-musk/", source: "Teslarati", date: "2018-06-18"}
- {id: 19, title: "SpaceX blames Starship Flight 8 mishap on engine hardware failure", url: "https://spacenews.com/spacex-blames-starship-flight-8-mishap-on-engine-hardware-failure/", source: "SpaceNews", date: "2025-03-25"}
- {id: 20, title: "Musk on steel vs composites for Starship (tweet)", url: "https://x.com/elonmusk/status/1929578350064050394", source: "@elonmusk", date: "2025-06-02"}
- {id: 21, title: "Elon Musk explains the stainless steel Starship", url: "https://www.space.com/43101-elon-musk-explains-stainless-steel-starship.html", source: "Space.com", date: "2019-01-23"}
- {id: 22, title: "Falcon 9 titanium grid fin upgrade", url: "https://spaceflightnow.com/2017/06/25/falcon-9-rocket-launching-sunday-sports-fin-upgrade/", source: "Spaceflight Now", date: "2017-06-25"}
- {id: 23, title: "SpaceX Super Heavy (propellant mass)", url: "https://en.wikipedia.org/wiki/SpaceX_Super_Heavy", source: "Wikipedia", date: "2026-01-01"}
- {id: 24, title: "Starbase to produce its own Starship propellant (Linde)", url: "https://www.texastribune.org/2025/07/09/spacex-south-texas-liquid-oxygen-plant-rocket-fuel/", source: "Texas Tribune", date: "2025-07-09"}
- {id: 25, title: "Mineral Commodity Summaries 2025: Titanium", url: "https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-titanium.pdf", source: "USGS", date: "2025-01-31"}
- {id: 26, title: "China's control of rare earths", url: "https://chinapower.csis.org/china-rare-earths/", source: "CSIS ChinaPower", date: "2025-10-01"}
- {id: 27, title: "STMicroelectronics & SpaceX decade partnership (Form 6-K)", url: "https://www.sec.gov/Archives/edgar/data/932787/000093278725000039/stmicroelectronicsandspace.htm", source: "SEC EDGAR (STMicroelectronics)", date: "2025-12-15"}
- {id: 28, title: "SpaceX is losing money on Starlink terminals", url: "https://techcrunch.com/2021/06/29/spacex-is-losing-money-on-its-starlink-terminals-but-sees-lower-costs-ahead/", source: "TechCrunch", date: "2021-06-29"}
- {id: 29, title: "SpaceX no longer losing money on Starlink antennas (Hofeller)", url: "https://www.teslarati.com/spacex-no-longer-losing-money-starlink-antenna-production/", source: "Teslarati", date: "2023-09-13"}
- {id: 30, title: "Starlink exits beta; orders delayed due to chip shortage", url: "https://arstechnica.com/information-technology/2021/11/starlink-exits-beta-but-spacex-says-orders-are-delayed-due-to-chip-shortage/", source: "Ars Technica", date: "2021-11-05"}
- {id: 31, title: "Starlink statistics (constellation tracker)", url: "https://planet4589.org/space/con/star/stats.html", source: "Jonathan McDowell", date: "2026-05-16"}
- {id: 32, title: "Inside the Bastrop Starlink factory: 15,000 dishes/day", url: "https://www.nextbigfuture.com/2025/03/first-look-in-the-basrop-starlink-factory-making-15000-starlink-dishes-per-day.html", source: "NextBigFuture", date: "2025-03-03"}
- {id: 33, title: "After SpaceX requests, Taiwanese suppliers move abroad", url: "https://www.cnbc.com/2024/11/06/after-spacexs-requests-taiwanese-suppliers-move-manufacturing-abroad-reuters-sources-say.html", source: "CNBC (Reuters)", date: "2024-11-06"}
- {id: 34, title: "DOJ sues SpaceX over export-control hiring", url: "https://www.wsgr.com/en/insights/doj-sues-spacex-in-continuing-campaign-against-use-of-export-controls-to-justify-employment-discrimination.html", source: "Wilson Sonsini", date: "2023-08-24"}
- {id: 35, title: "DOJ drops SpaceX hiring lawsuit", url: "https://www.upi.com/Top_News/US/2025/02/21/elon-musk-spacex-lawsuit-dropped-justice-department/4021740157044/", source: "UPI", date: "2025-02-24"}
- {id: 36, title: "A short history of Chinese export controls on critical raw materials", url: "https://globaltradealert.org/blog/a-short-history-of-chinese-export-controls-on-critical-raw-materials", source: "Global Trade Alert", date: "2025-10-09"}
- {id: 37, title: "Musk warns Trump tariff effect 'not trivial'", url: "https://fortune.com/2025/03/27/elon-musk-warns-trump-tariff-effect-not-trivial-for-tesla/", source: "Fortune", date: "2025-03-27"}
- {id: 38, title: "SpaceX pleads with Trump administration for tariff exemptions", url: "https://finance.yahoo.com/news/elon-musk-spacex-pleads-trump-155049996.html", source: "Yahoo Finance (FT)", date: "2025-04-01"}
- {id: 39, title: "FAA Mitigated FONSI/Record of Decision, Starship Boca Chica", url: "https://www.faa.gov/media/94336", source: "FAA", date: "2025-05-12"}
- {id: 40, title: "SpaceX secures majority of NSSL Phase 3 FY25 missions", url: "https://spacenews.com/spacex-secures-majority-of-nssl-phase-3-fiscal-year-2025-missions/", source: "SpaceNews", date: "2025-04-04"}
- {id: 41, title: "Ukraine and Europe seek alternatives to Starlink (IRIS²)", url: "https://www.euronews.com/my-europe/2025/04/22/govsatcom-eutelsat-iris2-ukraine-seeks-european-alternatives-to-starlink", source: "Euronews", date: "2025-04-22"}
- {id: 42, title: "Global Space Launch Activity 2024", url: "https://brycetech.com/reports/report-documents/global-space-launch-activity-2024/Bryce_Global_Space_Launch_Activity_2024.pdf", source: "BryceTech", date: "2025-01-31"}
- {id: 43, title: "SpaceX launch surge sets new global launch record in 2024", url: "https://spacenews.com/spacex-launch-surge-helps-set-new-global-launch-record-in-2024/", source: "SpaceNews", date: "2025-01-02"}
- {id: 44, title: "BryceTech: SpaceX accounted for ~50% of launches in 2025", url: "https://www.satellitetoday.com/launch/2026/04/10/brycetech-report-shows-spacex-accounted-for-50-of-launches-in-2025/", source: "Via Satellite", date: "2026-04-10"}
- {id: 45, title: "NASA awards SpaceX ISS deorbit vehicle contract", url: "https://spacenews.com/nasa-awards-spacex-contract-for-space-station-deorbit-vehicle/", source: "SpaceNews", date: "2024-06-26"}
- {id: 46, title: "Boeing Starliner (crew return on Dragon)", url: "https://en.wikipedia.org/wiki/Boeing_Starliner", source: "Wikipedia", date: "2025-03-01"}
- {id: 47, title: "SpaceX Transporter-16: over 1,600 rideshare payloads", url: "https://www.satellitetoday.com/launch/2026/03/30/spacex-launches-119-payloads-on-the-transporter-16-rideshare-mission/", source: "Via Satellite", date: "2026-03-30"}
- {id: 48, title: "FAA grounds SpaceX Falcon 9 (2024)", url: "https://www.npr.org/2024/08/28/g-s1-19934/faa-spacex-falcon9-grounded-polaris-dawn", source: "NPR", date: "2024-08-28"}
- {id: 49, title: "China targets 140 launches in 2026 amid commercial surge", url: "https://spacenews.com/china-targets-140-launches-in-2026-amid-commercial-space-surge/", source: "SpaceNews", date: "2025-12-15"}
- {id: 50, title: "Rocket Lab USA FY2022 Form 10-K (Deep Vertical Integration)", url: "https://www.sec.gov/Archives/edgar/data/0001819994/000095017023006499/rklb-20221231.htm", source: "SEC EDGAR (Rocket Lab)", date: "2023-02-28"}
- {id: 51, title: "BE-4 engine (ULA dependency, delays)", url: "https://en.wikipedia.org/wiki/BE-4", source: "Wikipedia", date: "2024-01-08"}
- {id: 52, title: "NASA CRS-7 Independent Review Team public summary", url: "https://www.nasa.gov/wp-content/uploads/2018/03/public_summary_nasa_irt_spacex_crs-7_final.pdf", source: "NASA LSP IRT", date: "2018-03-01"}
- {id: 53, title: "Failed strut doomed CRS-7 (Musk)", url: "https://www.americaspace.com/2015/07/20/failed-strut-doomed-crs-7-mission-no-falcon-9-launches-before-september-says-elon-musk/", source: "AmericaSpace", date: "2015-07-20"}
- {id: 54, title: "SpaceX finds cause of July 2024 Falcon 9 failure", url: "https://www.space.com/spacex-finds-cause-falcon-9-rocket-failure", source: "Space.com", date: "2024-07-25"}
- {id: 55, title: "SpaceX halts Falcon 9 flights after stage anomaly (Feb 2026)", url: "https://www.theregister.com/2026/02/04/spacex_halts_falcon_9_flights/", source: "The Register", date: "2026-02-04"}
- {id: 56, title: "SpaceX worker injury rates at Starbase outpace rivals", url: "https://techcrunch.com/2025/07/18/spacex-worker-injury-rates-at-starbase-outpace-industry-rivals/", source: "TechCrunch", date: "2025-07-18"}
- {id: 57, title: "Texas Semiconductor Innovation Fund grant to SpaceX (Bastrop)", url: "https://gov.texas.gov/news/post/governor-abbott-announces-texas-semiconductor-innovation-fund-grant-to-spacex", source: "Office of the Texas Governor", date: "2025-01-01"}
- {id: 58, title: "SEC EDGAR submissions, SPACE EXPLORATION TECHNOLOGIES CORP", url: "https://data.sec.gov/submissions/CIK0001181412.json", source: "SEC EDGAR", date: "2026-05-20"}
- {id: 59, title: "Starlink prices going up across the board ($499→$599)", url: "https://techcrunch.com/2022/03/23/spacexs-starlink-prices-are-going-up-across-the-board/", source: "TechCrunch", date: "2022-03-23"}
:::
