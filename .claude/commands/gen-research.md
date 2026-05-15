---
description: Research a topic with primary sources and write an HTML article into research/generative/
argument-hint: <topic>
---

# Generative Research

User-supplied topic: **$ARGUMENTS**

If the topic above is empty or just whitespace, ask the user for a topic and stop until they answer.

## What you are doing

Produce a single self-contained `<article>` HTML fragment about the topic and persist it via the canonical writer at `scripts/write_generative_research.py`. The writer handles slug, timestamp, index update, and git commit — your only job is the research and the body.

## Research

1. Use `WebSearch` to find primary sources (official docs, papers on arXiv, GitHub repos, posts from credible authors). Skip SEO farms and aggregator summaries.
2. Use `WebFetch` to actually read the sources you cite — do not cite a URL you have not read.
3. Corroborate non-obvious claims from at least two independent sources. If you cannot, say so explicitly in the article rather than asserting confidently.
4. Prefer recent material; note publication dates when freshness matters.

## Write the article

Compose one `<article>...</article>` fragment. Hard constraints (the writer will reject violations):

- No `<style>`, `<script>`, `<head>`, `<body>`, no inline `style=` attributes, no `on*=` handlers, no `javascript:` URLs.
- Allowed inner tags only: `h2 h3 h4 p ul ol li em strong code pre blockquote table thead tbody tr th td figure figcaption a img hr br`.
- Lead with a single `<h2>` containing the article title — the writer derives the stored title from this.
- After the `<h2>`, open with a lead paragraph that states the thesis in plain language.
- Use `<h3>` (and `<h4>` if needed) for sub-sections. Cite sources inline with `<a href="...">`.
- Keep body under ~200 KB. Plain prose, no markdown syntax inside the HTML.

Be honest about uncertainty. A short, accurate article beats a long, confident one.

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
  --html-body /tmp/gen-research-body.html
```

The writer prints the relative path of the new file and the index size on stdout, then commits locally. **Do not push** — leave the commit for the user to review.

## Report back to the user

One short message containing:

- The article title (the text inside your `<h2>`).
- The file path the writer printed (e.g. `research/generative/2026-05-15T....html`).
- A one-sentence note if any claim was left uncorroborated, so the user knows what to spot-check before pushing.
