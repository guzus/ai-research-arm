---
eyebrow: ANALYSIS · AI PRICING
title: Anthropic said 40%, Cursor said 40%, Artificial Analysis said zero — all three measured the same curve
deck: Claude Opus 5.5 shipped with a cost claim that three parties appeared to contradict each other about. They did not. The disagreement is a setting.
lede: |
  On 22 September 2026 Anthropic released Claude Opus 5.5 with a specific, checkable claim: at default settings it would cost 40% less than Opus 5 on typical workloads. Within hours Cursor said its own benchmark showed 40% less per task, and Artificial Analysis measured cost essentially flat. Those three results are not in conflict. They are three points on one downward-sloping curve whose free parameter is the `effort` setting — a dial whose default Anthropic moved underneath everyone in the same release. The interesting story is not who was right. It is that "cost per task" turned out not to be a property of a model at all.
stats:
  - {label: Advertised saving, value: "40%", note: "default settings, typical workloads"}
  - {label: Price-only saving, value: "31%", note: "Anthropic's own worked session"}
  - {label: Matched at max effort, value: "+2.0%", note: "Artificial Analysis — cost rose"}
  - {label: Each model at its default, value: "−62.9%", note: "our arithmetic on the same data"}
domain: software
---

## 01. Three numbers that were never in conflict

Anthropic's Opus 5.5 launch post makes one sentence do all the work: "Our tests show that at default settings it will cost 40% less than Opus 5 on typical workloads." [^1] Neither "default settings" nor "typical workloads" is defined anywhere on the page, and the claim carries no methodology footnote — the four numbered footnotes on that page all concern benchmarks. [^1] Within a day two other parties had published cost figures. Cursor announced that Opus 5.5 "is now available in Cursor! It's the new top model on CursorBench at 57.8% (Max) and costs 40% less per task than Opus 5." [^39] Artificial Analysis, running its Intelligence Index, measured $5.98 per task against Opus 5's $5.86 — a 2% increase. [^6,7]

Read as a dispute, that is a vendor and its largest coding-agent customer on one side and an independent benchmark on the other. Read as data, it is not a dispute at all. Artificial Analysis publishes cost per task at all five effort levels, and so does Cursor. Line the two ladders up and both show the same shape: a large saving at low effort, shrinking monotonically as effort rises, and inverting at `max`. Artificial Analysis measured `max`. Anthropic and Cursor did not.

:::callout(kind=info, label="The short answer")
- **The rate card fell 20%,** not 40%: $5/$25 to $4/$20 per million tokens. Cache reads fell 60%, to $0.20, via a model-specific pricing exception. [^2]
- **Anthropic's own engineering blog, holding token counts fixed, lands on 31%** — the pure price effect. The remaining nine points are a behavioural claim about tokens consumed. [^5]
- **Opus 5.5's API default effort is `medium`; Opus 5's was `high`.** A request that omits `effort` now runs one rung lower than it did. [^3]
- **At each model's own default, Artificial Analysis's data implies a 62.9% saving** — larger than Anthropic claimed. At matched `max` effort it implies a 2% increase. Both are true. [^7,9,10]
- **No third party has reproduced the specific 40% on a real agentic workload with disclosed methodology.** Every published "40%" traces to Anthropic or to Cursor's one-sentence post. [^31]
:::

The rest of this article does four things. It separates the part of the claim that is a price from the part that is a behaviour, because only one of them is contractual. It shows that the apparent disagreement between measurers collapses once effort is held fixed — including the uncomfortable detail that Cursor's own leaderboard contradicts Cursor's own sentence at the exact setting that sentence cites. It documents two mechanisms, both disclosed by Anthropic, that make most published numbers for this model uncontrolled experiments. And it asks the only question a buyer actually cares about: whether *your* bill falls, which turns out to be a fact about your workload that you can settle yourself in an afternoon.

One framing note, because it recurs. Throughout this piece, percentages computed from published dollar figures are flagged as our arithmetic rather than cited to a source, and dollar figures are cited to the page that printed them. The distinction matters more than usual here: almost every contested number in this story is a ratio someone computed from two figures taken at settings they did not name.

## 02. What actually changed in the rate card

Strip the behavioural half out of the claim and the rate card says something narrower than the headline: Opus 5.5 is a flat 20% cut on every metered line item except one, and that one exception — cache reads, down 60% — is a model-specific pricing carve-out rather than a general repricing.

:::stats
- {label: Input + output, value: "−20%", note: "every standard line item"}
- {label: Cache reads, value: "−60%", note: "the single exception"}
- {label: Price-only saving, value: "31%", note: "Anthropic's own worked session"}
- {label: Advertised saving, value: "40%", note: "default settings, typical workloads"}
:::

The 60% is not one decision. It is two stacked, and only the first is a price cut in the ordinary sense. Base input fell from $5 to $4 per million tokens, a 20% reduction that propagates mechanically into every category derived from it. [^2] On top of that, Anthropic changed the multiplier that converts base input price into a cache-read price. The docs are unusually blunt about it: "Cache hits and refreshes on Claude Opus 5.5 are priced at 0.05x the base input price," while "All other models use the standard 0.1x multiplier." [^2] A base 20% lower, multiplied by a coefficient cut in half, lands at 0.4 of the old rate — the 60%. The coefficient is now a per-model dial rather than a platform constant: Claude Fable 5.1 runs at 0.025x. [^2]

What did *not* move is the other half of the cache mechanism. Cache-**write** multipliers are unchanged at 1.25x base input for the five-minute TTL and 2x for the one-hour TTL, so the write side inherits only the flat 20%. [^2] That asymmetry is the whole distributional story of this release: a workload that writes a large context and reads it back hundreds of times captures the 60%; a workload that writes a fresh context per task and reuses it once or twice captures 20% and nothing more.

| Line item (per MTok) | Opus 5 | Opus 5.5 | Change |
|---|---|---|---|
| Input | $5.00 | $4.00 | −20% |
| Cache write, 5-minute | $6.25 | $5.00 | −20% |
| Cache write, 1-hour | $10.00 | $8.00 | −20% |
| *Cache read | $0.50 | $0.20 | **−60%** |
| Output | $25.00 | $20.00 | −20% |
| Batch input | $2.50 | $2.00 | −20% |
| Batch output | $12.50 | $10.00 | −20% |

Anthropic's launch post picks exactly the line item that moved most and tells you why it picked it: "Cache reads (which make up the majority of agentic and coding work costs) are $0.20 per million tokens, 60% less than Opus 5." [^1] That is a defensible weighting for an agent loop, and it is also the most favourable one available. The same post then separates the two terms explicitly — "It costs less per token than Opus 5 and uses fewer tokens per task, which nets out to a 40% drop in costs" [^1] — which is the sentence this entire article is really about.

The size of each term is recoverable from Anthropic's own cost-engineering write-up, which prices an identical session on both models while holding token counts fixed and concludes it "costs about 31% less." [^5] That 31% is the pure price effect, the part you can verify against a rate card. The gap between that 31% and the advertised 40% is entirely a claim about behaviour — fewer tokens consumed per task — and no rate card can confirm or refute it.

The same analysis sets out the four ratios that actually govern an agentic bill, and they are more extreme than the headline suggests:

:::kv
- {term: "Cached read", def: "5% of a fresh input token — down from a tenth of the input price to a twentieth"}
- {term: "One output token", def: "Costs 100 cache reads"}
- {term: "Cache write, 5-minute", def: "1.25x base input price"}
- {term: "Cache write, 1-hour", def: "2x base input price"}
:::

Those ratios dominate the 20-versus-60 question. A task consuming roughly 2.8M input tokens costs $11.20 uncached, $1.62 at a 90% cache hit rate, and about $0.99 at 96% — while 60K output tokens alone cost $1.20, more than the entire cached input. [^5] Past about a 90% hit rate, output is the bill and further cache savings are rounding error.

Three carve-outs bound the 40% further. Fast mode prices Opus 5.5 at $8/$40 per MTok against Opus 5's $10/$50 — the same 20% token cut, but at double the standard rate, first-party Claude API only and unavailable through the Batch API, so the headline number simply does not describe it. [^2] US-only inference selected via `inference_geo` carries a 1.1x multiplier across all pricing categories, and regional or multi-region endpoints carry a 10% premium over global — a data-residency requirement quietly eats half the token-price cut. [^2] And any longitudinal price series needs a tokenizer caveat: Anthropic discloses that "Claude 4.7 and later models ... use a newer tokenizer" producing "approximately 30% more tokens for the same text." [^2] Both Opus 5 and 5.5 sit on the new tokenizer, so this comparison is internally consistent — but a chart that crosses the 4.7 boundary is measuring two different units of account.

The obvious criticism — that 31% and 40% cannot both be true — is the wrong one. Anthropic states plainly that the residual comes from fewer tokens per task, so the gap is disclosed, not concealed. [^1,5] The honest objection is narrower: it publishes a reproducible worked example for the 31% and nothing comparable for the other nine points, which is the half that depends on configuration the buyer controls.

This matters because the two halves have different failure modes. The 20% is contractual and arrives whatever you do. The cache-read 60% arrives only if your context is reused, and the token-reduction residual arrives only at the effort setting Anthropic measured.

## 03. One curve, five points: the effort setting explains the whole disagreement

Cost per task is not a property of a model. It is a property of a model *plus a dial*, and on Claude Opus 5.5 that dial has five detents. Every published Opus 5.5 cost figure is defensible; they disagree only because each measurer sampled a different point on one downward-sloping curve whose free parameter is the `effort` setting — and Opus 5.5 moved where the default sits on that curve underneath everyone.

The load-bearing fact is in Anthropic's own effort documentation, and it is easy to read straight past: "Claude Opus 5.5 supports all five effort levels, and `medium` is the default (Claude Opus 5 and earlier Opus models default to `high`, so a request that omits `effort` runs one level lower than it did on Claude Opus 5)." [^3] That parenthetical *is* the dispute. Two engineers can send byte-identical request bodies to the two models, change nothing but the model string, and be measuring different amounts of thinking. Anyone who pinned `effort` explicitly measured a like-for-like swap. Anyone who omitted it — which is most people, because that is what "default settings" means — measured a swap *and* a step down the ladder, and got a much bigger number.

Artificial Analysis is the only public source that published the whole ladder for both models. For Opus 5.5 it reports cost per Intelligence Index task of $0.55 at low (index 42), $1.34 at medium (51), $1.82 at high (54), $3.46 at xhigh (56), and $5.98 at max (58). [^10] For Opus 5 the corresponding ladder runs $1.10 (39), $2.19 (45), $3.61 (48), $4.88 (50), $5.86 (51), each row carrying its own published run total — $1,560.91 over 26M output tokens at low, $2,731.91 over 49M at medium, $4,331.68 over 81M at high, $5,867.76 over 110M at xhigh, and $7,274.74 over 140M at max. Every row on both ladders was verified against Artificial Analysis's per-effort model pages, all on index v4.3.2. [^10,9,7]

:::line-chart(title="Cost per Intelligence Index task by effort level", subtitle="Artificial Analysis, index v4.3.2, as of 2026-09-22", y-unit=$)
x: low,medium,high,xhigh,max
Opus 5: 1.10,2.19,3.61,4.88,5.86
Opus 5.5: 0.55,1.34,1.82,3.46,5.98
:::

Read the two lines and the reconciliation is immediate: they start far apart and converge, then cross. Now do the comparison that "default settings" actually describes — each model at *its own* default, Opus 5.5 at medium ($1.34) against Opus 5 at high ($3.61). Our arithmetic on AA's published figures makes that a 62.9% reduction, and it arrives at a *higher* index score (51 versus 48). On Artificial Analysis's own data, the default-to-default saving is not 40%; it is substantially larger than the number Anthropic put in its headline. The measurement everyone treated as the skeptical one turns out, at the default, to be the generous one.

This is not an artifact of one harness. Cursor's published CursorBench 4.0 leaderboard reports Opus 5.5 cost per task of $13.43 at Max (57.8% score), $6.98 at XHigh (56.0%), $3.97 at High (56.0%), $2.91 at Medium (52.5%) and $1.17 at Low (43.7%), against Opus 5 at $11.95 (46.6%), $11.43 (46.1%), $9.00 (44.7%), $6.94 (43.3%) and $4.87 (40.7%). [^12]

:::slope(left-label="Opus 5", right-label="Opus 5.5", unit=$)
| Effort | Opus 5 | Opus 5.5 |
|---|---|---|
| Low | 4.87 | 1.17 |
| Medium | 6.94 | 2.91 |
| High | 9.00 | 3.97 |
| Extra High | 11.43 | 6.98 |
| Max | 11.95 | 13.43 |
:::

Four lines fall steeply. One rises. Put the matched-effort changes from both harnesses side by side — all of these percentages are our arithmetic on the published dollar figures above, not numbers either source printed:

| Effort | Artificial Analysis Δ | CursorBench Δ |
|---|---|---|
| Low | −50.0% | −76.0% |
| Medium | −38.8% | −58.1% |
| High | −49.6% | −55.9% |
| Extra high | −29.1% | −38.9% |
| *Max | +2.0% | +12.4% |

Two independent harnesses, two different workloads, two different pricing contexts, and the same shape: large savings at the bottom of the ladder, shrinking monotonically as effort rises, inverting at max. A curve that reproduces across measurement setups is a property of the model, not of anyone's methodology.

The inversion has a mechanical cause, and it is token growth outrunning a real price cut. At max effort AA measures Opus 5.5 emitting roughly 119k output tokens per task, 84k of them reasoning tokens, against Opus 5's ~73k and 43k [^8] — 260M versus 140M output tokens across the full index, with the total index run costing $8,708 versus $7,275, and AA flagging 260M as "very verbose in comparison to the median of 88M" even as the blended price per 1M fell from $3.85 to $2.94. [^6,7,11] Anthropic says the same thing in plainer words in its own release notes: "At the same effort setting the model tends to think more per turn than Claude Opus 5, most of all at `xhigh` and `max`." [^4] The vendor documented the inversion before anyone measured it.

Two further wrinkles make max-effort comparisons a bad canonical baseline anyway. Anthropic's own launch page states that "unless otherwise noted, all Claude Opus 5.5 results use adaptive thinking at max effort," while the 40%-cheaper claim is scoped "at default settings" — so the headline score and the headline price describe two different configurations of the same model. [^1] And max is not even reliably the model's ceiling: ARC Prize measured Opus 5.5 on ARC-AGI-2 at 70.1 (low), 87.5 (medium), 93.3 (high), 92.5 (xhigh) and 91.7 (max), with high beating max outright. [^24]

