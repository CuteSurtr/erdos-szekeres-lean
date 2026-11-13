import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick
from greedy_delta import greedy
from collections import Counter
def capfree(pts): return len(pts) < 4 or quick(pts)[1] <= 3
def gonfree(pts, k): return len(pts) < k or quick(pts)[0] < k
st = Counter()
k = 7
for fn in sys.argv[1:]:
    sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    for P in sets:
        P = sorted(tuple(p) for p in P); A = Analysis(P); n = A.n
        cm, cp, be, om = A.cap_end, A.cap_start, A.cup_end, A.cup_start
        DR = {i for i in range(n) if cm[i] + be[i] >= k+2}
        DL = {i for i in range(n) if cp[i] + om[i] >= k+2}
        r1 = {i for i in DR if cp[i] <= 3} | {i for i in DL if cm[i] <= 3}
        ok1 = capfree([P[i] for i in r1]) and gonfree([P[i] for i in range(n) if i not in r1], k)
        b, r = greedy(P, k, False); b2, r2 = greedy(P, k, True)
        g1 = capfree(r); g2 = capfree(r2)
        st[('r1', ok1)] += 1; st[('greedy_either', g1 or g2)] += 1
print(dict(st))
