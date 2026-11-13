"""Real point sets of the (A,B) class and their exact coupled assignments (soundness control)."""
import random, itertools
from fractions import Fraction
import etv_common as ec
from etv_common import A, B

def det(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def labels(P):
    """P sorted by x. Returns Em[u][v], Ep[u][v] (longest cap/cup ending with (u,v)), u<v."""
    n = len(P); Em = [[0] * n for _ in range(n)]; Ep = [[0] * n for _ in range(n)]
    for v in range(n):
        for u in range(v):
            em = ep = 2
            for t in range(u):
                s = det(P[t], P[u], P[v])
                if s < 0: em = max(em, Em[t][u] + 1)
                elif s > 0: ep = max(ep, Ep[t][u] + 1)
            Em[u][v] = em; Ep[u][v] = ep
    return Em, Ep

def max_convex(P):
    n = len(P); best = min(n, 2) if n else 0
    for p in range(n):
        # longest cup / cap starting at p ending with (u,v)
        cu = {}; ca = {}
        for v in range(p + 1, n):
            cu[(p, v)] = 2; ca[(p, v)] = 2
        for v in range(p + 1, n):
            for u in range(p + 1, v):
                bu = ba = -1
                for t in range(p, u):
                    if (t, u) not in cu: continue
                    s = det(P[t], P[u], P[v])
                    if s > 0 and cu[(t, u)] > 0: bu = max(bu, cu[(t, u)] + 1)
                    if s < 0 and ca[(t, u)] > 0: ba = max(ba, ca[(t, u)] + 1)
                cu[(u, v)] = bu; ca[(u, v)] = ba
        for q in range(p + 1, n):
            c1 = max([cu[(u, q)] for u in range(p, q) if (u, q) in cu] + [0])
            c2 = max([ca[(u, q)] for u in range(p, q) if (u, q) in ca] + [0])
            best = max(best, c1 + c2 - 2)
    return best

def general(P, x):
    if any(abs(x[0] - p[0]) == 0 for p in P): return False
    for p, q in itertools.combinations(P, 2):
        if det(p, q, x) == 0: return False
    return True

def ok_class(P):
    P = sorted(P)
    Em, Ep = labels(P)
    n = len(P)
    if any(Em[u][v] > A + 1 for v in range(n) for u in range(v)): return False
    if any(Ep[u][v] > B + 1 for v in range(n) for u in range(v)): return False
    return max_convex(P) <= 7

def greedy_set(rng, tries=400, R=10**6, target=40):
    P = []
    for _ in range(tries):
        x = (rng.randrange(-R, R), rng.randrange(-R, R))
        if not general(P, x): continue
        Q = P + [x]
        if ok_class(Q): P = Q
        if len(P) >= target: break
    return sorted(P)

def states(P):
    P = sorted(P); n = len(P); Em, Ep = labels(P)
    out = []
    for v in range(n):
        cells = set()
        for u in range(v):
            a, b = Em[u][v] - 1, Ep[u][v] - 1
            for x in range(1, a + 1):
                for y in range(1, b + 1): cells.add((x, y))
        f = tuple(max([y for (x, y) in cells if x == c] + [0]) for c in range(1, A + 1))
        out.append(ec.SINDEX[f])
    return out, Em, Ep

def convex4(ps):
    a, b, c, d = ps
    x, y, z, w = det(a, b, c) > 0, det(a, b, d) > 0, det(a, c, d) > 0, det(b, c, d) > 0
    # convex iff no point inside the triangle of the others
    def inside(p, q, r, s):
        d1, d2, d3 = det(q, r, p), det(r, s, p), det(s, q, p)
        return (d1 > 0) == (d2 > 0) == (d3 > 0)
    return not (inside(a, b, c, d) or inside(b, a, c, d) or inside(c, a, b, d) or inside(d, a, b, c))

def assignment(cnf, P, owners):
    """Truth values of the CNF atoms for owners (point indices into sorted P), in support index order."""
    P = sorted(P); Em, Ep = labels(P); val = {}
    for key, var in cnf.ids.items():
        kind = key[0]
        if kind == 'before':
            i, j = key[1:]; val[var] = owners[i] < owners[j]
        elif kind in ('cap_ge', 'cup_ge'):
            i, j, k = key[1:]; u, v = sorted((owners[i], owners[j]))
            lab = (Em[u][v] - 1) if kind == 'cap_ge' else (Ep[u][v] - 1)
            val[var] = lab >= k
        elif kind == 'orientation':
            i, j, k = key[1:]; val[var] = det(P[owners[i]], P[owners[j]], P[owners[k]]) > 0
        elif kind == 'convex_four':
            val[var] = convex4([P[owners[t]] for t in key[1:]])
    return val

def check_clauses(cnf, val):
    bad = []
    for c, t in zip(cnf.clauses, cnf.tags):
        if not any((val[abs(l)] if l > 0 else not val[abs(l)]) for l in c):
            bad.append((c, t))
    return bad