The counterpoint is that the ladder does not fully exonerate the claim. A customer who pinned `effort: high` a year ago and never touched it again sees a genuine, large saving — roughly half, on both harnesses. A customer running at max sees a bill that goes *up*. Anthropic's headline never says which population it is describing, and "typical workloads" quietly assumes the default-omitting majority. Nor is either ladder authoritative for a given buyer: AA's Intelligence Index is not an agentic-coding workload, CursorBench is, and they disagree by a factor of two on the size of the saving at every rung.

That matters because the disagreement people are arguing about is not epistemic — it is a configuration question wearing a measurement costume, and the only honest way to quote an Opus 5.5 price is to quote the effort level with it.

## 04. Cursor against Cursor

The most-cited independent corroboration of Anthropic's 40% figure is a single sentence that welds a max-effort benchmark score to a per-task cost claim that is false at max effort by Cursor's own published leaderboard — while Cursor's own documentation makes only the narrower, defensible claim.

A sourcing caveat first, because it bears on how much weight this sentence can carry. x.com returns HTTP 402 to automated fetchers and our runner had no X session cookies available, so the text below was recovered from search-engine snippets of the post rather than fetched at source. We could not verify it against the live timeline, and a reader should treat the wording as high-confidence but not first-party-retrieved.

:::quote(attr="@cursor_ai, 22 September 2026")
Claude Opus 5.5 is now available in Cursor! It's the new top model on CursorBench at 57.8% (Max) and costs 40% less per task than Opus 5. [^39]
:::

The 57.8% is real and it is a Max-effort result. So is the price attached to that same row — and it goes the other way. [^12]

:::compare
- {role: LOWEST, name: "Opus 5 at Max — avg cost/task", value: "$11.95"}
- {role: HIGHEST, name: "Opus 5.5 at Max — the cited 57.8% row", value: "$13.43"}
- {role: SUBJECT, name: "Cost change the sentence implies", value: "−40%"}
:::

By our own arithmetic on Cursor's published figures, Opus 5.5 at Max costs **12.4% more** per task than Opus 5 at Max, not 40% less. The mechanism is visible in the token column rather than the rate card: at Max the newer model spends 218,363 tokens across 185 steps against the older model's 85,384 tokens across 106 steps — it buys its 11-point score gain with roughly 2.6x the tokens, which a 20% per-token discount cannot absorb. [^12]

Here is the full published pairing, Cursor's numbers throughout:

| Effort | Opus 5 score | Opus 5 $/task | Opus 5.5 score | Opus 5.5 $/task |
|---|---|---|---|---|
| *Max | 46.6% | $11.95 | 57.8% | $13.43 |
| Extra High | 46.1% | $11.43 | 56.0% | $6.98 |
| High | 44.7% | $9.00 | 56.0% | $3.97 |
| Medium | 43.3% | $6.94 | 52.5% | $2.91 |
| Low | 40.7% | $4.87 | 43.7% | $1.17 |

Read down the table and the 40% has exactly one plausible home. Our arithmetic on the matched pairings gives −38.9% at Extra High, −55.9% at High, −58.1% at Medium, −76.0% at Low, and +12.4% at Max. Only the Extra High rung lands near 40%; every other iso-effort comparison is far larger or has the wrong sign. Cursor never states which pairing produced its number, and with no stated derivation it is genuinely unresolvable from public data whether Cursor computed 40% off its own Extra High row or simply adopted Anthropic's headline figure and set it beside its own top score.

This is the part that should defuse any suspicion of inflation: on Cursor's own data the *defensible* claim is bigger than the one it made. Comparing each model at its own API default — Opus 5.5 at Medium against Opus 5 at High — our arithmetic gives −67.7%. The sentence is not overstating the saving. It is attaching a real number to the wrong configuration, and the configuration it names is the one where the saving does not exist.

Two further caveats sit in Cursor's own fine print. The cost column is not what anyone pays: Cursor states that "Avg cost / task is computed by applying each model's published per-million-token pricing (input, cache read, cache write, and output) to the tokens it used on each task" — a computed list-price figure, not Cursor's realized cost and not a Cursor subscriber's bill. [^12] And the leaderboard warns that "Results are subject to variance; small differences in scores may not be statistically meaningful," which matters because Opus 5.5 scores exactly 56.0% at both Extra High and High — the same score at 1.76x the price, a gap that may be noise rather than a real efficiency cliff. [^12]

The counterpoint worth taking seriously is that CursorBench is not an audited public benchmark. Anthropic describes it as evaluating "coding agents on ambiguous, multi-file tasks taken from real Cursor sessions"; Cursor describes it as "our internal eval suite based on real Cursor sessions from our engineering team," scored with "agentic graders." [^1,12] Task count, trials per task, and harness parity across models are unpublished, so the cost column's precision — two decimal places on a per-task dollar figure — outruns what an unspecified sample size can support. That cuts against our arithmetic as much as against Cursor's.

Fairness also demands noting what this is not. Cursor's post is an independent publication, not a testimonial supplied to Anthropic: Anthropic's launch post quotes more than twenty named organisations and Cursor is not among them, with CursorBench appearing there as a benchmark cited without an attribution footnote for who computed its per-task costs. [^1] And Cursor's own model documentation for Opus 5.5 makes only the per-token claim — "It sets a new high score on CursorBench, ahead of Fable 5.1, and costs 20% less than Opus 5 per token" — with the 40% per-task figure appearing in neither the docs nor the changelog. [^13] The rigorous number is in the documentation; the loose one is in the post.

Why this matters: the single most-quoted third-party confirmation of the 40% reproduces the exact failure it is being used to corroborate — a max-effort score printed beside a non-max-effort price — which means the independent check and the original claim share a defect rather than cancelling one.

## 05. The saving is fewer steps, not shorter sentences

Anthropic's "uses fewer tokens per task" is a claim about the agent loop rather than about prose style: Opus 5.5 reaches the same result in fewer search-and-verify iterations, which is why the saving is large on debugging and checking work, close to zero on pure generation, and negative at `max`.

The launch sentence is precise if you read it as two independent terms rather than one: "It costs less per token than Opus 5 and uses fewer tokens per task, which nets out to a 40% drop in costs." [^1] The rate-card term is contractual; the consumption term is what this section tests. A third figure sits beside it and is routinely folded into the efficiency story despite measuring something else entirely — "Opus 5.5 also generates output more than 30% faster than Opus 5" [^1] is a throughput claim, and a model that emits tokens faster can still emit more of them.

Only one independent harness has published a protocol that can isolate the consumption term. Lovable states its method explicitly: "We evaluated Opus 5.5 against Opus 5 at equivalent reasoning effort levels: low, medium, and high, on the same code and with the same judges", with each task run at least three times and every difference in both tables statistically significant at the 95% confidence level. [^14] Matching effort is what makes the result interpretable — without it, any token delta is confounded with the setting, which is the whole argument of this article.

