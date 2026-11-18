"""Functions of upper_real.py (upper chains of saturated pairs, 4-caps) as a library."""
def upper_chains(P, O, capB, cupB, n):
    m = len(P); out = []
    for (u, v), c in capB.items():
        if c + cupB[u, v] != n + 1: continue
        if c == 2: out.append((u, v))
        elif c == 3:
            for k in range(u + 1, v):
                if O[u, k, v] < 0: out.append((u, k, v))
        elif c == 4:
            for k1 in range(u + 1, v):
                if O[u, k1, v] > 0: continue
                for k2 in range(k1 + 1, v):
                    if O[u, k1, k2] < 0 and O[k1, k2, v] < 0: out.append((u, k1, k2, v))
        else: raise ValueError('cap of size %d' % c)
    return out
def caps4(P, O):
    m = len(P); out = []
    for b in range(m):
        for c in range(b + 1, m):
            L = [a for a in range(b) if O[a, b, c] < 0]
            if not L: continue
            R = [d for d in range(c + 1, m) if O[b, c, d] < 0]
            out += [(a, b, c, d) for a in L for d in R]
    return out
