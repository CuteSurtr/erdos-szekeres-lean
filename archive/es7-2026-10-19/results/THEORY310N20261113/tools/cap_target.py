#!/usr/bin/env python3
"""How strong must a capacity row on F = {residual states with f1 >= 5} be?

Owners of F-states form a 5-cap-free, octagon-free set (junction freeness), so
|O cap F| <= N(5-cap, 8-gon).  For c in a range, test with CP-SAT whether a
0/1 hole vector with state 0 occupied, all 2,650 rows, sum(h) <= budget and
|O cap F| <= c exists.  Infeasible at budget 33 means the capacity c alone
would give residual budget 33, i.e. ES(8) <= 309 together with balanced 64.
"""
import gzip, json, sys, time
from ortools.sat.python import cp_model

src = json.load(gzip.open('/home/jay/research/lean/erdos-szekeres-lean/experiments/'
                          'omission-residual32-rank-global-2026-10-10/source-2650.json.gz'))
S = src['states']; C = src['constraints']
F = [i for i, s in enumerate(S) if s[0] >= 5]
assert len(F) == 84

def test(c, budget, tl, extra=()):
    m = cp_model.CpModel()
    h = [m.NewBoolVar(f'h{i}') for i in range(len(S))]
    m.Add(h[0] == 0)
    for r in list(C) + list(extra):
        m.Add(sum(h[i] for i in r['support']) >= r['rhs'])
    m.Add(sum(h) <= budget)
    m.Add(sum(h[i] for i in F) >= len(F) - c)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl
    sv.parameters.num_workers = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    st = sv.Solve(m)
    holes = [i for i in range(len(S)) if st in (cp_model.FEASIBLE, cp_model.OPTIMAL) and sv.Value(h[i])]
    return sv.StatusName(st), holes

if __name__ == '__main__':
    budget = int(sys.argv[1]); tl = float(sys.argv[2])
    out = {}
    for c in [int(x) for x in sys.argv[4].split(',')]:
        t0 = time.time()
        st, holes = test(c, budget, tl)
        nF = sum(1 for i in holes if i in F)
        print(f'c={c} budget={budget} status={st} holes={len(holes)} F-holes={nF} t={time.time()-t0:.0f}s', flush=True)
        out[c] = {'status': st, 'holes': holes}
    json.dump(out, open(f'cap_target_b{budget}.json', 'w'))
