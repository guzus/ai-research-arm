#!/usr/bin/env python3
"""Build/verify docs/backend-matrix.md — the per-workflow agent harness &
token-provider matrix.

The matrix answers, for every GitHub Actions workflow: which agent harness
runs (claude-code-action direct, the agent-run wrapper, run-pi-container,
or the Codex CLI), which provider serves the tokens (Anthropic, Fireworks,
Z.ai, ChatGPT/Codex), under which model id, authenticated by which GitHub
secret, and what the fallback chain is.

It is DERIVED, never hand-maintained: rows are parsed out of
`.github/workflows/*.yml` plus the backend profile table inside
`.github/actions/agent-run/action.yml`. This mirrors the
`build_wiki_index.py --check` pattern — the doc carries a generated block
between markers, CI fails when the block is stale.

Usage:
    uv run python scripts/build_backend_matrix.py            # regenerate doc
    uv run python scripts/build_backend_matrix.py --check    # verify, exit 1 if stale
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
AGENT_RUN_ACTION = REPO_ROOT / ".github" / "actions" / "agent-run" / "action.yml"
DOC_PATH = REPO_ROOT / "docs" / "backend-matrix.md"

BEGIN_MARKER = "<!-- BEGIN GENERATED BACKEND MATRIX (scripts/build_backend_matrix.py — do not edit by hand) -->"
END_MARKER = "<!-- END GENERATED BACKEND MATRIX -->"

SECRET_RE = re.compile(r"secrets\.([A-Z0-9_]+)")
# Both tier regexes take only the FIRST tier of a compound `||` condition; a
# step gated on two tiers would be attributed to one (none exist today).
TIER_IF_RE = re.compile(r"steps\.backend\.outputs\.name\s*==\s*'([a-z0-9\-]+)'")
EFFECTIVE_IF_RE = re.compile(r"steps\.effective\.outputs\.backend\s*==\s*'([a-z0-9\-]+)'")
MODEL_ARG_RE = re.compile(r"--model\s+([^\s\"']+)")
DETERMINISTIC_RE = re.compile(r"(deterministic_[a-z_]+\.py)")
# Loose on purpose (any run block with "codex" then "exec"); a shell `exec`
# in an unrelated codex-mentioning step would create a phantom lane — if that
# ever happens, tighten to the actual `codex ... exec` invocation shape.
CODEX_EXEC_RE = re.compile(r"\bcodex\b[^\n]*(?:\n[^\n]*)*?\bexec\b")


@dataclass
class Row:
    workflow: str
    order: int
    lane: str
    harness: str
    provider: str
    model: str
    token: str
    fallback: str
    step_name: str = ""
    retry_count: int = 0

    def config_key(self) -> tuple:
        return (self.workflow, self.harness, self.provider, self.model, self.token, self.fallback)


@dataclass
class Profile:
    normalized: str
    provider: str
    model_id: str
    display_name: str
    selectors: list[str] = field(default_factory=list)


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def workflow_files() -> list[Path]:
    # GitHub accepts both extensions; globbing only *.yml would let a future
    # *.yaml workflow's lanes silently vanish from the matrix with --check green.
    return sorted(list(WORKFLOWS_DIR.glob("*.yml")) + list(WORKFLOWS_DIR.glob("*.yaml")))


def load_yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # boundary: malformed workflow file
        fail(f"cannot parse {path}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path} did not parse to a mapping")
    return data


def parse_agent_run_profiles(action: dict) -> dict[str, Profile]:
    """Extract the backend case-block from agent-run's `Resolve agent backend`
    step into selector → Profile. Fails loudly if the block shape changes so
    the matrix can never silently misreport a profile."""
    steps = action.get("runs", {}).get("steps", [])
    resolve = next((s for s in steps if s.get("id") == "profile"), None)
    if resolve is None or "run" not in resolve:
        fail("agent-run action.yml: could not find the id=profile resolve step")

    profiles: dict[str, Profile] = {}
    selectors: list[str] = []
    fields: dict[str, str] = {}
    for raw_line in resolve["run"].splitlines():
        line = raw_line.strip()
        m = re.fullmatch(r"([a-z0-9|.\-]+)\)", line)
        if m and m.group(1) != "*":
            selectors = m.group(1).split("|")
            fields = {}
            continue
        m = re.fullmatch(r'(normalized|provider|model_id|display_name)="([^"]*)"', line)
        if m and selectors:
            fields[m.group(1)] = m.group(2)
            continue
        if line == ";;" and selectors:
            if "normalized" in fields:
                profile = Profile(
                    normalized=fields["normalized"],
                    provider=fields.get("provider", "?"),
                    model_id=fields.get("model_id", ""),
                    display_name=fields.get("display_name", fields["normalized"]),
                    selectors=selectors,
                )
                for sel in selectors:
                    profiles[sel] = profile
            selectors = []
            fields = {}
    if len({p.normalized for p in profiles.values()}) < 3:
        fail("agent-run action.yml: parsed fewer than 3 backend profiles — case block shape changed?")
    return profiles


def agent_run_defaults(action: dict) -> dict[str, str]:
    inputs = action.get("inputs", {})
    return {
        "backend": inputs.get("backend", {}).get("default", ""),
        "native-model": inputs.get("native-model", {}).get("default", ""),
        "fireworks-fallback": inputs.get("fireworks-fallback", {}).get("default", ""),
    }


def slugify(name: str, limit: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if len(slug) > limit:
        slug = slug[:limit].rsplit("-", 1)[0]
    return slug or "step"


def first_secret(value: object) -> str:
    m = SECRET_RE.search(str(value or ""))
    return m.group(1) if m else ""


def lane_for(step: dict) -> str:
    cond = str(step.get("if", ""))
    m = TIER_IF_RE.search(cond)
    if m:
        return f"tier:{m.group(1)}"
    m = EFFECTIVE_IF_RE.search(cond)
    if m:
        return f"backend={m.group(1)}"
    if "fireworks_active" in cond:
        return "backend=fireworks (deepseek-v4-flash / glm-5p2)"
    return slugify(str(step.get("name", "step")))


def native_model_from_args(with_block: dict) -> str:
    m = MODEL_ARG_RE.search(str(with_block.get("claude_args", "")))
    return m.group(1) if m else "(action default)"


def collect_deterministic_fallbacks(job: dict) -> tuple[dict[str, str], list[str]]:
    """Map tier → deterministic fallback script for steps gated on a tier,
    plus job-wide scripts for ungated fallback steps."""
    by_tier: dict[str, str] = {}
    job_wide: list[str] = []
    for step in job.get("steps", []) or []:
        run = str(step.get("run", ""))
        scripts = sorted(set(DETERMINISTIC_RE.findall(run)))
        if not scripts:
            continue
        tier = TIER_IF_RE.search(str(step.get("if", "")))
        for script in scripts:
            if tier:
                by_tier.setdefault(tier.group(1), script)
            elif script not in job_wide:
                job_wide.append(script)
    return by_tier, job_wide


def rows_for_workflow(
    wf_path: Path, profiles: dict[str, Profile], defaults: dict[str, str]
) -> list[Row]:
    wf = load_yaml(wf_path)
    rows: list[Row] = []
    order = 0
    for job in (wf.get("jobs") or {}).values():
        det_by_tier, det_job_wide = collect_deterministic_fallbacks(job)

        def det_suffix(lane: str) -> str:
            tier = lane.removeprefix("tier:")
            script = det_by_tier.get(tier)
            if script is None and det_job_wide:
                script = det_job_wide[0]
            return f"; then `{script}`" if script else ""

        for step in job.get("steps", []) or []:
            uses = str(step.get("uses", ""))
            with_block = step.get("with") or {}
            env = step.get("env") or {}
            lane = lane_for(step)
            row = None

            if uses.startswith("./.github/actions/agent-run"):
                backend = str(with_block.get("backend", "") or defaults["backend"]).strip()
                if "${{" in backend:
                    row = Row(wf_path.name, order, lane, "Claude Code · agent-run",
                              "resolved at runtime", f"dynamic: `{backend}`",
                              "(per resolved backend)", "(per resolved backend)")
                else:
                    profile = profiles.get(backend)
                    if profile is None:
                        fail(f"{wf_path.name}: agent-run backend '{backend}' has no profile in agent-run/action.yml")
                    fallback_setting = str(with_block.get("fireworks-fallback", "") or defaults["fireworks-fallback"]).strip()
                    native_model = str(with_block.get("native-model", "") or defaults["native-model"]).strip()
                    if profile.provider == "fireworks":
                        token = first_secret(with_block.get("fireworks-api-key")) or "(none passed!)"
                        # agent-run hard-fails on ANY non-"claude" fallback value.
                        fallback = (
                            f"native Claude (`{native_model}`)" if fallback_setting == "claude"
                            else f"hard fail (`fireworks-fallback: {fallback_setting}`)"
                        )
                        model = profile.model_id
                    elif profile.provider == "zai":
                        token = first_secret(with_block.get("zai-api-key")) or "(none passed!)"
                        fallback = "hard fail if key unset (no provider fallback)"
                        model = profile.model_id
                    else:  # native claude through the wrapper
                        token = "CLAUDE_CODE_OAUTH_TOKEN"
                        fallback = "—"
                        model = native_model
                    row = Row(wf_path.name, order, lane, "Claude Code · agent-run",
                              profile.display_name, f"`{model}`", token,
                              fallback + det_suffix(lane))

            elif uses.startswith("anthropics/claude-code-action"):
                base_url = str(env.get("ANTHROPIC_BASE_URL", ""))
                if "fireworks" in base_url:
                    provider = "Fireworks (Anthropic-compatible endpoint)"
                    model = str(env.get("ANTHROPIC_MODEL", "?"))
                    model = f"dynamic: `{model}`" if "${{" in model else f"`{model}`"
                    token = first_secret(env.get("ANTHROPIC_AUTH_TOKEN")) or "(none!)"
                elif "z.ai" in base_url:
                    provider = "Z.ai (Anthropic-compatible endpoint)"
                    model = f"`{env.get('ANTHROPIC_MODEL', '?')}`"
                    token = first_secret(env.get("ANTHROPIC_AUTH_TOKEN")) or "(none!)"
                else:
                    provider = "Anthropic (native)"
                    arg_model = native_model_from_args(with_block)
                    if arg_model in {"opus", "sonnet", "haiku"}:
                        pin = str(env.get(f"ANTHROPIC_DEFAULT_{arg_model.upper()}_MODEL")
                                  or env.get("ANTHROPIC_MODEL") or "")
                        if pin and "${{" not in pin:
                            model = f"`{arg_model}` → `{pin}` (env pin)"
                        else:
                            model = f"`{arg_model}` (claude_args alias)"
                    else:
                        model = f"`{arg_model}`"
                    token = first_secret(with_block.get("claude_code_oauth_token")) or "(none!)"
                on_block = wf.get("on") or wf.get(True) or {}
                dispatch_inputs = ((on_block.get("workflow_dispatch") or {}).get("inputs") or {})
                fallback = "—"
                if provider.startswith("Fireworks") and "fireworks_fallback" in dispatch_inputs:
                    default = dispatch_inputs["fireworks_fallback"].get("default", "?")
                    fallback = f"workflow-level `fireworks_fallback` input (default `{default}`)"
                row = Row(wf_path.name, order, lane, "Claude Code · claude-code-action (direct)",
                          provider, model, token, fallback + det_suffix(lane))

            elif uses.startswith("./.github/actions/run-pi-container"):
                row = Row(wf_path.name, order, lane, "pi · run-pi-container",
                          f"{with_block.get('provider', '?')} (pi built-in)",
                          f"`{with_block.get('model', '?')}`",
                          first_secret(with_block.get("fireworks-api-key")) or "(none!)",
                          "—" + det_suffix(lane))

            elif "run" in step and CODEX_EXEC_RE.search(str(step["run"])):
                wf_text = wf_path.read_text(encoding="utf-8")
                token = "CODEX_AUTH_JSON" if "CODEX_AUTH_JSON" in wf_text else "(unknown)"
                row = Row(wf_path.name, order, lane, "Codex CLI",
                          "OpenAI (ChatGPT subscription auth)", "codex CLI default",
                          token, "—")

            if row is not None:
                row.step_name = str(step.get("name", ""))
                rows.append(row)
                order += 1

    # Fold explicit retry steps into their config-identical base row. Steps
    # that merely share a config but do different jobs (e.g. the Twitter
    # primary processor vs. its auto-research selector) stay separate.
    folded: list[Row] = []
    for row in rows:
        if re.search(r"retry", row.step_name, re.IGNORECASE):
            base = next((r for r in folded if r.config_key() == row.config_key()
                         and not re.search(r"retry", r.step_name, re.IGNORECASE)), None)
            if base is not None:
                base.retry_count += 1
                continue
        folded.append(row)

    # Disambiguate repeated lane labels (a tier can host several model
    # steps) by appending the step slug.
    by_lane: dict[str, int] = {}
    for row in folded:
        by_lane[row.lane] = by_lane.get(row.lane, 0) + 1
    for row in folded:
        if by_lane[row.lane] > 1:
            row.lane = f"{row.lane} · {slugify(row.step_name)}"
    for row in folded:
        if row.retry_count:
            row.lane += f" (+{row.retry_count} retry step{'s' if row.retry_count > 1 else ''})"
    return folded


def build_generated_block() -> str:
    action = load_yaml(AGENT_RUN_ACTION)
    profiles = parse_agent_run_profiles(action)
    defaults = agent_run_defaults(action)

    all_rows: list[Row] = []
    no_model: list[str] = []
    for wf_path in workflow_files():
        rows = rows_for_workflow(wf_path, profiles, defaults)
        if rows:
            all_rows.extend(rows)
        else:
            no_model.append(wf_path.name)

    lines = [BEGIN_MARKER, ""]
    lines.append("### Model lanes")
    lines.append("")
    lines.append("| Workflow | Lane | Harness | Provider | Model | Token secret | Fallback |")
    lines.append("|---|---|---|---|---|---|---|")
    for row in all_rows:
        cells = [f"`{row.workflow}`", row.lane, row.harness, row.provider,
                 row.model, f"`{row.token}`", row.fallback]
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    lines.append("")
    lines.append("### Workflows with no model lane (deterministic / infra)")
    lines.append("")
    for name in no_model:
        lines.append(f"- `{name}`")
    lines.append("")
    lines.append(f"_{len(all_rows)} model lanes across {len(workflow_files())} workflows;"
                 f" {len(no_model)} workflows run no model._")
    lines.append("")
    lines.append(END_MARKER)
    return "\n".join(lines)


def splice(doc_text: str, block: str) -> str:
    begin = doc_text.find(BEGIN_MARKER)
    end = doc_text.find(END_MARKER)
    if begin == -1 or end == -1 or end < begin:
        fail(f"{DOC_PATH}: generated-block markers missing or malformed")
    return doc_text[:begin] + block + doc_text[end + len(END_MARKER):]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="verify the committed doc matches the workflows; exit 1 if stale")
    args = parser.parse_args()

    if not DOC_PATH.exists():
        fail(f"{DOC_PATH} does not exist — create it with the generated-block markers first")

    doc_text = DOC_PATH.read_text(encoding="utf-8")
    updated = splice(doc_text, build_generated_block())

    if args.check:
        if updated != doc_text:
            print(
                "docs/backend-matrix.md is STALE relative to .github/workflows/ — "
                "regenerate with: uv run python scripts/build_backend_matrix.py",
                file=sys.stderr,
            )
            return 1
        print("docs/backend-matrix.md is in sync with the workflows.")
        return 0

    if updated != doc_text:
        tmp = DOC_PATH.with_suffix(".md.tmp")
        tmp.write_text(updated, encoding="utf-8")
        tmp.replace(DOC_PATH)
        print(f"Updated {DOC_PATH.relative_to(REPO_ROOT)}")
    else:
        print(f"{DOC_PATH.relative_to(REPO_ROOT)} already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
