#!/usr/bin/env python3
"""Quick encoder sanity: evaluate every base.cnf clause over triple variables only (GP, A4, SB units, hull-SB) on real
centrally symmetric 34-point sets in the angular normal form (first point a hull vertex), bit-parallel over labellings.
usage: encsanity.py BASE_CNF BASE_JSON NSETS SEED"""
import functools, itertools, json, random, sys

BASE, MAP, NS, SEED = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
info = json.load(open(MAP)); XV = info["X_vars"]; trip = info["triples"]
rng = random.Random(SEED)

def orient(p, q, r):
    d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (d > 0) - (d < 0)

def hull_vertices(pts):
    pts = sorted(set(pts))
    def half(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and orient(h[-2], h[-1], p) <= 0: h.pop()
            h.append(p)
        return h
    lo, up = half(pts), half(pts[::-1])
    return lo[:-1] + up[:-1]

def normal_form(P, start):
    o = (0, 0)
    pts = P + [(-x, -y) for x, y in P]
    left = [q for q in pts if q != start and q != (-start[0], -start[1]) and orient(o, start, q) > 0]
    assert len(left) == 16
    left.sort(key=functools.cmp_to_key(lambda q, q2: -orient(o, q, q2)))
    lab = [start, (-start[0], -start[1])]
    for q in left: lab += [q, (-q[0], -q[1])]
    return lab + [o]

def gen(par):
    while True:
        if par:
            P = [(rng.randint(900, 1100), rng.randint(-150, 150)), (rng.randint(-150, 150), rng.randint(900, 1100))]
            while len(P) < 17: P.append((rng.randint(-350, 350), rng.randint(-350, 350)))
        else:
            P = [(rng.randint(-1000, 1000), rng.randint(-1000, 1000)) for _ in range(17)]
        pts = P + [(-x, -y) for x, y in P]
        if len(set(pts)) < 34 or (0, 0) in pts: continue
        if any(orient(p, q, r) == 0 for p, q, r in itertools.combinations(pts, 3)): continue
        return P

labs = []
for k in range(NS):
    P = gen(k % 2 == 0)
    pts = P + [(-x, -y) for x, y in P]
    for s in hull_vertices(pts):
        labs.append(normal_form(P, s))
L = len(labs); ALL = (1 << L) - 1
val = [0] * (XV + 1)
for j, lab in enumerate(labs):
    seen = {}
    for a, b, c, v, s in trip:
        x = s * orient(lab[a], lab[b], lab[c]) > 0
        assert orient(lab[a], lab[b], lab[c]) != 0
        if v in seen: assert seen[v] == x, "identification inconsistent"
        seen[v] = x
        if x: val[v] |= 1 << j
pos = val; neg = [ALL & ~m for m in val]
n_eval = n_skip = n_fail = 0; fails = []
with open(BASE) as f:
    for line in f:
        if line[0] in "cp": continue
        lits = line.split()[:-1]
        m = 0; skip = False
        for t in lits:
            l = int(t); v = l if l > 0 else -l
            if v > XV: skip = True; break
            m |= pos[v] if l > 0 else neg[v]
        if skip: n_skip += 1; continue
        n_eval += 1
        if m != ALL:
            n_fail += 1
            if len(fails) < 5: fails.append((line.strip(), bin(ALL & ~m).count("1")))
print(f"labellings {L}; clauses over triple vars evaluated {n_eval}, skipped (aux vars) {n_skip}, violated {n_fail}", fails)
