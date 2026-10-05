"""Independent determinant checks, known geometric cases, and algebraic rounding."""
import importlib.util
import hashlib
from itertools import combinations, product
import json
from math import prod
from pathlib import Path
import tempfile
import unittest

from joint_planar_repair import integer_model, orientation_terms, run
from search import general_position, orient


class PlanarPolynomialTests(unittest.TestCase):
    def test_polynomial_signs_against_direct_geometry(self):
        original = [(0, 1), (2, 3), (5, -2), (7, 8)]
        for moving in ((0,), (0, 2), (0, 1, 2)):
            polynomials = {triple: orientation_terms(original, moving, triple)
                           for triple in combinations(range(4), 3)}
            for values in product((-3, 0, 4), repeat=2 * len(moving)):
                points = original.copy()
                for j, index in enumerate(moving):
                    points[index] = tuple(values[2 * j:2 * j + 2])
                for triple, terms in polynomials.items():
                    value = sum(c * prod(values[j] for j in monomial)
                                for monomial, c in terms.items())
                    actual = orient(*(points[i] for i in triple))
                    self.assertEqual((value > 0) - (value < 0), (actual > 0) - (actual < 0))


@unittest.skipUnless(importlib.util.find_spec("z3"), "optional Z3 dependency")
class PlanarSolverTests(unittest.TestCase):
    def check_fixture(self, points, moving):
        with tempfile.TemporaryDirectory() as folder:
            source, output = (Path(folder) / name for name in ("input.json", "output.json"))
            source.write_text(json.dumps({"gon": 4, "coordinates": points}))
            return run(source, output, moving, seconds=20)

    def test_four_points_sat(self):
        result = self.check_fixture([(0, 0), (1, 0), (2, 1), (3, 3)], [1, 2])
        self.assertEqual(result["status"], "sat")
        self.assertTrue(result["candidate_avoids_gon_verified"])
        self.assertEqual(result["coordinates"][0], (0, 0))
        scale = result["coordinate_scale"]
        self.assertEqual(result["coordinates"][3], (3 * scale, 3 * scale))

    def test_five_points_unsat(self):
        result = self.check_fixture([(i, i * i) for i in range(5)], [3, 4])
        self.assertEqual(result["status"], "unsat")
        self.assertGreater(len(result["cuts"]), 0)

    def test_algebraic_model_preserves_orientation(self):
        import z3
        x, y = z3.Reals("x y")
        solver = z3.SolverFor("QF_NRA")
        solver.add(x * x == 2, x > 0, y == 1)
        self.assertEqual(solver.check(), z3.sat)
        original = [(0, 0), (3, 0), (0, 3), (1, 1)]
        symbolic = [(0, 0), (3, 0), (0, 3), (x, y)]
        expressions = {triple: z3.simplify(z3.RealVal(1) * orient(*(symbolic[i] for i in triple)))
                       for triple in combinations(range(4), 3)}
        candidate, metadata = integer_model(original, (3,), [x, y], solver.model(), expressions)
        self.assertTrue(metadata["algebraic_model"])
        self.assertTrue(general_position(candidate))
        self.assertGreater(candidate[3][0], candidate[3][1])

    def test_invalid_resume_cycle_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            source, output, prior = (Path(folder) / name for name in
                                     ("input.json", "output.json", "prior.json"))
            source.write_text(json.dumps({"gon": 4, "coordinates":
                                          [(0, 0), (1, 0), (2, 1), (3, 3)]}))
            prior.write_text(json.dumps({"source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                                         "moving_indices": [1, 2], "gon": 4, "logic": "QF_NRA",
                                         "status": "unknown", "cuts": [[0, 1, 1, 3]]}))
            with self.assertRaises(ValueError):
                run(source, output, [1, 2], resume=prior)

    def test_cut_transfer_between_searches(self):
        with tempfile.TemporaryDirectory() as folder:
            source, output, cuts = (Path(folder) / name for name in
                                    ("input.json", "output.json", "cuts.json"))
            source.write_text(json.dumps({"gon": 4, "coordinates":
                                          [(0, 0), (1, 0), (2, 1), (3, 3)]}))
            cuts.write_text(json.dumps({"gon": 4, "points": 4,
                                       "cuts": [[0, 3, 2, 1], [0, 1, 2, 3]]}))
            result = run(source, output, [1, 2], seconds=20, seed_cuts=[cuts])
            self.assertEqual(result["status"], "sat")
            self.assertEqual(result["seed_cut_sources"][0]["retained_new_cuts"], 2)


if __name__ == "__main__":
    unittest.main()
