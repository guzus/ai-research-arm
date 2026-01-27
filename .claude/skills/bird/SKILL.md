---
name: bird
description: X/Twitter CLI for reading, searching, posting, and engagement via cookies.
---

# bird

Fast X/Twitter CLI using GraphQL + cookie auth.

## Install

```bash
npm install -g @steipete/bird
# or: brew install steipete/tap/bird
# or one-shot: bunx @steipete/bird whoami
```

## Authentication

`bird` uses cookie-based auth.

Use `--auth-token` / `--ct0` to pass cookies directly, or `--cookie-source` for browser cookies.

Run `bird check` to see which source is active. For Arc/Brave, use `--chrome-profile-dir <path>`.

## Commands

### Account & Auth

```bash
bird whoami                    # Show logged-in account
bird check                     # Show credential sources
bird query-ids --fresh         # Refresh GraphQL query ID cache
```

### Reading Tweets

```bash
bird read <url-or-id>          # Read a single tweet
bird <url-or-id>               # Shorthand for read
bird thread <url-or-id>        # Full conversation thread
bird replies <url-or-id>       # List replies to a tweet
```

### Timelines

```bash
bird home                      # Home timeline (For You)
bird home --following          # Following timeline
bird user-tweets @handle -n 20 # User's profile timeline
bird mentions                  # Tweets mentioning you
bird mentions --user @handle   # Mentions of another user
```

### Search

```bash
bird search "query" -n 10
bird search "from:steipete" --all --max-pages 3
```

### News & Trending

```bash
bird news -n 10                # AI-curated from Explore tabs
bird news --ai-only            # Filter to AI-curated only
bird news --sports             # Sports tab
bird news --with-tweets        # Include related tweets
bird trending                  # Alias for news
```

### Lists

```bash
bird lists                     # Your lists
bird lists --member-of         # Lists you're a member of
bird list-timeline <id> -n 20  # Tweets from a list
```

### Bookmarks & Likes

```bash
bird bookmarks -n 10
bird bookmarks --folder-id <id>
bird unbookmark <url-or-id>
bird likes -n 10
```

### Social Graph

```bash
bird following -n 20
bird followers -n 20
bird following --user <id>
bird about @handle
```

### Engagement Actions

```bash
bird follow @handle
bird unfollow @handle
```

### Posting

```bash
bird tweet "hello world"
bird reply <url-or-id> "nice thread!"
bird tweet "check this out" --media image.png --alt "description"
```

**Warning**: Posting is more likely to be rate limited; if blocked, use the browser tool instead.

## Media Uploads

```bash
bird tweet "hi" --media img.png --alt "description"
bird tweet "pics" --media a.jpg --media b.jpg  # Up to 4 images
bird tweet "video" --media clip.mp4            # Or 1 video
```

## Pagination

Commands supporting pagination: `replies`, `thread`, `search`, `bookmarks`, `likes`, `list-timeline`, `following`, `followers`, `user-tweets`

```bash
bird bookmarks --all                    # Fetch all pages
bird bookmarks --max-pages 3            # Limit pages
bird bookmarks --cursor <cursor>        # Resume from cursor
bird replies <id> --all --delay 1000    # Delay between pages (ms)
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

## Config File

`~/.config/bird/config.json5` (global) or `./.birdrc.json5` (project):

```json5
{
  cookieSource: ["chrome"],
  chromeProfileDir: "/path/to/Arc/Profile",
  timeoutMs: 20000,
  quoteDepth: 1
}
```

Environment variables: `AUTH_TOKEN`, `CT0`, `BIRD_TIMEOUT_MS`, `BIRD_COOKIE_TIMEOUT_MS`, `BIRD_QUOTE_DEPTH`

## Troubleshooting

- **Query IDs stale (404 errors)**: Run `bird query-ids --fresh`
- **Cookie extraction fails**: Check browser is logged into X, try different `--cookie-source`
- **Arc/Brave**: Use `--chrome-profile-dir` to point at the correct profile
