import { uiText, type UiLanguage } from '../i18n';

export type ArmTimelineItemKind = 'completed' | 'scheduled';

export type ArmTimelineItem = {
  id: string;
  kind: ArmTimelineItemKind;
  lane: string;
  title: string;
  status: string;
  start: string;
  end: string;
  source: string;
  model?: string;
  commit?: string;
  url?: string;
};

export type ArmTimeline = {
  generatedAt: string;
  windowStart: string;
  windowEnd: string;
  timezone: 'UTC';
  items: ArmTimelineItem[];
};

type ParsedArmTimelineItem = ArmTimelineItem & { startMs: number; endMs: number };
type LaneDetailProfile = {
  statuses: Set<string>;
  sources: Set<string>;
  models: Set<string>;
  hasMissingModel: boolean;
};

const HOUR_MS = 60 * 60 * 1000;
const MINUTE_MS = 60 * 1000;

function parseTime(value: string): number | null {
  const ms = Date.parse(value);
  return Number.isFinite(ms) ? ms : null;
}

function formatUtcTime(ms: number, language: UiLanguage): string {
  return new Intl.DateTimeFormat(language === 'ko' ? 'ko-KR' : 'en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'UTC',
  }).format(new Date(ms));
}

function formatUtcDateTime(ms: number, language: UiLanguage): string {
  return new Intl.DateTimeFormat(language === 'ko' ? 'ko-KR' : 'en-US', {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'UTC',
  }).format(new Date(ms)) + ' UTC';
}

function formatDuration(startMs: number, endMs: number, language: UiLanguage): string {
  const mins = Math.max(1, Math.round((endMs - startMs) / MINUTE_MS));
  if (mins < 60) return language === 'ko' ? mins + '분' : mins + 'm';
  const hours = Math.floor(mins / 60);
  const rest = mins % 60;
  if (language === 'ko') return rest === 0 ? hours + '시간' : hours + '시간 ' + rest + '분';
  return rest === 0 ? hours + 'h' : hours + 'h ' + rest + 'm';
}

function makeText(tag: string, className: string, text: string): HTMLElement {
  const el = document.createElement(tag);
  el.className = className;
  el.textContent = text;
  return el;
}

function normalizedValue(value?: string): string {
  return (value || '').trim();
}

function isFailureStatus(status: string): boolean {
  return /\b(?:fail|failed|failure|error|cancelled|canceled|timeout|timed out)\b/i.test(status);
}

function statusValue(item: ArmTimelineItem): string {
  return normalizedValue(item.status || item.kind).toLowerCase();
}

function laneDetailProfile(items: ParsedArmTimelineItem[]): LaneDetailProfile {
  return {
    statuses: new Set(items.map((item) => statusValue(item))),
    sources: new Set(items.map((item) => normalizedValue(item.source).toLowerCase()).filter(Boolean)),
    models: new Set(items.map((item) => normalizedValue(item.model).toLowerCase()).filter(Boolean)),
    hasMissingModel: items.some((item) => !normalizedValue(item.model)),
  };
}

function appendDetailRow(list: HTMLElement, label: string, value: string): void {
  if (!value) return;
  const row = document.createElement('div');
  row.className = 'agents-work-detail-row';
  row.appendChild(makeText('dt', '', label));
  row.appendChild(makeText('dd', '', value));
  list.appendChild(row);
}

