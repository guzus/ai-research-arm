---
eyebrow: AUDIT · AI MATHEMATICS
title: "OpenAI's 722 manuscripts: the sub-n log n multiplication claim is real, unchecked mathematics — and the Lean badge covers less than it looks"
deck: "A multitape Turing machine that beats n log n by a factor of (lg n) to the power 2⁻¹⁸² would refute a 55-year-old conjecture. It has no Lean proof, no referee and no named author. Neither has most of the release."
domain: general
lede: |
  On 6 October 2026 OpenAI put 722 mathematics manuscripts, grouped into 372 "families", on GitHub under an Apache-2.0 licence and attributed them to an internal model it has not released. The single most provocative file claims to multiply two n-bit integers faster than n log n on a multitape Turing machine. If that holds, it refutes the lower half of the conjecture Schönhage and Strassen stated in 1971. This audit reads that manuscript's LaTeX source, the release's Lean catalogue and the advisory group's guidelines. The verdict is narrower than both the hype and the backlash. The multiplication paper is a serious, internally coherent claim in exactly the model where the conjecture lives. It contradicts no proven theorem, and it has not been machine-checked at all. Across the release, OpenAI's own Lean manifest calls its coverage "Partial progress" and its review status "unchecked".
stats:
  - {label: Manuscripts, value: "722", note: "in 372 families"}
  - {label: Problems posed, value: "~4,000", note: "OpenAI-chosen pool"}
  - {label: Lean catalogue, value: "162", note: "papers with a formalized main result"}
  - {label: Claimed saving, value: "κ = 2⁻¹⁸²", note: "O(n(lg n)^(1−κ))"}
---

:::callout(kind=info, label="Short answer")
- **The multiplication claim:** a deterministic algorithm for one fixed multitape Turing machine, running in O(n(lg n)^(1−κ)) with κ = 2⁻¹⁸², for every input length. It is the model in which Harvey and van der Hoeven proved O(n log n) in 2019 [^2,3,18].
- **Does it break a theorem?** No. An Ω(n log n) lower bound is proved only for *on-line* multitape machines. For Boolean circuits and for general off-line Turing machines the known Ω(n log n) bounds are conditional [^23,24,25].
- **Is it Lean-verified?** No. The integer-multiplication family (109) has no Lean documentation page and is not in `formalization.yaml` [^9,15].
- **Release-wide Lean coverage:** 162 papers and 185 declarations out of 722 manuscripts, with the manifest marked "unchecked" [^9].
- **What is actually new:** a large catalogue of *claims*, published with partial machine certificates and a revision policy. It is not yet a body of accepted theorems, and the advisory group whose guidance shaped it explicitly declined to endorse the process [^1,33].
:::

## 01. What was actually released

The release is a catalogue of claims with uneven supporting evidence. It is not a set of 722 independent theorems. OpenAI's README says "the current catalogue contains 722 manuscripts organized into 372 families". A family "groups related papers, which may include a principal result, companion arguments, consequences, or alternative proofs" [^1]. The same README says the model "was posed approximately 4,000 problems", and that results were kept only if they met "an appropriate level of significance" [^1]. On average each result used "three hours of ChatGPT Pro thinking compute" with the unreleased model [^1].

:::kv
- {term: Licence, def: "Apache-2.0 [^1]"}
- {term: Repository history, def: "One commit on main at release; no external pull requests [^1]"}
- {term: Reasoning summaries, def: "10 abridged summaries, one each for families 007, 017, 087, 102, 159, 197, 221, 271, 287 and 362 [^1,17]"}
- {term: Process exceptions, def: "Zeta zero-free region and Hodge for CM abelian varieties; the Re(s) > 11/12 writeup was 'human edited for readability' [^1]"}
- {term: Production window, def: "Manuscript folders dated from 10 September to early October 2026 [^16]"}
- {term: Model, def: "Unnamed 'internal OpenAI model', not publicly available [^1,31]"}
:::

The family unit matters because the headline count inflates the number of independent ideas. In the part of `CONTENTS.md` that could be read (families 001–056), one family, 034 on log abundance, holds 14 manuscripts, and families 014 and 032 hold 8 each [^16]. Family numbers also skip: no family 045, 061 or 070 appears in `overview.tex` [^15]. So "372 results", the unit Scientific American used [^31], is closer to the truth than "722 papers". Even 372 overstates independence, because some families are variants of each other.

The families by discipline below come from a third-party count. ARA checked four sections against `overview.tex` (number theory 31, algebraic and complex geometry 36, analysis 16, convex geometry 15). The other thirteen rest on the third party's tally, as of 2026-10-07 [^38,15].

:::rank-list
- {label: Theoretical computer science, value: "40", pct: 100, highlight: true}
- {label: Combinatorics, value: "37", pct: 93}
- {label: Algebraic & complex geometry, value: "36", pct: 90}
- {label: Number theory, value: "31", pct: 78}
- {label: Probability & statistical mechanics, value: "29", pct: 73}
- {label: Differential geometry, value: "29", pct: 73}
- {label: Mathematical physics, value: "25", pct: 63}
- {label: "Other 10 disciplines (operator algebras … logic)", value: "145", pct: 100}
:::

