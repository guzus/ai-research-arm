import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = ROOT / ".claude" / "settings.json"


class ClaudeSandboxPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))

    def test_runtime_socket_mask_uses_canonical_directory(self) -> None:
        deny_read = self.settings["sandbox"]["filesystem"]["denyRead"]

        # On Ubuntu /var/run is a symlink to /run. bubblewrap cannot mount the
        # denyRead tmpfs on that symlink and aborts before the command starts.
        self.assertIn("/run", deny_read)
        self.assertNotIn("/var/run", deny_read)

        if sys.platform.startswith("linux"):
            noncanonical_paths = [
                (str(path), str(path.resolve()))
                for raw_path in deny_read
                if (path := Path(raw_path).expanduser()).exists()
                and path.absolute() != path.resolve()
            ]
            self.assertEqual(
                [],
                noncanonical_paths,
                "bubblewrap denyRead mounts must target canonical paths",
            )

    def test_tool_permission_matches_runtime_socket_mask(self) -> None:
        permissions = self.settings["permissions"]["deny"]

        self.assertIn("Read(//run/**)", permissions)
        # Keep the lexical alias denied for the Read tool even though bwrap
        # must only receive the canonical /run mount destination.
        self.assertIn("Read(//var/run/**)", permissions)

    def test_research_tree_has_no_committed_diagnostic_dotfiles(self) -> None:
        allowed = {".gitignore", ".gitkeep"}
        unexpected = []
        for path in (ROOT / "research").rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT / "research")
            hidden_components = [part for part in relative.parts if part.startswith(".")]
            if not hidden_components:
                continue
            if hidden_components == [path.name] and path.name in allowed:
                continue
            unexpected.append(str(path.relative_to(ROOT)))

        self.assertEqual([], sorted(unexpected))


if __name__ == "__main__":
    unittest.main()
