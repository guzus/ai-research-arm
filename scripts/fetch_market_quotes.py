#!/usr/bin/env python3
"""Refresh research/market/quotes.json for wiki entities that carry `market`.

The wiki stores market IDENTITY (ticker/exchange/symbol); prices are volatile
runtime data and live here instead, so a stale quote can never make a wiki page
stale. The dashboard reads this file once per session to put a price row in the
wiki hover card.

Symbols come from research/wiki/index.json, so this script has no list of its
own to drift: adding `market:` to an entity page and regenerating the index is
the only step needed to start quoting a new company.

Usage:
  uv run --extra stock python scripts/fetch_market_quotes.py
  uv run --extra stock python scripts/fetch_market_quotes.py --dry-run
  uv run --extra stock python scripts/fetch_market_quotes.py --max-age-hours 48

Output contract (research/market/quotes.json):

    {
      "generated_at": "2026-08-01T10:04:00Z",
      "quotes": {
        "NASDAQ:NVDA": {
          "symbol": "NASDAQ:NVDA", "ticker": "NVDA",
          "price": 200.75, "change": 3.91, "changePercent": 1.99,
          "currency": "USD", "marketState": "REGULAR"|null,
          "asOf": "2026-08-01T20:00:01Z", "source": "yahoo", "stale": false
        }
      }
    }

Keys are the wiki's `market.symbol`, so the dashboard joins on one field.

Failure policy is fail-soft per symbol and fail-loud in aggregate. A symbol that
cannot be refreshed keeps its previous entry marked `stale: true` (a known-old
price with an honest asOf beats a blank row); a symbol that has never been
fetched is simply absent. But if EVERY symbol fails, that is an environment
problem — a 429 wall, no network, a dead dependency — and exit 1 makes it
visible rather than silently publishing a fully stale file. Same reasoning as
postbuild-seo.mjs's all-social-cards-failed guard.

Change is computed from the last two daily closes rather than any provider
"previousClose" field: Yahoo exposes previousClose, chartPreviousClose and
fast_info.previous_close, and on 2026-08-01 those returned 195.04, 206.84 and
196.839 for the same ticker. Differencing the series we already fetched is
self-consistent and matches what a reader would compute by hand.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_INDEX = REPO_ROOT / "research" / "wiki" / "index.json"
DEFAULT_OUT = REPO_ROOT / "research" / "market" / "quotes.json"
DEFAULT_MAX_AGE_HOURS = 24


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_symbols(index_path: Path) -> list[dict[str, str]]:
    """Return [{symbol, ticker, provider}] for every entity carrying `market`.

    Deduplicated by symbol: two pages may legitimately reference one security.
    """
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read {index_path}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    seen: dict[str, dict[str, str]] = {}
    for page in data.get("pages") or []:
        market = page.get("market")
        if not isinstance(market, dict):
            continue
        symbol, ticker = market.get("symbol"), market.get("ticker")
        if not symbol or not ticker:
            continue
        seen.setdefault(symbol, {
            "symbol": symbol,
            "ticker": ticker,
            "provider": market.get("provider") or "yahoo",
        })
    return [seen[k] for k in sorted(seen)]


def _epoch_seconds(value: Any) -> int | None:
    """Normalize Yahoo timestamps across yfinance response versions.

    Older yfinance releases returned ``regularMarketTime`` as Unix seconds;
    yfinance 1.6 returns a pandas ``Timestamp``. Missing datetime-like values
    such as pandas ``NaT`` are treated as absent so the caller can use its
    existing current-time fallback.
    """
    if value is None:
        return None

    try:
        raw_seconds = value.timestamp() if hasattr(value, "timestamp") else value
        seconds = float(raw_seconds)
    except (TypeError, ValueError, OverflowError):
        return None

    if not math.isfinite(seconds):
        return None
    return int(seconds)


def _closes_via_yfinance(ticker: str) -> tuple[list[float], str, int | None, str | None]:
    import yfinance as yf  # local import — optional `stock` extra

    t = yf.Ticker(ticker)
    hist = t.history(period="5d", interval="1d", auto_adjust=False)
    if hist.empty:
        raise ValueError(f"yfinance returned empty history for {ticker}")
    closes = [float(c) for c in hist["Close"] if c == c]  # drop NaN
    if not closes:
        raise ValueError(f"yfinance returned no usable closes for {ticker}")
    meta = t.history_metadata or {}
    currency = str(meta.get("currency") or "USD")
    as_of = meta.get("regularMarketTime")
    market_state = meta.get("marketState")
    return closes, currency, _epoch_seconds(as_of), (str(market_state) if market_state else None)


def _closes_via_urllib(ticker: str) -> tuple[list[float], str, int | None, str | None]:
    """Fallback when the optional `stock` extra is not installed.

    Yahoo 429s this path from many IPs (see stock_prices.py) — that is exactly
    why it is the fallback and not the primary.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import stock_prices as sp  # type: ignore

    result = sp.fetch_chart(ticker, "5d", "1d")
    closes, _labels = sp.extract_series(result, "1d")
    if not closes:
        raise ValueError(f"no closes for {ticker}")
    meta = result.get("meta") or {}
    return (
        closes,
        str(meta.get("currency") or "USD"),
        meta.get("regularMarketTime"),
        (str(meta.get("marketState")) if meta.get("marketState") else None),
    )


