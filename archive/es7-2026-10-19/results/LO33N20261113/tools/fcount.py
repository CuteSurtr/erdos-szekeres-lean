"""Count integer F-patterns: hole sets inside F with exactly t holes satisfying every row whose support lies inside F
(2,650 Lean rows + certified rows).  CP-SAT enumeration, COMPUTED only.  Usage: fcount.py t limit seconds"""
import sys, json, time
from lo_common import *
from ortools.sat.python import cp_model
t, limit, secs = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
Fs = set(F); cert = certified_supports()
rows = [(s, d) for s, d in ROWS if set(s) <= Fs] + [(tuple(s), 1) for s in cert if set(s) <= Fs]
m = cp_model.CpModel(); h = {i: m.NewBoolVar(f'h{i}') for i in F}
for s, d in rows: m.Add(sum(h[i] for i in s) >= d)
m.Add(sum(h.values()) == t)
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        super().__init__(); self.n = 0; self.sols = []
    def on_solution_callback(self):
        self.n += 1
        if len(self.sols) < 2000: self.sols.append([i for i in F if self.Value(h[i])])
        if self.n >= limit: self.StopSearch()
cb = CB(); sol = cp_model.CpSolver(); sol.parameters.enumerate_all_solutions = True; sol.parameters.num_workers = 1
sol.parameters.max_time_in_seconds = secs
t0 = time.time(); st = sol.Solve(m, cb)
print(json.dumps({'t': t, 'rows_in_F': len(rows), 'status': sol.StatusName(st), 'count': cb.n, 'seconds': round(time.time() - t0, 1)}))
json.dump(cb.sols, open(f'fpat_t{t}.json', 'w'))
