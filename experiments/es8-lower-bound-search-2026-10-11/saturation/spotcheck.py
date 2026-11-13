#!/usr/bin/env python3
r"""Third, explicit-coordinate spot check using the repository's own code.

Random arrangement vertices v (line(a,b) /\ line(c,d)) and random wedge
directions d = +-(b-a) +-(d-c) are turned into explicit rational points
p = v + d / 2^j, with j increased until the explicit sign vector of p
w.r.t. all C(N,2) lines equals the symbolic one (so p lies in that face).
Coordinates are scaled to integers, and the unchanged
`largest_convex_subset` from scripts/es_lower_bound_witness.py (an O(N^4)
DP) must report n for S + {p}: p creates a convex n-gon.

usage: spotcheck.py n samples seed
"""
import json, os, random, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "scripts"))
from es_lower_bound_witness import witness, largest_convex_subset, orient, general_position


def sgn(x):
    return (x > 0) - (x < 0)


def main():
    n, samples, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    S = witness(n)
    N = len(S)
    lines = [(a, b) for a in range(N) for b in range(a + 1, N)]
    done = 0
    results = []
    t0 = time.time()
    while done < samples:
        (a, b), (c, d) = rng.sample(lines, 2)
        if len({a, b, c, d}) < 4:
            continue
        A, B, C, Dp = S[a], S[b], S[c], S[d]
        u = (B[0] - A[0], B[1] - A[1]); w = (Dp[0] - C[0], Dp[1] - C[1])
        den = u[0] * w[1] - u[1] * w[0]
        if den == 0:
            continue
        T = (C[0] - A[0]) * w[1] - (C[1] - A[1]) * w[0]
        if den < 0:
            den, T = -den, -T
        X, Y = A[0] * den + T * u[0], A[1] * den + T * u[1]   # v = (X/den, Y/den)
        s1, s2 = rng.choice((1, -1)), rng.choice((1, -1))
        dx, dy = s1 * u[0] + s2 * w[0], s1 * u[1] + s2 * w[1]
        # symbolic signs
        sym = []
        valid = True
        for (e, f) in lines:
            E, Fp = S[e], S[f]
            o = (Fp[0] - E[0]) * (Y - E[1] * den) - (Fp[1] - E[1]) * (X - E[0] * den)
            if o == 0:
                o = (Fp[0] - E[0]) * dy - (Fp[1] - E[1]) * dx
            if o == 0:
                valid = False
                break
            sym.append(sgn(o))
        if not valid:
            continue
        j = 1
        while True:
            M = den << j
            P = (X * (1 << j) + dx * den, Y * (1 << j) + dy * den)  # p * M
            SS = [(x * M, y * M) for x, y in S]
            if all(sgn(orient(SS[e], SS[f], P)) == s for (e, f), s in zip(lines, sym)):
                break
            j += 1
        pts = SS + [P]
        assert general_position(pts)
        size = largest_convex_subset(pts)
        results.append(size)
        done += 1
    out = {"n": n, "samples": samples, "seed": seed,
           "largest_convex_subset_values": sorted(set(results)),
           "all_equal_n": all(r == n for r in results), "seconds": round(time.time() - t0, 1)}
    print(json.dumps(out))
    return 0 if out["all_equal_n"] else 1


if __name__ == "__main__":
    sys.exit(main())
