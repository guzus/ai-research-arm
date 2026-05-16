#!/usr/bin/env python3
"""Specialized search wrappers for primary-source research.

Used by generative-research.yml sub-agents that need to surface primary
sources (arXiv papers, SEC filings, peer-reviewed work) rather than
general-web results. Each backend returns a normalized plain-text block
that an LLM can read directly — no JSON parsing required downstream.

Usage:
  research_search.py SOURCE "query" [--limit N]

  SOURCE = arxiv | edgar | crossref | semanticscholar | github

Each backend is implemented with stdlib only (urllib + json + xml) so the
script has zero dependencies and works on any runner that has Python 3.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
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


# ── arXiv ─────────────────────────────────────────────────────────
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def search_arxiv(query: str, limit: int) -> Iterable[str]:
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
def search_edgar(query: str, limit: int) -> Iterable[str]:
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
def search_crossref(query: str, limit: int) -> Iterable[str]:
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
def search_semanticscholar(query: str, limit: int) -> Iterable[str]:
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
def search_github(query: str, limit: int) -> Iterable[str]:
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


# ── Dispatch ──────────────────────────────────────────────────────
BACKENDS = {
    "arxiv": search_arxiv,
    "edgar": search_edgar,
    "crossref": search_crossref,
    "semanticscholar": search_semanticscholar,
    "ss": search_semanticscholar,
    "github": search_github,
    "gh": search_github,
}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", choices=sorted(BACKENDS.keys()))
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    args = p.parse_args(argv)
    fn = BACKENDS[args.source]
    print(f"# {args.source} search: {args.query} (top {args.limit})\n")
    try:
        for chunk in fn(args.query, args.limit):
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
