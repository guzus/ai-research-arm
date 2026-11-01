# Aradio — ARA AI News

Aradio is ARA's rolling audio news station: a short two-host bulletin that
answers **"what is going on in AI right now, and what changed since the last
bulletin?"** An editor agent maintains a persistent **situation board** — a
small set of live storylines — and every bulletin is a spoken read of the
board's latest deltas. Its distinctive input is **spoken primary sources**:
podcasts, YouTube long-form, and earnings calls, where executives, researchers
and investors say things that never become a tweet or a headline.

| | |
|---|---|
| Route | `ara.guzus.xyz/aradio` (the "ARA AI News" player) |
| Podcast feed | `ara.guzus.xyz/aradio/feed.xml` (built at deploy, see "Dashboard") |
| Producer | `.github/workflows/aradio.yml` (whenever an input lane finishes, plus an hourly `:50` backstop; see "Triggers") |
| Source lane it adds | `.github/workflows/podcasts.yml` (every 2 h, `:41`) → `research/podcasts/` |
| Editor | `agent-dispatch`, dedicated route `aradio` (isolated adapter; since 2026-10-31 the isolated Claude Code container on `claude-sonnet-5-5` under `.github/claude/aradio.json`: read the staged inbox, write the one ops file, nothing else) |
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
aradio.yml (when an input lane finishes; hourly backstop):
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

### Triggers

| Trigger | Why |
|---|---|
| `workflow_run` `completed` on `main` of "Podcast Signal", "Daily Earnings Signal", "Twitter AI News (hourly matrix)" and "Hyperscaler Model Release Timeline (Every 24 Hours)" | The four lanes the inbox reads (podcasts and YouTube channels, earnings, Twitter stories, model tickets). The station wakes when its picture changes. A test pins the list to the registry producers of what the gate reads. |
| `schedule` `50 * * * *` | Backstop: routine material that waited for the 2 h cadence airs within the next hour even when no lane finishes. |
| `workflow_dispatch` (`force`) | Manual run; `force` bypasses the gate. |

Any completed lane run from this repository wakes the job, whatever its
conclusion: a lane can publish and then fail a later step (Twitter's headline
alerts run after its push), and a stop is model-free. A run from another
repository's fork is skipped. Under `workflow_run`, `github.ref` is the
default branch, so the main-only guard passes, and secrets and permissions are
as for a scheduled run. Concurrency stays single-writer and without
cancel-in-progress. GitHub keeps one pending run per group and cancels the
older one, so a burst of triggers is one running run plus one pending, and the
pending run reads the branch tip when it starts. A run that can never write
takes a group of its own (`aradio-isolated-<run id>`), so it can never
displace a real pending run: a lane run from a fork, which the job skips, or
a dispatch from another branch, which the ref guard refuses. A forced
dispatch can be displaced by a real run, though: a lane's run queued
behind it cancels it, and `force` would be lost without a word. So a forced
dispatch is named "Aradio (forced)" (`run-name`), and the history step looks
for a run with that name that ended cancelled without starting, a second or
so after another run was queued (the one that displaced it). The force stays
pending until an editor runs after it: in a bulletin stamped later, or in a
later run whose editor step ran (the jobs API shows which steps ran). The
first run that finds it pending honours it. So exactly one editor run spends
it, even one that then hangs past `timeout-minutes` or is a re-run, and a run
that fails before its editor passes it on. Serialization is untouched. Runs
are ordered by `run_started_at`, when their latest attempt was queued: a
re-run keeps its `created_at`. A re-run never honours a force: its first
attempt had that chance. A forced run cancelled by hand while it waited had
no run queued behind it, so it is not honoured. Gate stops report to
Hooker once per UTC hour (`aradio-stop-<hour>` idempotency key), so the extra
wake-ups do not add telemetry.

