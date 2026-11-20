# HEURISTIC (HiGHS guide only): second Z-type row. Z* = {f(0)=5, f(4)>=1}: a 6-cup and a 6-cap of H end at the owner;
# by THEORY310N Lemma B the owners have no 6-cap and no 6-cup, so they are an N66-class set: h(Z*) >= 70 - 55 = 15.
import json, numpy as np, highspy
d = json.load(open('/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))
S = d['states']; N = len(S); R = [(r['support'], r['rhs']) for r in d['constraints']]
Z = [i for i, f in enumerate(S) if f[0] <= 4 and f[4] == 0]
Zs = [i for i, f in enumerate(S) if f[0] == 5 and f[4] >= 1]
tr = lambda f: tuple(sum(1 for x in f if x > j) for j in range(5))
T = {tuple(f): i for i, f in enumerate(S)}
print('|Z| %d |Z*| %d disjoint %s; Z* transpose-closed %s; Z transpose-closed %s' % (len(Z), len(Zs), not (set(Z) & set(Zs)),
      set(T[tr(S[i])] for i in Zs) == set(Zs), set(T[tr(S[i])] for i in Z) == set(Z)))
def lp(rows, obj=None):
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1); inf = highspy.kHighsInf
    c = np.ones(N) if obj is None else obj
    for j in range(N): h.addVar(0.0, 1.0); h.changeColCost(j, float(c[j]))
    for sup, rhs in rows:
        idx = np.array(sup, dtype=np.int32); h.addRow(float(rhs), inf, len(idx), idx, np.ones(len(idx)))
    h.run(); return h.getInfo().objective_function_value, np.array(h.getSolution().col_value)
v1, x1 = lp(R + [(Z, 15)])
print('catalog + Z: root LP %.4f; h(Z*) at x* = %.3f' % (v1, x1[Zs].sum()))
o = np.zeros(N); o[Zs] = 1; print('LP min h(Z*) on catalog + Z: %.3f' % lp(R + [(Z, 15)], o)[0])
for r2 in (15, 16, 17, 18, 20):
    v2, x2 = lp(R + [(Z, 15), (Zs, r2)])
    print('catalog + Z(15) + Z*(%d): root LP %.4f (gain %+.3f)' % (r2, v2, v2 - v1), flush=True)
v3, _ = lp(R + [(Z, 16), (Zs, 16)]); print('both rows at 16 (N66 <= 54): %.4f' % v3)
