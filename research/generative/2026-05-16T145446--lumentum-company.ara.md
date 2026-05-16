---
eyebrow: Optical infrastructure · Equity research
title: 'Lumentum: the EML chokepoint inside NVIDIA''s photonics build-out'
deck: A spin-off that nobody talked about for eight years just printed a quarter that nearly doubled.
  The story is not transceivers — it is one indium phosphide die that five companies on Earth can make
  and only one can ship in volume at 200G per lane.
lede: 'On May 6, 2026, Lumentum Holdings (NASDAQ: LITE) reported third-quarter fiscal 2026 revenue of
  $808.4 million, up 90% year over year, with non-GAAP gross margin of 47.9% and a guide for the next
  quarter implying a ~$3.0 billion fiscal-year run-rate against $1.65 billion in FY25. Three months earlier,
  NVIDIA had written the company a $2.0 billion convertible-preferred check at $695.31 per share, a binding
  equity tie wrapped around a multiyear capacity commitment. Six weeks after that, Lumentum closed on
  a 6-inch indium phosphide fab in Greensboro, North Carolina that it bought from Qorvo for $38 million
  in cash. The optical-components vendor that nobody outside the optics trade press paid attention to
  for a decade has become, in eighteen months, the single most concentrated bet on the chip-level chokepoint
  of the AI optical bill of materials. This report works through what changed, why the math holds together,
  and where the thesis is most likely to break.'
stats:
- label: Q3 FY26 revenue YoY
  value: +90.1%
- label: Non-GAAP gross margin
  value: '47.9%'
- label: NVIDIA preferred investment
  value: $2.0B at $695.31/sh
- label: '200G EML supply gap (mgmt)'
  value: '>30% under demand'
- label: Convertible fair value
  value: $19.1B vs $3.2B carrying
---

## 1. The Inflection

On May 6, 2026, Lumentum Holdings reported the cleanest single-quarter inflection in the recent history of optical components. Revenue for the third quarter of fiscal 2026, the period ended March 28, was **$808.4 million**, up **90.1% year over year** from $425.2 million[^1]. GAAP gross margin reached 44.2% and non-GAAP gross margin **47.9%**, an expansion of 540 basis points sequentially and 1,270 basis points year over year[^1]. GAAP income from operations swung from a *$37.7 million loss* a year earlier to a **$174.5 million profit**; non-GAAP operating margin printed at **32.2%**[^1]. This is not a company growing through a cycle — this is a company that has been re-platformed onto a different demand curve, and the numbers are the thesis.

The translation to per-share economics was just as violent. GAAP diluted EPS came in at **$1.50**; non-GAAP diluted EPS at **$2.37**, both well above guidance set on the prior call[^2]. The mix was the tell: the Components line printed **$533.3 million** (66% of revenue, +77% YoY), and the Systems line — which now houses Cloud Light's switch-side optical assemblies — printed **$275.1 million** (34% of revenue, **+121% YoY**)[^2]. Systems is the AI build-out in pure form. CEO Michael Hurlston framed it directly: *"Lumentum delivered an exceptional third quarter, with revenue growing 90% year over year to a record $808 million."*[^2]

Step back to the trailing fiscal year for context. Lumentum closed FY25 (ended June 28, 2025) at **$1,645.0 million** in revenue, up 21% off a prior-year base that had itself declined 23%[^3]. Nine-month FY26 revenue was **$2,007.7 million** versus $1,164.3 million in the prior-year nine months — growth of **72.4%**[^1]. Said differently: in nine months of FY26, Lumentum has already booked 22% more revenue than it did across all twelve months of FY25.

The forward guide is where the run-rate math becomes inescapable. For Q4 FY26 the company guided revenue of **$960 million to $1,010 million**, non-GAAP operating margin of **35–36%**, and non-GAAP EPS of **$2.85–$3.05**[^2]. Take the midpoint and full-year FY26 revenue lands at roughly **$2.99 billion** — call it $3.0B — against $1.65B in FY25, a single-year increase of **~82%**. The exit-quarter run-rate is **~$3.94 billion annualized**. CFO Wajid Ali, at the company's March 2026 analyst day, set the medium-term target even higher: a **$2 billion quarterly** revenue exit with **40% non-GAAP operating margin**, mapping to roughly $25 of non-GAAP EPS on the current diluted share count[^4].

| Period | Revenue | YoY | Source |
|---|---|---|---|
| FY23 (prior cycle peak) | $1,767M | — | FY25 10-K[^3] |
| FY24 | $1,360M | -23% | FY25 10-K[^3] |
| FY25 | $1,645M | +21% | FY25 10-K[^3] |
| 9M FY26 (actual) | $2,008M | +72% | Q3 FY26 10-Q[^1] |
| Q4 FY26 guide (mid) | $985M | — | Q3 FY26 release[^2] |
| FY26E (implied) | **~$2,993M** | **+82%** | Computed |
| Q4 FY26 annualized | ~$3,940M | — | Q4 guide x 4 |

The margin reset matters as much as the revenue. Non-GAAP gross margin moving from 35.2% a year ago to 47.9% in a single fiscal year is a **1,270 basis-point** reflation that did not happen by accident — it is the combined effect of EML mix lifting Components ASPs, Cloud Light optical assemblies layering on at materially higher contribution margin than the legacy 3D-sensing and pump-laser businesses they displace, and the Thailand fab finally running at volumes where fixed overhead absorbs[^1]. A non-GAAP operating margin guide of 35–36% for Q4 implies operating margin will have expanded by more than **3,000 basis points** in roughly four quarters — a magnitude of operating leverage normally reserved for early-stage software companies, not 30-year-old optical-component vendors.

What would weaken this read: the +90% YoY headline rides on a Q3 FY25 comp of $425.2 million that was itself depressed by the trough of the telecom and 3D-sensing cycle[^3]. A fairer measure of the structural step-up is to compare the implied FY26 figure of ~$3.0B against the prior-cycle peak of FY23 at $1,767M — that is **+70%** over the previous high, not +90% over a fresh base. Real, but not as vertiginous as the YoY optics suggest. If AI-driven optical demand normalizes in calendar 2027 the way 400G demand normalized in 2022, the exit run-rate becomes the ceiling rather than the floor, and the 35%+ operating margin guide becomes the part of the model that compresses fastest. Why this matters: a single quarter of revenue that nearly doubles, paired with a guide that pushes the company to a ~$3 billion fiscal year and a stated medium-term path to $8B+ run-rate, forces a discontinuous re-rating — and every subsequent section of this report is an attempt to underwrite whether the components driving that print are durable enough to sustain it.

## 2. Cloud Light — the $750M acquisition that re-platformed Lumentum onto AI

On October 30, 2023, Lumentum announced it would acquire privately held Cloud Light Technology for approximately $750 million in cash, closing the deal eight days later on November 7, 2023[^5,6]. The final purchase price recorded in the FY25 10-K landed at $728.5 million — $705.0 million in cash plus $23.5 million in share-based consideration assumed for unvested Cloud Light equity[^3]. Measured against any reasonable horizon, this is the single most consequential capital allocation decision Lumentum has made since its 2015 spin-off from JDSU. It took a company whose identity was telecom transport and 3D-sensing for the iPhone and bolted on a hyperscale transceiver business at exactly the moment hyperscale transceiver demand inflected.

