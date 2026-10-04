"""Check rejection of bad SAT assignments and replay a realized geometric witness."""
import json
from pathlib import Path
import tempfile
import unittest

from realize_model import check_cnf, read_model
from search import convex_subset, general_position


class CertificateTests(unittest.TestCase):
    def test_assignment_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            cnf = Path(folder) / "instance.cnf"
            cnf.write_text("p cnf 2 2\n1 2 0\n-1 0\n")
            self.assertEqual(check_cnf(cnf, {1: False, 2: True}), 2)
            for bad in ({1: True, 2: True}, {1: False, 2: False}, {1: False}):
                with self.assertRaises(ValueError):
                    check_cnf(cnf, bad)
            cnf.write_text("p cnf 2 3\n1 2 0\n-1 0\n")
            with self.assertRaises(ValueError):
                check_cnf(cnf, {1: False, 2: True})

    def test_wrapped_model(self):
        with tempfile.TemporaryDirectory() as folder:
            model = Path(folder) / "solver.log"
            model.write_text("c log\ns SATISFIABLE\nv -1 2\nv -3 0\n")
            self.assertEqual(read_model(model), {1: False, 2: True, 3: False})

    def test_saved_integer_witness(self):
        path = Path(__file__).resolve().parents[1] / "experiments/gon5-n8-realization.json"
        result = json.loads(path.read_text())
        points = [tuple(p) for p in result["coordinates"]]
        self.assertEqual(len(points), 8)
        self.assertTrue(general_position(points))
        self.assertIsNone(convex_subset(points, 5))


if __name__ == "__main__":
    unittest.main()
