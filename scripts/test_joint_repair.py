"""Independent arithmetic and optional solver checks for joint point moves."""
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import tempfile
import unittest

from joint_vertical_repair import orientation_coefficients, run
from search import orient


class JointCoefficientTests(unittest.TestCase):
    def test_against_direct_determinants(self):
        original = [(0, 0), (2, 3), (5, -2), (7, 8)]
        for moving in ((0,), (0, 2), (0, 1, 2, 3)):
            for values in product((-5, 0, 9), repeat=len(moving)):
                points = original.copy()
                for index, value in zip(moving, values):
                    points[index] = (points[index][0], value)
                for triple in combinations(range(4), 3):
                    coefficients = orientation_coefficients(original, moving, triple)
                    value = sum(a * y for a, y in zip(coefficients, values)) + coefficients[-1]
                    actual = orient(*(points[i] for i in triple))
                    self.assertEqual((value > 0) - (value < 0), (actual > 0) - (actual < 0))


@unittest.skipUnless(importlib.util.find_spec("z3"), "optional Z3 dependency")
class JointSolverTests(unittest.TestCase):
    def check_fixture(self, points):
        with tempfile.TemporaryDirectory() as folder:
            source, output = (Path(folder) / name for name in ("input.json", "output.json"))
            source.write_text(json.dumps({"gon": 4, "coordinates": points}))
            return run(source, output, list(range(len(points))), seconds=15)

    def test_four_points_sat(self):
        result = self.check_fixture([(0, 0), (1, 0), (2, 1), (3, 3)])
        self.assertEqual(result["status"], "sat")
        self.assertTrue(result["candidate_avoids_gon_verified"])

    def test_five_points_unsat(self):
        result = self.check_fixture([(i, i * i) for i in range(5)])
        self.assertEqual(result["status"], "unsat")
        self.assertGreater(len(result["cuts"]), 0)


if __name__ == "__main__":
    unittest.main()
