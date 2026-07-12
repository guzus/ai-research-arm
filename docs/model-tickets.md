# Model-release tickets

The hyperscaler model timeline is a **persistent set of tickets**, not a
daily-regenerated table. Each upcoming release, rumor, partnership, or
legal event is one ticket. The daily workflow (`24h-model-timeline.yml`)
runs an agent that **CRUDs** tickets — create new ones, update existing
ones, close resolved ones — based on the last 24 hours of signal.

Tickets live at `research/models/tickets/<slug>.md`. Each file is
markdown with a YAML frontmatter block defining the structured fields,
followed by a free-form body.

This doc is the **contract**: the CRUD agent reads it each run, and the
validator (`scripts/check_model_tickets.py`) enforces it. Keep it in
sync with the validator.

## File layout

```
research/models/
├── tickets/
│   ├── mythos-public-release.md
│   ├── gemini-3-2-flash.md
│   ├── opus-4-7.md
│   └── ...
├── 2026-05-13-timeline.md       # legacy daily table (frozen, kept for old links)
├── 2026-05-17-timeline.md       # legacy daily table (frozen)
└── 2026-05-19-timeline.md       # NEW format: daily diff summary derived from ticket changes
```

The pre-tickets `<date>-timeline.md` files (large markdown tables) stay
on disk so old dashboard URLs don't 404, but they are not updated.
New dates produce a *diff summary* instead — see "Daily diff" below.

## Frontmatter schema

```yaml
---
slug: mythos-public-release        # required, matches filename without .md
title: Claude Mythos full public release   # required, human-readable headline
company: Anthropic                 # required, free text (e.g. "Anthropic", "Google / DeepMind", "OpenAI / Codex")
model: Mythos                      # optional, the named model/product the ticket tracks; null for non-model events
status: in-testing                 # required, one of the 5 canonical states (see below)
status_note: |                     # optional, free text for the nuance the canonical state can't carry
  Multi-cloud gated preview (AWS GA May 11, GCP Vertex Private Preview May 16);
  no public release planned per kimmonismus.
expected: "TBD — voluntary CAISI partnership"   # optional, free text date / window / condition
labels:                            # optional, list of free-text tags
  - frontier-model
  - gated
  - multi-cloud
verification: confirmed            # required, one of: confirmed | partial | unverified
sources:                           # required, list of citations (URLs or @handles), >=1
  - https://red.anthropic.com/2026/mythos-preview/
  - "@scaling01"
  - "@kimmonismus"
polymarket:                        # optional, 1-3 Polymarket market mappings (see "Polymarket market mappings")
  - event_slug: mythos-released-by         # required, gamma event slug (polymarket.com/event/<event_slug>)
    market_id: "2850825"                   # required, gamma market id — quote it, must be a string
    token_id: "31380452762865791793..."    # required, CLOB YES-outcome token id — quote it, must be a string
    question: "Mythos released by Aug 31, 2026?"   # required, human question incl. the outcome
    outcome: "Aug 31 2026"                 # optional, short outcome label for the dashboard chip
created_at: 2026-04-15             # required, YYYY-MM-DD
updated_at: 2026-05-16             # required, YYYY-MM-DD (>= created_at)
closed_at: null                    # required, YYYY-MM-DD when status=closed, else null
closed_reason: null                # required, short reason when status=closed, else null
history:                           # required, append-only timeline of CRUD events
  - ts: 2026-04-15
    change: Created — initial leak of Mythos benchmark scores
  - ts: 2026-05-05
    change: "Pricing leak: $25/$125 per MTok"
  - ts: 2026-05-11
    change: AWS GA — confirms multi-cloud private preview pattern
  - ts: 2026-05-16
    change: GCP Vertex AI Private Preview confirmed via blog
---
```

After the closing `---`, the body is free-form markdown. Use it for the
"why this matters" narrative, deeper context, and any commentary that
doesn't fit a structured field. The body is what an analyst reads to
understand the ticket; the frontmatter is what filters and dashboards
read.

## Canonical lifecycle (5 states)

| State        | Meaning                                                                                  |
|--------------|------------------------------------------------------------------------------------------|
| `rumored`    | Speculation only — single-source tease, prediction, "Polymarket says...", no artifact   |
| `in-testing` | Real artifact exists: private preview, leak, internal usage, GCP/AWS console listing    |
| `confirmed`  | Official announcement, primary-source news, or multi-source corroboration               |
| `released`   | Publicly available right now (anyone can use it)                                        |
| `closed`     | Resolved — shipped & rolled into normal coverage, OR disproved, OR superseded            |

