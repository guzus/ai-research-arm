---
eyebrow: REPORT · MANUFACTURING
title: How HBM is made
deck: A 1024-bit bus, 12 dies thinned to 30 micrometers, 8,000 copper-filled tunnels per layer, and a 70-ton press — the manufacturing recipe behind the chip that gates the entire AI build.
lede: |
  High-Bandwidth Memory is not a memory chip. It is a vertical city of memory chips — twelve identical DRAM dies, each ground to roughly the thickness of a sheet of paper, drilled through with thousands of copper-filled tunnels, and welded into a single cube that sits beside a GPU on a silicon raft larger than a postage stamp. The hardest steps are not on the front-end DRAM line — those are well understood — but at the back end, where the cubes are assembled. That assembly is why SK Hynix earned a 72% operating margin in Q1 2026, why Samsung lost eighteen months at NVIDIA's front door, why TSMC's CoWoS capacity is the binding constraint on the entire AI build, and why a Hefei-funded entrant called CXMT is the geopolitical asterisk on the whole story.
stats:
  - {label: HBM bandwidth/stack, value: "2", unit: TB/s, note: "HBM4, 16× HBM1"}
  - {label: Per-die thickness,   value: "30", unit: μm,   note: "HBM3; drops ~40% at HBM3E 12-Hi"}
  - {label: HBM revenue 2025,    value: "$35", unit: B,   note: ">30% of DRAM"}
  - {label: SK Hynix HBM share,  value: "57", unit: "%",  note: "Q3 2025 bit share, Counterpoint"}
---

## 01. The bandwidth wall — why HBM exists at all

The premise of HBM is that you cannot solve AI's memory problem with faster wires. Conventional DDR/GDDR scaled bandwidth by pushing pin rates higher on a narrow bus — 32 bits for DDR, 384 bits for GDDR — and ran into a power wall around 10 GB/s/W on the GPU side.[^4] AMD's 2015 HBM whitepaper benchmarked the original HBM stack at over 35 GB/s/W, more than three times the per-watt bandwidth of GDDR5 on a Radeon R9 290X.[^4] The recipe was not faster wires but more of them: a 1,024-bit interface running at modest per-pin speeds, organized as eight independent channels of 128 bits each, all running in parallel.[^1]

A decade later that recipe has compounded. JEDEC published the original HBM standard (JESD235) in October 2013 at 128 GB/s per stack.[^1] HBM2 reached 410 GB/s by 2020 (JESD235C, 3.2 Gb/s per pin).[^3] HBM3 doubled the channels from 8 to 16 and the speed to 6.4 Gb/s, yielding 819 GB/s per stack on the same 1,024-bit bus (JESD238, January 2022).[^2] HBM3E pushed past 1.2 TB/s on the SK Hynix 9.6 Gb/s product that NVIDIA's H200 and Blackwell families use.[^5] In April 2025 JEDEC ratified HBM4 (JESD270-4), which doubles the physical interface for the first time since 2013 — from 1,024 to 2,048 bits — and delivers up to 2 TB/s per stack at the 8 Gb/s spec speed; vendors are now sampling above 10 Gb/s.[^6]

:::line-chart(title="HBM per-stack bandwidth, 2013-2026", subtitle="Each step is a roughly 2x widening or doubling, not a faster wire.", y-unit=" GB/s")
x: HBM1 (2013),HBM2 (2016),HBM2E (2020),HBM3 (2022),HBM3E (2024),HBM4 (2026)
Per-stack: 128,256,410,819,1229,2048
:::

:::compare
- {role: GDDR5 R9 290X,  name: AMD baseline,    value: 10.7,  unit: " GB/s/W"}
- {role: HBM1 (2015),    name: AMD Fiji,        value: 35,    unit: " GB/s/W"}
- {role: SUBJECT,        name: HBM3E (2024),    value: 1229,  unit: " GB/s/stack"}
:::

The wide-slow architecture is also a packaging argument. A 1,024-bit bus would be impossible on a printed circuit board — the routing density does not exist in PCB. HBM only works because it sits on a silicon interposer micrometers away from the GPU, with copper traces drawn at lithographic precision rather than mechanical etch.[^7] That tightly couples HBM economics to TSMC's CoWoS supply, which is treated in Section 06. The point of HBM, in one sentence: it traded a manageable manufacturing problem (faster wires) for a hard one (stacking thinned DRAM on silicon over silicon), because the manageable problem had run out of room. {accent}The bandwidth wall is not a memory wall — it is a packaging wall.{/}

What would weaken this thesis: if GDDR7 (36 Gb/s per pin, shipping in 2025) plus inference-optimized accelerators can replace HBM for low-batch inference, the HBM premium compresses. NVIDIA's RTX 50 series demonstrates GDDR7 in volume; whether AMD's MI400 or Intel's Gaudi 4 can dent HBM share on inference-only workloads is the open question.

## 02. The DRAM die — what gets stacked

Before the cube is a stack, it is twelve identical wafers, each holding hundreds of HBM core dies. Each die is itself a frontier-node DRAM device. SK Hynix builds HBM3E on its 1b node (sixth-generation 10nm-class, ~12 nm half-pitch); the same line will feed the first HBM4.[^8] Samsung shipped commercial HBM4 in February 2026 on its 1c DRAM (its EUV-heavy node) paired with a 4 nm logic base die from Samsung Foundry.[^9] Micron uses the same de-risking strategy as Hynix — its HBM3E and early HBM4 ride 1-beta (non-EUV multipatterning), with the EUV-based 1-gamma node moving into the line as 2025 progresses.[^10]

The EUV layer count is the clearest disclosure of how heavily each vendor leans on lithography. SK Hynix went from one EUV layer at 1a, to four at 1b, to "more than five" (reportedly six) at 1c.[^11][^12] Samsung made the opposite bet — five EUV layers at 1a, the same node where Hynix used one — and paid for it in 2024 with HBM3E qualification delays that Korean trade press eventually traced to yield issues on the densely-EUV'd 1a periphery.[^12] {accent}It is not lithography that determines whether you ship HBM; it is whether the die yields enough good rows to be worth stacking.{/}

:::stats
- {label: "SK Hynix 1a EUV layers", value: "1"}
- {label: "SK Hynix 1b EUV layers", value: "4"}
- {label: "SK Hynix 1c EUV layers", value: "5+"}
- {label: "Samsung 1a EUV layers",  value: "5"}
- {label: "Micron HBM3E node",      value: "1-beta", note: "non-EUV multipatterning"}
- {label: "ASML memory bookings 4Q25", value: "56%", note: "first quarter > logic"}
:::

ASML's TWINSCAN NXE:3800E — the third-generation low-NA EUV scanner — lists at least 195 wafers per hour at a 30 mJ/cm² dose, and is explicitly positioned for 2 nm logic plus leading-edge DRAM.[^13] In Q4 2025, memory bookings overtook logic at ASML for the first time in the company's history (56% vs 44%), with HBM and DDR5 cited as the swing factors.[^14] SK Hynix installed the first volume-class High-NA EUV system (the EXE:5200B, 0.55 NA) at its M16 fab in September 2025, ahead of any DRAM competitor, though it is positioned for the HBM5/DDR6 generation rather than HBM4.[^15] Concretely: every HBM cube shipping in 2026 carries between 36 and 96 EUV-printed layers across its twelve dies. The DRAM cell, in other words, has stopped being the cheap part of HBM. But it is still not the hard part.

## 03. Drilling the silicon — through-silicon vias

The hard part begins after the DRAM transistors are done. To stack twelve dies and let signals walk up the cube, each die must be drilled with thousands of vertical copper-filled tunnels — through-silicon vias, or TSVs. Each HBM die carries thousands of TSVs: 1,024 of them are signal I/O at HBM3, with the rest dedicated to power, ground, and redundancy.[^21] HBM4 doubles the signal count to 2,048 bits and pushes the total above 3,000 microbumps per die.[^17]

