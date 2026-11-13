"""Independent acceptance and corruption controls for rounded cover cuts."""
import copy
import unittest

from check_omission_cover_cuts import check


class CoverFixture:
    def setUp(self):
        self.source = {"states": [None] * 3, "constraints": [
            {"support": [0, 1], "rhs": 1},
            {"support": [1, 2], "rhs": 1},
            {"support": [0, 2], "rhs": 1}]}
        self.certificate = {"base_rows": 3, "proofs": [
            {"row": 3, "support": [0, 1, 2], "rhs": 2, "capacity": 2,
             "weights": [[0, 1], [1, 1], [2, 1]], "parents": [0, 1, 2],
             "exact_margin": 1},
            {"row": 4, "support": [0, 1, 2], "rhs": 2, "capacity": 1,
             "weights": [[3, 1]], "parents": [3], "exact_margin": 1}]}


class CoverCutTests(CoverFixture, unittest.TestCase):
    def test_valid_odd_cover_and_dependent_cut(self):
        result = check(self.source, self.certificate)
        self.assertEqual(result["derived_rows"], 2)
        self.assertEqual(result["maximum_derivation_depth"], 2)
        self.assertEqual(result["minimum_margin"], 1)

    def test_reject_corrupted_certificates(self):
        for label, mutation in [
            ("future parent", lambda c: c["proofs"][0].update(
                weights=[[4, 1]], parents=[4])),
            ("excess demand", lambda c: c["proofs"][0].update(rhs=3)),
            ("missing support state", lambda c: c["proofs"][0].update(support=[0, 1])),
            ("negative weight", lambda c: c["proofs"][0].update(
                weights=[[0, -1]], parents=[0])),
            ("boolean capacity", lambda c: c["proofs"][0].update(capacity=True)),
            ("duplicate parent", lambda c: c["proofs"][0].update(
                weights=[[0, 1], [0, 1]], parents=[0, 0])),
            ("wrong source size", lambda c: c.update(base_rows=4)),
            ("false recorded margin", lambda c: c["proofs"][0].update(exact_margin=2)),
            ("noninteger recorded margin", lambda c: c["proofs"][0].update(exact_margin=1.0)),
        ]:
            with self.subTest(label=label):
                corrupted = copy.deepcopy(self.certificate)
                mutation(corrupted)
                with self.assertRaises(ValueError):
                    check(self.source, corrupted)


class CoverExportTests(CoverFixture, unittest.TestCase):
    def test_preserve_original_row_order_and_metadata(self):
        from omission_cover_export import augmented_data
        source = copy.deepcopy(self.source)
        source["constraints"][0]["provenance"] = "original first row"
        result = augmented_data(source, self.certificate, "residual", "source", "proof")
        self.assertEqual(result["constraints"][:3], source["constraints"])
        self.assertEqual([row["support"] for row in result["constraints"][3:]],
                         [[0, 1, 2], [0, 1, 2]])
        self.assertEqual([row["rhs"] for row in result["constraints"]], [1, 1, 1, 2, 2])

    def test_export_refuses_overwrite_and_binds_inputs(self):
        import hashlib
        import json
        from pathlib import Path
        import tempfile
        from unittest.mock import patch
        from omission_cover_export import FAMILIES, export
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, certificate, output = root / "original.json", root / "cuts.json", root / "out"
            source.write_text(json.dumps(self.source))
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            cuts = copy.deepcopy(self.certificate)
            cuts["source_sha256"] = source_hash
            certificate.write_text(json.dumps(cuts))
            with patch.dict(FAMILIES["residual"], source_sha256=source_hash):
                manifest = export(source, certificate, output, "residual")
                self.assertEqual(manifest["source_sha256"], source_hash)
                self.assertFalse(manifest["lean_checked"])
                lean = (output / "ResidualCoverCuts.lean").read_text()
                self.assertIn("(by decide +kernel)", lean)
                self.assertIn("(fun i => Fin.elim0 i)", lean)
                self.assertNotIn("native_decide", lean)
                frozen = {p.name: p.read_bytes() for p in output.iterdir()}
                with self.assertRaises(FileExistsError):
                    export(source, certificate, output, "residual")
                self.assertEqual(frozen, {p.name: p.read_bytes() for p in output.iterdir()})
                with self.assertRaises(ValueError):
                    export(source, certificate, root / "invalid-name", "residual", "bad/name")
                self.assertFalse((root / "invalid-name").exists())
                renamed = export(source, certificate, root / "renamed", "residual", "SeparateCuts")
                self.assertEqual(renamed["module"], "SeparateCuts")
                self.assertIn("namespace SeparateCuts", (root / "renamed/SeparateCuts.lean").read_text())
                cuts["proofs"][0]["rhs"] = 3
                certificate.write_text(json.dumps(cuts))
                with self.assertRaises(ValueError):
                    export(source, certificate, root / "corrupt", "residual")
                self.assertFalse((root / "corrupt").exists())
                source.write_text(source.read_text() + " ")
                with self.assertRaises(ValueError):
                    export(source, certificate, root / "changed", "residual")
                self.assertFalse((root / "changed").exists())


if __name__ == "__main__":
    unittest.main()
