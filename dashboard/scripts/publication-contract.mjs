export const PUBLICATION_UNAVAILABLE_MARKER = '<!-- ara-publication-state: unavailable -->';

const FALLBACK_BANNER = '> **Deterministic fallback digest.**';

/** The operational fallback generator owns this exact banner. Restrict the
 * check to the document header so an editorial discussion of the fallback
 * mechanism cannot accidentally suppress a real brief. */
export function isDeterministicFallbackSource(markdown) {
  return String(markdown)
    .split(/\r?\n/)
    .slice(0, 8)
    .some(line => line.trim() === FALLBACK_BANNER || line.trim().startsWith(`${FALLBACK_BANNER} `));
}

export function unavailableDigestMarkdown(date) {
  return `${PUBLICATION_UNAVAILABLE_MARKER}\n# AI Daily Digest — ${date}\n`;
}

export function isPublicUnavailableDigest(markdown) {
  return String(markdown).trimStart().startsWith(PUBLICATION_UNAVAILABLE_MARKER);
}

/** Keep file availability separate from editorial publication. A sanitized
 * unavailable digest remains fetchable for an explicit dated route, but it
 * must never become the root page's "latest brief". */
export function editorialDigestDates(dates, readDigest) {
  return Array.from(new Set(dates))
    .filter(date => !isPublicUnavailableDigest(readDigest(date)))
    .sort();
}

export function latestEditorialRecord(records) {
  return records
    .filter(record => record && !record.unavailable && typeof record.date === 'string')
    .slice()
    .sort((a, b) => a.date.localeCompare(b.date))
    .at(-1) ?? null;
}

export function latestEditorialAliasPlan(records) {
  const record = latestEditorialRecord(records);
  return record ? { kind: 'editorial', record } : { kind: 'empty' };
}

/** Static crawlers must see the same publication type as the hydrated app.
 * An unavailable dated route is a diagnostic WebPage, not an Article with a
 * fabricated publication event. */
export function digestStaticSeoSemantics(date, unavailable) {
  return unavailable
    ? { ogType: 'website', articlePublishedTime: null }
    : { ogType: 'article', articlePublishedTime: date };
}
