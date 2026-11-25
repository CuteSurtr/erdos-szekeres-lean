#!/usr/bin/env python3
"""Own re-evaluation of encoder A's float directions (C7UPPER/gen.py patterns + angle_config) for a given m:
is every reduction x % (2*math.pi) a no-op, and how far is each float direction from the exact one?
Exact directions are rationals times pi; pi is enclosed by 50-digit rationals. usage: encA_float_m.py m [m ...]"""
import sys, math
from fractions import Fraction as Fr

PI_LO = Fr('3.14159265358979323846264338327950288419716939937510')
PI_HI = PI_LO + Fr(1, 10 ** 50)


def check(m):
    odd = m % 2 == 1
    unit_f = math.pi / m if odd else 2 * math.pi / m          # gen.py patterns()
    unit_x = Fr(1, m) if odd else Fr(2, m)                     # in units of pi
    worst, n = Fr(0), 0
    for nl in (1, 2, 3):                                       # number of distinct layers of a triple
        for with0 in (True, False):
            for r in range(nl):
                q = r + (0 if with0 else 1)
                if with0 and r == 0:
                    variants = [(0.0, Fr(0))]                  # layer 0: psi = 0.0, theta = 0.0
                else:
                    psi_f = unit_f * q / (nl + 1)              # same evaluation order as gen.py
                    psi_x = unit_x * q / (nl + 1)
                    if odd:
                        variants = [(psi_f + 0.0, psi_x), (psi_f + math.pi / m, psi_x + Fr(1, m))]
                    else:
                        variants = [(psi_f, psi_x)]
                for th_f, th_x in variants:
                    for k in range(m):
                        pre = th_f + 2 * math.pi * k / m       # gen.py angle_config()
                        a = pre % (2 * math.pi)
                        assert 0.0 <= pre < 2 * math.pi and a == pre, (m, nl, q, k)
                        ex = th_x + Fr(2 * k, m)
                        assert ex < 2
                        fa = Fr(a)
                        worst = max(worst, abs(fa - ex * PI_LO), abs(fa - ex * PI_HI))
                        n += 1
    # exact directions are multiples of delta0 = unit/(nl+1) >= unit/4; so is pi
    delta0 = unit_x / 4
    return n, float(worst), delta0


if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        n, w, d0 = check(m)
        print('m=%d: %d float directions, all reductions no-ops, max |float - exact| = %.3e; '
              'exact non-pi gaps are >= %s pi from 0 and pi (eps = 1e-9)' % (m, n, w, d0))
