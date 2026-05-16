---
eyebrow: AI infrastructure
title: 'Creating a datacenter from scratch: what''s needed'
deck: The shell is the last 15 months of a five-year process. Power, water, and political consent are
  the gates that actually decide which gigawatts come online.
lede: A 2026 AI datacenter is no longer a real-estate project. It is a queue position with concrete attached.
  The slab, the cooling loop, and the GPU racks are downstream of a five-to-seven-year contest for substation
  capacity, transformer slots, regulatory approval, and TSMC packaging allocation. The operators winning
  this cycle are not the ones moving fastest on construction; they are the ones who locked in the gates
  first. This piece walks the build from the empty section of land to the running cluster, citing only
  primary filings, SEC reports, ISO/RTO documents, vendor specs, and engineering publications where they
  exist.
stats:
- label: Load seeking interconnection in ERCOT alone (~87% data centers)[^2]
  value: ~410 GW
- label: Average lead time for a large power transformer, Q2 2025[^4]
  value: '128 weeks'
- label: Total rack power of a single GB200 NVL72 — liquid cooling mandatory[^18]
  value: '132 kW'
- label: NVIDIA Data Center revenue, Q4 FY26[^50]
  value: $62.3B
- label: Meta FY26 capex guidance, raised on datacenter cost[^34]
  value: $125-145B
- label: CBRE H2 2025 primary-market vacancy — a record low[^14]
  value: '1.4%'
---

## 1. The hard prerequisites: why "from scratch" is the wrong frame

For a 2026 AI datacenter, the instinct to "start from scratch" — clear ground, pour slab, install racks — is the wrong mental model; the build is now gated by three pre-shovel prerequisites (firm power, water and cooling permissibility, and political consent) that consume four of every five years on the schedule, leaving the shell as the final 15-month sprint of a process that begins long before any earth is moved.

The power gate is the binding one. PJM, the largest US grid operator, is processing a transition queue of roughly 46 GW and reports that projects energized in 2025 averaged more than seven years from application to commercial operation[^1]. ERCOT's April 2026 large-load filing is more vivid: approximately 410 GW of load is seeking interconnection in Texas alone, of which about 87% is datacenter demand — a figure that exceeds the entire installed peak of the Texas grid several times over[^2]. A developer who closes on land in 2026 expecting utility power by 2028 is not building a datacenter; they are buying a lottery ticket.

This is why the marquee "greenfield" builds of 2025-2026 are, on inspection, not greenfield at all. xAI's Colossus in Memphis stood up roughly 100,000 GPUs in 122 days, but only because the team retrofitted a ~785,000 sq ft former Electrolux appliance plant rather than pouring a slab[^40], and even then resorted to a fleet of on-site gas turbines under a contested air permit to bridge the utility gap[^15]. Crusoe's Abilene site — the physical home of Stargate — broke ground in June 2024 and first energized in September 2025, a roughly 15-month shell-to-power timeline that was only achievable because the 1.2 GW campus is fed behind-the-meter by dedicated gas generation rather than waiting in the ERCOT queue[^39]. The pattern is consistent: speed is bought by sidestepping the interconnection queue, not by beating it.

:::callout(kind=info)
**The binding constraint.** In CBRE's H2 2025 survey, North American primary-market supply reached 9,432 MW (+36% year-over-year) with 5,994 MW under construction, yet vacancy collapsed to 1.4%[^14]. Record construction is being absorbed faster than it completes, which is only possible when the gating resource is energized megawatts, not square footage. The shell is no longer the product; the interconnection agreement is.
:::

The water gate has become nearly as hard, and faster-moving. In August 2025, Tucson's city council voted 7-0 to reject "Project Blue," a datacenter campus that would have consumed roughly 2,000 acre-feet per year of municipal water in a basin already in Tier 1 Colorado River shortage[^78]. The reference case operators want to avoid is Google's The Dalles facility, which drew 434.4 million gallons in 2024 — roughly one-third of the entire city's water supply, a disclosure forced only by litigation[^24]. Communities have learned to read the water-use disclosures, and "trust us on evaporative cooling" is no longer a viable permit narrative in arid jurisdictions.

Regulatory consent is the third gate, and it now moves on timescales that capex planners cannot model. Loudoun County, Virginia — the densest datacenter cluster on Earth — eliminated by-right datacenter zoning on March 18, 2025, forcing every new build into discretionary special-exception review[^11]. Ireland's CRU lifted its Dublin-region grid moratorium on December 12, 2025, but only conditionally: new datacenter connections must demonstrate at least 80% on-site or contracted renewable supply[^12]. Singapore's December 2025 DC-CFA2 allocation made just 200 MW available to the entire market — a single hyperscale campus' worth — with a 50% green-energy mandate attached[^13]. These are not local quirks; they are the new template.

The counterpoint deserves a hearing. Behind-the-meter gas, on-site solar-plus-storage, and small modular reactor PPAs are arguably collapsing the seven-year power timeline into something closer to two, and if SMRs deliver on their 2028-2030 commissioning promises, the interconnection queue may matter less than this section implies. It is also true that secondary markets (Indiana, Mississippi, Alberta) with friendly zoning and surplus power are absorbing the overflow that Loudoun and Dublin will not. The "from scratch" frame may be wrong in 2026 and right again in 2029.

Why it matters: the analyst who treats a 2026 AI datacenter project as a construction problem will underwrite the wrong risks, the wrong timeline, and the wrong counterparties. The real diligence questions are about utility queue position, water rights, and zoning history, none of which appear on a site plan.

## 2. The seven-year pipe: queues, transformers, turbines

The binding constraint on greenfield AI datacenters between now and 2028 is not capital and not generation MW in the abstract. It is the queue: the interconnection study line, the transformer and GSU build slot, and the gas-turbine factory delivery date. Every exotic workaround in the field — behind-the-meter gas, nuclear restart, SMR offtake — is a response to a five-to-seven-year physical pipe that capital cannot compress.

Start with the queues themselves. PJM's transition queue alone holds roughly 46 GW of generation seeking interconnection, and the average study-to-in-service interval for projects energizing in 2025 has stretched past seven years[^1]. ERCOT's large-load queue sits near 410 GW of requests, roughly 87% of which are data centers[^2]. MISO reports about 169 GW in its active generator queue, with 70 GW already approved but unbuilt and another 32 GW formally delayed[^3]. These are not paperwork backlogs; they are physical commitments to copper, steel, and right-of-way that have not been poured.

The second choke is iron. Wood Mackenzie's Q2 2025 supply-chain read clocks power transformers at **128 weeks** of lead time, generator step-up units (GSUs) at **144 weeks**, and even medium-voltage switchgear at **44 weeks**[^4]. A 500 MW campus needs multiple large power transformers and at least one GSU per generation tie-in; ordering today means energization in 2028 at the earliest, and that assumes the foundry slot holds. The third choke is the prime mover. GE Vernova has disclosed an **80 GW gas-turbine backlog stretching into 2029** and is effectively sold out through 2030, meaning a developer who decides today to self-generate cannot get a heavy-frame F or HA machine on site until the back half of the decade[^5].

| Constraint | Headline number | Practical earliest energization | Source |
|---|---|---|---|
| PJM generator interconnection | ~46 GW transition queue; >7-yr avg for 2025 in-service | 2031-2032 for new entrants | [^1] |
| ERCOT large-load queue | ~410 GW requested, ~87% datacenter | Throttled by SB-load rules; 2027+ | [^2] |
| MISO generator queue | ~169 GW active; 70 GW approved-unbuilt; 32 GW delayed | 2029-2030 for queued MW | [^3] |
| Power transformer | 128 weeks lead time | Order 2026 → online 2028 | [^4] |
| Generator step-up (GSU) | 144 weeks lead time | Order 2026 → online late 2028 | [^4] |
| Medium-voltage switchgear | 44 weeks lead time | Order 2026 → online 2027 | [^4] |
| Heavy-frame gas turbine | 80 GW backlog; sold out through 2030 | Order 2026 → on-site 2029-2030 | [^5] |
| Nuclear restart (Crane / TMI-1) | 835 MW, 20-yr Microsoft PPA | 2028 target | [^7] |
| SMR (Amazon-X-energy, Google-Kairos) | 5 GW by 2039; 500 MW first online 2030 | 2030+ at earliest | [^8], [^9] |

