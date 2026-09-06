---
eyebrow: BENCHMARK FORENSICS · AI RESEARCH AGENTS
title: "Repo-To-Skill's 41.78-point jump: the 5,353-skill library is not the thing that was measured"
deck: A skill library distilled from 1,000 GitHub repositories reports the largest single gain in MLE-bench's history. Read the appendix and the artifact does not appear in the experiment.
domain: general
lede: |
  On 2 September 2026 a team from BAAI and three universities posted Repo-To-Skill, which
  distils GitHub repositories into agent skills and reports MLE-bench "Any Medal" rising from
  31.11% to 72.89% on the full 75-competition suite — a 41.78-point move, the largest ever
  claimed on that benchmark. The obvious suspicion is contamination: mine enough of GitHub and
  you eventually mine the answers. A direct audit of the published library says otherwise. What
  it also says is that the published library was not what produced the number.
stats:
  - {label: MLE-bench Any Medal, value: 72.89, unit: "%", note: "from 31.11%, full 75 competitions"}
  - {label: Skills in the library, value: "5,353", note: "explicitly excluded from the benchmark runs"}
  - {label: Per-competition graphs built, value: 75, note: "pre-run; none published"}
  - {label: Best listed public score, value: 64.44, unit: "%", note: "board closed since 2026-04-24"}
---

## 01. The number, exactly as reported

Repo-To-Skill (arXiv:2609.02749, submitted 2 September 2026, eleven authors led by BAAI) presents DisCo, an agent that turns repositories into reusable skills, and the AREX-Skill Library those skills live in.[^1][^2] Its Table 1 reports MLE-bench Any Medal at 31.11 ± 2.22 without skills and 72.89 ± 1.18 with them, over the full 75-competition suite, averaged across three repeated runs, with Codex as the harness and a GPT-5.5 backbone held fixed.[^2] The paper describes the single manipulated variable as whether the agent is equipped with the distilled skills or not.[^2]

That is a real, correctly transcribed number, and it is worth saying up front that nothing in this article suggests otherwise. The question is what it measures.

:::kv
- {term: "Did the 5,353-skill library produce the 72.89%", def: "No. The paper states that paper-derived and task-oriented graphs are not included in that count, and MLE-bench used 75 per-competition graphs built separately."}
- {term: "Is the library seeded with Kaggle solutions", def: "No evidence of it. A sweep of all 178 family indexes covering the 1,000 source repositories found no competition or solution repository, and no gradient-boosting library at all."}
- {term: "Was the comparison compute-matched", def: "On the running phase only. The skill arm additionally received up to 24 GPU-hours of per-task exploration, including diagnostic trials on the competition being graded."}
- {term: "Can anyone check the MLE-bench result", def: "Not today. The 75 graphs are the one benchmark artifact the repository withholds, no per-competition table is published, and the leaderboard has been closed since 2026-04-24."}
- {term: "So: capability or contamination", def: "Neither, on the current evidence. The defensible reading is a third category, per-task preparation, which no benchmark rule currently governs or requires anyone to disclose."}
:::

The rest of this piece is the working behind those five lines: what the paper says in its own words, what the published artifact contains when you open it, what the benchmark's own contamination machinery was built to catch, and what four cheap experiments would settle in a fortnight.

---

## 02. Two systems wearing one name

The paper's title, its abstract and every summary written about it describe one artifact: a library of 5,000-plus verified skills distilled from 1,000 widely used ML repositories, routed through 20 areas and 178 capability families.[^1] The precise figure appears in §4.1: "The repository snapshot contains 5,353 skills across 1,000 repository graphs, organized into 20 areas and 178 capability families."[^2]

The same paragraph closes with one sentence that reorganises everything downstream of it: "Paper-derived and task-oriented graphs are not included in these counts."[^2]

Section 4.3 says what MLE-bench used instead: "MLE-bench uses one descriptive graph for each of 75 competitions, built through task decomposition, source discovery, and bounded diagnostic trials".[^2] Section 5.1 says where the material came from — the graphs were distilled from "knowledge sources collected through web search while excluding the original competition webpage and competition-specific content".[^2]

So the headline number was produced by seventy-five bespoke artifacts, each one built for the competition it was about to be scored on, from a live web search conducted before the clock started.[^2] One precision worth keeping: Table 1's row label reads "Codex + AREX-Skill", and no sentence in the paper explicitly says the repository library was *withheld* from the MLE-bench runs — so a combined configuration is not formally ruled out by the text. What the paper does establish is that the library was not what was built for the task, and was not counted as part of what was.[^2]

| | The AREX-Skill Library | The MLE-bench skill sets |
|---|---|---|
| *What it is | 5,353 sub-skills over 1,000 repository graphs [^2] | 75 per-competition descriptive graphs [^2] |
| How built | Distilled from repository source, docs, tests and examples [^4] | Web search plus "bounded diagnostic trials" on the target task [^2] |
| Reused across tasks | Yes — routed by area → family → repository [^4] | No — one graph per competition [^2] |
| Published | Yes, Apache-2.0, browsable [^4] | No [^5] |
| Produced the 72.89% | No [^2] | Yes [^2] |

This is not concealment. Every sentence quoted above is in the paper, in plain language, and the authors draw the distinction themselves.[^2] But it inverts how the result reads. "A downloadable library of 5,353 skills lifts a research agent by 134%" is a claim about a reusable public good. "Seventy-five individually prepared briefing documents, built with trial runs on the graded task, lift a vanilla agent by 134%" is a claim about preparation. Both may be true. Only the second was tested.

:::callout(kind=danger, label="The load-bearing distinction")
Every argument in this article turns on separating the two systems. Section 06 audits the published library and finds it clean. That finding is real and it does not defend the headline number, because the published library did not produce the headline number.
:::

The rest follows from taking the second claim seriously. If the mechanism is per-task preparation, then the questions worth asking are about the preparation: what it cost, what it read, and whether anyone can inspect it.

---

## 03. The budget that isn't in the comparison

The comparison that produces +41.78 points is not a comparison of equal machines. It is a comparison of a skill-equipped arm that has already spent a phase of compute on the target competition against a baseline that has not. The paper's own protocol table says so in plain text; the arithmetic of what that costs is left to the reader.

Appendix A.2.1's Table 5 lays out two stages, each with its own ceiling. Verbatim: "The two-stage MLE-bench protocol. Both limits apply per task. Skill construction is completed before benchmark running begins."[^3] Exploration is defined as "Explore useful modeling and execution decisions and finalize a task-oriented set of descriptive skills" at "≤ 24 GPU-hours"; Running is "Let Codex select from the finalized skill pool and optimize a full benchmark submission" at "≤ 24 GPU-hours".[^3] §5.1 states the accounting rule directly: "the one-time construction budget is separate and is not counted in either run-time condition."[^2]

The unit below is GPU-hours per competition, and these are ceilings, not realized usage — the paper reports no measured spend for either arm.[^2]

:::stack-rows
categories: [Exploration, Running]
rows:
  - {label: "No-skill baseline", values: [0, 24]}
  - {label: "Skill-equipped arm", values: [24, 24]}
:::

One nuance has to be stated plainly, because the paper does not overclaim here and neither should this section. Appendix A.2.1 says only: "The no-skill condition uses the same Codex backbone and running budget but does not receive the distilled skills."[^3] It never says the baseline was *denied* an exploration phase. The asymmetry above is an implication of a design that grants exploration to one arm and describes the other purely in terms of the running budget — not a stated denial. That distinction matters for how strongly the point can be pressed, and it is exactly the kind of thing a compute-parity claim should have foreclosed explicitly.

What makes the exploration phase more than bookkeeping is what happens inside it. §4.3: "MLE-bench uses one descriptive graph for each of 75 competitions, built through task decomposition, source discovery, and bounded diagnostic trials".[^2] Diagnostic *trials* means code executes against the target competition before grading begins. The paper does not elaborate on what those trials contain — how many, on which data splits, or whether their outcomes were inspected.[^2] So the skill arm arrives at the graded run having already observed the task; the baseline arrives cold.

My arithmetic, not the paper's: ≤48 GPU-hours per competition for the skill arm against ≤24 for the baseline is up to 2.0x, and across all 75 competitions up to roughly 1,800 GPU-hours of exploration with no baseline counterpart. Because realized usage is never reported, 2x is an upper bound rather than a measurement.[^2] It cannot even be closed out at the run level: the paper does not state whether exploration was re-run for each of the three repeated runs, so total GPU-hours are unpinnable in either direction.[^2]

The disclosure gap widens on hardware.

| Resource | No-skill baseline | Skill-equipped arm |
|---|---|---|
| Backbone | Same Codex backbone [^3] | Same Codex backbone [^3] |
| Harness | Two-stage protocol, running phase [^3] | Two-stage protocol, exploration + running [^3] |
| *Exploration budget | Not described; no exploration stated [^3] | ≤ 24 GPU-hours per task [^3] |
| Running budget | ≤ 24 GPU-hours per task [^3] | ≤ 24 GPU-hours per task [^3] |
| Graded-run hardware | Not stated [^2] | Not stated [^2] |
| Repeated runs | Three; exploration re-run unstated [^2] | Three; exploration re-run unstated [^2] |

