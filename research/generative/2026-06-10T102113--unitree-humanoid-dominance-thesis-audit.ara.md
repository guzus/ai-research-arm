---
eyebrow: DEEP DIVE · ROBOTICS · CHINA
title: "Unitree and the humanoid race: the cost machine is real, the word 'dominate' is not"
deck: A first-principles audit of the SemiAnalysis thesis that China's Unitree will own global humanoid robotics — built from the IPO prospectus, the actuator physics, and the export-control paperwork.
domain: general
lede: |
  Unitree is the most important hardware story in humanoid robotics: the only profitable maker, the price-setter, the company that shipped more humanoids in 2025 than Tesla, Figure and Boston Dynamics combined could deploy. The SemiAnalysis thesis — that Unitree runs the "DJI playbook" and will dominate the world the way DJI dominated drones and BYD dominated EVs — is the sharpest articulation of the bull case. It is also, in three specific places, contradicted by its own evidence. The cost machine is real and the iteration speed is real. But "dominate global" runs into a domestic duopoly, a physics ceiling on cheap actuators, an autonomy problem nobody has solved, and — as of two days ago — a Pentagon designation that puts Unitree on exactly the path that locked DJI and BYD out of the West.
stats:
  - {label: G1 list price, value: $13.5K, note: "was $16K at 2024 launch"}
  - {label: 2025 revenue, value: ¥1.70B, note: "+335% YoY"}
  - {label: 2025 humanoid units, value: "4,200", note: "Omdia: 2nd behind AgiBot"}
  - {label: IPO raise (STAR), value: "~$610M", note: "~$7B target valuation"}
  - {label: Productive deployments, value: "~3-4%", note: "of 2025 humanoid units"}
---

The thesis under audit is SemiAnalysis's "China's Unitree Will Dominate Global Humanoid Robotics."[^1] It is a strong piece of industrial analysis, and its mechanism — own the bottleneck component, bootstrap a research audience, ride the ecosystem, unlock a new market each hardware generation — is the correct lens. This report stress-tests it against primary sources: Unitree's Shanghai STAR Market prospectus, the MIT actuator paper that invented the design Unitree uses, Tesla and Figure disclosures, USGS and IEA mineral data, and the U.S. statute book. The conclusion is not that the thesis is wrong. It is that the thesis is *half right in a way that matters for the investment and policy decisions that ride on it*.

:::kv
- {term: "Is Unitree the global low-cost humanoid leader?", def: "Yes. $13.5K G1, ~60% gross margin, only profitable maker, ~335% revenue growth.[^5][^8][^9]"}
- {term: "Will it 'dominate' the way DJI/BYD did?", def: "Unlikely as stated. It is one of a Chinese duopoly (with AgiBot), and DJI/BYD were locked out of the West despite winning on cost.[^13][^41]"}
- {term: "Is the cheap-actuator moat durable?", def: "Partly. QDD wins on cost and dynamics but is thermally capped; Tesla and Figure chose expensive harmonic drives for industrial torque.[^17][^19]"}
- {term: "Are humanoids 'economically viable today'?", def: "Not as a general claim. ~96% of Unitree humanoids go to labs; real production work runs on $150K teleoperated machines.[^8][^28]"}
- {term: "The biggest risk the thesis under-weighted?", def: "Western market access. On 2026-06-08 the Pentagon named Unitree a Chinese military company.[^2][^3]"}
:::

## 01. The thesis, stated fairly — and the news that already dates it

The bull case is not hype, and it deserves to be stated at full strength. Unitree, founded in 2016 by Wang Xingxing on the back of a graduate-school quadruped, drove the price of a four-legged robot from $45,000 (Laikago, 2018) to roughly $1,600 today (Go2) — a ~96% decline that funded years of manufacturing learning before it ever built a humanoid.[^1] It then carried that supply chain into bipeds: the G1 launched at $16,000 in May 2024 and now lists at **$13,500** on Unitree's own store, with an R1 model introduced in July 2025 at **$5,900**.[^5][^6][^7] No Western humanoid is within an order of magnitude on price.

The SemiAnalysis "DJI strategy" framing — own the critical component, bootstrap a niche, ride ecosystem cost curves, unlock a new market each generation — genuinely describes what happened.[^1] Where the thesis gets into trouble is its load-bearing word: *dominate global*. Both precedents it invokes, DJI and BYD, won cost and unit-share dominance and were then **shut out of the West on national-security and trade grounds** — DJI by customs detentions and an FCC Covered-List action,[^41] BYD by a 100%+ U.S. tariff that leaves the great majority of its sales in China (it jumped from ~179K to ~604K NEVs in 2020-21 yet remains effectively barred from the U.S.).[^51][^56] Owning a Chinese supply chain did not protect them; it was the *reason* for the exclusion.

