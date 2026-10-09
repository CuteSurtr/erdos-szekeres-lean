"""Shape, coverage, and optional kernel controls for fused leaf generation."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest

from check_omission_lean import run, verify_sources
from omission_fused_export import export, fuse_source
from omission_lean_export import export as original_export, sha256
from test_omission_lean_export import control


class FusedExportTests(unittest.TestCase):
    def test_preserves_catalog_data_branch_coverage_and_checker_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, _ = control(folder)
            old = original_export(source, tree, folder / "original", namespace="Example",
                                  module_prefix="Proof", leaf_limit=1)
            new = export(source, tree, folder / "fused", namespace="Example",
                         module_prefix="Proof", leaf_limit=1)
            for key in ["states", "rows", "budget", "base", "root", "full_tree_root",
                        "parts", "contexts", "exported_leaves", "exported_parts"]:
                self.assertEqual(old[key], new[key])
            self.assertEqual(verify_sources(folder / "fused"), new)
            self.assertFalse(new["lean_checked"])
            self.assertEqual(new["fused_weighted_leaves"], 2)
            self.assertEqual((folder / "original/Proof/Root.lean").read_text(),
                             (folder / "fused/Proof/Root.lean").read_text())
            for path in (folder / "fused/Proof").glob("Part*.lean"):
                self.assertNotIn("theorem loads", path.read_text())
                self.assertIn("fused_sparse_packed_excludes", path.read_text())

    def test_rejects_changed_leaf_shape_and_invalid_numeric_certificate(self):
        with self.assertRaisesRegex(ValueError, "partial rewrite"):
            fuse_source("theorem loads1 : True := by trivial\n")
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, data = control(folder)
            data = copy.deepcopy(data)
            data["nodes"][1]["weights"] = [[0, 0]]
            tree.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                export(source, tree, folder / "fused")
            self.assertFalse((folder / "fused").exists())

    def test_subtree_and_over_budget_leaf_keep_their_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, _ = control(folder, over_budget=True)
            report = export(source, tree, folder / "fused", subtree=2)
            self.assertEqual(report["fused_weighted_leaves"], 0)
            self.assertEqual(report["contexts"], {"missing": [0], "occupied": []})
            root = (folder / "fused/Root.lean").read_text()
            self.assertNotIn("theorem excludes_budget", root)
            self.assertIn("CertificateTree.overBudget", (folder / "fused/Part00000.lean").read_text())


@unittest.skipUnless(os.environ.get("ERDOS_LEAN_FUSED_TEST") == "1", "optional Lean control")
class FusedKernelTests(unittest.TestCase):
    def test_full_root_and_corrupted_packed_coefficient(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, _ = control(folder)
            directory = folder / "fused"
            export(source, tree, directory, module_prefix="FusedControl", leaf_limit=1)
            result = run(directory, workers=1, memory=2500)
            self.assertTrue(result["complete"])
            part = directory / "FusedControl/Part00000.lean"
            original = part.read_text()
            mutated = original.replace("cs1 : List ℕ := [1, 0]", "cs1 : List ℕ := [0, 0]")
            self.assertNotEqual(original, mutated)
            part.write_text(mutated)
            manifest = json.loads((directory / "export.json").read_text())
            manifest["files"]["FusedControl/Part00000.lean"] = sha256(part)
            (directory / "export.json").write_text(json.dumps(manifest))
            with self.assertRaises(RuntimeError):
                run(directory, workers=1, memory=2500)
            record = json.loads((directory / "kernel-check.json").read_text())
            self.assertFalse(record["complete"])
            self.assertNotEqual(record["modules"]["Part00000"]["exit"], 0)


if __name__ == "__main__":
    unittest.main()
