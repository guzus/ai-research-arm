---
eyebrow: RESEARCH · PROTEIN DESIGN
title: "The 26.8% binder hit rate: what Claude actually designed, and why the RFdiffusion 19% baseline settles less than it seems"
deck: "Anthropic's autonomous protein-design campaign cleared 14 of 15 targets at a 26.8% hit rate. That headline is real and independently validated. But it is not a single-model win over RFdiffusion — it is an orchestration result, and the '19% baseline' conflates two different questions."
lede: |
  On August 18, 2026 Anthropic reported that Claude (Mythos Preview and Opus 4.8) autonomously designed protein binders against 16 targets in 24–48 hour sessions, and that two independent contract labs confirmed binders for 14 of the 15 targets with interpretable data — 354 of 1,320 designs, a 26.8% hit rate [^1][^2]. The comparison often attached to it — "better than RFdiffusion's ~19%" — comes from the original RFdiffusion paper [^3]. The number is real. The comparison, treated as a settlement, is not. This article separates the agent's design (what Claude orchestrated) from any single generator's (what RFdiffusion produced), and argues that the 19% baseline both understates and overstates what the result means.
---

## 01. What the 26.8% actually is

The figure is not one model's design success. It is the outcome of an *agentic orchestration layer*: Claude spontaneously assembled pipelines out of open-source structure-generation methods — PXDesign, RFdiffusion3, Genie 3, FreeBindCraft, BindCraft, BoltzGen, RFdiffusion, Proteina-Complexa, FoldCraft and BoltzDesign1 — together with sequence-design and co-folding predictors, chose epitopes, ran in-silico optimization rounds, and returned 30 ranked designs per target [^2][^4]. Adaptyv Bio and Twist Bioscience then synthesized and measured every design exactly as delivered, blind to model and rank [^2][^5].

Under the report's "integrated call" — which reconciles both CROs and, notably, adds 19 binders Adaptyv Bio had not classified as such — 354 of 1,320 designs bound, for 26.8% [^1][^2]. Counting Adaptyv Bio's own classification alone yields roughly 336 of 1,296 [^2]. The overall number is an average over targets that range from 0% (maltose-binding protein, 0 of 90) to 80% (TREM2, 72 of 90) [^2]. A single claim of "26.8%" therefore hides the widest possible dispersion: the pooled hit rate is the least informative number in the paper.

:::stats
- {label: Designs bound, value: 354, note: "of 1,320 tested"}
- {label: Targets with binders, value: "14 / 15", note: "MBP = the one failure"}
- {label: Mythos PT hit rate, value: 35.1%, note: "single-target mode"}
- {label: Top-ranked hit rate, value: 49%, note: "of 41 rankings"}
:::

The report itself flags the same caution: "we have described campaigns rather than models." Each combination of model, format and target ran exactly once, so model, format and run-to-run variation are all confounded [^2]. The single-target format gave each target 2.8× the per-target compute budget of the multi-target format, so the observed 35.1% versus 26.7% improvement across modes "cannot separate the effect of focus from that of budget" [^2].

Per-model multi-target figures, always cited next to the headline, split the difference: Mythos Preview hit 26.7% (104 of 390) and Opus 4.8 hit 22.6% (88 of 390) when designing against 13 targets simultaneously in one 48-hour session [^2][^5]. The "26.8%" headline and the 26.7% model figure are two different aggregations over the same data — a distinction the coverage frequently blurs.

:::compare
- {role: LOWEST,  name: MBP target, value: "0%"}
- {role: HIGHEST, name: TREM2,     value: "80%"}
- {role: SUBJECT, name: "Claude (pooled)", value: "26.8%"}
:::

:::bar-chart(title="Hit rate by campaign / model", orientation=horizontal, value-unit=%, value-suffix="%")
categories: Opus 4.8 (multi), Mythos (multi), Mythos (single-target), Pooled (all)
Hit rate: 22.6, 26.7, 35.1, 26.8
:::

:::kv
- {term: Designs tested, def: "1,320"}
- {term: Binders (integrated call), def: "354"}
- {term: Adaptyv-only binder count, def: "~336 of 1,296"}
- {term: Targets with a binder, def: "14 of 15"}
:::

## 02. What Claude "designed," precisely