def fetch_quote(entry: dict[str, str]) -> dict[str, Any]:
    """Fetch one symbol. Raises on failure; the caller decides fail-soft policy."""
    ticker = entry["ticker"]
    try:
        closes, currency, as_of_epoch, market_state = _closes_via_yfinance(ticker)
        source = "yahoo"
    except ImportError:
        closes, currency, as_of_epoch, market_state = _closes_via_urllib(ticker)
        source = "yahoo"

    price = round(closes[-1], 4)
    # A single close means no prior session to difference against — emit the
    # price with a null change rather than a fabricated 0.00 (+0.00%).
    if len(closes) >= 2 and closes[-2]:
        change = round(price - closes[-2], 4)
        change_percent = round((price - closes[-2]) / closes[-2] * 100, 4)
    else:
        change = None
        change_percent = None

    as_of = _iso(datetime.fromtimestamp(as_of_epoch, tz=timezone.utc)) if as_of_epoch else _iso(_utc_now())
    return {
        "symbol": entry["symbol"],
        "ticker": ticker,
        "price": price,
        "change": change,
        "changePercent": change_percent,
        "currency": currency,
        "marketState": market_state,
        "asOf": as_of,
        "source": source,
        "stale": False,
    }


def _load_previous(out_path: Path) -> dict[str, Any]:
    try:
        data = json.loads(out_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    quotes = data.get("quotes")
    return quotes if isinstance(quotes, dict) else {}


def _mark_stale(prev: dict[str, Any], max_age: timedelta, now: datetime) -> dict[str, Any] | None:
    """Carry a previous quote forward as stale, or drop it once it is too old.

    A price from an hour ago labelled as such is useful; one from last month
    presented next to a company name is misinformation.
    """
    as_of = prev.get("asOf")
    if not isinstance(as_of, str):
        return None
    try:
        parsed = datetime.strptime(as_of, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    if now - parsed > max_age:
        return None
    carried = dict(prev)
    carried["stale"] = True
    return carried


def write_atomic(out_path: Path, payload: dict[str, Any]) -> None:
    """Temp file in the same dir + os.replace (load-bearing rule 8): a
    half-written quotes.json must never reach the dashboard prebuild."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, out_path)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--index", type=Path, default=WIKI_INDEX)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--max-age-hours", type=int, default=DEFAULT_MAX_AGE_HOURS,
                    help="Drop a carried-forward stale quote older than this (default 24).")
    ap.add_argument("--dry-run", action="store_true", help="Print the payload; write nothing.")
    args = ap.parse_args(argv)

    entries = load_symbols(args.index)
    if not entries:
        print("No wiki entities carry `market` — nothing to quote.")
        return 0

    now = _utc_now()
    previous = _load_previous(args.out)
    max_age = timedelta(hours=args.max_age_hours)

    quotes: dict[str, Any] = {}
    failures: list[str] = []
    for entry in entries:
        symbol = entry["symbol"]
        try:
            quotes[symbol] = fetch_quote(entry)
        except Exception as exc:  # noqa: BLE001 — boundary: any provider fault is fail-soft
            failures.append(f"{symbol}: {type(exc).__name__}: {exc}")
            carried = _mark_stale(previous.get(symbol) or {}, max_age, now)
            if carried:
                quotes[symbol] = carried

    for line in failures:
        print(f"WARN {line}", file=sys.stderr)

    fresh = sum(1 for q in quotes.values() if not q.get("stale"))
    print(f"{fresh} fresh, {len(quotes) - fresh} carried-stale, {len(failures)} failed, of {len(entries)} symbol(s)")

    if fresh == 0:
        print(
            "ERROR: every symbol failed to refresh — treat as an environment problem "
            "(rate limit, network, missing `stock` extra), not per-symbol noise.",
            file=sys.stderr,
        )
        return 1

    payload = {"generated_at": _iso(now), "quotes": quotes}
    if args.dry_run:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    write_atomic(args.out, payload)
    print(f"wrote {args.out} ({len(quotes)} quote(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
