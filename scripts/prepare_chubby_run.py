#!/usr/bin/env python3
"""Prepare a private, credential-free Claude configuration for a Chubby step.

The bearer key is validated in memory only; the action injects it into the
child's environment. No network request, auth file, or global env write occurs.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import shlex
import tempfile
import uuid

from chubby_config import DEFAULT_BASE_URL, validate_config


MODEL_ENV = (
    "ANTHROPIC_MODEL", "ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL", "ANTHROPIC_DEFAULT_FABLE_MODEL",
    "ANTHROPIC_SMALL_FAST_MODEL", "CLAUDE_CODE_SUBAGENT_MODEL",
)


def prepare(root: Path, runner_temp: Path, api_key: str, base_url: str,
            model: str, claude_args: str) -> dict[str, str]:
    base_url = validate_config(api_key, base_url, model)
    args = shlex.split(claude_args)
    if any(arg.split("=", 1)[0] in {"--settings", "--setting-sources", "--fallback-model"}
           for arg in args):
        raise ValueError("Chubby owns settings, setting-sources, and model fallback configuration")
    # Retain project instructions/skills and the reviewed sandbox, while excluding
    # local settings and inherited user credentials. Reject project bearer injection;
    # command-line settings pin the other routing and auth fields.
    policy = copy.deepcopy(json.loads((root / ".claude/settings.json").read_text()))
    env = policy.setdefault("env", {})
    if any(name in env for name in ("ANTHROPIC_AUTH_TOKEN", "CHUBBY_API_KEY")):
        raise ValueError("Project settings must not supply Chubby bearer credentials")
    env.update({name: model for name in MODEL_ENV})
    env.update({
        "ANTHROPIC_BASE_URL": base_url,
        "ANTHROPIC_API_KEY": "", "CLAUDE_CODE_OAUTH_TOKEN": "",
        "ANTHROPIC_CUSTOM_HEADERS": "", "ANTHROPIC_FEDERATION_RULE_ID": "",
        "ANTHROPIC_ORGANIZATION_ID": "",
        "CLAUDE_CODE_USE_BEDROCK": "", "CLAUDE_CODE_USE_VERTEX": "",
        "CLAUDE_CODE_USE_FOUNDRY": "", "ENABLE_TOOL_SEARCH": "false",
        "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "DISABLE_TELEMETRY": "1",
        "CLAUDE_CODE_MAX_RETRIES": "0", "CLAUDE_CODE_RETRY_WATCHDOG": "",
        "CLAUDE_CODE_ENABLE_TELEMETRY": "0", "OTEL_METRICS_EXPORTER": "none",
        "OTEL_LOGS_EXPORTER": "none", "OTEL_TRACES_EXPORTER": "none",
        "OTEL_EXPORTER_OTLP_ENDPOINT": "", "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "4096",
        "HTTPS_PROXY": "", "HTTP_PROXY": "", "https_proxy": "", "http_proxy": "",
        "ALL_PROXY": "", "all_proxy": "", "NO_PROXY": "", "no_proxy": "",
        "NODE_TLS_REJECT_UNAUTHORIZED": "1", "NODE_EXTRA_CA_CERTS": "",
    })
    # Auth is step environment only. Reviewed policy cannot inject another key.
    env.pop("ANTHROPIC_AUTH_TOKEN", None)
    env.pop("CHUBBY_API_KEY", None)
    policy["apiKeyHelper"] = ""
    policy["otelHeadersHelper"] = ""
    policy["enableAllProjectMcpServers"] = False
    policy["sandbox"]["enableWeakerNestedSandbox"] = False
    home = Path(tempfile.mkdtemp(prefix="ara-chubby-", dir=runner_temp))
    # Moving HOME must not move the sandbox's home-directory protection away
    # from the real runner's provider credentials. Keep both homes denied.
    real_home = str(Path.home().resolve())
    policy["sandbox"]["filesystem"]["denyRead"].append(real_home + "/")
    # Read denies outrank the sandbox allowRead exceptions. Mirror only the
    # reviewed credential rules: a whole-home Read deny would also deny this
    # repository when the runner checkout lives beneath its original home.
    home_read_rules = [rule for rule in policy["permissions"]["deny"]
                       if rule.startswith("Read(~/")]
    policy["permissions"]["deny"].extend(
        "Read(/" + real_home + "/" + rule[len("Read(~/"):]
        for rule in home_read_rules
    )
    config_dir = home / ".claude"
    config_dir.mkdir(mode=0o700)
    env.update({"HOME": str(home), "CLAUDE_CONFIG_DIR": str(config_dir)})
    settings = home / "policy.json"
    settings.write_text(json.dumps(policy))
    settings.chmod(0o600)
    args.extend(["--setting-sources", "user,project", "--settings", str(settings), "--model", model])
    return {"home": str(home), "config-dir": str(config_dir),
            "claude-args": shlex.join(args)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--github-output", type=Path, required=True)
    args = parser.parse_args()
    try:
        outputs = prepare(Path.cwd(), Path(os.environ["RUNNER_TEMP"]),
                          os.environ.get("CHUBBY_API_KEY", ""),
                          os.environ.get("CHUBBY_BASE_URL", DEFAULT_BASE_URL),
                          os.environ.get("CHUBBY_MODEL", ""),
                          os.environ.get("CLAUDE_ARGS", ""))
    except (ValueError, OSError, KeyError):
        # Config errors deliberately do not echo values or arbitrary exception text.
        print("::error::Invalid Chubby run configuration; check scoped key, endpoint, model, arguments, and project sandbox policy")
        return 2
    with args.github_output.open("a") as output:
        for key, value in outputs.items():
            delimiter = "CHUBBY_" + uuid.uuid4().hex
            output.write(f"{key}<<{delimiter}\n{value}\n{delimiter}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
