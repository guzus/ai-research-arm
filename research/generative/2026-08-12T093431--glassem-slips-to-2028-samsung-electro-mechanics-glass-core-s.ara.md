---
eyebrow: REPORT · ADVANCED PACKAGING
domain: semiconductor
title: "GlaSSEM and the 2028 date: what Samsung Electro-Mechanics actually said, and why a glass-substrate delay postpones almost nothing"
deck: Two of the premise's three claims are factually wrong. The third is right for the wrong reason — and correcting it makes the outlook for glass worse, not better.
lede: |
  On 30 July 2026 Samsung Electro-Mechanics told analysts it is aiming for full-scale glass-substrate operation "from 2028." That statement has circulated as a slip — a program that was supposed to ship in 2026, pushed out two years, taking a chunk of the AI packaging roadmap with it. The framing needs three corrections, and they do not all run the same direction. GlaSSEM is not the delayed program; it is a separate glass-core materials joint venture announced four weeks earlier. The 2028 date was not leaked; SEMCO published it itself, as the first mass-production year it has ever put into a formal investor channel. But it is a genuine delay — and as of 12 August 2026 the same trade outlet that transcribed the call reports the schedule has moved again, blocked by a customer reliability evaluation SEMCO failed. What that postpones, on the evidence, is remarkably little: the 2027–2029 accelerator roadmap runs on organic substrates, financed by roughly eight times more committed capital, and the technology it would displace is the one TSMC calls a bottleneck.
stats:
  - {label: SEMCO glass MP target, value: "2028", note: "and reported slipping again"}
  - {label: GlaSSEM JV capital, value: "₩482.1B", note: SEMCO 66% / Dongwoo 34%}
  - {label: Public glass design wins, value: "0", note: as of 2026-08-12}
  - {label: Organic vs glass capex, value: "~8×", note: new 2026–28 commitments}
---

## 01. The short answer

The question as posed — "GlaSSEM slips to 2028, and what does that postpone?" — bundles three claims. Two fail outright on the record. The third survives, but for a different and more damaging reason than the question assumes.

:::callout(kind=warn, label="Three corrections")
**GlaSSEM is not the program that slipped.** It is the tentative name of a glass-*core materials* joint venture between Samsung Electro-Mechanics and Sumitomo Chemical's Korean subsidiary Dongwoo Fine-Chem, announced 2 July 2026 — the acronym encodes Glass + Samsung + Sumitomo + Electronic + Materials.[^4,5]

**2028 was not leaked, and it is not late by industry standards.** SEMCO said it on its own Q2 2026 earnings call, in the phrase "본격 가동" — full-scale *operation* — and it is the first specific mass-production year the company has ever given through an investor-relations channel rather than a trade-show press scrum.[^1,2] Measured against every competitor that has published a date, 2028 sits at the front of the pack.

**It is nonetheless a real delay, with a named mechanism.** Reporting on 12 August 2026 attributes the movement to a bottleneck in customer prototype reliability evaluation that SEMCO did not pass, and says the GlaSSEM line's own equipment-order schedule has slipped at least three times.[^18]

**And almost nothing downstream is postponed.** The 2027–2029 AI accelerator roadmap is being built on organic ABF substrates, financed by roughly 8× more committed capital than glass has attracted, and TSMC's own packaging executive names memory and ABF supply — not glass — as the binding constraints.[^33,34,44]
:::

What survives the correction is a harder story than "Samsung is behind." Glass-core substrates are a genuine engineering advance with a real physical rationale, moving at the pace such advances actually move: pilot lines that run, coupons that pass, and a demand side that has committed nothing. The delay is real. Its consequences are not.

:::kv
- {term: What GlaSSEM is, def: "Glass-core materials JV, SEMCO 66% / Dongwoo Fine-Chem 34%, ₩482.1bn capital, Pyeongtaek"}
- {term: What it makes, def: "Glass cores — the blank; SEMCO builds the finished substrate around it"}
- {term: JV supply-system date, def: "2H fiscal 2027 as announced; equipment orders since deferred three times"}
- {term: SEMCO substrate date, def: "Full-scale operation from 2028; reported 12 Aug 2026 as \"2028 or later\""}
- {term: Named customers, def: "None. Some at \"technology approval and sample evaluation\""}
:::

## 02. What was actually said, and where

The record matters because the "slip" narrative depends on treating two very different kinds of statement as the same thing.

Every pre-2026 date traces to a press scrum or a trade-show briefing. At a CES 2024 press event on 10 January, CEO Jang Duck-hyun described a pilot line in 2024, a prototype in 2025, and a full mass-production system in 2026 — though the same article's headline hedged it to "after '26," so even the founding target was internally inconsistent.[^8] Three months later, at a doorstep after a Seoul National University lecture, the target had already widened to "2026~2027."[^9] At the March 2025 shareholder meeting Jang said SEMCO was developing both a glass interposer and a glass core, would run Sejong pilot production from Q2 2025, and expected the substantive market to open in "2027, 2028."[^10] In September 2025, at the KPCA Show, package marketing leader Lee Seung-eun put product launch at 2027–2028.[^11]

None of that was guidance. It was executives answering reporters. The FY2025 results call in January 2026 said only that SEMCO would reach mass production "in time" for lead customers — deliberately dateless. The 30 July 2026 call is the first time a specific year entered an IR channel, and ETNews's own headline renders it as a target, not a retreat: "유리기판 2028년 양산 목표."[^1]

