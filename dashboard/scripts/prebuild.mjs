#!/usr/bin/env node
// Copy research data from ../research/ into public/research/ and emit the
// manifest.json the dashboard consumes. Runs as `prebuild` (before
// `vite build`) and `predev` (before `vite dev`), so the Railway Docker
// build and local development hit the same pre-build code path.
//
// Keeping this logic in-repo (rather than inline in a deploy workflow) means
// any build environment — the production Railway image, a local checkout, or
// a fork's own host — is self-contained and reproducible.

import { spawnSync } from 'node:child_process';
import { existsSync, readdirSync, mkdirSync, readFileSync, writeFileSync, cpSync, statSync, openSync, readSync, closeSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import * as yaml from 'js-yaml';

const here = dirname(fileURLToPath(import.meta.url));
const dashboardDir = dirname(here);
const repoRoot = dirname(dashboardDir);
const researchSrc = join(repoRoot, 'research');
const publicResearch = join(dashboardDir, 'public', 'research');
const ticketsSrc = join(researchSrc, 'models', 'tickets');
const ticketsDest = join(publicResearch, 'models', 'tickets');
const skipLfsPointers = process.env.SKIP_LFS_POINTERS === '1';

// Subdirs to mirror into public/research/. Keys match how the dashboard
// fetches them; the manifest builder below uses the same set.
// `wiki` carries research/wiki/ (committed index.json + entities/concepts/themes
// markdown). The index is built in Python (scripts/build_wiki_index.py) and
// committed — we only copy it here; we never rebuild it in JS.
const COPY_DIRS = ['twitter', 'models', 'front-page', 'digest', 'audio', 'generative', 'wiki', 'youtube', 'arm'];

// Regex patterns for the date-keyed sources. The `generative` key is
// special-cased below: it reads research/generative/index.json directly.
const DATE_PATTERNS = {
  twitter:   { dir: 'twitter',    re: /^(\d{4}-\d{2}-\d{2})\.md$/ },
  models:    { dir: 'models',     re: /^(\d{4}-\d{2}-\d{2})-timeline\.md$/ },
  frontpage: { dir: 'front-page', re: /^(\d{4}-\d{2}-\d{2})-front-page\.png$/ },
  today:     { dir: 'digest',     re: /^(\d{4}-\d{2}-\d{2})-digest\.md$/ },
  audio:     { dir: 'audio',      re: /^(\d{4}-\d{2}-\d{2})-digest\.mp3$/ },
  youtube:   { dir: 'youtube',    re: /^(\d{4}-\d{2}-\d{2})\.md$/ },
};

const ARM_WINDOW_PAST_HOURS = 36;
const ARM_WINDOW_FUTURE_HOURS = 36;
const ARM_MINUTE_MS = 60 * 1000;
const ARM_HOUR_MS = 60 * ARM_MINUTE_MS;
const armSourcePath = join(researchSrc, 'arm', 'timeline.json');
const armPublicPath = join(publicResearch, 'arm', 'timeline.json');

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

function findAllLfsPointers() {
  const pointers = [];
  for (const sub of COPY_DIRS) {
    pointers.push(...findLfsPointers(join(researchSrc, sub)));
  }
  return pointers;
}

function tryHydrateLfsObjects() {
  const result = spawnSync('git', ['lfs', 'pull'], {
    cwd: repoRoot,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  if (result.status === 0) {
    console.warn('prebuild: hydrated git-lfs objects with `git lfs pull`; continuing build.');
    return true;
  }
  const stderr = (result.stderr || result.stdout || '').trim();
  console.warn(
    'prebuild: attempted `git lfs pull` after finding pointer files, but it failed' +
    (stderr ? `:\n${stderr}` : '.'),
  );
  return false;
}

function copyResearchDir(src, dest) {
  cpSync(src, dest, {
    recursive: true,
    filter: (source) => {
      if (!skipLfsPointers || !LFS_EXT_RE.test(source)) return true;
      return !isLfsPointer(source);
    },
  });
}

function copyData() {
  mkdirSync(publicResearch, { recursive: true });

  // Pre-flight: scan for LFS pointer files in the source tree. If any are
  // found, the build environment didn't hydrate LFS objects — usually
  // because Vercel's "Git LFS" toggle is OFF in project settings, or a
  // GitHub Actions checkout is missing `lfs: true`. Fail loudly here instead
  // of silently shipping pointer text to production.
  let allPointers = findAllLfsPointers();
  if (allPointers.length > 0 && !skipLfsPointers && tryHydrateLfsObjects()) {
    allPointers = findAllLfsPointers();
  }
  if (allPointers.length > 0 && skipLfsPointers) {
    console.warn(
      `prebuild: WARNING — skipping ${allPointers.length} git-lfs pointer file(s) ` +
      'because SKIP_LFS_POINTERS=1. Media assets backed by those pointers ' +
      'will be absent from this build, but dashboard code/type/build checks can continue.\n' +
      'Sample skipped pointer files:\n' +
      allPointers.slice(0, 5).map((p) => `  - ${p}`).join('\n'),
    );
  } else if (allPointers.length > 0) {
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
    copyResearchDir(src, dest);
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

// Lenient shape-check for the optional `polymarket:` frontmatter (see
// docs/model-tickets.md). scripts/check_model_tickets.py is the strict
// gate; here a malformed mapping is dropped with a warning so one bad
// autonomous-agent write can never fail the deploy. Returns a clean
// array of mappings, or null when nothing usable remains.
function sanitizeTicketPolymarket(raw, ticketName) {
  if (raw == null) return null;
  if (!Array.isArray(raw)) {
    console.warn(`prebuild: WARNING — tickets/${ticketName}: polymarket is not a list; dropping it`);
    return null;
  }
  const clean = [];
  for (const entry of raw) {
    if (!entry || typeof entry !== 'object' || Array.isArray(entry)) {
      console.warn(`prebuild: WARNING — tickets/${ticketName}: polymarket mapping is not an object; dropping mapping`);
      continue;
    }
    const str = (v) => (typeof v === 'string' && v.trim() ? v.trim() : null);
    const event_slug = str(entry.event_slug);
    const question = str(entry.question);
    // market_id is small enough to coerce from an accidental YAML number;
    // token_id is ~78 digits and unrecoverable once parsed as a number.
    const market_id = str(entry.market_id) ??
      (typeof entry.market_id === 'number' && Number.isSafeInteger(entry.market_id)
        ? String(entry.market_id)
        : null);
    const token_id = str(entry.token_id);
    if (!event_slug || !market_id || !token_id || !question) {
      console.warn(`prebuild: WARNING — tickets/${ticketName}: polymarket mapping missing/invalid required field; dropping mapping`);
      continue;
    }
    const mapping = { event_slug, market_id, token_id, question };
    const outcome = str(entry.outcome);
    if (outcome) mapping.outcome = outcome;
    clean.push(mapping);
  }
  if (clean.length > 3) {
    console.warn(`prebuild: WARNING — tickets/${ticketName}: polymarket has ${clean.length} mappings; keeping the first 3`);
    clean.length = 3;
  }
  return clean.length ? clean : null;
}

function buildTicketsIndex() {
  // Parse every research/models/tickets/<slug>.md, split frontmatter
  // and body, and emit a single tickets/index.json that the dashboard
  // fetches in one shot to render the cards. The index is consumed by
  // the `models` tab. If the tickets dir is empty (pre-migration), we
  // skip — the dashboard handles a missing index gracefully.
  if (!existsSync(ticketsSrc)) return;
  const files = readdirSync(ticketsSrc).filter((n) => n.endsWith('.md')).sort();
  if (files.length === 0) return;

  // A single malformed ticket among ~55 must NOT fail the whole deploy: skip
  // the bad file and warn, then ship the rest of the timeline. scripts/
  // check_model_tickets.py (run in CI) is the hard schema gate; this copy step
  // is best-effort so one corrupt autonomous-agent write can't stale the site.
  const tickets = [];
  let skipped = 0;
  for (const name of files) {
    const path = join(ticketsSrc, name);
    const text = readFileSync(path, 'utf8');
    if (!text.startsWith('---\n')) {
      console.warn(`prebuild: WARNING — tickets/${name}: missing leading '---'; skipping ticket`);
      skipped++;
      continue;
    }
    const end = text.indexOf('\n---\n', 4);
    if (end < 0) {
      console.warn(`prebuild: WARNING — tickets/${name}: missing closing '---'; skipping ticket`);
      skipped++;
      continue;
    }
    const header = text.slice(4, end);
    const body = text.slice(end + 5).replace(/^\n+/, '');
    let fm;
    try {
      fm = yaml.load(header);
    } catch (e) {
      console.warn(`prebuild: WARNING — tickets/${name}: YAML parse error: ${e.message}; skipping ticket`);
      skipped++;
      continue;
    }
    if (!fm || typeof fm !== 'object') {
      console.warn(`prebuild: WARNING — tickets/${name}: frontmatter is not a mapping; skipping ticket`);
      skipped++;
      continue;
    }
    // Normalize date fields to ISO strings so JSON round-trips cleanly.
    const isoDate = (v) => (v instanceof Date ? v.toISOString().slice(0, 10) : v);
    fm.created_at = isoDate(fm.created_at);
    fm.updated_at = isoDate(fm.updated_at);
    fm.closed_at = isoDate(fm.closed_at);
    if (Array.isArray(fm.history)) {
      fm.history = fm.history.map((h) => ({ ...h, ts: isoDate(h.ts) }));
    }
    // Optional Polymarket odds mappings — pass through only well-shaped
    // entries so the dashboard never sees a malformed mapping.
    const polymarket = sanitizeTicketPolymarket(fm.polymarket, name);
    if (polymarket) fm.polymarket = polymarket;
    else delete fm.polymarket;
    tickets.push({ ...fm, body });
  }

  mkdirSync(ticketsDest, { recursive: true });
  const indexPath = join(ticketsDest, 'index.json');
  writeFileSync(indexPath, JSON.stringify({ tickets }));
  const byStatus = tickets.reduce((acc, t) => {
    acc[t.status] = (acc[t.status] || 0) + 1;
    return acc;
  }, {});
  console.log(
    `prebuild: tickets/index.json (${tickets.length} tickets` +
    (skipped > 0 ? `, ${skipped} skipped as malformed` : '') + ')',
    byStatus,
  );
}

function isoMinute(date) {
  return new Date(Math.floor(date.getTime() / ARM_MINUTE_MS) * ARM_MINUTE_MS).toISOString();
}

function isoMinuteCeil(date) {
  return new Date(Math.ceil(date.getTime() / ARM_MINUTE_MS) * ARM_MINUTE_MS).toISOString();
}

function parseSubjectUtc(subject) {
  const m = subject.match(/(\d{4}-\d{2}-\d{2})\s+(\d{2}):(\d{2})\s+UTC/);
  if (!m) return null;
  const ms = Date.parse(`${m[1]}T${m[2]}:${m[3]}:00Z`);
  return Number.isFinite(ms) ? new Date(ms) : null;
}

function subjectDetails(subject) {
  if (/^RSS\b/i.test(subject)) return { lane: 'RSS', title: 'RSS official announcements', model: 'scheduled agent' };
  if (/^Twitter \(DeepSeek\)/i.test(subject)) return { lane: 'Twitter/X', title: 'Twitter/X DeepSeek brief', model: 'deepseek-v4-flash' };
  if (/^Twitter \(pi\+Fireworks\)/i.test(subject)) return { lane: 'Twitter/X', title: 'Twitter/X Fireworks pi brief', model: 'kimi-k2p7' };
  if (/^Twitter\b/i.test(subject)) return { lane: 'Twitter/X', title: 'Twitter/X brief', model: 'deepseek-v4-flash' };
  if (/^Track delivered Twitter/i.test(subject)) return { lane: 'Delivery', title: 'Twitter alert delivery', model: 'hooker' };
  if (/^Community/i.test(subject)) return { lane: 'Community', title: 'HN + Reddit digest', model: 'scheduled agent' };
  if (/^AI expert blog/i.test(subject)) return { lane: 'Blogs', title: 'AI expert blog watch', model: 'scheduled agent' };
  if (/^Bluesky/i.test(subject)) return { lane: 'Bluesky', title: 'Bluesky commentary', model: 'scheduled agent' };
  if (/^YouTube/i.test(subject)) return { lane: 'YouTube', title: 'YouTube signal', model: 'scheduled agent' };
  if (/^Model tickets/i.test(subject)) return { lane: 'Models', title: 'Model release tickets', model: 'scheduled agent' };
  if (/^arXiv/i.test(subject)) return { lane: 'arXiv', title: 'arXiv papers', model: 'scheduled agent' };
  if (/^Wiki ingest/i.test(subject)) return { lane: 'Wiki', title: 'LLM wiki ingest', model: 'scheduled agent' };
  if (/^Generative research:/i.test(subject)) return { lane: 'Generative', title: subject.replace(/^Generative research:\s*/i, '').slice(0, 96), model: 'research agent' };
  if (/Arm|Agents|dashboard|frontend|visualization|tab/i.test(subject)) return { lane: 'Dashboard', title: subject.slice(0, 96), model: 'codex' };
  return null;
}

function collectCompletedArmItems(now) {
  const result = spawnSync('git', [
    'log',
    '--max-count=140',
    '--pretty=format:%H%x09%cI%x09%an%x09%s',
    '--',
    '.',
  ], {
    cwd: repoRoot,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  if (result.status !== 0 || !result.stdout.trim()) return null;
  const cutoff = now.getTime() - (ARM_WINDOW_PAST_HOURS * ARM_HOUR_MS);
  const items = [];
  for (const line of result.stdout.split('\n')) {
    const [sha, committedAt, author, ...subjectParts] = line.split('\t');
    const subject = subjectParts.join('\t').trim();
    const end = new Date(committedAt);
    if (!sha || !subject || Number.isNaN(end.getTime()) || end.getTime() < cutoff) continue;
    const details = subjectDetails(subject);
    if (!details) continue;
    const parsedStart = parseSubjectUtc(subject);
    const fallbackMinutes = details.lane === 'Generative' ? 50 : details.lane === 'Dashboard' ? 20 : 8;
    let start = parsedStart || new Date(end.getTime() - (fallbackMinutes * ARM_MINUTE_MS));
    if (start.getTime() > end.getTime()) start = new Date(end.getTime() - (fallbackMinutes * ARM_MINUTE_MS));
    if (end.getTime() - start.getTime() > 6 * ARM_HOUR_MS) start = new Date(end.getTime() - (fallbackMinutes * ARM_MINUTE_MS));
    items.push({
      id: `commit-${sha.slice(0, 12)}`,
      kind: 'completed',
      lane: details.lane,
      title: details.title,
      status: 'completed',
      start: isoMinute(start),
      end: isoMinuteCeil(end),
      source: author || 'git commit',
      model: details.model,
      commit: sha.slice(0, 12),
      url: `https://github.com/guzus/ai-research-arm/commit/${sha}`,
    });
  }
  return items;
}

function parseCronField(field, min, max) {
  const values = new Set();
  for (const part of String(field).split(',')) {
    const trimmed = part.trim();
    if (trimmed === '*') {
      for (let i = min; i <= max; i += 1) values.add(i);
      continue;
    }
    const step = trimmed.match(/^\*\/(\d+)$/);
    if (step) {
      const n = Number(step[1]);
      for (let i = min; i <= max; i += n) values.add(i);
      continue;
    }
    const rangeStep = trimmed.match(/^(\d+)-(\d+)\/(\d+)$/);
    if (rangeStep) {
      const start = Number(rangeStep[1]);
      const end = Number(rangeStep[2]);
      const n = Number(rangeStep[3]);
      for (let i = start; i <= end; i += n) if (i >= min && i <= max) values.add(i);
      continue;
    }
    const range = trimmed.match(/^(\d+)-(\d+)$/);
    if (range) {
      for (let i = Number(range[1]); i <= Number(range[2]); i += 1) if (i >= min && i <= max) values.add(i);
      continue;
    }
    const value = Number(trimmed);
    if (Number.isInteger(value) && value >= min && value <= max) values.add(value);
  }
  return values;
}

function cronMatches(cron, date) {
  const parts = cron.trim().split(/\s+/);
  if (parts.length !== 5) return false;
  const [minute, hour, dayOfMonth, month, dayOfWeek] = parts;
  const tests = [
    [parseCronField(minute, 0, 59), date.getUTCMinutes()],
    [parseCronField(hour, 0, 23), date.getUTCHours()],
    [parseCronField(dayOfMonth, 1, 31), date.getUTCDate()],
    [parseCronField(month, 1, 12), date.getUTCMonth() + 1],
    [parseCronField(dayOfWeek, 0, 7), date.getUTCDay()],
  ];
  return tests.every(([set, value], index) => {
    if (index === 4 && set.has(7) && value === 0) return true;
    return set.has(value);
  });
}

function scheduledDurationMinutes(name, file) {
  const key = `${name} ${file}`.toLowerCase();
  if (key.includes('twitter')) return 60;
  if (key.includes('digest')) return 60;
  if (key.includes('community')) return 30;
  if (key.includes('rss')) return 15;
  if (key.includes('model')) return 45;
  if (key.includes('blog')) return 30;
  if (key.includes('arxiv')) return 30;
  if (key.includes('youtube')) return 25;
  if (key.includes('bluesky')) return 25;
  if (key.includes('wiki')) return 30;
  if (key.includes('liveness')) return 20;
  return 30;
}

function scheduledLane(name, file) {
  const key = `${name} ${file}`.toLowerCase();
  if (key.includes('twitter')) return 'Twitter/X';
  if (key.includes('rss')) return 'RSS';
  if (key.includes('community')) return 'Community';
  if (key.includes('blog')) return 'Blogs';
  if (key.includes('arxiv')) return 'arXiv';
  if (key.includes('youtube')) return 'YouTube';
  if (key.includes('bluesky')) return 'Bluesky';
  if (key.includes('model')) return 'Models';
  if (key.includes('wiki')) return 'Wiki';
  if (key.includes('digest')) return 'Digest';
  return 'Scheduled';
}

function collectScheduledArmItems(now) {
  const workflowsDir = join(repoRoot, '.github', 'workflows');
  if (!existsSync(workflowsDir)) return [];
  const windowEnd = now.getTime() + (ARM_WINDOW_FUTURE_HOURS * ARM_HOUR_MS);
  const files = readdirSync(workflowsDir).filter((name) => name.endsWith('.yml') || name.endsWith('.yaml')).sort();
  const items = [];
  for (const file of files) {
    const text = readFileSync(join(workflowsDir, file), 'utf8');
    const name = (text.match(/^name:\s*(.+)$/m)?.[1] || file).trim().replace(/^['"]|['"]$/g, '');
    const crons = Array.from(text.matchAll(/cron:\s*['"]([^'"]+)['"]/g)).map((m) => m[1]);
    if (crons.length === 0) continue;
    const duration = scheduledDurationMinutes(name, file);
    const lane = scheduledLane(name, file);
    for (const cron of crons) {
      const cursor = new Date(Math.ceil(now.getTime() / ARM_MINUTE_MS) * ARM_MINUTE_MS);
      for (let guard = 0; cursor.getTime() <= windowEnd && guard < ARM_WINDOW_FUTURE_HOURS * 60; guard += 1) {
        if (cronMatches(cron, cursor)) {
          const start = new Date(cursor);
          const end = new Date(start.getTime() + duration * ARM_MINUTE_MS);
          items.push({
            id: `scheduled-${file}-${cron}-${start.toISOString()}`.replace(/[^a-zA-Z0-9_-]/g, '-'),
            kind: 'scheduled',
            lane,
            title: name,
            status: 'scheduled',
            start: isoMinute(start),
            end: isoMinuteCeil(end),
            source: `cron ${cron}`,
          });
        }
        cursor.setUTCMinutes(cursor.getUTCMinutes() + 1);
      }
    }
  }
  return items;
}

function readFallbackArmTimeline() {
  for (const path of [armPublicPath, armSourcePath]) {
    if (!existsSync(path)) continue;
    try {
      const data = JSON.parse(readFileSync(path, 'utf8'));
      if (Array.isArray(data.items)) return data;
    } catch (e) {
      console.warn(`prebuild: WARNING — failed to read arm timeline fallback ${path}: ${e.message}`);
    }
  }
  return null;
}

function buildArmTimeline() {
  const now = new Date();
  const windowStart = new Date(Math.floor((now.getTime() - ARM_WINDOW_PAST_HOURS * ARM_HOUR_MS) / ARM_HOUR_MS) * ARM_HOUR_MS);
  const windowEnd = new Date(Math.ceil((now.getTime() + ARM_WINDOW_FUTURE_HOURS * ARM_HOUR_MS) / ARM_HOUR_MS) * ARM_HOUR_MS);
  const fallback = readFallbackArmTimeline();
  const fallbackItems = Array.isArray(fallback?.items) ? fallback.items : [];
  const completedFromGit = collectCompletedArmItems(now);
  const scheduledFromWorkflows = collectScheduledArmItems(now);
  const completed = completedFromGit || fallbackItems.filter((item) => item.kind === 'completed');
  const scheduled = scheduledFromWorkflows.length > 0
    ? scheduledFromWorkflows
    : fallbackItems.filter((item) => item.kind === 'scheduled');
  const items = [...completed, ...scheduled]
    .filter((item) => Date.parse(item.end) >= windowStart.getTime() && Date.parse(item.start) <= windowEnd.getTime())
    .sort((a, b) => String(a.start).localeCompare(String(b.start)) || String(a.title).localeCompare(String(b.title)));
  const timeline = {
    generatedAt: now.toISOString(),
    windowStart: windowStart.toISOString(),
    windowEnd: windowEnd.toISOString(),
    timezone: 'UTC',
    items,
  };
  mkdirSync(dirname(armPublicPath), { recursive: true });
  writeFileSync(armPublicPath, JSON.stringify(timeline, null, 2));
  if (process.env.ARM_TIMELINE_WRITE_SOURCE === '1') {
    mkdirSync(dirname(armSourcePath), { recursive: true });
    writeFileSync(armSourcePath, JSON.stringify(timeline, null, 2));
  }
  const byKind = items.reduce((acc, item) => {
    acc[item.kind] = (acc[item.kind] || 0) + 1;
    return acc;
  }, {});
  console.log(`prebuild: arm/timeline.json (${items.length} items)`, byKind);
}

function buildManifest() {
  const manifest = {
    // Deploy-health stamp (scripts/check_deploy_health.py reads these from the
    // LIVE site). `generatedAt` is the build wall-clock: on a healthy system a
    // push to main rebuilds within minutes, so the live value should never lag
    // far behind the latest commit. `gitSha` is best-effort diagnostic only —
    // the Docker build context has no .git, so never shell out to git here;
    // Railway/Vercel expose the sha via env when configured, else null.
    // Additive only: main.ts's loadManifest() normalizes by picking known
    // keys, so existing consumers ignore these fields.
    generatedAt: new Date().toISOString(),
    gitSha: process.env.RAILWAY_GIT_COMMIT_SHA || process.env.VERCEL_GIT_COMMIT_SHA || null,
  };
  for (const [key, { dir, re }] of Object.entries(DATE_PATTERNS)) {
    manifest[key] = collectDates(join(publicResearch, dir), re);
  }
  const genIndex = join(publicResearch, 'generative', 'index.json');
  if (existsSync(genIndex)) {
    // A half-written/malformed generative index (the publish + audio-backfill
    // agents write this file) must NOT crash the whole deploy — degrade to an
    // empty generative list and warn, so the rest of the site still ships.
    // check_generative_research.py / write_generative_research.py remain the
    // hard gate; this is only the deploy-time copy step.
    try {
      manifest.generative = JSON.parse(readFileSync(genIndex, 'utf8'));
    } catch (e) {
      console.warn(
        `prebuild: WARNING — generative/index.json failed to parse (${e.message}); ` +
        'shipping with an empty generative list for this build.',
      );
      manifest.generative = [];
    }
  } else {
    manifest.generative = [];
  }
  writeFileSync(
    join(publicResearch, 'manifest.json'),
    JSON.stringify(manifest),
  );
  const counts = Object.fromEntries(
    Object.entries(manifest)
      .filter(([, v]) => Array.isArray(v))
      .map(([k, v]) => [k, v.length]),
  );
  console.log(
    `prebuild: manifest.json (generatedAt=${manifest.generatedAt} gitSha=${manifest.gitSha ?? 'null'})`,
    counts,
  );
}

// ── Tweet card hydration ───────────────────────────────────
// Fetch real tweet data (author/text/avatar/likes/time) for the status URLs
// referenced in the Twitter view, so the dashboard renders native tweet cards
// instead of bare links or third-party iframes. X's public syndication
// endpoint returns clean JSON server-side (no auth; CORS blocks the browser,
// hence build-time). Disk-cached under data/source-cache/tweets/ (gitignored)
// so repeat builds don't refetch; capped + concurrency-limited + fully
// graceful so a slow/blocked/rate-limited X never fails or stalls the build.
const tweetCacheDir = join(repoRoot, 'data', 'source-cache', 'tweets');
const TWEET_FETCH_CAP = 200;     // max NEW network fetches per build
const TWEET_CONCURRENCY = 8;
const TWEET_TIMEOUT_MS = 4000;
const TWEET_RECENT_FILES = 21;   // only scan the most recent N twitter days

function syndicationToken(id) {
  return ((Number(id) / 1e15) * Math.PI).toString(36).replace(/(0+|\.)/g, '');
}

function collectTweetIds() {
  const dir = join(researchSrc, 'twitter');
  if (!existsSync(dir)) return [];
  const files = readdirSync(dir)
    .filter((n) => /^\d{4}-\d{2}-\d{2}\.md$/.test(n))
    .sort()
    .reverse()
    .slice(0, TWEET_RECENT_FILES);
  const ids = new Set();
  for (const name of files) {
    const text = readFileSync(join(dir, name), 'utf8');
    for (const m of text.matchAll(/(?:x|twitter)\.com\/\w+\/status\/(\d+)/g)) ids.add(m[1]);
  }
  return Array.from(ids);
}

async function fetchTweetCard(id) {
  const token = syndicationToken(id);
  const url = `https://cdn.syndication.twimg.com/tweet-result?id=${id}&token=${token}&lang=en`;
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TWEET_TIMEOUT_MS);
  try {
    const r = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' }, signal: ctrl.signal });
    if (!r.ok) return null;
    const d = await r.json();
    if (!d || !d.user) return null;
    let text = String(d.text || '');
    const range = Array.isArray(d.display_text_range) ? d.display_text_range : null;
    if (range && range.length === 2 && range[1] <= text.length) text = text.slice(range[0], range[1]);
    text = text.replace(/\s*https:\/\/t\.co\/\S+\s*$/, '').trim();
    return {
      name: String(d.user.name || ''),
      handle: String(d.user.screen_name || ''),
      avatar: String(d.user.profile_image_url_https || ''),
      verified: !!(d.user.verified || d.user.is_blue_verified),
      text,
      date: String(d.created_at || ''),
      likes: Number(d.favorite_count || 0),
      replies: Number(d.conversation_count || 0),
      url: `https://x.com/${d.user.screen_name}/status/${id}`,
    };
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

async function hydrateTweets() {
  const outPath = join(publicResearch, 'tweets.json');
  const ids = collectTweetIds();
  if (ids.length === 0) {
    writeFileSync(outPath, '{}');
    return;
  }
  mkdirSync(tweetCacheDir, { recursive: true });
  const out = {};
  const toFetch = [];
  for (const id of ids) {
    const cachePath = join(tweetCacheDir, `${id}.json`);
    if (existsSync(cachePath)) {
      try { out[id] = JSON.parse(readFileSync(cachePath, 'utf8')); continue; } catch { /* fall through to refetch */ }
    }
    toFetch.push(id);
  }
  const fetchList = toFetch.slice(0, TWEET_FETCH_CAP);
  let ok = 0;
  let fail = 0;
  for (let i = 0; i < fetchList.length; i += TWEET_CONCURRENCY) {
    const batch = fetchList.slice(i, i + TWEET_CONCURRENCY);
    const results = await Promise.all(batch.map(async (id) => [id, await fetchTweetCard(id)]));
    for (const [id, card] of results) {
      if (card) {
        out[id] = card;
        ok++;
        try { writeFileSync(join(tweetCacheDir, `${id}.json`), JSON.stringify(card)); } catch { /* cache best-effort */ }
      } else {
        fail++;
      }
    }
  }
  writeFileSync(outPath, JSON.stringify(out));
  const over = toFetch.length - fetchList.length;
  console.log(
    `prebuild: tweets.json (${Object.keys(out).length} cards; ${ok} fetched, ${fail} failed` +
    (over > 0 ? `, ${over} over cap` : '') + ')',
  );
}

// ── Search index (digest sections + twitter cycles) ─────────
// A small, bounded JSON the SPA loads once so digest sections and twitter
// cycles become searchable jump targets in the global command palette. Bounded
// to recent dates (older sections/cycles aren't worth searching) and fully
// best-effort so a malformed file never fails the build.
const DIGEST_RECENT_FILES = 14;

function buildSearchIndex() {
  const out = { digestSections: [], twitter: [] };
  // Digest sections: split each recent digest on `## ` headings (mirrors
  // splitSections() in main.ts). Skip "Executive Summary" — it renders as the
  // tldr card with no .content-card-title to scroll to.
  try {
    const dir = join(researchSrc, 'digest');
    if (existsSync(dir)) {
      const re = /^(\d{4}-\d{2}-\d{2})-digest\.md$/;
      const dates = readdirSync(dir)
        .map((n) => (re.exec(n) || [])[1])
        .filter(Boolean)
        .sort()
        .reverse()
        .slice(0, DIGEST_RECENT_FILES);
      const SKIP = new Set(['Executive Summary']);
      for (const date of dates) {
        const md = readFileSync(join(dir, `${date}-digest.md`), 'utf8');
        let title = null;
        let buf = [];
        const flush = () => {
          if (title && !SKIP.has(title)) {
            const snippet = buf
              .join(' ')
              .replace(/[#>*_`~|\[\]()]/g, ' ')
              .replace(/https?:\/\/\S+/g, ' ')
              .replace(/\s+/g, ' ')
              .trim()
              .slice(0, 140);
            out.digestSections.push({ date, sectionTitle: title, snippet });
          }
        };
        for (const line of md.split('\n')) {
          const mm = line.match(/^## (.+)/);
          if (mm) {
            flush();
            title = mm[1].trim();
            buf = [];
          } else if (title) {
            buf.push(line);
          }
        }
        flush();
      }
    }
  } catch (e) {
    console.warn('prebuild: digest search index skipped:', e?.message || e);
  }
  // Twitter cycles: split each recent twitter file on `## HH:MM UTC` cycle
  // headings; index the Cycle summary (Signal Brief) + story titles. The anchor
  // MUST match the id assigned in renderTwitterReport (cycle-HHMMutc).
  try {
    const dir = join(researchSrc, 'twitter');
    if (existsSync(dir)) {
      const files = readdirSync(dir)
        .filter((n) => /^\d{4}-\d{2}-\d{2}\.md$/.test(n))
        .sort()
        .reverse()
        .slice(0, TWEET_RECENT_FILES);
      for (const name of files) {
        const date = name.slice(0, 10);
        const text = readFileSync(join(dir, name), 'utf8');
        const parts = text.split(/^## (\d{2}:\d{2} UTC)\s*$/m);
        for (let i = 1; i < parts.length; i += 2) {
          const cycleTime = parts[i];
          const body = parts[i + 1] || '';
          const sum = body.match(/\*\*Cycle summary\*\*:\s*([\s\S]*?)(?=\n#{1,3}\s|\n\*\*|\n## |$)/i);
          const summary = (sum ? sum[1] : '').replace(/\s+/g, ' ').trim().slice(0, 200);
          const storyTitles = [
            ...[...body.matchAll(/^####\s+\d+\.\s+(.+)$/gm)].map((m) => m[1].trim()),
            ...[...body.matchAll(/class="twitter-story-title"[^>]*>([^<]+)</g)].map((m) => m[1].trim()),
          ];
          if (!summary && storyTitles.length === 0) continue;
          const anchor = 'cycle-' + cycleTime.replace(/[:\s]/g, '').toLowerCase();
          out.twitter.push({ date, cycleTime, anchor, summary, storyTitles });
        }
      }
    }
  } catch (e) {
    console.warn('prebuild: twitter search index skipped:', e?.message || e);
  }
  writeFileSync(join(publicResearch, 'search-index.json'), JSON.stringify(out));
  console.log(
    `prebuild: search-index.json (${out.digestSections.length} digest sections, ${out.twitter.length} twitter cycles)`,
  );
}

copyData();
buildArmTimeline();
buildTicketsIndex();
buildManifest();
buildSearchIndex();
await hydrateTweets().catch((e) => console.warn('prebuild: tweet hydration skipped:', e?.message || e));
