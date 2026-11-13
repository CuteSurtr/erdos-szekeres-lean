"""Exact cycle-row optimum by lazy separation, RC2 as the exact solver (COMPUTED).  Writes rows_cycle.json."""
import json, time, random, sys
from pysat.formula import WCNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2
import etv_common as ec
from etv_common import N
from cyclists import masks, find_lists, extend
M = masks(ec.TT); rng = random.Random(5); rows = {}
def rc2_opt(rows):
    pool = IDPool(start_from=N + 1); w = WCNF(); var = lambda i: i + 1
    for i in ec.FIXED_OCC: w.append([-var(i)])
    for s, d in rows.items():
        L = [var(i) for i in s if i not in ec.FIXED_OCC]
        if d == 1: w.append(L)
        else:
            for c in CardEnc.atleast(lits=L, bound=d, vpool=pool, encoding=EncType.seqcounter).clauses: w.append(c)
    for i in range(N):
        if i not in ec.FIXED_OCC: w.append([-var(i)], weight=1)
    with RC2(w, solver='g4', adapt=True, exhaust=True, minz=True, trim=5) as r:
        m = r.compute(); return r.cost, [i for i in range(N) if m[i] > 0]
t0 = time.time(); it = 0
while True:
    it += 1
    cost, H = rc2_opt(rows)
    occ = [i for i in range(N) if i not in H]
    L = find_lists(M, occ, 8, limit=80, rng=rng)
    for l in L:
        E = extend(ec.TT, l, rng); rows[tuple(sorted(E))] = len(E) - 7
    print(json.dumps({'it': it, 'rows': len(rows), 'opt': cost, 'new': len(L), 't': round(time.time() - t0, 1)}), flush=True)
    if not L: break
json.dump([[list(k), v] for k, v in rows.items()], open('rows_cycle.json', 'w'))
json.dump({'min_holes': cost, 'holes': H}, open('cyc_opt.json', 'w'))
print('FINAL', cost, 'capacity', N - cost)
