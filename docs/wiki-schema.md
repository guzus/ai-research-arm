# LLM Wiki schema

The LLM Wiki is a **compounding, interlinked knowledge base** at
`research/wiki/`, not a daily-regenerated digest. It is a persistent set of
markdown pages — one per entity, concept, or theme — that a daily Claude agent
**maintains** by ingesting ARA's *curated* synthesis (the daily digest and the
model-release tickets), **not** the raw firehose. Each page accretes detail and
cross-links over time; pages are updated and interlinked, rarely deleted.

This doc is the **contract**: the maintenance agent reads it each run, and the
validator (`scripts/check_wiki.py`) enforces it. Keep this doc and the validator
in lockstep — every field and rule described here is checked there, and vice
versa.

> **Scope note.** This doc defines the *data contract* only. How the wiki
> renders as a static page in the dashboard is a separate concern owned by the
> dashboard lane and is deliberately out of scope here. Nothing in this schema
> depends on the rendering.

## File layout

```
research/wiki/
├── index.md                 # catalog of every page, grouped by type (agent-maintained)
├── index.json               # GENERATED machine index for the dashboard (do not hand-edit)
├── log.md                   # append-only operations log
├── entities/
│   ├── nebius.md
│   ├── anthropic.md
│   └── ...
├── concepts/
│   └── neocloud.md
└── themes/
    └── ai-capex.md
```

`research/wiki/` contains **only** `index.md`, `index.json`, `log.md`, and the
three subdirectories `entities/`, `concepts/`, `themes/`. The schema itself
lives in `docs/` (this file), not under `research/wiki/`. Each page file is
markdown with a YAML frontmatter block defining the structured fields, followed
by a non-empty free-form body.

`index.json` is a **generated artifact**, not hand-authored: `scripts/build_wiki_index.py`
rebuilds it from the pages (page metadata, the slug∪alias resolver, the backlink
graph, and recent log entries) and the dashboard reads it directly. It is
committed so the dashboard build (`dashboard/scripts/prebuild.mjs`) just copies
it — no page parsing happens in the browser or at Vercel build time. Regenerate
it whenever pages change (`uv run python scripts/build_wiki_index.py`); CI's
`build_wiki_index.py --check` fails the build if it is stale. `check_wiki.py`
ignores `index.json` (it only globs the page subdirs).

## Frontmatter schema

Every page begins with a YAML frontmatter block. Field names and types are the
contract — match them exactly.

```yaml
---
slug: nebius                       # required; matches filename without .md; ^[a-z0-9]+(-[a-z0-9]+)*$
title: Nebius Group                # required; human-readable display name
type: entity                       # required; one of: entity | concept | theme
aliases: [Nebius, NBIS, "Nebius Group N.V."]   # optional; list of strings (other names this page answers to)
tags: [neocloud, gpu-cloud, ai-infrastructure] # optional; list of strings (free-text facets)
summary: Amsterdam-based AI cloud ("neocloud") provider spun out of Yandex.  # required; ONE line
created_at: 2026-05-24             # required; YYYY-MM-DD (ISO date)
updated_at: 2026-05-24             # required; YYYY-MM-DD (>= created_at)
sources:                           # optional; list of mappings, each with a title (req)
  - {title: "ARA daily digest 2026-05-24", path: research/digest/2026-05-24-digest.md}
  - {title: "Nebius Q1 2026 results", url: "https://example.com/nebius-q1", date: 2026-05-20}
---

Body in markdown — non-empty. See "[[link]] convention" below.
```

Field reference:

| Field | Req? | Type | Notes |
|---|---|---|---|
| `slug` | yes | string | Lowercase kebab; matches the filename stem; unique across **all** subdirs. |
| `title` | yes | string | Human-readable display name. |
| `type` | yes | enum | `entity` \| `concept` \| `theme`. Must match the subdir (see taxonomy). |
| `aliases` | no | list[str] | Alternate names. **Each alias joins the wikilink resolver namespace** (see slug rules). |
| `tags` | no | list[str] | Free-text facets used by search/lint. |
| `summary` | yes | string | A single line (no embedded newlines). |
| `created_at` | yes | date | ISO `YYYY-MM-DD`. |
| `updated_at` | yes | date | ISO `YYYY-MM-DD`; must be `>= created_at`. |
| `sources` | no | list[map] | Each item is a mapping with `title` (req) and optional `url` (http(s)), `path` (repo-relative), `date` (ISO). No other keys. |

