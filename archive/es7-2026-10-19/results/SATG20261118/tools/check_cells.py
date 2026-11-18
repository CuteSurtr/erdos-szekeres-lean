#!/usr/bin/env python3
"""check_cells.py -- vx1118, 18 Nov 2026. Trusted replay of the sample file written by satcells.cpp.
Exact Python integers / Fractions only; shares no code with satcells.cpp.

Usage: python3 check_cells.py points.txt K samples.txt [max_fail_dp]

(a)  S in general position; largest convex subset of S is K-1 (own O(n^4) DP over the lex-lowest vertex).
(b1) F = 1 + L + sum_v (k_v - 1): the number of open cells of the arrangement of the L = C(n,2) lines through pairs
     of S (insertion argument: a new line met at m distinct points by the earlier lines adds m + 1 cells; a vertex where
     k lines meet contributes k - 1 such points). k_v from the exact intersection points (Fractions); parallel pairs
     simply never meet.
(b2) every sample q = (QX/QD, QY/QD) has orient(s_i, s_j, q) != 0 for all pairs (S + q in general position); the sign
     vectors of the samples are pairwise distinct and there are exactly F of them. Distinct sign vectors lie in distinct
     open cells, so the samples meet all F open cells.
(b3) every sample marked P: the K-1 listed points of S plus q are in convex position (exact hull has K vertices).
(b4) every sample marked F (up to max_fail_dp of them): largest convex subset of S + q is < K (DP), i.e. q is on no
     convex K-gon of S + q.
"""
import sys
from fractions import Fraction
from functools import cmp_to_key


def read_points(path):
    pts = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        x, y = line.split()[:2]
        pts.append((int(x), int(y)))
    return pts


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def largest_convex(P):
    """Size of the largest subset of P in convex position (P in general position, integer coordinates)."""
    n = len(P)
    best = min(n, 2)
    for b in range(n):
        pb = P[b]
        U = [i for i in range(n) if (P[i][1], P[i][0]) > (pb[1], pb[0])]
        U.sort(key=cmp_to_key(lambda i, j: -1 if orient(pb, P[i], P[j]) > 0 else 1))
        for a in range(1, len(U)):
            assert orient(pb, P[U[a - 1]], P[U[a]]) > 0, "angular order"
        m = len(U)
        dp = [[0] * m for _ in range(m)]
        for j in range(m):
            pj = P[U[j]]
            for i in range(j):
                pi = P[U[i]]
                v = 3                      # polygon chain b -> U[i] -> U[j]
                for k in range(i):
                    c = dp[k][i] + 1
                    if c > v and orient(P[U[k]], pi, pj) > 0:
                        v = c
                dp[i][j] = v
                if v > best and orient(pi, pj, pb) > 0:
                    best = v
    return best


