import './style.css';
import { marked, Marked } from 'marked';
import type { Tokens, TokenizerThis } from 'marked';
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
type Tab = 'today' | 'twitter' | 'models' | 'frontpage' | 'research' | 'wiki';
// Tabs that route by date (calendar-driven). research + wiki are slug-driven
// (or index views) and are excluded — mirror the research precedent.
type DateTab = Exclude<Tab, 'research' | 'wiki'>;
type GenResearchKind = 'fragment' | 'standalone';
type ResearchLanguage = 'en' | 'ko';
type GenResearchTranslation = {
  file: string;
  audio_file?: string;
  kind?: GenResearchKind;
  language?: ResearchLanguage | string;
  title?: string;
  model?: string;
  created_at?: string;
  source?: string;
  prompt?: string;
  tags?: string[];
};
type GenResearchRow = {
  slug: string;
  file: string;
  audio_file?: string;
  kind?: GenResearchKind;  // optional for back-compat; undefined = fragment
  language?: ResearchLanguage | string;
  translations?: Record<string, GenResearchTranslation>;
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
type TwitterStory = {
  rank: string;
  title: string;
  body: string;
  links: string[];
  handles: string[];
};

// Model-release ticket — see docs/model-tickets.md for the contract.
type TicketStatus = 'rumored' | 'in-testing' | 'confirmed' | 'released' | 'closed';
type TicketVerification = 'confirmed' | 'partial' | 'unverified';
type TicketHistoryEntry = { ts: string; change: string };
type Ticket = {
  slug: string;
  title: string;
  company: string;
  model: string | null;
  status: TicketStatus;
  status_note: string | null;
  expected: string | null;
  labels: string[];
  verification: TicketVerification;
  sources: string[];
  created_at: string;
  updated_at: string;
  closed_at: string | null;
  closed_reason: string | null;
  history: TicketHistoryEntry[];
  body: string;
};
type TicketIndex = { tickets: Ticket[] };

let currentDate = new Date();
let searchTerm = '';
let activeTab: Tab = 'today';
let selectedSlug: string | null = null;
let activeLanguage: ResearchLanguage = loadStoredLanguage();
let calendarMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
const availabilityCache = new Map<string, Set<string>>();
let loadRequestId = 0;
let activeLoadController: AbortController | null = null;
let searchDebounceId: number | null = null;
let manifest: Manifest | null = null;
let manifestPromise: Promise<Manifest | null> | null = null;
// Cache the last-fetched research doc body so search-as-you-type doesn't refetch.
let researchDocCache: { slug: string; language: ResearchLanguage; body: string } | null = null;
// Cache the tickets index — fetched once per session on first models-tab visit.
let ticketsCache: Ticket[] | null = null;
let ticketsPromise: Promise<Ticket[] | null> | null = null;
// Which ticket is expanded (showing body + history). Null = grid view.
let expandedTicketSlug: string | null = null;
// Filter state for the tickets grid.
const ticketFilters = { status: 'all', company: 'all' };
const LOAD_TIMEOUT_MS = 12000;
const SPEECH_CHUNK_MAX_CHARS = 2600;
const RESEARCH_AUDIO_PLAYBACK_ENABLED = false;

type ResearchAudioStatus = 'idle' | 'loading' | 'playing' | 'paused';
type ResearchAudioState = {
  key: string | null;
  status: ResearchAudioStatus;
  chunks: string[];
  index: number;
  utterance: SpeechSynthesisUtterance | null;
};

const researchAudioState: ResearchAudioState = {
  key: null,
  status: 'idle',
  chunks: [],
  index: 0,
  utterance: null,
};

// ── DOM refs ──────────────────────────────────────────
const content = document.getElementById('content')!;
const calendarEl = document.getElementById('calendar')!;
const searchInput = document.getElementById('searchInput') as HTMLInputElement;
const searchCountEl = document.getElementById('searchCount')!;
const languageSwitch = document.getElementById('languageSwitch')!;

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
  if (activeTab === 'wiki') {
    return selectedSlug ? '/wiki/' + selectedSlug : '/wiki';
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
  // Wiki slugs are tighter than research's: ^[a-z0-9]+(-[a-z0-9]+)*$ per the
  // index contract. Gate at the route level so a crafted /wiki/FOO.evil never
  // reaches the resolver lookup.
  const wikiMatch = trimmed.match(/^wiki(?:\/([a-z0-9-]+))?$/);
  if (wikiMatch) {
    activeTab = 'wiki';
    selectedSlug = wikiMatch[1] || null;
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
  // Models tab shows the ticket grid (no date routing); the calendar
  // would just be dead UI on this tab. Same toggle pattern as research.
  document.body.classList.toggle('tab-models', activeTab === 'models');
  // Wiki is slug/index-driven, not date-driven — same calendar-hiding
  // toggle as research/models.
  document.body.classList.toggle('tab-wiki', activeTab === 'wiki');
}

// ── Helpers ───────────────────────────────────────────
function loadStoredLanguage(): ResearchLanguage {
  try {
    return localStorage.getItem('ara-language') === 'ko' ? 'ko' : 'en';
  } catch {
    return 'en';
  }
}

function storeLanguage(language: ResearchLanguage): void {
  try {
    localStorage.setItem('ara-language', language);
  } catch {
    // Ignore storage failures in private mode or locked-down browsers.
  }
}

function researchVariant(row: GenResearchRow, language: ResearchLanguage): GenResearchRow {
  if (language === 'en') return row;
  const translation = row.translations?.[language];
  if (!translation?.file) return row;
  return {
    ...row,
    ...translation,
    slug: row.slug,
    file: translation.file,
    kind: translation.kind || row.kind,
    language,
    title: translation.title || row.title,
    model: translation.model || row.model,
    created_at: translation.created_at || row.created_at,
    source: translation.source || row.source,
    prompt: translation.prompt || row.prompt,
    tags: translation.tags || row.tags,
    translations: row.translations,
  };
}

function hasResearchLanguage(row: GenResearchRow | null, language: ResearchLanguage): boolean {
  if (language === 'en') return true;
  return Boolean(row?.translations?.[language]?.file);
}

function syncLanguageUi(row: GenResearchRow | null = null): void {
  languageSwitch.querySelectorAll<HTMLButtonElement>('[data-language]').forEach((btn) => {
    const language = btn.dataset.language as ResearchLanguage;
    const available = !row || hasResearchLanguage(row, language);
    btn.classList.toggle('active', language === activeLanguage);
    btn.classList.toggle('unavailable', !available);
    btn.setAttribute('aria-pressed', String(language === activeLanguage));
    btn.title = available
      ? (language === 'ko' ? 'Show Korean' : 'Show English')
      : 'Korean version has not been published for this article';
  });
}

function languageFallbackNote(row: GenResearchRow): string {
  if (activeLanguage !== 'ko' || hasResearchLanguage(row, 'ko')) return '';
  return '<div class="gen-research-language-note">Korean version has not been published for this article yet.</div>';
}

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
    ADD_TAGS: ['mark', 'article', 'figure', 'figcaption', 'iframe', 'audio'],
    ADD_ATTR: ['data-slug', 'data-pct', 'data-filter-status', 'data-filter-company', 'data-has-audio-file', 'sandbox', 'loading', 'allow', 'decoding', 'referrerpolicy', 'controls', 'preload', 'src'],
  });
  el.insertAdjacentHTML('beforeend', clean);
}

// ── Research audio playback ───────────────────────────
function isSpeechSupported(): boolean {
  return 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
}

function currentResearchAudioKey(): string {
  return `${selectedSlug || ''}:${activeLanguage}`;
}

function researchAudioUrl(row: GenResearchRow): string | null {
  return row.audio_file ? `${DATA_BASE}/${row.audio_file}` : null;
}

function researchAudioControlsHtml(row: GenResearchRow): string {
  if (!RESEARCH_AUDIO_PLAYBACK_ENABLED) return '';
  const unsupported = !isSpeechSupported();
  const fileUrl = researchAudioUrl(row);
  if (fileUrl) {
    return [
      '<span class="gen-research-audio-controls has-file" aria-label="Article audio controls">',
      '  <audio class="gen-research-audio-file" preload="metadata" src="' + escapeHtml(fileUrl) + '">Your browser does not support the audio element.</audio>',
      '  <button class="gen-research-file-audio" data-research-file-audio-toggle aria-pressed="false" title="Play article audio">',
      '    <span class="gen-research-file-audio-icon" aria-hidden="true"></span>',
      '    <span class="gen-research-file-audio-label" data-research-file-audio-label>Listen</span>',
      '    <span class="gen-research-file-audio-progress" data-research-file-audio-progress aria-hidden="true"></span>',
      '    <span class="gen-research-file-audio-time" data-research-file-audio-time>--:--</span>',
      '  </button>',
      '</span>',
    ].join('\n');
  }
  return [
    '<span class="gen-research-audio-controls" aria-label="Article read-aloud controls">',
    '  <button class="gen-research-audio" data-research-audio-toggle data-has-audio-file="' + (fileUrl ? 'true' : 'false') + '" aria-pressed="false"' +
      (unsupported ? ' disabled title="Read-aloud is not supported in this browser"' : ' title="Play this article with browser read-aloud"') +
      '>',
    '    <span class="gen-research-audio-icon" aria-hidden="true"></span>',
    '    <span data-research-audio-label>' + (unsupported ? 'Audio unavailable' : 'Listen') + '</span>',
    '  </button>',
    '  <button class="gen-research-audio-stop" data-research-audio-stop hidden title="Stop article audio">Stop</button>',
    '</span>',
  ].join('\n');
}

function formatAudioTime(seconds: number): string {
  if (!Number.isFinite(seconds) || seconds < 0) return '--:--';
  const whole = Math.floor(seconds);
  const minutes = Math.floor(whole / 60);
  const secs = whole % 60;
  return `${minutes}:${String(secs).padStart(2, '0')}`;
}

function updateResearchFileAudioUi(): void {
  const audio = content.querySelector<HTMLAudioElement>('.gen-research-audio-file');
  const toggle = content.querySelector<HTMLButtonElement>('[data-research-file-audio-toggle]');
  if (!audio || !toggle) return;
  const label = content.querySelector<HTMLElement>('[data-research-file-audio-label]');
  const time = content.querySelector<HTMLElement>('[data-research-file-audio-time]');
  const progress = content.querySelector<HTMLElement>('[data-research-file-audio-progress]');
  const duration = Number.isFinite(audio.duration) ? audio.duration : 0;
  const pct = duration > 0 ? Math.min(100, Math.max(0, (audio.currentTime / duration) * 100)) : 0;
  toggle.classList.toggle('is-playing', !audio.paused && !audio.ended);
  toggle.setAttribute('aria-pressed', String(!audio.paused && !audio.ended));
  if (label) label.textContent = audio.paused || audio.ended ? 'Listen' : 'Pause';
  if (time) time.textContent = duration > 0 ? `${formatAudioTime(audio.currentTime)} / ${formatAudioTime(duration)}` : '--:--';
  if (progress) progress.style.setProperty('--audio-progress', `${pct}%`);
}

function bindResearchFileAudioUi(): void {
  const audio = content.querySelector<HTMLAudioElement>('.gen-research-audio-file');
  if (!audio || audio.dataset.bound === 'true') return;
  audio.dataset.bound = 'true';
  audio.addEventListener('loadedmetadata', updateResearchFileAudioUi);
  audio.addEventListener('timeupdate', updateResearchFileAudioUi);
  audio.addEventListener('play', updateResearchFileAudioUi);
  audio.addEventListener('pause', updateResearchFileAudioUi);
  audio.addEventListener('ended', updateResearchFileAudioUi);
  audio.addEventListener('error', () => {
    const label = content.querySelector<HTMLElement>('[data-research-file-audio-label]');
    if (label) label.textContent = 'Unavailable';
  });
  updateResearchFileAudioUi();
}

function updateResearchAudioUi(): void {
  bindResearchFileAudioUi();
  const key = currentResearchAudioKey();
  const toggle = content.querySelector<HTMLButtonElement>('[data-research-audio-toggle]');
  const stop = content.querySelector<HTMLButtonElement>('[data-research-audio-stop]');
  const label = content.querySelector<HTMLElement>('[data-research-audio-label]');
  if (!toggle || !label) return;

  if (!isSpeechSupported()) {
    toggle.disabled = true;
    toggle.classList.remove('is-playing', 'is-paused', 'is-loading');
    toggle.setAttribute('aria-pressed', 'false');
    label.textContent = 'Audio unavailable';
    if (stop) stop.hidden = true;
    return;
  }

  const isCurrent = researchAudioState.key === key;
  const status: ResearchAudioStatus = isCurrent ? researchAudioState.status : 'idle';
  toggle.disabled = status === 'loading';
  toggle.classList.toggle('is-loading', status === 'loading');
  toggle.classList.toggle('is-playing', status === 'playing');
  toggle.classList.toggle('is-paused', status === 'paused');
  toggle.setAttribute('aria-pressed', String(status === 'playing'));
  label.textContent =
    status === 'loading' ? 'Preparing' :
    status === 'playing' ? 'Pause' :
    status === 'paused' ? 'Resume' :
    'Listen';
  if (stop) stop.hidden = !(status === 'playing' || status === 'paused' || status === 'loading');
}

async function toggleResearchFileAudio(): Promise<void> {
  const audio = content.querySelector<HTMLAudioElement>('.gen-research-audio-file');
  if (!audio) return;
  if (audio.paused || audio.ended) {
    stopResearchAudio();
    try {
      await audio.play();
    } catch {
      const label = content.querySelector<HTMLElement>('[data-research-file-audio-label]');
      if (label) label.textContent = 'Unavailable';
    }
  } else {
    audio.pause();
  }
  updateResearchFileAudioUi();
}

function stopResearchAudio(): void {
  if (isSpeechSupported()) {
    window.speechSynthesis.cancel();
  }
  researchAudioState.key = null;
  researchAudioState.status = 'idle';
  researchAudioState.chunks = [];
  researchAudioState.index = 0;
  researchAudioState.utterance = null;
  updateResearchAudioUi();
}

function normalizeSpeechText(text: string): string {
  return text
    .replace(/\s+/g, ' ')
    .replace(/\s+([,.;:!?])/g, '$1')
    .trim();
}

function readableTextFromElement(root: Element, title: string): string {
  const clone = root.cloneNode(true) as HTMLElement;
  clone
    .querySelectorAll('script, style, noscript, svg, iframe, button, nav, .ara-toc, .gen-research-doc-meta')
    .forEach((el) => el.remove());
  const bodyText = normalizeSpeechText(clone.textContent || '');
  if (!bodyText) return normalizeSpeechText(title);
  if (bodyText.toLowerCase().startsWith(title.toLowerCase())) return bodyText;
  return normalizeSpeechText(`${title}. ${bodyText}`);
}

function readableTextFromHtml(html: string, title: string): string {
  const parsed = new DOMParser().parseFromString(html, 'text/html');
  const article = parsed.querySelector('article.ara-doc') || parsed.querySelector('article') || parsed.body;
  return readableTextFromElement(article, title);
}

