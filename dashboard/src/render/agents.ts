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

function formatUtcTime(ms: number): string {
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'UTC',
  }).format(new Date(ms));
}

function formatUtcDateTime(ms: number): string {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'UTC',
  }).format(new Date(ms)) + ' UTC';
}

function formatDuration(startMs: number, endMs: number): string {
  const mins = Math.max(1, Math.round((endMs - startMs) / MINUTE_MS));
  if (mins < 60) return mins + 'm';
  const hours = Math.floor(mins / 60);
  const rest = mins % 60;
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

function makeItemDetails(item: ParsedArmTimelineItem, profile: LaneDetailProfile): HTMLElement {
  const details = document.createElement('dl');
  details.className = 'agents-work-details';

  const failed = isFailureStatus(item.status);
  const primaryLabel = failed ? 'Failed' : item.kind === 'scheduled' ? 'Scheduled' : 'Updated';
  const primaryMs = item.kind === 'scheduled' ? item.startMs : item.endMs;
  appendDetailRow(details, primaryLabel, formatUtcDateTime(primaryMs));
  appendDetailRow(details, 'Time', formatUtcTime(item.startMs) + '-' + formatUtcTime(item.endMs) + ' UTC');
  appendDetailRow(details, 'Duration', formatDuration(item.startMs, item.endMs));

  const showStatus = failed || profile.statuses.size > 1 || statusValue(item) !== item.kind;
  if (showStatus) appendDetailRow(details, 'Status', normalizedValue(item.status || item.kind));

  const model = normalizedValue(item.model);
  if (model && (profile.models.size > 1 || profile.hasMissingModel)) {
    appendDetailRow(details, 'Model', model);
  }

  const source = normalizedValue(item.source);
  if (source && profile.sources.size > 1) appendDetailRow(details, 'Source', source);
  if (item.commit) appendDetailRow(details, 'Commit', item.commit);

  return details;
}

function itemSort(a: ArmTimelineItem, b: ArmTimelineItem): number {
  return String(a.start).localeCompare(String(b.start)) || a.title.localeCompare(b.title);
}

export function renderAgentsStudioHtml(): string {
  return [
    '<section class="agents-lite-page" aria-label="Arm work timeline">',
    '  <div class="content-card agents-lite-card">',
    '    <div class="content-card-header agents-lite-header">',
    '      <div>',
    '        <div class="content-card-title">Agent workers</div>',
    '        <p>Real completed and scheduled pipeline work, shown by UTC start and end time.</p>',
    '      </div>',
    '      <div class="agents-lite-metrics" id="armMetrics">',
    '        <div class="agents-lite-metric"><span>completed</span><strong>--</strong></div>',
    '        <div class="agents-lite-metric"><span>scheduled</span><strong>--</strong></div>',
    '        <div class="agents-lite-metric"><span>window</span><strong>--</strong></div>',
    '      </div>',
    '    </div>',
    '    <div class="content-card-body agents-lite-body" id="armTimeline">',
    '      <div class="agents-lite-status">Loading real work timeline...</div>',
    '    </div>',
    '  </div>',
    '</section>',
  ].join('\n');
}

export function hydrateAgentsTimeline(root: ParentNode, timeline: ArmTimeline | null): void {
  const mount = root.querySelector<HTMLElement>('#armTimeline');
  const metrics = root.querySelector<HTMLElement>('#armMetrics');
  if (!mount) return;
  mount.replaceChildren();

  if (!timeline || !Array.isArray(timeline.items) || timeline.items.length === 0) {
    mount.appendChild(makeText('div', 'agents-lite-status', 'No completed or scheduled work found.'));
    return;
  }

  const windowStartMs = parseTime(timeline.windowStart);
  const windowEndMs = parseTime(timeline.windowEnd);
  if (windowStartMs === null || windowEndMs === null || windowEndMs <= windowStartMs) {
    mount.appendChild(makeText('div', 'agents-lite-status', 'Timeline data is malformed.'));
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
    mount.appendChild(makeText('div', 'agents-lite-status', 'No completed or scheduled work found in this window.'));
    return;
  }

  const completed = items.filter((item) => item.kind === 'completed').length;
  const scheduled = items.filter((item) => item.kind === 'scheduled').length;
  if (metrics) {
    metrics.replaceChildren();
    for (const [label, value] of [
      ['completed', String(completed)],
      ['scheduled', String(scheduled)],
      ['window', formatDuration(windowStartMs, windowEndMs)],
    ]) {
      const card = document.createElement('div');
      card.className = 'agents-lite-metric';
      card.appendChild(makeText('span', '', label));
      card.appendChild(makeText('strong', '', value));
      metrics.appendChild(card);
    }
  }

  const header = document.createElement('div');
  header.className = 'agents-work-summary';
  header.appendChild(makeText('div', 'agents-work-summary-title', 'UTC work ledger'));
  header.appendChild(makeText('div', 'agents-work-summary-meta', formatUtcDateTime(windowStartMs) + ' - ' + formatUtcDateTime(windowEndMs)));
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
    tick.textContent = formatUtcTime(windowStartMs + (i * HOUR_MS));
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
    head.appendChild(makeText('span', '', laneItems.length + ' items'));
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
      card.setAttribute('aria-label', item.title + ', ' + formatUtcDateTime(item.startMs) + ' to ' + formatUtcDateTime(item.endMs));
      card.appendChild(makeText('strong', '', item.title));
      if (failed) card.appendChild(makeText('span', 'agents-work-fail-badge', 'FAILED'));
      card.appendChild(makeItemDetails(item, detailProfile));
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
