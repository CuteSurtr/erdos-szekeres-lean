"""Trust-boundary controls for actual Lean axiom-report forms."""
import unittest

from check_axioms import audit_output


class AxiomAuditTests(unittest.TestCase):
    def test_standard_and_axiom_free_reports(self):
        self.assertEqual(audit_output("'X' does not depend on any axioms\n", "X"), [])
        self.assertEqual(audit_output("'X' depends on axioms: []\n", "X"), [])
        self.assertEqual(audit_output("'X' depends on axioms: [propext, Quot.sound]\n", "X"),
                         ["Quot.sound", "propext"])

    def test_rejects_missing_wrong_malformed_and_duplicate_reports(self):
        for output in ["", "'Y' does not depend on any axioms",
                       "'X' depends on axioms: [propext] ignored trailer",
                       "'X' does not depend on any axioms\n'X' depends on axioms: []\n"]:
            with self.subTest(output=output), self.assertRaises(ValueError):
                audit_output(output, "X")

    def test_rejects_nonstandard_axioms(self):
        for axiom in ["sorryAx", "Lean.ofReduceBool", "unproved_geometry"]:
            with self.subTest(axiom=axiom), self.assertRaises(ValueError):
                audit_output(f"'X' depends on axioms: [propext, {axiom}]\n", "X")


if __name__ == '__main__':
    unittest.main()
