/**
 * Aradio — the rolling AI-news station, rendered from research/aradio/*.json.
 *
 * Contract: docs/aradio.md ("Published files", "Audio", "Dashboard").
 *
 * WHY EVERYTHING HERE IS DEFENSIVE
 * --------------------------------
 * Every string is model output or third-party text relayed by the editor
 * agent (podcast speakers, filings, tweets). So:
 *   - every value is escaped for BOTH text and attribute contexts (`esc`) and
 *     the assembled HTML still goes through the app's DOMPurify sink;
 *   - links survive only as http(s) URLs (`safeHttpUrl`);
 *   - fetch paths and S3 keys are rebuilt from validated shapes
 *     (`aradioBulletinPath`, `normalizeAradioAudio`), never taken verbatim, so
 *     a malformed index cannot point the page at an arbitrary URL.
 * Before the first editor run none of the files exist, and a schema bump must
 * degrade to "missing field", never to a crash — every field is optional.
 *
 * This module is pure (no DOM, no fetch): main.ts owns state, polling and the
 * shared audio player; node tests import this file directly.
 */

import { uiText, type UiCopyKey, type UiLanguage } from '../i18n.ts';

// ── Types ─────────────────────────────────────────────────────────────────

export type AradioThreadStatus = 'escalating' | 'developing' | 'steady' | 'resolved';
export type AradioEvidenceKind =
  | 'podcast' | 'video' | 'earnings-call' | 'earnings' | 'twitter' | 'ticket' | 'other';
/** ok = parsed; missing = 404 / never published; error = network or corrupt. */
export type AradioLoadStatus = 'ok' | 'missing' | 'error';

export type AradioEvidence = {
  url: string;
  kind: AradioEvidenceKind;
  label: string;
  at: string | null;
  speaker: string | null;
  quote: string | null;
};

export type AradioHistoryEntry = { at: string | null; change: string };

export type AradioThread = {
  slug: string;
  title: string;
  status: AradioThreadStatus;
  importance: number;
  firstSeen: string | null;
  updatedAt: string | null;
  now: string;
  changed: string;
  watch: string;
  evidence: AradioEvidence[];
  history: AradioHistoryEntry[];
};

export type AradioBoard = { updatedAt: string | null; headline: string; threads: AradioThread[] };

export type AradioAudio = { key: string; durationS: number | null; bytes: number | null };

export type AradioBulletinEntry = {
  id: string;
  airedAt: string;
  headline: string;
  /** Validated path relative to /research/aradio/, or null when underivable. */
  path: string | null;
  audio: AradioAudio | null;
  covers: string[];
};

export type AradioIndex = {
  updatedAt: string | null;
  degraded: boolean;
  /** Newest first, de-duplicated by id, at most ARADIO_MAX_BULLETINS. */
  bulletins: AradioBulletinEntry[];
};

export type AradioLine = { speaker: string; text: string };

export type AradioBulletin = {
  id: string;
  airedAt: string;
  headline: string;
  lines: AradioLine[];
  covers: string[];
  threads: Array<{ slug: string; title: string; status: AradioThreadStatus }>;
  sources: AradioEvidence[];
  audio: AradioAudio | null;
  editorModel: string | null;
};

export type AradioTranscriptState =
  | { kind: 'ready'; bulletin: AradioBulletin }
  | { kind: 'loading'; entry: AradioBulletinEntry }
  | { kind: 'error'; entry: AradioBulletinEntry }
  | { kind: 'none' };

export type AradioViewState = {
  language: UiLanguage;
  nowMs: number;
  index: AradioIndex | null;
  indexStatus: AradioLoadStatus;
  board: AradioBoard | null;
  boardStatus: AradioLoadStatus;
  /** Detail of the newest bulletin, for the hero's speaker strip. */
  latestDetail: AradioBulletin | null;
  selectedId: string | null;
  transcript: AradioTranscriptState;
  keepListening: boolean;
  showAll: boolean;
  checkedAt: number | null;
};

// ── Constants ─────────────────────────────────────────────────────────────

export const ARADIO_MAX_BULLETINS = 72;
/** The contract's ON AIR window: the latest bulletin aired < 2 h ago. */
export const ARADIO_ON_AIR_MS = 2 * 60 * 60 * 1000;
/** Rows shown before "Show all": a day of hourly bulletins at most. */
export const ARADIO_LOG_PREVIEW = 12;

const STATUSES: readonly AradioThreadStatus[] = ['escalating', 'developing', 'steady', 'resolved'];
const STATUS_ORDER: Record<AradioThreadStatus, number> = { escalating: 0, developing: 1, steady: 2, resolved: 3 };
const EVIDENCE_KINDS: readonly AradioEvidenceKind[] = ['podcast', 'video', 'earnings-call', 'earnings', 'twitter', 'ticket'];
// Spoken primary sources are the station's distinctive input (docs/aradio.md),
// so their chips are tinted; filings, posts and tickets stay neutral.
const SPOKEN_KINDS = new Set<AradioEvidenceKind>(['podcast', 'video', 'earnings-call']);

const SLUG_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SAFE_ID_RE = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$/;
const BULLETIN_ID_RE = /^(\d{4}-\d{2}-\d{2})-(\d{2})(\d{2})$/;
const BULLETIN_PATH_RE = /^bulletins\/\d{4}-\d{2}-\d{2}\/\d{4}\.json$/;
// audio/aradio/<id>.mp3 per the contract; nested segments are tolerated, but
// every segment must start alphanumeric, so `..` can never form a segment.
const AUDIO_KEY_RE = /^audio\/aradio\/(?:[A-Za-z0-9][A-Za-z0-9._-]*\/)*[A-Za-z0-9][A-Za-z0-9._-]*\.mp3$/;
// Relative evidence links resolve against the public site, never the viewer's
// origin, so a preview host cannot change where an evidence chip points.
const SITE_ORIGIN = 'https://ara.guzus.xyz';

