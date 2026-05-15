#!/usr/bin/env node
// Copy research data from ../research/ into public/research/ and emit the
// manifest.json the dashboard consumes. Runs as `prebuild` (before
// `vite build`) and `predev` (before `vite dev`), so both Vercel and local
// development hit the same pre-build code path.
//
// Replaces what .github/workflows/deploy-dashboard.yml did inline in CI —
// keeping the logic in-repo means any Vercel build is self-contained and
// the GH Pages workflow can call this same script too if you simplify it
// later.

import { existsSync, readdirSync, mkdirSync, readFileSync, writeFileSync, cpSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const dashboardDir = dirname(here);
const repoRoot = dirname(dashboardDir);
const researchSrc = join(repoRoot, 'research');
const publicResearch = join(dashboardDir, 'public', 'research');

// Subdirs to mirror into public/research/. Keys match how the dashboard
// fetches them; the manifest builder below uses the same set.
const COPY_DIRS = ['twitter', 'models', 'front-page', 'digest', 'audio', 'generative'];

// Regex patterns for the date-keyed sources. The `generative` key is
// special-cased below: it reads research/generative/index.json directly.
const DATE_PATTERNS = {
  twitter:   { dir: 'twitter',    re: /^(\d{4}-\d{2}-\d{2})\.md$/ },
  models:    { dir: 'models',     re: /^(\d{4}-\d{2}-\d{2})-timeline\.md$/ },
  frontpage: { dir: 'front-page', re: /^(\d{4}-\d{2}-\d{2})-front-page\.png$/ },
  today:     { dir: 'digest',     re: /^(\d{4}-\d{2}-\d{2})-digest\.md$/ },
  audio:     { dir: 'audio',      re: /^(\d{4}-\d{2}-\d{2})-digest\.mp3$/ },
};

function copyData() {
  mkdirSync(publicResearch, { recursive: true });
  for (const sub of COPY_DIRS) {
    const src = join(researchSrc, sub);
    if (!existsSync(src)) continue;
    const dest = join(publicResearch, sub);
    cpSync(src, dest, { recursive: true });
  }
}

function collectDates(dir, re) {
  if (!existsSync(dir)) return [];
  const dates = new Set();
  for (const name of readdirSync(dir)) {
    const m = re.exec(name);
    if (m) dates.add(m[1]);
  }
  return Array.from(dates).sort();
}

function buildManifest() {
  const manifest = {};
  for (const [key, { dir, re }] of Object.entries(DATE_PATTERNS)) {
    manifest[key] = collectDates(join(publicResearch, dir), re);
  }
  const genIndex = join(publicResearch, 'generative', 'index.json');
  if (existsSync(genIndex)) {
    manifest.generative = JSON.parse(readFileSync(genIndex, 'utf8'));
  } else {
    manifest.generative = [];
  }
  writeFileSync(
    join(publicResearch, 'manifest.json'),
    JSON.stringify(manifest),
  );
  const counts = Object.fromEntries(
    Object.entries(manifest).map(([k, v]) => [k, Array.isArray(v) ? v.length : 0]),
  );
  console.log('prebuild: manifest.json', counts);
}

copyData();
buildManifest();
