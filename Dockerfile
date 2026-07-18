FROM oven/bun:1-alpine AS build

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

FROM oven/bun:1-alpine AS runtime

RUN apk add --no-cache caddy

ENV PORT=8080

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/dashboard/dist/ /srv/

EXPOSE 8080

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
