FROM node:22-alpine AS build

WORKDIR /app

COPY dashboard/package*.json ./dashboard/
RUN cd dashboard && npm ci

COPY . .

ENV SKIP_LFS_POINTERS=1
RUN cd dashboard && npm run build

FROM caddy:2-alpine

ENV PORT=8080

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/dashboard/dist /srv

EXPOSE 8080
