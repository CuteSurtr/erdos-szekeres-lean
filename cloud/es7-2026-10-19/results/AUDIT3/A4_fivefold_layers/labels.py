#!/usr/bin/env python3
"""Labellings of a real symmetric configuration in the encoders' normal forms (audit A4, own implementation).

Layer normal form (symcnf_layers.py): orbit o = o-th convex layer (outermost first); (0,0) = any point of layer 0;
for o >= 1 the representative (o,0) is the point of layer o whose angle at the centre, measured counter-clockwise
from the ray to (0,0), lies in the open interval (0, 2 pi/m); (o,r) = R^r (o,0).
Angle normal form (symcnf.py, odd m): orbit 0 = any orbit, (0,0) = any of its points; the other orbits' sector
representatives sorted by increasing angle.
Sector membership is decided exactly and cross-checked with floating-point angles.
"""
import cmath, math
from geo import Z4, Z5


def sector_index(ring, p00, q):
    """k such that the angle of q, measured ccw at the centre from the ray to p00, is in (2 pi k/m, 2 pi (k+1)/m);
    exact; None if on a boundary ray. Cross-checked with floats."""
    m = ring.m
    if ring is Z5:
        w = Z5.mul(q, Z5.conj(p00))
        zinv = Z5.conj((0, 1, 0, 0, 0))
        ks = []
        for k in range(m):
            # angle(w) - 2 pi k/m in (0, 2 pi/m)  <=>  Im(w z^-k) > 0 and Im(w z^-(k+1)) < 0
            a = w
            for _ in range(k):
                a = Z5.mul(a, zinv)
            b = Z5.mul(a, zinv)
            sa, sb = Z5.im_sign(a), Z5.im_sign(b)
            if sa == 0 or sb == 0:
                return None
            if sa > 0 and sb < 0:
                ks.append(k)
        assert len(ks) == 1, ks
        k = ks[0]
    else:
        wx = q[0] * p00[0] + q[1] * p00[1]
        wy = q[1] * p00[0] - q[0] * p00[1]
        if wx == 0 or wy == 0:
            return None
        k = {(1, 1): 0, (-1, 1): 1, (-1, -1): 2, (1, -1): 3}[((wx > 0) - (wx < 0), (wy > 0) - (wy < 0))]
    # float cross-check
    ang = (cmath.phase(ring.to_complex(q)) - cmath.phase(ring.to_complex(p00))) % (2 * math.pi)
    kf = ang / (2 * math.pi / m)
    if abs(kf - round(kf)) > 1e-7:
        assert int(kf) == k, (kf, k)
    return k


def layer_labelling(cfg, layers_orbits, j00=0, ccw=True, swap=None, shift=0, rotate_p00_only=False):
    """layers_orbits: orbit indices, outermost first. j00: which point of layer 0 is (0,0).
    Mutations for negative controls: ccw=False labels clockwise; swap=(i,j) swaps two layers; shift=k takes the
    representative from sector k instead of 0; rotate_p00_only relabels (0,0) after the representatives are chosen."""
    ring, m = cfg.ring, cfg.m
    order = list(layers_orbits)
    if swap:
        i, j = swap
        order[i], order[j] = order[j], order[i]
    p00 = cfg.orbits[order[0]][j00]
    lab = {}
    step = 1 if ccw else -1
    for o, oi in enumerate(order):
        if o == 0:
            q = p00
        else:
            cand = [x for x in cfg.orbits[oi] if sector_index(ring, p00, x) == shift % m]
            assert len(cand) == 1
            q = cand[0]
        for r in range(m):
            lab[o * m + r] = ring.rot(q, step * r)
    if rotate_p00_only:
        for r in range(m):
            lab[r] = ring.rot(p00, step * (r + 1))
    return lab


def angle_labelling(cfg, orbit0, j00=0):
    ring, m = cfg.ring, cfg.m
    p00 = cfg.orbits[orbit0][j00]
    reps = {}
    for oi in range(len(cfg.orbits)):
        if oi == orbit0:
            continue
        cand = [x for x in cfg.orbits[oi] if sector_index(ring, p00, x) == 0]
        assert len(cand) == 1
        reps[oi] = cand[0]
    # sort by angle: exact comparison chi(c, u, v) > 0 <=> u before v (all angles in (0, 2 pi/m), m >= 3)
    import functools
    c = ring.zero
    others = sorted(reps, key=functools.cmp_to_key(lambda a, b: -1 if ring.orient(c, reps[a], reps[b]) > 0 else 1))
    # float cross-check of the order
    angs = [(cmath.phase(ring.to_complex(reps[o])) - cmath.phase(ring.to_complex(p00))) % (2 * math.pi) for o in others]
    assert all(angs[i] < angs[i + 1] for i in range(len(angs) - 1)), angs
    lab = {}
    for o, oi in enumerate([orbit0] + others):
        q = p00 if o == 0 else reps[oi]
        for r in range(m):
            lab[o * m + r] = ring.rot(q, r)
    return lab
