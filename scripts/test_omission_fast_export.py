"""Shape, coverage, and optional kernel controls for packed-lookup leaf generation."""
import json
import os
from pathlib import Path
import tempfile
import unittest

from check_omission_lean import run, verify_sources
from omission_fast_export import export, fast_source, lookup_source
from omission_fused_export import export as fused_export
from omission_lean_export import sha256
from test_omission_lean_export import control


class FastExportTests(unittest.TestCase):
    def test_preserves_statements_branches_and_checker_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, _ = control(folder)
            old = fused_export(source, tree, folder / "fused", namespace="Example",
                               module_prefix="Proof", leaf_limit=1)
            new = export(source, tree, folder / "fast", namespace="Example",
                         module_prefix="Proof", leaf_limit=1)
            for key in ["states", "rows", "budget", "base", "root", "full_tree_root",
                        "parts", "contexts", "exported_leaves", "exported_parts"]:
                self.assertEqual(old[key], new[key])
            self.assertEqual(verify_sources(folder / "fast"), new)
            self.assertEqual(new["fast_weighted_leaves"], 2)
            self.assertEqual((folder / "fused/Proof/Root.lean").read_text(),
                             (folder / "fast/Proof/Root.lean").read_text())
            for path in (folder / "fast/Proof").glob("Part*.lean"):
                fast, fused = path.read_text(), (folder / "fused/Proof" / path.name).read_text()
                self.assertNotIn("fused_sparse_packed_excludes", fast)
                self.assertIn("fused_fast_excludes", fast)
                statement = lambda text: [line for line in text.splitlines()
                                          if not line.startswith("  ")]
                self.assertEqual(statement(fast), statement(fused))

    def test_rejects_changed_leaf_shape_and_unpackable_base(self):
        with self.assertRaisesRegex(ValueError, "partial rewrite"):
            fast_source("  apply fused_sparse_packed_excludes base cs1 support demand code\n")
        with self.assertRaisesRegex(ValueError, "power of two"):
            lookup_source([([0], 1)], 1, 6)

    def test_packed_slots_hold_every_code(self):
        rows = [([0, 2], 1), ([1], 2), ([0, 1, 2], 3)]
        text = lookup_source(rows, 3, 4)
        self.assertIn("6-bit slots", text)
        self.assertIn("theorem fastCode_eq", text)


@unittest.skipUnless(os.environ.get("ERDOS_LEAN_FAST_TEST") == "1", "optional Lean control")
class FastKernelTests(unittest.TestCase):
    def test_full_root_and_corrupted_packed_coefficient(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, _ = control(folder)
            directory = folder / "fast"
            export(source, tree, directory, module_prefix="FastControl", leaf_limit=1)
            result = run(directory, workers=1, memory=2500)
            self.assertTrue(result["complete"])
            part = directory / "FastControl/Part00000.lean"
            original = part.read_text()
            mutated = original.replace("cs1 : List ℕ := [1, 0]", "cs1 : List ℕ := [0, 0]")
            self.assertNotEqual(original, mutated)
            part.write_text(mutated)
            manifest = json.loads((directory / "export.json").read_text())
            manifest["files"]["FastControl/Part00000.lean"] = sha256(part)
            (directory / "export.json").write_text(json.dumps(manifest))
            with self.assertRaises(RuntimeError):
                run(directory, workers=1, memory=2500)
            record = json.loads((directory / "kernel-check.json").read_text())
            self.assertFalse(record["complete"])
            self.assertNotEqual(record["modules"]["Part00000"]["exit"], 0)


if __name__ == "__main__":
    unittest.main()