The blank hardware row is conspicuous because Repo-To-Skill does specify hardware elsewhere: FrontierCS containers "limited to 2 CPUs and 4 GiB of RAM", and PassNet "conducted on NVIDIA A100-SXM4-40GB".[^2] MLE-bench, meanwhile, fixes its envelope exactly: "On each run, agents have access to a machine with 36 vCPUs, 440GB RAM, 4095 GiB SSD, and a single Nvidia A10 GPU", with "a maximum of 24 hours to produce a submission" per competition.[^9] Note the unit mismatch — MLE-bench denominates 24 *hours wall-clock* on a one-GPU box; Repo-To-Skill denominates 24 *GPU-hours*. Those are the same number only if the graded box has one GPU, which is never asserted.[^2]

None of this would matter if the metric were budget-insensitive. It is not, and MLE-bench's own paper is the source.

:::slope(left-label="Baseline budget", right-label="Expanded budget", unit=%)
| Item | Baseline | Expanded |
|---|---|---|
| GPT-4o, 24h to 100h | 8.7 | 11.8 |
| o1-preview, pass@1 to pass@8 | 16.9 | 34.1 |
| AIDE o1-preview, reported to AIRA harness (Lite) | 35.2 | 45.9 |
:::

"GPT-4o scores 8.7% given 24 hours to attempt each competition, but 11.8% when given 100 hours" — though the 100h arm also raised the AIDE node cap from 500 to 5,000, so that is a compound change, not clean time.[^9] Retries are cleaner: "o1-preview's score doubles from 16.9% using pass@1 to 34.1% using pass@8", and "both agents' pass@6 scores are roughly double their pass@1 scores", with GPT-4o at pass@6 (17.0%) landing on o1-preview's pass@1 (16.9%).[^9] Harness alone moves it too: AIRA-dojo re-ran the identical published AIDE-greedy o1-preview agent in their own environment and it "improves the medal rate from 35.2 % to 45.9 % compared to the reported results".[^30]

Credit where it is due: the paper discloses the exclusion in plain text rather than burying it, and defends it on amortization — "Creator mode is paid once per source and amortized over every task that later draws on the result".[^2] It also prices construction honestly: "Construction uses GPT-5.5 and GPT-5.6-sol with xhigh reasoning effort, at an average allocation of about $40 per repository."[^2] This is a framing choice, not concealment.

But the amortization defence is load-bearing only where amortization actually happens. For the 5,353-skill library it is genuinely strong — built once, drawn on indefinitely. For the MLE-bench arm it does not hold, because the graphs are task-oriented and built one per competition.[^2] A cost paid per graded task, on the graded task, is not amortized. It is part of the run.

---

## 04. What MLE-bench's contamination defences can and cannot see

MLE-bench did not wave contamination through. It shipped three separate controls, ran them, and published the results — and all three came back null.[^9] That record is most of the reason a headline number on this benchmark gets taken at face value. But a control is only as good as the surface it inspects, and each of these three inspects one of exactly two things: the model's weights, or the code the agent submitted. The mechanism at issue in a skill-library system is neither. It is a document assembled before the graded run began, by a separate pipeline, and handed to the agent as context.

:::stats
- {label: "Dolos similarity threshold", value: 60, unit: "%"}
- {label: "Reference notebooks per competition", value: 50}
- {label: "Submissions flagged", value: 0, note: "across all medal winners"}
- {label: "Obfuscated vs original", value: "8.4 vs 8.5", unit: "%", note: "GPT-4o, 10 seeds"}
:::

Take them in order. The **plagiarism** control ran Dolos code fingerprinting over k=23 token subsequences, comparing every medal-winning submission against the top 50 associated notebooks from the relevant Kaggle competition and surfacing anything above 60% similarity: "We surface any submission file with a similarity score above 60% for human review of potential plagiarism, finding no detected cases of plagiarism."[^9] The **obfuscation** control manually rewrote all 75 competition descriptions to hide the competition's identity, then ran GPT-4o with AIDE over 10 seeds — 8.5 ± 0.6% Any Medal on the originals against 8.4 ± 1.0% on the obfuscated versions.[^9] The **familiarity** control defined familiarity as the mean probability the base model assigns to each token in a document (the competition page plus its 5 most popular discussion posts) and correlated it against per-competition performance: "We find no correlation between the familiarity of GPT-4o's base model with a competition and its performance on that competition."[^9] No correlation coefficient and no p-value accompany that sentence; it is a qualitative reading of a scatter plot.[^9]

| Control | What it inspects | Result | What it cannot see |
|---|---|---|---|
| *Plagiarism (Dolos, k=23) | Submitted code against the top 50 Kaggle notebooks per competition [^9] | Nothing above 60% similarity; no cases detected [^9] | Prose that describes a winning approach and shares no token subsequence with any notebook |
| Obfuscation | Whether naming the competition changes the score [^9] | 8.4% vs 8.5% Any Medal, GPT-4o, 10 seeds [^9] | Material retrieved by task shape rather than by competition name |
| Familiarity | Base-model token probabilities over the competition page and its 5 top discussion posts [^9] | No correlation with per-competition performance [^9] | Anything assembled after training and injected at inference, which the weights never memorised |

The gap is not an inference an outside critic has to draw. The paper draws it:

> We have mitigations in place to prevent plagiarism of the top participants' code or test labels … but it is difficult to detect the reuse of high-level strategies.
> — Chan et al., MLE-bench

That is the whole seam.[^9] A distilled skill document is high-level strategy in prose form. It shares no k=23 token run with a notebook, so Dolos is blind to it. It need not name the competition to be retrieved, so obfuscation does not disturb it. And it is not in the weights at all, so a token-probability familiarity measure has nothing to register. The three controls are well-designed against the two contamination routes they were built for; the third route runs between them.

:::callout(kind=warn, label="Scope")
Every one of these controls was measured on GPT-4o in 2024, at an overall Any Medal rate of 8.5%.[^9] A null result obtained in a near-floor regime does not transfer to a system reporting 72.89% — there was very little signal available for contamination to inflate. The 0.1pp obfuscation delta sits well inside the ±1.0 standard error, which makes it consistent with no effect and equally consistent with an effect the experiment lacked the power to see.[^9]
:::

The authors are candid about the residual risk elsewhere too. They concede that "it's possible that models have trained on all public Kaggle material including competition details, solutions, and even the datasets," and a footnote records that GPT-4's base model could reproduce several rows from the Titanic competition dataset.[^9] Their bottom line is carefully bounded: "Our experiments find no evidence of results being systematically inflated due to memorization," with "no guarantees about future models."[^9] No evidence of inflation is not evidence of no inflation, and the authors do not claim otherwise.

What about the rules? The instructions file shipped to the agent says: "You are not allowed to view others' solutions to this competition. If we detect that your submission is plagiarized from others, the submission will be disqualified," and "You may not hand-label the data to produce a submission file."[^11] The paper adds that "Agents are also forbidden from viewing solutions online, which can often be found on Kaggle or GitHub."[^9] But internet access itself is neither granted nor forbidden — the paper only asks developers to report "whether the agent had internet access" alongside models, scaffolding, hardware and runtime, and the repo frames its resource defaults as "not a strict requirement of the benchmark but please report if you stray from these defaults!"[^9][^10] Every one of those prohibitions is scoped to the agent during the graded episode. Nothing in the rulebook governs what a developer may compute *before* the task begins. This is a norm gap, not a violation, and it should be said plainly: no rule was broken.

The two projects also draw their own boundaries very differently. Repo-To-Skill states that skills are distilled from web-searched material "while excluding the original competition webpage and competition-specific content".[^2] "Competition-specific content" is never defined; Kaggle discussion winner posts and third-party solution repositories are never named as excluded. Compare PaperBench, where each task ships a "blacklist.txt containing websites that the agent is disallowed from using (e.g. the paper's original codebase)" — enumerated, per-task, auditable.[^34] One is a stated intention; the other is a checkable artifact.

The independent literature has a name for the failure mode this leaves open. "Search-Time Contamination" describes inference-time retrieval returning answer-bearing content, "where external retrieval bypasses intended reasoning and inflates measured performance", with measured turn-level jumps immediately after explicit answer leakage of 7.69% to 89.74% on MedQA and 19.25% to 79.45% on MedMCQA.[^23] Two caveats belong with those figures: the domain is medical QA, not ML engineering, and aggregate inflation there was modest even where the per-turn effects were dramatic.[^23] The structural point survives the caveats: a one-time audit of model weights cannot clear a pipeline whose inputs are rebuilt for every task, because there is nothing fixed to audit.

None of this is evidence that leakage occurred. Repo-To-Skill's construction pipeline is documented as excluding the competition page, and its outputs are described as descriptive rather than executable — "Final skills are descriptive rather than executable… contain no runnable training or inference scripts".[^2] No one has audited the 75 graphs. The honest statement is narrower and more uncomfortable than either side would like: MLE-bench's defences were not designed to answer this question, so the question is open, not answered either way.

---

## 05. Inside the High split

The High-complexity cell is where Repo-To-Skill's claim stops being an improvement and starts being an outlier. Table 1 reports Any Medal on the 15 High competitions rising from 13.33 ± 3.85 to 62.22 ± 2.22, against an overall move of 31.11 ± 2.22 to 72.89 ± 1.18, Low of 42.42 ± 6.60 to 86.36 ± 2.62, and Medium of 31.58 ± 1.52 to 69.30 ± 3.16 — all means over three repeated runs.[^2] The paper prices the High jump in the most impressive available units: "from 13.33% to 62.22%", a "366.8% improvement, or 4.67 times the no-skill score".[^2]

That multiplier is a ratio of small integers. Fifteen competitions run three times is 45 competition-runs; 13.33% of 45 is about 6 medals and 62.22% of 45 is exactly 28 — my arithmetic on the reported percentages, not a figure the paper prints.[^2] Per run, that is roughly two medals before and roughly nine after.