State transitions are monotonic except for `released → closed`:
```
  rumored → in-testing → confirmed → released → closed
                                      ↓
                                    closed (without released, if disproved/superseded)
```

If the underlying claim flips (e.g. "Gemini 3.5 expected" gets disproved
when Gemini 3.2 leaks), the old ticket closes with `closed_reason:
superseded-by:<other-slug>` and a new ticket carries the new shape.
Never rewrite history on the closed ticket.

Mapping from the legacy table's freeform statuses:

| Legacy status              | Canonical    |
|----------------------------|--------------|
| Rumored, Speculated, Predicted | `rumored`    |
| In Discussion, In Development, In Testing | `in-testing` |
| Confirmed, Announced, Reaffirmed, Reported | `confirmed`  |
| _(rolled out to users)_    | `released`   |
| _(shipped + ≥4 weeks old, OR disproved)_ | `closed`     |

The legacy status's nuance ("Confirmed event; tier now skewing to 3.2",
"In Testing — GCP console artifact") goes into `status_note`.

## Verification flag

The legacy table uses `⚠` / `🚩 Unverified — STILL NO PRIMARY CONFIRM N CYCLES`
for claims that haven't been primary-source corroborated. The new ticket
captures this in `verification`:

| Value         | Meaning                                                                     |
|---------------|-----------------------------------------------------------------------------|
| `confirmed`   | At least one primary source (company blog, official handle, court filing)   |
| `partial`     | Multiple secondary corroborations but no primary source yet                 |
| `unverified`  | Single-source tease, or a claim that hasn't been corroborated in ≥10 cycles |

If a ticket sits at `unverified` for more than ~15 daily cycles, the
CRUD agent may close it with `closed_reason: stale-rumor-unverified`.

## Polymarket market mappings (optional)

A ticket tracks a real-world event; a Polymarket market is the crowd's
live probability for that event. The optional `polymarket:` frontmatter
key binds the two so the dashboard's models tab can render live odds
(and their evolution) on the ticket card.

Shape — a list of 1–3 mappings, **most-relevant first** (the first
mapping is the primary one and gets the price-history sparkline):

| Field        | Required | Meaning                                                                    |
|--------------|----------|-----------------------------------------------------------------------------|
| `event_slug` | yes      | Gamma event slug — the page at `https://polymarket.com/event/<event_slug>`  |
| `market_id`  | yes      | Gamma market `id` inside that event (string — quote it in YAML)             |
| `token_id`   | yes      | CLOB token id of the **Yes** outcome (string — quote it; ~78 digits)        |
| `question`   | yes      | Human-readable market question including the outcome/date                   |
| `outcome`    | no       | Short outcome label for the chip, e.g. `"Dec 31 2026"`                       |

Validator rules (`scripts/check_model_tickets.py`): the key may be
omitted or `null`; when present it must be a list of 1–3 mappings; every
required field must be a non-empty **string** (`market_id` and
`token_id` must be quoted in YAML — an unquoted 78-digit token id parses
as a number and loses precision); no keys other than the five above are
allowed inside a mapping.

Maintenance protocol for the CRUD agent:

1. **Add** a mapping only when a clearly-matching **active** market
   exists — the market's resolution criteria must resolve on the same
   real-world event the ticket tracks (e.g. a "GPT-6 released by ..."
   market does NOT match a GPT-5.6 ticket; a "Grok 5" market that
   excludes Grok 4.x variants does NOT match a Grok 4.5 ticket). Find
   candidates via
   `https://gamma-api.polymarket.com/public-search?q=<terms>&events_status=active`,
   then read the event via
   `https://gamma-api.polymarket.com/events?slug=<event_slug>` and check
   the market's `description` text before mapping.
2. **Never invent IDs.** Only use `event_slug` / `market_id` /
   `token_id` values read from the Polymarket API response
   (`markets[].id` and the first element of the market's
   `clobTokenIds` JSON array = the Yes token). No recalled,
   pattern-matched, or guessed IDs.
3. **Keep mappings when markets resolve.** Final odds and the price
   history stay valuable on released/closed tickets — do not remove a
   mapping because the market closed.
4. **Max 3 mappings per ticket**, most-relevant first. Prefer one
   near-term date market plus (optionally) a longer-dated one from the
   same event.

Adding, correcting, or pruning a mapping is a ticket UPDATE: bump
`updated_at` and append a `history` entry describing the change.

