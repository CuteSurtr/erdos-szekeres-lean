#!/usr/bin/env python3
"""Randomized exact-arithmetic test of the GEOMETRIC steps of the chord-lemma proof, on arbitrary
configurations (no heptagon-freeness needed).  Independent code (does not import tools/ of this result).

U1 (core of the lemma): H convex hexagon (ccw), i, m in {1,2,3}, a=h_i, b=h_{i+m+1},
    q_1..q_{m+1} in the open region R(i,m) with {a,b,q's} in convex position
    ==> kept vertices u {q's} (7 points) are in convex position.
U2 (corollary, region description): for p in general position w.r.t. H (p not a vertex),
    p in R(j-1,1)  <=>  p in open ear triangle h_{j-1}h_jh_{j+1}
                        or vis(p) in { {e_{j-1}}, {e_j}, {e_{j-1},e_j} }.
U3 p sees exactly one edge of H ==> H u {p} in convex position (7 points).
U4 for p,q strictly on one side of line ab: {a,b,p,q} not convex <=> exactly one of
    p in int T(a,b,q), q in int T(a,b,p).
U5 visible edges of an outside point form one nonempty contiguous proper chain.
"""
import random
import sys
from itertools import combinations


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def strictly_inside(p, a, b, c):
    o = orient(a, b, c)
    s1, s2, s3 = orient(a, b, p), orient(b, c, p), orient(c, a, p)
    if o > 0:
        return s1 > 0 and s2 > 0 and s3 > 0
    return s1 < 0 and s2 < 0 and s3 < 0


def gift_wrap(P):
    """ccw hull by Jarvis march (points in general position)."""
    start = min(P)
    hull = []
    cur = start
    while True:
        hull.append(cur)
        nxt = P[0] if P[0] != cur else P[1]
        for p in P:
            if p != cur and orient(cur, nxt, p) < 0:
                nxt = p
        cur = nxt
        if cur == start:
            break
    return hull


def general_position(P):
    return len(set(P)) == len(P) and all(orient(a, b, c) != 0 for a, b, c in combinations(P, 3))


def convex_position(P):
    """General position assumed: convex iff hull contains all points."""
    if len(P) <= 3:
        return True
    return len(gift_wrap(P)) == len(P)