The industry settled on "via-middle" — TSVs are formed after the front-end transistors are done but before back-end metallization — because it balances density, cost, and thermal stress better than via-first (interposer-style) or via-last (image-sensor style).[^16] Lam Research, which dominates the equipment side, reports HBM TSVs at 2-5 µm in diameter and 30-60 µm deep — roughly the geometry of a human hair pierced through a sheet of paper — at a stable 10:1 aspect ratio.[^18]

:::timeline
- {date: Step 1, headline: "Lithography",       body: "Define the TSV mask on the wafer between FEOL and BEOL."}
- {date: Step 2, headline: "Bosch DRIE etch",    body: "Alternate SF6 etch / C4F8 passivation cycles cut a vertical hole with scalloped sidewalls."}
- {date: Step 3, headline: "PECVD SiO2 liner",   body: "Insulating sleeve so the copper does not short to silicon."}
- {date: Step 4, headline: "TaN/TiN barrier",    body: "Conformal layer (PVD or ALD) that stops copper diffusion."}
- {date: Step 5, headline: "Cu seed + ECD fill", body: "Electroplated copper fills the hole bottom-up; air entrapment is the dominant yield killer."}
- {date: Step 6, headline: "CMP overburden",     body: "Polish the surface flat again before metallization resumes."}
- {date: Step 7, headline: "Backside reveal",    body: "After thinning (next section), grind from the back to expose TSV tips for bumping."}
:::

The Bosch process is the heart of it. SF6 etches silicon; C4F8 deposits a fluorocarbon film on the new sidewalls; the cycle alternates every few seconds.[^19] You get a vertical hole with characteristic scalloped sidewalls that the integration flow has to tolerate. Copper electroplating then fills the hole, but here the recipe gets fragile: at 5-6 µm diameter and 36 µm depth, void-free fill requires pre-wetting, low current density (~0.06 A/dm²), and proprietary leveler/accelerator chemistry.[^20] An IEDM 2023 SK Hynix paper showed that simply increasing the count and placement of power TSVs in the bank region cut IR-drop on the stack by 62% — the TSVs are not just signal pipes, they are the power-delivery network for the whole cube.[^21]

:::callout(kind=warn, label=Yield)
Early HBM3E TSV yields ran only 40-60% per TrendForce — every void or barrier defect kills the die, and a 12-Hi stack needs twelve good dies in a row.[^22] By 2025 composite end-to-end stack yields had improved into a 50-60% band industry-wide.[^23]
:::

TSVs are also why HBM dies are 35-45% larger than DDR5 dies on the same node and yield 20-30 points lower.[^24] Each TSV consumes a "keep-out zone" of silicon around it because the differential thermal expansion between copper and silicon warps the transistors nearby.[^18] You pay for HBM's bandwidth in millimeters of die area you cannot use. SK Hynix's published density comparison is the cleanest evidence: 1z DDR4 reaches 0.296 Gb/mm²; HBM3 on the same node reaches only 0.16 Gb/mm² — DDR4 is 85% denser per square millimeter of silicon.[^25]

## 04. Thin as wallpaper — wafer grinding for the 12-Hi cube

The next constraint is geometric. JEDEC caps the package height for an HBM stack at 720 µm (HBM3) and 775 µm (HBM3E and HBM4) — roughly the thickness of nine sheets of newsprint.[^26] To fit twelve DRAM dies inside that envelope along with their bonding layers, each die has to be ground from a typical 720 µm wafer down to roughly 30 µm at HBM3 and ~20 µm at HBM3E 12-Hi.[^27] SK Hynix's own engineers describe the 12-Hi HBM3E die as 40% thinner than its 8-Hi predecessor.[^5]

:::slope(left-label="8-Hi HBM3", right-label="12-Hi HBM3E", unit="μm")
| Generation | 8-Hi HBM3 | 12-Hi HBM3E |
|------------|----------:|------------:|
| Per-die thickness | 30 | 18 |
| Stack height (JEDEC max) | 720 | 775 |
:::

The grinder is itself a near-monopoly. Disco Corporation of Japan holds an estimated 70-80% of the global market for wafer dicing, grinding, and polishing tools, and is effectively the sole supplier of the ultra-thin grinders qualified for HBM lines.[^28] Disco posted ¥436.9B in revenue in its fiscal year ending March 2026, up 11% on HBM-driven equipment sales.[^29] Its TAIKO process leaves a roughly 3 mm thick edge ring while thinning the interior — a manufacturing trick to keep the wafer rigid enough to survive downstream TSV reveal and bumping without warping into a potato chip.[^30]

:::iso
- {label: "8-Hi HBM3 stack",  glyph: "▬", count: 8}
- {label: "12-Hi HBM3E stack", glyph: "▬", count: 12}
- {label: "16-Hi HBM4 (target)", glyph: "▬", count: 16}
:::

Thin wafers are fragile. Below ~50 µm, silicon stops behaving like a brick and starts behaving like a sheet — it warps. Samsung's R&D EVP told an ECTC 2025 audience that warpage on the order of 180 µm has been observed on 16-Hi hybrid-bonded prototypes; the working tolerance has to stay below 100 µm or the bonding step fails.[^31] To handle the thinned wafer through the next dozen process steps, fabs use temporary bonding — adhesives like Brewer Science WaferBOND HT-10.10 mount the device wafer to a glass carrier, then a debond step (laser, slide-thermal, or mechanical) releases it back at the end.[^32] Brewer's guideline is total thickness variation under 5% across the device wafer; in practice the spec is held tighter, and TTV failures are a leading cause of stack-level rework.

:::callout(kind=warn, label="Failure mode")
Three things kill a thinned HBM wafer between grinding and bumping: chipping at the edge (TAIKO mitigates this), warpage in the carrier (debond stress is the usual cause), and particles from CMP or grinding that lodge between layers at the next bonding step and create voids.[^31] Each failure rejects an entire wafer's worth of dies.
:::

The migration to hybrid bonding at HBM4E/HBM5 will collapse the bump-height contribution to zero — current microbumps add 10-25 µm of standoff between dies, while hybrid bond joints add nothing — which is the only realistic path to 16-Hi (and eventually 20-Hi) stacks staying within the JEDEC height envelope.[^33] KLA's ECTC 2025 process-evolution table makes the migration explicit: from solder bump (>130 µm pitch, >80 µm height) at the start of advanced packaging, to copper pillar, to microbump (20-50 µm / 10-25 µm), to hybrid bond at <10 µm pitch and effectively zero standoff.[^33] The wafer-thinning equipment makers — Disco, Lam, Applied — are positioned to be paid twice: once for ever-thinner grinding, then again for the surface preparation that hybrid bonding requires.

## 05. Stacking the cube — MR-MUF vs TC-NCF

Bonding the twelve thinned dies into a single cube is the step where SK Hynix earned its NVIDIA monopoly. There are two competing recipes, and the choice between them is the single most important manufacturing decision in the HBM industry today.

SK Hynix uses MR-MUF — Mass Reflow with Molded Underfill. The microbumps that connect each die to the one below are placed dry; the entire stack is then heated in a single pass; molten solder reflows simultaneously across every layer; and a liquid heat-dissipating epoxy is injected under vacuum at 70 tons of pressure to fill every void.[^34] The whole stack bonds in one shot. Samsung and Micron use TC-NCF — Thermo-Compression with Non-Conductive Film. Each die is laminated with a pre-cut adhesive film, then pressed onto the stack below at ~300 °C with high force, die by die.[^35] TC-NCF is slower, runs hotter, and leaves a lower-conductivity film between layers rather than the heat-spreading epoxy MR-MUF deposits.

