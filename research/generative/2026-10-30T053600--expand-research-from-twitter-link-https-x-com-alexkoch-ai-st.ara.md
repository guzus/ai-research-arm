---
eyebrow: RESEARCH · ROBOTICS · HOME SERVICES
title: "Tau Robotics' $30 humanoid cleaner: a teleoperation business selling a data option"
deck: "A recurring subscription for humanoid cleaners went live on 2026-10-29. Read against Tau's own terms, the price, the autonomy claim and the economics look different from the headline."
lede: |
  On 2026-10-29 Alexander Koch, CEO of San Francisco's Tau Robotics, announced that customers can now book the company's humanoid cleaners on a recurring subscription, for up to three hours per cleaning, with a 4× sped-up "first take, uncut" video.[^1] The thread invites an easy reading: robots are now cleaning homes for $30 an hour. This article tests that reading against Tau's own booking page, service terms and privacy policy, against the hardware's published limits, against labour-market data, and against the robot-learning literature that would have to make "imitate, then exceed" true. The finding is narrower and more interesting: Tau is selling teleoperated labour at roughly human-cost parity, and the real product is the right to record the homes it works in.
domain: general
stats:
  - {label: Headline price, value: "$30", unit: "/robot-hr", note: "weekly tier only"}
  - {label: One-off price, value: "$50", unit: "/robot-hr", note: "two robots, $100 per hour"}
  - {label: Paid hours so far, value: "~160", note: "reported, Oct 2026"}
  - {label: Liability cap, value: "$2,500", note: "per claim, Service Terms"}
---

:::kv
- {term: "Direct answer 1", def: "The seed post is a pricing-model change (recurring bookings, up to 3 h), not an autonomy milestone. Tau's own terms state: the robot is not autonomous and a person controls it.[^2]"}
- {term: "Direct answer 2", def: "The widely quoted $30/hour is the weekly-subscription price per robot-hour; a one-off booking is $50 per robot-hour on the current booking page.[^3]"}
- {term: "Direct answer 3", def: "Even at $30, the arithmetic only works if one operator supervises several robots; at one operator per robot the labour cost alone exceeds revenue (ARA calculation in section 04)."}
- {term: "Direct answer 4", def: "Footage is kept and used to train Tau's models under a perpetual licence, and faces are not blurred.[^2,4] The business is as much a data-acquisition channel as a cleaning service."}
:::

## 01. The seed post is a pricing change, and the price is not what it seems

**Thesis: the headline figure of $30 an hour describes the cheapest tier of a two-robot visit, not a per-visit price.**

Koch's post says customers can book "on a recurring subscription, for up to 3 hours per cleaning", that the video is "first take, uncut" at 4× speed, and that a reply carries 1× footage.[^1] It links to Tau's booking page. The post is the third public pricing state of a service that launched in July: press coverage at the 2026-07-28 launch reported an invite-only service at $30 per hour,[^6] and Hoodline's launch write-up described one humanoid per appointment.[^8]

The booking page today tells a different story. It sells "two humanoids, every visit", and for a one-hour visit quotes $60 per visit weekly, $80 every two weeks, $90 every four weeks, and $100 one-time; a repeating clean is described as a subscription that can be cancelled any time, and booking requires an invite code.[^3] Tau's Service Terms, last updated 2026-10-24, state the standard fee as "$50 per humanoid per hour" and normally send two humanoids, so $100, $200 or $300 for one, two or three hours.[^2] Dividing by two robots gives the per-robot-hour price at each cadence.

:::bars
- {label: "Weekly subscription", value: "$30", pct: 60}
- {label: "Every 2 weeks", value: "$40", pct: 80}
- {label: "Every 4 weeks", value: "$45", pct: 90}
- {label: "One-time booking", value: "$50", pct: 100}
:::

:::source
Tau booking page and Service Terms, fetched 2026-10-30; per-robot-hour values are ARA arithmetic (visit price ÷ two robots), one-hour visits.
:::

