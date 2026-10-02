---
eyebrow: DEEP RESEARCH · INFRA · SPACE COMPUTE
domain: infra
title: "Suncatcher reaches orbit: what one four-TPU satellite can and cannot settle about space-based AI compute"
deck: Google has turned a 2025 design paper into hardware in orbit. Read its published numbers closely, though, and the flight tests the easy parts of orbital compute and leaves the decisive ones for 2027 and beyond.
lede: |
  On 1 October 2026 a SpaceX Falcon 9 lifted off from Vandenberg carrying 130 payloads [^7]. One was a refrigerator-sized Planet satellite with Google tensor processing units inside. Hours later Google said it had "confirmed contact with the satellite and it is operating as expected" [^1]. That is the first time Google has put its own AI accelerators in orbit, and the pre-launch headlines spoke of AI data centers in space. The project's lead called the same flight "a very minimal test" [^6]. Both are true, and the gap between them is the subject of this article. We take Google's own design paper, its radiation-beam data and the independent cost models, and sort what four chips running in roughly 15-minute bursts can actually measure from what they structurally cannot [^5,6].
stats:
  - {label: TPUs on board (reported), value: "4", note: "per press reports"}
  - {label: Solar power (reported), value: "~1", unit: kW}
  - {label: Design cluster, value: "81", unit: sats, note: "100–200 m apart, MODELED"}
  - {label: "Launched power at $200/kg", value: "$810", unit: "/kW/yr", note: "vs $14,700 today"}
---

:::callout(kind=info, label="Short answer")
- **Can settle:** whether TPUs survive launch loads and run in orbit. It can also check the ground-predicted silent-data-corruption rate to within roughly 2–3x, and confirm a heat-pipe and radiator design at about 1 kW [^2,5].
- **Cannot settle:** Tbps laser links between satellites flying 100–200 m apart (that test is a two-satellite flight in 2027), rare crash and hard-failure rates across a fleet, radiator mass at gigawatt scale, or the economics [^2,5].
- **Economics:** Google's own paper says only that $200/kg launch brings launched power near terrestrial energy cost [^5]. Servers alone run about $5,000/kW/yr on the ground [^29]. Independent models put orbit at 1.5–4.4x ground cost today. Their optimistic or 2040-era scenarios narrow that toward parity [^32,33].
- **Status as of 2026-10-03:** Google has confirmed contact with the satellite, which is still being commissioned. No TPU data has been published [^1,9].
:::

## 01. What actually reached orbit

What flew on October 1 is a deliberately minimal component test: Google's chips riding in a borrowed Planet bus. As of 2026-10-03 Google has confirmed contact with that bus, not any result from its TPUs [^1,15]. The distinction matters because almost everything that would make or break orbital AI compute sits downstream of the payload, and none of it has been reported yet [^1].

:::kv
- {term: Vehicle, def: "SpaceX Falcon 9, Transporter-18 rideshare, Vandenberg; liftoff 11:32 a.m. PT on 1 Oct 2026 [^7]"}
- {term: Payloads on the rideshare, def: "130 [^7]"}
- {term: Builder, def: "Planet; Owl bus, per Planet's CFO in December 2025 [^11]"}
- {term: Payload, def: "Four TPUs (reported); Google's own posts give no chip count or generation [^14,15]"}
- {term: Power, def: "About 1 kW of solar (reported, not first-party) [^14]"}
- {term: Duty cycle, def: "Roughly 15-minute Gemma runs before a cooldown (reported) [^6]"}
- {term: Orbit, def: "Sun-synchronous low Earth orbit; altitude not disclosed [^6]"}
- {term: Planned operations, def: "One year [^6]"}
- {term: "Status as of 2026-10-03", def: "Contact confirmed and 'operating as expected' [^1]; Planet commissioning under way [^9]"}
:::

### A borrowed bus, by design

The satellite was not purpose-built around the chips. Benzinga reported that "to speed things up, Google installed its chips in a ready-made Planet Labs satellite," and that the spacecraft is named MVP [^15]. In December 2025 Planet's CFO told investors the work used the Owl bus, and CEO Will Marshall said "a couple of demo satellites" were on contract [^11]. Project lead Travis Beals described the flight to NPR as "a very minimal test." Planet gets the satellite up and running first, then Google powers up and exercises the TPUs [^6]. NPR also reported that radiators are among the heaviest components, an early hint that the binding constraint is heat rather than electricity [^6].

Suncatcher was one of 20 Planet satellites on the launch, alongside Tanager-2 and 18 SuperDoves. Planet counts it as its 40th launch, with 718 satellites built and delivered [^8]. It reported initial contact with Tanager-2, the Suncatcher prototype and two SuperDoves, and said commissioning had begun [^9]. In engineering terms, the hardware is a payload riding a mature, high-volume bus. That removes most bus risk from the experiment and leaves the TPU as the variable under test [^8,15].

### What Google has and has not said

Google's October 1 post is precise about scope. "Our team has confirmed contact with the satellite and it is operating as expected," Beals wrote. He promised data "over the coming weeks" on "how our TPUs handle the physical stress of spaceflight and the radiation and thermal extremes of space" [^1]. The same post announced that the team's peer-reviewed paper is now published in *Joule* [^1]. Nothing in it reports a TPU power-on, a completed inference run or a single radiation upset count [^1].

The September 24 facts post sets out what the hardware had to survive first: roughly 10 minutes of launch, up to 10 g of sustained acceleration and component loads of 50 to 100 g. The design had already been through thermal-vacuum chamber testing on the ground [^2]. The post also says future satellites will carry "dozens of TPU chips," which puts this flight well below any useful compute node [^2]. Google's own leadership frames it the same way: Google SVP James Manyika told Engadget, "We don't expect … anything usefully operational in the next few years" [^14].

:::timeline
- {date: 2025-11-04, headline: "Suncatcher announced", body: "Planet to launch two prototype satellites by early 2027 [^3,10]."}
- {date: 2025-12-10, headline: "Planet names the bus", body: "CFO cites the Owl bus; CEO says 'a couple of demo satellites' are on contract [^11]."}
- {date: 2026-03-19, headline: "Accounting disclosed", body: "Planet says the partnership is contra-R&D [^12]."}
- {date: 2026-06-17, headline: "Design paper v2", body: "Revised arXiv design paper posted [^5]."}
- {date: 2026-09-24, headline: "Facts post", body: "TPUs launching 'next week'; two laser-linked satellites planned for 2027 [^2]."}
- {date: 2026-10-01, headline: "Launch and contact", body: "Transporter-18 lifts off; Google confirms contact and announces the Joule paper [^1,7]."}
:::

### The plan changed shape

In November 2025 the stated plan was two prototype satellites by early 2027 [^3]. By September 2026 it had become one single-satellite test now, followed by two laser-linked satellites in 2027 [^2]. Neither company has explained the change. Our reading is that the program was re-sequenced so that chip-level qualification flies before the inter-satellite link experiment, rather than putting both risks on the same pair of spacecraft [^2,3]. That ordering is sound engineering. It also means the link question, which section 05 treats as decisive, has been deferred rather than answered [^2].

### The strongest skeptical reading

