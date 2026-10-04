#!/usr/bin/env python3
"""Reject nonstandard axioms in the principal formalization milestones."""
import argparse
from pathlib import Path
import re
import subprocess


def check(lake="lake"):
    root = Path(__file__).resolve().parents[1]
    audit = root / "scripts/AxiomAudit.lean"
    expected = re.findall(r"^#print axioms (\S+)$", audit.read_text(), re.MULTILINE)
    result = subprocess.run([lake, "env", "lean", str(audit)], cwd=root,
                            text=True, capture_output=True, check=True)
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    for name in expected:
        found = re.search(r"'" + re.escape(name) + r"' depends on axioms: \[([^]]*)\]", result.stdout)
        if found is None:
            raise RuntimeError(f"Missing axiom report for {name}: {result.stdout}")
        axioms = {x.strip() for x in found.group(1).split(",") if x.strip()}
        if not axioms <= allowed:
            raise RuntimeError(f"Nonstandard axioms in {name}: {axioms - allowed}")
    print(f"Axiom audit passed for {len(expected)} theorems: only standard Lean axioms.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lake", default="lake")
    check(parser.parse_args().lake)
