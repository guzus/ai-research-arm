import json
import tempfile
import unittest
from pathlib import Path

from build_opencode_config import build


class BuildOpenCodeConfigTest(unittest.TestCase):
    def test_injects_arbitrary_registered_model_and_preserves_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "base.json"
            destination = root / "generated.json"
            source.write_text(json.dumps({
                "$schema": "https://opencode.ai/config.json",
                "permission": {"edit": "allow", "bash": "allow"},
            }))
            build(source, destination, "opencode-go/novel-flash")
            generated = json.loads(destination.read_text())
            self.assertEqual("allow", generated["permission"]["edit"])
            self.assertEqual({}, generated["provider"]["opencode-go"]
                             ["models"]["novel-flash"])
            self.assertEqual(0o400, destination.stat().st_mode & 0o777)

    def test_rejects_noncanonical_or_injectable_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "base.json"
            source.write_text("{}")
            for model_ref in ("deepseek", "../x/y", "opencode-go/a/b", "x/ bad"):
                with self.subTest(model_ref=model_ref), self.assertRaises(ValueError):
                    build(source, Path(tmp) / "out.json", model_ref)

    def test_merges_existing_provider_catalog_without_static_global_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "base.json"
            source.write_text(json.dumps({
                "provider": {"opencode-go": {"models": {"old": {}}}},
                "permission": {"webfetch": "allow"},
            }))
            destination = root / "generated.json"
            build(source, destination, "opencode-go/new")
            generated = json.loads(destination.read_text())
            self.assertEqual({"old", "new"}, set(
                generated["provider"]["opencode-go"]["models"]
            ))
            self.assertNotIn("model", generated)


if __name__ == "__main__":
    unittest.main()
