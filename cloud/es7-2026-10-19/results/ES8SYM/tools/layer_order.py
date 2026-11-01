#!/usr/bin/env python3
"""Permute the rows of an m-fold point file (rows of integers w_0..w_{m-1}, point = sum_j w_j zeta^j) into the
layer form expected by `verify_cfg.py --pts`: orbits sorted by decreasing radius (exact comparison), row o*m+k equal
(as an element of Z[zeta_m]) to zeta^k times row o*m, and the centre (if present) last.

The output contains exactly the input rows (same strings), only in a different order; the script checks this and
that every orbit is complete.  Whether the orbits are really the convex layers is then checked by verify_cfg.py.
usage: layer_order.py IN.pts m OUT.pts
"""
import os
import sys
from functools import cmp_to_key

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zm import ZM


def main():
    src, m, dst = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    lines = [l.rstrip('\n') for l in open(src) if l.strip() and not l.startswith('#')]
    rows = [[int(v) for v in l.split()] for l in lines]
    assert all(len(r) == m for r in rows)
    Z = ZM(m)
    canon = [Z.canon(r) for r in rows]
    assert len(set(canon)) == len(rows), 'repeated point'
    where = {c: i for i, c in enumerate(canon)}
    zero = Z.canon([0] * m)
    centre = [i for i, c in enumerate(canon) if c == zero]
    used = set(centre)
    orbits = []
    for i in range(len(rows)):
        if i in used:
            continue
        orb = []
        for k in range(m):
            c = Z.canon(Z.rot(rows[i], k))
            assert c in where, 'orbit of row %d is not complete' % i
            orb.append(where[c])
        assert not (set(orb) & used)
        used |= set(orb)
        orbits.append(orb)
    orbits.sort(key=cmp_to_key(lambda a, b: -Z.r2cmp(rows[a[0]], rows[b[0]])))
    order = [i for orb in orbits for i in orb] + centre
    assert sorted(order) == list(range(len(rows)))
    with open(dst, 'w') as f:
        f.write('# rows of %s in layer form (orbits by decreasing radius, centre last); m=%d n=%d\n'
                % (os.path.basename(src), m, len(rows)))
        for i in order:
            f.write(lines[i] + '\n')
    print('orbits=%d centre=%d rows=%d' % (len(orbits), len(centre), len(rows)))


if __name__ == '__main__':
    main()
