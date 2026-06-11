#!/usr/bin/env node

import { readFile, writeFile } from "node:fs/promises";

const [date, output = "/tmp/front-page.html"] = process.argv.slice(2);

if (!date || !/^\d{4}-\d{2}-\d{2}$/.test(date)) {
  console.error("Usage: node scripts/render_front_page.mjs YYYY-MM-DD [/tmp/front-page.html]");
  process.exit(1);
}

const digestPath = `research/digest/${date}-digest.md`;
const markdown = await readFile(digestPath, "utf8");

const monthDay = new Intl.DateTimeFormat("en-US", {
  month: "long",
  day: "numeric",
  year: "numeric",
  timeZone: "UTC",
}).format(new Date(`${date}T00:00:00Z`));

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function stripMarkdown(value) {
  return value
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\*([^*]+)\*/g, "$1")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\*\*/g, "")
    .replace(/[*_[\]]/g, "")
    .replace(/^[-*]\s+/, "")
    .replace(/^\d+\.\s+/, "")
    .replace(/\s+/g, " ")
    .trim();
}

function markdownLinks(value) {
  const links = [];
  const re = /\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g;
  for (const match of value.matchAll(re)) {
    links.push({ label: stripMarkdown(match[1]), url: match[2] });
  }
  return links;
}

function section(name) {
  const pattern = new RegExp(`^##\\s+${name}\\s*$([\\s\\S]*?)(?=^##\\s+|\\z)`, "mi");
  return markdown.match(pattern)?.[1]?.trim() ?? "";
}

function bulletRecords(text, limit) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => /^([-*]|\d+\.)\s+/.test(line))
    .map((raw) => ({ raw, text: stripMarkdown(raw), links: markdownLinks(raw) }))
    .filter((item) => item.text)
    .slice(0, limit);
}

function bullets(text, limit) {
  return bulletRecords(text, limit).map((item) => item.text);
}

function paragraphs(text, limit) {
  return text
    .split(/\n{2,}/)
    .map(stripMarkdown)
    .filter(Boolean)
    .slice(0, limit);
}

