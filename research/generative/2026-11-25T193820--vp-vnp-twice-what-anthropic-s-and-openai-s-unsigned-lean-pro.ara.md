---
eyebrow: Deep Research · Algebraic Complexity · Formal Verification
title: "VP ≠ VNP, twice: what two unsigned Lean proofs pin down, and what no machine checked"
deck: "Anthropic and OpenAI each posted an AI-written proof of Valiant's conjecture within about five hours of each other. The Lean kernels accept both. But they accept different theorems, checked by different tool setups, and the step that matters most, whether the formal statement says what the title claims, has been signed off by no named human."
domain: general
lede: |
  On 23 November 2026 at 20:04 UTC, a commit titled "vp-vnp: VP != VNP, paper and Lean proof" landed in Anthropic's formal-math repository. It credits the result to "an internal research Claude model" and came with no announcement [^1,6]. About five hours later, OpenAI committed its own "VP and VNP are different" manuscript and Lean development to openai/math, and its history file says the result "was obtained on November 6, 2026" [^10,18]. Both developments compile. Both limit themselves to Lean's three standard axioms. Both READMEs, in different words, say the same thing: the kernel checked the proof, and nobody has checked the statement [^1,9]. This article reads the two trusted statement files line by line. It separates what each kernel certified from what the papers claim, and it lists what is still unchecked.
stats:
  - {label: "Time between commits", value: "≈5h10m", note: "20:04Z Nov 23 → 01:14Z Nov 24"}
  - {label: "Anthropic Comparator targets", value: "5", note: "nanoda second kernel on"}
  - {label: "OpenAI Comparator targets", value: "1", note: "nanoda off"}
  - {label: "Prior best general bound", value: "Ω(n log n)", note: "Baur–Strassen, 1983"}
---

:::callout(kind=info, label="Direct answer")
- **What Anthropic's Lean proves.** A trusted file that imports only Mathlib states that, for an absolute constant c > 0, circuits computing the Hamiltonian cycle polynomial need more than m^(c·(log₂ m)^(1/3)) gates over every field, and so do circuits for the permanent outside characteristic 2. The same holds for approximating (border) circuits. It also states VP ⊊ VNP and VNP ⊄ closure(VP) over every field. All five targets pass Comparator, with the independent nanoda kernel turned on [^2,3].
- **What OpenAI's Lean proves.** Its one Comparator target is `vp_ne_vnp`: over every field, the predicates IsVP and IsVNP differ, for families on `Fin n × Bool` variables. The check uses only the Lean kernel, because nanoda is disabled [^11,12]. Its paper's headline result, an exp(Ω((log n)^(5/4))) lower bound for *border* circuits, is not formalized. The Lean proves only an exact, qualitative superpolynomial bound [^13,16].
- **What is unchecked in both.** Whether the trusted definitions of circuits, VP and VNP match Valiant's 1979 classes. ARA's own reading finds no mismatch, but that reading is no substitute for a named algebraic-complexity theorist signing off, and none has [^1,35,36].
- **What it would not mean.** Even if both are right, VP ≠ VNP does not imply P ≠ NP, and the bounds are quasi-polynomial, so the stronger VNP ⊄ VQP stays open [^21,35].
:::

## 1. Two commits, five hours, one contested date

Thesis: the release order is documented to the second, but the discovery order is not. The only evidence for OpenAI's earlier date is a sentence OpenAI wrote itself.

GitHub's records give the Anthropic commit, authored by Thomas Steinke, at 20:04:44 UTC on 23 November. It was merged as PR #51 at about 21:43 UTC [^6]. OpenAI's commit `e07100d`, "Add VP != VNP manuscript and Lean.", carries an author time of 01:14:20 UTC on 24 November. That is still the evening of the 23rd in California, which is why OpenAI's folder is named "November-23-2026". The commit touched 3,163 files and added 442,736 lines [^18]. Commit-to-commit the gap is about 5 hours 10 minutes, and merge-to-merge about 3 hours 47 minutes. Which pair of timestamps an outlet used explains why some coverage reported a gap of "four hours" [^45].

:::timeline
- {date: "1979", headline: "Valiant defines VP and VNP", body: "Permanent shown VNP-complete outside characteristic 2; Hamiltonian cycle polynomial complete over every field."}
- {date: "2026-10-26/27", headline: "Both labs post ETH refutations", body: "OpenAI's upload (20:35Z Oct 26) precedes Anthropic's eth folder (03:07Z Oct 27)."}
- {date: "2026-11-06", headline: "OpenAI's claimed discovery date", body: "Stated only in openai/math history.md."}
- {date: "2026-11-20", headline: "Alpöge's Claude-assisted Riemann Hypothesis claim", body: "Lean-backed; an adjacent test of whether a formal certificate is enough."}
- {date: "2026-11-23 20:04Z", headline: "Anthropic commits vp-vnp", body: "Paper credited to Claude; merged 21:43Z after CI passed."}
- {date: "2026-11-24 01:14Z", headline: "OpenAI commits 'VP and VNP are different'", body: "Signed 'OpenAI'; 3,163 files changed."}
- {date: "2026-11-25 00:04Z", headline: "OpenAI family 379", body: "Hierarchy and Hamiltonian-cycle papers that 'subsume' the Nov 23 manuscript."}
:::

