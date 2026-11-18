"""Upper-chain statement on the REAL certificate sets of ETVTHY20261113 (exact per set; pure Python + pysat).
For a point set with no 5-cap and no convex n-gon: a pair u < v is saturated if capB(u,v) + cupB(u,v) = n + 1
(longest cap / cup between them); the upper chains of the convex (n-1)-gons are exactly the longest caps of the
saturated pairs.  Question: is there a 4-cap-free Delta that meets every upper chain?  (Then Delta meets every
convex (n-1)-gon at a vertex of its own cap part.)  The returned Delta is re-checked: 4-cap-free by pyexact chains,
and against a recomputed list of upper chains.     usage: upper_real.py n certfile.jsonl [strong]"""
import sys, json, time
import pyexact_etvthy as px
from pysat.solvers import Glucose4
W = '/home/jay/research/data/etvthy-20261113/'
n = int(sys.argv[1]); strong = len(sys.argv) > 3 and sys.argv[3] == 'strong'
def upper_chains(P, O, capB, cupB, n):
    m = len(P); out = []
    for (u, v), c in capB.items():
        if c + cupB[u, v] != n + 1: continue
        if c == 2: out.append((u, v))
        elif c == 3:
            for k in range(u + 1, v):
                if O[u, k, v] < 0: out.append((u, k, v))
        elif c == 4:
            for k1 in range(u + 1, v):
                if O[u, k1, v] > 0: continue
                for k2 in range(k1 + 1, v):
                    if O[u, k1, k2] < 0 and O[k1, k2, v] < 0: out.append((u, k1, k2, v))
        else: raise ValueError('cap of size %d' % c)
    return out
def caps4(P, O):
    m = len(P); out = []
    for b in range(m):
        for c in range(b + 1, m):
            L = [a for a in range(b) if O[a, b, c] < 0]
            if not L: continue
            R = [d for d in range(c + 1, m) if O[b, c, d] < 0]
            out += [(a, b, c, d) for a in L for d in R]
    return out
cache = {}; cnt = ok = 0; t0 = time.time(); sizes = []
for line in open(sys.argv[2]):
    rec = json.loads(line); fn = rec['file']
    if fn not in cache: cache[fn] = [json.load(open(W + fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(W + fn)]
    P = sorted(tuple(p) for p in cache[fn][rec['index']]); m = len(P)
    O = px.otable(P); capE, cupE, capB, cupB = px.chains(P, O)
    assert max(capB.values()) <= 4 and max(capB[k] + cupB[k] - 2 for k in capB) <= n - 1
    UC = upper_chains(P, O, capB, cupB, n); K4 = caps4(P, O)
    with Glucose4() as s:
        for K in K4: s.add_clause([-(i + 1) for i in K])
        for U in UC: s.add_clause([i + 1 for i in U])
        sat = s.solve()
        D = [i for i in range(m) if s.get_model()[i] > 0] if sat else None
    cnt += 1
    if sat:
        Ds = set(D)
        # independent re-check
        sub = [P[i] for i in D]
        if len(sub) >= 2:
            _, _, cb, _ = px.chains(sub); assert max(cb.values()) <= 3, 'Delta has a 4-cap'
        assert all(Ds & set(U) for U in UC)
        rest = [P[i] for i in range(m) if i not in Ds]
        if len(rest) >= 3:
            _, _, cb, ub = px.chains(rest); assert max(cb[k] + ub[k] - 2 for k in cb) <= n - 2, 'a gon misses Delta'
        ok += 1; sizes.append(len(D))
    else:
        print('NO upper-chain transversal:', fn, rec['index'], m, 'points', len(UC), 'upper chains', flush=True)
print('%s n=%d: %d sets, a 4-cap-free Delta meeting every upper chain exists in %d (re-checked); |Delta| between %d and %d; %.0fs' % (sys.argv[2].split('/')[-1], n, cnt, ok, min(sizes or [0]), max(sizes or [0]), time.time() - t0), flush=True)
