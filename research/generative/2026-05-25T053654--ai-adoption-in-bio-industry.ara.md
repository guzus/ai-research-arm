---
eyebrow: REPORT · BIOTECH × AI
domain: biotech
title: AI in the bio industry — adoption is real, transformation is not (yet)
deck: A first-principles audit of where artificial intelligence has actually been adopted across drug discovery, the clinic, diagnostics and the lab — and where the evidence still stops at the door of human efficacy.
lede: |
  Almost every large pharma now calls itself "AI-first," billion-dollar AI-drug partnerships are announced monthly, and an AI-designed molecule has reached a randomized Phase 2 trial. Yet the economics that AI was hired to fix — a ~$2.6B cost per approved drug and a ~90% clinical failure rate — have not moved. The honest reading in mid-2026: AI is deeply, measurably adopted in the cheap upstream half of biology (structure, design, documents, diagnostics) and almost entirely unproven in the expensive downstream half (human efficacy and safety) where drugs actually live or die.
stats:
  - {label: Cost per approved drug, value: $2.6B, note: capitalized, DiMasi/Tufts}
  - {label: Programs reaching approval, value: 13.8%, note: of those entering Phase 1}
  - {label: AI/ML medical devices cleared, value: "1,000+", note: ~76% radiology}
  - {label: AI-designed drugs FDA-approved, value: "0", note: as of 2026-05}
---

The phrase "AI in the bio industry" hides at least five different industries: drug discovery, clinical operations, diagnostics, genomics, and the lab bench itself. They are at wildly different stages of adoption, and lumping them together is how both hype and dismissal get manufactured. This report separates them, demands primary evidence for each, and asks the only question that matters for a drug company: does the AI move a number that a regulator or a patient cares about?

:::kv
- {term: Where AI is genuinely adopted, def: "Protein structure (AlphaFold), generative molecule/protein design, medical imaging triage, variant interpretation, and back-office document drafting — all upstream, all measurable."}
- {term: Where adoption is shallow, def: "Clinical-stage efficacy. No AI-designed drug is approved; AI-origin molecules hit the same ~40% Phase 2 wall as everyone else."}
- {term: The money signal, def: "~$3B/yr of real VC flows in, but headline pharma 'deal values' are 95–98% contingent biobucks — Recursion has banked $213M of an announced $12B."}
- {term: The honest verdict, def: "AI compresses the ~32% of cost and time that sits in discovery; it has not yet been shown to fix the ~63% that sits in clinical attrition."}
:::

## 01. The $2.6B problem AI was hired to solve

The case for AI in biology starts with an economic emergency, not a technological one. The capitalized cost to bring a single new drug to approval is about {accent}$2.6 billion{/} in 2013 dollars, of which roughly $1.4B is out-of-pocket cash and the rest is the cost of capital over a ~10–15 year timeline.[^1] The US Congressional Budget Office, with no industry axe to grind, brackets the same figure at "less than $1 billion to more than $2 billion."[^6] The $2.6B headline is contested and discount-rate-sensitive: an independent JAMA analysis of 63 drugs put the median capitalized cost far lower, at ~$985M (mean $1.3B).[^67] Even that floor is severe, and Deloitte's most recent industry cohort put the cost at ~$2.23B per asset in 2024 — still rising.[^7]

Worse, productivity fell for decades. {accent}Eroom's Law{/} — Moore's Law spelled backwards — is the finding that new drugs approved per inflation-adjusted billion dollars of R&D halved roughly every nine years from 1950, an ~80-fold collapse {sparkline:80,40,20,10,5,2.5,1.2}.[^2] The decline only arguably bent upward after 2010, and that bend predates generative AI and is plausibly explained by the oncology and obesity-drug booms rather than algorithms.[^7]

The reason drugs are expensive is attrition, and attrition is concentrated. Of every drug program entering Phase 1, only ~13.8% ever reaches approval.[^3] The kill stage is Phase 2 — the first real test of efficacy — where the transition rate is only ~32%, versus ~64.5% for the safety-focused Phase 1.[^4] Oncology is worse still, at ~3.4% Phase-1-to-approval.[^3]

:::bars
- {label: "Phase 1 → 2 (safety)", value: 64.5%, pct: 64}
- {label: "Phase 2 → 3 (efficacy)", value: 32.4%, pct: 32}
- {label: "Phase 3 → filing", value: 60%, pct: 60}
- {label: "Phase 1 → approval (all)", value: 13.8%, pct: 14}
:::

Here is the structural trap that every AI-in-bio claim must answer. Discovery — target identification, hit-finding, lead optimization, the stages where AI demonstrably helps — is only ~32% of capitalized cost; the clinical phases are ~63%, with Phase 2/3 attrition "the most important" lever on the whole system.[^5] {accent}Compressing the cheap end does not, by itself, move the expensive end.{/} Faster, cheaper discovery raises shots-on-goal; it does not raise the probability that any given shot survives contact with human biology. That gap — between upstream speed and downstream success — is the thesis this entire report stress-tests.[^5]

## 02. Follow the money: ~$3B in, but the deals are mostly air

Capital is the clearest adoption signal, and it is genuinely large. Venture investors put roughly $3.2B into ~135 AI drug-discovery startups in a trailing-twelve-month window, with 2025 deal value rebounding to ~$3.8B.[^8] The marquee raises are real cash on real balance sheets: Xaira Therapeutics launched in 2024 with over $1B committed, the largest initial commitment in ARCH Venture Partners' history;[^12] Isomorphic Labs — the DeepMind spin-out — raised $600M in its first external round in 2025.[^11]