def random_convex_hexagon(rng, R):
    while True:
        style = rng.random()
        if style < 0.5:
            P = [(rng.randint(-R, R), rng.randint(-R, R)) for _ in range(rng.randint(8, 40))]
        else:  # skinny / stretched configurations
            sx, sy = rng.randint(1, R), rng.randint(1, max(1, R // rng.choice([1, 10, 100, 1000])))
            P = [(rng.randint(-sx, sx), rng.randint(-sy, sy)) for _ in range(rng.randint(8, 40))]
        P = list(set(P))
        if len(P) < 6 or not general_position(P):
            continue
        Hh = gift_wrap(P)
        if len(Hh) < 6:
            continue
        idx = sorted(rng.sample(range(len(Hh)), 6))
        H = [Hh[t] for t in idx]
        return H


def region_pred(H, i, m):
    a, b = H[i], H[(i + m + 1) % 6]
    hm1, hb1 = H[(i - 1) % 6], H[(i + m + 2) % 6]

    def inR(p):
        return orient(a, b, p) < 0 and orient(hm1, a, p) > 0 and orient(b, hb1, p) > 0
    return a, b, inR


def sample_region_points(rng, H, inR, k, box, near_boundary_lines=None):
    pts = []
    tries = 0
    while len(pts) < k and tries < 20000:
        tries += 1
        if near_boundary_lines and rng.random() < 0.5:
            # sample near a point on a boundary line, then perturb
            (u, v) = rng.choice(near_boundary_lines)
            t = rng.random() * rng.choice([0.5, 2, 10])
            base = (u[0] + t * (v[0] - u[0]), u[1] + t * (v[1] - u[1]))
            eps = rng.choice([1, 3, 10, 100, 1000])
            p = (int(round(base[0])) + rng.randint(-eps, eps), int(round(base[1])) + rng.randint(-eps, eps))
        else:
            p = (rng.randint(-box, box), rng.randint(-box, box))
        if p in H or p in pts:
            continue
        if inR(p):
            pts.append(p)
    return pts


def vis_edges(H, p):
    return tuple(t for t in range(6) if orient(H[t], H[(t + 1) % 6], p) < 0)


def contiguous(vis):
    s = set(vis)
    if not s or len(s) == 6:
        return False
    starts = [t for t in s if (t - 1) % 6 not in s]
    return len(starts) == 1


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    ntrials = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    rng = random.Random(seed)
    Rr = 10 ** 6
    stats = dict(U1_checked=0, U1_viol=0, U1_degenerate_skipped=0, U2_checked=0, U2_viol=0, U3_checked=0, U3_viol=0,
                 U4_checked=0, U4_viol=0, U5_checked=0, U5_viol=0, U1_by_m={1: 0, 2: 0, 3: 0})
    for trial in range(ntrials):
        H = random_convex_hexagon(rng, Rr)
        assert all(orient(H[t], H[(t + 1) % 6], H[(t + 2) % 6]) > 0 for t in range(6))
        box = 4 * max(max(abs(x), abs(y)) for x, y in H) + 10
        i = rng.randrange(6)
        m = rng.choice([1, 2, 3])
        a, b, inR = region_pred(H, i, m)
        kept = [H[(i + m + 1 + t) % 6] for t in range(6 - m)]
        lines = [(H[(i - 1) % 6], H[i]), (H[(i + m + 1) % 6], H[(i + m + 2) % 6]), (a, b)]
        Q = sample_region_points(rng, H, inR, rng.randint(m + 1, m + 7), box, near_boundary_lines=lines)
        # U1: all (m+1)-subsets in convex position with a, b
        for qs in combinations(Q, m + 1):
            pts = [a, b] + list(qs)
            allp = kept + list(qs)
            if not general_position(list(set(H) | set(qs))):
                stats["U1_degenerate_skipped"] += 1
                continue
            if convex_position(pts):
                stats["U1_checked"] += 1
                stats["U1_by_m"][m] += 1
                if not convex_position(allp):
                    stats["U1_viol"] += 1
                    print("U1 VIOLATION", H, i, m, qs)
        # U2/U3/U5: random p
        for _ in range(30):
            if rng.random() < 0.5:
                p = (rng.randint(-box, box), rng.randint(-box, box))
            else:
                (u, v) = rng.choice([(H[t], H[(t + 1) % 6]) for t in range(6)] + [(H[t], H[(t + 2) % 6]) for t in range(6)])
                t = rng.random() * 3 - 1
                p = (int(round(u[0] + t * (v[0] - u[0]))) + rng.randint(-50, 50),
                     int(round(u[1] + t * (v[1] - u[1]))) + rng.randint(-50, 50))
            if p in H or not general_position(H + [p]):
                continue
            vis = vis_edges(H, p)
            for j in range(6):
                _, _, inR1 = region_pred(H, (j - 1) % 6, 1)
                lhs = inR1(p)
                ear = strictly_inside(p, H[(j - 1) % 6], H[j], H[(j + 1) % 6])
                rhs = ear or (set(vis) in ({(j - 1) % 6}, {j}, {(j - 1) % 6, j}))
                stats["U2_checked"] += 1
                if lhs != rhs:
                    stats["U2_viol"] += 1
                    print("U2 VIOLATION", H, j, p, vis)
            inside_H = all(orient(H[t], H[(t + 1) % 6], p) > 0 for t in range(6))
            if not inside_H:
                stats["U5_checked"] += 1
                if not contiguous(vis):
                    stats["U5_viol"] += 1
                    print("U5 VIOLATION", H, p, vis)
            if len(vis) == 1:
                stats["U3_checked"] += 1
                if not convex_position(H + [p]):
                    stats["U3_viol"] += 1
                    print("U3 VIOLATION", H, p, vis)
        # U4
        for _ in range(20):
            a2, b2 = rng.sample(H, 2)
            p = (rng.randint(-box, box), rng.randint(-box, box))
            q = (rng.randint(-box, box), rng.randint(-box, box))
            if len({a2, b2, p, q}) < 4 or not general_position([a2, b2, p, q]):
                continue
            if (orient(a2, b2, p) > 0) != (orient(a2, b2, q) > 0):
                continue
            stats["U4_checked"] += 1
            nonconv = not convex_position([a2, b2, p, q])
            x1, x2 = strictly_inside(p, a2, b2, q), strictly_inside(q, a2, b2, p)
            if nonconv != ((x1 + x2) == 1) or (x1 and x2):
                stats["U4_viol"] += 1
                print("U4 VIOLATION", a2, b2, p, q)
    print("seed", seed, "trials", ntrials, stats)


if __name__ == "__main__":
    main()
