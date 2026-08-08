#!/usr/bin/env python3
"""Refresh research/market/model-pricing.json — price vs. capability, and the
Pareto frontier between them.

WHY THIS LANE EXISTS
--------------------
The digest already writes this comparison by hand, every day, in prose:
"50 on the Artificial Analysis Intelligence Index at $0.14/$0.27 per million
tokens", "GPT-5.4 at extra-high effort scored 51 ... at 12.5x the price".
Every one of those sentences is an unaudited join between two numbers the
pipeline never stored. Re-deriving them from prose on the next run is how a
"105x cheaper" claim ends up with no inputs behind it.

This lane stores the join instead. One artifact then feeds three consumers:
the dashboard chart, the digest's pricing paragraph, and — the part that
compounds — `type: "derived"` claim-ledger entries, which under load-bearing
rule 1 must carry `inputs`/`formula`/`result` and are recomputed by
`check_generative_research.py --audit-derived-claims`. A price ratio sourced
from this file is auditable; the same ratio scraped back out of yesterday's
prose is not.

THE SERIES IS THE POINT, NOT THE SNAPSHOT
------------------------------------------
A file holding only "now" answers "what is cheap today". The append-only
`history` answers the question actually worth asking: **what does a given
level of capability cost, and when did it get cheaper?** Each record stores
`frontier_price_at` — the cheapest USD/Mtok that buys a score at or above each
capability tier. Watch one tier across months and you are measuring capability
deflation directly, from primary sources, with no model in the loop.

SOURCES (both unauthenticated, both machine-readable, neither scraped)
---------------------------------------------------------------------
Price      OpenRouter  https://openrouter.ai/api/v1/models
           Public JSON, no key. `pricing.prompt` / `pricing.completion` are
           USD **per token** as strings; this lane multiplies by 1e6 to reach
           the USD/Mtok that every vendor pricing page quotes.

Capability Epoch AI    https://epoch.ai/data/benchmarks.csv
           Published under a **Creative Commons Attribution license** and
           carrying `mean_score` + `stderr` per (model, benchmark, run).
           `/data/` is not disallowed by their robots.txt (verified
           2026-08-07; only `/assets/`, `/inspect-viewer/` and the
           FrontierMath problem pages are). Attribution is stamped into the
           artifact as `capability_license` / `capability_attribution` so it
           survives into anything that republishes the numbers.

A NOTE ON THE SOURCE **NOT** USED, SO NOBODY RE-LITIGATES IT
-------------------------------------------------------------
Artificial Analysis is the obvious capability source and is deliberately not
used. Its homepage embeds ~26 models in plaintext, but the full dataset is
served from `/data/<hash>.txt` **encrypted**, with the key delivered
separately to the client — a technical protection measure. Decrypting it to
get the other few hundred models would be circumventing that, regardless of
what robots.txt allows, so this lane does not. Their sanctioned path is an API
key; if one is ever configured, add it as a *new* capability resolver rather
than reaching around the encryption.

The choice turned out better than the thing it replaced. A named benchmark
with an error bar ("GPQA diamond, 0.887 +/- 0.02") can be checked by a reader;
an opaque vendor composite ("intelligence 64.9") cannot.

THE CORRECTNESS DETAIL THAT MATTERS MOST: PRICE VARIANTS
---------------------------------------------------------
OpenRouter lists priced variants of the same model as separate rows:

    Claude Opus 4.7            $5.00 / $25.00  per Mtok
    Claude Opus 4.7 (Fast)    $30.00 / $150.00 per Mtok   <- 6x

Both normalize to the same model name. Joining a capability score to whichever
row happened to sort first would place the point at up to 6x its true price
and silently corrupt the entire frontier — the failure would look like a
plausible chart, which is the dangerous kind. So variants are resolved
explicitly: rows are grouped by base name (the part before ` (`), and the
canonical row is the **unparenthesized base tier** when one exists, falling
back to the cheapest priced variant only when it does not. The variant that
was actually used is recorded per model as `price_variant`, so a surprising
point can always be traced.

Free ($0) rows are excluded from canonical selection outright: a $0 promo tier
would dominate the Pareto frontier at every capability level and make the
chart useless.

THE OTHER ONE: SCORE VARIANTS
------------------------------
Epoch runs the same model at several reasoning efforts
(`gemini-3.6-flash_high` vs `..._low`) and sometimes several times. Averaging
across efforts conflates two different products; this lane reports the **best**
score the model achieved on the benchmark and records which
`id_model_version` produced it, plus the run count. "What can this model do,
at what list price" is the question the chart answers, so best-effort score
against base-tier price is the honest pairing — and recording the variant
keeps it checkable.

PARETO FRONTIER
---------------
Model M is on the frontier iff no other model N is at least as good AND at
least as cheap, with at least one of those strict:

    dominated(M) := exists N != M s.t.
        score(N) >= score(M) and price(N) <= price(M)
        and (score(N) > score(M) or price(N) < price(M))

Exact ties (same score, same price) therefore do NOT dominate each other, and
both stay on the frontier — dropping one arbitrarily would hide a real choice.

OUTPUT CONTRACT (research/market/model-pricing.json)
----------------------------------------------------
    {
      "generated_at": "2026-08-07T04:00:00Z",
      "method_version": 1,
      "stale": false,
      "benchmark": "GPQA diamond",
      "metric": "usd_per_mtok",
      "price_basis": "OpenRouter list price, base tier, USD per 1M tokens",
      "score_basis": "best mean_score across model versions and runs",
      "price_source": "openrouter", "price_source_url": "...",
      "capability_source": "epoch.ai", "capability_source_url": "...",
      "capability_license": "CC-BY", "capability_attribution": "...",
      "capability_stale": false,
      "benchmarks_available": {"GPQA diamond": 148, ...},
      "history_fields": [...],
      "snapshot": {
        "as_of": "...",
        "models": [
          {"key": "claudeopus5", "name": "Claude Opus 5", "vendor": "anthropic",
           "openrouter_id": "anthropic/claude-opus-5", "price_variant": null,
           "input_usd_per_mtok": 5.0, "output_usd_per_mtok": 25.0,
           "blended_usd_per_mtok": 10.0, "context_length": 1000000,
           "score": 0.887, "stderr": 0.02, "score_variant": "claude-opus-5_high",
           "runs": 3, "score_as_of": "2026-07-24", "pareto": true}
        ],
        "unscored": [ ... priced but no capability match ... ],
        "counts": {"priced": 378, "scored": 148, "plotted": 76, "pareto": 9}
      },
      "history": [ {"ts": "...", "benchmark": "...", "plotted": 76,
                    "pareto": 9, "best_score": 0.912, "cheapest_plotted": 0.27,
                    "frontier_price_at": {"0.5": 0.27, "0.6": 0.9, ...}} ]
    }

ARTIFACT SIZE BOUND
-------------------
This file is committed to git AND copied into the deployed image by
`prebuild.mjs` (research/market/ is in its COPY_DIRS), and the lane runs 4x a
day, so every byte is rewritten ~1,460 times a year. Measured at ~152 KB:

    models      ~76 rows, full detail          ~34 KB
    alternates  ~258 rows across 5 benchmarks  ~41 KB   (score-only; prices
                                                         are NOT duplicated)
    unscored    ~231 rows, 5 fields            ~30 KB
    history     1 line per run                 ~0.2 KB/record

`history` is the only part that grows, at ~0.2 KB per record, so
`--history-max 720` (~6 months at this cadence) bounds it near 145 KB and the
whole artifact stays under ~300 KB indefinitely once the series fills. Raising the cadence or the
alternate count means lowering `--history-max` to hold that. The bound is
stated here for the same reason `fetch_gpu_spot.py` states its ~1 MB one: a
file this shape grows silently, and git keeps every revision.

FAILURE POLICY
--------------
Price source unreachable      -> FAIL LOUD (exit 1). Previous artifact is
                                 carried forward with `stale: true` and NO
                                 history record is appended. A stale price
                                 must never enter the series.
Capability source unreachable -> FAIL SOFT. Prices publish with
                                 `capability_stale: true`, the chart degrades
                                 to a price-only list, and again no history
                                 record is appended (a frontier cannot be
                                 computed without scores, and a gap in the
                                 series is honest where a fabricated point is
                                 not).
Both unreachable              -> exit 1, previous artifact untouched on disk.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "research" / "market" / "model-pricing.json"
DEFAULT_ALIASES = REPO_ROOT / "data" / "sources" / "model_pricing_aliases.json"

PRICE_URL = "https://openrouter.ai/api/v1/models"
CAPABILITY_URL = "https://epoch.ai/data/benchmarks.csv"
CAPABILITY_ATTRIBUTION = (
    "Epoch AI, 'AI Benchmarking Hub', https://epoch.ai/data/ai-benchmarking-dashboard "
    "— used under a Creative Commons Attribution license."
)

# Bump when a definition below changes, so a methodology change is never
# mistaken for a market move. Same discipline as fetch_gpu_spot.py.
METHOD_VERSION = 1

DEFAULT_BENCHMARK = "GPQA diamond"

# Extra benchmarks published (score-only) so the chart can offer a selector.
# Ranked by how many models carry a score, so the alternates are the ones with
# enough coverage to make a frontier worth drawing.
DEFAULT_ALTERNATES = 5

# Capability tiers for the `frontier_price_at` series. Epoch scores are 0..1
# accuracies, so these are absolute score thresholds, not percentiles — a tier
# means the same thing in every record, which is what makes the series
# comparable across months.
# The top tier is deliberately set ABOVE the current best score, so it reads
# `null` until some model reaches it. "Not yet purchasable at any price" is a
# real and datable fact about the frontier; a tier ceiling that the field has
# already saturated would stop recording anything.
CAPABILITY_TIERS: tuple[float, ...] = (0.5, 0.6, 0.7, 0.8, 0.9, 0.95)

# Blended price assumes 3 input tokens per 1 output token — a common, and
# ARBITRARY, mix. It is published as a convenience column and is deliberately
# NOT the Pareto axis: a frontier that moves when you change an assumed ratio
# is not a frontier. Output price is the axis.
BLEND_INPUT_RATIO = 3.0

HISTORY_FIELDS: tuple[str, ...] = (
    "benchmark", "plotted", "pareto", "best_score", "cheapest_plotted", "frontier_price_at",
)

DEFAULT_HISTORY_MAX = 720  # 6h cadence -> ~6 months
DEFAULT_TIMEOUT = 60
USER_AGENT = "ara-model-pricing/1.0 (+https://github.com/guzus/ai-research-arm)"


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


_PAREN_RE = re.compile(r"\s*\([^)]*\)")


def strip_variant(name: str) -> str:
    """'Claude Opus 4.7 (Fast)' -> 'Claude Opus 4.7'."""
    return _PAREN_RE.sub("", name).strip()


def variant_of(name: str) -> Optional[str]:
    """'Claude Opus 4.7 (Fast)' -> 'Fast'; base tier -> None."""
    found = re.findall(r"\(([^)]*)\)", name)
    return found[-1].strip() if found else None


def norm_key(name: str) -> str:
    """Join key: vendor prefix dropped, variants stripped, punctuation removed.

    OpenRouter renders names as 'Anthropic: Claude Opus 5'; Epoch renders the
    same model as 'Claude Opus 5'. Splitting on ':' aligns them. Dots are kept
    because they carry the version ('4.5' must not collapse into '45').
    """
    base = strip_variant(name)
    if ":" in base:
        base = base.split(":", 1)[1]
    base = base.lower().strip()
    return re.sub(r"[^a-z0-9.]+", "", base)


def _to_float(value: Any) -> Optional[float]:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if out == out and out not in (float("inf"), float("-inf")) else None


# --------------------------------------------------------------------------
# fetch
# --------------------------------------------------------------------------

def http_get(url: str, timeout: int = DEFAULT_TIMEOUT) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
        return response.read()


def fetch_prices(timeout: int = DEFAULT_TIMEOUT) -> list[dict[str, Any]]:
    payload = json.loads(http_get(PRICE_URL, timeout=timeout).decode("utf-8"))
    data = payload.get("data")
    if not isinstance(data, list) or not data:
        raise ValueError("openrouter returned no models")
    return data


def fetch_capability_rows(timeout: int = DEFAULT_TIMEOUT) -> list[dict[str, str]]:
    raw = http_get(CAPABILITY_URL, timeout=timeout).decode("utf-8", errors="replace")
    rows = list(csv.DictReader(io.StringIO(raw)))
    if not rows:
        raise ValueError("epoch.ai returned no benchmark rows")
    return rows


# --------------------------------------------------------------------------
# transform: prices
# --------------------------------------------------------------------------

def build_price_index(models: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Group OpenRouter rows by normalized base name, pick one canonical row.

    Canonical = the unparenthesized base tier when present, else the cheapest
    priced variant. Free ($0) rows never win — see module docstring.
    """
    grouped: dict[str, list[dict[str, Any]]] = {}
    for model in models:
        name = model.get("name") or model.get("id") or ""
        pricing = model.get("pricing") or {}
        prompt = _to_float(pricing.get("prompt"))
        completion = _to_float(pricing.get("completion"))
        if not name or prompt is None or completion is None:
            continue
        if completion <= 0:  # free/zero tier — excluded from the frontier
            continue
        grouped.setdefault(norm_key(name), []).append(
            {
                "openrouter_id": model.get("id"),
                "name": strip_variant(name.split(":", 1)[-1].strip()),
                "price_variant": variant_of(name),
                "vendor": (model.get("id") or "/").split("/", 1)[0],
                "input_usd_per_mtok": round(prompt * 1e6, 6),
                "output_usd_per_mtok": round(completion * 1e6, 6),
                "context_length": model.get("context_length"),
            }
        )

    index: dict[str, dict[str, Any]] = {}
    for key, rows in grouped.items():
        base = [r for r in rows if r["price_variant"] is None]
        pool = base or rows
        chosen = min(pool, key=lambda r: (r["output_usd_per_mtok"], r["openrouter_id"] or ""))
        chosen = dict(chosen)
        chosen["blended_usd_per_mtok"] = round(
            (chosen["input_usd_per_mtok"] * BLEND_INPUT_RATIO + chosen["output_usd_per_mtok"])
            / (BLEND_INPUT_RATIO + 1.0),
            6,
        )
        chosen["variants_seen"] = len(rows)
        index[key] = chosen
    return index


