import { marked } from 'marked';
import {
  escapeHtml,
  isModelReleaseDigestSection,
  sectionAnchorId,
  splitSections,
  wrapTables,
} from './shared';

export type TodayRenderOptions = {
  md: string;
  dateStr: string;
  fallbackTitle: string;
  audioBase: string;
  audioDates: string[];
  searchTerm: string;
  frontPageCardHtml: string | null;
};

/** Render the daily digest. Treats Executive Summary specially as a TL;DR block.
 * When `frontPageCardHtml` is supplied the layout splits into two desktop
 * columns: front page on the left, digest cards on the right. */
export function renderTodayHtml(options: TodayRenderOptions): string {
  const sections = splitSections(options.md);

  // Digest files often start with `# AI Daily Digest - <date>` before the
  // first `## Section`, which duplicates the date already shown in the
  // card header. Strip the leading h1 from the pre-`##` body; if nothing
  // else remains, drop the section so we don't render a blank card.
  if (sections.length > 0 && !sections[0].title) {
    sections[0].body = sections[0].body.replace(/^\s*#\s+[^\n]+\n*/, '').trim();
    if (!sections[0].body) sections.shift();
  }

  const cards: string[] = [];

  if (options.audioDates.includes(options.dateStr)) {
    const audioUrl = `${options.audioBase}/audio/${options.dateStr}-digest.mp3`;
    cards.push(
      [
        '<div class="today-audio">',
        '  <audio controls preload="metadata" style="width:100%;" src="' + audioUrl + '">',
        '    Your browser does not support the audio element.',
        '  </audio>',
        '</div>',
      ].join('\n'),
    );
  }

  let sectionIndex = 0;
  for (const section of sections) {
    if (!section.title && !section.body) continue;
    if (section.title && isModelReleaseDigestSection(section.title)) continue;

    const isSummary = /^(executive summary|tl;dr|tldr|summary)$/i.test(section.title.trim());
    const title = section.title || options.fallbackTitle;
    const anchorId = sectionAnchorId('today', isSummary ? 'tl-dr' : title, sectionIndex);
    sectionIndex += 1;

    let html = marked.parse(section.body) as string;
    html = wrapTables(html);

    html = html.replace(
      /(?<!\w)(@\w+)/g,
      '<span class="handle">$1</span>',
    );

    if (options.searchTerm) {
      const escaped = options.searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const re = new RegExp('(' + escaped + ')', 'gi');
      html = html.replace(re, '<mark>$1</mark>');
    }

    if (isSummary) {
      cards.push(
        [
          '<div id="' + anchorId + '" class="content-card today-card">',
          '  <div class="content-card-body">',
          '    <div class="today-tldr">',
          '      <span class="today-tldr-label">TL;DR</span>',
          '      <div class="md-content">' + html + '</div>',
          '    </div>',
          '  </div>',
          '</div>',
        ].join('\n'),
      );
    } else {
      cards.push(
        [
          '<div id="' + anchorId + '" class="content-card">',
          '  <div class="content-card-header">',
          '    <div class="content-card-title">' + escapeHtml(title) + '</div>',
          '  </div>',
          '  <div class="content-card-body">',
          '    <div class="md-content">' + html + '</div>',
          '  </div>',
          '</div>',
        ].join('\n'),
      );
    }
  }

  const todayCards = cards.join('\n');
  if (!options.frontPageCardHtml) return todayCards;

  return [
    '<div class="today-layout">',
    '  <div class="today-layout-frontpage">' + options.frontPageCardHtml + '</div>',
    '  <div class="today-layout-digest">' + todayCards + '</div>',
    '</div>',
  ].join('\n');
}
