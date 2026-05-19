# Methodology Improvements — 2026-05-19

## Why this PR changes hourly-rss.yml

Yesterday's review (2026-05-18) cleared the two big aggregation outages
(Bluesky 403, RSS workflow disabled). With both lanes producing again,
the next-most-impactful gap is **source breadth in the RSS lane**: the
daily-digest synthesizer is *quoting* sources that ARA does not ingest
directly, and is relying on the Twitter lane to surface them as
second-hand citations.

This PR promotes five expert-commentary sources and one missing
tech-news source from "cited in digest" to "first-class RSS input."

## 1. Coverage gap: digest quotes SemiAnalysis, MIT Tech Review,
   Simon Willison without ingesting their feeds

### Evidence

Reading [`research/digest/2026-05-18-digest.md`](../../research/digest/2026-05-18-digest.md)
and [`research/2026-05-18-ai-news.md`](../../research/2026-05-18-ai-news.md)
end-to-end, the following sources appear as quoted/linked references but
do not exist in any `research/rss/*.md` daily file:

- **SemiAnalysis** — cited 5+ times in the 2026-05-18 digest cycle
  (96% Anthropic token-share procurement signal, Jensen MFU quote,
  ABF substrates story, NVIDIA HBM analysis, Rubin CPX coverage).
  ARA only sees these once they bubble through Twitter via
  `@SemiAnalysis_`.
- **MIT Technology Review** — cited twice in the 2026-05-18 digest
  (Musk v. Altman week-3 coverage; Mythos cybersecurity stories
  flagged in 2026-05-11 carry).
- **Simon Willison's Weblog** — Simon publishes the most rigorous
  hands-on coverage of each new LLM release (Opus 4.7, DeepSeek V4,
  Gemma 4, etc.) and his posts routinely make HN front page, but
  ARA only sees them via second-hand HN pickup.

### Root cause

The original `hourly-rss.yml` source list was scoped to **official
company blogs + traditional tech press + arXiv**. It does not cover
the **expert-commentary lane** (independent researchers, applied-AI
educators, hardware/infra newsletter authors) that the daily-digest
synthesizer has come to rely on for analysis-grade signal.

### Fix

Added six feeds to `.github/workflows/hourly-rss.yml`. Each was
probed today and returned HTTP 200 with valid RSS/Atom containing
recent dated entries:

| Feed | URL | Items in probe | Role |
|---|---|---|---|
| MIT Technology Review AI | `https://www.technologyreview.com/topic/artificial-intelligence/feed/` | 10 | Long-form AI journalism |
| SemiAnalysis | `https://semianalysis.com/feed/` | 10 | AI/HW infrastructure analysis |
| Simon Willison | `https://simonwillison.net/atom/everything/` | 30 | Hands-on LLM coverage |
| Interconnects (Nathan Lambert) | `https://www.interconnects.ai/feed` | 7 | Open-model commentary |
| Import AI (Jack Clark) | `https://jack-clark.net/feed/` | 10 | Anthropic-cofounder essays |
| One Useful Thing (Ethan Mollick) | `https://www.oneusefulthing.org/feed` | 2 | Applied-AI essays |

Workflow changes:

- Added six `curl` blocks to the **Fetch RSS Feeds** step, each with
  the same `User-Agent` header pattern and `|| echo "<rss></rss>"`
  fallback the existing feeds use.
- Added a new **Expert Commentary** group in the Claude prompt's
  SOURCE FILES section and a corresponding **🧠 Expert Commentary**
  section in the OUTPUT format, so the new feeds land in their own
  bucket rather than being silently merged into Tech News.
- Added MIT Technology Review to the existing **Tech News** group.

### Expected impact

- **Faster first-touch on SemiAnalysis pieces** — currently ARA waits
  for `@SemiAnalysis_` to post the link to Twitter; with the RSS feed,
  ARA sees it on publication. For pieces like the Jensen-MFU recap or
  ABF-substrates story that anchored 2026-05-18's digest, this is
  hours-to-half-a-day earlier.
- **First-party Simon Willison posts** — instead of seeing them
  reflected via HN comments, ARA gets the original text. Useful for
  the model-release coverage the digest depends on.
- **Anthropic policy reads via Import AI** — Jack Clark's newsletter
  is one of the most reliable surfaces for "what Anthropic is thinking
  about AGI policy" coverage that doesn't go through corporate comms.
  Pairs naturally with the existing `anthropic.xml`.

## What was deliberately not changed

- **Twitter, Hacker News, Reddit, arXiv, models-timeline, digest,
  front-page, audio-digest, bluesky** are all producing healthy daily
  output — no further churn warranted.
- **arXiv & model-timeline 2026-05-18 files are missing** — the
  `research/arxiv/2026-05-17-papers.md` file is the most recent, and
  `research/models/2026-05-17-timeline.md` likewise. Both are
  single-day gaps with no preceding pattern; without access to the
  Actions run-log it isn't clear whether this is a runner-availability
  blip or a workflow failure. Flagging for the next operator pass
  rather than churning the workflow files speculatively.
