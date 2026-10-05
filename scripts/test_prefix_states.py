"""Cross-check incoming ranks against exhaustive monochromatic subsequences."""
from itertools import combinations
import unittest

from prefix_states import incoming_states, signotope_masks


class PrefixStateTests(unittest.TestCase):
    def test_ranks_by_exhaustive_chains(self):
        self.assertEqual(len(list(signotope_masks(4))), 8)
        n = 5
        patterns = list(signotope_masks(n))
        self.assertEqual(len(patterns), 62)
        index = {t: i for i, t in enumerate(combinations(range(n), 3))}
        for mask in patterns:
            states = []
            for v in range(n):
                heights = [0] * 4
                for u in range(v):
                    ranks = [1, 1]
                    for size in range(u + 1):
                        for prefix in combinations(range(u), size):
                            chain = prefix + (u, v)
                            for sign in (0, 1):
                                if all((mask >> index[tuple(chain[i:i+3])]) & 1 == sign
                                       for i in range(len(chain) - 2)):
                                    ranks[sign] = max(ranks[sign], len(chain) - 1)
                    for x in range(ranks[0]):
                        heights[x] = max(heights[x], ranks[1])
                states.append(tuple(heights))
            self.assertEqual(incoming_states(n, mask, 4, 4), tuple(states))


if __name__ == "__main__":
    unittest.main()