def hull_size(Q):
    """Number of vertices of the convex hull of integer points Q (Andrew's monotone chain, strict turns)."""
    Q = sorted(Q)
    def chain(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and orient(h[-2], h[-1], p) <= 0:
                h.pop()
            h.append(p)
        return h
    lo, up = chain(Q), chain(Q[::-1])
    return len(lo) + len(up) - 2


def main():
    pts_path, K, samp_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    max_fail_dp = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    S = read_points(pts_path)
    n = len(S)
    xs = [p[0] for p in S]
    ys = [p[1] for p in S]
    print(f"input {pts_path} n={n} K={K}")

    # (a)
    assert len(set(S)) == n, "repeated point"
    coll = sum(1 for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n) if orient(S[i], S[j], S[k]) == 0)
    lc = largest_convex(S)
    print(f"a.collinear_triples={coll} largest_convex_subset={lc} -> {'OK' if coll == 0 and lc == K - 1 else 'FAIL'}")

    # (b1)
    lines = [(i, j) for i in range(n) for j in range(i + 1, n)]
    L = len(lines)
    coef = [(-(ys[j] - ys[i]), xs[j] - xs[i], (ys[j] - ys[i]) * xs[i] - (xs[j] - xs[i]) * ys[i]) for i, j in lines]
    for (i, j), (A, B, C) in zip(lines, coef):
        for k in range(n):
            assert A * xs[k] + B * ys[k] + C == orient(S[i], S[j], S[k])
    verts = {}
    par = 0
    for a in range(L):
        A1, B1, C1 = coef[a]
        for b in range(a + 1, L):
            A2, B2, C2 = coef[b]
            D = A1 * B2 - A2 * B1
            if D == 0:
                par += 1
                continue
            x = Fraction(B1 * C2 - B2 * C1, D)
            y = Fraction(C1 * A2 - C2 * A1, D)
            assert A1 * x + B1 * y + C1 == 0 and A2 * x + B2 * y + C2 == 0
            e = verts.get((x, y))
            if e is None:
                verts[(x, y)] = [{a, b}, 1]
            else:
                e[0].add(a)
                e[0].add(b)
                e[1] += 1
    sum_km1 = 0
    hist = {}
    for (lset, gen) in verts.values():
        k = len(lset)
        assert gen == k * (k - 1) // 2, "vertex multiplicity"
        sum_km1 += k - 1
        hist[k] = hist.get(k, 0) + 1
    F = 1 + L + sum_km1
    print(f"b1.lines={L} parallel_pairs={par} vertices={len(verts)} hist={dict(sorted(hist.items()))} "
          f"sum(k_v-1)={sum_km1} F={F}")

    # (b2)-(b4)
    info = [(i, xs[j] - xs[i], ys[j] - ys[i]) for i, j in lines]
    seen = set()
    nsamp = npass = nfail = nfail_dp = 0
    bad = 0
    maxbits = 0
    with open(samp_path) as fh:
        for line in fh:
            parts = line.split()
            QX, QY, QD = int(parts[0]), int(parts[1]), int(parts[2])
            tag = parts[3]
            nsamp += 1
            assert QD > 0
            maxbits = max(maxbits, QX.bit_length(), QY.bit_length(), QD.bit_length())
            PX = [QX - x * QD for x in xs]
            PY = [QY - y * QD for y in ys]
            vals = [dx * PY[i] - dy * PX[i] for (i, dx, dy) in info]   # orient(s_i, s_j, q) * QD (QD > 0)
            if 0 in vals:
                print(f"  sample {nsamp}: on a line")
                bad += 1
                continue
            key = int(''.join('1' if v > 0 else '0' for v in vals), 2)
            if key in seen:
                print(f"  sample {nsamp}: repeated cell")
                bad += 1
            seen.add(key)
            if tag == 'P':
                T = [int(t) for t in parts[4:4 + K - 1]]
                assert len(set(T)) == K - 1 and all(0 <= t < n for t in T)
                Q = [(xs[t] * QD, ys[t] * QD) for t in T] + [(QX, QY)]
                if hull_size(Q) != K:
                    print(f"  sample {nsamp}: witness not in convex position")
                    bad += 1
                else:
                    npass += 1
            elif tag == 'F':
                nfail += 1
                if nfail_dp < max_fail_dp:
                    P = [(x * QD, y * QD) for x, y in S] + [(QX, QY)]
                    if largest_convex(P) >= K:
                        print(f"  sample {nsamp}: marked F but a convex {K}-gon exists")
                        bad += 1
                    nfail_dp += 1
            else:
                bad += 1
    ok = (bad == 0 and len(seen) == nsamp == F and coll == 0 and lc == K - 1)
    print(f"b2.samples={nsamp} distinct_cells={len(seen)} F={F} max_sample_bits={maxbits}")
    print(f"b3.pass_with_verified_witness={npass}  b4.fail={nfail} (DP-confirmed {nfail_dp})  bad={bad}")
    verdict = ("SATURATED" if nfail == 0 else "NOT_SATURATED") if ok else "CHECK_FAILED"
    print(f"REPLAY n={n} K={K} cells={F} pass={npass} fail={nfail} bad={bad} verdict={verdict}")
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
