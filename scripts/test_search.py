"""Independent small fixtures for the exact geometry used in experiments."""
import unittest
from itertools import combinations, product
from search import convex_subset, general_position, hull, orient, search_grid


def inside_triangle(p, a, b, c):
    signs = [orient(a, b, p), orient(b, c, p), orient(c, a, p)]
    return all(s > 0 for s in signs) or all(s < 0 for s in signs)


class GeometryTests(unittest.TestCase):
    def test_known_shapes(self):
        triangle_with_center = [(0, 0), (6, 0), (0, 6), (1, 1)]
        self.assertTrue(general_position(triangle_with_center))
        self.assertIsNone(convex_subset(triangle_with_center, 4))
        square = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.assertEqual(len(hull(square)), 4)
        self.assertIsNotNone(convex_subset(square, 4))

    def test_degeneracies(self):
        self.assertFalse(general_position([(0, 0), (1, 1), (2, 2)]))
        self.assertFalse(general_position([(0, 0), (0, 0)]))
        self.assertEqual(hull([(0, 0), (1, 1), (2, 2)]), [(0, 0), (2, 2)])

    def test_against_triangle_criterion(self):
        # Independent convexity criterion on every small grid configuration in GP.
        for size in (4, 5):
            for pts in combinations(list(product(range(4), repeat=2)), size):
                if general_position(pts):
                    no_interior_point = not any(
                        inside_triangle(p, *t)
                        for p in pts
                        for t in combinations([q for q in pts if q != p], 3)
                    )
                    self.assertEqual(len(hull(pts)) == size, no_interior_point)

    def test_grid_search(self):
        result = search_grid(4, 5, 4)
        self.assertTrue(result["grid_exhausted"])
        self.assertGreater(result["general_position_subsets_checked"], 0)
        self.assertIsNone(result["avoiding_configuration"])


if __name__ == "__main__":
    unittest.main()
