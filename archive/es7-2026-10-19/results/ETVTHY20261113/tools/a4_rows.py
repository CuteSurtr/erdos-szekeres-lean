"""a=4: test Delta candidates from Baek's (alpha,beta)-plane: D1 = {beta + [alpha>=2] = n-1}, D2 = {beta=n-1} u {beta=n-2, alpha>=2}."""
import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick
from collections import Counter
def alpha_beta(A):
    n = A.n; s = A.capS - 1
    al = [1]*n; be = [1]*n
    for j in range(n):
        for i in range(j):
            c = int(A.cupE[i, j]); be[j] = max(be[j], c)
            if s[i, j] == 1: al[j] = max(al[j], c)
    return al, be
st = Counter()
for fn, ngon in [('pool_a4.jsonl', 8), ('pool_a4n7.jsonl', 7)]:
    for l in open(fn):
        P = sorted(tuple(p) for p in json.loads(l)['P']); A = Analysis(P); n = A.n
        al, be = alpha_beta(A)
        for name, D in [('D1', [i for i in range(n) if be[i] + (al[i] >= 2) == ngon - 1]),
                        ('D2', [i for i in range(n) if be[i] == ngon - 1 or (be[i] == ngon - 2 and al[i] >= 2)])]:
            Dp = [P[i] for i in D]; rest = [P[i] for i in range(n) if i not in set(D)]
            cup = len(Dp) < 3 or quick(Dp)[1] <= 2
            hits = len(rest) < ngon - 1 or quick(rest)[0] <= ngon - 2
            st[(ngon, name, 'cup', cup, 'hits', hits)] += 1
for k in sorted(st): print(k, st[k])