**Counterpoint.** The denominator flatters nobody in particular, because nobody outside OpenAI knows it. The ~4,000 problems were assembled by OpenAI after its "existing mathematical evaluations saturated" [^1]. No per-problem outcome table and no failure count are published [^1,38]. A 9.3% family-to-problem ratio (372/4,000) is therefore not a solve rate.

**Why it matters.** Every downstream question — novelty, correctness, credit — has to be asked family by family. The release's own structure says so.

## 02. The multiplication manuscript, read exactly

The integer-multiplication paper is not a trick of the model of computation. It states its claim in precisely the setting where the n log n conjecture is open. Its abstract describes "a deterministic algorithm that multiplies two n-bit integers in O(n(lg n)^(1−κ)) worst-case time, with κ = 2⁻¹⁸²" [^2]. It runs on "one fixed finite-alphabet Turing machine with a fixed finite number of one-dimensional tapes", and the paper claims to refute "the n log n optimality conjecture of Schönhage and Strassen in this model" [^2,3]. The author line reads simply "OpenAI", dated 23 September 2026 [^2]. The catalogue lists it as family 109, "Integer multiplication below n log n" [^15].

:::kv
- {term: Bound, def: "O(n(lg n)^(1−κ)), κ = 2⁻¹⁸², worst case, every n ≥ 1 [^2,3]"}
- {term: Model, def: "Fixed multitape Turing machine; 'No random-access simulation is used' [^2,53]"}
- {term: Hypotheses, def: "None stated; uses the unconditional O(n log n) multiplier as an ordinary subroutine [^3]"}
- {term: Pipeline, def: "CRT onto prime cyclic axes, Harvey–van der Hoeven Gaussian resampling, Bluestein, Nussbaumer–Quandalle transforms [^3,6]"}
- {term: Corollaries, def: "k×k bit-matrix transposition, exact division and integer square root at the same bound [^7,53]"}
- {term: Structure, def: "Introduction, section files 02–10 and an appendix [^2]"}
:::

The paper disposes of the obvious objection itself. Its history section cites Schönhage's 1980 linear-time multiplication on storage-modification machines, and a sub-logarithmic saving on a unit-cost RAM with excluded preprocessing. It says neither establishes the bound "in the fixed finite-tape model" [^4]. That is accurate. Schönhage's pointer machines do multiply in O(n) [^26], and on a log-RAM the original Schönhage–Strassen algorithm already runs in O(n) word operations [^27]. Those results are why "n log n is the speed limit" is false as a model-free statement. They do not touch the multitape setting [^18].

### Where the saving comes from

The mechanism is the step a referee must break. The multiplication arithmetic stays at the Harvey–van der Hoeven level, and the paper instead saves on *data movement*. Address-field interchange and Fourier butterfly layers are performed by fixed linear networks that "form XOR combinations of intermediate data, even though its final effect is a permutation" [^4]. This "lies outside models restricted to moving data without such computations" [^4]. In the swap section, a network with W wires implements an m-dimensional address shear using edge matrices of total rank s. Each unit of rank costs one recursive call on a V/W volume, so the recursion is F_k ≤ (s/W)F_{k−1} + O(1) [^5]. The introduction says the strict inequality s < Wm "is the source of the power saving" [^3]. κ is a bookkeeping residue, not a natural exponent. The assembly section takes the smallest margin in its cost table, 2⁻¹⁸¹, and keeps half: "Thus min_i g_i = 2⁻¹⁸¹ = 2κ" [^6].

:::quote(attr="Abstract, 'Integer multiplication below n log n', OpenAI, 23 September 2026")
The algorithm is exact for every input length … refuting the n log n optimality conjecture of Schönhage and Strassen in this model.
:::

### How small is 2⁻¹⁸²?

Asymptotically it is a genuine power-of-log saving, larger than any log* or log log improvement. Hacker News commenter keeganryan noted it "would traditionally be hidden as n lg n ^ (1 - eps) for some eps > 0" [^29]. Numerically it is unimaginably small. The speed-up factor over n log n is (lg n)^κ, which reaches 2 only when lg n = 2^(2^182). Even for an integer with 2^(2^64) bits, the gain is a factor of roughly 1 + 10⁻⁵³ (ARA arithmetic). The paper concedes that "the constants and thresholds in the construction are extremely large" [^3]. For comparison, Harvey and van der Hoeven's O(n log n) algorithm has a threshold of 2^(1729¹²) bits [^19]. Production libraries such as GMP still use Toom variants and a Fermat-style Schönhage–Strassen FFT [^28].

**Counterpoint.** "Galactic" is not a criticism of a lower-bound refutation. A conjecture that says *no* algorithm beats n log n is refuted by any algorithm, however impractical. Harvey himself wrote in 2019 that he "would be very surprised if the conjecture turned out to be wrong" [^20].

**Why it matters.** If correct, this is the most consequential complexity-theory claim in the release. Its truth turns on one finite gadget with a relative rank deficit of about 10⁻¹¹ [^52].

## 03. Does it contradict anything proven? No — and the reason is instructive

The claim refutes a conjecture, not a theorem. The lower-bound landscape is thinner than the folklore suggests. The 1971 conjecture had two halves. Harvey and van der Hoeven settled the upper half in *Annals of Mathematics* in 2021: O(n log n) bit operations on a multitape Turing machine [^18]. The lower half has only conditional support in general models.

