/**
 * Aradio — ARA Radio, the rolling AI-news station, rendered from
 * research/aradio/*.json.
 *
 * Contract: docs/aradio.md ("Published files", "Audio", "Dashboard").
 *
 * RADIO FIRST
 * -----------
 * The page is a radio before it is a dashboard. One large button starts
 * continuous listening: the newest bulletin with audio first, then older ones,
 * skipping text-only bulletins; a bulletin that airs while someone listens
 * plays next. Above the fold there is only what a listener needs: the station,
 * whether it is on air, what is playing, a seek bar, previous/next and what
 * comes next. The situation board, the bulletin log and the transcripts sit
 * below it, "Behind the broadcast". The running order is a pure data
 * structure (`AradioProgramme`) so its rules are tested here, not in the DOM.
 * One bad file must not end the listening: a bulletin whose audio fails is
 * skipped and never retried by itself; when nothing left can play, the card
 * says so ("Couldn't play") and play tries again from the first one missed.
 *
 * WHY EVERYTHING HERE IS DEFENSIVE
 * --------------------------------
 * Every string is model output or third-party text relayed by the editor
 * agent (podcast speakers, filings, tweets). So:
 *   - every value is escaped for BOTH text and attribute contexts (`esc`) and
 *     the assembled HTML still goes through the app's DOMPurify sink;
 *   - URLs never travel through HTML strings. The markup carries an empty
 *     slot per evidence link; `hydrateAradioLinks` builds each <a> with DOM
 *     APIs from a fresh `new URL(raw)` parse (absolute http/https only),
 *     setting `href` as a property and the label via textContent. The podcast
 *     feed address is filled in the same way (`hydrateAradioFeed`);
 *   - an audio URL exists only via `aradioAudioSrc`, for a key matching
 *     ARADIO_AUDIO_KEY_RE; any other key means "this bulletin has no audio";
 *   - fetch paths are rebuilt from validated shapes (`aradioBulletinPath`),
 *     never taken verbatim, so a malformed index cannot point the page at an
 *     arbitrary URL.
 * Before the first editor run none of the files exist, and a schema bump must
 * degrade to "missing field", never to a crash — every field is optional.
 *
 * This module touches no globals (no `document`, no fetch): the DOM helpers
 * take the document/root as a parameter. main.ts owns state, polling and the
 * shared audio player (the site's ONE <audio> element); node tests import
 * this file directly.
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

/**
 * A listening session's running order: the ids of playable bulletins and the
 * one on now (`pos`). Built newest first from the index; a bulletin that airs
 * during the session is inserted right after the one on now. "Previous" walks
 * back through it, "next" forward, and "Up next" is what follows `pos`.
 * `failed` lists the bulletins whose audio did not load or play this session:
 * they stay in `ids` (so a poll never queues them again) but every step skips
 * them, so nothing is retried unless the listener asks.
 */
export type AradioProgramme = { readonly ids: readonly string[]; readonly pos: number; readonly failed?: readonly string[] };

/**
 * off = nothing of ours is playing; waiting = caught up, the next bulletin to
 * air plays; failed = stopped because nothing left in the running order could
 * play (play tries again).
 */
export type AradioRadioMode = 'off' | 'playing' | 'paused' | 'waiting' | 'failed';

/** What main.ts knows about the station and the shared player, as data. */
export type AradioRadioInput = {
  /** Every bulletin the page knows (the poller's newest index), newest first. */
  bulletins: readonly AradioBulletinEntry[];
  indexStatus: AradioLoadStatus;
  programme: AradioProgramme | null;
  /** The Aradio bulletin loaded in the shared player; null when it holds none. */
  loaded: AradioBulletinEntry | null;
  playing: boolean;
  /** The loaded bulletin played to its end. */
  ended: boolean;
  /** Caught up while listening: the next bulletin to air starts by itself. */
  waiting: boolean;
  buffering: boolean;
  position: number;
  duration: number;
  stopAfter: boolean;
};

export type AradioViewState = {
  language: UiLanguage;
  nowMs: number;
  /** The index the "Behind the broadcast" sections show (applied on request). */
  index: AradioIndex | null;
  indexStatus: AradioLoadStatus;
  board: AradioBoard | null;
  boardStatus: AradioLoadStatus;
  selectedId: string | null;
  transcript: AradioTranscriptState;
  /** The transcript is collapsed until the listener asks for it. */
  transcriptOpen: boolean;
  showAll: boolean;
  checkedAt: number | null;
  /** The radio card always reflects the newest data the poller has seen. */
  radio: AradioRadioInput;
  /** The radio card's own transcript: the bulletin `aradioScriptEntry` names. */
  script?: AradioTranscriptState;
  /** What this viewer has heard (localStorage), for the log's play pills. */
  listened?: AradioListened;
  /** This viewer's playback speed. */
  rate?: number;
};

// ── Constants ─────────────────────────────────────────────────────────────

export const ARADIO_MAX_BULLETINS = 72;
/** The contract's ON AIR window: the latest bulletin aired < 2 h ago. */
export const ARADIO_ON_AIR_MS = 2 * 60 * 60 * 1000;
/** Rows shown before "Show all": a day of hourly bulletins at most. */
export const ARADIO_LOG_PREVIEW = 12;
/** How many bulletins "Up next" lists. */
export const ARADIO_UP_NEXT = 3;
/** "Previous" restarts the bulletin on now when it is further in than this. */
export const ARADIO_RESTART_S = 3;
/** The podcast feed postbuild-seo.mjs writes (absolute URL is hydrated). */
export const ARADIO_FEED_PATH = '/aradio/feed.xml';
/** The show art, the same file the feed and the lock screen use (a test pins them). */
export const ARADIO_COVER_PATH = '/brand/aradio-cover.png';
/**
 * The show on Spotify, `https://open.spotify.com/show/<id>` (listed
 * 2026-11-01; docs/aradio.md, "Listing on Spotify"). Empty hides the button.
 */
export const ARADIO_SPOTIFY_SHOW_URL = 'https://open.spotify.com/show/6XPmQwa4EfqXz7S3Vs1Owb';
/** How far the skip buttons (and lock-screen skips without their own offset) jump. */
export const ARADIO_JUMP_S = 15;
/** The speeds the speed button cycles through. */
export const ARADIO_RATES: readonly number[] = [1, 1.25, 1.5, 2];
/**
 * Seconds of silence between two speakers' turns. Measured on the first real
 * bulletin (2026-10-31 08:53): turn changes left 0.4–0.75 s gaps.
 */
export const ARADIO_TURN_PAUSE_S = 0.5;

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
// The shared key policy: a flat audio/aradio/<name>.mp3 (docs/aradio.md uses
// audio/aradio/<id>.mp3). Nesting, traversal, another prefix or a full URL all
// fail, and a bulletin whose key fails is treated as having no audio.
// dashboard/scripts/aradio-feed.mjs mirrors it for the podcast feed (a parity
// test pins the two together).
export const ARADIO_AUDIO_KEY_RE = /^audio\/aradio\/[A-Za-z0-9._-]+\.mp3$/;

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

/**
 * The link guard: an absolute http(s) URL or null. `new URL(raw)` gets no
 * base, so relative and protocol-relative values throw and are rejected, as
 * is every other scheme (javascript:, data:, mailto:, …).
 */
export function parseAradioHttpUrl(raw: unknown): URL | null {
  if (typeof raw !== 'string' || !raw.trim()) return null;
  let url: URL;
  try {
    url = new URL(raw.trim());
  } catch {
    return null;
  }
  return url.protocol === 'https:' || url.protocol === 'http:' ? url : null;
}

/** Normalized href kept in the model; links are re-parsed when built. */
export function safeHttpUrl(value: unknown): string | null {
  return parseAradioHttpUrl(value)?.href ?? null;
}

/** The only way to an audio URL: `${base}/${key}` for a policy-valid key. */
export function aradioAudioSrc(base: string, audio: { key: string } | null | undefined): string | null {
  const key = audio?.key;
  return typeof key === 'string' && ARADIO_AUDIO_KEY_RE.test(key) ? `${base}/${key}` : null;
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
  if (!ARADIO_AUDIO_KEY_RE.test(key)) return null;
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
 * id) is folded in so the player can never disagree with the list.
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

/** ON AIR when the given bulletin aired less than two hours ago. */
export function aradioAirState(latestAiredAt: string | null | undefined, nowMs: number): AradioAirState {
  const aired = msOf(latestAiredAt ?? null);
  if (!aired) return { state: 'none', ageMs: null };
  // A viewer clock running behind the writer's must not show negative ages.
  const ageMs = Math.max(0, nowMs - aired);
  return { state: ageMs < ARADIO_ON_AIR_MS ? 'live' : 'idle', ageMs };
}

// ── The running order (continuous listening) ─────────────────────────────

/** Ids of the bulletins a listener can hear (policy-valid audio), newest first. */
export function aradioPlayableIds(bulletins: readonly AradioBulletinEntry[]): string[] {
  const out: string[] = [];
  for (const entry of bulletins) {
    if (entry.audio && !out.includes(entry.id)) out.push(entry.id);
  }
  return out;
}

/**
 * A new running order: every playable bulletin, newest first, positioned on
 * `startId` (default: the newest). Text-only bulletins are never in it, so
 * they are skipped by construction. Null when there is nothing to hear or
 * `startId` is not playable.
 */
export function startAradioProgramme(
  bulletins: readonly AradioBulletinEntry[],
  startId: string | null = null,
): AradioProgramme | null {
  const ids = aradioPlayableIds(bulletins);
  if (!ids.length) return null;
  const pos = startId === null ? 0 : ids.indexOf(startId);
  return pos < 0 ? null : { ids, pos };
}

