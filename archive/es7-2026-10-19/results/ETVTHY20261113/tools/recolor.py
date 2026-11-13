"""Recoloring test: cap (x,y,z) with s(xy)=3 (edge xy starts a 4-cap) -> cup*. S* is 4-cap*-free.
Report longest cup* and longest weak (3,k)-gon* in S*."""
import sys, json
import numpy as np
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis
from collections import Counter

def star_stats(P, rule='s3'):
    A = Analysis(P); n = A.n
    s = A.capS - 1   # s(xy) = longest cap starting with (x,y) minus 1
    O = {}
    cap = np.zeros((n, n, n), bool)
    for a in range(n):
        for b in range(a+1, n):
            for c in range(b+1, n):
                if A.o(a, b, c) < 0:
                    if rule == 's3' and s[a, b] == 3: continue  # recolored to cup*
                    cap[a, b, c] = True
    # longest cap*/cup* ending with edge (i,j), and between endpoints
    capE = np.full((n, n), 2); cupE = np.full((n, n), 2)
    for j in range(n):
        for i in range(j):
            for h in range(i):
                if cap[h, i, j]: capE[i, j] = max(capE[i, j], capE[h, i] + 1)
                else: cupE[i, j] = max(cupE[i, j], cupE[h, i] + 1)
    maxcap = capE.max() if n > 1 else 1; maxcup = cupE.max() if n > 1 else 1
    # weak (3,k)-gon*: 3-cap* (u,w,v) and cup* from u to v of length k: longest cup* between endpoints
    best = 0
    for u in range(n):
        D = np.zeros((n, n), int)
        for j in range(u+1, n): D[u, j] = 2
        for j in range(u+1, n):
            for i in range(u+1, j):
                m = 0
                for h in range(u, i):
                    if D[h, i] and not cap[h, i, j]: m = max(m, D[h, i] + 1)
                D[i, j] = m
        for v in range(u+2, n):
            if any(cap[u, w, v] for w in range(u+1, v)):
                k = max(D[i, v] for i in range(u, v))
                best = max(best, k)
    return n, int(maxcap), int(maxcup), best

if __name__ == '__main__':
    st = Counter(); rows = []
    for fn in sys.argv[1:]:
        sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
        for P in sets:
            r = star_stats(sorted(tuple(p) for p in P)); rows.append(r)
    print('n, maxcap*, maxcup*, max k of weak (3,k)-gon*')
    for r in sorted(rows, key=lambda r: -r[2])[:10]: print(r)
    print('max cup* overall', max(r[2] for r in rows), 'max (3,k)* overall', max(r[3] for r in rows))
