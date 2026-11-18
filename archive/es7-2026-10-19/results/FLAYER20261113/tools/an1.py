"""Quick structure stats over pools: sizes of X, E\X, A\X, Z; (4,5)-gons inside E=B5; etc."""
import sys, json, itertools
import fl
from fl import *
from esgeo import Analysis, quick
def sub_gon_types(P):
    """max over (s,t) pairs of (cap,cup) with both chains inside P: returns set of (capB, cupB) pairs maximal"""
    A = Analysis(P); n = A.n; out = set()
    for s in range(n):
        for t in range(s+1, n):
            out.add((int(A.capB[s,t]), int(A.cupB[s,t])))
    return out, A
def has_gon(P, i, j):
    if len(P) < i + j - 2: return False
    ty, A = sub_gon_types(P)
    return any(a >= i and b >= j for a, b in ty)
if __name__ == '__main__':
    tot = 0; bad45 = 0; mx = {}
    for fn in sys.argv[1:]:
        for rec in load_jsonl(fn):
            P = [tuple(p) for p in rec['P']]
            S = Set66(P)
            if not S.ok: print('INVALID', fn); continue
            tot += 1
            E = [S.P[v] for v in range(S.n) if S.in_f[v][0] == 4]
            Aset = [S.P[v] for v in range(S.n) if S.in_f[v][3] >= 1]
            X = [S.P[v] for v in range(S.n) if S.in_f[v][0] == 4 and S.in_f[v][3] >= 1]
            Z = S.n - len(E) - len(Aset) + len(X)
            g45 = has_gon(E, 4, 5); g54 = has_gon(Aset, 5, 4)
            bad45 += g45 or g54
            key = (S.n, len(E), len(Aset), len(X), Z, int(g45), int(g54))
            print(fn.split('/')[-1][:14], 'n=%d E=%d A=%d X=%d Z=%d  E has(4,5)=%d A has(5,4)=%d' % key, 'Egon', quick(E) if len(E)>2 else None)
    print('total', tot, 'sets with (4,5) in E or (5,4) in A:', bad45)
