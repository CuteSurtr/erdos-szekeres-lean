"""Find a small subset of rows that already excludes `budget` holes (CP-SAT assumption cores, a few
shrinking passes).  usage: subset_core.py <budget> <out.json> [passes]
Input rows: rows_cycle.json + cores.jsonl + trows.jsonl (all current rows).  Output: list of
{'support','demand','kind'} where kind is 'cycle' or 'coupled'."""
import json, sys, time, os, random
from ortools.sat.python import cp_model
import etv_common as ec
from etv_common import N
HERE = os.path.dirname(os.path.abspath(__file__)); P = lambda f: os.path.join(HERE, f)
budget = int(sys.argv[1]); out = sys.argv[2]; passes = int(sys.argv[3]) if len(sys.argv) > 3 else 3
rows = {}
for s, d in json.load(open(P('rows_cycle.json'))): rows[tuple(sorted(s))] = (d, 'cycle')
for fn in ('cores.jsonl', 'trows.jsonl'):
    for line in open(P(fn)):
        s = tuple(sorted(json.loads(line)['support']))
        if s not in rows: rows[s] = (1, 'coupled')
keys = list(rows)
def infeasible_core(keys, seed):
    m = cp_model.CpModel(); h = [m.NewBoolVar(f'h{i}') for i in range(N)]
    for i in ec.FIXED_OCC: m.Add(h[i] == 0)
    m.Add(sum(h) <= budget)
    b = []
    for k in keys:
        lit = m.NewBoolVar(''); b.append(lit)
        m.Add(sum(h[i] for i in k) >= rows[k][0]).OnlyEnforceIf(lit)
    m.AddAssumptions(b)
    so = cp_model.CpSolver(); so.parameters.num_workers = 1; so.parameters.max_time_in_seconds = 900
    so.parameters.random_seed = seed
    st = so.Solve(m)
    if st != cp_model.INFEASIBLE: return so.StatusName(st), None
    core = set(so.SufficientAssumptionsForInfeasibility())
    return 'INFEASIBLE', [k for k, lit in zip(keys, b) if lit.Index() in core]
t0 = time.time(); cur = keys
for p in range(passes):
    st, core = infeasible_core(cur, p)
    print('pass', p, st, 'rows in', len(cur), 'core', None if core is None else len(core), round(time.time() - t0, 1), flush=True)
    if core is None: break
    if len(core) == len(cur): cur = core; break
    cur = core
json.dump([{'support': list(k), 'demand': rows[k][0], 'kind': rows[k][1]} for k in cur], open(out, 'w'))
print('subset', len(cur), 'cycle', sum(rows[k][1] == 'cycle' for k in cur), 'coupled', sum(rows[k][1] == 'coupled' for k in cur))
