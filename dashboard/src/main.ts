import './style.css';
import { Marked } from 'marked';
import type { Tokens, TokenizerThis } from 'marked';
import DOMPurify from 'dompurify';
import {
  cleanPublicLeadText,
  escapeHtml,
  extractUrls,
  renderReportMarkdown,
  splitSections,
  stripMarkdown,
  truncateText,
  wrapTables,
} from './render/shared';
import { renderAgentsStudioHtml } from './render/agents';
import { renderTodayHtml } from './render/today';
import {
  parseTwitterStories,
  renderTwitterReportHtml,
  sanitizePublicReportMarkdown,
  storyCurrentLead,
} from './render/twitter';
import type { TwitterStory } from './render/twitter';
import {
  closeAraFigureModal,
  enhanceAraArticle,
  enhanceAraVisuals,
  hideResearchTOC,
  openAraFigureModal,
  scrollToHashIfPresent,
} from './ara-enhance';

const DATA_BASE: string = import.meta.env.BASE_URL + 'research';

// Audio files live in S3 (s3.guzus.xyz), not in research/audio/. The mp3s in
// the repo are 0-byte stubs that exist so prebuild.mjs's manifest pipeline
// keeps surfacing which dates have audio. Override via VITE_AUDIO_BASE_URL.
const AUDIO_BASE: string =
  import.meta.env.VITE_AUDIO_BASE_URL || 'https://s3.guzus.xyz/obj-ai-research-arm';

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
type Tab = 'today' | 'twitter' | 'models' | 'frontpage' | 'research' | 'wiki' | 'focusReader' | 'agents';
// Tabs that route by date (calendar-driven). research + wiki are slug-driven
// (or index views) and are excluded — mirror the research precedent.
type DateTab = Exclude<Tab, 'research' | 'wiki' | 'focusReader' | 'agents'>;
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
type FrontPageAsset = {
  url: string;
  html: string | null;
  fallback: string | null;
};
type FocusReaderItem = {
  title: string;
  label: string;
  summary: string;
  body: string;
  minutes: number;
  sources: string[];
  signal: string;
  score: number;
};
type FocusReaderData = {
  date: string;
  digestDate: string;
  generatedAt: string | null;
  items: FocusReaderItem[];
  digestCount: number;
  researchCount: number;
  ticketCount: number;
  activeTicketCount: number;
  wikiCount: number;
  latestResearchTitle: string;
  frontend: DesignFrontendData;
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
type DesignSurface = 'digest' | 'signals' | 'models' | 'research' | 'wiki';
type DesignFrontendData = {
  digestDate: string | null;
  twitterDate: string | null;
  digestItems: FocusReaderItem[];
  twitterStories: TwitterStory[];
  tickets: Ticket[];
  researchRows: GenResearchRow[];
  wikiPages: WikiPage[];
};

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
let focusReaderData: FocusReaderData | null = null;
let focusReaderSelectedIndex = 0;
let focusReaderSearchTerm = '';
let focusReaderSurface: DesignSurface = 'digest';
// Which ticket is expanded (showing body + history). Null = grid view.
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

type DigestAudioState = {
  date: string | null;
  src: string | null;
  title: string;
  dismissedSrc: string | null;
};

const digestAudioState: DigestAudioState = {
  date: null,
  src: null,
  title: 'Daily Digest',
  dismissedSrc: null,
};

let digestAudioEl: HTMLAudioElement | null = null;
let digestAudioBarEl: HTMLElement | null = null;
let digestAudioPlayEl: HTMLButtonElement | null = null;
let digestAudioTitleEl: HTMLButtonElement | null = null;
let digestAudioTimeEl: HTMLElement | null = null;
let digestAudioProgressEl: HTMLInputElement | null = null;
let lastDigestAudioBarActivation = 0;
let lastInlineDigestAudioActivation = 0;

// ── DOM refs ──────────────────────────────────────────
const content = document.getElementById('content')!;
const calendarEl = document.getElementById('calendar')!;
const searchInput = document.getElementById('searchInput') as HTMLInputElement;
const searchCountEl = document.getElementById('searchCount')!;
const languageSwitch = document.getElementById('languageSwitch');

// ── Path routing ─────────────────────────────────────
// Format (history API, no hash):
//   date tabs:  /tab/YYYY-MM-DD  e.g. /models/2026-02-03, /twitter/2026-01-29
//   research:   /research        (index list)
//               /research/<slug> (single doc)
// Static fetches under /research/... (manifest.json, generative/*.html, etc.)
// are disambiguated from routes by the file extension; Vercel rewrites only
// extensionless paths to /index.html.
function routeFromState(): string {
  if (activeTab === 'focusReader') {
    return '/design/focus-reader';
  }
  if (activeTab === 'agents') {
    return '/agents';
  }
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
  if (trimmed === 'design/focus-reader') {
    activeTab = 'focusReader';
    selectedSlug = null;
    syncTabUi();
    return true;
  }
  if (trimmed === 'agents') {
    activeTab = 'agents';
    selectedSlug = null;
    syncTabUi();
    return true;
  }
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
    const tabButton = b as HTMLElement;
    const isActive = tabButton.dataset.tab === activeTab;
    tabButton.classList.toggle('active', isActive);
  });
  const activeTabButton = document.querySelector<HTMLElement>('.tab.active');
  if (activeTabButton) {
    const activeButton = activeTabButton;
    const revealActiveTab = () => {
      const tabs = document.getElementById('tabs');
      if (!tabs) return;
      const target =
        activeButton.offsetLeft - (tabs.clientWidth - activeButton.offsetWidth) / 2;
      tabs.scrollLeft = Math.max(0, target);
    };
    requestAnimationFrame(revealActiveTab);
    window.setTimeout(revealActiveTab, 120);
  }
  document.body.classList.toggle('tab-today', activeTab === 'today');
  document.body.classList.toggle('tab-research', activeTab === 'research');
  document.body.classList.toggle('tab-frontpage', activeTab === 'frontpage');
  // Models tab shows the ticket grid (no date routing); the calendar
  // would just be dead UI on this tab. Same toggle pattern as research.
  document.body.classList.toggle('tab-models', activeTab === 'models');
  // Wiki is slug/index-driven, not date-driven — same calendar-hiding
  // toggle as research/models.
  document.body.classList.toggle('tab-wiki', activeTab === 'wiki');
  document.body.classList.toggle('tab-focus-reader', activeTab === 'focusReader');
  document.body.classList.toggle('tab-agents', activeTab === 'agents');
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
  if (!languageSwitch) return;  // language toggle removed (English-only for now)
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

/** A dated artifact (digest/twitter/front-page for `YYYY-MM-DD`) is treated as
 * immutable — and therefore safe to serve straight from the HTTP cache without
 * a forced revalidation round-trip — only when its date is comfortably in the
 * past. We keep a one-day buffer (strictly before *yesterday*, local time) so
 * timezone skew between the viewer's local clock and the pipeline's UTC write
 * schedule can never cause a still-updating "today"/"yesterday" file (the
 * digest regenerates daily; the twitter report rewrites every few hours) to be
 * mistakenly cached. Today's and yesterday's files keep `cache: 'no-cache'`. */
function isImmutableDate(dateStr: string): boolean {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  return dateStr < fmtDate(yesterday);
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
      // `digest` is a legacy alias for `today` that older manifests emitted;
      // it's not part of the current Manifest shape, so type the parsed object
      // as Partial<Manifest> plus that one optional legacy key rather than
      // reaching for `as any`.
      const m = (await resp.json()) as Partial<Manifest> & { digest?: unknown };
      // Normalize: ensure all sources have an array
      const normalized: Manifest = {
        today: Array.isArray(m.today) ? m.today : (Array.isArray(m.digest) ? m.digest : []),
        twitter: Array.isArray(m.twitter) ? m.twitter : [],
        models: Array.isArray(m.models) ? m.models : [],
        frontpage: Array.isArray(m.frontpage) ? m.frontpage : [],
        audio: Array.isArray(m.audio) ? m.audio : [],
        generative: Array.isArray(m.generative) ? m.generative : [],
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
  let html = '<div class="cal-header" data-cal-toggle>';
  html += '<span class="cal-header-label">' + monthLabel + '<span class="cal-chevron">' + (open ? '&#9650;' : '&#9660;') + '</span></span>';
  html += '</div>';

  // Month nav + day grid live in a popover so the pill keeps a fixed size.
  html += '<div class="cal-pop">';
  html += '<div class="cal-header-nav">';
  html += '<button class="cal-nav-btn" data-cal-nav="-1">&lsaquo;</button>';
  html += '<button class="cal-today-btn" data-cal-today>Today</button>';
  html += '<button class="cal-nav-btn" data-cal-nav="1">&rsaquo;</button>';
  html += '</div>';

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
  html += '</div>';
  return html;
}

// The picker popover is position:fixed (so it escapes the .tabs overflow clip);
// position it under the pill in viewport coords after each render.
function positionCalPop(): void {
  const pop = calendarEl.querySelector<HTMLElement>('.cal-pop');
  const header = calendarEl.querySelector<HTMLElement>('.cal-header');
  if (!pop || !header) return;
  const r = header.getBoundingClientRect();
  pop.style.top = (r.bottom + 8) + 'px';
  pop.style.left = Math.max(8, Math.min(r.left, window.innerWidth - 296)) + 'px';
}

function renderCalendar(): void {
  setSafeCalendar(calendarEl, buildCalendarHtml());
  if (calendarEl.classList.contains('open')) positionCalPop();
}

// Close the picker on scroll — the pill isn't sticky, so a fixed popover would
// otherwise detach from it.
window.addEventListener('scroll', () => {
  if (calendarEl.classList.contains('open')) {
    calendarEl.classList.remove('open');
    renderCalendar();
  }
}, true);

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
    // The pill is a date picker: clicking it opens the calendar from any tab;
    // picking a day (cal-day handler) then opens that day's digest/newspaper.
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
    activeTab = 'today';
    syncTabUi();
    calendarMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
    load();
    return;
  }

  const dayEl = target.closest('.cal-day') as HTMLElement | null;
  if (dayEl && dayEl.dataset.date) {
    const parts = dayEl.dataset.date.split('-');
    currentDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
    activeTab = 'today';                 // picking a date opens that day's view
    syncTabUi();
    calendarEl.classList.remove('open');
    const clickedMonth = new Date(+parts[0], +parts[1] - 1, 1);
    if (clickedMonth.getTime() !== calendarMonth.getTime()) {
      calendarMonth = clickedMonth;
      probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
    }
    load();
  }
}

/** Safely set element content using DOMPurify + insertAdjacentHTML.
 *
 * By default `iframe` is FORBIDDEN. Almost everything that flows through here
 * is LLM-synthesized and/or sourced from adversarial inputs (the daily digest,
 * the Twitter report, model tickets, the gen-research article body) and none
 * of it passes the fragment validator — so an injected raw `<iframe>` must not
 * survive (clickjacking/redress/referrer-leak via an un-sandboxed external
 * frame; inline JS is already stripped). This mirrors `setSafeWikiContent`
 * below, which likewise forbids iframe.
 *
 * The ONE trusted exception is the standalone research-doc view, which embeds
 * its own iframe that *we* construct with a sandboxed (`sandbox="allow-scripts"`,
 * no `allow-same-origin`) escapeHtml'd src. That single call site passes
 * `{ allowIframe: true }`; it is the only caller permitted to. The iframe
 * still renders THROUGH this sanitizer, so the allowance is opt-in rather
 * than a bypass. */
