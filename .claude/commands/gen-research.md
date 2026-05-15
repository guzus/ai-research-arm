---
description: Research a topic with primary sources and write an HTML article into research/generative/
argument-hint: <topic>
---

# Generative Research

User-supplied topic: **$ARGUMENTS**

If the topic above is empty or just whitespace, ask the user for a topic and stop until they answer.

## What you are doing

Produce a single self-contained `<article>` HTML fragment about the topic and persist it via the canonical writer at `scripts/write_generative_research.py`. The writer handles slug, timestamp, index update, and git commit — your only job is the research and the body.

**You compose from a fixed component vocabulary, not freeform HTML.** Read `COMPONENTS.md` at the repo root before writing. The writer parses your body and rejects unknown classes or tags.

## Research

1. Use `WebSearch` to find primary sources (official docs, papers on arXiv, GitHub repos, posts from credible authors). Skip SEO farms and aggregator summaries.
2. Use `WebFetch` to actually read the sources you cite — do not cite a URL you have not read.
3. Corroborate non-obvious claims from at least two independent sources. If you cannot, say so explicitly in the article rather than asserting confidently.
4. Prefer recent material; note publication dates when freshness matters.

## Write the article

Compose one `<article class="ara-doc">...</article>` fragment using **only** classes that start with `ara-` and **only** tags in the allowlist. The writer enforces both.

Hard rules (the writer will reject violations):

- Root must be `<article class="ara-doc">`.
- Every `class=` token must start with `ara-`.
- Allowed tags only: `article section div header footer h2 h3 h4 p span em strong code mark sup sub abbr time ul ol li dl dt dd a img figure figcaption table thead tbody tr th td blockquote pre br hr`.
- No `<style>`, `<script>`, `<iframe>`, `<head>`, `<body>`, `<h1>`. No inline `style=`, no `on*=` handlers, no `javascript:` URLs.
- Body under ~200 KB.

Read `COMPONENTS.md` for the full vocabulary. Skeleton:

```html
<article class="ara-doc">
  <span class="ara-eyebrow">Category · Topic</span>
  <h2 class="ara-display">Article title</h2>
  <p class="ara-deck">Optional one-line dek.</p>

  <p class="ara-lede">Opening paragraph.</p>

  <p>Body paragraph.</p>

  <h3 class="ara-h2"><span class="ara-h2-num">01</span>First section</h3>
  <p>…</p>
</article>
```

The visual reference article (slug: `components`) in the Research tab exercises every primitive. When in doubt, look at how the reference uses a component.

Be honest about uncertainty. A short, accurate article beats a long, confident one. Use `ara-callout--warn` to mark unverified claims; `ara-callout--danger` only for red flags.

## Persist via the writer

Do not paste HTML on the command line — it will be mangled by shell quoting. Write the fragment to a temp file, then call the writer with `--html-body` pointing at it.

```bash
# 1. Write the body to a temp file (use the Write tool, not heredocs in bash).
#    Path: /tmp/gen-research-body.html

# 2. Invoke the writer. Quote the topic so spaces survive.
python3 scripts/write_generative_research.py \
  --topic "<the exact topic the user gave>" \
  --model "claude-opus-4-7" \
  --source "local" \
  --kind fragment \
  --html-body /tmp/gen-research-body.html
```

If the writer prints a validation error (`disallowed tag`, `non-ara-* classes`), fix the body and re-run. Do **not** strip the validation; the design system is the point.

The writer prints the relative path of the new file and the index size on stdout, then commits locally. **Do not push** — leave the commit for the user to review.

## Report back to the user

One short message containing:

- The article title.
- The file path the writer printed.
- A one-sentence note if any claim was left uncorroborated, so the user knows what to spot-check before pushing.
