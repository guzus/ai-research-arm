/** Resolve a requested calendar day to a date that was actually published.
 *
 * The browser's local day can be ahead of the UTC publication pipeline. A
 * Today URL must never claim that older fallback content belongs to that newer
 * day, so missing days resolve to the nearest earlier publication. If no
 * earlier publication exists, there is no truthful fallback.
 */
export function resolvePublishedDate(dates: string[], requested: string): string | null {
  const published = Array.from(new Set(dates)).sort();
  if (published.length === 0) return null;
  if (published.includes(requested)) return requested;

  let previous: string | null = null;
  for (const date of published) {
    if (date > requested) break;
    previous = date;
  }
  return previous;
}
