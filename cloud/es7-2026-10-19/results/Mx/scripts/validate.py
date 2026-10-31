#!/usr/bin/env python3
"""Mx encoding validation on random and structured exactly mirror-symmetric point sets.

For each set (n odd, one axis point, integer coordinates, general position, distinct x):
  * chi from exact integer determinants on the x-sorted points;
  * mirror sign rule chi(m-k,m-j,m-i) == chi(i,j,k) checked on every triple;
  * every signotope clause satisfied;
  * case clauses: 'top' clauses hold iff the axis point is an upper-hull vertex (hull from
    Andrew's monotone chain on coordinates), 'interior' clauses hold iff it is interior,
    'sym' unit holds iff chi(0,1,2);
  * no-k-gon: the least model of the Horn aux clauses (forward chaining) satisfies every gon
    clause iff the brute force (bfgon, exhaustive over convex-position subsets) finds no
    convex k-gon.  (Least model violates a purely negative clause => every model does.)
  * a subsample is also run through CaDiCaL on the written CNF with orientation units.
"""
import sys, os, random, json, itertools, subprocess, time
from collections import defaultdict, Counter
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mxgen
HERE = os.path.dirname(os.path.abspath(__file__))
BF = os.environ.get('BFGON', '/tmp/claude-0/mx/bfgon')
CADICAL = os.environ.get('CADICAL', '/tmp/claude-0/sw/cadical/build/cadical')
TMP = os.environ.get('MXTMP', '/tmp/claude-0/mx')

def gp_ok(P):
    if len(set(x for x, _ in P)) != len(P): return False
    for a, b, c in itertools.combinations(P, 3):
        if (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]) == 0: return False
    return True

