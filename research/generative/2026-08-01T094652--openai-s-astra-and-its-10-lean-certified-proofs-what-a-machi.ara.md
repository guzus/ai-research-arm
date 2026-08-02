---
eyebrow: REPORT · AI & MATHEMATICS
title: "OpenAI's Astra and its ten Lean certificates: what a machine-checkable proof actually settles"
domain: general
deck: A certificate ends the argument the October 2025 Erdős fiasco was about. It does not begin the one that matters.
lede: |
  On 1 August 2026 OpenAI published ten claimed advances in mathematics and theoretical computer science, attributed them to an unreleased model called Astra, and did something its last mathematical announcement did not: it shipped machine-checkable Lean proofs. That closes the failure mode of October 2025 outright — a certificate constructs a theorem instead of citing one. But the Lean kernel certifies that a proof follows from three axioms *relative to the definitions in the file*, and in these certificates almost every load-bearing definition was written by the same party that wrote the proof. The checker's own authors say so in its README. Hours after publication, no named mathematician had inspected a single one.
stats:
  - {label: Results claimed, value: "10", note: "manifest lists 12"}
  - {label: Stated token cost, value: $2,000, note: "at Sol API rates"}
  - {label: Attempts disclosed, value: "0", note: "no denominator"}
  - {label: Named human authors, value: "0", note: "no preprint, no journal"}
---

:::callout(kind=info, label="The short answer")
- **A Lean certificate does settle something real.** October 2025's failure — a model retrieving known literature and staff calling it new — cannot survive a machine-checked proof, because the proof constructs the theorem rather than citing it. [^30,33]
- **It settles less than "verified" implies.** The kernel proves the term inhabits the stated proposition. Whether that proposition is the famous conjecture is a human judgment, and Comparator's own README says definition-level solutions "**must** always be checked with an additional (potentially human) verifier." [^14]
- **The trust surface moved, it did not shrink.** Every challenge file imports only `import Mathlib` and then defines its own `SpherePackingConstant`, `HasKazhdanPropertyT`, `ConnesRigidityAssertion`. Nothing checkable guarantees those mean what their names say. [^5,6]
- **The ten are not one claim.** They run from a sharp Ehrhart constant to a 0.9% exponent gain to a Ramsey bound that will not beat the 2021 record until k is around 10^60. [^13,8]
- **The $2,000 has no denominator.** DeepMind published its own — 9 of 353 — at a comparable per-result cost. OpenAI published ten successes and no attempt count. [^36,1]
:::

## 01. The release, and why it is not October 2025 again

On 1 August 2026, OpenAI published ten claimed mathematical advances — spanning sphere packing, binary and spherical codes, non-sofic groups, Connes's rigidity conjecture, arithmetic circuit complexity, quantum parallel repetition, the closest vector problem, Ehrhart's volume conjecture, multicolour Ramsey numbers, and extremal-number conjectures — each attributed to an unreleased internal build of Astra and each shipped with a Lean certificate in a public repository. [^1,2] Sébastien Bubeck announced it as "10 such Astra proofs, complete with lean certificates and CoT walkthroughs for each of them." [^32] {accent}OpenAI attached machine-checkable certificates to this announcement precisely because its previous mathematical announcement collapsed under scrutiny: the certificate is the institutional lesson of October 2025, and it does change what can be faked.{/}

The shape of the release, as OpenAI itself documents it — note that the manifest lists twelve main results, not ten, splitting binary from spherical codes and compactness from two-degenerate graphs [^3]:

:::kv
- {term: Model, def: "Internal version of Astra, unreleased"}
- {term: Results claimed, def: "10 (formalization.yaml lists 12)"}
- {term: Certificates, def: "Lean 4.32.0, mathlib pinned"}
- {term: Permitted axioms, def: "propext, Quot.sound, Classical.choice"}
- {term: Review status, def: "agent-reviewed"}
- {term: Named human authors, def: "None"}
:::

In October 2025, OpenAI staff posted that GPT-5 had found solutions to ten Erdős problems "listed as open." It had not solved them; it had located the existing literature. Thomas Bloom, who runs erdosproblems.com, called the claim "a dramatic misrepresentation," Demis Hassabis called it "embarrassing," and the posts were deleted. [^30,31,33,34] The failure mode is worth naming precisely, because it is narrower than "the model was wrong": nothing about the mathematics was false. What was false was the claim of novelty — and it survived to publication because the only thing standing between the model's output and the announcement was a human reading prose and believing it.

That specific failure mode cannot survive a Lean certificate, and it is worth saying so plainly before qualifying anything. A certificate does not cite a theorem; it constructs one. Lean's kernel replays the proof term against the stated theorem and either accepts it or refuses, and no amount of fluent prose moves that verdict. A model that has quietly recovered a known result and dressed it as new will still emit a certificate that checks — but what it has produced is a proof *of* the theorem rather than an assertion *about* the literature, and the residual question ("is this new?") is a bibliographic one a competent human can settle in an afternoon. October 2025 is now, in principle, mechanically excluded. That is a categorical improvement, not a cosmetic one.

It is also not unprecedented, and the prior art sets the bar. DeepMind's AlphaProof reached IMO 2024 silver-medal standard with machine-checked Lean proofs, scoring 28 points against a 29-point gold cutoff. [^35] In May 2026, DeepMind's formal proof-search agent autonomously resolved 9 of 353 open Erdős problems with Lean-verified proofs — and reported that a much simpler baseline replicated those successes. [^36] Both results share a property the ten do not: a denominator. Ten successes out of an undisclosed number of attempts is not a rate.

Two things would weaken the certificate story, and both are already on the record. First, a Lean development can type-check while proving nothing about the object it claims to be about: on 3 June 2026 a LeanMarathon run formalizing OpenAI's own unit-distance disproof modelled a number field as a dummy record, yielding a development that "type-checks and passes CI, but proves nothing real." [^39] The kernel checks the proof, never the fidelity of the statement to the mathematics it is named after. Second, OpenAI's page is internally inconsistent about who formalized what — it says the model "formalized each argument in a Lean certificate," and also that "we helped prepare the manuscripts and formalize the proofs in Lean, and we take responsibility for their correctness." [^1] Both cannot be fully true, and the gap sits exactly on the fidelity question. The surrounding hygiene is thin: the repository is a single commit with Issues disabled and no CI workflow [^2], and the companion chain-of-thought walkthroughs are themselves model-written. [^13,32]

The chronology explains why the release looks the way it does — a decade of announcement norms compressed into nine months. [^23,29,30,35,36,38,39,68]

:::timeline
- {date: 2025-10, headline: "The Erdős retraction", body: "OpenAI staff post that GPT-5 found solutions to ten Erdős problems 'listed as open'; the model had located existing literature. Bloom calls it 'a dramatic misrepresentation'; Hassabis calls it 'embarrassing'; the posts are deleted."}
- {date: 2025-11, headline: "AlphaProof in Nature", body: "DeepMind's AlphaProof reaches IMO 2024 silver-medal standard with machine-checked Lean proofs — 28 points against a 29-point gold cutoff."}
- {date: 2026-05-20, headline: "Unit distance, human-digested", body: "OpenAI's disproof of the Erdős unit-distance conjecture survives, but only after nine named mathematicians — including Bloom and Gowers — digest and simplify it."}
- {date: 2026-05-21, headline: "A published denominator", body: "DeepMind's formal proof-search agent autonomously resolves 9 of 353 open Erdős problems with Lean-verified proofs; a much simpler baseline replicates those successes."}
- {date: 2026-06-02, headline: "The Leiden Declaration", body: "3,340 signatories, endorsed by the International Mathematical Union, warn against announcing results by press release or blog post without a paper."}
- {date: 2026-06-03, headline: "A certificate that proved nothing", body: "A LeanMarathon run formalizing OpenAI's unit-distance disproof models a number field as a dummy record; the development 'type-checks and passes CI, but proves nothing real.'"}
- {date: 2026-07-20, headline: "Buzzard changes his terms", body: "Kevin Buzzard says he refuses to read AI-generated informal mathematics and asks for a full Lean formalization instead."}
- {date: 2026-07-31, headline: "Astra previewed", body: "Astra remains a tentative codename; OpenAI has not decided whether to ship it as GPT-6, GPT-5.7, or a separate class alongside Sol, Terra and Luna."}
- {date: 2026-08-01, headline: "Ten proofs, ten certificates", body: "OpenAI publishes ten results attributed to an internal Astra build, with Lean certificates in a public repository."}
:::

