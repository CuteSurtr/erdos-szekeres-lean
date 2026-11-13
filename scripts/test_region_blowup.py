"""Independent small geometric checks for the extremal-profile experiments."""
from itertools import combinations
from math import comb
import unittest

from region_blowup import cups_caps, monotone_convex_chain, profile
from search import general_position, orient


class RegionBlowupTests(unittest.TestCase):
    def test_cups_caps_against_exhaustive(self):
        for a, b in ((2, 4), (3, 3), (3, 4), (4, 3)):
            points = cups_caps(a, b)
            self.assertEqual(len(points), comb(a + b - 2, a - 1))
            self.assertTrue(general_position(points))
            for bound, sign in ((a, 1), (b, -1)):
                self.assertEqual(len(monotone_convex_chain(points, sign > 0)), bound)
                for subset in combinations(points, bound + 1):
                    self.assertTrue(any(sign * orient(*triple) < 0
                                        for triple in combinations(subset, 3)))

    def test_product_and_convexity_obstruction(self):
        result = profile(3, 3, 2, 2)
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(result["region_size"], 12)
        self.assertEqual(result["height"] * result["width"], 12)
        self.assertEqual(result["largest_ambient_convex_subset"], 6)
        self.assertEqual(result["exhaustive_upper_check"], {"gon": 7, "subsets_checked": 11440})


if __name__ == "__main__":
    unittest.main()
