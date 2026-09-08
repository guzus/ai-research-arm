---
eyebrow: REPORT · GENOMICS
domain: biotech
title: "AlphaGenome Atlas scored 9 billion variants. It was trained on how rare they are."
deck: What DeepMind's 1-petabyte variant map settles, what its benchmark table actually shows, and the axes on which the AVI score has not yet been tested.
lede: |
  On 8 September 2026 Google DeepMind published a precomputed molecular
  prediction for every one of the roughly 9 billion single-nucleotide
  substitutions possible in the human reference genome, plus a single ranked
  impact score — AVI — layered on top. The scale is real and the engineering
  is not in dispute. What is worth arguing about is narrower and more
  consequential: the supervision signal underneath that score is population
  rarity rather than curated pathogenicity, its genome-wide comparator set
  contains two models, and the regime where a clinical variant score actually
  operates — one patient, one locus — is the regime this model class has been
  measured in and found weakest. None of that makes the Atlas a bad resource.
  It makes the number on top of it a prioritiser, not a verdict.
stats:
  - {label: SNVs scored, value: "~9B", note: "Arithmetic ceiling, not a discovery"}
  - {label: Ever observed in a human, value: "786.5M", note: "gnomAD v4"}
  - {label: Genome-wide baselines, value: "2", note: "CADD v1.7 and GPN-Star"}
  - {label: Calibrated AVI thresholds, value: "0", note: "None computed to date"}
---

:::kv
- {term: "Does it settle the scale problem?", def: "Yes. Roughly 27,000 predictions per variant, free to look up, removes a real compute barrier [^1][^5]."}
- {term: "Is \"9 billion\" new?", def: "No. CADD has precomputed every possible human SNV since 2014. The depth per variant is what is new [^11]."}
- {term: "What is AVI trained on?", def: "A gnomAD v4.1 filtering-allele-frequency proxy at 0.1% — rarity, not clinical pathogenicity [^2]."}
- {term: "Is it best-in-class?", def: "Against CADD v1.7 and GPN-Star, largely yes. Against splicing specialists it ties, and it loses two strata outright [^2]."}
- {term: "Can it be used clinically?", def: "No. DeepMind says so, and no AVI threshold has been calibrated to any ACMG/AMP evidence strength [^1][^14]."}
- {term: "Where is it least validated?", def: "Cross-individual prediction, distal enhancers, non-European ancestry, and against orthogonal experimental ground truth [^18][^20][^45][^59]."}
:::

## 01. What actually shipped — and what "9 billion" is a count of

The headline number is a property of the reference genome rather than a
property of the model: 9 billion is simply every position in the ~3.1-gigabase
reference times the three alternative bases, so the count was fixed before a
single prediction was run.[^1] What is actually new is the *depth* attached to
each of those positions — and the terms under which you may use it.

:::stats
- {label: SNVs scored, value: "~9B", note: "Reference positions × 3 alternate bases"}
- {label: Dataset size, value: "1 PB", note: "More than 30× the AlphaFold Database"}
- {label: Predictions per variant, value: "~27,000", note: "Experiment-specific scalars, on average"}
- {label: Indels scored, value: ">100M", note: "Observed only — gnomAD, UK Biobank, All of Us"}
:::

DeepMind released the Atlas on 2026-09-08 through a free website portal, the
AlphaGenome API, and a skill in Google Antigravity, describing it as
"available for academic research through an intuitive and free-to-use website
portal" and offered "for non-commercial use through our website" now "as well
as for commercial use on Google Cloud soon."[^1] The artefact itself is "a
massive 1-petabyte dataset, more than 30 times larger than the AlphaFold
Database."[^1] The petabyte is not the variant count doing the work; it is the
roughly 27,000 experiment-specific scalar predictions carried per variant on
average, spanning hundreds of human and mouse cell types and tissues.[^2] That
per-variant depth, not the row count, is the release's substantive novelty.

The indel side makes the distinction explicit. Over 100 million insertions and
deletions were scored, but only ones observed in gnomAD, UK Biobank and All of
Us — an enumeration of what has been seen, not a saturating sweep of what is
possible.[^2] The SNV table is saturating precisely because saturation is cheap
there; indel space is not enumerable at all.

:::compare
- {role: POSSIBLE, name: "SNVs in GRCh38", value: "9.0B"}
- {role: OBSERVED, name: "gnomAD v4 SNVs", value: "786.5M"}
- {role: SUBJECT, name: "Share ever seen in a human", value: "~8.7%"}
:::

gnomAD v4 contains 786,500,648 SNVs passing QC — alongside 122,583,462 indels —
from 807,162 individuals, 730,947 exomes and 76,215 genomes, on GRCh38.[^10]
The ~8.7% figure in the third card is our own division of that count by the
~9 billion possible substitutions; neither DeepMind nor gnomAD states it. The
point it makes is structural: roughly nine in ten Atlas rows describe a
substitution that has never been observed in a sequenced human, so for most of
the table there is no allele-frequency anchor and no carrier to phenotype.

A second, smaller discrepancy is worth flagging because it recurs when blog
prose and technical papers are read as one source. The blog says the Atlas
includes "over 2,500 recurrent DNA sequences — the 'words' of the genome — and
their locations"; the technical paper gives the figure as 2,601 motifs.[^1][^2]
Not a contradiction, but a reminder of which document is load-bearing.

The genuinely new constraint is the licence, and it is easiest to see against
the field's existing precomputed resources.

| Resource | What is free | Licence / terms | Commercial use |
|---|---|---|---|
| AlphaFold DB | The predicted-structure database [^42] | CC-BY-4.0 [^42] | Yes — academic and commercial [^42] |
| CADD | All possible human SNVs, GRCh38, since 2014; 81 GB, 625 GB with annotations [^11] | Free for non-commercial applications only [^11] | Requires a University of Washington licence [^11] |
| Evo 2 | 40B-parameter genomic model weights on Hugging Face [^43] | apache-2.0 [^43] | Yes [^43] |
| *AlphaGenome Atlas | Website portal and API, non-commercial [^1] | API "provided for non-commercial use only"; outputs "should not be used for the training of other machine learning models" [^9] | "on Google Cloud soon" [^1] |

CADD establishes that a precomputed, saturating, non-commercially-licensed SNV
table is a twelve-year-old genre, not a 2026 invention.[^11] AlphaGenome splits
the grant more finely than CADD does: the AVI static score table is distributed
as a tabix-indexed, bgzip-compressed TSV from a DeepMind downloads page, and
the Ensembl VEP plugin states "AVI scores were developed by Google DeepMind and
are available for commercial and non-commercial use" — while the feature
attributions behind the score "can be accessed via Google DeepMind's AlphaGenome
Atlas, which is available for non-commercial use."[^7] The number is portable;
the reasoning behind the number is not. Pushmeet Kohli indicated that
DeepMind's sister drug-discovery company Isomorphic Labs would get Atlas access
but "would also require a commercial license for access," without laying out
commercial terms.[^3]

The strongest case against reading this as repackaged arithmetic is that
precomputation is itself the product. Jonathan Sebat, a psychiatric geneticist
at UC San Diego, put it directly: "Our own workflows in the lab can be
streamlined quite a bit because we don't actually have to compute anything," and
"We literally can just look up everything."[^5] That is a real service, priced in
compute nobody else has to spend — Carl de Boer calls AlphaGenome the "field's
leading model," yet also "very slow and computationally intensive."[^4] A table
that eliminates that cost changes who can run the analysis at all.

Kohli framed the release as the researcher reaching a comprehensive map of human
genetic variation "by simply opening a browser," and as unfinished Human Genome
Project business: "As the saying goes, we bought the book, but we did not
understand how to read it."[^3] Scientific American's characterisation is the
counterweight — "30 times larger than AlphaFold's database, although it is far
less accurate."[^5] DeepMind says as much itself: "we also view it as a baseline
rather than an endpoint," and "AlphaGenome has not been validated for, and is
not approved for, any clinical use."[^1]

This matters because the framing determines the question the rest of this
report has to ask: not whether nine billion scores exist, but what a score
means for the roughly 91% of them attached to a substitution no human has been
observed to carry.

## 02. The score is trained on rarity, not pathogenicity

AVI is presented as a pathogenicity-shaped number, but its supervision signal is
population frequency: a gnomAD filtering-allele-frequency threshold stands in
for the label, and that one design choice sets the terms on which every
downstream benchmark in this release should be read.

DeepMind describes the AlphaGenome Variant Impact score as combining the
strengths of AlphaGenome and AlphaMissense into a single number describing the
impact of each genetic variant.[^1] What the announcement does not foreground,
and the technical paper states plainly, is what that number was fit against:
"the population group max filtering allele frequency from gnomAD v4.1 is used to
derive proxy labels to train AVI scores," with variants above the 0.1%
filtering allele frequency taking the proxy-benign label and variants below it
the proxy-impactful label.[^2] No curated clinical assertion enters the
training target. AVI is, at its supervision layer, a rarity classifier
published on a deleteriousness scale.

:::kv
- {term: "Training label", def: "gnomAD v4.1 population-group max filtering allele frequency; above 0.1% = proxy-benign, below = proxy-impactful [^2]"}
- {term: "Feature count", def: "18 — the paper reports \"only 18 features were required for robust performance\" [^2]"}
- {term: "Combined models", def: "AlphaGenome in-silico saturation mutagenesis predictions plus AlphaMissense, in a supervised framework [^1][^2]"}
- {term: "Conservation inputs", def: "PhastCons 470-way and Zoonomia Cactus 241-way [^2]"}
- {term: "Other inputs", def: "Three Ensembl VEP loss-of-function annotations; indel indicators; protein-coding features [^2]"}
- {term: "Output scale", def: "PHRED-like percentile rank; AVI_PHRED runs 0 to approximately 80 [^7]"}
- {term: "Raw range", def: "AVI_RAW approximately -1.3 to +4.0; higher means more deleterious [^7]"}
- {term: "Reading 10 / 20 / 30", def: "Top 10% of the genome; top 1% of substitutions genome-wide; strongest one in a thousand [^3][^7]"}
:::

