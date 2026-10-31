import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

// The view module is pure (no DOM) and imports i18n with an explicit .ts
// extension, so node's type stripping can load it directly.
const mod = await import('../src/render/aradio.ts');
const { uiText } = await import('../src/i18n.ts');
const { ARADIO_FEED_ARTWORK_PATH } = await import('./aradio-feed.mjs');

const fixture = (path) =>
  JSON.parse(readFileSync(new URL(`./fixtures/aradio/${path}`, import.meta.url), 'utf8'));

const INDEX = fixture('index.json');
const STATE = fixture('state.json');
const B1450 = fixture('bulletins/2026-10-30/1450.json');
const B1250 = fixture('bulletins/2026-10-30/1250.json');
const LATEST_MS = Date.parse('2026-10-30T14:50:00Z');

/** The radio's input: nothing loaded in the shared player unless overridden. */
function radioInput(overrides = {}) {
  return {
    bulletins: mod.normalizeAradioIndex(INDEX).bulletins,
    indexStatus: 'ok',
    programme: null,
    loaded: null,
    playing: false,
    ended: false,
    waiting: false,
    buffering: false,
    position: 0,
    duration: 0,
    stopAfter: false,
    ...overrides,
  };
}

function viewState(overrides = {}) {
  const index = 'index' in overrides ? overrides.index : mod.normalizeAradioIndex(INDEX);
  const board = mod.normalizeAradioBoard(STATE);
  const latestDetail = mod.normalizeAradioBulletin(B1450, mod.normalizeAradioIndex(INDEX).bulletins[0]);
  const state = {
    language: 'en',
    nowMs: LATEST_MS + 20 * 60 * 1000,
    index,
    indexStatus: 'ok',
    board,
    boardStatus: 'ok',
    selectedId: index?.bulletins[0]?.id ?? null,
    transcript: { kind: 'ready', bulletin: latestDetail },
    transcriptOpen: false,
    showAll: false,
    checkedAt: LATEST_MS + 19 * 60 * 1000,
    // The radio card's own transcript: the newest bulletin's, already loaded.
    script: { kind: 'ready', bulletin: latestDetail },
    ...overrides,
  };
  // The radio follows the (possibly overridden) index unless a test sets it.
  if (!('radio' in overrides)) state.radio = radioInput({ bulletins: index?.bulletins ?? [], indexStatus: state.indexStatus });
  return state;
}

/** A playable index entry at `HH:MM` UTC on 2026-10-30. */
function entry(hhmm, { audio = true, headline } = {}) {
  const id = `2026-10-30-${hhmm.replace(':', '')}`;
  return {
    id,
    aired_at: `2026-10-30T${hhmm}:00Z`,
    headline: headline ?? `Bulletin ${hhmm}`,
    audio: audio ? { key: `audio/aradio/${id}.mp3`, duration_s: 200, bytes: 3_000_000 } : null,
  };
}

const bulletinsOf = (...rows) => mod.normalizeAradioIndex({ bulletins: rows }).bulletins;
const rawOf = (bulletins) => bulletins.map((row) => ({ id: row.id, aired_at: row.airedAt, headline: row.headline, audio: row.audio }));
const ids = (list) => list.map((item) => (typeof item === 'string' ? item : item.id).slice(11));
const onNow = (programme) => programme.ids[programme.pos].slice(11);

test('index: newest first by aired_at, validated paths and audio, text-only kept', () => {
  const shuffled = { ...INDEX, bulletins: [INDEX.bulletins[2], INDEX.bulletins[0], INDEX.bulletins[1], INDEX.bulletins[0]] };
  const index = mod.normalizeAradioIndex(shuffled);
  assert.deepEqual(index.bulletins.map((item) => item.id), ['2026-10-30-1450', '2026-10-30-1250', '2026-10-30-1050']);
  assert.equal(index.bulletins[0].path, 'bulletins/2026-10-30/1450.json');
  assert.deepEqual(index.bulletins[0].audio, { key: 'audio/aradio/2026-10-30-1450.mp3', durationS: 242.1, bytes: 3874211 });
  assert.equal(index.bulletins[1].audio, null);
  assert.equal(index.degraded, false);
});

test('index: `latest` as an object is folded in; junk entries are dropped; non-objects are null', () => {
  const index = mod.normalizeAradioIndex({
    bulletins: [{ id: '2026-10-30-1050', aired_at: '2026-10-30T10:50:00Z' }, { id: '../x' }, null, 'str', { headline: 'no id' }],
    latest: { id: '2026-10-30-1150', headline: 'Newest' },
  });
  assert.deepEqual(index.bulletins.map((item) => item.id), ['2026-10-30-1150', '2026-10-30-1050']);
  // aired_at falls back to the UTC run stamp in the id.
  assert.equal(index.bulletins[0].airedAt, '2026-10-30T11:50:00.000Z');
  for (const raw of [null, [], 'index', 42]) assert.equal(mod.normalizeAradioIndex(raw), null);
  assert.deepEqual(mod.normalizeAradioIndex({}).bulletins, []);
});

test('index: caps at 72 bulletins', () => {
  const bulletins = Array.from({ length: 80 }, (_, i) => {
    const at = new Date(Date.UTC(2026, 9, 1) + i * 3600_000).toISOString();
    return { id: `b${i}`, aired_at: at, headline: `h${i}` };
  });
  const index = mod.normalizeAradioIndex({ bulletins });
  assert.equal(index.bulletins.length, 72);
  assert.equal(index.bulletins[0].id, 'b79');
});

test('fetch paths and S3 keys are rebuilt from validated shapes only', () => {
  const path = (p, id = '2026-10-30-1450') => mod.aradioBulletinPath({ id, path: p });
  assert.equal(path('bulletins/2026-10-30/1450.json'), 'bulletins/2026-10-30/1450.json');
  assert.equal(path('/research/aradio/bulletins/2026-10-30/1450.json'), 'bulletins/2026-10-30/1450.json');
  // Anything else falls back to the id-derived path, never through verbatim.
  for (const hostile of ['../../manifest.json', 'https://evil.example/x.json', 'bulletins/2026-10-30/1450.json?x=1', 'bulletins/../state.json']) {
    assert.equal(path(hostile), 'bulletins/2026-10-30/1450.json', hostile);
  }
  assert.equal(path('../x.json', 'not-a-stamp'), null);
});

test('audio guard: only audio/aradio/<name>.mp3 becomes a URL; anything else is text-only', () => {
  const base = 'https://s3.guzus.xyz/obj-ai-research-arm';
  assert.equal(mod.aradioAudioSrc(base, { key: 'audio/aradio/2026-10-30-1450.mp3' }), `${base}/audio/aradio/2026-10-30-1450.mp3`);
  const hostile = [
    'audio/aradio/2026/1450.mp3', 'audio/aradio/../../research/state.mp3', 'audio/aradio/x.mp3?y=1',
    'audio/aradio/x.mp3#t', 'audio/2026-10-30-digest.mp3', 'audio/aradio/x.wav', 'https://evil.example/audio/aradio/a.mp3',
    '/audio/aradio/a.mp3', 'audio/aradio/a b.mp3', 'audio/aradio/%2e%2e.mp3', '',
  ];
  for (const key of hostile) {
    assert.equal(mod.aradioAudioSrc(base, { key }), null, key);
    assert.equal(mod.normalizeAradioAudio(key), null, key);
    assert.equal(mod.normalizeAradioAudio({ key, duration_s: 200 }), null, key);
  }
  assert.equal(mod.aradioAudioSrc(base, null), null);
  assert.equal(mod.aradioAudioSrc(base, { key: 42 }), null);
  assert.equal(mod.normalizeAradioAudio({ key: 'audio/aradio/b.mp3', duration_s: 'x' }).durationS, null);

  // A bulletin whose key fails the policy is text-only: nothing to play.
  const index = mod.normalizeAradioIndex({
    bulletins: [{ id: '2026-10-30-1450', aired_at: '2026-10-30T14:50:00Z', headline: 'H', audio: { key: 'audio/aradio/../x.mp3' } }],
  });
  assert.equal(index.bulletins[0].audio, null);
  const { html } = mod.renderAradioView(viewState({ index, transcript: { kind: 'none' } }));
  assert.doesNotMatch(html, /data-aradio-play=|data-aradio-toggle/);
  assert.match(html, /No audio to play yet/);
});

test('board: unresolved by status then importance; resolved kept apart', () => {
  const board = mod.normalizeAradioBoard(STATE);
  const { open, resolved } = mod.sortAradioThreads(board.threads);
  assert.deepEqual(open.map((thread) => thread.slug), [
    'hyperscaler-capex-q3', // escalating, 5
    'hbm-supply-crunch', // escalating, 4
    'anthropic-ipo', // developing, 5
    'gemini-enterprise-pricing', // developing, 3
    'eu-ai-act-gpai-code', // steady
  ]);
  assert.deepEqual(resolved.map((thread) => thread.slug), ['openai-devday-launches']);
  // History is shown newest first.
  assert.match(board.threads[0].history[0].change, /^Escalating/);
});

test('board: hostile thread content is escaped, bad links dropped, enums clamped', () => {
  const board = mod.normalizeAradioBoard({
    threads: [
      {
        slug: 'x-thread', title: '<img src=x onerror=alert(1)>', status: 'ON FIRE', importance: 99,
        now: '"><script>alert(1)</script>', changed: 'c', watch: 'w',
        evidence: [
          { url: 'javascript:alert(1)', kind: 'podcast', label: 'js' },
          { url: 'data:text/html,hi', kind: 'video', label: 'data' },
          { url: 'https://example.com/a" onmouseover="alert(1)', kind: 'mystery', label: 'quote"break' },
        ],
      },
      { slug: 'BAD SLUG', title: 'dropped' },
      { slug: 'no-title' },
    ],
  });
  assert.equal(board.threads.length, 1);
  const [thread] = board.threads;
  assert.equal(thread.status, 'developing');
  assert.equal(thread.importance, 5);
  assert.equal(thread.evidence.length, 1);
  assert.equal(thread.evidence[0].kind, 'other');
  // No transcript, so the board's links are the only ones rendered.
  const { html, links } = mod.renderAradioView(viewState({ board, transcript: { kind: 'none' } }));
  assert.doesNotMatch(html, /<img src=x/);
  assert.doesNotMatch(html, /<script>/);
  assert.doesNotMatch(html, /javascript:|data:text|onmouseover/);
  assert.match(html, /&lt;img src=x onerror=alert\(1\)&gt;/);
  // The surviving link is not in the HTML at all: a slot plus a spec.
  assert.equal(links.length, 1);
  assert.equal(links[0].label, 'quote"break');
  assert.equal(links[0].url, 'https://example.com/a%22%20onmouseover=%22alert(1)');
  assert.match(html, /data-aradio-link="0"/);
});

