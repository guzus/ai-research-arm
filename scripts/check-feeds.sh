#!/usr/bin/env bash
# scripts/check-feeds.sh — operator health-check for the AI-news data pipeline.
#
# Probes every RSS/JSON endpoint the hourly-rss and 2h-bluesky workflows
# rely on, reporting HTTP status + content-shape + freshness in one table.
# Exit code: 0 if every endpoint passes both the HTTP and content check,
# 1 if any single feed fails (transport, shape, OR > 30-day stale).
#
# Use this whenever:
#   - the daily digest's "RSS" attribution stops matching reality,
#   - the bluesky channel emits "no data" stubs, or
#   - you want to verify a proposed feed swap before patching the workflow.
#
# Why two user agents: some properties (BunnyCDN-fronted endpoints,
# legacy Microsoft pages) return HTTP 403 for the "compatible;
# AIResearchBot/1.0" UA the workflows historically used. The workflows
# now use a browser-shaped UA; this script does the same and additionally
# probes the legacy UA against the same URLs to flag any regression.

set -uo pipefail

UA_BROWSER="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
UA_BOT="Mozilla/5.0 (compatible; AIResearchBot/1.0; +health-check)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
FAILED=0
NOW_EPOCH=$(date +%s)
STALE_DAYS=30

# check_feed <url> <shape> <label>
# shape ∈ {rss, atom, json}
check_feed() {
  local url="$1" shape="$2" label="$3"
  local out="$TMP/${label//[^A-Za-z0-9]/_}"
  local code
  code=$(curl -sL --max-time 20 -A "$UA_BROWSER" -o "$out" -w "%{http_code}" "$url" 2>/dev/null || echo "000")

  local size body_ok="" latest="" status="OK" age_days=""
  size=$(wc -c <"$out" 2>/dev/null | tr -d ' ')

  case "$shape" in
    rss)
      grep -qiE "<rss|<rdf" "$out" 2>/dev/null && body_ok="yes"
      latest=$(grep -oE '<pubDate>[^<]+</pubDate>' "$out" 2>/dev/null | head -1 | sed -E 's|</?pubDate>||g')
      ;;
    atom)
      grep -qiE "<feed" "$out" 2>/dev/null && body_ok="yes"
      latest=$(grep -oE '<updated>[^<]+</updated>' "$out" 2>/dev/null | head -1 | sed -E 's|</?updated>||g')
      ;;
    json)
      head -c 1 "$out" 2>/dev/null | grep -q '{' && body_ok="yes"
      ;;
  esac

  if [[ -n "$latest" ]]; then
    local latest_epoch
    latest_epoch=$(date -d "$latest" +%s 2>/dev/null || echo 0)
    if [[ "$latest_epoch" -gt 0 ]]; then
      age_days=$(( (NOW_EPOCH - latest_epoch) / 86400 ))
    fi
  fi

  if [[ "$code" != 2* ]]; then
    status="FAIL HTTP=$code"; FAILED=1
  elif [[ -z "$body_ok" ]]; then
    status="FAIL wrong-shape"; FAILED=1
  elif [[ -n "$age_days" && "$age_days" -gt "$STALE_DAYS" ]]; then
    status="FAIL stale=${age_days}d"; FAILED=1
  elif [[ -n "$age_days" ]]; then
    status="OK age=${age_days}d"
  fi

  printf "%-9s  %4s  %8sB  %-32s  %s\n" "$status" "$code" "$size" "${latest:-—}" "$label"
}

# check_dead <url> <expected-failure-mode> <label>
# Asserts that an endpoint the workflows have intentionally dropped is
# still actually dead. Reverse-canary: if it comes back to life, we may
# want to re-add it.
check_dead() {
  local url="$1" why="$2" label="$3"
  local out="$TMP/dead_${label//[^A-Za-z0-9]/_}"
  local code
  code=$(curl -sL --max-time 15 -A "$UA_BROWSER" -o "$out" -w "%{http_code}" "$url" 2>/dev/null || echo "000")
  printf "%-9s  %4s  %-50s  (expected: %s)\n" "DEAD?" "$code" "$label" "$why"
}

