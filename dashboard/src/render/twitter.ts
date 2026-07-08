import {
  cleanPublicLeadText,
  escapeHtml,
  extractHandles,
  extractUrls,
  isSourceMethodLead,
  renderInfoTimeline,
  splitSections,
  stripMarkdown,
  truncateText,
} from './shared';
import type { InfoTimelineItem } from './shared';

export type TwitterStory = {
  rank: string;
  title: string;
  body: string;
  links: string[];
  handles: string[];
};

type TwitterMindshareCycle = {
  anchor: string;
  body: string;
  lead: string;
  recencyWeight: number;
  stories: TwitterStory[];
};

type TwitterMindshareItem = {
  label: string;
  share: number;
  tone: 'rising' | 'steady' | 'fading';
  href: string;
  handles: string[];
  sources: number;
};

type TimeInfo = {
  utc: string;
  local: string;
  localHours: number;
  localMinutes: number;
};

export type TwitterReportRenderOptions = {
  fallbackDate: string | null;
  currentDateStr: string;
  currentDateTitle: string;
  shownDateTitle: string;
  prevDate: string | null;
  nextDate: string | null;
  searchTerm: string;
  parseUtcTime: (title: string, dateStr: string) => TimeInfo | null;
  clockIcon: (hours: number, minutes: number) => string;
  twitterMarkdownToHtml: (md: string) => string;
  renderSourceChips: (urls: string[], limit?: number) => string;
  renderHandleChips: (handles: string[], limit?: number) => string;
};

function highlightPlainText(text: string, searchTerm: string): string {
  const escapedText = escapeHtml(text);
  if (!searchTerm) return escapedText;
  const escaped = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const re = new RegExp('(' + escaped + ')', 'gi');
  return escapedText.replace(re, '<mark>$1</mark>');
}

