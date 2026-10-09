"""Exporter boundaries and optional end-to-end Lean controls.

Run integration controls under lake env with ERDOS_LEAN_EXPORT_TEST=1.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from check_omission_lean import audit_output, run, verify_sources
from omission_lean_export import export, normalize_leaf, sha256


def control(folder, over_budget=False):
    source, tree = folder / "source.json", folder / "tree.json"
    source.write_text(json.dumps({"states": [None, None], "constraints": [
        {"support": [0], "rhs": 1}, {"support": [1], "rhs": 1}]}))
    nodes = [{"type": "branch", "vertex": 0, "zero": 1, "one": 2},
             {"type": "weighted", "capacity": 0, "weights": [[0, 1]]},
             {"type": "over_budget"} if over_budget else
             {"type": "weighted", "capacity": 1, "weights": [[1, 1]]}]
    data = {"source_sha256": sha256(source), "hole_budget": 0 if over_budget else 1,
            "nodes": nodes, "root": 0}
    tree.write_text(json.dumps(data))
    return source, tree, data


class OmissionLeanExportTests(unittest.TestCase):
    def test_branches_partition_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, _ = control(folder)
            out = folder / "export"
            report = export(source, tree, out, leaf_limit=1)
            self.assertEqual(report["exported_parts"], 2)
            self.assertEqual(report["exported_leaves"], 2)
            self.assertFalse(report["lean_checked"])
            self.assertEqual(verify_sources(out), report)
            part = out / "Part00000.lean"
            part.write_text(part.read_text().replace("cs1 : List ℕ := [1, 0]",
                                                      "cs1 : List ℕ := [0, 0]"))
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                verify_sources(out)

    def test_rejects_corrupt_certificate_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, data = control(folder)
            mutations = [dict(data, source_sha256="wrong"), copy.deepcopy(data),
                         copy.deepcopy(data)]
            mutations[1]["nodes"][0]["one"] = 1
            mutations[2]["nodes"][1]["weights"] = [[0, 0]]
            for bad in mutations:
                tree.write_text(json.dumps(bad))
                out = folder / "export"
                with self.assertRaises(ValueError):
                    export(source, tree, out)
                self.assertFalse(out.exists())

    def test_subtree_retains_context_and_has_no_global_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, _ = control(folder)
            report = export(source, tree, folder / "export", subtree=1)
            self.assertEqual(report["contexts"], {"missing": [], "occupied": [0]})
            self.assertNotIn("theorem excludes_budget", (folder / "export/Root.lean").read_text())

    def test_normalization_discards_satisfied_rows(self):
        rows = [([0], 1), ([0, 1], 2), ([2], 1)]
        entries, columns = normalize_leaf(3, rows, {
            "weights": [[0, 50], [1, 3], [2, 0]]}, [0])
        self.assertEqual(entries, [(1, 3)])
        self.assertEqual(columns, [3, 3, 0])

    def test_axiom_audit_rejects_missing_and_nonstandard(self):
        self.assertEqual(audit_output("'Example.root' depends on axioms: [propext]",
                                      "Example.root"), ["propext"])
        for text in ["", "'Example.other' depends on axioms: []",
                     "'Example.root' depends on axioms: [propext, sorryAx]",
                     "'Example.root' depends on axioms: [customAssumption]"]:
            with self.assertRaises(ValueError):
                audit_output(text, "Example.root")


@unittest.skipUnless(os.environ.get("ERDOS_LEAN_EXPORT_TEST") == "1",
                     "optional Lean exporter integration controls")
class OmissionLeanIntegrationTests(unittest.TestCase):
    def test_prefixed_trees_link_without_module_collisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, _ = control(folder)
            paths = []
            for prefix in ("FirstProof", "SecondProof"):
                out = folder / prefix
                export(source, tree, out, namespace=prefix, leaf_limit=1,
                       module_prefix=prefix)
                self.assertTrue(run(out)["complete"])
                paths.append(str(out))
            combined = folder / "Combined.lean"
            combined.write_text("import FirstProof.Root\nimport SecondProof.Root\n"
                                "#print axioms FirstProof.excludes_budget\n"
                                "#print axioms SecondProof.excludes_budget\n")
            env = dict(os.environ)
            env["LEAN_PATH"] = os.pathsep.join([*paths, env.get("LEAN_PATH", "")])
            result = subprocess.run(["lean", str(combined)], env=env,
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for prefix in ("FirstProof", "SecondProof"):
                audit_output(result.stdout, prefix + ".excludes_budget")

    def test_weighted_and_overbudget_trees_compile(self):
        for over_budget in (False, True):
            with self.subTest(over_budget=over_budget), tempfile.TemporaryDirectory() as tmp:
                folder = Path(tmp)
                source, tree, _ = control(folder, over_budget)
                out = folder / "export"
                export(source, tree, out, leaf_limit=1)
                self.assertTrue(run(out)["complete"])
                self.assertTrue(run(out, resume=True)["complete"])

    def test_corrupted_column_is_rejected_by_lean(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, tree, _ = control(folder)
            out = folder / "export"
            report = export(source, tree, out, leaf_limit=1)
            part = out / "Part00000.lean"
            original = part.read_text()
            corrupted = original.replace("cs1 : List ℕ := [1, 0]", "cs1 : List ℕ := [0, 0]")
            self.assertNotEqual(original, corrupted)
            part.write_text(corrupted)
            # Even a corrupt generator that updates its manifest cannot bypass Lean.
            report["files"][part.name] = sha256(part)
            (out / "export.json").write_text(json.dumps(report))
            with self.assertRaisesRegex(RuntimeError, "Kernel check failed"):
                run(out)
            record = json.loads((out / "kernel-check.json").read_text())
            self.assertFalse(record["complete"])
            self.assertFalse(record["modules"]["Part00000"]["audited"])
