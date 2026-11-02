#!/usr/bin/env python3
"""SAT relaxation for ONE orbit of tiny clusters (Lemma 1, no centre), general K: all composition constraints.

Frame (as in primefold/theory Thm E): points p_0..p_{n-1} of the cluster sorted by the inward radial coordinate
(possible because F(1,1) = 1 is forced when m*2 > K-1, i.e. no segment within pi/m of the tangent).  For i < j,
t_ij in (1, m-1) is the direction of p_i -> p_j measured ccw from the ccw tangent in units pi/m; b_ij = floor(t_ij)
in {1..m-2} (order encoded: L[i,j,v] <=> b_ij <= v <=> t_ij < v+1).  T[i,j,k] (i<j<k) <=> left turn at p_j
<=> t_ij < t_jk.  Facts (a) turn/bins, (b) t_ik strictly between t_ij and t_jk (mediant property).
A ccw chain with directions in (-a, b) (units pi/m from the ccw tangent) is an outward part followed by an inward
part meeting at their common most-outward point p; read in sorted order it is a CAP starting at p with all t > m-a
plus a CUP starting at p with all t < b (cup = increasing t).  Hence
    F(a,b) = max_p [ capS_p(m-a) + cupS_p(b) - 1 ].
Constraint (Lemma 1): for every cyclic composition (g_1..g_r) of m, r >= 2: sum_i F(g_i, g_{i+1}) <= K-1.
Only forcing implications are encoded (true values satisfy every clause), so UNSAT => no such cluster with n points.
usage: clsat_full.py m K n out.cnf [fixfile]    (fixfile: optional real cluster "x y" lines (local frame x outward
radial, y ccw tangent) whose bins/turns are added as unit clauses -- soundness test)
"""
import sys, math
from itertools import combinations, product
m, K, n, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
fix = sys.argv[5] if len(sys.argv) > 5 else None
B = m - 2
nv = 0
def new():
    global nv; nv += 1; return nv
L = {(i, j, v): new() for i, j in combinations(range(n), 2) for v in range(1, B)}
T = {t: new() for t in combinations(range(n), 3)}
cl = []
def le(i, j, v):          # b_ij <= v
    if v <= 0: return None   # false
    if v >= B: return True
    return L[i, j, v]
def notle(i, j, v):
    x = le(i, j, v)
    if x is None: return True
    if x is True: return None
    return -x
def clause(lits):
    o = []
    for l in lits:
        if l is True: return
        if l is None: continue
        o.append(l)
    cl.append(o)
for i, j in combinations(range(n), 2):
    for v in range(1, B - 1):
        cl.append([-L[i, j, v], L[i, j, v + 1]])
for i, j, k in combinations(range(n), 3):
    t = T[i, j, k]
    for v in range(1, B):
        clause([notle(i, j, v), le(j, k, v), t])      # b_ij <= v < b_jk  -> left
        clause([notle(j, k, v), le(i, j, v), -t])     # b_jk <= v < b_ij  -> right
    for v in range(1, B + 1):
        clause([le(i, j, v - 1), le(j, k, v - 1), notle(i, k, v - 1)])   # b_ik >= min(b_ij, b_jk)
        clause([notle(i, j, v), notle(j, k, v), le(i, k, v)])            # b_ik <= max(b_ij, b_jk)
    # finer: if left turn, t_ij < t_ik < t_jk ; if right turn, t_jk < t_ik < t_ij
    for v in range(1, B + 1):
        clause([-t, le(i, j, v - 1), notle(i, k, v - 1)])   # left & b_ij >= v -> b_ik >= v
        clause([-t, notle(j, k, v), le(i, k, v)])           # left & b_jk <= v -> b_ik <= v
        clause([t, le(j, k, v - 1), notle(i, k, v - 1)])    # right & b_jk >= v -> b_ik >= v
        clause([t, notle(i, j, v), le(i, k, v)])            # right & b_ij <= v -> b_ik <= v
# chains starting at p: CU[p,i,j,l] (cup p..i,j with >= l points), CA likewise (caps)
LM = K
CU, CA = {}, {}
for p in range(n):
    for i, j in combinations(range(p, n), 2):
        for l in range(3, LM + 1):
            if i == p: continue
            CU[p, i, j, l] = new(); CA[p, i, j, l] = new()
