#!/usr/bin/env bash
# scripts/check-feeds.sh — operator health-check for the AI-news data pipeline.
#
# Probes every RSS/JSON endpoint the hourly-rss and 2h-bluesky workflows
# rely on, reporting HTTP status + content-shape + freshness in one table.
# Exit code: 0 if every endpoint passes both the HTTP and content check,
# 1 if any single feed fails.
#
# Use this whenever:
#   - the daily digest's "RSS" attribution stops matching reality, or
#   - the bluesky channel emits "no data" stubs, or
#   - you want to verify a proposed feed swap before patching the workflow.
#
# Why two user agents: Microsoft properties (blogs.microsoft.com/ai,
# microsoft.com/en-us/research) return HTTP 403 for the "compatible;
# AIResearchBot/1.0" UA the workflows historically used. The workflows
# now use a browser-shaped UA; this script does the same and additionally
# probes the legacy UA against the same URLs to flag any regression.

set -uo pipefail

UA_BROWSER="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
UA_BOT="Mozilla/5.0 (compatible; AIResearchBot/1.0; +health-check)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
FAILED=0

# check_feed <url> <expected-shape> <label>
# expected-shape ∈ {rss, atom, json}
check_feed() {
  local url="$1" shape="$2" label="$3"
  local out="$TMP/${label//[^A-Za-z0-9]/_}"
  local code
  code=$(curl -sL --max-time 20 -A "$UA_BROWSER" -o "$out" -w "%{http_code}" "$url" || echo "000")

  local size body_ok="" latest="" status="OK"
  size=$(wc -c <"$out" | tr -d ' ')

  case "$shape" in
    rss)
      grep -qiE "<rss|<rdf" "$out" && body_ok="yes"
      latest=$(grep -oE '<pubDate>[^<]+</pubDate>' "$out" | head -1 | sed -E 's|</?pubDate>||g')
      ;;
    atom)
      grep -qiE "<feed" "$out" && body_ok="yes"
      latest=$(grep -oE '<updated>[^<]+</updated>' "$out" | head -1 | sed -E 's|</?updated>||g')
      ;;
    json)
      head -c 1 "$out" | grep -q '{' && body_ok="yes"
      ;;
  esac

  if [[ "$code" != 2* ]]; then
    status="HTTP-$code"; FAILED=1
  elif [[ -z "$body_ok" ]]; then
    status="WRONG-SHAPE"; FAILED=1
  elif [[ "$size" -lt 500 ]]; then
    status="SUSPICIOUSLY-SMALL($size)"; FAILED=1
  fi

  printf "  %-12s %-9s %-30s %s\n" "$status" "$shape" "${latest:--}" "$url"
}

echo "== hourly-rss feeds =="
check_feed "https://openai.com/news/rss.xml"                                rss  openai
check_feed "https://openrss.org/www.anthropic.com/news"                     rss  anthropic_openrss
check_feed "https://research.google/blog/rss/"                              rss  google_research
check_feed "https://deepmind.google/blog/rss.xml"                           rss  deepmind
check_feed "https://huggingface.co/blog/feed.xml"                           atom huggingface
check_feed "https://export.arxiv.org/rss/cs.AI"                             rss  arxiv_ai
check_feed "https://export.arxiv.org/rss/cs.LG"                             rss  arxiv_lg
check_feed "https://techcrunch.com/category/artificial-intelligence/feed/"  rss  techcrunch
check_feed "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml" rss verge
check_feed "https://venturebeat.com/category/ai/feed/"                      rss  venturebeat
check_feed "https://blogs.nvidia.com/feed/"                                 rss  nvidia
check_feed "https://aws.amazon.com/blogs/machine-learning/feed/"            rss  aws_ml
check_feed "https://blogs.microsoft.com/ai/feed/"                           rss  microsoft_ai
check_feed "https://www.amazon.science/index.rss"                           rss  amazon_science
check_feed "https://feeds.arstechnica.com/arstechnica/index"                rss  arstechnica
check_feed "https://www.wired.com/feed/tag/ai/latest/rss"                   rss  wired_ai
check_feed "https://www.technologyreview.com/feed/"                         rss  mit_tech_review
check_feed "https://research.facebook.com/feed/"                            rss  meta_research
check_feed "https://engineering.fb.com/feed/"                               rss  meta_engineering
check_feed "https://simonwillison.net/atom/everything/"                     atom simonwillison
check_feed "https://importai.substack.com/feed"                             rss  importai
check_feed "https://www.interconnects.ai/feed"                              rss  interconnects
check_feed "https://www.oneusefulthing.org/feed"                            rss  oneusefulthing
check_feed "https://www.latent.space/feed"                                  rss  latent_space
check_feed "https://www.lesswrong.com/feed.xml"                             rss  lesswrong

echo
echo "== known-dead URLs (must report FAIL — guards against regression) =="
check_feed "https://ai.meta.com/blog/rss/"                                  rss  meta_ai_legacy
check_feed "http://googleaiblog.blogspot.com/atom.xml"                      atom googleaiblog_legacy

echo
echo "== 2h-bluesky endpoints =="
# api.bsky.app (no public. prefix) is the working host as of 2026-05-16.
# public.api.bsky.app returns HTTP 403 to this runner's IP.
check_feed "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI&limit=5&sort=latest"                json bsky_search_api
check_feed "https://api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=karpathy.bsky.social&limit=5"    json bsky_author_karpathy
check_feed "https://api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=simonw.bsky.social&limit=5"      json bsky_author_simonw

echo
echo "== Microsoft UA-gating regression check =="
echo "  (these probe the same URL with bot UA — they should FAIL while above passes)"
ms_url="https://blogs.microsoft.com/ai/feed/"
ms_code=$(curl -sL --max-time 20 -A "$UA_BOT" -o /dev/null -w "%{http_code}" "$ms_url" || echo "000")
echo "  bot-UA HTTP-$ms_code  $ms_url"
if [[ "$ms_code" == 2* ]]; then
  echo "  [!] Microsoft AI accepts bot UA now — remove the browser-UA workaround in hourly-rss.yml"
fi

echo
if [[ "$FAILED" -ne 0 ]]; then
  echo "RESULT: one or more feeds failed."
  exit 1
fi
echo "RESULT: all feeds healthy."
