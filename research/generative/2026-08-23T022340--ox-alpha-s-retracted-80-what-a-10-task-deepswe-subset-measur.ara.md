---
eyebrow: REPORT · AI CODING BENCHMARKS
title: "Ox Alpha's retracted 80%: what a 10-task DeepSWE sample measured, and what the ~63% at ~47K output tokens actually settles"
deck: An 8-of-10 sample was read as a frontier signal for 24 hours before its own author walked it back. The full-suite numbers that survived — ~58% and ~63%, at flash-class token budgets — settle a different, more interesting claim.
lede: |
  On August 20, 2026, OpenRouter listed a new "stealth" reasoning model
  — `stealth/ox-alpha` — with a million-token context, image and video
  input, and a price of zero for a one-week preview [^1][^3][^2]. The
  anonymous provider declined to say who built it; the opencode terminal
  agent promoted it as free with "capacity for 100T tokens per day"
  [^2][^24]. Within about a day, developer Ben Davis (davis7) ran it
  through ten tasks of DeepSWE — a new long-horizon software-engineering
  benchmark — and got eight of ten, an "80%" that briefly outscored
  every configuration on DeepSWE's official leaderboard [^4][^8]. That
  figure has since been retracted by the people who produced and spread
  it: the full 113-task run landed at roughly 63%, and a separate full
  run was reported at 58.4% [^6][^7][^11]. What a ten-task sample can
  and cannot measure — and what a measured ~63% at ~47K average output
  tokens actually establishes — is the sharper story [^5][^6].
stats:
  - {label: "Claimed" , value: "80%", note: "8/10 on a 10-task subset"}
  - {label: "Full-suite runs", value: "58.4–63%", note: "113 tasks, community"}
  - {label: "Avg output tokens", value: "~47K", note: "winkey_h subset run"}
  - {label: "DeepSeek V4 Pro [max]", value: "62.8%", note: "official leaderboard"}
  - {label: "Claude Opus 5 [max]", value: "73.6%", note: "current official high"}
---

## 01. A stealth model arrives with a capacity claim nobody could check

The listing itself was thin. OpenRouter showed `stealth/ox-alpha` at a
1,048,576-token context window, a 131,072-token output cap, text plus
image plus video input, tool calling and structured output, and a
third-party provider that "has chosen to remain anonymous during this
preview" [^1]. The opencode account that pushed it added the hooks that
made it go viral: free for a week, "generous rate limits, near
unlimited usage," and "capacity for 100T tokens per day" [^2]. OpenRouter's
own launch post repeated the 1M context and multimodal pitch without
naming a lab [^3]. The provider not only stayed anonymous — the data
handling was described inconsistently: opencode advertised "Zero Data
Retention" while the OpenRouter listing said the provider retains
prompts and completions and does not use them for training [^8][^1].

Anonymity was half the marketing. Ox Alpha is the fifth frontier-ish
model released without attribution in about six months, and the
previous four — Zhipu's GLM-5 line, Xiaomi's MiMo-V2-Pro, and models
later tied to Ant and Meituan — were all claimed by Chinese labs [^13].
The LocalLLaMA thread that tried to fingerprint the newcomer
immediately, and run-by-run traffic on OpenRouter showed coding agents
behaving the way they behave around attention: Hermes Agent, Claude
Code, and the pi client together moved more than a trillion tokens to
the model within days of the listing [^21][^1]. The claim escalator
also started early: the "100T tokens per day" figure was amplified in
one aggregator into "1 quadrillion daily token capacity" — a unit error,
a telco-bill-grade multiplication of a number that was itself
unverifiable [^26][^9]. None of this was load-bearing evidence of model
quality; all of it was evidence of distribution strength [^8].

