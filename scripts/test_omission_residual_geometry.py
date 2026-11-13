"""Check literal catalog alignment and reject incomplete/tampered exports."""
import gzip
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from check_omission_residual_geometry import verify_sources
from omission_geometry_export import cycles_from_source, digest

ROOT = Path(__file__).resolve().parents[1]


class OmissionResidualGeometryTests(unittest.TestCase):
    def test_literal_state_order_matches_arithmetic_source(self):
        source = ROOT / "experiments/omission-residual-geometry-2026-10-09/row-source.json.gz"
        data = json.loads(gzip.decompress(source.read_bytes()))
        lean = (ROOT / "ErdosSzekeres/Omission/ResidualCatalogData.lean").read_text()
        literal = re.search(r"^def catalog : List \(List Nat\) := (.+)$", lean, re.MULTILINE)[1]
        self.assertEqual(json.loads(literal), data["states"])

    def test_cycle_parser_does_not_read_box_data_or_accept_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "cycles.lean"
            p.write_text('def boxes := "9 8 7"\ndef cycles := "0 1 2\\n3 4 5"')
            self.assertEqual(cycles_from_source(p), [[0, 1, 2], [3, 4, 5]])
            p.write_text('def cycles := "0 1; code"')
            with self.assertRaises(ValueError):
                cycles_from_source(p)

    def test_geometry_manifest_rejects_source_tampering_and_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in ["ResidualGeometry00000.lean", "ResidualGeometry.lean", "ResidualCycleIndex.lean"]:
                (folder / name).write_text("-- test input\n")
            manifest = {"rows": 1164, "total_rows": 1187, "excluded_rows": [973, *range(1165, 1187)], "modules": [{"module": "ResidualGeometry00000", "start": 0, "end": 1164}],
                        "files": {p.name: digest(p) for p in folder.glob("*.lean")}}
            path = folder / "export.json"
            path.write_text(json.dumps(manifest))
            verify_sources(folder)
            manifest["modules"][0]["start"] = 1
            path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                verify_sources(folder)
            manifest["modules"][0]["start"] = 0
            path.write_text(json.dumps(manifest))
            (folder / "ResidualGeometry00000.lean").write_text("-- changed\n")
            with self.assertRaises(ValueError):
                verify_sources(folder)

    @unittest.skipUnless(os.environ.get("ERDOS_LEAN_EXPORT_TEST") == "1",
                         "Run under lake env with ERDOS_LEAN_EXPORT_TEST=1")
    def test_lean_accepts_cycle_and_rejects_corrupted_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "CycleControl.lean"
            prefix = ("import ErdosSzekeres.Omission.ResidualCycleGeometry\n"
                      "open ErdosSzekeres.Omission\n"
                      "set_option maxRecDepth 100000\n")
            p.write_text(prefix + "example : ResidualCycleValid [0, 4, 8, 14, 23, 33, 25, 17] := by decide +kernel\n")
            good = subprocess.run(["lean", str(p)], cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
            p.write_text(prefix + "example : ResidualCycleValid [0, 8, 4, 14, 23, 33, 25, 17] := by decide +kernel\n")
            bad = subprocess.run(["lean", str(p)], cwd=ROOT, text=True, capture_output=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("Tactic `decide` proved that the proposition", bad.stdout + bad.stderr)
            self.assertIn("is false", bad.stdout + bad.stderr)


if __name__ == '__main__':
    unittest.main()
