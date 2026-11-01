#!/usr/bin/env python3
"""Like lrat_to_lean.py, but packs the clause list, the start clauses and the proof into
natural numbers (see ETVEncoding/Packed.lean), which elaborate instantly.

Usage: lrat_to_packed.py FILE.cnf PROOF.lrat PREFIX
Prints definitions PREFIXCnf, PREFIXStart, PREFIXProof (codes) and PREFIXCnfLen,
PREFIXStartLen, PREFIXProofLen (digit counts, used as fuel)."""
import sys

BASE = 2 ** 20
sys.set_int_max_str_digits(0)


def lit(l):
    return 2 * abs(l) + (1 if l < 0 else 0)


def pack(groups):
    digits = []
    for g in groups:
        for x in g:
            assert x + 2 < BASE
            digits.append(x + 2)
        digits.append(1)
    n = 0
    for d in reversed(digits):
        n = n * BASE + d
    return n, len(digits)


def main():
    cnf_path, proof_path, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
    clauses = []
    with open(cnf_path) as f:
        for line in f:
            if line.startswith("c") or line.startswith("p") or not line.strip():
                continue
            nums = [int(t) for t in line.split()]
            assert nums[-1] == 0
            clauses.append(nums[:-1])
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
            steps.append(([int(tok[0])] + [lit(l) for l in lits], hints))
    cnf_code, cnf_len = pack([[lit(l) for l in c] for c in clauses])
    start_code, start_len = pack([[i] + [lit(l) for l in clauses[i - 1]] for i in sorted(used)])
    proof_groups = []
    for g, h in steps:
        proof_groups.append(g)
        proof_groups.append(h)
    proof_code, proof_len = pack(proof_groups)
    for name, code, n in (("Cnf", cnf_code, cnf_len), ("Start", start_code, start_len),
                          ("Proof", proof_code, proof_len)):
        print("def %s%sLen : ℕ := %d" % (prefix, name, n + 1))
        print("def %s%s : ℕ :=\n  %d\n" % (prefix, name, code))


if __name__ == "__main__":
    main()