The fairest reading is that this is a qualification flight, and bus contact is not payload success [^1]. A healthy Owl bus shows that Planet's spacecraft works, which 718 deliveries already suggested [^8]. It says nothing yet about TPU upset rates, throttling or thermal margins [^1]. Why this matters: read every later claim here about what Suncatcher has proven against this baseline. That is four reported chips, about a kilowatt and 15-minute bursts, with no TPU data published as of 2026-10-03 [^1,6,14].

## 02. Radiation: the one question a single flight can actually answer

Four TPUs flown for months can check the ground-predicted silent-data-corruption rate to within a factor of about two to three. They cannot bound the rare crash, latch-up and hard-failure rates that decide whether a fleet is viable. The ground baseline is unusually specific: Google put Trillium TPUs through a 67 MeV proton beam at UC Davis's Crocker Nuclear Laboratory and published per-rad error rates [^2,5]. Every figure below was MEASURED in that beam unless it is marked MODELED or labelled as ARA's own arithmetic.

:::stats
- {label: HBM irregularity onset, value: "2", unit: krad(Si), note: "MEASURED, proton beam"}
- {label: Max dose tested, value: "15", unit: krad(Si), note: "one chip, no hard failures"}
- {label: Shielded 5-year dose, value: "750", unit: rad(Si), note: "MODELED, ~150 rad/yr behind 10 mm Al-equiv."}
- {label: HBM uncorrectable errors, value: "1 per 44", unit: rad, note: "MEASURED, 203 events"}
:::

The headline result is a margin. The high-bandwidth memory began showing irregularities only after about 2 krad(Si), and one chip reached 15 krad(Si) without a hard failure. The modeled five-year mission dose is roughly 750 rad(Si) behind 10 mm of aluminium-equivalent shielding [^5]. On paper, that is a 2.7x margin to the first irregularity and 20x to the maximum tested dose [^5]. The beam also logged soft errors, including 203 HBM uncorrectable-error events at about one per 44 rad. The paper extrapolates silent data corruption to about one per 3 million inferences at one inference per second [^5]. One caveat on versions: TechCrunch reports that Google redid the beam tests for the *Joule* paper after finding the original setup over-shielded the chips. The retest found slightly more logic errors, and Beals described the inference error rate more loosely as "like one in a million" [^52]. The arXiv v2 figures used here may therefore differ modestly from the peer-reviewed version.

### What four chips can resolve

The table below is ARA's own derivation, not a figure from Google. It applies the paper's per-rad rates [^5] to the modeled dose of 150 rad per chip-year and treats the four chips as Poisson counters. Two chip-years equals four chips flying for six months.

| Event (ground rate) | Expected, 2 chip-years | Expected, 4 chip-years | What a count would tell you |
|---|---|---|---|
| Silent data corruption (~1 per 14.4–20 rad) | ~18 | ~35 | 95% CI at n=18 is about 10.7–28.5, so the rate is pinned to a factor of ~2.7 |
| HBM uncorrectable error (1 per 44 rad) | ~7 | ~14 | Coarse check, factor of ~3–4 |
| TPU crash / SEFI (~1 per 5 krad) | 0.06 | 0.12 | 94% chance of zero events in 2 chip-years; uninformative |
| Host CPU crash (1 per 450 rad) | 0.67 | 1.33 | One event or none; uninformative |

:::bars
- {label: Silent data corruption, value: "35", pct: 100}
- {label: HBM uncorrectable error, value: "14", pct: 40}
- {label: Host CPU crash, value: "1.3", pct: 4}
- {label: TPU crash (SEFI), value: "0.12", pct: 1}
:::

The asymmetry is the whole story. A count of silent corruptions is a real measurement, but zero crashes is not evidence of anything. By ARA's arithmetic, showing with 95% confidence that the crash (SEFI) rate is no worse than the ground estimate would take roughly 100 chip-years without an event. That is 25 years for this satellite. The four chips also share one board, one shield and almost certainly one wafer lot. They are not four independent samples of the population a constellation would fly.

### Why the ground numbers might not transfer

Several gaps between beam and orbit cut in different directions. The 15 krad result rests on a single chip [^5]. The beam delivered dose at up to about 1 krad per minute, far faster than the gradual accumulation in orbit, and dose-rate and annealing effects differ between those regimes [^5]. The test used protons only, so without heavy ions, latch-up and the more severe functional interrupts were not reproduced [^5]. Shielding is the largest lever. The 750 rad budget assumes 10 mm of aluminium-equivalent shielding, so an in-orbit error rate means little unless Google discloses the shielding actually flown [^5]. The authors note that correctable-error counts were "not reliably available" and that the impact on training "requires further study" [^5]. Launch coverage also described only roughly 15-minute active compute windows. The chips are checked for a fraction of wall-clock time, which shrinks the detectable counts in the table [^6].

Prior in-orbit evidence on commercial hardware suggests the failures that matter may not be in the logic at all. HPE's Spaceborne Computer-1 on the ISS lost 9 of 20 SSDs and 1 of 4 power supplies, and needed 4 reboots, over about 1.6 years [^24]. A proton test of a 14 nm FinFET NXP system-on-chip projects 0.44–0.78 Linux crashes per year at 500 km, with 56% of errors in the filesystem and eMMC storage [^23]. Storage, not compute, tends to fail first [^23,24]. Starcloud-1 carried an H100 to orbit in November 2025 and trained NanoGPT, but has published no error rates [^25].

The counterpoint is that even a modest data release would be a first. Suppose Google publishes silent-corruption counts with the flown shielding and the actual duty cycle. That would be the first in-orbit error dataset for a datacenter accelerator with HBM. A factor-of-three check on a ground model is more than any orbital compute project has disclosed so far [^5,25]. As of 2026-10-03, though, only bus contact and commissioning are confirmed, and no TPU data has been reported [^1,9].

Why this matters: reliability sets the spares ratio, and SemiAnalysis already assumes 20% spare capacity in orbit [^32]. One satellite can validate the soft-error input to that number, but not the hard-failure tail that drives it.

## 03. The thermal wall behind the 15-minute duty cycle

Space is not "free cooling." With no air or water to carry heat away, a satellite can reject waste heat only by radiating it. The prototype's 15-minute run limit is that constraint showing up at roughly 1 kW. Google's own facts post puts it plainly: "In a vacuum, you can only diffuse heat via radiators" [^2]. The satellite moves heat from the TPUs to radiators through heat pipes, and Google says the design was tested in a thermal vacuum chamber before launch [^2]. NPR reported that the Gemma model will run "for 15 minutes at a time due to heat management constraints," and that radiators are among the heaviest components on the spacecraft [^6]. That is a REPORTED operating limit, not a measured flight result. As of 2026-10-03 only initial contact with the satellite has been confirmed [^9].

### The physics is settled; the mass is not

A radiator's capacity follows the Stefan–Boltzmann law, q = εσT⁴ per radiating side, so the required area depends almost entirely on surface temperature. ARA's calculation for an ideal two-sided panel facing a 3 K sky, with emissivity 0.9, gives about 1.69 m² per kW at 276 K and 0.83 m² per kW at 330 K. The International Space Station is the best-documented benchmark: its six radiator arrays reject about 70 kW [^18]. With each array roughly 23.3 × 3.4 m, that works out to about 6.8 m² of panel per kW, about four times the ideal area at a similar loop temperature. Real radiators lose capacity to sun and Earth views, fin efficiency and temperature drops along the coolant loop (ARA derivation from [^18]).

