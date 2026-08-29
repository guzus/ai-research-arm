import { evidenceEnumLabel } from '../product-intelligence.ts';
import type { PublicClaim, WatchlistState } from '../product-intelligence.ts';

function esc(value: unknown): string {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[char] || char));
}

function safeUrl(value: string): string {
  try {
    const origin = typeof location === 'undefined' ? 'https://ara.guzus.xyz' : location.origin;
    const url = new URL(value, origin);
    return ['http:', 'https:'].includes(url.protocol) ? esc(url.href) : '#';
  } catch {
    return '#';
  }
}

export type BriefItem = {
  id: string;
  kind: 'digest' | 'model' | 'wiki' | 'pricing' | 'gpu';
  title: string;
  summary: string;
  why: string;
  watch: string;
  confidence: 'high' | 'medium' | 'context';
  freshness: string;
  href: string;
  topics: string[];
  changedAt: string;
};

const KIND_LABEL: Record<BriefItem['kind'], { en: string; ko: string }> = {
  digest: { en: 'Daily synthesis', ko: '일일 종합' },
  model: { en: 'Model tracker', ko: '모델 트래커' },
  wiki: { en: 'Knowledge update', ko: '지식 업데이트' },
  pricing: { en: 'Capability economics', ko: '성능 경제성' },
  gpu: { en: 'Compute market', ko: '컴퓨트 시장' },
};

export function renderWhatChanged(items: BriefItem[], watchlist: WatchlistState, language: 'en' | 'ko'): string {
  const ko = language === 'ko';
  const watched = new Set(watchlist.topics);
  const rows = items.map((item) => {
    const isWatched = item.topics.some((topic) => watched.has(topic));
    return [
      `<article class="change-card${isWatched ? ' is-watched' : ''}">`,
      '  <div class="change-card-meta">',
      `    <span class="change-kind change-kind--${item.kind}">${esc(KIND_LABEL[item.kind][language])}</span>`,
      `    <span class="change-freshness">${esc(item.freshness)}</span>`,
      '  </div>',
      `  <h3><a href="${esc(item.href)}">${esc(item.title)}</a></h3>`,
      `  <p class="change-summary">${esc(item.summary)}</p>`,
      '  <dl class="change-reasoning">',
      `    <div><dt>${ko ? '중요한 이유' : 'Why it matters'}</dt><dd>${esc(item.why)}</dd></div>`,
      `    <div><dt>${ko ? '다음 확인' : 'Watch next'}</dt><dd>${esc(item.watch)}</dd></div>`,
      '  </dl>',
      '  <div class="change-card-foot">',
      `    <span class="evidence-confidence evidence-confidence--${item.confidence}">${ko ? '신뢰' : 'Confidence'}: ${esc(evidenceEnumLabel(item.confidence, language))}</span>`,
      item.topics.slice(0, 3).map((topic) => `<button class="watch-chip${watched.has(topic) ? ' is-active' : ''}" type="button" data-watch-topic="${esc(topic)}" aria-pressed="${watched.has(topic)}">${watched.has(topic) ? '★' : '+'} ${esc(topic.replace(/-/g, ' '))}</button>`).join(''),
      '  </div>',
      '</article>',
    ].filter(Boolean).join('\n');
  }).join('\n');
  return [
    '<section class="what-changed" aria-labelledby="whatChangedTitle">',
    '  <header class="what-changed-head">',
    `    <div><span class="ara-eyebrow">${ko ? '의사결정 브리프' : 'Decision brief'}</span><h2 id="whatChangedTitle">${ko ? '무엇이 바뀌었나' : 'What changed?'}</h2></div>`,
    `    <div class="watchlist-actions"><a href="/feed.xml" class="watchlist-rss">${ko ? '사이트 전체 피드' : 'Site-wide feed'}</a><button type="button" data-share-watchlist>${ko ? '관심 표시 공유' : 'Share highlights'}</button></div>`,
    '  </header>',
    watchlist.topics.length ? `<p class="watchlist-summary">${ko ? '이 기기에서 강조 표시' : 'Highlighted on this device'}: ${esc(watchlist.topics.join(', ').replace(/-/g, ' '))}</p>` : '',
    `<p class="watchlist-note">${ko ? '관심 주제는 이 기기에서 일치하는 카드를 강조할 뿐이며, 구독이나 개인 맞춤 순위가 아닙니다. 피드는 사이트 전체 내용을 제공합니다.' : 'Watched topics only highlight matching cards on this device; they do not subscribe you or personalize ranking. The feed is site-wide.'}</p>`,
    `  <div class="change-grid">${rows}</div>`,
    '</section>',
  ].filter(Boolean).join('\n');
}