// ── Primitive coercion ───────────────────────────────────────────────────

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

/** Trimmed string, whitespace-collapsed, capped; '' for anything else. */
function text(value: unknown, max: number): string {
  if (typeof value !== 'string') return '';
  const collapsed = value.replace(/\s+/g, ' ').trim();
  if (collapsed.length <= max) return collapsed;
  return collapsed.slice(0, Math.max(0, max - 1)).trimEnd() + '…';
}

function textOrNull(value: unknown, max: number): string | null {
  return text(value, max) || null;
}

function isoOrNull(value: unknown): string | null {
  if (typeof value !== 'string' || !value.trim()) return null;
  const ms = Date.parse(value);
  return Number.isFinite(ms) ? new Date(ms).toISOString() : null;
}

function msOf(iso: string | null): number {
  if (!iso) return 0;
  const ms = Date.parse(iso);
  return Number.isFinite(ms) ? ms : 0;
}

/** Only http(s) survives. Site-relative paths resolve against the public site. */
export function safeHttpUrl(value: unknown): string | null {
  if (typeof value !== 'string') return null;
  const raw = value.trim();
  if (!raw) return null;
  try {
    const url = raw.startsWith('/') && !raw.startsWith('//') ? new URL(raw, SITE_ORIGIN) : new URL(raw);
    return url.protocol === 'https:' || url.protocol === 'http:' ? url.href : null;
  } catch {
    return null;
  }
}

/**
 * Escape for BOTH text and attribute contexts. shared.ts's escapeHtml leaves
 * quotes intact, which is unsafe inside `attr="..."` — see render/pricing.ts.
 */
