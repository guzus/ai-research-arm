#!/usr/bin/env python3
"""The generative-research `prompt:` input must stay under a safe ceiling.

Run: uv run python -m unittest scripts.test_generative_prompt_size

WHY THIS GATE EXISTS — a real outage, 2026-08-02.

`anthropics/claude-code-action@v1` has a size ceiling on its `prompt:` input.
Cross it and the action stops invoking the agent, but does NOT fail: the step
reports `success`, runs for ~2 seconds, writes NO execution file, and produces
no article. `show_full_output: false` hides the provider-side cause. The
workflow then fails much later at "Fail Claude run without article", which
points at everything except the real problem.

Observed, same runner and same credential:

    main    prompt 52,741 chars -> Claude step ran 3,171 s, article published
    branch  prompt 83,978 chars -> Claude step ran ~2 s, no execution file

The exact ceiling is not documented by the action, so this gate uses a
CONSERVATIVE limit anchored to the largest size empirically proven to work,
plus modest headroom. That is deliberately pessimistic: the cost of being
under is a doc pointer, and the cost of being over is a lane that looks
green in CI, passes every other gate here, and silently produces nothing in
production.

HOW TO STAY UNDER IT. Do not delete guidance — MOVE it. Reference material
belongs in `docs/*.md`, which CLAUDE.md already documents as "read at runtime
by the agents", and the prompt keeps a short imperative plus the path:

    docs/generative-research-toolbelt.md    tools + Twitter-seed procedure
    docs/generative-research-components.md  the ARA component vocabulary
    docs/generative-research-redteam.md     the step-6.5 red-team contract
    docs/claim-store.md                     claim reuse + candidate contract

Keep genuinely BEHAVIOURAL rules inline (anti-patterns, "claim store first",
the never-write-empty-findings invariant). Move REFERENCE material out.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "generative-research.yml"

# Largest size empirically proven to invoke the agent (main, run 30741406379).
PROVEN_WORKING = 52_741
# Ceiling with headroom over the proven size, comfortably below the ~64 KB
# boundary the 83,978-char failure sat above. Raise ONLY with evidence from a
# real run that a larger prompt still invokes the agent.
MAX_PROMPT_CHARS = 60_000


def _prompts() -> dict[str, str]:
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for job in (data.get("jobs") or {}).values():
        for step in job.get("steps") or []:
            with_block = step.get("with") or {}
            if "prompt" in with_block:
                key = step.get("id") or step.get("name") or f"step-{len(out)}"
                out[key] = with_block["prompt"]
    return out


class GenerativePromptSizeTests(unittest.TestCase):
    def test_workflow_has_prompt_bearing_steps(self):
        """Guard the guard: a parsing change must not silently pass this file."""
        prompts = _prompts()
        self.assertGreaterEqual(
            len(prompts), 2, "expected the claude and fireworks prompt families"
        )

    def test_every_prompt_is_under_the_ceiling(self):
        for name, prompt in _prompts().items():
            with self.subTest(step=name):
                self.assertLessEqual(
                    len(prompt),
                    MAX_PROMPT_CHARS,
                    f"{name} prompt is {len(prompt):,} chars, over the "
                    f"{MAX_PROMPT_CHARS:,} ceiling. Over the action's limit the "
                    "agent is never invoked and the step still reports success "
                    "— move reference material into docs/*.md and leave a "
                    "pointer. See this module's docstring.",
                )

    def test_prompts_still_point_at_the_externalised_contracts(self):
        """Shrinking must not orphan the docs the prompt delegates to."""
        required = [
            "docs/generative-research-toolbelt.md",
            "docs/generative-research-components.md",
            "docs/generative-research-redteam.md",
            "docs/claim-store.md",
        ]
        for name, prompt in _prompts().items():
            for doc in required:
                with self.subTest(step=name, doc=doc):
                    self.assertIn(
                        doc,
                        prompt,
                        f"{name} no longer references {doc}; the agent would "
                        "lose that contract entirely",
                    )

    def test_referenced_contract_docs_exist_on_disk(self):
        seen: set[str] = set()
        for prompt in _prompts().values():
            for token in prompt.split():
                cleaned = token.strip("`,.;:()[]'\"")
                if cleaned.startswith("docs/") and cleaned.endswith(".md"):
                    seen.add(cleaned)
        self.assertTrue(seen, "expected the prompt to delegate to docs/*.md")
        for doc in sorted(seen):
            with self.subTest(doc=doc):
                self.assertTrue(
                    (REPO_ROOT / doc).is_file(),
                    f"prompt references {doc} but it does not exist — the agent "
                    "would follow a dead pointer and lose that contract",
                )


if __name__ == "__main__":
    unittest.main()