The sophistication here sits in the features, not in the target. The paper
describes AVI as integrating those saturation-mutagenesis predictions with
AlphaMissense, conservation metrics and protein-coding features in a supervised
framework, and reports feature attributions that decompose the score additively
into splicing, expression and protein categories.[^1][^2] Those are real
modelling achievements. They are also, all of them, ways of predicting *rarity*
better.

### The chain of proxies

Write the inference out link by link, because each link loses information.
Rarity is a proxy for {accent}purifying selection{/} — a variant is scarce
because carriers left fewer descendants. Purifying selection is a proxy for
{accent}fitness cost{/}, averaged over every genetic background and environment
the population has occupied. Fitness cost is, in turn, only loosely a proxy for
{accent}causing a specific disease in a specific patient{/}, which is the
question a clinical genomicist is actually asking. A variant can be strongly
selected against and still be irrelevant to the phenotype under investigation;
a late-onset or low-penetrance disease variant can carry almost no fitness cost
at all. The paper does not claim otherwise — it calls its labels proxy
labels.[^2] The distance between the two ends of that chain is the interpretive
space a single number silently collapses.

### Unobserved is the default state

The second problem is that rarity is measured against a finite sample. gnomAD v4
contains 786,500,648 SNVs from 807,162 individuals.[^10] Set that against the
roughly nine billion possible single-nucleotide substitutions the Atlas
enumerates, and the observed fraction is small.

:::iso
- {label: "Possible SNVs", glyph: "▩", count: 100}
- {label: "Ever observed", glyph: "▩", count: 9}
:::

:::note
Each glyph stands for roughly 90 million variants. The 9-in-100 ratio is our
arithmetic on the two cited figures — gnomAD v4's 786,500,648 catalogued SNVs
[^10] against the Atlas's ~9 billion enumerated substitutions [^1] — not a
figure either source publishes.
:::

Roughly nine possible substitutions in a hundred have ever been seen in a human.
For the other ninety-one, "below the filtering allele frequency" is true by
construction, and the proxy-impactful label is partly a statement about
sequencing depth rather than about biology. The scale of the real signal is
modest in comparison: a typical human genome differs from the reference at 4.1
million to 5.0 million sites, of which only 40,000 to 200,000 — 1% to 4% —
have a frequency below 0.5%.[^64]

:::callout(kind=warn, label="Shared confound")
ClinVar, the main evaluation set for scores of this kind, is ascertained on the
same correlate the label is built from: clinicians submit variants that are rare
and that turned up in affected patients. Training on rarity and testing on
ClinVar is therefore not a clean test against independent ground truth — the
predictor and the benchmark share a confound. This is a weaker and more precise
claim than leakage: nobody has shown that AVI saw its test labels. The point is
that agreement between a rarity-trained score and a rarity-ascertained benchmark
is partly guaranteed by how each was assembled, so the benchmark cannot be read
as though it were independent.
:::

The same coupling shows up inside DeepMind's own rare-disease benchmark.
Applying a gnomAD allele-frequency filter of 0.001 raised AVI's top-50 recall
from 29.5% to 74.3%, and CADD v1.7's from 12.5% to 61.0%.[^2] That filter
threshold is the same 0.1% used to derive AVI's training labels.[^2] The
filtered comparison is not an orthogonal preprocessing step; it removes exactly
the class of variants AVI was trained to score low. Two observations follow, and
they cut in different directions. By our arithmetic on the reported figures the
filter is worth 44.8 points of recall to AVI and 48.5 points to CADD — the
baseline gains slightly more, which is what you would expect if the filter is
doing frequency work both scores were partly doing internally. But AVI still
finishes 13.3 points ahead after filtering, and the paper does not report what
AVI adds on a set where the frequency signal has been fully neutralised.

### The steelman

Proxy-label training is not a defect; it is standard practice, and here it is
arguably the right call. CADD v1.7 — the baseline AVI is measured against — is
itself a supervised ensemble trained on proxy-neutral, near-fixed human-derived
variants versus simulated variants, on top of protein language models,
regulatory CNNs and other nucleotide-level scores.[^13] And training on
frequency specifically *avoids* the sharper circularity that dogged
AlphaMissense, which scored all 71 million possible human missense variants and
classified 32% likely pathogenic and 57% likely benign at cutoffs achieving 90%
precision on ClinVar.[^41] ClinGen's Sequence Variant Interpretation group later
found that AlphaMissense's developer-recommended 0.564 threshold does not reach
even the Supporting level of evidence, recalibrated PP3_Strong to 0.990, and
retained "potential circularities" as an unresolved limitation of newer
predictors.[^15] Against that, a frequency-derived label is the more honest
engineering choice. The critique is about how the resulting number should be
read — not that the design is illegitimate.

CADD's maintainers already say the quiet part about percentile scales: the
scaled scores are pure ranks, and the documentation advises "We therefore
recommend integrating C-scores with other evidence and to rank your candidates
for follow up rather than hard filtering," because on threshold choice "there is
not a natural choice here -- it is always arbitrary."[^12] AVI ships on the same
kind of scale, with the same absent natural cutoff, into a lookup interface that
also exposes prediction detail across 11 different output types.[^3][^4][^7]

> It has a clear use, but it also is probably going to be easily misinterpreted.
> We're talking about a very complex system and there's a lot of moving parts.
> — Carl de Boer, genomicist, University of British Columbia [^4]

DeepMind's own genomics lead frames the ceiling similarly, calling the
predictions "accurate enough to really point us in the right direction with
downstream studies" while cautioning researchers not to treat them as "the
universal truth."[^3] Why this matters: a rarity-trained percentile is an
excellent *prioritiser* and a poor *adjudicator*, so every benchmark in the next
section has to be read as evidence about ranking under a shared frequency
confound — not as evidence that AVI knows which variant makes a patient sick.

## 03. Reading the benchmark table the blog post doesn't show you

"Best-in-class" is a claim about a comparator set, and the Atlas's comparator
set is two general-purpose models — so the benchmark table shows a real, large
win in the categories where no specialist was entered, and a tie wherever one
was.

Start with what the announcement itself asserts. The DeepMind post says the AVI
score "provides best-in-class performance across many variant pathogenicity and
rare disease benchmarks," and then names no comparator model and no metric
anywhere on the page.[^1] That is a superlative with the denominator removed.
The technical paper supplies the denominator, and it is narrow: across the
headline ClinVar breakdown, the models AVI is measured against are GPN-Star, in
its vertebrate and mammal variants, and CADD v1.7.[^2]

:::exhibit(num="Exhibit 1", title="AVI versus next-best, ClinVar by consequence class", subtitle="AUPRC; higher is better", source="AlphaGenome Atlas technical paper; ARA analysis", note="Error bars in the source are 95% CIs from 100 bootstraps, so the 5'UTR margin of 0.01 is not a difference.")
:::bar-chart(title="ClinVar AUPRC by consequence class", orientation=horizontal, mode=grouped)
categories: Intronic, Synonymous, 3'UTR, 5'UTR, Protein-altering
AVI: 0.76, 0.57, 0.50, 0.26, 0.90
Next-best baseline: 0.44, 0.35, 0.18, 0.27, 0.86
:::
:::

The margins are not uniform, and the pattern in how they vary is the story. On
intronic ClinVar SNVs AVI scores 0.76 AUPRC against GPN-Star-V's 0.44; on
synonymous variants 0.57 against CADD v1.7's 0.35; on 3'UTR variants 0.50
against GPN-Star-M's 0.18. On protein-altering variants — the category with
decades of dedicated tooling behind it — the gap collapses to 0.90 versus
0.86.[^2] The three biggest wins are all in non-coding or silent territory,
measured against a conservation model and a general ensemble, with no
category-specific predictor in the race.

That framing matters because of what GPN-Star actually is. It is an alignment-
and phylogeny-based model — "Genomic Pretrained Network with Species Tree and
Alignment Representations" — whose signal is evolutionary conservation rather
than sequence-to-function prediction; its V, M and P suffixes denote vertebrate,
mammal and primate alignments, its training windows are selected using PhastCons
scores, and its loss upweights conserved elements.[^25] Beating a conservation
prior on intronic variants is a meaningful result, but it is not the same claim
as beating the best available intronic predictor. CADD v1.7, the other baseline,
is itself a supervised ensemble that already folds in protein language models,
regulatory CNNs and Zoonomia conservation[^13] — and AVI's own input features
include AlphaMissense, PhastCons 470-way and Zoonomia Cactus 241-way
conservation, and Ensembl VEP loss-of-function annotations.[^2] On the coding
axis, AVI and its nearest baseline are partly drawing on the same upstream
evidence, which is one plausible reason the protein-altering margin is the
smallest one in the exhibit.

Now look at the single category where a specialist *was* entered.

:::rank-list
- {label: "AVI / AlphaGenome (merged)", value: "0.943", pct: 100, highlight: true}
- {label: "SpliceAI", value: "0.940", pct: 100}
- {label: "Pangolin", value: "0.939", pct: 100}
- {label: "GPN-Star-V", value: "0.348", pct: 37}
- {label: "CADD v1.7", value: "0.289", pct: 31}
:::

On the splicing exon-extension task the paper reports AVI/AlphaGenome merged at
0.943 and notes that "SpliceAI (41) and Pangolin (42) also performed well at
this task (AUPRC: 0.940 and 0.939, respectively)," while on the same task
GPN-Star-V scores 0.348 and CADD v1.7 scores 0.289.[^2] Read the ranking as two
clusters rather than five ranks. The general-purpose baselines are roughly 0.6
AUPRC away; the specialists are 0.003 and 0.004 away, which given that the
paper's own error bars are "95% confidence intervals from 100 bootstraps"[^2] is
a tie, not a lead. SpliceAI is a 2019-era tool. The honest summary is that AVI
matches it.

