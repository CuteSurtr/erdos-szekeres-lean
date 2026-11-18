"""Pool oracle for a slice t (HEURISTIC / COMPUTED): CP-SAT over h0 = 0, the 2,650 rows, the certified rows AND every
pooled transported row (newrows.json, fnewrows.json, lonewrows.json; valid if the transport is sound, but only the
certified ones are used in exact claims), with h(F) >= t, h(Lo) >= 33 - t, sum h <= 33.
 FEASIBLE  -> a 33-hole vector that no pooled row kills: a candidate obstruction (needs new cores).
 INFEASIBLE-> (COMPUTED) the slice is empty once enough pooled rows are certified.
Usage: poolfind.py t seconds workers"""
import json, os, sys, time
from lo_common import *
from ortools.sat.python import cp_model
t, secs, W = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
cs = certified_supports(); pool = pooled()
m = cp_model.CpModel(); h = [m.NewBoolVar(f'h{i}') for i in range(N)]
m.Add(h[0] == 0)
for s, d in ROWS: m.Add(sum(h[i] for i in s) >= d)
seen = set()
for s in cs + pool:
    s = tuple(s)
    if s in seen: continue
    seen.add(s); m.AddBoolOr([h[i] for i in s])
m.Add(sum(h[i] for i in F) >= t); m.Add(sum(h[i] for i in LO) >= 33 - t); m.Add(sum(h) <= 33)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = secs; sol.parameters.num_workers = W
t0 = time.time(); st = sol.Solve(m); name = sol.StatusName(st)
out = {'slice': t, 'status': name, 'demand_one_rows': len(seen), 'seconds': round(time.time() - t0, 1), 'workers': W, 't': time.strftime('%H:%M:%S')}
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    H = [i for i in range(N) if sol.Value(h[i])]
    out.update(holes=H, F_occupied=len(set(F) - set(H)), Lo_occupied=len(set(LO) - set(H)))
print(json.dumps(out), flush=True)
open(os.path.join(HERE, 'poolfind.jsonl'), 'a').write(json.dumps(out) + '\n')
