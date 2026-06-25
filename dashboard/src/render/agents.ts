import { escapeHtml } from './shared';

type AgentClip = {
  title: string;
  meta: string;
  className: string;
};

type AgentTrack = {
  name: string;
  role: string;
  status: string;
  clips: AgentClip[];
};

const TRACKS: AgentTrack[] = [
  {
    name: 'Intake',
    role: 'source collection',
    status: 'watching feeds',
    clips: [
      { title: 'Twitter/X sweep', meta: 'birdy fan-out', className: 'agents-lite-clip--a' },
      { title: 'RSS + community', meta: 'fallback ready', className: 'agents-lite-clip--b' },
      { title: 'Snapshot cache', meta: 'dedupe input', className: 'agents-lite-clip--c' },
    ],
  },
  {
    name: 'Research',
    role: 'evidence checks',
    status: 'triangulating',
    clips: [
      { title: 'Primary sources', meta: 'official docs', className: 'agents-lite-clip--d' },
      { title: 'Counter-check', meta: 'claim stress test', className: 'agents-lite-clip--e' },
      { title: 'Source map', meta: 'links + handles', className: 'agents-lite-clip--f' },
    ],
  },
  {
    name: 'Writing',
    role: 'synthesis',
    status: 'drafting',
    clips: [
      { title: 'Cycle brief', meta: 'top stories', className: 'agents-lite-clip--g' },
      { title: 'Long-form section', meta: 'tables + notes', className: 'agents-lite-clip--h' },
    ],
  },
  {
    name: 'Review',
    role: 'quality gate',
    status: 'checking drift',
    clips: [
      { title: 'Method audit', meta: 'assumptions', className: 'agents-lite-clip--i' },
      { title: 'Contract check', meta: 'schema + files', className: 'agents-lite-clip--j' },
      { title: 'Smoke run', meta: 'build + browser', className: 'agents-lite-clip--k' },
    ],
  },
  {
    name: 'Publish',
    role: 'delivery',
    status: 'shipping',
    clips: [
      { title: 'Commit', meta: 'safe push', className: 'agents-lite-clip--l' },
      { title: 'Notify', meta: 'Hooker relay', className: 'agents-lite-clip--m' },
    ],
  },
];

const METRICS = [
  ['workers', '5'],
  ['handoffs', '13'],
  ['latest', '19:57'],
];

function renderClip(track: AgentTrack, clip: AgentClip): string {
  return [
    '<article class="agents-lite-clip ' + clip.className + '" aria-label="' + escapeHtml(track.name + ': ' + clip.title) + '">',
    '  <strong>' + escapeHtml(clip.title) + '</strong>',
    '  <span>' + escapeHtml(clip.meta) + '</span>',
    '</article>',
  ].join('\n');
}

function renderTrack(track: AgentTrack): string {
  return [
    '<section class="agents-lite-track">',
    '  <header class="agents-lite-track-head">',
    '    <div>',
    '      <strong>' + escapeHtml(track.name) + '</strong>',
    '      <span>' + escapeHtml(track.role) + '</span>',
    '    </div>',
    '    <em>' + escapeHtml(track.status) + '</em>',
    '  </header>',
    '  <div class="agents-lite-lane">',
    track.clips.map((clip) => renderClip(track, clip)).join('\n'),
    '  </div>',
    '</section>',
  ].join('\n');
}

function renderMetrics(): string {
  return METRICS.map(([label, value]) => [
    '<div class="agents-lite-metric">',
    '  <span>' + escapeHtml(label) + '</span>',
    '  <strong>' + escapeHtml(value) + '</strong>',
    '</div>',
  ].join('\n')).join('\n');
}

export function renderAgentsStudioHtml(): string {
  return [
    '<section class="agents-lite-page" aria-label="Parallel agent workers">',
    '  <div class="content-card agents-lite-card">',
    '    <div class="content-card-header agents-lite-header">',
    '      <div>',
    '        <div class="content-card-title">Agent workers</div>',
    '        <p>Parallel research work, shown as tracks and task spans.</p>',
    '      </div>',
    '      <div class="agents-lite-metrics">' + renderMetrics() + '</div>',
    '    </div>',
    '    <div class="content-card-body agents-lite-body">',
    '      <div class="agents-lite-ruler" aria-hidden="true">',
    '        <span>intake</span><span>research</span><span>write</span><span>review</span><span>publish</span>',
    '      </div>',
    '      <div class="agents-lite-board">',
    '        <div class="agents-lite-playhead" aria-hidden="true"></div>',
    TRACKS.map(renderTrack).join('\n'),
    '      </div>',
    '    </div>',
    '  </div>',
    '</section>',
  ].join('\n');
}