:::statement(attr="ARA Research")
The feature the thesis celebrates — a vertically integrated, Chinese-controlled supply chain — is the precise attribute that triggers a Western lockout. Verticalization is the moat against competitors and the bullseye for regulators.
:::

That abstraction stopped being abstract on **2026-06-08**, when the U.S. Department of Defense added Unitree to its Section 1260H list of "Chinese military companies," alongside Alibaba, Baidu and BYD — a list of 188 entities the Pentagon says contribute to China's military-civil fusion.[^2][^3][^4] Under the NDAA's contracting rules, the Defense Department may not contract with listed firms from **2026-06-30**, with indirect contracting barred a year later.[^2] It is not yet an import ban — but it is step one of the exact sequence that produced the DJI lockout, arriving *before* Unitree has any meaningful U.S. installed base to protect. Why this matters: the thesis is a claim about global dominance, and the largest, richest robotics market on earth is in the process of closing its door.

## 02. The cost machine is real — and the prospectus corrects the legend

Strip away the analogies and the core of the thesis is an income statement, and here the bull case is strongest. Unitree's revenue climbed from ¥159M (2023) to ¥392M (2024) to **¥1.70B (2025)**, a ~335% jump that makes the thesis's "tripling revenues" framing an *understatement*.[^8][^9][^11] It turned its first profit in 2024 and is, by multiple prospectus readings, the **only profitable humanoid robotics company in the world** — a fact that alone separates it from a field burning billions.[^9]

:::stats
- {label: Revenue 2023, value: ¥159M}
- {label: Revenue 2024, value: ¥392M, note: first net profit (¥94.5M)}
- {label: Revenue 2025, value: ¥1.70B, note: +335% YoY}
- {label: Company gross margin, value: ~60%, note: 9M 2025}
- {label: External parts, value: "14-18%", note: of total cost (rest in-house)}
:::

But a careful audit corrects several numbers that have hardened into legend. The SemiAnalysis figure of a **$27,300 G1** does not match Unitree's own storefront, which lists the G1 from **$13,500**; the "$50K+" history and "$27.3K" both appear to conflate optioned EDU configurations or reseller markups with the base unit.[^5] An independent teardown puts the base G1 bill-of-materials near **¥41,574 (~$5,720)**, below the ~$8,976 the thesis cites — while *confirming* the load-bearing structural claim: integrated joints are ~66% of that BOM, squarely inside the "50-70% of cost is actuators" range, and Unitree makes them itself.[^54][^9] The margins are real but compressing: humanoid gross margin fell from **87.67% (2023) to 68.44% (2024) to 62.91% (Jan-Sep 2025)** as average selling prices collapsed ~72%.[^10]

That last series is the tell. Unitree's humanoids became its largest revenue line not because they command premium prices but because volume exploded while ASPs cratered — and more than 70% of those units went to universities and research labs, with only ~9% reaching industry and, by one prospectus-based analysis, an estimated ~3-4% doing genuinely productive enterprise work.[^8][^9] The cost machine is verified. What it is *not* yet is an industrial-deployment machine.

:::donut(center-label="9M'25 rev")
- {label: Humanoids, value: 51.5}
- {label: Quadrupeds, value: 42.3}
- {label: Components & other, value: 6.2}
:::

:::note
Revenue-mix shares are Unitree's first-nine-months-2025 figures from prospectus reporting; "humanoid" is now the largest line by revenue but is dominated by research/education buyers, not factories.[^8]
:::

## 03. The actuator bet: a real moat that is also a real ceiling

The engineering heart of the thesis is that Unitree owns the actuator bottleneck through **quasi-direct drive** (QDD): a brushless motor plus a low-ratio gearbox, cheap to make on standard equipment, where rivals use expensive strain-wave (harmonic) reducers. The cost direction is right — a research QDD arm can be built for under $5,000 against harmonic-drive arms at $25,000-$67,000.[^18] But two parts of the thesis need correction, and the correction is the whole story.

First, the headline efficiency claim — QDD at 95-98% versus harmonic at 85-90% — is a category error. QDD's high efficiency comes from *barely gearing at all*, not from superior gear quality; well-made planetary trains and harmonic drives both span wide efficiency bands depending on load.[^20] More important, the MIT Cheetah paper that *invented* this design quantifies the trade-off the thesis waves past: torque-production efficiency scales with gear ratio to roughly the **4.1 power**, and the authors state plainly that "a load-carrying robot walking at slow speeds could energetically benefit from a higher gear ratio."[^17] Low gearing means the motor must pour current in to make torque, which means heat, which means a hard ceiling on continuous payload and duty cycle — exactly the regime industrial work lives in.

