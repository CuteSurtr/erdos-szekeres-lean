"""Lower-chain statement on the REAL certificate sets of ETVTHY20261113 (exact per set, lazy clauses):
is there a 4-cap-free Delta that meets the CUP part (lower chain, including the two ends) of every convex (n-1)-gon?
The lower chains are the longest cups of the saturated pairs (capB + cupB = n + 1).  Lazy loop: SAT over the points with
all 4-caps forbidden; for the current Delta every saturated pair u, v outside Delta whose longest cup inside S - Delta is
as long as in S yields a violated lower chain (one longest cup avoiding Delta), which is added as a clause.
capB / cupB come from the C library of ETVTHY20261113 (esgeo); the final Delta is re-checked with pyexact (pure Python).
usage: lower_real.py n certfile.jsonl"""
import sys, json, time
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, orient
import pyexact_etvthy as px
from pysat.solvers import Glucose4
W = '/home/jay/research/data/etvthy-20261113/'
n = int(sys.argv[1]); RECHECK = int(sys.argv[3]) if len(sys.argv) > 3 else 0     # re-check every RECHECK-th set in pure Python
def longest_cup(P, idx, u, v):
    """one longest cup from u to v using only points of idx (sorted list of indices containing u and v)"""
    pts = [i for i in idx if u <= i <= v]
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
    best = max((D.get((i, v), 0), i) for i in pts[:-1])
    L, i = best; cup = [v, i]; j = v
    while i != u: h = B[i, j]; cup.append(h); j = i; i = h
    return L, cup[::-1]
cache = {}; cnt = ok = 0; t0 = time.time(); rounds_tot = 0; nre = 0
for line in open(sys.argv[2]):
    rec = json.loads(line); fn = rec['file']
    if fn not in cache: cache[fn] = [json.load(open(W + fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(W + fn)]
    P = sorted(tuple(p) for p in cache[fn][rec['index']]); m = len(P)
    A = Analysis(P); assert A.gon() <= n - 1
    sat_pairs = [(u, v) for u in range(m) for v in range(u + 1, m) if A.capB[u, v] + A.cupB[u, v] == n + 1]
    caps4 = []
    for b in range(m):
        for c in range(b + 1, m):
            L = [a for a in range(b) if orient(P[a], P[b], P[c]) < 0]
            if L:
                R = [d for d in range(c + 1, m) if orient(P[b], P[c], P[d]) < 0]
                caps4 += [(a, b, c, d) for a in L for d in R]
    s = Glucose4(bootstrap_with=[[i + 1, -(i + 1)] for i in range(m)])
    for K in caps4: s.add_clause([-(i + 1) for i in K])
    status = None
    for rnd in range(400):
        if not s.solve(): status = 'NONE'; break
        mod = s.get_model(); D = {i for i in range(m) if mod[i] > 0}
        rest = [i for i in range(m) if i not in D]
        if len(rest) < 2: status = 'OK'; break
        Ar = Analysis([P[i] for i in rest]); pos = {p: k for k, p in enumerate(rest)}
        viol = [(u, v) for (u, v) in sat_pairs if u in pos and v in pos and Ar.cupB[pos[u], pos[v]] == A.cupB[u, v]]
        if not viol: status = 'OK'; break
        for (u, v) in viol[:200]:
            L, cup = longest_cup(P, rest, u, v); assert L == A.cupB[u, v]
            s.add_clause([i + 1 for i in cup])
    s.delete(); cnt += 1; rounds_tot += rnd + 1
    if status == 'OK':
        sub = [P[i] for i in sorted(D)]
        if len(sub) >= 2:
            _, _, cb, _ = px.chains(sub); assert max(cb.values()) <= 3, 'Delta has a 4-cap'
        if RECHECK and (cnt % RECHECK == 1 or RECHECK == 1):
            # independent pure-Python re-check of the lower-chain property (pyexact, no C library)
            _, _, cbF, ubF = px.chains(P)
            assert max(cbF.values()) <= 4 and max(cbF[k] + ubF[k] - 2 for k in cbF) <= n - 1
            rest = [i for i in range(m) if i not in D]
            if len(rest) >= 2:
                _, _, cbR, ubR = px.chains([P[i] for i in rest])
                for x in range(len(rest)):
                    for y in range(x + 1, len(rest)):
                        u, v = rest[x], rest[y]
                        assert cbF[u, v] + ubR[x, y] <= n, 'lower chain missed'
            nre += 1
        ok += 1
    else: print('NO lower-chain transversal (%s):' % status, fn, rec['index'], m, 'points', len(sat_pairs), 'saturated pairs', flush=True)
print('%s n=%d: %d sets, a 4-cap-free Delta meeting every lower chain exists in %d; %d lazy rounds in all; pure-Python re-check of capB_S + cupB_{S-Delta} <= n on %d sets; %.0fs' % (sys.argv[2].split('/')[-1], n, cnt, ok, rounds_tot, nre, time.time() - t0), flush=True)
