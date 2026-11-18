"""Collect several abstract FL(a,b) configurations on n points without a strong split (CEGAR as in
cegar_split.py; every counterexample is blocked exactly and the search continues).  Each counterexample is
re-verified by brute force over all partitions (numpy) before it is written.
usage: cegar_more.py a b n K out.jsonl [time_limit_s]"""
import sys, itertools, json, time
from pysat.solvers import Cadical153
import numpy as np
import fls, split
a, b, n, K, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
tl = float(sys.argv[6]) if len(sys.argv) > 6 else 600
w = fls.FL(a, b, n); so = Cadical153(bootstrap_with=w.cl); aux = {}
def chainvar(sgn, idx):
    key = (sgn, idx)
    if key not in aux:
        v = w.new(); aux[key] = v
        for i in range(len(idx) - 2): so.add_clause([-v, sgn * w.o[idx[i], idx[i + 1], idx[i + 2]]])
    return aux[key]
def gonvar(capidx, cupidx):
    key = ('g', capidx, cupidx)
    if key not in aux:
        g = w.new(); aux[key] = g
        for (sgn, idx) in ((-1, capidx), (1, cupidx)):
            if len(idx) >= 3: so.add_clause([-g, chainvar(sgn, idx)])
    return aux[key]
def gons(S, lc, lu):
    res = []; ic, iu = lc - 2, lu - 2
    for ui in range(len(S)):
        for vi in range(ui + 1, len(S)):
            mid = S[ui + 1:vi]
            if len(mid) < ic + iu: continue
            for cs in itertools.combinations(mid, ic):
                rest = [p for p in mid if p not in cs]
                for us in itertools.combinations(rest, iu):
                    res.append(gonvar((S[ui],) + cs + (S[vi],), (S[ui],) + us + (S[vi],)))
    return res
T = list(itertools.combinations(range(n), 3)); t0 = time.time(); found = 0; it = 0
ALL = np.arange(1 << n, dtype=np.int64); FULL = (1 << n) - 1
def brute_count(sg):
    def chains(L, s): return [idx for idx in itertools.combinations(range(n), L) if all(sg[idx[q], idx[q+1], idx[q+2]] == s for q in range(L - 2))]
    m = lambda s_: sum(1 << p for p in s_)
    def gg(caps, cups):
        by = {}
        for c in cups: by.setdefault((c[0], c[-1]), []).append(c)
        return [m(set(c) | set(u)) for c in caps for u in by.get((c[0], c[-1]), [])]
    capsA1 = chains(a - 1, -1); cupsB1 = chains(b - 1, 1)
    bad1 = set(m(c) for c in capsA1) | set(gg(chains(a - 2, -1), cupsB1)); bad2 = set(m(c) for c in cupsB1) | set(gg(capsA1, chains(b - 2, 1)))
    ok = np.ones(1 << n, dtype=bool)
    for x in bad1: ok &= (ALL & x) != x
    comp = FULL ^ ALL
    for x in bad2: ok &= (comp & x) != x
    return int(ok.sum())
while found < K and time.time() - t0 < tl:
    it += 1
    if not so.solve(): print('search space exhausted: no further counterexample', flush=True); break
    m_ = set(x for x in so.get_model() if x > 0); sg = {t: (1 if w.o[t] in m_ else -1) for t in T}
    f = lambda i, j, k: sg[i, j, k]
    ok, S1, ncl = split.split(n, f, a, b)
    if ok:
        S1 = sorted(S1); S2 = [p for p in range(n) if p not in set(S1)]
        lits = [chainvar(-1, idx) for idx in itertools.combinations(S1, a - 1)] + gons(S1, a - 2, b - 1)
        lits += [chainvar(1, idx) for idx in itertools.combinations(S2, b - 1)] + gons(S2, a - 1, b - 2)
        so.add_clause(lits)
    else:
        assert brute_count(sg) == 0
        sig = ''.join('+' if sg[t] > 0 else '-' for t in T); found += 1
        with open(out, 'a') as fo: fo.write(json.dumps({'a': a, 'b': b, 'n': n, 'm': n, 'sig': sig, 'T': [], 'states': None}) + '\n')
        so.add_clause([(-w.o[t] if sg[t] > 0 else w.o[t]) for t in T])
        print(f'counterexample {found} at iteration {it}, {time.time()-t0:.0f}s', flush=True)
print(f'done: {found} counterexamples, {it} iterations, {time.time()-t0:.0f}s', flush=True)
