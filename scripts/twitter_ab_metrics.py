#!/usr/bin/env python3
"""Metrics, blinding, and de-blinding for the Twitter model A/B eval.

Used by .github/workflows/twitter-model-ab.yml (design doc:
docs/twitter-model-ab.md). STDLIB ONLY (plus sibling script imports) so it
runs anywhere the pipeline does. Two subcommands:

collect
    Parse per-leg run metadata (written by the workflow), the Claude Code
    execution transcript of each leg, and each leg's output directory into
    `research/eval/twitter-ab/<date>/metrics.json`. When BOTH legs produced
    the main digest .md, also stage the BLINDED judge inputs:
    `<judge-dir>/pass1/{A,B}.md` and `<judge-dir>/pass2/{A,B}.md` (pass 2 is
    the position-swapped copy), with the leg→letter assignment randomized
    per run. The mapping is recorded ONLY in metrics.json — never inside the
    judge-visible files — and a fixed list of model/provider/lane strings is
    scrubbed from the copies (URLs are preserved: they come verbatim from
    the shared input snapshot and carry no authorship signal).

finalize
    Read the two judge verdicts (either may be missing/garbled — fail open),
    de-blind letter→leg via the mapping in metrics.json, write the committed
    `judge-verdict.json`, and merge the judge summary back into metrics.json.

Every leg is optional end-to-end: a leg that wrote nothing is scored
mechanically as such and the judge stage is skipped.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_twitter_public_output as vt  # noqa: E402

REQUIRED_ARTIFACTS = ("status", "summary", "headlines")
LETTERS = ("A", "B")

# Model/provider/lane identifiers scrubbed from judge copies (blinding).
# Longest-first so specific ids are replaced before family names. Applied
# case-insensitively OUTSIDE URLs; both letters get the identical treatment,
# so any content loss is symmetric. The judge prompt tells the judge not to
# penalize the placeholder.
SCRUB_TOKENS = [
    "twitter-ab-judge-swapped",
    "twitter-ab-judge",
    "twitter-ab-claude",
    "twitter-ab-zai",
    "claude-opus-4-8",
    "claude-sonnet-5",
    "zai-glm-5p2",
    "glm-5.2",
    "glm-5p2",
    "anthropic",
    "deepseek",
    "fireworks",
    "claude",
    "sonnet",
    "zhipu",
    "haiku",
    "kimi",
    "opus",
    "z.ai",
    "glm",
    "zai",
]
SCRUB_PLACEHOLDER = "[redacted]"
URL_RE = re.compile(r"https?://[^\s<>\"')\]]+")
_SCRUB_RE = re.compile(
    "|".join(
        r"(?<![A-Za-z0-9])" + re.escape(token) + r"(?![A-Za-z0-9])"
        for token in SCRUB_TOKENS
    ),
    re.IGNORECASE,
)

def atomic_write_text(path: Path, text: str) -> None:
    """Same-directory temp file + os.replace (repo load-bearing rule 8)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def atomic_write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, sort_keys=False) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def scrub_text(text: str) -> tuple[str, int]:
    """Replace scrub-listed tokens outside URLs. Returns (scrubbed, hits)."""
    pieces: list[str] = []
    hits = 0
    pos = 0
    for url in URL_RE.finditer(text):
        segment, n = _SCRUB_RE.subn(SCRUB_PLACEHOLDER, text[pos : url.start()])
        hits += n
        pieces.append(segment)
        pieces.append(url.group(0))  # URLs pass through verbatim
        pos = url.end()
    segment, n = _SCRUB_RE.subn(SCRUB_PLACEHOLDER, text[pos:])
    hits += n
    pieces.append(segment)
    return "".join(pieces), hits


def parse_stream_objects(text: str) -> list[dict[str, Any]]:
    """Parse a Claude Code execution transcript: JSONL, a JSON array, or
    concatenated JSON documents. Returns the flat list of dict objects."""
    objects: list[dict[str, Any]] = []
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(text):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos >= len(text):
            break
        try:
            obj, end = decoder.raw_decode(text, pos)
        except json.JSONDecodeError:
            line_end = text.find("\n", pos)
            if line_end == -1:
                break
            pos = line_end + 1
            continue
        if isinstance(obj, dict):
            objects.append(obj)
        elif isinstance(obj, list):
            objects.extend(o for o in obj if isinstance(o, dict))
        pos = end
    return objects


