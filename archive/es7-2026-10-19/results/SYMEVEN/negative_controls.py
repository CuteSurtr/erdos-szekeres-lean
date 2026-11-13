#!/usr/bin/env python3
"""Negative controls.
(1) Same construction but the middle cluster M0 is scaled by a factor F. For F = 1 (M0 much smaller than
    the outer clusters) there is no convex k-gon; when M0 becomes larger than the outer clusters, the
    configuration 'cup in B_{n/2-1}, two points of M, cap in B_{n/2+1}' becomes convex and a k-gon appears.
(2) 'Split middle' variant: k clusters on a centrally symmetric base without centre, middle clusters of
    types (k/2,k/2+1) and (k/2+1,k/2); the four central base points form a parallelogram, so a k-gon exists.
All checks exact (angular DP + cup/cap DP + hull test of the witness)."""
import sys
from construct import G, middle_cluster, flatten, center, neg, max_abs_slope, ceil_frac, normalize
from geom_check import (general_position_violations, largest_convex_angular, largest_convex_cupcap,
                        in_convex_position)
from fractions import Fraction


def build_scaled(k, F):
    n, m = k - 2, k // 2
    xs = [2 * j - n + 1 for j in range(n // 2)] + [0] + [2 * j - n - 1 for j in range(n // 2 + 1, n + 1)]
    Gs = {j: G(j + 2, k - j) for j in range(n // 2)}
    M0 = middle_cluster(m)
    RM = max(abs(p[0]) + abs(p[1]) for p in M0)
    s_max = max([max_abs_slope(Gs[j]) for j in Gs] + [Fraction(0)])
    H_max = max(max(p[1] for p in normalize(Gs[j])) for j in Gs)
    c = max(ceil_frac(16 * s_max), 8 * RM, 8 * H_max) + 1
    flat = {j: center(flatten(Gs[j], c)) for j in Gs}
    Rc = max(max(abs(p[0]) + abs(p[1]) for p in flat[j]) for j in flat)
    Lam = 10 ** 18          # keep the base scale far above every cluster scale used here
    pts = []
    for j in range(n // 2):
        Bj = [(Lam * xs[j] + p[0], Lam * xs[j] ** 3 + p[1]) for p in flat[j]]
        pts += Bj + neg(Bj)
    pts += [(F * p[0], F * p[1]) for p in M0]
    return pts, RM, Rc


def report(tag, P, k):
    gp = general_position_violations(P)
    a, wit = largest_convex_angular(P)
    b = largest_convex_cupcap(P)
    print("%-48s N=%d collinear=%d  largest convex: A=%d B=%d  witness convex=%s  k-gon present=%s"
          % (tag, len(P), len(gp), a, b, in_convex_position(wit), a >= k))
    return a


def split_middle(k):
    """k clusters: x-positions symmetric, no centre; types (j+2,k-j) for j<n/2, middle pair
    (k/2,k/2+1) at x=-1 and (k/2+1,k/2) at x=+1, outer clusters at odd positions."""
    n = k - 2
    xs_left = [2 * j - n - 1 for j in range(n // 2)] + [-1]      # e.g. k=6: [-5,-3,-1]
    types_left = [(j + 2, k - j) for j in range(n // 2)] + [(k // 2, k // 2 + 1)]
    sets = [G(a, b) for (a, b) in types_left]
    s_max = max([max_abs_slope(S) for S in sets] + [Fraction(0)])
    c = ceil_frac(64 * s_max) + 1
    Lam = 10 ** 15
    pts = []
    for x, S in zip(xs_left, sets):
        B = [(Lam * x + p[0], Lam * x ** 3 + p[1]) for p in center(flatten(S, c))]
        pts += B + neg(B)
    return pts


if __name__ == "__main__":
    for k in (6, 8):
        print("k =", k)
        for F in (1, 10, 100, 1000, 10 ** 4, 10 ** 6):
            P, RM, Rc = build_scaled(k, F)
            report("  middle cluster scaled by F=%g (R_M*F=%d, R_c=%d)" % (F, RM * F, Rc), P, k)
        report("  split-middle variant (k clusters, no centre)", split_middle(k), k)
