import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import {
  digestStaticSeoSemantics,
  editorialDigestDates,
  isDeterministicFallbackSource,
  isPublicUnavailableDigest,
  latestEditorialAliasPlan,
  latestEditorialRecord,
  unavailableDigestMarkdown,
} from './publication-contract.mjs';

const repoRoot = join(import.meta.dirname, '..', '..');

test('publication contract recognizes only the exact operational fallback banner', () => {
  const fallback = '# AI Daily Digest - 2026-08-30\n\n> **Deterministic fallback digest.** Source lanes were unavailable.';
  assert.equal(isDeterministicFallbackSource(fallback), true);
  assert.equal(isDeterministicFallbackSource('# Editorial\n\nWe audited scripts/deterministic_daily_digest.py.'), false);
  assert.equal(isDeterministicFallbackSource('# Editorial\n\nTop verbatim excerpt from each covered lane.'), false);
  assert.equal(isDeterministicFallbackSource(`${'\n'.repeat(10)}> **Deterministic fallback digest.**`), false);

  const classifier = join(repoRoot, 'scripts/digest_publication_state.py');
  const classify = input => spawnSync('python3', [classifier, '-'], { input, encoding: 'utf8' }).status === 0;
  assert.equal(classify(fallback), true);
  assert.equal(classify('# Editorial\n\n> Note: > **Deterministic fallback digest.** was retired'), false);
  assert.equal(classify(`${'\n'.repeat(10)}> **Deterministic fallback digest.**`), false);
});

test('recovered editorial digests are no longer treated as operational fallbacks', () => {
  const recovered = readFileSync(join(repoRoot, 'research/digest/2026-08-29-digest.md'), 'utf8');
  assert.equal(isDeterministicFallbackSource(recovered), false);

  const classifier = join(repoRoot, 'scripts/digest_publication_state.py');
  const classified = spawnSync('python3', [classifier, '-'], { input: recovered, encoding: 'utf8' });
  assert.equal(classified.status, 1);
});

test('public projection carries status only and never copies fallback source material', () => {
  const projected = unavailableDigestMarkdown('2026-08-29');
  assert.equal(isPublicUnavailableDigest(projected), true);
  assert.match(projected, /2026-08-29/);
  assert.doesNotMatch(projected, /Verbatim excerpts|research\/summaries|deterministic_daily_digest/i);
});

test('editorial manifest dates exclude unavailable projections and ignore input order', () => {
  const byDate = new Map([
    ['2026-08-28', unavailableDigestMarkdown('2026-08-28')],
    ['2026-08-27', '# AI Daily Digest — 2026-08-27\n\nEditorial brief.'],
    ['2026-08-29', '# AI Daily Digest — 2026-08-29\n\nEditorial brief.'],
  ]);
  assert.deepEqual(
    editorialDigestDates(['2026-08-29', '2026-08-28', '2026-08-27', '2026-08-29'], date => byDate.get(date)),
    ['2026-08-27', '2026-08-29'],
  );
});

test('static Today alias selects the latest editorial record, not the newest unavailable file', () => {
  assert.deepEqual(
    latestEditorialRecord([
      { date: '2026-08-30', unavailable: true },
      { date: '2026-08-27', unavailable: false },
      { date: '2026-08-29', unavailable: false },
    ]),
    { date: '2026-08-29', unavailable: false },
  );
});

test('static Today alias fails closed when every routable digest is unavailable', () => {
  assert.deepEqual(
    latestEditorialAliasPlan([
      { date: '2026-08-29', unavailable: true },
      { date: '2026-08-30', unavailable: true },
    ]),
    { kind: 'empty' },
  );
});

test('static dated digest metadata distinguishes diagnostic pages from editorial articles', () => {
  assert.deepEqual(digestStaticSeoSemantics('2026-08-30', true), {
    ogType: 'website',
    articlePublishedTime: null,
  });
  assert.deepEqual(digestStaticSeoSemantics('2026-08-29', false), {
    ogType: 'article',
    articlePublishedTime: '2026-08-29',
  });
});

test('historical audio cleanup derives only the seven exact fallback-date keys', () => {
  const cleanup = spawnSync('bash', [join(repoRoot, 'scripts/delete_fallback_audio.sh')], {
    cwd: repoRoot,
    env: { ...process.env, FALLBACK_AUDIO_DRY_RUN: '1' },
    encoding: 'utf8',
  });
  assert.equal(cleanup.status, 0, cleanup.stderr);
  const keys = [...cleanup.stdout.matchAll(/Fallback audio candidate: (.+)/g)].map(match => match[1]);
  assert.deepEqual(keys, [
    'audio/2026-07-07-digest.mp3',
    'audio/2026-08-08-digest.mp3',
    'audio/2026-08-09-digest.mp3',
    'audio/2026-08-10-digest.mp3',
    'audio/2026-08-17-digest.mp3',
    'audio/2026-08-28-digest.mp3',
    'audio/2026-08-30-digest.mp3',
  ]);
});

test('workflows suppress fallback-derived front pages, notifications, and audio', () => {
  const digestWorkflow = readFileSync(join(repoRoot, '.github/workflows/daily-digest.yml'), 'utf8');
  const frontPageWorkflow = readFileSync(join(repoRoot, '.github/workflows/daily-front-page.yml'), 'utf8');
  const wikiWorkflow = readFileSync(join(repoRoot, '.github/workflows/wiki-ingest.yml'), 'utf8');
  const cleanupWorkflow = readFileSync(join(repoRoot, '.github/workflows/cleanup-fallback-publications.yml'), 'utf8');
  assert.match(digestWorkflow, /id: digest-publication[\s\S]*editorial=false/);
  for (const step of ['Rewrite summary', 'Generate audio digest', 'Upload audio digest', 'Send Telegram notification', 'Send audio to Hooker', 'Truncate audio', 'Push audio stub']) {
    const start = digestWorkflow.indexOf(`- name: ${step}`);
    assert.notEqual(start, -1, `${step} step exists`);
    assert.match(digestWorkflow.slice(start, start + 220), /digest-publication\.outputs\.editorial == 'true'/, `${step} is editorial-only`);
  }
  assert.match(frontPageWorkflow, /publishable=false/);
  assert.doesNotMatch(frontPageWorkflow, /if: steps\.check\.outputs\.exists == 'true'/);
  assert.match(wikiWorkflow, /id: digest-publication[\s\S]*Operational fallback found; skipping wiki ingest/);
  assert.match(wikiWorkflow, /name: Ingest digest into wiki[\s\S]{0,180}digest-publication\.outputs\.editorial == 'true'/);
  assert.match(digestWorkflow, /name: Revoke fallback audio objects from S3[\s\S]{0,1000}delete_fallback_audio\.sh/);
  assert.match(cleanupWorkflow, /workflow_dispatch:[\s\S]*delete_fallback_audio\.sh/);
});
