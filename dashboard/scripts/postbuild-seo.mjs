#!/usr/bin/env node
// Postbuild: emit static SEO-friendly HTML for every research article.
// Runs after `vite build`. For each fragment-kind entry in
// research/generative/index.json, generates dist/research/<slug>/index.html
// containing:
//   - per-article <title>, <meta description>, OG / Twitter Card meta
//   - <link rel="canonical">
//   - JSON-LD Article schema
//   - the article body inlined into #content so non-JS crawlers and link
//     unfurlers see the actual content (the SPA hydrates on top and
//     replaces #content with the SPA-wrapped version, identical content)
//   - the same Vite bundle script/style tags from the built shell
//
// Also emits dist/sitemap.xml (article + tab URLs with lastmod) and
// dist/robots.txt (allow all + sitemap pointer).
//
// Standalone-kind entries (iframe articles) are skipped — they're already
// self-contained HTML and need a different SEO path.

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const dashboardDir = dirname(here);
const repoRoot = dirname(dashboardDir);
const dist = join(dashboardDir, 'dist');
const indexHtmlPath = join(dist, 'index.html');
const articlesDir = join(repoRoot, 'research', 'generative');
const indexJsonPath = join(articlesDir, 'index.json');

// Override via env (POSTBUILD_SITE_ORIGIN) for preview deploys.
const SITE_ORIGIN = process.env.POSTBUILD_SITE_ORIGIN || 'https://ara.guzus.xyz';

function stripTags(html) {
  return html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
}

function decodeEntities(s) {
  return s
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .replace(/&mdash;/g, '—')
    .replace(/&ndash;/g, '–')
    .replace(/&hellip;/g, '…')
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, n) => String.fromCodePoint(parseInt(n, 16)));
}

function htmlEscapeAttr(s) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// SERPs typically truncate descriptions around 155–160 chars. Aim for ~190
// and gracefully clip on a word boundary so OG / Twitter cards stay clean.
function truncateDescription(s, max = 190) {
  if (s.length <= max) return s;
  const clipped = s.slice(0, max);
  const lastSpace = clipped.lastIndexOf(' ');
  return (lastSpace > 100 ? clipped.slice(0, lastSpace) : clipped) + '…';
}

function extractMeta(articleHtml) {
  const titleMatch = articleHtml.match(/<h2\s+class="ara-display"[^>]*>([\s\S]*?)<\/h2>/);
  const title = titleMatch ? decodeEntities(stripTags(titleMatch[1])) : '';
  const deckMatch = articleHtml.match(/<p\s+class="ara-deck"[^>]*>([\s\S]*?)<\/p>/);
  const ledeMatch = articleHtml.match(/<p\s+class="ara-lede"[^>]*>([\s\S]*?)<\/p>/);
  const firstPMatch = articleHtml.match(/<p[^>]*>([\s\S]*?)<\/p>/);
  let raw = '';
  if (deckMatch) raw = stripTags(deckMatch[1]);
  else if (ledeMatch) raw = stripTags(ledeMatch[1]);
  else if (firstPMatch) raw = stripTags(firstPMatch[1]);
  const desc = truncateDescription(decodeEntities(raw));
  return { title, desc };
}

function buildArticlePage(template, row, articleHtml) {
  const url = `${SITE_ORIGIN}/research/${row.slug}`;
  const { title: extracted, desc } = extractMeta(articleHtml);
  const title = extracted || row.title || row.slug;
  const dateIso = row.created_at;

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: title,
    description: desc,
    datePublished: dateIso,
    dateModified: dateIso,
    author: { '@type': 'Organization', name: 'ara — AI research arm', url: SITE_ORIGIN },
    publisher: { '@type': 'Organization', name: 'ara', url: SITE_ORIGIN },
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    url,
  };

  const metaBlock = [
    `<title>${htmlEscapeAttr(title)} — ara</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="canonical" href="${url}" />`,
    `<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />`,
    `<meta property="og:type" content="article" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${url}" />`,
    `<meta property="og:site_name" content="ara — AI research arm" />`,
    `<meta property="article:published_time" content="${dateIso}" />`,
    `<meta name="twitter:card" content="summary" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>`,
  ].join('\n    ');

  let html = template.replace(/<title>[\s\S]*?<\/title>/, metaBlock);
  html = html.replace(
    '<div id="content"></div>',
    `<div id="content"><div class="content-card gen-research-doc"><div class="content-card-body">${articleHtml}</div></div></div>`,
  );
  return html;
}

function buildSitemap(entries) {
  const today = new Date().toISOString().slice(0, 10);
  const rootEntries = [
    { loc: SITE_ORIGIN + '/', priority: '1.0' },
    { loc: SITE_ORIGIN + '/today', priority: '0.9' },
    { loc: SITE_ORIGIN + '/twitter', priority: '0.7' },
    { loc: SITE_ORIGIN + '/models', priority: '0.7' },
    { loc: SITE_ORIGIN + '/frontpage', priority: '0.6' },
    { loc: SITE_ORIGIN + '/research', priority: '0.9' },
  ].map(e => ({ ...e, lastmod: today }));

  const articleEntries = entries.map(e => ({
    loc: `${SITE_ORIGIN}/research/${e.slug}`,
    lastmod: (e.created_at || today).slice(0, 10),
    priority: '0.8',
  }));

  const all = [...rootEntries, ...articleEntries];
  const lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ];
  for (const e of all) {
    lines.push(
      `  <url><loc>${e.loc}</loc><lastmod>${e.lastmod}</lastmod><priority>${e.priority}</priority></url>`,
    );
  }
  lines.push('</urlset>', '');
  return lines.join('\n');
}

function buildRobots() {
  return [
    'User-agent: *',
    'Allow: /',
    '',
    `Sitemap: ${SITE_ORIGIN}/sitemap.xml`,
    '',
  ].join('\n');
}

// ---- run ----
if (!existsSync(indexHtmlPath)) {
  console.error(`postbuild-seo: ${indexHtmlPath} not found — did vite build run?`);
  process.exit(1);
}
if (!existsSync(indexJsonPath)) {
  console.warn(`postbuild-seo: ${indexJsonPath} not found — skipping article SEO`);
  process.exit(0);
}

const template = readFileSync(indexHtmlPath, 'utf8');
const entries = JSON.parse(readFileSync(indexJsonPath, 'utf8'));

let written = 0;
let skipped = 0;
for (const row of entries) {
  if (row.kind === 'standalone') {
    skipped++;
    continue;
  }
  const articlePath = join(articlesDir, row.file);
  if (!existsSync(articlePath)) {
    skipped++;
    continue;
  }
  const articleHtml = readFileSync(articlePath, 'utf8');
  const page = buildArticlePage(template, row, articleHtml);
  const outDir = join(dist, 'research', row.slug);
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'index.html'), page);
  written++;
}

writeFileSync(join(dist, 'sitemap.xml'), buildSitemap(entries));
writeFileSync(join(dist, 'robots.txt'), buildRobots());

console.log(`postbuild-seo: wrote ${written} article pages (${skipped} skipped)`);
console.log('postbuild-seo: sitemap.xml + robots.txt written to dist/');
