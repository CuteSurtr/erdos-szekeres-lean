"""Type-specific convex polygon witnesses: an a-cap and b-cup with common endpoints (exact)."""
import sys
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, orient

def chain_between(P, s, t, length, sign):
    """Return a chain (cap: sign<0, cup: sign>0) from s to t with exactly `length` points, or None."""
    idx = [i for i in range(s, t+1)]
    # D[(i,j)] = longest chain from s ending with edge (i,j); back pointers
    D = {}; B = {}
    for j in idx[1:]:
        D[(s, j)] = 2; B[(s, j)] = None
    for j in idx[1:]:
        for i in idx[1:]:
            if i >= j: break
            best = 0; bp = None
            for h in range(s, i):
                if (h, i) in D and D[(h, i)] and (orient(P[h], P[i], P[j]) > 0) == (sign > 0):
                    if D[(h, i)] + 1 > best: best = D[(h, i)] + 1; bp = h
            D[(i, j)] = best; B[(i, j)] = bp
    cands = [(D[(i, t)], i) for i in range(s, t) if D.get((i, t), 0) >= length]
    if not cands: return None
    L, i = max(cands)
    chain = [t, i]; j = t
    while i != s:
        h = B[(i, j)]; chain.append(h); j = i; i = h
    chain = chain[::-1]
    # trim interior points to exact length (subsets of caps/cups with endpoints kept are caps/cups)
    while len(chain) > length: chain.pop(1)
    return chain

def type_witness(P, idx, types):
    """Search inside subset idx (sorted list of indices into P) for a polygon of one of the given (a,b) types."""
    Q = [P[i] for i in idx]
    if len(Q) < 3: return None
    A = Analysis(Q); n = A.n
    for s in range(n):
        for t in range(s+1, n):
            for a, b in types:
                if A.capB[s, t] >= a and A.cupB[s, t] >= b:
                    K = chain_between(Q, s, t, a, -1); D = chain_between(Q, s, t, b, +1)
                    if K is None or D is None: continue
                    return sorted({idx[i] for i in K} | {idx[i] for i in D})
    return None