Cost: if GitHub fired every trigger on a weekday, that would be 57 runs (24
cron, 12 podcast, 12 earnings, 8 Twitter, 1 ticket). A stop is model-free,
about 22 s, and the full clone is most of that. A replay of such a weekday
through the gate (110 min cadence, priority goes at once) gives 13 editor runs
of about 2.6 min each. That is ≈ 50 runner-min/day, against ≈ 38 for the
hourly cron alone. Over the 24 h to 2026-10-31 14:00 UTC, the lane runs that
actually happened would have woken it 7 times (5 editor runs), ≈ 14 min. That
bound holds while runs publish. During an outage the backoff (see "The gate")
holds the editor to about 8 attempts a day, 12 with priority material.

**Why not the cron alone.** On 2026-10-31 the hourly cron fired none of its
slots between the workflow's re-enable at 08:21 UTC and 14:00, even after
#6316 pushed this file at 11:17 to re-register it. Its first scheduled run
was created at 14:47. In the 26 h to 14:00 UTC (read
from the Actions API), the repository's other schedules were also delayed and
dropped:

- 2-hourly crons (RSS, Arm timeline, blog subscriptions, production
  synthetic): 5 of 13 runs each.
- 3-hourly: 4 of 9. 6-hourly: 4 of 5.
- Earnings: 1 of 6. Podcast Signal: 1 of 5 since it was created at 03:14.
- Daily lanes ran 3 to 6.8 h late.

GitHub documents that scheduled runs may be delayed under high load and that
some may be dropped. The numbers fit that, with fewer runs firing the more
often a cron is scheduled. They do not show why this cron fired none. Whether
the re-enable, the workflow's age or the `:50` slot matters cannot be checked
from the repository. The input lanes are cron-driven too, so `workflow_run`
inherits their delays. Every lane run that does happen now wakes the station,
though, when it finishes. Between the 08:21 re-enable and 14:00 that would
have been three wake-ups instead of none, at about 10:38 (Podcast Signal),
12:19 (Twitter) and 13:03 (model tickets).

### The gate (deterministic, before any model runs)

```
new = inbox candidates whose key is not in research/aradio/cursor.json
force (workflow_dispatch input)         → run the editor
no new items                            → stop: "no new material"
failed editor runs since last bulletin  → stop until the backoff ends (below)
any priority item in new                → run the editor now
≥ 110 min since cursor.last_editor_run_at (or never ran) → run the editor
otherwise                               → stop: routine material waits for the 2 h cadence
```

Priority items: earnings filings, earnings-call episodes, and **long-form**
(≥ 10 min) P0 episodes whose transcript is available. Short official clips —
OpenAI posts about one 90–250 s customer testimonial a day as a P0 video — and
metadata-only episodes are routine material that waits for the 2 h cadence.
A stopped gate commits nothing and exits 0.

**Backoff while the station is stuck.** The cursor moves only on
publication, so during an outage (editor quota or token, a validator mismatch,
a broken push) the 110 min anchor never moves. Without a backoff, every trigger
would retry the editor on the shared Claude subscription, up to about 57 times
on a weekday. Failed runs commit nothing, so `aradio_run_alert.py --history`
reads them from the run history before the gate: the runs since
`cursor.last_editor_run_at` whose editor step ran, and when the newest one
finished. Each of them failed, since an editor run that published would have
moved the cursor. A run that hung past `timeout-minutes` counts: GitHub
reports it as cancelled, and its jobs show that it started. A setup or gate
failure spent no editor time, so it does not lengthen the wait. The gate then
waits 30 min after the newest failed editor run, doubling per failure to a
4 h cap, or 2 h while priority material waits so a fixed outage resumes it
quickly. A publication moves the cursor, which resets the backoff, and
`force` bypasses it. With a trigger every 20 min and every attempt failing, a
24 h outage makes 8 editor attempts instead of 72 (12 with priority material
waiting). Each run's jobs cost an API call, so at most 20 runs are looked up,
newest first; past that the count is a lower bound, which can only shorten
the wait. A failed lookup, or the step's 3 min `timeout-minutes`, writes no
record, which means no backoff and no force, never a station that stops
trying.

**Bounded edge cases.** The run history can mislead the history step in
four known ways. Each costs at most one extra editor run, never a stuck
station:

- The API shows only a run's latest attempt. If the run that honoured a
  force is re-run and the re-run stops at its gate, the honouring editor run
  is hidden, and the next run can honour the force again.
- A run whose jobs list comes back empty looks as if it never started. If it
  was the honouring run, the force can be honoured twice.
- The bulletin's stamp comes from the runner's clock, run times from
  GitHub's. A runner clock more than a minute slow can make the run that
  published look like a later gate stop, with the same result.
- More than 20 newer displaced or failed runs use up the lookups before an
  older editor failure is reached, so that run does not back off. Its own
  editor run is then the newest, which the next run finds first.

**Why the gate runs on the full clone.** On 2026-10-31 a pre-gate was built
and then dropped. It decided on a blobless, depth-1 sparse checkout of only
the gate's inputs (~7 MB, ~4 s) before paying for the full clone (~284 MB,
14 s). It saved less than it seemed to, for two reasons:

- The runner's workspace is shared. Sixteen scheduled lanes reuse whatever
  clone is there without a quarantine, so after a sparse stop the next of
  them re-cloned the full repository: the saving moved to that lane.
- Lane-woken runs are mostly editor runs (5 of 7 in the observed 24 h),
  which need the full clone anyway.

A replay of the runner's job order put a number on it. If every cron fired on
a weekday, runner-wide clone traffic would drop from 23.6 to 19.0 GB/day and
checkout time by 0.4 min/day. Over the observed 24 h the saving was nothing.
In exchange, a sparse-checkout list had to cover every file the gate reads,
or the pre-gate would stop silently on material it could not see. In review,
it also broke the reusing lanes: a sparse `.git` left at the workspace root
was inherited, because git 2.34's `sparse-checkout disable` does not clear
`core.sparseCheckout` or the blob filter. If bandwidth ever becomes the
constraint, that design is the place to start: a subdirectory clone, deleted
every run. The numbers do not justify it today.

**Priority material that expires unaired is reported.** A priority item opens
the gate at once, so one that leaves its window (3 days for earnings, 7 for
episodes) with its key absent from the cursor was lost to an outage: every
editor run in its window failed or never ran. Every run, stop or go, re-runs
the two priority collectors at `now − 24 h` and lists the priority items that
were eligible then, are not now, and were never consumed (an episode consumed
from its show notes counts as aired). The workflow posts each to Hooker
(`ara-telemetry`, priority 4) keyed `aradio-expired-<item key>`, so the day's
later runs are idempotency hits, and annotates the run only on that first
post. After 24 h an item is never listed again, so nothing repeats once
Hooker's idempotency record ages out. Hooker keeps a key even when every
delivery of its message failed, so an item whose first delivery is lost is not
re-sent; the outage behind it is alerted separately. A failure inside the
report never changes the gate's decision (test-pinned); it only warns. Each
POST is time-boxed (`--max-time 30`, the step to 5 min), because on a go it
runs just before the editor, and never retried: Hooker records a key before it
delivers, so a retry would come back as an idempotency hit that delivered
nothing.

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
                   min_gap_s: int = 120,
                   sentence_end: Callable[[str, str | None], bool] | None = None) -> list[dict]:
    """segments = tuber transcript segments [{"startMs": int, "text": str}].
    Returns ≤ max_windows non-overlapping windows [{"text": str, "at_s": int}]
    of ≤ max_words words each, highest-information first by score, then
    re-sorted by at_s. Deterministic; sponsor reads and intros/outros score low.
    With sentence_end (the inbox passes check_aradio.sentence_end) the same
    windows keep the captions' " >> " speaker changes and get "…" glued to
    an edge that cuts into a sentence; the lane's own excerpts stay plain."""