#### Workarounds and why they exist

Read in this light, the unusual deals of the past eighteen months are not strategy — they are queue arbitrage. Constellation's **Crane Clean Energy Center**, restarting the 835 MW Three Mile Island Unit 1 under a 20-year PPA with Microsoft, is attractive precisely because the interconnection rights, the GSU, and the switchyard already exist on site; the developer is paying for fuel and refurbishment, not a seven-year queue slot[^7]. Crusoe's 1.8 GW Wyoming campus with Tallgrass leans on stranded Rocky Mountain gas and integrated CCS for the same reason: behind-the-meter generation that bypasses the ISO study cycle entirely[^54].

Behind-the-meter, however, collides with cost-shift politics. FERC's November 2024 rejection of the Talen-AWS Susquehanna ISA amendment, over an alleged **$140M/yr** cost shift to other PJM ratepayers, made clear that simply co-locating a hyperscaler at a nuclear plant without a network upgrade does not get a free pass[^6]. Every behind-the-meter deal now has to be structured around that ruling.

SMRs are the favored 2030s answer, and the contracts are real: Amazon has put more than **$500M** into X-energy with a target of 5 GW of SMR capacity by 2039 and at least 300 MW with Dominion[^8]; Google has signed for 500 MW from Kairos Power with first units online in 2030[^9]. None of this helps the 2026-2028 crunch. SMRs are a decade-out hedge dressed as a near-term solution.

*Counterpoint:* renewables plus storage clear the queue faster in some ISOs and have visible price signals — LevelTen's Q4 2025 index puts solar P25 PPAs at $49/MWh in ERCOT, $81 in PJM, and $115 in ISO-NE[^10]. But intermittent generation with four-hour storage cannot underwrite a 24/7 training cluster's load factor without massive overbuild, and the same transformer and switchgear queues constrain renewable interconnection as well; the iron bottleneck is technology-agnostic.

**Why it matters:** if your model of AI buildout is "throw capex at it," you will miss the actual 2026-2028 binding constraint — a roughly seven-year physical pipe of queues, transformers, and turbines that determines which gigawatts come online, and therefore which labs and which hyperscalers can train the next generation of frontier models on schedule.

## 3. The shell, structural, and permitting critical path

Once a transformer is on order and the substation slot is locked, the bottleneck migrates from the grid to the jobsite. The modern AI shell is no longer a tilt-up warehouse with a raised floor; it is a heavily reinforced industrial structure with classified-grade compartments, water loops the size of municipal mains, and a labor profile closer to a refinery turnaround than to commercial real estate. In a market where four out of five contractors cannot staff craft positions, schedule risk has moved into concrete, steel, and tradespeople.

The first thing that breaks is the floor. Commercial code minimum is roughly 100 psf, and even legacy enterprise datacenters like Intel's are designed for around 350 psf[^80]. A liquid-cooled rack housing 120-250 kW of GPUs, plus its cold-plate manifold and reservoir, can deliver point loads in excess of 800 psf[^80] — enough to require thickened slabs, post-tensioned decks, or steel-framed mezzanines designed from scratch. Retrofits of older buildings frequently fail this single test, which is why most operators are now building new on greenfield sites or, like xAI in Memphis, gutting an industrial host (a former Electrolux appliance plant) where the existing slab and crane bays were already rated for heavy manufacturing[^40].

Speed is the second variable, and it has collapsed in a way the construction industry was not designed for. xAI's Colossus cluster reportedly went from empty shell to first training run in 122 days inside that Memphis retrofit[^40], and Crusoe's flagship Abilene campus — a 1.2 GW build with DPR Construction and Mortenson as the construction joint venture[^55] — broke ground in June 2024 and energized its first phase in September 2025, roughly fifteen months for a hyperscale-class facility[^39]. Those timelines are only achievable with parallel-path construction: foundations, structural steel, mechanical rough-in, and electrical gear all proceed simultaneously, which in turn requires thousands of trades on site at peak.

That is where the labor wall hits. The Associated General Contractors' 2025 Workforce Survey found that 82% of construction firms cannot fill craft positions, 77% specifically report electrician shortages, and 45% of projects have been delayed as a result[^56]. A 100+ MW campus typically needs 1,500-5,000 trades workers at peak — electricians, pipefitters, ironworkers, millwrights, controls technicians — in regions (West Texas, central Ohio, Phoenix exurbs) that have nowhere near that local workforce. The IBEW has responded by routing journeymen into datacenter work at $48-60/hr base in Northern Virginia, with top earners pulling $240,000-$280,000/year on overtime-heavy shifts[^57]. Wages that high are a tell: they are the clearing price of a structural shortage, not a cyclical bump.

:::callout(kind=info)
**The labor math.** 82% of US contractors cannot fill craft positions and 77% report electrician shortages[^56], even as IBEW journeymen on datacenter jobs earn $48-60/hr base and top out at $240,000-$280,000/year[^57]. A 100 MW AI campus needs 1,500-5,000 trades workers at peak in counties that often have a few hundred available. The constraint is no longer "can we build it" but "can we staff it" — and the answer is increasingly: only by paying double, only by training apprentices the operator funds itself, and only by accepting that the next site over will outbid you.
:::

Code overlays add a second layer of complexity that generic construction crews are not used to. NFPA 75, the standard for the fire protection of information technology equipment, governs separation, suppression (typically clean-agent or pre-action sprinkler), and compartmentation for IT spaces[^59], and it interacts awkwardly with liquid-cooling loops that introduce dielectric fluid and chilled-water risk into the same room as the suppression system. For workloads with a classified or sovereign-AI dimension, the relevant document is ICD 705, the Intelligence Community's Tech Specs for the construction and management of Sensitive Compartmented Information Facilities, currently at version 15[^60]. ICD 705 dictates wall construction, acoustic isolation, RF shielding, door hardware, and access control to a level of prescription that adds months to design review and requires cleared installers — a vanishingly small pool inside an already-tight trades market.

The counterpoint is that Washington has noticed. A July 2025 White House executive order directs federal agencies to accelerate permitting for qualifying datacenter infrastructure, including expanded NEPA categorical exclusions and faster reviews for transmission, water, and siting on federal land[^58]. That helps at the federal interface; it does nothing about local zoning hearings, county building departments, or the AGC's craft-labor gap. Permitting reform shortens the paper critical path; it does not pour concrete or pull conduit.

Why it matters: even with power secured and capital committed, the next 18-24 months of AI capacity are gated by slabs rated for 800 psf, by SCIF-grade compartments that take cleared trades to build, and by an electrician shortage that no executive order can paper over — meaning the operators who win this cycle are the ones who locked in construction joint ventures and labor agreements before the gigawatt orders landed.

## 4. Cooling: the death of air at 120 kW per rack

Air cooling is finished at the front of the AI cluster. A single NVIDIA GB200 NVL72 rack dissipates roughly 120-132 kW and ships with mandatory direct-to-chip liquid plumbing[^17], more than five times the thermal envelope that conventional perimeter-air halls were ever designed to absorb. Greenfield AI campuses no longer have the option of bolting cooling onto the building after the fact; the cold-plate manifolds, coolant distribution units (CDUs), and dry-cooler yards have to be committed to in the first design pass, and in arid markets they increasingly have to be closed-loop, accepting a higher electricity bill to eliminate evaporative water use.

The numerical jump is brutal. Supermicro's GB200 NVL72 datasheet lists 132 kW total rack power with a 125-135 kW operating band, fed by an in-rack 250 kW CDU specifically because the cold plates need redundant headroom over the IT load[^18]. The Register's teardown of NVIDIA's reference design pegs steady-state at ~120 kW per NVL72, with 25 °C inlet coolant flowing at 2 L/s, and notes that NVIDIA's choice of copper backplane over optics for the NVLink spine saved roughly 20 kW of in-rack heat that would otherwise have to be pulled out as well[^67]. At the pod level, NVIDIA's DGX SuperPOD reference architecture groups eight NVL72 racks into a single Scalable Unit dissipating about 2.1 MW with hybrid liquid-plus-air[^79] — meaning a 100 MW AI hall is, in cooling terms, roughly fifty of these units bolted together.

