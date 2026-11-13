#!/usr/bin/env python3
"""Decode unit literals of the fivefold CNF into chi statements, written for an expected triple when one matches.
usage: decode_units.py MAP.json lit lit ...  (for each literal, print every triple in its variable's orbit that
involves the centre c=35 and an orbit-0 point, plus the min representative)"""
import json, sys
info = json.load(open(sys.argv[1]))
m, c = info["m"], info["center_index"]
inv = {}
for a, b, cc, v, s in info["triples"]:
    inv.setdefault(v, []).append((a, b, cc, s))
def nm(i):
    return "c" if i == c else f"({i // m},{i % m})"
def chi_of(lit, a, b, cc):
    """value of chi(a,b,cc) (in this argument order) asserted by literal lit, or None if not in lit's orbit"""
    def psort(t):
        x, y, z = t
        inv_ = (x > y) + (x > z) + (y > z)
        return tuple(sorted(t)), (-1 if inv_ & 1 else 1)
    S, sg = psort((a, b, cc))
    for (p, q, r, s) in inv[abs(lit)]:
        if (p, q, r) == S:
            return sg * s * (1 if lit > 0 else -1)
    return None
for tok in sys.argv[2:]:
    lit = int(tok)
    hits = []
    for o in range(1, info["t"]):
        for base in ((0, 0), (0, 1)):
            val = chi_of(lit, c, base[0] * m + base[1], o * m)
            if val is not None:
                hits.append(f"chi(c,{nm(base[0]*m+base[1])},{nm(o*m)})={'+' if val > 0 else '-'}")
    print(lit, "=>", "; ".join(hits) if hits else "(no sector-type triple)")
