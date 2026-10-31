#!/usr/bin/env python3
"""Mutation tests for the t = 17 harness: the checks must be able to fail.
1. Alternative (wrong) class maps for (B) are compared with what real reflected sets give:
   claimed (a - i), and wrong ones (17 - a - i), (a - i - 1), (a + i), (-i) (= restart at the other end of the hull).
2. A clockwise normal form (sort reversed) must violate the SB units; a non-hull first point must violate hull-SB.
usage: mut17.py MAP HULLCUBES L2DIR TAIL n seed"""
import itertools, random, sys, os, functools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom import *

mp = Map(sys.argv[1]); hull = load_cubes(sys.argv[2]); L2DIR = sys.argv[3]
lines = [l.split() for l in open(sys.argv[4]) if l.strip()]
sbu = [int(l[0]) for l in lines[:136]]; hsb = [[int(x) for x in l[:-1]] for l in lines[136:]]
n, seed = int(sys.argv[5]), int(sys.argv[6])
T = 17
rng = random.Random(seed)
l2 = {a: load_cubes(f"{L2DIR}/P{a}_cubes.txt") for a in range(1, T)}


def subcase(P, first):
    X = normal_form(P, first)
    val = mp.assign(X)
    a = [n_ for n_, c in hull.items() if cube_true(val, c)]
    assert len(a) == 1 and a[0][0] == "P"
    a = int(a[0][1:])
    s = [n_ for n_, c in l2[a].items() if cube_true(val, c)]
    assert len(s) == 1
    return a, tuple(int(x) for x in s[0].split("_")[1].split("-"))


maps = {"claimed (a-i)": lambda a, i: (a - i) % T, "(17-a-i)": lambda a, i: (T - a - i) % T,
        "(a-i-1)": lambda a, i: (a - i - 1) % T, "(a+i)": lambda a, i: (a + i) % T, "(-i)": lambda a, i: (-i) % T}
mism = {k: 0 for k in maps}
tot = 0
for _ in range(n):
    a = rng.randrange(1, T)
    inner = [o for o in range(1, T) if o != a]
    V = tuple(sorted(rng.sample(inner, rng.choice((2, 3)))))
    while True:
        P, p0 = design(T, a, V, rng)
        if general_position(P):
            break
    ga, gV = subcase(P, p0)
    pa = normal_form(P, p0)[2 * ga]
    kind = rng.randrange(3)
    Q = reflect(P, kind)
    got = subcase(Q, reflect([pa], kind)[0])
    tot += 1
    for k, f in maps.items():
        if got != (ga, tuple(sorted(f(ga, i) for i in gV))):
            mism[k] += 1
print("reflected sets:", tot, "mismatches per candidate map:", mism)

# 2. clockwise sort / non-hull first point
bad_sb = bad_hsb = 0
for _ in range(50):
    a = rng.randrange(1, T)
    inner = [o for o in range(1, T) if o != a]
    V = tuple(sorted(rng.sample(inner, 2)))
    while True:
        P, p0 = design(T, a, V, rng)
        if general_position(P):
            break
    X = normal_form(P, p0)
    # clockwise: reverse the order of classes 1..16 (keep representatives)
    Xc = X[:2]
    for o in range(T - 1, 0, -1):
        Xc += [X[2 * o], X[2 * o + 1]]
    Xc.append(X[-1])
    val = mp.assign(Xc)
    if not all(lit_true(val, l) for l in sbu):
        bad_sb += 1
    # first point not on the hull: an inner representative as (0,0)
    inner_pt = [p for p in P if p not in set(hull_ccw(P))][0]
    Xi = normal_form(P, inner_pt)
    val = mp.assign(Xi)
    if not all(any(lit_true(val, l) for l in cl) for cl in hsb):
        bad_hsb += 1
print("clockwise labellings rejected by the SB units:", bad_sb, "/ 50;",
      "inner first point rejected by hull-SB:", bad_hsb, "/ 50")
