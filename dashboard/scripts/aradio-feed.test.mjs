import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import {
  ARADIO_AUDIO_KEY_RE,
  ARADIO_DEFAULT_AUDIO_BASE,
  ARADIO_FEED_ARTWORK_PATH,
  ARADIO_FEED_DESCRIPTION_MAX,
  ARADIO_FEED_MAX_ITEMS,
  aradioFeedBulletinPath,
  buildAradioFeed,
  readAradioFeedData,
  selectAradioFeedEntries,
  xmlEscape,
} from './aradio-feed.mjs';

// The page's own rules, which the feed mirrors (node's type stripping loads
// the pure view module directly; postbuild itself never imports .ts).
const page = await import('../src/render/aradio.ts');

const FIXTURE_DIR = fileURLToPath(new URL('./fixtures/aradio/', import.meta.url));
const fixture = (path) => JSON.parse(readFileSync(join(FIXTURE_DIR, path), 'utf8'));
const INDEX = fixture('index.json');
const B1450 = fixture('bulletins/2026-10-30/1450.json');
const B1050 = fixture('bulletins/2026-10-30/1050.json');
const ORIGIN = 'https://ara.guzus.xyz';
const ARTWORK = 'https://ara.guzus.xyz/brand/aradio-cover.png';
const BASE = ARADIO_DEFAULT_AUDIO_BASE;
const FOOTER = `\n\nTranscript and sources: ${ORIGIN}/aradio`;
const ITUNES_NS = 'http://www.itunes.com/dtds/podcast-1.0.dtd';

// ── A strict XML 1.0 well-formedness checker ──────────────────────────────
// There is no XML parser in devDependencies, so this accepts only what the
// feed may emit and returns a tree with DECODED text/attribute values: one
// root after the declaration, matching tags, quoted unique attributes, only
// the five named entities or numeric references after `&`, no raw `<` or `>`
// in character data or attribute values (so `]]>` cannot occur either), no
// comments, CDATA, PIs or doctype, and no character XML 1.0 forbids.

const XML_CHARS_RE = /^[\t\n\r -퟿-�\u{10000}-\u{10FFFF}]*$/u;
const NAME = '[A-Za-z_][A-Za-z0-9._-]*(?::[A-Za-z_][A-Za-z0-9._-]*)?';
const START_TAG_RE = new RegExp(`^<(${NAME})((?:\\s+${NAME}\\s*=\\s*(?:"[^"]*"|'[^']*'))*)\\s*(/?)>`);
const ATTR_RE = new RegExp(`(${NAME})\\s*=\\s*(?:"([^"]*)"|'([^']*)')`, 'g');
const END_TAG_RE = new RegExp(`^</(${NAME})\\s*>`);
const DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>';
const NAMED_ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" };

function decode(raw, where) {
  assert.ok(!raw.includes('<'), `raw "<" in ${where}`);
  assert.ok(!raw.includes('>'), `raw ">" in ${where}`);
  return raw.replace(/&([^;]*);?/g, (whole, ref) => {
    assert.ok(whole.endsWith(';'), `unterminated reference ${JSON.stringify(whole)} in ${where}`);
    if (Object.hasOwn(NAMED_ENTITIES, ref)) return NAMED_ENTITIES[ref];
    const numeric = /^#(?:(\d+)|x([0-9A-Fa-f]+))$/.exec(ref);
    assert.ok(numeric, `unknown entity &${ref}; in ${where}`);
    const char = String.fromCodePoint(numeric[1] ? Number(numeric[1]) : parseInt(numeric[2], 16));
    assert.ok(XML_CHARS_RE.test(char), `reference to a forbidden character in ${where}`);
    return char;
  });
}

function parseXml(xml) {
  assert.ok(XML_CHARS_RE.test(xml), 'the document contains a character XML 1.0 forbids');
  assert.ok(xml.startsWith(DECLARATION), 'missing XML declaration');
  const document = { name: '#document', attrs: {}, children: [], text: '' };
  const stack = [document];
  let i = DECLARATION.length;
  while (i < xml.length) {
    const lt = xml.indexOf('<', i);
    const chunk = xml.slice(i, lt === -1 ? xml.length : lt);
    const open = stack.at(-1);
    if (open === document) assert.match(chunk, /^\s*$/, 'character data outside the root element');
    else open.text += decode(chunk, `<${open.name}>`);
    if (lt === -1) break;
    const rest = xml.slice(lt);
    assert.ok(!rest.startsWith('<!') && !rest.startsWith('<?'), `unexpected markup: ${rest.slice(0, 24)}`);
    const end = END_TAG_RE.exec(rest);
    if (end) {
      assert.ok(stack.length > 1, `stray end tag </${end[1]}>`);
      assert.equal(stack.pop().name, end[1], 'mismatched end tag');
      i = lt + end[0].length;
      continue;
    }
    const start = START_TAG_RE.exec(rest);
    assert.ok(start, `malformed tag: ${rest.slice(0, 40)}`);
    const attrs = {};
    for (const attr of start[2].matchAll(ATTR_RE)) {
      assert.ok(!Object.hasOwn(attrs, attr[1]), `duplicate attribute ${attr[1]}`);
      attrs[attr[1]] = decode(attr[2] ?? attr[3], `${start[1]}@${attr[1]}`);
    }
    const element = { name: start[1], attrs, children: [], text: '' };
    if (open === document) assert.equal(document.children.length, 0, 'more than one root element');
    open.children.push(element);
    if (!start[3]) stack.push(element);
    i = lt + start[0].length;
  }
  assert.equal(stack.length, 1, `unclosed <${stack.at(-1).name}>`);
  assert.equal(document.children.length, 1, 'no root element');
  return document.children[0];
}

