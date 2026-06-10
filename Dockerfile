FROM oven/bun:1-alpine AS build

WORKDIR /app

# The dashboard's package manager is bun (package-lock.json was dropped in #102,
# so `npm ci` can no longer run). Its pre/postbuild lifecycle scripts shell out
# to `node` (node scripts/prebuild.mjs, postbuild-seo.mjs), so install nodejs too.
RUN apk add --no-cache nodejs

COPY dashboard/package.json dashboard/bun.lock ./dashboard/
RUN cd dashboard && bun install --frozen-lockfile

COPY . .

RUN cd dashboard && SKIP_LFS_POINTERS=1 bun run build

FROM caddy:2-alpine

ENV PORT=8080

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/dashboard/dist /srv

EXPOSE 8080
