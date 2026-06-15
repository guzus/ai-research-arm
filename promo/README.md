# ara — promo video

A [Remotion](https://www.remotion.dev/) project that renders the launch /
landing promo for **[ara.guzus.xyz](https://ara.guzus.xyz)** — the automated
AI-news intelligence pipeline.

It's built almost entirely from **real product output**: the actual "AGI
Awareness Post" daily front-page renders (`research/front-page/`) and live,
full-page screen captures of the dashboard (Today, Model Timeline, Wiki,
Generative Research) that auto-scroll inside a browser frame.

![poster](preview/poster.png)

The video is self-contained and lives **outside** `dashboard/`, so it never
touches the Vite/Docker build or CI (`ci.yml` only triggers on
`workflows/dashboard/scripts`). It's an asset project, run on demand.

## Quick start

```bash
cd promo
npm install
npm run dev        # open Remotion Studio to scrub/preview
npm run render     # -> out/ara-promo.mp4   (1920×1080, h264)
npm run poster     # -> out/poster.png
```

`npm run *` runs `scripts/prepare-assets.mjs` first (see **Assets** below), so a
clean checkout renders without any manual setup.

> Uses **npm** (not the repo-wide bun) on purpose: `@remotion/renderer` ships a
> Chrome Headless Shell and native bits that are best-trodden under npm. The
> project is fully isolated (own `package.json` / `node_modules`), so the
> package-manager split is contained here.

## Compositions

One timeline, three aspect ratios (scenes read `useVideoConfig()` and re-flow
for portrait):

| id              | size       | use                          | command                  |
| --------------- | ---------- | ---------------------------- | ------------------------ |
| `Promo`         | 1920×1080  | landing hero · YouTube · X   | `npm run render`         |
| `PromoSquare`   | 1080×1080  | feed posts                   | `npm run render:square`  |
| `PromoVertical` | 1080×1920  | Shorts · Reels · TikTok      | `npm run render:vertical`|

~29s @ 30fps. The exact frame count is derived in `src/Promo.tsx`
(`PROMO_DURATION`) from the per-scene holds minus the transition overlaps.

## Scenes (`src/scenes/`)

| # | scene          | what it shows                                                        |
| - | -------------- | ------------------------------------------------------------------- |
| 1 | `ColdOpen`     | the `ara` wordmark over a drifting field of source names            |
| 2 | `Firehose`     | "Everything in AI. As it happens." — a counter + a live ticker      |
| 3 | `Pipeline`     | Aggregate → Synthesize → Generate → Publish, "no human in the loop" |
| 4 | `FrontPage`    | a coverflow press-run of **real** AGI Awareness Post editions       |
| 5 | `Product`      | **real** dashboard captures auto-scrolling inside a browser frame   |
| 6 | `Outro`        | wordmark · `ara.guzus.xyz` · sources                                |

Assembled with `@remotion/transitions` (fade / wipe / slide) in `src/Promo.tsx`.

## Assets

`scripts/prepare-assets.mjs` (run automatically before every `dev`/`render`)
does two things:

1. **`copy-frontpages.mjs`** — copies the 12 most recent
   `research/front-page/*.png` editions into `public/frontpages/`
   (**gitignored** — the source PNGs already ship in the repo as regular git
   blobs, so we don't duplicate them) and writes `src/frontpages.ts`, the
   single source of truth for which editions the montage fans through.
2. **`gen-screens.mjs`** — scans `public/screens/*.png`, reads each PNG's
   dimensions from its header, and writes `src/screens.ts` (the `{src,w,h}`
   manifest the `Product` scene needs for exact scroll math). A missing key
   falls back to a styled mock panel, so the project always renders.

### Refreshing the dashboard captures

`public/screens/*.png` are **committed** point-in-time snapshots of the live
site (it changes daily, so they can't be regenerated deterministically). To
refresh them, capture full-page screenshots at **1440px CSS width, 2× DPI**,
light mode, of:

| key        | route                       |
| ---------- | --------------------------- |
| `today`    | `https://ara.guzus.xyz/`        |
| `models`   | `https://ara.guzus.xyz/models`  |
| `research` | `https://ara.guzus.xyz/research`|
| `wiki`     | `https://ara.guzus.xyz/wiki`    |

Downscale to **1440px wide** (`models` is huge — top-crop to ~7600px first),
drop them in `public/screens/<key>.png`, and re-run `npm run assets`. Any
headless browser works (Playwright/Puppeteer); the `Product` scene auto-scrolls
whatever height you give it (capped for readability).

## Design

Mirrors the dashboard's ARA "McKinsey" system
(`dashboard/src/components/ara-research.css`):

- **Palette** — deep navy `#051c2c`, electric royal `#2251ff`, cyan `#00a9f4`
  on newspaper paper. A near-monochrome blue family, no rainbow. (`src/theme.ts`)
- **Type** — Source Serif 4 (display), Inter (UI), JetBrains Mono (eyebrows /
  metadata), loaded via `@remotion/google-fonts` (`src/fonts.ts`).
