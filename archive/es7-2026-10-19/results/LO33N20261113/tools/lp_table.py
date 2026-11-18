"""LP values (HiGHS, floating point: a guide only, never evidence) for pairs (c, c2)."""
import sys, json
import numpy as np, highspy
from lo_common import *
cert = certified_supports()
def lp(c, c2, use_cert=True):
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
    v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
    h.changeColBounds(0, 0, 0)
    for s, d in ROWS: h.addConstr(h.qsum(v[i] for i in s) >= d)
    if use_cert:
        for s in cert: h.addConstr(h.qsum(v[i] for i in s) >= 1)
    if 84 - c > 0: h.addConstr(h.qsum(v[i] for i in F) >= 84 - c)
    if 70 - c2 > 0: h.addConstr(h.qsum(v[i] for i in LO) >= 70 - c2)
    h.run(); x = np.array(h.getSolution().col_value)
    return h.getObjectiveValue(), x[F].sum(), x[LO].sum()
print('base', lp(84, 70))
print('Lo alone:')
for c2 in range(50, 62): print(' c2', c2, [round(z, 3) for z in lp(84, c2)])
print('slices (84-t, 37+t):')
for t in range(17, 27): print(' t', t, 'pair', (84 - t, 37 + t), [round(z, 3) for z in lp(84 - t, 37 + t)])
print('c=65:')
for c2 in range(55, 64): print(' (65,%d)' % c2, [round(z, 3) for z in lp(65, c2)])
