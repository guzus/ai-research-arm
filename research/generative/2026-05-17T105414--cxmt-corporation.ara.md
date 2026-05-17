---
eyebrow: REPORT · COMPANY · CXMT
title: 'CXMT comes into focus: a Hefei-financed fourth player rewrites the global DRAM map'
deck: A Dec 30 2025 STAR Market prospectus turned China's biggest DRAM project from a black box into a numbered company. The numbers explain three otherwise puzzling facts about the 2025–2026 memory cycle.
lede: |
  ChangXin Memory Technologies — Project 506 in its 2016 origin, "Innotron" in its 2018 marketing, and CXMT after a 2019 rename[^8] — filed a 6.77 MB prospectus with the Shanghai Stock Exchange on the evening of December 30, 2025, seeking RMB 29.5 billion (~US$4.2 billion) at an implied valuation near RMB 300 billion (~US$42 billion)[^1,2]. The document is the first audited disclosure the firm has ever published. It shows FY2024 revenue of RMB 24.18 billion[^1], a 9M 2025 run-rate of RMB 32.08 billion (+97.79% YoY)[^1], a Q3 2025 comprehensive gross margin of 35.00%[^1], cumulative net losses of RMB 40.86 billion through H1 2025[^1], 15,300 employees[^1] (30.41% in R&D[^1]), and a customer list that reads Alibaba, ByteDance, Tencent, Lenovo, Xiaomi, Transsion, Honor, OPPO, vivo[^1]. It explains why the world's most concentrated industry — three Korean and one American firm controlling 93.4% of global DRAM revenue[^91] — is being repriced from the bottom up.
stats:
- {label: "FY2024 revenue",      value: "RMB 24.18B",  note: "+166% YoY[^1]"}
- {label: "9M 2025 revenue",     value: "RMB 32.08B",  note: "+97.79% YoY[^1]"}
- {label: "Q3 2025 gross margin", value: "35.0%",      note: "from −3.67% in FY22[^1]"}
- {label: "Headcount (H1 2025)", value: "15,300",      note: "30.41% R&D[^1]"}
- {label: "Cumulative net loss", value: "RMB 40.86B",  note: "through H1 2025[^1]"}
- {label: "IPO raise (target)",  value: "~US$4.2B",    note: "STAR Market, Dec 2025[^1,2]"}
- {label: "DRAM WPM (end-2025)", value: "~290k",       note: "from 20k in 2019[^15,45,11]"}
- {label: "Global DRAM share Q3 25", value: "~5%",     note: "revenue basis[^19]; ~10–15% on bits[^16,64]"}
---

The thesis of this report is that three facts about CXMT — its cost stack, its customer base, and its place inside the export-control regime — have become measurable for the first time, and together they explain the 2025–2026 memory cycle better than any single narrative on either side of the policy debate. The bear story (CXMT is propped-up, sub-scale, and behind by five years) and the bull story (CXMT is the next SK Hynix on a five-year delay) both have to contend with a single new artifact: an audited Chinese prospectus showing a firm that has run an RMB 40.86B cumulative loss[^1] while building a 15,300-person, 290,000-wafer-per-month operation that just posted a 35% gross margin in one quarter[^1,15] — and now sells DRAM into the same hyperscaler accounts Korean and American producers depend on[^1,52].

## 01. Origin — Project 506, a German IP archive, and a chairman with two jobs

CXMT was launched in May 2016 as Hefei's "Project 506," the city's contribution to the "Made in China 2025" plan to fill the missing DRAM layer of China's chip stack[^8,44]. The original capital pool was a Hefei municipal commitment of RMB 14.4 billion plus a RMB 3.6 billion equity contribution from GigaDevice Semiconductor, the Shanghai-listed NOR/eMMC designer whose founder Zhu Yiming would also chair CXMT[^44,75]. The dual-chair structure is unique in the Chinese memory ecosystem: GigaDevice is both an equity holder and a major commercial customer for CXMT's DDR3/4 niche dies, giving CXMT a built-in demand floor that YMTC, on the NAND side, lacks[^75]. Three wholly-owned project vehicles were spun up in late 2017 — CXMT itself, Hefei ChangXin, and "Innotron Memory" — and rebranded under the CXMT name in 2019[^8].

The technology came from a different continent. In November 2019, Polaris Innovations Limited — the WiLAN/Quarterhill subsidiary that had bought the former German DRAM maker Qimonda's patent portfolio from Infineon in 2015 — signed a patent license and acquisition agreement with CXMT covering Qimonda's DRAM IP[^9]. Qimonda had been Europe's flagship DRAM firm until its 2009 bankruptcy; many of its engineers had moved to Inotera in Taiwan, where Liu Liming would later be poached to advise CXMT[^8]. The Qimonda archive gave CXMT a freedom-to-operate base for the trench-cell technology that underlies its current DDR4 line.

:::timeline
- {date: "2016-05",    headline: "Project 506 launches",            body: "Hefei municipal government commits RMB 14.4B + GigaDevice RMB 3.6B equity."}
- {date: "2017-07",    headline: "Fab 1 ground-breaking",          body: "$7.2B announced project; 125k wpm design; 65,000 m² cleanroom."}
- {date: "2019-11",    headline: "Qimonda patent license",         body: "WiLAN/Polaris–CXMT agreement on former Qimonda DRAM patents."}
- {date: "2019-12",    headline: "First DDR4 commercial production", body: "Fab 1 starts at ~20k wpm."}
- {date: "2023-10",    headline: "Big Fund II injects ¥14.5B",      body: "33.14% of ChangXin Xinqiao (DDR5 fab vehicle)."}
- {date: "2024-08",    headline: "HBM2 mass production claimed",   body: "TrendForce reports CXMT begins HBM2 ramp, ~2 years ahead of telegraphed."}
- {date: "2024-12-02", headline: "BIS Dec 2 rule — CXMT carve-out", body: "140 Chinese entities added to Entity List; CXMT removed from draft after Japan/TEL pressure."}
- {date: "2025-12-26", headline: "Samsung trade-secret indictments", body: "Seoul prosecutors charge 10 (5 ex-Samsung + 5 CXMT) with leaking 10nm DRAM tech."}
- {date: "2025-12-30", headline: "SSE prospectus filed",            body: "RMB 29.5B raise; first audited financial disclosure ever."}
- {date: "2026-01-15", headline: "Trump BIS rule (H200/MI325X)",    body: "Reports of fresh Entity List package including CXMT being drafted."}
:::

The cap table the prospectus discloses is a Hefei consortium with no controlling shareholder: Hefei Qinghui Jidian (a municipal LP) 21.67%, Changxin Integration 11.71%, National IC Industry Investment Fund Phase II ("Big Fund II") 8.73%, Hefei Jixian 8.37%, Anhui Province Investment 7.91%[^104]. Aggregated, Hefei municipal SOEs + Anhui Province + Big Fund II together hold more than 38% directly[^104], and because Hefei vehicles also control Qinghui Jidian and Changxin Integration, the effective state stake is materially higher than the headline. Big Fund Phase III, launched May 24, 2024 with RMB 344 billion (~US$47.5 billion) of paid capital across 19 shareholders[^40], has not yet been disclosed as a direct listco shareholder — its early deployments have skewed to equipment and HBM supply chain, not the IDM. The counterpoint to "this is just state capital": CXMT also raised RMB 10.8 billion in a March 2024 commercial round at an implied valuation of RMB 150.8 billion (~US$21 billion)[^3], and GigaDevice — a separately listed company answering to public shareholders — contributed RMB 1.5 billion of it[^3]. Why this matters: CXMT is now structurally too large to fail and too widely owned to back-door consolidate, which forecloses Beijing's prior tactic of folding losing chip projects into stronger SOEs.

## 02. The prospectus — first numbers in nine years

The December 30 2025 prospectus closes the most expensive information asymmetry in semiconductors. Until that filing, every CXMT estimate in print — capacity, yield, market share, margin — was an analyst guess. The audited figures change the analytic frame in three ways.

First, growth is real and accelerating. Revenue moved from RMB 8.29B (FY2022) to RMB 9.09B (FY2023) to RMB 24.18B (FY2024) and a nine-month 2025 print of RMB 32.08B (+97.79% YoY); Q3 2025 alone ran RMB 16.65B (+148.80% YoY)[^1]. Full-year 2025 guidance is RMB 55–58 billion with a first-ever annual net profit of RMB 2.0–3.5 billion[^1]. The H1 2026 outlook the firm filed with the exchange — RMB 110–120 billion of revenue and RMB 66–75 billion of net profit[^100] — would, if hit, make CXMT a $30B+ annualized DRAM business inside a year of the IPO filing.

