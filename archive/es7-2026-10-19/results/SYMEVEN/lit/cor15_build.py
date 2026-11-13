#!/usr/bin/env python3
"""Build Baek-Balko's x-blow-up (Corollary 15, SoCG 2025 Sec. 6.2) of a centrally symmetric base, with threshold
L = N/2 and clusters paired by the half-turn, for x = 1 (k = m + 2), and check the result exactly.
For x = 1 every cluster is a cap rotated clockwise by pi/2 (a right-bulging, almost vertical arc):
  left point p_i, i >= 2: P'(k-1-s_i... ) = cap of (k-1-s_i) points;  p_1: P'(k,3,k) = cap of k-1 points.
Right clusters are the negatives of the left ones.  Usage: cor15_build.py base.txt m out.txt"""
import sys, math, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from maxconvex import max_convex, orient

def read(path):
    P = []
    for line in open(path):
        line = line.strip()
        if line and not line.startswith('#'):
            x, y = line.split()[:2]; P.append((int(x), int(y)))
    return P

def convex_pos(T):
    for i in range(len(T)):
        for a, b, c in itertools.combinations([j for j in range(len(T)) if j != i], 3):
            o1 = orient(T[a], T[b], T[i]); o2 = orient(T[b], T[c], T[i]); o3 = orient(T[c], T[a], T[i])
            if (o1 > 0) == (o2 > 0) == (o3 > 0): return False
    return True

def left_profile(P, u):
    proj = [u[0]*x + u[1]*y for x, y in P]
    order = sorted(range(len(P)), key=lambda i: proj[i])
    left = [i for i in order if proj[i] < 0]
    prof = []
    for pos, i in enumerate(left):
        before = left[:pos]; best = 1
        for r in range(len(before), 0, -1):
            if any(convex_pos([P[j] for j in T] + [P[i]]) for T in itertools.combinations(before, r)):
                best = r + 1; break
        prof.append(best)
    return left, prof

def main():
    P = read(sys.argv[1]); m = int(sys.argv[2]); out = sys.argv[3]
    N = len(P); k = m + 2
    target = [1, 2, 3, 3, 4, 4, 4, 4] if m == 6 else None
    # find a good direction
    crit = sorted({(math.atan2(b[1]-a[1], b[0]-a[0]) + math.pi/2 + s*math.pi) % (2*math.pi)
                   for a, b in itertools.combinations(P, 2) for s in (0, 1)})
    good = None
    for i in range(len(crit)):
        t = (crit[i] + crit[(i+1) % len(crit)] + (2*math.pi if i == len(crit)-1 else 0)) / 2
        u = (round(math.cos(t)*10**9), round(math.sin(t)*10**9))
        proj = [u[0]*x + u[1]*y for x, y in P]
        if len(set(proj)) < N or 0 in proj: continue
        left, prof = left_profile(P, u)
        if sorted(prof) == target:
            good = (u, left, prof); break
    assert good, 'no good direction'
    u, left, prof = good
    print('direction u =', u, ' left profile (x-order):', prof)
    a, b = u
    rot = lambda p: (a*p[0] + b*p[1], -b*p[0] + a*p[1])     # orientation-preserving similarity
    R = [rot(p) for p in P]
    # margins
    D = max(max(abs(c) for c in p) for p in R)
    rho = min(abs(orient(R[i], R[j], R[l])) / (6*D) for i, j, l in itertools.combinations(range(N), 3))
    gX = min(abs(R[i][0] - R[j][0]) for i, j in itertools.combinations(range(N), 2))
    H = 2*D
    cmax = k - 1
    # offsets (-alpha t^2, beta t), t = 1..c:  need beta*cmax, alpha*cmax^2 << rho;  beta/alpha >> 2*cmax*H/gX
    # work with a global integer scale K so that alpha >= 1
    beta_over_alpha = 10 * 2 * cmax * H / gX
    # choose beta = rho/(10*cmax) (in rotated units), alpha = beta / beta_over_alpha; scale K to make alpha >= 1
    beta = rho / (10*cmax); alpha = beta / beta_over_alpha
    K = max(1, math.ceil(1 / alpha)) * 10
    Kb, Ka = int(beta*K), max(1, int(alpha*K))
    print(f'D={D:.3e} rho={rho:.3e} gX={gX:.3e}  scale K={K:.3e} beta*K={Kb:.3e} alpha*K={Ka:.3e}')
    pts = []
    for pos, i in enumerate(left):
        c = (k - 1) if pos == 0 else (k - 1 - prof[pos])     # x = 1: cluster sizes C(k-1-s,1) = k-1-s; p_1: 1+(k-2)
        X0, Y0 = R[i][0]*K, R[i][1]*K
        cl = [(X0 - Ka*t*t, Y0 + Kb*t) for t in range(1, c+1)]
        pts += cl
    pts += [(-x, -y) for x, y in pts]
    print('size', len(pts), ' expected 2^(k-2) =', 2**(k-2))
    S = set(pts)
    assert len(S) == len(pts), 'duplicates'
    assert all((-x, -y) in S for x, y in pts) and (0, 0) not in S, 'symmetry'
    col = sum(1 for p, q, r in itertools.combinations(pts, 3) if orient(p, q, r) == 0)
    print('collinear triples:', col)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print('distinct x:', len(set(xs)) == len(xs), ' distinct y:', len(set(ys)) == len(ys))
    mc = max_convex(pts)
    print('largest subset in convex position:', mc, ' (need <', k, ')')
    with open(out, 'w') as f:
        f.write(f'# Corollary-15 x-blow-up (x=1, k={k}) of {sys.argv[1]}, direction {u}; centrally symmetric, '
                f'{len(pts)} points; largest convex subset {mc}\n')
        for x, y in pts: f.write(f'{x} {y}\n')

if __name__ == '__main__':
    main()
