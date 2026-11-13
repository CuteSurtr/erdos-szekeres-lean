#!/usr/bin/env python3
"""Independent checks for signotopes (abstract x-sorted point sets).

sig is a dict {(i,j,k): +1/-1} for 1<=i<j<k<=N.

* is_signotope: every quadruple's (ijk, ijl, ikl, jkl) has at most one sign change.
* convex subsets (method A, '4-point test', independent of caps/cups): a set is in convex position
  iff no point lies inside a triangle of three others, where d is inside abc iff
  O(a,b,d) = O(b,c,d) = O(c,a,d) with O the orientation extended to all orderings by permutation parity.
  max_convex_4pt does an exact DFS (subsets of convex sets are convex, so pruning is exact).
* method B, cap/cup DP: largest cap+cup with common endpoints (Szekeres-Peters model).
* brute force over all K-subsets (method C) is in brute_kgon.c.
"""
import itertools
import sys


def orient_fn(sig):
    def O(a, b, c):
        t = (a, b, c)
        s = sorted(t)
        # parity of permutation t -> sorted
        inv = (a > b) + (a > c) + (b > c)
        v = sig[tuple(s)]
        return v if inv % 2 == 0 else -v
    return O


def is_signotope(sig, N):
    for i, j, k, l in itertools.combinations(range(1, N + 1), 4):
        seq = [sig[(i, j, k)], sig[(i, j, l)], sig[(i, k, l)], sig[(j, k, l)]]
        changes = sum(1 for t in range(3) if seq[t] != seq[t + 1])
        if changes > 1:
            return False, (i, j, k, l)
    return True, None


def inside(O, d, a, b, c):
    o1 = O(a, b, d)
    return o1 == O(b, c, d) == O(c, a, d)


def convex_4pt(O, pts):
    for q in itertools.combinations(pts, 4):
        for idx in range(4):
            d = q[idx]
            a, b, c = [q[t] for t in range(4) if t != idx]
            if inside(O, d, a, b, c):
                return False
    return True


def count_convex_4pt(sig, N, K, stop_at=None):
    """Number of K-subsets in convex position (4-point test), DFS with exact pruning."""
    O = orient_fn(sig)
    count = 0
    best = 0

    def ok_add(cur, p):
        # new 4-subsets all contain p
        for a, b, c in itertools.combinations(cur, 3):
            if inside(O, p, a, b, c) or inside(O, a, b, c, p) or inside(O, b, a, c, p) or inside(O, c, a, b, p):
                return False
        return True

    def dfs(cur, start):
        nonlocal count, best
        if len(cur) > best:
            best = len(cur)
        if len(cur) == K:
            count += 1
            return stop_at is not None and count >= stop_at
        for p in range(start, N + 1):
            if N - p + 1 < K - len(cur):
                break
            if ok_add(cur, p):
                cur.append(p)
                if dfs(cur, p + 1):
                    return True
                cur.pop()
        return False

    dfs([], 1)
    return count


def max_convex_4pt(sig, N):
    O = orient_fn(sig)
    best = 0

    def ok_add(cur, p):
        for a, b, c in itertools.combinations(cur, 3):
            if inside(O, p, a, b, c) or inside(O, a, b, c, p) or inside(O, b, a, c, p) or inside(O, c, a, b, p):
                return False
        return True

    def dfs(cur, start):
        nonlocal best
        best = max(best, len(cur))
        for p in range(start, N + 1):
            if len(cur) + (N - p + 1) <= best:
                break
            if ok_add(cur, p):
                cur.append(p)
                dfs(cur, p + 1)
                cur.pop()

    dfs([], 1)
    return best


def max_convex_capcup(sig, N):
    """Method B: max over x<y of (longest cap x..y) + (longest cup x..y) - 2 (and >= min(N,2))."""
    best = min(N, 2)
    # L[s][a][b] longest chain of sign s starting at x ending with (a,b) computed per x
    for x in range(1, N + 1):
        for s in (+1, -1):
            pass
    for x in range(1, N + 1):
        capd = {}
        cupd = {}
        for b in range(x + 1, N + 1):
            capd[(x, b)] = 2
            cupd[(x, b)] = 2
        for a in range(x + 1, N + 1):
            for b in range(a + 1, N + 1):
                bc = 0
                bu = 0
                for w in range(x, a):
                    if sig[(w, a, b)] < 0:
                        if (w, a) in capd:
                            bc = max(bc, capd[(w, a)] + 1)
                    else:
                        if (w, a) in cupd:
                            bu = max(bu, cupd[(w, a)] + 1)
                if bc:
                    capd[(a, b)] = bc
                if bu:
                    cupd[(a, b)] = bu
        for y in range(x + 1, N + 1):
            lc = max(v for (a, b), v in capd.items() if b == y)
            lu = max(v for (a, b), v in cupd.items() if b == y)
            best = max(best, lc + lu - 2)
    return best


def read_model(path, nX):
    vals = {}
    sat = None
    with open(path) as f:
        for line in f:
            if line.startswith("s "):
                sat = line.strip()
            if line.startswith("v "):
                for t in line.split()[1:]:
                    v = int(t)
                    if v != 0:
                        vals[abs(v)] = v > 0
    return sat, vals


def model_to_sig(vals, N):
    sig = {}
    idx = 0
    for t in itertools.combinations(range(1, N + 1), 3):
        idx += 1
        sig[t] = 1 if vals.get(idx, False) else -1
    return sig


if __name__ == "__main__":
    N, K, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    from math import comb
    sat, vals = read_model(path, comb(N, 3))
    print("status:", sat)
    sig = model_to_sig(vals, N)
    ok, bad = is_signotope(sig, N)
    print("signotope axioms:", ok, bad)
    print("max convex (4-point DFS):", max_convex_4pt(sig, N))
    print("max convex (cap/cup DP):", max_convex_capcup(sig, N))
    print(f"#convex {K}-subsets (4-point DFS):", count_convex_4pt(sig, N, K))
    hull = all(sig[(1, i, j)] > 0 for i, j in itertools.combinations(range(2, N + 1), 2))
    print("X(1,i,j)=+ for all i<j:", hull)
    with open(path + ".sig", "w") as f:
        for t in itertools.combinations(range(1, N + 1), 3):
            f.write(f"{t[0]} {t[1]} {t[2]} {sig[t]}\n")
