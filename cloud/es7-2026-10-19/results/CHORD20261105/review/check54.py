#!/usr/bin/env python3
"""Evaluate the chord clauses (restricted to layers 0..8) on the certified 54-point set c6_54pts_9layers.pts with
exact Eisenstein-integer arithmetic.

Point = sum_j w_j zeta^j, zeta = e^(2 pi i/6), reduced to a + b zeta (zeta^2 = zeta - 1).  det(a1+b1 z, a2+b2 z) =
(a1 b2 - b1 a2) * sqrt3/2, so orientation signs are signs of integers.  Layers: orbits under multiplication by zeta,
sorted by |.|^2 = a^2+ab+b^2 decreasing (layer 0 outermost).  Labelling as in gen.py: v0 = a chosen vertex of
layer 0 is (0,0) (theta_0 = 0); (i,0) = the vertex of layer i in the half-open cone [v0, zeta v0), (i,k) = zeta^k (i,0).
theta_i in (0,60) strictly needs det(v0,(i,0)) > 0; Y(i,j) = [theta_i < theta_j] = [det((i,0),(j,0)) > 0].
All 6 choices of v0 are tried (they must give identical clause values)."""
import sys, json, itertools
from indep_enc import TRIPLE_OF, YINV, NTRIP

PTS = '<results-dir>/ES8SYM/sets/c6_54pts_9layers.pts'
D = '<six10-work-dir>'


def reduce6(w):
    # zeta^0..5 = 1, z, z-1, -1, -z, 1-z  -> (a, b)
    basis = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    a = sum(wj * basis[j][0] for j, wj in enumerate(w)); b = sum(wj * basis[j][1] for j, wj in enumerate(w))
    return (a, b)


def mulz(p):      # (a + b z) z = a z + b (z - 1) = -b + (a + b) z
    return (-p[1], p[0] + p[1])


def det2(p, q):   # 2/sqrt3 * det
    return p[0] * q[1] - p[1] * q[0]


def n2(p):
    return p[0] * p[0] + p[0] * p[1] + p[1] * p[1]


def orient(p, q, r):
    return det2(p, q) + det2(q, r) + det2(r, p)


raw = []
for line in open(PTS):
    if line.startswith('#') or not line.strip():
        continue
    raw.append(reduce6(list(map(int, line.split()))))
assert len(raw) == 54 and len(set(raw)) == 54
assert (0, 0) not in raw
# layers
norms = sorted({n2(p) for p in raw}, reverse=True)
assert len(norms) == 9, len(norms)
layers = []
for nv in norms:
    L = [p for p in raw if n2(p) == nv]
    assert len(L) == 6
    q = L[0]; orb = [q]
    for _ in range(5):
        q = mulz(q); orb.append(q)
    assert set(orb) == set(L), 'layer is not a zeta-orbit'
    layers.append(L)
# general position (all 54 points)
gp_bad = sum(1 for a, b, c in itertools.combinations(raw, 3) if orient(a, b, c) == 0)
# nesting: every point of layer i+1 strictly left of every ccw edge of layer i (ccw: v -> zeta v)
nest_bad = 0
for i in range(8):
    for v in layers[i]:
        w = mulz(v)
        for u in layers[i + 1]:
            if orient(v, w, u) <= 0:
                nest_bad += 1


def labelling(v0):
    w0 = mulz(v0)
    lab = {}; theta_ok = True
    seeds = []
    for i, L in enumerate(layers):
        cand = [u for u in L if det2(v0, u) >= 0 and det2(u, w0) > 0]
        assert len(cand) == 1, (i, cand)
        s = cand[0]
        if i == 0:
            assert s == v0
        elif det2(v0, s) == 0:
            theta_ok = False
        seeds.append(s)
        q = s
        for k in range(6):
            lab[6 * i + k] = q
            q = mulz(q)
    return lab, seeds, theta_ok


def rd(fn, limit=None, maxvar=None):
    out = []
    for line in open(fn):
        if line[0] in 'cp':
            continue
        l = list(map(int, line.split()))[:-1]
        if maxvar and any(abs(x) > maxvar for x in l):
            continue
        out.append(l)
        if limit and len(out) >= limit:
            break
    return out


chord = rd(D + '/main/chord_rules.clauses')
base = rd(D + '/cegar/base/encA_6_8_10.cnf', limit=7709, maxvar=5746)


def applicable(cl):
    for l in cl:
        v = abs(l)
        if v <= NTRIP:
            if max(TRIPLE_OF[v]) >= 54:
                return False
        else:
            i, j = YINV[v]
            if j >= 9:
                return False
    return True


results = []
for v0 in layers[0]:
    lab, seeds, theta_ok = labelling(v0)
    phase_distinct = all(det2(seeds[i], seeds[j]) != 0 for i in range(1, 9) for j in range(i + 1, 9))

    def lv(l):
        v = abs(l)
        if v <= NTRIP:
            a, b, c = (lab[x] for x in TRIPLE_OF[v]); o = orient(a, b, c); assert o != 0
            x = o > 0
        else:
            i, j = YINV[v]; x = det2(seeds[i], seeds[j]) > 0
        return x if l > 0 else not x

    ca = [c for c in chord if applicable(c)]
    cv = [c for c in ca if not any(lv(l) for l in c)]
    ba = [c for c in base if applicable(c)]
    bv = [c for c in ba if not any(lv(l) for l in c)]
    # phases (float, for the log only)
    import math
    ang = [math.degrees(math.atan2(s[1] * math.sqrt(3) / 2, s[0] + s[1] / 2)) for s in seeds]
    th = [round((a - ang[0]) % 360, 6) for a in ang]
    results.append({'v0': v0, 'theta_strict_ok': theta_ok, 'phases_distinct': phase_distinct, 'theta_deg': th,
                    'chord_applicable': len(ca), 'chord_violated': cv, 'base_applicable': len(ba), 'base_violated': bv,
                    'chord_values_signature': hash(tuple(tuple(lv(l) for l in c) for c in ca))})
print(json.dumps({'points': len(raw), 'layers': len(layers), 'radii2_desc': norms, 'gp_degenerate_triples': gp_bad,
                  'nesting_violations': nest_bad}, default=str))
sigs = {r['chord_values_signature'] for r in results}
for r in results:
    r.pop('chord_values_signature')
    print(json.dumps(r, default=str))
print('identical chord literal values for all 6 choices of v0:', len(sigs) == 1)
