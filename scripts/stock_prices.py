#!/usr/bin/env python3
"""Fetch stock-price time series from Yahoo Finance for ara-line-chart.

Yahoo's chart endpoint is unauthenticated, no rate-limit headaches at
the volume gen-research produces (a handful of tickers per article).
The output is plain text designed to be dropped straight into the
data-* attributes of an `ara-line-chart` or `ara-sparkline` element —
no parsing, no jq, no fragile shell pipelines.

Usage:
  python3 scripts/stock_prices.py AAPL
  python3 scripts/stock_prices.py AAPL --range 6mo --interval 1d
  python3 scripts/stock_prices.py AAPL,MSFT --range 2y --interval 1mo
  python3 scripts/stock_prices.py BE --range 1y --interval 1wk --format html

Output formats:
  --format kv (default) — key:value lines, easy to copy into data-*:
        ticker_AAPL: 178.5,180.2,...,210.4
        ticker_MSFT: 412.1,418.6,...,460.2
        x_labels:    2025-05,2025-06,...,2026-05
        y_unit:      $

  --format html — a ready-to-paste <div class="ara-line-chart" ...>
        with all data-* attributes filled in. The agent can embed this
        directly in the article body.

  --format json — machine-readable; one object with `series` (dict),
        `x_labels` (list), `y_unit` (str), `errors` (list).

Errors are non-fatal: a missing ticker is logged to stderr and the
output for that ticker is omitted (empty string in JSON `errors`).
Mirrors the bird CLI's "fall back gracefully" pattern.

Valid ranges:    1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
Valid intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
(Yahoo enforces compatibility, e.g. intraday only for short ranges.)
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"

# Yahoo blocks the python-urllib UA. Pretend to be a browser.
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json,*/*",
}

# Fallback SSL roots for environments without certifi (mirrors
# research_search.py's pattern).
_SYSTEM_CA_PATHS = [
    "/etc/ssl/cert.pem",
    "/etc/ssl/certs/ca-certificates.crt",
    "/etc/pki/tls/certs/ca-bundle.crt",
]


def _ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    if not ctx.get_ca_certs():
        for path in _SYSTEM_CA_PATHS:
            try:
                ctx.load_verify_locations(cafile=path)
                break
            except (OSError, ssl.SSLError):
                continue
    return ctx


def fetch_chart(ticker: str, range_: str, interval: str) -> dict:
    """Hit Yahoo's chart endpoint and return the parsed payload.
    Raises urllib.error.URLError or ValueError on any failure."""
    url = f"{YAHOO_CHART.format(ticker=ticker)}?range={range_}&interval={interval}"
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(req, timeout=15, context=_ssl_context()) as resp:
        data = json.load(resp)
    chart = data.get("chart") or {}
    err = chart.get("error")
    if err:
        raise ValueError(f"Yahoo returned error for {ticker}: {err.get('description') or err}")
    results = chart.get("result") or []
    if not results:
        raise ValueError(f"Yahoo returned no results for {ticker}")
    return results[0]


def extract_series(result: dict, interval: str) -> tuple[list[float], list[str]]:
    """Pull (close-prices, x-labels) from a Yahoo chart result."""
    ts = result.get("timestamp") or []
    indicators = result.get("indicators") or {}
    quote = (indicators.get("quote") or [{}])[0]
    closes = quote.get("close") or []
    if not ts or not closes:
        raise ValueError("Yahoo result missing timestamp/close arrays")
    # Strip Nones (Yahoo holes on illiquid days) and align ts to closes.
    paired = [(t, c) for t, c in zip(ts, closes) if c is not None]
    if not paired:
        raise ValueError("all close prices are null")
    ts_clean, close_clean = zip(*paired)
    labels = [_label_for(t, interval) for t in ts_clean]
    return list(close_clean), labels


def _label_for(epoch: int, interval: str) -> str:
    dt = datetime.fromtimestamp(epoch, tz=timezone.utc)
    if interval.endswith("mo") or interval == "1wk":
        return dt.strftime("%Y-%m")
    if interval in ("1d", "5d"):
        return dt.strftime("%Y-%m-%d")
    return dt.strftime("%Y-%m-%d %H:%M")


def round_series(closes: list[float]) -> list[float]:
    """Round to 2 dp — keeps data-* attrs short without losing readability."""
    return [round(x, 2) for x in closes]


def emit_kv(series: dict[str, list[float]], labels: list[str], unit: str) -> str:
    lines = []
    for ticker, closes in series.items():
        lines.append(f"ticker_{ticker}: " + ",".join(str(x) for x in closes))
    lines.append("x_labels:    " + ",".join(labels))
    lines.append(f"y_unit:      {unit}")
    return "\n".join(lines) + "\n"


def emit_json(series: dict[str, list[float]], labels: list[str], unit: str, errors: list[str]) -> str:
    return json.dumps(
        {"series": series, "x_labels": labels, "y_unit": unit, "errors": errors},
        indent=2,
    ) + "\n"


def emit_html(series: dict[str, list[float]], labels: list[str], unit: str, title: str) -> str:
    if not series:
        return "<!-- stock_prices: no series fetched -->\n"
    attrs = [
        'class="ara-line-chart"',
        f'data-x-labels="{",".join(labels)}"',
        f'data-y-unit="{unit}"',
        f'data-title="{title}"',
    ]
    for i, (ticker, closes) in enumerate(list(series.items())[:4], start=1):
        attrs.append(f'data-series-{i}="{",".join(str(x) for x in closes)}"')
        attrs.append(f'data-series-{i}-label="{ticker}"')
    return f"<div {' '.join(attrs)}></div>\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "tickers",
        help="comma-separated ticker symbols (max 4 for ara-line-chart)",
    )
    p.add_argument(
        "--range",
        dest="range_",
        default="1y",
        help="Yahoo range: 1d 5d 1mo 3mo 6mo 1y 2y 5y 10y ytd max (default 1y)",
    )
    p.add_argument(
        "--interval",
        default="1mo",
        help="Yahoo interval: 1d 1wk 1mo etc. (default 1mo)",
    )
    p.add_argument(
        "--format",
        dest="fmt",
        default="kv",
        choices=("kv", "json", "html"),
        help="output format (default kv)",
    )
    p.add_argument(
        "--unit",
        default="$",
        help="y-axis unit symbol for the chart (default $)",
    )
    p.add_argument(
        "--title",
        default=None,
        help="chart title (default: '<tickers> close, <range>')",
    )
    args = p.parse_args(argv)

    tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    if not tickers:
        print("stock_prices: no tickers given", file=sys.stderr)
        return 2
    if len(tickers) > 4:
        print(
            f"stock_prices: ara-line-chart supports up to 4 series; "
            f"truncating from {len(tickers)} to 4",
            file=sys.stderr,
        )
        tickers = tickers[:4]

    series: dict[str, list[float]] = {}
    labels: list[str] = []
    errors: list[str] = []

    for ticker in tickers:
        try:
            result = fetch_chart(ticker, args.range_, args.interval)
            closes, ts_labels = extract_series(result, args.interval)
        except (urllib.error.URLError, ValueError, json.JSONDecodeError) as e:
            msg = f"{ticker}: {e}"
            errors.append(msg)
            print(f"stock_prices: {msg}", file=sys.stderr)
            continue
        series[ticker] = round_series(closes)
        # Use the longest label set as the chart's x-axis. Cheap heuristic;
        # for multi-series this picks the densest ticker which is usually
        # the correct alignment for Yahoo-aligned data.
        if len(ts_labels) > len(labels):
            labels = ts_labels

    if not series:
        print("stock_prices: all tickers failed to fetch", file=sys.stderr)
        return 1

    title = args.title or f"{','.join(series.keys())} close, {args.range_}"

    if args.fmt == "kv":
        sys.stdout.write(emit_kv(series, labels, args.unit))
    elif args.fmt == "json":
        sys.stdout.write(emit_json(series, labels, args.unit, errors))
    elif args.fmt == "html":
        sys.stdout.write(emit_html(series, labels, args.unit, title))
    return 0


if __name__ == "__main__":
    sys.exit(main())