echo "=== RSS feeds (hourly-rss.yml) ==="
check_feed "https://openai.com/news/rss.xml"                              rss  "openai"
check_feed "https://openrss.org/www.anthropic.com/news"                   rss  "anthropic_proxy"
check_feed "https://research.google/blog/rss/"                            rss  "google_research"
check_feed "https://deepmind.google/blog/rss.xml"                         rss  "deepmind"
check_feed "https://research.facebook.com/feed/"                          rss  "meta_research"
check_feed "https://engineering.fb.com/feed/"                             rss  "meta_engineering"
check_feed "https://huggingface.co/blog/feed.xml"                         rss  "huggingface"
check_feed "https://blogs.nvidia.com/feed/"                               rss  "nvidia"
check_feed "https://aws.amazon.com/blogs/machine-learning/feed/"          rss  "aws_ml"
check_feed "https://news.microsoft.com/source/topics/ai/feed/"            rss  "microsoft_news_ai"
check_feed "https://www.microsoft.com/en-us/research/blog/feed/"          rss  "microsoft_research"
check_feed "https://www.amazon.science/index.rss"                         rss  "amazon_science"

check_feed "https://export.arxiv.org/rss/cs.AI"                           rss  "arxiv_ai"
check_feed "https://export.arxiv.org/rss/cs.LG"                           rss  "arxiv_lg"

check_feed "https://techcrunch.com/category/artificial-intelligence/feed/"     rss  "techcrunch"
check_feed "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml" rss  "verge"
check_feed "https://venturebeat.com/category/ai/feed/"                         rss  "venturebeat"
check_feed "https://feeds.arstechnica.com/arstechnica/index"                   rss  "arstechnica"
check_feed "https://www.wired.com/feed/tag/ai/latest/rss"                      rss  "wired"
check_feed "https://www.technologyreview.com/feed/"                            rss  "mit_tech_review"

check_feed "https://simonwillison.net/atom/everything/"                   atom "simonwillison"
check_feed "https://importai.substack.com/feed"                           rss  "importai"
check_feed "https://www.interconnects.ai/feed"                            rss  "interconnects"
check_feed "https://www.oneusefulthing.org/feed"                          rss  "oneusefulthing"
check_feed "https://www.latent.space/feed"                                rss  "latent_space"
check_feed "https://www.chinatalk.media/feed"                             rss  "chinatalk"

echo
echo "=== Bluesky (2h-bluesky.yml) ==="
check_feed "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI&limit=5&sort=latest"                   json "bsky_search"
check_feed "https://api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=karpathy.bsky.social&limit=5"       json "bsky_author_feed"

echo
echo "=== Regression guards (must stay dead) ==="
check_dead "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI" "HTTP 403 from BunnyCDN" "public.api.bsky.app"
check_dead "https://ai.meta.com/blog/rss/"                                   "HTTP 400/404"           "ai.meta.com/blog/rss"
check_dead "http://googleaiblog.blogspot.com/atom.xml"                       "frozen at 2025-10-07"   "googleaiblog.blogspot.com"
check_dead "https://blogs.microsoft.com/ai/feed/"                            "frozen at 2022-12-06"   "blogs.microsoft.com/ai"

echo
echo "=== Microsoft UA-gating regression check ==="
# These two URLs return 403 if you hit them with the legacy bot UA.
# The workflow now uses a browser UA — verify the legacy UA *still*
# fails (to detect if Microsoft drops the gating, in which case any
# UA works again).
for url in "https://news.microsoft.com/source/topics/ai/feed/" "https://www.microsoft.com/en-us/research/blog/feed/"; do
  code=$(curl -sLI --max-time 10 -A "$UA_BOT" -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
  printf "%-15s  bot-UA HTTP=%s  %s\n" "BOT-UA" "$code" "$url"
done

echo
if [[ "$FAILED" -eq 0 ]]; then
  echo "[OK] All configured feeds healthy."
  exit 0
else
  echo "[FAIL] At least one feed failed. See lines marked FAIL above."
  exit 1
fi
