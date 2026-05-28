#!/usr/bin/env node
// Postbuild: emit static SEO-friendly HTML so non-JS crawlers and link
// unfurlers see real metadata + content. Runs after `vite build`.
//
// Coverage:
//   - Homepage (dist/index.html): rewrites the SEO:DEFAULT block with a
//     homepage-specific title/description/OG + the default social share image.
//   - "today" route (dist/today/index.html): latest daily digest -- per-page
//     title/description/OG + the digest body inlined into #content.
//   - Generative articles (dist/research/<slug>/index.html): per-article
//     title/description/OG + JSON-LD Article + article body inlined.
//   - Wiki pages (dist/wiki/<slug>/index.html): per-page title/description/OG
//     from research/wiki/index.json + page body inlined.
//
// Also emits dist/sitemap.xml (article + tab + wiki URLs with lastmod) and
// dist/robots.txt (allow all + sitemap pointer).
//
// Social share image: the most recent research/front-page/<date>-front-page.png
// (the purpose-built daily newspaper graphic) is reused as the default og:image
// / twitter:image. The image is referenced by its public URL, so it resolves on
// the deployed site even when the build environment skipped LFS hydration
// (Vercel hydrates LFS for the production deploy).
//
// Standalone-kind generative entries (iframe articles) are skipped -- they are
// already self-contained HTML and need a different SEO path.

import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';

const here = dirname(fileURLToPath(import.meta.url));
const dashboardDir = dirname(here);
const repoRoot = dirname(dashboardDir);
const dist = join(dashboardDir, 'dist');
const indexHtmlPath = join(dist, 'index.html');
const researchRoot = join(repoRoot, 'research');
const articlesDir = join(researchRoot, 'generative');
const indexJsonPath = join(articlesDir, 'index.json');
const frontPageDir = join(researchRoot, 'front-page');
const digestDir = join(researchRoot, 'digest');
const wikiDir = join(researchRoot, 'wiki');
const wikiIndexPath = join(wikiDir, 'index.json');

// Override via env (POSTBUILD_SITE_ORIGIN) for preview deploys.
const SITE_ORIGIN = process.env.POSTBUILD_SITE_ORIGIN || 'https://ara.guzus.xyz';

// Markers that delimit the default SEO block in index.html. postbuild replaces
// the whole block (markers included) per page; if the markers are absent we
// fall back to replacing just <title>...</title> so older shells still work.
const SEO_BLOCK_RE = /<!-- SEO:DEFAULT:START[\s\S]*?SEO:DEFAULT:END -->/;

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

// SERPs typically truncate descriptions around 155-160 chars. Aim for ~190
// and gracefully clip on a word boundary so OG / Twitter cards stay clean.
function truncateDescription(s, max = 190) {
  if (s.length <= max) return s;
  const clipped = s.slice(0, max);
  const lastSpace = clipped.lastIndexOf(' ');
  return (lastSpace > 100 ? clipped.slice(0, lastSpace) : clipped) + '…';
}

// Build-time defense in depth: our own generated markdown is trusted, but
// strip anything executable before inlining a rendered snapshot into the
// crawler-facing HTML. The SPA itself runs DOMPurify at runtime.
function sanitizeFragment(html) {
  return html
    .replace(/<script\b[\s\S]*?<\/script>/gi, '')
    .replace(/<style\b[\s\S]*?<\/style>/gi, '')
    .replace(/<iframe\b[\s\S]*?<\/iframe>/gi, '')
    .replace(/\son\w+\s*=\s*"[^"]*"/gi, '')
    .replace(/\son\w+\s*=\s*'[^']*'/gi, '')
    .replace(/javascript:/gi, '');
}