OpenAI's history file has one line on precedence: "VP and VNP are different. This result was obtained on November 6, 2026" [^10]. It gives no hash, timestamped artifact or log. The paper's own date field is empty [^16]. OpenAI's README says it will "defer to the math community completely on matters of credit, precedence, and concurrent work" [^9]. Putting a discovery date 17 days before a rival's upload is an assertion of precedence all the same, made in the one format, an unsigned changelog line, that outsiders cannot audit. Anthropic's README gives no date for when its model found the result [^1]. The upload also came three days after Anthropic mathematician Levent Alpöge said he had, "working with Claude, discovered a proof of the Riemann Hypothesis", a claim backed by Lean [^42]. Andrew Curran, who flagged both uploads on X, reported them as unannounced, and ARA found no blog post or announcement from either lab [^40,41].

Counterpoint: the precedence question may matter less than it looks. The ETH refutations followed the same pattern a month earlier, with OpenAI uploading first that time, and nobody has suggested either lab copied the other [^7,10]. Why this matters: when two unnamed internal models reach the same open conjecture within weeks, the scarce resource is not proofs. It is credible human statement review, and neither release came with it.

## 2. What Valiant's conjecture is, and what it is not

Thesis: VP ≠ VNP is a sharply defined algebraic statement, much weaker than P ≠ NP. It is still far beyond anything the field had proved for general circuits.

Leslie Valiant introduced the classes at STOC 1979. VP is the families of polynomials whose number of variables, degree and arithmetic circuit size all grow at most polynomially. VNP is the families obtained by summing a VP family over exponentially many Boolean assignments to extra variables [^20]. The permanent is VNP-complete over every field of characteristic other than two. In characteristic two, the permanent and the determinant coincide, since −1 = +1, so the permanent is in VP there [^20,36]. The Hamiltonian cycle polynomial, by contrast, is VNP-complete over every field [^20]. That is why both labs state bounds for the Hamiltonian cycle polynomial "over every field" and exclude characteristic 2 for the permanent.

Before November 2026 the state of the art was very weak. For an unrestricted arithmetic circuit computing an explicit polynomial, the best lower bound was the Ω(n log n) of Strassen and Baur–Strassen. Bürgisser's 2024 survey notes that nobody knew how to prove even n² log n for the n×n permanent [^20]. The celebrated recent progress was for *restricted* circuits. Limaye, Srinivasan and Tavenas proved superpolynomial lower bounds for constant-depth circuits in 2021, and won the FOCS 2021 best paper award for it [^22,47]. Forbes extended that result to every field at CCC 2024 [^23]. Depth-reduction results show how far that was from VP ≠ VNP. A depth-3 bound of exp(ω(√d·log^(3/2) d)) for the permanent would already imply general superpolynomial lower bounds [^24], and LST-strength bounds sit well below that bar.

:::compare
- {role: "BEST PROVEN LOWER BOUND, pre-Nov 2026", name: "Baur–Strassen (general circuits)", value: "Ω(n log n)"}
- {role: "BEST KNOWN UPPER BOUND", name: "Ryser-type formula for the permanent", value: "≈ 2^n · n"}
- {role: SUBJECT, name: "Anthropic's claimed lower bound", value: "2^(c·(log m)^(4/3))"}
:::

Rewriting the bounds shows what kind of separation this is. Anthropic's m^(c·(log m)^(1/3)) equals 2^(c·(log m)^(4/3)). That beats every polynomial, because the exponent c·(log m)^(1/3) grows without limit, but it is still *quasi-polynomial* [^2,35]. OpenAI's exp(Ω((log n)^(5/4))) has the same character [^16,36]. Neither therefore settles Valiant's "extended hypothesis", VNP ⊄ VQP, which needs a bound of 2^(ω(polylog)) [^21]. Neither touches Boolean complexity either. The known implications run only one way: Boolean hardness implies algebraic hardness, for instance NP ⊄ P/poly implies VP ≠ VNP over F₂, so an algebraic separation does not prove P ≠ NP [^20,21]. Fortnow said exactly this: "VP ≠ VNP does not imply this Boolean separation" [^35]. VP vs VNP is also not a Clay Millennium problem. P vs NP is [^26].

Counterpoint: "much weaker than P ≠ NP" can be overstated. Anthropic's Lean also states VNP ⊄ closure(VP), a border-complexity separation of the kind Geometric Complexity Theory was built to reach [^2,25]. Since VP sits inside its closure, that statement logically implies VP ≠ VNP, not the other way round. Why this matters: the result is large enough that the burden of proof should be high, and narrow enough that it should not be oversold.

## 3. Anthropic's trusted file, line by line

Thesis: Anthropic put every definition the claim depends on into one file that imports only Mathlib. Read closely, that file encodes the standard non-uniform Valiant classes, with no obvious escape hatch.

The README sets out the trust model plainly: "Lean checks the proofs, but no machine checks that this file says what is claimed" [^1]. It points to Appendix Q of the paper, Table 3, as the map between paper and Lean statements and the list of where they differ [^1]. The circuit model in `Statement.lean` is minimal. Each gate is a variable, an arbitrary constant `C a`, or the sum or product of two earlier gates. Variables and constants count toward the size [^2].

```
def Computes (f : MvPolynomial V R) (s : ℕ) : Prop :=
  ∃ l : ℕ → MvPolynomial V R,
    (∀ k < s, (∃ v, l k = X v) ∨ (∃ a, l k = C a) ∨
      (∃ i < k, ∃ j < k, l k = l i + l j) ∨ (∃ i < k, ∃ j < k, l k = l i * l j)) ∧
    ∃ k < s, l k = f
```

