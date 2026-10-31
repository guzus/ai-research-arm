// Aradio podcast feed: research/aradio/ → RSS 2.0 + iTunes tags, written by
// postbuild-seo.mjs to dist/aradio/feed.xml and served at /aradio/feed.xml.
//
// Contract: docs/aradio.md ("Published files", "Audio"). Postbuild reads the
// station data from dist/research/aradio/ (the copy the page itself fetches),
// so one deploy's feed and page always describe the same bulletins.
//
// WHY THE PAGE'S RULES ARE RESTATED HERE INSTEAD OF IMPORTED
//   The Docker image runs postbuild with alpine's `nodejs`, which cannot load
//   src/render/aradio.ts, so this stays plain .mjs. Every rule that decides
//   what reaches a listener mirrors that module, and aradio-feed.test.mjs pins
//   each copy to its original: the S3 key policy (ARADIO_AUDIO_KEY_RE, by
//   source), the enclosure URL (aradioAudioSrc), the bulletin file path
//   (aradioBulletinPath) and the default audio base (main.ts AUDIO_BASE).
//
// WHAT AN ATTACKER CONTROLS
//   index.json and every bulletin are model-authored and relay third-party
//   speech. So an enclosure exists only for a key that passes the page's key
//   policy; a bulletin file is read only at a path rebuilt from a validated
//   shape, and only if it resolves inside the station directory (neither a
//   hostile `path` nor a committed symlink can pull another file into a public
//   feed); and every text node and attribute goes through xmlEscape, which
//   also drops the characters XML 1.0 forbids outright, because escaping
//   cannot make a NUL or a form feed well-formed. There is no CDATA.
//   Podcast apps render a <description> as HTML once the XML is parsed, so
//   description text is HTML-escaped first (htmlEscapeText), then XML-escaped:
//   a "<script>" in a transcript reaches them as text, never as markup.
//   Titles stay plain (see itemLines).
//
// DETERMINISM
//   Nothing reads the clock, and a date is taken only from a string that
//   carries its own zone: Date.parse reads a zone-less date-time in the build
//   host's zone (KST on the runner, UTC in Docker). The same data therefore
//   produces the same bytes in any input order, on any host.

import { readFileSync, realpathSync, statSync } from 'node:fs';
import { join, sep } from 'node:path';

/** Same cap as the page's history (render/aradio.ts ARADIO_MAX_BULLETINS). */
export const ARADIO_FEED_MAX_ITEMS = 72;
/** Per-episode <description> cap in characters, footer included. */
export const ARADIO_FEED_DESCRIPTION_MAX = 4000;
/** main.ts AUDIO_BASE's default; postbuild uses it when VITE_AUDIO_BASE_URL is unset. */
export const ARADIO_DEFAULT_AUDIO_BASE = 'https://s3.guzus.xyz/obj-ai-research-arm';
/** Mirror of render/aradio.ts ARADIO_AUDIO_KEY_RE: a flat audio/aradio/<name>.mp3. */
export const ARADIO_AUDIO_KEY_RE = /^audio\/aradio\/[A-Za-z0-9._-]+\.mp3$/;
/**
 * The show art in public/brand/: a 3000x3000 RGB PNG without alpha (Apple
 * takes a 1400-3000 px square JPEG or PNG; Spotify a 1:1 image, PNG before
 * JPEG). Both fetch art once per URL, so a new design needs a new file name.
 */
export const ARADIO_FEED_ARTWORK_PATH = '/brand/aradio-cover.png';

const DEFAULT_SITE_ORIGIN = 'https://ara.guzus.xyz';
const CHANNEL_TITLE = 'ARA Radio';
const CHANNEL_AUTHOR = 'ARA';
const CHANNEL_DESCRIPTION =
  "A short two-host bulletin on what changed in AI since the last one, voiced from ara's live " +
  'situation board. New episodes air when earnings calls, podcasts, launches or filings change the picture.';
const ITUNES_NS = 'http://www.itunes.com/dtds/podcast-1.0.dtd';
const ATOM_NS = 'http://www.w3.org/2005/Atom';