Claude designed nothing from a blank sheet. It selected, filtered, optimized and ranked candidates produced by existing specialist models — and the report is explicit that hit rates tabulated per generator are "descriptive and not a controlled comparison of the methods" [^2]. A released per-design provenance table records which tools produced which design: PXDesign 358, RFdiffusion3 267, Genie 3 185, FreeBindCraft 135, a PyRosetta-free BindCraft build, BoltzGen 134, RFdiffusion 118, Proteina-Complexa 100, FoldCraft 14, BoltzDesign1 2, Protein Hunter 2 [^2]. RFdiffusion was itself one of those generators, contributing 118 base plus 267 RFdiffusion3 designs out of a 1,315-design pool [^2]. Every listed generator with at least 100 ordered designs produced binders at per-method rates between 22% and 43%, spanning nanomolar to micromolar affinities [^2].

So the correct decomposition is: an agent (Claude) operating an ensemble (many generators, most newer than 2023 RFdiffusion) that was screened and ranked by a strong co-folding filter. A fair number for "Claude's design" is therefore better read as the *coverage* — 14 of 15 targets, including TNFα where multiple published efforts reported no de novo binders [^2][^6] — and the *calibrated ranking*: the single top-ranked design per target and campaign bound 49% of the time, over all 30 designs 28% [^2]. The rank ordering was strongly correlated with the co-folding score (median Spearman ρ = 0.86 within a target) [^2].

Anchoring that ranking was a deliberately chosen filter. Anthropic benchmarked an ensembled ESMFold2 + Protenix v2 filter on the Overath et al. dataset (3,532 designs, 13 targets, 391 binders) and found it reached macro-AP 0.62, above the strongest previously reported predictor (AlphaFold3 at 0.55), tightening to 0.66 as a z-score ensemble [^2][^8]. Claude's ranking followed that score closely — which is to say much of the "design intelligence" sits in the filtering step, not in generative novelty [^2].

## 03. Where the "19% baseline" comes from

The ~19% figure is not Anthropic's baseline; it comes from the RFdiffusion paper itself. Watson et al. (Nature 2023) reported: "The overall experimental success rate, defined as binding at or above 50% of the maximal response for the positive control, was 19%" — across five targets (influenza haemagglutinin, IL-7Rα, insulin receptor, PD-L1, TrkA), testing fewer than 100 designs per target, with binders found for all five [^3]. The significance of that number was contextual: RFdiffusion was roughly two orders of magnitude above prior Rosetta-based design, whose estimated per-target success rates were 0% (HA), 2.2%, 5.5%, 3.7% and 1.5% [^3].

Notably, Anthropic's own blog post does **not** cite 19% as its reference point. It compares Claude against the "10 to 15% ... typical in protein design campaigns today" (derived from ProteinBase) and against Adaptyv's open competitions, where it would have won five of six and beat the field's hit rates and affinities [^1][^5]. The technical report likewise benchmarked only against Adaptyv competitions and its own integrated hit rates — it never runs an RFdiffusion-only control [^2]. The 19%/26.8% pairing is made by outside commentary, not by the authors. Independent Adaptyv re-validation of RFdiffusion exists as a public collection, but that is not what Claude's 26.8% is being measured against [^10].

## 04. Why the comparison does not "settle" it

Three structural reasons make the RFdiffusion-versus-Claude framing misleading as a settlement.

First, it is not apples-to-apples on design budgets. RFdiffusion-2023 was a single generator; Claude's campaigns drew on methods released up to a year later — BindCraft, RFdiffusion3, Genie 3, BoltzGen and Proteina-Complexa [^11][^12][^13] — plus tens of thousands of H100-hours per campaign (up to 12,500 per multi-target run; up to $50,000 in cloud GPU) [^2]. Trading a 26.8% ensemble against a 19% single-2023-model number credits the agent with tool-advances it merely picked up.

Second, the assays are not comparable. RFdiffusion's 19% used a single-point 10 μM BLI screen and a "≥50% of positive control" threshold [^3]. Anthropic's 26.8% used two CROs (SPR single-cycle at Adaptyv; SPR Fc-array at Twist), a multi-criterion integrated call, and a binder definition that expanded the count above Adaptyv's own tally [^2][^5]. Denominator and threshold differences of this kind can move hit rates several points without any real change in design quality.

Third, one number hides extreme per-target and per-campaign variance, so the headline is not stable. IL-7Rα and PD-L1 produce many binders (49/90 and up to 14/90); MBP produced 0/90, BBF-14 3/90 and 15-PGDH 1/30 [^2]. A single averaged "26.8%" would move by several points if any one hard target were included or excluded. The claim is a summary statistic masquerading as a controlled result.