| Model | Best known lower bound for n-bit multiplication | Status | Conflicts with OpenAI claim? |
|---|---|---|---|
| On-line multitape TM | Ω(n log n) mean time (Paterson–Fischer–Meyer 1974) [^25] | Proven | No: the new algorithm is off-line |
| Constant-degree Boolean circuits | Ω(n lg n) if the network coding conjecture holds [^23] | Conditional | Not directly: TM-to-circuit simulation adds a log factor |
| *Off-line multitape TM | Ω(n log n) if bit-matrix transposition needs Ω(n² log n) (2025) [^24] | Conditional | Implies transposition is also below n² log n, and the paper claims exactly that [^7] |
| Storage-modification (pointer) machine | O(n) upper bound already known [^26] | Faster than n log n since 1980 | No |
| Word RAM, log n-bit words | O(n) word operations [^27] | Faster since the 1970s analyses | No |

The off-line multitape row is the one that matters. In 2025 Harvey and van der Hoeven proved that "if matrix transposition is as hard as expected, then integer multiplication is also as hard as expected" [^24]. Their paper also observes that "virtually no non-trivial (i.e. superlinear) lower bounds are known for basic computational tasks such as transposition" [^24]. OpenAI's manuscript uses their reduction in the forward direction to claim O(k²(lg k)^(1−κ)) transposition [^7]. So the two surprises stand or fall together. That makes the transposition corollary the cleanest place to look for an error.

:::timeline
- {date: 1962, headline: "Karatsuba", body: "O(n^1.585) — the first sub-quadratic method."}
- {date: 1971, headline: "Schönhage–Strassen", body: "O(n log n log log n), plus the conjecture that n log n is optimal."}
- {date: 2007, headline: "Fürer", body: "n log n · 2^O(log* n)."}
- {date: 2014, headline: "Harvey–van der Hoeven–Lecerf", body: "Explicit constant: O(n log n · 8^(log* n)) unconditionally."}
- {date: 2018, headline: "Harvey–van der Hoeven", body: "Unconditional O(n log n · 4^(log* n))."}
- {date: 2019, headline: "O(n log n)", body: "Harvey–van der Hoeven; published in Annals of Mathematics 2021."}
- {date: 2025, headline: "Transposition reduction", body: "Multiplication is at least as hard as bit-matrix transposition."}
- {date: 2026-09-23, headline: "OpenAI manuscript", body: "Claims O(n(lg n)^(1−2⁻¹⁸²)). Unreviewed, no Lean."}
:::

The 2014 and 2018 rows are documented in the arXiv preprints [^21,22]. The 2019 result is the Annals paper [^18], and the 2025 reduction is arXiv 2503.22848 [^24].

### The network-coding subtlety

One loose end deserves precision. Afshani, Freksen, Kamma and Larsen showed in 2019 that, if a central network-coding conjecture holds, "any constant degree boolean circuit for multiplication must have size Ω(n lg n)" [^23]. It is tempting to read the OpenAI result as refuting that conjecture. As stated, it does not. The standard simulation of a time-T Turing machine by circuits costs O(T log T), which turns n(lg n)^(1−κ) into roughly n(lg n)^(2−κ), still above n lg n (ARA analysis). The tension reappears only if the machine is *oblivious*, meaning its head movements do not depend on the data. Then a near-linear circuit simulation is available, and a network-coding gain inside a fixed gadget is exactly what the conjecture forbids in the undirected setting. In the sections ARA read, the manuscript never states whether its machine is oblivious, and its history section does not mention the network-coding lower bound [^4]. Whether it is oblivious is an inference a referee would have to check, not something the paper says.

**Counterpoint.** No contradiction is not the same as plausibility. Most complexity theorists, Harvey included, expected n log n to be tight [^20]. A refutation by a 2⁻¹⁸² margin through an XOR-based permutation gadget is the kind of result that tends to hide a counting error.

**Why it matters.** The claim is falsifiable in a precise place. That makes it more useful to the field than a vague "breakthrough", and more dangerous to repeat before anyone has checked it.

## 04. Where a referee would look first

The manuscript is internally consistent at the level of its stated arithmetic. Its correctness reduces to a handful of hand-proved finite facts that nobody outside OpenAI has checked. The swap gadget works over two fields at once: data passes through pointwise XOR over 𝔽₂, while addresses move by rational shears over ℤ/q^b. The rank budget comes from Alon-type intersection-parity set systems, and the history section credits index-coding ideas [^52,4]. The deficit that buys the whole saving is tiny, about 1.5 × 10⁻¹¹ in relative terms, so a single sign or rank error anywhere erases it [^52].

:::callout(kind=warn, label=Unverified)
No Lean formalization exists for family 109. `lean/docs/109.md` returns 404, and no entry in `formalization.yaml` covers integer multiplication [^9,15]. The closest formal artifact is a manifest entry titled "Finite tensor savings and exact Fourier circuits", about circuits for the exact DFT, which is a different model [^9].
:::

Three checks would settle most of the risk:

1. **Field mismatch.** The rank of the gadget is computed over ℚ from projections, but the interchanges are executed mod q^b. A referee must confirm that every denominator in the rational factorization is invertible mod q^b, and that the counted rank equals the number of interchanges actually performed [^5].
2. **Transposition.** Sub-n²log n transposition of a bit matrix on a multitape machine is a strong, separately testable consequence [^7,24].
3. **Obliviousness.** If the tape schedule is data-independent, the result would bear on the network-coding conjecture. The paper should say so [^4,23].

