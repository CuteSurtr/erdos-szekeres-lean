"""Probe 4: CP-SAT minimisation of holes in the balanced V2 system (primal upper bound + dual bound).
Usage: p4_cpsat.py workers seconds out.jsonl [hintfile.json]"""
import os, sys, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from ortools.sat.python import cp_model

workers, limit, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
hint = json.load(open(sys.argv[4]))['holes'] if len(sys.argv) > 4 else None
which = 'bal'
states, rows = load(BAL_V2)
n = len(states)
m = cp_model.CpModel()
h = [m.NewBoolVar(f'h{i}') for i in range(n)]
for s, d in rows:
    m.Add(sum(h[i] for i in s) >= d)
m.Minimize(sum(h))
if hint:
    H = set(hint)
    for i in range(n):
        m.AddHint(h[i], 1 if i in H else 0)
sv = cp_model.CpSolver()
sv.parameters.num_workers = workers
sv.parameters.max_time_in_seconds = limit
sv.parameters.random_seed = 7


class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s2):
        super().__init__(); s2.t = time.time()

    def on_solution_callback(s2):
        holes = [i for i in range(n) if s2.Value(h[i])]
        bad = check_exact(rows, holes)
        with open(out, 'a') as f:
            f.write(json.dumps({'t': round(time.time() - s2.t, 1), 'holes': len(holes), 'violated': len(bad),
                                'bound': s2.BestObjectiveBound(), 'set': holes}) + '\n')


st = sv.Solve(m, CB())
with open(out, 'a') as f:
    f.write(json.dumps({'final': sv.StatusName(st), 'objective': sv.ObjectiveValue(),
                        'bound': sv.BestObjectiveBound(), 'wall': sv.WallTime()}) + '\n')
