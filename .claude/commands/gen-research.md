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
  `backend=claude`. Your chat is freed instantly. The runner
  produces a longer article (4500–7000 words target, ≥20 cited
  references) and pushes the commit directly to `main`.
  Recommended for substantive topics where you want maximum depth
  without spending in-chat time.

After the user picks:

- **Route** → follow PATH A below.
- **Run locally** → follow PATH B below.

---

## PATH A — Route to the GitHub workflow

Dispatch the workflow with the user's topic. Use `claude` as the
backend unless the user explicitly asked for `deepseek` in their
brief.

```bash
gh workflow run generative-research.yml \
  -f topic="<the exact topic the user gave>" \
  -f backend=claude
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

Read `COMPONENTS.md` at the repo root before writing. The writer
parses the body at commit time and rejects unknown classes or
tags. The visual reference article (slug: `components`) in the
Research tab exercises every primitive.

### Toolbelt

Beyond `Read` / `Write` / `WebSearch` / `WebFetch`, you have:

- `python3 scripts/prior_context.py "<topic>"` — lists related
  past articles already in this repo (slug, title, file path).
  Run this FIRST so you don't redo their work.
- `python3 scripts/research_search.py SOURCE "query"` —
  primary-source search. `SOURCE` = `arxiv` | `edgar` | `crossref`
  | `semanticscholar` | `github`. Use this BEFORE `WebSearch` when
  the topic clearly has academic / SEC / GitHub footprints.
- `curl -sL <url> -o /tmp/x.pdf && pdftotext /tmp/x.pdf - | head -c 60000`
  — read PDFs (10-Ks, S-1s, papers, whitepapers).
- `python3 scripts/stock_prices.py <ticker[,ticker...]> --range 1y --interval 1mo --format kv`
  — fetches close-price time series from Yahoo Finance (no API
  key). Output is plain text designed to paste directly into
  `ara-line-chart` data attributes, or use `--format html` to get
  a ready-made `<div class="ara-line-chart" ...>` element. Use
  for any equity-bearing topic. Up to 4 tickers per chart.
- `python3 scripts/check_generative_research.py /tmp/gen-research-body.html`
  — COMPILE-CHECK the article body. Runs the same validation rules
  the writer enforces (tag allowlist, ara-* class exact-match
  against COMPONENTS.md, size cap, etc.). Exit 0 = valid; exit 1 =
  errors printed to stderr with suggestions. Use this loop after
  writing the body and before committing — see step 7.5.

### Process — non-negotiable, in order

**0. PLAN + PRIOR-COVERAGE CHECK.**

- Run `python3 scripts/prior_context.py "<topic>"` and `Read` any
  high-overlap article files it returns. Note what's already
  covered so you don't duplicate.
- **Read `COMPONENTS.md` at repo root** for the canonical ara-*
  class vocabulary. The writer ENFORCES an exact-match allowlist
  parsed from COMPONENTS.md — invented classes (ara-references,
  ara-stat-num, ara-link, ara-ref-link, etc.) are REJECTED with
  suggestions. Also Read the visual reference article (slug:
  `components`) to see every primitive in use.
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
- tell the agent it CAN use `python3 scripts/research_search.py
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

**2. BUILD A LEDGER** in your context. Dedupe by `source_url`.
Drop packets with `confidence < 2` unless they're the only signal
on a non-trivial question. Group packets by which planning
question they answer.

**3. SPOT-CHECK.** `WebFetch` or `curl+pdftotext` yourself on the
5–8 most load-bearing primary sources to confirm the headline
numbers exist on the pages agents cited.

**4. OUTLINE.** Decide the article's 5–8 numbered H3 sections
with a one-line thesis per section. Map ledger packets to
sections (each packet routes to ≥1 section).

**4.5. SECTION WRITERS IN WAVES.** Use the `Task` tool to
dispatch ONE writer sub-agent per H3 section, IN WAVES OF NO MORE
THAN 3 AT A TIME (so 5–8 writers across 2–3 waves). Each writer
prompt MUST include:

- the full outline (so each writer knows what the OTHER sections
  cover and avoids duplication)
- this section's number, thesis, and the relevant subset of
  ledger packets
- the per-section contract (below)
- a 500–900-word target for THIS section
- the strict tag/class validation rules (below)
- the Component vocabulary block (below) AND an instruction to
  `Read COMPONENTS.md` first
- the DATA SHAPE of the packets (time series / distribution /
  ranking / comparison / ratio / chronology) plus an EXPLICIT
  instruction to use the matching ara-* visualization primitive,
  NOT default to ara-table or prose. Ranking → ara-rank-list,
  % breakdown → ara-donut / ara-stack-bar, time series →
  ara-line-chart / ara-sparkline, before/after → ara-slope,
  chronology → ara-timeline, key facts → ara-kv.