# --------------------------------------------------------------------------
# transform: capability
# --------------------------------------------------------------------------

def build_capability_index(
    rows: Iterable[dict[str, str]], benchmark: str
) -> dict[str, dict[str, Any]]:
    """Best score per model on one benchmark, with the winning variant recorded."""
    best: dict[str, dict[str, Any]] = {}
    for row in rows:
        if (row.get("task") or "").strip() != benchmark:
            continue
        name = (row.get("Model") or "").strip()
        score = _to_float(row.get("mean_score"))
        if not name or score is None:
            continue
        key = norm_key(name)
        entry = best.get(key)
        if entry is None:
            entry = {
                "score": score,
                "stderr": _to_float(row.get("stderr")),
                "score_variant": (row.get("id_model_version") or "").strip() or None,
                "score_as_of": (row.get("Version release date") or "").strip() or None,
                "epoch_model": name,
                "organization": (row.get("Organization") or "").strip() or None,
                "runs": 1,
            }
            best[key] = entry
            continue
        entry["runs"] += 1
        if score > entry["score"]:
            entry.update(
                score=score,
                stderr=_to_float(row.get("stderr")),
                score_variant=(row.get("id_model_version") or "").strip() or None,
            )
    return best


def benchmark_counts(rows: Iterable[dict[str, str]]) -> dict[str, int]:
    """Distinct scored models per benchmark — drives the chart's selector."""
    seen: dict[str, set[str]] = {}
    for row in rows:
        task = (row.get("task") or "").strip()
        name = (row.get("Model") or "").strip()
        if task and name and _to_float(row.get("mean_score")) is not None:
            seen.setdefault(task, set()).add(name)
    return dict(sorted(((t, len(m)) for t, m in seen.items()), key=lambda kv: (-kv[1], kv[0])))