The same discipline has to apply to the losses, and here the authors are
straightforward about them. The paper states plainly that "GPN-Star-V
outperformed AVI on 5'UTR ClinVar SNVs (0.27 vs. 0.26)."[^2] On TraitGym, AVI
ranks second to GPN-Star-M on Mendelian trait variants at 0.76 versus 0.77, and
leads on complex traits at 0.28 versus 0.27.[^2] All three of those are 0.01
gaps inside bootstrap intervals — none is a difference in either direction, and
the complex-trait number should not be reported as a win any more than the
Mendelian one should be reported as a defeat. TraitGym also anchors the absolute
scale: its design samples nine matched negative controls per positive causal
variant, matched on chromosome, consequence and TSS distance — and, for complex
traits, on minor allele frequency and LD score as well — so a random classifier
lands near 0.1 AUPRC.[^26] A 0.28 on complex traits is above
chance and nowhere near usable.

The comparator asymmetry becomes hardest to unsee when the two papers are set
side by side.

| Model | Appears as a baseline in |
|---|---|
| GPN-Star (V / M) | Atlas and GPN-Star [^2][^25] |
| CADD v1.7 | Atlas and GPN-Star [^2][^25] |
| SpliceAI | Atlas — splicing task only [^2] |
| Pangolin | Atlas — splicing task only [^2] |
| AlphaMissense | GPN-Star only; an AVI *input feature* in the Atlas [^25][^2] |
| PhyloP / PhastCons | GPN-Star only; PhastCons is an AVI *input feature* [^25][^2] |
| PrimateAI-3D | GPN-Star only [^25] |
| ESM-1b | GPN-Star only [^25] |
| Enformer | GPN-Star only [^25] |
| Borzoi | GPN-Star only [^25] |
| Evo 2 | GPN-Star only [^25] |
| Nucleotide Transformer | GPN-Star only [^25] |
| AlphaGenome | GPN-Star only [^25] |

GPN-Star's own paper benchmarks against a strictly larger comparator set than
the Atlas does, spanning PhyloP, PhastCons, CADD, Nucleotide Transformer, Evo 2,
GPN-MSA, ESM-1b, AlphaMissense, PrimateAI-3D and — for non-coding — Enformer,
Borzoi and AlphaGenome.[^25] TraitGym's published roster is similarly broad,
covering Enformer, Borzoi, Sei, GPN-MSA, Evo 2, Caduceus, HyenaDNA, Nucleotide
Transformer, phyloP, phastCons and CADD, with GPN-MSA leading on Mendelian
variants, CADD on complex traits, and the authors conceding that for complex
traits "none of the models does very well in absolute terms."[^26] No evidence
was found that REVEL, BayesDel, VEST4, MutPred2, PrimateAI-3D, ESM, Enformer,
Borzoi, Evo 2, Nucleotide Transformer, or phyloP and phastCons alone appear as
baselines anywhere in the Atlas evaluation.[^2][^25] And in GPN-Star's own
evaluation on non-coding OMIM and HGMD variants, sequence-to-function models
"performed substantially worse than evolutionary models on this task," with
GPN-Star (M) best on both.[^25] That is the reciprocal comparison the Atlas does
not run.

The counterpoint deserves equal weight, because parts of this record are strong
and the authors do not hide the parts that are not. On saturation genome
editing, AVI achieves the highest Spearman correlation with measured variant
effects in eight of ten screens and the best merged AUPRC — 0.668 versus CADD
v1.7's 0.647 on SNVs, and 0.759 versus 0.653 once indels are included.[^2] That
is functional assay data, not a curated database. The published AlphaGenome
Nature paper claims the model "matches or exceeds the strongest available
external models in 25 of 26 evaluations of variant effect prediction," up from
24 of 26 in the June 2025 preprint[^24][^23] — and the named loss in that record
is disclosed rather than buried: on MFASS, a massively parallel splicing
reporter assay, AlphaGenome "was outperformed by Pangolin (auPRC 0.54 vs. 0.51)
but surpassed SpliceAI and DeltaSplice."[^23] A team hiding behind its
comparator set does not publish its own defeats at that granularity. A
general-purpose score that ties the specialist on the specialist's own turf
while also covering intronic, synonymous and 3'UTR variants is a real advance;
the intronic and synonymous gains are large and probably durable.

Why this matters: intronic variants account for 1,005,231 of ClinVar's 4,561,224
records and missense variants for 2,538,230 — 22.0% and 55.7%, on overlapping
consequence annotations that do not partition the database[^63][^33] — so a
score whose demonstrated edge is concentrated where no specialist was
benchmarked will be applied at scale to exactly the categories its comparator
set never tested.

## 04. One genome at a time: the regime where the score is least validated

Sequence-to-function models score well when asked which genes are expressed
across the reference genome, and collapse when asked what one particular
person's variant does at one particular locus — and the second regime is the
only one a clinical variant score ever operates in.

The cleanest demonstration is Sasse et al.'s benchmark of Enformer on the ROSMAP
cohort of 839 individuals. Scored against population-average cortex expression
on the reference genome across 13,397 expressed protein-coding genes, the model
looks strong: the authors report "good prediction accuracy as measured by the
Pearson correlation coefficient R=0.58". Re-scored across individuals at 6,825
cortex-expressed genes, the same predictions produce "a large distribution in
Pearson's R (min R=−0.76, max R=0.84, mean = 0.01)".[^18] Nothing about the
model changed. Only the question did.

:::slope(left-label="Across genes", right-label="Across individuals", unit=r)
| Model | Across genes | Across individuals |
|-----------|------|------|
| Enformer  | 0.57 | 0.01 |
| Basenji2  | 0.52 | 0.01 |
| ExPecto   | 0.53 | 0.01 |
| Xpresso   | 0.33 | 0.01 |
:::

Be explicit about what that right-hand column is and is not. The left column
holds four separately published across-gene Spearman correlations against median
observed expression from Huang et al. — "0.57 for Enformer, 0.52 for Basenji2,
0.53 for ExPecto and 0.33 for Xpresso".[^19] The right column is
==one shared illustrative value, not four measured per-model figures==: Huang et
al. report only that "the distribution of cross-individual correlations is
centered close to zero for all models",[^19] and the 0.01 plotted here is Sasse
et al.'s ROSMAP mean for Enformer specifically.[^18] Read the slope as a
direction, not as four independent measurements.

The sharper failure is not magnitude but sign. Of the ROSMAP genes where
Enformer's predictions were "significantly correlated to observed expression for
598 genes," the model was "significantly anti-correlated with the true gene
expression for 195 (33%) of these genes"; Sasse et al. conclude it "fails to
correctly attribute the variants' direction of effect."[^18] Huang et al. reach
the same verdict independently on Geuvadis lymphoblastoid lines (n=421,
restricted to 3,259 genes carrying a significant eQTL): the models "often fail
to predict the correct direction of effect of cis-regulatory genetic variation
on expression."[^19] A score that ranks a variant highly and gets the sign
backwards is worse than no score at all, because it is confidently wrong in the
direction a curator is least equipped to check.

Both papers then do the thing that hurts. Against a linear PrediXcan elastic-net
baseline on the 1,570 genes where both applied, Sasse et al. count "921
significantly predicted gene by PrediXcan vs. 162 by Enformer, Mean R Enformer =
0.02, Mean R PrediXcan = 0.26" — and "all PrediXcan's significantly predicted
genes have a positive correlation between predicted and observed."[^18] Huang et
al. describe a per-gene elastic net over nearby variant dosages, window-matched
to Enformer's ~197 kb, as "a minimum baseline" that explains "much more
cross-individual variation."[^19] The deep model is not losing to another deep
model. It is losing to regression on genotype dosages.

There is a mechanistic reason, and it is the part AlphaGenome inherits
structurally. Karollus, Mauermeier and Gagneur found Enformer correlated
r = 0.81 with promoter strength but only r = 0.137 with enhancer strength in the
Bergman plasmid assay, and "strongly underestimates the effect of known
enhancers, particularly if they are distal to the TSS" — median predicted effect
around 4% against around 20% measured knockdown across 522 validated enhancers,
such that "the threshold for ~50% recall of validated enhancers is a ~3%
predicted effect."[^20]

:::compare
- {role: PROMOTER, name: "Enformer vs measured strength", value: "r 0.81"}
- {role: ENHANCER, name: "Enformer vs measured strength", value: "r 0.137"}
- {role: SUBJECT, name: "Median predicted enhancer effect", value: "~4%"}
:::

That is the across-gene score decomposed: a model that has learned very well
what a promoter looks like, and much less well what a distal regulatory element
*does*. Common non-coding variation is overwhelmingly the second kind.

Now the fair part, stated plainly. AlphaGenome is materially better here. An
independent single-author evaluation on GTEx personal genomes found it clearly
beat Enformer — 1,374 versus 430 gene-tissue pairs — while still reporting 2,459
positive against 971 negative correlations, roughly 28% wrong-signed, and
concluding that AlphaGenome's "performance still lags behind that of classic
machine learning models trained directly on personal-level data," beating
Elastic Net in only 218 pairs and Random Forest in only 63; the same author
notes DeepMind prohibits fine-tuning AlphaGenome outputs for downstream tasks.
This is a preprint, not peer reviewed, and it evaluated the June 2025 preview
through the API.[^21] A second preprint, also not peer reviewed, evaluating
sequence-to-function scores including AlphaGenome on multi-ancestry blood eQTLs
(per-ancestry n = 224, 209 and 235), reported Spearman rho no higher than 0.138
across all strata, direction-of-effect concordance of 50.2% to 54.7% on nominal
eQTLs, and performance near zero beyond 35 kb — but performance rose sharply on
high-PIP fine-mapped variants (rho 0.747 in one ancestry stratum, AUROC 0.82),
leading its authors to "support using S2F scores as prioritization evidence for
fine-mapped regulatory variants" rather than as standalone effect-size
predictors.[^22] That conclusion is close to how DeepMind positions AVI, and it
should be read as a qualified endorsement of the narrow use, not a dismissal.