:::rank-list
- {label: "Xaira Therapeutics (launch, 2024)", value: "$1.0B", pct: 100, highlight: true}
- {label: "Isomorphic Labs (round, 2025)", value: "$600M", pct: 60}
- {label: "Insilico Medicine (HK IPO, 2025)", value: "$293M", pct: 29}
- {label: "Generate:Biomedicines (Series C, 2023)", value: "$273M", pct: 27}
- {label: "EvolutionaryScale (seed, 2024)", value: "$142M", pct: 14}
:::

But the headline numbers that dominate press releases — the billion-dollar pharma partnerships — are mostly contingent {accent}"biobucks"{/}, not cash. Isomorphic Labs' 2024 Eli Lilly collaboration was announced at "up to $1.7 billion"; the upfront cash was $45 million, about 2.6% of the headline.[^9] Its two 2024 deals together were framed as "nearly $3 billion" of potential value on a combined ~$82.5M of upfront cash.[^10] The cleanest natural experiment is Recursion's Roche/Genentech deal: announced in 2021 at "up to $12 billion," it had paid Recursion exactly {accent}$213 million{/} in upfront and milestone payments as of November 2025 — under 2% of the headline converted to cash in roughly four years.[^13]

:::callout(kind=warn, label="Read the upfront, not the headline")
Across every major AI-pharma partnership, disclosed upfront payments run $37.5M–$150M while announced totals run $1.2B–$12B. The realized-cash conversion rate, where it can be measured, is ~2%. Treat any "billion-dollar AI deal" as ~95–98% performance-contingent option value, not revenue.[^13][^9]
:::

The signal in the cash is therefore narrower than the signal in the announcements: a few billion dollars a year of genuine risk capital believes in AI discovery platforms, while large pharma is mostly buying cheap, milestone-gated optionality on those platforms rather than betting balance-sheet cash. That is rational behavior for a buyer who has watched the platforms struggle to convert.[^8]

## 03. The clinic: what AI-designed drugs actually exist

This is where adoption meets reality. As of mid-2026 there is {accent}no FDA-approved AI-designed drug{/} — but the clinical pipeline is no longer hypothetical. The most-cited proof point is Insilico Medicine's rentosertib (ISM001-055), a TNIK inhibitor for idiopathic pulmonary fibrosis whose target and molecule were both generative-AI-derived. In the randomized Phase 2a GENESIS-IPF trial, the 60 mg arm improved forced vital capacity by +98.4 mL versus a −20.3 mL decline on placebo over 12 weeks, published in Nature Medicine.[^14][^15]

:::timeline
- {date: "2022", headline: "First AI-designed drug killed in Phase 1", body: "Exscientia's DSP-1181 (OCD) discontinued after Phase 1 — fast discovery, ordinary clinical fate."}
- {date: "2024-12", headline: "REC-617 shows a response", body: "Recursion's AI-designed CDK7 inhibitor reports a confirmed partial response in platinum-resistant ovarian cancer (Phase 1/2)."}
- {date: "2025-06", headline: "Rentosertib Phase 2a in Nature Medicine", body: "Insilico's generative-AI IPF drug shows an FVC benefit vs placebo — the first peer-reviewed Phase 2 readout for an AI-origin molecule."}
- {date: "2025-12", headline: "Zasocitinib hits Phase 3", body: "Takeda's TYK2 inhibitor, designed with physics-based computational chemistry, meets all co-primary psoriasis endpoints; filing expected 2026."}
- {date: "2026 (expected)", headline: "Isomorphic's first trials", body: "DeepMind spin-out expects its first fully AI-designed candidates to enter the clinic by year end."}
:::

Read carefully, the pipeline carries two caveats that the press routinely drops. First, {accent}the most clinically advanced asset is the least "AI."{/} Takeda's zasocitinib reached positive Phase 3 readouts in psoriasis, but it was built with physics-based free-energy-perturbation chemistry, not generative deep learning.[^16] The genuinely generative assets — rentosertib, Iambic's HER2 inhibitor IAM1363 (Phase 1), Generate:Biomedicines' AI-designed antibody GB-0669 (Phase 1) — are all still early.[^17][^18] Second, "fastest ever discovery" claims (rentosertib's ~18-month target-to-candidate; REC-617 found in under 11 months) describe the discovery phase only and say nothing about efficacy.[^19]

The decisive number is the one a Boston Consulting Group team published in *Drug Discovery Today*: AI-discovered molecules show an ~80–90% Phase 1 success rate but revert to ~40% in Phase 2 — "comparable to historic industry averages."[^20] Phase 1 mostly tests safety and pharmacokinetics, exactly where AI-optimized drug-like properties help; Phase 2 tests whether the biology was right, where AI shows no edge yet.

:::slope(left-label="Phase 1 success", right-label="Phase 2 success", unit=%)
| Cohort | Phase 1 success | Phase 2 success |
|---|---|---|
| AI-discovered molecules | 85 | 40 |
| Historic industry baseline | 64 | 32 |
:::

The honest summary: AI has demonstrably reached the clinic and demonstrably improves the early, drug-like-property gates. Whether it improves the efficacy gate that determines attrition is, on the published evidence, still unproven — the sample is tiny (~21 AI molecules through Phase 1) and no AI-origin drug has yet read out a pivotal Phase 3 on efficacy.[^20][^13]

## 04. AlphaFold and the limits of structure

