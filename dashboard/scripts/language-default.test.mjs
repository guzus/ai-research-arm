import assert from 'node:assert/strict';
import test from 'node:test';

import { resolveUiLanguage } from '../src/i18n.ts';

test('an explicit saved language overrides browser preferences', () => {
  assert.equal(resolveUiLanguage('en', ['ko-KR']), 'en');
  assert.equal(resolveUiLanguage('ko', ['en-US']), 'ko');
});

test('a first-time Korean browser defaults to Korean', () => {
  assert.equal(resolveUiLanguage(null, ['ko-KR', 'en-US']), 'ko');
  assert.equal(resolveUiLanguage(null, ['ko_KR']), 'ko');
});

test('browser negotiation uses the first supported language', () => {
  assert.equal(resolveUiLanguage(null, ['ja-JP', 'ko-KR', 'en-US']), 'ko');
  assert.equal(resolveUiLanguage(null, ['en-US', 'ko-KR']), 'en');
  assert.equal(resolveUiLanguage(null, ['ja-JP']), 'en');
});