:::compare
- {role: LOWEST, name: "Unitree G1 (QDD)", value: ~2 kg payload}
- {role: HIGHEST, name: "Boston Dynamics Atlas", value: ~50 kg lift}
- {role: SUBJECT, name: "Unitree G1 (QDD)", value: ~2 kg payload}
:::

The market test settles it. Tesla's Optimus and Figure's robots — the firms chasing high-value industrial manipulation — did **not** choose QDD. Optimus uses 28 custom actuators built around **harmonic drives** (rotary) and **planetary roller screws** (linear), the expensive, torque-dense, stiff path, precisely because that is what sustained industrial torque demands.[^19] The honest version of the thesis is therefore narrower and stronger: Unitree dominates the *cost-sensitive, dynamic, low-duty-cycle* segment — research platforms, locomotion, light service — not necessarily the heavy-manipulation frontier where the margins and the labor-replacement dollars actually are.

A market signal cuts the other way too. If cheap QDD were making strain-wave reducers obsolete, the leading harmonic-drive maker's equity should reflect it. Instead, Harmonic Drive Systems (Tokyo: 6324) **more than doubled** over the year to June 2026, peaking near ¥7,800, as investors bid up the incumbent on humanoid-actuator demand.[^53]

:::line-chart(title="Harmonic Drive Systems (6324.T), trailing 12 months", subtitle="Monthly close, ¥ — the 'obsolete' incumbent the market is bidding up", y-unit=¥)
x: 2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06
6324.T: 2906,2578,2647,2852,3090,3780,3400,4555,3465,5220,7800,6240
:::

What would weaken this section's claim: if Unitree's cycloidal-QDD and active-cooling work (vapor chambers, pelvis cooling) closes the torque-density and thermal gap, the "ceiling" softens. The research direction is real — but so is the fact that the field is engineering *around* classic QDD precisely because it tops out.[^17]

## 04. "Dominate" is the wrong word: it is a duopoly in a crowded, subsidized field

Even granting the cost machine, the thesis's claim is about *one company*. The data describes a *country* — and within it, at least two co-leaders. The only independent shipment tracker, Omdia, ranks **AgiBot first in 2025 with 5,168 humanoids, Unitree second at 4,200, and UBTech third near 1,000**, out of 13,318 globally; Unitree's own claim of "#1, 5,500+ units" is a self-report the tracker contradicts.[^13] A leader whose top ranking depends on its own numbers is not dominant.

:::rank-list
- {label: AgiBot (Zhiyuan), value: "5,168", pct: 100}
- {label: Unitree, value: "4,200", pct: 81, highlight: true}
- {label: UBTech (9880.HK), value: "~1,000", pct: 19}
- {label: All others (global), value: "~3,000", pct: 58}
:::

:::source
2025 humanoid shipments, Omdia via SCMP. Global total 13,318 units, up ~480% YoY.[^13]
:::

The competitive field is deep and state-backed. AgiBot — founded by ex-Huawei star Peng Zhihui — hit its 10,000th robot by March 2026 and is reverse-merging into STAR-listed Swancor for a public listing.[^16] UBTech (HK:9880) began Walker S2 mass production in November 2025 with a **2025 order book over ¥800M** from automakers including BYD, Geely and Foxconn — meaning UBTech, not Unitree, leads on actual *factory* deployments.[^15] Behind them sit Galbot (~$3B valuation), Robot Era, EngineAI, Fourier and LimX, many with captive automaker backers (XPeng, Geely, CATL) that Unitree lacks.[^55] TrendForce projects Unitree and AgiBot together will take **~80%** of China's 2026 humanoid shipments — the very definition of a duopoly, not a monopoly.[^14]

The deepest problem for a *company* moat: the cost advantage is an *ecosystem* advantage. Every credible source attributes China's price lead to the shared EV-and-drone supply chain — components available to all ~140-200 domestic OEMs.[^50] An advantage 140 rivals can also tap is not defensible against those rivals, and Unitree's Q1 2026 core profit already fell ~53% under competitive pressure.[^9] And state capital is flooding a deep bench of rivals — Robot Era, Galbot and others raising hundreds of millions each — rather than anointing one champion.[^55][^50] The defensible claim is "China dominates global humanoid manufacturing." "Unitree dominates" is a different, weaker claim.

## 05. The deployment mirage: "economically viable today" does not survive contact

The thesis's most aggressive claim is that Unitree humanoids are economically viable *now* for labor replacement, with ~250 in productive deployments. This is where first-principles scrutiny does the most damage, because the argument quietly swaps two different robots.