What Lovable found is a step collapse. Steps per task fell 48% / 26% / 26% at low / medium / high effort on 0-to-1 building, 47% / 34% / 34% on iterative code fixing, and 57% / 46% / 42% on verification discipline; input tokens per task moved almost in lockstep, at 46% / 21% / 26%, 36% / 27% / 29%, and 59% / 46% / 41%. [^14] Input tokens tracking steps is the tell: context re-read on each loop is the dominant cost of an agentic task, so removing loops removes input tokens mechanically.

:::stack-rows
categories: [Low, Medium, High]
rows:
  - {label: 0-to-1 building, values: [48, 26, 26]}
  - {label: Iterative code fixing, values: [47, 34, 34]}
  - {label: Verification discipline, values: [57, 46, 42]}
:::

:::note
Values are percentage *reductions* in steps per task, Opus 5 to Opus 5.5, at matched reasoning effort. Plotted as positive magnitudes; a longer row is a larger saving. [^14]
:::

The decisive evidence is the asymmetry in *output* tokens. Lovable reports output tokens falling 37% to 64% on iterative code fixing and verification discipline, but staying close to Opus 5's on 0-to-1 building, "where the work is generating the app itself" — and it attributes the gain to one-pass context gathering (chaining file listings, searches and reads into one command), batched edits, and proportionate checking, with quality tied on two task types and 4–6% better on verification discipline. [^14] A model that had simply learned to write tersely would have cut output tokens everywhere. This one cut them only where the output was scaffolding for its own search process.

:::bars
- {label: "Fix + verify — output tokens, top of range", value: "−64%", pct: 64}
- {label: "Fix + verify — output tokens, bottom of range", value: "−37%", pct: 37}
- {label: "0-to-1 building — output tokens", value: "≈ Opus 5", pct: 3}
- {label: "Verification discipline — steps, low effort", value: "−57%", pct: 57}
- {label: "0-to-1 building — steps, low effort", value: "−48%", pct: 48}
- {label: "Iterative fixing — steps, low effort", value: "−47%", pct: 47}
:::

:::quote(attr="Lovable engineering, 22 September 2026")
Opus 5.5 is now available in Lovable, and it gets you the same results as Opus 5 while finishing in a third to half fewer steps.
:::

A second vendor points the same way with weaker controls. SonarSource, running 4,444 Java tasks drawn from HumanEval, MBPP and ComplexCodeEval (544 with executable tests), measured output tokens down 40%, from 21.71M to 12.96M, and lines of code down 27.5%, with pass rate slipping slightly from 88.6% to 87.68%. [^15] Two caveats matter more than the headline: the run used a pre-release build, and it compares "Opus 5.5 High" against "Opus 5 Thinking" — not a clean matched-effort pair, so part of that 40% may be the setting rather than the model.

Push the setting the other way and the sign flips. Artificial Analysis measured Opus 5.5 at `max` effort emitting roughly 119k output tokens per task, 84k of them reasoning, against Opus 5's ~73k with 43k reasoning [^8] — 260M versus 140M across the full index, which AA called very verbose in comparison to the median of 88M. [^6,7,11] Anthropic's own documentation predicts exactly this: "At the same effort setting the model tends to think more per turn than Claude Opus 5, most of all at `xhigh` and `max`." [^4] Efficiency at low/medium/high and inflation at the top of the ladder are both first-party documented behaviour of the same weights.

The strongest disconfirming result comes from a practitioner. CodeRabbit, running its own production code-review pipeline, measured token usage **up** 40.6% to 60.1% in every configuration against its baseline, concluded that Opus 5.5's efficiency "remains an open question", and cautioned teams to verify whether lower per-token prices actually translate into lower production-review costs. [^30] It is not a clean 5-vs-5.5 comparison — its "Standard" and "Max" are pipeline configurations rather than API effort levels, and its baseline is a model mix — but it is a real bill from a real workload moving the wrong way. Lovable, meanwhile, is an Anthropic launch partner with pre-release access: its protocol is the best published, and it is not a disinterested party. The customer figures inside the launch post are weaker still, spanning a 3x range with no methodology or effort level disclosed — Factory at 20–25% fewer output tokens (explicitly medium-vs-high), Box at "a third of the tokens", Rogo at about 60%, Kiro at "about 40% fewer calls and using half the tokens", Optiver at "about half the turns, time and output tokens" [^1] — and Box published its own evaluation the same day while stating that Opus 5.5 "will be coming to Box AI soon", i.e. it was not yet shipping the model it was quoted about. [^29]

Why this matters: if the saving is fewer loops rather than fewer words, then whether your bill falls is a property of your workload, not of the model — agentic pipelines that search, patch and re-check should see most of the 40%, while generation-heavy and `max`-effort workloads should budget for the same spend or more.

## 06. The model you benchmarked may not be the model you called

Two documented mechanisms — a server-side safeguard fallback that can complete your request on an older model, and a Claude Code release that silently dropped stored effort settings — mean that a large share of the published Opus 5.5 numbers, and essentially all of the informal "I upgraded and it got cheaper" reports, are uncontrolled experiments.

The strongest evidence is not an outside audit; it is the vendor's own launch page. Anthropic states that Opus 5.5 "was evaluated with its production safeguards enabled," and that when those safeguards intervened, "cybersecurity tasks were completed by Claude Opus 4.8, and biology and frontier LLM development tasks were completed by Claude Opus 5" — a substitution the company itself says "likely reduces Claude Opus 5.5's performance on these benchmarks." [^1] The same document then runs the opposite configuration for its agentic Zapier evaluation: those AutomationBench runs "were performed without fallback models, so safeguard interventions were considered failures," producing what Anthropic calls "a lower score than Claude Opus 5.5 would achieve in practice." [^1] One launch page, two fallback regimes, no reconciliation between them — and no table column telling a reader which regime produced which row.

:::timeline
- {date: 2026-09-22, headline: "Launch page discloses substitution", body: "Anthropic reports that safeguard interventions routed cybersecurity tasks to Opus 4.8 and biology and frontier-LLM tasks to Opus 5, and says this likely reduces the published scores."}
- {date: 2026-09-22, headline: "The same page runs the opposite config", body: "AutomationBench is evaluated with no fallback models, scoring every safeguard intervention as a failure — a lower number than the model would achieve in practice."}
- {date: 2026-09-22, headline: "Claude Code 2.1.280 resets stored effort", body: "The release adds Opus 5.5 and notes a saved /effort level no longer carries over to newly released models; users pinned to high land on the new default."}
- {date: 2026-09-22, headline: "Users report running at medium without knowing", body: "Independent commenters describe the model reporting Effort medium hours after launch, while believing high was still set."}
- {date: 2026-09-23, headline: "Third parties publish under disclosed but unquantified fallback", body: "Vals AI publishes fallback-penalised scores alongside its headline; Artificial Analysis labels its run Default Fallback but reports no intervention rate."}
:::

The mechanism is documented in detail. Anthropic's refusals-and-fallback documentation defines five refusal categories — `cyber`, `bio`, `frontier_llm`, `reasoning_extraction`, `general_harms` — and warns that ordinary work trips them, noting flatly that "Benign cybersecurity work can also trigger this category." [^16] Setting `fallbacks` to `"default"` makes the API retry a declined request on whichever model Anthropic recommends for that category, and "For categories with no recommended fallback, the refusal stands." [^16] The disclosure stops one step short of usefulness: the docs decline to publish the category-to-model mapping, stating that "The routing is applied server-side and is not published per model on the Models API." [^16] That absence is itself the finding. A caller who enabled fallback cannot determine from the API which model produced a given answer.