for p in range(n):
    for j, k in combinations(range(p + 1, n), 2):
        clause([-T[p, j, k], CU[p, j, k, 3]])
        clause([T[p, j, k], CA[p, j, k, 3]])
    for i, j, k in combinations(range(p + 1, n), 3):
        for l in range(4, LM + 1):
            clause([-CU[p, i, j, l - 1], -T[i, j, k], CU[p, j, k, l]])
            clause([-CA[p, i, j, l - 1], T[i, j, k], CA[p, j, k, l]])
# cupS[p,x,l]: cup from p with >= l points and last t < x ; capS[p,y,l]: cap from p, last t > y
CUS = {(p, x, l): new() for p in range(n) for x in range(1, m) for l in range(2, LM + 1)}
CAS = {(p, y, l): new() for p in range(n) for y in range(1, m) for l in range(2, LM + 1)}
for p in range(n):
    for x in range(1, m):
        for j in range(p + 1, n):
            clause([notle(p, j, x - 1), CUS[p, x, 2]])        # t_pj < x
            clause([le(p, j, x - 1), CAS[p, x, 2]])           # t_pj > x
        for i, j in combinations(range(p + 1, n), 2):
            for l in range(3, LM + 1):
                clause([-CU[p, i, j, l], notle(i, j, x - 1), CUS[p, x, l]])
                clause([-CA[p, i, j, l], le(i, j, x - 1), CAS[p, x, l]])
        for l in range(3, LM + 1):
            cl.append([-CUS[p, x, l], CUS[p, x, l - 1]]); cl.append([-CAS[p, x, l], CAS[p, x, l - 1]])
def cus(p, x, l):
    if l <= 1: return True
    if x >= m: x = m - 1      # all t < m-1 anyway
    if x <= 1: return None    # no t < 1
    return CUS[p, x, l]
def cas(p, y, l):
    if l <= 1: return True
    if y <= 1: y = 1          # all t > 1
    if y >= m - 1: return None
    return CAS[p, y, l]
# Fge[a,b,v]: F(a,b) >= v
FG = {(a, b, v): new() for a in range(1, m) for b in range(1, m) for v in range(2, K + 1)}
for a in range(1, m):
    for b in range(1, m):
        for v in range(3, K + 1):
            cl.append([-FG[a, b, v], FG[a, b, v - 1]])
        for p in range(n):
            for l1 in range(1, LM + 1):
                for l2 in range(1, LM + 1):
                    v = l1 + l2 - 1
                    if v < 2: continue
                    v = min(v, K)
                    x1, x2 = cas(p, m - a, l1), cus(p, b, l2)
                    if x1 is None or x2 is None: continue
                    lits = []
                    if x1 is not True: lits.append(-x1)
                    if x2 is not True: lits.append(-x2)
                    cl.append(lits + [FG[a, b, v]])
def fg(a, b, v):
    if v <= 1: return True
    return FG[a, b, v]
# compositions
def comps(total):
    if total == 0: yield (); return
    for f in range(1, total + 1):
        for rest in comps(total - f): yield (f,) + rest
ncomp = 0
for g in comps(m):
    r = len(g)
    if r < 2: continue
    pairs = [(g[i], g[(i + 1) % r]) for i in range(r)]
    for vs in product(range(1, K + 1), repeat=r):
        if sum(vs) != K: continue
        lits = []
        for (a, b), v in zip(pairs, vs):
            x = fg(a, b, v)
            if x is True: continue
            lits.append(-x)
        cl.append(lits); ncomp += 1
if fix:
    P = [tuple(map(float, l.split())) for l in open(fix) if l.strip() and not l.startswith('#')]
    assert len(P) == n
    P.sort(key=lambda q: -q[0])          # inward order: decreasing outward coordinate x
    def tval(i, j):
        dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
        ang = math.degrees(math.atan2(dy, dx))
        return ((ang - 90.0) % 360.0) / (180.0 / m)
    for i, j in combinations(range(n), 2):
        t = tval(i, j); assert 1 < t < m - 1, t
        b = int(math.floor(t))
        for v in range(1, B):
            cl.append([L[i, j, v]] if b <= v else [-L[i, j, v]])
    for i, j, k in combinations(range(n), 3):
        cl.append([T[i, j, k]] if tval(i, j) < tval(j, k) else [-T[i, j, k]])
with open(out, 'w') as f:
    f.write('p cnf %d %d\n' % (nv, len(cl)))
    for c in cl:
        f.write(' '.join(map(str, c)) + ' 0\n')
print('m=%d K=%d n=%d vars=%d clauses=%d composition-clauses=%d fix=%s' % (m, K, n, nv, len(cl), ncomp, fix))
