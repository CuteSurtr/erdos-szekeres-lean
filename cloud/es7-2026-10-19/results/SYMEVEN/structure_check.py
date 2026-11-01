#!/usr/bin/env python3
"""Check, exactly, that an instance satisfies the hypotheses (H0)-(H5) of the blow-up lemma (Lemma 3) in PROOF.md,
using the cluster labels in the points file. Usage: python3 structure_check.py POINTS_FILE K"""
import sys
from fractions import Fraction
from math import comb
from geom_check import read_points, orient, longest_cup_cap


def sgn(v):
    return (v > 0) - (v < 0)


def main():
    path, k = sys.argv[1], int(sys.argv[2])
    n = k - 2
    h = n // 2
    xs = [2 * j - n + 1 for j in range(h)] + [0] + [2 * j - n - 1 for j in range(h + 1, n + 1)]
    P, lab = read_points(path)
    B = {j: [p for p, l in zip(P, lab) if l == j] for j in range(n + 1)}
    ok = True
    print("base abscissae x_j:", xs)
    # sizes and symmetry of the cluster structure
    sizes = {j: len(B[j]) for j in B}
    s_ok = all(sizes[j] == comb(k - 2, j) for j in B)
    sym_ok = all(sorted((-x, -y) for x, y in B[j]) == sorted(B[n - j]) for j in B)
    print("cluster sizes:", sizes, " == C(k-2,j):", s_ok)
    print("B_{n-j} = -B_j for all j (incl. middle B_{n/2} = -B_{n/2}):", sym_ok)
    ok &= s_ok and sym_ok
    # H0 distinct x
    h0 = len({p[0] for p in P}) == len(P)
    print("(H0) distinct x-coordinates:", h0)
    # H1 separation
    h1 = all(max(p[0] for p in B[j]) < min(p[0] for p in B[j + 1]) for j in range(n))
    print("(H1) clusters x-separated in index order:", h1)
    # H2 slopes
    intra = []
    inter = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            s = Fraction(P[j][1] - P[i][1], P[j][0] - P[i][0])
            (intra if lab[i] == lab[j] else inter).append(s)
    h2 = max(intra) < min(inter)
    print("(H2) max intra-cluster slope %s (%.4g) < min inter-cluster slope %s (%.4g): %s"
          % (max(intra), float(max(intra)), min(inter), float(min(inter)), h2))
    # H3 and H4
    h3_bad = h3_cnt = h4_bad = h4_cnt = 0
    for a in range(n + 1):
        for b in range(a + 1, n + 1):
            for c in range(b + 1, n + 1):
                ssum = xs[a] + xs[b] + xs[c]
                for p in B[a]:
                    for q in B[b]:
                        for r in B[c]:
                            o = sgn(orient(p, q, r))
                            if ssum != 0:
                                h3_cnt += 1
                                if o != sgn(ssum):
                                    h3_bad += 1
                            else:
                                assert b == h and c == n - a, "unexpected zero-sum base triple"
                                if p[0] + r[0] != 0:
                                    h4_cnt += 1
                                    if o != -sgn(p[0] + r[0]):
                                        h4_bad += 1
    print("(H3) triples from distinct clusters with nonzero base sum: %d checked, %d with wrong sign" % (h3_cnt, h3_bad))
    print("(H4) triples (B_j, B_{n/2}, B_{n-j}) with x(p)+x(r) != 0: %d checked, %d with wrong sign" % (h4_cnt, h4_bad))
    # H5 cup/cap parameters
    h5 = True
    for j in range(n + 1):
        cu, ca = longest_cup_cap(B[j])
        need_cu, need_ca = j + 1, k - j - 1
        good = cu <= need_cu and ca <= need_ca
        h5 &= good
        print("(H5) B_%d: longest cup %d (<= %d), longest cap %d (<= %d): %s" % (j, cu, need_cu, ca, need_ca, good))
    ok &= h0 and h1 and h2 and h3_bad == 0 and h4_bad == 0 and h5
    print("STRUCTURE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
