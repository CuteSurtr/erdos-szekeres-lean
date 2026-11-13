import sys
from fractions import Fraction as Fr
import numpy as np, highspy, json
sys.argv=[sys.argv[0]]
from cap_lp import res, fam
RS, RC = res['states'], res['constraints']
F = fam(RS, lambda s: s[0] >= 5)
rows = list(RC) + [{'support': F, 'rhs': 28}]
h = highspy.Highs(); h.silent(); h.setOptionValue('threads', 1); inf = highspy.kHighsInf
for i in range(154):
    h.addVar(0.0, 0.0 if i == 0 else 1.0); h.changeColCost(i, 1.0)
for r in rows:
    h.addRow(float(r['rhs']), inf, len(r['support']), np.array(r['support'], dtype=np.int32), np.ones(len(r['support'])))
h.run(); y = h.getSolution().row_dual
yq = [max(Fr(0), Fr(v).limit_denominator(1000)) for v in y]
nz = [(k, w) for k, w in enumerate(yq) if w]
print('nonzero duals', len(nz), 'denominators', sorted({w.denominator for _, w in nz}))
w3 = {k: int(6 * w) for k, w in nz if (6 * w).denominator == 1}
print('all integral after x6:', len(w3) == len(nz))
load = [0] * 154
for k, w in w3.items():
    for i in rows[k]['support']: load[i] += w
D = sum(w * rows[k]['rhs'] for k, w in w3.items())
C = 6
excess = sum(max(0, load[i] - C) for i in range(1, 154))
print('D =', D, 'C =', C, 'sum (L_i - C)_+ over i != 0 =', excess, '; leaf test C*b + excess < D holds for b <=', (D - excess - 1) // C)
print('capacity row weight', w3.get(len(RC)), 'rows used', sorted(w3)[:10], '...')
json.dump({'weights_times6': w3, 'D': D, 'excess': excess}, open('w1_leaf_certificate.json', 'w'))
