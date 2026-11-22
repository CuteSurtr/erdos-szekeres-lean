#!/usr/bin/env python3
"""Reviewer's positive control (HEURISTIC, finite evidence): the 2,025 block rows rowsP/Q/U/A (parsed from the
worker's Rows.lean by my own parser) and the 2,650 base rows on real residual configurations.

Generator only: THEORY310N's real_sets.hull/chart (as VERIFY_LO did). Everything else is my own code, in exact
rationals: min-slope partition, junction removal, the residual hypotheses (distinct x, no collinear triple, longest
cap <= 5, no junction, largest convex polygon <= 7), labels -> columns -> catalog state (the Lean definitions:
labels(u,v) = (6 - longest cap starting with (u,v), longest cup ending with (u,v) - 1),
column v i = max_{u<v} [labels.2 if i+1 <= labels.1 else 0], state = columns ++ [0]), owner injectivity, h0 = 0.
A row violation would refute that row (es-research section 2). Writes argv[1].
"""
import gzip, hashlib, json, random, re, sys, time
from fractions import Fraction as Fr
from pathlib import Path
sys.path.insert(0, '/home/jay/research/data/theory310-20261113')
from real_sets import hull, chart  # generator only

SRC = Path('/home/jay/research/data/es308-20261114/inputs/source-2650.json.gz')
raw = gzip.decompress(SRC.read_bytes()); assert hashlib.sha256(raw).hexdigest().startswith('e800d5f8')
cat = json.loads(raw); ST = cat['states']; IDX = {tuple(s): i for i, s in enumerate(ST)}
BASE = [(frozenset(r['support']), r['rhs']) for r in cat['constraints']]
text = Path('/home/jay/research/data/formalize-20261122/res118/lean/Res118/Rows.lean').read_text()
EXTRA = [frozenset(int(x) for x in re.findall(r'\d+', r))
         for m in re.finditer(r'def rows[PQUA]_\d+ : List \(List Nat\) := \[(.*?)\n\]', text, re.S)
         for r in re.findall(r'\[([^\[\]]*)\]', m.group(1))]
assert len(EXTRA) == 2025, len(EXTRA)

def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def analyse(pts, check):
    pts = sorted(pts); n = len(pts)
    assert len({p[0] for p in pts}) == n, 'distinct x'
    up = {}
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                o = orient(pts[i], pts[j], pts[k]); assert o != 0, 'collinear'
                up[i, j, k] = o > 0  # cup turn
    cupEnd, capStart = {}, {}
    for v in range(n):
        for u in range(v):
            cupEnd[u, v] = max([cupEnd[t, u] + 1 for t in range(u) if up[t, u, v]] + [2])
    for u in range(n - 1, -1, -1):
        for v in range(n - 1, u, -1):
            capStart[u, v] = max([capStart[v, w] + 1 for w in range(v + 1, n) if not up[u, v, w]] + [2])
    if check:
        if n >= 2 and max(capStart.values()) > 5:
            return None
        for u in range(n):
            ec = max([cupEnd[t, u] for t in range(u)] + [1]); sc = max([capStart[u, w] for w in range(u + 1, n)] + [1])
            if ec >= 6 and sc >= 5:
                return None
        best = 0  # largest convex polygon: cup a..b plus cap a..b
        for a in range(n):
            cu, ca = {}, {}
            for v in range(a + 1, n):
                cu[a, v] = 2; ca[a, v] = 2
                for u in range(a + 1, v):
                    x = [cu[t, u] + 1 for t in [a] + list(range(a + 1, u)) if (t, u) in cu and up[t, u, v]]
                    y = [ca[t, u] + 1 for t in [a] + list(range(a + 1, u)) if (t, u) in ca and not up[t, u, v]]
                    if x: cu[u, v] = max(x)
                    if y: ca[u, v] = max(y)
            ecu, eca = {}, {}
            for (u, v), L in cu.items(): ecu[v] = max(ecu.get(v, 0), L)
            for (u, v), L in ca.items(): eca[v] = max(eca.get(v, 0), L)
            for b in range(a + 1, n):
                best = max(best, ecu.get(b, 0) + eca.get(b, 0) - 2)
        if best > 7:
            return None
    owner = []
    for v in range(n):
        labs = [(6 - capStart[u, v], cupEnd[u, v] - 1) for u in range(v)]
        assert all(1 <= a <= 4 and 1 <= b <= 6 for a, b in labs)
        st = tuple([max([b for a, b in labs if i + 1 <= a] + [0]) for i in range(4)] + [0])
        owner.append(IDX[st])
    assert len(set(owner)) == n, 'owner map injective'
    holes = frozenset(range(154)) - set(owner)
    return {'n': n, 'holes': len(holes), 'h0': 0 in holes,
            'base_viol': sum(1 for s, d in BASE if len(s & holes) < d),
            'extra_viol': sum(1 for s in EXTRA if not (s & holes)),
            'extra_tight': sum(1 for s in EXTRA if len(s & holes) == 1)}, pts