:::bar-chart(title="Ideal radiator area per kW rejected", subtitle="two-sided panel, emissivity 0.9, 3 K sink; ARA calculation", orientation=horizontal, value-suffix=" m²")
categories: 276 K, 300 K, 330 K, 350 K, ISS actual (~276 K)
m² per kW: 1.69, 1.21, 0.83, 0.65, 6.8
:::

The ISS bar is derived from 70 kW over six arrays [^18]. Scale makes the gap concrete. NASA lists the station's eight main solar arrays at 75 to 90 kW, so a 1 GW cluster would need more than ten thousand times the ISS's original solar power [^19]. By ARA's derivation, rejecting 1 GW at 330 K would need at least 0.83 km² of ideal radiator. Built to ISS-heritage area per kW, it would need about 6.8 km².

### Hotter chips buy smaller radiators

The lever that matters is the allowable chip and coolant temperature, because radiated power rises with the fourth power of absolute temperature. IEEE Spectrum's analysis puts the radiator for a single H100 at about 1.0 m² if the chip runs at 85 °C, 1.4 m² at 60 °C and roughly 3 m² at 20 °C [^20].

:::compare
- {role: LOWEST, name: "H100 at 85 °C", value: "1.0 m²"}
- {role: HIGHEST, name: "H100 at 20 °C", value: "~3 m²"}
- {role: SUBJECT, name: "H100 at 60 °C", value: "1.4 m²"}
:::

Rack scale compounds quickly: IEEE Spectrum estimates that one 40 kW rack would need about 80 m² of radiator [^48]. Degradation compounds it further. ABI Research's Andrew Cavalier told IEEE Spectrum that required radiator area grows about 40% after five years in orbit, and that orbital compute would cost at least ten times as much as a ground data center [^20]. Planet's Mike Safyan made the same point to TechCrunch: "You're relying on very large radiators to just be able to dissipate that heat into the blackness of space" [^22]. Carnegie Mellon's Brandon Lucia told NPR that the costs and complexity of operating in space are "amplified by a factor of 10, maybe a factor of 100" [^6].

### What the bulls assume

The counterpoint is that none of this violates physics. It is an engineering mass budget, and optimistic models make specific choices to shrink it. Andrew McCalip's public cost model assumes radiator emissivity of 0.90 at about 75 °C. It treats the solar array area as the radiator and carries no dedicated radiator mass at all [^21]. That holds only if chips tolerate that temperature and arrays can double as radiators without overheating the cells. Then the area penalty shrinks toward the ideal curve above [^21]. Google's own paper is more cautious. It treats thermal design qualitatively and lists thermal management among the open problems [^5]. It also warns that neighbouring satellites in a dense cluster can block one another's view of cold space [^4,5].

What this flight can settle is narrow but real: whether a heat-pipe and radiator design at about 1 kW behaves as the thermal-vacuum tests predicted [^2]. It cannot settle the variable that decides viability: radiator kilograms per square metre and operating temperature at gigawatt scale, in a formation where satellites shade each other [^5]. This matters because once launch costs fall, radiator mass rather than solar power sets how many kilograms each kilowatt of orbital compute must lift.

## 04. Power: the "8x" is real, and it is the easy part

Orbital solar is genuinely better than ground solar, but the advantage is 5.5x to 8x depending on the ground baseline. Energy per panel is also not energy per dollar or per kilogram. And the terrestrial problem orbit targets is grid access, not sunlight.

Google's wording is consistent across venues. The facts post says satellites "can access near-constant sunlight, generating up to eight times more solar power than on Earth" [^2]. The Research blog says that "in the right orbit, a solar panel can be up to 8 times more productive than on earth" [^4]. The paper is the most careful: "up to 8× more solar energy per year than a panel located on Earth at mid-latitude." It cites NSRDB irradiance data for that figure rather than deriving it from first principles [^5]. The reference design flies a dawn-dusk sun-synchronous orbit at 650 km, riding the day-night terminator so the arrays face the Sun almost continuously [^5]. The prototype launched on 2026-10-01 reportedly carries about 1 kW of solar [^14]. NPR describes its sun-synchronous orbit as one where the panels "will almost never be in the shade" [^6].

### Reproducing the multiple

The physics is short. Above the atmosphere a panel sees the solar constant, about 1.361 kW/m², while ground panels are rated at a standard 1.0 kW/m². In sunlight ~99% of the year (8,766 hours), a panel rated at 1 kW on the ground delivers the equivalent of a ~135% capacity factor in orbit (ARA calculation). The ground side of the ratio is where the "8x" moves. US utility-scale solar ran at a 24.4% capacity factor in 2025 (preliminary) [^17].

:::line-chart(title="US utility-scale solar capacity factor", subtitle="EIA, % (2025 preliminary)", y-unit=%)
x: 2016,2017,2018,2019,2020,2021,2022,2023,2024,2025
Capacity factor: 25.0,25.6,25.1,24.3,24.2,24.4,24.4,23.2,23.2,24.4
:::

Against that fleet the orbital multiple is about 5.5x [^17]. Plants install more DC panel capacity than inverter capacity, so EIA's AC figure understates per-panel output. Assuming a typical DC-to-AC overbuild, the per-panel figure is roughly 19%, which gives about a 7.1x multiple (ARA assumption). For a fixed-tilt panel at a cloudier mid-latitude site, ARA assumes 11–15%, which gives 9–12x. Google's "up to 8x" sits inside that range and is honest for its stated baseline [^2,5]. It is not the multiple a hyperscaler buying power from the best US solar sites would face [^17].

:::bars
- {label: "vs EIA utility-scale AC fleet (24.4%)", value: "5.5x", pct: 46}
- {label: "vs per-panel DC basis (~19%, assumed)", value: "7.1x", pct: 59}
- {label: "Google claim, mid-latitude panel", value: "up to 8x", pct: 67}
- {label: "vs fixed mid-latitude panel (11-15%, assumed)", value: "9-12x", pct: 100}
:::

*ARA calculation: 1.361 kW/m² × ~99% sunlit × 8,766 h, divided by each ground capacity factor. Ground data from EIA [^17]; Google's claim from [^2,4,5].*

### What the multiple leaves out

"Near-constant" is not constant. By ARA's geometric calculation, a dawn-dusk orbit at the paper's 650 km still passes through Earth's shadow for up to about 20 minutes per orbit around the June solstice. That leaves an annual sunlit fraction of roughly 98–99% [^5]. Each eclipse must be bridged with batteries or by shedding the compute load. The 8x also ignores three costs. Solar cells lose efficiency as they get hotter. The arrays degrade cumulatively under radiation. And radiators must reject essentially every collected watt as heat, which section 03 shows is the harder half of the problem.

The better metric is delivered watts per kilogram of satellite, because launch is priced by mass. McCalip's cost model defaults to 36.5 W/kg for the whole satellite [^21]. Google's paper implies about 49 W/kg for a Starlink v2-class satellite of 575 kg producing ~28 kW [^5]. SpaceX's FCC filing claims about 100 kW per tonne, or ~100 W/kg [^22,47]. That 2.7x spread in a single input moves orbital economics far more than the gap between 5.5x and 8x.

### Why build up there at all

The terrestrial bottleneck is the grid queue, not the Sun. LBNL's *Queued Up* counts 2,061 GW of capacity waiting in US interconnection queues at end-2025, down from a peak near 2,600 GW at end-2023. Time from request to commercial operation now exceeds five years [^49]. Energy itself is not expensive: US industrial electricity averaged 9.77¢/kWh in July 2026 [^28]. Orbit sidesteps the queue entirely, and that is the real pitch.