:::stack-rows
categories: [Throughput, Thermal path, Stack-level warpage, NVIDIA 12-Hi qual]
rows:
  - {label: "SK Hynix MR-MUF",  values: [40, 30, 20, 10]}
  - {label: "Samsung TC-NCF",   values: [25, 20, 30, 25]}
:::

The Samsung HBM3E 12-Hi was announced in February 2024 with the industry's smallest 7 µm chip-to-chip gap, achieved with advanced TC-NCF.[^36] SK Hynix announced volume production of its 12-Hi HBM3E in September 2024 with Advanced MR-MUF, claiming 10% better heat dissipation and the ability to fit 40% thinner dies in the same stack height.[^5] What followed is the disclosure story of 2024–2025.

:::timeline
- {date: 2024-02, headline: "Samsung announces 36 GB HBM3E 12-Hi",     body: "Advanced TC-NCF, 7 µm gap, 1,280 GB/s."}
- {date: 2024-09, headline: "SK Hynix volume-produces 36 GB HBM3E 12-Hi", body: "Advanced MR-MUF, 9.6 Gb/s, 1.22 TB/s."}
- {date: 2024-05, headline: "Samsung replaces DS head Kyung Kye-hyun",  body: "Jun Young-hyun installed as memory chief; HBM crisis cited."}
- {date: 2024-11, headline: "Samsung makes Jun co-CEO with memory under him", body: "Second leadership shake-up in six months."}
- {date: 2025-09, headline: "Samsung 12-Hi HBM3E reportedly clears NVIDIA", body: "~18 months after the spec-sheet announcement; volumes initially small."}
- {date: 2025-09, headline: "SK Hynix completes HBM4 development",       body: ">10 Gb/s, 2,048-bit, mass-production ready."}
- {date: 2026-02, headline: "Samsung ships commercial HBM4",             body: "11.7 Gb/s, 3.3 TB/s; first foundry-fabbed 4 nm logic base die."}
:::

The cost of the eighteen-month delay was structural. Samsung's HBM share fell from 42.4% of revenue in FY 2024[^55] to 13-17% bit share in Q1-Q2 2025 — losing the #2 position to Micron — before recovering to 22% in Q3 2025 once 12-Hi HBM3E qualified.[^37][^38] SK Hynix held 62% bit-share in Q2 2025 and 57% in Q3.[^37][^38] The leadership at Samsung's Device Solutions division was replaced twice inside six months — Kyung Kye-hyun out in May 2024, Jun Young-hyun installed as memory chief and then made co-CEO in November 2024 with memory under his direct control.[^39][^40] No corporate disclosure has linked the leadership changes to HBM specifically, but the timing is exact.

:::quote(attr="SK Hynix engineering team interview, on the 12-layer HBM3 process")
We applied intense heat momentarily to ensure that the bumps connecting the chips were evenly spliced. Then we placed a new heat-dissipating EMC material under vacuum and applied 70 tons of pressure to fill the tight spaces between the chips.
:::

:::callout(kind=success, label="Why MR-MUF won")
MR-MUF bonds the entire stack in a single thermal cycle rather than die-by-die, and the molded epoxy carries heat away from the middle dies that increasingly limit GPU clocks. Yield analysts estimate roughly a 20-point yield gap in MR-MUF's favor at 12-Hi.[^35] That gap is the proximate cause of SK Hynix's 72% operating margin in Q1 2026.
:::

The endgame is hybrid bonding — direct copper-to-copper joints with no bumps and no underfill — which both vendors plan to adopt at HBM4E or HBM5. Samsung announced hybrid bonding for HBM4 16-Hi in 2024.[^41] SK Hynix announced in September 2025 that it would keep Advanced MR-MUF for HBM4 16-Hi, having evaluated and rejected an intermediate "fluxless bonding" variant in Q4 2025.[^42] In late March 2026 SK Hynix placed its first mass-production order for the Applied Materials / BESI integrated "Kinex" die-to-wafer hybrid bonding system — at a single line, ~₩20B (~$15M), pilot scale — signaling that the migration is real but at least one generation away.[^43] Applied and BESI claim 1,600 die placements per hour on Kinex; whether that throughput is real at HBM-class stack heights is the unanswered question.

## 06. The 2.5D package — CoWoS connects the cube to the GPU

A finished HBM cube is useless on its own. It has to sit micrometers from the GPU on a silicon raft that routes its 1,024 (or 2,048) signal pins to the GPU's matching beachfront. TSMC's CoWoS (Chip-on-Wafer-on-Substrate) is that raft. CoWoS is the parallel bottleneck to HBM itself; the two have to scale together or neither ships.

CoWoS comes in three variants. CoWoS-S uses a monolithic silicon interposer up to 3.3× reticle area (~2,700 mm²). CoWoS-L stitches multiple interposer segments together using local silicon interconnect (LSI) bridges and supports >5× reticle (~4,700 mm²) — large enough to host two near-reticle GPU dies plus up to twelve HBM stacks.[^44] CoWoS-R uses a polymer-RDL interposer for cost-down. The interposer itself contains no transistors; it is roughly 65 nm-class metallization and TSVs on a passive silicon wafer.[^45]

:::rank-list
- {label: "NVIDIA A100 80GB (CoWoS-S, HBM2E)", value: "5 active stacks", pct: 31}
- {label: "NVIDIA H100 SXM5 (CoWoS-S, HBM3)",   value: "5 active / 6 sites", pct: 31}
- {label: "NVIDIA H200 (CoWoS-S, HBM3E 8-Hi)",  value: "6 stacks", pct: 38}
- {label: "NVIDIA B200 (CoWoS-L, HBM3E 8-Hi)",  value: "8 stacks", pct: 50}
- {label: "NVIDIA B300 (CoWoS-L, HBM3E 12-Hi)", value: "8 stacks", pct: 50}
- {label: "NVIDIA Vera Rubin (CoWoS-L, HBM4)",  value: "8 stacks", pct: 50, highlight: true}
- {label: "NVIDIA Rubin Ultra (CoWoS-L, HBM4E)", value: "16 stacks", pct: 100}
:::

The stack count per package roughly doubled in three years — from five HBM3 stacks on H100 (80 GB at 3.35 TB/s) to eight HBM3E 12-Hi stacks on B300 (288 GB at 8 TB/s) to eight HBM4 stacks on Vera Rubin (288 GB at ~22 TB/s).[^46][^47][^48] Rubin Ultra is targeted at sixteen HBM4E stacks per package, supporting roughly 768 GB on a 12-Hi configuration or close to 1 TB on a 16-Hi fallback.[^49] Each step required a new CoWoS reticle-size ceiling and finer interposer routing.

:::line-chart(title="TSMC CoWoS capacity, monthly wafer starts", subtitle="Endpoints from TrendForce (Dec 2024) and TokenRing (Feb 2026); midpoints interpolated.", y-unit=" k wpm")
x: 2024-Q4,2025-Q2,2025-Q4,2026-Q2,2026-Q4
CoWoS wpm: 35,55,75,100,130
:::

TSMC's CoWoS capacity has roughly quadrupled in two years — from ~35,000 wafers per month at end-2024 to a targeted 130,000 wpm by end-2026, with new fabs at Zhunan (AP6), Chiayi (AP7), and Tainan (AP8, acquired from Innolux for ~$520M in 2024).[^50][^51] On its Q1 2026 earnings call, TSMC said CoWoS capacity remained "extremely tight" and that more than 10% of its $52-56B 2026 capex — over $5B — would go to advanced packaging, test, and mask.[^52] CoWoS-L is gating Blackwell specifically: a CTE mismatch between the GPU chiplets, the LSI bridges, the RDL interposer, and the motherboard substrate caused warpage failures on the first B200 builds, forcing NVIDIA to redesign the top metal and bump layers in late 2024.[^53]