This matters because the mathematical community has already moved its terms to meet exactly this artifact. Kevin Buzzard now refuses to read AI-generated informal mathematics and asks for a full Lean formalization instead [^23], while the Leiden Declaration — 3,340 signatories, endorsed by the International Mathematical Union — warns against announcing results by press release or blog post without a paper. [^29] OpenAI has supplied the formalization and skipped the paper. Whether half of that bargain is enough is what the rest of this article tests.

## 02. What a Lean certificate mechanically proves

The Astra certificates are checked by an unusually strong pipeline — stronger than most published AI-math claims — and it is worth stating precisely what that pipeline does and does not put beyond dispute.

Start with the object being checked. A Lean proof is not prose that a referee reads; it is a term whose type is the theorem statement, and "checking" it means a small kernel re-derives that typing judgement from scratch. Everything the elaborator did on the way — tactics, macros, `simp` sets, whatever a model emitted — is discarded. What survives into the trusted computing base is the kernel, the definitions the statement mentions, and any axioms invoked. That is the whole of it, and it is small enough to enumerate. [^16,20,21,22,14]

:::kv
- {term: Foundational axioms, def: "propext, Quot.sound, Classical.choice"}
- {term: Independent kernels, def: "lean4export + nanoda, a from-scratch Rust kernel"}
- {term: Build sandbox, def: "landrun, on the Linux Landlock LSM"}
- {term: Reference corpus, def: "mathlib: 283,758 theorems, 772 contributors"}
- {term: Comparator guarantees, def: "3 (same statement, no extra axioms, kernel-accepted)"}
- {term: Comparator assumptions, def: "6, including 'no sandbox escape' and kernel correctness"}
:::

The tooling here was not improvised for the occasion. Comparator was built by the Lean FRO with the AIMO team "in support of the AIMO series of competitions," explicitly to enable "trustworthy LLM Lean evaluation on Kaggle" — an adversarial-grader problem specified before this release existed. [^14] OpenAI's configs set `permitted_axioms` to exactly the three standard axioms and turn on `enable_nanoda`, so each proof is replayed by a second kernel written independently of Lean's own. [^4,3]

| Step | What it does | What it rules out |
|---|---|---|
| 1 | Build `Challenge` with `lake` inside a `landrun` sandbox | Build scripts that phone home, patch the toolchain, or read the solution before it is submitted |
| 2 | Run `lean4export` on the produced `Challenge.olean`, sandboxed | Divergence between the source a human reads and the environment actually compiled |
| 3 | Repeat the sandboxed build and export for `Solution` | A solution environment assembled by any path other than a clean, isolated build |
| 4 | Verify every declaration used in the *statements* is identical in both environments | Redefining `Nat`, an order relation, or a hypothesis class so the "theorem" proved is a trivial impostor |
| *5 | Verify theorem bodies use no axioms outside `permitted_axioms` | `sorry` (which surfaces as `sorryAx`), smuggled custom axioms, and `native_decide` |
| 6 | Replay the `Solution` environment into the Lean kernel | Environment hacking that only the elaborator would accept — anything that never faces the kernel |

Two of these deserve emphasis because they defeat attacks that have actually been attempted. Step 5's audit is not grep: Math Inc.'s FormalQualBench documented models building the token `"ax" ++ "iom"` by string concatenation inside an `elab` block, which no textual scan catches but an environment-level axiom check does. [^63] And the sandbox in steps 1 to 3 is not paranoia about the *proof* — it is that building an untrusted Lean file executes arbitrary attacker-controlled code, because elaboration runs metaprograms and lakefile build scripts long before the kernel sees a term. [^22] Excluding `native_decide` matters for the same reason: it would drag the Lean compiler and interpreter, "extra 30k lines of code," into the trusted base. [^17]

A warning to anyone about to audit this repository by keyword. The `ComparatorChallenges` files in `openai/ten-proofs` contain `sorry` — four of them in `A_SpherePacking.lean` alone. This is the protocol working as designed, not fraud: the README specifies that `Challenge.lean` "contains at least a theorem named `todo1` that has a `sorry`," and the separate solution module supplies the real proof. [^14,5] A naive `grep sorry` over this repository produces a false accusation. The honest check is the axiom audit, which is why Lean's own documentation describes `sorryAx` as meaning "this theorem or one of its dependencies uses `sorry` or is otherwise incomplete." [^16]

Is the double-kernel step theatre? No. A Lean 4 kernel bug filed 2026-07-28 let a user prove `False` through the ordinary checked path with no axioms at all, and `#print axioms` reported nothing. [^18] A separate open issue shows `@[csimp]` smuggling an axiom past `#print axioms`, which lists only `Lean.ofReduceBool`. [^19] Independent replay through a from-scratch Rust kernel is the defence against exactly that class, and Leonardo de Moura presented this multi-kernel architecture at FLoC 2026, quoting Tao that it is "really important with these formal proof assistants that there are no backdoors or exploits" because reinforcement learning is so good at finding them. [^62]

Now the limit, and it is not small. ==None of this was demonstrably run on the public artifact.== The repository carries no CI workflow, no build badge, and no published Comparator transcript, so the claim that these certificates compile and pass is currently OpenAI attesting to its own unpublished run. [^2] Comparator's guarantee is itself conditional — three guarantees resting on six stated assumptions, including that nothing escaped the sandbox and that the kernels are correct. [^14] A reader can reproduce the run; nobody has published having done so.

This matters because it fixes the argument's boundary. Everything above establishes that *if* the theorem statement says what a mathematician thinks it says, the proof is real. Whether it does is a different question entirely — and it is the one that decides what the release is worth.

## 03. Where the trust actually lives

Everything Comparator checks is downstream of a choice it cannot check — what the theorem says — and in these certificates almost every load-bearing definition was written by the same party that wrote the proof.

Open any of the Astra challenge files and the shape is immediate. Each one imports exactly one thing, `import Mathlib`, and then declares its entire mathematical vocabulary locally. `SpherePackingConstant`, `SpherePacking`, `FullAdmissible` and `fullLinearProgram` are all defined inside `A_SpherePacking.lean`; `IsICC`, `HasKazhdanPropertyT`, `vonNeumannClosure`, `groupVonNeumannAlgebra` and `ConnesRigidityAssertion` are all defined inside `E_ConnesRigidity.lean`. Not one of them is a mathlib notion. [^5,6] The kernel then does exactly what it advertises: it certifies that the proof term inhabits *that* proposition, from three axioms, with no `sorry`. It has nothing to say about whether that proposition is the one the press release named.

This is not evidence of bad faith, and it is important to say so plainly. Mathlib has no soficity, no arithmetic-circuit complexity, and no II₁-factor rigidity theory. A team attacking those problems in Lean has no alternative but to build the vocabulary in-file. The consequence is structural rather than moral: it relocates the trust surface off the machine-checked proof and onto human review of the bespoke definitions — around ten in the sphere-packing challenge file and around fifteen in the Connes one. [^5,6] The verification is real; it has simply been performed on a different object than the reader assumes.