export function renderEvidenceDrawer(claims: PublicClaim[], options: { language: 'en' | 'ko'; fallbackStatus?: string; title?: string }): string {
  const ko = options.language === 'ko';
  const reusable = claims.filter((claim) => claim.reusable).length;
  const sources = new Set(claims.flatMap((claim) => claim.source_urls)).size;
  const rows = claims.slice().sort((a, b) => (b.as_of || '').localeCompare(a.as_of || '') || a.key.localeCompare(b.key)).map((claim) => [
    '<li class="evidence-claim">',
    `  <p>${esc(claim.claim)}</p>`,
    '  <div class="evidence-claim-meta">',
    `    <span class="evidence-confidence evidence-confidence--${esc(claim.confidence)}">${esc(evidenceEnumLabel(claim.confidence, options.language))}</span>`,
    claim.as_of ? `    <span>${ko ? '기준일' : 'As of'} ${esc(claim.as_of)}</span>` : '',
    claim.risk ? `    <span>${ko ? '위험' : 'Risk'}: ${esc(evidenceEnumLabel(claim.risk, options.language))}</span>` : '',
    `    <span>${esc(claim.type)}</span>`,
    '  </div>',
    claim.reusable
      ? `  <div class="evidence-reuse is-reusable">${ko ? '다시 인용 가능한 안정적 근거' : 'Reusable evidence metadata; verify the linked source when stakes are high.'}</div>`
      : `  <div class="evidence-reuse is-blocked">${ko ? '실시간 재검증 필요' : 'Reverify live'}${claim.reuse_block ? ` · ${esc(evidenceEnumLabel(claim.reuse_block, options.language))}` : ''}</div>`,
    claim.source_tiers.length ? `  <div class="evidence-tier-list">${claim.source_tiers.map((tier) => `<span>${esc(evidenceEnumLabel(tier, options.language))}</span>`).join('')}</div>` : '',
    '  <div class="evidence-sources">' + claim.source_urls.slice(0, 4).map((url, index) =>
      `<a href="${safeUrl(url)}" target="_blank" rel="noopener noreferrer">${esc((() => { try { return new URL(url).hostname; } catch { return claim.hosts?.[index] || `source ${index + 1}`; } })())}</a>`
    ).join('') + '</div>',
    '</li>',
  ].join('\n')).join('\n');
  return [
    '<details class="evidence-drawer">',
    `  <summary><span>${esc(options.title || (ko ? '근거 메타데이터' : 'Evidence metadata'))}</span><span>${claims.length} ${ko ? '개 주장' : 'claims'} · ${sources} ${ko ? '개 소스' : 'sources'}</span></summary>`,
    '  <div class="evidence-drawer-body">',
    `    <p class="evidence-contract">${ko ? '이 장부는 독립적인 출처가 아니라 검증 메타데이터입니다. 링크된 원문을 기준으로 판단하세요.' : 'This ledger is evidence metadata, never an independent source of truth. Follow the linked primary material before making a high-stakes decision.'}</p>`,
    `    <div class="evidence-summary"><span>${reusable} ${ko ? '재사용 가능' : 'reusable'}</span><span>${claims.length - reusable} ${ko ? '재검증 필요' : 'reverify live'}</span><span>${esc(options.fallbackStatus || (ko ? '정상 게시' : 'publication path not marked degraded'))}</span></div>`,
    rows ? `    <ol class="evidence-list">${rows}</ol>` : `    <p class="evidence-empty">${ko ? '구조화된 주장 장부가 없습니다. 본문의 원문 링크를 확인하세요.' : 'No structured claim ledger is available for this item. Use the inline source links.'}</p>`,
    '  </div>',
    '</details>',
  ].join('\n');
}