:::line-chart(title="CXMT annual revenue, RMB billion (compiled from SSE prospectus)", subtitle="9M 2025 = 32.08B (+97.79% YoY); Q3 25 alone 16.65B (+148.80% YoY)", y-unit="RMB B")
x: 2022,2023,2024,9M-2025
CXMT-revenue: 8.29,9.09,24.18,32.08
:::

Second, margins inverted. Main-business gross margin moved from −3.67% (FY22) → −2.19% (FY23) → +5.00% (FY24) → +12.72% (H1 25) → 35.00% comprehensive in Q3 25[^1]. The DDR4 and LPDDR4X lines were sold at gross margins of −108.76% and −121.62% respectively in 2024[^28] — explicit dumping for share[^20] — before the firm wound them down and pivoted to DDR5/LPDDR5/5X. The Q3 25 gross margin of 35% is a credit to the AI-driven DRAM supercycle as much as to CXMT execution: SK hynix posted a 72% operating margin in 1Q26[^69] and Samsung's DS division printed a 65.7% operating margin in the same quarter[^67]. The interesting fact is not that CXMT closed the gap — it didn't — but that it cleared the loss-line at all.

:::stats
- {label: "GM FY22",        value: "−3.67%",  note: "main-business[^1]"}
- {label: "GM FY23",        value: "−2.19%",  note: "main-business[^1]"}
- {label: "GM FY24",        value: "+5.00%",  note: "main-business[^1]"}
- {label: "GM H1 25",       value: "+12.72%", note: "main-business[^1]"}
- {label: "GM Q3 25",       value: "+35.00%", note: "comprehensive[^1]"}
- {label: "SK Hynix Q1 26", value: "+72%",    note: "op. margin[^69]"}
:::

Third, structure. R&D was 33.11% of cumulative revenue across 2022–H1 2025 (RMB 18.87B)[^1] — far above the 5% threshold STAR Market sets for "technology" firms — though intensity is falling as revenue scales (51% in 2022, 24% in H1 2025[^1]). Headcount rose from 8,303 (2022) to 15,300 (H1 25); 4,653 (30.41%) are R&D personnel and 74.90% hold a bachelor's or higher[^1]. Customer concentration is high but easing: top-5 share fell from 74.12% (FY23) to 59.99% (H1 25)[^1]. Total assets at 30 Sep 2025 were RMB 302.87B against RMB 172.80B of liabilities (57.65% debt-to-asset)[^1]; cumulative accumulated losses were RMB 40.86B at June 30 2025[^1] and roughly RMB 46.8B by Sep 30 2025 once H2 25 losses are added[^1]. Product mix is exclusively commodity DRAM: LPDDR 69.74% of main-business revenue in H1 25, DDR series 27.82%[^1]. ==There is no HBM revenue disclosed as commercial — the prospectus treats HBM strictly as a forward-looking R&D direction[^1].==

The geographic mix flipped sharply in H1 2025. From a 14%/86% domestic/overseas split in FY22 (overseas is almost entirely Hong Kong-booked sales for USD settlement), the H1 25 number is 63%/37%[^1] — customers re-booking via mainland entities "for financing convenience and security," per the prospectus[^1]. Read carefully: this is not a loss of overseas demand; it is a settlement-currency shift after the December 2024 export-control package made USD-denominated semiconductor flows from China more politically conspicuous. The substantive customer list remains predominantly Chinese.

:::donut(center-label="H1 2025 mix")
- {label: "LPDDR series", value: 69.74}
- {label: "DDR series",   value: 27.82}
- {label: "Other",        value: 2.44}
:::

## 03. Capacity — the 14× ramp that triggered the cycle

CXMT's wafer starts went from ~20,000 per month at the December 2019 production start[^8] to ~100,000 in early 2024[^12], ~200,000 in Q1 2025[^12], and a reported plateau of ~240,000–290,000 by year-end 2025[^15,45]. UBS estimates Chinese memory capacity will add another 120,000–140,000 wafers monthly across 2026 across CXMT, YMTC, and Wuhan Xinxin[^45]. This is the single most important number in the report: it is the mechanism behind the 2024 DDR4 price collapse, the 2025 Korean DDR4 exit, and the 2026 DRAM shortage all at once.

:::line-chart(title="CXMT DRAM wafer starts per month, 2019–2026E", subtitle="TrendForce / Digitimes / UBS analyst estimates", y-unit="k wpm")
x: 2019-12,2020-12,2022-12,2024-Q1,2025-Q1,2025-Q4,2026E
CXMT-WPM: 20,40,70,100,200,290,300
:::

Three fabs feed the output. Hefei Fab 1 ("Fab 1") was completed in mid-2017 under a $7.2 billion announced project budget for a 125,000-wafer/month, 12-inch design with a 65,000 m² cleanroom, and entered commercial production in December 2019[^8]. Hefei Fab 2, operated by the Changxin Xinqiao vehicle into which Big Fund II injected RMB 14.5 billion (33.14% stake) in October 2023[^41], is the DDR5/advanced-node ramp site. A Beijing fab adds R&D plus pilot-line capacity. The next mega-fab — in Shanghai — is sized at two to three times the Hefei base; equipment installation is planned for the second half of 2026, with volume production starting in 2027[^13].

How big is this in global context? Samsung runs roughly 730,000 12-inch DRAM WPM, SK Hynix ~480,000, Micron ~400,000 per SemiAnalysis's wafer-fab model[^16] — call it ~1.6 million WPM for the Big 3. CXMT's 290,000 WPM is now 50% of SK Hynix and 33% of Samsung[^15], placing it as the world's #4 DRAM producer by capacity well ahead of the Taiwanese tier (Nanya, Winbond, Powerchip). On a bit-share basis, CXMT lags its wafer share because its current G4 16nm die is roughly 40% larger than Samsung's 1a/1b 14nm equivalent for 16Gb DDR5[^4,63,64] — so the same wafer yields fewer good bits. SemiAnalysis estimates CXMT at ~15% of global DRAM bit share by end of 2026[^16], rising toward 490k WPM by 2030 in their model.

:::rank-list
- {label: "Samsung",                       value: "~730k WPM", pct: 100}
- {label: "SK Hynix",                      value: "~480k WPM", pct: 66}
- {label: "Micron",                        value: "~400k WPM", pct: 55}
- {label: "CXMT",                          value: "~290k WPM", pct: 40, highlight: true}
- {label: "Nanya, Winbond, PSMC (combined)", value: "~125k WPM", pct: 17}
:::

The counterargument: wafer-starts are an input metric. Effective bit output is constrained by yield. The TrendForce/Citi claim that CXMT hit 80% DDR5 yield by late 2024[^6] is disputed by Korean industry sources telling Business Korea that real DDR5 yield was 10–20% at the same time[^7] — and TechInsights' April 2025 teardown of a Gloway DDR5-6000 UDIMM kit with 16 CXMT 16Gb DDR5 chips suggests the production exists at saleable yield even if the absolute number is contested[^4]. The honest synthesis: CXMT has saleable yield on a G4 die that is structurally larger than Korean equivalents, and the size penalty is permanent unless DUV multi-patterning can be pushed to a node where the cost-of-extra-passes exceeds the cost of an EUV scanner CXMT does not have.

## 04. The DDR4 reversal — a Chinese fab triggered the biggest DRAM spike ever recorded

The 2025–2026 DRAM cycle is the most violent ever measured, and CXMT is the proximate cause of both the bottom and the top. The chronology is unusually clean.

Through 2024, CXMT's expanding DDR4 line crushed legacy prices. Chinese DDR4 was selling at roughly half the price of South Korean equivalent product[^20], and new chips were trading 5% below second-hand reballed memory[^20]. Micron's December 2024 prepared remarks called it out by silhouette: "Consistent with analyst reports, we have seen an increase in bit supply at legacy technology nodes from a China-based DRAM and a China-based NAND supplier… Competition from China supply is focused on China market demand — in DRAM with DDR4 and LP4 products"[^17].

SK Hynix announced a step-down of DDR4's share of its DRAM mix from 40% in June 2024 to 30% in September 2024 to a planned 20% by year-end[^11], shifting wafers to 1a-node and HBM. Samsung and Micron followed with near-simultaneous DDR4 end-of-life dates: Samsung stops orders June 2025 and ships through mid-Dec 2025; Micron stops shipping Q1 2026; SK Hynix stops orders October 2025 and ships through April 2026[^46]. CXMT itself then phased out DDR4 and pivoted capacity to DDR5/LPDDR5/5X — DDR5 was projected to exceed 60% of CXMT output by year-end 2025[^23].

