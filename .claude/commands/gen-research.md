---
description: Research a topic with primary sources and write an HTML article. Asks first whether to run locally (in-chat, ~5-15 min) or route to the GitHub workflow (self-hosted runner, ~20-45 min, deeper output).
argument-hint: <topic>
---

# Generative Research

User-supplied topic: **$ARGUMENTS**

If the topic above is empty or just whitespace, ask the user for
a topic and stop until they answer.

## Step 1 — choose execution mode (always ask)

Use `AskUserQuestion` to ask the user how they want this run
executed. DO NOT skip this prompt — the two modes have very
different cost, latency, and depth profiles. Present these two
options:

- **Run locally (in this chat)** — ~5–15 min. Deep pipeline runs
  in the current session using sub-agents (Task tool), evidence
  packets, and a verifier pass. Article lands as a local commit
  in `research/generative/` (not pushed). Recommended for topics
  you want to iterate on, or when you want to read the result
  immediately.
- **Route to GitHub workflow** — ~20–45 min on the self-hosted
  runner. Dispatches `generative-research.yml` with
  `backend=deepseek-v4-pro` by default. Your chat is freed instantly. The runner
  produces a longer article (4500–7000 words target, ≥20 cited
  references) and pushes the commit directly to `main`.
  Recommended for substantive topics where you want maximum depth
  without spending in-chat time.

After the user picks:

- **Route** → follow PATH A below.
- **Run locally** → follow PATH B below.

---

## PATH A — Route to the GitHub workflow

Dispatch the workflow with the user's topic. Use `deepseek-v4-pro` as
the backend unless the user explicitly asked for Claude in their brief.

```bash
gh workflow run generative-research.yml \
  -f topic="<the exact topic the user gave>" \
  -f backend=deepseek-v4-pro
```

Then wait briefly for the run to register and surface its URL:

```bash
sleep 5
gh run list --workflow=generative-research.yml --limit 1 \
  --json databaseId,status,url,createdAt,event \
  --jq '.[0]'
```

Report to the user in one short message:

- "Dispatched to GitHub workflow."
- The run URL.
- The command to watch live: `gh run watch <id>`.
- Expected runtime (~20–45 min) and the destination
  (`research/generative/`). The runner pushes the commit, so the
  article shows up at https://ara.guzus.xyz/research/<slug>
  after the next Vercel deploy.

Then STOP. Do not run any research or write the article locally
in this session.

---

## PATH B — Run locally (deep pipeline, bridged from the workflow)

This path mirrors the workflow's depth contract — same evidence
packet schema, same verifier pass, same per-section structure —
adapted for in-chat execution. The defaults are slightly smaller
than the workflow (fewer sub-agents per wave, smaller word
target) because the chat session shares your local resources and
your time.

Read `ARA_DSL.md` at the repo root (the source language you'll
write) AND `COMPONENTS.md` (the visual primitives the DSL compiles
to). The compiler + writer reject unknown directives, unknown
classes, and unknown tags at commit time. The visual reference
article (slug: `components`) in the Research tab exercises every
primitive.

### Toolbelt

Beyond `Read` / `Write` / `WebSearch` / `WebFetch`, you have:

- `uv run python scripts/prior_context.py "<topic>"` — lists related
  past articles already in this repo (slug, title, file path).
  Run this FIRST so you don't redo their work.
- `uv run python scripts/research_search.py SOURCE "query"` —
  primary-source search. `SOURCE` = `arxiv` | `edgar` | `crossref`
  | `semanticscholar` | `github`. Use this BEFORE `WebSearch` when
  the topic clearly has academic / SEC / GitHub footprints.
- `curl -sL <url> -o /tmp/x.pdf && pdftotext /tmp/x.pdf - | head -c 60000`
  — read PDFs (10-Ks, S-1s, papers, whitepapers).
- `uv run python scripts/stock_prices.py <ticker[,ticker...]> --range 1y --interval 1mo --format kv`
  — fetches close-price time series from Yahoo Finance (yfinance
  handles auth; no API key). Stdout shows `x:` and `ticker_X:`
  rows ready to paste into the body of a
  `:::line-chart(title=..., y-unit=$)` block. Up to 4 tickers per
  chart.
- `uv run python scripts/compile_ara.py path.ara.md --out /tmp/x.html`
  — compile DSL source to the HTML fragment. Run this if you want
  to inspect the rendered HTML, but normally the check script
  below does it for you.
- `uv run python scripts/check_generative_research.py /tmp/gen-research.ara.md`
  — COMPILE-CHECK the article. Accepts `.ara.md` (compiles, then
  validates the resulting HTML) or `.html` (validates directly).
  Catches DSL grammar errors AND any ara-* class invented inside
  a `:::raw` block. Exit 0 = valid; exit 1 = errors with
  suggestions. Use this in a tight loop — see step 7.5.