:::callout(kind=info, label="Reading the numbers")
The numbers in this article are pass rates, not scores. DeepSWE grades
each task pass/fail against hand-written behavioral verifiers, and the
leaderboard reports two forms: pass@1 (share of scored attempts that
pass) and pass@4 (share of tasks passed by at least one of four
rollouts) [^14][^16]. Community runs like davis7's report single-attempt
pass@1, which is the right unit for comparing to the leaderboard's
headline column — but the denominators differ wildly, which is the
point of this story [^4][^6].
:::

## 02. The 80% that left the building

The number came from one man running one sample. On August 21, davis7
posted a table from DeepSWE's 10-task smoke test, run with Pier —
DataCurve's reproduction harness — driving the same `mini-swe-agent`
already used for the official leaderboard [^22][^17][^12]:

> I ran this thing through 10 tasks on DeepSWE (so there could be a ton
> of variance in its real score, this is a subset), but uh... gpt-5.6-sol:
> 52%, fable: 65%, whatever the hell this is: 80% (was a near miss on
> the "x"s so actually over 80%). I am very confused
> — Ben Davis (davis7), X, 2026-08-21 [^4]

The caveat was in the original post, and it was specific and correct:
a ten-task sample carries enormous variance, and two of the "misses"
were near-misses at the pass/fail margin [^4][^9]. The warning did not
survive the telephone game. AICrier relayed it as "80% on a 10-task
DeepSWE sample" while noting the result was "too small to establish a
reliable benchmark lead" [^9]. Aggregators and SEO-farm tech blogs did
worse. One headline converted the subset into its opposite: "Ox Alpha
Hits 80% on Full DeepSWE Benchmark, First Run of All 113 Tasks" — a
claim nobody had run at that point — and attributed it to a researcher
who, in the corrections, was the one reporting the lower number [^10].
Another breathlessly concluded that "AI can now handle complex,
multi-step software engineering and security tasks that previously
required senior human engineers" [^28]. A third declared Ox Alpha
"beats GPT-5.6 and Claude Fable 5 at coding with 80% on DeepSWE" [^27].
Within roughly 36 hours, an 8-of-10 convenience sample had become a
frontier-defining result in three separate corners of the web [^10][^28][^27].

:::donut(center-label="10 tasks")
- {label: Passed, value: 80}
- {label: Missed, value: 20}
:::

:::source
8/10 vs 2/10 on davis7's DeepSWE subset, per his posted table [^4][^9].
:::

What made the decay possible is that pass rates were treated as
properties of the model rather than of the *sample the model happened
to draw*. davis7's own table showed the same 10 tasks scoring Sol at
52% and Fable at 65% — compatible with their 113-task leaderboard
averages of 61% and 65%, respectively, but individually noisy [^4][^14].
The Ox Alpha column was one draw of a random variable, not an estimate
[^9][^12].

## 03. What a ten-task sample can and cannot measure

The statistics are unforgiving. Eight successes in ten trials yields a
point estimate of 80%, but the two-sided 95% confidence interval —
Clopper-Pearson exact — runs from roughly 44% to 98% [^4]. A sample
that size cannot even distinguish a mediocre model from a breathtaking
one. The official leaderboard implicitly concedes this: every
configuration is run across all 113 tasks, four times per task, and
DataCurve still publishes run-to-run confidence bands — ±2.3 points
(Grok 4.6 medium), ±6.3 points (DeepSeek V4 Pro max) — because even
four full sweeps wobble [^14]. On a tenth of the tasks, the wobble is
the signal.

Two structural features of DeepSWE make small samples especially
misleading on this benchmark. First, tasks are long-horizon by design:
mean prompt length is 2,158 characters — roughly half of SWE-bench
Pro's 4,614 — yet reference solutions add a mean 668 lines across 7
files, against Pro's 120 lines across 5 [^16]. An agent that nails
nineteen of twenty sub-requirements on a task still fails the binary
verifier [^16][^15]. Second, because the verifiers are behavioral, a
task's outcome is sensitive to a single missed behavior — which is why
"near-miss" scores cluster right below the bar. The official per-task
data shows exactly this shape: `meriyah-explicit-resource-declarations`
— add parser support for `using` declarations — defeated most frontier
configurations outright, with 0-of-4 passes for GLM-5.3 max, Grok 4.6
medium, GPT-5.6 Sol max, Claude Opus 5 max and Claude Opus 4.8 max [^15][^14].

