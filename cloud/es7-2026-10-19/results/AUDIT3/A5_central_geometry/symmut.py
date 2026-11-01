#!/usr/bin/env python3
"""Auditor A5: mutants of the (B) literal map for a = 8, to show that symcheck can fail. Writes sigma files:
  mutB8_noneg   : no global sign change (treat the reflection as orientation preserving)
  mutB8_noflip  : correct class map, but no switch to the antipode for new classes j > a
  mutB8_shift   : class map i -> (a + 1 - i) mod 17 (an off-by-one variant), same flip rule
  mutA8_flipall : (A) for b = 8 with the antipode switch applied to every class
and the hull clauses of (0,0) for a wrong-extra test (hull_a0.cnf). Also checks the cube part for the mutants.
usage: symmut.py BASE_JSON RESULTS_DIR OUTDIR"""
import itertools, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a5lib import *
import symmaps_lib as L

MAPF, RES, OUT = sys.argv[1:4]
pt = lambda o, r: 2 * o + r
a = 8


def pi_custom(a, cls, flip):
    pi = {pt(0, 0): pt(a, 0), pt(0, 1): pt(a, 1), Z: Z}
    for j in range(1, T):
        o, r = cls(j), flip(j)
        pi[pt(j, 0)] = pt(o, r)
        pi[pt(j, 1)] = pt(o, 1 - r)
    return pi


muts = {
    "mutB8_noneg": (L.pi_B(a), +1),
    "mutB8_noflip": (pi_custom(a, lambda j: (a - j) % T, lambda j: 0), -1),
    "mutB8_shift": (pi_custom(a, lambda j: (a + 1 - j) % T if (a + 1 - j) % T not in (0, a) else ((a - j) % T), lambda j: 1 if j > a else 0), -1),
    "mutA8_flipall": (pi_custom(17 - a, lambda j: (j + 17 - a) % T if (j + 17 - a) % T != 0 else 0, lambda j: 1), +1),
}
for tag, (pi, eps) in muts.items():
    # the shifted map may not be a bijection on classes; skip it if so
    if len(set(pi.values())) != len(pi):
        print(tag, "not a bijection on points; skipped")
        continue
    try:
        sg = L.sigma(pi, eps)
    except AssertionError as e:
        print(tag, "sigma inconsistent on triple classes (already a detected failure):", str(e)[:80])
        continue
    with open(os.path.join(OUT, f"sigma_{tag}.bin"), "wb") as f:
        f.write(b"".join(struct.pack("<i", x) for x in sg))
    print(tag, "written")
with open(os.path.join(OUT, "hull_a0.cnf"), "w") as f:
    for cl in L.hull_clauses(pt(0, 0)):
        f.write(" ".join(map(str, cl)) + " 0\n")
print("hull_a0.cnf written")
