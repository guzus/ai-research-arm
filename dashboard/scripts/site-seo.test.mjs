import test from 'node:test';
import assert from 'node:assert/strict';

import {
  datedPagePolicy,
  datedRoute,
  isIsoCalendarDate,
  isIndexableResearchEntry,
  latestAliasPolicy,
  sortDatedRecords,
} from './site-seo.mjs';

test('dated public reports use stable self-canonical routes', () => {
  assert.deepEqual(
    datedPagePolicy('twitter', '2026-07-14', 'https://ara.guzus.xyz/'),
    {
      route: '/twitter/2026-07-14',
      canonicalRoute: '/twitter/2026-07-14',
      canonicalUrl: 'https://ara.guzus.xyz/twitter/2026-07-14',
      indexable: true,
    },
  );
});

test('research fixtures remain available without entering the search index', () => {
  assert.equal(isIndexableResearchEntry({ slug: 'useful', tags: ['ai'] }), true);
  assert.equal(isIndexableResearchEntry({ slug: 'seed', tags: ['fixture'] }), false);
  assert.equal(isIndexableResearchEntry({ slug: 'test-run', tags: ['test'] }), false);
  assert.equal(isIndexableResearchEntry({ slug: 'components', tags: ['reference'] }), false);
});

test('undated latest aliases canonicalize to the dated report and stay out of the index', () => {
  assert.deepEqual(
    latestAliasPolicy('today', '2026-07-15', 'https://ara.guzus.xyz'),
    {
      route: '/today',
      canonicalRoute: '/today/2026-07-15',
      canonicalUrl: 'https://ara.guzus.xyz/today/2026-07-15',
      indexable: false,
    },
  );
});

test('route inputs and dated ordering are deterministic', () => {
  assert.equal(datedRoute('frontpage', '2026-07-15'), '/frontpage/2026-07-15');
  assert.throws(() => datedRoute('agents', '2026-07-15'), /invalid dated section/);
  assert.throws(() => datedRoute('today', '../latest'), /invalid route date/);
  assert.equal(isIsoCalendarDate('2026-02-28'), true);
  assert.equal(isIsoCalendarDate('2026-02-29'), false);
  assert.equal(isIsoCalendarDate('2026-02-31'), false);
  assert.equal(isIsoCalendarDate('2026-99-99'), false);
  assert.deepEqual(
    sortDatedRecords([{ date: '2026-07-15' }, { date: 'bad' }, { date: '2026-07-13' }])
      .map(record => record.date),
    ['2026-07-13', '2026-07-15'],
  );
});