If one thing earns the word "transformation," it is AI structural biology — but the transformation is in research infrastructure, not yet in therapeutic outcomes. The AlphaFold Protein Structure Database holds over {accent}200 million{/} predicted structures, and the 2021 AlphaFold2 paper is among the most-cited papers in modern science; DeepMind reports the database has been used by over 3 million researchers in 190+ countries.[^22][^21][^23] AlphaFold3 (2024) extended prediction to protein–ligand, protein–DNA and antibody complexes with a claimed ≥50% improvement over prior methods, and the work earned the 2024 Nobel Prize in Chemistry (Baker; Hassabis and Jumper).[^24][^25]

:::stats
- {label: Predicted structures, value: 200M, unit: "+"}
- {label: Researchers reached, value: 3M, unit: "+"}
- {label: AF2 paper citations, value: "~36k"}
- {label: AF3 accuracy gain, value: 50%, note: vs prior methods (benchmark)}
:::

Reach, however, is not outcome. There is no published case of AlphaFold shortening a registrational drug program or moving a clinical endpoint. The most-cited "acceleration" anecdote — Insilico's 30-days-to-first-hit CDK20 example — is an uncontrolled hit-finding demonstration with no non-AI comparison arm.[^14] Peer-reviewed benchmarking found AlphaFold models perform {accent}worse{/} than experimental structures for docking-based virtual screening, sometimes with zero enrichment, because static predicted structures lack the ligand-induced fit, water and cofactors that binding depends on.[^27]

:::quote(attr="Derek Lowe, medicinal chemist, In the Pipeline")
It is very, very rare for knowledge of a protein's structure to be any sort of rate-limiting step in a drug discovery project.
:::

That practitioner critique — that structure is rarely the bottleneck — is the sharpest counter to structure-prediction hype, and it predates AF3, which narrowed but did not close the protein–ligand gap.[^26][^24] The defensible read: AlphaFold is a genuine, Nobel-grade scientific breakthrough and a near-universal research tool, whose therapeutic return on investment remains, as of mid-2026, anecdotal.

## 05. Designing life: generative biology and self-driving labs

One layer up from prediction is generation — designing proteins, binders, enzymes and gene editors that never existed. Here the field has crossed from "folds in a computer" to "works on a bench" for a handful of flagship cases. Baker-lab RFdiffusion raised experimental binder-design success rates by about two orders of magnitude and produced de novo antibodies whose designed loop matched cryo-EM structure to 0.8 Å.[^28] Profluent's LLM-designed gene editor {accent}OpenCRISPR-1{/} edited human cells with ~95% fewer off-target edits than SpCas9 and was independently reproduced in crops — a rare case of an AI-designed biological tool working in outside hands.[^29]

But the gap between creator-reported and independent success rates is the field's defining caveat. When Adaptyv Bio ran an open EGFR-binder competition, only 53 of 378 expressed designs actually bound the target — a {accent}14% wet-lab hit rate{/}, even as the best entry beat the approved antibody cetuximab on affinity.[^30] Baker-lab de novo serine hydrolases achieved life-like multi-step catalysis, but only ~18% of one screening round was active.[^31]

:::bars
- {label: "Peptide binders, best target (in-lab)", value: 58%, pct: 58}
- {label: "Serine hydrolase screen (in-lab)", value: 18%, pct: 18}
- {label: "EGFR competition (independent)", value: 14%, pct: 14}
:::

Self-driving labs supply the throughput to brute-force those odds. Recursion's robotic platform can run {accent}up to 2.2 million experiments per week{/}, generating ~16 million images and 135 TB of data.[^32] The honest counterweight: throughput is not validated drugs, and autonomy claims get overstated — Berkeley's celebrated A-Lab autonomous chemistry result drew a published novelty challenge from outside crystallographers. The pattern across generative biology is consistent: real bench wins exist, but typical hit rates in independent hands are low, and "designed" still routinely fails to mean "useful."[^30]

## 06. Incumbents go all-in: compute capex and enterprise LLMs

Large pharma's adoption splits into two modes with very different evidentiary weight. The hard-to-fake mode is compute capex. Eli Lilly deployed a wholly-owned NVIDIA DGX SuperPOD with {accent}1,016 Blackwell Ultra GPUs{/} — described as the largest pharma-owned AI factory;[^34] Roche/Genentech scaled its "lab in the loop" program into a hybrid AI factory exceeding 3,500 GPUs.[^33] NVIDIA opened its BioNeMo platform to 200+ pharma and techbio users and made a $50M equity investment in Recursion.[^33][^53] Lilly also launched TuneLab, a federated platform exposing models trained on over $1B of its preclinical data to smaller biotechs.[^35]

:::stats
- {label: "Lilly AI factory", value: "1,016", unit: GPUs}
- {label: "Roche/Genentech factory", value: "3,500", unit: GPUs}
- {label: "Moderna custom GPTs", value: "750", unit: "+"}
- {label: "BioNeMo platform users", value: "200", unit: "+"}
:::

The cheaper, softer mode is enterprise LLM rollout, where adoption metrics are real but vendor-reported. Moderna deployed ChatGPT Enterprise to ~3,000 employees who built {accent}750+ custom GPTs{/} across legal, research, manufacturing and commercial — with 100% legal-team adoption.[^36] Sanofi declared itself the company aiming to be "first powered by artificial intelligence at scale" and rolled out its plai decision app to tens of thousands of staff.[^37]

:::callout(kind=info, label="Where the boundary holds")
Even the most aggressive incumbent claim — Sanofi/OpenAI "AI-generated first drafts of FDA documents" — is human-in-the-loop drafting. No incumbent is putting AI-authored content in front of a regulator without human authorship and review. The GxP boundary is the line adoption has not crossed.[^37]
:::

