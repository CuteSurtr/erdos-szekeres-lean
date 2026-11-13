#!/usr/bin/env python3
"""Exact checks cited in k8_soundness.tex (6 November 2026).  Standard library only; imports no encoder code.

For (m, t) = (6, 11) and (7, 10):
  1. triple orbits under the rotation (i,k) -> (i,k+1): number, sizes, stabilised orbits (each must be
     {x, rho^{m/3} x, rho^{2m/3} x} in one layer), and orbits containing a same-layer antipodal pair (even m);
  2. the circular-order dichotomy: for every orbit representative (encoder B's canonical form, re-implemented here)
     and every phase pattern (ranks of the free layers, H bits for odd m), the six integer keys of the three points
     and their antipodes are either not distinct (even m, same-layer antipodal pair), or their cyclic P/A word
     alternates, or it is a rotation of PPPAAA; any other word is counted as 'other' (must be 0);
  3. encoder A's representative phases (gen.py, Enc.patterns): every direction is an integer multiple of
     pi/(m(nl+1)) (odd m) or 2pi/(m(nl+1)) (even m); the least distance of a gap that is not exactly pi from
     {0, pi} (exact, in units of pi);
  4. the rounding error of encoder A's binary64 directions: its float expressions are re-evaluated exactly as in
     gen.py and compared with the exact angles, pi being enclosed between two 36-digit rationals; the value
     reduced modulo 2*math.pi is asserted to lie in [0, 2*math.pi) before the reduction, so the reduction
     returns it unchanged.  The inputs depend only on m and on the number (1, 2 or 3) of layers of a triple,
     not on t or K.
Run: python3 -I k8_soundness_checks.py   (a few seconds on one core)
"""
import itertools
import math
from fractions import Fraction as Fr

PI_LO = Fr('3.14159265358979323846264338327950288')
PI_HI = Fr('3.14159265358979323846264338327950289')


def canon(tri, m):
    best = None
    for (_, k0) in tri:
        s = (-k0) % m
        rt = tuple(sorted((i, (k + s) % m) for (i, k) in tri))
        if best is None or rt < best:
            best = rt
    return best


