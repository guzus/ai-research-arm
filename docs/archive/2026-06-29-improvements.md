# Methodology Improvements — 2026-06-29

Analysis of 2026-06-28 output across all research lanes.

## Concrete defect found (cited)

**The RSS lane silently lost two feeds — including Anthropic's own blog —
on every hourly run, and the deterministic fallback that was carrying the
lane discarded each broken feed wholesale.**

Evidence:

- `research/rss/2026-06-28.md` — every single hourly `### Feed Notes`
  section (lines 71–74, 118–121, 165–168, … repeated **12×** across the
  day) reports:
  ```
  - anthropic.xml: parse error: not well-formed (invalid token): line 17, column 8
  - marktechpost.xml: parse error: mismatched tag: line 80, column 2
  ```
- Persistence (count of `anthropic.xml: parse error` per daily file):
  `06-25:0 → 06-26:5 → 06-27:9 → 06-28:12 → 06-29:3`. The failure is not a
  one-off; it has recurred on every run since 2026-06-26.
- These two feeds therefore contributed **zero items** for four days.
  `anthropic.xml` is Anthropic's own news feed and `marktechpost.xml` is a
  high-volume model-release / open-source aggregator — both first-class
  sources in `hourly-rss.yml`.

Root cause (two layers, both confirmed by reading the code):

1. `scripts/deterministic_rss_digest.py` parsed each feed with a strict
   `ET.fromstring(body)` (old line 184); on any `ParseError`,
   `collect_items` (old line 225) recorded a note and dropped the **entire
   feed**. A single mismatched tag or one stray byte in a 30-item feed threw
   away all 30 items. This is exactly the `marktechpost.xml` shape
   (`mismatched tag: line 80`).
2. `.github/workflows/hourly-rss.yml` fetched feeds with `curl -sL … || echo
   "<rss></rss>"`. Because `-sL` (no `-f`) exits **0** on HTTP 4xx/5xx, a
   proxy/CDN error page (e.g. OpenRSS returning HTML for `anthropic.xml`)
   was saved as the feed body and then failed XML parsing every run — the
   `|| echo` fallback was dead code. This is the `anthropic.xml` shape
   (`not well-formed (invalid token): line 17`, the start of an HTML page).

## Changes made

1. **`scripts/deterministic_rss_digest.py` — resilient feed parsing.**
   New `resilient_entries()` replaces the bare `ET.fromstring` in
   `parse_feed`:
   - fast path: strict parse (unchanged behavior for healthy feeds);
   - on failure: retry after `_sanitize_xml()` strips invalid XML control
     bytes and escapes bare ampersands (the two most common
     "invalid token" causes);
   - last resort: `_salvage_entries()` extracts each `<item>`/`<entry>`
     block and parses it in isolation under a wrapper that re-declares the
     common feed namespaces (`content:`, `dc:`, `media:`, …), keeping the
     survivors. One broken entry — or a truncated download — no longer
     discards the whole feed.
   - A genuinely non-feed body (an HTML error page with no entries) still
     raises and surfaces as a Feed Note, so real outages stay visible.

2. **`scripts/test_deterministic_rss_digest.py` — coverage for the above.**
   Four new tests: one-broken-item salvage (the marktechpost shape), bare-
   ampersand recovery, truncated-feed salvage, and the guarantee that a
   non-feed HTML error page still raises.

## Recommended follow-up (NOT in this PR — needs `workflows` permission)

The companion fix for the `anthropic.xml` layer is a one-line-per-feed change
in `.github/workflows/hourly-rss.yml`: replace the repeated
`curl -sL … || echo "<rss></rss>"` invocations with a `fetch()` helper using
`curl -fsL --max-time 30 --retry 2`. With `-f`, an HTTP 4xx/5xx makes curl
exit non-zero so the empty-document fallback actually fires — the proxy's
HTML error page never reaches the parser (today, without `-f`, that fallback
is dead code). **This change is not included here because the bot's
`GITHUB_TOKEN` lacks the `workflows` permission to push workflow files**
(`refusing to allow a GitHub App to … update workflow … without workflows
permission`). The maintainer should apply it manually. The parser fix above
is independent and already eliminates the whole-feed-drop failure mode.

## Expected impact

- `marktechpost.xml` items (and any future feed with one malformed entry or
  a truncated download) are recovered by the deterministic fallback instead
  of being dropped — the core defect, fixed in this PR.
- No behavior change for healthy feeds (strict parse remains the fast path);
  a genuinely non-feed body (HTML error page) still surfaces as a Feed Note.
- Once the `curl -f` follow-up lands, `anthropic.xml` HTTP-error responses
  become a clean empty feed instead of 12 lines/day of recurring
  parse-error noise in committed output.

## Observed but NOT fixed here (flagged for the maintainer)

The RSS **Fireworks agent path** degraded sharply over the same window and
the deterministic fallback carried the lane:

| date | agent-format sections (emoji headers) | deterministic fallback sections (`Feed Notes`) |
|---|---|---|
| 06-23 | 12 | 0 |
| 06-25 | 3 | 2 |
| 06-26 | 3 | 5 |
| 06-27 | 2 | 9 |
| **06-28** | **0** | **12** |
| 06-29 | 3 | 3 |

On 2026-06-28 **every** hourly run fell back to the deterministic writer
(`steps.rss-agent.outcome == 'failure'` → `Deterministic RSS fallback`
step). The root cause requires the workflow run logs (transient Fireworks
availability vs. an `expected-paths` commit-guard failure vs. a prompt
issue), which are not derivable from the committed output alone, so it is
**not** patched blind here. Recommended next step: inspect a recent
`Hourly RSS` run's `Process RSS Feeds with Fireworks` step logs to classify
the failure before changing the agent path.
