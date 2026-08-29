import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

import { createServer } from 'vite';

import { uiText } from '../src/i18n.ts';

const dashboardRoot = new URL('../', import.meta.url);

const PRIMARY_TAB_KEYS = [
  'nav.twitter',
  'nav.models',
  'nav.research',
  'nav.wiki',
  'nav.pricing',
  'nav.agents',
];

test('every primary navigation tab declares and renders distinct Korean copy', async () => {
  const html = await readFile(new URL('index.html', dashboardRoot), 'utf8');
  const declaredKeys = Array.from(
    html.matchAll(/<a\b[^>]*class="tab"[^>]*data-i18n="([^"]+)"[^>]*>/g),
    (match) => match[1],
  );

  assert.deepEqual(declaredKeys, PRIMARY_TAB_KEYS);
  for (const key of PRIMARY_TAB_KEYS) {
    const english = uiText('en', key);
    const korean = uiText('ko', key);
    assert.notEqual(korean, english, `${key} must not fall back to English`);
    assert.match(korean, /[가-힣]/, `${key} must contain user-visible Korean copy`);
  }
});

test('index-driven tabs have Korean empty, filter, and action-state contracts', () => {
  const requiredCopy = {
    research: ['research.noMatches', 'research.allArticles', 'research.savePdf'],
    wiki: ['wiki.noPages', 'wiki.noMatches', 'wiki.backlinks', 'wiki.history'],
    models: ['models.allCompanies', 'models.noTickets', 'models.noMatches', 'models.history'],
  };

  for (const [tab, keys] of Object.entries(requiredCopy)) {
    for (const key of keys) {
      const english = uiText('en', key);
      const korean = uiText('ko', key);
      assert.notEqual(korean, english, `${tab} UI key ${key} must be translated`);
      assert.match(korean, /[가-힣]/, `${tab} UI key ${key} must emit Korean`);
    }
  }
});

test('standalone tab renderers accept Korean and emit localized UI chrome', async (t) => {
  const previousDocument = globalThis.document;
  globalThis.document = {
    createElement() {
      let text = '';
      return {
        set textContent(value) { text = String(value); },
        get innerHTML() {
          return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
        },
      };
    },
  };
  t.after(() => {
    if (previousDocument === undefined) delete globalThis.document;
    else globalThis.document = previousDocument;
  });

  const vite = await createServer({
    root: dashboardRoot.pathname,
    configFile: false,
    appType: 'custom',
    logLevel: 'silent',
    server: { middlewareMode: true },
  });
  t.after(() => vite.close());

  const [today, twitter, pricing, agents] = await Promise.all([
    vite.ssrLoadModule('/src/render/today.ts'),
    vite.ssrLoadModule('/src/render/twitter.ts'),
    vite.ssrLoadModule('/src/render/pricing.ts'),
    vite.ssrLoadModule('/src/render/agents.ts'),
  ]);

  const todayHtml = today.renderTodayHtml({
    md: '## Executive Summary\n\n- A concise editorial fixture.',
    dateStr: '2026-08-13',
    fallbackTitle: '2026-08-13',
    audioDates: ['2026-08-13'],
    searchTerm: '',
    frontPageCardHtml: null,
    language: 'ko',
  });
  assert.match(todayHtml, />다이제스트 오디오 재생</);

  const fallbackHtml = today.renderTodayHtml({
    md: '<!-- ara-publication-state: unavailable -->\n# AI Daily Digest — 2026-08-30',
    dateStr: '2026-08-30',
    fallbackTitle: '2026-08-30',
    audioDates: ['2026-08-30'],
    searchTerm: '',
    frontPageCardHtml: '<div>unreviewed front page</div>',
    language: 'ko',
  });
  assert.match(fallbackHtml, /2026-08-30에는 편집 브리프가 게시되지 않았습니다/);
  assert.doesNotMatch(fallbackHtml, /Verbatim excerpts|research\/|unreviewed source dump|unreviewed front page|다이제스트 오디오 재생|저하 모드/i);

  const twitterHtml = twitter.renderTwitterReportHtml(
    '## 16:00 UTC\n\n**Cycle summary**: A concise editorial fixture.',
    {
      language: 'ko',
      fallbackDate: null,
      currentDateStr: '2026-08-13',
      currentDateTitle: '2026-08-13',
      shownDateTitle: '2026-08-13',
      prevDate: '2026-08-12',
      nextDate: '2026-08-14',
      searchTerm: '',
      parseUtcTime: () => null,
      clockIcon: () => '',
      twitterMarkdownToHtml: (markdown) => markdown,
      renderSourceChips: () => '',
      renderHandleChips: () => '',
    },
  );
  assert.match(twitterHtml, />이전 날</);
  assert.match(twitterHtml, />트위터 요약</);
  assert.match(twitterHtml, />다음 날</);
  assert.match(twitterHtml, />타임라인</);

  const pricingHtml = pricing.renderPricing({
    generated_at: new Date().toISOString(),
    benchmark: 'FixtureBench',
    snapshot: {
      as_of: '2026-08-13',
      models: [{
        key: 'fixture/model',
        name: 'Fixture Model',
        vendor: 'fixture',
        input_usd_per_mtok: 1,
        output_usd_per_mtok: 2,
        score: 50,
        pareto: true,
      }],
      counts: { priced: 1 },
    },
  }, undefined, 'ko');
  assert.match(pricingHtml, />가격 대비 성능</);
  assert.ok(pricingHtml.includes(uiText('ko', 'pricing.frontier')));
  assert.match(pricingHtml, /마지막 동기화/);

  const agentsHtml = agents.renderAgentsStudioHtml('ko');
  assert.ok(agentsHtml.includes(uiText('ko', 'agents.title')));
  assert.ok(agentsHtml.includes(uiText('ko', 'agents.loading')));
});
