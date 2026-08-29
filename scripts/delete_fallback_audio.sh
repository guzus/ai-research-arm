#!/usr/bin/env bash
set -euo pipefail

if [ "${FALLBACK_AUDIO_DRY_RUN:-0}" != "1" ]; then
  : "${S3_ENDPOINT_URL:?S3_ENDPOINT_URL is required}"
  : "${S3_BUCKET:?S3_BUCKET is required}"
  command -v aws >/dev/null 2>&1 || { echo "aws CLI is required" >&2; exit 1; }
fi

deleted=0
while IFS= read -r date; do
  if [[ ! "$date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "Refusing unexpected digest filename: $digest" >&2
    exit 1
  fi
  key="audio/${date}-digest.mp3"
  echo "Fallback audio candidate: $key"
  if [ "${FALLBACK_AUDIO_DRY_RUN:-0}" = "1" ]; then
    deleted=$((deleted + 1))
    continue
  fi
  aws s3api delete-object --bucket "$S3_BUCKET" --key "$key" \
    --endpoint-url "$S3_ENDPOINT_URL" >/dev/null
  aws s3api wait object-not-exists --bucket "$S3_BUCKET" --key "$key" \
    --endpoint-url "$S3_ENDPOINT_URL"
  deleted=$((deleted + 1))
done < <(python3 scripts/digest_publication_state.py --list-fallback-dates research/digest)

echo "Processed ${deleted} non-editorial audio object(s); exact keys are now inaccessible."
