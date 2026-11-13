#!/usr/bin/env python3
"""Completeness/soundness check of the 4- and 5-point axioms used in symcnf.py, written
independently of symcnf.py.

For 4 and 5 labelled points enumerate every sign assignment to the triples; decide it by the
axioms (A4 interiority on every 4-subset, GP 3-term relations on the 5-set); compare with the
set of labelled chirotopes of random real point sets (which must saturate: all realizable
patterns are found).  Required outcome: accepted == realizable (as sets), 14 patterns for 4
points, 264 for 5 points.  Also checks the GP relation numerically on random real points.
"""
import itertools
import random
import sys


def parity(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return -1 if inv & 1 else 1


def make_O(sig):
    def O(a, b, c):
        return parity((a, b, c)) * sig[tuple(sorted((a, b, c)))]
    return O


def ok_A4(O, S):
    for t in S:
        p, q, r = [x for x in S if x != t]
        for s in (1, -1):
            if O(t, q, r) == s and O(p, t, r) == s and O(p, q, t) == s and O(p, q, r) != s:
                return False
    return True


def ok_GP(O, S):
    for x in S:
        y1, y2, y3, y4 = [y for y in S if y != x]
        t1 = O(x, y1, y2) * O(x, y3, y4)
        t2 = -O(x, y1, y3) * O(x, y2, y4)
        t3 = O(x, y1, y4) * O(x, y2, y3)
        if t1 == t2 == t3:
            return False
    return True


def accepted(n):
    triples = list(itertools.combinations(range(n), 3))
    acc = set()
    for pat in itertools.product((1, -1), repeat=len(triples)):
        sig = dict(zip(triples, pat))
        O = make_O(sig)
        if all(ok_A4(O, S) for S in itertools.combinations(range(n), 4)) and \
           all(ok_GP(O, S) for S in itertools.combinations(range(n), 5)):
            acc.add(pat)
    return triples, acc


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def realizable(n, triples, samples, rng):
    found = set()
    for _ in range(samples):
        pts = [(rng.random(), rng.random()) for _ in range(n)]
        pat = []
        bad = False
        for t in triples:
            d = orient(pts[t[0]], pts[t[1]], pts[t[2]])
            if abs(d) < 1e-12:
                bad = True
                break
            pat.append(1 if d > 0 else -1)
        if not bad:
            found.add(tuple(pat))
    return found


def gp_numeric(samples, rng):
    """the 3-term Grassmann-Pluecker identity with the sign convention of ok_GP"""
    worst = 0.0
    for _ in range(samples):
        P = [(rng.random(), rng.random()) for _ in range(5)]
        x, a, b, c, d = P
        val = orient(x, a, b) * orient(x, c, d) - orient(x, a, c) * orient(x, b, d) + orient(x, a, d) * orient(x, b, c)
        worst = max(worst, abs(val))
    return worst


def main():
    rng = random.Random(12345)
    print("GP identity max residual on random points:", gp_numeric(10000, rng))
    for n, samples in ((4, 20000), (5, 400000)):
        triples, acc = accepted(n)
        real = realizable(n, triples, samples, rng)
        print(f"n={n}: patterns={2**len(triples)} accepted_by_axioms={len(acc)} realizable_found={len(real)} "
              f"accepted==realizable: {acc == real}; realizable-not-accepted={len(real - acc)} accepted-not-realizable={len(acc - real)}")
        if acc != real:
            sys.exit(1)


if __name__ == "__main__":
    main()