def orbits_and_dichotomy(m, t):
    odd = m % 2 == 1
    pts = [(i, k) for i in range(t) for k in range(m)]
    orbits = {}
    ntri = 0
    for tri in itertools.combinations(pts, 3):
        ntri += 1
        orbits.setdefault(canon(tri, m), []).append(tri)
    sizes = {}
    for mem in orbits.values():
        sizes[len(mem)] = sizes.get(len(mem), 0) + 1
    stab = [c for c, mem in orbits.items() if len(mem) < m]
    stab_ok = all(len({i for i, _ in c}) == 1
                  and sorted((k - c[0][1]) % m for _, k in c) == [0, m // 3, 2 * m // 3] for c in stab)
    anti = [c for c in orbits if not odd and any(a[0] == b[0] and (a[1] - b[1]) % m == m // 2
                                                 for a, b in itertools.combinations(c, 2))]
    cnt = {'alternating': 0, 'block': 0, 'coinciding keys': 0, 'other': 0}
    for c in orbits:
        free = sorted(set(i for i, _ in c) - {0})
        for ranks in itertools.permutations(range(len(free))):
            rk = {L: r + 1 for L, r in zip(free, ranks)}
            rk[0] = 0
            for hb in itertools.product([0, 1], repeat=len(free) if odd else 0):
                h = {L: b for L, b in zip(free, hb)}
                h[0] = 0
                objs = []
                for idx, (i, k) in enumerate(c):
                    if odd:
                        J = (2 * k + h[i]) % (2 * m)
                        Ja = (J + m) % (2 * m)
                    else:
                        J, Ja = k, (k + m // 2) % m
                    objs.append(((J, rk[i]), 'P', idx))
                    objs.append(((Ja, rk[i]), 'A', idx))
                if len(set(o[0] for o in objs)) < 6:
                    cnt['coinciding keys'] += 1
                    continue
                objs.sort()
                w = ''.join(o[1] for o in objs)
                if w in ('PAPAPA', 'APAPAP'):
                    cnt['alternating'] += 1
                elif 'PPPAAA' in w + w:
                    cnt['block'] += 1
                else:
                    cnt['other'] += 1
    return dict(triples=ntri, orbits=len(orbits), orbit_sizes=sizes, stabilised_orbits=len(stab),
                stabilisers_are_3_cycles_in_one_layer=stab_ok, antipodal_orbits=len(anti), patterns=cnt)


def representative_separation(m, t):
    """Encoder A's representative directions, exactly (units of pi)."""
    odd = m % 2 == 1
    unit = Fr(1, m) if odd else Fr(2, m)
    worst = None
    seen = set()
    for tri in itertools.combinations([(i, k) for i in range(t) for k in range(m)], 3):
        c = canon(tri, m)
        if c in seen:
            continue
        seen.add(c)
        Ls = sorted(set(i for i, _ in c))
        nl = len(Ls)
        step = unit / (nl + 1)
        for perm in itertools.permutations(Ls):
            if 0 in Ls and perm[0] != 0:
                continue
            psi = {L: (Fr(0) if L == 0 else unit * (r + (0 if 0 in Ls else 1)) / (nl + 1))
                   for r, L in enumerate(perm)}
            hs = [L for L in Ls if L != 0]
            for bits in itertools.product([True, False], repeat=len(hs) if odd else 0):
                th = dict(psi)
                for L, bt in zip(hs, bits):
                    th[L] = psi[L] + (0 if bt else Fr(1, m))
                ang = sorted((th[i] + Fr(2 * k, m)) % 2 for i, k in c)
                assert all((x / step).denominator == 1 for x in ang)
                assert ang[-1] <= 2 - step
                for g in (ang[1] - ang[0], ang[2] - ang[1], 2 - (ang[2] - ang[0])):
                    assert g > 0
                    if g != 1:
                        d = min(g, abs(g - 1))
                        worst = d if worst is None or d < worst else worst
    return worst


def float_error(m):
    """Largest |computed - exact| over all directions encoder A can compute (gen.py float expressions)."""
    odd = m % 2 == 1
    worst = Fr(0)
    n = 0
    for nl in (1, 2, 3):
        cases = [(None, 0)] + [(q, h) for q in range(1, nl + 1) for h in ((0, 1) if odd else (0,))]
        for q, h in cases:
            if q is None:
                th, ex = 0.0, Fr(0)
            else:
                unit = math.pi / m if odd else 2 * math.pi / m      # as in Enc.patterns
                psi = unit * q / (nl + 1)
                th = (psi + (0.0 if h == 0 else math.pi / m)) if odd else psi
                ex = (Fr(1, m) if odd else Fr(2, m)) * Fr(q, nl + 1) + (Fr(h, m) if odd else 0)
            for k in range(m):
                pre = th + 2 * math.pi * k / m                            # the float that Enc.angle_config reduces
                a = pre % (2 * math.pi)                                   # as in Enc.angle_config
                # the reduction is a no-op: pre is already in [0, 2*math.pi) (float comparison, exact)
                assert 0.0 <= pre < 2 * math.pi and a == pre
                exk = ex + Fr(2 * k, m)
                fa = Fr(a)
                worst = max(worst, abs(fa - exk * PI_LO), abs(fa - exk * PI_HI))
                n += 1
    return n, worst


if __name__ == '__main__':
    for m, t in [(6, 11), (7, 10)]:
        print('m=%d t=%d' % (m, t), orbits_and_dichotomy(m, t))
        print('  least distance of a non-pi gap from {0, pi}: %s pi' % representative_separation(m, t))
        n, err = float_error(m)
        print('  encoder A directions: %d cases (nl, q, h, k), all reductions no-ops, max |float - exact| < %.3e'
              % (n, float(err)))