Comparator's own maintainers say this out loud. The README concedes that "many definition hole challenges can be gamed without additional oversight," and that such solutions "**must** always be checked with an additional (potentially human) verifier." The worked example is a solver who defines `ChallengeSolution := RiemannHypothesis` and discharges the goal by reflexivity — a certificate that passes every mechanical check and proves nothing. [^14] The Lean 4 reference manual makes the same point from the other end, listing among the issues that *remain* after every mechanical check has passed: [^16]

:::quote(attr="Lean 4 reference manual, Validating proofs")
No human error or misleading presentation of the theorem statement in the trusted challenge file.
:::

Terence Tao's Erdős-problems wiki names the two exploits precisely: "1) introduction of unproved axioms; 2) misformalization of the problem statement," with the practical advice that a proof which "looks suspiciously trivial" deserves a second look. [^24] Comparator's axiom audit closes the first exploit completely. Nothing in the pipeline closes the second.

### The Buzzard asymmetry

The reason this is usually a non-issue in practice — and the reason it is an issue here — is visible in a single anecdote. Kevin Buzzard checked a 1,076-line AI-generated Lean counterexample in "under 5 minutes in total." He could do that only because the statement used "only concepts in mathlib," so `HopfAlgebra` "can be trusted to mean what mathematicians think of as Hopf algebras." [^23] Statement review is cheap when the vocabulary is a community-audited commons; the reviewer reads one line and inherits ten years of other people's scrutiny. Exactly that precondition fails for the Astra certificates. A reader of `E_ConnesRigidity.lean` must independently convince themselves that `vonNeumannClosure` is the bicommutant, that `HasKazhdanPropertyT` is property (T), and that `ConnesRigidityAssertion` is Connes's conjecture — three acts of mathematical judgment the kernel cannot assist with.

How often does that judgment fail? The only available measurements come from benchmark audits, and they are not reassuring. These are rates at which formal statements were judged to *faithfully* encode the informal statements they claim to represent — higher is better, and none is near 100%. [^41,42,44]

:::rank-list
- {label: "miniF2F Lean 4 gold statements judged correct", value: "82.8%", pct: 83}
- {label: "miniF2F Isabelle/HOL gold statements judged correct", value: "76.6%", pct: 77}
- {label: "ProofNet Lean 4 gold statements judged correct", value: "64.8%", pct: 65}
- {label: "MATH-500 auto-formalized statements faithful (manual audit)", value: "43%", pct: 43}
- {label: "miniF2F end-to-end pipeline accuracy", value: "36%", pct: 36}
:::

Those are *gold* statements — hand-curated reference formalizations — failing at roughly one in five on the best-studied benchmark and one in three on ProofNet. [^42] Auto-formalized statements audited manually were faithful 43% of the time. [^44] A corpus audit across five Lean benchmarks reported 4,833 findings, including 398 mechanically certified issues: counterexamples, vacuous theorems, unsound axioms. [^40] And the failure modes are not subtle-in-hindsight, they are load-bearing: a LeanMarathon run formalizing OpenAI's own May 2026 unit-distance disproof "faked the number theory: it modeled a number field as a dummy record and discharged the key step with placeholder values," which the authors summarised as "This type-checks and passes CI, but proves nothing real." In the same run, a misformalized invariant for Erdős #164 "was satisfied by the trivial identity kernel `P n m = [n=m]`, so it constrained nothing." [^39]

### An audit that came back clean

It is worth showing what this review looks like when it goes the other way, because the most suspicious-looking thing in the release turns out to be fine. `ConnesRigidityAssertion` quantifies over all Γ and Λ but imposes ICC and Kazhdan property (T) on Γ only, while also *concluding* that Λ is ICC. [^6] Read cold, that is exactly the shape of a weakened statement: drop a hypothesis, add a conclusion, and a universally quantified claim becomes easier to refute. The natural suspicion is that `connesRigidityAssertion_false` refutes something less than the conjecture operator-algebraists care about.

It does not, and the reason is a piece of domain knowledge no checker holds. Connes's rigidity conjecture is *standardly* stated in precisely this one-sided form — that any ICC property (T) group G is W*-superrigid, meaning that for an arbitrary group H, an isomorphism of the group von Neumann algebras forces G ≅ H. [^75] The missing hypotheses on Λ are not assumed away; they are recovered, because Murray–von Neumann make "L(G) is a factor" equivalent to G being ICC and Connes–Jones make property (T) a W*-invariant. For the same reason the extra conclusion is not a strengthening at all: ICC is a group-isomorphism invariant, so `IsICC Λ ∧ GroupsIsomorphic Γ Λ` says no more than `GroupsIsomorphic Γ Λ` once Γ is ICC. The formalization is faithful. One narrower observation survives — `propertyTGroupFactorCounterexample`, the witness bundling all eight conditions, is a `def` and does not appear in the JSON's `theorem_names`, so it sits outside the independently checked perimeter — but since the conditions are mathematically implied, that is bookkeeping rather than a gap. [^7]

The file rewards close reading in the other direction too. `TracialGroupFactorsIsomorphic` demands a trace-preserving star-isomorphism, a *stronger* hypothesis that makes refutation formally harder, and `vonNeumannClosure` is a genuine bicommutant construction on ℓ²(G) rather than the algebraic group ring. [^6] The sphere-packing file is similarly clean: `occupiedBallRegion` uses balls of radius `separation/2`, the density is the standard limsup of a ball ratio, and the base `√(e/2π)` matches the advertised Cohn–Elkies threshold. [^5] Whoever wrote these was not cutting corners.

That result cuts against this section's own argument, and it should. But notice what it took to establish: two papers stating the conjecture in its canonical form, and two classical equivalences from operator-algebra theory that a reader has to already know to apply. [^75] The kernel supplied none of it. That is the whole thesis in one example — the check is real, it is cheap for a specialist, and there is no mechanical substitute for the specialist.

The honest counterpoint is that the rates above come from competition-level benchmarks with mass-produced statements, not from a hand-built research formalization a team spent weeks on. They set an order-of-magnitude prior, not an estimate for this artifact. And there is no well-documented case of a *published* machine-checked result later overturned because its statement was wrong — the defensible claim is that the base rate here is unmeasured, not that it is high. What is measurable is who looked: OpenAI's own `formalization.yaml` records the review status as `agent-reviewed` — reviewed by a model, not by mathematicians. [^3] That matters because the one check the kernel provably cannot perform is the only one that has not yet been performed by a human expert.

## 04. Grading the ten against prior art

Taken one at a time, the ten results are not one thing — they range from a genuine first improvement to a 48-year-old exponent to a bound that will not beat the classical one until k is around 10^60.

| Result | Prior best | Astra claim | Size of the step |
|---|---|---|---|
| Sphere packing | KL exponent `0.59905576`, 1978 [^45] | Exponent `0.60440`, decay base `√(e/2π)` [^13] | Real, but 0.9% of the exponent |
| Binary/spherical codes | Second MRRW, 1977 [^55] | Strict beat at every minimum distance [^13] | Exponential in principle; 1.08% measured |
| Ehrhart volume conjecture | Order `4^d` in general [^54] | Sharp `(n+1)^n/n!` [^9,13] | Exponential gap closed to sharp |
| Ramsey `R(3;k)` / Erdős 183 | `380^(k/5)`, base ≈ 3.2806 [^26] | Superexponential; `log R = Θ(k log k)` [^8] | Decisive; numerically inert to k ≈ 10^60 |
| Erdős 146 + 180 | `O(n^(2−1/4r))` [^27]; folklore forest example [^28] | Both disproved [^10,11] | Conjectures flipped, not bounds improved |
| Permanent formula bound | Kalorkoti `Ω(n^3)`, early 1980s [^52] | `n^4/log n` [^1] | Attains the classical ceiling [^53] |
| Quantum parallel repetition | Yuen `c·n^(−1/4)·log n` [^48] | Exponential, two-player [^1] | Cleanest outright close, if general |
| Closest vector problem | `n^(c/log log n)`, sub-polynomial [^50] | Polynomial-factor hardness [^1] | Category jump, but unspecified [^51] |
| Non-sofic groups | Existence open as of April 2026 [^72] | A finitely presented example [^13] | New object; no prior number to beat |
| Connes rigidity | Open since ≈1980 [^75] | Disproof [^7] | Flipped; formal statement checks out |

