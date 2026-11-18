"""Exact test of the lower-chain form on one real point set (lazy SAT; chain lengths from the C library esgeo of
ETVTHY20261113).  lower_delta(P, n, b) -> ('OK', Delta) or ('NONE', None):
Delta has no b-cap and capB_S(u,v) + cupB_{S-Delta}(u,v) <= n for all u < v outside Delta."""
import sys, itertools
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, orient
from pysat.solvers import Glucose4

def all_caps(P, b):
    """all b-caps (index tuples) of the sorted point list P, b >= 3"""
    m = len(P); out = []
    nxt = {}
    for i in range(m):
        for j in range(i + 1, m):
            nxt[i, j] = [k for k in range(j + 1, m) if orient(P[i], P[j], P[k]) < 0]
    def ext(ch):
        if len(ch) == b: out.append(tuple(ch)); return
        for k in nxt[ch[-2], ch[-1]]: ext(ch + [k])
    for i in range(m):
        for j in range(i + 1, m): ext([i, j])
    return out

def longest_cup(P, pts, u, v):
    pts = [i for i in pts if u <= i <= v]
    D = {}; B = {}
    for j in pts[1:]: D[u, j] = 2; B[u, j] = None
    for bj in range(1, len(pts)):
        j = pts[bj]
        for bi in range(1, bj):
            i = pts[bi]; best = 0; bp = None
            for bh in range(0, bi):
                h = pts[bh]
                if D.get((h, i), 0) and orient(P[h], P[i], P[j]) > 0 and D[h, i] + 1 > best: best = D[h, i] + 1; bp = h
            D[i, j] = best; B[i, j] = bp
    L, i = max((D.get((i, v), 0), i) for i in pts[:-1]); cup = [v, i]; j = v
    while i != u: h = B[i, j]; cup.append(h); j = i; i = h
    return L, cup[::-1]

def lower_delta(P, n, b, A=None):
    P = sorted(P); m = len(P); A = A or Analysis(P)
    sat_pairs = [(u, v) for u in range(m) for v in range(u + 1, m) if A.capB[u, v] + A.cupB[u, v] == n + 1]
    s = Glucose4(bootstrap_with=[[i + 1, -(i + 1)] for i in range(m)])
    for K in all_caps(P, b): s.add_clause([-(i + 1) for i in K])
    try:
        for rnd in range(600):
            if not s.solve(): return 'NONE', None, rnd
            mod = s.get_model(); D = {i for i in range(m) if mod[i] > 0}
            rest = [i for i in range(m) if i not in D]
            if len(rest) < 2: return 'OK', sorted(D), rnd
            Ar = Analysis([P[i] for i in rest]); pos = {p: k for k, p in enumerate(rest)}
            viol = [(u, v) for (u, v) in sat_pairs if u in pos and v in pos and Ar.cupB[pos[u], pos[v]] == A.cupB[u, v]]
            if not viol: return 'OK', sorted(D), rnd
            for (u, v) in viol[:200]:
                L, cup = longest_cup(P, rest, u, v); assert L == A.cupB[u, v]
                s.add_clause([i + 1 for i in cup])
        return 'ROUNDS', None, 600
    finally: s.delete()
