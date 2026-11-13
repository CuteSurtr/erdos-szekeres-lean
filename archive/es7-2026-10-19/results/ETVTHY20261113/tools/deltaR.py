"""Test: Delta_R = {v : capend(v) + cupend(v) >= k+2} (right endpoints of convex k-gons... ) 4-cap-free?"""
import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick
from collections import Counter
def check(P, k=7):
    A = Analysis(P); n = A.n
    D = [i for i in range(n) if A.cap_end[i] + A.cup_end[i] >= k + 2]
    DL = [i for i in range(n) if A.cap_start[i] + A.cup_start[i] >= k + 2]
    q = quick([A.P[i] for i in D]) if len(D) >= 3 else (len(D), 1, len(D))
    qL = quick([A.P[i] for i in DL]) if len(DL) >= 3 else (len(DL), 1, len(DL))
    rest = [A.P[i] for i in range(n) if i not in set(D)]
    qr = quick(rest) if len(rest) >= 3 else (len(rest), 1, len(rest))
    return n, len(D), q, qr, len(DL), qL
st = Counter(); worst = []
for fn in sys.argv[2:]:
    sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    for P in sets:
        r = check([tuple(p) for p in P], int(sys.argv[1]))
        st[(r[2][1], r[5][1])] += 1
        worst.append(r)
print('(maxcap in Delta_R, maxcap in Delta_L) counts:', dict(st))
print('max |Delta_R|', max(w[1] for w in worst), 'max gon of rest', max(w[3][0] for w in worst))
for w in sorted(worst, key=lambda w: -w[1])[:5]: print(w)