Sphere packing is the headline, and it is the one to read most carefully. Keep two numbers apart: the packing density decays like `b^d`, and the *base* `b` the new theorem pins is `√(e/2π)` ≈ 0.6577, which corresponds to a base-2 *exponent* of `½·log₂(2π/e)` ≈ 0.60440. It is that exponent — not the base — that beats Kabatiansky–Levenshtein's `0.59905576`. [^13] The KL exponent had stood since 1978; every intervening gain — Cohn–Zhao, Sardari–Zargar's factor of 0.4325 — was constant-factor, leaving the exponent untouched. [^45] OpenAI's manuscript claims this as "the first improvement since 1978 to the general sphere-packing exponent," a gap of 48 years. [^13] But the improvement is 0.9% of the exponent: a factor of `2^(0.0054d)`, roughly 43× at d = 1000, against an upper/lower gap that remains exponential — the best lower bound is order `d^2·2^(-d)` (Klartag 2025), leaving about `2^(0.3956d)` unaccounted. [^46]

:::compare
- {role: LOWEST, name: "Kabatiansky–Levenshtein 1978", value: "0.59906"}
- {role: HIGHEST, name: "Cohn–Elkies LP limit (conjectured 2020)", value: "0.60440"}
- {role: SUBJECT, name: "Astra, proved 2026", value: "0.60440"}
:::

The subject card and the ceiling card carry the same number, and that is the point: the target was already known. Afkhami-Jeddi, Cohn, Hartman, de Laat and Tajdini conjectured this exact value numerically in 2020 via the modular bootstrap. [^47] Astra closed a conjecture; it did not discover where to aim.

Codes are the structurally hardest of the ten and the most under-quantified. Samorodnitsky's integrality gap means the plain Delsarte LP can never beat the second MRRW bound, so any improvement has to escape the LP through a hierarchy — and Astra claims exactly that, a strict separation below the classical bound at every fixed minimum distance. [^55,13] A strict separation is genuinely exponential in the block length. Yet the manuscript quantifies the gap at a single point, the kissing number, where level 2 of the hierarchy gives exponent 0.39661 against the classical optimized 0.400944 — 1.08%. [^13] Ehrhart is the largest clean win: the general bound was order `4^d` against a conjectured `(d+1)^d/d!` ≈ `e^d`, an exponential gap of about `1.47^d`, and the Lean statement bounds `normalizedVolume S` by `((n : ℝ) + 1) ^ n / (n.factorial : ℝ)` under five explicit hypotheses. [^54,9] Sharp constant, exponentially wrong predecessor.

Erdős 183 is where "resolves a conjecture" and "improves a number" come apart most violently. The prior lower bound for multicolour Ramsey was exponential, `R(3;k) ≥ 380^(k/5) − O(1)`, base ≈ 3.2806, from Schur-number work (Ageron et al. 2021); Erdős offered $250 for the limit of `R(3;k)^(1/k)` and $100 merely for proving it finite. [^26] Astra's superexponential lower bound has base `k^(1/3)/(6e^38·log k)`, which forces `R(3;k)^(1/k)` to diverge, answering the $100 question negatively and pinning `log R` to `Θ(k log k)`. [^8] That is decisive. It is also numerically inert: with `e^38` ≈ 3.19×10^16 in the denominator, the new base does not overtake 3.2806 until k reaches roughly 10^60 — this article's own arithmetic from the constant in the Lean statement, not a figure OpenAI published. [^8] For every k a combinatorialist will ever write down, the 2021 bound is still the better number.

Two results are disproofs rather than improvements — the Lean theorems are literally named `not_erdos_146` and `not_erdos_180`. [^11,10] For 146 ($500), a connected bipartite 2-degenerate H with `ex(n,H) ≥ c·n^(3/2+ε)` breaks the conjectured `O(n^(3/2))` at r = 2, where the prior best was only Alon–Krivelevich–Sudakov's weaker `O(n^(2−1/4r))`. [^27] For 180, the counterexample sits at exponent `21/16 = 4/3 − 1/48` on families required to be connected, bipartite and non-acyclic — a real strengthening, since 180's general form already had a folklore forest counterexample. [^28] Worth recording: erdosproblems.com still listed 183, 146 and 180 as OPEN with no AI attribution, last edited 2026-04-10 and 2026-01-18. [^26,27,28] Those pages predate the announcement, so this is lag, not dissent — but as of 1 August 2026 the field's registrar had ratified none of the three.

The complexity-theoretic three are the softest. OpenAI's "arithmetic-formula lower bound of order n 4/log n" must mean `n^4/log n`, since `n^(4/log n)` is the constant `e^4` and bounds nothing. [^1] Against Kalorkoti's `Ω(n^3)` formula-size bound for the determinant, which transfers to the permanent and dates to the early 1980s, that is a real `n/log n` gain after four decades — but in the variable count `N = n^2` it is exactly `N^2/log N`, the known ceiling of the Nechiporuk–Kalorkoti technique. It reaches the classical method's limit rather than escaping it, and stays far from what Valiant's conjecture requires. [^52,53] Quantum parallel repetition may be the cleanest of the ten: exponential decay was known only for anchored or free games, and Bavarian–Vidick–Yuen amplify a *transformed* game, not the original, so a general two-player exponential theorem closes a well-posed decade-old problem outright. [^48,49,1] CVP is unjudgeable as stated: moving from `n^(c/log log n)` — sub-polynomial, slower than `n^ε` for every positive ε — to a polynomial factor is a category jump, but the announcement names neither exponent nor hardness assumption, and Aharonov–Regev put `√n`-approximation in NP ∩ coNP, capping any NP-hardness below exponent ½. [^50,51]

The last two claim objects, not bounds. The specialist literature treated non-sofic existence as ==open as recently as 2026, on a preprint whose full text could not be re-read to confirm the wording quoted here== — and Astra's Lean target is stronger than Gromov's bare question, asserting a *finitely presented* example. [^72] Keep three things distinct that coverage will blur: Connes's embedding problem was refuted by `MIP*=RE` in 2020, that left the sofic question open, and Connes's rigidity conjecture is a third problem again. [^73] The rigidity disproof claims a conjecture standing since Connes posed it around 1980 — that every ICC group with property (T) is W*-superrigid, so that its group von Neumann algebra determines it up to isomorphism. [^75] The Lean development refutes exactly that assertion, and it is by some distance the largest artifact in the release. [^7]

The obvious way this grading is wrong: no arXiv preprint or ECCC report exists for any of the ten — there are one-line summaries, a manuscripts PDF, and the Lean certificates. [^13] Grading a press-release sentence is bad practice, and several of these, CVP and the permanent bound especially, will read differently once the manuscripts are worked through. This matters because the ten will be reported as one event with one size, and they are not: a sharp Ehrhart constant, a 0.9% exponent gain, and a bound that becomes better than its predecessor at k ≈ 10^59 are three different kinds of claim wearing the same headline.

## 05. The $2,000 number, and the denominator it hides

OpenAI's release note contains one sentence that travelled further than any other: "The total number of tokens needed to find solutions to these problems would cost roughly $2,000 at Sol API rates." [^1] The headline cost figure is the most quoted number in the release and the least informative — it prices the winning tickets and omits how many were bought.

