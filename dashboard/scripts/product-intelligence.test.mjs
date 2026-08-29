import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const root = join(import.meta.dirname, '..');

async function importTs(relativePath) {
  return import(new URL(`../${relativePath}`, import.meta.url));
}

test('watchlists are account-free, normalized, bounded, and shareable', async () => {
  const mod = await importTs('src/product-intelligence.ts');
  const memory = new Map();
  const storage = { getItem: (key) => memory.get(key) ?? null, setItem: (key, value) => memory.set(key, value) };
  mod.writeWatchlist({ topics: ['Anthropic', 'anthropic', 'GPU Compute'] }, storage);
  assert.deepEqual(mod.readWatchlist(storage).topics, ['anthropic', 'gpu-compute']);
  assert.equal(mod.watchlistSharePath(['anthropic', 'gpu-compute'], '/wiki/anthropic', 'ko'), '/wiki/anthropic?watch=anthropic%2Cgpu-compute&lang=ko');
  assert.deepEqual(mod.watchlistFromUrl('?watch=Anthropic,gpu%20compute'), ['anthropic', 'gpu-compute']);
});

test('evidence search applies trust and language filters before ranking', async () => {
  const mod = await importTs('src/product-intelligence.ts');
  const entries = [
    { id: 'c1', type: 'claim', title: 'Anthropic revenue', body: 'Primary filing evidence', url: '/', confidence: 'high', sourceTier: 'primary', language: 'en', reusable: true },
    { id: 'c2', type: 'claim', title: 'Anthropic rumor', body: 'Secondary report', url: '/', confidence: 'low', sourceTier: 'secondary', language: 'en', reusable: false, reuse_block: 'time-sensitive' },
    { id: 'w1', type: 'wiki', title: '앤스로픽', body: '회사 지식', url: '/', language: 'ko' },
  ];
  assert.deepEqual(mod.searchEvidence(entries, 'anthropic', { confidence: 'high', sourceTier: 'primary' }).map((row) => row.id), ['c1']);
  assert.deepEqual(mod.searchEvidence(entries, '', { language: 'ko' }).map((row) => row.id), ['w1']);
  const equivalent = [
    { id: 'blocked', type: 'claim', title: 'Same evidence', body: 'same body', url: '/', confidence: 'high', reusable: false },
    { id: 'reusable', type: 'claim', title: 'Same evidence', body: 'same body', url: '/', confidence: 'high', reusable: true },
  ];
  assert.deepEqual(mod.searchEvidence(equivalent, 'evidence', {}).map((row) => row.id), ['reusable', 'blocked']);
});

test('evidence labels localize stable enums without changing raw semantics', async () => {
  const mod = await importTs('src/product-intelligence.ts');
  assert.equal(mod.evidenceEnumLabel('context', 'en'), 'Context');
  assert.equal(mod.evidenceEnumLabel('context', 'ko'), '맥락');
  assert.equal(mod.evidenceEnumLabel('high', 'ko'), '높음');
  assert.equal(mod.evidenceEnumLabel('single-source', 'en'), 'Single source');
  assert.equal(mod.evidenceEnumLabel('single-source', 'ko'), '단일 출처');
});

test('What changed DOM exposes reasoning, freshness, honest local highlights, and a site-wide feed', async () => {
  globalThis.location = new URL('https://ara.guzus.xyz/');
  const mod = await importTs('src/render/product.ts');
  const html = mod.renderWhatChanged([{
    id: 'x', kind: 'digest', title: 'Model release', summary: 'A concise summary', why: 'It changes cost.', watch: 'Verify adoption.', confidence: 'high', freshness: '2026-08-29', href: '/today/2026-08-29', topics: ['anthropic'], changedAt: '2026-08-29T00:00:00Z',
  }], { topics: ['anthropic'] }, 'en');
  assert.match(html, /What changed\?/);
  assert.match(html, /Why it matters/);
  assert.match(html, /Watch next/);
  assert.doesNotMatch(html, /Since your last visit/);
  assert.match(html, /only highlight matching cards on this device/);
  assert.match(html, /Site-wide feed/);
  assert.match(html, /href="\/feed\.xml"/);
  assert.match(html, /data-watch-topic="anthropic"/);
  const degraded = mod.renderWhatChanged([], { topics: [] }, 'en', true);
  assert.match(degraded, /Degraded mode/);
  assert.match(degraded, /not an editorial ranking/);
  const nav = readFileSync(join(root, 'index.html'), 'utf8');
  assert.equal((nav.match(/class="tab"/g) || []).length, 6);
});

test('prebuild search contract preserves claim reuse metadata and refuses unresolved article routes', () => {
  const source = readFileSync(join(root, 'scripts/prebuild.mjs'), 'utf8');
  assert.match(source, /if \(!articleSlug\) continue/);
  assert.match(source, /reusable: claim\.reusable/);
  assert.match(source, /reuse_block: claim\.reuse_block/);
  assert.doesNotMatch(source, /articleSlugByStem\.get\(claim\.article\) \|\| ''/);
});