Cloud Light at the time of announcement was small but extraordinarily well-positioned. Lumentum's own deal disclosure described it as a business generating "more than $200 million" in trailing-twelve-month revenue, with "nearly all" of that revenue derived from 400G-or-higher speed transceivers and "over half" coming specifically from 800G modules[^5]. In a market where most legacy optical-component vendors were still shipping 100G and 200G volumes into telecom, Cloud Light was already a pure-play next-generation datacom asset. Then-CEO Alan Lowe — succeeded by Michael Hurlston in February 2025 — framed the rationale plainly on the announcement: "We are making a strategic investment to significantly expand our opportunities in the cloud data center and networking infrastructure space. Cloud Light provides us with the highest speed transceiver solutions at scale."[^5] Lumentum claimed the deal delivered "more than a five-fold expansion in the company's served opportunity inside of data centers."[^5]

| Deal term | Value |
|---|---|
| Announcement | Oct 30, 2023 |
| Close | Nov 7, 2023 |
| Cash consideration | $705.0M |
| Share-based consideration | $23.5M |
| Total purchase price (per 10-K) | $728.5M |
| Cloud Light TTM revenue at announcement | >$200M |
| Share of revenue from 400G+ | nearly 100% |
| Share of optical transceiver revenue from 800G | >50% |
| Nov 2025 indemnification settlement (recovery) | $27.5M |

The post-close economics have outrun even the deal-day narrative. In Q3 FY26 alone, Lumentum's cloud transceiver product lines added more than $137.0 million in year-over-year revenue, and over the trailing nine months added more than $268 million[^1]. That nine-month incremental figure alone exceeds Cloud Light's *entire* TTM revenue at the time of the deal — meaning the acquired business has roughly doubled inside the parent in about two years. There is also a small but symbolically meaningful coda on price: in November 2025, Lumentum and the former Cloud Light shareholders settled outstanding indemnification claims for $27.5 million, a recovery that further trims the effective net deal cost[^1].

Pre-Cloud Light, Lumentum did not even use "AI" or "cloud" as a primary segment narrative. The company's pitch was telecom transport (ROADMs, pumps, tunable lasers) plus a large, lumpy 3D-sensing business tethered to Apple's iPhone Face ID stack. The phrase "AI/Cloud" first surfaced in earnest on the Q1 FY24 earnings communications — the same quarter the deal was announced — as Lumentum reframed its addressable market around hyperscale buildouts[^6]. The geographic fingerprints of that re-platforming are visible in the FY25 10-K's customer-geography note. Cloud Light operates out of Hong Kong, and Lumentum's Hong Kong ship-to revenue line moved from $246.7 million in FY23 to $261.9 million in FY24 to $398.6 million in FY25, tracking the Cloud Light integration[^3].

The bear-side reading: the Cloud Light price tag looks brilliant today only because hyperscale capex inflected within a quarter or two of close. Late 2023 was, by contrast, the trough of a brutal telecom-optical inventory correction — Lumentum's own FY24 revenue would collapse to $1,359 million, down 23% year over year, and most strategic buyers for optical assets had retreated[^3]. A reasonable bearish framing is that Lumentum bought a high-quality but concentrated transceiver shop in a buyer's market and got lucky on the macro: the AI capex wave arrived months after close. The risk-adjusted version of the bull case is therefore less "management foresight" and more "right asset at the bottom of the cycle, with optionality the buyer did not have to pay for." Either way, the realized return is unambiguous, and without Cloud Light, Lumentum in 2026 is still a telecom-and-iPhone company waiting for the next 3D-sensing refresh.

## 3. The EML chokepoint — why 200G-per-lane indium phosphide lasers sit atop the AI BOM

Strip a 1.6T transceiver down to its silicon-and-glass essentials and you find an unglamorous truth: the most expensive, hardest-to-source, and least-substitutable component is not the DSP, not the photonic integrated circuit, and not the connector — it is a small indium phosphide laser die called an electro-absorption modulated laser, or EML. There are five companies on the planet that can make one in volume — Lumentum, Coherent, Mitsubishi Electric, Sumitomo Electric, and Broadcom[^7]. Of those five, only one is shipping the next-generation 200-gigabit-per-lane variant in commercial volume, and it is Lumentum[^8]. This is the economic core of the company. Everything else — the transceiver assembly, the ROADM line cards, the industrial lasers — orbits this 1-mm-square chip.

The supplier landscape is unusually concentrated because the manufacturing barrier is unusually high. EMLs are built on indium phosphide wafers — a notoriously brittle III-V semiconductor that has resisted the wafer-size scaling silicon long ago took for granted. Yields are sensitive to defects measured in tens of atoms; epitaxial growth tolerances are sub-nanometer; and each step up the data rate — 50G to 100G to 200G to a future 400G per lane — requires re-tuning the active region, the grating, and the absorber simultaneously. Lumentum is estimated to hold roughly 50-60% of the global high-end EML market, and is described by independent analysts as "currently the only supplier shipping 200G-per-lane EMLs at volume"[^8].

| Supplier | EML position | 200G/lane status |
|---|---|---|
| Lumentum | ~50-60% global share, front-runner | Shipping at volume; supply < demand by >30% |
| Coherent | Second-largest merchant supplier | Sampling; migrating to 6-inch InP wafers |
| Mitsubishi Electric | Japanese incumbent, strong in telecom | Qualifying; behind on volume |
| Sumitomo Electric | Japanese incumbent, niche datacom | Qualifying; behind on volume |
| Broadcom | Captive — supplies its own modules | Internal; not a meaningful merchant source |

The financial signature of this scarcity is now visible in the income statement. Lumentum reported in its Q3 FY26 earnings call that 200G EML revenue had more than doubled sequentially, and that the company shipped roughly twice as many laser chips as in the same quarter the prior year[^9]. CEO Michael Hurlston guided to more than 50% growth in 200G/lane EML units in the December 2026 quarter versus December 2025[^9]. Even with that ramp, the company is not catching up. Asked on the same call about the supply-demand gap, Hurlston was unambiguous: "We continue to lag demand. The supply-demand imbalance is probably even higher than we reported in our last call, somewhere greater than 30%."[^9] In a normal semiconductor cycle, a 30% gap would be closed within two quarters by an opportunistic competitor. Here, the competitor set is four other names, none of whom can step in.

What makes this chokepoint genuinely interesting — as opposed to merely tight — is the price-cost asymmetry. Jefferies' supply-chain model, cited by independent equity research, puts 200G EML pricing at "nearly 2x 100G at only 15% increase in COGS"[^10]. Read that sentence twice. A doubling of average selling price against a low-double-digit increase in unit cost means the incremental gross margin on every 200G die shipped is in the 80%+ range — software-like economics on a piece of hardware that requires a dedicated indium phosphide wafer fab to produce. The mix shift is what is dragging Lumentum's consolidated gross margin north even as the company spends aggressively on capacity: management is guiding 200G+ EMLs from roughly 10% of Datacom laser-chip revenue today toward 25% by end-2026[^13].

The capacity build is real and expensive. Lumentum invested approximately $125 million of capex in Q3 FY26 alone, the bulk of it directed at cloud and AI laser capacity[^1]. Property, plant and equipment in Thailand — where the transceiver and laser back-end sits — grew by $109.8 million, or roughly 50%, over the first nine months of FY26, reaching $328.4 million[^1]. And the technology roadmap continues to extend. At OFC 2026, Lumentum demonstrated a 1.6T DR4 OSFP module built around four 400-gigabit-per-lane differential EMLs — explicitly described as "a stepping-stone to a future 3.2T module" — with optical power above 1.0 W at 25 degrees Celsius, linewidth below 100 kHz, and side-mode suppression above 40 dB[^14]. Each generation extends the chokepoint by another two years.

