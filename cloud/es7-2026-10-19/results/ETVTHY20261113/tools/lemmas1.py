"""Test candidate decomposition lemmas on a pool of 5-cap-free octagon-free sets."""
import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick

def gon_types(A, idx):
    """Set of (a,b) such that an a-cap and b-cup within idx share endpoints (a,b maximal per pair)."""
    if len(idx) < 3: return set(), (len(idx), 1, len(idx))
    B = Analysis([A.P[i] for i in idx]); n = B.n
    ts = set()
    for s in range(n):
        for t in range(s+1, n):
            ts.add((int(B.capB[s, t]), int(B.cupB[s, t])))
    mc = max(int(B.capB.max()), 1); mu = max(int(B.cupB.max()), 1)
    g = max(a+b-2 for a, b in ts)
    return ts, (g, mc, mu)

def has(ts, a, b):
    return any(x >= a and y >= b for x, y in ts)

def test(P):
    A = Analysis(P); n = A.n
    cp, cm, beta = A.cap_start, A.cap_end, A.cup_end
    Z = [i for i in range(n) if cp[i] <= 3 and cm[i] <= 3]
    B4 = [i for i in range(n) if cp[i] == 4 and cm[i] <= 3]
    B4r = [i for i in range(n) if cm[i] == 4 and cp[i] <= 3]
    M = [i for i in range(n) if cp[i] == 4 and cm[i] == 4]
    L4 = B4 + M; R4 = B4r + M
    tsM, qM = gon_types(A, M)
    tsB, qB = gon_types(A, B4)
    tsBr, qBr = gon_types(A, B4r)
    tsL, qL = gon_types(A, sorted(L4))
    tsR, qR = gon_types(A, sorted(R4))
    # left endpoints of 7-cups vs right endpoints
    Lset = [s for s in range(n) if any(A.cupB[s, t] >= 7 for t in range(s+1, n))]
    Rset = [t for t in range(n) if beta[t] >= 7]
    interleave = bool(Lset and Rset and max(Lset) > min(Rset))
    return dict(n=n, Z=len(Z), B4=len(B4), B4r=len(B4r), M=len(M), L4=len(L4), R4=len(R4),
                M_q=qM, M_45=has(tsM, 4, 5), M_36=has(tsM, 3, 6), B4_36=has(tsB, 3, 6), B4r_36=has(tsBr, 3, 6),
                L4_q=qL, R4_q=qR, L4_36=has(tsL, 3, 6), L4_45=has(tsL, 4, 5), R4_45=has(tsR, 4, 5),
                LRinter=interleave, nL7=len(Lset), nR7=len(Rset))

if __name__ == '__main__':
    rows = []
    for fn in sys.argv[1:]:
        sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
        for P in sets:
            r = test([tuple(p) for p in P]); rows.append(r)
            print(json.dumps(r), flush=True)
    print('SUMMARY sets', len(rows))
    for key in ['M_45', 'M_36', 'B4_36', 'B4r_36', 'L4_36', 'L4_45', 'R4_45', 'LRinter']:
        print(key, sum(1 for r in rows if r[key]))
    for key in ['Z', 'B4', 'B4r', 'M', 'L4', 'R4']:
        print(key, 'max', max(r[key] for r in rows))
    print('max M-Z', max(r['M']-r['Z'] for r in rows), 'max L4', max(r['L4'] for r in rows))