DeepMind concedes the boundary in its own words. The model takes 1 megabase of
input DNA context;[^23] IEEE Spectrum notes enhancers can act at distances
outside roughly that window, and that many diseases involve multiple variants
rather than one.[^4] The AlphaGenome preprint states that "accurately capturing
cell type-specific expression deviations remains a challenging task," that
"further improvements are needed to precisely predict intermediate splicing
efficiencies and to capture tissue-specific nuances," and that predictive
accuracy "decays with distance to the target gene across all eQTL tasks."[^23]
Natasha Latysheva, a DeepMind author on the paper, was reported at a press
conference as saying the model "wasn't designed or validated for personal genome
prediction" — though this is a search-engine-recovered paraphrase of a
GenomeWeb article that could not be fetched directly, so the exact wording is
==unverified==.[^24] Seven named UK experts in the Science Media Centre roundup
all attached caveats: Professor Kristian Helin of the Institute of Cancer
Research noted "capturing cell type–specific regulation remains an important
challenge," and Dr Robert Goldstone of the Francis Crick Institute that
"AlphaGenome is not a magic bullet for all biological questions."[^48]

:::quote(attr="Xianghua Li, King's College London, Science Media Centre roundup on the AlphaGenome paper")
These predictions are not yet ready for use in clinics. [^48]
:::

The honest bottom line is an absence, not a verdict: one day after launch, no
published evaluation of the AVI score itself in the cross-individual regime
exists. That is not evidence AVI fails there — it is evidence nobody has yet
checked. This matters because every downstream use of a 9-billion-variant atlas,
from candidate triage to an ACMG-style evidence line, happens one genome at a
time, in exactly the regime where the model class it descends from has been
measured and found weakest.

## 05. The evidence bar AVI has not been asked to clear

Clinical genetics has had a formal calibration standard for computational
predictors for a decade, and its most consistent finding is that a tool's own
recommended threshold carries little or no evidentiary weight — AVI has not been
through that process, which is precisely why no AVI value should yet appear in a
variant classification.

The 2015 ACMG/AMP framework set the ceiling first: computational evidence enters
a classification only at Supporting strength, predictions from different
in-silico tools are treated as a *single* piece of evidence rather than as
independent votes, "it is not recommended that these predictions be used as the
sole source of evidence to make a clinical assertion," and the guideline warns
outright that such tools have "low specificity, resulting in over-prediction of
missense changes as deleterious."[^17]

ClinGen's Sequence Variant Interpretation working group later replaced that
qualitative ceiling with arithmetic. Starting from an estimated 4.41% prior
probability of pathogenicity, Pejaver and colleagues derived the local positive
likelihood ratio a score interval must achieve before it can be quoted at each
evidence strength.[^14]

| Evidence strength | Local LR+ required | Posterior probability | Tools reaching it (missense calibration) |
|---|---|---|---|
| Supporting | 2.406 | 0.0999 | CADD only after recalibration, from ≥25.3; its published default does not reach this bar [^14] |
| Moderate | 5.790 | 0.2108 | CADD's default of 20.0 falls in the moderate interval for BP4 — the benign direction [^14] |
| Strong | 33.53 | 0.6073 | BayesDel ≥0.50, MutPred2 ≥0.932, REVEL ≥0.932, VEST4 ≥0.965 — 4 of 13 [^14] |
| Very Strong | 1,124 | 0.9811 | None for pathogenicity; REVEL alone reaches it for benignity, at ≤0.003 [^14] |

:::source
ClinGen SVI missense calibration; thresholds derived at a 4.41% prior. [^14]
:::

The CADD result is the canonical cautionary case, because the developer default
did not merely fail to clear the bar — it pointed the wrong way. A score of 20.0
carried a local LR+ of 0.157 (95% CI 0.107–0.215), evidence *against*
pathogenicity, which the authors called "an inappropriate use of this threshold
as evidence for pathogenicity."[^14]

The same defaults over-called at scale. Against a 4.41% prior, the three tools
flagged a large share of ordinary gnomAD variation as damaging — "suggesting a
high false positive rate with respect to PP3" — and stacking them did not rescue
the result: no pairwise or three-way consensus reached Supporting, with
PolyPhen-2 closest at LR+ 1.993.[^14]

:::bars
- {label: "SIFT (default ≤0.05)", value: "50.4%", pct: 50}
- {label: "PolyPhen-2 (default ≥0.902)", value: "29.3%", pct: 29}
- {label: "CADD (default ≥20)", value: "65.1%", pct: 65}
- {label: "Estimated prior probability of pathogenicity", value: "4.41%", pct: 4}
:::

That is also why ClinGen tells laboratories to pick one genome-wide tool and
commit to it in advance: the choice "must always be made before seeing
prediction results and preferably other lines of evidence," to avoid "cherry
picking" among methods that "overlap and thus do not offer independent
assessment of pathogenicity" — and it cautions that the calibrated thresholds
"must be considered with utmost care for any use outside our
recommendations."[^14]

The nearest precedent for AVI is AlphaMissense, and it followed the pattern. Its
developer-recommended cutoff of 0.564 met neither the Supporting level for
pathogenicity nor for benignity; recalibration put PP3_Supporting at 0.792–0.905,
Moderate at 0.906–0.971 and Strong at ≥0.990, with the entire 0.170–0.791 span
ruled indeterminate — gains over REVEL, BayesDel, VEST4 and MutPred2 were "at
best only modest."[^15] For splicing the discipline is the same: SpliceAI ≥0.2
earns PP3 (LR 15.99, 78% sensitivity) and ≤0.1 earns BP4 (LR 0.17, 87%
specificity), 0.1–0.2 is uninformative, and even a well-calibrated splice
prediction is applied at Supporting weight only and can never yield PVS1 on its
own.[^16]

:::timeline
- {date: 2015, headline: "ACMG/AMP variant interpretation framework", body: "Computational evidence capped at Supporting; multiple tools count as one piece of evidence, never the sole basis for an assertion."}
- {date: 2022, headline: "ClinGen SVI PP3/BP4 calibration", body: "Likelihood-ratio thresholds derived for 13 missense predictors from a 4.41% prior; SIFT, PolyPhen-2 and CADD defaults fail to reach Supporting."}
- {date: 2023, headline: "ClinGen splicing recommendations", body: "SpliceAI calibrated at 0.2 for PP3 and 0.1 for BP4; predictive codes applied at Supporting weight only."}
- {date: 2025, headline: "ClinGen SVI calibrates AlphaMissense", body: "The 0.564 developer cutoff clears neither direction; recalibrated Supporting begins at 0.792 and Strong at 0.990."}
- {date: 2025-04, headline: "SVI working group retired", body: "Its general recommendations, including the PP3/BP4 calibration, were marked archived in July 2025."}
- {date: 2026-09-08, headline: "AlphaGenome Atlas and AVI released", body: "A percentile-ranked impact score with no published mapping from any AVI value to an ACMG/AMP evidence strength."}
:::

AVI is published on a PHRED-like percentile scale where 10 marks the top 10% of
variants and 30 the top 0.1%, and no accessible source maps any AVI cut point to
an ACMG evidence strength.[^3][^2] The correct inference is not that AVI is a
poor predictor — it is that ==no threshold on AVI currently carries any defined
evidentiary weight, because nobody has computed one==.

The counterpoint deserves its full weight: DeepMind states plainly that
"AlphaGenome has not been validated for, and is not approved for, any clinical
use,"[^1] and the Atlas paper positions Atlas and AVI as research tools that can
serve only as part of an evidence chain, not as sufficient evidence on their
own.[^2] By the AlphaMissense precedent, calibration takes one to two years, so
its absence one day after launch is expected rather than negligent. And the
calibrated framework turns out to be conservative when someone actually runs it
end to end. A 2024 study applied the recommended criteria across 300 Rare
Genomes Project probands and found that the strong pathogenic tier fired for
about one variant per patient, with a handful more at the weaker tiers and
several dozen picked up by the benign code instead — the framework's practical
effect was to suppress pathogenic calls rather than multiply them.[^65] That is
an argument *for* the calibration process, not against new tools entering it.

:::callout(kind=warn, label="Governance gap")
The road to a calibrated AVI is less clearly marked than it was. ClinGen retired
the SVI working group in April 2025 and archived its general recommendations,
including the PP3/BP4 calibration, in July 2025.[^58] Nor does regulation fill
the gap: FDA's 2018 recognition of ClinGen covers only germline variants in
hereditary disease curated through an approved Variant Curation Expert Panel,
not computational predictions,[^44] and after the May 2024 laboratory-developed
test rule was vacated in its entirety on 2025-03-31 and FDA reverted the
regulation by final rule on 2025-09-19, no standalone in silico pathogenicity
predictor was found to be FDA-cleared.[^62]
:::

Why this matters: the gap between "the top 0.1% of predicted effects" and
"Supporting evidence toward a pathogenic call" is not a rounding step but a
measured likelihood ratio that no one has yet measured for AVI — which is the
concrete content of Dr Xianghua Li's assessment that "these predictions are not
yet ready for use in clinics."[^48]

## 06. The case studies, with their denominators restored

Both of DeepMind's early-validation stories are real, and neither is a
diagnostic yield — restoring the denominators shows what the Atlas plausibly
adds and what it has not yet demonstrated.

Start with the rare-disease case. DeepMind's blog reports that Broad Institute
researchers, working with the GREGoR Consortium, used AVI to rank previously
overlooked variants and "discovered a variant affecting a gene called DNM1,"
tied to epileptic encephalopathy, where the variant "created an incorrect splice
site" causing "an abnormal extension of the resulting protein," later confirmed
by experimental screens.[^1] The technical paper supplies the denominator the
blog leaves out: the screen involved "systematically ranking and analyzing all
small de novo variants in 814 individuals with parent and proband genomes
available."[^2]

:::stats
- {label: GREGoR trios screened by AVI, value: "814"}
- {label: Publicized new diagnoses, value: "1"}
- {label: GREGoR participants unsolved, value: "84%"}
- {label: Yield added by genome over exome, value: ">8", unit: "pts"}
:::

