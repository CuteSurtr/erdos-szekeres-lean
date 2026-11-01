"""Independent exact geometry for the check of Proposition 8 (written from scratch; imports nothing from tools/).
All coordinates are int or fractions.Fraction; no floating point is used in any decision."""
from fractions import Fraction as F
from itertools import combinations


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sgn(x):
    return (x > 0) - (x < 0)


def general_position(P):
    return all(orient(a, b, c) != 0 for a, b, c in combinations(P, 3))


def hull(P):
    """Andrew monotone chain, strict (collinear points dropped). Returns CCW list of vertices."""
    Q = sorted(set(P))
    if len(Q) <= 2:
        return Q
    lo, up = [], []
    for p in Q:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(Q):
        while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def convex_position(Y):
    return len(hull(Y)) == len(Y)


def convex_position_tri(Y):
    """Second, independent test: no point in a closed triangle of three others (general position assumed)."""
    Y = list(Y)
    for t in combinations(range(len(Y)), 3):
        a, b, c = (Y[i] for i in t)
        o = sgn(orient(a, b, c))
        for j in range(len(Y)):
            if j in t:
                continue
            q = Y[j]
            if sgn(orient(a, b, q)) == o and sgn(orient(b, c, q)) == o and sgn(orient(c, a, q)) == o:
                return False
    return True


def gon(P):
    """Largest subset in convex position, exact O(n^4)-ish DP: for each choice of the lowest vertex p
    (lexicographically smallest by (y, x)), points above it sorted by angle; dp over last edge."""
    P = list(P)
    n = len(P)
    if n <= 2:
        return n
    best = 2
    for p in P:
        above = [q for q in P if (q[1], q[0]) > (p[1], p[0])]
        # sort by angle around p: all in the half-plane above p (or same y, right of p); comparator by orient
        import functools

        def cmp(a, b):
            o = orient(p, a, b)
            return -1 if o > 0 else (1 if o < 0 else 0)

        above.sort(key=functools.cmp_to_key(cmp))
        m = len(above)
        # dp[i][j] = max #vertices of a convex chain p -> ... -> above[i] -> above[j] (CCW, all left turns)
        dp = [[0] * m for _ in range(m)]
        for j in range(m):
            for i in range(j):
                dp[i][j] = 3  # p, above[i], above[j]  (angle order guarantees left turn at p .. i .. j? checked below)
        # validity of the triangle p, i, j requires orient(p, i, j) > 0, true since i before j in angle order
        for j in range(m):
            for i in range(j):
                if dp[i][j] == 0:
                    continue
                for k in range(j + 1, m):
                    if orient(above[i], above[j], above[k]) > 0 and dp[i][j] + 1 > dp[j][k]:
                        dp[j][k] = dp[i][j] + 1
        for j in range(m):
            for i in range(j):
                # close the polygon: turn at above[j] towards p must be left: orient(i, j, p) > 0
                if dp[i][j] and orient(above[i], above[j], p) > 0:
                    best = max(best, dp[i][j])
    return best


def gon_bruteforce_ge(P, k):
    """True iff some k-subset is in convex position (exhaustive)."""
    return any(convex_position(Y) for Y in combinations(P, k))


def max_cap_xsorted(P):
    """Largest cap (upper convex chain) of a set with distinct x-coordinates: DP over last edge."""
    Q = sorted(P)
    assert len(set(q[0] for q in Q)) == len(Q)
    m = len(Q)
    if m <= 2:
        return m
    dp = [[2] * m for _ in range(m)]
    best = 2
    for j in range(m):
        for i in range(j):
            for k in range(j + 1, m):
                if orient(Q[i], Q[j], Q[k]) < 0 and dp[i][j] + 1 > dp[j][k]:
                    dp[j][k] = dp[i][j] + 1
                    best = max(best, dp[j][k])
    return best


def is_cap_xsorted(Y):
    Y = sorted(Y)
    return all(orient(Y[i], Y[j], Y[k]) < 0 for i, j, k in combinations(range(len(Y)), 3))


def is_cup_xsorted(Y):
    Y = sorted(Y)
    return all(orient(Y[i], Y[j], Y[k]) > 0 for i, j, k in combinations(range(len(Y)), 3))


def v_order_key(v):
    import functools

    def cmp(a, b):
        o = orient(v, a, b)
        # p <_v q iff orient(v,p,q) < 0  (q clockwise from p seen from v)
        return -1 if o < 0 else (1 if o > 0 else 0)

    return functools.cmp_to_key(cmp)


def is_v_cap(Y, v):
    """Direct definition in the v-frame: sort by <_v; every middle point strictly on the side of the
    chord opposite to v."""
    Y = sorted(Y, key=v_order_key(v))
    for i, j, k in combinations(range(len(Y)), 3):
        a, b, c = Y[i], Y[j], Y[k]
        if sgn(orient(a, c, b)) == sgn(orient(a, c, v)):
            return False
        if orient(a, c, b) == 0 or orient(a, c, v) == 0:
            return False
    return True


def is_v_cup(Y, v):
    Y = sorted(Y, key=v_order_key(v))
    for i, j, k in combinations(range(len(Y)), 3):
        a, b, c = Y[i], Y[j], Y[k]
        if sgn(orient(a, c, b)) != sgn(orient(a, c, v)) or orient(a, c, v) == 0:
            return False
    return True


def phi_map(T, v, n):
    """Projective map sending v to the vertical point at infinity (my own normalisation, written
    independently): with w(p) = n.(p - v) > 0 and u = (-n_y, n_x),
       phi(p) = ( -u.(p - v) / w(p),  -1 / w(p) ).
    Returns dict p -> phi(p) (Fractions)."""
    u = (-n[1], n[0])
    out = {}
    for p in T:
        d = (p[0] - v[0], p[1] - v[1])
        w = n[0] * d[0] + n[1] * d[1]
        assert w > 0, "n does not separate v from T"
        out[p] = (F(-(u[0] * d[0] + u[1] * d[1]), w), F(-1, w))
    return out


def separating_normal(T, v, tries=2000, seed=1):
    """Find an integer vector n with n.(p - v) > 0 for all p in T (exists iff v not in conv(T))."""
    import random
    rng = random.Random(seed)
    # first try the sum of directions to the two hull neighbours of v in T u {v}
    H = hull(list(T) + [v])
    if v in H:
        i = H.index(v)
        a, b = H[i - 1], H[(i + 1) % len(H)]
        # inward normals of the two hull edges at v (hull is CCW): their sum is strictly positive on T
        L1 = (-(b[1] - v[1]), b[0] - v[0])
        L2 = (-(v[1] - a[1]), v[0] - a[0])
        n = (L1[0] + L2[0], L1[1] + L2[1])
        if all(n[0] * (p[0] - v[0]) + n[1] * (p[1] - v[1]) > 0 for p in T):
            return n
    for _ in range(tries):
        n = (rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6))
        if all(n[0] * (p[0] - v[0]) + n[1] * (p[1] - v[1]) > 0 for p in T):
            return n
    return None
