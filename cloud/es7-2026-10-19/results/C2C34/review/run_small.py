#!/usr/bin/env python3
"""usage: run_small.py CNF MAP NCONF SEED [--mode random|nested|mixed]"""
import sys, os, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import advlib, zlayers

cnf, mapf, nconf, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
mode = sys.argv[sys.argv.index('--mode') + 1] if '--mode' in sys.argv else 'mixed'
rng = random.Random(seed)
t0 = time.time()
M = advlib.Model(cnf, mapf)
t, K = M.t, M.K
adm = zlayers.profiles(t)
print(f"model t={t} K={K} nv={M.nv} nc={M.nc} (setup {time.time()-t0:.1f}s)", flush=True)

configs = []
for ci in range(nconf):
    kind = mode if mode != 'mixed' else rng.choice(['random', 'nested', 'nested_near', 'nested_any'])
    if kind == 'random':
        P = advlib.gen_random(t, rng, box=rng.choice([6, 12, 60, 1000]))
    else:
        if kind == 'nested_any':
            # arbitrary layer sizes (h >= 4 allowed), last may be 1
            while True:
                prof, rest = [], t
                while rest:
                    h = rng.randint(1, min(rest, 5))
                    if h == 1 and rest != 1:
                        continue
                    prof.append(h)
                    rest -= h
                if all(h >= 2 for h in prof[:-1]):
                    break
            prof = tuple(prof)
        else:
            prof = rng.choice(adm)
        P = advlib.gen_nested(prof, rng, near=(kind == 'nested_near'))
        if P is None:
            print("gen failed", prof)
            continue
    configs.append((kind, P))

stats = dict(configs=0, labelings=0, unit_false=0, units_mismatch=0, ccw_bad=0, other_viol=0, kcount_bad=0,
             exhaust_bad=0, k_viol_total=0, fully_sat=0, adm_prof=0)
batch = []
for kind, P in configs:
    L = advlib.layers_of(P)
    mc = advlib.max_convex(P, cap=K + 1)
    nk = advlib.count_convex(P, K) if len(P) >= K else 0
    if K % 2 == 0:   # half-turn-invariant K-sets are their own canonical form
        import itertools as _it
        pairs = [(P[2 * i], P[2 * i + 1]) for i in range(t)]
        assert all(b == advlib.neg(a) for a, b in pairs)
        ninv = sum(1 for Q in _it.combinations(pairs, K // 2) if advlib.convex_set([x for pr in Q for x in pr]))
        nk += ninv
    for p00 in L[0]:
        prof, X, L2, order = advlib.normal_form(P, p00)
        if advlib.check_ccw_claim(L2, order):
            stats['ccw_bad'] += 1
            print("CCW claim fails", kind, prof, P, p00)
        T, val, cval = M.truth(X)
        us, false, same, ndiff = advlib.check_units(M, T, X, L2, prof)
        if false:
            stats['unit_false'] += 1
            print("FALSE UNITS", kind, prof, false[:10], P, p00)
        if not same:
            stats['units_mismatch'] += 1
            print("units differ from geometry-derived set", kind, prof, ndiff)
        if K == 7 and mc < 7 and prof not in adm:
            stats['exhaust_bad'] += 1
            print("profile not admissible although 7-gon-free", prof, P)
        batch.append((kind, P, p00, prof, T, nk))
    stats['configs'] += 1
print(f"labelings: {len(batch)} (prep {time.time()-t0:.1f}s)", flush=True)
res = M.eval_stream([b[4] for b in batch])
for (kind, P, p00, prof, T, nk), r in zip(batch, res):
    stats['labelings'] += 1
    stats['k_viol_total'] += r['k_viol']
    if r['k_viol'] == 0 and r['other_viol'] == 0:
        stats['fully_sat'] += 1
    if prof in adm:
        stats['adm_prof'] += 1
    if r['other_viol']:
        stats['other_viol'] += 1
        print("NON-K CLAUSE VIOLATED", kind, prof, r['other'][:5], P, p00)
    if r['k_viol'] * 2 != nk:
        stats['kcount_bad'] += 1
        print("K-violation count mismatch", kind, prof, r['k_viol'], nk / 2, P, p00)
print(stats, f"total {time.time()-t0:.1f}s")
