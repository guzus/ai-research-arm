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
import csv
import io
import json
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
# Stooq is the fallback when Yahoo rate-limits (which happens from residential
# / non-datacenter IPs more or less constantly). No API key, no rate-limit
# headaches, returns CSV with same daily/weekly/monthly granularity.
STOOQ_CSV = "https://stooq.com/q/d/l/"

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


def fetch_chart_yfinance(ticker: str, range_: str, interval: str) -> tuple[list[float], list[str]]:
    """Primary backend when yfinance is installed. Handles Yahoo's crumb-
    cookie dance and retries internally, so it works from residential
    IPs and self-hosted CI runners where the bare urllib path 429s."""
    import yfinance as yf  # local import — optional dependency

    t = yf.Ticker(ticker)
    hist = t.history(period=range_, interval=interval, auto_adjust=False)
    if hist.empty:
        raise ValueError(f"yfinance returned empty history for {ticker}")
    closes = [float(c) for c in hist["Close"] if c == c]  # drop NaN
    if not closes:
        raise ValueError(f"yfinance returned no usable closes for {ticker}")
    # Match the label format used by the urllib path so output is consistent.
    if interval.endswith("mo") or interval == "1wk":
        labels = [str(d.date())[:7] for d in hist.index]
    elif interval in ("1d", "5d"):
        labels = [str(d.date()) for d in hist.index]
    else:
        labels = [d.strftime("%Y-%m-%d %H:%M") for d in hist.index]
    # Trim to the same length as `closes` after NaN filtering.
    labels = labels[: len(closes)]
    return closes, labels


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


# Map our Yahoo-style range/interval to stooq's CSV params.
# Stooq wants explicit d1/d2 dates and a single-letter interval (d/w/m).
_INTERVAL_TO_STOOQ = {
    "1d": "d", "5d": "d",
    "1wk": "w",
    "1mo": "m", "3mo": "m",
}
_RANGE_TO_DAYS = {
    "1d": 1, "5d": 5,
    "1mo": 31, "3mo": 92, "6mo": 184,
    "1y": 366, "2y": 731, "5y": 1827, "10y": 3653,
    "ytd": -1,  # special: compute from Jan 1
    "max": 365 * 30,  # cap stooq pulls at 30y
}


def fetch_chart_stooq(ticker: str, range_: str, interval: str) -> tuple[list[float], list[str]]:
    """Fallback: pull daily/weekly/monthly close-only series from stooq's CSV.
    Returns (closes, x_labels) directly — no Yahoo-shaped envelope to unpack.

    Stooq tickers: US equities take a `.us` suffix and are lowercased.
    A bare ticker (no exchange suffix) is interpreted as a US equity here;
    callers passing non-US tickers should pass them already-suffixed.
    """
    interval_stooq = _INTERVAL_TO_STOOQ.get(interval)
    if interval_stooq is None:
        raise ValueError(
            f"stooq fallback doesn't support interval={interval} "
            f"(supported: {sorted(_INTERVAL_TO_STOOQ)})"
        )
    if "." not in ticker:
        stooq_symbol = f"{ticker.lower()}.us"
    else:
        stooq_symbol = ticker.lower()

    today = datetime.now(timezone.utc).date()
    if range_ == "ytd":
        d1 = today.replace(month=1, day=1)
    else:
        days = _RANGE_TO_DAYS.get(range_)
        if days is None:
            raise ValueError(
                f"stooq fallback doesn't support range={range_} "
                f"(supported: {sorted(_RANGE_TO_DAYS)})"
            )
        d1 = today - timedelta(days=days)
    url = (
        f"{STOOQ_CSV}?s={stooq_symbol}"
        f"&d1={d1.strftime('%Y%m%d')}"
        f"&d2={today.strftime('%Y%m%d')}"
        f"&i={interval_stooq}"
    )
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(req, timeout=15, context=_ssl_context()) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    if "<html" in text.lower() or "no data" in text.lower():
        raise ValueError(f"stooq returned no data for {stooq_symbol}")
    reader = csv.DictReader(io.StringIO(text))
    closes: list[float] = []
    labels: list[str] = []
    for row in reader:
        try:
            closes.append(float(row["Close"]))
        except (KeyError, ValueError):
            continue
        date_str = row.get("Date") or ""
        # Reformat to match Yahoo-style labels for monthly/weekly.
        if interval in ("1mo", "3mo") and len(date_str) >= 7:
            labels.append(date_str[:7])
        else:
            labels.append(date_str)
    if not closes:
        raise ValueError(f"stooq returned 0 usable rows for {stooq_symbol}")
    return closes, labels


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
        closes: list[float] = []
        ts_labels: list[str] = []
        source = None
        last_err: Exception | None = None

        # Backend chain: yfinance (handles Yahoo auth) → bare urllib Yahoo
        # → stooq CSV. Each backend's failure cascades to the next so the
        # script succeeds whenever ANY backend can reach a price source.
        backends: list[tuple[str, callable]] = []
        try:
            import yfinance  # noqa: F401
            backends.append(("yfinance", lambda: fetch_chart_yfinance(ticker, args.range_, args.interval)))
        except ImportError:
            pass
        backends.append(
            ("yahoo-urllib", lambda: extract_series(fetch_chart(ticker, args.range_, args.interval), args.interval)),
        )
        backends.append(
            ("stooq", lambda: fetch_chart_stooq(ticker, args.range_, args.interval)),
        )

        for name, call in backends:
            try:
                closes, ts_labels = call()
                source = name
                break
            except (urllib.error.URLError, ValueError, json.JSONDecodeError) as e:
                last_err = e
                print(f"stock_prices: {ticker}: {name} failed ({e})", file=sys.stderr)
                continue

        if source is None:
            msg = f"{ticker}: all backends failed (last: {last_err})"
            errors.append(msg)
            print(f"stock_prices: {msg}", file=sys.stderr)
            continue

        print(f"stock_prices: {ticker}: ok ({source}, {len(closes)} points)", file=sys.stderr)
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
