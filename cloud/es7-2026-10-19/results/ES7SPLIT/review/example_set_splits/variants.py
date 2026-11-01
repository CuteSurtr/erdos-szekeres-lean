#!/usr/bin/env python3
"""Alternative realizations of the classical Erdos-Szekeres 32-point construction (same recursive stacking scheme as
scripts/es_lower_bound_witness.py, re-implemented here with tunable horizontal gaps and vertical offsets), and an
exact check, for each realization, of (i) the order type (all triple signs) vs the repository realization,
(ii) the one-sided partitions (backtracking), (iii) for each one-sided partition, whether some z exists (exact_z).
"""
import sys, os, itertools, random, math, json
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_z import z_exists, verify
from backtrack_onesided import enumerate_onesided


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sgn(x):
    return (x > 0) - (x < 0)


def make_stack(rng, mode):
    def stack(sign, left, right):
        gap = 0 if mode == "orig" else rng.choice([0, 0, 1, 5, 50])
        t = max(p[0] for p in left) - min(p[0] for p in right) + 1 + gap
        moved = [(x + t, y) for x, y in right]
        need = Fraction(0)
        for a, a2 in itertools.combinations(sorted(left), 2):
            for b in moved:
                need = max(need, Fraction(-sign * orient(a, a2, b), a2[0] - a[0]))
        for a in left:
            for b, b2 in itertools.combinations(sorted(moved), 2):
                need = max(need, Fraction(sign * orient(a, b, b2), b2[0] - b[0]))
        m = math.floor(need) + 1
        if mode == "orig":
            pass
        elif mode == "random":
            m = m * rng.choice([1, 1, 2, 10, 1000]) + rng.choice([0, 3, 100])
        elif mode == "huge_last":
            m = m * (10 ** 6 if len(left) >= 16 else 1)
        elif mode == "huge_first":
            m = m * (10 ** 6 if len(left) < 16 else 1)
        return left + [(x, y + sign * m) for x, y in moved]
    return stack


def witness(n, stack):
    cache = {}
    def ccf(k, l):
        if (k, l) not in cache:
            if k == 2 or l == 2:
                cache[k, l] = [(0, 0)]
            else:
                cache[k, l] = stack(1, ccf(k - 1, l), ccf(k, l - 1))
        return cache[k, l]
    pts = ccf(n, 2)
    for j in range(1, n - 1):
        pts = stack(-1, pts, ccf(n - j, j + 2))
    return pts


def chirotope(P):
    return tuple(sgn(orient(P[i], P[j], P[k])) for i, j, k in itertools.combinations(range(len(P)), 3))


def main():
    out_lines = []
    base = witness(7, make_stack(None, "orig"))
    repo = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.split()]
    assert base == repo, "re-implementation does not reproduce the repository set"
    chi0 = chirotope(base)
    configs = [("orig", 0), ("huge_last", 0), ("huge_first", 0)] + [("random", s) for s in range(1, 13)]
    for mode, seed in configs:
        rng = random.Random(seed)
        P = witness(7, make_stack(rng, mode))
        same = chirotope(P) == chi0
        sols, _ = enumerate_onesided(P)
        res = []
        for X in sols:
            A = X
            B = frozenset(range(len(P))) - X
            ok, w = z_exists(P, A, B)
            if ok:
                assert verify(P, A, B, w)
            res.append(((len(A), len(B), min(A)), ok))
        nsplit = sum(1 for _, ok in res if ok)
        line = (f"{mode:10s} seed={seed:2d} maxcoord={max(max(abs(x), abs(y)) for x, y in P):>22d} "
                f"same_order_type={same} one_sided={len(sols)} splits_with_z={nsplit} "
                f"detail={sorted(res)}")
        print(line, flush=True)
        out_lines.append(line)


if __name__ == "__main__":
    main()
