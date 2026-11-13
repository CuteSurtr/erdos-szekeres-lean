#!/usr/bin/env python3
"""Corollary-15 x-blow-up with x = 2 (k = m + 4) of a centrally symmetric base, threshold N/2, paired clusters.
Clusters (pre-images, before the clockwise quarter-turn):
  left p_i (i>=2): P(a,u) with a = k+1-x-s_i (no a-cap), u = x+2 (no u-cup);  size C(k-1-s_i, x)
  left p_1:        P'(k, x+2, k): Valtr/ES construction, size sum_{l<=x} C(k-2,l)
Right clusters are negatives.  All exact; final set checked by two independent DPs.
Usage: cor15_build_x2.py base.txt m out.txt"""
import sys, math, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from maxconvex import max_convex, orient
from maxconvex_cupcap import max_convex_cupcap
from cor15_build import read, left_profile
from math import comb

def longest_cup_cap(P):
    P = sorted(P); n = len(P)
    assert len({p[0] for p in P}) == n
    cup = [[2]*n for _ in range(n)]; cap = [[2]*n for _ in range(n)]
    bu = min(n, 2); bc = min(n, 2)
    for j in range(n):
        for i in range(j):
            for h in range(i):
                o = orient(P[h], P[i], P[j])
                if o > 0: cup[i][j] = max(cup[i][j], cup[h][i] + 1)
                elif o < 0: cap[i][j] = max(cap[i][j], cap[h][i] + 1)
                else: raise ValueError('collinear')
            bu = max(bu, cup[i][j]); bc = max(bc, cap[i][j])
    return bu, bc

def maxslope(P):
    s = Fraction(0)
    for p, q in itertools.combinations(P, 2):
        s = max(s, Fraction(abs(q[1]-p[1]), abs(q[0]-p[0])))
    return s

from fractions import Fraction

def P_au(a, u):
    """no a-cap, no u-cup, C(a+u-4, a-2) points: A = P(a,u-1) left, B = P(a-1,u) right, A-B slopes > internal."""
    if a <= 2 or u <= 2: return [(0, 0)]
    A, B = P_au(a, u-1), P_au(a-1, u)
    s = math.ceil(max(maxslope(A) if len(A) > 1 else 0, maxslope(B) if len(B) > 1 else 0)) + 1
    ax1 = max(p[0] for p in A); bx0 = min(p[0] for p in B)
    dx = ax1 - bx0 + 1
    Bx = [(x + dx, y) for x, y in B]
    span = max(p[0] for p in Bx) - min(p[0] for p in A)
    ay1 = max(p[1] for p in A); by0 = min(p[1] for p in Bx)
    dy = (ay1 - by0) + s * span + 1
    return sorted(A + [(x, y + dy) for x, y in Bx])

def flatten(P, lam_num, lam_den):
    # (x, y) -> (lam_den * x, lam_num * y): positive diagonal map, keeps cups/caps; makes slopes small if lam small
    return [(lam_den * x, lam_num * y) for x, y in P]

def valtr_endpoint(k, x):
    """P'(k, x+2, k): no (x+2)-cup, no k points in convex position, size sum_{l<=x} C(k-2,l).
    Valtr's construction (Baek-Balko Sec. 4) with a = k, u = x+2: clusters Q_i = P(k-i+2, i), i = 2..x+2
    (no (k-i+2)-cap, no i-cup, C(k-2, i-2) points), placed near base points q_i in general position sorted by
    increasing y, each cluster flattened (slopes <= 1/100) and tiny, so that Q_i is deep below Q_j for i < j."""
    clusters = []
    for i in range(2, x + 3):
        Q = P_au(k - i + 2, i)
        sl = maxslope(Q) if len(Q) > 1 else Fraction(0)
        F = int(100 * sl) + 1
        Qf = [(F * px, py) for px, py in Q]
        cx = (min(p[0] for p in Qf) + max(p[0] for p in Qf)) // 2
        cy = (min(p[1] for p in Qf) + max(p[1] for p in Qf)) // 2
        clusters.append([(px - cx, py - cy) for px, py in Qf])
    size = max(max(max(abs(p[0]), abs(p[1])) for p in Q) for Q in clusters) + 1
    Lb = 1000 * size
    # base points in general position, increasing y: alternate left/right of the y-axis on a convex-ish zigzag
    base = [((-1)**j * Lb * (j + 1), Lb * (j + 1) * (j + 2)) for j in range(len(clusters))]
    out = []
    for (bx, by), Q in zip(base, clusters):
        out += [(bx + px, by + py) for px, py in Q]
    return out

def check_cluster(P, a_cap, u_cup, kgon=None):
    cu, ca = longest_cup_cap(P)
    ok = cu < u_cup and ca < a_cap
    if kgon is not None:
        mc = max_convex_cupcap(P); ok = ok and mc < kgon
        return ok, (cu, ca, mc)
    return ok, (cu, ca)

