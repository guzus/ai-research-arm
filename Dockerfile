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

RUN cd dashboard && SKIP_LFS_POINTERS=1 bun run build

FROM caddy:2.11.4-alpine@sha256:5f5c8640aae01df9654968d946d8f1a56c497f1dd5c5cda4cf95ab7c14d58648 AS runtime

ENV PORT=8080

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/dashboard/dist/ /srv/

EXPOSE 8080

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
