"""Finite relaxation controls; none asserts a geometric Erdős–Szekeres result."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from omission_row_probe import read_rows, run, valid_holes


class OmissionRowTests(unittest.TestCase):
    def test_exact_counts_and_invalid_rows(self):
        data = {"states": [[], [], []], "constraints": [
            {"support": [0, 1], "rhs": 1}, {"support": [1, 2], "rhs": 1}]}
        n, rows = read_rows(data)
        self.assertTrue(valid_holes(n, rows, 1, [1]))
        self.assertFalse(valid_holes(n, rows, 1, [0]))
        self.assertFalse(valid_holes(n, rows, 2, [1, 1]))
        self.assertFalse(valid_holes(n, rows, 2, [1, 3]))
        data["constraints"][0]["support"] = [0, 0]
        with self.assertRaises(ValueError):
            read_rows(data)


@unittest.skipUnless(importlib.util.find_spec("z3"), "optional Z3 dependency")
class OmissionSolverTests(unittest.TestCase):
    def check(self, budget):
        with tempfile.TemporaryDirectory() as folder:
            source, output = (Path(folder)/s for s in ("source.json", "output.json"))
            source.write_text(json.dumps({"states": [[], [], []], "constraints": [
                {"support": [0, 1], "rhs": 1}, {"support": [1, 2], "rhs": 1}]}))
            return run(source, output, budget=budget, seconds=5)

    def test_one_hole_sat(self):
        result = self.check(1)
        self.assertEqual(result["status"], "sat")
        self.assertEqual(result["holes"], [1])

    def test_zero_holes_unsat(self):
        self.assertEqual(self.check(0)["status"], "unsat")


if __name__ == "__main__":
    unittest.main()
