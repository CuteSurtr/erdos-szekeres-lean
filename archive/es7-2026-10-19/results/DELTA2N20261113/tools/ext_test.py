"""Extension test (E2), HEURISTIC sampling: for a valid signotope S, call a point p 'safe' if for EVERY working Delta' of
S - p, Delta' or Delta' + p works for S.  Does every S have a safe point?  Which points are safe?"""
import sys, json, itertools, random, collections
from siglib import *
comb = itertools.combinations
def working(o, m, a, n, idx):
    """all working weak Deltas (bitmasks over positions in idx) of the sub-signotope on idx"""
    idx = sorted(idx); pos = {p: i for i, p in enumerate(idx)}
    G = [sum(1 << pos[i] for i in g) for g in gons(o, m, n - 1, idx)]
    K = [sum(1 << pos[i] for i in c) for c in caps(o, m, a - 1, idx)]
    k = len(idx)
    return [D for D in range(1 << k) if not any(D & c == c for c in K) and all(D & g for g in G)], G, K
def safe_points(o, m, a, n):
    Wfull, G, K = working(o, m, a, n, range(m)); Wset = set(Wfull); out = []
    for p in range(m):
        idx = [i for i in range(m) if i != p]
        Wp, _, _ = working(o, m, a, n, idx)
        ok = True
        for D in Wp:
            full = sum(1 << idx[i] for i in range(m - 1) if D >> i & 1)
            if full not in Wset and (full | 1 << p) not in Wset: ok = False; break
        if ok: out.append(p)
    return out
if __name__ == '__main__':
    a, n, m, cnt, seed = [int(x) for x in sys.argv[1:6]]
    from eager_cert import Enc
    from pysat.solvers import Cadical153
    E = Enc(a, n, m, False, base_only=True); rnd = random.Random(seed)
    tris = list(comb(range(m), 3)); st = collections.Counter(); nosafe = []
    with Cadical153(bootstrap_with=E.base) as s:
        for it in range(cnt):
            vs = list(range(1, E.ntri + 1)); rnd.shuffle(vs)
            ass = [v if rnd.random() < 0.5 else -v for v in vs[:max(1, len(vs) // 10)]]
            if not s.solve(assumptions=ass): continue
            mod = s.get_model(); o = {t: mod[E.tri[t] - 1] > 0 for t in tris}
            sp = safe_points(o, m, a, n)
            st['sets'] += 1; st['has safe point'] += bool(sp); st['last point safe'] += (m - 1) in sp; st['first point safe'] += 0 in sp
            st['#safe=%d' % len(sp)] += 1
            if not sp: nosafe.append(''.join('+' if o[t] else '-' for t in tris))
    print(a, n, m, sorted(st.items()), flush=True)
    if nosafe: json.dump(nosafe, open('nosafe_a%d_n%d_m%d.json' % (a, n, m), 'w'))