One new diagnosis is publicized from that screen, and the paper does not state a
diagnostic yield across the cohort.[^2] Be precise about what is inference: the
814 is stated, but "one publicized solve" is *our* reading of the absence of any
other reported case, not a numerator DeepMind reports. It bounds what has been
*shown*, not what the screen found. The cohort context cuts both ways — GREGoR
is an NHGRI consortium enriched for exome-negative cases, "the majority of
participants remain unsolved (84%)," and short-read genome sequencing added over
8 percentage points of yield over exome alone.[^39] A hard cohort makes one
solve more impressive and also makes a single anecdote a weak estimator.

The retrospective benchmark is the part with a real denominator, and it is where
the framing matters most. On 112 known likely-pathogenic variants, AVI ranked
the causal variant in the top 50 candidates 29.5% of the time against CADD
v1.7's 12.5% — a headline 2.4x, and the one Atlas benchmark figure the press
coverage independently reports.[^3] But restrict to variants surviving a gnomAD
allele-frequency filter of 0.001, the routine first move in any diagnostic lab,
and recall at top 50 rises to 74.3% for AVI and 61.0% for CADD — a post-filter
pair that appears only in the technical paper.[^2] The 2.4x
is measured on an unfiltered variant set nobody actually works from; after the
filter the gap is 13.3 points — that subtraction is our arithmetic on the cited
figures, not a published statistic.

:::timeline
- {date: 2025, headline: "UK Biobank rare non-coding baseline", body: "54,306 individuals, 2,907 proteins, 1.1 billion variants, 123 million aggregate tests; 604 rare non-coding single-variant associations and 357 conditionally independent regions, 74 of them undetectable by single-variant testing alone."}
- {date: 2026-09-08, headline: "Atlas retrospective, 112 variants", body: "Top-50 recall 29.5% for AVI against 12.5% for CADD v1.7 unfiltered; 74.3% against 61.0% after a gnomAD 0.001 allele-frequency filter."}
- {date: 2026-09-08, headline: "GREGoR prospective screen, 814 trios", body: "All small de novo variants ranked; one publicized new diagnosis in DNM1; no cohort-wide diagnostic yield reported."}
- {date: 2026-09-08, headline: "UK Biobank re-analysis, 54,000+ participants", body: "Rare variants grouped by predicted molecular effect; 22% more non-coding associations; 19 BMI regions from the top 1% of flagged non-coding variants."}
:::

Case B has the same shape. Dr Gareth Hawkes applied the Atlas to whole-genome
data from "over 54,000 UK Biobank participants," grouped rare variants by
predicted molecular effect, and "uncovered 22% more non-coding genetic
associations"; for BMI, focusing on the top "1% of non-coding variants," he
"identified 19 genetic regions" — which the blog frames as pointing "toward the
next round of targeted study," with no claim that any is novel.[^1] The missing
term is the baseline the 22% is measured against. A 2025 study of rare
non-coding variation used 54,306 individuals, 2,907 proteins and 1.1 billion
variants across 123 million aggregate tests, finding 604 rare non-coding
single-variant associations plus "357 conditionally independent associated
regions, of which 74 (21%) were not detectable by single-variant testing
alone."[^40] The cohort size and method match, so the comparator appears to be
the same author's own prior pipeline on the same cohort — that is our inference
from the match, not something DeepMind states. Note also that 54,000 is not a
data ceiling: UK Biobank recruited 503,317 participants and released 490,640
whole genomes in November 2023.[^31]

The reason to insist on denominators is the historical base rate for exactly
this residual. The 100,000 Genomes Project pilot "made genetic diagnoses in 25%
of the probands," with "14% of the diagnoses ... made by means of the
combination of research and automated approaches" — the pathway non-coding
findings travel through — and 35% yield for likely-monogenic against 11% for
likely-complex phenotypes.[^37] A dedicated deep-intronic and non-canonical
splicing sweep across 38,688 individuals produced 258 de novo splicing variants
in known disease genes, "35 new likely diagnoses," 26 of those 35 intronic and
"left out of the standard tiering pipeline," and 6 confirmed molecular
diagnoses, 4 via RNA studies.[^38] Bar widths below are illustrative log-scaled
proportions, not linear shares of the first row; a linear rendering would
collapse the last three rows below one pixel.

:::bars
- {label: "Individuals sequenced", value: "38,688", pct: 100}
- {label: "De novo splicing variants in known disease genes", value: "258", pct: 34}
- {label: "New likely diagnoses", value: "35", pct: 17}
- {label: "Confirmed molecular diagnoses", value: "6", pct: 8}
:::

Against that base rate — an entire sequencing-modality upgrade buys about 8
points, and a purpose-built splicing sweep across 38,688 people confirmed six
diagnoses — a re-ranking score that surfaces more candidates is genuinely
valuable but should not be expected to move yield by a large margin.[^38][^39]

The counterpoint deserves its full weight. The DNM1 variant creates "a
brain-specific cryptic splice acceptor site resulting in a 13 amino acid
in-frame extension of exon 10a," validated by a multiplexed splicing reporter
screen that "measured mean alternative 3' splice site rates across replicates
and 5 cell lines."[^2] A brain-specific cryptic acceptor is precisely the
mechanism blood-derived RNA-seq cannot see, and splicing is empirically where
non-coding diagnoses come from — 26 of 35 in the 100,000 Genomes sweep were
intronic variants the tiering pipeline discarded.[^38] This is the
highest-probability place for the Atlas to pay off, and the case was
experimentally closed rather than asserted. Martin Kircher of the Max Delbrück
Centre calls it "a useful and generous way to scale up access to a strong
model," while adding that it will not replace experiments or the accounting for
details of individual cases.[^6]

Why this matters: roughly 300 million people worldwide live with a rare disease,
71.9% of which are genetic,[^53] and among 6,507 diagnosed patients "73%
(4756/6507) were misdiagnosed at least one time" with 25% waiting five years or
more[^54] — so a tool that promotes better candidates is worth having, provided
it is evaluated on candidates promoted rather than on a yield it has not yet
claimed.

## 07. Whose genome is the reference?

"Every possible single-letter change in the human genome" is a claim bounded
twice — once by the coordinate system the letters are enumerated against, and
once by the functional data the effects are supervised on — and both bounds lean
the same way.

Take the coordinate system first. GRCh38 is not a population consensus; it is a
mosaic, and the assembly papers say so plainly: "GRCh38 and its predecessors
thus comprise mosaics of many haplotypes, albeit with a single library (RP11)
contributing the majority," with RP11 supplying roughly 70% of the primary
assembly.[^29] How much sequence that omits is now measurable. The Human
Pangenome Reference Consortium's draft — 47 diploid individuals, 94 haplotype
assemblies — "adds 119 million base pairs of euchromatic polymorphic sequences
and 1,115 gene duplications relative to GRCh38," cutting small-variant discovery
error by 34% and raising detected structural variants per haplotype by
104%.[^30] An exhaustive enumeration over GRCh38 is exhaustive over one mosaic,
not over the species.

The second bound is the supervision. AlphaGenome "simultaneously predicts 5,930
human or 1,128 mouse genome tracks across 11 modalities" from a 1 megabase input
context, with GTEx contributing 49 tissues; the released Hugging Face
checkpoints exclude GTEx tissue data for licensing reasons.[^23] Those 5,930
tracks are not a neutral sample of humanity. GTEx v8's eQTL cohort of 838
postmortem donors was "715 (85.3%) were European American, 103 (12.3%) African
American, and 12 (1.4%) Asian American," with 16 (1.9%) Hispanic/Latino and 557
(66.4%) male.[^27]

:::donut(center-label="838")
- {label: European American, value: 85.3}
- {label: African American, value: 12.3}
- {label: Hispanic/Latino, value: 1.9}
- {label: Asian American, value: 1.4}
:::

These are the GTEx v8 eQTL-cohort percentages exactly as the source reports them;
they sum to about 100.9 rather than 100 because the source's ancestry and
Hispanic/Latino categories are separately rounded and partially overlap.

The cell-line side is narrower still. ENCODE's Tier 1 common cell types are
GM12878, K562 and H1-hESC; GM12878 is "a lymphoblastoid cell line produced from
the blood of a female donor with northern and western European ancestry by EBV
transformation," K562 comes from a female patient with chronic myelogenous
leukemia, and HepG2, at Tier 2, is a male liver carcinoma line; ENCODE's own
karyotype remarks note only that GM12878 and HUVEC are near-normal.[^28] Cancer
provenance matters independently of ancestry: a tumour-derived line is a strange
place to learn what a regulatory element does in healthy tissue.

:::stack-rows
categories: [European / white, Other or non-European]
rows:
  - {label: GTEx v8, values: [85.3, 14.7]}
  - {label: UK Biobank, values: [94.6, 5.4]}
  - {label: ENCODE Tier 1, values: [100, 0]}
:::

Two honesty notes on that chart. The ENCODE row is *our* characterisation, and a
weak one: only GM12878's ancestry is documented in the cited source,[^28] while
the ancestries of K562 and H1-hESC are not stated there at all, so read that row
as an illustration of how few donors underlie Tier 1 rather than as a
composition statistic. And every "other or non-European" figure is simply 100
minus the cited European or white share, not an independently reported number.
The UK Biobank share is the published one: it recruited 503,317 participants who
"are mostly (94.6%) of white ethnicity."[^31] The Atlas's own UK Biobank case
study ran on over 54,000 participants and reports 22% more non-coding genetic
associations — and the announcement states no ancestry stratification of that
result.[^1]

That is where the chain closes badly, because the populations with the least
representation in the training data already carry the most uncertain calls. In a
cohort of 36,684 people with no personal cancer history tested on one 30-gene
panel, the combined hereditary breast/ovarian and Lynch VUS rate was 5.8% for
European-ancestry patients, 7.1% Hispanic, 12.3% African and 13.1% Asian and
Pacific Islander. Detection of actionable variants ran the other way: in the
other cancer genes on that same 30-gene panel, pathogenic and likely pathogenic
calls reached 7.6% for European-ancestry patients against 2.4% for
African-ancestry patients.[^45] The two figures come from different gene subsets
within one cohort and should not be read as a single continuous rate.