// A document whose elements record properties and refuse HTML parsing: any
// regression to string-built links trips the innerHTML trap.
function fakeDocument() {
  const created = [];
  const doc = {
    createElement(tag) {
      const el = {
        tagName: tag.toUpperCase(),
        className: '',
        children: [],
        ownText: '',
        set textContent(value) { this.ownText = String(value); },
        get textContent() { return this.ownText + this.children.map((child) => child.textContent).join(''); },
        append(...nodes) { this.children.push(...nodes); },
        setAttribute() { throw new Error('links are built with properties, not attributes'); },
      };
      Object.defineProperty(el, 'innerHTML', {
        get() { return ''; },
        set() { throw new Error('innerHTML must never be used for evidence links'); },
      });
      created.push(el);
      return el;
    },
  };
  return { doc, created };
}

test('evidence links: no URL in the HTML; every link is built from a slot spec', () => {
  const { html, links } = mod.renderAradioView(viewState());
  assert.doesNotMatch(html, /<a\b[^>]*aradio-evidence/);
  assert.doesNotMatch(html, /https?:\/\//, 'URLs must not travel through HTML strings');
  assert.ok(links.length >= 8, `expected evidence links, got ${links.length}`);
  const slots = html.match(/data-aradio-link="\d+"/g) || [];
  assert.equal(slots.length, links.length);
  const { doc } = fakeDocument();
  for (const spec of links) {
    const anchor = mod.createAradioEvidenceLink(doc, spec);
    assert.equal(anchor.tagName, 'A');
    assert.equal(anchor.href, new URL(spec.url).href);
    assert.match(anchor.href, /^https?:\/\//);
    assert.equal(anchor.target, '_blank');
    assert.equal(anchor.rel, 'noopener noreferrer');
    assert.equal(anchor.textContent, spec.kindLabel + spec.label);
  }
});

test('link guard: only absolute http(s), href as a property, label as text', () => {
  for (const ok of ['https://www.sec.gov/x.htm', 'http://example.com/a?b=c#d', '  https://x.com/a/status/1  ']) {
    assert.ok(mod.parseAradioHttpUrl(ok) instanceof URL, ok);
  }
  for (const bad of [
    'javascript:alert(1)', 'JavaScript:alert(1)', 'data:text/html,<b>x</b>', 'vbscript:x', 'mailto:a@b.c',
    'ftp://example.com/x', '/models/forecast/x', '//evil.example/x', 'example.com/x', '', '   ', null, 42, {},
  ]) {
    assert.equal(mod.parseAradioHttpUrl(bad), null, String(bad));
    assert.equal(mod.safeHttpUrl(bad), null, String(bad));
  }
  // A spec that skipped normalization is re-checked at build time.
  const { doc, created } = fakeDocument();
  assert.equal(mod.createAradioEvidenceLink(doc, { url: 'javascript:alert(1)', kind: 'podcast', kindLabel: 'Podcast', label: 'x' }), null);
  assert.equal(created.length, 0, 'nothing is built for a rejected URL');
  const label = '<img src=x onerror=alert(1)> **[md](javascript:x)**';
  const anchor = mod.createAradioEvidenceLink(doc, { url: 'https://example.com/p', kind: 'not-a-kind', kindLabel: 'Source', label });
  assert.equal(anchor.className, 'aradio-evidence aradio-evidence--other');
  assert.equal(anchor.children[1].textContent, label, 'third-party label is inert text');
  assert.equal(anchor.title, label);
});

test('podcast feed address is a property set by hydration, never an HTML attribute', () => {
  const { html } = mod.renderAradioView(viewState());
  assert.match(html, /<input class="aradio-feed-input" type="text" readonly[^>]*data-aradio-feed-url[^>]*value="">/);
  assert.match(html, /data-aradio-copy-feed/);
  assert.match(html, /Apple Podcasts can follow a show by URL/);
  const inputs = [{ value: 'x' }, { value: '' }];
  const root = { querySelectorAll: (selector) => (selector === '[data-aradio-feed-url]' ? inputs : []) };
  mod.hydrateAradioFeed(root, 'https://ara.guzus.xyz/aradio/feed.xml');
  assert.deepEqual(inputs.map((input) => input.value), ['https://ara.guzus.xyz/aradio/feed.xml', 'https://ara.guzus.xyz/aradio/feed.xml']);
  mod.hydrateAradioFeed(root, 'javascript:alert(1)');
  assert.deepEqual(inputs.map((input) => input.value), ['', ''], 'a non-http address is never shown');
  assert.equal(mod.ARADIO_FEED_PATH, '/aradio/feed.xml');
});

test('the radio is one big labelled button and never adds an <audio> element', () => {
  const { html } = mod.renderAradioView(viewState());
  // The shared bottom bar owns the page's only <audio>; the view adds none.
  assert.doesNotMatch(html, /<audio\b/);
  assert.equal((html.match(/data-aradio-toggle/g) || []).length, 1);
  assert.match(html, /<button type="button" class="aradio-toggle" data-aradio-toggle aria-label="Play ARA Radio" aria-describedby="aradioNowHeadline">/);
  // A media button changes its name (Play ↔ Pause), so it carries no aria-pressed.
  assert.doesNotMatch(html, /data-aradio-toggle[^>]*aria-pressed/);
  assert.match(html, /<h2 class="aradio-station" id="aradioStation">ARA Radio<\/h2>/);
  assert.match(html, /data-aradio-radio="ready"/);
  // Off: previous/next stay focusable but inert; "stop after" is a real toggle.
  assert.match(html, /data-aradio-prev aria-label="Previous bulletin" aria-disabled="true"/);
  assert.match(html, /data-aradio-next aria-label="Next bulletin" aria-disabled="true"/);
  assert.match(html, /data-aradio-stop-after aria-pressed="false"/);
  assert.match(html, /<input class="aradio-seek" type="range"[^>]*aria-label="Seek bulletin audio"[^>]*disabled/);
  // One polite live region announces what starts playing.
  assert.equal((html.match(/aria-live="polite" data-aradio-live/g) || []).length, 1);
  // "Behind the broadcast" sits below the radio, as a second-level section.
  assert.ok(html.indexOf('data-aradio-radio=') < html.indexOf('Behind the broadcast'));
  assert.match(html, /<h2 class="aradio-behind-title" id="aradioBehindTitle">Behind the broadcast<\/h2>/);
  assert.match(html, /<h3 class="aradio-section-title" id="aradioBoardTitle">Situation board<\/h3>/);
});

test('ON AIR for two hours after the newest bulletin with audio, then its age', () => {
  assert.deepEqual(mod.aradioAirState(null, LATEST_MS), { state: 'none', ageMs: null });
  assert.equal(mod.aradioAirState('2026-10-30T14:50:00Z', LATEST_MS + 119 * 60_000).state, 'live');
  assert.equal(mod.aradioAirState('2026-10-30T14:50:00Z', LATEST_MS + 120 * 60_000).state, 'idle');
  // A viewer clock behind the writer's still reads as live, never negative.
  assert.deepEqual(mod.aradioAirState('2026-10-30T14:50:00Z', LATEST_MS - 60_000), { state: 'live', ageMs: 0 });

  const live = mod.renderAradioView(viewState()).html;
  assert.match(live, /class="aradio-badge is-live" data-aradio-badge>/);
  assert.match(live, /data-aradio-badge-text>On air</);
  const idle = mod.renderAradioView(viewState({ nowMs: LATEST_MS + 3 * 3600_000 })).html;
  assert.match(idle, /class="aradio-badge" data-aradio-badge>/);
  assert.match(idle, /data-aradio-badge-text>Latest bulletin · 3h ago</);

  // A text-only bulletin cannot be heard: ON AIR follows the newest playable
  // one, and the card says the newer one is there to read.
  const bulletins = bulletinsOf(entry('17:40', { audio: false }), entry('14:50'));
  const nowMs = Date.parse('2026-10-30T17:50:00Z');
  const view = mod.aradioRadioView(radioInput({ bulletins }), nowMs);
  assert.equal(view.air.state, 'idle');
  assert.equal(view.now.id, '2026-10-30-1450');
  assert.equal(view.textOnlyNewest.id, '2026-10-30-1740');
  const copy = mod.aradioRadioCopy(view, nowMs, 'en');
  assert.equal(copy.badge, 'Latest bulletin · 3h ago');
  assert.equal(copy.note, 'The 17:40 UTC bulletin is text only. Read it below.');
});

test('running order: newest first, text-only skipped, can start anywhere playable', () => {
  const bulletins = mod.normalizeAradioIndex(INDEX).bulletins;
  assert.deepEqual(mod.aradioPlayableIds(bulletins), ['2026-10-30-1450', '2026-10-30-1050']);
  assert.deepEqual(mod.startAradioProgramme(bulletins), { ids: ['2026-10-30-1450', '2026-10-30-1050'], pos: 0 });
  assert.deepEqual(mod.startAradioProgramme(bulletins, '2026-10-30-1050'), { ids: ['2026-10-30-1450', '2026-10-30-1050'], pos: 1 });
  assert.equal(mod.startAradioProgramme(bulletins, '2026-10-30-1250'), null, 'a text-only bulletin cannot start the radio');
  assert.equal(mod.startAradioProgramme([]), null);
  assert.equal(mod.startAradioProgramme(bulletinsOf(entry('12:50', { audio: false }))), null);
});

test('running order: a bulletin that airs mid-listen plays next, several in the order they aired', () => {
  const start = bulletinsOf(entry('14:50'), entry('13:50', { audio: false }), entry('12:50'), entry('11:50'));
  const programme = mod.startAradioProgramme(start);
  assert.deepEqual(ids(programme.ids), ['1450', '1250', '1150']);
  assert.equal(mod.syncAradioProgramme(programme, start), programme, 'nothing new: same object');

  // 15:50 and 16:50 air (and a text-only 16:20) while 14:50 plays.
  const newer = bulletinsOf(entry('16:50'), entry('16:20', { audio: false }), entry('15:50'), ...rawOf(start));
  const synced = mod.syncAradioProgramme(programme, newer);
  assert.deepEqual(ids(synced.ids), ['1450', '1550', '1650', '1250', '1150']);
  assert.equal(synced.pos, 0, 'the bulletin on now keeps playing');
  assert.deepEqual(ids(mod.aradioUpNext(synced, newer)), ['1550', '1650', '1250']);

  // Another one airs before those have played: it queues behind them.
  const newest = bulletinsOf(entry('17:50'), ...rawOf(newer));
  assert.deepEqual(ids(mod.syncAradioProgramme(synced, newest).ids), ['1450', '1550', '1650', '1750', '1250', '1150']);

  // Listening to an older bulletin: the new ones still play next.
  const onOld = { ids: programme.ids, pos: 2 };
  assert.deepEqual(ids(mod.syncAradioProgramme(onOld, newer).ids), ['1450', '1250', '1150', '1550', '1650']);
});

test('running order: steps skip bulletins that left the index; up next lists what follows', () => {
  const bulletins = bulletinsOf(entry('14:50'), entry('12:50'), entry('10:50'));
  const programme = { ids: ['2026-10-30-1450', '2026-10-30-1350', '2026-10-30-1250', '2026-10-30-1050'], pos: 0 };
  const next = mod.stepAradioProgramme(programme, bulletins, 1);
  assert.equal(next.pos, 2, '13:50 aged out of the index and is skipped');
  assert.equal(mod.stepAradioProgramme(next, bulletins, -1).pos, 0);
  assert.equal(mod.stepAradioProgramme(programme, bulletins, -1), null);
  assert.equal(mod.stepAradioProgramme({ ids: programme.ids, pos: 3 }, bulletins, 1), null);
  assert.deepEqual(ids(mod.aradioUpNext(programme, bulletins)), ['1250', '1050']);
  assert.deepEqual(ids(mod.aradioUpNext(programme, bulletins, 1)), ['1250']);
});

test('radio view: off, playing, paused — what is on and what comes next', () => {
  const bulletins = mod.normalizeAradioIndex(INDEX).bulletins;
  const [b1450, , b1050] = bulletins;
  const nowMs = LATEST_MS + 20 * 60_000;

  const off = mod.aradioRadioView(radioInput(), nowMs);
  assert.equal(off.kind, 'ready');
  assert.equal(off.mode, 'off');
  assert.equal(off.now.id, b1450.id, 'pressing play starts the newest bulletin with audio');
  assert.deepEqual(off.upNext.map((item) => item.id), [b1050.id], 'the text-only 12:50 is skipped');
  assert.equal(off.canPrevious, false);
  assert.equal(off.canNext, false);
  assert.equal(off.seekable, false);
  const offCopy = mod.aradioRadioCopy(off, nowMs, 'en');
  assert.equal(offCopy.label, 'Up first');
  assert.equal(offCopy.toggleLabel, 'Play ARA Radio');
  assert.equal(offCopy.toggleIcon, 'play');
  assert.equal(offCopy.elapsed, '0:00');
  assert.equal(offCopy.remaining, '−4:02', 'the index duration until the audio loads');
  assert.equal(offCopy.time, '14:50 UTC');

  const programme = mod.startAradioProgramme(bulletins);
  const playing = mod.aradioRadioView(radioInput({ programme, loaded: b1450, playing: true, position: 61.4, duration: 242.1 }), nowMs);
  assert.equal(playing.mode, 'playing');
  assert.equal(playing.canNext, true);
  assert.equal(playing.canPrevious, true);
  assert.equal(playing.seekable, true);
  const playingCopy = mod.aradioRadioCopy(playing, nowMs, 'en');
  assert.equal(playingCopy.label, 'Now playing');
  assert.equal(playingCopy.toggleLabel, 'Pause ARA Radio');
  assert.equal(playingCopy.toggleIcon, 'pause');
  assert.equal(playingCopy.elapsed, '1:01');
  assert.equal(playingCopy.remaining, '−3:00');
  assert.equal(playingCopy.seekText, '1:01 of 4:02');
  assert.deepEqual([playingCopy.seekMax, playingCopy.seekValue], [242, 61]);

  const paused = mod.aradioRadioView(radioInput({ programme, loaded: b1450, playing: false, position: 61, duration: 242.1 }), nowMs);
  const pausedCopy = mod.aradioRadioCopy(paused, nowMs, 'en');
  assert.equal(paused.mode, 'paused');
  assert.equal(pausedCopy.label, 'Paused');
  assert.equal(pausedCopy.toggleLabel, 'Resume ARA Radio');
  assert.equal(pausedCopy.toggleIcon, 'play');

  // Buffering shows on the button only while it is meant to be playing.
  assert.match(
    mod.renderAradioRadio(viewState({ radio: radioInput({ programme, loaded: b1450, playing: true, buffering: true }) })),
    /class="aradio-toggle is-playing is-buffering"/,
  );
  assert.equal(mod.aradioRadioView(radioInput({ programme, loaded: b1450, buffering: true }), nowMs).buffering, false);
});

test('radio view: caught up stays on; "stop after this bulletin" turns it off on the next one', () => {
  const bulletins = mod.normalizeAradioIndex(INDEX).bulletins;
  const [b1450, , b1050] = bulletins;
  const nowMs = LATEST_MS + 20 * 60_000;
  const programme = mod.startAradioProgramme(bulletins);

  // The last bulletin ended: on, silent, the next to air plays by itself.
  const last = { ids: programme.ids, pos: 1 };
  const waiting = mod.aradioRadioView(radioInput({ programme: last, loaded: b1050, ended: true, waiting: true, duration: 196.4, position: 196.4 }), nowMs);
  assert.equal(waiting.mode, 'waiting');
  assert.deepEqual(waiting.upNext, []);
  assert.equal(waiting.canNext, false);
  assert.equal(waiting.canPrevious, true, 'previous replays the last bulletin');
  const waitingCopy = mod.aradioRadioCopy(waiting, nowMs, 'en');
  assert.equal(waitingCopy.label, 'Caught up');
  assert.equal(waitingCopy.toggleLabel, 'Turn off ARA Radio');
  assert.equal(waitingCopy.toggleIcon, 'pause');
  assert.match(mod.renderAradioUpNext(waiting, waitingCopy), /New bulletins play as soon as they air/);

  // Stopped after 14:50: play resumes with the next in the running order...
  const stopped = mod.aradioRadioView(radioInput({ programme, loaded: b1450, ended: true }), nowMs);
  assert.equal(stopped.mode, 'off');
  assert.equal(stopped.now.id, b1050.id);
  assert.deepEqual(stopped.upNext, []);
  // ...and after the last one, from the newest again.
  const stoppedLast = mod.aradioRadioView(radioInput({ programme: last, loaded: b1050, ended: true }), nowMs);
  assert.equal(stoppedLast.now.id, b1450.id);
  assert.deepEqual(stoppedLast.upNext.map((item) => item.id), [b1050.id]);

  const html = mod.renderAradioRadio(viewState({ radio: radioInput({ programme, loaded: b1450, playing: true, stopAfter: true }) }));
  assert.match(html, /data-aradio-stop-after aria-pressed="true"/);
  assert.match(html, /aradio-deck aradio-mode--playing/);
});

test('audio failure: the radio skips to the next bulletin that can play, in running order', () => {
  const bulletins = bulletinsOf(entry('14:50'), entry('13:50', { audio: false }), entry('12:50'), entry('11:50'), entry('10:50'));
  const programme = mod.startAradioProgramme(bulletins);
  assert.deepEqual(ids(programme.ids), ['1450', '1250', '1150', '1050']);

  // 14:50 fails: 12:50 plays next (the text-only 13:50 was never in the order).
  const first = mod.failAradioProgramme(programme, bulletins, '2026-10-30-1450');
  assert.equal(first.action, 'skip');
  assert.equal(onNow(first.programme), '1250');
  assert.deepEqual(ids(first.programme.failed), ['1450']);
  assert.deepEqual(first.programme.ids, programme.ids, 'the order itself is unchanged');

  // 12:50 fails too: on to 11:50, both failures carried.
  const second = mod.failAradioProgramme(first.programme, bulletins, '2026-10-30-1250');
  assert.equal(second.action, 'skip');
  assert.equal(onNow(second.programme), '1150');
  assert.deepEqual(ids(second.programme.failed), ['1450', '1250']);

  // Listening to an older bulletin: a failure moves on, never back to the newest.
  const onOld = mod.startAradioProgramme(bulletins, '2026-10-30-1150');
  assert.equal(onNow(mod.failAradioProgramme(onOld, bulletins, '2026-10-30-1150').programme), '1050');
  // A bulletin that left the index meanwhile is passed over as well.
  const aged = bulletinsOf(entry('14:50'), entry('12:50'), entry('10:50'));
  assert.equal(onNow(mod.failAradioProgramme(first.programme, aged, '2026-10-30-1250').programme), '1050');
});

test('audio failure: a failed bulletin is never tried again by itself; one failure is handled once', () => {
  const bulletins = bulletinsOf(entry('14:50'), entry('12:50'), entry('10:50'));
  const on1250 = mod.stepAradioProgramme(mod.startAradioProgramme(bulletins), bulletins, 1);
  const { programme } = mod.failAradioProgramme(on1250, bulletins, '2026-10-30-1250');
  assert.equal(onNow(programme), '1050');
  assert.equal(mod.aradioHasFailed(programme, '2026-10-30-1250'), true);
  assert.equal(mod.aradioHasFailed(programme, '2026-10-30-1050'), false);
  assert.equal(mod.aradioHasFailed(null, '2026-10-30-1250'), false);

  // The element's `error` and the rejected play() describe one failure: the
  // second report, or a late one about a bulletin no longer on, is a no-op.
  assert.equal(mod.failAradioProgramme(programme, bulletins, '2026-10-30-1250'), null);
  assert.equal(mod.failAradioProgramme(programme, bulletins, '2026-10-30-1450'), null);
  assert.equal(mod.failAradioProgramme(on1250, bulletins, '2026-10-30-1450'), null, 'only the bulletin on now can fail');

  // Previous and next step over it, and "Up next" leaves it out.
  const back = mod.stepAradioProgramme(programme, bulletins, -1);
  assert.equal(onNow(back), '1450');
  assert.equal(onNow(mod.stepAradioProgramme(back, bulletins, 1)), '1050');
  assert.deepEqual(ids(mod.aradioUpNext(back, bulletins)), ['1050']);
  assert.deepEqual(ids(mod.aradioRadioView(radioInput({ bulletins, programme: back, loaded: bulletins[0], playing: true }), LATEST_MS).upNext), ['1050']);

  // Polls never bring it back: the same index is a no-op, and a newer one
  // carries the failure and queues only the new bulletin.
  assert.equal(mod.syncAradioProgramme(programme, bulletins), programme);
  const newer = bulletinsOf(entry('15:50'), ...rawOf(bulletins));
  const synced = mod.syncAradioProgramme(programme, newer);
  assert.deepEqual(ids(synced.ids), ['1450', '1250', '1050', '1550']);
  assert.deepEqual(ids(synced.failed), ['1250']);
  assert.deepEqual(ids(mod.aradioUpNext(synced, newer)), ['1550']);
  // A session the listener starts afresh (a bulletin picked in the log) is clean.
  assert.equal(mod.startAradioProgramme(newer, '2026-10-30-1250').failed, undefined);
});

test('audio failure: when everything left fails the radio stops, says so and offers to try again', () => {
  const bulletins = bulletinsOf(entry('14:50'), entry('12:50', { audio: false }), entry('10:50'));
  const [b1450, , b1050] = bulletins;
  const nowMs = LATEST_MS + 20 * 60_000;
  const skip = mod.failAradioProgramme(mod.startAradioProgramme(bulletins), bulletins, b1450.id);
  assert.equal(skip.action, 'skip');
  const stop = mod.failAradioProgramme(skip.programme, bulletins, b1050.id);
  assert.equal(stop.action, 'stop');
  assert.equal(onNow(stop.programme), '1050', 'the order stays on the last failure');
  assert.deepEqual(ids(stop.programme.failed), ['1450', '1050']);
  assert.equal(mod.failAradioProgramme(stop.programme, bulletins, b1050.id), null, 'the rejected play() after `error` adds nothing');
  assert.equal(mod.stepAradioProgramme(stop.programme, bulletins, 1), null);
  assert.equal(mod.stepAradioProgramme(stop.programme, bulletins, -1), null, 'nothing behind it can play either');

  // The player still holds 10:50: the card says it stopped, never a silent "Paused".
  const input = radioInput({ bulletins, programme: stop.programme, loaded: b1050, playing: false });
  const view = mod.aradioRadioView(input, nowMs);
  assert.equal(view.mode, 'failed');
  assert.equal(mod.aradioRadioView({ ...input, waiting: true }, nowMs).mode, 'failed', 'a stop outranks caught up');
  assert.equal(view.now.id, b1450.id, 'play tries again from the first bulletin missed');
  assert.deepEqual(view.upNext.map((item) => item.id), [b1050.id]);
  assert.equal(view.canPrevious, false);
  assert.equal(view.canNext, false);
  assert.equal(view.seekable, false);
  assert.equal(view.elapsed, 0);
  const copy = mod.aradioRadioCopy(view, nowMs, 'en');
  assert.equal(copy.label, 'Couldn’t play');
  assert.equal(copy.toggleLabel, 'Try ARA Radio again');
  assert.equal(copy.toggleIcon, 'play');
  assert.equal(copy.note, 'The audio didn’t load. Try again, or read the transcript.');
  assert.equal(copy.time, '14:50 UTC');
  const html = mod.renderAradioRadio(viewState({ index: { updatedAt: null, degraded: false, bulletins }, radio: input }));
  assert.match(html, /aradio-deck aradio-mode--failed/);
  assert.match(html, /data-aradio-now-label>Couldn’t play</);
  assert.match(html, /data-aradio-toggle aria-label="Try ARA Radio again"/);
  assert.match(html, /data-aradio-note>The audio didn’t load\. Try again, or read the transcript\.</);

  // Trying again is a fresh session from 14:50, so each gets one more go.
  const retry = mod.retryAradioProgramme(stop.programme, bulletins);
  assert.deepEqual(retry, { ids: stop.programme.ids, pos: 0 });
  assert.equal(onNow(mod.stepAradioProgramme(retry, bulletins, 1)), '1050');
  for (const [key, time] of [['aradio.skipFailed', '14:50'], ['aradio.stoppedFailed', '10:50'], ['aradio.playerFailed', '10:50']]) {
    assert.ok(uiText('en', key, { time }).includes(`${time} UTC`), key);
  }
});

test('audio failure: trying again replays what was missed, not what already played', () => {
  const bulletins = bulletinsOf(entry('14:50'), entry('12:50'), entry('10:50'));
  // 14:50 failed and was skipped, 12:50 played to its end, then 10:50 failed.
  const on1250 = mod.failAradioProgramme(mod.startAradioProgramme(bulletins), bulletins, '2026-10-30-1450').programme;
  const on1050 = mod.stepAradioProgramme(on1250, bulletins, 1);
  const stop = mod.failAradioProgramme(on1050, bulletins, '2026-10-30-1050');
  assert.equal(stop.action, 'stop');
  const retry = mod.retryAradioProgramme(stop.programme, bulletins);
  assert.equal(onNow(retry), '1050', '12:50 played, so only 10:50 was missed');
  assert.equal(retry.failed, undefined);
  // What was missed has left the index: nothing to retry (the radio starts from the newest).
  assert.equal(mod.retryAradioProgramme(stop.programme, bulletinsOf(entry('14:50'), entry('12:50'))), null);
  const view = mod.aradioRadioView(radioInput({ bulletins: bulletinsOf(entry('14:50'), entry('12:50')), programme: stop.programme, loaded: bulletins[2] }), LATEST_MS);
  assert.equal(view.mode, 'failed');
  assert.equal(view.now.id, '2026-10-30-1450');
});

test('audio failure while caught up: the new bulletin is not retried and nothing spins', () => {
  const bulletins = bulletinsOf(entry('14:50'), entry('12:50'));
  // Everything played: caught up on 12:50, waiting for the next bulletin.
  const last = mod.stepAradioProgramme(mod.startAradioProgramme(bulletins), bulletins, 1);
  assert.equal(mod.stepAradioProgramme(last, bulletins, 1), null);

  // 15:50 airs; the poll queues it after the one on now and the radio starts it.
  const aired = bulletinsOf(entry('15:50'), ...rawOf(bulletins));
  const onNew = mod.stepAradioProgramme(mod.syncAradioProgramme(last, aired), aired, 1);
  assert.equal(onNow(onNew), '1550');

  // Its audio fails. Nothing follows it, so the radio stops on it rather than
  // claim "caught up" over a bulletin the listener never heard.
  const stop = mod.failAradioProgramme(onNew, aired, '2026-10-30-1550');
  assert.equal(stop.action, 'stop');
  // Later polls of the same index are no-ops: it is never queued or played again.
  for (let poll = 0; poll < 3; poll += 1) assert.equal(mod.syncAradioProgramme(stop.programme, aired), stop.programme);
  assert.equal(mod.stepAradioProgramme(stop.programme, aired, 1), null);
  assert.equal(mod.failAradioProgramme(stop.programme, aired, '2026-10-30-1550'), null);
  const view = mod.aradioRadioView(radioInput({ bulletins: aired, programme: stop.programme, loaded: aired[0] }), LATEST_MS + 70 * 60_000);
  assert.equal(view.mode, 'failed');
  assert.equal(view.now.id, '2026-10-30-1550', 'play tries the bulletin that failed');
  assert.deepEqual(view.upNext, []);

  // The next bulletin to air still joins the order behind it; trying again plays both.
  const later = bulletinsOf(entry('16:50'), ...rawOf(aired));
  const synced = mod.syncAradioProgramme(stop.programme, later);
  assert.deepEqual(ids(synced.ids), ['1450', '1250', '1550', '1650']);
  assert.deepEqual(ids(synced.failed), ['1550']);
  const retry = mod.retryAradioProgramme(synced, later);
  assert.equal(onNow(retry), '1550');
  assert.deepEqual(ids(mod.aradioUpNext(retry, later)), ['1650']);
});

test('radio card: hostile headlines are escaped wherever they show', () => {
  const headline = '<img src=x onerror=alert(1)> "quoted" & \'single\'';
  const bulletins = bulletinsOf(entry('14:50', { headline }), entry('12:50', { headline }));
  const html = mod.renderAradioRadio(viewState({ index: { updatedAt: null, degraded: false, bulletins }, radio: radioInput({ bulletins }) }));
  assert.doesNotMatch(html, /<img src=x/);
  assert.equal((html.match(/&lt;img src=x onerror=alert\(1\)&gt; &quot;quoted&quot; &amp; &#39;single&#39;/g) || []).length, 2, 'now playing and up next');
});

test('the radio card keeps its shape while bulletins change (no layout shift)', () => {
  const bulletins = mod.normalizeAradioIndex(INDEX).bulletins;
  const programme = mod.startAradioProgramme(bulletins);
  const shape = (html) => (html.match(/data-aradio-[a-z-]+/g) || []).join(' ');
  const off = mod.renderAradioRadio(viewState());
  const playing = mod.renderAradioRadio(viewState({ radio: radioInput({ programme, loaded: bulletins[0], playing: true, position: 30, duration: 242 }) }));
  const waiting = mod.renderAradioRadio(viewState({ radio: radioInput({ programme: { ids: programme.ids, pos: 1 }, loaded: bulletins[2], ended: true, waiting: true }) }));
  const failed = mod.renderAradioRadio(viewState({ radio: radioInput({ programme: { ids: programme.ids, pos: 1, failed: [bulletins[2].id] }, loaded: bulletins[2] }) }));
  // Same hooks in the same order: main.ts patches text in place.
  assert.equal(shape(playing), shape(off));
  assert.equal(shape(waiting), shape(off));
  assert.equal(shape(failed), shape(off));
  // Up next always fills its reserved rows: entries, or one line saying why not.
  assert.match(waiting, /<ol class="aradio-upnext-list" data-aradio-upnext><li class="aradio-upnext-empty">/);
});

test('before the first run: OFF AIR, an honest empty state and the podcast feed', () => {
  const html = mod.renderAradioView(viewState({
    index: null, indexStatus: 'missing', board: null, boardStatus: 'missing',
    selectedId: null, transcript: { kind: 'none' }, checkedAt: null,
  })).html;
  assert.match(html, /data-aradio-radio="none"/);
  assert.match(html, /class="aradio-badge is-off" data-aradio-badge>/);
  assert.match(html, /data-aradio-badge-text>Off air</);
  assert.match(html, /The first bulletin hasn’t aired yet/);
  assert.match(html, /Checks for new bulletins every 5 minutes/);
  assert.match(html, /Listen in your podcast app/);
  assert.match(html, /data-aradio-feed-url/);
  assert.doesNotMatch(html, /data-aradio-toggle|aradio-board|aradio-bulletins|class="aradio-behind"/);

  const failed = mod.renderAradioView(viewState({
    index: null, indexStatus: 'error', board: null, boardStatus: 'error',
    selectedId: null, transcript: { kind: 'none' }, checkedAt: null,
  })).html;
  assert.match(failed, /data-aradio-radio="error"/);
  assert.match(failed, /Could not reach the station/);
  assert.match(failed, /data-retry/);
});

test('only text-only bulletins: OFF AIR, nothing to play, the log is still there to read', () => {
  const bulletins = bulletinsOf(entry('14:50', { audio: false }), entry('12:50', { audio: false }));
  const index = { updatedAt: null, degraded: true, bulletins };
  const html = mod.renderAradioView(viewState({ index, transcript: { kind: 'none' } })).html;
  assert.match(html, /data-aradio-radio="text-only"/);
  assert.match(html, /No audio to play yet/);
  assert.match(html, /data-aradio-badge-text>Off air</);
  assert.doesNotMatch(html, /data-aradio-toggle|data-aradio-play=/);
  assert.match(html, /Behind the broadcast/);
  assert.equal((html.match(/data-aradio-row=/g) || []).length, 2);
  assert.equal(mod.startAradioProgramme(bulletins), null);
});

test('board without bulletins (first run went off air) still renders the board', () => {
  const html = mod.renderAradioView(viewState({
    index: { updatedAt: null, degraded: false, bulletins: [] }, selectedId: null, transcript: { kind: 'none' },
  })).html;
  assert.match(html, /The first bulletin hasn’t aired yet/);
  assert.match(html, /Situation board/);
  assert.doesNotMatch(html, /aradio-bulletins/);
});

test('text-only bulletins render without a play control', () => {
  const { html } = mod.renderAradioView(viewState({ showAll: true }));
  assert.match(html, /data-aradio-row="2026-10-30-1250"><span class="aradio-log-noaudio"/);
  assert.doesNotMatch(html, /data-aradio-play="2026-10-30-1250"/);
  assert.match(html, /Text only/);
  const bulletin = mod.normalizeAradioBulletin(B1250, mod.normalizeAradioIndex(INDEX).bulletins[1]);
  const transcript = mod.renderAradioTranscript({ kind: 'ready', bulletin }, { language: 'en', boardSlugs: new Set() }).html;
  assert.match(transcript, /Audio did not make it for this bulletin/);
  assert.doesNotMatch(transcript, /data-aradio-play=/);
  assert.doesNotMatch(transcript, /HTTP 503/, 'raw audio_error is operational detail, not reader copy');
});

test('transcript: collapsed until asked for, then speaker roles, follow-along spans, live covers', () => {
  const bulletin = mod.normalizeAradioBulletin(B1450);
  const { html, links } = mod.renderAradioTranscript(
    { kind: 'ready', bulletin },
    { language: 'en', boardSlugs: new Set(['hbm-supply-crunch', 'anthropic-ipo']) },
  );
  assert.match(html, /^<details class="aradio-transcript-details" data-aradio-transcript-details><summary class="aradio-transcript-summary">/);
  assert.match(html, /<span class="aradio-transcript-summary-label">Transcript<\/span><time datetime="2026-10-30T14:50:00.000Z">14:50 UTC<\/time>/);
  assert.match(
    mod.renderAradioTranscript({ kind: 'ready', bulletin }, { language: 'en', boardSlugs: new Set(), open: true }).html,
    /^<details class="aradio-transcript-details" data-aradio-transcript-details open>/,
  );
  assert.match(mod.renderAradioView(viewState()).html, /data-aradio-transcript-details><summary/, 'the page starts collapsed');
  assert.match(mod.renderAradioView(viewState({ transcriptOpen: true })).html, /data-aradio-transcript-details open><summary/);

  assert.equal(links.length, 4, 'one link spec per bulletin source');
  assert.equal((html.match(/class="aradio-line aradio-line--s1"/g) || []).length, 7);
  assert.equal((html.match(/class="aradio-line aradio-line--s2"/g) || []).length, 6);
  assert.match(html, />Anchor</);
  assert.match(html, />Co-host</);
  assert.match(html, /data-aradio-goto="hbm-supply-crunch"/);
  assert.doesNotMatch(html, /data-aradio-goto="hyperscaler-capex-q3"/);
  assert.match(html, /Script by claude-opus-5/);
  // A bulletin with audio can be played from any line: each is a button, one tab stop for the list.
  assert.equal((html.match(/data-aradio-seek-line="\d+"/g) || []).length, 13);
  assert.equal((html.match(/data-aradio-seek-line="\d+" tabindex="0"/g) || []).length, 1);
  assert.match(html, /data-aradio-seek-line="0" tabindex="0"/);
  assert.doesNotMatch(html, /aria-current="true"|is-following/, 'nothing is being read: no live line');
});

test('bulletin: falls back to the raw script (tags stripped) and to the index entry', () => {
  const fallback = { id: '2026-10-30-0950', airedAt: '2026-10-30T09:50:00.000Z', headline: 'From the index' };
  const bulletin = mod.normalizeAradioBulletin({
    script: ['Speaker 1: [high_energy] Hello [emphasis]there[/emphasis].', 'Speaker 2: Hi.', 'not a line'],
  }, fallback);
  assert.equal(bulletin.id, fallback.id);
  assert.equal(bulletin.headline, 'From the index');
  assert.deepEqual(bulletin.lines, [
    { speaker: 'Speaker 1', text: 'Hello there.' },
    { speaker: 'Speaker 2', text: 'Hi.' },
  ]);
  assert.equal(mod.normalizeAradioBulletin('nope'), null);
});

test('log shows a day of bulletins until expanded', () => {
  const bulletins = Array.from({ length: 30 }, (_, i) => ({
    id: `2026-10-29-${String(i).padStart(2, '0')}50`.slice(0, 15),
    aired_at: new Date(Date.UTC(2026, 9, 29) + i * 3600_000).toISOString(),
    headline: `Bulletin ${i}`,
    audio: { key: `audio/aradio/b${i}.mp3`, duration_s: 200 },
  }));
  const index = mod.normalizeAradioIndex({ bulletins });
  const collapsed = mod.renderAradioLog(viewState({ index }));
  assert.equal((collapsed.match(/data-aradio-row=/g) || []).length, mod.ARADIO_LOG_PREVIEW);
  assert.match(collapsed, /Show all 30 bulletins/);
  const expanded = mod.renderAradioLog(viewState({ index, showAll: true }));
  assert.equal((expanded.match(/data-aradio-row=/g) || []).length, 30);
  assert.match(expanded, /aria-expanded="true"/);
});

test('Korean: the radio, chrome, statuses, kinds and speakers are localized', () => {
  const { html, links } = mod.renderAradioView(viewState({ language: 'ko' }));
  for (const copy of [
    'ARA 라디오', '방송 중', '먼저 들을 방송', '다음 순서', '이 방송까지만 듣기', '팟캐스트 앱으로 듣기', '방송 배경 자료',
    '상황판', '확대 중', '전개 중', '대본', '앵커', '공동 진행자', 'aria-label="ARA 라디오 듣기"',
  ]) {
    assert.ok(html.includes(copy), `missing Korean copy: ${copy}`);
  }
  assert.ok(links.some((link) => link.kindLabel === '실적 발표 콜'), 'evidence kinds are localized too');
  assert.doesNotMatch(html, />Situation board<|>Up next<|>Behind the broadcast</);

  // Every radio string reads as Korean, not as English left behind.
  const keys = [
    'aradio.station', 'aradio.album', 'aradio.latestAgo', 'aradio.upFirst', 'aradio.nowPlaying', 'aradio.paused',
    'aradio.caughtUp', 'aradio.playStation', 'aradio.pauseStation', 'aradio.resumeStation', 'aradio.turnOff',
    'aradio.previous', 'aradio.next', 'aradio.stopAfter', 'aradio.upNext', 'aradio.upNextEmpty', 'aradio.seekValue',
    'aradio.announceNow', 'aradio.textOnlyNewest', 'aradio.textOnlyTitle', 'aradio.textOnlyBody', 'aradio.podcastTitle',
    'aradio.podcastHint', 'aradio.feedLabel', 'aradio.copy', 'aradio.copied', 'aradio.copyFailed', 'aradio.behind',
    'aradio.behindHint', 'aradio.emptyTitle', 'aradio.emptyBody', 'aradio.player', 'aradio.playerTitle',
    'aradio.couldNotPlay', 'aradio.tryAgain', 'aradio.failedNote', 'aradio.skipFailed', 'aradio.stoppedFailed',
    'aradio.playerFailed',
  ];
  for (const key of keys) {
    assert.notEqual(uiText('ko', key), uiText('en', key), `${key} must be translated`);
    assert.match(uiText('ko', key), /[가-힣]/, `${key} must emit Hangul`);
  }
  // Every time-bearing failure message keeps its time in Korean too.
  for (const key of ['aradio.skipFailed', 'aradio.stoppedFailed', 'aradio.playerFailed']) {
    assert.ok(uiText('ko', key, { time: '12:50' }).includes('UTC 12:50'), key);
  }

  // A stop on failures reads as Korean on the card.
  const bulletins = mod.normalizeAradioIndex(INDEX).bulletins;
  const failed = mod.renderAradioRadio(viewState({
    language: 'ko',
    radio: radioInput({ programme: { ids: ['2026-10-30-1450', '2026-10-30-1050'], pos: 1, failed: ['2026-10-30-1450', '2026-10-30-1050'] }, loaded: bulletins[2] }),
  }));
  for (const key of ['aradio.couldNotPlay', 'aradio.tryAgain', 'aradio.failedNote']) {
    assert.ok(failed.includes(uiText('ko', key)), `failed card missing Korean ${key}`);
  }
});

// ── Following the transcript ──────────────────────────────────────────────

const REAL_0853 = JSON.parse(readFileSync(new URL('../../research/aradio/bulletins/2026-10-31/0853.json', import.meta.url), 'utf8'));
// Where each line of the first real bulletin actually starts, in seconds of
// its audio (171.98 s): word timestamps from a speech recogniser, checked
// against the silences ffmpeg's silencedetect finds at every turn change.
const REAL_0853_STARTS = [0.23, 12.55, 24.15, 26.25, 39.65, 51.6, 62.63, 69.97, 82.65, 96.18, 108.36, 116.86, 126.3, 140.85, 154.45, 163.51, 169.06];

test('timing: line spans tile the bulletin, a turn pause after each line, scaled to the real duration', () => {
  assert.equal(mod.aradioLineTimings([{ text: 'a b' }], 0), null);
  assert.equal(mod.aradioLineTimings([{ text: 'a b' }], Number.NaN), null);
  assert.equal(mod.aradioLineTimings([{ text: 'a b' }], -3), null);
  assert.deepEqual(mod.aradioLineTimings([], 120), []);
  assert.deepEqual(mod.aradioLineTimings([{ text: 'one line' }], 9), [{ start: 0, end: 9 }]);

  // Two equal lines: each gets half the speaking time; the gap belongs to the first.
  const pause = mod.ARADIO_TURN_PAUSE_S;
  const two = mod.aradioLineTimings([{ text: 'same words here' }, { text: 'same words here' }], 10);
  const speaking = (10 - pause) / 2;
  assert.ok(Math.abs(two[0].end - (speaking + pause)) < 1e-9);
  assert.ok(Math.abs(two[1].end - two[1].start - speaking) < 1e-9);

  // The real bulletin: contiguous, increasing, from 0 to the last second exactly.
  const lines = mod.normalizeAradioBulletin(REAL_0853).lines;
  const timings = mod.aradioLineTimings(lines, 171.98);
  assert.equal(timings.length, lines.length);
  assert.equal(timings[0].start, 0);
  assert.equal(timings.at(-1).end, 171.98);
  for (let i = 1; i < timings.length; i += 1) {
    assert.equal(timings[i].start, timings[i - 1].end);
    assert.ok(timings[i].start > timings[i - 1].start);
  }
  // A short bulletin cannot spend more than a fifth of itself on pauses.
  const many = Array.from({ length: 30 }, () => ({ text: 'Hi.' }));
  const short = mod.aradioLineTimings(many, 6);
  assert.ok(short.every((span) => span.end > span.start));
  assert.ok(Math.abs(short.at(-1).end - 6) < 1e-9);
});

test('timing: what is spoken longhand weighs more than its letters', () => {
  const w = mod.aradioLineWeight;
  assert.ok(w('UTC') > w('utc'), 'an acronym is spelled out');
  assert.ok(w('Nasdaq 100') > w('Nasdaq abc'), 'digits are read as words');
  assert.ok(w('first, second') > w('first second'), 'a comma is a pause');
  assert.ok(w('First. Second') > w('First Second'), 'so is a full stop inside the line');
  assert.equal(w('Done.'), w('Done'), 'the full stop that ends a line is the turn pause');
  assert.equal(w(''), 1, 'never zero');
  assert.equal(w('…'), 1);
});

test('timing: against the first real bulletin the estimate stays within about a second', () => {
  const lines = mod.normalizeAradioBulletin(REAL_0853).lines;
  assert.equal(lines.length, REAL_0853_STARTS.length);
  const timings = mod.aradioLineTimings(lines, 171.98);
  const errors = timings.map((span, i) => Math.abs(span.start - REAL_0853_STARTS[i]));
  const mean = errors.reduce((sum, e) => sum + e, 0) / errors.length;
  assert.ok(mean < 1.2, `mean start error ${mean.toFixed(2)} s`);
  assert.ok(Math.max(...errors) < 3, `worst start error ${Math.max(...errors).toFixed(2)} s`);
  // Sampled every 0.1 s, the line marked live is the one being read ~9 times in 10.
  let right = 0;
  let total = 0;
  for (let t = 0; t < 171.9; t += 0.1) {
    let actual = 0;
    while (actual + 1 < REAL_0853_STARTS.length && t >= REAL_0853_STARTS[actual + 1]) actual += 1;
    if (mod.aradioLiveLine(timings, t) === actual) right += 1;
    total += 1;
  }
  assert.ok(right / total > 0.88, `${((100 * right) / total).toFixed(1)}% of the time on the right line`);
});

test('timing: the live line, and which bulletin the player is reading', () => {
  const timings = [{ start: 0, end: 4 }, { start: 4, end: 9 }, { start: 9, end: 12 }];
  assert.equal(mod.aradioLiveLine(null, 3), -1);
  assert.equal(mod.aradioLiveLine([], 3), -1);
  assert.equal(mod.aradioLiveLine(timings, -1), -1);
  assert.equal(mod.aradioLiveLine(timings, Number.NaN), -1);
  assert.deepEqual([0, 3.99, 4, 8.9, 9, 12, 40].map((t) => mod.aradioLiveLine(timings, t)), [0, 0, 1, 1, 2, 2, 2]);

  const bulletins = mod.normalizeAradioIndex(INDEX).bulletins;
  const detail = mod.normalizeAradioBulletin(B1450, bulletins[0]);
  const programme = mod.startAradioProgramme(bulletins);
  const at = (overrides) => mod.aradioPlayerLine(radioInput({ programme, ...overrides }), detail);
  assert.equal(at({}), -1, 'nothing in the player');
  assert.equal(at({ loaded: bulletins[2], position: 50, duration: 196.4 }), -1, 'another bulletin is in the player');
  assert.equal(at({ loaded: bulletins[0], position: 0, duration: 242.1 }), 0);
  assert.equal(at({ loaded: bulletins[0], position: 241, duration: 242.1 }), detail.lines.length - 1);
  assert.equal(at({ loaded: bulletins[0], position: 30 }), mod.aradioLiveLine(mod.aradioLineTimings(detail.lines, 242.1), 30), 'the index duration until the audio loads');
  assert.equal(at({ loaded: bulletins[0], ended: true, waiting: true }), detail.lines.length, 'played to the end: every line is heard');
  assert.equal(at({ loaded: bulletins[0], programme: { ...programme, failed: [bulletins[0].id] } }), -1, 'a failed bulletin is not being read');
});

test('radio transcript: the bulletin on now follows along, a line plays from there, nothing is announced', () => {
  const bulletins = mod.normalizeAradioIndex(INDEX).bulletins;
  const programme = mod.startAradioProgramme(bulletins);
  const idle = mod.renderAradioRadio(viewState());
  assert.match(idle, /<section class="aradio-script" aria-labelledby="aradioScriptTitle">/);
  assert.match(idle, /<h3 class="aradio-script-title" id="aradioScriptTitle">Transcript<\/h3>/);
  assert.match(idle, /Timing is approximate/);
  assert.match(idle, /data-aradio-script-window>/);
  assert.equal((idle.match(/class="aradio-line-seek" data-aradio-seek-line="\d+"/g) || []).length, 13);
  assert.equal((idle.match(/tabindex="0"/g) || []).length, 1, 'one tab stop for the lines');
  const script = idle.slice(idle.indexOf('data-aradio-script-slot'), idle.indexOf('class="aradio-upnext"'));
  assert.doesNotMatch(script, /aria-current|is-following|is-past|is-live/, 'off: no line is live');
  assert.match(script, /<button type="button" class="aradio-relive" data-aradio-relive hidden>/);
  assert.match(script, /Back to live line/);
  // No live region inside the transcript: the line changing is never announced.
  assert.doesNotMatch(script, /aria-live/);
  assert.doesNotMatch(script, /\d:\d\d/, 'no per-line times: the timing is an estimate');

  const detail = mod.normalizeAradioBulletin(B1450, bulletins[0]);
  const live = mod.aradioLiveLine(mod.aradioLineTimings(detail.lines, 242.1), 61.4);
  assert.ok(live > 1);
  const playing = mod.renderAradioRadio(viewState({ radio: radioInput({ programme, loaded: bulletins[0], playing: true, position: 61.4, duration: 242.1 }) }));
  assert.match(playing, /class="aradio-lines aradio-lines--script is-following" data-aradio-lines="2026-10-30-1450"/);
  assert.equal((playing.match(/aria-current="true"/g) || []).length, 1);
  assert.match(playing, new RegExp(`data-aradio-line="${live}"><button type="button" class="aradio-line-seek" data-aradio-seek-line="${live}" tabindex="0" aria-current="true">`));
  assert.equal((playing.match(/ is-past"/g) || []).length, live);
  assert.match(playing, new RegExp(`class="aradio-line aradio-line--s\\d is-live" data-aradio-line="${live}"`));
});

test('radio transcript: the storylines it covered, with their status when it aired, linked to the board', () => {
  const html = mod.renderAradioRadio(viewState());
  assert.match(html, /<h3 class="aradio-covered-title" id="aradioCoveredTitle">In this bulletin<\/h3>/);
  // Every slug in the fixture's covers is on the board: each is a button to it.
  for (const slug of ['hyperscaler-capex-q3', 'hbm-supply-crunch', 'anthropic-ipo', 'eu-ai-act-gpai-code']) {
    assert.match(html, new RegExp(`data-aradio-goto="${slug}"`));
  }
  assert.match(html, /<span class="aradio-pill aradio-pill--escalating">Escalating<\/span><span class="aradio-covered-name">The HBM supply crunch<\/span>/);
  // One that has left the board is plain text.
  const board = { ...mod.normalizeAradioBoard(STATE) };
  board.threads = board.threads.filter((thread) => thread.slug !== 'anthropic-ipo');
  const off = mod.renderAradioRadio(viewState({ board }));
  assert.doesNotMatch(off, /data-aradio-goto="anthropic-ipo"/);
  assert.match(off, /<span class="aradio-covered-item is-static"><span class="aradio-pill aradio-pill--developing">Developing<\/span><span class="aradio-covered-name">Anthropic&#39;s IPO<\/span>/);
});

test('radio transcript: loading, failed, and hostile lines', () => {
  const bulletins = mod.normalizeAradioIndex(INDEX).bulletins;
  const loading = mod.renderAradioRadio(viewState({ script: undefined }));
  assert.match(loading, /aria-busy="true"/);
  assert.match(loading, /Loading the transcript…/);
  assert.match(loading, /data-aradio-script-key="en\|loading\|2026-10-30-1450"/);
  const failed = mod.renderAradioRadio(viewState({ script: { kind: 'error', entry: bulletins[0] } }));
  assert.match(failed, /This transcript did not load\. <button type="button" class="aradio-text-button" data-aradio-script-retry>Retry<\/button>/);

  const hostile = mod.normalizeAradioBulletin({
    ...B1450,
    lines: [{ speaker: '<b>x</b>', text: '<img src=x onerror=alert(1)> "q" & \'s\'' }],
    threads: [{ slug: 'hbm-supply-crunch', title: '<script>alert(1)</script>', status: 'escalating' }],
  }, bulletins[0]);
  const html = mod.renderAradioRadio(viewState({ script: { kind: 'ready', bulletin: hostile } }));
  assert.doesNotMatch(html, /<img src=x|<script>|<b>x<\/b>/);
  assert.match(html, /&lt;img src=x onerror=alert\(1\)&gt; &quot;q&quot; &amp; &#39;s&#39;/);
  assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
});

test('text-only station: the newest bulletin is there to read, as plain text', () => {
  const bulletins = bulletinsOf(entry('14:50', { audio: false }), entry('12:50', { audio: false }));
  const index = { updatedAt: null, degraded: true, bulletins };
  const textOnly = mod.normalizeAradioBulletin({ ...B1250, id: '2026-10-30-1450' }, bulletins[0]);
  const html = mod.renderAradioRadio(viewState({ index, radio: radioInput({ bulletins }), script: { kind: 'ready', bulletin: textOnly } }));
  assert.match(html, /data-aradio-radio="text-only"/);
  assert.match(html, /data-aradio-script-window tabindex="0" role="region" aria-labelledby="aradioScriptTitle"/);
  assert.match(html, /<p class="aradio-line-text">/);
  assert.doesNotMatch(html, /data-aradio-seek-line|data-aradio-relive|Timing is approximate|data-aradio-toggle/);
  assert.equal(mod.aradioRadioView(radioInput({ bulletins }), LATEST_MS).scriptEntry.id, '2026-10-30-1450');
});

test('player: ±15 s and speed beside the one big button; the cover at identity size', () => {
  const bulletins = mod.normalizeAradioIndex(INDEX).bulletins;
  const programme = mod.startAradioProgramme(bulletins);
  const off = mod.renderAradioRadio(viewState());
  assert.match(off, /data-aradio-back aria-label="Back 15 seconds" aria-disabled="true"/);
  assert.match(off, /data-aradio-forward aria-label="Forward 15 seconds" aria-disabled="true"/);
  assert.match(off, /<button type="button" class="aradio-rate" data-aradio-rate aria-label="Playback speed 1×">1×<\/button>/);
  // The big button stays one, between the skips.
  const order = ['data-aradio-prev', 'data-aradio-back', 'data-aradio-toggle', 'data-aradio-forward', 'data-aradio-next'].map((hook) => off.indexOf(hook));
  assert.deepEqual(order, order.slice().sort((a, b) => a - b));
  const playing = mod.renderAradioRadio(viewState({ rate: 1.5, radio: radioInput({ programme, loaded: bulletins[0], playing: true, position: 30, duration: 242.1 }) }));
  assert.match(playing, /data-aradio-back aria-label="Back 15 seconds" aria-disabled="false"/);
  assert.match(playing, /data-aradio-forward aria-label="Forward 15 seconds" aria-disabled="false"/);
  assert.match(playing, /aria-label="Playback speed 1\.5×">1\.5×</);
  // The show's cover: decorative (the station is named in text), the feed's and lock screen's file.
  assert.match(off, /<img class="aradio-art" src="\/brand\/aradio-cover\.png" alt="" width="64" height="64" decoding="async">/);
  assert.equal(mod.ARADIO_COVER_PATH, ARADIO_FEED_ARTWORK_PATH);
});

test('speed: 1×, 1.25×, 1.5×, 2× and round again; anything stored that is not one of them is 1×', () => {
  assert.deepEqual(mod.ARADIO_RATES, [1, 1.25, 1.5, 2]);
  assert.deepEqual([1, 1.25, 1.5, 2].map(mod.aradioNextRate), [1.25, 1.5, 2, 1]);
  for (const raw of [null, undefined, '', 'fast', '3', 0, -1, 1.1, '1.5x', Number.NaN, {}, '2e0x']) {
    assert.equal(mod.aradioParseRate(raw), 1, String(raw));
  }
  assert.equal(mod.aradioParseRate('1.25'), 1.25);
  assert.equal(mod.aradioParseRate(' 2 '), 2);
  assert.equal(mod.aradioNextRate(7), 1.25, 'an unknown speed counts as 1×');
  assert.deepEqual([1, 1.25, 1.5, 2].map(mod.aradioRateLabel), ['1×', '1.25×', '1.5×', '2×']);
});

test('liveness: when the station last aired and when to expect more, never a schedule or a listener count', () => {
  const html = mod.renderAradioRadio(viewState());
  assert.match(html, /<p class="aradio-liveness" data-aradio-liveness><time class="aradio-updated" datetime="2026-10-30T14:50:00\.000Z" data-aradio-rel="2026-10-30T14:50:00\.000Z" data-aradio-rel-key="aradio\.updated"[^>]*>Updated 20m ago\.<\/time>/);
  assert.match(html, /The next bulletin airs when the picture changes\./);
  assert.ok(mod.ARADIO_REL_KEYS.includes('aradio.updated'), 'the ticker re-ages it');
  // Off air the sign already says how old the latest bulletin is: not twice.
  const idle = mod.renderAradioRadio(viewState({ nowMs: LATEST_MS + 3 * 3600_000 }));
  assert.match(idle, /data-aradio-badge-text>Latest bulletin · 3h ago</);
  assert.match(idle, /<time hidden class="aradio-updated"/);
  // ...unless a newer text-only bulletin is what the station updated with.
  const newer = bulletinsOf(entry('17:40', { audio: false }), entry('14:50'));
  const copy = mod.aradioRadioCopy(mod.aradioRadioView(radioInput({ bulletins: newer }), Date.parse('2026-10-30T18:00:00Z')), Date.parse('2026-10-30T18:00:00Z'), 'en');
  assert.deepEqual([copy.badge, copy.updated, copy.updatedShown], ['Latest bulletin · 3h ago', 'Updated 20m ago.', true]);
  assert.doesNotMatch(html, /listen(er|ing)s?\b.*\d|\d+\s*listening/i);
  // A text-only bulletin newer than the last playable one still counts as an update.
  const bulletins = bulletinsOf(entry('17:40', { audio: false }), entry('14:50'));
  assert.equal(mod.aradioRadioView(radioInput({ bulletins }), LATEST_MS).updatedAt, '2026-10-30T17:40:00.000Z');
  // Before the first bulletin, or unreachable: nothing to date.
  for (const state of [
    { index: null, indexStatus: 'missing', board: null, boardStatus: 'missing', selectedId: null, transcript: { kind: 'none' }, script: { kind: 'none' } },
    { index: null, indexStatus: 'error', board: null, boardStatus: 'error', selectedId: null, transcript: { kind: 'none' }, script: { kind: 'none' } },
  ]) {
    assert.doesNotMatch(mod.renderAradioRadio(viewState(state)), /aradio-liveness/);
  }
});

test('log rows: a play pill with the length, the time left or "Played", filled by what was heard', () => {
  const listened = {
    '2026-10-30-1450': { at: 121.05, duration: 242.1, done: false },
    '2026-10-30-1050': { at: 196.4, duration: 196.4, done: true },
  };
  const html = mod.renderAradioLog(viewState({ showAll: true, listened }));
  assert.match(html, /<button type="button" class="aradio-log-play is-partial" data-aradio-play="2026-10-30-1450" aria-label="Play the 14:50 UTC bulletin: [^"]+ \(2:02 left\)" style="--aradio-heard:50\.0%">/);
  assert.match(html, /data-aradio-pill-text>2:02 left</);
  assert.match(html, /class="aradio-log-play is-done" data-aradio-play="2026-10-30-1050"[^>]*\(Played\)" style="--aradio-heard:100\.0%"/);
  const fresh = mod.renderAradioLog(viewState({ showAll: true }));
  assert.match(fresh, /class="aradio-log-play is-new" data-aradio-play="2026-10-30-1450"[^>]*\(4:02\)" style="--aradio-heard:0\.0%"/);
  assert.match(fresh, /data-aradio-pill-text>4:02</);
  // Text-only rows say so where the pill would be.
  assert.match(fresh, /data-aradio-row="2026-10-30-1250"><span class="aradio-log-noaudio">Text only<\/span>/);
});

test('listened: parsed defensively, written only when a pill would change, finishing is sticky', () => {
  for (const raw of [null, '', 'nope', '[]', '42', '{"x":1}', JSON.stringify({ '../x': { at: 1, duration: 2 } })]) {
    assert.deepEqual(mod.aradioParseListened(raw), {}, String(raw));
  }
  const parsed = mod.aradioParseListened(JSON.stringify({
    '2026-10-30-1450': { at: 500, duration: 242.1, done: false },
    '2026-10-30-1250': { at: -1, duration: 100 },
    '2026-10-30-1050': { at: 10, duration: 0 },
    '2026-10-30-0950': { at: 'x', duration: 100 },
  }));
  assert.deepEqual(parsed, { '2026-10-30-1450': { at: 242.1, duration: 242.1, done: false } }, 'clamped to the duration; junk dropped');

  const id = '2026-10-30-1450';
  let heard = mod.aradioRecordListen({}, id, 1.5, 242.1);
  assert.deepEqual(heard, {}, 'a second or two in is still unheard');
  heard = mod.aradioRecordListen(heard, id, 60, 242.1);
  assert.deepEqual(heard[id], { at: 60, duration: 242.1, done: false });
  assert.equal(mod.aradioRecordListen(heard, id, 60.4, 242.1), heard, 'under a second later: same object, no write');
  heard = mod.aradioRecordListen(heard, id, 240, 242.1);
  assert.equal(heard[id].done, true, 'within a few seconds of the end counts as heard');
  heard = mod.aradioRecordListen(heard, id, 20, 242.1);
  assert.deepEqual(heard[id], { at: 20, duration: 242.1, done: true }, 'replaying a heard bulletin keeps it heard');
  assert.equal(mod.aradioRecordListen(heard, '../evil', 20, 100), heard);
  assert.equal(mod.aradioRecordListen(heard, id, 20, Number.NaN), heard);
  assert.equal(mod.aradioRecordListen({}, id, 0, 242.1, true)[id].done, true, 'ended');

  assert.deepEqual(mod.aradioListenState(undefined, 242.1), { state: 'new', fraction: 0, remaining: 242.1 });
  assert.deepEqual(mod.aradioListenState({ at: 60.525, duration: 242.1, done: false }, null), { state: 'partial', fraction: 0.25, remaining: 181.575 });
  assert.equal(mod.aradioListenState({ at: 2, duration: 242.1, done: true }, null).state, 'done');

  const kept = mod.aradioPruneListened({ a1: heard[id], [id]: heard[id] }, [id, 'other']);
  assert.deepEqual(Object.keys(kept), [id]);
  const same = { [id]: heard[id] };
  assert.equal(mod.aradioPruneListened(same, [id]), same, 'nothing to drop: same object');
});

test('follow: a link per app this platform can open, none of them in the HTML', () => {
  const feed = 'https://ara.guzus.xyz/aradio/feed.xml';
  const iphone = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1';
  const ipad = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15';
  const android = 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Mobile Safari/537.36';
  const windows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36';
  assert.equal(mod.aradioPlatform(iphone), 'ios');
  assert.equal(mod.aradioPlatform(ipad, 5), 'ios', 'iPadOS reports a Mac; a touch screen gives it away');
  assert.equal(mod.aradioPlatform(ipad, 0), 'mac');
  assert.equal(mod.aradioPlatform(android, 5), 'android');
  assert.equal(mod.aradioPlatform(windows), 'other');
  assert.equal(mod.aradioPlatform(undefined), 'other');

  const apps = (links) => links.map((link) => `${link.app} ${link.href}${link.newTab ? ' (new tab)' : ''}`);
  assert.deepEqual(apps(mod.aradioFollowLinks(feed, 'ios')), [
    'apple podcast://ara.guzus.xyz/aradio/feed.xml',
    'overcast overcast://x-callback-url/add?url=https%3A%2F%2Fara.guzus.xyz%2Faradio%2Ffeed.xml',
    'pocketcasts pktc://subscribe/ara.guzus.xyz/aradio/feed.xml',
  ]);
  assert.deepEqual(apps(mod.aradioFollowLinks(feed, 'mac')), [
    'apple podcast://ara.guzus.xyz/aradio/feed.xml',
    'pocketcasts https://pocketcasts.com/follow/https://ara.guzus.xyz/aradio/feed.xml (new tab)',
  ]);
  assert.deepEqual(apps(mod.aradioFollowLinks(feed, 'android')), ['pocketcasts pktc://subscribe/ara.guzus.xyz/aradio/feed.xml']);
  assert.deepEqual(apps(mod.aradioFollowLinks(feed, 'other')), ['pocketcasts https://pocketcasts.com/follow/https://ara.guzus.xyz/aradio/feed.xml (new tab)']);
  // Spotify appears only once the show URL is set, and only a real show URL.
  assert.equal(mod.ARADIO_SPOTIFY_SHOW_URL, '', 'not listed yet: no Spotify button');
  const show = 'https://open.spotify.com/show/0123456789abcdefABCDEF';
  assert.deepEqual(apps(mod.aradioFollowLinks(feed, 'other', show)).slice(0, 1), [`spotify ${show} (new tab)`]);
  assert.deepEqual(apps(mod.aradioFollowLinks(feed, 'ios', show)).map((line) => line.split(' ')[0]), ['apple', 'spotify', 'overcast', 'pocketcasts']);
  for (const bad of ['https://open.spotify.com/show/short', 'javascript:alert(1)', 'https://evil.example/show/0123456789abcdefABCDEF', `${show}?si=x`]) {
    assert.ok(!mod.aradioFollowLinks(feed, 'ios', bad).some((link) => link.app === 'spotify'), bad);
  }
  // Only an https feed gets links.
  for (const bad of ['http://ara.guzus.xyz/aradio/feed.xml', 'javascript:alert(1)', '/aradio/feed.xml', '']) {
    assert.deepEqual(mod.aradioFollowLinks(bad, 'ios'), [], bad);
  }

  const { html } = mod.renderAradioView(viewState());
  assert.match(html, /<ul class="aradio-follow" data-aradio-follow-list hidden><li hidden><a class="aradio-follow-link" data-aradio-follow="apple" aria-label="Follow in Apple Podcasts">Apple Podcasts<\/a><\/li>/);
  assert.doesNotMatch(html, /podcast:\/\/|overcast:\/\/|pktc:\/\/|pocketcasts\.com|spotify\.com/);
  assert.match(html, /data-aradio-copy-feed>Copy RSS</);
});

test('follow: hydration gives the platform\'s buttons their links as properties and hides the rest', () => {
  const anchors = ['apple', 'spotify', 'overcast', 'pocketcasts'].map((app) => {
    const item = { hidden: true };
    const anchor = {
      dataset: { aradioFollow: app },
      href: '',
      target: '',
      rel: '',
      removed: [],
      closest: () => item,
      removeAttribute(name) { this.removed.push(name); if (name === 'href') this.href = ''; },
      item,
    };
    return anchor;
  });
  const list = { hidden: true, querySelectorAll: () => anchors };
  const root = { querySelectorAll: (selector) => (selector === '[data-aradio-follow-list]' ? [list] : []) };
  mod.hydrateAradioFollow(root, mod.aradioFollowLinks('https://ara.guzus.xyz/aradio/feed.xml', 'mac'));
  assert.equal(list.hidden, false);
  assert.deepEqual(anchors.map((a) => a.item.hidden), [false, true, true, false]);
  assert.equal(anchors[0].href, 'podcast://ara.guzus.xyz/aradio/feed.xml');
  assert.deepEqual([anchors[0].target, anchors[0].removed.includes('target')], ['', true], 'an app link opens in place');
  assert.equal(anchors[3].href, 'https://pocketcasts.com/follow/https://ara.guzus.xyz/aradio/feed.xml');
  assert.deepEqual([anchors[3].target, anchors[3].rel], ['_blank', 'noopener noreferrer'], 'a web page opens beside the radio');
  mod.hydrateAradioFollow(root, []);
  assert.equal(list.hidden, true, 'nothing to offer: the list hides');
});

test('Korean: the transcript, player, follow and log strings are translated', () => {
  const keys = [
    'aradio.updated', 'aradio.nextAirs', 'aradio.jumpBack', 'aradio.jumpForward', 'aradio.speed', 'aradio.scriptNote',
    'aradio.lineHint', 'aradio.backToLive', 'aradio.inThisBulletin', 'aradio.followIn', 'aradio.played', 'aradio.timeLeft', 'aradio.pillPlaying',
    'aradio.textOnlyBody',
  ];
  for (const key of keys) {
    assert.notEqual(uiText('ko', key), uiText('en', key), `${key} must be translated`);
    assert.match(uiText('ko', key), /[가-힣]/, `${key} must emit Hangul`);
  }
  const html = mod.renderAradioRadio(viewState({ language: 'ko' }));
  for (const copy of ['이번 방송에서 다룬 이야기', '타이밍은 대략적입니다', '지금 읽는 줄로 돌아가기', '15초 뒤로', '15초 앞으로', '재생 속도 1×', 'RSS 복사', '다음 방송은 상황이 바뀌면 나갑니다.', 'Apple Podcasts에서 팔로우']) {
    assert.ok(html.includes(copy), `missing Korean copy: ${copy}`);
  }
});
