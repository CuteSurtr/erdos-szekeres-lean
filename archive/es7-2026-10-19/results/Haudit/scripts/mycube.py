# Independent re-implementation of the soundness-note definitions (not importing Mii-S code).
from itertools import combinations
N = 33
VAR = {}
n = 0
for i in range(1, N+1):
    for j in range(i+1, N+1):
        for k in range(j+1, N+1):
            n += 1; VAR[(i,j,k)] = n
def orb(i,j,k):
    """orbit representative of X(i,j,k), i<j<k; rule X(34-k,34-j,34-i) = +X(i,j,k)"""
    a = VAR[(i,j,k)]; b = VAR[(34-k,34-j,34-i)]
    return a if a < b else b
def ccw(p,q,r):
    """literal for orient(p,q,r) > 0"""
    t = [p,q,r]; s = 1
    # bubble sort counting swaps
    for x in range(3):
        for y in range(2-x):
            if t[y] > t[y+1]: t[y],t[y+1] = t[y+1],t[y]; s = -s
    return s*orb(*t)
def hull(U, L):
    U = sorted(U); L = sorted(L)
    low = [1] + L + [34-a for a in L[::-1]] + [33]
    up_lr = [1] + U + [34-a for a in U[::-1]] + [33]
    return low + up_lr[::-1][1:-1]
def cube(U, L):
    H = hull(U, L); m = len(H); lits = set()
    for t in range(m):
        p, q = H[t], H[(t+1) % m]
        for r in range(1, N+1):
            if r != p and r != q: lits.add(ccw(p,q,r))
    for a in range(m):
        for b in range(a+1, m):
            for c in range(b+1, m):
                lits.add(ccw(H[a],H[b],H[c]))
    ups = set(U) | {34-a for a in U}; lows = set(L) | {34-a for a in L}
    for v in ups | lows:
        for i in range(1, v):
            for k in range(v+1, N+1):
                lits.add(-orb(i,v,k) if v in ups else orb(i,v,k))
    return lits
def cases():
    P = range(2,17); out = []
    for a in P: out += [((a,),()), ((),(a,))]
    for a,b in combinations(P,2): out += [((a,b),()), ((),(a,b))]
    for a in P:
        for b in P:
            if a != b: out.append(((a,),(b,)))
    return out
def UP(U):
    pts = [1] + sorted(U); nxt = pts[1:] + [34 - pts[-1]]; s = set()
    for v, q in zip(pts, nxt):
        for r in range(1, N+1):
            if r not in (v,q): s.add(-ccw(v,q,r))
    return s