The bear case here is not that demand softens — it is that supply catches up. Coherent has announced the industry's first 6-inch InP wafer fab, claiming roughly 4x more dies per wafer and a die-cost reduction of more than 60% versus the 3-4 inch wafers Lumentum currently uses[^11]. If Coherent qualifies 200G EMLs on a 6-inch line in late 2026 or 2027, the wafer-economics gap inverts. Lumentum's non-GAAP gross margin lead over Coherent is presently only about 800 basis points (47.9% versus 39.6%), and Coherent's is improving[^12]. The "2x price at 1.15x cost" math is a function of scarcity, not physics; close the gap and the premium compresses. Why this matters: Lumentum's AI thesis is not really a transceiver story — module assembly is a contract-manufacturing business with mid-teens margins. The thesis is that a single 1-mm InP die, made by five companies and shipped in volume by one, sits on the critical path of every 800G and 1.6T optic going into NVIDIA, Google, and Meta racks through 2027.

## 4. NVIDIA's $2B bet and the two-customer problem

On March 2, 2026, NVIDIA wrote Lumentum a check that reordered the company's strategic map. Lumentum issued and sold approximately **2.9 million shares of Series A Convertible Preferred Stock** at **$695.31 per share**, for an aggregate purchase price of **$2.0 billion**, with each preferred share converting one-for-one into common stock after Hart-Scott-Rodino clearance[^1]. This is not an MOU, not a letter of intent, not a "framework." It is a binding equity tie at a fixed strike — the kind of capital structure event that hardwires a customer relationship into the shareholder register.

NVIDIA's own language framed the deal as a multi-vector commitment: "NVIDIA is investing $2 billion in Lumentum to support R&D, future capacity and operations. The nonexclusive agreement includes an NVIDIA multibillion purchase commitment and future capacity access rights."[^15] The word that matters is *capacity*. NVIDIA is not buying lasers off a shelf — it is reserving slots on a constrained EML and CW DFB line that, as the prior section laid out, the rest of the industry is also queuing for. Jensen Huang's quote made the framing explicit: "AI has reinvented computing and is driving the largest computing infrastructure buildout in history. Together with Lumentum, NVIDIA is advancing the world's most sophisticated silicon photonics to build the next generation of gigawatt-scale AI factories."[^15] CEO Michael Hurlston: "This multiyear strategic agreement reflects our shared commitment to advancing the optics technologies that will power the next generation of AI infrastructure."[^15]

The deal does not exist in isolation. The same day, NVIDIA committed a parallel **$2 billion** to Coherent, expanding what it described as a twenty-year relationship and effectively double-sourcing its laser supply across the only two Western vendors capable of producing high-volume 200G-per-lane EMLs[^16]. Read together, the two checks are a $4B insurance policy on Spectrum-X and Quantum-X Photonics co-packaged optics switch volumes through the end of the decade. NVIDIA is not picking a winner; it is funding the duopoly. The strike price tells its own story. NVIDIA priced the preferred at $695.31 while LITE traded in a roughly $600-700 band; by mid-May 2026 the common had rallied through **$1,000**, leaving NVIDIA's economic position materially in the money before HSR even cleared[^17]. The market read the deal as validation, not dilution.

But validation cuts both ways. The same Q3 FY26 10-Q that disclosed the NVIDIA placement also crystallized the concentration problem that has been quietly building inside Lumentum's customer file. Per Note 15: "During the three months ended March 28, 2026, two customers individually accounted for **26% and 12%** of our total revenue, respectively. During the nine months ended March 28, 2026, two customers individually accounted for 24% and 16% of our total net revenue."[^1] Accounts receivable tells the same story: as of the quarter close, two customers represented **25% and 10%** of gross AR[^1]. The customer mix is not just concentrated on the income statement — it is concentrated on the balance sheet.

CEO Hurlston has been transparent about who at least one of those customers is. On the Q3 FY26 earnings call, asked about hyperscaler exposure, he said: "Google is obviously doing very well in the market... they're certainly one of our largest customers, and we've benefited greatly from that relationship."[^9] The second 10%+ customer is widely inferred to be a second hyperscaler in the transceiver supply chain, with NVIDIA itself poised to become a third once the preferred converts and the purchase commitment ramps.

| Period | Customer A | Customer B | Combined |
|---|---|---|---|
| FY24 | 18.9% | 11.4% | 30.3% |
| FY25 | 16.0% | 15.4% | 31.4% |
| 9M FY26 | 24% | 16% | 40% |
| Q3 FY26 | **26%** | **12%** | **38%** |

The bear-side counterpoint is that the concentration is a feature of the cycle, not necessarily a permanent structural risk. Historically Lumentum's top-two exposure ran in the high-20s to low-30s in aggregate; the jump to 26%/12% in a single quarter — versus 17%/15% in the prior-year comparable — reflects how steeply hyperscaler optics demand has ramped against a still-recovering Industrial Tech base[^3]. As NVIDIA's purchase commitment activates and as Microsoft, Meta, and Amazon backfill the supplier-qualification pipeline, the denominator should broaden. The bear case is that it doesn't — that a single hyperscaler's decision to dual-source to Coherent, or to insource via an acquisition, lops 10-15 points off the revenue line in a quarter with no offset. Why this matters: NVIDIA's $2B is the bull thesis and the bear thesis in the same document — it underwrites the next three years of demand visibility while simultaneously confirming that Lumentum's revenue line is now a derivative of two — soon three — buyers' capex decisions.

## 5. The co-packaged optics pivot — how Lumentum turned the pluggable-killer into an annuity

For five years, the consensus bear case on every pluggable-optics vendor read the same way: co-packaged optics will collapse the transceiver TAM. Move the optical engine onto the switch ASIC substrate, the argument went, and you eliminate the retiming silicon, the housing, the connector — and most of the laser content — that pluggables charge a premium for. Lumentum, Coherent, Marvell-Inphi, and Innolight were all supposed to watch a $30B socket migrate into the switch BOM and disappear as a discrete line item. The technology arrived on schedule. The disintermediation did not. NVIDIA's Spectrum-X Photonics (Ethernet) and Quantum-X Photonics (InfiniBand) switches, announced at GTC on March 18, 2025, are the first volume CPO products in the AI build-out — and their reference architecture explicitly preserves an external laser source socket sitting on the front panel of the switch chassis[^18]. Lumentum is selling into that socket. The pluggable-killer became a pluggable annuity.

The architectural choice is the entire story. In a conventional pluggable transceiver, a small distributed-feedback (DFB) laser sits inside each QSFP-DD or OSFP module — eight lasers per 800G port, roughly 1,000+ lasers per top-of-rack switch. CPO does not eliminate lasers; it relocates them. NVIDIA's design pulls every active laser out of the optical engine, consolidates them into far fewer, far higher-power continuous-wave (CW) sources, and pipes light into the package over polarization-maintaining fiber. The company claims the resulting system delivers 3.5x more power efficiency, 63x greater signal integrity, 10x greater network resiliency, and 1.3x faster deployment versus pluggable-based fabrics[^18]. The corollary, less marketed but more important to Lumentum shareholders: the laser that replaces eight DFBs is not a commodity component. It must hit hundreds of milliwatts of fiber-coupled power, sub-megahertz linewidth, and telecom-grade reliability — and it has to do so in a hot-swappable, field-replaceable form factor because a dead laser cannot strand a switch.

Lumentum's ultra-high-power (UHP) CW laser, packaged in the ELSFP (External Laser Source for CPO) pluggable, is engineered exactly to that envelope: 350 mW at 50°C (235 mW at 70°C), 1311 nm on indium phosphide, up to 24 dBm of optical output per wavelength, linewidth under 500 kHz, relative intensity noise below -147 dB/Hz, and greater than 20% power conversion efficiency[^19]. These are not data-com specs — they are closer to coherent-transmission specs delivered in a pluggable. They are also not specs that NVIDIA's existing DFB suppliers can hit at volume without years of process work, which is the moat. On the February 3, 2026 Q2 FY26 call, management disclosed an "incremental multi-hundred-million-dollar" purchase order for UHP CPO lasers, deliverable in the first half of calendar 2027[^20]. By the Q3 FY26 release, Hurlston's framing was that "as our key growth drivers of co-packaged optics and optical circuit switches begin to kick in, we would expect further increases in earnings power"[^2] — and the optical circuit switch line, which uses Lumentum's MEMS technology and is sold into both Google's TPU fabrics and emerging hyperscaler reference designs, already crossed $25M in Q3 FY26 revenue alone, with year-to-date OCS revenue above $38M[^1].

