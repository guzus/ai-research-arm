// Pure route-policy helpers used by the SEO postbuild and tests. Keeping the
// canonical/indexability decisions here makes it harder for the sitemap and
// emitted HTML to silently disagree.

const DATE_RE = /^(\d{4})-(\d{2})-(\d{2})$/;
const DATED_SECTIONS = new Set(['today', 'twitter', 'frontpage']);

export function datedRoute(section, date) {
  if (!DATED_SECTIONS.has(section)) throw new TypeError('invalid dated section');
  if (!isIsoCalendarDate(date)) throw new TypeError('invalid route date');
  return `/${section}/${date}`;
}

export function latestAliasPolicy(section, date, siteOrigin) {
  const route = datedRoute(section, date);
  return {
    route: `/${section}`,
    canonicalRoute: route,
    canonicalUrl: `${String(siteOrigin).replace(/\/+$/, '')}${route}`,
    indexable: false,
  };
}

export function datedPagePolicy(section, date, siteOrigin) {
  const route = datedRoute(section, date);
  return {
    route,
    canonicalRoute: route,
    canonicalUrl: `${String(siteOrigin).replace(/\/+$/, '')}${route}`,
    indexable: true,
  };
}

export function sortDatedRecords(records) {
  return [...records]
    .filter(record => isIsoCalendarDate(record?.date))
    .sort((a, b) => String(a.date).localeCompare(String(b.date)));
}

export function isIsoCalendarDate(value) {
  const match = DATE_RE.exec(String(value || ''));
  if (!match) return false;
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.getUTCFullYear() === year &&
    date.getUTCMonth() === month - 1 &&
    date.getUTCDate() === day;
}

export function isIndexableResearchEntry(entry) {
  if (!entry || typeof entry !== 'object') return false;
  const tags = new Set(
    (Array.isArray(entry.tags) ? entry.tags : [])
      .map(tag => String(tag).trim().toLowerCase())
      .filter(Boolean),
  );
  if (tags.has('fixture') || tags.has('test')) return false;
  if (String(entry.slug || '') === 'components') return false;
  if (tags.has('system') && tags.has('reference')) return false;
  return true;
}
