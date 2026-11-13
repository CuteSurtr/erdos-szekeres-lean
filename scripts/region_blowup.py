#!/usr/bin/env python3
"""Exact experiments on simultaneous local HMPT extremal parameters.

These explicit clusters attain height times width and both cups-caps binomials.
Their largest convex subsets are also measured; attaining the local factors
does not establish the polygon-avoidance hypothesis of the global bound.
"""
import argparse
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from math import comb

from mixed_cap_certificate import in_closed_triangle, spike
from search import general_position, hull, largest_convex_subset, orient


@lru_cache(None)
def cups_caps(a, b):
    """Classical recursive configuration with maximum cup a and maximum cap b."""
    if a < 1 or b < 1:
        raise ValueError("Positive cup/cap parameters required")
    if a == 1 or b == 1:
        return ((0, 0),)
    left, right = cups_caps(a - 1, b), cups_caps(a, b - 1)
    size = len(left) + len(right)
    height = max(abs(y) for _, y in left + right) + 1
    shift = 10 * size * height
    return left + tuple((x + len(left), y + shift) for x, y in right)


def configuration(a, b, c, d):
    if min(a, b, c, d) < 2:
        raise ValueError("All four cap parameters must be at least two")
    vertical, horizontal = cups_caps(a, b), cups_caps(d, c)
    v = len(vertical)
    outer_scale = 10000 * (max(abs(y) for _, y in vertical) + 1)
    flatten = 100 * (max(abs(y) for _, y in horizontal) + 1)
    local = [(x * flatten, -30 * x * flatten + y) for x, y in horizontal]
    cluster_scale = 100000 * (max(max(abs(x), abs(y)) for x, y in local) + 1)
    anchors = [(10000 * i * v * outer_scale * cluster_scale,
                -100000 * i * i * v * outer_scale * cluster_scale) for i in range(4)]
    centers = [((15000 * v + 1000 * x) * outer_scale,
                (-200000 * v - 49000 * x) * outer_scale + y) for x, y in vertical]
    groups = [[(px * cluster_scale + x, py * cluster_scale + y) for x, y in local]
              for px, py in centers]
    return anchors, groups


def monotone_convex_chain(points, positive):
    """Longest cup or cap in x-order, with an explicitly checked witness."""
    points = sorted(points)
    best = tuple(points[:2])
    paths = {}
    for j in range(len(points)):
        for i in range(j):
            path = (points[i], points[j])
            for h in range(i):
                area = orient(points[h], points[i], points[j])
                if area != 0 and (area > 0) == positive:
                    previous = paths[h, i]
                    if len(previous) + 1 > len(path):
                        path = previous + (points[j],)
            paths[i, j] = path
            if len(path) > len(best):
                best = path
    if not all((orient(*t) > 0) == positive and orient(*t) != 0 for t in combinations(best, 3)):
        raise AssertionError("Monotone-chain witness is not monochromatic")
    return best


def inner_supported(points, anchor):
    return all(any(p != q and all(orient(p, q, anchor) * orient(p, q, z) > 0
                                 for z in points if z not in (p, q))
                   for q in points) for p in points)


def profile(a, b, c, d):
    anchors, groups = configuration(a, b, c, d)
    points = sum(groups, [])
    ambient = anchors + points
    v, h = len(groups), len(groups[0])
    checks = {
        "general_position": general_position(ambient),
        "all_points_in_spike": all(spike(anchors, p) for p in points),
        "between_groups_chain": all(
            in_closed_triangle(q, anchors[0], anchors[3], p)
            for i in range(v) for j in range(i + 1, v) for p in groups[i] for q in groups[j]),
        "within_groups_antichain": all(
            not in_closed_triangle(q, anchors[0], anchors[3], p) and
            not in_closed_triangle(p, anchors[0], anchors[3], q)
            for group in groups for p, q in combinations(group, 2)),
    }
    chain = [group[0] for group in groups]
    left = monotone_convex_chain(chain, True)
    right = monotone_convex_chain(chain, False)
    checks["vertical_left_attained"] = len(left) == a and len(hull(left + (anchors[2],))) == a + 1
    checks["vertical_right_attained"] = len(right) == b and len(hull(right + (anchors[1],))) == b + 1
    checks["vertical_left_maximal"] = all(len(hull(s + (anchors[2],))) < a + 2
                                          for s in combinations(chain, a + 1))
    checks["vertical_right_maximal"] = all(len(hull(s + (anchors[1],))) < b + 2
                                           for s in combinations(chain, b + 1))
    horizontal = groups[0]
    inner = monotone_convex_chain(horizontal, False)
    outer = monotone_convex_chain(horizontal, True)
    checks["inner_attained"] = len(inner) == c and inner_supported(inner, anchors[0])
    # Exhaust every larger candidate, without assuming that the support predicate is hereditary.
    checks["inner_maximal"] = all(not inner_supported(s, anchors[0])
                                  for size in range(c + 1, h + 1)
                                  for s in combinations(horizontal, size))
    checks["outer_attained"] = len(outer) == d
    checks["outer_maximal"] = all(any(orient(*t) < 0 for t in combinations(s, 3))
                                  for s in combinations(horizontal, d + 1))
    checks["height_width_product_attained"] = len(points) == v * h
    checks["vertical_binomial_attained"] = v == comb(a + b - 2, a - 1)
    checks["horizontal_binomial_attained"] = h == comb(c + d - 2, c - 1)
    if not all(checks.values()):
        raise AssertionError([name for name, value in checks.items() if not value])
    maximum = largest_convex_subset(ambient)
    local_maximum = largest_convex_subset(points)
    exhaustive = None
    if len(ambient) <= 22:
        size = len(maximum) + 1
        checked = 0
        for subset in combinations(ambient, size):
            checked += 1
            if len(hull(subset)) == size:
                raise AssertionError("Exhaustive hull check contradicts the dynamic program")
        exhaustive = {"gon": size, "subsets_checked": checked}
    return {
        "parameters": {"left": a, "right": b, "inner": c, "outer": d},
        "region_size": len(points), "height": v, "width": h,
        "checks": checks,
        "largest_local_convex_subset": len(local_maximum),
        "largest_ambient_convex_subset": len(maximum),
        "convex_witness_labels": [ambient.index(p) for p in hull(maximum)],
        "exhaustive_upper_check": exhaustive,
        "coordinate_sha256": hashlib.sha256(json.dumps(ambient).encode()).hexdigest(),
        "verification": "Exact integer predicates and dynamic programs; small cases exhaustively cross-checked; not Lean-certified",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parameters", type=int, nargs=4, metavar=("A", "B", "C", "D"))
    args = parser.parse_args()
    cases = [args.parameters] if args.parameters else [
        (2, 2, 2, 2), (3, 3, 2, 2), (3, 3, 2, 3), (3, 3, 3, 3),
        (3, 3, 2, 5), (4, 4, 2, 2), (4, 4, 2, 3), (4, 4, 3, 3), (4, 4, 2, 5)]
    print(json.dumps({"scope": "Structured examples, not a universal bound or stability theorem",
                      "profiles": [profile(*case) for case in cases]}, indent=2))
