#!/usr/bin/env python3
"""Run a local generative-research article through ../oracle.

This is the local counterpart to .github/workflows/generative-research.yml:

1. Bundle ARA docs, prior local context, and recent research artifacts.
2. Ask Oracle / GPT-5.5 Pro for a single .ara.md article source.
3. Extract the ARA source, compile-check it, then hand it to the existing
   writer so the dashboard index and git commit path stay unchanged.

Oracle does the model call; scripts/write_generative_research.py remains the
only publisher.
"""

from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
DEFAULT_ORACLE_DIR = (REPO / "../oracle").resolve()


def run(cmd: list[str], *, cwd: Path = REPO, check: bool = True) -> subprocess.CompletedProcess[str]:
    printable = " ".join(shlex.quote(c) for c in cmd)
    print(f"+ {printable}", file=sys.stderr)
    return subprocess.run(cmd, cwd=str(cwd), check=check, text=True, capture_output=False)


def capture(cmd: list[str], *, cwd: Path = REPO, check: bool = True) -> str:
    return subprocess.run(cmd, cwd=str(cwd), check=check, text=True, capture_output=True).stdout


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:60].rstrip("-") or "untitled"


def latest(pattern: str) -> Path | None:
    matches = sorted(REPO.glob(pattern))
    return matches[-1] if matches else None


def existing(path: str) -> Path | None:
    p = REPO / path
    return p if p.exists() else None


def collect_context_files(extra: list[str]) -> list[Path]:
    candidates: list[Path | None] = [
        existing("ARA_DSL.md"),
        existing("COMPONENTS.md"),
        existing("docs/generative-research-backends.md"),
        existing("research/generative/index.json"),
        existing("research/generative/2026-05-15T072758--components.ara.md"),
        latest("research/digest/*-digest.md"),
        latest("research/models/*-timeline.md"),
        latest("research/arxiv/*-papers.md"),
        latest("research/twitter/*.md"),
        latest("research/twitter-deepseek/*.md"),
        latest("research/community/*-hn.md"),
        latest("research/community/*-reddit.md"),
        latest("research/bluesky/*.md"),
    ]
    for raw in extra:
        p = (REPO / raw).resolve() if not Path(raw).is_absolute() else Path(raw)
        if p.exists():
            candidates.append(p)
        else:
            print(f"warn: extra context file not found: {raw}", file=sys.stderr)

    seen: set[Path] = set()
    files: list[Path] = []
    for p in candidates:
        if p is None:
            continue
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            files.append(rp)
    return files


def oracle_command(oracle_dir: Path) -> list[str]:
    override = os.environ.get("ORACLE_BIN")
    if override:
        return shlex.split(override)

    built = oracle_dir / "dist/bin/oracle-cli.js"
    if built.exists():
        return ["node", str(built)]

    tsx = oracle_dir / "node_modules/.bin/tsx"
    if tsx.exists():
        return ["pnpm", "-C", str(oracle_dir), "exec", "tsx", "bin/oracle-cli.ts"]

    raise SystemExit(
        f"Oracle checkout is not built: {oracle_dir}\n"
        "Run: pnpm -C ../oracle install\n"
        "Or set ORACLE_BIN to a runnable oracle command."
    )


def build_prompt(topic: str, slug: str, tags: str, prior_context: str) -> str:
    return f"""You are writing a dashboard-ready ARA generative-research article.

Reason from first principles. Before drafting, stress-test the premise:
- What is actually being asked?
- What mechanics and constraints determine the answer?
- What do the attached files prove directly versus merely suggest?
- What would falsify the thesis?

Topic: {topic}
Slug: {slug}
Tags: {tags or "(none)"}

Use the attached ARA_DSL.md and COMPONENTS.md exactly. Output must be valid
.ara.md source, not raw HTML. The local checker will run:

uv run python scripts/check_generative_research.py "$DRAFT" --diversity-min 3 --callout-max 5 --strict-shape

Hard output contract:
- Return ONLY the article source between these exact markers:
  BEGIN_ARA_MD
  END_ARA_MD
- The first line after BEGIN_ARA_MD must be YAML frontmatter starting with ---.
- Include title, deck, lede, and optional stats in frontmatter.
- Use 5-9 numbered ## sections.
- Include at least 3 distinct visualization primitives from ARA_DSL.
- Every substantive factual claim needs a [^N] citation.
- End with a :::references block containing every cited source.
- Do not include commentary outside the markers.

Recent prior-context lookup:

{prior_context.strip() or "(no prior context returned)"}

Research standard:
- Prefer primary sources: vendor docs, GitHub/llama.cpp PRs, benchmark posts,
  Apple specs, NVIDIA specs, official model cards, pricing pages, and papers.
- For home inference, distinguish throughput, latency, VRAM/unified memory,
  memory bandwidth, power draw, thermal/noise, admin overhead, and API fallback.
- Treat Mac mini fleets and consumer GPU boxes as different systems, not
  interchangeable "local AI" vibes.
- Include what would make the home rack thesis wrong.
"""


