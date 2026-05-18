#!/usr/bin/env python3
"""Specialized search wrappers for primary-source research.

Used by generative-research.yml sub-agents that need to surface primary
sources (arXiv papers, SEC filings, peer-reviewed work, structured facts,
patents, prediction-market consensus, global news, non-English coverage)
rather than general-web results. Each backend returns a normalized
plain-text block that an LLM can read directly — no JSON parsing required
downstream.

Usage:
  research_search.py SOURCE "query" [--limit N] [--lang LANG]

  SOURCE = arxiv | edgar | crossref | semanticscholar | github
         | wikidata | uspto | jedec | predictionmarket | gdelt | nonenglish

  --lang only consumed by `nonenglish` (default: all non-English langs).
         Accepts ISO codes: zh, ja, ko, de, fr, es, ar, ru, pt, it.

Each backend is implemented with stdlib only (urllib + json + xml + html +
re) so the script has zero dependencies and works on any runner that has
Python 3.

Source guide (when to reach for each):
  arxiv            academic preprints; ML / physics / cs
  edgar            SEC filings; US public-company disclosures
  crossref         peer-reviewed DOIs; any discipline
  semanticscholar  paper search + abstracts; cross-discipline
  github           OSS repos by stars / activity
  wikidata         structured facts about entities (companies, people,
                   models); founding dates, HQs, parent orgs, CEOs
  uspto            US patents (via Google Patents JSON; the official
                   PatentsView API was retired in 2024-2025)
  jedec            JEDEC standards (JESD numbers) — best-effort surface
                   via Bing RSS; precision lower than API-backed sources
  predictionmarket Polymarket active-market consensus; implied YES prob
  gdelt            global news + sentiment; non-US coverage; multilingual
  nonenglish       non-English primary-source coverage via GDELT
                   sourcelang filter (deviation from earlier site-list
                   plan because DuckDuckGo HTML is blocked from our IPs;
                   GDELT covers the same intent more cleanly)
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Iterable

USER_AGENT = "ai-research-arm/1.0 (https://github.com/guzus/ai-research-arm)"
# SEC EDGAR's fair-access policy requires a UA that names the requester and
# includes contact info; the generic UA above earns a 403. Send an EDGAR-
# specific UA only on SEC requests.
# SEC enforces a "Sample Company Name AdminContact@sample.com" format —
# anything else gets 403'd as an "Undeclared Automated Tool".
EDGAR_UA = "ai-research-arm guzuseth@gmail.com"
# Some sources (Bing RSS, Google Patents XHR) reject the project UA; they
# want something that looks like a real browser. Use this UA only for
# scraping endpoints — keep the project UA elsewhere so source operators
# can identify us in their logs.
BROWSER_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
TIMEOUT = 20

# Build a single ssl.Context that finds CAs on Linux runners (default works)
# and on local macOS (default context lacks CAs — fall back to /etc/ssl/cert.pem,
# Homebrew's openssl bundles, or whatever SSL_CERT_FILE points at). Built once
# at import so all _fetch calls share it.
def _build_ssl_context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE")
    if cafile and os.path.isfile(cafile):
        return ssl.create_default_context(cafile=cafile)
    for p in (
        "/etc/ssl/cert.pem",                              # macOS system
        "/etc/ssl/certs/ca-certificates.crt",             # Debian / Ubuntu
        "/etc/pki/tls/certs/ca-bundle.crt",               # RHEL / Fedora
        "/opt/homebrew/etc/openssl@3/cert.pem",           # Homebrew arm64
        "/usr/local/etc/openssl@3/cert.pem",              # Homebrew intel
    ):
        if os.path.isfile(p):
            return ssl.create_default_context(cafile=p)
    return ssl.create_default_context()


SSL_CTX = _build_ssl_context()


def _fetch(url: str, accept: str = "application/json", extra_headers: dict | None = None) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": accept,
        **(extra_headers or {}),
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CTX) as resp:
        return resp.read()


def _block(idx: int, *lines: str) -> str:
    return "\n".join([f"[{idx}]"] + [l for l in lines if l]) + "\n"


def _strip_html(s: str) -> str:
    """Remove HTML tags and decode entities — Google Patents and Bing RSS both
    embed <b>highlight</b> tags and &hellip; entities in snippets. Cheap regex
    is fine for our display purpose; we never feed this back into a parser."""
    s = re.sub(r"<[^>]+>", "", s or "")
    s = html.unescape(s)
    return s.strip()


# ── arXiv ─────────────────────────────────────────────────────────
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def search_arxiv(query: str, limit: int, **_kw) -> Iterable[str]:
    params = urllib.parse.urlencode({
        "search_query": query,
        "max_results": str(limit),
        "sortBy": "relevance",
        "sortOrder": "descending",
    })
    url = f"http://export.arxiv.org/api/query?{params}"
    body = _fetch(url, accept="application/atom+xml")
    root = ET.fromstring(body)
    entries = root.findall("atom:entry", ATOM_NS)
    if not entries:
        yield "(arxiv) no results"
        return
    for i, e in enumerate(entries, 1):
        title = (e.findtext("atom:title", default="", namespaces=ATOM_NS) or "").strip().replace("\n", " ")
        summary = (e.findtext("atom:summary", default="", namespaces=ATOM_NS) or "").strip().replace("\n", " ")
        published = (e.findtext("atom:published", default="", namespaces=ATOM_NS) or "").strip()[:10]
        authors = ", ".join(
            (a.findtext("atom:name", default="", namespaces=ATOM_NS) or "").strip()
            for a in e.findall("atom:author", ATOM_NS)
        )
        link = ""
        for l in e.findall("atom:link", ATOM_NS):
            if l.get("rel") == "alternate":
                link = l.get("href") or ""
                break
        if not link:
            link = (e.findtext("atom:id", default="", namespaces=ATOM_NS) or "").strip()
        yield _block(
            i,
            f"Title: {title}",
            f"Authors: {authors}",
            f"Published: {published}",
            f"URL: {link}",
            f"Abstract: {summary[:600]}",
        )


# ── SEC EDGAR full-text ───────────────────────────────────────────
def search_edgar(query: str, limit: int, **_kw) -> Iterable[str]:
    params = urllib.parse.urlencode({"q": query, "forms": "10-K,10-Q,8-K,S-1,DEF 14A,13F-HR"})
    url = f"https://efts.sec.gov/LATEST/search-index?{params}"
    # SEC requires an identifying User-Agent — generic UA returns 403.
    req = urllib.request.Request(url, headers={
        "User-Agent": EDGAR_UA,
        "Accept": "application/json",
        "Accept-Encoding": "identity",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CTX) as resp:
        body = resp.read()
    data = json.loads(body)
    hits = (data.get("hits") or {}).get("hits", [])[:limit]
    if not hits:
        yield "(edgar) no results"
        return
    for i, h in enumerate(hits, 1):
        src = h.get("_source", {}) or {}
        accession = (h.get("_id") or "").split(":")[0].replace("-", "")
        cik = (src.get("ciks") or [""])[0]
        form = src.get("form", "")
        display_names = "; ".join(src.get("display_names") or [])
        filed = src.get("file_date", "")
        adsh = h.get("_id", "")
        # Build the canonical filing index URL
        url_idx = (
            f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type={form}"
            if cik else ""
        )
        url_doc = (
            f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{adsh.split(':',1)[-1]}"
            if cik and accession and ":" in adsh else ""
        )
        yield _block(
            i,
            f"Form: {form}",
            f"Filer: {display_names}",
            f"Filed: {filed}",
            f"CIK: {cik}",
            f"Filing page: {url_idx}",
            f"Document URL: {url_doc}",
        )


# ── Crossref ──────────────────────────────────────────────────────
def search_crossref(query: str, limit: int, **_kw) -> Iterable[str]:
    params = urllib.parse.urlencode({"query": query, "rows": str(limit)})
    url = f"https://api.crossref.org/works?{params}"
    body = _fetch(url)
    data = json.loads(body)
    items = ((data.get("message") or {}).get("items") or [])[:limit]
    if not items:
        yield "(crossref) no results"
        return
    for i, it in enumerate(items, 1):
        title = " ".join(it.get("title") or []).strip()
        authors = ", ".join(
            f"{a.get('given','')} {a.get('family','')}".strip()
            for a in (it.get("author") or [])[:5]
        )
        venue = " ".join(it.get("container-title") or [])
        year = ""
        for k in ("published-print", "published-online", "issued"):
            dp = (it.get(k) or {}).get("date-parts") or []
            if dp and dp[0]:
                year = str(dp[0][0])
                break
        url_doi = it.get("URL", "")
        yield _block(
            i,
            f"Title: {title}",
            f"Authors: {authors}",
            f"Venue: {venue}",
            f"Year: {year}",
            f"URL: {url_doi}",
        )


# ── Semantic Scholar ──────────────────────────────────────────────
def search_semanticscholar(query: str, limit: int, **_kw) -> Iterable[str]:
    fields = "title,authors,abstract,year,venue,url,externalIds"
    params = urllib.parse.urlencode({"query": query, "limit": str(limit), "fields": fields})
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?{params}"
    try:
        body = _fetch(url)
    except urllib.error.HTTPError as e:
        # Semantic Scholar rate-limits aggressively without an API key
        yield f"(semanticscholar) HTTP {e.code} — try again or use --limit smaller"
        return
    data = json.loads(body)
    items = data.get("data") or []
    if not items:
        yield "(semanticscholar) no results"
        return
    for i, it in enumerate(items, 1):
        title = (it.get("title") or "").strip()
        authors = ", ".join((a.get("name") or "") for a in (it.get("authors") or [])[:5])
        year = it.get("year", "")
        venue = it.get("venue", "")
        abstract = (it.get("abstract") or "").strip().replace("\n", " ")
        url_ss = it.get("url") or ""
        ext = it.get("externalIds") or {}
        doi = ext.get("DOI", "")
        arxiv_id = ext.get("ArXiv", "")
        yield _block(
            i,
            f"Title: {title}",
            f"Authors: {authors}",
            f"Year: {year}",
            f"Venue: {venue}",
            f"URL: {url_ss}",
            f"DOI: {doi}" if doi else "",
            f"arXiv: {arxiv_id}" if arxiv_id else "",
            f"Abstract: {abstract[:600]}",
        )


# ── GitHub code search (best-effort via public API) ───────────────
def search_github(query: str, limit: int, **_kw) -> Iterable[str]:
    # Public unauthenticated search has a 60 req/h limit per IP — usually
    # enough for one workflow run. The agent can fall back to the gh CLI
    # via Bash if it has GITHUB_TOKEN.
    params = urllib.parse.urlencode({"q": query, "per_page": str(min(limit, 30))})
    url = f"https://api.github.com/search/repositories?{params}"
    try:
        body = _fetch(url)
    except urllib.error.HTTPError as e:
        yield f"(github) HTTP {e.code} — likely unauthenticated rate-limit; use `gh search` instead"
        return
    data = json.loads(body)
    items = (data.get("items") or [])[:limit]
    if not items:
        yield "(github) no results"
        return
    for i, it in enumerate(items, 1):
        full_name = it.get("full_name", "")
        desc = (it.get("description") or "").strip()
        stars = it.get("stargazers_count", 0)
        lang = it.get("language", "")
        url_gh = it.get("html_url", "")
        updated = (it.get("updated_at") or "")[:10]
        yield _block(
            i,
            f"Repo: {full_name}",
            f"Stars: {stars}",
            f"Language: {lang}",
            f"Updated: {updated}",
            f"URL: {url_gh}",
            f"Description: {desc[:300]}",
        )


# ── Wikidata ──────────────────────────────────────────────────────
# Property IDs we surface from each candidate entity. Each tuple is
# (PID, display label). We resolve the value-side QIDs for a small
# allowlist (LABEL_RESOLVED_PIDS) so the output reads as labels
# instead of opaque Q-numbers. Dates and counts pass through raw.
WD_PROPS: list[tuple[str, str]] = [
    ("P31", "instance of"),
    ("P279", "subclass of"),
    ("P571", "founded"),
    ("P576", "dissolved"),
    ("P169", "CEO"),
    ("P112", "founded by"),
    ("P159", "HQ location"),
    ("P17", "country"),
    ("P856", "website"),
    ("P749", "parent org"),
    ("P452", "industry"),
    ("P1128", "employees"),
    ("P2139", "revenue"),
    ("P1448", "official name"),
    ("P361", "part of"),
]
# Only resolve QID → label for these PIDs (cap on N+1 fetches).
LABEL_RESOLVED_PIDS = {"P31", "P279", "P169", "P112", "P159", "P17",
                       "P749", "P452", "P361"}
WD_API = "https://www.wikidata.org/w/api.php"
WD_ENTITY = "https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"


def _wd_extract_value(claim: dict) -> tuple[str, bool]:
    """Return (rendered, is_qid). is_qid==True means caller should resolve label."""
    snak = (claim or {}).get("mainsnak") or {}
    if snak.get("snaktype") != "value":
        return "", False
    dv = (snak.get("datavalue") or {})
    val = dv.get("value")
    dtype = dv.get("type")
    if dtype == "wikibase-entityid" and isinstance(val, dict):
        qid = val.get("id") or ""
        return qid, True
    if dtype == "time" and isinstance(val, dict):
        # Wikidata times look like "+2003-08-30T00:00:00Z" — strip sign and time.
        t = (val.get("time") or "").lstrip("+")
        return t[:10], False
    if dtype == "quantity" and isinstance(val, dict):
        amt = (val.get("amount") or "").lstrip("+")
        return amt, False
    if dtype == "string":
        return str(val), False
    if dtype == "monolingualtext" and isinstance(val, dict):
        return val.get("text") or "", False
    if dtype == "globecoordinate" and isinstance(val, dict):
        lat = val.get("latitude")
        lon = val.get("longitude")
        return f"{lat},{lon}" if lat is not None and lon is not None else "", False
    if dtype == "url" or isinstance(val, str):
        return str(val), False
    return "", False


def _wd_resolve_labels(qids: list[str]) -> dict[str, str]:
    """Batch-resolve QID → label via wbgetentities (1 round-trip, props=labels)."""
    if not qids:
        return {}
    # API caps at 50 ids per call — we'll always have <40 anyway.
    params = urllib.parse.urlencode({
        "action": "wbgetentities",
        "ids": "|".join(qids[:50]),
        "props": "labels",
        "languages": "en",
        "format": "json",
    })
    try:
        body = _fetch(f"{WD_API}?{params}")
    except urllib.error.HTTPError:
        return {q: q for q in qids}
    out: dict[str, str] = {}
    data = json.loads(body)
    for qid, entity in (data.get("entities") or {}).items():
        label = (((entity.get("labels") or {}).get("en") or {}).get("value")) or qid
        out[qid] = label
    return out


def search_wikidata(query: str, limit: int, **_kw) -> Iterable[str]:
    # Step 1: wbsearchentities to find top candidates.
    n = min(max(1, limit), 5)  # capped — full entity fetch is heavy
    search_params = urllib.parse.urlencode({
        "action": "wbsearchentities",
        "search": query,
        "format": "json",
        "language": "en",
        "limit": str(n),
    })
    try:
        body = _fetch(f"{WD_API}?{search_params}")
    except urllib.error.HTTPError as e:
        yield f"(wikidata) HTTP {e.code} on entity search"
        return
    search_data = json.loads(body)
    candidates = search_data.get("search") or []
    if not candidates:
        yield "(wikidata) no results"
        return
    # Step 2: collect all QID values across all candidates that need labels,
    # then resolve them in one batch.
    pending_labels: set[str] = set()
    rendered: list[tuple[dict, dict[str, list[tuple[str, bool]]]]] = []
    for cand in candidates:
        qid = cand.get("id") or ""
        if not qid:
            continue
        try:
            ebody = _fetch(WD_ENTITY.format(qid=qid))
        except urllib.error.HTTPError:
            rendered.append((cand, {}))
            continue
        edata = json.loads(ebody)
        entity = ((edata.get("entities") or {}).get(qid) or {})
        claims = entity.get("claims") or {}
        prop_values: dict[str, list[tuple[str, bool]]] = {}
        for pid, _label in WD_PROPS:
            statements = claims.get(pid) or []
            vals: list[tuple[str, bool]] = []
            for st in statements[:3]:  # cap per property
                rendered_val, is_qid = _wd_extract_value(st)
                if not rendered_val:
                    continue
                vals.append((rendered_val, is_qid))
                if is_qid and pid in LABEL_RESOLVED_PIDS:
                    pending_labels.add(rendered_val)
            if vals:
                prop_values[pid] = vals
        rendered.append((cand, prop_values))
    # Step 3: batch-resolve labels.
    label_map = _wd_resolve_labels(sorted(pending_labels)) if pending_labels else {}
    # Step 4: emit blocks.
    for i, (cand, prop_values) in enumerate(rendered, 1):
        qid = cand.get("id") or ""
        cand_label = ((cand.get("display") or {}).get("label") or {}).get("value") or cand.get("label") or qid
        cand_desc = ((cand.get("display") or {}).get("description") or {}).get("value") or cand.get("description") or ""
        url_wd = f"https://www.wikidata.org/wiki/{qid}" if qid else ""
        lines = [
            f"Label: {cand_label}",
            f"QID: {qid}",
            f"Description: {cand_desc[:300]}",
            f"URL: {url_wd}",
        ]
        for pid, plabel in WD_PROPS:
            vals = prop_values.get(pid) or []
            if not vals:
                continue
            rendered_vals: list[str] = []
            for rendered_val, is_qid in vals:
                if is_qid and pid in LABEL_RESOLVED_PIDS:
                    rendered_vals.append(label_map.get(rendered_val, rendered_val))
                else:
                    rendered_vals.append(rendered_val)
            lines.append(f"{plabel} ({pid}): {'; '.join(rendered_vals)}")
        yield _block(i, *lines)


# ── USPTO (via Google Patents XHR JSON) ───────────────────────────
# The official PatentsView API (api.patentsview.org) was retired in
# 2024-2025 and now 301-redirects to a transition-guide page. The Google
# Patents XHR endpoint exposes the same underlying corpus as clean JSON
# and is what the patents.google.com SPA itself calls. We use it because
# (a) it works without auth, (b) the canonical viewer URL it implies is
# the human-friendly Google Patents page anyway.
GP_XHR = "https://patents.google.com/xhr/query"


def search_uspto(query: str, limit: int, **_kw) -> Iterable[str]:
    n = max(1, min(limit, 25))
    # The endpoint expects a URL-encoded `url` parameter whose VALUE is
    # itself a URL-encoded query string. Hence the double-encoding.
    inner = urllib.parse.urlencode({"q": query, "num": str(n)})
    params = urllib.parse.urlencode({"url": inner, "exp": ""})
    url = f"{GP_XHR}?{params}"
    try:
        body = _fetch(url, accept="application/json",
                      extra_headers={"User-Agent": BROWSER_UA})
    except urllib.error.HTTPError as e:
        # 503 typically = Google's "Sorry..." captcha page (anti-bot
        # rate limit); 429 = explicit rate limit. Surface both clearly
        # so the LLM caller knows to retry later or use arxiv instead.
        if e.code in (429, 503):
            yield (f"(uspto) HTTP {e.code} — Google Patents rate-limited "
                   "this IP; retry in a few minutes or use arxiv/crossref")
        else:
            yield f"(uspto) HTTP {e.code} — Google Patents XHR rejected request"
        return
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        # Google sometimes serves an HTML captcha page with 200 status.
        body_head = body[:80].decode("utf-8", errors="replace")
        if "<html" in body_head.lower():
            yield ("(uspto) HTML response from Google Patents — likely "
                   "captcha / rate-limit; retry in a few minutes")
        else:
            yield "(uspto) non-JSON response from Google Patents — endpoint may have changed"
        return
    clusters = (data.get("results") or {}).get("cluster") or []
    results = []
    for c in clusters:
        results.extend(c.get("result") or [])
    results = results[:n]
    if not results:
        yield "(uspto) no results"
        return
    for i, r in enumerate(results, 1):
        p = r.get("patent") or {}
        title = _strip_html(p.get("title") or "")
        snippet = _strip_html(p.get("snippet") or "")
        pubnum = p.get("publication_number") or ""
        assignee = p.get("assignee") or ""
        inventor = p.get("inventor") or ""
        pub_date = p.get("publication_date") or ""
        filing_date = p.get("filing_date") or ""
        grant_date = p.get("grant_date") or ""
        # Google Patents viewer URL — the most accessible viewer per task.
        url_p = f"https://patents.google.com/patent/{pubnum}" if pubnum else ""
        yield _block(
            i,
            f"Title: {title}",
            f"Patent: {pubnum}",
            f"Assignee: {assignee}",
            f"Inventor: {inventor}",
            f"Filed: {filing_date}",
            f"Granted: {grant_date}",
            f"Published: {pub_date}",
            f"URL: {url_p}",
            f"Snippet: {snippet[:400]}",
        )


# ── JEDEC (best-effort via Wikipedia full-text + Bing RSS fallback) ─
# Honest limits: jedec.org itself is Cloudflare-protected (403 on direct
# scrape) and Bing geo-routes our IP unpredictably. Wikipedia's full-text
# API reliably surfaces the JEDEC-standard articles a researcher would
# actually need (DDR generation pages, HBM generation pages, JESD index
# pages) with proper JESD-number citations baked into the text. We use
# Wikipedia as the primary path, then optionally augment with a Bing RSS
# pass when Wikipedia returns nothing useful. Lower precision than
# API-backed sources — flagged in docstring.
WP_API = "https://en.wikipedia.org/w/api.php"
BING_RSS = "https://www.bing.com/search"
JEDEC_HOST_RE = re.compile(r"(?:^|//)(?:www\.)?(jedec\.org)\b", re.IGNORECASE)
JESD_TITLE_RE = re.compile(r"\bJESD[\-\d]+\b|\bJEP\d+\b", re.IGNORECASE)


def _bing_rss(query: str, *, n: int = 15) -> list[dict]:
    """Hit Bing RSS, return parsed [{title, link, description, pubdate}, ...]
    Returns [] on soft-empty result. Raises HTTPError on hard failure."""
    params = urllib.parse.urlencode({
        "q": query,
        "format": "rss",
        "count": str(n),
        "setlang": "en-US",
        "mkt": "en-US",
        "cc": "US",
    })
    url = f"{BING_RSS}?{params}"
    body = _fetch(url, accept="application/rss+xml",
                  extra_headers={
                      "User-Agent": BROWSER_UA,
                      "Accept-Language": "en-US,en;q=0.9",
                  })
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return []
    items = []
    for item in root.iter("item"):
        items.append({
            "title": (item.findtext("title") or "").strip(),
            "link": (item.findtext("link") or "").strip(),
            "description": (item.findtext("description") or "").strip(),
            "pubdate": (item.findtext("pubDate") or "").strip(),
        })
    return items


def _wiki_search(query: str, *, n: int) -> list[dict]:
    """Wikipedia full-text search via api.php; returns search-result dicts.
    Raises HTTPError on hard failure."""
    params = urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": str(n),
    })
    body = _fetch(f"{WP_API}?{params}")
    data = json.loads(body)
    return (data.get("query") or {}).get("search") or []


def search_jedec(query: str, limit: int, **_kw) -> Iterable[str]:
    # Primary: Wikipedia full-text search for "JEDEC <query>". Wikipedia
    # articles cite JESD numbers and publication dates inline.
    enriched = f"JEDEC {query}" if "JEDEC" not in query.upper() else query
    wp_results: list[dict] = []
    try:
        wp_results = _wiki_search(enriched, n=max(limit, 5))
    except urllib.error.HTTPError as e:
        yield f"(jedec) Wikipedia HTTP {e.code}"
    counter = 0
    for r in wp_results[:limit]:
        title = r.get("title") or ""
        snippet = _strip_html(r.get("snippet") or "")
        url_w = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
        jesd_match = JESD_TITLE_RE.search(snippet) or JESD_TITLE_RE.search(title)
        jesd_tag = jesd_match.group(0) if jesd_match else ""
        counter += 1
        yield _block(
            counter,
            f"Title: {title}",
            f"URL: {url_w}",
            f"Source: en.wikipedia.org",
            f"Standard: {jesd_tag}" if jesd_tag else "",
            f"Updated: {(r.get('timestamp') or '')[:10]}",
            f"Snippet: {snippet[:400]}",
        )
    # Secondary: top up with Bing RSS hits whose URL is on jedec.org or
    # whose title carries a JESD code. Best-effort — Bing geo-routing may
    # return irrelevant pages; we filter aggressively before emitting.
    if counter < limit:
        try:
            bing_items = _bing_rss(f"{query} JESD", n=20)
        except urllib.error.HTTPError:
            bing_items = []
        for it in bing_items:
            if counter >= limit:
                break
            on_jedec = bool(JEDEC_HOST_RE.search(it["link"] or ""))
            jesd_match = JESD_TITLE_RE.search(it["title"] or "")
            if not (on_jedec or jesd_match):
                continue
            counter += 1
            yield _block(
                counter,
                f"Title: {_strip_html(it['title'])}",
                f"URL: {it['link']}",
                f"Source: {'jedec.org' if on_jedec else 'indexed-page'}",
                f"Standard: {jesd_match.group(0) if jesd_match else ''}",
                f"Date: {it['pubdate']}",
                f"Snippet: {_strip_html(it['description'])[:300]}",
            )
    if counter == 0:
        yield ("(jedec) no Wikipedia or Bing matches — JEDEC's site is "
               "Cloudflare-restricted; try a more specific JESD number")


# ── Prediction markets (Polymarket) ───────────────────────────────
# Originally specced to include Kalshi, but Kalshi's /events endpoint
# silently ignores `term=` filters (verified empirically) so we'd be
# returning unfiltered events. Polymarket's public-search endpoint
# returns events with markets, where each market carries outcomePrices
# as a JSON-string-in-JSON. Implied YES probability = first element.
POLY_SEARCH = "https://gamma-api.polymarket.com/public-search"


def search_predictionmarket(query: str, limit: int, **_kw) -> Iterable[str]:
    n = max(1, min(limit, 25))
    params = urllib.parse.urlencode({"q": query, "limit_per_type": str(n)})
    url = f"{POLY_SEARCH}?{params}"
    try:
        body = _fetch(url)
    except urllib.error.HTTPError as e:
        yield f"(predictionmarket) HTTP {e.code} from Polymarket"
        return
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        yield "(predictionmarket) non-JSON response from Polymarket"
        return
    events = data.get("events") or []
    if not events:
        yield "(predictionmarket) no Polymarket events for query"
        return
    emitted = 0
    for ev in events:
        if emitted >= n:
            break
        title = ev.get("title") or ev.get("question") or "?"
        slug = ev.get("slug") or ""
        url_ev = f"https://polymarket.com/event/{slug}" if slug else ""
        volume = ev.get("volume") or 0
        end_date = ev.get("endDate") or ""
        closed = ev.get("closed", False)
        markets = ev.get("markets") or []
        # If event has 1 binary market, render it inline; otherwise summarize
        # the top market and note count.
        if not markets:
            yield _block(
                emitted + 1,
                f"Event: {title}",
                f"URL: {url_ev}",
                f"Volume: ${volume:.0f}" if isinstance(volume, (int, float)) else f"Volume: {volume}",
                f"End: {end_date}",
                f"Status: {'closed' if closed else 'active'}",
                f"Markets: (none returned)",
            )
            emitted += 1
            continue
        # Render the primary market.
        m = markets[0]
        m_question = m.get("question") or title
        outcomes_raw = m.get("outcomes") or "[]"
        prices_raw = m.get("outcomePrices") or "[]"
        try:
            outcomes = json.loads(outcomes_raw) if isinstance(outcomes_raw, str) else (outcomes_raw or [])
            prices = json.loads(prices_raw) if isinstance(prices_raw, str) else (prices_raw or [])
        except (json.JSONDecodeError, TypeError):
            outcomes, prices = [], []
        implied = ""
        if prices:
            try:
                implied = f"{float(prices[0]) * 100:.1f}%"
            except (ValueError, TypeError):
                implied = ""
        price_lines = []
        for o, p in zip(outcomes, prices):
            try:
                price_lines.append(f"{o}={float(p):.3f}")
            except (ValueError, TypeError):
                price_lines.append(f"{o}={p}")
        prices_str = "; ".join(price_lines)
        m_volume = m.get("volume") or 0
        more = f" (+{len(markets)-1} more markets)" if len(markets) > 1 else ""
        yield _block(
            emitted + 1,
            f"Question: {m_question}{more}",
            f"URL: {url_ev}",
            f"Implied YES: {implied}" if implied else "",
            f"Prices: {prices_str}" if prices_str else "",
            f"Volume: ${float(m_volume):.0f}" if isinstance(m_volume, (int, float, str)) and str(m_volume).replace('.','').isdigit() else f"Volume: {m_volume}",
            f"End: {m.get('endDate') or end_date}",
            f"Status: {'closed' if m.get('closed') or closed else 'active'}",
        )
        emitted += 1


# ── GDELT 2.0 DocAPI ──────────────────────────────────────────────
# GDELT can return HTTP 200 with a plain-text error body (`"Your search
# contained a keyword that was too short."`, `Please limit requests to
# one every 5 seconds...`, etc.) — JSON parsing those is fatal. We probe
# for `{` before parsing and return the raw text as the per-source error.
GDELT_DOC = "https://api.gdeltproject.org/api/v2/doc/doc"


def _gdelt_call(query: str, *, n: int, sort: str = "hybridrel") -> tuple[list[dict] | None, str]:
    """Return (articles, raw_error_text). Articles None means error."""
    params = urllib.parse.urlencode({
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": str(n),
        "sort": sort,
    })
    url = f"{GDELT_DOC}?{params}"
    try:
        body = _fetch(url)
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8", errors="replace").strip()
        except Exception:  # noqa: BLE001
            err_body = ""
        return None, f"HTTP {e.code}: {err_body[:200]}"
    text = body.decode("utf-8", errors="replace").strip()
    # GDELT returns plain text for short-query / rate-limit errors with 200.
    if not text.startswith("{"):
        return None, text[:200]
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None, "non-JSON body"
    return data.get("articles") or [], ""


def search_gdelt(query: str, limit: int, **_kw) -> Iterable[str]:
    n = max(1, min(limit, 50))
    articles, err = _gdelt_call(query, n=n)
    if articles is None:
        yield f"(gdelt) {err}"
        return
    if not articles:
        yield "(gdelt) no results"
        return
    for i, a in enumerate(articles, 1):
        seendate = a.get("seendate") or ""
        # GDELT timestamps look like "20260518T013000Z" — display YYYY-MM-DD.
        if len(seendate) >= 8 and seendate[:8].isdigit():
            seendate = f"{seendate[:4]}-{seendate[4:6]}-{seendate[6:8]}"
        yield _block(
            i,
            f"Title: {a.get('title','')}",
            f"URL: {a.get('url','')}",
            f"Source: {a.get('domain','')}",
            f"Country: {a.get('sourcecountry','')}",
            f"Language: {a.get('language','')}",
            f"Date: {seendate}",
        )


# ── Non-English coverage (via GDELT sourcelang filter) ────────────
# Deviation from the original DDG-with-site-list spec: DuckDuckGo HTML
# is captcha-walled from our runners and Bing strips `site:` for the
# specific outlets the spec named (caixin.com, nikkei.com, etc.). GDELT's
# `sourcelang:<Language>` operator covers the same intent cleanly and
# returns URL + language + country in one shot. The downstream LLM agent
# uses WebFetch with a translation prompt as the task already anticipated.
# Lower precision when the language has few daily articles indexed.
LANG_MAP = {
    "zh": "chinese", "ja": "japanese", "ko": "korean",
    "de": "german", "fr": "french", "es": "spanish",
    "ar": "arabic", "ru": "russian", "pt": "portuguese",
    "it": "italian",
}
# When --lang not specified, scan a default set of high-priority langs.
DEFAULT_NONENG_LANGS = ("chinese", "japanese", "korean", "german", "french")


def search_nonenglish(query: str, limit: int, lang: str | None = None, **_kw) -> Iterable[str]:
    if lang:
        normalized = LANG_MAP.get(lang.lower(), lang.lower())
        langs = [normalized]
    else:
        langs = list(DEFAULT_NONENG_LANGS)
    n_per_lang = max(2, limit // max(1, len(langs)))
    emitted = 0
    counter = 0
    seen_urls: set[str] = set()
    lang_status: list[str] = []  # per-lang summary appended at end
    for idx, lng in enumerate(langs):
        if emitted >= limit:
            lang_status.append(f"{lng}: skipped (limit reached)")
            continue
        gdelt_query = f"{query} sourcelang:{lng}"
        articles, err = _gdelt_call(gdelt_query, n=n_per_lang, sort="DateDesc")
        # Be polite to GDELT — it 429s after one query/5sec. Skip the
        # sleep on the final iteration (caller doesn't need to wait).
        if idx < len(langs) - 1:
            time.sleep(5.2)
        if articles is None:
            lang_status.append(f"{lng}: error — {err[:80]}")
            continue
        if not articles:
            lang_status.append(f"{lng}: 0 articles indexed")
            continue
        lang_count = 0
        for a in articles:
            if emitted >= limit:
                break
            url = a.get("url") or ""
            if url in seen_urls:
                continue
            seen_urls.add(url)
            seendate = a.get("seendate") or ""
            if len(seendate) >= 8 and seendate[:8].isdigit():
                seendate = f"{seendate[:4]}-{seendate[4:6]}-{seendate[6:8]}"
            counter += 1
            lang_count += 1
            yield _block(
                counter,
                f"Title: {a.get('title','')}",
                f"URL: {url}",
                f"Source: {a.get('domain','')}",
                f"Country: {a.get('sourcecountry','')}",
                f"Language: {a.get('language','') or lng}",
                f"Date: {seendate}",
                "Note: original-language snippet; use WebFetch + translation prompt to read body",
            )
            emitted += 1
        lang_status.append(f"{lng}: {lang_count} returned")
    # Always emit a per-lang summary so the LLM caller can see whether
    # silence means "no index coverage" vs. "we got rate-limited".
    yield "(nonenglish) coverage: " + "; ".join(lang_status)
    if emitted == 0:
        yield ("(nonenglish) no articles across queried languages — "
               "GDELT's non-English index is sparse for some topics")


# ── Dispatch ──────────────────────────────────────────────────────
BACKENDS = {
    "arxiv": search_arxiv,
    "edgar": search_edgar,
    "crossref": search_crossref,
    "semanticscholar": search_semanticscholar,
    "ss": search_semanticscholar,
    "github": search_github,
    "gh": search_github,
    "wikidata": search_wikidata,
    "wd": search_wikidata,
    "uspto": search_uspto,
    "patents": search_uspto,
    "jedec": search_jedec,
    "predictionmarket": search_predictionmarket,
    "polymarket": search_predictionmarket,
    "pm": search_predictionmarket,
    "gdelt": search_gdelt,
    "nonenglish": search_nonenglish,
    "noneng": search_nonenglish,
}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", choices=sorted(BACKENDS.keys()))
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--lang", default=None,
                   help="ISO lang code for nonenglish (zh, ja, ko, de, ...); "
                        "ignored by other sources")
    args = p.parse_args(argv)
    fn = BACKENDS[args.source]
    print(f"# {args.source} search: {args.query} (top {args.limit})\n")
    extra: dict = {}
    if args.lang:
        extra["lang"] = args.lang
    try:
        for chunk in fn(args.query, args.limit, **extra):
            print(chunk)
    except urllib.error.URLError as e:
        print(f"ERROR: network failure: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
