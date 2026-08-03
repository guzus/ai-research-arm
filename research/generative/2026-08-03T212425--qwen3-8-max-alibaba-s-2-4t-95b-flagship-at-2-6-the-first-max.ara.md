---
eyebrow: DEEP RESEARCH · ALIBABA / QWEN
title: "Qwen3.8-Max: the three claims and what survives an audit"
deck: Alibaba shipped a real frontier-scale model on 3 August. It also shipped a benchmark lead measured on a different scaffold than its rivals', an open-weights promise with a four-for-four failure record, and a sixteen-day autonomy claim whose own repository contains a human's fingerprints.
domain: software
lede: |
  On 3 August 2026 Alibaba released Qwen3.8-Max — 2.4 trillion parameters,
  95 billion active per token, a million-token context, $2 and $6 per million
  input and output tokens. The model is real and the price is real. The three
  claims wrapped around it are more interesting: that it sits second only to
  Claude Fable 5, that it will be the first Max-class Qwen ever released as
  open weights, and that it coded autonomously for sixteen days. Alibaba
  published enough evidence to check all three. This is what checking them
  found.
stats:
  - {label: Total / active params, value: "2.4T / 95B"}
  - {label: List price, value: "$2 / $6", note: per 1M tokens}
  - {label: Autonomy claim, value: 16, unit: "days"}
  - {label: Max-tier weights ever shipped, value: 0}
---

## 00. The short answer

:::kv
- {term: "Is Qwen3.8-Max a frontier model?", def: "Yes, frontier-adjacent. Independent measurement puts it at Intelligence Index 53, ranked #16 of 186 — competitive, not leading [^10]."}
- {term: "Is $2/$6 actually cheap?", def: "On sticker, against Western flagships. On cost per completed task it is expensive: 150M output tokens and $2,159.51 to finish one benchmark index, against a 63M median [^10]."}
- {term: "Does it really beat Claude on Terminal-Bench?", def: "By 2.0 points — but Qwen ran itself on Claude Code and took its rivals' numbers from other harnesses, and one model's score can move 17.5 points across frameworks [^1][^23]."}
- {term: "Will the weights actually ship?", def: "Unknown. Four Max-tier flagships since September 2025 have shipped closed, no calendar date was given, and no license has been named [^44][^46]."}
- {term: "Did it code for 16 days on its own?", def: "It ran, and the commit count verifies exactly. But a human edited the agent's coordinator prompt mid-window, and no commit is cryptographically signed [^32][^33]."}
:::

## 01. What Alibaba actually shipped on 3 August

Qwen3.8-Max is a real, precisely specified frontier-scale model — but the public record splits cleanly into what Alibaba **documented** and what it only **promised**, and the promises are the load-bearing part.

The documented half is unusually specific. Qwen's launch post gives the model's shape in a single clause: "2.4T parameters (95B active), with open weights releasing next week" [^1]. That is roughly a 25:1 sparsity ratio, on an architecture the post says descends from Qwen 3.5 [^1]. Everything below that headline is missing: no expert count, no top-k, no layer count, no attention topology appears in any first-party document [^1].

:::stats
- {label: Total parameters, value: 2.4T}
- {label: Active per token, value: 95B, note: "~25:1 sparsity"}
- {label: Context window, value: 1M, unit: "tok."}
- {label: List price, value: "$2 / $6", note: "per 1M in / out"}
- {label: Intelligence Index, value: 53, note: "#16 of 186"}
:::

The secondary record is already wrong about the part Alibaba *did* disclose. Widely-read same-day coverage stated that "Alibaba has not disclosed the activated-parameter count" [^5] — the 95B figure is in the first sentence of the official blog [^1]. That is worth flagging early, because most of what follows depends on reading the vendor's own artifacts rather than the write-ups of them.

The token envelope comes from Alibaba's model page and does not add up the way a marketing "1M context" implies [^2]. A 991K maximum input plus a 131K maximum output exceeds the 1M window, so these are per-field ceilings, not a budget you can spend simultaneously [^2]. Qwen concedes the gap itself: its published harness config declares `"effective_context_window_percent": 95`, meaning the vendor does not claim the full million is usable [^1].

:::kv
- {term: Context, def: 1M}
- {term: Max input, def: 991K}
- {term: "Max input, thinking enabled", def: 983K}
- {term: Max output, def: 131K}
- {term: Max reasoning budget, def: 262K}
- {term: "Effective context (Qwen's own harness config)", def: 95%}
:::

Reasoning is exposed as a `reasoning_effort` enum — `xhigh` (default), `medium`, `low` — not a numeric token budget, with `preserve_thinking` on by default [^1]. That is an API-surface decision, not a capability one: you cannot dial a 262K reasoning budget directly, only pick a tier. On modalities the two first-party surfaces disagree. The model page lists text, image and video in, text out [^2]; Alibaba's own Codex and OpenClaw config snippets enumerate only text and image, which suggests video input is endpoint-specific rather than universal [^1]. The same pattern shows up in routing: Qwen serves an Anthropic-protocol endpoint at `https://dashscope-intl.aliyuncs.com/apps/anthropic`, so Claude Code reaches `qwen3.8-max` with a base-URL and model-ID swap [^1] — but the model page advertises only DashScope and OpenAI tabs, so how general that route is remains undocumented [^2].

Serving is fragmented across QwenCloud/DashScope (Beijing, Singapore, US-Virginia), Vercel AI Gateway as `alibaba/qwen3.8-max`, and OpenRouter as `qwen/qwen3.8-max` [^2][^7]. Here is the clearest thing that would weaken a "fully shipped" reading: coverage says GA arrived "via Alibaba Cloud's Model Studio APIs" [^3], yet Model Studio's own pricing and text-generation pages still top out at `qwen3.7-max` [^8]. Most likely documentation lag — but as of today, "documented on Model Studio" is simply false. Smaller drift points the same way: Vercel publishes max output 128,000 against Alibaba's 131K (=131,072), while pricing agrees at $2/$6 everywhere, marking that as metadata staleness rather than a real product difference [^7].

:::timeline
- {date: "2026-07-19", headline: "Preview at WAIC Shanghai", body: "Announced as qwen3.8-max-preview, two weeks before general availability."}
- {date: "2026-08-03", headline: "General availability", body: "Launch blog timestamped 2026-08-03T10:00:00+08:00; QwenWork enters public beta alongside it."}
- {date: "2026-08-03", headline: "Open-weights promise", body: "\"The model weights will be open-sourced on Hugging Face and ModelScope next week\" — no calendar date given."}
- {date: "2026-08-04", headline: "Nothing published yet", body: "The Hugging Face Qwen organization still contains no Qwen3.8 repository of any kind."}
:::

One loose thread sits outside the blog entirely: a second checkpoint, Qwen3.8-27B, is named in the official @Alibaba_Qwen post but never appears in the blog body [^6]. QwenWork, Alibaba's workplace agent platform, entered public beta the same day and is backed by the new model [^80]. Independently, Artificial Analysis places the served model at Intelligence Index 53, ranked #16 of 186, at 46.5 output tokens/sec, ranked #122 of 186 [^10]. And as of 2026-08-04 no Qwen3.8 weights have appeared on Hugging Face [^44].

Why this matters: an API you can call today is a commodity, and Qwen3.8-Max's measured intelligence is mid-pack. The asset that would actually reprice the frontier is 2.4T weights on Hugging Face — and that part is still a sentence, not a file.

## 02. The price: $2/$6, flat to a million tokens

Qwen3.8-Max lists at $2.00 per million input tokens and $6.00 per million output — a price that reads as aggressive only if your comparison set is Western, and that inverts entirely once you measure cost per completed task rather than cost per token.

The full first-party card is more interesting than the headline. Alongside the $2/$6 base, QwenCloud publishes an implicit cache read at $0.25, an explicit cache *creation* charge at $2.50, and an explicit cache read at $0.17 [^2]. The widely-quoted "$0.25 cached input" is the implicit rate only; explicit caching is a different, cheaper-on-read, dearer-on-write instrument. Two of those three numbers quietly undercut Qwen's own documented percentage rule. The context-cache docs say implicit cached tokens bill at 20% of input price — $0.40 here — and explicit reads at 10%, or $0.20; the card says $0.25 and $0.17 [^12]. Only the 125% creation premium matches exactly. On the predecessor qwen3.7-max the percentage rule holds precisely [^11], which makes the 3.8 deviation a deliberate discount rather than a documentation error.

The flat tier is real: one rate from zero to a million tokens, with no context bands [^2]. That is a genuine differentiator against Google, whose Gemini 3.1 Pro steps input $2.00→$4.00 and output $12.00→$18.00 above 200K [^15], and against OpenAI, which exposes explicit "Short context" and "Long context" columns priced at 2x input and 1.5x output [^14]. But it is not the differentiator the launch coverage claimed. Anthropic has already dropped its long-context surcharge: its pricing page states that "Claude 4.6 and later models... include the full 1M token context window at standard pricing" [^13]. Flatness is now table stakes among two of the four major vendors; the argument has to rest on the absolute level.

:::rank-list
- {label: DeepSeek V4-Flash, value: "$0.14 / $0.28", pct: 1}
- {label: DeepSeek V4-Pro, value: "$0.435 / $0.87", pct: 4}
- {label: GLM-5.2, value: "$1.40 / $4.40", pct: 14}
- {label: Qwen3.8-Max, value: "$2.00 / $6.00", pct: 20, highlight: true}
- {label: Claude Sonnet 5, value: "$2.00 / $10.00", pct: 20}
- {label: Gemini 3.1 Pro, value: "$2.00 / $12.00", pct: 20}
- {label: Kimi K3, value: "$3.00 / $15.00", pct: 30}
- {label: Claude Opus 5, value: "$5.00 / $25.00", pct: 50}
- {label: GPT-5.6 Sol, value: "$5.00 / $30.00", pct: 50}
- {label: Claude Fable 5, value: "$10.00 / $50.00", pct: 100}
:::