function splitSpeechText(text: string): string[] {
  const normalized = normalizeSpeechText(text);
  if (!normalized) return [];
  const sentences = normalized.match(/[^.!?]+[.!?]+["')\]]*|[^.!?]+$/g) || [normalized];
  const chunks: string[] = [];
  let current = '';

  const pushCurrent = () => {
    const trimmed = current.trim();
    if (trimmed) chunks.push(trimmed);
    current = '';
  };

  for (const sentence of sentences) {
    const next = sentence.trim();
    if (!next) continue;
    if (next.length > SPEECH_CHUNK_MAX_CHARS) {
      pushCurrent();
      const words = next.split(/\s+/);
      let longChunk = '';
      for (const word of words) {
        if ((longChunk + ' ' + word).trim().length > SPEECH_CHUNK_MAX_CHARS) {
          if (longChunk.trim()) chunks.push(longChunk.trim());
          longChunk = word;
        } else {
          longChunk = `${longChunk} ${word}`.trim();
        }
      }
      if (longChunk.trim()) chunks.push(longChunk.trim());
      continue;
    }
    if ((current + ' ' + next).trim().length > SPEECH_CHUNK_MAX_CHARS) {
      pushCurrent();
    }
    current = `${current} ${next}`.trim();
  }
  pushCurrent();
  return chunks;
}

async function resolveCurrentResearchAudioText(): Promise<string | null> {
  if (!selectedSlug) return null;
  const row = findResearchRow(selectedSlug);
  if (!row) return null;
  const variant = researchVariant(row, activeLanguage);
  const title = variant.title || row.title;
  const renderedArticle = content.querySelector('article.ara-doc');
  if (renderedArticle) {
    return readableTextFromElement(renderedArticle, title);
  }

  const controller = new AbortController();
  const html = await withTimeout(fetchResearchDoc(variant, controller.signal), LOAD_TIMEOUT_MS, controller);
  return html && html !== 'timeout' ? readableTextFromHtml(html, title) : null;
}

function speakCurrentResearchChunk(): void {
  if (!isSpeechSupported()) return;
  const key = researchAudioState.key;
  if (!key || researchAudioState.index >= researchAudioState.chunks.length) {
    stopResearchAudio();
    return;
  }

  const utterance = new SpeechSynthesisUtterance(researchAudioState.chunks[researchAudioState.index]);
  utterance.lang = activeLanguage === 'ko' ? 'ko-KR' : 'en-US';
  researchAudioState.utterance = utterance;
  researchAudioState.status = 'playing';
  updateResearchAudioUi();

  utterance.onend = () => {
    if (
      researchAudioState.key !== key ||
      researchAudioState.utterance !== utterance ||
      researchAudioState.status !== 'playing'
    ) {
      return;
    }
    researchAudioState.index += 1;
    speakCurrentResearchChunk();
  };
  utterance.onerror = () => {
    if (researchAudioState.key === key && researchAudioState.utterance === utterance) {
      stopResearchAudio();
    }
  };
  window.speechSynthesis.speak(utterance);
}

async function toggleResearchAudio(): Promise<void> {
  if (!isSpeechSupported() || !selectedSlug) return;
  const key = currentResearchAudioKey();
  if (researchAudioState.key === key && researchAudioState.status === 'playing') {
    window.speechSynthesis.pause();
    researchAudioState.status = 'paused';
    updateResearchAudioUi();
    return;
  }
  if (researchAudioState.key === key && researchAudioState.status === 'paused') {
    window.speechSynthesis.resume();
    researchAudioState.status = 'playing';
    updateResearchAudioUi();
    return;
  }
  if (researchAudioState.key === key && researchAudioState.status === 'loading') return;

  stopResearchAudio();
  researchAudioState.key = key;
  researchAudioState.status = 'loading';
  updateResearchAudioUi();

  const text = await resolveCurrentResearchAudioText();
  if (researchAudioState.key !== key || researchAudioState.status !== 'loading') return;
  const chunks = splitSpeechText(text || '');
  if (chunks.length === 0) {
    stopResearchAudio();
    return;
  }
  researchAudioState.chunks = chunks;
  researchAudioState.index = 0;
  speakCurrentResearchChunk();
}

// ── Fetch ─────────────────────────────────────────────
function isViteAppShell(text: string): boolean {
  const head = text.slice(0, 1000).trim().toLowerCase();
  return (
    head.startsWith('<!doctype html') &&
    (head.includes('script type="module" src="/@vite/client"') || head.includes('<title>ai research'))
  );
}

async function fetchMarkdownReport(url: string, signal: AbortSignal): Promise<string | null> {
  try {
    const resp = await fetch(url, { signal, cache: 'no-cache' });
    if (!resp.ok) return null;
    const text = await resp.text();
    return isViteAppShell(text) ? null : text;
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') return null;
    return null;
  }
}

async function fetchTwitter(dateStr: string, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/twitter/${dateStr}.md`;
  return fetchMarkdownReport(url, signal);
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

async function fetchDigest(dateStr: string, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/digest/${dateStr}-digest.md`;
  return fetchMarkdownReport(url, signal);
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
    : activeTab === 'wiki'
    ? (selectedSlug ? 'Loading wiki page\u2026' : 'Loading wiki\u2026')
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

function stripMarkdown(md: string): string {
  return md
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/!\[[^\]]*]\([^)]+\)/g, ' ')
    .replace(/\[([^\]]+)]\([^)]+\)/g, '$1')
    .replace(/https?:\/\/\S+/g, ' ')
    .replace(/[#>*_`~|]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function truncateText(text: string, max = 360): string {
  if (text.length <= max) return text;
  const sliced = text.slice(0, max).replace(/\s+\S*$/, '').trim();
  return sliced + '...';
}

function cleanPublicLeadText(text: string): string {
  return text
    .replace(/\([^)]*\b(?:verified|curl|re-verified|source checks?|multi-source primary-source confirmed)[^)]*\)/gi, '')
    .replace(/\b(?:verified|re-verified|confirmed)\s+(?:via|by)\s+(?:curl|source checks?|snapshot)[^.;—]*[.;—]?\s*/gi, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function isSourceMethodLead(text: string): boolean {
  return /\b(?:verified|curl|source checks?|originating .*source|confirmed via|post body|press-release teaser|raw URL|snapshot)\b/i.test(text);
}

function highlightPlainText(text: string): string {
  const escapedText = escapeHtml(text);
  if (!searchTerm) return escapedText;
  const escaped = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const re = new RegExp('(' + escaped + ')', 'gi');
  return escapedText.replace(re, '<mark>$1</mark>');
}

function extractUrls(md: string): string[] {
  const urls = new Set<string>();
  const re = /https?:\/\/[^\s)>\]]+/g;
  let match: RegExpExecArray | null;
  while ((match = re.exec(md))) {
    urls.add(match[0].replace(/[.,;:]+$/, ''));
  }
  return Array.from(urls);
}

function extractHandles(md: string, limit = 12): string[] {
  const handles = new Set<string>();
  const re = /(?<!\w)@([A-Za-z0-9_]{2,20})/g;
  let match: RegExpExecArray | null;
  while ((match = re.exec(md)) && handles.size < limit) {
    handles.add('@' + match[1]);
  }
  return Array.from(handles);
}

function hostnameOf(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch {
    return url;
  }
}

function renderTweetAgoFromUrl(url: string): string {
  const match = url.match(/(?:x|twitter)\.com\/[^/]+\/status\/(\d+)/);
  if (!match) return '';
  const date = snowflakeToDate(match[1]);
  return date ? '<span class="tweet-ago">' + escapeHtml(timeAgo(date)) + '</span>' : '';
}

function sourceLabel(url: string): string {
  try {
    const u = new URL(url);
    const host = u.hostname.replace(/^www\./, '');
    const pathParts = u.pathname.split('/').filter(Boolean);
    if ((host === 'x.com' || host.endsWith('.twitter.com') || host === 'twitter.com') && pathParts[0]) {
      return '@' + pathParts[0];
    }
    return host;
  } catch {
    return url;
  }
}

function renderSourceChips(urls: string[], limit = 8): string {
  const html = urls.slice(0, limit).map((url) => {
    return (
      '<a class="twitter-source-chip" href="' + escapeHtml(url) + '" target="_blank" rel="noopener noreferrer">' +
        escapeHtml(sourceLabel(url)) +
        renderTweetAgoFromUrl(url) +
      '</a>'
    );
  }).join('');
  const extra = urls.length > limit ? '<span class="twitter-source-more">+' + (urls.length - limit) + '</span>' : '';
  return html + extra;
}

function renderHandleChips(handles: string[], limit = 10): string {
  return handles.slice(0, limit).map((handle) => {
    return '<span class="twitter-handle-chip">' + escapeHtml(handle) + '</span>';
  }).join('');
}

function twitterMarkdownToHtml(md: string): string {
  let html = marked.parse(md) as string;
  html = wrapTables(html);
  html = html.replace(
    /href="https?:\/\/(?:x|twitter)\.com\/\w+\/status\/(\d+)"[^>]*>([^<]+)<\/a>/g,
    (match, tweetId: string) => {
      const date = snowflakeToDate(tweetId);
      if (!date) return match;
      return match + '<span class="tweet-ago">' + escapeHtml(timeAgo(date)) + '</span>';
    },
  );
  html = html.replace(/(?<!\w)(@\w+)/g, '<span class="handle">$1</span>');
  return html;
}

// ── Wiki (LLM Wiki) ───────────────────────────────────
//
// The wiki is a compounding knowledge base under research/wiki/. The Python
// side (scripts/build_wiki_index.py) emits a committed research/wiki/index.json
// — the pinned contract. We CONSUME it: never re-parse pages for the graph,
// never reimplement wikilink parsing. The only JS-side parsing is (1) stripping
// YAML frontmatter off a page body and (2) the marked inline extension that
// turns `[[target]]` into a link, resolving via the index `resolver`.

type WikiType = 'entity' | 'concept' | 'theme';

type WikiPage = {
  slug: string;
  title: string;
  type: WikiType | string;
  tags: string[];
  summary: string;
  created_at: string;
  updated_at: string;
  file: string;            // relative to research/wiki/, e.g. "entities/nebius.md"
  aliases: string[];
  outbound: string[];      // slugs
  inbound: string[];       // slugs
};

type WikiLogEntry = { date: string; op: string; summary: string };

type WikiIndex = {
  pages: WikiPage[];
  resolver: Record<string, string>;  // lowercased slug-or-alias → canonical slug
  recent_log: WikiLogEntry[];        // newest first
};

// One-time fetch cache for the index, plus a derived slug→page Map so backlink
// rendering is O(n) not O(n^2) (advisor note 5).
let wikiIndexCache: WikiIndex | null = null;
let wikiPageMap: Map<string, WikiPage> = new Map();
// Body cache keyed by slug so re-visiting a page doesn't refetch.
const wikiBodyCache = new Map<string, string>();

async function loadWikiIndex(signal: AbortSignal): Promise<WikiIndex | null> {
  if (wikiIndexCache) return wikiIndexCache;
  try {
    const resp = await fetch(`${DATA_BASE}/wiki/index.json`, { signal });
    if (!resp.ok) return null;
    const raw = (await resp.json()) as Partial<WikiIndex>;
    const idx: WikiIndex = {
      pages: Array.isArray(raw.pages) ? (raw.pages as WikiPage[]) : [],
      resolver: raw.resolver && typeof raw.resolver === 'object' ? raw.resolver : {},
      recent_log: Array.isArray(raw.recent_log) ? (raw.recent_log as WikiLogEntry[]) : [],
    };
    wikiIndexCache = idx;
    wikiPageMap = new Map(idx.pages.map((p) => [p.slug, p]));
    return idx;
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') return null;
    return null;
  }
}

/** Strip leading YAML frontmatter, matching the validator/prebuild semantics
 * EXACTLY: if the text starts with `---\n`, drop everything through the FIRST
 * `\n---\n`, then trim leading newlines. Otherwise use as-is. Deliberately not
 * a greedy regex — a casual /^---[\s\S]*?---/ would mis-handle a body that
 * happens to contain a `---` horizontal rule. */
function stripWikiFrontmatter(text: string): string {
  if (!text.startsWith('---\n')) return text;
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) return text; // no closing fence — treat whole thing as body
  return text.slice(end + 5).replace(/^\n+/, '');
}

/** Resolve a raw wikilink target against the current index resolver.
 * Returns the canonical slug, or null if unresolved (→ broken link). */
function resolveWikiTarget(target: string): string | null {
  const resolver = wikiIndexCache?.resolver;
  if (!resolver) return null;
  const slug = resolver[target.trim().toLowerCase()];
  return slug || null;
}

// Scoped marked instance for wiki pages. We do NOT touch the global `marked`
// (used by twitter/research/tickets) — the inline extension is registered only
// here, so `[[...]]` is wiki-only behavior.
//
// Why an inline tokenizer guarantees fenced-code safety (stress-test #1):
// marked block-lexes first (fenced/indented code -> `code` tokens whose text is
// emitted as escaped literal text, never re-fed to inline tokenizers) and
// inline-lexes the rest (backtick spans -> `codespan` tokens, also not
// re-tokenized). An inline extension only ever sees inline-walkable text, so a
// `[[x]]` inside a fenced block or a code span is left literal by construction
// — it is never a regex pass over the produced HTML.
const WIKILINK_RE = /^\[\[([^\]|\n]+?)(?:\|([^\]\n]+?))?\]\]/;
const wikiMarked = new Marked({
  gfm: true,
  breaks: false,
  extensions: [
    {
      name: 'wikilink',
      level: 'inline',
      // Jump straight to the next `[[` (perf + idiom); without this marked
      // walks every character looking for a custom-token start.
      start(this: TokenizerThis, src: string) {
        return src.indexOf('[[');
      },
      // `src` is already sliced to the current match position, so anchor with ^.
      // Capture: [[target]] or [[target|Label]]. Disallow ] | and newline in
      // target; disallow ] and newline in label.
      tokenizer(this: TokenizerThis, src: string) {
        const m = src.match(WIKILINK_RE);
        if (!m) return undefined;
        return {
          type: 'wikilink',
          raw: m[0],
          target: m[1].trim(),
          label: (m[2] || '').trim(),
        } as Tokens.Generic;
      },
      renderer(token: Tokens.Generic) {
        const target = String(token.target ?? '');
        const label = String(token.label ?? '');
        const slug = resolveWikiTarget(target);
        if (slug) {
          const page = wikiPageMap.get(slug);
          const text = label || page?.title || slug;
          return (
            '<a href="/wiki/' + escapeHtml(slug) + '" class="wikilink" ' +
            'data-wiki-slug="' + escapeHtml(slug) + '">' + escapeHtml(text) + '</a>'
          );
        }
        // Unresolved -> render visibly broken (NOT a dead <a> to an empty page).
        const text = label || target;
        return (
          '<span class="wikilink-broken" title="unresolved: ' +
          escapeHtml(target) + '">' + escapeHtml(text) + '</span>'
        );
      },
    },
  ],
});

/** Render a wiki page body (frontmatter already stripped) to HTML via the
 * scoped wiki marked instance (so [[wikilinks]] resolve through the index). */
function wikiMarkdownToHtml(md: string): string {
  return wikiMarked.parse(md) as string;
}

/** Stricter sanitizer for LLM-authored (semi-trusted) wiki pages. Unlike the
 * global setSafeContent — which deliberately WIDENS the default allowlist to
 * permit iframe/SVG for sandboxed standalone docs — this LOCKS DOWN: forbids
 * iframe/script/style/svg/math/form/input/button and inline style=, while
 * keeping data-wiki-slug (+ href/class/title) on anchors/spans for click-routing
 * and broken-link tooltips. */
function setSafeWikiContent(el: HTMLElement, rawHtml: string): void {
  while (el.firstChild) el.removeChild(el.firstChild);
  const clean = DOMPurify.sanitize(rawHtml, {
    USE_PROFILES: { html: true },
    ADD_ATTR: ['data-wiki-slug'],
    FORBID_TAGS: ['style', 'iframe', 'script', 'svg', 'math', 'form', 'input', 'button'],
    FORBID_ATTR: ['style'],
  });
  el.insertAdjacentHTML('beforeend', clean);
}

const WIKI_TYPE_ORDER: WikiType[] = ['entity', 'concept', 'theme'];
const WIKI_TYPE_LABEL: Record<string, string> = {
  entity: 'Entities',
  concept: 'Concepts',
  theme: 'Themes',
};

function wikiTagsHtml(tags: string[] | undefined): string {
  if (!tags || tags.length === 0) return '';
  return (
    '<span class="wiki-tags">' +
    tags.map((t) => '<span class="wiki-tag">' + escapeHtml(t) + '</span>').join('') +
    '</span>'
  );
}

/** Internal link to another wiki page (used in lists/backlinks). Always an
 * <a data-wiki-slug> so the content click handler intercepts it for SPA nav. */
function wikiInternalLink(slug: string, text?: string): string {
  const label = text || wikiPageMap.get(slug)?.title || slug;
  return (
    '<a href="/wiki/' + escapeHtml(slug) + '" class="wikilink" ' +
    'data-wiki-slug="' + escapeHtml(slug) + '">' + escapeHtml(label) + '</a>'
  );
}

