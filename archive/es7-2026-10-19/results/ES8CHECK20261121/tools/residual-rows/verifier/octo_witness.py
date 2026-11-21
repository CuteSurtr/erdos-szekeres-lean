"""Extract and independently verify the convex octagon among the A_2 owners of the literal-hypothesis example."""
import itertools, json, sys
from geo import Conf, sub

lines = open(sys.argv[1]).read().splitlines()
ex = json.loads(lines[1])
P = [tuple(p) for p in ex['points']]
C = Conf(P)
S = C.states()
own = [v for v in range(C.n) if S[v][3] >= 2]
assert own == ex['A2_owner_idx']
Q = sub(P, own)
D = Conf(Q)
O, n = D.O, D.n
# DP with back-pointers for caps / cups from fixed start i
found = None
for i in range(n):
    cap = {}; cup = {}
    for v in range(i + 1, n):
        cap[(i, v)] = (2, None); cup[(i, v)] = (2, None)
        for u in range(i + 1, v):
            bc = bu = None
            for t in range(i, u):
                if O[t][u][v] < 0 and (t, u) in cap:
                    if bc is None or cap[(t, u)][0] + 1 > bc[0]: bc = (cap[(t, u)][0] + 1, t)
                if O[t][u][v] > 0 and (t, u) in cup:
                    if bu is None or cup[(t, u)][0] + 1 > bu[0]: bu = (cup[(t, u)][0] + 1, t)
            if bc: cap[(u, v)] = bc
            if bu: cup[(u, v)] = bu
    for j in range(i + 1, n):
        mc = max(((cap[(u, j)][0], u) for u in range(i, j) if (u, j) in cap))
        mu = max(((cup[(u, j)][0], u) for u in range(i, j) if (u, j) in cup))
        if mc[0] + mu[0] >= 10 and found is None:
            def back(tab, u, v):
                ch = [v, u]
                while tab[(u, v)][1] is not None:
                    u, v = tab[(u, v)][1], u
                    ch.append(u)
                return ch[::-1]
            capc = back(cap, mc[1], j); cupc = back(cup, mu[1], j)
            found = (capc, cupc)
    if found: break
capc, cupc = found
verts = sorted(set(capc) | set(cupc))
pts = [Q[k] for k in verts]
# independent check: every one of the chosen points is a strict hull vertex (not inside any triangle of others)
def o(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
def inside(p, a, b, c):
    s = (o(a, b, p), o(b, c, p), o(c, a, p))
    return all(x > 0 for x in s) or all(x < 0 for x in s)
octa = pts[:]
take = None
for comb in itertools.combinations(range(len(octa)), 8):
    sel = [octa[k] for k in comb]
    if all(not inside(p, *t) for p in sel for t in itertools.combinations([q for q in sel if q != p], 3)):
        take = sel; break
R_ok = (C.longcap <= 5, C.longcup <= 7, not C.junction(), C.gon())
print('full set n =', C.n, '| no 6-cap, no 8-cup, no junction, largest convex polygon in R:', R_ok)
print('A_2 owners:', len(own), '| longest cap', D.longcap, 'longest cup', D.longcup, 'largest convex polygon', D.gon())
print('cap chain', capc, 'cup chain', cupc)
print('8 points in convex position among A_2 owners (independent point-in-triangle test):', take is not None)
print(json.dumps(take))
print('their states:', [S[own[k]] for k in verts if Q[k] in (take or [])])