export function renderDossierRelated(options: {
  slug: string;
  language: 'en' | 'ko';
  research: Array<{ slug: string; title: string; created_at: string }>;
  tickets: Array<{ slug: string; title: string; status: string; updated_at: string }>;
  claims: PublicClaim[];
  watchlisted: boolean;
}): string {
  const ko = options.language === 'ko';
  const research = options.research.slice(0, 6).map((row) => `<li><a href="/research/${esc(row.slug)}">${esc(row.title)}</a><time>${esc(row.created_at.slice(0, 10))}</time></li>`).join('');
  const tickets = options.tickets.slice(0, 6).map((row) => `<li><a href="/models/forecast/${esc(row.slug)}">${esc(row.title)}</a><span>${esc(row.status)}</span></li>`).join('');
  return [
    '<section class="dossier-context" aria-labelledby="dossierContextTitle">',
    `  <header><div><span class="ara-eyebrow">${ko ? '통합 정보' : 'Connected dossier'}</span><h2 id="dossierContextTitle">${ko ? '관련 파이프라인 기록' : 'Across the research arm'}</h2></div><button class="watch-topic-button${options.watchlisted ? ' is-active' : ''}" type="button" data-watch-topic="${esc(options.slug)}" aria-pressed="${options.watchlisted}">${options.watchlisted ? '★' : '+'} ${ko ? '관심 주제' : 'Watch topic'}</button></header>`,
    '  <div class="dossier-context-grid">',
    `    <section><h3>${ko ? '긴 리서치' : 'Long-form research'}</h3>${research ? `<ul>${research}</ul>` : `<p>${ko ? '연결된 글 없음' : 'No linked articles yet.'}</p>`}</section>`,
    `    <section><h3>${ko ? '이벤트·예측' : 'Events & forecasts'}</h3>${tickets ? `<ul>${tickets}</ul>` : `<p>${ko ? '연결된 티켓 없음' : 'No linked model tickets yet.'}</p>`}</section>`,
    '  </div>',
    renderEvidenceDrawer(options.claims.slice(0, 30), { language: options.language, title: ko ? '이 주제의 공개 근거' : 'Public evidence for this topic' }),
    '</section>',
  ].join('\n');
}

type PricingHistory = { ts: string; frontier_price_at?: Record<string, number | null> };
type GpuSpot = { generated_at?: string; stale?: boolean; snapshot?: { models?: Record<string, { median?: number; min?: number; samples?: number; stale?: boolean; truncated?: boolean }> }; history?: Array<Record<string, unknown>> };

function sparkline(values: number[]): string {
  if (values.length < 2) return '';
  const width = 260, height = 72, min = Math.min(...values), max = Math.max(...values), span = max - min || 1;
  const points = values.map((value, index) => `${(index / (values.length - 1) * width).toFixed(1)},${(height - ((value - min) / span) * (height - 8) - 4).toFixed(1)}`).join(' ');
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="trend over ${values.length} snapshots"><polyline points="${points}" fill="none" vector-effect="non-scaling-stroke"/></svg>`;
}

export function renderMarketTrends(pricingHistory: PricingHistory[] = [], gpu: GpuSpot | null, language: 'en' | 'ko'): string {
  const ko = language === 'ko';
  const tier = Object.keys(pricingHistory[pricingHistory.length - 1]?.frontier_price_at || {}).filter((key) => pricingHistory.some((row) => typeof row.frontier_price_at?.[key] === 'number')).sort((a, b) => Number(b) - Number(a))[0];
  const prices = pricingHistory.slice(-36).map((row) => row.frontier_price_at?.[tier]).filter((value): value is number => typeof value === 'number');
  const gpuRows = Object.entries(gpu?.snapshot?.models || {}).filter(([, row]) => typeof row.median === 'number').sort((a, b) => (a[1].median || 0) - (b[1].median || 0)).slice(0, 8);
  return [
    '<section class="market-trends" aria-labelledby="marketTrendsTitle">',
    `  <header><span class="ara-eyebrow">${ko ? '장기 비용 신호' : 'Longitudinal cost signals'}</span><h2 id="marketTrendsTitle">${ko ? '성능 디플레이션과 GPU 현물' : 'Capability deflation & GPU spot'}</h2></header>`,
    '  <div class="market-trends-grid">',
    `    <article><h3>${ko ? `벤치마크 ${esc(tier || '—')} 달성 비용` : `Cost to reach score ${esc(tier || '—')}`}</h3>${sparkline(prices)}<p>${prices.length ? `$${prices[prices.length - 1].toFixed(2)} / Mtok` : (ko ? '데이터 없음' : 'No comparable history yet')} · ${prices.length} ${ko ? '개 스냅샷' : 'snapshots'}</p></article>`,
    `    <article><h3>${ko ? 'GPU당 시간당 중앙값' : 'Median USD per GPU-hour'}</h3><div class="gpu-price-list">${gpuRows.map(([name, row]) => `<div><span>${esc(name)}${row.truncated ? ' *' : ''}</span><strong>$${Number(row.median).toFixed(2)}</strong><small>${row.samples || 0} samples</small></div>`).join('')}</div><p>${gpu?.stale ? (ko ? '가격 지연' : 'Prices stale') : (ko ? `실시간 스냅샷 · ${esc(gpu?.generated_at || '')}` : `Live snapshot · ${esc(gpu?.generated_at || '')}`)}</p></article>`,
    '  </div>',
    `  <p class="market-method-note">${ko ? '* 부분 표본. 스냅샷 방법 버전이 같은 시계열만 비교하세요.' : '* Incomplete sample. Compare only history points with the same method version; spot listings are not executable quotes.'}</p>`,
    '</section>',
  ].join('\n');
}