Two things follow. First, "$30 an hour" in headlines is real but conditional: it is the weekly-subscriber price per robot-hour, and a customer who books once pays 67% more per robot-hour. A subscription is therefore a retention device as much as a convenience, which is consistent with Tau's stated interest in volume (it has said it wants about 1,000 cleanings a week in San Francisco by 2027).[^7] Second, the terms and the booking page disagree about whether a subscription exists. The Service Terms describe a full charge at booking and contain no recurring-billing clause,[^2] while the booking page defines a repeating clean as a subscription billed per visit.[^3] That is an ordinary lag between a live product page and a legal document, but a buyer reading only the terms would not learn that the product exists.

Counterpoint: the 2- and 3-hour prices are not listed on the booking page, so the "up to 3 hours" tier cannot be priced from public text beyond the terms' $300 one-off figure.[^2,3] Why it matters: every downstream calculation in this article depends on which of these per-robot-hour prices applies.

## 02. Teleoperation is the product

**Thesis: Tau's own documents and CEO describe human-controlled robots with an AI assist, and the autonomy is a roadmap, not a feature.**

The Service Terms say it in two sentences: "The robot is not autonomous. A person is controlling it." and "Every cleaning is recorded. Your operator watches live."[^2] Koch told The Register that each humanoid is jointly controlled by a human operator and AI, that "the balance varies by task", and that a human is always guiding the AI policy, sometimes directly and sometimes through higher-level instructions.[^6] Tau's own site adds that a supervisor travels with the robots and can take manual control, and that children needing supervision require an adult to be present.[^5]

The roadmap is explicit. In a CBS interview Koch said the robots will first be trained to imitate human performance and then to exceed it, and that technicians would be phased out around 2028–29.[^7] The Register reports he compares the human to a safety backstop in autonomous driving.[^6] None of these sources gives a quantified operator-to-robot ratio, and an attempt to find any published intervention rate for Tau came back empty. The only scale figure available is secondary: a MarketWatch-derived summary puts the fleet at about eight robots with roughly 160 paid robot-hours across nearly 100 cleanings, all teleoperated, and notes the robots needed help with stairs and a smooth glass surface.[^9]

:::timeline
- {date: "2026-07-28", headline: "Invite-only launch at $30/hour", body: "Koch announces the San Francisco service; The Register interviews him the next day.[^6]"}
- {date: "2026-07-28", headline: "FCC lists foreign-produced robots", body: "Public Notice DA 26-786 adds advanced robotic devices to the Covered List.[^15]"}
- {date: "2026-10-17", headline: "~160 paid hours, ~100 cleanings", body: "Secondary summary of MarketWatch reporting.[^9]"}
- {date: "2026-10-24", headline: "Service Terms updated", body: "Recording, training licence, $2,500 cap, arbitration.[^2]"}
- {date: "2026-10-29", headline: "Recurring subscription announced", body: "Seed post: up to three hours per cleaning.[^1]"}
:::

The hedging language matters, because the product is easy to over-read. The company calls the service "operated by humans and artificial intelligence",[^8] and its marketing page lists dusting, wiping, toilet cleaning, vacuuming and mopping across bathrooms, kitchens, bedrooms and offices.[^5] The booking page, however, leaves bathrooms and bedrooms off-limits by default unless the customer asks for them.[^3] That default is itself informative about where the operators and robots are least confident.

Counterpoint: teleoperation is not a fraud; Tau says so plainly in the legal document the customer accepts. The risk is in the surrounding commentary, where "humanoid cleaners" is routinely read as "autonomous humanoids". Why it matters: the autonomy gap determines whether this is a robotics company or a staffing company with expensive equipment.

## 03. The hardware: a modified G1, a 2-hour battery, and a $50k bill of materials

**Thesis: the reported hardware cost is about 3.7× the base robot's list price, and a three-hour session needs more than one battery.**

No Tau document I could fetch names the robot. Press and trade coverage identify it as a visibly modified Unitree G1;[^10] CBS quotes Koch saying the robots cost $50,000 each to make and that "the camera system, the networking and the computers are all our own".[^7] Bloomberg Línea, relaying the same interview, reports a claimed payback of under a year at 40 hours a week;[^11] humanoid.guide, summarising MarketWatch, cites about $55,000 per unit for the G1 bodies before Tau's modifications, which conflicts with Unitree's list price and so is not independent corroboration of the $50,000.[^9]

