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
type GenResearchKind = 'fragment' | 'standalone';
type GenResearchRow = {
  slug: string;
  file: string;
  kind?: GenResearchKind;  // optional for back-compat; undefined = fragment
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

// ── Path routing ─────────────────────────────────────
// Format (history API, no hash):
//   date tabs:  /tab/YYYY-MM-DD  e.g. /models/2026-02-03, /twitter/2026-01-29
//   research:   /research        (index list)
//               /research/<slug> (single doc)
// Static fetches under /research/... (manifest.json, generative/*.html, etc.)
// are disambiguated from routes by the file extension; Vercel rewrites only
// extensionless paths to /index.html.
function routeFromState(): string {
  if (activeTab === 'research') {
    return selectedSlug ? '/research/' + selectedSlug : '/research';
  }
  return '/' + activeTab + '/' + fmtDate(currentDate);
}

// Tracks whether the SPA has rendered at least once. The first call
// to updateRoute() comes from the initial load() and must not add a
// history entry (the user's just-landed URL already lives at the top
// of the stack). Every subsequent call is a user navigation and gets
// pushState so browser back/forward walks through the visited views.
let routeInitialized = false;

// Tracks the last pathname we routed to. Lets popstate distinguish a
// real route change from a hash-only navigation (anchor click between
// sections in the same article). Maintained from both updateRoute and
// the popstate handler.
let lastAppliedPathname = location.pathname;

// gtag is loaded by the <script> in index.html. Type as optional so the
// dashboard still works when GA is blocked (adblockers, privacy modes).
declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
  }
}

/** Fire a SPA page_view to GA. The `gtag('config')` in index.html only
 * fires automatically on the initial document load; in-app pushState /
 * popstate navigation has to be tracked manually. page_title may lag
 * by one nav (set in render functions that run after this) — page_path
 * is always accurate, which is what GA reports key on. */
function trackPageView(): void {
  if (typeof window.gtag !== 'function') return;
  window.gtag('event', 'page_view', {
    page_path: location.pathname + location.search,
    page_title: document.title,
    page_location: location.href,
  });
}

function updateRoute(): void {
  const target = routeFromState();
  const current = location.pathname + location.search;
  if (current !== target) {
    if (routeInitialized) {
      history.pushState(null, '', target);
      trackPageView();
    } else {
      history.replaceState(null, '', target);
    }
  }
  routeInitialized = true;
  lastAppliedPathname = location.pathname;
}

function parseRoute(path: string): boolean {
  // Strip the trailing slash but keep the leading one
  const clean = path.replace(/\/+$/, '') || '/';
  if (clean === '/') return false;
  const trimmed = clean.replace(/^\/+/, '');
  const dateMatch = trimmed.match(/^(today|twitter|models|frontpage)(?:\/(\d{4}-\d{2}-\d{2}))?$/);
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
  const researchMatch = trimmed.match(/^research(?:\/([A-Za-z0-9._-]+))?$/);
  if (researchMatch) {
    activeTab = 'research';
    selectedSlug = researchMatch[1] || null;
    syncTabUi();
    return true;
  }
  return false;
}

