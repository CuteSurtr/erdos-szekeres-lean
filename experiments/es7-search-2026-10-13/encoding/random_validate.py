#!/usr/bin/env python3
"""Random validation of the CNF for larger N, K (where exhaustive enumeration is impossible).

Samples (a) random realizable signotopes (random integer points, x-sorted) and
(b) random abstract signotopes (random wiring diagrams = random reduced words of the reversal),
evaluates the actual CNF file with X fixed (exact: the aux part is Horn; unit propagation),
and compares with the independent 4-point brute force for a convex K-subset.

usage: random_validate.py N K cnf seed samples
"""
import itertools
import random
import sys
from exhaustive_validate import load_cnf, cnf_sat_given_X
from sigcheck import count_convex_4pt, is_signotope


def sig_from_points(pts):
    pts = sorted(pts)
    n = len(pts)
    sig = {}
    for i, j, k in itertools.combinations(range(n), 3):
        a, b, c = pts[i], pts[j], pts[k]
        o = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if o == 0:
            return None
        sig[(i + 1, j + 1, k + 1)] = 1 if o > 0 else -1
    return sig


def random_points(n, rng, R):
    while True:
        xs = rng.sample(range(-R, R), n)
        pts = [(x, rng.randrange(-R, R)) for x in xs]
        s = sig_from_points(pts)
        if s is not None:
            return s


def random_wiring(n, rng):
    perm = list(range(1, n + 1))
    t = 0
    when = {}
    while True:
        cand = [p for p in range(n - 1) if perm[p] < perm[p + 1]]
        if not cand:
            break
        p = rng.choice(cand)
        a, b = perm[p], perm[p + 1]
        when[(a, b)] = t
        t += 1
        perm[p], perm[p + 1] = b, a
    sig = {}
    for i, j, k in itertools.combinations(range(1, n + 1), 3):
        sig[(i, j, k)] = 1 if when[(i, j)] < when[(j, k)] else -1
    return sig


def main():
    N, K, path, seed, samples = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    rng = random.Random(seed)
    nv, clauses = load_cnf(path)
    occ = [[] for _ in range(nv + 1)]
    for ci, c in enumerate(clauses):
        for l in c:
            occ[abs(l)].append(ci)
    triples = list(itertools.combinations(range(1, N + 1), 3))
    stats = {"points": [0, 0, 0], "wiring": [0, 0, 0]}  # samples, free, mismatches
    for s in range(samples):
        for kind in ("points", "wiring"):
            if kind == "points":
                R = rng.choice([20, 100, 10000])
                sig = random_points(N, rng, R)
            else:
                sig = random_wiring(N, rng)
            assert is_signotope(sig, N)[0]
            free = count_convex_4pt(sig, N, K, stop_at=1) == 0
            r = cnf_sat_given_X(nv, clauses, occ, {n + 1: sig[t] > 0 for n, t in enumerate(triples)})
            st = stats[kind]
            st[0] += 1
            st[1] += free
            if r != free:
                st[2] += 1
                print("MISMATCH", kind, r, free)
    print(f"N={N} K={K}: " + "; ".join(f"{k}: samples={v[0]} K-gon-free={v[1]} mismatches={v[2]}" for k, v in stats.items()))


if __name__ == "__main__":
    main()
