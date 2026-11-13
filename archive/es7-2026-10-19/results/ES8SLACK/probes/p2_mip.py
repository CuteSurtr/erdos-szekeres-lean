"""Probe 2: primal MIP search (HiGHS via scipy.milp) for low-hole Boolean assignments.
Upper bound on min sum h.  Usage: p2_mip.py {bal|res} seconds [fix0 indices comma]"""
import sys, time, json
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from common import *

which, secs = sys.argv[1], float(sys.argv[2])
fix0 = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 and sys.argv[3] else []
path = BAL_V2 if which == 'bal' else RES_2650
states, rows = load(path)
n = len(states)
A, b = matrix(n, rows)
lb = np.zeros(n); ub = np.ones(n)
for i in fix0:
    ub[i] = 0
t = time.time()
res = milp(np.ones(n), integrality=np.ones(n), bounds=Bounds(lb, ub),
           constraints=[LinearConstraint(A, b, np.inf)],
           options={'time_limit': secs, 'disp': False, 'mip_rel_gap': 0})
el = time.time() - t
out = {'which': which, 'fix_occupied': fix0, 'status': int(res.status), 'message': res.message,
       'seconds': round(el, 1), 'dual_bound': getattr(res, 'mip_dual_bound', None)}
if res.x is not None:
    holes = [i for i in range(n) if res.x[i] > 0.5]
    out['holes'] = holes
    out['num_holes'] = len(holes)
    out['violated_exact'] = check_exact(rows, holes)
print(json.dumps(out))