:::callout(kind=warn, label=Unreconstructable)
Fallback routing is also **sticky**. After a conversation falls back, the API records which model served it; that record "is retained for approximately 1 hour and is scoped to your organization," is best-effort, and a sticky-served turn "carries no `fallback` content block, because no model declined that turn." [^16] Combine that with the unpublished category-to-model mapping and a single early refusal can move an entire hour of subsequent work onto an older model with no per-turn signal — so a caller cannot reconstruct, even after the fact, which model served which turn of a session.
:::

Vals AI is the only operator that has measured the size of the effect. It ran Opus 5.5 "with Claude Opus 5 and Claude Opus 4.8 as server-side fallbacks for refusals," then published what happens if fallback-assisted tasks are scored as failures: Terminal-Bench 4.0 drops from 61.62% to 53.54%, with 30 of 198 tasks affected, and SRE Bench collapses from 33.59% to 5.34% because 217 of 262 tasks — 82.8% — were fallback-assisted. [^17] On that second benchmark the published headline is substantially a measurement of Opus 4.8 wearing an Opus 5.5 label.

The spread this produces across operators is wider than most of the disputes the industry does argue about.

| Operator | Score | Configuration |
|---|---|---|
| Anthropic | 66.4% | xhigh effort, own harness, safeguards enabled with fallbacks |
| Vals AI | 61.62% | max effort, server-side fallback enabled |
| Artificial Analysis | 59.6% | adaptive reasoning, max effort, default fallback |
| *Vals AI, fallback penalised | 53.54% | fallback-assisted tasks scored as failures |

Roughly thirteen points on one benchmark, for one model, in one week — and nobody frames it as a dispute, because each operator is reporting its own configuration honestly. [^1,17,11] What nobody reports is a rate. Neither Anthropic's launch page, nor its fallback documentation, nor METR's predeployment evaluation publishes an intervention frequency; METR's summary does not mention safety classifiers, refusals, or fallback at all, and its finding — "an incremental improvement above Fable 5.1 on our quantitative evaluations, rather than a discontinuous jump" — comes with its own qualifications: API access over ten business days, an unpaid engagement, and a first draft written by METR that "then Anthropic had the opportunity to review and edit." [^1,16,25]

The second mechanism is the one that invalidates the anecdotes. Claude Code 2.1.280 added Opus 5.5 and noted that a stored `/effort` level "no longer carries over to newly released models such as Opus 5.5," so a user who had pinned `high` on Opus 5 silently lands on Opus 5.5's `medium` default; independent users reported exactly that within hours, one observing the model running at `Effort: medium` while believing high was set. [^22,36] The same release also flipped the default model on Pro and Team Standard plans from Sonnet to Opus. [^22] Two caveats on that evidence, stated plainly: the changelog wording was retrieved through a summarising reader rather than byte-verified, and the corroborating user reports are pseudonymous forum comments. Anyone who upgraded, felt the bill move, and posted about it was comparing two different effort levels on two different models at once.

The counterpoint matters and is not small. On the first-party Claude API, fallback is opt-in and in beta — you must set `fallbacks` and send the `server-side-fallback-2026-07-01` beta header on every request, because the docs insist you "Make fallback a property of the request, not of ambient state." [^16] So the framing that "A request sent to Opus 5.5 could, in fact, be handled by Opus 4.8 or Opus 5 instead" is true per Anthropic's own launch page, but the headline word "secretly" overstates the first-party case, and the article asserting it carries no link to a primary source in those paragraphs. [^26,1] Evaluators showing "Default Fallback" in their run labels turned it on deliberately. [^6] And note the direction of the distortion: safeguard fallback demonstrably depresses *scores*, and nobody — not Anthropic, not Vals AI, not Artificial Analysis — has published what it does to *cost*, in either direction.

Which is the point: a number that changes by thirteen points depending on who ran it, and by an unknown amount depending on how often a server-side classifier fired, is not yet a measurement of a model.

## 07. Whether your bill falls is a fact about your workload

The rate card already decides who captures 60% and who captures 20%, and the same API that bills you ships every token-accounting field needed to settle the question on your own traffic — which makes this one of the rare vendor claims a customer can audit rather than argue about. Anthropic's own cost analysis publishes the spread rather than the headline: cache-dominated sessions save "up to 60% on input," while short prompts that produce long answers save "up to 20%." [^5] The advertised 40% is the midpoint of a distribution whose ends differ by a factor of three, and your position on it is fixed by the ratio of cached input to fresh input to output — a property of your traffic, not of the model.

:::rank-list
- {label: "Long agentic session, high cache reuse", value: "up to −60% input", pct: 100, highlight: true}
- {label: "Batch pipeline, stable shared prefix", value: "read-dominated", pct: 80}
- {label: "Mixed agentic, partial reuse", value: "near the advertised 40%", pct: 64}
- {label: "Write-heavy, low reuse", value: "write price unchanged", pct: 34}
- {label: "Short prompt, long answer", value: "up to −20%", pct: 32}
- {label: "Max-effort, output-dominated", value: "≈0 or worse", pct: 8}
:::

The ratios that fix that position are arithmetic, not judgment. On Opus 5.5 a cached read costs 5% of a fresh input token, and one output token costs about 100 times a cache read. [^5] Anthropic's worked example: a task consuming 2.8M input tokens costs $11.20 uncached, $1.62 at a 90% cache hit rate, and roughly $0.99 at 96% — while the 60K output tokens that same task generates cost $1.20 either way. [^5] Read together, a threshold appears. Somewhere near a 90% hit rate the bill stops being an input bill; past it, output dominates and every further point of cache efficiency is rounding error against a generation cost the discount never touched.

:::donut(center-label="$2.82")
- {label: "Input (90% from cache)", value: 1.62}
- {label: "Output, 60K tokens", value: 1.20}
:::

:::source
Anthropic, "What a task costs on Opus 5.5" — worked 2.8M-input-token task at a 90% cache hit rate.
:::

That ceiling has a floor under it. Cache **write** multipliers are unchanged — 1.25x base input for the five-minute TTL, 2x for the one-hour TTL [^2] — so the 60% read cut never reaches a workload that writes a large prefix and reads it once. A context that churns every request pays the old write premium and keeps only the flat 20%. [^5] Which bucket you occupy is not a matter of opinion, because the Messages API decomposes it on every response.

:::kv
- {term: "input_tokens", def: "Uncached input counted only AFTER the last cache breakpoint — not the whole prompt."}
- {term: "cache_read_input_tokens", def: "Prefix tokens served from cache, billed at 5% of base input."}
- {term: "cache_creation_input_tokens", def: "Tokens written into the cache at the 1.25x or 2x write multiplier."}
- {term: "cache_creation.ephemeral_5m / _1h_input_tokens", def: "Splits that write between the two TTLs, so it can be priced correctly."}
- {term: "output_tokens", def: "Every generated token, including reasoning you never see."}
- {term: "output_tokens_details.thinking_tokens", def: "The reasoning share of output — the only view into what thinking cost."}
:::