Unitree's own spec page lists the G1 at about 1.32 m tall and about 35 kg, 23 degrees of freedom in the base version, an arm payload of about 2 kg that "varies greatly with arm extension posture", a 9,000 mAh battery and roughly two hours of runtime; the dexterous three-finger hand is an optional extra on the EDU model.[^12] The list price was $16,000 at the May 2024 launch,[^13] and Unitree's page now shows about $13.5k for the base unit.[^12] A reseller lists the pack at 46.8 V nominal and 421.2 Wh,[^14] which implies an average draw of roughly 210 W over the rated two hours (ARA calculation). A three-hour visit at that draw needs about 630 Wh, or around 1.5 packs, before accounting for arms-extended cleaning or teleoperation radios. Tau has not said how it handles this: whether by battery swaps, a dock or shorter active time.

:::slope(left-label="G1 list price", right-label="Reported Tau build cost", unit=$k)
| Item | G1 list | Tau build |
|------|---------|-----------|
| Cost per robot | 13.5 | 50 |
:::

The gap is not itemised by any source. A plausible reading is that Tau's custom heads, cameras, compute, wrist cameras and grippers account for most of it,[^7,10] but this is inference. The standard G1 ships without a hand,[^12] so the cleaning end-effectors are in-house.

Counterpoint: if the true cost is closer to the list price, the economics improve sharply; if the figure is a development-unit cost with only eight units built, volume production would cut it. Why it matters: capital cost per robot is the largest line in the break-even calculation below.

## 04. Unit economics: a labour-cost parity play, not a labour-cost saving

**Thesis: at $30 per robot-hour the service roughly matches the loaded cost of a San Francisco human cleaner before any robot capital, so profit depends on operator leverage and robot life.**

Start with the human benchmark. The BLS Occupational Employment survey shows the national median for maids and housekeeping cleaners (SOC 37-2012) at $16.08 an hour in May 2023, with 836,230 jobs;[^19] a wage aggregator mirroring the May 2025 data reports a $17.07 median and 860,670 jobs.[^20] I did not find a fetchable San Francisco-metro wage or a dated Bay Area customer-price series, so the comparison below is against the national wage and should be read as a floor; San Francisco wages are higher.
Now the robot. Define revenue per robot-hour R = $30, a robot price P, operator loaded cost per hour O shared across N robots, and variable cost V per robot-hour. Break-even service hours are P ÷ (R − O/N − V). Using an assumed $3 variable cost and an assumed $37.50 loaded San Francisco operator cost (a $30 wage with a 25% load; both are ARA assumptions, not sourced figures):

| Operator setup | Operator cost per robot-hour | Break-even hours, P = $16k | Break-even hours, P = $50k |
|---|---|---|---|
| One operator per robot | $37.50 | never | never |
| One operator per 3 robots | $12.50 | 1,103 | 3,448 |
| One operator per 5 robots | $7.50 | 821 | 2,564 |
| Offshore operator at $2/hr, 1:1 | $2.00 | 640 | 2,000 |

:::note
All rows are ARA calculations. The $3 variable cost, the $37.50 loaded operator cost, and the absence of any sourced humanoid service life are assumptions. Tau's operators are on-site San Francisco employees, not offshore, so the last row is a counterfactual.[^4,6]
:::

Three conclusions survive the uncertainty. With one operator per robot, each billed hour loses money. Tau's operators work on-site in San Francisco, per its privacy policy, so the offshore labour thesis does not describe this company;[^4] the often-cited Manila convenience-store operators earn up to about $300 a month but supervise up to 50 robots on a far simpler shelf-stocking task.[^23] And the payback claim reported by Bloomberg Línea (under a year) is revenue-only: $50,000 ÷ ($30 × 40 hours × 52 weeks) is about 0.80 years at full utilisation with no operator cost, while the 3:1 leverage case needs 3,448 billed hours, which is roughly 1.7 years at 40 billed hours a week.[^11]