With four producers simultaneously exiting DDR4, prices inverted. In July 2025, 8GB DDR4 modules traded above 8GB DDR5 modules — the first such crossover in DRAM generations since DDR2 to DDR3[^46]. TrendForce's 3Q25 consumer DDR4 contract price forecast was revised to +85–90% QoQ, the steepest single-quarter DDR4 jump on record, with LPDDR4X up 38–43% QoQ[^47]. By 1Q26, the supercycle had broadened to all DRAM: TrendForce raised the conventional DRAM contract price forecast to +90–95% QoQ, with PC DRAM above +100% QoQ — the largest single-quarter DRAM price surge ever recorded[^48]. Samsung's response was to reallocate ~80,000 DRAM wafers/month from HBM to DDR5 RDIMM in Q4 2025 to capture the AI server contract spike[^49] — visible empirical evidence that the cycle, not yield discipline, now sets the wafer allocation.

:::timeline
- {date: "2024-12", headline: "Chinese DDR4 ≈ −50% vs Korea",      body: "CXMT new chips priced 5% below second-hand reballed memory."}
- {date: "2025-Q1", headline: "Korea exits DDR4",                  body: "SK Hynix mix 40%→20%; Samsung/Micron set EOLs."}
- {date: "2025-Q3", headline: "CXMT pivots to DDR5",               body: "DDR5 >60% of CXMT output by year-end."}
- {date: "2025-07", headline: "DDR4 > DDR5 inversion",             body: "8GB DDR4 modules trade above 8GB DDR5 — first since DDR2/3."}
- {date: "2025-Q3", headline: "+85–90% QoQ DDR4",                  body: "TrendForce: steepest DDR4 jump on record."}
- {date: "2026-Q1", headline: "+90–95% QoQ conventional DRAM",     body: "PC DRAM >+100% QoQ — largest DRAM spike ever."}
:::

The memory cycle is a direct read on these moves through the public equities. From the June 2024 start to the May 2026 print, Micron is up ~5.5×, SK Hynix ~7.7×, Samsung ~3.3× per Yahoo Finance monthly close[^106] — concentrated in the post-July 2025 inversion window.

:::line-chart(title="Memory chipmaker prices, indexed and absolute (Yahoo Finance, monthly close)", subtitle="June 2024 = base; chart shows raw price progression", y-unit=$)
x: 2024-06,2024-09,2024-12,2025-03,2025-06,2025-09,2025-12,2026-03,2026-05
MU: 131.53,103.71,84.16,86.89,123.25,167.32,285.41,337.84,724.66
:::

Why this matters: cycle theory said memory was structurally cyclical because supply takes 18+ months to add and demand can shift in a quarter. CXMT compressed the cycle by being the only player with both excess capacity at legacy nodes and policy cover to keep running them sub-cost — then by abruptly redirecting that capacity. ==The cycle now lasts as long as Beijing's industrial-policy attention span, not as long as a Samsung capex committee's planning horizon.==

## 05. HBM — the gap that still matters

DDR5 the firm can ramp. HBM the firm cannot — yet. The HBM stack is the binding constraint on whether China can train competitive frontier AI models on Huawei silicon, and CXMT is the only domestic firm with a credible chance of supplying it. The prospectus discloses zero HBM revenue[^1]; the public-record HBM trajectory is samples and pilot lines.

SK Hynix began volume production of the world's first 12-layer HBM3E with 36GB capacity and 9.6 Gbps per pin in September 2024[^31]. Samsung's HBM3E is shipping in volume to multiple AI accelerator customers; both Korean producers are sampling 16-Hi HBM4. CXMT's reported HBM sample speed at end-2025 was 4.4 Gbps, with a 5.2 Gbps year-end target[^38] — roughly half the SK Hynix HBM3E spec. TrendForce reported CXMT began HBM2 mass production in August 2024[^32]; Morgan Stanley reframed this as sampling with small-scale production targeted for mid-2025[^101]. Digitimes reports that CXMT plans to begin HBM3 mass production in 2026 using mass reflow molded underfill (MR-MUF) packaging — the same process SK Hynix uses[^88] — and has shipped 16nm HBM3 samples to Huawei for the Ascend 920 launch[^96]. Counterpoint's leaked yield figure for CXMT HBM3 in 2025–2026 was 10–20%[^37], versus the 70%+ SK Hynix reportedly achieves on HBM3E.

:::compare
- {role: LOWEST,  name: "CXMT HBM (end-25 sample)", value: "4.4 Gbps/pin"}
- {role: HIGHEST, name: "SK Hynix HBM3E 12-Hi",     value: "9.6 Gbps/pin"}
- {role: SUBJECT, name: "CXMT HBM3 2026 target",    value: "~6.4 Gbps/pin"}
:::

The single hardest data point for the bull case is from a TechInsights teardown reported by Bloomberg on October 3, 2025: Huawei Ascend 910C samples contained HBM2E from Samsung and SK Hynix — not CXMT[^97,35]. Huawei, the customer most aggressively willing to take performance and ramp risk to use domestic HBM, has chosen Korean HBM stockpile over CXMT samples in the production silicon as of late 2025. SemiAnalysis estimates CXMT will be able to make ~2 million HBM stacks in 2026, enough for only 250,000–300,000 Ascend 910C packages[^34] — well below the ~1.6 million packages Huawei could fabricate from its Samsung/SK Hynix HBM stockpile.

:::quote(attr="SemiAnalysis, April 2025")
We believe CXMT will only be able to make ~2 million stacks of HBM next year, which is only sufficient for 250,000–300,000 Ascend 910C's… Without access to more foreign HBM, Huawei will not be able to fabricate even 1 million Huawei Ascend chips next year.
:::

