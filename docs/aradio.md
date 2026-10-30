# Aradio — the AI situation, on air

Aradio is ARA's rolling audio news station: a short two-host bulletin that
answers **"what is going on in AI right now, and what changed since the last
bulletin?"** An editor agent maintains a persistent **situation board** — a
small set of live storylines — and every bulletin is a spoken read of the
board's latest deltas. Its distinctive input is **spoken primary sources**:
podcasts, YouTube long-form, and earnings calls, where executives, researchers
and investors say things that never become a tweet or a headline.

| | |
|---|---|
| Route | `ara.guzus.xyz/aradio` |
| Producer | `.github/workflows/aradio.yml` (hourly, `:50`) |
| Source lane it adds | `.github/workflows/podcasts.yml` (every 2 h, `:41`) → `research/podcasts/` |
| Editor | `agent-dispatch`, dedicated route `aradio` (isolated adapter) |
| Voice | Gemini 3.8 Flash TTS → `s3://…/audio/aradio/<id>.mp3` |

## How it differs from the daily broadcast

`daily-digest.yml` ends with a 60–90 s two-host clip: a stateless, once-a-day
rewrite of the digest summary. Aradio differs on three axes, and each is the
reason it exists:

| | Daily broadcast | Aradio |
|---|---|---|
| Cadence | once, 00:00 UTC | rolling: within one cycle of new material |
| Editing | stateless rewrite of one summary | stateful: the board is CRUD'd through editor ops |
| Inputs | the digest summary (text lanes) | spoken sources + fresh items from other lanes |

## What "realtime" means here

Aradio is **not** a live stream; its latency is bounded by its sources
(measured 2026-10-30):

- **Earnings filings** — the 8-K/EX-99 release is accepted 27–85 min *before*
  the call. The earnings lane runs every 2 h on weekdays so a filing reaches
  the station within ~3 h.
- **Earnings calls** — Alphabet and Tesla stream calls on their own YouTube
  channels; the replay is up 3–8 min after the call and tuber can transcribe it
  once captions exist. Microsoft/Amazon/Meta/NVIDIA host calls elsewhere.
- **Podcasts / YouTube long-form** — every surveyed full-episode AI podcast is
  on YouTube; the video appears with the audio (AI Daily Brief trails by
  ~13 h). Captions may lag upload, and YouTube rate-limits transcript access.
- **Twitter / model tickets** — every 3 h / daily.

So "realtime" means: **new material reaches the station within one cycle
(≤ 1 h for priority items, ≤ 2 h for routine ones), and the station stays
silent — at zero model or TTS cost — when nothing changed.**

## Pipeline

```
podcasts.yml (model-free, tuber) ───────► research/podcasts/{index.json,YYYY-MM-DD.md}
daily-earnings.yml, hourly-twitter.yml, 24h-model-timeline.yml ──► research/<lane>/
aradio.yml (hourly):
  1. build_aradio_inbox.py   trusted, deterministic: items not yet consumed →
                             .agent-input/aradio/ + trusted copy in $RUNNER_TEMP.
                             GATE (below): stop here unless it says go.
  2. editor (agent-dispatch) reads the inbox + board, writes ONE artifact:
                             .tmp/aradio/edit.json  (ops + optional script)
  3. check_aradio.py         trusted validator; hard errors fail the run,
                             soft errors are repaired and reported.
  4. aradio_tts.py           Gemini TTS → mp3 (only when on_air)
  5. aws s3 cp               audio/aradio/<id>.mp3 (immutable key)
  6. write_aradio_bulletin.py  the ONLY committer for research/aradio/
  7. safe-push; then the job fails if the editor or the audio failed.
```

### The gate (deterministic, before any model runs)

```
new = inbox candidates whose key is not in research/aradio/cursor.json
force (workflow_dispatch input)         → run the editor
no new items                            → stop: "no new material"
any priority item in new                → run the editor now
≥ 110 min since cursor.last_editor_run_at (or never ran) → run the editor
otherwise                               → stop: routine material waits for the 2 h cadence
```

Priority items: earnings filings, earnings-call episodes, and **long-form**
(≥ 10 min) P0 episodes whose transcript is available. Short official clips —
OpenAI posts about one 90–250 s customer testimonial a day as a P0 video — and
metadata-only episodes are routine material that waits for the 2 h cadence.
A stopped gate commits nothing and exits 0.