The actual utilisation is far below that. Roughly 160 paid hours over a period of weeks across eight robots is a few hours per robot.[^9] That is consistent with the early, paid-field-test character of the launch.[^8,9] The price therefore appears to buy two things: cleaning labour and training data. The footage is the asset.

Counterpoint: depreciation per service hour falls fast with robot life. At $50k, a 2,000-hour life consumes $25 of every $30; at 10,000 hours it consumes $5 (ARA calculation, with the lifetimes as assumptions). If robot reliability proves much better than assumed, or the bill of materials falls toward list price, the picture changes. Why it matters: the decisive variable is operator leverage, and no public number exists for it.

## 05. Regulation and supply chain: the FCC listing and the G1's security record

**Thesis: the new FCC rule bites future models rather than the existing fleet, but it adds a new-model risk to a business built on one vendor's body.**

On 2026-07-28 the FCC added "foreign-produced advanced robotic devices", including humanoids and quadrupeds, to its Covered List, with exceptions for devices granted a Conditional Approval by the Department of War (Public Notice DA 26-786).[^15] The notice does not name Unitree, and equipment is listed by place of production rather than company nationality.[^15] Trade analysis reports the practical effect as barring new equipment authorisations rather than the sale of already-authorised models, and that Unitree authorised several products, including the R1, H2 and A2, in the weeks before the rule; the same source puts the US at 13.3% of Unitree's 2025 revenue.[^16] I could not confirm the G1's own authorisation date or whether Unitree has applied for a Conditional Approval, which is the key open item.

The G1 also has a documented security record. A 2025 arXiv assessment of the platform found persistent telemetry connections to external servers that transmit robot state and sensor data, and static encryption keys in the configuration;[^17] the video stream is reported as disabled in that analysis, so it does not show camera footage leaving a G1. IEEE Spectrum covered "UniPwn", a Bluetooth Low Energy flaw affecting the Go2, B2, G1 and H1 that allowed root takeover through command injection and hardcoded keys; Unitree reportedly said most fixes were done by late September 2025, but I could not confirm the fix status for G1 firmware in the field.[^18] Tau says its cameras, networking and compute are its own,[^7] which would reduce, but not remove, exposure to a vendor-side data path: the body and its low-level control remain Unitree's.

Counterpoint: the FCC action is category-wide, not a Unitree blacklist, and existing authorised models stay lawful to sell.[^15,16] Tau's exposure is as much to a future successor robot as to today's units. Why it matters: a home-cleaning fleet that cannot easily add newer hardware inherits a refresh-cycle risk its competitors with domestic hardware may avoid.

## 06. The legal wrapper: recording, liability and an unsettled standard

**Thesis: Tau's terms transfer a great deal of risk and data rights to the customer, in a legal environment with no standard that squarely covers an in-home humanoid.**

The Service Terms state that Tau keeps the footage and uses it to train its models, under a licence over "footage, telemetry, and other data" that is described as perpetual; liability for a cleaning is capped at $2,500, with personal injury caused by negligence, fraud and wilful injury carved out; there is no insurance clause; and disputes go to AAA arbitration in San Francisco with class actions barred and a 30-day opt-out.[^2] The Service Privacy Policy says the robot's head and wrist cameras record continuously, faces are not blurred, microphones are disabled, no facial recognition is used, video is kept indefinitely unless the customer asks for deletion (with Tau unable to un-train a model), and a third-party labelling vendor has view-only access.[^4] The company's separate website privacy policy covers only the public site and points in-home recording to the Service Privacy Policy.[^4]

Standards do not fill the gap. A summary of the ISO catalogue describes ISO 25785-1 as a draft for dynamically stable industrial mobile robots that explicitly leaves non-industrial settings to ISO 13482, which is itself flagged for revision;[^41] ANSI/A3 R15.06-2025 is industrial in scope. The net position as of this research is that no consensus standard squarely covers a legged, teleoperated humanoid in a home. On privacy, California's all-party-consent recording rules (Penal Code §632) make Tau's recorded-visit disclosure its main defence, which is my legal inference rather than a sourced finding. Illinois biometric-privacy suits filed in October 2026 against two remote-operated delivery-robot firms show the plaintiff-side theory, though Tau currently operates only in San Francisco.[^40] I did not find a ruling on in-home robot recording.

