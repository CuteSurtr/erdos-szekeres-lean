"""The preflight rejects altered provenance before launching any compiler."""
import copy
import json
import unittest
from unittest.mock import patch

import check


class ProvenancePreflightTests(unittest.TestCase):
    def test_valid_and_altered_source_identity(self):
        manifest = json.loads((check.BUNDLE / "manifest.json").read_text())
        with patch.object(check.subprocess, "run", side_effect=AssertionError("unexpected compiler")):
            checked = check.preflight(manifest)
            self.assertEqual(checked["source archive"], manifest["source_archive_sha256"])
            self.assertEqual(checked["pending contexts"], manifest["pending_contexts_sha256"])
            changed = copy.deepcopy(manifest)
            changed["source_archive_sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "Provenance mismatch for source archive"):
                check.preflight(changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
