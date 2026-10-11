"""Numerical controls for the integer Erdős–Szekeres lower-bound witnesses."""
from itertools import combinations
import random
import unittest

from es_lower_bound_witness import (general_position, largest_convex_subset,
                                    orient, witness)


def convex_position(points):
    """No point lies in a triangle of three others."""
    for d in points:
        for a, b, c in combinations([p for p in points if p != d], 3):
            o = orient(a, b, c)
            if all(o * orient(*e, d) > 0 for e in [(a, b), (b, c), (c, a)]):
                return False
    return True


def brute_force(points):
    best = min(len(points), 2)
    for r in range(3, len(points) + 1):
        if not any(convex_position(list(c)) for c in combinations(points, r)):
            break
        best = r
    return best


class WitnessTests(unittest.TestCase):
    def test_witnesses_have_no_convex_n_gon(self):
        for n in range(3, 9):
            with self.subTest(n=n):
                points = witness(n)
                self.assertEqual(len(set(points)), 2 ** (n - 2))
                self.assertEqual(len({x for x, _ in points}), 2 ** (n - 2))
                self.assertTrue(general_position(points))
                self.assertEqual(largest_convex_subset(points), n - 1)

    def test_dynamic_program_matches_brute_force(self):
        rng = random.Random(1)
        checked = 0
        while checked < 150:
            points = list({(rng.randint(-30, 30), rng.randint(-30, 30))
                           for _ in range(rng.randint(3, 9))})
            if general_position(points):
                self.assertEqual(largest_convex_subset(points), brute_force(points))
                checked += 1

    def test_points_in_convex_position(self):
        parabola = [(x, x * x) for x in range(-6, 7)]
        self.assertEqual(largest_convex_subset(parabola), len(parabola))


if __name__ == '__main__':
    unittest.main()