# --------------------------------------------------------------------------
# transform: join + frontier
# --------------------------------------------------------------------------

def build_alternates(
    rows: list[dict[str, str]],
    prices: dict[str, dict[str, Any]],
    aliases: dict[str, str],
    primary: str,
    limit: int,
) -> dict[str, list[dict[str, Any]]]:
    """Compact re-joins of the SAME price index against other benchmarks.

    The chart's benchmark selector needs more than one score axis, but the
    prices never change between them — so alternates carry only the fields a
    point needs to move (`score`, `stderr`, `pareto`) plus enough identity to
    label it. Duplicating the full price record per benchmark would multiply
    the artifact for no information gain.

    `history` is deliberately NOT computed for alternates: the series means
    "the price of capability", and capability has to mean ONE fixed thing for
    a number to be comparable across months. Mixing benchmarks into one series
    would make a methodology change look like a market move.
    """
    ranked = [task for task in benchmark_counts(rows) if task != primary][:limit]
    out: dict[str, list[dict[str, Any]]] = {}
    for task in ranked:
        plotted, _ = join_models(prices, build_capability_index(rows, task), aliases)
        if not plotted:
            continue
        mark_pareto(plotted)
        out[task] = [
            {
                "key": m["key"],
                "name": m["name"],
                "vendor": m["vendor"],
                "output_usd_per_mtok": m["output_usd_per_mtok"],
                "score": m["score"],
                "stderr": m["stderr"],
                "pareto": m["pareto"],
            }
            for m in plotted
        ]
    return out