The architectural choice is not unique to NVIDIA. Broadcom's Tomahawk 6-Davisson, announced October 2025 as the industry's first 102.4 Tb/s CPO switch, also pulls the lasers out of the package and into field-replaceable external modules on the chassis face[^21]. That convergence between the two CPO leaders matters because it converts a single-customer bet into a category architecture. Management's revenue-content math reflects this: on the Q2 FY26 call they framed the ELSFP opportunity as roughly 2.0x to 2.5x the dollar content per system versus selling lasers alone into traditional pluggables[^20] — because the ELSFP is itself a sophisticated, separately-tested, separately-margined module, not a sub-component sold to a transceiver house at a markup floor.

| Platform | Vendor | Throughput | Ports | Laser sourcing | Ship window |
|---|---|---|---|---|---|
| Quantum-X Photonics | NVIDIA | 115 Tb/s | 144 x 800G (InfiniBand) | External (ELSFP) | 2H CY2025 |
| Spectrum-X Photonics (entry) | NVIDIA | 100 Tb/s | 128p / 512p @ 800G | External (ELSFP) | CY2026 |
| Spectrum-X Photonics (scale) | NVIDIA | 400 Tb/s | 512p / 2,048p @ 800G | External (ELSFP) | CY2026 |
| Tomahawk 6-Davisson | Broadcom | 102.4 Tb/s | Configurable 800G/1.6T | External, field-replaceable | Sampling Oct 2025 |
| Monolithic InP-on-Si (research) | Marvell / TSMC COUPE | TBD | TBD | On-package (potential) | 2028+ |

LightCounting's March 2025 timeline is consistent with management's order book: InfiniBand CPO ramps in 2H25, Ethernet CPO in 2H26, NVLink-class CPO around 2028, with mass adoption between 2028 and 2030 — and critically, the pluggable TAM does not disappear, it co-exists, with the firm modeling roughly $34B of pluggables alongside a ~$9B CPO market by 2030[^22]. That is the shape of an additive cycle, not a substitution cycle, which is the single most important framing shift for Lumentum's multiple.

The bear-case counterpoint is that the entire ELS thesis is contingent on one architectural decision that is not physically mandatory. If TSMC's COUPE silicon-photonics platform or a Marvell / Celestial AI integration matures to the point where indium-phosphide lasers can be heterogeneously bonded directly onto the silicon photonic die — true monolithic InP-on-Si — the external laser socket disappears, and Lumentum's CPO content goes with it. Both NVIDIA and Broadcom chose external sourcing for thermal, reliability, and field-serviceability reasons in this generation, but neither has committed to that choice for the next one. Why this matters: if the architectural pattern set by NVIDIA and Broadcom holds, the CPO transition does not compress Lumentum's content per port — it expands it by roughly 2-2.5x, and concentrates the highest-spec, highest-margin photonic component in the system inside a part that only two or three vendors on Earth can currently build.

## 6. Manufacturing reset — Thailand 4x, Greensboro 6-inch InP, and a capex curve built for a $4B year

Lumentum is in the middle of a manufacturing footprint reset on a scale it has never executed in its decade as a standalone company. The arithmetic is the cleanest way in: property, plant and equipment in Thailand alone has gone from $141.0M (June 2024) to $218.6M (June 2025) to $328.4M (March 2026) — a 133% step-up in 21 months concentrated in a single country[^1]. Capex tells the same story from the other side of the cash flow statement: $128.5M in FY23, $133.0M in FY24, $231.0M in FY25 (+74%), and $284.5M through just nine months of FY26 with $125M of that in Q3 alone — a run-rate that puts the company on a $400M+ FY26 print, more than triple the FY23 baseline[^1]. This is not a maintenance refresh. It is a balance-sheet bet that Cloud Light, EML, and CPO laser orders will arrive on the timeline the cloud capex curve implies — and that Lumentum needs the owned capacity to take them.

The center of gravity is Thailand. The Nava Nakorn Industrial Estate site in Pathum Thani is a 1,173,000 square foot owned facility — the largest single owned site in Lumentum's global portfolio[^3]. In October 2025, Lumentum committed an additional 2.3 billion baht (~$70M) to the site, bringing cumulative Thailand investment past THB 20B per the Thailand Board of Investment, with the stated goal of quadrupling production capacity within two years (late 2027) and ramping headcount toward 11,000 from roughly 3,000 at the start of 2025[^23]. To partially fund the migration, Lumentum sold its Shenzhen, China facility — announced December 17, 2024 and closed March 5, 2025 for $47.8M in net proceeds and a $34.9M book gain — and moved production into Thailand-owned lines[^3]. The Shenzhen sale also nudges the company's manufacturing concentration away from contract manufacturers in China: "Contract Manufacturer A" — widely understood to be Fabrinet — was 30.3% of inventory purchases in FY24 but had declined to 19% in 9M FY26 as Lumentum insourced[^1].

The second leg of the reset is Greensboro, North Carolina. On March 17, 2026, Lumentum closed the acquisition of a 240,000 sq ft indium phosphide fab in Greensboro, NC for $38.0M cash from a third party — widely reported as Qorvo[^1,4]. The plant runs 6-inch InP wafers — a meaningful step up in wafer diameter for InP, which has historically been a 3- or 4-inch business — and is being purpose-built for the continuous-wave and ultra-high-power lasers that feed co-packaged optics, with production ramp targeted for mid-2028 and NVIDIA as the anchor customer[^1]. Strategically, Greensboro is a US-sovereign hedge inside an otherwise Thailand-heavy footprint; tactically, it doesn't ship product for two years, which means it solves the 2028 problem, not the 2026 one.

| Site | Sq Ft | Function | Status |
|---|---|---|---|
| Pathum Thani, Thailand | 1,173,000 | Datacom/telecom assembly & test; CW laser scale-up | Owned; +THB 2.3B Oct 2025; 4x capacity by late 2027 |
| Sagamihara, Japan | 472,000 | InP wafer fab | Owned; purchased July 2024 for $42M |
| San Jose, CA (Rose Orchard) | 238,000 | HQ + UHP InP fab | Owned |
| Greensboro, NC | 240,000 | 6-inch InP — CPO CW/UHP lasers | Acquired Mar 2026 for $38M; production mid-2028 |
| United Kingdom | 183,000 | Components | Owned; purchased Aug 2023 for $23M |
| Vipava, Slovenia | 36,000 | Components | Owned |
| Shenzhen, China | — | Datacom assembly (legacy) | SOLD Mar 2025; $47.8M net, $34.9M gain |

A few things stand out in the table. First, Lumentum is now an owner of fabs and factories, not a renter. Five of the seven sites are owned freehold, including three InP wafer fabs (Sagamihara, San Jose, and Greensboro from mid-2028) — a vertical-integration posture that is unusual for a $2B-revenue components company and which is being financed partly by the convertible structure described in the next section. Second, the geographic distribution — Thailand, Japan, US (CA + NC), UK, Slovenia — is deliberately allied-country and excludes mainland China after the Shenzhen exit. Third, the supplier commitments behind these sites are accelerating ahead of the buildings: total purchase obligations grew from $837.0M at June 2025 to $1,795.6M at March 2026 — a 115% increase in nine months and the cleanest single-line evidence of step-function supply commitments to back hyperscaler contracts[^1].