Counterpoint: customers choose the service knowing it records, and Tau's explicit disclosure and arbitration terms are common for in-home services. Others in the home, such as guests, children and neighbours, did not accept the terms; the terms reportedly address this through an indemnity clause.[^2] Why it matters: the model's data engine depends on customers accepting terms that a first serious incident could test.

## 07. Can teleoperation data bootstrap autonomy?

**Thesis: the literature supports "imitate" at modest scale and diversity, but "exceed" has come from reinforcement learning with corrections on narrow tasks, and no public source shows operator supervision falling toward zero.**

Imitation from teleoperated demonstrations works with surprisingly little data when it is co-trained with other data. Mobile ALOHA found that co-training with static-arm data raised whole-task success on tasks such as wiping wine from 50% to 95% and rinsing a pan from 0% to 80%, using about 50 demonstrations per task mixed with an 825-episode static pool.[^24] For household generalisation specifically, Physical Intelligence's pi0.5 reports cleaning kitchens and bedrooms in entirely new homes, with about 400 hours of mobile-manipulator data from roughly 100 homes making up a small share of a mostly non-household mixture.[^25] A scaling study found generalisation follows a power law in the number of training environments and objects rather than raw demonstration count, and reached about 90% zero-shot success on two simple tasks in new environments.[^26]

Against that, Tau's reported 160 paid hours is well under the 400 hours and 100 homes where pi0.5 became competitive (ARA comparison: 160 ÷ 400 = 0.4).[^9,25] Two points temper any read-across. The public alternatives are also accumulating: the HIW-500 dataset offers over 500 hours of G1 whole-body teleoperation across 12 real homes under a CC BY 4.0 licence,[^30] so raw G1 teleop hours are not exclusive to Tau; and Koch's own open-source Koch v1.1 arm costs about $477 for leader and follower, making data collection cheap for everyone.[^39] The scarce input is diverse homes plus a good policy, not teleoperation itself.

"Exceed" is a different mechanism. The pi*0.6 work reports that on-robot reinforcement learning with expert interventions more than doubled throughput and roughly halved failures on the hardest tasks, with each box-assembly iteration mixing 600 autonomous trials and 360 with expert interventions.[^27] Intervention-learning theory, such as RLIF, shows policies can outperform suboptimal experts using only intervention signals.[^28] But I found no public time series of interventions per robot-hour in a deployment, so the claim that supervision cost falls toward zero is unevidenced. Industry practice is mixed: Figure's Helix was trained on about 500 hours of teleoperated data,[^29] and 1X's NEO uses remote experts for unfamiliar chores.[^32]

:::compare
- {role: "LOWEST", name: "Tau paid robot-hours (reported)", value: "~160"}
- {role: "HIGHEST", name: "pi0.5 mobile-manipulator data", value: "~400 h"}
- {role: "SUBJECT", name: "HIW-500 public G1 teleop data", value: "500+ h"}
:::

Counterpoint: customer homes are exactly the diversity that labs struggle to buy, and a paid-for-by-customer data channel is cheaper than hiring collectors. Why it matters: Tau's strategic case is that the subscription finances the data flywheel; the evidence says the flywheel needs hundreds of homes, not eight robots.

## 08. The competitive field: nobody is delivering autonomous household cleaning at scale

**Thesis: every comparable model either keeps a human in the loop or has not yet delivered, so Tau's disclosed teleoperation makes it the transparent end of a field of unverified autonomy claims.**

