"""MIP: min holes with the 2,650 rows, h0 = 0 and h(F) >= 84 - c.  Does a capacity
c in 57..60 force >= 34 holes (integer reasoning beyond the LP threshold 56)?"""
import sys, time
c = int(sys.argv[1]); tl = float(sys.argv[2]); sys.argv = [sys.argv[0]]
import numpy as np, highspy
from cap_lp import res, fam
RS, RC = res['states'], res['constraints']
F = fam(RS, lambda s: s[0] >= 5)
h = highspy.Highs(); h.setOptionValue('threads', 1); h.setOptionValue('time_limit', tl)
h.setOptionValue('output_flag', True); h.setOptionValue('log_to_console', True)
h.setOptionValue('mip_rel_gap', 0.0)
inf = highspy.kHighsInf
for i in range(154):
    h.addVar(0.0, 0.0 if i == 0 else 1.0); h.changeColCost(i, 1.0); h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
for r in list(RC) + [{'support': F, 'rhs': 84 - c}]:
    h.addRow(float(r['rhs']), inf, len(r['support']), np.array(r['support'], dtype=np.int32), np.ones(len(r['support'])))
t0 = time.time(); h.run(); info = h.getInfo()
sol = h.getSolution().col_value
holes = [i for i in range(154) if sol[i] > 0.5]
import json; json.dump({'c': c, 'status': str(h.getModelStatus()), 'holes': holes, 'F_occupied': sum(1 for i in F if i not in holes)}, open(f'cap_mip{c}_sol.json', 'w'))
print(f'c={c}: status {h.getModelStatus()} incumbent {info.objective_function_value} dual bound {info.mip_dual_bound} nodes {info.mip_node_count} t={time.time()-t0:.0f}s')
