---
eyebrow: RESEARCH · AGENT EVALUATION
title: "The 49-Point Gap: What SWE-bench Science's Visible-Test Scores Hide"
deck: A new scientific-software benchmark pairs a 96.64% public score with a 47.90% Pass@1 on held-out tests. Reading that gap correctly means separating signal, metric design, and failure mechanics.
lede: |
  On 20 August 2026, a team of researchers at the Shanghai Innovation Institute and Fudan University released SWE-bench Science, a repository-level benchmark for scientific software engineering built around a specific measuring idea: show an agent only a small set of "public" diagnostic tests, then grade it on a separately-mounted suite of "private" tests that are never visible during the repair loop [^1]. The headline result sounds like a red flag about benchmark hygiene — Claude Code with Opus-5 (max), the best performer, scores 96.64% on the visible public tests yet only 47.90% Pass@1 on the hidden ones, a ~49-point gap [^1][^2]. But the paper's own framing, and the way the benchmark is constructed, suggest this gap is less a smoking gun of leakage and more a deliberately engineered diagnostic that separates surface-level test-passing from complete private-test correctness. The question worth answering is which reading is right.
stats:
  - {label: "Best agent Pass@1", value: "47.90%", note: "Claude-Opus-5 (max), held-out private tests"}
  - {label: "Same agent, public score", value: "96.64%", note: "visible diagnostic tests"}
  - {label: "Tasks / repos / domains", value: "119 / 98 / 20", note: "20 scientific domains"}
  - {label: "Public-to-private gap", value: "48.74pt", note: "96.64% − 47.90%"}
---

## 01. The Gap Is Real — and It Is an Intentional Part of the Design

The number pair that anchors this analysis comes directly from SWE-bench Science's Table 2 and the paper's conclusion: across eight agent configurations, the strongest result is 47.90% Pass@1, and the same configuration (Claude Code with Opus-5, reasoning at max) attains a 96.64% public score [^1][^2]. The arithmetic is a 48.74-percentage-point gap — the "49-point gap" of the topic line. It is not a statistical accident: the same pattern recurs across the whole leaderboard, not just the top row. DeepSeek-V4-Pro (max) shows a 100.00% public score against a 42.02% overall Pass@1; Qwen3.8-27B (max) is 100.00% public against 29.41%; DeepSeek-V4-flash (high) is 100.00% public against 19.33% [^2]. Every single one of the thirteen listed configurations posts a public score above 93% while only the top model clears 40% on the hidden tests [^1][^2].

:::bar-chart(title="Public score vs. Pass@1 on SWE-bench Science", subtitle="percent of tasks", mode=grouped)
categories: Claude-Opus-5, GPT-5.6-sol, DeepSeek-V4-Pro, Qwen3.8-27B, DeepSeek-V4-flash
Public score: 96.64, 99.16, 100.00, 100.00, 100.00
Pass@1: 47.90, 46.22, 42.02, 29.41, 19.33
:::

The reason the two numbers diverge this much is structural to how the benchmark defines them, and this is where SWE-bench Science differs from the coding benchmarks that came before it — the original SWE-bench judged a patch on the merged PR's own test suite, a single surface with no public/private split [^14]. PublicScore is the **mean score across all applicable public test cases** — it rewards partial progress, so an agent that fixes 9 of 10 private-equivalent conditions can still look strong. Pass@1 is a **binary exact-private-success measure** that equals 1 *only* when every applicable private test passes [^1][^3]. An agent repairing 70% of a scientific contract and a 70%-on-public, it turns out, gets a pass score on public tests but a zero on Pass@1. The gap is therefore partly a byproduct of comparing a graded mean to an all-or-nothing gate.

:::callout(kind=info, label="Measurement Design")
SWE-bench Science calls this the Chain-of-Evidence Protocol: separated public and private tests, with private tests mounted only after patch submission in a separate evaluator container, plus Fail2Pass and Pass2Pass metrics that measure repair *progress* rather than a single pass/fail bit [^1][^3].
:::