:::timeline
- {date: "2024-01-10", headline: "CES 2024 press briefing", body: "CEO Jang: pilot line 2024, prototype 2025, \"full mass-production system\" in 2026. Same article headline hedges to \"after 2026.\"[^8]"}
- {date: "2024-04-11", headline: "Doorstep remarks, Seoul", body: "Target restated as a band: mass production \"2026~2027.\"[^9]"}
- {date: "2025-Q2", headline: "Sejong pilot line runs", body: "Pilot production from Q2 2025; prototype substrates only, no disclosed capacity or panel format.[^10]"}
- {date: "2025-05", headline: "ECTC 2025", body: "SEMCO's disclosed coupon: 40 µm TGVs, 8 build-up layers on a 640 µm core, 80 × 80 mm body. Board- and system-level reliability \"as yet unknown.\"[^12]"}
- {date: "2025-09-03", headline: "KPCA Show", body: "Marketing lead puts launch at 2027–2028 and sets the glass crossover at 120–140 mm body size.[^11]"}
- {date: "2026-07-02", headline: "GlaSSEM JV announced", body: "₩482.1bn glass-core JV with Dongwoo Fine-Chem; supply system targeted 2H FY2027.[^4]"}
- {date: "2026-07-30", headline: "Q2 2026 earnings call", body: "First IR-channel date: full-scale operation \"from 2028.\" Three outlets report it independently within 75 minutes.[^1,2,3]"}
- {date: "2026-08-12", headline: "Reliability bottleneck reported", body: "THE ELEC: schedule pushed to \"2028 or later\"; cause given as a failed customer prototype reliability evaluation; GlaSSEM equipment orders deferred three times.[^18]"}
:::

One detail is worth preserving because it is routinely mistranslated. SEMCO said *가동* (operation), not *양산* (mass production); the full-transcript outlet reproduces 가동, while a third outlet paraphrased to 양산.[^2,3] The distinction is not pedantry — "full-scale operation of a line" and "volume production of a qualified part" are separated, at every substrate maker in history, by exactly the customer qualification cycle that has now become the reported blocker.

:::callout(kind=danger, label="The 12 August report")
The most consequential source in this piece was published the day it was written. THE ELEC reports that SEMCO's glass investment schedule "is being pushed back" because "a bottleneck has emerged in the customer's prototype reliability evaluation," with a source saying the schedule was halted "as Samsung Electro-Mechanics failed to pass the reliability evaluation." It frames the Q2 call as having *revised* start-up timing to 2028 less than a month after the JV announced 2H 2027, and reports GlaSSEM "has been unable to convey an equipment order schedule to partner firms," with dates slipping "at least three times — to last December, then March, then June this year."[^18]

Two caveats travel with it. It is attributed entirely to unnamed industry officials, with no named spokesperson and no filing. And it is one outlet — though it is the same outlet that published the verbatim call transcript this article relies on elsewhere. Treat it as well-sourced trade reporting, not as disclosure.
:::

:::callout(kind=info, label="Provenance note")
SEMCO's own published newsroom release for Q2 2026 contains no reference to glass substrates, the joint venture, or 2028; the company's Package commentary says only that demand for high-value data-centre FC-BGA will stay strong.[^7] The 2028 date exists solely as spoken conference-call commentary. Anyone citing it as company guidance is citing a journalist's transcription of an unnamed executive — accurate, corroborated three ways, and still not a filed document.
:::

## 03. GlaSSEM is a supply-chain move, not a program rename

The joint venture is the most informative thing SEMCO did in 2026, and reading it as "the glass program" misses what it says.

Sumitomo Chemical's own release gives the terms: a company tentatively named GlaSSEM, capitalised at ₩482,100 million, owned 66% by Samsung Electro-Mechanics and 34% by Dongwoo Fine-Chem, sited in Pyeongtaek, whose business is "development, manufacturing, and sales of glass core substrates for advanced semiconductor packages," with a supply system to be established "by the second half of fiscal 2027."[^4] SEMCO's Korean filings put its stake at 66.2%.[^1] Note the site: Pyeongtaek is inside Dongwoo Fine-Chem's plant — a different campus from SEMCO's Sejong substrate operation.[^4]

That 2H FY2027 date is the source of much of the confusion in circulation. Japanese fiscal 2027 ends in March 2028, so "2H FY2027" plausibly means October 2027 to March 2028, which would make the JV and substrate dates a sequential ramp — cores first, finished substrates a beat later.[^4] Outlets reporting "SEMCO targets 2H2027 mass production" were reporting the core-material date and attaching it to the substrate.[^31] That reconciliation now looks too generous: the 12 August reporting says the JV's own line build has been deferred repeatedly, so the two dates are not a clean relay but two schedules moving together.[^18]

The strategically interesting part is what the JV admits. A ₩482 billion vehicle to secure glass *blanks* is an acknowledgement that the raw panel is not a commodity SEMCO can simply buy. The published supply base is thin and rigid: SCHOTT sells a standard 510 × 515 mm format in four CTE grades from 3.2 to 7.2 ppm/K, with total thickness variation guaranteed only to 10–20 µm and warp to 100–200 µm — floor commitments, with tighter specs available only on request.[^40] Nippon Electric Glass's glass-ceramic cores run 6.1–8.9 ppm/°C, and NEG chose its 515 × 510 mm format so that it "will enable semiconductor manufacturers to use the equipment they currently use and reduce capital investment" — a format chosen by installed tool base, not by physics.[^41,42]

Against that, ₩482 billion is small: about 4.3% of SEMCO's FY2025 revenue of ₩11.31 trillion.[^45] It is a call option on a materials position, not a capital commitment of consequence — and it is the only hard KRW figure SEMCO has ever attached to glass. **No Sejong glass pilot-line investment figure has ever been publicly disclosed.**

## 04. 2028 is not late — it is the front of the pack

The delay framing collapses fastest when the date is compared with anyone else's.

| Player | Stated glass-core volume date | Evidence quality |
|---|---|---|
| *Samsung Electro-Mechanics | **2028**, reported slipping further | Earnings call, three outlets; delay report[^1,2,18] |
| Absolics / SKC | 2027 capacity per US government page; still pre-PoC | NIST project page; SKC Q2 call[^22,26] |
| Dai Nippon Printing | Fiscal 2028 (ends March 2029) | Company plan via trade press[^30] |
| LG Innotek | 2030, moved out from ~2028 | CEO at CES 2026, as reported[^29] |
| Intel | "Second half of this decade" (2023) → ~2030 | Newsroom, then trade press[^16,19] |
| TSMC | Glass core "after 2030"; CoPoS panel first | Analyst reconstruction[^32] |