The industry has not caught up. Uptime Institute's 2025 cooling survey found that 75% of operators still rely on perimeter air as their primary method and only 22% have deployed direct liquid cooling at any scale, even though 67% of respondents agreed DLC becomes necessary above 20 kW per rack[^19]. The gap between "we know we need it" and "we have it" is the central operational problem of the 2026 buildout. Compounding it, Uptime's headline efficiency number — the global weighted-average PUE — has sat at 1.54 for six consecutive years[^20], suggesting the fleet's thermal architecture has essentially stopped improving while rack densities have gone vertical.

| Cooling technology | Practical kW/rack ceiling | Fits GB200 NVL72 (~120-132 kW)? |
|---|---|---|
| Perimeter / CRAC air | ~15-20 kW | No |
| Rear-door heat exchanger (Motivair ChilledDoor M4-M16) | 12-75 kW nominal | Partial / auxiliary only |
| Direct-to-chip liquid (in-rack CDU, e.g. Vertiv CoolChip) | ~120+ kW per CDU loop | Yes (design baseline) |
| Single-phase / two-phase immersion | ~150-250 kW | Yes, with rebuilt server form factor |

The middle rows of that table are where most retrofits live. Motivair's ChilledDoor rear-door heat exchanger family is rated from 12 kW (M4) up to 75 kW (M16) nominal capacity[^21] — enough to take a dense CPU or H100 rack off the room air, but still short of a single NVL72. For full DLC, Vertiv's CoolChip in-rack CDU pushes 121 kW at 120 L/min with a 4 °C approach temperature difference[^22], almost exactly sized to one NVL72 — and that one-to-one ratio is what forces the rack-and-row layout of the entire hall, including pipe gallery widths, leak-detection trays, and the secondary loop out to dry coolers or cooling towers.

Water becomes the second design axis. Google's The Dalles campus drew 434.4 million gallons in 2024, roughly one third of the city's total water consumption[^24], the kind of disclosure that is now closing siting options in Arizona, Spain, and the Gulf. Microsoft's August 2024 "zero-water" design, deploying from 2026, replaces evaporative cooling with a closed chip-to-chiller loop that the company says avoids more than 125 million litres of water per site per year and targets a water-usage effectiveness of 0.30 L/kWh[^23].

**Counterpoint.** Closed-loop is not a free lunch. Eliminating evaporation means rejecting heat sensibly to air through dry coolers or refrigerant chillers, which on a 40 °C summer day pushes condensing temperatures up and pulls PUE the wrong way; Microsoft's own framing of the design as a deliberate trade-off — water saved at the cost of more electricity — is the honest version[^23]. Equally, the Uptime data is a reminder that the median datacenter is not a GB200 hall: three quarters of operators are still air-cooled[^19], and an enormous installed base of 10-20 kW colocation cabinets will continue to run on CRAC units for years, because the tenants in them are running storage, networking, and inference on lower-density silicon that simply does not need a cold plate.

**Why it matters.** Cooling is no longer a facilities line item; it is a determinant of which chips a campus can host. A site designed around 20 kW air-cooled cabinets cannot, in practice, accept an NVL72 tenant without ripping out the floor — the 120 kW figure[^67] is six times the 20 kW threshold at which Uptime's own respondents say liquid becomes mandatory[^19]. For a developer making a multi-year capex commitment in 2026, the cooling architecture — DLC manifold pitch, CDU redundancy, dry-cooler yard area, and the water-vs-power posture for the local climate — has to be frozen before the slab is poured, because every one of those decisions is downstream of a chip roadmap that has already left air cooling behind.

## 5. The compute stack: silicon, fabric, and the CoWoS bottleneck

A finished building with megawatts on the busbar is inert without accelerators, and filling it with usable AI silicon is a separate, equally constrained problem. NVIDIA's Q3 FY26 Data Center revenue hit $51.2 billion, up 66% year-over-year, with management stating that Blackwell was "sold out"[^49]; one quarter later, Data Center revenue grew again to $62.3 billion, Rubin was formally announced as the successor architecture, and NVIDIA disclosed a multi-million-GPU partnership with Meta alongside the unveiling of next-generation systems[^50]. The binding constraint behind those numbers is not customer demand or cash, but TSMC CoWoS advanced packaging capacity and SK Hynix HBM allocation: SK Hynix reported in Q3 2025 that its DRAM and HBM lines were "effectively sold out" through 2026, with HBM4 mass production beginning in September 2025[^52]. A new datacenter operator placing a Blackwell order today is, in practice, queuing for packaging substrates and stacked memory that were allocated 12-18 months earlier.

The unit economics make the scarcity legible. A GB200 NVL72 rack — 72 Blackwell GPUs plus 36 Grace CPUs in a single liquid-cooled cabinet — lists around $3 million, working out to roughly $60,000-$70,000 per superchip fully equipped[^33]. That rack is not just dense compute; it is a single 72-GPU NVLink domain delivering 1.8 TB/s per GPU and 130 TB/s of all-to-all bandwidth inside the cabinet, a design NVIDIA contributed to the Open Compute Project to encourage ecosystem adoption[^25]. Fifth-generation NVLink extends the same coherent fabric to a 576-GPU domain at more than 1 PB/s of aggregate bandwidth, which is the practical unit for training trillion-parameter models without paying the latency tax of crossing into the slower scale-out network[^26].

Outside the NVLink island, networking has quietly become 10-20% of cluster capex, and topology choice determines whether the GPUs are actually utilized. The canonical pattern is a rail-optimized fat-tree, in which each GPU within a server connects to a dedicated leaf switch ("rail") so that same-rank GPUs across the cluster reach each other with minimal hops; SemiAnalysis documents that real 100,000-GPU H100 fabrics run roughly 7:1 oversubscription between islands to keep the build affordable[^30]. Meta's two 24,576-H100 GenAI clusters illustrate the two viable scale-out stacks — one built on RoCE Ethernet, the other on InfiniBand, both at 400 Gbps per port — explicitly to de-risk vendor concentration[^28]. xAI's Colossus pushed the Ethernet path further, deploying NVIDIA Spectrum-X across roughly 100,000 GPUs and reporting 95% effective throughput against a 60% baseline for conventional Ethernet — the difference between a cluster that trains and a cluster that stalls on collectives[^27].

The switch silicon itself is on the same exponential. Broadcom's Tomahawk 6, announced at 102.4 Tbps of switching capacity, makes 128,000-XPU clusters reachable in just two tiers of switching, and its Davisson co-packaged optics option cuts optical-interconnect power by roughly 70% versus pluggable transceivers[^29]. That power saving is not cosmetic: in a gigawatt-class building, optics can account for a double-digit percentage of total IT load, and removing it directly buys back GPU headroom under the same utility contract.

A credible second source of accelerators is finally emerging, but slowly and largely captive. AWS's Project Rainier brings roughly 500,000 Trainium2 chips online for Anthropic in a single coordinated buildout[^42], and the broader Anthropic-Amazon agreement commits more than $100 billion over ten years and up to 5 GW of Trainium2/3/4 capacity[^51]. Google's TPU line and AMD's MI355/MI450 roadmap round out the alternatives. The counterpoint, however, is that none of these chips are sold on the open merchant market the way Hopper and Blackwell are: Trainium is consumed almost entirely inside AWS for AWS or Anthropic workloads, TPUs are rentable but not purchasable, and AMD's installed base remains a single-digit share of frontier training. For a third-party datacenter operator signing a tenant today, "diversifying away from NVIDIA" usually means hosting someone else's NVIDIA gear, not buying alternative silicon.

| Hyperscaler | Primary accelerator | Merchant access |
|---|---|---|
| Microsoft / Oracle / CoreWeave | NVIDIA Hopper, Blackwell, Rubin | Available (subject to allocation) |
| AWS | Trainium2/3/4 (Anthropic); NVIDIA for general tenants | Trainium captive; NVIDIA rentable |
| Google | TPU v5/v6 internal; NVIDIA for GCP customers | TPU rentable, not for sale |
| Meta | NVIDIA H100/Blackwell + internal MTIA | Fully captive |

