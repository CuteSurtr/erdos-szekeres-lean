"""Own implementation (review304-controls), written from the definitions in
ActualRanks.lean / BalancedStates.lean / Realization.lean:
  orient(a,b,c) = (b-a) x (c-a)  (Python ints, exact)
  cup(i,j,k) = orient(p_i,p_j,p_k) > 0 for i<j<k in x-order; cap = orient < 0
  rank(color,u,v) = max #points of an x-increasing chain ending with edge (u,v) whose consecutive
                    triples all have that color (EndingPath); 2 for the bare edge
  labels(u,v) = (rank_cap(u,v)-1, rank_cup(u,v)-1) = (capLabel, cupLabel)
  column(v,i) = max_{u<v} (cupLabel(u,v) if i+1 <= capLabel(u,v) else 0)   (0 if no u)
No project code is imported.
"""
import numpy as np


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sort_check(points):
    """Sort by x; return sorted list or None if x not distinct."""
    pts = sorted((int(x), int(y)) for x, y in points)
    for i in range(len(pts) - 1):
        if pts[i][0] == pts[i + 1][0]:
            return None
    return pts


def sign_tensor(pts):
    """S[i,j,k] in {+1,-1} for i<j<k (exact Python-int orientation); 0 elsewhere.
    Returns (S, ok) where ok=False if some triple is collinear."""
    n = len(pts)
    S = np.zeros((n, n, n), dtype=np.int8)
    ok = True
    for i in range(n):
        xi, yi = pts[i]
        for j in range(i + 1, n):
            xj, yj = pts[j]
            dx, dy = xj - xi, yj - yi
            row = S[i, j]
            for k in range(j + 1, n):
                xk, yk = pts[k]
                d = dx * (yk - yi) - dy * (xk - xi)
                if d > 0:
                    row[k] = 1
                elif d < 0:
                    row[k] = -1
                else:
                    ok = False
    return S, ok


def ranks(S, color):
    """R[u,v] (u<v) = max #points of a chain of the given color (+1 cup, -1 cap) ending with edge (u,v).
    Plain DP over the EndingPath definition: R[u,v] = max(2, max_{t<u, S[t,u,v]==color} R[t,u]+1)."""
    n = S.shape[0]
    R = np.zeros((n, n), dtype=np.int16)
    for u in range(n):
        R[u, u + 1:] = 2
        if u == 0:
            continue
        # contributions from t < u
        A = R[:u, u].astype(np.int16)  # R[t,u] (>=2 for t<u)
        M = (S[:u, u, :] == color)  # (t, v)
        cand = np.where(M, (A + 1)[:, None], 0).max(axis=0)
        R[u, u + 1:] = np.maximum(R[u, u + 1:], cand[u + 1:])
    return R


def ranks_pure(S, color):
    """Second, loop-only implementation of ranks (for cross-checking)."""
    n = S.shape[0]
    R = [[0] * n for _ in range(n)]
    for v in range(n):
        for u in range(v):
            best = 2
            for t in range(u):
                if S[t, u, v] == color and R[t][u] + 1 > best:
                    best = R[t][u] + 1
            R[u][v] = best
    return R


def states(S):
    """Return (list of 5-tuples f_v, max cap rank, max cup rank)."""
    n = S.shape[0]
    Rcap = ranks(S, -1)
    Rcup = ranks(S, +1)
    out = []
    for v in range(n):
        f = [0] * 5
        for u in range(v):
            capL = int(Rcap[u, v]) - 1
            cupL = int(Rcup[u, v]) - 1
            for i in range(5):
                if i + 1 <= capL and cupL > f[i]:
                    f[i] = cupL
        out.append(tuple(f))
    mcap = int(Rcap.max()) if n >= 2 else (1 if n == 1 else 0)
    mcup = int(Rcup.max()) if n >= 2 else (1 if n == 1 else 0)
    return out, mcap, mcup


def longest_chains(S, idx):
    """Longest cap and cup (number of points) inside the sub-configuration idx (sorted indices)."""
    idx = sorted(idx)
    m = len(idx)
    if m <= 2:
        return m, m
    sub = S[np.ix_(idx, idx, idx)]
    return int(ranks(sub, -1).max()), int(ranks(sub, +1).max())


def max_convex(S):
    """Largest number of points in convex position (exact, via cap(a->b) + cup(a->b) - 2).
    L[a,u,v] = longest chain starting at a and ending with edge (u,v) (0 = none)."""
    n = S.shape[0]
    if n <= 3:
        return n
    best = 3
    res = {}
    for color in (-1, +1):
        L = np.zeros((n, n, n), dtype=np.int16)
        for a in range(n):
            L[a, a, a + 1:] = 2
        for u in range(1, n):
            A = L[:, :u, u]  # (a, t)
            M = (S[:u, u, :] == color)  # (t, v)
            cand = np.where(M[None, :, :] & (A[:, :, None] > 0), A[:, :, None] + 1, 0).max(axis=1)
            L[:, u, u + 1:] = np.maximum(L[:, u, u + 1:], cand[:, u + 1:])
        res[color] = L.max(axis=1)  # [a, b] longest chain a -> b (0 if a>=b)
    tot = res[-1].astype(np.int32) + res[+1].astype(np.int32) - 2
    valid = (res[-1] > 0) & (res[+1] > 0)
    if valid.any():
        best = max(best, int(tot[valid].max()))
    return best


def in_triangle_strict(p, a, b, c):
    o1 = orient(a, b, p)
    o2 = orient(b, c, p)
    o3 = orient(c, a, p)
    return (o1 > 0 and o2 > 0 and o3 > 0) or (o1 < 0 and o2 < 0 and o3 < 0)


def convex_position_brute(pts):
    """General position assumed: convex position iff no point inside a triangle of three others."""
    from itertools import combinations
    m = len(pts)
    for i in range(m):
        others = [pts[j] for j in range(m) if j != i]
        for a, b, c in combinations(others, 3):
            if in_triangle_strict(pts[i], a, b, c):
                return False
    return True


def max_convex_brute(pts, kmax=None):
    from itertools import combinations
    n = len(pts)
    best = min(n, 3)
    k = 4
    while k <= n and (kmax is None or k <= kmax):
        found = False
        for sub in combinations(range(n), k):
            if convex_position_brute([pts[i] for i in sub]):
                found = True
                break
        if not found:
            break
        best = k
        k += 1
    return best