Absolics is the instructive case, because it is the most advanced merchant supplier and the one with public money behind it. It holds up to $75 million in CHIPS direct funding against $343 million of expected capex for a 120,000 sq ft Covington, Georgia facility, plus a separate $100 million NAPMP award — the first US national program whose solicitation named glass explicitly as one of three substrate categories.[^22,24,25] SK's own marketing page claimed high-volume manufacturing "in 2025" alongside up to 50% power reduction and 30% signal improvement.[^27] The US government's project page still says "first deliveries to customers are expected in 2025 and production capacity is expected to kick in 2027."[^22]

What actually happened: as of SKC's Q2 2026 call on 27 July, Absolics samples had progressed substrate-level testing in Georgia and electrical evaluation in Japan, and had only just begun *initial* package-level reliability evaluation in Taiwan — a stage before proof of concept, let alone revenue.[^26] SKC earmarked ₩589.6 billion of rights-offering proceeds for the glass business, aimed at customer certification, yield and equipment.[^26,28]

:::slope(left-label="First stated", right-label="Current", unit="")
| Player | First | Current |
|---|---|---|
| Samsung Electro-Mechanics | 2026 | 2028 |
| Absolics / SKC | 2025 | 2027 |
| LG Innotek | 2028 | 2030 |
:::

The pattern is not one company slipping. It is every company slipping about two years, in the same two years — the signature of a technology whose difficulty was systematically underestimated across the field, rather than one whose champion stumbled. LG Innotek's CEO is reported to have said the quiet part: development is "completed," but "current demand is still insufficient to absorb the full production capacity such an investment would create."[^29]

Counterpoint worth taking seriously: a demand-framed delay is also the most face-saving way to announce a yield problem, and LG Innotek is the least advanced of the three Korean entrants — so its framing should not be generalised without support. SEMCO's own reported blocker, notably, is not demand but reliability.[^18]

## 05. Four mechanisms, not one "manufacturing challenge"

Schedule slips in packaging are always specific. Four failure modes recur across the published record, and none is close to retired. That SEMCO's reported blocker is a *reliability* evaluation rather than a capacity or demand problem points directly at this list.[^18]

**Via formation is not the bottleneck; the etch is.** Laser modification of glass runs at thousands of vias per second, and LPKF specifies up to 1:50 aspect ratio at 5 µm minimum diameter with ±1 µm positional accuracy across a 515 × 510 mm panel.[^60] But the laser only writes a modified track — a wet etch opens it. A peer-reviewed process needed roughly **nine hours in 8 mol/L KOH at 110 °C** to open vias in 100 µm glass, at a previously reported 333× selectivity, and the etch thins the whole panel while it works.[^37] Production etchants are proprietary and faster, but the cycle-time and cost driver sits in the bath, not the laser.

**Copper does not stick to glass.** Glass is atomically smooth — surface roughness of 0.28 nm — which is exactly why lithography likes it and exactly why plating does not. Measured adhesion of copper to bare glass is 72 ± 18 gf/cm against a practical target above 500; an engineered porous titania promoter reaches 1,392 ± 64 gf/cm, but at a 600 °C sinter that is incompatible with organic build-up flows.[^36]

:::compare
- {role: LOWEST, name: "Copper on bare glass", value: "72 gf/cm"}
- {role: HIGHEST, name: "With porous TiO₂ promoter", value: "1,392 gf/cm"}
- {role: SUBJECT, name: "Practical target", value: "> 500 gf/cm"}
:::

**Glass cracks at the edges.** Toppan named back-cracking (*seware*) and second-level reliability as its glass-core blockers at ECTC 2025.[^39] At ECTC 2026 STATS ChipPAC reported that 74 × 74 mm glass-core packages **failed every reliability test segment without edge coating**, and that edge coating cut warpage 33.5%.[^15] That failure size sits *below* the 80 × 80 mm coupon SEMCO demonstrated a year earlier — a reminder that "demonstrated" and "yielding" are different verbs.

**Nobody has published board-level reliability.** The single most revealing line in SEMCO's ECTC 2025 disclosure is the caveat: board- and system-level reliability "are as yet unknown."[^12] The best public glass-core reliability datapoint remains DNP's stress-relief-resin structure — 80 µm vias in a 400 µm core surviving 1,000 hours of −55 °C to 150 °C — at a 5:1 aspect ratio, roughly four times easier than Intel's 20:1 target, with sample size and failure criterion unreported.[^39]

A disclosure gap compounds this. SEMCO authored no glass-core paper at ECTC in 2024, 2025 or 2026; in the ECTC 2026 program the company appears twice as a panellist on non-glass sessions and once as a co-author affiliation on a lithography-metrology paper, while the glass-core block belongs to Intel, Georgia Tech, DNP, Samsung *Electronics* and others.[^14] Its ECTC 2025 numbers reached the public as the session moderator's notes, and the archived special-session deck carries slides from AMD, TSMC and Toppan but none from SEMCO.[^12,13] A company two years from volume that publishes no peer-reviewed reliability data is either protecting a lead or does not have the data. The 12 August report suggests the latter.[^18]

## 06. The CTE paradox: glass may be matched to the wrong thing

This is the deepest technical objection in the literature, and it inverts the standard sales pitch.

The pitch is that glass's coefficient of thermal expansion — 3–8 ppm/°C — sits close to silicon's 2.6, so a glass-cored package warps less than an organic one at 9–20 ppm/°C. That is true and measured: Amkor and STATS ChipPAC reported 30–40% lower substrate warpage versus organic references.[^15] TSMC's first reported glass validation, on an 85 × 110 mm five-reticle package, is said to show 16% better warpage alongside 27% lower power-supply resistance and 42% lower inductance — though the reporting names no primary TSMC document, so treat the figures as reported rather than published.[^56]