:::iso
- {label: "Codex, no skills", glyph: "🥉", count: 2}
- {label: "Codex + AREX-Skill", glyph: "🥉", count: 9}
:::

Those are the per-run medal counts implied by 13.33% and 62.22% of 15 competitions.[^2] Twenty-two additional medals across 45 attempts is a real result. It is not a result that resists being enumerated, and that matters, because the next question is which fifteen competitions and how hard each medal actually is.

:::donut(center-label="75")
- {label: Medium, value: 38}
- {label: "Low (== Lite)", value: 22}
- {label: High, value: 15}
:::

MLE-bench's 75 competitions split 22 Low / 38 Medium / 15 High, with the Low split byte-identical to the "Lite" subset — the official leaderboard column header literally reads "Low == Lite (%)".[^9][^10] The complexity label is an estimate of *human* effort: "Low if we estimate that an experienced ML engineer can produce a sensible solution in under 2 hours", Medium 2–10 hours, High more than 10.[^9] It was never calibrated against agent difficulty. A task that costs a human three days of data wrangling may cost an agent one long script.

The second thing "High" does not tell you is what a medal costs. Reading the grader's `get_thresholds(num_teams)` directly: under 100 teams, gold/silver/bronze fall at 10%/20%/40% of the field; at 100–249 teams gold becomes fixed position 10; at 250–999 teams gold is `10 + int(num_teams * 0.002)`, silver is fixed position 50, and bronze is fixed position 100; only at 1000+ teams does bronze become a true top 10%.[^12] In a 546-team competition, bronze is rank 100 — the top 18.3% of the field, not the top 10%.[^12]

:::rank-list
- {label: iwildcam-2019, value: "top 29.8%", pct: 100, highlight: true}
- {label: 3d-object-detection, value: "top 18.3%", pct: 61}
- {label: smartphone-decimeter-2022, value: "top 17.5%", pct: 59}
- {label: predict-volcanic-eruptions, value: "top 16.7%", pct: 56}
- {label: bms-molecular-translation, value: "top 11.4%", pct: 38}
- {label: rsna-2022-cervical-spine, value: "top 11.3%", pct: 38}
- {label: nfl-player-contact-detection, value: "top 10.6%", pct: 36}
- {label: identify-contrails, value: "top 10.5%", pct: 35}
:::

:::note
Effective bronze bar = the grader's fixed rank-100 cutoff divided by team count, for the eight High competitions with fewer than 1,000 teams.[^12] Every team count here is compiled from competition organiser reports and public write-ups rather than from a single machine-readable source, so all of them should be read as approximate; the cutoff rule itself is exact, read from the grader source.[^12][^50]
:::

On these figures, eight of the 15 High competitions had fewer than 1,000 teams and therefore sat in the flat rank-100 bronze bracket.[^12] The remaining seven — including siim-covid19-detection (1,305), rsna-miccai (1,555), stanford-covid-vaccine (1,636), rsna-breast-cancer-detection (1,687) and hms-harmful-brain-activity-classification (2,767) — are the ones where bronze means what a reader assumes it means.[^50] "Any Medal on High" is thus not one bar; it is at least two, and the softer one covers more than half the split.

Existing systems already clear a meaningful part of it. Official per-competition grading reports committed to the MLE-bench repo let you count medals directly:[^14][^15]

| System | High medals (of 15, sampled seed) | Leaderboard High (%) |
|---|---|---|
| AIRA-dojo (o3) | 3 | not listed |
| Famou-Agent | 5 | 42.22 ± 2.22 (listed as Famou-Agent 2.0) |
| CAIR MARS+ | 7 | not listed |
| AIBuildAI (Claude-Opus-4.6) | 7 | 46.67 ± 0.00 |

AIBuildAI's 7-of-15 on the sampled seed matches its published High cell of 46.67 ± 0.00 exactly.[^15][^10] Three competitions look close to free for a strong agent: `iwildcam-2019-fgvc6`, `predict-volcanic-eruptions-ingv-oe` and `stanford-covid-vaccine` were gold-medalled by every one of those four systems on the sampled seed.[^14][^15] Four were medalled by none of them — `bms-molecular-translation`, `hms-harmful-brain-activity-classification`, `rsna-2022-cervical-spine-fracture-detection`, `siim-covid19-detection` — though this is a five-report sample, not evidence of "never".[^14][^15]

Against that field, 62.22 would sit above every non-flagged published High figure: AIBuildAI at 46.67 ± 0.00, Famou-Agent 2.0 and ML-Master 2.0 at 42.22 ± 2.22, AIDE with o1-preview at 11.67 ± 1.27 in October 2024.[^10] The only higher number on the board, Disarray at 71.11 ± 2.22, appears in the separate "Test-set feedback" table the leaderboard itself marks "not directly comparable".[^10]

The last soft spot is retrievability. The 15 High slugs are public in `experiments/splits/high.txt`,[^13] and for at least nine of them a first-place write-up with runnable code is an ordinary search result — contrails,[^38] RSNA breast cancer,[^39] RSNA cervical spine,[^40] Vesuvius ink detection.[^51] A single volunteer GitHub index describes itself as "a curated collection of solutions, ideas, and insights from top performers across hundreds of Kaggle competitions" and carries some 6.5k stars.[^37] And you do not need first place: bronze on this split is rank ~100 to ~276, so a mid-pack public write-up suffices.[^12] The irony is structural — MLE-bench commits, per competition, a `kernels.txt` of the top 50 public Kaggle notebooks as the reference corpus for its own plagiarism detector, and for several High competitions those lists include explicitly placement-labelled solutions.[^9][^10]

None of this shows that Repo-To-Skill's skill graphs used those solutions. The three near-free competitions plus the four that several existing agents already medal account for most of a plausible 9-of-15; the genuinely new ground is a handful of competitions, and nobody can say which, because Repo-To-Skill publishes per-paper results for PaperBench but only four aggregate rows for MLE-bench.[^2] The High cell is less impossible than it reads. It is also, in its current form, unfalsifiable at the competition level.

---

## 06. What the audit clears: the library is not an answer key

The crude version of the contamination worry is easy to state and, unusually for a dispute like this, easy to test: that someone mined Kaggle winning solutions into a skill library, and the agent recites them back at MLE-bench. AREX-Skill is published. So what follows is a direct forensic pass over the artifact — what is in it, what is conspicuously not, and what a skill body actually says when you open one.[^4]

Scope first. The router's build metadata records `repository_count: 1000`, `area_count: 20`, `family_count: 178`, `assignment_count: 2209` and `non_empty_family_count: 178` — every family populated, nothing left unrouted, which is what makes a sweep of all 178 family index files reach all 1,000 repositories.[^6] The paper counts the same object differently: "The repository snapshot contains 5,353 skills across 1,000 repository graphs".[^2] The 5,353 are sub-skills. The directory listing holds about 1,000 roots — GitHub's own banner on that page reads "Sorry, we had to truncate this directory to 1,000 files. 1 entry was omitted from the list." — and roots carry several sub-skills each: `timm` has 7, `optuna` has 6.[^53]

The shape of the index is a general ML-engineering library, not a competition shelf. By repository count, the eight largest areas:[^52]

:::bars
- {label: LLM Applications, value: 325, pct: 100}
- {label: Computer Vision, value: 312, pct: 96}
- {label: Generative Media, value: 194, pct: 60}
- {label: Data Science, value: 152, pct: 47}
- {label: LLM Models-Training-Alignment, value: 149, pct: 46}
- {label: Training Infrastructure, value: 135, pct: 42}
- {label: Scientific Computing, value: 124, pct: 38}
- {label: MLOps, value: 116, pct: 36}
:::

Those eight plus the twelve smaller areas — down through Model Deployment 114, Reinforcement Learning 82, Robotics 81, NLP 78, Information Retrieval 67, Speech and Audio 56, Time Series 53, Biomedical AI 50, Graph Learning 42, Autonomous Driving 38, Responsible AI 21, Probabilistic and Causal 20 — sum to 2,209, which matches the `assignment_count` rather than the 1,000 repositories, because a repository routed into more than one family is counted in each.[^52][^6]

**The first negative finding.** Across the 178 family index files, no repository owner or name contains `kaggle`, `solution`, `1st-place`, `winning`, or `competition`.[^7][^52] The only occurrence of "Kaggle" encountered was descriptive prose inside one skill blurb, for `ujjwalkarn/DataSciencePython`, which mentions "Kaggle-style tabular classifiers" — a genre label, not a leaderboard entry.[^7]

:::note
This extraction was a careful read of the 178 routing indexes, not a byte-exact grep of every one of the 5,353 skill bodies. Nobody has read those end to end, and the finding should be read as "no marker survived a careful pass over the indexes" rather than as a proof.[^52][^2]
:::

**The second negative finding is the surprising one.** XGBoost, LightGBM, CatBoost, scikit-learn and pandas have no skill directory in the library at all. All five paths return HTTP 404, including the kebab-case variant the repo's own slug convention would require, and none appears in any of the 178 family files.[^4][^52]

| Library | Role in a typical MLE-bench solution | In AREX-Skill? |
|---|---|---|
| *`xgboost` | Gradient-boosted trees; the default tabular baseline | No — 404 |
| `lightgbm` | Faster GBDT; the usual leaderboard workhorse | No — 404 |
| `catboost` | GBDT with native categorical handling | No — 404 |
| `scikit-learn` | Preprocessing, CV splits, metrics | No — 404 |
| `pandas` | Data loading and feature assembly | No — 404 |
| `transformers` | NLP and multimodal backbones | Yes |
| `timm` | Vision backbones and pretrained configs | Yes — 7 sub-skills |
| `albumentations` | Image augmentation | Yes |
| `optuna` | Hyperparameter search | Yes — 6 sub-skills |
| `torchvision` | Vision datasets, transforms, models | Yes |