def main():
    Pb = read(sys.argv[1]); m = int(sys.argv[2]); out = sys.argv[3]
    x = 2; k = m + 2*x; N = len(Pb)
    # good direction
    crit = sorted({(math.atan2(b[1]-a[1], b[0]-a[0]) + math.pi/2 + s*math.pi) % (2*math.pi)
                   for a, b in itertools.combinations(Pb, 2) for s in (0, 1)})
    good = None
    for i in range(len(crit)):
        t = (crit[i] + crit[(i+1) % len(crit)] + (2*math.pi if i == len(crit)-1 else 0)) / 2
        u = (round(math.cos(t)*10**9), round(math.sin(t)*10**9))
        proj = [u[0]*px + u[1]*py for px, py in Pb]
        if len(set(proj)) < N or 0 in proj: continue
        left, prof = left_profile(Pb, u)
        if sorted(prof) == [1, 2, 3, 3, 4, 4, 4, 4]:
            good = (u, left, prof); break
    u, left, prof = good
    print('direction', u, 'profile', prof)
    # clusters (pre-images)
    E = valtr_endpoint(k, x)
    ok, info = check_cluster(E, k, x + 2, kgon=k)
    print(f'endpoint cluster: {len(E)} pts (expect {sum(comb(k-2,l) for l in range(x+1))}), no {x+2}-cup & no {k}-gon: {ok} {info}')
    assert ok and len(E) == sum(comb(k-2, l) for l in range(x+1))
    pre = []
    for pos, i in enumerate(left):
        if pos == 0: pre.append(E); continue
        s = prof[pos]; a = k + 1 - x - s
        Q = P_au(a, x + 2)
        ok, info = check_cluster(Q, a, x + 2)
        assert ok and len(Q) == comb(k - 1 - s, x), (s, len(Q), info)
        pre.append(Q)
    print('cluster sizes (left):', [len(Q) for Q in pre], 'sum', sum(len(Q) for Q in pre))
    # rotate clockwise by pi/2: (px,py) -> (py, -px); centre each cluster
    rotc = []
    for Q in pre:
        R = [(py, -px) for px, py in Q]
        cx = (min(p[0] for p in R) + max(p[0] for p in R)) // 2; cy = (min(p[1] for p in R) + max(p[1] for p in R)) // 2
        rotc.append([(px - cx, py - cy) for px, py in R])
    # base in rotated frame
    a_, b_ = u
    RB = [(a_*px + b_*py, -b_*px + a_*py) for px, py in Pb]
    D = max(max(abs(c) for c in p) for p in RB)
    rho = min(Fraction(abs(orient(RB[i], RB[j], RB[l])), 6*D) for i, j, l in itertools.combinations(range(N), 3))
    gX = min(abs(RB[i][0] - RB[j][0]) for i, j in itertools.combinations(range(N), 2))
    H = 2*D
    # cluster internal geometry: need (after scaling X by al, Y by be) every internal line steep: |dY|*be/(|dX|*al) > 20*H/gX
    worst = Fraction(10**30)
    for R in rotc:
        for p, q in itertools.combinations(R, 2):
            dX = abs(q[0]-p[0]); dY = abs(q[1]-p[1])
            if dX == 0: continue
            worst = min(worst, Fraction(dY, dX))
    wX = max(max(abs(p[0]) for p in R) for R in rotc) + 1; wY = max(max(abs(p[1]) for p in R) for R in rotc) + 1
    # be * wY <= rho/10 ; al * wX <= rho/10 ; be/al >= 20*H/(gX*worst)
    be = rho / (10 * wY)
    ratio = Fraction(20) * H / (gX * worst)
    al = be / ratio
    # integer scale K
    K = math.ceil(1 / min(al, be)) * 10
    alK = max(1, math.floor(al * K)); beK = max(1, math.floor(be * K))
    print(f'rho~{float(rho):.3e} gX={gX:.3e} worst slope ratio {float(worst):.3e}; K={K:.3e} alK={alK} beK={beK}')
    pts = []
    for pos, i in enumerate(left):
        X0, Y0 = RB[i][0]*K, RB[i][1]*K
        pts += [(X0 + alK*px, Y0 + beK*py) for px, py in rotc[pos]]
    pts += [(-px, -py) for px, py in pts]
    S = set(pts)
    print('size', len(pts), 'distinct', len(S) == len(pts), 'symmetric', all((-px, -py) in S for px, py in pts), '0 not in S', (0, 0) not in S)
    xs = [p[0] for p in pts]
    print('distinct x:', len(set(xs)) == len(xs))
    import time
    if len(sys.argv) > 4 and sys.argv[4] == '--quick':
        with open(out, 'w') as f:
            f.write(f'# Corollary-15 x-blow-up (x=2, k={k}) of {sys.argv[1]}, direction {u}; centrally symmetric, {len(pts)} points; NOT YET CHECKED\n')
            for px, py in pts: f.write(f'{px} {py}\n')
        print('quick mode: wrote', out); return
    t = time.time(); col = sum(1 for p, q, r in itertools.combinations(pts, 3) if orient(p, q, r) == 0)
    print('collinear triples:', col, f'({time.time()-t:.1f}s)', flush=True)
    t = time.time(); mc = max_convex(pts); print('angular DP largest convex subset:', mc, f'({time.time()-t:.1f}s)', flush=True)
    with open(out, 'w') as f:
        f.write(f'# Corollary-15 x-blow-up (x=2, k={k}) of {sys.argv[1]}, direction {u}; centrally symmetric, {len(pts)} points; angular-DP largest convex subset {mc}\n')
        for px, py in pts: f.write(f'{px} {py}\n')
    t = time.time(); mc2 = max_convex_cupcap(pts); print('cup-cap DP largest convex subset:', mc2, f'({time.time()-t:.1f}s)', flush=True)

if __name__ == '__main__':
    main()
