FROM node:22-alpine AS build

WORKDIR /app

COPY dashboard/package*.json ./dashboard/
RUN cd dashboard && npm ci

COPY . .

RUN cd dashboard && SKIP_LFS_POINTERS=1 npm run build

FROM caddy:2-alpine

ENV PORT=8080

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/dashboard/dist /srv

EXPOSE 8080
