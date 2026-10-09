"""The rows-only export must retain every row and remove arithmetic imports."""
import json
from pathlib import Path
import tempfile
import unittest

from omission_balanced_rows import export, run
from check_omission_global import digest


class BalancedRowsOnlyTests(unittest.TestCase):
    def fixture(self, directory):
        directory.mkdir()
        (directory / "Geometry00000.lean").write_text("import BalancedProof.Catalog\n")
        (directory / "BalancedOccupancy.lean").write_text("import BalancedProof.Root\n")
        (directory / "BalancedGeometry.lean").write_text(
            "import BalancedProof.Root\nimport BalancedOccupancy\nimport Geometry00000\n"
            "namespace OmissionBalanced\n"
            "theorem all_geometric_rows : True := True.intro\n"
            "theorem real_configuration_bound : True := True.intro\n"
            "end OmissionBalanced\n")
        manifest = {"arithmetic_prefix": "BalancedProof",
                    "modules": [{"module": "Geometry00000", "start": 0, "end": 2685}],
                    "files": {p.name: digest(p) for p in directory.glob("*.lean")}}
        (directory / "export.json").write_text(json.dumps(manifest))

    def test_preserves_all_row_modules_and_drops_population(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            self.fixture(folder / "original")
            result = export(folder / "original", folder / "rows")
            self.assertEqual(result["rows"], 2685)
            self.assertEqual((folder / "rows/Geometry00000.lean").read_bytes(),
                             (folder / "original/Geometry00000.lean").read_bytes())
            aggregate = (folder / "rows/BalancedRows.lean").read_text()
            self.assertIn("theorem all_geometric_rows", aggregate)
            for forbidden in ["import BalancedProof.Root", "import BalancedOccupancy",
                              "real_configuration_bound"]:
                self.assertNotIn(forbidden, aggregate)

    def test_rejects_changed_parent_and_incomplete_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            self.fixture(folder / "original")
            export(folder / "original", folder / "rows")
            p = folder / "rows/export.json"
            m = json.loads(p.read_text())
            m["modules"][0]["start"] = 1
            p.write_text(json.dumps(m))
            with self.assertRaisesRegex(ValueError, "discontinuous"):
                run(folder / "rows", folder / "unused")
            (folder / "original/Geometry00000.lean").write_text("changed")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                export(folder / "original", folder / "altered")


if __name__ == "__main__":
    unittest.main()
