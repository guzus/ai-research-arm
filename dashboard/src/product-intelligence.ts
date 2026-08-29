export type PublicClaim = {
  article: string;
  article_title: string;
  article_created_at?: string;
  key: string;
  claim: string;
  type: string;
  confidence: 'high' | 'medium' | 'low' | string;
  risk?: string | null;
  as_of?: string | null;
  reusable: boolean;
  reuse_block?: string | null;
  source_tiers: string[];
  source_urls: string[];
  hosts?: string[];
};

export type EvidenceSearchEntry = {
  id: string;
  type: 'research' | 'wiki' | 'model' | 'claim';
  title: string;
  body: string;
  url: string;
  date?: string;
  entity?: string;
  confidence?: string;
  risk?: string;
  sourceTier?: string;
  sourceTiers?: string[];
  language?: string;
};

export type WatchlistState = {
  topics: string[];
  lastVisit: string | null;
};

const WATCHLIST_KEY = 'ara:watchlist:v1';

export function normalizeTopic(value: string): string {
  return value.trim().toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, '');
}

export function readWatchlist(storage: Storage | null = typeof localStorage === 'undefined' ? null : localStorage): WatchlistState {
  if (!storage) return { topics: [], lastVisit: null };
  try {
    const parsed = JSON.parse(storage.getItem(WATCHLIST_KEY) || '{}') as Partial<WatchlistState>;
    const topics = Array.isArray(parsed.topics)
      ? Array.from(new Set(parsed.topics.map(normalizeTopic).filter(Boolean))).slice(0, 50)
      : [];
    return { topics, lastVisit: typeof parsed.lastVisit === 'string' ? parsed.lastVisit : null };
  } catch {
    return { topics: [], lastVisit: null };
  }
}

export function writeWatchlist(state: WatchlistState, storage: Storage | null = typeof localStorage === 'undefined' ? null : localStorage): void {
  if (!storage) return;
  storage.setItem(WATCHLIST_KEY, JSON.stringify({
    topics: Array.from(new Set(state.topics.map(normalizeTopic).filter(Boolean))).slice(0, 50),
    lastVisit: state.lastVisit,
  }));
}

export function watchlistFromUrl(search: string): string[] {
  const raw = new URLSearchParams(search).get('watch');
  if (!raw) return [];
  return Array.from(new Set(raw.split(',').map(normalizeTopic).filter(Boolean))).slice(0, 50);
}

export function watchlistSharePath(topics: string[], pathname = '/', language?: 'en' | 'ko'): string {
  const clean = Array.from(new Set(topics.map(normalizeTopic).filter(Boolean))).slice(0, 50);
  const params = new URLSearchParams();
  if (clean.length) params.set('watch', clean.join(','));
  if (language) params.set('lang', language);
  const safePath = pathname.startsWith('/') && !pathname.startsWith('//') ? pathname : '/';
  return params.size ? `${safePath}?${params.toString()}` : safePath;
}

export function textMatchesTopic(text: string, topic: string): boolean {
  const words = normalizeTopic(topic).split('-').filter((word) => word.length > 2);
  const hay = text.toLowerCase();
  return words.length > 0 && words.every((word) => hay.includes(word));
}

export function claimArticleStem(file: string): string {
  return file.replace(/\.(?:ko\.)?html$/i, '');
}

export function claimsForArticle(claims: PublicClaim[], file: string): PublicClaim[] {
  const stem = claimArticleStem(file);
  return claims.filter((claim) => claim.article === stem);
}

export function claimsForTopic(claims: PublicClaim[], topic: string, aliases: string[] = []): PublicClaim[] {
  const needles = [topic, ...aliases].map((value) => value.trim().toLowerCase()).filter((value) => value.length > 2);
  return claims.filter((claim) => {
    const hay = `${claim.claim} ${claim.article_title}`.toLowerCase();
    return needles.some((needle) => hay.includes(needle));
  });
}

export function confidenceRank(value?: string): number {
  if (value === 'high') return 3;
  if (value === 'medium') return 2;
  if (value === 'low') return 1;
  return 0;
}

export function searchEvidence(
  entries: EvidenceSearchEntry[],
  query: string,
  filters: Partial<Pick<EvidenceSearchEntry, 'type' | 'confidence' | 'risk' | 'sourceTier' | 'language'>>,
  limit = 80,
): EvidenceSearchEntry[] {
  const terms = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  return entries
    .filter((entry) => !filters.type || entry.type === filters.type)
    .filter((entry) => !filters.confidence || entry.confidence === filters.confidence)
    .filter((entry) => !filters.risk || entry.risk === filters.risk)
    .filter((entry) => !filters.sourceTier || entry.sourceTier === filters.sourceTier || entry.sourceTiers?.includes(filters.sourceTier))
    .filter((entry) => !filters.language || entry.language === filters.language)
    .map((entry) => {
      const title = entry.title.toLowerCase();
      const body = entry.body.toLowerCase();
      const score = terms.reduce((sum, term) => sum + (title.includes(term) ? 8 : 0) + (body.includes(term) ? 2 : 0), 0);
      return { entry, score };
    })
    .filter(({ score }) => terms.length === 0 || score > 0)
    .sort((a, b) => b.score - a.score || (b.entry.date || '').localeCompare(a.entry.date || '') || a.entry.title.localeCompare(b.entry.title))
    .slice(0, limit)
    .map(({ entry }) => entry);
}

export function excerptAround(text: string, query: string, max = 220): string {
  const clean = text.replace(/\s+/g, ' ').trim();
  if (clean.length <= max) return clean;
  const term = query.trim().toLowerCase().split(/\s+/).find(Boolean);
  const index = term ? clean.toLowerCase().indexOf(term) : -1;
  const start = Math.max(0, index > -1 ? index - Math.floor(max / 3) : 0);
  const prefix = start > 0 ? '…' : '';
  const suffix = start + max < clean.length ? '…' : '';
  return prefix + clean.slice(start, start + max).trim() + suffix;
}