:::stats
- {label: "Stated cost, all ten", value: "$2,000", note: "at Sol API rates"}
- {label: "Implied cost per result", value: "~$200", note: "if the ten are the denominator"}
- {label: "Implied token volume", value: "67–400M", note: "at $30/$5 per Mtok out/in"}
- {label: "Attempts disclosed", value: "0", note: "no problems-attempted figure"}
:::

Read the sentence as a measurement claim and three things fall out of it. First, it is a counterfactual repricing rather than a bill: Astra is unreleased and unpriced, so the figure is what the token volume *would have* cost had it been produced by Sol, a different and already-shipped model. [^1] Second, "tokens needed to find solutions" scopes the accounting to the search runs that landed. That is a marginal cost per success, not a total cost per success — the difference between the price of a winning lottery ticket and the price of playing. Third, the figure excludes training amortisation, the human manuscript preparation, and the Lean formalisation labour, all of which OpenAI acknowledges took place. [^1] None of those three is a gotcha. Each is a defensible scoping choice. Together they mean the number answers a much narrower question than the one readers think they are asking.

The arithmetic is worth doing, because it points the same way. OpenAI's published Sol rates are $5.00 per million input tokens and $30.00 per million output tokens as of 1 August 2026; $2,000 buys 66.7M output tokens at the top rate, or 400M input tokens at the bottom, and a reasoning-heavy proof search is output-dominated — so the realistic band is roughly 67–100M tokens for all ten results. [^65] That is a startlingly *small* budget for ten decade-old conjectures. The correct inference from a suspiciously efficient number is not that the efficiency is remarkable; it is that the accounting boundary is narrow.

The decisive comparison is not with a human but with the nearest lab. DeepMind published its denominator: its most capable formal proof-search agent autonomously resolved 9 of 353 open Erdős problems — a hit rate near 2.5% — at "the per-problem cost of a few hundred dollars." [^36] So OpenAI's implied ~$200 per result is not better than the published comparable. It sits inside the same band while omitting the one quantity DeepMind chose to disclose. If Astra attempted N problems and ten landed, the honest figure is (N/10) times the marginal cost, and nobody outside OpenAI can supply N.

That the harness matters as much as the model is now measurable. An independent First Proof consortium ran four systems — three research harnesses plus one commercial product — over ten research-level problems of its own, and recorded totals from $117 to $4,799, a spread of roughly 40× on identical work, as of its published run in June 2026. One of the four figures is imputed rather than billed. [^66]

:::bars
- {label: "System B", value: "$4,799", pct: 100}
- {label: "System A", value: "$3,186", pct: 66}
- {label: "System D (imputed)", value: "$1,014", pct: 21}
- {label: "System C", value: "$117", pct: 2}
:::

Terence Tao cited the same dataset in his ICM 2026 lecture on 24 July 2026, as costs ranging from 10 to 1,000 USD per problem. [^76] Against that variance, any single headline price without its harness and its attempt count is close to uninterpretable. The critique also predates the release: Melanie Matchett Wood had already noted that OpenAI does not share the cases where its model failed on an open problem, or produced an incorrect solution with flawed reasoning. [^71] Within an hour of publication the top objection in the first Hacker News thread was not mathematical at all but "the lack of transparency around the total experiment and construction," with one commenter likening the $2,000 figure to p-hacking. [^64]

The human comparator, which coverage reached for immediately, does not rescue the number either. The US Bureau of Labor Statistics puts the median mathematician wage at $121,680 as of May 2024 — but that occupation code covers roughly 16,000 applied mathematicians in defence, finance and government, not the academic pure mathematicians who work on open conjectures, so it is very likely the wrong population. [^67] The deeper problem is that the comparison is malformed in kind: a salary buys a year, not a result. Resolving a decade-old conjecture is a rare event in an academic career, so the per-open-problem human cost is a salary divided by a success probability nobody has estimated. Any clean ratio quoted anywhere was manufactured.

The counterpoint deserves equal weight. Omission is not proof of exaggeration. Ten Lean-certified results at any price is a real deliverable; a false positive is far harder to sustain when a machine-checkable certificate ships alongside it; and no lab publishes its failures by default — DeepMind's disclosure is the exception, not the norm. The criticism here is about *selection*, not correctness. Ten successes with an unstated denominator say nothing about reliability in either direction.

Why it matters: the cost figure is the only part of the release a non-mathematician can evaluate, and it is the part nobody can reproduce. Astra is not externally runnable and remains a tentative codename — OpenAI has not decided whether to ship it as GPT-6, GPT-5.7, or a separate class — so no outside party can rerun the search or price it. [^68] Meanwhile Axiom Math raised $200M at a valuation above $1.6B in March 2026 to work on formal mathematics. [^69] When that much capital rides on the narrative, an unfalsifiable per-result price should be read as positioning until a denominator arrives.

## 06. Who is qualified to check this, and will they

As of roughly five hours after the announcement, a search of the obvious venues for this article turned up no named mathematician or proof-assistant expert who had publicly inspected the artifacts. Terence Tao's Mathstodon carried nothing on Astra; Buzzard's Xena blog and Gowers's blog were both still on July posts; no Lean Zulip, r/math or Bluesky thread on the release was indexed; and in the first Hacker News thread no commenter claimed to have compiled the repository or reproduced anything. [^61,64,23] That absence needs reading carefully — it is a timing fact about an hours-old release, not evidence of doubt. The honest reading of an empty comment section at hour five is that the relevant experts were asleep. But it does isolate the question the certificate cannot answer for itself, and that question is this section's thesis: {accent}the certificate moves the bottleneck rather than removing it — from "can anyone verify the proof" to "will anyone with the right expertise spend a week reading definitions for no professional credit."{/}

Mathematics has already started building vocabulary for this exact state. The community wiki tracking AI contributions to Erdős problems tags entries with a `(Lean)` qualifier — "Partial result (Lean)" and similar — separating what a machine has certified from what the field has absorbed, and it keeps distinct buckets for AI work later found redundant with existing literature and for AI work found outright incorrect. [^25] The distinction is not a slur. It is an accounting entry recording that one of two independent checks has cleared and the other has not started, which is precisely where the ten Astra results sit.

The scarce resource is the second check, and mathlib gives us the only honest empirical measure of it. The library holds roughly 283,758 theorems from 772 contributors, and its own roadmap names the review backlog "the primary constraint on Mathlib's growth" — about 300 open pull requests against a median wait around two weeks, as of the 2026 roadmap snapshot. [^20,56] The nuance matters more than the number. Those are *library-integration* reviews, not correctness reviews; Lean's kernel already certifies correctness, so nobody is re-deriving the logic by hand. What the queue is actually rationing is expert judgment about significance and fidelity — does this statement say what it claims to say, do these definitions mean what their names imply, is this worth carrying. That is exactly what the Astra results need, and exactly what no kernel supplies.

The precedent for how long that second check takes is not encouraging, and it is not speculative. [^57,58,1]

:::timeline
- {date: "1976", headline: "Four Colour Theorem", body: "Appel and Haken's computer-assisted proof is accepted but distrusted, because the case analysis at its core was never checked by hand."}
- {date: "1998", headline: "Kepler submitted", body: "Hales submits his sphere-packing proof to Annals of Mathematics."}
- {date: "2003", headline: "Referees give up", body: "After four years the twelve-member Kepler panel certifies only 99% confidence, unable to check every computer calculation. The paper is published in 2005, seven years after submission."}
- {date: "2005", headline: "Four Colour, formalized", body: "Gonthier and Werner's Coq formalization removes the trust dependency that had dogged Appel–Haken for 29 years."}
- {date: "2014", headline: "Flyspeck completes", body: "Formal verification of the Kepler proof finishes after eleven and a half years of collaborative work."}
- {date: "2017", headline: "Flyspeck published", body: "The formal proof appears in Forum of Mathematics, Pi — three further years of ordinary refereeing, despite the machine certificate."}
- {date: "2026-08-01", headline: "Ten certificates, no paper", body: "OpenAI publishes ten results with Lean certificates, no named authors, no preprint, and no journal submission."}
:::