The companion paper is often confused with the main one. "An explicit power saving for the exact discrete Fourier transform", dated 25 September, claims O(n(log n)^(1−10⁻¹³)) operations in an algebraic model with "unit-cost logarithmic-size indexing" [^8]. Because indexing is unit-cost there, the DFT claim lives in a RAM-like model rather than on tapes, so the two papers should be judged separately [^8].

Public scrutiny so far is thin. The Hacker News thread had 91 points and 62 comments when fetched on 7 October [^29]. Commenters joked about the exponent ("2^-182 is very funny but it's bigger than 0") and asked "Is there an associated machine-checked proof of this?" [^29]. Nobody reported an error. An X post by @AcerFur on 6 October read: "oh yeah btw guys we can do integer multiplication faster than n log n lol" [^43]. ARA found no complexity-theory blog analysis of the paper by 7 October, and Gil Kalai's next-day post addressed the release only in general [^35].

**Counterpoint.** Silence is not evidence of error, and one day is too short for a referee report. Harvey and van der Hoeven's own 2019 preprint went from posting to Annals acceptance on a timescale of months [^18].

**Why it matters.** A falsifiable claim with a named weak point can be checked cheaply by a specialist. That is the strongest argument for publishing it, even unrefereed.

## 05. The Lean badge: what it covers and what it doesn't

Lean coverage is real, partial and self-described as unreviewed. Reporting has blurred all three. OpenAI's README says "Many, but not all, of the manuscripts have been formalized" and "Some of the unformalized results could have issues" [^1]. The machine-readable manifest is blunter: `scope: "Partial progress."`, `review: status: unchecked`, `automation: method: agent` [^9]. It lists 162 source papers and 185 main-result declarations, on toolchain `leanprover/lean4:v4.34.1` [^9,14].

:::stack-bar(legend=true)
- {label: "Manuscripts with a catalogued formalized main result (162)", pct: 22}
- {label: "Manuscripts with no catalogue entry (560)", pct: 78}
:::

The secondary figure that circulated, "235 of the 372 result families link to a Lean formalization page, and 162 papers have a fully formalized main result", comes from Tech Insider relaying a FourWeekMBA count [^37]. It mixes units: 235 counts *families* with a documentation page, while 162 counts *papers* in the manifest. And "fully" is contradicted by the manifest's own "Partial progress" [^9]. Kingy.ai's careful version calls its count "not a measured proof-pass percentage" [^38]. ARA's own reading of the 54 families numbered 001–055 in `CONTENTS.md` (there is no 045) found Lean links on 22 (41%), well below the 63% that 235/372 implies [^16]. Either Lean coverage is denser later in the catalogue, or the 235 count is generous.

### What a certificate actually certifies

Each formal claim is checked by Comparator, the Lean FRO's judge. It builds a trusted *challenge* module and a *solution* module, then verifies that the theorem statements match, that only permitted axioms are used, and that the kernel accepts the proof [^13]. OpenAI's configurations permit only Lean's three standard axioms (`propext`, `Quot.sound`, `Classical.choice`) and list no definition holes [^50]. That is good practice. But Comparator proves that a solution matches the challenge, not that the challenge matches the paper. Its own README warns that "many definition hole challenges can be gamed without additional oversight" [^13]. The fidelity burden sits in each challenge file's definitions. The Unique Games challenge, for example, defines its own encodings of 3SAT and translation games on top of Mathlib's polynomial-time Turing machine notion [^50,12].

| Headline claim (family) | Lean doc page | Comparator target | Note |
|---|---|---|---|
| Zero-free half-plane for ζ and Dirichlet L (003) | Yes [^10] | Re(s) > 7/8 via Mathlib's `riemannZeta` [^51] | The 11/12 writeup OpenAI highlighted is a human-edited companion; its proof is not the one checked [^1,10] |
| ω ≤ 9/4 over ℂ (107) | Yes [^11] | Yes | Arithmetic, not bit, complexity [^11] |
| Unique Games Conjecture (102) | Yes [^12] | Yes | About 30 trusted definitions in the challenge file [^50] |
| Integer multiplication below n log n (109) | No (404) [^15] | None [^9] | Manuscript only |
| L = RL = BPL (103) | No (404) [^15] | None [^9] | Manuscript only |
| Rational Hodge for CM abelian varieties (032) | No [^16] | None | Process exception; one companion is explicitly conditional [^1,16] |

:::callout(kind=warn, label="Two different statuses")
"Lean-checked" means a kernel accepted a proof of the *formal statement*. "Mathematically accepted" means humans agree that the statement says what the paper claims, that it is new, and that credit is right. The August 2026 human audit of OpenAI's earlier Astra results made the same point: "a formalization can encode the wrong proposition" [^40].
:::

**Counterpoint.** Where certificates exist, they are much stronger than a press release. The zeta statement uses Mathlib's own `riemannZeta` and introduces no new definitions, so there is little room for a definitional trick [^51]. If the Comparator run for family 003 reproduces, that one result is close to certain, and historic.

**Why it matters.** Readers should treat "has Lean" as a per-family property to be checked against the specific declaration. It is not a release-wide guarantee.