Each writer returns ONLY the HTML for their section (an
`<h3 class="ara-h2">` + section body, no `<article>` wrapper, no
references list). You stitch.

**5. STITCH.** Compose the final ONE `<article class="ara-doc">`
HTML fragment:

- header block: `ara-eyebrow` + `ara-display` + `ara-deck` +
  `ara-lede` + `ara-stats`
- assembled section writers' output (in order)
- a "what could break the thesis" / counter-arguments section
  (you write this yourself from the ledger)
- a references list at the bottom

Normalize voice in a quick pass. Every substantive factual claim
MUST be followed by a numbered
`<sup><a class="ara-cite" href="#ref-N">N</a></sup>` pointing to
the packet's `source_url`, with `<li id="ref-N">…</li>` in the
references list.

**6. VERIFIER PASS.** Use the `Task` tool to dispatch ONE more
sub-agent. Pass it the draft article body. Instruct it to:

- read every numbered `ara-cite` in the draft
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
- (b) demoted to `<mark class="ara-mark">unverified: …</mark>`, or
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
| Time series | `ara-line-chart` (full SVG, up to 4 series) or `ara-sparkline` (inline) |
| Distribution / breakdown | `ara-donut`, `ara-stack-bar` (+ `ara-stack-legend`), or `ara-stack-rows` |
| Ranking | `ara-rank-list` (proportional fills built-in) |
| "Where X sits in the range" | `ara-compare` (lowest / highest / subject cards) |
| Ratios | `ara-iso` (pictogram), `ara-stat` + `ara-stat-unit` |
| Before / after delta | `ara-slope` (two-period) |
| Chronology | `ara-timeline` |
| Key/value facts | `ara-kv` |
| Single bars | `ara-bars` / `ara-bar` |

Anti-patterns — REJECT in your own draft:

- "the top 5 are…" as `<ul>` → use `ara-rank-list`
- "the breakdown is X%/Y%/Z%" in prose → `ara-donut` or `ara-stack-bar`
- time series described in prose → embed `ara-sparkline` or use `ara-line-chart`
- before/after numbers in prose → `ara-slope`
- key facts as `<ul>` → `ara-kv`

### Per-section contract (replaces mechanical density rules)

Each H3 numbered section must contain:

- 1 section-thesis sentence
- 3–5 sourced factual claims (each with numbered cite)
- ≥ 1 quantitative datapoint where one exists
- ≥ 1 counterpoint or "what would weaken this" line
- 1 sentence on why this matters

If the data shape calls for a visualization (per the table above),
USE the matching ara-* primitive. Do NOT default to `ara-table` or
prose for visualizable data. Use `ara-callout` sparingly: thesis
break, risk flag, or source caveat only.

### Validation (the compiler is the source of truth)

The writer enforces:

- Root `<article class="ara-doc">`.
- Every `class=` token is an exact-match ara-* class documented
  in `COMPONENTS.md` (or a modifier like `ara-callout--info` of a
  documented base).
- Allowed tags: `article, section, div, header, footer, h2, h3,
  h4, p, span, em, strong, code, mark, sup, sub, abbr, time, ul,
  ol, li, dl, dt, dd, a, img, figure, figcaption, table, thead,
  tbody, tr, th, td, blockquote, pre, br, hr`.
- No `<h1>`, `<style>`, `<script>`, `<iframe>`, `<head>`, `<body>`.
- No inline `style=`, no `on*=` handlers, no `javascript:`.
- Body under 200 KB.

You don't have to mentally validate the body. Write it, then run
the compile check below — it'll list every problem with a
suggested fix.

### Save and commit via the writer

**7.5. Compile-check the body, fix, re-check, loop until clean.**

```bash
# Write the body to /tmp/gen-research-body.html via the Write tool,
# then compile-check it:
python3 scripts/check_generative_research.py /tmp/gen-research-body.html
# Exit 0 → safe to commit (proceed below).
# Exit 1 → stderr lists every invalid class/tag with suggestions.
#          Fix the body in place and re-run the check. Iterate.
```

**8. Commit** via the writer (which re-runs the same validation as
defense in depth, then writes the file + updates the index + makes
a local commit):

```bash
python3 scripts/write_generative_research.py \
  --topic "<the exact topic the user gave>" \
  --model "claude-opus-4-7" \
  --source "local" \
  --kind fragment \
  --html-body /tmp/gen-research-body.html
```

If the writer prints a validation error (`disallowed tag`,
`non-ara-* classes`), fix the body and re-run. Do **not** strip
the validation — the design system is the point.

The writer prints the relative path of the new file and the index
size on stdout, then commits locally. **Do not push** — leave the
commit for the user to review.

### Report back to the user (PATH B)

One short message containing:

- The article title.
- The file path the writer printed.
- A one-sentence note flagging anything left as `unverified` or
  any claim the user should spot-check before pushing.
