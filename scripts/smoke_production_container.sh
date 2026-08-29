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

for route in / /today /twitter /models /research /wiki; do
  headers="$(mktemp)"
  body="$(mktemp)"
  curl -fsS --max-time 10 -D "$headers" -o "$body" "$base$route"
  grep -Eiq '^content-type: text/html' "$headers"
  grep -Eiq '^x-content-type-options: nosniff' "$headers"
  grep -Eiq '^cache-control: .*max-age=0' "$headers"
  grep -Eiq '<title' "$body"
  rm -f "$headers" "$body"
done

manifest_headers="$(mktemp)"
manifest_body="$(mktemp)"
curl -fsS --max-time 10 -D "$manifest_headers" -o "$manifest_body" "$base/research/manifest.json"
grep -Eiq '^content-type: application/json' "$manifest_headers"
grep -q '"generatedAt"' "$manifest_body"
rm -f "$manifest_headers" "$manifest_body"

for route in /robots.txt /sitemap.xml /feed.xml /llms.txt; do
  curl -fsS --max-time 10 "$base$route" >/dev/null
done

status="$(curl -sS --max-time 10 -o /dev/null -w '%{http_code}' "$base/__ara_smoke_missing__")"
test "$status" = 404

echo "production Docker/Caddy smoke passed at $base"
