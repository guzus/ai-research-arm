FROM oven/bun:1-alpine AS build

WORKDIR /app

# The dashboard's package manager is bun (package-lock.json was dropped in #102,
# so `npm ci` can no longer run). Its pre/postbuild lifecycle scripts shell out
# to `node` (node scripts/prebuild.mjs, postbuild-seo.mjs), so install nodejs too.
# Caddy is installed here as well so Railway does not need to pull a second
# Docker Hub base image for the static-file runtime.
RUN apk add --no-cache nodejs caddy

COPY dashboard/package.json dashboard/bun.lock ./dashboard/
RUN cd dashboard && bun install --frozen-lockfile

COPY . .

RUN cd dashboard && SKIP_LFS_POINTERS=1 bun run build

ENV PORT=8080

COPY Caddyfile /etc/caddy/Caddyfile
RUN mkdir -p /srv && cp -R /app/dashboard/dist/. /srv/

EXPOSE 8080

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
