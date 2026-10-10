"""Reject altered literal-row provenance before any compiler is invoked."""
import copy
import json
import unittest
from unittest.mock import patch

import check


class PreflightTests(unittest.TestCase):
    def test_changed_row_binding_identity(self):
        manifest = json.loads((check.HERE / "manifest.json").read_text())
        changed = copy.deepcopy(manifest)
        changed["inputs"]["row-bindings.json"] = "0" * 64
        with patch.object(check.subprocess, "run", side_effect=AssertionError("unexpected compiler")):
            with self.assertRaisesRegex(ValueError, "Changed bundle input: row-bindings.json"):
                check.preflight(changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
