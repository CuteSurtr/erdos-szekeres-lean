#!/usr/bin/env python3
"""Reject nonstandard axioms in the principal formalization milestones."""
import argparse
from pathlib import Path
import re
import subprocess


ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def audit_output(output, expected):
    """Require exactly one complete report, including Lean's axiom-free form."""
    pattern = (r"^'" + re.escape(expected) +
               r"' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)\s*$")
    reports = re.findall(pattern, output, re.MULTILINE)
    if len(reports) != 1:
        raise ValueError(f"Expected one axiom report for {expected}; found {len(reports)}")
    axioms = {a.strip() for a in reports[0].split(",") if a.strip()}
    if not axioms <= ALLOWED:
        raise ValueError(f"Nonstandard axioms in {expected}: {sorted(axioms - ALLOWED)}")
    return sorted(axioms)


def check(lake="lake", output=None):
    root = Path(__file__).resolve().parents[1]
    audit = root / "scripts/AxiomAudit.lean"
    expected = re.findall(r"^#print axioms (\S+)$", audit.read_text(), re.MULTILINE)
    result = subprocess.run([lake, "env", "lean", str(audit)], cwd=root,
                            text=True, capture_output=True, check=True)
    for name in expected:
        audit_output(result.stdout, name)
    summary = f"Axiom audit passed for {len(expected)} theorems: only standard Lean axioms."
    if output is not None:
        Path(output).write_text(result.stdout.rstrip() + "\n" + summary + "\n")
    print(summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lake", default="lake")
    parser.add_argument("--output", type=Path, help="Save the verified full axiom report")
    args = parser.parse_args()
    check(args.lake, args.output)