**Why it matters:** a datacenter operator can pour the slab, energize the substation, and pipe the cooling loops on schedule and still miss the window if HBM and CoWoS allocations are not locked in years ahead. The compute stack has become its own seven-year pipe — only the gating utility is TSMC and SK Hynix instead of the local grid, and the contract you need is a GPU allocation letter, not a power purchase agreement.

## 6. Reliability reinvented: why AI training doesn't want Tier IV

The reflex assumption among datacenter buyers is that more nines is always better — that a Tier IV, 2N fault-tolerant facility is the gold standard and a Tier III concurrently-maintainable shell is the merely-acceptable floor. That mental model, codified by the Uptime Institute's four-level Tier classification[^44], was built for enterprise IT and colocation, where any outage translates directly into lost transactions. AI *training* is a different animal: failures are not exceptional events to be engineered out at the facility layer, they are the steady-state condition that the software stack is explicitly designed to absorb. Hyperscalers building greenfield training campuses are therefore self-spec'ing past Tier IV in some dimensions (power density, liquid cooling, control-plane redundancy) and deliberately below it in others (no 2N UPS for every GPU rack), because the marginal dollar buys far more reliability in software than in switchgear.

The numbers behind this shift are stark. Meta's published analysis of a 16,384-GPU Llama 3 training cluster reports a mean time to failure of roughly 7.9 hours at the 1,024-GPU scale, and projects MTTF collapsing to about 0.23 hours — under 14 minutes — for a hypothetical 131,072-GPU job; across the observed run, only 0.2% of jobs but 18.7% of runtime were directly impacted by interruptions[^46]. No facility-level redundancy scheme remedies that. A 2N electrical topology can keep the room energised through a utility blip, but it cannot keep a single failing HBM stack, a flaky NVLink, or a degraded optical transceiver from killing a synchronous all-reduce. The dominant failure modes are inside the rack, not upstream of it, so spending 60-80% more in capex for Tier IV power and cooling — roughly the premium Tier IV commands over Tier II in current market surveys[^48] — buys vanishing reliability gains for a training job whose practical availability is governed by GPU silicon, not switchgear.

Where the reliability budget actually pays off is in the control plane and the checkpoint pipeline. Google's Borg paper documents 99.99% Borgmaster availability achieved via Paxos-replicated state across five replicas, with the cluster scheduler engineered to survive machine, rack, and zone failures without operator intervention[^47]. Meta's MAST scheduler and the checkpoint/restart machinery around it embody the same philosophy at training scale: assume nodes die, snapshot frequently, restart from the last good checkpoint, and let the orchestrator route around the corpse[^46]. Reliability is moved from the facility to the distributed system, where it can be tested, versioned, and improved with every release — unlike a static-transfer switch, which is essentially frozen at commissioning.

The Uptime Institute itself has quietly aligned with this reality. The widely-cited "expected downtime per year" numbers (28.8 hours for Tier II, 1.6 hours for Tier III, 26.3 minutes for Tier IV) were formally removed from the Tier Standard in 2009; Uptime now stresses that the classification is a topology and capability framework, not a service-level guarantee[^45]. That semantic correction matters: training operators were never going to hit those availability targets at the *job* level anyway, and pretending the Tier number maps to job uptime obscured the real engineering trade-off. The new rack power envelopes make the trade-off even sharper. Open Compute Project specifications, most visibly the Mt Diablo 400/800 VDC rack family co-developed by Meta, Microsoft, Google, and Nvidia, contemplate distribution at 100 kW to 1 MW per rack[^81]; replicating that on a strict 2N basis would roughly double the substation, the busway, and the cooling loop for every megawatt of IT load, and most of that redundancy would sit idle protecting workloads that can already tolerate a node loss.

:::callout(kind=info)
**The MTTF math, made concrete.** At 1,024 GPUs, Meta observed MTTF of 7.9 hours; their scaling model projects 0.23 hours at 131,072 GPUs[^46]. A Tier IV facility targeting 26 minutes of annual downtime contributes negligibly when the job itself fails every 14 minutes. The reliability lever that actually moves the needle is a Paxos-replicated control plane delivering 99.99% scheduler availability[^47] plus aggressive checkpointing — a software investment, not a switchgear one.
:::

The counterpoint is that not all GPU capacity is training capacity. Inference fleets serving paid API traffic or latency-bound consumer products behave like classical revenue-bearing systems: every minute of unavailability is measurable lost revenue and contractual SLA exposure, and there is no checkpoint to restart from when a user request times out. For those workloads the older Tier III / Tier IV logic still holds, and operators are visibly bifurcating their estates — training campuses built to a leaner, software-resilient spec; inference halls retained at concurrent-maintainable or fault-tolerant topologies, often colocated with existing enterprise zones[^44]. The interesting design question for the next generation of campuses is whether to physically segregate the two or to build a single shell with zoned reliability tiers, accepting the operational complexity in exchange for capex flexibility.

**Why it matters.** The 60-80% Tier IV premium[^48], compounded across the multi-gigawatt training buildouts described earlier in this article, is one of the largest discretionary line items in a hyperscale capex plan. Recognising that training reliability is a software problem, not a facility problem, frees that capital to be redeployed into more megawatts, denser racks, and better checkpoint storage — which is exactly where the marginal training-throughput dollar belongs.

## 7. Software-defined operations: from DCIM to autonomous cooling

A modern AI datacenter is a cyber-physical system whose software stack — DCIM, BMS/SCADA, predictive maintenance, branch-circuit metering, Kubernetes and Slurm GPU schedulers, OpenBMC and Redfish out-of-band management, and OT cybersecurity overlays — is now as deep and as load-bearing as the concrete, copper, and coolant beneath it. Without it, a 100 MW campus cannot be operated to the SLAs hyperscale tenants demand; with it, the cognitive load on human operators falls dramatically even as the minimum 24/7 floor coverage stays stubbornly fixed.

The most-cited proof point remains Google DeepMind's intervention in Google's own production cooling plants. The 2016 deployment used a neural-network recommender that ingested thousands of sensor streams — temperatures, pump speeds, setpoints — and proposed operator actions that cut energy used for cooling by roughly 40% and reduced overall PUE overhead by about 15% across the facilities where it ran[^61]. Two years later the team closed the loop: an autonomous direct-control system began issuing setpoints to chillers and cooling towers itself, delivering an initial ~12% energy saving that climbed toward 30% as the model accumulated data, guarded by eight engineered safety mechanisms (action verification, two-layer rule-based constraints, real-time operator override, and uncertainty-gated fall-back to the legacy BMS)[^62]. The lesson for greenfield builders is not "buy an AI thermostat" but that the cooling plant must be instrumented and addressable from day one — every CRAH fan, every CDU pump, every facility-water valve exposed through BACnet/Modbus into a normalized DCIM data model — because retrofitting telemetry into a commissioned plant is far more expensive than designing it in.

:::callout(kind=info)
**Autonomous cooling, by the numbers.** Google's DeepMind cut cooling-energy use by 40% in recommendation mode and reduced overall PUE overhead by ~15%[^61]. In closed-loop autonomous mode, savings rose from 12% at launch toward 30% as the model accumulated data, behind eight engineered safety mechanisms[^62]. For a new build, the implication is architectural: every CRAH fan, every CDU pump, every facility-water valve must be exposed to a normalized data model from day one.
:::

One layer up, the scheduler is now a capacity-planning instrument, not just a job placer. AWS's Project Rainier — the multi-site Trainium2 cluster Anthropic is using to train and serve Claude — is explicitly designed so that the same silicon time-multiplexes workloads: Anthropic uses the majority of the chips for inference during daytime hours and shifts them to training overnight, on shared Trainium2 servers stitched together with NeuronLink and EFA fabrics[^42]. That kind of diurnal repurposing is impossible without a software-defined operations layer — Kubernetes or Slurm-class schedulers that can drain, checkpoint, and re-bind tens of thousands of accelerators on a predictable cadence, coupled to power-and-thermal telemetry so the facility team can pre-stage cooling and grid draw to the swing.

