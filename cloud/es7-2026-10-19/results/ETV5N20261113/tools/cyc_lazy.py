"""Exact optimum of the cycle-row system by lazy separation + CP-SAT (COMPUTED).
usage: cyc_lazy.py <table: TT|TTR> <out.json> [workers]"""
import sys, json, time, random
from ortools.sat.python import cp_model
import etv_common as ec
from cyclists import masks, find_lists, extend
T = getattr(ec, sys.argv[1]); out = sys.argv[2]; W = int(sys.argv[3]) if len(sys.argv) > 3 else 2
M = masks(T); rng = random.Random(5)
rows = {}
def solve(rows):
    m = cp_model.CpModel(); h = [m.NewBoolVar(f'h{i}') for i in range(ec.N)]
    for i in ec.FIXED_OCC: m.Add(h[i] == 0)
    for s, d in rows.items(): m.Add(sum(h[i] for i in s) >= d)
    m.Minimize(sum(h))
    so = cp_model.CpSolver(); so.parameters.num_workers = W; so.parameters.max_time_in_seconds = 600
    st = so.Solve(m)
    return so.StatusName(st), [i for i in range(ec.N) if so.Value(h[i])], so.BestObjectiveBound()
t0 = time.time(); it = 0
while True:
    it += 1
    st, H, bd = solve(rows)
    occ = [i for i in range(ec.N) if i not in H]
    L = find_lists(M, occ, 8, limit=60, rng=rng)
    add = 0
    for l in L:
        E = extend(T, l, rng); key = frozenset(E)
        if key not in rows: rows[key] = len(E) - 7; add += 1
    print(f'it {it} rows {len(rows)} status {st} holes {len(H)} bound {bd} new {add} t={time.time()-t0:.1f}', flush=True)
    if not L: break
json.dump({'table': sys.argv[1], 'status': st, 'holes': H, 'min_holes': len(H),
           'rows': [[sorted(k), v] for k, v in rows.items()]}, open(out, 'w'))
print('FINAL', st, 'min holes', len(H), 'capacity', ec.N - len(H))
