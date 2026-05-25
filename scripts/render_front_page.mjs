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
    .replace(/^[-*]\s+/, "")
    .replace(/^\d+\.\s+/, "")
    .replace(/\s+/g, " ")
    .trim();
}

function section(name) {
  const pattern = new RegExp(`^##\\s+${name}\\s*$([\\s\\S]*?)(?=^##\\s+|\\z)`, "mi");
  return markdown.match(pattern)?.[1]?.trim() ?? "";
}

function bullets(text, limit) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => /^([-*]|\d+\.)\s+/.test(line))
    .map(stripMarkdown)
    .filter(Boolean)
    .slice(0, limit);
}

function paragraphs(text, limit) {
  return text
    .split(/\n{2,}/)
    .map(stripMarkdown)
    .filter(Boolean)
    .slice(0, limit);
}

const executive = bullets(section("Executive Summary"), 5);
const breaking = bullets(section("Breaking News"), 3);
const models = bullets(section("Model Releases & Updates"), 3);
const research = bullets(section("Research Highlights"), 5);
const business = bullets(section("Funding & Business"), 4);
const policy = bullets(section("Policy & Regulation"), 3);
const quoteBlock = markdown.match(/## Quote of the Day\s+>\s*([\s\S]*?)(?=\n---|\n##\s+|$)/i)?.[1] ?? "";
const quote = stripMarkdown(quoteBlock.replace(/^>\s?/gm, " "));

const lead = executive[0] || paragraphs(markdown, 1)[0] || "Today's AI digest is ready.";
const leadDeck = executive.slice(1, 4);
const issue = Math.floor((new Date(`${date}T00:00:00Z`) - new Date(`${date.slice(0, 4)}-01-01T00:00:00Z`)) / 86400000) + 1;

function storyList(items) {
  return items.map((item) => `<p>${escapeHtml(item)}</p>`).join("\n");
}

function smallList(items) {
  return items.map((item) => `<li>${escapeHtml(item)}</li>`).join("\n");
}

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
