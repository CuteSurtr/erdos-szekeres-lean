#!/usr/bin/env python3
"""Minimal, separately written clause check: does a full assignment satisfy every clause of a DIMACS CNF?

usage: python3 -I satcheck.py CNF ASSIGN [ASSIGN ...]
ASSIGN holds one literal per variable 1..nv ("v" or "-v"), terminated by 0.  Prints one JSON line per assignment
with the number of clauses that contain no true literal.  It shares no code with k8exact.py or k8exact_a.py.
Exit status 1 if any assignment leaves a clause unsatisfied (or if no assignment is given), else 0.
"""
import hashlib
import json
import sys


def main():
    cnf, assigns = sys.argv[1], sys.argv[2:]
    assert assigns, 'no assignment files given'
    failed = 0
    data = open(cnf, 'rb').read()
    lines = data.split(b'\n')
    p, kind, nv, ncl = lines[0].split()
    nv, ncl = int(nv), int(ncl)
    clauses = [list(map(int, ln.split())) for ln in lines[1:] if ln.strip()]
    assert len(clauses) == ncl and all(c[-1] == 0 for c in clauses)
    for fn in assigns:
        lits = list(map(int, open(fn).read().split()))
        assert lits[-1] == 0
        lits = lits[:-1]
        assert sorted(abs(l) for l in lits) == list(range(1, nv + 1)), 'not one literal per variable'
        true = bytearray(2 * nv + 2)                 # index nv + l is 1 iff literal l is true
        for l in lits:
            true[nv + l] = 1
        unsat = sum(1 for c in clauses if not any(true[nv + l] for l in c[:-1]))
        print(json.dumps({'cnf_sha256': hashlib.sha256(data).hexdigest(), 'assignment': fn.rsplit('/', 1)[-1],
                          'variables': nv, 'clauses': ncl, 'true_literals': sum(1 for l in lits if l > 0),
                          'unsatisfied_clauses': unsat}), flush=True)
        failed += unsat > 0
    sys.exit(1 if failed else 0)


main()
