#!/usr/bin/env python3
"""Guard the generative-research `prompt:` size against a proven-good ceiling.

Run: uv run python -m unittest scripts.test_generative_prompt_size

WHY THIS GATE EXISTS — a real, expensive failure on 2026-08-02.

Growing this prompt broke the lane in a way NO existing gate could see.
`anthropics/claude-code-action@v1` stopped invoking the agent while still
reporting success: the step ran ~3 seconds, wrote no execution file, produced
no article, and emitted no error (`show_full_output: false` hides the cause).
CI stayed green. The workflow failed much later at "Fail Claude run without
article", pointing at everything except the real problem. It took four real
dispatches to localise.

Measured, with model / credential / runner / every other step input held
identical and only prompt length varying:

    52,741 chars -> Claude step ran 3,171 s, article published   (main)
    56,317 chars -> Claude step ran ~3 s, no execution file
    83,978 chars -> Claude step ran ~3 s, no execution file

BE HONEST ABOUT WHAT IS AND IS NOT KNOWN. A threshold somewhere inside a
3,576-char band is too tight to be a clean documented size limit, so the
MECHANISM IS NOT ESTABLISHED — it may not be raw length at all (encoding,
a specific construct, or an interaction). What IS established: 52,741 works
and 56,317 does not, on an otherwise identical step.

So this gate is deliberately empirical rather than principled. It pins the
prompt near the only size proven to invoke the agent. Raising it is allowed
but must be earned:

  1. Raise MAX_PROMPT_CHARS.
  2. Dispatch generative-research.yml from your branch WITHOUT a `backend`
     input (the default lane resolves opus-5; passing `backend=claude` pins
     claude-sonnet-5, a different path that also no-ops and will confound
     your result — that mistake cost two of the four runs above).
  3. Confirm the "Run Generative Research (Claude, attempt 1)" step runs for
     MINUTES, not seconds. A green CI run proves nothing here.

To add agent guidance without growing the prompt, put reference material in
`docs/*.md` — which CLAUDE.md already documents as "read at runtime by the
agents" — and leave a short imperative plus the path in the prompt.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "generative-research.yml"

PROVEN_WORKING = 52_741   # main run 30741406379: agent ran 3,171 s
PROVEN_BROKEN = 56_317    # branch run 30747747723: agent no-op'd in ~3 s
MAX_PROMPT_CHARS = 54_000  # between them, close to proven-good


def _prompts() -> dict[str, str]:
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for job in (data.get("jobs") or {}).values():
        for step in job.get("steps") or []:
            with_block = step.get("with") or {}
            if "prompt" in with_block:
                out[step.get("id") or step.get("name") or f"step-{len(out)}"] = with_block["prompt"]
    return out


class GenerativePromptSizeTests(unittest.TestCase):
    def test_ceiling_sits_between_the_measured_good_and_bad_sizes(self):
        """Guard the guard: the constant must stay empirically anchored."""
        self.assertGreaterEqual(MAX_PROMPT_CHARS, PROVEN_WORKING)
        self.assertLess(MAX_PROMPT_CHARS, PROVEN_BROKEN)

    def test_workflow_has_prompt_bearing_steps(self):
        """A parsing change must not let this file silently pass."""
        self.assertGreaterEqual(
            len(_prompts()), 2, "expected the claude and fireworks prompt families"
        )

    def test_every_prompt_is_under_the_ceiling(self):
        for name, prompt in _prompts().items():
            with self.subTest(step=name):
                self.assertLessEqual(
                    len(prompt),
                    MAX_PROMPT_CHARS,
                    f"{name} prompt is {len(prompt):,} chars, over the "
                    f"{MAX_PROMPT_CHARS:,} ceiling. Past this the action has been "
                    "observed to stop invoking the agent while still reporting "
                    "success — CI cannot see it. Move reference material into "
                    "docs/*.md, or raise the ceiling only with a real dispatch "
                    "proving the agent still runs for minutes. See this module's "
                    "docstring.",
                )


if __name__ == "__main__":
    unittest.main()
