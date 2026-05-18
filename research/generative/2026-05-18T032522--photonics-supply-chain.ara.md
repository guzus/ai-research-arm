---
eyebrow: AI infrastructure · Supply chain
title: 'The photonics supply chain: how AI''s optical bill of materials concentrates onto a few dozen companies'
deck: A 1-millimeter indium phosphide laser, a 3-nanometer DSP, a 45-nanometer photonic IC, a Chinese
  assembly line, a Japanese fiber draw tower. Trace the dollars in any AI cluster's optics back to
  source and you find the same handful of names.
lede: 'In the eighteen months between October 2024 and May 2026, the AI photonics supply chain went
  from analyst footnote to the single most concentrated dependency in the hyperscaler stack. NVIDIA
  wrote $4 billion of equity into Lumentum and Coherent on the same day in March 2026, then another
  $500 million plus up to $3.2 billion of Corning warrants two months later — $7 billion of vertical
  integration that nobody had modeled. Combined hyperscaler capex stepped from roughly $400 billion in
  2025 to a guided $660–690 billion in 2026[^74], with optical transceivers now sized at $26 billion against
  shipments that LightCounting says will fall ~30% short of demand[^4]. Beneath those headline numbers sits
  a stack: an indium phosphide substrate market controlled by four companies, an EML laser oligopoly of
  five, a merchant DSP duopoly of two, a silicon-photonics PIC foundry race led by TSMC, a Chinese
  module-assembly bloc that captures more than half of NVIDIA''s wallet at 33–47% gross margin, a fiber
  layer in which Corning effectively touches both the glass and the connector, and switches that are
  collapsing pluggable optics into the package. This report walks layer by layer through who actually
  builds what, where the dollars accrue, where the chokepoints sit, and where the thesis is most
  likely to break.'
stats:
- label: 2026 transceiver TAM
  value: $26B
  note: LightCounting, +60% YoY
- label: '800G+ unit shipments 2026'
  value: 63M
  note: +163% YoY
- label: NVIDIA equity in optics
  value: $7B+
  note: LITE, COHR, GLW combined
- label: Hyperscaler capex 2026
  value: ~$680B
  note: +65% YoY
- label: EML supply gap 2025
  value: ~50%
  note: ~20M cap vs ~40M demand
- label: Lumentum 1Y return
  value: +921%
  note: Jun-25 → May-26
---

## 1. The shape of the stack

Strip an 800G or 1.6T optical transceiver down to its component flow chart and the chain of custody is depressingly short. A bulk wafer of indium phosphide comes from one of four companies in the world. An epitaxial growth tool from Aixtron or Veeco lays down the active layers. A laser-chip vendor — one of five — dices out an electro-absorption modulated laser (EML) or a continuous-wave distributed-feedback (CW DFB) laser. A merchant DSP from Marvell or Broadcom (or, increasingly, Credo or Acacia/Cisco) does the signal processing. A photonic integrated circuit (PIC) from TSMC, GlobalFoundries, or Tower handles the waveguides and modulators. A Chinese contract assembler — typically Innolight or Eoptolink — bonds the chips, drops in the optics, screws on a connector from US Conec or Senko, splices it to single-mode fiber from Corning or Furukawa, and ships it to one of five buyers: Microsoft, Meta, Alphabet, Amazon, or NVIDIA itself.

At every layer the supplier count is single digits, and at most layers it is *small* single digits. {accent}This is the only place in the AI stack — not GPUs, not HBM, not power — where the entire merchant supply base for a critical generation of hardware can be enumerated on one hand at every level{/}. The 1-millimeter InP die that costs $14–20 and weighs nothing[^1,2] sits on the critical path of every NVIDIA rack and every TPU pod scheduled to ship through 2027.

The dollar shape of the stack is the second surprise. Optical transceiver sales reached $23.8 billion in 2025 per LightCounting, with 24 million 800G-and-faster units shipped, jumping ~2.6× to ~63 million in 2026[^3]. The April 2026 LightCounting forecast puts AI-cluster-specific optics (transceivers + LPO + CPO) at $5B (2024) → $16.5B (2025) → $26B (2026), a +60% YoY step with demand exceeding supply by roughly 30%[^4]. Dell'Oro projects roughly 100 million cumulative 800G + 1.6T switch-port shipments through 2028 and AI back-end network spending past $20B by 2028[^5]. Yet optical transceivers still represent only about 3.1% of the top-five hyperscalers' capex in 2026, rising to 4.1% by 2031[^4] — a sliver of the dollar pie that exerts vastly disproportionate leverage on whether the GPUs in the racks can talk to each other.

:::rank-list
- {label: "InP wafers — Sumitomo Electric (Japan)", value: "~60%", pct: 100, highlight: true}
- {label: "EML chips — Lumentum (US)", value: "50–60%", pct: 92}
- {label: "PIC packaging — TSMC COUPE (Taiwan)", value: "1.6T anchor", pct: 85}
- {label: "Merchant 1.6T DSP — Marvell + Broadcom", value: "~80%", pct: 80}
- {label: "Transceiver modules — Innolight (China)", value: ">50% NVIDIA wallet", pct: 78}
- {label: "Single-mode fiber + MTP connector — Corning ecosystem", value: "duopoly+", pct: 70}
- {label: "Co-packaged switch silicon — NVIDIA + Broadcom", value: "≥ 200 Tb/s shipping", pct: 65}
- {label: "Optical assembly CM — Fabrinet (Thailand)", value: "27.6% NVDA in FY25", pct: 55}
:::

What the rank-list above hides is that the concentration intensifies as you move *up* the stack — closer to the InP die — and softens as you move *down* — closer to the buyer. The substrate layer is a four-name oligopoly with one of them (Sumitomo) at ~60% share of the 4-inch Fe-doped semi-insulating segment[^6]. The EML chip layer is a five-name oligopoly with one of them (Lumentum) at 50–60% share and the only volume 200G/lane supplier[^7]. The DSP layer is a two-name merchant duopoly (Marvell + Broadcom) with three challengers (Credo, MaxLinear, Cisco/Acacia)[^8,9,10]. The module layer is more fragmented in vendor count (Innolight, Eoptolink, Coherent, Fabrinet, AAOI, Accelink) but more concentrated in customer share — Innolight alone reportedly holds >50% of NVIDIA's transceiver wallet[^11]. The pattern matters because the dollars accrue at the *concentrated* layers when supply is tight, and at the *fragmented* layers when supply is loose. In 2025 and 2026, supply has been tight at every layer.

The remainder of this report walks the stack from substrate up, treats Lumentum as one node rather than the focus (the company already has a standalone report in this archive), and quantifies the dollars, gross margins, and chokepoints at each layer. The closing sections cover the buyer-funded vertical-integration plays, the geopolitics that gate them, and the falsifiers that would re-rate the whole stack downward.

## 2. The wafer floor — indium phosphide and the 6-inch reset

The deepest chokepoint in the stack is also the smallest market in dollars. The merchant InP wafer business throws off only a few hundred million dollars a year at the substrate level — but every 200G EML laser, every CW DFB for co-packaged optics, every photonic detector and every InP-based transceiver chip is grown on a wafer from one of four producers: Sumitomo Electric and JX Advanced Metals in Japan, AXT in the US, and the Coherent / II-VI / JX consortium that, together, "monopolize more than 95% of the global production capacity" per Chinese industry data[^6].

InP is not silicon. It is a notoriously brittle III-V semiconductor whose yields are sensitive to point defects measured in tens of atoms; epitaxial growth tolerances are sub-nanometer; and the historic wafer size — 2-inch, 3-inch, and 4-inch — has resisted the scaling that silicon long ago took for granted. {accent}The structural reset of the InP market is the transition to 6-inch (150 mm) wafers{/}, which delivers roughly four times the number of dies per wafer and, per Coherent's 2024 announcement of the industry's first 6-inch InP scalable fabs, more than 60% reduction in die cost versus the 3-inch lines that preceded them[^12].

:::donut(center-label="InP")
- {label: "Sumitomo Electric (4-inch Fe-doped SI)", value: 60}
- {label: "AXT / Tongmei (VGF)", value: 35}
- {label: "JX + II-VI / Coherent (combined)", value: 5}
:::

Sumitomo's November 2025 IR deck is the cleanest single document on substrate capacity. The company guides InP substrate capacity to 2× by 2026 and 2.4× by 2028 versus a 2023 base; intra-datacenter optical-device capacity to 4× by 2024, **12× by 2026** and 13.4× by 2028; and — perhaps most consequentially — a chip-mix forecast in which EML's share of the company's own datacenter laser shipments falls from 76% in 2024 to 31% in 2028 while CW-LD (the light source for co-packaged optics) climbs from 24% to 69%[^1]. Sumitomo also reveals that its workhorse production today is on **4-inch** wafers, not 6-inch — a structural cost handicap unless it migrates.

JX Advanced Metals, the second Japanese substrate house, announced in July 2025 a ¥1.5 billion (~$10.2 million) investment to increase InP substrate production capacity at its Isohara plant by approximately 20%[^13], with the company signalling further cumulative tranches as customer demand from AI optical-comms intensifies. AXT — the only large Western merchant supplier of InP through its Chinese Tongmei subsidiary — saw quarterly InP revenue surge ~250% sequentially to a three-year high of $13.1 million in Q3 2025[^14], then guide a path toward a $35 million quarterly run-rate by end-2026 on roughly $30 million of incremental capex[^15]. Coherent's 6-inch InP capability is shared across Sherman, Texas (backed by a $33 million CHIPS Act preliminary memorandum of terms in December 2024[^16]) and Järfälla, Sweden, with a third 6-inch site in Zürich planned for early 2027 and a guide to "more than double" InP capacity by end of 2026 and double again by end of 2027[^17].

:::timeline
- {date: "2024-03", headline: "Coherent: world-first 6-inch InP scalable fabs", body: "Sherman TX + Järfälla SE; 4x dies/wafer, >60% die-cost reduction vs 3-inch."}
- {date: "2024-12", headline: "Coherent CHIPS Act PMT signed", body: "Up to $33M direct funding for Sherman 150mm InP expansion."}
- {date: "2025-02", headline: "China MOFCOM InP export control effective", body: "HS 2853904051 plus trimethyl-/triethylindium; ~60-business-day permit lead time."}
- {date: "2025-06", headline: "AXT/Tongmei receives first MOFCOM permits", body: "Permit regime confirmed operational for friendly customers; Q3 InP revenue snaps back +250% QoQ."}
- {date: "2025-11", headline: "Sumitomo Electric IR: 12x optical-device capacity by 2026", body: "Concurrent 2.4x InP substrate capacity by 2028; chip-mix pivots EML → CW-LD."}
- {date: "2026-03", headline: "Lumentum closes Greensboro NC 6-inch InP fab", body: "Bought a 240,000 sq ft plant from Qorvo; production targeted mid-2028; >400 jobs."}
- {date: "2026-03", headline: "TNO 6-inch InP industrial pilot line breaks ground in Eindhoven", body: "€153M EU Chips Act-supported; 10,000 wafers/yr; full ops 2028."}
:::