:::compare
- {role: EUROPEAN, name: "VUS rate, HBOC + Lynch genes", value: "5.8%"}
- {role: AFRICAN, name: "VUS rate, same genes", value: "12.3%"}
- {role: SUBJECT, name: "P/LP detection, other cancer genes, African vs European", value: "2.4% vs 7.6%"}
:::

The same pattern holds at scale: across 493,515 Invitae probands, "frequencies
of VUS and PGV remained significantly higher (46% v 32%; P < .0001) and lower
(9% v 13%; P < .0001) in AA/B".[^46] A predictor trained mostly on
European-ancestry functional data, evaluated without ancestry stratification, is
weakest precisely where clinical uncertainty is highest. And where someone did
stratify, the ceiling was low: an independent evaluation of sequence-to-function
scores including AlphaGenome on multi-ancestry blood eQTLs reported Spearman rho
no higher than 0.138 across all ancestry strata, on per-ancestry sample sizes of
224, 209 and 235 — a preprint, not peer reviewed.[^22]

There is a third, separable bound. "We cover the other 98%" is a statement about
coordinates, not function. Zoonomia found that "at least 332 million bases
(~10.7%) in the human genome are unusually conserved across species" across 240
mammals, with 3.3% significantly constrained at single-base 5% FDR, 4,552
ultraconserved elements, and 80% of constrained bases lying outside coding exons
— half of which lack any ENCODE annotation, against roughly 1–2% protein-coding
sequence and ENCODE's 2012 biochemical-activity figure of 80.4%.[^32] Half the
constrained non-coding genome has no assay in the panel at all. That cuts both
ways, and it should be said as such: it is a limit on today's supervision *and*
evidence of real headroom the model has simply not been given data for.

:::callout(kind=info, label=Counterpoint)
The steelman is strong. Over 100 million indels observed in gnomAD, UK Biobank
and All of Us were scored, with All of Us contributing the variant list for
indels — a genuine widening of who gets enumerated, even though it does not
enter model training.[^2] The disparity is also narrowing on its own: on ten
high- and moderate-penetrance genes, Invitae VUS rates fell between 2015 and
2022 from 42.5% to 17.4% for African American and Black patients and from 22.9%
to 10.8% for non-Hispanic white patients.[^46] And this is a field-level
constraint — every model in this class trains on the same consortia — not an
AlphaGenome-specific defect.
:::

Why this matters: a variant-effect atlas is only as universal as the cohort that
taught it what "effect" looks like, so until ancestry-stratified evaluation is
published, the safest reading is that the Atlas is strongest for the patients who
already had the fewest unresolved variants.

## 08. What a percentile rank does to a candidate list

A percentile rank over nine billion variants does not, by itself, produce a
tractable candidate list — it produces a very long one, sorted.

The Ensembl VEP plugin for AVI emits `AVI_PHRED` by default, documented as a
"PHRED-scaled quantile (0 to approximately 80)" in which "A phred of 20 means
the variant is among the top 1% most deleterious substitutions
genome-wide."[^7] That is CADD's convention transplanted intact: scaled scores
are percentile ranks over all possible SNVs, so 10 is the top 10%, 20 the top 1%,
and 30 the top 0.1%.[^12] What follows is arithmetic on that cited scale
definition, not a finding of ours: across an atlas of nine billion
substitutions, a phred ≥ 20 cut selects on the order of ninety million rows, and
phred ≥ 30 still selects about nine million. {accent}A quantile cannot be
scarce.{/} Scarcity has to come from somewhere else.

Somewhere else is the individual genome, where the numbers are merely large. A
typical human genome differs from the reference at 4.1 to 5.0 million sites, of
which only 40,000 to 200,000 — 1 to 4% — sit below 0.5% population
frequency.[^64] What an actual diagnostic funnel looks like was measured
directly in a whole-genome study of neurodevelopmental trios, which reported "on
average ∼5.8 × 10^6 variants in the noncoding regions per genome (>99% of the
variants), of which ∼455 000 are rare and ∼35 200 have a higher CADD score value
than their region-specific thresholds"; adding a de novo inheritance filter cut
that to roughly 80 variants, about 8 of them above threshold.[^55]

:::bars
- {label: "Non-coding variants per genome", value: "~5.8M", pct: 100}
- {label: "Rare", value: "~455,000", pct: 55}
- {label: "Above region-specific CADD threshold", value: "~35,200", pct: 38}
- {label: "De novo", value: "~80", pct: 12}
- {label: "De novo and above threshold", value: "~8", pct: 6}
:::

:::note
Bar widths are illustrative log-scaled proportions, not linear shares — on a
linear axis every stage after the first would render as an invisible sliver. The
underlying analysis covered two trios.[^55]
:::

Read the funnel in the order it collapses. Rarity strips out most of the
non-coding candidates; the score strips out most of what rarity left; and the two
together still leave about 35,200 variants per genome, which is not a list
anyone works through. The collapse to single digits comes from inheritance
pattern, and in practice from phenotype after it. The score orders the
survivors. Rarity and inheritance are what create them. {accent}A percentile
score is a re-ranker inside a filter stack, not a filter.{/}

CADD's documentation says exactly this, about as plainly as documentation can:
"We therefore recommend integrating C-scores with other evidence and to rank
your candidates for follow up rather than hard filtering," and on where to draw
a line, "there is not a natural choice here -- it is always arbitrary."[^12] The
advice did not hold. When ClinGen calibrated CADD against clinical evidence
strength, the tool's own default of 20.0 fell in the score interval
corresponding to moderate evidence for BP4 — the benign direction — and at
developer defaults CADD flagged 65.1% of gnomAD variants as damaging against an
estimated 4.41% prior probability of pathogenicity.[^14]

An arbitrary threshold matters because the space downstream of it is already
saturated with uncertainty. ClinVar held 4,561,224 variation records as of
2026-09-08: 2,373,336 uncertain significance (52.0%), 1,166,236 likely benign
(25.6%), 281,265 benign (6.2%), 256,785 pathogenic (5.6%) and 166,953 likely
pathogenic (3.7%) — pathogenic plus likely pathogenic together being 423,738, or
9.3%.[^33]

:::donut(center-label="4.56M")
- {label: Uncertain significance, value: 52.0}
- {label: Likely benign, value: 25.6}
- {label: Benign, value: 6.2}
- {label: Pathogenic, value: 5.6}
- {label: Likely pathogenic, value: 3.7}
- {label: Conflicting or unclassified, value: 6.9}
:::

:::source
The five named buckets sum to 93.1%; the sixth slice is the residual to 100%,
not a category ClinVar itself publishes. [^33]
:::

The documented failure mode of a free, ranked, uncalibrated score is not that
people ignore it. In a survey of 3,672 breast-cancer patients (68% response) and
their 377 attending surgeons (78% response), adjusted bilateral-mastectomy
probabilities among average-pretest-risk patients were 85% with a pathogenic
mutation, 51% with only a variant of uncertain significance, and 42% with no
mutation detected; among lower-volume surgeons, 50% managed BRCA1/2 variants of
uncertain significance the same as pathogenic mutations, against 24% of
higher-volume surgeons — the authors concluding that "half of average-risk
patients with VUS undergo BLM, suggesting a limited understanding of results
that some surgeons share."[^36] The cost of a wrong call is also not evenly
distributed: of 94 variants previously reported as causing hypertrophic
cardiomyopathy, five were too common in the general population to be pathogenic,
the top five accounted for 74% of the misclassified variation, and seven
patients — all of African or unspecified ancestry — had received "pathogenic" or
"presumed pathogenic" reports, misclassifications that "invalidate risk
assessments undertaken in relatives, requiring a chain of amended reports and
management plans."[^35] The same shape recurs wherever ranked output reaches
consumers unmediated: across 49 patients whose direct-to-consumer raw genotype
flags were sent for clinical confirmation, "60% of the variants analyzed were
confirmed, while 40% were not confirmed (false positives)" — though that cohort
was self-referred, no third-party service was named, and the authors later
clarified they had assessed raw data files rather than FDA-authorized
reports.[^57]

The honest counterpoint is that uncertainty mostly resolves the boring way.
Across 1.45 million individuals and 1.67 million initial tests at one
laboratory, "7.7% (2048 of 26 670) of unique variants of uncertain significance
were reclassified" — and of those, the split was lopsided.[^34]

:::rank-list
- {label: "Downgraded to benign or likely benign", value: "91.2%", pct: 100, highlight: true}
- {label: "Upgraded to pathogenic or likely pathogenic", value: "8.7%", pct: 10}
:::

:::note
This is the split *within* the 7.7% of unique VUS ever reclassified at all;
median time to amended report was 1.17 years for downgrades and 1.86 years for
upgrades, while definitive calls were far more stable — 0.7% of pathogenic and
likely pathogenic, and 0.2% of benign and likely benign, unique variants were
reclassified. [^34]
:::

So the base-rate-correct posture toward a high-ranking uncertain variant is
skepticism, and a score that raises the visibility of uncertain variants without
changing their prior mostly manufactures work that resolves benign years later.

The regulatory position is genuinely favourable to DeepMind, and it should be
said. FDA's Clinical Decision Support guidance, reissued 2026-01-29 under docket
FDA-2017-D-6569, names a "Prioritized list" of preventive, diagnostic or
treatment options as an acceptable non-device output, and fails software under
Criterion 3 only when it "provides a specific preventive, diagnostic or
treatment output or directive" — a ranked variant list is the former, not the
latter.[^56] The exposure is Criterion 4, which requires a clinician be able to
independently review the basis, including "a description of the data relied upon
so that an HCP can assess whether the data is representative of their patient
population" and "a description of the results from clinical studies conducted to
validate the algorithm/recommendations"; the same guidance names the risk it is
guarding against, that "Automation bias is the propensity of humans to over-rely
on a suggestion from an automated system."[^56] That is worth pairing with the
licence split from section 01: the feature attributions that would supply
Criterion 4's basis are the non-commercial tier, while the bare score is the
portable one.[^7] DeepMind states that "AlphaGenome has not been validated for,
and is not approved for, any clinical use."[^1] Under 21 CFR 801.4, though,
intended use is established by "labeling claims, advertising matter, or oral or
written statements," by "the circumstances surrounding the distribution of the
article," and even where a product is "offered or used for a purpose for which
it is neither labeled nor advertised" — so a research-use disclaimer is itself a
labeling statement, and is not dispositive.[^56]