const childrenNamed = (element, name) => element.children.filter((child) => child.name === name);
function one(element, name) {
  const found = childrenNamed(element, name);
  assert.equal(found.length, 1, `expected one <${name}> in <${element.name}>`);
  return found[0];
}
const channelOf = (xml) => one(parseXml(xml), 'channel');
const itemsOf = (xml) => childrenNamed(channelOf(xml), 'item');
const allNames = (element) => [element.name, ...element.children.flatMap(allNames)];

/** An independent parser (expat via python3), when one is installed. */
function expatCheck(t, xml) {
  const run = spawnSync('python3', ['-I', '-c', 'import sys, xml.dom.minidom as m; m.parseString(sys.stdin.buffer.read())'], { input: xml });
  if (run.error) {
    t.diagnostic('python3 unavailable: skipped the expat cross-check');
    return;
  }
  assert.equal(run.status, 0, `expat rejected the feed: ${run.stderr}`);
}

/** `YYYY-MM-DD-HHMM` for a UTC instant — the writer's bulletin id. */
function stampOf(ms) {
  return new Date(ms).toISOString().slice(0, 16).replace('T', '-').replace(':', '');
}

function entryAt(ms, extra = {}) {
  const id = stampOf(ms);
  return {
    id,
    aired_at: new Date(ms).toISOString().replace('.000Z', 'Z'),
    headline: `Bulletin ${id}`,
    audio: { key: `audio/aradio/${id}.mp3`, bytes: 1000, duration_s: 60 },
    ...extra,
  };
}