test('runtime global search uses the shared evidence ranker and renders reuse warnings', () => {
  const source = readFileSync(join(root, 'src/main.ts'), 'utf8');
  assert.match(source, /const rankedEvidence = searchEvidence\(/);
  assert.match(source, /evidence-search\.json`, \{ cache: 'no-cache'/);
  assert.match(source, /Keep language variants as separate evidence records/);
  assert.match(source, /Reverify live/);
  assert.match(source, /실시간 재검증 필요/);
});

test('digest cards do not infer confidence from URL count', () => {
  const source = readFileSync(join(root, 'src/main.ts'), 'utf8');
  assert.match(source, /A link count describes sourcing volume, not corroboration quality/);
  assert.doesNotMatch(source, /sourceCount >= 3 \? 'high'/);
});

test('reader evidence explicitly denies independent-truth status and shows reverify warnings', async () => {
  globalThis.location = new URL('https://ara.guzus.xyz/');
  const mod = await importTs('src/render/product.ts');
  const html = mod.renderEvidenceDrawer([{ article: 'a', article_title: 'A', key: 'a#1', claim: 'A claim', type: 'metric', confidence: 'medium', risk: 'single-source', as_of: '2026-08-01', reusable: false, reuse_block: 'single-source', source_tiers: ['primary'], source_urls: ['https://example.com'] }], { language: 'en' });
  assert.match(html, /never an independent source of truth/);
  assert.match(html, /Reverify live/);
  assert.match(html, /As of 2026-08-01/);
  assert.match(html, /target="_blank" rel="noopener noreferrer"/);
  assert.match(html, />Medium</);
  assert.match(html, /Risk: Single source/);
  assert.match(html, /Reverify live · Single source/);
  const ko = mod.renderEvidenceDrawer([{ article: 'a', article_title: 'A', key: 'a#1', claim: 'A claim', type: 'metric', confidence: 'medium', risk: 'single-source', as_of: '2026-08-01', reusable: false, reuse_block: 'single-source', source_tiers: ['primary'], source_urls: ['https://example.com'] }], { language: 'ko' });
  assert.match(ko, />중간</);
  assert.match(ko, /위험: 단일 출처/);
  assert.match(ko, /실시간 재검증 필요 · 단일 출처/);
  assert.match(ko, />1차 출처</);
});

test('brief confidence labels are localized while raw values remain CSS semantics', async () => {
  globalThis.location = new URL('https://ara.guzus.xyz/');
  const mod = await importTs('src/render/product.ts');
  const item = { id: 'x', kind: 'digest', title: 'T', summary: 'S', why: 'W', watch: 'N', confidence: 'context', freshness: '2026-08-29', href: '/', topics: [], changedAt: '2026-08-29T00:00:00Z' };
  const en = mod.renderWhatChanged([item], { topics: [] }, 'en');
  const ko = mod.renderWhatChanged([item], { topics: [] }, 'ko');
  assert.match(en, /evidence-confidence--context">Confidence: Context/);
  assert.match(ko, /evidence-confidence--context">신뢰: 맥락/);
});

test('claim reuse projection fails closed on malformed canonical metadata', async () => {
  const mod = await import('./evidence-contract.mjs');
  assert.doesNotThrow(() => mod.assertClaimReuseContract({ article: 'a', key: 'a#ok', reusable: true }));
  assert.doesNotThrow(() => mod.assertClaimReuseContract({ article: 'a', key: 'a#blocked', reusable: false, reuse_block: 'single-source' }));
  assert.throws(() => mod.assertClaimReuseContract({ article: 'a', key: 'a#missing' }), /a#missing: reusable must be boolean/);
  assert.throws(() => mod.assertClaimReuseContract({ article: 'a', key: 'a#empty', reusable: false, reuse_block: '  ' }), /a#empty: reusable=false requires a non-empty reuse_block/);
  const source = readFileSync(join(root, 'scripts/prebuild.mjs'), 'utf8');
  assert.match(source, /if \(e instanceof EvidenceContractError\) throw e/);
});

test('product surfaces preserve loading/error paths and mobile containment', () => {
  const main = readFileSync(join(root, 'src/main.ts'), 'utf8');
  const css = readFileSync(join(root, 'src/style.css'), 'utf8');
  assert.match(main, /if \(pricing === 'timeout'\)/);
  assert.match(main, /showError\('Loading timed out'/);
  assert.match(main, /else \{\s*showEmpty\(dateStr\);/);
  assert.match(css, /@media \(max-width: 760px\)[\s\S]*\.change-grid[\s\S]*grid-template-columns: 1fr/);
  assert.match(css, /@media \(max-width: 420px\)[\s\S]*\.search-filters \{ grid-template-columns: 1fr/);
});