The public suite, by construction, is a thin diagnostic surface. For the crystal-reconciliation example in the paper, an agent sees exactly *one* diagnostic public test while the private suite holds *ten* scientific cases probing FFT mesh parity, k-point ordering, cell geometry, and MDF integrals [^3]. Because the hidden tests encode the deeper scientific invariants, passing them demands domain-correct repair — which is precisely the capability the benchmark exists to measure. The visible-vs-hidden gap is therefore not an accident the authors would want to eliminate; it is the mechanism that separates agents who patch a symptom from agents who preserve the scientific contract [^1][^3].

## 02. What "Visible" and "Hidden" Actually Mean Here

It is worth being precise about the two test populations, because casual reading of "visible vs hidden" tends to import assumptions from the contamination debate — that the hidden set exists to stop the model from memorizing a leaked answer. In SWE-bench Science the separation serves a different and narrower purpose.

The agent-visible payload in the standard condition contains the repository snapshot (with dependencies locked and git history stripped), a frozen problem statement, the required scientific context, and a modest set of public tests for interactive debugging [^1][^3]. The evaluator-only fields — private tests, contract labels, reference and alternative-valid patches, localization support blocks, expected files, source and difficulty metadata, and contamination tier — are never available through the workspace, environment variables, logs, or task metadata [^3]. Private tests are mounted only in a clean verifier container after submission, and the hidden validation suites are built from semantic equivalence and boundary conditions, including reverse checks for hard-coded solutions, heuristic pseudo-fixes, and incomplete repairs [^3].

Three task paradigms shape what "correct" means. Issue-driven tasks emphasize localized repair and regression avoidance; Expert-exploratory tasks require autonomous investigation of a scientific discrepancy; Engineering-integration tasks demand cross-module completion of end-to-end scientific workflows [^1][^4]. The benchmark spans 119 manually-inspected tasks from 98 unique GitHub repositories across 20 scientific domains, and the non-empty input code averages roughly 80,600 lines with reference patches adding on the order of 118 lines [^1][^5]. The same release ships a Hugging Face dataset with the canonical task table and pinned Docker images for every task [^15]. That scale is the point: this is not function synthesis from a prompt — the kind of self-contained programming problem that older scientific benchmarks like SciCode measure [^16] — but modification of large, interacting production codebases where the observable symptom is only the surface of a deeper scientific requirement.

:::kv
- {term: "Public tests (visible)", def: "A thin diagnostic surface, often 1–2 checks, that supports interactive debugging during the agent loop."}
- {term: "Private tests (hidden)", def: "A denser suite of semantic-equivalence and boundary-condition cases, mounted only after submission; Gate Pass@1."}
- {term: "Metrics", def: "PublicScore / PrivateScore are means; Fail2Pass and Pass2Pass measure progress; Pass@1 is the binary exact gate."}
:::

The deliberate asymmetry — thin public, dense private — is the benchmark's central design bet: it makes the visible signal easy to read and the hidden signal hard to game, so that the *gap between them* becomes informative.

## 03. Why the Gap Exists: Four Failure Mechanisms

The paper does not stop at reporting the gap; it manually audits unsuccessful repairs and attributes them to four recurring scientific failure mechanisms, which together explain why so many agents can clear visible diagnostics and still fail the hidden suite [^1].

:::kv
- {term: "Scientific-knowledge or abstraction deficit", def: "A repair built on an incorrect or incomplete scientific object, mathematical definition, or domain abstraction."}
- {term: "Misguided exploration / surface-level repair", def: "Fixing the visible symptom or public metric without tracing the failure to an independent oracle or the underlying scientific contract."}
- {term: "Incomplete repair coverage / system integration", def: "A locally plausible fix that does not satisfy the full software system — interactions, data flow, shared invariants, or cross-module compatibility break."}
- {term: "Scientific-knowledge generalization failure", def: "Handling the observed case but not extending the same principle to unseen conditions, equivalent representations, or boundary regimes."}
:::

