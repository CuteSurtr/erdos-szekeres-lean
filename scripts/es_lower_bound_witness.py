#!/usr/bin/env python3
"""Exact integer witnesses for the Erdős–Szekeres lower bound.

This mirrors the construction proved in ErdosSzekeres/LowerBound: blocks with
no k-cup and no l-cap are stacked upward, and the blocks (n - i, i + 2) are
stacked downward. Each stacking translates the second block by the least
horizontal offset that places it to the right, and then by the least positive
vertical offset that realizes the required mixed-triple signs.

The script is an independent numerical check, not part of the proof. It
verifies general position and computes the largest subset in convex position
with an exact O(N^4) dynamic program, which must equal n - 1.
"""
import argparse
from fractions import Fraction
from functools import cmp_to_key
from itertools import combinations
import json
import math
import sys


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def stack(sign, left, right):
    """Translate `right` by (t, sign * m) so that it is stacked on `left`."""
    t = max(p[0] for p in left) - min(p[0] for p in right) + 1
    moved = [(x + t, y) for x, y in right]
    # sign * orient(a, a', b + (0, sign*m)) = (a'x - ax) m + sign * orient(a, a', b).
    # sign * orient(a, b + w, b' + w) = -(b'x - bx) m + sign * orient(a, b, b').
    need = Fraction(0)
    for a, a2 in combinations(sorted(left), 2):
        for b in moved:
            need = max(need, Fraction(-sign * orient(a, a2, b), a2[0] - a[0]))
    for a in left:
        for b, b2 in combinations(sorted(moved), 2):
            need = max(need, Fraction(sign * orient(a, b, b2), b2[0] - b[0]))
    m = math.floor(need) + 1
    return left + [(x, y + sign * m) for x, y in moved]


def cup_cap_free(k, l, cache={}):
    """Choose(k + l - 4, k - 2) points with no k-cup and no l-cap."""
    if (k, l) not in cache:
        if k == 2 or l == 2:
            cache[k, l] = [(0, 0)]
        else:
            cache[k, l] = stack(1, cup_cap_free(k - 1, l), cup_cap_free(k, l - 1))
    return cache[k, l]


def witness(n):
    """2^(n-2) points in general position with no convex n-gon."""
    points = cup_cap_free(n, 2)
    for j in range(1, n - 1):
        points = stack(-1, points, cup_cap_free(n - j, j + 2))
    return points


def general_position(points):
    return all(orient(a, b, c) != 0 for a, b, c in combinations(points, 3))


def largest_convex_subset(points):
    """Exact size of a largest subset in convex position (general position assumed)."""
    best = min(len(points), 2)
    for p in points:
        # p is the lowest vertex (ties broken by x); the others are sorted by angle.
        above = [q for q in points if (q[1], q[0]) > (p[1], p[0])]
        # Exact angular order: all points lie in the half-plane above p.
        q = sorted(above, key=cmp_to_key(lambda a, b: -1 if orient(p, a, b) > 0 else 1))
        m = len(q)
        # chain[j][i]: longest convex chain p, ..., q[j], q[i] with j < i.
        chain = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i):
                value = 3
                for k in range(j):
                    if chain[k][j] and orient(q[k], q[j], q[i]) > 0:
                        value = max(value, chain[k][j] + 1)
                chain[j][i] = value
                if orient(q[j], q[i], p) > 0:
                    best = max(best, value)
    return best


def check(n):
    points = witness(n)
    assert len(points) == len(set(points)) == 2 ** (n - 2)
    assert len({x for x, _ in points}) == len(points)
    assert general_position(points)
    size = largest_convex_subset(points)
    return points, size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int, nargs="?", default=8)
    parser.add_argument("--json", action="store_true", help="print the coordinates")
    args = parser.parse_args()
    if args.n < 3:
        parser.error("n must be at least 3")
    points, size = check(args.n)
    if args.json:
        json.dump(points, sys.stdout)
        print()
    print(f"n={args.n}: {len(points)} points in general position; "
          f"largest convex subset has {size} points",
          file=sys.stderr if args.json else sys.stdout)
    return 0 if size == args.n - 1 else 1


if __name__ == "__main__":
    sys.exit(main())
