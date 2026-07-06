#!/usr/bin/env python3
"""Build/verify docs/backend-matrix.md from the backend routing SSOT.

`data/agent-backends.json` is the SINGLE SOURCE OF TRUTH for which backend
every lane runs. Consumption is two-mode:

- harness=agent-run and harness=dispatch-default lanes are resolved AT
  RUNTIME on the runner (scripts/resolve_backend_lane.py), so editing the
  file re-routes them with no workflow change;
- harness=pi and harness=claude-code-action lanes are CI-ENFORCED MIRRORS:
  the model/provider stays literal in the workflow step and this script
  fails when workflow and file disagree.

This script therefore does two jobs:
1. CROSS-CHECK the file against `.github/workflows/*` (lane exists, every
   agent-run call site passes lane + all provider secrets, mirrors match,
   no orphan lanes, backends resolve in the profile table);
2. GENERATE the per-lane table in docs/backend-matrix.md AND the mermaid
   routing diagram in README.md, each between markers.

Usage:
    uv run python scripts/build_backend_matrix.py            # regenerate doc
    uv run python scripts/build_backend_matrix.py --check    # verify, exit 1 if stale/inconsistent
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
AGENT_RUN_ACTION = REPO_ROOT / ".github" / "actions" / "agent-run" / "action.yml"
LANES_FILE = REPO_ROOT / "data" / "agent-backends.json"
DOC_PATH = REPO_ROOT / "docs" / "backend-matrix.md"
README_PATH = REPO_ROOT / "README.md"

BEGIN_MARKER = "<!-- BEGIN GENERATED BACKEND MATRIX (scripts/build_backend_matrix.py — do not edit by hand) -->"
END_MARKER = "<!-- END GENERATED BACKEND MATRIX -->"
BEGIN_DIAGRAM = "<!-- BEGIN GENERATED BACKEND DIAGRAM (scripts/build_backend_matrix.py — do not edit by hand) -->"
END_DIAGRAM = "<!-- END GENERATED BACKEND DIAGRAM -->"

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
RESOLVER_CALL_RE = re.compile(r"resolve_backend_lane\.py\s+([a-z0-9\-]+)")

# Backends generative-research.yml can actually execute (its params step
# validates against this same set at runtime).
GEN_RESEARCH_BACKENDS = {"claude", "codex", "deepseek-v4-flash", "glm-5p2"}

REQUIRED_AGENT_RUN_SECRETS = {
    "claude-code-oauth-token": "CLAUDE_CODE_OAUTH_TOKEN",
    "fireworks-api-key": "FIREWORKS_API_KEY",
    "zai-api-key": "ZAI_API_KEY",
}


@dataclass
class Profile:
    normalized: str
    provider: str
    model_id: str
    display_name: str
    selectors: list[str] = field(default_factory=list)


@dataclass
class AgentRunStep:
    workflow: str
    lane: str
    raw_backend: str
    step_name: str
    tier: str
    secrets: dict[str, str]
    fireworks_fallback: str
    native_model_override: str
    is_retry: bool


@dataclass
class PiStep:
    workflow: str
    tier: str
    provider: str
    model: str
    step_name: str


@dataclass
class NativeStep:
    workflow: str
    step_name: str
    rerouted_provider: str  # "" when native
    model: str
    env_pin: str
    lane_hint: str
    is_retry: bool


@dataclass
class Observation:
    agent_run: list[AgentRunStep] = field(default_factory=list)
    pi: list[PiStep] = field(default_factory=list)
    native: list[NativeStep] = field(default_factory=list)
    codex: bool = False
    codex_token: str = ""
    resolver_lanes: set[str] = field(default_factory=set)
    det_by_tier: dict[str, str] = field(default_factory=dict)
    det_job_wide: list[str] = field(default_factory=list)
    has_dispatch_fireworks_fallback: bool = False


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


def load_lanes() -> tuple[dict[str, dict], dict]:
    try:
        data = json.loads(LANES_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {LANES_FILE}: {exc}")
    lanes = data.get("lanes")
    if not isinstance(lanes, dict) or not lanes:
        fail(f"{LANES_FILE} has no 'lanes' mapping")
    fallback = data.get("fallback")
    if not isinstance(fallback, dict):
        fail(f"{LANES_FILE} must define a global 'fallback' object "
             "(harness/chain/native_model)")
    return lanes, fallback


def load_profiles() -> dict[str, Profile]:
    """The backend profile table lives in the SSOT file itself (selector →
    provider/model/display + aliases); selectors and aliases all resolve to
    the same Profile, mirroring scripts/select_backend.py's normalization."""
    try:
        data = json.loads(LANES_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {LANES_FILE}: {exc}")
    backends = data.get("backends")
    if not isinstance(backends, dict) or len(backends) < 3:
        fail(f"{LANES_FILE} must define the 'backends' profile table")
    profiles: dict[str, Profile] = {}
    for key, spec in backends.items():
        profile = Profile(
            normalized=key,
            provider=str(spec.get("provider", "")),
            model_id=str(spec.get("model", "")),
            display_name=str(spec.get("display_name", key)),
            selectors=[key, *(spec.get("aliases") or [])],
        )
        for selector in profile.selectors:
            if selector in profiles:
                fail(f"backends table: selector '{selector}' defined twice")
            profiles[selector] = profile
    return profiles


def check_fallback(fallback: dict, profiles: dict[str, Profile]) -> list[str]:
    """The global fallback chain is routing too — validate it like a lane."""
    errors: list[str] = []
    for key in ("harness", "native_model"):
        if not isinstance(fallback.get(key), str) or not fallback[key]:
            errors.append(f"fallback.{key} must be a non-empty string")
    chain = fallback.get("chain")
    if not isinstance(chain, list) or not chain:
        errors.append("fallback.chain must be a non-empty ordered list of backend selectors")
        return errors
    if errors:
        return errors
    if fallback["harness"] != "agent-run":
        errors.append(f"fallback.harness '{fallback['harness']}' unsupported — "
                      "the fallback runs inside agent-run")
    seen: set[str] = set()
    for entry in chain:
        profile = profiles.get(str(entry))
        if profile is None:
            errors.append(f"fallback.chain entry '{entry}' is not in the backends table")
            continue
        if profile.normalized in seen:
            errors.append(f"fallback.chain entry '{entry}' duplicates an earlier candidate")
        seen.add(profile.normalized)
    return errors


def agent_run_fallback_default(action: dict) -> str:
    return action.get("inputs", {}).get("fireworks-fallback", {}).get("default", "claude")


def slugify(name: str, limit: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if len(slug) > limit:
        slug = slug[:limit].rsplit("-", 1)[0]
    return slug or "step"


def first_secret(value: object) -> str:
    m = SECRET_RE.search(str(value or ""))
    return m.group(1) if m else ""


def native_model_from_args(with_block: dict) -> str:
    m = MODEL_ARG_RE.search(str(with_block.get("claude_args", "")))
    return m.group(1) if m else "(action default)"


def observe_workflow(wf_path: Path) -> Observation:
    wf = load_yaml(wf_path)
    obs = Observation()
    on_block = wf.get("on") or wf.get(True) or {}
    dispatch_inputs = ((on_block.get("workflow_dispatch") or {}).get("inputs") or {})
    obs.has_dispatch_fireworks_fallback = "fireworks_fallback" in dispatch_inputs

    for job in (wf.get("jobs") or {}).values():
        for step in job.get("steps", []) or []:
            uses = str(step.get("uses", ""))
            with_block = step.get("with") or {}
            env = step.get("env") or {}
            run = str(step.get("run", ""))
            cond = str(step.get("if", ""))
            step_name = str(step.get("name", ""))
            tier_m = TIER_IF_RE.search(cond)
            tier = tier_m.group(1) if tier_m else ""
            is_retry = bool(re.search(r"retry", step_name, re.IGNORECASE))

            if run:
                obs.resolver_lanes.update(RESOLVER_CALL_RE.findall(run))
                scripts = sorted(set(DETERMINISTIC_RE.findall(run)))
                for script in scripts:
                    if tier:
                        obs.det_by_tier.setdefault(tier, script)
                    elif script not in obs.det_job_wide:
                        obs.det_job_wide.append(script)

            if uses.startswith("./.github/actions/agent-run"):
                secrets = {k: first_secret(with_block.get(k)) for k in REQUIRED_AGENT_RUN_SECRETS}
                obs.agent_run.append(AgentRunStep(
                    workflow=wf_path.name,
                    lane=str(with_block.get("lane", "")).strip(),
                    raw_backend=str(with_block.get("backend", "")).strip(),
                    step_name=step_name,
                    tier=tier,
                    secrets=secrets,
                    fireworks_fallback=str(with_block.get("fireworks-fallback", "")).strip(),
                    native_model_override=str(with_block.get("native-model", "")).strip(),
                    is_retry=is_retry,
                ))

            elif uses.startswith("./.github/actions/run-pi-container"):
                obs.pi.append(PiStep(
                    workflow=wf_path.name,
                    tier=tier,
                    provider=str(with_block.get("provider", "")),
                    model=str(with_block.get("model", "")),
                    step_name=step_name,
                ))

            elif uses.startswith("anthropics/claude-code-action"):
                base_url = str(env.get("ANTHROPIC_BASE_URL", ""))
                rerouted = ""
                if "fireworks" in base_url:
                    rerouted = "fireworks"
                elif "z.ai" in base_url:
                    rerouted = "zai"
                arg_model = native_model_from_args(with_block)
                env_pin = ""
                if arg_model in {"opus", "sonnet", "haiku"}:
                    pin = str(env.get(f"ANTHROPIC_DEFAULT_{arg_model.upper()}_MODEL")
                              or env.get("ANTHROPIC_MODEL") or "")
                    if pin and "${{" not in pin:
                        env_pin = pin
                eff = EFFECTIVE_IF_RE.search(cond)
                lane_hint = eff.group(1) if eff else ("fireworks" if "fireworks_active" in cond else "")
                obs.native.append(NativeStep(
                    workflow=wf_path.name,
                    step_name=step_name,
                    rerouted_provider=rerouted,
                    model=str(env.get("ANTHROPIC_MODEL", "")) if rerouted else (env_pin or arg_model),
                    env_pin=env_pin,
                    lane_hint=lane_hint,
                    is_retry=is_retry,
                ))

            elif run and CODEX_EXEC_RE.search(run):
                obs.codex = True
                wf_text = wf_path.read_text(encoding="utf-8")
                obs.codex_token = "CODEX_AUTH_JSON" if "CODEX_AUTH_JSON" in wf_text else "(unknown)"

    return obs


def cross_check(lanes: dict[str, dict], observations: dict[str, Observation],
                profiles: dict[str, Profile]) -> list[str]:
    errors: list[str] = []
    seen_lanes: set[str] = set()

    for wf_name, obs in observations.items():
        for step in obs.agent_run:
            label = f"{wf_name} step '{step.step_name}'"
            if step.raw_backend:
                errors.append(f"{label}: passes explicit backend '{step.raw_backend}' — "
                              "workflows must route via lane: (data/agent-backends.json)")
            if not step.lane:
                errors.append(f"{label}: agent-run call has no lane: input")
                continue
            seen_lanes.add(step.lane)
            lane = lanes.get(step.lane)
            if lane is None:
                errors.append(f"{label}: lane '{step.lane}' is not defined in data/agent-backends.json")
                continue
            if lane.get("harness") != "agent-run":
                errors.append(f"{label}: lane '{step.lane}' has harness "
                              f"'{lane.get('harness')}', expected agent-run")
            if lane.get("workflow") != wf_name:
                errors.append(f"{label}: lane '{step.lane}' belongs to workflow "
                              f"'{lane.get('workflow')}', not {wf_name}")
            backend = str(lane.get("backend", ""))
            if backend not in profiles:
                errors.append(f"lane '{step.lane}': backend '{backend}' is not in the "
                              "backends table in data/agent-backends.json")
            elif lane.get("pinned"):
                # A pin is only real if it's machine-checked: the lane must
                # declare which provider it is pinned to, and the backend
                # must keep resolving to that provider.
                pinned_provider = lane.get("pinned_provider")
                if not pinned_provider:
                    errors.append(f"lane '{step.lane}': pinned lanes must declare "
                                  "pinned_provider so the pin is enforceable")
                elif profiles[backend].provider != pinned_provider:
                    errors.append(f"lane '{step.lane}' is PINNED to provider "
                                  f"'{pinned_provider}' but backend '{backend}' resolves to "
                                  f"'{profiles[backend].provider}' — re-routing a pinned lane "
                                  "requires deliberately updating pinned_provider too")
            lane_tier = str(lane.get("tier", ""))
            if lane_tier and lane_tier != step.tier:
                errors.append(f"{label}: lane '{step.lane}' declares tier '{lane_tier}' but "
                              f"the step is gated on tier '{step.tier or '(none)'}' — the SSOT "
                              "must not lie about tier placement")
            if "strict" in lane and not isinstance(lane.get("strict"), bool):
                errors.append(f"lane '{step.lane}': strict must be a boolean")
            for input_name, expected in REQUIRED_AGENT_RUN_SECRETS.items():
                if step.secrets.get(input_name) != expected:
                    errors.append(f"{label}: must pass {input_name}: secrets.{expected} — "
                                  "every agent-run call site carries all provider keys so a "
                                  "data/agent-backends.json flip re-routes without workflow edits")

        for step in obs.pi:
            match = [
                (key, lane) for key, lane in lanes.items()
                if lane.get("harness") == "pi" and lane.get("workflow") == wf_name
                and (not lane.get("tier") or lane.get("tier") == step.tier)
            ]
            if not match:
                errors.append(f"{wf_name} pi step '{step.step_name}' (tier '{step.tier}') "
                              "has no pi lane in data/agent-backends.json")
                continue
            key, lane = match[0]
            seen_lanes.add(key)
            if lane.get("model") != step.model or lane.get("provider") != step.provider:
                errors.append(f"{wf_name} pi step '{step.step_name}': workflow pins "
                              f"{step.provider}/{step.model} but lane '{key}' says "
                              f"{lane.get('provider')}/{lane.get('model')} — update one (mirror contract)")

        for step in obs.native:
            if step.rerouted_provider:
                # generative-research's env-rerouted Fireworks path is a known
                # execution path of its dispatch-default lane. Anywhere else,
                # an env-rerouted direct claude-code-action step would be a
                # token-spending model lane invisible to the SSOT — ban it.
                if wf_name != "generative-research.yml":
                    errors.append(f"{wf_name} step '{step.step_name}': direct "
                                  f"claude-code-action step reroutes to '{step.rerouted_provider}' "
                                  "via ANTHROPIC_BASE_URL outside generative-research.yml — "
                                  "route provider traffic through agent-run lanes instead")
                continue
            candidates = [
                (key, lane) for key, lane in lanes.items()
                if lane.get("harness") == "claude-code-action" and lane.get("workflow") == wf_name
            ]
            if not candidates:
                errors.append(f"{wf_name} native step '{step.step_name}' has no "
                              "claude-code-action lane in data/agent-backends.json")
                continue
            key, lane = candidates[0]
            seen_lanes.add(key)
            if lane.get("model") != step.model:
                errors.append(f"{wf_name} native step '{step.step_name}': serves model "
                              f"'{step.model}' but lane '{key}' says '{lane.get('model')}' "
                              "— update one (mirror contract)")

    for key, lane in lanes.items():
        harness = lane.get("harness")
        wf_name = str(lane.get("workflow", ""))
        if not (WORKFLOWS_DIR / wf_name).exists():
            errors.append(f"lane '{key}': workflow '{wf_name}' does not exist")
            continue
        if harness == "dispatch-default":
            obs = observations.get(wf_name)
            if obs is None or key not in obs.resolver_lanes:
                errors.append(f"lane '{key}': {wf_name} never calls "
                              f"resolve_backend_lane.py {key} — the default is not SSOT-routed")
            else:
                seen_lanes.add(key)
            backend = str(lane.get("backend", ""))
            if wf_name == "generative-research.yml" and backend not in GEN_RESEARCH_BACKENDS:
                errors.append(f"lane '{key}': backend '{backend}' is not supported by "
                              f"generative-research.yml (allowed: {sorted(GEN_RESEARCH_BACKENDS)})")
        elif key not in seen_lanes:
            errors.append(f"lane '{key}' ({wf_name}) is defined in data/agent-backends.json "
                          "but no workflow step references it — orphan lanes hide dead routing")

    # One agent-run call site per lane: duplicates would make "which step is
    # this lane" ambiguous in the table and in freshness debugging.
    counts: dict[str, int] = {}
    for obs in observations.values():
        for step in obs.agent_run:
            if step.lane:
                counts[step.lane] = counts.get(step.lane, 0) + 1
    for lane_key, n in sorted(counts.items()):
        if n > 1:
            errors.append(f"lane '{lane_key}' is referenced by {n} agent-run steps — "
                          "one lane per call site; add a distinct lane per step")

    return errors


def build_rows(lanes: dict[str, dict], observations: dict[str, Observation],
               profiles: dict[str, Profile], native_fallback: str,
               fallback_default: str, chain: list[str]) -> list[list[str]]:
    rows: list[list[str]] = []

    def det_suffix(obs: Observation, tier: str) -> str:
        script = obs.det_by_tier.get(tier) if tier else None
        if script is None and obs.det_job_wide:
            script = obs.det_job_wide[0]
        return f"; then `{script}`" if script else ""

    def render_chain(requested: str) -> str:
        parts = []
        for entry in chain:
            profile = profiles.get(str(entry))
            if profile is None or profile.normalized == requested:
                continue  # select_backend skips the already-failed requested backend
            if profile.provider == "claude":
                parts.append(f"claude (`{native_fallback}`)")
            else:
                parts.append(f"`{profile.normalized}`")
        return "chain: " + " → ".join(parts) if parts else "hard fail (chain exhausted)"

    TOKEN_BY_PROVIDER = {"fireworks": "FIREWORKS_API_KEY", "zai": "ZAI_API_KEY",
                         "claude": "CLAUDE_CODE_OAUTH_TOKEN"}

    for key in sorted(lanes):
        lane = lanes[key]
        wf_name = str(lane.get("workflow", ""))
        obs = observations.get(wf_name, Observation())
        harness = lane.get("harness")
        pinned = " · PINNED" if lane.get("pinned") else ""

        if harness == "agent-run":
            step = next((s for s in obs.agent_run if s.lane == key), None)
            backend = str(lane.get("backend", ""))
            profile = profiles.get(backend)
            provider = profile.display_name if profile else backend
            model = f"`{profile.model_id}`" if profile and profile.model_id else f"`{native_fallback}`"
            token = TOKEN_BY_PROVIDER.get(profile.provider if profile else "", "?")
            setting = (step.fireworks_fallback if step and step.fireworks_fallback
                       else fallback_default)
            if lane.get("strict"):
                fallback = "hard fail (strict — never walks the chain)"
            elif setting == "none":
                fallback = "hard fail (`fireworks-fallback: none`)"
            else:
                fallback = render_chain(profile.normalized if profile else backend)
            tier = step.tier if step else ""
            fallback += det_suffix(obs, tier)
            lane_label = key + (f" (tier:{tier})" if tier else "") + pinned
            rows.append([lane_label, f"`{wf_name}`", "Claude Code · agent-run (runtime SSOT)",
                         provider, model, f"`{token}`", fallback])

        elif harness == "pi":
            rows.append([key + (f" (tier:{lane.get('tier')})" if lane.get("tier") else ""),
                         f"`{wf_name}`", "pi · run-pi-container (CI-enforced mirror)",
                         f"{lane.get('provider', '?')} (pi built-in)",
                         f"`{lane.get('model', '?')}`", "`FIREWORKS_API_KEY`", "—"])

        elif harness == "claude-code-action":
            native_steps = [s for s in obs.native if not s.rerouted_provider]
            variants = len([s for s in native_steps if not s.is_retry])
            retries = len([s for s in native_steps if s.is_retry])
            suffix = ""
            if variants > 1:
                suffix += f" (×{variants} step variants)"
            if retries:
                suffix += f" (+{retries} retry step{'s' if retries > 1 else ''})"
            rows.append([key + suffix, f"`{wf_name}`",
                         "Claude Code · claude-code-action (CI-enforced mirror)",
                         "Anthropic (native)", f"`{lane.get('model', '?')}`",
                         "`CLAUDE_CODE_OAUTH_TOKEN`", "—"])

        elif harness == "dispatch-default":
            fallback = "—"
            if obs.has_dispatch_fireworks_fallback:
                fallback = "workflow-level `fireworks_fallback` input (default `claude`)"
            rows.append([key, f"`{wf_name}`", "dispatch default (runtime SSOT)",
                         "(per chosen backend)", f"default: `{lane.get('backend', '?')}`",
                         "(per chosen backend)", fallback])
        else:
            fail(f"lane '{key}': unknown harness '{harness}'")

    # Dispatch-path rows observed in generative-research (fireworks dynamic +
    # codex) — real execution paths of the dispatch-default lane, shown for
    # completeness but not themselves routing decisions.
    for wf_name, obs in sorted(observations.items()):
        fw_steps = [s for s in obs.native if s.rerouted_provider == "fireworks"]
        if fw_steps:
            retries = len([s for s in fw_steps if s.is_retry])
            suffix = f" (+{retries} retry step{'s' if retries > 1 else ''})" if retries else ""
            rows.append([f"(dispatch path) backend=fireworks{suffix}", f"`{wf_name}`",
                         "Claude Code · claude-code-action (env-rerouted)",
                         "Fireworks (Anthropic-compatible endpoint)",
                         "dynamic: per fireworks profile step", "`FIREWORKS_API_KEY`",
                         "workflow-level `fireworks_fallback` input (default `claude`)"
                         if obs.has_dispatch_fireworks_fallback else "—"])
        if obs.codex:
            rows.append(["(dispatch path) backend=codex", f"`{wf_name}`", "Codex CLI",
                         "OpenAI (ChatGPT subscription auth)", "codex CLI default",
                         f"`{obs.codex_token}`", "—"])

    return rows


PROVIDER_NODES = {
    "fireworks": ("FW", "🎆 Fireworks"),
    "zai": ("ZAI", "⚡ Z.ai"),
    "claude": ("ANT", "🅰️ Anthropic<br/><i>native Claude</i>"),
}


def _wrap(items: list[str], per_line: int = 3) -> str:
    lines = [" · ".join(items[i:i + per_line]) for i in range(0, len(items), per_line)]
    return "<br/>".join(lines)


def build_readme_diagram(lanes: dict[str, dict], profiles: dict[str, Profile],
                         chain: list[str], native_fallback: str,
                         has_codex: bool) -> str:
    """Mermaid routing diagram for the README, derived from the SSOT. Lanes
    are grouped per backend (strict lanes separately) so a re-route in the
    JSON changes the picture on the next regeneration."""
    by_backend: dict[str, list[str]] = {}
    strict_by_backend: dict[str, list[str]] = {}
    native_lanes: list[str] = []
    native_models: set[str] = set()
    pi_lanes: list[str] = []
    pi_models: list[str] = []
    gen_default: tuple[str, str] | None = None
    for key in sorted(lanes):
        lane = lanes[key]
        harness = lane.get("harness")
        if harness == "agent-run":
            backend = profiles[str(lane["backend"])].normalized
            target = strict_by_backend if lane.get("strict") else by_backend
            target.setdefault(backend, []).append(key)
        elif harness == "claude-code-action":
            native_lanes.append(key)
            native_models.add(str(lane.get("model", "")))
        elif harness == "pi":
            pi_lanes.append(key)
            pi_models.append(str(lane.get("model", "")).split("/")[-1])
        elif harness == "dispatch-default":
            gen_default = (key, profiles[str(lane["backend"])].normalized)

    out = ["flowchart LR"]
    out.append('    subgraph runtime["⚙️ Runtime-routed lanes — lane: → data/agent-backends.json"]')
    edges: list[tuple[str, str]] = []
    for i, backend in enumerate(sorted(by_backend)):
        keys = by_backend[backend]
        node = f"lanes{i}"
        out.append(f'        {node}["{_wrap(keys)}<br/><i>{len(keys)} lane{"s" if len(keys) > 1 else ""}</i>"]')
        edges.append((node, backend))
    for i, backend in enumerate(sorted(strict_by_backend)):
        keys = strict_by_backend[backend]
        node = f"strict{i}"
        out.append(f'        {node}["🔒 {_wrap(keys)}<br/><i>strict — never falls back</i>"]')
        edges.append((node, backend))
    if gen_default:
        out.append(f'        gendef["{gen_default[0]}<br/><i>dispatch default</i>"]')
        edges.append(("gendef", gen_default[1]))
    out.append("    end")

    out.append('    subgraph mirrors["🪞 CI-enforced mirrors — literal in workflow, equality-gated"]')
    out.append(f'        pi["{_wrap(pi_lanes)}"]')
    out.append(f'        native["{_wrap(native_lanes)}"]')
    out.append("    end")

    out.append('    subgraph providers["🏭 Token providers"]')
    for node, label in PROVIDER_NODES.values():
        out.append(f'        {node}["{label}"]')
    if has_codex:
        out.append('        OAI["🤖 OpenAI Codex CLI<br/><i>ChatGPT auth</i>"]')
    out.append("    end")

    for node, backend in edges:
        profile = profiles[backend]
        short = profile.model_id.split("/")[-1] or native_fallback
        out.append(f'    {node} -->|"{short}"| {PROVIDER_NODES[profile.provider][0]}')
    out.append(f'    pi -->|"{" · ".join(sorted(set(pi_models)))}"| FW')
    out.append(f'    native -->|"{" · ".join(sorted(m for m in native_models if m))}"| ANT')
    if gen_default and has_codex:
        out.append('    gendef -.->|"backend=codex"| OAI')

    # ordered chain arrows between providers: primary-heaviest provider first,
    # then each chain hop
    primary_counts: dict[str, int] = {}
    for backend, keys in by_backend.items():
        prov = profiles[backend].provider
        primary_counts[prov] = primary_counts.get(prov, 0) + len(keys)
    hops: list[str] = []
    top_primary = max(primary_counts, key=lambda k: primary_counts[k]) if primary_counts else None
    if top_primary:
        hops.append(PROVIDER_NODES[top_primary][0])
    for entry in chain:
        node = PROVIDER_NODES[profiles[str(entry)].provider][0]
        if node not in hops:
            hops.append(node)
    for i in range(len(hops) - 1):
        out.append(f'    {hops[i]} -. "provider outage → fallback #{i + 1}" .-> {hops[i + 1]}')
    return "\n".join(out)


def build_generated_blocks() -> tuple[str, str]:
    lanes, fallback = load_lanes()
    profiles = load_profiles()
    action_text = AGENT_RUN_ACTION.read_text(encoding="utf-8")
    if "select_backend.py" not in action_text:
        fail("agent-run action.yml no longer calls scripts/select_backend.py — "
             "the runtime selector and this validator must stay coupled")
    fallback_default = agent_run_fallback_default(load_yaml(AGENT_RUN_ACTION))
    native_fallback = str(fallback.get("native_model", ""))
    chain = [str(c) for c in (fallback.get("chain") or [])]

    observations = {p.name: observe_workflow(p) for p in workflow_files()}

    errors = check_fallback(fallback, profiles) + cross_check(lanes, observations, profiles)
    if errors:
        for err in errors:
            print(f"CROSS-CHECK: {err}", file=sys.stderr)
        fail(f"{len(errors)} SSOT consistency error(s) between data/agent-backends.json "
             "and .github/workflows/ — fix the routing before regenerating the matrix")

    rows = build_rows(lanes, observations, profiles, native_fallback, fallback_default, chain)

    lane_workflows = {str(l.get("workflow")) for l in lanes.values()}
    no_model = [p.name for p in workflow_files()
                if p.name not in lane_workflows
                and not any([observations[p.name].agent_run, observations[p.name].pi,
                             observations[p.name].native, observations[p.name].codex])]

    lines = [BEGIN_MARKER, ""]
    lines.append("### Lanes")
    lines.append("")
    lines.append("| Lane | Workflow | Harness | Provider | Model | Token secret | Fallback |")
    lines.append("|---|---|---|---|---|---|---|")
    for row in rows:
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in row) + " |")
    lines.append("")
    lines.append("### Workflows with no model lane (deterministic / infra)")
    lines.append("")
    for name in no_model:
        lines.append(f"- `{name}`")
    lines.append("")
    chain_text = " → ".join(f"`{c}`" for c in chain)
    lines.append(f"_Global ordered fallback chain (SSOT `fallback.chain`): {chain_text}; "
                 f"native path serves `{native_fallback}`. {len(lanes)} SSOT lanes "
                 f"(+{len(rows) - len(lanes)} dispatch execution paths) across "
                 f"{len(workflow_files())} workflows; {len(no_model)} workflows run no model._")
    lines.append("")
    lines.append(END_MARKER)

    has_codex = any(o.codex for o in observations.values())
    diagram = build_readme_diagram(lanes, profiles, chain, native_fallback, has_codex)
    diagram_block = "\n".join([
        BEGIN_DIAGRAM,
        "```mermaid",
        diagram,
        "```",
        f"_Generated from [`data/agent-backends.json`](data/agent-backends.json) — "
        f"fallback chain: {' → '.join(f'`{c}`' for c in chain)}; regenerate with "
        f"`uv run python scripts/build_backend_matrix.py`._",
        END_DIAGRAM,
    ])
    return "\n".join(lines), diagram_block


