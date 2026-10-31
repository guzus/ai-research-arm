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

COPY dashboard/package.json dashboard/bun.lock ./dashboard/
RUN cd dashboard && bun install --frozen-lockfile

COPY dashboard ./dashboard
COPY research ./research

# The Aradio podcast feed's <itunes:owner> address, where Spotify for Creators
# mails its ownership code. It is public in /aradio/feed.xml. The platform
# hands a service variable to the build only if the stage declares it, so one
# set there overrides this default; empty emits no owner block. See
# docs/aradio.md "Podcast feed".
ARG ARADIO_FEED_OWNER_EMAIL=i@guzus.xyz

# Every push to main changes research/, so this step never hits the cache.
# Keep its layer down to what the runtime needs (no RUN --mount: Railway's
# builder rejects bind mounts and unprefixed cache mounts):
#   - prebuild's public/research mirror is deleted once vite has copied it;
#   - front-page PNGs (more than half of dist; prebuild copies them byte for
#     byte) are removed from dist and shipped by the front-page stage below as
#     their own runtime layer, which BuildKit reuses until a PNG is added or
#     changed. The list records which PNGs prebuild kept, since it suppresses
#     fallback-digest dates.
RUN cd dashboard \
    && SKIP_LFS_POINTERS=1 bun run build \
    && rm -rf public/research \
    && mkdir -p /app/front-page \
    && cd dist/research/front-page \
    && { ls -1 | grep '\.png$' || true; } > /app/front-page/published.txt \
    && xargs -r rm -- < /app/front-page/published.txt

FROM caddy:2.11.4-alpine@sha256:5f5c8640aae01df9654968d946d8f1a56c497f1dd5c5cda4cf95ab7c14d58648 AS front-page

COPY research/front-page/*.png /src/
COPY --from=build /app/front-page/published.txt /published.txt
RUN mkdir /out && cd /src && xargs -r cp -t /out -- < /published.txt

FROM caddy:2.11.4-alpine@sha256:5f5c8640aae01df9654968d946d8f1a56c497f1dd5c5cda4cf95ab7c14d58648 AS runtime

ENV PORT=8080

COPY Caddyfile /etc/caddy/Caddyfile
# Rarely-changing front-page PNGs first, so most deploys reuse this layer and
# only the dist layer below is new.
COPY --from=front-page /out/ /srv/research/front-page/
COPY --from=build /app/dashboard/dist/ /srv/

EXPOSE 8080

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