The same near-miss dynamics flipped outcome labels for Ox Alpha itself
within days. The forensic write-up accompanying the original sample
reported that Ox Alpha solved that same `meriyah` task single-shot [^12].
Yet a separate community full-suite run in progress against DeepSWE's
113 tasks — using the `opencode-go/ox-alpha-free` route — shows
`meriyah-explicit-resource-declarations` *not* solved, with 46 of 49
feature tests passing and the whole 51,469-test regression suite green:
a near-miss that is a "not solved" under the binary scheme [^19]. That
is the definition of a fragile measurement: the same model, the same
task, one attempt apart, a different verdict [^19][^12].

:::callout(kind=warn, label="Sample arithmetic")
Eight of ten passes is indistinguishable, at 95% confidence, from a
true rate anywhere in roughly 44–98%. The 80% headline was not merely
unproven; it was statistically non-informative [^4].
:::

## 04. The retraction was crowdsourced, not issued

There was no press release. The correction arrived as a small pile of
individual posts, each piling a full-suite number on the original.

- On August 21, winkey_h posted: "Ok ox-alpha has that big model smell.
  I'm getting around 63% at 47K avg output tokens on a DeepSWE subset.
  This is pareto optimal amongst open models and just shy of Grok 4.6
  compared to closed models!" [^5]
- On August 22, davis7 finished the full run and closed his own
  chapter: "Ended at ~63% NOT the 80% my first subset test got... It
  being on around Sol medium feels about right." [^6]
- The same morning, reports attributed to @henryzhangumich put a full
  113-task figure at 58.4%, "landing the model at almost identical
  performance to Claude Opus 4.8 (59%)", and a separate poster
  summarized: "The Rumored ~80% pass rate is completely incorrect"
  [^11].
- HuggingNews replaced its "80% full-run" headline with a correction
  titled "Ox Alpha Scores 58.4% on DeepSWE" [^11][^10]. A community-run
  live-status gist captured a parallel full sweep still in progress on
  the same official agent harness that morning [^22].

The two surviving full-suite figures — 58.4% and ~63% — disagree with
each other, and that disagreement is itself informative. At 113 tasks,
66 passes (58.4%) and 71 passes (62.8%) carry 95% intervals of roughly
49–68% and 53–72% respectively: statistically compatible, and both
consistent with a true rate around 60–62% [^11][^6]. The spread between
the runs is a reminder that even "full" community runs differ in the
details DataCurve pins down for its own table — reasoning effort,
harness version, concurrency — which is why the official leaderboard
still matters [^14][^18].

:::timeline
- {date: 2026-08-14, headline: "Zhipu ships GLM-5.3 (text-only)", body: "The plausible parent family of Ox Alpha lands a text-only flagship upgrade."}
- {date: 2026-08-20, headline: "Ox Alpha listed on OpenRouter", body: "Free one-week preview: 1M context, image/video input, anonymous provider."}
- {date: 2026-08-21, headline: "10-task sample posts 80%", body: "davis7's subset run: 8/10, explicitly flagged as high-variance."}
- {date: 2026-08-21, headline: "~63% at ~47K output tokens", body: "winkey_h reports a subset run near 63%, 'pareto optimal amongst open models'."}
- {date: 2026-08-22, headline: "80% retracted", body: "davis7's full run lands ~63%; separate reports put a full run at 58.4%."}
- {date: 2026-08-27, headline: "Free preview window ends", body: "Prior stealth releases in the same channel were claimed by labs at reveal."}
:::