/**
 * Fold a newer index into a running order. A playable bulletin the order has
 * not seen and that aired after everything in it is NEW: it goes right after
 * the bulletin on now — behind any earlier new ones, so several play in the
 * order they aired (each answers "what changed since the last one"). Anything
 * else unseen is appended. Returns the same object when nothing changed, so
 * callers can compare by identity.
 */
export function syncAradioProgramme(
  programme: AradioProgramme,
  bulletins: readonly AradioBulletinEntry[],
): AradioProgramme {
  const aired = new Map<string, number>();
  for (const entry of bulletins) if (!aired.has(entry.id)) aired.set(entry.id, msOf(entry.airedAt));
  const known = new Set(programme.ids);
  const unseen: AradioBulletinEntry[] = [];
  for (const entry of bulletins) {
    if (!entry.audio || known.has(entry.id)) continue;
    known.add(entry.id);
    unseen.push(entry);
  }
  if (!unseen.length) return programme;
  const newestKnown = programme.ids.reduce((max, id) => Math.max(max, aired.get(id) ?? 0), 0);
  const ids = programme.ids.slice();
  const onNow = aired.get(ids[programme.pos]) ?? 0;
  const fresh = unseen.filter((entry) => msOf(entry.airedAt) > newestKnown).reverse();
  for (const entry of fresh) {
    let at = programme.pos + 1;
    while (at < ids.length && (aired.get(ids[at]) ?? 0) > onNow) at += 1;
    ids.splice(at, 0, entry.id);
  }
  for (const entry of unseen) if (msOf(entry.airedAt) <= newestKnown) ids.push(entry.id);
  return { ...programme, ids };
}

/**
 * Move one bulletin forward (1) or back (-1), skipping any that left the
 * index, lost their audio or failed this session. Null at either end.
 */
export function stepAradioProgramme(
  programme: AradioProgramme,
  bulletins: readonly AradioBulletinEntry[],
  delta: 1 | -1,
): AradioProgramme | null {
  const playable = new Set(aradioPlayableIds(bulletins));
  for (let pos = programme.pos + delta; pos >= 0 && pos < programme.ids.length; pos += delta) {
    const id = programme.ids[pos];
    if (playable.has(id) && !aradioHasFailed(programme, id)) return { ...programme, pos };
  }
  return null;
}

/** The bulletin's audio failed to load or play in this listening session. */
export function aradioHasFailed(programme: AradioProgramme | null, id: string | null | undefined): boolean {
  return Boolean(programme && id && programme.failed?.includes(id));
}

/**
 * The bulletin on now (`id`) failed to load or play: record it and move to
 * the next bulletin that can still play. `skip` plays the returned order's
 * bulletin on now; `stop` means nothing playable is left after it, so the
 * radio stops and says so. Null when `id` is not the bulletin on now or has
 * already failed: the element's `error` and the rejected play() report the
 * same failure, and a late report about a bulletin already skipped past
 * changes nothing. A failed bulletin is never tried again by itself, so a
 * run of broken files (or a dead connection) ends in one stop, not a loop.
 */
export function failAradioProgramme(
  programme: AradioProgramme,
  bulletins: readonly AradioBulletinEntry[],
  id: string,
): { action: 'skip' | 'stop'; programme: AradioProgramme } | null {
  if (programme.ids[programme.pos] !== id || aradioHasFailed(programme, id)) return null;
  const failed: AradioProgramme = { ...programme, failed: [...(programme.failed ?? []), id] };
  const next = stepAradioProgramme(failed, bulletins, 1);
  return next ? { action: 'skip', programme: next } : { action: 'stop', programme: failed };
}

/**
 * "Try again" after a stop on failures: a fresh session (nothing failed),
 * starting at the first of the failures that stopped the radio — the listener
 * missed all of them, and the newest missed one plays first. A bulletin that
 * played before them (or was never reached) stays behind. Null when none of
 * what was missed can still play.
 */
export function retryAradioProgramme(
  programme: AradioProgramme,
  bulletins: readonly AradioBulletinEntry[],
): AradioProgramme | null {
  const playable = new Set(aradioPlayableIds(bulletins));
  let start = programme.pos;
  for (let pos = programme.pos - 1; pos >= 0; pos -= 1) {
    const id = programme.ids[pos];
    if (aradioHasFailed(programme, id)) start = pos;
    else if (playable.has(id)) break;
  }
  for (let pos = start; pos < programme.ids.length; pos += 1) {
    if (playable.has(programme.ids[pos])) return { ids: programme.ids, pos };
  }
  return null;
}

/** The next `count` playable bulletins after the one on now. */
export function aradioUpNext(
  programme: AradioProgramme,
  bulletins: readonly AradioBulletinEntry[],
  count = ARADIO_UP_NEXT,
): AradioBulletinEntry[] {
  const byId = new Map(bulletins.map((entry) => [entry.id, entry]));
  const out: AradioBulletinEntry[] = [];
  for (let pos = programme.pos + 1; pos < programme.ids.length && out.length < count; pos += 1) {
    const entry = byId.get(programme.ids[pos]);
    if (entry?.audio && !aradioHasFailed(programme, entry.id) && !out.includes(entry)) out.push(entry);
  }
  return out;
}

// ── The stall watchdog ───────────────────────────────────────────────────

/**
 * How long a bulletin the listener wants to hear may sit starved — not
 * playing on, and no audio arriving — before it counts as failed. A source
 * that hangs never errors, so without this the radio would buffer forever.
 */
export const ARADIO_STALL_MS = 20_000;

/** When the watchdog last saw the bulletin on now move, and where it was then. */
export type AradioStallWatch = {
  readonly id: string;
  /** currentTime, seconds. */
  readonly position: number;
  /** Seconds of audio buffered, all ranges together. */
  readonly buffered: number;
  /** The player's `progress` events so far. */
  readonly received: number;
  readonly since: number;
};

/** One look at the shared player, as data. */
export type AradioStallSample = {
  /** The radio bulletin in the player; null while it holds none (or holds the digest). */
  id: string | null;
  /** The listener wants sound: pressed play and has not paused since. */
  intent: boolean;
  paused: boolean;
  ended: boolean;
  /** Short of data to play on (readyState below HAVE_FUTURE_DATA). */
  starved: boolean;
  /** Some of this bulletin has played (the player's `played` ranges are not empty). */
  started: boolean;
  position: number;
  buffered: number;
  /** The player's `progress` events so far: a count that only grows. */
  received: number;
  /**
   * A monotonic clock in milliseconds (main.ts: performance.now()), so a jump
   * of the system clock can neither bring a skip forward nor hold one back.
   */
  nowMs: number;
};

/**
 * One step of the watchdog: what it watches now, and whether the bulletin is
 * stuck. Stuck = the listener wants sound, the player is trying to play and
 * says it is short of data, and in ARADIO_STALL_MS nothing has moved: not its
 * position, not its buffered audio, and — until playback has started — not a
 * single `progress` event, because Chrome reports no buffered range before
 * about 32 KB have arrived, so on a slow link those events are the only sign
 * of audio coming in. Any movement restarts the clock, so buffering that
 * recovers, or audio still arriving, never trips it. It compares the player's
 * own state between looks rather than counting timer ticks or event gaps, so
 * a page frozen behind a locked screen cannot mistake its own sleep for a
 * stall; a late look only delays the skip. Time comes only from `nowMs`.
 */
export function aradioStallStep(
  watch: AradioStallWatch | null,
  sample: AradioStallSample,
): { watch: AradioStallWatch | null; stalled: boolean } {
  if (!sample.id || !sample.intent || sample.paused || sample.ended) return { watch: null, stalled: false };
  const moved = !watch
    || watch.id !== sample.id
    || sample.position !== watch.position
    || sample.buffered > watch.buffered
    || (!sample.started && sample.received > watch.received);
  if (moved || !sample.starved) {
    const fresh = {
      id: sample.id, position: sample.position, buffered: sample.buffered, received: sample.received, since: sample.nowMs,
    };
    return { watch: fresh, stalled: false };
  }
  // A buffer that shrank is followed down, so audio arriving later still counts.
  const kept = sample.buffered < watch.buffered ? { ...watch, buffered: sample.buffered } : watch;
  return { watch: kept, stalled: sample.nowMs - kept.since >= ARADIO_STALL_MS };
}

/**
 * When the watchdog should look again: as the stall falls due, in whole
 * milliseconds rounded up and a few after. A timer takes whole milliseconds
 * and can fire a fraction of one before a finer monotonic clock says the time
 * has come; a look that lands that hair early finds nothing due and books
 * again, so the floor is short (50 ms) for it to try again at once.
 */
export function aradioStallRecheckMs(watch: AradioStallWatch, nowMs: number): number {
  return Math.max(50, Math.ceil(watch.since + ARADIO_STALL_MS - nowMs) + 5);
}

/** Everything the radio card shows, derived from `AradioRadioInput`. */
export type AradioRadioView = {
  /** ready = something to hear; none = nothing aired; text-only = aired, no audio. */
  kind: 'ready' | 'none' | 'text-only' | 'error';
  mode: AradioRadioMode;
  /** ON AIR is about what a listener can hear: the newest PLAYABLE bulletin. */
  air: AradioAirState;
  latestAiredAt: string | null;
  /** On now (playing / paused / last heard), or what pressing play starts. */
  now: AradioBulletinEntry | null;
  upNext: AradioBulletinEntry[];
  canPrevious: boolean;
  canNext: boolean;
  /** The newest bulletin, when it is text-only and newer than anything playable. */
  textOnlyNewest: AradioBulletinEntry | null;
  /** When the newest bulletin of any kind aired: the station's "Updated". */
  updatedAt: string | null;
  /** The bulletin whose transcript the card shows: `now`, or the newest when nothing can be heard. */
  scriptEntry: AradioBulletinEntry | null;
  elapsed: number;
  duration: number;
  seekable: boolean;
  buffering: boolean;
  stopAfter: boolean;
};

