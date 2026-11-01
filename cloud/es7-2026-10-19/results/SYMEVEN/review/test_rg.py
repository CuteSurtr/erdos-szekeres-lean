"""Validate rg.py's DPs against brute force on random point sets in general position."""
import random, sys
from itertools import combinations
from rg import (orient, collinear_triples, max_convex_bf, max_convex_cupcap, max_convex_angular,
                count_convex_bf, count_convex_cupcap, longest_cup_cap, convex_position_bf)


def bf_cup_cap(pts):
    P = sorted(pts)
    bc = bk = min(len(P), 2)
    for s in range(3, len(P) + 1):
        for sub in combinations(P, s):
            t = [orient(sub[i - 1], sub[i], sub[i + 1]) for i in range(1, s - 1)]
            if all(v > 0 for v in t):
                bc = max(bc, s)
            if all(v < 0 for v in t):
                bk = max(bk, s)
    return bc, bk


def rand_set(rng, n, mode):
    while True:
        if mode == 0:
            pts = [(rng.randint(-60, 60), rng.randint(-60, 60)) for _ in range(n)]
        elif mode == 1:   # points near a convex curve (many large convex subsets)
            pts = []
            for _ in range(n):
                x = rng.randint(-40, 40)
                pts.append((x, x * x + rng.randint(-30, 30)))
        else:             # clustered
            pts = []
            centers = [(rng.randint(-1000, 1000), rng.randint(-1000, 1000)) for _ in range(3)]
            for _ in range(n):
                c = rng.choice(centers)
                pts.append((c[0] + rng.randint(-20, 20), c[1] + rng.randint(-20, 20)))
        if len(set(pts)) < n or len(set(p[0] for p in pts)) < n:
            continue
        if collinear_triples(pts):
            continue
        return pts


def main(trials, seed):
    rng = random.Random(seed)
    fails = 0
    for t in range(trials):
        n = rng.randint(3, 11)
        pts = rand_set(rng, n, t % 3)
        mb, _ = max_convex_bf(pts)
        m1, w1 = max_convex_cupcap(pts)
        m2 = max_convex_angular(pts)
        ok = (mb == m1 == m2) and len(w1) == m1 and convex_position_bf(w1)
        if n <= 10:
            cb = count_convex_bf(pts)
            cd = count_convex_cupcap(pts)
            cb = {s: c for s, c in cb.items() if c}
            ok = ok and (cb == cd)
        lc = longest_cup_cap(pts)
        ok = ok and (lc == bf_cup_cap(pts))
        if not ok:
            fails += 1
            print("FAIL", pts, mb, m1, m2)
    print("trials=%d seed=%d failures=%d" % (trials, seed, fails))


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