:::donut(center-label="The three-leg bottleneck")
- {label: "HBM stacks (Korea + US)",   value: 40}
- {label: "CoWoS interposer (TSMC)",   value: 40}
- {label: "ABF substrate (Japan)",     value: 20}
:::

The third leg of the bottleneck is the organic substrate — the green PCB-like layer underneath the silicon. Ajinomoto Build-up Film (ABF) is the dielectric material, and Ajinomoto is the sole supplier; five board makers (Unimicron, Ibiden, AT&S, Nan Ya PCB, Shinko) hold ~74% of the substrate market.[^54] Ajinomoto has committed to expanding ABF film capacity 50% by 2030 — too late to relieve the current bottleneck. All three legs — HBM, interposer, substrate — must clear together for an AI accelerator to ship. {accent}This is why "HBM is sold out" and "CoWoS is sold out" and "ABF is sold out" are the same sentence said three different ways.{/}

## 07. The duopoly economics — share, pricing, and who owns the NVIDIA queue

HBM is a near-duopoly with an American challenger. In 2024, SK Hynix held 52.5% of HBM revenue, Samsung 42.4%, and Micron 5.1%.[^55] That distribution shifted hard inside 2025 as Samsung struggled with NVIDIA qualification and Micron ramped HBM3E. By Q2 2025, Counterpoint's bit-share read was SK Hynix 62%, Micron 21%, Samsung 17% — Micron had overtaken Samsung for #2.[^37] By Q3, Samsung recovered to 22% while SK Hynix gave back to 57%.[^37] HBM revenue itself roughly doubled from 2024 to 2025 (Yole and Micron both anchored 2025 at ~$35B); the prior $100B TAM target has been pulled in from 2030 to 2028.[^56]

:::donut(center-label="2024")
- {label: "SK Hynix",  value: 52.5}
- {label: "Samsung",   value: 42.4}
- {label: "Micron",    value: 5.1}
:::

:::slope(left-label="Q2 2025", right-label="Q3 2025", unit="% bit share")
| Vendor | Q2 2025 | Q3 2025 |
|--------|--------:|--------:|
| SK Hynix | 62 | 57 |
| Micron   | 21 | 21 |
| Samsung  | 17 | 22 |
:::

NVIDIA is the single biggest customer of all three, accounting for more than 60% of HBM3E consumption in 2024 per Morgan Stanley estimates relayed by TrendForce.[^57] In the first half of 2025, NVIDIA alone reportedly drove ~27% of SK Hynix's total revenue (~₩11T of ₩39.9T).[^58] SK Hynix's CEO formalized the contract cycle in March 2025: all 2026 HBM supply commitments would be locked by mid-2025, a forward-booking cadence the company has now repeated for 2027.[^59] In its Q3 2025 earnings call, SK Hynix said total DRAM, NAND, and HBM capacity for 2026 was already sold out.[^60] The company posted ₩52.58T revenue and a 72% operating margin in Q1 2026 — the cleanest read on how the duopoly economics translate into financial results.[^87]

:::line-chart(title="HBM supply-chain market caps, monthly", subtitle="MU, NVDA, ASML — 2 years to 2026-05.", y-unit=$)
x: 2024-06,2024-07,2024-08,2024-09,2024-10,2024-11,2024-12,2025-01,2025-02,2025-03,2025-04,2025-05,2025-06,2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05
MU: 131.53,109.82,96.24,103.71,99.65,97.95,84.16,91.24,93.63,86.89,76.95,94.46,123.25,109.14,119.01,167.32,223.77,236.48,285.41,414.88,412.37,337.84,517.16,724.66
NVDA: 123.54,117.02,119.37,121.44,132.76,138.25,134.29,120.07,124.92,108.38,108.92,135.13,157.99,177.87,174.18,186.58,202.49,177.0,186.5,191.13,177.19,174.4,199.57,225.32
ASML: 1022.73,936.7,903.87,833.25,672.55,686.61,693.08,739.31,709.08,662.63,668.08,736.77,801.39,694.71,742.62,968.09,1059.23,1060.0,1069.86,1423.0,1450.56,1320.83,1438.99,1501.81
:::

The pricing is the inversion. HBM3E sold for roughly 4-5× server DDR5 per gigabit through 2024-2025, before the gap began narrowing toward 1-2× by end-2026 as DDR5 caught up.[^61] HBM's value share of the overall DRAM market climbed past 20% in 2024 and over 30% in 2025, up from single digits in 2023.[^62] HBM bit supply grew 260% in 2024 — and ASPs rose in parallel, the textbook inversion of commodity-DRAM behavior.[^63] HBM4 contract pricing reportedly settled in the mid-$500s per stack for first-year NVIDIA volumes, roughly 60-70% above HBM3E 12-Hi at ~$300.[^64] One trade-press estimate has NVIDIA paying Samsung ~$500 per HBM4 module versus ~$250 per HBM3E module — a doubling within one product generation.[^65]

:::stats
- {label: "SK Hynix Q1'26 revenue", value: "₩52.6", unit: T,  note: "+198% YoY"}
- {label: "SK Hynix Q1'26 OP margin", value: "72",  unit: "%", note: "memory company, 1Q"}
- {label: "NVIDIA share of SK Hynix 1H25 revenue", value: "27", unit: "%"}
- {label: "HBM revenue 2025E",     value: "$35", unit: B, note: "vs ~$16B in 2024"}
- {label: "HBM share of DRAM revenue", value: "30",  unit: "%", note: "from 8% in 2023"}
- {label: "Micron HBM run-rate Q3 FY25", value: "$6", unit: "B+", note: ">$24B annualized late-FY26"}
:::

:::quote(attr="Jensen Huang, NVIDIA, January 2026")
NVIDIA is the sole client for HBM4 for quite a long time, and as the initial and sole customer for HBM4, Team Green will be the beneficiary for now.
:::

Micron's trajectory is the cleanest tell. The company skipped HBM and HBM2 entirely, qualified HBM3E 8-Hi at NVIDIA for the H200 in February 2024, passed 12-Hi qualification for Blackwell Ultra in early 2025, and shipped HBM4 12-Hi to Vera Rubin in Q1 calendar 2026.[^66][^67][^68] CEO Sanjay Mehrotra has said publicly that Micron's HBM share will converge to its overall DRAM share (~22-23%) — implying a HBM revenue trajectory toward ~$8B annualized by late FY26, then higher.[^69] The US government finalized $6.165B in CHIPS funding for Micron's Boise R&D fab and Clay, New York mega-fab in December 2024; an expanded ~$200B US investment commitment followed in June 2025, including a domestic HBM packaging line at Manassas, Virginia.[^70][^71]

## 08. HBM4 — the architectural break, not just a faster bus

JEDEC ratified HBM4 in April 2025 as JESD270-4. The headline numbers — 2 TB/s per stack at 8 Gb/s, 16-Hi stacks of up to 64 GB on 32 Gb dies — understate what changed. HBM4 is the first generation since 2013 to widen the physical interface (from 1,024 to 2,048 bits) and the first to move the base die off of DRAM process and onto a true logic process.[^6][^17]

:::stats
- {label: Interface width,        value: "2,048", unit: " bit", note: "doubled from HBM3"}
- {label: Channels per stack,     value: "32",                   note: "+2 pseudo-channels"}
- {label: Max stack height,       value: "16-Hi",                note: "64 GB at 32 Gb dies"}
- {label: Spec speed,             value: "8",     unit: " Gb/s", note: "vendors at 10-13 Gb/s"}
- {label: Per-bit energy target,  value: "<3",    unit: " pJ/b", note: "vs ~4 at HBM3E"}
- {label: Microbumps per stack,   value: "~3,000",               note: "from ~1,500-2,000 at HBM3"}
:::