export function aradioRadioView(input: AradioRadioInput, nowMs: number): AradioRadioView {
  const bulletins = input.bulletins;
  const newest = bulletins[0] ?? null;
  const newestPlayable = bulletins.find((entry) => entry.audio) ?? null;
  const kind: AradioRadioView['kind'] = newestPlayable
    ? 'ready'
    : bulletins.length ? 'text-only' : input.indexStatus === 'error' ? 'error' : 'none';
  const loaded = input.loaded;
  // The player still holds the bulletin that failed last: the radio stopped on it.
  const mode: AradioRadioMode = loaded && aradioHasFailed(input.programme, loaded.id)
    ? 'failed'
    : loaded && input.waiting
      ? 'waiting'
      : loaded && !input.ended ? (input.playing ? 'playing' : 'paused') : 'off';
  // Off or stopped on a failure, the card shows what pressing play starts.
  const idle = mode === 'off' || mode === 'failed';

  let now: AradioBulletinEntry | null = null;
  let order: AradioProgramme | null = null;
  if (!idle) {
    now = loaded;
    order = input.programme;
  } else {
    // After failures, play tries again from the first bulletin missed; after
    // "stop after this bulletin", the next one in the running order;
    // otherwise the newest.
    const programme = loaded ? input.programme : null;
    const next = !programme
      ? null
      : mode === 'failed' ? retryAradioProgramme(programme, bulletins) : stepAradioProgramme(programme, bulletins, 1);
    order = next ?? startAradioProgramme(bulletins);
    const id = order ? order.ids[order.pos] : null;
    now = bulletins.find((entry) => entry.id === id) ?? null;
  }
  const upNext = mode === 'waiting' || !order ? [] : aradioUpNext(order, bulletins);
  const active = mode === 'playing' || mode === 'paused';
  const duration = idle
    ? now?.audio?.durationS ?? 0
    : input.duration > 0 ? input.duration : now?.audio?.durationS ?? 0;
  const elapsed = idle ? 0 : mode === 'waiting' ? duration : Math.max(0, Math.min(input.position, duration || input.position));
  return {
    kind,
    mode,
    air: aradioAirState(newestPlayable?.airedAt ?? null, nowMs),
    latestAiredAt: newestPlayable?.airedAt ?? null,
    now,
    upNext,
    canPrevious: !idle,
    canNext: active && Boolean(input.programme && stepAradioProgramme(input.programme, bulletins, 1)),
    textOnlyNewest: newest && !newest.audio && newestPlayable && msOf(newest.airedAt) > msOf(newestPlayable.airedAt)
      ? newest
      : null,
    updatedAt: newest?.airedAt ?? null,
    scriptEntry: kind === 'ready' ? now : kind === 'text-only' ? newest : null,
    elapsed,
    duration,
    seekable: active && input.duration > 0,
    buffering: mode === 'playing' && input.buffering,
    stopAfter: input.stopAfter,
  };
}

// ── Following the transcript ─────────────────────────────────────────────
//
// TTS returns audio, not timestamps, so where each line falls is ESTIMATED:
// a line takes time in proportion to its length in characters (spaces and
// punctuation included: they stand for the word breaks and pauses read into
// it), the speakers leave a short gap between turns, and the whole is scaled
// to the bulletin's real duration. On the only real bulletin so far
// (2026-10-31 08:53, 17 lines, 171.9 s; line starts measured from its audio)
// that is ~0.8 s off on average, ~2.8 s at worst, and on the right line ~92%
// of the time. Finer weights (acronyms and digits read out longhand,
// punctuation pauses) did no better there, so the estimate stays this simple
// until more bulletins say otherwise. The page says the timing is approximate
// and never shows a per-line time.

export type AradioLineTiming = { start: number; end: number };

/**
 * Estimated [start, end) seconds of each line in a bulletin `durationS` long.
 * The lines tile the bulletin exactly (the first starts at 0, each ends where
 * the next starts, the last at `durationS`); the gap after a line counts as
 * part of it, so the line just read stays current until the next one starts.
 * Null without a usable duration.
 */
export function aradioLineTimings(lines: readonly { text: string }[], durationS: number): AradioLineTiming[] | null {
  if (!Number.isFinite(durationS) || durationS <= 0) return null;
  if (!lines.length) return [];
  const weights = lines.map((line) => Math.max(1, line.text.length));
  const total = weights.reduce((sum, weight) => sum + weight, 0);
  const gaps = lines.length - 1;
  // The pauses never take more than a fifth of a (suspiciously short) bulletin.
  const pause = gaps ? Math.min(ARADIO_TURN_PAUSE_S, (durationS * 0.2) / gaps) : 0;
  const perWeight = (durationS - pause * gaps) / total;
  const starts: number[] = [];
  let cursor = 0;
  for (const weight of weights) {
    starts.push(cursor);
    cursor += weight * perWeight + pause;
  }
  return starts.map((start, i) => ({ start, end: i + 1 < starts.length ? starts[i + 1] : durationS }));
}

/** The line being read at `positionS`: -1 without timings or before the start. */
export function aradioLiveLine(timings: readonly AradioLineTiming[] | null, positionS: number): number {
  if (!timings?.length || !Number.isFinite(positionS) || positionS < 0) return -1;
  for (let i = timings.length - 1; i > 0; i -= 1) {
    if (positionS >= timings[i].start) return i;
  }
  return 0;
}

/**
 * The line of `bulletin` the shared player is reading: -1 when the player
 * holds another bulletin (or a failed one), the line count once it has played
 * to its end, so every line reads as heard.
 */
export function aradioPlayerLine(
  radio: Pick<AradioRadioInput, 'loaded' | 'programme' | 'ended' | 'waiting' | 'position' | 'duration'>,
  bulletin: { id: string; lines: readonly AradioLine[]; audio: AradioAudio | null },
): number {
  const loaded = radio.loaded;
  if (!loaded || loaded.id !== bulletin.id || !bulletin.lines.length || aradioHasFailed(radio.programme, loaded.id)) return -1;
  if (radio.ended || radio.waiting) return bulletin.lines.length;
  const duration = radio.duration > 0 ? radio.duration : bulletin.audio?.durationS ?? loaded.audio?.durationS ?? 0;
  return aradioLiveLine(aradioLineTimings(bulletin.lines, duration), radio.position);
}

// ── Playback speed ───────────────────────────────────────────────────────

/** A stored or requested speed, if it is one the button offers; else 1. */
export function aradioParseRate(raw: unknown): number {
  const rate = typeof raw === 'string' ? Number(raw.trim()) : typeof raw === 'number' ? raw : NaN;
  return ARADIO_RATES.includes(rate) ? rate : 1;
}

/** The speed after `rate` (wrapping round to 1×). */
export function aradioNextRate(rate: number): number {
  const at = ARADIO_RATES.indexOf(aradioParseRate(rate));
  return ARADIO_RATES[(at + 1) % ARADIO_RATES.length];
}

export function aradioRateLabel(rate: number): string {
  return `${aradioParseRate(rate)}×`;
}

// ── What this viewer has heard ───────────────────────────────────────────
//
// Kept in the viewer's own localStorage (main.ts reads and writes it inside
// try/catch), so it is a convenience, never a record: a private window, a
// cleared site or a blocked store simply shows every bulletin as new. Only
// the log's play pills read it; playback itself always starts a bulletin
// from the top, as a radio does.

/** One bulletin's listening: where the viewer got to, out of how long, and whether they finished. */
export type AradioListen = { at: number; duration: number; done: boolean };
export type AradioListened = Readonly<Record<string, AradioListen>>;
export type AradioListenState = { state: 'new' | 'partial' | 'done'; fraction: number; remaining: number };

/** The localStorage keys main.ts uses. */
export const ARADIO_LISTENED_KEY = 'ara.aradio.listened.v1';
export const ARADIO_RATE_KEY = 'ara.aradio.rate.v1';
/** Bulletins remembered: the index's 72 and some slack for ones that aged out. */
export const ARADIO_LISTENED_MAX = 120;
/** Under this many seconds in, a bulletin still counts as unheard. */
const LISTEN_STARTED_S = 3;
/** Within this many seconds of the end counts as heard. */
const LISTEN_DONE_SLACK_S = 3;

function listenOf(raw: unknown): AradioListen | null {
  if (!isRecord(raw)) return null;
  const at = Number(raw.at);
  const duration = Number(raw.duration);
  if (!Number.isFinite(at) || at < 0 || !Number.isFinite(duration) || duration <= 0) return null;
  return { at: Math.min(at, duration), duration, done: raw.done === true };
}

/** This viewer's listening of bulletin `id`, never an inherited property ("constructor" is a valid id). */
export function aradioListenOf(listened: AradioListened | null | undefined, id: string): AradioListen | undefined {
  return listened && Object.prototype.hasOwnProperty.call(listened, id) ? listened[id] : undefined;
}

/** Parse what localStorage held. Anything malformed is dropped, never thrown. */
export function aradioParseListened(raw: string | null | undefined): AradioListened {
  if (typeof raw !== 'string' || !raw) return {};
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return {};
  }
  if (!isRecord(parsed)) return {};
  const out: Record<string, AradioListen> = {};
  for (const [id, value] of Object.entries(parsed)) {
    const listen = SAFE_ID_RE.test(id) ? listenOf(value) : null;
    if (listen) out[id] = listen;
    if (Object.keys(out).length >= ARADIO_LISTENED_MAX) break;
  }
  return out;
}

/**
 * Record that the viewer is `positionS` into bulletin `id` (`ended`: it
 * played to its end). Finishing is sticky: replaying a heard bulletin moves
 * its position but it stays heard. Returns the same object when nothing a
 * pill shows would change, so callers can skip the write.
 */
