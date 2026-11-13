#!/usr/bin/env python3
"""Auditor A5: importable copy of the map builders of symmaps.py (base.json path from the environment A5_MAP)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a5lib import *

mp = Map(os.environ["A5_MAP"])
convnum, last = conv_numbering(mp.nX)
assert last == mp.nv
pt = lambda o, r: 2 * o + r
rep = {}
for (x, y, z), (v, s) in mp.tv.items():
    rep.setdefault(v, []).append(((x, y, z), s))


def pi_A(a):
    pi = {pt(0, 0): pt(a, 0), pt(0, 1): pt(a, 1)}
    for j in range(1, T):
        if j <= 16 - a:
            o, r = a + j, 0
        elif j == 17 - a:
            o, r = 0, 1
        else:
            o, r = j + a - 17, 1
        pi[pt(j, 0)] = pt(o, r)
        pi[pt(j, 1)] = pt(o, 1 - r)
    pi[Z] = Z
    return pi


def pi_B(a):
    pi = {pt(0, 0): pt(a, 0), pt(0, 1): pt(a, 1)}
    for j in range(1, T):
        if j < a:
            o, r = a - j, 0
        elif j == a:
            o, r = 0, 0
        else:
            o, r = 17 + a - j, 1
        pi[pt(j, 0)] = pt(o, r)
        pi[pt(j, 1)] = pt(o, 1 - r)
    pi[Z] = Z
    return pi


def sigma(pi, eps):
    sg = [0] * (mp.nv + 1)
    for v, lst in rep.items():
        vals = set()
        for (x, y, z), s in lst:
            L = mp.lit(pi[x], pi[y], pi[z])
            assert L != 0, "zero triple hit"
            vals.add(s * eps * L)
        assert len(vals) == 1, ("sigma inconsistent on a triple class", v, vals)
        sg[v] = vals.pop()
    for S, v in convnum.items():
        sg[v] = convnum[canon(tuple(sorted(pi[i] for i in S)))]
    assert len({abs(x) for x in sg[1:]}) == mp.nv, "sigma not a bijection on variables"
    return sg


def hull_clauses(q):
    out = []
    for x, y, z in itertools.combinations([i for i in range(N) if i != q], 3):
        for s in (1, -1):
            cl = [-s * mp.lit(x, y, q), -s * mp.lit(y, z, q), -s * mp.lit(z, x, q)]
            if not any(-l in cl for l in cl):
                out.append(cl)
    return out
