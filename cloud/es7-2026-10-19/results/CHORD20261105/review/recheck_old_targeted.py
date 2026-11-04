#!/usr/bin/env python3
"""Re-evaluate the 33 'violations' of the first targeted run (old Cartesian evaluator with a flawed trust threshold)
with (a) the corrected evaluator and (b) a 400-digit Cartesian reference with a correct error bound."""
import json, mpmath as mp, stress
from indep_enc import TRIPLE_OF, YINV, NTRIP
rows = [json.loads(l) for l in open('stress_targeted_OLDEVAL_precision_artifacts.log')][:-1]
real = 0
for d in rows:
    cl = d['clause']; rs = [mp.mpf(x) for x in d['r']]; th = [mp.mpf(x) for x in d['theta']]
    v, u = stress.evaluate(rs, th, [cl])
    with mp.workdps(400):
        rs4 = [mp.mpf(x) for x in d['r']]; th4 = [mp.mpf(x) for x in d['theta']]
        lits = []
        for l in cl:
            if abs(l) <= NTRIP:
                P = []
                for x in TRIPLE_OF[abs(l)]:
                    i, k = divmod(x, 6); a = mp.radians(th4[i] + 60 * k); P.append((rs4[i] * mp.cos(a), rs4[i] * mp.sin(a)))
                a, b, c = P; o = (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
                bound = mp.mpf(10) ** -380 * max(rs4) ** 2
                val = None if abs(o) < bound else (o > 0)
            else:
                i, j = YINV[abs(l)]; val = th4[i] < th4[j]
            lits.append(None if val is None else (val if l > 0 else not val))
        ref_viol = all(x is False for x in lits)
    real += ref_viol
    print(cl, 'new-evaluator violated:', bool(v), 'undetermined:', u, '| 400-digit reference violated:', ref_viol, lits)
print('genuine violations:', real, 'of', len(rows))
