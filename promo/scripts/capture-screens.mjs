// Refresh the live dashboard captures in public/screens/.
//
// OPTIONAL tool — the captures are committed, so the video renders without
// running this. Use it to re-shoot the dashboard when the UI changes.
//
// Prereq (kept out of the default install to stay lean):
//   npm i -D playwright && npx playwright install chromium
//   node scripts/capture-screens.mjs
//
// First principles: ara.guzus.xyz is a client-rendered Vite SPA — it hydrates
// after load and pulls fonts. A naive shot grabs a blank shell, so we wait for
// networkidle + an explicit settle and assert the DOM actually has text before
// shooting. Captured at DPR 1 / 1440px wide — already the size the BrowserFrame
// shows them at, so no post-resize step is needed.
import {chromium} from 'playwright';
import {mkdirSync, statSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname, join} from 'node:path';

const OUT = join(dirname(fileURLToPath(import.meta.url)), '..', 'public', 'screens');
mkdirSync(OUT, {recursive: true});

const BASE = 'https://ara.guzus.xyz';
const VW = 1440, VH = 900;

// name -> {path, mode}. 'full' = whole page (scrolled in the Product scene);
// 'clip' = top N px (for the very long Model Timeline ledger).
const ROUTES = [
  {name: 'today', path: '/', mode: 'full'},
  {name: 'models', path: '/models', mode: 'clip', clipH: 4000},
  {name: 'wiki', path: '/wiki', mode: 'full'},
  {name: 'research', path: '/research', mode: 'full'},
];

async function settle(page, label) {
  for (let i = 1; i <= 3; i++) {
    await page.waitForTimeout(i === 1 ? 2600 : 3200);
    const t = await page.evaluate(() => (document.body?.innerText || '').trim().length);
    console.log(`  [${label}] try ${i}: text=${t}`);
    if (t > 350) return true;
  }
  return false;
}

const browser = await chromium.launch();
const ctx = await browser.newContext({
  viewport: {width: VW, height: VH},
  deviceScaleFactor: 1,
  colorScheme: 'light',
});

for (const r of ROUTES) {
  const page = await ctx.newPage();
  const url = `${BASE}${r.path}`;
  console.log(`> ${r.name}  ${url}`);
  await page.goto(url, {waitUntil: 'networkidle', timeout: 45000}).catch(() => {});
  await settle(page, r.name);
  const out = join(OUT, `${r.name}.png`);
  if (r.mode === 'clip') {
    await page.screenshot({path: out, clip: {x: 0, y: 0, width: VW, height: r.clipH}});
  } else {
    await page.screenshot({path: out, fullPage: true});
  }
  console.log(`  saved ${r.name}.png (${(statSync(out).size / 1024).toFixed(0)}KB)`);
  await page.close();
}

await browser.close();
console.log('DONE — now run: node scripts/gen-screens.mjs');