The takeaway: the capex commitments are credible signals of conviction because they cost real money; the "all-in" rhetoric and seat-count metrics measure engagement, not validated outcomes. Both are adoption — but only one is hard evidence.[^34]

## 07. The unglamorous win: documents, safety, manufacturing

The best-evidenced, most-mature AI adoption in pharma is not in discovery at all — it is in the document-heavy back office, where language models genuinely excel and labor cost is high. A Merck and McKinsey tool cut clinical study report first-draft time from ~180 hours to ~80 hours and reduced errors by 50%, delivering a first draft in as little as five minutes.[^38] A Takeda-evaluated platform (AutoIND) cut IND nonclinical-summary first-draft time by {accent}97%{/} — from ~100 hours to under four.[^39]

:::slope(left-label="Manual hours", right-label="With gen-AI", unit=h)
| Task | Manual hours | With gen-AI |
|---|---|---|
| Clinical study report draft | 180 | 80 |
| IND nonclinical summary | 100 | 4 |
:::

But every credible figure here is a {accent}first-draft, pre-QC{/} number, and the ceiling is identical across medical writing, pharmacovigilance and manufacturing: validation, hallucination, and 21 CFR Part 11 / ALCOA++ data-integrity rules keep a human in the loop. The clearest illustration came from the regulator itself: the FDA's internal generative-AI tool Elsa was reported to fabricate nonexistent studies and citations, limiting it to administrative work.[^40]

:::quote(attr="FDA employee, on the agency's Elsa tool, to CNN")
Anything that you don't have time to double-check is unreliable. It hallucinates confidently.
:::

So the real economic effect of LLMs across the pharma value chain in 2024–2026 is cycle-time compression and headcount leverage on drafting and review — substantial, durable, and under-hyped relative to discovery — but not end-to-end automation.[^38][^40]

## 08. Diagnostics and genomics: the commercially mature edge

If discovery is where AI is loudest, diagnostics is where it is most {accent}deployed{/}. The FDA's list of AI/ML-enabled medical devices has surpassed 1,000 marketing authorizations, of which roughly 76% are radiology.[^42][^43] Landmark approvals are real: IDx-DR became the first autonomous AI diagnostic in 2018 (87% sensitivity, 90% specificity for diabetic retinopathy), and Paige Prostate was the first FDA-cleared AI in pathology in 2021.[^44][^45]

:::donut(center-label="AI devices")
- {label: Radiology, value: 76}
- {label: Cardiovascular, value: 9}
- {label: Neurology, value: 6}
- {label: Other specialties, value: 9}
:::

Yet clearance is not adoption, and adoption is not reimbursement. Only ~30% of US radiologists report using AI clinically, and a systematic review found just ~5% of cleared radiology devices underwent prospective testing.[^46][^43] The reimbursement bottleneck is severe: the entire radiology-AI field has only a handful of permanent CPT codes. Clearance volume overstates clinical rigor.[^43]

Genomics shows the same split between scale and decision-impact. DeepMind's AlphaMissense classified {accent}89% of all 71 million possible human missense variants{/}, against a prior baseline where only ~0.1% had expert classification;[^47] Arc Institute's Evo 2 is a 40-billion-parameter DNA foundation model trained on 9.3 trillion base pairs.[^48] But peer-reviewed benchmarks found single-cell foundation models like scGPT and Geneformer can be outperformed by simple linear baselines on key tasks — scale and AUROC have outrun validated decision-impact.[^49] The exception that proves adoption can be commercial is Tempus AI, whose precision-oncology data business reached ~$1.3B in FY2025 revenue (up 83%), albeit still net-loss-making.[^50]

## 09. The map: public markets, consolidation and China

The public-market verdict on pure-play AI drug discovery is brutal, and it is mostly a story of biotech beta rather than AI alpha. Recursion (RXRX) fell from ~$7.50 to ~$3.00 over two years; Schrödinger (SDGR) roughly halved; AbCellera (ABCL) round-tripped.[^66] The flagship corporate event was defensive: Recursion's all-stock acquisition of Exscientia (closed November 2024) merged two cash-burning platforms — Recursion holders ended with ~74%, Exscientia ~26% — and removed a ticker rather than creating one.[^52]

:::line-chart(title="AI-biotech equities, monthly close ($)", subtitle="Yahoo Finance, to 2026-05", y-unit=$)
x: 2024-06,2024-08,2024-10,2024-12,2025-02,2025-04,2025-06,2025-08,2025-10,2025-12,2026-02,2026-04,2026-05
RXRX: 7.5,7.28,6.32,6.76,7.51,5.59,5.06,4.7,5.52,4.09,3.67,3.46,3.01
SDGR: 19.34,21.03,17.59,19.29,22.31,25.63,20.12,19.51,21.04,17.88,12.06,11.96,13.3
ABCL: 2.96,2.56,2.73,2.93,2.59,2.61,3.43,4.18,5.55,3.42,3.61,4.15,5.2
:::

The cohort is bifurcated by business model, not by "AI." Two names have real revenue — Tempus (TEM, ~$1.3B) and Schrödinger (SDGR, ~$256M, two-thirds recurring software);[^50][^54] the platform-discovery names trade on pipeline optionality with negligible revenue. Recursion booked just ~$39M over nine months of 2025 against a ~$540M operating loss.[^13] And the macro dominates: the SPDR biotech ETF (XBI) fell ~20% and ~26% in 2021–2022, then rallied ~36% in 2025, so most AI-bio price action is sector beta, not AI-specific signal.[^55]