But a package has two interfaces, not one. Below the substrate is a printed circuit board at roughly 18 ppm/°C. Matching the core to the die necessarily *un*-matches it from the board. Finite-element work published in September 2025 quantifies the trade: with a 4.8 ppm/°C glass core, accumulated inelastic strain in the corner solder joint reached **19% per cycle**, against **8.43%** for an organic core — more than twice the thermal-fatigue damage at the second level. In the companion hybrid-bonding case, raising the glass CTE toward 10 ppm/°C cut warpage 48% and strain 50%, and the authors recommend matching the core to the *board*, not the die.[^35]

:::bars
- {label: "Organic core — corner solder joint strain", value: "8.43%/cycle", pct: 44}
- {label: "Glass core, 4.8 ppm/°C — corner solder joint strain", value: "19%/cycle", pct: 100}
- {label: "Glass core, hybrid-bonding case, CTE raised toward 10 ppm/°C", value: "16% → 8%/cycle", pct: 42}
:::

This is not a fringe view. At ECTC 2025, Unimicron and Shinko — the two largest organic incumbents — argued that low-CTE glass is itself the problem and that a *higher*-CTE core is needed for board-level reliability.[^39] Nippon Electric Glass already sells glass-ceramic cores at 6.1–8.9 ppm/°C aimed explicitly at organic matching rather than silicon.[^41] And SCHOTT ships four CTE grades precisely because the industry has not decided which number it wants.[^40]

The honest caveats: the strain study is simulation on a 20 × 20 mm substrate with no cycles-to-failure measured, and the cited page lists no author affiliations, so any claim about the authors' commercial alignment is inference rather than fact.[^35] Glass's warpage advantage is also largest at exactly the 100 mm-plus bodies the simulation does not cover. The finding is a real constraint on the claim, not a refutation of glass.

The residual mismatch, meanwhile, is not in the core at all: copper at ~16.4 ppm/°C inside a near-zero-CTE glass leaves roughly 260 MPa of residual stress at the via edge after a 260 °C reflow excursion, and thickening surface redistribution from 5 µm to 15 µm raises that stress about 22%.[^38] The stress moved from the core into the vias and the RDL. It did not go away.

## 07. Follow the capital: organic is winning by an order of magnitude

If glass were about to displace organic substrates, the capital would already be moving. It is moving the other way, and the gap is the most decisive number in this analysis.

:::rank-list
- {label: "Ibiden — AI-server IC package substrates, FY2026–28", value: "¥500bn (~$3.3bn)", pct: 100}
- {label: "AT&S — high-end IC substrates, Kulim", value: "€1.5–2.0bn (~$2.0bn)", pct: 61}
- {label: "SEMCO — FC-BGA capacity, 2026", value: "> ₩1tn (~$0.66bn)", pct: 20}
- {label: "SKC → Absolics — glass, first tranche", value: "₩589.6bn (~$0.39bn)", pct: 12, highlight: true}
- {label: "GlaSSEM JV — glass cores, total capital", value: "₩482bn (~$0.32bn)", pct: 10, highlight: true}
:::

Ibiden's February 2026 board notice commits approximately ¥500 billion across fiscal 2026–2028 to high-performance IC package substrates for AI and high-performance servers, with a ¥220 billion first phase at the Gama plant and mass production from fiscal 2027. The release does not contain the word glass.[^33] AT&S disclosed that a €1.5–2.0 billion expansion is "fully supported and financed by long-term customer commitments" — with the release adding that those commitments "remain subject to final negotiation and execution" — while raising revenue growth guidance from 30–35% to 45–55% and lifting capex plans from €400 million to €1.0–1.2 billion.[^34]

That financing mechanism is the one that matters. The substrate transition is being funded by the **chip designer**, through take-or-pay commitments and advance payments — and every disclosed prepay is for conventional build-up substrates. The same customers running glass at qualification scale are prepaying billions for incumbent capacity in the identical window.

On new 2026–2028 capacity commitments the arithmetic is roughly $5.7–6.3 billion of incumbent-substrate money against roughly $0.71 billion of fresh glass money — the SKC tranche plus the GlaSSEM JV — or about 8×. Adding Intel's cumulative $1 billion-plus Chandler glass R&D line, spent over roughly five years on a line that has produced no product, brings the all-in ratio to roughly 3.5×.[^17,33,34] Either way the direction is the same, and currency conversions here are approximate and directional only.

:::callout(kind=warn, label="What the asymmetry means")
Announced capex is a claim about the *next* three years, made by people with cost-of-capital discipline and customer contracts in hand. Incumbent substrate makers are building qualified capacity against signed demand. Glass players are funding qualification. Those are different activities, and no amount of TAM forecasting reconciles them.
:::

Forecast disagreement is itself evidence. Counterpoint projects a market growing "from approximately $650 million in 2024 to more than $8.1 billion by 2030" — but that figure is explicitly "the combined FOPLP and glass substrate market," bundling panel-level fan-out, which already ships in volume, with glass, which does not.[^20] ==Yole is reported to size glass-core specifically in the multi-hundred-million range by 2030 inside a roughly $31 billion advanced-IC-substrate market — implying penetration on the order of 1–2% — but this analysis could not reach a primary Yole document to verify either figure, and both should be treated as unconfirmed.== Averaging estimates built on different definitions would be malpractice.

## 08. The demand-side vacuum

Here is the finding that should worry a glass bull far more than any schedule.

**As of August 2026, no chip designer or substrate supplier has publicly disclosed a signed supply agreement, capacity reservation, or qualified design-in for a glass-core substrate.** Not one.

The evidence ladder for the entire category stops early: sampling ✓ → performance evaluation ~ → qualification ✗ → capacity reservation ✗ → supply agreement ✗ → shipping ✗. Absolics — CHIPS-funded, fab complete, the most advanced merchant supplier — names no customer on its own website, and SKC's latest disclosed milestone is pre-PoC package-level reliability testing.[^26,59] SEMCO says only that "some customers" are at "technology approval and sample evaluation."[^1,2]

Run the named-customer claims to ground and they thin out:

- **Nvidia.** No first-party glass-substrate statement exists. Its largest "glass" commitment is the May 2026 Corning partnership — which covers optical fiber, connectivity and photonics, and never uses the words substrate or packaging.[^48] The conflation of drawn optical fiber with package substrates is the most common error in this narrative.
- **AMD.** The only named AMD employee on record, senior fellow Deepak Kulkarni, calls glass a technology with "enormous potential for the future of energy-efficient AI compute" — the language of an evaluation, not a design-in.[^47] AMD's disclosed packaging for MI400-class parts is 3.5D with HBM4.
- **Apple and Broadcom.** Both trace to a single Korean exclusive attributed to an unnamed industry official, and it describes sample supply, not a contract or order.[^50] No first-party confirmation from any of the three companies.
- **AWS.** Reported in November 2025 to have delayed its glass quality test "indefinitely," and separately reported in 2026 to be testing prototypes. The contradiction is unresolved.[^49] Meanwhile the one hyperscaler accelerator whose packaging is documented in detail, Trainium3, ships on CoWoS-R over a 20-layer organic ABF substrate.[^57]

Against that, the counter-argument deserves its due: hyperscalers and fabless designers routinely keep packaging confidential, so absence of a public design win is not proof of absence. But the asymmetry cuts hard. A supplier that raised over half a trillion won on this thesis, and a JV capitalised at ₩482 billion, both have every incentive to announce a named anchor customer — and neither does. The 12 August reporting supplies the likely reason: the customer evaluation has not been passed.[^18]

:::statement(attr="ARA Research")
A supply-side bet this large with a demand side this quiet is not a delayed transition. It is an option being kept alive until someone exercises it.
:::

## 09. So what does 2028 actually postpone?

Very little on the capability axis, and that is this article's central claim.

The AI accelerator roadmap through 2029 scales on **interposer area and package body size**. The published CoWoS ladder starts at 1.5 reticles in 2016 and steps through 3.3, then 5.5 on a 100 × 100 mm substrate carrying 12 HBM4 stacks, reaching 9 reticles — 7,722 mm² — on a body beyond 120 × 120 mm targeted for 2027.[^43] A 14-reticle step is reported for 2028, with the 5.5-reticle generation already in mass production above 98% yield.[^44] None of the cited roadmap sources place a glass core in any of those steps, and TSMC's own glass-core timing is reported as post-2030 — a generation behind its 310 × 310 mm CoPoS panel transition.[^32]

:::line-chart(title="TSMC CoWoS maximum reticle multiple by year", subtitle="Reticle = 26 × 33 mm = 858 mm². No cited roadmap step specifies a glass core.", y-unit="")
x: 2016,2024,2026,2027,2028
Reticle multiple: 1.5,3.3,5.5,9,14
:::

More telling still: asked what constrains AI packaging, TSMC's VP of advanced packaging named memory shortages and tight ABF substrate supply over the next few years.[^44] Not glass. Not the absence of glass. **Tight supply of the incumbent material** — a volume problem, which capex solves, not a capability problem, which only a new material solves.

The second confusion worth dissolving is between glass and panel-level packaging. They are separable transitions:

- **Glass carriers** — temporary, debonded before the part ships — are in volume production today.
- **Panel-level packaging** is a line *form factor*, material-agnostic. Taiwanese panel makers already run fan-out panel-level packaging in volume at up to 620 × 750 mm for mature-node PMIC and RF parts.[^32] ASE targets FOPLP mass production by end-2026 on a 310 × 310 mm line aimed at AI and chiplet applications.[^21]
- **Glass core substrates** are at pilot and qualification.
- **Glass interposers** are earliest-stage of all.

Intel's ECTC 2026 demonstration makes the separability concrete: its 510 × 515 mm, 24-layer glass-core panel with copper-filled TGVs, embedded EMIB bridges and optical waveguides was **processed on existing organic-substrate lines**.[^15] The panel transition does not require glass, and glass does not require the panel transition. If CoPoS reaches pilot in 2027 and volume in 2H 2028 on 310 × 310 mm, the "2028 AI packaging transition" is a form-factor change, not a materials change.[^32]

What a 2028 glass date genuinely does postpone is narrower and mostly economic:

1. **Cost relief on very large bodies.** Panel area utilisation improves with package size. By ARA's own calculation, a 120 × 120 mm package fits 16 to a 510 × 515 mm panel — 16 × 14,400 mm² over 262,650 mm², or 87.7% utilisation — against just 2 on a 300 mm wafer of 70,686 mm², or 40.7%, because a 2 × 2 block would put its corner at a radius of 169.7 mm on a 150 mm wafer. That is a cost argument, and cost arguments can wait.
2. **Warpage headroom above ~120 mm.** SEMCO's own marketing lead puts the crossover where CCL cores run out at 120–140 mm per side.[^11] Analyst reporting says Nvidia's response to substrate warpage on Rubin Ultra was to cut the part from four compute dies to two rather than adopt glass — retreating from the constraint rather than going through it, though Nvidia has publicly disputed downgrade claims.[^23]
3. **Co-packaged optics with glass waveguides**, which Intel has demonstrated at panel scale but nobody has committed to in a product.[^15]

And here is the uncomfortable arithmetic for the whole category: SEMCO's largest *demonstrated* glass body is 80 × 80 mm, with 105 × 105 mm stated only as a target and never publicly confirmed as met.[^12] Its own stated crossover threshold is 120–140 mm.[^11] The demonstrated body is smaller than the size at which the company's own engineers say glass becomes necessary.

## 10. What would falsify this

This analysis is a bear case on timing, not on physics, and it has identifiable failure points.

**It breaks if a named design win appears.** A single disclosed supply agreement — AMD, Broadcom, an OpenAI-Broadcom custom part, a hyperscaler ASIC — for a 2028 product on a glass core would invert the demand-vacuum argument overnight. The evidence for "zero design wins" is evidence of absence, bounded by legitimate confidentiality and by paywalls that hid body text from this research.

