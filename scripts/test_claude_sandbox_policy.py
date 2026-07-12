import json
import re
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
        # Claude merges Read(...) denies into the Bash sandbox's denyRead
        # paths. Keeping the lexical alias here therefore recreates the broken
        # `bwrap --tmpfs /var/run` mount even when sandbox.filesystem.denyRead
        # correctly uses /run.
        aliases = [
            rule
            for rule in permissions
            if rule.startswith(("Read(//var/run", "Edit(//var/run"))
        ]
        self.assertEqual([], aliases)

        if sys.platform.startswith("linux"):
            noncanonical_paths = []
            for rule in permissions:
                match = re.fullmatch(r"(?:Read|Edit)\(//(.+?)(?:/\*\*)?\)", rule)
                if not match:
                    continue
                path = Path("/" + match.group(1))
                if path.exists() and path.absolute() != path.resolve():
                    noncanonical_paths.append((rule, str(path.resolve())))
            self.assertEqual(
                [],
                noncanonical_paths,
                "absolute Read/Edit denies merged into bwrap must be canonical",
            )

    def test_read_tool_can_access_workspace_under_home(self) -> None:
        permissions = self.settings["permissions"]["deny"]

        # GitHub checks out the repository below /home/guzus. Permission deny
        # rules take precedence, so Read(~/**) blocks the workspace even though
        # sandbox.filesystem.allowRead contains "." (that carve-out applies to
        # sandboxed subprocesses, not to the independent Read tool).
        self.assertNotIn("Read(~/**)", permissions)

        # Preserve direct-tool protection for the credential directories the
        # Bash sandbox masks instead of denying the runner's whole home tree.
        for path in (".aws", ".config/gh", ".docker", ".ssh", ".claude"):
            self.assertIn(f"Read(~/{path}/**)", permissions)
        self.assertIn("Read(~/.claude.json)", permissions)

    def test_git_remote_token_is_not_readable_via_file_tool(self) -> None:
        permissions = self.settings["permissions"]["deny"]
        allow_read = self.settings["sandbox"]["filesystem"]["allowRead"]

        # claude-code-action temporarily stores its GitHub credential in the
        # checkout's remote URL. Deny direct Read access, while the exact
        # sandbox allowRead carve-out keeps permitted Bash(git:*) operations
        # able to read the repository config.
        self.assertIn("Read(./.git/config)", permissions)
        self.assertIn(".git/config", allow_read)

    def test_sandbox_masks_agent_credentials(self) -> None:
        credentials = self.settings["sandbox"]["credentials"]
        denied_files = {
            item["path"] for item in credentials["files"] if item["mode"] == "deny"
        }
        denied_env = {
            item["name"] for item in credentials["envVars"] if item["mode"] == "deny"
        }

        self.assertTrue({"~/.claude", "~/.claude.json"} <= denied_files)
        self.assertTrue({"GITHUB_TOKEN", "GH_TOKEN"} <= denied_env)

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
