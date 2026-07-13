# Twitter Model A/B Eval

`twitter-model-ab.yml` runs a controlled head-to-head between two models on
the pipeline's REAL Twitter-summary workload, cleanly separating model
capability from harness/rescue effects:

| Leg | Lane (SSOT) | Provider route | Served model |
|---|---|---|---|
| `claude` | `twitter-ab-claude` | native Claude via `agent-run` | `claude-sonnet-5` (the production native model) |
| `zai-glm-5p2` | `twitter-ab-zai` | Z.ai Coding Plan via `agent-run` | `glm-5.2` |

Outputs land under `research/eval/twitter-ab/`:

```
research/eval/twitter-ab/
├── <date>/
│   ├── claude/          # leg output: <date>.md digest + status/ + summary + headlines
│   ├── zai-glm-5p2/     # same shape
│   ├── metrics.json     # mechanical metrics + blinding mapping + contamination verdict
│   └── judge-verdict.json  # de-blinded judge scores (when the judge ran)
└── <date>-report.md     # the human report
```

## Design

The cardinal rule is **parity** — any config asymmetry between legs
invalidates the eval. The workflow enforces it structurally:

1. **One input snapshot, byte-identical per leg.** A single
   `twitter-fetch` (production claude-tier parameters: concurrency 8, no
   pre-filter, aggregated `all.json`) stages the snapshot into
   `.ab-input/bird/` and records its sha256 (`metrics.json →
   input.all_json_sha256`, plus a manifest hash over every staged file).
   Before each leg, a **fresh copy** is placed at `.twitter-input/bird/`
   (the exact path the shared prompt hardcodes) and its sha256 + file
   count are re-verified against the snapshot — a mismatch hard-fails the
   run. After each leg the hash is taken again; a leg that mutated its
   input copy is flagged `input-mutated`. Both legs' pre-run hashes are
   recorded in `metrics.json` (`legs.<leg>.input_integrity`), which is the
   committed proof both legs consumed byte-identical input.
2. **One prompt, rendered per leg only for paths.** Both legs use the
   production `prompts/twitter-analyst.md` via the shared
   `render-twitter-prompt` composite with identical inputs — same neutral
   `harness_label` and `title_suffix` (neither model is told what it is),
   same budgets (`bird_budget` 20 / `curl_budget` 4), same cycle window —
   differing ONLY in `output_dir`/`summaries_dir` (each leg writes
   exclusively inside `research/eval/twitter-ab/<date>/<leg>/`). The
   **prompt parity guard** substitutes each leg's directory with a
   placeholder and requires the two rendered prompts to be byte-identical
   (`metrics.json → parity.normalized_prompt_sha256`); any other
   difference fails the run before model tokens are spent.