const executive = bullets(section("Executive Summary"), 5);
const executiveRecords = bulletRecords(section("Executive Summary"), 5);
const breaking = bullets(section("Breaking News"), 3);
const breakingRecords = bulletRecords(section("Breaking News"), 3);
const models = bullets(section("Model Releases & Updates"), 3);
const modelRecords = bulletRecords(section("Model Releases & Updates"), 3);
const research = bullets(section("Research Highlights"), 5);
const researchRecords = bulletRecords(section("Research Highlights"), 5);
const business = bullets(section("Funding & Business"), 4);
const businessRecords = bulletRecords(section("Funding & Business"), 4);
const policy = bullets(section("Policy & Regulation"), 3);
const policyRecords = bulletRecords(section("Policy & Regulation"), 3);
const quoteBlock = markdown.match(/## Quote of the Day\s+>\s*([\s\S]*?)(?=\n---|\n##\s+|$)/i)?.[1] ?? "";
const quote = stripMarkdown(quoteBlock.replace(/^>\s?/gm, " "));

const lead = executive[0] || paragraphs(markdown, 1)[0] || "Today's AI digest is ready.";
const leadDeck = executive.slice(1, 4);
const issue = Math.floor((new Date(`${date}T00:00:00Z`) - new Date(`${date.slice(0, 4)}-01-01T00:00:00Z`)) / 86400000) + 1;

function uniqueSourceLinks() {
  const records = [
    ...executiveRecords,
    ...breakingRecords,
    ...modelRecords,
    ...researchRecords,
    ...businessRecords,
    ...policyRecords,
  ];
  const seen = new Set();
  const links = [];
  for (const record of records) {
    for (const link of record.links) {
      if (seen.has(link.url)) continue;
      seen.add(link.url);
      links.push({ ...link, story: record.text });
    }
  }
  return links;
}

function firstMetaContent(htmlText, names) {
  for (const name of names) {
    const patterns = [
      new RegExp(`<meta[^>]+property=["']${name}["'][^>]+content=["']([^"']+)["'][^>]*>`, "i"),
      new RegExp(`<meta[^>]+content=["']([^"']+)["'][^>]+property=["']${name}["'][^>]*>`, "i"),
      new RegExp(`<meta[^>]+name=["']${name}["'][^>]+content=["']([^"']+)["'][^>]*>`, "i"),
      new RegExp(`<meta[^>]+content=["']([^"']+)["'][^>]+name=["']${name}["'][^>]*>`, "i"),
    ];
    for (const pattern of patterns) {
      const value = htmlText.match(pattern)?.[1];
      if (value) return value.replaceAll("&amp;", "&");
    }
  }
  return "";
}

function absoluteUrl(candidate, baseUrl) {
  try {
    return new URL(candidate, baseUrl).toString();
  } catch {
    return "";
  }
}

async function fetchWithTimeout(url, options = {}, timeoutMs = 8000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

// Real browser UA — many publishers/CDNs serve og:image meta only to
// browser-like clients; a generic bot UA gets a thin or blocked response
// (which is why non-arxiv sources previously yielded no image).
const IMAGE_FETCH_UA =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";

// Hosts whose pages don't yield a usable article image:
// - arxiv.org exposes the generic arxiv LOGO as og:image, not the paper,
// - x.com / twitter.com are auth-walled to non-browser clients,
// - news.ycombinator.com pages are comment threads, not articles.
function isImageCandidate(url) {
  try {
    const host = new URL(url).hostname.replace(/^www\./, "").toLowerCase();
    if (/(^|\.)arxiv\.org$/.test(host)) return false;
    if (/(^|\.)(x|twitter)\.com$/.test(host)) return false;
    if (host === "news.ycombinator.com") return false;
    return true;
  } catch {
    return false;
  }
}

// The digest links are almost entirely arxiv (Research Highlights), so its
// only reliable og:image is the arxiv logo. Pull richer candidates from the
// raw aggregation — RSS (news/blog articles) and community (HN/Reddit outbound
// links) carry real article URLs with real og:images.
async function richSourceLinks() {
  const out = [];
  for (const file of [
    `research/rss/${date}.md`,
    `research/community/${date}-hn.md`,
    `research/community/${date}-reddit.md`,
  ]) {
    try {
      const text = await readFile(file, "utf8");
      for (const link of markdownLinks(text)) out.push({ ...link, story: link.label });
    } catch {
      // file may not exist for this date — skip it
    }
  }
  return out;
}

// Prioritised, de-duped, filtered candidate links for the lead image:
// rich aggregation sources first (real article images), digest links last.
async function imageCandidateLinks() {
  const all = [...(await richSourceLinks()), ...uniqueSourceLinks()];
  const seen = new Set();
  const out = [];
  for (const link of all) {
    if (!isImageCandidate(link.url) || seen.has(link.url)) continue;
    seen.add(link.url);
    out.push(link);
  }
  return out.slice(0, 30);
}

// Content-type headers lie often enough (CDN error pages, mislabeled
// formats) that the downloaded bytes are the only trustworthy signal.
function sniffImageFormat(bytes) {
  if (bytes.length >= 4 && bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47) return "image/png";
  if (bytes.length >= 3 && bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) return "image/jpeg";
  if (bytes.length >= 4 && bytes.toString("ascii", 0, 4) === "GIF8") return "image/gif";
  if (bytes.length >= 12 && bytes.toString("ascii", 0, 4) === "RIFF" && bytes.toString("ascii", 8, 12) === "WEBP") return "image/webp";
  if (bytes.length >= 12 && bytes.toString("ascii", 4, 8) === "ftyp" && /^av(if|is)/.test(bytes.toString("ascii", 8, 12))) return "image/avif";
  return null;
}

const ALL_IMAGE_FORMATS = ["image/png", "image/jpeg", "image/gif", "image/webp", "image/avif"];
// resvg cannot decode webp/avif — embedding one paints an empty frame on
// the rendered PNG, so the SVG path must stick to this set.
const SVG_SAFE_FORMATS = ["image/png", "image/jpeg", "image/gif"];

async function imageFromPage(link, allowedFormats) {
  try {
    const pageResponse = await fetchWithTimeout(link.url, {
      headers: {
        "user-agent": IMAGE_FETCH_UA,
        accept: "text/html,application/xhtml+xml",
      },
      redirect: "follow",
    });
    if (!pageResponse.ok) return null;
    const htmlText = (await pageResponse.text()).slice(0, 250000);
    const imageUrl = absoluteUrl(
      firstMetaContent(htmlText, ["og:image", "twitter:image", "twitter:image:src"]),
      pageResponse.url || link.url,
    );
    if (!imageUrl || imageUrl.endsWith(".svg")) return null;

    const imageResponse = await fetchWithTimeout(imageUrl, {
      headers: {
        "user-agent": IMAGE_FETCH_UA,
        accept: "image/avif,image/webp,image/png,image/jpeg,image/*",
      },
      redirect: "follow",
    });
    if (!imageResponse.ok) return null;
    const contentType = imageResponse.headers.get("content-type")?.split(";")[0]?.trim() || "";
    if (!/^image\/(png|jpe?g|webp|avif|gif)$/.test(contentType)) return null;
    const contentLength = Number(imageResponse.headers.get("content-length") || "0");
    if (contentLength > 2500000) return null;
    const bytes = Buffer.from(await imageResponse.arrayBuffer());
    if (bytes.length > 2500000) return null;
    const format = sniffImageFormat(bytes);
    if (!format || !allowedFormats.includes(format)) return null;
    return {
      src: `data:${format};base64,${bytes.toString("base64")}`,
      imageUrl,
      alt: link.label || link.story,
      caption: link.story,
      sourceUrl: link.url,
    };
  } catch {
    return null;
  }
}

async function resolveImages(limit = 3, allowedFormats = ALL_IMAGE_FORMATS) {
  const images = [];
  for (const link of await imageCandidateLinks()) {
    const image = await imageFromPage(link, allowedFormats);
    if (image) images.push(image);
    if (images.length >= limit) break;
  }
  return images;
}

function storyList(items) {
  return items.map((item) => `<p>${escapeHtml(item)}</p>`).join("\n");
}

function smallList(items) {
  return items.map((item) => `<li>${escapeHtml(item)}</li>`).join("\n");
}

function yamlValue(value) {
  return JSON.stringify(String(value ?? ""));
}

function directiveAttr(value) {
  return JSON.stringify(String(value ?? ""));
}

function yamlItems(items, mapper) {
  return items.map(mapper).join("\n");
}

function renderAraSource(images = []) {
  const leadBody = leadDeck.length
    ? leadDeck.map((item) => `${item}`).join("\n\n")
    : "No executive-summary detail was available for this edition.";
  const breakingItems = [...breaking, ...policy].slice(0, 6);
  if (breakingItems.length === 0) {
    breakingItems.push("No breaking or policy items were highlighted in this edition.");
  }
  const storyItems = [
    ["Models & Systems", models, "hot"],
    ["Research Ledger", research, "research"],
    ["Capital & Compute", business, "market"],
  ];
  const source = [
    "---",
    "title: " + yamlValue("THE AGI AWARENESS POST"),
    "kicker: " + yamlValue("Your Daily Artificial Intelligence Briefing"),
    "date: " + yamlValue(monthDay),
    "edition: " + yamlValue("All Sources Edition"),
    "volume: " + yamlValue(date.slice(0, 4)),
    "number: " + yamlValue(issue),
    "deck: " + yamlValue("An interactive newspaper edition generated from the daily AI digest."),
    "---",
    "",
    ":::paper-index",
    "- label: " + yamlValue("Lead") + "\n  target: " + yamlValue("#lead-top-story"),
    "- label: " + yamlValue("Breaking") + "\n  target: " + yamlValue("#briefs-breaking-policy"),
    "- label: " + yamlValue("Signals") + "\n  target: " + yamlValue("#meter-signal-mix"),
    "- label: " + yamlValue("Departments") + "\n  target: " + yamlValue("#deck-departments"),
    ":::",
    "",
    `:::lead(id="lead-top-story", label="Top Story", title=${directiveAttr(lead)})`,
    leadBody,
    ":::",
    "",
    ...(
      images[0]
        ? [
            `:::figure(src=${directiveAttr(images[0].imageUrl)}, alt=${directiveAttr(images[0].alt)}, caption=${directiveAttr(images[0].caption)}, source-url=${directiveAttr(images[0].sourceUrl)}, variant=wide)`,
            ":::",
            "",
          ]
        : []
    ),
    `:::briefs(id="briefs-breaking-policy", title="Breaking & Policy", columns=2)`,
    yamlItems(breakingItems, (item, index) => {
      const tag = index < breaking.length ? "Breaking" : "Policy";
      return "- headline: " + yamlValue(item) + "\n  tag: " + yamlValue(tag);
    }),
    ":::",
    "",
    `:::news-meter(id="meter-signal-mix", title="Signal Mix")`,
    "- label: " + yamlValue("Breaking news") + "\n  value: " + Math.min(100, breaking.length * 25) + "\n  display: " + yamlValue(`${breaking.length} items`) + "\n  tone: hot",
    "- label: " + yamlValue("Model releases") + "\n  value: " + Math.min(100, models.length * 25) + "\n  display: " + yamlValue(`${models.length} items`) + "\n  tone: watch",
    "- label: " + yamlValue("Research highlights") + "\n  value: " + Math.min(100, research.length * 20) + "\n  display: " + yamlValue(`${research.length} items`) + "\n  tone: research",
    "- label: " + yamlValue("Funding and compute") + "\n  value: " + Math.min(100, business.length * 25) + "\n  display: " + yamlValue(`${business.length} items`) + "\n  tone: market",
    ":::",
    "",
    `:::story-deck(id="deck-departments", title="Departments")`,
    yamlItems(storyItems, ([label, items, tone]) => {
      const summary = items.slice(0, 3).join(" ");
      return "- headline: " + yamlValue(label) + "\n  summary: " + yamlValue(summary || "No items reported in this section.") + "\n  meta: " + yamlValue(`${items.length} digest items`) + "\n  tone: " + tone;
    }),
    ":::",
    "",
    `:::quote(label="Quote of the Day")`,
    quote || "No quote of the day was available in the digest.",
    ":::",
    "",
  ];
  return source.join("\n");
}

function wrapText(text, maxChars) {
  const words = text.split(/\s+/).filter(Boolean);
  const lines = [];
  let line = "";
  for (const word of words) {
    const next = line ? `${line} ${word}` : word;
    if (next.length > maxChars && line) {
      lines.push(line);
      line = word;
    } else {
      line = next;
    }
  }
  if (line) lines.push(line);
  return lines;
}

// Truncation must stay visible: a clamp that drops words silently produces
// mid-sentence headlines on the rendered page.
function clampText(text, maxChars, maxLines) {
  const lines = wrapText(text, maxChars);
  if (lines.length <= maxLines) return lines;
  const kept = lines.slice(0, maxLines);
  const last = kept[maxLines - 1].slice(0, Math.max(1, maxChars - 1));
  kept[maxLines - 1] = `${last.replace(/[\s,;:.—–-]+$/, "")}…`;
  return kept;
}

// The digest's lead bullet is a full paragraph; only its first sentence is
// headline-sized. Requiring a following capital/figure and a 30-char minimum
// avoids false splits on decimals ("$19.2B") and short abbreviations.
function splitFirstSentence(text) {
  for (const match of text.matchAll(/[.!?]["”')\]]*\s+(?=["“(]?[A-Z0-9~$€£#@])/g)) {
    const head = text.slice(0, match.index + match[0].length).trimEnd();
    if (head.length < 30) continue;
    if (/\b(?:vs|Mr|Mrs|Ms|Dr|Prof|St|Vol|No|Inc|Corp|Co|Ltd|Jr|Sr|etc)\.$/i.test(head.replace(/["”')\]]+$/, ""))) continue;
    return [head, text.slice(match.index + match[0].length)];
  }
  return [text.trim(), ""];
}

function svgText(x, y, lines, options = {}) {
  const {
    size = 24,
    weight = "400",
    family = "Georgia, Times New Roman, serif",
    lineHeight = Math.round(size * 1.25),
    anchor = "start",
    italic = false,
  } = options;
  const style = `font-family:${family};font-size:${size}px;font-weight:${weight};font-style:${italic ? "italic" : "normal"};fill:#191713`;
  const tspans = lines
    .map((line, index) => `<tspan x="${x}" dy="${index === 0 ? 0 : lineHeight}">${escapeHtml(line)}</tspan>`)
    .join("");
  return `<text y="${y}" text-anchor="${anchor}" style="${style}">${tspans}</text>`;
}

function svgImage(image, x, y, width, height) {
  return [
    `<clipPath id="lead-image-clip"><rect x="${x}" y="${y}" width="${width}" height="${height}" rx="4"/></clipPath>`,
    `<image href="${image.src}" x="${x}" y="${y}" width="${width}" height="${height}" preserveAspectRatio="xMidYMid slice" clip-path="url(#lead-image-clip)"/>`,
    `<rect x="${x}" y="${y}" width="${width}" height="${height}" fill="none" stroke="#2b251d" stroke-width="2"/>`,
  ].join("\n");
}

function renderSvg(images = []) {
  const parts = [];
  parts.push(`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1600" viewBox="0 0 1200 1600">`);
  parts.push(`<rect width="1200" height="1600" fill="#fff8ed"/>`);
  parts.push(`<rect x="32" y="32" width="1136" height="1536" fill="none" stroke="#1f1a14" stroke-width="2"/>`);
  parts.push(`<line x1="62" x2="1138" y1="54" y2="54" stroke="#1f1a14" stroke-width="3"/>`);
  parts.push(`<line x1="62" x2="1138" y1="60" y2="60" stroke="#1f1a14" stroke-width="1"/>`);
  parts.push(svgText(600, 95, ["Your Daily Artificial Intelligence Briefing"], {
    size: 17,
    weight: "700",
    family: "Arial, sans-serif",
    anchor: "middle",
  }));
  parts.push(svgText(600, 170, ["THE AGI AWARENESS POST"], {
    size: 66,
    weight: "700",
    anchor: "middle",
  }));
  parts.push(svgText(62, 218, [`Vol. 2026, No. ${issue}`], { size: 18, weight: "700", family: "Arial, sans-serif" }));
  parts.push(svgText(600, 218, [monthDay], { size: 18, weight: "700", family: "Arial, sans-serif", anchor: "middle" }));
  parts.push(svgText(1138, 218, ["All Sources Edition"], { size: 18, weight: "700", family: "Arial, sans-serif", anchor: "end" }));
  parts.push(`<line x1="62" x2="1138" y1="242" y2="242" stroke="#1f1a14" stroke-width="3"/>`);
  parts.push(`<line x1="62" x2="1138" y1="248" y2="248" stroke="#1f1a14" stroke-width="1"/>`);

  // Lead column geometry: text flows from y=305 and must stop above the
  // image slot (fixed at 690..900) or, with no image, above the 930 rule.
  // Every block fits its remaining vertical budget — content that doesn't
  // fit is ellipsized or dropped, never painted over by a later element.
  const imageTop = 690;
  const leadBottom = images[0] ? imageTop - 18 : 906;
  let y = 305;
  const [headlineText, headlineRest] = splitFirstSentence(lead);
  const headlineSize = headlineText.length > 130 ? 36 : 44;
  const headlineWrap = headlineSize === 36 ? 31 : 25;
  const headlineLineHeight = headlineSize === 36 ? 40 : 48;
  const headlineLines = clampText(headlineText, headlineWrap, 5);
  parts.push(svgText(62, y, headlineLines, { size: headlineSize, weight: "700", lineHeight: headlineLineHeight }));
  y += headlineLines.length * headlineLineHeight + 24;
  for (const item of [headlineRest, ...leadDeck].filter(Boolean)) {
    const linesThatFit = Math.floor((leadBottom - y) / 29) + 1;
    if (linesThatFit < 2) break;
    const lines = clampText(item, 54, Math.min(4, linesThatFit));
    parts.push(svgText(62, y, lines, { size: 22, lineHeight: 29 }));
    y += lines.length * 29 + 14;
  }
  if (images[0]) {
    parts.push(svgImage(images[0], 62, imageTop, 650, 210));
    parts.push(svgText(62, 924, clampText(images[0].alt, 72, 1), {
      size: 13,
      weight: "700",
      family: "Arial, sans-serif",
    }));
  }

  parts.push(`<line x1="760" x2="760" y1="282" y2="900" stroke="#2b251d" stroke-width="2"/>`);
  const sidebarBottom = 906;
  let sideY = 305;
  for (const [label, items] of [["Breaking", breaking], ["Policy Watch", policy]]) {
    // Section label plus at least two lines of its first item must fit,
    // otherwise the whole section is dropped rather than spilling over
    // the 930 rule into the departments grid.
    if (items.length === 0 || sideY + 31 + 22 > sidebarBottom) continue;
    parts.push(`<line x1="790" x2="1138" y1="${sideY - 22}" y2="${sideY - 22}" stroke="#1f1a14" stroke-width="7"/>`);
    parts.push(svgText(790, sideY, [label.toUpperCase()], { size: 16, weight: "800", family: "Arial, sans-serif" }));
    sideY += 31;
    for (const item of items.slice(0, 3)) {
      const linesThatFit = Math.floor((sidebarBottom - sideY) / 22) + 1;
      if (linesThatFit < 2) break;
      const lines = clampText(item, 38, Math.min(4, linesThatFit));
      parts.push(svgText(790, sideY, lines, { size: 17, lineHeight: 22 }));
      sideY += lines.length * 22 + 14;
    }
    sideY += 14;
  }

  parts.push(`<line x1="62" x2="1138" y1="930" y2="930" stroke="#2b251d" stroke-width="2"/>`);
  const columns = [
    ["Models & Systems", models],
    ["Research Ledger", research],
    ["Capital & Compute", business],
  ];
  for (let i = 0; i < columns.length; i += 1) {
    const x = 62 + i * 365;
    if (i > 0) parts.push(`<line x1="${x - 22}" x2="${x - 22}" y1="958" y2="1360" stroke="#7d725f" stroke-width="1"/>`);
    parts.push(svgText(x, 982, [columns[i][0]], { size: 26, weight: "700" }));
    const columnBottom = 1360;
    let columnY = 1022;
    for (const item of columns[i][1].slice(0, i === 1 ? 4 : 3)) {
      const linesThatFit = Math.floor((columnBottom - columnY) / 22) + 1;
      if (linesThatFit < 2) break;
      const lines = clampText(`• ${item}`, 35, Math.min(4, linesThatFit));
      parts.push(svgText(x, columnY, lines, { size: 17, lineHeight: 22 }));
      columnY += lines.length * 22 + 12;
    }
  }

  parts.push(`<rect x="62" y="1390" width="1076" height="106" fill="#fffaf2" stroke="#2b251d" stroke-width="2"/>`);
  parts.push(svgText(84, 1426, clampText(quote || "No quote of the day was available in the digest.", 100, 3), {
    size: 18,
    lineHeight: 25,
    italic: true,
  }));
  parts.push(`<line x1="62" x2="1138" y1="1528" y2="1528" stroke="#2b251d" stroke-width="1"/>`);
  parts.push(svgText(62, 1554, ["Sources: Twitter/X, Hacker News, Reddit, arXiv, RSS, Bluesky"], {
    size: 13,
    weight: "700",
    family: "Arial, sans-serif",
  }));
  parts.push(svgText(1138, 1554, ["Generated by AGI Awareness Post Pipeline"], {
    size: 13,
    weight: "700",
    family: "Arial, sans-serif",
    anchor: "end",
  }));
  parts.push(`</svg>`);
  return parts.join("\n");
}

if (output.endsWith(".png")) {
  const { Resvg } = await import("/tmp/node_modules/@resvg/resvg-js/index.js");
  const images = await resolveImages(1, SVG_SAFE_FORMATS);
  const png = new Resvg(renderSvg(images), {
    fitTo: { mode: "width", value: 2400 },
    font: {
      fontFiles: [],
      loadSystemFonts: true,
      defaultFontFamily: "Georgia",
    },
  }).render().asPng();
  await writeFile(output, png);
  console.log(`Wrote ${output}`);
  process.exit(0);
}

if (output.endsWith(".ara.md")) {
  const images = await resolveImages(3);
  await writeFile(output, renderAraSource(images), "utf8");
  console.log(`Wrote ${output}`);
  process.exit(0);
}

const htmlImages = await resolveImages(1);

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>The AGI Awareness Post - ${escapeHtml(monthDay)}</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: #f2eee4;
    color: #191713;
    font-family: Georgia, "Times New Roman", serif;
  }
  .page {
    width: 1200px;
    height: 1600px;
    overflow: hidden;
    padding: 54px 62px 44px;
    background:
      linear-gradient(rgba(255,255,255,.32), rgba(255,255,255,.08)),
      #fff8ed;
  }
  .topline, .rule { border-top: 3px double #1f1a14; }
  .masthead {
    text-align: center;
    padding: 18px 0 14px;
  }
  .kicker {
    font: 700 17px Arial, sans-serif;
    letter-spacing: 0;
    text-transform: uppercase;
  }
  h1 {
    margin: 6px 0 0;
    font-size: 72px;
    line-height: .9;
    letter-spacing: 0;
  }
  .meta {
    display: flex;
    justify-content: space-between;
    margin-top: 12px;
    font: 700 18px Arial, sans-serif;
  }
  .layout {
    display: grid;
    grid-template-columns: 1.25fr .75fr;
    gap: 30px;
    padding-top: 26px;
  }
  .headline {
    margin: 0 0 14px;
    font-size: 46px;
    line-height: .98;
  }
  .lead p {
    font-size: 22px;
    line-height: 1.36;
    margin: 0 0 15px;
  }
  .lead p:first-of-type::first-letter {
    float: left;
    font-size: 76px;
    line-height: .82;
    padding: 7px 9px 0 0;
  }
  .lead-image {
    float: right;
    width: 310px;
    margin: 2px 0 14px 20px;
    padding: 6px;
    border: 2px solid #2b251d;
    background: #fffaf2;
  }
  .lead-image img {
    display: block;
    width: 100%;
    height: 190px;
    object-fit: cover;
  }
  .lead-image figcaption {
    margin-top: 6px;
    font: 700 12px/1.25 Arial, sans-serif;
  }
  .sidebar {
    border-left: 2px solid #2b251d;
    padding-left: 26px;
  }
  .label {
    font: 800 16px Arial, sans-serif;
    text-transform: uppercase;
    border-top: 8px solid #1f1a14;
    padding-top: 8px;
    margin: 0 0 12px;
  }
  .sidebar p, .column p, li {
    font-size: 17px;
    line-height: 1.32;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    border-top: 2px solid #2b251d;
    margin-top: 28px;
    padding-top: 22px;
  }
  .column + .column {
    border-left: 1px solid #7d725f;
    padding-left: 24px;
  }
  h2 {
    margin: 0 0 10px;
    font-size: 26px;
    line-height: 1.02;
  }
  ul {
    padding-left: 18px;
    margin: 8px 0 0;
  }
  li {
    margin-bottom: 9px;
  }
  .quote {
    margin-top: 22px;
    padding: 15px 18px;
    border: 2px solid #2b251d;
    background: rgba(255,255,255,.36);
    font-size: 18px;
    line-height: 1.35;
    font-style: italic;
  }
  .footer {
    margin-top: 22px;
    padding-top: 10px;
    border-top: 1px solid #2b251d;
    font: 700 13px Arial, sans-serif;
    display: flex;
    justify-content: space-between;
  }
</style>
</head>
<body>
  <main class="page">
    <div class="topline"></div>
    <header class="masthead">
      <div class="kicker">Your Daily Artificial Intelligence Briefing</div>
      <h1>THE AGI AWARENESS POST</h1>
      <div class="meta"><span>Vol. 2026, No. ${issue}</span><span>${escapeHtml(monthDay)}</span><span>All Sources Edition</span></div>
    </header>
    <div class="rule"></div>

    <section class="layout">
      <article class="lead">
        <h2 class="headline">${escapeHtml(lead)}</h2>
        ${htmlImages[0] ? `<figure class="lead-image"><img src="${htmlImages[0].src}" alt="${escapeHtml(htmlImages[0].alt)}"><figcaption>${escapeHtml(htmlImages[0].alt)}</figcaption></figure>` : ""}
        ${storyList(leadDeck)}
      </article>
      <aside class="sidebar">
        <h2 class="label">Breaking</h2>
        ${storyList(breaking)}
        <h2 class="label">Policy Watch</h2>
        ${storyList(policy)}
      </aside>
    </section>

    <section class="grid">
      <article class="column">
        <h2>Models & Systems</h2>
        <ul>${smallList(models)}</ul>
      </article>
      <article class="column">
        <h2>Research Ledger</h2>
        <ul>${smallList(research)}</ul>
      </article>
      <article class="column">
        <h2>Capital & Compute</h2>
        <ul>${smallList(business)}</ul>
      </article>
    </section>

    <section class="quote">${escapeHtml(quote || "No quote of the day was available in the digest.")}</section>
    <footer class="footer">
      <span>Sources: Twitter/X, Hacker News, Reddit, arXiv, RSS, Bluesky</span>
      <span>Generated by AGI Awareness Post Pipeline</span>
    </footer>
  </main>
</body>
</html>
`;

await writeFile(output, html, "utf8");
console.log(`Wrote ${output}`);