The counterpoint is that orbit is not the only way out of the queue. An on-site solar-plus-storage farm, or a behind-the-meter gas plant in a permissive jurisdiction, also avoids interconnection, with no launch, no radiator and no eclipse. The comparison that matters is all-in cost per kilowatt-hour delivered to the chip, and the panel multiple is only one term in it.

Why this matters: the flight will mostly confirm that a ~1 kW array produces what the model predicts [^14]. That is useful, but it validates the least uncertain number in the whole stack.

## 05. What one satellite cannot settle: links, formation flying, debris

What would make orbital compute a datacenter rather than a scattering of servers is a mesh of terabit-class optical links between satellites flying 100–200 m apart. That cannot be tested with one satellite. And the bandwidth requirement is exactly what forces the riskiest orbital geometry in the design [^4,5]. Google's own plan acknowledges the gap: the next milestone after the October 2026 flight is a pair of satellites in 2027 to test the laser links [^2].

### The bandwidth gap

Training a large model across many chips needs inter-chip bandwidth comparable to a terrestrial datacenter network. The Suncatcher paper sizes that at roughly 10 Tbps per inter-satellite link, one to two orders of magnitude above what commercial inter-satellite links carry today [^5]. The only MEASURED number against that target is a bench demonstration in which one transceiver pair "achieved 800 Gbps each-way transmission (1.6 Tbps total)" over a short free-space path [^4,5].

:::compare
- {role: LOWEST, name: "Commercial inter-satellite links", value: "1–100 Gbps"}
- {role: SUBJECT, name: "Suncatcher bench demo (one transceiver pair)", value: "1.6 Tbps"}
- {role: HIGHEST, name: "Required per link (design)", value: "~10 Tbps"}
:::

The bench result is real but narrow. A lab path has no relative motion between terminals, no orbital pointing jitter, no kilometre-scale path and no thermal cycling through sunlight and eclipse. The design calls for pointing accuracy on the order of 1 µrad between moving spacecraft [^4,5]. A single satellite has no partner to point at, so the October flight produces no evidence on this question at all [^1,2].

### Why the link budget dictates the orbit

The governing physics is the inverse-square law. Received optical power falls as 1/d², so the only way to stack many parallel channels onto one link is to keep transmitter and receiver close [^4,5]. The paper's own numbers make the point: a 2×2 spatially multiplexed array closes at about 1.25 km, and a 4×4 array only at about 0.32 km. That is why Google concludes the satellites must fly "kilometers or less" apart [^4,5]. The bandwidth requirement is not an add-on to the formation; it sets how dense the formation must be [^5].

:::kv
- {term: "Satellites (illustrative, MODELED)", def: "81 [^5]"}
- {term: "Cluster radius", def: "1 km [^5]"}
- {term: "Orbit", def: "Mean altitude 650 km, dawn-dusk sun-synchronous [^5]"}
- {term: "Neighbour spacing", def: "Oscillates ~100–200 m [^4,5]"}
- {term: "Link design", def: "24 DWDM channels → 9.6 Tbps bidirectional [^5]"}
- {term: "J2 drift", def: "<3 m/s/yr per km after axis-ratio correction [^5]"}
:::

All of these figures are MODELED rather than measured [^4,5]. The link design reaches 9.6 Tbps bidirectional with 24 dense-wavelength-division (DWDM) channels, still just short of the ~10 Tbps per-link target [^5]. Formation dynamics are modelled with the Hill-Clohessy-Wiltshire equations plus the J2 term for Earth's oblateness. Correcting the cluster's axis ratio holds J2-induced drift under 3 m/s per year per kilometre of separation [^5]. Differential atmospheric drag is mentioned but not quantified. The paper gives no total delta-v budget and no collision-avoidance analysis for spacecraft a few hundred metres apart [^5]. Google itself lists thermal management, high-bandwidth ground communications and on-orbit reliability as open problems [^4,5].

### The neighbourhood is getting crowded

A tight cluster is being proposed for an environment that is already congested. ESA counts about 40,000 tracked objects, about 11,000 of them active payloads at end-2024, plus more than 1.2 million objects larger than 1 cm. It projects that debris will keep growing even with no new launches [^45]. Astronomer Jonathan McDowell counted 14,518 active payloads at end-January 2026, 9,555 of them Starlink [^47]. SpaceX has filed for up to 1,000,000 satellites. McDowell says such a fleet "will absolutely be required to have a fleet of tow-truck satellites" [^47].

Starlink's reported collision-avoidance manoeuvres rose from 148,696 in the prior half-year to 207,152 in Dec 2025–May 2026 (as of 2026-07-15), as the fleet passed 10,000 satellites by June 2026 [^46]. Debris researcher Hugh Lewis warns that "we're heading towards a situation where there will be a collision involving an operational satellite" [^46]. The counts overstate risk in one respect: Starlink manoeuvres whenever collision probability exceeds 3 in 10 million, a very conservative trigger [^46]. A Suncatcher cluster faces the opposite problem. Every dodge by one satellite perturbs a formation whose links only work at a few hundred metres, and the paper does not analyse that case [^5].

### The counterpoint: not every workload needs the mesh

The 10 Tbps requirement comes from training, and training is the workload least suited to orbit. An arXiv study of which workloads suit orbit scores LLM training 1 out of 5 on bandwidth and data locality [^50]. Analyst Michael Pierce puts it plainly: "Training workloads likely cannot tolerate the synchronization and latency constraints of a distributed orbital system" [^48]. Inference and in-space processing of Earth-observation data need far less inter-satellite bandwidth. A loosely coupled fleet could be useful for those without ever solving the terabit mesh or the 100–200 m geometry [^50]. That is a smaller business than an orbital datacenter, but one a single-satellite program can credibly grow into.

Why this matters: the October 2026 flight tests components. The 2027 two-satellite link test is the real decision point for whether Suncatcher can ever behave like a datacenter [^2,5].

## 06. Economics: launch is not the binding constraint

Launch is the cost everyone argues about, and Google's own paper suggests it can plausibly be solved. The costs that decide whether orbital AI compute pays are server depreciation, short unserviceable lifetimes and spares. A four-TPU flight test measures none of them [^5,29,32].

The historical curve behind the optimism is real. In 2021 dollars, the Space Shuttle cost about $65,400 per kilogram to low Earth orbit, while Falcon 9 brought that to about $2,600/kg and Falcon Heavy to about $1,500/kg [^26]. Small dedicated launchers cost far more per kilogram, which is why Electron sits above the heavy expendable rockets of the 2000s [^26].

:::bar-chart(title="Launch cost to LEO by vehicle", subtitle="$ per kg, 2021 dollars, by first-launch year", orientation=horizontal, value-unit=$)
categories: Space Shuttle (1981), Ariane 5G (1997), Atlas V (2002), Delta IV Heavy (2004), Falcon 9 (2010), Electron (2018), Falcon Heavy (2018)
$/kg: 65400, 10200, 8100, 11600, 2600, 23100, 1500
:::

### Google's math: launched power converges on grid power

