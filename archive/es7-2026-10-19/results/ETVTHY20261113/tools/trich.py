"""Heptagon trichotomy statistics and the Delta_A candidate:
Delta_A = {right ends in Q} U {left ends in Q' of saturated pairs whose right end is in L4}."""
import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick
from collections import Counter
st = Counter()
for fn in sys.argv[1:]:
    sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    for P in sets:
        P = sorted(tuple(p) for p in P); A = Analysis(P); n = A.n
        cp, cm = A.cap_start, A.cap_end
        sat = [(u, v) for u in range(n) for v in range(u+1, n) if A.capB[u, v] + A.cupB[u, v] >= 9]
        t3 = [(u, v) for u, v in sat if cp[v] == 4 and cm[u] == 4]
        DA = {v for u, v in sat if cp[v] <= 3} | {u for u, v in sat if cp[v] == 4 and cm[u] <= 3}
        capfree = len(DA) < 4 or quick([P[i] for i in DA])[1] <= 3
        rest = [P[i] for i in range(n) if i not in DA]
        hits = len(rest) < 7 or quick(rest)[0] <= 6
        st[('typeiii_pairs>0', len(t3) > 0, 'DA capfree', capfree, 'DA hits', hits)] += 1
for k, v in sorted(st.items()): print(k, v)
