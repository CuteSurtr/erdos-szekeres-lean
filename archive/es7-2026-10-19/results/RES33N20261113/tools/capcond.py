"""Conditional test: add the capacity row 'at most c of F occupied' (F = 84 residual states with f1 >= 5;
by Lemma A of THEORY310N20261113, |O ∩ F| <= N(cap<=4), the octagon-free 5-cap-free maximum) to all rows.
min sum h (h0=0). If the optimum is >= 34, then N(cap<=4) <= c implies residual budget 33 is excluded,
i.e. ES(8) <= 309 (numerical solver result; uncertified)."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
c = int(sys.argv[1]); solver = sys.argv[2]; DL = float(sys.argv[3])
from common import N, STATES, check
F = [i for i in range(N) if STATES[i][0] >= 5]
assert len(F) == 84
out = {'c': c, 'solver': solver, 'start': time.strftime('%H:%M:%S')}
if solver == 'highs':
    import highspy
    from hfind import load_rows
    rows = load_rows()
    h = highspy.Highs(); h.setOptionValue('output_flag', True); h.setOptionValue('log_to_console', False)
    h.setOptionValue('log_file', f'capcond_{c}.log'); h.setOptionValue('threads', 1)
    h.setOptionValue('time_limit', DL - time.time())
    v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
    h.changeColBounds(0, 0, 0)
    for i in range(N): h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
    for s, d in rows: h.addConstr(h.qsum(v[i] for i in s) >= d)
    h.addConstr(h.qsum(v[i] for i in F) >= 84 - c)
    h.run(); info = h.getInfo()
    out.update(status=h.modelStatusToString(h.getModelStatus()), best=info.objective_function_value,
               bound=info.mip_dual_bound, nodes=info.mip_node_count, rows=len(rows) + 1)
else:
    from mip import load_rows
    from ortools.sat.python import cp_model
    rows, _, _ = load_rows()
    m = cp_model.CpModel(); hv = [m.NewBoolVar(f'h{i}') for i in range(N)]
    m.Add(hv[0] == 0)
    for s, d in rows: m.Add(sum(hv[i] for i in s) >= d)
    m.Add(sum(hv[i] for i in F) >= 84 - c)
    m.Minimize(sum(hv))
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = DL - time.time()
    sol.parameters.num_workers = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    st = sol.Solve(m)
    out.update(status=sol.StatusName(st), best=sol.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
               bound=sol.BestObjectiveBound(), rows=len(rows) + 1)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        H = [i for i in range(N) if sol.Value(hv[i])]; out['holes'] = H
out['end'] = time.strftime('%H:%M:%S')
with open(os.path.join(HERE, 'capcond.jsonl'), 'a') as f: f.write(json.dumps(out) + '\n')
print(json.dumps(out))
