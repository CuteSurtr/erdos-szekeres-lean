import gzip, json, highspy, numpy as np, time
d=json.load(gzip.open('experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'))
C=d['constraints']
h=highspy.Highs(); h.setOptionValue('output_flag', False)
n=154
for i in range(n): h.addVar(0,1)
h.changeColsCost(n, np.arange(n,dtype=np.int32), np.ones(n))
h.changeColBounds(0, 0., 0.)
for c in C:
    idx=np.array(sorted(c['support']),dtype=np.int32)
    h.addRow(c['rhs'], highspy.kHighsInf, len(idx), idx, np.ones(len(idx)))
t=time.time(); h.run(); print('LP optimum', h.getInfo().objective_function_value, time.time()-t)