// Most recent research/front-page/<date>-front-page.png, referenced by its
// public URL so it resolves on the deployed site regardless of whether this
// build hydrated LFS. Returns an absolute URL string or null.
function findShareImageUrl() {
  if (!existsSync(frontPageDir)) return null;
  const re = /^(\d{4}-\d{2}-\d{2})-front-page\.png$/;
  let best = null;
  for (const name of readdirSync(frontPageDir)) {
    const m = re.exec(name);
    if (m && (!best || m[1] > best)) best = m[1];
  }
  return best ? `${SITE_ORIGIN}/research/front-page/${best}-front-page.png` : null;
}

// Shared OG/Twitter image tags (or [] when no share image is available).
function imageMetaTags(imageUrl, alt) {
  if (!imageUrl) return [];
  return [
    `<meta property="og:image" content="${htmlEscapeAttr(imageUrl)}" />`,
    `<meta property="og:image:alt" content="${htmlEscapeAttr(alt)}" />`,
    `<meta name="twitter:image" content="${htmlEscapeAttr(imageUrl)}" />`,
  ];
}

// Replace the marked SEO block with metaBlock. Fallback: if the markers are
// absent (older shell), replace just the <title> so we never silently no-op.
function applySeoBlock(template, metaBlockLines) {
  const metaBlock = metaBlockLines.join('\n    ');
  if (SEO_BLOCK_RE.test(template)) {
    return template.replace(SEO_BLOCK_RE, metaBlock);
  }
  return template.replace(/<title>[\s\S]*?<\/title>/, metaBlock);
}

function inlineContent(template, innerHtml) {
  return template.replace(
    '<div id="content"></div>',
    `<div id="content">${innerHtml}</div>`,
  );
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

function buildArticlePage(template, row, articleHtml, shareImageUrl) {
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
    author: { '@type': 'Organization', name: 'ara -- AI research arm', url: SITE_ORIGIN },
    publisher: { '@type': 'Organization', name: 'ara', url: SITE_ORIGIN },
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    url,
  };
  if (shareImageUrl) jsonLd.image = shareImageUrl;

  const metaBlock = [
    `<title>${htmlEscapeAttr(title)} -- ara</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="canonical" href="${url}" />`,
    `<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />`,
    `<meta property="og:type" content="article" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${url}" />`,
    `<meta property="og:site_name" content="ara -- AI research arm" />`,
    `<meta property="article:published_time" content="${dateIso}" />`,
    ...imageMetaTags(shareImageUrl, title),
    `<meta name="twitter:card" content="${shareImageUrl ? 'summary_large_image' : 'summary'}" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="alternate" type="application/rss+xml" title="ara -- AI research arm" href="${SITE_ORIGIN}/feed.xml" />`,
    `<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>`,
  ];

  let html = applySeoBlock(template, metaBlock);
  html = inlineContent(
    html,
    `<div class="content-card gen-research-doc"><div class="content-card-body">${articleHtml}</div></div>`,
  );
  return html;
}

function buildHomePage(template, shareImageUrl) {
  const title = 'ara -- AI research arm';
  const desc = truncateDescription(
    'An automated AI-news intelligence pipeline: daily digests, a model-release ' +
    'timeline, an LLM wiki, and long-form generative research synthesized from ' +
    'Twitter/X, RSS, Bluesky, Hacker News, Reddit, and arXiv.',
  );
  const url = `${SITE_ORIGIN}/`;
  const metaBlock = [
    `<title>${htmlEscapeAttr(title)}</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="canonical" href="${url}" />`,
    `<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />`,
    `<meta property="og:type" content="website" />`,
    `<meta property="og:site_name" content="ara -- AI research arm" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${url}" />`,
    ...imageMetaTags(shareImageUrl, 'ara daily AI newspaper front page'),
    `<meta name="twitter:card" content="${shareImageUrl ? 'summary_large_image' : 'summary'}" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="alternate" type="application/rss+xml" title="ara -- AI research arm" href="${SITE_ORIGIN}/feed.xml" />`,
  ];
  return applySeoBlock(template, metaBlock);
}