def extract_result(execution_path: Path | None) -> dict[str, Any]:
    """Extract the final `type: result` object from an execution transcript.

    Returns a dict that always contains `result_found`; the other keys are
    None when absent so downstream rendering never KeyErrors.
    """
    out: dict[str, Any] = {
        "result_found": False,
        "is_error": None,
        "subtype": None,
        "num_turns": None,
        "duration_ms": None,
        "duration_api_ms": None,
        "total_cost_usd": None,
        "permission_denials_count": None,
        "observed_models": [],
        "usage": None,
    }
    if execution_path is None or not execution_path.exists():
        return out
    try:
        objects = parse_stream_objects(
            execution_path.read_text(encoding="utf-8", errors="replace")
        )
    except OSError:
        return out
    result = None
    for obj in objects:
        if obj.get("type") == "result" or "num_turns" in obj:
            result = obj
    if result is None:
        return out
    denials = result.get("permission_denials")
    model_usage = result.get("modelUsage")
    out.update(
        {
            "result_found": True,
            "is_error": result.get("is_error"),
            "subtype": result.get("subtype"),
            "num_turns": result.get("num_turns"),
            "duration_ms": result.get("duration_ms"),
            "duration_api_ms": result.get("duration_api_ms"),
            "total_cost_usd": result.get("total_cost_usd"),
            "permission_denials_count": len(denials)
            if isinstance(denials, list)
            else None,
            "observed_models": sorted(model_usage)
            if isinstance(model_usage, dict)
            else [],
            "usage": result.get("usage")
            if isinstance(result.get("usage"), dict)
            else None,
        }
    )
    return out


def leg_paths(leg_dir: Path, date: str, hour: str) -> dict[str, Path]:
    return {
        "digest": leg_dir / f"{date}.md",
        "status": leg_dir / "status" / f"{date}-{hour}h.json",
        "summary": leg_dir / f"{date}-twitter-ab-{hour}h-summary.txt",
        "headlines": leg_dir / f"{date}-twitter-ab-{hour}h-headlines.json",
    }


def count_section_items(digest_path: Path, hour: str) -> dict[str, Any]:
    """Story-card / quick-hit counts for the same-hour section (best effort)."""
    counts: dict[str, Any] = {
        "section_present": False,
        "counted_public_items": None,
        "story_cards": None,
    }
    if not digest_path.exists():
        return counts
    try:
        text = digest_path.read_text(encoding="utf-8")
    except OSError:
        return counts
    sections = vt.cycle_sections(text, hour)
    if not sections:
        return counts
    section = sections[0]
    counts["section_present"] = True
    counts["counted_public_items"] = vt.public_item_count(section)
    counts["story_cards"] = len(
        [
            m
            for m in vt.STORY_BLOCK_RE.finditer(section)
            if "twitter-story" in (m.group("attrs") or "")
        ]
    )
    return counts


def check_format(
    paths: dict[str, Path], date: str, hour: str, timestamp: str, run_id: str,
    run_attempt: int,
) -> dict[str, Any]:
    """Run the production signal-only contract validator against a leg."""
    result: dict[str, Any] = {"valid": False, "error": None}
    try:
        vt.validate(
            backend="claude",  # contract selector: both legs write the 3-artifact (headlines) shape
            status_file=paths["status"],
            digest_file=paths["digest"],
            summary_file=paths["summary"],
            headlines_file=paths["headlines"],
            date=date,
            hour=hour,
            generated_at=timestamp,
            run_id=run_id,
            run_attempt=run_attempt,
        )
        result["valid"] = True
    except vt.ContractError as exc:
        result["error"] = str(exc)
    except OSError as exc:  # unreadable artifact — still a mechanical failure
        result["error"] = f"artifact unreadable: {exc}"
    return result


