#!/usr/bin/env python3
"""Cross-check construction of the D3 instance: the 3-fold CNF of symcnf.py, unchanged, plus
binary clauses chi(S a, S b, S c) = -chi(a, b, c) for every triple, where S is the label
permutation of the mirror (see d3cnf.py; S(0,r) = (0,-r), S(j,r) = (t-j,-r-1), centre fixed).
This shares only the label rule with d3cnf.py (no D3 orbit canonicalisation of variables,
axioms or convexity flags), so agreement of the two answers checks d3cnf's bookkeeping.
usage: c3refl.py C3.cnf C3.json OUT.cnf
"""
import json
import sys

cnf, mp, outp = sys.argv[1:4]
info = json.load(open(mp))
t, P, c = info["t"], info["P"], info["center_index"]
assert info["m"] == 3 and info["center"] == "aux" and t % 2 == 1


def sigma(i):
    if i == c:
        return i
    o, r = divmod(i, 3)
    if o == 0:
        return (-r) % 3
    return (t - o) * 3 + (-r - 1) % 3


tv = {(a, b, cc): (v, s) for a, b, cc, v, s in info["triples"]}


def parity(x):
    a, b, cc = x
    inv = (a > b) + (a > cc) + (b > cc)
    return -1 if inv & 1 else 1


def lit(a, b, cc):
    x = (a, b, cc)
    srt = tuple(sorted(x))
    v, s = tv[srt]
    return parity(x) * s * v


extra = set()
for (a, b, cc) in tv:
    x = lit(a, b, cc)
    y = lit(sigma(a), sigma(b), sigma(cc))
    # x <-> -y
    if x == -y:
        continue
    if x == y:
        raise SystemExit(f"triple {(a, b, cc)} forced to orientation 0")
    extra.add(tuple(sorted((x, y))))            # x or y
    extra.add(tuple(sorted((-x, -y))))          # not x or not y
with open(cnf) as f, open(outp, "w") as g:
    for line in f:
        if line.startswith("p "):
            _, _, nv, nc = line.split()
            g.write(f"c c3refl: {len(extra)} reflection clauses appended\n")
            g.write(f"p cnf {nv} {int(nc) + len(extra)}\n")
        else:
            g.write(line)
    for a, b in sorted(extra):
        g.write(f"{a} {b} 0\n")
print(json.dumps({"reflection_clauses": len(extra)}))