function applyRoute(): boolean {
  // Migrate legacy hash URLs (#research/<slug>, #twitter/<date>) to clean paths
  // so existing bookmarks keep working without an explicit redirect.
  if (location.hash) {
    const legacy = location.hash.replace(/^#/, '');
    if (legacy && parseRoute('/' + legacy)) {
      history.replaceState(null, '', routeFromState());
      return true;
    }
  }
  return parseRoute(location.pathname);
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

/** Safely set element content using DOMPurify + insertAdjacentHTML.
 * `iframe` is allowed only with sandbox/src/loading/title attributes; we
 * use it for standalone research docs whose styling/scripts are isolated
 * inside a sandboxed iframe. Fragments cannot embed iframes — the writer's
 * deny list rejects <iframe in fragment bodies before they reach here. */
function setSafeContent(el: HTMLElement, rawHtml: string): void {
  while (el.firstChild) el.removeChild(el.firstChild);
  const clean = DOMPurify.sanitize(rawHtml, {
    USE_PROFILES: { html: true, svg: true, svgFilters: true },
    ADD_TAGS: ['mark', 'article', 'figure', 'figcaption', 'iframe'],
    ADD_ATTR: ['data-slug', 'data-pct', 'sandbox', 'loading', 'allow'],
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

/** Render the daily digest. Treats Executive Summary specially as a TL;DR block.
 * When `frontPage` is supplied the layout splits into two desktop columns: front
 * page on the left, digest cards on the right. Stacks under ~900px. */
function renderToday(md: string, frontPage: { url: string; fallback: string | null } | null = null): void {
  const sections = splitSections(md);

  // Digest files often start with `# AI Daily Digest - <date>` before the
  // first `## Section`, which duplicates the date already shown in the
  // card header. Strip the leading h1 from the pre-`##` body; if nothing
  // else remains, drop the section so we don't render a blank card.
  if (sections.length > 0 && !sections[0].title) {
    sections[0].body = sections[0].body.replace(/^\s*#\s+[^\n]+\n*/, '').trim();
    if (!sections[0].body) sections.shift();
  }

  const cards: string[] = [];

  // Prepend an audio player if a Deepgram-generated digest MP3 exists for
  // this date. Manifest is populated by dashboard/scripts/prebuild.mjs.
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

  const todayCards = cards.join('\n');
  if (frontPage) {
    const noteHtml = frontPage.fallback
      ? '  <div class="frontpage-fallback-note">Today’s front page auto-generates at 00:30 UTC. Showing ' + escapeHtml(frontPage.fallback) + ' instead.</div>'
      : '';
    const fpCard = [
      '<div class="content-card frontpage-card today-frontpage-card">',
      '  <div class="content-card-header">',
      '    <div class="content-card-title">THE AI INTELLIGENCER — ' + escapeHtml(displayDate(currentDate)) + '</div>',
      '  </div>',
      noteHtml,
      '  <div class="content-card-body frontpage-body">',
      '    <img class="frontpage-img" src="' + escapeHtml(frontPage.url) + '" alt="Front Page" />',
      '  </div>',
      '</div>',
    ].join('\n');
    setSafeContent(
      content,
      [
        '<div class="today-layout">',
        '  <div class="today-layout-frontpage">' + fpCard + '</div>',
        '  <div class="today-layout-digest">' + todayCards + '</div>',
        '</div>',
      ].join('\n'),
    );
    return;
  }
  setSafeContent(content, todayCards);
}

// ── Generative research ───────────────────────────────

// Default <title> from index.html, used to reset when leaving an article.
const DEFAULT_DOC_TITLE = document.title;

/** Update the browser title so the print dialog suggests a useful PDF
 * filename (browsers default to <title>). Reset on back-to-index. */
function setDocTitle(articleTitle: string | null): void {
  document.title = articleTitle
    ? `${articleTitle} — ara`
    : DEFAULT_DOC_TITLE;
}

function renderResearchIndex(rows: GenResearchRow[]): void {
  setDocTitle(null);
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
    // Surface first three tags inline; the chip on the right indicates fragment vs standalone.
    const tagHtml = (row.tags || [])
      .slice(0, 3)
      .map((t) => '<span class="gen-research-tag">' + escapeHtml(t) + '</span>')
      .join('');
    const isStandalone = row.kind === 'standalone';
    const kindLabel = isStandalone ? 'Standalone' : 'Article';
    const kindClass = isStandalone ? 'gen-research-kind--standalone' : 'gen-research-kind--article';
    items.push(
      [
        '<li class="gen-research-item" data-slug="' + escapeHtml(row.slug) + '" tabindex="0">',
        '  <div class="gen-research-item-main">',
        '    <div class="gen-research-item-title">' + title + '</div>',
        '    <div class="gen-research-item-meta">',
        '      <span class="gen-research-model">' + escapeHtml(row.model) + '</span>',
        rel ? '      <span class="gen-research-time">' + escapeHtml(rel) + '</span>' : '',
        tagHtml ? '      <span class="gen-research-tags">' + tagHtml + '</span>' : '',
        '    </div>',
        '  </div>',
        '  <span class="gen-research-kind ' + kindClass + '">' + kindLabel + '</span>',
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
      '    <button class="gen-research-pdf" data-research-pdf title="Save this article as a PDF">Save as PDF</button>',
      '  </div>',
      '  <div class="content-card-body">',
      docHtml,
      '  </div>',
      '</div>',
    ].join('\n'),
  );

  setDocTitle(row.title);

  // After DOM is in place, apply data-pct viz fills, wrap tables in a
  // horizontal-scroll container, expand pictogram counts, inject SVG
  // charts, and build the floating TOC.
  const article = content.querySelector('article.ara-doc') as HTMLElement | null;
  if (article) {
    applyBarFills(article);
    wrapAraTables(article);
    applyIsotypes(article);
    renderSparklines(article);
    renderLineCharts(article);
    renderDonuts(article);
    renderSlopes(article);
    renderResearchTOC(article);
    addSectionAnchors(article);
    scrollToHashIfPresent();
  } else {
    hideResearchTOC();
  }
}

/** Expand `<span class="ara-iso-glyphs" data-count="17" data-glyph="🚶">`
 * into N repeated child glyph spans. Done in JS (not in the article HTML)
 * so authors don't have to paste long strings of identical glyphs and so
 * the count is machine-readable. Hard cap at 200 to keep a typo from
 * rendering a million emoji into the DOM. */
function applyIsotypes(root: HTMLElement): void {
  const groups = root.querySelectorAll<HTMLElement>('.ara-iso-glyphs');
  for (const g of groups) {
    if (g.dataset.expanded === '1') continue;
    const count = Math.max(0, Math.min(200, Number(g.dataset.count) || 0));
    const glyph = g.dataset.glyph || '•';
    g.textContent = '';
    for (let i = 0; i < count; i++) {
      const s = document.createElement('span');
      s.className = 'ara-iso-glyph';
      s.textContent = glyph;
      g.appendChild(s);
    }
    g.dataset.expanded = '1';
  }
}

// ── SVG chart injection ──────────────────────────────────────────────
//
// Authored markup uses <div data-*> only — the writer's tag allowlist
// rejects <svg> in fragments, so we generate SVG at render time and
// inject it here. Same security model as applyBarFills / applyIsotypes:
// values come from data-* attrs (validator strips on*= and inline style),
// and we never `innerHTML` raw author strings — every numeric attr is
// parsed and clamped before being templated into the SVG.

const SVG_NS = 'http://www.w3.org/2000/svg';

function svgEl<T extends SVGElement>(tag: string, attrs: Record<string, string | number>): T {
  const el = document.createElementNS(SVG_NS, tag) as T;
  for (const [k, v] of Object.entries(attrs)) {
    el.setAttribute(k, String(v));
  }
  return el;
}

/** Parse a comma-separated number list from a data attribute. Drops
 * anything non-finite. Caps length so a typo can't blow up render. */
function parseSeries(raw: string | undefined, cap = 1000): number[] {
  if (!raw) return [];
  return raw
    .split(',')
    .map((s) => Number(s.trim()))
    .filter((n) => Number.isFinite(n))
    .slice(0, cap);
}

function parseLabels(raw: string | undefined, cap = 200): string[] {
  if (!raw) return [];
  return raw.split(',').map((s) => s.trim()).slice(0, cap);
}

/** Build a polyline d-attribute from (x,y) pairs. */
function pathFromPoints(points: Array<[number, number]>): string {
  if (!points.length) return '';
  return points
    .map(([x, y], i) => (i === 0 ? `M${x.toFixed(2)},${y.toFixed(2)}` : `L${x.toFixed(2)},${y.toFixed(2)}`))
    .join(' ');
}

/** Sparkline — small inline trend, no axes. */
function renderSparklines(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-sparkline');
  for (const el of els) {
    if (el.dataset.rendered === '1') continue;
    const values = parseSeries(el.dataset.points, 500);
    if (values.length < 2) continue;
    const w = 80;
    const h = 22;
    const pad = 2;
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;
    const points: Array<[number, number]> = values.map((v, i) => [
      pad + (i / (values.length - 1)) * (w - pad * 2),
      h - pad - ((v - min) / range) * (h - pad * 2),
    ]);
    const svg = svgEl<SVGSVGElement>('svg', { viewBox: `0 0 ${w} ${h}`, preserveAspectRatio: 'none' });
    const path = svgEl<SVGPathElement>('path', { class: 'ara-sparkline-path', d: pathFromPoints(points) });
    svg.appendChild(path);
    const last = points[points.length - 1];
    const dot = svgEl<SVGCircleElement>('circle', { class: 'ara-sparkline-end', cx: last[0], cy: last[1], r: 1.6 });
    svg.appendChild(dot);
    el.textContent = '';
    el.appendChild(svg);
    el.dataset.rendered = '1';
  }
}

/** Full line chart with axes. Supports up to 4 series via data-series-{1..4}.
 * Optional data-series-{N}-label, data-x-labels, data-y-unit, data-title,
 * data-subtitle. */
function renderLineCharts(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-line-chart');
  for (const el of els) {
    if (el.dataset.rendered === '1') continue;
    // data-series-N attrs use digit suffixes — DOMStringMap leaves the
    // hyphen in (data-series-1 does NOT map to dataset.series1), so read
    // them with getAttribute to sidestep the gotcha.
    const seriesList: Array<{ values: number[]; label: string }> = [];
    for (let i = 1; i <= 4; i++) {
      const v = parseSeries(el.getAttribute(`data-series-${i}`) || undefined, 1000);
      if (!v.length) continue;
      const label = el.getAttribute(`data-series-${i}-label`) || `Series ${i}`;
      seriesList.push({ values: v, label });
    }
    if (!seriesList.length) continue;
    const xLabels = parseLabels(el.dataset.xLabels, 20);
    const yUnit = el.dataset.yUnit || '';
    const title = el.dataset.title || '';
    const subtitle = el.dataset.subtitle || '';

    const W = 640;
    const H = 220;
    const ML = 44;
    const MR = 12;
    const MT = 10;
    const MB = 26;
    const innerW = W - ML - MR;
    const innerH = H - MT - MB;

    const allValues = seriesList.flatMap((s) => s.values);
    const min = Math.min(...allValues);
    const max = Math.max(...allValues);
    const pad = (max - min) * 0.08 || 1;
    const yMin = min - pad;
    const yMax = max + pad;
    const yRange = yMax - yMin || 1;
    const longest = Math.max(...seriesList.map((s) => s.values.length));

    const xFor = (i: number, total: number) => ML + (i / Math.max(1, total - 1)) * innerW;
    const yFor = (v: number) => MT + innerH - ((v - yMin) / yRange) * innerH;

    el.textContent = '';
    if (title) {
      const t = document.createElement('p');
      t.className = 'ara-line-chart-title';
      t.textContent = title;
      el.appendChild(t);
    }
    if (subtitle) {
      const s = document.createElement('p');
      s.className = 'ara-line-chart-subtitle';
      s.textContent = subtitle;
      el.appendChild(s);
    }
    const svg = svgEl<SVGSVGElement>('svg', { viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: 'xMidYMid meet' });

    // 5 horizontal gridlines + y-axis tick labels
    const Y_TICKS = 5;
    for (let i = 0; i <= Y_TICKS; i++) {
      const y = MT + (i / Y_TICKS) * innerH;
      const v = yMax - (i / Y_TICKS) * yRange;
      svg.appendChild(svgEl('line', { class: 'ara-chart-grid', x1: ML, y1: y, x2: W - MR, y2: y }));
      const lab = svgEl<SVGTextElement>('text', { class: 'ara-chart-tick-label', x: ML - 6, y: y + 3, 'text-anchor': 'end' });
      lab.textContent = `${yUnit}${v.toFixed(yRange < 5 ? 2 : 1)}`;
      svg.appendChild(lab);
    }

    // X-axis labels — sparse to avoid clutter
    if (xLabels.length) {
      const stepRender = Math.max(1, Math.ceil(xLabels.length / 8));
      for (let i = 0; i < xLabels.length; i += stepRender) {
        const x = xFor(i, xLabels.length);
        const lab = svgEl<SVGTextElement>('text', { class: 'ara-chart-tick-label', x, y: H - 8, 'text-anchor': 'middle' });
        lab.textContent = xLabels[i];
        svg.appendChild(lab);
      }
    }

    // Series paths
    seriesList.forEach((s, idx) => {
      const points: Array<[number, number]> = s.values.map((v, i) => [
        xFor(i, s.values.length === 1 ? 2 : s.values.length),
        yFor(v),
      ]);
      svg.appendChild(svgEl('path', { class: `ara-chart-series ara-chart-series-${idx + 1}`, d: pathFromPoints(points) }));
    });

    el.appendChild(svg);
    longest; // (silence unused — could be used for x-tick stride)

    // Legend
    if (seriesList.length > 1) {
      const legend = document.createElement('div');
      legend.className = 'ara-line-chart-legend';
      seriesList.forEach((s, idx) => {
        const item = document.createElement('span');
        item.className = `ara-chart-legend-item ara-chart-legend-item--${idx + 1}`;
        item.textContent = s.label;
        legend.appendChild(item);
      });
      el.appendChild(legend);
    }
    el.dataset.rendered = '1';
  }
}

/** Donut chart with side legend. Author writes data-labels + data-values. */
function renderDonuts(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-donut');
  for (const el of els) {
    if (el.dataset.rendered === '1') continue;
    const labels = parseLabels(el.dataset.labels, 8);
    const values = parseSeries(el.dataset.values, 8);
    if (!values.length || labels.length !== values.length) continue;
    const total = values.reduce((a, b) => a + b, 0);
    if (total <= 0) continue;

    const size = 200;
    const cx = size / 2;
    const cy = size / 2;
    const ro = 88;
    const ri = 56;
    const centerLabel = el.dataset.centerLabel || '';

    el.textContent = '';
    const svgWrap = document.createElement('div');
    const svg = svgEl<SVGSVGElement>('svg', { viewBox: `0 0 ${size} ${size}` });

    let acc = 0;
    values.forEach((v, idx) => {
      const start = (acc / total) * Math.PI * 2 - Math.PI / 2;
      acc += v;
      const end = (acc / total) * Math.PI * 2 - Math.PI / 2;
      const largeArc = end - start > Math.PI ? 1 : 0;
      const sx = cx + ro * Math.cos(start);
      const sy = cy + ro * Math.sin(start);
      const ex = cx + ro * Math.cos(end);
      const ey = cy + ro * Math.sin(end);
      const sxi = cx + ri * Math.cos(end);
      const syi = cy + ri * Math.sin(end);
      const exi = cx + ri * Math.cos(start);
      const eyi = cy + ri * Math.sin(start);
      const d =
        `M${sx.toFixed(2)},${sy.toFixed(2)}` +
        ` A${ro},${ro} 0 ${largeArc},1 ${ex.toFixed(2)},${ey.toFixed(2)}` +
        ` L${sxi.toFixed(2)},${syi.toFixed(2)}` +
        ` A${ri},${ri} 0 ${largeArc},0 ${exi.toFixed(2)},${eyi.toFixed(2)}` +
        ' Z';
      svg.appendChild(svgEl('path', { class: `ara-donut-slice ara-donut-slice--${(idx % 6) + 1}`, d }));
    });

    if (centerLabel) {
      const text = svgEl<SVGTextElement>('text', { class: 'ara-donut-center-label', x: cx, y: cy + 1, 'font-size': '18' });
      text.textContent = centerLabel;
      svg.appendChild(text);
    }
    svgWrap.appendChild(svg);
    el.appendChild(svgWrap);

    const legend = document.createElement('ul');
    legend.className = 'ara-donut-legend';
    labels.forEach((label, idx) => {
      const li = document.createElement('li');
      const swatch = document.createElement('span');
      swatch.className = `ara-donut-legend-swatch ara-donut-legend-swatch--${(idx % 6) + 1}`;
      const name = document.createElement('span');
      name.textContent = label;
      const value = document.createElement('span');
      value.className = 'ara-donut-legend-value';
      const pct = (values[idx] / total) * 100;
      value.textContent = `${pct.toFixed(1)}%`;
      li.appendChild(swatch);
      li.appendChild(name);
      li.appendChild(value);
      legend.appendChild(li);
    });
    el.appendChild(legend);
    el.dataset.rendered = '1';
  }
}

/** Two-period slopegraph. data-items, data-left-values, data-right-values,
 * data-left-label, data-right-label. Lines colored green/red by direction. */
function renderSlopes(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-slope');
  for (const el of els) {
    if (el.dataset.rendered === '1') continue;
    const items = parseLabels(el.dataset.items, 12);
    const leftValues = parseSeries(el.dataset.leftValues, 12);
    const rightValues = parseSeries(el.dataset.rightValues, 12);
    if (!items.length || items.length !== leftValues.length || items.length !== rightValues.length) continue;
    const leftLabel = el.dataset.leftLabel || 'Left';
    const rightLabel = el.dataset.rightLabel || 'Right';
    const unit = el.dataset.unit || '';

    const W = 640;
    const rowH = 26;
    const headerH = 30;
    const H = headerH + items.length * rowH + 20;
    const colL = 220;
    const colR = W - 220;

    const all = [...leftValues, ...rightValues];
    const min = Math.min(...all);
    const max = Math.max(...all);
    const range = max - min || 1;
    const yTop = headerH + 10;
    const yBot = H - 14;
    const yFor = (v: number) => yBot - ((v - min) / range) * (yBot - yTop);

    el.textContent = '';
    const svg = svgEl<SVGSVGElement>('svg', { viewBox: `0 0 ${W} ${H}` });

    // Headers
    const lh = svgEl<SVGTextElement>('text', { class: 'ara-slope-header', x: colL, y: 18, 'text-anchor': 'end' });
    lh.textContent = leftLabel;
    svg.appendChild(lh);
    const rh = svgEl<SVGTextElement>('text', { class: 'ara-slope-header', x: colR, y: 18, 'text-anchor': 'start' });
    rh.textContent = rightLabel;
    svg.appendChild(rh);

    items.forEach((name, i) => {
      const lv = leftValues[i];
      const rv = rightValues[i];
      const ly = yFor(lv);
      const ry = yFor(rv);
      const direction = rv > lv ? 'up' : rv < lv ? 'down' : 'flat';
      const line = svgEl<SVGLineElement>('line', {
        class: `ara-slope-line ${direction !== 'flat' ? `ara-slope-line--${direction}` : ''}`.trim(),
        x1: colL + 6,
        y1: ly,
        x2: colR - 6,
        y2: ry,
      });
      svg.appendChild(line);
      svg.appendChild(svgEl('circle', { class: 'ara-slope-dot', cx: colL + 6, cy: ly, r: 3 }));
      svg.appendChild(svgEl('circle', { class: 'ara-slope-dot', cx: colR - 6, cy: ry, r: 3 }));
      const lLabel = svgEl<SVGTextElement>('text', { class: 'ara-slope-label', x: colL - 8, y: ly + 4, 'text-anchor': 'end' });
      lLabel.textContent = `${name} ${unit}${lv}`;
      svg.appendChild(lLabel);
      const rLabel = svgEl<SVGTextElement>('text', { class: 'ara-slope-label', x: colR + 8, y: ry + 4, 'text-anchor': 'start' });
      rLabel.textContent = `${unit}${rv} ${name}`;
      svg.appendChild(rLabel);
    });

    el.appendChild(svg);
    el.dataset.rendered = '1';
  }
}

/** Wrap each bare `.ara-table` in a `.ara-table-wrap` div so wide tables
 * scroll horizontally on narrow viewports instead of pushing the page
 * wider than the viewport. Done in JS (not in the article's HTML) so
 * existing fragments don't need to be rewritten. Counterpart to wrapTables()
 * above, which handles markdown-rendered tables for non-research tabs. */
function wrapAraTables(root: HTMLElement): void {
  const tables = root.querySelectorAll<HTMLTableElement>('.ara-table');
  for (const t of tables) {
    const parent = t.parentElement;
    if (!parent || parent.classList.contains('ara-table-wrap')) continue;
    const wrap = document.createElement('div');
    wrap.className = 'ara-table-wrap';
    parent.insertBefore(wrap, t);
    wrap.appendChild(t);
  }
}

/** Read every `data-pct` and stamp `--ara-bar-pct: <n>%` on the element so
 * the bar / stacked-segment CSS picks up the value. Avoids inline style=
 * in authored articles. */
function applyBarFills(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('[data-pct]');
  for (const el of els) {
    const raw = el.dataset.pct;
    if (!raw) continue;
    const n = Number(raw);
    if (!Number.isFinite(n)) continue;
    const clamped = Math.max(0, Math.min(100, n));
    el.style.setProperty('--ara-bar-pct', clamped + '%');
  }
}

let tocScrollHandler: ((e: Event) => void) | null = null;

function hideResearchTOC(): void {
  const toc = document.getElementById('researchToc');
  if (toc) toc.hidden = true;
  document.body.classList.remove('has-toc');
  if (tocScrollHandler) {
    window.removeEventListener('scroll', tocScrollHandler);
    tocScrollHandler = null;
  }
}

function tocSlug(text: string): string {
  return text.toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48) || 'section';
}

/** Walk the article for `<h3 class="ara-h2">` (section heads) and
 * `<h4 class="ara-h3">` (subsections), assign IDs if missing, and build
 * a floating TOC in #researchToc. Sets up a passive scroll listener for
 * active-section highlighting. Hides if fewer than three sections. */
function renderResearchTOC(article: HTMLElement): void {
  const toc = document.getElementById('researchToc');
  const list = document.getElementById('researchTocList');
  if (!toc || !list) return;

  while (list.firstChild) list.removeChild(list.firstChild);

  const heads = Array.from(
    article.querySelectorAll<HTMLElement>(
      'h2.ara-h2, h3.ara-h2, h4.ara-h2, h2.ara-h3, h3.ara-h3, h4.ara-h3',
    ),
  );
  // Skip the article's display title — only section heads.
  if (heads.length < 3) {
    hideResearchTOC();
    return;
  }

  const links: HTMLAnchorElement[] = [];
  for (const h of heads) {
    if (!h.id) {
      const num = h.querySelector('.ara-h2-num');
      const rawText = (h.textContent || '').replace(num?.textContent || '', '').trim();
      h.id = tocSlug(rawText);
    }
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.className = 'ara-toc-link';
    a.href = '#' + h.id;
    if (h.classList.contains('ara-h3')) li.style.paddingLeft = '14px';
    const num = h.querySelector('.ara-h2-num');
    const restText = (h.textContent || '').replace(num?.textContent || '', '').trim();
    a.textContent = restText;
    // CSS clips overflow with ellipsis; surface the full title on hover.
    a.title = restText;
    a.dataset.target = h.id;
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const t = document.getElementById(a.dataset.target!);
      if (t) {
        // Push the fragment into the URL so users can copy/share the
        // section-level deep link directly from the address bar.
        history.pushState(null, '', '#' + a.dataset.target);
        t.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
    li.appendChild(a);
    list.appendChild(li);
    links.push(a);
  }
  toc.hidden = false;
  document.body.classList.add('has-toc');

  // Scroll-spy: the last heading whose top is above an offset is "current".
  if (tocScrollHandler) window.removeEventListener('scroll', tocScrollHandler);
  const OFFSET = 120;
  const onScroll = () => {
    let activeIndex = 0;
    for (let i = 0; i < heads.length; i++) {
      if (heads[i].getBoundingClientRect().top - OFFSET < 0) activeIndex = i;
      else break;
    }
    for (let i = 0; i < links.length; i++) {
      links[i].classList.toggle('active', i === activeIndex);
    }
  };
  tocScrollHandler = onScroll;
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/** Attach a small `#` anchor button to every section / subsection heading
 * that already has an id (renderResearchTOC assigns them). Clicking it
 * copies the deep link to the clipboard and updates the address bar so the
 * user can paste the URL anywhere. Cmd/Ctrl-click opens in a new tab via
 * the browser's default anchor behavior. */
function addSectionAnchors(article: HTMLElement): void {
  const heads = article.querySelectorAll<HTMLElement>(
    'h2.ara-h2, h3.ara-h2, h4.ara-h2, h2.ara-h3, h3.ara-h3, h4.ara-h3',
  );
  for (const h of heads) {
    if (!h.id || h.querySelector('.ara-anchor')) continue;
    const a = document.createElement('a');
    a.className = 'ara-anchor';
    a.href = '#' + h.id;
    a.title = 'Copy link to this section';
    a.setAttribute('aria-label', 'Copy link to this section');
    a.textContent = '#';
    h.appendChild(a);
    a.addEventListener('click', (e) => {
      // Honor open-in-new-tab modifiers — let the browser handle them.
      if (e.metaKey || e.ctrlKey || e.shiftKey || (e as MouseEvent).button === 1) return;
      e.preventDefault();
      history.pushState(null, '', '#' + h.id);
      h.scrollIntoView({ behavior: 'smooth', block: 'start' });
      const url = location.origin + location.pathname + '#' + h.id;
      copyTextToClipboard(url).then(() => {
        a.classList.add('ara-anchor--copied');
        window.setTimeout(() => a.classList.remove('ara-anchor--copied'), 1400);
      }).catch(() => {
        // Silent — the URL is still in the address bar, user can copy from there.
      });
    });
  }
}

/** Clipboard write with a non-secure-context fallback so this works on
 * localhost over plain HTTP and other edge environments. */
function copyTextToClipboard(text: string): Promise<void> {
  if (navigator.clipboard?.writeText) {
    return navigator.clipboard.writeText(text);
  }
  return new Promise((resolve, reject) => {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      resolve();
    } catch (err) {
      reject(err);
    } finally {
      ta.remove();
    }
  });
}

/** After the article renders, if the URL has a fragment, scroll to the
 * matching element. Runs in rAF so layout (chart sizing, isotype expansion,
 * table wrapping) has settled before we measure scroll positions. */
function scrollToHashIfPresent(): void {
  if (!location.hash) return;
  const id = decodeURIComponent(location.hash.slice(1));
  if (!id) return;
  const t = document.getElementById(id);
  if (!t) return;
  requestAnimationFrame(() => {
    t.scrollIntoView({ behavior: 'auto', block: 'start' });
  });
}

function renderResearchStandalone(row: GenResearchRow): void {
  const created = new Date(row.created_at);
  const rel = isNaN(created.getTime()) ? '' : timeAgo(created);
  const src = `${DATA_BASE}/generative/${row.file}`;
  // Iframe sandbox: `allow-scripts` lets the report's own TOC/scroll-spy
  // run, but WITHOUT `allow-same-origin` the script runs in a null origin
  // and cannot read parent state, cookies, or make same-origin requests.
  setSafeContent(
    content,
    [
      '<div class="content-card gen-research-doc gen-research-standalone">',
      '  <div class="content-card-header">',
      '    <div class="content-card-title">' + escapeHtml(row.title) + '</div>',
      '  </div>',
      '  <div class="gen-research-doc-meta">',
      '    <button class="gen-research-back" data-research-back>&lsaquo; All articles</button>',
      '    <span class="gen-research-model">' + escapeHtml(row.model) + '</span>',
      rel ? '    <span class="gen-research-time">' + escapeHtml(rel) + '</span>' : '',
      '    <a class="gen-research-fullscreen" href="' + escapeHtml(src) + '" target="_blank" rel="noopener noreferrer">Open full ↗</a>',
      '  </div>',
      '  <iframe class="gen-research-iframe" src="' + escapeHtml(src) + '" sandbox="allow-scripts" loading="lazy" title="' + escapeHtml(row.title) + '"></iframe>',
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

  // Hide the floating TOC unconditionally; renderResearchDoc shows it
  // again when it has enough sections to be useful.
  hideResearchTOC();

  updateRoute();
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
        } else if (row.kind === 'standalone') {
          // Standalone docs render as an iframe; no body fetch needed.
          researchDocCache = null;
          renderResearchStandalone(row);
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
      // Fetch digest + front page in parallel — the front page goes
      // into the left column of the two-column today layout on desktop.
      const [digestResult, fpResult] = await Promise.all([
        withTimeout(fetchDigest(dateStr, controller.signal), LOAD_TIMEOUT_MS, controller),
        fetchFrontPage(dateStr, controller.signal),
      ]);
      if (requestId !== loadRequestId) return;
      // Resolve which front-page URL to pass (today's, or the most-recent fallback).
      let frontPage: { url: string; fallback: string | null } | null = null;
      if (fpResult) {
        frontPage = { url: fpResult, fallback: null };
      } else {
        const fp = findMostRecentAvailable('frontpage', dateStr);
        if (fp && fp !== dateStr) {
          frontPage = {
            url: `${DATA_BASE}/front-page/${fp}-front-page.png`,
            fallback: fp,
          };
        }
      }
      if (digestResult === 'timeout') {
        showError('Loading timed out', 'Network may be slow. Click to retry.');
      } else if (digestResult) {
        renderToday(digestResult, frontPage);
      } else {
        // Digest missing — fall back to most recent
        const fallback = findMostRecentAvailable('today', dateStr);
        if (fallback && fallback !== dateStr) {
          const fallbackMd = await fetchDigest(fallback, controller.signal);
          if (fallbackMd) {
            renderToday(fallbackMd, frontPage);
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
  if (target.closest('[data-research-pdf]')) {
    // Browser handles the rest: print stylesheet hides chrome,
    // user picks "Save as PDF" in the system dialog.
    window.print();
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
applyRoute();
// applyRoute() may have mutated activeTab to anything in Tab; TS won't see
// that across the function boundary, so we widen the read explicitly.
const currentTab: Tab = activeTab as Tab;
document.body.classList.toggle('tab-research', currentTab === 'research');
if (currentTab !== 'research') {
  probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
}
load();

// Back/forward button — pathname-based router uses popstate, not hashchange.
// Hash-only changes (anchor click within an article) just scroll; route
// changes re-fetch via load() and fire a SPA page_view to GA.
window.addEventListener('popstate', () => {
  const newPathname = location.pathname;
  if (newPathname === lastAppliedPathname) {
    // Same article, different anchor — just scroll to the new fragment.
    scrollToHashIfPresent();
    return;
  }
  lastAppliedPathname = newPathname;
  if (applyRoute()) {
    load();
    trackPageView();
  }
});
