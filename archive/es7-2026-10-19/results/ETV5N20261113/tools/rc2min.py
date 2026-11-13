"""Exact minimum of holes over the current rows with pysat RC2 (core-guided MaxSAT).  COMPUTED.
usage: rc2min.py [rowsfile-or-'all'] """
import json, sys, time, os
from pysat.formula import WCNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2, RC2Stratified
import etv_common as ec
from etv_common import N
def load_all():
    rows = {}
    for s, d in json.load(open('rows_cycle.json')): rows[tuple(sorted(s))] = max(d, rows.get(tuple(sorted(s)), 0))
    for fn in ('cores.jsonl', 'trows.jsonl'):
        if os.path.exists(fn):
            for line in open(fn):
                s = tuple(sorted(json.loads(line)['support'])); rows[s] = max(1, rows.get(s, 0))
    return rows
def build(rows):
    pool = IDPool(start_from=N + 1); w = WCNF(); var = lambda i: i + 1
    for i in ec.FIXED_OCC: w.append([-var(i)])
    for s, d in rows.items():
        L = [var(i) for i in s if i not in ec.FIXED_OCC]
        if d == 1: w.append(L)
        else:
            for c in CardEnc.atleast(lits=L, bound=d, vpool=pool, encoding=EncType.seqcounter).clauses: w.append(c)
    for i in range(N):
        if i not in ec.FIXED_OCC: w.append([-var(i)], weight=1)
    return w
if __name__ == '__main__':
    t = time.time()
    rows = load_all() if len(sys.argv) < 2 or sys.argv[1] == 'all' else {tuple(sorted(s)): d for s, d in json.load(open(sys.argv[1]))}
    w = build(rows)
    with RC2(w, solver='g4', adapt=True, exhaust=True, minz=True, trim=5) as r:
        m = r.compute()
        H = [i for i in range(N) if m[i] > 0]
        print(json.dumps({'rows': len(rows), 'rc2_cost': r.cost, 'holes': H, 'seconds': round(time.time() - t, 1)}), flush=True)
