---
name: birdy
description: X/Twitter CLI for reading, searching, posting, and engagement via cookies, with multi-account rotation.
---

# birdy

Fast X/Twitter CLI using GraphQL + cookie auth. One static Go binary — no
Node runtime.

> Replaced the Node `bird` CLI (`@steipete/bird`), retired 2026-08-08. birdy
> began as a rotation proxy in front of bird and has served all 24 commands
> natively since v1.0.0. Command and flag names are unchanged, so `bird X` is
> `birdy X`. npm reports `@steipete/bird` as "no longer supported" — do not
> reinstall it. Note that birdy still *falls back* to `bird` when its native
> path errors, so a `bird CLI not found` message means the native call failed
> (usually a rate limit), not that you need to install bird.

## Install

```bash
brew tap guzus/tap && brew trust guzus/tap && brew install birdy
# or: curl -fsSL https://raw.githubusercontent.com/guzus/birdy/main/install.sh | bash
# in CI: use .github/actions/install-birdy
```

## Authentication

`birdy` uses cookie-based auth, and can rotate several accounts to spread
rate-limit pressure.

Use `--auth-token` / `--ct0` to pass cookies directly, or `--cookie-source` for browser cookies.

Run `birdy check` to see which source is active. For Arc/Brave, use `--chrome-profile-dir <path>`.

### Multi-account rotation

```bash
birdy account add main            # store an account
birdy account list                # list accounts
birdy account disable <name>      # take out of rotation without removing
birdy status                      # current rotation status
birdy budget                      # per-account 429 history + cooldown state
birdy -a main read <id>           # pin one account, skipping rotation
birdy -s quota-aware search "ai"  # route around accounts marked "hot"
```

Rotation strategies (`-s`): `round-robin` (default), `least-recently-used`,
`least-used`, `random`.

## Commands

### Account & Auth

```bash
birdy whoami                    # Show logged-in account
birdy check                     # Show credential sources
birdy query-ids --fresh         # Refresh GraphQL query ID cache
```

### Reading Tweets

```bash
birdy read <url-or-id>          # Read a single tweet
birdy <url-or-id>               # Shorthand for read
birdy thread <url-or-id>        # Full conversation thread
birdy replies <url-or-id>       # List replies to a tweet
```

### Timelines

```bash
birdy home                      # Home timeline (For You)
birdy home --following          # Following timeline
birdy user-tweets @handle -n 20 # User's profile timeline
birdy mentions                  # Tweets mentioning you
birdy mentions --user @handle   # Mentions of another user
```

### Search

```bash
birdy search "query" -n 10
birdy search "from:steipete" --all --max-pages 3
```

### News & Trending

```bash
birdy news -n 10                # AI-curated from Explore tabs
birdy news --ai-only            # Filter to AI-curated only
birdy news --sports             # Sports tab
birdy news --with-tweets        # Include related tweets
birdy trending                  # Alias for news
```

### Lists

```bash
birdy lists                     # Your lists
birdy lists --member-of         # Lists you're a member of
birdy list-timeline <id> -n 20  # Tweets from a list
```

### Bookmarks & Likes

```bash
birdy bookmarks -n 10
birdy bookmarks --folder-id <id>
birdy unbookmark <url-or-id>
birdy likes -n 10
```

### Social Graph

```bash
birdy following -n 20
birdy followers -n 20
birdy following --user <id>
birdy about @handle
```

### Engagement Actions

```bash
birdy follow @handle
birdy unfollow @handle
```

### Posting

```bash
birdy tweet "hello world"
birdy reply <url-or-id> "nice thread!"
birdy tweet "check this out" --media image.png --alt "description"
```

**Warning**: Posting is more likely to be rate limited; if blocked, use the browser tool instead.
In automation, set `BIRDY_READ_ONLY=1` so these can never fire.

## Media Uploads

```bash
birdy tweet "hi" --media img.png --alt "description"
birdy tweet "pics" --media a.jpg --media b.jpg  # Up to 4 images
birdy tweet "video" --media clip.mp4            # Or 1 video
```

## Pagination

Commands supporting pagination: `replies`, `thread`, `search`, `bookmarks`, `likes`, `list-timeline`, `following`, `followers`, `user-tweets`

```bash
birdy bookmarks --all                    # Fetch all pages
birdy bookmarks --max-pages 3            # Limit pages
birdy bookmarks --cursor <cursor>        # Resume from cursor
birdy replies <id> --all --delay 1000    # Delay between pages (ms)
```

## Output Options

```bash
--json          # JSON output
--json-full     # JSON with raw API response
--plain         # No emoji, no color (script-friendly)
--no-emoji      # Disable emoji
--no-color      # Disable ANSI colors (or set NO_COLOR=1)
--quote-depth n # Max quoted tweet depth in JSON (default: 1)
```

## Global Options

```bash
--auth-token <token>       # Set auth_token cookie
--ct0 <token>              # Set ct0 cookie
--cookie-source <source>   # Cookie source for browser cookies (repeatable)
--chrome-profile <name>    # Chrome profile name
--chrome-profile-dir <path>
--firefox-profile <name>
--timeout <ms>
--cookie-timeout <ms>
```

## Batch fetching

`multi-fetch` runs a manifest of operations concurrently and writes each result
to `<output-dir>/<id>.json` — one process instead of N, which is how ARA's
Twitter lane fetches ~70 sources per run.

```bash
birdy multi-fetch --manifest manifest.json --output-dir /tmp/bird
```

```json
{
  "operations": [
    {"id": "OpenAI",    "args": ["user-tweets", "@OpenAI", "-n", "20", "--json", "--plain"]},
    {"id": "search-ai", "args": ["search", "AI announcement", "-n", "50", "--json", "--plain"]}
  ],
  "concurrency": 8
}
```

A failed operation still writes `[]`, so downstream readers never crash on a
missing file.

## State

`~/.config/birdy/` holds `accounts.json` (credentials + per-account use and
429 counters), `state.json` (rotation position), and the query-id cache.

Environment variables: `AUTH_TOKEN`, `CT0`, `BIRDY_READ_ONLY=1` (blocks every
write command — set it in any automated context), `BIRDY_ACCOUNTS` (JSON
account list, for CI where there is no config dir).

## Troubleshooting

- **`bird CLI not found, and --bird requires it`**: birdy's native call failed
  and it tried to fall back to the retired Node CLI. The real cause is
  upstream — usually a rate limit. Check `birdy budget`; do not install bird.
- **Query IDs stale (404 errors)**: Run `birdy query-ids --fresh`
- **Cookie extraction fails**: Check browser is logged into X, try different `--cookie-source`
- **Arc/Brave**: Use `--chrome-profile-dir` to point at the correct profile
- **Verbose**: `-v` prints which account and which engine (`native (go)`) served the call
