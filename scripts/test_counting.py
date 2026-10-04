import unittest
from itertools import product
from math import comb, prod
from counting_experiments import (
    balanced_horizontal_product, compressed_factor, horizontal_max_dp, relaxed_profile,
)


class CountingTests(unittest.TestCase):
    def test_vandermonde_compression(self):
        for tops in product(range(5), repeat=3):
            for bottoms in product(*(range(a + 1) for a in tops)):
                self.assertLessEqual(prod(comb(a, b) for a, b in zip(tops, bottoms)),
                                     comb(sum(tops), sum(bottoms)))

    def test_balancing_against_independent_dp(self):
        for n in range(5, 20):
            for k in range(4, n, 2):
                optimum = horizontal_max_dp(n, k // 2) ** 2
                self.assertEqual(balanced_horizontal_product(n, k), optimum)
                self.assertLessEqual(optimum, compressed_factor(n, k))

    def test_profiles_respect_relaxed_constraints(self):
        for n in range(5, 30):
            for k in range(4, n, 2):
                p = relaxed_profile(n, k)
                self.assertTrue(p["adjacent_budget_valid"])
                self.assertTrue(p["parity_budget_valid"])
                self.assertTrue(p["outer_budget_valid"])


if __name__ == "__main__":
    unittest.main()
