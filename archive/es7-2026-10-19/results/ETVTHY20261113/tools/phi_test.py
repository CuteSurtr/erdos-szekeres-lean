import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick
from alphafeat import baek_alpha
from collections import Counter
st = Counter()
for fn in sys.argv[1:]:
    sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    for P in sets:
        P = sorted(tuple(p) for p in P); A = Analysis(P); al, ao = baek_alpha(A); n = A.n
        phi = [a[2] + (a[0] >= 2) + (a[1] >= 2) for a in al]
        for name, D in [('phi=7', [i for i in range(n) if phi[i] == 7]), ('phi>=7', [i for i in range(n) if phi[i] >= 7])]:
            capok = len(D) < 4 or quick([P[i] for i in D])[1] <= 3
            rest = [P[i] for i in range(n) if i not in set(D)]
            gonok = len(rest) < 7 or quick(rest)[0] <= 6
            st[(name, capok, gonok)] += 1
print(dict(st))