def collect_leg(
    meta: dict[str, Any], *, date: str, hour: str, timestamp: str, run_id: str,
    run_attempt: int, snapshot_sha: str,
) -> dict[str, Any]:
    leg_dir = Path(str(meta.get("leg_dir", "")))
    paths = leg_paths(leg_dir, date, hour)
    exec_path_raw = str(meta.get("execution_file") or "")
    agent = extract_result(Path(exec_path_raw) if exec_path_raw else None)

    artifacts = {name: paths[name].exists() for name in paths}
    required_written = sum(1 for name in REQUIRED_ARTIFACTS if artifacts[name])

    status_state = None
    public_items = None
    if artifacts["status"]:
        try:
            status = read_json(paths["status"])
            if isinstance(status, dict):
                status_state = status.get("status")
                public_items = status.get("public_items")
        except (json.JSONDecodeError, OSError):
            status_state = "unparseable"
    headline_count = None
    if artifacts["headlines"]:
        try:
            headlines = read_json(paths["headlines"])
            headline_count = len(headlines) if isinstance(headlines, list) else None
        except (json.JSONDecodeError, OSError):
            headline_count = None

    fmt = check_format(paths, date, hour, timestamp, run_id, run_attempt)
    counts = count_section_items(paths["digest"], hour)

    expected_provider = str(meta.get("expected_provider", ""))
    expected_model = str(meta.get("expected_model", ""))
    served_model = str(
        (
            meta.get("native_model")
            if expected_provider == "claude"
            else meta.get("model_id")
        )
        or ""
    )
    requested = str(meta.get("requested_backend", ""))
    effective = str(meta.get("effective_backend", ""))
    used_fallback = str(meta.get("used_fallback", "")).lower() == "true"

    started = meta.get("started_at_epoch")
    finished = meta.get("finished_at_epoch")
    wall_time = None
    if isinstance(started, int) and isinstance(finished, int) and finished >= started:
        wall_time = finished - started

    sha_pre = str(meta.get("input_sha_pre", ""))
    sha_post = str(meta.get("input_sha_post", ""))
    matches_snapshot = bool(snapshot_sha) and sha_pre == snapshot_sha
    unchanged = bool(sha_pre) and sha_pre == sha_post

    base_sha = str(meta.get("base_sha", ""))
    post_sha = str(meta.get("post_sha", ""))

    flags: list[str] = []
    outcome = str(meta.get("outcome", ""))
    if outcome != "success":
        flags.append("leg-failed")
    if not agent["result_found"]:
        flags.append("no-result-json")
    if agent["is_error"] is True:
        flags.append("agent-error")
    if not effective or requested != effective or used_fallback:
        flags.append("backend-mismatch")
    if expected_model and served_model != expected_model:
        flags.append("model-mismatch")
    if agent["observed_models"] and expected_model and expected_model not in agent["observed_models"]:
        flags.append("expected-model-not-observed")
    if not matches_snapshot:
        flags.append("input-mismatch")
    if not unchanged:
        flags.append("input-mutated")
    if isinstance(agent["permission_denials_count"], int) and agent["permission_denials_count"] > 0:
        flags.append("sandbox-suspect")
    if not fmt["valid"]:
        flags.append("format-invalid")
    if not post_sha or post_sha == base_sha:
        flags.append("no-commit")

    return {
        "lane": meta.get("lane"),
        "leg_dir": str(leg_dir),
        "outcome": outcome,
        "backend": {
            "requested": requested,
            "effective": effective,
            "used_fallback": used_fallback,
            "model_id": meta.get("model_id"),
            "native_model": meta.get("native_model"),
            "expected_provider": expected_provider,
            "expected_model": expected_model,
            "served_model": served_model,
            "observed_models": agent["observed_models"],
        },
        "agent": {k: v for k, v in agent.items() if k != "observed_models"},
        "wall_time_seconds": wall_time,
        "artifacts": {
            **artifacts,
            "required_written": f"{required_written}/{len(REQUIRED_ARTIFACTS)}",
        },
        "format": {
            **fmt,
            "status": status_state,
            "public_items": public_items,
            "headline_count": headline_count,
            **counts,
        },
        "input_integrity": {
            "sha_pre": sha_pre,
            "sha_post": sha_post,
            "matches_snapshot": matches_snapshot,
            "unchanged_during_leg": unchanged,
        },
        "prompt_sha256": meta.get("prompt_sha256"),
        "commits": {
            "base_sha": base_sha,
            "post_sha": post_sha,
            "committed": bool(post_sha) and post_sha != base_sha,
        },
        "flags": flags,
    }


CONTAMINATION_FLAGS = {
    "backend-mismatch",
    "model-mismatch",
    "expected-model-not-observed",
    "input-mismatch",
    "input-mutated",
}


