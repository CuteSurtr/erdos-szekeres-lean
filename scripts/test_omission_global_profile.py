"""Failure controls for exact version selection in cover assembly profiles."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from check_omission_global import digest
from check_omission_global_profile import read_profile, verify_cover_profile


class CoverProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.profile = {"version": 1, "bound": 315, "final_module": "FinalCover315B61R30"}
        for side, states, rows, cuts, budget in [("balanced", 252, 2685, 446, 61),
                                                ("residual", 154, 1187, 402, 30)]:
            self.profile[side] = {"states": states, "original_rows": rows,
                "derived_rows": cuts, "rows": rows + cuts, "budget": budget,
                "namespace": side.capitalize() + "Cover", "module_prefix": side.capitalize() + "Proof",
                "cut_module": side.capitalize() + "Cuts", "cut_namespace": side.capitalize() + "Cuts",
                "bridge": side.capitalize() + "Bridge", "arithmetic_manifest_sha256": "a" * 64,
                "cut_manifest_sha256": "b" * 64, "augmented_source_sha256": "c" * 64}
        self.path = self.root / "profile.json"

    def read(self):
        self.path.write_text(json.dumps(self.profile))
        return read_profile(self.path)

    def test_accepts_b61_v2_r30_v1_dimensions(self):
        self.assertEqual(self.read()["bound"], 315)

    def test_rejects_wrong_bound_or_original_geometry(self):
        self.profile["bound"] = 314
        with self.assertRaisesRegex(ValueError, "threshold disagree"):
            self.read()
        self.profile["bound"] = 315
        self.profile["balanced"]["original_rows"] = 2684
        with self.assertRaisesRegex(ValueError, "original geometric"):
            self.read()

    def test_rejects_wrong_row_count_or_unpinned_manifest(self):
        self.profile["balanced"]["rows"] = 2905
        with self.assertRaisesRegex(ValueError, "row cardinalities"):
            self.read()
        self.profile["balanced"]["rows"] = 3131
        self.profile["residual"]["arithmetic_manifest_sha256"] = "latest"
        with self.assertRaisesRegex(ValueError, "exact manifest"):
            self.read()

    def test_rejects_module_path_injection(self):
        self.profile["balanced"]["bridge"] = "../ForeignProof"
        with self.assertRaisesRegex(ValueError, "module or namespace"):
            self.read()

    def test_rejects_changed_manifest_and_wrong_extended_source(self):
        item = copy.deepcopy(self.profile["balanced"])
        arithmetic, cuts = self.root / "arithmetic", self.root / "cuts"
        arithmetic.mkdir()
        cuts.mkdir()
        a = {key: item[key] for key in ["namespace", "states", "rows", "budget", "module_prefix"]}
        a["source_sha256"] = item["augmented_source_sha256"]
        c = {key: item[key] for key in ["states", "original_rows", "derived_rows"]}
        c.update(module=item["cut_module"], namespace=item["cut_namespace"],
                 augmented_source_sha256=item["augmented_source_sha256"])
        (arithmetic / "export.json").write_text(json.dumps(a))
        (cuts / "export.json").write_text(json.dumps(c))
        item["arithmetic_manifest_sha256"] = digest(arithmetic / "export.json")
        item["cut_manifest_sha256"] = digest(cuts / "export.json")
        verify_cover_profile(item, arithmetic, cuts, a, c)
        c["augmented_source_sha256"] = "d" * 64
        with self.assertRaisesRegex(ValueError, "different extended row"):
            verify_cover_profile(item, arithmetic, cuts, a, c)
        (arithmetic / "export.json").write_text("a different frozen export")
        with self.assertRaisesRegex(ValueError, "changed proof input"):
            verify_cover_profile(item, arithmetic, cuts, a, c)


if __name__ == "__main__":
    unittest.main()