The economic model prices a tote-handoff task at the cheap robot's price (~$13-27K → ~$12-15/hour amortized) but credits it with the *work* that only the expensive robot can do. A Unitree G1 has a **~2 kg arm payload**; warehouse totes weigh 15-25 kg.[^31] The only humanoid actually moving totes under a commercial contract is Agility's **Digit** — a ~$150K-class machine that crossed 100,000 totes at GXO under the industry's first humanoid Robots-as-a-Service deal.[^27][^28] No single machine today is both cheap *and* capable of the task; the model gets viability by combining the price of one with the performance of the other.

:::callout(kind=warn, label="The hidden cost")
Most current humanoid "deployments" are **teleoperated**, not autonomous. If a human is still in the loop — even offshore — you have relocated labor, not replaced it. At realistic near-1:1 operator ratios (Figure pays U.S. operators $25-35/hour), the all-in cost can *exceed* the warehouse worker it replaces, whose fully loaded U.S. cost is ~$25-30/hour, not the ~$46 all-industry average sometimes cited.[^32]
:::

Independent observers are blunt about the gap between demos and production. IEEE Spectrum called the humanoid market "almost entirely hypothetical" in late 2025; Bain described deployments as pilots "heavily dependent on human input."[^32][^34] Even the sell-side bulls put the inflection in the **2030s and beyond**: Morgan Stanley's ~1 billion units and $5 trillion is a *2050* number; Bank of America projects 3 billion units by *2060* — forecasts that disagree by orders of magnitude, which is what speculation looks like.[^35][^36] A thesis claiming today-viability is arguing against its own sell-side support.

:::quote(attr="Rodney Brooks, roboticist (iRobot, Rethink Robotics), Sept 2025")
We are more than ten years away from the first profitable deployment of humanoid robots even with minimal dexterity.
:::

What would falsify *this* skepticism: a disclosed, audited deployment of cheap autonomous humanoids doing sustained paid work without a teleoperator behind the curtain. As of mid-2026, the best-documented "real" deployment remains a single expensive, contract-bound Digit fleet — not a fleet of cheap autonomous Unitrees.[^28] Why it matters: every billion-dollar TAM rests on a cost crossover that has not happened.

## 06. The software question: the body is commoditizing, the brain is not

A second thesis is fighting the first: that the robot body is becoming a commodity and the durable moat is autonomy — the "brain." If true, a hardware-cost story under-describes who wins. The honest read is that the two theses are more complementary than opposed.

Autonomy progress in 2025-2026 is real but narrow. Physical Intelligence's π0.5 reaches ~94% success on tasks in homes it never trained in, with generalization improving as training-environment diversity grows.[^46] Google DeepMind's on-device model adapts to new tasks with 50-100 demonstrations and transfers across robot bodies.[^47] Figure demonstrated an 8-hour autonomous sorting shift — though the policy was trained on hundreds of hours of teleoperation, a vendor demo rather than an independent result.[^57] Every one of these is single-task, vendor-scored, or teleoperation-derived; nothing is general-purpose autonomy in the open world, and the consensus bottleneck is the absence of internet-scale *action* data.[^33]

This is where cheap hardware re-enters as a *software* argument: more robots in the world generate more real-world data, a flywheel that compounds, because generalization improves with the diversity of environments a model has actually seen.[^46] A 4,000-strong Unitree fleet is, in principle, a data asset — *if* those robots are doing manipulation, not just RL locomotion in a lab, which today they mostly are.[^9]