The main theorem fixes the order of quantifiers carefully. It asserts an absolute c > 0 and, for each characteristic p, a threshold m₀. Then, over every field of characteristic p and for every m ≥ m₀, every circuit for the Hamiltonian cycle polynomial, and every circuit for the permanent when p ≠ 2, has more than m^(c·(log₂ m)^(1/3)) gates [^2]. VP is defined as families with variable count, total degree and circuit size all at most n^a + a. VNP is defined as Boolean sums of a VP family over r(n) auxiliary bits [^2]. The headline is `Separation : ∀ F [Field F], VP F ⊂ VNP F`. Because `⊂` is strict inclusion, the statement carries VP ⊆ VNP as well as the inequality [^2].

:::kv
- {term: "Gate set", def: "Variables, arbitrary field constants, binary + and ×. No subtraction gate is needed, since C(−1) supplies negation."}
- {term: "Size measure", def: "Every list entry, including inputs and constants, counts as a gate."}
- {term: "VP bound", def: "Variables, total degree and size ≤ n^a + a, for some a."}
- {term: "VNP", def: "f_n = Σ over e ∈ {0,1}^r(n) of g_n(x, e), with g in VP. r(n) is bounded implicitly because g's variable count is."}
- {term: "Border model", def: "A circuit over Laurent series in ε computing f + ε·g, with g's coefficients power series in ε."}
- {term: "Fields", def: "Any `Field F` with `CharP F p`. The permanent clause excludes p = 2."}
- {term: "Axioms", def: "propext, Classical.choice and Quot.sound only."}
:::

ARA's audit of this file checked the standard ways a statement can go wrong and found none of them. **Vacuity**: `Beyond` uses `Real.logb 2 m`, and Mathlib returns junk value 0 for arguments 0, 1 and −1 [^49]. That cannot trivialize the statement, because it applies only for m ≥ m₀. **Characteristic**: quantifying over every natural number p adds only vacuous cases, because no field has a characteristic that is neither 0 nor prime. **Border**: allowing intermediate constants to be any Laurent series makes approximating circuits *more* powerful, so a lower bound against them is at least as strong as the textbook border notion [^2]. **Witnesses**: VNP needs no explicit bound on r(n), because the VP condition on g already caps its variable count. Comparator runs with an empty `definition_names` list, so the solver could not supply its own definitions [^3]. Comparator's README warns that challenges with such holes "can be gamed without additional oversight" [^27].

`comparator.json` lists five targets: `mainTheorem`, `mainTheoremApprox`, `separation`, `separationClosure` and a fifth, `permanent_over_real`, which the README does not mention [^3]. `Solution.lean` is a thin wrapper. Each target is discharged by citing a theorem in the `Paper/` tree, so all the mathematics lives in untrusted files that only the kernels check [^4]. The repository's rules forbid any `sorry` outside `Challenge.lean` [^7]. The CI script forces `enable_nanoda=true` and passes only on the exact line "Your solution is okay!" [^5]. The verification job passed on PR #51 before the merge [^6]. The toolchain is Lean v4.33.1 [^8], newer than the July kernel-soundness fixes discussed in Section 6.

Counterpoint: the strongest remaining doubt about this file is not in the Lean. It is in the provenance. The README says *AI models* wrote both the paper and the formalization [^1]. A secondary reading of the paper reports that four supporting results, including program constructions that one branch of the main argument needs, are checked only in Lean and not written out in the paper [^43]. If that is right, the paper is not a self-contained human-readable proof. ARA could not extract the PDF to confirm it, so it is not stated here as fact. Why this matters: Anthropic's design makes a human review cheap, since it means reading roughly 100 lines of definitions. It does not make the review unnecessary.

## 4. OpenAI's challenge: a narrower certified theorem than its paper claims

Thesis: OpenAI's trusted statement is correct in shape but deliberately minimal. The quantitative and border claims that make its paper distinctive sit outside what Comparator was asked to check.

OpenAI's challenge file defines `Computes` with binary gates `a + b`, `a − b` or `a * b`. Inputs and field constants are free and not counted [^11]. "Polynomially bounded" means `∃ A d N, ∀ n ≥ N, f n ≤ A * n ^ d`. A p-family bounds variable count and total degree. VNP is again a Boolean sum, here over a polynomially bounded witness set, of a VP family [^11]. Up to constant factors and additive terms, these are the same classes as Anthropic's. A subtraction gate costs one constant and one product in Anthropic's model, and counting or not counting inputs changes size by at most an additive amount. The single target reads:

```
theorem vp_ne_vnp (F : Type u) [Field F] :
    (IsVP : Family F (fun n => Fin n × Bool) → Prop) ≠ IsVNP
```

Two features of this statement deserve attention. First, `≠` between predicates is weaker *as written* than Anthropic's `⊂`. It would also hold if some VP family failed to be in VNP. Here that cannot happen: with an empty witness set the Boolean sum has one term, so VP ⊆ VNP follows immediately from these definitions. OpenAI's 25 November hierarchy challenge, `strict_inclusions`, does state `VP F ⊂ VNP F` explicitly [^14]. Second, the family type is fixed to variables `Fin n × Bool`. That is a restriction on the witness family, not a loophole, since exhibiting one separating family suffices.