The geopolitics here are sharper than the dollar figures suggest. On February 4, 2025, China's Ministry of Commerce and General Administration of Customs imposed export-license controls on indium phosphide (HS 2853904051), trimethyl-indium and triethyl-indium under the Export Control Law[^18,19]. Every customer order from AXT's Beijing Tongmei subsidiary requires a per-customer MOFCOM permit, which now takes roughly 60 business days to issue. AXT's first permits came on June 11, 2025, four months after the rule took effect[^20]; the resulting backlog drove the Q3 revenue snap-back. {accent}China made its surgically-targeted move at the most upstream layer of the photonics supply chain a full year before the US has done the equivalent on the downstream side{/}. There is, as of mid-2026, no public BIS license requirement specifically singling out 200G-per-lane EMLs or DSPs — the US restrictions on photonics flow through Entity List additions (CIOMP, Shanghai Institute of Optics, Nanjing Simite added January 2025[^21]) and foundry due-diligence guidance, not ECCN-specific photonics controls.

What weakens the InP-chokepoint thesis is the inelasticity cuts both ways. The same wafer-supply tightness that prices in pricing power for substrate vendors also caps how fast downstream lasers can ramp — Sumitomo, AXT, Coherent, and JX are all expanding 40–50%, but more slowly than the equipment-order pace at the chip fabs would suggest the laser side wants. The most likely 2027 bottleneck is not InP demand outrunning supply; it is InP supply ramping faster than competing substrates' yield-and-spec maturity, leaving Sumitomo and AXT structurally over-supplied for one or two quarters if the order book softens. The bear case writes itself: an InP-substrate spot price retracement of 30%+ would mark the cycle.

## 3. The chip chokepoint — EMLs and the five-name oligopoly

If the substrate layer has four producers and >$1 billion combined revenue, the laser-chip layer above it has *five* producers and writes the most concentrated piece of the AI optical bill of materials. The five are Lumentum, Coherent, Mitsubishi Electric, Sumitomo Electric, and Broadcom (captive). Of those five, only Lumentum is shipping the next-generation 200-gigabit-per-lane EML — the laser that turns an 800G transceiver into a 1.6T transceiver — at commercial volume[^7,22].

The previous report in this archive walks Lumentum's $808M Q3 FY26 quarter, the NVIDIA $2 billion preferred placement, the >30% supply-demand gap on 200G EMLs, and the 47.9% non-GAAP gross margin that 200G mix delivers. The same dynamics are now visible — at different speeds — at every other name in the oligopoly.

Coherent shipped Q3 FY26 revenue of ~$1.58–1.81 billion (range across reporting sources) with Data Center & Communications now ~75% of total and growing >40% YoY; non-GAAP gross margin of 39.6% expanded ~57 bps sequentially with the improvement attributed primarily to DC&C[^23]. The company's 6-inch InP move is the structural counter-thesis to Lumentum's lead: Coherent claims 4× dies per wafer and >60% die-cost reduction, and added a 400-gigabit-per-lane differential-EML (D-EML) demonstration at OFC 2025 targeting 3.2T transceivers with general availability of 200G D-EML slated for 2026[^24]. On March 2, 2026, NVIDIA matched its Lumentum check with a parallel **$2 billion equity investment in Coherent** plus a multibillion-dollar purchase commitment[^25,26] — explicit double-sourcing of 200G-class lasers across the only two Western vendors with credible volume pathways.

Mitsubishi Electric's May 2025 semiconductor & device business presentation is the clearest single source on what the third name in the oligopoly is doing. Mitsubishi claims #1 global market share in EMLs for data centers (its own estimate, FY23 actual)[^27]; sizes the ultra-high-speed EML market at $4 billion (2023) → $20 billion (2028); and discloses a strategic capex pivot: *"The budget for investments in the power device business to be partially shifted to the more profitable optical device business."*[^27] Sumitomo Electric (the chip side of the substrate house) lists itself as one of NVIDIA's silicon-photonics ecosystem partners and explicitly addresses 200G/wavelength EML and 350 mW+ CW-LD requirements at 4-inch mass production[^1]. Broadcom, the fifth name, is captive: a Bell Labs-heritage InP fab in Breinigsville, Pennsylvania, with total EML capacity growing from 40M+ units in 2025 to ~50M in 2026, and CW laser capacity climbing from the mid-teens millions to ~30M — supplying Broadcom's own optical modules sold into NVIDIA systems, not merchant[^28].

:::compare
- {role: "LOWEST", name: "Mitsubishi (EML datacenter market, 2023)", value: "$4B"}
- {role: "HIGHEST", name: "Mitsubishi forecast 2028", value: "$20B"}
- {role: "SUBJECT", name: "2025 EML supply vs demand", value: "~20M / ~40M units"}
:::

The dollar arithmetic per laser die is the part most retail coverage misses. A 100G EML chip sells at roughly $10–11 per unit at scale; eight of them populate an 800G EML-based module, giving roughly $80–$100 of EML BOM content per 800G transceiver[^29]. A 200G EML chip — needed in half the count for a 1.6T transceiver — was modeled by Jefferies at ~$14 starting and raised to ~$20 in 2026, with the central asymmetry being *"200G laser pricing nearly 2× 100G at only 15% increase in COGS"*[^2,29]. That is the source of Lumentum's segment-level gross-margin expansion (Jefferies model puts the company's InP segment GM peaking at 54% in 2027[^2]) and of why every supplier in the oligopoly is trying to qualify at 200G — the incremental gross profit dollars on every 200G die shipped land in the 80%-of-incremental-ASP range.

Sumitomo's own forecast contains the most important long-term qualifier. The company's IR mix chart shows EML's share of its own datacenter laser shipments collapsing from 76% in 2024 to 31% in 2028, with CW-LD inversely rising from 24% to 69% as co-packaged optics displace EML-based pluggables[^1]. If Sumitomo is right about its own customers, the *EML oligopoly* is in fact a near-term wedge sitting on top of a structural pivot to CW lasers — and the company that has the deeper CW-LD position (Coherent, with NVIDIA's $2B and a 150mm fab; or Lumentum, with the new Greensboro 6-inch site) wins the 2028+ frame even if the 2026 EML scoreboard says Lumentum. The bear case here is straightforward: a Coherent 200G qualification slip combined with an Innolight or Eoptolink decision to formally dual-source 200G EMLs to a Chinese-domestic supplier (Source Photonics, Zetta Semiconductor, Accelink) compresses Lumentum's 80%+ incremental margin in two quarters. The bull case is that the Chinese 200G EML qualification is still nascent — Photoncap puts Chinese self-sufficiency on ≥25G optical chips below 15%[^11] — and Coherent's 200G D-EML general availability slipped to 2026, leaving Lumentum the only volume option for the immediate ramp.

## 4. The silicon brain — DSPs from Marvell to Credo

If lasers are the chokepoint, DSPs are the brain. A modern 800G or 1.6T pluggable transceiver is, in BOM-decomposition terms, roughly 20–30% DSP, 10–15% EML, 20%+ driver + TIA, and the remainder split across the PIC, optical assembly, connector and casing[^29]. The DSP also accounts for roughly half the module's power budget — 6–8 watts of a typical 14–17 watt 800G transceiver — which is why every CPO architecture so far has tried to push the DSP off the module and onto the host substrate.

The DSP layer is a merchant duopoly with a fast-rising third name. Marvell finished FY2026 with $8.195 billion in revenue (+42% YoY); Q4 FY2026 alone hit $2.219 billion with data center contributing $1.651 billion (74% of total, +21% YoY), at non-GAAP gross margin of 59.0%[^30]. The 200G/lane DSP family is the broadest in the industry: Nova (5nm, 2023, first to market), Ara (3nm, 2024, in mass volume in InnoLight 1.6T modules), and four new 3nm SKUs (Ara X, Ara T, Petra, Aquila M) sampling Q1 2026[^31]. Broadcom's Sian family — Sian2 in general availability for 200G optical + 100G electrical, and Sian3 at 3nm targeting 800G and 1.6T SMF transceivers — is the second leg of the merchant duopoly, with 200G/lane SerDes feeding both Sian and the Tomahawk 5/6 switch silicon as a tightly coupled stack[^32]. The user-facing names are different; the structural posture is identical: TSMC 3nm allocation is the binding constraint.

Credo is the breakout. Q3 FY26 revenue of $407.0 million (+51.9% QoQ, +201.5% YoY) at a non-GAAP gross margin of 68.6% — the highest in the public DSP/connectivity peer set — made it the fastest-growing connectivity name in the AI build[^33]. On April 13, 2026, Credo announced the acquisition of Israeli silicon-photonics PIC vendor DustPhotonics for $750 million in cash plus ~0.92 million shares upfront and up to ~3.21 million contingent shares; combined optical revenue is guided to exceed $500 million in fiscal 2027[^34]. The deal vertically integrates SerDes + DSP + PIC into a single stack — the same direction Marvell took with the December 2025 announcement to acquire Celestial AI for up to $5.5 billion ($3.25B upfront)[^35], and the same direction Acacia/Cisco took with the launch of the 3nm Kibo 1.6T client-optics DSP that ends Acacia's captive-only posture[^36]. {accent}Three of the four merchant DSP houses have either made or announced a vertical-integration acquisition into the PIC layer in the last six months{/} — a clearer signal of where the cost reduction and margin capture are expected to live next than any analyst forecast.

:::timeline
- {date: "2021-04", headline: "Marvell completes $10B Inphi acquisition", body: "Cornerstones Marvell's DSP + electro-optics business; transforms Inphi from coherent into PAM4 leader."}
- {date: "2021-03", headline: "Cisco closes $4.5B Acacia deal", body: "Brings coherent DSP and the future Jannu/Kibo families under Cisco's roof."}
- {date: "2023-08", headline: "Intel–Tower $5.4B deal terminated by China veto", body: "$353M termination fee paid; Intel separately sells pluggable module business to Jabil."}
- {date: "2025-12", headline: "Marvell announces $5.5B Celestial AI acquisition", body: "$3.25B upfront ($1B cash + 27.2M shares @ $2.25B) + up to $2.25B earnout; Q4 FY29 $1B annualized run-rate target."}
- {date: "2026-02", headline: "Marvell closes Celestial AI", body: "Photonic Fabric chiplet brings 16 Tbps single-chiplet optical interconnect into Marvell's stack."}
- {date: "2026-03", headline: "Marvell expands 1.6T DSP family", body: "Ara X, Ara T, Petra, Aquila M sampling Q1 FY27; six DSPs in production or sampling across 5nm and 3nm."}
- {date: "2026-04", headline: "Credo agrees to acquire DustPhotonics for $750M", body: "Vertically integrates SerDes + DSP + PIC; combined optical revenue target >$500M FY27."}
:::