The 2,048-bit interface roughly doubles the microbump count per stack to ~3,000+ and grows the PHY area on the base die by ~36% (from ~11 mm² at HBM3E to ~15 mm² at HBM4E on TSMC N3P).[^17][^72] On its own this would be a routing nightmare. The fix is to move the base die from a DRAM process (~14-16 nm DRAM logic) to a real logic node where the controller, PHY, and any customer-specified accelerator logic can fit in the area budget. SK Hynix announced in April 2024 that TSMC would fabricate the HBM4 base die using its advanced logic process — the first time the bottom layer of an HBM stack is built outside the memory company.[^73] Trade reporting points to TSMC N3 for NVIDIA-bound premium HBM4 and N12FFC/N5 for mainstream parts; the "custom HBM4E" variant lives on N3P.[^74][^75]

:::kv
- {term: "SK Hynix HBM4 base die",     def: "TSMC N3 (NVIDIA tier) / N12 (mainstream)"}
- {term: "Samsung HBM4 base die",      def: "Samsung Foundry 4 nm — in-house, vertical-integration play"}
- {term: "Micron HBM4 base die",       def: "TSMC N12FFC+ or N5 — de-risked logic node"}
- {term: "Custom HBM4E (C-HBM4E)",     def: "TSMC N3P, customer-specified controller and accelerator logic"}
- {term: "NVIDIA in-house HBM base die", def: "Reported TSMC N3 trial, H2 2027 small-batch"}
:::

The custom-base-die opportunity is the second-order story. SK Hynix's roster of custom-HBM4E customers includes NVIDIA, Microsoft, and Broadcom for H2 2026 production; NVIDIA is separately reported to be designing its own HBM base die for trial production in late 2027, with SK Hynix doing the stacking.[^76][^77] Samsung is allocating over half of its Pyeongtaek 4 nm foundry capacity to its own HBM4 base dies and is rumored to be the exclusive HBM4 supplier for OpenAI's Titan AI chip in 2H 2026.[^78] These customer-customizable base dies turn HBM from a commodity catalog part into a co-designed component — and the engineering capacity required to do them is itself rationed.

:::timeline
- {date: 2024-04, headline: "SK Hynix–TSMC HBM4 base die partnership", body: "First time the base die moves off DRAM process and onto a logic process."}
- {date: 2025-03, headline: "SK Hynix ships first 12-Hi HBM4 samples",  body: "Six months ahead of original 2026 schedule; matches NVIDIA Rubin pull-in."}
- {date: 2025-04, headline: "JEDEC publishes HBM4 (JESD270-4)",         body: "2,048-bit interface, 32 channels, 16-Hi 64 GB ceiling."}
- {date: 2025-09, headline: "SK Hynix completes HBM4 development",       body: ">10 Gb/s, mass-production system ready."}
- {date: 2026-02, headline: "Samsung ships commercial HBM4",             body: "11.7 Gb/s, 4 nm in-house base die, 40% power efficiency vs HBM3E."}
- {date: 2026-Q1, headline: "Micron HBM4 12-Hi HVM for Vera Rubin",      body: ">11 Gb/s, >2.8 TB/s per stack, FY26 supply fully booked."}
:::

The competitive shape that emerges from HBM4 is unusual. SK Hynix leads on stacking process and customer share but depends on TSMC for the base die. Samsung is uniquely vertically integrated (DRAM + foundry + packaging in-house) and is using that integration to court customers Hynix cannot serve as flexibly. Micron is the de-risked option, using mature nodes and gaining a US policy moat. None of them are easily displaced.

## 09. What could break the thesis

HBM bears the marks of a winner-take-most market with three suppliers, one buyer (NVIDIA + a few large ASIC customers), and a multi-year backlog. That structure is brittle in specific ways.

:::rank-list
- {label: "NVIDIA insources the HBM base die (TSMC N3, 2027)", value: "Erodes vendor differentiation", pct: 100}
- {label: "Hybrid bonding tooling slips → HBM4E 16-Hi delays", value: "Compresses 2027-28 capacity",  pct: 80}
- {label: "CXMT qualifies HBM3 at Huawei in 2026",             value: "Adds 4th supplier, China-only",  pct: 60}
- {label: "DDR5 ASPs rise faster than HBM (already starting)", value: "Reverses wafer allocation",     pct: 60}
- {label: "GDDR7 + inference accelerators replace HBM at the edge", value: "Bifurcates the AI memory TAM", pct: 50}
- {label: "Ajinomoto ABF capacity remains the gate through 2027", value: "Slows total AI accelerator output", pct: 50}
:::

The most concrete risk is also the most visible. Samsung is already reallocating ~80,000 wafers per month from HBM lines back to DDR5 RDIMM, where 64 GB modules with $450 ASPs at >75% gross margins now offer better economics than HBM at Samsung's yield level.[^79] If DDR5 server premium economics persist into 2026, the entire industry's wafer split between HBM and commodity DRAM is in motion — which would in turn relieve HBM supply but tighten commodity supply. {accent}The same mechanism — HBM consumes roughly 3× the wafer area per gigabit of DDR5{/} — works in both directions.[^80]

:::callout(kind=danger, label=Concentration)
The combined SK Hynix + Samsung share of global HBM was 93% in 2024 and 79% in Q3 2025. Both operate primarily in the Korean peninsula, with one logistics hub for the world's AI memory. A natural disaster, labor stoppage, or geopolitical shock in Korea has no near-term substitute. Micron's US capacity, even fully ramped, would not close the gap before 2028.
:::

