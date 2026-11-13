"""Failure controls for the final proof assembly's prerequisite gate."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from check_omission_global import (digest, verify_complete_family, verify_dependency,
                                   verify_snapshot, verify_import_layout, run)


class GlobalAssemblyGateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name).resolve()
        self.directory = self.repo / "family"
        self.directory.mkdir()
        self.source = self.directory / "Root.lean"
        self.obj = self.directory / "Root.olean"
        self.input = self.repo / "Prerequisite.olean"
        self.source.write_text("#print axioms Example.complete\n")
        self.obj.write_bytes(b"unit-test object fixture, never loaded by Lean")
        self.input.write_bytes(b"unit-test dependency fixture")
        self.manifest = {"files": {"Root.lean": digest(self.source)}}
        self.save_manifest()
        self.binding = {"manifest": digest(self.directory / "export.json"),
                        "lean": "test Lean version", "inputs": {str(self.input): digest(self.input)}}
        self.record = {"exit": 0, "audited": True, "source_sha256": digest(self.source),
                       "olean_sha256": digest(self.obj), "axioms": ["propext"],
                       "stdout": "'Example.complete' depends on axioms: [propext]\n"}
        self.report = {"complete": True, "binding": self.binding,
                       "fingerprint": self.fingerprint(), "modules": {"Root": self.record}}
        self.save_report()

    def fingerprint(self):
        return hashlib.sha256(json.dumps(self.binding, sort_keys=True).encode()).hexdigest()

    def save_manifest(self):
        (self.directory / "export.json").write_text(json.dumps(self.manifest))

    def save_report(self):
        (self.directory / "kernel-check.json").write_text(json.dumps(self.report))

    def verify(self):
        return verify_complete_family(self.directory, self.repo, "test Lean version")

    def test_accepts_complete_binding_and_rejects_later_mutation(self):
        _, snapshot = self.verify()
        verify_snapshot(snapshot)
        self.obj.write_bytes(b"changed after prerequisite validation")
        with self.assertRaisesRegex(ValueError, "changed proof input"):
            verify_snapshot(snapshot)

    def test_rejects_incomplete_family(self):
        self.report["complete"] = False
        self.save_report()
        with self.assertRaisesRegex(ValueError, "Incomplete prerequisite"):
            self.verify()

    def test_rejects_changed_source_object_or_input(self):
        for path in [self.source, self.obj, self.input]:
            with self.subTest(path=path.name):
                original = path.read_bytes()
                path.write_bytes(original + b" changed")
                with self.assertRaisesRegex(ValueError, "changed proof input"):
                    self.verify()
                path.write_bytes(original)

    def test_rejects_nonstandard_axiom_even_with_matching_record(self):
        self.record["stdout"] = "'Example.complete' depends on axioms: [sorryAx]\n"
        self.record["axioms"] = ["sorryAx"]
        self.save_report()
        with self.assertRaisesRegex(ValueError, "Nonstandard axioms"):
            self.verify()

    def test_rejects_missing_module_record(self):
        self.report["modules"] = {}
        self.save_report()
        with self.assertRaisesRegex(ValueError, "Unchecked prerequisite"):
            self.verify()

    def test_rejects_fingerprint_and_version_mismatch(self):
        with self.assertRaisesRegex(ValueError, "Toolchain mismatch"):
            verify_complete_family(self.directory, self.repo, "different Lean")
        self.report["fingerprint"] = "0" * 64
        self.save_report()
        with self.assertRaisesRegex(ValueError, "Invalid binding fingerprint"):
            self.verify()

    def test_requires_the_selected_dependency(self):
        verify_dependency(self.directory, self.input)
        other = self.repo / "Other.olean"
        other.write_bytes(self.input.read_bytes())
        with self.assertRaisesRegex(ValueError, "selected dependency"):
            verify_dependency(self.directory, other)

    def test_rejects_unlisted_import_shadow(self):
        shadow = self.directory / "Residual124" / "Catalog.olean"
        shadow.parent.mkdir()
        shadow.write_bytes(b"unlisted shadow object")
        with self.assertRaisesRegex(ValueError, "shadow checked imports"):
            verify_import_layout(self.directory)

    def test_rejects_cover_budget_threshold_mismatch_before_building(self):
        with self.assertRaisesRegex(ValueError, "budgets and requested global threshold"):
            run(self.repo / "unused-output", "unused", "unused", "unused",
                bound=317, balanced_cover_budget=60, residual_cover_budget=30,
                residual_cover_arithmetic="unused", residual_cover_cuts="unused",
                balanced_cover_arithmetic="unused", balanced_cover_cuts="unused")
        self.assertFalse((self.repo / "unused-output").exists())


if __name__ == "__main__":
    unittest.main()