The Suncatcher paper frames launch as a cost per kilowatt-year of putting power-generating mass in orbit (MODELED) [^5]. At a current reusable Falcon 9 price of roughly $3,600/kg, it puts launched power at $14,700/kW/yr. That falls to $810/kW/yr if launch drops to $200/kg [^5]. Its learning-curve projection reaches ≲$200/kg by the mid-2030s. It compares that with a terrestrial power spend of roughly $570–3,000/kW/yr [^5]. As a cross-check, the US average industrial electricity price was 9.77¢/kWh in July 2026 [^28]. At full load that is about $856/kW/yr (ARA arithmetic: $0.0977 × 8,760 h), squarely inside Google's band.

:::compare
- {role: LOWEST, name: "Terrestrial power spend (low end)", value: "$570/kW/yr"}
- {role: HIGHEST, name: "Launched power at today's ~$3,600/kg", value: "$14,700/kW/yr"}
- {role: SUBJECT, name: "Launched power at $200/kg (mid-2030s)", value: "$810/kW/yr"}
:::

That comparison carries two caveats. First, the paper excludes satellite hardware, ground stations and replacement. It compares launch only against power only, and says it "does not constitute a full economic analysis" [^5]. Second, prices are not yet moving the right way for small payloads. As of 2026-02-27, SpaceX rideshare pricing was about $7,000/kg and rising, not falling [^27].

### The cost that does not move when you leave the ground

Energy is a small slice of an AI datacenter's bill. Epoch AI estimates a 1 GW AI datacenter at about $38B upfront, $26B of compute and $12B of construction. Annualized, that is about $8.5B per year, of which servers account for roughly $5B, or 60% [^29].

:::donut(center-label="$8.5B/yr")
- {label: "Servers", value: 5.0}
- {label: "Everything else (construction, power, opex)", value: 3.5}
:::

Spread that $5B across 1 GW and server depreciation comes to about $5,000/kW/yr, roughly 6x Google's $810/kW/yr launch figure (ARA arithmetic) [^5,29]. That cost is the same on the ground and in orbit, so even free launch leaves the largest line item untouched [^29]. Orbit also shortens the depreciation period. Alphabet depreciates its servers over six years [^30]. A satellite that cannot be serviced caps chip life at satellite life, which the paper's design puts at roughly five years [^5]. Andrew McCalip's public cost model puts it bluntly: "This is not a 25% mismatch. It's 400%" [^21]. Fox Business reported that OpenAI's Sam Altman called orbital data centers "ridiculous" in "the current landscape" [^42].

### What independent models say

Every outside model that adds chips, spares and lifetime back in lands above terrestrial cost today (MODELED):

| Model | Orbit vs ground | Key drivers |
|---|---|---|
| SemiAnalysis [^32] | $10.91 vs $2.49 per GPU-hour (~4.4x) after availability and redundancy | Launch is $1.6M of $3.1M per-unit space facility capex; 5-year vs 15-year facility life; 20% spares in orbit vs ≤5% on the ground |
| BCG [^33] | 20-year TCO of $660–750M/MW vs $230–300M/MW (2.5–3x); realistic path 1.5–1.8x | GPUs are ~half of TCO, launch ~one fifth; result swings on an in-orbit failure rate of 10–30% |
| McCalip [^21] | $31.20/W vs $14.80/W for 1 GW over 5 years at $1,000/kg | Excludes chips, so the gap comes from power, thermal and structure alone |
| Google paper [^5] | Launch-only vs power-only comparison | Explicitly "does not constitute a full economic analysis" |

The 1.5x-to-4.4x spread is mostly a disagreement about lifetime and failure, not about rockets [^32,33]. SemiAnalysis's 20% spares assumption and BCG's 10–30% failure-rate band ask the same question two ways: how many chips die in orbit with no technician to swap them [^32,33]? Both models also project the gap closing over time. BCG's aggressive path reaches about 1.1–1.2x at 5–10% failure rates, and SemiAnalysis projects parity around 2040, with orbit cheaper after that [^32,33]. The skeptical case is therefore about the next decade, not about all time.

The strongest counterpoint is that paying more is not the same as ruling it out. With a 67% cut in launch cost and an in-orbit failure rate near 10%, BCG's realistic path narrows to about 1.5x. A buyer stuck for years in grid interconnection queues might pay that premium to get power sooner [^33,49].

This is where the flight test contributes something, if only one number. An in-orbit failure-rate datapoint feeds the most sensitive variable in BCG's model [^1,33]. Four chips on one satellite cannot pin a fleet failure rate. But every current model runs on assumptions here, so even one real measurement adds something [^1,5]. Why this matters: chip lifetime and replacement economics will decide whether orbital AI compute is viable. A successful ~1 kW prototype launch mainly speaks to launch cost, which was already the easiest argument to win [^1,5,29].

## 07. The race: who has actually computed in orbit

Google is not first to put AI compute in orbit. China's Three-Body constellation and Starcloud both ran models in space before the Suncatcher prototype launched on 2026-10-01 [^1,25,34]. What sets Suncatcher apart is not timing but completeness. Its plan covers chips, inter-satellite links and formation flying in one design, backed by published ground radiation data. Most rival claims rest on regulatory filings, funding rounds or press releases [^3,5].

:::timeline
- {date: 2025-05-14, headline: "Three-Body constellation launches", body: "ADA Space and Zhejiang Lab put 12 computing satellites in orbit carrying an 8B-parameter on-board model [^34]."}
- {date: 2025-10-15, headline: "Nvidia previews Starcloud-1", body: "Billed as the first time a state-of-the-art, data center-class GPU is in outer space [^36]."}
- {date: 2025-11-04, headline: "Suncatcher announced", body: "Google publishes the TPU-in-orbit research program [^3]."}
- {date: 2025-11, headline: "Starcloud-1 (H100) launches", body: "Trains NanoGPT and runs Gemma inference [^25]."}
- {date: 2026-01-11, headline: "Axiom/Kepler ODC nodes launch", body: "Two orbital data center nodes; no performance data published [^37]."}
- {date: 2026-02-02, headline: "SpaceX acquires xAI", body: "Deal cites orbital data centers; FCC filing for up to 1M satellites [^38,47]."}
- {date: 2026-03, headline: "Starcloud FCC filing reported", body: "Application for up to 88,000 satellites [^39]."}
- {date: 2026-08-21, headline: "Starcloud raises $250M", body: "At a $2.3B valuation [^40]."}
- {date: 2026-08-24, headline: "Nvidia names Starmind", body: "SpaceXAI first-generation satellite on Vera Rubin NVL72, on a when-and-if-available basis [^41]."}
- {date: 2026-10-01, headline: "Suncatcher prototype launches", body: "Four TPUs on a Planet-built bus; contact confirmed [^1]."}
:::

**Three-Body ran first, but its numbers are self-reported.** The operators claim 744 TOPS peak for the most capable satellite, 5 POPS across the 12 linked satellites, and laser links of up to 100 Gbps [^35]. No numeric precision is stated, so a rating of this kind is most likely low-precision integer arithmetic. In our judgment, 5 POPS is in the range of the headline sparse rating of a single high-end datacenter GPU. That makes Three-Body a real in-orbit inference demonstration, but not datacenter scale [^35]. Its 8B-parameter on-board model fits that budget [^34].

