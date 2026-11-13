#!/usr/bin/env python3
"""All single-flip neighbours (that are still signotopes) of a K-gon-free signotope, plus random
2-flip neighbours: compare CNF (X fixed, exact Horn propagation) with the 4-point brute force.
usage: neighbor_validate.py N K cnf start.sig seed n2"""
import itertools, random, sys
from exhaustive_validate import load_cnf, cnf_sat_given_X
from sigcheck import count_convex_4pt
from flip_validate import quad_ok

N, K, path, start, seed, n2 = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
rng = random.Random(seed)
sig = {}
for line in open(start):
    i, j, k, s = map(int, line.split()); sig[(i, j, k)] = s
nv, clauses = load_cnf(path)
occ = [[] for _ in range(nv + 1)]
for ci, c in enumerate(clauses):
    for l in c: occ[abs(l)].append(ci)
triples = list(itertools.combinations(range(1, N + 1), 3))
def valid_after(ts):
    quads = set()
    for t in ts:
        for m in range(1, N + 1):
            if m not in t: quads.add(tuple(sorted(set(t) | {m})))
    return all(quad_ok(sig, q) for q in quads)
def evaluate():
    c = count_convex_4pt(sig, N, K, stop_at=3)
    r = cnf_sat_given_X(nv, clauses, occ, {n + 1: sig[x] > 0 for n, x in enumerate(triples)})
    return c, r
c0, r0 = evaluate()
assert c0 == 0 and r0, "start must be K-gon-free and CNF-satisfiable"
flippable = []
hist = {}; mism = 0
for t in triples:
    sig[t] = -sig[t]
    if valid_after([t]):
        flippable.append(t)
        c, r = evaluate(); hist[c] = hist.get(c, 0) + 1
        if r != (c == 0): mism += 1; print("MISMATCH 1-flip", t)
    sig[t] = -sig[t]
print(f"N={N} K={K} {start}: 1-flip neighbours={len(flippable)} hist(#K-gons capped 3)={dict(sorted(hist.items()))} mismatches={mism}")
hist = {}; mism = 0; done = 0
while done < n2:
    t1, t2 = rng.sample(triples, 2)
    sig[t1] = -sig[t1]; sig[t2] = -sig[t2]
    if valid_after([t1, t2]):
        done += 1
        c, r = evaluate(); hist[c] = hist.get(c, 0) + 1
        if r != (c == 0): mism += 1; print("MISMATCH 2-flip", t1, t2)
    sig[t1] = -sig[t1]; sig[t2] = -sig[t2]
print(f"N={N} K={K} {start}: 2-flip neighbours sampled={done} hist={dict(sorted(hist.items()))} mismatches={mism}")