export function aradioRecordListen(
  listened: AradioListened,
  id: string,
  positionS: number,
  durationS: number,
  ended = false,
): AradioListened {
  if (!SAFE_ID_RE.test(id) || !Number.isFinite(durationS) || durationS <= 0) return listened;
  const at = ended ? durationS : Math.max(0, Math.min(Number.isFinite(positionS) ? positionS : 0, durationS));
  const prior = aradioListenOf(listened, id);
  const done = Boolean(prior?.done) || ended || at >= durationS - LISTEN_DONE_SLACK_S;
  if (prior && prior.done === done && Math.abs(prior.at - at) < 1 && prior.duration === durationS) return listened;
  if (!prior && at < LISTEN_STARTED_S && !done) return listened;
  return { ...listened, [id]: { at, duration: durationS, done } };
}

/** Keep only bulletins still in `keepIds` (the index), at most ARADIO_LISTENED_MAX. */
export function aradioPruneListened(listened: AradioListened, keepIds: Iterable<string>): AradioListened {
  const out: Record<string, AradioListen> = {};
  for (const id of keepIds) {
    const listen = aradioListenOf(listened, id);
    if (listen) out[id] = listen;
    if (Object.keys(out).length >= ARADIO_LISTENED_MAX) break;
  }
  return Object.keys(out).length === Object.keys(listened).length ? listened : out;
}

/** What a play pill shows for one bulletin. */
export function aradioListenState(listen: AradioListen | null | undefined, durationS: number | null): AradioListenState {
  const duration = listen?.duration ?? durationS ?? 0;
  if (listen?.done) return { state: 'done', fraction: 1, remaining: 0 };
  if (!listen || duration <= 0 || listen.at < LISTEN_STARTED_S) return { state: 'new', fraction: 0, remaining: duration };
  return { state: 'partial', fraction: Math.min(1, listen.at / duration), remaining: Math.max(0, duration - listen.at) };
}

// ── Following the show in a podcast app ──────────────────────────────────
//
// None of these links can be checked from a web page (an app's URL scheme is
// either handled or not), so each is offered only where its app can exist,
// and the feed address with Copy stays as the fallback everywhere.
//   - Apple Podcasts: `podcast://<feed without its scheme>` (iPhone, iPad, Mac)
//     opens the app's "Follow a Show by URL" box, prefilled. The app fills it
//     in as http://, which the site redirects to https.
//   - Overcast: its documented subscribe link, iPhone and iPad only.
//   - Pocket Casts: `pktc://subscribe/…` on iPhone, iPad and Android (the
//     apps); elsewhere its web player's follow URL.
//   - Spotify cannot follow an RSS feed: the show URL, once it is listed.

export type AradioPlatform = 'ios' | 'mac' | 'android' | 'other';
export type AradioFollowApp = 'apple' | 'spotify' | 'overcast' | 'pocketcasts';
/** `newTab`: an https page, opened beside the radio so it keeps playing. */
export type AradioFollowLink = { app: AradioFollowApp; href: string; newTab: boolean };

export const ARADIO_FOLLOW_APPS: readonly AradioFollowApp[] = ['apple', 'spotify', 'overcast', 'pocketcasts'];
const SPOTIFY_SHOW_RE = /^https:\/\/open\.spotify\.com\/show\/[A-Za-z0-9]{22}$/;

/**
 * The viewer's platform from its user agent. iPadOS Safari reports a Mac user
 * agent, so a "Mac" with a multi-touch screen is an iPad.
 */
export function aradioPlatform(userAgent: string, maxTouchPoints = 0): AradioPlatform {
  const ua = typeof userAgent === 'string' ? userAgent : '';
  if (/\b(iPhone|iPad|iPod)\b/.test(ua)) return 'ios';
  if (/\bMacintosh\b/.test(ua)) return maxTouchPoints > 1 ? 'ios' : 'mac';
  if (/\bAndroid\b/.test(ua)) return 'android';
  return 'other';
}