The DSP layer's gross-margin profile is a cleaner read on AI demand-pull than the transceiver assemblers'. Credo at 68.6% is a high-IP DSP/SerDes pure-play whose mix is being lifted by Active Electrical Cables and ZeroFlap optics into hyperscalers. Marvell at 59.0% is blended — custom XPU silicon (lower GM in the 50% range) dilutes the merchant DSP business. Industry consensus is that merchant 1.6T DSPs sell at roughly $150+ per unit (vs ~$80–90 for 800G), supporting the gross-margin gap[^29]. The structural risk for the merchant duopoly is the same as for the lasers: that hyperscalers commission custom XPU silicon (Trainium, TPU, Maia) at increasingly larger volumes, displacing merchant DSP attach. Marvell's custom-XPU business is partly a hedge against exactly this risk, but it also pulls Marvell's blended GM down toward the custom-ASIC mid-50s%. The cleaner long-duration call in the DSP layer is therefore Credo — concentrated in merchant IP, no custom-ASIC drag, now vertically integrated.

## 5. The PIC foundries — TSMC COUPE and a three-leader race

Below the lasers and DSPs sits the photonic integrated circuit (PIC) — the silicon-based waveguide-plus-modulator-plus-photodetector layer that has, over the past five years, gone from research curiosity to the load-bearing piece of every co-packaged optics deployment. The PIC layer is more fragmented than the laser layer above it (more vendors, more processes, no single dominant name) but is consolidating fast onto three foundries.

