import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

// The view module is pure (no DOM) and imports i18n with an explicit .ts
// extension, so node's type stripping can load it directly.
const mod = await import('../src/render/aradio.ts');

const fixture = (path) =>
  JSON.parse(readFileSync(new URL(`./fixtures/aradio/${path}`, import.meta.url), 'utf8'));

const INDEX = fixture('index.json');
const STATE = fixture('state.json');
const B1450 = fixture('bulletins/2026-10-30/1450.json');
const B1250 = fixture('bulletins/2026-10-30/1250.json');
const LATEST_MS = Date.parse('2026-10-30T14:50:00Z');

function viewState(overrides = {}) {
  const index = mod.normalizeAradioIndex(INDEX);
  const board = mod.normalizeAradioBoard(STATE);
  const latestDetail = mod.normalizeAradioBulletin(B1450, index.bulletins[0]);
  return {
    language: 'en',
    nowMs: LATEST_MS + 20 * 60 * 1000,
    index,
    indexStatus: 'ok',
    board,
    boardStatus: 'ok',
    latestDetail,
    selectedId: index.bulletins[0].id,
    transcript: { kind: 'ready', bulletin: latestDetail },
    keepListening: false,
    showAll: false,
    checkedAt: LATEST_MS + 19 * 60 * 1000,
    ...overrides,
  };
}

