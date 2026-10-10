"""An altered proof archive cannot pass provenance validation."""
import copy
import json
import unittest
from unittest.mock import patch

import check


class PreflightTests(unittest.TestCase):
    def test_changed_subtree_archive_is_rejected(self):
        manifest = json.loads((check.BUNDLE / "manifest.json").read_text())
        altered = copy.deepcopy(manifest)
        altered["proofs"][0]["archive_sha256"] = "0" * 64
        with patch.object(check.subprocess, "run", side_effect=AssertionError("unexpected compiler")):
            with self.assertRaisesRegex(ValueError, "Changed prerequisite: .*closed-context-492357"):
                check.preflight(altered)


if __name__ == "__main__":
    unittest.main(verbosity=2)