// Mirrors of render/aradio.ts.
const SAFE_ID_RE = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$/;
const BULLETIN_ID_RE = /^(\d{4}-\d{2}-\d{2})-(\d{2})(\d{2})$/;
const BULLETIN_PATH_RE = /^bulletins\/\d{4}-\d{2}-\d{2}\/\d{4}\.json$/;
const AUDIO_TAG_RE = /\[\/?[a-z_]+\]/gi;
const SCRIPT_LINE_RE = /^(Speaker [12]):\s*(.+)$/;
const SPEAKER_ROLE_RE = /^(?:speaker\s*)?([12])$/i;

// An ISO-8601 date, or date-time with an explicit zone (a bare date is UTC by
// the ECMAScript spec). Zone-less date-times fall back to the id's UTC stamp.
const ZONED_INSTANT_RE = /^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2}))?$/;
// The XML 1.0 Char production, inverted: C0 controls other than tab/LF/CR,
// lone surrogates (the u flag reads a valid pair as one code point), U+FFFE
// and U+FFFF.
const XML_INVALID_RE = /[^\t\n\r\u0020-\uD7FF\uE000-\uFFFD\u{10000}-\u{10FFFF}]/gu;
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const CUT_MARK = '\n\n…';

function isRecord(value) {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

/** Escape for text and attribute contexts, dropping characters XML 1.0 forbids. */
export function xmlEscape(value) {
  return String(value ?? '')
    .replace(XML_INVALID_RE, '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

/**
 * Escape text for an HTML text node: `&`, `<` and `>` only. Quotes need no
 * escaping outside attributes, and leaving them (and every apostrophe in
 * speech) alone keeps a description readable in the few apps that show it raw.
 */
export function htmlEscapeText(value) {
  return String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/**
 * Cut to `max` characters with "…", never inside a surrogate pair — nor, for
 * HTML-escaped text (`escaped`), inside an entity such as `&amp;`.
 */
function clip(value, max, escaped = false) {
  if (value.length <= max) return value;
  let cut = Math.max(0, max - 1);
  if (escaped) {
    // Every `&` in escaped text opens an entity; back off one the cut would split.
    const amp = value.lastIndexOf('&', cut - 1);
    if (amp !== -1 && value.indexOf(';', amp) >= cut) cut = amp;
  }
  if (cut > 0 && /[\uD800-\uDBFF]/.test(value[cut - 1])) cut -= 1;
  return value.slice(0, cut).trimEnd() + '…';
}

/** The page's text(): whitespace-collapsed, trimmed, capped; '' for non-strings. */
function text(value, max) {
  if (typeof value !== 'string') return '';
  // Invalid XML characters become spaces first, so a stray control between two
  // words cannot glue them together once it is dropped.
  return clip(value.replace(XML_INVALID_RE, ' ').replace(/\s+/g, ' ').trim(), max);
}

function zonedInstantMs(value) {
  if (typeof value !== 'string') return null;
  const trimmed = value.trim();
  if (!ZONED_INSTANT_RE.test(trimmed)) return null;
  const ms = Date.parse(trimmed);
  return Number.isFinite(ms) ? ms : null;
}

function airedMsFromId(id) {
  const match = BULLETIN_ID_RE.exec(id);
  return match ? zonedInstantMs(`${match[1]}T${match[2]}:${match[3]}:00Z`) : null;
}

/** Mirror of normalizeAradioAudio: `{key, bytes, duration_s}`, a bare key, or null. */
function normalizeAudio(raw) {
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

/**
 * Mirror of aradioBulletinPath: the bulletin file relative to the station
 * directory, from the entry's `path` (tolerating a leading `/` or
 * `research/aradio/`) or else its id; null rather than an unvalidated path.
 */
export function aradioFeedBulletinPath(entry) {
  if (typeof entry.path === 'string') {
    const cleaned = entry.path.trim().replace(/^\/+/, '').replace(/^research\/aradio\//, '');
    if (BULLETIN_PATH_RE.test(cleaned)) return cleaned;
  }
  const match = BULLETIN_ID_RE.exec(entry.id);
  return match ? `bulletins/${match[1]}/${match[2]}${match[3]}.json` : null;
}

function normalizeEntry(raw) {
  if (!isRecord(raw)) return null;
  const id = typeof raw.id === 'string' ? raw.id.trim() : '';
  if (!SAFE_ID_RE.test(id)) return null;
  const airedMs = zonedInstantMs(raw.aired_at) ?? airedMsFromId(id);
  if (airedMs === null) return null;
  return {
    id,
    airedMs,
    headline: text(raw.headline, 200),
    path: aradioFeedBulletinPath({ id, path: raw.path }),
    audio: normalizeAudio(raw.audio),
  };
}

/**
 * The feed's episodes: the page's bulletin list (index.bulletins plus an
 * object `latest`, de-duplicated by id, newest first, at most 72) minus the
 * text-only bulletins. Ties are broken on the whole normalized entry, so
 * duplicate ids resolve the same way in any input order.
 */
export function selectAradioFeedEntries(index) {
  if (!isRecord(index)) return [];
  const candidates = Array.isArray(index.bulletins) ? index.bulletins.slice() : [];
  if (isRecord(index.latest)) candidates.push(index.latest);
  const ranked = candidates
    .map(normalizeEntry)
    .filter((entry) => entry !== null)
    .map((entry) => ({ entry, canonical: JSON.stringify(entry) }))
    .sort((a, b) =>
      b.entry.airedMs - a.entry.airedMs
      || (a.entry.id < b.entry.id ? 1 : a.entry.id > b.entry.id ? -1 : 0)
      || (a.canonical < b.canonical ? -1 : a.canonical > b.canonical ? 1 : 0));
  const seen = new Set();
  const list = [];
  for (const { entry } of ranked) {
    if (seen.has(entry.id)) continue;
    seen.add(entry.id);
    list.push(entry);
  }
  return list.slice(0, ARADIO_FEED_MAX_ITEMS).filter((entry) => entry.audio !== null);
}

/** The page's speakerLabel in English: Speaker 1 → Anchor, Speaker 2 → Co-host. */
function speakerLabel(speaker) {
  const role = SPEAKER_ROLE_RE.exec(speaker.trim())?.[1];
  if (role === '1') return 'Anchor';
  if (role === '2') return 'Co-host';
  return speaker || 'Anchor';
}

/** Mirror of normalizeLines: display `lines`, else the raw `script`. */
function transcriptLines(bulletin) {
  const lines = [];
  if (Array.isArray(bulletin.lines)) {
    for (const item of bulletin.lines) {
      if (!isRecord(item)) continue;
      const line = text(item.text, 1200);
      if (line) lines.push({ speaker: text(item.speaker, 40), text: line });
    }
  }
  if (lines.length === 0 && Array.isArray(bulletin.script)) {
    for (const item of bulletin.script) {
      if (typeof item !== 'string') continue;
      const match = SCRIPT_LINE_RE.exec(item.trim());
      if (!match) continue;
      const line = text(match[2].replace(AUDIO_TAG_RE, ''), 1200);
      if (line) lines.push({ speaker: match[1], text: line });
    }
  }
  return lines.slice(0, 60);
}

/** Join HTML-escaped paragraphs within `budget`, cutting only between them, marked "…". */
function capParagraphs(parts, budget) {
  let body = '';
  for (let i = 0; i < parts.length; i += 1) {
    const next = body ? `${body}\n\n${parts[i]}` : parts[i];
    // Until the last paragraph, keep room to close a cut with the mark.
    const room = i === parts.length - 1 ? budget : budget - CUT_MARK.length;
    if (next.length <= room) {
      body = next;
      continue;
    }
    // `body` is empty only if one paragraph overflows on its own: a
    // 1,200-character line that escaping has grown (`&` → `&amp;`). Cut inside
    // it rather than drop it.
    return body ? body + CUT_MARK : clip(parts[i], budget, true);
  }
  return body;
}

/**
 * The episode's <description> text, HTML-escaped (xmlEscape is applied on
 * output). The cap counts escaped characters: that is what an app receives.
 */
function describe(bulletin, headline, origin) {
  const footer = htmlEscapeText(`\n\nTranscript and sources: ${origin}/aradio`);
  const lines = bulletin ? transcriptLines(bulletin) : [];
  const parts = (lines.length ? lines.map((line) => `${speakerLabel(line.speaker)}: ${line.text}`) : [headline])
    .map(htmlEscapeText);
  return capParagraphs(parts, Math.max(0, ARADIO_FEED_DESCRIPTION_MAX - footer.length)) + footer;
}

const pad2 = (value) => String(value).padStart(2, '0');

function fallbackTitle(ms) {
  const date = new Date(ms);
  return `ARA Radio — ${date.getUTCDate()} ${MONTHS[date.getUTCMonth()]} ${date.getUTCFullYear()}, `
    + `${pad2(date.getUTCHours())}:${pad2(date.getUTCMinutes())} UTC`;
}

function lookup(bulletins, path) {
  if (!path || !bulletins) return undefined;
  if (bulletins instanceof Map) return bulletins.get(path);
  return isRecord(bulletins) && Object.hasOwn(bulletins, path) ? bulletins[path] : undefined;
}

function itemLines(entry, rawBulletin, origin, audioBase) {
  const bulletin = isRecord(rawBulletin) ? rawBulletin : null;
  const own = bulletin ? normalizeAudio(bulletin.audio) : null;
  // The bulletin's own size and duration describe this enclosure only when
  // they belong to the same S3 object.
  const same = own && own.key === entry.audio.key ? own : null;
  const bytes = entry.audio.bytes ?? same?.bytes ?? null;
  const durationS = entry.audio.durationS ?? same?.durationS ?? null;
  const seconds = durationS === null ? null : Math.round(durationS);
  const title = entry.headline || (bulletin ? text(bulletin.headline, 200) : '') || fallbackTitle(entry.airedMs);
  const lines = [
    '    <item>',
    // Titles stay plain text, XML-escaped only: podcast apps show <title> as
    // text and never parse it as HTML, so HTML-escaping it would put "&amp;"
    // on screen in place of "&".
    `      <title>${xmlEscape(title)}</title>`,
    `      <link>${xmlEscape(`${origin}/aradio`)}</link>`,
    `      <guid isPermaLink="false">${xmlEscape(entry.id)}</guid>`,
    `      <pubDate>${new Date(entry.airedMs).toUTCString()}</pubDate>`,
    `      <description>${xmlEscape(describe(bulletin, title, origin))}</description>`,
    // The URL the page plays: aradioAudioSrc(AUDIO_BASE, entry.audio).
    `      <enclosure url="${xmlEscape(`${audioBase}/${entry.audio.key}`)}" `
      + `length="${Number.isSafeInteger(bytes) ? bytes : 0}" type="audio/mpeg"/>`,
  ];
  if (Number.isSafeInteger(seconds) && seconds > 0) lines.push(`      <itunes:duration>${seconds}</itunes:duration>`);
  lines.push('    </item>');
  return lines;
}

/**
 * RSS 2.0 podcast feed for the station. `index` is the parsed index.json (any
 * value; a non-object yields a valid feed with no episodes); `bulletins` maps
 * a bulletin path relative to the station directory (Map or plain object) to
 * the parsed bulletin file. `ownerEmail` adds an <itunes:owner> block unless
 * it is blank or not a string.
 */
export function buildAradioFeed({
  index,
  bulletins,
  siteOrigin = DEFAULT_SITE_ORIGIN,
  audioBase = ARADIO_DEFAULT_AUDIO_BASE,
  ownerEmail = '',
} = {}) {
  const origin = String(siteOrigin).replace(/\/+$/, '');
  const base = String(audioBase).replace(/\/+$/, '');
  const artwork = `${origin}${ARADIO_FEED_ARTWORK_PATH}`;
  // 254 characters is the longest address SMTP can carry.
  const owner = text(ownerEmail, 254);
  const entries = selectAradioFeedEntries(index);
  const updatedMs = isRecord(index) ? zonedInstantMs(index.updated_at) : null;
  const lastBuildMs = updatedMs ?? entries[0]?.airedMs ?? null;
  const lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    `<rss version="2.0" xmlns:itunes="${ITUNES_NS}" xmlns:atom="${ATOM_NS}">`,
    '  <channel>',
    `    <title>${xmlEscape(CHANNEL_TITLE)}</title>`,
    `    <link>${xmlEscape(`${origin}/aradio`)}</link>`,
    `    <atom:link href="${xmlEscape(`${origin}/aradio/feed.xml`)}" rel="self" type="application/rss+xml"/>`,
    `    <description>${xmlEscape(htmlEscapeText(CHANNEL_DESCRIPTION))}</description>`,
    '    <language>en</language>',
  ];
  if (lastBuildMs !== null) lines.push(`    <lastBuildDate>${new Date(lastBuildMs).toUTCString()}</lastBuildDate>`);
  lines.push(
    // RSS 2.0 wants the channel's own title and link here. No width/height:
    // their 144x400 maximum describes a thumbnail, not this art.
    '    <image>',
    `      <url>${xmlEscape(artwork)}</url>`,
    `      <title>${xmlEscape(CHANNEL_TITLE)}</title>`,
    `      <link>${xmlEscape(`${origin}/aradio`)}</link>`,
    '    </image>',
    `    <itunes:author>${xmlEscape(CHANNEL_AUTHOR)}</itunes:author>`,
  );
  // Spotify for Creators mails its ownership code to <itunes:email>. Anyone
  // who opens the feed can read the address, so it is opt-in.
  if (owner) {
    lines.push(
      '    <itunes:owner>',
      `      <itunes:name>${xmlEscape(CHANNEL_AUTHOR)}</itunes:name>`,
      `      <itunes:email>${xmlEscape(owner)}</itunes:email>`,
      '    </itunes:owner>',
    );
  }
  lines.push(
    `    <itunes:image href="${xmlEscape(artwork)}"/>`,
    '    <itunes:explicit>false</itunes:explicit>',
    '    <itunes:type>episodic</itunes:type>',
    '    <itunes:category text="Technology"/>',
    '    <itunes:category text="News">',
    '      <itunes:category text="Tech News"/>',
    '    </itunes:category>',
  );
  for (const entry of entries) lines.push(...itemLines(entry, lookup(bulletins, entry.path), origin, base));
  lines.push('  </channel>', '</rss>', '');
  return lines.join('\n');
}

/**
 * Read `${dir}/index.json` and the bulletin file of every episode the feed
 * will carry. Missing or unparsable files count as absent (with a warning);
 * this never throws, so a station that has not aired yet still builds.
 */
export function readAradioFeedData(dir, { warn = console.warn } = {}) {
  const bulletins = new Map();
  let root;
  try {
    root = realpathSync(dir);
  } catch {
    warn(`aradio-feed: no station data at ${dir}; the feed has no episodes`);
    return { index: null, bulletins };
  }
  const index = readContainedJson(root, 'index.json', warn);
  if (index !== undefined && !isRecord(index)) warn('aradio-feed: index.json is not an object; the feed has no episodes');
  for (const entry of selectAradioFeedEntries(index)) {
    if (!entry.path || bulletins.has(entry.path)) continue;
    const bulletin = readContainedJson(root, entry.path, warn);
    if (bulletin !== undefined) bulletins.set(entry.path, bulletin);
  }
  return { index: index === undefined ? null : index, bulletins };
}

// `rel` is 'index.json' or a BULLETIN_PATH_RE match, so it is lexically inside
// `root`; resolving it also refuses a symlink that leads anywhere else.
function readContainedJson(root, rel, warn) {
  try {
    const file = realpathSync(join(root, rel));
    if (!file.startsWith(root + sep) || !statSync(file).isFile()) {
      warn(`aradio-feed: ${rel} is not a file inside the station directory; skipped`);
      return undefined;
    }
    return JSON.parse(readFileSync(file, 'utf8'));
  } catch (error) {
    warn(`aradio-feed: ${rel} unreadable (${error?.code || error?.message || error}); skipped`);
    return undefined;
  }
}
