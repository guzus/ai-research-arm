// Pure helpers shared by the SEO postbuild and its tests. Forecast pages are
// deliberately limited to tickets with a valid prediction-market mapping:
// ordinary model tickets stay on the board and do not become thin indexable
// pages merely because they exist.

const SLUG_RE = /^[a-z0-9]+(?:[a-z0-9._-]*[a-z0-9])?$/;

function compact(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function validMapping(mapping) {
  return !!mapping && typeof mapping === 'object' &&
    ['event_slug', 'market_id', 'token_id', 'question']
      .every(key => compact(mapping[key]).length > 0);
}

export function mappedForecastTickets(index) {
  const tickets = Array.isArray(index?.tickets) ? index.tickets : [];
  return tickets
    .filter(ticket =>
      ticket && typeof ticket === 'object' &&
      SLUG_RE.test(compact(ticket.slug)) &&
      compact(ticket.title) &&
      ticket.verification === 'confirmed' &&
      Array.isArray(ticket.polymarket) &&
      ticket.polymarket.length > 0 &&
      ticket.polymarket.slice(0, 3).every(validMapping))
    .map(ticket => ({ ...ticket, polymarket: ticket.polymarket.slice(0, 3) }))
    .sort((a, b) => compact(a.slug).localeCompare(compact(b.slug)));
}

export function forecastRoute(slug) {
  if (!SLUG_RE.test(compact(slug))) throw new TypeError('invalid forecast slug');
  return `/models/forecast/${compact(slug)}`;
}

export function forecastSeoRecord(ticket, siteOrigin) {
  const route = forecastRoute(ticket.slug);
  const questions = ticket.polymarket.map(mapping => compact(mapping.question));
  const title = `${compact(ticket.title)} forecast`;
  const company = compact(ticket.company) || 'AI model';
  const status = compact(ticket.status).replace(/-/g, ' ') || 'tracked';
  const updated = compact(ticket.updated_at);
  const marketSummary = questions.length === 1
    ? `Linked prediction market: ${questions[0]}`
    : `${questions.length} linked prediction markets, including: ${questions[0]}`;
  const marketSentence = /[.!?]$/.test(marketSummary) ? marketSummary : `${marketSummary}.`;
  const dateSummary = updated ? ` Updated ${updated}.` : '';
  return {
    route,
    url: `${String(siteOrigin).replace(/\/+$/, '')}${route}`,
    title,
    description: `${company} model-release forecast (${status}). ${marketSentence}${dateSummary}`,
    questions,
  };
}
