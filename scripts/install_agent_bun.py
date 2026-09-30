#!/usr/bin/env python3
"""Install the audited Claude-action Bun into a unique runner-temp directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PIN_FILE = ROOT / "data/toolchain-pins.json"


def validate_pins(pins: dict) -> None:
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", pins.get("version", "")):
        raise ValueError("agent_bun.version must be an exact release version")
    checksums = pins.get("sha256", {})
    if set(checksums) != {"linux_x64", "linux_aarch64"}:
        raise ValueError("agent_bun must pin both supported Linux architectures")
    if any(not re.fullmatch(r"[0-9a-f]{64}", value) for value in checksums.values()):
        raise ValueError("agent_bun checksums must be SHA-256 digests")


def install_bun(pins: dict, runner_temp: Path) -> Path:
    validate_pins(pins)
    arch = {"x86_64": "x64", "amd64": "x64", "aarch64": "aarch64", "arm64": "aarch64"}.get(
        platform.machine().lower()
    )
    if platform.system() != "Linux" or arch is None:
        raise ValueError("agent Bun supports Linux x64/aarch64 runners only")
    version = pins["version"]
    asset = f"bun-linux-{arch}"
    url = f"https://github.com/oven-sh/bun/releases/download/bun-v{version}/{asset}.zip"
    directory = Path(tempfile.mkdtemp(prefix="agent-bun-", dir=runner_temp))
    try:
        archive = directory / "download.zip"
        digest = hashlib.sha256()
        request = urllib.request.Request(url, headers={"User-Agent": "ARA-agent-bun"})
        with urllib.request.urlopen(request, timeout=60) as response, archive.open("wb") as output:
            for block in iter(lambda: response.read(1024 * 1024), b""):
                digest.update(block)
                output.write(block)
        if digest.hexdigest() != pins["sha256"][f"linux_{arch}"]:
            raise ValueError(f"Bun {version} {arch} archive SHA-256 mismatch")
        binary = directory / "bun"
        # Extract only the expected member after authentication; never trust
        # archive paths or overwrite the shared ~/.bun/bin/bun executable.
        with zipfile.ZipFile(archive) as release, release.open(f"{asset}/bun") as source:
            with binary.open("wb") as target:
                shutil.copyfileobj(source, target)
        binary.chmod(0o755)
        result = subprocess.run([str(binary), "--version"], text=True, capture_output=True, timeout=15)
        if result.returncode != 0 or result.stdout.strip() != version:
            raise ValueError(f"Installed Bun did not report pinned version {version}")
        (directory / "bunx").symlink_to("bun")
        archive.unlink()
        return binary
    except BaseException:
        shutil.rmtree(directory)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--github-output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        pins = json.loads(PIN_FILE.read_text())["agent_bun"]
        binary = install_bun(pins, Path(os.environ["RUNNER_TEMP"]))
        with args.github_output.open("a") as output:
            output.write(f"bun-path={binary}\nversion={pins['version']}\n")
    except (OSError, ValueError, KeyError, subprocess.SubprocessError, zipfile.BadZipFile) as error:
        print(f"::error::Cannot install isolated agent Bun: {error}", file=sys.stderr)
        return 1
    print(f"Installed verified Bun {pins['version']} at {binary}")
    # Keep the executable for Claude's post steps. The runner owns RUNNER_TEMP
    # cleanup; another invocation gets a distinct directory, even in this job.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
