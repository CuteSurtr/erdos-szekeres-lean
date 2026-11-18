"""Guide LP (floating point, not evidence): for slice t, sub-slice by k = h(F7), F7 = states with f1 = 6.
phi(k) = min h(Lo) s.t. rows, h(F7) <= k, h(F6) <= t - k.  Sub-slice is LP-dead iff phi > 33 - t or infeasible."""
import sys, json
import numpy as np, highspy
from lo_common import *
cert = certified_supports()
F7 = [i for i in F if STATES[i][0] == 6]; F6 = [i for i in F if STATES[i][0] == 5]
print(len(F7), len(F6))
def phi(t, k):
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
    L = set(LO)
    v = [h.addVariable(lb=0, ub=1, obj=(1.0 if i in L else 0.0)) for i in range(N)]
    h.changeColBounds(0, 0, 0)
    for s, d in ROWS: h.addConstr(h.qsum(v[i] for i in s) >= d)
    for s in cert: h.addConstr(h.qsum(v[i] for i in s) >= 1)
    h.addConstr(h.qsum(v[i] for i in F7) <= k); h.addConstr(h.qsum(v[i] for i in F6) <= t - k)
    h.run()
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal: return None
    return round(h.getObjectiveValue(), 3)
for t in (19, 20, 21):
    print('t', t, 'need phi <=', 33 - t, {k: phi(t, k) for k in range(5, 14)})
