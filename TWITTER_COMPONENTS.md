# Twitter Components

Twitter/X cycle reports are still stored as Markdown under `research/twitter/`,
but new cron output should use a small HTML component vocabulary for Top
Stories. The dashboard renders these components directly and falls back to the
legacy Markdown parser for older reports.

## Story

```html
<article class="twitter-story" data-rank="1">
  <h3 class="twitter-story-title">Current-cycle news headline</h3>
  <p class="twitter-story-lead">One or two sentences on what happened now.</p>
  <details class="twitter-story-details">
    <summary>Full analysis</summary>
    <div class="twitter-story-sources">
      <a class="twitter-source-chip" href="https://x.com/handle/status/ID">@handle</a>
    </div>
    <div class="twitter-story-signals">
      <div><span>Verify</span>Verification status and reason.</div>
      <div><span>Watch</span>Concrete next signal.</div>
    </div>
    <div class="twitter-story-body">
      <p><strong>Evidence:</strong> Details and links.</p>
      <p><strong>Counter / contradicting:</strong> Skeptical read.</p>
      <p><strong>Context:</strong> Optional prior-cycle context.</p>
    </div>
  </details>
</article>
```

Rules:

- The folded view is only `twitter-story-title` and `twitter-story-lead`.
- `twitter-story-lead` must start with current-cycle news, not prior context.
- Do not put source-method prose such as `verified by curl`, raw URLs, or audit
  details in `twitter-story-lead`.
- Put source chips, verification detail, watch items, and prior context inside
  `twitter-story-details`.
- Historical Markdown reports remain valid; the dashboard uses the old parser
  when `twitter-story` components are absent.
