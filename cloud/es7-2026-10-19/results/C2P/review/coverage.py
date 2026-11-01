#!/usr/bin/env python3
"""Coverage of the C2P work list under the reflection pairing (my own orbit computation):
for a = 1..8 every orbit {V, (a - V) mod 17} of the 560 subcases must have a member that is in lists/C2P.tsv, or
certified by both checkers in C2C34/logs/p8_units.tsv; each case needs its cover (P8: certified in the pilot).
Also compares orbits/P<a>.tsv with my orbits and checks the canonical case lists of C2C34/canonical.txt."""
import os
import csv, itertools, sys
C = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")  # results/C2P
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")  # results
T = 17
nm = lambda a, V: f"P{a}_" + "-".join(map(str, sorted(V)))
rows = list(csv.DictReader(open(f"{C}/lists/C2P.tsv"), delimiter="\t"))
listed = {r["unit"] for r in rows}
assert len(rows) == len(listed), "duplicate units in list"
p8 = list(csv.DictReader(open(f"{R}/C2C34/logs/p8_units.tsv"), delimiter="\t"))
cert8 = {r["unit"] for r in p8 if r["status"] == "UNSATISFIABLE" and r["lrat_check"] == "c VERIFIED"
         and r["cake_lpr"] == "s VERIFIED UNSAT"}
other8 = {r["unit"]: r["status"] for r in p8 if r["unit"] not in cert8}
print("P8 pilot: certified", len(cert8), "not certified", other8)
problems = []
for a in range(1, 9):
    inner = [o for o in range(1, T) if o != a]
    subs = [tuple(V) for h in (2, 3) for V in itertools.combinations(inner, h)]
    orbits = {}
    for V in subs:
        W = tuple(sorted((a - i) % T for i in V))
        assert W in set(subs) or W in subs
        orbits.setdefault(frozenset([V, W]), None)
    fixed = sum(1 for o in orbits if len(o) == 1)
    nopen = 0
    for o in orbits:
        names = {nm(a, V) for V in o}
        if names & listed:
            continue
        if names & cert8:
            continue
        nopen += 1
        problems.append(f"P{a}: orbit {sorted(names)} not covered (pilot status: {[other8.get(n) for n in names]})")
    cov = f"P{a}_cover"
    if not (cov in listed or cov in cert8):
        problems.append(f"{cov} missing")
    # orbit files
    fo = {l.split()[0]: l.split()[1] for l in open(f"{C}/orbits/P{a}.tsv") if not l.startswith("subcase")}
    for o in orbits:
        rep = min(o)          # tuple order = mklist's key
        for V in sorted(o):
            if fo.get(nm(a, V)) != nm(a, rep):
                problems.append(f"orbits/P{a}.tsv: {nm(a, V)} -> {fo.get(nm(a, V))}, expected {nm(a, rep)}")
    inlist = sum(1 for r in rows if r["case"] == f"P{a}" and r["kind"] != "cover")
    print(f"P{a}: orbits {len(orbits)} fixed {fixed}; listed subcase units {inlist}; uncovered orbits {nopen}")
# canonical hull cases: least cyclic gap sequence under rotation and reversal
def canon(seq):
    n = len(seq)
    forms = [tuple(seq[(i + k) % n] for k in range(n)) for i in range(n)]
    rs = seq[::-1]
    forms += [tuple(rs[(i + k) % n] for k in range(n)) for i in range(n)]
    return min(forms)
can = set()
for a in range(1, T):
    if canon((a, T - a)) == (a, T - a):
        can.add(f"P{a}")
for a, b in itertools.combinations(range(1, T), 2):
    s = (a, b - a, T - b)
    if canon(s) == s:
        can.add(f"H{a}-{b}")
filecan = {l.strip() for l in open(f"{R}/C2C34/canonical.txt") if l.strip()}
print("canonical.txt matches least-sequence rule:", filecan == can, len(filecan))
print("PROBLEMS", len(problems))
for p in problems[:30]:
    print("  ", p)