def load_aliases(path: Path) -> dict[str, str]:
    """Manual epoch-name -> openrouter-name overrides for joins normalization misses."""
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    pairs = raw.get("aliases", raw) if isinstance(raw, dict) else {}
    return {norm_key(str(k)): norm_key(str(v)) for k, v in pairs.items()} if isinstance(pairs, dict) else {}


def join_models(
    prices: dict[str, dict[str, Any]],
    capability: dict[str, dict[str, Any]],
    aliases: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (plotted, unscored). Plotted rows carry both a price and a score."""
    plotted: list[dict[str, Any]] = []
    matched_price_keys: set[str] = set()

    for cap_key, cap in capability.items():
        price_key = cap_key if cap_key in prices else aliases.get(cap_key)
        price = prices.get(price_key) if price_key else None
        if price is None:
            continue
        matched_price_keys.add(price_key)  # type: ignore[arg-type]
        row = dict(price)
        row["key"] = price_key
        row.update(
            score=cap["score"],
            stderr=cap["stderr"],
            score_variant=cap["score_variant"],
            score_as_of=cap["score_as_of"],
            runs=cap["runs"],
            epoch_model=cap["epoch_model"],
        )
        plotted.append(row)

    # Priced but unscored models are a LOOKUP list ("what does model X cost"),
    # not chart input — nothing plots them, because a point needs both axes.
    # Carrying the full price record here cost 71 KB of a 208 KB artifact that
    # is committed to git and copied into the deployed image four times a day,
    # so only the fields that answer the lookup are kept.
    unscored = [
        {
            "key": key,
            "name": price["name"],
            "vendor": price["vendor"],
            "input_usd_per_mtok": price["input_usd_per_mtok"],
            "output_usd_per_mtok": price["output_usd_per_mtok"],
        }
        for key, price in prices.items()
        if key not in matched_price_keys
    ]
    plotted.sort(key=lambda r: (-r["score"], r["output_usd_per_mtok"]))
    unscored.sort(key=lambda r: r["output_usd_per_mtok"])
    return plotted, unscored


def mark_pareto(models: list[dict[str, Any]]) -> int:
    """Flag non-dominated (cheap, capable) models. Returns the frontier size.

    O(n^2) is deliberate: n is ~100, and the explicit predicate reads exactly
    like the definition in the docstring, which matters more here than speed.
    """
    count = 0
    for candidate in models:
        dominated = False
        for other in models:
            if other is candidate:
                continue
            at_least_as_good = (
                other["score"] >= candidate["score"]
                and other["output_usd_per_mtok"] <= candidate["output_usd_per_mtok"]
            )
            strictly_better = (
                other["score"] > candidate["score"]
                or other["output_usd_per_mtok"] < candidate["output_usd_per_mtok"]
            )
            if at_least_as_good and strictly_better:
                dominated = True
                break
        candidate["pareto"] = not dominated
        count += not dominated
    return count


def frontier_price_at(models: list[dict[str, Any]], tiers: Iterable[float]) -> dict[str, Any]:
    """Cheapest output $/Mtok that buys a score >= each tier. None when unreachable."""
    out: dict[str, Any] = {}
    for tier in tiers:
        qualifying = [m["output_usd_per_mtok"] for m in models if m["score"] >= tier]
        out[f"{tier:g}"] = min(qualifying) if qualifying else None
    return out


# --------------------------------------------------------------------------
# assemble
# --------------------------------------------------------------------------

def history_record(models: list[dict[str, Any]], benchmark: str, timestamp: str) -> dict[str, Any]:
    return {
        "ts": timestamp,
        "benchmark": benchmark,
        "plotted": len(models),
        "pareto": sum(1 for m in models if m.get("pareto")),
        "best_score": max((m["score"] for m in models), default=None),
        "cheapest_plotted": min((m["output_usd_per_mtok"] for m in models), default=None),
        "frontier_price_at": frontier_price_at(models, CAPABILITY_TIERS),
    }


def build_payload(
    plotted: list[dict[str, Any]],
    unscored: list[dict[str, Any]],
    benchmark: str,
    benchmarks: dict[str, int],
    priced_count: int,
    scored_count: int,
    capability_ok: bool,
    price_ok: bool,
    previous_history: list[Any],
    now: datetime,
    history_max: int,
    alternates: Optional[dict[str, list[dict[str, Any]]]] = None,
) -> dict[str, Any]:
    timestamp = _iso(now)
    history = list(previous_history)
    # A record is appended only when BOTH sources were live this run. A
    # frontier computed from carried-forward prices, or from no scores at all,
    # would be indistinguishable from a real market move later.
    if price_ok and capability_ok and plotted:
        history.append(history_record(plotted, benchmark, timestamp))
    if history_max > 0 and len(history) > history_max:
        history = history[-history_max:]

    return {
        "generated_at": timestamp,
        "method_version": METHOD_VERSION,
        "stale": not price_ok,
        "capability_stale": not capability_ok,
        "benchmark": benchmark,
        "metric": "usd_per_mtok",
        "price_basis": (
            "OpenRouter list price for the base (non-Fast, non-batch, non-free) tier, "
            "USD per 1,000,000 tokens; output price is the Pareto axis"
        ),
        "score_basis": (
            "best mean_score across the model's reasoning-effort variants and runs; "
            "the winning variant is recorded per model as score_variant"
        ),
        "blend_input_ratio": BLEND_INPUT_RATIO,
        "price_source": "openrouter",
        "price_source_url": PRICE_URL,
        "capability_source": "epoch.ai",
        "capability_source_url": CAPABILITY_URL,
        "capability_license": "CC-BY",
        "capability_attribution": CAPABILITY_ATTRIBUTION,
        "capability_tiers": list(CAPABILITY_TIERS),
        "benchmarks_available": benchmarks,
        "history_fields": list(HISTORY_FIELDS),
        "snapshot": {
            "as_of": timestamp,
            "models": plotted,
            "alternates": alternates or {},
            "unscored": unscored,
            "counts": {
                "priced": priced_count,
                "scored": scored_count,
                "plotted": len(plotted),
                "pareto": sum(1 for m in plotted if m.get("pareto")),
                "unscored": len(unscored),
            },
        },
        "history": history,
    }


# --------------------------------------------------------------------------
# serialize / write  (history records on one line — same contract as gpu-spot)
# --------------------------------------------------------------------------

_COMPACT_PREFIX = "@@ARA_COMPACT@@"
# Must consume a WHOLE JSON string token, escapes included: a lazy `(.*?)"`
# stops at the first escaped quote inside the record and truncates it.
_COMPACT_RE = re.compile(r'"' + re.escape(_COMPACT_PREFIX) + r'((?:[^"\\]|\\.)*)"')


class _CompactMarker:
    def __init__(self, payload: Any) -> None:
        self.payload = payload


class _CompactEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, _CompactMarker):
            return _COMPACT_PREFIX + json.dumps(o.payload, separators=(",", ":"), sort_keys=True)
        return super().default(o)


def serialize(payload: dict[str, Any]) -> str:
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
    """Temp file in the SAME directory + os.replace (load-bearing rule 8)."""
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


def load_previous(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


# --------------------------------------------------------------------------
# run
# --------------------------------------------------------------------------

def run(
    fetch_price: Callable[[], list[dict[str, Any]]],
    fetch_capability: Callable[[], list[dict[str, str]]],
    previous: dict[str, Any],
    now: datetime,
    benchmark: str = DEFAULT_BENCHMARK,
    aliases: Optional[dict[str, str]] = None,
    history_max: int = DEFAULT_HISTORY_MAX,
    alternate_limit: int = DEFAULT_ALTERNATES,
) -> tuple[dict[str, Any], int]:
    """Assemble the artifact. Pure except through the two fetch callables."""
    aliases = aliases or {}
    previous_history = previous.get("history")
    previous_history = previous_history if isinstance(previous_history, list) else []

    try:
        price_rows = fetch_price()
        prices = build_price_index(price_rows)
        price_ok = bool(prices)
    except (urllib.error.URLError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: price source failed: {exc}", file=sys.stderr)
        prices, price_ok = {}, False

    capability_rows: list[dict[str, str]] = []
    try:
        capability_rows = fetch_capability()
        capability = build_capability_index(capability_rows, benchmark)
        benchmarks = benchmark_counts(capability_rows)
        capability_ok = bool(capability)
        if not capability_ok:
            print(f"WARNING: no scores for benchmark {benchmark!r}", file=sys.stderr)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"WARNING: capability source failed (publishing price-only): {exc}", file=sys.stderr)
        capability, benchmarks, capability_ok = {}, {}, False

    if not price_ok:
        # Carry the previous artifact forward marked stale; never append history.
        if previous:
            carried = dict(previous)
            carried["generated_at"] = _iso(now)
            carried["stale"] = True
            return carried, 1
        return build_payload([], [], benchmark, benchmarks, 0, 0, capability_ok, False,
                             previous_history, now, history_max), 1

    plotted, unscored = join_models(prices, capability, aliases)
    if plotted:
        mark_pareto(plotted)

    alternates = (
        build_alternates(capability_rows, prices, aliases, benchmark, alternate_limit)
        if capability_ok and capability_rows
        else {}
    )

    payload = build_payload(
        plotted=plotted,
        unscored=unscored,
        benchmark=benchmark,
        benchmarks=benchmarks or (previous.get("benchmarks_available") or {}),
        priced_count=len(prices),
        scored_count=len(capability),
        capability_ok=capability_ok,
        price_ok=True,
        previous_history=previous_history,
        now=now,
        history_max=history_max,
        alternates=alternates,
    )
    # 0 = healthy. 3 = published, but degraded (prices are live, scores are
    # not) — the run still commits, because withholding a good price snapshot
    # over a missing score axis helps nobody. The caller distinguishes the two
    # so "degraded" is visible in the workflow rather than only in the JSON.
    return payload, (0 if capability_ok else 3)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--benchmark", default=DEFAULT_BENCHMARK,
                        help=f"Capability benchmark (default {DEFAULT_BENCHMARK!r}).")
    parser.add_argument("--aliases", type=Path, default=DEFAULT_ALIASES,
                        help="JSON map of epoch-name -> openrouter-name join overrides.")
    parser.add_argument("--history-max", type=int, default=DEFAULT_HISTORY_MAX,
                        help=f"Keep this many most-recent history records (default {DEFAULT_HISTORY_MAX}).")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--list-benchmarks", action="store_true",
                        help="Print available benchmarks with model counts, then exit.")
    parser.add_argument("--dry-run", action="store_true", help="Print the payload; write nothing.")
    args = parser.parse_args(argv)

    if args.list_benchmarks:
        for task, count in benchmark_counts(fetch_capability_rows(timeout=args.timeout)).items():
            print(f"{count:5d}  {task}")
        return 0

    payload, exit_code = run(
        fetch_price=lambda: fetch_prices(timeout=args.timeout),
        fetch_capability=lambda: fetch_capability_rows(timeout=args.timeout),
        previous=load_previous(args.out),
        now=_utc_now(),
        benchmark=args.benchmark,
        aliases=load_aliases(args.aliases),
        history_max=args.history_max,
    )

    if args.dry_run:
        print(serialize(payload), end="")
        return exit_code

    write_atomic(args.out, payload)
    counts = payload.get("snapshot", {}).get("counts", {})
    print(
        f"wrote {args.out} — {counts.get('plotted', 0)} plotted "
        f"({counts.get('pareto', 0)} on the frontier), "
        f"{counts.get('priced', 0)} priced, {counts.get('scored', 0)} scored, "
        f"{len(payload.get('history', []))} history record(s)"
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
