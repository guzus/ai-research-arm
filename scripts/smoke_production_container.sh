#!/usr/bin/env bash
# Build and exercise the exact root Dockerfile/Caddy runtime Railway deploys.
# This must run only on a GitHub-hosted CI runner for pull requests: PR code is
# untrusted and must never gain a path to the persistent self-hosted runner.
set -euo pipefail

image="ara-production-smoke:${GITHUB_SHA:-local}"
container="ara-production-smoke-${GITHUB_RUN_ID:-local}-${GITHUB_RUN_ATTEMPT:-1}"
container="${container//[^A-Za-z0-9_.-]/-}"

cleanup() {
  docker rm -f "$container" >/dev/null 2>&1 || true
  docker image rm "$image" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker build --pull --tag "$image" .
docker run --detach --rm --name "$container" --publish 127.0.0.1::8080 "$image" >/dev/null
port="$(docker port "$container" 8080/tcp | awk -F: 'NR==1 {print $NF}')"
if [[ ! "$port" =~ ^[0-9]+$ ]]; then
  echo "could not resolve mapped container port: $port" >&2
  exit 1
fi
base="http://127.0.0.1:$port"

for attempt in {1..30}; do
  if curl -fsS --max-time 2 "$base/" >/dev/null; then break; fi
  if [ "$attempt" -eq 30 ]; then
    docker logs "$container" >&2 || true
    echo "production container never became healthy" >&2
    exit 1
  fi
  sleep 1
done

for route in / /today /twitter /models /research /wiki /pricing /pricing/; do
  headers="$(mktemp)"
  body="$(mktemp)"
  curl -fsS --max-time 10 -D "$headers" -o "$body" "$base$route"
  grep -Eiq '^content-type: text/html' "$headers"
  grep -Eiq '^x-content-type-options: nosniff' "$headers"
  grep -Eiq '^cache-control: .*max-age=0' "$headers"
  grep -Eiq '<title' "$body"
  rm -f "$headers" "$body"
done

for route in /pricing /pricing/; do
  pricing_headers="$(mktemp)"
  curl -fsS --max-time 10 -D "$pricing_headers" -o /dev/null "$base$route"
  grep -Eiq '^x-robots-tag: noindex, nofollow' "$pricing_headers"
  rm -f "$pricing_headers"
done

manifest_headers="$(mktemp)"
manifest_body="$(mktemp)"
curl -fsS --max-time 10 -D "$manifest_headers" -o "$manifest_body" "$base/research/manifest.json"
grep -Eiq '^content-type: application/json' "$manifest_headers"
grep -q '"generatedAt"' "$manifest_body"

# A generated dated page must win over the temporary missing-date redirect.
latest_today="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["today"][-1])' "$manifest_body")"
rm -f "$manifest_headers" "$manifest_body"
generated_headers="$(mktemp)"
generated_body="$(mktemp)"
curl -fsS --max-time 10 -D "$generated_headers" -o "$generated_body" "$base/today/$latest_today"
grep -Eiq '^content-type: text/html' "$generated_headers"
grep -Fq "$latest_today" "$generated_body"
if grep -Eiq '^location:' "$generated_headers"; then
  echo "generated Today page redirected unexpectedly" >&2
  exit 1
fi
rm -f "$generated_headers" "$generated_body"

status="$(curl -sS --max-time 10 -o /dev/null -w '%{http_code}' "$base/today/$latest_today/")"
test "$status" = 200

# A valid but unpublished date redirects temporarily to the generated alias;
# no-store ensures the future artifact can take over without a cached redirect.
missing_headers="$(mktemp)"
status="$(curl -sS --max-time 10 -D "$missing_headers" -o /dev/null -w '%{http_code}' "$base/today/2999-12-31")"
test "$status" = 307
grep -Eiq '^location: /today' "$missing_headers"
grep -Eiq '^cache-control: no-store' "$missing_headers"
grep -Eiq '^cdn-cache-control: no-store' "$missing_headers"
rm -f "$missing_headers"

for route in /robots.txt /sitemap.xml /feed.xml /llms.txt; do
  curl -fsS --max-time 10 "$base$route" >/dev/null
done

status="$(curl -sS --max-time 10 -o /dev/null -w '%{http_code}' "$base/__ara_smoke_missing__")"
test "$status" = 404

for route in /today/not-a-date /assets/__ara_smoke_missing__.js; do
  status="$(curl -sS --max-time 10 -o /dev/null -w '%{http_code}' "$base$route")"
  test "$status" = 404
done

echo "production Docker/Caddy smoke passed at $base"