// LIST view: catalog grouped by type + a recent-changes panel + a count.
function renderWikiIndex(index: WikiIndex): void {
  setDocTitle('Wiki');
  const pages = index.pages.slice();
  if (pages.length === 0) {
    setSafeWikiContent(
      content,
      [
        '<div class="content-card">',
        '  <div class="empty-state">',
        '    <div class="empty-state-icon">' + DOC_ICON + '</div>',
        '    <div class="empty-state-text">No wiki pages yet</div>',
        '  </div>',
        '</div>',
      ].join('\n'),
    );
    return;
  }

  // Optional search filter over title/summary/tags/aliases.
  const term = searchTerm.toLowerCase();
  const visible = term
    ? pages.filter((p) => {
        const hay = (
          p.title + ' ' + (p.summary || '') + ' ' +
          (p.tags || []).join(' ') + ' ' + (p.aliases || []).join(' ')
        ).toLowerCase();
        return hay.indexOf(term) !== -1;
      })
    : pages;

  // Group by type, with the known types first then any unknown types.
  const groups = new Map<string, WikiPage[]>();
  for (const p of visible) {
    const key = String(p.type || 'other');
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key)!.push(p);
  }
  const orderedKeys = [
    ...WIKI_TYPE_ORDER.filter((k) => groups.has(k)),
    ...Array.from(groups.keys()).filter((k) => !WIKI_TYPE_ORDER.includes(k as WikiType)),
  ];

  const sections: string[] = [];
  for (const key of orderedKeys) {
    const rows = groups.get(key)!.slice().sort((a, b) => a.title.localeCompare(b.title));
    const label = WIKI_TYPE_LABEL[key] || (key.charAt(0).toUpperCase() + key.slice(1));
    const items = rows
      .map((p) =>
        [
          '<li class="wiki-item">',
          '  <div class="wiki-item-head">',
          '    ' + wikiInternalLink(p.slug, p.title),
          '    <span class="wiki-type-chip wiki-type-' + escapeHtml(String(p.type)) + '">' +
            escapeHtml(String(p.type)) + '</span>',
          '  </div>',
          p.summary ? '  <div class="wiki-item-summary">' + escapeHtml(p.summary) + '</div>' : '',
          wikiTagsHtml(p.tags),
          '</li>',
        ].join('\n'),
      )
      .join('\n');
    sections.push(
      [
        '<section class="wiki-group">',
        '  <h2 class="wiki-group-title">' + escapeHtml(label) +
          ' <span class="wiki-group-count">' + rows.length + '</span></h2>',
        '  <ul class="wiki-list">',
        items,
        '  </ul>',
        '</section>',
      ].join('\n'),
    );
  }

  // Recent-changes panel (newest first, already ordered in the index).
  const log = (index.recent_log || []).slice(0, 12);
  const logHtml = log.length
    ? [
        '<aside class="wiki-recent">',
        '  <h2 class="wiki-recent-title">Recent changes</h2>',
        '  <ul class="wiki-recent-list">',
        log
          .map((e) =>
            [
              '<li class="wiki-recent-item">',
              '  <span class="wiki-recent-date">' + escapeHtml(e.date || '') + '</span>',
              '  <span class="wiki-recent-op wiki-op-' + escapeHtml(e.op || '') + '">' +
                escapeHtml(e.op || '') + '</span>',
              '  <span class="wiki-recent-summary">' + escapeHtml(e.summary || '') + '</span>',
              '</li>',
            ].join('\n'),
          )
          .join('\n'),
        '  </ul>',
        '</aside>',
      ].join('\n')
    : '';

  const emptyNote =
    visible.length === 0
      ? '<div class="empty-state-text wiki-empty">No wiki pages match the search.</div>'
      : '';

  setSafeWikiContent(
    content,
    [
      '<div class="content-card wiki-index-card">',
      '  <div class="wiki-index-header">',
      '    <h1 class="wiki-index-title">LLM Wiki</h1>',
      '    <span class="wiki-index-count">' + pages.length + ' pages</span>',
      '  </div>',
      '  <div class="wiki-index-layout">',
      '    <div class="wiki-index-main">',
      emptyNote,
      sections.join('\n'),
      '    </div>',
      logHtml,
      '  </div>',
      '</div>',
    ].join('\n'),
  );
}

// PAGE view: title + type chip + tags + rendered body + backlinks + related.
function renderWikiPage(page: WikiPage, body: string): void {
  setDocTitle(page.title);
  const bodyHtml = wikiMarkdownToHtml(stripWikiFrontmatter(body));

  // Backlinks from page.inbound (slug list). Titles come from the index map.
  const inbound = (page.inbound || []).filter((s) => s !== page.slug);
  const backlinksHtml = inbound.length
    ? [
        '<section class="wiki-backlinks">',
        '  <h2 class="wiki-section-title">Backlinks</h2>',
        '  <ul class="wiki-link-list">',
        inbound
          .map((s) => '<li class="wiki-link-item">' + wikiInternalLink(s) + '</li>')
          .join('\n'),
        '  </ul>',
        '</section>',
      ].join('\n')
    : '';

  // Related = outbound links not already shown as backlinks (avoid duplication).
  const inboundSet = new Set(inbound);
  const related = (page.outbound || []).filter((s) => s !== page.slug && !inboundSet.has(s));
  const relatedHtml = related.length
    ? [
        '<section class="wiki-related">',
        '  <h2 class="wiki-section-title">Related</h2>',
        '  <ul class="wiki-link-list">',
        related
          .map((s) => '<li class="wiki-link-item">' + wikiInternalLink(s) + '</li>')
          .join('\n'),
        '  </ul>',
        '</section>',
      ].join('\n')
    : '';

  // Two-pass render. The scaffold (back BUTTON, header, meta, backlinks,
  // related) is dashboard-authored, trusted chrome — render it with the
  // standard setSafeContent so the <button data-wiki-back> survives (the
  // strict wiki sanitizer FORBIDs <button> and would strip it, killing the
  // back-nav handler). The page BODY is the only semi-trusted LLM-authored
  // part — inject it separately through setSafeWikiContent. The body slot is
  // left empty in the scaffold and filled in the second pass.
  setSafeContent(
    content,
    [
      '<div class="content-card wiki-page-card">',
      '  <div class="wiki-page-meta">',
      '    <button class="gen-research-back" data-wiki-back>&lsaquo; All pages</button>',
      '    <span class="wiki-type-chip wiki-type-' + escapeHtml(String(page.type)) + '">' +
        escapeHtml(String(page.type)) + '</span>',
      '  </div>',
      '  <div class="wiki-page-header">',
      '    <h1 class="wiki-page-title">' + escapeHtml(page.title) + '</h1>',
      page.summary ? '    <p class="wiki-page-summary">' + escapeHtml(page.summary) + '</p>' : '',
      wikiTagsHtml(page.tags),
      '  </div>',
      '  <div class="wiki-page-body md-content"></div>',
      backlinksHtml,
      relatedHtml,
      '</div>',
    ].join('\n'),
  );

  // Second pass: the LLM-authored markdown body goes through the stricter
  // sanitizer (forbids iframe/script/style/svg/math/form/input/button + inline
  // style), keeping only data-wiki-slug anchors/spans for click-routing.
  const bodyEl = content.querySelector('.wiki-page-body') as HTMLElement | null;
  if (bodyEl) setSafeWikiContent(bodyEl, bodyHtml);
}

function renderWikiNotFound(slug: string): void {
  setDocTitle('Wiki');
  // All trusted dashboard chrome (including the back <button>) — use the
  // standard sanitizer so the button + data-wiki-back survive. No LLM body here.
  setSafeContent(
    content,
    [
      '<div class="content-card">',
      '  <div class="empty-state">',
      '    <div class="empty-state-icon">' + DOC_ICON + '</div>',
      '    <div class="empty-state-text">Wiki page not found: ' + escapeHtml(slug) + '</div>',
      '    <button class="gen-research-back" data-wiki-back>&lsaquo; Back to wiki</button>',
      '  </div>',
      '</div>',
    ].join('\n'),
  );
}

