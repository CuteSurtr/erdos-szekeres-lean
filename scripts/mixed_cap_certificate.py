#!/usr/bin/env python3
"""Replay the 22-point mixed-cap obstruction, independently of its Lean proof."""
import json
from itertools import combinations
from math import comb

from search import general_position, hull, largest_convex_subset, orient


def fixture():
    anchors = [(10000 * i, -100000 * i * i) for i in range(6)]
    chain = [(15000 + 100 * t, -200000 - 4900 * t + t * t) for t in range(8)]
    inner = [(35000 + 100 * t, -1200000 - 7000 * t - t * t) for t in range(8)]
    return anchors, chain, inner


def interior(p, a, b, c):
    area = orient(a, b, c)
    return all(area * value > 0 for value in
               (orient(a, b, p), orient(b, c, p), orient(c, a, p)))


def in_closed_triangle(p, a, b, c):
    area = orient(a, b, c)
    return area != 0 and all(area * value >= 0 for value in
                            (orient(a, b, p), orient(b, c, p), orient(c, a, p)))


def spike(frame, p):
    a, b, c, d = frame
    return orient(a, b, p) < 0 < orient(b, c, p) and orient(c, d, p) < 0


def obstruction_certificates(anchors, chain, inner):
    """Each tuple lists the interior point followed by its enclosing triangle."""
    for p, q, r in combinations(chain, 3):
        for t in inner:
            yield q, p, r, t
    for p, q in combinations(chain, 2):
        for t in inner:
            yield q, p, anchors[2], t


def verify(anchors, chain, inner):
    points = anchors + chain + inner
    if (len(anchors), len(chain), len(inner)) != (6, 8, 8):
        raise ValueError("This certificate has six anchors and two eight-point caps")
    first, last = anchors[:4], anchors[2:]
    checks = {
        "general_position": general_position(points),
        "distinct_x": len({p[0] for p in points}) == len(points),
        "clockwise_anchors": all(orient(*triple) < 0 for triple in combinations(anchors, 3)),
        "vertical_spike": all(spike(first, p) for p in chain),
        "horizontal_spike": all(spike(last, p) for p in inner),
        "vertical_chain_order": all(in_closed_triangle(q, first[0], first[3], p)
                                    for p, q in combinations(chain, 2)),
        "left_cap": len(hull(chain + [first[2]])) == 9,
        "horizontal_antichain": all(
            not in_closed_triangle(q, last[0], last[3], p)
            for p in inner for q in inner if p != q),
    }
    supports = []
    for p in inner:
        q = next((q for q in inner if p != q and all(
            orient(p, q, last[0]) * orient(p, q, z) > 0
            for z in inner if z not in (p, q))), None)
        supports.append(q)
    checks["inner_cap_supports"] = all(q is not None for q in supports)
    certificates = list(obstruction_certificates(anchors, chain, inner))
    checks["interior_certificates"] = all(interior(*c) for c in certificates)
    if not all(checks.values()):
        raise ValueError(f"Invalid certificate: {[k for k, v in checks.items() if not v]}")

    # Independent of the structural cardinality argument and the dynamic program.
    checked = 0
    for subset in combinations(points, 16):
        checked += 1
        if len(hull(subset)) == 16:
            raise ValueError("A convex 16-gon contradicts the proposed certificate")
    witness = anchors + inner + [chain[-1]]
    if len(hull(witness)) != 15:
        raise ValueError("The proposed 15-gon is not convex")
    dp_witness = largest_convex_subset(points)
    if len(dp_witness) != 15:
        raise ValueError("The dynamic program disagrees with exhaustive verification")
    return {
        "scope": "Counterexample to unconditional mixed-cap addition; not to Erdős–Szekeres",
        "anchors": anchors,
        "vertical_cap": chain,
        "inner_cap": inner,
        "frame_indices_zero_based": [0, 2],
        "checks": checks,
        "inner_support_vertices": supports,
        "interior_certificate_count": len(certificates),
        "certificate_patterns": [
            "C[j] lies inside triangle(C[i], C[k], T[t]) for i < j < k",
            "C[j] lies inside triangle(C[i], A[2], T[t]) for i < j",
        ],
        "ambient_cardinality": len(points),
        "cap_cardinality_sum": len(chain) + len(inner),
        "maximum_convex_cardinality": 15,
        "maximum_witness": hull(witness),
        "sixteen_subsets_checked": checked,
        "sixteen_subsets_total": comb(len(points), 16),
        "lean_theorem": "ErdosSzekeres.HMPT.MixedCap.mixed_cap_budget_counterexample",
        "verification": "Exact Python replay; separate Lean proof checks all geometric hypotheses and the cardinality argument",
    }


if __name__ == "__main__":
    print(json.dumps(verify(*fixture()), indent=2, ensure_ascii=False))