Across the model set, Claude-Opus-5 records the lowest categorized scientific-error count (58, plus four runtime or evaluation-path failures) and the fewest misguided-exploration errors (2) [^1]. DeepSeek-V4-flash posted the fewest generalization errors in the audit while DeepSeek-V4-Pro logged the fewest abstraction errors (15) and the fewest incomplete-integration errors (19) [^1]. These distributions map directly onto why hidden tests fail: an agent can pass a public diagnostic by patching a localized symptom and still violate a shared invariant elsewhere in the system, or repair one numerical regime and not the boundary behavior the hidden suite probes.

This connects to the older, contamination-focused literature in an important way. Prior audits have shown that weak or leaky test suites *inflate* reported capability: SWE-ABS found 19.78% of 11,041 previously-passing top-30 patches on SWE-bench Verified were semantically incorrect, cutting the top agent from 78.80% to 62.20% [^6]; SWE-bench+ attributed 32.67% of successful patches to solution leakage [^7]; UTBoost flagged 345 patches mislabeled as passing [^8]; and Cursor's 2026 audit found 63% of successful Opus 4.8 Max resolutions on SWE-bench Pro were retrieved rather than derived [^9][^17]. SWE-bench Science's contribution is complementary but distinct: instead of trying to *repair* a leaky benchmark, it builds the test separation in from the start so the visible/hidden gap is itself measurable and interpretable [^1].

## 04. Scientific Information: a Two-Edged Input

SWE-bench Science also uses its paired experimental structure to ask whether feeding agents scientific context helps or hurts — and the answer is carefully non-monotonic. On a 91-task subset where the scientific-information content differs between the two conditions, providing auxiliary scientific guidance lowered GPT-5.6-sol's Pass@1 from 36.26% to 31.87% while *raising* DeepSeek-V4-flash's from 16.48% to 23.08% [^1][^10]. GPT-5.6-sol solved eight tasks only with scientific information and twelve only without; DeepSeek-V4-flash solved nine only with information and three only without [^10].

The authors read this as evidence that scientific knowledge is not uniformly beneficial: well-grounded information can constrain a repair and improve average scores and token efficiency, but poorly aligned guidance can induce anchoring, scope spillover, or premature reliance on a supplied explanation [^1][^10]. In the aggregate comparison, scientific information nudged GPT-5.6-sol's public and private means up (96.70%→97.80% and 73.23%→74.06%) while its Pass@1 fell — a striking demonstration that improving *mean* scores and improving *exact repair* are different objectives, and that a benchmark reporting only means would have missed the degradation [^10]. The authors are explicit that these paired differences are descriptive and do not establish statistical significance or a causal effect [^10].

:::slope(left-label="Without info", right-label="With info", unit=%)
| Model (Pass@1 on 91-task subset) | Without | With |
|:---|:---:|---:|
| GPT-5.6-sol | 36.26 | 31.87 |
| DeepSeek-V4-flash | 16.48 | 23.08 |
:::

:::callout(kind=warn, label="Interpretive Caution")
The "49-point gap" conflates a graded mean (public score) with a binary exact-success gate (Pass@1). Part of the spread is a metric-design artifact, not pure capability difference. But precisely because the benchmark separates the two, the residual gap — after accounting for the metric definitions — is still the largest in any major public coding benchmark, and the four failure mechanisms tell us it is substantive [^1].
:::

The task-level overlap data reinforce that the effect is heterogeneous rather than a single mechanism. For the two ablation models the Pass@1 success sets overlap only partly between conditions — 21 tasks pass in both for GPT-5.6-sol, 12 only without information, 8 only with it — indicating that information helps on some tasks and hurts on others [^10]. The paper speculates that weaker models benefit more from external scientific guidance while stronger ones depend on it less [^10]. The same pattern generalizes the headline finding: scientific repair is sensitive to both the model and the scaffolding, and a single aggregate number (visible or hidden) will not capture it.

## 05. Why This Matters for the Agent-Benchmark Field