function makeItemDetails(item: ParsedArmTimelineItem, profile: LaneDetailProfile, language: UiLanguage): HTMLElement {
  const details = document.createElement('dl');
  details.className = 'agents-work-details';

  const failed = isFailureStatus(item.status);
  const primaryLabel = failed ? uiText(language, 'agents.failed') : item.kind === 'scheduled' ? uiText(language, 'agents.scheduled') : uiText(language, 'agents.updated');
  const primaryMs = item.kind === 'scheduled' ? item.startMs : item.endMs;
  appendDetailRow(details, primaryLabel, formatUtcDateTime(primaryMs, language));
  appendDetailRow(details, uiText(language, 'agents.time'), formatUtcTime(item.startMs, language) + '-' + formatUtcTime(item.endMs, language) + ' UTC');
  appendDetailRow(details, uiText(language, 'agents.duration'), formatDuration(item.startMs, item.endMs, language));

  const showStatus = failed || profile.statuses.size > 1 || statusValue(item) !== item.kind;
  if (showStatus) appendDetailRow(details, uiText(language, 'agents.status'), normalizedValue(item.status || item.kind));

  const model = normalizedValue(item.model);
  if (model && (profile.models.size > 1 || profile.hasMissingModel)) {
    appendDetailRow(details, uiText(language, 'agents.model'), model);
  }

  const source = normalizedValue(item.source);
  if (source && profile.sources.size > 1) appendDetailRow(details, uiText(language, 'agents.source'), source);
  if (item.commit) appendDetailRow(details, uiText(language, 'agents.commit'), item.commit);

  return details;
}

function itemSort(a: ArmTimelineItem, b: ArmTimelineItem): number {
  return String(a.start).localeCompare(String(b.start)) || a.title.localeCompare(b.title);
}

export function renderAgentsStudioHtml(language: UiLanguage): string {
  return [
    '<section class="agents-lite-page" aria-label="' + uiText(language, 'agents.label') + '">',
    '  <div class="content-card agents-lite-card">',
    '    <div class="content-card-header agents-lite-header">',
    '      <div>',
    '        <div class="content-card-title">' + uiText(language, 'agents.title') + '</div>',
    '        <p>' + uiText(language, 'agents.description', { blog: '<a href="https://guzus.substack.com/p/open-sourcing-ai-research-arm-ara" target="_blank" rel="noopener noreferrer">' + uiText(language, 'agents.blog') + '</a>' }) + '</p>',
    '      </div>',
    '    </div>',
    '    <div class="content-card-body agents-lite-body" id="armTimeline">',
    '      <div class="agents-lite-status">' + uiText(language, 'agents.loading') + '</div>',
    '    </div>',
    '  </div>',
    '</section>',
  ].join('\n');
}

