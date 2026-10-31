#!/usr/bin/env python3
"""Independent review library for sgn.py (exact integer arithmetic only; no code imported from sgn/).

Conventions (my own, re-derived):
  det(a,b,c) = (b-a) x (c-a); orientation of (a,b,c) is 'left' iff det > 0.
  A labelled configuration is a list S with S[i-1] = p_i, labels 1..n.
"""
import functools, itertools, random

ORIGIN = (0, 0)


def det(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def neg(p):
    return (-p[0], -p[1])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def general_position(P):
    return all(det(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))


def symmetric(P):
    s = set(P)
    return len(s) == len(P) and all(neg(p) in s for p in P) and ORIGIN not in s


def hull_ccw(P):
    """Jarvis march (independent of the monotone-chain code in sgn/). General position assumed; verified."""
    start = min(P)
    H = [start]
    cur = start
    while True:
        cand = None
        for q in P:
            if q == cur:
                continue
            if cand is None or det(cur, cand, q) < 0:
                cand = q
        if cand == start:
            break
        H.append(cand)
        cur = cand
        assert len(H) <= len(P)
    h = len(H)
    for e in range(h):
        a, b = H[e], H[(e + 1) % h]
        for q in P:
            if q != a and q != b:
                assert det(a, b, q) > 0, "hull check failed"
    return H


def max_convex(P):
    """Size of the largest subset in convex position (>=3 points), O(n^4) angular DP around the lexicographic minimum
    vertex. Independent of cups/caps."""
    pts = sorted(P)
    best = min(len(P), 2)
    for ai, a in enumerate(pts):
        rest = pts[ai + 1:]
        rest.sort(key=functools.cmp_to_key(lambda p, q: -1 if det(a, p, q) > 0 else 1))
        m = len(rest)
        f = [[0] * m for _ in range(m)]
        for j in range(m):
            rj = rest[j]
            for i in range(j):
                ri = rest[i]
                assert det(a, ri, rj) > 0
                v = 3
                for p in range(i):
                    if f[p][i] and det(rest[p], ri, rj) > 0 and f[p][i] + 1 > v:
                        v = f[p][i] + 1
                f[i][j] = v
                if det(ri, rj, a) > 0 and v > best:
                    best = v
    return best


def in_convex_position(Q):
    return len(hull_ccw(list(Q))) == len(Q)


def max_convex_brute(P):
    best = min(len(P), 2)
    for k in range(3, len(P) + 1):
        if any(in_convex_position(Q) for Q in itertools.combinations(P, k)):
            best = k
    return best


# ---------------------------------------------------------------- normal forms

def par_normal_form(P, rs=True, choice=0):
    """--par normal form. P: centrally symmetric (about the origin), general position, hull = parallelogram.
    Returns (S, info): S[i-1] = p_i sorted by d = M*nu + t (a genuine direction, M large => lexicographic (nu.p, t.p)),
    nu = outward normal of the chosen CCW hull edge V1->V2, t = V2 - V1 (tilt towards V2).
    rs: choose among edges whose diagonal class holds >= ceil(m/2) inner pairs; `choice` selects among those."""
    H = hull_ccw(P)
    assert len(H) == 4, len(H)
    hs = set(H)
    inner = [p for p in P if p not in hs]
    reps = [q for q in inner if q > neg(q)]
    m = len(reps)

    def cls(A, B):  # pairs with a point in the open sector from ray cA to ray cB (c = origin)
        return sum(1 for q in reps if (cross(A, q) > 0) == (cross(q, B) > 0))

    edges = [(H[e], H[(e + 1) % 4]) for e in range(4)]
    good = [e for e in edges if cls(*e) >= (m + 1) // 2] if rs else edges
    V1, V2 = good[choice % len(good)]
    t = (V2[0] - V1[0], V2[1] - V1[1])
    nu = (t[1], -t[0])
    top = dot(nu, V1)
    assert dot(nu, V2) == top
    for p in P:
        if p not in (V1, V2):
            assert dot(nu, p) < top
    M = 2 * max(abs(dot(t, p)) for p in P) + 1
    d = (M * nu[0] + t[0], M * nu[1] + t[1])
    S = sorted(P, key=lambda p: dot(d, p))
    keys = [dot(d, p) for p in S]
    assert len(set(keys)) == len(keys), "d-values not distinct"
    # lexicographic equivalence
    assert S == sorted(P, key=lambda p: (dot(nu, p), dot(t, p)))
    n = len(S)
    assert S[-1] == V2 and S[-2] == V1 and S[0] == neg(V2) and S[1] == neg(V1)
    assert all(S[n - 1 - i] == neg(S[i]) for i in range(n))
    return S, {"V1": V1, "V2": V2, "nu": nu, "t": t, "d": d, "m": m, "class": cls(V1, V2),
               "ngood": len(good), "edges_cls": [cls(*e) for e in edges]}


def x_normal_form(P):
    """plain --sym labelling: sorted by a direction with distinct values (lexicographic x, y)."""
    M = 2 * max(abs(p[1]) for p in P) + 1
    d = (M, 1)
    S = sorted(P, key=lambda p: dot(d, p))
    keys = [dot(d, p) for p in S]
    assert len(set(keys)) == len(keys)
    n = len(S)
    assert all(S[n - 1 - i] == neg(S[i]) for i in range(n))
    return S


# ---------------------------------------------------------------- generators

def rand_par_set(rng, m, R=1000, spread=None, A=None, B=None, inner_fn=None):
    """Centrally symmetric set with parallelogram hull +-(A+B)*R, +-(B-A)*R  (image of the square [-R,R]^2 under the
    linear map with columns A, B, det > 0) and m inner pairs (u,v) in (-R,R)^2 mapped by the same linear map.
    Returns None if the result is not in general position."""
    if A is None:
        while True:
            A = (rng.randint(-9, 9), rng.randint(-9, 9))
            B = (rng.randint(-9, 9), rng.randint(-9, 9))
            if cross(A, B) > 0:
                break
    L = lambda u, v: (u * A[0] + v * B[0], u * A[1] + v * B[1])
    P = [L(R, R), L(-R, R), L(-R, -R), L(R, -R)]
    uv = []
    for _ in range(m):
        if inner_fn is not None:
            u, v = inner_fn(rng, R)
        else:
            s = spread or R - 1
            u, v = rng.randint(-s, s), rng.randint(-s, s)
        uv.append((u, v))
        P += [L(u, v), L(-u, -v)]
    if len(set(P)) != len(P) or ORIGIN in P or not general_position(P):
        return None
    return P


def reflect(P):
    return [(-x, y) for x, y in P]


# ---------------------------------------------------------------- orientation of a labelled configuration

def orient_table(S):
    n = len(S)
    return {t: det(S[t[0] - 1], S[t[1] - 1], S[t[2] - 1]) > 0 for t in itertools.combinations(range(1, n + 1), 3)}


def chi_real(S, a, b, c):
    return det(S[a - 1], S[b - 1], S[c - 1]) > 0


def exact_cups(o, n, K):
    """cup[(k,a,j,l)] = True iff there is an exact k-cup a=c1<...<c_{k-1}=j<c_k=l (consecutive triples left turns)."""
    cup = {}
    for (a, j, l) in itertools.combinations(range(1, n + 1), 3):
        if o[(a, j, l)]:
            cup[(3, a, j, l)] = True
    for k in range(4, K + 1):
        for (a, i, j, l) in itertools.combinations(range(1, n + 1), 4):
            if cup.get((k - 1, a, i, j)) and o[(i, j, l)]:
                cup[(k, a, j, l)] = True
    return cup


def exact_cups_brute(o, n, K):
    cup = {}
    for k in range(3, K + 1):
        for c in itertools.combinations(range(1, n + 1), k):
            if all(o[(c[x], c[x + 1], c[x + 2])] for x in range(k - 2)):
                cup[(k, c[0], c[-2], c[-1])] = True
    return cup
