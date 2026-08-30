import test from 'node:test';
import assert from 'node:assert/strict';

import {
  editorialDatesFromManifest,
  isExplicitUnavailableTodayDate,
  latestPublishedDate,
  resolvePublishedDate,
  resolveTodayEntryPlan,
  transitionRootRoute,
  unavailableTodayRoutePolicy,
} from '../src/date-routing.ts';
import { uiText } from '../src/i18n.ts';

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

test('root and Today alias select the latest editorial date without trusting manifest order or local day', () => {
  const editorial = ['2026-08-27', 'invalid', '2026-08-29', '2026-08-28', '2026-02-30'];
  assert.equal(latestPublishedDate(editorial), '2026-08-29');
  assert.deepEqual(resolveTodayEntryPlan(editorial, '2026-08-30', true), {
    kind: 'editorial',
    date: '2026-08-29',
  });
});

test('explicit dated deep links retain their requested publication contract', () => {
  const editorial = ['2026-08-27', '2026-08-29'];
  assert.deepEqual(resolveTodayEntryPlan(editorial, '2026-08-28', false), {
    kind: 'explicit',
    date: '2026-08-28',
  });
  assert.deepEqual(resolveTodayEntryPlan(editorial, '2026-08-30', false), {
    kind: 'explicit',
    date: '2026-08-30',
  });
});

test('root route identity survives rerenders, clears for explicit dates, and restores on Back', () => {
  let rootActive = false;
  rootActive = transitionRootRoute(rootActive, 'enter-home');
  rootActive = transitionRootRoute(rootActive, 'rerender'); // language switch
  rootActive = transitionRootRoute(rootActive, 'rerender'); // refresh button
  assert.equal(rootActive, true);
  rootActive = transitionRootRoute(rootActive, 'enter-other'); // calendar date
  assert.equal(rootActive, false);
  rootActive = transitionRootRoute(rootActive, 'enter-home'); // popstate back to /
  assert.equal(rootActive, true);
});

test('legacy manifests fail closed instead of treating newest routable Today file as editorial', () => {
  const legacyManifest = {
    today: ['2026-08-29', '2026-08-30'], // newest file is an unavailable projection
  };
  const editorial = editorialDatesFromManifest(legacyManifest.todayEditorial);
  assert.deepEqual(editorial, []);
  assert.deepEqual(resolveTodayEntryPlan(editorial, '2026-08-30', true), { kind: 'empty' });
});

test('explicit routable non-editorial Today dates use the unavailable publication contract', () => {
  const today = ['2026-08-29', '2026-08-30'];
  const editorial = ['2026-08-29'];
  assert.equal(isExplicitUnavailableTodayDate(today, editorial, '2026-08-30', false), true);
  assert.equal(isExplicitUnavailableTodayDate(today, editorial, '2026-08-29', false), false);
  assert.equal(isExplicitUnavailableTodayDate(today, editorial, '2026-08-30', true), false);
  assert.equal(isExplicitUnavailableTodayDate(today, editorial, '2026-08-31', false), false);
  assert.deepEqual(unavailableTodayRoutePolicy('2026-08-30'), {
    canonicalPath: '/today/2026-08-30',
    indexable: false,
    type: 'website',
  });
  assert.equal(uiText('en', 'today.unavailableTitle', { date: '2026-08-30' }), 'No editorial brief was published for 2026-08-30');
  assert.equal(uiText('ko', 'today.unavailableTitle', { date: '2026-08-30' }), '2026-08-30에는 편집 브리프가 게시되지 않았습니다');
  assert.match(uiText('en', 'today.unavailableBody'), /not published as editorial content/);
  assert.match(uiText('ko', 'today.unavailableBody'), /편집 콘텐츠로 공개하지 않습니다/);
});
