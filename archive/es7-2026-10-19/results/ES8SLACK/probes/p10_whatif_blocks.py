"""Probe 10 (what-if, NOT a proof): if the residual block capacity were c instead of 22 (block rows
(28,6) -> (28, 28-c)), how far would the residual LP and the min-hole value move?
Usage: p10_whatif_blocks.py capacity seconds"""
import sys, json, time
import numpy as np
from scipy.optimize import milp, linprog, LinearConstraint, Bounds
from common import *

cap, secs = int(sys.argv[1]), float(sys.argv[2])
states, rows = load(RES_2650)
n = len(states)
blk = [k for k in json.load(open('res_block_rows.json')) if len(rows[k][0]) == 28 and rows[k][1] == 6]
rows2 = list(rows)
for k in blk:
    rows2[k] = (rows[k][0], 28 - cap)
A, b = matrix(n, rows2)
ub = np.ones(n); ub[0] = 0
lp = linprog(np.ones(n), A_ub=-A, b_ub=-b, bounds=list(zip(np.zeros(n), ub)), method='highs').fun
res = milp(np.ones(n), integrality=np.ones(n), bounds=Bounds(np.zeros(n), ub),
           constraints=[LinearConstraint(A, b, np.inf)], options={'time_limit': secs, 'disp': False})
holes = sorted(i for i in range(n) if res.x is not None and res.x[i] > 0.5)
print(json.dumps({'capacity': cap, 'block_rows_changed': len(blk), 'lp': lp, 'mip_status': res.message,
                  'best_holes': len(holes), 'dual_bound': getattr(res, 'mip_dual_bound', None),
                  'exact_ok': not check_exact(rows2, holes)}))
