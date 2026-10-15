---
name: gen-research-ko-backfill
description: "Generate and publish a Korean translation for an existing ARA generative research article."
---

# Gen Research Ko Backfill

Publish a Korean translation of an existing ARA generative-research article by dispatching the repo's `translate-generative-research.yml` ("Korean Generative Research Backfill"). That workflow is the publication path: it resolves the canonical source, translates in an isolated adapter, checks source/translation parity, writes through the canonical writer, verifies the exact commit, and lands it as a review PR (or auto-merges on request). `main` is PR-only, so do not translate and commit locally instead. The dashboard is static and manifest-driven: do not add runtime translation.

## First-Principles Check

Before dispatching, answer:

- Which article is the target, and does `research/generative/index.json` on the default branch contain its slug?
- Is there already a Korean artifact under `translations.ko`? If yes, did the user ask to replace it?
- Does the user want the review PR (the default) or an auto-merge?

If the target slug does not exist, stop and ask for the correct article.

## Workflow

1. Resolve the repo and the target article from an up-to-date default branch.

```bash
cd "$(git rev-parse --show-toplevel)"
git fetch origin
git show origin/main:research/generative/index.json \
  | jq -r '.[] | select(.slug=="<slug>") | [.slug, .file, (.translations.ko.file // "")] | @tsv'
```

2. Dispatch the backfill.

```bash
gh workflow run translate-generative-research.yml -f slug="<slug>"
```

Add `-f overwrite=true` only when a Korean version exists and the user asked to replace it. Add `-f auto_merge=true` only when the user asked to skip the review PR.

3. Follow the run to completion.

```bash
gh run list --workflow translate-generative-research.yml --limit 3
gh run watch <run-id> --exit-status
```

A failed run is a failed backfill: report the failing step and its log excerpt (`gh run view <run-id> --log-failed`), and do not retry by publishing another way. The run summary names the artifact path and, in review mode, the PR (branch prefix `automation/ko-backfill`).

4. Verify the result.

- Review mode: the PR exists and changes only the Korean artifact(s) and `research/generative/index.json`.
- After merge: `translations.ko.file` is set for the slug on `origin/main`, and the artifact passes `uv run python scripts/check_generative_research.py research/generative/<ko-file>`.
- If dashboard verification is in scope, open `/research/<slug>` and switch to `한국어`: it should render the Korean article, and show the "not yet published" note only when `translations.ko.file` is missing.

## Output

Report:

- The target slug.
- The workflow run URL and its conclusion.
- The PR URL (review mode) or the merge result (auto-merge).
- The Korean artifact path and whether `translations.ko.file` is now set.
- Any existing dirty files you intentionally left untouched.