The hardware-management plane is being standardized in parallel. Open Compute Project specifications, most visibly the Mt Diablo 400/800 VDC rack family co-developed by Meta, Microsoft, Google, and Nvidia, push not only higher-voltage power distribution but a common out-of-band management surface so that a 100,000-GPU fleet can be inventoried, firmware-flashed, and health-polled with one toolchain rather than per-vendor BMCs[^81]. For a from-scratch operator this is a procurement decision with operational consequences: choosing OCP-compliant racks collapses what would otherwise be three or four parallel management stacks into one, which is how a single NOC can plausibly cover tens of megawatts.

The counterpoint is that none of this software has eliminated humans from the floor. Industry rules of thumb still put staffing for a Tier III/IV-grade 100 MW AI campus at roughly 30 to 80 full-time operations personnel — critical-facilities engineers on a 4-shift rotation, network and compute on-call, plus security and logistics — and that minimum is set by 24/7 physical coverage requirements (one qualified electrician and one mechanical tech per shift, two-person rules for medium-voltage work) rather than by cognitive workload, which is precisely the variable software does compress. The AGC's 2025 Workforce Survey found 82% of contractors reporting craft-labor shortages, which means the commissioning and ongoing maintenance bench is structurally thin even before the operator tries to hire[^56]. Microsoft's Project Natick offers the inverse cautionary tale: the Phase 2 underwater pod ran 864 servers at about 240 kW with a server-failure rate roughly one-eighth that of a matched land-based control group when retrieved in July 2020 — an astonishing reliability result attributed largely to a sealed, nitrogen-filled, human-free environment — yet Microsoft shuttered the program in 2024, indicating that pure-software, no-touch operation at production scale remains an aspiration rather than a deliverable[^66].

Finally, the OT-cybersecurity surface deserves its own line in the operations budget. Every Redfish endpoint, every BACnet gateway, every PLC on the chilled-water loop is now a network asset; segmenting the BMS/SCADA VLANs from the tenant compute fabric, enforcing signed firmware on BMCs, and logging every setpoint change into an immutable audit trail are table stakes for any campus that wants to sell capacity to a regulated AI customer.

**Why it matters:** the software stack is what converts a 100 MW shell full of GPUs into a sellable, auditable, dispatchable AI utility — autonomous cooling claws back 30-40% of the largest non-IT energy line item, OCP-standardized management collapses fleet operations onto one toolchain, and schedulers like those behind Project Rainier let the same silicon earn inference revenue by day and training revenue by night. The floor still needs humans, and the from-scratch operator who under-budgets either the software platform or the 24/7 staffing rota will discover the gap the first time a chiller trips at 3 a.m.

## 8. Capex and financing: what $40M per megawatt actually buys

The headline figure circulating in 2026 underwriting decks — roughly **$40 million per megawatt of IT load, all-in** for a frontier AI campus — is not a single line item but a stack of three distinct cost layers, financed through three distinct capital structures. Decomposing the number, and tracing the dollars back to audited filings rather than press-release totals, is the only way to separate what is being built from what is still a slide in a pitch deck.

Start with the shell. JLL's 2026 global outlook puts average shell-and-core construction at **$10.7M/MW in 2025, rising to $11.3M/MW in 2026**, with AI-grade fit-outs pushing total delivered cost as high as $25M/MW before any silicon is racked[^31]. Cushman & Wakefield's parallel survey of 19 US markets lands at **$11.7M/MW** for base build, and flags the violent inflation in electrical bill-of-materials: **switchgear pricing is up roughly 50% and standby generators up 45% since 2021**, driven by long lead times on medium-voltage gear[^32]. That inflation alone explains why a 2021 underwriting model produces fantasy numbers in 2026.

The second layer — mechanical and electrical fit-out tuned for 130-150 kW racks, including liquid-to-chip CDUs, busways, and N+1 UPS strings — adds another $4-8M/MW on top of the shell, with JLL pegging the upper bound of AI-specific fit-out as high as $25M/MW for the most aggressive direct-liquid-cooled designs[^31]. The third and largest layer is the IT itself. An NVIDIA **GB200 NVL72 rack lists around $3 million**, with individual GB200 superchips at $60-70k; a 100 MW hall populated end-to-end with NVL72s implies roughly **$2.0-2.5 billion of GPU capex alone**, or $20-25M/MW[^33]. Add the shell and fit-out and the $40M/MW headline reconciles cleanly.

| Layer | Cost per MW IT | What it buys | Source |
|---|---|---|---|
| Shell & core | $10.7-11.7M | Land, structure, substation tie-in, base MEP | [^31], [^32] |
| AI fit-out | $4-13M (up to $25M aggressive) | Liquid cooling, busways, switchgear, UPS | [^31] |
| GPU IT | $20-25M | ~7 GB200 NVL72 racks/MW @ ~$3M each | [^33] |
| All-in | $35-50M | Day-one operational AI hall | Composite |

Who is writing those checks? The first and dominant vehicle is hyperscaler self-funding from operating cash flow. **Microsoft committed roughly $80 billion of FY25 capex specifically to AI datacenters**[^35], and **Meta has guided to $125-145 billion for FY26** — a step-up that single-handedly reset the industry's capex baseline[^34]. These numbers come from audited 10-Ks and SEC-filed press releases, which is the reliable anchor for any serious financial model.

Two concrete projects illustrate where that money lands. Microsoft's **Fairwater campus in Mount Pleasant, Wisconsin**, has now passed **$7 billion in disclosed investment** ($3.3B initial plus a $4B expansion) for what it markets as the world's most powerful AI datacenter[^43]. Meta's Richland Parish, Louisiana facility — anchored by an Entergy commitment to build **2,260 MW of new gas generation** dedicated to the site — represents a **$27 billion Meta investment** in a single campus[^41]. At those scales the shell-versus-IT split inverts the historical norm: GPUs dominate the bill.

