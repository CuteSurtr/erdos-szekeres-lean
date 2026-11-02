#!/usr/bin/env python3
"""Per-pivot cross-check of the chain family on real configurations (any t, e.g. t = 10).
For each pivot layer i: (a) does the least-fixpoint extension of the real assignment violate a chain clause of
pivot i?  (b) independent DP: sort Q_p by angle around p = (i,0) (atan2 in the tangent frame), longest chain with
left turns (O(n^3) DP over pairs) -- is there a convex polygon of K points with vertex p and the other vertices in
layers >= i?  The answers must agree (soundness needs (a) => (b)).
usage: test_chain_dp.py CNF N seed
"""
import sys, json, math, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import gen
from validate import orient_f, layers_to_points, random_layers
from validate2 import real_assign


def dp_has_chain(pts, p, Q, L):
    P = pts[p]
    # tangent frame: direction of p from O is outward normal; angles of q - P measured from -normal (into disk)
    nx, ny = P[0], P[1]
    ang = {}
    for q in Q:
        dx, dy = pts[q][0] - P[0], pts[q][1] - P[1]
        # rotate so that the inward normal (-nx,-ny) is the +y axis; angle in (0, pi) from the +x axis
        ux, uy = -ny, nx                      # tangent direction (frame (u, -n) right-handed)
        a = math.atan2(-(dx * nx + dy * ny), dx * ux + dy * uy)
        ang[q] = a
    order = sorted(Q, key=lambda q: ang[q])
    # check orientation consistency: orient(p, q, q') > 0 iff q' after q?  (ccw around p)
    best = {}
    n = len(order)
    for b in range(n):
        for a in range(b):
            best[(order[a], order[b])] = 2
    for c in range(n):
        for b in range(c):
            qb, qc = order[b], order[c]
            for a in range(b):
                qa = order[a]
                if orient_f(pts[qa], pts[qb], pts[qc]) > 0:
                    v = best[(qa, qb)] + 1
                    if v > best[(qb, qc)]:
                        best[(qb, qc)] = v
    return max(best.values()) >= L, order, ang


def main():
    cnf = sys.argv[1]; N = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
    meta = json.load(open(cnf + '.json'))
    m, K, t = meta['m'], meta['K'], meta['t']
    E = gen.Enc(m, K, t)
    base = E.nv
    # clause index ranges per pivot
    c0 = meta['ranges']['chain'][0]
    piv = []
    for (i, nq, ncl) in meta['chain']:
        piv.append((i, c0, c0 + ncl)); c0 += ncl
    agree = 0; dis = 0
    for s in range(N):
        layers = random_layers(m, t, rng, ['free', 'needle'][s % 2])
        assign, mind = real_assign(E, m, layers)
        if mind < 1e-9:
            continue
        pts, lay = layers_to_points(m, layers)
        viol = {i: False for (i, _, _) in piv}
        def lv(l):
            x = assign.get(abs(l), False)
            return x if l > 0 else not x
        with open(cnf) as f:
            f.readline()
            for idx, line in enumerate(f):
                if idx < piv[0][1]:
                    continue
                cl = list(map(int, line.split()))[:-1]
                if any(lv(l) for l in cl):
                    continue
                pos = [l for l in cl if l > base]
                if pos:
                    assign[pos[0]] = True
                    continue
                for (i, a, b) in piv:
                    if a <= idx < b:
                        viol[i] = True
        res = []
        for (i, a, b) in piv:
            p = i * m
            Q = [x for x in range(i * m, t * m) if x != p]
            has, order, ang = dp_has_chain(pts, p, Q, K - 1)
            # sanity: angular order agrees with orientation around p
            for u in range(len(order) - 1):
                assert orient_f(pts[p], pts[order[u]], pts[order[u + 1]]) > 0
            if has == viol[i]:
                agree += 1
            else:
                dis += 1
                print('DISAGREE pivot layer', i, 'cnf', viol[i], 'dp', has, layers)
            res.append(int(has))
        print('config', s, 'pivot layers with a convex %d-gon:' % K, res, flush=True)
    print('agreements', agree, 'disagreements', dis)


main()