Both flow style (`aliases: [a, b]`, `sources: - {title: ...}`) and block style
parse identically under `yaml.safe_load`; either is accepted.

After the closing `---`, the body is free-form markdown and **must be
non-empty**. Use it for the narrative, "why it matters", open questions, and
inline citations. The body is what an analyst reads; the frontmatter is what
search, lint, and the dashboard read.

## Type taxonomy

Three types, three subdirectories. The `type` field **must** match the subdir
the file lives in.

| Type | Subdir | What goes here |
|---|---|---|
| `entity` | `entities/` | Companies, orgs, products, models, people — concrete named things. E.g. Nebius, Anthropic, Gemini 3.5 Flash. |
| `concept` | `concepts/` | Techniques, ideas, mechanisms, business models. E.g. neocloud, mixture-of-experts, take-or-pay financing. |
| `theme` | `themes/` | Cross-cutting narratives that tie entities and concepts together. E.g. the AI capex supercycle, the open-weights wave. |

Rule of thumb: if you could point at it (a company, a model, a person) it's an
**entity**; if it's a way of doing something it's a **concept**; if it's a story
running across many entities/concepts over time it's a **theme**.

## Slug rules

- Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$` — lowercase ASCII alphanumerics,
  hyphen-separated, no underscores, no leading/trailing/double hyphens.
- The **filename stem equals the slug**: a page with `slug: nebius` is
  `entities/nebius.md`.
- Slugs are **globally unique across all three subdirs** — never two pages with
  the same slug, even in different subdirs.
- Version numbers use hyphen-separated digits: `gemini-3-5-flash`, not
  `gemini-3.5-flash` (dots cause filesystem ambiguity).
- **The resolver namespace is slugs ∪ aliases.** A `[[link]]` resolves if its
  target matches a page's slug *or* one of its aliases. Therefore aliases must
  not collide: an alias may not equal another page's slug, nor another page's
  alias. The validator builds one resolver map and hard-fails on any collision.
  Resolution is case-insensitive for aliases (slugs are already lowercase), so
  an alias `NBIS` is reachable as `[[nbis]]`, `[[NBIS]]`, etc.
- Slugs should be stable across a page's lifetime; if a thing is renamed, prefer
  updating `title` and adding the old name to `aliases` over re-slugging.

## `[[link]]` convention

Pages interlink with wikilinks:

```
[[slug]]                 # link by slug, label = slug
[[slug|Display Label]]   # link by slug, custom label
[[An Alias]]             # link by alias (resolves to the owning page's slug)
```

Rules:

- The target (text before an optional `|`) must resolve to a page **slug or
  alias**. Unresolved targets are a hard validation failure.
- **Links inside fenced code blocks are NOT links.** The validator strips
  ```` ``` ````- and `~~~`-fenced blocks before scanning, so documentation
  examples that contain `[[bracket-text]]` do not register. (Inline
  single-backtick spans are a known v1 limitation — keep example links in
  fences.)
- Cross-link generously: a good page links the entities, concepts, and themes
  it touches. The lint mode surfaces orphans (no inbound links) and missing
  reciprocal links as advisories.

## `index.md` format

`research/wiki/index.md` is the catalog. Shape:

```
# Wiki Index

## Entities
- [[slug]] — one-line summary
- ...

## Concepts
- [[slug]] — one-line summary

## Themes
- [[slug]] — one-line summary
```

- First line must be exactly `# Wiki Index`.
- One `##` section per type (`Entities` / `Concepts` / `Themes`).
- Each catalog line is `- [[slug]] — one-line summary` (em dash `—`).
- **Every page must be listed exactly once**, under the section matching its
  `type`. **Every listed slug must have a page file.** The validator checks both
  directions and the section↔type match.

## `log.md` format

`research/wiki/log.md` is an append-only operations log. Each entry:

```
## [YYYY-MM-DD] <op> | <summary>
```

- `op` ∈ `{seed, ingest, query, lint}`:
  - `seed` — initial creation of pages.
  - `ingest` — a daily maintenance pass that created/updated pages from new
    digest + ticket signal.
  - `query` — a recorded search/lookup against the wiki.
  - `lint` — a recorded advisory lint pass.
- Dates are **non-decreasing top→bottom** (append newest at the bottom).
- The summary (after `|`) must be non-empty.
- Prose/headings between entries are allowed; only `## ` lines are validated.

## INGEST / DEDUP PROTOCOL