function setSafeContent(
  el: HTMLElement,
  rawHtml: string,
  opts: { allowIframe?: boolean } = {},
): void {
  while (el.firstChild) el.removeChild(el.firstChild);
  // `src`/`loading`/`decoding`/`controls`/`preload` serve the <audio>/<img>
  // elements that also flow through here (front-page image, digest/article
  // audio players), so they stay in the default allowlist; they are NOT
  // iframe-only.
  const addTags = ['mark', 'article', 'figure', 'figcaption', 'audio', 'nav', 'section', 'details', 'summary'];
  const addAttr = ['id', 'href', 'type', 'data-slug', 'data-focus-index', 'data-pct', 'data-paper-date', 'data-columns', 'data-filter-status', 'data-filter-company', 'data-has-audio-file', 'data-digest-audio-play', 'data-digest-audio-label', 'data-audio-date', 'aria-label', 'aria-current', 'aria-expanded', 'aria-controls', 'aria-pressed', 'loading', 'decoding', 'controls', 'preload', 'src', 'max', 'value'];
  if (opts.allowIframe) {
    // iframe + its iframe-only attributes are re-enabled exclusively for the
    // trusted, self-constructed sandboxed standalone-doc iframe.
    addTags.push('iframe');
    addAttr.push('sandbox', 'allow', 'referrerpolicy');
  }
  const clean = DOMPurify.sanitize(rawHtml, {
    USE_PROFILES: { html: true, svg: true, svgFilters: true },
    ADD_TAGS: addTags,
    ADD_ATTR: addAttr,
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
  return row.audio_file ? `${AUDIO_BASE}/${row.audio_file}` : null;
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

function dateFromString(dateStr: string): Date | null {
  const parts = dateStr.split('-');
  if (parts.length !== 3) return null;
  const date = new Date(+parts[0], +parts[1] - 1, +parts[2]);
  return Number.isNaN(date.getTime()) ? null : date;
}

function digestAudioUrl(dateStr: string): string {
  return `${AUDIO_BASE}/audio/${dateStr}-digest.mp3`;
}

function digestAudioTitle(dateStr: string): string {
  const date = dateFromString(dateStr);
  return `Daily Digest · ${date ? displayDate(date) : dateStr}`;
}

function ensureDigestAudioPlayer(): HTMLAudioElement {
  if (digestAudioEl) return digestAudioEl;

  const bar = document.createElement('aside');
  bar.id = 'digestAudioBar';
  bar.className = 'digest-audio-bar';
  bar.hidden = true;
  bar.setAttribute('aria-label', 'Daily digest audio player');
  bar.innerHTML = [
    '<audio preload="metadata"></audio>',
    '<div class="digest-audio-shell">',
    '  <button class="digest-audio-toggle" type="button" data-digest-audio-toggle aria-label="Play digest audio" aria-pressed="false">',
    '    <span class="digest-audio-toggle-icon" aria-hidden="true"></span>',
    '  </button>',
    '  <button class="digest-audio-title" type="button" data-digest-audio-title>Daily Digest</button>',
    '  <span class="digest-audio-time" data-digest-audio-time aria-live="off">0:00 / --:--</span>',
    '  <input class="digest-audio-progress" data-digest-audio-progress type="range" min="0" max="1000" value="0" step="1" aria-label="Seek digest audio">',
    '  <button class="digest-audio-close" type="button" data-digest-audio-close aria-label="Close audio player">&times;</button>',
    '</div>',
  ].join('\n');
  document.body.appendChild(bar);

  digestAudioBarEl = bar;
  digestAudioEl = bar.querySelector('audio');
  digestAudioPlayEl = bar.querySelector('[data-digest-audio-toggle]');
  digestAudioTitleEl = bar.querySelector('[data-digest-audio-title]');
  digestAudioTimeEl = bar.querySelector('[data-digest-audio-time]');
  digestAudioProgressEl = bar.querySelector('[data-digest-audio-progress]');

  if (!digestAudioEl || !digestAudioPlayEl || !digestAudioTitleEl || !digestAudioTimeEl || !digestAudioProgressEl) {
    throw new Error('Digest audio player failed to initialize');
  }

  const activateBarToggle = (event: Event) => {
    event.preventDefault();
    event.stopPropagation();
    const now = Date.now();
    if (now - lastDigestAudioBarActivation < 250) return;
    lastDigestAudioBarActivation = now;
    void toggleDigestAudioPlayback();
  };
  digestAudioPlayEl.addEventListener('pointerup', activateBarToggle);
  digestAudioPlayEl.addEventListener('click', activateBarToggle);
  digestAudioPlayEl.addEventListener('keydown', (event) => {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    activateBarToggle(event);
  });
  digestAudioTitleEl.addEventListener('click', navigateToDigestAudioDate);
  digestAudioProgressEl.addEventListener('input', () => {
    const audio = ensureDigestAudioPlayer();
    const duration = Number.isFinite(audio.duration) ? audio.duration : 0;
    if (duration <= 0) return;
    const next = Number(digestAudioProgressEl?.value || 0) / 1000;
    audio.currentTime = duration * Math.max(0, Math.min(1, next));
  });
  bar.querySelector('[data-digest-audio-close]')?.addEventListener('click', closeDigestAudioPlayer);

  digestAudioEl.addEventListener('loadedmetadata', updateDigestAudioUi);
  digestAudioEl.addEventListener('durationchange', updateDigestAudioUi);
  digestAudioEl.addEventListener('timeupdate', updateDigestAudioUi);
  digestAudioEl.addEventListener('play', updateDigestAudioUi);
  digestAudioEl.addEventListener('pause', updateDigestAudioUi);
  digestAudioEl.addEventListener('ended', () => {
    hideDigestAudioPlayer();
    updateDigestAudioUi();
  });
  digestAudioEl.addEventListener('error', () => {
    if (digestAudioTitleEl) digestAudioTitleEl.textContent = `${digestAudioState.title} · unavailable`;
    updateDigestAudioUi();
  });

  return digestAudioEl;
}

function showDigestAudioPlayer(): void {
  ensureDigestAudioPlayer();
  if (digestAudioBarEl) digestAudioBarEl.hidden = false;
  document.body.classList.add('has-digest-player');
}

function hideDigestAudioPlayer(): void {
  if (digestAudioBarEl) digestAudioBarEl.hidden = true;
  document.body.classList.remove('has-digest-player');
}

function setDigestAudioTrack(dateStr: string, autoplay: boolean): void {
  const audio = ensureDigestAudioPlayer();
  const src = digestAudioUrl(dateStr);
  const changed = digestAudioState.src !== src || audio.getAttribute('src') !== src;
  digestAudioState.date = dateStr;
  digestAudioState.src = src;
  digestAudioState.title = digestAudioTitle(dateStr);
  digestAudioState.dismissedSrc = null;
  if (changed) {
    audio.src = src;
    audio.currentTime = 0;
    audio.load();
  }
  showDigestAudioPlayer();
  updateDigestAudioUi();
  if (autoplay) {
    stopResearchAudio();
    void audio.play().catch(() => {
      updateDigestAudioUi();
    });
  }
}

function syncDigestAudioForDate(dateStr: string): void {
  if (!manifest?.audio.includes(dateStr)) {
    updateDigestAudioUi();
    return;
  }
  const src = digestAudioUrl(dateStr);
  const audio = digestAudioEl;
  const hasActivePlayback = audio !== null && Boolean(digestAudioState.src) && !audio.paused && !audio.ended;
  if (hasActivePlayback && digestAudioState.src !== src) {
    updateDigestAudioUi();
    return;
  }
  if (digestAudioState.src !== src) {
    if (digestAudioState.dismissedSrc === src) {
      updateDigestAudioUi();
      return;
    }
    digestAudioState.date = dateStr;
    digestAudioState.src = src;
    digestAudioState.title = digestAudioTitle(dateStr);
    if (audio) {
      audio.src = src;
      audio.currentTime = 0;
      audio.load();
    }
  }
  updateDigestAudioUi();
}

async function toggleDigestAudioPlayback(dateStr: string | null = digestAudioState.date): Promise<void> {
  if (!dateStr) return;
  const audio = ensureDigestAudioPlayer();
  const src = digestAudioUrl(dateStr);
  if (digestAudioState.src !== src || audio.getAttribute('src') !== src) {
    setDigestAudioTrack(dateStr, true);
    return;
  }
  digestAudioState.dismissedSrc = null;
  showDigestAudioPlayer();
  if (audio.paused || audio.ended) {
    stopResearchAudio();
    try {
      await audio.play();
    } catch {
      updateDigestAudioUi();
    }
  } else {
    audio.pause();
  }
  updateDigestAudioUi();
}

function closeDigestAudioPlayer(): void {
  const audio = ensureDigestAudioPlayer();
  if (digestAudioState.src) digestAudioState.dismissedSrc = digestAudioState.src;
  audio.pause();
  hideDigestAudioPlayer();
  updateDigestAudioUi();
}

function navigateToDigestAudioDate(): void {
  if (!digestAudioState.date) return;
  const date = dateFromString(digestAudioState.date);
  if (!date) return;
  currentDate = date;
  activeTab = 'today';
  selectedSlug = null;
  calendarMonth = new Date(date.getFullYear(), date.getMonth(), 1);
  syncTabUi();
  probeAvailability(calendarMonth.getFullYear(), calendarMonth.getMonth());
  load();
}

function updateDigestAudioUi(): void {
  const audio = digestAudioEl;
  const src = digestAudioState.src;
  const isPlaying = Boolean(audio && src && !audio.paused && !audio.ended);
  const duration = audio && Number.isFinite(audio.duration) ? audio.duration : 0;
  const current = audio ? audio.currentTime : 0;
  const pct = duration > 0 ? Math.round((current / duration) * 1000) : 0;
  const label = isPlaying ? 'Pause digest audio' : 'Play digest audio';

  if (digestAudioPlayEl) {
    digestAudioPlayEl.setAttribute('aria-label', label);
    digestAudioPlayEl.setAttribute('aria-pressed', String(isPlaying));
    digestAudioPlayEl.classList.toggle('is-playing', isPlaying);
  }
  if (digestAudioTitleEl) digestAudioTitleEl.textContent = digestAudioState.title;
  if (digestAudioTimeEl) {
    digestAudioTimeEl.textContent = `${formatAudioTime(current)} / ${duration > 0 ? formatAudioTime(duration) : '--:--'}`;
  }
  if (digestAudioProgressEl) {
    digestAudioProgressEl.value = String(Math.max(0, Math.min(1000, pct)));
    digestAudioProgressEl.disabled = duration <= 0;
    digestAudioProgressEl.style.setProperty('--audio-progress', `${Math.max(0, Math.min(100, pct / 10))}%`);
  }

  content.querySelectorAll<HTMLButtonElement>('[data-digest-audio-play]').forEach((button) => {
    if (button.dataset.digestAudioBound !== 'true') {
      button.dataset.digestAudioBound = 'true';
      const activate = (event: Event) => {
        event.preventDefault();
        event.stopPropagation();
        const now = Date.now();
        if (now - lastInlineDigestAudioActivation < 250) return;
        lastInlineDigestAudioActivation = now;
        void toggleDigestAudioPlayback(button.dataset.audioDate || fmtDate(currentDate));
      };
      button.addEventListener('pointerup', activate);
      button.addEventListener('click', activate);
      button.addEventListener('keydown', (event) => {
        if (event.key !== 'Enter' && event.key !== ' ') return;
        activate(event);
      });
    }
    const buttonDate = button.dataset.audioDate || null;
    const isCurrent = buttonDate ? digestAudioState.src === digestAudioUrl(buttonDate) : false;
    const buttonPlaying = isCurrent && isPlaying;
    button.classList.toggle('is-playing', buttonPlaying);
    button.setAttribute('aria-pressed', String(buttonPlaying));
    const buttonLabel = button.querySelector<HTMLElement>('[data-digest-audio-label]');
    if (buttonLabel) {
      buttonLabel.textContent = buttonPlaying ? 'Pause digest audio' : isCurrent && audio && audio.currentTime > 0 && !audio.ended ? 'Resume digest audio' : 'Play digest audio';
    }
  });
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
  // Vercel serves index.html (HTTP 200) for any missing /research/... path —
  // its SPA fallback for client-side routes. No real research artifact
  // (markdown, txt, or an HTML *fragment*) is a full HTML document, so a
  // doctype-led response is always the app shell, never content. Keep this
  // title-/build-independent: it previously also required the dev-only Vite
  // client or a literal `<title>ai research`, which silently stopped matching
  // in production once the page <title> became "ara -- AI research arm" —
  // leaking index.html into the Signal Brief (and any other date with no file).
  return text.slice(0, 200).trim().toLowerCase().startsWith('<!doctype html');
}

// `cache: 'no-cache'` forces a conditional-GET revalidation round-trip on
// every fetch. That's correct for files the pipeline still rewrites (today's
// digest/report, the always-mutable manifest, CRUD'd wiki pages) but pure
// latency waste for past dated artifacts that never change again. Callers pass
// `immutable: true` for those so the browser can serve them from cache without
// a round-trip; the default stays `no-cache` so nothing becomes stale by
// accident.
async function fetchMarkdownReport(
  url: string,
  signal: AbortSignal,
  immutable = false,
): Promise<string | null> {
  try {
    const resp = await fetch(url, { signal, cache: immutable ? 'default' : 'no-cache' });
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
  return fetchMarkdownReport(url, signal, isImmutableDate(dateStr));
}

async function fetchFrontPage(dateStr: string, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/front-page/${dateStr}-front-page.png`;
  try {
    const resp = await fetch(url, {
      method: 'HEAD',
      signal,
      cache: isImmutableDate(dateStr) ? 'default' : 'no-cache',
    });
    if (!resp.ok) return null;
    const contentType = (resp.headers.get('content-type') || '').toLowerCase();
    if (!contentType.startsWith('image/')) return null;
    return url;
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') return null;
    return null;
  }
}

async function fetchFrontPageHtml(dateStr: string, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/front-page/${dateStr}-front-page.html`;
  try {
    const resp = await fetch(url, {
      signal,
      cache: isImmutableDate(dateStr) ? 'default' : 'no-cache',
    });
    if (!resp.ok) return null;
    const text = await resp.text();
    if (isViteAppShell(text) || !text.includes('class="ara-paper"')) return null;
    return text;
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') return null;
    return null;
  }
}

async function fetchFrontPageAsset(dateStr: string, signal: AbortSignal): Promise<FrontPageAsset | null> {
  const [url, html] = await Promise.all([
    fetchFrontPage(dateStr, signal),
    fetchFrontPageHtml(dateStr, signal),
  ]);
  if (!url && !html) return null;
  return {
    url: url || `${DATA_BASE}/front-page/${dateStr}-front-page.png`,
    html,
    fallback: null,
  };
}

async function findFrontPageAtOrBefore(
  targetDateStr: string,
  signal: AbortSignal,
): Promise<FrontPageAsset | null> {
  const candidates = (manifestDates('frontpage') ?? [])
    .filter((date) => date <= targetDateStr)
    .sort()
    .reverse();
  for (const date of candidates) {
    const asset = await fetchFrontPageAsset(date, signal);
    if (asset) return { ...asset, fallback: date === targetDateStr ? null : date };
  }
  return null;
}

async function fetchDigest(dateStr: string, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/digest/${dateStr}-digest.md`;
  // Past digests are immutable; today's/yesterday's keep no-cache because the
  // digest workflow can regenerate the current day's file.
  return fetchMarkdownReport(url, signal, isImmutableDate(dateStr));
}

async function fetchResearchDoc(row: GenResearchRow, signal: AbortSignal): Promise<string | null> {
  const url = `${DATA_BASE}/generative/${row.file}`;
  try {
    const resp = await fetch(url, { signal });
    if (!resp.ok) return null;
    const text = await resp.text();
    // Same SPA-fallback guard as fetchMarkdownReport: a missing/not-yet-
    // deployed generative file resolves to index.html (HTTP 200), not a 404.
    return isViteAppShell(text) ? null : text;
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
    : activeTab === 'focusReader'
    ? 'Loading focus reader\u2026'
    : activeTab === 'agents'
    ? 'Loading Arm\u2026'
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
    : activeTab === 'focusReader'
    ? 'No focus reader data available'
    : activeTab === 'agents'
    ? 'Arm view unavailable'
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

// Ancestors whose text must NOT be wrapped in <mark>: SVG charts (axis labels
// etc. — wrapping there breaks the rendered chart), code/pre (highlighting code
// noise), and any element we've already marked.
const HIGHLIGHT_SKIP_ANCESTORS = new Set(['SVG', 'CODE', 'PRE', 'MARK', 'SCRIPT', 'STYLE', 'TEXTAREA']);

/** Wrap occurrences of `searchTerm` in `<mark>` by walking the rendered DOM's
 * text nodes — the markup-safe replacement for the old `>([^<]+)<` regex over
 * serialized HTML, which could corrupt chart `data-*` attributes and element
 * markup. Operates on real Text nodes only, so structure is never touched; it
 * skips nodes inside SVG/code/pre/existing-mark subtrees. Idempotent enough for
 * a single render pass (each text node is matched at most once). */
function highlightSearchMatches(root: HTMLElement, term: string): void {
  if (!term) return;
  const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  // Collect first, mutate after — never mutate the tree the walker is reading.
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      let el = node.parentElement;
      while (el && el !== root) {
        // nodeName is upper-case for HTML; SVG elements report e.g. 'svg'/'text',
        // so compare case-insensitively for the SVG subtree guard.
        if (HIGHLIGHT_SKIP_ANCESTORS.has(el.nodeName.toUpperCase())) return NodeFilter.FILTER_REJECT;
        el = el.parentElement;
      }
      return NodeFilter.FILTER_ACCEPT;
    },
  });
  const targets: Text[] = [];
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    if (n.nodeValue && new RegExp(escaped, 'i').test(n.nodeValue)) targets.push(n as Text);
  }
  for (const textNode of targets) {
    const value = textNode.nodeValue || '';
    const re = new RegExp('(' + escaped + ')', 'gi');
    const frag = document.createDocumentFragment();
    let lastIndex = 0;
    let m: RegExpExecArray | null;
    while ((m = re.exec(value))) {
      if (m.index > lastIndex) frag.appendChild(document.createTextNode(value.slice(lastIndex, m.index)));
      const mark = document.createElement('mark');
      mark.textContent = m[0];
      frag.appendChild(mark);
      lastIndex = m.index + m[0].length;
      // Guard against zero-length matches looping forever (escaped term is
      // always non-empty here, but be defensive).
      if (m[0].length === 0) re.lastIndex++;
    }
    if (lastIndex < value.length) frag.appendChild(document.createTextNode(value.slice(lastIndex)));
    textNode.parentNode?.replaceChild(frag, textNode);
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
  let html = renderReportMarkdown(md);
  html = wrapTables(html);
  html = html.replace(
    /<a\s+href="(https?:\/\/(?:x|twitter)\.com\/\w+\/status\/(\d+))"[^>]*>([\s\S]*?)<\/a>/g,
    (match, url: string, tweetId: string, text: string) => {
      // A "bare" status link (visible text IS the URL) is a source citation —
      // leave a slot the renderer hydrates into a native tweet card from
      // tweets.json. Inline text links stay links (annotated with how long ago).
      const bare = text.trim() === url.trim() || /^https?:\/\/(?:x|twitter)\.com\//.test(text.trim());
      if (bare) {
        return '<div class="tweet-card-slot" data-tweet-id="' + escapeHtml(tweetId) +
          '" data-tweet-url="' + escapeHtml(url) + '"></div>';
      }
      const date = snowflakeToDate(tweetId);
      if (!date) return match;
      return match + '<span class="tweet-ago">' + escapeHtml(timeAgo(date)) + '</span>';
    },
  );
  html = html.replace(/(?<!\w)(@\w+)/g, '<span class="handle">$1</span>');
  return html;
}

// ── Native tweet cards ────────────────────────────────────
// Real tweet data (author / text / avatar / likes / time) is hydrated at
// BUILD time into research/tweets.json (prebuild.mjs, via X's public
// syndication endpoint — CORS blocks fetching it from the browser). We render
// lightweight native cards from it: no third-party iframe, no runtime script,
// on-brand styling. Missing data falls back to a compact "view on X" card.
type TweetCard = {
  name: string; handle: string; avatar: string; verified: boolean;
  text: string; date: string; likes: number; replies: number; url: string;
};
let tweetsPromise: Promise<Record<string, TweetCard>> | null = null;
function loadTweets(): Promise<Record<string, TweetCard>> {
  if (!tweetsPromise) {
    tweetsPromise = fetch(`${DATA_BASE}/tweets.json`)
      .then((r) => (r.ok ? r.json() : {}))
      .catch(() => ({}));
  }
  return tweetsPromise;
}

function compactNum(n: number): string {
  if (!n || n < 0) return '0';
  if (n < 1000) return String(n);
  if (n < 1_000_000) return (n / 1000).toFixed(n < 10_000 ? 1 : 0).replace(/\.0$/, '') + 'K';
  return (n / 1_000_000).toFixed(1).replace(/\.0$/, '') + 'M';
}

const X_LOGO_SVG = '<svg class="tweet-card-logo" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>';
const VERIFIED_SVG = '<svg class="tweet-card-verified" viewBox="0 0 22 22" aria-label="Verified" fill="currentColor"><path d="M20.396 11c-.018-.646-.215-1.275-.57-1.816-.354-.54-.852-.972-1.438-1.246.223-.607.27-1.264.14-1.897-.131-.634-.437-1.218-.882-1.687-.47-.445-1.053-.75-1.687-.882-.633-.13-1.29-.083-1.897.14-.273-.587-.704-1.086-1.245-1.44S11.647 1.62 11 1.604c-.646.017-1.273.213-1.813.568s-.969.854-1.24 1.44c-.608-.223-1.267-.272-1.902-.14-.635.13-1.22.436-1.69.882-.445.47-.749 1.055-.878 1.688-.13.633-.08 1.29.144 1.896-.587.274-1.087.705-1.443 1.245-.356.54-.555 1.17-.574 1.817.02.647.218 1.276.574 1.817.356.54.856.972 1.443 1.245-.224.606-.274 1.263-.144 1.896.13.634.433 1.218.877 1.688.47.443 1.054.747 1.687.878.633.132 1.29.084 1.897-.136.274.586.705 1.084 1.246 1.439.54.354 1.17.551 1.816.569.647-.016 1.276-.213 1.817-.567s.972-.854 1.245-1.44c.604.239 1.266.296 1.903.164.636-.132 1.221-.447 1.68-.907.46-.46.776-1.044.908-1.681s.075-1.299-.165-1.903c.586-.274 1.084-.705 1.439-1.246.354-.54.551-1.17.569-1.816zM9.662 14.85l-3.429-3.428 1.293-1.302 2.072 2.072 4.4-4.794 1.347 1.246z"/></svg>';
const HEART_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 21.638l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54z"/></svg>';
const REPLY_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.067c-4.49.1-8.183-3.51-8.183-8.01z"/></svg>';

function tweetCardHtml(t: TweetCard): string {
  const time = t.date ? timeAgo(new Date(t.date)) : '';
  const avatar = t.avatar
    ? '<img class="tweet-card-avatar" src="' + escapeHtml(t.avatar) + '" alt="" loading="lazy" decoding="async">'
    : '<span class="tweet-card-avatar"></span>';
  return [
    '<a class="tweet-card" href="' + escapeHtml(t.url) + '" target="_blank" rel="noopener noreferrer">',
    '<div class="tweet-card-head">',
    avatar,
    '<span class="tweet-card-id">',
    '<span class="tweet-card-name">' + escapeHtml(t.name) + (t.verified ? VERIFIED_SVG : '') + '</span>',
    '<span class="tweet-card-handle">@' + escapeHtml(t.handle) + '</span>',
    '</span>',
    X_LOGO_SVG,
    '</div>',
    '<div class="tweet-card-text">' + escapeHtml(t.text) + '</div>',
    '<div class="tweet-card-meta">',
    time ? '<span>' + escapeHtml(time) + '</span>' : '',
    '<span class="tweet-card-stat">' + HEART_SVG + compactNum(t.likes) + '</span>',
    t.replies ? '<span class="tweet-card-stat">' + REPLY_SVG + compactNum(t.replies) + '</span>' : '',
    '</div>',
    '</a>',
  ].filter(Boolean).join('');
}

function tweetFallbackHtml(url: string): string {
  return '<a class="tweet-card tweet-card--fallback" href="' + escapeHtml(url) +
    '" target="_blank" rel="noopener noreferrer">' + X_LOGO_SVG +
    '<span class="tweet-card-fallback-text">View post on X</span></a>';
}

// Fill any tweet-card slots emitted by twitterMarkdownToHtml with real cards.
async function hydrateTweetCards(root: HTMLElement): Promise<void> {
  const slots = Array.from(root.querySelectorAll('.tweet-card-slot')) as HTMLElement[];
  if (slots.length === 0) return;
  const tweets = await loadTweets();
  for (const slot of slots) {
    const id = slot.getAttribute('data-tweet-id') || '';
    const url = slot.getAttribute('data-tweet-url') || '';
    const data = tweets[id];
    // Fields are escapeHtml'd in the builders; route through the app's
    // DOMPurify wrapper too (defense-in-depth + allows the card's svg/img).
    setSafeContent(slot, data ? tweetCardHtml(data) : tweetFallbackHtml(url));
  }
}

// ── Wiki mentions (auto-link known entities to the LLM wiki) ──────────────
// In rendered content (digest / twitter / articles) underline the FIRST
// mention of any term that has an LLM-wiki page, link it, and show a hover
// preview on desktop — so readers can quick-look + discover without leaving
// the page. Clicking navigates to the wiki (cross-tab, SPA).
let wikiIndexLoad: Promise<WikiIndex | null> | null = null;
function loadWikiIndexCached(): Promise<WikiIndex | null> {
  if (wikiIndexCache) return Promise.resolve(wikiIndexCache);
  if (!wikiIndexLoad) wikiIndexLoad = loadWikiIndex(new AbortController().signal);
  return wikiIndexLoad;
}

let wikiMatcher: { re: RegExp; map: Map<string, string> } | null = null;
function getWikiMatcher(index: WikiIndex): { re: RegExp; map: Map<string, string> } | null {
  if (wikiMatcher) return wikiMatcher;
  const map = new Map<string, string>();   // lowercased term → slug
  for (const p of index.pages) {
    for (const term of [p.title, ...(p.aliases || [])]) {
      const key = (term || '').trim().toLowerCase();
      if (key.length < 3) continue;          // skip noise like "AI"
      if (!map.has(key)) map.set(key, p.slug);
    }
  }
  if (map.size === 0) return null;
  // Longest terms first so "Claude Opus 4.8" wins over "Claude".
  const escaped = Array.from(map.keys())
    .sort((a, b) => b.length - a.length)
    .map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  wikiMatcher = {
    re: new RegExp('(?<![A-Za-z0-9])(' + escaped.join('|') + ')(?![A-Za-z0-9])', 'gi'),
    map,
  };
  return wikiMatcher;
}

// Text inside these must NOT be wikified (links, code, chips, tweet cards).
const WIKIFY_SKIP = 'a, code, pre, kbd, mark, button, select, .tweet-card, .ara-tag, .handle, .ara-eyebrow, .twitter-source-chip, .twitter-handle-chip, [data-wiki-slug], .wiki-mention';

async function wikifyContent(root: HTMLElement): Promise<void> {
  if (document.body.classList.contains('tab-wiki')) return;  // don't self-link the wiki
  const index = await loadWikiIndexCached();
  if (!index) return;
  const matcher = getWikiMatcher(index);
  if (!matcher) return;
  const used = new Set<string>();   // link only the FIRST mention of each entity
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node: Node): number {
      const el = (node as Text).parentElement;
      if (!el || el.closest(WIKIFY_SKIP)) return NodeFilter.FILTER_REJECT;
      return node.nodeValue && node.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    },
  });
  const textNodes: Text[] = [];
  for (let n = walker.nextNode(); n; n = walker.nextNode()) textNodes.push(n as Text);
  for (const node of textNodes) {
    const text = node.nodeValue || '';
    matcher.re.lastIndex = 0;
    const hits: Array<{ s: number; e: number; slug: string; term: string }> = [];
    let m: RegExpExecArray | null;
    while ((m = matcher.re.exec(text))) {
      const slug = matcher.map.get(m[1].toLowerCase());
      if (slug && !used.has(slug)) {
        used.add(slug);
        hits.push({ s: m.index, e: m.index + m[1].length, slug, term: m[1] });
      }
    }
    if (hits.length === 0) continue;
    const frag = document.createDocumentFragment();
    let cur = 0;
    for (const h of hits) {
      if (h.s > cur) frag.appendChild(document.createTextNode(text.slice(cur, h.s)));
      const a = document.createElement('a');
      a.className = 'wiki-mention';
      a.setAttribute('data-wiki-slug', h.slug);
      a.setAttribute('href', '/wiki/' + h.slug);
      a.textContent = h.term;
      frag.appendChild(a);
      cur = h.e;
    }
    if (cur < text.length) frag.appendChild(document.createTextNode(text.slice(cur)));
    node.parentNode?.replaceChild(frag, node);
  }
  ensureWikiHover();
}

// Shared desktop hover-preview card (one element, repositioned per mention).
let wikiHoverEl: HTMLElement | null = null;
let wikiHoverReady = false;
function ensureWikiHover(): void {
  if (wikiHoverReady) return;
  wikiHoverReady = true;
  document.addEventListener('mouseover', (e) => {
    const el = (e.target as HTMLElement)?.closest?.('.wiki-mention') as HTMLElement | null;
    if (el) showWikiHover(el);
  });
  document.addEventListener('mouseout', (e) => {
    if ((e.target as HTMLElement)?.closest?.('.wiki-mention')) hideWikiHover();
  });
  window.addEventListener('scroll', hideWikiHover, true);
}
function showWikiHover(el: HTMLElement): void {
  const slug = el.getAttribute('data-wiki-slug');
  const page = slug ? wikiPageMap.get(slug) : null;
  if (!page) return;
  if (!wikiHoverEl) {
    wikiHoverEl = document.createElement('div');
    wikiHoverEl.className = 'wiki-hover';
    document.body.appendChild(wikiHoverEl);
  }
  setSafeContent(
    wikiHoverEl,
    '<span class="wiki-hover-type">' + escapeHtml(String(page.type)) + '</span>' +
    '<span class="wiki-hover-title">' + escapeHtml(page.title) + '</span>' +
    '<span class="wiki-hover-summary">' + escapeHtml(page.summary || '') + '</span>',
  );
  const r = el.getBoundingClientRect();
  const left = Math.max(12, Math.min(r.left, window.innerWidth - 320 - 12));
  wikiHoverEl.style.display = 'block';
  wikiHoverEl.style.left = left + 'px';
  wikiHoverEl.style.top = (r.bottom + 8) + 'px';
}
function hideWikiHover(): void {
  if (wikiHoverEl) wikiHoverEl.style.display = 'none';
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

type WikiImage = {
  url: string;
  alt: string;
  caption?: string;
  credit?: string;
  source_url?: string;
};

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
  images?: WikiImage[];
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
    tags.map((t) => '<span class="ara-tag">' + escapeHtml(t) + '</span>').join('') +
    '</span>'
  );
}

function safeWikiImageUrl(url: string | undefined): string | null {
  if (!url || /\s/.test(url)) return null;
  if (/\.svg(?:$|[?#])/i.test(url)) return null;
  if (/^https?:\/\//i.test(url)) return url;
  if (url.startsWith('/') && !url.startsWith('//')) return url;
  return null;
}

function safeWikiSourceUrl(url: string | undefined): string | null {
  if (!url || /\s/.test(url)) return null;
  if (/^https?:\/\//i.test(url)) return url;
  return null;
}

function wikiImagesHtml(images: WikiImage[] | undefined): string {
  const valid = (images || [])
    .map((img) => ({ ...img, url: safeWikiImageUrl(img.url), source_url: safeWikiSourceUrl(img.source_url) }))
    .filter((img) => img.url && img.alt);
  if (!valid.length) return '';

  const mode = valid.length === 1 ? 'single' : 'multi';
  const figures = valid.map((img) => {
    const credit = img.credit
      ? img.source_url
        ? '<a href="' + escapeHtml(img.source_url) + '" class="wiki-image-credit">' + escapeHtml(img.credit) + '</a>'
        : '<span class="wiki-image-credit">' + escapeHtml(img.credit) + '</span>'
      : img.source_url
        ? '<a href="' + escapeHtml(img.source_url) + '" class="wiki-image-credit">Source</a>'
        : '';
    const captionBits = [
      img.caption ? '<span class="wiki-image-caption-text">' + escapeHtml(img.caption) + '</span>' : '',
      credit,
    ].filter(Boolean);
    return [
      '<figure class="wiki-image-figure">',
      '  <img src="' + escapeHtml(img.url || '') + '" alt="' + escapeHtml(img.alt) + '" loading="lazy" decoding="async">',
      captionBits.length ? '  <figcaption class="wiki-image-caption">' + captionBits.join(' ') + '</figcaption>' : '',
      '</figure>',
    ].filter(Boolean).join('\n');
  }).join('\n');

  return '<div class="wiki-image-gallery wiki-image-gallery--' + mode + '">' + figures + '</div>';
}

// Page metadata as an ara-kv grid. Surfaces updated/created (which the index
// carries but the UI never showed) + the link degree, so a page reads like a
// compact entity card.
function wikiKvHtml(page: WikiPage): string {
  const rows = [
    page.updated_at ? '<dt>Updated</dt><dd>' + escapeHtml(page.updated_at) + '</dd>' : '',
    page.created_at ? '<dt>Created</dt><dd>' + escapeHtml(page.created_at) + '</dd>' : '',
    '<dt>Links</dt><dd>' + (page.inbound || []).length + ' in · ' + (page.outbound || []).length + ' out</dd>',
  ].filter(Boolean).join('');
  return '<dl class="ara-kv">' + rows + '</dl>';
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

  const emptyNote =
    visible.length === 0
      ? '<div class="empty-state-text wiki-empty">No wiki pages match the search.</div>'
      : '';

  setSafeWikiContent(
    content,
    [
      '<div class="content-card wiki-index-card">',
      '  <div class="wiki-index-main">',
      emptyNote,
      sections.join('\n'),
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
      '  </div>',
      '  <div class="wiki-page-header">',
      '    <span class="ara-eyebrow">' + escapeHtml(String(page.type)) + '</span>',
      '    <h1 class="wiki-page-title">' + escapeHtml(page.title) + '</h1>',
      page.summary
        ? '    <div class="ara-callout ara-callout--info"><span class="ara-callout-label">Summary</span><p>' + escapeHtml(page.summary) + '</p></div>'
        : '',
      wikiImagesHtml(page.images),
      wikiKvHtml(page),
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

function renderTwitterReport(md: string, fallbackDate: string | null = null): void {
  setSafeContent(content, renderTwitterReportHtml(md, {
    fallbackDate,
    currentDateStr: fmtDate(currentDate),
    currentDateTitle: displayDate(currentDate),
    searchTerm,
    parseUtcTime,
    clockIcon,
    twitterMarkdownToHtml,
    renderSourceChips,
    renderHandleChips,
  }));
  void hydrateTweetCards(content);
  void wikifyContent(content);
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

// Compact card — status + title + company + a few labels. Everything else
// (note, expected, model, verification, sources, history) lives in the modal
// that opens on click, so the board stays short and scannable.
function ticketCard(ticket: Ticket): string {
  // Bird's-eye board = company + title only; labels/details live in the modal.
  return `<article class="ticket-card ticket-card-${ticket.status}" data-slug="${escapeHtml(ticket.slug)}" tabindex="0" role="button" aria-label="${escapeHtml(ticket.title)}">
    <div class="ticket-card-top">
      <span class="ticket-company">${escapeHtml(ticket.company)}</span>
    </div>
    <h3 class="ticket-title">${escapeHtml(ticket.title)}</h3>
  </article>`;
}

function ticketExpandedPanel(ticket: Ticket | null): string {
  if (!ticket) return '';
  // Verification → ara-flag dot (honest 3-state use: confirmed/partial/unverified).
  const verifFlag: Record<TicketVerification, string> = {
    'confirmed': 'ara-flag--green',
    'partial': 'ara-flag--yellow',
    'unverified': 'ara-flag--red',
  };
  const verifLabel: Record<TicketVerification, string> = {
    'confirmed': 'Confirmed',
    'partial': 'Partial corroboration',
    'unverified': 'Unverified',
  };
  // Structured metadata as an ara-kv definition grid.
  const kvRows = [
    `<dt>Company</dt><dd>${escapeHtml(ticket.company)}</dd>`,
    ticket.model ? `<dt>Model</dt><dd>${escapeHtml(ticket.model)}</dd>` : '',
    ticket.expected ? `<dt>Expected</dt><dd>${escapeHtml(ticket.expected)}</dd>` : '',
    `<dt>Verification</dt><dd><span class="ara-flag ${verifFlag[ticket.verification]}"></span>${escapeHtml(verifLabel[ticket.verification])}</dd>`,
    `<dt>Updated</dt><dd>${escapeHtml(ticket.updated_at)}</dd>`,
    `<dt>Created</dt><dd>${escapeHtml(ticket.created_at)}</dd>`,
    ticket.status === 'closed' && ticket.closed_reason
      ? `<dt>Closed</dt><dd>${escapeHtml(ticket.closed_at || '')} — ${escapeHtml(ticket.closed_reason)}</dd>`
      : '',
  ].filter(Boolean).join('\n');
  // History → ara-timeline (the canonical chronological-log component).
  const historyItems = ticket.history.map((h) =>
    `<li class="ara-timeline-item"><time class="ara-timeline-date">${escapeHtml(h.ts)}</time><div class="ara-timeline-event"><p>${escapeHtml(h.change)}</p></div></li>`,
  ).join('');
  return `<section class="ticket-detail-panel" aria-label="${escapeHtml(ticket.title)} details">
    <div class="ticket-detail-header">
      ${ticketStatusPill(ticket.status)}
      <h3>${escapeHtml(ticket.title)}</h3>
    </div>
    <div class="ticket-expanded">
      <dl class="ara-kv">${kvRows}</dl>
      <div class="ticket-body md-content">${DOMPurify.sanitize(renderReportMarkdown(ticket.body))}</div>
      <div class="ticket-history">
        <h4 class="ticket-history-title">History</h4>
        <ol class="ara-timeline">${historyItems}</ol>
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

// Ticket detail modal — clicking a card opens a larger overlay with the full
// ticket (metadata grid, body, history timeline, sources).
let ticketModalEl: HTMLElement | null = null;
function openTicketModal(ticket: Ticket): void {
  if (!ticketModalEl) {
    ticketModalEl = document.createElement('div');
    ticketModalEl.className = 'ticket-modal';
    ticketModalEl.addEventListener('click', (e) => {
      const tgt = e.target as HTMLElement;
      if (tgt === ticketModalEl || tgt.closest('.ticket-modal-close')) closeTicketModal();
    });
    document.body.appendChild(ticketModalEl);
  }
  setSafeContent(
    ticketModalEl,
    '<div class="ticket-modal-card"><button class="ticket-modal-close" type="button" aria-label="Close">✕</button>' +
      ticketExpandedPanel(ticket) + '</div>',
  );
  ticketModalEl.style.display = 'flex';
  document.body.classList.add('modal-open');
}
function closeTicketModal(): void {
  if (ticketModalEl) ticketModalEl.style.display = 'none';
  document.body.classList.remove('modal-open');
}
document.addEventListener('keydown', (e) => {
  if (!ticketModalEl) return;
  if (e.key === 'Escape' && ticketModalEl.style.display === 'flex') {
    closeTicketModal();
    return;
  }
  if ((e.key === 'Enter' || e.key === ' ') && document.body.classList.contains('tab-models')) {
    const card = (document.activeElement as HTMLElement | null)?.closest?.('.ticket-card') as HTMLElement | null;
    const slug = card?.dataset.slug;
    const ticket = slug && ticketsCache ? ticketsCache.find((t) => t.slug === slug) : null;
    if (ticket) { e.preventDefault(); openTicketModal(ticket); }
  }
});

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
  setSafeContent(
    content,
    `<div class="tickets-view">
      <div class="tickets-controls">
        <div class="ticket-filters">${statusBar}</div>
        <select class="ticket-company-select" data-filter-company>${companyOptions}</select>
      </div>
      <div class="tickets-board">
        ${board}
      </div>
      ${emptyNote}
    </div>`,
  );
}

 function frontPageBodyHtml(frontPage: FrontPageAsset): string {
  if (frontPage.html) {
    return [
      '  <div class="content-card-body frontpage-body frontpage-body-interactive">',
      frontPage.html,
      '  </div>',
    ].join('\n');
  }
  return [
    '  <div class="content-card-body frontpage-body">',
    '    <img class="frontpage-img" src="' + escapeHtml(frontPage.url) + '" alt="Front Page" />',
    '  </div>',
  ].join('\n');
}

function enhanceNewspaper(root: ParentNode = content): void {
  const papers = root.querySelectorAll<HTMLElement>('article.ara-paper');
  for (const paper of papers) {
    enhanceAraVisuals(paper);
    const toggles = paper.querySelectorAll<HTMLButtonElement>('.ara-paper-toggle');
    for (const toggle of toggles) {
      if (toggle.dataset.bound === 'true') continue;
      toggle.dataset.bound = 'true';
      const controlledId = toggle.getAttribute('aria-controls');
      const panel = controlledId ? paper.querySelector<HTMLElement>('#' + CSS.escape(controlledId)) : null;
      // Unfold by default — sections (Departments, lead, etc.) start expanded so
      // the content reads without a click; clicking still collapses.
      toggle.setAttribute('aria-expanded', 'true');
      if (panel) panel.hidden = false;
      toggle.addEventListener('click', () => {
        const expanded = toggle.getAttribute('aria-expanded') !== 'false';
        toggle.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        if (panel) panel.hidden = expanded;
      });
    }
  }
}

function renderFrontPage(frontPage: FrontPageAsset): void {
  setSafeContent(
    content,
    [
      '<div class="content-card frontpage-card">',
      frontPageBodyHtml(frontPage),
      '</div>',
    ].join('\n'),
  );
  enhanceNewspaper();
}

function renderToday(md: string, frontPage: FrontPageAsset | null = null): void {
  const dateStr = fmtDate(currentDate);
  let frontPageCardHtml: string | null = null;
  if (frontPage) {
    frontPageCardHtml = [
      '<div class="content-card frontpage-card today-frontpage-card">',
      frontPageBodyHtml(frontPage),
      '</div>',
    ].join('\n');
  }

  setSafeContent(content, renderTodayHtml({
    md,
    dateStr,
    fallbackTitle: displayDate(currentDate),
    audioDates: manifest?.audio || [],
    searchTerm,
    frontPageCardHtml,
  }));
  if (frontPage) enhanceNewspaper();
  syncDigestAudioForDate(dateStr);
  void wikifyContent(content);
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
  // The article body is inserted verbatim and search matches are highlighted
  // AFTER render by walking the DOM's text nodes (see highlightSearchMatches),
  // which can't corrupt chart `data-*` attributes the way the old regex over
  // serialized HTML could.
  const docHtml = body;
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
    enhanceAraArticle(article);
    void wikifyContent(article);
  } else {
    hideResearchTOC();
  }

  // Highlight search matches LAST — after every chart/SVG has rendered — so the
  // text-node walk skips already-built SVG subtrees and only marks prose. Runs
  // on the whole body so non-ara-doc article shapes are highlighted too.
  if (searchTerm) {
    const cardBody = content.querySelector('.content-card-body') as HTMLElement | null;
    if (cardBody) highlightSearchMatches(cardBody, searchTerm);
  }
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
    // The standalone-doc view is the ONLY trusted caller allowed to keep the
    // iframe above (sandboxed, no allow-same-origin, escapeHtml'd src). Every
    // other setSafeContent caller renders LLM/adversarial content with iframe
    // forbidden by default.
    { allowIframe: true },
  );
  setDocTitle(row.title);
  updateResearchAudioUi();
}

function renderAgentsStudio(): void {
  setSafeContent(content, renderAgentsStudioHtml());
  document.title = 'Arm — ara';
}

// ── Focus Reader design route ─────────────────────────
function latestDateFromList(dates: string[] | undefined, target = fmtDate(new Date())): string | null {
  if (!dates || dates.length === 0) return null;
  let best: string | null = null;
  for (const date of dates.slice().sort()) {
    if (date <= target) best = date;
  }
  return best || dates.slice().sort()[dates.length - 1] || null;
}

function sentenceFromMarkdown(md: string, max = 220): string {
  const text = stripMarkdown(md)
    .replace(/^\s*[-*]\s+/, '')
    .replace(/\s+/g, ' ')
    .trim();
  if (!text) return '';
  const sentence = text.match(/^(.+?[.!?])(?:\s|$)/)?.[1] || text;
  return truncateText(sentence, max);
}

function digestSectionItems(md: string): FocusReaderItem[] {
  const sections = splitSections(md);
  const cleanSections = sections
    .map((section) => ({
      title: (section.title || 'Daily brief').trim(),
      body: section.body.replace(/^\s*#\s+[^\n]+\n*/, '').trim(),
    }))
    .filter((section) => section.body);

  const items = cleanSections.slice(0, 6).map((section, index) => {
    const urls = extractUrls(section.body);
    const wordCount = stripMarkdown(section.body).split(/\s+/).filter(Boolean).length;
    const minutes = Math.max(2, Math.min(12, Math.ceil(wordCount / 190)));
    const score = Math.max(46, Math.min(94, 64 + urls.length * 4 + (cleanSections.length - index)));
    const label = /summary|tl;dr/i.test(section.title)
      ? 'Executive scan'
      : section.title.replace(/&amp;/g, '&');
    return {
      title: label,
      label,
      summary: sentenceFromMarkdown(section.body),
      body: section.body,
      minutes,
      sources: urls,
      signal: score >= 80 ? 'High signal' : score >= 68 ? 'Watch' : 'Brief',
      score,
    };
  });

  if (items.length > 0) return items;

  // Deterministic fallback for older or malformed digest files that do not
  // split into sections. This keeps the design route useful without inventing
  // visible fixture labels.
  return [{
    title: 'Daily brief',
    label: 'Digest',
    summary: sentenceFromMarkdown(md) || 'Latest AI research digest is available.',
    body: md,
    minutes: 4,
    sources: extractUrls(md),
    signal: 'Brief',
    score: 64,
  }];
}

function generatedAtFromDigest(md: string): string | null {
  const match = md.match(/\*Generated at ([^*]+)\*/i);
  return match ? match[1].trim() : null;
}

function sourceLinkHtml(url: string, index: number): string {
  const label = sourceLabel(url);
  return [
    '<a class="focus-source-link" href="' + escapeHtml(url) + '" target="_blank" rel="noopener noreferrer">',
    '  <span>',
    '    <strong>' + escapeHtml(label) + '</strong>',
    '    <span class="focus-source-meta">Source ' + String(index + 1).padStart(2, '0') + '</span>',
    '  </span>',
    '  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 17 17 7"></path><path d="M8 7h9v9"></path></svg>',
    '</a>',
  ].join('\n');
}

const DESIGN_SURFACES: Array<{ key: DesignSurface; label: string }> = [
  { key: 'digest', label: 'Digest' },
  { key: 'signals', label: 'Signals' },
  { key: 'models', label: 'Models' },
  { key: 'research', label: 'Research' },
  { key: 'wiki', label: 'Wiki' },
];

function latestManifestDate(dates: string[] | undefined): string | null {
  if (!dates || dates.length === 0) return null;
  return dates.slice().sort().reverse()[0] || null;
}

function designExcerpt(text: string, max = 120): string {
  return truncateText(cleanPublicLeadText(stripMarkdown(text)), max);
}

function renderDesignSurfaceTabs(prefix: string, active: DesignSurface): string {
  return DESIGN_SURFACES.map((surface) => (
    '<button class="' + prefix + '-surface-tab" type="button" data-design-surface="' + surface.key + '" aria-current="' + (active === surface.key ? 'true' : 'false') + '">' +
    '<span>' + escapeHtml(surface.label) + '</span>' +
    '</button>'
  )).join('\n');
}

function renderDesignSurfaceList(data: DesignFrontendData, surface: DesignSurface, prefix: string): string {
  if (surface === 'digest') {
    const rows = data.digestItems.slice(0, 3).map((item) => [
      '<article class="' + prefix + '-surface-item">',
      '  <div class="' + prefix + '-surface-kicker">' + escapeHtml(item.label) + ' · ' + escapeHtml(String(item.score)) + '</div>',
      '  <h3>' + escapeHtml(item.title) + '</h3>',
      '  <p>' + escapeHtml(item.summary || designExcerpt(item.body)) + '</p>',
      '  <span>' + escapeHtml(String(item.sources.length)) + ' sources · ' + escapeHtml(String(item.minutes)) + ' min</span>',
      '</article>',
    ].join('\n')).join('\n');
    return rows || '<div class="' + prefix + '-surface-empty">No digest sections available.</div>';
  }
  if (surface === 'signals') {
    const rows = data.twitterStories.slice(0, 3).map((story) => [
      '<article class="' + prefix + '-surface-item">',
      '  <div class="' + prefix + '-surface-kicker">Signal ' + escapeHtml(story.rank || 'watch') + '</div>',
      '  <h3>' + escapeHtml(story.title) + '</h3>',
      '  <p>' + escapeHtml(designExcerpt(storyCurrentLead(story.body) || story.body)) + '</p>',
      '  <span>' + escapeHtml(String(story.links.length)) + ' links · ' + escapeHtml(story.handles.slice(0, 2).join(', ') || 'source report') + '</span>',
      '</article>',
    ].join('\n')).join('\n');
    return rows || '<div class="' + prefix + '-surface-empty">No signal stories available.</div>';
  }
  if (surface === 'models') {
    const rows = data.tickets.slice(0, 3).map((ticket) => [
      '<article class="' + prefix + '-surface-item">',
      '  <div class="' + prefix + '-surface-kicker">' + escapeHtml(ticket.company) + ' · ' + escapeHtml(ticket.status) + '</div>',
      '  <h3>' + escapeHtml(ticket.title) + '</h3>',
      '  <p>' + escapeHtml(designExcerpt(ticket.status_note || ticket.body || ticket.expected || ticket.title)) + '</p>',
      '  <span>' + escapeHtml(ticket.verification) + ' · ' + escapeHtml(String(ticket.sources.length)) + ' sources</span>',
      '</article>',
    ].join('\n')).join('\n');
    return rows || '<div class="' + prefix + '-surface-empty">No model tickets available.</div>';
  }
  if (surface === 'research') {
    const rows = data.researchRows.slice(0, 3).map((row) => [
      '<article class="' + prefix + '-surface-item">',
      '  <div class="' + prefix + '-surface-kicker">' + escapeHtml(row.model) + '</div>',
      '  <h3>' + escapeHtml(row.title) + '</h3>',
      '  <p>' + escapeHtml(designExcerpt(row.prompt || row.source || row.title)) + '</p>',
      '  <span>' + escapeHtml((row.tags || []).slice(0, 3).join(', ') || 'long-form') + '</span>',
      '</article>',
    ].join('\n')).join('\n');
    return rows || '<div class="' + prefix + '-surface-empty">No research articles available.</div>';
  }
  const rows = data.wikiPages.slice(0, 3).map((page) => [
    '<article class="' + prefix + '-surface-item">',
    '  <div class="' + prefix + '-surface-kicker">' + escapeHtml(String(page.type)) + '</div>',
    '  <h3>' + escapeHtml(page.title) + '</h3>',
    '  <p>' + escapeHtml(page.summary || (page.aliases || []).slice(0, 3).join(', ') || 'Entity memory page') + '</p>',
    '  <span>' + escapeHtml(String((page.inbound || []).length + (page.outbound || []).length)) + ' graph links</span>',
    '</article>',
  ].join('\n')).join('\n');
  return rows || '<div class="' + prefix + '-surface-empty">No wiki pages available.</div>';
}

function renderDesignSurfacePanel(prefix: string, data: DesignFrontendData, surface: DesignSurface): string {
  const meta = DESIGN_SURFACES.find((item) => item.key === surface) || DESIGN_SURFACES[0];
  return [
    '<section class="' + prefix + '-surface-panel" aria-label="' + escapeHtml(meta.label) + ' surface">',
    '  <div class="' + prefix + '-surface-head">',
    '    <h2>' + escapeHtml(meta.label) + '</h2>',
    '    <div class="' + prefix + '-surface-tabs">' + renderDesignSurfaceTabs(prefix, surface) + '</div>',
    '  </div>',
    '  <div class="' + prefix + '-surface-grid">' + renderDesignSurfaceList(data, surface, prefix) + '</div>',
    '</section>',
  ].join('\n');
}

async function loadDesignFrontendData(m: Manifest, signal: AbortSignal): Promise<DesignFrontendData> {
  const digestDate = latestManifestDate(m.today);
  const twitterDate = latestManifestDate(m.twitter);
  const [digestMd, twitterMd, tickets, wiki] = await Promise.all([
    digestDate ? fetchDigest(digestDate, signal) : Promise.resolve(null),
    twitterDate ? fetchTwitter(twitterDate, signal) : Promise.resolve(null),
    loadTickets(),
    loadWikiIndex(signal),
  ]);
  const cleanTwitter = twitterMd ? sanitizePublicReportMarkdown(twitterMd) : '';
  const parsedTwitterStories = cleanTwitter ? parseTwitterStories(cleanTwitter).slice(0, 6) : [];
  return {
    digestDate,
    twitterDate,
    digestItems: digestMd ? digestSectionItems(digestMd).slice(0, 8) : [],
    twitterStories: parsedTwitterStories,
    tickets: (tickets || []).slice().sort((a, b) => (b.updated_at || '').localeCompare(a.updated_at || '')),
    researchRows: (m.generative || []).slice().sort((a, b) => (b.created_at || '').localeCompare(a.created_at || '')),
    wikiPages: (wiki?.pages || []).slice().sort((a, b) => (b.updated_at || '').localeCompare(a.updated_at || '')),
  };
}

async function loadFocusReaderData(signal: AbortSignal): Promise<FocusReaderData | null> {
  if (focusReaderData) return focusReaderData;
  const m = await loadManifest();
  if (!m) return null;
  const today = fmtDate(new Date());
  const digestDate = latestDateFromList(m.today, today) || today;
  const digestMd = await fetchDigest(digestDate, signal);
  if (!digestMd) return null;

  const [tickets, wikiIndex] = await Promise.all([
    loadTickets(),
    loadWikiIndex(signal),
  ]);
  const rows = m.generative;
  const sortedResearch = rows.slice().sort((a, b) => a.created_at.localeCompare(b.created_at));
  const latestResearch = sortedResearch[sortedResearch.length - 1];
  const ticketList = tickets ?? [];
  const frontend = await loadDesignFrontendData(m, signal);

  const data: FocusReaderData = {
    date: today,
    digestDate,
    generatedAt: generatedAtFromDigest(digestMd),
    items: digestSectionItems(digestMd),
    digestCount: m.today.length,
    researchCount: rows.length,
    ticketCount: ticketList.length,
    activeTicketCount: ticketList.filter((ticket) => ticket.status !== 'closed').length,
    wikiCount: wikiIndex?.pages?.length ?? 0,
    // Deterministic fallback for manifests that predate generative research.
    latestResearchTitle: latestResearch?.title || 'No long-form research published yet',
    frontend,
  };
  if (!signal.aborted && tickets && wikiIndex) {
    focusReaderData = data;
  }
  return data;
}

function renderFocusReader(data: FocusReaderData): void {
  setDocTitle('Focus Reader');
  const term = focusReaderSearchTerm.trim().toLowerCase();
  const visibleEntries = data.items
    .map((item, index) => ({ item, index }))
    .filter(({ item }) => {
      if (!term) return true;
      const hay = [item.title, item.label, item.summary, item.body, ...item.sources].join(' ').toLowerCase();
      return hay.includes(term);
    });
  const selectedEntry = visibleEntries.find((entry) => entry.index === focusReaderSelectedIndex) || visibleEntries[0];
  const hasVisibleMatch = visibleEntries.length > 0;
  const selected = hasVisibleMatch
    ? (selectedEntry?.item || data.items[Math.max(0, Math.min(focusReaderSelectedIndex, data.items.length - 1))] || data.items[0])
    : null;
  const selectedIndex = selected && selectedEntry ? selectedEntry.index : (selected ? data.items.indexOf(selected) : -1);
  const articleHtml = selected
    ? wrapTables(renderReportMarkdown(selected.body))
    : '<p class="focus-empty-copy">No briefing section contains "' + escapeHtml(focusReaderSearchTerm.trim()) + '".</p>';
  const sources = selected && selected.sources.length
    ? selected.sources.slice(0, 3).map(sourceLinkHtml).join('\n')
    : selected ? [
        // Deterministic fallback when a digest section has no direct URLs.
        sourceLinkHtml('/research/digest/' + data.digestDate + '-digest.md', 0),
      ].join('\n') : '<p class="focus-note">No source stack while the search has no matching briefing.</p>';
  const queue = visibleEntries.map(({ item, index }) => [
    '<button class="focus-story-card" type="button" data-focus-index="' + index + '" aria-current="' + (index === selectedIndex ? 'true' : 'false') + '">',
    '  <span class="focus-story-meta">' + escapeHtml(item.label) + ' · ' + item.minutes + ' min</span>',
    '  <h3>' + escapeHtml(item.title) + '</h3>',
    item.summary ? '  <p>' + escapeHtml(item.summary) + '</p>' : '',
    '  <span class="focus-story-footer">',
    '    <span class="focus-signal">' + escapeHtml(item.signal) + '</span>',
    '    <span class="focus-story-meta">' + item.sources.length + ' sources</span>',
    '  </span>',
    '</button>',
  ].join('\n')).join('\n');
  const queueEmpty = visibleEntries.length === 0
    ? '<div class="focus-queue-empty">No briefings match the search.</div>'
    : '';

  setSafeContent(
    content,
    [
      '<div class="focus-reader-page">',
      '  <header class="focus-masthead">',
      '    <a class="focus-brand" href="/today/' + escapeHtml(data.digestDate) + '" aria-label="ARA home">',
      '      <span class="focus-brand-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 19 12 4l7 15"></path><path d="M8 14h8"></path></svg></span>',
      '      <span>ARA</span>',
      '    </a>',
      '    <label class="focus-search">',
      '      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="m16 16 4 4"></path></svg>',
      '      <input type="search" value="' + escapeHtml(focusReaderSearchTerm) + '" placeholder="Search briefings, sources, claims" aria-label="Search briefings, sources, claims">',
      '    </label>',
      '    <div class="focus-header-actions" aria-label="Reader actions">',
      '      <a class="focus-icon-button" href="/research" aria-label="Open research index"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 7h10v10H7z"></path><path d="M4 4h10"></path><path d="M10 20h10V10"></path></svg></a>',
      '      <a class="focus-icon-button primary" href="/models" aria-label="Open model timeline"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 21H5V3h11l3 3v15Z"></path><path d="M8 3v6h8"></path><path d="M8 17h8"></path></svg></a>',
      '    </div>',
      '  </header>',
      '  <main class="focus-workspace">',
      '    <aside class="focus-queue" aria-label="Reading queue">',
      '      <div class="focus-queue-header"><h2>Today</h2><span class="focus-count">' + visibleEntries.length + '</span></div>',
      '      <div class="focus-story-list">' + queue + queueEmpty + '</div>',
      '    </aside>',
      '    <section class="focus-reader" aria-label="Current briefing">',
      '      <div class="focus-reader-toolbar">',
      '        <div class="focus-reading-state">',
      '          <span>Focus reader</span><span class="focus-dot" aria-hidden="true"></span><span>' + escapeHtml(data.digestDate) + '</span><span class="focus-dot" aria-hidden="true"></span><span>' + escapeHtml(data.generatedAt || 'Latest manifest data') + '</span>',
      '        </div>',
      '        <div class="focus-reader-actions">',
      '          <a class="focus-icon-button" href="/today/' + escapeHtml(data.digestDate) + '" aria-label="Open full digest"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 6h16"></path><path d="M4 12h16"></path><path d="M4 18h10"></path></svg></a>',
      '          <a class="focus-icon-button" href="/wiki" aria-label="Open wiki"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5z"></path></svg></a>',
      '        </div>',
      '      </div>',
      '      <article class="focus-article">',
      '        <div class="focus-article-inner">',
      '          <div class="focus-kicker">' + escapeHtml(selected?.label || 'Search') + '</div>',
      '          <h1>' + escapeHtml(selected?.title || 'No matching briefing') + '</h1>',
      selected?.summary ? '          <p class="focus-dek">' + escapeHtml(selected.summary) + '</p>' : '',
      '          <div class="focus-article-meta"><span>Signal score ' + (selected?.score ?? 0) + '</span><span>' + (selected?.sources.length ?? 0) + ' sources</span><span>' + (selected?.minutes ?? 0) + ' min read</span><span>Digest: ' + escapeHtml(data.digestDate) + '</span></div>',
      '          <div class="focus-article-body md-content">' + articleHtml + '</div>',
      '        </div>',
      '      </article>',
      '    </section>',
      '    <aside class="focus-evidence" aria-label="Evidence">',
      '      <div class="focus-evidence-header"><h2>Evidence</h2><span class="focus-count">' + (selected?.score ?? 0) + '</span></div>',
      '      <div class="focus-evidence-body">',
      '        <section class="focus-meter" aria-label="Confidence"><div class="focus-meter-top"><span class="focus-meter-label">Confidence</span><strong>' + (selected?.score ?? 0) + '</strong></div><div class="focus-bar" aria-hidden="true"><span></span></div><p class="focus-note">Score combines section depth, source count, and whether the item appears in the latest digest cycle.</p></section>',
      '        <section class="focus-source-list" aria-label="Source stack"><h3 class="focus-section-title">Source Stack</h3>' + sources + '</section>',
      '        <section class="focus-notes" aria-label="Repository state"><h3 class="focus-section-title">Repo State</h3>',
      '          <p class="focus-note">' + data.digestCount + ' digests · ' + data.researchCount + ' research articles · ' + data.wikiCount + ' wiki pages.</p>',
      '          <p class="focus-note">' + data.activeTicketCount + ' active model tickets out of ' + data.ticketCount + '. Latest research: ' + escapeHtml(data.latestResearchTitle) + '.</p>',
      '        </section>',
      '      </div>',
      '    </aside>',
      '  </main>',
      '  <section class="focus-full-frontend" aria-label="Complete ARA frontend">',
      renderDesignSurfacePanel('focus', data.frontend, focusReaderSurface),
      '  </section>',
      '</div>',
    ].join('\n'),
  );
  const bar = content.querySelector<HTMLElement>('.focus-bar span');
  if (bar) bar.style.width = (selected?.score ?? 0) + '%';
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
    if (activeTab === 'agents') {
      renderAgentsStudio();
      renderCalendar();
      currentSection = 0;
      updateNavCounter();
      updateSearchCount();
      return;
    }
    if (!manifest) {
      await loadManifest();
      if (requestId !== loadRequestId) return;
    }
    if (activeTab === 'focusReader') {
      const result = await withTimeout(loadFocusReaderData(controller.signal), LOAD_TIMEOUT_MS, controller);
      if (requestId !== loadRequestId) return;
      if (result === 'timeout') {
        showError('Loading timed out', 'Network may be slow. Click to retry.');
      } else if (result) {
        renderFocusReader(result);
      } else {
        showEmpty(dateStr);
      }
    } else if (activeTab === 'wiki') {
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
      const result = await withTimeout(fetchFrontPageAsset(dateStr, controller.signal), LOAD_TIMEOUT_MS, controller);
      if (requestId !== loadRequestId) return;
      if (result === 'timeout') {
        showError('Loading timed out', 'Network may be slow. Click to retry.');
      } else if (result) {
        renderFrontPage(result);
      } else {
        // Front page missing for today — fall back to the most recent available
        const fallback = await findFrontPageAtOrBefore(dateStr, controller.signal);
        if (fallback) {
          renderFrontPage(fallback);
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
        fetchFrontPageAsset(dateStr, controller.signal),
      ]);
      if (requestId !== loadRequestId) return;
      // Resolve which front-page URL to pass (today's, or the most-recent fallback).
      let frontPage: FrontPageAsset | null = null;
      if (fpResult) {
        frontPage = fpResult;
      } else {
        const fp = await findFrontPageAtOrBefore(dateStr, controller.signal);
        if (requestId !== loadRequestId) return;
        if (fp) frontPage = fp;
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
      // Search-driven deep link into a specific digest section.
      if (pendingDigestSection) {
        const want = pendingDigestSection;
        pendingDigestSection = null;
        requestAnimationFrame(() => scrollToDigestSection(want));
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
      // Search-driven deep link into a specific twitter cycle (by id anchor).
      if (pendingTwitterAnchor) {
        const id = pendingTwitterAnchor;
        pendingTwitterAnchor = null;
        requestAnimationFrame(() =>
          document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' }),
        );
      }
    }

    if (activeTab !== 'research' && activeTab !== 'wiki' && activeTab !== 'focusReader') {
      syncDigestAudioForDate(dateStr);
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

// Deferred scroll targets for search-driven navigation into the today/twitter
// views — set by activateSearchHit, consumed post-render in load().
let pendingDigestSection: string | null = null;
let pendingTwitterAnchor: string | null = null;

// Digest section cards carry no id, so match by the rendered .content-card-title
// (textContent decodes &amp; back to &, so a literal-& title compares equal).
function scrollToDigestSection(title: string): void {
  const want = title.trim();
  const idx = getCards().findIndex(
    (c) => (c.querySelector('.content-card-title')?.textContent || '').trim() === want,
  );
  if (idx >= 0) scrollToSection(idx);
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

// Clicking the wordmark returns to the home (today) view.
function goHome(): void {
  activeTab = 'today';
  selectedSlug = null;
  syncTabUi();
  load();
}
const brandHome = document.getElementById('brandHome');
brandHome?.addEventListener('click', goHome);
brandHome?.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); goHome(); }
});

const searchToggle = document.getElementById('searchToggle');
const searchOverlay = document.getElementById('searchOverlay');
const searchClear = document.getElementById('searchClear');
const searchResultsEl = document.getElementById('searchResults');

// ── Global search ─────────────────────────────────────
// Search across ALL content — research articles, wiki pages, model tickets —
// from any tab; a result jumps straight to the item. The corpus is built lazily
// from the already-loaded indexes and cached.
type SearchHit = { type: 'research' | 'wiki' | 'model' | 'digest' | 'twitter'; title: string; subtitle: string; slug: string; hay: string; date?: string; anchor?: string; sectionTitle?: string };
let searchCorpus: SearchHit[] | null = null;
let searchHits: SearchHit[] = [];
let searchSel = -1;
const SEARCH_TYPE_LABEL: Record<SearchHit['type'], string> = { research: 'Research', wiki: 'Wiki', model: 'Model', digest: 'Digest', twitter: 'Twitter' };

// Build-time content index (digest sections + twitter cycles) — see
// scripts/prebuild.mjs:buildSearchIndex. Loaded once, cached, best-effort.
type SearchIndexFile = {
  digestSections?: { date: string; sectionTitle: string; snippet?: string }[];
  twitter?: { date: string; cycleTime: string; anchor: string; summary?: string; storyTitles?: string[] }[];
};
let searchIndexCache: SearchIndexFile | null = null;
let searchIndexPromise: Promise<SearchIndexFile | null> | null = null;
function loadSearchIndex(): Promise<SearchIndexFile | null> {
  if (searchIndexCache) return Promise.resolve(searchIndexCache);
  if (searchIndexPromise) return searchIndexPromise;
  searchIndexPromise = (async () => {
    try {
      const r = await fetch(`${DATA_BASE}/search-index.json`);
      if (!r.ok) return null;
      const j = (await r.json()) as SearchIndexFile;
      searchIndexCache = j;
      return j;
    } catch {
      return null; // missing file / SPA-shell HTML / parse error → no content hits
    }
  })();
  return searchIndexPromise;
}
function ymdToDate(s: string): Date {
  const [y, m, d] = s.split('-').map(Number);
  return new Date(y, (m || 1) - 1, d || 1);
}

async function buildSearchCorpus(): Promise<SearchHit[]> {
  if (searchCorpus) return searchCorpus;
  const [m, wiki, tickets, idx] = await Promise.all([loadManifest(), loadWikiIndexCached(), loadTickets(), loadSearchIndex()]);
  const hits: SearchHit[] = [];
  if (wiki) for (const p of wiki.pages) {
    hits.push({ type: 'wiki', title: p.title, subtitle: (p.aliases || []).slice(0, 3).join(', ') || String(p.type),
      slug: p.slug, hay: (p.title + ' ' + (p.aliases || []).join(' ') + ' ' + (p.summary || '') + ' ' + (p.tags || []).join(' ')).toLowerCase() });
  }
  if (m) for (const r of (m.generative || [])) {
    hits.push({ type: 'research', title: r.title, subtitle: (r.tags || []).slice(0, 4).join(', '),
      slug: r.slug, hay: (r.title + ' ' + (r.tags || []).join(' ') + ' ' + (r.prompt || '')).toLowerCase() });
  }
  if (tickets) for (const t of tickets) {
    hits.push({ type: 'model', title: t.title, subtitle: t.company + (t.model ? ' · ' + t.model : ''),
      slug: t.slug, hay: (t.title + ' ' + t.company + ' ' + (t.model || '') + ' ' + (t.labels || []).join(' ')).toLowerCase() });
  }
  const ds = idx?.digestSections;
  if (ds) for (const s of ds) {
    hits.push({ type: 'digest', title: s.sectionTitle, subtitle: displayDate(ymdToDate(s.date)) + ' digest',
      slug: '', date: s.date, sectionTitle: s.sectionTitle,
      hay: (s.date + ' ' + s.sectionTitle + ' ' + (s.snippet || '')).toLowerCase() });
  }
  const tw = idx?.twitter;
  if (tw) for (const c of tw) {
    const titleText = c.summary || c.storyTitles?.[0] || (c.cycleTime + ' cycle');
    hits.push({ type: 'twitter', title: titleText, subtitle: displayDate(ymdToDate(c.date)) + ' · ' + c.cycleTime,
      slug: '', date: c.date, anchor: c.anchor,
      hay: (c.date + ' ' + c.cycleTime + ' ' + (c.summary || '') + ' ' + (c.storyTitles || []).join(' ')).toLowerCase() });
  }
  searchCorpus = hits;
  return hits;
}

function renderSearchHits(): void {
  if (!searchResultsEl) return;
  if (searchHits.length === 0) {
    setSafeContent(searchResultsEl, '<div class="search-empty">No matches</div>');
    searchResultsEl.hidden = false;
    return;
  }
  const rows = searchHits.map((h, i) =>
    '<button class="search-result' + (i === searchSel ? ' is-sel' : '') + '" type="button" role="option" data-sr-index="' + i + '">' +
    '<span class="search-result-type">' + SEARCH_TYPE_LABEL[h.type] + '</span>' +
    '<span class="search-result-title">' + escapeHtml(h.title) + '</span>' +
    (h.subtitle ? '<span class="search-result-sub">' + escapeHtml(h.subtitle) + '</span>' : '') +
    '</button>',
  ).join('');
  setSafeContent(searchResultsEl, rows);
  searchResultsEl.hidden = false;
}

async function runGlobalSearch(query: string): Promise<void> {
  const q = query.trim().toLowerCase();
  if (!q) {
    searchHits = [];
    searchSel = -1;
    if (searchResultsEl) searchResultsEl.hidden = true;
    if (searchCountEl) searchCountEl.textContent = '';
    return;
  }
  const corpus = await buildSearchCorpus();
  searchHits = corpus
    .map((h) => {
      const t = h.title.toLowerCase();
      const score = t.startsWith(q) ? 3 : t.includes(q) ? 2 : h.hay.includes(q) ? 1 : 0;
      return { h, score };
    })
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score || a.h.title.length - b.h.title.length)
    .slice(0, 24)
    .map((x) => x.h);
  searchSel = searchHits.length ? 0 : -1;
  if (searchCountEl) searchCountEl.textContent = searchHits.length ? String(searchHits.length) : '';
  renderSearchHits();
}

function moveSearchSel(d: number): void {
  if (searchHits.length === 0) return;
  searchSel = (searchSel + d + searchHits.length) % searchHits.length;
  renderSearchHits();
  (searchResultsEl?.querySelector('.search-result.is-sel') as HTMLElement | null)?.scrollIntoView({ block: 'nearest' });
}

function activateSearchHit(h: SearchHit): void {
  closeSearch();
  if (h.type === 'model') {
    activeTab = 'models';
    selectedSlug = null;
    syncTabUi();
    load();
    const t = ticketsCache ? ticketsCache.find((x) => x.slug === h.slug) : null;
    if (t) window.setTimeout(() => openTicketModal(t), 60);
    return;
  }
  if (h.type === 'digest') {
    if (h.date) {
      activeTab = 'today';
      selectedSlug = null;
      currentDate = ymdToDate(h.date);
      calendarMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
      pendingDigestSection = h.sectionTitle || null;
      syncTabUi();
      load();
    }
    return;
  }
  if (h.type === 'twitter') {
    if (h.date) {
      activeTab = 'twitter';
      selectedSlug = null;
      currentDate = ymdToDate(h.date);
      calendarMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
      pendingTwitterAnchor = h.anchor || null;
      syncTabUi();
      load();
    }
    return;
  }
  activeTab = h.type; // 'research' | 'wiki'
  selectedSlug = h.slug;
  syncTabUi();
  load();
}

function syncSearchClear(): void {
  if (searchClear) (searchClear as HTMLElement).hidden = searchInput.value.length === 0;
}
function openSearch(): void {
  if (searchOverlay) searchOverlay.hidden = false;
  syncSearchClear();
  searchInput.focus();
  searchInput.select();
}
function closeSearch(): void {
  if (searchOverlay) searchOverlay.hidden = true;
  if (searchResultsEl) searchResultsEl.hidden = true;
}
function clearSearch(): void {
  searchInput.value = '';
  syncSearchClear();
  void runGlobalSearch('');
  searchInput.focus();
}
searchToggle?.addEventListener('click', () => {
  if (searchOverlay && searchOverlay.hidden) openSearch();
  else closeSearch();
});
searchClear?.addEventListener('click', clearSearch);
searchResultsEl?.addEventListener('click', (e) => {
  const btn = (e.target as HTMLElement).closest('.search-result') as HTMLElement | null;
  if (!btn) return;
  const i = Number(btn.dataset.srIndex);
  if (searchHits[i]) activateSearchHit(searchHits[i]);
});
searchInput.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') { closeSearch(); searchInput.blur(); }
  else if (e.key === 'ArrowDown') { e.preventDefault(); moveSearchSel(1); }
  else if (e.key === 'ArrowUp') { e.preventDefault(); moveSearchSel(-1); }
  else if (e.key === 'Enter') { e.preventDefault(); if (searchHits[searchSel]) activateSearchHit(searchHits[searchSel]); }
});
// ⌘F / Ctrl+F opens search from anywhere (overrides native find); click outside
// the panel closes it.
document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && (e.key === 'f' || e.key === 'F')) {
    e.preventDefault();
    openSearch();
  }
});
document.addEventListener('mousedown', (e) => {
  if (!searchOverlay || searchOverlay.hidden) return;
  const t = e.target as Node;
  if (!searchOverlay.contains(t) && !(searchToggle && searchToggle.contains(t))) closeSearch();
});

