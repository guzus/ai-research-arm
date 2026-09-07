---
slug: google-weathernext-3-2026-09
title: WeatherNext 3 — Google DeepMind's global weather model, live in Search, Gemini and Maps
company: Google / DeepMind (with Google Research)
model: WeatherNext 3
status: released
status_note: |
  Announced 2026-09-03 by @GoogleDeepMind and @GoogleAI. WeatherNext 3 learns
  directly from real-world, real-time observations rather than running a
  traditional physics simulation, and Google claims prediction **up to 5x
  sharper than WeatherNext 2** with **up to a 50% reduction in global
  precipitation forecast error** — the largest gains in regions where forecasts
  have historically been least reliable. Precipitation is the specific hard case
  Google calls out: prior global models produce blurry estimates or miss severe
  storm boundaries.

  Distribution is what makes this a shipping artifact rather than a paper. From
  2026-09-03 it powers forecasts in **Google Search, the Gemini app, Google Maps
  and the Google Maps Platform Weather API**, with real-time data available to
  developers and researchers via **BigQuery, Earth Engine and GCS**.

  Not a language model, and deliberately in scope anyway: it is a named,
  publicly-shipped frontier model release from a tracked lab in this cycle's
  window, on the same release train as [[gemini-3-8-flash-2026-09]] and
  [[google-lyria-3-5-2026-07]].
expected: "RELEASED 2026-09-03 into Search, Gemini, Maps and the Maps Platform Weather API, with developer access via BigQuery, Earth Engine and GCS. Open: independent verification of the 50% precipitation-error reduction against operational NWP baselines."
labels:
  - google
  - weather
  - scientific-model
  - released
verification: confirmed
sources:
  - https://x.com/GoogleDeepMind/status/2095528012791902536
  - https://x.com/GoogleAI/status/2095544944190788064
  - "@demishassabis"
created_at: 2026-09-07
updated_at: 2026-09-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-07
    change: "Created — RELEASED. @GoogleDeepMind and @GoogleAI announced WeatherNext 3 on 2026-09-03 15:03 UTC, developed with Google Research. The model learns directly from real-world real-time observations instead of running a traditional physics simulation; Google claims prediction up to 5x sharper than WeatherNext 2 and up to a 50% reduction in global precipitation forecast error, with the largest improvements in historically under-served regions — precipitation being the specific failure mode Google names for prior global models (blurry estimates, missed severe-storm boundaries). Shipped the same day into Google Search, the Gemini app, Google Maps and the Google Maps Platform Weather API, with real-time data for developers and researchers via BigQuery, Earth Engine and GCS. Status released, verification confirmed on Google's own announcement; the accuracy claims are Google's and are not independently verified against operational NWP baselines in this cycle's signal. Same release train as [[gemini-3-8-flash-2026-09]] and [[google-lyria-3-5-2026-07]]."
---

This is the quietest of Google's three September releases and probably the one
with the widest real-world blast radius. Gemini 3.8 Flash competes for
developers; WeatherNext 3 goes straight into the default weather forecast seen
by everyone using Search and Maps.

The technical claim worth holding onto is the precipitation one. Global
data-driven weather models have generally been good at temperature and pressure
fields and bad at rain, because precipitation is spatially sharp and the loss
functions that produce good average scores produce blurry, over-smoothed
rainfall. A claimed 50% error reduction concentrated in historically poorly
served regions is the failure mode being addressed directly, not a headline
score.

None of it is independently verified. Google's numbers are Google's, benchmarked
against its own WeatherNext 2, and nothing in this cycle's signal checks them
against operational numerical weather prediction. Worth revisiting once national
meteorological services publish comparisons — that is the corroboration that
would move this from Google's claim to an established result.
