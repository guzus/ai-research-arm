#!/usr/bin/env bash
# scripts/check-feeds.sh — operator health-check for the AI-news data pipeline.
#
# Probes every RSS/JSON endpoint the hourly-rss and 2h-bluesky workflows
# rely on, reporting HTTP status + content-shape + freshness in one table.
# Use this whenever:
#   - the daily digest's "RSS" attribution stops matching reality, or
#   - the bluesky channel emits "no data" stubs, or
#   - you want to verify a proposed feed swap before patching the workflow.
#
# Exit code: 0 if every endpoint passes both the HTTP and content check,
# 1 if any single feed fails. Run it from anywhere; it has no repo deps.

set -uo pipefail

UA="Mozilla/5.0 (compatible; AIResearchBot/1.0; +health-check)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
FAILED=0

# --- check_feed <url> <expected-shape> <label> ----------------------------
# expected-shape ∈ {rss, atom, json}.
# Prints a single fixed-width row; sets FAILED=1 on any check fail.
check_feed() {
  local url="$1" shape="$2" label="$3"
  local out="$TMP/${label//[^A-Za-z0-9]/_}"
  local code
  code=$(curl -sL --max-time 20 -A "$UA" -o "$out" -w "%{http_code}" "$url" || echo "000")

  local size body_ok="" latest="" status="OK"
  size=$(wc -c <"$out" | tr -d ' ')

  case "$shape" in
    rss)
      grep -qiE "<rss|<rdf" "$out" && body_ok="yes"
      latest=$(grep -oE '<pubDate>[^<]+</pubDate>' "$out" | head -1 \
               | sed -E 's|</?pubDate>||g')
      ;;
    atom)
      grep -qiE "<feed" "$out" && body_ok="yes"
      latest=$(grep -oE '<updated>[^<]+</updated>' "$out" | head -1 \
               | sed -E 's|</?updated>||g')
      ;;
    json)
      head -c 1 "$out" | grep -q '{' && body_ok="yes"
      ;;
  esac

  if [[ "$code" != 2* ]]; then
    status="HTTP-$code"; FAILED=1
  elif [[ -z "$body_ok" ]]; then
    status="BAD-BODY";  FAILED=1
  fi

  printf '%-10s %-8s %7s  %-25s  %s\n' \
    "$status" "$code" "$size" "${latest:0:25}" "$label"
}

# --- table header ---------------------------------------------------------
echo "AI-news pipeline feed health — $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
printf '%-10s %-8s %7s  %-25s  %s\n' "STATUS" "HTTP" "BYTES" "LATEST-ITEM" "LABEL"
printf '%s\n' "------------------------------------------------------------------------------------------"

echo "# RSS — official lab blogs"
check_feed "https://openai.com/news/rss.xml"                                rss  "openai"
check_feed "https://openrss.org/www.anthropic.com/news"                     rss  "anthropic-openrss"
check_feed "https://research.google/blog/rss/"                              rss  "google-research"
check_feed "https://deepmind.google/blog/rss.xml"                           rss  "deepmind"
check_feed "https://huggingface.co/blog/feed.xml"                           rss  "huggingface"
check_feed "https://cohere.com/blog/rss.xml"                                rss  "cohere"
check_feed "https://engineering.fb.com/category/ml-applications/feed/"      rss  "meta-engineering-ml"

echo
echo "# RSS — known-broken (kept for visibility; should appear as FAIL)"
check_feed "https://ai.meta.com/blog/rss/"                                  rss  "meta-ai-LEGACY-404"
check_feed "http://googleaiblog.blogspot.com/atom.xml"                      atom "google-blogspot-FROZEN"
check_feed "http://blog.research.google/atom.xml"                           atom "google-blogger-FROZEN"

echo
echo "# RSS — arXiv"
check_feed "https://export.arxiv.org/rss/cs.AI"                             rss  "arxiv-cs.AI"
check_feed "https://export.arxiv.org/rss/cs.LG"                             rss  "arxiv-cs.LG"
check_feed "https://export.arxiv.org/rss/cs.CL"                             rss  "arxiv-cs.CL"

echo
echo "# RSS — tech press"
check_feed "https://techcrunch.com/category/artificial-intelligence/feed/"  rss  "techcrunch-ai"
check_feed "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml" rss "verge-ai"
check_feed "https://venturebeat.com/category/ai/feed/"                      rss  "venturebeat-ai"
check_feed "https://www.technologyreview.com/feed/"                         rss  "mit-tech-review"

echo
echo "# RSS — independent analysts (high signal/byte)"
check_feed "https://simonwillison.net/atom/everything/"                     atom "simonw"
check_feed "https://importai.substack.com/feed"                             rss  "import-ai"
check_feed "https://www.interconnects.ai/feed"                              rss  "interconnects"
check_feed "https://www.oneusefulthing.org/feed"                            rss  "one-useful-thing"
check_feed "https://www.latent.space/feed"                                  rss  "latent-space"
check_feed "https://stratechery.com/feed/"                                  rss  "stratechery"
check_feed "https://www.aisnakeoil.com/feed"                                rss  "ai-snake-oil"
check_feed "https://www.lesswrong.com/feed.xml"                             rss  "lesswrong"

echo
echo "# Bluesky — current workflow endpoint (expected FAIL until workflow patched)"
check_feed "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI&limit=3" json "bsky-public-search"

echo
echo "# Bluesky — replacement endpoints (expected OK)"
check_feed "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI&limit=3"        json "bsky-search-noprefix"
check_feed "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=karpathy.bsky.social&limit=3" json "bsky-authorfeed-karpathy"

echo
if [[ $FAILED -eq 0 ]]; then
  echo "All checks passed."
else
  echo "One or more checks failed (see STATUS column above)."
fi
exit "$FAILED"
