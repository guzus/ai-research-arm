#!/usr/bin/env node
// Postbuild: emit static SEO-friendly HTML so non-JS crawlers and link
// unfurlers see real metadata + content. Runs after `vite build`.
//
// Coverage:
//   - Homepage (dist/index.html): rewrites the SEO:DEFAULT block with a
//     homepage-specific title/description/OG + the default social share image.
//   - Dated daily digest, Twitter/X report, and newspaper routes: unique
//     metadata/content; undated latest aliases canonicalize to the dated page.
//   - Research and wiki archive hubs: crawlable collections with real links.
//   - Generative articles (dist/research/<slug>/index.html): per-article
//     title/description/OG + JSON-LD Article + article body inlined.
//   - Wiki pages (dist/wiki/<slug>/index.html): per-page title/description/OG
//     from research/wiki/index.json + page body inlined.
//   - Verified mapped model forecasts (dist/models/forecast/<slug>/index.html):
//     stable metadata + committed evidence and prediction-market links.
//   - Internal/duplicate routes (agents, focus-reader, dated model aliases):
//     explicit noindex pages with an appropriate canonical.
//
// Also emits dist/sitemap.xml (canonical indexable URLs only, with lastmod),
// dist/robots.txt (allow all + sitemap pointer), dist/feed.xml, and
// dist/llms.txt for AI-answer engines.
//
// Social share images:
//   - Per-article: a deterministic 1200x630 typographic card rendered at build
//     time by scripts/social-card.mjs (resvg, no Chromium/network/S3 — the
//     replaced Playwright screenshot pipeline needed all three and silently
//     degraded when any was missing). Written to
//     dist/research/generative/<stem>.social.png, same URL contract as before.
//   - Everything else: the committed brand illustration in public/brand/
//     (1280x640) with the wordmark composited in white at build time — a
//     valid 2:1 card on every route.
//
// Standalone-kind generative entries (iframe articles) are skipped -- they are
// already self-contained HTML and need a different SEO path.

import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import { renderSiteDefaultCardPng, renderSocialCardPng } from './social-card.mjs';
import { forecastSeoRecord, mappedForecastTickets } from './forecast-seo.mjs';
import {
  datedPagePolicy,
  isIndexableResearchEntry,
  latestAliasPolicy,
  sortDatedRecords,
} from './site-seo.mjs';

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
const twitterDir = join(researchRoot, 'twitter');
const modelTimelineDir = join(researchRoot, 'models');
const wikiDir = join(researchRoot, 'wiki');
const wikiIndexPath = join(wikiDir, 'index.json');
const distGenerativeDir = join(dist, 'research', 'generative');
const distTicketIndexPath = join(dist, 'research', 'models', 'tickets', 'index.json');
const armTimelinePath = join(researchRoot, 'arm', 'timeline.json');

// Override via env (POSTBUILD_SITE_ORIGIN) for preview deploys.
const SITE_ORIGIN = process.env.POSTBUILD_SITE_ORIGIN || 'https://ara.guzus.xyz';
const SITE_NAME = 'ara -- AI research arm';
const SITE_DESCRIPTION =
  'Automated AI-news intelligence: daily digests, a model-release timeline, ' +
  'an LLM wiki, and long-form generative research synthesized from Twitter/X, ' +
  'RSS, Bluesky, Hacker News, Reddit, and arXiv.';
const HOME_DESCRIPTION =
  'An automated AI-news intelligence pipeline: daily digests, a model-release ' +
  'timeline, an LLM wiki, and long-form generative research synthesized from ' +
  'Twitter/X, RSS, Bluesky, Hacker News, Reddit, and arXiv.';
const SITE_LINKS = {
  github: 'https://github.com/guzus/ai-research-arm',
  author: 'https://x.com/uncanny_guzus',
};
// Markers that delimit the default SEO block in index.html. postbuild replaces
// the whole block (markers included) per page; if the markers are absent we
// fall back to replacing just <title>...</title> so older shells still work.
const SEO_BLOCK_RE = /<!-- SEO:DEFAULT:START[\s\S]*?SEO:DEFAULT:END -->/;
const STATIC_CONTENT_RE = /<!-- SEO:STATIC:START -->[\s\S]*?<!-- SEO:STATIC:END -->/;

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

function jsonLdTag(data) {
  // JSON.stringify does not escape HTML-significant characters. Keep model-
  // authored ticket/article text from terminating the JSON-LD script early.
  const json = JSON.stringify(data).replace(/</g, '\\u003c').replace(/>/g, '\\u003e');
  return `<script type="application/ld+json">${json}</script>`;
}

function sharedMetaTags(title, desc) {
  return [
    `<meta name="author" content="ara -- AI research arm" />`,
    `<meta name="application-name" content="ara" />`,
    `<meta name="theme-color" content="#0f172a" />`,
    `<meta name="generator" content="ARA static SEO postbuild" />`,
    `<meta name="keywords" content="${htmlEscapeAttr('AI news, AI research, LLMs, model releases, artificial intelligence digest, generative AI, machine learning')}" />`,
    `<meta name="abstract" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:locale" content="en_US" />`,
  ];
}

function organizationNode() {
  return {
    '@type': 'Organization',
    '@id': `${SITE_ORIGIN}/#organization`,
    name: SITE_NAME,
    alternateName: 'ara',
    url: SITE_ORIGIN,
    sameAs: [SITE_LINKS.github, SITE_LINKS.author],
  };
}

function publisherNode() {
  return { '@id': `${SITE_ORIGIN}/#organization` };
}

