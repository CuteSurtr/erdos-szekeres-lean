#!/usr/bin/env python3
"""Soundness test of gen.py on real configurations.

Given layers (r_i, theta_i) (outermost first), build the real assignment of every non-chain variable
(triple orbit orientations from coordinates, Y/H from the phases), extend it to the chain variables by
least-fixpoint propagation, and report unsatisfied clauses per family.  Every family except 'chain' must be
satisfied by every real nested configuration; 'chain' must be satisfied iff the configuration has no convex K-gon
(with an outermost-layer vertex as pivot -- i.e. no convex K-gon at all).

usage: validate.py m K t CNF  (random N | pts FILE.pts | cfg r0,th0;r1,th1;...)
"""
import sys, math, json, random, itertools
from fractions import Fraction
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import gen


def orient_f(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def layers_to_points(m, layers):
    th0 = layers[0][1]
    pts = []
    lay = []
    for (r, th) in layers:
        th = (th - th0) % (2 * math.pi / m)
        lay.append((r, th))
        for k in range(m):
            a = th + 2 * math.pi * k / m
            pts.append((r * math.cos(a), r * math.sin(a)))
    return pts, lay


def read_pts(fn, m):
    rows = []
    for line in open(fn):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        w = list(map(int, line.split()))
        x = sum(w[j] * math.cos(2 * math.pi * j / m) for j in range(m))
        y = sum(w[j] * math.sin(2 * math.pi * j / m) for j in range(m))
        rows.append((x, y))
    pts = [p for p in rows if math.hypot(*p) > 1e-6]
    # group into layers by radius
    pts.sort(key=lambda p: -math.hypot(*p))
    layers = []
    for s in range(0, len(pts), m):
        grp = pts[s:s + m]
        r = math.hypot(*grp[0])
        th = math.atan2(grp[0][1], grp[0][0]) % (2 * math.pi / m)
        layers.append((r, th))
    return layers


def check(m, K, t, E, layers, verbose=True):
    pts, lay = layers_to_points(m, layers)
    n = m * t
    assign = {}
    mind = float('inf')
    for C, v in E.tvar.items():
        d = orient_f(pts[C[0]], pts[C[1]], pts[C[2]])
        mind = min(mind, abs(d))
        assign[v] = d > 0
    unit = math.pi / m if m % 2 else 2 * math.pi / m
    psi = [th % unit for (_, th) in lay]
    for (i, j), v in E.Y.items():
        assign[v] = psi[i] < psi[j]
    for i, v in E.H.items():
        assign[v] = lay[i][1] < math.pi / m
    # chain variables: least fixpoint
    def litval(l):
        x = assign.get(abs(l), False)
        return x if l > 0 else not x
    a, b = E.ranges['chain']
    changed = True
    while changed:
        changed = False
        for cl in E.cls[a:b]:
            if any(litval(l) for l in cl):
                continue
            pos = [l for l in cl if l > 0 and abs(l) > E.ntriplevars + len(E.Y) + len(E.H)]
            if pos:
                assign[pos[0]] = True
                changed = True
    res = {}
    for fam, (a, b) in E.ranges.items():
        bad = 0
        for cl in E.cls[a:b]:
            if not any(litval(l) for l in cl):
                bad += 1
        res[fam] = bad
    return res, mind, lay


def random_layers(m, t, rng, mode):
    """random nested configuration; mode 'free' or 'needle' (small phase drift, ratios near 1)"""
    while True:
        layers = [(1.0, 0.0)]
        r, th = 1.0, 0.0
        ok = True
        for i in range(1, t):
            for _ in range(200):
                if mode == 'needle':
                    th2 = th + rng.uniform(-0.15, 0.15)
                    r2 = r * rng.uniform(0.6, 0.999)
                else:
                    th2 = rng.uniform(0, 2 * math.pi)
                    r2 = r * rng.uniform(0.2, 0.999)
                # nesting: vertex of new layer inside every previous layer
                good = True
                for (rr, tt) in layers:
                    # point at angle th2 radius r2 inside regular m-gon (rr,tt):
                    # distance to centre along direction must be < apothem / cos(angle to nearest edge normal)
                    off = (th2 - tt) % (2 * math.pi / m) - math.pi / m
                    if r2 * math.cos(off) >= rr * math.cos(math.pi / m) * (1 - 1e-9):
                        good = False
                        break
                if good:
                    layers.append((r2, th2))
                    r, th = r2, th2
                    break
            else:
                ok = False
                break
        if ok:
            return layers


if __name__ == '__main__':
    m, K, t = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    E, cnt, st = gen.build(m, K, t)
    mode = sys.argv[4]
    if mode == 'pts':
        layers = read_pts(sys.argv[5], m)[:t]
        res, mind, lay = check(m, K, t, E, layers)
        print('pts', sys.argv[5], 'layers used', len(layers), res, 'min|det| %.3g' % mind)
    elif mode == 'random':
        N = int(sys.argv[5])
        rng = random.Random(int(sys.argv[6]) if len(sys.argv) > 6 else 1)
        tot = {}
        free_ok = 0
        for s in range(N):
            layers = random_layers(m, t, rng, 'needle' if s % 2 else 'free')
            res, mind, lay = check(m, K, t, E, layers)
            if mind < 1e-9:
                continue
            for k, v in res.items():
                if k != 'chain' and v:
                    print('VIOLATION', k, v, layers)
                tot[k] = tot.get(k, 0) + (v > 0)
            if res['chain'] == 0:
                free_ok += 1
        print('random', N, 'configs; configs with violated clauses per family:', tot,
              '; configs satisfying the chain family:', free_ok)