- **The "MCP Search: not invoked this cycle" line in the digest** is
  not a workflow defect — the digest synthesis prompt already routes
  to MCP only when internal sources are thin, and the 2026-05-18
  cycle had plenty of internal signal.
- **Meta AI Blog** remains commented out in `hourly-rss.yml` — still
  404 as of the 2026-05-18 probe.

## Push-permission blocker (carry from 2026-05-18 improvement #3)

The matching workflow edit was prepared and validated locally but
**cannot be pushed from `daily-improve.yml`** until the `claude[bot]`
GitHub App installation is granted **Workflows: read & write** on this
repository. The push fails with:

```
! [remote rejected]   improve/2026-05-19 -> improve/2026-05-19
  (refusing to allow a GitHub App to create or update workflow
   `.github/workflows/hourly-rss.yml` without `workflows` permission)
```

This is the **same blocker** documented in
[`docs/archive/2026-05-18-improvements.md`](2026-05-18-improvements.md)
section 3, and is exactly what the prior PR's removal of the
`|| echo "Already pushed..."` swallow was meant to surface — so the
failure is intentional, not a regression. This PR is therefore
**docs-only**, with the workflow patch embedded below for a maintainer
to apply by hand (or for the App permission to be granted, after which
a follow-up automated PR can carry the workflow change directly).

### Workflow patch to apply manually

Apply against `.github/workflows/hourly-rss.yml` (the file matches
`main` at the time of this PR):

```diff
@@ -90,6 +90,47 @@ jobs:
             -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
             > /tmp/rss/venturebeat_ai.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/venturebeat_ai.xml

+          # MIT Technology Review — Artificial Intelligence section.
+          # Cited frequently in daily-digest synthesis; adds long-form
+          # journalism on AI policy and lab dynamics.
+          curl -sL "https://www.technologyreview.com/topic/artificial-intelligence/feed/" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/mit_tech_review_ai.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/mit_tech_review_ai.xml
+
+          # SemiAnalysis — Dylan Patel's AI/hardware infrastructure newsletter.
+          # Daily-digest cited it 5+ times in 2026-05-18 cycle (compute,
+          # procurement, datacenter analysis); promoting from secondary-pickup
+          # to first-class source.
+          curl -sL "https://semianalysis.com/feed/" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/semianalysis.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/semianalysis.xml
+
+          # Simon Willison's Weblog (atom/everything) — covers every LLM
+          # release with hands-on notes; high signal-to-noise on practical
+          # capability changes.
+          curl -sL "https://simonwillison.net/atom/everything/" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/simonwillison.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/simonwillison.xml
+
+          # Interconnects (Nathan Lambert) — open-model commentary and
+          # research-lab analysis from an Ai2 perspective.
+          curl -sL "https://www.interconnects.ai/feed" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/interconnects.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/interconnects.xml
+
+          # Import AI (Jack Clark, Anthropic co-founder) — frontier-lab
+          # commentary; pairs well with anthropic.xml for "what is Anthropic
+          # actually thinking" coverage.
+          curl -sL "https://jack-clark.net/feed/" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/import_ai.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/import_ai.xml
+
+          # One Useful Thing (Ethan Mollick, Wharton) — applied-AI essays
+          # often picked up by HN and r/artificial.
+          curl -sL "https://www.oneusefulthing.org/feed" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/one_useful_thing.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/one_useful_thing.xml
+
           echo "RSS feeds fetched successfully"
           ls -la /tmp/rss/

@@ -124,6 +165,14 @@ jobs:
             - techcrunch_ai.xml (TechCrunch AI)
             - verge_ai.xml (The Verge AI)
             - venturebeat_ai.xml (VentureBeat AI)
+            - mit_tech_review_ai.xml (MIT Technology Review — AI)
+
+            **Expert Commentary:**
+            - semianalysis.xml (SemiAnalysis — AI/HW infrastructure)
+            - simonwillison.xml (Simon Willison — practical LLM coverage)
+            - interconnects.xml (Nathan Lambert — open-model commentary)
+            - import_ai.xml (Jack Clark / Anthropic — frontier-lab essays)
+            - one_useful_thing.xml (Ethan Mollick — applied-AI essays)

             RSS XML structure:
             - channel/item/title (article title)
@@ -167,6 +216,26 @@ jobs:
             #### VentureBeat
             - [Title](url) - date

+            #### MIT Technology Review
+            - [Title](url) - date
+
+            ### 🧠 Expert Commentary
+
+            #### SemiAnalysis
+            - [Title](url) - date
+
+            #### Simon Willison
+            - [Title](url) - date
+
+            #### Interconnects
+            - [Title](url) - date
+
+            #### Import AI
+            - [Title](url) - date
+
+            #### One Useful Thing
+            - [Title](url) - date
+
             ### 📄 New arXiv Papers

             #### CS.AI
```

After applying, run `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/hourly-rss.yml'))"` — should print no errors.

## Files changed

- `docs/archive/2026-05-19-improvements.md` (this file)
- `.github/workflows/hourly-rss.yml` — **proposed**, see the patch
  above; cannot be pushed by `daily-improve.yml` until the
  `claude[bot]` App is granted `Workflows: write` on the repo.