:::source
Dates from the cited posts, listings and aggregator corrections [^2][^3][^4][^5][^6][^11][^12].
:::

## 05. What ~63% at ~47K output tokens actually settles

Measured against the official DeepSWE table (refreshed August 20, before
any sanctioned Ox Alpha run existed), the surviving community figures
put Ox Alpha in a specific, identifiable place [^14][^18].

:::rank-list
- {label: "Claude Opus 5 [max] – official", value: "73.6%", pct: 100}
- {label: "GLM-5.3 [max] – official", value: "69.0%", pct: 94}
- {label: "Grok 4.6 [medium] – official", value: "67.5%", pct: 92}
- {label: "Ox Alpha – community full/subsets (58.4–63%)", value: "~63%", pct: 86, highlight: true}
- {label: "DeepSeek V4 Pro [max] – official", value: "62.8%", pct: 85}
- {label: "GPT-5.6 Sol [medium] – official", value: "61.1%", pct: 83}
- {label: "Claude Opus 4.8 [max] – official", value: "59.0%", pct: 80}
:::

:::source
DeepSWE live leaderboard, v1.1, generated 2026-08-20; Ox Alpha row is
ARA's reading of community runs, not a DataCurve-sanctioned figure
[^14][^6][^5][^11].
:::

Implication one: if the community numbers hold, Ox Alpha is an
upper-mid agentic coder, sitting in the same band as DeepSeek V4 Pro
and GPT-5.6 Sol Medium (~60–63%), roughly five points under Grok 4.6
medium, and roughly ten under the Opus-5 frontier [^14]. It is not the
frontier-beater the 80% claimed, and Ananth's characterization — "the
80% deepswe score was completely wrong... but still impressive for a
flash model" — is the accurate synthesis [^7].

:::kv
- {term: "Claude Opus 5 [max]", def: "73.6% pass@1 · 117.6K mean out tokens · $11.84"}
- {term: "GLM-5.3 [max]",       def: "69.0% · 80.4K tokens · $3.99"}
- {term: "Grok 4.6 [medium]",   def: "67.5% · 49.8K tokens · $3.45"}
- {term: "DeepSeek V4 Pro [max]", def: "62.8% · 106.0K tokens · $0.24"}
- {term: "Ox Alpha (community)",   def: "~60–63% · ~47K tokens (one run) · free"}
- {term: "GPT-5.6 Sol [medium]", def: "61.1% · 18.4K tokens · $1.86"}
:::

Implication two, and the more durable one: the token budget is where
this model differentiates. ~47K average output tokens per task is
roughly the same order as Grok 4.6 medium's 49.8K — but at a similar
score Ox Alpha would be burning less than half the output tokens of
DeepSeek V4 Pro max (106K) [^14][^5]. winkey_h's "pareto optimal
amongst open models" is a defensible reading of that point on the
accuracy-vs-tokens frontier — with the caveat that it rests on a single
slice of the distribution and on output tokens, not wall-clock time or
cost, and davis7 added that the model "does not feel fast at all,
especially at higher reasoning levels" despite what he called a "pretty
solid" token average [^6][^5]. What the ~63% at ~47K output tokens settles, then, is
*narrower but real*: Ox Alpha is a genuinely competent agentic coder at
flash-class efficiency, not the frontier-resetting model its opening
week claimed [^6][^5][^12].

:::statement(attr="ARA Research")
The 80% aged in hours. The durable number is a 113-task needle around
60–63%, paid for with flash-class token budgets — a capability-density
story, not a frontier story.
:::

## 06. The forensics: why it matters that it's probably GLM

The open question everyone ran to — who made Ox Alpha — turned out to
be answerable, and the answer is what makes the efficiency reading
coherent. A forensic dossier assembled via direct API probes and the
public DeepSWE trial data concluded, at "roughly 90% confidence", that
Ox Alpha is Zhipu's next-generation unified multimodal GLM — a
stronger-than-GLM-5.3 checkpoint of the GLM-5V / GLM-5.5 lineage [^12].
The evidence is layered and specific [^12][^13]:

- a tokenizer identical to GLM-5.3's across 25 diverse prompts, modula
  a constant +75-token hidden wrapper, implying a shared vocabulary
  [^12][^13];
- a video-encoder budget that matches GLM-5V-Turbo token-for-token on
  identical test clips (296 tokens for a 2-second, 30fps, 360p clip),
  while MiMo, Qwen and GLM-4.6V all spend visibly differently [^12];
- the same audio-rejection behavior as GLM-5V (no audio endpoints),
  which rules out MiMo V2.5, the leading rival theory [^12];
- a decode speed within ~6% of GLM-5V-Turbo's 40B-active mixture, an
  error-string and greedy-decoding signature matching z.ai's GLM-5.3,
  and nearly identical agent cadence on DeepSWE (~117 steps/task vs
  GLM-5.3's ~124) [^12][^13].

Independent coverage put the attribution claim even more baldly:
"99 percent certain" the model belongs to the Zhipu GLM-5.x series
[^13]. Ananth's read — "ox alpha is glm 5.3 flash", a model Zhipu can
serve at 100T tokens/day because it is small — matches the capacity
story the launch sold [^7]. Zhipu did ship GLM-5.3 text-only on August
14, which would leave vision as the obvious next release, and the same
anonymous channel previously carried Pony Alpha → GLM-5 [^12][^13].

Attribution is not cosmetic here. Zhipu's own GLM-5.3 max sits at 69.0%
on the official DeepSWE table with 80.4K mean output tokens — roughly
the same class of result the community measured from Ox Alpha's ~63% at
~47K [^14]. A ~40-billion-active-parameter model holding ~63% at
flash-class token budgets is the genuinely new factoid, if forensics and
runs both hold: it frames the "100T tokens/day" fleet claim as a large
but plausible deployment of small checkpoints, not laboratory bravado,
and it makes "63% at 47K" a statement about what *efficient* models
cost, which is a different market from the one the 80% headline
described [^7][^12][^14]. None of this is officially conceded: as of
this writing no lab has claimed the model, and a minority hypothesis —
a Gemini Pro successor — still floats [^13].

## 07. Analyst position: treat the correction as a methodology lesson

The episode's most transferable output is not a number. It is the
demonstration that an n=10 sample, promoted with confidence and free
tokens, outran its own evidence within a day — and that the ecosystem,
left to itself, corrected it within another. The correction worked
because the retractors ran the *same harness on the full task set*:
full-suite runs with published methodology and near-threshold partials
[^6][^5][^11][^19]. The failure mode that produced the 80% was that a
convenience sample was announced with the confidence of a census.

:::position(confidence=medium, horizon=2026-Q4)
stance: >-
  Read the surviving figures — roughly 60–63% at ~47K average output
  tokens — as a flash-class capability-density result from a likely
  Zhipu GLM-model, not a frontier-parity claim; the durable news is how
  much competence a small checkpoint can now carry, not that it beats
  Opus or Grok.
consensus: >-
  The market and the press read the 80% as a frontier upset, then
  mostly walked it back to "strong cheap model"; the identity
  hypothesis has congealed around Zhipu without an official claim.
resolves: >-
  A DataCurve-sanctioned full-suite run (the leaderboard has yet to list
  an Ox Alpha configuration); a formal reveal or denial from a lab; and
  whether a ~40B-active model reproduces ~63% on the official harness
  within the leaderboard's confidence bands.
:::

:::note
The DeepSWE live leaderboard refreshed on August 20 contains no Ox
Alpha configuration, and the benchmark's changelog (latest entries
August 13–14) contains no mention of it [^14][^18]. Every number in the
retraction-and-correction arc is a community measurement on the
official agent harness, not a DataCurve-sanctioned result [^6][^5][^11][^22][^19].
:::

