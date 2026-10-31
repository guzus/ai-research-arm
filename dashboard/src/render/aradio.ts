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
    elapsed,
    duration,
    seekable: active && input.duration > 0,
    buffering: mode === 'playing' && input.buffering,
    stopAfter: input.stopAfter,
  };
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

/** m:ss for the seek bar; whole seconds, never negative. */
export function aradioClock(seconds: number): string {
  const whole = Number.isFinite(seconds) && seconds > 0 ? Math.floor(seconds) : 0;
  return `${Math.floor(whole / 60)}:${pad2(whole % 60)}`;
}

/** The i18n keys a `data-aradio-rel-key` attribute may name (ticker refresh). */
export const ARADIO_REL_KEYS: readonly UiCopyKey[] = [
  'aradio.updatedAgo', 'aradio.resolvedAgo', 'aradio.checked',
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

function renderPodcast(language: UiLanguage): string {
  const t = (key: UiCopyKey) => esc(uiText(language, key));
  return [
    '<div class="aradio-podcast">',
    `<p class="aradio-podcast-title">${t('aradio.podcastTitle')}</p>`,
    '<div class="aradio-podcast-row">',
    `<input class="aradio-feed-input" type="text" readonly spellcheck="false" data-aradio-feed-url aria-label="${t('aradio.feedLabel')}" value="">`,
    `<button type="button" class="aradio-copy" data-aradio-copy-feed>${t('aradio.copy')}</button>`,
    '</div>',
    `<p class="aradio-podcast-hint">${t('aradio.podcastHint')}</p>`,
    '<p class="aradio-sr" aria-live="polite" data-aradio-copy-status></p>',
    '</div>',
  ].join('');
}

function renderRadioHead(copy: AradioRadioCopy, language: UiLanguage): string {
  // Station name and on-air sign share a row (the sign wraps below only when
  // it cannot fit); the tagline runs underneath.
  return [
    '<header class="aradio-radio-head">',
    `<h2 class="aradio-station" id="aradioStation">${esc(uiText(language, 'aradio.station'))}</h2>`,
    `<p class="aradio-badge${copy.live ? ' is-live' : ''}${copy.off ? ' is-off' : ''}" data-aradio-badge>`,
    '<span class="aradio-badge-lamp" aria-hidden="true"></span>',
    `<span data-aradio-badge-text>${esc(copy.badge)}</span></p>`,
    `<p class="aradio-tagline">${esc(uiText(language, 'aradio.tagline'))}</p>`,
    '</header>',
  ].join('');
}

/** The masthead's "Checked N ago" line; re-rendered after every poll. */
export function renderAradioChecked(checkedAt: number | null, language: UiLanguage, nowMs: number): string {
  return checkedAt
    ? relTime(new Date(checkedAt).toISOString(), 'aradio.checked', { nowMs, language })
    : esc(uiText(language, 'aradio.checking'));
}

/**
 * The radio card. `data-aradio-radio` names the card's shape (ready / none /
 * text-only / error); main.ts re-renders the card only when that changes and
 * otherwise patches its text and controls in place, so focus and layout never
 * jump while bulletins change.
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
      renderRadioHead(copy, language),
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
      renderPodcast(language),
      live,
      '</section>',
    ].join('');
  }

  const now = view.now;
  // One DOM order for every layout (button, what is on, seek, transport, up
  // next), so keyboard and screen-reader order match what is seen: the CSS
  // grid puts the button left of the headline on wide screens and centred
  // above it on phones.
  return [
    open,
    renderRadioHead(copy, language),
    `<div class="aradio-deck aradio-mode--${view.mode}" data-aradio-deck>`,
    `<button type="button" class="aradio-toggle${copy.toggleIcon === 'pause' ? ' is-playing' : ''}${view.buffering ? ' is-buffering' : ''}" data-aradio-toggle`,
    ` aria-label="${esc(copy.toggleLabel)}" aria-describedby="aradioNowHeadline">${ICON_PLAY_PAUSE}</button>`,
    '<div class="aradio-now">',
    `<p class="aradio-now-label" data-aradio-now-label>${esc(copy.label)}</p>`,
    `<p class="aradio-now-headline" id="aradioNowHeadline" data-aradio-now-headline>${esc(copy.headline)}</p>`,
    '<p class="aradio-now-meta">',
    `<time data-aradio-now-time datetime="${esc(copy.datetime)}">${esc(copy.time)}</time>`,
    `<span class="aradio-now-day" data-aradio-now-day>${esc(copy.day)}</span>`,
    `<button type="button" class="aradio-text-button" data-aradio-read="${esc(now?.id ?? '')}">${t('aradio.readTranscript')}</button>`,
    '</p>',
    '</div>',
    '<div class="aradio-progress">',
    `<span class="aradio-elapsed" data-aradio-elapsed aria-hidden="true">${esc(copy.elapsed)}</span>`,
    `<input class="aradio-seek" type="range" min="0" max="${copy.seekMax}" step="1" value="${copy.seekValue}" data-aradio-seek`,
    ` aria-label="${t('aradio.seek')}" aria-valuetext="${esc(copy.seekText)}"${view.seekable ? '' : ' disabled'}`,
    ` style="--aradio-progress:${esc(copy.progressPct)}">`,
    `<span class="aradio-remaining" data-aradio-remaining aria-hidden="true">${esc(copy.remaining)}</span>`,
    '</div>',
    '<div class="aradio-transport">',
    `<button type="button" class="aradio-skip" data-aradio-prev aria-label="${t('aradio.previous')}" aria-disabled="${view.canPrevious ? 'false' : 'true'}">${ICON_PREVIOUS}</button>`,
    `<button type="button" class="aradio-skip" data-aradio-next aria-label="${t('aradio.next')}" aria-disabled="${view.canNext ? 'false' : 'true'}">${ICON_NEXT}</button>`,
    `<button type="button" class="aradio-stop-after" data-aradio-stop-after aria-pressed="${view.stopAfter ? 'true' : 'false'}">`,
    `<span class="aradio-check" aria-hidden="true"></span><span>${t('aradio.stopAfter')}</span></button>`,
    '</div>',
    `<p class="aradio-note" data-aradio-note>${esc(copy.note)}</p>`,
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

function playIconButton(entry: AradioBulletinEntry, language: UiLanguage, className: string): string {
  return `<button type="button" class="${esc(className)}" data-aradio-play="${esc(entry.id)}"`
    + ` aria-label="${esc(aradioPlayAria(entry, language, false))}"><span class="aradio-mini-icon" aria-hidden="true"></span></button>`;
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
      const duration = entry.audio ? aradioDuration(entry.audio.durationS) : uiText(language, 'aradio.textOnly');
      return [
        `<li class="aradio-log-row${selected ? ' is-selected' : ''}${entry.audio ? '' : ' is-text-only'}" data-aradio-row="${esc(entry.id)}">`,
        entry.audio
          ? playIconButton(entry, language, 'aradio-log-play')
          : `<span class="aradio-log-noaudio" aria-hidden="true"></span>`,
        `<button type="button" class="aradio-log-select" data-aradio-select="${esc(entry.id)}" aria-controls="aradio-transcript"${selected ? ' aria-current="true"' : ''}>`,
        `<time class="aradio-log-time" datetime="${esc(entry.airedAt)}">${esc(aradioUtcTime(entry.airedAt))}</time>`,
        `<span class="aradio-log-headline">${esc(headlineOf(entry))}</span>`,
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

type TranscriptOptions = { language: UiLanguage; boardSlugs: ReadonlySet<string>; open?: boolean };

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
  const sources = bulletin.sources.map((item) => `<li>${evidenceSlot(item, language, links)}</li>`).join('');
  return [
    summary,
    `<article class="aradio-transcript" data-aradio-transcript="${esc(bulletin.id)}">`,
    bulletin.headline ? `<p class="aradio-transcript-headline">${esc(bulletin.headline)}</p>` : '',
    bulletin.audio
      ? `<button type="button" class="aradio-transcript-play" data-aradio-play="${esc(bulletin.id)}" aria-label="${esc(aradioPlayAria(bulletin, language, false))}">`
        + `<span class="aradio-mini-icon" aria-hidden="true"></span><span data-aradio-play-label>${esc(uiText(language, 'aradio.play'))}</span></button>`
      : `<p class="aradio-muted">${esc(uiText(language, 'aradio.noAudioHint'))}</p>`,
    lines ? `<ol class="aradio-lines">${lines}</ol>` : `<p class="aradio-muted">${esc(uiText(language, 'aradio.transcriptError'))}</p>`,
    covers
      ? `<div class="aradio-transcript-foot"><h5>${esc(uiText(language, 'aradio.storylines'))}</h5><ul class="aradio-covers">${covers}</ul></div>`
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
    `<div class="aradio-transcript-slot" id="aradio-transcript" data-aradio-transcript-slot>${transcriptHtml(s.transcript, { language: s.language, boardSlugs, open: s.transcriptOpen }, links)}</div>`,
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
