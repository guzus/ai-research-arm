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

import { existsSync, readdirSync, mkdirSync, readFileSync, writeFileSync, cpSync, statSync, openSync, readSync, closeSync } from 'node:fs';
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

// Binary file extensions that are routed through git-lfs (see .gitattributes
// at repo root). Anything else can be skipped — pointer-file detection is
// only meaningful for files that COULD be LFS-routed.
const LFS_EXT_RE = /\.(png|jpg|jpeg|gif|webp|mp3|wav|ogg|mp4|webm|pdf)$/i;

// LFS pointer files are tiny (~135 bytes) and start with this prefix. If the
// build runs on a checkout that didn't hydrate LFS objects, cpSync happily
// copies the pointer text and the deployed dashboard serves it as if it were
// the real binary — silent breakage. We'd rather fail the build loudly.
function isLfsPointer(filePath) {
  let stats;
  try {
    stats = statSync(filePath);
  } catch {
    return false;
  }
  // Real binaries are always larger than the largest plausible pointer file.
  // LFS pointer spec is 3 lines, well under 1KB; cap at 1024 to be safe.
  if (!stats.isFile() || stats.size > 1024) return false;
  const fd = openSync(filePath, 'r');
  const buf = Buffer.alloc(64);
  try {
    readSync(fd, buf, 0, 64, 0);
  } finally {
    closeSync(fd);
  }
  return buf.toString('utf8').startsWith('version https://git-lfs.github.com/spec/v1');
}

function findLfsPointers(dir) {
  const pointers = [];
  if (!existsSync(dir)) return pointers;
  for (const name of readdirSync(dir)) {
    if (!LFS_EXT_RE.test(name)) continue;
    const full = join(dir, name);
    if (isLfsPointer(full)) pointers.push(full);
  }
  return pointers;
}

function copyData() {
  mkdirSync(publicResearch, { recursive: true });

  // Pre-flight: scan for LFS pointer files in the source tree. If any are
  // found, the build environment didn't hydrate LFS objects — usually
  // because Vercel's "Git LFS" toggle is OFF in project settings, or a
  // GitHub Actions checkout is missing `lfs: true`. Fail loudly here instead
  // of silently shipping pointer text to production.
  const allPointers = [];
  for (const sub of COPY_DIRS) {
    allPointers.push(...findLfsPointers(join(researchSrc, sub)));
  }
  if (allPointers.length > 0) {
    console.error(
      `prebuild: ERROR — found ${allPointers.length} git-lfs pointer file(s) ` +
      'in the source tree. The build environment did not hydrate LFS objects. ' +
      'On Vercel: enable "Git LFS" in Project Settings > Git, then redeploy. ' +
      'On GitHub Actions: add `lfs: true` to actions/checkout. ' +
      'On local dev: run `git lfs install && git lfs pull`.\n' +
      'Sample pointer files:\n' +
      allPointers.slice(0, 5).map((p) => `  - ${p}`).join('\n'),
    );
    process.exit(1);
  }

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