/** The follow links to offer on `platform`, in display order. */
export function aradioFollowLinks(
  feedUrl: string,
  platform: AradioPlatform,
  spotifyShowUrl: string = ARADIO_SPOTIFY_SHOW_URL,
): AradioFollowLink[] {
  const feed = parseAradioHttpUrl(feedUrl);
  const links: AradioFollowLink[] = [];
  if (feed?.protocol === 'https:') {
    const bare = `${feed.host}${feed.pathname}${feed.search}`;
    if (platform === 'ios' || platform === 'mac') links.push({ app: 'apple', href: `podcast://${bare}`, newTab: false });
    if (platform === 'ios') {
      links.push({ app: 'overcast', href: `overcast://x-callback-url/add?url=${encodeURIComponent(feed.href)}`, newTab: false });
    }
    links.push(platform === 'ios' || platform === 'android'
      ? { app: 'pocketcasts', href: `pktc://subscribe/${bare}`, newTab: false }
      : { app: 'pocketcasts', href: `https://pocketcasts.com/follow/${feed.href}`, newTab: true });
  }
  const spotify = typeof spotifyShowUrl === 'string' ? spotifyShowUrl.trim() : '';
  if (SPOTIFY_SHOW_RE.test(spotify)) links.push({ app: 'spotify', href: spotify, newTab: true });
  return links.sort((a, b) => ARADIO_FOLLOW_APPS.indexOf(a.app) - ARADIO_FOLLOW_APPS.indexOf(b.app));
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

/** m:ss for the seek bar; whole seconds, never negative. */
export function aradioClock(seconds: number): string {
  const whole = Number.isFinite(seconds) && seconds > 0 ? Math.floor(seconds) : 0;
  return `${Math.floor(whole / 60)}:${pad2(whole % 60)}`;
}

/** The i18n keys a `data-aradio-rel-key` attribute may name (ticker refresh). */
export const ARADIO_REL_KEYS: readonly UiCopyKey[] = [
  'aradio.updatedAgo', 'aradio.resolvedAgo', 'aradio.checked', 'aradio.updated',
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

function headlineOf(entry: { airedAt: string; headline: string }): string {
  return entry.headline || `${aradioUtcTime(entry.airedAt)} UTC`;
}

// ── Links (built with DOM APIs, never as HTML strings) ─────────────────────

/** An evidence link that a slot in the rendered HTML stands for. */
export type AradioLinkSpec = { url: string; kind: AradioEvidenceKind; kindLabel: string; label: string };

/** Rendered HTML (which contains no URLs) plus the links its slots stand for. */
export type AradioRender = { html: string; links: AradioLinkSpec[] };

const LINK_KINDS = new Set<AradioEvidenceKind>([...EVIDENCE_KINDS, 'other']);

/**
 * Build one evidence link. The URL is parsed again here (the spec may not
 * have come through normalization); `href` is assigned as a property and the
 * labels as textContent, so no third-party string is ever parsed as HTML.
 */
export function createAradioEvidenceLink(doc: Document, spec: AradioLinkSpec): HTMLAnchorElement | null {
  const url = parseAradioHttpUrl(spec.url);
  if (!url) return null;
  const kind: AradioEvidenceKind = LINK_KINDS.has(spec.kind) ? spec.kind : 'other';
  const anchor = doc.createElement('a');
  anchor.className = `aradio-evidence aradio-evidence--${kind}${SPOKEN_KINDS.has(kind) ? ' is-spoken' : ''}`;
  anchor.href = url.href;
  anchor.target = '_blank';
  anchor.rel = 'noopener noreferrer';
  anchor.title = String(spec.label);
  const kindEl = doc.createElement('span');
  kindEl.className = 'aradio-evidence-kind';
  kindEl.textContent = String(spec.kindLabel);
  const labelEl = doc.createElement('span');
  labelEl.className = 'aradio-evidence-label';
  labelEl.textContent = String(spec.label);
  anchor.append(kindEl, labelEl);
  return anchor;
}

/** Replace every `[data-aradio-link]` slot under `root` with its built link. */
export function hydrateAradioLinks(root: ParentNode, links: readonly AradioLinkSpec[]): void {
  root.querySelectorAll<HTMLElement>('[data-aradio-link]').forEach((slot) => {
    const spec = links[Number(slot.dataset.aradioLink)];
    const anchor = spec ? createAradioEvidenceLink(slot.ownerDocument, spec) : null;
    if (anchor) {
      slot.replaceWith(anchor);
      return;
    }
    // A link that cannot be built leaves no empty chip behind.
    (slot.closest('li') ?? slot).remove();
  });
}

/**
 * Fill the podcast-feed address. It is the site's own constant path on the
 * site's own origin, set as a property like every other URL on this page.
 */
export function hydrateAradioFeed(root: ParentNode, feedUrl: string): void {
  const url = parseAradioHttpUrl(feedUrl);
  root.querySelectorAll<HTMLInputElement>('[data-aradio-feed-url]').forEach((input) => {
    input.value = url ? url.href : '';
  });
}

/**
 * Give each follow button its link (`aradioFollowLinks`), as a property like
 * every URL on this page, and show only the buttons that got one. The HTML
 * carries no addresses: an app this platform cannot have stays hidden.
 */
export function hydrateAradioFollow(root: ParentNode, links: readonly AradioFollowLink[]): void {
  root.querySelectorAll<HTMLElement>('[data-aradio-follow-list]').forEach((list) => {
    let shown = 0;
    list.querySelectorAll<HTMLAnchorElement>('a[data-aradio-follow]').forEach((anchor) => {
      const link = links.find((item) => item.app === anchor.dataset.aradioFollow);
      const item = anchor.closest('li') ?? anchor;
      item.hidden = !link;
      if (!link) {
        anchor.removeAttribute('href');
        return;
      }
      shown += 1;
      anchor.href = link.href;
      if (link.newTab) {
        anchor.target = '_blank';
        anchor.rel = 'noopener noreferrer';
      } else {
        anchor.removeAttribute('target');
        anchor.removeAttribute('rel');
      }
    });
    list.hidden = shown === 0;
  });
}

// ── Rendering: the radio ─────────────────────────────────────────────────

/** Accessible name for a bulletin's play control (log rows, transcript). */
export function aradioPlayAria(entry: { airedAt: string; headline: string }, language: UiLanguage, playing: boolean): string {
  const time = aradioUtcTime(entry.airedAt);
  return playing
    ? uiText(language, 'aradio.pauseAria', { time })
    : uiText(language, 'aradio.playAria', { time, headline: entry.headline || time });
}

/** Every string the radio card shows. The renderer and main.ts's in-place patcher share it. */
export type AradioRadioCopy = {
  badge: string;
  /** ON AIR: the newest bulletin with audio aired under two hours ago. */
  live: boolean;
  /** OFF AIR: nothing to hear at all (the card's shape changes with it). */
  off: boolean;
  label: string;
  headline: string;
  time: string;
  day: string;
  datetime: string;
  toggleLabel: string;
  toggleIcon: 'play' | 'pause';
  elapsed: string;
  remaining: string;
  seekMax: number;
  seekValue: number;
  seekText: string;
  progressPct: string;
  note: string;
  upNextEmpty: string;
  /** "Updated 12 min ago." for the newest bulletin of any kind; '' before the first. */
  updated: string;
  updatedIso: string;
  /** Off air the sign already gives that age ("Latest bulletin · 3h ago"); it is not said twice. */
  updatedShown: boolean;
};

export function aradioRadioCopy(view: AradioRadioView, nowMs: number, language: UiLanguage): AradioRadioCopy {
  const t = (key: UiCopyKey, params?: Record<string, string | number>) => uiText(language, key, params);
  const live = view.kind === 'ready' && view.air.state === 'live';
  const badge = view.kind !== 'ready'
    ? t('aradio.offAir')
    : live ? t('aradio.onAir') : t('aradio.latestAgo', { age: aradioAge(view.latestAiredAt, nowMs, language) });
  const labels: Record<AradioRadioMode, UiCopyKey> = {
    off: 'aradio.upFirst', playing: 'aradio.nowPlaying', paused: 'aradio.paused', waiting: 'aradio.caughtUp',
    failed: 'aradio.couldNotPlay',
  };
  const toggles: Record<AradioRadioMode, UiCopyKey> = {
    off: 'aradio.playStation', playing: 'aradio.pauseStation', paused: 'aradio.resumeStation', waiting: 'aradio.turnOff',
    failed: 'aradio.tryAgain',
  };
  const now = view.now;
  const duration = view.duration > 0 ? view.duration : 0;
  const seekMax = Math.max(1, Math.round(duration));
  const seekValue = Math.min(seekMax, Math.round(view.elapsed));
  // Caught up needs no note: "Up next" already says new bulletins play as they air.
  // A stop on failures always says why, so it is never a silent "Paused".
  const note = view.mode === 'failed'
    ? t('aradio.failedNote')
    : view.textOnlyNewest
      ? t('aradio.textOnlyNewest', { time: aradioUtcTime(view.textOnlyNewest.airedAt) })
      : '';
  return {
    badge,
    live,
    off: view.kind !== 'ready',
    label: t(labels[view.mode]),
    headline: now ? headlineOf(now) : '',
    time: now ? `${aradioUtcTime(now.airedAt)} UTC` : '',
    day: now ? aradioUtcDay(now.airedAt, language, true) : '',
    datetime: now?.airedAt ?? '',
    toggleLabel: t(toggles[view.mode]),
    toggleIcon: view.mode === 'playing' || view.mode === 'waiting' ? 'pause' : 'play',
    elapsed: aradioClock(view.elapsed),
    remaining: duration > 0 ? `−${aradioClock(Math.max(0, duration - view.elapsed))}` : '−-:--',
    seekMax,
    seekValue,
    seekText: t('aradio.seekValue', { elapsed: aradioClock(view.elapsed), duration: duration > 0 ? aradioClock(duration) : '--:--' }),
    progressPct: `${duration > 0 ? Math.min(100, (view.elapsed / duration) * 100).toFixed(2) : '0.00'}%`,
    note,
    upNextEmpty: t('aradio.upNextEmpty'),
    updated: view.updatedAt ? t('aradio.updated', { age: aradioAge(view.updatedAt, nowMs, language) }) : '',
    updatedIso: view.updatedAt ?? '',
    updatedShown: Boolean(view.updatedAt) && (live || view.kind !== 'ready' || view.updatedAt !== view.latestAiredAt),
  };
}

/** The "Up next" rows: text only, nothing focusable, so it can be swapped freely. */
export function renderAradioUpNext(view: AradioRadioView, copy: AradioRadioCopy): string {
  if (!view.upNext.length) return `<li class="aradio-upnext-empty">${esc(copy.upNextEmpty)}</li>`;
  return view.upNext.map((entry) => '<li class="aradio-upnext-item">'
    + `<time class="aradio-upnext-time" datetime="${esc(entry.airedAt)}">${esc(aradioUtcTime(entry.airedAt))}</time>`
    + `<span class="aradio-upnext-headline">${esc(headlineOf(entry))}</span>`
    + `<span class="aradio-upnext-duration">${esc(aradioDuration(entry.audio?.durationS ?? null))}</span></li>`).join('');
}

const ICON_PLAY_PAUSE = '<svg class="aradio-toggle-icon" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
  + '<path class="aradio-icon-play" d="M18 12.5v23a1.5 1.5 0 0 0 2.3 1.27l18.2-11.5a1.5 1.5 0 0 0 0-2.54l-18.2-11.5A1.5 1.5 0 0 0 18 12.5z"/>'
  + '<path class="aradio-icon-pause" d="M14 12h7v24h-7zM27 12h7v24h-7z"/></svg>';
const ICON_PREVIOUS = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 5h2.2v14H6zM20 5.6v12.8a.8.8 0 0 1-1.22.68L9.2 12.68a.8.8 0 0 1 0-1.36l9.58-6.4A.8.8 0 0 1 20 5.6z"/></svg>';
const ICON_NEXT = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M15.8 5H18v14h-2.2zM4 5.6v12.8a.8.8 0 0 0 1.22.68l9.58-6.4a.8.8 0 0 0 0-1.36L5.22 4.92A.8.8 0 0 0 4 5.6z"/></svg>';
// A ring open at the upper left with its arrow at the top: turn back. The
// forward icon is its mirror image. The seconds sit in the ring as text.
const ICON_JUMP_BACK = '<svg class="aradio-jump-ring" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
  + '<path d="M16 5a11 11 0 1 1-9.53 5.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>'
  + '<path d="M11.4 5 16.8 1.4v7.2z" fill="currentColor"/></svg>';
const ICON_JUMP_FORWARD = '<svg class="aradio-jump-ring" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
  + '<path d="M16 5a11 11 0 1 0 9.53 5.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>'
  + '<path d="M20.6 5 15.2 1.4v7.2z" fill="currentColor"/></svg>';
const ICON_TO_LIVE = '<svg class="aradio-relive-icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
  + '<path d="M8 2.5v10M3.8 8.6 8 12.8l4.2-4.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';

/** App names are brand names: the same in every language. */
const FOLLOW_NAMES: Record<AradioFollowApp, string> = {
  apple: 'Apple Podcasts',
  spotify: 'Spotify',
  overcast: 'Overcast',
  pocketcasts: 'Pocket Casts',
};

/**
 * Following the show: a button per podcast app (empty and hidden here;
 * hydrateAradioFollow gives the ones this platform can use their links), then
 * the feed address to copy, and the manual Apple Podcasts route as the
 * fallback when a link cannot open its app.
 */
function renderPodcast(language: UiLanguage): string {
  const t = (key: UiCopyKey) => esc(uiText(language, key));
  const apps = ARADIO_FOLLOW_APPS.map((app) => `<li hidden><a class="aradio-follow-link" data-aradio-follow="${app}"`
    + ` aria-label="${esc(uiText(language, 'aradio.followIn', { app: FOLLOW_NAMES[app] }))}">${esc(FOLLOW_NAMES[app])}</a></li>`).join('');
  return [
    '<div class="aradio-podcast">',
    `<p class="aradio-podcast-title">${t('aradio.podcastTitle')}</p>`,
    `<ul class="aradio-follow" data-aradio-follow-list hidden>${apps}</ul>`,
    '<div class="aradio-podcast-row">',
    `<input class="aradio-feed-input" type="text" readonly spellcheck="false" data-aradio-feed-url aria-label="${t('aradio.feedLabel')}" value="">`,
    `<button type="button" class="aradio-copy" data-aradio-copy-feed>${t('aradio.copy')}</button>`,
    '</div>',
    `<p class="aradio-podcast-hint">${t('aradio.podcastHint')}</p>`,
    '<p class="aradio-sr" aria-live="polite" data-aradio-copy-status></p>',
    '</div>',
  ].join('');
}

function renderRadioHead(copy: AradioRadioCopy, kind: AradioRadioView['kind'], s: { language: UiLanguage; nowMs: number }): string {
  const language = s.language;
  // Station name and on-air sign share a row (the sign wraps below only when
  // it cannot fit); the tagline runs underneath, then how fresh the station
  // is and when to expect more. There is no schedule to promise: a bulletin
  // airs when the material changes the picture.
  const updated = relTime(copy.updatedIso || null, 'aradio.updated', s, 'aradio-updated');
  const liveness = kind === 'ready' || kind === 'text-only'
    ? '<p class="aradio-liveness" data-aradio-liveness>'
      + (copy.updatedShown ? updated : updated.replace('<time ', '<time hidden '))
      + `<span class="aradio-next-airs">${esc(uiText(language, 'aradio.nextAirs'))}</span></p>`
    : '';
  return [
    '<header class="aradio-radio-head">',
    `<h2 class="aradio-station" id="aradioStation">${esc(uiText(language, 'aradio.station'))}</h2>`,
    `<p class="aradio-badge${copy.live ? ' is-live' : ''}${copy.off ? ' is-off' : ''}" data-aradio-badge>`,
    '<span class="aradio-badge-lamp" aria-hidden="true"></span>',
    `<span data-aradio-badge-text>${esc(copy.badge)}</span></p>`,
    `<p class="aradio-tagline">${esc(uiText(language, 'aradio.tagline'))}</p>`,
    liveness,
    '</header>',
  ].join('');
}

/** The masthead's "Checked N ago" line; re-rendered after every poll. */
export function renderAradioChecked(checkedAt: number | null, language: UiLanguage, nowMs: number): string {
  return checkedAt
    ? relTime(new Date(checkedAt).toISOString(), 'aradio.checked', { nowMs, language })
    : esc(uiText(language, 'aradio.checking'));
}

type LinesOptions = {
  language: UiLanguage;
  /** Each line is a button that plays the bulletin from there (it has audio). */
  seekable: boolean;
  /** The line being read (`aradioPlayerLine`): -1 none, the line count once all are heard. */
  live: number;
};

/**
 * A transcript's lines. While its bulletin is in the player, the line being
 * read is `is-live` (and `aria-current`), the ones before it `is-past`; the
 * list says `is-following`. Seekable lines are buttons with one tab stop for
 * the list (the live line, else the first): arrow keys move between them.
 */
function renderLines(bulletin: AradioBulletin, o: LinesOptions, className: string): string {
  const following = o.live >= 0;
  const stop = following ? Math.min(o.live, bulletin.lines.length - 1) : 0;
  const items = bulletin.lines.map((line, i) => {
    const role = aradioSpeakerRole(line.speaker);
    const state = !o.seekable ? ' is-static' : !following ? '' : i < o.live ? ' is-past' : i === o.live ? ' is-live' : '';
    const speaker = `<span class="aradio-speaker">${esc(speakerLabel(line.speaker, o.language))}</span>`;
    const body = o.seekable
      ? `<button type="button" class="aradio-line-seek" data-aradio-seek-line="${i}" tabindex="${i === stop ? '0' : '-1'}"`
        + `${i === o.live ? ' aria-current="true"' : ''}>${speaker}<span class="aradio-line-text">${esc(line.text)}</span></button>`
      : `${speaker}<p class="aradio-line-text">${esc(line.text)}</p>`;
    return `<li class="aradio-line aradio-line--s${role}${state}" data-aradio-line="${i}">${body}</li>`;
  }).join('');
  return `<ol class="aradio-lines ${className}${following ? ' is-following' : ''}" data-aradio-lines="${esc(bulletin.id)}">${items}</ol>`;
}

/**
 * The storylines a bulletin covered, with their status when it aired. One on
 * the board is a button that goes to it there; one that has left the board is
 * plain text.
 */
function renderCoveredList(bulletin: AradioBulletin, language: UiLanguage, boardSlugs: ReadonlySet<string>): string {
  const threads = new Map(bulletin.threads.map((thread) => [thread.slug, thread]));
  const items = bulletin.covers.map((slug) => {
    const thread = threads.get(slug);
    const pill = thread
      ? `<span class="aradio-pill aradio-pill--${thread.status}">${esc(statusLabel(thread.status, language))}</span>`
      : '';
    const name = `<span class="aradio-covered-name">${esc(thread?.title || slug.replace(/-/g, ' '))}</span>`;
    return boardSlugs.has(slug)
      ? `<li><button type="button" class="aradio-covered-item" data-aradio-goto="${esc(slug)}">${pill}${name}</button></li>`
      : `<li><span class="aradio-covered-item is-static">${pill}${name}</span></li>`;
  }).join('');
  return items ? `<ul class="aradio-covered-list">${items}</ul>` : '';
}

export type AradioScriptOptions = {
  language: UiLanguage;
  /** Slugs on the board the page shows: covered storylines link to them. */
  boardSlugs: ReadonlySet<string>;
  radio: AradioRadioInput;
};

/** What the radio card's transcript slot shows; main.ts re-renders the slot when it changes. */
export function aradioScriptKey(script: AradioTranscriptState, language: UiLanguage, boardSlugs: ReadonlySet<string>): string {
  if (script.kind === 'none') return `${language}|none`;
  if (script.kind !== 'ready') return `${language}|${script.kind}|${script.entry.id}`;
  const linked = script.bulletin.covers.filter((slug) => boardSlugs.has(slug)).join(',');
  return `${language}|ready|${script.bulletin.id}|${linked}`;
}

/**
 * The radio card's transcript (the bulletin on now, or up first; the newest
 * when nothing can be heard) and the storylines it covers. The lines sit in a
 * fixed-height window that main.ts scrolls to keep the line being read in
 * view; the page itself never moves.
 */
export function renderAradioScript(script: AradioTranscriptState, o: AradioScriptOptions): string {
  if (script.kind === 'none') return '';
  const t = (key: UiCopyKey) => esc(uiText(o.language, key));
  const bulletin = script.kind === 'ready' ? script.bulletin : null;
  const seekable = Boolean(bulletin?.audio && bulletin.lines.length);
  let body: string;
  if (bulletin) {
    body = bulletin.lines.length
      ? renderLines(bulletin, { language: o.language, seekable, live: seekable ? aradioPlayerLine(o.radio, bulletin) : -1 }, 'aradio-lines--script')
      : `<p class="aradio-script-status">${t('aradio.transcriptError')}</p>`;
  } else {
    body = `<p class="aradio-script-status">${t(script.kind === 'loading' ? 'aradio.transcriptLoading' : 'aradio.transcriptError')}`
      + (script.kind === 'error' ? ` <button type="button" class="aradio-text-button" data-aradio-script-retry>${esc(uiText(o.language, 'action.retry'))}</button>` : '')
      + '</p>';
  }
  // Without buttons inside, the window itself takes focus so it can be scrolled from the keyboard.
  const windowAttrs = seekable
    ? ''
    : ' tabindex="0" role="region" aria-labelledby="aradioScriptTitle"';
  const covered = bulletin ? renderCoveredList(bulletin, o.language, o.boardSlugs) : '';
  return [
    `<section class="aradio-script" aria-labelledby="aradioScriptTitle"${script.kind === 'loading' ? ' aria-busy="true"' : ''}>`,
    '<div class="aradio-script-head">',
    `<h3 class="aradio-script-title" id="aradioScriptTitle">${t('aradio.transcript')}</h3>`,
    seekable ? `<p class="aradio-script-note">${t('aradio.scriptNote')}</p>` : '',
    '</div>',
    seekable ? `<p class="aradio-sr">${t('aradio.lineHint')}</p>` : '',
    '<div class="aradio-script-frame">',
    `<div class="aradio-script-window" data-aradio-script-window${windowAttrs}>${body}</div>`,
    seekable
      ? `<button type="button" class="aradio-relive" data-aradio-relive hidden>${ICON_TO_LIVE}<span>${t('aradio.backToLive')}</span></button>`
      : '',
    '</div>',
    '</section>',
    covered
      ? `<section class="aradio-covered" aria-labelledby="aradioCoveredTitle"><h3 class="aradio-covered-title" id="aradioCoveredTitle">${t('aradio.inThisBulletin')}</h3>${covered}</section>`
      : '',
  ].join('');
}

/** The transcript slot of the radio card, keyed so main.ts can tell when to swap it. */
function scriptSlot(s: AradioViewState, view: AradioRadioView): string {
  const script: AradioTranscriptState = s.script
    ?? (view.scriptEntry ? { kind: 'loading', entry: view.scriptEntry } : { kind: 'none' });
  const boardSlugs = new Set((s.board?.threads ?? []).map((thread) => thread.slug));
  return `<div class="aradio-script-slot" data-aradio-script-slot data-aradio-script-key="${esc(aradioScriptKey(script, s.language, boardSlugs))}">`
    + renderAradioScript(script, { language: s.language, boardSlugs, radio: s.radio })
    + '</div>';
}

/**
 * The radio card. `data-aradio-radio` names the card's shape (ready / none /
 * text-only / error); main.ts re-renders the card only when that changes and
 * otherwise patches its text and controls in place, so focus and layout never
 * jump while bulletins change. The transcript slot is swapped as a unit when
 * its bulletin changes (`aradioScriptKey`).
 */
export function renderAradioRadio(s: AradioViewState): string {
  const language = s.language;
  const view = aradioRadioView(s.radio, s.nowMs);
  const copy = aradioRadioCopy(view, s.nowMs, language);
  const t = (key: UiCopyKey) => esc(uiText(language, key));
  const live = '<p class="aradio-sr" aria-live="polite" data-aradio-live></p>';
  const open = `<section class="content-card aradio-radio aradio-radio--${view.kind}" aria-labelledby="aradioStation" data-aradio-radio="${view.kind}">`;

  if (view.kind !== 'ready') {
    const [titleKey, bodyKey]: [UiCopyKey, UiCopyKey] = view.kind === 'error'
      ? ['aradio.errorTitle', 'aradio.errorBody']
      : view.kind === 'text-only' ? ['aradio.textOnlyTitle', 'aradio.textOnlyBody'] : ['aradio.emptyTitle', 'aradio.emptyBody'];
    return [
      open,
      renderRadioHead(copy, view.kind, s),
      '<div class="aradio-radio-empty">',
      `<h3 class="aradio-empty-title">${t(titleKey)}</h3>`,
      `<p class="aradio-empty-copy">${t(bodyKey)}</p>`,
      view.kind === 'error'
        ? `<button type="button" class="aradio-empty-action" data-retry>${esc(uiText(language, 'action.retry'))}</button>`
        : '',
      // Before the first run there is no "Behind the broadcast" header to
      // carry the poll line, so the empty card says when it last looked.
      view.kind === 'none'
        ? `<p class="aradio-checked" data-aradio-checked>${renderAradioChecked(s.checkedAt, language, s.nowMs)}</p>`
        : '',
      '</div>',
      // Nothing to hear yet, but the newest bulletin is there to read.
      view.kind === 'text-only' ? scriptSlot(s, view) : '',
      renderPodcast(language),
      live,
      '</section>',
    ].join('');
  }

  const jumpDisabled = view.seekable ? 'false' : 'true';
  const rate = aradioRateLabel(s.rate ?? 1);
  // One DOM order for every layout: the controls (the big button among them),
  // what is on, the seek bar, speed and "stop after", then the transcript and
  // up next. Focus order follows it everywhere. Phones show it as is; wide
  // screens lift the (unfocusable) headline above the controls and put the
  // transcript in a column of its own.
  return [
    open,
    renderRadioHead(copy, view.kind, s),
    `<div class="aradio-deck aradio-mode--${view.mode}" data-aradio-deck>`,
    '<div class="aradio-transport">',
    `<button type="button" class="aradio-skip" data-aradio-prev aria-label="${t('aradio.previous')}" aria-disabled="${view.canPrevious ? 'false' : 'true'}">${ICON_PREVIOUS}</button>`,
    `<button type="button" class="aradio-jump" data-aradio-back aria-label="${esc(uiText(language, 'aradio.jumpBack', { seconds: ARADIO_JUMP_S }))}" aria-disabled="${jumpDisabled}">`,
    `${ICON_JUMP_BACK}<span class="aradio-jump-num" aria-hidden="true">${ARADIO_JUMP_S}</span></button>`,
    `<button type="button" class="aradio-toggle${copy.toggleIcon === 'pause' ? ' is-playing' : ''}${view.buffering ? ' is-buffering' : ''}" data-aradio-toggle`,
    ` aria-label="${esc(copy.toggleLabel)}" aria-describedby="aradioNowHeadline">${ICON_PLAY_PAUSE}</button>`,
    `<button type="button" class="aradio-jump" data-aradio-forward aria-label="${esc(uiText(language, 'aradio.jumpForward', { seconds: ARADIO_JUMP_S }))}" aria-disabled="${jumpDisabled}">`,
    `${ICON_JUMP_FORWARD}<span class="aradio-jump-num" aria-hidden="true">${ARADIO_JUMP_S}</span></button>`,
    `<button type="button" class="aradio-skip" data-aradio-next aria-label="${t('aradio.next')}" aria-disabled="${view.canNext ? 'false' : 'true'}">${ICON_NEXT}</button>`,
    '</div>',
    '<div class="aradio-now">',
    `<img class="aradio-art" src="${esc(ARADIO_COVER_PATH)}" alt="" width="64" height="64" decoding="async">`,
    '<div class="aradio-now-id">',
    `<p class="aradio-now-label" data-aradio-now-label>${esc(copy.label)}</p>`,
    '<p class="aradio-now-meta">',
    `<time data-aradio-now-time datetime="${esc(copy.datetime)}">${esc(copy.time)}</time>`,
    `<span class="aradio-now-day" data-aradio-now-day>${esc(copy.day)}</span>`,
    '</p>',
    '</div>',
    `<p class="aradio-now-headline" id="aradioNowHeadline" data-aradio-now-headline>${esc(copy.headline)}</p>`,
    '</div>',
    '<div class="aradio-progress">',
    `<span class="aradio-elapsed" data-aradio-elapsed aria-hidden="true">${esc(copy.elapsed)}</span>`,
    `<input class="aradio-seek" type="range" min="0" max="${copy.seekMax}" step="1" value="${copy.seekValue}" data-aradio-seek`,
    ` aria-label="${t('aradio.seek')}" aria-valuetext="${esc(copy.seekText)}"${view.seekable ? '' : ' disabled'}`,
    ` style="--aradio-progress:${esc(copy.progressPct)}">`,
    `<span class="aradio-remaining" data-aradio-remaining aria-hidden="true">${esc(copy.remaining)}</span>`,
    '</div>',
    '<div class="aradio-options">',
    `<button type="button" class="aradio-rate" data-aradio-rate aria-label="${esc(uiText(language, 'aradio.speed', { rate }))}">${esc(rate)}</button>`,
    `<button type="button" class="aradio-stop-after" data-aradio-stop-after aria-pressed="${view.stopAfter ? 'true' : 'false'}">`,
    `<span class="aradio-check" aria-hidden="true"></span><span>${t('aradio.stopAfter')}</span></button>`,
    '</div>',
    `<p class="aradio-note" data-aradio-note>${esc(copy.note)}</p>`,
    scriptSlot(s, view),
    '<div class="aradio-upnext">',
    `<h3 class="aradio-upnext-title">${t('aradio.upNext')}</h3>`,
    `<ol class="aradio-upnext-list" data-aradio-upnext>${renderAradioUpNext(view, copy)}</ol>`,
    '</div>',
    '</div>',
    renderPodcast(language),
    live,
    '</section>',
  ].join('');
}

// ── Rendering: behind the broadcast ──────────────────────────────────────

/** What a log row's play pill says: its length, the time left, or that it was heard. */
export type AradioPillCopy = { state: AradioListenState['state']; text: string; label: string; heard: string };

export function aradioPillCopy(
  entry: { airedAt: string; headline: string; audio: AradioAudio | null },
  listen: AradioListenState,
  language: UiLanguage,
  playing: boolean,
): AradioPillCopy {
  const text = listen.state === 'done'
    ? uiText(language, 'aradio.played')
    : listen.state === 'partial'
      ? uiText(language, 'aradio.timeLeft', { time: aradioClock(Math.ceil(listen.remaining)) })
      : aradioDuration(entry.audio?.durationS ?? null);
  const action = aradioPlayAria(entry, language, playing);
  return {
    state: listen.state,
    text,
    // The name carries the visible text, so voice control can say it too.
    label: text ? `${action} (${text})` : action,
    heard: `${(listen.fraction * 100).toFixed(1)}%`,
  };
}

/**
 * A log row's play pill: play/pause, and how much of the bulletin this viewer
 * has heard, as a fill behind its length ("2:52", "1:20 left", "Played").
 */
function playPill(entry: AradioBulletinEntry, s: AradioViewState): string {
  const listen = aradioListenState(aradioListenOf(s.listened, entry.id), entry.audio?.durationS ?? null);
  const pill = aradioPillCopy(entry, listen, s.language, false);
  return `<button type="button" class="aradio-log-play is-${pill.state}" data-aradio-play="${esc(entry.id)}"`
    + ` aria-label="${esc(pill.label)}" style="--aradio-heard:${esc(pill.heard)}">`
    + '<span class="aradio-mini-icon" aria-hidden="true"></span>'
    + `<span class="aradio-log-pill-text" data-aradio-pill-text>${esc(pill.text)}</span></button>`;
}

/** An empty slot for an evidence link; hydrateAradioLinks() fills it. */
function evidenceSlot(evidence: AradioEvidence, language: UiLanguage, links: AradioLinkSpec[]): string {
  links.push({ url: evidence.url, kind: evidence.kind, kindLabel: kindLabel(evidence.kind, language), label: evidence.label });
  return `<span class="aradio-link-slot" data-aradio-link="${links.length - 1}"></span>`;
}

function renderQuotes(evidence: readonly AradioEvidence[]): string {
  const quoted = evidence.filter((item) => item.quote);
  if (!quoted.length) return '';
  return '<div class="aradio-quotes">' + quoted.map((item) => {
    const who = [item.speaker, item.label].filter(Boolean).join(', ');
    return `<blockquote class="aradio-quote"><p>${esc(item.quote)}</p>`
      + (who ? `<footer>${esc(who)}</footer>` : '')
      + '</blockquote>';
  }).join('') + '</div>';
}

function renderSignal(importance: number, language: UiLanguage): string {
  const bars = [1, 2, 3, 4, 5].map((n) => `<i${n <= importance ? ' class="on"' : ''}></i>`).join('');
  return `<span class="aradio-signal" role="img" aria-label="${esc(uiText(language, 'aradio.importance', { value: importance }))}">${bars}</span>`;
}

function renderThread(thread: AradioThread, s: AradioViewState, links: AradioLinkSpec[]): string {
  const language = s.language;
  const facts = [
    thread.changed ? `<div><dt>${esc(uiText(language, 'aradio.changed'))}</dt><dd>${esc(thread.changed)}</dd></div>` : '',
    thread.watch ? `<div><dt>${esc(uiText(language, 'aradio.watch'))}</dt><dd>${esc(thread.watch)}</dd></div>` : '',
  ].join('');
  const evidence = thread.evidence.length
    ? `<ul class="aradio-evidence-list" aria-label="${esc(uiText(language, 'aradio.evidence'))}">`
      + thread.evidence.map((item) => `<li>${evidenceSlot(item, language, links)}</li>`).join('')
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
    `<h4 class="aradio-thread-title">${esc(thread.title)}</h4>`,
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
    `<h4>${esc(thread.title)}</h4>`,
    thread.changed ? `<p>${esc(thread.changed)}</p>` : '',
    relTime(thread.updatedAt, 'aradio.resolvedAgo', s, 'aradio-resolved-age'),
    '</li>',
  ].join('')).join('');
  return `<details class="aradio-resolved"><summary>${esc(uiText(s.language, 'aradio.resolvedSection', { count: threads.length }))}</summary>`
    + `<ul class="aradio-resolved-list">${items}</ul></details>`;
}