The second vehicle is the listed REIT channel (Digital Realty, Equinix), which historically built to ~$10M/MW economics and leased to enterprise tenants. That model is being out-scaled by the third and most interesting development: **GPU-collateralized debt**. In early 2026 CoreWeave closed an **$8.5 billion financing facility — the first GPU-backed debt to receive investment-grade ratings (A3 from Moody's, A-low from DBRS)**[^37]. This matters because it converts depreciating silicon into bankable collateral and unlocks a pool of insurance-company and pension capital that cannot touch sub-investment-grade paper.

Headline announcements should be read with more skepticism. **OpenAI's Stargate Project carries a $500 billion / four-year banner**[^38], but the figure aggregates intent across multiple partners (SoftBank, Oracle, MGX) and is paced by site-by-site groundbreakings. The most concrete piece is Crusoe's Abilene, Texas campus, which has expanded to **2.1 GW** and added a dedicated 900 MW AI factory for Microsoft alongside the original Stargate buildout — real concrete, but a fraction of the $500B headline[^36]. Treat the press-release total as a ceiling, not a forecast.

**Counterpoints worth underwriting.** First, the Stargate aggregate is partly aspirational: only the Abilene phases are funded and under construction, and contributors retain unilateral exit rights. Second, CoreWeave's investment-grade rating rests heavily on the credit quality of a small number of anchor offtake contracts, and a ratings downgrade of any single counterparty would propagate directly into the debt stack[^37]. Third, the GPU-as-collateral thesis assumes residual value; an entire generation of H100 inventory financed in 2023-24 now competes with Blackwell and Rubin pricing, and lenders are quietly marking residual curves steeper. A 100 MW hall of stranded H100s is not worth $2 billion in 2027.

**Why it matters.** The $40M/MW unit cost, multiplied by the gigawatts that Microsoft, Meta, Google, Amazon, and Oracle have already permitted, implies trillion-dollar cumulative AI infrastructure capex this decade. The math only closes if GPU IT retains useful economic life beyond the 4-6 year window today's financing models assume. Investors should anchor to audited hyperscaler 10-Ks[^34,35], treat headline consortium totals as aspirational ceilings[^38], and watch CoreWeave's facility[^37] as the leading indicator for whether GPU-backed debt becomes a genuine asset class or a one-cycle innovation.

## 9. The global buildout: sovereign capital and geographic arbitrage

Outside the United States, AI datacenter construction in 2025 was gated not by engineering but by a five-factor stack: access to sovereign capital, abundant cheap energy, regulatory speed, US export-control tier status, and an anchor offtake contract from a hyperscaler or frontier lab. The countries that cleared all five factors broke ground at gigawatt scale; those that missed even one stalled at the substation. The single most consequential geopolitical lever of the year was the Trump administration's May 2025 decision to lift chip-flow restrictions to the United Arab Emirates and Saudi Arabia, which immediately reordered where the next hundred gigawatts of frontier-class capacity would land.

The clearest demonstration of the new regime is Stargate UAE, announced in May 2025 as a joint venture between G42, OpenAI, Oracle, NVIDIA, Cisco, and SoftBank. The campus is sized at 5 GW with a first 1 GW Stargate cluster, making it the largest announced AI compute build outside the continental United States and a direct beneficiary of the relaxed export tiering[^69]. The deal pairs Emirati sovereign capital with a US hyperscaler anchor and US silicon, and it works only because Abu Dhabi can guarantee both gas-fired baseload and a regulatory fast-lane that no Western jurisdiction currently matches.

Capital formation at this scale is itself a new asset class. The BlackRock / Global Infrastructure Partners / Microsoft / MGX AI Infrastructure Partnership, launched September 2024, targets $30 billion in equity with a path to $100 billion once debt is layered on, and explicitly couples Abu Dhabi sovereign capital (MGX) with US asset managers and a hyperscaler offtaker[^72]. This is the template: Gulf LP capital, Western GP discipline, hyperscaler take-or-pay. Anywhere the template can be replicated, gigawatts follow.

Other jurisdictions are explicitly trying to import the same model with local adjustments. Singapore's Infocomm Media Development Authority opened its DC-CFA2 round in December 2025, allocating roughly 200 MW of new datacenter capacity under a mandate that at least 50% of the energy mix be green[^13]. The volume is modest by Gulf standards, but the signal matters: Singapore is reopening after a multi-year moratorium because it cannot afford to cede regional AI hosting to Johor and Batam. Ireland made the parallel pivot in the same month: the Commission for Regulation of Utilities ended the de facto Dublin grid-connection moratorium, conditioned on new datacenter loads being backed by at least 80% renewable supply[^12]. Both moves trade absolute carbon discipline for the right to stay in the AI infrastructure game.

The United Kingdom is betting on planning reform rather than sovereign capital. The government's AI Growth Zones policy, published in 2025, designates specific regions where datacenter projects receive accelerated planning consent and pre-cleared grid access, with the first zones anchored at Culham and (more recently) North Lanarkshire[^73]. It is a credible play for tier-two AI workloads but unlikely to attract frontier-cluster builds while UK industrial electricity prices remain among the highest in the OECD.

China is the structural counter-case. Cut off from leading-edge NVIDIA silicon, Beijing has been forced to vertically integrate. SemiAnalysis estimates Huawei will produce roughly 805,000 Ascend units in 2025, supplying close to 50% of Chinese AI datacenter accelerator demand[^74]. That is a genuine industrial achievement, but the same analysis flags a binding constraint: Ascend remains HBM-supply-limited, dependent on a narrow channel of Korean and increasingly domestic high-bandwidth memory that cannot yet match the volumes SK Hynix and Micron ship into Hopper and Blackwell. China can build the concrete and the power; it cannot yet build the memory stack at parity scale.

| Bloc | Capital source | Energy source | Regulatory speed | Chip access (post May 2025) |
|---|---|---|---|---|
| UAE | Sovereign (MGX, G42) | Gas + nuclear (Barakah) | Very fast | Tier-1 (lifted) |
| Saudi Arabia | Sovereign (PIF, HUMAIN) | Gas + solar | Fast | Tier-1 (lifted) |
| Singapore | Private + REIT | Imported / green-mandated | Constrained quota | Tier-1 |
| Japan | Corporate (SoftBank, KDDI) | Nuclear restart + LNG | Moderate | Tier-1 |
| India | Conglomerate (Reliance, Adani) | Coal + solar | Improving | Tier-1 |
| UK | Private + AI Growth Zones | Gas + offshore wind | Improving (zones) | Tier-1 |
| EU (Ireland) | Hyperscaler self-build | Wind (80% mandate) | Slow, just reopening | Tier-1 |
| China | State + provincial | Coal + hydro | Fast domestically | Restricted; Huawei Ascend |

The counter-arguments are real and stack-ranked. First, sovereign capital can dry up faster than it accumulates: a sustained oil-price collapse or a redirection of PIF and ADIA balance sheets toward domestic obligations would strand half-built Gulf campuses. Second, export-control tier status is reversible — what one US administration relaxed in May 2025, a successor or a single national-security incident could re-tighten, leaving Stargate UAE-class projects holding allocated but undeliverable GPUs. Third, China's Ascend ramp, however impressive at 805,000 units, remains HBM-constrained and therefore caps the ceiling on indigenous frontier training runs regardless of how much concrete and power Beijing pours[^74].

**Why it matters:** the geography of AI compute is no longer a function of where electricity is cheapest or where fiber lands. It is a function of which jurisdictions can simultaneously underwrite ten-figure equity checks, deliver multi-gigawatt power on a five-year timeline, push permits through in months rather than years, and sit on the right side of a US export-control line that is itself a policy variable. In 2025 only a handful of places cleared all four hurdles, and the resulting concentration of frontier compute in the Gulf, with secondary hubs in Singapore, Japan, and the UK, will shape who can train the next generation of models and who has to rent them.

## 10. What could break the thesis

The argument above — that an AI datacenter is a queue position with concrete attached, and that gigawatts will keep flowing into purpose-built campuses through the late 2020s — has at least four plausible failure modes. None is dispositive on its own, but each is supported by primary signals already in the public record, and any two combined would force a serious downward revision.

**Demand mean-reversion.** The most cited disconfirming datapoint of 2025 was a TD Cowen note alleging Microsoft had quietly walked away from up to 2 GW of US and international datacenter leases, suggesting capacity is being booked ahead of clear monetization paths[^76]. Construction-industry trackers picked up the broader pattern: datacenter project cancellations reportedly quadrupled to roughly 25 in 2025 from six in 2024, and Baird's read of the 2026 pipeline finds only about 5 GW of the 12-16 GW publicly announced is actually under construction[^75]. If a single foundation lab — OpenAI, Anthropic, xAI — misses a training run or fails a funding round, the take-or-pay assumptions underwriting Stargate-scale capex weaken fast.

**Silicon obsolescence cycles outrun depreciation schedules.** H100 spot rental rates fell ~44% year-over-year as Blackwell deployment ramped[^77]. Whole halls financed in 2023-24 on the assumption of 5-6 year H100 economic life now face a Blackwell-Rubin transition that the original models did not contemplate, and CoreWeave's $8.5B investment-grade GPU-backed facility[^37] rests on residual-value assumptions that will be tested in 2027 when Rubin ramps. If GPU residuals follow the curve of mining-era ASICs, the new debt class will reprice sharply.

**Permitting backlash, not just delay.** The pattern of 2025 community rejections is harder to dismiss as noise. Tucson's 7-0 vote against Project Blue[^78], Loudoun County's elimination of by-right zoning in the densest datacenter cluster on Earth[^11], and the NAACP-Earthjustice federal suit against xAI over 27 unpermitted gas turbines in Southaven[^16] are different jurisdictions reaching the same conclusion: the social license to build is being withdrawn faster than expansion plans can be revised. If EPA action closes the "portable/temporary" turbine loophole that some operators have leaned on, the on-site gas workaround disappears with it.

**Power-system limits convert into a regulatory ceiling.** FERC's November 2024 rejection of the Talen-AWS Susquehanna ISA amendment was rooted in an alleged $140M/yr cost shift to other PJM ratepayers[^6]; ERCOT now sits with ~410 GW of large-load requests pressing against a grid roughly an order of magnitude smaller[^2]. State legislatures will, at some point, decide whether residential ratepayers should subsidize hyperscaler load growth — and if the answer is no, "behind-the-meter" becomes the only legal pathway at exactly the moment EPA tightens the rules under which it can be built.

The honest read is that all four risks are bounded by the same underlying scarcity: there is more capital chasing AI compute than there are buildable sites, and whichever side of the trade you take, the binding constraint is the same five-year pipe of substations, transformers, and political consent. If demand mean-reverts, capital pulls back and the pipe relaxes. If demand holds, the pipe keeps biting and only the operators who locked in the gates first will deliver. The middle case — runaway construction without consequence — is the one the primary evidence is least supportive of.

## References

:::references
- id: 1
  title: PJM Interconnection Reform Progress fact sheet —
  url: https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/fact-sheets/interconnection-reform-progress-fact-sheet.pdf
- id: 2
  title: ERCOT Large Load Update, April 2026 Senate B&C briefing —
  url: https://www.ercot.com/files/docs/2026/04/01/ERCOT_LargeLoad_Update_April2026_B-C_-Hearing.pdf
- id: 3
  title: 'MISO System Planning Committee 9 Dec 2025: Resource Adequacy and Generator Interconnection Queue
    Update —'
  url: https://cdn.misoenergy.org/20251209%20System%20Planning%20Committee%20of%20the%20BOD%20Item%2005%20Resource%20Adequacy%20and%20Generator%20Interconnection%20Queue%20Update730302.pdf
- id: 4
  title: '"Transformers in 2026: Shortage Scramble or Self-Inflicted Crisis?" — Power Magazine, citing
    Wood Mackenzie Q2 2025 —'
  url: https://www.powermag.com/transformers-in-2026-shortage-scramble-or-self-inflicted-crisis/
- id: 5
  title: '"GE Vernova''''s gas-turbine backlog stretches into 2029" — Utility Dive, Dec 2025 investor-day
    coverage —'
  url: https://www.utilitydive.com/news/ge-vernova-gas-turbine-investor/807662/
- id: 6
  title: FERC Order 189 FERC ¶ 61,078, Docket ER24-2172-000, 1 Nov 2024 —
  url: https://www.ferc.gov/sites/default/files/2024-11/20241101-3061_ER24-2172-000.pdf
- id: 7
  title: 'Constellation Energy: "Constellation to Launch Crane Clean Energy Center" —'
  url: https://www.constellationenergy.com/news/2024/Constellation-to-Launch-Crane-Clean-Energy-Center-Restoring-Jobs-and-Carbon-Free-Power-to-The-Grid.html
- id: 8
  title: 'Amazon: "Amazon''s nuclear small modular reactor investment for net-carbon-zero" —'
  url: https://www.aboutamazon.com/news/sustainability/amazon-nuclear-small-modular-reactor-net-carbon-zero
- id: 9
  title: Kairos Power and Google partnership to deploy 500 MW —
  url: https://kairospower.com/external_updates/google-and-kairos-power-partner-to-deploy-500-mw-of-clean-electricity-generation/
- id: 10
  title: LevelTen Energy Q4 2025 North American PPA Price Index —
  url: https://www.leveltenenergy.com/post/levelten-q4-2025-north-american-ppa-price-index-solar-prices-rise-while-wind-experiences-a-slight-decline
- id: 11
  title: '"Loudoun County Eliminates By-Right Data Center Development" — Holland & Knight client alert
    —'
  url: https://www.hklaw.com/en/insights/publications/2025/04/loudoun-county-virginia-eliminates-by-right-data-center-development
- id: 12
  title: '"Ireland ends moratorium on new power links to data centers" — EnergyConnects, citing CRU decision
    Dec 12 2025 —'
  url: https://www.energyconnects.com/news/utilities/2025/december/ireland-ends-moratorium-on-new-power-links-to-data-centers/
- id: 13
  title: '"Singapore announces data center capacity allocation call" — Morgan Lewis on DC-CFA2 —'
  url: https://www.morganlewis.com/pubs/2026/03/singapore-announces-data-center-capacity-allocation-call
- id: 14
  title: CBRE North America Data Center Trends, H2 2025 —
  url: https://www.cbre.com/insights/books/north-america-data-center-trends-h2-2025
- id: 15
  title: '"Musk''''s xAI gets permit for turbines to power supercomputer in Memphis" — CNBC, 3 July 2025
    —'
  url: https://www.cnbc.com/2025/07/03/musks-xai-gets-permit-for-turbines-to-power-supercomputer-in-memphis.html
- id: 16
  title: '"xAI Sued for Illegal Power Plant" — Earthjustice press release on NAACP / SELC Clean Air Act
    complaint —'
  url: https://earthjustice.org/press/2026/xai-sued-for-illegal-power-plant
- id: 17
  title: NVIDIA GB200 NVL72 product page —
  url: https://www.nvidia.com/en-us/data-center/gb200-nvl72/
- id: 18
  title: Supermicro SuperCluster GB200 NVL72 datasheet —
  url: https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB200_NVL72.pdf
- id: 19
  title: Uptime Institute, "Data center cooling," Field 181, July 2025 —
  url: https://intelligence.uptimeinstitute.com/sites/default/files/2025-07/UI%20Field%20181_Data%20center%20cooling.pdf
- id: 20
  title: Uptime Institute Global Data Center Survey 2025 —
  url: https://intelligence.uptimeinstitute.com/resource/uptime-institute-global-data-center-survey-2025
- id: 21
  title: Motivair ChilledDoor rear-door heat exchanger brochure —
  url: https://www.motivaircorp.com/uploads/files/brochures/ChilledDoor%20brochure_2023.pdf
- id: 22
  title: Vertiv CoolChip CDU datasheet —
  url: https://www.vertiv.com/4930fc/globalassets/shared/vertiv-coolchip-cdu_datasheet_en-na.pdf
- id: 23
  title: 'Microsoft Cloud Blog: "Sustainable by design: next-generation datacenters consume zero water
    for cooling" —'
  url: https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/12/09/sustainable-by-design-next-generation-datacenters-consume-zero-water-for-cooling/
- id: 24
  title: '"The Dalles mayor on Google datacenter water use" — OPB, 23 Jan 2026 —'
  url: https://www.opb.org/article/2026/01/23/the-dalles-mayor-data-center-google/
- id: 25
  title: '"NVIDIA contributes GB200 NVL72 designs to Open Compute Project" — NVIDIA Developer blog —'
  url: https://developer.nvidia.com/blog/nvidia-contributes-nvidia-gb200-nvl72-designs-to-open-compute-project/
- id: 26
  title: '"NVIDIA GB200 NVL72 Delivers Trillion-Parameter LLM Training and Real-Time Inference" — NVIDIA
    Developer blog —'
  url: https://developer.nvidia.com/blog/nvidia-gb200-nvl72-delivers-trillion-parameter-llm-training-and-real-time-inference/
- id: 27
  title: '"Spectrum-X Ethernet networking for xAI Colossus" — NVIDIA Newsroom —'
  url: https://nvidianews.nvidia.com/news/spectrum-x-ethernet-networking-xai-colossus
- id: 28
  title: '"Building Meta''''s GenAI Infrastructure" — Meta Engineering, 12 Mar 2024 —'
  url: https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/
- id: 29
  title: '"Broadcom Announces Tomahawk 6 Davisson" — Broadcom investor news —'
  url: https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-tomahawkr-6-davisson-industrys-first-1024
- id: 30
  title: '"100,000 H100 clusters: power, network topology, Ethernet vs InfiniBand" — SemiAnalysis —'
  url: https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network
- id: 31
  title: JLL Global Data Center Outlook —
  url: https://www.jll.com/en-us/insights/market-outlook/data-center-outlook
- id: 32
  title: Cushman & Wakefield US Data Center Development Cost Guide —
  url: https://www.cushmanwakefield.com/en/united-states/insights/data-center-development-cost-guide
- id: 33
  title: '"NVIDIA''''s Blackwell AI GPUs to cost up to $70,000; server racks up to $3M" — Tom''''s Hardware
    —'
  url: https://www.tomshardware.com/pc-components/gpus/nvidias-next-gen-blackwell-ai-gpus-to-cost-up-to-dollar70000-fully-equipped-servers-range-up-to-dollar3000000-report
- id: 34
  title: Meta Q1 2026 Earnings Release —
  url: https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/default.aspx
- id: 35
  title: '"Microsoft expects to spend $80 billion on AI data centers in FY 2025" — CNBC, 3 Jan 2025 —'
  url: https://www.cnbc.com/2025/01/03/microsoft-expects-to-spend-80-billion-on-ai-data-centers-in-fy-2025.html
- id: 36
  title: '"Crusoe expands Abilene AI campus with new 900 MW AI factory for Microsoft" — Data Center Knowledge
    —'
  url: https://www.datacenterknowledge.com/build-design/crusoe-expands-abilene-ai-campus-with-new-900mw-ai-factory-for-microsoft
- id: 37
  title: '"CoreWeave Closes Landmark $8.5 Billion Financing Facility" — CoreWeave investor relations —'
  url: https://investors.coreweave.com/news/news-details/2026/CoreWeave-Closes-Landmark-8-5-Billion-Financing-Facility-Achieving-First-Investment-Grade-Rated-GPU-backed-Financing/default.aspx
- id: 38
  title: '"Announcing the Stargate Project" — OpenAI, 21 Jan 2025 —'
  url: https://openai.com/index/announcing-the-stargate-project/
- id: 39
  title: '"Crusoe Announces Flagship Abilene Data Center Is Live" — Crusoe newsroom —'
  url: https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live
- id: 40
  title: '"Colossus (supercomputer)" — Wikipedia overview of xAI Memphis build —'
  url: https://en.wikipedia.org/wiki/Colossus_(supercomputer)
- id: 41
  title: '"Entergy Louisiana to power Meta''''s data center in Richland Parish" — Entergy newsroom —'
  url: https://www.entergy.com/news/entergy-louisiana-power-meta-s-data-center-in-richland-parish
- id: 42
  title: '"AWS Project Rainier: Trainium chips compute cluster" — About Amazon —'
  url: https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster
- id: 43
  title: '"Made in Wisconsin: the world''''s most powerful AI datacenter" — Microsoft On the Issues —'
  url: https://blogs.microsoft.com/on-the-issues/2025/09/18/made-in-wisconsin-the-worlds-most-powerful-ai-datacenter/
- id: 44
  title: '"Explaining Uptime Institute''''s Tier Classification System" — Uptime Institute Journal —'
  url: https://journal.uptimeinstitute.com/explaining-uptime-institutes-tier-classification-system/
- id: 45
  title: '"Myths and Misconceptions Regarding the Uptime Institute''''s Tier System" — Uptime Institute
    Journal —'
  url: https://journal.uptimeinstitute.com/myths-and-misconceptions-regarding-the-uptime-institutes-tier-certification-system/
- id: 46
  title: '"Revisiting Reliability in Large-Scale Machine Learning Research Clusters" (Meta, arXiv 2410.21680)
    —'
  url: https://arxiv.org/html/2410.21680v1
- id: 47
  title: '"Large-scale cluster management at Google with Borg" (EuroSys 2015) —'
  url: https://research.google.com/pubs/archive/43438.pdf
- id: 48
  title: '"2025 Guide to Data Center Certifications" — Datacenters.com —'
  url: https://www.datacenters.com/news/2025-guide-to-data-center-certifications-uptime-hipaa-soc-2-more
- id: 49
  title: NVIDIA Q3 FY26 Earnings Release (SEC) —
  url: https://www.sec.gov/Archives/edgar/data/1045810/000104581025000228/q3fy26pr.htm
- id: 50
  title: NVIDIA Q4 FY26 Earnings Release (SEC) —
  url: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26pr.htm
- id: 51
  title: '"Anthropic and Amazon expand compute partnership" — Anthropic news —'
  url: https://www.anthropic.com/news/anthropic-amazon-compute
- id: 52
  title: '"SK hynix announces 3Q25 financial results" —'
  url: https://news.skhynix.com/sk-hynix-announces-3q25-financial-results/
- id: 54
  title: '"Crusoe and Tallgrass announce AI data center in Wyoming" — Crusoe newsroom —'
  url: https://www.crusoe.ai/resources/newsroom/crusoe-and-tallgrass-announce-ai-data-center-in-wyoming
- id: 55
  title: 'DPR Construction project page: Crusoe Abilene Data Center —'
  url: https://www.dpr.com/projects/crusoe-abilene-data-center
- id: 56
  title: AGC of America & NCCER 2025 Workforce Survey, National Results —
  url: https://www.agc.org/sites/default/files/users/user21902/2025_Workforce_Survey_National_FINAL_m.pdf
- id: 57
  title: '"The Data Center Surge: A New Generation of IBEW Jobs" — IBEW Electrical Worker —'
  url: https://ibew.org/electrical_worker/the-data-center-surge-a-new-generation-of-ibew-jobs/
- id: 58
  title: 'White House EO: Accelerating Federal Permitting of Data Center Infrastructure (July 2025) —'
  url: https://www.whitehouse.gov/presidential-actions/2025/07/accelerating-federal-permitting-of-data-center-infrastructure/
- id: 59
  title: NFPA 75 Standard for Fire Protection of Information Technology Equipment —
  url: https://www.nfpa.org/codes-and-standards/nfpa-75-standard-development/75
- id: 60
  title: ICD 705 Tech Specs for Construction and Management of SCIFs, v15 —
  url: https://www.dni.gov/files/Governance/IC-Tech-Specs-for-Const-and-Mgmt-of-SCIFs-v15.pdf
- id: 61
  title: '"DeepMind AI reduces Google data centre cooling bill by 40%" — DeepMind blog, 20 July 2016 —'
  url: https://deepmind.google/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/
- id: 62
  title: '"Safety-first AI for autonomous data centre cooling and industrial control" — DeepMind blog,
    17 Aug 2018 —'
  url: https://deepmind.google/discover/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/
- id: 66
  title: '"Project Natick" — Microsoft Research site —'
  url: https://natick.research.microsoft.com/
- id: 67
  title: '"A closer look at Nvidia''''s 120kW DGX GB200 NVL72 rack system" — The Register, 21 Mar 2024
    —'
  url: https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/
- id: 69
  title: '"Global Tech Alliance Launches Stargate UAE" — G42 newsroom —'
  url: https://g42.ai/resources/news/global-tech-alliance-launches-stargate-uae
- id: 72
  title: '"BlackRock, GIP, Microsoft and MGX launch new AI partnership" — Microsoft news —'
  url: https://news.microsoft.com/source/2024/09/17/blackrock-global-infrastructure-partners-microsoft-and-mgx-launch-new-ai-partnership-to-invest-in-data-center-and-energy-infrastructure/
- id: 73
  title: '"Delivering AI Growth Zones" — UK Government policy paper —'
  url: https://www.gov.uk/government/publications/delivering-ai-growth-zones
- id: 74
  title: '"Huawei Ascend production ramp" — SemiAnalysis —'
  url: https://newsletter.semianalysis.com/p/huawei-ascend-production-ramp
- id: 75
  title: '"Data center project cancellations, power, public pushback" — Construction Dive, citing Baird
    —'
  url: https://www.constructiondive.com/news/data-center-project-cancellations-power-public-pushback/818157/
- id: 76
  title: '"Microsoft cancels up to 2 GW of data center projects, says TD Cowen" — Data Center Dynamics
    —'
  url: https://www.datacenterdynamics.com/en/news/microsoft-cancels-up-to-2gw-of-data-center-projects-says-td-cowen/
- id: 77
  title: '"The great GPU shortage: rental capacity" — SemiAnalysis —'
  url: https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity
- id: 78
  title: '"Project Blue would have used millions of gallons of Tucson water — residents, city leaders
    said no" — KJZZ —'
  url: https://www.kjzz.org/fronteras-desk/2025-08-11/project-blue-would-have-used-millions-of-gallons-of-tucson-water-residents-city-leaders-said-no
- id: 79
  title: 'NVIDIA DGX SuperPOD: Scalable Infrastructure for GB200 reference architecture —'
  url: https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-gb200/latest/dgx-superpod-components.html
- id: 80
  title: '"Design Parameters for Data Center Facilities" — Structure Magazine —'
  url: https://www.structuremag.org/article/design-parameters-for-data-center-facilities/
- id: 81
  title: Open Compute Project —
  url: https://www.opencompute.org/
:::