**Starcloud has the most testable claim to date.** In the company's words, its one-H100 satellite Starcloud-1 was "the first spacecraft to train an LLM - the nano GPT model from Andrej Karpathy." It also ran Gemma inference [^25]. Nvidia framed the payload as "100x more powerful GPU compute than any previous space-based operation" [^36]. That is against a weak baseline, but a named model on a named GPU can at least be checked [^25,36]. Starcloud's CEO says the binding constraint is now launch slots, not chips. the Falcon 9 program is "scheduled to end in 2028," and Starcloud-3 is planned to fly on Starship [^40]. The next step, Starcloud-2, is planned as two 8 kW satellites in 2027 [^40].

**The largest numbers are filings, not hardware.** SpaceX's FCC filing for up to 1M satellites argues that "within a few years the lowest cost to generate AI compute will be in space" [^38,47]. TechCrunch reports the filing's design point at roughly 100 kW of compute per tonne of satellite [^22]. Yet SpaceX's own IPO risk factors warn that the orbital data center plan "may not achieve commercial viability" [^51]. Starmind, its first compute satellite, has so far appeared only in an Nvidia release that describes it on a "when-and-if-available" basis [^41]. Axiom has published no performance data for its 2026 nodes [^37].

| Program | Demonstrated in orbit | Status | Key figure |
|---|---|---|---|
| Three-Body (ADA Space/Zhejiang Lab) | Yes, 8B on-board model | 12 sats launched | 744 TOPS peak, 5 POPS combined, up to 100 Gbps laser links (self-reported) [^35] |
| Starcloud-1 | Yes, training and inference | 1 sat launched | 1 H100, trained NanoGPT [^25,36] |
| Axiom/Kepler ODC | Claimed, unverified | 2 nodes launched | No performance published [^37] |
| *Suncatcher MVP | Not yet | Launched, contact confirmed | 4 TPUs (reported); no TPU data yet [^1,14] |
| Starcloud-2 | No | Planned | 2 × 8 kW satellites in 2027 [^40] |
| SpaceX Starmind | No | Announced | Vera Rubin NVL72-based; "when-and-if-available" [^41] |
| SpaceX 1M-satellite filing | No | Filed with FCC | Up to 1,000,000 satellites [^47] |

As of 2026-10-03, Suncatcher is the only program in the table that published radiation beam results and link bench data before launch. Even so, its satellite has confirmed only bus contact, not TPU operation [^1,5]. **Counterpoint:** integration cuts both ways. Google owns its TPU, its models and its radiation data, but SpaceX owns launch, the very cost lever Google's own economics depend on [^5,38]. A rival that is vertically integrated and also sets the price of reaching orbit has a structural advantage Google cannot buy.

Why this matters: of all these programs, only Suncatcher and Starcloud have published anything a third party can test. The race metric to watch is published in-orbit error and thermal data, not the number of satellites filed with the FCC [^1,25,39].

## 08. The business signal: Planet, Alphabet and the stated timelines

The money and the principals' own words say the same thing: Suncatcher is a research moonshot, not a capacity plan. Planet books it as an offset to R&D with no revenue attached. The prototype is a rounding error against Alphabet's capital budget. And the program's own lead does not expect cost parity within five years. The one market that reacted sharply, Planet's stock, is pricing a narrative.

:::stats
- {label: "PL move, 2026-10-02", value: "+7.8%", note: "to $17.44"}
- {label: "PL vs 52-week high", value: "66.1%", unit: "below", note: "$51.40 high, May 2026"}
- {label: "Planet FQ2 FY2027 revenue", value: "$116M", note: "+58% YoY"}
- {label: "Alphabet 2026 capex guide", value: "$195–205B", note: "raised from $180–190B"}
:::

### How Planet accounts for it

Planet has been unusually explicit that Suncatcher is not a revenue line. On its Q3 FY2026 call, management described the work as "just an R&D at this phase. This is an R&D contract," covering "a couple of demo satellites" for Google [^11]. By the Q4 FY2026 call, management said the "SunCatcher partnership is structured as an R&D partnership," and the CFO drew the accounting line precisely [^12]:

:::quote(attr="Ashley Johnson, CFO, Planet Labs, Q4 FY2026 earnings call")
It is not contra revenue. It is contra R&D expense. [^12]
:::

The distinction has a mechanical consequence. Google's payments reduce Planet's reported R&D cost rather than appearing in the top line, so Suncatcher adds nothing to the revenue growth investors model [^12]. The original November 2025 announcement said Planet would build and operate the satellites. It targeted launch by early 2027 and reused the same satellite bus as Planet's Owl program [^10]. In effect, Planet is adapting a platform it already needed, with the customer offsetting the engineering cost [^10,12].

Planet's core business is strong on its own terms. On its Q2 FY2027 call on 2026-09-09, it reported record revenue of $116M, roughly 58% growth, and 688 satellites launched on 42 rockets. By our reading of the transcript, Suncatcher was not discussed [^13]. Three weeks later, the launch release listed the Suncatcher flight as part of Planet's 40th launch, with 718 satellites built and delivered [^8].

### What the stock is pricing

PL traded near $16.46 before the launch, per Benzinga [^15]. On 2026-10-02 it rose 7.8% to $17.44, which still left it 66.1% below its May 2026 52-week high of $51.40 [^16]. That is a large move on a demo satellite that, per Planet's own CFO, books no revenue. It is a sentiment trade on the space-compute narrative, not a repricing of cash flows [^12,16].

### Scale against Alphabet

Alphabet raised its 2026 capital-expenditure guide to $195–205B from $180–190B and spent $44.9B in Q2 alone [^31]. Neither Google nor Planet has disclosed what the prototype cost, so no precise ratio is possible [^1,12]. But a single satellite with about a kilowatt of solar is, by any reasonable estimate, immaterial against a budget of roughly $200B [^14,31]. Nothing in that budget treats orbital compute as capacity.

### The stated timelines

The principals' own forecasts spread across two decades, and the people closest to the hardware are the most conservative.