def build_judge_document(leg: str, legs: dict[str, Any], date: str, hour: str) -> str | None:
    """Composite blinded document for one leg: digest + headlines + summary +
    status. Returns None when the leg produced no main digest."""
    leg_dir = Path(str(legs[leg]["leg_dir"]))
    paths = leg_paths(leg_dir, date, hour)
    if not paths["digest"].exists():
        return None
    digest = paths["digest"].read_text(encoding="utf-8", errors="replace")

    def optional(path: Path, empty: str) -> str:
        if not path.exists():
            return "(missing)"
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        return text if text else empty

    return "\n".join(
        [
            "## Public digest (markdown)",
            "",
            digest.strip(),
            "",
            "## Headline alerts (JSON)",
            "",
            "```json",
            optional(paths["headlines"], "(empty)"),
            "```",
            "",
            "## Telegram summary",
            "",
            "```",
            optional(paths["summary"], "(empty file — no notification)"),
            "```",
            "",
            "## Machine status (JSON)",
            "",
            "```json",
            optional(paths["status"], "(empty)"),
            "```",
            "",
        ]
    )


def stage_judge_inputs(
    legs: dict[str, Any], judge_dir: Path, *, date: str, hour: str,
    input_json: Path | None, seed: int | None,
) -> tuple[dict[str, Any] | None, str | None]:
    """Write blinded pass1/pass2 inputs. Returns (blinding, skip_reason)."""
    leg_names = list(legs)
    if len(leg_names) != 2:
        return None, f"judge requires exactly 2 legs, got {len(leg_names)}"

    documents: dict[str, str] = {}
    for leg in leg_names:
        doc = build_judge_document(leg, legs, date, hour)
        if doc is None:
            return None, f"leg '{leg}' produced no main digest .md"
        documents[leg] = doc

    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    ordered = list(leg_names)
    if rng.random() < 0.5:
        ordered.reverse()
    pass1 = dict(zip(LETTERS, ordered))
    pass2 = dict(zip(LETTERS, reversed(ordered)))

    scrub_hits: dict[str, int] = {}
    for pass_name, mapping in (("pass1", pass1), ("pass2", pass2)):
        for letter, leg in mapping.items():
            scrubbed, hits = scrub_text(documents[leg])
            scrub_hits[leg] = hits  # same doc both passes — same count
            atomic_write_text(
                judge_dir / pass_name / f"{letter}.md",
                f"# Brief {letter}\n\n{scrubbed}",
            )

    snapshot_staged = False
    if input_json is not None and input_json.exists():
        try:
            snapshot = read_json(input_json)
            # Pretty-print: all.json is minified to one line, which the
            # judge's Read tool cannot page through. NOT scrubbed — it is
            # the shared input, identical for both legs.
            atomic_write_text(
                judge_dir / "snapshot.json", json.dumps(snapshot, indent=1)
            )
            snapshot_staged = True
        except (json.JSONDecodeError, OSError):
            snapshot_staged = False

    blinding = {
        "pass1": pass1,
        "pass2": pass2,
        "scrub_hits": scrub_hits,
        "snapshot_staged": snapshot_staged,
    }
    return blinding, None