The Thailand concentration is a real exposure. The Q3 FY26 10-Q calls out "higher U.S. tariffs on the import of certain products manufactured in Thailand or China (and vice-versa)" as a discrete risk, and the FY25 10-K Risk Factors flag "the conflict between Cambodia and Thailand" as a geopolitical concern — a sentence that would have read as boilerplate two years ago and reads as live risk today[^1]. Greensboro is the right structural hedge but, again, doesn't ship product until mid-2028; for the next eight quarters, a tariff regime or a regional flare-up in Southeast Asia would land directly on the largest owned site in the company. Why this matters: the capex curve, the Thailand square footage, and the $1.8B purchase-obligations line are the leading indicators of a revenue print Lumentum has not yet booked — management is pre-building a factory base sized for a $4B+ datacom year, and the bet only works if the EML and CPO laser orders actually materialize on schedule.

## 7. The convertible tower — $3.18B of notes, $19.1B of fair value, and the dilution already underway

Strip away the optics narrative and Lumentum's capital structure looks like a venture-stage equity story stapled onto a mid-cap balance sheet. The company carries four tranches of convertible senior notes totaling $3,183.4M in carrying value as of March 28, 2026 — but those same notes mark to a fair value of $19,074.7M, an embedded equity overhang nearly six times the face amount[^1]. Every series is deep in-the-money, every conversion price sits below the May 2026 share price, and the conversion machinery is no longer hypothetical: it is grinding forward in real time. The 8-K filed April 7, 2026 disclosed that $474.6M of principal — $264.8M of the 2026 Notes and $209.8M of the 2029 Notes — had already been retired in exchange for roughly 5.7M new common shares[^24]. By April 30, conversion requests had climbed to $500.8M, and that figure is still ticking[^1].

The arithmetic is unforgiving once you lay out the tranches side by side. The 2029 Notes, struck at $69.54, are by far the most equity-like: a $600.9M carrying balance trades for $6,262.3M of fair value — a ~10x mark[^1]. The 2026 and 2028 Notes, at $99.29 and $131.03 conversion prices, are also deeply in-the-money but closer to maturity, which is why they are converting first. The 2032 Notes, issued in September 2025 at a $187.77 conversion price with a capped call extending economic exposure to $244.10, are the only tranche with meaningful upside cushion before dilution begins to pinch the holder[^1].

| Series | Coupon | Carrying ($M) | Fair Value ($M) | Conv. Price | Status |
|---|---|---|---|---|---|
| 2026 Notes | 0.50% | 468.3 | 3,328.0 | $99.29 | Actively converting |
| 2028 Notes | 0.50% | 858.5 | 4,617.2 | $131.03 | Deep ITM |
| 2029 Notes | 1.50% | 600.9 | 6,262.3 | $69.54 | ~10x mark; converting |
| 2032 Notes | 0.375% | 1,255.7 | 4,867.2 | $187.77 (cap $244.10) | ITM, capped call cushion |
| **Total** |  | **3,183.4** | **19,074.7** |  |  |

Layered on top of the converts is the NVIDIA Series A Convertible Preferred — approximately 2.9 million shares purchased at $695.31 on March 2, 2026 for an aggregate $2.0B investment, convertible 1-for-1 into common stock once HSR clearance lands[^1]. At the May 2026 trading level of roughly $1,000 per share, NVIDIA's preferred is already approximately 44% in-the-money on a paper-mark basis before it has even converted[^17]. That single instrument adds another 2.9M shares to the diluted count the moment regulatory approval closes.

The dilution arithmetic is already visible in the share count. As of March 28, 2026, common shares outstanding were 71.7M — but weighted-average diluted shares for Q3 FY26 came in at 96.2M under the if-converted method, which assumes every convert tranche settles in stock[^1]. That's a 34% gap between the common float and the fully-diluted equity story, and it's growing every quarter as exchanges close. The April 2026 exchange alone moved 5.7M shares from "if-converted" to actually-issued; the NVIDIA preferred will move another 2.9M; and the residual $2.7B of carrying-value notes still sitting on the balance sheet will, on current trajectories, convert too.

What makes the structure unusual is that management has been actively retiring converts with converts, not with cash. The September 2025 issuance of the 2032 Notes raised $1,265M (including greenshoe), of which $843.1M was immediately deployed to repurchase 2026 Notes and $102.0M to fund a capped call on the new tranche[^1]. No common-stock repurchase activity occurred in the first nine months of FY26 — the $1B buyback authorization sitting on the books since 2022 remains entirely untouched[^1]. Every dollar of "shareholder return" has, in practice, been a dollar of convertible-debt refinancing. And the cash to defend the equity is sitting there: $2,617.8M in cash plus $554.5M in short-term investments brought total liquidity to $3,172.3M at March 2026, up from just $520.7M at FY25 close — a >6x increase driven largely by the NVIDIA investment and the 2032 Notes proceeds[^1].

The bull case is that this is exactly the kind of capital structure a hyperscale supplier should have during a build-out: the stock has run roughly 10x in twelve months, so issuing another 25M shares to settle the converts costs roughly $25B at the current quote — a price tag the equity can absorb because the underlying earnings power is moving with it. The bear case is that the optionality is asymmetric — on any future date when LITE corrects, the converts and the NVIDIA preferred crystallize as a permanent overhang that limits multiple expansion, because every marginal buyer is bidding against a known queue of in-the-money instruments waiting to settle. Why this matters: Lumentum is no longer a 70-million-share company — it is functionally a 96-million-share company that hasn't finished printing the certificates, and any per-share valuation that anchors on the common float is mispricing the structure by roughly a third.

## 8. Competitive frame — Coherent at 6 inches, Innolight at 60%, and the US chip moat

Lumentum's 800G/1.6T story is compelling on its own terms, but the company sells into a market with one credible Western peer, one dominant contract manufacturer, and a Chinese module-maker bloc that already owns the majority of NVIDIA's wallet. Understanding how value is partitioned across that stack — chips, modules, assembly — is the key to underwriting whether Lumentum's current margin trajectory is durable or whether it compresses back toward commodity optics economics by 2027.

Start with the direct comparable. Coherent (COHR) reported Q3 FY26 revenue of $1.81B, up 21% year-over-year, with the combined Datacenter & Communications segment growing roughly 40% YoY to $1.36B[^12]. Those are excellent numbers in absolute terms, but Lumentum's consolidated growth is running roughly three times faster on a YoY basis, and Lumentum's non-GAAP gross margin of 47.9% sits ~830 basis points above Coherent's 39.6% non-GAAP gross margin[^12]. The gap reflects two things: Lumentum's higher mix of merchant EMLs (which carry chip-like margins) versus Coherent's broader exposure to lasers, materials, and networking subsystems; and Coherent's still-in-progress manufacturing consolidation following the II-VI/Coherent merger.

Fabrinet (FN) is the third leg of the Western stool, but it competes differently — as the contract manufacturer that assembles many of Lumentum's and Coherent's modules. Fabrinet's Q3 FY26 revenue hit a record $1.214B (+39% YoY), with optical communications at $889M (73% of total) and telecom at a record $628M (+55% YoY)[^25]. The interesting tell is inside the datacom line: DCI modules grew +90% YoY to $197M, but the broader datacom segment grew only +4% YoY to $260M, with management explicitly citing "broadening component and material supply constraints" — which in plain English means EML and DSP allocation[^25]. Fabrinet's bottleneck is Lumentum's pricing power.