## 06. What is actually new — and what was inflated

Separating OpenAI's claims from commentators' amplifications shrinks the "solved famous problems" story. It leaves a still-extraordinary residue that is mostly unverified. The overview lists, among others: "Proves Khot's Unique Games Conjecture" (102), "Proves L = RL = BPL" (103), and ω ≤ 9/4 over ℂ (107) [^15]. Number theory family 003 claims every Dirichlet L-function, ζ included, "is zero-free in Re s > 7/8", with a companion giving "a different proof of the zero-free half-plane Re s > 11/12" [^16,10]. Classical zero-free regions shrink toward the line Re s = 1, and no zero-free half-plane to its left has ever been established. That is why Latent Space built its headline around this family [^39].

The matrix-multiplication claim shows the scale of the jumps being asserted:

:::bars
- {label: "Naive algorithm", value: "ω = 3", pct: 100}
- {label: "Published record before release", value: "≈ 2.3712–2.3713", pct: 37}
- {label: "OpenAI 107: over any field", value: "< 2.371055", pct: 37}
- {label: "OpenAI 107: the paper's weaker headline bound", value: "< 2.258", pct: 26}
- {label: "OpenAI 107: over ℂ", value: "≤ 2.25", pct: 25}
- {label: "Trivial lower bound", value: "ω ≥ 2", pct: 0}
:::

Bar fill is (ω − 2) on a 0–1 scale. OpenAI's bounds are from `lean/docs/107.md` [^11]. The prior record is from Alman, Duan, Vassilevska Williams, Xu, Xu and Zhou, whose paper reports ω below 2.3714 in its revisions [^46]. Since Coppersmith–Winograd's 2.376 in 1990, published improvements have totalled roughly 0.005, so a drop to 2.25 would be a discontinuity, not a step (ARA arithmetic).

Commentary then went further than the files. Latent Space's AINews headline said the release solved "90 of the top 500 open math problems". No source for the 90 is visible, and the post itself says the results "have not been independently verified" [^39]. A KuCoin flash item claimed the Riemann Hypothesis itself had been proven [^45]. Startup Fortune said every result carried a machine-checkable proof [^49]. That contradicts OpenAI's own README [^1].

**What is genuinely new, independent of correctness:** (1) the scale, about 37 times the ten-result Astra release of 1 August when counted in families (372 vs 10) [^48,1]; (2) publication of certificates alongside unchecked prose, with a versioning promise that "corrections and revisions will be recorded as new versions" [^1]; and (3) a declared denominator of roughly 4,000 problems, which earlier releases lacked [^1].

:::slope(left-label="Astra, 2026-08-01", right-label="openai/math, 2026-10-06", unit="")
| Measure | Astra | openai/math |
|---|---|---|
| Claimed results (families) | 10 | 372 |
| Results with a Lean certificate | 10 | 162 |
:::

The Astra figures (ten results, each with a Lean formalization) are from Kingy.ai's evidence review [^48]. The openai/math figures are from the README and manifest [^1,9]. The slope makes the trade explicit: coverage per result collapsed even as the count of results exploded.

**Counterpoint.** Prior AI-math releases have had novelty problems that only surfaced later. In October 2025 GPT-5's "solved" Erdős problems turned out to be literature lookups, which Thomas Bloom called "a dramatic misrepresentation" [^41]. Specialists disputed the novelty and attribution of some Astra results [^48]. No 722-specific duplicate had been identified by 7 October, but the release describes no prior-art check [^1].

**Why it matters.** The honest unit of novelty is "claims that survive review". That number is currently unknown for every family without a Comparator run.

## 07. How the results were produced, and what the denominator hides

The process disclosure is better than OpenAI's past practice and worse than its advisers asked for. A spokesperson told Scientific American the model "produced almost every one of the results in response to a single prompt handed to a single AI agent", while conceding "some results might have taken multiple attempts" [^31]. The README says only that "the vast majority of results were obtained with the same procedure" [^1]. The contrast with September's Navier–Stokes claim is large: that run used roughly 10,000 concurrent agents for about 88 hours [^42].

:::timeline
- {date: 2025-10-19, headline: "Erdős episode", body: "GPT-5 'solutions' turn out to be literature finds; Hassabis calls it 'embarrassing'."}
- {date: 2026-08-01, headline: "Astra: ten results", body: "Ten claimed advances, each with a Lean formalization."}
- {date: 2026-09-08, headline: "Navier–Stokes claim", body: "About 10,000 agents for 88 hours."}
- {date: 2026-09-29, headline: "AGMAI guidelines", body: "Nine mathematicians; more than 600 survey responses."}
- {date: 2026-10-06, headline: "openai/math", body: "722 manuscripts released at 22:00 UTC; erdosproblems.com freezes proof claims the same day."}
:::

The sources for the timeline are TechCrunch [^41], Kingy.ai [^48], RuntimeWire [^42], AGMAI [^32], Scientific American [^31] and Thomas Bloom's site notice [^36].

The compute disclosure is an average over *kept* results. On a successful run, three hours of ChatGPT Pro thinking is a wall-clock figure on an unreleased model, with no token or dollar conversion [^1,38]. If the discarded problems also received about three hours each, total compute would be several times larger than the published per-result figure implies (ARA analysis). MIT's Andrew Sutherland put the methodological point bluntly: "treat any claims about one-shotting problems with a single agent as unverified … We should ask for receipts" [^31].