def cmd_collect(args: argparse.Namespace) -> int:
    legs: dict[str, Any] = {}
    for meta_path in args.leg_meta:
        path = Path(meta_path)
        if not path.exists():
            print(f"::warning::leg meta missing, leg skipped: {path}")
            continue
        try:
            meta = read_json(path)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"::warning::unreadable leg meta {path}: {exc}")
            continue
        leg_name = str(meta.get("leg", "")).strip()
        if not leg_name:
            print(f"::warning::leg meta {path} has no 'leg' key; skipped")
            continue
        legs[leg_name] = collect_leg(
            meta,
            date=args.date,
            hour=args.hour,
            timestamp=args.timestamp,
            run_id=args.run_id,
            run_attempt=args.run_attempt,
            snapshot_sha=args.snapshot_sha,
        )

    total_tweets = None
    input_json = Path(args.input_json) if args.input_json else None
    if input_json is not None and input_json.exists():
        try:
            meta_block = read_json(input_json).get("meta", {})
            if isinstance(meta_block, dict):
                total_tweets = meta_block.get("total_tweets")
        except (json.JSONDecodeError, OSError):
            total_tweets = None

    blinding = None
    judge_skip_reason: str | None = "judge disabled"
    if args.judge_dir:
        blinding, judge_skip_reason = stage_judge_inputs(
            legs,
            Path(args.judge_dir),
            date=args.date,
            hour=args.hour,
            input_json=input_json,
            seed=args.blind_seed,
        )

    reasons = sorted(
        {
            f"{leg}:{flag}"
            for leg, data in legs.items()
            for flag in data["flags"]
            if flag in CONTAMINATION_FLAGS
        }
    )
    sandbox_suspect = any("sandbox-suspect" in data["flags"] for data in legs.values())

    metrics = {
        "schema_version": 1,
        "kind": "twitter-model-ab-metrics",
        "date": args.date,
        "hour": f"{args.hour}:00 UTC",
        "generated_at": args.timestamp,
        "run_id": args.run_id,
        "run_attempt": args.run_attempt,
        "input": {
            "all_json_sha256": args.snapshot_sha,
            "manifest_sha256": args.manifest_sha,
            "total_tweets": total_tweets,
        },
        "parity": {
            "normalized_prompt_sha256": args.normalized_prompt_sha,
            "allowed_asymmetries": [
                "API_TIMEOUT_MS=3000000 on the Z.ai route (provider-latency accommodation)",
                "CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000 on the Z.ai route",
                "CLAUDE_CODE_EFFORT_LEVEL=max on the non-native routes (pre-existing agent-run provider env)",
            ],
        },
        "legs": legs,
        "blinding": blinding,
        "judge_staged": blinding is not None,
        "judge_skip_reason": judge_skip_reason,
        "judge": None,
        "contamination": {
            "contaminated": bool(reasons),
            "reasons": reasons,
            "sandbox_suspect": sandbox_suspect,
        },
    }
    atomic_write_json(Path(args.out), metrics)
    print(
        f"metrics written: {args.out} (legs={list(legs)}, "
        f"judge_staged={blinding is not None}, contaminated={bool(reasons)})"
    )
    return 0


def parse_verdict(path: Path) -> dict[str, Any] | None:
    """Parse one judge verdict file; tolerate code fences / surrounding prose."""
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return None
    for candidate in (text,):
        try:
            data = json.loads(candidate)
            break
        except json.JSONDecodeError:
            data = None
    if data is None:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match is None:
            return None
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    if not isinstance(data, dict):
        return None
    scores = data.get("scores")
    preferred = data.get("preferred")
    if not isinstance(scores, dict) or preferred not in {"A", "B", "tie"}:
        return None
    return data


