"""Exhaustive small semantic checks for the direct integer-row exporter."""
from itertools import product
import re
import unittest

from omission_opb import encode
from omission_row_probe import valid_holes


def evaluate(opb, assignment):
    """Interpret the emitted OPB subset independently using integer arithmetic."""
    lines = opb.splitlines()
    header = re.fullmatch(r"\* #variable= (\d+) #constraint= (\d+) #equal= 0 intsize= \d+", lines[0])
    assert header and int(header[1]) == len(assignment)
    assert int(header[2]) == len(lines) - 1
    answers = []
    for line in lines[1:]:
        left, right = line.split(">=")
        bound = re.fullmatch(r"\s*(-?\d+)\s*;", right)
        assert bound
        terms = left.split()
        assert len(terms) % 2 == 0
        total = 0
        for coefficient, variable in zip(terms[::2], terms[1::2]):
            assert re.fullmatch(r"x[1-9]\d*", variable)
            total += int(coefficient) * assignment[int(variable[1:]) - 1]
        answers.append(total >= int(bound[1]))
    return all(answers)


class OmissionOpbTests(unittest.TestCase):
    def test_all_assignments_and_budgets(self):
        for n in range(1, 7):
            families = [[], [([], 0)], [(list(range(n)), n // 2)],
                        [(list(range(n)), n), ([0], 1)]]
            if n >= 3:
                families.append([([0, 1], 1), ([1, 2], 2)])
            for rows in families:
                for budget in range(n + 1):
                    opb = encode(n, rows, budget)
                    for bits in product((0, 1), repeat=n):
                        holes = [i for i, bit in enumerate(bits) if bit]
                        self.assertEqual(evaluate(opb, bits), valid_holes(n, rows, budget, holes))

    def test_rejects_invalid_constraints(self):
        for n, rows, budget in [(0, [], 0), (2, [], -1), (2, [], 3),
                                (2, [([0, 0], 1)], 1), (2, [([2], 1)], 1),
                                (2, [([0], 2)], 1), (2, [([0], 0.5)], 1)]:
            with self.assertRaises(ValueError):
                encode(n, rows, budget)


if __name__ == "__main__":
    unittest.main()