function latestDigest() {
  if (!existsSync(digestDir)) return null;
  const re = /^(\d{4}-\d{2}-\d{2})-digest\.md$/;
  let best = null;
  for (const name of readdirSync(digestDir)) {
    const m = re.exec(name);
    if (m && (!best || m[1] > best)) best = m[1];
  }
  if (!best) return null;
  return { date: best, path: join(digestDir, `${best}-digest.md`) };
}

// Pull a sentence-ish description out of the digest markdown: skip the H1 and
// section headings, take the first substantive bullet / paragraph.
function digestDescription(md) {
  const lines = md.split('\n');
  for (const raw of lines) {
    let line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    line = line.replace(/^[-*]\s+/, '');
    const text = decodeEntities(stripTags(marked.parseInline(line)));
    if (text.length >= 40) return truncateDescription(text);
  }
  return 'The day in AI: releases, funding, research, and community signal, synthesized into a single daily digest.';
}

function buildDigestPage(template, digest, shareImageUrl) {
  const md = readFileSync(digest.path, 'utf8');
  const title = `AI Daily Digest -- ${digest.date}`;
  const desc = digestDescription(md);
  const url = `${SITE_ORIGIN}/today`;
  const bodyHtml = sanitizeFragment(marked.parse(md));

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: title,
    description: desc,
    datePublished: digest.date,
    dateModified: digest.date,
    author: { '@type': 'Organization', name: 'ara -- AI research arm', url: SITE_ORIGIN },
    publisher: { '@type': 'Organization', name: 'ara', url: SITE_ORIGIN },
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    url,
  };
  if (shareImageUrl) jsonLd.image = shareImageUrl;

  const metaBlock = [
    `<title>${htmlEscapeAttr(title)} -- ara</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="canonical" href="${url}" />`,
    `<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />`,
    `<meta property="og:type" content="article" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${url}" />`,
    `<meta property="og:site_name" content="ara -- AI research arm" />`,
    `<meta property="article:published_time" content="${digest.date}" />`,
    ...imageMetaTags(shareImageUrl, title),
    `<meta name="twitter:card" content="${shareImageUrl ? 'summary_large_image' : 'summary'}" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="alternate" type="application/rss+xml" title="ara -- AI research arm" href="${SITE_ORIGIN}/feed.xml" />`,
    `<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>`,
  ];

  let html = applySeoBlock(template, metaBlock);
  html = inlineContent(
    html,
    `<div class="content-card"><div class="content-card-body">${bodyHtml}</div></div>`,
  );
  return html;
}

function buildWikiPage(template, page, shareImageUrl) {
  const url = `${SITE_ORIGIN}/wiki/${page.slug}`;
  const title = page.title || page.slug;
  const desc = truncateDescription(decodeEntities(stripTags(page.summary || title)));

  // Inline the page body (markdown after the YAML frontmatter) for crawlers.
  let bodyHtml = '';
  const pagePath = page.file ? join(wikiDir, page.file) : null;
  if (pagePath && existsSync(pagePath)) {
    let text = readFileSync(pagePath, 'utf8');
    if (text.startsWith('---\n')) {
      const end = text.indexOf('\n---\n', 4);
      if (end >= 0) text = text.slice(end + 5);
    }
    // [[wiki-links]] are not markdown; render as plain text for the snapshot.
    text = text.replace(/\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]/gi, (_, slug, label) => label || slug);
    bodyHtml = sanitizeFragment(marked.parse(text));
  }

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: title,
    description: desc,
    datePublished: page.created_at,
    dateModified: page.updated_at || page.created_at,
    author: { '@type': 'Organization', name: 'ara -- AI research arm', url: SITE_ORIGIN },
    publisher: { '@type': 'Organization', name: 'ara', url: SITE_ORIGIN },
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    url,
  };
  if (shareImageUrl) jsonLd.image = shareImageUrl;

  const metaBlock = [
    `<title>${htmlEscapeAttr(title)} -- ara wiki</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="canonical" href="${url}" />`,
    `<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />`,
    `<meta property="og:type" content="article" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${url}" />`,
    `<meta property="og:site_name" content="ara -- AI research arm" />`,
    ...imageMetaTags(shareImageUrl, title),
    `<meta name="twitter:card" content="${shareImageUrl ? 'summary_large_image' : 'summary'}" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="alternate" type="application/rss+xml" title="ara -- AI research arm" href="${SITE_ORIGIN}/feed.xml" />`,
    `<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>`,
  ];

  let html = applySeoBlock(template, metaBlock);
  html = inlineContent(
    html,
    `<div class="content-card"><div class="content-card-body"><h2>${htmlEscapeAttr(title)}</h2>${bodyHtml}</div></div>`,
  );
  return html;
}

