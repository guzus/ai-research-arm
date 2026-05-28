# ARA generative UI direction

ARA should copy the catalog/protocol discipline from Google's A2UI work and
the reader-facing interaction polish from Vercel's AI UI stack.

## Premise

Generated research articles are durable artifacts. They need to render as
dashboard pages, static HTML, PDF, Telegram summaries, and audio scripts.
That makes arbitrary generated React/JSX the wrong primitive for ARA: it is
harder to validate, harder to archive, and harder to re-render outside the
dashboard.

The right primitive is structured UI intent that maps onto a fixed component
catalog. ARA already had most of this shape with `.ara.md`; `ARA_CATALOG.json`
now makes the component contract explicit and machine-readable.

## What to copy from Vercel

- Stream intermediate agent states as useful UI: source collection, claim
  extraction, chart drafting, red-team pass, and final render.
- Render tool results as compact components instead of raw logs: source cards,
  claim cards, contradiction cards, chart drafts, ticker snapshots, and timeline
  events.
- Treat citations, copy actions, file exports, reasoning visibility, and
  loading states as first-class UI states.
- Make every generated data component inspectable with hover, keyboard focus,
  and copy/export affordances.

Reference: https://vercel.com/blog/ai-sdk-3-generative-ui

## What to copy from Google

- Agents emit UI intent against a catalog; clients own rendering.
- Catalogs carry component purpose, props, examples, constraints, and version.
- Validation happens before render, not after a broken page reaches readers.
- The client can expose only the components that make sense for the current
  surface: dashboard, mobile, PDF, audio summary, or Telegram.
- Streaming should tolerate partial output, but the committed artifact must
  pass a strict schema/validator.

Reference: https://developers.googleblog.com/a2ui-v0-9-generative-ui/

## ARA decisions

1. Keep `.ara.md` as the author-facing source.
2. Treat `ARA_CATALOG.json` as the machine-readable component contract.
3. Keep `COMPONENTS.md` as the human reference.
4. Keep dashboard enhancement runtime-only: authors never write `script`,
   `style`, `iframe`, `svg`, event handlers, or inline styles.
5. Prefer safe, portable structured intent over generated app code.

## Next implementation steps

- Add an optional JSON intent format that compiles to `.ara.md`.
- Add 2-3 high-quality examples per catalog component.
- Add a research-run progress timeline in the dashboard.
- Add copy-data/export affordances for generated charts.
- Add a preflight planner view before expensive long-form research runs.