**It breaks if organic hits a wall sooner than expected.** The reported roadmap runs to 14 reticles in 2028, but TSMC's own ABF tightness and the reported Rubin Ultra die-count reduction both suggest strain.[^44,23] If a 2028 flagship cannot be built on organic at acceptable yield, glass stops being a cost option and becomes a requirement, and every date compresses.

**It breaks if the CTE objection is solved rather than traded.** The strain finding assumes today's low-CTE cores; NEG already ships 6.1–8.9 ppm/°C glass-ceramics and SCHOTT ships four grades.[^40,41] If a mid-CTE core delivers the warpage win without the second-level penalty, the deepest technical objection here evaporates.

**Beware one widely circulated false datapoint.** Several aggregators have claimed Intel took glass substrates into high-volume manufacturing with Clearwater Forest at CES 2026. No primary Intel source supports it, and the packaging attributed to that part in credible coverage is Intel 18A with Foveros Direct, not glass. Intel's glass remains a Chandler pilot line with commercialisation reported around 2030.[^19]

**The sourcing has known weak points.** The Apple, Broadcom and AWS customer claims rest on unnamed Korean sourcing recycled through aggregators — one chain, not independent corroboration.[^49,50] The TSMC glass validation percentages come from an aggregator naming no primary document.[^56] The pivotal 12 August delay report is single-outlet and entirely unnamed-source.[^18] Share-price data for SEMCO is inconsistent across vendors; the ₩1,335,000 close on 12 August 2026 reconciles against published market cap and share count, but aggregator valuation ratios for this security are internally contradictory and should not be cited.[^55]

**And the base rate cuts both ways.** Rao Tummala's Georgia Tech group claimed 2× to 10× interposer cost savings from glass in 2012; fourteen years later no glass interposer has reached volume.[^58] The counter-case is that the physics is real and the incumbents concede it: Amkor and STATS ChipPAC measured 30–40% warpage improvement, and Intel has built a 24-layer glass panel that works.[^15] Nobody in this debate argues glass cannot be made. They argue about when it can be made profitably, in volume, with board-level reliability — and on that question the published evidence still says "not yet."

The one thing state money says is that nobody is waiting on subsidy. Korea named next-generation glass package substrates as a cooperation model only on 6 August 2026 — six days before this writing — inside a ₩91 billion five-year envelope shared across five projects, and its flagship advanced-packaging program names chiplet, 3D, 2.5D and fan-out without mentioning glass at all.[^51,52] The US has committed the most glass-specific public money, $175 million to Absolics, on milestones that encode 2025 and 2027 dates the company has already missed.[^22,24] Public money is not setting this clock. Defect rates and customer qualification are — which is precisely what the 12 August reporting says stopped SEMCO.[^18]

Finally, the institutional memory. In 2019 Samsung Electro-Mechanics sold its panel-level packaging business — built for ₩264 billion, world-first into a Galaxy Watch package — to Samsung Electronics for ₩785 billion, saying it lacked the capital for the required scale-up. Samsung Electronics wrote off the entire ₩206.7 billion of goodwill within a year.[^53,54] The parallel is imperfect and no source draws it. But SEMCO has exited a capital-intensive packaging platform at the scale-up step before, and the question its glass program will face in 2028 is the same one: who funds the fab.

:::note
Red-team pass: 2 of 3 top claims survived an adversarial search unbroken; the third — that 2028 is not a delay — was contradicted by same-day reporting and has been revised in the text rather than defended. Volatile figures carry an explicit as-of date; share price and market data are as of 2026-08-12. Currency conversions are approximate and directional. The panel-utilisation figures in section 09 are ARA's own calculation from the stated dimensions.
:::

