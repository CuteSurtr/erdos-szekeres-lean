"""Cross-check the extension cut criterion against an independent convex hull."""
from itertools import combinations, product
import unittest

from extend_configuration import evaluate, exactly_one_visible, line, primitive_line
from search import convex_subset, general_position, hull, largest_convex_subset, orient


class ExtensionTests(unittest.TestCase):
    def test_dynamic_program_against_exhaustive(self):
        checked = 0
        for points in combinations(list(product(range(3), repeat=2)), 5):
            if general_position(points):
                checked += 1
                expected = max(k for k in range(3, 6) if convex_subset(points, k))
                self.assertEqual(len(largest_convex_subset(points)), expected)
        self.assertGreater(checked, 10)
        self.assertEqual(largest_convex_subset([]), ())
        self.assertEqual(len(largest_convex_subset([(0, 0), (1, 0)])), 2)
        with self.assertRaises(ValueError):
            largest_convex_subset([(0, 0), (1, 0), (2, 0)])

    def test_line_representation(self):
        for a, b, q in (((2, 3), (-5, 1), (4, -9)), ((0, 0), (1, 0), (0, 1))):
            self.assertEqual(evaluate(line(a, b), *q), orient(a, b, q))
            self.assertEqual(evaluate(line(a, b), q[0] * 7, q[1] * 7, 7),
                             orient(a, b, q) * 7)
            for scale in (1, 1000000):
                aa, bb, qq = (tuple(scale * v for v in p) for p in (a, b, q))
                value = evaluate(primitive_line(aa, bb), *qq)
                self.assertEqual(value > 0, orient(aa, bb, qq) > 0)
                self.assertEqual(value == 0, orient(aa, bb, qq) == 0)

    def test_visible_edge_criterion(self):
        fixtures = (
            [(0, 0), (3, 0), (0, 3)],
            [(-2, -2), (2, -2), (2, 2), (-2, 2)],
            [(-3, 0), (-1, -3), (2, -2), (3, 1), (0, 3)],
            [(-3, 0), (-2, -2), (0, -3), (3, 0), (2, 2), (0, 3)],
        )
        checked = 0
        for polygon in fixtures:
            polygon = hull(polygon)
            for q in product(range(-5, 6), repeat=2):
                if general_position(polygon + [q]):
                    checked += 1
                    self.assertEqual(exactly_one_visible(polygon, q),
                                     len(hull(polygon + [q])) == len(polygon) + 1)
        self.assertGreater(checked, 100)


if __name__ == "__main__":
    unittest.main()
