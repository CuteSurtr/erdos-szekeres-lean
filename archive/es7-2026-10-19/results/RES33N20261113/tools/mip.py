"""Find a 0/1 residual hole vector with h0 = 0, sum <= budget, satisfying all rows (CP-SAT)."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROWS, N, check
from ortools.sat.python import cp_model

def load_rows(extra_files=('templates.json', 'newrows.json')):
    rows = list(ROWS)
    seen = {s for s, d in rows if d >= 1}
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = json.load(open(os.path.join(here, 'templates.json')))
    ntpl = 0
    for name, v in tpl.items():
        for s in v['supports']:
            s = tuple(sorted(s))
            if s not in seen:
                seen.add(s); rows.append((s, 1)); ntpl += 1
    nnew = 0
    p = os.path.join(here, 'newrows.json')
    if os.path.exists(p):
        for r in json.load(open(p)):
            s = tuple(sorted(r['support']))
            if s not in seen:
                seen.add(s); rows.append((s, 1)); nnew += 1
    return rows, ntpl, nnew

def find(rows, budget=33, seconds=120, workers=4, seed=0, forbid=()):
    m = cp_model.CpModel()
    h = [m.NewBoolVar(f'h{i}') for i in range(N)]
    m.Add(h[0] == 0)
    for s, d in rows:
        m.Add(sum(h[i] for i in s) >= d)
    m.Add(sum(h) <= budget)
    for holes in forbid:  # no-good: differ from a previous vector
        m.AddBoolOr([h[i].Not() for i in holes] + [h[i] for i in range(N) if i not in set(holes)])
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = seconds
    sol.parameters.num_workers = workers
    sol.parameters.random_seed = seed
    st = sol.Solve(m)
    name = sol.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        holes = [i for i in range(N) if sol.Value(h[i])]
        assert not check(holes, rows) and 0 not in holes and len(holes) <= budget
        return name, holes, sol.WallTime()
    return name, None, sol.WallTime()

if __name__ == '__main__':
    rows, ntpl, nnew = load_rows()
    print('rows', len(rows), 'templates', ntpl, 'new', nnew, flush=True)
    st, holes, t = find(rows, seconds=float(sys.argv[1]) if len(sys.argv) > 1 else 120)
    print(st, len(holes) if holes else None, holes, round(t, 1))
