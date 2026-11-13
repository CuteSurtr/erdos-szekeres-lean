"""Global CP-SAT in optimisation mode: minimise sum h (h0=0) over catalog+templates+newrows.
Logs incumbents/bounds; any incumbent with <= 33 holes is appended to vectors.json for the loop.
A proven lower bound >= 34 would mean (numerically, uncertified) residual budget 33 is excluded."""
import json, os, sys, time, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from mip import load_rows
from common import N, check
from ortools.sat.python import cp_model
DL = float(sys.argv[1]); workers = int(sys.argv[2])
vp = os.path.join(HERE, 'vectors.json')
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(self, h, rows):
        super().__init__(); self.h = h; self.rows = rows; self.found = False
    def on_solution_callback(self):
        H = [i for i in range(N) if self.Value(self.h[i])]
        rec = {'t': time.strftime('%H:%M:%S'), 'incumbent': len(H), 'bound': self.BestObjectiveBound()}
        if len(H) <= 33 and not check(H, self.rows):
            vs = json.load(open(vp)) if os.path.exists(vp) else []
            if H not in vs:
                vs.append(H); json.dump(vs, open(vp + '.tmp', 'w')); os.replace(vp + '.tmp', vp)
            rec['holes'] = H
            self.found = True
            self.StopSearch()
        with open(os.path.join(HERE, 'finder.jsonl'), 'a') as f: f.write(json.dumps(rec) + '\n')
while time.time() < DL - 120:
    rows, _, _ = load_rows()
    m = cp_model.CpModel()
    h = [m.NewBoolVar(f'h{i}') for i in range(N)]
    m.Add(h[0] == 0)
    for s, d in rows: m.Add(sum(h[i] for i in s) >= d)
    CAPC = os.environ.get('CAPC')
    if CAPC:
        from common import STATES
        F = [i for i in range(N) if STATES[i][0] >= 5]
        m.Add(sum(h[i] for i in F) >= 84 - int(CAPC))
    m.Minimize(sum(h))
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = min(400, DL - time.time() - 60)
    sol.parameters.num_workers = workers
    sol.parameters.random_seed = random.randrange(10**6)
    cb = CB(h, rows)
    st = sol.Solve(m, cb)
    if cb.found:
        # wait (max 8 min) for the CEGAR loop to add rows refuting it, then start a fresh round
        npath = os.path.join(HERE, 'newrows.json'); t0 = os.path.getmtime(npath); w = time.time()
        while os.path.getmtime(npath) == t0 and time.time() - w < 480: time.sleep(10)
    rec = {'t': time.strftime('%H:%M:%S'), 'round_status': sol.StatusName(st), 'rows': len(rows),
           'best': sol.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
           'bound': sol.BestObjectiveBound()}
    rec['capc'] = os.environ.get('CAPC')
    with open(os.path.join(HERE, 'finder.jsonl'), 'a') as f: f.write(json.dumps(rec) + '\n')
    if st == cp_model.OPTIMAL and sol.ObjectiveValue() >= 34:
        break
