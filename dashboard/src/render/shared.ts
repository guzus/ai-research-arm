import { Marked } from 'marked';

export type InfoTimelineItem = {
  href: string;
  label: string;
  title: string;
  detail: string;
};

export type MarkdownSection = {
  title: string;
  body: string;
};

const reportMarked = new Marked({
  gfm: true,
  breaks: false,
  tokenizer: {
    // Report prose uses "~" as approximation syntax ("~$7B", "~40%").
    // marked's GFM strikethrough accepts single tildes, which can cross whole
    // sentences when two approximations appear in one line.
    del() {
      return undefined;
    },
  },
});

export function renderReportMarkdown(md: string): string {
  return reportMarked.parse(md) as string;
}

export function escapeHtml(str: string): string {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

export function sectionAnchorId(prefix: string, title: string, index: number): string {
  const slug = title
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48);
  return prefix + '-' + String(index + 1).padStart(2, '0') + (slug ? '-' + slug : '');
}

export function isModelReleaseDigestSection(title: string): boolean {
  return /\b(?:new\s+)?model\s+releases?\b/i.test(title) || /\bmodel\s+releases?\s*(?:&|and)\s*updates?\b/i.test(title);
}

export function renderInfoTimeline(className: string, label: string, items: InfoTimelineItem[]): string {
  if (items.length === 0) return '';
  return [
    '<nav class="info-timeline ' + className + '" aria-label="' + escapeHtml(label) + ' timeline">',
    '  <div class="info-timeline-head">' + escapeHtml(label) + '</div>',
    '  <ol class="info-timeline-list">',
    items.map((item) => [
      '    <li class="info-timeline-item">',
      '      <a href="' + escapeHtml(item.href) + '">',
      '        <time>' + escapeHtml(item.label) + '</time>',
      '        <span>' + escapeHtml(item.detail || item.title) + '</span>',
      '      </a>',
      '    </li>',
    ].join('\n')).join('\n'),
    '  </ol>',
    '</nav>',
  ].join('\n');
}

/** Split markdown by ## headings into separate sections */
export function splitSections(md: string): MarkdownSection[] {
  const lines = md.split('\n');
  const sections: MarkdownSection[] = [];
  let currentTitle = '';
  let currentLines: string[] = [];

  for (const line of lines) {
    const h2Match = line.match(/^## (.+)/);
    if (h2Match) {
      if (currentTitle || currentLines.length) {
        sections.push({ title: currentTitle, body: currentLines.join('\n').trim() });
      }
      currentTitle = h2Match[1];
      currentLines = [];
    } else {
      currentLines.push(line);
    }
  }
  if (currentTitle || currentLines.length) {
    sections.push({ title: currentTitle, body: currentLines.join('\n').trim() });
  }
  return sections;
}

/** Wrap rendered tables in a horizontally scrollable container so wide tables
 * (many columns or long cell content) don't overflow the card. */
export function wrapTables(html: string): string {
  return html
    .replace(/<table(\s[^>]*)?>/g, '<div class="md-table-wrap"><table$1>')
    .replace(/<\/table>/g, '</table></div>');
}

export function stripMarkdown(md: string): string {
  return md
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/!\[[^\]]*]\([^)]+\)/g, ' ')
    .replace(/\[([^\]]+)]\([^)]+\)/g, '$1')
    .replace(/https?:\/\/\S+/g, ' ')
    .replace(/[#>*_`~|]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export function truncateText(text: string, max = 360): string {
  if (text.length <= max) return text;
  const sliced = text.slice(0, max).replace(/\s+\S*$/, '').trim();
  return sliced + '...';
}

export function cleanPublicLeadText(text: string): string {
  return text
    .replace(/\([^)]*\b(?:verified|curl|re-verified|source checks?|multi-source primary-source confirmed)[^)]*\)/gi, '')
    .replace(/\b(?:verified|re-verified|confirmed)\s+(?:via|by)\s+(?:curl|source checks?|snapshot)[^.;—]*[.;—]?\s*/gi, '')
    .replace(/\s+/g, ' ')
    .trim();
}

export function isSourceMethodLead(text: string): boolean {
  return /\b(?:verified|curl|source checks?|originating .*source|confirmed via|post body|press-release teaser|raw URL|snapshot)\b/i.test(text);
}

export function extractUrls(md: string): string[] {
  const urls = new Set<string>();
  const re = /https?:\/\/[^\s)>\]]+/g;
  let match: RegExpExecArray | null;
  while ((match = re.exec(md))) {
    urls.add(match[0].replace(/[.,;:]+$/, ''));
  }
  return Array.from(urls);
}

export function extractHandles(md: string, limit = 12): string[] {
  const handles = new Set<string>();
  const re = /(?<!\w)@([A-Za-z0-9_]{2,20})/g;
  let match: RegExpExecArray | null;
  while ((match = re.exec(md)) && handles.size < limit) {
    handles.add('@' + match[1]);
  }
  return Array.from(handles);
}
