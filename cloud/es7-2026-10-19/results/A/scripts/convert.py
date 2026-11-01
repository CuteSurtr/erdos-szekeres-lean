#!/usr/bin/env python3
"""Convert integer point sets to x-sorted signotopes, exactly (Python ints only).

usage: convert.py [--rot90] OUT_PREFIX FILE [FILE ...]

--rot90 first applies the rotation (x, y) -> (-y, x) (determinant 1, orientations unchanged), so the
sweep direction, and hence the signotope, is a different one for the same order type.

Input lines: `tag label hash n x1 y1 ... xn yn` (the pool files distinct_K7*.txt).
If two points share an x-coordinate, the exact shear (x, y) -> (L*x + y, y) with
L = 2*max|y| + 1 is applied first. Its determinant is L > 0, so every orientation is
unchanged, and it makes all x distinct (the new x-order is the lexicographic (x, y) order).
Points are then sorted by x and the orientation of every triple i<j<k (1-based) is recorded:
'+' = counterclockwise = CNF variable X(i,j,k) true, '-' = clockwise.

Outputs:
  OUT_PREFIX.sig  : `id tag label hash n signs` (signs: C(n,3) chars in lexicographic order)
  OUT_PREFIX.pts  : `id n x1 y1 ... xn yn` (the x-sorted, possibly sheared, integer points)
  OUT_PREFIX.meta.json
"""
import itertools
import json
import sys


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def to_sig(pts):
    """Return (sorted points, sign string, sheared?) for a list of integer points."""
    sheared = False
    if len(set(p[0] for p in pts)) != len(pts):
        L = 2 * max(abs(p[1]) for p in pts) + 1
        pts = [(L * x + y, y) for x, y in pts]
        sheared = True
    pts = sorted(pts)
    xs = [p[0] for p in pts]
    assert len(set(xs)) == len(xs), "distinct x needed"
    n = len(pts)
    out = []
    for i, j, k in itertools.combinations(range(n), 3):
        o = orient(pts[i], pts[j], pts[k])
        if o == 0:
            raise ValueError("collinear triple")
        out.append('+' if o > 0 else '-')
    return pts, ''.join(out), sheared


def main():
    args = sys.argv[1:]
    rot = args[0] == '--rot90'
    if rot:
        args = args[1:]
    prefix = args[0]
    files = args[1:]
    nid = 0
    nshear = 0
    per_file = {}
    with open(prefix + '.sig', 'w') as fs, open(prefix + '.pts', 'w') as fp:
        for fn in files:
            cnt = 0
            for line in open(fn):
                t = line.split()
                if not t:
                    continue
                tag, label, h, n = t[0], t[1], t[2], int(t[3])
                vals = list(map(int, t[4:]))
                assert len(vals) == 2 * n, (fn, label)
                pts = [(vals[2 * a], vals[2 * a + 1]) for a in range(n)]
                if rot:
                    pts = [(-y, x) for x, y in pts]
                assert len(set(pts)) == n
                spts, signs, sh = to_sig(pts)
                nshear += sh
                fs.write(f"{nid} {tag} {label} {h} {n} {signs}\n")
                fp.write(f"{nid} {n} " + " ".join(f"{x} {y}" for x, y in spts) + "\n")
                nid += 1
                cnt += 1
            per_file[fn.split('/')[-1]] = cnt
    meta = {"sets": nid, "sheared": nshear, "rot90": rot, "per_file": per_file}
    json.dump(meta, open(prefix + '.meta.json', 'w'), indent=1)
    print(json.dumps(meta))


if __name__ == '__main__':
    main()