So 6 of 10 probed MLE-bench-relevant libraries are present and 4 absent, with coverage skewed toward vision and NLP rather than tabular.[^4] The `data-science / tabular-modeling` family holds 17 repositories and its own scope line promises exactly the missing material — "Classical and neural classifiers and regressors for tabular or structured data, including gradient boosting and tabular deep learning" — yet it indexes only AutoML wrappers and pedagogical repos: `autogluon`, `auto-pytorch`, `tabpfn`, `mljar-supervised`, `imbalanced-learn`, `cuml`, `mlxtend`, `lazypredict`.[^7] The same pattern shows up one layer down the stack: `training-infrastructure / deep-learning-frameworks` holds 7 repos — `apple/axlearn`, `chainer/chainer`, `Jittor/jittor`, `ludwig-ai/ludwig`, `lululxvi/deepxde`, `tensorlayer/TensorLayer`, `tflearn/tflearn` — and does not include `pytorch/pytorch`.[^54] That reads as foundational frameworks being scoped out as assumed-known, not as a library seeded from competition write-ups.

Make the inference explicitly, because it is the strongest point available to the authors: a Kaggle-seeded index would {accent}over-represent{/} gradient boosting, which is the single most common tool in competitive tabular work. Its total absence is evidence against seeding, not for it.[^7][^4]

Then there is what a skill actually contains. Even the sub-skill explicitly named `benchmarking-and-results` carries no measured numbers. Verbatim: "This sub-skill covers benchmark execution and result interpretation only", and "Pick the smallest representative scope first: one model, one device, low batch size, and low iteration counts."[^8] The `timm` root skill reads, verbatim: "Keep model transforms tied to `model.pretrained_cfg` whenever pretrained weights are involved".[^8] That is API discipline, not a leaderboard recipe — and the file even warns that bundled CSVs are "snapshots from specific accelerators, software versions, precision modes, and layouts".[^8] One tension to name rather than paper over: the paper describes its skills as "descriptive rather than executable", while the repository markets "5,000+ verified, executable skills" — the two are reconcilable only if the "descriptive" wording scopes the task-oriented graphs and not the library, which is how this article reads it, but the paper does not say so outright.[^2][^4] Provenance is repo-internal to match: `optuna/references/repo-provenance.md` records schema `disco.repo-provenance.v1`, commit `243c156d9dda5093fa4358c6923fb22cd721fd04` on `master`, remote `https://github.com/optuna/optuna.git`, `generated_at_utc: 2026-06-21T00:00:00Z`, with evidence drawn from the repository's own source, docs, examples, tests and configs — no external write-ups.[^4] One wrinkle worth a line: the repo is Apache-2.0 but states every skill carries its own license, and sampled frontmatter is inconsistent — `optuna` reads `license: NOASSERTION` while `transformers` and `timm` read `license: Apache 2.0`.[^4][^53]

:::callout(kind=success, label="What this clears")
The published AREX-Skill library shows no sign of Kaggle-solution seeding: no competition repositories, no craft skills, and skill bodies made of procedure rather than results.[^7][^8] The absence of the entire gradient-boosting family — the tool a competition-mined index would over-represent above all others — is affirmative evidence in the authors' favour, not merely a null result.[^7][^4]
:::

And now the limit, which is larger than the finding. The sweep audits the wrong artifact. Repo-To-Skill's MLE-bench number was produced by 75 per-competition task-oriented graphs, and the repository publishes task-oriented graphs for FrontierCS, PaperBench and PassNet — but has no MLE-bench directory.[^5] The clean library result is real, and it is beside the point.

---

## 07. Gain tracks bespokeness, and bespokeness tracks non-release

Line the paper's four headline results up next to each other and a pattern falls out that the paper never names. The size of the reported gain tracks one variable more tightly than any other: how closely the skill artifact was fitted to the individual evaluation task it was later scored on. The four raw metrics are not commensurable — an Any Medal rate, a replication score, an AS Score and a task score do not share a scale — so each series below is indexed to its own no-skill baseline at 100, which is the only honest way to put them on one axis.[^2]

:::slope(left-label="Without skills", right-label="With skills", unit="index, baseline = 100")
| Benchmark | Without | With |
|---|---|---|
| MLE-bench (Any Medal) | 100 | 234.3 |
| PaperBench (replication) | 100 | 134.4 |
| PassNet (AS Score) | 100 | 114.0 |
| FrontierCS (score) | 100 | 109.2 |
:::

The raw numbers behind that fan: MLE-bench Any Medal 31.11 to 72.89, +134.3% over n=75; PaperBench replication 29.45 to 39.59, +34.4% over 20 papers; PassNet AS Score 1.343 to 1.5313, +14.0% over 200 samples; FrontierCS 70.63 to 77.14, +9.2% over 188 Agent Track tasks.[^2] Now set that ordering beside how each skill set was actually constructed.[^2]

| Benchmark | How the skills were built | Bespokeness | Variance reported | Graphs published? |
|---|---|---|---|---|
| *MLE-bench | 75 separate per-competition graphs, web search plus "bounded diagnostic trials" | Highest — one artifact per scored task | ± SEM over three runs; no CI, no significance test | No [^5] |
| PaperBench | 636 paper-derived skills from 153 source papers, gated per target paper | High — gated per target paper | None | Yes — 20 per-paper directories [^5] |
| PassNet | One benchmark-level graph, refined on the benchmark's own training split | Medium — tuned on in-distribution data | None | Yes — 6 skills [^5] |
| FrontierCS | One recovery-oriented graph shared across all 188 tasks, frozen before evaluation | Lowest — frozen, task-agnostic | Paired bootstrap 95% CI | Yes — 1 graph, 8 sub-skills [^5] |

The ordering of the gain column and the ordering of the bespokeness column are the same ordering. So, inverted, is the statistical-rigour column. FrontierCS — the smallest gain, the least bespoke artifact — is the {accent}only{/} benchmark in the paper carrying an inferential statistic: "A paired bootstrap over all 188 tasks yields a 95% confidence interval of [3.41,9.83] points for the mean improvement".[^2] MLE-bench, the largest gain, reports ± SEM over three repeated runs with no confidence interval and no significance test. PaperBench and PassNet report no variance at all.[^2] The claim that would need the most statistical support has the least.

And it is the only one you cannot inspect. The AREX-Skill repository's `skills/task-oriented/` directory contains exactly three subdirectories — FrontierCS, PaperBench and PassNet.[^5] There is no MLE-bench directory. Of four benchmark artifacts, the withheld one is precisely the most bespoke, the highest-scoring and the thinnest-evidenced. A smaller tell in the same repo: `skills/README.md` still describes `task-oriented/` as "reserved for future expansion" and "To be added in a future version" while the directory already holds three benchmark graphs.[^4]

The paper does offer a mechanism, but only inside a benchmark: "The improvement is markedly larger in relative terms on tasks where Codex without skills starts from a low replication score".[^2] That is a real and testable within-benchmark effect. It is not a cross-benchmark explanation, and the authors never give one for why MLE-bench gained 4–15 times more in relative terms than the other three.

PaperBench is where the per-task texture is visible: 18 of 20 papers improved and 2 regressed.[^2]

:::compare
- {role: LOWEST, name: "stay-on-topic", value: "-4.52"}
- {role: HIGHEST, name: "rice", value: "+40.57"}
- {role: SUBJECT, name: "20-paper mean", value: "+10.14"}
:::

`rice` moved 7.94 to 48.51; `sequential-neural` 41.67 to 65.37; `what-will-my-model-forget` 9.35 to 30.45; `lca-on-the-line` 22.08 to 39.59; `pinn` 40.64 to 58.10.[^2] The regressors are `sample-specific-masks` (57.11 to 52.04) and `stay-on-topic` (32.31 to 27.79).[^2] The authors read them as retrieval failures: "Both have no-skill scores above the 20-task average (29.45), suggesting a possible retrieval-precision failure," and "following the retrieved skill may pull the agent away from an approach it would have converged on unaided".[^2] Plausible — but note the shape of the evidence. Both regressors started above average, which is equally consistent with regression to the mean under run-to-run noise, a possibility the authors do not address and, absent per-paper variance, cannot rule out.[^2]

PassNet has the same asymmetry in miniature. G-Mean rises 1.5891 to 1.6688, Correctness 81.35% to 90.76%, failed cases fall 14 to 5 — while `Fast_1` regresses 28.48% to 26.72% and goes undiscussed.[^2] "AS" is never expanded anywhere in the paper: the headline metric is ==not defined==.[^2]

FrontierCS, the most disciplined arm, carries the one usage confound the authors do try to close. Skills raised steps 55.9 to 88.7, tokens 2.46M to 4.47M (+81.7%) and tool calls 64.7 to 105.0, for +6.51 points; the defence is that "Spearman's ρ is 0.006 for tokens, 0.014 for steps, and 0.015 for tool calls," therefore "Additional usage alone does not account for the score improvement".[^2] The inference does not follow. A near-zero *within-condition, per-task* rank correlation does not rule out a *between-condition level* effect: if extra compute lifts nearly every task by a similar amount, cross-task correlation sits at about zero while the entire mean shift is usage-driven. The control that would settle it is a usage-matched baseline arm, which was not run. In the authors' favour, the 102 tasks with no sub-agent invocation still gained 5.54 points against 7.66 on the 86 that used sub-agents — real evidence, though not the missing arm.[^2]

