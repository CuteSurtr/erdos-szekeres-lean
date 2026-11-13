#!/usr/bin/env python3
"""Exact integer-grid experiments, not a proof over arbitrary real configurations."""
import argparse
import json
from functools import cmp_to_key
from itertools import combinations, product
from math import comb


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def general_position(points):
    return len(set(points)) == len(points) and all(
        orient(*triple) != 0 for triple in combinations(points, 3)
    )


def hull(points):
    """Andrew's monotone chain; discard collinear non-extreme boundary points."""
    ordered = sorted(set(points))
    if len(ordered) <= 1:
        return ordered

    def chain(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and orient(out[-2], out[-1], p) <= 0:
                out.pop()
            out.append(p)
        return out

    return chain(ordered)[:-1] + chain(reversed(ordered))[:-1]


def convex_subset(points, k):
    if k < 3:
        raise ValueError("A polygon must have at least three vertices")
    return next((s for s in combinations(points, k) if len(hull(s)) == k), None)


def largest_convex_subset(points):
    """Exact O(n^4) dynamic program for general-position input.

    Choose the lowest vertex, order the remaining upper-half-plane points by
    angle, and extend chains with strictly left turns. Angular order makes each
    chain simple, and the lowest vertex makes both closing turns left turns.
    Keep a witness, so positive findings can be checked independently by hull().
    """
    if not general_position(points):
        raise ValueError("The dynamic program requires general position")
    ordered = sorted(points, key=lambda p: (p[1], p[0]))
    best = tuple(ordered[:2])
    for pivot_index, pivot in enumerate(ordered):
        around = sorted(ordered[pivot_index + 1:], key=cmp_to_key(
            lambda a, b: -1 if orient(pivot, a, b) > 0 else 1))
        paths = {}
        for j in range(len(around)):
            for i in range(j):
                path = (pivot, around[i], around[j])
                for h in range(i):
                    if orient(around[h], around[i], around[j]) > 0:
                        previous = paths[h, i]
                        if len(previous) + 1 > len(path):
                            path = previous + (around[j],)
                paths[i, j] = path
                if len(path) > len(best):
                    best = path
    if len(hull(best)) != len(best):
        raise AssertionError("Dynamic-program witness is not convex")
    return best


def search_grid(side, size, k):
    if side < 1 or not 3 <= k <= size <= side * side:
        raise ValueError("Require side >= 1 and 3 <= gon <= points <= side²")
    grid = list(product(range(side), repeat=2))
    checked = in_general_position = 0
    witness = None
    for points in combinations(grid, size):
        checked += 1
        if not general_position(points):
            continue
        in_general_position += 1
        if convex_subset(points, k) is None:
            witness = points
            break
    return {
        "scope": "integer grid only; not all planar order types",
        "grid_side": side,
        "points": size,
        "gon": k,
        "total_grid_subsets": comb(side * side, size),
        "checked_subsets": checked,
        "general_position_subsets_checked": in_general_position,
        "grid_exhausted": checked == comb(side * side, size),
        "avoiding_configuration": witness,
        "verification": "exact Python integer arithmetic; not Lean-certified",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid", type=int, default=4)
    parser.add_argument("--points", type=int, default=5)
    parser.add_argument("--gon", type=int, default=4)
    args = parser.parse_args()
    print(json.dumps(search_grid(args.grid, args.points, args.gon), indent=2))