## 05. The strongest evidence is where it cannot be gamed

The most defensible parts of the result are the targets and measures least vulnerable to training-data leakage. On 15-PGDH and latent GDF-8 — two novel targets with no pre-recorded successes Anthropic could source from training or search — Claude's hit rates were low in absolute terms (1/30 on 15-PGDH, 14/60 on latent GDF-8) but still beat the field: the Berlin Bio × Adaptyv 15-PGDH competition produced 1 binder from 106 entries, and the EPFL GDF-8 challenge 6 of 100, so Claude's single 15-PGDH binder equals the best the crowd managed [^2][^14][^15]. On RBX1, 28 of 90 Claude designs bound against 9 of 245 in the open competition, with the tightest reaching 3.9 nM versus the competition winner's 45 nM re-measured on the same plate [^2][^16].

The cross-reactivity data are another under-reported strength: 154 of 179 binders with an evaluable cynomolgus titration bound the cynomolgus ortholog, and 130 of 233 bound the mouse ortholog, on eight targets [^2]. TNFα is the standout — 12 of 150 designs bound (8%), all from Opus 4.8, on a target where AlphaProteo and other teams reported none [^2][^6]. The report candidly notes it cannot attribute the TNFα success to the model rather than the campaign variation, because each combination ran once [^2].

:::callout(kind=info, label=Methodology)
Binding is not structure or function. Every design's pose was predicted, not solved; affinities on the five oligomeric targets (TNFα, VEGF-A, Nipah G, latent GDF-8, 15-PGDH) are apparent values affected by avidity; and the "binder" label is a concentration-dependent signal at one or both CROs, not proof of therapeutic behavior [^2].
:::

## 06. What the result fairly establishes

On the two questions the headline actually raises, the evidence separates cleanly.

*Can an agent match or exceed specialist-generator hit rates autonomously?* On this evidence, yes. The result is strongest where it is hardest to game (novel targets 15-PGDH and latent GDF-8) and where a direct same-lab comparison exists (RBX1, TREM2, Nipah, EGFR) [^2][^5][^17][^18]. Against the 2023-era RFdiffusion number, Claude's 26.8% is higher by about a third in absolute terms, but that gap is not a controlled comparison.

*Does the 26.8% versus 19% gap prove Claude "beat" RFdiffusion?* It settles nothing of the kind, and the authors do not claim it does. They explicitly disclaim that "Claude's designs are better than an expert would obtain with the same tools and budget" [^2]. The honest conclusion is that an LLM agent can now carry a whole binder-design campaign — target research, epitope selection, tool orchestration, filtering, ranking — with binders concentrated at the top of its ranking, and release an open, reproducible protocol and benchmark [^2][^4].

:::position(confidence=medium, horizon="2027-Q4")
stance: The durable finding is autonomy and coverage, not a marginal hit-rate edge over RFdiffusion. The 26.8% should be read as an orchestration-plus-filtering result over an ensemble of open models, so later claims should compare agent pipelines against the individual generators they assemble before crediting the agent itself.
consensus: The field is treating 26.8% as direct evidence that Claude is a better de novo binder designer than RFdiffusion's 19%.
resolves: An independent run of the released protocol that holds the underlying generator fixed (RFdiffusion3 only) and varies only the agent would isolate the agent's marginal contribution; structure, function and matched-control experiments would test whether the hit-rate edge survives.
:::

## 07. Why it matters for the field

The significance is a shift in *who* does the design, not a step-change in *how well* any one generative model performs. Protein design hit rates have been climbing for three years for everyone — RFdiffusion raised success ~100× over Rosetta in 2023 [^3][^20], Adaptyv's competitions now routinely reach double-digit hit rates [^5][^7], and the Overath et al. meta-analysis (3,766 characterized binders across 15 targets) shows the scoring heuristics matter as much as the generator [^8]. The intervening deep-learning filtering literature — Bennett et al.'s improvement of de novo binder design with confidence filtering — is precisely the layer Anthropic's co-folding screen formalizes [^19]. What Anthropic adds is the agentic layer that prices out the "labour of orchestration" — the field's real bottleneck — and does so with a frozen 16,000-word prompt, open tools, and both CROs' data released under CC BY 4.0 [^1][^2].