One tempting story does not survive contact with the details: that the ordering tracks how publicly available the answers are. PaperBench covers 20 ICML 2024 papers whose original code *is* public, which is exactly why each task ships a blacklist of disallowed sites including the paper's own codebase.[^34] FrontierCS goes the other way — "Reference solutions are withheld, while the algorithmic test cases are now released for local and batch evaluation".[^35] Public-solution availability therefore does not order these benchmarks uniformly, and anyone advancing a simple contamination narrative has to concede that.

Bespokeness does order them. An artifact built per task, with diagnostic trials run on that task, is doing something categorically different from a frozen general artifact applied unchanged to 188 unseen problems — and the paper's own four numbers separate those two regimes cleanly, without any need to allege that an answer key leaked.[^2]

---

## 08. What skills do when someone else measures them

A single lab's number means what the surrounding literature says it means. On agent skills, that literature now exists — a dozen-odd papers in 2026 measuring the same object with paired designs, ablations, and held-out repositories — and it converges on a three-joint failure chain: selection breaks as the pool grows, the average published skill is inert, and whatever does work decays without announcing itself. Each joint is measured independently, by different groups, on different substrates. Read together they set the prior against which a +41.78-point jump has to be interpreted.[^2]

**Joint one: selection breaks with scale.** "Demystifying Agent Skills: Why They Work—Until They Don't" (14 Aug 2026) reports the cleanest version: "Retrieval is a separate bottleneck: as pools grow from 5 to 100, actual-use precision falls from 29.6% to 3.3%."[^16] A second study, scaling to a 202-skill library, finds performance degrading "by up to 21% when scaling from a small set of helpful skills to a 202-skill library" and identifies "skill selection failure, not the enlarged context, is the primary bottleneck" — a two-author paper, so less scrutinised than the larger efforts, but pointing the same direction.[^19]

The nuance matters and is routinely dropped. The Demystifying authors also find that exact ground-truth invocation is "neither sufficient nor necessary," and downstream success held steady under confusable distractors.[^16] Precision collapse is therefore not automatically task-failure collapse: an agent can pull the "wrong" skill and still solve the problem. What the finding establishes is that at pool scale you no longer know *which* artifact produced the outcome — which is a measurement problem before it is a performance problem.

The same paper's mechanism finding cuts deeper into the standard story: "Procedural anchoring accounts for 65.7% of skill cases, versus 4.5% for explicit knowledge injection."[^16] If that holds, skills mostly work by stabilising behaviour, not by supplying facts — which undercuts the "externalised operational knowledge" framing that motivates mining thousands of skills out of repositories. The caveat is real: this comes from open-coded trajectory analysis (238 valid labels from 240 records, normalised over 8,135 trials), that is, human and LLM coding, not an execution metric.[^16]

Anthropic's own design rationale is worth stating fairly here, because it explains the architecture rather than defends it. The Agent Skills spec is built on progressive disclosure: a skill's `name` and `description` are pre-loaded so the system "provides just enough information for Claude to know when each skill should be used," making "the amount of context that can be bundled into a skill" effectively unbounded.[^36] The design is elegant and the unbounded-body property is genuinely useful. It also routes every selection decision through the description field alone — precisely the mechanism the retrieval literature measures failing as pools grow.[^16]

**Joint two: the average published skill does nothing.** SWE-Skills-Bench, "Do Agent Skills Actually Help in Real-World Software Engineering?" (16 Mar 2026), ran a paired with/without design over real repositories — 49 skills, about 565 instances, 6 subdomains — and found that "39 of 49 skills yield zero pass-rate improvement," that "the average gain is only +1.2%," and that "three degrade performance (up to -10%)," with token overhead reaching +451%.[^18] Seven skills did help, the best by +30%: the distribution is a long tail of nothing with a short head of something.[^18]

The counterweight is stronger than the sceptics usually admit. A large multi-author benchmark of hand-curated skills reports that "Curated Skills raise the average pass rate from 33.9% to 50.5% (+16.6 percentage points; 25.5% normalized gain)," ranging +4.1 to +25.7 points across 18 model-harness configurations.[^20] Skills can work, substantially. But the same paper concludes that "Focused Skills with at most three modules outperform larger or exhaustive bundles"[^20] — the field's strongest pro-skill result is an argument against library scale. And "Curated" is doing the work: these are hand-selected, not retrieved from a pool, so the number is a ceiling the retrieval literature says you cannot reach at scale.

Two adjacent results sit in the same register. A controlled study of repository-level context files for coding agents found that "providing context files does not generally improve task success rates, while increasing inference cost by over 20% on average".[^21] And a retrieval-over-skills system reports Pass@1 rising "from 9.2% to 16.4% (+78.3%" on one benchmark — a 7.2-point absolute move off a 9.2% floor — while on a second benchmark "agents readily use the retrieved skills (70.1% use rate) yet show no performance gain".[^22] Usage is not efficacy.

**Joint three: decay is silent.** Repo2Skill-Evo, "Repository Skills Go Stale in Silence" (22 Aug 2026), tracked 105 release transitions across 57 repositories and found that "every evaluated transition invalidates part of the V1 skill set," with six frontier agents reaching "only 29.9%-69.7% avg@3 macro F1" on the repair task.[^17] The load-bearing finding is architectural: after a release, a skill "may become stale without raising any explicit signal, while continuing to provide obsolete guidance".[^17] Nothing in the retrieval path can see that. The 105 transitions were selected rather than randomly sampled, which plausibly inflates the 100% invalidation rate.[^17]

| Study | Design | Headline effect | What it implies for a 5,353-skill library |
|---|---|---|---|
| Demystifying Agent Skills | Pool-size sweep, 5 to 100, plus trajectory coding | Use precision 29.6% to 3.3%; anchoring 65.7% vs 4.5% injection [^16] | At 5,353 the pool is 50x the largest tested; selection is unmeasured, not merely degraded |
| 202-skill shadowing study | Scaling from a helpful subset to 202 skills | Up to 21% degradation; selection failure is the bottleneck [^19] | Adding skills can subtract performance well before this scale |
| *SWE-Skills-Bench | Paired with/without, 49 skills, ~565 real instances | 39/49 zero gain; mean +1.2%; 3 harmful; +451% tokens [^18] | Most of a mined library is expected to be inert or costly |
| Curated Skills benchmark | Hand-curated, 18 model-harness configs | 33.9% to 50.5% (+16.6 pts), range +4.1 to +25.7 [^20] | The best case is hand-selection with at most 3 modules |
| Repo2Skill-Evo | 105 release transitions, 57 repos | Every transition invalidates part of V1; 29.9–69.7% F1 repair [^17] | Staleness accrues invisibly and is not detectable from loadability |
| Repository context files | Controlled with/without context files | No general success-rate gain; >20% cost increase [^21] | Shipping more repo context is neither free nor automatically useful |

The most relevant positive result is HASTE, "Why Solve It Twice? Hierarchical Accumulation of Skills for Transfer-Efficient ML Engineering" (arXiv:2606.30911, 29 June 2026, DL4C workshop at ICML 2026), which reports a 77.3% medal rate on MLE-bench Lite with Claude Sonnet 4.6 at a 12-hour budget — explicitly "a single-seed campaign result," with multi-seed replication named as the top follow-up.[^45] Its controlled ablation is the more useful artifact: holding a 159-skill inventory constant across 8 competitions, tiered loading reaches a 100% medal rate while flat loading reaches 62.5% — matching loading no skills at all, at twice the output tokens.[^45] Structure, not inventory, carried the gain.

:::callout(kind=info, label="Split discipline")
HASTE's 77.3% is on MLE-bench Lite — the easiest 22 competitions — not the full 75.[^45] It is not comparable to a full-75 figure, and conflating the two splits is the most common error in this literature. Any cross-paper comparison that does not name the split is uninterpretable.
:::

Which puts the headline number in its distribution. Independent effect sizes cluster at +1.2 points for the average published skill,[^18] +16.6 points for hand-curated skills in the best-case study,[^20] and 7.2 points absolute for retrieval over a large pool.[^22] Repo-To-Skill reports +41.78 points.[^2]

:::compare
- {role: LOWEST, name: "SWE-Skills-Bench mean", value: "+1.2 pts"}
- {role: HIGHEST, name: "Curated Skills benchmark", value: "+16.6 pts"}
- {role: SUBJECT, name: "Repo-To-Skill, MLE-bench", value: "+41.78 pts"}
:::

That is roughly two and a half times the best independently-measured effect and an order of magnitude above the typical one. An unusually large effect is not evidence of misconduct — breakthroughs are, definitionally, outliers, and every result in the table above was once nobody's prior. But when a number sits that far outside the distribution, the disciplined next question is what is different about the measurement, not what is different about the method.

---

## 09. Sixteen months of MLE-bench, and where 72.89 sits

A single benchmark number is unreadable without its curve. MLE-bench's public leaderboard has one, and it is steep. When the benchmark shipped in October 2024, the best full-75 "Any Medal" score on the board was AIDE + o1-preview at 17.12 ± 0.61.[^10] The 2024 field behind it was thinner still: AIDE + gpt-4o at 8.63 ± 0.54, AIDE + claude-3-5-sonnet at 7.56 ± 1.60, OpenHands + gpt-4o at 4.89 ± 0.44, AIDE + llama-3.1-405b at 3.33 ± 0.38, and MLAB + gpt-4o at 1.60 ± 0.27.[^10] The last accepted entry, Famou-Agent 2.0 + Gemini-3-Pro-Preview on 2026-02-23, sits at 64.44 ± 1.18.[^10] By my arithmetic that is +47.32 points across roughly 16.5 months — a mean of about 2.9 points per month, sustained, with no visible plateau at the top.