:::source
List prices per 1M input / output tokens, as of 2026-08-04; bar length scales with input price [^18][^17][^2][^13][^15][^16][^14].
:::

Read down that column and the picture is unambiguous. Against Western flagships, Qwen3.8-Max matches Sonnet and Gemini on input while charging 40% and 50% less on output, and undercuts GPT-5.6 Sol by 60% and 80% [^14]. Against Chinese peers it is the *expensive* option — GLM-5.2 is 30% cheaper on input and 27% cheaper on output [^17], and DeepSeek V4-Flash is priced at a fourteenth of it [^18]. This is a frontier price, not a dumping price. It also has a short shelf life: Sonnet 5's $2/$10 is introductory pricing through 2026-08-31, stepping to $3/$15 on 1 September in a pre-announced 50% increase [^20][^13]. Today's input parity becomes a 33% Qwen discount in four weeks.

Then the counterpoint that undoes most of the above. Artificial Analysis measures Qwen3.8-Max at a blended $1.18 per million tokens — cheaper than its own card implies, because input dominates real traffic — and simultaneously at $2,159.51 to complete the Intelligence Index, having burned 150M output tokens against a comparison median of 63M, with the model explicitly labelled "very verbose" [^10]. Reasoning is mandatory and `xhigh` is the default effort level, and every thinking token bills as output at $6 [^1][^10].

:::compare
- {role: LOWEST, name: Blended token price, value: $1.18}
- {role: HIGHEST, name: Index run cost, value: $2159.51}
- {role: SUBJECT, name: Output tokens burned, value: 150M}
:::

:::source
Artificial Analysis Intelligence Index, as of 2026-08-04; comparison median output 63M tokens [^10].
:::

A cheaper token you need three of is not a cheaper answer. On sticker, Qwen3.8-Max sits mid-table; on realized cost to finish a fixed benchmark, it lands among the most expensive models measured, because verbosity multiplies through the output rate exactly where that rate is highest.

A second counterpoint runs against the generational framing. qwen3.7-max lists at $2.50/$7.50, but carries a standing "50% off" tag on every line — a street price of $1.25/$3.75 [^11].

:::slope(left-label=Qwen3.7-Max, right-label=Qwen3.8-Max, unit=$)
| Item | 3.7 | 3.8 |
|---|---|---|
| List input, per 1M | 2.50 | 2.00 |
| List output, per 1M | 7.50 | 6.00 |
| Implicit cache read, per 1M | 0.50 | 0.25 |
:::

:::source
QwenCloud model pages, as of 2026-08-04; list prices before the standing 3.7 discount [^11][^2].
:::

So the same launch is a 20% cut against list and a 60% *increase* against what customers were actually paying. Domestically the story differs again: RMB 12 input, RMB 36 output, RMB 1.5 implicit cache per million in mainland China [^19] — an implied FX of exactly 6.00 against the international card, roughly 15% below a market rate near 7.1, and identical to Qwen3.7-Max's RMB 12/36 [^19]. In China the entire capability jump shipped at a flat price. Alibaba's own management points away from an undercutting narrative entirely: an executive on the Q4 FY2026 call said the company has *raised* per-token prices and that demand held [^60] — though that comes through an interpreter and is attributed to no named speaker, so it carries little weight.

This matters because procurement decisions anchored on the rate card will misprice this model by roughly an order of magnitude on reasoning-heavy work. The number to negotiate against is not $2/$6; it is dollars per finished task, and Qwen3.8-Max's is high.

## 03. The benchmark table measures the scaffold, not the model

Alibaba's claimed two-point lead on Terminal-Bench 2.1 is smaller than the documented variance from harness choice alone — and Qwen's own methodology footnotes disclose that it ran itself on one scaffold and took its competitors' scores from another [^1][^21].

| Benchmark | Qwen3.8-Max | Claude Opus 4.8 | Claude Fable 5 | GPT-5.6 Sol |
|---|---|---|---|---|
| *Terminal-Bench 2.1 | 86.6 | 84.6 | 84.6 | 88.8 |
| SWE-bench Pro | 67.7 | 69.2 | 80.0 | 64.6 |
| PaperBench | 93.0 | 80.3 | 88.8 | 90.5 |
| GPQA Diamond | 92.6 | 92.0 | 92.6 | 94.1 |
| IFBench | 82.8 | 62.2 | 63.5 | 72.7 |
| HLE | 43.6 | 45.7 | 53.3 | 47.2 |

