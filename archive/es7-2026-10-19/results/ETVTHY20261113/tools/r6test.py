import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick
def r6info(P):
    A = Analysis(P); n = A.n; beta = A.cup_end
    R6 = [i for i in range(n) if beta[i] >= 6]
    R7 = [i for i in range(n) if beta[i] == 7]
    q = quick([A.P[i] for i in R6]) if len(R6) >= 3 else None
    return n, len(R6), len(R7), q
for fn in sys.argv[1:]:
    sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    for P in sets:
        print(r6info([tuple(p) for p in P]))