function compactText(s) {
  return String(s || '').replace(/\s+/g, ' ').trim();
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

// Site-wide default share image: the committed 2:1 brand illustration with
// the wordmark composited in white at build time, written to dist/brand/.
// Falls back to the raw brand asset if compositing fails, then to the newest
// front-page newspaper PNG for forks that stripped the brand asset entirely.
// Returns an absolute URL string or null.
const brandSourcePath = join(dashboardDir, 'public', 'brand', 'github-social-preview.png');

async function findShareImageUrl() {
  if (existsSync(brandSourcePath)) {
    try {
      const png = await renderSiteDefaultCardPng(readFileSync(brandSourcePath), 'ai-research-arm');
      const outDir = join(dist, 'brand');
      mkdirSync(outDir, { recursive: true });
      writeFileSync(join(outDir, 'site-social-card.png'), png);
      return `${SITE_ORIGIN}/brand/site-social-card.png`;
    } catch (e) {
      console.warn(`postbuild-seo: site share-card compositing failed (${e.message}); using raw brand image`);
      return `${SITE_ORIGIN}/brand/github-social-preview.png`;
    }
  }
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
function absoluteImageUrl(url) {
  if (typeof url !== 'string' || !url.trim() || /\s/.test(url)) return null;
  if (/\.svg(?:$|[?#])/i.test(url)) return null;
  if (/^https?:\/\//i.test(url)) return url;
  if (url.startsWith('/') && !url.startsWith('//')) return `${SITE_ORIGIN}${url}`;
  return null;
}

function imageMetaItems(imageInput, fallbackAlt) {
  if (!imageInput) return [];
  const rawItems = Array.isArray(imageInput)
    ? imageInput
    : typeof imageInput === 'string'
      ? [{ url: imageInput, alt: fallbackAlt }]
      : [imageInput];
  return rawItems
    .map(item => {
      if (typeof item === 'string') return { url: absoluteImageUrl(item), alt: fallbackAlt };
      const url = absoluteImageUrl(item?.url);
      const alt = String(item?.alt || fallbackAlt || '').trim();
      const width = Number.isFinite(Number(item?.width)) ? Number(item.width) : null;
      const height = Number.isFinite(Number(item?.height)) ? Number(item.height) : null;
      const type = String(item?.type || '').trim() || imageMimeType(url);
      return { url, alt, width, height, type };
    })
    .filter(item => item.url);
}

function imageMimeType(url) {
  const path = String(url || '').split(/[?#]/, 1)[0].toLowerCase();
  if (path.endsWith('.png')) return 'image/png';
  if (path.endsWith('.jpg') || path.endsWith('.jpeg')) return 'image/jpeg';
  if (path.endsWith('.webp')) return 'image/webp';
  if (path.endsWith('.gif')) return 'image/gif';
  return '';
}

function isImageLikeUrl(url) {
  return /\.(png|jpe?g|webp|gif)(?:$|[?#])/i.test(String(url || ''));
}

function imageMetaTags(imageInput, alt) {
  const images = imageMetaItems(imageInput, alt);
  if (!images.length) return [];
  const tags = [];
  for (const img of images) {
    tags.push(`<meta property="og:image" content="${htmlEscapeAttr(img.url)}" />`);
    if (img.width) tags.push(`<meta property="og:image:width" content="${htmlEscapeAttr(String(img.width))}" />`);
    if (img.height) tags.push(`<meta property="og:image:height" content="${htmlEscapeAttr(String(img.height))}" />`);
    if (img.type) tags.push(`<meta property="og:image:type" content="${htmlEscapeAttr(img.type)}" />`);
    if (img.alt) tags.push(`<meta property="og:image:alt" content="${htmlEscapeAttr(img.alt)}" />`);
  }
  tags.push(`<meta name="twitter:image" content="${htmlEscapeAttr(images[0].url)}" />`);
  return tags;
}

function articleArtifactUrl(url) {
  const value = String(url || '').trim();
  if (!value || !isImageLikeUrl(value)) return null;
  if (/^https?:\/\//i.test(value) || value.startsWith('/')) return value;
  if (value.startsWith('research/')) return `/${value}`;
  if (value.startsWith('generative/')) return `/research/${value}`;
  return `/research/generative/${value}`;
}

function normalizeArticleArtifactImage(imageInput, fallbackAlt) {
  if (!imageInput) return null;
  if (typeof imageInput === 'string') {
    const url = articleArtifactUrl(imageInput);
    return url ? { url, alt: fallbackAlt } : null;
  }
  if (Array.isArray(imageInput)) {
    const images = imageInput
      .map(item => normalizeArticleArtifactImage(item, fallbackAlt))
      .filter(Boolean);
    return images.length ? images : null;
  }
  const url = articleArtifactUrl(imageInput.url || imageInput.path || imageInput.file);
  if (!url) return null;
  return {
    ...imageInput,
    url,
    alt: String(imageInput.alt || fallbackAlt || '').trim(),
  };
}

function articleArtifactImage(row, fallbackAlt) {
  const declared =
    row?.social_image ||
    row?.og_image ||
    row?.preview_image ||
    row?.artifact_image ||
    row?.image ||
    row?.artifacts?.social_image ||
    row?.artifacts?.preview_image ||
    row?.artifacts?.image;
  if (declared) return normalizeArticleArtifactImage(declared, fallbackAlt);

  const file = typeof row?.file === 'string' ? row.file : '';
  if (!file.endsWith('.html')) return null;
  const stem = file.slice(0, -'.html'.length);
  for (const ext of ['png', 'jpg', 'jpeg', 'webp', 'gif']) {
    const name = `${stem}.${ext}`;
    if (existsSync(join(articlesDir, name))) {
      return { url: `/research/generative/${name}`, alt: fallbackAlt };
    }
  }
  return null;
}

function articleShareImage(row, fallbackShareImageUrl, fallbackAlt, generatedImages = new Map()) {
  return articleArtifactImage(row, fallbackAlt) || generatedImages.get(row.slug) || fallbackShareImageUrl;
}

// Deterministic per-article social card, written to
// dist/research/generative/<stem>.social.png — the same URL contract as the
// retired Chromium-screenshot pipeline, so links crawled against old deploys
// pick up the new card on their next re-crawl without a URL change.
function articleSocialCardMeta(row, alt) {
  const file = typeof row?.file === 'string' ? row.file : '';
  if (!file.endsWith('.html')) return null;
  const stem = file.slice(0, -'.html'.length);
  return {
    outputPath: join(distGenerativeDir, `${stem}.social.png`),
    image: {
      url: `/research/generative/${stem}.social.png`,
      alt,
      width: 1200,
      height: 630,
      type: 'image/png',
    },
  };
}

const CARD_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
function cardDateLabel(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(iso || ''));
  if (!m) return '';
  return `${CARD_MONTHS[Number(m[2]) - 1]} ${Number(m[3])}, ${m[1]}`;
}

// Card chrome is deliberately spare — date, title, deck, model attribution,
// domain — so shared links read canonical rather than decorated.
async function generateArticleSocialCard(row, title, description) {
  const meta = articleSocialCardMeta(row, title);
  if (!meta) return null;
  const png = await renderSocialCardPng({
    eyebrow: cardDateLabel(row.created_at),
    title,
    description,
    attribution: row.model ? `Research by ${row.model}` : '',
  });
  mkdirSync(distGenerativeDir, { recursive: true });
  writeFileSync(meta.outputPath, png);
  return meta.image;
}

// Replace the marked SEO block with metaBlock. Fallback: if the markers are
// absent (older shell), replace just the <title> so we never silently no-op.
function applySeoBlock(template, metaBlockLines) {
  const metaBlock = metaBlockLines.join('\n    ');
  if (SEO_BLOCK_RE.test(template)) {
    // Preserve the markers so a diagnostic/manual second postbuild remains
    // idempotent instead of appending a second canonical/OG block.
    const wrapped = [
      '<!-- SEO:DEFAULT:START -->',
      metaBlock,
      '<!-- SEO:DEFAULT:END -->',
    ].join('\n    ');
    return template.replace(SEO_BLOCK_RE, wrapped);
  }
  return template.replace(/<title>[\s\S]*?<\/title>/, metaBlock);
}

function inlineContent(template, innerHtml) {
  const block = `<!-- SEO:STATIC:START -->${innerHtml}<!-- SEO:STATIC:END -->`;
  if (STATIC_CONTENT_RE.test(template)) {
    return template.replace(STATIC_CONTENT_RE, block);
  }
  return template.replace(
    '<div id="content"></div>',
    `<div id="content">${block}</div>`,
  );
}

function demoteHeadings(html) {
  return String(html || '')
    .replace(/<h1(\s[^>]*)?>/gi, '<h2$1>')
    .replace(/<\/h1>/gi, '</h2>');
}

function singleH1Snapshot(title, bodyHtml, classes = 'content-card') {
  return [
    `<article class="${htmlEscapeAttr(classes)}">`,
    '<div class="content-card-body">',
    `<h1>${htmlEscapeAttr(title)}</h1>`,
    demoteHeadings(bodyHtml),
    '</div>',
    '</article>',
  ].join('');
}

function standardMetaBlock({
  title,
  description,
  canonicalUrl,
  shareImage,
  type = 'website',
  indexable = true,
  jsonLd,
  published,
  modified,
}) {
  const desc = truncateDescription(compactText(description));
  return [
    `<title>${htmlEscapeAttr(title)} -- ara</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    ...sharedMetaTags(title, desc),
    `<link rel="canonical" href="${htmlEscapeAttr(canonicalUrl)}" />`,
    `<meta name="robots" content="${indexable ? 'index,follow,max-image-preview:large,max-snippet:-1' : 'noindex,follow'}" />`,
    `<meta property="og:type" content="${htmlEscapeAttr(type)}" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${htmlEscapeAttr(canonicalUrl)}" />`,
    `<meta property="og:site_name" content="ara -- AI research arm" />`,
    published ? `<meta property="article:published_time" content="${htmlEscapeAttr(published)}" />` : '',
    modified ? `<meta property="article:modified_time" content="${htmlEscapeAttr(modified)}" />` : '',
    ...imageMetaTags(shareImage, title),
    `<meta name="twitter:card" content="${shareImage ? 'summary_large_image' : 'summary'}" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="alternate" type="application/rss+xml" title="ara -- AI research arm" href="${SITE_ORIGIN}/feed.xml" />`,
    `<link rel="alternate" type="text/plain" title="llms.txt" href="${SITE_ORIGIN}/llms.txt" />`,
    jsonLd ? jsonLdTag(jsonLd) : '',
  ].filter(Boolean);
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

function buildArticlePage(template, row, articleHtml, shareImageUrl, generatedImages = new Map(), indexable = true) {
  const url = `${SITE_ORIGIN}/research/${row.slug}`;
  const { title: extracted, desc } = extractMeta(articleHtml);
  const title = extracted || row.title || row.slug;
  const dateIso = row.created_at;
  const keywords = Array.isArray(row.tags) ? row.tags.filter(Boolean) : [];
  const pageShareImage = articleShareImage(row, shareImageUrl, title, generatedImages);

  const jsonLd = {
    '@type': 'Article',
    headline: title,
    description: desc,
    datePublished: dateIso,
    dateModified: dateIso,
    inLanguage: 'en',
    isAccessibleForFree: true,
    author: publisherNode(),
    publisher: publisherNode(),
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    keywords,
    about: keywords.map(name => ({ '@type': 'Thing', name })),
    url,
  };
  const jsonLdImages = imageMetaItems(pageShareImage, title).map(img => img.url);
  if (jsonLdImages.length) jsonLd.image = jsonLdImages;

  const metaBlock = [
    `<title>${htmlEscapeAttr(title)} -- ara</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    ...sharedMetaTags(title, desc),
    keywords.length ? `<meta name="news_keywords" content="${htmlEscapeAttr(keywords.join(', '))}" />` : '',
    `<link rel="canonical" href="${url}" />`,
    `<meta name="robots" content="${indexable ? 'index,follow,max-image-preview:large,max-snippet:-1' : 'noindex,follow'}" />`,
    `<meta property="og:type" content="article" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${url}" />`,
    `<meta property="og:site_name" content="ara -- AI research arm" />`,
    `<meta property="article:published_time" content="${dateIso}" />`,
    ...imageMetaTags(pageShareImage, title),
    `<meta name="twitter:card" content="${pageShareImage ? 'summary_large_image' : 'summary'}" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="alternate" type="application/rss+xml" title="ara -- AI research arm" href="${SITE_ORIGIN}/feed.xml" />`,
    `<link rel="alternate" type="text/plain" title="llms.txt" href="${SITE_ORIGIN}/llms.txt" />`,
    jsonLdTag({ '@context': 'https://schema.org', '@graph': [organizationNode(), jsonLd] }),
  ].filter(Boolean);

  let html = applySeoBlock(template, metaBlock);
  const displayHeadingRe = /<h2(\s+class="ara-display"[^>]*)>([\s\S]*?)<\/h2>/i;
  const demotedArticleHtml = demoteHeadings(articleHtml);
  const crawlerArticleHtml = displayHeadingRe.test(demotedArticleHtml)
    ? demotedArticleHtml.replace(displayHeadingRe, '<h1$1>$2</h1>')
    : `<h1>${htmlEscapeAttr(title)}</h1>${demotedArticleHtml}`;
  html = inlineContent(
    html,
    `<div class="content-card gen-research-doc"><div class="content-card-body">${crawlerArticleHtml}</div></div>`,
  );
  return html;
}

function buildHomePage(template, shareImageUrl) {
  const title = 'ara -- AI research arm';
  const desc = truncateDescription(HOME_DESCRIPTION);
  const url = `${SITE_ORIGIN}/`;
  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      organizationNode(),
      {
        '@type': 'WebSite',
        '@id': `${SITE_ORIGIN}/#website`,
        name: SITE_NAME,
        alternateName: 'ara',
        url,
        description: desc,
        inLanguage: 'en',
        publisher: publisherNode(),
      },
    ],
  };
  const metaBlock = [
    `<title>${htmlEscapeAttr(title)}</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    ...sharedMetaTags(title, desc),
    `<link rel="canonical" href="${url}" />`,
    `<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />`,
    `<meta property="og:type" content="website" />`,
    `<meta property="og:site_name" content="ara -- AI research arm" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${url}" />`,
    ...imageMetaTags(shareImageUrl, 'ara — AI research arm'),
    `<meta name="twitter:card" content="${shareImageUrl ? 'summary_large_image' : 'summary'}" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="alternate" type="application/rss+xml" title="ara -- AI research arm" href="${SITE_ORIGIN}/feed.xml" />`,
    `<link rel="alternate" type="text/plain" title="llms.txt" href="${SITE_ORIGIN}/llms.txt" />`,
    jsonLdTag(jsonLd),
  ];
  const snapshot = [
    '<section class="content-card forecast-static-page">',
    '<div class="content-card-body">',
    '<p class="ara-eyebrow">Independent AI intelligence</p>',
    '<h1>AI news, model forecasts, and research</h1>',
    `<p>${htmlEscapeAttr(desc)}</p>`,
    '<nav aria-label="Explore ara">',
    '<ul>',
    '<li><a href="/today">Daily AI digest</a></li>',
    '<li><a href="/twitter">Twitter/X AI signal reports</a></li>',
    '<li><a href="/models">AI model forecasts and prediction markets</a></li>',
    '<li><a href="/research">Long-form generative research</a></li>',
    '<li><a href="/wiki">LLM wiki</a></li>',
    '<li><a href="/frontpage">Daily AI newspaper</a></li>',
    '</ul>',
    '</nav>',
    '</div>',
    '</section>',
  ].join('');
  return inlineContent(applySeoBlock(template, metaBlock), snapshot);
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

function buildDigestPage(template, digest, shareImageUrl, policy = datedPagePolicy('today', digest.date, SITE_ORIGIN)) {
  const md = readFileSync(digest.path, 'utf8');
  const title = `AI Daily Digest -- ${digest.date}`;
  const desc = digestDescription(md);
  const url = policy.canonicalUrl;
  const bodyHtml = sanitizeFragment(marked.parse(md));

  const jsonLd = {
    '@type': 'Article',
    headline: title,
    description: desc,
    datePublished: digest.date,
    dateModified: digest.date,
    inLanguage: 'en',
    isAccessibleForFree: true,
    author: publisherNode(),
    publisher: publisherNode(),
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    about: [
      { '@type': 'Thing', name: 'AI news' },
      { '@type': 'Thing', name: 'model releases' },
      { '@type': 'Thing', name: 'AI research' },
    ],
    url,
  };
  if (shareImageUrl) jsonLd.image = shareImageUrl;

  const metaBlock = [
    `<title>${htmlEscapeAttr(title)} -- ara</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    ...sharedMetaTags(title, desc),
    `<link rel="canonical" href="${url}" />`,
    `<meta name="robots" content="${policy.indexable ? 'index,follow,max-image-preview:large,max-snippet:-1' : 'noindex,follow'}" />`,
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
    `<link rel="alternate" type="text/plain" title="llms.txt" href="${SITE_ORIGIN}/llms.txt" />`,
    jsonLdTag({ '@context': 'https://schema.org', '@graph': [organizationNode(), jsonLd] }),
  ];

  let html = applySeoBlock(template, metaBlock);
  html = inlineContent(
    html,
    singleH1Snapshot(title, bodyHtml),
  );
  return html;
}

function datedMarkdownRecords(dir, pattern) {
  if (!existsSync(dir)) return [];
  return sortDatedRecords(readdirSync(dir).map(name => {
    const match = pattern.exec(name);
    return match ? { date: match[1], path: join(dir, name), name } : null;
  }).filter(Boolean));
}

function digestRecords() {
  return datedMarkdownRecords(digestDir, /^(\d{4}-\d{2}-\d{2})-digest\.md$/);
}

function twitterRecords() {
  return datedMarkdownRecords(twitterDir, /^(\d{4}-\d{2}-\d{2})\.md$/);
}

function renderedWordCount(markdown) {
  const text = decodeEntities(stripTags(sanitizeFragment(marked.parse(markdown))));
  return compactText(text).split(/\s+/).filter(Boolean).length;
}

function frontPageRecords() {
  if (!existsSync(frontPageDir)) return [];
  return sortDatedRecords(readdirSync(frontPageDir).map(name => {
    const match = /^(\d{4}-\d{2}-\d{2})-front-page\.png$/.exec(name);
    if (!match) return null;
    const notesPath = join(frontPageDir, `${match[1]}-front-page.ara.md`);
    return {
      date: match[1],
      path: join(frontPageDir, name),
      notesPath: existsSync(notesPath) ? notesPath : null,
      imageUrl: `${SITE_ORIGIN}/research/front-page/${name}`,
    };
  }).filter(Boolean));
}

function buildTwitterPage(template, report, shareImageUrl, policy = datedPagePolicy('twitter', report.date, SITE_ORIGIN)) {
  const markdown = readFileSync(report.path, 'utf8');
  const title = `Twitter/X AI signal report -- ${report.date}`;
  const description = digestDescription(markdown);
  const bodyHtml = sanitizeFragment(marked.parse(markdown));
  const reportNode = {
    '@type': 'Report',
    headline: title,
    description,
    datePublished: report.date,
    dateModified: report.date,
    inLanguage: 'en',
    isAccessibleForFree: true,
    author: publisherNode(),
    publisher: publisherNode(),
    mainEntityOfPage: { '@type': 'WebPage', '@id': policy.canonicalUrl },
    about: [{ '@type': 'Thing', name: 'AI news from Twitter and X' }],
    url: policy.canonicalUrl,
  };
  if (shareImageUrl) reportNode.image = shareImageUrl;
  const metaBlock = standardMetaBlock({
    title,
    description,
    canonicalUrl: policy.canonicalUrl,
    shareImage: shareImageUrl,
    type: 'article',
    indexable: policy.indexable,
    published: report.date,
    modified: report.date,
    jsonLd: { '@context': 'https://schema.org', '@graph': [organizationNode(), reportNode] },
  });
  return inlineContent(
    applySeoBlock(template, metaBlock),
    singleH1Snapshot(title, bodyHtml),
  );
}

function frontPageDescription(record) {
  const digestPath = join(digestDir, `${record.date}-digest.md`);
  if (existsSync(digestPath)) return digestDescription(readFileSync(digestPath, 'utf8'));
  if (record.notesPath) {
    const notes = readFileSync(record.notesPath, 'utf8');
    const deck = notes.match(/^deck:\s*["']?(.+?)["']?\s*$/m)?.[1];
    if (deck) return truncateDescription(deck);
  }
  return `The ara daily AI newspaper front page for ${record.date}, generated from the verified daily digest.`;
}

function buildFrontPagePage(template, record, policy = datedPagePolicy('frontpage', record.date, SITE_ORIGIN)) {
  const title = `Daily AI newspaper -- ${record.date}`;
  const description = frontPageDescription(record);
  const image = {
    url: record.imageUrl,
    alt: `ara daily AI newspaper front page for ${record.date}`,
  };
  const workNode = {
    '@type': 'CreativeWork',
    headline: title,
    description,
    datePublished: record.date,
    dateModified: record.date,
    inLanguage: 'en',
    isAccessibleForFree: true,
    author: publisherNode(),
    publisher: publisherNode(),
    mainEntityOfPage: { '@type': 'WebPage', '@id': policy.canonicalUrl },
    image: record.imageUrl,
    url: policy.canonicalUrl,
  };
  const metaBlock = standardMetaBlock({
    title,
    description,
    canonicalUrl: policy.canonicalUrl,
    shareImage: image,
    type: 'article',
    indexable: policy.indexable,
    published: record.date,
    modified: record.date,
    jsonLd: { '@context': 'https://schema.org', '@graph': [organizationNode(), workNode] },
  });
  const body = [
    `<p>${htmlEscapeAttr(description)}</p>`,
    `<figure><img src="${htmlEscapeAttr(record.imageUrl)}" alt="${htmlEscapeAttr(image.alt)}" loading="eager" decoding="async"><figcaption>${htmlEscapeAttr(title)}</figcaption></figure>`,
    `<p><a href="/today/${htmlEscapeAttr(record.date)}">Read the source daily digest</a></p>`,
  ].join('');
  return inlineContent(
    applySeoBlock(template, metaBlock),
    singleH1Snapshot(title, body),
  );
}

function buildArchivePage(template, {
  route,
  title,
  description,
  eyebrow,
  items,
  shareImageUrl,
}) {
  const url = `${SITE_ORIGIN}${route}`;
  const normalized = items.map((item, index) => ({ ...item, position: index + 1 }));
  const collectionNode = {
    '@type': 'CollectionPage',
    name: title,
    description,
    url,
    isPartOf: { '@id': `${SITE_ORIGIN}/#website` },
    mainEntity: {
      '@type': 'ItemList',
      numberOfItems: normalized.length,
      itemListElement: normalized.map(item => ({
        '@type': 'ListItem',
        position: item.position,
        name: item.title,
        url: `${SITE_ORIGIN}${item.route}`,
      })),
    },
  };
  const metaBlock = standardMetaBlock({
    title,
    description,
    canonicalUrl: url,
    shareImage: shareImageUrl,
    jsonLd: { '@context': 'https://schema.org', '@graph': [organizationNode(), collectionNode] },
  });
  const list = normalized.map(item => [
    '<li>',
    `<a href="${htmlEscapeAttr(item.route)}"><strong>${htmlEscapeAttr(item.title)}</strong></a>`,
    item.meta ? `<p>${htmlEscapeAttr(item.meta)}</p>` : '',
    item.description ? `<p>${htmlEscapeAttr(truncateDescription(compactText(item.description), 240))}</p>` : '',
    '</li>',
  ].filter(Boolean).join('')).join('');
  const snapshot = [
    '<section class="content-card forecast-static-page">',
    '<div class="content-card-body">',
    `<p class="ara-eyebrow">${htmlEscapeAttr(eyebrow)}</p>`,
    `<h1>${htmlEscapeAttr(title)}</h1>`,
    `<p>${htmlEscapeAttr(description)}</p>`,
    `<ol>${list}</ol>`,
    '</div>',
    '</section>',
  ].join('');
  return inlineContent(applySeoBlock(template, metaBlock), snapshot);
}

function buildNoindexPage(template, { route, canonicalRoute, title, description, body, shareImageUrl }) {
  const canonicalUrl = `${SITE_ORIGIN}${canonicalRoute}`;
  const metaBlock = standardMetaBlock({
    title,
    description,
    canonicalUrl,
    shareImage: shareImageUrl,
    indexable: false,
  });
  return inlineContent(
    applySeoBlock(template, metaBlock),
    singleH1Snapshot(title, `<p>${htmlEscapeAttr(body || description)}</p>`),
  );
}

function polymarketEventUrl(mapping) {
  return `https://polymarket.com/event/${encodeURIComponent(String(mapping.event_slug))}`;
}

// A crawler-facing forecast page intentionally contains only committed
// evidence and mapping metadata. Live odds remain a fail-soft browser concern;
// baking a build-time price into OG copy would make shared cards stale or false.
function buildForecastPage(template, ticket, shareImageUrl) {
  const record = forecastSeoRecord(ticket, SITE_ORIGIN);
  const desc = truncateDescription(record.description);
  const published = ticket.created_at || ticket.updated_at;
  const modified = ticket.updated_at || ticket.created_at;
  const keywords = [
    'AI forecast',
    'prediction markets',
    'Polymarket',
    ticket.company,
    ticket.model,
    ...(Array.isArray(ticket.labels) ? ticket.labels : []),
  ].filter(Boolean);
  const marketUrls = ticket.polymarket.map(polymarketEventUrl);
  const sourceUrls = (Array.isArray(ticket.sources) ? ticket.sources : [])
    .filter(source => /^https?:\/\/\S+$/i.test(String(source)));
  const jsonLd = {
    '@type': 'Report',
    headline: record.title,
    description: desc,
    datePublished: published,
    dateModified: modified,
    inLanguage: 'en',
    isAccessibleForFree: true,
    author: publisherNode(),
    publisher: publisherNode(),
    mainEntityOfPage: { '@type': 'WebPage', '@id': record.url },
    about: record.questions.map(name => ({ '@type': 'Thing', name })),
    keywords,
    citation: sourceUrls,
    sameAs: marketUrls,
    url: record.url,
  };
  if (shareImageUrl) jsonLd.image = shareImageUrl;

  const metaBlock = [
    `<title>${htmlEscapeAttr(record.title)} -- ara</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    ...sharedMetaTags(record.title, desc),
    `<meta name="news_keywords" content="${htmlEscapeAttr(keywords.join(', '))}" />`,
    `<link rel="canonical" href="${record.url}" />`,
    `<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />`,
    `<meta property="og:type" content="article" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(record.title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${record.url}" />`,
    `<meta property="og:site_name" content="ara -- AI research arm" />`,
    published ? `<meta property="article:published_time" content="${htmlEscapeAttr(published)}" />` : '',
    modified ? `<meta property="article:modified_time" content="${htmlEscapeAttr(modified)}" />` : '',
    ...imageMetaTags(shareImageUrl, record.title),
    `<meta name="twitter:card" content="${shareImageUrl ? 'summary_large_image' : 'summary'}" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(record.title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="alternate" type="application/rss+xml" title="ara -- AI research arm" href="${SITE_ORIGIN}/feed.xml" />`,
    `<link rel="alternate" type="text/plain" title="llms.txt" href="${SITE_ORIGIN}/llms.txt" />`,
    jsonLdTag({ '@context': 'https://schema.org', '@graph': [organizationNode(), jsonLd] }),
  ].filter(Boolean);

  const marketItems = ticket.polymarket.map(mapping => {
    const outcome = String(mapping.outcome || '').trim();
    return [
      '<li>',
      `<a href="${htmlEscapeAttr(polymarketEventUrl(mapping))}" rel="noopener noreferrer">${htmlEscapeAttr(mapping.question)}</a>`,
      outcome ? ` <span>(${htmlEscapeAttr(outcome)} outcome)</span>` : '',
      '</li>',
    ].join('');
  }).join('');
  const sources = sourceUrls.map(source =>
    `<li><a href="${htmlEscapeAttr(source)}" rel="noopener noreferrer">${htmlEscapeAttr(source)}</a></li>`,
  ).join('');
  const bodyHtml = sanitizeFragment(marked.parse(String(ticket.body || '')));
  const status = String(ticket.status || 'tracked').replace(/-/g, ' ');
  const snapshot = [
    '<article class="content-card forecast-static-page">',
    '<div class="content-card-body">',
    '<p class="ara-eyebrow">AI forecast · prediction-market linked</p>',
    `<h1>${htmlEscapeAttr(ticket.title)}</h1>`,
    `<p>${htmlEscapeAttr(ticket.company)} · ${htmlEscapeAttr(status)} · verified · updated ${htmlEscapeAttr(ticket.updated_at || 'unknown')}</p>`,
    '<section><h2>Linked prediction markets</h2>',
    `<ul>${marketItems}</ul>`,
    '<p>Live probabilities load in the interactive view and may be unavailable. Market links and questions are committed mappings; no price is asserted in this static snapshot.</p>',
    '</section>',
    bodyHtml ? `<section><h2>Forecast evidence</h2>${bodyHtml}</section>` : '',
    sources ? `<section><h2>Sources</h2><ul>${sources}</ul></section>` : '',
    '</div>',
    '</article>',
  ].filter(Boolean).join('');

  return inlineContent(applySeoBlock(template, metaBlock), snapshot);
}

function buildModelsPage(template, forecastTickets, shareImageUrl) {
  const url = `${SITE_ORIGIN}/models`;
  const title = 'AI model forecasts and prediction markets';
  const desc = truncateDescription(
    'Verified AI model-release forecasts with evidence timelines and linked prediction-market questions. Live probabilities load in the interactive model board.',
  );
  const forecastRecords = forecastTickets.map(ticket => ({
    ticket,
    record: forecastSeoRecord(ticket, SITE_ORIGIN),
  }));
  const jsonLd = {
    '@type': 'CollectionPage',
    name: title,
    description: desc,
    url,
    isPartOf: { '@id': `${SITE_ORIGIN}/#website` },
    mainEntity: {
      '@type': 'ItemList',
      numberOfItems: forecastRecords.length,
      itemListElement: forecastRecords.map(({ record }, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        name: record.title,
        url: record.url,
      })),
    },
  };
  const metaBlock = [
    `<title>${htmlEscapeAttr(title)} -- ara</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    ...sharedMetaTags(title, desc),
    `<link rel="canonical" href="${url}" />`,
    `<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />`,
    `<meta property="og:type" content="website" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${url}" />`,
    `<meta property="og:site_name" content="ara -- AI research arm" />`,
    ...imageMetaTags(shareImageUrl, title),
    `<meta name="twitter:card" content="${shareImageUrl ? 'summary_large_image' : 'summary'}" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="alternate" type="application/rss+xml" title="ara -- AI research arm" href="${SITE_ORIGIN}/feed.xml" />`,
    `<link rel="alternate" type="text/plain" title="llms.txt" href="${SITE_ORIGIN}/llms.txt" />`,
    jsonLdTag({ '@context': 'https://schema.org', '@graph': [organizationNode(), jsonLd] }),
  ];
  const rows = forecastRecords.map(({ ticket, record }) => [
    '<li>',
    `<a href="${htmlEscapeAttr(record.route)}"><strong>${htmlEscapeAttr(ticket.title)}</strong></a>`,
    `<p>${htmlEscapeAttr(ticket.company)} · ${htmlEscapeAttr(String(ticket.status).replace(/-/g, ' '))} · updated ${htmlEscapeAttr(ticket.updated_at)}</p>`,
    `<p>${htmlEscapeAttr(record.questions.join(' · '))}</p>`,
    '</li>',
  ].join('')).join('');
  const snapshot = [
    '<section class="content-card forecast-static-page">',
    '<div class="content-card-body">',
    '<p class="ara-eyebrow">AI forecast radar</p>',
    `<h1>${htmlEscapeAttr(title)}</h1>`,
    `<p>${htmlEscapeAttr(desc)}</p>`,
    rows ? `<ol>${rows}</ol>` : '<p>No verified market-linked forecasts are currently published.</p>',
    '<p>Probabilities are informational only and may be unavailable. Each forecast page identifies its committed market mapping and source evidence.</p>',
    '</div>',
    '</section>',
  ].join('');
  return inlineContent(applySeoBlock(template, metaBlock), snapshot);
}

function wikiPageImages(page, fallbackAlt) {
  if (!Array.isArray(page?.images)) return [];
  return imageMetaItems(
    page.images.map(img => ({
      url: img?.url,
      alt: String(img?.alt || fallbackAlt || ''),
    })),
    fallbackAlt,
  );
}

function wikiImageGalleryHtml(page, title) {
  if (!Array.isArray(page?.images)) return '';
  const figures = page.images
    .map(img => {
      const url = absoluteImageUrl(img?.url);
      const alt = String(img?.alt || title || '').trim();
      if (!url || !alt) return '';
      const caption = String(img?.caption || '').trim();
      const credit = String(img?.credit || '').trim();
      const sourceUrl = /^https?:\/\/\S+$/i.test(String(img?.source_url || '')) ? String(img.source_url) : '';
      const creditHtml = credit
        ? sourceUrl
          ? `<a href="${htmlEscapeAttr(sourceUrl)}" class="wiki-image-credit">${htmlEscapeAttr(credit)}</a>`
          : `<span class="wiki-image-credit">${htmlEscapeAttr(credit)}</span>`
        : sourceUrl
          ? `<a href="${htmlEscapeAttr(sourceUrl)}" class="wiki-image-credit">Source</a>`
          : '';
      const captionParts = [];
      if (caption) captionParts.push(`<span class="wiki-image-caption-text">${htmlEscapeAttr(caption)}</span>`);
      if (creditHtml) captionParts.push(creditHtml);
      const captionHtml = captionParts.join(' ');
      return [
        '<figure class="wiki-image-figure">',
        `<img src="${htmlEscapeAttr(url)}" alt="${htmlEscapeAttr(alt)}" loading="lazy" decoding="async">`,
        captionHtml ? `<figcaption class="wiki-image-caption">${captionHtml}</figcaption>` : '',
        '</figure>',
      ].filter(Boolean).join('');
    })
    .filter(Boolean);
  if (!figures.length) return '';
  const mode = figures.length === 1 ? 'single' : 'multi';
  return `<div class="wiki-image-gallery wiki-image-gallery--${mode}">${figures.join('')}</div>`;
}

function buildWikiPage(template, page, shareImageUrl) {
  const url = `${SITE_ORIGIN}/wiki/${page.slug}`;
  const title = page.title || page.slug;
  const desc = truncateDescription(decodeEntities(stripTags(page.summary || title)));
  const keywords = [
    ...(Array.isArray(page.tags) ? page.tags : []),
    ...(Array.isArray(page.aliases) ? page.aliases : []),
  ].filter(Boolean);

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
    '@type': 'TechArticle',
    headline: title,
    description: desc,
    datePublished: page.created_at,
    dateModified: page.updated_at || page.created_at,
    inLanguage: 'en',
    isAccessibleForFree: true,
    author: publisherNode(),
    publisher: publisherNode(),
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    keywords,
    about: keywords.map(name => ({ '@type': 'Thing', name })),
    url,
  };
  const pageImages = wikiPageImages(page, title);
  const metaImages = pageImages.length
    ? pageImages
    : imageMetaItems(shareImageUrl, title);
  if (metaImages.length) jsonLd.image = metaImages.map(img => img.url);

  const metaBlock = [
    `<title>${htmlEscapeAttr(title)} -- ara wiki</title>`,
    `<meta name="description" content="${htmlEscapeAttr(desc)}" />`,
    ...sharedMetaTags(title, desc),
    `<link rel="canonical" href="${url}" />`,
    `<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />`,
    `<meta property="og:type" content="article" />`,
    `<meta property="og:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta property="og:description" content="${htmlEscapeAttr(desc)}" />`,
    `<meta property="og:url" content="${url}" />`,
    `<meta property="og:site_name" content="ara -- AI research arm" />`,
    ...imageMetaTags(metaImages, title),
    `<meta name="twitter:card" content="${metaImages.length ? 'summary_large_image' : 'summary'}" />`,
    `<meta name="twitter:title" content="${htmlEscapeAttr(title)}" />`,
    `<meta name="twitter:description" content="${htmlEscapeAttr(desc)}" />`,
    `<link rel="alternate" type="application/rss+xml" title="ara -- AI research arm" href="${SITE_ORIGIN}/feed.xml" />`,
    `<link rel="alternate" type="text/plain" title="llms.txt" href="${SITE_ORIGIN}/llms.txt" />`,
    jsonLdTag({ '@context': 'https://schema.org', '@graph': [organizationNode(), jsonLd] }),
  ];

  let html = applySeoBlock(template, metaBlock);
  html = inlineContent(
    html,
    singleH1Snapshot(title, `${wikiImageGalleryHtml(page, title)}${bodyHtml}`),
  );
  return html;
}

function buildSitemap(entries, wikiPages, forecastTickets, datedPages) {
  const today = new Date().toISOString().slice(0, 10);
  const rootEntries = [
    { loc: SITE_ORIGIN + '/', priority: '1.0' },
    { loc: SITE_ORIGIN + '/models', priority: '0.7' },
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

  const forecastEntries = (forecastTickets || []).map(ticket => ({
    loc: forecastSeoRecord(ticket, SITE_ORIGIN).url,
    lastmod: (ticket.updated_at || ticket.created_at || today).slice(0, 10),
    priority: '0.7',
  }));

  const reportEntries = (datedPages || []).map(page => ({
    loc: `${SITE_ORIGIN}${page.route}`,
    lastmod: page.date,
    priority: page.section === 'today' ? '0.8' : page.section === 'twitter' ? '0.6' : '0.5',
  }));

  const all = [...rootEntries, ...reportEntries, ...articleEntries, ...wikiEntries, ...forecastEntries]
    .sort((a, b) => a.loc.localeCompare(b.loc));
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
    'User-agent: GPTBot',
    'Allow: /',
    '',
    'User-agent: ClaudeBot',
    'Allow: /',
    '',
    'User-agent: PerplexityBot',
    'Allow: /',
    '',
    'User-agent: CCBot',
    'Allow: /',
    '',
    `Sitemap: ${SITE_ORIGIN}/sitemap.xml`,
    '',
  ].join('\n');
}

function markdownLine(s) {
  return compactText(s).replace(/[\[\]]/g, '');
}

function recentDigestEntries(limit = 10) {
  if (!existsSync(digestDir)) return [];
  const re = /^(\d{4}-\d{2}-\d{2})-digest\.md$/;
  return readdirSync(digestDir)
    .map(n => (re.exec(n) || [])[1])
    .filter(Boolean)
    .sort()
    .reverse()
    .slice(0, limit)
    .map(date => {
      const md = readFileSync(join(digestDir, `${date}-digest.md`), 'utf8');
      return {
        date,
        title: `AI Daily Digest -- ${date}`,
        url: `${SITE_ORIGIN}/today/${date}`,
        description: digestDescription(md),
      };
    });
}

function buildLlmsTxt(entries, wikiPages, forecastTickets) {
  const today = new Date().toISOString().slice(0, 10);
  const digests = recentDigestEntries(10);
  const latestTwitter = twitterRecords().at(-1);
  const recentArticles = entries
    .filter(e => e.kind !== 'standalone')
    .slice()
    .sort((a, b) => String(b.created_at || '').localeCompare(String(a.created_at || '')))
    .slice(0, 15);
  const recentWiki = (wikiPages || [])
    .slice()
    .sort((a, b) => String(b.updated_at || b.created_at || '').localeCompare(String(a.updated_at || a.created_at || '')))
    .slice(0, 20);

  const lines = [
    '# ara -- AI research arm',
    '',
    `> ${SITE_DESCRIPTION}`,
    '',
    `Updated: ${today}`,
    '',
    '## Canonical entry points',
    '',
    `- [Homepage](${SITE_ORIGIN}/): Live AI-news dashboard and archive navigation.`,
    `- [Latest daily digest](${digests[0]?.url || `${SITE_ORIGIN}/today`}): Daily AI news synthesis.`,
    latestTwitter ? `- [Latest Twitter/X report](${SITE_ORIGIN}/twitter/${latestTwitter.date}): Source-attributed AI signals from Twitter/X.` : '',
    `- [Research archive](${SITE_ORIGIN}/research): Long-form generative research articles.`,
    `- [LLM Wiki](${SITE_ORIGIN}/wiki): Entity, concept, and theme pages built from curated AI-news synthesis.`,
    `- [Model timeline](${SITE_ORIGIN}/models): Model-release timeline and tickets.`,
    `- [RSS feed](${SITE_ORIGIN}/feed.xml): Recent digests and research in RSS 2.0.`,
    `- [Sitemap](${SITE_ORIGIN}/sitemap.xml): Full crawl map.`,
    '',
    '## Citation guidance',
    '',
    '- Prefer canonical URLs from this file, the sitemap, or each page canonical tag.',
    '- Treat dated digest anchors as daily snapshots and research article URLs as stable article pages.',
    '- The site is generated from public research artifacts in the GitHub repository linked on the homepage.',
    '',
  ];

  if (digests.length) {
    lines.push('## Recent daily digests', '');
    for (const digest of digests) {
      lines.push(`- [${markdownLine(digest.title)}](${digest.url}): ${markdownLine(digest.description)}`);
    }
    lines.push('');
  }

  if (recentArticles.length) {
    lines.push('## Recent generative research', '');
    for (const article of recentArticles) {
      const title = markdownLine(article.title || article.slug);
      const tags = Array.isArray(article.tags) && article.tags.length
        ? ` Tags: ${article.tags.map(markdownLine).join(', ')}.`
        : '';
      const desc = markdownLine(article.prompt || title);
      lines.push(`- [${title}](${SITE_ORIGIN}/research/${article.slug}): ${desc}${tags}`);
    }
    lines.push('');
  }

  if (recentWiki.length) {
    lines.push('## Recently updated wiki pages', '');
    for (const page of recentWiki) {
      const title = markdownLine(page.title || page.slug);
      const desc = markdownLine(page.summary || title);
      lines.push(`- [${title}](${SITE_ORIGIN}/wiki/${page.slug}): ${desc}`);
    }
    lines.push('');
  }

  if (forecastTickets?.length) {
    lines.push('## Verified prediction-market forecasts', '');
    for (const ticket of forecastTickets) {
      const record = forecastSeoRecord(ticket, SITE_ORIGIN);
      lines.push(`- [${markdownLine(record.title)}](${record.url}): ${markdownLine(record.description)}`);
    }
    lines.push('');
  }

  return lines.join('\n') + '\n';
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
        link: `${SITE_ORIGIN}/today/${date}`,
        guid: `${SITE_ORIGIN}/today/${date}`,
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
const shareImageUrl = await findShareImageUrl();

const entries = existsSync(indexJsonPath)
  ? JSON.parse(readFileSync(indexJsonPath, 'utf8'))
  : [];
if (!existsSync(indexJsonPath)) {
  console.warn(`postbuild-seo: ${indexJsonPath} not found -- no article pages`);
}

// 1) Generative article pages. Every non-standalone article gets a
//    deterministic typographic social card unless it ships its own artifact
//    image (articleArtifactImage precedence is unchanged).
let written = 0;
let skipped = 0;
let cardAttempts = 0;
let cardsGenerated = 0;
const generatedArticleImages = new Map();
const articleRows = [];
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
  const indexable = isIndexableResearchEntry(row);
  const { title: extractedTitle, desc: extractedDesc } = extractMeta(articleHtml);
  const cardTitle = extractedTitle || row.title || row.slug;
  if (!articleArtifactImage(row, cardTitle)) {
    cardAttempts++;
    try {
      const image = await generateArticleSocialCard(row, cardTitle, extractedDesc);
      if (image) {
        generatedArticleImages.set(row.slug, image);
        cardsGenerated++;
      }
    } catch (e) {
      console.warn(`postbuild-seo: social card failed for ${row.slug}: ${e.message}`);
    }
  }
  const page = buildArticlePage(template, row, articleHtml, shareImageUrl, generatedArticleImages, indexable);
  const outDir = join(dist, 'research', row.slug);
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'index.html'), page);
  articleRows.push({ row, articleHtml, outDir, indexable });
  written++;
}

// Per-card failures are tolerable (that article falls back to the site share
// image), but EVERY card failing means the environment is broken — resvg
// binding didn't load, fonts missing — and shipping a green build with zero
// cards would hide it indefinitely (CI never runs the Dockerfile; see
// CLAUDE.md load-bearing rule 3). Fail the build instead.
if (cardAttempts > 0 && cardsGenerated === 0) {
  console.error(
    `postbuild-seo: all ${cardAttempts} social-card renders failed — ` +
    'resvg/native-binding or system-font breakage; refusing to ship a build with no article cards',
  );
  process.exit(1);
}

// 2) Dated editorial reports. Each real artifact receives one self-canonical
// route. Undated convenience routes are noindex aliases to the latest dated
// artifact, so they remain useful to humans without duplicating the index.
const digests = digestRecords();
const twitterReports = twitterRecords();
const frontPages = frontPageRecords();
const datedPages = [];
for (const digest of digests) {
  const policy = datedPagePolicy('today', digest.date, SITE_ORIGIN);
  const outDir = join(dist, 'today', digest.date);
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'index.html'), buildDigestPage(template, digest, shareImageUrl, policy));
  datedPages.push({ section: 'today', date: digest.date, route: policy.route });
}
const latestDigestRecord = digests.at(-1) || null;
if (latestDigestRecord) {
  const outDir = join(dist, 'today');
  mkdirSync(outDir, { recursive: true });
  writeFileSync(
    join(outDir, 'index.html'),
    buildDigestPage(
      template,
      latestDigestRecord,
      shareImageUrl,
      latestAliasPolicy('today', latestDigestRecord.date, SITE_ORIGIN),
    ),
  );
}

for (const report of twitterReports) {
  const markdown = readFileSync(report.path, 'utf8');
  report.wordCount = renderedWordCount(markdown);
  const basePolicy = datedPagePolicy('twitter', report.date, SITE_ORIGIN);
  const policy = report.wordCount >= 300
    ? basePolicy
    : { ...basePolicy, indexable: false };
  const outDir = join(dist, 'twitter', report.date);
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'index.html'), buildTwitterPage(template, report, shareImageUrl, policy));
  if (policy.indexable) datedPages.push({ section: 'twitter', date: report.date, route: policy.route });
}
const latestTwitterRecord = twitterReports.at(-1) || null;
if (latestTwitterRecord) {
  const outDir = join(dist, 'twitter');
  mkdirSync(outDir, { recursive: true });
  writeFileSync(
    join(outDir, 'index.html'),
    buildTwitterPage(
      template,
      latestTwitterRecord,
      shareImageUrl,
      latestAliasPolicy('twitter', latestTwitterRecord.date, SITE_ORIGIN),
    ),
  );
}

for (const frontPage of frontPages) {
  const policy = {
    route: `/frontpage/${frontPage.date}`,
    canonicalRoute: `/today/${frontPage.date}`,
    canonicalUrl: `${SITE_ORIGIN}/today/${frontPage.date}`,
    indexable: false,
  };
  const outDir = join(dist, 'frontpage', frontPage.date);
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'index.html'), buildFrontPagePage(template, frontPage, policy));
}
const latestFrontPageRecord = frontPages.at(-1) || null;
if (latestFrontPageRecord) {
  const outDir = join(dist, 'frontpage');
  mkdirSync(outDir, { recursive: true });
  writeFileSync(
    join(outDir, 'index.html'),
    buildFrontPagePage(
      template,
      latestFrontPageRecord,
      {
        route: '/frontpage',
        canonicalRoute: `/today/${latestFrontPageRecord.date}`,
        canonicalUrl: `${SITE_ORIGIN}/today/${latestFrontPageRecord.date}`,
        indexable: false,
      },
    ),
  );
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


// Archive hubs are indexable collections, not generic SPA shells. Their
// direct links also keep valuable articles and wiki pages within a short crawl
// path from the homepage.
const publishedEntries = articleRows.filter(item => item.indexable).map(item => item.row);
const researchItems = publishedEntries
  .slice()
  .sort((a, b) => String(b.created_at || '').localeCompare(String(a.created_at || '')))
  .map(row => ({
    route: `/research/${row.slug}`,
    title: row.title || row.slug,
    meta: row.created_at ? String(row.created_at).slice(0, 10) : '',
    description: row.prompt || row.title || row.slug,
  }));
const researchHubDir = join(dist, 'research');
mkdirSync(researchHubDir, { recursive: true });
writeFileSync(join(researchHubDir, 'index.html'), buildArchivePage(template, {
  route: '/research',
  title: 'AI research archive',
  description: 'Source-cited, long-form research on AI models, companies, infrastructure, policy, and emerging technical claims.',
  eyebrow: 'Generative research',
  items: researchItems,
  shareImageUrl,
}));

const wikiItems = wikiPages
  .slice()
  .sort((a, b) => String(a.title || a.slug).localeCompare(String(b.title || b.slug)))
  .map(page => ({
    route: `/wiki/${page.slug}`,
    title: page.title || page.slug,
    meta: [page.type, page.updated_at || page.created_at].filter(Boolean).join(' · '),
    description: decodeEntities(stripTags(page.summary || page.title || page.slug)),
  }));
const wikiHubDir = join(dist, 'wiki');
mkdirSync(wikiHubDir, { recursive: true });
writeFileSync(join(wikiHubDir, 'index.html'), buildArchivePage(template, {
  route: '/wiki',
  title: 'LLM and AI wiki',
  description: 'A maintained knowledge base of AI labs, models, infrastructure concepts, policy themes, and market participants.',
  eyebrow: 'Compounding knowledge base',
  items: wikiItems,
  shareImageUrl,
}));

// 4) Verified model forecasts with committed Polymarket mappings. Read the
// sanitized index emitted by prebuild so crawler and runtime contracts cannot
// drift. Ordinary/unverified tickets intentionally receive no static page.
let forecastTickets = [];
let forecastWritten = 0;
if (existsSync(distTicketIndexPath)) {
  try {
    const ticketIndex = JSON.parse(readFileSync(distTicketIndexPath, 'utf8'));
    forecastTickets = mappedForecastTickets(ticketIndex);
    for (const ticket of forecastTickets) {
      const outDir = join(dist, 'models', 'forecast', ticket.slug);
      mkdirSync(outDir, { recursive: true });
      writeFileSync(join(outDir, 'index.html'), buildForecastPage(template, ticket, shareImageUrl));
      forecastWritten++;
    }
  } catch (e) {
    console.warn(`postbuild-seo: ticket index parse failed (${e.message}); skipping forecast pages`);
  }
}
const distModelsDir = join(dist, 'models');
mkdirSync(distModelsDir, { recursive: true });
writeFileSync(join(distModelsDir, 'index.html'), buildModelsPage(template, forecastTickets, shareImageUrl));

// Historical /models/YYYY-MM-DD URLs all render the same live ticket board.
// Preserve those legacy links, but canonicalize and noindex them instead of
// presenting 100+ duplicate pages to crawlers.
const modelTimelineRecords = datedMarkdownRecords(modelTimelineDir, /^(\d{4}-\d{2}-\d{2})-timeline\.md$/);
for (const record of modelTimelineRecords) {
  const outDir = join(distModelsDir, record.date);
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'index.html'), buildNoindexPage(template, {
    route: `/models/${record.date}`,
    canonicalRoute: '/models',
    title: `AI model timeline -- ${record.date}`,
    description: 'This historical URL resolves to the live AI model forecast board.',
    body: 'The model board is maintained as a live ticket collection. Continue to the canonical model forecasts page.',
    shareImageUrl,
  }));
}