function renderBoard(s: AradioViewState, links: AradioLinkSpec[]): string {
  const language = s.language;
  const { open, resolved } = sortAradioThreads(s.board?.threads ?? []);
  let body: string;
  if (s.boardStatus === 'error' && !s.board) {
    body = `<p class="aradio-muted">${esc(uiText(language, 'aradio.boardError'))} `
      + `<button type="button" class="aradio-text-button" data-retry>${esc(uiText(language, 'action.retry'))}</button></p>`;
  } else if (!s.board) {
    body = `<p class="aradio-muted">${esc(uiText(language, 'aradio.boardMissing'))}</p>`;
  } else if (!open.length) {
    body = `<p class="aradio-muted">${esc(uiText(language, 'aradio.boardEmpty'))}</p>`;
  } else {
    body = `<div class="aradio-thread-grid">${open.map((thread) => renderThread(thread, s, links)).join('')}</div>`;
  }
  const count = open.length === 1
    ? uiText(language, 'aradio.boardCountOne')
    : uiText(language, 'aradio.boardCount', { count: open.length });
  return [
    '<section class="content-card aradio-board" aria-labelledby="aradioBoardTitle">',
    '<header class="aradio-section-head">',
    `<h3 class="aradio-section-title" id="aradioBoardTitle">${esc(uiText(language, 'aradio.board'))}</h3>`,
    s.board
      ? `<p class="aradio-section-meta"><span>${esc(count)}</span>${relTime(s.board.updatedAt, 'aradio.updatedAgo', s)}</p>`
      : '',
    '</header>',
    body,
    renderResolved(resolved, s),
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
    `<h4 class="aradio-log-date">${esc(group.label)}</h4>`,
    '<ol class="aradio-log-list">',
    group.rows.map((entry) => {
      const selected = entry.id === s.selectedId;
      // Audio rows lead with a play pill; text-only ones say so in its place.
      return [
        `<li class="aradio-log-row${selected ? ' is-selected' : ''}${entry.audio ? '' : ' is-text-only'}" data-aradio-row="${esc(entry.id)}">`,
        entry.audio
          ? playPill(entry, s)
          : `<span class="aradio-log-noaudio">${esc(uiText(language, 'aradio.textOnly'))}</span>`,
        `<button type="button" class="aradio-log-select" data-aradio-select="${esc(entry.id)}" aria-controls="aradio-transcript"${selected ? ' aria-current="true"' : ''}>`,
        `<time class="aradio-log-time" datetime="${esc(entry.airedAt)}">${esc(aradioUtcTime(entry.airedAt))}</time>`,
        `<span class="aradio-log-headline">${esc(headlineOf(entry))}</span>`,
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

type TranscriptOptions = {
  language: UiLanguage;
  boardSlugs: ReadonlySet<string>;
  open?: boolean;
  /** The shared player, so the transcript of the bulletin in it follows along. */
  radio?: AradioRadioInput;
};

/**
 * The transcript panel for the selected bulletin: a disclosure, collapsed
 * until the listener opens it (or picks a bulletin in the log).
 */
export function renderAradioTranscript(transcript: AradioTranscriptState, s: TranscriptOptions): AradioRender {
  const links: AradioLinkSpec[] = [];
  return { html: transcriptHtml(transcript, s, links), links };
}

function transcriptHtml(transcript: AradioTranscriptState, s: TranscriptOptions, links: AradioLinkSpec[]): string {
  if (transcript.kind === 'none') return '';
  const language = s.language;
  const entry = transcript.kind === 'ready' ? transcript.bulletin : transcript.entry;
  const summary = [
    `<details class="aradio-transcript-details" data-aradio-transcript-details${s.open ? ' open' : ''}>`,
    '<summary class="aradio-transcript-summary">',
    `<span class="aradio-transcript-summary-label">${esc(uiText(language, 'aradio.transcript'))}</span>`,
    `<time datetime="${esc(entry.airedAt)}">${esc(aradioUtcTime(entry.airedAt))} UTC</time>`,
    `<span class="aradio-transcript-summary-day">${esc(aradioUtcDay(entry.airedAt, language, true))}</span>`,
    '</summary>',
  ].join('');
  if (transcript.kind === 'loading' || transcript.kind === 'error') {
    const loading = transcript.kind === 'loading';
    return [
      summary,
      `<article class="aradio-transcript" aria-busy="${loading ? 'true' : 'false'}">`,
      transcript.entry.headline ? `<p class="aradio-transcript-headline">${esc(transcript.entry.headline)}</p>` : '',
      `<p class="aradio-muted">${esc(uiText(language, loading ? 'aradio.transcriptLoading' : 'aradio.transcriptError'))}`,
      loading ? '' : ` <button type="button" class="aradio-text-button" data-aradio-select="${esc(transcript.entry.id)}">${esc(uiText(language, 'action.retry'))}</button>`,
      '</p>',
      '</article>',
      '</details>',
    ].join('');
  }
  const bulletin = transcript.bulletin;
  // A bulletin with audio can be played from any line; the one in the player follows along.
  const seekable = Boolean(bulletin.audio);
  const live = seekable && s.radio ? aradioPlayerLine(s.radio, bulletin) : -1;
  const lines = bulletin.lines.length ? renderLines(bulletin, { language, seekable, live }, 'aradio-lines--archive') : '';
  const covers = renderCoveredList(bulletin, language, s.boardSlugs);
  const sources = bulletin.sources.map((item) => `<li>${evidenceSlot(item, language, links)}</li>`).join('');
  return [
    summary,
    `<article class="aradio-transcript" data-aradio-transcript="${esc(bulletin.id)}">`,
    bulletin.headline ? `<p class="aradio-transcript-headline">${esc(bulletin.headline)}</p>` : '',
    bulletin.audio
      ? `<button type="button" class="aradio-transcript-play" data-aradio-play="${esc(bulletin.id)}" aria-label="${esc(aradioPlayAria(bulletin, language, false))}">`
        + `<span class="aradio-mini-icon" aria-hidden="true"></span><span data-aradio-play-label>${esc(uiText(language, 'aradio.play'))}</span></button>`
      : `<p class="aradio-muted">${esc(uiText(language, 'aradio.noAudioHint'))}</p>`,
    lines || `<p class="aradio-muted">${esc(uiText(language, 'aradio.transcriptError'))}</p>`,
    covers
      ? `<div class="aradio-transcript-foot"><h5>${esc(uiText(language, 'aradio.storylines'))}</h5>${covers}</div>`
      : '',
    sources
      ? `<div class="aradio-transcript-foot"><h5>${esc(uiText(language, 'aradio.sources'))}</h5><ul class="aradio-evidence-list">${sources}</ul></div>`
      : '',
    `<p class="aradio-credit">${esc(bulletin.editorModel
      ? uiText(language, 'aradio.credit', { model: bulletin.editorModel })
      : uiText(language, 'aradio.creditNoModel'))}</p>`,
    '</article>',
    '</details>',
  ].join('');
}

function renderBulletins(s: AradioViewState, links: AradioLinkSpec[]): string {
  const bulletins = s.index?.bulletins ?? [];
  if (!bulletins.length) return '';
  const boardSlugs = new Set((s.board?.threads ?? []).map((thread) => thread.slug));
  return [
    '<section class="content-card aradio-bulletins" aria-labelledby="aradioBulletinsTitle">',
    '<div class="aradio-bulletins-grid">',
    '<div class="aradio-log">',
    '<header class="aradio-section-head">',
    `<h3 class="aradio-section-title" id="aradioBulletinsTitle">${esc(uiText(s.language, 'aradio.bulletins'))}</h3>`,
    `<p class="aradio-section-meta">${esc(uiText(s.language, 'aradio.bulletinsCount', { count: bulletins.length }))}</p>`,
    '</header>',
    `<div data-aradio-log>${renderAradioLog(s)}</div>`,
    '</div>',
    `<div class="aradio-transcript-slot" id="aradio-transcript" data-aradio-transcript-slot>${transcriptHtml(s.transcript, { language: s.language, boardSlugs, open: s.transcriptOpen, radio: s.radio }, links)}</div>`,
    '</div>',
    '</section>',
  ].join('');
}

/**
 * "Behind the broadcast": the board, the bulletin log and the transcript,
 * below the radio and visually secondary. New data reaches it through the
 * update chip, never by re-rendering under someone reading it. Empty before
 * the first run: the radio card alone carries that state.
 */
export function renderAradioBehind(s: AradioViewState): AradioRender {
  const links: AradioLinkSpec[] = [];
  const hasBulletins = Boolean(s.index?.bulletins.length);
  const hasBoard = Boolean(s.board?.threads.length);
  if (!hasBulletins && !hasBoard && s.boardStatus !== 'error') return { html: '', links };
  const language = s.language;
  const html = [
    '<section class="aradio-behind" aria-labelledby="aradioBehindTitle">',
    '<header class="aradio-behind-head">',
    '<div class="aradio-behind-copy">',
    `<h2 class="aradio-behind-title" id="aradioBehindTitle">${esc(uiText(language, 'aradio.behind'))}</h2>`,
    `<p class="aradio-behind-hint">${esc(uiText(language, 'aradio.behindHint'))}</p>`,
    '</div>',
    '<div class="aradio-behind-meta">',
    `<p class="aradio-checked" data-aradio-checked>${renderAradioChecked(s.checkedAt, language, s.nowMs)}</p>`,
    '<button type="button" class="aradio-update" data-aradio-apply hidden>'
      + '<span class="aradio-update-dot" aria-hidden="true"></span><span data-aradio-update-text></span>'
      + '<span class="aradio-update-time" data-aradio-update-time></span></button>',
    '</div>',
    '</header>',
    renderBoard(s, links),
    renderBulletins(s, links),
    '</section>',
  ].join('');
  return { html, links };
}

/**
 * The whole /aradio view: the radio, then what is behind the broadcast.
 * Missing files render empty states, never throw. Insert `html`, then call
 * hydrateAradioLinks(root, links) and hydrateAradioFeed(root, feedUrl).
 */
export function renderAradioView(s: AradioViewState): AradioRender {
  const behind = renderAradioBehind(s);
  const html = [
    '<div class="aradio-view">',
    `<div class="aradio-radio-slot" data-aradio-radio-slot>${renderAradioRadio(s)}</div>`,
    `<div class="aradio-behind-slot" data-aradio-behind-slot>${behind.html}</div>`,
    '</div>',
  ].join('');
  return { html, links: behind.links };
}
