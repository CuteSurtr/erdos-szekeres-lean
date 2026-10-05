"""Check certificate soundness against exhaustive assignments and corruptions."""
import copy
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import tempfile
import unittest

from omission_row_probe import valid_holes
from omission_tree import check_tree, leaf_margin


class OmissionTreeTests(unittest.TestCase):
    def test_compaction_preserves_a_strict_certificate(self):
        from omission_tree_compact import compact_leaf
        rows = [([0, 1], 1), ([1, 2], 1), ([0, 2], 1)]
        original = {"type": "weighted", "capacity": 2_000_000,
                    "weights": [[0, 1_000_000], [1, 1_000_000], [2, 1_000_000]]}
        result = compact_leaf(3, rows, 1, set(), set(), original)
        self.assertLess(result["capacity"], original["capacity"])
        self.assertTrue(check_tree(3, rows, 1, [result], 0)["complete"])
        with self.assertRaises(ValueError):
            compact_leaf(3, rows, 2, set(), set(), original)

    def test_every_small_leaf_against_assignments(self):
        n = 3
        rows = [([0, 1], 1), ([1, 2], 2), ([0, 2], 1)]
        for states in product((-1, 0, 1), repeat=n):
            missing = {i for i, x in enumerate(states) if x == 1}
            occupied = {i for i, x in enumerate(states) if x == 0}
            assignments = [[i for i, x in enumerate(bits) if x] for bits in product((0, 1), repeat=n)
                           if all(x == -1 or x == bits[i] for i, x in enumerate(states))]
            for weights in product(range(3), repeat=len(rows)):
                for capacity in range(3):
                    node = {"capacity": capacity, "weights": [[r, w] for r, w in enumerate(weights)]}
                    for budget in range(n + 1):
                        if leaf_margin(n, rows, budget, missing, occupied, node) > 0:
                            self.assertFalse(any(valid_holes(n, rows, budget, h) for h in assignments))

    def test_tree_coverage_and_corruptions(self):
        # Both singletons must be missing, which contradicts budget one.
        rows = [([0], 1), ([1], 1)]
        nodes = [{"type": "branch", "vertex": 0, "zero": 1, "one": 2},
                 {"type": "weighted", "capacity": 0, "weights": [[0, 1]]},
                 {"type": "weighted", "capacity": 1, "weights": [[1, 1]]}]
        self.assertTrue(check_tree(2, rows, 1, nodes, 0)["complete"])
        mutations = []
        for field, value in (("zero", 0), ("one", 1), ("one", 99), ("vertex", 2)):
            bad = copy.deepcopy(nodes)
            bad[0][field] = value
            mutations.append(bad)
        for leaf in ({"type": "weighted", "capacity": 1, "weights": [[1, 0]]},
                     {"type": "weighted", "capacity": 1, "weights": [[1, -1]]},
                     {"type": "weighted", "capacity": 1, "weights": [[1, 1], [1, 1]]},
                     {"type": "pending"}, {"type": "over_budget"}):
            bad = copy.deepcopy(nodes)
            bad[2] = leaf
            mutations.append(bad)
        mutations.append(nodes + [{"type": "over_budget"}])
        for bad in mutations:
            with self.assertRaises(ValueError):
                check_tree(2, rows, 1, bad, 0)
        incomplete = copy.deepcopy(nodes)
        incomplete[2] = {"type": "pending"}
        report = check_tree(2, rows, 1, incomplete, 0, allow_pending=True)
        self.assertFalse(report["complete"])
        self.assertEqual(report["pending"], 1)


@unittest.skipUnless(importlib.util.find_spec("highspy"), "optional HiGHS dependency")
class OmissionTreeSearchTests(unittest.TestCase):
    def test_branching_and_resume(self):
        from omission_tree_search import run
        rows = [(list(edge), 1) for edge in combinations(range(4), 2)]
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "source.json"
            source.write_text(json.dumps({"states": [None] * 4, "constraints": [
                {"support": support, "rhs": demand} for support, demand in rows],
                "nodes": [{"type": "pending"}], "root": 0, "hole_budget": 1}))
            first = run(source, folder / "first.json", seconds=5, max_nodes=1)
            self.assertEqual(first["status"], "unknown")
            self.assertGreater(first["checked"]["pending"], 0)
            second = run(source, folder / "second.json", seconds=5, seed_tree=folder / "first.json")
            self.assertEqual(second["status"], "unsat")
            self.assertTrue(check_tree(4, rows, 2, second["nodes"], second["root"])["complete"])
            self.assertFalse(any(valid_holes(4, rows, 2, list(h)) for h in combinations(range(4), 2)))
            third = run(source, folder / "sat.json", budget=3, seconds=5)
            self.assertEqual(third["status"], "sat")
            self.assertTrue(valid_holes(4, rows, 3, third["holes"]))


if __name__ == "__main__":
    unittest.main()