def extract_ara(text: str) -> str:
    marker = re.search(r"BEGIN_ARA_MD\s*(.*?)\s*END_ARA_MD", text, re.DOTALL)
    if marker:
        return marker.group(1).strip() + "\n"

    fence = re.search(r"```(?:ara\.md|markdown|md)?\s*(---\n.*?\n)```", text, re.DOTALL)
    if fence:
        return fence.group(1).strip() + "\n"

    stripped = text.strip()
    if stripped.startswith("---\n"):
        return stripped + "\n"

    raise SystemExit(
        "Oracle output did not contain BEGIN_ARA_MD/END_ARA_MD or a .ara.md fence. "
        "Inspect the oracle output path printed above."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", help="research topic")
    parser.add_argument("--slug", default="", help="dashboard slug; defaults to slugified topic")
    parser.add_argument("--tags", default="", help="comma-separated dashboard tags")
    parser.add_argument("--model", default="gpt-5.5-pro", help="Oracle model id")
    parser.add_argument("--engine", default="browser", choices=["browser", "api"], help="Oracle engine")
    parser.add_argument("--oracle-dir", default=str(DEFAULT_ORACLE_DIR), help="path to local oracle checkout")
    parser.add_argument("--thinking", default="heavy", choices=["light", "standard", "extended", "heavy"])
    parser.add_argument("--timeout", default="60m", help="Oracle/browser timeout")
    parser.add_argument("--extra-file", action="append", default=[], help="extra context file to attach")
    parser.add_argument("--no-commit", action="store_true", help="publish files but skip writer git commit")
    parser.add_argument("--oracle-dry-run", action="store_true", help="preview Oracle bundle only")
    args = parser.parse_args(argv)

    topic = args.topic.strip()
    if not topic:
        raise SystemExit("topic is required")
    slug = args.slug.strip() or slugify(topic)

    tmpdir = Path(tempfile.mkdtemp(prefix="ara-oracle-"))
    prior_path = tmpdir / "prior-context.txt"
    oracle_output = tmpdir / "oracle-output.md"
    draft_path = tmpdir / f"{slug}.ara.md"

    prior = capture(["python3", "scripts/prior_context.py", topic], check=False)
    prior_path.write_text(prior, encoding="utf-8")

    context_files = collect_context_files(args.extra_file)
    context_files.append(prior_path)

    prompt = build_prompt(topic, slug, args.tags, prior)
    cmd = [
        *oracle_command(Path(args.oracle_dir).resolve()),
        "--engine",
        args.engine,
        "--model",
        args.model,
        "--slug",
        f"ara-{slug}",
        "--write-output",
        str(oracle_output),
        "--timeout",
        args.timeout,
        "--files-report",
        "-p",
        prompt,
    ]

    if args.engine == "browser":
        cmd += [
            "--browser-manual-login",
            "--browser-auto-reattach-delay",
            "5s",
            "--browser-auto-reattach-interval",
            "3s",
            "--browser-auto-reattach-timeout",
            "60s",
            "--browser-thinking-time",
            args.thinking,
        ]
    else:
        cmd += ["--provider", "openai", "--wait"]

    if args.oracle_dry_run:
        cmd += ["--dry-run", "summary"]

    for path in context_files:
        cmd += ["--file", str(path)]

    print(f"oracle output: {oracle_output}", file=sys.stderr)
    print(f"draft path:    {draft_path}", file=sys.stderr)
    run(cmd)

    if args.oracle_dry_run:
        return 0

    raw_output = oracle_output.read_text(encoding="utf-8")
    draft = extract_ara(raw_output)
    draft_path.write_text(draft, encoding="utf-8")

    run([
        "python3",
        "scripts/check_generative_research.py",
        str(draft_path),
        "--diversity-min",
        "3",
        "--callout-max",
        "5",
        "--strict-shape",
    ])

    writer = [
        "python3",
        "scripts/write_generative_research.py",
        "--topic",
        topic,
        "--slug",
        slug,
        "--tags",
        args.tags,
        "--source",
        "local-oracle",
        "--prompt",
        prompt,
        "--model",
        args.model,
        "--html-body",
        str(draft_path),
    ]
    if args.no_commit:
        writer.append("--no-commit")
    run(writer)

    print(f"done: published {slug} from {draft_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
