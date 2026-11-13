#!/usr/bin/env python3
"""F4 check 1 (generic geometry, exact integers, independent of the project's code).

For random point sets in general position with distinct x-coordinates, compute the LEAST
FIXPOINT of the C3a chain definitions exactly as README/c3cnf.py state them:
    Y[x,b,c]      <- B(x,c) and ccw(x,b,c)
    W2[x,a,b]     <- B(x,a) and Y[x,a,b]
    W(r+1)[x,b,c] <- W r[x,a,b] and Y[x,b,c] and ccw(a,b,c)        (c not in {a,b})
    gon:  W(k-2)[x,a,b] and Y[x,b,c] and ccw(a,b,c) -> false        (c not in {a,b})
(B(x,c) = x has smaller x-coordinate than c.)

Tests:
  (S) soundness direction needed for UNSAT claims: least fixpoint violates a gon clause  =>
      a real convex k-gon exists.  Tested twice: (i) against brute force on k-gon-free sets,
      (ii) every complete chain found by DFS is checked to be a convex k-gon in that ccw order.
  (C) the other direction ("a real convex k-gon forces a contradiction"): brute force finds
      a convex k-set => least fixpoint violates a gon clause.
Usage: chain_lemma_check.py SEED TRIALS
"""
import itertools
import random
import sys


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def hull_ccw(pts):
    """indices of the convex hull vertices in ccw order (monotone chain, exact)."""
    idx = sorted(range(len(pts)), key=lambda i: pts[i])
    def half(order):
        h = []
        for i in order:
            while len(h) >= 2 and orient(pts[h[-2]], pts[h[-1]], pts[i]) <= 0:
                h.pop()
            h.append(i)
        return h
    lo = half(idx)
    up = half(idx[::-1])
    return lo[:-1] + up[:-1]


def convex_position(pts):
    return len(hull_ccw(pts)) == len(pts)


def gen_points(rng, n, shape):
    while True:
        P = set()
        while len(P) < n:
            if shape == "box":
                p = (rng.randint(-60, 60), rng.randint(-60, 60))
            elif shape == "parab":  # near a convex curve with noise: many large convex subsets
                t = rng.randint(-25, 25)
                p = (t * 4 + rng.randint(-1, 1), t * t // 3 + rng.randint(-6, 6))
            elif shape == "clusters":  # few tight clusters: small convex subsets
                c = rng.choice([(-200, 0), (200, 10), (0, 300), (5, -250)])
                p = (c[0] + rng.randint(-8, 8), c[1] + rng.randint(-8, 8))
            else:
                raise ValueError(shape)
            P.add(p)
        P = list(P)
        if len({p[0] for p in P}) < n:
            continue
        if any(orient(*t) == 0 for t in itertools.combinations(P, 3)):
            continue
        return P


def least_fixpoint_violated(P, k):
    n = len(P)
    B = lambda x, c: P[x][0] < P[c][0]
    ccw = lambda a, b, c: orient(P[a], P[b], P[c]) > 0
    Y = {(x, b, c) for x in range(n) for b in range(n) for c in range(n)
         if len({x, b, c}) == 3 and B(x, c) and ccw(x, b, c)}
    W = {(x, a, b) for (x, a, b) in Y if B(x, a)}
    for r in range(2, k - 1):
        nxt = set()
        viol = False
        for (x, a, b) in W:
            for c in range(n):
                if c in (x, a, b):
                    continue
                if (x, b, c) in Y and ccw(a, b, c):
                    if r + 1 <= k - 2:
                        nxt.add((x, b, c))
                    else:
                        viol = True
        if r == k - 2:
            return viol
        W = nxt
    raise AssertionError("k too small")


def all_chains(P, k):
    """every x | p1..p(k-1) satisfying the chain conditions (right of x, consecutive ccw about x,
    left turns at p2..p(k-2))."""
    n = len(P)
    B = lambda x, c: P[x][0] < P[c][0]
    ccw = lambda a, b, c: orient(P[a], P[b], P[c]) > 0
    out = []
    def dfs(x, seq):
        if len(seq) == k - 1:
            out.append((x,) + tuple(seq))
            return
        for c in range(n):
            if c == x or c in seq[-2:]:
                continue
            if not B(x, c):
                continue
            if seq:
                if not ccw(x, seq[-1], c):
                    continue
                if len(seq) >= 2 and not ccw(seq[-2], seq[-1], c):
                    continue
            dfs(x, seq + [c])
    for x in range(n):
        dfs(x, [])
    return out


def has_convex_kset(P, k):
    return any(convex_position([P[i] for i in S]) for S in itertools.combinations(range(len(P)), k))


def main():
    seed, trials = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    stats = {"sets": 0, "with_kgon": 0, "kgon_free": 0, "chains_checked": 0,
             "fail_sound": 0, "fail_complete": 0, "fail_chain_not_convex": 0}
    for t in range(trials):
        shape = rng.choice(["box", "box", "parab", "clusters"])
        n = rng.randint(7, 12)
        k = rng.randint(4, 7)
        P = gen_points(rng, n, shape)
        viol = least_fixpoint_violated(P, k)
        real = has_convex_kset(P, k)
        stats["sets"] += 1
        stats["with_kgon" if real else "kgon_free"] += 1
        if viol and not real:
            stats["fail_sound"] += 1
            print("SOUNDNESS FAIL", shape, n, k, P)
        if real and not viol:
            stats["fail_complete"] += 1
            print("COMPLETENESS FAIL", shape, n, k, P)
        ch = all_chains(P, k)
        if bool(ch) != viol:
            print("DFS/fixpoint disagreement", shape, n, k, P)
            stats["fail_sound"] += 1
        for c in ch:
            stats["chains_checked"] += 1
            pts = [P[i] for i in c]
            h = hull_ccw(pts)
            ok = len(h) == k
            if ok:  # the chain order must be the ccw hull order (cyclic rotation of h)
                j = h.index(0)
                ok = h[j:] + h[:j] == list(range(k))
            if not ok:
                stats["fail_chain_not_convex"] += 1
                print("CHAIN NOT A CONVEX k-GON", shape, n, k, c, P)
    print(stats)


if __name__ == "__main__":
    main()