| Metric (Q3 FY26) | Lumentum (LITE) | Coherent (COHR) | Fabrinet (FN) |
|---|---|---|---|
| Total revenue | $808.4M | $1.81B | $1.214B (record) |
| Revenue YoY growth | +90% | +21% | +39% |
| Non-GAAP gross margin | 47.9% | 39.6% | ~12-13% |
| Datacom/DC growth YoY | Systems +121% | Datacenter & Communications +40% | Datacom +4%; DCI +90% |
| Strategic moat | 200G EML chip capacity | 6-inch InP wafer scale | Vertically integrated assembly |

The 800G volume picture is the uncomfortable part of the bull thesis. Innolight and Eoptolink together supply roughly 60% of NVIDIA's 800G module orders, with the remaining 40% split among Coherent, Lumentum, and Broadcom[^26]. Innolight's 2024 revenue reached ¥23.86B (+122.6% YoY) with net profit up 137.9%; Eoptolink posted ¥8.65B in revenue (+179%) and net profit up 312%[^26]. Seven of the top ten optical-module suppliers globally were Chinese in 2024, up from two in 2016[^27]. At the module assembly layer, the share war is essentially over.

But — and this is the load-bearing claim of the Lumentum bull case — the DSP chips and EML lasers inside those Chinese-assembled modules are still sourced from Broadcom, Marvell, Lumentum, and Coherent[^27]. Marvell's Ara DSP (3nm, 200G/lane) is shipping in mass volume[^28], and Broadcom launched its competing 3nm PAM-4 DSP (Taurus BCM83640) on March 11, 2026 — meaning two Western merchant DSP suppliers capture economic rent regardless of which Asian module house wins a given NVIDIA SKU[^29]. The same logic applies to EMLs: Lumentum and Coherent are the qualified merchant suppliers at 200G/lane today. The chokepoint is one layer below where the share war is being fought.

NVIDIA's behavior reinforces this framing. The $2B investments into Lumentum and the parallel ~$2B commitment into Coherent are best read not as picking a winner but as deliberately funding a Western chip-supplier duopoly — a hedge against single-vendor risk at the EML/DSP layer while letting the Chinese module assemblers continue to compete at the box level[^16]. The optical-component TAM justifies the spend: total optical-component revenue reached ~$25B in 2025, with datacom alone above $19B (+70% YoY) and consensus pointing to 20%+ CAGR from here[^30,36].

The single most concrete threat to Lumentum's margin advantage is Coherent's 6-inch InP wafer ramp. Coherent claims the world's first 6-inch InP scalable wafer fabs in production, with ~4x the device count per wafer and a stated >60% reduction in die cost versus 3-inch[^11]. If Coherent qualifies 200G EMLs on 6-inch through late 2026 and into 2027, the per-die cost gap that today underwrites Lumentum's gross-margin premium narrows materially, and the ~800bps spread between LITE (47.9%) and COHR (39.6%) likely compresses. Layer on top of that the slow improvement of Chinese chip producers — Source Photonics, Yuanjie, Almae — on linewidth and RIN; if any of them reach 200G/lane parity by 2027, the chip moat that the entire bull thesis rests on starts to erode from both directions simultaneously. Why this matters: Lumentum's premium multiple is not really a bet on optical modules — it is a bet that the value-capture line inside an AI optical transceiver stays exactly where it is today, at the EML and DSP layer, for at least the next 24-36 months. Coherent's 6-inch fab is the clock on that bet.

## 9. Industrial Tech, now a footnote — how the Apple VCSEL business went from the story to a disclosure item

For most of Lumentum's first eight years as a public company, the headline franchise was not telecom — it was Industrial Tech: VCSEL arrays for Apple Face ID and LiDAR, kilowatt fiber lasers, and ultrafast micromachining tools sold into consumer electronics and semicap. That book has collapsed with extraordinary speed. Segment revenue went from $444.5M in FY23 to $274.3M in FY24 to $234.2M in FY25 — a 47% decline in two years — and segment profit fell from $152.7M to $12.1M, a 92% evaporation of operating contribution[^3]. Mix share fell in lockstep: 25.2% of revenue in FY23, 20.2% in FY24, 14.2% in FY25, and roughly 8% pro-forma in FY26 as the cloud datacom line scales past $2B run-rate[^3].

The reporting structure caught up to the economics. In the first quarter of fiscal 2026, Lumentum told investors it had "implemented a re-organization, and we are now managed as a single, integrated enterprise," and retired the Cloud & Networking / Industrial Tech split entirely[^1]. The new disclosure is a Components vs. Systems product cut, which has the convenient effect of making the legacy industrial book invisible to anyone not willing to back into it. Industrial Tech is no longer a segment. It is a footnote.

| Period | Industrial Tech revenue | Segment profit | Op margin | % of total |
|---|---|---|---|---|
| FY23 | $444.5M | $152.7M | 34.4% | 25.2% |
| FY24 | $274.3M | ~$1.1M | 0.4% | 20.2% |
| FY25 | $234.2M | $12.1M | 5.2% | 14.2% |
| FY26E | ~$170M (pro-forma) | n/d | n/d | ~8% |

The proximate cause is consumer 3D sensing. Lumentum's own MD&A attributes the drop to "a decline in unit sales of our imaging and sensing products due to higher market competition in the consumer end-market for these products."[^3] The specific competitive event was Sony's displacement of Lumentum on the iPhone 15 Pro and Pro Max time-of-flight VCSEL for LiDAR — Sony shipped an integrated VCSEL-plus-driver-IC with lower power consumption, an architectural advantage Lumentum's discrete approach could not match[^31]. The financial fingerprint is visible in the customer concentration table: Customer A (almost certainly Apple) ran 15.3% of revenue in FY23, troughed at 11.4% in FY24, and recovered to 16.0% in FY25 as the dot-projector business stabilized even after the LiDAR loss[^3].

It would be wrong, however, to read the entire collapse as a laser franchise in decline. The industrial laser sub-segment — fiber and ultrafast — actually grew by $17.5M year-over-year in FY25, driven by ultrafast lasers shipping into solar cell manufacturing[^3]. The $210M two-year decline is almost entirely a VCSEL share-loss story layered on top of a modestly growing laser tools business.

What Lumentum has not done is the obvious adjacent move. A full-text search of the FY25 10-K returns zero hits for "aerospace" and zero for "directed energy"; the three mentions of "defense" are all ITAR and litigation boilerplate[^3]. Compare the peer set: IPG Photonics is shipping the CROSSBOW counter-UAS laser system, nLight has a fast-growing Defense segment with directed-energy contracts, and Coherent has a dedicated aerospace and defense vertical. The DoD directed-energy budget is one of the few growth pockets in laser-tools land, and Lumentum has chosen — or by inaction defaulted — not to compete for it.

The counterpoint is that calling Industrial Tech a footnote may be premature. The iPhone 17 cycle that launched in September 2025 brought what Lumentum characterized as "modest growth following a new smartphone launch and some incremental share gains" in 3D sensing — the first positive share commentary in years[^33]. Segment operating margin in Q4 FY25 rebuilt to roughly 6% from 0.4% in the prior year as the fixed-cost base normalized[^32]. If 3D-sensing share stabilizes and ultrafast lasers continue gaining in semicap and solar, the legacy book could re-stabilize at $300-400M annually at a mid-teens operating margin — still dwarfed by the AI line, but meaningful in absolute dollars and free cash flow. Why this matters: Lumentum's identity has flipped violently in 24 months, from an Apple supplier with a telecom side business to an NVIDIA supplier with a consumer-electronics side business. The Industrial Tech line is a useful reminder that single-customer concentration in a discrete-component architecture is a structurally fragile position — and that the same dynamic now applies, in reverse, to the hyperscaler EML business that has replaced it.

## 10. What could break the thesis

An honest read of the Lumentum story requires holding the bull and the bear case in the same hand. Every chokepoint advantage described in the preceding sections has a specific event that would invalidate it, and most of those events are not low-probability tail risks — they are technology and policy developments already underway in 2026. The point of this section is to enumerate them concretely, not to handicap probabilities.

