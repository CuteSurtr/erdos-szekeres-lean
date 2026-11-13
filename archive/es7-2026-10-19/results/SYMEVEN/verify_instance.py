#!/usr/bin/env python3
"""Exact verification of an instance file (uses only the coordinates, not the cluster labels).
Usage: python3 verify_instance.py POINTS_FILE K [random_trials] [seed]"""
import random
import sys
import time
from itertools import combinations
from math import comb
from geom_check import (read_points, symmetry_report, general_position_violations, largest_convex_angular,
                        largest_convex_cupcap, brute_largest, in_convex_position, count_convex_by_size)


def main():
    path, k = sys.argv[1], int(sys.argv[2])
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 12345
    P, _ = read_points(path)
    N = len(P)
    ok = True
    print("file:", path, " k =", k, " N =", N, " max|coord| =", max(max(abs(x), abs(y)) for x, y in P))
    sr = symmetry_report(P)
    print("symmetry:", sr)
    ok &= sr["distinct"] and sr["centrally_symmetric"] and sr["origin_absent"] and N == 2 ** (k - 2)
    print("size == 2^(k-2):", N == 2 ** (k - 2))
    print("distinct x-coordinates:", len({x for x, _ in P}) == N)
    t0 = time.time()
    gp = general_position_violations(P)
    print("collinear triples: %d   (checked %d triples, %.1fs)" % (len(gp), comb(N, 3), time.time() - t0))
    ok &= not gp
    t0 = time.time()
    a, wit = largest_convex_angular(P)
    print("(A) angular DP: largest convex subset = %d  (%.1fs)" % (a, time.time() - t0))
    wok = len(set(wit)) == a and set(wit) <= set(P) and in_convex_position(wit)
    print("    witness of size %d independently in convex position (hull test): %s" % (len(wit), wok))
    print("    witness:", wit)
    t0 = time.time()
    b = largest_convex_cupcap(P)
    print("(B) cup+cap DP: largest convex subset = %d  (%.1fs)" % (b, time.time() - t0))
    t0 = time.time()
    cnt = count_convex_by_size(P, k + 1)
    print("counting DP: number of convex L-subsets, L=3..%d: %s  (%.1fs)" % (k + 1, cnt[3:], time.time() - t0))
    print("    count[3] == C(N,3):", cnt[3] == comb(N, 3))
    ok &= (a == b == k - 1) and wok and cnt[k] == 0 and cnt[k + 1] == 0 and cnt[3] == comb(N, 3)
    ok &= max(L for L in range(3, k + 2) if cnt[L] > 0) == a
    # (C) brute force on random subsets, compared with (A) and (B)
    rng = random.Random(seed)
    mism = 0
    hist = {}
    t0 = time.time()
    for t in range(trials):
        if t % 2 == 0:
            s = rng.randint(8, 14)
            Q = rng.sample(P, s)
        else:   # biased: a largest convex subset plus random extra points
            extra = rng.randint(3, 8)
            Q = list(set(wit) | set(rng.sample(P, extra)))
        x, y, z = largest_convex_angular(Q)[0], largest_convex_cupcap(Q), brute_largest(Q)
        hist[z] = hist.get(z, 0) + 1
        if not (x == y == z):
            mism += 1
            print("MISMATCH on subset", Q, x, y, z)
    print("(C) random subsets: %d trials, mismatches A/B/brute = %d, brute maxima histogram %s  (%.1fs)"
          % (trials, mism, dict(sorted(hist.items())), time.time() - t0))
    ok &= mism == 0
    if N <= 16:
        t0 = time.time()
        full = {}
        for L in range(3, min(N, k + 1) + 1):
            full[L] = sum(1 for c in combinations(P, L) if in_convex_position(c))
        print("full brute force (all subsets, hull test): convex L-subsets", full, " (%.1fs)" % (time.time() - t0))
        ok &= full.get(k, 0) == 0 and all(full[L] == cnt[L] for L in full)
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