function extractCycleSummary(body: string): string {
  const match = body.match(/\*\*Cycle summary\*\*:\s*([\s\S]*?)(?=\n###|\n####|\n\*\*(?:Evidence|Previously|Counter|Verification|Watch)\*\*:|$)/i);
  return match ? match[1].trim() : '';
}

function extractSectionText(body: string, label: string): string {
  const re = new RegExp('\\*\\*' + label + '\\*\\*:\\s*([\\s\\S]*?)(?=\\n\\*\\*(?:Previously|Evidence|Counter / contradicting|Verification|Watch)\\*\\*:|\\n####\\s+\\d+\\.|$)', 'i');
  const match = body.match(re);
  return match ? match[1].trim() : '';
}

function cleanEvidenceLead(text: string): string {
  return text
    .split('\n')
    .map((line) => line
      .replace(/\*\*/g, '')
      .replace(/^[-*]\s+/, '')
      .replace(/^https?:\/\/\S+\s*(?:—|-|:)\s*/i, '')
      .replace(/^[\w.-]+\.[a-z]{2,}(?:\/\S*)?\s*(?:\([^)]*\))?\s*(?:—|-|:)+\s*/i, '')
      .replace(/^@[\w_]+:\s*/i, '')
      .replace(/^@[\w_]+\s+[^—\n]{0,140}\s+—\s*/i, '')
      .replace(/^["“]?[^"”]{0,160}["”]?\s+—\s+https?:\/\/\S+\s*(?:—\s*)?/i, '')
      .replace(/^\s*(?:—|-)+\s*/, '')
      .replace(/^the originating\b/i, 'Originating')
      .trim())
    .filter(Boolean)
    .join(' ');
}

export function storyCurrentLead(body: string): string {
  const evidence = extractSectionText(body, 'Evidence');
  if (evidence) return cleanEvidenceLead(evidence);
  return body
    .replace(/\*\*Previously\*\*:?[\s\S]*?(?=\n\*\*(?:Evidence|Counter \/ contradicting|Verification|Watch)\*\*:|$)/i, '')
    .trim();
}

export function parseTwitterStories(body: string): TwitterStory[] {
  const storyRe = /^####\s+(\d+)\.\s+(.+)$/gm;
  const matches = Array.from(body.matchAll(storyRe));
  return matches.map((match, idx) => {
    const start = (match.index || 0) + match[0].length;
    const nextStory = idx + 1 < matches.length ? matches[idx + 1].index || body.length : body.length;
    const nextSection = body.slice(start).search(/\n###\s+/);
    const sectionEnd = nextSection >= 0 ? start + nextSection : body.length;
    const end = Math.min(nextStory, sectionEnd);
    const storyBody = body.slice(start, end).trim();
    return {
      rank: match[1],
      title: match[2].trim(),
      body: storyBody,
      links: extractUrls(storyBody),
      handles: extractHandles(match[2] + '\n' + storyBody),
    };
  });
}

const TWITTER_MINDSHARE_TERMS: Array<{ label: string; pattern: RegExp }> = [
  { label: 'Anthropic', pattern: /\b(?:Anthropic|Claude|Fable\s*5|Mythos\s*5)\b/gi },
  { label: 'OpenAI', pattern: /\b(?:OpenAI|GPT-?5|GPT-?4\.?1|ChatGPT|Codex)\b/gi },
  { label: 'Google', pattern: /\b(?:Google|Gemini|DeepMind|NotebookLM|Veo)\b/gi },
  { label: 'xAI', pattern: /\b(?:xAI|Grok)\b/gi },
  { label: 'Meta', pattern: /\b(?:Meta|Llama)\b/gi },
  { label: 'Mistral', pattern: /\bMistral\b/gi },
  { label: 'Broadcom', pattern: /\bBroadcom\b/gi },
  { label: 'Sakana', pattern: /\bSakana\b/gi },
  { label: 'Marlin', pattern: /\bMarlin\b/gi },
  { label: 'Xiaomi', pattern: /\b(?:Xiaomi|MiMo)\b/gi },
  { label: 'Nebius', pattern: /\bNebius\b/gi },
  { label: 'Kimi', pattern: /\bKimi\b/gi },
  { label: 'MiniMax', pattern: /\bMiniMax\b/gi },
  { label: 'GLM', pattern: /\bGLM\b/gi },
  { label: 'Manus', pattern: /\bManus\b/gi },
  { label: 'NVIDIA', pattern: /\b(?:NVIDIA|NVDA|Blackwell|GB200|GB300)\b/gi },
  { label: 'Cerebras', pattern: /\bCerebras\b/gi },
  { label: 'Groq', pattern: /\bGroq\b/gi },
  { label: 'Adobe', pattern: /\bAdobe\b/gi },
  { label: 'Zoom', pattern: /\bZoom\b/gi },
  { label: 'Samsung', pattern: /\bSamsung\b/gi },
  { label: 'Sophos', pattern: /\bSophos\b/gi },
  { label: 'Apollo', pattern: /\bApollo\b/gi },
  { label: 'Blackstone', pattern: /\bBlackstone\b/gi },
  { label: 'Neuralink', pattern: /\bNeuralink\b/gi },
];

function twitterMindshareMatches(text: string): string[] {
  const labels: string[] = [];
  for (const term of TWITTER_MINDSHARE_TERMS) {
    term.pattern.lastIndex = 0;
    if (term.pattern.test(text)) labels.push(term.label);
  }
  return labels;
}

function rankWeight(rank: string): number {
  const n = Number(rank);
  if (!Number.isFinite(n) || n <= 0) return 1;
  return Math.max(1, 5 - n);
}

function buildTwitterMindshare(cycles: TwitterMindshareCycle[]): TwitterMindshareItem[] {
  const scores = new Map<string, {
    score: number;
    latest: number;
    earlier: number;
    href: string;
    topWeight: number;
    handles: Set<string>;
    sources: Set<string>;
  }>();
  const midpoint = Math.max(1, Math.ceil(cycles.length / 2));

  const addScore = (
    label: string,
    weight: number,
    cycle: TwitterMindshareCycle,
    handles: string[],
    sources: string[],
    isLatestHalf: boolean,
  ) => {
    const current = scores.get(label) || {
      score: 0,
      latest: 0,
      earlier: 0,
      href: '#' + cycle.anchor,
      topWeight: 0,
      handles: new Set<string>(),
      sources: new Set<string>(),
    };
    current.score += weight;
    if (isLatestHalf) current.latest += weight;
    else current.earlier += weight;
    if (weight > current.topWeight) {
      current.href = '#' + cycle.anchor;
      current.topWeight = weight;
    }
    handles.forEach((handle) => current.handles.add(handle));
    sources.forEach((source) => current.sources.add(source));
    scores.set(label, current);
  };

  cycles.forEach((cycle, index) => {
    const isLatestHalf = index < midpoint;
    const cycleWeight = Math.max(1, cycle.recencyWeight);
    const leadLabels = twitterMindshareMatches(cycle.lead);
    for (const label of leadLabels) {
      addScore(label, cycleWeight * 0.8, cycle, extractHandles(cycle.lead, 4), extractUrls(cycle.lead), isLatestHalf);
    }

    for (const story of cycle.stories) {
      const storyText = story.title + '\n' + story.body;
      const labels = twitterMindshareMatches(storyText);
      const weight = cycleWeight * rankWeight(story.rank);
      for (const label of labels) {
        addScore(label, weight, cycle, story.handles, story.links, isLatestHalf);
      }
    }
  });

  const total = Array.from(scores.values()).reduce((sum, item) => sum + item.score, 0);
  if (total <= 0) return [];

  return Array.from(scores.entries())
    .map(([label, item]) => {
      let tone: TwitterMindshareItem['tone'] = 'steady';
      if (item.latest > item.earlier * 1.25) tone = 'rising';
      else if (item.earlier > item.latest * 1.25) tone = 'fading';
      return {
        label,
        share: Math.max(1, Math.round((item.score / total) * 100)),
        tone,
        href: item.href,
        handles: Array.from(item.handles).slice(0, 2),
        sources: item.sources.size,
      };
    })
    .sort((a, b) => b.share - a.share || a.label.localeCompare(b.label))
    .slice(0, 18);
}

function twitterMindshareSizeClass(index: number): string {
  if (index === 0) return 'twitter-mindshare-tile--xl';
  if (index < 3) return 'twitter-mindshare-tile--lg';
  if (index < 7) return 'twitter-mindshare-tile--md';
  return 'twitter-mindshare-tile--sm';
}

function renderTwitterMindshareMap(items: TwitterMindshareItem[]): string {
  if (items.length === 0) return '';
  const tiles = items.map((item, index) => {
    return [
      '<a class="twitter-mindshare-tile ' + twitterMindshareSizeClass(index) + ' twitter-mindshare-tile--' + item.tone + '" href="' + escapeHtml(item.href) + '" aria-label="' + escapeHtml(item.label + ' mindshare, ' + item.tone) + '">',
      '  <strong>' + escapeHtml(item.label) + '</strong>',
      '</a>',
    ].filter(Boolean).join('\n');
  }).join('\n');
  return [
    '<section class="twitter-mindshare" aria-label="Twitter mindshare map">',
    '  <div class="twitter-mindshare-head">',
    '    <h2>Mindshare</h2>',
    '  </div>',
    '  <div class="twitter-mindshare-map">' + tiles + '</div>',
    '</section>',
  ].join('\n');
}

function extractStructuredTwitterStoryTitles(body: string): string[] {
  if (!/\btwitter-story-title\b/.test(body)) return [];
  const doc = new DOMParser().parseFromString('<div>' + body + '</div>', 'text/html');
  return Array.from(doc.querySelectorAll('article.twitter-story .twitter-story-title'))
    .map((node) => node.textContent?.replace(/\s+/g, ' ').trim() || '')
    .filter(Boolean);
}

function cleanTimelineStoryTitle(title: string): string {
  return cleanPublicLeadText(title
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/[*_`]/g, '')
    .replace(/\s+/g, ' ')
    .trim())
    .split(/\s+—\s+/)[0]
    .replace(/\.$/, '')
    .trim();
}

function summarizeTwitterTimeline(leadText: string, stories: TwitterStory[], body: string): string {
  const storyTitles = (stories.length > 0 ? stories.map((story) => story.title) : extractStructuredTwitterStoryTitles(body))
    .slice(0, 2)
    .map((title) => cleanTimelineStoryTitle(title))
    .filter(Boolean);
  if (storyTitles.length > 0) return truncateText(storyTitles.join('; ') + '.', 190);

  const sentences = leadText.match(/[^.!?]+[.!?]+/g)?.map((sentence) => sentence.trim()).filter(Boolean) || [];
  if (sentences.length > 0) return truncateText(sentences.slice(0, 2).join(' '), 190);
  return truncateText(leadText, 190);
}

function firstText(root: ParentNode, selector: string): string {
  return root.querySelector(selector)?.textContent?.replace(/\s+/g, ' ').trim() || '';
}

function firstHtml(root: ParentNode, selector: string): string {
  return (root.querySelector(selector) as HTMLElement | null)?.innerHTML?.trim() || '';
}

function twitterSignalsToCallouts(story: Element, searchTerm: string): string {
  const sig = story.querySelector('.twitter-story-signals');
  if (!sig) return '';
  const rows = Array.from(sig.querySelectorAll(':scope > div'));
  if (rows.length === 0) return '';
  return rows.map((row) => {
    const label = (row.querySelector('span')?.textContent || '').trim();
    let text = (row.textContent || '').replace(/\s+/g, ' ').trim();
    if (label && text.startsWith(label)) text = text.slice(label.length).trim();
    const isVerify = /verif/i.test(label);
    let variant = 'ara-callout--info';
    let flag = '';
    if (isVerify) {
      if (/⚠/.test(text)) { variant = 'ara-callout--warn'; flag = '<span class="ara-flag ara-flag--yellow"></span>'; }
      else if (/✓/.test(text)) { variant = 'ara-callout--success'; flag = '<span class="ara-flag ara-flag--green"></span>'; }
      text = text.replace(/^[✓⚠✗]\s*/, '');
    }
    const labelText = label || (isVerify ? 'Verify' : 'Watch');
    return '<div class="ara-callout ' + variant + '">'
      + '<span class="ara-callout-label">' + flag + escapeHtml(labelText) + '</span>'
      + '<p>' + highlightPlainText(text, searchTerm) + '</p></div>';
  }).join('\n');
}

function extractSkepticCorner(body: string): string {
  const m = body.match(/###\s+[^\n]*[Ss]keptic[^\n]*\n([\s\S]*?)(?=\n#{2,3}\s|$)/);
  return m ? m[1].trim() : '';
}

function renderStructuredTwitterStories(
  body: string,
  searchTerm: string,
): string {
  if (!/\btwitter-story\b/.test(body)) return '';
  const doc = new DOMParser().parseFromString('<div>' + body + '</div>', 'text/html');
  const stories = Array.from(doc.querySelectorAll('article.twitter-story'));
  if (stories.length === 0) return '';

  return stories.map((story, idx) => {
    const rank = story.getAttribute('data-rank') || String(idx + 1);
    const title = firstText(story, '.twitter-story-title, h3');
    const lead = firstText(story, '.twitter-story-lead');
    const sources = firstHtml(story, '.twitter-story-sources');
    const signalsHtml = twitterSignalsToCallouts(story, searchTerm);
    const bodyHtml = firstHtml(story, '.twitter-story-body') || firstHtml(story, '.twitter-story-details');
    const detailsBits = [
      sources ? '<div class="twitter-story-chips">' + sources + '</div>' : '',
      signalsHtml,
      bodyHtml ? '<div class="md-content twitter-story-body">' + bodyHtml + '</div>' : '',
    ].filter(Boolean).join('\n');

    return [
      '<article class="twitter-story-card">',
      '  <div class="twitter-story-rank">' + escapeHtml(rank) + '</div>',
      '  <div class="twitter-story-main">',
      title ? '    <h3 class="twitter-story-title">' + highlightPlainText(title, searchTerm) + '</h3>' : '',
      lead ? '    <p class="twitter-story-summary">' + highlightPlainText(truncateText(cleanPublicLeadText(lead), 360), searchTerm) + '</p>' : '',
      detailsBits
        ? [
            '    <details class="twitter-story-details">',
            '      <summary>Full analysis</summary>',
            detailsBits,
            '    </details>',
          ].join('\n')
        : '',
      '  </div>',
      '</article>',
    ].filter(Boolean).join('\n');
  }).join('\n');
}

export function sanitizePublicReportMarkdown(md: string): string {
  const lines = md.split('\n');
  const out: string[] = [];
  let skippingInternalSection = false;
  let skippingInternalStory = false;
  const internalToolLeak =
    /\b(?:bird-fast|bird)\b.*(?:HTTP\s*403|Cloudflare|cookie|auth|User not found|\[err\]|returned|failed|blocked|degraded)/i;
  const internalAccessNote =
    /(?:Twitter access degraded|access restoration|cookie-clearance|not independently re-verifiable|0 successful bird|successful bird-fast|degraded-access)/i;

  for (const line of lines) {
    if (/^###\s+Research notes\b/i.test(line)) {
      skippingInternalSection = true;
      skippingInternalStory = false;
      continue;
    }
    if (skippingInternalSection && /^##\s+/.test(line)) {
      skippingInternalSection = false;
    } else if (skippingInternalSection) {
      continue;
    }

    if (/^####\s+\d+\.\s+.*(?:TWITTER ACCESS DEGRADED|BIRD-FAST HTTP|BIRD HTTP|ACCESS DEGRADED)/i.test(line)) {
      skippingInternalStory = true;
      continue;
    }
    if (skippingInternalStory && /^(?:####\s+\d+\.|###\s+|##\s+)/.test(line)) {
      skippingInternalStory = false;
    } else if (skippingInternalStory) {
      continue;
    }

    if (internalToolLeak.test(line) || internalAccessNote.test(line)) continue;
    out.push(
      line
        .replace(/\bverified bird-fast (?:user-tweets|search|read|tweet|thread)\b/gi, 'verified')
        .replace(/\bre-verified bird-fast (?:user-tweets|search|read|tweet|thread)\b/gi, 're-verified')
        .replace(/\bbird-fast\s+/gi, ''),
    );
  }

  return out.join('\n').replace(/\n{4,}/g, '\n\n\n').trim();
}

function renderTwitterDateNav(options: TwitterReportRenderOptions): string {
  const link = (date: string | null, label: string, cls: string): string => {
    if (!date) {
      return '<span class="twitter-date-link twitter-date-link--disabled ' + cls + '">' + label + '</span>';
    }
    return [
      '<a class="twitter-date-link ' + cls + '" href="/twitter/' + escapeHtml(date) + '" aria-label="' + escapeHtml(label + ' Twitter summary: ' + date) + '">',
      '  <span class="twitter-date-link-label">' + label + '</span>',
      '  <span class="twitter-date-link-date">' + escapeHtml(date) + '</span>',
      '</a>',
    ].join('');
  };
  return [
    '<nav class="twitter-date-nav" aria-label="Twitter summary dates">',
    '  ' + link(options.prevDate, 'Prev day', 'twitter-date-link--prev'),
    '  <div class="twitter-date-current">',
    '    <div class="twitter-date-current-label">Twitter summaries</div>',
    '    <div class="twitter-date-current-date">' + escapeHtml(options.shownDateTitle) + '</div>',
    options.fallbackDate ? '    <div class="twitter-date-current-note">Showing fallback for ' + escapeHtml(options.currentDateStr) + '</div>' : '',
    '  </div>',
    '  ' + link(options.nextDate, 'Next day', 'twitter-date-link--next'),
    '</nav>',
  ].filter(Boolean).join('\n');
}

export function renderTwitterReportHtml(md: string, options: TwitterReportRenderOptions): string {
  const sections = splitSections(sanitizePublicReportMarkdown(md)).reverse();
  const cards: string[] = [renderTwitterDateNav(options)];
  const timelineItems: InfoTimelineItem[] = [];
  const mindshareCycles: TwitterMindshareCycle[] = [];
  if (options.fallbackDate) {
    cards.push(
      '<div class="frontpage-fallback-note">No Twitter report for ' +
        escapeHtml(options.currentDateStr) +
        '. Showing ' +
        escapeHtml(options.fallbackDate) +
        ' instead.</div>',
    );
  }

  for (const section of sections) {
    if (!section.title && (!section.body || /^#\s+.+$/.test(section.body.trim()))) continue;

    const title = section.title || options.currentDateTitle;
    const timeInfo = options.parseUtcTime(section.title, options.currentDateStr);
    const cycleAnchor = 'cycle-' + section.title.replace(/[:\s]/g, '').toLowerCase();
    const cycleSummary = extractCycleSummary(section.body);
    const stories = parseTwitterStories(section.body);
    const displayTime = timeInfo
      ? '<span class="twitter-cycle-time">' + escapeHtml(timeInfo.utc) + '</span><span class="local-time">' + escapeHtml(timeInfo.local) + '</span>'
      : '<span class="twitter-cycle-time">' + escapeHtml(title) + '</span>';
    const leadText = cycleSummary
      ? cleanPublicLeadText(stripMarkdown(cycleSummary))
      : truncateText(cleanPublicLeadText(stripMarkdown(section.body)), 620);
    mindshareCycles.push({
      anchor: cycleAnchor,
      body: section.body,
      lead: leadText,
      recencyWeight: Math.max(1, sections.length - mindshareCycles.length),
      stories,
    });
    timelineItems.push({
      href: '#' + cycleAnchor,
      label: timeInfo ? timeInfo.utc.replace(/\s*UTC$/i, '') : title,
      title: timeInfo ? timeInfo.local : title,
      detail: summarizeTwitterTimeline(leadText, stories, section.body),
    });

    const fallbackBody = section.body
      .replace(/\*\*Cycle summary\*\*:[\s\S]*?(?=\n#{1,3}\s|$)/i, '')
      .replace(/###\s+[^\n]*[Ss]keptic[^\n]*\n[\s\S]*?(?=\n#{2,3}\s|$)/i, '')
      .trim();
    const structuredStoryCards = renderStructuredTwitterStories(section.body, options.searchTerm);
    const storyCards = structuredStoryCards || stories.map((story) => {
      const verification = truncateText(stripMarkdown(extractSectionText(story.body, 'Verification')), 210);
      const watch = truncateText(stripMarkdown(extractSectionText(story.body, 'Watch')), 210);
      const storyIntro = stripMarkdown(storyCurrentLead(story.body))
        .replace(/^[\s\-—–]+/, '')
        .replace(/^the originating\b/i, 'Originating');
      const storySummary = isSourceMethodLead(storyIntro) ? '' : truncateText(cleanPublicLeadText(storyIntro), 360);
      const storyLinks = options.renderSourceChips(story.links, 6);
      const storyHandles = options.renderHandleChips(story.handles, 8);
      return [
        '<article class="twitter-story-card">',
        '  <div class="twitter-story-rank">' + escapeHtml(story.rank) + '</div>',
        '  <div class="twitter-story-main">',
        '    <h3 class="twitter-story-title">' + highlightPlainText(story.title, options.searchTerm) + '</h3>',
        storySummary ? '    <p class="twitter-story-summary">' + highlightPlainText(storySummary, options.searchTerm) + '</p>' : '',
        '    <details class="twitter-story-details">',
        '      <summary>Full analysis</summary>',
        storyLinks || storyHandles ? '      <div class="twitter-story-chips">' + storyLinks + storyHandles + '</div>' : '',
        verification || watch
          ? '      <div class="twitter-story-signals">' +
              (verification ? '<div><span>Verify</span>' + highlightPlainText(verification, options.searchTerm) + '</div>' : '') +
              (watch ? '<div><span>Watch</span>' + highlightPlainText(watch, options.searchTerm) + '</div>' : '') +
            '</div>'
          : '',
        '      <div class="md-content twitter-story-body">' + options.twitterMarkdownToHtml(story.body) + '</div>',
        '    </details>',
        '  </div>',
        '</article>',
      ].filter(Boolean).join('\n');
    }).join('\n');

    const skepticBody = extractSkepticCorner(section.body);
    const skepticHtml = skepticBody
      ? '<div class="ara-callout ara-callout--danger">' + options.twitterMarkdownToHtml(skepticBody) + '</div>'
      : '';

    cards.push(
      [
        '<section id="' + cycleAnchor + '" class="content-card twitter-cycle-card">',
        '  <div class="twitter-cycle-header">',
        '    <div class="twitter-cycle-kicker">' + (timeInfo ? options.clockIcon(timeInfo.localHours, timeInfo.localMinutes) : '') + displayTime + '</div>',
        '  </div>',
        '  <div class="twitter-wire-brief">',
        '    <div>',
        '      <p class="twitter-brief-text">' + highlightPlainText(leadText, options.searchTerm) + '</p>',
        '    </div>',
        '  </div>',
        storyCards ? '  <div class="twitter-story-grid">' + storyCards + '</div>' : '  <div class="md-content twitter-story-body twitter-cycle-fallback">' + options.twitterMarkdownToHtml(fallbackBody) + '</div>',
        skepticHtml,
        '</section>',
      ].join('\n'),
    );
  }

  const mindshareMap = renderTwitterMindshareMap(buildTwitterMindshare(mindshareCycles));
  return '<div class="twitter-report">' + mindshareMap + renderInfoTimeline('twitter-info-timeline', 'Timeline', timelineItems) + cards.join('\n') + '</div>';
}