function buildSitemap(entries, wikiPages) {
  const today = new Date().toISOString().slice(0, 10);
  const rootEntries = [
    { loc: SITE_ORIGIN + '/', priority: '1.0' },
    { loc: SITE_ORIGIN + '/today', priority: '0.9' },
    { loc: SITE_ORIGIN + '/twitter', priority: '0.7' },
    { loc: SITE_ORIGIN + '/models', priority: '0.7' },
    { loc: SITE_ORIGIN + '/frontpage', priority: '0.6' },
    { loc: SITE_ORIGIN + '/research', priority: '0.9' },
    { loc: SITE_ORIGIN + '/wiki', priority: '0.7' },
  ].map(e => ({ ...e, lastmod: today }));

  const articleEntries = entries.map(e => ({
    loc: `${SITE_ORIGIN}/research/${e.slug}`,
    lastmod: (e.created_at || today).slice(0, 10),
    priority: '0.8',
  }));

  const wikiEntries = (wikiPages || []).map(p => ({
    loc: `${SITE_ORIGIN}/wiki/${p.slug}`,
    lastmod: (p.updated_at || p.created_at || today).slice(0, 10),
    priority: '0.6',
  }));

  const all = [...rootEntries, ...articleEntries, ...wikiEntries];
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

// ---- RSS 2.0 feed of recent digests + recent generative articles ----
function rssEscape(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function toRfc822(input) {
  // input is a YYYY-MM-DD or ISO timestamp; fall back to now on parse failure.
  const d = new Date(input);
  return (isNaN(d.getTime()) ? new Date() : d).toUTCString();
}

function buildFeed(entries, shareImageUrl) {
  const items = [];

  // Recent digests (newest first, capped).
  if (existsSync(digestDir)) {
    const re = /^(\d{4}-\d{2}-\d{2})-digest\.md$/;
    const dates = readdirSync(digestDir)
      .map(n => (re.exec(n) || [])[1])
      .filter(Boolean)
      .sort()
      .reverse()
      .slice(0, 10);
    for (const date of dates) {
      const md = readFileSync(join(digestDir, `${date}-digest.md`), 'utf8');
      items.push({
        title: `AI Daily Digest -- ${date}`,
        link: `${SITE_ORIGIN}/today`,
        guid: `${SITE_ORIGIN}/today#${date}`,
        date,
        description: digestDescription(md),
      });
    }
  }

  // Recent generative articles (skip standalone iframes), newest first, capped.
  const articleItems = entries
    .filter(e => e.kind !== 'standalone')
    .slice()
    .sort((a, b) => String(b.created_at || '').localeCompare(String(a.created_at || '')))
    .slice(0, 15)
    .map(e => ({
      title: e.title || e.slug,
      link: `${SITE_ORIGIN}/research/${e.slug}`,
      guid: `${SITE_ORIGIN}/research/${e.slug}`,
      date: e.created_at,
      description: truncateDescription(decodeEntities(stripTags(e.prompt || e.title || e.slug))),
    }));
  items.push(...articleItems);

  // Newest first across both sources, capped to a small feed.
  items.sort((a, b) => String(b.date || '').localeCompare(String(a.date || '')));
  const top = items.slice(0, 25);
  const lastBuild = top.length ? toRfc822(top[0].date) : new Date().toUTCString();

  const lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
    '  <channel>',
    `    <title>ara -- AI research arm</title>`,
    `    <link>${SITE_ORIGIN}/</link>`,
    `    <atom:link href="${SITE_ORIGIN}/feed.xml" rel="self" type="application/rss+xml" />`,
    `    <description>Automated AI-news intelligence: daily digests and long-form generative research.</description>`,
    `    <language>en</language>`,
    `    <lastBuildDate>${lastBuild}</lastBuildDate>`,
  ];
  if (shareImageUrl) {
    lines.push(
      '    <image>',
      `      <url>${rssEscape(shareImageUrl)}</url>`,
      `      <title>ara -- AI research arm</title>`,
      `      <link>${SITE_ORIGIN}/</link>`,
      '    </image>',
    );
  }
  for (const it of top) {
    lines.push(
      '    <item>',
      `      <title>${rssEscape(it.title)}</title>`,
      `      <link>${rssEscape(it.link)}</link>`,
      `      <guid isPermaLink="false">${rssEscape(it.guid)}</guid>`,
      `      <pubDate>${toRfc822(it.date)}</pubDate>`,
      `      <description>${rssEscape(it.description)}</description>`,
      '    </item>',
    );
  }
  lines.push('  </channel>', '</rss>', '');
  return lines.join('\n');
}

// ---- run ----
if (!existsSync(indexHtmlPath)) {
  console.error(`postbuild-seo: ${indexHtmlPath} not found -- did vite build run?`);
  process.exit(1);
}

const template = readFileSync(indexHtmlPath, 'utf8');
const shareImageUrl = findShareImageUrl();

const entries = existsSync(indexJsonPath)
  ? JSON.parse(readFileSync(indexJsonPath, 'utf8'))
  : [];
if (!existsSync(indexJsonPath)) {
  console.warn(`postbuild-seo: ${indexJsonPath} not found -- no article pages`);
}

// 1) Generative article pages.
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
  const page = buildArticlePage(template, row, articleHtml, shareImageUrl);
  const outDir = join(dist, 'research', row.slug);
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'index.html'), page);
  written++;
}

