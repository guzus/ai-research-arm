# Claim store contract

The cross-article claim store turns the per-article methodology sidecars into
a queryable, compounding asset. It is the claim-level analogue of the wiki:
**accumulate and reuse, don't regenerate** (load-bearing rule 10).

| Piece | What it is |
|---|---|
| `research/generative/<stem>.claims.json` | The per-run ledger. Written by the generative-research agent, schema-gated by `scripts/generative_methodology.py`. **The source of truth.** |
| `scripts/build_claim_index.py` | Walks every ledger, joins article metadata, emits the index. `--check` is a CI drift gate. |
| `research/claims/index.json` | The generated, committed index. Pure function of the ledgers — no timestamps. |
| `scripts/claim_search.py` | The read side. BM25 search, host/URL lookup, and contradiction **candidate** shortlisting. |

## Why it exists

Every generative-research run verified claims against primary sources, wrote
them to disk with tiers/dates/confidence — and then nothing read them back.
Each new article re-derived the same facts from zero, and could contradict a
prior article without anyone noticing. At the time this shipped there were
**1,312 verified claims across 46 articles** sitting unused.

## The reuse contract — the load-bearing part

A store whose selling point is *"reuse instead of re-verify"* is also, by
construction, a machine for laundering stale numbers: it hands back a
six-month-old figure carrying the authority of "already verified". So reuse
is **conservative and explicit**.

Every record carries `reusable: bool` and, when false, a `reuse_block` reason:

| `reuse_block` | Meaning | What the agent must do |
|---|---|---|
| *(none, `reusable: true`)* | `risk: stable`, has `as_of`, not low-confidence | May cite directly. **`as_of` travels with the claim** into the new article. |
| `volatile` | TVL, price, share, ranking — moves | Re-verify against a live source |
| `contested` | Sources disagreed when it was written | Re-verify **and** carry the disagreement forward |
| `single-source` | Only one source supported it | Seek corroboration before restating |
| `no-as-of` | Undated, so unfalsifiable as of when | Re-verify and date it |
| `low-confidence` | The author flagged it weak | Treat as a lead, not evidence |

**`reusable` is not advisory.** A hit with `reusable: false` must be
re-verified before it is restated. `claim_search.py --reusable-only` returns
just the safe set.

## The candidate contract — shortlists, never verdicts

`claim_search.py --candidates "<claim you are about to write>"` shortlists
prior claims that **overlap strongly in wording AND carry a differing figure
of the same unit**. That is a deterministic heuristic. It is **not**
contradiction detection.

Two claims can differ numerically and both be true — different period, scope,
entity, or restatement basis. The agent adjudicates against the sources. This
is the same split already used for headline dedupe
(`dedupe_headline_alerts.py` shortlists → `headline_judge.py` adjudicates).

A false *"we contradicted ourselves"* is worse than silence: it invites
rewriting a correct claim to resolve a conflict that never existed. Two
guards keep precision up:

- **Numbers are matched, not cross-produced.** Each query figure is paired
  with an equal (within 2%) stored figure of the same unit and consumed. Only
  *unpaired* figures count as disagreement. Without this, an identical
  sentence "contradicts itself" — the 65% pairing against the 68% of a
  different quantity. Regression-tested in `test_claim_store.py`.
- **Units never cross.** Percent, bps, currency and bare counts are separate
  namespaces, so `50%` can never be compared against `$50 billion`.

## Seam with derived claims — cross-article inputs are OUT OF SCOPE in v1

`--audit-derived-claims` rule **R2** requires every `inputs[].ref` to resolve
to another claim **in the same ledger**. A stored claim from a *previous*
article therefore **cannot** be used as a derived-claim input today: R2 will
reject it.

This is deliberate for v1, not an oversight. Recomputation is only meaningful
if the validator can see the input's value and support status at audit time,
and a cross-article input would have to be resolved and re-validated against
a store that may have changed since. The supported pattern is:

> Reuse the prior claim's **value and source** by restating it as a normal
> claim in the new ledger (citing the same source, carrying its `as_of`),
> then reference *that* entry as the derived input.

If cross-ledger inputs are ever wanted, R2 needs an explicit extension and
`docs/claim-store.md` plus the R1–R7 contract must move in lockstep.

## Index schema

```jsonc
{
  "schema_version": 1,
  "article_count": 46,
  "claim_count": 1312,
  "reusable_count": 615,
  "articles": [{ "stem", "slug", "title", "created_at", "tags", "claim_count" }],
  "claims": [{
    "key": "<article-stem>#<claim-id>",  // ids are unique only WITHIN a ledger
    "article", "article_title", "article_created_at", "id",
    "claim", "type", "source_urls", "source_tiers", "hosts",
    "as_of", "confidence", "risk",
    "reusable": true,
    "reuse_block": null
    // NOTE: figures are NOT stored. They are a pure function of `claim`
    // (extract_numerics) and claim_search recomputes them per query, so the
    // index carries no derivable data with a second chance to drift.
  }],
  "by_host": { "sec.gov": ["<key>", ...] },
  "by_url":  { "https://…": ["<key>", ...] }
}
```

Claim `id`s (`c1`, `c2`, …) repeat across articles, so the global key is
**composite**: `<article-stem>#<claim-id>`.

## CLI

```bash
uv run python scripts/build_claim_index.py            # rebuild
uv run python scripts/build_claim_index.py --check    # CI drift gate

uv run python scripts/claim_search.py "hyperscaler capex" --top 5
uv run python scripts/claim_search.py "tsmc capex" --reusable-only --json
uv run python scripts/claim_search.py --host sec.gov
uv run python scripts/claim_search.py --url https://www.sec.gov/Archives/…
uv run python scripts/claim_search.py "<claim draft>" --candidates
```

## Invariants

1. **The index is generated, never hand-edited.** `--check` fails CI on drift;
   rebuild instead of patching.
2. **Ledgers are the source of truth.** The index is derivable from them and
   can be deleted and rebuilt at any time.
3. **Deterministic output** — sorted throughout, no timestamps, so `--check`
   is a real gate rather than a clock.
4. **Atomic writes** (rule 8): temp file in the same directory + `os.replace`.
5. **Not shipped to the dashboard.** `research/claims/` is deliberately absent
   from `COPY_DIRS` in `prebuild.mjs` and from the `.dockerignore` allowlist —
   it is agent-facing tooling read from the runner's checkout. Adding a
   dashboard surface means updating **both** lists (enforced by
   `test_dockerignore_research_dirs.py`).