The Comparator config is where the two labs diverge. `VPVNP.json` names one theorem, permits the three standard axioms, and sets `enable_nanoda: false`, so only Lean's own kernel checks the proof [^12]. The Hamiltonian-cycle and permanent bounds do exist, as `corollary12` in `Separation.lean`: for every exponent C and characteristic q, eventually m^C < circuitSize(HC_m), and the same for the permanent if q ≠ 2 [^13]. But they are not Comparator targets. The polynomial definitions they use live in the untrusted library rather than a Mathlib-only trusted file [^12,13]. Buzzard has identified that pattern as a failure mode in itself: definitions buried in large untrusted libraries [^32].

:::stack-rows
categories: [Formalized and Comparator-checked, Formalized in library only, Not formalized]
rows:
  - {label: "Anthropic: headline claims (5)", values: [5, 0, 0]}
  - {label: "OpenAI Nov 23: headline claims (4)", values: [1, 2, 1]}
:::

:::note
ARA's tally from the trusted statement files and Comparator configs. Anthropic's five claims are its five comparator.json targets. OpenAI's four headline claims are the VP ≠ VNP separation (a Comparator target); the Hamiltonian cycle and permanent superpolynomial bounds (`corollary12` in the library); and Theorem 1.1's explicit exp(Ω((log n)^(5/4))) border bound (unformalized). Anthropic's explicit exponent is formalized inside `MainTheorem`; OpenAI's Lean states only "beats every n^C".
:::

The gap between OpenAI's paper and its Lean is explicit. Theorem 1.1 of the manuscript reads: "Over every field, border circuits for f_n require exp(Ω((log n)^(5/4))) gates" [^16]. The Lean's `separation_lower_bound` says only that for every C ≥ 1 there is an N beyond which n^C < circuitSize. That is exact circuits, with no rate [^13]. The follow-up papers repeat the pattern. The Hamiltonian-cycle paper claims exp(c·(log N)²/(log log N)²) gates over any field, but its README says the Lean proves "eventual superpolynomial exact circuit lower bounds" [^17]. The family-379 scope document lists seven items that remain unformalized, among them "the paper's explicit n^Ω((log n)^(1/12)) lower bound for the n×n grid" [^15]. OpenAI marks these gaps honestly. It also describes the whole repository as "raw research data, rather than polished academic papers", with about 42% of top-line results formalized [^9].

Counterpoint: a qualitative bound is all VP ≠ VNP needs. On the question of the separation itself, OpenAI's single Comparator target is sufficient, and its definitions read as faithful [^11]. Why this matters: anyone citing OpenAI's *stronger* numbers, the (log n)^(5/4) border rate or the (log N)²/(log log N)² Hamiltonian bound, is citing an unrefereed AI-written paper, not a kernel certificate.

## 5. Same conjecture, different certificates

Thesis: in this case a larger formal development certifies less of the paper, and the size of the trusted statement surface matters more than the line count.

:::bars
- {label: "OpenAI commit e07100d: lines added (all files)", value: "442,736", pct: 100}
- {label: "Anthropic vp-vnp: Lean lines (reported)", value: "72,932", pct: 16}
:::

:::note
OpenAI's figure is the whole commit diff, including Markdown and the paper source, not only Lean. Anthropic's 324 files / 72,932 lines is a secondary count (lilting.ch), not recounted by ARA.
:::

The OpenAI commit is about six times larger than the reported size of Anthropic's development [^18,19]. Neither number says anything about correctness. The quantity a human reviewer has to read is the trusted statement: roughly 100 lines for Anthropic and roughly 60 for OpenAI's challenge file [^2,11].

| Dimension | Anthropic (anthropics/formal-math/vp-vnp) | OpenAI (openai/math, Nov 23 edition) |
|---|---|---|
| Credited author | "Claude (Anthropic)"; "internal research Claude model" [^1] | "OpenAI"; "an unnamed internal OpenAI model" [^9,16] |
| Trusted statement | `Statement.lean`, imports only Mathlib [^2] | `ComparatorChallenges/VPVNP.lean`, imports Mathlib [^11] |
| Separation form | `VP F ⊂ VNP F` and `¬ VNP F ⊆ VPBar F` [^2] | `IsVP ≠ IsVNP` on `Fin n × Bool` families [^11] |
| Explicit rate in Lean | Yes: m^(c·(log₂ m)^(1/3)) [^2] | No: "eventually > n^C" [^13] |
| Border result in Lean | Yes, Comparator target [^3] | No (paper Theorem 1.1) [^16] |
| Permanent / HC in trusted file | Yes [^2] | No; library `corollary12` [^13] |
| Second kernel | nanoda on [^3] | nanoda off [^12] |
| Lean toolchain | v4.33.1 [^8] | v4.34.1 [^19] |
| Human review stated | "no human mathematician has checked the proof" [^1] | None stated; "raw research data" [^9] |

The configurations reflect different theories of trust. Anthropic's CI script *forces* the second kernel on [^5]. OpenAI's repository disables it for this challenge [^12]. In the other direction, OpenAI had already gone through a full public correction cycle before this release: on 7 October it withdrew three manuscripts because "a sign error invalidates a stabilization-trace cancellation argument" [^10]. Anthropic's vp-vnp folder, by contrast, is labelled "Not maintained and not accepting contributions" [^1].

Counterpoint: running nanoda is defence in depth against kernel bugs, which are rare. It does nothing for the risk that dominates in practice, a mis-stated theorem [^28,31]. Why this matters: if a single fact about each release is reported, it should be which statement was certified, not how many lines were written.

## 6. What the kernel certifies, and the July precedent