// Operational and design-preview surfaces are public for transparency and QA,
// but they are not search landing pages.
const agentsDescription = existsSync(armTimelinePath)
  ? 'Live operational timeline for the autonomous agents and scheduled workflows that maintain ara.'
  : 'Operational surface for the autonomous agents that maintain ara.';
const agentsDir = join(dist, 'agents');
mkdirSync(agentsDir, { recursive: true });
writeFileSync(join(agentsDir, 'index.html'), buildNoindexPage(template, {
  route: '/agents',
  canonicalRoute: '/agents',
  title: 'ara agent operations',
  description: agentsDescription,
  body: agentsDescription,
  shareImageUrl,
}));
const focusReaderDir = join(dist, 'design', 'focus-reader');
mkdirSync(focusReaderDir, { recursive: true });
writeFileSync(join(focusReaderDir, 'index.html'), buildNoindexPage(template, {
  route: '/design/focus-reader',
  canonicalRoute: '/design/focus-reader',
  title: 'Focus reader design preview',
  description: 'An internal design preview for ara reading experiences.',
  body: 'This route is a design and quality-assurance surface, not a published research page.',
  shareImageUrl,
}));

// 5) Homepage -- rewrite dist/index.html LAST (it was the template above, so
//    article/today/wiki pages inherit the default block, not the homepage one).
writeFileSync(indexHtmlPath, buildHomePage(template, shareImageUrl));

// 6) sitemap.xml, robots.txt, feed.xml, llms.txt.
writeFileSync(join(dist, 'sitemap.xml'), buildSitemap(publishedEntries, wikiPages, forecastTickets, datedPages));
writeFileSync(join(dist, 'robots.txt'), buildRobots());
writeFileSync(join(dist, 'feed.xml'), buildFeed(publishedEntries, shareImageUrl));
writeFileSync(join(dist, 'llms.txt'), buildLlmsTxt(publishedEntries, wikiPages, forecastTickets));

console.log(
  `postbuild-seo: ${written} article pages (${skipped} skipped, ${cardsGenerated} social cards), ` +
  `${digests.length} digests, ${twitterReports.length} Twitter reports ` +
  `(${twitterReports.filter(report => report.wordCount >= 300).length} indexable), ` +
  `${frontPages.length} newspaper pages, ${wikiWritten} wiki pages, ` +
  `${forecastWritten} verified forecast pages, ${modelTimelineRecords.length} noindex model aliases`,
);
console.log(`postbuild-seo: share image: ${shareImageUrl || '(none found)'}`);
console.log('postbuild-seo: sitemap.xml + robots.txt + feed.xml + llms.txt written to dist/');