### Process — non-negotiable, in order

**0. PLAN + PRIOR-COVERAGE CHECK.**

- Run `uv run python scripts/prior_context.py "<topic>"` and `Read` any
  high-overlap article files it returns. Note what's already
  covered so you don't duplicate.
- **Read `ARA_DSL.md` and `COMPONENTS.md` at repo root.** The
  compiler dispatches `:::directive` names against a fixed table
  (DSL grammar), and the writer ENFORCES an exact-match ara-*
  allowlist (for any HTML that ends up in a `:::raw` block).
  Invented directives or classes are REJECTED with suggestions.
  Also Read the visual reference article (slug: `components`) to
  see every primitive rendered.
- Internally draft (hold in context, don't save):
  - 8–14 specific answerable questions
  - For each question: what counts as PRIMARY evidence (paper,
    filing, IR page, spec, first-party blog)
  - 3–5 disconfirming questions ("what would falsify the popular
    narrative")
  - For each question, the likely DATA SHAPE (time series /
    distribution / ranking / comparison / ratio / chronology) so
    section writers can pick the right visualization primitive
    instead of defaulting to ara-table or prose.

**1. EVIDENCE COLLECTION IN WAVES.** Use the `Task` tool
(`subagent_type: general-purpose`) to dispatch sub-agents IN
WAVES OF NO MORE THAN 6 AT A TIME. After each wave completes,
dispatch the next. Total target: 12–24 sub-agents across 2–4
waves. Send each wave's dispatches in a single message so its
sub-agents run concurrently, then await results before the next
wave.

Each sub-agent prompt MUST:

- name a domain-expert framing (e.g. "you are a senior equity
  analyst", "chip architect", "monetary economist")
- instruct first-principles reasoning
- require WebSearch + WebFetch on PRIMARY sources
- tell the agent it CAN use `uv run python scripts/research_search.py
  SOURCE "query"` for arxiv/edgar/crossref/semanticscholar/github
- tell the agent it CAN use `curl + pdftotext` for PDF sources
- cap output at ~10 evidence packets

Sub-agents MUST return STRUCTURED EVIDENCE PACKETS, not prose
summaries. Each packet:

- `claim`: the factual assertion in one sentence
- `source_url`: URL the agent actually fetched
- `source_type`: `primary` | `secondary` | `commentary`
  - primary = SEC filing / company IR / academic paper / spec
    sheet / first-party docs
  - secondary = mainstream press citing primaries
  - commentary = blogs, opinion, sell-side notes
- `date`: YYYY-MM-DD when published or claim was made
- `figure`: the exact number, name, or date the claim turns on
- `excerpt`: verbatim quote, <40 words
- `confidence`: 1 (rumour) … 5 (multiple primary sources)
- `caveat`: what would weaken or contradict the claim
- `shape`: one of `single-fact`, `time-series`, `ranking`,
  `breakdown`, `paired-delta`, `cross-entity-categorical`,
  `pictogram`, `key-value`, `chronology`, `quote`. Tag the SHAPE
  OF THE DATA THIS CLAIM CAN COMPOSE INTO when combined with
  sibling packets — not the topic. The stitcher uses this in
  step 4 to route packets to the right viz directive instead of
  leaving every writer to recognize the shape from prose.

**2. BUILD A LEDGER** in your context. Dedupe by `source_url`.
Drop packets with `confidence < 2` unless they're the only signal
on a non-trivial question. Group packets by which planning
question they answer.

**3. SPOT-CHECK.** `WebFetch` or `curl+pdftotext` yourself on the
5–8 most load-bearing primary sources to confirm the headline
numbers exist on the pages agents cited.

**4. OUTLINE + BUCKET BY SHAPE.** Decide the article's 5–8
numbered `## ` sections with a one-line thesis per section. Map
ledger packets to sections (each packet routes to ≥1 section).
THEN, for each section, walk its packets and identify SHAPE
BUNDLES — groups of 2+ packets that share a `shape` and could
compose into one viz directive:

- 3+ `breakdown` packets summing to ~one whole → `:::donut`
- 3+ `ranking` packets, same metric → `:::rank-list`
- 3+ `time-series` points on same metric (or `stock_prices.py`
  output) → `:::line-chart`
- 5+ `time-series` points inline in prose → `{sparkline:...}`
- 1 `paired-delta` packet → `:::compare`
- 3+ `paired-delta` packets, same dimension → `:::slope`
- 2+ `cross-entity-categorical` packets with matching axes
  → `:::stack-rows`
- 3+ `key-value` packets, single subject → `:::kv`
- 1+ `chronology` packets, dated → `:::timeline`
- 1 `pictogram` packet (count of N identical units) → `:::iso`
- standalone `quote` packet → `:::quote`
- 4–8 `single-fact` packets that share a frame (e.g. headline
  KPIs for one company) → `:::stats`

Write this as a SECTION ROUTING TABLE before dispatching writers:

```
Section 02 (Speed as the moat):
  - :::stats     packets [4, 8, 11]   (headline KPIs)
  - :::line-chart packets [12, 14]    (BE close TTM)
  - :::compare   packets [9, 10]      (BE vs PJM lead time)
  - prose body   packets [5, 6, 7, 13, 15]
```

The point is to remove ALL viz-shape-recognition work from the
section writers — they get told what to emit for each bundle.

**4.5. SECTION WRITERS IN WAVES.** Use the `Task` tool to
dispatch ONE writer sub-agent per H3 section, IN WAVES OF NO MORE
THAN 3 AT A TIME (so 5–8 writers across 2–3 waves). Each writer
prompt MUST include:

- the full outline (so each writer knows what the OTHER sections
  cover and avoids duplication)
- this section's number, thesis, and the relevant subset of
  ledger packets
- **this section's SECTION ROUTING TABLE** — EXPLICIT
  instructions for what to emit. The writer FILLS IN the
  blocks; they do NOT decide which directive to use.
- the per-section contract (below)
- a 500–900-word target for THIS section
- the Component vocabulary block (below) AND an instruction to
  `Read ARA_DSL.md` and `COMPONENTS.md` first
- an EXPLICIT note that they CAN fetch live stock-price series
  via `uv run python scripts/stock_prices.py <ticker[s]> --range 1y
  --interval 1mo --format kv` (Yahoo Finance via yfinance, no
  API key, up to 4 tickers per chart). Stdout is ready to paste
  into the body of a `:::line-chart(title=..., y-unit=$)` block.

Each writer returns ONLY their section as DSL — start with
`## N. Section title` and emit paragraphs, `:::directives` (from
the routing table), blockquotes, etc. as documented in
ARA_DSL.md. NO frontmatter, NO `:::references` block, NO raw
HTML. You stitch.

**5. STITCH.** Compose the final `.ara.md` source:

- YAML frontmatter (`eyebrow`, `title`, `deck`, `lede`, optional
  `stats:` grid) wrapped in `---` fences
- assembled section writers' DSL output (in order)
- a "what could break the thesis" / counter-arguments `## `
  section (you write this yourself from the ledger)
- a final `:::references` block listing every cited source as
  `{id: N, title: ..., url: ..., source: ..., date: ...}`

Normalize voice in a quick pass. Every substantive factual claim
MUST be followed by a `[^N]` (or `[^1,2,3]` for multi-cite) where
N matches a matching `id:` in the `:::references` block. The
compiler renders `[^N]` as the ara-cite superscript — do NOT
write raw `<sup><a class="ara-cite">` HTML.

**6. VERIFIER PASS.** Use the `Task` tool to dispatch ONE more
sub-agent. Pass it the draft `.ara.md` body AND the
`:::references` block. Instruct it to:

- read every `[^N]` in the draft and pair it with the matching
  `:::references` entry
- fetch each cited URL (WebFetch or curl+pdftotext)
- emit a STRUCTURED findings table only (NOT a rewritten article):

  ```
  claim_id | section | support_status (supported | weak | unsupported)
           | cited_source | problem | required_fix
  ```

- additionally flag any factual claim WITHOUT a cite

**7. BOUNDED REVISION.** Address ONLY the verifier's findings.
Each unsupported claim must be either:

- (a) replaced with a supported variant from the ledger,
- (b) demoted by wrapping in `==unverified: ...==` (compiles to
  `<mark class="ara-mark">`), or
- (c) deleted.

Do NOT generically expand or pad. ONE revision pass maximum.

### Quality targets — these, not word count, are the bar

- Research questions answered: ≥ 80% of your plan
- Substantive factual claims with cite: ≥ 85%
- Primary-source share among cited sources: ≥ 50% (when primary
  sources exist for the topic)
- Evidence density: ≥ 10 cited claims per 1,000 words
- Quantitative density: ≥ 2 concrete numbers/dates/named entities
  per H3 numbered section
- Counter-argument: ≥ 1 serious counterclaim or "what would
  falsify this" per major thesis
- References: ≥ 15 distinct source URLs in the numbered
  references list
- **Visualization diversity: ≥ 2 distinct visualization primitives**
  across the article — pick from `ara-bars`, `ara-stack-bar`,
  `ara-stack-rows`, `ara-sparkline`, `ara-line-chart`, `ara-donut`,
  `ara-slope`, `ara-compare`, `ara-rank-list`, `ara-iso`,
  `ara-timeline`, `ara-kv`. (`ara-table` and `ara-callout` do NOT
  count — they're the safe defaults.)
- Word count: 3000–5000 as a GUARDRAIL only

### Component vocabulary (pick by data shape)

| Data shape | Use |
|---|---|
| Time series | `:::line-chart` (full SVG, up to 4 series) or inline `{sparkline:1,2,3}` |
| Distribution / breakdown | `:::donut`, `:::stack-bar(legend=true)`, or `:::stack-rows` |
| Ranking | `:::rank-list` (proportional fills built-in) |
| "Where X sits in the range" | `:::compare` (lowest / highest / subject cards) |
| Ratios | `:::iso` (pictogram), or `:::stats` with `unit:` on a big number |
| Before / after delta | `:::slope` (two-period) |
| Chronology | `:::timeline` |
| Key/value facts | `:::kv` |
| Single bars | `:::bars` |

Anti-patterns — REJECT in your own draft:

- "the top 5 are…" as a markdown list → use `:::rank-list`
- "the breakdown is X%/Y%/Z%" in prose → `:::donut` or `:::stack-bar`
- time series described in prose → embed `{sparkline:...}` or `:::line-chart`
- before/after numbers in prose → `:::slope`
- key facts as a markdown list → `:::kv`

### Per-section contract (replaces mechanical density rules)

Each `## ` numbered section must contain:

- 1 section-thesis sentence
- 3–5 sourced factual claims (each with `[^N]` cite)
- ≥ 1 quantitative datapoint where one exists
- ≥ 1 counterpoint or "what would weaken this" line
- 1 sentence on why this matters

If the data shape calls for a visualization (per the table above),
USE the matching `:::directive`. Do NOT default to a markdown
table or prose for visualizable data. Use `:::callout` sparingly:
thesis break, risk flag, or source caveat only.

### Validation (the compiler is the source of truth)

The compile pipeline enforces:

- Source is a valid `.ara.md`: YAML frontmatter with at least
  `title:`, then markdown body with `## ` headings and
  `:::directives` from the fixed grammar in `ARA_DSL.md`.
- The compiler dispatches `:::name(...)` against its fixed
  directive table; unknown names error with a list of valid
  directives.
- After compile, the writer's `validate_body` is the backstop:
  every `class=` token is an exact-match ara-* class documented
  in `COMPONENTS.md` (only relevant if you used `:::raw`),
  allowed tags only, no `style=` / `on*=` / `javascript:`, body
  under 200 KB.

You don't have to mentally validate the body. Write it, then run
the compile check below — it'll list every problem with a
suggested fix.

### Save and commit via the writer

**7.5. Compile-check the body, fix, re-check, loop until clean.**

```bash
# Write the body to /tmp/gen-research.ara.md via the Write tool,
# then compile-check it WITH design gates:
uv run python scripts/check_generative_research.py /tmp/gen-research.ara.md \
  --diversity-min 3 --callout-max 5 --strict-shape
# Exit 0 → safe to commit (proceed below). Soft warnings on
#          stderr are advisory.
# Exit 1 → stderr lists every DSL grammar error, invalid
#          class/tag, OR design-gate violation (fewer than 3
#          distinct viz primitives, more than 5 callouts).
#          Fix the body in place and re-run. Iterate.
```

Common design fixes when diversity gate fails:
- 4+ percentage shares of one whole in prose → `:::donut`
- "the top N are…" list → `:::rank-list`
- Paired before/after numbers → `:::compare` (one pair) or
  `:::slope` (3+ pairs)
- Chronology of dated events → `:::timeline`
- 4+ headline KPIs as separate sentences → `:::stats` grid

**8. Commit** via the writer (which re-compiles + re-validates as
defense in depth, then writes both the `.ara.md` source and the
compiled `.html` artifact + updates the index + makes a local
commit):

```bash
uv run python scripts/write_generative_research.py \
  --topic "<the exact topic the user gave>" \
  --model "claude-opus-4-7" \
  --source "local" \
  --kind fragment \
  --html-body /tmp/gen-research.ara.md
```

(The `--html-body` flag accepts either an `.ara.md` source or a
raw `.html` body — it auto-detects by extension. The writer will
compile and store both files when given DSL.)

If the writer prints a validation error (`unknown directive`,
`disallowed tag`, `non-ara-* classes`), fix the body and re-run.
Do **not** strip the validation — the design system is the point.

The writer prints the relative paths of the new files and the
index size on stdout, then commits locally. **Do not push** —
leave the commit for the user to review.

### Report back to the user (PATH B)

One short message containing:

- The article title.
- The file path the writer printed.
- A one-sentence note flagging anything left as `unverified` or
  any claim the user should spot-check before pushing.