**Counterpoint.** Releasing the denominator at all is a real improvement on the 2025 Erdős episode [^41], and the README is candid that unformalized work "could have issues" [^1].

**Why it matters.** Without per-result prompts, attempts and failures, nobody can estimate the model's true hit rate, so the 722 cannot calibrate expectations for the model once it is released.

## 08. Governance: the guidance OpenAI cited, versus what it did

The release is better described as "partially aligned with" the advisory group's guidance than as "following" it. The Advisory Group on Mathematics and Artificial Intelligence (AGMAI), hosted at the Institute for Advanced Study, published guidelines on 29 September informed by more than 600 survey responses [^32]. On release day it issued a statement that its involvement "should not be interpreted as a judgment of the impact of these results or an endorsement of the process" [^33].

| AGMAI recommendation (29 Sep) | OpenAI release (6 Oct) | Verdict |
|---|---|---|
| Repository "should not be controlled by any AI lab" [^32] | github.com/openai; "exploring community-hosted repositories" [^1] | {flag:red} Not met |
| Publish "the name of the model, the prompts used" [^32] | Unnamed model; no prompts [^1,31] | {flag:red} Not met |
| A "(summarized) chain of thought" [^32] | 10 summaries for 372 families [^1] | {flag:yellow} Partial |
| Time taken and estimated cost per result [^32] | Average only [^1,31] | {flag:yellow} Partial |
| Report problems tried and failed [^32] | ~4,000 problems posed; no outcome table [^1] | {flag:yellow} Partial |
| Formalize as far as possible, or state status [^32] | Lean for 162 papers; manifest "unchecked" [^9] | {flag:yellow} Partial |
| Persistent versions and recorded changes [^32] | Versioning promise, on a lab-controlled host [^1] | {flag:green} Met in spirit |

OpenAI's spokesperson told Scientific American the company is "not bound by these recommendations" [^31]. The group's opening position was stronger still: "we ask them to stop testing advanced mathematical problems on proprietary models" [^32].

Reaction among mathematicians split along predictable lines. Daniel Litt argued for openness: "I see no reason why we should ask the company to keep them secret from us" [^31]. Terence Tao, posting the same day, warned that "solutions to open problems are now being harvested at large scale in an unsustainable fashion" [^34]. Gil Kalai called it "an amazing milestone for mathematics" but added that "the results will needs to be verified and digested by human mathematicians in the months to come" [^35]. Thomas Bloom froze new proof claims on erdosproblems.com that day, and removed its solved counts, because most comments had become "people announcing AI-generated proofs" [^36]. Bloom did not name OpenAI.

**Counterpoint.** AGMAI also called its talks with OpenAI "constructive" [^33]. Releasing under Apache-2.0, with certificates and a revision policy, is far closer to scholarly norms than a press release would be.

**Why it matters.** Verification labour is the scarce input. A release on an AI lab's own host, without prompts, asks the community to do that labour on the lab's terms.

## 09. What could break this audit

This audit's conclusions could fail in four specific ways.

- **The multiplication paper may simply be right.** In that case the "unverified" framing will look overly cautious, but it is still accurate as of 7 October. The test is a specialist reading of the swap and motif sections [^5]. Unconditional refutation would also give sub-n²log n bit-matrix transposition [^7,24].
- **Lean coverage may be higher than the manifest suggests.** The 235-family figure could be right if coverage is concentrated in later families [^37,16]. The manifest, though, is OpenAI's own and says "Partial progress" [^9].
- **Comparator runs could reproduce cleanly**, turning families 003, 102 and 107 into near-certain results [^10,11,12]. That would make the release historic regardless of the unformalized remainder. No independent run had been reported by 7 October.
- **The novelty problem may not recur.** The October 2025 Erdős episode and the Astra attribution disputes [^41,48] are priors, not findings about these 722.

**Red-team pass: 3/3 top claims unbroken.** An adversarial reviewer ran repeated contradiction searches against three claims: the manuscript's stated bound and model, the absence of any Lean formalization for family 109, and the manifest's 162/185 counts. It found no contradicting source for any of them. It did confirm the 2025 transposition paper's remark that, for full multitape machines, nothing beyond trivial linear lower bounds is known [^24]. A separate verifier pass flagged weaker sub-claims, mostly mis-pointed section citations and two unsourced anecdotes. Those were corrected or removed before publication.

