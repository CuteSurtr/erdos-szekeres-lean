#!/usr/bin/env python3
"""states.py -- incoming states (down-sets of labels) of a real point set; cup/cap ranks."""
import sys, itertools, json
sys.path.insert(0, '.')
import geom

def labels(P, S=None):
    """E[-1][(u,v)], E[+1][(u,v)] = longest cap / cup ending with the pair (u,v)."""
    n = len(P); S = S or geom.orient(P)
    E = {}
    for sgn in (1, -1):
        L = {(j, k): 2 for j in range(n) for k in range(j + 1, n)}
        for k in range(n):
            for j in range(k):
                for i in range(j):
                    if S[(i, j, k)] == sgn and L[(i, j)] + 1 > L[(j, k)]:
                        L[(j, k)] = L[(i, j)] + 1
        E[sgn] = L
    return E

def states(P, A, B, S=None):
    n = len(P); E = labels(P, S)
    out = []
    for v in range(n):
        f = [0] * A
        for u in range(v):
            a = E[-1][(u, v)] - 1; b = E[1][(u, v)] - 1
            for c in range(a):
                f[c] = max(f[c], b)
        out.append(tuple(f))
    return out

if __name__ == '__main__':
    P = geom.load(sys.argv[1]); A = int(sys.argv[2]); B = int(sys.argv[3])
    st = states(P, A, B)
    print(st)
    print('distinct', len(set(st)) == len(st))
    from collections import Counter
    print('f1 histogram (beta-1):', sorted(Counter(s[0] for s in st).items()))
    E = labels(P)
    n = len(P)
    # starts of longest cups
    print('max cup', max(E[1].values()), 'max cap', max(E[-1].values()))
    ends6 = sorted({v for (u, v), l in E[1].items() if l == B + 1})
    print('ends of %d-cups:' % (B + 1), ends6)
