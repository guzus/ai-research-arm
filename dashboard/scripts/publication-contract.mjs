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
