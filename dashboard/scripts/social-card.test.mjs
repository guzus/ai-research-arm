import test from 'node:test';
import assert from 'node:assert/strict';
import {
  CARD_HEIGHT,
  CARD_WIDTH,
  escapeXml,
  estimateWidth,
  fitTitle,
  renderSocialCardPng,
  renderSocialCardSvg,
  wrapText,
} from './social-card.mjs';

test('escapeXml neutralizes markup-significant characters', () => {
  assert.equal(escapeXml(`<script>&"'`), '&lt;script&gt;&amp;&quot;&apos;');
});

test('wrapText keeps short text on one line and never exceeds maxLines', () => {
  assert.deepEqual(wrapText('Short title', 60, 1056, 3), ['Short title']);
  const long = 'word '.repeat(80).trim();
  const lines = wrapText(long, 60, 1056, 3);
  assert.equal(lines.length, 3);
  assert.ok(lines.at(-1).endsWith('…'), 'overflow is ellipsized');
});

test('wrapped lines respect the pixel budget', () => {
  const lines = wrapText(
    'Moonshot AI: the lab that traded its consumer app for the open-weights frontier',
    58, 1056, 4,
  );
  for (const line of lines) {
    assert.ok(estimateWidth(line, 58) <= 1056, `line overflows: ${line}`);
  }
});

test('fitTitle steps down for long titles and never returns zero lines', () => {
  const short = fitTitle('Kimi K3');
  const long = fitTitle(
    'Kimi K3: Moonshot’s 2.8T-parameter model, its LMArena Frontend Code #1, and what the win actually proves',
  );
  // Exact sizes depend on host font metrics (calibration); assert the
  // invariants instead: a short title gets the largest step, a long one
  // steps down or wraps to more lines, and lines are never empty.
  assert.equal(short.lines.length, 1);
  assert.ok(long.size <= short.size);
  assert.ok(long.lines.length > short.lines.length);
  assert.ok(long.lines.length >= 1);
});

test('renderSocialCardSvg embeds escaped content at card dimensions', () => {
  const svg = renderSocialCardSvg({
    eyebrow: 'Jul 17, 2026',
    title: 'A title with <angle> & "quotes"',
    description: 'Deck text',
    attribution: 'Research by claude-sonnet-5',
    domain: 'ara.guzus.xyz',
  });
  assert.ok(svg.includes(`width="${CARD_WIDTH}" height="${CARD_HEIGHT}"`));
  // Wrap position may split the phrase across <text> lines; assert each
  // escaped token independently and that nothing survives unescaped.
  assert.ok(svg.includes('&lt;angle&gt;'));
  assert.ok(svg.includes('&quot;quotes&quot;'));
  assert.ok(!svg.includes('<angle>'));
  assert.ok(svg.includes('JUL 17, 2026'));
  assert.ok(svg.includes('Research by claude-sonnet-5'));
  assert.ok(svg.includes('ara.guzus.xyz'));
});

test('renderSocialCardPng produces a 1200x630 PNG', async () => {
  const png = await renderSocialCardPng({
    eyebrow: 'Research',
    title: 'Smoke test article',
    description: 'One line of deck copy.',
  });
  // PNG signature, then IHDR width/height at fixed offsets.
  assert.deepEqual([...png.subarray(0, 8)], [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  assert.equal(png.readUInt32BE(16), CARD_WIDTH);
  assert.equal(png.readUInt32BE(20), CARD_HEIGHT);
});
