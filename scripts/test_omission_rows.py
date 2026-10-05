"""Finite relaxation controls; none asserts a geometric Erdős–Szekeres result."""
import importlib.util
import json
from itertools import product
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
    def test_cnf_against_all_original_assignments(self):
        import z3
        from omission_cnf import encode, hole_variables

        def check(n, rows, budget, alternatives=None):
            dimacs = encode(n, rows, budget, alternatives)
            mapping = hole_variables(dimacs)
            header = next(s for s in dimacs.splitlines() if s.startswith("p cnf")).split()
            variables = {i: z3.Bool(f"v{i}") for i in range(1, int(header[2]) + 1)}
            solver = z3.Solver()
            for line in dimacs.splitlines():
                if line.startswith(("c", "p")) or not line.strip():
                    continue
                literals = list(map(int, line.split()))
                self.assertEqual(literals[-1], 0)
                solver.add(z3.Or([variables[x] if x > 0 else z3.Not(variables[-x])
                                  for x in literals[:-1]]))
            for bits in product((False, True), repeat=n):
                solver.push()
                for label, variable in mapping.items():
                    solver.add(variables[variable] == bits[label])
                missing = [i for i, bit in enumerate(bits) if bit]
                expected = valid_holes(n, rows, budget, missing) and (alternatives is None or
                    any(set(s).isdisjoint(missing) for s in alternatives))
                self.assertEqual(solver.check() == z3.sat, expected)
                solver.pop()

        for n in range(1, 6):
            rows = [(list(range(n)), n // 2)]
            for budget in range(n + 1):
                check(n, rows, budget)
                if n >= 3:
                    check(n, rows + [([0, 2], 1)], budget, [[0, 1], [1, 2]])

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