:::line-chart(title="MLE-bench full-75 Any Medal, running best", subtitle="Official leaderboard, %")
x: 2024-10,2025-05,2025-07,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02
Best public: 17.12,31.60,34.22,36.44,43.56,48.44,59.56,61.33,64.44
:::

:::source
Running maximum of the "All %" column, assembled from the dated rows of the official MLE-bench leaderboard: AIDE + o1-preview (2024-10-08), AIRA-dojo + o3 (2025-05-15), Neo (2025-07-28), InternAgent + deepseek-r1 (2025-09-12), Famou-Agent + Gemini-2.5-Pro (2025-10-10), Thesis + gpt-5-codex (2025-11-10), Famou-Agent 2.0 + Gemini-2.5-Pro (2025-12-27), PiEvolve (2026-01-05) and Famou-Agent 2.0 + Gemini-3-Pro-Preview (2026-02-23).[^10]
:::

Against that slope, Repo-To-Skill's 72.89% is not an outlier in kind. It is one large step ahead of a line that has been stepping the whole time. The paper itself makes the comparison explicitly, reporting a move "from 64.44% to 72.89% (+8.45 points)" over the strongest public baseline, with tier-level gains of 6.06 (Low), 5.26 (Medium) and 15.55 (High) points.[^2] An 8.45-point jump is roughly three months of trend. Systems on this board have delivered comparable single-entry jumps before — Leeroo posted 50.67 ± 1.33 on 2025-12-07 and Famou-Agent 2.0 posted 59.56 ± 0.89 on 2025-12-27, an 8.89-point move in twenty days.[^10]

:::timeline
- {date: 2024-10, headline: "MLE-bench released", body: "AIDE + o1-preview sets the opening full-75 mark at 17.12 ± 0.61."}
- {date: 2025-05, headline: "AIRA-dojo passes 30", body: "AIRA-dojo + o3 reaches 31.60 ± 0.82, the first entry above thirty."}
- {date: 2025-12, headline: "ML-Master 2.0 passes 55", body: "56.44 ± 2.47 with DeepSeek-V3.2-Speciale; three record holders inside one month."}
- {date: 2026-02, headline: "64.44, the last accepted entry", body: "Famou-Agent 2.0 + Gemini-3-Pro-Preview, 64.44 ± 1.18, on 2026-02-23."}
- {date: 2026-04, headline: "OpenAI pauses submissions", body: "The repo README, dated 04-24-2026, closes the board pending a fairness review."}
- {date: 2026-09, headline: "Repo-To-Skill claims 72.89", body: "Announced against a leaderboard that has recorded no movement since February."}
:::

The timing is the part worth stating plainly, and neutrally. The repo README, dated 04-24-2026, reads: "We are currently not taking any new submissions to the leaderboard while we develop an improved process for ensuring submissions are fair and comparable."[^10] Nothing moved on the board between March and September 2026 because nothing could.[^10] So 72.89% cannot presently be listed, re-graded, or independently placed alongside the entries it is measured against. That is a fact about the calendar, not about the authors.

It also flatters the trend line more than the trend line deserves. The 2.9-points-a-month figure is computed over a protocol that drifted underneath it.[^10] Runtime budgets are not normalised: entries run at 12h, 24h and 36h, with MLEvolve, InternAgent and R&D-Agent's best configuration at 12h, Neo at 36h, and 24h as the canonical default.[^10] A leaderboard footnote concedes that some rows were "Computed by padding incomplete seeds with failing scores".[^10] The top entry is a multi-model system, primarily driven by Gemini-3-Pro-Preview with a subset of modules on GPT-5 and GPT-5-mini.[^10] And a separate table exists for entries flagged "Test-set feedback," explicitly "not directly comparable to the main leaderboard": Disarray at 77.78 ± 0.44 and LoongFlow at 62.66.[^10] Disarray's number is higher than Repo-To-Skill's — and it is precisely the entry the maintainers segregated.

The other way to misread this board is by split. The leaderboard's "Low" column is labelled "Low == Lite (%)" — Lite *is* the 22-competition Low-complexity split, not a lighter grading of the full set.[^10][^9] The same-system gaps are wide enough to swallow a whole thesis.

| System | Low == Lite (%) | All 75 (%) | Gap (pts) |
|---|---|---|---|
| *AIDE + o1-preview | 35.91 | 17.12 | 18.79 |
| R&D-Agent + gpt-5 | 68.18 | 35.11 | 33.07 |
| MLEvolve | 80.30 | 61.33 | 18.97 |

:::note
Gap column is my arithmetic from the two published columns.[^10] Papers reporting "MLE-bench" without naming a split cannot be placed on this chart without reading the leaderboard or the full text.[^10][^9]
:::

Two prominent systems are routinely misfiled this way. MLE-STAR (Google) reports winning medals in 64% of competitions on MLE-bench Lite, and has no full-75 leaderboard entry at all.[^33] AIRA-dojo's headline "39.6% to 47.7%" is also Lite; its full-75 figure is the 31.60 in the chart above.[^30][^10]

Finally, the baseline. Repo-To-Skill's no-skill arm is vanilla Codex on a GPT-5.5 backbone at 31.11 ± 2.22.[^2] On the public board, "Thesis" with gpt-5-codex scored 48.44 ± 3.64 back in November 2025 — a stronger scaffold on a comparable-generation model.[^10] The 31.11 is therefore not the state of the art being improved on; it is an unscaffolded control, which makes the 134.3% relative gain partly a statement about how weak vanilla Codex is. In the authors' defence, that is exactly the claim they make: skills added to "vanilla Codex with added distilled skills, without a custom execution harness, specialized agent orchestration strategy, or modified control loop".[^2] The measurement discipline is the softer spot. MLE-bench's guidance is at least three seeds reported as mean ± SEM, yet its own headline rows used 16 seeds for o1-preview + AIDE and 36 for gpt-4o + AIDE.[^9] Repo-To-Skill reports three repeated runs.[^2] Against a metric whose pass@6 roughly doubles pass@1, three is thin.[^9]

---

## 10. The experiment that would settle it, and the rulebook that doesn't ask for it

Everything above is inference from a published artifact, which is a weak position to argue from. It is worth being honest about why the stronger evidence is missing: not because it is expensive to produce, but because nobody was ever asked to produce it. Four experiments would resolve the exposure question in weeks. Each has a published precedent inside this same literature. None of them requires taking anyone's word for anything.

:::kv
- {term: Compute-matched control, def: "Give the baseline the extra exploration budget instead of the skills. MLE-bench's own ablations show budget alone moves the metric."}
- {term: Domain-blocklist ablation, def: "Rebuild the skill graphs with kaggle.com and solution repositories excluded, then re-run. A search-contamination study measured exactly this effect."}
- {term: Post-cutoff held-out tasks, def: "Freeze the graphs, then evaluate on competitions that closed afterwards. LiveCodeBench scores both sides of a release-date boundary."}
- {term: Per-competition disclosure, def: "Publish the graphs, the retrieved URLs and per-competition results, then correlate performance with public-solution availability."}
:::

The first test is one the benchmark's own authors already ran. Skills are not free: building 75 task-oriented graphs consumes search, tokens and wall-clock that the baseline never receives. MLE-bench establishes that this axis is live — "GPT-4o scores 8.7% given 24 hours to attempt each competition, but 11.8% when given 100 hours", and "o1-preview's score doubles from 16.9% using pass@1 to 34.1% using pass@8".[^9] The pattern generalises: repeated sampling alone raises SWE-bench Lite coverage from 15.9% to 56%.[^44] Until the baseline is handed the same budget as undirected exploration, a gain attributed to skills is partly a gain attributable to spending.

The second test is the load-bearing one, because the exposure at issue is a pre-run web search rather than pretraining. The precedent is precise and comes with a measured effect size: a study logged the URLs a search agent retrieved, labelled each question contaminated by whether an answer-bearing domain was hit, then re-ran the same questions with that domain blocked — "we observe a drop in accuracy on the contaminated subset of approximately 15%."[^24] Its five-condition ladder is directly transplantable: Default, No-Search, Blocked-domain, Only-that-domain, Date-cutoff.[^24] One caveat matters. A single-domain blocklist is a floor, not a fix; mirrors and forums carry the same write-ups under different hostnames, so a null result under a kaggle.com block is weak evidence of no exposure while a positive result is strong evidence of it. A closer-to-home datapoint, which belongs in an appendix as the weaker of the two: removing Kaggle competition write-ups from an ML agent's retrieval corpus cost 13.3 points versus 7.8 for removing arXiv.[^47]

The third test freezes the graphs and evaluates on competitions that closed afterwards. LiveCodeBench annotates problems with release dates and scores both sides of a model's cutoff; one model's LeetCode Pass@1 falls from roughly 60 on May 2023 problems to roughly 0 on September 2023 problems.[^28] Read the limit carefully: this detects *pretraining* contamination and does not by itself defeat inference-time retrieval. A post-cutoff competition whose solution is already sitting in a public notebook remains fully exposed to a live web search.

