"""Decomposition statistics and lemma tests on 5-cap-free octagon-free sets."""
import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick

def sub_quick(A, idx):
    return quick([A.P[i] for i in idx]) if len(idx) >= 3 else (len(idx), 1, len(idx))

def has_gon_type(A, idx, a, b):
    """Is there an a-cap and b-cup within idx sharing endpoints (weak (a,b)-gon)?"""
    if len(idx) < 2: return False
    B = Analysis([A.P[i] for i in idx])
    n = B.n
    return any(B.capB[s, t] >= a and B.cupB[s, t] >= b for s in range(n) for t in range(s+1, n))

def stats(P):
    A = Analysis(P); n = A.n
    beta = A.cup_end; cplus = A.cap_start; cminus = A.cap_end
    out = {'n': n}
    levels = {k: [i for i in range(n) if beta[i] == k] for k in range(1, 8)}
    out['B'] = {k: len(v) for k, v in levels.items()}
    out['B_gon3k'] = {k: has_gon_type(A, v, 3, k) for k, v in levels.items() if k >= 2}
    out['B_maxcap'] = {k: sub_quick(A, v)[1] for k, v in levels.items() if v}
    Q = [i for i in range(n) if cplus[i] <= 3]
    L4 = [i for i in range(n) if cplus[i] == 4]
    R4 = [i for i in range(n) if cminus[i] == 4]
    M = [i for i in L4 if cminus[i] == 4]
    Bset = [i for i in L4 if cminus[i] <= 3]
    out.update({'Q': len(Q), 'L4': len(L4), 'R4': len(R4), 'M': len(M), 'B4': len(Bset),
                'Qr': len([i for i in range(n) if cminus[i] <= 3])})
    out['M_q'] = sub_quick(A, M); out['L4_q'] = sub_quick(A, L4); out['B4_q'] = sub_quick(A, Bset)
    out['L4_gon36'] = has_gon_type(A, L4, 3, 6)
    out['B4_gon36'] = has_gon_type(A, Bset, 3, 6)
    T = [i for i in range(n) if beta[i] <= 6]
    out['T'] = len(T)
    R6 = [i for i in range(n) if beta[i] >= 6]
    out['R6'] = len(R6)
    return out

if __name__ == '__main__':
    for fn in sys.argv[1:]:
        if fn.endswith('.json'):
            sets = [json.load(open(fn))]
        else:
            sets = [json.loads(l)['P'] for l in open(fn)]
        for P in sets:
            P = [tuple(p) for p in P]
            print(json.dumps(stats(P)))