The documented identity is `total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens`, and the first trap sits inside it: `input_tokens` counts only tokens after the last cache breakpoint, so summing that field across a session — the obvious move — badly understates real input. [^18] The second trap is that part of the bill is invisible by construction. The docs are blunt: "The billed output token count does not match the visible token count in the response. You are billed for the full thinking process, not the thinking content visible in the response." [^19] On Opus 5.5 thinking is always on and cannot be turned off — setting the `thinking` block to type `disabled` returns a 400 at every effort level [^3] — and one Anthropic example shows 312 of 348 output tokens being reasoning the caller never sees. [^19]

The third trap destroys the evidence you are gathering. Changing top-level `effort` between requests invalidates the prompt cache; Anthropic's runnable demo shows a request flipping from `high` to `medium` turning a full 3,546-token cache read into a 3,546-token cache write. [^3,19] The natural back-to-back comparison therefore pays full input price on its second leg and *understates* the saving. The escape hatch is a per-message effort change under the `mid-conversation-output-config-2026-07-01` beta header, which preserves the cache on Opus 5.5, Opus 5, Fable 5.1 and Mythos 5.1. [^3,19] Two smaller distortions finish the list: cache lifetime is clocked from the start of the request that writes or reads the entry, not from the end of its response [^18] — a four-minute streamed answer leaves about a minute of a five-minute window, and if both cache fields return 0 the prompt was simply never cached [^18] — and platform choices multiply on top, with `inference_geo: "us"` adding 1.1x to every category including cache reads, regional endpoints carrying a 10% premium over global, and fast mode at $8/$40 confined to first-party Claude API with no Batch support. [^2]

Anthropic's own advice is to run an effort sweep on your evals rather than carry settings over from an earlier model, and to set a large `max_tokens` at higher levels. [^3] The gap is conspicuous: no before/after cost-audit recipe is published anywhere, and the cost-optimisation guide carries no Opus 5.5 sweep at all, though it does publish measured dollar sweeps for Opus 5. [^23] The one real before/after Anthropic offers is modest and hedged — a 44-ticket prompt-audit benchmark moving from Opus 4.8 at default to Opus 5.5 at low effort "cut the benchmark's cost by about 18%," prompt edits adding roughly another 9%, with the caution that it "comes from one benchmark, so treat it as an example rather than a number to expect." [^5]

The objection that lands hardest is that this audit is an API customer's privilege, and they are the minority. Claude Code and the Claude apps bill a subscription, so the rate card never reaches those users and no token accounting is exposed to them at all. Anthropic said it was "increasing five-hour usage limits on Pro, Max, Team, and seat-based Enterprise plans" without quantifying it [^1]; a claim that limits stretch about 25% further appears in the cost blog [^5]; the widely-reported "+20%" figure could not be confirmed in any primary source. Meanwhile Claude Code 2.1.280 switched the default model on Pro and Team Standard from Sonnet to Opus — changing what a subscriber consumes per prompt independently of any limit change [^22] — and that changelog wording was retrieved through a summarising reader rather than read directly.

Why this matters: a benchmark can only report the average of whatever mixture it happened to run, so the only number that describes your bill is the one your own `usage` object produces — and arguing about the vendor's figure is now strictly more work than measuring your own.

## 08. Forty percent is below the industry's own run rate

Measured against the background rate at which the cost of a fixed level of AI capability actually falls, a 40% cut spread over ten months is not a discount — it is a lag, and the mechanism behind that is structural rather than cynical.

The same day Opus 5.5 shipped, Epoch AI published its measurement of that background rate: across five benchmarks since 2023, the cost of achieving a given level of AI performance has fallen an average of about 47% per quarter, roughly 13x per year. [^20] The decline is consistent enough across task types to be hard to dismiss as a benchmark artifact — 47.1% per quarter on AIME OTIS Mock, 43.0% on Chess Puzzles, 53.1% on FrontierMath tiers 1–3, 47.0% on GPQA Diamond, and 44.0% on Mystery Game Puzzles. [^20] The single most vivid instance: o3 scoring 75% on GPQA Diamond cost $0.30 per question on 2025-01-31, and GPT-5.6 Luna reached the same bar at $0.0004 — a 725x fall in under eighteen months. [^20]

Now the Opus line, at list price, over the same window.

:::line-chart(title="Anthropic Opus-line list price", subtitle="Input and output, USD per million tokens, at launch", y-unit=$)
x: 2024-03,2025-05,2025-08,2025-11,2026-02,2026-04,2026-05,2026-07,2026-09
Input: 15,15,15,5,5,5,5,5,4
Output: 75,75,75,25,25,25,25,25,20
:::

:::note
Price levels are from Anthropic's current pricing documentation; launch months are from its dated announcement posts. The 2024-03, 2025-11 and 2026-09 points are the only ones where the price changed — the six intermediate releases all shipped on the rate card already in force. [^2,21]
:::

Claude 3 Opus launched on 2024-03-04 at $15/$75 per million input/output tokens, and Opus 4 and 4.1 shipped at exactly that rate card fourteen and seventeen months later. [^2,21] Opus 4.5 cut it to $5/$25 on 2025-11-24, and then the price sat at $5/$25 across five consecutive releases — 4.5, 4.6, 4.7, 4.8, and Opus 5 — before Opus 5.5 moved it to $4/$20. [^2,21] Deflation on this line is stepwise and infrequent, not the smooth exponential Epoch's frontier traces.

:::timeline
- {date: 2024-03, headline: "Claude 3 Opus at $15/$75", body: "The rate card that would hold for three consecutive releases."}
- {date: 2025-08, headline: "Opus 4.1 — still $15/$75", body: "Third straight launch at the original price."}
- {date: 2025-11, headline: "Opus 4.5 cuts to $5/$25", body: "A 3x step down, paired with a much larger efficiency claim."}
- {date: 2026-05, headline: "Opus 4.8 — fourth release at $5/$25", body: "Four launches, no price movement."}
- {date: 2026-07, headline: "Opus 5 — fifth release at $5/$25", body: "The flat stretch reaches nine months."}
- {date: 2026-09, headline: "Opus 5.5 cuts to $4/$20", body: "A 20% token-price cut, ten months after the previous step."}
:::

Our arithmetic on that series, not a sourced figure: $15 input to $4 input over roughly 2.55 years is a 3.75x fall, about 1.68x per year — roughly eight times slower than Epoch's 13x. The Opus 4.5 to 5.5 step alone is a 20% token-price cut over 302 days, about 1.31x annualised. And even granting the full 40% cost-per-task claim at face value over that same 302-day gap, the implied rate is about 1.85x per year, or roughly 14% per quarter — under a third of Epoch's 47% average.

:::compare
- {role: HIGHEST, name: "Epoch frontier, freshly-SOTA capability", value: "75x/yr"}
- {role: LOWEST, name: "Anthropic Opus list price, 2024-03 to 2026-09", value: "1.7x/yr"}
- {role: SUBJECT, name: "Opus 4.5 to 5.5, cost per task at 40%", value: "1.9x/yr"}
:::