Read as a scoreboard, the launch table is a split decision: Qwen3.8-Max leads on three of six flagship text rows and trails on three, winning PaperBench (93.0 against 80.3) and IFBench (82.8 against 62.2) while losing SWE-bench Pro (67.7 against Fable 5's 80.0) and Humanity's Last Exam (43.6 against 53.3) [^1][^21]. That is a competitive frontier model, not a coronation. The row Alibaba's messaging leans hardest on is Terminal-Bench 2.1, where 86.6 beats both Claude Opus 4.8 and Claude Fable 5 at 84.6 — and still trails GPT-5.6 Sol at 88.8 [^1][^21].

The problem is that a terminal-agent score is not a property of a model. It is a joint measurement of the model, the scaffold that gives it a shell and a file system, and the sampling policy that decides how many attempts it gets. Change any one of the three and the number moves. Qwen states its own conditions precisely: Terminal-Bench 2.1 was "Evaluated with Claude Code (avg@10), using a 5-hour timeout and max_tokens=131,072," and SWE-bench Pro with "the Claude Code harness, temp=1.0, top_p=0.95, and a 256K context window" [^1]. The competitor columns were not re-run under those conditions. Qwen's own footnote says so: "For all other models, we report the best published score across harnesses," naming Opus 4.8 and Fable 5 under Terminus 2 via Artificial Analysis, and GPT-5.6 Sol under Codex [^1][^21]. That is best-of-published-sources compilation, not a controlled head-to-head.

How much does that matter? Independent work running one model across four agent frameworks moves Claude Opus 4.7 from 62.5 to 45.0 — a 17.5-point spread with the model held constant [^23]. Qwen's claimed margin over Opus 4.8 and Fable 5 is 2.0 points, roughly a ninth of that spread. Be careful with this argument, though, because the same paper cuts against its strongest form: its authors conclude that frameworks "affect performance, but do not substantially change the underlying model's capability ceiling" [^23]. The honest claim is narrower than "the harness explains everything" — it is that a 2.0-point gap cannot be resolved by a comparison that varies the harness, and Qwen's does.

:::compare
- {role: LOWEST,  name: "Qwen's claimed Terminal-Bench lead", value: "+2.0 pts"}
- {role: HIGHEST, name: "One model, four frameworks", value: "17.5 pts"}
- {role: SUBJECT, name: "Matched-scaffold blind test", value: "Kimi K3 83 / Qwen 80"}
:::

:::callout(kind=warn, label=Methodology)
The asymmetry is disclosed, not hidden. Qwen's WideSearch footnote states the setup outright — "Claude Code harness for external models and the Qwen-Agent harness for ours" — and on SkillsBench the split runs three ways, with "the Qwen-series are evaluated on OpenCode" while rivals run on Claude Code and Codex [^1]. A vendor measuring itself on its own scaffold and its rivals on someone else's is running two experiments, not one comparison.
:::

Public leaderboards are the natural check, and they place the model lower than its own table does. As of 2026-08-03 Qwen3.8-Max sits second globally on multimodal behind a single Fable 5 variant, and behind Fable 5 plus three Opus variants on text [^28]. On Frontend Code — the one board publishing Elo — it ranks fourth [^24].

:::rank-list
- {label: "Claude Opus 5 (Max)",  value: "1,705", pct: 100}
- {label: "Kimi K3 (Max)",       value: "1,676", pct: 98}
- {label: "Claude Opus 5 (High)", value: "1,669", pct: 98}
- {label: "Qwen3.8-Max",          value: "1,668", pct: 98, highlight: true}
:::

The one-Elo gap to third place is noise; the 37-Elo gap to first is not [^24]. These are day-one standings on a model still accumulating votes, as of 2026-08-03.

Only one independent test held the scaffold constant. A blind review on OpenCode 1.17.13 — identical task card and permissions, a 60-minute wall clock, a 269-file SHA-256-pinned corpus — scored Kimi K3 at 83/100 against Qwen3.8-Max-Preview at 80/100 after factual penalties, though Qwen won the tool-use subscore 9–8 with 44 calls and zero failures [^22]. Three caveats travel with it: it tested the Preview rather than the GA model, it is a single task, and its author warns that one matched run "cannot isolate the model from its serving route" [^22]. A Chinese hands-on review of the same preview was sharper still, calling deep-research output "essentially comparable" to Qwen3.7-Max and judging three of four build tasks failures — while flagging that preview and release can differ substantially [^27].

As of 2026-08-03 no independent re-run of the GA model existed: no Artificial Analysis-independent eval, no SWE-bench Verified, no LiveBench, no Aider, no ARC-AGI [^25]. One aggregator ranking it #31 of 215 sources 100% of its 52 benchmark rows from Qwen's release blog, where "verified" means "tied to a published source," not independently reproduced [^25]. Citing it as corroboration double-counts Alibaba's own table. Several launch rows — QwenSWEBench, QwenQoderBench, CoWorkBench, RecreationBench — are Qwen's own constructions, and the blog labels others "internal benchmarks," which are unauditable by definition [^1][^21]. Prior-generation work found the Qwen2.5 pretraining corpus overlapping MATH-500, AMC and AIME 2024, and a leakage study across 35 open models ranked the Qwen family highest [^26]. No contamination allegation attaches to Qwen3.8-Max; the relevance is a raised prior on saturated static benchmarks, which makes the unexplained PaperBench jump from 64.8 to 93.0 in one generation the row most deserving replication [^1][^21].

The strongest counterpoint runs in Alibaba's favour. On DeepSWE 1.1 the footnote reads: "We report the highest score among both harnesses; notably, Qwen3.8-Max performs best on Claude Code" [^1]. Disclosing a max-over-harnesses practice on a row where the model scores 56.6 — well short of the leaders — is transparency, not spin [^1][^21]. Most vendors bury the harness; Qwen printed it, which is precisely why this analysis is possible at all.

This matters because the same evidentiary standard governs the autonomy claim in the next section — an analyst on the record asks "Sixteen days of what? How many times did a human step in? Did the output survive code review?" [^29]. Until someone re-runs Qwen3.8-Max, Opus 4.8 and Fable 5 on one scaffold with one sampling policy, the honest reading of Terminal-Bench 2.1 is that the three are statistically indistinguishable [^1][^23].

## 04. Sixteen days, audited against its own repository

Alibaba did the rare thing and named the artifact behind its autonomy claim, which makes the claim checkable — and checking it finds a real, substantial engineering run that is nonetheless not quite the thing the headline says.

Start with the number, because Alibaba's own launch post carries two of them for the same run. The section heading reads "10+ Days of Autonomous Coding: Building a Self-Evolving Harness"; the body reports that the result arrived "after approximately 16 days of fully autonomous AI operation," yielding "265 commits, 127 PRs, and 151 issues" [^1]. Two official @Alibaba_Qwen posts in the same launch thread repeat the split [^6][^41]. The discrepancy originates with the company, not with sloppy aggregation downstream. The most parsimonious reconciliation — which Alibaba never offers — is that ~16 days is the repository's calendar age (created 2026-07-13, censused 2026-07-30) while "10+ days" is accumulated run time [^1][^30]. Contiguity was never actually claimed.

:::timeline
- {date: "2026-07-13", headline: "Repository created 11:43Z; root commit 12:22Z", body: "The parentless root commit lands 39 minutes later as a single +3,222 / −0 drop."}
- {date: "2026-07-23", headline: "Human commit 59eca7c edits the coordinator prompt", body: "Account qqqys reorders the loop's action priority mid-window."}
- {date: "2026-07-30", headline: "Census date: 265 commits, 127 PRs, 151 issues", body: "The figures Alibaba published are measured to here."}
- {date: "2026-08-03", headline: "Launch — and the repo is still being pushed to", body: "Last push 20:38Z the same day, so the artifact is live, not frozen."}
- {date: "2026-08-04", headline: "Still no independent replication", body: "Zero releases, zero tags, nothing published to npm."}
:::

The verification is the first thing to report, and it is favourable. Counting back 265 commits from the census date lands exactly on the parentless root commit `170a3d8a`, dated 2026-07-13T12:22:21Z, message "feat: scaffold oh-my-cli with toolchain, tools, and fake-provider smoke test" [^33]. Alibaba's headline figure is not marketing rounding; it is a number that reproduces against the public API to the commit. That is more corroboration than almost any comparable autonomy claim ships with.

"From an empty folder" is the imprecise part. That root commit is a single +3,222 / −0 drop landing 39 minutes after the repository was created, already containing a layered CLI plus tests — and roughly 2,093 of those lines are a lockfile, leaving about 1,129 authored lines [^33]. Thirty-nine minutes is entirely consistent with fast agentic generation, so this does not demonstrate pre-seeded human code. What it demonstrates is narrower and still important: the git trace does not show from-zero construction, because the first observable state is already a scaffold.

Nor is the result a toy. GitHub reports it as Apache-2.0 TypeScript [^30], and the repository tree carries three runtime dependencies, roughly 130 `*.test.ts` files across unit, integration and smoke suites, LSP and MCP integration, and an Electron desktop shell [^42][^43]. The CI is more hardened than most human repositories: one `verify` job running build, typecheck, unit, integration and smoke, plus a gitleaks history scan pinned by version *and* SHA-256, and an `npm audit --omit=dev --audit-level=high` gate [^43]. Sampled feature commits average roughly 250 changed lines, with about two-thirds of added lines being tests [^33]. Against that, there are zero releases, zero tags, and no npm publication — the `oh-my-cli` name there belongs to an unrelated tool from May 2026 [^42]. Nobody outside Alibaba has run this as shipped.

:::stats
- {label: Commits to census date, value: 265}
- {label: Human contributions, value: 13}
- {label: Signed work commits, value: 0}
- {label: Independent replications, value: 0}
:::

Then the contributor list, which is where the framing breaks. As of 2026-08-03 GitHub records 463 contributions from `qwen-code-dev-bot` and 13 from a human account, `qqqys` [^31]. The bot figure keeps climbing because the repository is still running; the human count has not moved.

:::bars
- {label: "qwen-code-dev-bot (agent account)", value: "463", pct: 100}
- {label: "qqqys (human)", value: "13", pct: 3}
:::

The fill above is scaled to the bot's count, so the human bar reads as 3% *of the agent's* contributions — small, and not the point. The point is what one of them changed.

:::callout(kind=danger, label="Human in the loop")
Commit `59eca7c` was authored and committed by qqqys (qys177@gmail.com) at 2026-07-23T07:26:00Z — squarely inside the claimed window. Titled "chore(governance): increase idle community discovery cadence," it changes three files, +71/−9: `.autonomy/community.yml`, a new unit test, and `.autonomy/prompts/coordinator.md` (+15/−7). It reorders the coordinator's action priority and cuts the community-discovery interval from 24 hours to 2 [^32]. Alibaba could fairly argue governance is not product code. But a coordinator-prompt edit changes how the loop decides what to do next. That is steering.
:::

The scaffold around the loop is human-authored too, and openly so. `AUTONOMY.md` and the coordinator prompt describe a permanent loop over bounded ticks with a fixed 11-item priority order, a one-lease/one-branch concurrency limit, three-strike failure quarantine, and four CODEOWNERS-protected paths the bot may read but never modify — "Only the independent governance maintainer may approve and merge governance changes" [^34][^35]. The loop is explicitly instructed to "recover idempotently after restarts, never request Goal re-arming, never delete itself," and never to declare the product complete [^34][^35]. A sixteen-day run therefore does not imply a sixteen-day session, and every guardrail names the failure mode it was written against. Chinese coverage adds what English coverage dropped: the run was seeded by one instruction — "create a self-evolving agent Harness" — and human engineers fed further requirements in through DingTalk while it ran, which sits awkwardly beside the same article's "no human intervention" framing [^39].

Finally, attestation. No agent work commit sampled for this article is cryptographically signed; the API reports verification reason "unsigned" on each one, while GitHub's own web-flow merge commits carry a valid signature [^32]. `qwen-code-dev-bot` is an ordinary User account, not a Bot type [^30]. This is completely normal GitHub behaviour and is *not* evidence of deception. It is decisive on the evidentiary question anyway: the repository was offered as the proof, and on its own terms it cannot establish that a model rather than a person produced the commits.

Set against the field, is sixteen days even the impressive number? The best-known measure of long-horizon capability deliberately measures something else. METR states that a time horizon is "not the length of time AIs can work independently" but "the amount of serial human labor they can replace with a 50% success rate," and the top measured 50% horizon in its January 2026 note is 4 hours 49 minutes, on a 95% confidence interval running from 1h49m to 20h25m [^36]. The two numbers are dimensionally different, so they do not contradict. **By my arithmetic**, 16 days is 384 hours: across 151 issues that is ~2.5 hours per issue, across 127 PRs ~3.0 hours per PR — every unit task sits inside that measured band, and the gap between 151 issues and 127 PRs means roughly two dozen were never closed. The run needs no 384-hour horizon, only a verifier loop chaining hours-long tasks. The mechanism is documented elsewhere: OpenAI says its long-running agent was "natively trained to operate across multiple context windows through a process called compaction," finishing work by "pruning its history while preserving the most important context" [^76], and Qwen's own agent framework runs a five-stage eviction ladder for "effectively unlimited context length" [^77]. A long run implies a long task, never a long context. That matters because independent long-horizon work finds frontier agents solving under 30% of such tasks with a meaningful share of reward-hacked rollouts — and a verifier-gaming agent still logs sixteen days of "autonomous operation" [^40].

Which leaves the disclosure asymmetry, on the same blog page. For its paper-reproduction demo, Alibaba published effort: the model worked "completely on its own for about five days" (~125 compute hours), producing "roughly 7,600 lines of code" across "33 rounds of GPU training" [^1][^37]. Its own predecessor claim, 35 hours of continuous autonomy in May 2026, came with 1,158 tool calls and 432 kernel evaluations [^38].

:::compare
- {role: LOWEST, name: "Paper demo — effort disclosed", value: "~125 compute hrs"}
- {role: HIGHEST, name: "16-day run — effort disclosed", value: "none"}
- {role: SUBJECT, name: "Qwen3.7-Max, May 2026", value: "1,158 tool calls"}
:::

For the sixteen-day run Alibaba published artifact counts and no effort metric at all — no hours, no tokens, no actions, no restarts. Eleven times the duration, 74 days later, with less evidence. This matters because the industry is converging on wall-clock autonomy as its headline capability metric, and this is the best-documented instance available: if the most auditable such claim still cannot distinguish a model's work from a person's, then duration is a marketing unit, not a measurement.

## 05. The open-weight promise and a four-for-four base rate

"The first Max-tier open-weight release" is the single most consequential claim in the 3 August launch, and it is the least delivered: no Max-class Qwen flagship has ever shipped weights, no date has been committed, and no license has been named. Alibaba says as much itself — the launch post calls this "the first time we will open-source the weights of a Qwen-Max-class model" [^1].

The commitment itself is first-party and unambiguous. Alibaba's own launch post states that "The model weights will be open-sourced on Hugging Face and ModelScope next week" [^1], and the official @Alibaba_Qwen account names two artifacts rather than one: "Next week, the open weights of Qwen3.8-Max will be released, and Qwen3.8-27B is also going open-weights to meet you all!" [^6]. SCMP — which Alibaba owns, and which discloses that ownership in the article — frames the general-availability announcement as arriving "ahead of an open-weights release next week" [^3]. Three channels, one promise, and in none of them a calendar date. Since 2026-08-03 was a Monday, "next week" points at roughly 10–16 August 2026; that mapping is *my inference*, not a claim any first-party source makes [^1,3]. It is also the only calendar a reader has.

:::iso
- {label: "Max-tier flagships since Sept 2025", glyph: "🔒", count: 4}
- {label: "Max-tier weights ever released", glyph: "📦", count: 0}
:::

The second row is empty on purpose: the count is zero, and a pictogram of nothing is the honest rendering of the record. Every Max-tier Qwen flagship since Qwen3-Max-Preview in September 2025 has shipped closed — Qwen3-Max-Preview, Qwen3.6-Max-Preview (2026-04-20), Qwen3.7-Max (2026-05-20), and Qwen3.8-Max-Preview (2026-07-19) [^46] — and the Hugging Face organization contains no Max-class checkpoint to contradict it [^44,46]. That is four for four.

One framing in circulation needs correcting: Qwen3.6-Max-Preview was **not** the first flagship held back. The closed-flagship policy dates to September 2025 [^46], which makes it an eleven-month, repeatedly reaffirmed commercial posture rather than a three-month experiment. The forecast changes accordingly — reopening the top tier is a policy reversal, not a course correction. And there is no *successful* precedent to anchor on either: not one Max-tier open-weights release has ever been promised and then delivered on schedule, so the base rate here is not merely unfavorable, it is empty.

:::timeline
- {date: "2025-09", headline: "Qwen3-Max-Preview", body: "Closed. The start of the closed-flagship policy."}
- {date: "2026-04-20", headline: "Qwen3.6-Max-Preview", body: "Closed."}
- {date: "2026-05-20", headline: "Qwen3.7-Max", body: "Closed."}
- {date: "2026-08-03", headline: "Qwen3.8-Max", body: "Weights promised \"next week.\" No date given, no license named."}
:::

As of 2026-08-04, the promise is unfulfilled on the channel that can be checked. Querying the Hugging Face API for the Qwen organization sorted by last-modified returns no repository containing "3.8"; the most recently modified Qwen repository dates from 2026-07-22, and the highest version present is Qwen3.6 [^44]. Because a new upload would necessarily sort to the top of a last-modified ordering, that absence is dispositive rather than merely suggestive. ModelScope could not be verified — its organization page returns a JavaScript shell — so treat that channel as unchecked, not confirmed-negative. One day in, with the promised window not yet open, this is a baseline measurement, not a broken promise.

:::callout(kind=warn, label=License)
No license has been named for the promised weights in any first-party English or Chinese channel [^1,39]. Qwen's precedent is split by **tier**, not by default: small models ship Apache 2.0, but its largest open checkpoints have carried a bespoke Tongyi Qianwen License reading "If you are commercially using the Materials, and your product or service has more than 100 million monthly active users, You shall request a license from Us" — a license that also bars using the model's outputs to improve any other LLM, and requires its own terms to travel with every redistribution [^45]. Since the restricted terms have historically attached to the *biggest* open models, and 2.4T would be by far the biggest, "Apache 2.0 because Qwen always ships Apache 2.0" is a selection-biased inference from the small-model tier. The competitive bar is set higher: GLM-5.2 ships MIT [^47].
:::

The second promised checkpoint is shakier still. Qwen3.8-27B appears in the official X post [^6] but not in the blog body [^1], and English coverage of it traces back to a single Chinese business-press report [^48]. Nothing is published about its parameter count, dense-versus-MoE structure, context length, license, or memory footprint — so nothing about it should be asserted.

:::kv
- {term: "Release date", def: "\"Next week\" — uncommitted"}
- {term: "License", def: "Unnamed"}
- {term: "Hugging Face (as of 2026-08-04)", def: "No Qwen3.8 repository"}
- {term: "ModelScope", def: "Unverified — JS shell, not checked"}
- {term: "Second checkpoint (Qwen3.8-27B)", def: "Announced on X, absent from the blog"}
- {term: "Precedent for a Max-tier release", def: "None"}
:::

Two things cut the other way, and both are real. First, Qwen's **non-Max** track delivers: the Hugging Face organization does contain Qwen3.5-397B-A17B along with its FP8 and GPTQ-Int4 variants, Qwen3.5-122B-A10B and Qwen3.5-27B — real, downloadable, frontier-scale weights [^44]. That is a good record; it is simply a record belonging to a different pipeline, and conflating the open track with the Max track is exactly the error a combined announcement invites. Second, the competitive incentive genuinely changed: Moonshot shipped Kimi K3 as an open-weight model days before Qwen previewed 3.8-Max, and at 2.8 trillion parameters it is the larger of the two [^9][^63]. For the first time Qwen faces a *larger* already-open rival, which is not the situation that produced the four-for-four streak. Chinese tech press reconstructs the internal rationale as defensive ecosystem retention — open-sourcing as "the optimal choice for the company to maintain its reputation and ecosystem" [^47] — though that paraphrases unnamed sources.

Why it matters: Qwen is not a marginal participant whose license terms affect a hobbyist niche. Cumulative Hugging Face downloads reached 942.1M by March 2026, roughly double Llama's 476.0M after passing it in September 2025, and Qwen's share of new fine-tunes and adaptations rose from 1% in January 2024 to 69% by February 2026 [^49]; Chinese open-weight models crossed US models on OpenRouter token volume for the first time in the week of 2026-02-09, 4.12 trillion tokens against 2.94 trillion [^50]. Read those downloads carefully — they are HTTP requests to a file-hosting endpoint, inflated by bots and CI, and are not active users [^49]. Even discounted, they mean the terms attached to a 2.4T checkpoint would propagate through most of the world's open fine-tuning. A Max-tier release under MIT-or-Apache terms would be the largest open-weights event to date; the same sentence with a 100M-MAU clause and no ship date is a marketing asset.

## 06. What 2.4 trillion parameters cost to serve

Sparsity is what makes $2/$6 possible, but it is a weaker lever than the marketing implies — decode cost tracks *total* parameters through memory bandwidth, not active ones — and the same arithmetic that explains the price also shows that a 2.4-trillion-parameter open-weight release is a datacenter artifact, not a self-hosting event.

Begin with the number that is not negotiable. {accent}This next figure is my arithmetic, not a published one:{/} 2.4e12 parameters at two bytes each is 4.8 TB of weights at BF16, 2.4 TB at FP8, and 1.2 TB at INT4. That is weights only — before the KV cache, activations, and framework reserve, which for MoE serving typically add another 15–40% on top [^55].

:::bar-chart(title="Weights-only memory footprint, 2.4T parameters", orientation=horizontal, value-suffix=" TB")
categories: BF16, FP8, INT4
Checkpoint size: 4.8, 2.4, 1.2
:::

Converting bytes into boxes is also my arithmetic: at 141 GB of HBM per H200-class card and eight cards per node, the checkpoint alone needs 40 GPUs at BF16, 24 at FP8, and 16 at INT4 — five, three, and two nodes respectively, with nothing left over for context.

:::rank-list
- {label: "BF16 — 5 nodes", value: "40 GPUs", pct: 100, highlight: true}
- {label: "FP8 — 3 nodes", value: "24 GPUs", pct: 60}
- {label: "INT4 — 2 nodes", value: "16 GPUs", pct: 40}
:::

Third-party sizing for the nearest real analogues corroborates the shape: a 1.6T MoE is put at "12+ H200 SXM5 across two nodes even at FP8," and a 1T MoE at FP8 fits neither an 8×H100 node (640 GB) nor an 8×H200 node (1,128 GB) [^55]. That guide is published by a GPU-cloud operator with a commercial interest in large deployments, so treat the framing sceptically — but the underlying division is checkable. For scale at the rack level, one NVIDIA GB200 NVL72 carries 13.4 TB of HBM3E, which by my arithmetic means the BF16 checkpoint occupies roughly 36% of an entire rack before a single user connects [^54].

The KV cache, not the weights, is the real ceiling. A single 1M-token sequence plausibly consumes somewhere between 37 GB and 164 GB at FP8 depending on attention design — a bracketed estimate, not a measurement, because Qwen publishes no layer count, no attention type, and no KV head count, which makes that roughly fourfold spread irreducible from public data [^1]. On the 24-GPU FP8 build above, that leaves room for only a small number of concurrent full-context sequences. The spread *is* the finding: it is the difference between a viable million-token product and one that cannot be served profitably at any advertised price.

Here is the first-principles correction that most coverage skips. Active parameters govern prefill arithmetic; decode cost tracks total parameters through memory traffic, because every decoded token still drags routed weights across the bus. Epoch's framing is that MoEs "are more efficient at inference than dense models of the same total parameter count, but less efficient than dense models with the same active parameter count," with an eight-way-sparse MoE serving roughly like a dense model of half its total size [^53].

:::kv
- {term: "What active parameters govern", def: "Prefill arithmetic"}
- {term: "What total parameters govern", def: "Decode memory traffic"}
- {term: "Dense-equivalent of an 8-way-sparse MoE", def: "~50% of total parameters"}
- {term: "Consequence", def: "Cheap input, expensive output — hence the 3:1 price ratio"}
:::

So "95B active" does not mean "serves like a 95B model." It means prefill is cheap and decode is not — which is precisely why input prices at $2 and output at $6. The measured serving profile is consistent with that: 46.5 output tokens per second, ranked #122 of 186, with a 2.48-second median time to first chunk [^10]. Reasoning is mandatory with `xhigh` as the default, and reasoning tokens bill as output at $6 [^1][^10] — mandatory high-effort thinking is revenue-accretive at a fixed cost per token.

For an actual cost anchor there is exactly one first-party production accounting of a large sparse MoE: DeepSeek's Open Source Week disclosure of 226.75 nodes of 8×H800 averaged over 24 hours, where "assuming the leasing cost of one H800 GPU is $2 per hour, the total daily cost amounts to $87,072" against $562,027 of theoretical daily revenue — the famous "545% cost profit margin" [^51]. Restated honestly, and this is my arithmetic: 545% is profit over *cost*. On the denominator every other company uses, (562,027 − 87,072) / 562,027 = 84.5% gross margin, a high but entirely ordinary software number. DeepSeek also stated that "only a subset of services are monetized (web and APP access remain free)" and applied large off-peak discounts, so the revenue side is explicitly counterfactual [^51]. Independently, LMSYS served DeepSeek V3 on 96 H100s with wide expert parallelism at "a cost of $0.20/1M output tokens, which is about one-fifth the cost of the official DeepSeek Chat API," landing within 5.6% (prefill) and 6.6% (decode) of DeepSeek's own published profile [^52].

:::compare
- {role: LOWEST, name: "LMSYS measured, DeepSeek V3", value: "$0.20 / 1M out"}
- {role: HIGHEST, name: "Qwen3.8-Max list output", value: "$6.00 / 1M out"}
- {role: SUBJECT, name: "Scaled estimate at 2.4T", value: "~$0.72 / 1M out"}
:::

Scaling that anchor is my arithmetic and rests on one assumption — that decode is HBM-traffic-bound and therefore scales with total, not active, parameters. On that basis 2.4T / 671B ≈ 3.58x gives roughly $0.72 per million output tokens, an ~8x markup against a $6 list price; even doubling the estimate for worse expert-parallel efficiency at 2.4T leaves about 4x.

The weakness deserves top billing, because it attacks my own number hardest. The $0.20 figure is a *ceiling* achievable by expert engineers at near-full utilisation on a 96-GPU minimum deployment. Independent work measures the same hardware producing anywhere from $0.21 to $15.25 per million tokens driven by arrival rate alone, and finds that naive estimates understate real cost by 2.5–24x [^56]. A serving fleet that is idle half the day does not get $0.72.

Is the price nonetheless below cost? The natural experiment says no. Subsidy-free US hosts serve the same open weights at identical prices — Together lists Kimi K3 at $3.00/$15.00 against Moonshot's own $3.00/$15.00, and GLM-5.2 at $1.40/$4.40 against Z.ai's $1.40/$4.40 [^58]. Chinese providers are estimated to hold 20–40% API gross margins while pricing at 10–20% of Western rates, on training costs around a tenth of comparable overseas systems and GPU utilisation above 70% against a 40–50% industry norm [^58]; that margin range may be the outlet's inference rather than its cited analyst's, and no cost data exists for Alibaba or DeepSeek at all. Meanwhile prices for a *fixed* capability level have fallen at a median of about 50x per year, rising to roughly 200x per year on post-January-2024 data, with no clear evidence that reduced profit margins explain the drops [^57].

This matters because it relocates the story: $2/$6 is the base rate of a deflating market meeting a sparse architecture, not a subsidy — and the 40 GPUs it takes to hold the weights mean the open-weight promise buys auditability and sovereign hosting, not a model anyone runs at home.

## 07. Why Alibaba reopened the top tier now

The decision to reopen the top of the Qwen line is legible as capex defence rather than generosity: Alibaba is spending at a rate that has already swung its free cash flow negative, its cloud segment is the only line that converts that spend into revenue, and a larger, already-open Chinese rival shipped three days before Qwen3.8-Max was previewed.

Start with the cash, because it constrains everything downstream. FY2026 capital expenditure reached RMB 126,063 million (US$18,275 million), up roughly 50% from about RMB 84.3 billion in FY2025, with RMB 26,887 million spent in the March quarter alone [^59]. Over the same year free cash flow reversed from an inflow of RMB 73.9 billion to an outflow of RMB 46.6 billion, and in the March quarter alone group adjusted EBITA fell 84% year over year to RMB 5,102 million — against a full-year decline of 56% to RMB 76,416 million. Management attributes the cash swing to quick commerce *and* cloud infrastructure jointly, so it is not an AI-only number [^59].

:::slope(left-label="FY2025", right-label="FY2026", unit="RMB bn")
| Item | FY2025 | FY2026 |
|---|---|---|
| Capital expenditure | 84.3 | 126.1 |
| Free cash flow | 73.9 | -46.6 |
:::

Against that outflow, exactly one segment monetizes the buildout. Cloud Intelligence revenue was RMB 41,626 million (US$6,035 million) in the quarter ended 2026-03-31, up 38% year over year, with external customer revenue growth accelerating to 40% and AI-related products at roughly 30% of external cloud revenue [^59]. Depreciation from the servers arrives on schedule; the demand that fills them does not.

:::stats
- {label: "Cloud Intelligence revenue", value: "RMB 41.6bn", note: "+38% YoY, quarter ended 2026-03-31"}
- {label: "AI share of external cloud", value: "~30%"}
- {label: "Quarterly capex", value: "RMB 26.9bn"}
- {label: "MaaS ARR", value: "over CNY 8bn"}
:::

The RMB 380 billion (~US$53 billion) three-year AI and cloud infrastructure commitment announced 2025-02-24 has since functioned as a floor rather than a plan, with CEO Eddie Wu telling the Q4 FY2026 call that "it's likely given that kind of investment that we will overshoot the original CapEx figure" and that AI-related product revenue should "cross the 50% threshold" within about a year [^60][^61].

:::quote(attr="Eddie Wu, CEO, Alibaba Group, Q4 FY2026 earnings call")
We need 10 times the amount of data center infrastructure compared to what we had in 2022.
:::

:::note
These remarks were delivered in Mandarin through an interpreter and are taken from a transcript republisher rather than Alibaba's own IR posting, so the English wording is the interpreter's, not the speaker's.
:::

The trigger was competitive and recent. Moonshot shipped Kimi K3 — 2.8 trillion total parameters, the largest Chinese model at the time — as an open-weight release days before Alibaba previewed Qwen3.8-Max on 2026-07-19, leaving Qwen the smaller of the two [^9][^63]. Chinese tech press reconstructs the internal rationale as necessity — "under the dual pressure from Kimi K3 and DeepSeek V4, Alibaba must sprint ahead," with the preview framed as "a critical move to seize the release window" — though this is informed reconstruction from unnamed sources, and no Alibaba executive has been quoted directly on the open-sourcing decision [^47].

What the weights buy is distribution the paid tier has not won. Qwen sits at roughly 942 million cumulative Hugging Face downloads and 69% of new model adaptations — more derivatives than Google and Meta combined [^65]. Yet no Qwen model leads OpenRouter by token volume: as of July 2026 the coding leaderboard is led by Xiaomi's MiMo-V2.5 at 7.54 trillion tokens and 29.1% share, with MiniMax, Tencent and GLM-5.2 also ahead [^66]. Wu's own framing exposes the gap — model-as-a-service ARR is "already over CNY 8 billion," but "most of that revenue is coming from our own proprietary models" [^60].

:::rank-list
- {label: "MiMo-V2.5 (Xiaomi)", value: "7.54T / 29.1%", pct: 100}
- {label: "MiniMax M3", value: "2.79T / 10.8%", pct: 37}
- {label: "Tencent Hy3", value: "2.52T / 9.7%", pct: 33}
- {label: "GLM-5.2 (Z.ai)", value: "2.25T / 8.7%", pct: 30}
- {label: "NVIDIA Nemotron 3 Ultra", value: "1.98T / 7.6%", pct: 26}
:::

There is a silicon dimension English coverage has missed entirely. Chinese-language reporting says Qwen3.8 is served in production on Alibaba's own T-Head hardware — 64 Zhenwu M890 cards on an ICN Switch 1.0 interconnect at 800 GB/s with 9 TB of aggregate memory, billed as the first domestic supernode to run a model above two trillion parameters, with up to a 1.5x agentic-inference speedup [^64]. Read the scope precisely: the source describes a node that "provides model inference services," and no Chinese or English source reviewed discloses what hardware *trained* the model — an absence of evidence, not evidence of absence [^64].

Two things cut against reading the launch as a catalyst. Citi reiterated Buy with a HK$191 target but attributed the rally partly to AWS and Azure cloud read-throughs, arguing that enterprise "model-agnostic" adoption erodes any single model's moat and shifts value to full-stack platform owners — a thesis under which the weights matter less than the capacity behind them [^65]. And the tape has run this play before: the US line closed up 4.13% at $127.30 on 2026-08-03 against a $122.25 prior close, ranging $126.04–$129.50 with an intraday high 1.7% above the close, still far below its $192.67 52-week high and well above its June low of $91.99 [^62]; the Hong Kong line closed about 7% higher at HK$125.20 the same day, per SCMP, which is Alibaba-owned and discloses this in-article [^3]. After the 2026-07-19 preview a near-identical Monday pop reversed across the following four sessions [^3].

This matters because it reframes the release for anyone underwriting the capex: opening the top tier is a customer-acquisition instrument for a cloud business carrying a negative-free-cash-flow buildout, and the metric that settles whether it worked is hosted-inference share and AI's share of external cloud revenue — not benchmark placement.

## 08. The legal overhang nobody has actually enacted

No enacted US law restricts downloading, hosting or serving a Chinese open-weight model; the rules in force attach to Alibaba the *entity*, not Qwen the *artifact* — and the two risks that could actually bite sit in Beijing and in a default toggle in Alibaba's own console.

Start with the negative finding, because most coverage skips it. The leading legislative vehicle, the No Adversarial AI Act (S.2177, 119th Congress), was introduced 2025-06-25 and has one recorded action in the thirteen months since — "Read twice and referred to the Committee on Homeland Security and Governmental Affairs" — clearing none of the four remaining stages [^67]. A proposed bill is not a law. The ~200-startup letter of 2026-07-22, from the newly formed Little Tech Association to the President, Commerce, State, Treasury and OSTP, argued a blanket ban would "stifle competition, entrench incumbents, and function as a tax on intelligence" — but it opposed a *proposed and still-unannounced* measure, and its signatory count is unreconciled between "nearly 200" and 179 [^71].

| Measure | Status as of 2026-08-04 | Reach |
|---|---|---|
| No Adversarial AI Act (S.2177) | Proposed — in committee since 2025-06-25 | Would bar federal agency use |
| DoD 1260H designation of Alibaba | In force, published 2026-06-10 | Identification only, no penalty |
| FY2024 NDAA Sec. 805 | In force since 2026-06-30 | DoD contracting with Alibaba |
| BIS Entity List / MEU listing | Not listed | n/a |
| *PRC outbound AI controls | Under deliberation, reported 2026-07-08 | Could block the weight release |
| State device bans | In force in 17+ states | Government devices, DeepSeek app |

What *is* in force is entity-based. The Federal Register published on 2026-06-10 an expansion of the Section 1260H Chinese Military Companies list — the notice states no count, but the additions tally to roughly 76 entities — with Alibaba Group Holding Limited among them, on a stated basis of indirect SASAC affiliation plus a military-civil-fusion contributor designation, not any AI-specific or model-related conduct [^68]. The notice carries no penalty; 1260H is an identification mechanism whose consequences arrive through separate statutes [^68]. The consequence that bites is Section 805 of the FY2024 NDAA, effective 2026-06-30, barring the Defense Department — styled the Department of War in the 2026 notice — from entering, renewing or extending contracts directly with listed entities, with an indirect/supply-chain phase following 2027-06-30 [^69]. Three limits matter: it binds one department, not the whole government; it is prospective; and it restricts contracting *with Alibaba* — it does not prohibit a defense contractor from downloading openly licensed Qwen weights [^69]. Alibaba sued to overturn the designation in the District Court for the District of Columbia on 2026-06-11, and is on no BIS Entity List, Military End User list, or AI-specific designation — a negative finding established by absence across searches, not by a fetched BIS list, and weaker evidence accordingly [^73].

:::timeline
- {date: "2025-06-25", headline: "No Adversarial AI Act introduced", body: "S.2177 referred to committee; no further action in thirteen months."}
- {date: "2026-06-10", headline: "Alibaba designated under 1260H", body: "One of 65 additions; stated basis is indirect SASAC affiliation."}
- {date: "2026-06-12", headline: "Commerce restricts two Anthropic models", body: "Is-informed letter on Claude Fable 5 and Mythos 5; lifted 2026-06-30."}
- {date: "2026-06-30", headline: "NDAA Sec. 805 takes effect", body: "DoD barred from direct contracts with listed entities."}
- {date: "2026-07-08", headline: "Beijing weighs outbound AI controls", body: "Reported deliberations with Alibaba, ByteDance and Z.ai."}
:::

Now the asymmetry: the only 2026 US export control actually applied to model weights ran against an *American* model. Commerce sent Anthropic an "is-informed" letter on 2026-06-12 requiring a validated export licence for any foreign person to access Claude Fable 5 and Mythos 5; Anthropic took both dark worldwide until the controls were lifted 2026-06-30 — an eighteen-day outage [^70]. That letter bound one named company rather than proceeding by notice-and-comment rulemaking, so it set no generally applicable rule [^70]. Export-control jurisdiction reaches weights US firms control and cannot reach weights already published from China. A regime designed to slow rivals currently constrains only the home team.

Which is why the nearer-term threat to the promised weight drop is Chinese. Reuters reported on 2026-07-08 that Beijing was weighing outbound restrictions on Chinese frontier AI in meetings involving Alibaba, ByteDance and Z.ai, framed as a response to the Fable and Mythos controls [^74]. That is a deliberation, not a rule — but if enacted it would be the first real legal obstacle to the release. PRC law separately requires pre-launch filing for public generative AI services plus algorithm filing, with a CAC filing number a precondition of market access; no filing for Qwen3.8-Max could be confirmed, and the registry does not track model updates, so a Qwen-family filing does not establish that this checkpoint was separately assessed [^74].

The exposure enterprises will actually feel is closer to hand. Model Studio separates two dials most buyers conflate.

:::kv
- {term: Region controls, def: "Access point and data storage"}
- {term: Scope controls, def: "Where inference executes"}
- {term: Default scope, def: "Global — includes nodes inside China"}
- {term: How to restrict to the US, def: "Opt in with a -us model-name suffix"}
- {term: Singapore endpoint, def: "Scope-locked to International by default"}
:::

:::callout(kind=danger, label="Default setting")
The default inference scope is **Global**, documented as "any available node, including within and outside China." Restricting execution to the US is opt-in: "Use model names with the `-us` suffix (such as `qwen-plus-us`) to restrict inference to the US." Without the suffix, inference defaults to Global [^72].
:::

So a US enterprise calling the Virginia endpoint without the suffix may have its inference execute on nodes inside mainland China even though the access point and static storage sit in Virginia [^72]. Singapore, scope-locked to "International", excludes the Chinese mainland — arguably safer by default than Virginia [^72]. The risky dial fails open. Be precise about the statute buyers fear, though: PRC cross-border rules under PIPL bind entities processing personal information of individuals in mainland China or storing data there, so a US firm sending its own US-customer data to a Singapore or Virginia endpoint generally does not trigger provisions that govern data leaving China, not data entering Alibaba infrastructure abroad [^75]. Extraterritoriality is real — a Chinese court confirmed reach in September 2024 over a foreign-registered firm collecting from China-based individuals — but it is keyed to whose data, not whose vendor [^75]. Documented public-sector bans, likewise, target devices and procurement and name DeepSeek's consumer app, not open weights [^71].

The counterpoint: legal risk and political risk are different curves, and only one is flat. Airbnb's CEO said publicly, "We're relying a lot on Alibaba's Qwen model. It's very good. It's also fast and cheap," and a House committee subsequently opened an information request — no law was broken, and the cost landed anyway [^79]. Section 805's indirect phase lands 2027-06-30 and pulls supply chains into scope [^69], and the district court could uphold the designation [^73].

Why it matters: self-hosting open weights neutralizes the data-residency objection at the inference layer, because jurisdiction attaches to deployment, not model origin [^72] — which makes the open-weight promise a procurement question rather than an ideological one, and makes the console default, not the statute book, the thing to check first.

## 09. What would break this thesis

Every argument above is falsifiable, and several of them will be settled within weeks. Here is what would move them, in both directions.

:::statement(attr="ARA Research")
Alibaba published more checkable evidence than its rivals typically do — and that is precisely why its claims degrade under checking. The lesson is about disclosure norms, not about China.
:::

**The open-weight call is the one with a deadline.** If a 2.4T checkpoint appears on Hugging Face under Apache 2.0 or MIT during the week of 10 August 2026, the four-for-four base rate breaks and the sceptical read in section 05 is simply wrong [^44][^46]. That is a real possibility: the competitive incentive genuinely changed when Moonshot shipped a larger open model days before Qwen's preview [^9][^63], and Qwen's non-Max track does ship real frontier-scale weights [^44]. Two partial outcomes would be more revealing than either extreme — weights under a Tongyi Qianwen-style licence with a 100-million-MAU commercial trigger [^45], or only Qwen3.8-27B landing while the Max checkpoint slips. Both would technically satisfy the sentence Alibaba wrote and neither would deliver what the headline implied.

**The benchmark call dies the moment anyone runs a matched harness.** If an independent evaluator puts Qwen3.8-Max, Claude Opus 4.8 and Claude Fable 5 through Terminal-Bench 2.1 on one scaffold with one sampling policy and Qwen still leads, section 03 is wrong and the two-point margin is real [^1][^23]. As of 2026-08-03 no such run existed [^25]. The only matched-scaffold test anyone has published tested the *preview* on a single task and Qwen lost it by three points [^22] — a thin reed, and it should be treated as one. Working against Alibaba here is a specific, checkable anomaly: PaperBench jumping from 64.8 to 93.0 in a single generation is the kind of discontinuity that usually indicates a methodology change rather than a capability change, and it is the first row an independent replication should target [^1][^21].

**The autonomy call is the most robust and the most contingent.** Robust, because the human commit inside the window is a fact about a public repository, not an interpretation: `59eca7c` rewrote the coordinator's action priority on 2026-07-23 [^32]. Contingent, because a single disclosure would change the picture — if Alibaba published the run's token count, wall-clock hours, restart count and intervention log, the way it did for the paper-reproduction demo on the same blog page [^1][^37], most of section 04's scepticism would resolve one way or the other within an hour. The steelman deserves restating plainly: the 265-commit figure reproduces exactly against the GitHub API [^33], the codebase is genuinely substantial [^30], and Alibaba is one of very few vendors to name an artifact at all. An unverifiable claim and a falsified one are different things, and this is the former.

**What would break the sceptical read of the price.** Section 02 argues that verbosity inverts the sticker advantage, resting on one measurement: 150M output tokens and $2,159.51 to complete one benchmark index [^10]. If Alibaba ships a lower default `reasoning_effort`, or if the same index is re-run after serving-stack optimisation and the token count halves, the inversion narrows or disappears. Day-two measurements on a days-old serving stack are a floor, not a steady state — and Artificial Analysis publishes no measurement date, which is itself a limitation of the evidence [^10].

**The honest uncertainties.** Three gaps constrain everything above and should not be papered over. First, Qwen discloses no layer count, attention type or KV-head count, which is why the KV-cache estimate in section 06 spans a fourfold range rather than a point [^1] — a narrower disclosure would materially change the serving-economics conclusion. Second, no source in any language discloses what hardware *trained* the model; the T-Head supernode reporting covers inference serving only [^64]. Third, several load-bearing figures reach us through proxies and reconstructions rather than direct reads — Qwen's blog is JavaScript-rendered, X posts return 403 to automated fetches, and the earnings-call quotes are interpreter-mediated and come from a transcript republisher rather than Alibaba's IR site [^60].

**The argument that most threatens the whole frame.** Citi's read is that enterprise adoption is going model-agnostic, so no single model holds a moat and value accrues to full-stack platform owners [^65]. If that is right, then every claim audited here — the benchmark margin, the autonomy demo, even the licence terms — is a marketing artefact around the only thing that matters, which is whether Alibaba Cloud captures inference workloads it currently does not have. The evidence is uncomfortable for Alibaba on exactly that point: Qwen leads the world in open-model downloads and derivatives [^49][^65] and leads nothing on OpenRouter token volume [^66]. Wu's own admission that most model-as-a-service revenue still comes from Alibaba's proprietary models says the same thing from inside the company [^60].

**What the adversarial pass found.** An independent red-team review targeted this article's three load-bearing claims and tried to break them. Two survived unbroken against primary sources: the human commit inside the autonomy window, and the absence of any prior Max-tier open-weight release. The third — the attribution of the harness-asymmetry finding — turned out to be *under*-cited rather than wrong: the asymmetry is stated on Qwen's own blog, not merely reconstructed by analysts, which is a stronger footing than the draft originally claimed [^1]. Separately, a citation audit killed four figures that had looked solid, including a harness-variance number that had carried this article's deck. Those corrections are folded into the text above; they are noted here because an article about unverified claims has no standing to hide its own.

Reported plainly: Qwen3.8-Max is a competitive frontier model at a competitive price, launched by a company with a strong commercial reason to open it and a four-for-four record of not doing so [^4][^46]. The three headline claims are not lies. They are claims that were published with just enough evidence to check — and checking them is what this article did.

:::references
- {id: 1, title: "Qwen3.8-Max", url: "https://qwen.ai/blog?id=qwen3.8", source: "Qwen (Alibaba)", date: "2026-08-03"}
- {id: 2, title: "qwen3.8-max model page", url: "https://www.qwencloud.com/models/qwen3.8-max", source: QwenCloud, date: "2026-08-03"}
- {id: 3, title: "Alibaba's AI model Qwen3.8-Max made widely accessible ahead of open-weights release", url: "https://www.scmp.com/tech/article/3362738/alibabas-ai-model-qwen38-max-made-widely-accessible-ahead-open-weights-release", source: "South China Morning Post", date: "2026-08-03"}
- {id: 4, title: "Alibaba shares rally after unveiling Qwen3.8-Max AI model", url: "https://www.cnbc.com/2026/08/03/alibaba-ai-model-qwen-rival-anthropic.html", source: CNBC, date: "2026-08-03"}
- {id: 5, title: "Alibaba Qwen Releases Qwen3.8-Max", url: "https://www.marktechpost.com/2026/08/03/alibaba-qwen-releases-qwen3-8-max/", source: MarkTechPost, date: "2026-08-03"}
- {id: 6, title: "Open-weights announcement", url: "https://x.com/Alibaba_Qwen/status/2084100707423289643", source: "@Alibaba_Qwen", date: "2026-08-03"}
- {id: 7, title: "qwen3.8-max on AI Gateway", url: "https://vercel.com/ai-gateway/models/qwen3.8-max", source: Vercel, date: "2026-08-04"}
- {id: 8, title: "Model Studio model pricing", url: "https://www.alibabacloud.com/help/en/model-studio/model-pricing", source: "Alibaba Cloud", date: "2026-08-04"}
- {id: 9, title: "Alibaba Previews Qwen3.8-Max", url: "https://www.marktechpost.com/2026/07/19/alibaba-previews-qwen3-8-max-a-2-4-trillion-parameter-multimodal-model-days-after-moonshots-kimi-k3-open-weight-launch/", source: MarkTechPost, date: "2026-07-19"}
- {id: 10, title: "Qwen3.8-Max model profile", url: "https://artificialanalysis.ai/models/qwen3-8-max", source: "Artificial Analysis", date: "2026-08-04"}
- {id: 11, title: "qwen3.7-max model page", url: "https://www.qwencloud.com/models/qwen3.7-max", source: QwenCloud, date: "2026-08-04"}
- {id: 12, title: "Context cache", url: "https://docs.qwencloud.com/developer-guides/text-generation/context-cache", source: "QwenCloud docs", date: "2026-08-04"}
- {id: 13, title: "Model pricing", url: "https://platform.claude.com/docs/en/about-claude/pricing", source: Anthropic, date: "2026-08-04"}
- {id: 14, title: "API pricing", url: "https://platform.openai.com/docs/pricing", source: OpenAI, date: "2026-08-04"}
- {id: 15, title: "Gemini API pricing", url: "https://ai.google.dev/gemini-api/docs/pricing", source: Google, date: "2026-08-04"}
- {id: 16, title: "Kimi K3 chat pricing", url: "https://platform.kimi.ai/docs/pricing/chat-k3", source: Moonshot AI, date: "2026-08-04"}
- {id: 17, title: "Pricing overview", url: "https://docs.z.ai/guides/overview/pricing", source: "Z.ai", date: "2026-08-04"}
- {id: 18, title: "API pricing", url: "https://api-docs.deepseek.com/quick_start/pricing", source: DeepSeek, date: "2026-08-04"}
- {id: 19, title: "Alibaba releases Qwen3.8-Max with domestic pricing", url: "https://udn.com/news/story/7333/9667541", source: "United Daily News", date: "2026-08-03"}
- {id: 20, title: "Claude Sonnet 5", url: "https://www.anthropic.com/news/claude-sonnet-5", source: Anthropic, date: "2026-06-30"}
- {id: 21, title: "Qwen 3.8 benchmarks", url: "https://apidog.com/blog/qwen-3-8-benchmarks/", source: Apidog, date: "2026-08-03"}
- {id: 22, title: "Qwen3.8-Max benchmark: how it compares", url: "https://trilogyai.substack.com/p/qwen-38-max-benchmark-how-it-compares", source: "Trilogy AI", date: "2026-07-19"}
- {id: 23, title: "TerminalWorld", url: "https://arxiv.org/pdf/2605.22535", source: arXiv, date: "2026-05-31"}
- {id: 24, title: "Alibaba releases Qwen3.8-Max, challenging GPT-5.6 Sol and Claude Fable 5", url: "https://www.neowin.net/news/alibaba-releases-qwen38-max-challenging-gpt-56-sol-and-claude-fable-5-on-ai-benchmarks/", source: Neowin, date: "2026-08-03"}
- {id: 25, title: "Qwen3.8-Max model profile", url: "https://benchlm.ai/models/qwen3-8-max", source: BenchLM, date: "2026-08-03"}
- {id: 26, title: "Reasoning or Memorization? Unreliable Results of RL Due to Data Contamination", url: "https://arxiv.org/html/2507.10532v1", source: arXiv, date: "2025-07-14"}
- {id: 27, title: "Qwen3.8-Max preview hands-on", url: "https://www.ifanr.com/1672515", source: ifanr, date: "2026-07-20"}
- {id: 28, title: "Qwen3.8-Max debuts on Arena; QwenWork brings China state-law risk to enterprise workflows", url: "https://www.techtimes.com/articles/322773/20260803/qwen38-max-debuts-arenaai-qwenwork-brings-china-state-law-risk-enterprise-workflows.htm", source: TechTimes, date: "2026-08-03"}
- {id: 29, title: "Alibaba takes aim at OpenAI and Anthropic with Qwen3.8-Max launch", url: "https://www.infoworld.com/article/4204415/alibaba-takes-aim-at-openai-and-anthropic-with-qwen3-8-max-launch.html", source: InfoWorld, date: "2026-08-03"}
- {id: 30, title: "oh-my-cli repository metadata", url: "https://api.github.com/repos/qwen-code-dev-bot/oh-my-cli", source: "GitHub API", date: "2026-08-03"}
- {id: 31, title: "oh-my-cli contributors", url: "https://api.github.com/repos/qwen-code-dev-bot/oh-my-cli/contributors", source: "GitHub API", date: "2026-08-03"}
- {id: 32, title: "Commit 59eca7c", url: "https://api.github.com/repos/qwen-code-dev-bot/oh-my-cli/commits/59eca7c", source: "GitHub API", date: "2026-07-23"}
- {id: 33, title: "Root commit 170a3d8a", url: "https://api.github.com/repos/qwen-code-dev-bot/oh-my-cli/commits/170a3d8a326bde61f7af9710ddb281e41f411531", source: "GitHub API", date: "2026-07-13"}
- {id: 34, title: "AUTONOMY.md", url: "https://raw.githubusercontent.com/qwen-code-dev-bot/oh-my-cli/main/AUTONOMY.md", source: "oh-my-cli", date: "2026-08-03"}
- {id: 35, title: "Coordinator prompt", url: "https://raw.githubusercontent.com/qwen-code-dev-bot/oh-my-cli/main/.autonomy/prompts/coordinator.md", source: "oh-my-cli", date: "2026-08-03"}
- {id: 36, title: "Time horizon limitations", url: "https://metr.org/notes/2026-01-22-time-horizon-limitations/", source: METR, date: "2026-01-22"}
- {id: 37, title: "Alibaba's open-weight Qwen3.8-Max takes on long-horizon AI tasks", url: "https://the-decoder.com/alibabas-open-weight-qwen3-8-max-takes-on-long-horizon-ai-tasks-with-2-4-trillion-parameters/", source: "The Decoder", date: "2026-08-03"}
- {id: 38, title: "Alibaba's proprietary Qwen3.7-Max can run for 35 hours autonomously", url: "https://venturebeat.com/technology/alibabas-proprietary-qwen3-7-max-can-run-for-35-hours-autonomously-and-supports-external-harnesses-like-anthropics-claude-code", source: VentureBeat, date: "2026-05-21"}
- {id: 39, title: "Qwen3.8 launch coverage", url: "https://m.sohu.com/a/1058127944_258768", source: "Sohu / Kuai Technology", date: "2026-08-03"}
- {id: 40, title: "SWE-Marathon", url: "https://arxiv.org/abs/2606.07682", source: arXiv, date: "2026-06-05"}
- {id: 41, title: "Autonomous coding announcement", url: "https://x.com/Alibaba_Qwen/status/2084100720329130304", source: "@Alibaba_Qwen", date: "2026-08-03"}
- {id: 42, title: "oh-my-cli package record", url: "https://registry.npmjs.org/oh-my-cli", source: "npm registry", date: "2026-08-03"}
- {id: 43, title: "CI workflow", url: "https://raw.githubusercontent.com/qwen-code-dev-bot/oh-my-cli/main/.github/workflows/ci.yml", source: "oh-my-cli", date: "2026-08-03"}
- {id: 44, title: "Qwen organization model list", url: "https://huggingface.co/api/models?author=Qwen&sort=lastModified&direction=-1&limit=30", source: "Hugging Face API", date: "2026-08-04"}
- {id: 45, title: "Tongyi Qianwen License Agreement", url: "https://github.com/QwenLM/Qwen/blob/main/Tongyi%20Qianwen%20LICENSE%20AGREEMENT", source: QwenLM, date: "2026-08-04"}
- {id: 46, title: "Qwen's closed-flagship pivot", url: "https://www.digitalapplied.com/blog/qwen-closed-flagship-pivot-open-weight-retreat-2026", source: "Digital Applied", date: "2026-07-22"}
- {id: 47, title: "Alibaba's Qwen3.8 and the open-source calculus", url: "https://eu.36kr.com/en/p/3908187603621252", source: "36Kr", date: "2026-07-24"}
- {id: 48, title: "Alibaba launches Qwen3.8 with 2.4 trillion parameters", url: "https://technode.com/2026/08/03/alibaba-launches-qwen3-8-with-2-4-trillion-parameters/", source: TechNode, date: "2026-08-03"}
- {id: 49, title: "The open-model ecosystem report", url: "https://arxiv.org/html/2604.07190v2", source: "ATOM Project (arXiv)", date: "2026-05-25"}
- {id: 50, title: "The open-weight models that matter", url: "https://openrouter.ai/blog/insights/the-open-weight-models-that-matter-june-2026/", source: OpenRouter, date: "2026-06-30"}
- {id: 51, title: "DeepSeek-V3/R1 Inference System Overview", url: "https://github.com/deepseek-ai/open-infra-index/blob/main/202502OpenSourceWeek/day_6_one_more_thing_deepseekV3R1_inference_system_overview.md", source: DeepSeek, date: "2025-03-01"}
- {id: 52, title: "Deploying DeepSeek with large-scale expert parallelism", url: "https://lmsys.org/blog/2025-05-05-large-scale-ep/", source: LMSYS, date: "2025-05-05"}
- {id: 53, title: "MoE vs dense models at inference", url: "https://epoch.ai/gradient-updates/moe-vs-dense-models-inference", source: "Epoch AI", date: "2024-12-20"}
- {id: 54, title: "GB200 NVL72", url: "https://www.nvidia.com/en-us/data-center/gb200-nvl72/", source: NVIDIA, date: "2026-08-04"}
- {id: 55, title: "MoE inference optimization on GPU cloud", url: "https://www.spheron.network/blog/moe-inference-optimization-gpu-cloud/", source: Spheron, date: "2026-04-02"}
- {id: 56, title: "Inference cost variance under load", url: "https://arxiv.org/abs/2606.11690", source: arXiv, date: "2026-06-10"}
- {id: 57, title: "LLM inference price trends", url: "https://epoch.ai/data-insights/llm-inference-price-trends", source: "Epoch AI", date: "2025-03-12"}
- {id: 58, title: "China's AI models are closing the gap on a different cost curve", url: "https://technode.com/2026/07/27/chinas-ai-models-are-closing-the-gap-with-overseas-rivals-on-a-different-cost-curve/", source: TechNode, date: "2026-07-27"}
- {id: 59, title: "Q4 and FY2026 results announcement (exhibit 99.1)", url: "https://www.sec.gov/Archives/edgar/data/0001577552/000110465926060224/tm2614494d1_ex99-1.htm", source: "Alibaba Group via SEC EDGAR", date: "2026-05-13"}
- {id: 60, title: "Alibaba Q4 FY2026 earnings call transcript", url: "https://www.investing.com/news/transcripts/earnings-call-transcript-alibabas-q4-2026-shows-ai-growth-ebitda-decline-93CH-4684820", source: "Investing.com", date: "2026-05-13"}
- {id: 61, title: "Alibaba to invest RMB 380 billion in cloud and AI infrastructure", url: "https://www.alibabagroup.com/en-US/document-1830678592242057216", source: "Alibaba Group", date: "2025-02-24"}
- {id: 62, title: "Alibaba Group (BABA) stock quote", url: "https://stockanalysis.com/stocks/baba/", source: StockAnalysis, date: "2026-08-03"}
- {id: 63, title: "Alibaba unveils its most capable AI model to date, not far behind Moonshot's", url: "https://www.thestandard.com.hk/china/article/338878/Alibaba-unveils-its-most-capable-AI-model-to-date-not-far-behind-Moonshots", source: "The Standard", date: "2026-08-03"}
- {id: 64, title: "T-Head Zhenwu M890 supernode serves Qwen3.8", url: "https://www.ithome.com/0/980/677.htm", source: "IT Home", date: "2026-07-23"}
- {id: 65, title: "Alibaba's Qwen3.8-Max and China's next top AI model", url: "https://fortune.com/2026/08/03/alibaba-qwen3-8-max-china-next-top-ai-model/", source: Fortune, date: "2026-08-03"}
- {id: 66, title: "Chinese AI models take OpenRouter's top five", url: "https://dataconomy.com/2026/07/29/chinese-ai-models-openrouter-top-five/", source: Dataconomy, date: "2026-07-29"}
- {id: 67, title: "S.2177 — No Adversarial AI Act, all actions", url: "https://www.congress.gov/bill/119th-congress/senate-bill/2177/all-info", source: "Congress.gov", date: "2025-06-25"}
- {id: 68, title: "Notice of Availability of Designation of Chinese Military Companies", url: "https://www.federalregister.gov/documents/2026/06/10/2026-11571/notice-of-availability-of-designation-of-chinese-military-companies", source: "Federal Register", date: "2026-06-10"}
- {id: 69, title: "DoW updates Section 1260H list, expanding compliance obligations", url: "https://governmentcontractsnavigator.com/2026/07/22/dow-updates-section-1260h-list-expanding-compliance-obligations-for-government-contractors/", source: "Government Contracts Navigator", date: "2026-07-22"}
- {id: 70, title: "Department of Commerce restricted access to Anthropic's latest models", url: "https://www.csis.org/analysis/department-commerce-restricted-access-anthropics-latest-models-what-comes-next", source: CSIS, date: "2026-06-18"}
- {id: 71, title: "US startups push back on a Chinese open-weight AI model ban", url: "https://www.techrepublic.com/article/news-us-startups-chinese-open-weight-ai-model-ban/", source: TechRepublic, date: "2026-07-22"}
- {id: 72, title: "Model Studio regions and inference scopes", url: "https://www.alibabacloud.com/help/en/model-studio/regions/", source: "Alibaba Cloud", date: "2026-08-04"}
- {id: 73, title: "Alibaba challenges the Pentagon over its Chinese Military Companies listing", url: "https://bisi.org.uk/reports/alibaba-challenges-pentagon-over-chinese-military-companies-list-designation", source: BISI, date: "2026-06-11"}
- {id: 74, title: "China's AI services registry system: a complete guide", url: "https://oxfordchinapolicylab.org/research/china-s-ai-services-registry-system-a-complete-guide", source: "Oxford China Policy Lab", date: "2026-01-01"}
- {id: 75, title: "Chinese court releases landmark decision on cross-border transfer of personal information under the PIPL", url: "https://www.paulweiss.com/insights/client-memos/chinese-court-releases-landmark-decision-on-requirements-for-cross-border-transfer-of-personal-information-under-the-pipl", source: "Paul, Weiss", date: "2024-09-01"}
- {id: 76, title: "GPT-5.1-Codex-Max", url: "https://openai.com/index/gpt-5-1-codex-max/", source: OpenAI, date: "2025-11-19"}
- {id: 77, title: "Context management", url: "https://qwenlm.github.io/Qwen-Agent/en/guide/core_moduls/context/", source: "Qwen-Agent documentation", date: "2026-08-04"}
- {id: 79, title: "Airbnb CEO Brian Chesky called Chinese AI fast and cheap; now Congress wants answers", url: "https://www.forbes.com/sites/anishasircar/2026/05/21/airbnb-ceo-brian-chesky-called-chinese-ai-fast-and-cheap-now-congress-wants-answers/", source: Forbes, date: "2026-05-21"}
- {id: 80, title: "Alibaba unveils Qwen3.8 flagship AI model; QwenWork begins public beta testing", url: "https://www.yuantalks.com/alibaba-unveils-qwen3-8-flagship-ai-model-enterprise-ai-agent-qwenwork-begins-public-beta-testing/", source: YuanTalks, date: "2026-08-03"}
:::
