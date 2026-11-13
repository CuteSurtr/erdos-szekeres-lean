"""Cross-check the geometric obstruction certificates and their replay."""
import unittest

from mixed_cap_certificate import fixture, interior, obstruction_certificates, verify
from search import hull


class MixedCapTests(unittest.TestCase):
    def test_full_replay(self):
        result = verify(*fixture())
        self.assertEqual(result["maximum_convex_cardinality"], 15)
        self.assertEqual(result["cap_cardinality_sum"], 16)
        self.assertEqual(result["sixteen_subsets_checked"], 74613)
        self.assertEqual(result["interior_certificate_count"], 672)

    def test_interior_certificates_against_hull(self):
        for certificate in obstruction_certificates(*fixture()):
            self.assertTrue(interior(*certificate))
            self.assertEqual(len(hull(certificate)), 3)
            self.assertNotIn(certificate[0], hull(certificate))

    def test_corrupted_fixture_rejected(self):
        anchors, chain, inner = fixture()
        chain[1] = (chain[1][0], chain[1][1] + 50000)
        with self.assertRaises(ValueError):
            verify(anchors, chain, inner)


if __name__ == "__main__":
    unittest.main()