This section is the **contract the daily maintenance agent must follow**. The
workflow prompt will tell the agent to read and follow it verbatim. The agent
ingests ARA's **curated** synthesis only — the daily digest
(`research/digest/<date>-digest.md`) and the model tickets
(`research/models/tickets/*.md`) — never the raw per-source firehose.

On each daily run:

1. **Load the current wiki.** Read `research/wiki/index.md` and every page under
   `entities/`, `concepts/`, `themes/`. Build a map of
   `{slug, aliases} → page` so you can match new signal against existing pages.

2. **Read today's curated input.** Read the latest daily digest and the current
   set of model tickets. Extract the salient *named things* (entities), *ideas*
   (concepts), and *narratives* (themes) worth tracking. Ignore one-off noise
   that won't compound.

3. **Match each candidate against existing pages.** Ask: "Does a page already
   exist for this thing?" A match means the candidate is the **same entity /
   concept / theme** as an existing page — check the candidate's name and known
   aliases against every page's `slug` and `aliases`. Account for renames and
   version drift (e.g. a model that shipped under a different version number than
   it leaked under): match on identity, not on the exact string.

4. **If matched → UPDATE the page.**
   - Add or refine body content with the new, source-cited detail.
   - Add any new alternate names to `aliases` (this keeps future matching and
     wikilink resolution working).
   - Add new citations to `sources`.
   - Add new cross-links (`[[...]]`) to other pages the update touches.
   - Bump `updated_at` to today. **Do not** change `slug` or `created_at`.

5. **If no match → CREATE a page.**
   - Choose the correct `type` and put the file in the matching subdir.
   - Pick a slug per the slug rules; ensure it is unique across all subdirs and
     that its aliases don't collide with any existing slug or alias.
   - Set `created_at = updated_at = today`.
   - Write a non-empty body with at least the "why it matters" framing and
     source citations, and cross-link it to related pages.
   - Add it to `index.md` under the right section.

6. **Cross-link, don't silo.** When you create or update a page, link the
   entities/concepts/themes it references. A new entity should usually link the
   concept(s) that explain it and the theme(s) it belongs to, and those pages
   should gain a reciprocal link. Use the lint mode to find gaps.

7. **Update `index.md` and append to `log.md`.** Reflect every create in
   `index.md`. Append one `ingest` line to `log.md` summarizing the pass
   (what was created/updated), dated today.

8. **Never silently delete.** Pages compound. If something is genuinely
   obsolete, prefer noting that in its body over deleting the file (deletion
   loses the accreted history and breaks inbound links).

9. **Validate before finishing.** Run `scripts/check_wiki.py`. If it fails, fix
   the offending page(s) in place and re-run until clean. The workflow commits
   only when the validator is clean.

## Lint checklist

`scripts/check_wiki.py --lint` is **advisory** — it prints warnings and
**always exits 0**. It surfaces:

- **Orphans** — pages with no inbound links from any other page. Candidates for
  better cross-linking.
- **Stale pages** — `updated_at` older than ~30 days. Candidates for a refresh
  pass.
- **Missing reciprocal links** — page A links B but B does not link back to A.
  Often a cheap, high-value link to add.

Lint never blocks. It is guidance for the maintenance agent to improve graph
connectivity and freshness over time.

## Validator

`scripts/check_wiki.py` enforces this schema. Run with no args to validate every
page in `research/wiki/{entities,concepts,themes}/` plus `index.md`/`log.md`
consistency. Exit 0 on success, exit 1 on any failure with `FAIL <relpath>:
<field>: <msg>` lines.

Hard-fail checks:

- Frontmatter schema: required fields present and correctly typed; `sources`
  mappings well-formed; `summary` single-line.
- Slug: matches the pattern, equals the filename stem, globally unique; aliases
  don't collide (the resolver namespace is slugs ∪ aliases).
- `type`: in the enum and matching the subdir.
- Dates: ISO `YYYY-MM-DD`; `updated_at >= created_at`.
- Body: non-empty.
- Wikilinks: every `[[target]]` (outside fenced code) resolves to a slug or
  alias.
- `index.md` ↔ pages: every page listed once under the right section; every
  listed slug has a file.
- `log.md`: every `## ` entry matches `## [YYYY-MM-DD] <op> | <summary>` with a
  canonical op and non-decreasing dates.

Flags:

- `--root <dir>` — point the validator at an alternate wiki root (used by tests
  for tmp-dir isolation; defaults to `research/wiki`).
- `--lint` — advisory mode (see Lint checklist); always exits 0.

The maintenance agent must re-run the validator at the end of every run and fix
any failure in place before the workflow commits.
