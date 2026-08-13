import {
  escapeHtml,
  isModelReleaseDigestSection,
  renderReportMarkdown,
  sectionAnchorId,
  splitSections,
  wrapTables,
} from './shared';
import { uiText, type UiLanguage } from '../i18n';

export type TodayRenderOptions = {
  md: string;
  dateStr: string;
  fallbackTitle: string;
  audioDates: string[];
  searchTerm: string;
  frontPageCardHtml: string | null;
  language: UiLanguage;
};

/** Drop the first top-level list item from a markdown block, keeping any of
 * its wrapped continuation lines with it. Returns the input unchanged when
 * there is no leading bullet, so a paragraph-style summary is never gutted. */
function dropFirstBullet(md: string): string {
  const lines = md.split('\n');
  const start = lines.findIndex((l) => /^\s*[-*]\s+/.test(l));
  if (start === -1) return md;
  let end = start + 1;
  while (end < lines.length && !/^\s*[-*]\s+/.test(lines[end]) && lines[end].trim()) {
    end += 1;
  }
  return [...lines.slice(0, start), ...lines.slice(end)].join('\n').trim();
}

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
    cards.push(
      [
        '<div class="today-audio">',
        '  <button class="today-audio-play" type="button" data-digest-audio-play data-audio-date="' + escapeHtml(options.dateStr) + '" aria-pressed="false">',
        '    <span class="today-audio-play-icon" aria-hidden="true"></span>',
        '    <span class="today-audio-play-copy">',
        '      <span class="today-audio-play-label" data-digest-audio-label>' + uiText(options.language, 'today.playAudio') + '</span>',
        '      <span class="today-audio-play-date">' + escapeHtml(options.fallbackTitle) + '</span>',
        '    </span>',
        '  </button>',
        '</div>',
      ].join('\n'),
    );
  }

  let sectionIndex = 0;
  for (const section of sections) {
    if (!section.title && !section.body) continue;
    if (section.title && isModelReleaseDigestSection(section.title)) continue;

    const isSummary = /^(executive summary|tl;dr|tldr|summary)$/i.test(section.title.trim());

    // The front page's headline and standfirst ARE the first Executive
    // Summary bullet (render_front_page.mjs builds them from it), so with
    // both columns on screen the reader met the same sentence twice — once
    // at masthead size on the left, once as bullet one on the right. Drop it
    // from the TL;DR when the front page is showing it; no information is
    // lost, it just stops being said twice.
    if (isSummary && options.frontPageCardHtml) {
      section.body = dropFirstBullet(section.body);
      if (!section.body.trim()) continue;
    }
    const title = section.title || options.fallbackTitle;
    const anchorId = sectionAnchorId('today', isSummary ? 'tl-dr' : title, sectionIndex);
    sectionIndex += 1;

    let html = renderReportMarkdown(section.body);
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
