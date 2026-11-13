"""Exact rational dual certificate: rows + capacity row => sum(h) >= bound."""
import sys, json, gzip
from fractions import Fraction as Fr
import numpy as np, highspy
sys.argv_saved = sys.argv; sys.argv = [sys.argv[0]]
from cap_lp import res, bal, fam
def certify(S, C, extra, fixed0, label):
    rows = list(C) + list(extra); n = len(S)
    h = highspy.Highs(); h.silent(); h.setOptionValue('threads', 1)
    inf = highspy.kHighsInf
    for i in range(n):
        h.addVar(0.0, 0.0 if (fixed0 and i == 0) else 1.0); h.changeColCost(i, 1.0)
    for r in rows:
        sup = r['support']; h.addRow(float(r['rhs']), inf, len(sup), np.array(sup, dtype=np.int32), np.ones(len(sup)))
    h.run(); y = h.getSolution().row_dual; val = h.getInfo().objective_function_value
    yq = [max(Fr(0), Fr(v).limit_denominator(1000)) for v in y]
    load = [Fr(0)] * n
    for r, w in zip(rows, yq):
        if w:
            for i in r['support']: load[i] += w
    z = [max(Fr(0), load[i] - 1) if not (fixed0 and i == 0) else Fr(0) for i in range(n)]
    # h0 fixed to 0: its column has no constraint (any load allowed)
    bound = sum(w * r['rhs'] for r, w in zip(rows, yq)) - sum(z)
    print(f'{label}: LP {val:.6f}  exact dual bound {bound} = {float(bound):.6f}  => integer sum(h) >= {-(-bound.numerator // bound.denominator)}')
    return bound
RS, RC = res['states'], res['constraints']; BS, BC = bal['states'], bal['constraints']
F = fam(RS, lambda s: s[0] >= 5)
for c in [56, 55, 49]:
    certify(RS, RC, [{'support': F, 'rhs': 84 - c}], True, f'residual + h(F) >= {84-c} (capacity {c})')
Hi = fam(BS, lambda s: s[0] == 5)
for c in [78, 76]:
    certify(BS, BC, [{'support': Hi, 'rhs': 126 - c}], False, f'balanced + h(Hi) >= {126-c} (capacity {c})')