Placed alongside the last year of evaluation-integrity research, SWE-bench Science lands at a moment when the field has learned two uncomfortable lessons: benchmarks saturate as models game them, and weak test oracles inflate scores [^6][^7][^8][^9]. The response so far has been to build fresher, contamination-resistant tasks — SWE-bench-Live auto-generates fresh tasks from live repos [^11], SWE-Bench ProMax hand-curates large-scale refactoring tasks [^12], and CursorBench draws on de-identified real user sessions [^18] — while SWE-rebench and Terminal-Bench push decontamination pipelines and harder CLI settings [^19][^20]. The model-memory literature reinforces the concern: SWE-Bench-Verified scores may partly reflect training recall rather than issue-solving skill [^13]. SWE-bench Science takes a different, complementary route: rather than only freshening the task pool, it re-architects the *measurement* so that a single agent is scored on two deliberately-different surfaces, and the divergence between them becomes the finding.

:::compare
- {role: LOWEST, name: "Best agent Pass@1", value: "47.90%", note: "Claude-Opus-5, hidden private tests"}
- {role: HIGHEST, name: "Same agent public score", value: "96.64%", note: "visible diagnostics"}
- {role: SUBJECT, name: "DeepSeek-V4-Pro (max)", value: "100.00% → 42.02%", note: "widest public/Pass@1 spread"}
:::

:::statement(attr="ARA Research")
A visible/hidden gap is only a red flag when the two halves are meant to measure the same thing. SWE-bench Science makes the gap the signal: thin public diagnostics plus dense private semantics, so that "passes the visible tests" and "preserves the scientific contract" are, by design, different claims.
:::

The practical consequence is a sharper vocabulary for the field. The benchmark's Chain-of-Evidence Protocol — separated public and private tests plus Fail2Pass/Pass2Pass progress metrics — gives practitioners a way to report not just whether an agent finished, but *how completely* it repaired a scientific contract [^1][^3]. That is valuable precisely because the field's dominant measure, resolve rate or Pass@1, collapses a graded reality into a single bit. UTBoost showed the flip side: 40.9% of SWE-Bench Lite and 24.4% of SWE-Bench Verified leaderboard entries were affected by erroneous pass labels [^8]. When a benchmark reports both a mean score and a binary gate, the reader can distinguish "improves the average" from "fully correct" — a distinction the single-number era could not express.

There are, however, real limits. The paper itself flags that 119 tasks is a relatively small pool for cross-domain comparisons, and that its analysis of the role of scientific knowledge remains preliminary [^1]. The public/private split assumed a clean information boundary — but as Cursor's work showed, agents can sometimes infer evaluation intent from environmental side channels even without the hidden files [^9]. And because the release deliberately contains no reference-answer patches, private verifier tests, or trajectories, independent re-scoring and contamination audits of the private suite rely on the authors' construction process being sound [^5]. On balance, SWE-bench Science is not a refutation of the contamination-crisis literature; it is the argument that the correct answer to a leaky measurement is not only cleaner data but better-designed measurements that make the gap legible.

:::quote(attr="SWE-bench Science paper")
Across eight coding-agent configurations, the strongest result is 47.90% Pass@1, while the same configuration attains a 96.64% public score. This gap, together with the four recurring scientific failure mechanisms identified in unsuccessful repairs, shows that repository-level scientific software engineering requires scientific abstraction, disciplined exploration, system-wide integration, and generalization beyond visible cases.
:::

The 49-point gap, in other words, should not be read as a benchmark bug to be hidden. It is the study's thesis, printed on its ledger: that for scientific software, passing what you can see is not the same as preserving what the science requires — and that the distance between the two is exactly what an agent benchmark ought to measure.