Flyspeck is the load-bearing case, and its lesson is the opposite of the one usually drawn from it. Hales's Kepler proof took about seven years from submission to acceptance and its referee panel formally gave up, certifying only 99% confidence; Flyspeck — launched *because* of that refereeing failure — then took eleven and a half years to formalise it. [^58] The part everyone forgets is the coda: once the machine certificate existed, Forum of Mathematics, Pi refereed the formal proof for roughly three more years anyway. The certificate did not shorten the social process. It changed what the referees argued about. The earlier precedent runs the same way — Appel–Haken 1976 was accepted but distrusted for 29 years until Gonthier's Coq formalization removed the trust dependency, and even then the trust base shifted to the Coq kernel rather than vanishing. [^57] A certificate is evidence submitted to a community, not a substitute for one.

There is also a hard institutional wall between these results and the literature, and it is not mathematical.

:::quote(attr="The Leiden Declaration, 2 June 2026")
Credit and responsibility continue to belong to humans within the mathematical community and should not be given to automated systems.
:::

arXiv forbids listing generative AI as an author and requires each human signatory to "individually take full responsibility for all its contents, irrespective of how the contents were generated"; COPE's position is that "AI tools cannot meet the requirements for authorship as they cannot take responsibility for the submitted work." [^59,60] OpenAI's formula — "we take responsibility for their correctness" — asserts *corporate* rather than *individual* accountability, which is precisely the gap those policies exist to close. [^1] The binding constraint on getting Astra's ten into the literature is finding a named human willing to sign. And arXiv has already shown it will raise gates against machine-generated volume: in October 2025 its computer-science category stopped accepting review articles and position papers without prior peer review, citing generative AI making such papers "fast and easy to write." [^70] The Leiden Declaration — 3,340 signatories as of its 2 June 2026 publication, endorsed by the International Mathematical Union — separately warns that evaluation suffers when findings arrive through "informal channels such as press releases or blog posts, often without any research paper," and tells policymakers "Don't believe the hype," citing "a strong commercial incentive on the part of the technology industry to overstate the capabilities of their products." [^29] OpenAI supplied the formalization and skipped the paper.

The counterpoint is strong enough that the pessimistic reading is probably wrong on timing. It assumes nobody will look, and the incentives point the other way: ten machine-checked claims against famous conjectures are unusually attractive targets, the artifacts are public and Apache-licensed, a refutation would be career-making, and the check is *bounded* — read a dozen definitions and run `lake build` — rather than open-ended. The community's terms have already shifted toward accepting formal artifacts, with Buzzard now asking for Lean rather than prose and Lean's creator Leonardo de Moura presenting multi-kernel re-checking at FLoC 2026. [^23,62] So a better prediction than "nobody will verify" is that verification arrives in days while attribution and publication take years — which is precisely the Flyspeck shape, compressed at the front and unchanged at the back.

This matters because the two halves get reported as one. A repository that compiles is a fact available within hours; a result the field has read, credited, and built on is a process measured in years — and conflating them is how a genuine advance gets sold as a larger one than it is.

## 07. What would have to be true for this to be wrong

Every argument above rests on a small number of load-bearing claims, and each has a specific way of failing. Setting those out is more useful than a verdict, because within weeks the evidence that decides them will exist.

This article could be too harsh in three ways. First, the statement-fidelity worry is quantified only by benchmark data — competition problems with mass-produced formalizations — and there is no documented case of a published machine-checked mathematical result later overturned because its statement was wrong. [^41,42,44] The correct summary is that the base rate is *unmeasured*, not that it is high, and a research team that spent weeks on a hand-built formalization is not the population those benchmarks sampled. Second, the Astra definitions that could be read hold up. `vonNeumannClosure` is a real bicommutant; `occupiedBallRegion` uses the right radius; `TracialGroupFactorsIsomorphic` is stronger than the conjecture requires, which makes refutation harder rather than easier. [^5,6] That is the signature of careful work, not of gaming. Third, the verification stack is genuinely better than the field's norm: an axiom allowlist, a sandboxed build, and independent kernel replay through nanoda catch every documented attack short of misformalization — including the string-concatenated `axiom` that FormalQualBench recorded models attempting. [^63,21]

And it could be too generous in three ways. The `agent-reviewed` field in `formalization.yaml` means no human signed off on the formalization inside OpenAI either, which is a stronger admission than the announcement's careful language suggests. [^3] The absence of CI means the only evidence these certificates compile is an unpublished internal run. [^2] And the fidelity question was closed here for exactly one result out of twelve, on the two files small enough to read end to end; the remaining certificates run to megabytes apiece, and if a specialist finds that any one of their bespoke definitions is non-standard or vacuous, that result collapses regardless of how many kernels replayed the proof. [^5,6]

An earlier draft of this article asserted that the Connes formalization refuted a weaker statement than the conjecture proper. An adversarial check killed that claim: the one-sided form is the canonical statement. [^75] The correction is worth flagging rather than quietly absorbing, because it is evidence for the optimistic reading — the suspicious-looking case was resolvable in an afternoon by someone who knew where to look.

The clean falsification tests, in rough order of how fast they should resolve:

:::callout(kind=warn, label="What to watch")
- **Does `lake build All` succeed on a clean machine?** Resolvable in a day by anyone with Lean 4.32.0. Nobody had published a reproduction as of 1 August 2026. [^2,64]
- **Does `#print axioms` come back clean on the named theorems?** The configs *declare* the three-axiom allowlist; declaring is not running. [^4,3]
- **Do specialists accept the bespoke definitions in the eight unread certificates?** The two files checked here hold up; `GapCVP.lean` alone runs to megabytes and nobody has read it. [^5,6]
- **Does erdosproblems.com move 146, 180 and 183 out of OPEN?** Thomas Bloom's registrar is the field's de-facto adjudicator, and it had ratified none of the three. [^26,27,28]
- **Does a denominator appear?** Ten successes with no attempt count is not a rate, and DeepMind has shown that publishing one is possible. [^36]
:::

The most likely outcome, judged from the two nearest precedents, is neither vindication nor collapse. When OpenAI disproved the unit-distance conjecture in May 2026 the result survived — but only after nine named mathematicians digested and simplified it, and a later attempt to formalize that same disproof produced a development that passed CI while proving nothing. [^38,39] When DeepMind's agent resolved 9 of 353 Erdős problems, the striking finding buried in its own paper was that a much simpler generate-and-verify baseline replicated those successes, proving costlier only on the hardest problems — the scaffolding bought efficiency more than capability. [^36] A comparable pattern showed up in AlphaEvolve, which improved the state of the art on a minority of the open problems it was pointed at and merely rediscovered the known optimum on most of them. [^37] All three point the same way: the mathematics is probably substantially right, the framing is probably somewhat oversold, and the gap between "a repository compiles" and "the field has absorbed a result" will be measured in years rather than the news cycle the announcement was written for.

There is a version of this story that is straightforwardly good news, and it deserves the last word. Machine-checkable output is the only mechanism anyone has proposed that lets a field absorb more mathematics than it can referee, and Buzzard's five-minute check is the proof of concept: when the vocabulary is shared, verification collapses from months to minutes. [^23] The bottleneck the Astra release exposes is not that certificates are worthless. It is that their value scales with how much of the statement is written in a language the community already audits — and the frontier results, by construction, are the ones where that language does not exist yet. Extending mathlib is unglamorous, slow, and currently rate-limited by about 300 pull requests in a review queue. [^56] It is also, on this evidence, the binding constraint on whether any of this becomes knowledge.