Thesis: a Comparator pass means the proof establishes the challenge statement under three axioms, provided the kernels are sound. In 2026 that last condition was not theoretical.

Comparator's guarantee has three parts. If it succeeds, the solution theorems "Prove the same statement as provided in `Challenge`", use no more axioms than permitted, and are "accepted by the Lean kernel". With an external kernel enabled, the trust assumption weakens to "at least one of the Lean kernel or the `external_kernels` is correct" [^27]. The Lean reference manual draws the line plainly: "Lean can establish that a statement has been proven, but not whether it is the intended statement" [^28]. The kernel also cannot re-check native-code computation, which is why the "only three axioms" condition matters. External checkers "cannot check such proofs, as they do not have access to the Lean compiler" [^28].

July 2026 showed why a second kernel is more than ceremony. On 22 July, Lean 4.32.1 fixed a kernel bug that allowed proving `False`, though the recommended Comparator workflow was "not affected" [^44]. Six days later, 4.32.2 fixed a second bug in the handling of nested inductive types with phantom parameters. The release notes say: "The bug can be exploited even when using `comparator`" [^29]. nanoda did not share that bug, but Ramana Kumar showed one proof term could combine it with a separate nanoda flaw [^29]. The trigger, according to the oss-security advisory, was a repository claiming a Lean formalization disproving the Collatz conjecture, which both kernels had accepted, which led to the conclusion that "independently rechecking Lean declarations was not sufficient against this particular implementation flaw" [^30].

:::rank-list
- {label: "Statement fidelity (definitions match Valiant)", value: "unchecked by any human", pct: 100, highlight: true}
- {label: "Paper-only claims (rates, border for OpenAI)", value: "unformalized", pct: 80}
- {label: "Kernel soundness", value: "1 kernel (OpenAI) / 2 kernels (Anthropic)", pct: 35}
- {label: "Axiom hygiene", value: "3 standard axioms, both", pct: 10}
:::

:::note
ARA's ordering of residual risk. Fill length is a qualitative judgement of how much each item limits confidence today, not a measured probability.
:::

Both toolchains, v4.33.1 and v4.34.1, postdate the July fixes [^8,19]. Anthropic pins a nanoda build, from the robsimmons/nanoda_lib fork, and requires it to agree [^5]. The residual kernel risk is therefore small for Anthropic and somewhat larger for OpenAI. It is still dwarfed by the risk the kernels cannot address. Buzzard's 12 November audit of OpenAI's earlier release found that "around 38" of roughly 290 Lean-backed papers have Lean code that "does not even state, let alone prove, the main theorem of the paper" [^32]. His recommended remedy is a statement file with "very few imports beyond Mathlib" plus `lake comparator --paranoid` with many independent kernels. That is close to what Anthropic built, and further than what OpenAI's VP/VNP challenge uses [^32,3,12].

Counterpoint: the 4.32.2 exploit needed a *malicious* metaprogram. Neither lab is plausibly adversarial toward its own result. The realistic failure is an honest error that a model's search found convenient, and the axiom check and Comparator are designed to stop exactly that [^27]. Why this matters: "checked in Lean" is a family of claims of different strength. Readers should ask which kernel, which statement file and which toolchain.

## 7. The unchecked step: does the statement say "VP ≠ VNP"?

Thesis: statement fidelity is where formalized mathematics fails most often, and on both releases it rests on unsigned AI readings and a handful of blog-speed impressions.

The base rates are not reassuring. DeepMind's Formal Conjectures project reports that 291 misformalizations have been fixed across 7,559 Lean statements. AI proofs and disproofs were part of the auditing mechanism that found them [^33]. The fixes break down by error type as follows:

:::donut(center-label="291 fixes")
- {label: "Misrepresentation (140)", value: 48.1}
- {label: "Semantic (103)", value: 35.4}
- {label: "Implicit conventions (23)", value: 7.9}
- {label: "Reporting (15)", value: 5.2}
- {label: "Syntactic (9)", value: 3.1}
- {label: "Mathematical (1)", value: 0.3}
:::

:::source
Formal Conjectures misformalization taxonomy, arXiv 2605.13171 [^33].
:::

Separately, a 2025 audit of the miniF2F benchmark found "discrepancies between the formal and informal statements for more than half of the problems" [^34]. The categories that matter most for a VP/VNP statement are "misrepresentation" (wrong quantifiers, dropped hypotheses) and "semantic" errors (truncated subtraction, junk values). Section 3's audit was aimed at exactly those [^33].

Who has actually read these files? Lance Fortnow wrote on X, as reported by DataCamp, that he had Claude and Gemini check the formalization without processing the Lean proof, and he called the result "likely correct" [^38]. His blog post the same day called it "for now, the most important computational complexity result of the year" [^35]. Scott Aaronson wrote that the Lean certifies correctness "to a level considerably beyond what we'd normally demand". He also invited experts to raise "any real technical issue" [^36]. Gil Kalai wrote that he is "overwhelmed" and "quite confused about the nature and speed of events" [^37]. None of these is a line-by-line statement audit by a specialist in algebraic complexity. ARA found no such audit published by Saraf, Srinivasan, Limaye, Tavenas, Bürgisser, Grochow or any other specialist as of 26 November. A public fork re-checks Anthropic's proof with additional kernels. Its own notes say the only change to `Statement.lean` is notational, which re-validates the proof, not the meaning of the statement [^46].

:::quote(attr="Anthropic vp-vnp README, 23 November 2026")
Lean checks the proofs, but no machine checks that this file says what is claimed.
:::