function extractCycleSummary(body: string): string {
  const match = body.match(/\*\*Cycle summary\*\*:\s*([\s\S]*?)(?=\n###|\n####|\n\*\*(?:Evidence|Previously|Counter|Verification|Watch)\*\*:|$)/i);
  return match ? match[1].trim() : '';
}

function extractSectionText(body: string, label: string): string {
  const re = new RegExp('\\*\\*' + label + '\\*\\*:\\s*([\\s\\S]*?)(?=\\n\\*\\*(?:Previously|Evidence|Counter / contradicting|Verification|Watch)\\*\\*:|\\n####\\s+\\d+\\.|$)', 'i');
  const match = body.match(re);
  return match ? match[1].trim() : '';
}

function cleanEvidenceLead(text: string): string {
  return text
    .split('\n')
    .map((line) => line
      .replace(/\*\*/g, '')
      .replace(/^[-*]\s+/, '')
      .replace(/^https?:\/\/\S+\s*(?:—|-|:)\s*/i, '')
      .replace(/^[\w.-]+\.[a-z]{2,}(?:\/\S*)?\s*(?:\([^)]*\))?\s*(?:—|-|:)+\s*/i, '')
      .replace(/^@[\w_]+:\s*/i, '')
      .replace(/^@[\w_]+\s+[^—\n]{0,140}\s+—\s*/i, '')
      .replace(/^["“]?[^"”]{0,160}["”]?\s+—\s+https?:\/\/\S+\s*(?:—\s*)?/i, '')
      .replace(/^\s*(?:—|-)+\s*/, '')
      .replace(/^the originating\b/i, 'Originating')
      .trim())
    .filter(Boolean)
    .join(' ');
}

function storyCurrentLead(body: string): string {
  const evidence = extractSectionText(body, 'Evidence');
  if (evidence) return cleanEvidenceLead(evidence);
  return body
    .replace(/\*\*Previously\*\*:?[\s\S]*?(?=\n\*\*(?:Evidence|Counter \/ contradicting|Verification|Watch)\*\*:|$)/i, '')
    .trim();
}

function parseTwitterStories(body: string): TwitterStory[] {
  const storyRe = /^####\s+(\d+)\.\s+(.+)$/gm;
  const matches = Array.from(body.matchAll(storyRe));
  return matches.map((match, idx) => {
    const start = (match.index || 0) + match[0].length;
    const nextStory = idx + 1 < matches.length ? matches[idx + 1].index || body.length : body.length;
    const nextSection = body.slice(start).search(/\n###\s+/);
    const sectionEnd = nextSection >= 0 ? start + nextSection : body.length;
    const end = Math.min(nextStory, sectionEnd);
    const storyBody = body.slice(start, end).trim();
    return {
      rank: match[1],
      title: match[2].trim(),
      body: storyBody,
      links: extractUrls(storyBody),
      handles: extractHandles(match[2] + '\n' + storyBody),
    };
  });
}

function firstText(root: ParentNode, selector: string): string {
  return root.querySelector(selector)?.textContent?.replace(/\s+/g, ' ').trim() || '';
}

function firstHtml(root: ParentNode, selector: string): string {
  return (root.querySelector(selector) as HTMLElement | null)?.innerHTML?.trim() || '';
}

function renderStructuredTwitterStories(body: string): string {
  if (!/\btwitter-story\b/.test(body)) return '';
  const doc = new DOMParser().parseFromString('<div>' + body + '</div>', 'text/html');
  const stories = Array.from(doc.querySelectorAll('article.twitter-story'));
  if (stories.length === 0) return '';

  return stories.map((story, idx) => {
    const rank = story.getAttribute('data-rank') || String(idx + 1);
    const title = firstText(story, '.twitter-story-title, h3');
    const lead = firstText(story, '.twitter-story-lead');
    const sources = firstHtml(story, '.twitter-story-sources');
    const signals = firstHtml(story, '.twitter-story-signals');
    const bodyHtml = firstHtml(story, '.twitter-story-body') || firstHtml(story, '.twitter-story-details');
    const detailsBits = [
      sources ? '<div class="twitter-story-chips">' + sources + '</div>' : '',
      signals ? '<div class="twitter-story-signals">' + signals + '</div>' : '',
      bodyHtml ? '<div class="md-content twitter-story-body">' + bodyHtml + '</div>' : '',
    ].filter(Boolean).join('\n');

    return [
      '<article class="twitter-story-card">',
      '  <div class="twitter-story-rank">' + escapeHtml(rank) + '</div>',
      '  <div class="twitter-story-main">',
      title ? '    <h3 class="twitter-story-title">' + highlightPlainText(title) + '</h3>' : '',
      lead ? '    <p class="twitter-story-summary">' + highlightPlainText(truncateText(cleanPublicLeadText(lead), 360)) + '</p>' : '',
      detailsBits
        ? [
            '    <details class="twitter-story-details">',
            '      <summary>Full analysis</summary>',
            detailsBits,
            '    </details>',
          ].join('\n')
        : '',
      '  </div>',
      '</article>',
    ].filter(Boolean).join('\n');
  }).join('\n');
}

function sanitizePublicReportMarkdown(md: string): string {
  const lines = md.split('\n');
  const out: string[] = [];
  let skippingInternalSection = false;
  let skippingInternalStory = false;
  const internalToolLeak =
    /\b(?:bird-fast|bird)\b.*(?:HTTP\s*403|Cloudflare|cookie|auth|User not found|\[err\]|returned|failed|blocked|degraded)/i;
  const internalAccessNote =
    /(?:Twitter access degraded|access restoration|cookie-clearance|not independently re-verifiable|0 successful bird|successful bird-fast|degraded-access)/i;

  for (const line of lines) {
    if (/^###\s+Research notes\b/i.test(line)) {
      skippingInternalSection = true;
      skippingInternalStory = false;
      continue;
    }
    if (skippingInternalSection && /^##\s+/.test(line)) {
      skippingInternalSection = false;
    } else if (skippingInternalSection) {
      continue;
    }

    if (/^####\s+\d+\.\s+.*(?:TWITTER ACCESS DEGRADED|BIRD-FAST HTTP|BIRD HTTP|ACCESS DEGRADED)/i.test(line)) {
      skippingInternalStory = true;
      continue;
    }
    if (skippingInternalStory && /^(?:####\s+\d+\.|###\s+|##\s+)/.test(line)) {
      skippingInternalStory = false;
    } else if (skippingInternalStory) {
      continue;
    }

    if (internalToolLeak.test(line) || internalAccessNote.test(line)) continue;
    out.push(
      line
        .replace(/\bverified bird-fast (?:user-tweets|search|read|tweet|thread)\b/gi, 'verified')
        .replace(/\bre-verified bird-fast (?:user-tweets|search|read|tweet|thread)\b/gi, 're-verified')
        .replace(/\bbird-fast\s+/gi, ''),
    );
  }

  return out.join('\n').replace(/\n{4,}/g, '\n\n\n').trim();
}

function renderTwitterReport(md: string, fallbackDate: string | null = null): void {
  const sections = splitSections(sanitizePublicReportMarkdown(md)).reverse();
  const cards: string[] = [];
  if (fallbackDate) {
    cards.push(
      '<div class="frontpage-fallback-note">No Twitter report for ' +
        escapeHtml(fmtDate(currentDate)) +
        '. Showing ' +
        escapeHtml(fallbackDate) +
        ' instead.</div>',
    );
  }

  for (const section of sections) {
    // Skip the document-level H1 that appears before the first cycle heading.
    if (!section.title && (!section.body || /^#\s+.+$/.test(section.body.trim()))) continue;

    const title = section.title || displayDate(currentDate);
    const dateStr = fmtDate(currentDate);
    const timeInfo = parseUtcTime(section.title, dateStr);
    const cycleSummary = extractCycleSummary(section.body);
    const stories = parseTwitterStories(section.body);
    const displayTime = timeInfo
      ? '<span class="twitter-cycle-time">' + escapeHtml(timeInfo.utc) + '</span><span class="local-time">' + escapeHtml(timeInfo.local) + '</span>'
      : '<span class="twitter-cycle-time">' + escapeHtml(title) + '</span>';
    const leadText = cycleSummary
      ? truncateText(cleanPublicLeadText(stripMarkdown(cycleSummary)), 620)
      : truncateText(cleanPublicLeadText(stripMarkdown(section.body)), 620);
    const leadHtml = twitterMarkdownToHtml(section.body);
    const structuredStoryCards = renderStructuredTwitterStories(section.body);
    const storyCards = structuredStoryCards || stories.map((story) => {
      const verification = truncateText(stripMarkdown(extractSectionText(story.body, 'Verification')), 210);
      const watch = truncateText(stripMarkdown(extractSectionText(story.body, 'Watch')), 210);
      const storyIntro = stripMarkdown(storyCurrentLead(story.body))
        .replace(/^[\s\-—–]+/, '')
        .replace(/^the originating\b/i, 'Originating');
      const storySummary = isSourceMethodLead(storyIntro) ? '' : truncateText(cleanPublicLeadText(storyIntro), 360);
      const storyLinks = renderSourceChips(story.links, 6);
      const storyHandles = renderHandleChips(story.handles, 8);
      return [
        '<article class="twitter-story-card">',
        '  <div class="twitter-story-rank">' + escapeHtml(story.rank) + '</div>',
        '  <div class="twitter-story-main">',
        '    <h3 class="twitter-story-title">' + highlightPlainText(story.title) + '</h3>',
        storySummary ? '    <p class="twitter-story-summary">' + highlightPlainText(storySummary) + '</p>' : '',
        '    <details class="twitter-story-details">',
        '      <summary>Full analysis</summary>',
        storyLinks || storyHandles ? '      <div class="twitter-story-chips">' + storyLinks + storyHandles + '</div>' : '',
        verification || watch
          ? '      <div class="twitter-story-signals">' +
              (verification ? '<div><span>Verify</span>' + highlightPlainText(verification) + '</div>' : '') +
              (watch ? '<div><span>Watch</span>' + highlightPlainText(watch) + '</div>' : '') +
            '</div>'
          : '',
        '      <div class="md-content twitter-story-body">' + twitterMarkdownToHtml(story.body) + '</div>',
        '    </details>',
        '  </div>',
        '</article>',
      ].filter(Boolean).join('\n');
    }).join('\n');

    cards.push(
      [
        '<section class="content-card twitter-cycle-card">',
        '  <div class="twitter-cycle-header">',
        '    <div class="twitter-cycle-kicker">' + (timeInfo ? clockIcon(timeInfo.localHours, timeInfo.localMinutes) : '') + displayTime + '</div>',
        '  </div>',
        '  <div class="twitter-wire-brief">',
        '    <div>',
        '      <div class="twitter-brief-label">Signal Brief</div>',
        '      <p class="twitter-brief-text">' + highlightPlainText(leadText) + '</p>',
        '    </div>',
        '  </div>',
        '  <details class="twitter-cycle-summary">',
        '    <summary>Full cycle text</summary>',
        '    <div class="md-content twitter-summary-body">' + leadHtml + '</div>',
        '  </details>',
        storyCards ? '  <div class="twitter-story-grid">' + storyCards + '</div>' : '  <div class="md-content twitter-story-body">' + twitterMarkdownToHtml(section.body) + '</div>',
        '</section>',
      ].join('\n'),
    );
  }

  setSafeContent(content, '<div class="twitter-report">' + cards.join('\n') + '</div>');
}

function loadTickets(): Promise<Ticket[] | null> {
  if (ticketsCache) return Promise.resolve(ticketsCache);
  if (ticketsPromise) return ticketsPromise;
  ticketsPromise = (async () => {
    try {
      const resp = await fetch(`${DATA_BASE}/models/tickets/index.json`, { cache: 'no-cache' });
      if (!resp.ok) return null;
      const data = (await resp.json()) as TicketIndex;
      if (!data || !Array.isArray(data.tickets)) return null;
      ticketsCache = data.tickets;
      return ticketsCache;
    } catch {
      return null;
    }
  })();
  return ticketsPromise;
}

function ticketStatusPill(status: TicketStatus): string {
  // Color via class so dark/light mode and contrast stay consistent.
  const labels: Record<TicketStatus, string> = {
    'rumored': 'Rumored',
    'in-testing': 'In Testing',
    'confirmed': 'Confirmed',
    'released': 'Released',
    'closed': 'Closed',
  };
  return `<span class="ticket-pill ticket-pill-${status}">${escapeHtml(labels[status])}</span>`;
}

function ticketVerificationBadge(verification: TicketVerification): string {
  if (verification === 'confirmed') return '';
  const label = verification === 'partial' ? '◐ partial corroboration' : '⚠ unverified';
  return `<span class="ticket-verification ticket-verification-${verification}">${escapeHtml(label)}</span>`;
}

function ticketCard(ticket: Ticket): string {
  const expanded = ticket.slug === expandedTicketSlug;
  const sourcesPreview = ticket.sources.slice(0, 3).map((s) => {
    if (s.startsWith('@')) return `<span class="ticket-source-handle">${escapeHtml(s)}</span>`;
    return `<a class="ticket-source-link" href="${escapeHtml(s)}" target="_blank" rel="noopener">${escapeHtml(hostnameOf(s))}</a>`;
  }).join('');
  const extraSources = ticket.sources.length > 3 ? `<span class="ticket-source-more">+${ticket.sources.length - 3}</span>` : '';
  const labelsHtml = (ticket.labels || []).map((l) => `<span class="ticket-label">${escapeHtml(l)}</span>`).join('');
  const expectedRow = ticket.expected
    ? `<div class="ticket-row"><span class="ticket-row-key">Expected</span><span class="ticket-row-val">${escapeHtml(ticket.expected)}</span></div>`
    : '';
  const noteRow = ticket.status_note
    ? `<div class="ticket-row ticket-row-note">${escapeHtml(ticket.status_note)}</div>`
    : '';
  const closedRow = ticket.status === 'closed' && ticket.closed_reason
    ? `<div class="ticket-row ticket-row-closed"><span class="ticket-row-key">Closed</span><span class="ticket-row-val">${escapeHtml(ticket.closed_at || '')} — ${escapeHtml(ticket.closed_reason)}</span></div>`
    : '';

  const headerHtml = [
    `<div class="ticket-header">`,
    `  <div class="ticket-header-top">`,
    `    ${ticketStatusPill(ticket.status)}`,
    `    <span class="ticket-company">${escapeHtml(ticket.company)}</span>`,
    `    ${ticketVerificationBadge(ticket.verification)}`,
    `  </div>`,
    `  <h3 class="ticket-title">${escapeHtml(ticket.title)}</h3>`,
    ticket.model ? `  <div class="ticket-model">${escapeHtml(ticket.model)}</div>` : '',
    `</div>`,
  ].filter(Boolean).join('\n');

  const metaHtml = [
    expectedRow,
    noteRow,
    closedRow,
    labelsHtml ? `<div class="ticket-labels">${labelsHtml}</div>` : '',
    `<div class="ticket-sources">${sourcesPreview}${extraSources}</div>`,
    `<div class="ticket-footer"><span>updated ${escapeHtml(ticket.updated_at)}</span><span>slug: ${escapeHtml(ticket.slug)}</span></div>`,
  ].filter(Boolean).join('\n');

  return `<article class="ticket-card ticket-card-${ticket.status}${expanded ? ' ticket-card-expanded' : ''}" data-slug="${escapeHtml(ticket.slug)}">
    ${headerHtml}
    <div class="ticket-meta">${metaHtml}</div>
  </article>`;
}

function ticketExpandedPanel(ticket: Ticket | null): string {
  if (!ticket) return '';
  return `<section class="ticket-detail-panel" aria-label="${escapeHtml(ticket.title)} details">
    <div class="ticket-detail-header">
      ${ticketStatusPill(ticket.status)}
      <h3>${escapeHtml(ticket.title)}</h3>
    </div>
    <div class="ticket-expanded">
      <div class="ticket-body md-content">${DOMPurify.sanitize(marked.parse(ticket.body) as string)}</div>
      <div class="ticket-history">
        <h4 class="ticket-history-title">History</h4>
        <ol class="ticket-history-list">${ticket.history.map((h) => `<li><span class="ticket-history-ts">${escapeHtml(h.ts)}</span><span class="ticket-history-change">${escapeHtml(h.change)}</span></li>`).join('')}</ol>
      </div>
      <div class="ticket-all-sources">
        <h4 class="ticket-history-title">All sources (${ticket.sources.length})</h4>
        <ul class="ticket-source-list">${ticket.sources.map((s) => s.startsWith('@')
          ? `<li><span class="ticket-source-handle">${escapeHtml(s)}</span></li>`
          : `<li><a href="${escapeHtml(s)}" target="_blank" rel="noopener">${escapeHtml(s)}</a></li>`).join('')}</ul>
      </div>
    </div>
  </section>`;
}

function ticketSortKey(t: Ticket): [number, string] {
  // Active tickets first (sorted by updated_at desc), closed at the bottom.
  const isClosed = t.status === 'closed' ? 1 : 0;
  // Negate the date string so newer sorts before older after we lexsort.
  // Easier: prefix '~' for "high priority" sentinels and use string comparison.
  return [isClosed, t.updated_at];
}

function applyTicketFilters(tickets: Ticket[]): Ticket[] {
  let out = tickets;
  if (ticketFilters.status !== 'all') {
    out = out.filter((t) => t.status === ticketFilters.status);
  }
  if (ticketFilters.company !== 'all') {
    out = out.filter((t) => companyKey(t.company) === ticketFilters.company);
  }
  if (searchTerm) {
    const needle = searchTerm.toLowerCase();
    out = out.filter((t) =>
      t.title.toLowerCase().includes(needle) ||
      (t.model || '').toLowerCase().includes(needle) ||
      t.body.toLowerCase().includes(needle) ||
      (t.status_note || '').toLowerCase().includes(needle) ||
      t.company.toLowerCase().includes(needle) ||
      (t.labels || []).some((l) => l.toLowerCase().includes(needle)),
    );
  }
  // Sort: active first (by updated_at desc), then closed.
  out = [...out].sort((a, b) => {
    const [aClosed, aUpd] = ticketSortKey(a);
    const [bClosed, bUpd] = ticketSortKey(b);
    if (aClosed !== bClosed) return aClosed - bClosed;
    return aUpd < bUpd ? 1 : aUpd > bUpd ? -1 : 0;
  });
  return out;
}

function companyKey(company: string): string {
  // Normalize "Google / DeepMind" → "google", "OpenAI / Codex" → "openai".
  return company.toLowerCase().split('/')[0].trim();
}

function renderTickets(tickets: Ticket[] | null): void {
  if (!tickets || tickets.length === 0) {
    setSafeContent(
      content,
      `<div class="content-card"><div class="content-card-body">
        <p>No model tickets yet. The daily CRUD agent will seed this list on the next run, or run <code>workflow_dispatch</code> on
        <a href="https://github.com/guzus/ai-research-arm/actions/workflows/24h-model-timeline.yml" target="_blank" rel="noopener">24h-model-timeline</a>.</p>
      </div></div>`,
    );
    return;
  }
  const filtered = applyTicketFilters(tickets);

  const statusOptions: TicketStatus[] = ['rumored', 'in-testing', 'confirmed', 'released', 'closed'];
  const companyKeys = Array.from(new Set(tickets.map((t) => companyKey(t.company)))).sort();
  const companyLabels: Record<string, string> = {};
  for (const t of tickets) {
    const key = companyKey(t.company);
    if (!companyLabels[key]) companyLabels[key] = t.company.split('/')[0].trim();
  }
  const statusCounts: Record<string, number> = { all: tickets.length };
  for (const s of statusOptions) statusCounts[s] = tickets.filter((t) => t.status === s).length;

  const statusBar = [
    `<button class="ticket-filter-pill${ticketFilters.status === 'all' ? ' active' : ''}" data-filter-status="all">All <span class="ticket-filter-count">${statusCounts.all}</span></button>`,
    ...statusOptions.map((s) => `<button class="ticket-filter-pill ticket-filter-pill-${s}${ticketFilters.status === s ? ' active' : ''}" data-filter-status="${s}">${escapeHtml(s)} <span class="ticket-filter-count">${statusCounts[s]}</span></button>`),
  ].join('');

  const companyOptions = ['all', ...companyKeys].map((k) =>
    `<option value="${escapeHtml(k)}"${ticketFilters.company === k ? ' selected' : ''}>${escapeHtml(k === 'all' ? 'All companies' : companyLabels[k] || k)}</option>`).join('');

  const visibleStatuses = ticketFilters.status === 'all'
    ? statusOptions
    : statusOptions.filter((s) => s === ticketFilters.status);
  const statusLabels: Record<TicketStatus, string> = {
    'rumored': 'Rumored',
    'in-testing': 'In testing',
    'confirmed': 'Confirmed',
    'released': 'Released',
    'closed': 'Closed',
  };
  const board = visibleStatuses.map((status) => {
    const cards = filtered.filter((ticket) => ticket.status === status);
    const cardHtml = cards.length
      ? cards.map(ticketCard).join('\n')
      : '<div class="ticket-column-empty">No tickets</div>';
    return [
      `<section class="ticket-column ticket-column-${status}" aria-label="${escapeHtml(statusLabels[status])} tickets">`,
      `  <div class="ticket-column-header"><span>${escapeHtml(statusLabels[status])}</span><span class="ticket-column-count">${cards.length}</span></div>`,
      `  <div class="ticket-column-cards">${cardHtml}</div>`,
      `</section>`,
    ].join('\n');
  }).join('\n');

  const emptyNote = filtered.length === 0
    ? `<div class="ticket-board-empty">No tickets match the current filters.</div>`
    : '';
  const detailPanel = ticketExpandedPanel(
    expandedTicketSlug ? filtered.find((ticket) => ticket.slug === expandedTicketSlug) || null : null,
  );

  setSafeContent(
    content,
    `<div class="tickets-view">
      <div class="tickets-heading">
        <h2>Board</h2>
        <div class="tickets-actions">
          <button class="ticket-action-btn" type="button" disabled>Release</button>
          <button class="ticket-more-btn" type="button" disabled aria-label="More options">•••</button>
        </div>
      </div>
      <div class="tickets-controls">
        <div class="ticket-filters">${statusBar}</div>
        <select class="ticket-company-select" data-filter-company>${companyOptions}</select>
        <div class="ticket-summary">${filtered.length} of ${tickets.length} tickets</div>
      </div>
      <div class="tickets-board">
        ${board}
      </div>
      ${detailPanel}
      ${emptyNote}
    </div>`,
  );
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
      '    <div class="content-card-title">THE AGI AWARENESS POST — ' + escapeHtml(displayDate(currentDate)) + '</div>',
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
      '    <div class="content-card-title">THE AGI AWARENESS POST — ' + escapeHtml(displayDate(currentDate)) + '</div>',
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
    const languageHtml = hasResearchLanguage(row, 'ko')
      ? '      <span class="gen-research-tag" lang="ko">한국어</span>'
      : '';
    items.push(
      [
        '<li class="gen-research-item" data-slug="' + escapeHtml(row.slug) + '" tabindex="0">',
        '  <div class="gen-research-item-main">',
        '    <div class="gen-research-item-title">' + title + '</div>',
        '    <div class="gen-research-item-meta">',
        '      <span class="gen-research-model">' + escapeHtml(row.model) + '</span>',
        rel ? '      <span class="gen-research-time">' + escapeHtml(rel) + '</span>' : '',
        tagHtml ? '      <span class="gen-research-tags">' + tagHtml + '</span>' : '',
        languageHtml,
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
      languageFallbackNote(row),
      researchAudioControlsHtml(row),
      '    <button class="gen-research-pdf" data-research-pdf title="Save this article as a PDF">Save as PDF</button>',
      '  </div>',
      '  <div class="content-card-body">',
      docHtml,
      '  </div>',
      '</div>',
    ].join('\n'),
  );

  setDocTitle(row.title);
  updateResearchAudioUi();

  // After DOM is in place, apply data-pct viz fills, wrap tables in a
  // horizontal-scroll container, expand pictogram counts, inject SVG
  // charts, and build the floating TOC.
  const article = content.querySelector('article.ara-doc') as HTMLElement | null;
  if (article) {
    article.lang = row.language === 'ko' ? 'ko' : 'en';
    applyBarFills(article);
    wrapAraTables(article);
    applyIsotypes(article);
    renderSparklines(article);
    renderLineCharts(article);
    renderDonuts(article);
    renderSlopes(article);
    renderTradingView(article);
    renderBarCharts(article);
    applyAraTooltips(article);
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

function approxSvgTextWidth(text: string, fontPx: number, mono = false): number {
  return text.length * fontPx * (mono ? 0.62 : 0.56);
}

function formatNumber(value: number, digits?: number): string {
  if (digits !== undefined) return value.toFixed(digits);
  return Number.isInteger(value) ? String(value) : String(value);
}

function formatUnitValue(value: number, unit: string, digits?: number): string {
  const n = formatNumber(value, digits);
  const u = unit.trim();
  if (!u) return n;
  // Currency prefix with trailing context, e.g. "$/kW" → "$5/kW".
  const currency = u.match(/^([$€£¥₩])(.+)$/);
  if (currency) return `${currency[1]}${n}${currency[2]}`;
  // Bare currency symbol prefixes the number with no space, e.g. "$" → "$5".
  if (/^[$€£¥₩]$/.test(u)) return `${u}${n}`;
  // Percent and percent-prefixed phrases bind tight to the number ("17%", "17% bit share").
  if (u === '%') return `${n}%`;
  if (u.startsWith('%')) return `${n}${u}`;
  // Everything else (alphabetic units like "GB/s", non-ASCII like "μm",
  // multi-word phrases like "k wpm" / "RMB B", or units with punctuation
  // like "index (2019=100)") renders as "<value> <unit>" with a single space.
  return `${n} ${u}`;
}

function fitSvgText(text: string, maxPx: number, fontPx: number, mono = false): string {
  if (approxSvgTextWidth(text, fontPx, mono) <= maxPx) return text;
  const charPx = fontPx * (mono ? 0.62 : 0.56);
  const maxChars = Math.max(6, Math.floor(maxPx / charPx) - 1);
  return `${text.slice(0, maxChars)}…`;
}

function setSvgFullLabel(el: SVGElement, text: string): void {
  el.setAttribute('aria-label', text);
}

function appendSvgTitle(el: SVGElement, text: string): void {
  const title = svgEl<SVGTitleElement>('title', {});
  title.textContent = text;
  el.appendChild(title);
}

const ARA_TOOLTIP_TITLE_ATTR = 'data-ara-tooltip-title';
const ARA_TOOLTIP_BODY_ATTR = 'data-ara-tooltip-body';
const ARA_TOOLTIP_BOUND_ATTR = 'data-ara-tooltip-bound';
let araTooltipDelegatesBound = false;

function compactText(el: Element | null): string {
  return (el?.textContent || '').replace(/\s+/g, ' ').trim();
}

function formatSignedNumber(value: number, digits?: number): string {
  if (value === 0) return formatNumber(0, digits);
  const sign = value > 0 ? '+' : '-';
  return sign + formatNumber(Math.abs(value), digits);
}

function deltaDigits(value: number): number {
  const abs = Math.abs(value);
  if (abs === 0) return 0;
  if (abs < 1) return 2;
  if (abs < 10) return 2;
  return 1;
}

function formatSignedUnitValue(value: number, unit: string): string {
  if (value === 0) return formatUnitValue(0, unit);
  const sign = value > 0 ? '+' : '-';
  return sign + formatUnitValue(Math.abs(value), unit, deltaDigits(value));
}

function pctLabel(raw: string | undefined): string | null {
  if (!raw) return null;
  const n = Number(raw);
  if (!Number.isFinite(n)) return null;
  return `${Math.max(0, Math.min(100, n))}%`;
}

function setAraTooltip(target: Element, title: string, body = ''): void {
  const cleanTitle = title.replace(/\s+/g, ' ').trim();
  const cleanBody = body.replace(/\s+/g, ' ').trim();
  if (!cleanTitle) return;
  target.setAttribute(ARA_TOOLTIP_TITLE_ATTR, cleanTitle);
  if (cleanBody) target.setAttribute(ARA_TOOLTIP_BODY_ATTR, cleanBody);
  else target.removeAttribute(ARA_TOOLTIP_BODY_ATTR);
  target.setAttribute('aria-label', cleanBody ? `${cleanTitle}: ${cleanBody}` : cleanTitle);
  if ((target instanceof HTMLElement || target instanceof SVGElement) && !target.hasAttribute('tabindex')) {
    target.setAttribute('tabindex', '0');
  }
}

function ensureAraTooltip(): HTMLDivElement {
  let tooltip = document.getElementById('araTooltip') as HTMLDivElement | null;
  if (tooltip) return tooltip;
  tooltip = document.createElement('div');
  tooltip.id = 'araTooltip';
  tooltip.className = 'ara-tooltip';
  tooltip.setAttribute('role', 'tooltip');
  tooltip.hidden = true;
  document.body.appendChild(tooltip);
  return tooltip;
}

function placeAraTooltip(tooltip: HTMLElement, clientX: number, clientY: number): void {
  const gap = 12;
  const edge = 8;
  const rect = tooltip.getBoundingClientRect();
  let x = clientX + gap;
  if (x + rect.width > window.innerWidth - edge) x = clientX - rect.width - gap;
  x = Math.max(edge, Math.min(window.innerWidth - rect.width - edge, x));
  let y = clientY - rect.height - gap;
  if (y < edge) y = clientY + gap;
  y = Math.max(edge, Math.min(window.innerHeight - rect.height - edge, y));
  tooltip.style.left = `${x}px`;
  tooltip.style.top = `${y}px`;
}

function showAraTooltip(target: Element, clientX: number, clientY: number): void {
  const title = target.getAttribute(ARA_TOOLTIP_TITLE_ATTR);
  if (!title) return;
  const body = target.getAttribute(ARA_TOOLTIP_BODY_ATTR) || '';
  const tooltip = ensureAraTooltip();
  tooltip.textContent = '';
  const titleEl = document.createElement('div');
  titleEl.className = 'ara-tooltip-title';
  titleEl.textContent = title;
  tooltip.appendChild(titleEl);
  if (body) {
    const bodyEl = document.createElement('div');
    bodyEl.className = 'ara-tooltip-body';
    bodyEl.textContent = body;
    tooltip.appendChild(bodyEl);
  }
  tooltip.hidden = false;
  tooltip.classList.add('is-visible');
  placeAraTooltip(tooltip, clientX, clientY);
}

function hideAraTooltip(): void {
  const tooltip = document.getElementById('araTooltip') as HTMLDivElement | null;
  if (!tooltip) return;
  tooltip.classList.remove('is-visible');
  tooltip.hidden = true;
}

function closestAraTooltipTarget(start: Element | null): Element | null {
  let el: Element | null = start;
  while (el && el !== document.documentElement) {
    if (el.hasAttribute(ARA_TOOLTIP_TITLE_ATTR)) return el;
    el = el.parentElement;
  }
  return null;
}

function ensureAraTooltipDelegates(): void {
  if (araTooltipDelegatesBound) return;
  araTooltipDelegatesBound = true;

  const handleMove = (event: MouseEvent): void => {
    const target = closestAraTooltipTarget(document.elementFromPoint(event.clientX, event.clientY));
    if (target) showAraTooltip(target, event.clientX, event.clientY);
    else hideAraTooltip();
  };

  document.addEventListener('mousemove', handleMove, true);
  document.addEventListener('pointermove', handleMove, true);
  document.addEventListener('mouseleave', hideAraTooltip, true);
  document.addEventListener('focusin', (event) => {
    const target = closestAraTooltipTarget(event.target instanceof Element ? event.target : null);
    if (!target) return;
    const rect = target.getBoundingClientRect();
    showAraTooltip(target, rect.left + rect.width / 2, rect.top + rect.height / 2);
  }, true);
  document.addEventListener('focusout', hideAraTooltip, true);
}

function bindAraTooltip(target: Element): void {
  ensureAraTooltipDelegates();
  if (target.getAttribute(ARA_TOOLTIP_BOUND_ATTR) === '1') return;
  target.setAttribute(ARA_TOOLTIP_BOUND_ATTR, '1');
  // Typed as EventListener (not MouseEvent) because addEventListener on the
  // base Element interface uses ElementEventMap, which does not include
  // pointer/mouse events — TS6 routes through the string-based overload that
  // requires Event. PointerEvent extends MouseEvent at runtime, so the
  // instanceof narrowing covers both pointer* and mouse* listeners below.
  const showFromMouse: EventListener = (event) => {
    if (!(event instanceof MouseEvent)) return;
    showAraTooltip(target, event.clientX, event.clientY);
  };
  const moveFromMouse: EventListener = (event) => {
    if (!(event instanceof MouseEvent)) return;
    const tooltip = document.getElementById('araTooltip') as HTMLDivElement | null;
    if (!tooltip || tooltip.hidden) return;
    placeAraTooltip(tooltip, event.clientX, event.clientY);
  };
  target.addEventListener('pointerenter', showFromMouse);
  target.addEventListener('pointermove', moveFromMouse);
  target.addEventListener('pointerleave', hideAraTooltip);
  target.addEventListener('mouseenter', showFromMouse);
  target.addEventListener('mousemove', moveFromMouse);
  target.addEventListener('mouseleave', hideAraTooltip);
  const showFromFocus = () => {
    const rect = target.getBoundingClientRect();
    showAraTooltip(target, rect.left + rect.width / 2, rect.top + rect.height / 2);
  };
  target.addEventListener('focus', showFromFocus);
  target.addEventListener('focusin', showFromFocus);
  target.addEventListener('blur', hideAraTooltip);
  target.addEventListener('focusout', hideAraTooltip);
}

function numberedVariant(el: Element, prefix: string): string | null {
  for (const className of Array.from(el.classList)) {
    const match = new RegExp(`^${prefix}--(\\d+)$`).exec(className);
    if (match) return match[1];
  }
  return null;
}

function stackSegmentCategory(seg: HTMLElement): string {
  const ownText = compactText(seg);
  if (ownText) return ownText;
  const idx = numberedVariant(seg, 'ara-stack-seg');
  if (!idx) return 'Segment';
  const rows = seg.closest('.ara-stack-rows');
  const rowCat = rows?.querySelector(`.ara-stack-rows-cat--${idx}`);
  if (rowCat) return compactText(rowCat);
  const stack = seg.closest('.ara-stack-bar');
  const legend = stack?.nextElementSibling?.classList.contains('ara-stack-legend')
    ? stack.nextElementSibling
    : stack?.parentElement?.querySelector('.ara-stack-legend');
  const legendItem = legend?.querySelector(`.ara-stack-dot--${idx}`)?.closest('li');
  return compactText(legendItem ?? null) || `Segment ${idx}`;
}

function decorateDataTooltips(root: HTMLElement): void {
  for (const bar of root.querySelectorAll<HTMLElement>('.ara-bar[data-pct]')) {
    const pct = pctLabel(bar.dataset.pct);
    if (!pct) continue;
    const label = compactText(bar.querySelector('.ara-bar-label')) || 'Bar';
    const value = compactText(bar.querySelector('.ara-bar-value'));
    setAraTooltip(bar, label, value ? `${value} · ${pct} of scale` : `${pct} of scale`);
  }

  for (const item of root.querySelectorAll<HTMLElement>('.ara-rank-item')) {
    const fill = item.querySelector<HTMLElement>('.ara-rank-fill[data-pct]');
    const pct = pctLabel(fill?.dataset.pct);
    if (!fill || !pct) continue;
    const rank = compactText(item.querySelector('.ara-rank-num'));
    const label = compactText(item.querySelector('.ara-rank-label')) || 'Ranked item';
    const value = compactText(item.querySelector('.ara-rank-value'));
    const prefix = rank ? `#${rank} · ` : '';
    setAraTooltip(item, `${prefix}${label}`, value ? `${value} · ${pct} of max` : `${pct} of max`);
  }

  for (const seg of root.querySelectorAll<HTMLElement>('.ara-stack-seg[data-pct]')) {
    const pct = pctLabel(seg.dataset.pct);
    if (!pct) continue;
    const row = seg.closest('.ara-stack-rows-row');
    const rowLabel = compactText(row?.querySelector('.ara-stack-rows-label') || null);
    const category = stackSegmentCategory(seg);
    setAraTooltip(seg, rowLabel ? `${rowLabel} · ${category}` : category, pct);
  }
}

function applyAraTooltips(root: HTMLElement): void {
  decorateDataTooltips(root);
  for (const target of root.querySelectorAll<Element>(`[${ARA_TOOLTIP_TITLE_ATTR}]`)) {
    bindAraTooltip(target);
  }
}

/** Distribute words across `lineCount` lines, minimizing the longest line
 * (in characters, including the inter-word space). Greedy enumeration of
 * split points; O(W^(lineCount-1)) so we cap lineCount at 3 and words at ≤8
 * for the donut center-label case. Returns null if lineCount > words.length. */
function splitWordsIntoLines(words: string[], lineCount: number): string[] | null {
  if (lineCount < 1 || lineCount > words.length) return null;
  if (lineCount === 1) return [words.join(' ')];

  const widthOf = (line: string) => line.length; // monospace: width ≈ chars
  let best: { lines: string[]; widest: number } | null = null;

  // Enumerate all ways to choose (lineCount-1) split positions from
  // (words.length-1) gaps. Recursive walk for arbitrary lineCount.
  const walk = (startWord: number, linesLeft: number, acc: string[]) => {
    if (linesLeft === 1) {
      const tail = words.slice(startWord).join(' ');
      const candidate = [...acc, tail];
      const widest = Math.max(...candidate.map(widthOf));
      if (!best || widest < best.widest) best = { lines: candidate, widest };
      return;
    }
    // Leave at least (linesLeft - 1) words for the remaining lines.
    const maxEnd = words.length - (linesLeft - 1);
    for (let end = startWord + 1; end <= maxEnd; end++) {
      const line = words.slice(startWord, end).join(' ');
      walk(end, linesLeft - 1, [...acc, line]);
    }
  };
  walk(0, lineCount, []);
  return best ? (best as { lines: string[]; widest: number }).lines : null;
}

/** Wrap a donut center-label into up to `maxLines` lines and pick a font
 * size that fits the widest line within `usableWidth` SVG units. Prefers
 * fewer lines at larger fonts. Falls back to clamped `minFontSize` for a
 * single ultra-long unhyphenated word (it will visually overflow, which
 * is better than dropping the label). */
function wrapDonutCenterLabel(
  label: string,
  maxFontSize: number,
  minFontSize: number,
  usableWidth: number,
  maxLines = 3,
): { lines: string[]; fontSize: number } {
  const clean = label.trim();
  if (!clean) return { lines: [], fontSize: maxFontSize };

  // 1-line fast path: if the whole string fits at max font, use it.
  // Preserves the exact pre-change rendering for short labels.
  // Uses approxSvgTextWidth with mono=true (0.62 ratio) for consistency
  // with the rest of the SVG-text helpers in this file.
  if (approxSvgTextWidth(clean, maxFontSize, true) <= usableWidth) {
    return { lines: [clean], fontSize: maxFontSize };
  }

  const words = clean.split(/\s+/);

  // Guard against pathological input. splitWordsIntoLines is recursive and
  // enumerates O(W^(maxLines-1)) split positions; with maxLines=3 that's
  // O(W^2). Realistic donut center-labels are 1-4 words (the longest in
  // the corpus is "The three-leg bottleneck" at 3 words). If a malformed
  // ara source ever stuffs a paragraph into center-label, bypass the wrap
  // enumeration entirely and render the whole label on a single shrunk
  // line — better than hanging the page or silently dropping words.
  const WORD_ENUM_CAP = 12;
  if (words.length > WORD_ENUM_CAP) {
    const ideal = usableWidth / Math.max(1, clean.length * 0.62);
    const fontSize = Math.max(minFontSize, Math.min(maxFontSize, ideal));
    return { lines: [clean], fontSize };
  }

  // Try N = 1..maxLines. For each N, find the split that minimizes the
  // widest line, then compute the largest font that fits that line.
  // Prefer the largest font (which tends to be the highest N that still
  // fits comfortably). Short-circuit once we hit the max font.
  const lineCap = Math.min(maxLines, words.length);
  let best: { lines: string[]; fontSize: number } | null = null;
  for (let n = 1; n <= lineCap; n++) {
    const lines = splitWordsIntoLines(words, n);
    if (!lines) continue;
    const widestChars = Math.max(...lines.map((l) => l.length));
    // font ≤ usableWidth / (widestChars * 0.62)
    const ideal = usableWidth / Math.max(1, widestChars * 0.62);
    const fontSize = Math.max(minFontSize, Math.min(maxFontSize, ideal));
    if (!best || fontSize > best.fontSize) {
      best = { lines, fontSize };
    }
    // If this N hits the cap, no point trying more lines (more lines
    // can't beat a max-font fit at fewer lines).
    if (fontSize >= maxFontSize) break;
  }
  return best ?? { lines: [clean], fontSize: minFontSize };
}

/** Build a polyline d-attribute from (x,y) pairs. */
function pathFromPoints(points: Array<[number, number]>): string {
  if (!points.length) return '';
  return points
    .map(([x, y], i) => (i === 0 ? `M${x.toFixed(2)},${y.toFixed(2)}` : `L${x.toFixed(2)},${y.toFixed(2)}`))
    .join(' ');
}

type LineChartPoint = {
  x: number;
  y: number;
  xLabel: string;
  valueLabel: string;
  seriesLabel: string;
  seriesIndex: number;
  pointIndex: number;
};

// ── TradingView live embed ────────────────────────────
// The article fragment carries only a script-free placeholder
// `<div class="ara-tradingview" data-symbol="NASDAQ:NOW">` plus a fallback
// link — the writer's validator rejects <script>/<iframe> in fragments. Here,
// in trusted dashboard code, we inject the real TradingView Advanced Chart
// widget, lazily via IntersectionObserver so s3.tradingview.com is only hit
// when a chart scrolls into view. The symbol is re-validated (defense in
// depth) before it reaches the third-party widget config.
const TV_SYMBOL_RE = /^[A-Za-z0-9:._-]{1,32}$/;
const TV_TOKEN_RE = /^[A-Za-z0-9]{1,5}$/;
const TV_EMBED_SRC = 'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js';

function mountTradingView(el: HTMLElement): void {
  if (el.dataset.tvMounted === '1') return;
  const symbol = el.getAttribute('data-symbol') || '';
  if (!TV_SYMBOL_RE.test(symbol)) return; // bad symbol → leave the fallback link in place
  el.dataset.tvMounted = '1';

  const interval = el.getAttribute('data-interval') || 'D';
  const range = el.getAttribute('data-range') || '';
  const theme = el.getAttribute('data-theme') === 'light' ? 'light' : 'dark';

  const config: Record<string, unknown> = {
    autosize: true,
    symbol,
    theme,
    style: '1',
    locale: 'en',
    allow_symbol_change: false,
    hide_side_toolbar: true,
    support_host: 'https://www.tradingview.com',
  };
  if (TV_TOKEN_RE.test(interval)) config.interval = interval;
  if (range && TV_TOKEN_RE.test(range)) config.range = range;

  const container = document.createElement('div');
  container.className = 'tradingview-widget-container';
  const widget = document.createElement('div');
  widget.className = 'tradingview-widget-container__widget';
  container.appendChild(widget);

  // The embed script reads its JSON config from its own text content. We set
  // it via textContent (never innerHTML) before appending, so there is no HTML
  // parsing surface; the symbol is regex-validated above.
  const script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = TV_EMBED_SRC;
  script.async = true;
  script.textContent = JSON.stringify(config);
  container.appendChild(script);

  el.appendChild(container);
  el.classList.add('is-loaded'); // CSS hides .ara-tradingview-fallback
}

/** Inject live TradingView widgets into `<div class="ara-tradingview" data-symbol>`
 * placeholders, lazily as they scroll into view. */
function renderTradingView(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-tradingview[data-symbol]');
  if (!els.length) return;
  if (typeof IntersectionObserver === 'undefined') {
    els.forEach(mountTradingView);
    return;
  }
  const io = new IntersectionObserver(
    (entries, obs) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          mountTradingView(entry.target as HTMLElement);
          obs.unobserve(entry.target);
        }
      }
    },
    { rootMargin: '200px' },
  );
  els.forEach((el) => io.observe(el));
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
    const firstValue = values[0];
    const lastValue = values[values.length - 1];
    const delta = lastValue - firstValue;
    const pct = firstValue !== 0 ? ` (${formatSignedNumber((delta / Math.abs(firstValue)) * 100, 1)}%)` : '';
    setAraTooltip(
      el,
      `Sparkline ${formatNumber(firstValue)} -> ${formatNumber(lastValue)}`,
      `change ${formatSignedNumber(delta, deltaDigits(delta))}${pct}`,
    );
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
    const xLabels = parseLabels(el.dataset.xLabels, 1000);
    const yUnit = el.dataset.yUnit || '';
    const title = el.dataset.title || '';
    const subtitle = el.dataset.subtitle || '';

    const W = 640;
    const H = 220;
    const MT = 10;
    const MB = 26;

    const allValues = seriesList.flatMap((s) => s.values);
    const min = Math.min(...allValues);
    const max = Math.max(...allValues);
    const pad = (max - min) * 0.08 || 1;
    const yMin = min - pad;
    const yMax = max + pad;
    const yRange = yMax - yMin || 1;
    const longest = Math.max(...seriesList.map((s) => s.values.length));
    const Y_TICKS = 5;
    const yTickLabels = Array.from({ length: Y_TICKS + 1 }, (_, i) => {
      const v = yMax - (i / Y_TICKS) * yRange;
      return formatUnitValue(v, yUnit, yRange < 5 ? 2 : 1);
    });
    const maxYLabelW = Math.max(...yTickLabels.map((label) => approxSvgTextWidth(label, 10, true)));
    const ML = Math.min(118, Math.max(44, Math.ceil(maxYLabelW) + 10));
    const MR = 16;
    const innerW = W - ML - MR;
    const innerH = H - MT - MB;

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
    for (let i = 0; i <= Y_TICKS; i++) {
      const y = MT + (i / Y_TICKS) * innerH;
      svg.appendChild(svgEl('line', { class: 'ara-chart-grid', x1: ML, y1: y, x2: W - MR, y2: y }));
      const lab = svgEl<SVGTextElement>('text', { class: 'ara-chart-tick-label', x: ML - 6, y: y + 3, 'text-anchor': 'end' });
      lab.textContent = yTickLabels[i];
      svg.appendChild(lab);
    }

    // X-axis labels — sparse to avoid clutter
    if (xLabels.length) {
      const stepRender = Math.max(1, Math.ceil(xLabels.length / 8));
      for (let i = 0; i < xLabels.length; i += stepRender) {
        const x = xFor(i, xLabels.length);
        const anchor = i === 0 ? 'start' : i + stepRender >= xLabels.length ? 'end' : 'middle';
        const lab = svgEl<SVGTextElement>('text', { class: 'ara-chart-tick-label', x, y: H - 8, 'text-anchor': anchor });
        lab.textContent = xLabels[i];
        svg.appendChild(lab);
      }
    }

    const chartPoints: LineChartPoint[] = [];

    // Series paths
    seriesList.forEach((s, idx) => {
      const points: Array<[number, number]> = s.values.map((v, i) => [
        xFor(i, s.values.length === 1 ? 2 : s.values.length),
        yFor(v),
      ]);
      const latestLabel = xLabels[s.values.length - 1] || `point ${s.values.length}`;
      const latestValue = formatUnitValue(s.values[s.values.length - 1], yUnit);
      const path = svgEl<SVGPathElement>('path', {
        class: `ara-chart-series ara-chart-series-${idx + 1}`,
        d: pathFromPoints(points),
        tabindex: '0',
      });
      appendSvgTitle(path, `${s.label}: latest ${latestValue} (${latestLabel})`);
      svg.appendChild(path);

      if (points.length <= 24) {
        points.forEach(([x, y], pointIdx) => {
          const label = xLabels[pointIdx] || `point ${pointIdx + 1}`;
          const value = formatUnitValue(s.values[pointIdx], yUnit);
          const visible = svgEl<SVGCircleElement>('circle', {
            class: `ara-chart-point ara-chart-point--${idx + 1}`,
            cx: x,
            cy: y,
            r: 2.2,
          });
          svg.appendChild(visible);
          const hit = svgEl<SVGCircleElement>('circle', {
            class: 'ara-chart-hit',
            cx: x,
            cy: y,
            r: 7,
          });
          appendSvgTitle(hit, `${s.label} · ${label}: ${value}`);
          svg.appendChild(hit);
        });
      }

      points.forEach(([x, y], pointIdx) => {
        chartPoints.push({
          x,
          y,
          xLabel: xLabels[pointIdx] || `point ${pointIdx + 1}`,
          valueLabel: formatUnitValue(s.values[pointIdx], yUnit),
          seriesLabel: s.label,
          seriesIndex: idx,
          pointIndex: pointIdx,
        });
      });
    });

    if (chartPoints.length) {
      const hoverZone = svgEl<SVGRectElement>('rect', {
        class: 'ara-chart-hover-zone',
        x: ML,
        y: MT,
        width: innerW,
        height: innerH,
        tabindex: '0',
        role: 'img',
        'aria-label': `${title || 'Line chart'}: hover or focus to inspect point values`,
      });
      const tooltip = svgEl<SVGGElement>('g', { class: 'ara-chart-tooltip', 'aria-hidden': 'true' });
      const guide = svgEl<SVGLineElement>('line', {
        class: 'ara-chart-tooltip-guide',
        x1: ML,
        y1: MT,
        x2: ML,
        y2: H - MB,
      });
      const marker = svgEl<SVGCircleElement>('circle', {
        class: 'ara-chart-tooltip-marker ara-chart-point--1',
        cx: ML,
        cy: MT,
        r: 4,
      });
      const box = svgEl<SVGRectElement>('rect', {
        class: 'ara-chart-tooltip-box',
        x: 0,
        y: 0,
        width: 80,
        height: 36,
        rx: 0,
      });
      const labelText = svgEl<SVGTextElement>('text', {
        class: 'ara-chart-tooltip-label',
        x: 8,
        y: 14,
      });
      const valueText = svgEl<SVGTextElement>('text', {
        class: 'ara-chart-tooltip-value',
        x: 8,
        y: 29,
      });

      tooltip.appendChild(guide);
      tooltip.appendChild(marker);
      tooltip.appendChild(box);
      tooltip.appendChild(labelText);
      tooltip.appendChild(valueText);
      svg.appendChild(hoverZone);
      svg.appendChild(tooltip);

      const keyboardPoints = [...chartPoints].sort((a, b) => a.pointIndex - b.pointIndex || a.seriesIndex - b.seriesIndex);
      let keyboardIndex = keyboardPoints.length - 1;

      const nearestPoint = (svgX: number, svgY: number): LineChartPoint => {
        let best = chartPoints[0];
        let bestScore = Number.POSITIVE_INFINITY;
        for (const point of chartPoints) {
          const dx = point.x - svgX;
          const dy = point.y - svgY;
          const score = dx * dx + dy * dy;
          if (score < bestScore) {
            best = point;
            bestScore = score;
          }
        }
        return best;
      };

      const showTooltip = (point: LineChartPoint): void => {
        const labelLine = seriesList.length > 1 ? `${point.xLabel} · ${point.seriesLabel}` : point.xLabel;
        const valueLine = point.valueLabel;
        const maxTextW = 150;
        const fittedLabel = fitSvgText(labelLine, maxTextW, 10);
        const fittedValue = fitSvgText(valueLine, maxTextW, 11, true);
        const boxW = Math.ceil(Math.max(76, Math.max(approxSvgTextWidth(fittedLabel, 10), approxSvgTextWidth(fittedValue, 11, true)) + 16));
        const boxH = 36;
        let boxX = point.x + 10;
        if (boxX + boxW > W - 4) boxX = point.x - boxW - 10;
        boxX = Math.max(4, Math.min(W - boxW - 4, boxX));
        let boxY = point.y - boxH - 10;
        if (boxY < 4) boxY = point.y + 10;
        boxY = Math.max(4, Math.min(H - boxH - 4, boxY));

        guide.setAttribute('x1', point.x.toFixed(2));
        guide.setAttribute('x2', point.x.toFixed(2));
        marker.setAttribute('cx', point.x.toFixed(2));
        marker.setAttribute('cy', point.y.toFixed(2));
        marker.setAttribute('class', `ara-chart-tooltip-marker ara-chart-point--${point.seriesIndex + 1}`);
        box.setAttribute('x', boxX.toFixed(2));
        box.setAttribute('y', boxY.toFixed(2));
        box.setAttribute('width', String(boxW));
        box.setAttribute('height', String(boxH));
        labelText.setAttribute('x', (boxX + 8).toFixed(2));
        labelText.setAttribute('y', (boxY + 14).toFixed(2));
        labelText.textContent = fittedLabel;
        valueText.setAttribute('x', (boxX + 8).toFixed(2));
        valueText.setAttribute('y', (boxY + 29).toFixed(2));
        valueText.textContent = fittedValue;
        tooltip.classList.add('is-visible');
        tooltip.setAttribute('aria-hidden', 'false');
        hoverZone.setAttribute('aria-label', `${point.seriesLabel} · ${point.xLabel}: ${point.valueLabel}`);
      };

      const hideTooltip = (): void => {
        tooltip.classList.remove('is-visible');
        tooltip.setAttribute('aria-hidden', 'true');
      };

      const pointerToSvg = (event: PointerEvent): [number, number] => {
        const rect = svg.getBoundingClientRect();
        const svgX = ((event.clientX - rect.left) / Math.max(1, rect.width)) * W;
        const svgY = ((event.clientY - rect.top) / Math.max(1, rect.height)) * H;
        return [svgX, svgY];
      };

      hoverZone.addEventListener('pointermove', (event) => {
        const [svgX, svgY] = pointerToSvg(event);
        showTooltip(nearestPoint(svgX, svgY));
      });
      hoverZone.addEventListener('pointerleave', hideTooltip);
      hoverZone.addEventListener('focus', () => {
        keyboardIndex = keyboardPoints.length - 1;
        showTooltip(keyboardPoints[keyboardIndex]);
      });
      hoverZone.addEventListener('blur', hideTooltip);
      hoverZone.addEventListener('keydown', (event) => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        const step = event.key === 'ArrowRight' ? 1 : -1;
        keyboardIndex = Math.max(0, Math.min(keyboardPoints.length - 1, keyboardIndex + step));
        showTooltip(keyboardPoints[keyboardIndex]);
      });
    }

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
        const latestLabel = xLabels[s.values.length - 1] || `point ${s.values.length}`;
        item.title = `${s.label}: latest ${formatUnitValue(s.values[s.values.length - 1], yUnit)} (${latestLabel})`;
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
      const slice = svgEl<SVGPathElement>('path', {
        class: `ara-donut-slice ara-donut-slice--${(idx % 6) + 1}`,
        d,
        tabindex: '0',
      });
      const pct = `${((values[idx] / total) * 100).toFixed(1)}%`;
      appendSvgTitle(slice, `${labels[idx]}: ${values[idx]} (${pct})`);
      setAraTooltip(slice, labels[idx], `${values[idx]} (${pct})`);
      svg.appendChild(slice);
    });

    if (centerLabel.trim()) {
      // Conservative usable width: 85% of the donut hole diameter to leave
      // breathing room from the slices. ri = 56 → hole = 112 → usable = ~95.
      const usableWidth = ri * 2 * 0.85;
      const wrapped = wrapDonutCenterLabel(centerLabel, 18, 9, usableWidth, 3);
      if (wrapped.lines.length === 1) {
        // 1-line. Two sub-cases:
        //   - At max font (18): use the original y = cy + 1 nudge to keep
        //     short labels like "2024" bit-identical to the pre-fix output.
        //   - Below max font (single oversize token, e.g. "Verylongunhyphenatedword"):
        //     respect the shrunk font and center at cy. Without this branch
        //     the shrink fallback would be silently discarded and the label
        //     would still overflow the donut hole.
        const fs = wrapped.fontSize;
        const atMax = fs >= 18;
        const text = svgEl<SVGTextElement>('text', {
          class: 'ara-donut-center-label',
          x: cx,
          y: atMax ? cy + 1 : cy,
          'font-size': atMax ? '18' : fs.toFixed(2),
        });
        text.textContent = wrapped.lines[0];
        svg.appendChild(text);
      } else if (wrapped.lines.length > 1) {
        // Multi-line: center the block vertically around cy. With
        // dominant-baseline: middle (from CSS), each tspan's y is its
        // vertical center. Stack lines with lineHeight = fontSize * 1.1.
        const fs = wrapped.fontSize;
        const lineHeight = fs * 1.1;
        const firstY = cy - ((wrapped.lines.length - 1) * lineHeight) / 2;
        const text = svgEl<SVGTextElement>('text', {
          class: 'ara-donut-center-label',
          x: cx,
          y: firstY,
          'font-size': String(fs.toFixed(2)),
        });
        wrapped.lines.forEach((line, i) => {
          const tspan = svgEl<SVGTSpanElement>('tspan', {
            x: cx,
            y: (firstY + i * lineHeight).toFixed(2),
          });
          tspan.textContent = line;
          text.appendChild(tspan);
        });
        svg.appendChild(text);
      }
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
      li.title = `${label}: ${values[idx]} (${pct.toFixed(1)}%)`;
      setAraTooltip(li, label, `${values[idx]} (${pct.toFixed(1)}%)`);
      li.appendChild(swatch);
      li.appendChild(name);
      li.appendChild(value);
      legend.appendChild(li);
    });
    el.appendChild(legend);
    el.dataset.rendered = '1';
  }
}

/** In-place bounded anti-overlap. Sort items by current Y, walk top-down to
 * push colliders down by `lineHeight`, then if the bottommost item exceeds
 * `maxY` clamp it and walk back up pushing earlier items higher to make room.
 * Mutates the input array.
 *
 * Properties:
 * - Stable: items that don't overlap keep their original positions, so
 *   comfortable slope charts render pixel-identically to before this pass.
 * - Bounded: no item ends up below `maxY`, so labels can't get clipped by
 *   the SVG viewBox even when many values cluster at the bottom of the chart.
 *   (Bottom-bound only; the symmetric top-clip case would need yTop and
 *   doesn't trigger for any real data we render today.) */
function antiOverlap(positions: number[], lineHeight: number, maxY: number): void {
  if (positions.length < 2) return;
  const order = positions.map((_, i) => i).sort((a, b) => positions[a] - positions[b]);
  // Forward sweep: push each colliding label down by lineHeight.
  for (let j = 1; j < order.length; j++) {
    const prev = positions[order[j - 1]];
    const cur = positions[order[j]];
    if (cur - prev < lineHeight) {
      positions[order[j]] = prev + lineHeight;
    }
  }
  // Backward sweep: if the bottommost label overflows the viewport, clamp it
  // and push preceding labels up only as far as needed to keep `lineHeight`
  // between them. The clamp shrinks the gap from `lineHeight` toward zero
  // (labels can still overlap if too many cluster at the very bottom) but
  // keeps every label inside the SVG so nothing disappears.
  const last = order.length - 1;
  if (positions[order[last]] > maxY) {
    positions[order[last]] = maxY;
    for (let j = last - 1; j >= 0; j--) {
      const below = positions[order[j + 1]];
      if (positions[order[j]] > below - lineHeight) {
        positions[order[j]] = below - lineHeight;
      } else {
        // No more pressure to push; everything above is already clear.
        break;
      }
    }
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

    const W = 960;
    const rowH = 26;
    const headerH = 30;
    const H = headerH + items.length * rowH + 20;
    const leftTexts = items.map((name, i) => `${name} ${formatUnitValue(leftValues[i], unit)}`);
    const rightTexts = items.map((name, i) => `${formatUnitValue(rightValues[i], unit)} ${name}`);
    const maxLeftW = Math.max(...leftTexts.map((text) => approxSvgTextWidth(text, 12)));
    const maxRightW = Math.max(...rightTexts.map((text) => approxSvgTextWidth(text, 12)));
    const minPlotW = 180;
    const maxSideW = Math.floor((W - minPlotW) / 2) - 18;
    const leftW = Math.min(maxSideW, Math.max(130, Math.ceil(maxLeftW)));
    const rightW = Math.min(maxSideW, Math.max(130, Math.ceil(maxRightW)));
    const colL = leftW + 14;
    const colR = W - rightW - 14;

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

    // Pass 1: compute dot Y for each item and the desired label Y (baseline + 4
    // so the text visually centers on the dot for 12px font).
    const lys = items.map((_, i) => yFor(leftValues[i]));
    const rys = items.map((_, i) => yFor(rightValues[i]));
    const labelLY = lys.map((y) => y + 4);
    const labelRY = rys.map((y) => y + 4);

    // Pass 2: anti-overlap each side independently. Dots stay at lys/rys; only
    // label Y positions get nudged when two values would collide. `maxLabelY`
    // keeps the descender of a 12px label inside the SVG viewBox so the pass
    // never clips a label off the bottom.
    const lineHeight = 14; // 12px font + ~2px breathing room.
    const maxLabelY = H - 4; // ~3px below the baseline is where the descender ends.
    antiOverlap(labelLY, lineHeight, maxLabelY);
    antiOverlap(labelRY, lineHeight, maxLabelY);

    items.forEach((_, i) => {
      const lv = leftValues[i];
      const rv = rightValues[i];
      const ly = lys[i];
      const ry = rys[i];
      const direction = rv > lv ? 'up' : rv < lv ? 'down' : 'flat';
      const delta = rv - lv;
      const pctChange = lv !== 0 ? ` · ${formatSignedNumber((delta / Math.abs(lv)) * 100, 1)}%` : '';
      const tooltipBody =
        `${leftLabel}: ${formatUnitValue(lv, unit)} -> ${rightLabel}: ${formatUnitValue(rv, unit)}` +
        ` · change ${formatSignedUnitValue(delta, unit)}${pctChange}`;
      const line = svgEl<SVGLineElement>('line', {
        class: `ara-slope-line ${direction !== 'flat' ? `ara-slope-line--${direction}` : ''}`.trim(),
        x1: colL + 6,
        y1: ly,
        x2: colR - 6,
        y2: ry,
      });
      svg.appendChild(line);
      const hit = svgEl<SVGLineElement>('line', {
        class: 'ara-slope-hit',
        x1: colL + 6,
        y1: ly,
        x2: colR - 6,
        y2: ry,
      });
      setAraTooltip(hit, items[i], tooltipBody);
      svg.appendChild(hit);
      const leftDot = svgEl('circle', { class: 'ara-slope-dot', cx: colL + 6, cy: ly, r: 3 });
      setAraTooltip(leftDot, items[i], `${leftLabel}: ${formatUnitValue(lv, unit)}`);
      svg.appendChild(leftDot);
      const rightDot = svgEl('circle', { class: 'ara-slope-dot', cx: colR - 6, cy: ry, r: 3 });
      setAraTooltip(rightDot, items[i], `${rightLabel}: ${formatUnitValue(rv, unit)}`);
      svg.appendChild(rightDot);
      const lRaw = leftTexts[i];
      const lLabel = svgEl<SVGTextElement>('text', { class: 'ara-slope-label', x: colL - 8, y: labelLY[i], 'text-anchor': 'end' });
      lLabel.textContent = fitSvgText(lRaw, colL - 8, 12);
      if (lLabel.textContent !== lRaw) setSvgFullLabel(lLabel, lRaw);
      setAraTooltip(lLabel, items[i], `${leftLabel}: ${formatUnitValue(lv, unit)}`);
      svg.appendChild(lLabel);
      const rRaw = rightTexts[i];
      const rLabel = svgEl<SVGTextElement>('text', { class: 'ara-slope-label', x: colR + 8, y: labelRY[i], 'text-anchor': 'start' });
      rLabel.textContent = fitSvgText(rRaw, W - colR - 8, 12);
      if (rLabel.textContent !== rRaw) setSvgFullLabel(rLabel, rRaw);
      setAraTooltip(rLabel, items[i], `${rightLabel}: ${formatUnitValue(rv, unit)}`);
      svg.appendChild(rLabel);
    });

    el.appendChild(svg);
    el.dataset.rendered = '1';
  }
}

/** Nice-number rounded tick marks across [min, max].
 *
 * Returns an evenly-spaced ascending list of "round" values (steps of
 * 1/2/5 × 10^k) that bracket the domain — niceTicks[0] <= min and the
 * last entry >= max. Because the chart always passes a domain that
 * includes 0 (bars originate from a zero baseline), and 0 is a multiple
 * of every step, the returned ticks always include 0 when the domain
 * spans it. Used for both the value axis labels and gridline positions. */
function niceTicks(min: number, max: number, maxTicks = 6): number[] {
  if (!Number.isFinite(min) || !Number.isFinite(max)) return [0, 1];
  if (min === max) {
    // Degenerate domain (e.g. all-zero series). Give a tiny symmetric range.
    if (min === 0) return [0, 1];
    min = Math.min(0, min);
    max = Math.max(0, max);
    if (min === max) return [min, min + 1];
  }
  const range = max - min;
  const rawStep = range / Math.max(1, maxTicks - 1);
  const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
  const norm = rawStep / mag;
  let niceNorm: number;
  if (norm < 1.5) niceNorm = 1;
  else if (norm < 3) niceNorm = 2;
  else if (norm < 7) niceNorm = 5;
  else niceNorm = 10;
  const step = niceNorm * mag;
  const niceMin = Math.floor(min / step) * step;
  const niceMax = Math.ceil(max / step) * step;
  const ticks: number[] = [];
  // Build with integer arithmetic on step counts to dodge float drift
  // (e.g. 0.1 + 0.2 != 0.3); the last push guards against the loop
  // missing niceMax by an epsilon.
  const count = Math.round((niceMax - niceMin) / step);
  for (let i = 0; i <= count; i++) {
    ticks.push(niceMin + i * step);
  }
  return ticks;
}

/** Bar / column chart with a real numeric value axis. Authored markup is
 * one empty <div class="ara-bar-chart" data-*> (the writer's tag allowlist
 * rejects <svg> in fragments) — we inject the SVG here. Supports:
 *   - vertical stacked / grouped columns
 *   - horizontal diverging bars (signed values around a zero baseline)
 *   - plain horizontal/vertical single-series bars
 * data-series-N use digit suffixes, so they are read with getAttribute
 * (data-series-1 does NOT map to dataset.series1). */
function renderBarCharts(root: HTMLElement): void {
  const els = root.querySelectorAll<HTMLElement>('.ara-bar-chart');
  for (const el of els) {
    if (el.dataset.rendered === '1') continue;

    const seriesList: Array<{ values: number[]; label: string }> = [];
    for (let i = 1; i <= 6; i++) {
      const v = parseSeries(el.getAttribute(`data-series-${i}`) || undefined, 200);
      if (!v.length) continue;
      const label = el.getAttribute(`data-series-${i}-label`) || `Series ${i}`;
      seriesList.push({ values: v, label });
    }
    if (!seriesList.length) continue;

    const categories = parseLabels(el.dataset.categories, 200);
    if (!categories.length) continue;
    const N = categories.length;
    // Clamp every series to the category count so a mismatched author
    // attr can't read past the slot array (compiler already enforces
    // equality, but the renderer must not trust that).
    for (const s of seriesList) {
      if (s.values.length < N) {
        while (s.values.length < N) s.values.push(0);
      } else if (s.values.length > N) {
        s.values = s.values.slice(0, N);
      }
    }

    const orientation = el.dataset.orientation === 'horizontal' ? 'horizontal' : 'vertical';
    const mode = el.dataset.mode || (seriesList.length > 1 ? 'grouped' : 'simple');
    const prefix = el.dataset.unit || '';
    const suffix = el.dataset.valueSuffix || '';
    const title = el.dataset.title || '';
    const subtitle = el.dataset.subtitle || '';
    const isStacked = mode === 'stacked' && seriesList.length > 1;
    const isGrouped = mode === 'grouped' && seriesList.length > 1;

    // Value formatter: signed prefix + abs value (grouped thousands) + suffix.
    // e.g. -8000 with prefix "$" suffix "M" → "-$8,000M".
    const fmt = (v: number): string => {
      const sign = v < 0 ? '-' : '';
      return sign + prefix + Math.abs(v).toLocaleString('en-US', { maximumFractionDigits: 2 }) + suffix;
    };

    // ── Value-axis domain ────────────────────────────────────────────
    // stacked: per-category total (all >=0 by validation) → [0, maxTotal].
    // grouped/simple: every individual value, ALWAYS including zero so bars
    // originate from a zero baseline.
    let domainMin: number;
    let domainMax: number;
    if (isStacked) {
      const totals = categories.map((_, ci) =>
        seriesList.reduce((acc, s) => acc + s.values[ci], 0),
      );
      domainMin = 0;
      domainMax = Math.max(0, ...totals);
    } else {
      const allValues = seriesList.flatMap((s) => s.values);
      domainMin = Math.min(0, ...allValues);
      domainMax = Math.max(0, ...allValues);
    }
    const ticks = niceTicks(domainMin, domainMax, 6);
    const niceMin = ticks[0];
    const niceMax = ticks[ticks.length - 1];
    const valRange = niceMax - niceMin || 1;

    el.textContent = '';
    if (title) {
      const t = document.createElement('p');
      t.className = 'ara-bar-chart-title';
      t.textContent = title;
      el.appendChild(t);
    }
    if (subtitle) {
      const s = document.createElement('p');
      s.className = 'ara-bar-chart-subtitle';
      s.textContent = subtitle;
      el.appendChild(s);
    }

    const colorClass = (catIdx: number, seriesIdx: number): string => {
      // multi-series → color by series; single → color by category.
      const n = seriesList.length > 1 ? seriesIdx + 1 : (catIdx % 6) + 1;
      return `ara-bar-chart-bar ara-bar-chart-bar--${n}`;
    };

    let svg: SVGSVGElement;

    if (orientation === 'vertical') {
      // Columns: value axis on Y (left), categories along X (bottom).
      const W = 640;
      const H = 300;
      const MT = 12;
      const MB = 34;
      const MR = 16;
      const tickLabels = ticks.map((t) => fmt(t));
      const maxTickW = Math.max(...tickLabels.map((t) => approxSvgTextWidth(t, 10, true)));
      const ML = Math.min(140, Math.max(44, Math.ceil(maxTickW) + 10));
      const innerW = W - ML - MR;
      const innerH = H - MT - MB;
      const yFor = (v: number) => MT + innerH - ((v - niceMin) / valRange) * innerH;
      const slotW = innerW / N;

      svg = svgEl<SVGSVGElement>('svg', {
        viewBox: `0 0 ${W} ${H}`,
        preserveAspectRatio: 'xMidYMid meet',
        role: 'img',
        'aria-label': `${title || 'Bar chart'}: hover bars for values`,
      });

      // Gridlines + value tick labels.
      for (let i = 0; i < ticks.length; i++) {
        const y = yFor(ticks[i]);
        svg.appendChild(svgEl('line', { class: 'ara-chart-grid', x1: ML, y1: y, x2: W - MR, y2: y }));
        const lab = svgEl<SVGTextElement>('text', { class: 'ara-chart-tick-label', x: ML - 6, y: y + 3, 'text-anchor': 'end' });
        lab.textContent = tickLabels[i];
        svg.appendChild(lab);
      }
      // Emphasized zero baseline (coincides with axis edge when all-positive).
      const yZero = yFor(0);
      svg.appendChild(svgEl('line', { class: 'ara-bar-chart-baseline', x1: ML, y1: yZero, x2: W - MR, y2: yZero }));

      // Sparse category labels if crowded.
      const labelStep = N > 8 ? Math.ceil(N / 8) : 1;

      categories.forEach((cat, ci) => {
        const slotX = ML + ci * slotW;
        if (isStacked) {
          // Accumulate segments upward from baseline (all values >= 0).
          let posTop = 0; // running total above baseline
          const barW = slotW * 0.6;
          const barX = slotX + (slotW - barW) / 2;
          seriesList.forEach((s, si) => {
            const v = s.values[ci];
            const segTopVal = posTop + v;
            const yTop = yFor(segTopVal);
            const yBot = yFor(posTop);
            const h = Math.abs(yBot - yTop);
            const rect = svgEl<SVGRectElement>('rect', {
              class: colorClass(ci, si),
              x: barX,
              y: Math.min(yTop, yBot),
              width: barW,
              height: h,
            });
            appendSvgTitle(rect, `${s.label} · ${cat}: ${fmt(v)}`);
            svg.appendChild(rect);
            posTop = segTopVal;
          });
        } else if (isGrouped) {
          // N series bars side-by-side within the slot.
          const groupPad = slotW * 0.12;
          const bandW = slotW - groupPad * 2;
          const barW = bandW / seriesList.length;
          seriesList.forEach((s, si) => {
            const v = s.values[ci];
            const barX = slotX + groupPad + si * barW;
            const yVal = yFor(v);
            const yTop = Math.min(yVal, yZero);
            const h = Math.abs(yZero - yVal);
            const rect = svgEl<SVGRectElement>('rect', {
              class: colorClass(ci, si),
              x: barX + 0.5,
              y: yTop,
              width: Math.max(0, barW - 1),
              height: h,
            });
            appendSvgTitle(rect, `${s.label} · ${cat}: ${fmt(v)}`);
            svg.appendChild(rect);
          });
        } else {
          // simple: one bar per slot, centered.
          const v = seriesList[0].values[ci];
          const barW = slotW * 0.6;
          const barX = slotX + (slotW - barW) / 2;
          const yVal = yFor(v);
          const yTop = Math.min(yVal, yZero);
          const h = Math.abs(yZero - yVal);
          const rect = svgEl<SVGRectElement>('rect', {
            class: colorClass(ci, 0),
            x: barX,
            y: yTop,
            width: barW,
            height: h,
          });
          appendSvgTitle(rect, `${cat}: ${fmt(v)}`);
          svg.appendChild(rect);
        }

        // Category label under the slot (centered), sparse if crowded.
        if (ci % labelStep === 0) {
          const raw = cat;
          const fitted = fitSvgText(raw, slotW * (labelStep > 1 ? labelStep : 1) - 4, 10);
          const lab = svgEl<SVGTextElement>('text', {
            class: 'ara-chart-tick-label',
            x: slotX + slotW / 2,
            y: H - 12,
            'text-anchor': 'middle',
          });
          lab.textContent = fitted;
          if (fitted !== raw) setSvgFullLabel(lab, raw);
          svg.appendChild(lab);
        }
      });

      el.appendChild(svg);
    } else {
      // Horizontal bars: value axis along X (bottom), categories as Y rows.
      const W = 640;
      const rowH = 40;
      const MT = 12;
      const MB = 30;
      const MR = 18;
      const tickLabels = ticks.map((t) => fmt(t));
      const maxCatW = Math.max(...categories.map((c) => approxSvgTextWidth(c, 12)));
      const ML = Math.min(220, Math.max(60, Math.ceil(maxCatW) + 14));
      const H = MT + N * rowH + MB;
      const innerW = W - ML - MR;
      const innerH = N * rowH;
      const xFor = (v: number) => ML + ((v - niceMin) / valRange) * innerW;

      svg = svgEl<SVGSVGElement>('svg', {
        viewBox: `0 0 ${W} ${H}`,
        preserveAspectRatio: 'xMidYMid meet',
        role: 'img',
        'aria-label': `${title || 'Bar chart'}: hover bars for values`,
      });

      // Vertical gridlines + value tick labels along the bottom.
      for (let i = 0; i < ticks.length; i++) {
        const x = xFor(ticks[i]);
        svg.appendChild(svgEl('line', { class: 'ara-chart-grid', x1: x, y1: MT, x2: x, y2: MT + innerH }));
        const lab = svgEl<SVGTextElement>('text', { class: 'ara-chart-tick-label', x, y: H - 12, 'text-anchor': 'middle' });
        lab.textContent = tickLabels[i];
        svg.appendChild(lab);
      }
      // Emphasized zero baseline (vertical).
      const xZero = xFor(0);
      svg.appendChild(svgEl('line', { class: 'ara-bar-chart-baseline', x1: xZero, y1: MT, x2: xZero, y2: MT + innerH }));

      categories.forEach((cat, ci) => {
        const rowY = MT + ci * rowH;
        if (isStacked) {
          let posRight = 0; // running total (all >= 0)
          const barH = rowH * 0.6;
          const barY = rowY + (rowH - barH) / 2;
          seriesList.forEach((s, si) => {
            const v = s.values[ci];
            const xStart = xFor(posRight);
            const xEnd = xFor(posRight + v);
            const w = Math.abs(xEnd - xStart);
            const rect = svgEl<SVGRectElement>('rect', {
              class: colorClass(ci, si),
              x: Math.min(xStart, xEnd),
              y: barY,
              width: w,
              height: barH,
            });
            appendSvgTitle(rect, `${s.label} · ${cat}: ${fmt(v)}`);
            svg.appendChild(rect);
            posRight += v;
          });
        } else if (isGrouped) {
          const groupPad = rowH * 0.12;
          const bandH = rowH - groupPad * 2;
          const barH = bandH / seriesList.length;
          seriesList.forEach((s, si) => {
            const v = s.values[ci];
            const barY = rowY + groupPad + si * barH;
            const xVal = xFor(v);
            const xStart = Math.min(xVal, xZero);
            const w = Math.abs(xVal - xZero);
            const rect = svgEl<SVGRectElement>('rect', {
              class: colorClass(ci, si),
              x: xStart,
              y: barY + 0.5,
              width: w,
              height: Math.max(0, barH - 1),
            });
            appendSvgTitle(rect, `${s.label} · ${cat}: ${fmt(v)}`);
            svg.appendChild(rect);
          });
        } else {
          const v = seriesList[0].values[ci];
          const barH = rowH * 0.6;
          const barY = rowY + (rowH - barH) / 2;
          const xVal = xFor(v);
          const xStart = Math.min(xVal, xZero);
          const w = Math.abs(xVal - xZero);
          const rect = svgEl<SVGRectElement>('rect', {
            class: colorClass(ci, 0),
            x: xStart,
            y: barY,
            width: w,
            height: barH,
          });
          appendSvgTitle(rect, `${cat}: ${fmt(v)}`);
          svg.appendChild(rect);
        }

        // Right-aligned category label in the left margin, vertically centered.
        const raw = cat;
        const fitted = fitSvgText(raw, ML - 10, 12);
        const lab = svgEl<SVGTextElement>('text', {
          class: 'ara-chart-tick-label',
          x: ML - 8,
          y: rowY + rowH / 2 + 4,
          'text-anchor': 'end',
        });
        lab.textContent = fitted;
        if (fitted !== raw) setSvgFullLabel(lab, raw);
        svg.appendChild(lab);
      });

      el.appendChild(svg);
    }

    // Legend (only for multi-series). Reuses the line-chart legend item
    // swatch pattern; scoped CSS gives the bar-chart its own block fill.
    if (seriesList.length > 1) {
      const legend = document.createElement('div');
      legend.className = 'ara-bar-chart-legend';
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
      languageFallbackNote(row),
      researchAudioControlsHtml(row),
      '    <a class="gen-research-fullscreen" href="' + escapeHtml(src) + '" target="_blank" rel="noopener noreferrer">Open full ↗</a>',
      '  </div>',
      '  <iframe class="gen-research-iframe" src="' + escapeHtml(src) + '" sandbox="allow-scripts" loading="lazy" title="' + escapeHtml(row.title) + '"></iframe>',
      '</div>',
    ].join('\n'),
  );
  setDocTitle(row.title);
  updateResearchAudioUi();
}

// ── Main load ─────────────────────────────────────────
async function load(): Promise<void> {
  const dateStr = fmtDate(currentDate);
  const requestId = ++loadRequestId;
  if (activeLoadController) activeLoadController.abort();
  const controller = new AbortController();
  activeLoadController = controller;
  stopResearchAudio();

  // Hide the floating TOC unconditionally; renderResearchDoc shows it
  // again when it has enough sections to be useful.
  hideResearchTOC();

  updateRoute();
  showLoading();

  try {
    if (activeTab === 'wiki') {
      // Fetch + cache the committed index.json once; everything (catalog,
      // backlinks, resolver) is derived from it. No JS-side graph building.
      const idx = await withTimeout(loadWikiIndex(controller.signal), LOAD_TIMEOUT_MS, controller);
      if (requestId !== loadRequestId) return;
      if (idx === 'timeout') {
        showError('Loading timed out', 'Network may be slow. Click to retry.');
      } else if (!idx) {
        showError('Wiki unavailable', 'Could not load the wiki index. Click to retry.');
      } else if (!selectedSlug) {
        renderWikiIndex(idx);
      } else {
        const page = wikiPageMap.get(selectedSlug);
        if (!page) {
          renderWikiNotFound(selectedSlug);
        } else {
          const cached = wikiBodyCache.get(selectedSlug);
          if (cached !== undefined) {
            renderWikiPage(page, cached);
          } else {
            const body = await withTimeout(
              fetchMarkdownReport(`${DATA_BASE}/wiki/${page.file}`, controller.signal),
              LOAD_TIMEOUT_MS,
              controller,
            );
            if (requestId !== loadRequestId) return;
            if (body === 'timeout') {
              showError('Loading timed out', 'Network may be slow. Click to retry.');
            } else if (body) {
              wikiBodyCache.set(selectedSlug, body);
              renderWikiPage(page, body);
            } else {
              renderWikiNotFound(selectedSlug);
            }
          }
        }
      }
    } else if (activeTab === 'research') {
      // Make sure the manifest (and therefore the generative index) is loaded.
      const m = manifest || await loadManifest();
      if (requestId !== loadRequestId) return;
      const rows = m?.generative ?? [];
      if (!selectedSlug) {
        researchDocCache = null;
        syncLanguageUi(null);
        renderResearchIndex(rows);
      } else {
        const row = findResearchRow(selectedSlug);
        if (!row) {
          syncLanguageUi(null);
          showEmpty(dateStr);
        } else {
          syncLanguageUi(row);
          const variant = researchVariant(row, activeLanguage);
          if (variant.kind === 'standalone') {
            // Standalone docs render as an iframe; no body fetch needed.
            researchDocCache = null;
            renderResearchStandalone(variant);
          } else if (
            researchDocCache &&
            researchDocCache.slug === selectedSlug &&
            researchDocCache.language === activeLanguage
          ) {
            renderResearchDoc(variant, researchDocCache.body);
          } else {
            const result = await withTimeout(fetchResearchDoc(variant, controller.signal), LOAD_TIMEOUT_MS, controller);
            if (requestId !== loadRequestId) return;
            if (result === 'timeout') {
              showError('Loading timed out', 'Network may be slow. Click to retry.');
            } else if (result) {
              researchDocCache = { slug: selectedSlug, language: activeLanguage, body: result };
              renderResearchDoc(variant, result);
            } else {
              showEmpty(dateStr);
            }
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
      // Model timeline is now a ticket grid (one card per release/event).
      // The legacy <date>-timeline.md files still exist on disk for
      // back-compat; once the CRUD agent runs we'll surface daily diffs
      // by date here too. For now, models tab always shows tickets.
      const ticketsResult = await withTimeout(loadTickets(), LOAD_TIMEOUT_MS, controller);
      if (requestId !== loadRequestId) return;
      if (ticketsResult === 'timeout') {
        showError('Loading timed out', 'Network may be slow. Click to retry.');
      } else {
        renderTickets(ticketsResult);
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
        renderTwitterReport(result);
      } else {
        const fallback = findMostRecentAvailable('twitter', dateStr);
        if (fallback && fallback !== dateStr) {
          const fallbackMd = await fetchTwitter(fallback, controller.signal);
          if (requestId !== loadRequestId) return;
          if (fallbackMd) {
            renderTwitterReport(fallbackMd, fallback);
          } else {
            showEmpty(dateStr);
          }
        } else {
          showEmpty(dateStr);
        }
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
window.addEventListener('beforeunload', () => stopResearchAudio());

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

languageSwitch.addEventListener('click', (e) => {
  const btn = (e.target as HTMLElement).closest('[data-language]') as HTMLButtonElement | null;
  if (!btn) return;
  const language = btn.dataset.language === 'ko' ? 'ko' : 'en';
  if (language === activeLanguage) return;
  activeLanguage = language;
  storeLanguage(activeLanguage);
  researchDocCache = null;
  syncLanguageUi(selectedSlug ? findResearchRow(selectedSlug) : null);
  load();
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
  if (target.closest('[data-research-file-audio-toggle]')) {
    void toggleResearchFileAudio();
    return;
  }
  if (target.closest('[data-research-audio-toggle]')) {
    void toggleResearchAudio();
    return;
  }
  if (target.closest('[data-research-audio-stop]')) {
    stopResearchAudio();
    return;
  }
  // Wiki "back to all pages" / "back to wiki" buttons.
  const wikiBack = target.closest('[data-wiki-back]') as HTMLElement | null;
  if (wikiBack) {
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
  // Ticket status filter pills (only meaningful on the models tab).
  if (activeTab === 'models') {
    const statusPill = target.closest('[data-filter-status]') as HTMLElement | null;
    if (statusPill) {
      ticketFilters.status = statusPill.dataset.filterStatus || 'all';
      load();
      return;
    }
  }
  // Wiki internal links ([[wikilinks]] rendered as <a data-wiki-slug>) — intercept
  // for instant SPA nav so a click never triggers a full page reload. Mirror the
  // research [data-slug] branch. Placed before the [data-slug] lookup; they use
  // distinct attributes so there's no collision, but ordering keeps intent clear.
  const wikiAnchor = target.closest('[data-wiki-slug]') as HTMLElement | null;
  if (wikiAnchor && activeTab === 'wiki') {
    const slug = wikiAnchor.dataset.wikiSlug;
    if (slug) {
      e.preventDefault();
      selectedSlug = slug;
      // load() calls updateRoute() first thing, which pushState's /wiki/<slug>;
      // no full reload. Mirrors the research [data-slug] branch.
      load();
    }
    return;
  }
  const row = target.closest('[data-slug]') as HTMLElement | null;
  if (row && activeTab === 'research') {
    const slug = row.dataset.slug;
    if (slug) {
      selectedSlug = slug;
      load();
    }
    return;
  }
  if (row && activeTab === 'models') {
    // Don't toggle on link clicks inside the card — let them open.
    if (target.closest('a, button')) return;
    const slug = row.dataset.slug;
    if (slug) {
      expandedTicketSlug = expandedTicketSlug === slug ? null : slug;
      if (ticketsCache) renderTickets(ticketsCache);
    }
  }
});

// Company-filter <select> on the tickets view.
content.addEventListener('change', (e) => {
  const target = e.target as HTMLElement;
  if (activeTab !== 'models') return;
  const sel = target.closest('[data-filter-company]') as HTMLSelectElement | null;
  if (!sel) return;
  ticketFilters.company = sel.value;
  load();
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
    syncTabUi();
    document.body.classList.toggle('tab-research', activeTab === 'research');
    document.body.classList.toggle('tab-models', activeTab === 'models');
    document.body.classList.toggle('tab-wiki', activeTab === 'wiki');
    // Re-probe availability for current month with new tab (date tabs only).
    // The models/wiki tabs don't use date routing, so skip probing there too —
    // it'd just paint dots on a calendar that's hidden anyway.
    if (activeTab !== 'research' && activeTab !== 'models' && activeTab !== 'wiki') {
      probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
    }
    load();
  });
});

// ── Init ──────────────────────────────────────────────
calendarEl.addEventListener('click', handleCalendarClick);
syncLanguageUi(null);
// Kick off manifest fetch early so calendar + fallback logic have data ASAP.
loadManifest();
applyRoute();
// applyRoute() may have mutated activeTab to anything in Tab; TS won't see
// that across the function boundary, so we widen the read explicitly.
const currentTab: Tab = activeTab as Tab;
document.body.classList.toggle('tab-research', currentTab === 'research');
document.body.classList.toggle('tab-models', currentTab === 'models');
document.body.classList.toggle('tab-wiki', currentTab === 'wiki');
if (currentTab !== 'research' && currentTab !== 'models' && currentTab !== 'wiki') {
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