1X NEO is priced at $20,000 or $499 a month;[^31] unfamiliar chores are handled by a remote expert, and a delivery tracker's status, stamped 2026-08-07, found no confirmed customer receipts against a stated 2026 shipping window; I did not find a newer confirmation.[^33,32] Gatsby, a San Francisco service founded in 2026, charges a flat $150 per clean and claims the first consumer humanoid cleaning in the US on 2026-05-14, but its page says nothing about teleoperation, so its autonomy claim is unverified.[^34] Weave announced Isaac 1 at $7,999 or $449 a month with a teleoperation fallback and deliveries starting in fall 2026.[^37] Sunday Robotics raised $165 million at a $1.15 billion valuation in March 2026 to build household robots.[^36] Figure's CEO floated a lease of about $600 a month for its Figure 03 in a podcast, and I found no home deliveries.[^38] In China, X Square Robot and 58.com send a human cleaner with a wheeled dual-arm robot, splitting structured tasks to the robot and judgment-driven work to the person.[^35]

| Company | Model | Price | Autonomy | Delivery status |
|---|---|---|---|---|
| *Tau Robotics | Service | $30–50 per robot-hour | Teleoperated, stated | Live in San Francisco, small scale |
| Gatsby | Service | $150 per clean | Claimed, unverified | Live in San Francisco |
| 1X NEO | Product | $20k or $499/mo | Remote expert for some chores | No confirmed deliveries |
| Weave Isaac 1 | Product | $7,999 or $449/mo | Autonomous with teleop fallback | Announced for fall 2026 |
| X Square / 58.com | Human plus robot | Not found | Partial | Beijing pilot |

Tau's per-hour price is the only explicit labour-substitution price point in the set, and it is priced near the human wage, not far below it. Gatsby's flat $150 cannot be converted to an hourly price because its page gives no duration.[^34]

Counterpoint: product-side players have larger war chests and can wait for autonomy; a service-side player with $2.6 million of reported pre-seed funding cannot.[^8,36] Why it matters: the question for Tau is whether the operating loss per teleoperated hour is financed long enough to cross the autonomy threshold.

## 09. What could break the thesis

**Thesis: the strongest reading of Tau is an options play on autonomy, and four risks could make it worthless.**

- **Funding and runway.** Reported funding is $2.6 million pre-seed from one outlet, with no named investors in any fetched source;[^8] at a fully loaded San Francisco operator cost, each unleveraged hour loses money (section 04).
- **Autonomy plateau.** The evidence for exceeding human performance comes from narrow tasks with heavy intervention budgets,[^27] and the Helix, ALOHA and pi0.5 results were produced in lab or curated settings rather than customer homes.[^24,25,29]
- **Regulatory and supply risk.** The FCC rule makes newer foreign-made models harder to authorise,[^15] and the G1 has documented telemetry and Bluetooth weaknesses.[^17,18]
- **Legal exposure.** A capped liability, no stated insurance, continuous video and an indefinite retention policy sit in a legal environment without a settled standard.[^2,4,41]

Red-team pass: 3/3 top claims unbroken (the not-autonomous statement, the $30-versus-$50 per-robot-hour reading, and the footage and no-face-blur terms); the only nuance found is that launch-era press quoted $30 for one robot, the earlier pricing state described in section 01.

Evidence that would change my view: a published operator-to-robot ratio below one, an intervention rate that falls over deployment time, a named investor with a larger cheque, or a customer-home dataset of several hundred homes. Absent these, the careful description is a disclosed teleoperation service with a plausible data strategy.

Two limits of this research apply. I could not read the seed thread's replies or the original X posts directly (the platform returned HTTP 402), and I recovered the post text through public mirrors. And several secondary figures, notably the $50,000 and $55,000 robot costs, the roughly 160 paid hours and the funding amounts, trace to a single interview or outlet each and should be read as company-reported.[^7,8,9] The CEO's own price-per-hour claim has already drifted across three documents inside four months.