What the episode leaves behind is a cleaner question than the one it
started with. Whether "~63% at ~47K output tokens" turns out to be a
Zhipu flash-model benchmark or an anomaly, the 47K-token number is
already doing work that pass@1 never did: it ties benchmark outcome to
the operating economics of serving a model, and it invites the honest
comparison that matters to builders — competency per token, measured on
tasks an agent actually has to think about [^5][^14][^16]. The 80% was
never the finding. The finding is that a small, cheap model can sit in
the middle of the frontier's long tail, and that has to be demonstrated
on the whole catalog, with the sample size stated, every time [^6][^7][^12].

:::references
- {id: 1, title: "Ox Alpha – model listing (stealth/ox-alpha)", url: "https://openrouter.ai/stealth/ox-alpha", source: "OpenRouter", date: "2026-08-20"}
- {id: 2, title: "opencode launch post – free week / 100T tokens per day", url: "https://x.com/opencode/status/2090544355824038300", source: "X (opencode)", date: "2026-08-20"}
- {id: 3, title: "OpenRouter launch post – 'New stealth model: Ox Alpha'", url: "https://x.com/OpenRouter/status/2090544970923184269", source: "X (OpenRouter)", date: "2026-08-20"}
- {id: 4, title: "davis7 – 10-task DeepSWE subset run (8/10)", url: "https://x.com/davis7/status/2090655207831298095", source: "X (davis7)", date: "2026-08-21"}
- {id: 5, title: "winkey_h – '~63% at 47K avg output tokens … pareto optimal'", url: "https://x.com/winkey_h/status/2090814178810306874", source: "X (winkey_h)", date: "2026-08-21"}
- {id: 6, title: "davis7 – full DeepSWE run ends at ~63%", url: "https://x.com/davis7/status/2091285712566140986", source: "X (davis7)", date: "2026-08-22"}
- {id: 7, title: "Ananth7e – 'ox alpha is glm 5.3 flash … 58.4%'", url: "https://x.com/Ananth7e/status/2091165181976174701", source: "X (Ananth7e)", date: "2026-08-22"}
- {id: 8, title: "OpenRouter tests free Ox Alpha with a 1M-token context window", url: "https://www.ai-primer.com/engineer/stories/ox-alpha-openrouter-release", source: "AI Primer", date: "2026-08-20"}
- {id: 9, title: "Ox Alpha scores 80% on DeepSWE (10-task sample)", url: "https://aicrier.com/post/h6j1hut0pmc5pabqboxi", source: "AICrier", date: "2026-08-22"}
- {id: 10, title: "Ox Alpha Hits 80% on Full DeepSWE Benchmark (superseded headline)", url: "https://huggingnews.com/ai/update-ox-alpha-hits-80percent-on-full-deepswe-benchmark-first-run-of-al-18a12436", source: "HuggingNews", date: "2026-08-22"}
- {id: 11, title: "Ox Alpha Scores 58.4% on DeepSWE, Matching Claude Opus 4.8 Performance", url: "https://huggingnews.com/ai/ox-alpha-scores-584percent-on-deepswe-matching-claude-opus-48-performanc-4992e222", source: "HuggingNews", date: "2026-08-22"}
- {id: 12, title: "What Is Ox Alpha? (forensic evidence dossier)", url: "https://ox-alpha-evidence-production.up.railway.app/", source: "Independent forensics", date: "2026-08-21"}
- {id: 13, title: "Anonymous 'Ox Alpha' Model Beats GPT and Claude; Forensic Clues Point to China's Zhipu", url: "https://caimpare.ai/articles/anonymous-ox-alpha-model-beats-gpt-and-claude-on-coding-benchmark-forensic-clues-point-to-china-s-zhipu", source: "cAImpare", date: "2026-08-22"}
- {id: 14, title: "DeepSWE v1.1 live leaderboard (pass rates, tokens, cost, CIs)", url: "https://deepswe.datacurve.ai/artifacts/v1.1/leaderboard-live.json", source: "DeepSWE (DataCurve)", date: "2026-08-20"}
- {id: 15, title: "DeepSWE v1.1 task catalog (113 tasks)", url: "https://deepswe.datacurve.ai/artifacts/v1.1/tasks.json", source: "DeepSWE (DataCurve)", date: "2026-08-20"}
- {id: 16, title: "Introducing DeepSWE – benchmark design and task statistics", url: "https://deepswe.datacurve.ai/blog/deepswe", source: "DeepSWE blog (DataCurve)", date: "2026-05-26"}
- {id: 17, title: "Run DeepSWE – Pier + mini-swe-agent reproduction quickstart", url: "https://deepswe.datacurve.ai/run", source: "DeepSWE (DataCurve)"}
- {id: 18, title: "DeepSWE changelog", url: "https://deepswe.datacurve.ai/changelog", source: "DeepSWE (DataCurve)", date: "2026-08-14"}
- {id: 19, title: "ox-alpha DeepSWE benchmark – community full-suite run (opencode-go/ox-alpha-free)", url: "https://github.com/bmarti44/ox-alpha-deepswe", source: "GitHub (bmarti44)", date: "2026-08-22"}
- {id: 20, title: "deepswe – daily mirror of the DeepSWE live leaderboard", url: "https://github.com/benchget/deepswe", source: "GitHub (benchget)"}
- {id: 21, title: "New stealth model on OpenRouter: Ox Alpha (community thread)", url: "https://www.reddit.com/r/LocalLLaMA/comments/1vu8n8i/new_stealth_model_on_openrouter_ox_alph/", source: "Reddit r/LocalLLaMA", date: "2026-08-21"}
- {id: 22, title: "Live Ox Alpha × DeepSWE v1.1 benchmark status (gist)", url: "https://gist.github.com/nassimkhatiba-ai/d3da24d5b1a9287a7dcaf460c4e6d98d", source: "GitHub Gist", date: "2026-08-21"}
- {id: 23, title: "ℏεsam on davis7's 63% run (Tech Twitter mirror)", url: "https://www.techtwitter.com/tweet/67b60f16-4348-469f-9b04-25f6b91f6d32", source: "Tech Twitter", date: "2026-08-22"}
- {id: 24, title: "Stealth Model Ox Alpha Available For Free For A Week On OpenRouter And OpenCode", url: "https://officechai.com/ai/stealth-model-ox-alpha-available-for-free-for-a-week-on-openrouter-and-opencode/", source: "OfficeChai", date: "2026-08-21"}
- {id: 25, title: "Ox Alpha on OpenRouter: Free 1M Stealth Model (Aug 2026)", url: "https://www.explainx.ai/blog/openrouter-ox-alpha-stealth-model-august-2026", source: "explainx.ai", date: "2026-08-21"}
- {id: 26, title: "Ox Alpha Model Hits 1 Quadrillion Daily Token Capacity to Beat Fable Coding SOTA", url: "https://huggingnews.com/ai/ox-alpha-model-hits-1-quadrillion-daily-token-capacity-to-beat-fable-cod-9e132217", source: "HuggingNews", date: "2026-08-21"}
- {id: 27, title: "Ox Alpha: The Free Stealth AI Model Beating GPT-5.6 and Claude Fable 5", url: "https://pasqualepillitteri.it/en/news/12165/ox-alpha-stealth-ai-model-coding", source: "Pasquale Pillitteri", date: "2026-08-21"}
- {id: 28, title: "Ox Alpha: The Unchained AI Model Redefining Cybersecurity and Software Engineering Benchmarks", url: "https://undercodetesting.com/ox-alpha-the-unchained-ai-model-redefining-cybersecurity-and-software-engineering-benchmarks-video/", source: "Undercode Testing", date: "2026-08-21"}
:::
