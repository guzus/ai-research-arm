import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

// The view module is pure (no DOM) and imports i18n with an explicit .ts
// extension, so node's type stripping can load it directly.
const mod = await import('../src/render/aradio.ts');
const { uiText } = await import('../src/i18n.ts');

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
  // Same hooks in the same order: main.ts patches text in place.
  assert.equal(shape(playing), shape(off));
  assert.equal(shape(waiting), shape(off));
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
  const spans = mod.aradioLineSpans(bulletin.lines);
  assert.equal(spans[0][0], 0);
  assert.ok(Math.abs(spans[spans.length - 1][1] - 1) < 1e-12);
  for (let i = 1; i < spans.length; i += 1) assert.equal(spans[i][0], spans[i - 1][1]);
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
  ];
  for (const key of keys) {
    assert.notEqual(uiText('ko', key), uiText('en', key), `${key} must be translated`);
    assert.match(uiText('ko', key), /[가-힣]/, `${key} must emit Hangul`);
  }
});
