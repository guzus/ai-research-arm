import './style.css';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

const DATA_BASE: string = import.meta.env.BASE_URL + 'research';

const TWITTER_ICON =
  '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">' +
  '<path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>';

const DOC_ICON =
  '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">' +
  '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>' +
  '<path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>';

// ── State ─────────────────────────────────────────────
let currentDate = new Date();
let searchTerm = '';

// ── DOM refs ──────────────────────────────────────────
const content = document.getElementById('content')!;
const datePicker = document.getElementById('datePicker') as HTMLInputElement;
const searchInput = document.getElementById('searchInput') as HTMLInputElement;

// ── Helpers ───────────────────────────────────────────
function fmtDate(d: Date): string {
  return d.toISOString().slice(0, 10);
}

function displayDate(d: Date): string {
  return d.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function shiftDate(days: number): void {
  currentDate.setDate(currentDate.getDate() + days);
  datePicker.value = fmtDate(currentDate);
  load();
}

function escapeHtml(str: string): string {
  const div = document.createElement('div');
  div.textContent = str;
  return div.textContent ?? '';
}

/** Safely set element content using DOMPurify + insertAdjacentHTML */
function setSafeContent(el: HTMLElement, rawHtml: string): void {
  while (el.firstChild) el.removeChild(el.firstChild);
  const clean = DOMPurify.sanitize(rawHtml, {
    USE_PROFILES: { html: true, svg: true, svgFilters: true },
    ADD_TAGS: ['mark'],
  });
  el.insertAdjacentHTML('beforeend', clean);
}

// ── Fetch ─────────────────────────────────────────────
async function fetchTwitter(dateStr: string): Promise<string | null> {
  const url = `${DATA_BASE}/twitter/${dateStr}.md`;
  try {
    const resp = await fetch(url);
    if (!resp.ok) return null;
    return await resp.text();
  } catch {
    return null;
  }
}

// ── Rendering ─────────────────────────────────────────
function showLoading(): void {
  setSafeContent(
    content,
    [
      '<div class="content-card">',
      '  <div class="loading-indicator">',
      '    <div class="loading-bar"><div class="loading-bar-inner"></div></div>',
      '    <div class="loading-text">Loading Twitter report\u2026</div>',
      '  </div>',
      '</div>',
    ].join('\n'),
  );
}

function showEmpty(dateStr: string): void {
  setSafeContent(
    content,
    [
      '<div class="content-card">',
      '  <div class="empty-state">',
      '    <div class="empty-state-icon">' + DOC_ICON + '</div>',
      '    <div class="empty-state-text">No Twitter report for ' + escapeHtml(dateStr) + '</div>',
      '  </div>',
      '</div>',
    ].join('\n'),
  );
}

/** Split markdown by ## headings into separate sections */
function splitSections(md: string): { title: string; body: string }[] {
  const lines = md.split('\n');
  const sections: { title: string; body: string }[] = [];
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

function renderReport(md: string): void {
  const sections = splitSections(md);
  const cards: string[] = [];

  for (const section of sections) {
    // Skip the top-level h1 title section if it has no body
    if (!section.title && !section.body) continue;

    let html = marked.parse(section.body) as string;

    if (searchTerm) {
      const escaped = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const re = new RegExp('(' + escaped + ')', 'gi');
      html = html.replace(re, '<mark>$1</mark>');
    }

    // Use the ## heading as the card title, or fall back to date
    const title = section.title || escapeHtml(displayDate(currentDate));

    cards.push(
      [
        '<div class="content-card">',
        '  <div class="content-card-header">',
        '    <div class="content-card-icon">' + TWITTER_ICON + '</div>',
        '    <div class="content-card-title">' + escapeHtml(title) + '</div>',
        '  </div>',
        '  <div class="content-card-body">',
        '    <div class="md-content">' + html + '</div>',
        '  </div>',
        '</div>',
      ].join('\n'),
    );
  }

  setSafeContent(content, cards.join('\n'));
}

// ── Main load ─────────────────────────────────────────
async function load(): Promise<void> {
  const dateStr = fmtDate(currentDate);
  showLoading();
  const md = await fetchTwitter(dateStr);
  if (md) {
    renderReport(md);
  } else {
    showEmpty(dateStr);
  }
}

// ── Events ────────────────────────────────────────────
datePicker.value = fmtDate(currentDate);

document.getElementById('prevDay')!.addEventListener('click', () => shiftDate(-1));
document.getElementById('nextDay')!.addEventListener('click', () => shiftDate(1));
document.getElementById('todayBtn')!.addEventListener('click', () => {
  currentDate = new Date();
  datePicker.value = fmtDate(currentDate);
  load();
});

datePicker.addEventListener('change', () => {
  const parts = datePicker.value.split('-');
  currentDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
  load();
});

searchInput.addEventListener('input', () => {
  searchTerm = searchInput.value.trim();
  load();
});

document.getElementById('refreshBtn')!.addEventListener('click', () => {
  const btn = document.getElementById('refreshBtn')!;
  btn.classList.add('spinning');
  load().then(() => setTimeout(() => btn.classList.remove('spinning'), 500));
});

// Keyboard shortcuts
document.addEventListener('keydown', (e: KeyboardEvent) => {
  if ((e.target as HTMLElement).tagName === 'INPUT') return;
  switch (e.key) {
    case '[':
      shiftDate(-1);
      break;
    case ']':
      shiftDate(1);
      break;
    case 't':
    case 'T':
      currentDate = new Date();
      datePicker.value = fmtDate(currentDate);
      load();
      break;
    case '/':
      e.preventDefault();
      searchInput.focus();
      break;
    case 'r':
    case 'R':
      load();
      break;
  }
});

// ── Init ──────────────────────────────────────────────
load();