Here is where the comparison has to be handled honestly, because the two series are not commensurable and presenting the gap as hypocrisy would be wrong. Epoch defines its curve as "the lowest cost at which at least one available model can meet or beat a given accuracy target" — the *cheapest* model clearing a *fixed* bar, whoever ships it. [^20] That bar is relentlessly undercut from below by smaller, later, distilled models. Anthropic prices its flagship at a bar that rises with every release. A frontier vendor matching Epoch's rate would have to price this year's best model like last year's commodity, which is a different business. Epoch's own decomposition makes the point quantitatively: cost falls 66% per quarter (75x per year) for performance that has just debuted as state of the art, and only 32% per quarter (4.7x per year) for capability two years old. [^20] The deflation is real and enormous. It simply does not happen to the flagship SKU, and the flagship SKU is what a launch post prices.

Three further cautions cut against reading either series too cleanly. First, a naive long-run $/MTok chart of the Opus line is not measuring a constant unit: Anthropic's pricing documentation discloses that "Claude 4.7 and later models ... use a newer tokenizer" that "produces approximately 30% more tokens for the same text," so a flat headline rate across that boundary is a real price increase per unit of English — and the Opus 4.5-to-5.5 comparison crosses it. [^2] The 5-to-5.5 comparison, with both models on the new tokenizer, is internally consistent. Second, falling token prices do not reliably produce falling bills, and this article's own subject is the cleanest demonstration of it: at max effort Opus 5.5's blended price per million tokens fell 24%, from $3.85 to $2.94, while its cost per task still *rose* to $5.98 from $5.86, because token consumption grew faster than price fell. [^6,7,8] A per-token price cut is a necessary but not sufficient condition for a smaller invoice. Third, Epoch flags its own limitation plainly — "Essentially no user stays permanently on the cost frontier" — and its GPQA sensitivity check spans 42.9% to 58.0% per quarter, or 9.4x to 32.1x per year, making 13x a central estimate rather than a tight bound. [^20]

That looseness is not Epoch's failing so much as the field's. There is no ratified standard for agentic cost reporting, only proposals, and they do not even agree on what to put in the denominator. The Cost-of-Pass framework prices a task as the dollars expected to buy one correct solution, which makes accuracy and spend a single number rather than two. [^33] METR's "expenditure horizon" instead asks for the dollar budget at which an agent matches a human's marginal productivity, and is explicitly a proof of concept. [^34] Epoch's frontier is a third definition again. Three incompatible denominators and no ratified standard is precisely the condition under which a vendor gets to choose the flattering one — which is not an accusation so much as a description of the incentive. Nor can we yet place Opus 5.5 on Epoch's curve directly — its benchmarking hub carried no Claude Opus 5.5 entry as of 2026-09-23, which is a timing fact about a one-day-old model, not a judgment. [^20]

None of this is new house style, either. At Opus 4.5 the same pairing appeared: a token-price cut alongside a far larger efficiency claim measured at a reduced effort setting — "Set to a medium effort level, Opus 4.5 matches Sonnet 4.5's best score on SWE-bench Verified, but uses 76% fewer output tokens." [^21] That one was cross-tier, Opus against Sonnet, where Opus costs far more per token and 76% fewer tokens was needed merely to break even — a weaker claim shape than an intra-tier comparison, and worth separating from it.

Why this matters: a buyer who reads 40% as generous is benchmarking against the vendor's own past prices, when the relevant comparison is what a fixed capability level will cost from *anyone* ten months from now — and on that measure, staying on the flagship is the expensive choice.

## 09. What would break this thesis

The argument of this article is narrow and therefore falsifiable: the three headline numbers are consistent because cost per task is a function of the effort setting, and the measurers sampled different points. Here is what would break it, and where the evidence is genuinely thin.

**The ladder could be wrong.** Everything rests on two published cost-per-effort tables. Both were verified row by row at source, and both are single-operator measurements — which is a different and weaker thing than a reproduced one. [^9,7,10] Cursor's is the more fragile: task count, trials per task, and cross-model harness parity are all unpublished, and Cursor itself warns that "small differences in scores may not be statistically meaningful," which matters when Opus 5.5 posts an identical 56.0% at two adjacent rungs priced 1.76x apart. [^12] Neither ladder has been reproduced by a third party. If either turns out to be mis-configured — a wrong effort label, a stale rate card applied to the token counts — the reconciliation in this article goes with it.

**Nobody has actually reproduced the 40%.** This is the largest hole and it should be stated without hedging. No third party has published a measurement of Anthropic's specific claim — default settings, typical agentic workload, disclosed methodology. Every published "40%" traces back either to Anthropic's sentence or to Cursor's post; Vercel, for instance, relays it with explicit attribution rather than measuring it. [^31] The independent measurements that do exist (Artificial Analysis, Lovable, SonarSource, Vals AI, CodeRabbit) each measure something adjacent and none converges on 40%. That the surrounding evidence is directionally consistent is not the same as the claim being verified.

**The mechanism story could be an artifact of one harness.** The "fewer steps, not fewer words" finding rests most heavily on Lovable, which is an Anthropic launch partner with pre-release access, publishes no absolute numbers or dollar figures, and does not state that prompts were held identical across models. [^14] SonarSource corroborates the direction but ran a pre-release build and compared "Opus 5.5 High" against "Opus 5 Thinking" — not a matched pair. [^15] CodeRabbit measured token usage rising 40.6% to 60.1% in every configuration and concluded efficiency "remains an open question." [^30] If more production harnesses report CodeRabbit's result than Lovable's, the mechanism claim inverts.

**Safeguard routing could be doing more work than anyone has measured.** Anthropic discloses that benchmark runs substituted Opus 4.8 and Opus 5 for flagged tasks, and Vals AI showed that penalising fallback-assisted tasks moves SRE Bench from 33.59% to 5.34%. [^1,17] Neither Anthropic nor any benchmark operator has published an intervention *rate*, or any estimate of what fallback does to cost rather than score. [^1,16,25] If interventions are frequent on coding traffic, then every cost figure in this article — ours included — is an average over a model mixture.

**The honest counter-case for Anthropic.** It is worth stating plainly, because the article is critical of the framing rather than of the product. Anthropic disclosed the effort-default change in its own documentation before anyone found it [^3]; it disclosed that benchmarks ran at max effort while the cost claim ran at default [^1]; it disclosed the safeguard substitution and said it probably depressed its own scores [^1]; it published a worked cost example that lands on 31% rather than the more flattering 40% [^5]; and it ships every token-accounting field a customer needs to check the claim independently. [^18,19] On its own data, the default-to-default saving is larger than the number it advertised, not smaller. The criticism that survives all that is a narrow one about configuration disclosure: a cost claim and a capability claim measured at different settings, printed on the same page, without either being labelled in the other's presence.

**And the counter-case against reading any of this as settled.** The model was one day old when this was written, and Epoch AI's benchmarking hub had no entry for it. [^20] Most of the figures here come from operators who had pre-release access — Lovable, SonarSource and Box all say so — which is a population with an obvious selection bias, and most of the customers Anthropic quoted by name published nothing of their own, so their striking efficiency numbers exist only as quotes on the vendor's launch page. [^1,14,15,29] Day-one availability was also uneven enough to thin the evidence base further: GitHub shipped Opus 5.5 to Copilot's paid tiers only and staged the rollout. [^37] Most of the disconfirming evidence that will eventually exist has not been published yet.

