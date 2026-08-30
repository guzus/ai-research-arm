/** Resolve a requested calendar day to a date that was actually published.
 *
 * The browser's local day can be ahead of the UTC publication pipeline. A
 * Today URL must never claim that older fallback content belongs to that newer
 * day, so missing days resolve to the nearest earlier publication. If no
 * earlier publication exists, there is no truthful fallback.
 */
export function resolvePublishedDate(dates: string[], requested: string): string | null {
  const published = normalizedDates(dates);
  if (published.length === 0) return null;
  if (published.includes(requested)) return requested;

  let previous: string | null = null;
  for (const date of published) {
    if (date > requested) break;
    previous = date;
  }
  return previous;
}

function isIsoCalendarDate(value: string): boolean {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) return false;
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.getUTCFullYear() === year &&
    date.getUTCMonth() === month - 1 &&
    date.getUTCDate() === day;
}

function normalizedDates(dates: string[]): string[] {
  return Array.from(new Set(dates.filter(isIsoCalendarDate))).sort();
}

export function latestPublishedDate(dates: string[]): string | null {
  const published = normalizedDates(dates);
  return published[published.length - 1] ?? null;
}

export type RootRouteEvent = 'enter-home' | 'enter-other' | 'rerender';

/** Root identity belongs to the history entry, not to one render pass. A
 * rerender (refresh button, language switch) therefore retains it, while a
 * parsed or user-selected non-root destination clears it. */
export function transitionRootRoute(active: boolean, event: RootRouteEvent): boolean {
  if (event === 'enter-home') return true;
  if (event === 'enter-other') return false;
  return active;
}

/** Editorial availability is additive manifest data. Older manifests did not
 * distinguish operational fallback files from publications, so treating
 * `today` as editorial would publish exactly the content this field protects.
 * Missing or malformed data must therefore fail closed. */
export function editorialDatesFromManifest(value: unknown): string[] {
  return Array.isArray(value)
    ? normalizedDates(value.filter((date): date is string => typeof date === 'string'))
    : [];
}

/** A dated Today file can be routable without being an editorial publication
 * (the deterministic unavailable projection). Only explicit dated entries use
 * this state; root/latest aliases are handled by resolveTodayEntryPlan. */
export function isExplicitUnavailableTodayDate(
  todayDates: string[],
  editorialDates: string[],
  requested: string,
  isLatestEntry: boolean,
): boolean {
  if (isLatestEntry) return false;
  return normalizedDates(todayDates).includes(requested)
    && !normalizedDates(editorialDates).includes(requested);
}

export function unavailableTodayRoutePolicy(date: string): {
  canonicalPath: string;
  indexable: false;
  type: 'website';
} {
  return {
    canonicalPath: `/today/${date}`,
    indexable: false,
    type: 'website',
  };
}

export type TodayEntryPlan =
  | { kind: 'explicit'; date: string }
  | { kind: 'editorial'; date: string }
  | { kind: 'empty' };

/** The root and `/today` are latest-publication entry points. Explicit dated
 * routes are user-selected archival addresses and must not be rewritten. An
 * empty editorial list is a rendering decision, never permission to fetch an
 * operational fallback file as "latest". */
export function resolveTodayEntryPlan(
  editorialDates: string[],
  requested: string,
  isLatestEntry: boolean,
): TodayEntryPlan {
  if (!isLatestEntry) return { kind: 'explicit', date: requested };
  const latest = latestPublishedDate(editorialDates);
  return latest ? { kind: 'editorial', date: latest } : { kind: 'empty' };
}