test('index: newest first by aired_at, validated paths and audio, text-only kept', () => {
  const shuffled = { ...INDEX, bulletins: [INDEX.bulletins[2], INDEX.bulletins[0], INDEX.bulletins[1], INDEX.bulletins[0]] };
  const index = mod.normalizeAradioIndex(shuffled);
  assert.deepEqual(index.bulletins.map((entry) => entry.id), ['2026-10-30-1450', '2026-10-30-1250', '2026-10-30-1050']);
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
  assert.deepEqual(index.bulletins.map((entry) => entry.id), ['2026-10-30-1150', '2026-10-30-1050']);
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

  // A bulletin whose key fails the policy renders as text-only: no player.
  const index = mod.normalizeAradioIndex({
    bulletins: [{ id: '2026-10-30-1450', aired_at: '2026-10-30T14:50:00Z', headline: 'H', audio: { key: 'audio/aradio/../x.mp3' } }],
  });
  assert.equal(index.bulletins[0].audio, null);
  const { html } = mod.renderAradioView(viewState({ index, latestDetail: null, transcript: { kind: 'none' } }));
  assert.doesNotMatch(html, /data-aradio-play=/);
  assert.match(html, /Audio did not make it for this bulletin/);
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

test('ON AIR for two hours after the latest bulletin, then off air', () => {
  assert.deepEqual(mod.aradioAirState(null, LATEST_MS), { state: 'none', ageMs: null });
  assert.equal(mod.aradioAirState('2026-10-30T14:50:00Z', LATEST_MS + 119 * 60_000).state, 'live');
  assert.equal(mod.aradioAirState('2026-10-30T14:50:00Z', LATEST_MS + 120 * 60_000).state, 'idle');
  // A viewer clock behind the writer's still reads as live, never negative.
  assert.deepEqual(mod.aradioAirState('2026-10-30T14:50:00Z', LATEST_MS - 60_000), { state: 'live', ageMs: 0 });

  const live = mod.renderAradioView(viewState()).html;
  assert.match(live, /aradio-hero--live/);
  assert.match(live, /On air/);
  assert.match(live, /aired 20m ago/);
  const idle = mod.renderAradioView(viewState({ nowMs: LATEST_MS + 3 * 3600_000 })).html;
  assert.match(idle, /aradio-hero--idle/);
  assert.match(idle, /Last bulletin 3h ago/);
});

test('before the first run: empty state, no board or log, never a crash', () => {
  const html = mod.renderAradioView(viewState({
    index: null, indexStatus: 'missing', board: null, boardStatus: 'missing',
    latestDetail: null, selectedId: null, transcript: { kind: 'none' }, checkedAt: null,
  })).html;
  assert.match(html, /The first bulletin has not aired yet/);
  assert.match(html, /href="\/today"/);
  assert.match(html, /Checks for new bulletins every 5 minutes/);
  assert.doesNotMatch(html, /aradio-board|aradio-bulletins/);
  // Reserved slot for the "new bulletin" chip exists even when empty.
  assert.match(html, /data-aradio-apply hidden/);

  const failed = mod.renderAradioView(viewState({
    index: null, indexStatus: 'error', board: null, boardStatus: 'error',
    latestDetail: null, selectedId: null, transcript: { kind: 'none' }, checkedAt: null,
  })).html;
  assert.match(failed, /Could not reach the station/);
  assert.match(failed, /data-retry/);
});

test('board without bulletins (first run went off air) still renders the board', () => {
  const html = mod.renderAradioView(viewState({
    index: { updatedAt: null, degraded: false, bulletins: [] }, latestDetail: null, selectedId: null, transcript: { kind: 'none' },
  })).html;
  assert.match(html, /The first bulletin has not aired yet/);
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

test('transcript: speaker roles, follow-along spans, covers link only to live board slugs', () => {
  const bulletin = mod.normalizeAradioBulletin(B1450);
  const { html, links } = mod.renderAradioTranscript(
    { kind: 'ready', bulletin },
    { language: 'en', boardSlugs: new Set(['hbm-supply-crunch', 'anthropic-ipo']) },
  );
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
  const entry = { id: '2026-10-30-0950', airedAt: '2026-10-30T09:50:00.000Z', headline: 'From the index' };
  const bulletin = mod.normalizeAradioBulletin({
    script: ['Speaker 1: [high_energy] Hello [emphasis]there[/emphasis].', 'Speaker 2: Hi.', 'not a line'],
  }, entry);
  assert.equal(bulletin.id, entry.id);
  assert.equal(bulletin.headline, 'From the index');
  assert.deepEqual(bulletin.lines, [
    { speaker: 'Speaker 1', text: 'Hello there.' },
    { speaker: 'Speaker 2', text: 'Hi.' },
  ]);
  assert.equal(mod.normalizeAradioBulletin('nope'), null);
});

test('keep listening: queued new bulletins first, then earlier ones, skipping text-only and heard', () => {
  const bulletins = [
    { id: 'n2', audio: { key: 'audio/aradio/n2.mp3' } },
    { id: 'n1', audio: { key: 'audio/aradio/n1.mp3' } },
    { id: 'b1', audio: { key: 'audio/aradio/b1.mp3' } },
    { id: 'b2', audio: null },
    { id: 'b3', audio: { key: 'audio/aradio/b3.mp3' } },
  ];
  const heard = new Set(['b1']);
  assert.deepEqual(
    mod.pickNextAradioBulletin(bulletins, { heard, queue: ['n1', 'n2'], backCursor: 'b1' }),
    { id: 'n1', queue: ['n2'], backCursor: 'b1' },
  );
  // Queue drained: walk back from the cursor, skipping the text-only b2.
  assert.deepEqual(
    mod.pickNextAradioBulletin(bulletins, { heard: new Set(['b1', 'n1', 'n2']), queue: [], backCursor: 'b1' }),
    { id: 'b3', queue: [], backCursor: 'b3' },
  );
  assert.equal(mod.pickNextAradioBulletin(bulletins, { heard, queue: [], backCursor: 'b3' }), null);
  // A cursor that aged out of the index means nothing older is left.
  assert.equal(mod.pickNextAradioBulletin(bulletins, { heard, queue: [], backCursor: 'gone' }), null);
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

test('Korean: chrome, statuses, kinds and speakers are localized', () => {
  const { html, links } = mod.renderAradioView(viewState({ language: 'ko' }));
  for (const copy of ['상황판', '방송 중', '확대 중', '전개 중', '대본', '앵커', '공동 진행자', '계속 듣기']) {
    assert.ok(html.includes(copy), `missing Korean copy: ${copy}`);
  }
  assert.ok(links.some((link) => link.kindLabel === '실적 발표 콜'), 'evidence kinds are localized too');
  assert.doesNotMatch(html, />Situation board</);
});
