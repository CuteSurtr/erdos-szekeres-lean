"""Exact tools for integer point sets: orientation, general position, and the size of the largest
subset in convex position (O(n^4) dynamic program, anchored at the lowest point of the polygon)."""
from functools import cmp_to_key
from itertools import combinations


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def collinear_triples(P):
    return [(a, b, c) for a, b, c in combinations(range(len(P)), 3) if orient(P[a], P[b], P[c]) == 0]


def max_convex(P):
    """Largest number of points of P in convex position (P in general position, |P| >= 3)."""
    best = min(len(P), 2)
    for a in P:
        # points strictly above a in the (y, x) order: a is then the lowest vertex of the polygon
        up = [p for p in P if (p[1], p[0]) > (a[1], a[0])]
        # sort counterclockwise around a (all angles in [0, pi), so a cross-product comparison is a total order)
        up.sort(key=cmp_to_key(lambda p, q: -1 if orient(a, p, q) > 0 else 1))
        m = len(up)
        # D[i][j]: most vertices of a convex chain a -> ... -> up[i] -> up[j] (left turns only), i < j
        D = [[0] * m for _ in range(m)]
        for j in range(m):
            for i in range(j):
                v = 3 if orient(a, up[i], up[j]) > 0 else 0   # a -> up[i] -> up[j]
                if v:
                    for h in range(i):
                        if D[h][i] and orient(up[h], up[i], up[j]) > 0 and D[h][i] + 1 > v:
                            v = D[h][i] + 1
                D[i][j] = v
                # close: up[i] -> up[j] -> a must turn left
                if v and orient(up[i], up[j], a) > 0 and v > best:
                    best = v
    return best


def max_convex_brute(P):
    """Reference: largest k such that some k-subset is in convex position (small P only)."""
    def convex_position(S):
        for t in range(len(S)):
            others = S[:t] + S[t + 1:]
            for x, y, z in combinations(others, 3):
                o1, o2, o3 = orient(x, y, S[t]), orient(y, z, S[t]), orient(z, x, S[t])
                if (o1 > 0 and o2 > 0 and o3 > 0) or (o1 < 0 and o2 < 0 and o3 < 0):
                    return False
        return True
    best = min(len(P), 2)
    for k in range(3, len(P) + 1):
        if any(convex_position(list(S)) for S in combinations(P, k)):
            best = k
        else:
            break
    return best
