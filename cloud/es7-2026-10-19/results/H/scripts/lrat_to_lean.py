#!/usr/bin/env python3
"""Turn a DIMACS file and a textual LRAT proof for it (e.g. from
`cadical --lrat --no-binary`) into Lean definitions for the kernel check in
ETVEncoding/EndToEnd.lean:

  def PREFIXCnf   : List (List ℤ)        -- the clauses of the DIMACS file
  def PREFIXStart : List (ℕ × List ℤ)    -- the original clauses the proof uses, with ids
  def PREFIXProof : List Rup.Step        -- the RUP additions (deletions are dropped)

Usage: lrat_to_lean.py FILE.cnf PROOF.lrat PREFIX
Only RUP steps are accepted (no RAT hints)."""
import sys


def read_cnf(path):
    clauses = []
    with open(path) as f:
        for line in f:
            if line.startswith("c") or line.startswith("p") or not line.strip():
                continue
            nums = [int(t) for t in line.split()]
            assert nums[-1] == 0
            clauses.append(nums[:-1])
    return clauses


def lst(xs):
    return "[" + ", ".join(map(str, xs)) + "]"


def main():
    cnf_path, proof_path, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
    clauses = read_cnf(cnf_path)
    m = len(clauses)
    steps, used = [], set()
    with open(proof_path) as f:
        for line in f:
            tok = line.split()
            if not tok or tok[0] == "c" or tok[1] == "d":
                continue
            nums = [int(t) for t in tok[1:]]
            z = nums.index(0)
            lits, hints = nums[:z], nums[z + 1:]
            assert hints and hints[-1] == 0
            hints = hints[:-1]
            if any(h < 0 for h in hints):
                raise SystemExit("RAT step not supported: " + line.strip())
            used.update(h for h in hints if h <= m)
            steps.append(".add %s %s %s" % (tok[0], lst(lits), lst(hints)))
    print("set_option maxHeartbeats 0 in")
    print("def %sCnf : List (List ℤ) := [" % prefix)
    print(",\n".join("  " + lst(c) for c in clauses))
    print("]\n")
    print("set_option maxHeartbeats 0 in")
    print("def %sStart : List (ℕ × List ℤ) := [" % prefix)
    print(",\n".join("  (%d, %s)" % (i, lst(clauses[i - 1])) for i in sorted(used)))
    print("]\n")
    print("set_option maxHeartbeats 0 in")
    print("def %sProof : List Rup.Step := [" % prefix)
    print(",\n".join("  " + s for s in steps))
    print("]")


if __name__ == "__main__":
    main()
