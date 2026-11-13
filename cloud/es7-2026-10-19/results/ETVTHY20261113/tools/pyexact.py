"""Pure-Python exact analysis (arbitrary-size integer coordinates)."""
def orient(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])

def otable(P):
    n = len(P)
    O = {}
    for a in range(n):
        for b in range(a+1, n):
            for c in range(b+1, n):
                v = orient(P[a], P[b], P[c])
                if v == 0: raise ValueError('collinear')
                O[a, b, c] = 1 if v > 0 else -1
    return O

def chains(P, O=None):
    """capE, cupE (ending with edge), capB, cupB (between endpoints)."""
    n = len(P); O = O or otable(P)
    capE = {}; cupE = {}
    for j in range(n):
        for i in range(j):
            bc = bu = 2
            for h in range(i):
                if O[h, i, j] < 0: bc = max(bc, capE[h, i]+1)
                else: bu = max(bu, cupE[h, i]+1)
            capE[i, j] = bc; cupE[i, j] = bu
    capB = {}; cupB = {}
    for s in range(n):
        Dc = {}; Du = {}
        for j in range(s+1, n): Dc[s, j] = 2; Du[s, j] = 2
        for j in range(s+1, n):
            for i in range(s+1, j):
                bc = bu = 0
                for h in range(s, i):
                    if (h, i) not in Dc: continue
                    if O[h, i, j] < 0:
                        if Dc[h, i]: bc = max(bc, Dc[h, i]+1)
                    else:
                        if Du[h, i]: bu = max(bu, Du[h, i]+1)
                Dc[i, j] = bc; Du[i, j] = bu
        for t in range(s+1, n):
            capB[s, t] = max(Dc.get((i, t), 0) for i in range(s, t))
            cupB[s, t] = max(Du.get((i, t), 0) for i in range(s, t))
    return capE, cupE, capB, cupB

def summary(P):
    P = sorted(P); n = len(P)
    assert len({p[0] for p in P}) == n
    capE, cupE, capB, cupB = chains(P)
    mc = max(capB.values()); mu = max(cupB.values())
    g = max(capB[k]+cupB[k]-2 for k in capB)
    return g, mc, mu