The reason this is urgent rather than academic is distribution. Ewan Birney,
Director of EMBL's European Bioinformatics Institute, says his organisation is
working to build the AVI score into Ensembl's Variant Effect Predictor, because
"These tools reach their full value when they're open and plugged into the wider
data ecosystem."[^3] That is correct, and it is also the mechanism: VEP is where
a score stops being a website and becomes a column in every diagnostic
pipeline's output — at which point the arbitrariness of the threshold someone
picks for that column is no longer the model's problem to disclose but the
field's problem to absorb.

## 09. What would break this thesis

Three claims carry this report: that AVI's supervision signal is population
rarity, that its genome-wide comparator set is two models, and that no
calibrated threshold exists. Each is falsifiable, and it is worth naming exactly
what would falsify it.

The rarity claim rests on a single sentence in the technical paper stating that
"the population group max filtering allele frequency from gnomAD v4.1 is used to
derive proxy labels to train AVI scores."[^2] If the published bioRxiv version
shows a second, clinically-labelled training stage, or an ablation demonstrating
that AVI's ClinVar performance survives with the frequency signal removed, the
central argument of section 02 weakens sharply. That ablation is the single most
useful experiment DeepMind could publish, and its absence is currently the load
-bearing gap. The comparator claim is the easiest to overturn: any supplementary
table showing REVEL, BayesDel, Enformer, Borzoi or Evo 2 as Atlas baselines
would retire section 03's framing, and the Atlas paper's own inclusion of
SpliceAI and Pangolin on the splicing task shows the authors do enter specialists
where they think it matters.[^2] The calibration claim is the most likely to
expire: it is an absence one day after launch, and by the AlphaMissense
precedent a ClinGen-style calibration would be expected within one to two
years.[^15]

### The AlphaFold analogy, tested on its mechanics

The comparison every write-up reaches for is AlphaFold, and it is worth being
precise about why AlphaFold was credible immediately. CASP is a blinded,
prospective, third-party assessment with sequestered targets, and AlphaFold2's
CASP14 result was not close: group 427 scored a summed z-score of 244.02 across
92 domains against the runner-up group's 90.82.[^50] Nothing of that shape
exists for regulatory genomics. The nearest analogue, CAGI, concluded across
five editions and 50 blind challenges that assessment of regulatory-variant
methods was "less definitive," with performance "potentially suitable only for
auxiliary use in the clinic,"[^60] and its CAGI5 regulation-saturation challenge
topped out at an AUC of 0.81 for promoters and 0.79 for enhancers — with the
assessors noting that the challenge's own train/test split "is biased by
information leakage from the local context."[^47] AlphaGenome's reported CAGI5
result is a retrospective evaluation on that already-published dataset, not a
blind entry.[^23] Enformer, the direct ancestor of this model line, was itself
introduced on retrospective benchmarks.[^49]

The analogy also flatters AlphaFold in a way worth resisting. Even for proteins
— where a single measurable native fold exists — structure prediction is
documented as poor at exactly the task AVI attempts. AlphaFold2 predicts a
BRCA1 BRCT missense mutant and its wild type at an average Cα RMSD of 0.6 Å, and
scores a myosin VI mutant *higher* in confidence than the wild type;[^51] a
systematic test against experimental ΔΔG and a large GFP mutation dataset found
"a very weak or no correlation."[^52] If the most successful structure model in
history is weak on variant effects in the domain with unambiguous ground truth,
the prior for a regulatory model in a domain with no single ground truth should
be set accordingly.

### The ceiling on checking any of this

The deepest constraint is not modelling but measurement. MaveDB, the central
repository for multiplexed assays of variant effect, held over 7 million variant
effect measurements across 1,884 datasets as of November 2024[^59] — under 0.1%
of the Atlas's nine billion rows by our arithmetic, and dominated by protein
assays rather than regulatory ones. The clinical gold standard is narrower
still: saturation genome editing of BRCA1 assayed "96.5% of all possible single
nucleotide variants (SNVs) in 13 exons," producing function scores for nearly
4,000 SNVs in one gene.[^61] The field cannot experimentally check most of what
the Atlas predicts, and will not be able to for a long time. That is the
strongest argument *for* a resource like this — prediction is what you use when
measurement is unavailable — and simultaneously the reason no volume of
prediction substitutes for calibration against the measurements that do exist.

### Where this report could be wrong

An adversarial pass over the three load-bearing claims above found no
contradicting source for any of them: the rarity-training sentence, the
two-model comparator set, and the across-gene-versus-across-individual collapse
all survived. That is a real but bounded reassurance. The two AlphaGenome-era
claims rest on a technical PDF too large to fetch directly, so what was
established for them is the absence of a contradiction rather than independent
confirmation; only the third claim was checked line by line against its primary
sources.[^18][^19] Notably, no DeepMind-authored page reachable at launch —
blog, docs, repository or community forum — states any training target for AVI
at all.[^1][^8][^9]

Three ways. First, the cross-individual critique in section 04 is built on
Enformer-era evidence plus two non-peer-reviewed preprints on the June 2025
AlphaGenome preview;[^18][^19][^21][^22] AlphaGenome is measurably better than
Enformer on that axis, and the AVI score has never been tested there at all, so
the honest status is untested rather than failed. Second, the "trained on
rarity" framing could be read as an accusation of circularity when it is not:
the point is that a rarity-trained score tested on a rarity-ascertained
benchmark is not an independent test, which is a claim about inference, not
integrity. Third, the licence critique may prove moot — the static AVI table
already carries commercial permission, the code is on GitHub,[^8] and Ensembl
integration is under way,[^3] so the practical openness may exceed what the
terms literally guarantee.

:::position(confidence=medium, horizon="2027-Q3")
stance: "AVI will be adopted fast as a triage column and will not carry an ACMG-calibrated evidence weight for at least a year, and its first published cross-individual evaluation will land materially below its ClinVar numbers."
consensus: "Coverage frames the Atlas as a step toward clinical genome interpretation, treating the benchmark table as evidence of clinical readiness."
resolves: "A ClinGen-style local likelihood-ratio calibration of AVI thresholds, and any independent ancestry-stratified or personal-genome evaluation of the AVI score."
:::

The fair summary is the one DeepMind itself offers and most coverage skipped:
the Atlas is "a baseline rather than an endpoint."[^1] It settles a compute and
access problem, it demonstrably improves candidate ranking on intronic and
synonymous variants against the baselines it chose, and it produced at least one
experimentally-validated diagnosis in a hard cohort.[^2] It settles nothing
about whether a single percentile is the right shape for the answer.