Geographically, the center of gravity is shifting. China runs the only peer-reviewed generative-AI Phase 2a (rentosertib) and produced 2025's largest Hong Kong biotech IPO (Insilico, ~$293M).[^58] Chinese biopharma out-licensing hit a record ~$135.7B across 157 deals in 2025, roughly 2.6x 2024 — though the vast majority is conventional fast-follower chemistry, not AI-discovered.[^56] The US response has been defensive: the BIOSECURE Act became law in December 2025, restricting Chinese "biotech companies of concern," though the final text dropped the named-company list.[^59]

:::compare
- {role: "ANNOUNCED", name: "Recursion–Roche deal", value: "$12B"}
- {role: "REALIZED", name: "Paid to date (2025)", value: "$213M"}
- {role: SUBJECT, name: "Conversion rate", value: "1.8%"}
:::

## 10. The other risk: AI-enabled biosecurity

Adoption has a dual-use shadow, and here the evidence is more reassuring than the headlines — with one real exception. The single controlled red-team study, by RAND in 2024, found {accent}no statistically significant uplift{/} from current LLMs for biological-attack planning; model outputs largely mirrored what is already on the open internet.[^60] Frontier labs have nonetheless acted precautionarily: Anthropic deployed Claude Opus 4 under heightened "ASL-3" safeguards in 2025 because it could not rule out bio-risk — an inability-to-disprove trigger, not a demonstrated-hazard one.[^62]

:::timeline
- {date: "2023-10", headline: "US EO 14110", body: "Directs a nucleic-acid synthesis screening framework as the AI-bio guardrail (later rescinded Jan 2025)."}
- {date: "2024-01", headline: "RAND: no measurable uplift", body: "Controlled study finds current LLMs do not meaningfully aid bioweapon planning."}
- {date: "2025-05", headline: "Anthropic ASL-3", body: "Claude Opus 4 deployed under heightened CBRN safeguards as a precaution."}
- {date: "2025-10", headline: "AI evades DNA screening", body: "A Microsoft-led Science study shows AI protein redesign can slip toxin variants past synthesis screeners — then patches them before disclosure."}
- {date: "2025-12", headline: "BIOSECURE Act", body: "US law restricts Chinese biotech 'companies of concern.'"}
:::

The one demonstrated, empirically-grounded vulnerability sits not in chatbots but at the design-tool / DNA-synthesis interface: a Microsoft-led team showed AI protein redesign could generate toxin variants that evaded commercial DNA-synthesis screening in ~3% of cases — then ran ~10 months of responsible disclosure and globally patched the screeners before publishing.[^61] That makes the episode as much a governance success as a risk demonstration, and it locates the real chokepoint in a fixable, verifiable place: synthesis screening, not Q&A.[^61]

## 11. What would break this thesis

The thesis of this report — adoption is broad upstream, unproven downstream — has several ways it could be wrong, and intellectual honesty requires naming them. An adversarial falsification pass against independent sources left two of the three load-bearing claims unbroken — the ~2% biobuck conversion and the AI Phase-1-vs-Phase-2 reversion — while flagging one real caveat: the $2.6B cost headline is disputed by a JAMA estimate of ~$985M median, though even that floor sustains the argument that the economics are severe.[^67][^20][^13]

The strongest bull rebuttal is that {accent}the sample is too young{/}. Only ~21 AI-origin molecules have completed Phase 1; if the high Phase 1 success rate persists and Phase 2 rates hold even at baseline, end-to-end odds roughly double — and no AI drug has yet had a fair shot at a pivotal Phase 3.[^20] A single positive AI-origin Phase 3 efficacy readout would materially weaken the "upstream only" framing.

:::callout(kind=danger, label="The historical analog")
The Human Genome Project was sold circa 2000 as a near-term cure revolution; two decades on, its measurable population-health impact was modest, because the bottleneck was never data generation — it was biology. AI accelerates the same cheap upstream step (hypotheses, molecules, structures) that genomics did; the expensive downstream step (does it work in humans) is unchanged. The timeline error could again be a decade-plus.[^65]
:::

Three more falsifiers worth watching. First, the consultancy forecasts could be right: McKinsey models $60–110B/yr of gen-AI value for pharma — but the same firms concede the benefit is "not yet realized at scale," and market-research CAGR estimates for "AI in drug discovery" disagree on the current market size by 3.7x, which is the signature of marketing, not measurement.[^64] Second, the productivity rebound that bulls cite (pharma R&D IRR rising to ~5.9% in 2024) is GLP-1-driven, not AI-driven, with cost-per-asset still climbing.[^7] Third, the clinical wreckage is real and recent: Exscientia's DSP-1181 died in Phase 1, BenevolentAI's lead drug failed Phase 2 and the company cut ~180 staff, and Recursion discontinued multiple clinical programs post-merger — AI-origin assets fail like any others once they hit efficacy.[^63][^13]

The balanced verdict for mid-2026: AI is the most broadly adopted new toolset the bio industry has seen since high-throughput screening, and its upstream wins — structure, design, imaging, variant calling, documentation — are real, measurable, and compounding. But adoption is not transformation. The number that defines the industry — the probability that a molecule entering humans becomes a medicine — has not yet moved. Until an AI-origin drug clears a pivotal efficacy trial, "AI is transforming drug development" remains a forecast, not a finding.[^20][^5]