3. **One harness config.** Both legs run the same
   `.github/actions/agent-run` composite with the production claude
   tier's `--allowedTools` list, the same `--max-turns 40`, the same
   25-minute per-leg wall cap (so one hung provider call cannot take the
   other leg's results down with it), the same `BIRDY_READ_ONLY=1`
   daemon, and the same `expected-paths` / `allowed-paths` contracts. The
   only differences are the lane (which selects the provider) and the leg
   directory.
4. **No recovery.** Unlike the production lane, there is **no repair
   agent and no deterministic fallback** — a leg that fails, times out, or
   writes garbage is scored exactly as such (`continue-on-error: true`
   keeps leg B running when leg A dies). This is deliberate: the eval
   measures the model, not the rescue chain.
5. **Repo-state isolation via detached HEADs.** Each leg runs on a
   detached HEAD checked out from the same base SHA, so leg B can never
   read leg A's output, and each leg's commits stay off the branch. After
   both legs, the workflow harvests ONLY
   `research/eval/twitter-ab/<date>/<leg>/` from each leg's post-run SHA —
   an out-of-scope commit from a failed leg is structurally discarded and
   can never reach `main`. Neither leg has a prior-day file in its leg dir,
   so multi-day context is absent for both equally (each daily run is an
   independent trial).
6. **Strict, pinned lanes.** All four eval lanes in
   `data/agent-backends.json` are `strict` + `pinned`: a Z.ai outage FAILS
   the GLM leg instead of silently falling back to Claude (which would
   make the run Claude-vs-Claude). `select_backend.py`'s requested vs
   effective echo is recorded per leg and any divergence trips the
   contamination banner.

## Judging (blinded, position-swapped, true Opus)

- The judge only runs when **both** legs produced the main digest `.md`
  (and `judge` input is not `false`).
- `scripts/twitter_ab_metrics.py collect` stages
  `pass1/{A,B}.md` + `pass2/{A,B}.md` (pass 2 = positions swapped) under
  the run-scoped `/tmp/twitter-ab-<run_id>/judge/` dir. The leg→letter
  assignment is **randomized per run** and recorded ONLY in
  `metrics.json` — never in any judge-visible file.
- A fixed list of model/provider/lane strings (`claude`, `anthropic`,
  `sonnet`, `glm`, `z.ai`, `zhipu`, lane names, model ids, …) is scrubbed
  to `[redacted]` from both copies. URLs and `@handles` are preserved:
  they are quoted evidence from the shared snapshot and carry no
  authorship signal, and scrubbing them would break the judge's
  source-checking. The scrub is symmetric, and the judge is told not to
  penalize `[redacted]` tokens. Scrub-hit counts per leg are recorded in
  `metrics.json → blinding.scrub_hits`.
- The judge is a **true non-contestant**: lanes `twitter-ab-judge` /
  `twitter-ab-judge-swapped` are native Claude with the agent-run
  `native-model: claude-opus-4-8` override (that is what the `--model
  opus` alias resolves to for these two steps only) — not the
  `claude-sonnet-5` the claude leg ran on. Tools are `Read,Write` only.
- Rubric (1–10 integers per brief): coverage, faithfulness (spot-checked
  against a pretty-printed copy of the shared snapshot), headline
  quality, skepticism/source hygiene, format compliance, plus a holistic
  overall. Rationale ≤120 words per brief, and a `preferred` pick.
- **Position debias:** pass 2 re-judges with A/B contents swapped in a
  fresh context (the prompt does not reveal the swap). After de-blinding,
  the final preference is the two passes' agreement — disagreement yields
  `split` (treat as no-decision). A judge that always prefers the
  first-listed brief therefore cannot produce a winner.
- `scripts/twitter_ab_metrics.py finalize` de-blinds letter→leg, writes
  the committed `judge-verdict.json`, and merges per-leg averages into
  `metrics.json`. Missing/garbled verdicts fail open
  (`passes_parsed < 2`), never crash the run.

## Contamination guards

`metrics.json → contamination` + a banner at the top of the report:

| Guard | Trip condition | Effect |
|---|---|---|
| `backend-mismatch` | agent-run's effective backend ≠ requested, or the fallback chain was walked | CONTAMINATED |
| `model-mismatch` | served model (native-model / model-id echo) ≠ the leg's expected model | CONTAMINATED |
| `expected-model-not-observed` | the transcript's `modelUsage` never shows the expected model | CONTAMINATED |
| `input-mismatch` / `input-mutated` | staged copy ≠ snapshot hash, or the copy changed during the leg | CONTAMINATED |
| `sandbox-suspect` | `permission_denials > 0` on any leg | run marked **sandbox-suspect** (tool friction may have depressed a leg independently of model quality); not full contamination |

A CONTAMINATED report must not be read as a model comparison.

## How to dispatch

```bash
# full eval (both legs + judge)
gh workflow run twitter-model-ab.yml

# one leg only, or skip the judge
gh workflow run twitter-model-ab.yml -f legs=zai-glm-5p2 -f judge=false
```

It also runs daily at `21:40 UTC` (offset from the production twitter
crons) — **the `schedule:` block in the workflow is meant to be removed
when the eval week ends**; `workflow_dispatch` stays.

## How to read a report

`research/eval/twitter-ab/<date>-report.md`, top to bottom:

1. **Banner** — if CONTAMINATED, stop; the run is not a comparison.
   `sandbox-suspect` means read the mechanical table for which leg hit
   denials before trusting the judge deltas.
2. **Mechanical table** — per leg: `is_error`, turns, denials, cost,
   wall time, required files written (n/3: status/summary/headlines),
   digest presence, `validate_twitter_public_output.py` verdict
   (`format valid`), status/public-item/story/headline counts, input-hash
   checks, whether the leg committed.
3. **Judge table** — de-blinded per-criterion averages across the two
   position-swapped passes, and the **final preference**
   (`claude` / `zai-glm-5p2` / `tie` / `split`).
4. Single runs are noisy: judge one run's `split` or a ±1 overall delta
   as noise; look for a consistent preference across the eval week.

## Cost per run (estimate)

- `claude` leg: one Sonnet-5 agent run over a large snapshot, ≤40 turns —
  observed production twitter cycles land roughly **$1–4**; the actual
  number is recorded per run in `metrics.json → legs.claude.agent.total_cost_usd`.
- `zai-glm-5p2` leg: covered by the Z.ai Coding Plan subscription —
  **no marginal API cost** (the transcript's cost field, if any, is
  recorded as-is).
- Judge: two Opus-4-8 passes over two briefs + snapshot spot-checks,
  ≤16 turns each — roughly **$2–6** combined.
- Total: expect **~$3–10 per run**; trust the recorded
  `total_cost_usd` numbers over this estimate.

## Allowed asymmetries (documented, deliberate)

These are provider-route accommodations baked into the shared
`agent-run` composite (production behavior — the eval reuses it verbatim):

- `API_TIMEOUT_MS=3000000` on the Z.ai route (provider-latency
  accommodation; Z.ai needs the long timeout to finish long turns).
- `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` on the Z.ai route.
- `CLAUDE_CODE_EFFORT_LEVEL=max` on the non-native routes (Fireworks/Z.ai)
  — pre-existing agent-run env not set on the native path.

## Known limitations

- **Live follow-up tools:** `birdy-fast`/`curl` calls run at different
  wall-clock times per leg, so follow-up results are not identical
  (bounded by the shared 20/4 budgets). The snapshot — the primary
  input — is byte-identical.
- **Fixed leg order:** `claude` runs first, so the second leg's birdy
  follow-ups see slightly older stories and a daemon whose account
  budgets absorbed leg A's ≤20 calls. Bounded, and constant across runs.
- **Judge trust model:** blinding defends against label bias, not an
  adversarial judge — the Read tool could technically open other files.
  Same trust model as the production headline judge; the mapping is kept
  out of every staged judge file regardless.
- **Stylistic fingerprints** can't be scrubbed; a judge may recognize a
  model's voice. Position-swap + rubric anchoring reduce, not eliminate,
  this.

## Related parity fix

The production manual GLM lane (`twitter-zai` in `hourly-twitter.yml`)
was raised to the same `--max-turns 40` + claude-tier allowedTools list,
so future manual cross-model comparisons on the production workflow are
honest too. The primary claude lane and its recovery chain are untouched.