The second unchecked item is the mathematics a human would need to *understand*. Aaronson describes both proofs as "highly nontrivial 'compression' or 'shortening,' followed in the end by a diagonalization", and suggests diagonalization is what lets them evade the natural-proofs barrier. He adds that on the algebraic relativization barrier, "I don't know how to tell it yet" [^36]. Fortnow says Anthropic's proof "uses a variant of Strassen's asymptotic spectrum to split into two cases, one handled by a rank argument and the other by a diagonalization", with "essentially no algebraic geometry" [^35]. Anthropic's own Lean docstrings describe the same two-way case split, which the proof never decides [^50]. That makes the threshold m₀ non-effective. The theorem proves that it exists but gives no way to compute it. A certificate can establish that two barriers were passed without anyone yet being able to explain how.

Counterpoint: insisting on human statement review may soon be the bottleneck rather than the safeguard. Anthropic's statement file is short and conventional, and an AI-assisted reading by a complexity theorist found it sound [^38]. Why this matters: until one named expert puts a signature on roughly 100 lines, the honest status is "kernel-certified proof of a statement that very probably encodes VP ≠ VNP". That is strong, but it is not the same as "VP ≠ VNP is proved".

## 8. What else is unchecked: provenance, authorship and the paper-to-Lean seam

Thesis: beyond statement fidelity, both releases leave institutional questions open that the mathematics community normally settles through authorship and refereeing.

**Authorship.** Neither model is named. Anthropic's README credits "an internal research Claude model". OpenAI credits "an unnamed internal OpenAI model" and says the project used about 4,000 posed problems and about three hours of ChatGPT Pro thinking compute per result [^1,9]. Without a named model and process, no one outside can reproduce the discovery. They can only re-run the certificate.

**Provenance.** OpenAI's November 6 date is a single unsupported sentence [^10]. Anthropic offers no date at all [^1]. The ETH precedent shows both labs reaching the same class of result within a day of each other, with no public account of how [^7,10].

**The paper-to-Lean seam.** For OpenAI, every quantitative improvement in the papers, including the (log n)^(5/4) border bound, the (log N)²/(log log N)² Hamiltonian bound and the (log n)^(1/12) grid bound, sits on the unformalized side [^15,16,17]. For Anthropic, the README points to Appendix Q for where paper and Lean "differ" [^1]. One secondary account reports that a remark about approximate determinantal complexity is the only numbered statement without a Lean counterpart [^43].

**Maintenance.** OpenAI says two 24 November preprints "subsume" the 23 November paper, which "remains available unchanged" [^10]. Anthropic's folder accepts no contributions [^1]. Errata will therefore flow through a changelog in one case and nowhere in the other.

:::iso
- {label: "Comparator targets: Anthropic", glyph: "✔", count: 5}
- {label: "Comparator targets: OpenAI (VP/VNP)", glyph: "✔", count: 1}
- {label: "Named human statement audits (either lab)", glyph: "✍", count: 0}
:::

Counterpoint: refereeing has never been instant, and a few days without a formal audit is normal, not damning. Public scrutiny is already intense: the Hacker News thread on Anthropic's release had 366 points and 333 comments when ARA read it, though it mostly debated what the result means for P vs NP [^39]. Why this matters: the community's verdict, not the kernel's, will decide credit, and the artifacts as released give it few handles beyond the code itself.

## 9. What could break this reading

Thesis: there are three concrete ways this article's central judgement, "probably faithful statements, certified proofs, unsigned meaning", could turn out wrong.

**A definition is subtly off.** The most plausible failure is a Formal-Conjectures-style "misrepresentation" [^33]. Examples would be a size measure that lets a circuit reuse a polynomial for free in a way the paper's argument quietly needs, or a Laurent-series border model that differs from what the paper's bound uses. ARA's reading found neither. But ARA is itself running on a Claude model, so it is not independent of the system that wrote the Anthropic statement. This audit should be weighted accordingly.

**The kernel case is worse than assumed.** A third 2026-style kernel bug, combined with an unexploited nanoda flaw, would break Anthropic's two-kernel guarantee. Only the first condition would be needed to break OpenAI's single-kernel check [^29,30]. No such issue has been reported against either development. Neither is the kind of adversarial upload that triggered July's fixes.

**The convergence is evidence of a shared error, not a shared truth.** Aaronson notes the two proofs "look similar" [^36]. Two related models converging on similar compression-plus-diagonalization arguments is somewhat less independent than two human teams would be. In fairness, a shared conceptual error would still have to get past two separate kernels on two separate statement files.

:::callout(kind=warn, label="Red-team result")
Red-team pass: 3/3 top claims unbroken. An adversarial reviewer re-fetched the primary files on 26 November and searched for contrary evidence on the three load-bearing claims: the five-versus-one Comparator configuration, the unformalized status of OpenAI's border rate, and the absence of any named human statement audit. Neither config had changed, and no specialist audit had appeared. The one addition it found is that the kim-em fork now re-checks Anthropic's proof with further independent kernels on a newer Lean release candidate [^46]. That strengthens the kernel side and leaves the statement side untouched.
:::

Why this matters: each of these breaks is checkable in days by the right person. The first one, a specialist reading roughly 100 lines of `Statement.lean` and roughly 60 lines of `VPVNP.lean`, is the cheapest high-value act of peer review available in mathematics right now.