// 2) "today" digest page.
const digest = latestDigest();
if (digest) {
  const outDir = join(dist, 'today');
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'index.html'), buildDigestPage(template, digest, shareImageUrl));
}

// 3) Wiki pages.
let wikiPages = [];
let wikiWritten = 0;
if (existsSync(wikiIndexPath)) {
  try {
    const wikiIndex = JSON.parse(readFileSync(wikiIndexPath, 'utf8'));
    wikiPages = Array.isArray(wikiIndex.pages) ? wikiIndex.pages : [];
    for (const page of wikiPages) {
      if (!page.slug) continue;
      const outDir = join(dist, 'wiki', page.slug);
      mkdirSync(outDir, { recursive: true });
      writeFileSync(join(outDir, 'index.html'), buildWikiPage(template, page, shareImageUrl));
      wikiWritten++;
    }
  } catch (e) {
    console.warn(`postbuild-seo: wiki index parse failed (${e.message}); skipping wiki pages`);
  }
}

// 4) Homepage -- rewrite dist/index.html LAST (it was the template above, so
//    article/today/wiki pages inherit the default block, not the homepage one).
writeFileSync(indexHtmlPath, buildHomePage(template, shareImageUrl));

// 5) sitemap.xml, robots.txt, feed.xml.
writeFileSync(join(dist, 'sitemap.xml'), buildSitemap(entries, wikiPages));
writeFileSync(join(dist, 'robots.txt'), buildRobots());
writeFileSync(join(dist, 'feed.xml'), buildFeed(entries, shareImageUrl));

console.log(
  `postbuild-seo: ${written} article pages (${skipped} skipped), ` +
  `${digest ? 1 : 0} digest page, ${wikiWritten} wiki pages`,
);
console.log(`postbuild-seo: share image: ${shareImageUrl || '(none found)'}`);
console.log('postbuild-seo: sitemap.xml + robots.txt + feed.xml written to dist/');
