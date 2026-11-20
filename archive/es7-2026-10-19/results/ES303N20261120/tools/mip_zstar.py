# HEURISTIC (HiGHS MIP guide only): do good integer hole vectors (catalog + Z-row, h0 = h1 = 0) already have >= 15 holes
# in Z* = {f(0)=5, f(4)>=1}? Then the Z*-row is a fractional effect only.
import json, numpy as np, highspy
d = json.load(open('/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))
S = d['states']; N = len(S); R = [(r['support'], r['rhs']) for r in d['constraints']]
Z = [i for i, f in enumerate(S) if f[0] <= 4 and f[4] == 0]; Zs = [i for i, f in enumerate(S) if f[0] == 5 and f[4] >= 1]
one = [i for i, f in enumerate(S) if tuple(f) == (1, 0, 0, 0, 0)][0]
def mip(rows, tl, cap_zs=None):
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1); h.setOptionValue('time_limit', tl)
    inf = highspy.kHighsInf
    for j in range(N):
        lo, hi = (0.0, 0.0) if j in (0, one) else (0.0, 1.0); h.addVar(lo, hi); h.changeColCost(j, 1.0)
        h.changeColIntegrality(j, highspy.HighsVarType.kInteger)
    for sup, rhs in rows:
        idx = np.array(sup, dtype=np.int32); h.addRow(float(rhs), inf, len(idx), idx, np.ones(len(idx)))
    if cap_zs is not None:
        idx = np.array(Zs, dtype=np.int32); h.addRow(-inf, float(cap_zs), len(idx), idx, np.ones(len(idx)))
    h.run(); i = h.getInfo(); x = np.array(h.getSolution().col_value)
    return i.objective_function_value, i.mip_dual_bound, round(float(x[Zs].sum())), round(float(x[Z].sum())), str(h.getModelStatus()).split('.')[-1]
base = R + [(Z, 15)]
print('catalog+Z, free: incumbent %s bound %.2f h(Z*)=%s h(Z)=%s %s' % mip(base, 300), flush=True)
for c in (14, 10, 7):
    print('catalog+Z with h(Z*) <= %d: incumbent %s bound %.2f h(Z*)=%s h(Z)=%s %s' % ((c,) + mip(base, 300, c)), flush=True)