function withTempDir(fn) {
  const dir = mkdtempSync(join(tmpdir(), 'aradio-feed-'));
  try {
    return fn(dir);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

function writeJson(path, value) {
  mkdirSync(join(path, '..'), { recursive: true });
  writeFileSync(path, typeof value === 'string' ? value : JSON.stringify(value));
}

// ── Fixtures and parity with the page ─────────────────────────────────────

test('fixtures: two episodes, newest first; the text-only 12:50 bulletin is not one', (t) => {
  const warnings = [];
  const data = readAradioFeedData(FIXTURE_DIR, { warn: (message) => warnings.push(message) });
  assert.deepEqual(warnings, []);
  // Only the episodes' files are read: the text-only bulletin is never opened.
  assert.deepEqual([...data.bulletins.keys()].sort(), ['bulletins/2026-10-30/1050.json', 'bulletins/2026-10-30/1450.json']);
  const xml = buildAradioFeed({ ...data, siteOrigin: ORIGIN, audioBase: BASE });
  expatCheck(t, xml);
  const items = itemsOf(xml);
  assert.deepEqual(items.map((item) => one(item, 'guid').text), ['2026-10-30-1450', '2026-10-30-1050']);

  const [first, second] = items;
  assert.deepEqual(first.children.map((child) => child.name),
    ['title', 'link', 'guid', 'pubDate', 'description', 'enclosure', 'itunes:duration']);
  assert.equal(one(first, 'title').text, INDEX.bulletins[0].headline);
  assert.equal(one(first, 'link').text, `${ORIGIN}/aradio`);
  assert.deepEqual(one(first, 'guid').attrs, { isPermaLink: 'false' });
  assert.equal(one(first, 'pubDate').text, 'Fri, 30 Oct 2026 14:50:00 GMT');
  assert.deepEqual(one(first, 'enclosure').attrs, {
    url: `${BASE}/audio/aradio/2026-10-30-1450.mp3`,
    length: '3874211',
    type: 'audio/mpeg',
  });
  assert.equal(one(first, 'itunes:duration').text, '242');
  assert.equal(one(second, 'pubDate').text, 'Fri, 30 Oct 2026 10:50:00 GMT');
  assert.equal(one(second, 'enclosure').attrs.length, '3120044');
  assert.equal(one(second, 'itunes:duration').text, '196');

  // The transcript in the page's labels, blank-line separated, then the footer.
  const expected = B1450.lines
    .map((line) => `${line.speaker === 'Speaker 1' ? 'Anchor' : 'Co-host'}: ${line.text}`)
    .join('\n\n') + FOOTER;
  assert.equal(one(first, 'description').text, expected);
  assert.ok(one(second, 'description').text.startsWith(`Anchor: ${B1050.lines[0].text}\n\nCo-host: ${B1050.lines[1].text}`));
});

test('parity: the key policy is the page\'s, by source and by verdict', () => {
  assert.equal(ARADIO_AUDIO_KEY_RE.source, page.ARADIO_AUDIO_KEY_RE.source);
  assert.equal(ARADIO_AUDIO_KEY_RE.flags, page.ARADIO_AUDIO_KEY_RE.flags);
  assert.equal(ARADIO_AUDIO_KEY_RE.source, '^audio\\/aradio\\/[A-Za-z0-9._-]+\\.mp3$');
});

test('parity: episodes and enclosure URLs are exactly what the page lists and plays', () => {
  const t0 = Date.UTC(2026, 9, 30, 6, 50);
  const mixed = {
    bulletins: [
      entryAt(t0),
      entryAt(t0 + 3600e3, { audio: null }),
      entryAt(t0 + 7200e3, { audio: '  audio/aradio/bare-key.mp3  ' }),
      entryAt(t0 + 9000e3, { audio: { key: ' audio/aradio/padded.mp3\n', bytes: 5 } }),
      entryAt(t0 + 10800e3, { audio: { key: 'audio/aradio/../up.mp3' } }),
      { id: '../escape', aired_at: '2026-10-30T12:00:00Z', audio: 'audio/aradio/x.mp3' },
      { id: '2026-10-30-1150', headline: 'id-stamped time', audio: 'audio/aradio/2026-10-30-1150.mp3' },
    ],
    latest: entryAt(t0 + 14400e3),
  };
  for (const index of [INDEX, mixed]) {
    const pageEntries = page.normalizeAradioIndex(index).bulletins.filter((entry) => entry.audio !== null);
    assert.deepEqual(selectAradioFeedEntries(index).map((entry) => entry.id), pageEntries.map((entry) => entry.id));
    const items = itemsOf(buildAradioFeed({ index, bulletins: new Map(), siteOrigin: ORIGIN, audioBase: BASE }));
    assert.deepEqual(
      items.map((item) => one(item, 'enclosure').attrs.url),
      pageEntries.map((entry) => page.aradioAudioSrc(BASE, entry.audio)),
    );
  }
});

test('parity: bulletin paths are rebuilt exactly as the page rebuilds them', () => {
  const cases = [
    { id: '2026-10-30-1450', path: 'bulletins/2026-10-30/1450.json' },
    { id: '2026-10-30-1450', path: '/research/aradio/bulletins/2026-10-30/1450.json' },
    { id: '2026-10-30-1450', path: '//bulletins/2026-10-30/1450.json' },
    { id: '2026-10-30-1450', path: '../../../etc/passwd' },
    { id: '2026-10-30-1450', path: 'bulletins/2026-10-30/../../../decoy.json' },
    { id: '2026-10-30-1450', path: 'https://evil.example/bulletins/2026-10-30/1450.json' },
    { id: '2026-10-30-1450', path: 42 },
    { id: 'custom-id', path: '../decoy.json' },
    { id: 'custom-id' },
  ];
  for (const entry of cases) assert.equal(aradioFeedBulletinPath(entry), page.aradioBulletinPath(entry), JSON.stringify(entry));
  assert.equal(aradioFeedBulletinPath({ id: 'custom-id', path: '../../../etc/passwd' }), null);
});

test('parity: the default audio base is main.ts AUDIO_BASE\'s default', () => {
  const main = readFileSync(new URL('../src/main.ts', import.meta.url), 'utf8');
  const match = /VITE_AUDIO_BASE_URL\s*\|\|\s*(['"`])([^'"`]+)\1/.exec(main);
  assert.ok(match, 'main.ts no longer reads AUDIO_BASE from VITE_AUDIO_BASE_URL with a literal default');
  assert.equal(ARADIO_DEFAULT_AUDIO_BASE, match[2]);
});

// ── Hostile input ─────────────────────────────────────────────────────────

const HOSTILE = 'Q3 </title><script>alert(1)</script> & "quoted" \'apos\' ]]> nul\u0000 vt\u000b ff\u000c '
  + 'lone\uD800 pair😀 glued\u0000words end￾￿';
// Forbidden characters become spaces (so they never glue words together),
// whitespace collapses, and a valid surrogate pair survives.
const HOSTILE_CLEAN = 'Q3 </title><script>alert(1)</script> & "quoted" \'apos\' ]]> nul vt ff lone pair😀 '
  + 'glued words end';

test('hostile headline and transcript stay well-formed and come back verbatim', (t) => {
  const index = { bulletins: [entryAt(Date.UTC(2026, 9, 30, 14, 50), { headline: HOSTILE })] };
  const bulletin = {
    lines: [
      { speaker: 'Speaker 1', text: HOSTILE },
      // Nothing but forbidden characters: no line at all, not an empty "Co-host:".
      { speaker: 'Speaker 2', text: '\u0000\u0007￿' },
      { speaker: '<b>Guest</b> & "co"', text: 'A third voice keeps its own name.' },
    ],
  };
  const xml = buildAradioFeed({
    index,
    bulletins: new Map([['bulletins/2026-10-30/1450.json', bulletin]]),
    siteOrigin: ORIGIN,
    audioBase: BASE,
  });
  expatCheck(t, xml);
  assert.doesNotMatch(xml, /<script|<b>|CDATA/);
  const root = parseXml(xml);
  assert.ok(!allNames(root).some((name) => name === 'script' || name === 'b'));
  const [item] = childrenNamed(one(root, 'channel'), 'item');
  assert.deepEqual(item.children.map((child) => child.name),
    ['title', 'link', 'guid', 'pubDate', 'description', 'enclosure', 'itunes:duration']);
  assert.equal(one(item, 'title').text, HOSTILE_CLEAN);
  assert.equal(one(item, 'description').text,
    `Anchor: ${HOSTILE_CLEAN}\n\n<b>Guest</b> & "co": A third voice keeps its own name.${FOOTER}`);
});

test('xmlEscape covers both contexts and drops what escaping cannot fix', () => {
  assert.equal(xmlEscape('<a href="x">&\'</a>'), '&lt;a href=&quot;x&quot;&gt;&amp;&apos;&lt;/a&gt;');
  assert.equal(xmlEscape('a\u0000b\u0008c\u000bd\u000ce\u001ff￾g￿h\uDC00i'), 'abcdefghi');
  assert.equal(xmlEscape('tab\tlf\ncr\r ok 😀'), 'tab\tlf\ncr\r ok 😀');
  assert.equal(xmlEscape(null), '');
});

test('hostile audio keys never become enclosures (and the page agrees)', () => {
  const keys = [
    'audio/aradio/../../secret.mp3',
    'audio/aradio/nested/x.mp3',
    'audio/aradio/x.mp3?download=1',
    'audio/aradio/x.mp3#t=10',
    'https://evil.example/audio/aradio/x.mp3',
    '//evil.example/audio/aradio/x.mp3',
    'audio/aradio/x.wav',
    'audio/aradio/x.mp3.exe',
    '/audio/aradio/x.mp3',
    'audio/daily/x.mp3',
    'audio/aradio/x y.mp3',
    'audio/aradio/x%2F..%2Fy.mp3',
    'audio/aradio/x.mp3\nhttps://evil.example/',
    'AUDIO/ARADIO/X.MP3',
    '',
  ];
  const t0 = Date.UTC(2026, 9, 1);
  const bulletins = keys.flatMap((key, i) => [
    entryAt(t0 + i * 7200e3, { audio: { key, bytes: 1, duration_s: 1 } }),
    entryAt(t0 + i * 7200e3 + 3600e3, { audio: key }),
  ]);
  for (const key of keys) {
    assert.equal(page.normalizeAradioAudio(key), null, JSON.stringify(key));
    assert.equal(page.normalizeAradioAudio({ key }), null, JSON.stringify(key));
  }
  const xml = buildAradioFeed({ index: { bulletins }, siteOrigin: ORIGIN, audioBase: BASE });
  assert.equal(itemsOf(xml).length, 0);
  assert.doesNotMatch(xml, /evil|secret|nested/);

  // One valid key among them is the single episode.
  const valid = entryAt(Date.UTC(2026, 9, 30, 9, 50));
  const items = itemsOf(buildAradioFeed({ index: { bulletins: [...bulletins, valid] }, siteOrigin: ORIGIN, audioBase: BASE }));
  assert.deepEqual(items.map((item) => one(item, 'guid').text), [valid.id]);
});

test('a hostile path or symlink never pulls another file into the feed', () => {
  withTempDir((tmp) => {
    const decoy = { headline: 'DECOY', lines: [{ speaker: 'Speaker 1', text: 'DECOY-TRANSCRIPT' }], script: ['Speaker 1: DECOY-SCRIPT'] };
    writeJson(join(tmp, 'decoy.json'), decoy);
    const station = join(tmp, 'station');
    writeJson(join(station, 'decoy.json'), decoy);
    writeJson(join(station, 'bulletins', '2026-10-30', '1350.json'), {
      lines: [{ speaker: 'Speaker 2', text: 'REAL-TRANSCRIPT' }],
    });
    mkdirSync(join(station, 'bulletins', '2026-10-31'), { recursive: true });
    symlinkSync(join(tmp, 'decoy.json'), join(station, 'bulletins', '2026-10-31', '0950.json'));
    const t0 = Date.UTC(2026, 9, 30, 9, 50);
    writeJson(join(station, 'index.json'), {
      updated_at: '2026-10-31T10:00:00Z',
      bulletins: [
        // Verbatim paths are ignored; the id-derived file does not exist.
        entryAt(t0, { headline: 'Traversal path', path: '../decoy.json' }),
        entryAt(t0 + 3600e3, { headline: 'Etc path', path: '../../../etc/passwd' }),
        entryAt(t0 + 7200e3, { headline: 'Dot-dot inside path', path: 'bulletins/2026-10-30/../../decoy.json' }),
        { id: 'custom-id', aired_at: '2026-10-30T12:50:00Z', headline: 'No derivable path', path: '../../decoy.json', audio: 'audio/aradio/custom-id.mp3' },
        { id: 'other-id', aired_at: '2026-10-30T12:55:00Z', headline: 'Station-root decoy', path: 'decoy.json', audio: 'audio/aradio/other-id.mp3' },
        // A validated path whose file is a symlink out of the station.
        entryAt(Date.UTC(2026, 9, 31, 9, 50), { headline: 'Symlinked file' }),
        // The control: a validated path to a real file is read.
        entryAt(Date.UTC(2026, 9, 30, 13, 50), { headline: 'Real file' }),
      ],
    });
    const warnings = [];
    const data = readAradioFeedData(station, { warn: (message) => warnings.push(message) });
    const xml = buildAradioFeed({ ...data, siteOrigin: ORIGIN, audioBase: BASE });
    assert.doesNotMatch(xml, /DECOY/);
    assert.match(xml, /Co-host: REAL-TRANSCRIPT/);
    assert.equal(itemsOf(xml).length, 7);
    assert.ok(!data.bulletins.has('bulletins/2026-10-31/0950.json'));
    assert.ok(warnings.some((message) => message.includes('bulletins/2026-10-31/0950.json') && message.includes('not a file inside')));
    // Every key the reader produced is a validated relative bulletin path.
    for (const key of data.bulletins.keys()) assert.match(key, /^bulletins\/\d{4}-\d{2}-\d{2}\/\d{4}\.json$/);
    // Without a file, an episode is described by its headline.
    const traversal = itemsOf(xml).find((item) => one(item, 'title').text === 'Traversal path');
    assert.equal(one(traversal, 'description').text, `Traversal path${FOOTER}`);
  });
});

test('80 bulletins → the newest 72 episodes, and never one the page does not list', () => {
  const t0 = Date.UTC(2026, 9, 27);
  const all = Array.from({ length: 80 }, (_, i) => entryAt(t0 + i * 3600e3));
  const guids = (index) => itemsOf(buildAradioFeed({ index, siteOrigin: ORIGIN, audioBase: BASE }))
    .map((item) => one(item, 'guid').text);
  assert.equal(ARADIO_FEED_MAX_ITEMS, 72);
  const full = guids({ bulletins: all });
  assert.equal(full.length, 72);
  assert.equal(full[0], stampOf(t0 + 79 * 3600e3));
  assert.equal(full.at(-1), stampOf(t0 + 8 * 3600e3));
  assert.deepEqual(full, page.normalizeAradioIndex({ bulletins: all }).bulletins.map((entry) => entry.id));

  // Text-only bulletins leave gaps: the cap applies to the page's list first,
  // so the feed does not reach back past the oldest bulletin the page shows.
  const gappy = all.map((entry, i) => (i % 10 === 9 ? { ...entry, audio: null } : entry));
  const listed = page.normalizeAradioIndex({ bulletins: gappy }).bulletins;
  assert.equal(listed.length, 72);
  const episodes = guids({ bulletins: gappy });
  assert.equal(episodes.length, 64);
  assert.deepEqual(episodes, listed.filter((entry) => entry.audio !== null).map((entry) => entry.id));
});

// ── Empty and broken stations ─────────────────────────────────────────────

function assertEmptyFeed(t, xml, { lastBuildDate = null } = {}) {
  expatCheck(t, xml);
  const channel = channelOf(xml);
  assert.equal(childrenNamed(channel, 'item').length, 0);
  assert.equal(one(channel, 'title').text, 'ARA Radio');
  assert.equal(one(channel, 'itunes:image').attrs.href, ARTWORK);
  assert.equal(childrenNamed(channel, 'lastBuildDate')[0]?.text ?? null, lastBuildDate);
}

test('a missing directory, missing or broken index, or empty station is a valid empty feed', (t) => {
  withTempDir((tmp) => {
    const warnings = [];
    const warn = (message) => warnings.push(message);

    const missing = readAradioFeedData(join(tmp, 'never-created'), { warn });
    assert.equal(missing.index, null);
    assert.equal(missing.bulletins.size, 0);
    assertEmptyFeed(t, buildAradioFeed({ ...missing, siteOrigin: ORIGIN }));
    assert.match(warnings.pop(), /no station data/);

    const station = join(tmp, 'station');
    mkdirSync(station);
    const noIndex = readAradioFeedData(station, { warn });
    assert.equal(noIndex.index, null);
    assertEmptyFeed(t, buildAradioFeed({ ...noIndex, siteOrigin: ORIGIN }));
    assert.match(warnings.pop(), /index\.json unreadable \(ENOENT\)/);

    for (const raw of ['{"bulletins": [', '[]', '"index"', 'null', '42']) {
      writeFileSync(join(station, 'index.json'), raw);
      const data = readAradioFeedData(station, { warn });
      assertEmptyFeed(t, buildAradioFeed({ ...data, siteOrigin: ORIGIN }));
      assert.match(warnings.pop(), /index\.json (unreadable|is not an object)/, raw);
    }

    writeJson(join(station, 'index.json'), { schema: 1, updated_at: '2026-10-30T09:00:00Z', degraded: false, latest: null, bulletins: [] });
    const empty = readAradioFeedData(station, { warn });
    assertEmptyFeed(t, buildAradioFeed({ ...empty, siteOrigin: ORIGIN }), { lastBuildDate: 'Fri, 30 Oct 2026 09:00:00 GMT' });
    assert.deepEqual(warnings, []);
  });
  for (const index of [undefined, null, [], 'index', 42, {}, { bulletins: 'nope' }]) {
    assertEmptyFeed(t, buildAradioFeed({ index }));
  }
});

// ── Channel ───────────────────────────────────────────────────────────────

test('channel: podcast metadata, self link, categories, and square artwork', () => {
  const root = parseXml(buildAradioFeed({ index: INDEX, siteOrigin: ORIGIN, audioBase: BASE }));
  assert.equal(root.name, 'rss');
  assert.deepEqual(root.attrs, { version: '2.0', 'xmlns:itunes': ITUNES_NS, 'xmlns:atom': 'http://www.w3.org/2005/Atom' });
  const channel = one(root, 'channel');
  assert.equal(one(channel, 'title').text, 'ARA Radio');
  assert.equal(one(channel, 'link').text, `${ORIGIN}/aradio`);
  assert.deepEqual(one(channel, 'atom:link').attrs, { href: `${ORIGIN}/aradio/feed.xml`, rel: 'self', type: 'application/rss+xml' });
  assert.match(one(channel, 'description').text, /^A short two-host bulletin on what changed in AI/);
  assert.equal(one(channel, 'language').text, 'en');
  assert.equal(one(channel, 'lastBuildDate').text, 'Fri, 30 Oct 2026 14:52:10 GMT');
  assert.equal(one(channel, 'itunes:author').text, 'ARA');
  assert.equal(one(channel, 'itunes:explicit').text, 'false');
  assert.equal(one(channel, 'itunes:type').text, 'episodic');
  const categories = childrenNamed(channel, 'itunes:category');
  assert.deepEqual(categories.map((category) => category.attrs.text), ['Technology', 'News']);
  assert.equal(categories[0].children.length, 0);
  assert.deepEqual(categories[1].children.map((sub) => [sub.name, sub.attrs.text]), [['itunes:category', 'Tech News']]);
  // The same absolute HTTPS art for Apple (<itunes:image>) and plain RSS
  // (<image>, whose title and link are the channel's own).
  assert.deepEqual(one(channel, 'itunes:image').attrs, { href: ARTWORK });
  assert.deepEqual(one(channel, 'image').children.map((child) => [child.name, child.text]), [
    ['url', ARTWORK],
    ['title', 'ARA Radio'],
    ['link', `${ORIGIN}/aradio`],
  ]);
  // No owner unless one is configured (see the owner test).
  assert.equal(childrenNamed(channel, 'itunes:owner').length, 0);

  // Without updated_at, lastBuildDate is the newest episode's air time.
  const { updated_at: _omitted, ...withoutUpdated } = INDEX;
  assert.equal(one(channelOf(buildAradioFeed({ index: withoutUpdated })), 'lastBuildDate').text, 'Fri, 30 Oct 2026 14:50:00 GMT');
});

test('origin and audio base: trailing slashes dropped, values escaped', (t) => {
  const xml = buildAradioFeed({ index: INDEX, siteOrigin: 'https://preview.example/', audioBase: 'https://cdn.example/a&b"c/' });
  expatCheck(t, xml);
  const channel = channelOf(xml);
  assert.equal(one(channel, 'link').text, 'https://preview.example/aradio');
  assert.equal(one(channel, 'atom:link').attrs.href, 'https://preview.example/aradio/feed.xml');
  assert.equal(one(channel, 'itunes:image').attrs.href, 'https://preview.example/brand/aradio-cover.png');
  assert.equal(one(one(channel, 'image'), 'url').text, 'https://preview.example/brand/aradio-cover.png');
  const [first] = childrenNamed(channel, 'item');
  assert.equal(one(first, 'enclosure').attrs.url, 'https://cdn.example/a&b"c/audio/aradio/2026-10-30-1450.mp3');
  assert.ok(one(first, 'description').text.endsWith('\n\nTranscript and sources: https://preview.example/aradio'));
});

test('owner: absent unless an address is set; a set one is trimmed and escaped', (t) => {
  const reference = buildAradioFeed({ index: INDEX, siteOrigin: ORIGIN, audioBase: BASE });
  for (const ownerEmail of [undefined, null, '', '  \n ', '\u0000\u000b', 42, {}]) {
    // Byte-identical to a build that never heard of an owner.
    assert.equal(buildAradioFeed({ index: INDEX, siteOrigin: ORIGIN, audioBase: BASE, ownerEmail }), reference, String(ownerEmail));
  }
  assert.doesNotMatch(reference, /itunes:(?:owner|name|email)/);

  const plain = channelOf(buildAradioFeed({ index: INDEX, ownerEmail: '  radio@example.com\n' }));
  assert.deepEqual(one(plain, 'itunes:owner').children.map((child) => [child.name, child.text]), [
    ['itunes:name', 'ARA'],
    ['itunes:email', 'radio@example.com'],
  ]);

  // Markup in the setting stays text: no element of its own reaches the feed.
  const hostile = 'o\'neil&co@example.com</itunes:email></itunes:owner><itunes:block>Yes</itunes:block>';
  const xml = buildAradioFeed({ index: INDEX, siteOrigin: ORIGIN, audioBase: BASE, ownerEmail: hostile });
  expatCheck(t, xml);
  assert.doesNotMatch(xml, /<itunes:block/);
  assert.match(xml, /<itunes:email>o&apos;neil&amp;co@example\.com&lt;\/itunes:email&gt;&lt;\/itunes:owner&gt;/);
  const channel = channelOf(xml);
  assert.equal(childrenNamed(channel, 'itunes:block').length, 0);
  assert.equal(one(one(channel, 'itunes:owner'), 'itunes:email').text, hostile);
});

/** A PNG's chunks as {type, data}, checking the signature first. */
function pngChunks(png) {
  assert.deepEqual([...png.subarray(0, 8)], [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a], 'not a PNG');
  const chunks = [];
  for (let at = 8; at + 12 <= png.length; at += 12 + png.readUInt32BE(at)) {
    chunks.push({ type: png.toString('latin1', at + 4, at + 8), data: png.subarray(at + 8, at + 8 + png.readUInt32BE(at)) });
  }
  return chunks;
}

test('artwork: the file the feed names is art Apple and Spotify accept', () => {
  // The URL is what directories cache; a new design ships under a new name.
  assert.equal(ARADIO_FEED_ARTWORK_PATH, '/brand/aradio-cover.png');
  const png = readFileSync(new URL(`../public${ARADIO_FEED_ARTWORK_PATH}`, import.meta.url));
  // A git-lfs pointer would fail the signature: Railway's build does not hydrate LFS.
  const chunks = pngChunks(png);
  assert.deepEqual([chunks[0].type, chunks.at(-1).type], ['IHDR', 'IEND']);
  const ihdr = chunks[0].data;
  const [width, height] = [ihdr.readUInt32BE(0), ihdr.readUInt32BE(4)];
  // Apple: square, 1400-3000 px. Spotify: 1:1.
  assert.equal(width, height);
  assert.ok(width >= 1400 && width <= 3000, `${width}x${height}`);
  // 8-bit truecolor: RGB with no alpha channel, and no transparency chunk.
  assert.deepEqual({ depth: ihdr[8], colorType: ihdr[9] }, { depth: 8, colorType: 2 });
  assert.ok(!chunks.some((chunk) => chunk.type === 'tRNS'));
  // Apple asks for 72 dpi (pHYs counts pixels per metre).
  const phys = chunks.find((chunk) => chunk.type === 'pHYs')?.data;
  assert.ok(phys && phys[8] === 1, 'pHYs in pixels per metre');
  assert.deepEqual([phys.readUInt32BE(0), phys.readUInt32BE(4)].map((ppm) => Math.round(ppm * 0.0254)), [72, 72]);
  // No directory caps the bytes; this keeps the art light for listeners and the image.
  assert.ok(png.length <= 512 * 1024, `${png.length} bytes`);
});

// ── Items ─────────────────────────────────────────────────────────────────

test('description falls back to the script (tags stripped), then to the headline', () => {
  const index = { bulletins: [entryAt(Date.UTC(2026, 9, 30, 14, 50), { headline: 'Script only' }), entryAt(Date.UTC(2026, 9, 30, 13, 50), { headline: 'No file' })] };
  const bulletin = {
    lines: [{ speaker: 'Speaker 1', text: '   ' }, 'not a line'],
    script: ['Speaker 2: [high_energy] Hello there.', 'Narrator: not a host line', 42, 'Speaker 1:  Bye [/whisper]for now.'],
  };
  const items = itemsOf(buildAradioFeed({ index, bulletins: { 'bulletins/2026-10-30/1450.json': bulletin }, siteOrigin: ORIGIN }));
  assert.equal(one(items[0], 'description').text, `Co-host: Hello there.\n\nAnchor: Bye for now.${FOOTER}`);
  assert.equal(one(items[1], 'description').text, `No file${FOOTER}`);
});

test('title falls back to the bulletin headline, then to the air time', () => {
  const index = {
    bulletins: [
      entryAt(Date.UTC(2026, 9, 30, 14, 50), { headline: '   ' }),
      entryAt(Date.UTC(2026, 10, 5, 9, 5), { headline: '\u0000\u0008￾' }),
      { id: '2026-10-29-2350', audio: 'audio/aradio/2026-10-29-2350.mp3' },
    ],
  };
  const bulletins = { 'bulletins/2026-10-30/1450.json': { headline: '  From   the file ' } };
  const items = itemsOf(buildAradioFeed({ index, bulletins }));
  assert.deepEqual(items.map((item) => one(item, 'title').text), [
    'ARA Radio — 5 Nov 2026, 09:05 UTC',
    'From the file',
    'ARA Radio — 29 Oct 2026, 23:50 UTC',
  ]);
  // aired_at is optional: the id's UTC run stamp is the air time.
  assert.equal(one(items[2], 'pubDate').text, 'Thu, 29 Oct 2026 23:50:00 GMT');
});

test('length and duration come from the index, else the same object\'s bulletin, else 0 / omitted', () => {
  const key = 'audio/aradio/2026-10-30-1450.mp3';
  const index = {
    bulletins: [
      entryAt(Date.UTC(2026, 9, 30, 14, 50), { audio: key }),
      entryAt(Date.UTC(2026, 9, 30, 13, 50), { audio: { key: 'audio/aradio/2026-10-30-1350.mp3' } }),
      entryAt(Date.UTC(2026, 9, 30, 12, 50), { audio: { key: 'audio/aradio/2026-10-30-1250.mp3', bytes: 2e21, duration_s: 'long' } }),
    ],
  };
  const bulletins = new Map([
    ['bulletins/2026-10-30/1450.json', { audio: { key, bytes: 1234.4, duration_s: 61.6 } }],
    // Another object's metadata never describes this enclosure.
    ['bulletins/2026-10-30/1350.json', { audio: { key: 'audio/aradio/other.mp3', bytes: 999, duration_s: 99 } }],
  ]);
  const items = itemsOf(buildAradioFeed({ index, bulletins }));
  assert.equal(one(items[0], 'enclosure').attrs.length, '1234');
  assert.equal(one(items[0], 'itunes:duration').text, '62');
  for (const item of items.slice(1)) {
    assert.equal(one(item, 'enclosure').attrs.length, '0');
    assert.equal(childrenNamed(item, 'itunes:duration').length, 0);
  }
});

test('description cap: 4,000 characters with the footer, cut between lines with "…"', () => {
  const budget = ARADIO_FEED_DESCRIPTION_MAX - FOOTER.length;
  const describeLines = (texts) => {
    const index = { bulletins: [entryAt(Date.UTC(2026, 9, 30, 14, 50))] };
    const lines = texts.map((text) => ({ speaker: 'Speaker 1', text }));
    const xml = buildAradioFeed({ index, bulletins: { 'bulletins/2026-10-30/1450.json': { lines } }, siteOrigin: ORIGIN });
    return one(itemsOf(xml)[0], 'description').text;
  };
  // Four paragraphs that fill the budget exactly fit with no cut mark.
  const width = (budget - 3 * 2) / 4 - 'Anchor: '.length;
  assert.ok(Number.isInteger(width) && width <= 1200);
  const exact = Array.from({ length: 4 }, (_, i) => String(i).repeat(width));
  const full = describeLines(exact);
  assert.equal(full.length, ARADIO_FEED_DESCRIPTION_MAX);
  assert.equal(full, exact.map((text) => `Anchor: ${text}`).join('\n\n') + FOOTER);
  // A fifth paragraph forces a cut; the fourth then no longer leaves room for
  // the mark, so the cut lands after the third, between whole lines.
  const cut = describeLines([...exact, 'tail']);
  assert.equal(cut, exact.slice(0, 3).map((text) => `Anchor: ${text}`).join('\n\n') + `\n\n…${FOOTER}`);
  // The worst case: 60 lines, each over the page's 1,200-character line cap.
  const originals = Array.from({ length: 60 }, (_, i) => `${i} ${'word '.repeat(400)}`);
  const long = describeLines(originals);
  assert.ok(long.length <= ARADIO_FEED_DESCRIPTION_MAX);
  assert.ok(long.endsWith(`\n\n…${FOOTER}`));
  const paragraphs = long.slice(0, -(`\n\n…${FOOTER}`).length).split('\n\n');
  assert.equal(paragraphs.length, 3);
  paragraphs.forEach((paragraph, i) => {
    // Each kept paragraph is one whole (capped) line, in order.
    assert.ok(paragraph.startsWith('Anchor: ') && paragraph.endsWith('…'), paragraph.slice(0, 40));
    const kept = paragraph.slice('Anchor: '.length, -1);
    assert.ok(originals[i].startsWith(kept) && kept.length >= 1190 && kept.length < 1200);
  });
});

// ── Determinism ───────────────────────────────────────────────────────────

test('determinism: input order, duplicate ids, container type and time zone do not change a byte', () => {
  const data = readAradioFeedData(FIXTURE_DIR, { warn: () => {} });
  const reference = buildAradioFeed({ ...data, siteOrigin: ORIGIN, audioBase: BASE });
  const [a, b, c] = INDEX.bulletins;
  const shuffled = { ...INDEX, bulletins: [c, a, b, a] };
  const reversed = new Map([...data.bulletins.entries()].reverse());
  assert.equal(buildAradioFeed({ index: shuffled, bulletins: reversed, siteOrigin: ORIGIN, audioBase: BASE }), reference);
  assert.equal(buildAradioFeed({ index: shuffled, bulletins: Object.fromEntries(reversed), siteOrigin: ORIGIN, audioBase: BASE }), reference);

  // Duplicate ids with different content resolve the same way in any order.
  const twinA = entryAt(Date.UTC(2026, 9, 30, 8, 50), { headline: 'Twin A' });
  const twinB = { ...twinA, headline: 'Twin B' };
  const forward = buildAradioFeed({ index: { bulletins: [twinA, twinB] } });
  assert.equal(buildAradioFeed({ index: { bulletins: [twinB], latest: twinA } }), forward);
  assert.equal(itemsOf(forward).length, 1);

  // A zone-less aired_at would be read in the host's zone; it falls back to
  // the id's UTC stamp instead, so every zone builds the same feed.
  const zoneless = { bulletins: [entryAt(Date.UTC(2026, 9, 30, 14, 50), { aired_at: '2026-10-30T14:50:00' })] };
  const saved = process.env.TZ;
  try {
    const builds = ['UTC', 'Asia/Seoul', 'America/Los_Angeles'].map((zone) => {
      process.env.TZ = zone;
      return [buildAradioFeed({ index: zoneless }), buildAradioFeed({ ...data })];
    });
    for (const build of builds.slice(1)) assert.deepEqual(build, builds[0]);
    assert.equal(one(itemsOf(builds[0][0])[0], 'pubDate').text, 'Fri, 30 Oct 2026 14:50:00 GMT');
  } finally {
    if (saved === undefined) delete process.env.TZ;
    else process.env.TZ = saved;
  }
});