The fourth test is disclosure plus a regression, and it is the cheapest of the four. Publish the 75 graphs, the retrieved source URLs, and a per-competition result table, then correlate performance with public-solution availability. The precedent regressed per-problem success on whether the problem's solution appears on GitHub and found the effect significant before the training cutoff and null after — odds ratio 1.045 (CI 1.039–1.051, p<0.001) pre-cutoff versus 1.000 (0.986–1.014, p=0.988) post-cutoff, over 6,738 pre and 1,378 post observations.[^29] Its negative control is the transferable part: GitHub presence had no effect on merely reproducing problem titles, so the measured effect is on solving, not recall.[^29]

An optional fifth is worth the trouble: transfer the published artifact into an independent harness. AIRA-dojo re-ran the identical published AIDE-greedy o1-preview agent in their own environment and the medal rate rose from 35.2% to 45.9% — harness alone, no method change, a larger swing than their own method contribution.[^30]

| Test | What it isolates | Published precedent | Effect size at precedent |
|---|---|---|---|
| Compute-matched control | Budget versus method | MLE-bench ablations [^9] | 8.7% to 11.8% (24h to 100h); 16.9% to 34.1% (pass@1 to pass@8), full 75 |
| *Domain-blocklist ablation | Retrieval-time exposure | Search-contamination ladder [^24] | ~15% accuracy drop on the contaminated subset |
| Post-cutoff held-out tasks | Pretraining contamination only | LiveCodeBench [^28] | LeetCode Pass@1 ~60 to ~0 across the cutoff |
| Per-competition disclosure | Public-solution availability | GitHub-presence regression [^29] | OR 1.045 (1.039–1.051) pre-cutoff vs 1.000 (0.986–1.014) post |
| Independent harness transfer | Scaffold versus environment | AIRA-dojo [^30] | 35.2% to 45.9% medal rate on Lite, harness alone |

The reason to run any of this is that audits of this kind have repeatedly deflated headline numbers. An independent audit of SWE-bench found "32.67% of the successful patches involve 'cheating' as the solutions were directly provided in the issue report or the comments", cutting SWE-Agent + GPT-4 on Verified from 22.4% to 10.0%.[^25] A second study found models identify buggy file paths from issue text alone at 76% on SWE-Bench versus 53% on non-SWE-Bench repos, and reproduce verbatim 5-grams of the fix at 35% versus 18%.[^26] Rebuilding GSM8K as a private, distribution-matched held-out set exposed accuracy drops of up to 13%, concentrated in specific model families, with memorisation probability predicting the gap.[^27]

Which brings the real payload. None of these tests is required by anything. MLE-bench's resource defaults are explicitly advisory — "not a strict requirement of the benchmark but please report if you stray from these defaults!" — and its agent-facing rules bind the agent during the graded episode only.[^10] There is no rule covering what a developer may compute *before* the run. The strictest provenance rule in the adjacent literature is SWE-bench's: submissions must include predictions, per-instance logs and trajectories, those traces must be "Generated with the inference process, not post-hoc", and maintainers "run your model on a random subset of SWE-bench and verify the results"; since November 2025 eligibility also requires an open publication and at least one academic or established-lab author.[^41] Even that says nothing about internet access or pre-task preparation. Venue policy does not close it either: NeurIPS's checklist asks for "the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments" and separately for LLM-usage disclosure, but that item is about writing and methodology, not evaluation-time retrieval.[^42] The leading agent-benchmark checklist proposal, with 26 authors, documents that benchmark flaws distort scores "by up to 100% in relative terms" and that applying it cut one benchmark's overestimation by 33 points in absolute terms; its nearest items ask that agents be isolated from ground truth and that contamination measures be designed — and it scores MLE-bench *positively* on designing "experiments to measure data contamination and agent plagiarism".[^43] None of it reaches pre-task retrieval. A benchmark can be a model citizen of every published standard and still leave this door open, which is the point: the standards were written for a world in which the agent was the only thing that touched the task.

:::timeline
- {date: 2024-07, headline: "SWE-bench requires real trajectories", body: "Submissions must ship predictions, per-instance logs and trajectories generated with the inference process, not post-hoc. Silent on internet access."}
- {date: 2024-10, headline: "MLE-bench ships contamination controls", body: "Three contamination controls plus resource defaults that are explicitly advisory, not a strict requirement."}
- {date: 2025-11, headline: "SWE-bench adds eligibility rules", body: "Open publication and at least one academic or established-lab author required: provenance of people, still not of preparation."}
- {date: 2026-04, headline: "OpenAI pauses MLE-bench submissions", body: "Leaderboard paused on 2026-04-24 to develop an improved process for ensuring submissions are fair and comparable."}
- {date: 2026-09, headline: "72.89% reported under no disclosure rule", body: "Repo-To-Skill reports its headline number with no venue, benchmark or checklist requirement to disclose pre-task preparation."}
:::

Read as a sequence, the governance record tightens steadily on what happens *during* a graded episode and never once addresses what happens before it.[^41][^42][^43] A paper can be fully compliant with every rule in force and still be unauditable. The pause is the one institutional act that treats this as a problem rather than an oversight.[^10]

:::statement(attr="ARA Research")
Publish the 75 task-oriented skill graphs and the retrieved source URLs for the four High-complexity competitions that no non-flagged public system had previously medalled.
:::

That single artifact would move the claim from unfalsifiable to settled in an afternoon — and if the claim is sound, it costs its authors nothing.

---

## 11. What would break this thesis

The argument in this piece is deliberately narrow: not that Repo-To-Skill cheated, but that the reported number measures per-task preparation rather than the library it is named for, and that nobody can currently check the difference. Several things would break it, and it is worth naming them precisely.

**The 75 graphs could turn out to be boring.** If the authors publish them and they read like the library skills do — API discipline, failure-recovery patterns, "check your submission format before you spend eight hours training" — then the contamination framing collapses entirely and what remains is a strong result about operational scaffolding. That is a live possibility, and the library audit in section 06 makes it the *more* likely outcome, not the less. Every skill body inspected in the published repository contains procedure and no results.[^8]

**The compute asymmetry could be smaller than the ceilings suggest.** Table 5 reports budget caps, not consumption.[^3] If the exploration phase typically used two GPU-hours rather than twenty-four, the 2x figure in section 03 overstates the gap by an order of magnitude. Only the authors can settle that, and they have not reported it.[^2]

**The High-split result could survive per-competition disclosure intact.** Three of the fifteen High competitions are gold-medalled by every strong agent tested, and four more are medalled by several.[^14][^15] A 9-of-15 result composed mostly of competitions the field already solves would be unremarkable rather than suspicious. The number is only alarming if the new medals land on the four that nobody has cracked — and that is precisely the fact the paper's aggregate reporting hides in both directions.

**The independent-effect-size argument could be a category error.** Section 08 places +41.78 points against a literature clustering at +1.2 to +16.6.[^18][^20] But none of those studies gave an agent a per-task artifact built with trials on the target task. If task-oriented distillation is genuinely a different mechanism from library retrieval — which the paper explicitly claims — then comparing their effect sizes is comparing two different interventions, and the outlier framing loses force.

**An adversarial pass found nothing.** Before publication the three load-bearing claims here — that the library did not produce the number, that the 31.11-to-72.89 move is correctly transcribed and is the largest gain claimed on this benchmark, and that the exploration budget is one-sided — were each put through independent searches for contradicting primary or secondary sources. All three came back with no contradiction found, 3 of 3.[^1][^2][^3] That raises shipping confidence; it is not proof, because on a four-day-old paper an absence of contradicting coverage partly reflects an absence of coverage.

**The whole contamination frame could be the wrong lens.** The strongest evidence in this article is not that answers leaked. It is that four benchmarks in one paper produce gains ordered exactly by how tightly each skill artifact was fitted to its evaluation task, with statistical rigour running inversely to gain size, and with the most tightly-fitted artifact withheld.[^2][^5] That pattern is fully consistent with an honest, well-executed study whose headline framing outran its evidence. It is also fully consistent with something worse. The point of section 10 is that the discipline currently has no mechanism that distinguishes them.

Two counter-arguments deserve more weight than they usually get. First, the authors disclosed everything this article relies on. The two-stage protocol, the budget exclusion, the per-competition graph construction, the exclusion rule's exact wording, the count that omits task-oriented graphs — all of it is in the paper, in plain language, in sections a reader can find.[^2][^3] A team hiding something does not write Table 5. Second, their central claim is narrower than the coverage of it: skills added to "vanilla Codex … without a custom execution harness, specialized agent orchestration strategy, or modified control loop".[^2] Against a 31.11% unscaffolded control that is a defensible thing to measure, even if the resulting relative figure travels badly.

What does not survive scrutiny is the sentence the result is being read as. A 5,353-skill library you can `git clone` today has not been shown to lift a research agent by 134% on MLE-bench, because that library was not in the experiment.[^2] Until the 75 graphs exist in public, the honest label for the 72.89% is neither capability nor contamination. It is unaudited.

