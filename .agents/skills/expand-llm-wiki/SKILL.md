---
name: expand-llm-wiki
description: Expand and maintain the ARA LLM Wiki at `research/wiki/`. Use when Codex is asked to backfill, flourish, grow, ingest into, clean up, or improve the LLM wiki knowledge base; create or update entity/concept/theme pages; add OKF-native wiki content; reconcile new daily digests or model tickets into wiki pages; improve wiki cross-links, aliases, sources, index.md, log.md, or generated index.json.
---

# Expand LLM Wiki

Use this skill to grow ARA's compounding LLM wiki without corrupting its graph.
The wiki is not regenerated. It is CRUD-maintained: update existing pages by
default, create new pages only when the subject is genuinely missing, and never
delete pages.

## First Principles Check

Before writing, answer these briefly for yourself:

- What is actually being asked: latest digest ingest, topic backfill, graph
  cleanup, schema repair, or OKF export readiness?
- What are the mechanics: Markdown pages under `research/wiki/`, strict
  frontmatter, alias-aware `[[wikilinks]]`, generated `index.json`, append-only
  `log.md`.
- What is known directly: facts already in the daily digest, model tickets, or
  cited repo sources.
- What is assumed: unsourced claims, vendor benchmarks, rumored timelines, or
  anything only inferred from community chatter.

Challenge the premise if the requested expansion would duplicate pages, read
the raw firehose instead of curated synthesis, or turn weak signal into a
permanent wiki page.

## Required Context

Read these before editing:

1. `docs/wiki-schema.md` in full. It is the contract.
2. `research/wiki/index.md` and `research/wiki/log.md`.
3. The relevant existing pages under `research/wiki/{entities,concepts,themes}/`.
4. The curated input for the task:
   - Latest or specified `research/digest/*-digest.md`.
   - Relevant `research/models/tickets/*.md`, especially recently updated
     tickets.
   - For an explicit topic backfill, any repo-local research files the user
     points at.

Do not crawl `research/twitter/`, `research/rss/`, `research/community/`,
`research/blogs/`, `research/arxiv/`, or other raw-source directories for a
normal expansion pass. The digest exists to curate those sources. Use web search
only to corroborate a specific unstable claim or when the user explicitly asks
for current external verification.

## Expansion Workflow

1. Rank candidate subjects.
   Pull out significant entities, concepts, and themes. Ignore passing mentions.
   For manual backfills, prefer 4-8 high-leverage subjects over shallow coverage.

2. Search before every write.
   Run `uv run python scripts/wiki_search.py "<name>"` for the canonical name and
   likely aliases. If a plausible page exists, update it. Add aliases when a new
   name refers to the same subject. Create a page only when no existing page
   covers the identity.

3. Update in place.
   Fold new facts into the body with concise analysis:
   - why it matters
   - what changed
   - how it links to other pages
   - uncertainty and open questions

   Bump `timestamp` to the meaningful update date as
   `YYYY-MM-DDT00:00:00Z`. Do not change `created_at`, slug, or filename.

4. Create new pages conservatively.
   Choose the correct subdir and `type`: `entities`, `concepts`, or `themes`.
   Use stable lowercase kebab slugs. Write OKF-native frontmatter with
   `description` and `timestamp`, include repo-local `sources`, and link to
   related existing pages. Keep vendor/community claims explicitly caveated.

5. Maintain the graph.
   Cross-link generously but intentionally. Add reciprocal links when they make
   the receiving page more useful, not merely to silence advisory lint.
   Preserve alias uniqueness. Never introduce unresolved `[[links]]`.

6. Update the catalog and log.
   Add new pages to `research/wiki/index.md` under the correct section.
   Append exactly one new entry to `research/wiki/log.md`:

   ```markdown
   ## [YYYY-MM-DD] ingest | Created N (...). Updated M (...).
   ```

   Keep older log entries unchanged.

7. Regenerate generated artifacts.
   Run:

   ```bash
   uv run python scripts/build_wiki_index.py
   ```

   Never hand-edit `research/wiki/index.json`.

## Validation

Run these before reporting completion:

```bash
uv run python scripts/check_wiki.py
uv run python scripts/build_wiki_index.py --check
uv run python scripts/export_wiki_okf.py --out /tmp/ara-okf-check --clean
git diff --check
```

For substantive changes, also run:

```bash
uv run python -m unittest discover -s scripts -p 'test_*.py'
cd dashboard && bun run build
```

Run advisory lint after hard validation:

```bash
uv run python scripts/check_wiki.py --lint
```

Treat lint as guidance. Fix easy high-value reciprocal links, orphans, and stale
pages, but do not churn the graph solely to reach zero warnings.

## Quality Bar

- Preserve one page per subject. Duplicate pages are the main failure mode.
- Prefer durable knowledge over news blurbs.
- State uncertainty labels in prose when sources are partial, vendor-adjacent,
  preliminary, or rumor-grade.
- Use concrete numbers and dates from sources.
- Keep body content useful to an analyst or LLM agent: mechanisms, implications,
  relationships, and open questions beat decorative prose.
- Write only files needed for the wiki expansion unless the user explicitly asks
  for schema/tooling changes.