:::references
- {id: 1, title: "AlphaGenome Atlas: Molecular predictions for 9 billion human DNA variants", url: "https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/", source: Google DeepMind, date: "2026-09-08"}
- {id: 2, title: "AlphaGenome Atlas (technical paper, PDF)", url: "https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf", source: Google DeepMind, date: "2026-09-08"}
- {id: 3, title: "Google DeepMind publishes AI-powered predictions for all 9 billion possible single-point mutations to human DNA", url: "https://fortune.com/2026/09/08/google-deepmind-ai-predictions-9-billion-mutation-human-genome/", source: Fortune, date: "2026-09-08"}
- {id: 4, title: "AlphaGenome Atlas Maps 9 Billion Possible DNA Variants", url: "https://spectrum.ieee.org/alphagenome-atlas", source: IEEE Spectrum, date: "2026-09-08"}
- {id: 5, title: "New Google DeepMind atlas could transform our understanding of genetic diseases", url: "https://www.scientificamerican.com/article/new-google-deepmind-alphagenome-atlas-could-transform-our-understanding-of-genetic-diseases/", source: Scientific American, date: "2026-09-08"}
- {id: 6, title: "DeepMind's new genome 'atlas' charts effects of all 9 billion human gene mutations", url: "https://www.nature.com/articles/d41586-026-02835-4", source: Nature news, date: "2026-09-08"}
- {id: 7, title: "AVI.pm — Ensembl VEP plugin for AlphaGenome Variant Impact scores", url: "https://github.com/Ensembl/VEP_plugins/blob/release/116/AVI.pm", source: Ensembl / EMBL-EBI, date: "2026-09-08"}
- {id: 8, title: "google-deepmind/alphagenome", url: "https://github.com/google-deepmind/alphagenome", source: GitHub, date: "2026-09-09"}
- {id: 9, title: "AlphaGenome documentation — FAQs and terms", url: "https://www.alphagenomedocs.com/faqs.html", source: Google DeepMind, date: "2026-09-09"}
- {id: 10, title: "gnomAD v4.0 release announcement", url: "https://groups.google.com/g/exac_data_announcements/c/cdz1BNHe01w", source: gnomAD / Broad Institute, date: "2023-11-02"}
- {id: 11, title: "CADD downloads — all possible SNVs of GRCh38", url: "https://cadd.gs.washington.edu/download", source: University of Washington, date: "2026-09-09"}
- {id: 12, title: "CADD documentation — score interpretation and thresholds", url: "https://cadd.bihealth.org/info", source: CADD / BIH, date: "2023-11-01"}
- {id: 13, title: "CADD v1.7: using protein language models, regulatory CNNs and other nucleotide-level scores", url: "https://academic.oup.com/nar/article/52/D1/D1143/7511313", source: Nucleic Acids Research, date: "2024-01-05"}
- {id: 14, title: "Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC9748256/", source: "Pejaver et al., American Journal of Human Genetics", date: "2022-12-01"}
- {id: 15, title: "ClinGen SVI calibration of newer computational predictors including AlphaMissense", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11429929/", source: "Bergquist et al.", date: "2025-03-10"}
- {id: 16, title: "Using the ACMG/AMP framework to capture evidence related to predicted and observed impact on splicing", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10357475/", source: "Walker et al., American Journal of Human Genetics", date: "2023-07-06"}
- {id: 17, title: "Standards and guidelines for the interpretation of sequence variants (ACMG/AMP)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC4544753/", source: "Richards et al., Genetics in Medicine", date: "2015-05-01"}
- {id: 18, title: "Benchmarking of deep neural networks for predicting personal gene expression from DNA sequence highlights shortcomings", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10055057/", source: "Sasse et al.", date: "2023-03-16"}
- {id: 19, title: "Personal transcriptome variation is poorly explained by current genomic deep learning models", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10703684/", source: "Huang et al., Nature Genetics", date: "2023-11-30"}
- {id: 20, title: "Current sequence-based models capture gene expression determinants in promoters but mostly ignore distal enhancers", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10045630/", source: "Karollus, Mauermeier, Gagneur, Genome Biology", date: "2023-03-27"}
- {id: 21, title: "Independent evaluation of AlphaGenome on personal genome expression prediction", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC12440111/", source: "Shen (preprint)", date: "2025-09-09"}
- {id: 22, title: "Multi-ancestry evaluation of sequence-to-function scores against blood eQTLs", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC13320881/", source: "preprint", date: "2026-06-26"}
- {id: 23, title: "AlphaGenome: advancing regulatory variant effect prediction with a unified DNA sequence model (preprint)", url: "https://www.biorxiv.org/content/10.1101/2025.06.25.661532v1.full", source: bioRxiv, date: "2025-06-25"}
- {id: 24, title: "AlphaGenome (published version)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC12851941/", source: "Avsec et al., Nature 649:1206-1218", date: "2026-01-28"}
- {id: 25, title: "GPN-Star: Genomic Pretrained Network with Species Tree and Alignment Representations", url: "https://www.biorxiv.org/content/10.1101/2025.09.21.677619v1.full-text", source: bioRxiv, date: "2025-09-21"}
- {id: 26, title: "TraitGym: benchmarking causal-variant prediction for Mendelian and complex traits", url: "https://www.biorxiv.org/content/10.1101/2025.02.11.637758v2.full", source: bioRxiv, date: "2025-02-11"}
- {id: 27, title: "The GTEx Consortium atlas of genetic regulatory effects across human tissues", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7737656/", source: Science, date: "2020-09-11"}
- {id: 28, title: "ENCODE Project common cell types", url: "https://www.genome.gov/encode-project-common-cell-types", source: NHGRI, date: "2026-09-09"}
- {id: 29, title: "Evaluation of GRCh38 and de novo haploid genome assemblies", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5411779/", source: Genome Research, date: "2017-05-01"}
- {id: 30, title: "A draft human pangenome reference", url: "https://www.nature.com/articles/s41586-023-05896-x", source: Nature, date: "2023-05-10"}
- {id: 31, title: "UK Biobank — our participants", url: "https://www.ukbiobank.ac.uk/about-our-data/our-participants/", source: UK Biobank, date: "2026-09-09"}
- {id: 32, title: "Evolutionary constraint and disease variants across 240 mammalian genomes (Zoonomia)", url: "https://www.science.org/doi/10.1126/science.abn3943", source: Science, date: "2023-04-28"}
- {id: 33, title: "ClinVar classification counts via NCBI Entrez", url: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=%22clinsig+vus%22%5BProperties%5D&retmode=json", source: NCBI ClinVar, date: "2026-09-08"}
- {id: 34, title: "Prevalence of variant reclassification following hereditary cancer genetic testing", url: "https://jamanetwork.com/journals/jama/fullarticle/2703350", source: "Mersch et al., JAMA", date: "2018-09-25"}
- {id: 35, title: "Genetic misdiagnoses and the potential for health disparities", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5292722/", source: "Manrai et al., New England Journal of Medicine", date: "2016-08-18"}
- {id: 36, title: "Gaps in incorporating germline genetic testing into treatment decision-making for early-stage breast cancer", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5501363", source: "Kurian et al., Journal of Clinical Oncology", date: "2017-04-12"}
- {id: 37, title: "100,000 Genomes Pilot on Rare-Disease Diagnosis in Health Care", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7613219/", source: New England Journal of Medicine, date: "2021-11-11"}
- {id: 38, title: "De novo deep-intronic and non-canonical splicing variants in the 100,000 Genomes Project", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC9327385/", source: PMC, date: "2022-07-26"}
- {id: 39, title: "The GREGoR Consortium data model and cohort", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC13228420/", source: PMC, date: "2025-01-01"}
- {id: 40, title: "Whole-genome sequencing analysis of rare non-coding variation in UK Biobank", url: "https://www.nature.com/articles/s41588-025-02095-4", source: Nature Genetics, date: "2025-02-24"}
- {id: 41, title: "Accurate proteome-wide missense variant effect prediction with AlphaMissense", url: "https://www.science.org/doi/10.1126/science.adg7492", source: Science, date: "2023-09-19"}
- {id: 42, title: "AlphaFold Protein Structure Database licence and disclaimer", url: "https://alphafold.ebi.ac.uk/assets/License-Disclaimer.pdf", source: EMBL-EBI / Google DeepMind, date: "2026-09-09"}
- {id: 43, title: "arcinstitute/evo2_40b model card", url: "https://huggingface.co/arcinstitute/evo2_40b", source: "Arc Institute / NVIDIA", date: "2025-02-19"}
- {id: 44, title: "ClinGen FDA recognition", url: "https://clinicalgenome.org/about/fda-recognition/", source: ClinGen, date: "2018-12-01"}
- {id: 45, title: "Inequity in genomic variant interpretation across ancestry groups", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6785397/", source: "Ndugga-Kabuye & Issaka, Familial Cancer", date: "2019-10-01"}
- {id: 46, title: "Disparities in variants of uncertain significance among 493,515 probands", url: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12085080/", source: "Castillo et al., JCO Precision Oncology", date: "2024-07-01"}
- {id: 47, title: "CAGI5 regulation saturation challenge assessment", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6834773/", source: PMC, date: "2019-10-31"}
- {id: 48, title: "Expert reaction to paper on Google DeepMind's AlphaGenome", url: "https://www.sciencemediacentre.org/expert-reaction-to-paper-on-google-deepminds-alphagenome/", source: Science Media Centre, date: "2026-01-28"}
- {id: 49, title: "Effective gene expression prediction from sequence by integrating long-range interactions (Enformer)", url: "https://www.nature.com/articles/s41592-021-01252-x", source: Nature Methods, date: "2021-10-04"}
- {id: 50, title: "CASP14 final z-scores, all groups", url: "https://predictioncenter.org/casp14/zscores_final.cgi", source: Protein Structure Prediction Center, date: "2020-12-01"}
- {id: 51, title: "Can AlphaFold2 predict the impact of missense mutations on structure?", url: "https://www.nature.com/articles/s41594-021-00714-2", source: "Buel & Walters, Nature Structural & Molecular Biology", date: "2022-01-01"}
- {id: 52, title: "Using AlphaFold to predict the impact of single mutations on protein stability and function", url: "https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0282689", source: "Pak et al., PLOS ONE", date: "2023-03-16"}
- {id: 53, title: "Estimating cumulative point prevalence of rare diseases", url: "https://www.nature.com/articles/s41431-019-0508-0", source: European Journal of Human Genetics, date: "2019-09-16"}
- {id: 54, title: "Time to diagnosis in rare disease: a survey across 41 European countries", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11369105/", source: PMC, date: "2024-08-31"}
- {id: 55, title: "Region-specific thresholds for non-coding variant prioritisation in whole genomes", url: "https://academic.oup.com/nargab/article/7/4/lqaf157/8328387", source: NAR Genomics and Bioinformatics, date: "2025-11-19"}
- {id: 56, title: "Clinical Decision Support Software — FDA guidance (reissued 2026-01-29)", url: "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software", source: U.S. Food and Drug Administration, date: "2026-01-29"}
- {id: 57, title: "False-positive results released by direct-to-consumer genetic tests", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6301953/", source: "Tandy-Connor et al., Genetics in Medicine", date: "2018-03-22"}
- {id: 58, title: "ClinGen Sequence Variant Interpretation Working Group (retired April 2025)", url: "https://clinicalgenome.org/working-groups/sequence-variant-interpretation/", source: ClinGen, date: "2026-09-09"}
- {id: 59, title: "MaveDB: a repository for multiplexed assays of variant effect", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11753097/", source: PMC, date: "2025-01-21"}
- {id: 60, title: "CAGI, the Critical Assessment of Genome Interpretation: a decade of blind challenges", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10882881/", source: PMC, date: "2024-02-21"}
- {id: 61, title: "Accurate classification of BRCA1 variants with saturation genome editing", url: "https://www.biorxiv.org/content/10.1101/294520v1", source: "Findlay et al.", date: "2018-09-12"}
- {id: 62, title: "Court vacates FDA's laboratory-developed tests final rule (ACLA v. FDA)", url: "https://www.congress.gov/crs-product/LSB11312", source: Congressional Research Service, date: "2025-03-31"}
- {id: 63, title: "ClinVar molecular-consequence counts via NCBI Entrez", url: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=%22intron+variant%22%5BMolecular+consequence%5D&retmode=json", source: NCBI ClinVar, date: "2026-09-08"}
- {id: 64, title: "A global reference for human genetic variation (1000 Genomes Project phase 3)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC4750478/", source: Nature, date: "2015-10-01"}
- {id: 65, title: "Assessing the applicability of the ClinGen SVI PP3/BP4 recommendations in a rare disease cohort", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11560577/", source: "Stenton et al., Genetics in Medicine", date: "2024-07-01"}
:::