TSMC's COUPE (Compact Universal Photonic Engine) is the de facto leader. Trade press reporting in April 2026 puts the dedicated COUPE production line at full capacity for 1.6T optical modules supplying NVIDIA Spectrum-X / Quantum-X Photonics switches and Broadcom's Tomahawk 6-Davisson — both shipping or sampling in 2025–2026[^37]. The technology stack pairs an electrical IC with a photonic IC via SoIC-style copper-to-copper hybrid bonding (the same advanced-packaging family that gates HBM and 3D logic in TSMC's leading-edge roadmap), so customers competing for COUPE capacity are competing not just against each other but against TSMC's broader HBM and advanced-packaging customer set.

GlobalFoundries runs the most accessible merchant alternative. The GF Fotonix platform sits on a 45nm SOI process (45SPCLO) with monolithic integration of RF, analog, and silicon-photonic circuits on the same die[^38]. GF describes itself as *"the industry's only high-volume 300mm CMOS manufacturing foundry for silicon photonics"*[^38] and counts Broadcom, Cisco, Marvell, NVIDIA, Ayar Labs, Lightmatter, PsiQuantum, and Ranovus among its silicon-photonics design wins. In 2025 GF acquired Advanced Micro Foundry (AMF) in Singapore — both expanding its silicon-photonics footprint and reportedly planning an upgrade of AMF's 200mm line to 300mm[^39]. LightCounting's November 2025 note ranks GF #1 in silicon-photonics revenue post-AMF[^40].

Tower Semiconductor's PH18 platform (180nm CMOS-compatible) is the third commercial leg. The company plans to double silicon-photonics capacity by end of 2025 and triple it by mid-2026 across 200mm fabs in California, Texas, Israel and a 300mm fab in Japan — backed by $300 million in total investment[^40]. Tower's PH18DA InP-on-silicon platform, developed with OpenLight, received first volume production orders in March 2026[^41]. The fourth-place fab is Intel, whose silicon-photonics history is longest but whose strategic posture is the most damaged after the $5.4 billion Intel–Tower deal was blown up by Chinese regulators in August 2023 (Intel paid a $353 million termination fee[^42]) and the subsequent divestiture of Intel's pluggable-module business to Jabil. Intel's Optical Compute Interconnect (OCI) chiplet — demonstrated at OFC 2024 with 4 Tbps bidirectional bandwidth at 5 pJ/bit — shows that Intel retained the high-end optical-I/O IP, but post-Gelsinger volume commitment remains the largest open question in the PIC layer[^43].

:::stats
- {label: "TSMC COUPE status", value: "Mass prod", note: "2026 Q1; 1.6T line at capacity"}
- {label: "GF Fotonix node", value: "45nm SOI", note: "300mm; monolithic CMOS+SiPh"}
- {label: "Tower PH18 ramp", value: "2x → 3x", note: "EOY 2025 → mid-2026; $300M capex"}
- {label: "Intel OCI demo", value: "4 Tbps", note: "OFC 2024; 5 pJ/bit; prototype only"}
- {label: "Marvell + Celestial deal", value: "$5.5B", note: "Closed Feb 2026"}
- {label: "Credo + DustPhotonics", value: "$750M", note: "Announced Apr 2026"}
:::

The fabless PIC ecosystem — Ayar Labs, Lightmatter, Celestial AI (now Marvell), DustPhotonics (now Credo), Ranovus — adds a fourth dimension. Ayar Labs partnered with Alchip in September 2025 to integrate its TeraPHY optical I/O with TSMC's COUPE advanced packaging; first COUPE-based optical chiplet demonstrated December 2025[^44]. The company has shipped roughly 15,000 TeraPHY devices and raised a $500 million Series E in March 2026 from a syndicate including AMD Ventures, NVIDIA, MediaTek, QIA, and Sequoia[^44]. Lightmatter's Passage M1000 is a >4,000 mm² active photonic interposer built on GlobalFoundries Fotonix and Amkor packaging, delivering 114 Tbps of total optical bandwidth via 256 fibers, with summer 2025 availability[^45]. Below the volume-leader names sits an MPW shuttle ecosystem (AIM Photonics 300mm, IMEC ISiPP50G, IHP BiCMOS+SiPho, SMART Photonics InP) that keeps a long tail of academic and startup designers in production — but is not a volume answer to the COUPE-class deployments NVIDIA and Broadcom are building.

What weakens this section's bull thesis is the same architectural ambiguity that haunts the entire CPO transition. If TSMC's COUPE platform matures to the point that III-V gain dies are heterogeneously bonded directly onto the silicon photonic die — true monolithic InP-on-Si — then the external EML and CW-laser sockets that today's NVIDIA and Broadcom CPO designs preserve disappear, and Lumentum's, Coherent's, Mitsubishi's and Sumitomo's chip-level positions compress toward semi-custom IP licensing rather than merchant chip sales. Both NVIDIA and Broadcom chose *external* laser sourcing for thermal, reliability, and field-serviceability reasons in this generation; neither has committed to that choice for the next one. The PIC foundries are betting that the answer for at least two more generations is still "external laser, hybrid-bonded PIC, advanced-packaged with the switch ASIC." If they're right, COUPE + Fotonix + PH18 split the spoils. If they're wrong, the entire architecture compresses up into TSMC.

## 6. The module assemblers — Innolight's 47% gross margin

For two decades, optical-transceiver assembly was the textbook example of a commodity contract-manufacturing business — low margin, easy entry, easy capacity addition, no pricing power. The 2025–2026 AI build has temporarily inverted that economics. Of the eight transceiver vendors in LightCounting's TOP10 2024 list, the top three are now Chinese and the top three are all reporting **above 30% net margin** — gross margin in the 35–50% range — because the EML shortage upstream lets them price into supply tightness[^11,46].

Innolight Technology (300308.SZ) is the dominant name. Reported revenue grew 114% YoY in 2024 to $3.3 billion+, ranking #1 globally in LightCounting's TOP10 list[^46]. FY2025 operating revenue reached RMB 38.24 billion (~$5.3 billion, +60.25% YoY); Q1 2025 gross margin expanded to 36.70% (+162 bps QoQ) on richer 800G/1.6T mix[^47]. Industry analysis puts Innolight and Eoptolink combined at roughly 60% of NVIDIA's 800G transceiver wallet, with Innolight the larger of the two[^48,11] — a single-country concentration that is the most important reason NVIDIA wrote $4 billion of equity into Lumentum and Coherent in March 2026 to diversify the laser-and-module supply base. Innolight has also reportedly filed confidentially with the Hong Kong Stock Exchange for a secondary listing targeting at least $3 billion in proceeds[^49] — an A+H structure that would diversify the company's funding base outside mainland China and provide a tail hedge against any future US-listed-ADR ban.

Eoptolink (300502.SZ) is the most profitable. The company jumped from #7 in 2023 to #3 in LightCounting's 2024 list on $1.2 billion revenue (+175% YoY); FY2025 revenue hit RMB 24.84 billion (+187%) with gross margin of 47.02% and **net margin of 37.55%** — the highest profitability in the peer group, with 96.16% of revenue overseas[^50]. Accelink (002281.SZ) is the diversified incumbent — LTM revenue ~$1.6 billion, +44% YoY, with broader exposure across telecom + datacom + amplifiers + passive components[^51]. Source Photonics — acquired by Suzhou Dongshan Precision Manufacturing for ~$687 million in mid-2025 — is the Chinese-acquired hybrid that brings its own 200G PAM4 EML capability into the assembly bloc[^52].

The Western alternatives present a starkly different margin and scale picture. Coherent's transceiver business sits inside the company's $1.81 billion Q3 FY26 (+21% YoY) at 39.6% non-GAAP gross margin[^23] — high-quality, but mixed across lasers, materials, networking, and modules. AAOI (Applied Optoelectronics) is the public US-listed pure play: FY2025 revenue $455.7 million, with a first volume 800G order from a major hyperscale customer landing in Q4 2025 and contributing $4–8 million to that quarter[^53]; management subsequently guided FY2026 revenue to >$1 billion — a more than 2× step-up that, if realized, is the cleanest US-listed proxy for the same scarcity wedge that lifted the Chinese assemblers. Fabrinet, the largest dedicated photonics contract manufacturer, posted record Q3 FY26 revenue of $1.214 billion (+39% YoY) at a non-GAAP gross margin of 12.1%[^54] — the structural envelope for optical-assembly CM economics. {accent}Fabrinet's FY25 10-K names just two customers above the 10% threshold: NVIDIA at 27.6% (down from 35.1% in FY24, even as absolute dollars grew) and Cisco at 18.2%{/}[^55] — NVIDIA's customer base at Fabrinet is broadening even as the supply chain consolidates upstream.

:::compare
- {role: "MODULE — CHINA", name: "Eoptolink FY25 net margin", value: "37.5%"}
- {role: "MODULE — WEST", name: "Coherent Q3 FY26 non-GAAP GM", value: "39.6%"}
- {role: "ASSEMBLY CM", name: "Fabrinet Q3 FY26 non-GAAP GM", value: "12.1%"}
:::

The right way to read the table above is not that Chinese assemblers have invented a permanent margin structure. The 33–47% net margins at Eoptolink and Innolight are a function of EML scarcity at Lumentum + Mitsubishi + Broadcom letting module assemblers price into a 30%+ supply gap. When the gap closes — LightCounting's April 2026 forecast says it resolves by end of 2026[^4] — the same margin equation that lifted these names will normalize them downward. The bull case is that the 1.6T transition opens a *second* scarcity window in 2027 (200G EMLs more constrained than 100G EMLs were, with even fewer qualified suppliers), and that Innolight and Eoptolink hold the inventory positions and design wins to capture it. The bear case is that one hyperscaler quietly qualifying a second Western module source — AAOI's $200 million Q4 order is the data point most consistent with this — combined with a 200G EML qualification by Coherent or Mitsubishi, lops 10–15 points off the Chinese assemblers' margin profile inside two quarters.

There is also a genuine geopolitical risk that is not in the consensus math. Today's US export controls target compute (GPUs, advanced ASIC nodes) not optics — there is no public BIS license requirement on shipments of 200G-per-lane EMLs to Chinese assemblers. Any extension of Section 301 / Section 232 tariffs or BIS license requirements to high-end EMLs, DSPs, or PICs would re-route Innolight's >50% NVIDIA wallet share to Coherent + AAOI + Fabrinet inside a quarter. The Dongshan Precision–Source Photonics deal in mid-2025 (a Shenzhen-listed parent absorbing a Taiwan/US-rooted optical-chip business) is exactly the kind of transaction CFIUS-style scrutiny is designed to catch[^52], and the regulatory direction-of-travel is clear even if the calendar isn't.

## 7. The physical layer — fiber, MPO, and Corning's grip

Fiber and connectors are the silent dependency that scales non-linearly with AI compute. Corning's CEO Wendell Weeks put the per-rack delta plainly: NVIDIA's 72-GPU Blackwell-class racks require approximately 16 times more fiber than traditional cloud switch racks, with STL's Rahul Puri pegging the multiple closer to 36× for an AI rack versus a CPU rack — methodology-dependent but order-of-magnitude consistent[^56]. STL projects the US alone needs +213.3 million fiber miles by 2029 (159.6M → 372.9M), with data-center fiber demand growing ~76% YoY in 2025 and projected to reach ~30% of global fiber demand by 2027 versus less than 5% in 2024[^56].

:::stats
- {label: "Corning OC Q1 2026", value: $1.846B, note: +36% YoY}
- {label: "Meta–Corning deal ceiling", value: $6B, note: through 2030}
- {label: "NVIDIA Corning equity", value: $500M + $3.2B, note: warrants}
- {label: "Single-mode fiber spot", value: "+70%", note: vs 2021 trough}
- {label: "Specialty G.657A2", value: "+557%", note: YTD 2026}
- {label: "Corning BABA-compliant lead time", value: "~52 wks", note: vs 8–12 historical}
:::

Corning's exposure runs deeper than its segment reporting reveals. The Optical Communications segment hit Q1 2026 net sales of $1.846 billion (+36% YoY) with segment net income of $387 million (+93% YoY)[^57]; FY2025 segment sales reached ~$6.3 billion (+35% YoY) with Enterprise (intra-DC + hyperscale) growing 61% to ~$3 billion[^58]. The Meta–Corning agreement disclosed January 27, 2026 — up to $6 billion in optical fiber, cable, and connectivity through 2030, anchoring Hickory NC capacity expansion — is part of Meta's $600 billion US infrastructure commitment through 2028[^59]. Two additional hyperscale agreements of "similar size and duration" were announced in Q1 2026 (names not disclosed)[^57]. NVIDIA followed with a long-term partnership to fund three new US fiber plants in NC and TX — claiming a 10× expansion of US optical-connectivity capacity and a 50% increase in US fiber production[^60]; secondary coverage reports the financial structure as ~$500 million upfront plus warrants of up to $3.2 billion[^92].

The connector layer is structurally more concentrated than headline market-share reports suggest. US Conec — the dominant MTP/MPO ferrule vendor with an estimated ~18% of global multi-fiber connector share and ~$113.6 million in FY26 revenue — is jointly owned by Corning, Fujikura, and NTT-AT[^61]. Senko holds another ~15%, with the top-five vendors controlling roughly 50% of global MPO shipments. {accent}When you map Corning's direct fiber exposure plus its one-third stake in the dominant MPO connector vendor, the effective Corning grip on the AI photonics physical layer is materially wider than the Optical Communications segment alone reveals{/}.

Pricing is the cleanest leading indicator. Single-mode fiber spot prices surged ~70% from the 2021 trough of $3.70 per fiber-km to $6.30 by late 2025; specialty G.657A2 fiber spiked 557% YTD to $27–30 per fiber-km; and Corning loose-tube G.652D cable lead times for BABA-compliant orders stretched to ~52 weeks versus 8–12 weeks historically[^46]. Preform-capacity expansion runs on an 18–24 month cycle, so the 2026 supply tightness is structural through at least mid-2027 regardless of demand evolution.

The Japanese duopoly is making the most aggressive physical-layer leap. Furukawa Electric (via Lightera) commenced mass production in March 2026 of a 13,824-fiber rollable-ribbon cable at sub-40mm outer diameter — twice the prior generation's capacity at the same diameter — targeting hyperscale GPU-cluster inter-building links[^62]. Sumitomo Electric, AFL (Fujikura), Corning and TeraHop separately agreed on an SDM4 MCF multi-core fiber MSA in February 2026 for 4-core fiber optimized for O-band intra-campus AI links, with a claimed 2–4× capacity gain per fiber in the same diameter[^63]. Multi-core fiber is pre-commercial — the MSA is at the spec stage — but it is the most credible *physical-layer* roadmap response to the AI demand pull.

What weakens the fiber thesis is the same factor that weakens the InP-substrate thesis: the customer concentration runs both ways. Corning's "up to $6 billion" Meta agreement is a ceiling, not a floor; two additional unnamed hyperscaler deals make the customer concentration tighter, not looser. A single hyperscaler capex pause in 2027 would compress Corning's Enterprise growth rate sharply, and the lead-time visibility that justifies aggressive capex today would compress just as sharply if those orders soften. The fiber/connector duopoly is the most leveraged play on hyperscaler capex *continuing* — and the most vulnerable layer if it stops.

## 8. The switches — CPO and OCS rewrite the network

The most consequential architectural changes in the AI photonics supply chain are happening at the switch layer. Co-packaged optics (CPO) — moving the optical engine off the front-panel pluggable and onto the switch ASIC package — has flipped from "pluggable-killer" thesis to "pluggable-annuity" thesis as both NVIDIA and Broadcom shipped CPO products that preserve an *external* laser-source socket. Optical circuit switches (OCS), the orthogonal technology that replaces electronic packet switching with reconfigurable optical topology, has gone from one-customer Google deployment to a Lumentum + Coherent + HUBER+SUHNER-Polatis competition for a forecast $2.5 billion market by 2029[^64].

NVIDIA's Spectrum-X Photonics (Ethernet) and Quantum-X Photonics (InfiniBand) co-packaged switches were announced at GTC 2025 on March 18, with Quantum-X shipping in 2H 2025 (144 ports × 800 Gb/s = 115.2 Tb/s aggregate) and Spectrum-X following in 2026 at configurations up to 512 × 800G = 400 Tb/s[^65]. NVIDIA's own claims for the architecture: 3.5× power efficiency, 63× signal integrity, 10× network resiliency, 1.3× faster deployment, and 4× fewer lasers — the laser-count reduction is the relevant economic line because *the lasers that remain are higher-power, higher-spec CW sources sold through an ELSFP pluggable rather than embedded in each transceiver*. Broadcom matched the architectural choice in October 2025 with the Tomahawk 6-Davisson — the industry's first 102.4 Tb/s Ethernet CPO switch (64 ports of 1.6 TbE built from 16 × 6.4 Tb/s Davisson optical engines on TSMC COUPE) at 70% lower optical-interconnect power versus pluggables[^66]. Field-replaceable laser modules on the chassis face preserve hot-swap serviceability — the same architectural pattern as NVIDIA's design.

:::compare
- {role: "NVIDIA Quantum-X Photonics", name: "InfiniBand, 144x800G", value: "115.2 Tb/s"}
- {role: "Broadcom Tomahawk 6-Davisson", name: "Ethernet, 64x1.6T", value: "102.4 Tb/s"}
- {role: "NVIDIA Spectrum-X Photonics", name: "Ethernet, 512x800G", value: "400 Tb/s"}
:::

The orthogonal bet is OCS. Google's Apollo deployment — built around an *internally-developed* 3D MEMS 136×136 switch codenamed Palomar (176 mirrors per package, 40 disabled for yield) — was first described at SIGCOMM 2022 and now "forms the basis for the vast majority of our data center networks"[^67,68]. Google's own claims: 30% throughput improvement, 40% less power, 30% less capex, 50× less downtime versus the equivalent electronic-packet alternative; networking is reported to be <5% of TPU pod capex and <3% of power draw[^67]. The Apollo Palomar story is the single best worked example of optical switching's economic payoff at scale, and is the underwriting basis for every non-Google OCS effort that has launched since.

Lumentum's R64 (64×64 MEMS OCS for AI data centers, launched September 2025[^69]) is the leading merchant follow-on, with management on the Q3 FY26 call disclosing ~$400 million of planned H2 FY26 OCS shipments and a target of ~$100 million quarterly exit run-rate by end of CY2026[^70]. Coherent's competing OCS uses *digital liquid crystal* (DLX) — not MEMS — with port counts spanning 64×64 to 512×512[^71]. HUBER+SUHNER now owns the Polatis piezoelectric OCS line (sold by II-VI/Coherent in 2022) and opened a new ~3,000 m² production facility in Pisary, Poland in June 2025 sized to grow OCS output ≥5× over two years[^72] — three distinct OCS architectures (MEMS, DLX, piezoelectric) now competing in the same hyperscaler RFP.

:::timeline
- {date: "2022-08", headline: "Google Apollo Palomar paper at SIGCOMM 2022", body: "Tens of thousands of internal MEMS OCS units already deployed; 30%/40%/30%/50× advantages."}
- {date: "2025-03", headline: "NVIDIA Quantum-X / Spectrum-X Photonics CPO launch at GTC 2025", body: "Quantum-X 2H 2025; Spectrum-X 2026; built on TSMC COUPE + external ELSFP laser."}
- {date: "2025-09", headline: "Lumentum launches R64 64×64 MEMS OCS for AI DCs", body: "2RU; over a trillion mirror operating hours pedigree."}
- {date: "2025-10", headline: "Broadcom Tomahawk 6-Davisson 102.4 Tb/s CPO shipping", body: "16 × 6.4 Tb/s Davisson engines; field-replaceable lasers; 70% optical power reduction."}
- {date: "2026-Q1", headline: "TSMC COUPE silicon-photonics platform at full capacity", body: "Mass production for NVIDIA + Broadcom 1.6T modules."}
- {date: "2026", headline: "Spectrum-X Photonics scheduled ship window", body: "100 Tb/s entry config and 400 Tb/s scale config; ELSFP laser sourcing locked."}
:::

Adoption-curve forecasts disagree by about a factor of two. LightCounting's most aggressive read has CPO ports rising from ~50,000 in 2023 to 4.5 million in 2027, reaching ~30% of total 800G + 1.6T port shipments[^73]. Yole is more conservative, modeling CPO revenue of $38 million (2022) → $2.6 billion (2033) at 46% CAGR with mass production not arriving until 2029. The post-October-2025 reality — Broadcom Davisson shipping in volume — almost certainly accelerates the LightCounting curve faster than the conservative Yole timing. {accent}The most important framing point is that LightCounting models a coexisting $34B pluggable market alongside a ~$9B CPO market by 2030 — meaning CPO is *additive*, not substitutive{/}[^54]. That is the shape of a healthy build cycle, not a substitution one, and it is the single most important reason every transceiver vendor in this report is investing into both pluggables *and* the laser content that CPO requires.

What weakens the CPO thesis is architectural fragility. NVIDIA and Broadcom both chose external laser sourcing for this generation for thermal, reliability, and field-serviceability reasons; neither has committed to the same choice for the next one. If TSMC's COUPE evolves to support heterogeneous integration of InP gain dies directly bonded onto the silicon photonic die, the external ELSFP socket disappears and the Lumentum/Coherent/Mitsubishi laser content compresses dramatically. The OCS thesis has its own fragility — outside Google's deployed base, the production-scale customer set remains thin. Cignal AI flags Meta and Microsoft as "evaluating" OCS but no production deployment has been publicly disclosed at either; the consortium ecosystem (Open Compute Project's OCS subproject) is still pre-procurement.

## 9. The buyers — $660B capex and NVIDIA's $7B vertical integration

Five buyers fund the entire pull. Combined capex from Microsoft, Meta, Alphabet, Amazon, and Oracle stepped from approximately $400 billion in CY2025 to a guided $660–690 billion for CY2026 — a ~65% YoY step-up — with the major guides set in the April–February 2026 earnings cycle[^74]. Microsoft spent $80 billion on AI-enabled datacenters in FY2025 and posted Q1 FY2026 capital investment of $34.9 billion (of which $11.1 billion was datacenter leases alone)[^75,76]. Meta raised 2026 capex guidance to **$125–145 billion** (vs $72.2 billion actual 2025), an ~87% midpoint increase that prompted a 6% stock drop on the print[^77,78]. Alphabet guided 2026 capex to $180–190 billion with CFO commentary that 2027 will "significantly increase"; the call disclosed cloud backlog jumping from $240 billion at Q4 2025 to $460 billion at Q1 2026, with capex mix at roughly 60% servers / 40% datacenter+networking[^79]. Amazon guided 2026 capex to ~$200 billion versus $131 billion actual 2025 — a 53% YoY step — with AWS Q4 growth of +24% YoY and a stated plan to double infrastructure capacity by end-2027[^80].

:::slope(left-label="2025 capex", right-label="2026 guide", unit=$B)
| Hyperscaler | 2025 | 2026 |
|---|---|---|
| Amazon | 131 | 200 |
| Alphabet | 93 | 185 |
| Meta | 72 | 135 |
| Microsoft | 110 | 135 |
:::

Stargate adds the sixth funded lane outside the Big Four. OpenAI, Oracle, SoftBank, and MGX have firmed roughly 7 GW of planned site capacity and >$400 billion of investment commitments over three years[^81]; the OpenAI–Oracle compute contract alone is structured at $300 billion over 5 years[^82]. NVIDIA itself is the seventh — and the most consequential for the photonics supply chain — because NVIDIA is not just buying capacity, it is buying *supplier equity*. On March 2, 2026, NVIDIA wrote two $2 billion checks on the same day: one to Lumentum (Series A Convertible Preferred at $695.31/share, with a multibillion-dollar purchase commitment and capacity rights[^83]) and one to Coherent (equity plus multiyear supply agreement extending through end of decade[^25,26]). On May 6, 2026, NVIDIA followed with a long-term partnership to fund three new US optical-fiber and connectivity plants in NC and TX[^60], with secondary coverage placing the financial structure at ~$500 million upfront plus warrants up to $3.2 billion[^92].

{accent}Totalled, NVIDIA's vertical-integration cheque into the optical supply chain runs to ~$7 billion of equity plus multibillion-dollar purchase commitments at each name{/} — an unprecedented posture for a buyer that historically procured optical components through standard sourcing channels. It is also asymmetric reading: the $7 billion is the single clearest signal that NVIDIA sees optics as the next-binding constraint on its hyperscaler-facing rack volumes after HBM, and that it does not trust the merchant market to clear the demand on its own.

:::stats
- {label: "NVIDIA → Lumentum", value: $2B, note: "Series A pref @ $695.31"}
- {label: "NVIDIA → Coherent", value: $2B, note: "equity + multiyear supply"}
- {label: "NVIDIA → Corning", value: "~$0.5B + $3.2B", note: "warrants reported; 3 US plants"}
- {label: "Combined NVDA optics equity", value: $7B+, note: "Mar–May 2026"}
- {label: "Supply gap 2026", value: ~30%, note: "LightCounting; resolves end-2026"}
- {label: "Optics share of TOP-5 capex 2026", value: "3.1%", note: "→ 4.1% by 2031"}
:::

The per-rack optics math is where most retail coverage gets the framing wrong. The widely-cited "$1 million+ in optics per GB200 NVL72 rack" figure comes from a SemiAnalysis counterfactual: had NVIDIA used optical NVLink for *scale-up* inside the rack, 648 twin-port 1.6T transceivers at ~$850 cost each would have totaled $550,800 per rack at COGS, marked up to ~$2.2 million at NVIDIA's typical 75% gross margin[^84]. NVIDIA chose copper for scale-up specifically to avoid that $2.2 million cost and 19.4 kW of optics power. The *actual* optical content on a shipping NVL72 rack is the scale-out fabric only — 72 × 800G OSFP ports at $650–$1,200 ASP each, or roughly $50–$100 thousand of module BOM per rack before fiber and connectors. Both numbers — counterfactual and actual — are real and material; they just answer different questions about where the optics dollars live in the rack.

What weakens the buyers' thesis is the most-asked equity-market question: ROI. Meta's $145 billion 2026 capex prompted an immediate stock drop on the print, and Bloomberg's August 2025 reporting on Stargate flagged that funding commitments had not yet materialized at the scale of the announcements. The bull case is that hyperscaler capex is a function of AI-cluster utilization, which is in turn a function of model demand, which has continued to outpace supply at every benchmark through 2026. The bear case is that any single hyperscaler capex pause in 2027 — driven by ROI questions, regulatory friction, or model-quality plateau — would propagate down the supply chain inside one quarter, with the 33–47% Chinese module-assembler margins and the 47.9% Lumentum non-GAAP gross margin both compressing first.

## 10. Picks-and-shovels, geopolitics, and the market re-rating

The closing layer of the photonics supply chain is the equipment that builds it, the regulatory regimes that gate it, and the equity market's response to both. Aixtron and Veeco are the public-market read on MOCVD capacity — the chip-growth tools that convert InP wafers into laser dies. Aixtron's Q1 2026 results print showed optoelectronics driving 70% of quarterly equipment order intake (€118 million of €171.4 million); FY26 revenue guidance was raised to €560 million ±€30 million from €520 million ±€30 million; backlog reached €359.1 million with orders extending beyond 2026[^85]. CEO Felix Grawert framed it as "laser-related demand exceeded our expectations." Veeco announced on May 5, 2026 a $250 million+ order package for Spector IBD, Lumina MOCVD, and WaferEtch tools to manufacture InP lasers for 800G/1.6T transceivers, with deliveries starting 2026 and accelerating sharply into 2027[^86]. Named G10-AsP MOCVD customer wins on the Aixtron side include Nokia (April 2025) and SMART Photonics (May 2025); the larger US customer set (Lumentum, Coherent) is inferred but not confirmed. EV Group and SUSS MicroTec are the hybrid-bonding vendors that gate the III-V-on-Si integration the next-generation PIC architectures will require[^87,88].

Geographic concentration runs through every layer. InP substrates are Japan-dominated. EML chips are US-and-Japan dominated. DSPs are US-designed, TSMC-Taiwan-fabbed. PICs are Taiwan / US / Singapore. Module assembly is China-and-Thailand. Switches and the optical-engine architectures are US-designed.

:::stack-rows
categories: [Japan, US, China, Thailand, EU]
rows:
  - {label: "InP substrate", values: [60, 35, 0, 0, 5]}
  - {label: "EML / CW laser chips", values: [25, 70, 0, 0, 5]}
  - {label: "Merchant DSPs", values: [0, 95, 0, 0, 5]}
  - {label: "Silicon photonic ICs", values: [0, 60, 5, 0, 5]}
  - {label: "Transceiver module assembly", values: [0, 15, 60, 25, 0]}
  - {label: "Fiber + MPO", values: [25, 55, 10, 0, 10]}
  - {label: "CPO switch silicon", values: [0, 100, 0, 0, 0]}
:::

The regulatory direction-of-travel is asymmetric. China made the more surgical photonics-specific move first: the February 4, 2025 MOFCOM/GAC export-control regime on indium phosphide (HS 2853904051) plus trimethyl-/triethyl-indium imposes per-customer licensing on the most upstream layer of the supply chain[^18]. The US response has been broader but less targeted: BIS added the Chinese Academy of Sciences' Changchun Institute of Optics, Shanghai Institute of Optics and Fine Mechanics, and other state research arms to the Entity List on January 6, 2025[^21]; commerce strengthened foundry due-diligence guidance in December 2024 covering GlobalFoundries and Tower silicon-photonics PICs[^89]; USTR finalized Section 301 action on December 29, 2025 imposing an additional tariff layer (initially 0%, escalating to a TBD rate before June 23, 2027) on top of the existing 50% Section 301 tariff stack on Chinese semiconductors[^90]. On the supply side, Commerce signed a $33 million CHIPS Act Preliminary Memorandum of Terms with Coherent in December 2024 for its Sherman 150mm InP line[^16], and the EU Chips Act backed the TNO 6-inch InP industrial pilot line in Eindhoven at €153 million with construction beginning March 2026[^91]. *The US restrictions on photonics flow through Entity List and tariff layers, not photonics-specific ECCNs* — meaning Lumentum's 200G EML and Marvell's 1.6T Ara DSP ship freely under general EAR clearance as of mid-2026.

The market re-rating has priced all of this in, layer by layer. Over the 12 months from June 2025 to May 2026, the substrate, chip, and module layers re-rated hardest; the broad-portfolio chip names and the contract manufacturer least.

:::line-chart(title="AI photonics pure-plays — 12-month close ($)", subtitle="Jun-2025 → May-2026, monthly", y-unit=$)
x: 2025-06,2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05
LITE: 95.06,110.08,132.81,162.71,201.56,325.16,368.59,391.84,700.91,702.76,902.32,970.7
COHR: 89.21,107.6,90.47,107.72,131.96,164.26,184.57,212.18,258.93,238.21,319.71,382.45
FN: 294.68,323.73,331.29,364.62,440.57,459.41,455.28,489.44,545.63,521.52,683.47,722.04
CRDO: 92.59,111.55,123.06,145.61,187.62,177.6,143.89,125.28,112.27,93.87,174.01,172.17
:::

:::line-chart(title="Substrate, fiber, equipment — 12-month close ($)", subtitle="Jun-2025 → May-2026, monthly", y-unit=$)
x: 2025-06,2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05
GLW: 52.59,63.24,67.03,82.03,89.08,84.2,87.56,103.25,150.38,135.97,164.24,191.81
VECO: 20.32,20.78,24.52,30.43,28.75,29.23,28.58,31.23,30.56,33.86,49.85,58.64
AXTI: 2.09,2.08,2.9,4.49,7.95,10.7,16.35,18.54,37.9,56.98,79.22,123.78
:::

:::rank-list
- {label: "AXTI (InP substrate, US)", value: "+5,823%", pct: 100, highlight: true}
- {label: "LITE (Lumentum — EML, OCS, CPO laser)", value: "+921%", pct: 32}
- {label: "AAOI (US module pure-play)", value: "+641%", pct: 23}
- {label: "COHR (Coherent — EML, OCS, NVIDIA $2B)", value: "+329%", pct: 14}
- {label: "GLW (Corning — fiber + MPO)", value: "+265%", pct: 11}
- {label: "VECO (MOCVD, IBD, wet processing)", value: "+189%", pct: 9}
- {label: "MTSI (MACOM — drivers, CW lasers)", value: "+162%", pct: 8}
- {label: "FN (Fabrinet — optical CM)", value: "+145%", pct: 7}
- {label: "MRVL (Marvell — merchant DSP + custom XPU)", value: "+129%", pct: 6}
- {label: "CRDO (Credo — DSP + AECs + ZeroFlap optics)", value: "+86%", pct: 5}
- {label: "AVGO (Broadcom — captive EML + DSP + switch)", value: "+54%", pct: 4}
:::

The stack-rank above is itself the answer to the question "where did the market price the chokepoint?" AXT is a single-product pure-play on a previously thin substrate ramp (now thawed by MOFCOM permits and the AI demand pull). Lumentum is the only volume 200G EML shipper. AAOI is the US-listed module call option. Coherent is the second-source NVIDIA paid $2 billion to nurture. Corning is the silent fiber-and-connector grip. At the bottom, Broadcom is up "only" 54% because optics is a small slice of a $100B+ multi-segment business; Credo is up "only" 86% because the market hesitated on whether DustPhotonics's vertical-integration thesis would close before Marvell's Celestial deal pre-empted it. The shape of the curve is consistent with a market that has correctly identified concentration as the value driver — and is now bidding on every name with a quasi-monopolistic position in *its* layer.

## What could break the thesis

The bull case across this entire supply chain rests on three load-bearing premises: hyperscaler capex continues to step up through 2027; co-packaged optics is additive (not substitutive) to pluggables; and the InP wafer / EML chip layer remains supply-constrained. Each premise has at least one credible falsifier.

**Falsifier #1 — Monolithic InP-on-Si bonded inside the PIC.** If TSMC's COUPE, Marvell's 3D SiPho Engine, or a Celestial-AI heterogeneous integration matures to the point that III-V gain dies are bonded directly onto the silicon photonic die — true on-package laser integration — the external ELSFP socket NVIDIA and Broadcom designed disappears at the next architectural revision. The merchant EML laser content collapses by 50%+ over two generations. Both NVIDIA and Broadcom chose external sourcing for thermal, reliability, and field-serviceability reasons in this generation; neither has committed to that choice for the next.

**Falsifier #2 — Chinese 6-inch InP qualification accelerates.** Photoncap puts Chinese self-sufficiency on ≥25G optical chips below 15% today, and Accelink is the only Chinese-domestic 25G EML producer at scale. But Zetta Semiconductor demonstrated 200G PAM4 EMLs at ACP November 2025, Source Photonics is shipping single-lambda 200G PAM4 EML chips, and the Dongshan Precision–Source Photonics deal closed June 2025. A Chinese 200G EML qualification by Innolight or Eoptolink — even at 30% mix — re-routes the EML margin pool away from Lumentum/Coherent/Mitsubishi inside a quarter.

**Falsifier #3 — Hyperscaler insourcing.** Broadcom already runs a captive EML fab in Breinigsville, supplying its own optical modules sold into NVIDIA systems. The next logical step — Microsoft, Meta, or Google acquiring a small InP or PIC vendor and bringing optical-component design in-house — would compress merchant TAM by the share of hyperscaler-direct procurement that bypasses Innolight / Eoptolink / Coherent / Lumentum. Sumitomo's IR explicitly lists itself as one of NVIDIA's silicon-photonics ecosystem partners; nothing structurally prevents the same arrangement at Google or Meta.

**Falsifier #4 — Demand cycle turns.** ==The single most important data point in this report is that LightCounting's April 2026 forecast says the 30% supply gap "resolves by year-end 2026."==[^4] Once supply meets demand, the 33–47% Chinese module-assembler margins and the 47.9% Lumentum non-GAAP gross margin both normalize downward by an amount that retail multiple-expansion math is not pricing in. A Meta or Amazon capex pause in 2027 — driven by ROI questions, regulatory friction, or model-quality plateau — would propagate through all eleven names in the closing rank-list inside one quarter.

**Falsifier #5 — Export controls re-route the supply chain.** Today's US restrictions target compute, not optics. Any extension of Section 301, Section 232, or BIS license requirements to advanced EMLs or DSPs flowing to Chinese assemblers — combined with continued enforcement of China's February 2025 MOFCOM InP regime — would force NVIDIA to qualify Western and Thailand-based assembly (Coherent, AAOI, Fabrinet) at higher cost. The Dongshan Precision–Source Photonics deal is the kind of transaction that triggers the next regulatory turn; the Federal Register filings of 2026 will determine whether the regulatory direction-of-travel remains broad (Entity List + tariffs) or narrows to the photonics-specific BIS license layer that does not yet exist.

The honest read on the photonics supply chain in mid-2026 is that it has been correctly identified by the equity market as the most concentrated layer of the AI infrastructure stack and bid accordingly — and that the bear case for every name in the rank-list above lives in the same supply tightness that the bull case rides. ==The supply chain is currently being priced as if the 2026 30% supply gap is permanent.==[^4] The data in this report says it is most likely not.

:::references
- {id: 1, title: "Growth strategy for data center-related business", url: "https://sumitomoelectric.com/sites/default/files/2025-11/download_documents/Growth%20strategy%20for%20data%20center-related%20business_2025.pdf", source: "Sumitomo Electric IR", date: "2025-11-13"}
- {id: 2, title: "The Great Photonic Divergence — Jefferies 200G EML pricing model relayed", url: "https://benpouladian.com/the-great-photonic-divergence-why/", source: "Independent analyst (Pouladian)", date: "2025"}
- {id: 3, title: "Optical transceiver sales reached $23.8B in 2025 — March 2026 quarterly market update", url: "https://www.lightcounting.com/newsletter/en/march-2026-quarterly-market-update-380", source: "LightCounting", date: "2026-03"}
- {id: 4, title: "April 2026 market forecast — AI cluster optics $26B, supply gap 30%", url: "https://www.lightcounting.com/newsletter/en/april-2026-market-forecast-379", source: "LightCounting", date: "2026-04"}
- {id: 5, title: "2026 Predictions: Optical Transport Market — ~100M cumulative 800G+1.6T ports through 2028", url: "https://www.delloro.com/2026-predictions-optical-transport-market/", source: "Dell'Oro Group", date: "2026"}
- {id: 6, title: "InP wafer market structure — Sumitomo ~60%, AXT ~35%, JX + II-VI fill the rest", url: "https://eu.36kr.com/en/p/3651344579993989", source: "36Kr industry analysis", date: "2025-10-20"}
- {id: 7, title: "Lumentum and the Laser Bottleneck — sole 200G/lane volume supplier", url: "https://www.chipstrat.com/p/lumentum-and-the-laser-bottleneck", source: "Chipstrat (analyst aggregation)", date: "2025"}
- {id: 8, title: "Marvell 1.6T optical DSP family announcement", url: "https://www.marvell.com/company/newsroom/marvell-1-6t-optical-dsp-ai-data-center-connectivity.html", source: "Marvell IR", date: "2026-03-12"}
- {id: 9, title: "Broadcom Extends 200G/Lane DSP PHY Leadership for AI", url: "https://investors.broadcom.com/news-releases/news-release-details/broadcom-extends-200glane-dsp-phy-leadership-next-generation-ai", source: "Broadcom IR", date: "2025-03-25"}
- {id: 10, title: "Acacia / Cisco Kibo 1.6T client-optics DSP", url: "https://acacia-inc.com/blog/acacia-expands-client-optics-component-business/", source: "Acacia / Cisco", date: "2025-03"}
- {id: 11, title: "Chinese optical modules own 7 of TOP 10 — self-sufficiency <15% on ≥25G chips", url: "https://photoncap.net/p/chinese-optical-modules-own-7-of", source: "Photoncap analyst aggregation", date: "2025"}
- {id: 12, title: "World's first 6-inch InP scalable wafer fabs — 4x dies, >60% die-cost reduction", url: "https://www.coherent.com/news/press-releases/worlds-first-6-inch-inp-scalable-wafer-fabs-paving-the-way-for-the-next-generation-of-lasers-for-ai-transceivers-and-6g-wireless-networks", source: "Coherent press release", date: "2024-03-25"}
- {id: 13, title: "JX Advanced Metals investing ¥1.5bn to lift InP substrate output at Isohara plant", url: "https://www.semiconductor-today.com/news_items/2025/jul/jx-240725.shtml", source: "Semiconductor Today", date: "2025-07-24"}
- {id: 14, title: "AXT Q3 2025 — InP revenue +250% QoQ to $13.1M, three-year high", url: "https://www.semiconductor-today.com/news_items/2025/nov/axt-101125.shtml", source: "Semiconductor Today", date: "2025-11-10"}
- {id: 15, title: "AXT Q4 2025 — plans to double InP capacity by end-2026 with ~$30M capex", url: "https://www.semiconductor-today.com/news_items/2026/mar/axt-090326.shtml", source: "Semiconductor Today", date: "2026-03-09"}
- {id: 16, title: "Commerce Preliminary Memorandum of Terms with Coherent for 150mm InP expansion", url: "https://www.commerce.gov/news/press-releases/2024/12/biden-harris-administration-announce-preliminary-terms-coherent", source: "US Department of Commerce", date: "2024-12-09"}
- {id: 17, title: "Coherent Q3 FY2026 earnings call transcript — 6-inch InP capacity expansion plan", url: "https://www.fool.com/earnings/call-transcripts/2026/05/06/coherent-cohr-q3-2026-earnings-transcript/", source: "Motley Fool transcript", date: "2026-05-06"}
- {id: 18, title: "China MOFCOM/GAC export controls — indium phosphide HS 2853904051 effective 2025-02-04", url: "https://www.iea.org/policies/26795-decision-to-implement-export-controls-on-tungsten-tellurium-bismuth-molybdenum-and-indium-related-items", source: "IEA / MOFCOM notice republication", date: "2025-02-04"}
- {id: 19, title: "Global Times: MOFCOM/GAC dual-use export control on indium phosphide", url: "https://www.globaltimes.cn/page/202502/1327805.shtml", source: "Global Times", date: "2025-02-04"}
- {id: 20, title: "AXT 8-K — Tongmei InP export permits received", url: "https://www.sec.gov/Archives/edgar/data/1051627/000143774925020087/axti20250611_8k.htm", source: "SEC EDGAR", date: "2025-06-11"}
- {id: 21, title: "Federal Register: Revisions to the Entity List, January 6 2025 — CIOMP, SIOM and others added", url: "https://www.federalregister.gov/documents/2025/01/06/2024-31468/revisions-to-the-entity-list", source: "Federal Register", date: "2025-01-06"}
- {id: 22, title: "TrendForce: NVIDIA EML strategic lock-in — 200G supply tight through 2027", url: "https://www.trendforce.com/presscenter/news/20251208-12823.html", source: "TrendForce", date: "2025-12-08"}
- {id: 23, title: "Assessing Coherent's valuation at record AI demand — Q3 FY26 financials", url: "https://finance.yahoo.com/markets/stocks/articles/assessing-coherent-cohr-valuation-record-120653286.html", source: "Yahoo Finance / S&P Global", date: "2026-05"}
- {id: 24, title: "Coherent: industry's first 400G differential EML — 200G D-EML general availability 2026", url: "https://www.coherent.com/news/press-releases/400g-differential-eml", source: "Coherent press release", date: "2025-03-27"}
- {id: 25, title: "NVIDIA and Coherent announce strategic partnership — $2B investment + multibillion purchase commitment", url: "https://nvidianews.nvidia.com/news/nvidia-and-coherent-announce-strategic-partnership-to-develop-optics-technology-to-scale-next-generation-data-center-architecture", source: "NVIDIA Newsroom", date: "2026-03-02"}
- {id: 26, title: "NVIDIA invests in Coherent and Lumentum for AI optics", url: "https://www.cnbc.com/2026/03/02/nvidia-investment-coherent-lumentum.html", source: "CNBC", date: "2026-03-02"}
- {id: 27, title: "Mitsubishi Electric Semiconductor & Device Business presentation — #1 EML for datacenter, $4B → $20B 2023-2028", url: "https://www.mitsubishielectric.com/en/pr/2025/pdf/0528-5.pdf", source: "Mitsubishi Electric IR", date: "2025-05-28"}
- {id: 28, title: "Broadcom Makes Lasers — Breinigsville PA fab, 40M → 50M EML units 2025-2026", url: "https://www.chipstrat.com/p/broadcom-makes-lasers", source: "Chipstrat analyst aggregation", date: "2025"}
- {id: 29, title: "Deep Dive: Optical Module Market — BOM percentages, ASP trajectory, DSP $80-150+", url: "https://deepfundamental.substack.com/p/deep-dive-optical-module-market", source: "Deep Fundamental analyst", date: "2025-2026"}
- {id: 30, title: "Marvell Technology Q4 FY2026 financial results — $8.195B FY26, $1.651B Q4 data center", url: "https://investor.marvell.com/news-events/press-releases/detail/1011/marvell-technology-inc-reports-fourth-quarter-and-fiscal-year-2026-financial-results", source: "Marvell IR", date: "2026"}
- {id: 31, title: "Marvell 1.6T optical DSP roadmap — Nova / Ara / Ara X / Petra / Aquila M", url: "https://www.marvell.com/company/newsroom/marvell-1-6t-optical-dsp-ai-data-center-connectivity.html", source: "Marvell IR", date: "2026-03-12"}
- {id: 32, title: "Broadcom Sian2 / Sian2M / Sian3 200G/lane DSP family", url: "https://investors.broadcom.com/news-releases/news-release-details/broadcom-extends-200glane-dsp-phy-leadership-next-generation-ai", source: "Broadcom IR", date: "2025-03-25"}
- {id: 33, title: "Credo Technology Q3 FY2026 8-K — $407M revenue +201% YoY, 68.6% non-GAAP GM", url: "https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm", source: "SEC EDGAR", date: "2026-03-02"}
- {id: 34, title: "Credo to acquire DustPhotonics for $750M cash + shares; $500M+ optical revenue target FY27", url: "https://www.sec.gov/Archives/edgar/data/1807794/000162828026024892/april20268-kex991.htm", source: "SEC EDGAR", date: "2026-04-13"}
- {id: 35, title: "Marvell to acquire Celestial AI — up to $5.5B; $1B run-rate target Q4 FY29", url: "https://investor.marvell.com/news-events/press-releases/detail/1000/marvell-to-acquire-celestial-ai-accelerating-scale-up-connectivity-for-next-generation-data-centers", source: "Marvell IR", date: "2025-12-02"}
- {id: 36, title: "Acacia/Cisco Kibo 1.6T DSP — 3nm sample later 2025; >20% lower power", url: "https://acacia-inc.com/blog/acacia-expands-client-optics-component-business/", source: "Acacia / Cisco", date: "2025-03"}
- {id: 37, title: "TSMC begins mass production of COUPE silicon-photonics platform — 1.6T line at capacity", url: "https://machineherald.io/article/2026-04/07-tsmc-begins-mass-production-of-coupe-silicon-photonics-platform-as-ai-data-centers-shift-from-copper-to-light/", source: "Machine Herald trade press", date: "2026-04-07"}
- {id: 38, title: "GlobalFoundries Silicon Photonics — Fotonix 45nm SOI, monolithic CMOS+photonics", url: "https://gf.com/technologies/silicon-photonics/", source: "GlobalFoundries", date: "2026"}
- {id: 39, title: "GlobalFoundries buys Advanced Micro Foundry — silicon-photonics scale-up", url: "https://www.tomshardware.com/tech-industry/globalfoundries-buys-silicon-photonics-firm-advanced-micro-foundry-for-undisclosed-amount-move-makes-chipmaker-one-of-the-largest-silicon-photonics-manufacturers", source: "Tom's Hardware", date: "2025"}
- {id: 40, title: "LightCounting research note: November 2025 — The Year of Silicon Photonics 2026; Tower 2x → 3x ramp", url: "https://www.lightcounting.com/research-note/november-2025-the-year-of-silicon-photonics-2026-436", source: "LightCounting", date: "2025-11"}
- {id: 41, title: "OpenLight receives first volume production orders on Tower PH18DA InP-on-silicon", url: "https://www.semiconductor-today.com/news_items/2026/mar/openlight-tower-200326.shtml", source: "Semiconductor Today", date: "2026-03-20"}
- {id: 42, title: "Intel terminates $5.4B Tower Semiconductor acquisition after China veto", url: "https://techcrunch.com/2023/08/16/intel-tower-semiconductor-acquisition-china/", source: "TechCrunch", date: "2023-08-16"}
- {id: 43, title: "Intel unveils first fully-integrated optical I/O chiplet — OFC 2024, 4 Tbps bidirectional", url: "https://newsroom.intel.com/artificial-intelligence/intel-unveils-first-integrated-optical-io-chiplet", source: "Intel Newsroom", date: "2024-06"}
- {id: 44, title: "Alchip and Ayar Labs unveil co-packaged optics for AI datacenter scale-up", url: "https://ayarlabs.com/news/alchip-and-ayar-labs-unveil-co-packaged-optics-for-ai-datacenter-scale-up/", source: "Ayar Labs", date: "2025-09"}
- {id: 45, title: "Lightmatter Passage M1000 — GlobalFoundries Fotonix + Amkor; 114 Tbps", url: "https://lightmatter.co/press-release/lightmatter-unveils-passage-m1000-photonic-superchip-worlds-fastest-ai-interconnect/", source: "Lightmatter", date: "2025-03-31"}
- {id: 46, title: "AI data centers consuming fiber optic cable faster than suppliers can make it", url: "https://www.tomshardware.com/tech-industry/ai-data-centers-are-consuming-fiber-optic-cable-faster-than-suppliers-can-make-it", source: "Tom's Hardware", date: "2026"}
- {id: 47, title: "Innolight Q1 2025 — gross margin 36.7%; 60% revenue growth", url: "https://www.ainvest.com/news/zhongji-innolight-soars-57-profit-surge-riding-high-speed-data-wave-2504/", source: "AInvest summary", date: "2025"}
- {id: 48, title: "LightCounting May 2025 — Optical Vendor Landscape, Innolight #1 globally 2024", url: "https://www.lightcounting.com/newsletter/en/may-2025-optical-vendor-landscape-333", source: "LightCounting", date: "2025-05"}
- {id: 49, title: "Innolight files confidentially with HKEX targeting $3B secondary listing", url: "https://news.futunn.com/en/post/71020122/", source: "Futubull / Futu News", date: "2025"}
- {id: 50, title: "Eoptolink FY2025 — RMB 24.84B revenue, 47.02% GM, 37.55% NM", url: "https://news.futunn.com/en/post/64225452/", source: "Futubull / Futu News", date: "2025-Q3"}
- {id: 51, title: "Accelink Technologies FY2025 revenue trend — datacom-led growth", url: "https://www.alphaspread.com/security/szse/002281/financials/income-statement/revenue", source: "AlphaSpread aggregator (Shenzhen filings)", date: "2025-2026"}
- {id: 52, title: "Dongshan Precision acquires Source Photonics for ~$687M — Chinese consolidation into optical-chip supply", url: "https://www.yicaiglobal.com/news/chinas-dongshan-precision-soars-after-unveiling-plan-to-buy-optical-parts-maker-source-photonics", source: "Yicai Global", date: "2025"}
- {id: 53, title: "AOI Receives First Volume Order of 800G Data Center Transceivers from Major Hyperscale Customer", url: "https://www.globenewswire.com/news-release/2025/12/10/3203517/9986/en/AOI-Receives-First-Volume-Order-of-800G-Data-Center-Transceivers-from-Major-Hyperscale-Customer.html", source: "GlobeNewswire / Applied Optoelectronics", date: "2025-12-10"}
- {id: 54, title: "Fabrinet Q3 FY2026 earnings transcript — record $1.214B, 12.1% non-GAAP GM", url: "https://www.fool.com/earnings/call-transcripts/2026/05/04/fabrinet-fn-q3-2026-earnings-transcript/", source: "Motley Fool transcript", date: "2026-05-04"}
- {id: 55, title: "Fabrinet Form 10-K FY2025 — NVIDIA 27.6% / Cisco 18.2% revenue concentration", url: "https://investor.fabrinet.com/static-files/9a916b94-df74-471d-971e-a5ac4b02107c", source: "Fabrinet IR / SEC 10-K", date: "2025-08-19"}
- {id: 56, title: "AI rack fiber intensity 16x–36x vs CPU rack; STL US +213M fiber miles by 2029", url: "https://techblog.comsoc.org/2025/12/23/how-will-fiber-and-equipment-vendors-meet-the-increased-demand-for-fiber-in-2026-due-to-ai-data-center-buildouts/", source: "IEEE ComSoc Technology Blog citing Corning, STL", date: "2025-12-23"}
- {id: 57, title: "Corning Q1 2026 results — Optical Communications $1.846B +36% YoY", url: "https://investor.corning.com/news-and-events/news/news-details/2026/Corning-Announces-Strong-First-Quarter-2026-Financial-Results-1/default.aspx", source: "Corning IR", date: "2026-04-28"}
- {id: 58, title: "Corning 2025 full-year results — Optical Communications ~$6.3B (+35%); Enterprise +61%", url: "https://investor.corning.com/news-and-events/news/news-details/2026/Corning-Announces-Outstanding-2025-Financial-Results-1--Upgrades-Springboard-Plan-for-Faster-Sales-Growth-on-Significantly-Enhanced-Financial-Profile/default.aspx", source: "Corning IR", date: "2026-01-28"}
- {id: 59, title: "Corning and Meta announce multiyear up to $6B agreement to accelerate US data center buildout", url: "https://investor.corning.com/news-and-events/news/news-details/2026/Corning-and-Meta-Announce-Multiyear-up-to-6-Billion-Agreement-to-Accelerate-US-Data-Center-Buildout/default.aspx", source: "Corning IR", date: "2026-01-27"}
- {id: 60, title: "NVIDIA and Corning announce long-term partnership for US optical manufacturing", url: "https://nvidianews.nvidia.com/news/nvidia-and-corning-announce-long-term-partnership-to-strengthen-us-manufacturing-for-ai-infrastructure", source: "NVIDIA Newsroom", date: "2026-05-06"}
- {id: 61, title: "US Conec company overview — Corning / Fujikura / NTT-AT joint ownership", url: "https://www.usconec.com/about-us/company-overview", source: "US Conec", date: "2026"}
- {id: 62, title: "Furukawa Electric / Lightera 13,824-fiber rollable ribbon cable mass production", url: "https://www.furukawaelectric.com/en/release/2026/comm_20260312.html", source: "Furukawa Electric press release", date: "2026-03-12"}
- {id: 63, title: "Sumitomo Electric SDM4 MCF multi-core fiber MSA with AFL, Corning, TeraHop", url: "https://sumitomoelectric.com/press/2026/02/prs011", source: "Sumitomo Electric press release", date: "2026-02"}
- {id: 64, title: "Cignal AI: Optical Circuit Switching market to exceed $2.5B in 2029", url: "https://cignal.ai/2025/12/optical-circuit-switching-market-to-exceed-2-5b-in-2029/", source: "Cignal AI", date: "2025-12"}
- {id: 65, title: "NVIDIA Spectrum-X / Quantum-X Photonics CPO networking switches — GTC 2025", url: "https://nvidianews.nvidia.com/news/nvidia-spectrum-x-co-packaged-optics-networking-switches-ai-factories", source: "NVIDIA Newsroom", date: "2025-03-18"}
- {id: 66, title: "Broadcom announces Tomahawk 6-Davisson — industry first 102.4 Tb/s CPO Ethernet switch", url: "https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-tomahawkr-6-davisson-industrys-first-1024", source: "Broadcom IR", date: "2025-10-08"}
- {id: 67, title: "Mission Apollo — Google datacenter OCS deployment (SIGCOMM 2022 paper)", url: "https://arxiv.org/abs/2208.10041", source: "arXiv / SIGCOMM 2022 (Urata et al.)", date: "2022-08-22"}
- {id: 68, title: "Evolution of Google's Jupiter data center network — OCS forms basis of vast majority of network", url: "https://cloud.google.com/blog/topics/systems/the-evolution-of-googles-jupiter-data-center-network", source: "Google Cloud blog", date: "2023"}
- {id: 69, title: "Lumentum announces R64 64x64 MEMS optical circuit switch for AI data centers", url: "https://www.businesswire.com/news/home/20250924536510/en/Lumentum-Announces-R64-Optical-Circuit-Switch-for-AI-Data-Centers", source: "BusinessWire / Lumentum", date: "2025-09-24"}
- {id: 70, title: "Lumentum Q3 FY2026 earnings transcript — OCS $400M H2 ship plan; $100M/qtr exit run-rate by EOY CY26", url: "https://www.fool.com/earnings/call-transcripts/2026/05/06/lumentum-lite-q3-2026-earnings-transcript/", source: "Motley Fool transcript", date: "2026-05-06"}
- {id: 71, title: "Coherent Optical Circuit Switch product page — digital liquid crystal (DLX) architecture, 64x64 to 512x512", url: "https://www.coherent.com/networking/optical-circuit-switch", source: "Coherent product page", date: "2026"}
- {id: 72, title: "HUBER+SUHNER opens new Optical Circuit Switch production site in Pisary, Poland (Polatis)", url: "https://www.hubersuhner.com/en/newsroom/company-news/news-ad-hoc-news/new-optical-circuit-switch-production-site", source: "HUBER+SUHNER", date: "2025-06-12"}
- {id: 73, title: "Optics for AI clusters: $5B (2024) → >$10B (2026); CPO ramp 2026-2028", url: "https://www.lightcounting.com/newsletter/en/january-2025-optics-for-ai-clusters-319", source: "LightCounting", date: "2025-01"}
- {id: 74, title: "AI Capex 2026 — the $690B infrastructure sprint", url: "https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/", source: "Futurum Group", date: "2026"}
- {id: 75, title: "Microsoft expects to spend $80B on AI data centers in FY2025", url: "https://www.cnbc.com/2025/01/03/microsoft-expects-to-spend-80-billion-on-ai-data-centers-in-fy-2025.html", source: "CNBC", date: "2025-01-03"}
- {id: 76, title: "Microsoft spent $11.1B on data center leases alone in Q1 2026", url: "https://www.datacenterdynamics.com/en/news/microsoft-spent-111bn-on-data-center-leases-alone-in-q1-2026/", source: "DataCenterDynamics", date: "2026"}
- {id: 77, title: "Meta Q1 2026 IR release — capex guide raised to $125-145B", url: "https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/default.aspx", source: "Meta IR", date: "2026-04-29"}
- {id: 78, title: "Fortune: Meta $145B AI spending raises ROI questions", url: "https://fortune.com/2026/04/29/meta-zuckerberg-145-billion-ai-spending-roi/", source: "Fortune", date: "2026-04-29"}
- {id: 79, title: "Alphabet Q1 2026 earnings — $180-190B capex guide; cloud backlog $460B", url: "https://www.cnbc.com/2026/04/29/alphabet-googl-q1-2026-earnings.html", source: "CNBC", date: "2026-04-29"}
- {id: 80, title: "Amazon Q4 2025 earnings — $200B capex guide for 2026, double capacity by end-2027", url: "https://www.cnbc.com/2026/02/05/amazon-amzn-q4-earnings-report-2025.html", source: "CNBC", date: "2026-02-05"}
- {id: 81, title: "OpenAI Stargate — five new sites, 7 GW planned, $400B+ over 3 years", url: "https://openai.com/index/five-new-stargate-sites/", source: "OpenAI", date: "2025-09"}
- {id: 82, title: "Stargate advances with partnership with Oracle — $300B / 5yr compute contract", url: "https://openai.com/index/stargate-advances-with-partnership-with-oracle/", source: "OpenAI", date: "2025"}
- {id: 83, title: "Lumentum announces new US manufacturing facility for advanced lasers for AI data centers (Greensboro)", url: "https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-New-U-S--Manufacturing-Facility-to-Produce-Advanced-Lasers-for-the-Worlds-Largest-AI-Data-Centers/default.aspx", source: "Lumentum IR", date: "2026-03-26"}
- {id: 84, title: "NVIDIA's Optical Boogeyman — counterfactual $2.2M/rack optics NVL72", url: "https://semianalysis.com/2024/03/25/nvidias-optical-boogeyman-nvl72-infiniband/", source: "SemiAnalysis", date: "2024-03-25"}
- {id: 85, title: "Aixtron Q1 2026 results presentation — €560M FY guide, opto 70% of orders", url: "https://www.aixtron.com/investoren/publikationen/ir-praesentationen/2026/AIXA%20Q1-2026%20Results%20Presentation.pdf", source: "Aixtron IR", date: "2026-04-30"}
- {id: 86, title: "Veeco announces $250M+ equipment orders for manufacturing InP lasers", url: "https://www.globenewswire.com/news-release/2026/05/05/3288217/0/en/Veeco-Announces-250-Million-in-Equipment-Orders-for-Manufacturing-Indium-Phosphide-Lasers.html", source: "GlobeNewswire / Veeco", date: "2026-05-05"}
- {id: 87, title: "EV Group die-to-wafer fusion and hybrid bonding for silicon photonics", url: "https://www.evgroup.com/technologies/die-to-wafer-fusion-and-hybrid-bonding", source: "EV Group", date: "2025"}
- {id: 88, title: "SUSS MicroTec May 2026 investor presentation — XBC300 Gen2 hybrid bonder", url: "https://www.suss.com/en/content/download/3341/file/2026_05_SUSS_Investor%20Presentation_May%202026.pdf", source: "SUSS MicroTec IR", date: "2026-05"}
- {id: 89, title: "BIS strengthens restrictions on advanced computing semiconductors — enhanced foundry due diligence", url: "https://www.bis.gov/press-release/commerce-strengthens-restrictions-advanced-computing-semiconductors-enhance-foundry-due-diligence-prevent", source: "US BIS press release", date: "2024-12-02"}
- {id: 90, title: "Federal Register: Section 301 final action on China semiconductor practices", url: "https://www.federalregister.gov/documents/2025/12/29/2025-23912/notice-of-action-chinas-acts-policies-and-practices-related-to-targeting-of-the-semiconductor", source: "Federal Register / USTR", date: "2025-12-29"}
- {id: 91, title: "TNO 6-inch InP industrial pilot line breaks ground in Eindhoven — €153M EU Chips Act-supported", url: "https://www.trendforce.com/news/2026/03/18/news-worlds-first-6-inch-inp-photonic-chip-industrial-wafer-fab-broke-ground/", source: "TrendForce", date: "2026-03-18"}
- {id: 92, title: "NVIDIA-Corning long-term partnership — secondary coverage of ~$500M upfront + up to $3.2B in warrants for three US optical plants", url: "https://www.cnbc.com/2026/05/06/nvidia-corning-optical-factories-nc-texas-ai.html", source: "CNBC", date: "2026-05-06"}
:::
