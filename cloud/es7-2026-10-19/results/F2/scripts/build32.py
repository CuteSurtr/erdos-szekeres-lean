#!/usr/bin/env python3
"""Deep-below construction: S (26 integer points, no 5-cap, no 7-cup, no convex 7-gon; cup = ccw
x-sorted triple, the gen_etv.py convention) plus a 6-point cap T placed deep below S.
Lemma (plan/es7_plan.md): if T is deep below S, a subset meeting both is convex iff its T-part is a
cup and its S-part is a cap, so its size is <= cup(T) + cap(S) = 2 + 4 = 6; T alone has 6 points.
T_i = (x0 + w*i, -M - i^2), i = -3..2 (a cap), w = x-range of S (flat T).  M is chosen so that every point of T is strictly below
every line through two points of S, and every point of S is strictly above every line through two
points of T; both conditions are then re-checked exactly, and the caller re-checks the whole set.
usage: build32.py S.pts OUT.pts   (prints JSON)"""
import itertools, json, sys

def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def below_all(S, z):
    # z strictly below line(p,q) for p.x < q.x  <=>  orient(p, q, z) < 0 (needs distinct x in S)
    return all(orient(p, q, z) < 0 for p, q in itertools.combinations(sorted(S), 2))

def build(S):
    xs = [p[0] for p in S]
    assert len(set(xs)) == len(xs), "distinct x needed"
    x0 = (min(xs) + max(xs)) // 2
    w = max(1, max(xs) - min(xs))
    T_of = lambda M: [(x0 + w * i, -M - i * i) for i in range(-3, 3)]
    def good(M):
        T = T_of(M)
        return (all(below_all(S, z) for z in T) and
                all(orient(p, q, s) > 0 for p, q in itertools.combinations(sorted(T), 2) for s in S))
    lo, hi = 1, 1
    while not good(hi):
        hi *= 2
    lo = hi // 2
    while hi - lo > 1:   # smallest working M by bisection (keeps coordinates small)
        mid = (lo + hi) // 2
        if good(mid): hi = mid
        else: lo = mid
    return T_of(hi), hi

if __name__ == "__main__":
    S = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
    if len(set(p[0] for p in S)) != len(S):
        L = 2 * max(abs(p[1]) for p in S) + 1
        S = [(L * x + y, y) for x, y in S]
    T, M = build(S)
    P = S + T
    with open(sys.argv[2], "w") as f:
        for x, y in P: f.write(f"{x} {y}\n")
    print(json.dumps({"M": M, "max_abs_coord": max(max(abs(x), abs(y)) for x, y in P)}))
