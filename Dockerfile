# Keep the contest/release SBOM reproducible. The tag documents the human-
# readable version while the digest prevents it from moving underneath us.
FROM oven/bun:1.4.0-alpine@sha256:07235578f79ef8c6f97d94aee7938e76f5cdba5f21ae5dbfdd3d3d38058437eb AS build

WORKDIR /app

# The dashboard's package manager is bun (package-lock.json was dropped in #102,
# so `npm ci` can no longer run). Its pre/postbuild lifecycle scripts shell out
# to `node`; postbuild renders per-article social cards with @resvg/resvg-js,
# which rasterizes text from system fonts — font-liberation provides the
# Liberation Serif/Sans families the card renderer targets (alpine has no
# fonts by default; without this the cards render with no text).
RUN apk add --no-cache nodejs font-liberation

# Dependencies only change with the lockfile; the cache mount also keeps bun's
# download cache across lockfile changes.
ENV BUN_INSTALL_CACHE_DIR=/var/cache/bun
COPY dashboard/package.json dashboard/bun.lock ./dashboard/
RUN --mount=type=cache,id=ara-web-bun,target=/var/cache/bun \
    cd dashboard && bun install --frozen-lockfile

COPY dashboard ./dashboard

# Every push to main changes research/, so this step never hits the cache.
# Keep its layer down to what the runtime needs:
#   - research/ is bind-mounted, not COPYed, so it is not stored as a layer;
#   - prebuild's public/research mirror is deleted once vite has copied it;
#   - front-page PNGs (more than half of dist; prebuild copies them byte for
#     byte) are removed from dist and shipped by the front-page stage below as
#     their own runtime layer, which BuildKit reuses until a PNG is added or
#     changed. The list records which PNGs prebuild kept, since it suppresses
#     fallback-digest dates.
RUN --mount=type=bind,source=research,target=/app/research,rw \
    cd dashboard \
    && SKIP_LFS_POINTERS=1 bun run build \
    && rm -rf public/research \
    && mkdir -p /app/front-page \
    && cd dist/research/front-page \
    && { ls -1 | grep '\.png$' || true; } > /app/front-page/published.txt \
    && xargs -r rm -- < /app/front-page/published.txt

FROM caddy:2.11.4-alpine@sha256:5f5c8640aae01df9654968d946d8f1a56c497f1dd5c5cda4cf95ab7c14d58648 AS front-page

COPY --from=build /app/front-page/published.txt /published.txt
RUN --mount=type=bind,source=research/front-page,target=/src \
    mkdir /out && cd /src && xargs -r cp -t /out -- < /published.txt

FROM caddy:2.11.4-alpine@sha256:5f5c8640aae01df9654968d946d8f1a56c497f1dd5c5cda4cf95ab7c14d58648 AS runtime

ENV PORT=8080

COPY Caddyfile /etc/caddy/Caddyfile
# Rarely-changing front-page PNGs first, so most deploys reuse this layer and
# only the dist layer below is new.
COPY --from=front-page /out/ /srv/research/front-page/
COPY --from=build /app/dashboard/dist/ /srv/

EXPOSE 8080

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