:::references
- {id: 1, title: "Innovation in the pharmaceutical industry: New estimates of R&D costs", url: "https://doi.org/10.1016/j.jhealeco.2016.01.012", source: "DiMasi et al., J. Health Economics", date: "2016-05"}
- {id: 2, title: "Diagnosing the decline in pharmaceutical R&D efficiency (Eroom's Law)", url: "https://doi.org/10.1038/nrd3681", source: "Scannell et al., Nat. Rev. Drug Discov.", date: "2012-03"}
- {id: 3, title: "Estimation of clinical trial success rates and related parameters", url: "https://doi.org/10.1093/biostatistics/kxx069", source: "Wong, Siah, Lo, Biostatistics", date: "2019-04"}
- {id: 4, title: "Clinical development success rates for investigational drugs", url: "https://doi.org/10.1038/nbt.2786", source: "Hay et al., Nature Biotechnology", date: "2014-01"}
- {id: 5, title: "How to improve R&D productivity: the pharmaceutical industry's grand challenge", url: "https://doi.org/10.1038/nrd3078", source: "Paul et al., Nat. Rev. Drug Discov.", date: "2010-03"}
- {id: 6, title: "Research and Development in the Pharmaceutical Industry", url: "https://www.cbo.gov/publication/57025", source: "US Congressional Budget Office", date: "2021-04"}
- {id: 7, title: "Drug development cost hits $2.2B/asset in 2024; GLP-1s drive ROI", url: "https://www.fiercebiotech.com/biotech/drug-development-cost-pharma-22b-asset-2024-plus-how-glp-1s-impact-roi-deloitte", source: "FierceBiotech (Deloitte data)", date: "2025-03"}
- {id: 8, title: "Why AI drug discovery isn't the layup VCs expected", url: "https://pitchbook.com/news/articles/why-ai-drug-discovery-isnt-the-layup-vcs-expected", source: "PitchBook", date: "2025"}
- {id: 9, title: "Isomorphic Labs strategic collaboration with Lilly", url: "https://www.prnewswire.com/news-releases/isomorphic-labs-announces-strategic-multi-target-research-collaboration-with-lilly-302027392.html", source: "Isomorphic Labs / PR Newswire", date: "2024-01-07"}
- {id: 10, title: "Isomorphic Labs kicks off 2024 with two pharma collaborations", url: "https://www.isomorphiclabs.com/articles/isomorphic-labs-kicks-off-2024-with-two-pharmaceutical-collaborations", source: "Isomorphic Labs", date: "2024-01-07"}
- {id: 11, title: "Isomorphic Labs raises $600 million", url: "https://www.prnewswire.com/news-releases/isomorphic-labs-announces-600-million-funding-to-further-develop-its-next-generation-ai-drug-design-engine-and-advance-therapeutic-programs-into-the-clinic-302415534.html", source: "Isomorphic Labs / PR Newswire", date: "2025-03-31"}
- {id: 12, title: "New AI drug discovery powerhouse Xaira rises with $1B funding", url: "https://www.fiercebiotech.com/biotech/new-ai-drug-discovery-powerhouse-xaira-rises-1b-funding", source: "FierceBiotech", date: "2024-04-24"}
- {id: 13, title: "Recursion Q3 2025 results and business update", url: "https://www.globenewswire.com/news-release/2025/11/05/3181232/0/en/Recursion-Reports-Third-Quarter-2025-Financial-Results-and-Provides-Business-Update.html", source: "Recursion / GlobeNewswire", date: "2025-11-05"}
- {id: 14, title: "A generative AI-discovered TNIK inhibitor for IPF: a randomized phase 2a trial", url: "https://www.nature.com/articles/s41591-025-03743-2", source: "Nature Medicine", date: "2025-06-03"}
- {id: 15, title: "Rentosertib (ISM001-055) Phase 2a trial record", url: "https://clinicaltrials.gov/study/NCT05938920", source: "ClinicalTrials.gov", date: "2024"}
- {id: 16, title: "Takeda zasocitinib Phase 3 plaque psoriasis data", url: "https://www.takeda.com/newsroom/newsreleases/2025/takeda-zasocitinib-phase-3-plaque-psoriasis-data-once-daily-pill/", source: "Takeda", date: "2025-12-18"}
- {id: 17, title: "IAM1363 Phase 1/1b trial record", url: "https://clinicaltrials.gov/study/NCT06253871", source: "ClinicalTrials.gov / Iambic", date: "2024"}
- {id: 18, title: "First-in-human results for AI-designed antibody GB-0669", url: "https://generatebiomedicines.com/media-center/first-in-human-results-for-gb-0669-durable-neutralization-from-an-ai-designed-antibody", source: "Generate:Biomedicines", date: "2025-10-09"}
- {id: 19, title: "Recursion interim Phase 1 data for REC-617 (CDK7)", url: "https://www.globenewswire.com/news-release/2024/12/09/2994128/0/en/Recursion-Reports-Interim-Phase-1-Clinical-Data-for-REC-617-Monotherapy-a-Potential-Best-in-Class-CDK7-Inhibitor-With-Encouraging-Patient-Response-and-Favorable-Tolerability.html", source: "Recursion / GlobeNewswire", date: "2024-12-09"}
- {id: 20, title: "How successful are AI-discovered drugs in clinical trials?", url: "https://doi.org/10.1016/j.drudis.2024.104009", source: "Jayatunga et al. (BCG), Drug Discovery Today", date: "2024-06"}
- {id: 21, title: "Highly accurate protein structure prediction with AlphaFold", url: "https://www.nature.com/articles/s41586-021-03819-2", source: "Jumper et al., Nature", date: "2021-07"}
- {id: 22, title: "AlphaFold Protein Structure Database", url: "https://alphafold.ebi.ac.uk/", source: "EMBL-EBI / Google DeepMind", date: "2025"}
- {id: 23, title: "AlphaFold: five years of impact", url: "https://deepmind.google/blog/alphafold-five-years-of-impact/", source: "Google DeepMind", date: "2026"}
- {id: 24, title: "Accurate structure prediction of biomolecular interactions with AlphaFold3", url: "https://www.nature.com/articles/s41586-024-07487-w", source: "Abramson et al., Nature", date: "2024-05-08"}
- {id: 25, title: "The Nobel Prize in Chemistry 2024", url: "https://www.nobelprize.org/prizes/chemistry/2024/summary/", source: "NobelPrize.org", date: "2024-10-09"}
- {id: 26, title: "Why AlphaFold won't revolutionise drug discovery", url: "https://www.chemistryworld.com/opinion/why-alphafold-wont-revolutionise-drug-discovery/4016051.article", source: "Derek Lowe, Chemistry World", date: "2022-08"}
- {id: 27, title: "How good are AlphaFold models for docking-based virtual screening?", url: "https://www.cell.com/iscience/fulltext/S2589-0042(22)02193-9", source: "Scardino et al., iScience", date: "2023-01"}
- {id: 28, title: "De novo design of protein structure and function with RFdiffusion", url: "https://www.nature.com/articles/s41586-023-06415-8", source: "Watson et al. (Baker lab), Nature", date: "2023-07"}
- {id: 29, title: "OpenCRISPR-1: generative AI-designed gene editor (Nature publication)", url: "https://www.businesswire.com/news/home/20250730820469/en/Profluent-Announces-Publication-of-Generative-AI-Research-in-Nature-with-New-Results-for-OpenCRISPR-1", source: "Profluent / BusinessWire", date: "2025-07-30"}
- {id: 30, title: "Protein design competition results (EGFR binders)", url: "https://adaptyvbio.substack.com/p/protein-design-competition-results", source: "Adaptyv Bio", date: "2024-12"}
- {id: 31, title: "AI-designed enzymes with complex active sites (serine hydrolases)", url: "https://www.bakerlab.org/2025/02/13/ai-enzymes-with-complex-active-sites/", source: "Baker Lab / Science", date: "2025-02-13"}
- {id: 32, title: "Recursion Q4 2024 update: experimental throughput", url: "https://ir.recursion.com/news-releases/news-release-details/recursion-provides-business-updates-and-reports-fourth-quarter-2", source: "Recursion", date: "2025-02-28"}
- {id: 33, title: "NVIDIA opens BioNeMo to scale digital biology", url: "https://investor.nvidia.com/news/press-release-details/2024/NVIDIA-Opens-BioNeMo-to-Scale-Digital-Biology-for-Global-Biopharma-and-Scientific-Industry/default.aspx", source: "NVIDIA", date: "2024-11-18"}
- {id: 34, title: "Lilly builds largest pharma-owned AI factory on NVIDIA Blackwell", url: "https://blogs.nvidia.com/blog/lilly-ai-factory-nvidia-blackwell-dgx-superpod/", source: "NVIDIA", date: "2025-10-28"}
- {id: 35, title: "Lilly launches TuneLab platform for biotechs", url: "https://investor.lilly.com/news-releases/news-release-details/lilly-launches-tunelab-platform-give-biotechnology-companies", source: "Eli Lilly", date: "2025-09-09"}
- {id: 36, title: "Moderna and OpenAI: scaling ChatGPT Enterprise", url: "https://openai.com/index/moderna/", source: "OpenAI / Moderna", date: "2024-04-30"}
- {id: 37, title: "Sanofi: becoming the first pharma powered by AI at scale", url: "https://www.sanofi.com/en/media-room/press-releases/2023/2023-06-13-12-00-00-2687072", source: "Sanofi", date: "2023-06-13"}
- {id: 38, title: "Merck expands internal generative-AI solutions (CSR drafting)", url: "https://www.merck.com/news/merck-expands-innovative-internal-generative-ai-solutions-helping-to-deliver-medicines-to-patients-faster/", source: "Merck", date: "2025-06-25"}
- {id: 39, title: "AutoIND: LLM platform for IND nonclinical summaries", url: "https://arxiv.org/abs/2509.09738", source: "Weave / Takeda, arXiv", date: "2025-09-10"}
- {id: 40, title: "FDA's AI tool Elsa hallucinates studies, staff say", url: "https://www.cnn.com/2025/07/23/politics/fda-ai-elsa-drug-regulation-makary", source: "CNN", date: "2025-07-23"}
- {id: 41, title: "FDA proposes framework for AI credibility in drug submissions", url: "https://www.fda.gov/news-events/press-announcements/fda-proposes-framework-advance-credibility-ai-models-used-drug-and-biological-product-submissions", source: "US FDA", date: "2025-01-06"}
- {id: 42, title: "Artificial Intelligence-Enabled Medical Devices list", url: "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices", source: "US FDA", date: "2025-12"}
- {id: 43, title: "FDA approval of AI/ML devices in radiology: a systematic review", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC12595527/", source: "PMC (peer-reviewed)", date: "2025"}
- {id: 44, title: "Pivotal trial behind the first autonomous AI diagnostic (IDx-DR)", url: "https://www.digitaldiagnostics.com/pivotal-trial-results-behind-the-fdas-first-ever-clearance-of-an-autonomous-ai-diagnostic-system-published-in-nature-digital-medicine/", source: "Digital Diagnostics / Nature Digital Medicine", date: "2018-08"}
- {id: 45, title: "FDA De Novo decision DEN200080 (Paige Prostate)", url: "https://www.accessdata.fda.gov/cdrh_docs/pdf20/DEN200080.pdf", source: "US FDA", date: "2021-09-21"}
- {id: 46, title: "ACR Data Science Institute AI survey (radiologist adoption)", url: "https://www.jacr.org/article/S1546-1440(21)00293-3/pdf", source: "JACR", date: "2021-04"}
- {id: 47, title: "AlphaMissense: a catalogue of genetic mutations", url: "https://deepmind.google/discover/blog/a-catalogue-of-genetic-mutations-to-help-pinpoint-the-cause-of-diseases/", source: "Google DeepMind / Science", date: "2023-09-19"}
- {id: 48, title: "Evo 2: genome foundation model (40B params, 9.3T bp)", url: "https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1", source: "Arc Institute / NVIDIA, bioRxiv", date: "2025-02-19"}
- {id: 49, title: "Assessing the limits of single-cell foundation models", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC12007350/", source: "Genome Biology", date: "2025-04"}
- {id: 50, title: "Tempus AI FY2025 financial results", url: "https://www.sec.gov/Archives/edgar/data/1717115/000119312526066931/tem-ex99_1.htm", source: "SEC EDGAR (8-K)", date: "2026-02-24"}
- {id: 51, title: "Tempus AI IPO final prospectus (424B4)", url: "https://www.sec.gov/Archives/edgar/data/1717115/000119312524161989/d221145d424b4.htm", source: "SEC EDGAR", date: "2024-06-17"}
- {id: 52, title: "Recursion to acquire Exscientia (merger announcement)", url: "https://www.sec.gov/Archives/edgar/data/1601830/000119312524196505/d856792dex991.htm", source: "SEC EDGAR (8-K)", date: "2024-08-08"}
- {id: 53, title: "NVIDIA $50M PIPE investment in Recursion", url: "https://www.sec.gov/Archives/edgar/data/0001601830/000160183023000050/ex991-rxrxxnvidiapr.htm", source: "SEC EDGAR (8-K)", date: "2023-07-12"}
- {id: 54, title: "Schrödinger FY2025 financial results", url: "https://www.sec.gov/Archives/edgar/data/1490978/000149097826000009/sdgr-20251231xexx991.htm", source: "SEC EDGAR (8-K)", date: "2026-02-25"}
- {id: 55, title: "SPDR S&P Biotech ETF (XBI) performance", url: "https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-biotech-etf-xbi", source: "State Street Global Advisors", date: "2026-04"}
- {id: 56, title: "Chinese drug makers strike record $135.7B out-licensing deals in 2025", url: "https://www.scmp.com/business/china-business/article/3339011/chinese-drug-makers-strike-record-us136-billion-out-licensing-deals-2025", source: "South China Morning Post", date: "2025-12"}
- {id: 57, title: "Eli Lilly, XtalPi ink $250M AI drug discovery deal", url: "https://www.fiercebiotech.com/medtech/eli-lilly-xtalpi-ink-250m-deal-ai-powered-drug-discovery", source: "FierceBiotech", date: "2023-05-09"}
- {id: 58, title: "Insilico Medicine lists on Hong Kong Stock Exchange", url: "https://www.prnewswire.com/news-releases/insilico-medicine-lists-on-hong-kong-stock-exchange-showing-ai-drug-discovery-momentum-with-2025s-largest-hong-kong-biotech-ipo-302650606.html", source: "Insilico Medicine / PR Newswire", date: "2025-12-30"}
- {id: 59, title: "Congress passes the BIOSECURE Act", url: "https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2025/december/congress-passes-biosecure-act-here-s-what-you-need-to-know/", source: "Foley Hoag", date: "2025-12-17"}
- {id: 60, title: "RAND: current LLMs do not increase bioweapon attack-planning risk", url: "https://www.rand.org/news/press/2024/01/25.html", source: "RAND Corporation", date: "2024-01-25"}
- {id: 61, title: "When AI meets biology: promise, risk and responsibility (DNA screening)", url: "https://www.microsoft.com/en-us/research/blog/when-ai-meets-biology-promise-risk-and-responsibility/", source: "Microsoft Research / Science", date: "2025-10-02"}
- {id: 62, title: "Activating ASL-3 protections for Claude Opus 4", url: "https://www.anthropic.com/news/activating-asl3-protections", source: "Anthropic", date: "2025-05-22"}
- {id: 63, title: "BenevolentAI cuts up to 180 staff after mid-phase flop", url: "https://www.fiercebiotech.com/biotech/benevolentai-makes-deep-cuts-after-midphase-flop-laying-180-and-shrinking-lab-footprint", source: "FierceBiotech", date: "2023-05"}
- {id: 64, title: "Generative AI in pharma: moving from hype to reality", url: "https://www.mckinsey.com/industries/life-sciences/our-insights/generative-ai-in-the-pharmaceutical-industry-moving-from-hype-to-reality", source: "McKinsey & Company", date: "2024-01"}
- {id: 65, title: "Why sequencing the human genome failed to produce big breakthroughs", url: "https://theconversation.com/why-sequencing-the-human-genome-failed-to-produce-big-breakthroughs-in-disease-130568", source: "The Conversation", date: "2020"}
- {id: 66, title: "AI-biotech equity price series (RXRX, SDGR, ABCL)", url: "https://finance.yahoo.com/", source: "Yahoo Finance", date: "2026-05"}
- {id: 67, title: "Estimated R&D investment needed to bring a new medicine to market", url: "https://pubmed.ncbi.nlm.nih.gov/32125404/", source: "Wouters, McKee, Luyten, JAMA", date: "2020-03"}
:::
