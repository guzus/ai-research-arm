import './style.css';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

const DATA_BASE: string = import.meta.env.BASE_URL + 'research';

const DOC_ICON =
  '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">' +
  '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>' +
  '<path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>';

// ── Clock icon ───────────────────────────────────────────
/** Generate an SVG clock face with hands pointing to the given hour and minute */
function clockIcon(hours: number, minutes: number): string {
  const cx = 12, cy = 12, r = 9;
  // Minute hand
  const mAngle = (minutes / 60) * 360 - 90;
  const mRad = (mAngle * Math.PI) / 180;
  const mx = cx + Math.cos(mRad) * 6.5;
  const my = cy + Math.sin(mRad) * 6.5;
  // Hour hand
  const hAngle = ((hours % 12) / 12) * 360 + (minutes / 60) * 30 - 90;
  const hRad = (hAngle * Math.PI) / 180;
  const hx = cx + Math.cos(hRad) * 4.5;
  const hy = cy + Math.sin(hRad) * 4.5;

  return (
    '<svg class="clock-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">' +
    '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '"/>' +
    '<line x1="' + cx + '" y1="' + cy + '" x2="' + hx.toFixed(1) + '" y2="' + hy.toFixed(1) + '" stroke-width="2"/>' +
    '<line x1="' + cx + '" y1="' + cy + '" x2="' + mx.toFixed(1) + '" y2="' + my.toFixed(1) + '" stroke-width="1.5"/>' +
    '</svg>'
  );
}

/** Parse "HH:MM UTC" from title and return local time info */
function parseUtcTime(title: string, dateStr: string): { utc: string; local: string; localHours: number; localMinutes: number } | null {
  const match = title.match(/^(\d{2}):(\d{2})\s*UTC$/);
  if (!match) return null;
  const utcH = parseInt(match[1], 10);
  const utcM = parseInt(match[2], 10);
  const parts = dateStr.split('-');
  const d = new Date(Date.UTC(+parts[0], +parts[1] - 1, +parts[2], utcH, utcM));
  const localH = d.getHours();
  const localM = d.getMinutes();
  const localStr = d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
  return { utc: match[0], local: localStr, localHours: localH, localMinutes: localM };
}

// ── Tweet timestamp from Snowflake ID ─────────────────
const TWITTER_EPOCH = 1288834974657;

function snowflakeToDate(id: string): Date | null {
  try {
    const n = BigInt(id);
    const ms = Number(n >> 22n) + TWITTER_EPOCH;
    const d = new Date(ms);
    if (isNaN(d.getTime())) return null;
    return d;
  } catch {
    return null;
  }
}

function timeAgo(date: Date): string {
  const now = Date.now();
  const diff = now - date.getTime();
  if (diff < 0) return 'just now';
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return mins + 'm ago';
  const hours = Math.floor(mins / 60);
  if (hours < 24) return hours + 'h ago';
  const days = Math.floor(hours / 24);
  return days + 'd ago';
}

// ── State ─────────────────────────────────────────────
type Tab = 'today' | 'twitter' | 'models' | 'frontpage' | 'research';
type DateTab = Exclude<Tab, 'research'>;
type GenResearchRow = {
  slug: string;
  file: string;
  title: string;
  model: string;
  created_at: string;
  source: string;
  prompt: string;
  tags: string[];
};
type Manifest = {
  today: string[];
  twitter: string[];
  models: string[];
  frontpage: string[];
  audio: string[];
  generative: GenResearchRow[];
};

let currentDate = new Date();
let searchTerm = '';
let activeTab: Tab = 'today';
let selectedSlug: string | null = null;
let calendarMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
const availabilityCache = new Map<string, Set<string>>();
let loadRequestId = 0;
let activeLoadController: AbortController | null = null;
let searchDebounceId: number | null = null;
let manifest: Manifest | null = null;
let manifestPromise: Promise<Manifest | null> | null = null;
// Cache the last-fetched research doc body so search-as-you-type doesn't refetch.
let researchDocCache: { slug: string; body: string } | null = null;
const LOAD_TIMEOUT_MS = 12000;

// ── DOM refs ──────────────────────────────────────────
const content = document.getElementById('content')!;
const calendarEl = document.getElementById('calendar')!;
const searchInput = document.getElementById('searchInput') as HTMLInputElement;
const searchCountEl = document.getElementById('searchCount')!;

// ── Hash routing ─────────────────────────────────────
// Format:
//   date tabs:  #tab/YYYY-MM-DD  e.g. #models/2026-02-03, #twitter/2026-01-29
//   research:   #research        (index list)
//               #research/<slug> (single doc)
function updateHash(): void {
  let hash: string;
  if (activeTab === 'research') {
    hash = selectedSlug ? '#research/' + selectedSlug : '#research';
  } else {
    hash = '#' + activeTab + '/' + fmtDate(currentDate);
  }
  if (location.hash !== hash) {
    history.replaceState(null, '', hash);
  }
}

