import json, sys
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick
from collections import Counter
st = Counter()
for l in open('pool_a4.jsonl'):
    P = sorted(tuple(p) for p in json.loads(l)['P'])
    for mirror in (False, True):
        Q = sorted(((-x, y) for x, y in P)) if mirror else P
        A = Analysis(Q); n = A.n; be = A.cup_end
        D = []
        for r in range(1, 7):
            row = [i for i in range(n) if be[i] == r]
            if row: D.append(min(row))
        Dp = [Q[i] for i in D]; rest = [Q[i] for i in range(n) if i not in set(D)]
        cupok = len(Dp) < 3 or quick(Dp)[1] <= 2
        hept = len(rest) >= 7 and quick(rest)[0] >= 7
        st[(mirror, cupok, not hept)] += 1
print('(mirror, Delta is a cup, rest heptagon-free):', dict(st))