def rand_set(n, rng):
    R = rng.choice([30, 1000, 10**5, 10**7])
    while True:
        xs = rng.sample(range(1, R + 1), (n - 1) // 2) if R >= n else None
        if xs is None: R = 1000; continue
        pr = [(x, rng.randint(-R, R)) for x in xs]
        ys = [y for _, y in pr]
        u = rng.random()
        y0 = (max(ys) + rng.randint(1, R)) if u < .25 else (min(ys) - rng.randint(1, R)) if u < .5 \
            else rng.randint(-R, R)
        P = pr + [(-x, y) for x, y in pr] + [(0, y0)]
        if gp_ok(P): return sorted(P)

_M = None
def struct_set(rng):
    """Random sub-collection of mirror pairs of the mirror-symmetric classical 32-point
    heptagon-free set (tools/decomp/mirror.py, axis y=0 there; coordinates swapped so the
    axis is x=0), plus one axis point at random height."""
    global _M
    if _M is None:
        sys.path.insert(0, os.path.join(HERE, '../../../tools/decomp'))
        from mirror import mirror_construction
        from math import lcm
        M = mirror_construction(7); d = 1
        for x, y in M: d = lcm(d, x.denominator, y.denominator)
        _M = [(int(y * d), int(x * d)) for x, y in M]
        assert sorted(_M) == sorted((-x, y) for x, y in _M)
    pairs = [p for p in _M if p[0] > 0]
    ys = [y for _, y in _M]; lo, hi = min(ys), max(ys); sp = hi - lo
    while True:
        r = rng.randint(4, 16)
        pr = rng.sample(pairs, r)
        u = rng.random()
        y0 = hi + rng.randint(1, sp) if u < .2 else lo - rng.randint(1, sp) if u < .4 else \
            rng.randint(lo - sp // 10, hi + sp // 10)
        P = pr + [(-x, y) for x, y in pr] + [(0, y0)]
        if gp_ok(P): return sorted(P)

def chi_of(P):
    n = len(P); ch = {}
    for i, j, k in itertools.combinations(range(n), 3):
        a, b, c = P[i], P[j], P[k]
        ch[(i, j, k)] = (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]) > 0
    return ch

def axis_status(P):
    a = len(P) // 2; assert P[a][0] == 0
    def cross(o, p, q): return (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])
    lower, upper = [], []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    for p in reversed(P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    if P[a] in upper: return 'top'
    if P[a] in lower: return 'bottom'
    return 'interior'

def check_group(args):
    (n, k), items = args
    enc = mxgen.build(n, k, True, 'none')
    rep = enc['rep']; no = enc['norient']
    X = lambda i, j, l: rep[(i, j, l)]
    sig = [c for t, c in enc['clauses'] if t == 'sig']
    aux = [c for t, c in enc['clauses'] if t == 'aux']
    gon = [c for t, c in enc['clauses'] if t == 'gon']
    modes = {md: mxgen.mode_clauses(n, X, md) for md in ('top', 'interior', 'all')}
    out = []
    for it in items:
        P = it['P']; ch = chi_of(P); m = n - 1; err = []
        if any(ch[(m-l, m-j, m-i)] != ch[(i, j, l)] for (i, j, l) in ch): err.append('mirror-rule')
        val = [None] * (enc['nvars'] + 1)
        for t, v in ch.items():
            r = rep[t]
            if val[r] is None: val[r] = v
            elif val[r] != v: err.append('orbit'); break
        def sat(c): return any((val[abs(x)] if x > 0 else not val[abs(x)]) for x in c)
        if not all(sat(c) for c in sig): err.append('sig')
        st = axis_status(P)
        mt = all(sat(c) for _, c in modes['top']); mi = all(sat(c) for _, c in modes['interior'] if _ == 'case')
        if mt != (st == 'top'): err.append('top-clauses')
        if mi != (st == 'interior'): err.append('interior-clauses')
        if all(sat(c) for _, c in modes['all']) != ch[(0, 1, 2)]: err.append('sym')
        for v in range(no + 1, enc['nvars'] + 1): val[v] = False
        changed = True; passes = 0
        while changed:
            changed = False; passes += 1
            for c in aux:
                pos = c[-1]  # largest literal: the unique positive aux (new() ids increase)
                if pos <= no or val[pos]: continue
                if all((not val[abs(x)]) if x > 0 else val[abs(x)] for x in c[:-1]):
                    val[pos] = True; changed = True
        nogon = all(sat(c) for c in gon)
        if nogon != (it['L'] < k): err.append('gon(L=%d)' % it['L'])
        out.append(dict(id=it['id'], fam=it['fam'], n=n, k=k, L=it['L'], axis=st,
                        nogon=nogon, passes=passes, err=err))
    return out

def cadical_check(it):
    n, k, P = it['n'], it['k'], it['P']
    enc = mxgen.build(n, k, True, 'none'); ch = chi_of(P)
    path = os.path.join(TMP, 'val_%d.cnf' % it['id'])
    cl = [c for _, c in enc['clauses']]
    units = sorted({(r if ch[t] else -r) for t, r in enc['rep'].items() if len(t) == 3 and t in ch})
    with open(path, 'w') as f:
        f.write('p cnf %d %d\n' % (enc['nvars'], len(cl) + len(units)))
        for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
        for u in units: f.write('%d 0\n' % u)
    r = subprocess.run([CADICAL, '-q', path], capture_output=True, text=True)
    os.remove(path)
    return dict(id=it['id'], n=n, k=k, L=it['L'], sat=(r.returncode == 10), ok=((r.returncode == 10) == (it['L'] < k)))

if __name__ == '__main__':
    N = int(sys.argv[1]); seed = int(sys.argv[2]); outp = sys.argv[3]
    rng = random.Random(seed); items = []
    t0 = time.time()
    for idx in range(N):
        if rng.random() < 0.3:
            P = struct_set(rng); fam = 'struct'
        else:
            n = rng.choice(range(9, 34, 2)); P = rand_set(n, rng); fam = 'random'
        items.append(dict(id=idx, fam=fam, P=P))
    inp = ''.join('%d %s\n' % (len(it['P']), ' '.join('%d %d' % p for p in it['P'])) for it in items)
    # brute force in 4 parallel chunks
    chunks = [items[i::4] for i in range(4)]
    procs = [subprocess.Popen([BF], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True) for _ in chunks]
    outs = [p.communicate(''.join('%d %s\n' % (len(it['P']), ' '.join('%d %d' % q for q in it['P'])) for it in ch))[0].split()
            for p, ch in zip(procs, chunks)]
    for ch, o in zip(chunks, outs):
        for it, L in zip(ch, o): it['L'] = int(L)
    print('generated + brute force: %.0fs' % (time.time() - t0), flush=True)
    for it in items:
        n = len(it['P']); L = it['L']
        opts = [L, L + 1] + ([7] if it['fam'] == 'struct' else [])
        it['n'] = n; it['k'] = max(4, rng.choice(opts))
    groups = defaultdict(list)
    for it in items: groups[(it['n'], it['k'])].append(it)
    gl = sorted(groups.items(), key=lambda g: -g[0][0] * g[0][1] * len(g[1]))
    res = []
    with Pool(4) as pool:
        for r in pool.imap_unordered(check_group, gl):
            res += r
    print('encoding checks: %.0fs' % (time.time() - t0), flush=True)
    sub = rng.sample(items, min(200, N))
    with Pool(4) as pool:
        cad = pool.map(cadical_check, sub)
    bad = [r for r in res if r['err']]
    summ = dict(N=len(res), seed=seed, errors=len(bad), cadical_subsample=len(cad),
                cadical_disagree=sum(not c['ok'] for c in cad),
                cadical_sat=sum(c['sat'] for c in cad),
                by_family=Counter(r['fam'] for r in res),
                by_n=dict(sorted(Counter(r['n'] for r in res).items())),
                kgon_free=sum(r['nogon'] for r in res),
                kgon_free_by_k=dict(sorted(Counter(r['k'] for r in res if r['nogon']).items())),
                with_kgon_by_k=dict(sorted(Counter(r['k'] for r in res if not r['nogon']).items())),
                axis=Counter(r['axis'] for r in res),
                n33_k7=Counter((r['nogon']) for r in res if r['n'] == 33 and r['k'] == 7),
                k7_free_by_n=dict(sorted(Counter(r['n'] for r in res if r['k'] == 7 and r['nogon']).items())),
                max_passes=max(r['passes'] for r in res), seconds=round(time.time() - t0))
    json.dump(dict(summary=summ, bad=bad[:50], cadical=cad), open(outp, 'w'), indent=1, default=str)
    print(json.dumps(summ, default=str, indent=1))