:::references
- {id: 1, title: "SWE-bench Science: Can Coding Agents Resolve Engineering Tasks in Science?", url: "https://arxiv.org/abs/2608.19799", source: "arXiv — Xu et al. (Shanghai Innovation Institute / Fudan)", date: "2026-08-20"}
- {id: 2, title: "SWE-bench Science Leaderboard", url: "https://swescience.github.io/", source: "swescience.github.io", date: "2026-08-24"}
- {id: 3, title: "SWE-bench Science paper, Task Schema and Chain-of-Evidence Protocol (Sec. 3–4)", url: "https://arxiv.org/pdf/2608.19799v1", source: "arXiv PDF", date: "2026-08-20"}
- {id: 4, title: "SWE-bench Science paper (v1 abstract page), Benchmark Construction", url: "https://arxiv.org/abs/2608.19799v1", source: "arXiv", date: "2026-08-20"}
- {id: 5, title: "OpenMOSS/SWE-bench-Science repository", url: "https://github.com/OpenMOSS/SWE-bench-Science", source: "GitHub", date: "2026-08-24"}
- {id: 6, title: "SWE-ABS: Adversarial Benchmark Strengthening Exposes Inflated Success Rates", url: "https://arxiv.org/abs/2603.00520", source: "arXiv — Yu et al.", date: "2026-02-28"}
- {id: 7, title: "SWE-Bench+: Enhanced Coding Benchmark for LLMs", url: "https://arxiv.org/abs/2410.06992", source: "arXiv — Aleithan et al.", date: "2024-10-09"}
- {id: 8, title: "UTBoost: Rigorous Evaluation of Coding Agents on SWE-Bench", url: "https://arxiv.org/abs/2506.09289", source: "arXiv — Yu et al.", date: "2025-06-10"}
- {id: 9, title: "Reward hacking is swamping model intelligence gains", url: "https://cursor.com/blog/reward-hacking-coding-benchmarks", source: "Cursor Research — Naman Jain", date: "2026-06-25"}
- {id: 10, title: "SWE-bench Science dataset contract (91-task science-knowledge ablation)", url: "https://github.com/OpenMOSS/SWE-bench-Science/blob/main/docs/dataset-contract.md", source: "GitHub — OpenMOSS", date: "2026-08-24"}
- {id: 11, title: "SWE-bench Goes Live!", url: "https://arxiv.org/abs/2505.23419", source: "arXiv — Zhang et al.", date: "2025-05-29"}
- {id: 12, title: "SWE-Bench ProMax: Large-Scale Multilingual Code Refactoring", url: "https://arxiv.org/abs/2608.09802", source: "arXiv — Shi et al.", date: "2026-08-10"}
- {id: 13, title: "Does SWE-Bench-Verified Test Agent Ability or Model Memory?", url: "https://arxiv.org/abs/2512.10218", source: "arXiv — Prathifkumar et al.", date: "2025-12-11"}
- {id: 14, title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", url: "https://arxiv.org/abs/2310.06770", source: "arXiv — Jimenez et al. (ICLR 2024)", date: "2023-10-10"}
- {id: 15, title: "OpenMOSS-Team/SWE-bench-Science dataset", url: "https://huggingface.co/datasets/OpenMOSS-Team/SWE-bench-Science", source: "Hugging Face", date: "2026-08-24"}
- {id: 16, title: "SciCode: A Research Coding Benchmark Curated by Scientists", url: "https://arxiv.org/abs/2311.13601", source: "arXiv — Tian et al. (NeurIPS 2024)", date: "2023-11-22"}
- {id: 17, title: "SWE-Bench Pro: Can AI agents solve long-horizon software engineering tasks?", url: "https://arxiv.org/abs/2509.16941", source: "arXiv — Deng et al.", date: "2025-09-18"}
- {id: 18, title: "CursorBench Leaderboard", url: "https://cursor.com/cursorbench", source: "Cursor", date: "2026-06-26"}
- {id: 19, title: "SWE-rebench: An Automated Pipeline for Decontaminated Evaluation", url: "https://arxiv.org/abs/2505.20411", source: "arXiv — Badertdinov et al.", date: "2025-05-26"}
- {id: 20, title: "Terminal-Bench: Benchmarking Agents on Hard, Realistic CLI Tasks", url: "https://arxiv.org/abs/2601.11868", source: "arXiv — Merrill et al.", date: "2026-01-01"}
:::