export function esc(value: unknown): string {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// ── Normalization ────────────────────────────────────────────────────────

/** `audio` may be `{key, bytes, duration_s}`, a bare key string, or null. */
export function normalizeAradioAudio(raw: unknown): AradioAudio | null {
  const key = typeof raw === 'string' ? raw.trim() : isRecord(raw) && typeof raw.key === 'string' ? raw.key.trim() : '';
  if (!AUDIO_KEY_RE.test(key)) return null;
  const duration = isRecord(raw) ? Number(raw.duration_s) : NaN;
  const bytes = isRecord(raw) ? Number(raw.bytes) : NaN;
  return {
    key,
    durationS: Number.isFinite(duration) && duration > 0 ? duration : null,
    bytes: Number.isFinite(bytes) && bytes > 0 ? Math.round(bytes) : null,
  };
}

/** `YYYY-MM-DD-HHMM` (the UTC run stamp) → ISO, else null. */
export function airedAtFromId(id: string): string | null {
  const match = BULLETIN_ID_RE.exec(id);
  if (!match) return null;
  return isoOrNull(`${match[1]}T${match[2]}:${match[3]}:00Z`);
}

/**
 * The bulletin file path relative to /research/aradio/. Prefers the index's
 * `path` (tolerating a `research/aradio/` prefix), falls back to the id, and
 * returns null rather than ever emitting an unvalidated path.
 */
export function aradioBulletinPath(entry: { id: string; path?: unknown }): string | null {
  if (typeof entry.path === 'string') {
    const cleaned = entry.path.trim().replace(/^\/+/, '').replace(/^research\/aradio\//, '');
    if (BULLETIN_PATH_RE.test(cleaned)) return cleaned;
  }
  const match = BULLETIN_ID_RE.exec(entry.id);
  return match ? `bulletins/${match[1]}/${match[2]}${match[3]}.json` : null;
}

function slugList(raw: unknown): string[] {
  if (!Array.isArray(raw)) return [];
  const out: string[] = [];
  for (const item of raw) {
    const slug = typeof item === 'string' ? item.trim() : '';
    if (SLUG_RE.test(slug) && slug.length <= 64 && !out.includes(slug)) out.push(slug);
  }
  return out;
}

function normalizeStatus(raw: unknown): AradioThreadStatus {
  const value = typeof raw === 'string' ? raw.trim().toLowerCase() : '';
  return (STATUSES as readonly string[]).includes(value) ? value as AradioThreadStatus : 'developing';
}

function normalizeKind(raw: unknown): AradioEvidenceKind {
  const value = typeof raw === 'string' ? raw.trim().toLowerCase() : '';
  return (EVIDENCE_KINDS as readonly string[]).includes(value) ? value as AradioEvidenceKind : 'other';
}

function normalizeEvidence(raw: unknown): AradioEvidence | null {
  if (!isRecord(raw)) return null;
  const url = safeHttpUrl(raw.url);
  if (!url) return null;
  let label = text(raw.label, 90);
  if (!label) {
    try {
      label = new URL(url).hostname.replace(/^www\./, '');
    } catch {
      label = url;
    }
  }
  return {
    url,
    kind: normalizeKind(raw.kind),
    label,
    at: isoOrNull(raw.at),
    speaker: textOrNull(raw.speaker, 80),
    // The validator drops quotes over 40 words; this cap only guards layout.
    quote: textOrNull(raw.quote, 360),
  };
}

function evidenceList(raw: unknown, max: number): AradioEvidence[] {
  if (!Array.isArray(raw)) return [];
  const out: AradioEvidence[] = [];
  const seen = new Set<string>();
  for (const item of raw) {
    const evidence = normalizeEvidence(item);
    if (!evidence || seen.has(evidence.url)) continue;
    seen.add(evidence.url);
    out.push(evidence);
    if (out.length >= max) break;
  }
  return out;
}

function normalizeThread(raw: unknown): AradioThread | null {
  if (!isRecord(raw)) return null;
  const slug = typeof raw.slug === 'string' ? raw.slug.trim() : '';
  const title = text(raw.title, 140);
  if (!SLUG_RE.test(slug) || slug.length > 64 || !title) return null;
  const importance = Math.round(Number(raw.importance));
  const history = (Array.isArray(raw.history) ? raw.history : [])
    .map((entry): AradioHistoryEntry | null => {
      if (!isRecord(entry)) return null;
      const change = text(entry.change, 300);
      return change ? { at: isoOrNull(entry.at), change } : null;
    })
    .filter((entry): entry is AradioHistoryEntry => entry !== null)
    // Newest first for display; entries without a time keep their order last.
    .sort((a, b) => msOf(b.at) - msOf(a.at));
  return {
    slug,
    title,
    status: normalizeStatus(raw.status),
    importance: Number.isFinite(importance) ? Math.min(5, Math.max(1, importance)) : 3,
    firstSeen: isoOrNull(raw.first_seen),
    updatedAt: isoOrNull(raw.updated_at),
    now: text(raw.now, 600),
    changed: text(raw.changed, 400),
    watch: text(raw.watch, 300),
    evidence: evidenceList(raw.evidence, 8),
    history,
  };
}

/** state.json → board. Null only when the payload is not an object at all. */
export function normalizeAradioBoard(raw: unknown): AradioBoard | null {
  if (!isRecord(raw)) return null;
  const threads: AradioThread[] = [];
  const seen = new Set<string>();
  for (const item of Array.isArray(raw.threads) ? raw.threads : []) {
    const thread = normalizeThread(item);
    if (!thread || seen.has(thread.slug)) continue;
    seen.add(thread.slug);
    threads.push(thread);
  }
  return { updatedAt: isoOrNull(raw.updated_at), headline: text(raw.headline, 200), threads };
}

function normalizeEntry(raw: unknown): AradioBulletinEntry | null {
  if (!isRecord(raw)) return null;
  const id = typeof raw.id === 'string' ? raw.id.trim() : '';
  if (!SAFE_ID_RE.test(id)) return null;
  const airedAt = isoOrNull(raw.aired_at) ?? airedAtFromId(id);
  if (!airedAt) return null;
  return {
    id,
    airedAt,
    headline: text(raw.headline, 200),
    path: aradioBulletinPath({ id, path: raw.path }),
    audio: normalizeAradioAudio(raw.audio),
    covers: slugList(raw.covers),
  };
}

/**
 * index.json → newest-first bulletin list. Order is recomputed from
 * `aired_at` instead of trusting the file, and `latest` (an entry object or an
 * id) is folded in so the hero can never disagree with the list.
 */
export function normalizeAradioIndex(raw: unknown): AradioIndex | null {
  if (!isRecord(raw)) return null;
  const byId = new Map<string, AradioBulletinEntry>();
  const candidates = Array.isArray(raw.bulletins) ? raw.bulletins.slice() : [];
  if (isRecord(raw.latest)) candidates.push(raw.latest);
  for (const item of candidates) {
    const entry = normalizeEntry(item);
    if (entry && !byId.has(entry.id)) byId.set(entry.id, entry);
  }
  const bulletins = Array.from(byId.values())
    .sort((a, b) => msOf(b.airedAt) - msOf(a.airedAt) || (a.id < b.id ? 1 : a.id > b.id ? -1 : 0))
    .slice(0, ARADIO_MAX_BULLETINS);
  return { updatedAt: isoOrNull(raw.updated_at), degraded: raw.degraded === true, bulletins };
}

// Audio tags are stripped by the writer for `lines`; this only matters when we
// fall back to the raw `script` (e.g. a bulletin written before `lines`).
const AUDIO_TAG_RE = /\[\/?[a-z_]+\]/gi;
const SCRIPT_LINE_RE = /^(Speaker [12]):\s*(.+)$/;

function normalizeLines(raw: Record<string, unknown>): AradioLine[] {
  const lines: AradioLine[] = [];
  if (Array.isArray(raw.lines)) {
    for (const item of raw.lines) {
      if (!isRecord(item)) continue;
      const line = text(item.text, 1200);
      if (line) lines.push({ speaker: text(item.speaker, 40), text: line });
    }
  }
  if (lines.length === 0 && Array.isArray(raw.script)) {
    for (const item of raw.script) {
      if (typeof item !== 'string') continue;
      const match = SCRIPT_LINE_RE.exec(item.trim());
      if (!match) continue;
      const line = text(match[2].replace(AUDIO_TAG_RE, ''), 1200);
      if (line) lines.push({ speaker: match[1], text: line });
    }
  }
  return lines.slice(0, 60);
}

/**
 * bulletins/YYYY-MM-DD/HHMM.json → bulletin detail. `fallback` is the index
 * entry that pointed at the file: the file was fetched by that entry's path,
 * so it supplies the id / time / headline when the file omits them.
 */
export function normalizeAradioBulletin(
  raw: unknown,
  fallback?: Pick<AradioBulletinEntry, 'id' | 'airedAt' | 'headline'>,
): AradioBulletin | null {
  if (!isRecord(raw)) return null;
  const ownId = typeof raw.id === 'string' ? raw.id.trim() : '';
  const id = fallback?.id ?? ownId;
  if (!SAFE_ID_RE.test(id)) return null;
  const airedAt = isoOrNull(raw.aired_at) ?? fallback?.airedAt ?? airedAtFromId(id);
  if (!airedAt) return null;
  const threads = (Array.isArray(raw.threads) ? raw.threads : [])
    .map((item) => {
      if (!isRecord(item)) return null;
      const slug = typeof item.slug === 'string' ? item.slug.trim() : '';
      const title = text(item.title, 140);
      return SLUG_RE.test(slug) && title ? { slug, title, status: normalizeStatus(item.status) } : null;
    })
    .filter((item): item is { slug: string; title: string; status: AradioThreadStatus } => item !== null);
  return {
    id,
    airedAt,
    headline: text(raw.headline, 200) || fallback?.headline || '',
    lines: normalizeLines(raw),
    covers: slugList(raw.covers),
    threads,
    sources: evidenceList(raw.sources, 24),
    audio: normalizeAradioAudio(raw.audio),
    editorModel: isRecord(raw.editor) ? textOrNull(raw.editor.model, 60) : null,
  };
}

// ── Pure logic ───────────────────────────────────────────────────────────

/** Unresolved first (escalating → developing → steady, then importance). */
export function sortAradioThreads(threads: readonly AradioThread[]): { open: AradioThread[]; resolved: AradioThread[] } {
  const byRecency = (a: AradioThread, b: AradioThread) => msOf(b.updatedAt) - msOf(a.updatedAt);
  const open = threads
    .filter((thread) => thread.status !== 'resolved')
    .sort((a, b) =>
      STATUS_ORDER[a.status] - STATUS_ORDER[b.status]
      || b.importance - a.importance
      || byRecency(a, b)
      || a.title.localeCompare(b.title));
  const resolved = threads
    .filter((thread) => thread.status === 'resolved')
    .sort((a, b) => byRecency(a, b) || a.title.localeCompare(b.title));
  return { open, resolved };
}

export type AradioAirState = { state: 'live' | 'idle' | 'none'; ageMs: number | null };

/** ON AIR when the newest bulletin aired less than two hours ago. */
export function aradioAirState(latestAiredAt: string | null | undefined, nowMs: number): AradioAirState {
  const aired = msOf(latestAiredAt ?? null);
  if (!aired) return { state: 'none', ageMs: null };
  // A viewer clock running behind the writer's must not show negative ages.
  const ageMs = Math.max(0, nowMs - aired);
  return { state: ageMs < ARADIO_ON_AIR_MS ? 'live' : 'idle', ageMs };
}

export type AradioQueueState = {
  heard: ReadonlySet<string>;
  /** Bulletins that aired while listening, oldest first; they play next. */
  queue: readonly string[];
  /** The oldest bulletin reached so far by "continue to earlier ones". */
  backCursor: string | null;
};

/**
 * What "keep listening" plays after a bulletin ends: first anything that
 * aired during the session (queued by the poller), then the next-older
 * unheard bulletin with audio. Text-only bulletins are skipped.
 */
export function pickNextAradioBulletin(
  bulletins: readonly AradioBulletinEntry[],
  state: AradioQueueState,
): { id: string; queue: string[]; backCursor: string | null } | null {
  const playable = (id: string) => bulletins.some((entry) => entry.id === id && entry.audio !== null);
  const queue = state.queue.slice();
  while (queue.length) {
    const id = queue.shift() as string;
    if (!state.heard.has(id) && playable(id)) return { id, queue, backCursor: state.backCursor };
  }
  let start = 0;
  if (state.backCursor) {
    const at = bulletins.findIndex((entry) => entry.id === state.backCursor);
    // The cursor aged out of the 72-entry index: there is nothing older left.
    if (at < 0) return null;
    start = at + 1;
  }
  for (let i = start; i < bulletins.length; i += 1) {
    const entry = bulletins[i];
    if (entry.audio && !state.heard.has(entry.id)) return { id: entry.id, queue, backCursor: entry.id };
  }
  return null;
}

/** Word-proportional [start, end) fractions per line — TTS pace is steady. */
export function aradioLineSpans(lines: readonly AradioLine[]): Array<[number, number]> {
  const counts = lines.map((line) => Math.max(1, line.text.split(/\s+/).filter(Boolean).length));
  const total = counts.reduce((sum, count) => sum + count, 0) || 1;
  let cursor = 0;
  return counts.map((count) => {
    const start = cursor / total;
    cursor += count;
    return [start, cursor / total];
  });
}

/** Speaker 1 / Speaker 2 → 1 / 2; anything else is shown verbatim. */
export function aradioSpeakerRole(speaker: string): 1 | 2 | 0 {
  const match = /^(?:speaker\s*)?([12])$/i.exec(speaker.trim());
  return match ? (Number(match[1]) as 1 | 2) : 0;
}

// ── Formatting ───────────────────────────────────────────────────────────

const pad2 = (value: number) => String(value).padStart(2, '0');

export function aradioUtcTime(iso: string): string {
  const date = new Date(iso);
  return Number.isNaN(date.getTime()) ? '--:--' : `${pad2(date.getUTCHours())}:${pad2(date.getUTCMinutes())}`;
}

export function aradioUtcDay(iso: string, language: UiLanguage, long = false): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return '';
  return date.toLocaleDateString(language === 'ko' ? 'ko-KR' : 'en-GB', {
    weekday: long ? 'long' : 'short',
    day: 'numeric',
    month: long ? 'long' : 'short',
    timeZone: 'UTC',
  });
}

export function aradioAge(iso: string | null, nowMs: number, language: UiLanguage): string {
  const then = msOf(iso);
  if (!then) return '';
  const mins = Math.floor(Math.max(0, nowMs - then) / 60000);
  if (mins < 1) return uiText(language, 'time.now');
  if (mins < 60) return uiText(language, 'time.minutesAgo', { count: mins });
  const hours = Math.floor(mins / 60);
  if (hours < 48) return uiText(language, 'time.hoursAgo', { count: hours });
  return uiText(language, 'time.daysAgo', { count: Math.floor(hours / 24) });
}

export function aradioDuration(seconds: number | null): string {
  if (seconds === null || !Number.isFinite(seconds) || seconds <= 0) return '';
  const whole = Math.round(seconds);
  return `${Math.floor(whole / 60)}:${pad2(whole % 60)}`;
}

/** The i18n keys a `data-aradio-rel-key` attribute may name (ticker refresh). */
export const ARADIO_REL_KEYS: readonly UiCopyKey[] = [
  'aradio.airedAgo', 'aradio.lastBulletin', 'aradio.updatedAgo', 'aradio.resolvedAgo', 'aradio.checked',
];

/** Relative-time span the ticker can refresh in place without a re-render. */
function relTime(iso: string | null, key: UiCopyKey, s: { nowMs: number; language: UiLanguage }, className = ''): string {
  if (!iso) return '';
  const age = aradioAge(iso, s.nowMs, s.language);
  return `<time class="${esc(className)}" datetime="${esc(iso)}" data-aradio-rel="${esc(iso)}" data-aradio-rel-key="${esc(key)}"`
    + ` title="${esc(iso.replace('T', ' ').slice(0, 16))} UTC">${esc(uiText(s.language, key, { age }))}</time>`;
}

function statusLabel(status: AradioThreadStatus, language: UiLanguage): string {
  return uiText(language, `aradio.status.${status}` as UiCopyKey);
}

function kindLabel(kind: AradioEvidenceKind, language: UiLanguage): string {
  return uiText(language, `aradio.kind.${kind}` as UiCopyKey);
}

function speakerLabel(speaker: string, language: UiLanguage): string {
  const role = aradioSpeakerRole(speaker);
  if (role === 1) return uiText(language, 'aradio.speaker1');
  if (role === 2) return uiText(language, 'aradio.speaker2');
  return speaker || uiText(language, 'aradio.speaker1');
}

// ── Rendering ────────────────────────────────────────────────────────────

/** Accessible name for a bulletin's play control. */
export function aradioPlayAria(entry: { airedAt: string; headline: string }, language: UiLanguage, playing: boolean): string {
  const time = aradioUtcTime(entry.airedAt);
  return playing
    ? uiText(language, 'aradio.pauseAria', { time })
    : uiText(language, 'aradio.playAria', { time, headline: entry.headline || time });
}

function renderEvidenceChip(evidence: AradioEvidence, language: UiLanguage): string {
  const spoken = SPOKEN_KINDS.has(evidence.kind) ? ' is-spoken' : '';
  return (
    `<a class="aradio-evidence aradio-evidence--${esc(evidence.kind)}${spoken}" href="${esc(evidence.url)}" target="_blank" rel="noopener noreferrer"`
    + ` title="${esc(evidence.label)}">`
    + `<span class="aradio-evidence-kind">${esc(kindLabel(evidence.kind, language))}</span>`
    + `<span class="aradio-evidence-label">${esc(evidence.label)}</span>`
    + '</a>'
  );
}

function renderQuotes(evidence: readonly AradioEvidence[]): string {
  const quoted = evidence.filter((item) => item.quote);
  if (!quoted.length) return '';
  return '<div class="aradio-quotes">' + quoted.map((item) => {
    const who = [item.speaker, item.label].filter(Boolean).join(', ');
    return `<blockquote class="aradio-quote" cite="${esc(item.url)}"><p>${esc(item.quote)}</p>`
      + (who ? `<footer>${esc(who)}</footer>` : '')
      + '</blockquote>';
  }).join('') + '</div>';
}

function renderSignal(importance: number, language: UiLanguage): string {
  const bars = [1, 2, 3, 4, 5].map((n) => `<i${n <= importance ? ' class="on"' : ''}></i>`).join('');
  return `<span class="aradio-signal" role="img" aria-label="${esc(uiText(language, 'aradio.importance', { value: importance }))}">${bars}</span>`;
}

function renderThread(thread: AradioThread, s: AradioViewState): string {
  const language = s.language;
  const facts = [
    thread.changed ? `<div><dt>${esc(uiText(language, 'aradio.changed'))}</dt><dd>${esc(thread.changed)}</dd></div>` : '',
    thread.watch ? `<div><dt>${esc(uiText(language, 'aradio.watch'))}</dt><dd>${esc(thread.watch)}</dd></div>` : '',
  ].join('');
  const evidence = thread.evidence.length
    ? `<ul class="aradio-evidence-list" aria-label="${esc(uiText(language, 'aradio.evidence'))}">`
      + thread.evidence.map((item) => `<li>${renderEvidenceChip(item, language)}</li>`).join('')
      + '</ul>'
    : '';
  const history = thread.history.length
    ? `<details class="aradio-history"><summary>${esc(uiText(language, 'aradio.history', { count: thread.history.length }))}</summary><ol>`
      + thread.history.map((entry) =>
        '<li>'
        + (entry.at ? `<time datetime="${esc(entry.at)}">${esc(aradioUtcDay(entry.at, language))} ${esc(aradioUtcTime(entry.at))}</time>` : '')
        + `<span>${esc(entry.change)}</span></li>`).join('')
      + '</ol></details>'
    : '';
  return [
    `<article class="aradio-thread aradio-thread--${thread.status}" id="aradio-thread-${esc(thread.slug)}" data-aradio-thread="${esc(thread.slug)}">`,
    '<div class="aradio-thread-meta">',
    `<span class="aradio-pill aradio-pill--${thread.status}">${esc(statusLabel(thread.status, language))}</span>`,
    renderSignal(thread.importance, language),
    relTime(thread.updatedAt, 'aradio.updatedAgo', s, 'aradio-thread-age'),
    '</div>',
    `<h3 class="aradio-thread-title">${esc(thread.title)}</h3>`,
    thread.now ? `<p class="aradio-thread-now">${esc(thread.now)}</p>` : '',
    facts ? `<dl class="aradio-facts">${facts}</dl>` : '',
    evidence,
    renderQuotes(thread.evidence),
    history,
    '</article>',
  ].join('');
}

function renderResolved(threads: readonly AradioThread[], s: AradioViewState): string {
  if (!threads.length) return '';
  const items = threads.map((thread) => [
    `<li class="aradio-resolved-item" id="aradio-thread-${esc(thread.slug)}" data-aradio-thread="${esc(thread.slug)}">`,
    `<h3>${esc(thread.title)}</h3>`,
    thread.changed ? `<p>${esc(thread.changed)}</p>` : '',
    relTime(thread.updatedAt, 'aradio.resolvedAgo', s, 'aradio-resolved-age'),
    '</li>',
  ].join('')).join('');
  return `<details class="aradio-resolved"><summary>${esc(uiText(s.language, 'aradio.resolvedSection', { count: threads.length }))}</summary>`
    + `<ul class="aradio-resolved-list">${items}</ul></details>`;
}

function renderBoard(s: AradioViewState): string {
  const language = s.language;
  const { open, resolved } = sortAradioThreads(s.board?.threads ?? []);
  let body: string;
  if (s.boardStatus === 'error' && !s.board) {
    body = `<p class="aradio-note">${esc(uiText(language, 'aradio.boardError'))} `
      + `<button type="button" class="aradio-text-button" data-retry>${esc(uiText(language, 'action.retry'))}</button></p>`;
  } else if (!s.board) {
    body = `<p class="aradio-note">${esc(uiText(language, 'aradio.boardMissing'))}</p>`;
  } else if (!open.length) {
    body = `<p class="aradio-note">${esc(uiText(language, 'aradio.boardEmpty'))}</p>`;
  } else {
    body = `<div class="aradio-thread-grid">${open.map((thread) => renderThread(thread, s)).join('')}</div>`;
  }
  const count = open.length === 1
    ? uiText(language, 'aradio.boardCountOne')
    : uiText(language, 'aradio.boardCount', { count: open.length });
  return [
    '<section class="content-card aradio-board" aria-labelledby="aradioBoardTitle">',
    '<header class="aradio-section-head">',
    `<h2 class="aradio-section-title" id="aradioBoardTitle">${esc(uiText(language, 'aradio.board'))}</h2>`,
    s.board
      ? `<p class="aradio-section-meta"><span>${esc(count)}</span>${relTime(s.board.updatedAt, 'aradio.updatedAgo', s)}</p>`
      : '',
    '</header>',
    body,
    renderResolved(resolved, s),
    '</section>',
  ].join('');
}

function playIconButton(entry: AradioBulletinEntry, language: UiLanguage, className: string): string {
  return `<button type="button" class="${esc(className)}" data-aradio-play="${esc(entry.id)}" aria-pressed="false"`
    + ` aria-label="${esc(aradioPlayAria(entry, language, false))}"><span class="aradio-mini-icon" aria-hidden="true"></span></button>`;
}

/** The speaker strip: one segment per line, width ∝ words, coloured by host. */
export function renderAradioStrip(id: string | null, lines: readonly AradioLine[]): string {
  if (!id || !lines.length) {
    return '<div class="aradio-strip is-placeholder" aria-hidden="true"></div>';
  }
  const segments = lines.map((line) => {
    const words = Math.max(1, line.text.split(/\s+/).filter(Boolean).length);
    return `<span class="aradio-strip-seg aradio-strip-seg--${aradioSpeakerRole(line.speaker)}" style="flex-grow:${words}"></span>`;
  }).join('');
  return `<div class="aradio-strip" data-aradio-strip="${esc(id)}" aria-hidden="true">${segments}<span class="aradio-strip-veil"></span></div>`;
}

function renderHero(s: AradioViewState): string {
  const language = s.language;
  const latest = s.index?.bulletins[0] ?? null;
  const air = aradioAirState(latest?.airedAt, s.nowMs);
  const updateChip = '<button type="button" class="aradio-update" data-aradio-apply hidden>'
    + '<span class="aradio-update-dot" aria-hidden="true"></span><span data-aradio-update-text></span>'
    + '<span class="aradio-update-time" data-aradio-update-time></span></button>';
  const sign = (state: AradioAirState['state']) =>
    `<p class="aradio-sign" data-aradio-sign data-aired="${esc(latest?.airedAt ?? '')}">`
    + '<span class="aradio-sign-lamp" aria-hidden="true"></span>'
    + `<span data-aradio-sign-text>${esc(uiText(language, state === 'live' ? 'aradio.onAir' : 'aradio.offAir'))}</span></p>`;

  if (!latest) {
    const failed = s.indexStatus === 'error';
    return [
      `<section class="content-card aradio-hero aradio-hero--none" aria-labelledby="aradioHeroHeadline">`,
      '<div class="aradio-hero-top">',
      sign('none'),
      `<span class="aradio-hero-age">${esc(uiText(language, 'aradio.noBulletinYet'))}</span>`,
      updateChip,
      '</div>',
      '<div class="aradio-hero-empty">',
      `<h2 class="aradio-headline" id="aradioHeroHeadline">${esc(uiText(language, failed ? 'aradio.errorTitle' : 'aradio.emptyTitle'))}</h2>`,
      `<p class="aradio-hero-copy">${esc(uiText(language, failed ? 'aradio.errorBody' : 'aradio.emptyBody'))}</p>`,
      failed
        ? `<button type="button" class="aradio-hero-action" data-retry>${esc(uiText(language, 'action.retry'))}</button>`
        : `<a class="aradio-hero-action" href="/today">${esc(uiText(language, 'aradio.emptyAction'))}</a>`,
      '</div>',
      '</section>',
    ].join('');
  }

  const duration = aradioDuration(latest.audio?.durationS ?? null);
  const lines = s.latestDetail && s.latestDetail.id === latest.id ? s.latestDetail.lines : [];
  const playControl = latest.audio
    ? `<button type="button" class="aradio-play" data-aradio-play="${esc(latest.id)}" aria-pressed="false" aria-label="${esc(aradioPlayAria(latest, language, false))}">`
      + '<span class="aradio-play-icon" aria-hidden="true"></span>'
      + `<span class="aradio-play-text"><span class="aradio-play-label" data-aradio-play-label>${esc(uiText(language, 'aradio.play'))}</span>`
      + `<span class="aradio-play-duration">${esc(duration || ' ')}</span></span></button>`
    : `<p class="aradio-no-audio">${esc(uiText(language, 'aradio.noAudioHint'))}</p>`;

  return [
    `<section class="content-card aradio-hero aradio-hero--${air.state}" aria-labelledby="aradioHeroHeadline" data-aradio-hero="${esc(latest.id)}">`,
    '<div class="aradio-hero-top">',
    sign(air.state),
    relTime(latest.airedAt, air.state === 'live' ? 'aradio.airedAgo' : 'aradio.lastBulletin', s, 'aradio-hero-age'),
    updateChip,
    '</div>',
    '<div class="aradio-hero-grid">',
    '<div class="aradio-clock">',
    `<time class="aradio-clock-time" datetime="${esc(latest.airedAt)}">${esc(aradioUtcTime(latest.airedAt))}</time>`,
    `<span class="aradio-clock-meta"><span class="aradio-clock-zone">UTC</span> ${esc(aradioUtcDay(latest.airedAt, language, true))}</span>`,
    '</div>',
    '<div class="aradio-hero-main">',
    `<h2 class="aradio-headline" id="aradioHeroHeadline">${esc(latest.headline || aradioUtcTime(latest.airedAt) + ' UTC')}</h2>`,
    '<div class="aradio-controls">',
    playControl,
    `<button type="button" class="aradio-switch" role="switch" aria-checked="${s.keepListening ? 'true' : 'false'}" data-aradio-keep aria-describedby="aradioKeepHint">`,
    '<span class="aradio-switch-track" aria-hidden="true"><span class="aradio-switch-thumb"></span></span>',
    `<span class="aradio-switch-label">${esc(uiText(language, 'aradio.keepListening'))}</span></button>`,
    '</div>',
    `<p class="aradio-keep-hint" id="aradioKeepHint">${esc(uiText(language, 'aradio.keepListeningHint'))}</p>`,
    `<div class="aradio-strip-slot" data-aradio-strip-slot>${renderAradioStrip(lines.length ? latest.id : null, lines)}</div>`,
    '<div class="aradio-strip-legend">',
    `<span class="aradio-legend-key aradio-legend-key--1">${esc(uiText(language, 'aradio.speaker1'))}</span>`,
    `<span class="aradio-legend-key aradio-legend-key--2">${esc(uiText(language, 'aradio.speaker2'))}</span>`,
    `<button type="button" class="aradio-text-button" data-aradio-read="${esc(latest.id)}">${esc(uiText(language, 'aradio.readTranscript'))}</button>`,
    '</div>',
    '</div>',
    '</div>',
    '</section>',
  ].join('');
}

/** The program log: bulletins grouped by UTC day, newest first. */
export function renderAradioLog(s: AradioViewState): string {
  const bulletins = s.index?.bulletins ?? [];
  const language = s.language;
  const visible = s.showAll ? bulletins : bulletins.slice(0, ARADIO_LOG_PREVIEW);
  const groups: Array<{ day: string; label: string; rows: AradioBulletinEntry[] }> = [];
  for (const entry of visible) {
    const day = entry.airedAt.slice(0, 10);
    let group = groups[groups.length - 1];
    if (!group || group.day !== day) {
      group = { day, label: aradioUtcDay(entry.airedAt, language, true), rows: [] };
      groups.push(group);
    }
    group.rows.push(entry);
  }
  const rows = groups.map((group) => [
    '<div class="aradio-log-day">',
    `<h3 class="aradio-log-date">${esc(group.label)}</h3>`,
    '<ol class="aradio-log-list">',
    group.rows.map((entry) => {
      const selected = entry.id === s.selectedId;
      const duration = entry.audio ? aradioDuration(entry.audio.durationS) : uiText(language, 'aradio.textOnly');
      return [
        `<li class="aradio-log-row${selected ? ' is-selected' : ''}${entry.audio ? '' : ' is-text-only'}" data-aradio-row="${esc(entry.id)}">`,
        entry.audio
          ? playIconButton(entry, language, 'aradio-log-play')
          : `<span class="aradio-log-noaudio" aria-hidden="true"></span>`,
        `<button type="button" class="aradio-log-select" data-aradio-select="${esc(entry.id)}" aria-controls="aradio-transcript"${selected ? ' aria-current="true"' : ''}>`,
        `<time class="aradio-log-time" datetime="${esc(entry.airedAt)}">${esc(aradioUtcTime(entry.airedAt))}</time>`,
        `<span class="aradio-log-headline">${esc(entry.headline || aradioUtcTime(entry.airedAt) + ' UTC')}</span>`,
        `<span class="aradio-log-duration">${esc(duration)}</span>`,
        '</button>',
        '</li>',
      ].join('');
    }).join(''),
    '</ol>',
    '</div>',
  ].join('')).join('');
  const more = bulletins.length > ARADIO_LOG_PREVIEW
    ? `<button type="button" class="aradio-more" data-aradio-more aria-expanded="${s.showAll ? 'true' : 'false'}">`
      + esc(s.showAll ? uiText(language, 'aradio.showFewer') : uiText(language, 'aradio.showAll', { count: bulletins.length }))
      + '</button>'
    : '';
  return rows + more;
}

/** The transcript panel for the selected bulletin. */
export function renderAradioTranscript(
  transcript: AradioTranscriptState,
  s: { language: UiLanguage; boardSlugs: ReadonlySet<string> },
): string {
  const language = s.language;
  const head = (entry: { airedAt: string } | null) => [
    '<header class="aradio-section-head">',
    `<h3 class="aradio-section-title" id="aradioTranscriptTitle">${esc(uiText(language, 'aradio.transcript'))}</h3>`,
    entry
      ? `<p class="aradio-section-meta"><time datetime="${esc(entry.airedAt)}">${esc(aradioUtcTime(entry.airedAt))} UTC</time> `
        + `<span>${esc(aradioUtcDay(entry.airedAt, language, true))}</span></p>`
      : '',
    '</header>',
  ].join('');
  if (transcript.kind === 'none') return '';
  if (transcript.kind === 'loading' || transcript.kind === 'error') {
    const loading = transcript.kind === 'loading';
    return [
      `<article class="aradio-transcript" aria-labelledby="aradioTranscriptTitle" aria-busy="${loading ? 'true' : 'false'}">`,
      head(transcript.entry),
      transcript.entry.headline ? `<p class="aradio-transcript-headline">${esc(transcript.entry.headline)}</p>` : '',
      `<p class="aradio-note">${esc(uiText(language, loading ? 'aradio.transcriptLoading' : 'aradio.transcriptError'))}`,
      loading ? '' : ` <button type="button" class="aradio-text-button" data-aradio-select="${esc(transcript.entry.id)}">${esc(uiText(language, 'action.retry'))}</button>`,
      '</p>',
      '</article>',
    ].join('');
  }
  const bulletin = transcript.bulletin;
  const spans = aradioLineSpans(bulletin.lines);
  const lines = bulletin.lines.map((line, i) => {
    const role = aradioSpeakerRole(line.speaker);
    return `<li class="aradio-line aradio-line--s${role}" data-aradio-line-start="${spans[i][0].toFixed(4)}" data-aradio-line-end="${spans[i][1].toFixed(4)}">`
      + `<span class="aradio-speaker">${esc(speakerLabel(line.speaker, language))}</span>`
      + `<p class="aradio-line-text">${esc(line.text)}</p></li>`;
  }).join('');
  const titles = new Map(bulletin.threads.map((thread) => [thread.slug, thread.title]));
  const covers = bulletin.covers.map((slug) => {
    const title = titles.get(slug) || slug.replace(/-/g, ' ');
    return s.boardSlugs.has(slug)
      ? `<li><button type="button" class="aradio-cover" data-aradio-goto="${esc(slug)}">${esc(title)}</button></li>`
      : `<li><span class="aradio-cover is-static">${esc(title)}</span></li>`;
  }).join('');
  const sources = bulletin.sources.map((item) => `<li>${renderEvidenceChip(item, language)}</li>`).join('');
  return [
    `<article class="aradio-transcript" aria-labelledby="aradioTranscriptTitle" data-aradio-transcript="${esc(bulletin.id)}">`,
    head(bulletin),
    bulletin.headline ? `<p class="aradio-transcript-headline">${esc(bulletin.headline)}</p>` : '',
    bulletin.audio
      ? `<button type="button" class="aradio-transcript-play" data-aradio-play="${esc(bulletin.id)}" aria-pressed="false" aria-label="${esc(aradioPlayAria(bulletin, language, false))}">`
        + `<span class="aradio-mini-icon" aria-hidden="true"></span><span data-aradio-play-label>${esc(uiText(language, 'aradio.play'))}</span></button>`
      : `<p class="aradio-note">${esc(uiText(language, 'aradio.noAudioHint'))}</p>`,
    lines ? `<ol class="aradio-lines">${lines}</ol>` : `<p class="aradio-note">${esc(uiText(language, 'aradio.transcriptError'))}</p>`,
    covers
      ? `<div class="aradio-transcript-foot"><h4>${esc(uiText(language, 'aradio.storylines'))}</h4><ul class="aradio-covers">${covers}</ul></div>`
      : '',
    sources
      ? `<div class="aradio-transcript-foot"><h4>${esc(uiText(language, 'aradio.sources'))}</h4><ul class="aradio-evidence-list">${sources}</ul></div>`
      : '',
    `<p class="aradio-credit">${esc(bulletin.editorModel
      ? uiText(language, 'aradio.credit', { model: bulletin.editorModel })
      : uiText(language, 'aradio.creditNoModel'))}</p>`,
    '</article>',
  ].join('');
}

function renderBulletins(s: AradioViewState): string {
  const bulletins = s.index?.bulletins ?? [];
  if (!bulletins.length) return '';
  const boardSlugs = new Set((s.board?.threads ?? []).map((thread) => thread.slug));
  return [
    '<section class="content-card aradio-bulletins" aria-labelledby="aradioBulletinsTitle">',
    '<div class="aradio-bulletins-grid">',
    '<div class="aradio-log">',
    '<header class="aradio-section-head">',
    `<h2 class="aradio-section-title" id="aradioBulletinsTitle">${esc(uiText(s.language, 'aradio.bulletins'))}</h2>`,
    `<p class="aradio-section-meta">${esc(uiText(s.language, 'aradio.bulletinsCount', { count: bulletins.length }))}</p>`,
    '</header>',
    `<div data-aradio-log>${renderAradioLog(s)}</div>`,
    '</div>',
    `<div class="aradio-transcript-slot" id="aradio-transcript" data-aradio-transcript-slot>${renderAradioTranscript(s.transcript, { language: s.language, boardSlugs })}</div>`,
    '</div>',
    '</section>',
  ].join('');
}

/** The masthead's "Checked N ago" line; re-rendered after every poll. */
export function renderAradioChecked(checkedAt: number | null, language: UiLanguage, nowMs: number): string {
  return checkedAt
    ? relTime(new Date(checkedAt).toISOString(), 'aradio.checked', { nowMs, language })
    : esc(uiText(language, 'aradio.checking'));
}

/** The whole /aradio view. Missing files render empty states, never throw. */
export function renderAradioView(s: AradioViewState): string {
  const language = s.language;
  const hasBulletins = Boolean(s.index?.bulletins.length);
  const hasBoard = Boolean(s.board?.threads.length);
  return [
    '<div class="aradio-view">',
    '<header class="aradio-masthead">',
    '<div>',
    `<h2 class="aradio-title">${esc(uiText(language, 'aradio.title'))}</h2>`,
    `<p class="aradio-tagline">${esc(uiText(language, 'aradio.tagline'))}</p>`,
    '</div>',
    `<p class="aradio-checked" data-aradio-checked>${renderAradioChecked(s.checkedAt, language, s.nowMs)}</p>`,
    // Announces a newly detected bulletin; the chip itself is a hidden button.
    '<p class="aradio-sr" aria-live="polite" data-aradio-live></p>',
    '</header>',
    renderHero(s),
    // Before the first run there is nothing to put on a board or in a log;
    // the hero alone carries the empty state instead of three empty cards.
    hasBulletins || hasBoard || s.boardStatus === 'error' ? renderBoard(s) : '',
    renderBulletins(s),
    '</div>',
  ].join('');
}