:::references
- {id: 1, title: "Repo-To-Skill: Distilling GitHub Repositories Into AI4AI Skills (abstract)", url: "https://arxiv.org/abs/2609.02749", source: arXiv, date: "2026-09-02"}
- {id: 2, title: "Repo-To-Skill, full text (HTML)", url: "https://arxiv.org/html/2609.02749v1", source: arXiv, date: "2026-09-02"}
- {id: 3, title: "Repo-To-Skill, full text including Appendix A.2.1 and Table 5", url: "https://huggingface.co/papers/2609.02749", source: Hugging Face Papers, date: "2026-09-02"}
- {id: 4, title: "AREX-Skill: A Skill Library for Automated Machine Learning", url: "https://github.com/VectorSpaceLab/AREX-Skill", source: GitHub, date: "2026-09-06"}
- {id: 5, title: "AREX-Skill task-oriented skill graphs directory", url: "https://github.com/VectorSpaceLab/AREX-Skill/tree/main/skills/task-oriented", source: GitHub, date: "2026-09-06"}
- {id: 6, title: "AREX-Skill router build metadata and repository catalog", url: "https://raw.githubusercontent.com/VectorSpaceLab/AREX-Skill/main/skills/repositories/repo-skills-router/references/index/build-metadata.json", source: GitHub, date: "2026-09-06"}
- {id: 7, title: "AREX-Skill family index: data-science / tabular-modeling", url: "https://raw.githubusercontent.com/VectorSpaceLab/AREX-Skill/main/skills/repositories/repo-skills-router/references/families/data-science/tabular-modeling.md", source: GitHub, date: "2026-09-06"}
- {id: 8, title: "AREX-Skill timm sub-skill: benchmarking-and-results", url: "https://raw.githubusercontent.com/VectorSpaceLab/AREX-Skill/main/skills/repositories/repo-skills/timm/sub-skills/benchmarking-and-results/SKILL.md", source: GitHub, date: "2026-09-06"}
- {id: 9, title: "MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering", url: "https://arxiv.org/html/2410.07095v6", source: "arXiv / OpenAI", date: "2025-02-26"}
- {id: 10, title: "openai/mle-bench: benchmark repository, rules and leaderboard", url: "https://github.com/openai/mle-bench", source: GitHub, date: "2026-09-06"}
- {id: 11, title: "MLE-bench agent instructions (environment/instructions.txt)", url: "https://raw.githubusercontent.com/openai/mle-bench/main/environment/instructions.txt", source: GitHub, date: "2026-09-06"}
- {id: 12, title: "MLE-bench medal threshold logic (mlebench/grade_helpers.py)", url: "https://raw.githubusercontent.com/openai/mle-bench/main/mlebench/grade_helpers.py", source: GitHub, date: "2026-09-06"}
- {id: 13, title: "MLE-bench High-complexity split (experiments/splits/high.txt)", url: "https://raw.githubusercontent.com/openai/mle-bench/main/experiments/splits/high.txt", source: GitHub, date: "2026-09-06"}
- {id: 14, title: "MLE-bench per-competition grading report, AIRA-dojo group 1", url: "https://media.githubusercontent.com/media/openai/mle-bench/main/runs/aira-dojo_group1/grading_report_1.json", source: GitHub, date: "2026-09-06"}
- {id: 15, title: "MLE-bench per-competition grading report, AIBuildAI group 1", url: "https://media.githubusercontent.com/media/openai/mle-bench/main/runs/aba_group1/grading_report_group_1.json", source: GitHub, date: "2026-09-06"}
- {id: 16, title: "Demystifying Agent Skills: Why They Work—Until They Don't", url: "https://arxiv.org/abs/2608.14036", source: arXiv, date: "2026-08-14"}
- {id: 17, title: "Repo2Skill-Evo: Repository Skills Go Stale in Silence", url: "https://arxiv.org/abs/2608.21964", source: arXiv, date: "2026-08-22"}
- {id: 18, title: "SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering?", url: "https://arxiv.org/abs/2603.15401", source: arXiv, date: "2026-03-16"}
- {id: 19, title: "Skill shadowing and selection failure at library scale", url: "https://arxiv.org/abs/2605.24050", source: arXiv, date: "2026-05-21"}
- {id: 20, title: "Curated agent skills: a multi-configuration benchmark", url: "https://arxiv.org/abs/2602.12670", source: arXiv, date: "2026-02-13"}
- {id: 21, title: "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?", url: "https://arxiv.org/abs/2602.11988", source: arXiv, date: "2026-02-12"}
- {id: 22, title: "SkillFlow: Scalable and Efficient Agent Skill Retrieval System", url: "https://arxiv.org/abs/2504.06188", source: arXiv, date: "2026-03-27"}
- {id: 23, title: "Search-Time Contamination in retrieval-augmented agents", url: "https://arxiv.org/html/2606.05241", source: arXiv, date: "2026-06-03"}
- {id: 24, title: "Measuring search-time contamination in deep-research agents", url: "https://arxiv.org/html/2508.13180", source: "arXiv / Scale AI", date: "2025-08-12"}
- {id: 25, title: "SWE-Bench+: Enhanced Coding Benchmark for LLMs", url: "https://arxiv.org/html/2410.06992v2", source: arXiv, date: "2024-10-10"}
- {id: 26, title: "Remember Instead of Reason: memorisation in SWE-bench Verified", url: "https://arxiv.org/abs/2506.12286", source: arXiv, date: "2025-06-14"}
- {id: 27, title: "A Careful Examination of Large Language Model Performance on Grade School Arithmetic (GSM1k)", url: "https://arxiv.org/abs/2405.00332", source: "arXiv / Scale AI", date: "2024-05-01"}
- {id: 28, title: "LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code", url: "https://arxiv.org/abs/2403.07974", source: arXiv, date: "2024-03-12"}
- {id: 29, title: "Data Contamination Through the Lens of Time (GitHub presence regression)", url: "https://ar5iv.labs.arxiv.org/html/2310.10628", source: arXiv, date: "2023-10-16"}
- {id: 30, title: "AIRA-dojo: AI Research Agents and the search-scaffold gap", url: "https://arxiv.org/html/2507.02554v2", source: "arXiv / Meta", date: "2025-11-04"}
- {id: 33, title: "MLE-STAR: Machine Learning Engineering Agent via Search and Targeted Refinement", url: "https://arxiv.org/abs/2506.15692", source: "arXiv / Google", date: "2025-08-28"}
- {id: 34, title: "PaperBench: Evaluating AI's Ability to Replicate AI Research", url: "https://arxiv.org/abs/2504.01848", source: "arXiv / OpenAI", date: "2025-04-02"}
- {id: 35, title: "FrontierCS benchmark repository", url: "https://github.com/FrontierCS/Frontier-CS", source: GitHub, date: "2026-09-06"}
- {id: 36, title: "Equipping agents for the real world with Agent Skills", url: "https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills", source: Anthropic, date: "2025-10-16"}
- {id: 37, title: "Kaggle Solutions: curated index of competition solutions", url: "https://github.com/faridrashidi/kaggle-solutions", source: GitHub, date: "2026-08-06"}
- {id: 38, title: "1st place solution, Google Research Identify Contrails", url: "https://github.com/junkoda/kaggle_contrails_solution", source: GitHub, date: "2023-08-01"}
- {id: 39, title: "1st place solution, RSNA Screening Mammography Breast Cancer Detection", url: "https://github.com/dangnh0611/kaggle_rsna_breast_cancer", source: GitHub, date: "2023-03-01"}
- {id: 40, title: "1st place solution write-up, RSNA 2022 Cervical Spine Fracture Detection", url: "https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362607", source: Kaggle, date: "2022-11-01"}
- {id: 41, title: "SWE-bench experiments: submission and trajectory requirements", url: "https://github.com/SWE-bench/experiments", source: GitHub, date: "2025-11-18"}
- {id: 42, title: "NeurIPS Paper Checklist", url: "https://neurips.cc/public/guides/PaperChecklist", source: NeurIPS, date: "2026-01-01"}
- {id: 43, title: "The Agent Benchmark Checklist (ABC)", url: "https://arxiv.org/html/2507.02825v5", source: arXiv, date: "2025-08-07"}
- {id: 44, title: "Large Language Monkeys: Scaling Inference Compute with Repeated Sampling", url: "https://arxiv.org/abs/2407.21787", source: arXiv, date: "2024-07-31"}
- {id: 45, title: "Why Solve It Twice? Hierarchical Accumulation of Skills for Transfer-Efficient ML Engineering (HASTE)", url: "https://arxiv.org/abs/2606.30911", source: arXiv, date: "2026-06-29"}
- {id: 47, title: "KompeteAI: retrieval-corpus ablation for ML engineering agents", url: "https://arxiv.org/abs/2508.10177", source: arXiv, date: "2025-08-14"}
- {id: 50, title: "RSNA 2022 Cervical Spine Fracture AI Challenge report", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC9771809/", source: "Radiology: Artificial Intelligence", date: "2022-12-01"}
- {id: 51, title: "1st place solution, Vesuvius Challenge Ink Detection", url: "https://github.com/ainatersol/Vesuvius-InkDetection", source: GitHub, date: "2023-06-01"}
- {id: 52, title: "AREX-Skill repository router (repo-skills-router/SKILL.md): area and family taxonomy", url: "https://raw.githubusercontent.com/VectorSpaceLab/AREX-Skill/main/skills/repositories/repo-skills-router/SKILL.md", source: GitHub, date: "2026-09-06"}
- {id: 53, title: "AREX-Skill repo-skills directory listing (skill roots and sub-skills)", url: "https://github.com/VectorSpaceLab/AREX-Skill/tree/main/skills/repositories/repo-skills", source: GitHub, date: "2026-09-06"}
- {id: 54, title: "AREX-Skill family index: training-infrastructure / deep-learning-frameworks", url: "https://raw.githubusercontent.com/VectorSpaceLab/AREX-Skill/main/skills/repositories/repo-skills-router/references/families/training-infrastructure/deep-learning-frameworks.md", source: GitHub, date: "2026-09-06"}
:::
