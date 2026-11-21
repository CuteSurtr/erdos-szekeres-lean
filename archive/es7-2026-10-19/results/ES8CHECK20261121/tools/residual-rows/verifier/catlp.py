import gzip, json, sys
from math import comb
src = sys.argv[1]
d = json.load(gzip.open(src))
S = [tuple(s) for s in d['states']]
assert len(S) == 154 and len(set(S)) == 154 and S[0] == (0,0,0,0,0)
assert all(s[4] == 0 and s[0] >= s[1] >= s[2] >= s[3] >= 0 and s[0] <= 6 and (s[0] < 6 or s[1] == 6) for s in S)
fam = {
 'f4=0': [i for i,s in enumerate(S) if s[3] == 0],
 'f3=0': [i for i,s in enumerate(S) if s[2] == 0],
 'F (f1>=5)': [i for i,s in enumerate(S) if s[0] >= 5],
 'Lo (f1<=4)': [i for i,s in enumerate(S) if s[0] <= 4],
 'Lo & f4=0': [i for i,s in enumerate(S) if s[0] <= 4 and s[3] == 0],
 'f2=0': [i for i,s in enumerate(S) if s[1] == 0],
}
for k,v in fam.items(): print(k, len(v))
print('C(7,3)=', comb(7,3), ' ES cup-cap no 6-cup/no 5-cap C(6+5-4,6-2)=', comb(7,4))
caps = {'f4=0': 65, 'f3=0': 22, 'Lo & f4=0': 35}
dem = {k: len(fam[k]) - c for k,c in caps.items()}
print('demands', dem)
# LP: min sum h, 2650 rows, h0 = 0, 0<=h<=1; then add candidate rows with demand max(0,d)
import numpy as np, highspy
def lp(extra):
    rows = [(r['support'], r['rhs']) for r in d['constraints']] + extra
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
    n = 154
    lb = np.zeros(n); ub = np.ones(n); ub[0] = 0.0
    h.addVars(n, lb, ub)
    h.changeColsCost(n, np.arange(n, dtype=np.int32), np.ones(n))
    for sup, rhs in rows:
        idx = np.array(sup, dtype=np.int32)
        h.addRow(float(rhs), highspy.kHighsInf, len(idx), idx, np.ones(len(idx)))
    h.run()
    return h.getInfo().objective_function_value, h.modelStatusToString(h.getModelStatus())
base = lp([])
cand = lp([(fam[k], max(0, dem[k])) for k in caps])
print('LP base', base, 'LP with candidate rows', cand)
# context only: LP value if the {f4=0} owners had capacity c (h(f4=0) >= 63-c)
for c in (42, 45, 48, 50, 52, 55, 58, 60, 63):
    print('  hypothetical cap', c, 'LP', lp([(fam['f4=0'], 63 - c)])[0])