:::references
- {id: 1, title: "vp-vnp README: VP ≠ VNP over every field", url: "https://github.com/anthropics/formal-math/tree/main/vp-vnp", source: "Anthropic, GitHub", date: "2026-11-23"}
- {id: 2, title: "vp-vnp/Statement.lean", url: "https://raw.githubusercontent.com/anthropics/formal-math/main/vp-vnp/Statement.lean", source: "Anthropic, GitHub", date: "2026-11-23"}
- {id: 3, title: "vp-vnp/comparator.json", url: "https://raw.githubusercontent.com/anthropics/formal-math/main/vp-vnp/comparator.json", source: "Anthropic, GitHub", date: "2026-11-23"}
- {id: 4, title: "vp-vnp/Solution.lean", url: "https://raw.githubusercontent.com/anthropics/formal-math/main/vp-vnp/Solution.lean", source: "Anthropic, GitHub", date: "2026-11-23"}
- {id: 5, title: "formal-math CI: comparator-check.sh", url: "https://raw.githubusercontent.com/anthropics/formal-math/main/.github/scripts/comparator-check.sh", source: "Anthropic, GitHub", date: "2026-11-23"}
- {id: 6, title: "anthropics/formal-math commit history", url: "https://github.com/anthropics/formal-math/commits/main", source: "GitHub", date: "2026-11-23"}
- {id: 7, title: "anthropics/formal-math root README", url: "https://github.com/anthropics/formal-math", source: "Anthropic, GitHub", date: "2026-11-25"}
- {id: 8, title: "vp-vnp/lean-toolchain", url: "https://raw.githubusercontent.com/anthropics/formal-math/main/vp-vnp/lean-toolchain", source: "Anthropic, GitHub", date: "2026-11-23"}
- {id: 9, title: "openai/math README", url: "https://github.com/openai/math", source: "OpenAI, GitHub", date: "2026-11-25"}
- {id: 10, title: "openai/math history.md", url: "https://raw.githubusercontent.com/openai/math/main/history.md", source: "OpenAI, GitHub", date: "2026-11-25"}
- {id: 11, title: "ComparatorChallenges/VPVNP.lean", url: "https://raw.githubusercontent.com/openai/math/main/lean/ComparatorChallenges/VPVNP.lean", source: "OpenAI, GitHub", date: "2026-11-24"}
- {id: 12, title: "ComparatorChallenges/VPVNP.json", url: "https://raw.githubusercontent.com/openai/math/main/lean/ComparatorChallenges/VPVNP.json", source: "OpenAI, GitHub", date: "2026-11-24"}
- {id: 13, title: "OAI/Computability/VPVNP/Separation.lean", url: "https://raw.githubusercontent.com/openai/math/main/lean/OAI/Computability/VPVNP/Separation.lean", source: "OpenAI, GitHub", date: "2026-11-24"}
- {id: 14, title: "ComparatorChallenges/ArithmeticHierarchy.lean", url: "https://raw.githubusercontent.com/openai/math/main/lean/ComparatorChallenges/ArithmeticHierarchy.lean", source: "OpenAI, GitHub", date: "2026-11-25"}
- {id: 15, title: "Lean scope notes for family 379 (docs/379.md)", url: "https://raw.githubusercontent.com/openai/math/main/lean/docs/379.md", source: "OpenAI, GitHub", date: "2026-11-25"}
- {id: 16, title: "VP and VNP are different (paper source)", url: "https://raw.githubusercontent.com/openai/math/main/preprints/VP-and-VNP-are-different-November-23-2026/build/Paper.tex", source: "OpenAI, GitHub", date: "2026-11-24"}
- {id: 17, title: "Circuit lower bounds for Hamiltonian cycle and the permanent (README)", url: "https://raw.githubusercontent.com/openai/math/main/preprints/Circuit-lower-bounds-for-Hamiltonian-cycle-and-the-permanent-November-24-2026/README.md", source: "OpenAI, GitHub", date: "2026-11-25"}
- {id: 18, title: "Commit e07100d: Add VP != VNP manuscript and Lean.", url: "https://github.com/openai/math/commit/e07100d", source: "GitHub", date: "2026-11-24"}
- {id: 19, title: "openai/math lean/lean-toolchain", url: "https://raw.githubusercontent.com/openai/math/main/lean/lean-toolchain", source: "OpenAI, GitHub", date: "2026-11-24"}
- {id: 20, title: "Completeness classes in algebraic complexity theory (Bürgisser)", url: "https://arxiv.org/abs/2406.06217", source: arXiv, date: "2024-06-10"}
- {id: 21, title: "Algebraic complexity classes (Mahajan survey)", url: "https://arxiv.org/abs/1307.3863", source: arXiv, date: "2013-07-15"}
- {id: 22, title: "Superpolynomial lower bounds against low-depth algebraic circuits (Limaye, Srinivasan, Tavenas)", url: "https://eccc.weizmann.ac.il/report/2021/081/", source: ECCC, date: "2021-06-14"}
- {id: 23, title: "Low-depth algebraic circuit lower bounds over any field (Forbes)", url: "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2024.31", source: "CCC 2024, LIPIcs", date: "2024-07-01"}
- {id: 24, title: "Arithmetic circuits: a chasm at depth three (Gupta, Kamath, Kayal, Saptharishi)", url: "https://eccc.weizmann.ac.il/report/2013/026", source: ECCC, date: "2013-02-11"}
- {id: 25, title: "Boundaries of VP and VNP (Grochow, Mulmuley, Qiao)", url: "https://arxiv.org/abs/1605.02815", source: arXiv, date: "2016-05-10"}
- {id: 26, title: "Millennium Prize Problems", url: "https://www.claymath.org/millennium-problems/", source: "Clay Mathematics Institute"}
- {id: 27, title: "Comparator README", url: "https://github.com/leanprover/comparator", source: "Lean FRO, GitHub", date: "2026-10-20"}
- {id: 28, title: "Validating Proofs (Lean language reference)", url: "https://lean-lang.org/doc/reference/latest/ValidatingProofs/", source: "Lean FRO"}
- {id: 29, title: "Lean 4.32.2 release notes", url: "https://lean-lang.org/doc/reference/latest/releases/v4.32.2/", source: "Lean FRO", date: "2026-07-28"}
- {id: 30, title: "oss-security: Lean 4 kernel soundness advisory", url: "https://openwall.com/lists/oss-security/2026/08/02/1", source: "oss-security", date: "2026-08-02"}
- {id: 31, title: "nanoda_lib: external type checker for Lean 4", url: "https://github.com/ammkrn/nanoda_lib", source: GitHub}
- {id: 32, title: "And the proof is checked in Lean (Kevin Buzzard)", url: "https://xenaproject.wordpress.com/2026/11/12/and-the-proof-is-checked-in-lean/", source: "Xena Project", date: "2026-11-12"}
- {id: 33, title: "Formal Conjectures: misformalization audit", url: "https://arxiv.org/abs/2605.13171", source: arXiv, date: "2026-05-13"}
- {id: 34, title: "miniF2F in Rocq/Lean: formal vs informal statement discrepancies (Ospanov, Farnia, Yousefzadeh)", url: "https://arxiv.org/abs/2511.03108", source: arXiv, date: "2025-11-05"}
- {id: 35, title: "VP ≠ VNP (Lance Fortnow)", url: "https://blog.computationalcomplexity.org/2026/11/vp-vnp.html", source: "Computational Complexity blog", date: "2026-11-24"}
- {id: 36, title: "I've been drinking wine in my kitchen (Scott Aaronson)", url: "https://scottaaronson.blog/?p=10362", source: "Shtetl-Optimized", date: "2026-11-24"}
- {id: 37, title: "Algebraic complexity: VP ≠ VNP, Möbius pseudorandomness, the Riemann hypothesis (Gil Kalai)", url: "https://gilkalai.wordpress.com/2026/11/24/algebraic-complexity-vp-%E2%89%A0-vnp-mobius-pseudorandomness-the-riemann-hypothesis-and-tyi-61/", source: "Combinatorics and more", date: "2026-11-24"}
- {id: 38, title: "Lance Fortnow on X: VP ≠ VNP reaction, as quoted by DataCamp", url: "https://www.datacamp.com/blog/claude-claims-proof-of-valiants-conjecture-vp-vs-vnp", source: DataCamp, date: "2026-11-24"}
- {id: 39, title: "VP ≠ VNP over Every Field (discussion)", url: "https://news.ycombinator.com/item?id=50620102", source: "Hacker News", date: "2026-11-24"}
- {id: 40, title: "Andrew Curran on Anthropic's vp-vnp upload", url: "https://x.com/AndrewCurran_/status/2125001971690315858", source: X, date: "2026-11-23"}
- {id: 41, title: "Andrew Curran on OpenAI's VP ≠ VNP upload", url: "https://x.com/AndrewCurran_/status/2125289527531245998", source: X, date: "2026-11-24"}
- {id: 42, title: "Anthropic mathematician claims to prove the Riemann hypothesis", url: "https://www.scientificamerican.com/article/anthropic-mathematician-claims-to-prove-riemann-hypothesis-most-famous-problem-in-all-of-math/", source: "Scientific American", date: "2026-11-20"}
- {id: 43, title: "Checking Anthropic's VP≠VNP Lean proof, its difference from P≠NP, and CI verification scope", url: "https://lilting.ch/en/articles/vp-vnp-valiant-conjecture-claude-lean", source: lilting.ch, date: "2026-11-24"}
- {id: 44, title: "Lean 4.32.1 release notes", url: "https://lean-lang.org/doc/reference/latest/releases/v4.32.1/", source: "Lean FRO", date: "2026-07-22"}
- {id: 45, title: "OpenAI says it had a VP vs VNP proof 17 days before Anthropic posted one", url: "https://maccus.fr/en/openai-vp-vs-vnp-proof/", source: MACCUS, date: "2026-11-25"}
- {id: 46, title: "kim-em/vp-vnp (independent-kernel re-check fork)", url: "https://github.com/kim-em/vp-vnp", source: GitHub, date: "2026-11-25"}
- {id: 47, title: "Weizmann complexity seminar note on Limaye–Srinivasan–Tavenas (FOCS 2021 best paper)", url: "https://www.wisdom.weizmann.ac.il/~oded/MC/307.html", source: "Oded Goldreich, Weizmann Institute"}
- {id: 49, title: "Mathlib: Real.logb (Analysis/SpecialFunctions/Log/Base)", url: "https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/SpecialFunctions/Log/Base.html", source: "Mathlib docs"}
- {id: 50, title: "vp-vnp/Paper/Alternative.lean", url: "https://raw.githubusercontent.com/anthropics/formal-math/main/vp-vnp/Paper/Alternative.lean", source: "Anthropic, GitHub", date: "2026-11-23"}
:::