:::references
- {id: 1, title: "openai/math — README", url: "https://github.com/openai/math", source: "OpenAI (GitHub)", date: "2026-10-06"}
- {id: 2, title: "Integer multiplication below n log n — main.tex", url: "https://raw.githubusercontent.com/openai/math/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/main.tex", source: "OpenAI", date: "2026-09-23"}
- {id: 3, title: "Integer multiplication below n log n — §00 Introduction", url: "https://raw.githubusercontent.com/openai/math/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/00-introduction.tex", source: "OpenAI", date: "2026-09-23"}
- {id: 4, title: "Integer multiplication below n log n — §01 History", url: "https://raw.githubusercontent.com/openai/math/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/01-history.tex", source: "OpenAI", date: "2026-09-23"}
- {id: 5, title: "Integer multiplication below n log n — §04 Swap", url: "https://raw.githubusercontent.com/openai/math/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/04-swap.tex", source: "OpenAI", date: "2026-09-23"}
- {id: 6, title: "Integer multiplication below n log n — §08 Assembly", url: "https://raw.githubusercontent.com/openai/math/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/08-assembly.tex", source: "OpenAI", date: "2026-09-23"}
- {id: 7, title: "Integer multiplication below n log n — §10 Transposition", url: "https://raw.githubusercontent.com/openai/math/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/10-transposition.tex", source: "OpenAI", date: "2026-09-23"}
- {id: 8, title: "An explicit power saving for the exact discrete Fourier transform — main.tex", url: "https://raw.githubusercontent.com/openai/math/main/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/main.tex", source: "OpenAI", date: "2026-09-25"}
- {id: 9, title: "lean/formalization.yaml", url: "https://raw.githubusercontent.com/openai/math/main/lean/formalization.yaml", source: "OpenAI", date: "2026-10-06"}
- {id: 10, title: "lean/docs/003.md — quasi-Riemann hypothesis scope", url: "https://raw.githubusercontent.com/openai/math/main/lean/docs/003.md", source: "OpenAI", date: "2026-10-06"}
- {id: 11, title: "lean/docs/107.md — matrix multiplication scope", url: "https://raw.githubusercontent.com/openai/math/main/lean/docs/107.md", source: "OpenAI", date: "2026-10-06"}
- {id: 12, title: "lean/docs/102.md — Unique Games scope", url: "https://raw.githubusercontent.com/openai/math/main/lean/docs/102.md", source: "OpenAI", date: "2026-10-06"}
- {id: 13, title: "Comparator: a trustworthy judge for Lean proofs", url: "https://github.com/leanprover/comparator", source: "Lean FRO (GitHub)"}
- {id: 14, title: "lean/lean-toolchain", url: "https://raw.githubusercontent.com/openai/math/main/lean/lean-toolchain", source: "OpenAI", date: "2026-10-06"}
- {id: 15, title: "overview.tex — family catalogue", url: "https://raw.githubusercontent.com/openai/math/main/overview.tex", source: "OpenAI", date: "2026-10-06"}
- {id: 16, title: "CONTENTS.md — manuscript map", url: "https://raw.githubusercontent.com/openai/math/main/CONTENTS.md", source: "OpenAI", date: "2026-10-06"}
- {id: 17, title: "reasoning_traces/", url: "https://github.com/openai/math/tree/main/reasoning_traces", source: "OpenAI", date: "2026-10-06"}
- {id: 18, title: "Harvey & van der Hoeven, Integer multiplication in time O(n log n)", url: "https://annals.math.princeton.edu/2021/193-2/p04", source: "Annals of Mathematics 193(2)", date: "2021-03-03"}
- {id: 19, title: "David Harvey — O(n log n) FAQ", url: "https://web.maths.unsw.edu.au/~davidharvey/research/nlogn/index.html", source: "UNSW", date: "2019-03-28"}
- {id: 20, title: "We've found a quicker way to multiply really big numbers", url: "https://theconversation.com/weve-found-a-quicker-way-to-multiply-really-big-numbers-114923", source: "The Conversation (David Harvey)", date: "2019-04-09"}
- {id: 21, title: "Harvey, van der Hoeven, Lecerf — Even faster integer multiplication", url: "https://arxiv.org/abs/1407.3360", source: arXiv, date: "2014-07-12"}
- {id: 22, title: "Harvey & van der Hoeven — Faster integer multiplication using short lattice vectors", url: "https://arxiv.org/abs/1802.07932", source: arXiv, date: "2018-02-22"}
- {id: 23, title: "Afshani, Freksen, Kamma, Larsen — Lower bounds for multiplication via network coding", url: "https://arxiv.org/abs/1902.10935", source: "arXiv / ICALP 2019", date: "2019-02-28"}
- {id: 24, title: "Harvey & van der Hoeven — Integer multiplication is at least as hard as matrix transposition", url: "https://arxiv.org/abs/2503.22848", source: "arXiv / FOCS 2025", date: "2025-03-28"}
- {id: 25, title: "Paterson, Fischer, Meyer — An improved overlap argument for on-line multiplication", url: "https://dspace.mit.edu/handle/1721.1/148869", source: "MIT DSpace", date: "1974-01-01"}
- {id: 26, title: "Arnold Schönhage — research topics (storage modification machines)", url: "https://pages.iai.uni-bonn.de/schoenhage_arnold/topics.html", source: "University of Bonn"}
- {id: 27, title: "Fürer — How fast can we multiply large integers on an actual computer?", url: "https://arxiv.org/abs/1402.1811", source: "arXiv / LATIN 2014", date: "2014-02-08"}
- {id: 28, title: "GMP manual — FFT Multiplication", url: "https://gmplib.org/manual/FFT-Multiplication", source: "GNU MP"}
- {id: 29, title: "HN: Integer multiplication below n log n", url: "https://news.ycombinator.com/item?id=49985524", source: "Hacker News", date: "2026-10-06"}
- {id: 30, title: "HN: Sharing AI progress in mathematics", url: "https://news.ycombinator.com/item?id=49984923", source: "Hacker News", date: "2026-10-06"}
- {id: 31, title: "OpenAI unleashes hundreds more math results upon a field already in shock", url: "https://www.scientificamerican.com/article/openai-unleashes-hundreds-more-math-results-upon-a-field-already-in-shock/", source: "Scientific American (Joseph Howlett)", date: "2026-10-06"}
- {id: 32, title: "AGMAI — Guidelines (29 September)", url: "https://agmai.org/general-sep29/", source: "AGMAI / IAS", date: "2026-09-29"}
- {id: 33, title: "AGMAI — Statement (6 October)", url: "https://agmai.org/statement-oct6/", source: "AGMAI / IAS", date: "2026-10-06"}
- {id: 34, title: "Terence Tao — thread on harvesting open problems", url: "https://mathstodon.xyz/@tao/117395268889583356", source: Mathstodon, date: "2026-10-06"}
- {id: 35, title: "Gil Kalai — Updates: Sharing AI progress on mathematics", url: "https://gilkalai.wordpress.com/2026/10/07/updates-sharing-ai-progress-on-mathematics-amazing-and-my-lecture-plans/", source: "Combinatorics and more", date: "2026-10-07"}
- {id: 36, title: "erdosproblems.com — Changes (blog:9)", url: "https://www.erdosproblems.com/forum/thread/blog:9", source: "Thomas Bloom", date: "2026-10-06"}
- {id: 37, title: "OpenAI releases 722 math manuscripts from secret model", url: "https://tech-insider.org/openai-722-math-manuscripts-unreleased-model-2026/", source: "Tech Insider", date: "2026-10-07"}
- {id: 38, title: "OpenAI math: 722 manuscripts, results, proofs, compute costs", url: "https://kingy.ai/blog/openai-math-722-manuscripts-results-proofs-compute-costs/", source: "Kingy.ai", date: "2026-10-06"}
- {id: 39, title: "[AINews] Quasi-Riemann-Hypothesis: OpenAI publishes 722 math papers", url: "https://www.latent.space/p/ainews-quasi-riemann-hypothesis-openai", source: "Latent Space", date: "2026-10-06"}
- {id: 40, title: "A Human Audit of OpenAI's AI-Generated Mathematical Proofs", url: "https://arxiv.org/abs/2608.14673", source: arXiv, date: "2026-09-09"}
- {id: 41, title: "OpenAI's 'embarrassing' math", url: "https://techcrunch.com/2025/10/19/openais-embarrassing-math/", source: TechCrunch, date: "2025-10-19"}
- {id: 42, title: "OpenAI's 10,000 AI agents and the Navier–Stokes proof", url: "https://runtimewire.com/article/openai-10000-ai-agents-navier-stokes-proof", source: RuntimeWire, date: "2026-09-08"}
- {id: 43, title: "@AcerFur on integer multiplication", url: "https://x.com/AcerFur/status/2107606747972309163", source: "X", date: "2026-10-06"}
- {id: 44, title: "Techmeme: OpenAI says its internal model produced 372 math results", url: "https://www.techmeme.com/261006/p46", source: Techmeme, date: "2026-10-06"}
- {id: 45, title: "OpenAI Solves 722 Math Problems, Quasi-Riemann Hypothesis Proven", url: "https://www.kucoin.com/news/flash/openai-solves-722-math-problems-quasi-riemann-hypothesis-proven", source: "KuCoin News", date: "2026-10-07"}
- {id: 46, title: "Alman, Duan, Vassilevska Williams, Xu, Xu, Zhou — More asymmetry yields faster matrix multiplication", url: "https://arxiv.org/abs/2404.16349", source: arXiv, date: "2024-04-25"}
- {id: 47, title: "HN: OpenAI just dropped 700 preprints of mathematical proofs and counterexamples", url: "https://news.ycombinator.com/item?id=49985740", source: "Hacker News", date: "2026-10-06"}
- {id: 48, title: "OpenAI Astra: ten math results, evidence review", url: "https://kingy.ai/news/openai-astra-ten-math-results-evidence/", source: "Kingy.ai", date: "2026-08-02"}
- {id: 49, title: "OpenAI drops 722 AI math proofs and mathematicians are not impressed", url: "https://startupfortune.com/openai-drops-722-ai-math-proofs-and-mathematicians-are-not-impressed/", source: "Startup Fortune", date: "2026-10-07"}
- {id: 50, title: "ComparatorChallenges/UniqueGamesTheorem.lean and .json", url: "https://raw.githubusercontent.com/openai/math/main/lean/ComparatorChallenges/UniqueGamesTheorem.lean", source: "OpenAI", date: "2026-10-06"}
- {id: 52, title: "Integer multiplication below n log n — §03 Motifs", url: "https://raw.githubusercontent.com/openai/math/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/03-motifs.tex", source: "OpenAI", date: "2026-09-23"}
- {id: 53, title: "Integer multiplication below n log n — §09 Exact arithmetic", url: "https://raw.githubusercontent.com/openai/math/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/09-exact-arithmetic.tex", source: "OpenAI", date: "2026-09-23"}
- {id: 51, title: "ComparatorChallenges/QuasiRiemannHypothesis.lean", url: "https://raw.githubusercontent.com/openai/math/main/lean/ComparatorChallenges/QuasiRiemannHypothesis.lean", source: "OpenAI", date: "2026-10-06"}
:::
