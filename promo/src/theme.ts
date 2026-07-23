/**
 * Design tokens for the ara promo. Mirrors the dashboard's ARA "McKinsey"
 * palette (dashboard/src/components/ara-research.css): a near-monochrome blue
 * family — deep navy, electric royal, cyan — on newspaper paper. No rainbow.
 */
export const COLOR = {
  navy: "#051c2c", // deep navy — dark fills / cold-open ground
  navy2: "#0b2c44", // lifted navy for gradients
  navy3: "#14405f",
  royal: "#2251ff", // electric royal — primary accent, big figures
  cyan: "#00a9f4", // secondary accent / second data series
  sky: "#7fb3ff",
  periwinkle: "#e6ebff", // soft panel bg
  paper: "#fbfbf8", // newspaper off-white
  paper2: "#f2f1ec",
  ink: "#16181d", // primary body ink
  sec: "#5b6470", // secondary text
  sec3: "#9aa3af", // tertiary text
  rule: "#d8d8de", // thin hairline
  white: "#ffffff",
} as const;

/** The six raw signal sources ARA aggregates. Order is deliberate. */
export const SOURCES = [
  "Twitter / X",
  "arXiv",
  "Hacker News",
  "Reddit",
  "RSS",
  "Bluesky",
] as const;

/** The four product pillars surfaced on the dashboard. */
export const PILLARS = [
  {
    tab: "Today",
    title: "Daily Digest",
    blurb: "Every source, distilled into one briefing each morning.",
  },
  {
    tab: "Model Timeline",
    title: "Model Timeline",
    blurb: "A living ledger of every model release, rumor to ship.",
  },
  {
    tab: "Wiki",
    title: "LLM Wiki",
    blurb: "A knowledge base that compounds — one page per idea.",
  },
  {
    tab: "Research",
    title: "Generative Research",
    blurb: "Long-form, heavily-cited articles, written end to end.",
  },
] as const;

export const SITE_URL = "ara.guzus.xyz";

// The montage's edition list lives in the auto-generated src/frontpages.ts
// (built by scripts/copy-frontpages.mjs from research/front-page/).