The longer-tail risk is Chinese entry. CXMT (ChangXin Memory Technologies) was reported in August 2024 to have begun HBM2 mass production, ~two years ahead of its original 2026 schedule, with Huawei's Ascend AI accelerators as the anchor customer.[^81] Morgan Stanley's May 2025 read characterized CXMT's status as sampling with small-scale production by mid-2025, and HBM3 timing pushed to 2026.[^82] As of April 2026, Korean trade press reported HBM3 mass production in 2026 was "unlikely" despite CXMT's $4.2B Shanghai STAR IPO.[^83] US BIS export rules from December 2024 cap China's legal HBM access at memory-bandwidth-density below 3.3 GB/s/mm² — effectively HBM2, not HBM2E or above.[^84] NVIDIA's China-spec H20 carries 96 GB of HBM3 (more than H100's 80 GB) but with throttled compute, demonstrating the regulatory boundary.[^85] The Chinese supply chain — CXMT for DRAM die, Wuhan Xinxin / YMTC for stacking, Naura / Maxwell for tools — is taking shape, but each leg has yield and capacity gaps.[^86]

The architectural risk is in NVIDIA's hands. If NVIDIA brings the HBM base die in-house in 2027 — as supply-chain reporting suggests is in progress on TSMC N3 — then HBM moves from a co-designed component back toward a memory-only catalog part, and the value capture on the base die shifts from the memory makers to NVIDIA.[^77] The HBM vendors would still own the DRAM die, the TSV, the thinning, and the bonding — the hard parts of this article — but the strategic surface area they sit on would shrink.

The optimistic case is also concrete: HBM revenue may exceed $54B in 2026 (BofA), hit $100B in 2028 (Micron's revised TAM), and remain capacity-constrained throughout because every meaningful AI accelerator on every roadmap from now to Rubin Ultra needs more HBM per package than the previous generation.[^56] What would falsify that case: a meaningful slowdown in frontier-model training capex (which has not happened), a substitute architecture that uses less HBM per FLOP (which would require a model-side breakthrough), or a CXMT-class entrant clearing NVIDIA qualification (which is years away even in the bull case).

The chip itself, in the end, is a 30-micrometer-thick stack of memory wafers welded onto a silicon raft. Everything else — the share war, the pricing inversion, the geopolitics, the trillion-dollar capex projections — flows from how hard those welds are to make.

:::references
- {id: 1, title: "JEDEC JESD235 HBM standard (originally October 2013)", url: "https://en.wikipedia.org/wiki/High_Bandwidth_Memory", source: Wikipedia / JEDEC summary, date: "2013-10-01"}
- {id: 2, title: "JEDEC publishes JESD238 HBM3 spec", url: "https://www.servethehome.com/jedec-publishes-jesd238-hbm3-spec-for-next-gen-accelerators/", source: ServeTheHome, date: "2022-01-27"}
- {id: 3, title: "AnandTech on JESD235C HBM2E update", url: "https://www.anandtech.com/show/15469/", source: AnandTech, date: "2020-02-12"}
- {id: 4, title: "AMD HBM whitepaper", url: "https://vgamuseum.info/images/doc/amd/high-bandwidth-memory-hbm.pdf", source: AMD, date: "2015-05-19"}
- {id: 5, title: "SK Hynix begins volume production of 12-layer HBM3E", url: "https://news.skhynix.com/sk-hynix-begins-volume-production-of-the-world-first-12-layer-hbm3e/", source: SK Hynix Newsroom, date: "2024-09-26"}
- {id: 6, title: "JEDEC publishes JESD270-4 HBM4 standard", url: "https://www.jedec.org/news/pressreleases/jedec%C2%AE-and-industry-leaders-collaborate-release-jesd270-4-hbm4-standard-advancing", source: JEDEC, date: "2025-04-16"}
- {id: 7, title: "Scaling the Memory Wall: HBM technical analysis", url: "https://newsletter.semianalysis.com/p/scaling-the-memory-wall-the-rise-and-roadmap-of-hbm", source: SemiAnalysis, date: "2024-04-01"}
- {id: 8, title: "SK Hynix develops industry-first 1c DDR5", url: "https://news.skhynix.com/sk-hynix-develops-industry-first-1c-ddr5/", source: SK Hynix Newsroom, date: "2024-08-29"}
- {id: 9, title: "Samsung ships industry-first commercial HBM4", url: "https://semiconductor.samsung.com/news-events/news/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing/", source: Samsung Semiconductor, date: "2026-02-12"}
- {id: 10, title: "Micron announces shipment of 1-gamma DRAM", url: "https://www.globenewswire.com/news-release/2025/02/25/3032114/14450/en/Micron-Announces-Shipment-of-1%CE%B3-1-gamma-DRAM-Pioneering-Memory-Technology-Advancements-for-Future-Compute-Needs.html", source: Micron / GlobeNewswire, date: "2025-02-25"}
- {id: 11, title: "SK Hynix ramps 1c DRAM to 6 EUV layers", url: "https://www.tweaktown.com/news/106957/sk-hynix-ramps-1c-dram-to-6-euv-layers-preps-for-high-na-designs-destroy-samsung-in-hbm/index.html", source: TweakTown, date: "2024-09-30"}
- {id: 12, title: "Samsung reportedly mulls 1a DRAM redesign amid HBM3E delays", url: "https://www.trendforce.com/news/2024/10/18/news-samsung-reportedly-mulls-1a-dram-redesign-amid-hbm3e-verification-delays/", source: TrendForce, date: "2024-10-18"}
- {id: 13, title: "ASML TWINSCAN NXE:3800E EUV product page", url: "https://www.asml.com/en/products/euv-lithography-systems/twinscan-nxe-3800e", source: ASML, date: "2024-03-01"}
- {id: 14, title: "ASML memory chip orders explode past logic", url: "https://wccftech.com/asml-memory-chip-orders-explode-past-logic-first-time-as-dram-makers-scramble-for-euv-slots/", source: WccfTech, date: "2026-02-15"}
- {id: 15, title: "SK Hynix installs first High-NA EUV", url: "https://www.trendforce.com/news/2025/09/03/news-sk-hynix-leads-the-pack-to-introduce-asmls-high-na-euv-system-for-memory-production/", source: TrendForce, date: "2025-09-03"}
- {id: 16, title: "TSV Complexity Leads to Manufacturing Bottleneck", url: "https://semiengineering.com/tsv-complexity-leads-to-manufacturing-bottleneck/", source: Semiconductor Engineering, date: "2024-04-01"}
- {id: 17, title: "TSMC and GUC detail HBM4, HBM4E, C-HBM4E", url: "https://www.tomshardware.com/pc-components/dram/hbm-undergoes-major-architectural-shakeup-as-tsmc-and-guc-detail-hbm4-hbm4e-and-c-hbm4e-3nm-base-dies-to-enable-2-5x-performance-boost-with-speeds-of-up-to-12-8gt-s-by-2027", source: Tom's Hardware, date: "2025-06-01"}
- {id: 18, title: "What's Next For TSVs (Lam Research)", url: "https://semiengineering.com/whats-next-for-tsvs/", source: Semiconductor Engineering, date: "2025-01-06"}
- {id: 19, title: "Copper-filling process for small-diameter TSVs", url: "https://s-pack.org/wp-content/uploads/2022/12/Copper-filling-process-for-small-diameter-high-aspect-ratio-Through-Silicon-Via-TSV.pdf", source: Tsinghua University, date: "2014-12-01"}
- {id: 20, title: "AIST ECTC 2024 via-reveal paper", url: "https://www.semanticscholar.org/paper/6b7c81b5d4fc9b6ee346553d51bad68688003ff3", source: ECTC / AIST, date: "2024-05-27"}
- {id: 21, title: "IEDM 2023 SK Hynix HBM packaging paper", url: "https://iedm23.mapyourshow.com/mys_shared/iedm23/handouts/15-6_Tue_14482.pdf", source: IEEE IEDM, date: "2023-12-01"}
- {id: 22, title: "TrendForce on HBM3E TSV yields", url: "https://www.trendforce.com/presscenter/news/20240506-12125.html", source: TrendForce, date: "2024-05-06"}
- {id: 23, title: "AI-driven DRAM shortage and HBM yields", url: "https://markets.financialcontent.com/wral/article/tokenring-2025-12-26-ai-driven-dram-shortage-intensifies-as-sk-hynix-and-samsung-pivot-to-hbm4-production", source: TokenRing / FinancialContent, date: "2025-12-26"}
- {id: 24, title: "HBM die size and yield vs DDR5", url: "https://marklapedus.substack.com/p/high-bandwidth-memory-hbm-is-sold", source: Mark LaPedus / TrendForce, date: "2024-05-01"}
- {id: 25, title: "SK Hynix DRAM bit density (D1z DDR4 vs HBM3)", url: "https://newsletter.semianalysis.com/p/scaling-the-memory-wall-the-rise-and-roadmap-of-hbm", source: SemiAnalysis, date: "2024-04-01"}
- {id: 26, title: "Samsung HBM4 hybrid bonding and JEDEC stack height", url: "https://www.tomshardware.com/pc-components/dram/samsung-to-adopt-hybrid-bonding-for-hbm4-memory", source: Tom's Hardware, date: "2025-05-13"}
- {id: 27, title: "SK Hynix HBM3 development with 30 µm die thickness", url: "https://news.skhynix.com/sk-hynix-announces-development-of-hbm3-dram/", source: SK Hynix Newsroom, date: "2021-10-20"}
- {id: 28, title: "Disco Corporation HBM equipment dominance", url: "https://www.digitimes.com/news/a20240110PD201/disco-semiconductors-equipment-hbm-sic.html", source: Digitimes, date: "2024-01-10"}
- {id: 29, title: "Disco Corp FY2026 results", url: "https://www.tradingview.com/news/gurufocus:68564a0d3094b:0-disco-corp-the-precision-toolmaker-quietly-dominating-the-semiconductor-boom/", source: TradingView / GuruFocus, date: "2026-04-22"}
- {id: 30, title: "Disco TAIKO process whitepaper", url: "https://www.disco.co.jp/eg/solution/library/grinder/taiko_process.html", source: Disco Corporation, date: "2024-01-01"}
- {id: 31, title: "Samsung ECTC 2025 hybrid bonding warpage", url: "https://ectc.net/wp-content/uploads/2025/06/ECTC2025_SpecialSession_2-Hybrid-Bonding.pdf", source: IEEE ECTC 2025, date: "2025-05-27"}
- {id: 32, title: "Brewer Science WaferBOND temporary bonding", url: "https://www.brewerscience.com/processing-theories/temporary-bonding/", source: Brewer Science, date: "2024-01-01"}
- {id: 33, title: "KLA hybrid bonding bump-evolution table ECTC 2025", url: "https://ectc.net/wp-content/uploads/2025/06/ECTC2025_SpecialSession_2-Hybrid-Bonding.pdf", source: IEEE ECTC 2025 / KLA, date: "2025-05-27"}
- {id: 34, title: "SK Hynix engineering team interview on 12-layer HBM3", url: "https://news.skhynix.com/meet-the-sk-hynix-team-behind-the-worlds-first-12-layer-hbm3/", source: SK Hynix Newsroom, date: "2023-07-01"}
- {id: 35, title: "Deep dive on MR-MUF vs TC-NCF", url: "https://www.nomadsemi.com/p/deep-dive-on-hbm", source: NomadSemi, date: "2024-08-01"}
- {id: 36, title: "Samsung develops industry-first 36GB HBM3E 12-Hi", url: "https://semiconductor.samsung.com/news-events/news/samsung-develops-industry-first-36gb-hbm3e-12h-dram/", source: Samsung Semiconductor, date: "2024-02-27"}
- {id: 37, title: "Counterpoint Q3 2025 HBM share", url: "https://marklapedus.substack.com/p/sk-hynix-lead-shrinks-in-dram-hbm", source: Counterpoint / Mark LaPedus, date: "2025-12-24"}
- {id: 38, title: "SK Hynix 62% / Micron overtakes Samsung Q2 2025", url: "https://www.astutegroup.com/news/general/sk-hynix-holds-62-of-hbm-micron-overtakes-samsung-2026-battle-pivots-to-hbm4/", source: Astute Group, date: "2025-09-15"}
- {id: 39, title: "Samsung leadership change Jun Young-hyun May 2024", url: "https://www.trendforce.com/news/2024/05/21/news-samsung-leadership-change-young-hyun-jun-to-head-device-solutions-division/", source: TrendForce, date: "2024-05-21"}
- {id: 40, title: "Samsung Nov 2024 co-CEO reshuffle", url: "https://www.kedglobal.com/executive-reshuffles/newsView/ked202411270012", source: Korea Economic Daily, date: "2024-11-27"}
- {id: 41, title: "Samsung 12H HBM3E clears NVIDIA after 18-month setback", url: "https://www.trendforce.com/news/2025/09/22/news-samsung-12h-hbm3e-reportedly-clears-nvidia-tests-after-18-month-setback-hbm4-reaches-final-phase/", source: TrendForce, date: "2025-09-22"}
- {id: 42, title: "SK Hynix sticks with MR-MUF for HBM4 16-Hi", url: "https://www.trendforce.com/news/2026/01/13/news-sk-hynix-may-stick-with-mr-muf-for-hbm4-16-high-despite-asmpt-tc-bonder-orders/", source: TrendForce, date: "2026-01-13"}
- {id: 43, title: "SK Hynix orders Applied/BESI Kinex hybrid bonding line", url: "https://www.thelec.net/news/articleView.html?idxno=6246", source: The Elec, date: "2026-03-31"}
- {id: 44, title: "CoWoS-S vs R vs L variants and reticle limits", url: "https://www.aminext.blog/en/post/tsmc-cowos-s-r-l-differences", source: AmiNext, date: "2024-08-01"}
- {id: 45, title: "AI Expansion Supply Chain Analysis (CoWoS interposer)", url: "https://newsletter.semianalysis.com/p/ai-expansion-supply-chain-analysis", source: SemiAnalysis, date: "2023-07-26"}
- {id: 46, title: "NVIDIA H100 / Hopper Architecture In-Depth", url: "https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/", source: NVIDIA Developer Blog, date: "2022-03-22"}
- {id: 47, title: "NVIDIA H200 product page", url: "https://www.nvidia.com/en-us/data-center/h200/", source: NVIDIA, date: "2024-03-01"}
- {id: 48, title: "NVIDIA Rubin platform technical blog", url: "https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/", source: NVIDIA Developer Blog, date: "2026-03-01"}
- {id: 49, title: "NVIDIA Rubin Ultra 16-stack configuration", url: "https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date", source: Tom's Hardware, date: "2026-03-15"}
- {id: 50, title: "TSMC CoWoS capacity tripling by 2026", url: "https://www.trendforce.com/news/2024/12/13/news-tsmc-ramps-up-cowos-capacity-across-taiwan-projected-to-nearly-triple-by-2026/", source: TrendForce, date: "2024-12-13"}
- {id: 51, title: "TSMC to quadruple advanced packaging capacity to 130k wpm", url: "https://markets.financialcontent.com/stocks/article/tokenring-2026-2-5-tsmc-to-quadruple-advanced-packaging-capacity-reaching-130000-cowos-wafers-monthly-by-late-2026", source: TokenRing / FinancialContent, date: "2026-02-05"}
- {id: 52, title: "TSMC Q1 2026 earnings transcript on CoWoS capacity", url: "https://investor.tsmc.com/", source: TSMC Investor Relations, date: "2026-04-17"}
- {id: 53, title: "Why NVIDIA Blackwell is having issues with CoWoS-L", url: "https://www.3dincites.com/2024/10/iftle-607-why-nvidias-blackwell-is-having-issues-with-tsmc-cowos-l-technology/", source: 3D InCites / IFTLE, date: "2024-10-01"}
- {id: 54, title: "ABF substrate packaging expansion (Ajinomoto monopoly)", url: "https://www.digitimes.com/news/a20251218PD207/abf-substrate-packaging-expansion-ai-gpu-capacity.html", source: Digitimes, date: "2025-12-18"}
- {id: 55, title: "TrendForce HBM 2024 share (Hynix 52.5 / Samsung 42.4 / Micron 5.1)", url: "https://www.trendforce.com/research/download/RP251029MY", source: TrendForce, date: "2025-10-29"}
- {id: 56, title: "HBM supply curve gets steeper but still can't meet demand", url: "https://www.nextplatform.com/2025/12/19/hbm-supply-curve-gets-steeper-but-still-cant-meet-demand/", source: The Next Platform, date: "2025-12-19"}
- {id: 57, title: "NVIDIA accounts for over 60% of global HBM consumption in 2024", url: "https://www.trendforce.com/presscenter/news/20240808-12248.html", source: TrendForce, date: "2024-08-08"}
- {id: 58, title: "NVIDIA drives 27% of SK Hynix 1H25 revenue", url: "https://www.trendforce.com/news/2025/08/18/news-nvidia-reportedly-drives-27-of-sk-hynix-revenue-in-1h25-cementing-ai-chip-partnership", source: TrendForce, date: "2025-08-18"}
- {id: 59, title: "SK Hynix CEO: 2026 HBM orders locked by mid-2025", url: "https://www.kedglobal.com/korean-chipmakers/newsView/ked202503270004", source: Korea Economic Daily, date: "2025-03-27"}
- {id: 60, title: "SK Hynix Q3 2025: capacity sold out for 2026", url: "https://www.cnbc.com/2025/10/29/sk-hynix-q3-profit-revenue-record-.html", source: CNBC, date: "2025-10-29"}
- {id: 61, title: "HBM3E to DDR5 pricing ratio narrowing to 1-2x by end-2026", url: "https://www.trendforce.com/presscenter/news/20251218-12843.html", source: TrendForce, date: "2025-12-18"}
- {id: 62, title: "HBM share of DRAM revenue: 8.4% (2023) → 20.1% (2024) → >30% (2025)", url: "https://www.trendforce.com/presscenter/news/20240506-12125.html", source: TrendForce, date: "2024-05-06"}
- {id: 63, title: "HBM 260% supply bit growth in 2024", url: "https://www.trendforce.com/presscenter/news/20240318-12081.html", source: TrendForce, date: "2024-03-18"}
- {id: 64, title: "SK Hynix HBM4 12-Hi at $500 to NVIDIA", url: "https://www.tweaktown.com/news/106826/sk-hynix-drastically-raises-next-gen-hbm4-supply-price-in-war-of-nerves-with-nvidia/index.html", source: TweakTown, date: "2025-08-06"}
- {id: 65, title: "NVIDIA pays Samsung ~$500 per HBM4 module", url: "https://www.notebookcheck.net/Nvidia-may-raise-prices-as-it-pays-Samsung-double-for-future-HBM4-AI-memory-modules-with-3-3-TB-s-bandwidth.1172580.0.html", source: NotebookCheck, date: "2026-01-15"}
- {id: 66, title: "Micron commences volume production of HBM3E for NVIDIA H200", url: "https://investors.micron.com/news-releases/news-release-details/micron-commences-volume-production-industry-leading-hbm3e", source: Micron Investor Relations, date: "2024-02-26"}
- {id: 67, title: "Micron HBM4 product page", url: "https://www.micron.com/products/memory/hbm/hbm4", source: Micron, date: "2025-09-01"}
- {id: 68, title: "Micron enters HVM of HBM4 for NVIDIA Vera Rubin", url: "https://www.tomshardware.com/pc-components/dram/micron-enters-high-volume-production-of-hbm4-for-nvidia-vera-rubin", source: Tom's Hardware, date: "2026-03-18"}
- {id: 69, title: "Micron Q3 FY25 results — HBM share target", url: "https://blocksandfiles.com/2025/06/26/micron-q3-2025/", source: Blocks & Files, date: "2025-06-26"}
- {id: 70, title: "Commerce Dept awards $6.165B CHIPS funding to Micron", url: "https://www.commerce.gov/news/press-releases/2024/12/department-commerce-awards-chips-incentives-micron-idaho-and-new-york", source: US Department of Commerce, date: "2024-12-10"}
- {id: 71, title: "Micron expands US investment to ~$200B (incl HBM packaging)", url: "https://www.globenewswire.com/news-release/2025/06/12/3098344/14450/en/Micron-and-Trump-Administration-Announce-Expanded-U-S-Investments-in-Leading-Edge-DRAM-Manufacturing-and-R-D.html", source: Micron / GlobeNewswire, date: "2025-06-12"}
- {id: 72, title: "DesignCon 2025 paper on HBM3/4 interposer", url: "https://www.signalintegrityjournal.com/ext/resources/PDFs/DC25_PAPER_Track05_InnovativeInterposerSolutionsforHBM_Ilamparidhi_V6.pdf", source: DesignCon 2025, date: "2025-01-01"}
- {id: 73, title: "SK Hynix partners with TSMC on HBM4 base die", url: "https://news.skhynix.com/sk-hynix-partners-with-tsmc-to-strengthen-hbm-technological-leadership/", source: SK Hynix Newsroom, date: "2024-04-19"}
- {id: 74, title: "SK Hynix HBM4 to use TSMC 3nm base die", url: "https://www.trendforce.com/news/2024/12/04/news-sk-hynixs-hbm4-to-use-tsmcs-3nm-base-die/", source: TrendForce, date: "2024-12-04"}
- {id: 75, title: "SK Hynix completes HBM4 development, readies mass production", url: "https://news.skhynix.com/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/", source: SK Hynix Newsroom, date: "2025-09-12"}
- {id: 76, title: "SK Hynix custom HBM customers (NVIDIA / Microsoft / Broadcom)", url: "https://www.digitimes.com/news/a20250620VL205/sk-hynix-hbm-nvidia-microsoft-broadcom.html", source: Digitimes, date: "2025-06-20"}
- {id: 77, title: "NVIDIA reportedly eyes small-scale HBM base die production 2027", url: "https://www.trendforce.com/news/2025/08/18/news-nvidia-reportedly-eyes-small-scale-hbm-base-die-production-in-2027-rattling-memory-chip-markets/", source: TrendForce, date: "2025-08-18"}
- {id: 78, title: "Samsung allocates >50% of Pyeongtaek foundry to HBM4 base die / OpenAI", url: "https://www.trendforce.com/news/2026/03/20/news-samsung-reportedly-allocates-50-of-pyeongtaek-foundry-capacity-to-hbm4-base-die-said-to-win-openai-as-customer/", source: TrendForce, date: "2026-03-20"}
- {id: 79, title: "Samsung shifts 80k wafers/mo from HBM to DDR5 RDIMM", url: "https://www.digitimes.com/news/a20251208PD214/samsung-hbm-ddr5-dram-capacity.html", source: Digitimes, date: "2025-12-08"}
- {id: 80, title: "HBM consumes ~3x the wafer capacity per gigabyte of DDR5", url: "https://www.tomshardware.com/pc-components/ram/hbm-is-eating-your-ram", source: Tom's Hardware, date: "2025-12-19"}
- {id: 81, title: "CXMT begins HBM2 mass production ahead of schedule", url: "https://www.trendforce.com/news/2024/08/06/news-changxin-memory-technologies-has-reportedly-begun-mass-production-of-hbm2/", source: TrendForce, date: "2024-08-06"}
- {id: 82, title: "Morgan Stanley CXMT HBM2 sampling note", url: "https://x.com/Jukanlosreve/status/1927516409006792736", source: Morgan Stanley via X (Jukan), date: "2025-05-27"}
- {id: 83, title: "CXMT HBM3 mass production unlikely in 2026", url: "https://www.digitimes.com/news/a20260421PD230/cxmt-hbm3-dram-production-2026.html", source: Digitimes, date: "2026-04-22"}
- {id: 84, title: "US BIS License Exception HBM (15 CFR 740.25)", url: "https://www.law.cornell.edu/cfr/text/15/740.25", source: 15 CFR 740.25 / Cornell Law, date: "2024-12-05"}
- {id: 85, title: "NVIDIA H20 96GB HBM3 China-spec configuration", url: "https://www.tweaktown.com/news/95224/nvidias-tweaked-h20-ai-gpu-enters-mass-production-in-q2-2024-destined-for-china/index.html", source: TweakTown, date: "2024-04-01"}
- {id: 86, title: "Chinese domestic HBM3 supply chain map", url: "https://www.tomshardware.com/pc-components/dram/chinese-semiconductor-industry-gears-up-for-domestic-hbm3-production-by-the-end-of-2026-cxmt-to-produce-chips-while-naura-maxwell-and-u-preseason-design-tools-for-assembly", source: Tom's Hardware, date: "2025-04-01"}
- {id: 87, title: "SK Hynix Q1 2026 business results", url: "https://news.skhynix.com/q1-2026-business-results/", source: SK Hynix Newsroom, date: "2026-04-23"}
:::