**(a) The 200G EML moat closes faster than expected.** Coherent's 6-inch indium phosphide wafer line is in production today; the company's stated 4x dies-per-wafer and >60% die-cost reduction would, if qualified for 200G EMLs in 2027, invert the wafer-economics gap that underwrites Lumentum's ~830 bps non-GAAP gross-margin lead[^11]. The bull rebuttal is that wafer scaling does not deliver linewidth or RIN parity, and Coherent has continued to buy EMLs from Lumentum during the ramp — a behavior inconsistent with imminent self-sufficiency. But the clock is real. If the gross-margin premium compresses by even 500 bps, ~$150M of FY27 EBITDA evaporates against current consensus.

**(b) Monolithic InP-on-Si makes the ELSFP socket obsolete.** The CPO pivot described in Section 5 only works because NVIDIA and Broadcom chose to keep lasers external in this generation for thermal and serviceability reasons. TSMC's COUPE silicon-photonics platform and Marvell's reported acquisition of Celestial AI are both directional bets on heterogeneous integration — bonding indium phosphide lasers directly onto the silicon photonic die (==deal price unverified at primary source==). If that integration matures into a production-grade flow by 2028, Lumentum's multi-hundred-million-dollar UHP laser PO is its last large CPO socket order. The transceiver TAM continues; the external-laser annuity does not.

**(c) Hyperscaler capex digests.** The single biggest macro variable in the FY27 model is whether the Big-4 hyperscalers continue to ramp capex at the +77% YoY pace implied by 2026 guides totaling roughly $725 billion[^35]. Meta's stock reacted negatively to its Q1 2026 capex raise as investors began openly questioning ROI on training spend[^35]. If 2027 hyperscaler capex grows 20% instead of 50%, the optical-component TAM still grows — but it grows into the supply that Lumentum, Coherent, and the Japanese duopoly are simultaneously building. Pricing power inverts in roughly two quarters when an EML supply gap closes.

**(d) Single-customer cliff risk.** Two customers were 38% of Q3 FY26 revenue[^1]. If either of them — Google appears to be one per CEO commentary[^9] — decides to dual-source to Coherent or to insource via M&A, the revenue trajectory bends. Hyperscalers have a track record of doing exactly this once a component category matures: Apple did it on the iPhone 15 Pro LiDAR VCSEL, displacing Lumentum with Sony[^31]. The same architectural dynamic — a Western chip vendor displaced by a captive, vertically-integrated alternative once volumes justify it — is precisely what would derail the AI optics story.

**(e) Chinese vertical integration in EMLs.** Chinese module makers (Innolight, Eoptolink) already hold ~60% of NVIDIA's 800G module orders[^26]; today they remain buyers of Western EML chips. If Source Photonics, Yuanjie Semiconductor, or Almae reach 200G/lane parity by 2027 — a stated ambition with state-backed capex behind it — Lumentum loses access to the largest module-assembly volume in the AI build. Even if Western hyperscalers refuse to qualify Chinese EMLs on national-security grounds, the Chinese domestic AI market (Alibaba, Tencent, Baidu, ByteDance) is large enough to anchor a parallel supply chain that lowers the global ASP floor.

**(f) Tariffs and Thailand concentration.** The Q3 FY26 10-Q explicitly flags "higher U.S. tariffs on the import of certain products manufactured in Thailand" as a discrete risk; the FY25 10-K Risk Factors even cite "the conflict between Cambodia and Thailand" as a geopolitical concern[^1]. With Thailand carrying $328M of PP&E and 22% of Q3 FY26 ship-to revenue, a 10-15% tariff regime would compress gross margin by roughly 300-500 bps before mitigation[^1]. The Greensboro fab is the structural hedge, but it does not ship until mid-2028.

**(g) Dilution mathematics catch up with the multiple.** The $3.18B carrying / $19.1B fair-value convertible stack plus NVIDIA's $2.0B preferred imply a fully-diluted share count moving from ~72M common to ~100M+ by year-end FY27[^1]. Every per-share metric on the income statement is therefore being asked to grow against a denominator that is itself growing ~3-4% per quarter as exchanges close. A 28x TTM EV/sales multiple[^17] implicitly demands that the bull case described in Sections 1-6 not merely materialize but materialize at a pace fast enough to absorb the dilution.

**(h) Insider selling pattern.** In May 2026 alone, insiders sold approximately $19.8M of stock under 10b5-1 plans adopted in February 2026[^34]. Director Brian Lillie sold $11.7M, retaining a fraction of his pre-sale position; CFO Wajid Ali sold ~$3.7M earlier in the year; several other officers followed. None of this is dispositive — the plans were established when the stock was materially lower — but the magnitude of selling into the all-time high is a data point worth weighing against the management narrative that the company is sold out through 2027.

The unifying observation across these risks: Lumentum's premium valuation is not really paying for the +90% YoY revenue print or the 47.9% gross margin in isolation. It is paying for the proposition that the chokepoint stays a chokepoint — that 200G EMLs remain supply-constrained through 2027, that the ELSFP socket remains the chosen CPO architecture, that NVIDIA's $2B purchase commitment activates in volume, and that the customer concentration is durable rather than catastrophic. Each of the eight items above is a specific bet against one of those propositions, and the company's $70-95B market cap implies the market is treating each as low-probability. The thoughtful investor's job is to decide whether that pricing is right.

## References

:::references
- id: 1
  title: Lumentum Holdings Inc., Form 10-Q for the quarterly period ended March 28, 2026, filed May 6,
    2026 with the SEC
  url: https://www.sec.gov/Archives/edgar/data/1633978/000162828026030777/lite-20260328.htm
- id: 2
  title: '"Lumentum Announces Third Quarter of Fiscal Year 2026 Financial Results," Lumentum Investor
    Relations press release, May 5, 2026'
  url: https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx
- id: 3
  title: Lumentum Holdings Inc., Form 10-K for the fiscal year ended June 28, 2025, filed August 19, 2025
    with the SEC
  url: https://www.sec.gov/Archives/edgar/data/1633978/000162828025040830/lite-20250628.htm
- id: 4
  title: '"Lumentum touts AI optics boom: $2B quarterly target, new fab and 1.6T transceiver shipments,"
    Daily Political, March 21, 2026'
  url: https://www.dailypolitical.com/2026/03/21/lumentum-touts-ai-optics-boom-2b-quarterly-target-new-fab-and-1-6t-transceiver-shipments.html
- id: 5
  title: '"Lumentum to Acquire Cloud Light to Accelerate Data Center Speed and Scalability," Business
    Wire press release, October 30, 2023 (retrieved via Internet Archive)'
  url: https://www.businesswire.com/news/home/20231030099888/en/Lumentum-to-Acquire-Cloud-Light-to-Accelerate-Data-Center-Speed-and-Scalability
- id: 6
  title: '"Lumentum Announces Fiscal First Quarter 2024 Financial Results," Lumentum press release, November
    7, 2023'
  url: https://www.lumentum.com/en/media-room/news-releases/lumentum-announces-fiscal-first-quarter-2024-financial-results
- id: 7
  title: '"Lumentum and the Laser Bottleneck," Chipstrat newsletter, 2025'
  url: https://www.chipstrat.com/p/lumentum-and-the-laser-bottleneck
