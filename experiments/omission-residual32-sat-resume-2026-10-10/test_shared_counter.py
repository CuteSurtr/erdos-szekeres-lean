"""Exhaustive existential-auxiliary controls of the experimental encoding."""
from itertools import product
import unittest
import z3
from shared_counter import Circuit, encode


def solver_for(dimacs):
    count = int(next(s for s in dimacs.splitlines() if s.startswith("p cnf")).split()[2])
    variables = [None] + [z3.Bool(f"v{i}") for i in range(1, count + 1)]
    solver = z3.Solver()
    for line in dimacs.splitlines():
        if line.startswith(("c", "p")):
            continue
        lits = list(map(int, line.split()))
        assert lits[-1] == 0
        solver.add(z3.Or([variables[x] if x > 0 else z3.Not(variables[-x]) for x in lits[:-1]]))
    return solver, variables


class CounterTests(unittest.TestCase):
    def test_outside_reference_radius(self):
        for n in range(2, 7):
            reference = tuple(range(0, n, 2))
            rows = [(list(range(n)), 1)]
            for radius in range(n // 2 + 1):
                solver, variables = solver_for(encode(n, rows, n - 1, (), reference, radius))
                for bits in product((False, True), repeat=n):
                    solver.push()
                    solver.add(*(variables[i + 1] == b for i, b in enumerate(bits)))
                    expected = 1 <= sum(bits) <= n - 1 and sum(bits[i] for i in range(n) if i not in reference) <= radius
                    self.assertEqual(solver.check() == z3.sat, expected)
                    solver.pop()

    def test_every_threshold_truth_value(self):
        # Check both output truth values, not just satisfying input witnesses.
        for n in range(1, 8):
            c = Circuit(n)
            outputs = [c.threshold(tuple(range(1, n + 1)), k) for k in range(1, n + 1)]
            solver, variables = solver_for(c.dimacs(n))
            for bits in product((False, True), repeat=n):
                solver.push()
                solver.add(*(variables[i + 1] == b for i, b in enumerate(bits)))
                self.assertEqual(solver.check(), z3.sat)
                for k, out in enumerate(outputs, start=1):
                    solver.push()
                    solver.add(variables[out] != (sum(bits) >= k))
                    self.assertEqual(solver.check(), z3.unsat)
                    solver.pop()
                solver.pop()

    def test_combined_rows_budget_and_occupied(self):
        for n in range(1, 7):
            rows = [(list(range(n)), n // 2), (list(range(0, n, 2)), 1)]
            for budget in range(n + 1):
                for occupied in ((), (0,)):
                    solver, variables = solver_for(encode(n, rows, budget, occupied))
                    for bits in product((False, True), repeat=n):
                        solver.push()
                        solver.add(*(variables[i + 1] == b for i, b in enumerate(bits)))
                        expected = (sum(bits) <= budget and all(not bits[i] for i in occupied)
                                    and all(sum(bits[i] for i in support) >= demand for support, demand in rows))
                        self.assertEqual(solver.check() == z3.sat, expected)
                        solver.pop()


if __name__ == "__main__":
    unittest.main()
