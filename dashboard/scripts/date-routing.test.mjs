import test from 'node:test';
import assert from 'node:assert/strict';

import { resolvePublishedDate } from '../src/date-routing.ts';

test('Today uses the latest actual publication when the local day is ahead', () => {
  assert.equal(
    resolvePublishedDate(['2026-08-27', '2026-08-28', '2026-08-29'], '2026-08-30'),
    '2026-08-29',
  );
});

test('published dates remain stable and gaps resolve backward', () => {
  const dates = ['2026-08-29', '2026-08-27', '2026-08-29'];
  assert.equal(resolvePublishedDate(dates, '2026-08-29'), '2026-08-29');
  assert.equal(resolvePublishedDate(dates, '2026-08-28'), '2026-08-27');
});

test('requests before retained history have no truthful fallback', () => {
  assert.equal(resolvePublishedDate(['2026-08-28', '2026-08-29'], '2020-01-01'), null);
  assert.equal(resolvePublishedDate([], '2026-08-30'), null);
});
