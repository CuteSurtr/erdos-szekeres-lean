import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, orient
from collections import Counter
cnt = Counter(); tot = 0
for fn in sys.argv[1:]:
    sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    for P in sets:
        P = sorted(tuple(p) for p in P); A = Analysis(P); n = A.n
        cm, cp, be, om = A.cap_end, A.cap_start, A.cup_end, A.cup_start
        DR = [i for i in range(n) if cm[i] + be[i] >= 9]
        S = set(DR)
        for b in DR:
            for c in DR:
                if c <= b: continue
                if orient(P[0], P[0], P[0]) != 0: pass
                L = [a for a in DR if a < b and orient(P[a], P[b], P[c]) < 0]
                R = [d for d in DR if d > c and orient(P[b], P[c], P[d]) < 0]
                for a in L:
                    for d in R:
                        tot += 1
                        cnt[tuple((be[x], cm[x], cp[x]) for x in (a, b, c, d))] += 1
print('4-caps inside Delta_R:', tot)
for k, v in cnt.most_common(25): print(v, k)
