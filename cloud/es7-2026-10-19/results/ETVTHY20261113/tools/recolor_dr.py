"""Delta_R with recoloring: within Delta_R, caps (a,b,c) whose edge (a,b) starts a 4-cap inside Delta_R -> cup*.
Then Delta_R* is 4-cap*-free. Report longest cup* and largest k of a weak (3,k)*-gon (Baek n=k+1 bound needs k<=n-2)."""
import sys, json
import numpy as np
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis
from collections import Counter

def star_on(Q):
    A = Analysis(Q); n = A.n
    s = A.capS - 1
    cap = np.zeros((n, n, n), bool)
    for a in range(n):
        for b in range(a+1, n):
            for c in range(b+1, n):
                if A.o(a, b, c) < 0 and not (s[a, b] == 3): cap[a, b, c] = True
    capE = np.full((n, n), 2); cupE = np.full((n, n), 2)
    for j in range(n):
        for i in range(j):
            for h in range(i):
                if cap[h, i, j]: capE[i, j] = max(capE[i, j], capE[h, i] + 1)
                else: cupE[i, j] = max(cupE[i, j], cupE[h, i] + 1)
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
                best = max(best, max(D[i, v] for i in range(u, v)))
    return int(capE.max()) if n > 1 else 1, int(cupE.max()) if n > 1 else 1, best

st = Counter(); worst = (0, 0)
for fn in sys.argv[1:]:
    sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    for P in sets:
        P = sorted(tuple(p) for p in P); A = Analysis(P); n = A.n
        DR = [P[i] for i in range(n) if A.cap_end[i] + A.cup_end[i] >= 9]
        if len(DR) < 4: continue
        mc, mu, k3 = star_on(DR)
        st[(mc, mu, k3)] += 1
        worst = max(worst, (mu, k3))
print(sorted(st.items())); print('worst (cup*, (3,k)*):', worst)