export function hydrateAgentsTimeline(root: ParentNode, timeline: ArmTimeline | null, language: UiLanguage): void {
  const mount = root.querySelector<HTMLElement>('#armTimeline');
  if (!mount) return;
  mount.replaceChildren();

  if (!timeline || !Array.isArray(timeline.items) || timeline.items.length === 0) {
    mount.appendChild(makeText('div', 'agents-lite-status', uiText(language, 'agents.none')));
    return;
  }

  const windowStartMs = parseTime(timeline.windowStart);
  const windowEndMs = parseTime(timeline.windowEnd);
  if (windowStartMs === null || windowEndMs === null || windowEndMs <= windowStartMs) {
    mount.appendChild(makeText('div', 'agents-lite-status', uiText(language, 'agents.malformed')));
    return;
  }

  const items = timeline.items
    .map((item) => {
      const startMs = parseTime(item.start);
      const endMs = parseTime(item.end);
      if (startMs === null || endMs === null) return null;
      return { ...item, startMs, endMs: Math.max(endMs, startMs + MINUTE_MS) };
    })
    .filter((item): item is ArmTimelineItem & { startMs: number; endMs: number } => item !== null)
    .filter((item) => item.endMs >= windowStartMs && item.startMs <= windowEndMs)
    .sort(itemSort);

  if (items.length === 0) {
    mount.appendChild(makeText('div', 'agents-lite-status', uiText(language, 'agents.noneWindow')));
    return;
  }

  const header = document.createElement('div');
  header.className = 'agents-work-summary';
  header.appendChild(makeText('div', 'agents-work-summary-title', 'GitHub Actions'));
  header.appendChild(makeText('div', 'agents-work-summary-meta', formatUtcDateTime(windowStartMs, language) + ' - ' + formatUtcDateTime(windowEndMs, language)));
  mount.appendChild(header);

  const ledger = document.createElement('div');
  ledger.className = 'agents-work-ledger';

  const labels = document.createElement('div');
  labels.className = 'agents-work-labels';
  labels.appendChild(document.createElement('div')).className = 'agents-work-label-spacer';

  const scroll = document.createElement('div');
  scroll.className = 'agents-work-scroll';
  const totalHours = Math.max(1, Math.ceil((windowEndMs - windowStartMs) / HOUR_MS));
  const timelineWidth = Math.max(960, totalHours * 88);
  const lanes = Array.from(new Set(items.map((item) => item.lane))).sort();

  const ruler = document.createElement('div');
  ruler.className = 'agents-work-ruler';
  ruler.style.width = timelineWidth + 'px';
  for (let i = 0; i <= totalHours; i += 1) {
    const tick = document.createElement('span');
    tick.textContent = formatUtcTime(windowStartMs + (i * HOUR_MS), language);
    tick.style.left = ((i / totalHours) * 100) + '%';
    ruler.appendChild(tick);
  }
  scroll.appendChild(ruler);

  for (const lane of lanes) {
    const laneItems = items.filter((item) => item.lane === lane);
    const detailProfile = laneDetailProfile(laneItems);
    const head = document.createElement('header');
    head.className = 'agents-work-row-head';
    head.appendChild(makeText('strong', '', lane));
    head.appendChild(makeText('span', '', uiText(language, 'agents.items', { count: laneItems.length })));
    labels.appendChild(head);

    const track = document.createElement('div');
    track.className = 'agents-work-track';
    track.style.width = timelineWidth + 'px';

    for (const item of laneItems) {
      const start = Math.max(item.startMs, windowStartMs);
      const end = Math.min(item.endMs, windowEndMs);
      const left = ((start - windowStartMs) / (windowEndMs - windowStartMs)) * 100;
      const width = Math.max(1.4, ((end - start) / (windowEndMs - windowStartMs)) * 100);
      const card = document.createElement(item.url ? 'a' : 'article');
      const failed = isFailureStatus(item.status);
      card.className = 'agents-work-item agents-work-item--' + item.kind + (failed ? ' agents-work-item--failed' : '');
      if (item.url && card instanceof HTMLAnchorElement) {
        card.href = item.url;
        card.target = '_blank';
        card.rel = 'noopener noreferrer';
      }
      card.tabIndex = 0;
      card.dataset.status = normalizedValue(item.status || item.kind);
      card.style.left = left.toFixed(3) + '%';
      card.style.width = width.toFixed(3) + '%';
      card.setAttribute('aria-label', item.title + ', ' + formatUtcDateTime(item.startMs, language) + ' - ' + formatUtcDateTime(item.endMs, language));
      card.appendChild(makeText('strong', '', item.title));
      if (failed) card.appendChild(makeText('span', 'agents-work-fail-badge', uiText(language, 'agents.failedBadge')));
      card.appendChild(makeItemDetails(item, detailProfile, language));
      track.appendChild(card);
    }
    scroll.appendChild(track);
  }

  ledger.appendChild(labels);
  ledger.appendChild(scroll);
  mount.appendChild(ledger);

  const generatedMs = parseTime(timeline.generatedAt) ?? Date.now();
  const targetMs = Math.min(
    Math.max(generatedMs - (2 * HOUR_MS), windowStartMs),
    windowEndMs,
  );
  window.requestAnimationFrame(() => {
    const maxScroll = Math.max(0, scroll.scrollWidth - scroll.clientWidth);
    const ratio = (targetMs - windowStartMs) / (windowEndMs - windowStartMs);
    scroll.scrollLeft = Math.round(maxScroll * ratio);
  });
}
