import test from 'node:test';
import assert from 'node:assert/strict';

import { forecastRoute, forecastSeoRecord, mappedForecastTickets } from './forecast-seo.mjs';

const mapped = {
  slug: 'openai-ipo-2026-06',
  title: 'OpenAI IPO',
  company: 'OpenAI',
  status: 'confirmed',
  verification: 'confirmed',
  updated_at: '2026-07-11',
  polymarket: [{
    event_slug: 'openai-ipo-by',
    market_id: '123',
    token_id: '456',
    question: 'OpenAI IPO by December 31, 2026?',
  }],
};

test('only well-shaped mapped tickets receive forecast pages', () => {
  const rows = mappedForecastTickets({ tickets: [
    { ...mapped, slug: 'z-ticket' },
    { ...mapped, slug: 'a-ticket' },
    { ...mapped, slug: 'ordinary-ticket', polymarket: null },
    { ...mapped, slug: 'unverified-ticket', verification: 'partial' },
    { ...mapped, slug: 'broken-ticket', polymarket: [{ question: 'Missing IDs' }] },
    { ...mapped, slug: '../unsafe' },
  ] });
  assert.deepEqual(rows.map(row => row.slug), ['a-ticket', 'z-ticket']);
});

test('forecast metadata is deterministic and does not claim a live price', () => {
  const record = forecastSeoRecord(mapped, 'https://ara.guzus.xyz/');
  assert.equal(record.route, '/models/forecast/openai-ipo-2026-06');
  assert.equal(record.url, 'https://ara.guzus.xyz/models/forecast/openai-ipo-2026-06');
  assert.equal(record.title, 'OpenAI IPO forecast');
  assert.match(record.description, /Linked prediction market: OpenAI IPO by December 31, 2026\?/);
  assert.match(record.description, /Updated 2026-07-11/);
  assert.doesNotMatch(record.description, /\b\d+%|live odds/i);
  assert.doesNotMatch(record.description, /\?\./);
});

test('forecast routes reject unsafe slugs', () => {
  assert.throws(() => forecastRoute('../openai'), /invalid forecast slug/);
});