| Who | Stated timeline | Source |
|---|---|---|
| SpaceX FCC filing (Elon Musk's SpaceX/xAI) | "within a few years the lowest cost to generate AI compute will be in space" | [^38] |
| Sundar Pichai (Alphabet) | "a decade or so away we'll be viewing it as a more normal way to build data centers" | [^43] |
| Jeff Bezos (Blue Origin) | "We will be able to beat the cost of terrestrial data centres in space in the next couple of decades" | [^44] |
| Travis Beals (Suncatcher lead) | "I don't see this being something where it's cheaper to do this in the next five years" | [^6] |
| James Manyika (Google SVP) | "We don't expect … anything usefully operational in the next few years" | [^14] |
| Sam Altman (OpenAI) | "the idea with the current landscape of putting data centers in space is ridiculous" | [^42] |

The only voice forecasting parity within five years is the company that sells the launches and has merged with xAI to pursue an orbital data-center constellation [^38]. Google's CEO, program lead and SVP all point well past the next few years [^6,14,43].

### The counterpoint: this is a cheap option

None of this makes the program irrational. If grid interconnection, rather than chips, ends up capping AI capacity, a company that has already flown TPUs in a working satellite holds a real head start. The size of US interconnection queues gives that scenario weight [^49]. For Planet, a successful 2027 pair would turn the Owl-class bus into a product line for hosting compute [^10]. An option is worth buying when its premium is this small relative to capex [^31].

Why this matters: read Suncatcher as a cheap call option and a recruiting and positioning signal. It is not evidence that Alphabet expects orbital compute to carry meaningful load this decade.

## 09. What could break the thesis

The thesis is that Suncatcher's first flight is a real step that tests easy questions. It could be wrong in four ways, and each has a specific signal to watch.

**1. The flight could fail at the easy part.** Contact with the bus is not a working payload. Google has promised TPU data only "over the coming weeks" [^1]. Planet was still commissioning the satellite on launch day [^9]. Some outcomes would show that hardened ground testing does not transfer to orbit: a TPU that will not power on, HBM errors well above the beam-derived rate, or thermal throttling worse than the 15-minute budget [^5,6]. That would be a bigger negative signal than any cost model.

**2. Launch could fall faster and further than the models assume.** Starship reaching routine reuse would hit the paper's ≲$200/kg learning-curve target early [^5]. At that price SemiAnalysis's launch share of facility capex shrinks from about half [^32]. SpaceX's filing argues that "within a few years the lowest cost to generate AI compute will be in space" [^38]. But BCG's realistic path, which assumes a 67% cut in launch cost, still leaves a 1.5–1.8x premium [^33]. The skeptical reading therefore survives cheap launch unless chip lifetime and failure rates also cooperate.

**3. Chips could become cheap relative to power and grid access.** Our economics argument rests on servers being about 60% of AI datacenter cost [^29]. Two things would flip the ranking toward orbit: a sustained collapse in accelerator prices, or a terrestrial grid in which new capacity simply cannot be connected within five years [^49].

**4. Workloads could change shape.** Inference and in-space data processing need far less inter-satellite bandwidth than training [^50]. If demand shifts toward those, a loosely coupled fleet could be useful without the 10 Tbps mesh or the 100–200 m formation [^5,50]. The most important unsolved problem would then become irrelevant rather than solved.

:::callout(kind=warn, label="Red-team pass")
An adversarial pass attacked three load-bearing claims:

- **No TPU data has been published as of 2026-10-03.** This survived. No source reports a TPU power-on or any telemetry [^1].
- **Orbit costs 1.5–4.4x ground today.** This drew a medium-severity objection: the same models project parity around 2040, or 1.1–1.2x in optimistic cases. We now state that explicitly [^32,33].
- **The ~1 per 3 million inference error rate.** This drew a low-severity note: Beals's looser "one in a million" figure after the *Joule* retest [^52].

Net: 1 of 3 top claims unbroken; the other two were qualified, not overturned.
:::

What to watch, in order of evidentiary weight:

- Google publishing in-orbit error counts with the shielding and duty cycle actually flown [^1,5].
- The 2027 two-satellite laser-link test [^2].
- Starcloud-2's 8 kW satellites in 2027 [^40].
- Any FCC filing turning into launched mass [^39,47].

Why it matters: the question of orbital AI compute will be decided by measured link bandwidth, failure rates and radiator mass, not by launch announcements. This flight starts the measurement program without yet producing the numbers that matter.

:::references
- {id: 1, title: "Project Suncatcher's prototype satellite is in orbit", url: "https://blog.google/innovation-and-ai/models-and-research/google-research/project-suncatcher-prototype/", source: "Google (Travis Beals)", date: "2026-10-01"}
- {id: 2, title: "Behind Project Suncatcher: the facts", url: "https://blog.google/innovation-and-ai/models-and-research/google-research/google-project-suncatcher-facts/", source: "Google (Travis Beals)", date: "2026-09-24"}
- {id: 3, title: "Meet Project Suncatcher", url: "https://blog.google/innovation-and-ai/technology/research/google-project-suncatcher/", source: Google, date: "2025-11-04"}
- {id: 4, title: "Exploring a space-based, scalable AI infrastructure system design", url: "https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/", source: Google Research, date: "2025-11-04"}
- {id: 5, title: "Towards a future space-based, highly scalable AI infrastructure system design (v2)", url: "https://arxiv.org/html/2511.19468", source: "arXiv 2511.19468 (Agüera y Arcas, Beals et al.)", date: "2026-06-17"}
- {id: 6, title: "Google launches Project Suncatcher, a step towards AI data centers in space", url: "https://www.opb.org/article/2026/10/01/google-launches-project-suncatcher-a-step-towards-ai-data-centers-in-space/", source: NPR / OPB, date: "2026-10-01"}
- {id: 7, title: "The first mission milestones onboard SpaceX's Transporter-18 rideshare launch", url: "https://www.satellitetoday.com/launch/2026/10/01/the-first-mission-milestones-onboard-spacexs-transporter-18-rideshare-launch/", source: Via Satellite, date: "2026-10-01"}
- {id: 8, title: "Planet launches Suncatcher, Tanager-2 and 18 SuperDoves", url: "https://www.stocktitan.net/news/PL/planet-launches-suncatcher-tanager-2-and-18-super-dove-s3on34tpzo6r.html", source: "Planet (Business Wire)", date: "2026-09-30"}
- {id: 9, title: "Planet launches Suncatcher, Tanager-2 and 18 SuperDove satellites", url: "https://www.satcom.digital/news/planet-launches-suncatcher-tanager-2-and-18-superdove-satellites", source: "Planet via Satcom Digital", date: "2026-10-01"}
- {id: 10, title: "Planet to build and operate advanced space platform for Project Suncatcher moonshot", url: "https://www.planet.com/pulse/planet-to-build-and-operate-advanced-space-platform-for-project-suncatcher-moonshot/", source: Planet, date: "2025-11-04"}
- {id: 11, title: "Planet Labs Q3 FY2026 earnings call transcript", url: "https://stockanalysis.com/stocks/pl/transcripts/384048-q3-2026/", source: Stock Analysis, date: "2025-12-10"}
- {id: 12, title: "Planet Labs (PL) Q4 2026 earnings call transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/03/19/planet-labs-pl-q4-2026-earnings-call-transcript/", source: The Motley Fool, date: "2026-03-19"}
- {id: 13, title: "Planet Labs (PL) Q2 2027 earnings call transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/09/09/planet-labs-pl-q2-2027-earnings-call-transcript/", source: The Motley Fool, date: "2026-09-09"}
- {id: 14, title: "Google is sending a teensy tiny AI data center to space", url: "https://www.engadget.com/2267975/google-is-sending-a-teensy-tiny-ai-data-center-to-space/", source: Engadget, date: "2026-09-24"}
- {id: 15, title: "Google moves space data center plans forward", url: "https://finance.yahoo.com/technology/ai/articles/google-moves-space-data-center-023007693.html", source: Benzinga via Yahoo Finance, date: "2026-09"}
- {id: 16, title: "Planet Labs (PL) shares skyrocket, what you need to know", url: "https://markets.financialcontent.com/stocks/article/stockstory-2026-10-2-planet-labs-pl-shares-skyrocket-what-you-need-to-know", source: StockStory, date: "2026-10-02"}
- {id: 17, title: "Electric Power Monthly Table 6.07.B: capacity factors for utility-scale generators", url: "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_6_07_b", source: US EIA, date: "2026-09-24"}
- {id: 18, title: "Space Station heat rejection subsystem radiator assembly design and development (SAE 951651)", url: "https://saemobilus.sae.org/papers/space-station-heat-rejection-subsystem-radiator-assembly-design-development-951651", source: SAE International, date: "1995-07-01"}
- {id: 19, title: "International Space Station facts and figures", url: "https://www.nasa.gov/international-space-station/space-station-facts-and-figures/", source: NASA}
- {id: 20, title: "Orbital data centers have a heat problem", url: "https://spectrum.ieee.org/orbital-data-centers-heat", source: IEEE Spectrum, date: "2026-06-11"}
- {id: 21, title: "Space datacenters: orbital vs terrestrial cost model", url: "https://andrewmccalip.com/space-datacenters", source: Andrew McCalip, date: "2026"}
- {id: 22, title: "Why the economics of orbital AI are so brutal", url: "https://techcrunch.com/2026/02/11/why-the-economics-of-orbital-ai-are-so-brutal/", source: TechCrunch, date: "2026-02-11"}
- {id: 23, title: "Proton radiation testing of COTS FinFET SoCs for LEO", url: "https://arxiv.org/html/2503.03722v1", source: arXiv 2503.03722, date: "2025-03-05"}
- {id: 24, title: "HPE's Spaceborne Computer results", url: "https://www.theregister.com/2019/10/07/goh_hpe_spaceborne/", source: The Register, date: "2019-10-07"}
- {id: 25, title: "Starcloud-1 mission", url: "https://www.starcloud.com/starcloud-1", source: Starcloud}
- {id: 26, title: "Space launch to low Earth orbit: how much does it cost?", url: "https://aerospace.csis.org/data/space-launch-to-low-earth-orbit-how-much-does-it-cost/", source: CSIS Aerospace Security, date: "2022-09-01"}
- {id: 27, title: "Satellite ridesharing market analysis 2026", url: "https://newspaceeconomy.ca/2026/02/27/satellite-ridesharing-market-analysis-2026/", source: New Space Economy, date: "2026-02-27"}
- {id: 28, title: "Electric Power Monthly Table 5.6.A: average retail price of electricity by sector", url: "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a", source: US EIA, date: "2026"}
- {id: 29, title: "AI datacenter cost breakdown", url: "https://epoch.ai/data-insights/ai-datacenter-cost-breakdown", source: Epoch AI, date: "2026-05-14"}
- {id: 30, title: "Alphabet FY2025 Form 10-K: property and equipment note", url: "https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/R31.htm", source: SEC EDGAR, date: "2026-02"}
- {id: 31, title: "Earnings call transcript: Alphabet Q2 2026", url: "https://www.investing.com/news/transcripts/earnings-call-transcript-alphabet-beats-q2-2026-estimates-shares-fall-on-capex-surge-93CH-4807140", source: Investing.com, date: "2026-07-22"}
- {id: 32, title: "To boldly go: the case for space datacenters", url: "https://newsletter.semianalysis.com/p/to-boldly-go-the-case-for-space-datacenters", source: SemiAnalysis, date: "2026-06-03"}
- {id: 33, title: "Space-based data centers: cost outlook", url: "https://www.bcg.com/publications/2026/space-based-data-centers-cost-outlook", source: BCG, date: "2026-08-27"}
- {id: 34, title: "Three-Body Computing Constellation launch", url: "http://www.xinhuanet.com/tech/20250515/a4f002a57a304012865013110319f42d/c.html", source: Xinhua, date: "2025-05-15"}
- {id: 35, title: "Three-Body Computing Constellation specifications", url: "https://news.hangzhou.com.cn/zjnews/content/2025-05/15/content_8995480.htm", source: Hangzhou News, date: "2025-05-15"}
- {id: 36, title: "How Starcloud is bringing data centers to outer space", url: "https://blogs.nvidia.com/blog/starcloud/", source: NVIDIA, date: "2025-10-15"}
- {id: 37, title: "Orbital Data Center", url: "https://www.axiomspace.com/orbital-data-center", source: Axiom Space}
- {id: 38, title: "SpaceX acquires xAI to pursue orbital data center constellation", url: "https://www.satellitetoday.com/connectivity/2026/02/02/spacex-acquires-xai-to-pursue-orbital-data-center-constellation/", source: Via Satellite, date: "2026-02-02"}
- {id: 39, title: "Space Brief 2026-03-16 (Starcloud 88,000-satellite FCC filing)", url: "https://keeptrack.space/space-brief/space-brief-2026-03-16", source: KeepTrack, date: "2026-03-16"}
- {id: 40, title: "Starcloud raises funding for orbital data centers as launch options dry up", url: "https://techcrunch.com/2026/08/21/starcloud-raises-200-million-for-orbital-data-centers-as-launch-options-dry-up/", source: TechCrunch, date: "2026-08-21"}
- {id: 41, title: "SpaceXAI adopts NVIDIA Vera CPU to accelerate agentic AI at massive scale", url: "https://nvidianews.nvidia.com/news/spacexai-adopts-nvidia-vera-cpu-to-accelerate-agentic-ai-at-massive-scale", source: NVIDIA Newsroom, date: "2026-08-24"}
- {id: 42, title: "Altman calls Musk's space data center plans ridiculous", url: "https://www.foxbusiness.com/technology/altman-calls-musks-space-data-center-plans-ridiculous-current-ai-computing-needs", source: Fox Business, date: "2026-02-23"}
- {id: 43, title: "What is Sundar Pichai's timeline for AI data centers in space?", url: "https://fortune.com/article/what-is-google-ceo-sundar-pichai-timeline-ai-data-centers-in-space", source: Fortune, date: "2025-12"}
- {id: 44, title: "Bezos predicts data centers in space within 20 years", url: "https://www.techzine.eu/news/infrastructure/135156/bezos-predicts-data-centers-in-space-within-20-years/", source: Techzine, date: "2025-10-03"}
- {id: 45, title: "ESA Space Environment Report 2025", url: "https://www.esa.int/Space_Safety/Space_Debris/ESA_Space_Environment_Report_2025", source: ESA, date: "2025-04-01"}
- {id: 46, title: "Starlink satellites now dodging collisions almost weekly as maneuvers triple in a year", url: "https://starpath.global/news/starlink-satellites-now-dodging-collisions-almost-weekly-as-maneuvers-triple-in-a-year/", source: Starpath, date: "2026-07-15"}
- {id: 47, title: "SpaceX wants a million satellites for orbital datacenters", url: "https://www.theregister.com/2026/02/05/spacex_1m_satellite_datacenter/", source: The Register, date: "2026-02-05"}
- {id: 48, title: "The hype around orbital data centers", url: "https://spectrum.ieee.org/orbital-data-center-hype", source: IEEE Spectrum, date: "2026-07-01"}
- {id: 49, title: "Backlog of power plants seeking grid connection eased somewhat in 2025: LBNL", url: "https://www.publicpower.org/periodical/article/backlog-power-plants-seeking-transmission-grid-connection-eased-somewhat-2025-lbnl", source: American Public Power Association, date: "2026-07-01"}
- {id: 50, title: "Workload suitability for orbital compute", url: "https://arxiv.org/html/2603.20317v1", source: arXiv 2603.20317, date: "2026-03-19"}
- {id: 51, title: "SpaceX IPO filing flags orbital data centres may not be commercially viable", url: "https://thenextweb.com/news/spacex-orbital-data-centres-ipo-risk-disclosure", source: The Next Web, date: "2026-04"}
- {id: 52, title: "Google thinks a SpaceX Starship launch could change orbital data center economics (TechCrunch, syndicated)", url: "https://tech.yahoo.com/ai/gemini/articles/google-thinks-spacex-starship-launch-191803210.html", source: TechCrunch via Yahoo Tech, date: "2026-10-01"}
:::

