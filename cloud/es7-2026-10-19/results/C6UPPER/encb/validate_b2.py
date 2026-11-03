#!/usr/bin/env python3
"""Float64 assignment for a gen_b2.py CNF from a real layered configuration, for odd and even m
(C7UPPER/tests/validate_b.py with psi = theta mod pi/m for odd m and mod 2pi/m for even m; H only for odd m)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'C7UPPER', 'tests'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'C7UPPER'))
from validate import orient_f, layers_to_points
from validate_b import check


def assignment(mp, layers):
    m = mp['m']
    pts, lay = layers_to_points(m, layers)
    A = {}; mind = float('inf')
    for c, v in mp['orb']:
        d = orient_f(*[pts[i * m + k] for (i, k) in c]); mind = min(mind, abs(d)); A[v] = d > 0
    unit = math.pi / m if m % 2 else 2 * math.pi / m
    psi = [th % unit for (_, th) in lay]
    for i, j, v in mp['Y']:
        A[v] = psi[i] < psi[j]
    for i, v in mp['H']:
        A[v] = lay[i][1] < math.pi / m
    return A, mind
