#!/usr/bin/env python3
"""Streaming check of a large base CNF (+ layer units) on a few real labelled configurations (<= ~8 per pass).
usage: run_big.py CNF MAP SEED [--pts FILE] [--addpair FILE N] [--nested N] [--near N] [--random N] [--maxlab M]"""
import sys, os, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import advlib, zlayers

cnf, mapf, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
argv = sys.argv
def opt(name, default=None, n=1):
    if name in argv:
        i = argv.index(name)
        return argv[i + 1:i + 1 + n] if n > 1 else argv[i + 1]
    return default
rng = random.Random(seed)
t0 = time.time()
M = advlib.Model(cnf, mapf)
t, K = M.t, M.K
adm = zlayers.profiles(t)
print(f"model t={t} K={K} nv={M.nv} nc={M.nc} setup {time.time()-t0:.1f}s", flush=True)
maxlab = int(opt('--maxlab', 8))

def readpts(f):
    P = [tuple(map(int, l.split()[:2])) for l in open(f) if l.strip() and not l.startswith('#')]
    # reorder as antipodal pairs
    out, seen = [], set()
    for p in P:
        if p in seen:
            continue
        assert advlib.neg(p) in P
        out += [p, advlib.neg(p)]
        seen.update([p, advlib.neg(p)])
    return out

configs = []
if opt('--pts'):
    P = readpts(opt('--pts'))
    assert len(P) == 2 * t and advlib.general_position(P)
    configs.append(('real', P, None))
if opt('--addpair'):
    f, n = opt('--addpair', n=2)
    base = readpts(f)
    assert len(base) == 2 * t - 2
    made = 0
    while made < int(n):
        sc = rng.choice([30, 300, 3000, 30000, 300000, 3000000])
        q = (rng.randint(-sc, sc), rng.randint(-sc, sc))
        if q == advlib.O or q in base:
            continue
        P = base + [q, advlib.neg(q)]
        if not advlib.general_position(P):
            continue
        configs.append((f'addpair(sc={sc})', P, None))
        made += 1
for kind in ('--nested', '--near'):
    if opt(kind):
        for _ in range(int(opt(kind))):
            prof = rng.choice(adm)
            P = advlib.gen_nested(prof, rng, near=(kind == '--near'))
            if P is None:
                print('gen failed', prof); continue
            configs.append((kind[2:], P, None))
if opt('--random'):
    for _ in range(int(opt('--random'))):
        configs.append(('random', advlib.gen_random(t, rng, box=rng.choice([60, 1000, 10 ** 6])), None))

labs = []
for kind, P, _ in configs:
    L = advlib.layers_of(P)
    nk = advlib.count_convex(P, K)
    assert K % 2 == 1
    cands = list(L[0])
    rng.shuffle(cands)
    if kind == 'near':
        import math
        deeper = [q for V in L[1:] for q in V]
        nearness = lambda p: min(abs(advlib.cross(advlib.O, p, q)) / math.hypot(*p) / math.hypot(*q) for q in deeper)
        cands.sort(key=nearness)
        print(f"  near config prof={tuple(len(V)//2 for V in L)}: best |sin| = {nearness(cands[0]):.1e}")
    per = max(1, maxlab // len(configs))
    for p00 in cands[:per]:
        prof, X, L2, order = advlib.normal_form(P, p00)
        ccw = advlib.check_ccw_claim(L2, order)
        T, val, cval = M.truth(X)
        us, false, same, ndiff = advlib.check_units(M, T, X, L2, prof)
        labs.append(dict(kind=kind, P=P, p00=p00, prof=prof, T=T, nk=nk, ccw_bad=ccw, units=len(us), false=false,
                         same=same, ndiff=ndiff, adm=prof in adm))
print(f"{len(labs)} labelings prepared {time.time()-t0:.1f}s", flush=True)
res = M.eval_stream([d['T'] for d in labs])
print(f"stream done {time.time()-t0:.1f}s", flush=True)
vos = None
allok = True
for d, r in zip(labs, res):
    exp = d['nk'] // 2
    ok = (not d['ccw_bad'] and not d['false'] and d['same'] and r['other_viol'] == 0 and r['k_viol'] == exp)
    exact = ''
    if r['k_viol'] and r['k_viol'] <= 300:
        if vos is None:
            vos = advlib.var_of_set(M)
        X = None
        prof, X, L2, order = advlib.normal_form(d['P'], d['p00'])
        good = 0
        for cl in r['k_clauses']:
            Ss = advlib.identify_kset(M, cl, vos)
            if len(Ss) == 1 and advlib.convex_set([X[i] for i in Ss[0]]):
                good += 1
        exact = f" exact-check {good}/{r['k_viol']} K-clauses = convex canonical K-sets"
        ok = ok and good == r['k_viol']
    allok &= ok
    print(f"{'OK ' if ok else 'BAD'} {d['kind']:<18} prof={','.join(map(str, d['prof']))} adm={d['adm']} units={d['units']} "
          f"false_units={len(d['false'])} units==geom:{d['same']} ccw_bad={d['ccw_bad']} other_viol={r['other_viol']} "
          f"k_viol={r['k_viol']} expected={exp}{exact}")
    if r['other']:
        print("   e.g.", r['other'][:3])
print("ALL OK" if allok else "PROBLEMS", f"{time.time()-t0:.1f}s")
