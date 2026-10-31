#!/usr/bin/env python3
"""The ONLY committer for research/aradio/ (contract: docs/aradio.md).

Inputs are all trusted host artifacts: the validator's normalized edit, the
trusted inbox copy (under $RUNNER_TEMP), the optional TTS result and the S3
key the workflow uploaded to. The editor never rewrites the board; this script
applies its ops:

1. create -> new thread (first_seen = now, history = [change]);
   update -> patch the given fields, prepend new evidence (dedupe by URL,
   keep 8), append history; resolve -> status resolved, append history.
   Threads not named are untouched. Existing history entries are never
   modified (checked after applying, before anything is written).
2. Bounded board: unresolved threads untouched for 7 days are auto-resolved
   ("went quiet"); beyond 10 unresolved, the least important / least
   recently updated (untouched this run first) are auto-resolved ("board
   full"). Resolved threads idle for 7 days move to archive/YYYY-MM.json.
   Each thread keeps its newest 12 history entries in state.json; older ones
   move, in order and in the same run, to the `history` list of the run
   month's archive/YYYY-MM.json (append-only; each row is the entry plus the
   thread's slug and first_seen and its archived_at). Existing archive rows
   are kept verbatim; an archive that could only be extended by rewriting
   it (wrong shape, unknown field, a row that is not an object, a URL that
   fails the rule) is refused, never repaired. History is checked as:
   entries moved to the archive this run + the retained entries == the prior
   retained entries + entries stamped this run. Nothing is edited, reordered,
   or dropped without being archived.
3. Every inbox key is recorded as consumed in cursor.json with
   last_editor_run_at (and last_bulletin_at when on air); keys expire after
   21 days.
4. Files are written atomically (temp file + os.replace); cursor.json last, as
   the run marker. Exact paths are staged and committed:
   `Aradio bulletin YYYY-MM-DD HH:MM UTC` or `Aradio board update ...`.

The ops are re-validated against the current board before anything is
applied, so a mis-wired workflow cannot feed the raw agent artifact here.
Re-running for a run stamp that cursor.json already records is a no-op.

Published files (relative to research/aradio/):
  state.json, bulletins/YYYY-MM-DD/HHMM.json, index.json, cursor.json,
  archive/YYYY-MM.json. index.json bulletin `path`s are relative to
  research/aradio/, and `latest` is the newest bulletin id (or null).
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import check_aradio as contract
from build_aradio_inbox import bulletin_id, bulletin_relpath, iso_z, parse_ts

REPO_ROOT = Path(__file__).resolve().parent.parent
LANE_DIR = Path("research") / "aradio"
QUIET_AFTER = dt.timedelta(days=7)
ARCHIVE_AFTER = dt.timedelta(days=7)
# History entries kept per thread in state.json. A thread that stays live for
# weeks gains one entry per editor run, so without a bound state.json (and
# every copy of it) grows without limit.
HISTORY_KEEP = 12
# Identity fields on an archived history row; everything else is the entry.
ARCHIVE_ROW_KEYS = ("slug", "first_seen", "archived_at")
ARCHIVE_KEYS = ("schema", "month", "updated_at", "threads", "history")
KEY_TTL = dt.timedelta(days=21)
MAX_INDEX = 72
STAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:00Z$")
AUDIO_KEY_TEMPLATE = "audio/aradio/{id}.mp3"
# The dashboard refuses any other key shape; so does the writer.
AUDIO_KEY_RE = re.compile(r"^audio/aradio/[A-Za-z0-9._-]+\.mp3$")
QUIET_CHANGED = "No new developments for 7 days."
QUIET_CHANGE = "Went quiet: resolved automatically after 7 days without an update."
FULL_CHANGED = "Resolved to keep the board to the ten most important live storylines."
FULL_CHANGE = "Board full: resolved automatically (more than 10 live storylines)."
AUDIO_ERROR_MAX = 300
MAX_WARNINGS = 60

EXIT_OK = 0
EXIT_ERROR = 1


class WriterError(RuntimeError):
    pass


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def _load_optional(path: Path) -> Any | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise WriterError(f"{path} is unreadable: {exc}") from exc


def empty_cursor() -> dict:
    return {"schema": contract.SCHEMA, "updated_at": None, "last_editor_run_at": None,
            "last_bulletin_at": None, "keys": {}}


def empty_index(now_s: str) -> dict:
    return {"schema": contract.SCHEMA, "updated_at": now_s, "degraded": False,
            "latest": None, "bulletins": []}


# ---------------------------------------------------------------------------
# Board operations
# ---------------------------------------------------------------------------

def dedupe_evidence(entries: list[dict]) -> list[dict]:
    """Dedupe by URL (first wins), keep 8, and drop any URL failing the strict rule."""
    out: list[dict] = []
    seen: set[str] = set()
    for entry in entries:
        url = entry.get("url") if isinstance(entry, dict) else None
        if contract.safe_url(url) and url not in seen:
            seen.add(url)
            out.append(entry)
    return out[: contract.MAX_EVIDENCE]


def sanitize_thread(thread: dict) -> dict:
    """Legacy or hand-edited board entries get the same URL rule as new ones."""
    evidence = thread.get("evidence")
    thread["evidence"] = dedupe_evidence(list(evidence) if isinstance(evidence, list) else [])
    return thread


def unsafe_urls(value: Any, path: str = "$") -> list[str]:
    """Paths of every `url` field whose value fails the strict rule."""
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "url" and not contract.safe_url(item):
                found.append(f"{path}.url")
            found.extend(unsafe_urls(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(unsafe_urls(item, f"{path}[{index}]"))
    return found


def apply_ops(threads: list[dict], ops: list[dict], now_s: str
              ) -> tuple[list[dict], list[str]]:
    """Apply validated ops; return (threads, slugs touched in op order)."""
    by_slug = {thread["slug"]: copy.deepcopy(thread) for thread in threads}
    order = [thread["slug"] for thread in threads]
    touched: list[str] = []
    for op in ops:
        slug = op["slug"]
        if op["op"] == "create":
            if slug in by_slug:
                raise WriterError(f"create of existing slug {slug}")
            by_slug[slug] = {
                "slug": slug,
                "title": op["title"],
                "status": op["status"],
                "importance": op["importance"],
                "first_seen": now_s,
                "updated_at": now_s,
                "now": op["now"],
                "changed": op["changed"],
                "watch": op.get("watch", ""),
                "evidence": dedupe_evidence(list(op.get("evidence") or [])),
                "history": [{"at": now_s, "change": op["change"]}],
            }
            order.append(slug)
        else:
            thread = by_slug.get(slug)
            if thread is None:
                raise WriterError(f"{op['op']} of unknown slug {slug}")
            if op["op"] == "update":
                for name in ("title", "status", "importance", "now", "changed", "watch"):
                    if name in op:
                        thread[name] = op[name]
                if op.get("add_evidence"):
                    thread["evidence"] = dedupe_evidence(
                        list(op["add_evidence"]) + list(thread.get("evidence") or []))
            elif op["op"] == "resolve":
                thread["status"] = "resolved"
                thread["changed"] = op["changed"]
            else:
                raise WriterError(f"unknown op {op['op']}")
            thread["history"] = list(thread.get("history") or []) + [
                {"at": now_s, "change": op["change"]}]
            thread["updated_at"] = now_s
        if slug not in touched:
            touched.append(slug)
    return [by_slug[slug] for slug in order], touched


def _updated(thread: dict) -> dt.datetime:
    return (parse_ts(thread.get("updated_at")) or parse_ts(thread.get("first_seen"))
            or dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc))


def _auto_resolve(thread: dict, now_s: str, changed: str, change: str) -> None:
    thread["status"] = "resolved"
    thread["changed"] = changed
    thread["history"] = list(thread.get("history") or []) + [{"at": now_s, "change": change}]
    thread["updated_at"] = now_s


def bound_board(threads: list[dict], touched: list[str], now: dt.datetime
                ) -> list[tuple[str, str]]:
    """Auto-resolve quiet threads, then overflow beyond MAX_UNRESOLVED."""
    now_s = iso_z(now)
    auto: list[tuple[str, str]] = []
    for thread in threads:
        if thread.get("status") != "resolved" and now - _updated(thread) >= QUIET_AFTER:
            _auto_resolve(thread, now_s, QUIET_CHANGED, QUIET_CHANGE)
            auto.append((thread["slug"], "quiet"))
    live = [thread for thread in threads if thread.get("status") != "resolved"]
    overflow = len(live) - contract.MAX_UNRESOLVED
    if overflow > 0:
        def rank(thread: dict) -> tuple:
            importance = thread.get("importance")
            importance = importance if isinstance(importance, int) else 3
            return (thread["slug"] in touched, importance, _updated(thread), thread["slug"])

        for thread in sorted(live, key=rank)[:overflow]:
            _auto_resolve(thread, now_s, FULL_CHANGED, FULL_CHANGE)
            auto.append((thread["slug"], "board-full"))
    return auto


def split_archive(threads: list[dict], now: dt.datetime) -> tuple[list[dict], list[dict]]:
    keep: list[dict] = []
    archived: list[dict] = []
    for thread in threads:
        if thread.get("status") == "resolved" and now - _updated(thread) >= ARCHIVE_AFTER:
            moved = dict(thread)
            moved["archived_at"] = iso_z(now)
            archived.append(moved)
        else:
            keep.append(thread)
    return keep, archived


def trim_history(threads: list[dict], now: dt.datetime) -> list[dict]:
    """Keep the newest HISTORY_KEEP entries per thread (in place).

    Returns the removed entries, oldest first, as archive rows
    {slug, first_seen, <entry fields>, archived_at}.
    """
    now_s = iso_z(now)
    moved: list[dict] = []
    for thread in threads:
        history = list(thread.get("history") or [])
        if len(history) <= HISTORY_KEEP:
            continue
        cut = len(history) - HISTORY_KEEP
        for entry in history[:cut]:
            if not isinstance(entry, dict) or any(name in entry for name in ARCHIVE_ROW_KEYS):
                raise WriterError(f"history of {thread['slug']} has a malformed entry; "
                                  "refusing to archive it")
            moved.append({"slug": thread["slug"], "first_seen": thread.get("first_seen"),
                          **copy.deepcopy(entry), "archived_at": now_s})
        thread["history"] = history[cut:]
    return moved


def sort_threads(threads: list[dict]) -> list[dict]:
    def key(thread: dict) -> tuple:
        importance = thread.get("importance") if isinstance(thread.get("importance"), int) else 0
        resolved = thread.get("status") == "resolved"
        return (resolved, 0 if resolved else -importance, -_updated(thread).timestamp(),
                thread["slug"])

    return sorted(threads, key=key)


def assert_history_append_only(before: list[dict], kept: list[dict], archived: list[dict],
                               moved: list[dict], now_s: str) -> None:
    """History only grows, except that its oldest entries may move to the archive.

    `before` is the board as loaded; `kept` the threads staying in state.json;
    `archived` the threads moving to the archive whole; `moved` the history rows
    trim_history() takes out of `kept` this run, all of which are written to
    the archive in the same run. For every thread, with A = its rows in `moved`
    (in order) and R = its retained history:

        A + R == prior history + entries stamped by this run (`now_s`)

    so only a prefix leaves state.json, every removed entry is archived, and no
    entry is edited, reordered, or dropped. Every prior thread is still present
    (kept or archived) with the same first_seen; `kept` threads hold at most
    HISTORY_KEEP entries.
    """
    old: dict[str, dict] = {}
    for thread in before:
        if thread["slug"] in old:
            raise WriterError(f"board holds slug {thread['slug']} twice; refusing to "
                              "apply ops that would silently drop one")
        old[thread["slug"]] = thread
    moved_by_thread: dict[tuple, list] = {}
    for row in moved:
        if row.get("archived_at") != now_s:
            raise WriterError("an archived history row is not stamped by this run")
        entry = {name: value for name, value in row.items() if name not in ARCHIVE_ROW_KEYS}
        moved_by_thread.setdefault((row.get("slug"), row.get("first_seen")), []).append(entry)
    after: dict[str, dict] = {}
    for thread in kept + archived:
        if thread["slug"] in after:
            raise WriterError(f"thread {thread['slug']} would appear twice")
        after[thread["slug"]] = thread
    for slug in old:
        if slug not in after:
            raise WriterError(f"thread {slug} would be deleted")
    for slug, thread in after.items():
        prior = old.get(slug)
        if prior is not None and thread.get("first_seen") != prior.get("first_seen"):
            raise WriterError(f"first_seen of {slug} would change")
        prior_history = list(prior.get("history") or []) if prior is not None else []
        full = (moved_by_thread.pop((slug, thread.get("first_seen")), [])
                + list(thread.get("history") or []))
        if full[: len(prior_history)] != prior_history:
            raise WriterError(f"history of {slug} would be rewritten")
        if any(not isinstance(entry, dict) or entry.get("at") != now_s
               for entry in full[len(prior_history):]):
            raise WriterError(f"history of {slug} would gain an entry this run did not make")
    for thread in kept:
        if len(thread.get("history") or []) > HISTORY_KEEP:
            raise WriterError(f"history of {thread['slug']} would keep more than "
                              f"{HISTORY_KEEP} entries")
    if moved_by_thread:
        raise WriterError("archived history rows match no thread: "
                          + ", ".join(sorted(str(slug) for slug, _ in moved_by_thread)))


def archive_rows(archive: Any, month: str) -> tuple[list[dict], list[dict]]:
    """(threads, history) of the month's existing archive file, as they are.

    The archive is append-only, so the writer only ever adds rows after the
    existing ones. A file it could only extend by rewriting is refused
    instead, with nothing written: not an object, a field it does not know
    (it would be dropped), another schema or month, a `threads` or `history`
    that is not a list, or a row that is not an object.
    """
    if archive is None:
        return [], []
    where = f"archive/{month}.json"
    if not isinstance(archive, dict):
        raise WriterError(f"{where} must be an object; refusing to overwrite it")
    unknown = sorted(str(name) for name in set(archive) - set(ARCHIVE_KEYS))
    if unknown:
        raise WriterError(f"{where} has unknown fields ({', '.join(unknown)}); refusing to "
                          "overwrite it")
    if archive.get("schema", contract.SCHEMA) != contract.SCHEMA:
        raise WriterError(f"{where} has schema {archive['schema']!r}, not {contract.SCHEMA}; "
                          "refusing to overwrite it")
    if archive.get("month", month) != month:
        raise WriterError(f"{where} says month {archive['month']!r}; refusing to overwrite it")
    found: list[list[dict]] = []
    for name in ("threads", "history"):
        rows = archive.get(name, [])
        if not isinstance(rows, list):
            raise WriterError(f"{where} {name} must be a list; refusing to overwrite it")
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                raise WriterError(f"{where} {name}[{index}] is not an object; refusing to "
                                  "overwrite it")
        found.append(rows)
    return found[0], found[1]


# ---------------------------------------------------------------------------
# Audio outcome
# ---------------------------------------------------------------------------

def audio_outcome(on_air: bool, run_id: str, tts_result: dict | None,
                  audio_key: str | None, audio_error: str | None
                  ) -> tuple[dict | None, str | None]:
    if not on_air:
        return None, None
    expected_key = AUDIO_KEY_TEMPLATE.format(id=run_id)
    if audio_key and (audio_key != expected_key or not AUDIO_KEY_RE.match(audio_key)):
        raise WriterError(f"audio key {audio_key!r} does not match {expected_key!r}")
    if tts_result and tts_result.get("ok") is True and audio_key and not audio_error:
        size = tts_result.get("bytes")
        duration = tts_result.get("duration_s")
        if (not isinstance(size, int) or isinstance(size, bool) or size <= 0
                or not isinstance(duration, (int, float)) or isinstance(duration, bool)):
            raise WriterError("TTS result is ok but lacks bytes/duration_s")
        return {"key": audio_key, "bytes": size, "duration_s": round(float(duration), 1)}, None
    if audio_error:
        reason = audio_error
    elif tts_result is None:
        reason = "TTS did not run"
    elif tts_result.get("ok") is not True:
        reason = str(tts_result.get("error") or "TTS failed")
    else:
        reason = "audio upload to S3 failed"
    return None, contract.clip(contract.clean_text(reason), AUDIO_ERROR_MAX)[0]


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------

def compose(*, edit: dict, inbox: contract.TrustedInbox, board: dict, cursor: dict,
            index: dict | None, archive: dict | None, now: dt.datetime,
            audio: dict | None, audio_error: str | None, backend: str, model: str
            ) -> tuple[dict[str, Any], dict]:
    """Return ({relative path: JSON data}, summary) without touching disk."""
    now_s = iso_z(now)
    run_id = bulletin_id(now)
    before = [thread for thread in board.get("threads") or [] if isinstance(thread, dict)]
    threads, touched = apply_ops(before, edit["ops"], now_s)
    threads = [sanitize_thread(thread) for thread in threads]
    auto = bound_board(threads, touched, now)
    threads, archived = split_archive(threads, now)
    moved = trim_history(threads, now)
    # One check over the final result: ops, auto-resolves and the trim alike.
    assert_history_append_only(before, threads, archived, moved, now_s)
    threads = sort_threads(threads)
    outputs: dict[str, Any] = {}

    state = {"schema": contract.SCHEMA, "updated_at": now_s, "headline": edit["headline"],
             "threads": threads}
    outputs["state.json"] = state

    if archived or moved:
        month = now.strftime("%Y-%m")
        prior_threads, prior_rows = archive_rows(archive, month)
        seen = {(row.get("slug"), row.get("first_seen")) for row in prior_threads}
        # Append-only: earlier rows verbatim (never re-sanitized: a row that
        # fails the URL rule stops the run below instead of being rewritten),
        # this run's archived threads and trimmed entries after.
        outputs[f"archive/{month}.json"] = {
            "schema": contract.SCHEMA, "month": month, "updated_at": now_s,
            "threads": copy.deepcopy(prior_threads) + [
                row for row in archived if (row["slug"], row.get("first_seen")) not in seen],
            "history": copy.deepcopy(prior_rows) + moved}

    kinds = {}
    for item in inbox.items:
        kind = str(item.get("kind", ""))
        kinds[kind] = kinds.get(kind, 0) + 1
    kinds = dict(sorted(kinds.items()))

    on_air = edit["on_air"] is True
    index_data = copy.deepcopy(index) if isinstance(index, dict) else None
    if on_air:
        by_slug = {thread["slug"]: thread for thread in threads + archived}
        sources: list[dict] = []
        seen_urls: set[str] = set()
        for op in edit["ops"]:
            for entry in (op.get("evidence") or []) + (op.get("add_evidence") or []):
                if contract.safe_url(entry["url"]) and entry["url"] not in seen_urls:
                    seen_urls.add(entry["url"])
                    sources.append({"url": entry["url"], "kind": entry["kind"],
                                    "label": entry["label"]})
        lines = []
        for line in edit["script"]:
            speaker, raw = contract.split_script_line(line)
            lines.append({"speaker": speaker, "text": contract.strip_audio_tags(raw)})
        bulletin = {
            "schema": contract.SCHEMA,
            "id": run_id,
            "aired_at": now_s,
            "headline": edit["headline"],
            "lines": lines,
            "script": list(edit["script"]),
            "covers": list(edit["covers"]),
            "threads": [{"slug": slug, "title": by_slug[slug].get("title"),
                         "status": by_slug[slug].get("status")}
                        for slug in edit["covers"] if slug in by_slug],
            "sources": sources,
            "ops": [{"op": op["op"], "slug": op["slug"]} for op in edit["ops"]],
            "warnings": list(edit.get("warnings") or []),
            "audio": audio,
            "audio_error": audio_error,
            "editor": {"backend": backend, "model": model},
            "inbox": {"items": len(inbox.items), "kinds": kinds},
        }
        path = bulletin_relpath(now)
        outputs[path] = bulletin
        row = {"id": run_id, "aired_at": now_s, "headline": edit["headline"], "path": path,
               "audio": audio, "covers": list(edit["covers"]),
               "kinds": sorted({source["kind"] for source in sources})}
        rows = [r for r in (index_data or {}).get("bulletins") or []
                if isinstance(r, dict) and r.get("id") != run_id]
        rows = [row] + rows
        index_data = {"schema": contract.SCHEMA, "updated_at": now_s,
                      "degraded": audio is None, "latest": run_id,
                      "bulletins": rows[:MAX_INDEX]}
        outputs["index.json"] = index_data
    elif index_data is None:
        outputs["index.json"] = empty_index(now_s)

    keys: dict[str, str] = {}
    for key, consumed_at in (cursor.get("keys") or {}).items():
        consumed = parse_ts(consumed_at)
        if consumed is not None and now - consumed <= KEY_TTL:
            keys[key] = consumed_at
    for key in inbox.keys():
        keys.setdefault(key, now_s)
    outputs["cursor.json"] = {
        "schema": contract.SCHEMA,
        "updated_at": now_s,
        "last_editor_run_at": now_s,
        "last_bulletin_at": now_s if on_air else cursor.get("last_bulletin_at"),
        "keys": dict(sorted(keys.items())),
    }
    unsafe = [f"{name}: {where}" for name, data in outputs.items()
              for where in unsafe_urls(data)]
    if unsafe:
        raise WriterError("refusing to publish unsafe URLs: " + "; ".join(unsafe[:5]))
    summary = {"on_air": on_air, "id": run_id, "auto_resolved": auto,
               "archived": [row["slug"] for row in archived],
               "history_archived": len(moved),
               "threads": len(threads), "audio": audio is not None}
    return outputs, summary


# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------

def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-c", "core.hooksPath=/dev/null",
                           "-c", "core.fsmonitor=false", "-C", str(repo), *args],
                          check=check, capture_output=True, text=True)


def commit_paths(repo: Path, paths: list[str], message: str) -> bool:
    """Stage and commit exactly `paths`; return True when a commit was made."""
    _git(repo, "add", "--", *paths)
    if _git(repo, "diff", "--cached", "--quiet", "--", *paths, check=False).returncode == 0:
        return False
    _git(repo, "commit", "--quiet", "-m", message, "--", *paths)
    changed = _git(repo, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r",
                   "HEAD").stdout
    outside = sorted(set(changed.split()) - set(paths))
    if outside:
        raise WriterError(f"commit touched unexpected paths: {outside}")
    return True


def commit_message(on_air: bool, now: dt.datetime) -> str:
    stamp = now.strftime("%Y-%m-%d %H:%M UTC")
    return f"Aradio bulletin {stamp}" if on_air else f"Aradio board update {stamp}"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def write(*, repo_root: Path, edit_raw: Any, inbox: contract.TrustedInbox, now: dt.datetime,
          tts_result: dict | None, audio_key: str | None, audio_error: str | None,
          backend: str, model: str, commit: bool) -> dict:
    lane = repo_root / LANE_DIR
    now_s = iso_z(now)
    board = contract.load_board(lane / "state.json")
    cursor = _load_optional(lane / "cursor.json") or empty_cursor()
    if not isinstance(cursor, dict) or not isinstance(cursor.get("keys", {}), dict):
        raise WriterError("cursor.json must be an object with a keys map")
    run_id = bulletin_id(now)

    if cursor.get("last_editor_run_at") == now_s:
        # Already applied for this run stamp: never apply ops twice. The
        # archive is committed with the rest, or history trimmed out of
        # state.json by the first attempt would be committed without it.
        names = ("state.json", "cursor.json", "index.json",
                 f"archive/{now.strftime('%Y-%m')}.json", bulletin_relpath(now))
        written = [str(LANE_DIR / name) for name in names if (lane / name).exists()]
        committed = commit and commit_paths(repo_root, written, commit_message(
            cursor.get("last_bulletin_at") == now_s, now))
        return {"applied": False, "already_applied": True, "committed": committed,
                "paths": written, "id": run_id}
    if (lane / bulletin_relpath(now)).exists():
        raise WriterError(f"bulletin {bulletin_relpath(now)} already exists but cursor.json "
                          "does not record this run; refusing to overwrite")

    edit, report = contract.validate_edit(edit_raw, inbox, board)
    if edit is None:
        raise WriterError("edit failed re-validation: " + "; ".join(report.errors[:5]))
    # First-pass warnings describe repairs whose inputs are gone (e.g. dropped
    # URLs), so they are carried over; they are plain strings, bounded.
    carried = edit_raw.get("warnings") if isinstance(edit_raw, dict) else None
    carried = [contract.clip(contract.defang(contract.clean_text(w)), 300)[0]
               for w in (carried if isinstance(carried, list) else []) if isinstance(w, str)]
    edit["warnings"] = list(dict.fromkeys(carried + list(report.warnings)))[:MAX_WARNINGS]

    audio, error = audio_outcome(edit["on_air"], run_id, tts_result, audio_key, audio_error)
    index = _load_optional(lane / "index.json")
    archive = _load_optional(lane / "archive" / f"{now.strftime('%Y-%m')}.json")
    outputs, summary = compose(edit=edit, inbox=inbox, board=board, cursor=cursor,
                               index=index if isinstance(index, dict) else None,
                               archive=archive, now=now, audio=audio, audio_error=error,
                               backend=backend, model=model)
    ordered = sorted(outputs, key=lambda name: (name == "cursor.json", name == "state.json",
                                                name))
    for name in ordered:
        contract.atomic_write_json(lane / name, outputs[name])
    paths = [str(LANE_DIR / name) for name in ordered]
    committed = commit and commit_paths(repo_root, paths, commit_message(edit["on_air"], now))
    summary.update({"applied": True, "already_applied": False, "committed": committed,
                    "paths": paths, "audio_error": error})
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--edit", type=Path, required=True, help="normalized edit JSON")
    parser.add_argument("--inbox", type=Path, required=True, help="trusted inbox.json")
    parser.add_argument("--now", required=True, help="run stamp YYYY-MM-DDTHH:MM:00Z")
    parser.add_argument("--tts-result", type=Path, default=None)
    parser.add_argument("--audio-key", default="")
    parser.add_argument("--audio-error", default="")
    parser.add_argument("--backend", default="")
    parser.add_argument("--model", default="")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--no-commit", action="store_true")
    parser.add_argument("--github-output", default=None)
    args = parser.parse_args(argv)

    if not STAMP_RE.match(args.now):
        parser.error("--now must be a minute-aligned UTC stamp YYYY-MM-DDTHH:MM:00Z")
    now = parse_ts(args.now)
    try:
        edit_raw = json.loads(args.edit.read_text(encoding="utf-8"))
        inbox = contract.TrustedInbox.load(args.inbox)
        tts_result = None
        if args.tts_result is not None and args.tts_result.is_file():
            tts_result = json.loads(args.tts_result.read_text(encoding="utf-8"))
            if not isinstance(tts_result, dict):
                tts_result = None
        summary = write(repo_root=args.repo_root.resolve(), edit_raw=edit_raw, inbox=inbox,
                        now=now, tts_result=tts_result, audio_key=args.audio_key.strip() or None,
                        audio_error=args.audio_error.strip() or None,
                        backend=contract.clean_text(args.backend)[:80],
                        model=contract.clean_text(args.model)[:120],
                        commit=not args.no_commit)
    except (OSError, ValueError, WriterError, subprocess.CalledProcessError) as exc:
        print(f"::error::aradio writer: {contract.gh_escape(exc)}")
        return EXIT_ERROR

    if summary.get("already_applied"):
        print(f"aradio writer: run {summary['id']} was already applied; no ops re-applied")
    else:
        print(f"aradio writer: {'bulletin' if summary['on_air'] else 'board update'} "
              f"{summary['id']} -> {len(summary['paths'])} file(s); threads={summary['threads']} "
              f"auto_resolved={len(summary['auto_resolved'])} archived={len(summary['archived'])} "
              f"history_archived={summary['history_archived']} "
              f"audio={'yes' if summary['audio'] else 'no'} "
              f"committed={'yes' if summary['committed'] else 'no'}")
    contract.write_github_output(args.github_output, {
        "committed": "true" if summary.get("committed") else "false",
        "bulletin_id": summary["id"],
    })
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