```

## Inbox (`.agent-input/aradio/`, never committed)

| File | Content |
|---|---|
| `inbox.md` | the new items, rendered for the editor, priority first |
| `inbox.json` | the same items, machine-readable |
| `board.json` | the editor's VIEW of `research/aradio/state.json`: unresolved threads and threads resolved in the last 48 h, each with its last 3 history entries and its evidence; older resolved threads are listed by slug in `other_threads` (their slugs are taken). The validator and writer always read the full `state.json`. |
| `context.json` | `now`, `last_bulletin_at`, `last_headline`, limits — including the validator's quote/label budget (`quotes_per_source` 2, `quote_words_per_source` 60, `quotes_per_run` 8, `label_chars` 90; a parity test pins these to `check_aradio.py`) |
| `transcripts/<n>.txt` | top transcript windows (`[mm:ss] text`) for spoken items; `>>` marks a speaker change and `…` an edge that cuts into a sentence (a committed-excerpt fallback is marked `…` at both edges) |

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
| `research/podcasts/index.json` | `ep:<episode id>` (with a transcript) / `ep:<episode id>:meta` (show notes only) | published (else first seen) in the last 7 days, and transcript available or first seen ≥ 6 h ago without one |
| `research/earnings/index.json` + event `.md` | `earn:<accession>` | filed in the last 3 days |
| `research/twitter/<date>.md` stories | `tw:` + sha256(first source URL + "\n" + normalized title)[:20] (NFKC, case-folded, punctuation → space, whitespace collapsed) | run section in the last 26 h |
| `research/models/tickets/*.md` | `tk:<slug>:<history length>` | last history entry in the last 2 days |

An episode consumed from show notes only is offered once more when its
transcript lands (with `note: "transcript now available; previously offered
from show notes only"`); once consumed with a transcript it is never offered
again. Distinct stories that cite the same tweet get distinct keys; an
identical re-published story keeps its key; no key embeds a URL.

For earnings items, a Key-quote line that holds a URL is dropped whole —
stripping the URL out would splice words that were never adjacent into
something that reads as verbatim — and a header left with no quote goes too.

Caps: ≤ 40 items (priority first, then newest), ≤ 8 transcript files of
≤ 20 windows × ≤ 70 words; items (inbox.json, inbox.md, context.json,
transcripts) ≤ 400 KB and `board.json` ≤ 120 KB, budgeted SEPARATELY so the
board can never displace new material (over its cap the oldest resolved
threads move to `other_threads`, then long fields are clipped). A transcript
fetch failure — including a truncated response — falls back to the committed
excerpts. New material that leaves zero items staged is a real error (exit 1),
never an editor run on an empty inbox.

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
**dropped** — the editor cannot introduce a URL. Over-long text fields are
truncated (evidence `label` ≤ 90 characters, the width the dashboard shows);
unknown audio tags and URLs in the script are stripped. Evidence `kind` (and
`at`) are set from the inbox item that owns the URL, never trusted from the
editor; a spoken or earnings item owns its URLs before items that merely link
to them.

**Quotes** are the strictest field, because a quote puts words in someone's
mouth. A `quote` is kept only if it is EXACTLY ONE COMPLETE SENTENCE of one
transcript window of a spoken item (`podcast`, `video`, `earnings-call`) or of
the quoted words of one earnings `Key quotes:` line (issuer text from the
8-K). Titles, show notes, other text lines, and Twitter/ticket text — which
are ARA's own model-written summaries — are never quotable. Sentences end at
`.`, `!` or `?` (closing quotes or brackets may follow) before whitespace —
never inside a number, after an abbreviation, initials or an ellipsis, or
before a lower-case word (doubt means no split) — at a `>>` speaker change,
and at the segment's ends. The editor's string, case- and punctuation-folded,
must equal one whole sentence, and that sentence is published in the SOURCE'S
OWN WORDING, terminal punctuation included — so a quote keeps its own
negation, condition and question mark ("we will see AGI" cannot be cut from "I
don't think that over the next decade we will see AGI.", nor "Nvidia margins
hold" from "Will Nvidia margins hold?"). A sentence holding an ellipsis —
including the inbox's `…` mark where a window edge cuts it — is not quotable,
nor is a transcript sentence without its own `.`, `!` or `?` (so unpunctuated
captions yield no quote: paraphrase them); a Key-quotes line's last sentence
may end where the issuer's quotation ends. At most 40 words. A transcript
quote never carries `speaker` (captions do not record who is talking, and a
name in a window may be its subject); a Key-quotes quote carries that line's
own attribution, whatever the editor wrote. A quoted entry's `label` is the
owning item's `source`. Volume: per source (a deep link counts as its episode)
at most 2 quotes and 60 quoted words, counting quotes already on the board,
and at most 8 new quotes per run — the earnings lane's excerpt policy,
enforced on everything Aradio publishes. Excess quotes are dropped and their
evidence kept. Warnings never contain quote text (they are committed with each
bulletin). What stays unverifiable by design: the prose fields and the spoken
script. The prompt forbids naming a speaker the source does not name; the
validator cannot prove prose true. Residual quote risks: a caption `>>` placed
inside one speaker's sentence makes its tail look like a sentence; the
committed-excerpt fallback carries no `>>` at all, so there a sentence can run
across an unpunctuated speaker change; a caption speaker label
(`>> Name, Title: …`) is part of the turn's first sentence, so quoting that
sentence publishes the label with it.

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
3. Keeps each thread's history bounded: `state.json` holds the newest 12
   entries; older ones move, in order and in the same run, to the `history`
   list of the run month's `archive/YYYY-MM.json`. Checked before anything is
   written, for every thread: entries archived this run + entries retained ==
   prior entries + entries stamped this run. Edits, reordering, removal
   without archiving, a deleted thread, or a changed `first_seen` are refused.
   (Without the bound, history grew forever and the board eventually filled the
   editor's whole input budget.)
4. Records every inbox key as consumed (`cursor.json`), plus
   `last_editor_run_at` and, when on air, `last_bulletin_at`.
5. Writes atomically (temp file + `os.replace`), stages exact paths only
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
- `archive/YYYY-MM.json` — append-only:
  `{schema, month, updated_at, threads: [archived resolved Thread],
  history: [{slug, first_seen, at, change, archived_at}]}`. Existing rows are
  kept verbatim; a file the writer could only extend by rewriting (not an
  object, an unknown field, another schema or month, `threads`/`history` not
  a list, a row that is not an object, a row failing the URL rule) is
  refused and nothing is written.

Bulletin `id` is the UTC run stamp `YYYY-MM-DD-HHMM`. The dashboard's
"History (N)" therefore shows at most the 12 newest entries.

`aradio.yml` publishes only from `main`: a guard right after the workspace
quarantine fails any other ref before checkout, so a branch dispatch spends no
model or TTS budget and uploads no public mp3. `cursor.json` moves only when
the editor runs, so its freshness SLO is 30 h: replaying the gate over real lane
data (2026-10-10..30) found routine quiet gaps of 10–21 h, and the only gap
over 30 h was a genuine three-day Twitter-lane outage.

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
`continue-on-error` TTS step, which exited 0 on Gemini errors and left the
digest silently without audio from 2026-10-22 to 10-30, is the anti-pattern
this avoids: it still keeps the digest run green, so its missing audio pages
only hours later, through the `digest-audio` freshness SLO.

**One alert per outage, not per hour.** A run that fails without publishing
leaves the cursor where it was, so while the cause lasts (editor quota or
token, a validator mismatch, a broken push) every hour fails the same way, and
each used to post its own priority-5 Hooker event, about 24 a day.
`scripts/aradio_run_alert.py` keys such a run's telemetry on the stage that
failed, on `cursor.last_editor_run_at` (which only a publication moves) and on
the UTC date: `aradio-stuck-<stage>-<stamp>-<date>`. Hooker delivers the first
and drops the rest by Idempotency-Key, and a different stage failing in the
same outage alerts once more. The date is there because Hooker records a key
before delivering and keeps it when every delivery fails: one lost Telegram
delivery would otherwise silence the outage for two weeks. With it, a long
outage re-alerts once a day. A run that GitHub cancelled at `timeout-minutes`
is stuck on the stage it hung in. The first run that publishes again takes
the history step's count of this workflow's failed runs since that stamp
(`actions: read`; a run cancelled after it started is one) and, if there are
any, posts "Aradio recovered" once (`aradio-recovered-<stamp>`). A run that
fails after publishing (missing audio) put a new bulletin out, so it keeps its
per-run alert, and the 30 h `cursor.json` freshness SLO still pages daily
while the station stays stuck.

**A stale publication PR is closed, never merged.** `aradio.yml` publishes
through safe-push like every lane, but CLAUDE.md rule 13's "merge open
`automation/safe-push/*` PRs oldest first" does not apply here. If a
bulletin's PR fails to auto-merge, `main`'s cursor did not advance, so the
next hourly run re-reads the same material and airs it again from `main`.
Merging the stale PR afterwards would roll the board and cursor back over that
newer run. Close it; its orphaned mp3 on S3 is harmless (keys are never
reused).

## Dashboard

`/aradio` is a radio first ("ARA AI News"; `dashboard/src/render/aradio.ts`, the
Aradio section of `main.ts`). One large play button starts **continuous
listening**: the newest bulletin with audio, then older ones; text-only
bulletins are never in the running order; a bulletin that airs mid-listen plays
right after the one on now (several in the order they aired). Bulletins are
episodes, not a live stream, so nothing on the card claims to be on air. Its
status line gives the age of the newest bulletin **with audio** ("Latest
bulletin · 3h ago", whatever the age) and is absent when nothing is playable
(before the first bulletin, or only text-only ones: a text-only bulletin
cannot be heard, and the empty and text-only states say so). The card also
shows "Updated N ago" for the newest bulletin of any kind (not repeated when
the status line already gives that age) and "The next bulletin airs when the
picture changes" (there is no schedule to promise, and no listener count),
what is playing or up first with the show's cover, the controls
(previous, back 15 s, play, forward 15 s, next), a seek bar, the speed (1×,
1.25×, 1.5×, 2×) and "stop after this bulletin" (one-shot), the transcript of
the bulletin on now, the storylines it covered ("In this bulletin"), the next
three bulletins and the podcast-follow strip. When everything has played the
radio stays on, and the next bulletin to air starts by itself while the page
is open. Below it, "Behind the broadcast": the situation board, the last 72
bulletins and the transcript of the one picked in the log (collapsed until
asked for).

- **Following the transcript**: the radio card's transcript sits in a
  fixed-height window. While its bulletin plays, the line being read is in full
  ink (`aria-current`), the lines already read are quieter, and the window
  scrolls itself (never the page) to keep that line a third of the way down.
  Scrolling the window by hand (wheel, touch, its scrollbar, the keyboard)
  stops the following until "Back to live line". Each line of a bulletin with
  audio is a button that plays the bulletin from there; the lines are one tab
  stop (arrow keys, Home and End move between them). The line changing is
  never announced. A line focused from the keyboard puts the reader in charge
  of the window too, so following never scrolls the focused line away. TTS
  returns no timestamps, so line timing is **estimated** (`aradioLineTimings`:
  each line's length in characters plus 0.5 s between turns, scaled to the
  real duration). On the only real bulletin so far (2026-10-31 08:53, line
  starts measured from its audio with a speech recogniser and checked against
  the silences at each turn) it is ~0.8 s off on average, ~2.8 s at worst, and
  on the right line ~92 % of the time. That is in-sample: finer weights
  (acronyms, digits, punctuation pauses) did no better on it, and the
  estimate should be re-checked as bulletins accumulate. The page says
  "Timing is approximate" and shows no per-line times. A text-only bulletin's
  transcript is plain text.
- **Speed and progress** are this browser's own (localStorage, every access in
  try/catch; a blocked store means 1× and nothing heard): the speed applies to
  the shared player only while it holds a bulletin (the digest stays at 1×).
  The log's rows lead with a play pill showing the bulletin's length, the time
  left, or "Played", filled by how much was heard; playback still starts a
  bulletin from the top.
- **Following in a podcast app**: a button per app this platform can open (none
  of the addresses are in the HTML; `hydrateAradioFollow` sets them):
  Apple Podcasts `podcast://<feed without its scheme>` on iPhone, iPad and Mac
  (it opens the app's "Follow a Show by URL" box, prefilled with `http://…`,
  which the site redirects to https); Overcast's
  `overcast://x-callback-url/add?url=<feed>` on iPhone and iPad; Pocket Casts'
  `pktc://subscribe/<feed without its scheme>` on iPhone, iPad and Android,
  else its web player's `https://pocketcasts.com/follow/<feed>`; Spotify,
  which cannot follow a feed, through the listed show
  (https://open.spotify.com/show/6XPmQwa4EfqXz7S3Vs1Owb, listed 2026-11-01) set in `ARADIO_SPOTIFY_SHOW_URL`. Copy RSS and the manual Apple route stay as the fallback.

- **Audio** is `${AUDIO_BASE}/${audio.key}`, only for a key matching
  `^audio/aradio/[A-Za-z0-9._-]+\.mp3$`, played through the site's one shared
  bottom-bar `<audio>` (the digest and a bulletin can never play at once). The
  bar steps aside while the radio's own button is on screen.
- **Lock screen** (Media Session): title = headline, artist "ARA AI News", no
  album, artwork `/brand/ara-ai-news-cover.png` (the square show art the
  podcast feed uses; the digest keeps the site's social card); play,
  pause, seekto, previous/next, seekbackward/seekforward (15 s, or the offset
  the system asks for; iOS may show these skips in place of previous/next)
  and `setPositionState`. On `ended` the next
  bulletin starts at once and an overdue poll runs alongside: timers are
  throttled behind a locked screen, so playback never waits on the network.
- **Audio failures**: a bulletin whose mp3 does not load or play (the
  element's `error`, or `play()` rejecting with `NotSupportedError`) is
  skipped like an `ended` one — the next playable bulletin starts, keeping the
  play state, and the live region says "Couldn’t play the 12:50 UTC bulletin —
  skipping". A failed bulletin is never retried by itself in that listening
  session (polls do not queue it again). When nothing left can play, the radio
  stops and says so on the card ("Couldn’t play"), the bar and the lock screen
  (paused); play, from any of them, tries again from the first bulletin missed.
  A blocked or interrupted `play()` (autoplay policy, a newer load) is not a
  failure. The rules are `failAradioProgramme` / `retryAradioProgramme`.
- **Stalls**: a source that hangs never errors, so a watchdog
  (`aradioStallStep`) fails a bulletin the same way when, while the listener
  wants sound, the player is starved and nothing has moved for 20 s.
  Playback that resumes restarts the clock, and so does audio still arriving:
  after playback has started, buffered audio that grows; before it, any
  `progress` event. Chrome reports no buffered range until about 32 KB have
  arrived, so on a slow link those events are the only sign. The player's
  events drive the checks, and while it is starved a re-check is booked for
  when a stall would be due. A timer held behind a locked screen only delays
  the skip, because each check compares the player's own state. The clock is
  monotonic (`performance.now()`), so a system clock jump cannot move a skip.
  A stop on a stall drops the hung request, so trying again opens a fresh one.
  The digest is never watched.
- **Updates**: the page polls `research/aradio/index.json` every 5 minutes (and
  in the background while a bulletin plays). The radio card takes new data at
  once and is patched in place (fixed heights, no re-render, focus kept);
  "Behind the broadcast" takes it when the reader asks (the update chip).
- **Empty states**: before the first run, no status line and "The first
  bulletin hasn't aired yet"; with only text-only bulletins, no status line,
  "No audio to play yet" and the log to read.

### Podcast feed (`/aradio/feed.xml`)

`dashboard/scripts/aradio-feed.mjs` (called by `postbuild-seo.mjs`) writes
`dist/aradio/feed.xml` from the copy of `research/aradio/` the page itself
serves: RSS 2.0 with iTunes tags (title "ARA AI News", author "ARA", explicit
false, Technology and News › Tech News). Episodes are the page's bulletins with
a policy-valid audio key, newest first, ≤ 72: guid = bulletin id, pubDate =
`aired_at`, an enclosure with the same URL the page plays (`length` = `bytes`,
`audio/mpeg`), `itunes:duration`, and the transcript as the description
(≤ 4,000 characters as an app receives them). Apps render a description as
HTML, so its text is HTML-escaped and then XML-escaped: a `<tag>` in a
transcript stays text. Titles, which apps show as text, are XML-escaped only.
Bulletin files are read only at validated
paths inside the station directory, every value is XML-escaped, the output is
deterministic, and absent data is a valid feed with no episodes. Caddy caches
it like `/feed.xml`; the container smoke and `check_production_surface.py`
(`aradio-feed`) guard it. Anyone can follow it by URL (Apple Podcasts: Library
→ ⋯ → Follow a Show by URL).

**Artwork.** `<itunes:image>` and the RSS `<image>` (with the channel's title
and link) name `<origin>/brand/ara-ai-news-cover.png` (`ARADIO_FEED_ARTWORK_PATH`):
a 3000×3000 RGB PNG, no alpha channel, sRGB, 72 dpi, ~130 KB, committed in
`dashboard/public/brand/` as a regular git blob (`.gitattributes` keeps that
directory's `*.png`, not its JPEGs, out of LFS, which the Railway build does
not hydrate). That meets
Apple (square, 1400–3000 px, JPEG or PNG, RGB, no alpha) and Spotify (1:1, PNG
preferred over JPEG). It is the page's own type and tokens: "ARA" over "AI
News" in Source Serif 4 Subhead Bold from `dashboard/scripts/fonts/` rendered
with resvg, ground `#f4f5f8`, ink `#1a1a1a`, the play button in royal
`#2251ff`, and no sign or tagline. Apple and Spotify fetch art once per URL,
so a redesign ships under a new file name with the constant updated
(`aradio-cover.png` was the ARA Radio art; the 2026-11-01 rename to ARA AI
News shipped `ara-ai-news-cover.png`); overwriting the file in place changes
nothing in either app. The container smoke fetches whatever
`<itunes:image>` names and requires a real image with `Last-Modified` (Apple
checks art with HEAD).

**Owner email.** `ARADIO_FEED_OWNER_EMAIL`, a Dockerfile `ARG` that defaults to
`i@guzus.xyz`, adds `<itunes:owner>` with `<itunes:name>ARA</itunes:name>` and
the address (trimmed, escaped) in `<itunes:email>`. A service variable of the
same name on the deploy platform overrides the default; an empty value emits
no owner block, and so does a local build without the variable. Spotify
for Creators mails its ownership code to `<itunes:email>`; Apple's feed
requirements do not use it (Podcasts Connect asks for contact details itself).
Anyone who opens the feed can read the address. The build log line
`aradio/feed.xml written (N episodes, with|no itunes:owner)` shows whether the
variable reached the build.

**Listing on Spotify and Apple Podcasts.** Both list a show only once its feed
carries an episode, so wait for the first bulletin with audio.

- Spotify for Creators (then follow the show in the Spotify app):
  1. Check that `https://ara.guzus.xyz/aradio/feed.xml` shows
     `<itunes:email>i@guzus.xyz</itunes:email>` (the Dockerfile default) and at
     least one `<item>`.
  2. Sign in at `creators.spotify.com` with the Spotify account that should own
     the show. Choose **Find an existing show** (or, if the account already has
     a show, avatar menu → **Add a new show** → **Find an existing show**), then
     **Somewhere else**, and paste the feed URL.
  3. Spotify mails an 8-digit code from `noreply@hello.creators.spotify.com`
     to the feed's `<itunes:email>`. Paste it into the form, confirm the show
     details, and submit.
  4. Spotify re-reads the feed several times an hour; allow at least an hour
     before a change reaches the apps.
- Apple Podcasts Connect (`podcastsconnect.apple.com`):
  1. **+** → **New Show** → **Add a show with an RSS feed**, paste the feed
     URL, **Add**. Apple validates the feed: title, description, artwork,
     language, category and explicit on the show; title, enclosure and guid on
     every episode.
  2. On Show Information, check the details, set Content Rights, add the
     contact information, choose Availability, **Save**, then **Publish**.