## Slug conventions

- Lowercase ASCII, hyphen-separated, no underscores
- Format: `<company>-<artifact>-<distinguisher>`, e.g. `gemini-3-2-flash`,
  `anthropic-30b-series-f`, `openai-apple-legal-action`
- Stable for the lifetime of the ticket. The agent **must not** rename
  slugs. If a name changes (e.g. "Gemini 3.5" turns out to be "Gemini 3.2"),
  keep the original slug and update `title` + add a history entry.
- Version numbers in slugs use hyphen-separated digits: `opus-4-7` not
  `opus-4.7` (dots cause filesystem ambiguity).
- For news/event tickets without a named artifact, use
  `<company>-<short-noun>-<yyyy-mm>`, e.g.
  `anthropic-stainless-acquisition-2026-05`.

## CRUD dedup protocol

This section is the **contract the CRUD agent must follow**. Quote it
in the workflow prompt verbatim.

On each daily run, for each candidate event surfaced in the last 24h of
signal:

1. **List existing tickets** by reading `research/models/tickets/*.md`.
   Build a map of `{ company, model, status }` → slug.

2. **Match the candidate** against existing tickets. The agent must
   answer: "Is this signal about the same *shipping artifact* as an
   existing ticket?" Same shipping artifact means:
   - Same model name (allowing for version-number drift, e.g. "Gemini
     3.5" vs "Gemini 3.2 Flash" — see #4), AND
   - Same release event (a single product reveal, single partnership
     announcement, single funding round)

3. **If matched**:
   - If the existing ticket is **not closed**: update it. Add a `history`
     entry summarizing what changed. Update `status` if the lifecycle
     advanced. Update `status_note`, `expected`, `sources` as needed.
     Bump `updated_at`. Do NOT touch `created_at`, `slug`, or
     re-write earlier `history` entries.
   - If the existing ticket **is closed**: leave it alone. If the new
     signal contradicts the closure (e.g. a disproved rumor is now
     real), create a NEW ticket with `created_at = today` whose body
     references the closed ticket by slug.

4. **If no match**: create a new ticket. Pick a slug per conventions.
   Set `created_at = updated_at = today`, `status` per the strongest
   evidence (default `rumored` for single-source teases),
   `verification` honestly. Seed `history` with one entry: `Created`.

5. **Close** any ticket that meets one of:
   - Has shipped publicly ≥4 weeks ago AND is in `released` state
     (transition to `closed` with `closed_reason: released-and-aged`)
   - Has been `unverified` for ≥15 daily cycles with no new
     corroboration (`closed_reason: stale-rumor-unverified`)
   - Is contradicted by today's signal AND there's a successor ticket
     (`closed_reason: superseded-by:<successor-slug>`)

6. **Never delete**. Closing preserves history; deletion does not.

7. **Polymarket mappings** follow the "Polymarket market mappings"
   section above: add one only when a clearly-matching active market
   exists, keep mappings after markets resolve, never invent IDs (only
   IDs read from the Polymarket API), max 3 per ticket.

## Daily diff

The CRUD agent produces a derived markdown file at
`research/models/<date>-timeline.md` summarizing what changed that day.
This keeps the existing dashboard URL pattern (`/models/YYYY-MM-DD`)
working without modification. Shape:

```markdown
# Model Timeline — Diff for 2026-05-19

## 🆕 Created (3)
- `gemini-3-2-flash` — Google / DeepMind — In Testing — GCP console artifact
  ([ticket](/tickets/gemini-3-2-flash))
- ...

## 🔄 Updated (5)
- `mythos-public-release` — Anthropic — status: in-testing (unchanged)
  - GCP Vertex AI Private Preview confirmed via blog
  - ([ticket](/tickets/mythos-public-release))
- ...

## ✅ Closed (1)
- `gemini-3-5-expected` — superseded by `gemini-3-2-flash`
- ...

## 🌐 No change today (32)
_(collapsed list of slugs)_
```

The dashboard's date tab renders this markdown. The "tickets" tab
renders the card grid from `index.json` directly.

## Validator

`scripts/check_model_tickets.py` enforces this schema. Run with no args
to validate every ticket in `research/models/tickets/`. Exit 0 on
success, exit 1 on any failure with line numbers and reasons.

The CRUD agent must re-run the validator at the end of every daily run.
If it fails, the agent fixes the offending ticket in-place and re-runs.
The workflow commits only when validator is clean.
