"""In/out coupling test (exact CP-SAT): in-occupancy x, out-occupancy y (both satisfy the cycle rows),
perfect matching between occupied in-states and occupied out-states through junction-compatible pairs.
Compatible(s,t): for all cells (a,b) in s and (a2,b2) in t: a+a2 <= 4 or b+b2 <= 4."""
import sys, json, time
import fl
from fl import *
from ortools.sat.python import cp_model
rows = json.load(open('cyc_base_A4B4.json'))['rows']
CE = ec.CELLS
def compat(s, t):
    return all(a + a2 <= 4 or b + b2 <= 4 for (a, b) in CE[s] for (a2, b2) in CE[t])
C = [[compat(s, t) for t in range(N)] for s in range(N)]
print('compatible pairs', sum(map(sum, C)), 'of', N * N)
m = cp_model.CpModel()
x = [m.NewBoolVar(f'x{i}') for i in range(N)]; y = [m.NewBoolVar(f'y{i}') for i in range(N)]
z = {(s, t): m.NewBoolVar(f'z{s}_{t}') for s in range(N) for t in range(N) if C[s][t]}
for sup, d in rows:
    m.Add(sum(1 - x[i] for i in sup) >= d); m.Add(sum(1 - y[i] for i in sup) >= d)
for s in range(N): m.Add(sum(z[s, t] for t in range(N) if C[s][t]) == x[s])
for t in range(N): m.Add(sum(z[s, t] for s in range(N) if C[s][t]) == y[t])
# leftmost point: in-state 0 (empty), rightmost point: out-state 0
m.Add(x[0] == 1); m.Add(y[0] == 1)
m.Maximize(sum(x))
so = cp_model.CpSolver(); so.parameters.num_workers = 1; so.parameters.max_time_in_seconds = 50
st = so.Solve(m)
print(so.StatusName(st), 'max occupied', so.ObjectiveValue(), 'bound', so.BestObjectiveBound())
