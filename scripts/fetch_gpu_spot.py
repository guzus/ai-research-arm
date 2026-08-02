#!/usr/bin/env python3
"""Refresh research/market/gpu-spot.json — a per-GPU spot rental price series.

WHY THIS LANE EXISTS
--------------------
The research pipeline can cite what a filing *says* but cannot observe what a
market *does*. Spot GPU rental pricing is the missing primary input: it is the
number that anchors any argument about whether compute buyers are over- or
under-earning on contracted rates. Nobody publishes this as a clean time
series, so the pipeline observes it directly and compounds its own.

The compounding is the entire point. A file that holds only "now" is worthless
here — a single H100 print says nothing; H100 prints every 6h for a year say
whether the market is tightening. Hence `history`, which only ever appends.

SOURCE
------
Vast.ai's public marketplace endpoint, unauthenticated:

    https://console.vast.ai/api/v0/bundles/?q=<url-encoded JSON>

No credentials, no key, no account. Verified 2026-08-02.

THE ONE CORRECTNESS DETAIL THAT MATTERS MOST
--------------------------------------------
`dph_total` is dollars-per-hour for the WHOLE MACHINE, not per GPU. The
per-GPU price is `dph_total / num_gpus`. An off-by-num_gpus error here would
silently multiply every reported price by up to 8x and poison every downstream
article. Confirmed empirically 2026-08-02 three ways:
  - an 8x "H100 SXM" offer priced dph_total 19.2016 -> $2.40/GPU/hr, which is a
    plausible H100 rate; read as per-GPU it would be $19.20/GPU/hr, absurd;
  - a 1x "H100 SXM" offer on the same book priced 1.4911 -> $1.49/GPU/hr, the
    same order of magnitude as the 8x machine's per-GPU price;
  - `dph_total` == `dph_base` + `storage_total_cost` for the whole machine
    (19.20157 == 19.20009 + 0.00148).

`dph_total` is the all-in hourly ask (compute + default storage allocation),
which is what a renter actually pays and what the console displays. Bandwidth
is metered separately and is NOT included.

WHAT "SPOT" DOES AND DOES NOT MEAN HERE
---------------------------------------
This lane measures **on-demand ask prices for currently-rentable offers** —
the price at which you could start a machine right now. It is NOT Vast.ai's
interruptible "bid" tier. Every offer this query returns carries
`is_bid: false`, and passing `"type": "bid"` was verified to be silently
ignored by the endpoint (2026-08-02), so the interruptible book is simply not
observable through this call. Offers also carry a `min_bid` floor that is
typically far below `dph_total`; it is deliberately NOT collected, because
mixing a bid floor into an ask series would produce a number that is neither.

That distinction is recorded in the artifact as `sample_basis` so a downstream
article cannot cite this as "the spot/interruptible price" by accident. If the
interruptible tier is ever wanted, it belongs in a separate series with its own
`sample_basis`, not blended into this one.

THE 64-OFFER CAP AND WHY PARTITIONING IS ADAPTIVE
-------------------------------------------------
The endpoint silently caps results at 64 regardless of the requested `limit`
(`limit: 10000` returns 64; verified 2026-08-02). There is no pagination —
an `offset` key returns HTTP 400. Price-range partitioning via `dph_total`
bounds exists but leaks: a `{"lt": 0.35}` query returned rows whose response
`dph_total` was >= 0.35, so it is NOT a sound partition axis.

`num_gpus` IS sound, and it buys an exactness property worth stating plainly:

    within a fixed num_gpus bucket, ordering by dph_total ascending is
    EXACTLY ordering by per-GPU price ascending.

That is what makes truncation safe at the bottom of the book. When a query is
capped, the offers we lose are the EXPENSIVE tail, never the cheap end, so the
reported `min` (and the low quantiles) stay exact even for a truncated model.
`median`/`mean` do not — they are computed over a cheap-biased subset — which
is why `truncated` is recorded per model AND per history point.

Partitioning is adaptive because most models never need it: of 18 models
probed on 2026-08-02, 13 returned their complete book unpartitioned (H100 SXM
36, B200 24, L40S 35, A100 PCIE 56, ...) and only 5 hit the cap. So each model
is queried unpartitioned first and only re-queried per `num_gpus` bucket when
that first query came back at the cap. Trusting the unpartitioned result only
when it did NOT truncate is what makes this safe: the multi-GPU ordering trap
(an 8xH100 at $2/GPU sorting after a 1xH100 at $3/GPU) cannot bite when no
offers were dropped. Partitioned results are UNIONED with the unpartitioned
ones and deduped by offer id.

When partitioning fires, the bucket set is EXHAUSTIVE — every integer
1..16 plus a `{"gte": 17}` tail sweep. It has to be. The earlier design used a
sparse list of popular counts and leaned on the unpartitioned union to carry
the rest, which is exactly backwards: the unpartitioned page is the one that
truncated, and since dph_total ~= num_gpus x per-GPU price, ascending
truncation discards the HIGH-num_gpus offers first. Measured live on
2026-08-02, RTX 4090 had 11 rentable offers at counts 5/7/9/14 — the cheapest
at $0.3081/GPU — of which the sparse design captured one, while still
publishing `truncated: false`. `truncated` now means "the statistics are
computed over an incomplete sample" and is set both when any query caps AND
when the bucket specs cannot be proven to cover every num_gpus.

OUTPUT CONTRACT (research/market/gpu-spot.json)
-----------------------------------------------
    {
      "generated_at": "2026-08-02T05:12:00Z",
      "method_version": 1,
      "source": "vast.ai",
      "metric": "usd_per_gpu_hour",
      "price_basis": "dph_total / num_gpus",
      "sample_basis": "rentable on-demand ask prices (rentable=true, is_bid=false); ...",
      "stale": false,
      "history_fields": ["samples","min","p25","median","mean","max","truncated"],
      "snapshot": {
        "as_of": "2026-08-02T05:12:00Z",
        "models": {
          "H100 SXM": {
            "samples": 34, "min": 1.4911, "p25": 2.135, "median": 2.4,
            "mean": 2.5106, "max": 4.9689,
            "truncated": false, "partitioned": false,
            "by_num_gpus": {"1": 13, "2": 14, "4": 5, "8": 4},
            "stale": false, "as_of": "2026-08-02T05:12:00Z"
          }
        },
        "zero_offer_models": ["B300"],
        "dropped": {"total": 2, "by_reason": {"nonpositive_price": 2}},
        "requests": {"issued": 63, "failed": 0}
      },
      "history": [
        {"t": "2026-08-02T05:12:00Z", "method_version": 1,
         "models": {"H100 SXM": [34, 1.4911, 2.135, 2.4, 2.5106, 4.9689, false]}}
      ]
    }

History records use POSITIONAL arrays whose field order is documented by the
top-level `history_fields` key, and each record is serialized on ONE LINE while
the rest of the document stays indented. Both choices are measured, not
stylistic: at 18 models one record costs 2169 bytes fully indented vs 1075
bytes on one line, and a one-line record means an append shows up in git as a
single added line instead of a 200-line block. That matters beyond disk —
scheduled lanes publish through safe-push's auto-merged PR (rule 13), and a
one-line append is far less likely to conflict with a concurrent writer than a
large indented block.

`method_version` is stamped on every history record and MUST be bumped
whenever GPU_MODELS, NUM_GPU_BUCKETS, the sanity band, or the percentile
definition changes. A series nobody else publishes is only worth something if
a reader can distinguish a methodology change from a market move.

RETENTION
---------
`history` keeps the `--history-max` most recent records and drops the oldest
beyond that. Default 720 = 180 days at the lane's 4 runs/day.

Sized from a measured artifact, not a guess: with the shipped 18-model list a
one-line record is 1075 bytes and the snapshot is ~7 KB, so 720 records is
~0.78 MB. The bound being enforced is "the committed file stays under ~1 MB",
because this artifact is rewritten and committed 4x/day and also ships inside
the deployed dashboard image. Raise --history-max if you accept a larger file
(1460 records = 365 days = ~1.58 MB).

For multi-year retention the right extension is a daily rollup — collapse
records older than N days to one per day — which can be added without breaking
the contract because `history_fields` already pins the record shape. That is
deliberately NOT built yet: 180 days of 6-hourly prints is well past the point
where the series is useful, and an unused downsampler is just untested code.

FAILURE POLICY
--------------
Fail-soft per model, fail-loud in aggregate — the same shape as
fetch_market_quotes.py.

  - A model whose queries all fail carries its PREVIOUS snapshot entry forward
    marked `stale: true`, so a transient fault does not blank a row.
  - A model that returns HTTP 200 with an EMPTY body is NOT a failure. That is
    a real observation of no supply, and it is recorded in `zero_offer_models`
    rather than being carried forward as a stale price. Distinguishing these
    two matters: a curated `gpu_name` list fails silently when the upstream
    renames a model, and the only way to notice is to see the zero.
  - A model that returns offers of which EVERY ONE is rejected by the cleaning
    filters is a FAILURE, not zero supply. Those two shapes shared a bucket
    once, which meant a plausible upstream change (num_gpus serialized as a
    string) published "the RTX 5090 rental market has no supply" on a green
    run while ~300 machines were rentable. Zero supply now requires an
    actually-empty response; anything else carries forward stale and counts in
    `requests.failed`.
  - A carried-forward stale value is NEVER appended to `history`. Writing a
    stale number into a time series fabricates an observation that was never
    made. History records contain freshly-observed models only.
  - If ZERO models produced fresh data, that is an environment problem (IP
    block, 429 wall, dead endpoint), not per-model noise: the snapshot is
    written with everything carried forward and `stale: true`, no history
    record is appended, and the exit code is 1 so the lane goes red.

Usage:
  uv run python scripts/fetch_gpu_spot.py
  uv run python scripts/fetch_gpu_spot.py --dry-run
  uv run python scripts/fetch_gpu_spot.py --models "H100 SXM,B200"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "research" / "market" / "gpu-spot.json"

API_URL = "https://console.vast.ai/api/v0/bundles/"
USER_AGENT = "ai-research-arm/gpu-spot (+https://ara.guzus.xyz)"

# Bump whenever GPU_MODELS, NUM_GPU_BUCKETS, the sanity band, or the percentile
# definition changes. Stamped into every history record — see module docstring.
#
# v2 (2026-08-02, before the first scheduled run): the sample basis changed
# twice, both widening/narrowing what `min` is computed over, so records are
# not comparable across the bump.
#   * Bucket coverage went from a sparse hand-picked list to EVERY integer
#     1..16 plus a `{"gte": 17}` catch-all. The sparse list silently lost
#     whole num_gpus tiers on any model whose unpartitioned page hit the cap,
#     and because dph_total ~= num_gpus x per-GPU price, ascending truncation
#     drops HIGH-num_gpus offers first — exactly the ones the list omitted.
#     Measured live on 2026-08-02: RTX 4090 had 11 rentable offers at
#     out-of-bucket counts (5, 7, 9, 14) with a cheapest of $0.3081/GPU, and
#     the committed v1 artifact captured one of them.
#   * `is_bid` offers are now dropped, so `sample_basis` is enforced rather
#     than merely asserted.
METHOD_VERSION = 2

# Empirically observed 2026-08-02: the endpoint returns at most 64 offers no
# matter what `limit` asks for. A query returning exactly this many is assumed
# truncated. Override with --cap if upstream changes it.
DEFAULT_RESULT_CAP = 64

# Only consulted for a model whose unpartitioned query hit the cap. EVERY
# integer in 1..16, plus a `{"gte": NUM_GPU_TAIL_MIN}` catch-all, so the
# partitioned union is EXHAUSTIVE rather than a sample of popular counts.
#
# The previous sparse list (1,2,3,4,6,8,10,12,16) leaned on "offers with a
# count outside this list are still captured via the unpartitioned union" —
# which is false precisely when partitioning fires. The unpartitioned page is
# capped at 64 in ascending dph_total, and dph_total ~= num_gpus x per-GPU
# price, so the offers it truncates away are the HIGH-num_gpus ones: the very
# tiers the sparse list did not re-query. The result was a `min` that could be
# 2x wrong while the artifact still published `truncated: false`, and `min` is
# stamped into an append-only history series. Costs ~7 extra requests per
# capped model (~98/run vs ~63); still far under the ~180 the adaptive design
# exists to avoid.
NUM_GPU_BUCKETS = tuple(range(1, 17))
# Everything at or above this count is swept by one range query, so no offer
# can fall outside the union. `{"gte": N}` was confirmed accepted by the
# endpoint on 2026-08-02 (returned 0 rows for RTX 4090, i.e. the operator
# parses rather than errors).
NUM_GPU_TAIL_MIN = 17

# Curated list, pinned to names EMPIRICALLY CONFIRMED to return offers on
# 2026-08-02. The list is deliberately fixed rather than discovered per run: a
# time series must measure the same basket every period, or it is not a series.
# `A100X`, `GH200 SXM` and `MI300X` were probed and returned zero offers, so
# they are omitted rather than shipped as permanently-empty rows.
GPU_MODELS = (
    # Datacenter accelerators — the models that actually anchor capex arguments.
    "B200",
    "B300",
    "H200",
    "H200 NVL",
    "H100 SXM",
    "H100 NVL",
    "H100 PCIE",
    "A100 SXM4",
    "A100 PCIE",
    "L40S",
    "L40",
    # Workstation / prosumer — the cheap substitution margin.
    "RTX PRO 6000 S",
    "RTX PRO 6000 WS",
    "RTX 6000Ada",
    "RTX A6000",
    "RTX 5090",
    "RTX 4090",
    "RTX 3090",
)

# ABSOLUTE sanity band on per-GPU USD/hr. Deliberately NOT relative (no "drop
# anything above N x median"): a genuine price spike is the single most
# newsworthy event this series can capture, and a relative filter would eat
# exactly the observation worth publishing. These bounds only reject values
# that cannot be a real rental price.
MIN_SANE_USD_PER_GPU_HR = 0.001
MAX_SANE_USD_PER_GPU_HR = 100.0

DEFAULT_HISTORY_MAX = 720  # 180 days at 4 runs/day; ~0.78 MB. See RETENTION.
DEFAULT_TIMEOUT = 45
DEFAULT_SLEEP = 0.2
HTTP_ATTEMPTS = 3

HISTORY_FIELDS = ("samples", "min", "p25", "median", "mean", "max", "truncated")

# Stamped into the artifact so a reader cannot mistake this for Vast.ai's
# interruptible bid tier. See "WHAT 'SPOT' DOES AND DOES NOT MEAN HERE".
SAMPLE_BASIS = (
    "rentable on-demand ask prices (rentable=true, is_bid=false); "
    "excludes interruptible bid offers; includes default storage allocation, excludes bandwidth"
)


# --------------------------------------------------------------------------
# time
# --------------------------------------------------------------------------

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------
# statistics — one percentile definition for the whole file
# --------------------------------------------------------------------------

def percentile(sorted_values: list[float], q: float) -> float:
    """Linear-interpolation percentile (numpy's default 'linear' method).

    `q` in [0, 1]. `sorted_values` must be sorted ascending and non-empty.
    Median is just percentile(v, 0.5) so every quantile in the output shares
    one definition — mixing statistics.median with an interpolated p25 would
    make the two incomparable at small sample sizes.
    """
    if not sorted_values:
        raise ValueError("percentile of empty sequence")
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    pos = (len(sorted_values) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(sorted_values) - 1)
    frac = pos - lo
    return float(sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * frac)


def aggregate_prices(prices: Iterable[float]) -> dict[str, float | int]:
    """Distribution summary for one GPU model, at full precision.

    Rounding happens only at serialization — rounding here would compound
    through the mean.
    """
    values = sorted(float(p) for p in prices)
    if not values:
        raise ValueError("aggregate_prices requires at least one price")
    return {
        "samples": len(values),
        "min": values[0],
        "p25": percentile(values, 0.25),
        "median": percentile(values, 0.50),
        "mean": sum(values) / len(values),
        "max": values[-1],
    }


# --------------------------------------------------------------------------
# offer cleaning
# --------------------------------------------------------------------------

def per_gpu_price(offer: dict[str, Any]) -> float:
    """dph_total is for the WHOLE MACHINE — divide by num_gpus. See docstring."""
    return float(offer["dph_total"]) / float(offer["num_gpus"])


def clean_offers(
    offers: Iterable[Any],
    expected_gpu_name: str,
    seen_ids: set[Any],
    drops: dict[str, int],
) -> list[tuple[float, int]]:
    """Return [(per_gpu_price, num_gpus)] for offers that survive filtering.

    Every rejection is counted by reason in `drops` so the artifact can state
    how much of the raw book it discarded. `seen_ids` is mutated so an offer
    appearing in both the unpartitioned and a partitioned query counts once.

    Filters are structural (missing/non-numeric fields, non-positive counts or
    prices, wrong model, duplicate id) plus an ABSOLUTE price band. Nothing
    here is relative to the sample — see MIN_SANE/MAX_SANE.
    """
    kept: list[tuple[float, int]] = []
    for offer in offers:
        if not isinstance(offer, dict):
            drops["malformed_offer"] = drops.get("malformed_offer", 0) + 1
            continue

        offer_id = offer.get("id")
        if offer_id is not None:
            if offer_id in seen_ids:
                drops["duplicate_id"] = drops.get("duplicate_id", 0) + 1
                continue

        # `sample_basis` promises "rentable on-demand ask prices
        # (rentable=true, is_bid=false); excludes interruptible bid offers".
        # The query constrains only `rentable`, so without this the promise
        # was documentation. Every live row carries `is_bid` and `min_bid`
        # (checked 2026-08-02), so the endpoint plainly models both tiers: if
        # it ever bundles bid offers into a rentable response, their much
        # lower prices would blend into the ask series and drag `min` toward
        # the bid floor. Mirrors the defensive gpu_name check below.
        if offer.get("is_bid"):
            drops["is_bid"] = drops.get("is_bid", 0) + 1
            continue

        name = offer.get("gpu_name")
        if name != expected_gpu_name:
            # Defensive: the server filters on gpu_name, but a silent upstream
            # change must not let another model's prices into this model's row.
            drops["gpu_name_mismatch"] = drops.get("gpu_name_mismatch", 0) + 1
            continue

        raw_price = offer.get("dph_total")
        raw_count = offer.get("num_gpus")
        if not isinstance(raw_price, (int, float)) or isinstance(raw_price, bool):
            drops["missing_price"] = drops.get("missing_price", 0) + 1
            continue
        if not isinstance(raw_count, (int, float)) or isinstance(raw_count, bool):
            drops["missing_num_gpus"] = drops.get("missing_num_gpus", 0) + 1
            continue

        # Reject rather than truncate. int(2.7) == 2 would silently divide the
        # machine price by the wrong number — the exact off-by-num_gpus failure
        # this script exists to prevent. A fractional count means the upstream
        # shape changed and that must be visible, not absorbed.
        if float(raw_count) != int(float(raw_count)):
            drops["fractional_num_gpus"] = drops.get("fractional_num_gpus", 0) + 1
            continue
        count = int(raw_count)
        if count <= 0:
            drops["nonpositive_num_gpus"] = drops.get("nonpositive_num_gpus", 0) + 1
            continue
        if float(raw_price) <= 0:
            drops["nonpositive_price"] = drops.get("nonpositive_price", 0) + 1
            continue

        price = float(raw_price) / count
        if price != price or price in (float("inf"), float("-inf")):  # NaN / inf
            drops["non_finite_price"] = drops.get("non_finite_price", 0) + 1
            continue
        if not (MIN_SANE_USD_PER_GPU_HR <= price <= MAX_SANE_USD_PER_GPU_HR):
            drops["price_out_of_band"] = drops.get("price_out_of_band", 0) + 1
            continue

        if offer_id is not None:
            seen_ids.add(offer_id)
        kept.append((price, count))
    return kept


# --------------------------------------------------------------------------
# network boundary
# --------------------------------------------------------------------------

def build_query(
    gpu_name: str, num_gpus: int | dict[str, Any] | None, cap: int
) -> dict[str, Any]:
    """Ascending dph_total is load-bearing, not cosmetic — see module docstring.

    Within a fixed num_gpus bucket it orders by per-GPU price exactly, so a
    truncated response drops only the expensive tail and `min` stays exact.

    `num_gpus` is an int (exact bucket), a raw operator mapping such as
    `{"gte": 17}` for the tail sweep, or None for the unpartitioned page.
    """
    query: dict[str, Any] = {
        "rentable": {"eq": True},
        "gpu_name": {"eq": gpu_name},
        "limit": cap,
        "order": [["dph_total", "asc"]],
    }
    if isinstance(num_gpus, dict):
        query["num_gpus"] = dict(num_gpus)
    elif num_gpus is not None:
        query["num_gpus"] = {"eq": num_gpus}
    return query


def http_fetch(query: dict[str, Any], timeout: int = DEFAULT_TIMEOUT) -> list[Any]:
    """GET the marketplace endpoint. Raises on unrecoverable failure.

    Boundary code: retries 429 and 5xx with linear backoff, because an
    unauthenticated caller issuing ~60 requests per run is exactly the shape
    that gets rate-limited. 4xx other than 429 is not retried — it means the
    query is wrong, and retrying a wrong query just wastes the budget.
    """
    url = API_URL + "?" + urllib.parse.urlencode({"q": json.dumps(query)})
    request = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": USER_AGENT}
    )
    last_error: Exception | None = None
    for attempt in range(1, HTTP_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            offers = payload.get("offers")
            if not isinstance(offers, list):
                raise ValueError("response has no `offers` list")
            return offers
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code != 429 and exc.code < 500:
                raise
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
        if attempt < HTTP_ATTEMPTS:
            time.sleep(2 * attempt)
    # Not an assert: `python -O` strips asserts, and `raise None` would then
    # surface as a confusing TypeError instead of the real transport fault.
    if last_error is None:
        raise RuntimeError(f"{API_URL}: exhausted {HTTP_ATTEMPTS} attempts with no error recorded")
    raise last_error


# --------------------------------------------------------------------------
# per-model collection
# --------------------------------------------------------------------------

def collect_model(
    gpu_name: str,
    fetch: Callable[[dict[str, Any]], list[Any]],
    cap: int = DEFAULT_RESULT_CAP,
    sleep: float = 0.0,
    buckets: Iterable[int] = NUM_GPU_BUCKETS,
    tail_min: int | None = NUM_GPU_TAIL_MIN,
) -> dict[str, Any]:
    """Fetch one model's book, partitioning by num_gpus only if it truncated.

    Returns {samples, min, p25, median, mean, max, truncated, partitioned,
    by_num_gpus, raw_seen} or {"samples": 0, "raw_seen": N} when nothing
    survived. `raw_seen` lets the caller separate "the API returned an empty
    book" (real zero supply) from "the API returned N offers and every one
    failed a filter" (an upstream shape change masquerading as zero supply).
    Raises only when the model could not be observed at all — the caller
    decides fail-soft policy.

    `truncated` means "the published statistics are computed over an
    INCOMPLETE sample". It is set when any single query hit the cap, and also
    when the bucket specs do not provably cover every possible num_gpus — so
    `truncated: false` means what the docstring says rather than "the buckets
    we happened to ask for did not cap".
    """
    drops: dict[str, int] = {}
    seen_ids: set[Any] = set()
    raw_seen = 0

    raw = fetch(build_query(gpu_name, None, cap))
    raw_seen += len(raw)
    if len(raw) > cap:
        # The cap moved; our truncation detector is now wrong in the unsafe
        # direction (we would call a truncated book complete). Say so loudly.
        print(
            f"WARN {gpu_name}: query returned {len(raw)} offers, above the assumed "
            f"cap of {cap} — re-check DEFAULT_RESULT_CAP and bump METHOD_VERSION.",
            file=sys.stderr,
        )
    kept = clean_offers(raw, gpu_name, seen_ids, drops)
    partitioned = False
    truncated = False

    if len(raw) >= cap:
        # Unpartitioned result is truncated and, worse, mixes num_gpus values,
        # so ascending dph_total is NOT ascending per-GPU price. Re-query per
        # bucket, where that equivalence does hold, and union the results.
        partitioned = True
        bucket_list = sorted({int(c) for c in buckets})
        specs: list[int | dict[str, Any]] = list(bucket_list)
        if tail_min is not None:
            specs.append({"gte": int(tail_min)})
            # Exhaustive iff the exact buckets cover 1..tail_min-1 and the
            # tail sweeps everything at or above tail_min.
            exhaustive = set(bucket_list) >= set(range(1, int(tail_min)))
        else:
            exhaustive = False
        if not exhaustive:
            # Cannot prove the union covers every num_gpus, so the sample is
            # incomplete by construction. Say so rather than publishing a
            # confident `truncated: false` over a partial book.
            truncated = True
        for spec in specs:
            if sleep:
                time.sleep(sleep)
            bucket_raw = fetch(build_query(gpu_name, spec, cap))
            raw_seen += len(bucket_raw)
            if len(bucket_raw) >= cap:
                # This bucket (or the tail sweep) capped too — its own
                # expensive end is missing.
                truncated = True
            kept.extend(clean_offers(bucket_raw, gpu_name, seen_ids, drops))

    if not kept:
        return {"samples": 0, "raw_seen": raw_seen, "dropped": drops}

    by_num_gpus: dict[str, int] = {}
    for _price, count in kept:
        key = str(count)
        by_num_gpus[key] = by_num_gpus.get(key, 0) + 1

    stats = aggregate_prices(price for price, _count in kept)
    stats["truncated"] = truncated
    stats["partitioned"] = partitioned
    stats["by_num_gpus"] = {k: by_num_gpus[k] for k in sorted(by_num_gpus, key=int)}
    stats["dropped"] = drops
    stats["raw_seen"] = raw_seen
    return stats


# --------------------------------------------------------------------------
# payload assembly
# --------------------------------------------------------------------------

def _round(value: float) -> float:
    return round(float(value), 4)


def _render_model(stats: dict[str, Any], as_of: str) -> dict[str, Any]:
    return {
        "samples": stats["samples"],
        "min": _round(stats["min"]),
        "p25": _round(stats["p25"]),
        "median": _round(stats["median"]),
        "mean": _round(stats["mean"]),
        "max": _round(stats["max"]),
        "truncated": bool(stats["truncated"]),
        "partitioned": bool(stats["partitioned"]),
        "by_num_gpus": stats["by_num_gpus"],
        "stale": False,
        "as_of": as_of,
    }


def _history_record(fresh: dict[str, dict[str, Any]], timestamp: str) -> dict[str, Any]:
    """Positional per-model arrays ordered by HISTORY_FIELDS. Fresh models only.

    A carried-forward stale value must never land here — that would fabricate
    an observation the pipeline never made.
    """
    return {
        "t": timestamp,
        "method_version": METHOD_VERSION,
        "models": {
            name: [
                entry["samples"],
                entry["min"],
                entry["p25"],
                entry["median"],
                entry["mean"],
                entry["max"],
                entry["truncated"],
            ]
            for name, entry in sorted(fresh.items())
        },
    }


def load_previous(out_path: Path) -> dict[str, Any]:
    """Read the existing artifact. A corrupt/absent file is an empty start —
    never a crash, or one bad write would wedge the lane permanently."""
    try:
        data = json.loads(out_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


_COMPACT_PREFIX = "@@ARA_COMPACT@@"
# Matches one complete JSON string token that starts with the marker, honouring
# backslash escapes so it can never terminate early on an escaped quote.
_COMPACT_RE = re.compile(r'"' + re.escape(_COMPACT_PREFIX) + r'((?:[^"\\]|\\.)*)"')


class _CompactMarker:
    """Wraps a value that must serialize onto a single line."""

    __slots__ = ("payload",)

    def __init__(self, payload: Any) -> None:
        self.payload = payload


class _CompactEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, _CompactMarker):
            return _COMPACT_PREFIX + json.dumps(o.payload, separators=(",", ":"), sort_keys=True)
        return super().default(o)


def serialize(payload: dict[str, Any]) -> str:
    """Indented document, but each history record on one line. See docstring.

    Implemented by encoding each record as a marked JSON *string* and then
    unwrapping those strings back to raw JSON. The unwrap runs the matched
    token through json.loads, so escaping is handled by the JSON decoder rather
    than by the regex — the regex only has to find a complete string token.
    A round-trip test pins that serialize() -> json.loads() is the identity.
    """
    document = dict(payload)
    history = payload.get("history")
    if isinstance(history, list):
        document["history"] = [_CompactMarker(record) for record in history]

    text = json.dumps(document, indent=2, sort_keys=True, cls=_CompactEncoder)

    def _unwrap(match: "re.Match[str]") -> str:
        decoded = json.loads('"' + _COMPACT_PREFIX + match.group(1) + '"')
        return decoded[len(_COMPACT_PREFIX):]

    return _COMPACT_RE.sub(_unwrap, text) + "\n"


def write_atomic(out_path: Path, payload: dict[str, Any]) -> None:
    """Temp file in the SAME directory + os.replace (load-bearing rule 8).

    Serialization happens before the temp file is opened, so an unserializable
    payload cannot leave a partial file behind; any later failure unlinks the
    temp and leaves the previous artifact byte-for-byte intact. Same-directory
    placement keeps os.replace an atomic rename rather than a cross-device copy.
    """
    text = serialize(payload)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, out_path)
    except BaseException:
        try:
            tmp.unlink()
        except OSError:
            pass
        raise


def build_payload(
    fresh: dict[str, dict[str, Any]],
    carried: dict[str, dict[str, Any]],
    zero_offer_models: list[str],
    dropped: dict[str, int],
    requests_issued: int,
    requests_failed: int,
    previous_history: list[Any],
    now: datetime,
    history_max: int,
) -> dict[str, Any]:
    timestamp = _iso(now)
    models: dict[str, Any] = dict(sorted({**carried, **fresh}.items()))

    history = list(previous_history)
    if fresh:
        history.append(_history_record(fresh, timestamp))
    if history_max > 0 and len(history) > history_max:
        history = history[-history_max:]

    return {
        "generated_at": timestamp,
        "method_version": METHOD_VERSION,
        "source": "vast.ai",
        "source_url": API_URL,
        "metric": "usd_per_gpu_hour",
        "price_basis": "dph_total / num_gpus",
        "sample_basis": SAMPLE_BASIS,
        "stale": not fresh,
        "history_fields": list(HISTORY_FIELDS),
        "snapshot": {
            "as_of": timestamp,
            "models": models,
            "zero_offer_models": sorted(zero_offer_models),
            "dropped": {"total": sum(dropped.values()), "by_reason": dict(sorted(dropped.items()))},
            "requests": {"issued": requests_issued, "failed": requests_failed},
        },
        "history": history,
    }


# --------------------------------------------------------------------------
# run
# --------------------------------------------------------------------------

def run(
    models: Iterable[str],
    fetch: Callable[[dict[str, Any]], list[Any]],
    previous: dict[str, Any],
    now: datetime,
    cap: int = DEFAULT_RESULT_CAP,
    sleep: float = 0.0,
    history_max: int = DEFAULT_HISTORY_MAX,
) -> tuple[dict[str, Any], int]:
    """Collect every model and assemble the artifact. Returns (payload, exit_code).

    Pure with respect to IO except through `fetch`, so the whole failure matrix
    is testable offline.
    """
    model_list = list(models)  # materialize: `models` may be any iterable
    prev_snapshot = previous.get("snapshot") or {}
    prev_models = prev_snapshot.get("models") or {}
    prev_history = previous.get("history") or []
    if not isinstance(prev_history, list):
        prev_history = []

    timestamp = _iso(now)
    fresh: dict[str, dict[str, Any]] = {}
    carried: dict[str, dict[str, Any]] = {}
    zero_offer: list[str] = []
    dropped_total: dict[str, int] = {}
    failures: list[str] = []
    issued = 0
    failed = 0

    for name in model_list:
        if sleep:
            time.sleep(sleep)

        counting_fetch_calls = {"n": 0}

        def _counting(query: dict[str, Any]) -> list[Any]:
            counting_fetch_calls["n"] += 1
            return fetch(query)

        try:
            stats = collect_model(name, _counting, cap=cap, sleep=sleep)
        except Exception as exc:  # noqa: BLE001 — boundary: any fault is fail-soft
            issued += counting_fetch_calls["n"]
            failed += 1
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
            stale_prev = prev_models.get(name)
            if isinstance(stale_prev, dict):
                carried_entry = dict(stale_prev)
                carried_entry["stale"] = True
                carried[name] = carried_entry
            continue

        issued += counting_fetch_calls["n"]
        for reason, count in (stats.get("dropped") or {}).items():
            dropped_total[reason] = dropped_total.get(reason, 0) + count

        if stats["samples"] == 0:
            if stats.get("raw_seen"):
                # The API returned offers and EVERY one was rejected by the
                # cleaning filters. That is not an observation of zero supply,
                # it is an upstream shape change (e.g. num_gpus serialized as
                # a string) wearing zero supply's clothes — and publishing it
                # in `zero_offer_models` would assert that a live rental
                # market has no machines. The module docstring claims the zero
                # IS the detector for a renamed model, so the two must not
                # share a bucket. Fail-soft per model, same as an exception.
                failed += 1
                failures.append(
                    f"{name}: all {stats['raw_seen']} returned offer(s) were "
                    f"rejected by the cleaning filters "
                    f"({stats.get('dropped') or {}}) — treat as an upstream "
                    f"schema change, NOT as zero supply"
                )
                stale_prev = prev_models.get(name)
                if isinstance(stale_prev, dict):
                    carried_entry = dict(stale_prev)
                    carried_entry["stale"] = True
                    carried[name] = carried_entry
                continue
            # HTTP 200 with an empty book. A real observation of no supply —
            # NOT a failure, so it must not be carried forward as a price.
            zero_offer.append(name)
            continue

        fresh[name] = _render_model(stats, timestamp)

    for line in failures:
        print(f"WARN {line}", file=sys.stderr)

    print(
        f"{len(fresh)} fresh, {len(carried)} carried-stale, {len(zero_offer)} zero-supply, "
        f"{failed} failed, of {len(model_list)} model(s); "
        f"{issued} request(s), {sum(dropped_total.values())} offer(s) dropped"
    )

    payload = build_payload(
        fresh=fresh,
        carried=carried,
        zero_offer_models=zero_offer,
        dropped=dropped_total,
        requests_issued=issued,
        requests_failed=failed,
        previous_history=prev_history,
        now=now,
        history_max=history_max,
    )

    if not fresh:
        print(
            "ERROR: no model produced fresh data — treat as an environment problem "
            "(rate limit, IP block, endpoint change), not per-model noise. "
            "History preserved; no record appended.",
            file=sys.stderr,
        )
        return payload, 1
    return payload, 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--models",
        type=str,
        default="",
        help="Comma-separated gpu_name override (default: the curated GPU_MODELS list).",
    )
    parser.add_argument(
        "--history-max", type=int, default=DEFAULT_HISTORY_MAX,
        help=f"Keep this many most-recent history records (default {DEFAULT_HISTORY_MAX}; "
             "0 disables trimming and lets the file grow without bound).",
    )
    parser.add_argument("--cap", type=int, default=DEFAULT_RESULT_CAP,
                        help=f"Assumed server result cap (default {DEFAULT_RESULT_CAP}).")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--sleep", type=float, default=DEFAULT_SLEEP,
                        help="Seconds between requests; politeness for an unauthenticated API.")
    parser.add_argument("--dry-run", action="store_true", help="Print the payload; write nothing.")
    args = parser.parse_args(argv)

    models = [m.strip() for m in args.models.split(",") if m.strip()] if args.models else list(GPU_MODELS)
    if not models:
        print("ERROR: empty model list", file=sys.stderr)
        return 2

    def _fetch(query: dict[str, Any]) -> list[Any]:
        return http_fetch(query, timeout=args.timeout)

    payload, exit_code = run(
        models=models,
        fetch=_fetch,
        previous=load_previous(args.out),
        now=_utc_now(),
        cap=args.cap,
        sleep=args.sleep,
        history_max=args.history_max,
    )

    if args.dry_run:
        print(serialize(payload), end="")  # byte-identical to what would be written
        return exit_code

    write_atomic(args.out, payload)
    print(
        f"wrote {args.out} "
        f"({len(payload['snapshot']['models'])} model(s), {len(payload['history'])} history record(s))"
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