searchInput.addEventListener('input', () => {
  syncSearchClear();
  if (searchDebounceId !== null) window.clearTimeout(searchDebounceId);
  searchDebounceId = window.setTimeout(() => { void runGlobalSearch(searchInput.value); }, 120);
});

languageSwitch?.addEventListener('click', (e) => {
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
  if (target.closest('[data-ara-figure-close]')) {
    closeAraFigureModal();
    return;
  }
  const figureImg = target.closest('.ara-doc .ara-figure img') as HTMLImageElement | null;
  if (figureImg) {
    e.preventDefault();
    openAraFigureModal(figureImg);
    return;
  }
  if (target.closest('[data-retry]')) {
    load();
    return;
  }
  const designSurfaceButton = target.closest('[data-design-surface]') as HTMLElement | null;
  if (designSurfaceButton) {
    const surface = designSurfaceButton.dataset.designSurface as DesignSurface | undefined;
    if (surface && DESIGN_SURFACES.some((item) => item.key === surface)) {
      if (activeTab === 'focusReader' && focusReaderData) {
        focusReaderSurface = surface;
        renderFocusReader(focusReaderData);
      }
    }
    return;
  }
  const focusQueueButton = target.closest('[data-focus-index]') as HTMLElement | null;
  if (focusQueueButton && activeTab === 'focusReader') {
    const nextIndex = Number(focusQueueButton.dataset.focusIndex);
    if (Number.isFinite(nextIndex) && focusReaderData) {
      focusReaderSelectedIndex = Math.max(0, Math.min(nextIndex, focusReaderData.items.length - 1));
      renderFocusReader(focusReaderData);
    }
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
  // Wiki mentions (auto-linked entities in digest/twitter/articles) navigate
  // to the wiki from ANY tab — distinct from the wiki-tab-only links below.
  const wikiMention = target.closest('.wiki-mention') as HTMLElement | null;
  if (wikiMention) {
    const slug = wikiMention.dataset.wikiSlug;
    if (slug) {
      e.preventDefault();
      activeTab = 'wiki';
      selectedSlug = slug;
      load();
    }
    return;
  }
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
    // Don't open the modal on link clicks inside the card — let them through.
    if (target.closest('a, button')) return;
    const slug = row.dataset.slug;
    const ticket = slug && ticketsCache ? ticketsCache.find((t) => t.slug === slug) : null;
    if (ticket) openTicketModal(ticket);
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

content.addEventListener('input', (e) => {
  if (activeTab !== 'focusReader' || !focusReaderData) return;
  const input = (e.target as HTMLElement).closest('.focus-search input') as HTMLInputElement | null;
  if (!input) return;
  focusReaderSearchTerm = input.value;
  const needle = focusReaderSearchTerm.trim().toLowerCase();
  if (needle) {
    const matchIndex = focusReaderData.items.findIndex((item) =>
      [item.title, item.label, item.summary, item.body, ...item.sources].join(' ').toLowerCase().includes(needle),
    );
    if (matchIndex >= 0) focusReaderSelectedIndex = matchIndex;
  }
  renderFocusReader(focusReaderData);
  const nextInput = content.querySelector<HTMLInputElement>('.focus-search input');
  if (nextInput) {
    nextInput.focus();
    const end = nextInput.value.length;
    nextInput.setSelectionRange(end, end);
  }
});

content.addEventListener('keydown', (e: KeyboardEvent) => {
  if (e.key !== 'Enter' && e.key !== ' ') return;
  const target = e.target as HTMLElement;
  const figureImg = target.closest('.ara-doc .ara-figure img') as HTMLImageElement | null;
  if (figureImg) {
    e.preventDefault();
    openAraFigureModal(figureImg);
    return;
  }
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
  if (e.key === 'Escape') {
    closeAraFigureModal();
    return;
  }
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
      openSearch();
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
    document.body.classList.toggle('tab-focus-reader', activeTab === 'focusReader');
    document.body.classList.toggle('tab-agents', activeTab === 'agents');
    // Re-probe availability for current month with new tab (date tabs only).
    // The models/wiki tabs don't use date routing, so skip probing there too —
    // it'd just paint dots on a calendar that's hidden anyway.
    if (activeTab !== 'research' && activeTab !== 'models' && activeTab !== 'wiki' && activeTab !== 'focusReader' && activeTab !== 'agents') {
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
document.body.classList.toggle('tab-focus-reader', currentTab === 'focusReader');
document.body.classList.toggle('tab-agents', currentTab === 'agents');
if (currentTab !== 'research' && currentTab !== 'models' && currentTab !== 'wiki' && currentTab !== 'focusReader' && currentTab !== 'agents') {
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