## Sources come through tuber

Every podcast and video is read through **tuber-api** (`TUBER_API_BASE`,
default `https://tuber-api.guzus.xyz`), the service the YouTube lane already
uses. The lane is **read-only**: it never calls tuber's generation endpoints
(`/summarize`, `/acp/jobs`, `POST /podcast/episode/summarize`) — those spend
model budget on tuber's side.

| Registry `kind` | Discovery | Depth |
|---|---|---|
| `channel` | `GET /api/channel/{channel_id}?count=N` — long-form uploads (no Shorts; live streams are **not** listed) | `GET /api/video/{id}/transcript` |
| `search` | `GET /api/search?q=…&count=N`, keeping **only** results whose `channelId` equals the entry's mandatory `channel_id`. This finds first-party live streams (earnings calls) while third-party re-streams can never enter. | `GET /api/video/{id}/transcript` |
| `podcast` | `GET /api/podcast/episodes?rss=…&count=N` — RSS episodes, exact timestamps, ~80-word notes | metadata and notes only (tuber does not transcribe RSS audio) |

`/api/video/{id}/transcript` never runs ASR on request: it returns a persisted
transcript (YouTube captions, or ASR that tuber's background job already made)
or nothing. It is rate-limited by YouTube (HTTP 500 "temporarily rate-limited
transcript access" on ~half of requests in a burst), so the lane spaces
requests, retries with backoff, and re-tries an episode on later runs.

Curating official channels and named shows — instead of keyword search — is
deliberate: search-based discovery surfaces evergreen and off-topic videos.

### `data/sources/podcasts.json` (registry)

```json
{"id": "dwarkesh", "name": "Dwarkesh Podcast", "kind": "channel",
 "channel_id": "UCXl4i9dYBrFOabk0xGmbkRA", "priority": "P0",
 "tags": ["interviews"], "ai_filter": true, "min_duration_s": 900,
 "include_in_aradio": true}
{"id": "alphabet-earnings-call", "name": "Alphabet earnings call", "kind": "search",
 "query": "Alphabet earnings call", "channel_id": "UC9RZRAPdKRM91k1XwbELJEg",
 "priority": "P0", "tags": ["official", "earnings-call"], "ai_filter": false,
 "min_duration_s": 1800, "include_in_aradio": true}
```

- `ai_filter: true` marks a mixed-topic show (Dwarkesh also publishes
  history episodes): an episode is kept only if its title/notes pass the
  AI-topicality check.
- `min_duration_s` drops clips.
- Use the verified channel IDs, not obvious handles: several handles are
  clips-only (`@BigTechnologyPodcast`) or dormant.

### `research/podcasts/index.json` (lane output; rolling 30 days)

```json
{
  "lane": "podcasts",
  "schema": 1,
  "updated_at": "2026-10-30T08:41:00Z",
  "degraded": false,
  "episodes": [
    {
      "id": "dwarkesh:frYSOKvNiiE",
      "show_id": "dwarkesh",
      "show": "Dwarkesh Podcast",
      "kind": "podcast",
      "priority": "P0",
      "tags": ["interviews", "frontier-labs"],
      "title": "What will computer chips look like in 2045?",
      "url": "https://www.youtube.com/watch?v=frYSOKvNiiE",
      "video_id": "frYSOKvNiiE",
      "audio_url": null,
      "published_at": "2026-10-22T16:00:00Z",
      "published_precision": "approximate",
      "first_seen_at": "2026-10-22T18:41:00Z",
      "duration_s": 4141,
      "transcript": {"available": true, "source": "youtube_captions", "words": 11777,
                     "checked_at": "2026-10-22T18:41:00Z", "attempts": 1},
      "excerpts": [{"text": "≤ 60 words, verbatim", "at_s": 1234,
                    "url": "https://www.youtube.com/watch?v=frYSOKvNiiE&t=1234s"}],
      "description": "≤ 80 words of show notes, or empty"
    }
  ]
}
```

- `id` is `<show_id>:<video id>` (channel/search) or `<show_id>:<tuber pod-… id>`
  (podcast); stable across runs.
- `kind` is the listener-facing class: `earnings-call` for a show tagged
  `earnings-call` (this wins over `official`), `video` for one tagged
  `official` (lab launches), otherwise `podcast`.
- `url` is the YouTube watch URL, built only from an 11-character video id; for
  an RSS episode it is the audio file (tuber returns no episode page), else the
  feed URL. Every third-party URL passes `safe_url()` first (http/https, a host,
  no whitespace, control characters or Markdown-breaking punctuation) or is
  dropped.
- `published_at` is exact for RSS podcasts. For YouTube it is the MIDPOINT of
  the range tuber's rounded-down relative label implies ("Streamed 1d ago" =
  24–48 h), which keeps the error ≤ 30 min for episodes seen within a 2 h run.
- `first_seen_at` is set once and never changes.
- An episode without a transcript is retried on later runs while it is
  < 3 days old (`attempts` counts tries; at most 12 fetches per run, spaced,
  and the run stops fetching after repeated YouTube throttling).
  `transcript.available` is false for non-English tracks and fragments.
- `updated_at` changes only when content changes, so a quiet run is a
  no-op commit. `degraded` is true when more than half the sources failed.
- The daily `YYYY-MM-DD.md` is written on the first run of each UTC day even
  when nothing is new, so the 30 h freshness SLO does not page on a quiet day.
- Exit codes: 0 ok; 2 bad arguments/registry; 3 every source failed (nothing
  written); 4 tuber's relative-age labels stopped parsing (nothing written —
  the YouTube lane's 2026-09-29 failure, made loud).
- `/api/channel` omits past livestreams, so channels that stream full episodes
  (OpenAI keynotes, Cognitive Revolution) also have a channel-constrained
  `search` entry; a video found twice is owned by the first registry entry.
  Liveness and age come only from listings: `/api/video/{id}` reports
  `isLive: true` for any past stream and can carry a stale `publishDate`.
- **Transcript text is never committed.** At most 6 excerpts of ≤ 60 words per
  episode — the earnings lane's quote policy. Everything under `research/` is
  published by the dashboard prebuild, so committing a transcript would be
  republishing it.

Shared helper (owned by `scripts/fetch_podcast_signal.py`, imported by the
inbox builder):

```python
def select_windows(segments: list[dict], *, max_windows: int, max_words: int,
                   min_gap_s: int = 120) -> list[dict]:
    """segments = tuber transcript segments [{"startMs": int, "text": str}].
    Returns ≤ max_windows non-overlapping windows [{"text": str, "at_s": int}]
    of ≤ max_words words each, highest-information first by score, then
    re-sorted by at_s. Deterministic; sponsor reads and intros/outros score low."""
```

## Inbox (`.agent-input/aradio/`, never committed)

| File | Content |
|---|---|
| `inbox.md` | the new items, rendered for the editor, priority first |
| `inbox.json` | the same items, machine-readable |
| `board.json` | a copy of `research/aradio/state.json` (or an empty board) |
| `context.json` | `now`, `last_bulletin_at`, `last_headline`, limits |
| `transcripts/<n>.txt` | top transcript windows (`[mm:ss] text`) for spoken items |

The trusted copy of `inbox.json` (with the same `transcripts/`, used to verify
quotes) read by the validator and writer lives in `$RUNNER_TEMP`, never under
`.tmp/` (the import path) or `.agent-input/`.

Item shape:

```json
{"key": "ep:dwarkesh:frYSOKvNiiE", "kind": "podcast", "priority": true,
 "source": "Dwarkesh Podcast", "title": "…", "url": "https://…",
 "at": "2026-10-22T16:00:00Z", "text": "bounded body", "links": ["https://…"],
 "transcript_file": "transcripts/3.txt"}
```

| Source | Key | Eligible when |
|---|---|---|
| `research/podcasts/index.json` | `ep:<episode id>` | published (else first seen) in the last 7 days, and transcript available or first seen ≥ 6 h ago without one |
| `research/earnings/index.json` + event `.md` | `earn:<accession>` | filed in the last 3 days |
| `research/twitter/<date>.md` stories | `tw:<first source URL>` | run section in the last 26 h |
| `research/models/tickets/*.md` | `tk:<slug>:<history length>` | last history entry in the last 2 days |

Caps: ≤ 40 items (priority first, then newest), ≤ 8 transcript files of
≤ 20 windows × ≤ 70 words, total ≤ 400 KB. A transcript fetch failure falls
back to the committed excerpts.

The 7-day episode bound keeps a first run (or a newly registered show's back
catalogue) from flooding the inbox with old priority items, and keeps an
episode whose cursor key expired (21 days) from being re-offered by the
30-day podcast index.

## Editor output: `.tmp/aradio/edit.json`

The editor never rewrites the board. It emits **ops**; the writer applies
them, so history cannot be corrupted by a bad rewrite.

```json
{
  "schema": 1,
  "on_air": true,
  "headline": "≤ 140 chars: the situation in one line",
  "ops": [
    {"op": "create", "slug": "anthropic-ipo", "title": "…", "status": "developing",
     "importance": 5, "now": "…", "changed": "…", "watch": "…",
     "evidence": [{"url": "https://…", "label": "…", "speaker": "…", "quote": "…"}],
     "change": "history line"},
    {"op": "update", "slug": "hbm-shortage", "status": "escalating", "now": "…",
     "changed": "…", "watch": "…", "importance": 4,
     "add_evidence": [{"url": "https://…", "label": "…"}], "change": "history line"},
    {"op": "resolve", "slug": "devday-launches", "changed": "…", "change": "history line"}
  ],
  "script": ["Speaker 1: …", "Speaker 2: …"],
  "covers": ["anthropic-ipo", "hbm-shortage"],
  "note": "optional, ≤ 300 chars — e.g. why on_air is false"
}
```

`update` fields other than `slug`, `changed`, `change` are optional.
`on_air: false` is a legitimate editorial decision ("nothing material"): ops
still apply, consumed keys are still recorded, no audio is made. The editor's
prompt is `prompts/aradio-editor.md`.

## Validation (`scripts/check_aradio.py`)

**Hard errors** (exit 1, nothing published, cursor not advanced, so the next
run retries the same material): invalid JSON or schema; unknown op; `create`
of an existing slug or a malformed slug (`^[a-z0-9]+(-[a-z0-9]+)*$`, ≤ 64);
`update`/`resolve` of an unknown slug; more than 3 creates; `on_air` with a
missing or malformed script (a line not matching `^Speaker [12]: \S`, < 8 or
> 30 lines, < 250 or > 900 words); `covers` naming a slug that is not on the
board after the ops.

**URL rule** (every boundary: inbox items, evidence, published files). A URL is
usable only if `urllib.parse.urlsplit` gives an `http`/`https` scheme and a
non-empty hostname, it carries no credentials (`user:pass@`) and no malformed
port, it has no whitespace and no Unicode control/format (`C*`) characters
(which covers bidi overrides), none of `` <>"'()[]{}|\^` ``, and it is at most
2,048 characters. `check_aradio.safe_url` and `fetch_podcast_signal.safe_url`
implement the identical rule; a parity test keeps them in lockstep. The inbox drops
failing URLs (an item whose URL fails keeps `url: null` and stays usable as
text; a Twitter story with no passing URL gets a `tw:sha256:…` key); the
validator drops failing evidence even if the inbox lists it; the writer drops
failing evidence already on the board and refuses to write any `url` field
that fails. URL-like text and markdown links are stripped from prose fields
and the script, and diagnostics (`warnings`) carry a `url#<hash>` fingerprint
instead of the URL. `inbox.md` renders URLs as `<…>` autolinks; the validator
accepts a cited URL with or without the brackets.

**Soft errors** (repaired, listed in the bulletin's `warnings`): an evidence
URL not present in this run's inbox (`url`/`links`) or already on the board is
**dropped** — the editor cannot introduce a URL; a `quote` over 40 words, or
one that is not ONE contiguous verbatim span (case- and punctuation-folded)
inside a single segment of the owning item — its title, one line of its text,
or one transcript window — is dropped. The URL rule alone cannot stop a
fabricated quote attributed to a real source, and fragment matching cannot
either: ellipses, or a match that crosses a line or window boundary, would let
a "verbatim" quote be stitched from words spoken minutes apart. Over-long text fields are
truncated; unknown audio tags and URLs in the script are stripped. Evidence
`kind` (and `at`) are set from the inbox item that owns the URL, never trusted
from the editor.

## Writer rules (`scripts/write_aradio_bulletin.py`)

1. Applies ops: `create` → new thread (`first_seen` = now, history = [change]);
   `update` → patch given fields, prepend new evidence (dedupe by URL, keep 8),
   append history; `resolve` → status `resolved`, append history. Threads not
   named are untouched.
2. Keeps the board bounded: unresolved threads untouched for 7 days are
   auto-resolved ("went quiet"); if more than 10 remain unresolved, the
   least-recently-updated lowest-importance ones are auto-resolved ("board
   full"). Resolved threads idle for 7 days move to
   `research/aradio/archive/YYYY-MM.json`.
3. Records every inbox key as consumed (`cursor.json`), plus
   `last_editor_run_at` and, when on air, `last_bulletin_at`.
4. Writes atomically (temp file + `os.replace`), stages exact paths only
   (`.agent-input/` and `.tmp/` are not gitignored), commits
   `Aradio bulletin YYYY-MM-DD HH:MM UTC` or `Aradio board update …`.

## Published files (`research/aradio/`)

- `state.json` — the board:
  `{schema, updated_at, headline, threads: [Thread]}` where Thread is
  `{slug, title, status, importance, first_seen, updated_at, now, changed,
  watch, evidence: [{url, kind, label, at?, speaker?, quote?}],
  history: [{at, change}]}`;
  `status` ∈ `developing | escalating | steady | resolved`, `importance` 1–5,
  evidence `kind` ∈ `podcast | video | earnings-call | earnings | twitter | ticket`.
- `bulletins/YYYY-MM-DD/HHMM.json` — one per aired bulletin:
  `{schema, id, aired_at, headline, lines: [{speaker, text}], script,
  covers, threads: [{slug, title, status}], sources: [{url, kind, label}],
  ops: [{op, slug}], warnings, audio: {key, bytes, duration_s} | null,
  audio_error, editor: {backend, model}, inbox: {items, kinds}}`.
  `lines` is display-ready (audio tags stripped; `speaker` is `"Speaker 1"` or
  `"Speaker 2"`); `script` is the raw TTS input.
- `index.json` — `{schema, updated_at, degraded, latest, bulletins: [{id,
  aired_at, headline, path, audio, covers, kinds}]}`, newest first, ≤ 72.
  `degraded` is true when the latest on-air bulletin has no audio. `latest` is
  the newest bulletin `id` (null before the first); `path` is relative to
  `research/aradio/`. The writer creates an empty index on the first editor
  run so the freshness watchdog's `degraded` signal always has a file to read.
- `cursor.json` — `{schema, updated_at, last_editor_run_at,
  last_bulletin_at, keys: {key: consumed_at}}`, keys pruned after 21 days.
- `archive/YYYY-MM.json` — archived resolved threads.

Bulletin `id` is the UTC run stamp `YYYY-MM-DD-HHMM`.

## Audio (Gemini 3.8 Flash TTS)

Same model and voices as the daily broadcast (Speaker 1 = Charon, Speaker 2 =
Puck), via the Interactions API, using only fields in the documented REST
schema (no `speech_config.mode`). Limits (2026-10-30,
<https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-tts>): 8,192
input tokens and 16,384 output tokens at 25 audio tokens/s, ≈ 10.9 min of audio
per request, at most 2 prebuilt voices. Scripts are capped at 900 words
(≈ 4.8 min at the measured ~188 wpm), so one request suffices. A response
shorter than 60 % of the expected duration is treated as truncated and
fails — truncated audio is never published.

Cost: $9 per 1M audio-output tokens until 2026-12-31, $18 from 2027-01-01. A
4-minute bulletin is ~6,000 audio tokens ≈ $0.054 (≈ $0.11 from January).

S3: only the `audio/` prefix is publicly readable, so keys are
`audio/aradio/<id>.mp3`. s3.guzus.xyz sits behind Cloudflare and caches 200s
for 4 h, so keys are immutable — never overwrite one; the "latest" pointer is
`research/aradio/index.json`, which Caddy serves uncached.

**Audio failure is loud.** The text (board + bulletin with `audio: null` and
`audio_error`) still publishes; then the job fails. The daily broadcast's
`continue-on-error` TTS step that exits 0 on Gemini errors — silently missing
since 2026-10-22 — is the anti-pattern this avoids.

## Dashboard

`/aradio`: the latest bulletin with a player (`${AUDIO_BASE}/${audio.key}`), an
ON AIR indicator when the latest bulletin is < 2 h old, the situation board
(threads with status, importance, now/changed/watch, evidence chips by kind),
the bulletin transcript, and the last 72 bulletins. The page polls
`research/aradio/index.json` every 5 minutes and offers newer bulletins as they
air. Missing files (before the first run) render an empty state.