:::references
- {id: 1, title: "삼성전기 \"AI·전장 고성장 시장 집중\"…유리기판 2028년 양산 목표", url: "https://www.etnews.com/20260730000332", source: ETNews, date: "2026-07-30"}
- {id: 2, title: "삼성전기 2026년 2분기 실적발표 컨퍼런스콜 전문", url: "https://www.thelec.kr/news/articleView.html?idxno=60326", source: THE ELEC, date: "2026-07-30"}
- {id: 3, title: "삼성전기, 유리기판 합작법인 지분 66.2% 확보", url: "https://www.ddaily.co.kr/page/view/2026073014381730009", source: Digital Daily, date: "2026-07-30"}
- {id: 4, title: "Establishment of a Joint Venture for Glass Core Substrates", url: "https://www.sumitomo-chem.co.jp/english/news/detail/20260702e_2.html", source: Sumitomo Chemical, date: "2026-07-02"}
- {id: 5, title: "GlaSSEM naming and glass-core JV structure", url: "https://www.thelec.net/news/articleView.html?idxno=11916", source: THE ELEC, date: "2026-07-02"}
- {id: 7, title: "2026년 2분기 경영실적 발표", url: "https://www.samsungsem.com/kr/newsroom/news/view.do?id=10461", source: Samsung Electro-Mechanics, date: "2026-07-30"}
- {id: 8, title: "삼성전기, CES 2024 기자간담회 — 유리기판 로드맵", url: "https://v.daum.net/v/20240111150003453", source: Daum News, date: "2024-01-11"}
- {id: 9, title: "장덕현 사장 \"내년 유리기판 시제품…2026~2027년 양산\"", url: "https://v.daum.net/v/20240412182107348", source: Daum News, date: "2024-04-12"}
- {id: 10, title: "삼성전기 주총 — 유리 인터포저·코어 기판 동시 대응", url: "https://zdnet.co.kr/view/?no=20250319103134", source: ZDNet Korea, date: "2025-03-19"}
- {id: 11, title: "삼성전기 \"유리기판 제품 출시 2027~2028년 예상\"", url: "https://www.thelec.kr/news/articleView.html?idxno=40301", source: THE ELEC, date: "2025-09-04"}
- {id: 12, title: "Glass Core vs RDL Interposer Substrates: Ready for Prime Time?", url: "https://www.3dincites.com/2025/07/glass-core-vs-rdl-interposer-substrates-ready-for-prime-time/", source: 3D InCites / TechSearch International, date: "2025-07-17"}
- {id: 13, title: "ECTC 2025 Special Session 4 — Glass Core", url: "https://ectc.net/wp-content/uploads/2025/06/ECTC2025_SpecialSession_4-Glass-Core.pdf", source: IEEE ECTC, date: "2025-06-01"}
- {id: 14, title: "76th ECTC Final Program", url: "https://ectc.net/wp-content/uploads/2026/05/76-ECTCFinal-Web.v2.pdf", source: IEEE ECTC, date: "2026-05-26"}
- {id: 15, title: "ECTC 2026 — advanced packaging roundup", url: "https://newsletter.semianalysis.com/p/ectc2026", source: SemiAnalysis, date: "2026-07-02"}
- {id: 16, title: "Intel Unveils Industry-Leading Glass Substrates", url: "https://newsroom.intel.com/artificial-intelligence/intel-unveils-industry-leading-glass-substrates", source: Intel Newsroom, date: "2023-09-18"}
- {id: 17, title: "IFTLE 587: Intel glass core substrate update", url: "https://www.3dincites.com/2024/03/iftle-587-intel-glass-core-substrate-update/", source: 3D InCites, date: "2024-03-19"}
- {id: 18, title: "삼성전기 유리기판 투자 일정 지연…고객사 신뢰성 평가 병목", url: "https://www.thelec.kr/news/articleView.html?idxno=60802", source: THE ELEC, date: "2026-08-12"}
- {id: 19, title: "Intel reportedly eyes first glass substrate output at Rio Rancho", url: "https://www.trendforce.com/news/2026/05/26/news-intel-reportedly-eyes-worlds-first-glass-substrate-output-at-rio-rancho-offers-silicon-photonics-to-customers/", source: TrendForce, date: "2026-05-26"}
- {id: 20, title: "FOPLP and glass substrate market forecast to 2030", url: "https://counterpointresearch.com/en/insights/foplp-glass-substrate-forecast-2030-ai-hpc-demand", source: Counterpoint Research, date: "2026-06-22"}
- {id: 21, title: "ASE targets FOPLP mass production by end-2026", url: "https://www.trendforce.com/news/2026/06/25/news-ase-targets-foplp-mass-production-by-end-2026-launches-15-expansion-projects-this-year-amid-ai-boom/", source: TrendForce, date: "2026-06-25"}
- {id: 22, title: "CHIPS project profile: Absolics, Covington, Georgia", url: "https://www.nist.gov/chips/absolics-georgia-covington", source: NIST CHIPS Program Office, date: "2026-08-12"}
- {id: 23, title: "Nvidia Rubin Ultra reportedly cut from four dies on packaging limits", url: "https://www.techtimes.com/articles/319410/20260701/nvidia-rubin-ultra-four-die-gpu-cancelled-packaging-limits-cut-2027-performance-half.htm", source: Tech Times, date: "2026-07-01"}
- {id: 24, title: "Commerce announces $1.4 billion final awards to support next-generation packaging", url: "https://www.nist.gov/news-events/news/2025/01/us-department-commerce-announces-14-billion-final-awards-support-next", source: NIST, date: "2025-01-16"}
- {id: 25, title: "NAPMP materials and substrates NOFO — frequently asked questions", url: "https://www.nist.gov/chips/chips-rd-funding-opportunities/materials-and-substrates/frequently-asked-questions-national", source: NIST CHIPS R&D, date: "2024-11-21"}
- {id: 26, title: "SKC Q2 2026 earnings call — Absolics reliability validation status", url: "https://www.thelec.net/news/articleView.html?idxno=12584", source: THE ELEC, date: "2026-07-27"}
- {id: 27, title: "Absolics: how glass substrates are powering the AI revolution", url: "https://eng.sk.com/perspectives/absolics-how-glass-substrates-are-powering-the-ai-revolution", source: SK Group, date: "2026-08-12"}
- {id: 28, title: "SKC channels over half of ₩1tn capital increase into Absolics", url: "https://www.trendforce.com/news/2026/03/03/news-skc-reportedly-channels-over-half-of-%E2%82%A91t-capital-increase-into-absolics-to-fast-track-glass-substrates/", source: TrendForce, date: "2026-03-03"}
- {id: 29, title: "LG reportedly delays glass substrate commercialization to 2030", url: "https://www.trendforce.com/news/2026/01/13/news-lg-reportedly-delays-glass-substrate-commercialization-to-2030-on-demand-uncertainty/", source: TrendForce, date: "2026-01-13"}
- {id: 30, title: "DNP accelerates TGV glass substrate push with late-2025 pilot line", url: "https://www.trendforce.com/news/2025/12/22/news-dnp-accelerates-tgv-glass-substrate-push-with-late-2025-pilot-line-early-2026-sample-shipments/", source: TrendForce, date: "2025-12-22"}
- {id: 31, title: "Glass substrates eye 2027 launch, scale toward 2030", url: "https://www.trendforce.com/news/2026/06/05/news-glass-substrates-eye-2027-launch-scale-toward-2030-as-cowos-costs-rise-and-hyperscaler-demand-grows/", source: TrendForce, date: "2026-06-05"}
- {id: 32, title: "TSMC standardizes CoPoS on 310x310mm panels", url: "https://www.trendforce.com/presscenter/news/20260617-13107.html", source: TrendForce, date: "2026-06-17"}
- {id: 33, title: "Notice regarding capital investment plan for high-performance IC package substrates", url: "https://www.ibiden.com/company/2026/02/notice-regarding-capital-investment-plan-for-high-performance-ic-package-substrates.html", source: Ibiden, date: "2026-02-03"}
- {id: 34, title: "AT&S expands AI substrate capacity in Kulim and increases outlook for 2026/27", url: "https://www.eqs-news.com/news/ad-hoc/ats-austria-technologie-systemtechnik-ag-ats-expands-ai-substrate-capacity-in-kulim-and-increases-outlook-for-2026-27/1a92bc40-a144-4533-878c-cf31c886f44c_en", source: "AT&S ad-hoc release", date: "2026-06-13"}
- {id: 35, title: "Flip Chip on Glass-Core Substrates with Microbump and Cu-Cu Hybrid Bonding", url: "https://imapsjmep.org/article/144212-flip-chip-on-glass-core-substrates-with-microbump-and-cu-cu-hybrid-bonding", source: "Journal of Microelectronics and Electronic Packaging", date: "2025-09-15"}
- {id: 36, title: "Electroless copper adhesion to glass substrates via porous TiO2 promoters", url: "https://iopscience.iop.org/article/10.1149/1945-7111/adb5c9", source: "Journal of The Electrochemical Society", date: "2025-03-17"}
- {id: 37, title: "Laser-assisted wet etching of through-glass vias", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10536211/", source: PubMed Central, date: "2023-09-14"}
- {id: 38, title: "Thermal stress analysis of through-glass-via interposers", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC9607209/", source: PubMed Central, date: "2022-10-21"}
- {id: 39, title: "High-performance packaging dominates ECTC 2025", url: "https://pcdandf.com/pcdesign/index.php/current-issue/234-forefront/18793-storms-outside-breakthroughs-inside-high-performance-packaging-dominates-ectc", source: PCD&F, date: "2025-06-30"}
- {id: 40, title: "Glass panels for IC substrates — technical details", url: "https://www.schott.com/en-gb/products/glass-panels-p1001142/technical-details", source: SCHOTT, date: "2026-08-12"}
- {id: 41, title: "GC Core inorganic core substrate", url: "https://www.neg.co.jp/en/products/inorganic-core-substrate/index.html", source: Nippon Electric Glass, date: "2026-08-12"}
- {id: 42, title: "NEG develops GC Core glass-ceramic core substrate material", url: "https://www.neg.co.jp/en/news/20250115.html", source: Nippon Electric Glass, date: "2025-01-15"}
- {id: 43, title: "IFTLE 615: TSMC evolves CoWoS, promising 9x reticle size by 2027", url: "https://www.3dincites.com/2024/12/iftle-615-tsmc-evolves-cowos-technology-promising-9x-reticle-size-by-2027/", source: 3D InCites, date: "2024-12-24"}
- {id: 44, title: "TSMC's 5.5-reticle CoWoS reportedly tops 99% yield; flags memory, ABF as AI bottlenecks", url: "https://www.trendforce.com/news/2026/08/11/news-tsmcs-5-5-reticle-cowos-reportedly-tops-99-yield-flags-memory-abf-as-ai-bottlenecks/", source: TrendForce, date: "2026-08-11"}
- {id: 45, title: "2025년 연간 경영실적 — 매출 11조 3,145억원", url: "https://m.samsungsem.com/kr/newsroom/news/view.do?id=10041", source: Samsung Electro-Mechanics, date: "2026-01-28"}
- {id: 47, title: "Future AI chips could be built on glass", url: "https://www.technologyreview.com/2026/03/13/1134230/future-ai-chips-could-be-built-on-glass/", source: MIT Technology Review, date: "2026-03-13"}
- {id: 48, title: "NVIDIA and Corning announce long-term partnership", url: "https://nvidianews.nvidia.com/news/nvidia-and-corning-announce-long-term-partnership-to-strengthen-us-manufacturing-for-ai-infrastructure", source: NVIDIA Newsroom, date: "2026-05-06"}
- {id: 49, title: "Absolics glass substrate customer evaluation status", url: "https://www.thelec.net/news/articleView.html?idxno=5476", source: THE ELEC, date: "2025-11-04"}
- {id: 50, title: "삼성전기, 애플·브로드컴에 유리기판 샘플 공급", url: "https://www.thelec.kr/news/articleView.html?idxno=54740", source: THE ELEC, date: "2026-04-07"}
- {id: 51, title: "제16차 소재·부품·장비 경쟁력강화위원회 — 차세대 유리 패키지 기판 협력모델", url: "https://m.korea.kr/news/policyNewsView.do?newsId=148969611", source: "대한민국 정책브리핑", date: "2026-08-06"}
- {id: 52, title: "반도체 첨단패키징 선도기술개발사업 예타 통과", url: "https://www.motir.go.kr/kor/article/ATCL3f49a5a8c/169238/view", source: "MOTIE", date: "2024-06-26"}
- {id: 53, title: "삼성전기, PLP 사업 삼성전자에 7850억원에 양도", url: "https://www.thelec.kr/news/articleView.html?idxno=1535", source: THE ELEC, date: "2019-04-30"}
- {id: 54, title: "삼성전자, PLP 영업권 전액 손상차손 인식", url: "https://www.etoday.co.kr/news/view/2005730", source: etoday, date: "2021-03-18"}
- {id: 55, title: "삼성전기 (009150) 시세", url: "https://markets.hankyung.com/stock/009150", source: "Hankyung Markets", date: "2026-08-12"}
- {id: 56, title: "TSMC glass substrate CoWoS validation data", url: "https://finance.biggo.com/news/0FZvz54B5GWQxSUZ6mk3", source: BigGo Finance, date: "2026-06-16"}
- {id: 57, title: "AWS Trainium3 deep dive", url: "https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential", source: SemiAnalysis, date: "2025-12-04"}
- {id: 58, title: "Glass vs silicon interposers for 2.5D and 3D IC applications", url: "https://www.3dincites.com/2012/03/glass-vs-silicon-interposers-for-2-5d-and-3d-ic-applications/", source: 3D InCites, date: "2012-03-20"}
- {id: 59, title: "Absolics corporate site", url: "https://www.absolicsinc.com/", source: Absolics, date: "2026-08-12"}
- {id: 60, title: "LIDE technology — laser induced deep etching", url: "https://lide.lpkf.com/en/technology/lide", source: LPKF, date: "2026-08-12"}
:::
