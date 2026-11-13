#!/usr/bin/env python3
"""Auditor A5: reductions (A) and (B) as literal maps on the CNF.

A relabelling of a real configuration induces a map sigma from the variables of the NEW labelling (the formula that
was solved) to literals of the OLD labelling (the configuration to be excluded):
  triple variables: chi_new(T) = eps * chi_old(pi(T))  (eps = -1 for (B), which reflects; +1 for (A)),
  conv variables  : conv_new(S) = conv_old(canon(pi(S))),
with pi: new point index -> old point index (my derivation, see geomtests.py) and pi(Z) = Z.
If sigma(base) is contained in base + H_a (H_a = "(a,0) is not inside a triangle of three other points", valid for every
real configuration in case P_a) and sigma maps the solved cube onto the cube to be excluded, then
UNSAT(base + solved cube) implies UNSAT(base + H_a + excluded cube), hence no real configuration lies in the excluded
case. This script writes sigma (binary, for symcheck.c) and H_a, and checks the cube part for every subcase.
  (A) for b = 1..8, a = 17 - b: new labelling starts at old p_a; solved case P_b, excluded case P_a.
  (B) for a = 1..8: reflect and start at rho(old p_a); solved (P_a, V'), excluded (P_a, V), V' = {(a - i) mod 17}.
usage: symmaps.py BASE_JSON RESULTS_DIR OUTDIR"""
import itertools, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a5lib import *

MAPF, RES, OUT = sys.argv[1:4]
mp = Map(MAPF)
convnum, last = conv_numbering(mp.nX)
assert last == mp.nv
hull, _ = load_cubes(os.path.join(RES, "C2C34", "cubes.txt"))
L2 = {a: load_cubes(os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt"))[0] for a in range(1, 9)}
pt = lambda o, r: 2 * o + r

# class representative triples for every triple variable
rep = {}
for (x, y, z), (v, s) in mp.tv.items():
    rep.setdefault(v, []).append(((x, y, z), s))


def pi_A(a):
    """new index -> old index for (A): start at old (a,0), no reflection"""
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
    """new index -> old index for (B): reflect, start at rho(old (a,0))"""
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
            assert L != 0
            vals.add(s * eps * L)            # X_v^new = s * chi_new(T) = s * eps * chi_old(pi T)
        assert len(vals) == 1, ("sigma inconsistent on a triple class", v, vals)
        sg[v] = vals.pop()
    for S, v in convnum.items():
        sg[v] = convnum[canon(tuple(sorted(pi[i] for i in S)))]
    assert all(sg[v] != 0 for v in range(1, mp.nv + 1))
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


def write(tag, sg, a):
    with open(os.path.join(OUT, f"sigma_{tag}.bin"), "wb") as f:
        f.write(b"".join(struct.pack("<i", x) for x in sg))
    with open(os.path.join(OUT, f"hull_a{a}.cnf"), "w") as f:
        for cl in hull_clauses(pt(a, 0)):
            f.write(" ".join(map(str, cl)) + " 0\n")


def image(sg, lits):
    return {(sg[abs(l)] if l > 0 else -sg[abs(l)]) for l in lits}


fails = []
for b in range(1, 9):
    a = 17 - b
    sg = sigma(pi_A(a), +1)
    write(f"A{b}", sg, a)
    ok = image(sg, hull[f"P{b}"]) == set(hull[f"P{a}"])
    # the second-layer cubes too (not needed for (A), which is used at the hull level only)
    inner_new = [o for o in range(1, T) if o != b]
    okV = 0
    for h in (2, 3):
        for V in itertools.combinations(inner_new, h):
            pass
    print(f"(A) b={b}, a={a}: sigma(P{b} cube) == P{a} cube: {ok}")
    if not ok:
        fails.append(f"A{b}")
for a in range(1, 9):
    sg = sigma(pi_B(a), -1)
    write(f"B{a}", sg, a)
    ok_h = image(sg, hull[f"P{a}"]) == set(hull[f"P{a}"])
    bad = 0
    for n, c in L2[a].items():
        V = [int(x) for x in n.split("_")[1].split("-")]
        Vp = f"P{a}_" + "-".join(map(str, sorted((a - i) % T for i in V)))
        # solved cube is that of V' (new labelling); excluded is V (old labelling)
        if image(sg, L2[a][Vp]) != set(c):
            bad += 1
    print(f"(B) a={a}: sigma(P{a} cube) == P{a} cube: {ok_h}; subcases with sigma(cube(V')) != cube(V): {bad} of {len(L2[a])}")
    if not ok_h or bad:
        fails.append(f"B{a}")
print("cube-level FAILURES", fails)