:::references
- {id: 1, title: "Alexander Koch on X: recurring subscription for humanoid cleaners", url: "https://x.com/alexkoch_ai/status/2115871971393331663", source: "X / Tau Robotics CEO", date: "2026-10-29"}
- {id: 2, title: "Tau Robotics Service Terms", url: "https://tau-robotics.com/service-terms.html", source: "Tau Robotics", date: "2026-10-24"}
- {id: 3, title: "Tau Robotics booking page", url: "https://www.tau-robotics.com/book", source: "Tau Robotics", date: "2026-10-30"}
- {id: 4, title: "Tau Robotics Service Privacy Policy", url: "https://tau-robotics.com/service-privacy.html", source: "Tau Robotics", date: "2026-10-24"}
- {id: 5, title: "Tau Robotics home page and FAQ", url: "https://tau-robotics.com", source: "Tau Robotics", date: "2026-10-30"}
- {id: 6, title: "The Register on Tau Robotics humanoid cleaning at $30 an hour", url: "https://assets.theregister.com/2026/07/29/202621/", source: "The Register", date: "2026-07-29"}
- {id: 7, title: "CBS News: Tau Robotics humanoid AI cleaning robots in San Francisco", url: "https://www.cbsnews.com/news/tau-robotics-humanoid-ai-cleaning-robots-san-francisco/", source: "CBS News", date: "2026-08"}
- {id: 8, title: "S.F. startup wants its $30-an-hour robots cleaning your home", url: "https://hoodline.com/2026/08/s-f-startup-wants-its-30-an-hour-robots-cleaning-your-home/", source: "Hoodline", date: "2026-08-01"}
- {id: 9, title: "Tau Robotics humanoids clean homes for $30 an hour, with help", url: "https://humanoid.guide/tau-robotics-humanoids-clean-homes-for-30-an-hour-with-help/", source: "humanoid.guide", date: "2026-10-17"}
- {id: 10, title: "Tau Robotics launches $30 hour humanoid cleaning service amidst FCC ban turmoil", url: "https://www.humanoidsdaily.com/news/tau-robotics-launches-30-hour-humanoid-cleaning-service-amidst-fcc-ban-turmoil", source: "Humanoids Daily", date: "2026-08-04"}
- {id: 11, title: "Robots humanoides ya limpian casas por US$30 la hora en San Francisco", url: "https://www.bloomberglinea.com/tecnologia/robots-humanoides-ya-limpian-casas-por-us30-la-hora-en-san-francisco-asi-funciona-el-servicio/", source: "Bloomberg Linea", date: "2026-09-11"}
- {id: 12, title: "Unitree G1 specifications", url: "https://www.unitree.com/g1", source: "Unitree", date: "2026-10-30"}
- {id: 13, title: "Unitree unveils G1 humanoid for $16k", url: "https://www.therobotreport.com/unitree-robotics-unveils-g1-humanoid-for-16k/", source: "The Robot Report", date: "2024-05-15"}
- {id: 14, title: "Unitree G1 9000 mAh battery listing", url: "https://botland.store/akcesoria-do-robotow/28456-akumulator-do-robotow-unitree-g1-9000mah-5907085527444.html", source: "Botland (reseller)", date: "2026-10-30"}
- {id: 15, title: "FCC Public Notice DA 26-786: Covered List update, foreign-produced advanced robotic devices", url: "https://docs.fcc.gov/public/attachments/DA-26-786A1.txt", source: "FCC", date: "2026-07-28"}
- {id: 16, title: "US bans new Chinese humanoid robots; the biggest maker got in first", url: "https://www.tech-ish.com/2026/08/10/us-bans-new-chinese-humanoid-robots-the-catch-the-biggest-maker-got-in-first/", source: "Tech-ish", date: "2026-08-10"}
- {id: 17, title: "Cybersecurity assessment of the Unitree G1 humanoid", url: "https://arxiv.org/html/2509.14096", source: "arXiv 2509.14096", date: "2025-09-17"}
- {id: 18, title: "Unitree robot exploit (UniPwn)", url: "https://spectrum.ieee.org/unitree-robot-exploit", source: "IEEE Spectrum", date: "2025-09-20"}
- {id: 19, title: "Maids and housekeeping cleaners, SOC 37-2012, May 2023", url: "https://www.bls.gov/oes/2023/may/oes372012.htm", source: "US Bureau of Labor Statistics", date: "2023-05"}
- {id: 20, title: "Maids and housekeeping cleaners wage data (OEWS May 2025 mirror)", url: "https://wagedex.com/jobs/maids-and-housekeeping-cleaners", source: "Wagedex", date: "2025-05"}
- {id: 23, title: "Remote robot jobs surge: Manila operators guide store machines", url: "https://holistic.news/en/remote-robot-jobs-surge-humans-guide-store-machines/", source: "Holistic News", date: "2026"}
- {id: 24, title: "Mobile ALOHA: learning bimanual mobile manipulation with low-cost whole-body teleoperation", url: "https://arxiv.org/abs/2401.02117", source: "arXiv 2401.02117", date: "2024-01"}
- {id: 25, title: "pi0.5: a vision-language-action model with open-world generalization", url: "https://arxiv.org/html/2504.16054", source: "arXiv 2504.16054", date: "2025-04"}
- {id: 26, title: "Data scaling laws in imitation learning for robotic manipulation", url: "https://arxiv.org/abs/2410.18647", source: "arXiv 2410.18647", date: "2024-10"}
- {id: 27, title: "pi*0.6: a VLA that learns from experience", url: "https://arxiv.org/html/2511.14759", source: "arXiv 2511.14759", date: "2025-11"}
- {id: 28, title: "RLIF: interactive imitation learning as reinforcement learning", url: "https://arxiv.org/abs/2311.12996", source: "arXiv 2311.12996", date: "2023-11"}
- {id: 29, title: "Figure Helix: a vision-language-action model for generalist humanoid control", url: "https://www.figure.ai/news/helix", source: "Figure AI", date: "2025-02"}
- {id: 30, title: "HIW-500-LeRobot dataset card", url: "https://huggingface.co/datasets/BitRobot/HIW-500-LeRobot", source: "Hugging Face", date: "2026"}
- {id: 31, title: "1X NEO home robot", url: "https://1x.tech/discover/neo-home-robot", source: "1X Technologies", date: "2026-10-30"}
- {id: 32, title: "1X NEO helper robot and VR telepresence", url: "https://roadtovr.com/helper-robot-neo-vr-telepresence/", source: "Road to VR", date: "2025-10-30"}
- {id: 33, title: "1X NEO delivery watch", url: "https://offbrandhuman.com/blog/1x-neo-delivery-watch", source: "Off Brand Human", date: "2026-10-19"}
- {id: 34, title: "Gatsby humanoid cleaning", url: "https://www.aronfrishberg.com/gatsby", source: "Founder site", date: "2026-05-14"}
- {id: 35, title: "Robot-and-human cleaning team service reaches Beijing", url: "https://english.news.cn/20260419/fd23ea06d1c74cd288fb67d9d08f3069/c.html", source: "Xinhua", date: "2026-04-19"}
- {id: 36, title: "Humanoid robotics maker Sunday reaches $1.15B valuation", url: "https://techcrunch.com/2026/03/12/humanoid-robotics-maker-sunday-reaches-1-15b-valuation-to-build-household-robots/", source: "TechCrunch", date: "2026-03-12"}
- {id: 37, title: "Weave Robotics Isaac 1", url: "https://mikekalil.com/blog/weave-robotics-isaac-1/", source: "Mike Kalil", date: "2026-07-03"}
- {id: 38, title: "Figure CEO says humanoid robots could soon enter homes at $600 a month", url: "https://zerohedge.com/technology/figure-ceo-says-humanoid-robots-could-soon-enter-homes-600-month", source: "ZeroHedge", date: "2026-05-06"}
- {id: 39, title: "Koch v1.1 low-cost leader-follower arm", url: "https://github.com/jess-moss/koch-v1-1", source: "GitHub", date: "2024"}
- {id: 40, title: "Serve, Coco delivery robots unlawfully capture biometric scans, class action claims", url: "https://www.classaction.org/news/serve-coco-delivery-robots-unlawfully-capture-biometric-scans-in-chicago-class-action-lawsuits-claim", source: "ClassAction.org", date: "2026-10-09"}
- {id: 41, title: "ISO/CD 25785-1: safety requirements for dynamically stable industrial mobile robots", url: "https://www.iso.org/standard/91469.html", source: "ISO", date: "2026"}
:::