def _clamp_score(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return max(1.0, min(10.0, float(value)))


def deblind_pass(
    verdict: dict[str, Any], mapping: dict[str, str], pass_number: int
) -> dict[str, Any]:
    scores_by_leg: dict[str, Any] = {}
    rationale_by_leg: dict[str, Any] = {}
    rationales = verdict.get("rationale")
    for letter, leg in mapping.items():
        letter_scores = verdict.get("scores", {}).get(letter)
        if isinstance(letter_scores, dict):
            cleaned = {
                key: _clamp_score(val)
                for key, val in letter_scores.items()
                if _clamp_score(val) is not None
            }
            if "overall" not in cleaned and cleaned:
                cleaned["overall"] = round(
                    sum(cleaned.values()) / len(cleaned), 2
                )
            scores_by_leg[leg] = cleaned
        if isinstance(rationales, dict) and isinstance(rationales.get(letter), str):
            rationale_by_leg[leg] = rationales[letter]
    preferred_letter = verdict.get("preferred")
    preferred_leg = (
        "tie" if preferred_letter == "tie" else mapping.get(str(preferred_letter), "")
    )
    return {
        "pass": pass_number,
        "parsed": True,
        "letter_to_leg": mapping,
        "raw_preferred_letter": preferred_letter,
        "preferred_leg": preferred_leg,
        "scores_by_leg": scores_by_leg,
        "rationale_by_leg": rationale_by_leg,
    }


def cmd_finalize(args: argparse.Namespace) -> int:
    metrics_path = Path(args.metrics)
    try:
        metrics = read_json(metrics_path)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"::error::cannot read metrics {metrics_path}: {exc}", file=sys.stderr)
        return 1

    blinding = metrics.get("blinding") or {}
    judge_dir = Path(args.judge_dir)
    passes: list[dict[str, Any]] = []
    for pass_number, (verdict_name, mapping_key) in enumerate(
        (("verdict-1.json", "pass1"), ("verdict-2.json", "pass2")), start=1
    ):
        mapping = blinding.get(mapping_key)
        verdict = parse_verdict(judge_dir / verdict_name)
        if verdict is None or not isinstance(mapping, dict):
            passes.append(
                {
                    "pass": pass_number,
                    "parsed": False,
                    "reason": "verdict missing/unparseable"
                    if isinstance(mapping, dict)
                    else "no blinding mapping (judge was not staged)",
                }
            )
            continue
        passes.append(deblind_pass(verdict, mapping, pass_number))

    parsed = [p for p in passes if p.get("parsed")]
    leg_names = list((metrics.get("legs") or {}).keys())
    per_leg: dict[str, Any] = {}
    for leg in leg_names:
        criteria_totals: dict[str, list[float]] = {}
        overalls: list[float] = []
        for p in parsed:
            scores = p["scores_by_leg"].get(leg)
            if not isinstance(scores, dict):
                continue
            for key, val in scores.items():
                if key == "overall":
                    overalls.append(val)
                else:
                    criteria_totals.setdefault(key, []).append(val)
        if overalls or criteria_totals:
            per_leg[leg] = {
                "overall_avg": round(sum(overalls) / len(overalls), 2)
                if overalls
                else None,
                "criteria_avg": {
                    key: round(sum(vals) / len(vals), 2)
                    for key, vals in sorted(criteria_totals.items())
                },
                "passes_scored": len(
                    [p for p in parsed if leg in p["scores_by_leg"]]
                ),
            }

    if len(parsed) == 2:
        prefs = [p["preferred_leg"] for p in parsed]
        final_preference = prefs[0] if prefs[0] == prefs[1] else "split"
    elif len(parsed) == 1:
        final_preference = parsed[0]["preferred_leg"]
    else:
        final_preference = "none"

    judge = {
        "schema_version": 1,
        "kind": "twitter-model-ab-judge-verdict",
        "date": metrics.get("date"),
        "run_id": metrics.get("run_id"),
        "run_attempt": metrics.get("run_attempt"),
        "judge_model": args.judge_model,
        "position_swap": True,
        "blinding": {
            "pass1": blinding.get("pass1"),
            "pass2": blinding.get("pass2"),
        },
        "passes": passes,
        "per_leg": per_leg,
        "passes_parsed": len(parsed),
        "final_preference": final_preference,
    }
    atomic_write_json(Path(args.out_verdict), judge)

    metrics["judge"] = {
        "judge_model": args.judge_model,
        "passes_parsed": len(parsed),
        "per_leg": per_leg,
        "final_preference": final_preference,
        "verdict_file": str(args.out_verdict),
    }
    atomic_write_json(metrics_path, metrics)
    print(
        f"judge verdict written: {args.out_verdict} "
        f"(passes_parsed={len(parsed)}, final_preference={final_preference})"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    collect = sub.add_parser("collect", help="build metrics.json + stage blinded judge inputs")
    collect.add_argument("--date", required=True)
    collect.add_argument("--hour", required=True)
    collect.add_argument("--timestamp", required=True)
    collect.add_argument("--run-id", required=True)
    collect.add_argument("--run-attempt", type=int, required=True)
    collect.add_argument("--leg-meta", action="append", default=[],
                         help="per-leg meta JSON written by the workflow (repeatable)")
    collect.add_argument("--snapshot-sha", default="",
                         help="sha256 of the shared .ab-input/bird/all.json snapshot")
    collect.add_argument("--manifest-sha", default="",
                         help="aggregate sha256 over every staged input file")
    collect.add_argument("--input-json", default="",
                         help="path to the shared all.json (for total_tweets + judge snapshot)")
    collect.add_argument("--judge-dir", default="",
                         help="directory to stage blinded judge inputs into (empty = judge disabled)")
    collect.add_argument("--normalized-prompt-sha", default="",
                         help="sha256 both legs' prompts share after leg-dir normalization")
    collect.add_argument("--blind-seed", type=int, default=None,
                         help="deterministic blinding seed (tests only)")
    collect.add_argument("--out", required=True)
    collect.set_defaults(func=cmd_collect)

    finalize = sub.add_parser("finalize", help="de-blind judge verdicts into judge-verdict.json")
    finalize.add_argument("--metrics", required=True)
    finalize.add_argument("--judge-dir", required=True)
    finalize.add_argument("--judge-model", default="claude-opus-4-8")
    finalize.add_argument("--out-verdict", required=True)
    finalize.set_defaults(func=cmd_finalize)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
