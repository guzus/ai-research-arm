import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const dashboardRoot = new URL('../', import.meta.url);

test('Korean locale loads and selects Pretendard through shared typography tokens', async () => {
  const [html, css, main] = await Promise.all([
    readFile(new URL('index.html', dashboardRoot), 'utf8'),
    readFile(new URL('src/style.css', dashboardRoot), 'utf8'),
    readFile(new URL('src/main.ts', dashboardRoot), 'utf8'),
  ]);

  assert.match(html, /pretendardvariable-dynamic-subset\.css/);
  assert.match(css, /--font-korean:\s*'Pretendard Variable'/);
  assert.match(css, /:root:lang\(ko\)\s*\{[^}]*--font-serif:\s*var\(--font-korean\)/s);
  assert.match(css, /:root:lang\(ko\)\s*\{[^}]*--reading-font-family:\s*var\(--font-korean\)/s);
  assert.match(main, /document\.documentElement\.lang\s*=\s*activeLanguage/);
});