What would close the gap: CXMT and Tongfu Microelectronics (world's #3 OSAT) plus JCET are co-developing advanced packaging for HBM[^76]. Wuhan Xinxin — YMTC's foundry subsidiary — released a March 2024 tender for a dedicated HBM packaging fab targeting 3,000 12-inch wafers/month using hybrid-bonding IP from YMTC's 3D NAND work, with first output targeted for 2026[^105]. Tongfu announced an RMB 4.4 billion private placement in January 2026 explicitly to expand memory packaging capacity[^76]. The Chinese stack is being assembled — Tongfu and JCET on backend, Naura/Maxwell/U-Precision on assembly equipment[^36], CXMT on the core die — but it is roughly three years behind SK Hynix on stack height, two on per-pin speed, and a half-generation behind on TSV yield. ==An HBM gap of three years in a market growing 2× per year is not the same as a DRAM gap of three years.==

## 06. The export-control workaround — why CXMT isn't (yet) on the Entity List

The most striking fact about the Dec 2 2024 BIS package is what wasn't in it. The rule added 140 Chinese entities to the Entity List[^24,26], including upstream lithography vendors and Huawei-adjacent fabs. CXMT was on the original draft list of ~12 Huawei-network additions; BIS removed it in the final, reportedly after Japanese government pressure on behalf of Tokyo Electron, whose CXMT exposure runs through etch and litho-track tools[^25]. Instead of naming CXMT, BIS designed three indirect constraints in the companion Interim Final Rule[^27]:

:::kv
- {term: "ECCN 3A090.c",          def: "Controls HBM with memory bandwidth density > 2 GB/s/mm² to D:5 destinations. License exception only for items < 3.3 GB/s/mm² and only for US- or A:5-headquartered exporters."}
- {term: "DRAM threshold (new)",  def: "Advanced-node DRAM is now defined by memory cell area < 0.0019 µm² or memory density > 0.288 Gb/mm² — a metric-based test capturing CXMT's leading-edge DDR5/HBM lines without naming the firm."}
- {term: "SME FDPR",              def: "Foreign-produced direct product rule on 24 SME types + 3 software tools — captures TEL/ASML/Lam shipments to Chinese fabs even if no US component is in the tool."}
- {term: "FN5 Entity List FDPR",  def: "Footnote-5 designation on 16 specific Entity List firms triggers US jurisdiction on foreign-produced SME purchases. CXMT not among the 16."}
:::

The carve-out drew immediate fire on the Hill. House Select Committee on the CCP Chairman John Moolenaar wrote to Commerce Secretary Raimondo on December 4, 2024:

:::quote(attr="Rep. John Moolenaar, Chairman, House Select Committee on the CCP")
BIS has taken no action against ChangXin Memory Technologies (CXMT) which is poised to become a leader in the very same HBM technology BIS just export controlled… There is no national security justification for these loopholes.
:::

The bet BIS was making — that the SME FDPR plus the metric-based DRAM definition could constrain CXMT without listing it — looks weak ex-post. Rhodium Group concluded in December 2024 that CXMT had stockpiled enough semiconductor manufacturing equipment in 2H 2024 to plausibly sustain operations through 2026 or 2027[^30]; the firm's DRAM wafer capacity then tripled from ~100k WPM (early 2024) to ~290k WPM (end-2024)[^11,15]. The Trump administration reportedly drafted a fresh Entity List package including CXMT in January 2026, alongside a January 15 2026 BIS rule allowing H200/MI325X sales to China for a 25% US-government fee[^84] — a contradictory posture rather than a coherent doctrine.

The Tokyo Electron exposure that drove the original carve-out is itself moving. TEL's China revenue share fell from 42% (FY24) to ~35% (FY25) and was 38.6% in Q1 FY26[^81]; AMAT's China revenue fell from 37% (FY24 systems) to 28% (FY25) to 25% in Q4 FY25, with $600–710M of FY26 revenue at risk from the December 2024 rule[^62]; ASML's China share fell from 41% of system sales in 2024 to a guided ~20% in 2026[^82,57]. The political ground under the carve-out is shrinking on its own.

:::stack-rows
categories: ["China share peak", "Current China share", "China share guided 2026"]
rows:
  - {label: "ASML (systems)", values: [41, 33, 20]}
  - {label: "AMAT (systems)", values: [37, 28, 25]}
  - {label: "TEL",            values: [47, 35, 30]}
:::

The metric-based DRAM definition is the more elegant control. BIS chose cell area < 0.0019 µm² and density > 0.288 Gb/mm²[^28] precisely because CXMT's current G4 die (66.99 mm² / 0.239 Gb/mm² / ~16nm linewidth[^4]) sits just outside the threshold. The next CXMT node — G5 ~15nm, with R&D completion targeted late 2025 and mass production late 2026[^5] — will not. This is a designed slow-walk: keep CXMT's current capacity legal under existing tooling, choke off the next node. The bet is that DUV multi-patterning at sub-15nm becomes expensive enough that the policy choke binds before market forces push CXMT to G5 anyway.

## 07. The cost stack — why a 30% gross margin still works

The most quoted single number about CXMT is the price discount. A 32GB DDR5-5600 kit with CXMT chips has been seen at retail around $138, versus $180–210 for comparable kits from SK Hynix or Micron[^68] — a 26–35% server-SKU discount. On commodity DDR4 in early 2025 the discount was reported at ~50% to Korean equivalents[^20]. The interesting question is how CXMT books a 35% Q3 2025 gross margin while running that discount, while SK Hynix runs a 72% operating margin in the next quarter on the same product family[^69].

The bottom-up answer is that CXMT's wafer cost is structurally 30–50% higher than Samsung's at the same node, but state capital and depreciation policy absorb the gap.

:::stats
- {label: "CXMT G4 16Gb DDR5 die",    value: "66.99 mm²", note: "0.239 Gb/mm²[^4]"}
- {label: "Samsung 1a/1b 16Gb (est)", value: "~48 mm²",   note: "~40% smaller[^64]"}
- {label: "Die-area penalty",         value: "~40%",      note: "fewer good die per wafer[^64]"}
- {label: "DUV passes per layer",     value: "2–4",       note: "vs single-pass EUV[^65]"}
- {label: "CXMT FY24 depreciation",   value: "~RMB 15B",  note: "larger than NI[^66]"}
- {label: "CXMT vs SK Hynix margin",  value: "35% / 72%", note: "GM vs op. margin[^1,69]"}
:::

The die-area penalty is the structural reality: CXMT's 16Gb DDR5 die measures 66.99 mm² at G4 (~16nm linewidth)[^4], versus an estimated ~48 mm² for Samsung's 1a/1b 14nm equivalent — about 40% larger[^64]. That maps directly to ~40% fewer good die per wafer at the same yield, plus a meaningful share-of-wafer overhead penalty. DUV multi-patterning splits critical layers into 2–4 exposure passes versus a single EUV exposure, adding process steps, accumulating overlay error, and raising both wafer cost and yield risk[^65]. Industry estimates put the CXMT wafer cost premium at 30–50% above Korean equivalents on a like-for-like basis[^65,87].

The cost absorbers are five-fold:
1. State equity. The prospectus implies more than RMB 130 billion in owners' equity[^1] against cumulative state and strategic injections through 2024–25 estimated at $5–10B+[^93], plus Big Fund II's separate RMB 14.5B into ChangXin Xinqiao[^41]. The capex burden does not bear an equity-cost-of-capital line.
2. Land and power. Hefei municipal contributions to Project 506 included land grants and cleanroom construction[^44].
3. Tax. State Council Guofa [2020] No. 8 grants a 10-year corporate income tax holiday to IC firms operating at ≤28nm with ≥15 years of operation; CXMT qualifies in principle[^42] (the 15-year clock binds the start date).
4. Depreciation. CXMT booked ~RMB 15B of fixed-asset depreciation in 2024 and RMB 11B in H1 2025[^66] — the depreciation drag is larger than reported net income at the firm's current scale. ==unverified: CXMT useful-life assumptions on production equipment appear longer than the 5-year norm Samsung and SK Hynix use, which would inflate reported margins; the prospectus does not state the policy explicitly.==
5. Subsidized cost of capital. State-backed debt and equity allow CXMT to operate cash-flow positive at a price point that would drive a Western-cost-stack operator to negative GAAP margin.

Add it up and the picture is a firm that cannot match Samsung on cost-per-bit at the leading edge — won't for years, possibly ever, without EUV — but can clear the GAAP loss-line at a 35% discount to Korean pricing because state capital socializes the wafer-cost gap and a young depreciation book amortizes the capex one quarter at a time. Bull and bear both have to live with this fact.

## 08. The customer base — domestic-first, hyperscaler-hesitant

The prospectus discloses the customer list directly: Alibaba Cloud, ByteDance, Tencent, Lenovo, Xiaomi, Transsion, Honor, OPPO, and vivo[^1] — reached primarily through distributors[^1]. Top-5 concentration ran 69.43% (FY22) / 74.12% (FY23) / 67.30% (FY24) / 59.99% (H1 25)[^1], with new top-5 entrants Customer C (11.45%) and Customer D (10.95%) added in H1 25[^1]. CXMT now holds roughly 30% of China's domestic smartphone LPDDR market by Caixin's November 2025 estimate[^52]. The closest thing to a flagship Tier-1 PC OEM design-win outside the server channel is the Lenovo ThinkBook 14+/16+ 2026, which reportedly ships 32GB LPCAMM2 modules built from CXMT LPDDR5X at 8,533 MT/s[^54].

:::stack-rows
categories: ["Domestic (mainland)", "Overseas (mostly HK-booked)"]
rows:
  - {label: "FY 2022", values: [14, 86]}
  - {label: "FY 2023", values: [20, 80]}
  - {label: "FY 2024", values: [29, 71]}
  - {label: "H1 2025", values: [63, 37]}
:::

The hyperscaler-hesitancy is in the customer list itself: no Western Tier-1 hyperscaler is named, and no Tier-1 server OEM outside China. The two visible blockers are quality and geopolitics. On quality, early CXMT DDR5 samples in 2025 reportedly failed reliability tests at ~60 °C and at sub-zero temperatures, with yield "hovering just above 50%"[^103] — situation improved through H2 2025 but remains analyst-track, not Tier-1-CSP audit. On geopolitics, CXMT supplying memory to a hyperscaler that also has US government customers creates a Section 1260H "Chinese Military Companies" risk-vector that no responsible procurement team will accept without further policy clarity (CXMT was added to the DoD Section 1260H list on January 7, 2025[^30]). The hyperscaler channel is closed by structural design.

The flagship customer that ought to be CXMT's largest is Huawei, and the picture there is split. CXMT supplied LPDDR5 launch-customer designs to Xiaomi and Transsion in November 2023[^51]; the Huawei Mate 70 Pro and Pro Plus, by contrast, were teardown-confirmed in December 2024 as using SK Hynix 12 GB / 16 GB LPDDR built on 14nm EUV technology — not CXMT[^50]. CXMT has shipped 16nm HBM3 samples to Huawei[^96] but the production-silicon Ascend 910C as of October 2025 still used Samsung/SK Hynix HBM2E[^97]. Huawei's revealed preference at the flagship tier is for Korean memory; CXMT's design-wins concentrate in the secondary tier of Huawei's portfolio. ==China's own AI champion has not yet been able to design its production-volume accelerator around CXMT HBM.==

## 09. The geopolitical thread — Korean GDP, hyperscaler bills, allied tooling

A credible #4 in DRAM repositions four constituencies simultaneously.

Korea. Semiconductors were 20.8% of total Korean exports in 2024 (USD 141.9B[^78]). Samsung + SK Hynix DRAM revenue alone is forecast near $96B in 2025 — SK Hynix $49.6B vs Samsung $46.4B[^78]. Korea's Q1 2026 GDP grew 1.7% QoQ, the fastest in five and a half years, with the semiconductor manufacturing sector accounting for "nearly half" of that growth per Bank of Korea preliminary data[^77]. The Korean economy is structurally levered to the memory cycle, which is now structurally levered to a Chinese firm.

Hyperscaler bills. Server memory prices are tracking to double from early 2025 to end-2026[^79]; memory's share of AI server BOM was 10–25% pre-spike and is materially higher now[^79]. Microsoft, Amazon, Google, Meta, and Oracle pass these costs into model inference pricing, which the API-buying community sees as the model-pricing tightening of 2026. CXMT's domestic-only customer roster has the perverse external effect of making Korean and US-supplied bits scarcer at the margin.

Allied tooling. ASML China system-sales share peaked at 41% in 2024[^57], normalized to ~33% in 2025, and is guided to ~20% in 2026 by CEO Christophe Fouquet[^82]. AMAT, KLA, and Lam are tracking similar trajectories[^62]. NAURA, China's homegrown etch leader, won a ~$380M order from CXMT for 45 Primo nD dry etchers in November 2025 — the largest single domestic-WFE contract in China to date[^60]. AMEC's FY2024 revenue jumped to RMB 9.07B (+45% YoY), with etch alone +54.7%[^61]. The cost of the US/Dutch/Japanese tooling regime is now legible: Western SME vendors lose 15+ percentage points of revenue exposure, Chinese SME vendors take it.

:::rank-list
- {label: "Nanya (Taiwan, +84% QoQ Q3 25)",    value: "$627M", pct: 100, highlight: true}
- {label: "Winbond (Taiwan, +21.4% QoQ Q3 25)", value: "$222M", pct: 35}
- {label: "Powerchip DRAM (Taiwan, +62.8%)",   value: "$33M",  pct: 5}
:::

Taiwan. The Taiwanese DRAM tier (Nanya, Winbond, Powerchip) is the immediate beneficiary of the Korean DDR4 exit, posting 21–84% QoQ Q3 2025 revenue jumps[^83] — but faces the same node-class compression once CXMT DDR5 ramps in volume. The squeeze is structural: same node, smaller customer book, no equivalent state capital floor.

US response. The Biden administration's late-2024 package was designed around metric-based controls; the Trump administration of early 2026 is reportedly drafting a fresh Entity List package including CXMT while simultaneously authorizing H200/MI325X sales to China for a 25% US-government fee[^84]. Both moves shift the policy question from "containment of advanced compute in China" to "extraction of rent from advanced compute flows to China" — a different doctrine. SK Hynix's $3.87B 2.5D HBM packaging fab in West Lafayette, Indiana, targeting 2H 2028 mass production with a $458M CHIPS Act grant[^80], is the Korean industry's hedge against being caught between US controls and Korean political pressure to keep HBM at home.

## 10. What could break the thesis — bear case

Each section above contains its own counterpoint. Stitched together, the bear case is harder than the bull-side coverage of CXMT usually admits.

1. The "3 years behind" framing flatters CXMT. SK Hynix's industry-first 1c (~10nm-class) DDR5 was announced in August 2024[^73]; CXMT's G4 (~16nm) entered teardown evidence in early 2025[^4] and was Samsung's 2018–2019 generation. On a pure node-vintage basis the gap is closer to five or six years. The "3 years" headline is a function of CXMT's commercial DDR5 (~17–16nm) landing within ~3 years of Korean equivalent-class DDR5 (1z, ~14–15nm) — apples-to-apples on commodity DRAM but masks the leading-edge gap.

2. The 80% DDR5 yield is contested. Korean primary press (Business Korea, December 2024) pegged real CXMT DDR5 yield at 10–20% in late 2024[^7] — disputed by the TrendForce/Citi 80% number from the same window[^6]. Independent teardown evidence confirms saleable yield exists[^4]; absolute yield is unresolvable from open sources.

3. HBM is sample volume. The single hardest data point: Huawei Ascend 910C samples used Samsung/SK Hynix HBM2E in production silicon as of October 2025 per TechInsights, not CXMT[^97]. The bull narrative ("CXMT ships HBM3 to Huawei") is true at sample volume and untrue at production volume — and the gap is the binding constraint on Chinese AI compute scale.

4. IP litigation. South Korean prosecutors indicted 10 individuals — five former Samsung executives and five CXMT employees — for leaking Samsung's 10nm-class DRAM process technology to CXMT; SCMP dates the announcement to December 26, 2025[^56], while the Tom's Hardware report was filed December 23[^55]. A former Samsung researcher received a 7-year prison sentence. Samsung estimated 5 trillion won (~$3.7B) of damages in 2024 alone[^55]. ITC and civil follow-on suits remain plausible. The bull case assumes this stays a Korean criminal matter; the bear case is that Samsung extracts a settlement, royalty, or injunctive remedy that compresses CXMT's margin.

5. Cumulative losses despite a supercycle. The prospectus shows CXMT booked RMB 40.86B of cumulative net losses through 9M 2025[^1] — including RMB 5.98B in the first nine months of 2025 despite the AI-driven DRAM price spike. State backing is real and durable, but the bear read is: if a Korean-class supercycle cannot produce sustained GAAP profit at this scale, the structural cost gap may be wider than the marketing numbers suggest.

6. Equipment access tightens. BIS's metric-based DRAM definition is designed to catch G5 (~15nm) and below[^28]. The Trump administration's reported fresh Entity List package would name CXMT explicitly[^84]. If both fire, CXMT's next-node trajectory compresses or requires a 2–3 year homegrown SME replacement curve via NAURA/AMEC[^60,61] — feasible at G4, very hard at G5/G6.

7. Domestic competition splits capital. YMTC has allocated 50% of its Phase 3 fab to DRAM and is partnering with Wuhan Xinxin on HBM via hybrid bonding[^72] — splitting Big Fund III talent and tools allocation. The CXMT bull case assumes it remains Beijing's sole DRAM bet; the bear case is that the next round of state capital fragments.

8. The cycle is the cycle. SK Hynix and Samsung have warned shortages could last through 2027[^71], but this assumes AI accelerator demand stays parabolic. CXMT enters peak supply now, when shortage helps it monetize sub-spec capacity at premium prices. The asymmetric risk is a 2027–2028 down-cycle hitting just as CXMT's depreciation book matures and state-capital tolerance for losses tightens.

:::callout(kind=warn, label=Risk)
The single binding question for CXMT through 2027: can the firm cross the HBM3/3E volume bar (≥10–12 Gbps, ≥12-Hi, ≥60% yield) before Huawei's stockpiled Samsung/SK Hynix HBM2E supply runs out? If yes, the bull case has its proof point. If no, China's AI compute scale stays capped at ~250–300k Ascend 910C-class packages per year[^34], and the entire CXMT-as-strategic-asset thesis runs ahead of its underlying enabler.
:::

The honest synthesis. CXMT is real — not Fujian Jinhua, not vaporware. A 15,300-person, RMB 32 billion 9M revenue, 290,000 WPM firm is by any operating measure a Big-4 DRAM producer. But "real" does not mean "competitive at the leading edge." The bull error is to read the prospectus as proof CXMT has closed the gap; the bear error is to read the gap as proof CXMT will not matter. The center of gravity is that CXMT has become the world's lower-bound DRAM price-setter — a role that does not require leading-edge tech but does require sustained state capital and a domestic captive customer base, both of which are now visible on the cap table and the customer list.

:::references
- {id: 1, title: "CXMT (ChangXin Memory) SSE STAR Market prospectus (002170_20251230_B8QS.pdf)", url: "https://static.sse.com.cn/stock/disclosure/announcement/c/202512/002170_20251230_B8QS.pdf", source: "Shanghai Stock Exchange", date: "2025-12-30"}
- {id: 2, title: "China's DRAM giant CXMT plans US$4.2 billion IPO on Shanghai's STAR Market", url: "https://www.scmp.com/news/china-future-tech/semiconductors/article/3338246/chinas-dram-giant-cxmt-plans-us42-billion-ipo-shanghais-star-market", source: SCMP, date: "2025-12-30"}
- {id: 3, title: "Chinese Memory Chipmaker CXMT Starts Listing Preparations", url: "https://www.yicaiglobal.com/news/chinese-memory-chipmaker-cxmt-starts-listing-preparations", source: "Yicai Global", date: "2024-12-12"}
- {id: 4, title: "China Enters 2025 With Big Memory Breakthroughs", url: "https://www.techinsights.com/blog/china-enters-2025-big-memory-breakthroughs", source: TechInsights, date: "2025-02-13"}
- {id: 5, title: "CXMT advances to 16nm DRAM, pushes 15nm", url: "https://www.digitimes.com/news/a20250213VL204/dram-cxmt-16nm-production-development.html", source: Digitimes, date: "2025-02-13"}
- {id: 6, title: "CXMT Reportedly Achieves 80% DDR5 Yield, Targeting 90% by 2025", url: "https://www.trendforce.com/news/2024/12/30/news-chinese-dram-giant-cxmt-reportedly-achieves-80-ddr5-yield-targeting-90-by-2025/", source: TrendForce, date: "2024-12-30"}
- {id: 7, title: "South Korean press challenge CXMT yield claims", url: "https://www.digitimes.com/news/a20241226PD222/cxmt-ddr5-equipment-dram-samsung.html", source: Digitimes, date: "2024-12-26"}
- {id: 8, title: "ChangXin Memory Technologies", url: "https://en.wikipedia.org/wiki/ChangXin_Memory_Technologies", source: Wikipedia, date: "2026-01"}
- {id: 9, title: "WiLAN Subsidiary and CXMT Enter Into License and Acquisition Agreements", url: "https://www.prnewswire.com/news-releases/wilan-subsidiary-and-cxmt-enter-into-license-and-acquisition-agreements-300969655.html", source: PR Newswire, date: "2019-11-22"}
- {id: 10, title: "CXMT IEDM 2023 paper on 4F2 DRAM", url: "https://www.scmp.com/tech/article/3244898/tech-war-china-memory-chip-maker-cxmt-may-have-made-breakthrough-amid-us-sanctions-paper-indicates", source: SCMP, date: "2023-12-15"}
- {id: 11, title: "SK hynix and Samsung Reduce Legacy DRAM Production Like DDR4", url: "https://www.trendforce.com/news/2024/11/05/news-sk-hynix-and-samsung-reportedly-to-reduce-legacy-dram-production-like-ddr4-amid-chinese-competition/", source: TrendForce, date: "2024-11-05"}
- {id: 12, title: "CXMT muscles into DRAM top tier", url: "https://www.digitimes.com/news/a20250421PD218/cxmt-dram-samsung-sk-hynix-2025.html", source: Digitimes, date: "2025-04-21"}
- {id: 13, title: "China's CXMT and YMTC to Massively Expand Memory Output", url: "https://kr-asia.com/chinas-cxmt-and-ymtc-to-massively-expand-memory-output-amid-global-crunch", source: "Nikkei Asia / KrAsia", date: "2026-02-04"}
- {id: 14, title: "China Increases Investment in Domestic Memory Maker to $5.4B", url: "https://www.tomshardware.com/tech-industry/manufacturing/china-increases-investment-in-domestic-memory-maker-to-dollar54-billion-report", source: "Tom's Hardware", date: "2023-10"}
- {id: 15, title: "CXMT Q4 2025 Capacity ~240k Monthly Wafers", url: "https://economy.ac/news/2026/02/202602288024", source: "Economy.ac (Omdia)", date: "2026-02-28"}
- {id: 16, title: "Wafer Fab Model", url: "https://semianalysis.com/wafer-fab-model/", source: SemiAnalysis, date: "2025"}
- {id: 17, title: "Micron Technology FY2025 10-K", url: "https://www.sec.gov/Archives/edgar/data/723125/000072312525000028/mu-20250828.htm", source: "SEC EDGAR", date: "2025-10-03"}
- {id: 18, title: "TrendForce 3Q25 DRAM Revenue Rankings", url: "https://www.trendforce.com/presscenter/news/20251126-12802.html", source: TrendForce, date: "2025-11-26"}
- {id: 19, title: "Samsung Reclaims Global Memory Top Spot in Q3 2025", url: "https://counterpointresearch.com/en/insights/samsumg-reclaims-global-memory-market-top-spot-in-Q3-2025-driven-by-robust-dram-nand-demand", source: "Counterpoint Research", date: "2025-Q3"}
- {id: 20, title: "Chinese DDR4 Producers Undercut South Korean Rivals' Pricing by 50%", url: "https://www.tomshardware.com/pc-components/dram/chinese-ddr4-producers-are-undercutting-south-korean-rivals-pricing-by-50-percent", source: "Tom's Hardware / Digitimes", date: "2024-11-19"}
- {id: 21, title: "CXMT 2026 Output Growth & LPDDR4X Leadership", url: "https://www.trendforce.com/research/download/RP251112MX", source: TrendForce, date: "2025-11-12"}
- {id: 22, title: "SK hynix FY25 Financial Results", url: "https://news.skhynix.com/sk-hynix-announces-fy25-financial-results/", source: "SK Hynix IR", date: "2026-01"}
- {id: 23, title: "Some Clarity on 2025's DDR4 Price Surge", url: "https://thememoryguy.com/some-clarity-on-2025s-ddr4-price-surge/", source: "The Memory Guy", date: "2025-05"}
- {id: 24, title: "Commerce Strengthens Export Controls (Dec 2 2024)", url: "https://www.bis.gov/press-release/commerce-strengthens-export-controls-restrict-chinas-capability-produce-advanced-semiconductors-military", source: "US BIS", date: "2024-12-02"}
- {id: 25, title: "US Exempts Some Chinese Firms from Curbs in Concession to Japan", url: "https://www.scmp.com/tech/tech-war/article/3289594/chip-war-us-exempts-some-chinese-firms-curbs-concession-japan-sources-say", source: SCMP, date: "2024-12-05"}
- {id: 26, title: "Federal Register 2024-28267 — Entity List additions", url: "https://www.federalregister.gov/documents/2024/12/05/2024-28267/additions-and-modifications-to-the-entity-list-removals-from-the-validated-end-user-veu-program", source: "Federal Register", date: "2024-12-05"}
- {id: 27, title: "Federal Register 2024-28270 — FDPR / HBM / SME IFR", url: "https://www.federalregister.gov/documents/2024/12/05/2024-28270/foreign-produced-direct-product-rule-additions-and-refinements-to-controls-for-advanced-computing", source: "Federal Register", date: "2024-12-05"}
- {id: 28, title: "Baker McKenzie analysis of Dec 2024 BIS controls", url: "https://sanctionsnews.bakermckenzie.com/us-department-of-commerce-significantly-expands-controls-targeting-indigenous-production-of-advanced-semiconductors-in-china/", source: "Baker McKenzie", date: "2024-12-09"}
- {id: 29, title: "Moolenaar Letter to Commerce on Loopholes", url: "https://chinaselectcommittee.house.gov/media/letters/letter-to-commerce-secretary-on-dangerous-loopholes-in-new-export-control-rules", source: "House Select Committee on the CCP", date: "2024-12-04"}
- {id: 30, title: "Slaying Self-Reliance — US Chip Controls in Biden's Final Stretch", url: "https://rhg.com/research/slaying-self-reliance-us-chip-controls-in-bidens-final-stretch/", source: "Rhodium Group", date: "2024-12-04"}
- {id: 31, title: "SK hynix Begins Volume Production of World's First 12-Layer HBM3E", url: "https://news.skhynix.com/sk-hynix-begins-volume-production-of-the-world-first-12-layer-hbm3e/", source: "SK Hynix IR", date: "2024-09-26"}
- {id: 32, title: "CXMT Reportedly Begins Mass Production of HBM2", url: "https://www.trendforce.com/news/2024/08/06/news-changxin-memory-technologies-has-reportedly-begun-mass-production-of-hbm2/", source: TrendForce, date: "2024-08-06"}
- {id: 33, title: "Biden bars HBM exports to China", url: "https://www.theregister.com/2024/12/03/biden_hbm_china_export_ban/", source: "The Register", date: "2024-12-03"}
- {id: 34, title: "Huawei Ascend Production Ramp — HBM is the Bottleneck", url: "https://newsletter.semianalysis.com/p/huawei-ascend-production-ramp", source: SemiAnalysis, date: "2025-04-04"}
- {id: 35, title: "Huawei Ascend 910C teardown — Samsung / SK Hynix components", url: "https://www.digitimes.com/news/a20251005PD200/huawei-ascend-tsmc-techinsights-samsung.html", source: "Digitimes / TechInsights", date: "2025-10-05"}
- {id: 36, title: "Chinese semiconductor industry gears up for domestic HBM3 by end-2026", url: "https://www.tomshardware.com/pc-components/dram/chinese-semiconductor-industry-gears-up-for-domestic-hbm3-production-by-the-end-of-2026-cxmt-to-produce-chips-while-naura-maxwell-and-u-preseason-design-tools-for-assembly", source: "Tom's Hardware", date: "2026-01-21"}
- {id: 37, title: "CXMT Ships HBM3 Samples to Huawei", url: "https://wccftech.com/china-cxmt-ships-out-pivotal-hbm3-samples-to-huawei/", source: Wccftech, date: "2026-03"}
- {id: 38, title: "CXMT HBM sample speed 4.4 Gbps", url: "https://x.com/teortaxesTex/status/1995310565716316471", source: "X / @teortaxesTex", date: "2025-12"}
- {id: 39, title: "SK hynix Rumored to Boost 2025 Capex by 30%", url: "https://www.trendforce.com/news/2025/07/28/news-sk-hynix-rumored-to-boost-2025-capex-by-30-on-2026-hbm-demand-visibility/", source: TrendForce, date: "2025-07-28"}
- {id: 40, title: "China's Big Fund Phase III Commences — RMB 344B", url: "https://www.trendforce.com/news/2024/05/27/news-chinas-big-fund-phase-three-commences-injecting-344-billion-rmb-into-semiconductor-industry-growth/", source: TrendForce, date: "2024-05-27"}
- {id: 41, title: "Big Fund II Invests RMB 14.5B in ChangXin Xinqiao", url: "https://www.trendforce.com/news/2023/11/01/news-with-two-october-investments-big-fund-phase-ii-commits-nearly-19-billion-rmb/", source: TrendForce, date: "2023-11-01"}
- {id: 42, title: "China Unveils Major Tax Incentive Policy (Guofa [2020] No.8)", url: "https://www.scmp.com/tech/policy/article/3096131/china-unveils-major-tax-incentive-policy-encourage-innovation-domestic", source: SCMP, date: "2020-08-04"}
- {id: 43, title: "Department of Commerce Awards CHIPS Incentives to Micron — $6.165B", url: "https://www.commerce.gov/news/press-releases/2024/12/department-commerce-awards-chips-incentives-micron-idaho-and-new-york", source: "US Department of Commerce", date: "2024-12-10"}
- {id: 44, title: "Project 506 — Horizon Advisory CXMT Brief", url: "https://issuu.com/horizonadvisory/docs/horizon_advisory_-_project_506_december_2022", source: "Horizon Advisory", date: "2022-12"}
- {id: 45, title: "China's Memory Makers Are Playing a Long Game", url: "https://www.crnasia.com/news/2026/components-and-peripherals/china-s-memory-makers-are-playing-a-long-game-and-it-s-worki", source: "CRN Asia", date: "2026"}
- {id: 46, title: "Samsung/SK hynix Delay DDR4 Phase-Out — DDR4 > DDR5 inversion", url: "https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/", source: TrendForce, date: "2025-09-02"}
- {id: 47, title: "3Q25 Consumer DDR4 +85–90% QoQ", url: "https://www.trendforce.com/presscenter/news/20250811-12667.html", source: TrendForce, date: "2025-08-11"}
- {id: 48, title: "1Q26 Conventional DRAM +90–95% QoQ — Record DRAM Spike", url: "https://www.trendforce.com/presscenter/news/20260202-12911.html", source: TrendForce, date: "2026-02-02"}
- {id: 49, title: "Samsung reallocates ~80,000 wafers/month from HBM to DDR5", url: "https://www.digitimes.com/news/a20251208PD214/samsung-hbm-ddr5-dram-capacity.html", source: Digitimes, date: "2025-12-08"}
- {id: 50, title: "Huawei Mate 70 Pro / Pro Plus uses SK Hynix LPDDR (not CXMT)", url: "https://www.scmp.com/tech/tech-war/article/3292261/huaweis-new-flagship-smartphones-use-south-korean-memory-chips-not-chinese-ones", source: "SCMP / TechInsights", date: "2024-12-26"}
- {id: 51, title: "CXMT LPDDR5 Validated by Xiaomi and Transsion", url: "https://www.digitimes.com/news/a20231129PD215/cxmt-dram-lpddr-5-xiaomi-transsion.html", source: Digitimes, date: "2023-11-29"}
- {id: 52, title: "CXMT Takes Aim at Global Leaders with High-End DDR5", url: "https://www.caixinglobal.com/2025-11-26/chinas-cxmt-takes-aim-at-global-leaders-with-high-end-ddr5-memory-chips-102386784.html", source: "Caixin Global", date: "2025-11-26"}
- {id: 53, title: "Lenovo ThinkBook 2026 reportedly uses CXMT LPCAMM2 modules", url: "https://videocardz.com/newz/lenovo-thinkbook-2026-reportedly-uses-cxmt-lpcamm2-memory-modules", source: VideoCardz, date: "2026-03"}
- {id: 54, title: "Lenovo ThinkBook LPCAMM2 (alternate)", url: "https://videocardz.com/newz/lenovo-thinkbook-2026-reportedly-uses-cxmt-lpcamm2-memory-modules", source: VideoCardz, date: "2026-03"}
- {id: 55, title: "Ten Former Samsung Employees Indicted for Leaking 10nm DRAM Tech to CXMT", url: "https://www.tomshardware.com/tech-industry/semiconductors/ten-former-samsung-employees-arrested-for-industrial-espionage-charges-for-giving-china-chipmaker-10nm-tech-executives-and-researchers-allegedly-leaked-dram-technology-to-china-based-cxmt-resulting-in-trillions-of-losses-in-korean-won", source: "Tom's Hardware", date: "2025-12-23"}
- {id: 56, title: "Chinese Chipmaker CXMT in Crosshairs of South Korean Prosecutors", url: "https://www.scmp.com/tech/big-tech/article/3337835/chinese-chipmaker-cxmt-crosshairs-south-korean-prosecutors-over-samsung-tech-leak", source: SCMP, date: "2025-12-26"}
- {id: 57, title: "ASML's China Question", url: "https://www.mbi-deepdives.com/asmls-china-question/", source: "MBI Deep Dives", date: "2025-01-29"}
- {id: 58, title: "ASML 2024 Annual Report", url: "https://ourbrand.asml.com/m/3035813cf1b8ea4f/original/2024-Annual-Report-based-on-IFRS-FINAL.pdf", source: "ASML IR", date: "2025-02"}
- {id: 59, title: "High-end DUV ban — China's damage coming into focus", url: "https://asiatimes.com/2024/01/high-end-duv-ban-chinas-damage-coming-into-focus/", source: "Asia Times", date: "2024-01-10"}
- {id: 60, title: "NAURA Wins $380M CXMT Etcher Order", url: "https://semiconductorinsight.com/blog/naura-amec-and-sicarrier-shake-up-global-etch-equipment-market-amid-chinas-tech-rise/", source: "Semiconductor Insight", date: "2025-11"}
- {id: 61, title: "AMEC FY2024 Etch Revenue +54.7% YoY", url: "https://www.digitimes.com/news/a20251030VL219/amec-etching-thin-film-equipment-growth.html", source: Digitimes, date: "2025-10-30"}
- {id: 62, title: "Applied Materials — $710M China Revenue Hit", url: "https://invezz.com/news/2025/10/03/applied-materials-decline-after-710m-revenue-hit-from-us-export-restrictions/", source: Invezz, date: "2025-10-03"}
- {id: 63, title: "CXMT DDR5 Reveals 3-Year Technology Gap (TechInsights/SemiWiki)", url: "https://semiwiki.com/forum/threads/chinas-cxmts-ddr5-reveals-3-year-technology-gap.23270/", source: SemiWiki, date: "2025-10-15"}
- {id: 64, title: "Is CXMT a Threat or an Illusion?", url: "https://damnang2.substack.com/p/is-cxmt-a-threat-or-an-illusion", source: "Damnang2 Substack", date: "2025-09-15"}
- {id: 65, title: "The Memory Siege — CXMT vs the Big 3", url: "https://bizety.com/2025/12/28/the-memory-siege-chinas-cxmt-targets-the-big-3-dram-hegemony/", source: Bizety, date: "2025-12-28"}
- {id: 66, title: "CXMT Logs First Annual Profit on Price Spike", url: "https://www.digitimes.com/news/a20260102PD220/dram-cxmt-2025-profit-price.html", source: Digitimes, date: "2026-01-02"}
- {id: 67, title: "Samsung DS Division 65.7% Operating Margin in 1Q26", url: "https://www.trendforce.com/news/2026/04/30/news-samsungs-ds-division-tops-nvidia-with-65-7-operating-margin-driving-93-8-of-1q26-profit-on-memory-boom/", source: TrendForce, date: "2026-04-30"}
- {id: 68, title: "CXMT $138 server RAM pricing", url: "https://aihola.com/article/cxmt-china-ram-pricing-crisis", source: AIhola, date: "2026"}
- {id: 69, title: "SK hynix 1Q26 Financial Results", url: "https://www.prnewswire.com/news-releases/sk-hynix-announces-1q26-financial-results-302750959.html", source: "SK Hynix IR", date: "2026-04"}
- {id: 70, title: "YMTC Partners with CXMT for HBM", url: "https://www.tomshardware.com/pc-components/ram/ymtc-partners-with-cxmt-for-hbm", source: "Tom's Hardware", date: "2025-09-26"}
- {id: 71, title: "Samsung / SK hynix Warn AI Memory Shortages Through 2027+", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/samsung-and-sk-hynix-warn-ai-driven-memory-shortages-could-last-until-2027-and-beyond-as-hbm-demand-explodes-customers-already-reserving-supply-years-ahead-while-the-wider-dram-market-begins-to-tighten", source: "Tom's Hardware", date: "2026-02"}
- {id: 72, title: "YMTC Partners with CXMT for HBM (alt)", url: "https://www.tomshardware.com/pc-components/ram/ymtc-partners-with-cxmt-for-hbm", source: "Tom's Hardware", date: "2025-09-26"}
- {id: 73, title: "SK hynix Develops Industry-First 1c DDR5", url: "https://news.skhynix.com/sk-hynix-develops-industry-first-1c-ddr5/", source: "SK Hynix IR", date: "2024-08-29"}
- {id: 74, title: "Morgan Lewis — Dec 2024 BIS Controls", url: "https://www.morganlewis.com/pubs/2024/12/commerce-significantly-expands-controls-on-advanced-computing-and-semiconductor-manufacturing-items", source: "Morgan Lewis", date: "2024-12-05"}
- {id: 75, title: "How GigaDevice and Montage Earned a Place in Memory", url: "https://www.scmp.com/tech/tech-trends/article/3343706/how-chinas-gigadevice-and-montage-earned-place-memory-chip-market", source: SCMP, date: "2025"}
- {id: 76, title: "Tongfu Microelectronics RMB 4.4B placement; CXMT HBM packaging", url: "https://www.trendforce.com/news/2026/01/19/news-chinas-osat-giants-step-up-tongfu-microelectronics-to-raise-rmb-4-4b-jcet-backs-chip-fund/", source: TrendForce, date: "2026-01-19"}
- {id: 77, title: "Korea Logs Fastest GDP Growth in 5.5 Years on Chip Exports", url: "https://www.koreatimes.co.kr/economy/20260423/korea-logs-fastest-gdp-growth-in-5-12-yrs-on-strong-semiconductor-exports", source: "Korea Times / BoK", date: "2026-04-23"}
- {id: 78, title: "SK hynix Set to Overtake Samsung as DRAM Leader", url: "https://www.spglobal.com/market-intelligence/en/news-insights/research/2025/05/sk-hynix-set-to-overtake-samsung-as-dram-leader-amid-ai-driven-memory-boom", source: "S&P Global Market Intelligence", date: "2025-05"}
- {id: 79, title: "Server Memory Prices Could Double by 2026", url: "https://www.networkworld.com/article/4093752/server-memory-prices-could-double-by-2026-as-ai-demand-strains-supply.html", source: NetworkWorld, date: "2025-11-20"}
- {id: 80, title: "SK hynix to Build First US 2.5D HBM Packaging Plant — Indiana", url: "https://www.tomshardware.com/tech-industry/sk-hynix-to-build-first-us-2-5d-packaging-plant-for-hbm", source: "Tom's Hardware", date: "2025-12-30"}
- {id: 81, title: "Tokyo Electron AI-driven Sales Hitting 40% by 2026", url: "https://www.trendforce.com/news/2025/12/08/news-tokyo-electron-sees-ai-driven-sales-hitting-40-by-2026-offsetting-china-slowdown/", source: TrendForce, date: "2025-12-08"}
- {id: 82, title: "ASML Sees China Sales Normalizing in 2026", url: "https://www.caixinglobal.com/2025-10-16/asml-sees-china-sales-normalizing-in-2026-after-backlog-fueled-surge-102372186.html", source: Caixin Global, date: "2025-10-16"}
- {id: 83, title: "Memory Giants' HBM Focus / Taiwan DRAM Vendors Surge", url: "https://www.trendforce.com/news/2025/10/17/news-memory-giants-hbm-focus-could-limit-dram-growth-through-2026-taiwan-firms-boost-ddr4/", source: TrendForce, date: "2025-10-17"}
- {id: 84, title: "Trump Administration May Add CXMT to Entity List", url: "https://www.tomshardware.com/tech-industry/trump-administration-could-add-cxmt-and-other-chinese-chipmakers-to-ever-expanding-export-blacklist", source: "Tom's Hardware", date: "2026"}
- {id: 87, title: "Will China Hit the HBM Wall?", url: "https://www.chinatalk.media/p/will-china-hit-the-hbm-wall", source: ChinaTalk, date: "2025"}
- {id: 88, title: "CXMT MR-MUF HBM3 Packaging", url: "https://www.digitimes.com/news/a20251107PD215/hbm-sk-hynix-cxmt-mr-muf-2026.html", source: Digitimes, date: "2025-11-07"}
- {id: 91, title: "CXMT IPO Capacity Market Analysis", url: "https://www.digitimes.com/news/a20260102PD221/dram-cxmt-ipo-capacity-market.html", source: Digitimes, date: "2026-01-02"}
- {id: 93, title: "Hefei Model — CXMT IPO Coverage", url: "https://hellochinatech.com/p/hefei-model-cxmt-ipo-china-semiconductor", source: HelloChinaTech, date: "2025"}
- {id: 96, title: "CXMT Delivers 16nm HBM3 Samples to Huawei", url: "https://www.digitimes.com/news/a20250818PD202/cxmt-hbm3-hbm-huawei-expansion.html", source: Digitimes, date: "2025-08-18"}
- {id: 97, title: "Huawei Used TSMC, Samsung, SK Hynix Components in Top AI Chips", url: "https://www.bloomberg.com/news/articles/2025-10-03/huawei-used-tsmc-samsung-sk-hynix-components-in-top-ai-chips", source: Bloomberg, date: "2025-10-03"}
- {id: 100, title: "CXMT 1H 2026 Earnings Outlook", url: "https://x.com/jukan05/status/2055951991004958965", source: "X / @jukan05", date: "2026-05-17"}
- {id: 101, title: "Morgan Stanley note on CXMT HBM2 sampling", url: "https://x.com/Jukanlosreve/status/1927516409006792736", source: "X / Morgan Stanley", date: "2025-05-27"}
- {id: 103, title: "CXMT Surprising New Chipmaking Capabilities", url: "https://www.tomshardware.com/pc-components/dram/chinas-banned-memory-maker-cxmt-unveils-surprising-new-chipmaking-capabilities-despite-crushing-us-export-restrictions-ddr5-8000-and-lpddr5x-10667-displayed", source: "Tom's Hardware", date: "2025-07"}
- {id: 104, title: "CXMT SSE Prospectus Shareholder Disclosure (21jingji)", url: "https://m.21jingji.com/article/20251231/herald/1158b65e5308fc615eef69cc215976d3_zaker.html", source: "21st Century Business Herald", date: "2025-12-31"}
- {id: 105, title: "Wuhan Xinxin $2.4B HBM Packaging Fab", url: "https://www.tomshardware.com/pc-components/dram/chinese-memory-maker-gets-dollar24-billion-to-build-hbm-for-ai-processors-shanghai-packaging-facility-to-open-in-2026", source: "Tom's Hardware", date: "2024-05"}
- {id: 106, title: "MU, 005930.KS, 000660.KS — monthly close, June 2024–May 2026", url: "https://finance.yahoo.com/quote/MU/history", source: "Yahoo Finance", date: "2026-05"}
:::