function applyHash(): boolean {
  const hash = location.hash.replace(/^#/, '');
  if (!hash) return false;
  const dateMatch = hash.match(/^(today|twitter|models|frontpage)(?:\/(\d{4}-\d{2}-\d{2}))?$/);
  if (dateMatch) {
    activeTab = dateMatch[1] as Tab;
    selectedSlug = null;
    if (dateMatch[2]) {
      const parts = dateMatch[2].split('-');
      currentDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
    }
    calendarMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    syncTabUi();
    return true;
  }
  const researchMatch = hash.match(/^research(?:\/([A-Za-z0-9._-]+))?$/);
  if (researchMatch) {
    activeTab = 'research';
    selectedSlug = researchMatch[1] || null;
    syncTabUi();
    return true;
  }
  return false;
}

function syncTabUi(): void {
  document.querySelectorAll('.tab').forEach((b) => {
    b.classList.toggle('active', (b as HTMLElement).dataset.tab === activeTab);
  });
  document.body.classList.toggle('tab-research', activeTab === 'research');
}

// ── Helpers ───────────────────────────────────────────
function fmtDate(d: Date): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

function displayDate(d: Date): string {
  return d.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function shiftDate(days: number): void {
  currentDate.setDate(currentDate.getDate() + days);
  const newMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
  if (newMonth.getTime() !== calendarMonth.getTime()) {
    calendarMonth = newMonth;
    probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
  }
  load();
}

// ── Manifest ──────────────────────────────────────────
async function loadManifest(): Promise<Manifest | null> {
  if (manifest) return manifest;
  if (manifestPromise) return manifestPromise;
  manifestPromise = (async () => {
    try {
      const resp = await fetch(`${DATA_BASE}/manifest.json`, { cache: 'no-cache' });
      if (!resp.ok) return null;
      const m = (await resp.json()) as Partial<Manifest>;
      // Normalize: ensure all sources have an array
      const normalized: Manifest = {
        today: Array.isArray(m.today) ? m.today : (Array.isArray((m as any).digest) ? (m as any).digest : []),
        twitter: Array.isArray(m.twitter) ? m.twitter : [],
        models: Array.isArray(m.models) ? m.models : [],
        frontpage: Array.isArray(m.frontpage) ? m.frontpage : [],
        audio: Array.isArray((m as any).audio) ? (m as any).audio : [],
        generative: Array.isArray((m as any).generative) ? (m as any).generative as GenResearchRow[] : [],
      };
      manifest = normalized;
      // Pre-populate availability cache from manifest
      hydrateAvailabilityFromManifest(normalized);
      return normalized;
    } catch {
      return null;
    }
  })();
  return manifestPromise;
}

function hydrateAvailabilityFromManifest(m: Manifest): void {
  // Calendar/availability is date-keyed; the research tab is slug-keyed and
  // skipped on purpose.
  const tabs: DateTab[] = ['today', 'twitter', 'models', 'frontpage'];
  for (const tab of tabs) {
    const dates = m[tab];
    // Group by year-month, populate cache
    for (const dateStr of dates) {
      const [y, mo] = dateStr.split('-');
      const key = `${tab}-${y}-${mo}`;
      let set = availabilityCache.get(key);
      if (!set) {
        set = new Set<string>();
        availabilityCache.set(key, set);
      }
      set.add(dateStr);
    }
  }
}

function manifestDates(tab: DateTab): string[] | null {
  return manifest ? manifest[tab] : null;
}

function findResearchRow(slug: string): GenResearchRow | null {
  if (!manifest) return null;
  for (const row of manifest.generative) {
    if (row.slug === slug) return row;
  }
  return null;
}

// ── Calendar ──────────────────────────────────────────
function dataUrlForDate(dateStr: string): string {
  if (activeTab === 'today') {
    return `${DATA_BASE}/digest/${dateStr}-digest.md`;
  }
  if (activeTab === 'models') {
    return `${DATA_BASE}/models/${dateStr}-timeline.md`;
  }
  if (activeTab === 'frontpage') {
    return `${DATA_BASE}/front-page/${dateStr}-front-page.png`;
  }
  return `${DATA_BASE}/twitter/${dateStr}.md`;
}

function cacheKey(year: number, month: number): string {
  return `${activeTab}-${year}-${String(month + 1).padStart(2, '0')}`;
}

function probeAvailability(year: number, month: number): void {
  const key = cacheKey(year, month);
  if (availabilityCache.has(key)) {
    renderCalendar();
    return;
  }

  // If manifest is loaded, hydrate already populated this; ensure empty set exists.
  if (manifest) {
    if (!availabilityCache.has(key)) {
      availabilityCache.set(key, new Set<string>());
    }
    renderCalendar();
    return;
  }

  // No manifest yet — wait for it, then render. Avoids the 404 storm entirely.
  const available = new Set<string>();
  availabilityCache.set(key, available);
  renderCalendar();

  loadManifest().then((m) => {
    if (m) {
      // Hydrate already filled the cache; just re-render if still relevant.
      if (calendarMonth.getFullYear() === year && calendarMonth.getMonth() === month) {
        renderCalendar();
      }
      return;
    }
    // Fallback: manifest unavailable (older deploy). HEAD-probe this month only.
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const promises: Promise<void>[] = [];
    for (let d = 1; d <= daysInMonth; d++) {
      const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      const url = dataUrlForDate(dateStr);
      promises.push(
        fetch(url, { method: 'HEAD' }).then((resp) => {
          if (resp.ok) available.add(dateStr);
        }).catch(() => {}),
      );
    }
    Promise.all(promises).then(() => {
      if (calendarMonth.getFullYear() === year && calendarMonth.getMonth() === month) {
        renderCalendar();
      }
    });
  });
}

function buildCalendarHtml(): string {
  const year = calendarMonth.getFullYear();
  const month = calendarMonth.getMonth();
  const key = cacheKey(year, month);
  const available = availabilityCache.get(key) || new Set<string>();
  const today = new Date();
  const todayStr = fmtDate(today);
  const selectedStr = fmtDate(currentDate);

  const monthLabel = calendarMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const prevMonthDays = new Date(year, month, 0).getDate();

  const dows = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];
  const open = calendarEl.classList.contains('open');
  const coverage = available.size;
  const coverageHint = coverage > 0 ? ' · ' + coverage + (coverage === 1 ? ' day' : ' days') : '';
  let html = '<div class="cal-header" data-cal-toggle>';
  html += '<span class="cal-header-label">' + monthLabel + '<span class="cal-coverage">' + coverageHint + '</span> <span class="cal-chevron">' + (open ? '&#9650;' : '&#9660;') + '</span></span>';
  html += '<div class="cal-header-nav">';
  html += '<button class="cal-nav-btn" data-cal-nav="-1">&lsaquo;</button>';
  html += '<button class="cal-today-btn" data-cal-today>Today</button>';
  html += '<button class="cal-nav-btn" data-cal-nav="1">&rsaquo;</button>';
  html += '</div></div>';

  html += '<div class="cal-grid">';
  for (const dow of dows) {
    html += '<div class="cal-dow">' + dow + '</div>';
  }

  for (let i = firstDay - 1; i >= 0; i--) {
    const d = prevMonthDays - i;
    const pm = month === 0 ? 11 : month - 1;
    const py = month === 0 ? year - 1 : year;
    const dateStr = `${py}-${String(pm + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    html += '<div class="cal-day other-month" data-date="' + dateStr + '">' + d + '</div>';
  }

  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    let cls = 'cal-day';
    if (dateStr === todayStr) cls += ' today';
    if (dateStr === selectedStr) cls += ' selected';
    if (available.has(dateStr)) cls += ' has-data';
    html += '<div class="' + cls + '" data-date="' + dateStr + '">' + d + '</div>';
  }

  const totalCells = firstDay + daysInMonth;
  const remaining = (7 - (totalCells % 7)) % 7;
  for (let d = 1; d <= remaining; d++) {
    const nm = month === 11 ? 0 : month + 1;
    const ny = month === 11 ? year + 1 : year;
    const dateStr = `${ny}-${String(nm + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    html += '<div class="cal-day other-month" data-date="' + dateStr + '">' + d + '</div>';
  }

  html += '</div>';
  return html;
}

function renderCalendar(): void {
  setSafeCalendar(calendarEl, buildCalendarHtml());
}

/** Safely set calendar content using DOMPurify */
function setSafeCalendar(el: HTMLElement, rawHtml: string): void {
  while (el.firstChild) el.removeChild(el.firstChild);
  const clean = DOMPurify.sanitize(rawHtml, {
    USE_PROFILES: { html: true },
    ADD_ATTR: ['data-date', 'data-cal-nav', 'data-cal-today', 'data-cal-toggle'],
  });
  el.insertAdjacentHTML('beforeend', clean);
}

function handleCalendarClick(e: Event): void {
  const target = e.target as HTMLElement;

  // Toggle fold/unfold when clicking the header (but not nav buttons)
  const toggleEl = target.closest('[data-cal-toggle]') as HTMLElement | null;
  if (toggleEl && !target.closest('[data-cal-nav]') && !target.closest('[data-cal-today]')) {
    calendarEl.classList.toggle('open');
    renderCalendar();
    return;
  }

  const navBtn = target.closest('[data-cal-nav]') as HTMLElement | null;
  if (navBtn) {
    const dir = parseInt(navBtn.dataset.calNav!, 10);
    calendarMonth.setMonth(calendarMonth.getMonth() + dir);
    probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
    return;
  }

  if (target.closest('[data-cal-today]')) {
    const now = new Date();
    currentDate = now;
    calendarMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
    load();
    return;
  }

  const dayEl = target.closest('.cal-day') as HTMLElement | null;
  if (dayEl && dayEl.dataset.date) {
    const parts = dayEl.dataset.date.split('-');
    currentDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
    const clickedMonth = new Date(+parts[0], +parts[1] - 1, 1);
    if (clickedMonth.getTime() !== calendarMonth.getTime()) {
      calendarMonth = clickedMonth;
      probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
    }
    load();
  }
}

function escapeHtml(str: string): string {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

/** Safely set element content using DOMPurify + insertAdjacentHTML */
function setSafeContent(el: HTMLElement, rawHtml: string): void {
  while (el.firstChild) el.removeChild(el.firstChild);
  const clean = DOMPurify.sanitize(rawHtml, {
    USE_PROFILES: { html: true, svg: true, svgFilters: true },
    ADD_TAGS: ['mark', 'article', 'figure', 'figcaption'],
    ADD_ATTR: ['data-slug'],
  });
  el.insertAdjacentHTML('beforeend', clean);
}

// ── Fetch ─────────────────────────────────────────────
async function fetchTwitter(dateStr: string, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/twitter/${dateStr}.md`;
  try {
    const resp = await fetch(url, { signal });
    if (!resp.ok) return null;
    return await resp.text();
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') return null;
    return null;
  }
}

async function fetchFrontPage(dateStr: string, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/front-page/${dateStr}-front-page.png`;
  try {
    const resp = await fetch(url, { method: 'HEAD', signal });
    if (!resp.ok) return null;
    return url;
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') return null;
    return null;
  }
}

async function fetchModels(dateStr: string, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/models/${dateStr}-timeline.md`;
  try {
    const resp = await fetch(url, { signal });
    if (!resp.ok) return null;
    return await resp.text();
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') return null;
    return null;
  }
}

async function fetchDigest(dateStr: string, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/digest/${dateStr}-digest.md`;
  try {
    const resp = await fetch(url, { signal });
    if (!resp.ok) return null;
    return await resp.text();
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') return null;
    return null;
  }
}

async function fetchResearchDoc(row: GenResearchRow, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/generative/${row.file}`;
  try {
    const resp = await fetch(url, { signal });
    if (!resp.ok) return null;
    return await resp.text();
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') return null;
    return null;
  }
}

/** Find the most recent date <= target that has data in the manifest for this tab. */
function findMostRecentAvailable(tab: DateTab, targetDateStr: string): string | null {
  const dates = manifestDates(tab);
  if (!dates || dates.length === 0) return null;
  // dates is sorted ascending; find largest <= target
  let best: string | null = null;
  for (const d of dates) {
    if (d <= targetDateStr) best = d;
    else break;
  }
  return best;
}

/** Race a promise against a timeout. Returns 'timeout' if exceeded. */
function withTimeout<T>(p: Promise<T>, ms: number, controller: AbortController): Promise<T | 'timeout'> {
  return new Promise((resolve) => {
    const t = window.setTimeout(() => {
      controller.abort();
      resolve('timeout');
    }, ms);
    p.then((v) => {
      window.clearTimeout(t);
      resolve(v);
    }).catch(() => {
      window.clearTimeout(t);
      resolve('timeout');
    });
  });
}

// ── Rendering ─────────────────────────────────────────
function showLoading(): void {
  const label = activeTab === 'frontpage'
    ? 'Loading front page\u2026'
    : activeTab === 'models'
    ? 'Loading model timeline\u2026'
    : activeTab === 'research'
    ? (selectedSlug ? 'Loading article\u2026' : 'Loading research index\u2026')
    : 'Loading Twitter report\u2026';
  setSafeContent(
    content,
    [
      '<div class="content-card">',
      '  <div class="loading-indicator">',
      '    <div class="loading-bar"><div class="loading-bar-inner"></div></div>',
      '    <div class="loading-text">' + label + '</div>',
      '  </div>',
      '</div>',
    ].join('\n'),
  );
}

function showEmpty(dateStr: string): void {
  const label = activeTab === 'today'
    ? 'No digest yet for ' + escapeHtml(dateStr)
    : activeTab === 'frontpage'
    ? 'No front page for ' + escapeHtml(dateStr)
    : activeTab === 'models'
    ? 'No model timeline for ' + escapeHtml(dateStr)
    : activeTab === 'research'
    ? (selectedSlug ? 'Article not found: ' + escapeHtml(selectedSlug) : 'No research articles yet')
    : 'No Twitter report for ' + escapeHtml(dateStr);
  setSafeContent(
    content,
    [
      '<div class="content-card">',
      '  <div class="empty-state">',
      '    <div class="empty-state-icon">' + DOC_ICON + '</div>',
      '    <div class="empty-state-text">' + label + '</div>',
      '  </div>',
      '</div>',
    ].join('\n'),
  );
}

function showError(message: string, hint?: string): void {
  setSafeContent(
    content,
    [
      '<div class="content-card">',
      '  <div class="error-state">',
      '    <div class="error-state-text">' + escapeHtml(message) + '</div>',
      hint ? '    <div class="error-state-hint">' + escapeHtml(hint) + '</div>' : '',
      '    <button class="retry-btn" data-retry>Retry</button>',
      '  </div>',
      '</div>',
    ].join('\n'),
  );
}

/** Split markdown by ## headings into separate sections */
function splitSections(md: string): { title: string; body: string }[] {
  const lines = md.split('\n');
  const sections: { title: string; body: string }[] = [];
  let currentTitle = '';
  let currentLines: string[] = [];

  for (const line of lines) {
    const h2Match = line.match(/^## (.+)/);
    if (h2Match) {
      if (currentTitle || currentLines.length) {
        sections.push({ title: currentTitle, body: currentLines.join('\n').trim() });
      }
      currentTitle = h2Match[1];
      currentLines = [];
    } else {
      currentLines.push(line);
    }
  }
  if (currentTitle || currentLines.length) {
    sections.push({ title: currentTitle, body: currentLines.join('\n').trim() });
  }
  return sections;
}

/** Wrap rendered tables in a horizontally scrollable container so wide tables
 * (many columns or long cell content) don't overflow the card. */
function wrapTables(html: string): string {
  return html
    .replace(/<table(\s[^>]*)?>/g, '<div class="md-table-wrap"><table$1>')
    .replace(/<\/table>/g, '</table></div>');
}

function renderReport(md: string): void {
  const sections = splitSections(md).reverse();
  const cards: string[] = [];

  for (const section of sections) {
    // Skip the top-level h1 title section if it has no body
    if (!section.title && !section.body) continue;

    let html = marked.parse(section.body) as string;
    html = wrapTables(html);

    // Add time-ago labels to tweet URLs (extract Snowflake ID from status URL)
    html = html.replace(
      /href="https?:\/\/(?:x|twitter)\.com\/\w+\/status\/(\d+)"[^>]*>([^<]+)<\/a>/g,
      (match, tweetId: string) => {
        const date = snowflakeToDate(tweetId);
        if (!date) return match;
        const ago = timeAgo(date);
        return match + '<span class="tweet-ago">' + escapeHtml(ago) + '</span>';
      },
    );

    // Highlight @handles
    html = html.replace(
      /(?<!\w)(@\w+)/g,
      '<span class="handle">$1</span>',
    );

    if (searchTerm) {
      const escaped = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const re = new RegExp('(' + escaped + ')', 'gi');
      html = html.replace(re, '<mark>$1</mark>');
    }

    // Use the ## heading as the card title, or fall back to date
    const title = section.title || displayDate(currentDate);
    const dateStr = fmtDate(currentDate);
    const timeInfo = parseUtcTime(section.title, dateStr);

    let headerHtml: string;
    if (timeInfo) {
      headerHtml =
        '  <div class="content-card-header">' +
        '    ' + clockIcon(timeInfo.localHours, timeInfo.localMinutes) +
        '    <div class="content-card-title">' + escapeHtml(timeInfo.utc) +
        '      <span class="local-time">' + escapeHtml(timeInfo.local) + '</span>' +
        '    </div>' +
        '  </div>';
    } else {
      headerHtml =
        '  <div class="content-card-header">' +
        '    <div class="content-card-title">' + escapeHtml(title) + '</div>' +
        '  </div>';
    }

    cards.push(
      [
        '<div class="content-card">',
        headerHtml,
        '  <div class="content-card-body">',
        '    <div class="md-content">' + html + '</div>',
        '  </div>',
        '</div>',
      ].join('\n'),
    );
  }

  setSafeContent(content, cards.join('\n'));
}

function renderModels(md: string): void {
  const sections = splitSections(md);
  const cards: string[] = [];

  for (const section of sections) {
    if (!section.title && !section.body) continue;

    let html = marked.parse(section.body) as string;
    html = wrapTables(html);

    if (searchTerm) {
      const escaped = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const re = new RegExp('(' + escaped + ')', 'gi');
      html = html.replace(re, '<mark>$1</mark>');
    }

    const title = section.title || displayDate(currentDate);

    cards.push(
      [
        '<div class="content-card">',
        '  <div class="content-card-header">',
        '    <div class="content-card-title">' + escapeHtml(title) + '</div>',
        '  </div>',
        '  <div class="content-card-body">',
        '    <div class="md-content">' + html + '</div>',
        '  </div>',
        '</div>',
      ].join('\n'),
    );
  }

  setSafeContent(content, cards.join('\n'));
}

function renderFrontPage(imageUrl: string, fallbackDate: string | null): void {
  const noteHtml = fallbackDate
    ? '  <div class="frontpage-fallback-note">Today’s front page auto-generates at 00:30 UTC. Showing ' + escapeHtml(fallbackDate) + ' instead.</div>'
    : '';
  setSafeContent(
    content,
    [
      '<div class="content-card frontpage-card">',
      '  <div class="content-card-header">',
      '    <div class="content-card-title">THE AI INTELLIGENCER — ' + escapeHtml(displayDate(currentDate)) + '</div>',
      '  </div>',
      noteHtml,
      '  <div class="content-card-body frontpage-body">',
      '    <img class="frontpage-img" src="' + escapeHtml(imageUrl) + '" alt="Front Page" />',
      '  </div>',
      '</div>',
    ].join('\n'),
  );
}

/** Render the daily digest. Treats Executive Summary specially as a TL;DR block. */
function renderToday(md: string): void {
  const sections = splitSections(md);
  const cards: string[] = [];

  // Prepend an audio player if a Deepgram-generated digest MP3 exists for
  // this date. Manifest is populated by deploy-dashboard.yml's manifest step.
  const dateStr = fmtDate(currentDate);
  if (manifest?.audio?.includes(dateStr)) {
    const audioUrl = `${DATA_BASE}/audio/${dateStr}-digest.mp3`;
    cards.push(
      [
        '<div class="content-card today-audio-card">',
        '  <div class="content-card-header">',
        '    <div class="content-card-title">🎧 Audio digest</div>',
        '  </div>',
        '  <div class="content-card-body">',
        '    <audio controls preload="metadata" style="width:100%;" src="' + audioUrl + '">',
        '      Your browser does not support the audio element.',
        '    </audio>',
        '  </div>',
        '</div>',
      ].join('\n'),
    );
  }

  for (const section of sections) {
    if (!section.title && !section.body) continue;

    const isSummary = /^(executive summary|tl;dr|tldr|summary)$/i.test(section.title.trim());
    let html = marked.parse(section.body) as string;
    html = wrapTables(html);

    html = html.replace(
      /(?<!\w)(@\w+)/g,
      '<span class="handle">$1</span>',
    );

    if (searchTerm) {
      const escaped = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const re = new RegExp('(' + escaped + ')', 'gi');
      html = html.replace(re, '<mark>$1</mark>');
    }

    const title = section.title || displayDate(currentDate);

    if (isSummary) {
      // Render as TL;DR block (lead card)
      cards.push(
        [
          '<div class="content-card today-card">',
          '  <div class="content-card-header">',
          '    <div class="content-card-title">' + escapeHtml(displayDate(currentDate)) + '</div>',
          '  </div>',
          '  <div class="content-card-body">',
          '    <div class="today-tldr">',
          '      <span class="today-tldr-label">TL;DR</span>',
          '      <div class="md-content">' + html + '</div>',
          '    </div>',
          '  </div>',
          '</div>',
        ].join('\n'),
      );
    } else {
      cards.push(
        [
          '<div class="content-card">',
          '  <div class="content-card-header">',
          '    <div class="content-card-title">' + escapeHtml(title) + '</div>',
          '  </div>',
          '  <div class="content-card-body">',
          '    <div class="md-content">' + html + '</div>',
          '  </div>',
          '</div>',
        ].join('\n'),
      );
    }
  }

  setSafeContent(content, cards.join('\n'));
}

// ── Generative research ───────────────────────────────
function renderResearchIndex(rows: GenResearchRow[]): void {
  if (rows.length === 0) {
    showEmpty(fmtDate(currentDate));
    return;
  }
  const term = searchTerm.toLowerCase();
  // Newest first. The writer appends ascending, so reverse.
  const reversed = rows.slice().reverse();
  const visible = term
    ? reversed.filter((r) => {
        const hay = (r.title + ' ' + r.prompt + ' ' + (r.tags || []).join(' ')).toLowerCase();
        return hay.indexOf(term) !== -1;
      })
    : reversed;

  const items: string[] = [];
  for (const row of visible) {
    let title = escapeHtml(row.title);
    if (searchTerm) {
      const escaped = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const re = new RegExp('(' + escaped + ')', 'gi');
      title = title.replace(re, '<mark>$1</mark>');
    }
    const created = new Date(row.created_at);
    const rel = isNaN(created.getTime()) ? '' : timeAgo(created);
    const tagHtml = (row.tags || [])
      .map((t) => '<span class="gen-research-tag">' + escapeHtml(t) + '</span>')
      .join('');
    items.push(
      [
        '<li class="gen-research-item" data-slug="' + escapeHtml(row.slug) + '" tabindex="0">',
        '  <div class="gen-research-item-title">' + title + '</div>',
        '  <div class="gen-research-item-meta">',
        '    <span class="gen-research-model">' + escapeHtml(row.model) + '</span>',
        rel ? '    <span class="gen-research-time">' + escapeHtml(rel) + '</span>' : '',
        tagHtml ? '    <span class="gen-research-tags">' + tagHtml + '</span>' : '',
        '  </div>',
        '</li>',
      ].join('\n'),
    );
  }

  const empty = visible.length === 0
    ? '<div class="empty-state-text gen-research-empty">No articles match the search.</div>'
    : '';

  setSafeContent(
    content,
    [
      '<div class="content-card">',
      '  <div class="content-card-header">',
      '    <div class="content-card-title">Generative research</div>',
      '  </div>',
      '  <div class="content-card-body">',
      '    <ul class="gen-research-index">',
      items.join('\n'),
      '    </ul>',
      empty,
      '  </div>',
      '</div>',
    ].join('\n'),
  );
}

function renderResearchDoc(row: GenResearchRow, body: string): void {
  let docHtml = body;
  if (searchTerm) {
    const escaped = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp('(' + escaped + ')', 'gi');
    // Apply mark only to text outside tags. Simple split-by-tag pass.
    docHtml = docHtml.replace(/>([^<]+)</g, (_m, text: string) => {
      return '>' + text.replace(re, '<mark>$1</mark>') + '<';
    });
  }
  const created = new Date(row.created_at);
  const rel = isNaN(created.getTime()) ? '' : timeAgo(created);

  setSafeContent(
    content,
    [
      '<div class="content-card gen-research-doc">',
      '  <div class="content-card-header">',
      '    <div class="content-card-title">' + escapeHtml(row.title) + '</div>',
      '  </div>',
      '  <div class="gen-research-doc-meta">',
      '    <button class="gen-research-back" data-research-back>&lsaquo; All articles</button>',
      '    <span class="gen-research-model">' + escapeHtml(row.model) + '</span>',
      rel ? '    <span class="gen-research-time">' + escapeHtml(rel) + '</span>' : '',
      '  </div>',
      '  <div class="content-card-body">',
      docHtml,
      '  </div>',
      '</div>',
    ].join('\n'),
  );
}

// ── Main load ─────────────────────────────────────────
async function load(): Promise<void> {
  const dateStr = fmtDate(currentDate);
  const requestId = ++loadRequestId;
  if (activeLoadController) activeLoadController.abort();
  const controller = new AbortController();
  activeLoadController = controller;

  updateHash();
  showLoading();

  try {
    if (activeTab === 'research') {
      // Make sure the manifest (and therefore the generative index) is loaded.
      const m = manifest || await loadManifest();
      if (requestId !== loadRequestId) return;
      const rows = m?.generative ?? [];
      if (!selectedSlug) {
        researchDocCache = null;
        renderResearchIndex(rows);
      } else {
        const row = findResearchRow(selectedSlug);
        if (!row) {
          showEmpty(dateStr);
        } else if (researchDocCache && researchDocCache.slug === selectedSlug) {
          renderResearchDoc(row, researchDocCache.body);
        } else {
          const result = await withTimeout(fetchResearchDoc(row, controller.signal), LOAD_TIMEOUT_MS, controller);
          if (requestId !== loadRequestId) return;
          if (result === 'timeout') {
            showError('Loading timed out', 'Network may be slow. Click to retry.');
          } else if (result) {
            researchDocCache = { slug: selectedSlug, body: result };
            renderResearchDoc(row, result);
          } else {
            showEmpty(dateStr);
          }
        }
      }
    } else if (activeTab === 'frontpage') {
      const result = await withTimeout(fetchFrontPage(dateStr, controller.signal), LOAD_TIMEOUT_MS, controller);
      if (requestId !== loadRequestId) return;
      if (result === 'timeout') {
        showError('Loading timed out', 'Network may be slow. Click to retry.');
      } else if (result) {
        renderFrontPage(result, null);
      } else {
        // Front page missing for today — fall back to the most recent available
        const fallback = findMostRecentAvailable('frontpage', dateStr);
        if (fallback && fallback !== dateStr) {
          const fallbackUrl = `${DATA_BASE}/front-page/${fallback}-front-page.png`;
          renderFrontPage(fallbackUrl, fallback);
        } else {
          showEmpty(dateStr);
        }
      }
    } else if (activeTab === 'models') {
      const result = await withTimeout(fetchModels(dateStr, controller.signal), LOAD_TIMEOUT_MS, controller);
      if (requestId !== loadRequestId) return;
      if (result === 'timeout') {
        showError('Loading timed out', 'Network may be slow. Click to retry.');
      } else if (result) {
        renderModels(result);
      } else {
        showEmpty(dateStr);
      }
    } else if (activeTab === 'today') {
      const result = await withTimeout(fetchDigest(dateStr, controller.signal), LOAD_TIMEOUT_MS, controller);
      if (requestId !== loadRequestId) return;
      if (result === 'timeout') {
        showError('Loading timed out', 'Network may be slow. Click to retry.');
      } else if (result) {
        renderToday(result);
      } else {
        // Digest missing — fall back to most recent
        const fallback = findMostRecentAvailable('today', dateStr);
        if (fallback && fallback !== dateStr) {
          const fallbackMd = await fetchDigest(fallback, controller.signal);
          if (fallbackMd) {
            renderToday(fallbackMd);
            // Tweak the lead card with a fallback note
            const lead = content.querySelector('.today-card .content-card-title');
            if (lead) {
              lead.textContent = displayDate(currentDate) + ' · digest from ' + fallback;
            }
          } else {
            showEmpty(dateStr);
          }
        } else {
          showEmpty(dateStr);
        }
      }
    } else {
      const result = await withTimeout(fetchTwitter(dateStr, controller.signal), LOAD_TIMEOUT_MS, controller);
      if (requestId !== loadRequestId) return;
      if (result === 'timeout') {
        showError('Loading timed out', 'Network may be slow. Click to retry.');
      } else if (result) {
        renderReport(result);
      } else {
        showEmpty(dateStr);
      }
    }

    renderCalendar();
    currentSection = 0;
    updateNavCounter();
    updateSearchCount();
  } finally {
    if (activeLoadController === controller) {
      activeLoadController = null;
    }
  }
}

// ── Section navigation ─────────────────────────────────
let currentSection = 0;
const navCounter = document.getElementById('navCounter')!;

function getCards(): HTMLElement[] {
  return Array.from(content.querySelectorAll('.content-card'));
}

function updateNavCounter(): void {
  const cards = getCards();
  while (navCounter.firstChild) navCounter.removeChild(navCounter.firstChild);
  if (cards.length === 0) return;
  const card = cards[currentSection];
  const titleEl = card?.querySelector('.content-card-title');
  const titleText = (titleEl?.textContent || '').trim();
  const shortTitle = titleText.length > 18 ? titleText.slice(0, 16) + '…' : titleText;
  if (shortTitle) {
    const labelSpan = document.createElement('span');
    labelSpan.className = 'section-nav-counter-label';
    labelSpan.textContent = shortTitle;
    navCounter.appendChild(labelSpan);
  }
  const numSpan = document.createElement('span');
  numSpan.className = 'section-nav-counter-num';
  numSpan.textContent = (currentSection + 1) + '/' + cards.length;
  navCounter.appendChild(numSpan);
}

function updateSearchCount(): void {
  if (!searchTerm) {
    searchCountEl.textContent = '';
    return;
  }
  const matches = content.querySelectorAll('mark').length;
  const cards = getCards().length;
  searchCountEl.textContent = matches === 0 ? '0 matches' : matches + ' in ' + cards;
}

function scrollToSection(index: number): void {
  const cards = getCards();
  if (cards.length === 0) return;
  currentSection = Math.max(0, Math.min(index, cards.length - 1));
  cards[currentSection].scrollIntoView({ behavior: 'smooth', block: 'start' });
  updateNavCounter();
}

document.getElementById('navUp')!.addEventListener('click', () => scrollToSection(currentSection - 1));
document.getElementById('navDown')!.addEventListener('click', () => scrollToSection(currentSection + 1));

// ── Shortcut guide ────────────────────────────────────
const shortcutPanel = document.getElementById('shortcutPanel')!;
document.getElementById('shortcutToggle')!.addEventListener('click', () => {
  shortcutPanel.classList.toggle('open');
});

// ── Events ────────────────────────────────────────────

searchInput.addEventListener('input', () => {
  if (searchDebounceId !== null) window.clearTimeout(searchDebounceId);
  searchDebounceId = window.setTimeout(() => {
    searchTerm = searchInput.value.trim();
    load();
  }, 180);
});

// Retry button + research index navigation (event delegation on content)
content.addEventListener('click', (e) => {
  const target = e.target as HTMLElement;
  if (target.closest('[data-retry]')) {
    load();
    return;
  }
  const back = target.closest('[data-research-back]') as HTMLElement | null;
  if (back) {
    selectedSlug = null;
    load();
    return;
  }
  const row = target.closest('[data-slug]') as HTMLElement | null;
  if (row && activeTab === 'research') {
    const slug = row.dataset.slug;
    if (slug) {
      selectedSlug = slug;
      load();
    }
  }
});

content.addEventListener('keydown', (e: KeyboardEvent) => {
  if (e.key !== 'Enter' && e.key !== ' ') return;
  const target = e.target as HTMLElement;
  const row = target.closest('[data-slug]') as HTMLElement | null;
  if (row && activeTab === 'research') {
    e.preventDefault();
    const slug = row.dataset.slug;
    if (slug) {
      selectedSlug = slug;
      load();
    }
  }
});

document.getElementById('refreshBtn')!.addEventListener('click', () => {
  const btn = document.getElementById('refreshBtn')!;
  btn.classList.add('spinning');
  load().then(() => setTimeout(() => btn.classList.remove('spinning'), 500));
});

// Keyboard shortcuts
document.addEventListener('keydown', (e: KeyboardEvent) => {
  if ((e.target as HTMLElement).tagName === 'INPUT') return;
  switch (e.key) {
    case 'ArrowUp':
      e.preventDefault();
      scrollToSection(currentSection - 1);
      break;
    case 'ArrowDown':
      e.preventDefault();
      scrollToSection(currentSection + 1);
      break;
    case '[':
      shiftDate(-1);
      break;
    case ']':
      shiftDate(1);
      break;
    case 't':
    case 'T': {
      const now = new Date();
      currentDate = now;
      calendarMonth = new Date(now.getFullYear(), now.getMonth(), 1);
      probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
      load();
      break;
    }
    case '/':
      e.preventDefault();
      searchInput.focus();
      break;
    case 'r':
    case 'R':
      load();
      break;
    case '?':
      shortcutPanel.classList.toggle('open');
      break;
  }
});

// ── Tab navigation ────────────────────────────────────
document.querySelectorAll<HTMLButtonElement>('.tab').forEach((btn) => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab as Tab;
    if (tab === activeTab) return;
    activeTab = tab;
    selectedSlug = null;
    document.querySelectorAll('.tab').forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    document.body.classList.toggle('tab-research', activeTab === 'research');
    // Re-probe availability for current month with new tab (date tabs only).
    if (activeTab !== 'research') {
      probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
    }
    load();
  });
});

// ── Init ──────────────────────────────────────────────
calendarEl.addEventListener('click', handleCalendarClick);
// Kick off manifest fetch early so calendar + fallback logic have data ASAP.
loadManifest();
applyHash();
// applyHash() may have mutated activeTab to anything in Tab; TS won't see
// that across the function boundary, so we widen the read explicitly.
const currentTab: Tab = activeTab as Tab;
document.body.classList.toggle('tab-research', currentTab === 'research');
if (currentTab !== 'research') {
  probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
}
load();

window.addEventListener('hashchange', () => {
  if (applyHash()) load();
});