- id: 8
  title: '"Lumentum: Laser Demand, OCS, CPO & Optical Scale-Up," Vik''''s Newsletter, 2025'
  url: https://www.viksnewsletter.com/p/lumentum-laser-demand-ocs-cpo-optical-scaleup
- id: 9
  title: Lumentum Holdings, Q3 FY2026 earnings call transcript, May 6, 2026, The Motley Fool
  url: https://www.fool.com/earnings/call-transcripts/2026/05/06/lumentum-lite-q3-2026-earnings-transcript/
- id: 10
  title: '"Lumentum''''s AI Supply Squeeze: Why Demand Far Exceeding Supply Creates a Compelling Risk-Reward,"
    BeyondSPX, 2026'
  url: https://www.beyondspx.com/quote/LITE/lumentum-s-ai-supply-squeeze-why-demand-far-exceeding-supply-creates-a-compelling-risk-reward-nasdaq-lite
- id: 11
  title: '"World''''s First 6-Inch InP Scalable Wafer Fabs: Paving the Way for the Next Generation of
    Lasers for AI Transceivers and 6G Wireless Networks," Coherent Corp press release, 2025'
  url: https://www.coherent.com/news/press-releases/worlds-first-6-inch-inp-scalable-wafer-fabs-paving-the-way-for-the-next-generation-of-lasers-for-ai-transceivers-and-6g-wireless-networks
- id: 12
  title: '"Coherent Corp. Reports Third Quarter Fiscal 2026 Results," Globe Newswire, May 6, 2026'
  url: https://www.globenewswire.com/news-release/2026/05/06/3289361/11543/en/coherent-corp-reports-third-quarter-fiscal-2026-results.html
- id: 13
  title: '"Lumentum Sold Out Through 2027 as AI Demand Creates Unprecedented Supply Tightness," Stocks
    Foundry, December 10, 2025'
  url: https://www.stocksfoundry.com/articles/lumentum-sold-out-through-2027-as-ai-demand-creates-unprecedented-supply-tightness-20251210
- id: 14
  title: '"Lumentum Demonstrates Industry-Leading Technologies and Products for Scale-Out, Scale-Up and
    Scale-Across AI Infrastructure at OFC 2026," Lumentum IR press release, March 17, 2026'
  url: https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx
- id: 15
  title: '"NVIDIA Announces Strategic Partnership with Lumentum to Develop State-of-the-Art Optics Technology,"
    NVIDIA newsroom, March 2, 2026'
  url: https://nvidianews.nvidia.com/news/nvidia-announces-strategic-partnership-with-lumentum-to-develop-state-of-the-art-optics-technology
- id: 16
  title: '"NVIDIA and Coherent Announce Strategic Partnership to Develop Optics Technology to Scale Next-Generation
    Data Center Architecture," NVIDIA newsroom, March 2, 2026'
  url: https://nvidianews.nvidia.com/news/nvidia-and-coherent-announce-strategic-partnership-to-develop-optics-technology-to-scale-next-generation-data-center-architecture
- id: 17
  title: Yahoo Finance, LITE quote and historical statistics
  url: https://finance.yahoo.com/quote/LITE
- id: 18
  title: '"NVIDIA Announces Spectrum-X Co-Packaged Optics Networking Switches for AI Factories," NVIDIA
    newsroom, March 18, 2025'
  url: https://nvidianews.nvidia.com/news/nvidia-spectrum-x-co-packaged-optics-networking-switches-ai-factories
- id: 19
  title: '"UHP Lasers for CPO," Lumentum product page, accessed May 2026'
  url: https://www.lumentum.com/en/products/data-center/cw-lasers/uhp-lasers-cpo
- id: 20
  title: Lumentum Holdings, Q2 FY2026 earnings call transcript, February 3, 2026, The Motley Fool
  url: https://www.fool.com/earnings/call-transcripts/2026/02/03/lumentum-lite-q2-2026-earnings-call-transcript/
- id: 21
  title: '"Broadcom Announces Tomahawk 6-Davisson, Industry''''s First 102.4 Tbps Co-Packaged Optics Ethernet
    Switch," Broadcom Investor Relations press release, October 8, 2025'
  url: https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-tomahawkr-6-davisson-industrys-first-1024
- id: 22
  title: '"NVIDIA''''s CPO is the First Step in a Long Journey," LightCounting Research Note, March 2025'
  url: https://www.lightcounting.com/research-note/march-2025-nvidias-cpo-is-the-first-step-in-a-long-journey-395
- id: 23
  title: '"Thailand lands $70m investment from Lumentum for AI chipmaking," Nikkei Asia, October 2025'
  url: https://asia.nikkei.com/business/tech/semiconductors/thailand-lands-70m-investment-from-lumentum-for-ai-chipmaking
- id: 24
  title: Lumentum Holdings, Form 8-K disclosing privately negotiated exchange transactions, filed April
    7, 2026
  url: https://www.stocktitan.net/sec-filings/LITE/8-k-lumentum-holdings-inc-reports-material-event-e0d77648ecca.html
- id: 25
  title: Fabrinet, Q3 FY2026 earnings call transcript, May 4, 2026, The Motley Fool
  url: https://www.fool.com/earnings/call-transcripts/2026/05/04/fabrinet-fn-q3-2026-earnings-transcript/
- id: 26
  title: '"Nvidia Orders Surge: Innolight and Eoptolink Dominate 60% of 800G SFP Optical Modules Supply,"
    IP Fiber, May 2025'
  url: https://ip-fiber.com/blogs/news/nvidia-orders-surge-innolight-and-eoptolink-dominate-60-of-800g-sfp-optical-modules-supply
- id: 27
  title: '"Chinese Optical Modules Own 7 of the Top 10," PhotonCap analysis'
  url: https://photoncap.net/p/chinese-optical-modules-own-7-of
- id: 28
  title: '"Marvell Introduces Industry''''s First 1.6T Optical DSP for AI Data Center Connectivity," Marvell
    newsroom'
  url: https://www.marvell.com/company/newsroom/marvell-1-6t-optical-dsp-ai-data-center-connectivity.html
- id: 29
  title: '"Broadcom''''s DSP Launch Intensifies the AI Optics Race with Marvell," Futurum Group, March
    2026'
  url: https://futurumgroup.com/insights/broadcoms-dsp-launch-intensifies-the-ai-optics-race-with-marvell/
- id: 30
  title: '"Optical Component Revenue Reaches Nearly $25B in 2025," Cignal AI, January 2026'
  url: https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/
- id: 31
  title: '"Face ID for the iPhone 15 Pro Will Use Time-of-Flight VCSEL Technology from Sony, Replacing
    Lumentum," Patently Apple, February 24, 2023'
  url: https://www.patentlyapple.com/2023/02/face-id-for-the-iphone-15-pro-will-use-time-of-flight-vcsel-technology-from-sony-replacing-lumentum-.html
- id: 32
  title: '"Lumentum reports Q4 FY25 results," Semiconductor Today, August 22, 2025'
  url: https://www.semiconductor-today.com/news_items/2025/aug/lumentum-220825.shtml
- id: 33
  title: '"Lumentum reports Q2 FY26 results," Semiconductor Today, February 9, 2026'
  url: https://www.semiconductor-today.com/news_items/2026/feb/lumentum-090226.shtml
- id: 34
  title: Lumentum Holdings, SEC Form 4 filings, May 2026 (Brian Lillie, Pamela Fletcher, Ian Small, Jae
    Kim)
  url: https://www.stocktitan.net/sec-filings/LITE/form-4-lumentum-holdings-inc-insider-trading-activity-7d7c7adbab46.html
- id: 35
  title: '"Big Tech''''s AI Spending Plans Reach $725 Billion," Fortune, April 29, 2026'
  url: https://fortune.com/2026/04/29/microsoft-meta-google-ai-capex-spending-billions/
- id: 36
  title: '"Datacom Optical Component Revenue Surpasses $19B in 2025," Cignal AI, April 2026'
  url: https://cignal.ai/2026/04/datacom-optical-component-revenue-surpasses-19b-in-2025/
:::
