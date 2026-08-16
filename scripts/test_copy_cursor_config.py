import json
import tempfile
import unittest
from pathlib import Path

from copy_cursor_config import copy_config


class CopyCursorConfigTest(unittest.TestCase):
    def test_copies_permissions_without_injecting_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "cli-config.json"
            destination = root / "copied.json"
            source.write_text(json.dumps({
                "permissions": {"allow": ["Read(**/*)"], "deny": ["Mcp(*)"]},
            }))
            copy_config(source, destination, "cursor/composer-2.5")
            generated = json.loads(destination.read_text())
            self.assertEqual(["Read(**/*)"], generated["permissions"]["allow"])
            self.assertNotIn("model", generated)
            self.assertNotIn("provider", generated)
            self.assertEqual(0o400, destination.stat().st_mode & 0o777)

    def test_rejects_noncanonical_or_injectable_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "cli-config.json"
            source.write_text("{}")
            for model_ref in ("composer-2.5", "../x/y", "cursor/a/b", "x/ bad"):
                with self.subTest(model_ref=model_ref), self.assertRaises(ValueError):
                    copy_config(source, Path(tmp) / "out.json", model_ref)


if __name__ == "__main__":
    unittest.main()