:::kv
- {term: Unitree's own AI bet, def: "~$300M of IPO proceeds for in-house embodied foundation models; two open-sourced (UnifoLM-WMA-0, -VLA-0).[^49]"}
- {term: The hedge, def: "Also serves as NVIDIA's Isaac GR00T reference humanoid (H2 Plus) — leaning on a U.S. software/compute stack.[^48]"}
- {term: The exposure, def: "That same NVIDIA-Jetson dependence is a reverse export-control chokepoint the West could tighten."}
:::

So Unitree is not a pure hardware firm hoping someone else solves software — it is hedging, in-house *and* on NVIDIA. But its demonstrated strength is locomotion; dexterous manipulation autonomy is unsolved for *everyone*, which means the software moat is still unclaimed. Whoever claims it — a U.S. lab, a Chinese lab, or a fleet-data flywheel — is not yet determined by hardware cost alone.

## 07. The real bottleneck and the closing wall

The thesis says Unitree owns the bottleneck. At the component level the deeper bottleneck is upstream, and it belongs to *China the state*, not Unitree the company. Every humanoid actuator needs high-performance NdFeB magnets, doped with heavy rare earths (dysprosium, terbium) for heat resistance — and China controls roughly **69% of rare-earth mining, ~91% of refining, ~94% of magnet production, and ~99% of heavy-rare-earth separation**.[^37][^38]

:::bars
- {label: Heavy-RE separation (Dy/Tb), value: "~99%", pct: 99}
- {label: NdFeB magnet production, value: "~94%", pct: 94}
- {label: Rare-earth refining, value: "~91%", pct: 91}
- {label: Rare-earth mining, value: "~69%", pct: 69}
:::

:::source
China's share of the rare-earth value chain, 2024. USGS Mineral Commodity Summaries; IEA Critical Minerals.[^37][^38]
:::

This cuts both ways, and that is the point. It is a genuine structural tailwind for *all* Chinese robot makers — but it is a *national* lever, not a company moat, and China has shown it will pull it: on **2025-04-04** Beijing imposed export licensing on exactly the heavy rare earths and magnets humanoid actuators depend on, a control that also delayed Tesla's Optimus.[^39][^23] Wielding the lever, however, accelerated Western diversification — the Pentagon took a ~15% stake in MP Materials in July 2025 to build domestic magnet capacity, though at ~10,000 t/yr by 2028 it remains a fraction of Chinese output.[^40]

The wall on the demand side is rising faster than the drone precedent did. The toolkit that locked out DJI — customs detentions, the FCC Covered List, the 1260H designation — is proven and transferable, and lawmakers are explicitly invoking the "DJI playbook" for robots.[^41][^45] The threat surface is sharper: a networked, camera- and microphone-laden, *physically actuated* machine inside homes and factories is a worse espionage-and-safety object than a drone. And the evidence is already on the record — the "UniPwn" vulnerability (September 2025) let a single fleet-wide hardcoded key spread root-level code between Unitree robots over Bluetooth, and security researchers documented G1 units transmitting telemetry to servers in China by default.[^42][^43]

:::timeline
- {date: 2024-10, headline: "CBP detains DJI imports", body: "U.S. customs begins holding DJI shipments under the forced-labor statute — the template."}
- {date: 2025-04, headline: "China rare-earth export controls", body: "Licensing on Dy/Tb magnets; delays Optimus, signals the lever exists.[^39]"}
- {date: 2025-09, headline: "UniPwn disclosed", body: "Wormable BLE root RCE across Unitree Go2/G1/H1/B2 via one shared key.[^42]"}
- {date: 2025-11, headline: "Humanoid ROBOT Act introduced", body: "Senate bill bars federal acquisition of adversary-nation humanoids.[^44]"}
- {date: 2025-12, headline: "FCC adds foreign drones to Covered List", body: "Full DJI import-authorization lockout — the precedent for robots.[^41]"}
- {date: 2026-06, headline: "GUARD Act + Pentagon 1260H listing", body: "Bill to extend Covered List to robots; DoD names Unitree a Chinese military company.[^45][^2]"}
:::

Why this matters most: the thesis's own precedents prove that winning on cost does not buy Western market access — and the machinery to deny it is arriving earlier for humanoids than it did for drones. Unitree can plausibly own China and the Global South. The U.S. and allied security-sensitive markets are a different question, and the answer is trending toward "no."

## 08. What would break this analysis — and the scorecard

This report is itself a thesis, so it deserves its own falsification tests.

- **If autonomy is solved fast and cheaply** — a general manipulation model that runs on a $13K body — the payload/teleoperation objections in Section 05 collapse and the cheap-fleet data flywheel (Section 06) becomes decisive. Watch π-class and GR00T-class results on *unseen, unstructured* tasks.[^46][^48]
- **If the U.S. lockout stalls** — the GUARD Act dies in committee and 1260H stays a contracting-only measure — then "dominate global" survives in a world where the West simply isn't the relevant market, and China + Global South is enough.[^45]
- **If Unitree's cooling and cycloidal-QDD work closes the torque ceiling**, the Section 03 "ceiling" weakens and the cost advantage extends into heavy manipulation.
- **If the IPO prospectus numbers are revised** — the margins and deployment-mix figures are prospectus-derived secondaries; the audited STAR filing could move them.[^9]

Against the thesis, the strongest standing facts are the duopoly (AgiBot out-ships Unitree on the one independent tracker),[^13] the deployment reality (~3-4% productive),[^8] and the closing wall (1260H, two days old).[^2] In its favor: the cost machine and profitability are verified and genuinely without peer.[^9]

:::callout(kind=info, label="Red-team result")
Red-team pass: **3/3 top claims unbroken.** The three load-bearing claims here — the Pentagon 1260H listing (2026-06-08), the $13.5K G1 official price, and the Omdia 2025 shipment ranking — each survived an adversarial search for contradicting evidence. The thesis's strongest claim (Unitree's cost leadership and sole profitability) also held; it is the *scope* word "dominate," not the cost analysis, that fails.
:::

