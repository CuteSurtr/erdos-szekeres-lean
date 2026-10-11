"""Exploratory: minimum number of residual holes under the 2,650-row catalog, state 0 occupied."""
import gzip, json, sys, time
from ortools.sat.python import cp_model
src='experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
d=json.load(gzip.open(src)); C=d['constraints']
workers=int(sys.argv[1]); limit=float(sys.argv[2]); out=sys.argv[3]; seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
m=cp_model.CpModel(); h=[m.NewBoolVar(f'h{i}') for i in range(154)]
m.Add(h[0]==0)
for c in C: m.Add(sum(h[i] for i in c['support'])>=c['rhs'])
m.Minimize(sum(h))
s=cp_model.CpSolver(); s.parameters.num_workers=workers; s.parameters.max_time_in_seconds=limit
s.parameters.log_search_progress=True; s.parameters.random_seed=seed
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s2): super().__init__(); s2.t=time.time()
    def on_solution_callback(s2):
        holes=[i for i in range(154) if s2.Value(h[i])]
        ok=all(len(set(holes)&set(c['support']))>=c['rhs'] for c in C) and 0 not in holes
        with open(out,'a') as f: f.write(json.dumps({'t':time.time()-s2.t,'holes':len(holes),'replay_ok':ok,'set':holes})+'\n')
st=s.Solve(m, CB())
with open(out,'a') as f: f.write(json.dumps({'final':s.StatusName(st),'objective':s.ObjectiveValue(),'bound':s.BestObjectiveBound(),'wall':s.WallTime()})+'\n')