def splice(text: str, block: str, begin_marker: str, end_marker: str, where: Path) -> str:
    begin = text.find(begin_marker)
    end = text.find(end_marker)
    if begin == -1 or end == -1 or end < begin:
        fail(f"{where}: generated-block markers missing or malformed")
    return text[:begin] + block + text[end + len(end_marker):]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="verify SSOT consistency + doc freshness; exit 1 on failure")
    args = parser.parse_args()

    for path in (DOC_PATH, README_PATH):
        if not path.exists():
            fail(f"{path} does not exist — create it with the generated-block markers first")

    doc_block, diagram_block = build_generated_blocks()
    targets = [
        (DOC_PATH, doc_block, BEGIN_MARKER, END_MARKER),
        (README_PATH, diagram_block, BEGIN_DIAGRAM, END_DIAGRAM),
    ]

    stale = []
    for path, block, begin, end in targets:
        text = path.read_text(encoding="utf-8")
        updated = splice(text, block, begin, end, path)
        if updated != text:
            stale.append((path, updated))

    if args.check:
        if stale:
            names = ", ".join(str(p.relative_to(REPO_ROOT)) for p, _ in stale)
            print(
                f"{names} STALE relative to data/agent-backends.json + .github/workflows/ — "
                "regenerate with: uv run python scripts/build_backend_matrix.py",
                file=sys.stderr,
            )
            return 1
        print("Backend SSOT is consistent; docs/backend-matrix.md and the README diagram are in sync.")
        return 0

    for path, updated in stale:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(updated, encoding="utf-8")
        tmp.replace(path)
        print(f"Updated {path.relative_to(REPO_ROOT)}")
    if not stale:
        print("docs/backend-matrix.md and README diagram already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
