# Contributing

Thanks for your interest in `ai-research-arm`. This is primarily a personal
research pipeline that happens to be open source, so please read the scope
notes below before investing time in a large change.

## Orientation

- **[`README.md`](../README.md)** — what the project is, the Quickstart (no
  accounts needed), and an honest "what you can run vs. what needs the
  maintainer's accounts" boundary.
- **[`CLAUDE.md`](../CLAUDE.md)** — the full operator's manual: pipeline
  architecture, every workflow, output locations, and the **load-bearing
  rules** that, if broken, silently corrupt output. Read the relevant rule
  before touching workflows, `research/`, the ARA DSL, or the dashboard.

## Local development

```bash
# Dashboard (TypeScript SPA) — runs against committed sample data, no secrets.
cd dashboard && bun install && bun run dev

# Python tooling (stdlib-first; deps managed with uv).
uv sync --all-extras
uv run python -m unittest discover -s scripts -p 'test_*.py'
```

## Before you open a PR

- **Run the tests** above and any validator relevant to your change:
  - `uv run python scripts/check_model_tickets.py` (model tickets)
  - `uv run python scripts/check_wiki.py` (wiki pages)
  - `uv run python scripts/check_generative_research.py <file>` (ARA articles)
- **Generative-research output** must go through the DSL compile + validate
  contract — see load-bearing rule 1 in `CLAUDE.md`. Hand-written HTML in
  `research/generative/` will be rejected.
- **Keep secrets out of the repo.** Nothing in `.env` is ever committed
  (`.env.example` documents the contract). Workflows read credentials from
  GitHub Actions secrets only.
- **Workflow YAML:** never interpolate untrusted event input (issue/PR title
  or body) directly into `run:`; pass it through `env:` and quote it.

## Scope expectations

Bug fixes, documentation, new data-source lanes, and dashboard improvements are
welcome. Large architectural changes are best discussed in an issue first — much
of the pipeline assumes the maintainer's specific deployment, so not every
change generalizes cleanly.
