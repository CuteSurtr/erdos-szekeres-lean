"""Exact small-assignment checks of the explicit OPB coefficient serializer."""
from itertools import product
import unittest
from regenerate_opb import encode, parse


class OpbTests(unittest.TestCase):
    def test_coefficients_and_all_assignments(self):
        for n in range(1, 7):
            rows = [(list(range(n)), n // 2), (list(range(0, n, 2)), 1)]
            for budget in range(n + 1):
                text = encode(n, rows, budget, (0,))
                constraints = parse(text)
                self.assertEqual(len(constraints), len(rows) + 2)
                for bits in product((0, 1), repeat=n):
                    expected = (sum(bits) <= budget and bits[0] == 0 and
                                all(sum(bits[i] for i in support) >= demand for support, demand in rows))
                    actual = all(sum(coefficient * bits[i] for coefficient, i in pairs) >= rhs
                                 for pairs, rhs in constraints)
                    self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