files = ['/home/jay/research/lean/erdos-szekeres-lean/experiments/es8-lower-bound-search-2026-10-11/saturation/witness8.txt'] + \
        ['/home/jay/research/lean/erdos-szekeres-lean/experiments/es8-lower-bound-search-2026-10-11/family/sets/%s.txt' % s
         for s in ('ot0000', 'ot0001m', 'ot0002', 'ot0004m', 'ot0005', 'ot0006')]
NSUB = int(sys.argv[2]) if len(sys.argv) > 2 else 30
rng = random.Random(20261122)
summ = {'full_parts': 0, 'not_residual': 0, 'configs': 0, 'base_viol': 0, 'extra_viol': 0, 'h0_hole': 0,
        'configs_with_tight_extra_row': 0, 'max_n': 0, 'min_holes': 999, 'files': {}}
t0 = time.time()
for f in files:
    lines = [l.split() for l in open(f).read().split('\n') if l.strip()]
    if len(lines[0]) == 1: lines = lines[1:]
    S = [(int(x), int(y)) for x, y in lines]
    summ['files'][f.split('/')[-1]] = {'points': len(S), 'sha256': hashlib.sha256(open(f, 'rb').read()).hexdigest()}
    for a in hull(S):
        P = chart(S, a); n = len(P)
        m = [min((v for v in range(n) if v != u), key=lambda v: (P[v][1] - P[u][1]) / (P[v][0] - P[u][0])) for u in range(n)]
        U = [P[u] for u in range(n) if m[u] > u]
        pts = sorted(U); nU = len(pts)  # junction points G inside U, removed as the partition does
        upU = {(i, j, k): orient(pts[i], pts[j], pts[k]) > 0 for i in range(nU) for j in range(i + 1, nU) for k in range(j + 1, nU)}
        ce, cs = {}, {}
        for v in range(nU):
            for u in range(v): ce[u, v] = max([ce[t, u] + 1 for t in range(u) if upU[t, u, v]] + [2])
        for u in range(nU - 1, -1, -1):
            for v in range(nU - 1, u, -1): cs[u, v] = max([cs[v, w] + 1 for w in range(v + 1, nU) if not upU[u, v, w]] + [2])
        G = {u for u in range(nU) if max([ce[x, u] for x in range(u)] + [1]) >= 6 and max([cs[u, y] for y in range(u + 1, nU)] + [1]) >= 5}
        R = [pts[u] for u in range(nU) if u not in G]
        res = analyse(R, True)
        summ['full_parts'] += 1
        if res is None:
            summ['not_residual'] += 1; continue
        todo = [res]
        for _ in range(NSUB):
            k = rng.randint(max(8, len(R) // 3), len(R) - 1)
            todo.append(analyse(rng.sample(R, k), False))
        for info, _ in todo:
            summ['configs'] += 1
            summ['base_viol'] += info['base_viol'] > 0
            summ['extra_viol'] += info['extra_viol'] > 0
            summ['h0_hole'] += info['h0']
            summ['configs_with_tight_extra_row'] += info['extra_tight'] > 0
            summ['max_n'] = max(summ['max_n'], info['n']); summ['min_holes'] = min(summ['min_holes'], info['holes'])
summ['extra_rows_tested'] = len(EXTRA)
summ['seconds'] = round(time.time() - t0, 1)
print(json.dumps(summ, indent=1))
Path(sys.argv[1]).write_text(json.dumps(summ, indent=1) + '\n')
