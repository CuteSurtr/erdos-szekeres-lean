"""Optional solver checks; core CI does not need Z3."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from extend_configuration import run
from repair_near_miss import forbidden_subsets


@unittest.skipUnless(importlib.util.find_spec("z3"), "optional Z3 dependency")
class ExtensionSolverTests(unittest.TestCase):
    def check_allowance(self, allowance):
        with tempfile.TemporaryDirectory() as folder:
            source, output = (Path(folder) / s for s in ("input.json", "output.json"))
            source.write_text(json.dumps({"gon": 4, "coordinates":
                                        [(0, 0), (0, 1), (1, 1), (3, 2)]}))
            return run(source, output, seconds=10, fast=True, allowed_gons=allowance)

    def test_zero_allowance(self):
        self.assertEqual(self.check_allowance(0)["status"], "unsat")

    def test_one_allowance_is_not_counterexample(self):
        result = self.check_allowance(1)
        self.assertEqual(result["status"], "near_miss")
        self.assertFalse(result["candidate_avoids_gon_verified"])
        self.assertEqual(result["candidate_check"], "exhaustive subsets")
        self.assertEqual(result["candidate_subsets_checked"], 5)
        self.assertEqual(result["convex_gons_count"], 1)
        self.assertEqual(len(forbidden_subsets(result["coordinates"], 4)), 1)


if __name__ == "__main__":
    unittest.main()