The verdict: SemiAnalysis is right that Unitree built an extraordinary cost-and-iteration machine and right that it leads the early market. It is wrong, or at least over-reaching, on "dominate global." The realistic 2030 picture is a Chinese duopoly (Unitree + AgiBot) atop a deep subsidized ecosystem, winning the cost segment worldwide and the volume crown in China and the Global South — while a wall of Western export controls, a physics ceiling on cheap actuators, and an unsolved autonomy problem keep "global domination" out of reach. The cost machine is real. The word is not.

:::references
- {id: 1, title: "China's Unitree Will Dominate Global Humanoid Robotics", url: "https://newsletter.semianalysis.com/p/chinas-unitree-will-dominate-global", source: SemiAnalysis, date: "2026-06"}
- {id: 2, title: "Pentagon says Alibaba, Baidu, BYD and Unitree support China's military", url: "https://techcrunch.com/2026/06/08/pentagon-says-alibaba-baidu-byd-and-unitree-support-chinas-military/", source: TechCrunch, date: "2026-06-08"}
- {id: 3, title: "Entities Identified as Chinese Military Companies (Section 1260H)", url: "https://media.defense.gov/2026/Jun/08/2003945537/-1/-1/1/ENTITIES-IDENTIFIED-AS-CHINESE-MILITARY-COMPANIES-OPERATING-IN-THE-UNITED-STATES-IN-ACCORDANCE-WITH-SECTION-1260H.PDF", source: U.S. Department of Defense, date: "2026-06-08"}
- {id: 4, title: "Alibaba, Baidu, BYD named on Pentagon's China military list", url: "https://www.cnbc.com/2026/06/09/alibaba-baidu-byd-named-on-pentagons-china-military-list-.html", source: CNBC, date: "2026-06-09"}
- {id: 5, title: "Unitree G1 humanoid product page", url: "https://www.unitree.com/g1/", source: Unitree Robotics, date: "2026-06-10"}
- {id: 6, title: "Unitree unveils G1 humanoid for $16K", url: "https://www.therobotreport.com/unitree-robotics-unveils-g1-humanoid-for-16k/", source: The Robot Report, date: "2024-05-15"}
- {id: 7, title: "China's Unitree debuts US$5,900 humanoid robot", url: "https://www.scmp.com/tech/tech-trends/article/3319637/chinas-unitree-debuts-us5900-humanoid-robot-race-make-cheaper-products", source: South China Morning Post, date: "2025-07-29"}
- {id: 8, title: "Unitree IPO: does humanoid robotics really sell?", url: "https://hellochinatech.com/p/unitree-ipo-humanoid-robotics-really-sells", source: HelloChinaTech, date: "2026-03"}
- {id: 9, title: "Inside Unitree's prospectus: revenue climbs, profits dip", url: "https://www.humanoidsdaily.com/news/inside-unitree-s-prospectus-revenue-climbs-and-profits-dip-as-star-market-ipo-hearing-approaches", source: Humanoids Daily, date: "2026-05"}
- {id: 10, title: "Unitree prospectus segment margins (translation)", url: "https://eu.36kr.com/en/p/3731404085015046", source: 36Kr, date: "2026"}
- {id: 11, title: "Unitree Robotics files for $608M STAR Market IPO", url: "https://www.caixinglobal.com/2026-03-21/unitree-robotics-files-for-608-million-star-market-ipo-102425491.html", source: Caixin Global, date: "2026-03-21"}
- {id: 12, title: "China's Unitree plans $7 billion IPO valuation", url: "https://www.cnbc.com/2025/09/09/chinas-unitree-plans-7-billion-ipo-valuation-as-humanoid-robot-race-heats-up.html", source: CNBC, date: "2025-09-09"}
- {id: 13, title: "Chinese firms outpace US rivals in 2025 humanoid shipments; AgiBot takes lead", url: "https://www.scmp.com/tech/tech-trends/article/3339346/chinese-firms-outpace-us-rivals-2025-humanoid-robot-shipments-agibot-takes-lead", source: SCMP (Omdia data), date: "2026-01-09"}
- {id: 14, title: "Unitree and AgiBot to capture nearly 80% market share", url: "https://www.trendforce.com/presscenter/news/20260409-13007.html", source: TrendForce, date: "2026-04-09"}
- {id: 15, title: "UBTech Walker S2 begins mass production; orders exceed ¥800M", url: "https://www.prnewswire.com/news-releases/ubtech-humanoid-robot-walker-s2-begins-mass-production-and-delivery-with-orders-exceeding-800-million-yuan-302616924.html", source: UBTech / PR Newswire, date: "2025-11-17"}
- {id: 16, title: "AgiBot to take over Swancor in $290M deal", url: "https://en.tmtpost.com/post/7620691", source: TMTPost, date: "2025-07"}
- {id: 17, title: "Proprioceptive Actuator Design in the MIT Cheetah", url: "https://fab.cba.mit.edu/classes/865.18/motion/papers/mit-cheetah-actuator.pdf", source: Wensing et al., IEEE T-RO, date: "2017"}
- {id: 18, title: "Quasi-Direct Drive for Low-Cost Compliant Robotic Manipulation", url: "https://arxiv.org/abs/1904.03815", source: Gealy et al., ICRA, date: "2019"}
- {id: 19, title: "Tesla Optimus hardware specifications", url: "https://optimusk.blog/blog/tesla-optimus-hardware-specs/", source: Optimus technical compilation, date: "2026"}
- {id: 20, title: "Strain wave gearing (efficiency characteristics)", url: "https://en.wikipedia.org/wiki/Strain_wave_gearing", source: Wikipedia, date: "2026"}
- {id: 21, title: "Tesla Q4 2025 earnings call transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/01/28/tesla-tsla-q4-2025-earnings-call-transcript/", source: The Motley Fool, date: "2026-01-28"}
- {id: 22, title: "Tesla Q3 2025 earnings call transcript", url: "https://www.fool.com/earnings/call-transcripts/2025/10/22/tesla-tsla-q3-2025-earnings-call-transcript/", source: The Motley Fool, date: "2025-10-22"}
- {id: 23, title: "Tesla Optimus trips over China export licensing (rare earths)", url: "https://www.theregister.com/2025/04/23/tesla_optimus_china/", source: The Register, date: "2025-04-23"}
- {id: 24, title: "Figure exceeds $1B Series C at $39B valuation", url: "https://www.figure.ai/news/series-c", source: Figure AI, date: "2025-09-16"}
- {id: 25, title: "Figure 02 production work at BMW (pilot retired)", url: "https://www.figure.ai/news/production-at-bmw", source: Figure AI, date: "2025-11-19"}
- {id: 26, title: "Apptronik raises $520M at $5B valuation", url: "https://www.cnbc.com/2026/02/11/apptronik-raises-520-million-at-5-billion-valuation-for-apollo-robot.html", source: CNBC, date: "2026-02-11"}
- {id: 27, title: "GXO signs industry-first multi-year agreement with Agility Robotics", url: "https://www.agilityrobotics.com/content/gxo-signs-industry-first-multi-year-agreement-with-agility-robotics", source: Agility Robotics, date: "2024-06-27"}
- {id: 28, title: "Digit moves over 100,000 totes in commercial deployment", url: "https://www.agilityrobotics.com/content/digit-moves-over-100k-totes", source: Agility Robotics, date: "2025-11"}
- {id: 29, title: "1X NEO is a $20,000 home robot that learns via teleoperation", url: "https://www.engadget.com/ai/1x-neo-is-a-20000-home-robot-that-will-learn-chores-via-teleoperation-040252200.html", source: Engadget, date: "2025-10-29"}
- {id: 30, title: "Boston Dynamics unveils new electric Atlas", url: "https://bostondynamics.com/blog/boston-dynamics-unveils-new-atlas-robot-to-revolutionize-industry/", source: Boston Dynamics, date: "2026-01-05"}
- {id: 31, title: "Unitree G1 specifications (payload)", url: "https://humanoid.guide/product/g1/", source: Humanoid Guide, date: "2026"}
- {id: 32, title: "Why humanoid robots are so hard to scale", url: "https://spectrum.ieee.org/humanoid-robot-scaling", source: IEEE Spectrum, date: "2025-09"}
- {id: 33, title: "Why today's humanoids won't learn dexterity", url: "https://rodneybrooks.com/why-todays-humanoids-wont-learn-dexterity/", source: Rodney Brooks, date: "2025-09-26"}
- {id: 34, title: "Humanoid robots: from demos to deployment", url: "https://www.bain.com/insights/humanoid-robots-from-demos-to-deployment-technology-report-2025/", source: Bain & Company, date: "2025"}
- {id: 35, title: "Humanoid robot market could hit $5 trillion by 2050", url: "https://www.morganstanley.com/insights/articles/humanoid-robot-market-5-trillion-by-2050", source: Morgan Stanley, date: "2025-04-29"}
- {id: 36, title: "Bank of America: 3 billion humanoid robots by 2060", url: "https://fortune.com/2026/03/13/bank-of-america-humanoid-robot-forecast-3-billion-2060/", source: Fortune, date: "2026-03-13"}
- {id: 37, title: "Mineral Commodity Summaries 2025: Rare Earths", url: "https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-rare-earths.pdf", source: U.S. Geological Survey, date: "2025-01-31"}
- {id: 38, title: "Rare Earth Elements — executive summary", url: "https://www.iea.org/reports/rare-earth-elements/executive-summary", source: International Energy Agency, date: "2025"}
- {id: 39, title: "China imposes export controls on medium and heavy rare earths", url: "https://www.hklaw.com/en/insights/publications/2025/04/china-imposes-export-controls-on-medium-and-heavy-rare-earth-materials", source: Holland & Knight, date: "2025-04-04"}
- {id: 40, title: "MP Materials–DoD rare-earth magnet partnership", url: "https://mpmaterials.com/news/mp-materials-announces-transformational-public-private-partnership-with-the-department-of-defense-to-accelerate-u-s-rare-earth-magnet-independence/", source: MP Materials, date: "2025-07-10"}
- {id: 41, title: "FCC adds foreign-made drones and components to Covered List", url: "https://dronelife.com/2025/12/22/fcc-adds-foreign-made-drones-and-components-to-covered-list-citing-national-security-risks/", source: DroneLife, date: "2025-12-22"}
- {id: 42, title: "UniPwn: Unitree robot BLE exploit chain", url: "https://github.com/Bin4ry/UniPwn", source: Makris & Finisterre (disclosure repo), date: "2025-09-26"}
- {id: 43, title: "Unitree G1 vulnerability and telemetry analysis", url: "https://www.helpnetsecurity.com/2025/10/16/unitree-g1-humanoid-robot-vulnerability/", source: Help Net Security (Alias Robotics), date: "2025-10-16"}
- {id: 44, title: "Humanoid ROBOT Act (S.3275) press release", url: "https://www.cassidy.senate.gov/newsroom/press-releases/cassidy-introduces-legislation-to-protect-americans-from-foreign-robots/", source: U.S. Senate (Cassidy), date: "2025-11-21"}
- {id: 45, title: "GUARD Act to ban dangerous Chinese robots", url: "https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-obernolte-mcclellan-introduce-legislation-to-ban-dangerous-chinese-robots", source: U.S. House Select Committee on the CCP, date: "2026-06-03"}
- {id: 46, title: "π0.5: generalization to new environments", url: "https://www.pi.website/blog/pi05", source: Physical Intelligence, date: "2025-04-22"}
- {id: 47, title: "Gemini Robotics On-Device", url: "https://deepmind.google/blog/gemini-robotics-on-device-brings-ai-to-local-robotic-devices/", source: Google DeepMind, date: "2025-06-24"}
- {id: 48, title: "NVIDIA open humanoid robot reference design (Isaac GR00T)", url: "https://nvidianews.nvidia.com/news/nvidia-open-humanoid-robot-reference-design", source: NVIDIA, date: "2026-06-01"}
- {id: 49, title: "Unitree IPO: ~$300M for embodied foundation models", url: "https://www.techflowpost.com/en-US/article/31730", source: TechFlow Post, date: "2026-06-02"}
- {id: 50, title: "Why China's humanoid robot industry is winning the early market", url: "https://techcrunch.com/2026/02/28/why-chinas-humanoid-robot-industry-is-winning-the-early-market/", source: TechCrunch, date: "2026-02-28"}
- {id: 51, title: "BYD 2021 NEV deliveries up 232% YoY", url: "https://technode.com/2022/01/05/byd-ev-2021-deliveries-up-232-year-on-year/", source: TechNode, date: "2022-01-05"}
- {id: 52, title: "DJI market share history", url: "https://www.thedronegirl.com/2018/09/18/dji-market-share/", source: The Drone Girl, date: "2018-09-18"}
- {id: 53, title: "Harmonic Drive Systems (6324.T) share price", url: "https://finance.yahoo.com/quote/6324.T/", source: Yahoo Finance, date: "2026-06-10"}
- {id: 54, title: "Unitree G1 humanoid robot teardown (BOM)", url: "https://robotopian.com/blogs/news/unitree-g1-humanoid-robot-teardown", source: Robotopian, date: "2025"}
- {id: 55, title: "Robot Era raises $200M+ as China humanoid race heats up", url: "https://www.caixinglobal.com/2026-04-27/robot-era-raises-more-than-200-million-as-chinas-humanoid-robot-race-heats-up-102438549.html", source: Caixin Global, date: "2026-04-27"}
- {id: 56, title: "BYD Seagull EV puts global auto execs, politicians on edge (US tariffs)", url: "https://www.cnbc.com/2024/03/22/byd-seagull-ev-puts-global-auto-execs-politicians-on-edge.html", source: CNBC, date: "2024-03-22"}
- {id: 57, title: "Figure AI's Helix-02 robots complete full 8-hour autonomous shifts", url: "https://www.techtimes.com/articles/316632/20260514/figure-ais-helix-02-robots-complete-full-8-hour-autonomous-shifts-humanoid-race-intensifies.htm", source: TechTimes, date: "2026-05-13"}
:::