That makes the headline useful, but only if read correctly. Autonomy and coverage (14/15 targets, including a hard one) are the defensible, durable claims. "Beats RFdiffusion's 19%" is a rhetorical shortcut that conflates an agent with a generator, compares unlike assays, and hides the variance that will embarrass the statistic in the next campaign. The twin release — a reproducible prompt and an open benchmark dataset — is worth more to the field than the percentage itself [^2][^4][^9].

:::references
- {id: 1, title: "How Claude is accelerating protein design and analytical chemistry", url: "https://www.anthropic.com/research/Claude-accelerates-protein-design", source: "Anthropic Research", date: "2026-08-18"}
- {id: 2, title: "Autonomous de novo protein binder design with Claude (technical report)", url: "https://www-cdn.anthropic.com/30bf50e22a01388bb29bf077ee3f244531594b7a.pdf", source: "Anthropic", date: "2026-08-18"}
- {id: 3, title: "De novo design of protein structure and function with RFdiffusion", url: "https://www.nature.com/articles/s41586-023-06415-8", source: "Nature 620, 1089–1100", date: "2023-07-11"}
- {id: 4, title: "Claude protein binder design — prompts and data (HuggingFace)", url: "https://huggingface.co/datasets/Anthropic/claude-protein-binder-design", source: "HuggingFace", date: "2026-08-18"}
- {id: 5, title: "Case study: Benchmarking Claude's protein designs in the wet lab", url: "https://www.adaptyvbio.com/blog/anthropic-1", source: "Adaptyv Bio", date: "2026-08-19"}
- {id: 6, title: "De novo design of high-affinity protein binders with AlphaProteo", url: "https://arxiv.org/abs/2409.08022", source: "arXiv (Zambaldi et al., 2024)"}
- {id: 7, title: "Adaptyv Protein Design Competitions", url: "https://proteinbase.com/competitions", source: "ProteinBase"}
- {id: 8, title: "Predicting experimental success in de novo binder design: a meta-analysis of 3,766 experimentally characterised binders", url: "https://www.biorxiv.org/content/10.1101/2025.08.14.670059v2", source: "bioRxiv (Overath et al.)", date: "2025-09-17"}
- {id: 9, title: "BenchBB and Adaptyv benchmarks", url: "https://www.adaptyvbio.com/blog/benchbb", source: "Adaptyv Bio"}
- {id: 10, title: "RFdiffusion re-validation collection", url: "https://proteinbase.com/collections/rfdiffusion-re-validation", source: "ProteinBase"}
- {id: 11, title: "One-shot design of functional protein binders with BindCraft", url: "https://www.nature.com/articles/s41586-025-00011-8", source: "Nature (Pacesa et al.)"}
- {id: 12, title: "De novo design of all-atom biomolecular interactions with RFdiffusion3", url: "https://doi.org/10.1101/2025.09.18.676967", source: "bioRxiv (Butcher et al.)"}
- {id: 13, title: "BoltzGen: Toward universal binder design", url: "https://doi.org/10.1101/2025.11.20.689494", source: "bioRxiv (Stark et al.)"}
- {id: 14, title: "Berlin Bio × Adaptyv 15-PGDH binder design competition", url: "https://proteinbase.com/collections/berlin-bio-x-adaptyv-15-pgdh-binder-design-competition", source: "ProteinBase"}
- {id: 15, title: "EPFL × Adaptyv GDF-8 (myostatin) challenge results", url: "https://proteinbase.com/collections/gdf-8-challenge-results", source: "ProteinBase"}
- {id: 16, title: "GEM × Adaptyv RBX1 binder design competition, results", url: "https://proteinbase.com/collections/gem-x-adaptyv-rbx1-binder-design-competition-results", source: "ProteinBase"}
- {id: 17, title: "Adaptyv TREM2 hackathon: AI agents vs humans", url: "https://www.adaptyvbio.com/blog/agents-vs-humans", source: "Adaptyv Bio", date: "2026"}
- {id: 18, title: "Nipah binder competition results", url: "https://proteinbase.com/collections/nipah-binder-competition-results", source: "ProteinBase"}
- {id: 19, title: "Improving de novo protein binder design with deep learning", url: "https://www.nature.com/articles/s41467-023-38328-5", source: "Nature Communications 14, 2625 (Bennett et al.)"}
- {id: 20, title: "Design of protein-binding proteins from the target structure alone", url: "https://www.nature.com/articles/s41586-022-04628-x", source: "Nature (Cao et al.)"}
:::
