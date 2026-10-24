#!/usr/bin/env python3
"""Export sanitized research evidence via OTLP/HTTP; fetch RSI evidence via v2.

Run --help for offline preview and live commands. Never run this with Langfuse
keys inside an agent job; the workflow uses a fresh, separate reporting job.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from research_trace import ATTEMPTS, MAX_EVENTS, OUTCOMES, TOOLS, USAGE_FIELDS, choice, digest, known_identifiers, number, read_regular, summary, write_json

TRACE_NAME = "ara.generative-research"
STAGES = {
    **ATTEMPTS,
    "gen-codex": "Run Generative Research (Codex)",
    "gen-opencode": "Run Generative Research (OpenCode Go)",
    "gen-cursor": "Run Generative Research (Cursor CLI)",
    "quality": "Post-write quality gate",
    "verifier-audit": "Verifier-findings audit",
    "methodology": "Methodology artifact gate",
    "push": "Push changes",
    "fireworks-preflight": "Preflight Fireworks backend",
    "outfile": "Identify generated file",
    "provenance": "Verify pinned model provenance",
    "no-article-codex": "Fail Codex run without article",
    "no-article-opencode": "Fail OpenCode run without article",
    "no-article-cursor": "Fail Cursor run without article",
    "no-article-claude": "Fail Claude run without article",
    "no-article-fireworks": "Fail Fireworks run without article",
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("redirect refused")


class Langfuse:
    def __init__(self):
        self.base = os.environ.get("LANGFUSE_BASE_URL", "").rstrip("/")
        public = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
        secret = os.environ.get("LANGFUSE_SECRET_KEY", "")
        url = urllib.parse.urlsplit(self.base)
        if not public or not secret or url.scheme != "https" or not url.hostname or url.username or url.password or url.query or url.fragment:
            raise ValueError("Langfuse HTTPS base URL and both keys are required")
        self.headers = {"Authorization": "Basic " + base64.b64encode(f"{public}:{secret}".encode()).decode(),
                        "Content-Type": "application/json", "x-langfuse-ingestion-version": "4"}
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, path, payload=None):
        data = json.dumps(payload, allow_nan=False).encode() if payload is not None else None
        for attempt in range(2):
            try:
                request = urllib.request.Request(self.base + path, data=data, headers=self.headers)
                with self.opener.open(request, timeout=15) as response:
                    raw = response.read(8 * 1024 * 1024 + 1)
                    if len(raw) > 8 * 1024 * 1024:
                        raise ValueError("Langfuse response exceeds limit")
                    return json.loads(raw) if raw else {}
            except urllib.error.HTTPError as exc:
                if attempt == 0 and (exc.code == 429 or exc.code >= 500):
                    time.sleep(1)
                    continue
                # No response body: it may contain keys or private input.
                raise RuntimeError(f"Langfuse HTTP {exc.code}") from None
            except urllib.error.URLError:
                if attempt == 0:
                    time.sleep(1)
                    continue
                raise RuntimeError("Langfuse network error") from None


def nanos(value: str) -> int:
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp() * 1_000_000_000)


def attr(key, value):
    if isinstance(value, bool):
        encoded = {"boolValue": value}
    elif isinstance(value, int):
        encoded = {"intValue": str(value)}
    elif isinstance(value, float):
        encoded = {"doubleValue": value}
    elif isinstance(value, list):
        encoded = {"arrayValue": {"values": [{"stringValue": str(v)} for v in value]}}
    else:
        encoded = {"stringValue": str(value)}
    return {"key": key, "value": encoded}


def load_record(directory: Path, name: str) -> dict:
    try:
        result = json.loads(read_regular(directory / f"{name}.json", 2 * 1024 * 1024))
        return result if isinstance(result, dict) and result.get("schema_version") == 1 else {}
    except (OSError, ValueError, RecursionError):
        return {}


def trusted_summary(record, registry):
    # Re-project in the fresh job: uploaded artifacts are untrusted data even
    # when the producer used the normal sanitizer. Never forward arbitrary keys.
    steps = {key: {"outcome": value} for key, value in record.get("outcomes", {}).items()} if isinstance(record.get("outcomes"), dict) else {}
    def flag(key):
        value = record.get(key)
        return str(value).lower() if type(value) is bool else None
    steps["effective"] = {"outputs": {"requested_backend": record.get("requested_backend"),
                                      "backend": record.get("effective_backend"),
                                      "used_fallback": flag("used_fallback")}}
    steps.setdefault("push", {})["outputs"] = {"pushed": flag("published")}
    steps["outfile"] = {"outputs": {"has_file": flag("has_article")}}
    return summary(steps, registry)


def build_trace(bundle: Path, job: dict, registry: dict, *, repository: str,
                run_id: str, run_attempt: str, source_sha: str, environment: str) -> dict:
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", repository) or not run_id.isdigit() or not run_attempt.isdigit() or not re.fullmatch(r"[a-f0-9]{40}", source_sha):
        raise ValueError("invalid run identity")
    trace_id = digest(f"ara:{repository}:{run_id}:{run_attempt}")[:32]
    root_id = digest(trace_id + ":root")[:16]
    raw_summary = load_record(bundle, "summary")
    report = trusted_summary(raw_summary, registry)
    metadata = {"repository": repository, "run_id": run_id, "run_attempt": run_attempt,
                "source_sha": source_sha, "github_url": None if environment == "smoke-test" else f"https://github.com/{repository}/actions/runs/{run_id}/attempts/{run_attempt}",
                "schema_version": 1, "summary_available": bool(raw_summary),
                "content_policy": "metadata-only", **{k: v for k, v in report.items() if k not in {"outcomes", "schema_version"}}}
    shared = {"langfuse.trace.name": TRACE_NAME, "langfuse.session.id": f"{repository}:{run_id}",
              "langfuse.release": source_sha, "langfuse.environment": environment,
              "langfuse.trace.tags": ["ara", "generative-research"], "langfuse.trace.public": False,
              **{f"langfuse.trace.metadata.{k}": json.dumps(v) for k, v in metadata.items()}}
    spans = []

    def span(key, name, start, end, parent, kind="span", outcome="unknown", meta=None, extra=None):
        attributes = {**shared, "langfuse.observation.type": kind,
                      "langfuse.observation.metadata.outcome": json.dumps(outcome),
                      **{f"langfuse.observation.metadata.{k}": json.dumps(v) for k, v in (meta or {}).items()}, **(extra or {})}
        result = {"traceId": trace_id, "spanId": digest(trace_id + ":" + key)[:16], "name": name,
                  "kind": 1, "startTimeUnixNano": str(start), "endTimeUnixNano": str(max(start, end)),
                  "attributes": [attr(k, v) for k, v in attributes.items()],
                  "status": {"code": 2 if outcome in {"failure", "cancelled", "timed_out"} else 1 if outcome == "success" else 0}}
        if parent:
            result["parentSpanId"] = parent
        spans.append(result)
        return result["spanId"]

    start, end = nanos(job["started_at"]), nanos(job["completed_at"])
    span("root", TRACE_NAME, start, end, None, outcome=job.get("conclusion", "unknown"),
         meta={"outcomes": report["outcomes"], "coverage": "workflow-and-available-attempts"})
    steps = {step["name"]: step for step in job.get("steps", [])}
    models = known_identifiers(registry)
    attempt_summaries = []
    failed_stages = []
    for attempt, name in STAGES.items():
        step = steps.get(name)
        if not step or step.get("conclusion") == "skipped" or not step.get("started_at") or not step.get("completed_at"):
            continue
        record = load_record(bundle, attempt) if attempt in ATTEMPTS else {}
        coverage = choice(record.get("coverage"), {"structured", "missing", "unreadable", "unrecognized"},
                          "not-instrumented" if attempt.startswith("gen-") else "workflow")
        result = record.get("result") if isinstance(record.get("result"), dict) else {}
        events = record.get("events", [])
        events = events if isinstance(events, list) else []
        meta = {"attempt": attempt, "coverage": coverage,
                "events_capped": record.get("events_capped") is True or len(events) > MAX_EVENTS,
                "captured_event_count": min(len(events), MAX_EVENTS),
                "github_step_conclusion": choice(step.get("conclusion"), OUTCOMES | {"timed_out"})}
        fingerprint = record.get("transcript_sha256")
        if isinstance(fingerprint, str) and re.fullmatch(r"[0-9a-f]{64}", fingerprint):
            meta["transcript_sha256"] = fingerprint
        for key in ("duration_ms", "num_turns", "runtime_estimated_cost_usd"):
            value = number(result.get(key))
            if value is not None:
                meta[key] = value
        if type(result.get("is_error")) is bool:
            meta["session_is_error"] = result["is_error"]
        outcome = report["outcomes"].get(attempt, "unknown")
        # Agent steps use continue-on-error. GitHub's post-policy conclusion
        # "success" cannot recover their raw outcome when the capture is lost.
        if outcome == "unknown" and (not attempt.startswith("gen-") or step.get("conclusion") in {"failure", "cancelled", "timed_out"}):
            outcome = step.get("conclusion", "unknown")
        if outcome in {"failure", "cancelled", "timed_out"}:
            failed_stages.append(attempt)
        parent = span(attempt, name, nanos(step["started_at"]), nanos(step["completed_at"]), root_id,
                      kind="agent" if attempt.startswith("gen-") else "span", outcome=outcome, meta=meta)
        generation_ids = {}
        observed_models = set()
        reported_tokens = {}
        tool_outcomes = {"success": 0, "failure": 0, "unknown": 0}
        for index, event in enumerate(events[:MAX_EVENTS]):
            if not isinstance(event, dict) or choice(event.get("kind"), {"generation", "tool"}) == "unknown":
                continue
            kind = event["kind"]
            extra = {}
            event_meta = {"sequence": index, "timing": "not-reported"}
            event_parent = parent
            event_outcome = "unknown"
            if kind == "generation":
                model = event.get("model")
                model = model if isinstance(model, str) and model in models else "unknown"
                observed_models.add(model)
                event_meta["observed_model"] = model
                if model != "unknown":
                    extra["langfuse.observation.model.name"] = model
                usage = event.get("usage") if isinstance(event.get("usage"), dict) else {}
                tokens = {k: int(v) for k in USAGE_FIELDS if (v := number(usage.get(k))) is not None}
                for key, value in tokens.items():
                    reported_tokens[key] = reported_tokens.get(key, 0) + value
                if tokens:
                    # Explicit cache categories prevent treating cache hits as fresh input.
                    extra["langfuse.observation.usage_details"] = json.dumps({
                        {"input_tokens": "input", "output_tokens": "output",
                         "cache_read_input_tokens": "cache_read_input_tokens", "cache_creation_input_tokens": "cache_creation_input_tokens"}[k]: v for k, v in tokens.items()})
                event_name = "model generation"
            else:
                event_name = event.get("name") if isinstance(event.get("name"), str) and event["name"] in TOOLS else "other"
                generation = event.get("generation")
                event_parent = generation_ids.get(generation, parent) if type(generation) is int else parent
                event_outcome = choice(event.get("outcome"), OUTCOMES)
                tool_outcomes[event_outcome if event_outcome in {"success", "failure"} else "unknown"] += 1
            # The transcript has ordering, not reliable per-event timestamps.
            # Zero-duration markers explicitly report missing timing; the agent
            # step above has GitHub's measured wall time.
            marker = nanos(step["completed_at"])
            event_id = span(f"{attempt}:{index}", event_name, marker, marker, event_parent,
                            kind=kind, outcome=event_outcome, meta=event_meta, extra=extra)
            if kind == "generation":
                generation_ids[index] = event_id
        if attempt.startswith("gen-"):
            attempt_summaries.append({**meta, "outcome": outcome, "observed_models": sorted(observed_models),
                                      "reported_tokens": reported_tokens or None,
                                      "tool_outcomes": tool_outcomes if events else None})
    # Bounded diagnostics for the weekly reader, without N+1 child requests.
    spans[0]["attributes"].append(attr("langfuse.observation.metadata.attempts", json.dumps(attempt_summaries)))
    spans[0]["attributes"].append(attr("langfuse.observation.metadata.failed_stages", json.dumps(failed_stages)))
    scores = []
    if raw_summary:
        values = {"research.published": report["published"]} if report["published"] is not None else {}
        for key in ("quality", "verifier-audit", "methodology"):
            if report["outcomes"][key] in {"success", "failure"}:
                values[f"research.{key}"] = report["outcomes"][key] == "success"
        for name, value in values.items():
            scores.append({"id": digest(trace_id + name), "traceId": trace_id, "name": name,
                           "value": int(value), "dataType": "BOOLEAN",
                           "timestamp": job["completed_at"], "environment": environment,
                           "comment": "Mechanical workflow outcome, not an editorial quality judgment. Evaluator: research-trace-v1."})
    return {"trace_id": trace_id, "spans": spans, "scores": scores}


def export(client: Langfuse, trace: dict) -> None:
    for offset in range(0, len(trace["spans"]), 200):
        response = client.request("/api/public/otel/v1/traces", {"resourceSpans": [{
            "resource": {"attributes": [attr("service.name", "ai-research-arm")]},
            "scopeSpans": [{"scope": {"name": "ara.research", "version": "1"}, "spans": trace["spans"][offset:offset + 200]}]}]})
        if not isinstance(response, dict):
            raise ValueError("malformed OTLP response")
        partial = response.get("partialSuccess") or {}
        if not isinstance(partial, dict):
            raise ValueError("malformed OTLP partial response")
        if int(partial.get("rejectedSpans", 0)) or partial.get("errorMessage"):
            raise RuntimeError("Langfuse rejected part of the trace")
    if trace["scores"]:
        client.request("/api/public/scores", trace["scores"])


def evidence(client: Langfuse, days: int) -> dict:
    now = datetime.now(timezone.utc)
    query = {"name": TRACE_NAME, "fromStartTime": (now - timedelta(days=days)).isoformat(),
             "toStartTime": now.isoformat(), "limit": 100, "fields": "core,basic,time,metadata",
             "expandMetadata": "outcomes,attempts,failed_stages", "isRootObservation": "true", "environment": "production"}
    rows = []
    truncated = False
    for _ in range(3):
        page = client.request("/api/public/v2/observations?" + urllib.parse.urlencode(query))
        if not isinstance(page, dict) or not isinstance(page.get("data"), list) or not isinstance(page.get("meta"), dict):
            raise ValueError("malformed observations page")
        for row in page["data"]:
            if not isinstance(row, dict):
                raise ValueError("malformed observation")
            if row.get("name") != TRACE_NAME or row.get("parentObservationId"):
                continue
            if row.get("environment") != "production":
                continue
            metadata = row.get("metadata") or {}
            if not isinstance(metadata, dict):
                continue
            # Evidence is treated as untrusted data by the consumer. No I/O,
            # exception messages, user IDs or arbitrary metadata is requested.
            safe = {k: metadata.get(k) for k in ("run_id", "run_attempt", "source_sha", "github_url", "requested_backend", "effective_backend", "used_fallback", "published", "summary_available", "outcomes", "attempts", "failed_stages")}
            rows.append({"trace_id": row.get("traceId"), "environment": "production",
                         "start_time": row.get("startTime"), "level": row.get("level"), **safe})
        cursor = page.get("meta", {}).get("cursor")
        if not cursor:
            break
        query["cursor"] = cursor
    else:
        truncated = True
    return {"schema_version": 1, "status": "ok", "window_days": days,
            "truncated": truncated, "runs": rows,
            "interpretation": "Diagnostic evidence only. Absence is not success; freeze replay inputs and evaluator before tuning."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    send = sub.add_parser("export", help="Build traces offline with --preview, otherwise export")
    send.add_argument("--bundle-dir", type=Path, required=True)
    send.add_argument("--jobs-file", type=Path, required=True)
    send.add_argument("--preview", type=Path)
    send.add_argument("--environment", choices=["production", "evaluation", "smoke-test"], default="production")
    read = sub.add_parser("evidence", help="Fetch bounded, content-free evidence for RSI")
    read.add_argument("--days", type=int, choices=range(1, 31), default=7)
    read.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "evidence":
            write_json(args.output, evidence(Langfuse(), args.days))
            print("Langfuse RSI evidence fetched")
            return 0
        jobs = json.loads(read_regular(args.jobs_file, 4 * 1024 * 1024))
        job = next(j for j in jobs["jobs"] if j["name"] == "generative-research")
        registry = json.loads(Path("data/agent-backends.json").read_text())
        trace = build_trace(args.bundle_dir, job, registry, repository=os.environ["GITHUB_REPOSITORY"],
                            run_id=os.environ["GITHUB_RUN_ID"], run_attempt=os.environ["GITHUB_RUN_ATTEMPT"],
                            source_sha=os.environ["RESEARCH_SOURCE_SHA"], environment=args.environment)
        if args.preview:
            write_json(args.preview, trace)
            print(f"Preview: {len(trace['spans'])} spans, {len(trace['scores'])} scores")
        else:
            export(Langfuse(), trace)
            print(f"Langfuse export accepted: trace_id={trace['trace_id']}, spans={len(trace['spans'])}")
        return 0
    except (OSError, ValueError, KeyError, TypeError, StopIteration, RuntimeError) as exc:
        # Safe, observable failure. Workflow continue-on-error owns fail-open;
        # callers can still detect and test a failed export via the exit code.
        print(f"::warning::Langfuse {args.command} unavailable ({type(exc).__name__})")
        if args.command == "evidence":
            write_json(args.output, {"schema_version": 1, "status": "unavailable", "runs": []})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