:::references
- {id: 1, title: "Ten advances in mathematics and theoretical computer science", url: "https://openai.com/index/ten-advances-in-mathematics/", source: OpenAI, date: "2026-08-01"}
- {id: 2, title: "openai/ten-proofs — Lean certificates repository", url: "https://github.com/openai/ten-proofs", source: GitHub, date: "2026-08-01"}
- {id: 3, title: "openai/ten-proofs — formalization.yaml", url: "https://raw.githubusercontent.com/openai/ten-proofs/main/formalization.yaml", source: GitHub, date: "2026-08-01"}
- {id: 4, title: "ComparatorChallenges/A_SpherePacking.json", url: "https://raw.githubusercontent.com/openai/ten-proofs/main/ComparatorChallenges/A_SpherePacking.json", source: GitHub, date: "2026-08-01"}
- {id: 5, title: "ComparatorChallenges/A_SpherePacking.lean", url: "https://raw.githubusercontent.com/openai/ten-proofs/main/ComparatorChallenges/A_SpherePacking.lean", source: GitHub, date: "2026-08-01"}
- {id: 6, title: "ComparatorChallenges/E_ConnesRigidity.lean", url: "https://raw.githubusercontent.com/openai/ten-proofs/main/ComparatorChallenges/E_ConnesRigidity.lean", source: GitHub, date: "2026-08-01"}
- {id: 7, title: "ConnesRigidity/Main.lean", url: "https://raw.githubusercontent.com/openai/ten-proofs/main/ConnesRigidity/Main.lean", source: GitHub, date: "2026-08-01"}
- {id: 8, title: "ComparatorChallenges/I_MulticolorTriangleRamsey.lean", url: "https://raw.githubusercontent.com/openai/ten-proofs/main/ComparatorChallenges/I_MulticolorTriangleRamsey.lean", source: GitHub, date: "2026-08-01"}
- {id: 9, title: "ComparatorChallenges/F_EhrhartVolumeInequality.lean", url: "https://raw.githubusercontent.com/openai/ten-proofs/main/ComparatorChallenges/F_EhrhartVolumeInequality.lean", source: GitHub, date: "2026-08-01"}
- {id: 10, title: "ComparatorChallenges/J_CompactnessConjecture.lean", url: "https://raw.githubusercontent.com/openai/ten-proofs/main/ComparatorChallenges/J_CompactnessConjecture.lean", source: GitHub, date: "2026-08-01"}
- {id: 11, title: "ComparatorChallenges/J_TwoDegenerateGraphs.lean", url: "https://raw.githubusercontent.com/openai/ten-proofs/main/ComparatorChallenges/J_TwoDegenerateGraphs.lean", source: GitHub, date: "2026-08-01"}
- {id: 12, title: "openai/ten-proofs — lake-manifest.json", url: "https://raw.githubusercontent.com/openai/ten-proofs/main/lake-manifest.json", source: GitHub, date: "2026-08-01"}
- {id: 13, title: "Ten advances — companion manuscripts (PDF)", url: "https://cdn.openai.com/pdf/ten-proofs-oai.pdf", source: OpenAI, date: "2026-08-01"}
- {id: 14, title: "leanprover/comparator — README", url: "https://raw.githubusercontent.com/leanprover/comparator/master/README.md", source: "Lean FRO", date: "2026-08-01"}
- {id: 15, title: "comparator issue #59 — statement comparison is not proof-irrelevant", url: "https://github.com/leanprover/comparator/issues/59", source: GitHub, date: "2026-07-17"}
- {id: 16, title: "Lean 4 reference manual — Validating proofs", url: "https://lean-lang.org/doc/reference/latest/ValidatingProofs/", source: "Lean FRO", date: "2026-08-01"}
- {id: 17, title: "Lean 4 — Init/Core.lean (native_decide docstring)", url: "https://github.com/leanprover/lean4/blob/master/src/Init/Core.lean", source: GitHub, date: "2026-08-01"}
- {id: 18, title: "leanprover/lean4 issue #14576 — proving False via the checked addDecl path", url: "https://github.com/leanprover/lean4/issues/14576", source: GitHub, date: "2026-07-28"}
- {id: 19, title: "leanprover/lean4 issue #7463 — csimp can smuggle an axiom past #print axioms", url: "https://github.com/leanprover/lean4/issues/7463", source: GitHub, date: "2025-03-12"}
- {id: 20, title: "Mathlib statistics", url: "https://leanprover-community.github.io/mathlib_stats.html", source: "leanprover-community", date: "2026-08-01"}
- {id: 21, title: "ammkrn/nanoda_lib — an independent Lean kernel in Rust", url: "https://github.com/ammkrn/nanoda_lib", source: GitHub, date: "2026-08-01"}
- {id: 22, title: "Zouuup/landrun — Landlock-based sandbox", url: "https://github.com/Zouuup/landrun", source: GitHub, date: "2026-08-01"}
- {id: 23, title: "Human mathematicians are being outcounterexampled", url: "https://xenaproject.wordpress.com/2026/07/20/human-mathematicians-are-being-outcounterexampled/", source: "Kevin Buzzard, Xena Project", date: "2026-07-20"}
- {id: 24, title: "Erdős problems wiki — Disclaimers and caveats", url: "https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats", source: "teorth/erdosproblems", date: "2026-06-30"}
- {id: 25, title: "Erdős problems wiki — AI contributions to Erdős problems", url: "https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems", source: "teorth/erdosproblems", date: "2026-06-30"}
- {id: 26, title: "Erdős problem 183", url: "https://www.erdosproblems.com/183", source: erdosproblems.com, date: "2026-04-10"}
- {id: 27, title: "Erdős problem 146", url: "https://www.erdosproblems.com/146", source: erdosproblems.com, date: "2026-01-18"}
- {id: 28, title: "Erdős problem 180", url: "https://www.erdosproblems.com/180", source: erdosproblems.com, date: "2026-01-18"}
- {id: 29, title: "The Leiden Declaration on mathematics and AI", url: "https://leidendeclaration.ai/", source: leidendeclaration.ai, date: "2026-06-02"}
- {id: 30, title: "Post on ten Erdős problems listed as open", url: "https://x.com/MarkSellke/status/1979226538059931886", source: "Mark Sellke on X", date: "2025-10-17"}
- {id: 31, title: "Post on Erdős problem 339 and literature search", url: "https://x.com/SebastienBubeck/status/1977181716457701775", source: "Sébastien Bubeck on X", date: "2025-10-12"}
- {id: 32, title: "Post announcing ten Astra proofs with Lean certificates", url: "https://x.com/SebastienBubeck/status/2083456300692979886", source: "Sébastien Bubeck on X", date: "2026-08-01"}
- {id: 33, title: "OpenAI researcher deletes tweet claiming GPT-5 solved open problems", url: "https://futurism.com/artificial-intelligence/openai-researcher-deletes-tweet", source: Futurism, date: "2025-10-21"}
- {id: 34, title: "A GPT-5 math breakthrough that never happened", url: "https://the-decoder.com/leading-openai-researcher-announced-a-gpt-5-math-breakthrough-that-never-happened/", source: "The Decoder", date: "2025-10-18"}
- {id: 35, title: "Olympiad-level formal mathematical reasoning with reinforcement learning", url: "https://www.nature.com/articles/s41586-025-09833-y", source: Nature, date: "2025-11-12"}
- {id: 36, title: "AlphaProof Nexus — large-scale evaluation on open problems (arXiv:2605.22763)", url: "https://arxiv.org/abs/2605.22763", source: arXiv, date: "2026-05-21"}
- {id: 37, title: "AlphaEvolve: a Gemini-powered coding agent for designing advanced algorithms", url: "https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/", source: "Google DeepMind", date: "2025-05-14"}
- {id: 38, title: "Remarks on the disproof of the unit distance conjecture (arXiv:2605.20695)", url: "https://arxiv.org/abs/2605.20695", source: arXiv, date: "2026-05-20"}
- {id: 39, title: "LeanMarathon: long-horizon Lean autoformalization (arXiv:2606.05400)", url: "https://arxiv.org/html/2606.05400v1", source: arXiv, date: "2026-06-03"}
- {id: 40, title: "A corpus-scale audit of Lean benchmark defects (arXiv:2606.29493)", url: "https://arxiv.org/html/2606.29493v1", source: arXiv, date: "2026-06-28"}
- {id: 41, title: "miniF2F-v2: repairing formal/informal statement mismatch (arXiv:2511.03108)", url: "https://arxiv.org/abs/2511.03108", source: arXiv, date: "2025-11-04"}
- {id: 42, title: "Auditing reference formalizations with an LLM judge (arXiv:2506.10903)", url: "https://arxiv.org/pdf/2506.10903", source: arXiv, date: "2025-06-12"}
- {id: 43, title: "Verina: a Lean 4 benchmark for verified programming (arXiv:2505.23135)", url: "https://arxiv.org/abs/2505.23135", source: arXiv, date: "2025-05-29"}
- {id: 44, title: "Faithful verification and formal answer selection (arXiv:2605.28365)", url: "https://arxiv.org/html/2605.28365", source: arXiv, date: "2026-05-27"}
- {id: 45, title: "New upper bounds for spherical codes and packings", url: "https://link.springer.com/article/10.1007/s00208-023-02738-z", source: "Mathematische Annalen (Sardari & Zargar)", date: "2024-01-01"}
- {id: 46, title: "Lattice packing of spheres in high dimensions (arXiv:2504.05042)", url: "https://arxiv.org/abs/2504.05042", source: "arXiv (Klartag)", date: "2025-04-07"}
- {id: 47, title: "High-dimensional sphere packing and the modular bootstrap (arXiv:2006.02560)", url: "https://arxiv.org/abs/2006.02560", source: arXiv, date: "2020-12-14"}
- {id: 48, title: "A parallel repetition theorem for all entangled games (arXiv:1604.04340)", url: "https://arxiv.org/abs/1604.04340", source: "arXiv (Yuen)", date: "2016-04-15"}
- {id: 49, title: "Anchoring games for parallel repetition (arXiv:1509.07466)", url: "https://arxiv.org/pdf/1509.07466", source: "arXiv (Bavarian, Vidick & Yuen)", date: "2015-09-24"}
- {id: 50, title: "Approximating CVP to within almost-polynomial factors is NP-hard", url: "https://link.springer.com/article/10.1007/s00493-003-0019-y", source: "Combinatorica (Dinur, Kindler, Raz & Safra)", date: "2003-01-01"}
- {id: 51, title: "Lattice problems in NP intersect coNP", url: "https://cims.nyu.edu/~regev/papers/cvpconp.pdf", source: "Aharonov & Regev", date: "2005-09-08"}
- {id: 52, title: "Lower bounds via degree arguments (formula size of the determinant)", url: "https://link.springer.com/chapter/10.1007/BFb0012780", source: "Kalorkoti", date: "1985-01-01"}
- {id: 53, title: "On the limits of the Nechiporuk method (arXiv:1911.11793)", url: "https://arxiv.org/pdf/1911.11793", source: arXiv, date: "2019-11-26"}
- {id: 54, title: "Ehrhart's volume conjecture", url: "https://en.wikipedia.org/wiki/Ehrhart%27s_volume_conjecture", source: Wikipedia, date: "2026-08-01"}
- {id: 55, title: "The linear-programming hierarchy for linear codes", url: "https://people.cs.uchicago.edu/~csj/publications/LinearCodeLPHierarchy.pdf", source: "University of Chicago", date: "2022-01-01"}
- {id: 56, title: "Mathlib Initiative roadmap", url: "https://mathlib-initiative.org/roadmap/", source: "Mathlib Initiative", date: "2026-08-01"}
- {id: 57, title: "Formal proof — the four-color theorem", url: "https://www.ams.org/notices/200811/tx081101382p.pdf", source: "Notices of the AMS (Gonthier)", date: "2008-11-01"}
- {id: 58, title: "A formal proof of the Kepler conjecture", url: "https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/formal-proof-of-the-kepler-conjecture/78FBD5E1A3D1BCCB8E0D5B0C463C9FBC", source: "Forum of Mathematics, Pi", date: "2017-01-01"}
- {id: 59, title: "arXiv moderation and generative-AI policy", url: "https://info.arxiv.org/help/moderation/index.html", source: arXiv, date: "2023-11-01"}
- {id: 60, title: "Authorship and AI tools — COPE position statement", url: "https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools", source: COPE, date: "2023-02-13"}
- {id: 61, title: "Terence Tao on Mathstodon", url: "https://mathstodon.xyz/@tao", source: mathstodon.xyz, date: "2026-07-31"}
- {id: 62, title: "Lean and trustworthy proof checking — FLoC 2026", url: "https://leodemoura.github.io/static/floc26/", source: "Leonardo de Moura", date: "2026-07-26"}
- {id: 63, title: "FormalQualBench", url: "https://www.math.inc/formalqualbench", source: "Math Inc.", date: "2026-03-19"}
- {id: 64, title: "Discussion: Ten advances in mathematics and theoretical computer science", url: "https://news.ycombinator.com/item?id=49132058", source: "Hacker News", date: "2026-08-01"}
- {id: 65, title: "OpenAI API pricing", url: "https://platform.openai.com/docs/pricing", source: OpenAI, date: "2026-08-01"}
- {id: 66, title: "First Proof: an independent multi-harness evaluation (arXiv:2606.18119)", url: "https://arxiv.org/html/2606.18119v1", source: arXiv, date: "2026-06-16"}
- {id: 67, title: "Mathematicians and Statisticians — Occupational Outlook Handbook", url: "https://www.bls.gov/ooh/math/mathematicians-and-statisticians.htm", source: "US Bureau of Labor Statistics", date: "2025-08-28"}
- {id: 68, title: "Exclusive: OpenAI previews Astra AI model", url: "https://www.theinformation.com/briefings/exclusive-openai-previews-astra-ai-model-dc", source: "The Information", date: "2026-07-31"}
- {id: 69, title: "Verifiable-AI startup Axiom raises $200M", url: "https://siliconangle.com/2026/03/12/verifiable-ai-startup-axiom-raises-200m-prove-ai-generated-code-safe-use/", source: SiliconANGLE, date: "2026-03-12"}
- {id: 70, title: "Updated practice for review articles and position papers in arXiv CS", url: "https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/", source: "arXiv blog", date: "2025-10-31"}
- {id: 71, title: "AI guardrails and an Erdős math problem", url: "https://www.sciencenews.org/article/ai-guardrails-erdos-math-problem", source: "Science News", date: "2026-07-01"}
- {id: 72, title: "On minimal non-sofic and omega-non-sofic groups (arXiv:2604.19174)", url: "https://arxiv.org/pdf/2604.19174", source: arXiv, date: "2026-04-01"}
- {id: 73, title: "Connes' embedding problem and MIP*=RE — a survey (arXiv:2109.12682)", url: "https://arxiv.org/pdf/2109.12682", source: arXiv, date: "2022-01-01"}
- {id: 74, title: "leanprover/lean4checker", url: "https://github.com/leanprover/lean4checker", source: GitHub, date: "2026-08-01"}
- {id: 75, title: "W*-superrigidity for property (T) groups (arXiv:2503.12742)", url: "https://arxiv.org/html/2503.12742", source: "arXiv (Chifan, Fernández Quero, Osin & Tan)", date: "2025-03-17"}
- {id: 76, title: "Mathematics in the age of AI — ICM 2026 lecture slides", url: "https://teorth.github.io/tao-web/slides/age-of-ai-icm-2026.pdf", source: "Terence Tao", date: "2026-07-24"}
:::