**An adversarial pass did not break the core.** The article's three load-bearing claims — the `medium`-versus-`high` default asymmetry, the $13.43-versus-$11.95 CursorBench Max inversion, and the 62.9% default-to-default saving implied by Artificial Analysis's ladder — were each attacked with targeted searches for contradicting primary sources. All three survived: the Anthropic documentation states the effort asymmetry twice on separate pages, Cursor's leaderboard still prints both Max figures to the cent, and three separate Artificial Analysis pages agree on the ladder. That is a floor on confidence, not a ceiling; the searches ran one day after launch, against sources that had not yet had time to be corrected.

The single most useful thing a reader can do is not to adjudicate between any of these numbers but to run the effort sweep Anthropic itself recommends on their own traffic, and read their own `usage` object. [^3,18]

:::statement(attr="ARA Research")
The honest version of the claim is not "Opus 5.5 is 40% cheaper." It is "Opus 5.5 does the same work at a lower effort setting, and a lower effort setting costs less." Those are different sentences, and only one of them is about a price.
:::

:::references
- {id: 1, title: "Claude Opus 5.5", url: "https://www.anthropic.com/news/claude-opus-5-5", source: Anthropic, date: "2026-09-22"}
- {id: 2, title: "Pricing", url: "https://platform.claude.com/docs/en/about-claude/pricing", source: "Anthropic docs", date: "2026-09-23"}
- {id: 3, title: "Effort", url: "https://platform.claude.com/docs/en/build-with-claude/effort", source: "Anthropic docs", date: "2026-09-23"}
- {id: 4, title: "What's new in Claude Opus 5.5", url: "https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5", source: "Anthropic docs", date: "2026-09-22"}
- {id: 5, title: "What a task costs on Opus 5.5", url: "https://claude.com/blog/what-a-task-costs-on-opus-5-5", source: Anthropic, date: "2026-09-22"}
- {id: 6, title: "Claude Opus 5.5 (Adaptive Reasoning, Max Effort, Default Fallback)", url: "https://artificialanalysis.ai/models/claude-opus-5-5", source: "Artificial Analysis", date: "2026-09-22"}
- {id: 7, title: "Claude Opus 5 (Adaptive Reasoning, Max Effort)", url: "https://artificialanalysis.ai/models/claude-opus-5", source: "Artificial Analysis", date: "2026-09-22"}
- {id: 8, title: "Claude Opus 5.5 vs Claude Opus 5", url: "https://artificialanalysis.ai/models/comparisons/claude-opus-5-5-vs-claude-opus-5", source: "Artificial Analysis", date: "2026-09-22"}
- {id: 9, title: "Claude Opus 5 (Adaptive Reasoning, High Effort)", url: "https://artificialanalysis.ai/models/claude-opus-5-high", source: "Artificial Analysis", date: "2026-09-22"}
- {id: 10, title: "Claude Opus 5.5 release — cost and intelligence by effort level", url: "https://artificialanalysis.ai/models/releases/claude-opus-5-5", source: "Artificial Analysis", date: "2026-09-22"}
- {id: 11, title: "Claude Opus 5.5 analysis", url: "https://artificialanalysis.ai/articles/claude-opus-5-5", source: "Artificial Analysis", date: "2026-09-22"}
- {id: 12, title: "CursorBench 4.0 leaderboard", url: "https://cursor.com/cursorbench", source: Cursor, date: "2026-09-22"}
- {id: 13, title: "Claude Opus 5.5 in Cursor", url: "https://cursor.com/docs/models/claude-opus-5-5", source: "Cursor docs", date: "2026-09-22"}
- {id: 14, title: "Faster builds, same quality: Opus 5.5 now in Lovable", url: "https://lovable.dev/blog/opus-5-5-now-in-lovable", source: Lovable, date: "2026-09-22"}
- {id: 15, title: "Claude Opus 5.5: an evaluation", url: "https://www.sonarsource.com/blog/claude-opus-5-5-an-evaluation/", source: SonarSource, date: "2026-09-22"}
- {id: 16, title: "Refusals and fallback", url: "https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback", source: "Anthropic docs", date: "2026-09-23"}
- {id: 17, title: "Claude Opus 5.5 model report", url: "https://www.vals.ai/models/anthropic_claude-opus-5-5", source: "Vals AI", date: "2026-09-22"}
- {id: 18, title: "Prompt caching", url: "https://platform.claude.com/docs/en/build-with-claude/prompt-caching", source: "Anthropic docs", date: "2026-09-23"}
- {id: 19, title: "Thinking, steering and cost", url: "https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost", source: "Anthropic docs", date: "2026-09-23"}
- {id: 20, title: "The plunging price of thought", url: "https://epoch.ai/publications/the-plunging-price-of-thought", source: "Epoch AI", date: "2026-09-22"}
- {id: 21, title: "Claude Opus 4.5", url: "https://www.anthropic.com/news/claude-opus-4-5", source: Anthropic, date: "2025-11-24"}
- {id: 22, title: "Claude Code CHANGELOG, v2.1.280", url: "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md", source: GitHub, date: "2026-09-22"}
- {id: 23, title: "Optimizing for cost and intelligence", url: "https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence", source: "Anthropic docs", date: "2026-09-23"}
- {id: 24, title: "Claude Opus 5.5 results", url: "https://arcprize.org/results/anthropic-claude-opus-5-5", source: "ARC Prize", date: "2026-09-22"}
- {id: 25, title: "Summary of METR's predeployment evaluation of Claude Opus 5.5", url: "https://metr.org/blog/2026-09-22-claude-opus-5-5/", source: METR, date: "2026-09-22"}
- {id: 26, title: "Anthropic releases Opus 5.5 and cuts pricing by 20%", url: "https://thenewstack.io/claude-opus-5-5-release/", source: "The New Stack", date: "2026-09-22"}
- {id: 29, title: "Claude Opus 5.5: faster and leaner high-quality work", url: "https://blog.box.com/claude-opus-55-faster-and-leaner-high-quality-work", source: Box, date: "2026-09-22"}
- {id: 30, title: "Opus 5.5 model review", url: "https://www.coderabbit.ai/blog/opus-5-5-model-review", source: CodeRabbit, date: "2026-09-22"}
- {id: 31, title: "Claude Opus 5.5 now available on AI Gateway", url: "https://vercel.com/changelog/claude-opus-5-5-now-available-on-ai-gateway", source: Vercel, date: "2026-09-22"}
- {id: 33, title: "Cost-of-Pass: an economic framework for evaluating language models", url: "https://arxiv.org/abs/2504.13359", source: arXiv, date: "2025-04-17"}
- {id: 34, title: "Expenditure horizon", url: "https://metr.org/blog/2026-07-21-expenditure-horizon/", source: METR, date: "2026-07-21"}
- {id: 36, title: "Claude Opus 5.5 discussion thread", url: "https://news.ycombinator.com/item?id=49803892", source: "Hacker News", date: "2026-09-22"}
- {id: 37, title: "Claude Opus 5.5 is now available in GitHub Copilot", url: "https://github.blog/changelog/2026-09-22-claude-opus-5-5-is-now-available-in-github-copilot/", source: GitHub, date: "2026-09-22"}
- {id: 39, title: "Claude Opus 5.5 is now available in Cursor", url: "https://x.com/cursor_ai/status/2102448392773435706", source: "Cursor on X", date: "2026-09-22"}
:::
